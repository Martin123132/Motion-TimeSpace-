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
PARENT=BRANCH/'collision-operator-lift-pilot-20261025'
SOURCE=BRANCH/'history-aware-complete-band-temperature-test-20261025'
PARENT_SHA='5f732a56e0700ddee8dced19038d1a801a4cd511b16e569d77bc98ff8b1ab515'
sys.path.insert(0,str(PARENT))
import lift214 as lift
import node214 as helpers
import collision_operator as api
np,mp,linear=lift.np,lift.mp,lift.linear
source,metrics=lift.source,lift.metrics
read,write,packet,save,digest,check=lift.read,lift.write,lift.packet,lift.save,lift.digest,lift.check
COMPONENTS,ACTIVE=lift.COMPONENTS,lift.ACTIVE
LABELS=('warm','middle','cold')


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['full_node_qualified'] and parent['current_failures']==0
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    previous=read(SOURCE/'configuration.json')
    events=[]
    for row in previous['anchors']:
        report_path=SOURCE/f"anchors/frequency-6/{row['label']}/event-{row['event']:02d}.json"
        report=read(report_path)
        direct_path=report_path.with_suffix('.npz')
        assert not report['failed_checks']
        assert digest(direct_path)==report['sha256'] and digest(report['loop_path'])==report['loop_sha256']
        events.append(dict(**row,source_path=str(direct_path),source_sha256=report['sha256'],
                           loop_path=report['loop_path'],loop_sha256=report['loop_sha256']))
    assert len(events)==108
    original,theta=source.context(previous['target_fraction'])
    assert theta==previous['theta']
    for name in ('history-coefficients.npz','basis-metric.npz'):
        path=PARENT/'frozen'/name
        destination=ROOT/'frozen'/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(path.read_bytes())
    basis=packet(ROOT/'frozen/basis-metric.npz')
    assert np.array_equal(basis['mass'],original.basis.mass)
    inputs.update({str(path):digest(path) for path in original.inputs})
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            path=Path(name).resolve()
            implementation[str(path)]=digest(path)
            inputs[str(path)]=digest(path)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in bookmarks:
            archive.writestr(Path(path).name,Path(path).read_bytes())
    config=dict(stage=215,turn_start='2026-10-25T17:33:54+00:00',prepared_at=now(),
          safe_stop_utc='2026-10-25T21:10:00+00:00',target_fraction=previous['target_fraction'],theta=theta,
          events=events,operator_weights=previous['operator_weights'],anchor_offsets=previous['anchor_offsets'],
          anchor_thetas={label:next(row['theta'] for row in events if row['label']==label) for label in LABELS},
          target_operator_path=str(PARENT/'precision-repair/results/operator-node.npz'),
          target_operator_sha256=digest(PARENT/'precision-repair/results/operator-node.npz'),
          target_source_path=str(SOURCE/'results/source-node-6.npz'),
          target_source_sha256=digest(SOURCE/'results/source-node-6.npz'),
          coefficients_sha256=digest(ROOT/'frozen/history-coefficients.npz'),
          basis_sha256=digest(ROOT/'frozen/basis-metric.npz'),bookmarks=bookmarks,implementation=implementation,
          maximum_workers=2,numerical_threads=1,replay_not_new_holdout=True,
          protocol_hashes={name:digest(ROOT/name) for name in ('bridge215.py','ACCEPTANCE.md','DERIVATION.md')})
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='prepared',events_complete=0))
    print(json.dumps(dict(state='prepared',events=108,new_virtual_integrals_required=0,inputs=len(inputs))),flush=True)


def event_path(row):
    return ROOT/f"events/{row['label']}/event-{row['event']:02d}.npz"


def verify_event(row):
    path=event_path(row)
    report=read(path.with_suffix('.json'))
    assert digest(path)==report['sha256'] and not report['failed_checks']
    assert report['loop_sha256']==row['loop_sha256']
    values=packet(path)
    assert values['high'].shape==values['low'].shape==(6,98,97,2)
    assert float(values['theta'])==row['theta'] and float(values['weight'])==row['weight']
    return values,report


def run(worker,seconds):
    config=protocol()
    for name,value in config['implementation'].items():
        assert digest(name)==value,name
    original,theta=source.context(config['target_fraction'])
    bundle,models=api.evaluators(original)
    began=time.monotonic()
    done=0
    for ordinal,row in enumerate(config['events']):
        if ordinal%2!=worker:
            continue
        path=event_path(row)
        if path.exists():
            verify_event(row)
            continue
        if time.monotonic()-began>=seconds or datetime.now(timezone.utc)>=datetime.fromisoformat(config['safe_stop_utc']):
            break
        started=now();tick=time.monotonic()
        parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
        assert weight==row['weight'] and digest(row['loop_path'])==row['loop_sha256']
        loop=read(row['loop_path'])
        assert loop['finite'] and loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        matrix,diagnostics=api.evaluate_event(parameters,bundle,models,loop['scalar'],weight)
        checks=[]
        for name,value in diagnostics.items():
            check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not all(np.isfinite(values).all() for values in matrix)),0,'integrity')
        save(path,high=matrix[0],low=matrix[1],theta=row['theta'],weight=weight)
        failed=[row for row in checks if not row['passed']]
        report=dict(sha256=digest(path),checks=checks,failed_checks=failed,worker=worker,
            started_at=started,finished_at=now(),seconds=time.monotonic()-tick,
            loop_path=row['loop_path'],loop_sha256=row['loop_sha256'],new_virtual_integrals=0,
            scalar_precision=60,protected_precision=80)
        write(path.with_suffix('.json'),report)
        done+=1
        write(ROOT/f'workers/{worker}.json',dict(state='running',last_label=row['label'],last_event=row['event'],done=done,pid=os.getpid(),updated_at=now()))
        print(json.dumps(dict(label=row['label'],event=row['event'],seconds=report['seconds'],failed=len(failed))),flush=True)
        assert not failed,failed
    import psutil
    memory=psutil.Process().memory_info()
    write(ROOT/f'workers/{worker}.json',dict(state='stopped',completed_this_call=done,
        peak_working_set_bytes=getattr(memory,'peak_wset',memory.rss),stopped_at=now()))
    print(json.dumps(dict(worker=worker,completed_this_call=done)),flush=True)


def contract_histories(matrix,coefficients):
    outputs=[np.zeros((6,98,12)),np.zeros((6,98,12))]
    for join in range(2):
        columns=list(range(join,12,2))
        active=(coefficients['high'][np.ix_(ACTIVE,columns)],coefficients['low'][np.ix_(ACTIVE,columns)])
        result=api.apply_coefficients(matrix,active,join)
        for index in range(2):
            outputs[index][:,:,columns]=result[index]
    return tuple(np.moveaxis(values.reshape(6,98,3,4),2,0) for values in outputs)


def weighted_matrix(pairs,weights):
    high=np.zeros_like(pairs[0][0]);low=np.zeros_like(high)
    with mp.workdps(80):
        factors=list(map(mp.mpf,weights))
        for index in np.ndindex(high.shape):
            exact=mp.fsum(factor*(mp.mpf(float(pair[0][index]))+mp.mpf(float(pair[1][index]))) for pair,factor in zip(pairs,factors))
            high[index]=float(exact)
            low[index]=float(exact-mp.mpf(float(exact)))
    return high,low


def freeze():
    config=protocol()
    assert not (ROOT/'frozen/prediction-manifest.json').exists()
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    assert digest(ROOT/'frozen/history-coefficients.npz')==config['coefficients_sha256']
    operators=[];hashes={}
    for label in LABELS:
        matrices=[]
        for row in [row for row in config['events'] if row['label']==label]:
            values,report=verify_event(row)
            pair=(values['high'],values['low'])
            matrices.append(pair)
            for path in (event_path(row),event_path(row).with_suffix('.json')):
                hashes[str(path.relative_to(ROOT))]=digest(path)
            prediction=contract_histories(pair,coefficients)
            path=ROOT/f"frozen/replay/{label}/event-{row['event']:02d}.npz"
            save(path,high=prediction[0],low=prediction[1])
            hashes[str(path.relative_to(ROOT))]=digest(path)
        total=api.sum_events(matrices)
        operators.append(total)
        path=ROOT/f'results/operator-{label}.npz'
        save(path,high=total[0],low=total[1],theta=config['anchor_thetas'][label])
        hashes[str(path.relative_to(ROOT))]=digest(path)
        prediction=contract_histories(total,coefficients)
        path=ROOT/f'frozen/source-{label}.npz'
        save(path,high=prediction[0],low=prediction[1])
        hashes[str(path.relative_to(ROOT))]=digest(path)
    prediction=weighted_matrix(operators,config['operator_weights'])
    path=ROOT/'frozen/predicted-operator.npz'
    save(path,high=prediction[0],low=prediction[1],theta=config['theta'])
    hashes[str(path.relative_to(ROOT))]=digest(path)
    source_prediction=contract_histories(prediction,coefficients)
    path=ROOT/'frozen/predicted-source.npz'
    save(path,high=source_prediction[0],low=source_prediction[1])
    hashes[str(path.relative_to(ROOT))]=digest(path)
    hashes['frozen/history-coefficients.npz']=config['coefficients_sha256']
    hashes['frozen/basis-metric.npz']=config['basis_sha256']
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_at=now(),files=hashes,
        configuration_sha256=digest(ROOT/'configuration.json'),replay_not_new_holdout=True,
        target_temperature_previously_tested=True,unchanged_weights=True))
    write(ROOT/'progress.json',dict(state='operator_predictions_frozen',events_complete=108))
    print(json.dumps(dict(state='operator_predictions_frozen',events=108,files=len(hashes))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run','freeze'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=10500)
    args=parser.parse_args()
    if args.phase=='run':
        run(args.worker,args.seconds)
    else:
        {'prepare':prepare,'freeze':freeze}[args.phase]()
