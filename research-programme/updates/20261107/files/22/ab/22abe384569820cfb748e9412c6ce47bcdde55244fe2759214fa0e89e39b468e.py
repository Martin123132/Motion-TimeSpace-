from batch218 import *


def validate():
    config=protocol();assessment=read(ROOT/'results/assessment.json')
    rows=list(assessment['checks']);inputs=read(ROOT/'inputs.json')
    assert assessment['batch_complete'] and assessment['operator_nodes_ready']==[0,1,6]
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'all consumed and immediate input hashes unchanged',0,0,'integrity')
    selected=[row for row in config['events'] if row['frequency_index'] in config['batch_nodes']]
    sample_errors=[]
    for row in selected:
        values,report=verify_event(row)
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight']
        loop=read(row['loop_path'])
        assert digest(row['loop_path'])==row['loop_sha256'] and loop['finite']
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        assert report['new_virtual_integrals']==0 and report['scalar_precision']==60 and report['protected_precision']==80
        assert datetime.fromisoformat(report['replay_frozen_before_comparison'])<=datetime.fromisoformat(report['finished_at'])
    check(rows,'all216 batch matrix events completed',len(list((ROOT/'events').rglob('event-*.json')))-216,0,'integrity')
    check(rows,'no new virtual-cache files',len(list((ROOT/'virtual-cache').rglob('*'))) if (ROOT/'virtual-cache').exists() else 0,0,'integrity')
    catalog=[]
    with mp.workdps(100):
        for index in assessment['operator_nodes_ready']:
            anchors={}
            for label in LABELS:
                path=ROOT/f'results/operator-node-{index}-{label}.npz' if index!=6 else Path(config['reused_upper_node'][label]['path'])
                values=packet(path)
                anchors[label]=dict(path=str(path),sha256=digest(path),theta=config['anchor_thetas'][label])
                if index==6:
                    continue
                events=[verify_event(row)[0] for row in selected if row['frequency_index']==index and row['label']==label]
                for component,row_index,column,join in ((0,0,0,0),(1,2,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,1,96,1)):
                    members=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
                    exact=mp.fsum(mp.mpf(float(event['high'][member,row_index,column,join]))+mp.mpf(float(event['low'][member,row_index,column,join]))
                        for event in events for member in members)
                    stored=mp.mpf(float(values['high'][component,row_index,column,join]))+mp.mpf(float(values['low'][component,row_index,column,join]))
                    relative=float(abs(exact-stored)/max(abs(exact),mp.mpf('1e-300')))
                    sample_errors.append(relative)
                    check(rows,f'100digit node{index}:{label}:{component}:{row_index}:{column}:{join}',relative,1e-10,'identity')
            catalog.append(dict(frequency_index=index,frequency=config['original_panel'][index]['frequency'],
                original_seed_weight=config['original_panel'][index]['seed_weight'],weight_already_included=True,
                anchor_operators=anchors,active_input_indices=prior.ACTIVE,matrix_shape=[6,98,97,2],
                history_replay_qualified=assessment['qualified'] if index!=6 else True))
        for label in LABELS:
            subset=packet(ROOT/f'results/operator-subset-{label}.npz')
            members=[packet(entry['anchor_operators'][label]['path']) for entry in catalog]
            for component,row_index,column,join in ((0,0,0,0),(1,1,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,2,96,1)):
                indices=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
                exact=mp.fsum(mp.mpf(float(member['high'][part,row_index,column,join]))+mp.mpf(float(member['low'][part,row_index,column,join]))
                    for member in members for part in indices)
                stored=mp.mpf(float(subset['high'][component,row_index,column,join]))+mp.mpf(float(subset['low'][component,row_index,column,join]))
                relative=float(abs(exact-stored)/max(abs(exact),mp.mpf('1e-300')))
                sample_errors.append(relative)
                check(rows,f'100digit subset:{label}:{component}:{row_index}:{column}:{join}',relative,1e-10,'identity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or temporary outputs',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/operator-catalog.json',dict(original_panel=config['original_panel'],operator_nodes=catalog,
        pending_nodes=config['pending_nodes'],full_panel_complete=False,qualified=not failed,
        source_history_fraction=config['target_fraction'],basis_path=str(ROOT/'frozen/basis-metric.npz'),
        basis_sha256=digest(ROOT/'frozen/basis-metric.npz'),normalization='original event weights included; no partial-panel rescaling'))
    report=dict(stage=218,checks=rows,failed_checks=failed,qualified=not failed,inputs_rehashed=len(inputs),
        batch_events=216,new_virtual_integrals=0,operator_nodes_ready=[0,1,6],operator_nodes_pending=[2,3,4,5],
        full_seven_node_operator_complete=False,decimal_sample_max=max(sample_errors),
        assessment_sha256=digest(ROOT/'results/assessment.json'),catalog_sha256=digest(ROOT/'results/operator-catalog.json'),
        protected_workbench_recent_mtime_count=len(changed),guard_scope='recent mtime, not full-tree content hash',
        original_bank_changed=False,grids_changed=False,tolerances_changed=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),qualified=not failed,inputs=len(inputs),decimal_sample_max=max(sample_errors))),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/validation.json')
    assert digest(ROOT/'results/assessment.json')==validation['assessment_sha256']
    assert digest(ROOT/'results/operator-catalog.json')==validation['catalog_sha256']
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            before=archive.read(Path(name).name)
            assert hashlib.sha256(before).hexdigest()==value and Path(name).read_bytes().endswith(before)
            bookmarks.append(dict(path=name,previous_sha256=value,current_sha256=digest(name),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='batch_complete',qualified=validation['qualified'],batch_events_complete=216,
        operator_nodes_ready=[0,1,6],operator_nodes_pending=[2,3,4,5],full_panel_complete=False,active_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=218,state='batch_complete',qualified=validation['qualified'],sealed_at=now(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=read(ROOT/'inputs.json'),file_hashes=hashes,batch_events=216,new_virtual_integrals=0,
        operator_nodes_ready=[0,1,6],operator_nodes_pending=[2,3,4,5],full_seven_node_operator_complete=False,
        complete_source_panel_preserved=True,retained_current_failures=len(validation['failed_checks']),
        maximum_concurrent_workers=2,numerical_threads_per_worker=1,active_workers_at_seal=0,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,permission_to_propagate=False,
        github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(sha256=digest(destination),payloads=len(hashes),qualified=validation['qualified'])),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['validate','seal'])
    args=parser.parse_args();{'validate':validate,'seal':seal}[args.phase]()
