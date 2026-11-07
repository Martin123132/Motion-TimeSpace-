from finer_common import *
import mpmath as mp
import argparse
import time


def solve_precise(data,digits):
    with mp.workdps(digits):
        convert=lambda value:mp.mpf(float(value))
        mass=mp.matrix(data['mass'].tolist())
        stiffness=mp.matrix(data['stiffness'].tolist())
        temperature=mp.matrix(data['temperature'].tolist())
        step=convert(data['step'])
        first=int(data['index'])==1
        alpha=(mp.mpf(1) if first else mp.mpf('1.5'))/step
        history=mp.matrix(data['previous_photon'].tolist())/step if first else (2*mp.matrix(data['previous_photon'].tolist())-mp.mpf('.5')*mp.matrix(data['older_photon'].tolist()))/step
        gas_history=mp.matrix([data['previous_gas'].tolist()])/step if first else (2*mp.matrix([data['previous_gas'].tolist()])-mp.mpf('.5')*mp.matrix([data['older_gas'].tolist()]))/step
        rate,heat=convert(data['rate']),convert(data['heat'])
        external=mp.matrix(data['external'].tolist())
        spectral=alpha*mass-rate*stiffness
        column=rate*stiffness*temperature
        row=rate*temperature.T*stiffness
        diagonal=heat*(alpha+1)-(row*temperature)[0]
        matrix=mp.matrix(97,97)
        for index in range(96):
            for other in range(96):
                matrix[index,other]=spectral[index,other]
            matrix[index,96]=column[index]
            matrix[96,index]=row[index]
        matrix[96,96]=diagonal
        right_spectral=mass*history+rate*external
        right_gas=heat*gas_history-rate*temperature.T*external
        right=mp.matrix(97,external.cols)
        for index in range(96):
            for branch in range(external.cols):
                right[index,branch]=right_spectral[index,branch]
        for branch in range(external.cols):
            right[96,branch]=right_gas[branch]
        combined,pivots=mp.mp.LU_decomp(matrix)
        solved=mp.matrix(97,external.cols)
        for branch in range(external.cols):
            answer=mp.mp.U_solve(combined,mp.mp.L_solve(combined,right.column(branch),pivots))
            for index in range(97):
                solved[index,branch]=answer[index]
        photon=solved[:96,:]
        gas=solved[96:97,:]
        physical=stiffness*(photon-temperature*gas)+external
        photon_residual=mass*(alpha*photon-history)-rate*physical
        gas_residual=heat*((alpha+1)*gas-gas_history)+rate*temperature.T*physical
        photon_errors,gas_errors=[],[]
        for branch in range(external.cols):
            scale=mp.norm(mass*history.column(branch))+mp.norm(rate*physical.column(branch))+mp.norm(alpha*mass*photon.column(branch))
            photon_errors.append(float(mp.norm(photon_residual.column(branch))/max(scale,mp.mpf('1e-300'))))
            gas_scale=abs(heat*(alpha+1)*gas[branch])+abs(heat*gas_history[branch])+abs(rate)*mp.fsum(abs(temperature[index])*abs(physical[index,branch]) for index in range(96))
            gas_errors.append(float(abs(gas_residual[branch])/max(gas_scale,mp.mpf('1e-300'))))
        return dict(digits=digits,photon_relative=photon_errors,gas_relative=gas_errors,
            solution=[[mp.nstr(solved[index,branch],digits) for branch in range(external.cols)] for index in range(97)])


def precision_difference(first,second):
    with mp.workdps(80):
        lower=mp.matrix(first['solution'])
        higher=mp.matrix(second['solution'])
        photon,gas=[],[]
        for branch in range(higher.cols):
            photon.append(float(mp.norm(lower[:96,branch]-higher[:96,branch])/max(mp.norm(higher[:96,branch]),mp.mpf('1e-300'))))
            gas.append(float(abs(lower[96,branch]-higher[96,branch])/max(abs(higher[96,branch]),mp.mpf('1e-300'))))
        return photon,gas


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'gas-precision-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    source_folder=ROOT/'results'/f'feedback-m{int(args.upper*1000)}-n5120'
    local_packet(source_folder)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,source_folder/'status.json']
    checks,rows,selections=[],[],{}
    for model in ['heavy','cold']:
        source_path=source_folder/(model+'-source.npz')
        response_path=source_folder/(model+'-response.npz')
        source,response=read_npz(source_path),read_npz(response_path)
        inputs.extend([source_path,response_path])
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
        step=(source['coordinate'][-1]-source['coordinate'][0])/2048
        maximum=np.zeros(12)
        worst=np.ones(12,dtype=int)
        for index in range(1,2049):
            position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*index/2048)
            local=background.at(position)
            theta,rate=local['thermal_parameter'],local['coefficient']/local['thermal_parameter']
            stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
            pieces=forcing(position)
            external=np.column_stack([pieces.sum(axis=0),*pieces])
            alpha=(1. if index==1 else 1.5)/step
            gas=response['gas'][index]
            history=response['gas'][index-1]/step if index==1 else (2*response['gas'][index-1]-.5*response['gas'][index-2])/step
            physical=stiffness@(response['photon'][index]-basis.temperature[:,None]*gas)+external
            residual=background.chi*((alpha+1)*gas-history)+rate*basis.temperature@physical
            scale=np.maximum(abs(background.chi*(alpha+1)*gas)+abs(background.chi*history)+abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
            ratios=abs(residual)/scale
            changed=ratios>maximum
            maximum[changed]=ratios[changed]
            worst[changed]=index
        global_column=int(np.argmax(maximum))
        columns=np.array(sorted(set([0,1,2,global_column])),dtype=int)
        selected_steps=sorted(set(int(index) for index in [1,*worst[:3],worst[global_column]]))
        selections[model]=dict(raw_maximum_by_column=maximum.tolist(),worst_step_by_column=worst.tolist(),
            chosen_columns=columns.tolist(),chosen_steps=[int(index) for index in selected_steps])
        peak_gas=np.maximum(abs(response['gas'][:,columns]).max(axis=0),1e-300)
        peak_photon=np.maximum(photon_norm(response['photon'][:,:,columns],basis.mass).max(axis=0),1e-300)
        for index in selected_steps:
            position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*index/2048)
            local=background.at(position)
            theta,rate=local['thermal_parameter'],local['coefficient']/local['thermal_parameter']
            stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
            pieces=forcing(position)
            external=np.column_stack([pieces.sum(axis=0),*pieces])[:,columns]
            data=dict(mass=basis.mass,stiffness=stiffness,temperature=basis.temperature,step=step,index=index,
                rate=rate,heat=background.chi,external=external,
                previous_photon=response['photon'][index-1][:,columns],older_photon=response['photon'][max(0,index-2)][:,columns],
                previous_gas=response['gas'][index-1,columns],older_gas=response['gas'][max(0,index-2),columns],
                old_photon=response['photon'][index][:,columns],old_gas=response['gas'][index,columns],columns=columns)
            label=f'{model}-step{index:04d}'
            np.savez_compressed(folder/(label+'-inputs.npz'),**data)
            lower=solve_precise(data,50)
            higher=solve_precise(data,70)
            write_json(folder/(label+'-digits50.json'),lower)
            write_json(folder/(label+'-digits70.json'),higher)
            photon_difference,gas_difference=precision_difference(lower,higher)
            values=np.array(higher['solution'],dtype=float)
            gas_change=abs(values[96]-data['old_gas'])
            photon_change=photon_norm(values[:96]-data['old_photon'],basis.mass)
            alpha=(1. if index==1 else 1.5)/step
            history=data['previous_gas']/step if index==1 else (2*data['previous_gas']-.5*data['older_gas'])/step
            physical=stiffness@(values[:96]-basis.temperature[:,None]*values[96])+external
            residual=background.chi*((alpha+1)*values[96]-history)+rate*basis.temperature@physical
            scale=np.maximum(abs(background.chi*(alpha+1)*values[96])+abs(background.chi*history)+abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
            cast_error=abs(residual)/scale
            for precision,result in [(50,lower),(70,higher)]:
                for channel in ['photon','gas']:
                    checks.append(check(f'{label}:digits{precision}:{channel}',max(result[channel+'_relative']),1e-35))
            checks.extend([check(label+':50to70 photon',max(photon_difference),1e-25),check(label+':50to70 gas',max(gas_difference),1e-25)])
            for column,value in zip(columns,cast_error):
                checks.append(check(f'{label}:cast-to-double raw gas column{column}',value,1e-7))
            record=dict(model=model,upper=args.upper,step=index,columns=columns.tolist(),
                photon50to70=photon_difference,gas50to70=gas_difference,
                high_precision_photon_error=higher['photon_relative'],high_precision_gas_error=higher['gas_relative'],
                cast_raw_gas_relative=cast_error.tolist(),gas_change_over_old_local=(gas_change/np.maximum(abs(data['old_gas']),1e-300)).tolist(),
                gas_change_over_old_peak=(gas_change/peak_gas).tolist(),photon_change_over_old_peak=(photon_change/peak_photon).tolist(),
                input_path=str(folder/(label+'-inputs.npz')))
            rows.append(record)
            write_json(folder/'progress.json',dict(state='running',completed_witnesses=len(rows),last=label,seconds=time.monotonic()-started))
            print(json.dumps(dict(witness=label,gas70=max(higher['gas_relative']),precision=max(gas_difference),
                gas_state_peak=float(max(gas_change/peak_gas)),seconds=time.monotonic()-started)),flush=True)
    write_json(folder/'progress.json',dict(state='complete',completed_witnesses=len(rows)))
    finish(folder,dict(checks=checks,rows=rows,selections=selections,upper=args.upper,precision_digits=[50,70],
        full_coupled97_step_solved=True,original_equations_not_energy_ledger_only=True,
        preceding_states_and_coefficients_are_saved_doubles=True,full_high_precision_evolution=False,
        raw_gas_gate_relaxed=False,cast_failures_retained=True,mpmath_version=mp.__version__,seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
