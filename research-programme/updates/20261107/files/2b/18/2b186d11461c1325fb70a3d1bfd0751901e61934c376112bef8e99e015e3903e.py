from carry_common import *
from evaluate_carried_feedback import expand_source
import hashlib


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if path not in hashes:
            hashes[path]=digest(path)
        return hashes[path]
    parent_path=PARENT/'results/stage-integrity.json'
    assert hashed(parent_path)==PARENT_SEAL
    parent=json.loads(parent_path.read_text())
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks=[dict(name='All immediate Stage132 payloads unchanged',passed=True)]
    inputs=[]
    count=passed=0
    failures={}
    for name in summary['packet_names']:
        path=ROOT/'results'/name/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        script='build_carry_coefficients.py' if name=='coefficients' else 'test_carried_memory.py' if name=='memory-contract' else 'build_linear_source_cache.py' if name=='linear-source-cache' else 'attribute_carried_source.py' if name.startswith('attribution-') else 'continue_cubic_inner.py' if name.startswith('evolution-') else 'build_carry_weak.py' if name.startswith('weak-') else 'evaluate_carried_feedback.py'
        assert packet['script_sha256']==hashed(ROOT/script)
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(item.startswith(('Sensitivity1percent:','Superposition:')) or (item.startswith('Response:') and item.endswith(':gas')) for item in bad),bad
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not bad)
        count+=packet['count']
        passed+=sum(row['passed'] for row in packet['checks'])
        if bad:
            failures[name]=bad
        for source,sha in packet['input_hashes'].items():
            assert hashed(source)==sha,source
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        checks.append(dict(name='Finite sourced packet:'+name,passed=True))
    assert count==summary['scientific_checks'] and passed==summary['passing_scientific_checks'] and failures==summary['failed_by_packet']
    coefficient=read_npz(ROOT/'results/coefficients/bank.npz')
    coefficient_status=local_packet(ROOT/'results/coefficients')
    previous=read_npz(PARENT/'results/coefficients/bank.npz')
    for index,step in enumerate(SOURCE_STEPS):
        row=coefficient_status['rows'][index]
        assert hashed(row['event_path'])==row['event_sha256']
        event=read_npz(row['event_path'])
        raw,unused_weights,unused_errors=deposit_cubic(event['ratios'],event['rates'],coefficient['offsets'],float(coefficient['spacing']))
        assert np.array_equal(raw,coefficient['raw'][index])
        stencil=pair_cubic(raw,coefficient['offsets'],float(coefficient['spacing']))
        assert np.array_equal(stencil,coefficient['stencil'][index])
        assert symbol_bound(stencil,coefficient['offsets'],float(coefficient['spacing']),float(coefficient['eigenvalue'][index]))==row['bound']
    assert np.array_equal(coefficient['stencil'][0],previous['stencil'][-1])
    checks.append(dict(name='Physical event provenance,cubic construction and shared boundary coefficients',passed=True))
    restart_count=0
    for model in ['heavy','cold']:
        original=read_npz(refined_owner(model)/'results'/f'inner-{model}-n40960/prediction.npz')
        prefix=read_npz(PARENT/'results'/f'replay-{model}-cubic/prediction.npz')
        candidates={}
        for variant in ['control','reset','carry']:
            evolution_folder=ROOT/'results'/f'evolution-{model}-{variant}'
            prediction=read_npz(evolution_folder/'prediction.npz')
            candidates[variant]=prediction
            assert np.array_equal(prediction['saved_step_indices'],SOURCE_STEPS)
            fingerprint=json.loads((evolution_folder/'INPUTS.json').read_text())
            for source,sha in fingerprint.items():
                assert hashed(source)==sha,source
            fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
            records=sorted((evolution_folder/'checkpoints').glob('restart-*.json'))
            assert len(records)==8
            for step,record_path in zip(range(720,1281,80),records):
                record=json.loads(record_path.read_text())
                archive=record_path.parent/record['archive']
                assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
                state=read_npz(archive)
                assert record['completed_step']==step and int(state['completed_step'])==step
                assert state['error'].shape==state['previous_error'].shape==(5265,3)
                assert all(np.isfinite(value).all() for value in state.values())
                assert np.array_equal(state['error'],prediction['defect'][(step-640)//20])
                restart_count+=1
            if variant=='control':
                assert np.array_equal(prediction['defect'][-1],original['defect'][2])
            else:
                assert prediction['budget'].shape==(640,7,3) and np.all(prediction['budget'][:,2]<=0)
                assert np.max(prediction['budget'][:,5:])<1e-8
            if variant=='carry':
                for key in ['coordinate','slope','outer_slope','defect','lower_target']:
                    assert np.array_equal(prediction[key][0],prefix[key][-1])
        for key in ['coordinate','outer_slope','lower_target','profiles','gas']:
            assert np.array_equal(candidates['carry'][key],candidates['reset'][key])
        checks.append(dict(name='Bitwise original control,unbroken corrected prefix and both-level snapshots:'+model,passed=True))
    assert restart_count==48
    weak_count=0
    for window in [20,40]:
        weak_folder=ROOT/'results'/f'weak-m{window}'
        bank=read_npz(weak_folder/'bank.npz')
        prefix_bank=read_npz(PARENT/'results'/f'weak-m{window}/bank.npz')
        fingerprint=json.loads((weak_folder/'INPUTS.json').read_text())
        fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
        for source,sha in fingerprint.items():
            assert hashed(source)==sha,source
        for index in range(33):
            record=json.loads((weak_folder/f'epoch-{index:02d}.json').read_text())
            archive=weak_folder/record['archive']
            assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
            values=read_npz(archive)
            for key in ['physical','cubic']:
                assert np.array_equal(bank[key][index],values[key])
            weak_count+=1
        for key in ['physical','cubic']:
            assert np.array_equal(bank[key][0],prefix_bank[key][-1])
    assert weak_count==66
    checks.append(dict(name='All66 weak checkpoint records and exact endpoint source continuity',passed=True))
    for model in ['heavy','cold']:
        for window in [20,40]:
            feedback_folder=ROOT/'results'/f'feedback-{model}-m{window}'
            physical=read_npz(feedback_folder/'physical-source.npz')
            cubic=read_npz(feedback_folder/'cubic-source.npz')
            prior=read_npz(PARENT/'results'/f'feedback-{model}-m{window}/physical-source.npz')
            reference=expand_source(prior,physical['coordinate'])
            saved=read_npz(feedback_folder/'previous-expanded-source.npz')
            assert np.array_equal(reference['source'],saved['source'])
            assert np.array_equal(physical['source'][:,1:],cubic['source'][:,1:])
            new_coordinates=coefficient['coordinate'][1:]
            new_positions=np.searchsorted(physical['coordinate'],new_coordinates)
            unaffected=np.ones(len(physical['coordinate']),dtype=bool)
            unaffected[new_positions]=False
            for label,current in [('physical',physical),('cubic',cubic)]:
                previous_source=read_npz(PARENT/'results'/f'feedback-{model}-m{window}'/(label+'-source.npz'))
                expanded=expand_source(previous_source,current['coordinate'])
                for key in ['source','raw_source','energy_source','number_source','overlap_source']:
                    assert np.array_equal(current[key][unaffected],expanded[key][unaffected])
            for label,current,old in [('continuation',physical,reference),('discretization',cubic,physical)]:
                packet=read_npz(feedback_folder/(label+'-source.npz'))
                assert np.array_equal(packet['source'],current['source']-old['source'])
                response=read_npz(feedback_folder/(label+'-response.npz'))
                assert len(response['coordinate'])==2049 and int(response['integration_steps'])==2048
    checks.append(dict(name='Continuous two-interval source;unchanged prefix/tail;exact difference forcing',passed=True))
    for model in ['heavy','cold']:
        for window in [20,40]:
            attribution_folder=ROOT/'results'/f'attribution-{model}-m{window}'
            feedback_folder=ROOT/'results'/f'feedback-{model}-m{window}'
            previous_source=read_npz(feedback_folder/'previous-expanded-source.npz')['source']
            control_source=read_npz(attribution_folder/'control-source.npz')['source']
            reset_source=read_npz(attribution_folder/'reset-source.npz')['source']
            carry_source=read_npz(feedback_folder/'physical-source.npz')['source']
            for label,current,old in [('reference-reconstruction',control_source,previous_source),('operator-update',reset_source,control_source),('carried-memory',carry_source,reset_source)]:
                assert np.array_equal(read_npz(attribution_folder/(label+'-source.npz'))['source'],current-old)
    checks.append(dict(name='Independent signed source attribution reconstructed exactly',passed=True))
    prefix_coefficient=read_npz(PARENT/'results/coefficients/bank.npz')
    active=coefficient['offsets']!=0
    all_rates=np.concatenate([prefix_coefficient['stencil'],coefficient['stencil'][1:]])[:,active]
    for window in [20,40]:
        unit=read_npz(ROOT/'results/linear-source-cache'/f'unit-m{window}.npz')
        assembled=read_npz(ROOT/'results/linear-source-cache'/f'assembled-m{window}.npz')
        assert np.array_equal(assembled['adjoint'],np.einsum('tj,jkl->tkl',all_rates,unit['unit_adjoint'],optimize=True))
    checks.append(dict(name='Rate-linear source cache reconstructs all saved matrices',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for unused,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Scripts compile;no caches;folder limits;protected mtime zero',passed=True))
    consumed={str(path):sha for path,sha in hashes.items() if not path.is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=True,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,retained_failure_names=failures,compiled_scripts=len(scripts),
        rehashed_prior_files=len(consumed),consumed_and_immediate_rehashed=consumed,restart_records_verified=restart_count,
        weak_records_verified=weak_count,largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),science=count,passed=passed,failed=count-passed,prior_rehashed=len(consumed))),flush=True)


if __name__=='__main__':
    main()
