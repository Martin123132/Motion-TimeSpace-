from carry_common import *
from evaluate_carried_feedback import expand_source
from evaluate_source_probes import sources
from propagate_matched_feedback import solve_response
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'attribution-{args.model}-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    feedback=ROOT/'results'/f'feedback-{args.model}-m{int(args.upper*1000)}'
    previous_path=feedback/'previous-expanded-source.npz'
    carried_path=feedback/'physical-source.npz'
    previous,carried=map(read_npz,[previous_path,carried_path])
    reference_response_path=feedback/'continuation-response.npz'
    reference_response=read_npz(reference_response_path)
    prefix_path=PARENT/'results'/f'replay-{args.model}-cubic/prediction.npz'
    prefix=read_npz(prefix_path)
    inner_path=refined_owner(args.model)/'results'/f'inner-{args.model}-n40960/prediction.npz'
    cache_path=refined_owner(args.model)/'results'/f'feedback-m{int(args.upper*1000)}-n40960/source-cache.npz'
    inner,cache=map(read_npz,[inner_path,cache_path])
    operator_path=ROOT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    prefix_operator_path=PARENT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    operators,prefix_operators=map(read_npz,[operator_path,prefix_operator_path])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
    free_free=FreeFree(background,cache['frequency'])
    positions=np.searchsorted(carried['coordinate'],operators['coordinate'][1:])
    unchanged=np.ones(len(carried['coordinate']),dtype=bool)
    unchanged[positions]=False
    checks,rows=[],{}
    inputs=[previous_path,carried_path,reference_response_path,feedback/'status.json',prefix_path,inner_path,cache_path,
        operator_path,prefix_operator_path,*ladder.inputs,*emission.inputs,*free_free.inputs,
        background.parent.source,background.native_constants,ROOT/'ATTRIBUTION.md']
    candidates=dict(previous=previous,carry=carried)
    for label in ['control','reset']:
        replay_path=ROOT/'results'/f'evolution-{args.model}-{label}/prediction.npz'
        replay=read_npz(replay_path)
        prediction=dict(inner)
        for key in ['coordinate','defect','profiles','gas']:
            prediction[key]=np.concatenate([prefix[key],replay[key][1:]])
        events=dict(frequency=operators['frequency'],adjoint=np.concatenate([prefix_operators['physical'],operators['physical'][1:]]))
        fresh,source_checks,errors=sources(basis,ladder,prediction,cache,events,background,emission,free_free,args.upper)
        checks.extend(dict(row,name='Source:'+label+':'+row['name']) for row in source_checks)
        candidate={key:value.copy() for key,value in previous.items()}
        for key,value in fresh.items():
            if isinstance(value,np.ndarray) and value.ndim>0 and value.shape[0]==65 and key!='coordinate':
                candidate[key][positions]=value[33:]
        assert np.array_equal(candidate['source'][unchanged],previous['source'][unchanged])
        np.savez_compressed(folder/(label+'-source.npz'),**candidate)
        candidates[label]=candidate
        inputs.extend([replay_path,replay_path.parent/'status.json'])
    source_sum=np.zeros_like(previous['source'])
    gas_sum=np.zeros_like(reference_response['gas'])
    photon_sum=np.zeros_like(reference_response['photon_final'])
    for label,current,old in [('reference-reconstruction','control','previous'),('operator-update','reset','control'),('carried-memory','carry','reset')]:
        source=candidates[current]['source']-candidates[old]['source']
        source_sum+=source
        assert not np.count_nonzero(source[unchanged])
        packet=dict(coordinate=previous['coordinate'],source=source)
        np.savez_compressed(folder/(label+'-source.npz'),**packet)
        response,errors=solve_response(args.model,packet,2048,ladder,emission,background)
        np.savez_compressed(folder/(label+'-response.npz'),**{key:value for key,value in response.items() if key!='photon'},
            photon_final=response['photon'][-1],integration_steps=2048)
        gas_sum+=response['gas']
        photon_sum+=response['photon'][-1]
        checks.extend(check('Response:'+label+':'+name,value,1. if name=='energy_spectrum' else 1e-7) for name,value in errors.items())
        contribution=response['gas'][:,:3]
        target=reference_response['gas'][:,:3]
        peak=np.max(abs(contribution),axis=0)/np.maximum(np.max(abs(target),axis=0),1e-300)
        endpoint_fraction=contribution[-1]/np.where(abs(target[-1])>1e-300,target[-1],1e-300)
        rows[label]=dict(response_errors=errors,gas_endpoint=contribution[-1].tolist(),
            signed_endpoint_fraction_of_extension=endpoint_fraction.tolist(),peak_fraction_of_extension=peak.tolist())
    source_target=carried['source']-previous['source']
    source_scale=max(float(np.max(abs(source_target))),1e-300)
    checks.append(check('Exact source telescoping',float(np.max(abs(source_sum-source_target)))/source_scale,1e-12))
    gas_scale=np.maximum(np.max(abs(reference_response['gas']),axis=0),1e-300)
    gas_error=np.max(abs(gas_sum-reference_response['gas']),axis=0)/gas_scale
    checks.extend(check('Superposition:attribution:gas:'+str(index),value,1e-4) for index,value in enumerate(gas_error))
    photon_scale=np.maximum(np.linalg.norm(reference_response['photon_final'],axis=0),1e-300)
    photon_error=np.linalg.norm(photon_sum-reference_response['photon_final'],axis=0)/photon_scale
    checks.extend(check('Superposition:attribution:photon:'+str(index),value,1e-4) for index,value in enumerate(photon_error))
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Response:','Superposition:')))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,upper=args.upper,contributions=rows,
        gas_superposition=gas_error.tolist(),photon_superposition=photon_error.tolist(),
        counterfactual_reset_sources_are_not_new_physical_histories=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,upper=args.upper,
        fractions={label:row['signed_endpoint_fraction_of_extension'] for label,row in rows.items()},
        max_gas_superposition=float(np.max(gas_error)),failures=[row['name'] for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
