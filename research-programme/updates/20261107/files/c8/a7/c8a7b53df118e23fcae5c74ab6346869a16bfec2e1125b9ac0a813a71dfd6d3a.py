import os

for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[variable]='1'

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime,timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil
import run_final_real_directions as original

ROOT=Path(__file__).resolve().parent
FROZEN={'run_final_real_directions.py':'e0fd23ef120edaca3d7b74b7fc35a7869bf7eddf943ee74bc8a497fc1bfa9cde',
        'stable_absorption_panel.py':'8b0d7a28e511b266ffcec9a03cbed6ada54a062ec9941fc92c7520d44fa2728f',
        'real-ray003-panel036-diagnosis-001/results.json':'af14d75ae5289ea843cc91788f81b81727ffdd9ee1a52248ab4f8bad2604aaf3',
        'real-ray003-panel036-diagnosis-001/comparisons.npz':'6c99b092c72d9ba99ce6783472ba29403526e49daa91e618cc0125a99d0e8072',
        'final-real-batch-rays003-004/end.json':'cb6130d7d69d0f20e4d0f89223b159614908397533c5a71151926eaf855903d7'}
read,digest,verify=original.read,original.digest,original.verify


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path,value):
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)
        stream.flush()
        os.fsync(stream.fileno())


def require(condition,reason):
    if not condition:
        raise RuntimeError(reason)


def fixed_inputs():
    return {**{str(ROOT/name):expected for name,expected in FROZEN.items()},str(Path(__file__)):digest(__file__)}


def render(stage,ray):
    source,base=original.render(stage,ray)
    changes=[]
    def replace(before,after):
        nonlocal source
        source=original.replace(source,before,after,changes)
    qualified=f'compensated-epoch-source-final450-ray{ray:03d}'
    native=f'final-absorption-native-v2-ray{ray:03d}'
    if stage=='native':
        replace("DESTINATION = PARENT / 'native-paired-check'",f"DESTINATION = ROOT / '{native}'")
        replace("    inputs = dict(report['inputs'])","    inputs = dict(report['inputs'])\n    inputs.update(repair_inputs())")
        boundary="    panel_action, logarithm_action = context['panel_action'], context['logarithm_action']"
        replace(boundary,boundary+"\n    from stable_absorption_panel import panel_action")
    else:
        replace(f'final-epoch-real-source-ray{ray:03d}',f'final-epoch-real-v2-ray{ray:03d}')
        if stage in ('freeze','run'):
            replace(f'{qualified}/native-paired-check/validation.json',native+'/validation.json')
            replace("QUALIFIED / 'native-paired-check/validation.json'",f"ROOT / '{native}/validation.json'")
            replace("inputs = dict(context['inputs'])","inputs = dict(context['inputs'])\ninputs.update(repair_inputs())")
            boundary="panel_action, logarithm_action = context['panel_action'], context['logarithm_action']"
            replace(boundary,boundary+"\nfrom stable_absorption_panel import panel_action")
        elif stage=='check':
            replace(f'{qualified}/native-paired-check/separator-logarithm.npz',native+'/separator-logarithm.npz')
    return source,dict(original_program=base,replacements=changes,transformed_sha256=hashlib.sha256(source.encode()).hexdigest())


def seed_prefix(ray):
    require(ray==3,'Prefix reuse is qualified only for the observed ray3 failure')
    old=ROOT/'final-epoch-real-source-ray003'
    new=ROOT/'final-epoch-real-v2-ray003'
    before,after=read(old/'protocol.json'),read(new/'protocol.json')
    for name in ('panels','labels','history_cell','theta','event','angular_ray','angular_order','angular_weight','event_weight','gate','source_refinement_budget'):
        require(before[name]==after[name],'Prefix protocol differs: '+name)
    verify(before['inputs']); verify(after['inputs'])
    previous=digest(old/'protocol.json'); target_previous=digest(new/'protocol.json')
    destination=new/'order-18'; destination.mkdir()
    count=0
    for index,panel in enumerate(before['panels']['18']):
        if not panel['emission'] and panel['absorption']:
            break
        guard()
        source=old/'order-18'/f'panel-{index:03d}.json'; record=read(source)
        require(record['passed'] and all(row['passed'] for row in record['checks']) and record['previous_sha256']==previous
                and record['panel']==index and record['order']==18 and digest(source.with_suffix('.npz'))==record['packet_sha256'],'Unqualified prefix')
        target=destination/source.name
        with source.with_suffix('.npz').open('rb') as initial,target.with_suffix('.npz').open('xb') as copied:
            shutil.copyfileobj(initial,copied)
        require(digest(target.with_suffix('.npz'))==record['packet_sha256'],'Prefix copy differs')
        previous=digest(source)
        write(target,dict(record,previous_sha256=target_previous,reused_from=str(source),original_metadata_sha256=previous,
                          reuse_reason='Unchanged mathematical and numerical branch; point/sum/correction arrays copied byte for byte'))
        target_previous=digest(target); count+=1
    require(count==35,'Expected untouched prefix0..34')
    write(new/'prefix-reuse.json',dict(panels=count,order=18,source=str(old),source_protocol=digest(old/'protocol.json'),
                                      target_protocol=digest(new/'protocol.json'),failed_panel_copied=False,finished=now()))


def supervise():
    guard(); campaign.mkdir()
    original_protocol=read(ROOT/'final-real-batch-rays003-004/protocol.json')
    protected=dict(original_protocol['preserved_inputs'])
    if arguments.first==3:
        old=ROOT/'final-epoch-real-source-ray003/order-18'
        for path in [*old.glob('panel-*.json'),*old.glob('panel-*.npz'),old.parent/'protocol.json']:
            protected[str(path)]=digest(path)
    verify(protected)
    write(campaign/'protocol.json',dict(started=now(),stop_utc=arguments.stop_utc,rays=rays,inputs=fixed_inputs(),protected=protected,
        process=identity,review='Original failure retained. 100-digit replay favors stable thermal subtraction; geometry-only fix rejected.',
        policy='Use same law for ALL absorption-only panels, modes, joins and models; all other branches delegate to original; never force exchange',
        order=[18,26],panels_per_job=8,identity_gate=1e-10,refinement_gate=.002,max_active_numerical_workers=1))
    runs=[]; completed=[]; failure=None
    def child(stage,ray,extra=()):
        guard(); verify(fixed_inputs_manifest)
        label=f'{len(runs)+1:03d}-ray{ray:03d}-{stage}'
        command=([sys.executable,'-B',str(ROOT/'run_final_real_directions.py'),'precise','--ray',str(ray),'--stop-utc',arguments.stop_utc]
                 if stage=='precise' else [sys.executable,'-B',str(Path(__file__)),stage,'--first',str(arguments.first),'--ray',str(ray),'--stop-utc',arguments.stop_utc,*extra])
        with (campaign/(label+'.stdout.log')).open('x') as stdout,(campaign/(label+'.stderr.log')).open('x') as stderr:
            with subprocess.Popen(command,stdout=stdout,stderr=stderr,cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW) as worker:
                entry=dict(label=label,ray=ray,stage=stage,pid=worker.pid,created_time=psutil.Process(worker.pid).create_time(),command=command,started=now())
                write(campaign/(label+'.start.json'),entry)
                print(json.dumps(dict(started=label,pid=worker.pid)),flush=True)
                code=worker.wait()
        entry.update(actual_exit_code=code,finished=now());runs.append(entry); write(campaign/(label+'.end.json'),entry)
        print(json.dumps(dict(finished=label,exit_code=code)),flush=True)
        require(code==0,'Failed/held stage retained: '+label)
    try:
        for ray in rays:
            qualified=ROOT/f'compensated-epoch-source-final450-ray{ray:03d}'
            native=ROOT/f'final-absorption-native-v2-ray{ray:03d}'
            directory=ROOT/f'final-epoch-real-v2-ray{ray:03d}'
            require(not native.exists() and not directory.exists(),'Existing repaired outputs preserved')
            if not qualified.exists():
                child('precise',ray)
            precise=read(qualified/'validation.json'); require(precise['passed'] and all(row['passed'] for row in precise['checks']),'Passing precise source required')
            require(read(qualified/'prediction.json')['angular_ray']==ray,'Wrong ray qualification')
            verify(precise['inputs'])
            child('native',ray); require(read(native/'validation.json')['passed'],'Stable native qualification failed')
            child('freeze',ray)
            if ray==3:
                child('seed',ray)
            for order in (18,26):
                job=directory/f'order-{order}'; previous=len(list(job.glob('panel-*.json')))
                for iteration in range(12):
                    child('run',ray,('--order',str(order),'--panels','8','--minutes','25'))
                    latest=read(sorted(job.glob('attempt-*-end.json'))[-1])
                    require(latest['state'] in ('complete','batch_complete') and previous<latest['completed_panels']<=previous+8,'Held/failed/no-progress batch')
                    previous=latest['completed_panels']
                    if (job/'complete.json').exists():
                        break
                require(read(job/'complete.json')['passed'],'Radial completion failed')
                if ray==3 and order==18:
                    import numpy as np
                    tests=[]
                    with np.load(job/'panel-036.npz',allow_pickle=False) as packet,np.load(ROOT/'real-ray003-panel036-diagnosis-001/comparisons.npz',allow_pickle=False) as oracle:
                        for join in (0,1):
                            value=packet[f'point:difference:join{join}:l1:actions']
                            reference=oracle[f'join{join}:oracle_independent_geometry']
                            for name,indices in (('all coordinates',slice(None)),('independent exchange rows',[0,-1])):
                                error=np.linalg.norm(value[:,indices,:]-reference[:,indices,:],axis=1)/np.maximum(np.linalg.norm(reference[:,indices,:],axis=1),1e-300)
                                tests.append(dict(join=join,test=name,entries=int(error.size),maximum=float(error.max()),passed=bool(np.all(np.isfinite(error)&(error<=1e-10)))))
                            tests.append(dict(join=join,test='qualified stable replay',passed=bool(np.array_equal(value,oracle[f'join{join}:stable_thermal_native']))))
                    write(campaign/'verified-panel036.json',dict(checks=tests,gate=1e-10,passed=all(row['passed'] for row in tests)))
                    require(all(row['passed'] for row in tests),'Production packet differs from the qualified independent replay')
                child('check',ray,('--order',str(order))); require(read(job/'independent.json')['passed'],'Independent check failed')
            child('compare',ray)
            comparison=read(directory/'order18-vs26.json');require(comparison['all_component_rows_within_budget'],'Refinement gate failed')
            write(campaign/f'ray{ray:03d}-complete.json',dict(ray=ray,comparison=str(directory/'order18-vs26.json'),sha256=digest(directory/'order18-vs26.json'),finished=now()))
            completed.append(ray)
        verify(protected); verify(fixed_inputs_manifest)
    except BaseException as error:
        failure=repr(error)
        raise
    finally:
        write(campaign/'end.json',dict(state='complete' if failure is None else 'stopped',completed_rays=completed,failure=failure,runs=runs,finished=now(),no_automatic_retry=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('stage',choices=('batch','seed','native','freeze','run','check','compare'))
    parser.add_argument('--first',type=int,required=True,choices=range(1,127)); parser.add_argument('--ray',type=int)
    parser.add_argument('--stop-utc',required=True); parser.add_argument('--compile-only',action='store_true')
    arguments,remainder=parser.parse_known_args();rays=[arguments.first,arguments.first+1]
    campaign=ROOT/f'final-stable-real-batch-rays{rays[0]:03d}-{rays[1]:03d}'
    stop=datetime.fromisoformat(arguments.stop_utc.replace('Z','+00:00'));require(stop.utcoffset().total_seconds()==0,'Explicit UTC stop required')
    process=psutil.Process();process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS);process.cpu_affinity([4])
    identity=dict(pid=process.pid,created_time=process.create_time(),command=process.cmdline(),parent_pid=process.ppid())
    fixed_inputs_manifest=fixed_inputs();verify(fixed_inputs_manifest);verify({ROOT/name:expected for name,expected in original.PARENTS.items()})
    def stopping():
        folders=[ROOT,ROOT.parent,campaign,ROOT/'final-real-batch-rays003-004',ROOT/'final-real-batch-rays001-002',ROOT/'saved-epoch-cell450',ROOT/'final-epoch-kinematic-bank']
        for ray in rays:
            folders.extend(ROOT/f'{prefix}{ray:03d}' for prefix in ('final-epoch-real-source-ray','final-epoch-real-v2-ray','compensated-epoch-source-final450-ray','final-absorption-native-v2-ray'))
        return (datetime.now(timezone.utc)>=stop or 3<=datetime.now(timezone.utc).astimezone(ZoneInfo('Europe/London')).hour<14
                or any((path/'STOP-REQUESTED').exists() for path in folders) or (ROOT.parent/'execution-v3/STOP-REQUEST.json').exists()
                or shutil.disk_usage(ROOT).free<6*1024**3)
    def guard():
        require(not stopping(),'Owner/music/time/disk hold preserved')
    if arguments.stage=='batch':
        require(not remainder and not arguments.compile_only,'Use dry-run compile for individual stages')
        supervise(); raise SystemExit(0)
    ray=arguments.ray;require(ray in rays,'Direction outside frozen pair')
    if arguments.stage=='seed':
        guard(); seed_prefix(ray); raise SystemExit(0)
    source,adaptation=render(arguments.stage,ray)
    program=compile(source,str(ROOT/adaptation['original_program']['parent']),'exec')
    precise,changes=original.qualification_source('precise',ray)
    adaptation.update(ray=ray,adapter=str(Path(__file__)),adapter_sha256=digest(__file__),repair_inputs=fixed_inputs_manifest,
        precise_setup=dict(transformed_sha256=hashlib.sha256(precise.encode()).hexdigest(),replacements=changes))
    if arguments.compile_only:
        print(json.dumps(dict(compiled=True,ray=ray,stage=arguments.stage,sha256=adaptation['transformed_sha256'])));raise SystemExit(0)
    guard()
    def cached_owner(parameters,direction):
        from exact_kinematic_cache import CachedDirection
        path=ROOT/f'final-epoch-kinematic-bank/ray-{ray:03d}.json'; record=read(path); frozen=path.with_name('protocol.json')
        require(record['ray']==ray and record['passed'] and record['protocol_sha256']==digest(frozen),'Qualified matching angular cache required')
        verify(read(frozen)['inputs'])
        return CachedDirection(parameters,direction,path.with_name(f'ray-{ray:03d}-kernel.json'),record['kernel_sha256'])
    sys.argv=[str(Path(__file__)),*([arguments.stage] if arguments.stage in ('freeze','run') else []),*remainder]
    if arguments.stage in ('freeze','run'):
        sys.argv.extend(['--stop-utc',arguments.stop_utc])
    context=dict(__file__=str(Path(__file__)),__name__='qualified_stable_absorption',ADAPTATION=adaptation,
        adapter_guard=guard,adapter_stopping=stopping,endpoint_guard=guard,cached_owner=cached_owner,qualified_cached_owner=cached_owner,
        endpoint_source_text=lambda *unused:precise,repair_inputs=lambda:fixed_inputs_manifest)
    exec(program,context)
