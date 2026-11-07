from response_sites_common import *
from evaluate_source_probes import sources,response_metrics,source_diagnostics
from direct_common import dual_norm
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def merge_even_sites(previous,fresh):
    coordinate=np.sort(np.concatenate([previous['coordinate'],fresh['coordinate'][1:-1]]))
    assert len(coordinate)==33 and np.all(np.diff(coordinate)>0)
    old_indices=np.searchsorted(coordinate,previous['coordinate'])
    new_indices=np.searchsorted(coordinate,fresh['coordinate'][1:-1])
    result={}
    for key,value in previous.items():
        if value.ndim>0 and value.shape[0]==17:
            result[key]=interpolate.interp1d(previous['coordinate'],value,axis=0)(coordinate)
            result[key][new_indices]=fresh[key][1:-1]
            result[key][old_indices]=value
            assert np.array_equal(result[key][old_indices],value),key
        else:
            result[key]=value.copy()
    result['coordinate']=coordinate
    return result


def full_source(previous,initial,replace):
    coordinate=np.unique(np.concatenate([previous['coordinate'],initial['coordinate']]))
    assert len(coordinate)==138
    old_indices=np.searchsorted(coordinate,previous['coordinate'])
    initial_indices=np.searchsorted(coordinate,initial['coordinate'])
    result={}
    for key,value in previous.items():
        if value.ndim>0 and value.shape[0]==122:
            result[key]=interpolate.interp1d(previous['coordinate'],value,axis=0)(coordinate)
            if replace:
                result[key][initial_indices]=initial[key]
            result[key][old_indices]=value
            assert np.array_equal(result[key][old_indices],value),key
        else:
            result[key]=value.copy()
    result['coordinate']=coordinate
    return result


def save_response(path,response,full):
    stored=dict(response)
    stored['photon_final']=stored['photon'][-1].copy()
    if not full:
        del stored['photon']
    np.savez_compressed(path,**stored,integration_steps=2048,saved_step_indices=np.arange(2049),
        all_photon_steps_saved=full)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    label=int(args.upper*1000)
    folder=ROOT/'results'/f'sites-{args.model}-m{label}'
    folder.mkdir(parents=True,exist_ok=False)
    owner=refined_owner(args.model)
    parent_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    parent=read_npz(parent_path)
    cache_folder=owner/'results'/f'feedback-m{label}-n40960'
    cache=read_npz(cache_folder/'source-cache.npz')
    replay_path=ROOT/'results'/f'replay-{args.model}-s00000/prediction.npz'
    assert local_packet(replay_path.parent)['all_checks_passed']
    replay=read_npz(replay_path)
    assert np.array_equal(replay['saved_step_indices'],SOURCE_STEPS)
    chosen=(SOURCE_STEPS%40==20)|(SOURCE_STEPS==0)|(SOURCE_STEPS==640)
    prediction=dict(parent)
    for key in ['coordinate','defect','profiles','gas']:
        prediction[key]=replay[key][chosen].copy()
    assert len(prediction['coordinate'])==18
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    free_free=FreeFree(background,cache['frequency'])
    order=8 if args.upper==.04 else 6
    old_bank_path=BRANCH/'direct-doppler-compton-feedback-20261012/results'/f'bank-o{order}-q32-m{label}/bank.npz'
    old=read_npz(old_bank_path)
    fresh_path=ROOT/'results'/f'operator-m{label}/bank.npz'
    assert local_packet(fresh_path.parent)['all_checks_passed']
    bank=read_npz(fresh_path)
    assert np.array_equal(bank['steps'],SOURCE_STEPS[1:-1])
    assert np.array_equal(bank['coordinate'],replay['coordinate'][1:-1])
    events=dict(old)
    events['adjoint']=interpolate.interp1d(old['coordinate'],old['adjoint'],axis=0)(prediction['coordinate'])
    direct_events=dict(events)
    direct_events['adjoint']=events['adjoint'].copy()
    direct_events['adjoint'][1:-1]=bank['adjoint'][bank['steps']%40==20]
    prior_folder=PARENT/'results'/f'transient-{args.model}-m{label}'
    prior_status=local_packet(prior_folder)
    inputs=[parent_path,parent_path.parent/'status.json',cache_folder/'source-cache.npz',
        replay_path,replay_path.parent/'status.json',old_bank_path,fresh_path,fresh_path.parent/'status.json',
        prior_folder/'status.json',*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants]
    checks=[]
    evaluated={}
    for variant,event_set in [('assembled',events),('direct',direct_events)]:
        fresh,group,errors=sources(basis,ladder,prediction,cache,event_set,background,emission,free_free,args.upper)
        previous_path=prior_folder/(variant+'-evaluated.npz')
        previous=read_npz(previous_path)
        inputs.append(previous_path)
        checks.extend(dict(row,name=variant+':'+row['name']) for row in group)
        delta=fresh['source'][[0,-1]]-previous['source'][[0,-1]]
        scale=dual_norm(previous['raw_source'][[0,-1]],basis)+dual_norm(previous['overlap_source'][[0,-1]],basis)
        checks.append(check('Old interval ends:'+variant,np.max(dual_norm(delta,basis)/np.maximum(scale,1e-300)),1e-10))
        evaluated[variant]=merge_even_sites(previous,fresh)
        np.savez_compressed(folder/(variant+'-fresh.npz'),**fresh)
        np.savez_compressed(folder/(variant+'-evaluated.npz'),**evaluated[variant])
    assert np.array_equal(evaluated['assembled']['source'][:,1:],evaluated['direct']['source'][:,1:])
    comparisons,convergence,diagnostics,sampling={}, {}, {}, {}
    for variant in ['assembled','direct']:
        old_source_path=prior_folder/f'{variant}-16-source.npz'
        old_response_path=prior_folder/f'{variant}-16-response.npz'
        earlier_response_path=prior_folder/f'{variant}-8-response.npz'
        old_source=read_npz(old_source_path)
        old_response=read_npz(old_response_path)
        earlier_response=read_npz(earlier_response_path)
        inputs.extend([old_source_path,old_response_path,earlier_response_path])
        candidate=full_source(old_source,evaluated[variant],True)
        control=full_source(old_source,evaluated[variant],False)
        start,end=candidate['coordinate'][[0,-1]]
        response_points=np.array([float(start+(end-start)*index/2048) for index in range(2049)])
        collision_source=interpolate.interp1d(candidate['coordinate'],candidate['source'],axis=0)(response_points)
        sampled_error=dual_norm(collision_source[:33]-evaluated[variant]['source'],basis)
        sampled_scale=np.maximum(dual_norm(evaluated[variant]['source'],basis).max(axis=0),1e-300)
        forcing_error=float(np.max(sampled_error/sampled_scale))
        checks.append(check('Every initial response site supplied:'+variant,forcing_error,1e-10))
        coordinate_error=float(np.max(abs(response_points[:33]-evaluated[variant]['coordinate'])))
        checks.append(check('Initial source and response coordinates:'+variant,coordinate_error,4*np.spacing(float(end))))
        collocated=dict(coordinate=response_points,source=collision_source.copy())
        collocated['source'][:33]=evaluated[variant]['source']
        null_midpoints=(response_points[:32]+response_points[1:33])/2
        null_coordinate=np.sort(np.concatenate([response_points[:33],null_midpoints]))
        null_values=np.zeros(65)
        null_values[np.searchsorted(null_coordinate,null_midpoints)]=1.
        null_at=interpolate.interp1d(null_coordinate,null_values)
        checks.append(check('Between-update null probe:'+variant,np.max(abs(null_at(response_points[:33]))),1e-14))
        assert np.min(null_at(null_midpoints))>.99
        np.savez_compressed(folder/(variant+'-sampling-contract.npz'),response_coordinate=response_points,
            interpolated_forcing=collision_source[:33],direct_forcing=evaluated[variant]['source'],
            null_coordinate=null_coordinate,null_values=null_values)
        diagnostics[variant]=source_diagnostics('32_vs_16',evaluated[variant]['source'],
            interpolate.interp1d(old_source['coordinate'],old_source['source'],axis=0)(evaluated[variant]['coordinate']),basis)
        for column_index,column in enumerate(['baseline','join1','join2']):
            checks.append(check('Source1percent:'+variant+':'+column,
                np.max(np.array(diagnostics[variant]['relative_to_components'])[:,column_index]),.01))
        comparisons[variant]={}
        responses={}
        for representation,source in [('control',control),('sites32',candidate),('collocated',collocated)]:
            np.savez_compressed(folder/f'{variant}-{representation}-source.npz',**source)
            solution,errors=solve_response(args.model,source,2048,ladder,emission,background)
            metrics,view=readout(basis,parent,candidate,solution,args.upper)
            response={**solution,**view}
            save_response(folder/f'{variant}-{representation}-response.npz',response,representation=='sites32')
            reference=responses['sites32'] if representation=='collocated' else old_response
            comparison=response_metrics(response,reference,basis)
            parts=np.stack([solution['gas'][-1,offset:offset+3] for offset in [3,6,9]])
            comparison['gas_endpoint_components']=parts.tolist()
            comparison['endpoint_cancellation_factor']=(abs(parts).sum(axis=0)/np.maximum(abs(solution['gas'][-1,:3]),1e-300)).tolist()
            comparisons[variant][representation]=dict(comparison=comparison,response_errors=errors)
            checks.extend(check('Response:'+variant+':'+representation+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
            checks.append(check('Unresolved moments:'+variant+':'+representation,metrics['unresolved_energy_number_defect'],1e-10))
            if representation!='sites32':
                for metric in ['radiation_relative','gas_peak_relative']:
                    checks.append(check('Tabulation control:'+variant+':'+representation+':'+metric,max(comparison[metric]),1e-7))
            else:
                for metric in ['radiation_relative','gas_peak_relative','gas_late_relative','gas_endpoint_relative']:
                    checks.extend(check('Refinement1percent:'+variant+':'+metric+':'+column,value,.01)
                        for column,value in zip(['baseline','join1','join2'],comparison[metric]))
            responses[representation]=response
            print(json.dumps(dict(model=args.model,upper=args.upper,variant=variant,
                representation=representation,seconds=time.monotonic()-started)),flush=True)
        coarse=old_response['gas'][:,:3]-earlier_response['gas'][:,:3]
        fine=responses['sites32']['gas'][:,:3]-old_response['gas'][:,:3]
        convergence[variant]=dict(endpoint_difference_ratio=(abs(fine[-1])/np.maximum(abs(coarse[-1]),1e-300)).tolist(),
            peak_difference_ratio=(abs(fine).max(axis=0)/np.maximum(abs(coarse).max(axis=0),1e-300)).tolist(),
            late_difference_ratio=(abs(fine[1536:]).max(axis=0)/np.maximum(abs(coarse[1536:]).max(axis=0),1e-300)).tolist(),
            signed_endpoint_changes=[coarse[-1].tolist(),fine[-1].tolist()],
            gas_endpoints={str(level):response['gas'][-1,:3].tolist() for level,response in
                [(8,earlier_response),(16,old_response),(32,responses['sites32'])]})
        sampling[variant]=dict(initial_response_updates=32,initial_source_samples=33,source_site_roundoff=coordinate_error,
            sampled_forcing_relative_error=forcing_error,remaining_unsupplied_initial_response_sites=0,
            source_interpolation_closed_for_this_fixed_recurrence=True,physical_time_accuracy_certified=False)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,columns=['baseline','join1','join2'],
        comparisons=comparisons,convergence=convergence,source_differences=diagnostics,sampling=sampling,
        original_failed_checks=[row for row in prior_status['checks'] if not row['passed']],
        fixed_frequency_nodes=5265,inner_steps=40960,response_steps=2048,
        source_subdivisions=[16,32],source_knot_counts=[122,138],
        initial_state_tuned=False,inner_coefficients_resampled=False,other_source_intervals_changed=False,
        seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
