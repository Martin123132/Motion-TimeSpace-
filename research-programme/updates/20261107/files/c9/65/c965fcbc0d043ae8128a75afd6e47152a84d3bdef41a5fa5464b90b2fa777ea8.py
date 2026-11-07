from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,time,zipfile
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'history-aware-upper-outer-temperature-test-20261025'
PARENT_SHA='03003e31f54fdd6deb37b9d145ad5593f865100ebf088f03bdeac2d001501fc8'
FREQUENCIES=[19.694647474056552]
sys.path.insert(0,str(BRANCH/'history-aware-operator-temperature-test-20261025'))
import operator209 as core
core.ROOT=ROOT
foundation=core.previous
np,mp,linear=core.np,core.mp,core.linear
source,microscopic,saved=core.source,core.microscopic,core.saved
read,write,packet,save,digest,check=core.read,core.write,core.packet,core.save,core.digest,core.check
metrics=core.metrics
COMPONENTS,GRIDS=core.COMPONENTS,core.GRIDS
protocol,setup,verify_event=core.protocol,core.setup,core.verify_event
cache_inventory,virtual,loop_identity=core.cache_inventory,core.virtual,core.loop_identity
verify_prediction,now=core.verify_prediction,core.now


def event_path(kind,row):
    folder=ROOT/kind/f"frequency-{row['frequency_index']}"
    if kind=='anchors':
        folder=folder/row['label']
    return folder/f"event-{row['event']:02d}.npz"


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['nodes_and_six_frequency_qualified'] and not parent['full_band']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    parent_config=read(PARENT/'configuration.json')
    original,theta=source.context(parent_config['target_fraction'])
    assert theta==parent_config['theta']
    for path in original.inputs:
        saved.register(inputs,path)
    rows=[dict(row,name='reused history:'+row['name']) for row in read(PARENT/'results/preparation.json')['checks']]
    for name in ('frozen/history-coefficients.npz','histories/heavy-half.json','histories/heavy-quarter.json',
                 'histories/cold-half.json','histories/cold-quarter.json'):
        destination=ROOT/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        assert not destination.exists()
        destination.write_bytes((PARENT/name).read_bytes())
        check(rows,name+':identical reuse',int(digest(destination)!=digest(PARENT/name)),0,'integrity')
    reference_path=PARENT/'results/source-sum-6.npz'
    reference=packet(reference_path)
    assert float(reference['theta'])==theta and list(reference['frequencies'])==parent_config['coverage']
    assert reference['actual_high'].shape==reference['predicted_high'].shape==(3,6,98,4)
    reference_paths=[
        BRANCH/'history-aware-operator-temperature-test-20261025/results/source-node.npz',
        BRANCH/'history-aware-neighbour-temperature-test-20261025/results/source-node.npz',
        BRANCH/'history-aware-lower-pair-temperature-test-20261025/results/source-node-2.npz',
        BRANCH/'history-aware-lower-pair-temperature-test-20261025/results/source-node-1.npz',
        PARENT/'results/source-node-5.npz',
        PARENT/'results/source-node-0.npz']
    reference_leaves=[]
    replay={'actual':[],'predicted':[]}
    for path in reference_paths:
        assert str(path) in inputs and digest(path)==inputs[str(path)]
        values=packet(path)
        frequencies=np.atleast_1d(values['frequencies'] if 'frequencies' in values else values['frequency'])
        assert frequencies.shape==(1,) and float(values['theta'])==theta
        assert np.array_equal(values['components'],reference['components'])
        coefficients=path.parent.parent/'frozen/history-coefficients.npz'
        assert digest(coefficients)==digest(ROOT/'frozen/history-coefficients.npz')
        saved.register(inputs,coefficients)
        reference_leaves.append(dict(path=str(path),sha256=digest(path),frequency=float(frequencies[0]),
                                     coefficients_path=str(coefficients),coefficients_sha256=digest(coefficients)))
        for label in replay:
            replay[label].append((values[label+'_high'],values[label+'_low']))
    assert [row['frequency'] for row in reference_leaves]==parent_config['coverage']
    factor=linear.cholesky(original.basis.mass,lower=True)
    for label,pairs in replay.items():
        combined=metrics.primitives(pairs)
        expected=(reference[label+'_high'],reference[label+'_low'])
        error=metrics.subtract(combined,expected)
        for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
            relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(expected[0][:2]+expected[1][:2]),1e-300)
            check(rows,label+':six independent leaves replay '+name,relative.max(),1e-10,'identity')
    panel=parent_config['original_panel']
    actual_panel=sorted({(node['frequency'],node['seed_weight']) for node in source.physics.integration_nodes(theta,7) if 8.<node['frequency']<20.})
    assert actual_panel==[(row['frequency'],row['seed_weight']) for row in panel]
    assert sorted(parent_config['coverage']+FREQUENCIES)==[row['frequency'] for row in panel]
    check(rows,'original quadrature weight sum',sum(row['seed_weight'] for row in panel)-12,1e-13,'identity')
    cold_paths=(*foundation.prior.LEAVES,foundation.PARENT/'results/neighbour-source.npz')
    cold_roots={foundation.prior.leaf_frequency(path):path.parent.parent for path in cold_paths}
    anchors=[]
    targets=[]
    for frequency in FREQUENCIES:
        frequency_index=next(index for index,row in enumerate(panel) if row['frequency']==frequency)
        for anchor_index,label in enumerate(('warm','middle','cold')):
            anchor_theta=next(row['theta'] for row in parent_config['anchors'] if row['label']==label)
            for event,node in enumerate(microscopic.event_common.nodes(anchor_theta,frequency)):
                parameters,weight=source.physics.parameters_and_weight(anchor_theta,node)
                provenance={}
                if label in ('warm','cold'):
                    path=(foundation.WARM/f'events/frequency-{frequency_index}/node-{event:02d}.npz' if label=='warm'
                          else cold_roots[frequency]/f'prediction/event-{event:02d}.npz')
                    report=read(path.with_suffix('.json'))
                    values=packet(path)
                    assert digest(path)==report['sha256'] and not report['failed_checks']
                    assert float(values['theta'])==anchor_theta and float(values['weight'])==weight
                    assert json.loads(str(values['node']))==node
                    loop_path=Path(report['loop_path'])
                    assert digest(loop_path)==report['loop_sha256']
                    assert read(loop_path)['identity']==loop_identity(parameters)[0]
                    for file in (path,path.with_suffix('.json'),loop_path):
                        saved.register(inputs,file)
                    provenance=dict(path=str(path),sha256=digest(path),role='kinematics and exact virtual input only')
                inventory=cache_inventory(parameters)
                for match in inventory['matches']:
                    saved.register(inputs,match['path'])
                anchors.append(dict(frequency_index=frequency_index,frequency=frequency,anchor_index=anchor_index,
                                    label=label,event=event,node=node,theta=anchor_theta,weight=weight,
                                    cache_inventory=inventory,provenance=provenance))
        for event,node in enumerate(microscopic.event_common.nodes(theta,frequency)):
            parameters,weight=source.physics.parameters_and_weight(theta,node)
            inventory=cache_inventory(parameters)
            for match in inventory['matches']:
                saved.register(inputs,match['path'])
            targets.append(dict(frequency_index=frequency_index,frequency=frequency,event=event,node=node,
                                theta=theta,weight=weight,cache_inventory=inventory))
    assert len(anchors)==108 and len(targets)==36
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
    config=dict(stage=213,prepared_at=now(),turn_start='2026-10-25T14:03:01+00:00',
                safe_stop_utc='2026-10-25T17:40:00+00:00',parent_sha256=PARENT_SHA,
                target_fraction=parent_config['target_fraction'],theta=theta,offset=parent_config['offset'],
                anchor_offsets=parent_config['anchor_offsets'],operator_weights=parent_config['operator_weights'],
                frequencies=FREQUENCIES,reference_frequencies=parent_config['coverage'],
                coverage=parent_config['coverage']+FREQUENCIES,original_panel=panel,
                anchors=anchors,target=targets,source_prediction_tolerance=.01,identity_tolerance=1e-10,history_mesh_tolerance=.01,
                protocol_hashes={name:digest(ROOT/name) for name in ('operator213.py','assess213.py','ACCEPTANCE.md','DERIVATION.md')},
                implementation_hashes=implementation,frozen_hashes=frozen_hashes,bookmarks=bookmarks,
                anchor_cache_hits=sum(bool(row['cache_inventory']['matches']) for row in anchors),
                target_cache_hits=sum(bool(row['cache_inventory']['matches']) for row in targets),
                reference_source_path=str(reference_path),reference_source_sha256=digest(reference_path),reference_leaves=reference_leaves,
                cache_scope='exact identities in immediate child virtual-cache directories',
                target_temperature_prior_frequencies_exposed=parent_config['coverage'],global_target_nonuse_proven=False,
                prior_goal_turn='progress: Stage212 upper/outer nodes and six-frequency sum qualified',
                original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
                frequency_weights_reapplied=False,partial_panel_normalized=False,maximum_event_workers=2,numerical_threads_per_worker=1)
    write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='histories_and_protocol_frozen',anchor_events_complete=0,target_events_complete=0))
    print(json.dumps(dict(state='prepared',frequencies=FREQUENCIES,checks=len(rows),inputs=len(inputs),
                          anchor_cache_hits=config['anchor_cache_hits'],target_cache_hits=config['target_cache_hits'])),flush=True)


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
        scalar,loop_path,new_loop=virtual(parameters)
        if row['cache_inventory']['matches']:
            assert not new_loop
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
              frequency_index=row['frequency_index'],started_at=started,finished_at=now(),seconds=time.monotonic()-tick,worker=worker,
              loop_path=str(loop_path),loop_sha256=digest(loop_path),new_virtual_integral=new_loop,
              coefficients_sha256=digest(ROOT/'frozen/history-coefficients.npz')))
        done+=1
        write(ROOT/f'workers/{kind}-{worker}.json',dict(state='running',completed_this_call=done,last_event=row['event'],
              frequency_index=row['frequency_index'],label=row.get('label','target'),updated_at=now()))
        print(json.dumps(dict(kind=kind,frequency=row['frequency'],label=row.get('label','target'),worker=worker,
              event=row['event'],seconds=time.monotonic()-tick,failed_checks=len(failed),new_virtual_integral=new_loop)),flush=True)
        assert not failed,failed
    write(ROOT/f'workers/{kind}-{worker}.json',dict(state='stopped',completed_this_call=done,stopped_at=now()))


def freeze():
    config=protocol()
    assert not (ROOT/'frozen/prediction-manifest.json').exists()
    assert not list((ROOT/'target').rglob('event-*.npz'))
    assert digest(config['reference_source_path'])==config['reference_source_sha256']
    reference=packet(config['reference_source_path'])
    cumulative=(reference['predicted_high'],reference['predicted_low'])
    anchor_hashes={}
    for ordinal,frequency in enumerate(config['frequencies']):
        frequency_index=next(row['frequency_index'] for row in config['target'] if row['frequency']==frequency)
        pairs=[]
        for event in range(36):
            anchors=[]
            for label in ('warm','middle','cold'):
                path=ROOT/f'anchors/frequency-{frequency_index}/{label}/event-{event:02d}.npz'
                values,record=verify_event(path)
                assert record['coefficients_sha256']==digest(ROOT/'frozen/history-coefficients.npz')
                for file in (path,path.with_suffix('.json')):
                    anchor_hashes[str(file.relative_to(ROOT))]=digest(file)
                anchors.append((values['high'],values['low']))
            prediction=foundation.weighted_sum(anchors,config['operator_weights'])
            assert np.max(abs(prediction[0][-1]))+np.max(abs(prediction[1][-1]))==0
            save(ROOT/f'frozen/prediction/frequency-{frequency_index}/event-{event:02d}.npz',high=prediction[0],low=prediction[1])
            pairs.append(prediction)
        total=metrics.primitives(pairs)
        save(ROOT/f'frozen/predicted-node-{frequency_index}.npz',high=total[0],low=total[1])
        cumulative=metrics.primitives([cumulative,total])
        save(ROOT/f'frozen/predicted-sum-{ordinal+7}.npz',high=cumulative[0],low=cumulative[1])
    hashes={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen').rglob('*.npz')}
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_at=now(),configuration_sha256=digest(ROOT/'configuration.json'),
          files=hashes,anchor_files=anchor_hashes,direct_new_frequency_evaluations_at_freeze=0,frequencies=FREQUENCIES,
          events=36,reference_source_sha256=config['reference_source_sha256'],coverage=config['coverage']))
    write(ROOT/'progress.json',dict(state='predictions_frozen',anchor_events_complete=108,target_events_complete=0))
    print(json.dumps(dict(state='predictions_frozen',events=36,anchor_events=108,frozen_files=len(hashes),coverage=config['coverage'])),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','anchors','freeze','target'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=10800)
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare()
    elif args.phase=='freeze':
        freeze()
    else:
        run(args.phase,args.worker,args.seconds)

