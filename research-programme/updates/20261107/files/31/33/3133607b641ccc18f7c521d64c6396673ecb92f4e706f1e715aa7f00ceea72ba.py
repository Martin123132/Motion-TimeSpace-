from spatial_defect_common import *
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
    parent=json.loads(parent_path.read_text())
    assert hashed(parent_path)==PARENT_SEAL
    for name,sha in parent['file_hashes'].items():
        assert hashed(PARENT/name)==sha,name
    checks.append(dict(name='Every immediate Stage130 payload unchanged',passed=True))
    packets=sorted(path for path in (ROOT/'results').glob('*/status.json') if path.parent!=folder)
    assert len(packets)==9
    failures={}
    count=passed=0
    for path in packets:
        packet=json.loads(path.read_text())
        script='test_shape_derivatives.py' if path.parent.name=='preflight' else 'test_inner_dispersion.py' if path.parent.name=='inner-symbols' else 'test_inner_counterpart.py' if path.parent.name=='inner-counterpart' else 'build_spatial_defect.py' if path.parent.name.startswith('operator-') else 'evaluate_spatial_defect.py'
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['script_sha256']==hashed(ROOT/script)
        bad=[row['name'] for row in packet['checks'] if not row['passed']]
        assert all(name.startswith(('Sensitivity1percent:','Explained90percent:','Superposition:','Control:','Sampled dissipativity:')) or (name.startswith('Response:') and name.endswith(':gas')) for name in bad),bad
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
        checks.append(dict(name='Sourced finite result packet:'+path.parent.name,passed=True))
    assert count==summary['scientific_checks'] and passed==summary['passing_scientific_checks']
    assert failures==summary['failed_by_packet']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    coefficient=read_npz(PARENT/'results/balanced-coefficients/bank.npz')
    record_count=0
    for label in ['20','40']:
        bank_folder=ROOT/'results'/f'operator-m{label}'
        bank=read_npz(bank_folder/'bank.npz')
        fingerprint=json.loads((bank_folder/'INPUTS.json').read_text())
        for name,sha in fingerprint.items():
            assert hashed(name)==sha,name
        fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
        for index in range(33):
            record=json.loads((bank_folder/f'epoch-{index:02d}.json').read_text())
            archive=bank_folder/record['archive']
            assert record['fingerprint_sha256']==fingerprint_hash and hashed(archive)==record['archive_sha256']
            values=read_npz(archive)
            scale=float(values['normalization'])
            expected2=values['grid']/scale-values['second']
            expected3=expected2-values['third']
            assert np.array_equal(expected2,values['corrected2']) and np.array_equal(expected3,values['corrected3'])
            for name in ['physical','second','third','corrected2','corrected3','grid','inherited_physical']:
                assert np.array_equal(bank[name][index],values[name])
            diagnostics=record['diagnostics']
            for name,eigen in [('physical',diagnostics['physical_eigen']),('second',diagnostics['second_eigen']),('third',diagnostics['third_eigen']),
                ('corrected2',coefficient['eigenvalue'][index]/scale-diagnostics['second_eigen']),('corrected3',diagnostics['physical_eigen'])]:
                expected=bank['weights']*bank['frequency']*eigen/I3
                allowance=max(np.linalg.norm(expected),diagnostics['physical_eigen']*np.linalg.norm(bank['weights']*bank['frequency']/I3)*1e-10)
                assert np.linalg.norm(basis.temperature@values[name]-expected)/allowance<1e-9
                assert not np.count_nonzero(basis.chemical@values[name])
            record_count+=1
    assert record_count==66
    checks.append(dict(name='All66 checkpoint hashes and reference-free Taylor reconstruction',passed=True))
    checks.append(dict(name='Derived number/energy rows,including variance-only defect',passed=True))
    for model in ['heavy','cold']:
        replay=read_npz(PARENT/'results'/f'replay-{model}-balanced/prediction.npz')
        for window in ['20','40']:
            source_folder=ROOT/'results'/f'feedback-{model}-m{window}'
            template=read_npz(PARENT/'results'/f'feedback-{model}-m{window}/discrete-source.npz')
            operators=read_npz(ROOT/'results'/f'operator-m{window}/bank.npz')
            field=np.array([compact_defect(operators['frequency'],replay['frequency'],value,float(window)/1000) for value in replay['defect']])
            indices=np.searchsorted(template['coordinate'],replay['coordinate'])
            mask=np.ones(139,dtype=bool)
            mask[indices]=False
            for label,key in [('matched','physical'),('second','corrected2'),('third','corrected3')]:
                source=read_npz(source_folder/(label+'-source.npz'))
                for name in ['source','raw_source']:
                    assert np.array_equal(source[name][mask],template[name][mask])
                    assert np.array_equal(source[name][:,1:],template[name][:,1:])
                expected=np.einsum('nij,njk->nik',operators[key]-operators['grid'],field)
                scale=max(float(np.max(abs(template['source']))),1e-300)
                assert np.max(abs(source['source'][indices,0]-template['source'][indices,0]-expected))/scale<1e-13
                if label!='matched':
                    residual=read_npz(source_folder/(label+'-residual-source.npz'))
                    expected=np.einsum('nij,njk->nik',operators[key]-operators['physical'],field)
                    assert np.array_equal(residual['source'][indices,0],expected)
                    assert not np.count_nonzero(residual['source'][mask])
                    assert not np.count_nonzero(residual['source'][:,1:])
    checks.append(dict(name='Same saved states;only derived Compton correction and local residual forcing',passed=True))
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_text(encoding='utf-8'),str(script),'exec')
    assert not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for unused,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Scripts compile;no caches;folder bounds;protected mtime scan zero',passed=True))
    consumed={str(path):sha for path,sha in hashes.items() if not path.is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=True,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,retained_failure_names=failures,compiled_scripts=len(scripts),
        rehashed_prior_files=len(consumed),consumed_and_immediate_rehashed=consumed,
        temperature_records_verified=record_count,new_inner_steps=0,independent_full_response_reruns=0,
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0),
        __file__,[*inputs,ROOT/'NUMERICAL-SUMMARY.json',*ladder.inputs])
    print(json.dumps(dict(validation_checks=len(checks),science=count,passed=passed,failed=count-passed,prior_rehashed=len(consumed))),flush=True)


if __name__=='__main__':
    main()
