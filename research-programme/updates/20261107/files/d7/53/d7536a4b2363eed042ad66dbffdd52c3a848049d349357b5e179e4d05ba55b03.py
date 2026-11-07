from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse, copy, hashlib, json, math, time
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'temperature-history-response-matching-20261022'
sys.path[:0]=[str(PARENT),str(BRANCH/'repaired-history-microscopic-source-20261021')]
import matching198 as match
import source_stage190 as microscopic
saved=match.saved
np,linear,mp=microscopic.np,microscopic.linear,microscopic.mp
read,write,packet,save,digest,check=saved.read,saved.write,saved.packet,saved.save,saved.digest,saved.check
history=microscopic.prior
source=microscopic.source
smooth=history.previous.previous
OFFSET=-.015

def checked_protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def prepare():
    assert not (ROOT/'configuration.json').exists()
    parent=read(PARENT/'results/stage-integrity.json')
    assert parent['state']=='complete' and parent['stage']==198
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(PARENT/'results/stage-integrity.json')]=digest(PARENT/'results/stage-integrity.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    old=read(saved.ROOT/'configuration.json')
    config=dict(stage=199,started_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),offset=OFFSET,
        theta0=old['theta0'],expansion_span=old['expansion_span'],
        target_fraction=.875-OFFSET/old['expansion_span'],
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        offsets=[-.01,-.005,0.],prediction_weights=[3.,-3.,1.],
        history_groups=['original','candidate-half','candidate-quarter'],
        frequencies=read(saved.PARENT/'configuration.json')['panel_frequencies'],
        protocol_hashes={path.name:digest(path) for path in [ROOT/'continue199.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
        bookmarks={str(path):digest(path) for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    pairs=[]
    for tag in ('minus','minus_half','anchor'):
        path=saved.register(inputs,saved.ROOT/f'sources/{tag}.npz')
        data=packet(path)
        pairs.append((data['high'],data['low']))
    prediction=microscopic.source.precise_combine(pairs,config['prediction_weights'])
    save(ROOT/'frozen/panel-prediction.npz',high=prediction[0],low=prediction[1],offset=OFFSET)
    frozen=smooth.frozen_candidate()
    save(ROOT/'frozen/operator-prediction.npz',block=frozen['block'],tangent=frozen['tangent'],curvature=frozen['curvature'],
        prediction=smooth.candidate(OFFSET,frozen))
    config['prediction_hashes']={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen').glob('*.npz')}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
    write(ROOT/'inputs.json',inputs);write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='prediction_frozen',target_fraction=config['target_fraction']))
    print(json.dumps(dict(state='prediction_frozen',target_fraction=config['target_fraction'],inputs=len(inputs))),flush=True)

def collision():
    config=checked_protocol();frozen=packet(ROOT/'frozen/operator-prediction.npz')
    assert digest(ROOT/'frozen/operator-prediction.npz')==config['prediction_hashes'][str(Path('frozen')/'operator-prediction.npz')]
    old=smooth.old
    ladder,basis,theta0=old.setup();theta=theta0*math.exp(OFFSET)
    events=old.geometry_module.event_geometry(theta,6)
    began=time.monotonic()
    actual,discarded=old.ladder_module.scalar_physical_block(basis,theta,events)
    masks=packet(old.ROOT/'results/frozen-tangent.npz')['masks']
    boundary=np.zeros_like(actual);crossings=0
    for node,initial in enumerate(basis.values):
        ratio,extra,final,conductance=old.physical_pairs(basis,theta,events,node)
        inside=(final>=basis.minimum)&(final<=basis.maximum);changed=inside!=masks[node]
        if np.any(changed):
            difference=initial[None,:]-basis.evaluate(final[changed])
            sign=inside[changed].astype(int)-masks[node,changed].astype(int)
            boundary-=.5*(difference.T*(conductance[changed]*sign))@difference
            crossings+=int(changed.sum())
    rows=[]
    for label,block in [('live',actual),('anchor_mask',actual-boundary)]:
        change=block-frozen['block'];remainder=change-OFFSET*frozen['tangent']
        check(rows,label+':quadratic remainder',np.linalg.norm(.5*OFFSET**2*frozen['curvature']-remainder)/np.linalg.norm(remainder),.01)
        check(rows,label+':small change',np.linalg.norm(frozen['prediction']-block)/np.linalg.norm(change),.01)
    lower=OFFSET;upper=read(smooth.ROOT/'configuration.json')['domain'][1]
    controls=[smooth.candidate(lower,frozen),smooth.candidate(lower,frozen)+.5*(upper-lower)*(frozen['tangent']+lower*frozen['curvature']),smooth.candidate(upper,frozen)]
    factor=linear.cholesky(basis.mass,lower=True);orthogonal=linear.null_space((factor.T@basis.chemical)[None,:])
    for index,block in enumerate(controls):
        scale=np.linalg.norm(block)
        check(rows,f'Bernstein{index}:symmetry',np.linalg.norm(block-block.T)/scale,1e-10)
        check(rows,f'Bernstein{index}:number null',np.linalg.norm(block@basis.chemical)/(scale*np.linalg.norm(basis.chemical)),1e-10)
        whitened=smooth.whiten(block,factor);eigen=linear.eigvalsh(orthogonal.T@whitened@orthogonal)
        check(rows,f'Bernstein{index}:nonpositive',max(0.,float(eigen[-1]))/max(abs(float(eigen[0])),abs(float(eigen[-1]))),1e-10)
    save(ROOT/'collision/target.npz',actual=actual,boundary=boundary,theta=theta,offset=OFFSET)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'collision/status.json',dict(checks=rows,failed_checks=failed,seconds=time.monotonic()-began,crossings=crossings,
        discarded_weight_fraction=discarded,sha256=digest(ROOT/'collision/target.npz'),structure_scope='numerical Bernstein controls; not interval-rounded certificate'))
    write(ROOT/'progress.json',dict(state='collision_passed' if not failed else 'collision_failed'))
    print(json.dumps(dict(state=read(ROOT/'progress.json')['state'],checks=rows)),flush=True)

class ContinuedEquation(history.previous.ProbeEquation):
    def stiffness(self,coordinate):
        config=checked_protocol();local=self.operator.background.at(float(coordinate))
        offset=float(np.log(local['thermal_parameter']/self.theta0))
        assert OFFSET-1e-13<=offset<=read(smooth.ROOT/'configuration.json')['domain'][1]+1e-13
        scattering=smooth.candidate(offset,self.frozen)
        damping=self.operator.emission.at(local['thermal_parameter'],'dcbr')
        rate=local['coefficient']/local['thermal_parameter']
        return smooth.corner.mp_matrix(rate*(scattering-damping))

def extend(model,grid):
    config=checked_protocol();assert not read(ROOT/'collision/status.json')['failed_checks']
    folder=ROOT/'histories'/model/grid
    if (folder/'complete.json').exists():
        return
    originals=history.previous.history(model,'candidate',grid)
    states,unused,chain=history.read_history(model,'candidate',grid)
    assert len(states)==len(originals['expansion'])
    start=float(originals['expansion'][-1]);step=float(originals['step'])
    target=config['target_fraction']*config['expansion_span']
    coordinates=[];index=1
    while start+index*step<target-1e-14:
        coordinates.append(start+index*step);index+=1
    coordinates.append(target)
    seed=folder/'restart.json'
    if seed.exists():
        restart=read(seed);done=restart['done'];current_data=restart['current'];older_data=restart['older'];checks=restart['checks']
    else:
        done=0;current_data=states[-1];older_data=states[-2];checks=[]
    began=time.monotonic()
    with mp.workdps(80):
        equation=ContinuedEquation(model,'candidate')
        current,older=history.parse_state(current_data),history.parse_state(older_data)
        for ordinal in range(done,len(coordinates)):
            before=start if ordinal==0 else coordinates[ordinal-1]
            before_previous=start-step if ordinal==0 else start if ordinal==1 else coordinates[ordinal-2]
            delta=mp.mpf(coordinates[ordinal])-mp.mpf(before)
            old_delta=mp.mpf(before)-mp.mpf(before_previous)
            updated,diagnostic=equation.advance(current,older,mp.mpf(coordinates[ordinal]),delta,old_delta)
            checks.extend(history.identity_rows([dict(diagnostic,ordinal=ordinal)]))
            if ordinal==len(coordinates)-1:
                with mp.workdps(100):
                    audit_equation=ContinuedEquation(model,'candidate')
                    audit,audit_diag=audit_equation.advance(current,older,mp.mpf(coordinates[ordinal]),delta,old_delta)
                    numerator=mp.sqrt(mp.fsum(value*value for value in audit['profile']-updated['profile']))
                    denominator=mp.sqrt(mp.fsum(value*value for value in audit['profile']))
                    check(checks,'80/100 target profile',numerator/denominator,1e-10)
                    check(checks,'80/100 target gas',audit['gas']-updated['gas'],1e-10)
            older,current=current,updated
            record=dict(done=ordinal+1,total=len(coordinates),current=history.previous.serial_state(current),
                older=history.previous.serial_state(older),coordinate=coordinates[ordinal],checks=checks,source_chain_sha256=chain,
                source_start=start,step=step,elapsed_seconds=time.monotonic()-began)
            write(seed,record)
            if (ordinal+1)%8==0:
                print(json.dumps(dict(model=model,grid=grid,done=ordinal+1,total=len(coordinates))),flush=True)
        record.update(failed_checks=[row for row in checks if not row['passed']],target=target)
        write(folder/'complete.json',record)
        assert not record['failed_checks']
    print(json.dumps(dict(model=model,grid=grid,complete=True,steps=len(coordinates),seconds=time.monotonic()-began)),flush=True)

def repaired(original,grid):
    bundle=copy.deepcopy(original);epoch=bundle.epochs[0];values=[]
    for model_index,model in enumerate(('heavy','cold')):
        path=ROOT/'histories'/model/grid/'complete.json';record=read(path)
        assert not record['failed_checks'] and abs(record['coordinate']-epoch.coordinate)<1e-13
        state=record['current'];profile=np.array([float(value) for value in state['profile']])
        epoch.original[model]=profile;epoch.gas[model_index]=float(state['gas'])
        frequency,slope=epoch.tails[model]
        for lower,upper in ((1e-4,2e-4),(5e-5,1e-4)):
            phi=np.zeros(len(epoch.frequency));low=epoch.frequency<upper;high=epoch.frequency>lower
            tail=np.interp(np.log(epoch.frequency[low]),np.log(frequency),slope)*epoch.frequency[low]
            phi[high]=epoch.basis.evaluate(epoch.frequency[high])@profile
            phase=np.clip((epoch.frequency[low]-lower)/(upper-lower),0,1);blend=phase**3*(10-15*phase+6*phase**2)
            phi[low]=(1-blend)*tail+blend*phi[low];values.append(phi)
        bundle.inputs.append(path)
    from scipy.interpolate import CubicSpline
    epoch.values=np.column_stack(values);epoch.spline=CubicSpline(np.log(epoch.frequency),epoch.values,axis=0,extrapolate=False)
    epoch.derivative_spline=epoch.spline.derivative();bundle.gas=list(epoch.gas)
    return bundle

def virtual(parameters,inputs):
    identity=source.physics.event_owner.inherited.virtual_identity(parameters)
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    paths=[directory/key[:2]/(key+'.json') for directory in BRANCH.glob('*/virtual-cache')]
    existing=next((path for path in paths if path.is_file()),None)
    if existing:
        saved.register(inputs,existing);data=read(existing)
        assert data['identity']==identity and data['finite']
        return data['scalar'],existing,True
    destination=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    if destination.exists():
        data=read(destination)
    else:
        began=time.monotonic();unused,response=source.physics.weak.source.virtual_map(parameters,2)
        data=dict(identity=identity,scalar=float(response[0,0]),finite=bool(np.isfinite(response[0,0])),seconds=time.monotonic()-began)
        assert data['finite'];write(destination,data)
    assert data['identity']==identity and data['finite']
    return data['scalar'],destination,False

def events(seconds,max_events):
    config=checked_protocol();inputs=read(ROOT/'inputs.json')
    for name,value in config['prediction_hashes'].items():
        assert digest(ROOT/name)==value
    original,theta=source.context(config['target_fraction'])
    parts=[original,repaired(original,'half'),repaired(original,'quarter')]
    bundle=microscopic.crossed.HistoryGroup(parts);evaluators=source.models(bundle)
    for path in bundle.inputs:
        if not Path(path).resolve().is_relative_to(ROOT):
            saved.register(inputs,path)
    began=time.monotonic();completed=0
    for frequency_index,frequency in enumerate(config['frequencies']):
        nodes=microscopic.event_common.nodes(theta,frequency)
        assert len(nodes)==36
        for node_index,node in enumerate(nodes):
            path=ROOT/f'events/frequency-{frequency_index}/node-{node_index:02d}.npz'
            if path.exists():
                status=read(path.with_suffix('.json'));assert digest(path)==status['sha256'] and not status['failed_checks']
                continue
            if time.monotonic()-began>=seconds or completed>=max_events:
                write(ROOT/'inputs.json',inputs)
                write(ROOT/'progress.json',dict(state='safe_restart',frequency_index=frequency_index,node_index=node_index,
                    completed_events=len(list((ROOT/'events').rglob('*.npz'))),expected_events=252))
                return
            started=time.monotonic();parameters,weight=source.physics.parameters_and_weight(theta,node)
            scalar,loop_path,reused=virtual(parameters,inputs)
            high,low,diagnostics=microscopic.weighted(parameters,bundle,evaluators,scalar,weight)
            assert high.shape==low.shape==(3,6,98,4)
            rows=[]
            for name,value in diagnostics.items():
                check(rows,name,value,1e-10)
            check(rows,'all finite',int(not np.isfinite(high+low).all()),0,'integrity')
            save(path,high=high,low=low,theta=theta,weight=weight,node=json.dumps(node,sort_keys=True),loop_path=str(loop_path))
            report=dict(sha256=digest(path),checks=rows,failed_checks=[row for row in rows if not row['passed']],
                loop_path=str(loop_path),loop_sha256=digest(loop_path),loop_reused=reused,seconds=time.monotonic()-started)
            write(path.with_suffix('.json'),report);assert not report['failed_checks']
            completed+=1;write(ROOT/'inputs.json',inputs)
            write(ROOT/'progress.json',dict(state='evaluating',frequency_index=frequency_index,node_index=node_index,
                completed_events=len(list((ROOT/'events').rglob('*.npz'))),expected_events=252))
            print(json.dumps(dict(frequency=frequency,node=node_index,seconds=report['seconds'],reused_loop=reused)),flush=True)
    write(ROOT/'progress.json',dict(state='events_complete',completed_events=252))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','collision','history','events'])
    parser.add_argument('--model',choices=['heavy','cold']);parser.add_argument('--grid',choices=['half','quarter'])
    parser.add_argument('--seconds',type=float,default=7200);parser.add_argument('--max-events',type=int,default=252)
    args=parser.parse_args()
    if args.action=='prepare':prepare()
    elif args.action=='collision':collision()
    elif args.action=='history':extend(args.model,args.grid)
    else:events(args.seconds,args.max_events)
