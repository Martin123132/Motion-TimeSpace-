from adjacent_source_common import *


def integrate(model,count,initial,source_at,ladder,background,emission,lower,upper,label):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    begin,end=lower*background.end,upper*background.end
    step=(end-begin)/count
    state=np.vstack([initial['energy'],initial['photon'][coordinates.others]])
    previous=state.copy()
    gas,work,created=[initial[key].copy() for key in ['gas','work','integrated_number_source']]
    old_gas,old_work,old_created=gas.copy(),work.copy(),created.copy()
    histories=[state.copy()]
    gas_history,work_history,number_history=[gas.copy()],[work.copy()],[created.copy()]
    maxima={key:0. for key in ['source_rewrite','photon_equation','gas_equation','spectral_energy_roundoff']}
    for index in range(1,count+1):
        coordinate=begin+index*step
        local=background.at(coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        assert ladder.temperatures[0]*(1-1e-12)<=theta<=ladder.temperatures[-1]*(1+1e-12)
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        original=source_at(index/count)
        force,spectral_source,gas_source,rewrite=coordinates.source(original)
        maxima['source_rewrite']=max(maxima['source_rewrite'],rewrite['relative_change'])
        if index==1:
            alpha=1/step
            history=state/step
            gas_previous,work_previous,number_previous=gas/step,work/step,created/step
        else:
            alpha=1.5/step
            history=(2*state-.5*previous)/step
            gas_previous=(2*gas-.5*old_gas)/step
            work_previous=(2*work-.5*old_work)/step
            number_previous=(2*created-.5*old_created)/step
        projected=coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        gas_free=(history[0]+heat*gas_previous)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix=alpha*coordinates.mass-rate*projected
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_previous+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_previous=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)
        residual=basis.mass@(alpha*photon-photon_previous)-rate*physical-rate*original[1:-1]
        normalization=np.maximum(np.linalg.norm(basis.mass@photon_previous+rate*original[1:-1],axis=0),1e-300)
        maxima['photon_equation']=max(maxima['photon_equation'],float(np.max(np.linalg.norm(residual,axis=0)/normalization)))
        gas_residual=heat*((alpha+1)*new_gas-gas_previous)+rate*basis.temperature@physical-rate*original[-1]
        maxima['gas_equation']=max(maxima['gas_equation'],float(np.max(abs(gas_residual))))
        spectral=basis.energy@photon
        allowance=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(photon),1e-300)
        maxima['spectral_energy_roundoff']=max(maxima['spectral_energy_roundoff'],float(np.max(abs(spectral-updated[0])/allowance)))
        new_created=(number_previous+rate*basis.chemical@(physical+spectral_source))/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        histories.append(state.copy())
        gas_history.append(gas.copy())
        work_history.append(work.copy())
        number_history.append(created.copy())
    histories=np.array(histories)
    photons=np.einsum('ij,njk->nik',coordinates.transform,histories)
    gases,works,numbers=map(np.asarray,[gas_history,work_history,number_history])
    energy=histories[:,0]
    balance=energy+background.chi*gases+works
    scale=np.maximum(np.max(abs(energy)+abs(background.chi*gases)+abs(works),axis=0),1e-300)
    budget=float(np.max(abs(balance-balance[0])/scale))
    number_moment=np.einsum('i,nij->nj',basis.number,photons)
    number_scale=np.maximum(np.max(abs(number_moment)+abs(numbers),axis=0),1e-300)
    number_error=float(np.max(abs((number_moment-numbers)-(number_moment[0]-numbers[0]))/number_scale))
    checks=[]
    for name,value,limit in [('Source rewrite',maxima['source_rewrite'],1e-10),
                             ('Original photon equations',maxima['photon_equation'],1e-7),
                             ('Original gas equation',maxima['gas_equation'],1e-8),
                             ('Spectral energy roundoff',maxima['spectral_energy_roundoff'],1.),
                             ('Carried energy plus expansion work',budget,1e-7),
                             ('Carried photon number bookkeeping',number_error,1e-7)]:
        test(checks,name+':'+label,value,limit)
    result=dict(coordinate=np.linspace(begin,end,count+1),photon=photons,energy=energy,gas=gases,
                work=works,number=number_moment,integrated_number_source=numbers)
    for key in ['photon','energy','gas','work','number','integrated_number_source']:
        value=result[key]
        assert np.array_equal(value[...,6:8],np.zeros_like(value[...,6:8]))
        errors=[value[...,2:4]-value[...,:2]-value[...,4:6],
                value[...,10:12]-value[...,8:10]-value[...,2:4]]
        for identity,error in zip(['quadratic=secant+defect','old+new=old+quadratic'],errors):
            denominator=max(float(np.max(abs(value[...,2:4]))),1e-300)
            test(checks,'Independent superposition:'+label+':'+key+':'+identity,
                 np.max(abs(error))/denominator,1e-8)
    checks.append(dict(name='Zero extra source gives exactly zero addition:'+label,passed=True))
    return result,checks,dict(budget=budget,number_error=number_error,initial_balance=balance[0].tolist(),**maxima)


def terminal(result):
    return {key:result[key][-1].copy() for key in ['photon','energy','gas','work','integrated_number_source']}


def main():
    modest()
    folder=ROOT/'results/adjacent-response'
    folder.mkdir(parents=True,exist_ok=False)
    source_path=ROOT/'results/adjacent-sources/source.npz'
    source=read_npz(source_path)
    source_report=verify_packet(source_path.parent)
    readiness=verify_packet(ROOT/'results/energy-coordinate-readiness')
    assert readiness['all_checks_passed'] and readiness['energy_coordinate_evolution_allowed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,rows,inputs,comparisons=[],{},[source_path,source_path.parent/'status.json',ROOT/'results/energy-coordinate-readiness/status.json',*ladder.inputs],{}
    groups=['secant','quadratic','curvature_increment','zero_extra_source','old_window_replay','old_plus_new_direct']
    for model,selection in [('heavy',slice(0,2)),('cold',slice(2,4))]:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        old_path=BRANCH/'downstream-window-transfer-20261012/results/window-transfer'/f'{model}-main-1024.npz'
        old=read_npz(old_path)
        inputs.extend([old_path,*emission.inputs,background.parent.source,background.native_constants])
        initial={key:np.zeros((96,12)) if key=='photon' else np.zeros(12)
                 for key in ['photon','energy','gas','work','integrated_number_source']}
        for key in initial:
            initial[key][...,8:10]=old[key][0,...,:2]
            initial[key][...,10:12]=old[key][0,...,:2]
        start,end,curvature=[source[key][:,selection] for key in ['start','end','curvature']]
        def forcing(fraction):
            secant=(1-fraction)*start+fraction*end
            defect=4*fraction*(1-fraction)*curvature
            quadratic=secant+defect
            zero=np.zeros_like(secant)
            return np.column_stack([secant,quadratic,defect,zero,zero,quadratic])
        def no_forcing(fraction):
            return np.zeros((98,12))
        solutions={}
        for count in [256,512,1024]:
            active,active_checks,active_row=integrate(model,count,initial,forcing,ladder,background,emission,.5,.75,f'{model}-active{count}')
            final,transfer_checks,transfer_row=integrate(model,count,terminal(active),no_forcing,ladder,background,emission,.75,1.,f'{model}-transfer{count}')
            checks.extend(active_checks+transfer_checks)
            rows[f'{model}-{count}']=dict(active=active_row,transfer=transfer_row)
            solutions[count]=(active,final)
            np.savez_compressed(folder/f'{model}-active{count}.npz',**active)
            np.savez_compressed(folder/f'{model}-transfer{count}.npz',**final)
            print(json.dumps(dict(model=model,steps=count,finished=True)),flush=True)
        def photon_norm(value):
            return np.sqrt(np.maximum(np.einsum('ik,ij,jk->k',value,basis.mass,value),0.))
        comparisons[model]={}
        for phase_index,phase in enumerate(['active','transfer']):
            fine,coarse=solutions[1024][phase_index],solutions[512][phase_index]
            photon=photon_norm(fine['photon'][-1]-coarse['photon'][-1])/np.maximum(photon_norm(fine['photon'][-1]),1e-300)
            gas=abs(fine['gas'][-1]-coarse['gas'][-1])/np.maximum(np.max(abs(fine['gas']),axis=0),1e-300)
            comparisons[model][phase]=dict(photon_endpoint=photon.tolist(),gas_over_peak=gas.tolist())
            test(checks,'Time refinement photon:'+model+':'+phase,np.max(photon),.01)
            test(checks,'Time refinement gas:'+model+':'+phase,np.max(gas),.01)
        final=solutions[1024][1]
        new=final['photon'][-1,:,2:4]
        defect=final['photon'][-1,:,4:6]
        comparisons[model]['source_interpolation']=dict(photon=(
            photon_norm(defect)/np.maximum(photon_norm(new),1e-300)).tolist(),
            gas_over_quadratic_peak=(abs(final['gas'][-1,4:6])/
                np.maximum(np.max(abs(final['gas'][:,2:4]),axis=0),1e-300)).tolist())
        comparisons[model]['old_window_replay']=dict(photon=(
            photon_norm(final['photon'][-1,:,8:10]-old['photon'][-1,:,:2])/
            photon_norm(old['photon'][-1,:,:2])).tolist(),
            gas_over_old_endpoint=(abs(final['gas'][-1,8:10]-old['gas'][-1,:2])/
                abs(old['gas'][-1,:2])).tolist())
    finish(folder,dict(checks=checks,rows=rows,comparisons=comparisons,column_groups=groups,
                       steps=[256,512,1024],source_interval=[.5,.75],transfer_interval=[.75,1.],
                       old_source_not_reset=True,zero_source_control_is_not_zero_baseline=True,
                       new_window_low_frequency_feedback_recomputed=False,
                       source_grid_error_bounded=False,unchanged_basis_modes=96),
           __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
                          comparisons=comparisons)),flush=True)


if __name__=='__main__':
    main()
