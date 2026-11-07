from response221 import *


def validate():
    config=protocol();inputs=read(ROOT/'inputs-final.json');rows=[]
    candidate=read(ROOT/'causal-startup/configuration.json')
    assert digest(ROOT/'causal_startup221.py')==candidate['script_sha256']
    assert digest(ROOT/'CAUSAL-STARTUP-DERIVATION.md')==candidate['derivation_sha256']
    assert digest(ROOT/'results/assessment.json')==candidate['original_assessment_sha256']
    adapter=read(ROOT/'readout-output-contract.json')
    assert digest(ROOT/'evolve221.py')==adapter['script_sha256']
    assert digest(ROOT/'response221.py')==adapter['original_runner_sha256']
    for model in MODELS:
        folder=ROOT/'causal-startup'/'left'/model
        left=read(folder/'result.json')
        assert digest(folder/'source.npz')==left['source_sha256']
        assert digest(folder/'coefficients.npz')==left['coefficients_sha256']
        assert not left['failed_checks']
        for name,value in left['inputs'].items():
            assert digest(name)==value,name
            if not Path(name).resolve().is_relative_to(ROOT):
                assert inputs[name]==value,name
        for count in (2048,4096):
            folder=ROOT/'causal-startup'/'responses'/f'{model}-{count}'
            result=read(folder/'result.json')
            assert not result['failed_checks']
            for name,value in result['file_hashes'].items():
                assert digest(folder/name)==value,name
            for name,value in result['inputs'].items():
                assert digest(name)==value,name
                if not Path(name).resolve().is_relative_to(ROOT):
                    assert inputs[name]==value,name
    for relative in ('causal-startup/startup-algebra.json','results/cancellation-budget.json','results/matching-roundoff-diagnosis.json'):
        report=read(ROOT/relative)
        assert not report['failed_checks']
        rows.extend(dict(row,name=relative+':'+row['name']) for row in report['checks'])
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial/temp files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected recent mtime count',len(changed),0,'integrity')
    raw=read(ROOT/'results/assessment.json');candidate_result=read(ROOT/'causal-startup/assessment.json')
    write(ROOT/'results/supplementary-validation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],
        supporting_integrity_passed=all(row['passed'] for row in rows),raw_failures_retained=len(raw['failed_checks']),
        candidate_failures_retained=len(candidate_result['failed_checks']),candidate_qualified=candidate_result['qualified'],
        candidate_external_inputs_already_in_final_manifest=True,local_scripts_covered_by_final_payload=True,protected_recent_mtime_count=len(changed),
        extra_left_source_points=2,original_source_points=128,no_whole_project_success_claim=True))
    print(json.dumps(dict(checks=len(rows),failed=sum(not row['passed'] for row in rows),
        raw_failures_retained=len(raw['failed_checks']),candidate_failures_retained=len(candidate_result['failed_checks']),protected_count=len(changed))),flush=True)


if __name__=='__main__':
    source.modest()
    validate()
