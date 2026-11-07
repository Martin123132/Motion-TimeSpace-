from source202 import *


def validate():
    config=protocol();manifest=verify_frozen()
    report=read(ROOT/'results/source-assessment.json')
    rows=list(report['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    check(rows,'all consumed and immediate inputs rehashed unchanged',0,0,'integrity')
    for scope,summary in report['scopes'].items():
        assert digest(summary['result_path'])==summary['result_sha256'],scope
    parent_result=read(REFERENCE/'results/source-assessment.json')
    assert parent_result['x14_qualified'] and not parent_result['failed_checks']
    check(rows,'qualified x14 result reused unchanged',int(digest(REFERENCE/'results/x14-source.npz')!=parent_result['result_sha256']),0,'integrity')
    inherited_failures=read(PARENT/'results/source-assessment.json')['failed_checks']
    check(rows,'initial Stage201 failed attempt still retained',int(len(inherited_failures)!=276),0,'integrity')
    initial=read(ROOT/'preparation-attempt-01/preparation.json')
    check(rows,'initial panel preflight failures retained',int(len(initial['failed_checks'])!=2),0,'integrity')
    archived_config=read(ROOT/'preparation-attempt-01/configuration.json')
    for name,value in archived_config['protocol_hashes'].items():
        assert digest(ROOT/'preparation-attempt-01'/name)==value,name
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'scripts compile without bytecode',0,0,'integrity')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    check(rows,'no local virtual integration cache created',int((ROOT/'virtual-cache').exists()),0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    assert protected.is_dir()
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/validation.json',dict(checks=rows,failed_checks=failed,qualified=not failed,inputs_rehashed=len(inputs),
        source_assessment_sha256=digest(ROOT/'results/source-assessment.json'),retained_preparation_failures=2,
        original_parent_precision_failures_preserved=276,protected_workbench_recent_modified_file_count=len(changed),
        protected_scope='Recent mtime guard only, not full-tree hash',
        partial_panel_frequencies=[14.,FREQUENCY],full_frequency_panel_qualified=False,
        new_virtual_integrals=0,frequency_weights_reapplied=False,partial_panel_normalized=False))
    print(json.dumps(dict(checks=len(rows),failed=failed,inputs_rehashed=len(inputs))),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/validation.json')
    assert validation['qualified']
    assert digest(ROOT/'results/source-assessment.json')==validation['source_assessment_sha256']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes()
            assert current[current.index(b'# Stage201 COMPLETE'):]==before
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',neighbour_and_weighted_pair_qualified=True,
        active_numerical_workers=0,completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=202,state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=inputs,neighbour_and_weighted_pair_qualified=True,
        partial_panel_frequencies=[14.,FREQUENCY],full_frequency_panel_qualified=False,new_events=36,reused_reference_events=36,
        new_virtual_integrals=0,frequency_weights_reapplied=False,partial_panel_normalized=False,
        original_bank_changed=False,global_curve_changed=False,histories_changed=False,grids_changed=False,tolerances_changed=False,
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        maximum_long_running_numerical_workers=1,maximum_concurrent_python_workers=2,library_threads_per_worker=1,
        active_workers_at_seal=0,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()
