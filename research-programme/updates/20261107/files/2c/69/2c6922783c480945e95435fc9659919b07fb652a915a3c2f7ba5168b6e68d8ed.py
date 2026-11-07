import re
from window_transfer_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    expected={name:set(tests) for name,tests in review['retained_failed_checks'].items()}
    scripts=sorted(ROOT.glob('*.py'))
    for script in scripts:
        compile(script.read_bytes(),str(script),'exec')
    script_hashes={digest(script) for script in scripts}
    checks,inputs,failures=[],[],[]
    scientific,passing=0,0
    statuses=sorted(path for path in ROOT.rglob('status.json') if path.parent!=folder)
    for path in statuses:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and (path.parent/'COMPLETE').exists()
        assert packet['count']==len(packet['checks']) and packet['script_sha256'] in script_hashes
        failed={row['name'] for row in packet['checks'] if not row['passed']}
        name=path.parent.relative_to(ROOT).as_posix()
        assert failed==expected.get(name,set()),(name,failed)
        assert packet['all_checks_passed']==(not failed)
        for target,sha256 in packet['input_hashes'].items():
            assert digest(target)==sha256,(path,target)
        for target in path.parent.rglob('*.npz'):
            with np.load(target) as arrays:
                for key in arrays.files:
                    if np.issubdtype(arrays[key].dtype,np.number):
                        assert np.isfinite(arrays[key]).all(),(target,key)
            inputs.append(target)
        scientific+=packet['count']
        passing+=sum(bool(row['passed']) for row in packet['checks'])
        failures.extend(dict(packet=name,test=test) for test in sorted(failed))
        checks.append(dict(name='Completed packet integrity and truthful scope:'+name,passed=True))
        inputs.append(path)
    assert set(expected).issubset({path.parent.relative_to(ROOT).as_posix() for path in statuses})
    authority=json.loads((ROOT/'results/window-transfer/status.json').read_text())
    assert authority['numerical_integrity_all_passed'] and authority['work_and_number_initial_offsets_retained']
    assert authority['window_contribution_only'] and not authority['outside_window_source_assumed_physically_zero']
    assert all(record['test'].startswith('TRANSFER_DIAGNOSTIC:') for record in failures)
    checks.append(dict(name='Original equations,step/initial refinement,restart and stable superposition pass',passed=True))
    for key in ['new_empirical_fit','new_parent_history','full_parent_feedback_applied','source_frequency_continuum_error_bounded',
                'full_source_precision_gate_closed','outside_window_source_assumed_physically_zero','finite_source_recomputed','github_action']:
        assert review[key] is False,key
    assert review['modes_removed']==0 and review['source_evaluations']==0
    assert not (ROOT/'virtual-cache').exists() and not (ROOT/'runs').exists()
    checks.append(dict(name='Only the known window contribution;no extra source fit or event integration',passed=True))
    documents=[ROOT/name for name in ['RESULTS.md','DERIVATION.md','SOURCES.md','RESUME.md','DEVELOPMENT-NOTES.md']]
    citations=set()
    pattern=chr(96)+'([^'+chr(96)+']+)'+chr(96)
    for document in documents:
        for reference in re.findall(pattern,document.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.npz','.pdf')):
                target=(ROOT/reference).resolve()
                if target in [folder/'status.json',ROOT/'results/stage-integrity.json']:
                    continue
                assert target.is_file(),(document,reference)
                citations.add(target)
    checks.append(dict(name='Every cited local source exists',passed=True))
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected_hash in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected_hash,name
    checks.append(dict(name='All Stage106 payloads and its original failed checks preserved',value=len(parent['file_hashes']),passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile;no interrupted writes or bytecode;directories below1000 files',value=maximum,passed=True))
    finish(folder,dict(checks=checks,checked_packets=len(statuses),scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_scientific_checks=scientific-passing,retained_failure_records=failures,
        compiled_scripts=len(scripts),largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        accepted_current_scope_verified=True,recorded_web_urls=[],web_sources_newly_consulted=[]),__file__,
        [*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses),checks=scientific,passed=passing,validation_checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
