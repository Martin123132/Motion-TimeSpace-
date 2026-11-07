from window_transfer_common import *


def run(model,count,initial,ladder,background,emission,start_fraction=.5,end_fraction=1.,label='main'):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    start,end=start_fraction*background.end,end_fraction*background.end
    assert abs(float(initial['coordinate'][-1])-start)<1e-14
    step=(end-start)/count
    state=np.vstack([initial['energy'][-1],initial['photon'][-1,coordinates.others]])
    previous=state.copy()
    gas,work,created=[initial[key][-1].copy() for key in ['gas','work','integrated_number_source']]
    old_gas,old_work,old_created=gas.copy(),work.copy(),created.copy()
    saved_states=[state.copy()]
    saved_gas,saved_work,saved_numbers=[gas.copy()],[work.copy()],[created.copy()]
    initial_photon=coordinates.transform@state
    reconstruction=photon_norm(initial_photon-initial['photon'][-1],basis.mass)/np.maximum(photon_norm(initial['photon'][-1],basis.mass),1e-300)
    maxima={key:0. for key in ['original_photon_relative','original_gas_absolute','energy_roundoff_ratio','step_balance_absolute']}
    for index in range(1,count+1):
        coordinate=start+index*step
        local=background.at(coordinate)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        assert ladder.temperatures[0]*(1-1e-12)<=theta<=ladder.temperatures[-1]*(1+1e-12)
        assert emission.temperatures[0]*(1-1e-12)<=theta<=emission.temperatures[-1]*(1+1e-12)
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        if index==1:
            alpha=1/step
            history=state/step
            gas_history=gas/step
            work_history=work/step
            number_history=created/step
        else:
            alpha=1.5/step
            history=(2*state-.5*previous)/step
            gas_history=(2*gas-.5*old_gas)/step
            work_history=(2*work-.5*old_work)/step
            number_history=(2*created-.5*old_created)/step
        projected_stiffness=coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        gas_free=(history[0]+heat*gas_history)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix=alpha*coordinates.mass-rate*projected_stiffness
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_history+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_history=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)
        derivative=alpha*photon-photon_history
        residual=basis.mass@derivative-rate*physical
        normalization=np.maximum(np.linalg.norm(basis.mass@photon_history,axis=0),1e-300)
        gas_residual=heat*((alpha+1)*new_gas-gas_history)+rate*basis.temperature@physical
        maxima['original_photon_relative']=max(maxima['original_photon_relative'],float(np.max(np.linalg.norm(residual,axis=0)/normalization)))
        maxima['original_gas_absolute']=max(maxima['original_gas_absolute'],float(np.max(abs(gas_residual))))
        reconstructed=basis.energy@photon
        roundoff_bound=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(photon),1e-300)
        maxima['energy_roundoff_ratio']=max(maxima['energy_roundoff_ratio'],float(np.max(abs(reconstructed-updated[0])/roundoff_bound)))
        derivative_balance=alpha*updated[0]-history[0]+heat*(alpha*new_gas-gas_history)+heat*new_gas
        maxima['step_balance_absolute']=max(maxima['step_balance_absolute'],float(np.max(abs(derivative_balance))))
        number_rate=rate*basis.chemical@physical
        new_created=(number_history+number_rate)/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        saved_states.append(state.copy())
        saved_gas.append(gas.copy())
        saved_work.append(work.copy())
        saved_numbers.append(created.copy())
    states=np.asarray(saved_states)
    photons=np.einsum('ij,njk->nik',coordinates.transform,states)
    gases,works,numbers=np.asarray(saved_gas),np.asarray(saved_work),np.asarray(saved_numbers)
    energy=states[:,0,:]
    balance=energy+background.chi*gases+works
    scale=np.maximum(np.max(abs(energy)+abs(background.chi*gases)+abs(works),axis=0),1e-300)
    relative_balance=float(np.max(abs(balance)/scale))
    number_moment=np.einsum('i,nij->nj',basis.number,photons)
    number_scale=np.maximum(np.max(abs(number_moment)+abs(numbers),axis=0),1e-300)
    number_error=float(np.max(abs(number_moment-numbers)/number_scale))
    identity_errors={}
    component_offsets=[10,12,14]
    residual=photons[:,:,2:4]-sum(photons[:,:,offset:offset+2] for offset in component_offsets)
    denominator=max(float(np.max(sum(photon_norm(photons[:,:,offset:offset+2],basis.mass) for offset in component_offsets))),1e-300)
    identity_errors['photon']=float(np.max(photon_norm(residual,basis.mass))/denominator)
    for key,value in [('gas',gases),('energy',energy),('work',works),('number',number_moment)]:
        parts=[value[:,offset:offset+2] for offset in component_offsets]
        identity_errors[key]=float(np.max(abs(value[:,2:4]-sum(parts)))/max(float(np.max(sum(abs(part) for part in parts))),1e-300))
    suffix=f'{model}:{label}:{count}'
    checks=[
        dict(name='Invertible96-mode energy coordinate mass identity:'+suffix,value=coordinates.mass_rewrite_error,passed=coordinates.mass_rewrite_error<1e-12),
        dict(name='Inherited independent energy reconstructs all terminal photon modes:'+suffix,value=float(reconstruction.max()),passed=bool(reconstruction.max()<1e-12)),
        dict(name='Original homogeneous photon equations for every column:'+suffix,value=maxima['original_photon_relative'],passed=maxima['original_photon_relative']<1e-7),
        dict(name='Original independent gas equation:'+suffix,value=maxima['original_gas_absolute'],passed=maxima['original_gas_absolute']<1e-8),
        dict(name='Energy plus inherited and downstream expansion work:'+suffix,value=relative_balance,passed=relative_balance<1e-7),
        dict(name='Spectral energy within explicit floating-point allowance:'+suffix,value=maxima['energy_roundoff_ratio'],passed=maxima['energy_roundoff_ratio']<1),
        dict(name='Photon-number emission bookkeeping for every column:'+suffix,value=number_error,passed=number_error<1e-7),
        dict(name='Direct54 total equals separately transferred components:'+suffix,errors=identity_errors,passed=max(identity_errors.values())<1e-8)]
    result=dict(coordinate=np.linspace(start,end,count+1),photon=photons,energy=energy,gas=gases,work=works,
        number=number_moment,integrated_number_source=numbers,energy_from_spectrum=np.einsum('i,nij->nj',basis.energy,photons))
    row=dict(model=model,label=label,steps=count,start_fraction=start_fraction,end_fraction=end_fraction,heat=background.chi,
        energy_work_relative=relative_balance,number_relative=number_error,identity_errors=identity_errors,**maxima)
    return result,checks,row


def difference_metrics(reference,other,mass):
    norms=photon_norm(reference['photon'],mass)
    peak=norms.max(axis=0)
    photon=photon_norm(reference['photon'][-1]-other['photon'][-1],mass)
    gas=abs(reference['gas'][-1]-other['gas'][-1])
    gas_peak=abs(reference['gas']).max(axis=0)
    assert np.all(peak>0) and np.all(gas_peak>0)
    return dict(photon_relative_to_peak=(photon/peak).tolist(),gas_relative_to_peak=(gas/gas_peak).tolist(),
        photon_relative_to_endpoint=[float(value/denominator) if denominator>0 else None for value,denominator in zip(photon,norms[-1])],
        gas_relative_to_endpoint=[float(value/denominator) if denominator>0 else None for value,denominator in zip(gas,abs(reference['gas'][-1]))])


def main():
    modest()
    folder=ROOT/'results/window-transfer'
    folder.mkdir(parents=True,exist_ok=False)
    proof_path=ROOT/'results/transfer-preflight/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    for path,expected in proof['input_hashes'].items():
        assert digest(path)==expected,path
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    endpoint=Spectra(1.)
    checks,rows,inputs,summary=[],[],[proof_path,ROOT/'DERIVATION.md',*ladder.inputs,*endpoint.inputs],{}
    assert np.array_equal(endpoint.basis.mass,basis.mass)
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        initial_by_count={}
        for initial_count in [128,256,512]:
            initial,path=load_terminal(model,initial_count)
            inputs.append(path)
            initial_by_count[initial_count]=initial
        initial=initial_by_count[512]
        solutions={}
        def save_case(label,steps,start=.5,end=1.,state=None):
            solved,tests,row=run(model,steps,initial if state is None else state,ladder,background,emission,start,end,label)
            np.savez(folder/f'{model}-{label}-{steps}.npz',**solved)
            write_json(folder/f'{model}-{label}-{steps}-diagnostics.json',dict(checks=tests,metrics=row))
            checks.extend(tests)
            rows.append(row)
            return solved
        for steps in [256,512,1024]:
            solutions[steps]=save_case('main',steps)
        fine=solutions[1024]
        refinement=difference_metrics(fine,solutions[512],basis.mass)
        previous_refinement=difference_metrics(solutions[512],solutions[256],basis.mass)
        value=max(*refinement['photon_relative_to_peak'],*refinement['gas_relative_to_peak'])
        checks.append(dict(name='TRANSFER_NUMERICS: downstream timestep refinement within1percent:'+model,value=value,passed=value<.01))
        inherited_solutions={}
        for initial_count in [128,256]:
            inherited_solutions[initial_count]=save_case('from-parent'+str(initial_count),1024,state=initial_by_count[initial_count])
        initial_refinement=difference_metrics(fine,inherited_solutions[256],basis.mass)
        earlier_initial=difference_metrics(inherited_solutions[256],inherited_solutions[128],basis.mass)
        value=max(*initial_refinement['photon_relative_to_peak'],*initial_refinement['gas_relative_to_peak'])
        checks.append(dict(name='TRANSFER_NUMERICS: inherited-terminal refinement within1percent:'+model,value=value,passed=value<.01))
        first=save_case('split-first',512,.5,.75)
        second=save_case('split-second',512,.75,1.,first)
        split=difference_metrics(fine,second,basis.mass)
        value=max(*split['photon_relative_to_peak'],*split['gas_relative_to_peak'])
        checks.append(dict(name='TRANSFER_NUMERICS: matched-step split restart within1percent:'+model,value=value,passed=value<.01))
        central_norms=photon_norm(fine['photon'][:,:,:2],basis.mass)
        central_peak=central_norms.max(axis=0)
        central_endpoint=central_norms[-1]
        gas_peak=abs(fine['gas'][:,:2]).max(axis=0)
        gas_endpoint=abs(fine['gas'][-1,:2])
        assert np.all(central_endpoint>0) and np.all(gas_peak>0)
        budgets={}
        for level,offsets in [('43',[4,6,8]),('54',[10,12,14])]:
            photons=[fine['photon'][:,:,offset:offset+2] for offset in offsets]
            gases=np.asarray([fine['gas'][:,offset:offset+2] for offset in offsets])
            norms=np.asarray([photon_norm(value,basis.mass) for value in photons])
            photon_sum=norms.sum(axis=0)
            gas_sum=abs(gases).sum(axis=0)
            photon_coherent=photon_norm(sum(photons),basis.mass)
            gas_coherent=abs(gases.sum(axis=0))
            triangle=float(max(np.max((photon_coherent-photon_sum)/central_peak),np.max((gas_coherent-gas_sum)/gas_peak)))
            checks.append(dict(name=f'Component-sum triangle inequality:{model}:{level}',value=triangle,passed=triangle<1e-12))
            budgets[level]=dict(endpoint_photon_component_sum=(photon_sum[-1]/central_endpoint).tolist(),
                endpoint_gas_component_sum_to_peak=(gas_sum[-1]/gas_peak).tolist(),
                endpoint_gas_component_sum_to_endpoint=[float(value/denominator) if denominator>0 else None for value,denominator in zip(gas_sum[-1],gas_endpoint)],
                endpoint_photon_coherent=(photon_coherent[-1]/central_endpoint).tolist(),
                history_photon_component_sum_to_peak=(photon_sum.max(axis=0)/central_peak).tolist(),
                history_gas_component_sum_to_peak=(gas_sum.max(axis=0)/gas_peak).tolist(),
                photon_sum_of_component_peaks=(norms.max(axis=1).sum(axis=0)/central_peak).tolist(),
                gas_sum_of_component_peaks=(abs(gases).max(axis=1).sum(axis=0)/gas_peak).tolist(),
                endpoint_photon_components=(norms[:,-1]/central_endpoint).tolist(),
                endpoint_gas_components_to_peak=(abs(gases[:,-1])/gas_peak).tolist())
        contractions={}
        for key in ['endpoint_photon_component_sum','endpoint_gas_component_sum_to_peak','history_photon_component_sum_to_peak','history_gas_component_sum_to_peak']:
            contractions[key]=(np.asarray(budgets['54'][key])/np.asarray(budgets['43'][key])).tolist()
        for join in range(2):
            for key in ['endpoint_photon_component_sum','endpoint_gas_component_sum_to_peak']:
                value=budgets['54'][key][join]
                contraction=contractions[key][join]
                checks.extend([dict(name=f'TRANSFER_DIAGNOSTIC:54 budget within1percent:{model}:join{join+1}:{key}',value=value,passed=value<=.01),
                    dict(name=f'TRANSFER_DIAGNOSTIC:54/43 contracts:{model}:join{join+1}:{key}',value=contraction,passed=contraction<1)])
        parent_photon=endpoint.original[model]
        parent_norm=float(photon_norm(parent_photon[:,None],basis.mass)[0])
        parent_gas=float(endpoint.gas[0 if model=='heavy' else 1])
        initial_norm=photon_norm(initial['photon'][-1],basis.mass)
        final_norm=photon_norm(fine['photon'][-1],basis.mass)
        parent_fit_path=folder/f'{model}-final-window-contribution.npz'
        np.savez(parent_fit_path,photon_central=fine['photon'][-1,:,:2],photon_total54=fine['photon'][-1,:,2:4],
            photon_candidate5=fine['photon'][-1,:,:2]+fine['photon'][-1,:,2:4],
            gas_central=fine['gas'][-1,:2],gas_total54=fine['gas'][-1,2:4],
            parent_photon=parent_photon,parent_gas=parent_gas,mass=basis.mass,temperature=basis.temperature,chemical=basis.chemical)
        summary[model]=dict(downstream_refinement=refinement,previous_downstream_refinement=previous_refinement,
            initial_refinement=initial_refinement,previous_initial_refinement=earlier_initial,split_restart=split,
            budgets=budgets,contractions=contractions,photon_transfer_final_over_initial=(final_norm/initial_norm).tolist(),
            gas_transfer_final_over_initial=[float(new/old) if old!=0 else None for new,old in zip(fine['gas'][-1],initial['gas'][-1])],
            central_final_photon_norm=central_endpoint.tolist(),central_downstream_photon_peak=central_peak.tolist(),
            central_final_gas=fine['gas'][-1,:2].tolist(),central_downstream_gas_peak=gas_peak.tolist(),
            parent_final_photon_norm=parent_norm,parent_final_gas=parent_gas,
            central_relative_to_final_parent_photon=(central_endpoint/parent_norm).tolist(),
            central_relative_to_final_parent_gas=(abs(fine['gas'][-1,:2])/abs(parent_gas)).tolist() if parent_gas!=0 else None,
            final_energy=fine['energy'][-1].tolist(),final_work=fine['work'][-1].tolist(),final_number=fine['number'][-1].tolist())
        print(json.dumps(dict(model=model,completed=True,central_relative_to_parent=summary[model]['central_relative_to_final_parent_photon'],
            budgets=budgets,failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    structural=[row for row in checks if not row['name'].startswith('TRANSFER_DIAGNOSTIC:')]
    structural_passed=all(bool(row['passed']) for row in structural)
    finish(folder,dict(checks=checks,rows=rows,transfer_results=summary,numerical_integrity_all_passed=structural_passed,
        column_order=proof['column_order'],window_start=.25,window_end=.5,transfer_end=1.,full_spectral_modes=96,
        outside_window_source_assumed_physically_zero=False,window_contribution_only=True,
        finite_source_recomputed=False,leading_history_unchanged=True,new_empirical_fit=False,new_parent_history=False,
        operator_extrapolation=False,work_and_number_initial_offsets_retained=True,stage106_failures_retained=True),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    if not structural_passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
