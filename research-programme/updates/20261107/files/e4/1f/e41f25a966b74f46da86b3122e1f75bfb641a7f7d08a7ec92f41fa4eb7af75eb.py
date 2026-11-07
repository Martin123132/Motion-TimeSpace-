from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,math,time,zipfile
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'cold-source-temperature-connection-20261025'
PARENT_SHA='76344db35d0478ea3917616439f04a78970568dc89c5a4c60a51e0a6a800c215'
sys.path.insert(0,str(PARENT))
import connection208 as previous
np,mp,linear=previous.np,previous.mp,previous.linear
source,microscopic,saved=previous.source,previous.microscopic,previous.saved
read,write,packet,save,digest,check=previous.read,previous.write,previous.packet,previous.save,previous.digest,previous.check
metrics,cached,precise,evolution=previous.metrics,previous.cached,previous.precise,previous.evolution
GRIDS,COMPONENTS=previous.GRIDS,previous.COMPONENTS


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for group in ('protocol_hashes','implementation_hashes','frozen_hashes'):
        for name,value in config[group].items():
            path=Path(name) if group=='implementation_hashes' else ROOT/name
            assert digest(path)==value,str(path)
    return config


def loop_identity(parameters):
    identity=source.physics.event_owner.inherited.virtual_identity(parameters)
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    return identity,key


def cache_inventory(parameters):
    identity,key=loop_identity(parameters)
    matches=[]
    for directory in sorted(set([*BRANCH.glob('*/virtual-cache'),ROOT/'virtual-cache'])):
        path=directory/key[:2]/(key+'.json')
        if path.exists():
            values=read(path)
            assert values['identity']==identity and values['finite'] and np.isfinite(values['scalar']),str(path)
            matches.append(dict(path=str(path),sha256=digest(path),scalar=values['scalar']))
    assert not matches or all(item['scalar']==matches[0]['scalar'] for item in matches)
    return dict(identity=identity,key=key,matches=matches)


def virtual(parameters):
    inventory=cache_inventory(parameters)
    if inventory['matches']:
        found=inventory['matches'][0]
        return found['scalar'],Path(found['path']),False
    tensor,response=source.physics.weak.source.virtual_map(parameters,2)
    assert np.isfinite(tensor).all() and np.isfinite(response).all()
    key=inventory['key']
    path=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    write(path,dict(identity=inventory['identity'],scalar=float(response[0,0]),finite=True))
    return float(response[0,0]),path,True


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['outcome']=='central_temperature_forecast_rejected_and_diagnosed'
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    contract=read(PARENT/'NEXT-TRANSPORT-CONTRACT.json')
    fraction=contract['target_fraction']
    original,theta=source.context(fraction)
    for path in original.inputs:
        saved.register(inputs,path)
    history_config=read(previous.HISTORY/'configuration.json')
    rows=[]
    check(rows,'target temperature matches prespecified coordinate',theta/contract['target_theta']-1,1e-10,'identity')
    weights=contract['operator_weights']
    for power in range(3):
        check(rows,f'Lagrange degree {power}',sum(weight*node**power for weight,node in zip(weights,[0,.5,1]))-.25**power,0,'exact_algebra')
    check(rows,'cubic remainder factor',abs(.25*(.25-.5)*(.25-1))/6-1/128,0,'exact_algebra')
    previous_root=previous.ROOT
    try:
        previous.ROOT=ROOT
        histories={(model,grid):previous.sample_history(model,grid,fraction*history_config['expansion_span'],inputs)
                   for model in ('heavy','cold') for grid in GRIDS}
    finally:
        previous.ROOT=previous_root
    with mp.workdps(80):
        mass=evolution.smooth.corner.mp_matrix(original.basis.mass)
        norm=lambda vector:mp.sqrt((vector.T*mass*vector)[0])
        for index,model in enumerate(('heavy','cold')):
            half=evolution.history.parse_state(histories[(model,'half')]['current'])
            quarter=evolution.history.parse_state(histories[(model,'quarter')]['current'])
            reference=mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].original[model]])
            check(rows,model+':history photon repair mesh',norm(half['profile']-quarter['profile'])/norm(quarter['profile']-reference),.01,'mesh')
            check(rows,model+':history gas repair mesh',abs((half['gas']-quarter['gas'])/(quarter['gas']-mp.mpf(float(original.gas[index])))),.01,'mesh')
    for (model,grid),record in histories.items():
        rows.extend(dict(row,name=f'{model}:{grid}:'+row['name']) for row in record['checks'])
    bundle=previous.coefficient_bundle(original,histories)
    check(rows,'fixed tail coefficients exactly zero',np.max(abs(bundle.high[96:98]))+np.max(abs(bundle.low[96:98])),0,'identity')
    save(ROOT/'frozen/history-coefficients.npz',high=bundle.high,low=bundle.low)
    anchors=[]
    locations=[previous.WARM/'events/frequency-3',
               PARENT/'events/frequency-3',
               BRANCH/'cold-microscopic-history-response-20261023/precision-representation/prediction']
    for anchor_index,(label,offset,directory) in enumerate(zip(('warm','middle','cold'),contract['anchor_offsets'],locations)):
        anchor,unused=source.context(.875-offset/history_config['expansion_span'])
        assert np.array_equal(anchor.basis.mass,original.basis.mass)
        assert np.array_equal(anchor.epochs[0].frequency,original.epochs[0].frequency)
        probes=np.geomspace(1e-6,60,53)
        assert np.array_equal(anchor.basis.evaluate(probes),original.basis.evaluate(probes))
        for path in anchor.inputs:
            saved.register(inputs,path)
        for event in range(36):
            path=directory/(f'node-{event:02d}.npz' if anchor_index==0 else f'event-{event:02d}.npz')
            report=read(path.with_suffix('.json'))
            assert digest(path)==report['sha256'] and not report['failed_checks']
            values=packet(path)
            anchor_theta=float(values['theta'])
            assert abs(anchor_theta/(history_config['theta0']*math.exp(offset))-1)<1e-10
            node=json.loads(str(values['node']))
            assert node==microscopic.event_common.nodes(anchor_theta,14.)[event]
            parameters,weight=source.physics.parameters_and_weight(anchor_theta,node)
            assert weight==float(values['weight'])
            loop_path=Path(report['loop_path'])
            assert digest(loop_path)==report['loop_sha256']
            loop=read(loop_path)
            identity,key=loop_identity(parameters)
            assert loop['identity']==identity and loop['finite'] and np.isfinite(loop['scalar'])
            for file in (path,path.with_suffix('.json'),loop_path):
                saved.register(inputs,file)
            anchors.append(dict(anchor_index=anchor_index,label=label,event=event,theta=anchor_theta,node=node,
                                weight=weight,loop_path=str(loop_path),loop_sha256=digest(loop_path),
                                provenance_event=str(path),provenance_sha256=digest(path)))
    target=[]
    for event,node in enumerate(microscopic.event_common.nodes(theta,14.)):
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        inventory=cache_inventory(parameters)
        for match in inventory['matches']:
            saved.register(inputs,match['path'])
        target.append(dict(event=event,node=node,theta=theta,weight=weight,cache_inventory=inventory))
    assert len(target)==36 and len(anchors)==108
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
            implementation[str(Path(name).resolve())]=digest(name)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in bookmarks:
            archive.writestr(Path(name).name,Path(name).read_bytes())
    write(ROOT/'inputs.json',inputs)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=failed))
    assert not failed,failed
    frozen_hashes={str(path.relative_to(ROOT)):digest(path) for folder in ('frozen','histories') for path in (ROOT/folder).rglob('*') if path.is_file()}
    config=dict(stage=209,prepared_at=now(),turn_start='2026-10-25T03:26:06+00:00',
                safe_stop_utc='2026-10-25T06:50:00+00:00',
                parent_sha256=PARENT_SHA,target_fraction=fraction,theta=theta,offset=contract['target_offset'],
                anchor_offsets=contract['anchor_offsets'],operator_weights=weights,anchors=anchors,target=target,
                source_prediction_tolerance=.01,identity_tolerance=1e-10,history_mesh_tolerance=.01,
                protocol_hashes={name:digest(ROOT/name) for name in ('operator209.py','assess209.py','ACCEPTANCE.md','DERIVATION.md')},
                implementation_hashes=implementation,frozen_hashes=frozen_hashes,bookmarks=bookmarks,
                cache_scope='exact virtual identities in immediate child virtual-cache directories',
                target_cache_hits=sum(bool(row['cache_inventory']['matches']) for row in target),
                target_microscopic_global_nonuse_proven=False,prior_target_collision_operator_check_disclosed=True,
                prior_goal_turn='no progress: repeated saved Stage207 verification; now execute new physical-source test',
                original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
                frequency_weights_reapplied=False,maximum_event_workers=2,numerical_threads_per_worker=1)
    write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='histories_and_protocol_frozen',anchor_events_complete=0,target_events_complete=0))
    print(json.dumps(dict(state='prepared',history_checks=len(rows),inputs=len(inputs),anchor_inputs_reused=108,
                          target_cache_hits=config['target_cache_hits'],theta=theta)),flush=True)


def setup(config):
    original,theta=source.context(config['target_fraction'])
    assert theta==config['theta']
    histories={(model,grid):read(ROOT/f'histories/{model}-{grid}.json') for model in ('heavy','cold') for grid in GRIDS}
    bundle=previous.coefficient_bundle(original,histories)
    frozen=packet(ROOT/'frozen/history-coefficients.npz')
    assert np.array_equal(bundle.high,frozen['high']) and np.array_equal(bundle.low,frozen['low'])
    source.physics.precise_state=precise.precise_state
    return original,bundle,cached.models(bundle)


def event_path(kind,row):
    folder=ROOT/'anchors'/row['label'] if kind=='anchors' else ROOT/'target'
    return folder/f"event-{row['event']:02d}.npz"


def verify_event(path):
    record=read(path.with_suffix('.json'))
    assert digest(path)==record['sha256'] and not record['failed_checks'],str(path)
    assert digest(record['loop_path'])==record['loop_sha256']
    return packet(path),record


def verify_prediction(config):
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert manifest['configuration_sha256']==digest(ROOT/'configuration.json')
    for name,value in manifest['files'].items():
        assert digest(ROOT/name)==value,name
    for name,value in manifest['anchor_files'].items():
        assert digest(ROOT/name)==value,name
    return manifest


def run(kind,worker,seconds):
    config=protocol()
    manifest=verify_prediction(config) if kind=='target' else None
    original,bundle,evaluators=setup(config)
    selected=config['anchors'] if kind=='anchors' else config['target']
    began=time.monotonic()
    done=0
    for ordinal,row in enumerate(selected):
        if ordinal%2!=worker:
            continue
        path=event_path(kind,row)
        if path.exists():
            verify_event(path)
            continue
        if time.monotonic()-began>=seconds or datetime.now(timezone.utc)>=datetime.fromisoformat(config['safe_stop_utc']):
            break
        started=now()
        tick=time.monotonic()
        if manifest:
            assert datetime.fromisoformat(started)>datetime.fromisoformat(manifest['frozen_at'])
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight']
        if kind=='anchors':
            loop_path=Path(row['loop_path'])
            assert digest(loop_path)==row['loop_sha256']
            loop=read(loop_path)
            assert loop['identity']==loop_identity(parameters)[0]
            scalar,new_loop=loop['scalar'],False
        else:
            scalar,loop_path,new_loop=virtual(parameters)
        high,low,diagnostics=microscopic.weighted(parameters,bundle,evaluators,scalar,weight)
        checks=[]
        for name,value in diagnostics.items():
            check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
        check(checks,'shape',int(high.shape!=low.shape or high.shape!=(3,6,98,4)),0,'integrity')
        check(checks,'zero-history source exactly zero',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'negative_control')
        save(path,high=high,low=low,theta=row['theta'],weight=weight,node=json.dumps(row['node'],sort_keys=True))
        failed=[entry for entry in checks if not entry['passed']]
        write(path.with_suffix('.json'),dict(sha256=digest(path),checks=checks,failed_checks=failed,kind=kind,
              started_at=started,finished_at=now(),seconds=time.monotonic()-tick,worker=worker,
              loop_path=str(loop_path),loop_sha256=digest(loop_path),new_virtual_integral=new_loop,
              coefficients_sha256=digest(ROOT/'frozen/history-coefficients.npz')))
        done+=1
        write(ROOT/f'workers/{kind}-{worker}.json',dict(state='running',completed_this_call=done,last_event=row['event'],
                                                      label=row.get('label','target'),updated_at=now()))
        print(json.dumps(dict(kind=kind,label=row.get('label','target'),worker=worker,event=row['event'],
                              seconds=time.monotonic()-tick,failed_checks=len(failed))),flush=True)
        assert not failed,failed
    write(ROOT/f'workers/{kind}-{worker}.json',dict(state='stopped',completed_this_call=done,stopped_at=now()))


def freeze():
    config=protocol()
    assert not (ROOT/'frozen/prediction-manifest.json').exists()
    assert not list((ROOT/'target').glob('event-*.npz'))
    pairs=[]
    anchor_hashes={}
    for event in range(36):
        anchors=[]
        for label in ('warm','middle','cold'):
            path=ROOT/f'anchors/{label}/event-{event:02d}.npz'
            values,record=verify_event(path)
            assert not record['new_virtual_integral']
            assert record['coefficients_sha256']==digest(ROOT/'frozen/history-coefficients.npz')
            for file in (path,path.with_suffix('.json')):
                anchor_hashes[str(file.relative_to(ROOT))]=digest(file)
            anchors.append((values['high'],values['low']))
        prediction=previous.weighted_sum(anchors,config['operator_weights'])
        assert np.max(abs(prediction[0][-1]))+np.max(abs(prediction[1][-1]))==0
        save(ROOT/f'frozen/prediction/event-{event:02d}.npz',high=prediction[0],low=prediction[1])
        pairs.append(prediction)
    total=metrics.primitives(pairs)
    save(ROOT/'frozen/predicted-node.npz',high=total[0],low=total[1])
    hashes={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen/prediction').glob('*.npz')}
    hashes['frozen/predicted-node.npz']=digest(ROOT/'frozen/predicted-node.npz')
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_at=now(),configuration_sha256=digest(ROOT/'configuration.json'),
          files=hashes,anchor_files=anchor_hashes,direct_target_evaluations_at_freeze=0,frequency=14.,events=36))
    write(ROOT/'progress.json',dict(state='prediction_frozen',anchor_events_complete=108,target_events_complete=0))
    print(json.dumps(dict(state='prediction_frozen',events=36,anchor_events=108,frozen_files=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','anchors','freeze','target'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=5400)
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare()
    elif args.phase=='freeze':
        freeze()
    else:
        run(args.phase,args.worker,args.seconds)

