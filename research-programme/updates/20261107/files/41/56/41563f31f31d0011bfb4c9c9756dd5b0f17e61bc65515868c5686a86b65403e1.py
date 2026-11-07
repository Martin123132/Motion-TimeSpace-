from cubic_inner_common import *
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
    checks,inputs=[],[]
    parent_path=PARENT/'results/stage-integrity.json'
    assert hashed(parent_path)==PARENT_SEAL
    parent=json.loads(parent_path.read_text())
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks.append(dict(name='Every immediate Stage131 payload unchanged',passed=True))
    count=passed=0
    failures={}
    for name in summary['packet_names']:
        path=ROOT/'results'/name/'status.json'
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        script='build_cubic_bank.py' if name=='coefficients' else 'test_cubic_boundaries.py' if name=='boundary-contract' else 'replay_cubic_inner.py' if name.startswith('replay-') else 'build_cubic_weak.py' if name.startswith('weak-') else 'evaluate_cubic_feedback.py'
        assert packet['script_sha256']==hashed(ROOT/script)
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(item.startswith(('Sensitivity1percent:','Explained90percent:','Superposition:')) or (item.startswith('Response:') and item.endswith(':gas')) for item in bad),bad
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
        checks.append(dict(name='Sourced finite packet:'+name,passed=True))
    assert count==summary['scientific_checks'] and passed==summary['passing_scientific_checks'] and failures==summary['failed_by_packet']
    bank=read_npz(ROOT/'results/coefficients/bank.npz')
    coefficient_status=local_packet(ROOT/'results/coefficients')
    for index in range(33):
        expected=pair_cubic(bank['raw'][index],bank['offsets'],float(bank['spacing']))
        assert np.array_equal(expected,bank['stencil'][index])
        bound=symbol_bound(expected,bank['offsets'],float(bank['spacing']),float(bank['eigenvalue'][index]))
        assert bound==coefficient_status['rows'][index]['bound'] and bound['upper_bound']<0
    checks.append(dict(name='Unscaled paired coefficients and all-band stability bounds reconstructed',passed=True))
    restart_count=0
    for model in ['heavy','cold']:
        reference=read_npz(P130/'results'/f'replay-{model}-balanced/prediction.npz')
        for variant in ['control','cubic']:
            replay_folder=ROOT/'results'/f'replay-{model}-{variant}'
            replay=read_npz(replay_folder/'prediction.npz')
            fingerprint=json.loads((replay_folder/'INPUTS.json').read_text())
            for source,sha in fingerprint.items():
                assert hashed(source)==sha,source
            fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
            records=sorted((replay_folder/'checkpoints').glob('restart-*.json'))
            assert len(records)==8
            for step,record_path in zip(range(80,641,80),records):
                record=json.loads(record_path.read_text())
                archive=record_path.parent/record['archive']
                assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
                restart=read_npz(archive)
                assert record['completed_step']==step and int(restart['completed_step'])==step
                assert all(np.isfinite(value).all() for value in restart.values())
                assert restart['error'].shape==restart['previous_error'].shape==(5265,3)
                assert np.array_equal(restart['error'],replay['defect'][step//20])
                restart_count+=1
            for key in ['frequency','coordinate','outer_slope','lower_target','profiles','gas']:
                assert np.array_equal(replay[key],reference[key]),key
            assert np.array_equal(replay['defect'][0],reference['defect'][0])
            if variant=='control':
                assert np.array_equal(replay['defect'],reference['defect'])
            else:
                assert replay['budget'].shape==(640,7,3)
                assert np.all(replay['budget'][:,2]<=0)
                assert np.max(replay['budget'][:,5:])<1e-8
        checks.append(dict(name='Both-level restart provenance and bitwise control:'+model,passed=True))
    assert restart_count==32
    for model in ['heavy','cold']:
        replay=read_npz(ROOT/'results'/f'replay-{model}-cubic/prediction.npz')
        for window in [20,40]:
            feedback_folder=ROOT/'results'/f'feedback-{model}-m{window}'
            prior=read_npz(PARENT/'results'/f'feedback-{model}-m{window}/matched-source.npz')
            physical=read_npz(feedback_folder/'physical-source.npz')
            cubic=read_npz(feedback_folder/'cubic-source.npz')
            indices=np.searchsorted(prior['coordinate'],replay['coordinate'])
            mask=np.ones(139,dtype=bool)
            mask[indices]=False
            for source in [physical,cubic]:
                for key in ['source','raw_source','energy_source','number_source','overlap_source']:
                    assert np.array_equal(source[key][mask],prior[key][mask])
            assert np.array_equal(physical['source'][:,1:],cubic['source'][:,1:])
            for label,current,old in [('state-change',physical,prior),('discretization',cubic,physical)]:
                packet=read_npz(feedback_folder/(label+'-source.npz'))
                assert np.array_equal(packet['source'],current['source']-old['source'])
                assert not np.count_nonzero(packet['source'][mask])
                response=read_npz(feedback_folder/(label+'-response.npz'))
                assert int(response['integration_steps'])==2048 and len(response['coordinate'])==2049
    checks.append(dict(name='Identical later splice and exact independent difference-forcing packets',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for unused,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Scripts compile;no caches;bounded folders;protected mtime zero',passed=True))
    consumed={str(path):sha for path,sha in hashes.items() if not path.is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=True,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,retained_failure_names=failures,compiled_scripts=len(scripts),
        rehashed_prior_files=len(consumed),consumed_and_immediate_rehashed=consumed,restart_records_verified=restart_count,
        independent_full_response_reruns=0,largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json',ROOT/'PROJECTION-SCOPE.md'])
    print(json.dumps(dict(validation_checks=len(checks),science=count,passed=passed,failed=count-passed,prior_rehashed=len(consumed))),flush=True)


if __name__=='__main__':
    main()
