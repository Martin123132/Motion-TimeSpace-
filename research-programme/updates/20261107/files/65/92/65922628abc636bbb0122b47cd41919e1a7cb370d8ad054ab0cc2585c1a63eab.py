from source_probe_common import *
from direct_common import dual_norm
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def sources(basis,ladder,prediction,cache,events,background,emission,free_free,upper):
    raw,represented,projections,moments,raw_norm,unresolved_norm,projection_changes=[],[],[],[],[],[],[]
    bank_at=interpolate.interp1d(prediction['coefficient_knots'],prediction['coefficient_bank'],axis=0,bounds_error=True)
    errors={key:0. for key in ['mass_projection','dc_energy','compton_number','dc_represented_energy','compton_represented_number','source_decomposition']}
    for epoch,coordinate in enumerate(prediction['coordinate']):
        theta=background.at(float(coordinate))['thermal_parameter']
        values=prediction['defect'][epoch]
        canonical=compact_defect(basis.nodes,prediction['frequency'],values,upper)
        quadrature=compact_defect(cache['frequency'],prediction['frequency'],values,upper)
        event_values=compact_defect(events['frequency'],prediction['frequency'],values,upper)
        moment=(basis.values.T*basis.measure)@canonical
        projected=linalg.solve(basis.mass,moment,assume_a='pos')
        refined=cache['projection']@quadrature
        projection_changes.append(linalg.solve(basis.mass,refined-moment,assume_a='pos'))
        scattering=events['adjoint'][epoch]@event_values
        kappa=bank_at(coordinate)[len(prediction['offsets'])+1]
        dc=kappa*(cache['dc_operator']@values)
        br=-cache['projection']@(free_free.br_rates(theta)[:,None]*quadrature)
        source=np.stack([scattering,dc,br])
        operators=np.stack([ladder.at(theta,0)[:96,:96],-emission.at(theta,'dc'),-emission.interpolator(math.log(theta))])
        old=np.einsum('tij,jk->tik',operators,projected)
        projection_scale=np.maximum(np.linalg.norm(moment,axis=0),1e-300)
        errors['mass_projection']=max(errors['mass_projection'],float(np.max(np.linalg.norm(basis.mass@projected-moment,axis=0)/projection_scale)))
        for name,vector,row in [('dc_energy',dc,basis.temperature),('compton_number',scattering,basis.chemical),
                ('dc_represented_energy',old[1],basis.temperature),('compton_represented_number',old[0],basis.chemical)]:
            scale=np.maximum(abs(row)@abs(vector),1e-300)
            errors[name]=max(errors[name],float(np.max(abs(row@vector)/scale)))
        combined=(ladder.at(theta,0)[:96,:96]-emission.at(theta,'dcbr'))@projected
        operand=np.maximum(np.linalg.norm(abs(operators).sum(axis=0)@abs(projected),axis=0),1e-300)
        errors['source_decomposition']=max(errors['source_decomposition'],float(np.max(np.linalg.norm(old.sum(axis=0)-combined,axis=0)/operand)))
        raw.append(source)
        represented.append(old)
        projections.append(projected)
        moments.append(moment)
        raw_norm.append(norm(canonical,basis.measure))
        unresolved_norm.append(norm(canonical-basis.values@projected,basis.measure))
    raw,represented=np.array(raw),np.array(represented)
    source=raw-represented
    result=dict(coordinate=prediction['coordinate'],source=source,raw_source=raw,overlap_source=represented,
        projected_replacement=np.array(projections),replacement_moments=np.array(moments),replacement_norm=np.array(raw_norm),
        unresolved_norm=np.array(unresolved_norm),projection_quadrature_difference=np.array(projection_changes),
        number_source=np.einsum('i,ntik->ntk',basis.chemical,source),energy_source=np.einsum('i,ntik->ntk',basis.temperature,source),
        profiles=prediction['profiles'],gas=prediction['gas'],match_upper=upper)
    checks=[check(name,value,1e-10) for name,value in errors.items()]
    checks.append(dict(name='Zero initial source',passed=not np.count_nonzero(source[0])))
    return result,checks,errors


def source_diagnostics(label,current,reference,basis):
    delta=current-reference
    current_components=dual_norm(current,basis)
    reference_components=dual_norm(reference,basis)
    difference=dual_norm(delta.sum(axis=1),basis)
    total_scale=np.maximum(dual_norm(current.sum(axis=1),basis),dual_norm(reference.sum(axis=1),basis))
    component_scale=np.maximum(current_components.sum(axis=1),reference_components.sum(axis=1))
    floor=100*np.finfo(float).eps*np.maximum(component_scale.max(axis=0),1e-300)
    resolved=total_scale>floor
    return dict(label=label,difference_absolute=difference.tolist(),total_denominator=total_scale.tolist(),
        component_denominator=component_scale.tolist(),total_denominator_resolved=resolved.tolist(),
        relative_to_total=(difference/np.maximum(total_scale,1e-300)).tolist(),
        relative_to_components=(difference/np.maximum(component_scale,1e-300)).tolist(),
        component_absolute=dual_norm(delta,basis).tolist(),
        energy_moment=np.einsum('i,ntik->ntk',basis.temperature,delta).tolist(),
        number_moment=np.einsum('i,ntik->ntk',basis.chemical,delta).tolist())


def response_metrics(current,reference,basis):
    delta=current['gas'][:,:3]-reference['gas'][:,:3]
    peak=abs(reference['gas'][:,:3]).max(axis=0)
    late=abs(reference['gas'][1536:,:3]).max(axis=0)
    endpoint=abs(reference['gas'][-1,:3])
    radiation=norm(current['physical_change']-reference['physical_change'],basis.measure)
    return dict(radiation_relative=(radiation/np.maximum(norm(reference['physical_change'],basis.measure),1e-300)).tolist(),
        gas_peak_relative=(abs(delta).max(axis=0)/np.maximum(peak,1e-300)).tolist(),
        gas_late_relative=(abs(delta[1536:]).max(axis=0)/np.maximum(late,1e-300)).tolist(),
        gas_endpoint_relative=(abs(delta[-1])/np.maximum(endpoint,1e-300)).tolist(),
        gas_peak_denominator=peak.tolist(),gas_late_denominator=late.tolist(),gas_endpoint_denominator=endpoint.tolist(),
        gas_endpoint_signed_difference=delta[-1].tolist(),gas_endpoint=current['gas'][-1,:3].tolist(),
        reference_gas_endpoint=reference['gas'][-1,:3].tolist(),
        endpoint_near_zero=(endpoint<=1e-6*peak).tolist(),
        endpoint_sign_preserved=(np.sign(current['gas'][-1,:3])==np.sign(reference['gas'][-1,:3])).tolist())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'probe-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    owner=refined_owner(args.model)
    inner_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    parent=read_npz(inner_path)
    source_folder=owner/'results'/f'feedback-m{int(args.upper*1000)}-n40960'
    parent_source=read_npz(source_folder/(args.model+'-source.npz'))
    parent_response=read_npz(source_folder/(args.model+'-response.npz'))
    source_status=local_packet(source_folder)
    cache=read_npz(source_folder/'source-cache.npz')
    inputs=[inner_path,inner_path.parent/'status.json',source_folder/'source-cache.npz',
        source_folder/'status.json',source_folder/(args.model+'-source.npz'),source_folder/(args.model+'-response.npz')]
    all_states={}
    for restart in RESTART_STEPS:
        replay_path=ROOT/'results'/f'replay-{args.model}-s{restart:05d}/prediction.npz'
        assert local_packet(replay_path.parent)['all_checks_passed']
        replay=read_npz(replay_path)
        inputs.extend([replay_path,replay_path.parent/'status.json'])
        for index,step in enumerate(replay['saved_step_indices']):
            assert int(step) not in all_states
            all_states[int(step)]={key:replay[key][index] for key in ['coordinate','defect','profiles','gas']}
    all_steps=np.array(sorted(all_states))
    prediction=dict(parent)
    for key in ['coordinate','defect','profiles','gas']:
        prediction[key]=np.array([all_states[int(step)][key] for step in all_steps])
    new_mask=all_steps%640!=0
    new_steps=all_steps[new_mask]
    assert len(new_steps)==45 and len(all_steps)==68
    np.savez_compressed(folder/'sampled-states.npz',steps=all_steps,coordinate=prediction['coordinate'],defect=prediction['defect'])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    event_order=8 if args.upper==.04 else 6
    old_bank_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{event_order}-q32-m{int(args.upper*1000)}/bank.npz'
    old_events=read_npz(old_bank_path)
    fresh_bank_path=ROOT/'results'/f'operator-m{int(args.upper*1000)}/bank.npz'
    assert local_packet(fresh_bank_path.parent)['all_checks_passed']
    fresh=read_npz(fresh_bank_path)
    assert np.array_equal(new_steps,fresh['steps'])
    assert np.array_equal(prediction['coordinate'][new_mask],fresh['coordinate'])
    assert np.array_equal(cache['inner_frequency'],parent['frequency'])
    events=dict(old_events)
    events['adjoint']=interpolate.interp1d(old_events['coordinate'],old_events['adjoint'],axis=0,bounds_error=True)(prediction['coordinate'])
    direct_events=dict(events)
    direct_events['adjoint']=events['adjoint'].copy()
    direct_events['adjoint'][new_mask]=fresh['adjoint']
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    free_free=FreeFree(background,cache['frequency'])
    inputs.extend([*ladder.inputs,old_bank_path,fresh_bank_path,fresh_bank_path.parent/'status.json',
        *emission.inputs,*free_free.inputs,background.parent.source,background.native_constants])
    assembled,assembled_checks,assembled_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
    direct,direct_checks,direct_errors=sources(basis,ladder,prediction,cache,direct_events,background,emission,free_free,args.upper)
    np.savez_compressed(folder/'assembled-evaluated.npz',**assembled)
    np.savez_compressed(folder/'direct-evaluated.npz',**direct)
    checks=[]
    for label,group in [('Assembled',assembled_checks),('Direct',direct_checks)]:
        checks.extend(dict(row,name=label+':'+row['name']) for row in group)
    old_at=interpolate.interp1d(parent_source['coordinate'],parent_source['source'],axis=0,bounds_error=True)(prediction['coordinate'])
    old_indices=all_steps[~new_mask]//640
    endpoint_difference=dual_norm(direct['source'][~new_mask]-parent_source['source'][old_indices],basis)
    endpoint_scale=dual_norm(parent_source['raw_source'][old_indices],basis)+dual_norm(parent_source['overlap_source'][old_indices],basis)
    checks.append(check('Saved source endpoints reproduced',np.max(endpoint_difference/np.maximum(endpoint_scale,1e-300)),1e-10))
    decomposition=direct['source']-old_at-(assembled['source']-old_at)-(direct['source']-assembled['source'])
    checks.append(check('State and operator difference decomposition',np.max(abs(decomposition))/max(float(np.max(abs(direct['source']))),1e-300),1e-14))
    diagnostics=[source_diagnostics('assembly_vs_linear',assembled['source'][new_mask],old_at[new_mask],basis),
        source_diagnostics('direct_vs_linear',direct['source'][new_mask],old_at[new_mask],basis),
        source_diagnostics('operator_increment',direct['source'][new_mask],assembled['source'][new_mask],basis)]
    for row in diagnostics:
        for index,column in enumerate(['baseline','join1','join2']):
            checks.append(check('Source diagnostic1percent:'+row['label']+':'+column,
                np.max(np.array(row['relative_to_components'])[:,index]),.01))
    np.savez_compressed(folder/'point-sources.npz',steps=new_steps,coordinate=prediction['coordinate'][new_mask],
        linear=old_at[new_mask],assembled=assembled['source'][new_mask],direct=direct['source'][new_mask])
    coordinate=np.sort(np.concatenate([parent_source['coordinate'],prediction['coordinate'][new_mask]]))
    old_selection=np.searchsorted(coordinate,parent_source['coordinate'])
    new_selection=np.searchsorted(coordinate,prediction['coordinate'][new_mask])
    assert len(coordinate)==110 and np.all(np.diff(coordinate)>0)
    variants={}
    for label,evaluated in [('linear',None),('assembled',assembled),('direct',direct)]:
        hybrid={}
        for key,value in parent_source.items():
            if value.ndim>0 and value.shape[0]==65:
                hybrid[key]=interpolate.interp1d(parent_source['coordinate'],value,axis=0,bounds_error=True)(coordinate)
                if evaluated is not None:
                    hybrid[key][new_selection]=evaluated[key][new_mask]
                hybrid[key][old_selection]=value
            else:
                hybrid[key]=value.copy()
        hybrid['coordinate']=coordinate
        for key,value in parent_source.items():
            if value.ndim>0 and value.shape[0]==65:
                assert np.array_equal(hybrid[key][old_selection],value),key
        np.savez_compressed(folder/(label+'-source.npz'),**hybrid)
        solution,errors=solve_response(args.model,hybrid,2048,ladder,emission,background)
        metrics,view=readout(basis,parent,hybrid,solution,args.upper)
        np.savez_compressed(folder/(label+'-response.npz'),**solution,**view,integration_steps=2048,
            saved_step_indices=np.arange(2049),all_steps_saved=True)
        comparison=response_metrics({**solution,**view},parent_response,basis)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
        if label=='linear':
            for metric in ['radiation_relative','gas_peak_relative']:
                checks.append(check('Retabulation control:'+metric,max(comparison[metric]),1e-7))
        else:
            for metric in ['radiation_relative','gas_peak_relative','gas_late_relative','gas_endpoint_relative']:
                checks.extend(check('Sampled response1percent:'+label+':'+metric+':'+column,value,.01)
                    for column,value in zip(['baseline','join1','join2'],comparison[metric]))
        variants[label]=dict(comparison=comparison,response_errors=errors,metrics=metrics)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,columns=['baseline','join1','join2'],
        diagnostics=diagnostics,variants=variants,original_response_failures=[row for row in source_status['checks'] if not row['passed']],
        new_source_points=45,total_source_points=110,sampled_intervals=PROBE_INTERVALS,full_history_source_refinement=False,
        frequency_nodes=5265,inner_steps=40960,response_steps=2048,inner_coefficients_resampled=False,
        new_source_adjoint_evaluations_reused_between_backgrounds=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,variants={key:value['comparison'] for key,value in variants.items()},
        failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
