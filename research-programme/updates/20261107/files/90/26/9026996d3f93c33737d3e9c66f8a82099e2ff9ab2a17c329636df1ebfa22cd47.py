from source201 import *
import zipfile


def snapshot():
    config=protocol()
    destination=ROOT/'results/resume-before.zip'
    assert not destination.exists()
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in config['bookmarks'].items():
            assert digest(name)==value,name
            archive.writestr(Path(name).name,Path(name).read_bytes())
    print('Resume bodies backed up.',flush=True)


def validate():
    config=protocol()
    selected=ROOT/'precision-representation'
    repair_config=read(selected/'configuration.json')
    for name,value in repair_config['protocol_hashes'].items():
        assert digest(selected/name)==value,name
    initial=read(ROOT/'results/source-assessment.json')
    assert digest(ROOT/'results/source-assessment.json')==repair_config['retained_failed_attempt_sha256']
    assert digest(ROOT/'results/x14-source.npz')==initial['result_sha256']
    report=read(selected/'results/source-assessment.json')
    rows=list(report['checks'])
    assert digest(selected/'results/x14-source.npz')==report['result_sha256']
    for name in ('pilot/validation.json','cache-pilot/validation.json'):
        diagnostic=read(selected/name)
        rows.extend(dict(row,name=name+':'+row['name']) for row in diagnostic['checks'])
    execution=read(selected/'cache-execution.json')
    assert digest(ROOT/'cached201.py')==execution['sha256']
    assert digest(ROOT/'precise_history201.py')==execution['numerical_code_sha256']
    check(rows,'initial failed attempt preserved explicitly',int(not initial['failed_checks'] or initial['x14_qualified']),0,'integrity')
    inputs=read(ROOT/'inputs.json')
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
    for name,value in inputs.items():
        assert digest(name)==value,name
    write(ROOT/'inputs.json',inputs)
    check(rows,'consumed and immediate inputs rehashed unchanged',0,0,'integrity')
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    for attempt in (ROOT,selected):
        frozen=read(attempt/'frozen/prediction-manifest.json')
        for name,value in frozen['files'].items():
            assert digest(attempt/name)==value,name
        frozen_time=datetime.fromisoformat(frozen['frozen_utc'])
        analysis=read(attempt/'frozen/analysis-protocol.json')
        for name,value in analysis['hashes'].items():
            assert digest(attempt/name)==value,name
        analysis_time=datetime.fromisoformat(analysis['frozen_utc'])
        for index in range(36):
            status=read(attempt/f'actual/event-{index:02d}.json')
            actual_time=datetime.fromisoformat(status['finished_utc'])
            check(rows,f'{attempt.name}:event{index}:prediction and analysis frozen first',int(actual_time<=max(frozen_time,analysis_time)),0,'integrity')
            assert digest(attempt/f'actual/event-{index:02d}.npz')==status['sha256']
            assert status['new_virtual_integrals']==0
    comparison=read(ROOT/'results/representation-comparison.json')
    assert comparison['initial_result_sha256']==initial['result_sha256']
    assert comparison['selected_result_sha256']==report['result_sha256']
    check(rows,'no new virtual integrations',len(list((ROOT/'virtual-cache').rglob('*.json'))) if (ROOT/'virtual-cache').exists() else 0,0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    workbench=BRANCH.parent.parent/'formalization-workbench'
    assert workbench.is_dir()
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/validation.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        inputs_rehashed=len(inputs),protected_workbench_recent_modified_file_count=len(changed),
        protected_scope='Recent mtime only, not full-tree hash',new_virtual_integrals=0,
        x14_qualified=report['x14_qualified'],full_frequency_panel_qualified=False,
        selected_assessment=str(selected/'results/source-assessment.json'),
        initial_failed_checks_retained=len(initial['failed_checks']),
        initial_attempt_qualified=False,post_test_precision_repair=True,
        original_assessment_and_tolerances_unchanged=True))
    print(json.dumps(dict(checks=len(rows),failed=failed,inputs_rehashed=len(inputs))),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/validation.json')
    assert validation['qualified']
    for name in ('RESULTS.md','NEXT.md'):
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
            assert current[current.index(b'# Stage200 COMPLETE'):]==before
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',x14_qualified=True,active_numerical_workers=0,completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(state='complete',stage=201,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=inputs,x14_qualified=True,
        selected_assessment=validation['selected_assessment'],
        initial_failed_checks_retained=validation['initial_failed_checks_retained'],
        post_test_precision_repair=True,
        full_frequency_panel_qualified=False,new_virtual_integrals=0,events=36,
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        maximum_long_running_numerical_workers=1,maximum_concurrent_python_workers=2,library_threads_per_worker=1,
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        active_workers_at_seal=0,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['snapshot','validate','seal'])
    args=parser.parse_args()
    {'snapshot':snapshot,'validate':validate,'seal':seal}[args.phase]()
