from transient_common import *
from evaluate_source_probes import sources,response_metrics,source_diagnostics
from direct_common import dual_norm
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def retabulate(parent,evaluated,subdivisions,replace=True):
    added=evaluated['coordinate'][::16//subdivisions]
    coordinate=np.unique(np.concatenate([parent['coordinate'],added]))
    old_selection=np.searchsorted(coordinate,parent['coordinate'])
    selection=np.searchsorted(coordinate,added)
    hybrid={}
    for key,value in parent.items():
        if value.ndim>0 and value.shape[0]==len(parent['coordinate']):
            hybrid[key]=interpolate.interp1d(parent['coordinate'],value,axis=0,bounds_error=True)(coordinate)
            if replace:
                hybrid[key][selection]=evaluated[key][::16//subdivisions]
            hybrid[key][old_selection]=value
            assert np.array_equal(hybrid[key][old_selection],value),key
        else:
            hybrid[key]=value.copy()
    hybrid['coordinate']=coordinate
    return hybrid


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    label=int(args.upper*1000)
    folder=ROOT/'results'/f'transient-{args.model}-m{label}'
    folder.mkdir(parents=True,exist_ok=False)
    owner=refined_owner(args.model)
    parent_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    parent=read_npz(parent_path)
    cache_folder=owner/'results'/f'feedback-m{label}-n40960'
    cache=read_npz(cache_folder/'source-cache.npz')
    replay_folder=ROOT/'results'/f'replay-{args.model}-s00000'
    assert local_packet(replay_folder)['all_checks_passed']
    replay=read_npz(replay_folder/'prediction.npz')
    frozen=read_npz(replay_folder/'frozen-reference.npz')
    mask=replay['saved_step_indices']%40==0
    assert np.array_equal(replay['saved_step_indices'][mask],SOURCE_STEPS)
    prediction=dict(parent)
    frozen_prediction=dict(parent)
    for key in ['coordinate','defect','profiles','gas']:
        prediction[key]=replay[key][mask].copy()
        frozen_prediction[key]=prediction[key].copy()
    frozen_prediction['defect']=frozen['defect'][mask]
    assert np.array_equal(frozen['saved_step_indices'],replay['saved_step_indices'])
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
    fresh=read_npz(fresh_path)
    assert np.array_equal(fresh['steps'],SOURCE_STEPS[1:-1])
    assert np.array_equal(fresh['coordinate'],prediction['coordinate'][1:-1])
    assert np.array_equal(cache['inner_frequency'],parent['frequency'])
    events=dict(old)
    events['adjoint']=interpolate.interp1d(old['coordinate'],old['adjoint'],axis=0,bounds_error=True)(prediction['coordinate'])
    direct_events=dict(events)
    direct_events['adjoint']=events['adjoint'].copy()
    direct_events['adjoint'][1:-1]=fresh['adjoint']
    inputs=[parent_path,parent_path.parent/'status.json',cache_folder/'source-cache.npz',
        replay_folder/'prediction.npz',replay_folder/'status.json',replay_folder/'frozen-reference.npz',
        replay_folder/'initial-law.npz',old_bank_path,fresh_path,fresh_path.parent/'status.json',
        *ladder.inputs,*emission.inputs,*free_free.inputs,background.parent.source,background.native_constants]
    evaluated={}
    checks=[]
    for variant,event_set,trajectory in [('assembled',events,prediction),('direct',direct_events,prediction),
            ('frozen',direct_events,frozen_prediction)]:
        result,group,errors=sources(basis,ladder,trajectory,cache,event_set,background,emission,free_free,args.upper)
        evaluated[variant]=result
        checks.extend(dict(row,name=variant+':'+row['name']) for row in group)
        np.savez_compressed(folder/(variant+'-evaluated.npz'),**result)
    law=read_npz(replay_folder/'initial-law.npz')
    slope_prediction=dict(prediction)
    for key in ['coordinate','profiles','gas']:
        slope_prediction[key]=np.repeat(prediction[key][:1],2,axis=0)
    slope_prediction['defect']=np.stack([np.zeros_like(law['initial_drive']),law['initial_drive']])
    slope_events=dict(events)
    slope_events['adjoint']=np.repeat(events['adjoint'][:1],2,axis=0)
    slope_source,slope_checks,slope_errors=sources(basis,ladder,slope_prediction,cache,slope_events,background,emission,free_free,args.upper)
    checks.extend(dict(row,name='initial-source-derivative:'+row['name']) for row in slope_checks)
    initial_source_derivative=slope_source['source'][1]
    np.savez_compressed(folder/'initial-source-derivative.npz',source=initial_source_derivative,
        coordinate=prediction['coordinate'][0],initial_drive=law['initial_drive'])
    transient_diagnostics=source_diagnostics('frozen_vs_actual',evaluated['frozen']['source'][1:],
        evaluated['direct']['source'][1:],basis)
    tau=prediction['coordinate'][1:]-prediction['coordinate'][0]
    slope_diagnostics=source_diagnostics('linear_initial_slope_vs_actual',
        tau[:,None,None,None]*initial_source_derivative[None],evaluated['direct']['source'][1:],basis)
    comparisons={}
    convergence={}
    source_differences={}
    parent_folder=PARENT/'results'/f'probe-{args.model}-m{label}'
    parent_status=local_packet(parent_folder)
    inputs.append(parent_folder/'status.json')
    for variant in ['assembled','direct']:
        original_source=read_npz(parent_folder/(variant+'-source.npz'))
        original_response=read_npz(parent_folder/(variant+'-response.npz'))
        inputs.extend([parent_folder/(variant+'-source.npz'),parent_folder/(variant+'-response.npz')])
        endpoint_selection=np.searchsorted(original_source['coordinate'],prediction['coordinate'][::4])
        delta=evaluated[variant]['source'][::4]-original_source['source'][endpoint_selection]
        scale=dual_norm(original_source['raw_source'][endpoint_selection],basis)+dual_norm(original_source['overlap_source'][endpoint_selection],basis)
        checks.append(check('Prior quarter source:'+variant,np.max(dual_norm(delta,basis)/np.maximum(scale,1e-300)),1e-10))
        previous_source,previous_response=original_source,original_response
        saved_responses={4:original_response}
        differences=[]
        comparisons[variant]={}
        source_differences[variant]={}
        for refinement in ['control',8,16]:
            subdivisions=16 if refinement=='control' else refinement
            hybrid=retabulate(original_source,evaluated[variant],subdivisions,refinement!='control')
            assert len(hybrid['coordinate'])==(114 if subdivisions==8 else 122)
            np.savez_compressed(folder/f'{variant}-{refinement}-source.npz',**hybrid)
            solution,errors=solve_response(args.model,hybrid,2048,ladder,emission,background)
            metrics,view=readout(basis,parent,hybrid,solution,args.upper)
            response={**solution,**view}
            np.savez_compressed(folder/f'{variant}-{refinement}-response.npz',**response,integration_steps=2048,
                saved_step_indices=np.arange(2049),all_steps_saved=True)
            reference=original_response if refinement=='control' else previous_response
            comparison=response_metrics(response,reference,basis)
            components=np.stack([solution['gas'][-1,offset:offset+3] for offset in [3,6,9]])
            comparison['gas_endpoint_components']=components.tolist()
            comparison['endpoint_cancellation_factor']=(abs(components).sum(axis=0)/np.maximum(abs(solution['gas'][-1,:3]),1e-300)).tolist()
            comparisons[variant][str(refinement)]=dict(comparison=comparison,response_errors=errors)
            checks.extend(check('Response:'+variant+':'+str(refinement)+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
            checks.append(check('Unresolved moments:'+variant+':'+str(refinement),metrics['unresolved_energy_number_defect'],1e-10))
            if refinement=='control':
                for metric in ['radiation_relative','gas_peak_relative']:
                    checks.append(check('Retabulation control:'+variant+':'+metric,max(comparison[metric]),1e-7))
            else:
                for metric in ['radiation_relative','gas_peak_relative','gas_late_relative','gas_endpoint_relative']:
                    checks.extend(check('Refinement1percent:'+variant+':'+str(refinement)+':'+metric+':'+column,value,.01)
                        for column,value in zip(['baseline','join1','join2'],comparison[metric]))
                difference=solution['gas'][:,:3]-previous_response['gas'][:,:3]
                differences.append(difference)
                source_new=interpolate.interp1d(hybrid['coordinate'],hybrid['source'],axis=0)(prediction['coordinate'])
                source_old=interpolate.interp1d(previous_source['coordinate'],previous_source['source'],axis=0)(prediction['coordinate'])
                diagnostic=source_diagnostics(str(refinement)+'_vs_'+str(refinement//2),source_new,source_old,basis)
                source_differences[variant][str(refinement)]=diagnostic
                for column_index,column in enumerate(['baseline','join1','join2']):
                    checks.append(check('Source1percent:'+variant+':'+str(refinement)+':'+column,
                        np.max(np.array(diagnostic['relative_to_components'])[:,column_index]),.01))
                saved_responses[refinement]=response
                previous_source,previous_response=hybrid,response
            print(json.dumps(dict(model=args.model,upper=args.upper,variant=variant,refinement=refinement,
                seconds=time.monotonic()-started)),flush=True)
        coarse,fine=differences
        convergence[variant]=dict(endpoint_difference_ratio=(abs(fine[-1])/np.maximum(abs(coarse[-1]),1e-300)).tolist(),
            peak_difference_ratio=(abs(fine).max(axis=0)/np.maximum(abs(coarse).max(axis=0),1e-300)).tolist(),
            late_difference_ratio=(abs(fine[1536:]).max(axis=0)/np.maximum(abs(coarse[1536:]).max(axis=0),1e-300)).tolist(),
            signed_endpoint_changes=[coarse[-1].tolist(),fine[-1].tolist()],
            observed_endpoint_order=(-np.log2(np.maximum(abs(fine[-1])/np.maximum(abs(coarse[-1]),1e-300),1e-300))).tolist(),
            gas_endpoints={str(level):response['gas'][-1,:3].tolist() for level,response in saved_responses.items()})
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,columns=['baseline','join1','join2'],
        comparisons=comparisons,convergence=convergence,source_differences=source_differences,
        frozen_source_diagnostic=transient_diagnostics,linear_initial_slope_diagnostic=slope_diagnostics,
        original_failed_checks=[row for row in parent_status['checks'] if not row['passed']],
        fixed_frequency_nodes=5265,inner_steps=40960,response_steps=2048,
        source_subdivisions=[4,8,16],source_knot_counts=[110,114,122],
        initial_state_tuned=False,frozen_reference_replaces_physical_trajectory=False,
        inner_coefficients_resampled=False,other_source_intervals_changed=False,
        seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
