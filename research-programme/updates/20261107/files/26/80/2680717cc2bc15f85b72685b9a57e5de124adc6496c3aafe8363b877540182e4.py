from source_pair_common import *
from fractions import Fraction


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
    parent=json.loads(parent_path.read_text())
    assert hashed(parent_path)==PARENT_SEAL
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks.append(dict(name='All immediate parent payloads unchanged',passed=True))
    for ratio in [Fraction(7,6),Fraction(3,5),Fraction(11,4)]:
        for rate in [Fraction(2,7),Fraction(5,3)]:
            forward=rate/2
            inverse=rate/(2*ratio**3)
            eigen=forward*(1-1/ratio)+inverse*(1-ratio)
            moment=rate*(1-1/ratio-1/ratio**2+1/ratio**3)
            assert eigen==moment/2
            assert inverse*ratio**2==rate/(2*ratio)
            assert forward/ratio**2==rate/(2*ratio**2)
            assert eigen-forward-inverse==-rate*(1/ratio+1/ratio**2)/2
    checks.append(dict(name='Exact rational full adjoint coefficient identity',passed=True))
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    assert len(packets)==14
    failures={}
    count=passed=0
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['script_sha256']==hashed(ROOT/({'balanced-coefficients':'build_source_pairing.py','finite-adjoint':'test_finite_adjoint.py'}.get(path.parent.name,
            'replay_source_pairing.py' if path.parent.name.startswith('replay-') else 'compare_weak_actions.py' if path.parent.name.startswith('weak-') else 'attribute_shape_error.py' if path.parent.name.startswith('shape-error-') else 'evaluate_source_pairing.py')))
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Sensitivity1percent:','Difference-response:')) or (name.startswith('Response:') and name.endswith(':gas')) for name in bad),bad
        assert packet['count']==len(packet['checks']) and packet['all_checks_passed']==(not bad)
        count+=packet['count']
        passed+=sum(row['passed'] for row in packet['checks'])
        if bad:
            failures[path.parent.name]=bad
        for name,sha in packet['input_hashes'].items():
            assert hashed(name)==sha,name
        for archive in path.parent.glob('*.npz'):
            values=read_npz(archive)
            assert all(np.isfinite(value).all() for value in values.values() if value.dtype.kind not in ['U','S'])
            inputs.append(archive)
        inputs.append(path)
        checks.append(dict(name='Finite sourced packet:'+path.parent.name,passed=True))
    assert count==summary['scientific_checks'] and passed==summary['passing_scientific_checks']
    assert failures==summary['failed_by_packet']
    raw=read_npz(PARENT/'results/coefficients/bank.npz')
    bank=read_npz(ROOT/'results/balanced-coefficients/bank.npz')
    offsets,spacing=raw['offsets'],float(raw['spacing'])
    center=int(np.flatnonzero(offsets==0)[0])
    ratios=np.exp(offsets[center+1:]*spacing)
    for epoch in range(33):
        forward=(raw['low'][epoch,center+1:]+ratios**3*raw['low'][epoch,:center][::-1])/2
        backward=(raw['low'][epoch,:center][::-1]+ratios**-3*raw['low'][epoch,center+1:])/2
        eigen=np.sum(forward*(-np.expm1(-np.log(ratios)))+backward*(1-ratios))
        scale=raw['eigenvalue'][epoch]/eigen
        assert np.max(abs(bank['low'][epoch,center+1:]-scale*forward))/max(np.max(abs(scale*forward)),1e-300)<1e-11
        assert np.all(bank['low'][epoch,np.arange(len(offsets))!=center]>=0)
        assert abs(np.sum(bank['low'][epoch]))<1e-12
    checks.append(dict(name='Independent source-rate normalization reconstruction',passed=True))
    for epoch,event_path in enumerate(event_paths()):
        event=read_npz(event_path)
        inverse=1/event['ratios']
        lower=np.floor(np.log(event['ratios'])/spacing)
        first=np.exp(-lower*spacing)
        second=np.exp(-(lower+1)*spacing)
        variance=(inverse-second)*(first-inverse)
        predicted=np.sum(event['rates']*variance*(first+second+inverse-1))/2
        deposited=source_symbol(offsets*spacing,raw['low'][epoch],np.array([1.]))[0]
        physical=np.sum(event['rates']*(event['ratios']-1)**2*(event['ratios']+1)/event['ratios']**3)/2
        assert abs((deposited-physical)-predicted)/physical<1e-9
    checks.append(dict(name='Exact deposition variance source-eigenvalue bias',passed=True))
    restart_count=0
    for model in ['heavy','cold']:
        replay_folder=ROOT/'results'/f'replay-{model}-balanced'
        fingerprint=json.loads((replay_folder/'INPUTS.json').read_text())
        import hashlib
        fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
        for name,sha in fingerprint.items():
            assert hashed(name)==sha,name
        for record_path in sorted((replay_folder/'checkpoints').glob('restart-*.json')):
            record=json.loads(record_path.read_text())
            assert record['fingerprint_sha256']==fingerprint_hash
            assert hashed(record_path.parent/record['archive'])==record['archive_sha256']
            restart_count+=1
        replay=read_npz(replay_folder/'prediction.npz')
        parent_replay=read_npz(PARENT/'results'/f'replay-{model}-balanced/prediction.npz')
        for key in ['frequency','coordinate','saved_step_indices','outer_slope','lower_target','profiles','gas']:
            assert np.array_equal(replay[key],parent_replay[key]),key
        control=read_npz(PARENT/'results'/f'replay-{model}-control/prediction.npz')
        original=read_npz(BRANCH/'initial-source-response-sites-20261014/results'/f'replay-{model}-s00000/prediction.npz')
        assert np.array_equal(control['defect'],original['defect'])
    assert restart_count==16
    checks.append(dict(name='Sixteen restart hashes and unchanged drivers;inherited bitwise controls',passed=True))
    for model in ['heavy','cold']:
        for label in ['20','40']:
            candidate_folder=ROOT/'results'/f'feedback-{model}-m{label}'
            original=read_npz(PARENT/'results'/f'feedback-{model}-m{label}/balanced-direct-source.npz')
            physical=read_npz(candidate_folder/'physical-source.npz')
            discrete=read_npz(candidate_folder/'discrete-source.npz')
            replay=read_npz(ROOT/'results'/f'replay-{model}-balanced/prediction.npz')
            indices=np.searchsorted(original['coordinate'],replay['coordinate'])
            mask=np.ones(len(original['coordinate']),dtype=bool)
            mask[indices]=False
            for current in [physical,discrete]:
                assert np.array_equal(current['source'][mask],original['source'][mask])
                assert np.array_equal(current['coordinate'],original['coordinate'])
            assert np.array_equal(physical['source'][:,1:],discrete['source'][:,1:])
    checks.append(dict(name='Only Compton operator changes at fixed state;late splice preserved',passed=True))
    for path in (ROOT/'results').glob('shape-error-*/forcing.npz'):
        forcing=read_npz(path)
        scale=max(float(np.max(abs(forcing['difference']))),1e-300)
        assert np.max(abs(forcing['difference']-forcing['shape']-forcing['removed']))/scale<1e-14
        assert not np.count_nonzero(forcing['difference'][:,1:])
    checks.append(dict(name='Difference-forcing decomposition and Compton-only support',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for unused,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir()
    changed=[path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not changed
    checks.append(dict(name='Scripts compile;no cache;folder bounds;protected modification scan zero',passed=True))
    consumed={str(path):sha for path,sha in hashes.items() if not path.is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=True,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,retained_failure_names=failures,compiled_scripts=len(scripts),
        rehashed_prior_files=len(consumed),consumed_and_immediate_rehashed=consumed,
        restart_files_verified=restart_count,independent_sparse_steps_recomputed=0,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(validation_checks=len(checks),science=count,passed=passed,failed=count-passed,prior_rehashed=len(consumed))),flush=True)


if __name__=='__main__':
    main()
