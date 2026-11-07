from cubic_inner_common import *
from evaluate_source_probes import sources,response_metrics
from propagate_matched_feedback import solve_response
from propagate_repaired_feedback import readout
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    operator_path=ROOT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    operators=read_npz(operator_path)
    replay_path=ROOT/'results'/f'replay-{args.model}-cubic/prediction.npz'
    replay=read_npz(replay_path)
    assert local_packet(replay_path.parent)['all_checks_passed']
    parent_folder=PARENT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    template_path=parent_folder/'matched-source.npz'
    reference_path=parent_folder/'matched-response.npz'
    template,reference=map(read_npz,[template_path,reference_path])
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    cache_path=refined_owner(args.model)/'results'/f'feedback-m{int(args.upper*1000)}-n40960/source-cache.npz'
    inner,cache=map(read_npz,[inner_path,cache_path])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    free_free=FreeFree(background,cache['frequency'])
    indices=np.searchsorted(template['coordinate'],replay['coordinate'])
    assert np.array_equal(template['coordinate'][indices],replay['coordinate'])
    assert np.array_equal(operators['coordinate'],replay['coordinate'])
    untouched=np.ones(139,dtype=bool)
    untouched[indices]=False
    prediction=dict(inner)
    for key in ['coordinate','defect','profiles','gas']:
        prediction[key]=replay[key]
    checks,rows,source_sets,response_sets=[],{},{},{}
    for label in ['physical','cubic']:
        events=dict(frequency=operators['frequency'],adjoint=operators[label])
        fresh,source_checks,source_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
        checks.extend(dict(row,name='Source:'+label+':'+row['name']) for row in source_checks)
        candidate={key:value.copy() for key,value in template.items()}
        for key,value in fresh.items():
            if isinstance(value,np.ndarray) and value.ndim>0 and value.shape[0]==33 and key!='coordinate':
                candidate[key][indices]=value
        for key in ['source','raw_source','energy_source','number_source','overlap_source']:
            assert np.array_equal(candidate[key][untouched],template[key][untouched])
        np.savez_compressed(folder/(label+'-source.npz'),**candidate)
        solution,errors=solve_response(args.model,candidate,2048,ladder,emission,background)
        metrics,view=readout(basis,inner,candidate,solution,args.upper)
        response={**solution,**view}
        np.savez_compressed(folder/(label+'-response.npz'),**{name:value for name,value in response.items() if name!='photon'},
            photon_final=solution['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
        comparator=reference if label=='physical' else response_sets['physical']
        comparison=response_metrics(response,comparator,basis)
        rows[label]=dict(comparison=comparison,source_errors=source_errors,response_errors=errors)
        source_sets[label],response_sets[label]=candidate,response
    assert np.array_equal(source_sets['physical']['source'][:,1:],source_sets['cubic']['source'][:,1:])
    checks.append(dict(name='Common state:only Compton differs between cubic and physical sources',passed=True))
    residuals={}
    for label,current_source,old_source,current_response,old_response in [
        ('state-change',source_sets['physical'],template,response_sets['physical'],reference),
        ('discretization',source_sets['cubic'],source_sets['physical'],response_sets['cubic'],response_sets['physical'])]:
        packet=dict(coordinate=template['coordinate'],source=current_source['source']-old_source['source'])
        assert not np.count_nonzero(packet['source'][untouched])
        if label=='discretization':
            assert not np.count_nonzero(packet['source'][:,1:])
        np.savez_compressed(folder/(label+'-source.npz'),**packet)
        residual,errors=solve_response(args.model,packet,2048,ladder,emission,background)
        np.savez_compressed(folder/(label+'-response.npz'),**{name:value for name,value in residual.items() if name!='photon'},
            photon_final=residual['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        gas=residual['gas'][:,:3]
        reference_gas=old_response['gas'][:,:3]
        peak=np.max(abs(gas),axis=0)
        relative_peak=peak/np.maximum(np.max(abs(reference_gas),axis=0),1e-300)
        relative_late=np.max(abs(gas[1536:]),axis=0)/np.maximum(np.max(abs(reference_gas[1536:]),axis=0),1e-300)
        relative_endpoint=abs(gas[-1])/np.maximum(abs(reference_gas[-1]),1e-300)
        discrepancy=np.max(abs(current_response['gas'][:,:3]-reference_gas-gas),axis=0)
        superposition=discrepancy/np.maximum(peak,1e-300)
        for metric,values in [('peak',relative_peak),('late',relative_late),('endpoint',relative_endpoint)]:
            checks.extend(check('Sensitivity1percent:'+label+':'+metric+':'+column,value,.01)
                for column,value in zip(['baseline','join1','join2'],values))
        checks.extend(check('Superposition:'+label+':'+column,value,1e-4)
            for column,value in zip(['baseline','join1','join2'],superposition))
        rows[label]=dict(response_errors=errors,relative_peak=relative_peak.tolist(),relative_late=relative_late.tolist(),
            relative_endpoint=relative_endpoint.tolist(),superposition_relative=superposition.tolist(),gas_endpoint=gas[-1].tolist())
        residuals[label]=residual
    inputs=[operator_path,operator_path.parent/'status.json',replay_path,replay_path.parent/'status.json',template_path,reference_path,
        parent_folder/'status.json',inner_path,cache_path,*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants]
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Sensitivity1percent:','Superposition:','Response:')))
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,variants=rows,response_steps=2048,
        frequency_nodes=5265,inner_steps=640,local_splice_only=True,source_knots=139,
        later_state_carried=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,seconds=time.monotonic()-started,
        endpoints={label:rows[label]['relative_endpoint'] for label in ['state-change','discretization']},
        failures=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
