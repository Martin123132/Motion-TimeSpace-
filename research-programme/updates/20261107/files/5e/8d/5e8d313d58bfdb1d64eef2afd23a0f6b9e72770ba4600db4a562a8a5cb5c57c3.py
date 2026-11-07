import re
from history_frequency_common import *


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
    anchor=json.loads((ROOT/'results/frequency-sources/status.json').read_text())
    assert anchor['every_source_node_verified'] and anchor['numerical_integrity_all_passed']
    conservative=json.loads((ROOT/'results/frequency-response/status.json').read_text())
    assert conservative['numerical_integrity_all_passed'] and conservative['energy_coordinate_is_invertible']
    assert review['frequency_diagnostic_failures_retained'] is True
    assert digest(PARENT/'results/holdout-sources/source.npz')=='695037a1f7052d32d242457ab1b31b2a69becc544637c0ed77e0f2238eec8c3c'
    assert anchor['central_seed4_unchanged'] and anchor['controls_reused_without_recomputation'] and conservative['central_seed4_unchanged']
    assert all(record['test'].startswith('FREQUENCY_DIFFERENCE:') for record in failures)
    prediction_time=(ROOT/'results/frequency-preflight/COMPLETE').stat().st_mtime
    nodes=list((ROOT/'runs').rglob('nodes/*/*.npz'))
    assert len(nodes)==1512 and all(path.stat().st_mtime>=prediction_time for path in nodes)
    checks.append(dict(name='Frozen acceptance and successful reuse preflight precede every production node',value=len(nodes),passed=True))
    checks.append(dict(name='Both frequency sources and response integrity pass; unchanged seed4 central result and diagnostic misses retained',passed=True))
    for key in ['new_empirical_fit','new_parent_history','full_parent_feedback_applied','new_epoch_precision_gate_closed',
                'source_interpolation_error_bounded','source_frequency_continuum_error_bounded','control_coefficient_fitted','github_action']:
        assert review[key] is False,key
    loops=len(list((ROOT/'virtual-cache').rglob('*.json')))
    assert loops==review['new_virtual_loop_evaluations'] and review['modes_removed']==0
    checks.append(dict(name='All nodes verified;no promoted fit/history/precision or transplanted loop',passed=True))
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
    checks.append(dict(name='All cited local sources exist',passed=True))
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected_hash in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected_hash,name
    checks.append(dict(name='Stage104 payloads unchanged',value=len(parent['file_hashes']),passed=True))
    maximum=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert maximum<1000 and not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.tmp'))
    checks.append(dict(name='Scripts compile;no interrupted writes/bytecode;directories below1000 files',value=maximum,passed=True))
    finish(folder,dict(checks=checks,checked_packets=len(statuses),scientific_checks=scientific,passing_scientific_checks=passing,
        retained_failed_scientific_checks=scientific-passing,retained_failure_records=failures,
        compiled_scripts=len(scripts),largest_direct_file_count=maximum,local_citations=[str(path) for path in sorted(citations)],
        accepted_current_scope_verified=True,recorded_web_urls=[],web_sources_newly_consulted=[]),__file__,
        [*inputs,*scripts,*documents,*citations,ROOT/'ACCURACY-REVIEW.json'])
    print(json.dumps(dict(packets=len(statuses),checks=scientific,passed=passing,validation_checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
