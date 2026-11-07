from source_pair_common import *
from evaluate_source_probes import sources,response_metrics,source_diagnostics
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
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    owner=refined_owner(args.model)
    inner_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    inner=read_npz(inner_path)
    cache_path=owner/'results'/f'feedback-m{int(args.upper*1000)}-n40960/source-cache.npz'
    cache=read_npz(cache_path)
    free_free=FreeFree(background,cache['frequency'])
    operator_path=ROOT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    operators=read_npz(operator_path)
    replay_path=ROOT/'results'/f'replay-{args.model}-balanced/prediction.npz'
    replay=read_npz(replay_path)
    assert local_packet(replay_path.parent)['all_checks_passed']
    parent_folder=PARENT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    reference_path=parent_folder/'balanced-direct-response.npz'
    template_path=parent_folder/'balanced-direct-source.npz'
    reference=read_npz(reference_path)
    template=read_npz(template_path)
    assert len(template['coordinate'])==139
    indices=np.searchsorted(template['coordinate'],replay['coordinate'])
    assert np.array_equal(template['coordinate'][indices],replay['coordinate'])
    untouched=np.ones(139,dtype=bool)
    untouched[indices]=False
    prediction=dict(inner)
    for key in ['coordinate','defect','profiles','gas']:
        prediction[key]=replay[key]
    inputs=[inner_path,cache_path,operator_path,operator_path.parent/'status.json',replay_path,replay_path.parent/'status.json',
        reference_path,template_path,parent_folder/'status.json',*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants]
    checks,variants=[],{}
    source_sets,response_sets={},{}
    for label,operator_key in [('physical','physical'),('discrete','source')]:
        events=dict(frequency=operators['frequency'],adjoint=operators[operator_key])
        fresh,group,source_errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
        checks.extend(dict(row,name='Source:'+label+':'+row['name']) for row in group)
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
        np.savez_compressed(folder/(label+'-response.npz'),**{key:value for key,value in response.items() if key!='photon'},
            photon_final=solution['photon'][-1],integration_steps=2048)
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        checks.append(check('Unresolved moments:'+label,metrics['unresolved_energy_number_defect'],1e-10))
        comparator=reference if label=='physical' else response_sets['physical']
        source_reference=template if label=='physical' else source_sets['physical']
        comparison=response_metrics(response,comparator,basis)
        for metric in ['gas_peak_relative','gas_late_relative','gas_endpoint_relative','radiation_relative']:
            checks.extend(check('Sensitivity1percent:'+label+':'+metric+':'+column,value,.01)
                for column,value in zip(['baseline','join1','join2'],comparison[metric]))
        if label=='discrete':
            checks.append(dict(name='Only Compton source operator changed',passed=np.array_equal(candidate['source'][:,1:],source_sets['physical']['source'][:,1:])))
        diagnostics=source_diagnostics(label,candidate['source'][indices],source_reference['source'][indices],basis)
        variants[label]=dict(reference='stage129-balanced-direct' if label=='physical' else 'sourcepair-physical',
            comparison=comparison,versus_stage129=response_metrics(response,reference,basis),
            source_errors=source_errors,response_errors=errors,diagnostic=diagnostics)
        source_sets[label],response_sets[label]=candidate,response
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,variants=variants,
        response_steps=2048,evolution_frequency_nodes=5265,source_knots=139,local_splice_only=True,
        later_state_carried=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,failures=[row['name'] for row in checks if not row['passed']],
        comparisons={key:value['comparison'] for key,value in variants.items()})),flush=True)


if __name__=='__main__':
    main()
