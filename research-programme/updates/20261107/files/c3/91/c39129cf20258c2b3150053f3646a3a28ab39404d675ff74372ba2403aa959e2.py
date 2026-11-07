from seven_eighths_history_common import *
from replay_saved_response import solve_response_trace
from check_gas_precision import solve_precise,precision_difference
import mpmath as mp
import time


def gas_residual_precise(data,photon_values,gas_values,digits):
    with mp.workdps(digits):
        stiffness=mp.matrix(data['stiffness'].tolist())
        temperature=mp.matrix(data['temperature'].tolist())
        photon=mp.matrix(photon_values.tolist())
        gas=mp.matrix([gas_values.tolist()])
        external=mp.matrix(data['external'].tolist())
        step=mp.mpf(float(data['step']))
        first=int(data['index'])==1
        alpha=(mp.mpf(1) if first else mp.mpf('1.5'))/step
        history=mp.matrix([data['previous_gas'].tolist()])/step if first else (2*mp.matrix([data['previous_gas'].tolist()])-mp.mpf('.5')*mp.matrix([data['older_gas'].tolist()]))/step
        heat,rate=mp.mpf(float(data['heat'])),mp.mpf(float(data['rate']))
        physical=stiffness*(photon-temperature*gas)+external
        residual=heat*((alpha+1)*gas-history)+rate*temperature.T*physical
        values=[]
        for column in range(gas.cols):
            scale=abs(heat*(alpha+1)*gas[column])+abs(heat*history[column])+abs(rate)*mp.fsum(abs(temperature[index])*abs(physical[index,column]) for index in range(96))
            values.append(float(abs(residual[column])/max(scale,mp.mpf('1e-300'))))
        return values


def gas_residual_double(data,photon,gas):
    step=float(data['step'])
    alpha=(1. if int(data['index'])==1 else 1.5)/step
    history=data['previous_gas']/step if int(data['index'])==1 else (2*data['previous_gas']-.5*data['older_gas'])/step
    physical=data['stiffness']@(photon-data['temperature'][:,None]*gas)+data['external']
    residual=data['heat']*((alpha+1)*gas-history)+data['rate']*data['temperature']@physical
    scale=np.maximum(abs(data['heat']*(alpha+1)*gas)+abs(data['heat']*history)+abs(data['rate'])*abs(data['temperature'])@abs(physical),1e-300)
    return abs(residual)/scale


def expected_trace_source():
    path=BRANCH/'matched-low-frequency-feedback-20261012/propagate_matched_feedback.py'
    source=path.read_text(encoding='utf-8')
    body=source[source.index('def solve_response('):source.index('\ndef readout(')].rstrip()
    body=body.replace('def solve_response(model,source,steps,ladder,emission,background):',
        'def solve_response_trace(model,source,steps,ladder,emission,background,trace):')
    original="        errors['gas']=max(errors['gas'],float(np.max(abs(gas_residual)/gas_scale)))"
    assert body.count(original)==1
    body=body.replace(original,original+'\n        if trace is not None:\n            trace(index,photon,abs(gas_residual)/gas_scale)')
    return 'from seven_eighths_history_common import *\nfrom matched_feedback_common import EnergyCoordinates\n\n\n'+body+'\n'


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/saved-gas-residual'
    folder.mkdir(parents=True,exist_ok=False)
    assert (ROOT/'replay_saved_response.py').read_text(encoding='utf-8')==expected_trace_source()
    checks=[dict(name='Tracing copy changes observation only',passed=True)]
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,ROOT/'GAS-RESIDUAL-CHECK.md',ROOT/'replay_saved_response.py']
    selections,rows={},[]
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for window in [20,40]:
            name=f'{model}-m{window}'
            parent_folder=PARENT/'results'/f'feedback-{name}'
            source_path=parent_folder/'continuation-source.npz'
            response_path=parent_folder/'continuation-response.npz'
            source,saved=map(read_npz,[source_path,response_path])
            parent_status=local_packet(parent_folder)
            inputs.extend([source_path,response_path,parent_folder/'status.json'])
            photons=[np.zeros((96,12))]
            residuals=[np.zeros(12)]
            def observe(index,photon,ratios):
                assert index==len(photons)
                photons.append(photon.copy())
                residuals.append(ratios.copy())
            response,errors=solve_response_trace(model,source,2048,ladder,emission,background,observe)
            for key,value in saved.items():
                if key=='integration_steps':
                    assert int(value)==2048
                elif key=='photon_final':
                    assert np.array_equal(value,response['photon'][-1])
                else:
                    assert np.array_equal(value,response[key]),(name,key)
            assert errors==parent_status['variants']['continuation']['response_errors'],name
            photons=np.array(photons)
            residuals=np.array(residuals)
            assert np.max(residuals)==errors['gas']
            np.savez_compressed(folder/(name+'-replay.npz'),**response,loop_photon=photons,
                raw_gas_residual=residuals,integration_steps=2048)
            checks.append(dict(name='Bitwise saved response and exact raw diagnostics:'+name,passed=True))
            maximum=residuals.max(axis=0)
            worst=residuals.argmax(axis=0)
            global_column=int(np.argmax(maximum))
            columns=np.array(sorted(set([0,1,2,global_column])),dtype=int)
            steps=sorted(set(max(1,int(index)) for index in [*worst[:3],worst[global_column]]))
            selections[name]=dict(raw_maximum_by_column=maximum.tolist(),worst_step_by_column=worst.tolist(),
                columns=columns.tolist(),steps=steps,raw_errors=errors,source_path=str(source_path),response_path=str(response_path))
            forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
            step=(source['coordinate'][-1]-source['coordinate'][0])/2048
            peak_gas=np.maximum(abs(response['gas'][:,columns]).max(axis=0),1e-300)
            peak_photon=np.maximum(photon_norm(photons[:,:,columns],basis.mass).max(axis=0),1e-300)
            for index in steps:
                position=float(source['coordinate'][0]+(source['coordinate'][-1]-source['coordinate'][0])*index/2048)
                local=background.at(position)
                theta=local['thermal_parameter']
                stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
                pieces=forcing(position)
                data=dict(mass=basis.mass,stiffness=stiffness,temperature=basis.temperature,
                    step=step,index=index,rate=local['coefficient']/theta,heat=background.chi,
                    external=np.column_stack([pieces.sum(axis=0),*pieces])[:,columns],
                    previous_photon=photons[index-1][:,columns],older_photon=photons[max(0,index-2)][:,columns],
                    previous_gas=response['gas'][index-1,columns],older_gas=response['gas'][max(0,index-2),columns],
                    old_photon=photons[index][:,columns],old_gas=response['gas'][index,columns],columns=columns)
                label=f'{name}-step{index:04d}'
                np.savez_compressed(folder/(label+'-inputs.npz'),**data)
                old_double=gas_residual_double(data,data['old_photon'],data['old_gas'])
                old_precise=gas_residual_precise(data,data['old_photon'],data['old_gas'],50)
                lower=solve_precise(data,50)
                higher=solve_precise(data,70)
                write_json(folder/(label+'-digits50.json'),lower)
                write_json(folder/(label+'-digits70.json'),higher)
                photon_agreement,gas_agreement=precision_difference(lower,higher)
                values=np.array(higher['solution'],dtype=float)
                gas_change=abs(values[96]-data['old_gas'])
                photon_change=photon_norm(values[:96]-data['old_photon'],basis.mass)
                cast=gas_residual_double(data,values[:96],values[96])
                for digits,result in [(50,lower),(70,higher)]:
                    for channel in ['photon','gas']:
                        checks.append(check(f'{label}:digits{digits}:{channel}',max(result[channel+'_relative']),1e-35))
                checks.extend([check(label+':50to70 photon',max(photon_agreement),1e-25),
                    check(label+':50to70 gas',max(gas_agreement),1e-25)])
                for column,value in zip(columns,cast):
                    checks.append(check(f'Response:precision-cast:{label}:column{column}:gas',float(value),1e-7))
                row=dict(case=name,step=index,columns=columns.tolist(),input_path=str(folder/(label+'-inputs.npz')),
                    traced_raw_gas_relative=residuals[index,columns].tolist(),reevaluated_double_gas_relative=old_double.tolist(),
                    existing_state_50digit_gas_relative=old_precise,high_precision_gas_relative=higher['gas_relative'],
                    high_precision_photon_relative=higher['photon_relative'],photon50to70=photon_agreement,gas50to70=gas_agreement,
                    cast_raw_gas_relative=cast.tolist(),gas_change_over_old_local=(gas_change/np.maximum(abs(data['old_gas']),1e-300)).tolist(),
                    gas_change_over_saved_peak=(gas_change/peak_gas).tolist(),photon_change_over_saved_peak=(photon_change/peak_photon).tolist(),
                    old_endpoint_near_zero=(abs(data['old_gas'])<1e-6*peak_gas).tolist())
                rows.append(row)
                write_json(folder/'progress.json',dict(state='running',case=name,last_witness=label,completed=len(rows),seconds=time.monotonic()-started))
                print(json.dumps(dict(witness=label,raw=float(max(residuals[index,columns])),old50=max(old_precise),
                    solved70=max(higher['gas_relative']),state_peak=float(max(gas_change/peak_gas)),cast=float(max(cast)))),flush=True)
            deadline=os.environ.get('MTS_DEADLINE_UTC')
            if deadline and datetime.now(timezone.utc)>=datetime.fromisoformat(deadline):
                raise SystemExit(75)
    assert selections['cold-m20']['raw_errors']['gas']==1.1577453548534613e-7
    checks.append(dict(name='Original flagged Stage139 residual reproduced exactly',passed=True))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    assert all(row['passed'] for row in checks if not row['name'].startswith('Response:'))
    finish(folder,dict(checks=checks,rows=rows,selections=selections,response_steps=2048,
        fixed_frequency_nodes=5265,physical_basis_size=96,coupled_solve_size=97,precision_digits=[50,70],
        previous_states_and_coefficients_are_binary64=True,full_high_precision_history=False,
        original_failed_checks_unchanged=True,inner_evolution_rerun=False,
        mpmath_version=mp.__version__,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(witnesses=len(rows),checks=len(checks),failed=[row['name'] for row in checks if not row['passed']],
        max_gas_state_change_over_peak=max(max(row['gas_change_over_saved_peak']) for row in rows))),flush=True)


if __name__=='__main__':
    main()
