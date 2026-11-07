from quadrature_common import *
from evaluate_source_probes import response_metrics,source_diagnostics
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def save_response(path,response,full):
    stored=dict(response)
    stored['photon_final']=stored['photon'][-1].copy()
    if not full:
        del stored['photon']
    np.savez_compressed(path,**stored,integration_steps=2048,all_photon_steps_saved=full)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.04,.02],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    label=int(args.upper*1000)
    folder=ROOT/'results'/f'comparison-{args.model}-m{label}'
    folder.mkdir(parents=True,exist_ok=False)
    prior=PARENT/'results'/f'sites-{args.model}-m{label}'
    prior_status=local_packet(prior)
    original_source_path=prior/'direct-sites32-source.npz'
    original_response_path=prior/'direct-sites32-response.npz'
    original_source=read_npz(original_source_path)
    original_response=read_npz(original_response_path)
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    inner=read_npz(inner_path)
    replay_path=PARENT/'results'/f'replay-{args.model}-s00000/prediction.npz'
    replay=read_npz(replay_path)
    mask=replay['saved_step_indices']%40==20
    assert np.array_equal(replay['saved_step_indices'][mask],ODD_STEPS)
    coordinate=replay['coordinate'][mask]
    source_indices=np.searchsorted(original_source['coordinate'],coordinate)
    assert np.array_equal(original_source['coordinate'][source_indices],coordinate)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    inputs=[original_source_path,original_response_path,prior/'status.json',inner_path,inner_path.parent/'status.json',
        replay_path,replay_path.parent/'status.json',*ladder.inputs,*emission.inputs,background.parent.source,background.native_constants]
    checks,results,source_sets,response_sets=[],{}, {'legacy':original_source},{'legacy':original_response}
    control_solution,control_errors=solve_response(args.model,original_source,2048,ladder,emission,background)
    control_metrics,control_view=readout(basis,inner,original_source,control_solution,args.upper)
    control_response={**control_solution,**control_view}
    control_comparison=response_metrics(control_response,original_response,basis)
    save_response(folder/'legacy-control-response.npz',control_response,False)
    for metric in ['gas_peak_relative','radiation_relative']:
        checks.append(check('Legacy reproduction:'+metric,max(control_comparison[metric]),1e-7))
    checks.extend(check('Response:legacy-control:'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in control_errors.items())
    for variant in VARIANTS:
        bank_path=ROOT/'results'/f'bank-{variant}-m{label}/bank.npz'
        assert local_packet(bank_path.parent)['all_checks_passed']
        bank=read_npz(bank_path)
        assert np.array_equal(bank['coordinate'],coordinate)
        inputs.extend([bank_path,bank_path.parent/'status.json'])
        source={key:value.copy() for key,value in original_source.items()}
        new_raw=[]
        for selected,index in enumerate(source_indices):
            defect=compact_defect(bank['frequency'],replay['frequency'],replay['defect'][mask][selected],args.upper)
            scattering=bank['adjoint'][selected]@defect
            new_raw.append(scattering)
            source['raw_source'][index,0]=scattering
            source['source'][index,0]=scattering-source['overlap_source'][index,0]
            source['energy_source'][index,0]=basis.temperature@source['source'][index,0]
            source['number_source'][index,0]=basis.chemical@source['source'][index,0]
        changed=np.zeros(len(source['coordinate']),dtype=bool)
        changed[source_indices]=True
        for key in ['source','raw_source','energy_source','number_source']:
            assert np.array_equal(source[key][~changed],original_source[key][~changed]),key
            assert np.array_equal(source[key][:,1:],original_source[key][:,1:]),key
        assert np.array_equal(source['overlap_source'],original_source['overlap_source'])
        new_raw=np.array(new_raw)
        checks.append(check('Number source:'+variant,np.max(abs(np.einsum('i,nik->nk',basis.chemical,new_raw))),1e-14))
        if variant=='stable':
            old_raw=original_source['raw_source'][source_indices,0]
            energy_difference=np.einsum('i,nik->nk',basis.temperature,new_raw-old_raw)
            scale=np.maximum(np.einsum('i,nik->nk',abs(basis.temperature),abs(old_raw)),1e-300)
            checks.append(check('Same-rule energy source unchanged',np.max(abs(energy_difference)/scale),1e-10))
        np.savez_compressed(folder/(variant+'-source.npz'),**source)
        solution,errors=solve_response(args.model,source,2048,ladder,emission,background)
        metrics,view=readout(basis,inner,source,solution,args.upper)
        response={**solution,**view}
        save_response(folder/(variant+'-response.npz'),response,variant in ['stable','event2','frequency2','joint'])
        references={'stable':['legacy'],'event1':['stable'],'event2':['event1'],
            'frequency1':['stable'],'frequency2':['frequency1'],'joint':['event1','frequency1']}[variant]
        comparisons={}
        source_comparisons={}
        for reference in references:
            comparison=response_metrics(response,response_sets[reference],basis)
            comparisons[reference]=comparison
            diagnostic=source_diagnostics(variant+'_vs_'+reference,source['source'][source_indices],
                source_sets[reference]['source'][source_indices],basis)
            source_comparisons[reference]=diagnostic
            for column_index,column in enumerate(['baseline','join1','join2']):
                checks.append(check('Source1percent:'+variant+':'+reference+':'+column,
                    np.max(np.array(diagnostic['relative_to_components'])[:,column_index]),.01))
            for metric in ['radiation_relative','gas_peak_relative','gas_late_relative','gas_endpoint_relative']:
                checks.extend(check('Sensitivity1percent:'+variant+':'+reference+':'+metric+':'+column,value,.01)
                    for column,value in zip(['baseline','join1','join2'],comparison[metric]))
        checks.extend(check('Response:'+variant+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+variant,metrics['unresolved_energy_number_defect'],1e-10))
        checks.append(dict(name='Unchanged DC/BR gas:'+variant,passed=np.array_equal(solution['gas'][:,6:],original_response['gas'][:,6:])))
        parts=np.stack([solution['gas'][-1,offset:offset+3] for offset in [3,6,9]])
        results[variant]=dict(event_order=specification(args.upper,variant)[0],frequency_panel_order=specification(args.upper,variant)[1],
            comparisons=comparisons,source_comparisons=source_comparisons,
            versus_legacy=response_metrics(response,original_response,basis),
            gas_endpoint_components=parts.tolist(),endpoint_cancellation_factor=(abs(parts).sum(axis=0)/np.maximum(abs(solution['gas'][-1,:3]),1e-300)).tolist(),
            response_errors=errors)
        source_sets[variant],response_sets[variant]=source,response
        print(json.dumps(dict(model=args.model,upper=args.upper,variant=variant,seconds=time.monotonic()-started)),flush=True)
    refinement={}
    for label_name,levels in [('event',['stable','event1','event2']),('frequency',['stable','frequency1','frequency2'])]:
        first=response_sets[levels[1]]['gas'][:,:3]-response_sets[levels[0]]['gas'][:,:3]
        second=response_sets[levels[2]]['gas'][:,:3]-response_sets[levels[1]]['gas'][:,:3]
        refinement[label_name]=dict(endpoint_difference_ratio=(abs(second[-1])/np.maximum(abs(first[-1]),1e-300)).tolist(),
            peak_difference_ratio=(abs(second).max(axis=0)/np.maximum(abs(first).max(axis=0),1e-300)).tolist(),
            signed_endpoint_differences=[first[-1].tolist(),second[-1].tolist()])
    interaction=response_sets['joint']['gas'][:,:3]-response_sets['event1']['gas'][:,:3]-response_sets['frequency1']['gas'][:,:3]+response_sets['stable']['gas'][:,:3]
    peak=np.maximum(abs(response_sets['stable']['gas'][:,:3]).max(axis=0),1e-300)
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,columns=['baseline','join1','join2'],variants=results,
        legacy_control=dict(comparison=control_comparison,response_errors=control_errors),
        refinement=refinement,interaction_endpoint=interaction[-1].tolist(),interaction_peak_relative=(abs(interaction).max(axis=0)/peak).tolist(),
        original_failed_checks=[row for row in prior_status['checks'] if not row['passed']],
        frequency_nodes=5265,inner_steps=40960,response_steps=2048,source_knots=138,
        changed_source_sites=16,new_inner_steps=0,initial_state_tuned=False,inner_coefficients_resampled=False,
        full_recoil_evaluations=0,seconds=time.monotonic()-started),__file__,inputs)


if __name__=='__main__':
    main()
