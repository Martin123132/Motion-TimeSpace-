from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,time,zipfile,hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'operator-response-injection-20261025'
PARENT_SHA='75d7ef72d84f2285714979158ac28d1f04c038afe99410510cddc74694744eca'
ANCHORS=BRANCH/'collision-operator-temperature-bridge-20261025'
PANEL=BRANCH/'history-aware-complete-band-temperature-test-20261025'
sys.path.insert(0,str(ANCHORS))
import bridge215 as prior
np,mp,linear=prior.np,prior.mp,prior.linear
source,metrics,api,helpers=prior.source,prior.metrics,prior.api,prior.helpers
read,write,packet,save,digest,check=prior.read,prior.write,prior.packet,prior.save,prior.digest,prior.check
COMPONENTS,LABELS=prior.COMPONENTS,prior.LABELS
contract_histories,weighted_matrix=prior.contract_histories,prior.weighted_matrix
OWNER_NAMES={0:'history-aware-upper-outer-temperature-test-20261025',1:'history-aware-lower-pair-temperature-test-20261025',
    2:'history-aware-lower-pair-temperature-test-20261025',3:'history-aware-operator-temperature-test-20261025',
    4:'history-aware-neighbour-temperature-test-20261025',5:'history-aware-upper-outer-temperature-test-20261025'}


def now():
    return datetime.now(timezone.utc).isoformat()


def register(inputs,path,expected=None):
    path=Path(path).resolve();value=digest(path)
    assert expected is None or value==expected,str(path)
    assert str(path) not in inputs or inputs[str(path)]==value,str(path)
    inputs[str(path)]=value
    return path


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['frozen_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def prepare():
    assert not (ROOT/'configuration.json').exists()
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    parent=read(PARENT/'results/stage-integrity.json');assert parent['qualified']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    for name,value in parent['file_hashes'].items():
        register(inputs,PARENT/name,value)
    register(inputs,PARENT/'results/stage-integrity.json',PARENT_SHA)
    panel=read(register(inputs,PANEL/'configuration.json'))
    previous=read(register(inputs,ANCHORS/'configuration.json'))
    rows=[];events=[];ownership=[]
    for index,owner_name in OWNER_NAMES.items():
        owner=BRANCH/owner_name
        local=read(register(inputs,owner/'configuration.json'))
        assert local['target_fraction']==previous['target_fraction']
        assert local['operator_weights']==previous['operator_weights']
        assert digest(owner/'frozen/history-coefficients.npz')==previous['coefficients_sha256']
        frequency=panel['original_panel'][index]['frequency']
        selected=[row for row in local['anchors'] if row['node']['frequency']==frequency]
        assert len(selected)==108
        leaf=owner/('results/source-node.npz' if index in (3,4) else f'results/source-node-{index}.npz')
        register(inputs,leaf)
        ownership.append(dict(frequency_index=index,frequency=frequency,owner=str(owner),source_leaf=str(leaf),
            source_leaf_sha256=digest(leaf),batch='current' if index in (0,1) else 'next',events=108))
        for row in selected:
            folder=owner/'anchors'
            if index not in (3,4):
                folder=folder/f'frequency-{index}'
            report_path=register(inputs,folder/row['label']/f"event-{row['event']:02d}.json")
            report=read(report_path);assert not report['failed_checks']
            source_path=register(inputs,report_path.with_suffix('.npz'),report['sha256'])
            loop_path=register(inputs,report['loop_path'],report['loop_sha256'])
            parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
            loop=read(loop_path)
            assert weight==row['weight'] and loop['finite']
            assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
            events.append(dict(frequency_index=index,frequency=frequency,label=row['label'],event=row['event'],
                theta=row['theta'],node=row['node'],weight=weight,source_path=str(source_path),source_sha256=report['sha256'],
                loop_path=str(loop_path),loop_sha256=report['loop_sha256']))
    assert len(events)==648
    events.sort(key=lambda row:(row['frequency_index'],LABELS.index(row['label']),row['event']))
    original,theta=source.context(previous['target_fraction'])
    assert theta==previous['theta']
    for path in original.inputs:
        register(inputs,path)
    for name in ('history-coefficients.npz','basis-metric.npz'):
        path=register(inputs,ANCHORS/'frozen'/name)
        destination=ROOT/'frozen'/name;destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(path.read_bytes())
    basis=packet(ROOT/'frozen/basis-metric.npz')
    check(rows,'same source-context mass matrix',int(not np.array_equal(basis['mass'],original.basis.mass)),0,'integrity')
    reused={}
    for label in LABELS:
        path=register(inputs,ANCHORS/f'results/operator-{label}.npz')
        reused[label]=dict(path=str(path),sha256=digest(path))
    register(inputs,PANEL/'results/source-node-6.npz')
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
    config=dict(stage=218,turn_start='2026-10-25T21:10:00+00:00',prepared_at=now(),
        target_fraction=previous['target_fraction'],theta=theta,operator_weights=previous['operator_weights'],
        anchor_offsets=previous['anchor_offsets'],anchor_thetas=previous['anchor_thetas'],original_panel=panel['original_panel'],
        all_missing_nodes=list(range(6)),batch_nodes=[0,1],pending_nodes=[2,3,4,5],events=events,ownership=ownership,
        reused_upper_node=reused,implementation=implementation,bookmarks=bookmarks,
        protocol_hashes={path.name:digest(path) for path in [ROOT/'batch218.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
        frozen_hashes={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen').glob('*.npz')},
        replay_not_holdout=True,maximum_workers=2,numerical_threads_per_worker=1,new_virtual_integrals_required=0)
    write(ROOT/'inputs.json',inputs);write(ROOT/'configuration.json',config)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    write(ROOT/'progress.json',dict(state='prepared',batch_events_complete=0,batch_events_required=216,full_missing_events=648))
    print(json.dumps(dict(state='prepared',batch_nodes=[0,1],batch_events=216,all_missing_events=648,inputs=len(inputs))),flush=True)


def event_path(row):
    return ROOT/f"events/frequency-{row['frequency_index']}/{row['label']}/event-{row['event']:02d}.npz"


def verify_event(row):
    path=event_path(row);report=read(path.with_suffix('.json'))
    assert digest(path)==report['sha256'] and digest(path.with_name(path.stem+'-replay.npz'))==report['replay_sha256']
    assert report['loop_sha256']==row['loop_sha256'] and report['source_sha256']==row['source_sha256']
    assert not report['failed_checks'],report['failed_checks']
    values=packet(path)
    assert values['high'].shape==values['low'].shape==(6,98,97,2)
    assert float(values['theta'])==row['theta'] and float(values['weight'])==row['weight']
    return values,report


def run(worker,seconds,stop_at):
    config=protocol();deadline=datetime.fromisoformat(stop_at)
    for name,value in config['implementation'].items():
        assert digest(name)==value,name
    original,theta=source.context(config['target_fraction'])
    bundle,models=api.evaluators(original)
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    factor=linear.cholesky(packet(ROOT/'frozen/basis-metric.npz')['mass'],lower=True)
    selected=[row for row in config['events'] if row['frequency_index'] in config['batch_nodes']]
    began=time.monotonic();done=0
    write(ROOT/f'workers/{worker}.json',dict(state='running',pid=os.getpid(),started_at=now(),stop_at=stop_at))
    for ordinal,row in enumerate(selected):
        if ordinal%2!=worker:
            continue
        path=event_path(row)
        if path.with_suffix('.json').exists():
            verify_event(row);continue
        if datetime.now(timezone.utc)>=deadline or time.monotonic()-began>=seconds:
            break
        started=now();tick=time.monotonic()
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight'] and digest(row['loop_path'])==row['loop_sha256']
        loop=read(row['loop_path'])
        assert loop['finite'] and loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        matrix,diagnostics=api.evaluate_event(parameters,bundle,models,loop['scalar'],weight)
        checks=[];records=[]
        for name,value in diagnostics.items():
            check(checks,name,value,1e-10,'identity')
        check(checks,'finite operator',int(not all(np.isfinite(values).all() for values in matrix)),0,'integrity')
        save(path,high=matrix[0],low=matrix[1],theta=row['theta'],weight=weight)
        replay=contract_histories(matrix,coefficients)
        replay_path=path.with_name(path.stem+'-replay.npz')
        save(replay_path,high=replay[0],low=replay[1])
        frozen_at=now()
        assert digest(row['source_path'])==row['source_sha256']
        direct=packet(row['source_path'])
        helpers.compare('saved direct anchor event',replay,(direct['high'],direct['low']),factor,checks,records)
        failed=[entry for entry in checks if not entry['passed']]
        report=dict(sha256=digest(path),replay_sha256=digest(replay_path),loop_sha256=row['loop_sha256'],
            source_sha256=row['source_sha256'],checks=checks,failed_checks=failed,replays=records,
            worker=worker,started_at=started,replay_frozen_before_comparison=frozen_at,finished_at=now(),
            seconds=time.monotonic()-tick,new_virtual_integrals=0,scalar_precision=60,protected_precision=80)
        write(path.with_suffix('.json'),report);done+=1
        write(ROOT/f'workers/{worker}.json',dict(state='running',pid=os.getpid(),done=done,last_frequency=row['frequency_index'],
            last_label=row['label'],last_event=row['event'],updated_at=now(),stop_at=stop_at))
        print(json.dumps(dict(frequency_index=row['frequency_index'],label=row['label'],event=row['event'],seconds=report['seconds'],failed=len(failed))),flush=True)
        assert not failed,failed
    write(ROOT/f'workers/{worker}.json',dict(state='stopped',pid=os.getpid(),completed_this_call=done,stopped_at=now()))
    print(json.dumps(dict(worker=worker,completed_this_call=done)),flush=True)


def assess():
    config=protocol()
    assert not (ROOT/'results/assessment.json').exists()
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    basis=packet(ROOT/'frozen/basis-metric.npz');factor=linear.cholesky(basis['mass'],lower=True)
    rows=list(read(ROOT/'results/preparation.json')['checks']);replays=[];physical=[];identities={};matrices={};leaves=[]
    for index in config['batch_nodes']:
        node_operators=[]
        for label in LABELS:
            packets=[];event_sources=[];direct_sources=[]
            for row in [row for row in config['events'] if row['frequency_index']==index and row['label']==label]:
                values,report=verify_event(row)
                rows.extend(dict(entry,name=f'node{index}:{label}:event{row["event"]}:'+entry['name']) for entry in report['checks'])
                replays.extend(dict(entry,scope=f'node{index}:{label}:event{row["event"]}') for entry in report['replays'])
                packets.append((values['high'],values['low']))
                replay=packet(event_path(row).with_name(event_path(row).stem+'-replay.npz'))
                event_sources.append((replay['high'],replay['low']))
                direct=packet(row['source_path']);direct_sources.append((direct['high'],direct['low']))
            assert len(packets)==36
            total=api.sum_events(packets);node_operators.append(total)
            matrices[(index,label)]=total
            path=ROOT/f'results/operator-node-{index}-{label}.npz'
            save(path,high=total[0],low=total[1],theta=config['anchor_thetas'][label],frequency=config['original_panel'][index]['frequency'])
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
        leaves.append(old)
        helpers.compare(f'node{index}:original frozen source forecast',predicted_source,(old['predicted_high'],old['predicted_low']),factor,rows,replays)
        prediction_checks(f'node{index}',predicted_source,(old['actual_high'],old['actual_low']),factor,rows,physical)
    for label in LABELS:
        entry=config['reused_upper_node'][label];assert digest(entry['path'])==entry['sha256']
        values=packet(entry['path']);matrices[(6,label)]=(values['high'],values['low'])
    leaves.append(packet(PANEL/'results/source-node-6.npz'))
    subset=[*config['batch_nodes'],6];subset_anchors=[]
    for label in LABELS:
        total=api.sum_events([matrices[(index,label)] for index in subset]);subset_anchors.append(total)
        save(ROOT/f'results/operator-subset-{label}.npz',high=total[0],low=total[1],frequencies=np.array([config['original_panel'][index]['frequency'] for index in subset]))
        local=[];identities['subset:'+label]=helpers.matrix_identities(dict(high=total[0],low=total[1]),basis,local)
        rows.extend(dict(entry,name='subset:'+label+':'+entry['name']) for entry in local)
    predicted=weighted_matrix(subset_anchors,config['operator_weights'])
    contracted=contract_histories(predicted,coefficients)
    expected=metrics.primitives([(leaf['predicted_high'],leaf['predicted_low']) for leaf in leaves])
    actual=metrics.primitives([(leaf['actual_high'],leaf['actual_low']) for leaf in leaves])
    helpers.compare('subset:old forecast replay',contracted,expected,factor,rows,replays)
    prediction_checks('subset',contracted,actual,factor,rows,physical)
    save(ROOT/'results/operator-subset-predicted.npz',high=predicted[0],low=predicted[1])
    save(ROOT/'results/source-subset.npz',predicted_high=contracted[0],predicted_low=contracted[1],actual_high=actual[0],actual_low=actual[1])
    failed=[row for row in rows if not row['passed']]
    report=dict(stage=218,checks=rows,failed_checks=failed,replays=replays,physical_records=physical,column_identities=identities,
        qualified=not failed,batch_complete=True,operator_nodes_ready=subset,operator_nodes_pending=config['pending_nodes'],
        full_seven_node_operator_complete=False,all_frequency_operator_complete=False,uniform_temperature_qualified=False,
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,new_virtual_integrals=0)
    write(ROOT/'results/assessment.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),nodes_ready=subset,nodes_pending=config['pending_nodes'],
        max_replay=max(row['relative'] for row in replays),physical={name:max(row['relative'] for row in physical if row['component']==name) for name in COMPONENTS})),flush=True)


def prediction_checks(label,predicted,actual,factor,rows,records):
    error=metrics.subtract(predicted,actual)
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            records.append(dict(scope=label,grid=('half','quarter')[grid],component=COMPONENTS[component],
                background=('heavy','cold')[column//2],join=column%2,measure=name,relative=value))
            check(rows,f'{label}:physical forecast:{grid}:{component}:{column}:{name}',value,.01,'physical_prediction')


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','run','assess'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=11100)
    parser.add_argument('--stop-at',default='2026-10-26T00:35:00+00:00')
    args=parser.parse_args()
    if args.phase=='run':
        run(args.worker,args.seconds,args.stop_at)
    else:
        {'prepare':prepare,'assess':assess}[args.phase]()
