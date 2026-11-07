from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,time,zipfile,hashlib,math
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'collision-operator-temperature-bridge-20261025'
PARENT_SHA='f5996d325c96a1fac83e59fbc1ca451d69644569503f9168b701a995a0db3ef1'
sys.path.insert(0,str(PARENT))
import bridge215 as previous
import assess215 as previous_assessment
np,mp,linear=previous.np,previous.mp,previous.linear
source,metrics,api=previous.source,previous.metrics,previous.api
read,write,packet,save,digest,check=previous.read,previous.write,previous.packet,previous.save,previous.digest,previous.check
helpers,COMPONENTS,ACTIVE=previous.helpers,previous.COMPONENTS,previous.ACTIVE
core=previous.lift.owner
history=core.previous
evolution=history.evolution
contract_histories,weighted_matrix=previous.contract_histories,previous.weighted_matrix
LABELS=previous.LABELS


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['frozen_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['qualified'] and parent['operator_block_prediction_passed']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    contract=read(PARENT/'NEXT-TEMPERATURE-CONTRACT.json')
    parent_config=read(PARENT/'configuration.json')
    fraction=contract['native_source_fraction_estimate']
    original,theta=source.context(fraction)
    rows=[]
    check(rows,'prespecified temperature',theta/contract['theta_estimate']-1,1e-10,'identity')
    for power in (0,1,2):
        check(rows,f'frozen Lagrange degree {power}',sum(weight*offset**power for weight,offset in zip(contract['weights'],parent_config['anchor_offsets']))-contract['offset']**power,1e-14,'identity')
    history_config=read(history.HISTORY/'configuration.json')
    check(rows,'offset coordinate consistency',theta/(history_config['theta0']*math.exp(contract['offset']))-1,1e-10,'identity')
    for path in original.inputs:
        inputs[str(path)]=digest(path)
    old_root=history.ROOT
    try:
        history.ROOT=ROOT
        histories={(model,grid):history.sample_history(model,grid,fraction*history_config['expansion_span'],inputs)
                   for model in ('heavy','cold') for grid in core.GRIDS}
    finally:
        history.ROOT=old_root
    with mp.workdps(80):
        mass=evolution.smooth.corner.mp_matrix(original.basis.mass)
        norm=lambda vector:mp.sqrt((vector.T*mass*vector)[0])
        for index,model in enumerate(('heavy','cold')):
            half=evolution.history.parse_state(histories[(model,'half')]['current'])
            quarter=evolution.history.parse_state(histories[(model,'quarter')]['current'])
            reference=mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].original[model]])
            check(rows,model+':photon repair mesh',norm(half['profile']-quarter['profile'])/norm(quarter['profile']-reference),.01,'mesh')
            check(rows,model+':gas repair mesh',abs((half['gas']-quarter['gas'])/(quarter['gas']-mp.mpf(float(original.gas[index])))),.01,'mesh')
    for (model,grid),record in histories.items():
        rows.extend(dict(entry,name=f'{model}:{grid}:'+entry['name']) for entry in record['checks'])
    bundle=history.coefficient_bundle(original,histories)
    check(rows,'tail repair exactly zero',np.max(abs(bundle.high[96:98]))+np.max(abs(bundle.low[96:98])),0,'identity')
    save(ROOT/'frozen/history-coefficients.npz',high=bundle.high,low=bundle.low)
    save(ROOT/'frozen/basis-metric.npz',mass=original.basis.mass,norms=original.basis.norms,mean=original.basis.mean)
    old_original,unused=source.context(parent_config['target_fraction'])
    for path in old_original.inputs:
        inputs[str(path)]=digest(path)
    for label,left,right in (
        ('mass',original.basis.mass,old_original.basis.mass),
        ('frequency grid',original.epochs[0].frequency,old_original.epochs[0].frequency),
        ('all photon basis samples',original.basis.evaluate(original.epochs[0].frequency),old_original.basis.evaluate(old_original.epochs[0].frequency))):
        check(rows,'fixed operator domain '+label,int(not np.array_equal(left,right)),0,'integrity')
    anchors=[]
    for label in LABELS:
        path=PARENT/f'results/operator-{label}.npz'
        values=packet(path)
        anchors.append((values['high'],values['low']))
        inputs[str(path)]=digest(path)
    prediction=weighted_matrix(anchors,contract['weights'])
    save(ROOT/'frozen/predicted-operator.npz',high=prediction[0],low=prediction[1],theta=theta)
    predicted_source=contract_histories(prediction,dict(high=bundle.high,low=bundle.low))
    save(ROOT/'frozen/predicted-source.npz',high=predicted_source[0],low=predicted_source[1])
    events=[]
    for event,node in enumerate(core.microscopic.event_common.nodes(theta,contract['frequency'])):
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        inventory=core.cache_inventory(parameters)
        for match in inventory['matches']:
            inputs[match['path']]=match['sha256']
        events.append(dict(event=event,node=node,theta=theta,weight=weight,inventory=inventory))
    assert len(events)==36 and len({row['inventory']['key'] for row in events})==36
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            path=Path(name).resolve()
            inputs[str(path)]=digest(path);implementation[str(path)]=digest(path)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in bookmarks:
            archive.writestr(Path(path).name,Path(path).read_bytes())
    failed=[entry for entry in rows if not entry['passed']]
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=failed))
    assert not failed,failed
    write(ROOT/'inputs.json',inputs)
    frozen={str(path.relative_to(ROOT)):digest(path) for folder in ('frozen','histories') for path in (ROOT/folder).rglob('*') if path.is_file()}
    config=dict(stage=216,turn_start='2026-10-25T19:32:30+00:00',prepared_at=now(),safe_stop_utc='2026-10-25T23:10:00+00:00',
        theta=theta,target_fraction=fraction,offset=contract['offset'],frequency=contract['frequency'],operator_weights=contract['weights'],
        events=events,cache_hits=sum(bool(row['inventory']['matches']) for row in events),
        bookmarks=bookmarks,implementation=implementation,frozen_hashes=frozen,
        predicted_operator_path=str(ROOT/'frozen/predicted-operator.npz'),history_source='original-equation restart from saved Stage200 histories',
        new_temperature_global_nonuse_proven=False,observational_holdout=False,original_bank_changed=False,
        protocol_hashes={name:digest(ROOT/name) for name in ('test216.py','ACCEPTANCE.md','DERIVATION.md')})
    write(ROOT/'configuration.json',config)
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_at=now(),configuration_sha256=digest(ROOT/'configuration.json'),
            files=frozen,direct_new_events_at_freeze=0,weights_preselected_in_stage215=True))
    write(ROOT/'progress.json',dict(state='predictions_and_histories_frozen',events_complete=0))
    print(json.dumps(dict(state='prepared_and_frozen',checks=len(rows),events=36,cache_hits=config['cache_hits'],inputs=len(inputs),theta=theta)),flush=True)


def setup(config):
    original,theta=source.context(config['target_fraction'])
    assert theta==config['theta']
    records={(model,grid):read(ROOT/f'histories/{model}-{grid}.json') for model in ('heavy','cold') for grid in core.GRIDS}
    direct_bundle=history.coefficient_bundle(original,records)
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    assert np.array_equal(direct_bundle.high,coefficients['high']) and np.array_equal(direct_bundle.low,coefficients['low'])
    operator_bundle,operator_models=api.evaluators(original)
    return direct_bundle,core.cached.models(direct_bundle),operator_bundle,operator_models


def virtual(row,parameters):
    inventory=row['inventory']
    identity,key=core.loop_identity(parameters)
    assert identity==inventory['identity'] and key==inventory['key']
    if inventory['matches']:
        found=inventory['matches'][0]
        assert digest(found['path'])==found['sha256']
        return found['scalar'],Path(found['path']),False
    path=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    if path.exists():
        values=read(path)
        assert values['identity']==identity and values['finite']
        return values['scalar'],path,False
    with mp.workdps(60):
        tensor,response=source.physics.weak.source.virtual_map(parameters,2)
    assert np.isfinite(tensor).all() and np.isfinite(response).all()
    write(path,dict(identity=identity,scalar=float(response[0,0]),finite=True,order=2,precision=60))
    return float(response[0,0]),path,True


def verify_completed(row):
    path=ROOT/f"events/event-{row['event']:02d}.json"
    report=read(path)
    assert not report['failed_checks']
    for key in ('operator','direct','prediction'):
        assert digest(ROOT/report[key+'_path'])==report[key+'_sha256']
    assert digest(report['loop_path'])==report['loop_sha256']
    return report


def run(worker,seconds):
    config=protocol()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert manifest['configuration_sha256']==digest(ROOT/'configuration.json')
    for name,value in config['implementation'].items():
        assert digest(name)==value,name
    direct_bundle,direct_models,operator_bundle,operator_models=setup(config)
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    began=time.monotonic();done=0
    for row in config['events']:
        if row['event']%2!=worker:
            continue
        event=row['event']
        final=ROOT/f'events/event-{event:02d}.json'
        if final.exists():
            verify_completed(row)
            continue
        if time.monotonic()-began>=seconds or datetime.now(timezone.utc)>=datetime.fromisoformat(config['safe_stop_utc']):
            break
        started=now();tick=time.monotonic()
        assert datetime.fromisoformat(started)>datetime.fromisoformat(manifest['frozen_at'])
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight']
        scalar,loop_path,new_loop=virtual(row,parameters)
        operator_path=ROOT/f'events/operator-{event:02d}.npz'
        partial_path=ROOT/f'events/operator-{event:02d}.json'
        if partial_path.exists():
            partial=read(partial_path)
            assert digest(operator_path)==partial['sha256'] and not partial['failed_checks']
            values=packet(operator_path)
            matrix=(values['high'],values['low'])
            checks=list(partial['checks'])
        else:
            matrix,diagnostics=api.evaluate_event(parameters,operator_bundle,operator_models,scalar,weight)
            checks=[]
            for name,value in diagnostics.items():
                check(checks,'operator:'+name,value,1e-10,'identity')
            save(operator_path,high=matrix[0],low=matrix[1],theta=row['theta'],weight=weight)
            write(partial_path,dict(sha256=digest(operator_path),checks=checks,failed_checks=[entry for entry in checks if not entry['passed']],
                 loop_path=str(loop_path),loop_sha256=digest(loop_path),finished_at=now()))
        predicted=contract_histories(matrix,coefficients)
        prediction_path=ROOT/f'events/replay-{event:02d}.npz'
        if not prediction_path.exists():
            save(prediction_path,high=predicted[0],low=predicted[1])
        else:
            saved_prediction=packet(prediction_path)
            assert np.array_equal(saved_prediction['high'],predicted[0]) and np.array_equal(saved_prediction['low'],predicted[1])
        replay_frozen=now()
        old=source.physics.precise_state
        try:
            source.physics.precise_state=core.precise.precise_state
            high,low,diagnostics=core.microscopic.weighted(parameters,direct_bundle,direct_models,scalar,weight)
        finally:
            source.physics.precise_state=old
        for name,value in diagnostics.items():
            check(checks,'direct:'+name,value,1e-10,'identity')
        direct_path=ROOT/f'events/direct-{event:02d}.npz'
        save(direct_path,high=high,low=low,theta=row['theta'],weight=weight)
        check(checks,'finite',int(not np.isfinite(high+low).all() or not all(np.isfinite(value).all() for value in matrix)),0,'integrity')
        check(checks,'direct zero history',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'negative_control')
        failed=[entry for entry in checks if not entry['passed']]
        paths=dict(operator_path=str(operator_path.relative_to(ROOT)),operator_sha256=digest(operator_path),
            direct_path=str(direct_path.relative_to(ROOT)),direct_sha256=digest(direct_path),
            prediction_path=str(prediction_path.relative_to(ROOT)),prediction_sha256=digest(prediction_path))
        write(final,dict(**paths,event=event,worker=worker,started_at=started,finished_at=now(),replay_frozen_before_direct=replay_frozen,
            seconds=time.monotonic()-tick,checks=checks,failed_checks=failed,
            loop_path=str(loop_path),loop_sha256=digest(loop_path),new_virtual_integral=new_loop))
        done+=1
        write(ROOT/f'workers/{worker}.json',dict(state='running',done=done,last_event=event,pid=os.getpid(),updated_at=now()))
        print(json.dumps(dict(event=event,seconds=time.monotonic()-tick,new_loop=new_loop,failed=len(failed))),flush=True)
        assert not failed,failed
    import psutil
    memory=psutil.Process().memory_info()
    write(ROOT/f'workers/{worker}.json',dict(state='stopped',completed_this_call=done,stopped_at=now(),peak_working_set_bytes=getattr(memory,'peak_wset',memory.rss)))
    print(json.dumps(dict(worker=worker,completed_this_call=done)),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=10500)
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare()
    else:
        run(args.worker,args.seconds)
