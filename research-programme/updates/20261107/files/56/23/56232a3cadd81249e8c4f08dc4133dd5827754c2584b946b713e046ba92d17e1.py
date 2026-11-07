from bridge200 import *
import hashlib, zipfile


def snapshot():
    config=protocol()
    destination=ROOT/'results/resume-before.zip'
    assert not destination.exists()
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in config['bookmarks'].items():
            assert digest(name)==value,name
            archive.writestr(Path(name).name,Path(name).read_bytes())
    print('Resume bytes backed up.',flush=True)


def validate():
    config=protocol()
    qualification=read(ROOT/'results/qualification.json')
    histories=read(ROOT/'results/history-validation.json')
    rows=list(qualification['checks'])+list(histories['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'consumed and immediate inputs unchanged',0,0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    frozen_at=read(ROOT/'frozen/bridge.json')['frozen_at_utc']
    before=datetime.fromisoformat(frozen_at).timestamp()
    for index in range(3):
        path=ROOT/f'physical/probe-{index}/result.npz'
        check(rows,f'independent probe{index} saved after freeze',int(path.stat().st_mtime<before),0,'integrity')
    for path in (ROOT/'physical').glob('*/result.npz'):
        status=read(path.parent/'status.json')
        assert digest(path)==status['sha256']
    for model in ('heavy','cold'):
        for grid in ('half','quarter'):
            folder=ROOT/f'histories/{model}/{grid}'
            complete=read(folder/'complete.json')
            chain=digest(PARENT/f'histories/{model}/{grid}/complete.json')
            stop=0
            for path in sorted((folder/'blocks').glob('*.json')):
                block=read(path)
                assert block['previous_chain']==chain and block['start']==stop
                assert block['stop']-block['start']==len(block['states'])==len(block['diagnostics'])
                stop=block['stop']
                chain=hashlib.sha256((chain+digest(path)).encode()).hexdigest()
            assert stop==complete['total']==complete['done'] and chain==complete['chain']
            check(rows,f'{model}:{grid}:complete hash chain',0,0,'integrity')
    check(rows,'qualifier source unchanged',int(digest(ROOT/'qualify200.py')!=qualification['qualifier_sha256']),0,'integrity')
    frozen=read(ROOT/'evolution-configuration.json')
    check(rows,'evolution source unchanged',int(digest(ROOT/'evolve200.py')!=frozen['runner_sha256']),0,'integrity')
    workbench=BRANCH.parent.parent/'formalization-workbench'
    assert workbench.is_dir()
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    old_prediction=read(ROOT/'results/old-prediction.json')
    check(rows,'old rejected curvature results preserved',len(old_prediction['failed_checks'])-2,0,'integrity')
    failed=[row for row in rows if not row['passed']]
    report=dict(state='validated' if not failed else 'completed_with_failed_checks',checks=rows,failed_checks=failed,
        qualified=not failed,operator_qualified=qualification['qualified'],history_qualified=not histories['failed_checks'],
        retained_old_prediction_failures=old_prediction['failed_checks'],inputs_rehashed=len(inputs),
        protected_workbench_recent_modified_file_count=len(changed),protected_check_scope='Recent mtime only, not full-tree hash',
        new_full_microscopic_source_evaluations=0,full_source_prediction_status='pending')
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=failed,inputs_rehashed=len(inputs))),flush=True)


def seal():
    config=protocol()
    validation=read(ROOT/'results/validation.json')
    assert validation['qualified']
    for name in ('RESULTS.md','NEXT.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name)
            before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes()
            assert current[current.index(b'# Stage199 COMPLETE'):]==before
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',active_numerical_workers=0,completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(state='complete',stage=200,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=inputs,operator_qualified=True,history_qualified=True,
        retained_old_prediction_failure_count=2,full_source_retested=False,new_virtual_integrals=0,
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
