from precision214 import *


def validate():
    config,extension,repair=repair_protocol()
    pilot_report=read(ROOT/'results/api-validation.json')
    node_report=read(REPAIR/'results/assessment.json')
    retained_failures=read(EXT/'results/assessment.json')['failed_checks']
    assert len(retained_failures)==8
    for name,value in pilot_report['verified_api_hashes'].items():
        assert digest(ROOT/name)==value,name
    rows=[dict(row,name='pilot:'+row['name']) for row in pilot_report['checks']]
    rows.extend(dict(row,name='node:'+row['name']) for row in node_report['checks'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'consumed and immediate inputs unchanged',0,0,'integrity')
    for manifest_path,relative_root in ((ROOT/'frozen/replay-manifest.json',ROOT),(EXT/'frozen/manifest.json',None),(REPAIR/'frozen/manifest.json',None)):
        manifest=read(manifest_path)
        for name,value in manifest['files'].items():
            assert digest(relative_root/name if relative_root else name)==value,name
    matrices,unused=repaired_pairs()
    frozen_at=datetime.fromisoformat(read(REPAIR/'frozen/manifest.json')['frozen_at'])
    for row,matrix in zip(extension['events'],matrices):
        event=row['event']
        report=read(ROOT/'results/construction.json') if event==0 else read(EXT/f'events/event-{event:02d}.json')
        assert datetime.fromisoformat(report['finished_at'])<frozen_at
        assert not report['failed_checks']
        assert matrix[0].shape==matrix[1].shape==(6,98,97,2)
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight']
        assert digest(row['loop_path'])==row['loop_sha256']
        loop=read(row['loop_path'])
        assert loop['finite'] and loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        if event:
            values=packet(EXT/f'events/event-{event:02d}.npz')
            assert float(values['theta'])==row['theta'] and float(values['weight'])==weight
    check(rows,'all36 event matrices authenticated',len(matrices)-36,0,'integrity')
    check(rows,'only35 missing matrices calculated',len(list((EXT/'events').glob('*.npz')))-35,0,'integrity')
    check(rows,'zero new virtual integrals',read(ROOT/'results/construction.json')['new_virtual_integrals']+sum(read(path)['new_virtual_integrals'] for path in (EXT/'events').glob('*.json')),0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    prior=packet(PARENT/'frozen/history-coefficients.npz')
    for name in ('high','low'):
        check(rows,'identical coefficient values '+name,int(not np.array_equal(coefficients[name],prior[name])),0,'integrity')
    total=packet(REPAIR/'results/operator-node.npz')
    sampled=[]
    with mp.workdps(100):
        for component,row,index,join in ((0,0,0,0),(1,1,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,0,96,1)):
            members=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
            exact=mp.fsum(mp.mpf(float(high[member,row,index,join]))+mp.mpf(float(low[member,row,index,join]))
                         for high,low in matrices for member in members)
            computed=mp.mpf(float(total['high'][component,row,index,join]))+mp.mpf(float(total['low'][component,row,index,join]))
            relative=float(abs(exact-computed)/max(abs(exact),mp.mpf('1e-300')))
            check(rows,f'100digit aggregate:{component}:{row}:{index}:{join}',relative,1e-10,'identity')
            sampled.append(relative)
        prediction=packet(REPAIR/'frozen/node-prediction.npz')
        for grid,component,row,column in ((0,0,0,0),(1,4,97,3),(0,3,42,2),(1,5,81,1)):
            join=column%2
            original_column=4*grid+column
            exact=mp.fsum((mp.mpf(float(total['high'][component,row,index,join]))+mp.mpf(float(total['low'][component,row,index,join])))*
                    (mp.mpf(float(coefficients['high'][active,original_column]))+mp.mpf(float(coefficients['low'][active,original_column])))
                    for index,active in enumerate(ACTIVE))
            computed=mp.mpf(float(prediction['high'][grid,component,row,column]))+mp.mpf(float(prediction['low'][grid,component,row,column]))
            relative=float(abs(exact-computed)/max(abs(exact),mp.mpf('1e-300')))
            check(rows,f'100digit contraction:{grid}:{component}:{row}:{column}',relative,1e-10,'identity')
            sampled.append(relative)
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or unfinished writes',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.tmp')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    integrity_failures=[row for row in failed if row['category']!='representation']
    assert not integrity_failures,integrity_failures
    report=dict(stage=214,checks=rows,failed_checks=failed,integrity_passed=True,
                pilot_qualified=pilot_report['qualified'],full_node_qualified=node_report['qualified'],
                inputs_rehashed=len(inputs),decimal_sample_max=max(sampled),protected_workbench_recent_modified_file_count=len(changed),
                workbench_guard_scope='recent mtime, not full-tree hash',pilot_assessment_sha256=digest(ROOT/'results/api-validation.json'),
                node_assessment_sha256=digest(REPAIR/'results/assessment.json'),retained_failed_checks=retained_failures,
                retained_failed_assessment_sha256=digest(EXT/'results/assessment.json'),permission_to_propagate=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),pilot_qualified=report['pilot_qualified'],
                full_node_qualified=report['full_node_qualified'],inputs=len(inputs),decimal_sample_max=max(sampled))),flush=True)


def seal():
    config,extension,repair=repair_protocol()
    validation=read(ROOT/'results/validation.json')
    assert validation['integrity_passed']
    assert digest(ROOT/'results/api-validation.json')==validation['pilot_assessment_sha256']
    assert digest(REPAIR/'results/assessment.json')==validation['node_assessment_sha256']
    assert digest(EXT/'results/assessment.json')==validation['retained_failed_assessment_sha256']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            path=Path(name)
            old=archive.read(path.name)
            assert hashlib.sha256(old).hexdigest()==value
            assert path.read_bytes().endswith(old)
            bookmarks.append(dict(path=str(path),previous_sha256=value,current_sha256=digest(path),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',pilot_qualified=validation['pilot_qualified'],
                full_node_qualified=validation['full_node_qualified'],active_numerical_workers=0,completed_at=now(),permission_to_propagate=False,
                authoritative_operator='precision-repair/results/operator-node.npz',retained_failed_checks=len(validation['retained_failed_checks'])))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=214,state='complete',sealed_at=now(),
        pilot_qualified=validation['pilot_qualified'],full_node_qualified=validation['full_node_qualified'],
        frequency=config['event']['frequency'],theta=config['theta'],events=36,active_inputs=97,joins=2,
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        file_hashes=hashes,consumed_and_immediate_rehashed=inputs,
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        all_frequency_operator=False,uniform_temperature_operator=False,permission_to_propagate=False,
        maximum_concurrent_event_workers=1,numerical_threads_per_worker=1,active_workers_at_seal=0,
        protected_workbench_recent_modified_file_count=validation['protected_workbench_recent_modified_file_count'],
        retained_representation_failures=len(validation['retained_failed_checks']),current_failures=len(validation['failed_checks']),
        authoritative_operator='precision-repair/results/operator-node.npz',github_action=False,subagents=False,
        next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(seal=str(destination),sha256=digest(destination),payloads=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args()
    {'validate':validate,'seal':seal}[args.phase]()
