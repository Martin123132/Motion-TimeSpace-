from batch219 import *


def main():
    config=protocol()
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    destination=ROOT/'partial-saves'/stamp
    rows=[];replays=[];physical=[];hashes={};completed=[];pending=[];catalog=copy.deepcopy(config['reused_catalog'])
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    basis=packet(ROOT/'frozen/basis-metric.npz');factor=linear.cholesky(basis['mass'],lower=True)
    selected=[row for row in config['events'] if row['frequency_index'] in config['batch_nodes']]
    for row in selected:
        path=event_path(row)
        identity=dict(frequency_index=row['frequency_index'],label=row['label'],event=row['event'])
        if not path.with_suffix('.json').exists():
            assert not path.exists(),str(path)
            pending.append(identity)
            continue
        values,report=verify_event(row)
        completed.append(identity)
        rows.extend(dict(entry,name=f'{row["frequency_index"]}:{row["label"]}:{row["event"]}:'+entry['name']) for entry in report['checks'])
        replays.extend(report['replays'])
        for output in (path,path.with_suffix('.json'),path.with_name(path.stem+'-replay.npz')):
            hashes[str(output.relative_to(ROOT))]=digest(output)
    complete_nodes=[index for index in config['batch_nodes'] if sum(row['frequency_index']==index for row in completed)==108]
    for index in complete_nodes:
        node_operators=[];anchors={}
        for label in LABELS:
            packets=[];directs=[];event_sources=[]
            for row in [row for row in selected if row['frequency_index']==index and row['label']==label]:
                values,report=verify_event(row);packets.append((values['high'],values['low']))
                direct=packet(row['source_path']);directs.append((direct['high'],direct['low']))
                replay=packet(event_path(row).with_name(event_path(row).stem+'-replay.npz'));event_sources.append((replay['high'],replay['low']))
            assert len(packets)==36
            total=api.sum_events(packets);node_operators.append(total)
            path=destination/f'operator-node-{index}-{label}.npz'
            save(path,high=total[0],low=total[1],theta=config['anchor_thetas'][label],frequency=config['original_panel'][index]['frequency'])
            anchors[label]=dict(path=str(path),sha256=digest(path),theta=config['anchor_thetas'][label])
            contracted=contract_histories(total,coefficients)
            helpers.compare(f'node{index}:{label}:direct anchor sum',contracted,metrics.primitives(directs),factor,rows,replays)
            helpers.compare(f'node{index}:{label}:contraction order',contracted,metrics.primitives(event_sources),factor,rows,replays)
            local=[];helpers.matrix_identities(dict(high=total[0],low=total[1]),basis,local)
            rows.extend(dict(entry,name=f'node{index}:{label}:'+entry['name']) for entry in local)
        prediction=weighted_matrix(node_operators,config['operator_weights'])
        contracted=contract_histories(prediction,coefficients)
        leaf=next(row for row in config['ownership'] if row['frequency_index']==index)
        assert digest(leaf['source_leaf'])==leaf['source_leaf_sha256']
        previous=packet(leaf['source_leaf'])
        helpers.compare(f'node{index}:original forecast replay',contracted,(previous['predicted_high'],previous['predicted_low']),factor,rows,replays)
        engine.prediction_checks(f'node{index}',contracted,(previous['actual_high'],previous['actual_low']),factor,rows,physical)
        save(destination/f'source-node-{index}.npz',high=contracted[0],low=contracted[1])
        catalog.append(dict(frequency_index=index,frequency=config['original_panel'][index]['frequency'],
            original_seed_weight=config['original_panel'][index]['seed_weight'],weight_already_included=True,
            anchor_operators=anchors,active_input_indices=engine.prior.ACTIVE,matrix_shape=[6,98,97,2]))
    catalog.sort(key=lambda row:row['frequency_index'])
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    assert not list(ROOT.rglob('__pycache__')) and not list(ROOT.rglob('*.partial'))
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected workbench recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    for node in catalog:
        for anchor in node['anchor_operators'].values():
            assert digest(anchor['path'])==anchor['sha256']
        if node['frequency_index'] in complete_nodes:
            node['history_replay_qualified']=not failed
    write(destination/'operator-catalog.json',dict(operator_nodes=catalog,
        pending_nodes=[index for index in range(7) if index not in [node['frequency_index'] for node in catalog]],
        full_panel_complete=False,qualified=not failed,partial_batch=True))
    report=dict(stage=219,state='saved_partial',checks=rows,failed_checks=failed,completed_events=completed,pending_events=pending,
        qualified_completed_work=not failed,batch_complete=not pending,operator_nodes_ready=[node['frequency_index'] for node in catalog],
        inputs_rehashed=len(inputs),replays=replays,physical_records=physical,original_bank_changed=False,
        grids_changed=False,tolerances_changed=False,active_workers=0,created_at=now(),
        protected_workbench_recent_mtime_count=len(changed),guard_scope='recent mtime, not full-tree content hash')
    write(destination/'validation.json',report)
    for path in destination.rglob('*'):
        if path.is_file():
            hashes[str(path.relative_to(ROOT))]=digest(path)
    for path in [ROOT/'configuration.json',ROOT/'inputs.json',*ROOT.glob('*.py'),ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',*list((ROOT/'frozen').glob('*.npz'))]:
        hashes[str(path.relative_to(ROOT))]=digest(path)
    write(destination/'restart-integrity.json',dict(stage=219,state='partial_not_final_seal',created_at=now(),file_hashes=hashes,
        configuration_sha256=digest(ROOT/'configuration.json'),immutable_completed_events=len(completed),pending_events=len(pending),
        scope='listed immutable files only; future new events and worker status updates allowed',qualified_completed_work=not failed))
    write(ROOT/'progress.json',dict(state='saved_partial',batch_events_complete=len(completed),batch_events_pending=len(pending),
        operator_nodes_ready=[node['frequency_index'] for node in catalog],active_workers=0,restart_manifest=str(destination/'restart-integrity.json'),
        next='resume219.ps1 with a fresh attempt name and deadline inside the next four-hour turn'))
    print(json.dumps(dict(directory=str(destination),checks=len(rows),failed=len(failed),completed_events=len(completed),pending_events=len(pending),
        nodes_ready=[node['frequency_index'] for node in catalog],max_replay=max(row['relative'] for row in replays))),flush=True)


if __name__=='__main__':
    source.modest();main()
