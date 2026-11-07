from repair_common import *
from propagate_matched_feedback import solve_response
from decimal import Decimal,localcontext


def decimal_gas(heat,alpha,gas,history,rate,temperature,stiffness,photon,external):
    with localcontext() as context:
        context.prec=60
        convert=lambda value:Decimal.from_float(float(value))
        temp=[convert(value) for value in temperature]
        delta=[convert(value)-weight*convert(gas) for value,weight in zip(photon,temp)]
        physical=[sum((convert(coefficient)*value for coefficient,value in zip(row,delta)),Decimal(0))+convert(force) for row,force in zip(stiffness,external)]
        transfer=convert(rate)*sum((weight*value for weight,value in zip(temp,physical)),Decimal(0))
        balance=convert(heat)*((convert(alpha)+1)*convert(gas)-convert(history))+transfer
        return float(balance)


def main():
    modest()
    folder=ROOT/'results/budget-audit'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=list(ladder.inputs)
    checks,rows,coefficient_rows=[],[],[]
    event_base=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'
    physical_eigenvalues=[]
    for epoch in range(65):
        path=event_base/f'epoch-{epoch:02d}.npz'
        packet=read_npz(path)
        inputs.append(path)
        physical_eigenvalues.append(float(packet['rates']@(-np.expm1(-np.log(packet['ratios'])))))
    physical_eigenvalues=np.array(physical_eigenvalues)
    for model in ['heavy','cold']:
        for variant in ['fine','space']:
            path=ROOT/'results'/f'inner-{model}-{variant}-p4-n5120/prediction.npz'
            inner=read_npz(path)
            inputs.append(path)
            coefficient_at=interpolate.interp1d(inner['coefficient_knots'],inner['coefficient_bank'],axis=0,bounds_error=True)
            eigenvalues=coefficient_at(inner['coordinate'])[:,len(inner['offsets'])]
            error=float(np.max(abs(eigenvalues-physical_eigenvalues)/np.maximum(abs(physical_eigenvalues),1e-300)))
            coefficient_rows.append(dict(model=model,variant=variant,knots=len(inner['coefficient_knots']),frequency_nodes=len(inner['frequency']),
                minimum=float(inner['frequency'][0]),maximum=float(inner['frequency'][-1]),physical_eigenvalue_relative_difference=error))
            checks.append(check('Saved physical-event eigenvalue versus lower-order coefficient:'+model+':'+variant,error,1e-9))
    for upper,order in [(.04,8),(.02,6)]:
        for model in ['heavy','cold']:
            label=f'fine-p4-n5120-o{order}-q32-m{int(upper*1000)}'
            source_path=ROOT/'results'/('sources-'+label)/(model+'.npz')
            response_path=ROOT/'results'/('response-'+label+'-r2048')/(model+'.npz')
            local_packet(source_path.parent)
            local_packet(response_path.parent)
            inputs.extend([source_path,response_path,source_path.parent/'status.json',response_path.parent/'status.json'])
            source=read_npz(source_path)
            saved=read_npz(response_path)
            background=thermal_wave.thermal.ThermalBackground(model)
            emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
            inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
            solution,errors=solve_response(model,source,2048,ladder,emission,background)
            sampled=solution['photon'][saved['saved_step_indices']]
            scale=np.maximum(photon_norm(saved['photon'],basis.mass).max(axis=0),1e-300)
            replay=float(np.max(photon_norm(sampled-saved['photon'],basis.mass)/scale))
            checks.append(check('Exact saved response replay:'+model+f':m{int(upper*1000)}',replay,1e-12))
            forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
            step=(source['coordinate'][-1]-source['coordinate'][0])/2048
            maximum=np.zeros(12)
            worst=[None]*12
            for index in range(1,2049):
                position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*index/2048)
                local=background.at(position)
                theta=local['thermal_parameter']
                rate=local['coefficient']/theta
                stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
                pieces=forcing(position)
                external=np.column_stack([pieces.sum(axis=0),*pieces])
                alpha=(1. if index==1 else 1.5)/step
                gas=solution['gas'][index]
                history=solution['gas'][index-1]/step if index==1 else (2*solution['gas'][index-1]-.5*solution['gas'][index-2])/step
                photon=solution['photon'][index]
                physical=stiffness@(photon-basis.temperature[:,None]*gas)+external
                residual=background.chi*((alpha+1)*gas-history)+rate*basis.temperature@physical
                denominator=np.maximum(abs(background.chi*(alpha+1)*gas)+abs(background.chi*history)+abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
                ratios=abs(residual)/denominator
                for column in np.flatnonzero(ratios>maximum):
                    maximum[column]=ratios[column]
                    rounding_scale=background.chi*(abs((alpha+1)*gas[column])+abs(history[column]))+abs(rate)*abs(basis.temperature)@(abs(stiffness)@(abs(photon[:,column])+abs(basis.temperature*gas[column]))+abs(external[:,column]))
                    worst[column]=dict(step=index,coordinate=position,alpha=alpha,rate=rate,
                        gas=float(gas[column]),history=float(history[column]),denominator=float(denominator[column]),
                        raw_residual=float(residual[column]),operation_scale=float(rounding_scale),
                        stiffness=stiffness.copy(),photon=photon[:,column].copy(),external=external[:,column].copy())
            diagnostic=[]
            for column in sorted(set([0,1,2,int(np.argmax(maximum))])):
                witness=worst[column]
                precise=decimal_gas(background.chi,witness['alpha'],witness['gas'],witness['history'],witness['rate'],basis.temperature,
                    witness['stiffness'],witness['photon'],witness['external'])
                retained={key:value for key,value in witness.items() if key not in ['stiffness','photon','external']}
                retained.update(column=column,raw_relative=float(maximum[column]),
                    decimal_relative=abs(precise)/witness['denominator'],decimal_residual=precise,
                    double_eps_operation_scale=np.finfo(float).eps*witness['operation_scale'])
                diagnostic.append(retained)
            rows.append(dict(model=model,upper=upper,maximum_raw_gas_relative_by_column=maximum.tolist(),
                reference_raw_gas_relative=errors['gas'],precision_witnesses=diagnostic))
            print(json.dumps(dict(model=model,upper=upper,gas_all=float(maximum.max()),gas_total=maximum[:3].tolist(),witnesses=diagnostic)),flush=True)
            del solution
    windows=[]
    for model in ['heavy','cold']:
        wide=read_npz(ROOT/'results/response-fine-p4-n5120-o8-q32-m40-r2048'/(model+'.npz'))
        narrow=read_npz(ROOT/'results/response-fine-p4-n5120-o6-q32-m20-r2048'/(model+'.npz'))
        windows.append(dict(model=model,relative_radiation_difference=(norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure)).tolist(),
            final_gas_ratio=(narrow['gas'][-1,:3]/wide['gas'][-1,:3]).tolist()))
    finish(folder,dict(checks=checks,coefficient_rows=coefficient_rows,gas_rows=rows,window_rows=windows,
        raw_gas_gate_relaxed=False,decimal_precision=60,decimal_scope='Stored double input matrices and states re-evaluated;not a high-precision evolution',
        baseline_and_correction_both_tested=True),__file__,inputs)


if __name__=='__main__':
    main()
