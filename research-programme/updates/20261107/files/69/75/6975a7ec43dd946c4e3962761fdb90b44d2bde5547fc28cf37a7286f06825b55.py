import os

for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[variable]='1'

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil
import run_final_real_directions as original
import run_stable_absorption_pair as stable


ROOT=Path(__file__).resolve().parent
CAMPAIGN=ROOT/'legacy-stable-reconciliation-rays000-002'
CURRENT=ROOT/'final-stable-real-batch-rays025-026'
read,digest,verify=original.read,original.digest,original.verify
require,write,now=stable.require,stable.write,stable.now
RAYS=(0,1,2)
ORDERS=(18,26)


def homes(ray):
    return (ROOT/f'final-epoch-real-source-ray{ray:03d}',ROOT/f'final-epoch-real-v2-ray{ray:03d}',
            ROOT/f'final-absorption-native-v2-ray{ray:03d}',
            ROOT/('compensated-epoch-source-final450-001' if ray==0 else f'compensated-epoch-source-final450-ray{ray:03d}'))


def guard():
    require(not stopping(),'Time, owner, Music Lab or storage hold; no automatic retry')


def stopping():
    folders=[ROOT,ROOT.parent,CAMPAIGN,CURRENT,ROOT/'final-epoch-kinematic-bank',ROOT/'saved-epoch-cell450']
    for ray in RAYS:
        folders.extend(homes(ray))
    return (datetime.now(timezone.utc)>=deadline or 3<=datetime.now(ZoneInfo('Europe/London')).hour<14
            or any((folder/'STOP-REQUESTED').exists() for folder in folders)
            or (ROOT.parent/'execution-v3/STOP-REQUEST.json').exists() or shutil.disk_usage(ROOT).free<10*1024**3)


def fixed():
    inputs={str(ROOT/name):value for name,value in {**stable.FROZEN,**original.PARENTS}.items()}
    inputs.update({str(Path(stable.__file__)):'c8a7b53df118e23fcae5c74ab6346869a16bfec2e1125b9ac0a813a71dfd6d3a',
                   str(ROOT/'verify_stable_real_pair_003_004.py'):'249942eec79ad3828d9ab9141f621a40dc277d785f2a9a4cd4397d6398b994ef',
                   str(ROOT/'check_real_pair_023_024_reflection.py'):'34c4a8894612f1bf25d85aec28c634cdfa3a7bcf098e721e706c55103946df13'})
    for name in ('reconcile_legacy_real_sources.py','verify_legacy_real_reconciliation.py','LEGACY-REAL-RECONCILIATION-PREDICTION.md'):
        inputs[str(ROOT/name)]=digest(ROOT/name)
    return inputs


def render(stage,ray):
    source,meta=stable.render(stage,ray)
    precise,changes=original.qualification_source('precise',ray)
    if ray==0:
        source=source.replace('compensated-epoch-source-final450-ray000','compensated-epoch-source-final450-001')
        precise=precise.replace('compensated-epoch-source-final450-ray000','compensated-epoch-source-final450-001')
    if stage=='run':
        hook='from stable_absorption_panel import panel_action'
        require(source.count(hook)==1,'Stable panel hook changed')
        source=source.replace(hook,'panel_action=qualified_panel_action')
    meta.update(ray=ray,adapter=str(Path(__file__)),adapter_sha256=digest(__file__),transformed_sha256=hashlib.sha256(source.encode()).hexdigest(),
                precise_setup=dict(transformed_sha256=hashlib.sha256(precise.encode()).hexdigest(),replacements=changes),
                scope='Same stable action, exact old-panel replay, original grid; copy unaffected prefix, recompute suffix')
    return compile(source,str(ROOT/meta['original_program']['parent']),'exec'),precise,meta


def seed(ray):
    old,new,_,_=homes(ray)
    before,after=read(old/'protocol.json'),read(new/'protocol.json')
    for field in ('panels','labels','history_cell','coordinate','theta','event','angular_ray','angular_order','angular_weight','event_weight','gate','source_refinement_budget'):
        require(before[field]==after[field],'Original setup differs: '+field)
    verify(before['inputs']); verify(after['inputs'])
    for order in ORDERS:
        panels=before['panels'][str(order)]
        changed=[index for index,panel in enumerate(panels) if panel['absorption'] and not panel['emission']]
        require(len(panels)==41 and changed==[35,36],'Unqualified panel layout')
        job=old/f'order-{order}'; destination=new/job.name
        destination.mkdir()
        previous=digest(old/'protocol.json'); target_previous=digest(new/'protocol.json')
        for index in range(changed[0]):
            guard()
            path=job/f'panel-{index:03d}.json'; target=destination/path.name
            record=read(path)
            require(record['passed'] and all(row['passed'] for row in record['checks']) and record['previous_sha256']==previous
                    and record['order']==order and record['panel']==index and digest(path.with_suffix('.npz'))==record['packet_sha256'], 'Bad old prefix')
            with path.with_suffix('.npz').open('rb') as initial,target.with_suffix('.npz').open('xb') as copied:
                shutil.copyfileobj(initial,copied)
            require(digest(target.with_suffix('.npz'))==record['packet_sha256'],'Prefix copy differs')
            previous=digest(path)
            write(target,dict(record,previous_sha256=target_previous,reused_from=str(path),original_metadata_sha256=previous,
                              reuse_reason='Identical original branch before first absorption-only panel; independent byte copy'))
            target_previous=digest(target)
    write(new/'prefix-reuse.json',dict(panels=35,orders=list(ORDERS),source=str(old),source_protocol=digest(old/'protocol.json'),
                                      target_protocol=digest(new/'protocol.json'),affected_panels_copied=False,finished=now()))


def stage_work(stage,ray,order):
    if stage=='seed':
        seed(ray)
        return
    program,precise,adaptation=render(stage,ray)
    old,new,_,_=homes(ray)
    captured=[]
    packets={}
    def cached_owner(parameters,direction):
        from exact_kinematic_cache import CachedDirection
        path=ROOT/f'final-epoch-kinematic-bank/ray-{ray:03d}.json'; record=read(path)
        require(record['passed'] and record['ray']==ray and record['protocol_sha256']==digest(path.with_name('protocol.json'))
                and all(row['passed'] for row in record['checks']),'Original cache required')
        return CachedDirection(parameters,direction,path.with_name(f'ray-{ray:03d}-kernel.json'),record['kernel_sha256'])
    def panel_with_replay(factors,frequency,measure,densities,factor_data,mode,join,degree,event_weight,angular_weight,emission,absorption):
        import numpy as np
        from full_tail_action import panel_action as old_panel
        from stable_absorption_panel import panel_action as stable_panel
        matches=[panel['panel'] for panel in frozen_panels if np.array_equal(panel['frequencies'],frequency)
                 and np.array_equal(panel['measures'],measure) and (panel['emission'],panel['absorption'])==(emission,absorption)]
        require(len(matches)==1 and matches[0]>=35,'Replayed wrong original nodes/weights')
        index=matches[0]; key=f'{mode}:join{join}:l{degree}:actions'
        if index not in packets:
            path=old/f'order-{order}'/f'panel-{index:03d}.npz'
            require(digest(path)==read(path.with_suffix('.json'))['packet_sha256'],'Original packet changed')
            with np.load(path,allow_pickle=False) as packet:
                packets[index]={name[6:]:packet[name] for name in packet.files if name.startswith('point:') and name.endswith(':actions')}
        args=(factors,frequency,measure,densities,factor_data,mode,join,degree,event_weight,angular_weight,emission,absorption)
        updated=stable_panel(*args)
        baseline=old_panel(*args) if index in (35,36) else updated
        reference=packets[index][key]
        require(baseline.dtype==reference.dtype==np.float64 and np.array_equal(baseline.view(np.uint64),reference.view(np.uint64)),
                f'Original array not reproduced: ray{ray} order{order} panel{index} {key}')
        captured.append(dict(panel=index,key=key,bitwise_original=True,changed_values=int(np.count_nonzero(updated!=reference)),
                             maximum_absolute_change=float(np.max(np.abs(updated-reference)))))
        return updated
    if stage=='run':
        frozen_panels=read(old/'protocol.json')['panels'][str(order)]
    arguments={'native':[],'freeze':['freeze','--stop-utc',options.stop_utc],
               'run':['run','--order',str(order),'--panels','8','--minutes','25','--stop-utc',options.stop_utc],
               'check':['--order',str(order)],'compare':[]}
    sys.argv=[str(Path(__file__)),*arguments[stage]]
    context=dict(__file__=str(Path(__file__)),__name__='legacy_qualified_stable',ADAPTATION=adaptation,adapter_guard=guard,
                 adapter_stopping=stopping,endpoint_guard=guard,cached_owner=cached_owner,qualified_cached_owner=cached_owner,
                 endpoint_source_text=lambda *unused:precise,repair_inputs=lambda:read(CAMPAIGN/'protocol.json')['inputs'],
                 qualified_panel_action=panel_with_replay)
    try:
        exec(program,context)
    except SystemExit as error:
        if error.code not in (None,0):
            raise
    if stage=='run':
        require(read(new/f'order-{order}/complete.json')['passed'] and len(captured)==72
                and len({(row['panel'],row['key']) for row in captured})==72,'Incomplete suffix replay')
        write(new/f'order-{order}/original-replay.json',dict(order=order,ray=ray,rows=captured,finished=now(),passed=True))


def batch():
    guard()
    accepted=read(CURRENT/'integrity.json')
    require(accepted['passed'] and sorted(map(int,accepted['coverage']))==list(range(27)) and read(CURRENT/'reflection.json')['passed'],
            'Verified pair through 26 and completed mirror check required')
    protected=dict(read(CURRENT/'protocol.json')['protected'])
    for name in ('protocol.json','end.json','integrity.json','reflection.json','reflection-rows.csv'):
        protected[str(CURRENT/name)]=digest(CURRENT/name)
    for ray in RAYS:
        old,new,native,qual=homes(ray)
        require(not new.exists() and not native.exists(),'Existing reconciliation preserved')
        require(read(qual/'prediction.json')['angular_ray']==ray and read(qual/'validation.json')['passed'],'Original oracle required')
        base_protocol=digest(old/'protocol.json')
        for order in ORDERS:
            job=old/f'order-{order}'; previous=base_protocol
            for index in range(41):
                guard()
                path=job/f'panel-{index:03d}.json'; record=read(path)
                require(record['passed'] and record['panel']==index and record['order']==order and record['previous_sha256']==previous
                        and all(row['passed'] for row in record['checks']), 'Original panel chain')
                previous=digest(path)
                protected[str(path)],protected[str(path.with_suffix('.npz'))]=previous,record['packet_sha256']
            require(previous==read(job/'complete.json')['last_panel_sha256'] and read(job/'independent.json')['passed'],'Original endpoint chain')
    verify(protected)
    inputs=fixed(); verify(inputs)
    CAMPAIGN.mkdir()
    write(CAMPAIGN/'protocol.json',dict(started=now(),stop_utc=options.stop_utc,rays=list(RAYS),inputs=inputs,protected=protected,
          process=identity,order=list(ORDERS),panels_per_job=8,identity_gate=1e-10,refinement_gate=.002,max_active_numerical_workers=1,
          previous_coverage_sha256=digest(CURRENT/'integrity.json'),changed_panels=[35,36],prefix=35))
    runs=[]; completed=[]; failure=None
    def child(stage,ray,order=None):
        guard();verify(inputs)
        label=f'{len(runs)+1:03d}-ray{ray:03d}-{stage}'
        command=[sys.executable,'-B',str(Path(__file__)),stage,'--ray',str(ray),'--stop-utc',options.stop_utc]
        if order:
            command.extend(['--order',str(order)])
        with (CAMPAIGN/(label+'.stdout.log')).open('x') as stdout,(CAMPAIGN/(label+'.stderr.log')).open('x') as stderr:
            with subprocess.Popen(command,stdout=stdout,stderr=stderr,cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW) as worker:
                entry=dict(label=label,ray=ray,stage=stage,pid=worker.pid,created_time=psutil.Process(worker.pid).create_time(),command=command,started=now())
                write(CAMPAIGN/(label+'.start.json'),entry)
                print(json.dumps(dict(started=label,pid=worker.pid)),flush=True)
                code=worker.wait()
        entry.update(actual_exit_code=code,finished=now())
        runs.append(entry); write(CAMPAIGN/(label+'.end.json'),entry)
        print(json.dumps(dict(finished=label,exit_code=code)),flush=True)
        require(code==0,'Stopped at '+label+'; do not retry automatically')
    try:
        for ray in RAYS:
            _,directory,native,_=homes(ray)
            child('native',ray);require(read(native/'validation.json')['passed'],'Stable native qualification failed')
            child('freeze',ray);child('seed',ray)
            for order in ORDERS:
                child('run',ray,order);child('check',ray,order)
                require(read(directory/f'order-{order}/independent.json')['passed'],'Independent check failed')
            child('compare',ray)
            result=directory/'order18-vs26.json'
            require(read(result)['all_component_rows_within_budget'],'Original refinement gate failed')
            write(CAMPAIGN/f'ray{ray:03d}-complete.json',dict(ray=ray,comparison=str(result),sha256=digest(result),finished=now()))
            completed.append(ray)
        verify(protected);verify(inputs)
    except BaseException as error:
        failure=repr(error)
        raise
    finally:
        write(CAMPAIGN/'end.json',dict(state='complete' if failure is None else 'stopped',completed_rays=completed,failure=failure,
                                      runs=runs,finished=now(),no_automatic_retry=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=('compile','batch','native','freeze','seed','run','check','compare'))
    parser.add_argument('--ray',type=int,choices=RAYS);parser.add_argument('--order',type=int,choices=ORDERS)
    parser.add_argument('--stop-utc',required=True)
    options=parser.parse_args()
    deadline=datetime.fromisoformat(options.stop_utc.replace('Z','+00:00'))
    require(deadline.tzinfo is not None and deadline.utcoffset().total_seconds()==0,'Explicit UTC stop required')
    process=psutil.Process();process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS);process.cpu_affinity([4])
    identity=dict(pid=process.pid,created_time=process.create_time(),command=process.cmdline(),parent_pid=process.ppid())
    guard()
    if options.stage=='compile':
        for ray in RAYS:
            for stage in ('native','freeze','run','check','compare'):
                render(stage,ray)
        print('Compiled 15 retained stage programs without running them')
    elif options.stage=='batch':
        batch()
    else:
        verify(read(CAMPAIGN/'protocol.json')['inputs'])
        require(options.ray in RAYS,'Ray required')
        stage_work(options.stage,options.ray,options.order)
