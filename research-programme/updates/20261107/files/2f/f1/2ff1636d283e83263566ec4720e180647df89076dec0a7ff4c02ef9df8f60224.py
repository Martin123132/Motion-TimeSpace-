from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,time,zipfile,hashlib,copy
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'complete-panel-operator-batch1-20261025'
PARENT_SHA='b0c71a1a443db040239c1d2cf4549a7b152a0c7c36ab42e5ffd697df5b774691'
ENGINE_SHA='9ee747e04d0bee082ccc4b5ec35ec78d614ed9dc703bfe19eda5b301c14bfd5c'
sys.path.insert(0,str(PARENT))
import batch218 as engine
engine.ROOT=ROOT
np,mp,linear=engine.np,engine.mp,engine.linear
source,metrics,api,helpers=engine.source,engine.metrics,engine.api,engine.helpers
read,write,packet,save,digest,check=engine.read,engine.write,engine.packet,engine.save,engine.digest,engine.check
LABELS,COMPONENTS=engine.LABELS,engine.COMPONENTS
contract_histories,weighted_matrix=engine.contract_histories,engine.weighted_matrix
register,protocol,event_path,verify_event=engine.register,engine.protocol,engine.event_path,engine.verify_event


def now():
    return datetime.now(timezone.utc).isoformat()


def prepare():
    assert not (ROOT/'configuration.json').exists()
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    assert digest(PARENT/'batch218.py')==ENGINE_SHA
    parent=read(PARENT/'results/stage-integrity.json');assert parent['qualified']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    for name,value in parent['file_hashes'].items():
        register(inputs,PARENT/name,value)
    register(inputs,PARENT/'results/stage-integrity.json',PARENT_SHA)
    previous=read(PARENT/'configuration.json')
    old_catalog=read(PARENT/'results/operator-catalog.json')
    assert old_catalog['qualified'] and [row['frequency_index'] for row in old_catalog['operator_nodes']]==[0,1,6]
    for node in old_catalog['operator_nodes']:
        for anchor in node['anchor_operators'].values():
            register(inputs,anchor['path'],anchor['sha256'])
    selected=[row for row in previous['events'] if row['frequency_index'] in (2,3)]
    assert len(selected)==216
    for row in selected:
        register(inputs,row['source_path'],row['source_sha256'])
        register(inputs,row['loop_path'],row['loop_sha256'])
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        loop=read(row['loop_path'])
        assert weight==row['weight'] and loop['finite']
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    original,theta=source.context(previous['target_fraction'])
    assert theta==previous['theta']
    for path in original.inputs:
        register(inputs,path)
    for name in ('history-coefficients.npz','basis-metric.npz'):
        path=register(inputs,PARENT/'frozen'/name)
        destination=ROOT/'frozen'/name;destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(path.read_bytes())
    rows=[]
    check(rows,'same source-context mass',int(not np.array_equal(packet(ROOT/'frozen/basis-metric.npz')['mass'],original.basis.mass)),0,'integrity')
    implementation={}
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs,path);implementation[str(path)]=digest(path)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in bookmarks:
            archive.writestr(Path(name).name,Path(name).read_bytes())
    config=copy.deepcopy(previous)
    config.update(stage=219,turn_start='2026-10-26T00:29:00+00:00',prepared_at=now(),all_missing_nodes=[2,3,4,5],
        batch_nodes=[2,3],pending_nodes=[4,5],reused_catalog=old_catalog['operator_nodes'],
        engine_path=str(PARENT/'batch218.py'),engine_sha256=ENGINE_SHA,implementation=implementation,bookmarks=bookmarks,
        protocol_hashes={path.name:digest(path) for path in [ROOT/'batch219.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
        frozen_hashes={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen').glob('*.npz')})
    write(ROOT/'inputs.json',inputs);write(ROOT/'configuration.json',config)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    write(ROOT/'progress.json',dict(state='prepared',batch_events_complete=0,batch_events_required=216,full_remaining_events_at_start=432))
    print(json.dumps(dict(state='prepared',batch_nodes=[2,3],reused_nodes=[0,1,6],batch_events=216,inputs=len(inputs))),flush=True)


def assess():
    config=protocol();assert not (ROOT/'results/assessment.json').exists()
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    basis=packet(ROOT/'frozen/basis-metric.npz');factor=linear.cholesky(basis['mass'],lower=True)
    rows=list(read(ROOT/'results/preparation.json')['checks']);replays=[];physical=[];identities={};catalog=copy.deepcopy(config['reused_catalog'])
    for index in config['batch_nodes']:
        node_operators=[];anchors={}
        for label in LABELS:
            matrices=[];event_sources=[];direct_sources=[]
            for row in [row for row in config['events'] if row['frequency_index']==index and row['label']==label]:
                values,report=verify_event(row)
                rows.extend(dict(entry,name=f'node{index}:{label}:event{row["event"]}:'+entry['name']) for entry in report['checks'])
                replays.extend(dict(entry,scope=f'node{index}:{label}:event{row["event"]}') for entry in report['replays'])
                matrices.append((values['high'],values['low']))
                replay=packet(event_path(row).with_name(event_path(row).stem+'-replay.npz'))
                event_sources.append((replay['high'],replay['low']))
                direct=packet(row['source_path']);direct_sources.append((direct['high'],direct['low']))
            assert len(matrices)==36
            total=api.sum_events(matrices);node_operators.append(total)
            path=ROOT/f'results/operator-node-{index}-{label}.npz'
            save(path,high=total[0],low=total[1],theta=config['anchor_thetas'][label],frequency=config['original_panel'][index]['frequency'])
            anchors[label]=dict(path=str(path),sha256=digest(path),theta=config['anchor_thetas'][label])
            contracted=contract_histories(total,coefficients)
            helpers.compare(f'node{index}:{label}:contract-before-after-sum',contracted,metrics.primitives(event_sources),factor,rows,replays)
            helpers.compare(f'node{index}:{label}:summed direct anchor',contracted,metrics.primitives(direct_sources),factor,rows,replays)
            local=[];identities[f'{index}:{label}']=helpers.matrix_identities(dict(high=total[0],low=total[1]),basis,local)
            rows.extend(dict(entry,name=f'node{index}:{label}:'+entry['name']) for entry in local)
        prediction=weighted_matrix(node_operators,config['operator_weights'])
        predicted_source=contract_histories(prediction,coefficients)
        save(ROOT/f'results/predicted-node-{index}.npz',high=prediction[0],low=prediction[1])
        save(ROOT/f'results/source-node-{index}.npz',high=predicted_source[0],low=predicted_source[1])
        leaf=next(entry for entry in config['ownership'] if entry['frequency_index']==index)
        assert digest(leaf['source_leaf'])==leaf['source_leaf_sha256']
        old=packet(leaf['source_leaf'])
        helpers.compare(f'node{index}:original frozen source forecast',predicted_source,(old['predicted_high'],old['predicted_low']),factor,rows,replays)
        engine.prediction_checks(f'node{index}',predicted_source,(old['actual_high'],old['actual_low']),factor,rows,physical)
        catalog.append(dict(frequency_index=index,frequency=config['original_panel'][index]['frequency'],
            original_seed_weight=config['original_panel'][index]['seed_weight'],weight_already_included=True,anchor_operators=anchors,
            active_input_indices=engine.prior.ACTIVE,matrix_shape=[6,98,97,2]))
    catalog.sort(key=lambda row:row['frequency_index'])
    subset=[row['frequency_index'] for row in catalog];assert subset==[0,1,2,3,6]
    subset_anchors=[]
    for label in LABELS:
        members=[]
        for node in catalog:
            anchor=node['anchor_operators'][label]
            assert digest(anchor['path'])==anchor['sha256']
            values=packet(anchor['path']);members.append((values['high'],values['low']))
        total=api.sum_events(members);subset_anchors.append(total)
        save(ROOT/f'results/operator-subset-{label}.npz',high=total[0],low=total[1],frequencies=np.array([row['frequency'] for row in catalog]))
        local=[];identities['subset:'+label]=helpers.matrix_identities(dict(high=total[0],low=total[1]),basis,local)
        rows.extend(dict(entry,name='subset:'+label+':'+entry['name']) for entry in local)
    predicted=weighted_matrix(subset_anchors,config['operator_weights'])
    contracted=contract_histories(predicted,coefficients);leaves=[]
    for index in subset:
        path=engine.PANEL/'results/source-node-6.npz' if index==6 else Path(next(entry for entry in config['ownership'] if entry['frequency_index']==index)['source_leaf'])
        leaves.append(packet(path))
    expected=metrics.primitives([(leaf['predicted_high'],leaf['predicted_low']) for leaf in leaves])
    actual=metrics.primitives([(leaf['actual_high'],leaf['actual_low']) for leaf in leaves])
    helpers.compare('five-node:old forecast replay',contracted,expected,factor,rows,replays)
    engine.prediction_checks('five-node',contracted,actual,factor,rows,physical)
    save(ROOT/'results/operator-subset-predicted.npz',high=predicted[0],low=predicted[1])
    save(ROOT/'results/source-subset.npz',predicted_high=contracted[0],predicted_low=contracted[1],actual_high=actual[0],actual_low=actual[1])
    failed=[row for row in rows if not row['passed']]
    for node in catalog:
        if node['frequency_index'] in config['batch_nodes']:
            node['history_replay_qualified']=not failed
    write(ROOT/'results/operator-catalog.json',dict(original_panel=config['original_panel'],operator_nodes=catalog,
        pending_nodes=[4,5],full_panel_complete=False,qualified=not failed,source_history_fraction=config['target_fraction'],
        basis_path=str(ROOT/'frozen/basis-metric.npz'),basis_sha256=digest(ROOT/'frozen/basis-metric.npz'),
        normalization='original event weights included; no partial-panel rescaling'))
    report=dict(stage=219,checks=rows,failed_checks=failed,replays=replays,physical_records=physical,column_identities=identities,
        qualified=not failed,batch_complete=True,operator_nodes_ready=subset,operator_nodes_pending=[4,5],
        full_seven_node_operator_complete=False,all_frequency_operator_complete=False,uniform_temperature_qualified=False,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,new_virtual_integrals=0)
    write(ROOT/'results/assessment.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),nodes_ready=subset,pending=[4,5],max_replay=max(row['relative'] for row in replays),
        physical={name:max(row['relative'] for row in physical if row['component']==name) for name in COMPONENTS})),flush=True)


def validate():
    config=protocol();assessment=read(ROOT/'results/assessment.json');catalog=read(ROOT/'results/operator-catalog.json')
    rows=list(assessment['checks']);inputs=read(ROOT/'inputs.json')
    assert digest(config['engine_path'])==ENGINE_SHA==config['engine_sha256']
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'all consumed and immediate inputs unchanged',0,0,'integrity')
    selected=[row for row in config['events'] if row['frequency_index'] in config['batch_nodes']]
    for row in selected:
        values,report=verify_event(row)
        assert report['new_virtual_integrals']==0 and report['scalar_precision']==60 and report['protected_precision']==80
        assert datetime.fromisoformat(report['replay_frozen_before_comparison'])<=datetime.fromisoformat(report['finished_at'])
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        loop=read(row['loop_path'])
        assert weight==row['weight'] and digest(row['loop_path'])==row['loop_sha256'] and loop['finite']
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    check(rows,'all216 batch matrix events complete',len(list((ROOT/'events').rglob('event-*.json')))-216,0,'integrity')
    check(rows,'no new virtual-cache files',len(list((ROOT/'virtual-cache').rglob('*'))) if (ROOT/'virtual-cache').exists() else 0,0,'integrity')
    assert [row['frequency_index'] for row in catalog['operator_nodes']]==[0,1,2,3,6]
    samples=[]
    with mp.workdps(100):
        for node in catalog['operator_nodes']:
            index=node['frequency_index']
            for label,anchor in node['anchor_operators'].items():
                assert digest(anchor['path'])==anchor['sha256']
                if index not in config['batch_nodes']:
                    continue
                values=packet(anchor['path'])
                events=[verify_event(row)[0] for row in selected if row['frequency_index']==index and row['label']==label]
                for component,row_index,column,join in ((0,0,0,0),(1,2,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,1,96,1)):
                    parts=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
                    exact=mp.fsum(mp.mpf(float(event['high'][part,row_index,column,join]))+mp.mpf(float(event['low'][part,row_index,column,join])) for event in events for part in parts)
                    stored=mp.mpf(float(values['high'][component,row_index,column,join]))+mp.mpf(float(values['low'][component,row_index,column,join]))
                    relative=float(abs(exact-stored)/max(abs(exact),mp.mpf('1e-300')));samples.append(relative)
                    check(rows,f'100digit node{index}:{label}:{component}:{row_index}:{column}:{join}',relative,1e-10,'identity')
        for label in LABELS:
            subset=packet(ROOT/f'results/operator-subset-{label}.npz')
            members=[packet(node['anchor_operators'][label]['path']) for node in catalog['operator_nodes']]
            for component,row_index,column,join in ((0,0,0,0),(1,1,48,1),(2,97,96,0),(3,42,63,1),(4,83,47,0),(5,2,96,1)):
                parts=[component] if component<4 else [1,2,3] if component==4 else [0,1,2,3]
                exact=mp.fsum(mp.mpf(float(member['high'][part,row_index,column,join]))+mp.mpf(float(member['low'][part,row_index,column,join])) for member in members for part in parts)
                stored=mp.mpf(float(subset['high'][component,row_index,column,join]))+mp.mpf(float(subset['low'][component,row_index,column,join]))
                relative=float(abs(exact-stored)/max(abs(exact),mp.mpf('1e-300')));samples.append(relative)
                check(rows,f'100digit five-node:{label}:{component}:{row_index}:{column}:{join}',relative,1e-10,'identity')
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
    report=dict(stage=219,checks=rows,failed_checks=failed,qualified=not failed,inputs_rehashed=len(inputs),
        batch_events=216,new_virtual_integrals=0,operator_nodes_ready=[0,1,2,3,6],operator_nodes_pending=[4,5],
        full_seven_node_operator_complete=False,decimal_sample_max=max(samples),
        assessment_sha256=digest(ROOT/'results/assessment.json'),catalog_sha256=digest(ROOT/'results/operator-catalog.json'),
        protected_workbench_recent_mtime_count=len(changed),guard_scope='recent mtime, not full-tree content hash',
        original_bank_changed=False,grids_changed=False,tolerances_changed=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),qualified=not failed,inputs=len(inputs),decimal_sample_max=max(samples))),flush=True)


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
        operator_nodes_ready=[0,1,2,3,6],operator_nodes_pending=[4,5],full_panel_complete=False,active_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=219,state='batch_complete',qualified=validation['qualified'],sealed_at=now(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=read(ROOT/'inputs.json'),file_hashes=hashes,batch_events=216,new_virtual_integrals=0,
        operator_nodes_ready=[0,1,2,3,6],operator_nodes_pending=[4,5],full_seven_node_operator_complete=False,
        complete_source_panel_preserved=True,retained_current_failures=len(validation['failed_checks']),
        maximum_concurrent_workers=2,numerical_threads_per_worker=1,active_workers_at_seal=0,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,permission_to_propagate=False,
        github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(sha256=digest(destination),payloads=len(hashes),qualified=validation['qualified'])),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','run','assess','validate','seal'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=11600)
    parser.add_argument('--stop-at',default='2026-10-26T03:55:00+00:00')
    args=parser.parse_args()
    if args.phase=='run':
        engine.run(args.worker,args.seconds,args.stop_at)
    else:
        {'prepare':prepare,'assess':assess,'validate':validate,'seal':seal}[args.phase]()
