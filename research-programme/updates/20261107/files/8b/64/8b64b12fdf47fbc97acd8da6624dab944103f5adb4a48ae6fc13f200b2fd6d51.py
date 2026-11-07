from history_source_common import *
from inspect_coupled_response import response,NonlocalEmission,infrared_ladder


def coupled_step(basis,stiffness,rate,heat,source,gas_source,alpha,vector,scalar,work_history):
    forcing=basis.mass@vector+rate*source
    solved=linalg.solve(alpha*basis.mass-rate*stiffness,
        np.column_stack([forcing,-rate*stiffness@basis.temperature]),assume_a='pos')
    free,susceptibility=solved[:,:-1],solved[:,-1]
    paired=rate*(basis.temperature@source+gas_source)
    gas=(heat*scalar+basis.energy@vector+paired-alpha*(basis.energy@free))/(heat*(alpha+1)+alpha*(basis.energy@susceptibility))
    photon=free+susceptibility[:,None]*gas
    work=(work_history+heat*gas)/alpha
    photon_residual=alpha*basis.mass@photon-basis.mass@vector-rate*stiffness@(photon-basis.temperature[:,None]*gas)-rate*source
    gas_residual=heat*((alpha+1)*gas-scalar)+rate*basis.temperature@stiffness@(photon-basis.temperature[:,None]*gas)-rate*gas_source
    derivative_balance=basis.energy@(alpha*photon-vector)+heat*(alpha*gas-scalar)+heat*gas-paired
    reference=max(float(np.linalg.norm(forcing)),1e-300)
    return photon,gas,work,dict(photon_equation_relative=float(np.linalg.norm(photon_residual)/reference),
        gas_equation_absolute=float(np.max(abs(gas_residual))),energy_derivative_absolute=float(np.max(abs(derivative_balance))))


def integrate_response(model,count,anchor,ladder):
    background=thermal_wave.thermal.ThermalBackground(model)
    emission=NonlocalEmission(ladder.basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    basis=ladder.basis
    start,end=FRACTION*background.end,.5*background.end
    step=(end-start)/count
    selection=slice(0,2) if model=='heavy' else slice(2,4)
    labels=['secant_actual','secant_fixed_profiles','frozen_midpoint']
    photon,old_photon=np.zeros((96,6)),np.zeros((96,6))
    gas,old_gas,work,old_work=[np.zeros(6) for unused in range(4)]
    created,old_created=np.zeros(6),np.zeros(6)
    photons,gases,works,errors=[photon.copy()],[gas.copy()],[work.copy()],[]
    numbers=[created.copy()]
    maximum_pair=0.
    for index in range(1,count+1):
        coordinate=start+index*step
        fraction=index/count
        local=background.at(coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        end_source=anchor['midpoint'][:,selection]
        source=np.column_stack([(1-fraction)*anchor[key][:,selection]+fraction*end_source
            for key in ['quarter','temperature_only']]+[end_source])
        if index==1:
            alpha,vector,scalar,work_history=1/step,photon/step,gas/step,work/step
            number_history=created/step
        else:
            alpha=1.5/step
            vector=(2*photon-.5*old_photon)/step
            scalar=(2*gas-.5*old_gas)/step
            work_history=(2*work-.5*old_work)/step
            number_history=(2*created-.5*old_created)/step
        updated,new_gas,new_work,metrics=coupled_step(basis,stiffness,rate,heat,source[1:-1],source[-1],alpha,vector,scalar,work_history)
        number_rate=rate*basis.chemical@(stiffness@(updated-basis.temperature[:,None]*new_gas)+source[1:-1])
        new_created=(number_history+number_rate)/alpha
        maximum_pair=max(maximum_pair,float(np.max(abs(rate*(basis.temperature@source[1:-1]+source[-1])))))
        old_photon,photon=photon,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        photons.append(photon.copy())
        gases.append(gas.copy())
        works.append(work.copy())
        numbers.append(created.copy())
        errors.append(metrics)
    photons,gases,works=np.asarray(photons),np.asarray(gases),np.asarray(works)
    energies=np.einsum('i,nij->nj',basis.energy,photons)
    balance=energies+background.chi*gases+works
    number_moment=np.einsum('i,nij->nj',basis.number,photons)
    numbers=np.asarray(numbers)
    number_scale=max(float(np.max(abs(number_moment))),1e-300)
    number_error=float(np.max(abs(number_moment-numbers))/number_scale)
    scale=np.maximum(np.max(abs(energies)+abs(background.chi*gases)+abs(works),axis=0),1e-300)
    checks=[dict(name=f'Variable-history original photon equations:{model}-{count}',value=max(row['photon_equation_relative'] for row in errors),
        passed=max(row['photon_equation_relative'] for row in errors)<1e-7),
        dict(name=f'Variable-history independent gas equation:{model}-{count}',value=max(row['gas_equation_absolute'] for row in errors),
        passed=max(row['gas_equation_absolute'] for row in errors)<1e-8),
        dict(name=f'First-order energy plus expansion work:{model}-{count}',value=float(np.max(abs(balance)/scale)),
        passed=bool(np.max(abs(balance)/scale)<1e-7)),
        dict(name=f'All96 modes and all three forcing alternatives finite:{model}-{count}',
        passed=bool(np.isfinite(photons).all() and np.isfinite(gases).all())),
        dict(name=f'Photon number follows original collision plus correction:{model}-{count}',value=number_error,passed=number_error<1e-7)]
    result=dict(coordinate=np.linspace(start,end,count+1),photon=photons,gas=gases,work=works,energy=energies,
        number=number_moment,integrated_number_source=numbers)
    return result,checks,[*emission.inputs,background.parent.source,background.native_constants],dict(model=model,steps=count,
        forcing_labels=labels,heat=background.chi,max_forcing_pair=maximum_pair,energy_work_relative=float(np.max(abs(balance)/scale)))


def main():
    modest()
    folder=ROOT/'results/history-response'
    folder.mkdir(parents=True,exist_ok=False)
    anchor_path=ROOT/'results/anchor-source/source.npz'
    anchor=dict(np.load(anchor_path))
    status=json.loads((anchor_path.parent/'status.json').read_text())
    assert status['all_checks_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    assert np.array_equal(ladder.basis.mass,anchor['mass'])
    bundle=EpochBundle()
    basis=ladder.basis
    assert np.allclose(basis.number,basis.mass@basis.chemical,rtol=1e-12,atol=1e-14)
    background=thermal_wave.thermal.ThermalBackground('heavy')
    local=background.at(bundle.epochs[1].coordinate)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    stiffness=ladder.at(local['thermal_parameter'],0)[:96,:96]-emission.at(local['thermal_parameter'],'dcbr')
    rate=local['coefficient']/local['thermal_parameter']
    duration=.01
    photon,gas,metrics=response(basis,stiffness,rate,background.chi,anchor['midpoint'][1:-1,:2],anchor['midpoint'][-1,:2],duration)
    actual,actual_gas,work,unused=coupled_step(basis,stiffness,rate,background.chi,anchor['midpoint'][1:-1,:2],anchor['midpoint'][-1,:2],
        1/duration,np.zeros((96,2)),np.zeros(2),np.zeros(2))
    error=float(np.max(abs(actual-photon))/max(np.max(abs(photon)),1e-300))
    gas_error=float(np.max(abs(actual_gas-gas))/max(np.max(abs(gas)),1e-300))
    checks=[dict(name='Time-step law replays original frozen photon/gas response',photon_relative=error,gas_relative=gas_error,
        passed=error<1e-10 and gas_error<1e-10)]
    rows,inputs,arrays=[],[anchor_path,anchor_path.parent/'status.json',*ladder.inputs,*emission.inputs,*bundle.inputs],[]
    report_values={}
    def norms(value):
        return np.sqrt(np.maximum(np.sum(value*(basis.mass@value),axis=0),0.))
    for model in ['heavy','cold']:
        solutions={}
        for count in [128,256,512]:
            solved,tests,dependencies,row=integrate_response(model,count,anchor,ladder)
            solutions[count]=solved
            np.savez(folder/f'{model}-{count}.npz',**solved)
            checks+=tests
            inputs+=dependencies
            rows.append(row)
        fine=solutions[512]
        comparisons=[]
        for coarse_count,fine_count in [(128,256),(256,512)]:
            first,second=solutions[coarse_count],solutions[fine_count]
            photon_change=norms(second['photon'][-1]-first['photon'][-1])/np.maximum(norms(second['photon'][-1]),1e-300)
            gas_change=abs(second['gas'][-1]-first['gas'][-1])/np.maximum(np.max(abs(second['gas']),axis=0),1e-300)
            comparisons.append(dict(coarse=coarse_count,fine=fine_count,photon_relative=photon_change.tolist(),gas_relative_to_peak=gas_change.tolist()))
            if fine_count==512:
                checks.append(dict(name='Secant-source time-step refinement within1percent:'+model,
                    photon=float(photon_change.max()),gas=float(gas_change.max()),passed=bool(max(photon_change.max(),gas_change.max())<.01)))
        actual,fixed,frozen=np.split(fine['photon'][-1],3,axis=1)
        scale=np.maximum(norms(actual),1e-300)
        report_values[model]=dict(step_comparisons=comparisons,
            frozen_midpoint_photon_error_relative_to_secant=(norms(actual-frozen)/scale).tolist(),
            profile_history_photon_change_relative_to_secant=(norms(actual-fixed)/scale).tolist(),
            final_actual_photon_norm=norms(actual).tolist(),
            final_gas=fine['gas'][-1].tolist(),final_photon_energy=fine['energy'][-1].tolist(),final_work=fine['work'][-1].tolist(),
            final_photon_number_moment=fine['number'][-1].tolist())
    finish(folder,dict(checks=checks,rows=rows,response_results=report_values,
        forcing_interpolation='Two-anchor secant in log-expansion;not a certified source history.',
        first_order_fixed_geometry_response=True,source_interpolation_error_bounded=False,
        quarter_source_precision_gate_closed=False,new_parent_history=False,full_parent_feedback_applied=False,
        correction_initial_condition='Zero at fraction.25;increment accumulated only to fraction.5,not a full-range solution.'),__file__,inputs)
    print(json.dumps(dict(response_results=report_values,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
