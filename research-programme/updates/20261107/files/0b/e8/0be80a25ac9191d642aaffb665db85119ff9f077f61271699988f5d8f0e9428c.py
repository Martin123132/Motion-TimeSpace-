from matched_feedback_common import *


def solve_response(model,source,steps,ladder,emission,background):
    basis=ladder.basis
    coordinates=EnergyCoordinates(basis)
    forcing=interpolate.interp1d(source['coordinate'],source['source'],axis=0,bounds_error=True)
    start,end=source['coordinate'][[0,-1]]
    step=(end-start)/steps
    state,previous=np.zeros((96,12)),np.zeros((96,12))
    gas,old_gas,work,old_work,created,old_created=[np.zeros(12) for unused in range(6)]
    states,gases,works,numbers=[state.copy()],[gas.copy()],[work.copy()],[created.copy()]
    errors={key:0. for key in ['photon','gas','energy_spectrum','energy_step']}
    for index in range(1,steps+1):
        position=float(start+(end-start)*index/steps)
        local=background.at(position)
        theta,rate,heat=local['thermal_parameter'],local['coefficient']/local['thermal_parameter'],background.chi
        stiffness=ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr')
        pieces=forcing(position)
        external=np.column_stack([pieces.sum(axis=0),*pieces])
        force=coordinates.tests@external
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
        matrix=alpha*coordinates.mass-rate*coordinates.tests@stiffness@coordinates.transform
        coupling=-rate*coordinates.tests@stiffness@basis.temperature
        gas_free=(history[0]+heat*gas_history)/(heat*(alpha+1))
        energy_coefficient=alpha/(heat*(alpha+1))
        matrix[:,0]+=coupling*energy_coefficient
        right=coordinates.mass@history+rate*force+coupling[:,None]*gas_free
        updated=linalg.solve(matrix,right)
        new_gas=gas_free-energy_coefficient*updated[0]
        new_work=(work_history+heat*new_gas)/alpha
        photon=coordinates.transform@updated
        photon_history=coordinates.transform@history
        physical=stiffness@(photon-basis.temperature[:,None]*new_gas)+external
        derivative=alpha*photon-photon_history
        residual=basis.mass@derivative-rate*physical
        scale=np.maximum(np.linalg.norm(basis.mass@photon_history,axis=0)+np.linalg.norm(rate*physical,axis=0)+np.linalg.norm(alpha*basis.mass@photon,axis=0),1e-300)
        errors['photon']=max(errors['photon'],float(np.max(np.linalg.norm(residual,axis=0)/scale)))
        gas_residual=heat*((alpha+1)*new_gas-gas_history)+rate*basis.temperature@physical
        gas_scale=np.maximum(abs(heat*(alpha+1)*new_gas)+abs(heat*gas_history)+abs(rate)*abs(basis.temperature)@abs(physical),1e-300)
        errors['gas']=max(errors['gas'],float(np.max(abs(gas_residual)/gas_scale)))
        spectrum_energy=basis.energy@photon
        allowance=256*np.finfo(float).eps*np.maximum(abs(basis.energy)@abs(photon),1e-300)
        errors['energy_spectrum']=max(errors['energy_spectrum'],float(np.max(abs(spectrum_energy-updated[0])/allowance)))
        energy_error=alpha*updated[0]-history[0]+heat*((alpha+1)*new_gas-gas_history)
        energy_scale=np.maximum(abs(alpha*updated[0])+abs(history[0])+heat*(abs((alpha+1)*new_gas)+abs(gas_history)),1e-300)
        errors['energy_step']=max(errors['energy_step'],float(np.max(abs(energy_error)/energy_scale)))
        number_rate=rate*basis.chemical@physical
        new_created=(number_history+number_rate)/alpha
        previous,state=state,updated
        old_gas,gas=gas,new_gas
        old_work,work=work,new_work
        old_created,created=created,new_created
        states.append(state.copy())
        gases.append(gas.copy())
        works.append(work.copy())
        numbers.append(created.copy())
    states=np.array(states)
    photons=np.einsum('ij,njk->nik',coordinates.transform,states)
    gases,works,numbers=np.array(gases),np.array(works),np.array(numbers)
    energy=states[:,0]
    number_moment=np.einsum('i,nik->nk',basis.number,photons)
    energy_scale=np.maximum(np.max(abs(energy)+background.chi*abs(gases)+abs(works),axis=0),1e-300)
    number_scale=np.maximum(np.max(abs(number_moment)+abs(numbers),axis=0),1e-300)
    errors['energy_work']=float(np.max(abs(energy+background.chi*gases+works)/energy_scale))
    errors['number']=float(np.max(abs(number_moment-numbers)/number_scale))
    components=[photons[:,:,offset:offset+3] for offset in [3,6,9]]
    component_norm=sum(photon_norm(component,basis.mass) for component in components)
    errors['linearity']=float(np.max(photon_norm(photons[:,:,:3]-sum(components),basis.mass)/np.maximum(component_norm.max(axis=0),1e-300)))
    return dict(coordinate=np.linspace(start,end,steps+1),photon=photons,gas=gases,energy=energy,work=works,number=number_moment,integrated_number=numbers),errors


def readout(basis,model,source,solution,variant,upper):
    reader=ShapeReadout(basis,canonical=True)
    prediction,profiles,gas,dependencies=read_prediction(model,variant)
    replacement=CompactCorrection(basis,prediction['frequency'],upper)
    replacement.register('readout',basis.nodes)
    spline=interpolate.CubicSpline(np.log(prediction['frequency']),prediction['slope'][-1],axis=0,extrapolate=False)
    raw=replacement.at('readout',spline,profiles[-1])
    unresolved=raw-basis.values@source['projected_replacement'][-1]
    resolved=basis.values@solution['photon'][-1,:,:3]
    total=resolved+unresolved
    old=basis.values@profiles[-1]
    norm=lambda value:np.sqrt(np.sum(basis.measure[:,None]*value**2,axis=0))
    def residual(value):
        eta=(reader.measure*reader.frequency)@value/reader.capacity
        amplitudes=reader.amplitude_matrix@value
        return value-reader.frequency[:,None]*eta-reader.templates@amplitudes
    old_norm=norm(old)
    old_residual_norm=norm(residual(old))
    final_norm=norm(total)
    denominator=np.maximum(old_norm,1e-300)
    projection_quadrature_norm=photon_norm(source['projection_quadrature_difference'][-1],basis.mass)
    energy_error=abs((reader.measure*reader.frequency)@unresolved)
    number_error=abs(reader.measure@unresolved)
    moment_scale=np.maximum((reader.measure*(1+reader.frequency))@(abs(raw)+abs(basis.values@source['projected_replacement'][-1])),1e-300)
    metrics=dict(final_photon_change_over_saved_norm=(final_norm/denominator).tolist(),
        final_residual_change_over_saved_residual=(norm(residual(total))/np.maximum(old_residual_norm,1e-300)).tolist(),
        final_gas_change_over_saved=(abs(solution['gas'][-1,:3])/np.maximum(abs(gas[-1]),1e-300)).tolist(),
        final_resolved_photon_norm=norm(resolved).tolist(),final_unresolved_norm=norm(unresolved).tolist(),
        final_physical_change_norm=final_norm.tolist(),saved_photon_norm=old_norm.tolist(),
        final_saved_residual_norm=old_residual_norm.tolist(),
        fine_vs_canonical_projection_over_replacement=(projection_quadrature_norm/np.maximum(source['replacement_norm'][-1],1e-300)).tolist(),
        unresolved_energy_number_defect=float(np.max((energy_error+number_error)/moment_scale)),
        resolved_component_norms=[norm(basis.values@solution['photon'][-1,:,offset:offset+3]).tolist() for offset in [3,6,9]],
        old_residual_norm=old_residual_norm.tolist(),new_residual_norm=norm(residual(old+total)).tolist())
    output=dict(frequency=basis.nodes,measure=basis.measure,saved_potential=old,
        resolved_change=resolved,unresolved_change=unresolved,physical_change=total,
        residual_change=residual(total),saved_residual=residual(old))
    return metrics,output,dependencies


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--steps',type=int,choices=[512,1024],default=1024)
    args=parser.parse_args()
    modest()
    source_folder=ROOT/'results'/args.source
    status_path=source_folder/'status.json'
    status=json.loads(status_path.read_text())
    assert status['all_checks_passed']
    for path,sha in status['input_hashes'].items():
        assert digest(path)==sha,path
    folder=ROOT/'results'/('response-'+args.source.removeprefix('sources-')+'-n'+str(args.steps))
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,models,inputs=[],{},[status_path,*ladder.inputs]
    for model in ['heavy','cold']:
        path=source_folder/(model+'.npz')
        inputs.append(path)
        with np.load(path) as archive:
            source={key:archive[key].copy() for key in archive.files}
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        solution,errors=solve_response(model,source,args.steps,ladder,emission,background)
        metrics,view,dependencies=readout(basis,model,source,solution,status['variant'],status['match_upper'])
        inputs.extend(dependencies)
        for name,value in errors.items():
            limit=1. if name=='energy_spectrum' else 1e-7
            checks.append(dict(name=name+':'+model,value=value,limit=limit,passed=bool(value<=limit)))
        value=metrics['unresolved_energy_number_defect']
        checks.append(dict(name='Unresolved correction has no duplicated stored moments:'+model,value=value,limit=1e-10,passed=value<=1e-10))
        assert all(np.isfinite(value).all() for value in [*solution.values(),*view.values()])
        np.savez_compressed(folder/(model+'.npz'),**solution,**view)
        models[model]=dict(errors=errors,metrics=metrics)
        print(json.dumps(dict(model=model,source=args.source,steps=args.steps,errors=errors,metrics=metrics)),flush=True)
    finish(folder,dict(checks=checks,models=models,steps=args.steps,source_packet=args.source,
        resolved_response_and_unresolved_shape_both_reported=True,parent_history_rerun=False,
        paired_gas_exchange=True,conditional_response=True,iterated_self_consistent_feedback=False,
        direct_total_and_three_components=True),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
