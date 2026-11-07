from source206 import *


def validate():
    config=protocol();runner.verify_frozen()
    report=read(ROOT/'results/source-assessment.json')
    adapter=read(ROOT/'results/adapter-validation.json')
    rows=list(report['checks'])
    rows.extend(dict(row,name='adapter:'+row['name']) for row in adapter['checks'])
    cache_report=read(ROOT/'results/cache-complete.json')
    cache_config=read(ROOT/'cache-configuration.json')
    assert cache_report['configuration_sha256']==digest(ROOT/'cache-configuration.json')
    check(rows,'all 36 virtual inputs accepted',int(not cache_report['complete'])+abs(cache_report['accepted_inputs']-36),0,'integrity')
    check(rows,'unchanged virtual order and precision',int(cache_config['virtual_order']!=2 or cache_config['precision_dps']!=60),0,'integrity')
    check(rows,'acquisition count matches source configuration',cache_report['new_virtual_integrals']-config['new_virtual_integrals'],0,'integrity')
    for index,entry in enumerate(cache_report['records']):
        record=read(ROOT/f'cache-events/event-{index:02d}.json')
        assert record==entry and record['accepted'] and not record['failed_checks']
        assert digest(record['path'])==record['sha256']
        data=read(record['path'])
        assert data['identity']==cache_config['records'][index]['identity']
        check(rows,f'cache:{index}:finite recorded scalar matches',int(not data['finite'] or not np.isfinite(data['scalar']) or data['scalar']!=record['scalar']),0,'integrity')
        rows.extend(dict(row,name=f'cache:{index}:'+row['name']) for row in record['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():assert digest(name)==value,name
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    assert digest(REFERENCE)==config['reference_sha256']==adapter['reference_sha256']
    assert digest(ROOT/'results/adapter-replay-source.npz')==adapter['replay_sha256']
    check(rows,'all consumed and immediate inputs unchanged',0,0,'integrity')
    check(rows,'saved five-frequency source reused without source evaluations',adapter['physics_evaluations'],0,'integrity')
    expected={'neighbour':[FREQUENCY],'six-frequency':[item['frequency'] for item in config['partial_panel']]}
    for scope,summary in report['scopes'].items():
        assert digest(summary['result_path'])==summary['result_sha256'],scope
        values=packet(summary['result_path'])
        check(rows,scope+':declared frequencies correct',int(not np.array_equal(values['frequencies'],np.array(expected[scope]))),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'scripts compile without bytecode',0,0,'integrity')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    check(rows,'owned virtual cache matches recorded acquisitions',len(list((ROOT/'virtual-cache').rglob('*.json')))-config['new_virtual_integrals'],0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    assert protected.is_dir()
    started=datetime.fromisoformat(config['started_utc']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    expected_bookmarks=config['bookmarks']
    restart_path=ROOT/'results/restart-integrity.json'
    if restart_path.exists():
        restart=read(restart_path)
        assert restart['configuration_sha256']==digest(ROOT/'configuration.json')
        for name,value in restart['immutable_file_hashes'].items():assert digest(ROOT/name)==value,name
        expected_bookmarks={row['path']:row['current_sha256'] for row in restart['bookmarks']}
    for name,value in expected_bookmarks.items():assert digest(name)==value,name
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/validation.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        source_assessment_sha256=digest(ROOT/'results/source-assessment.json'),inputs_rehashed=len(inputs),
        protected_workbench_recent_modified_file_count=len(changed),protected_scope='Recent mtime only, not a full-tree hash',
        partial_panel_frequencies=expected['six-frequency'],full_frequency_panel_qualified=False,
        new_virtual_integrals=config['new_virtual_integrals'],source_phase_new_virtual_integrals=0,frequency_weights_reapplied=False,partial_panel_normalized=False))
    print(json.dumps(dict(checks=len(rows),failed=failed,inputs_rehashed=len(inputs))),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/validation.json')
    assert validation['qualified']
    assert digest(ROOT/'results/source-assessment.json')==validation['source_assessment_sha256']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name);before=archive.read(path.name)
            assert hashlib.sha256(before).hexdigest()==value
            current=path.read_bytes()
            assert current.endswith(before)
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',neighbour_and_six_frequency_qualified=True,
        active_numerical_workers=0,completed_utc=datetime.now(timezone.utc).isoformat()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=206,state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=inputs,neighbour_and_six_frequency_qualified=True,
        partial_panel_frequencies=validation['partial_panel_frequencies'],full_frequency_panel_qualified=False,
        new_events=36,reused_reference_events=180,new_virtual_integrals=config['new_virtual_integrals'],source_phase_new_virtual_integrals=0,frequency_weights_reapplied=False,partial_panel_normalized=False,
        original_bank_changed=False,global_curve_changed=False,histories_changed=False,grids_changed=False,tolerances_changed=False,
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        maximum_long_running_numerical_workers=1,maximum_concurrent_python_workers=1,library_threads_per_worker=1,
        active_workers_at_seal=0,github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()
