from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime, timezone
import argparse, copy, hashlib, json, math, time
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'farther-cold-operator-bridge-20261023'
sys.path.insert(0,str(PARENT))
import bridge200 as inherited
previous=inherited.previous
source,microscopic,saved=previous.source,previous.microscopic,previous.saved
np,mp,linear=previous.np,previous.mp,previous.linear
read,write,packet,save,digest,check=previous.read,previous.write,previous.packet,previous.save,previous.digest,previous.check
PARENT_SHA='bd69f8d24c27685ceb8cfc8accb7fc5fa5431b181f3046f280f6fc8bf1137305'
GRIDS=('half','quarter')


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def joined(original,profiles,gases,increment):
    from scipy.interpolate import CubicSpline
    bundle=copy.deepcopy(original)
    epoch=bundle.epochs[0]
    values=[]
    for model_index,model in enumerate(('heavy','cold')):
        profile=profiles[model_index]
        epoch.original[model]=profile
        epoch.gas[model_index]=gases[model_index]
        frequency,slope=epoch.tails[model]
        for lower,upper in ((1e-4,2e-4),(5e-5,1e-4)):
            phi=np.zeros(len(epoch.frequency))
            low=epoch.frequency<upper
            high=epoch.frequency>lower
            tail=np.zeros(low.sum()) if increment else np.interp(np.log(epoch.frequency[low]),np.log(frequency),slope)*epoch.frequency[low]
            phi[high]=epoch.basis.evaluate(epoch.frequency[high])@profile
            phase=np.clip((epoch.frequency[low]-lower)/(upper-lower),0,1)
            blend=phase**3*(10-15*phase+6*phase**2)
            phi[low]=(1-blend)*tail+blend*phi[low]
            values.append(phi)
    epoch.values=np.column_stack(values)
    epoch.spline=CubicSpline(np.log(epoch.frequency),epoch.values,axis=0,extrapolate=False)
    epoch.derivative_spline=epoch.spline.derivative()
    bundle.gas=list(epoch.gas)
    return bundle


def histories():
    original,theta=source.context(.90625)
    increment_parts=[]
    absolutes=[original]
    rows=[]
    for grid in GRIDS:
        profiles=[];gases=[];increments=[];gas_increments=[]
        with mp.workdps(80):
            for model_index,model in enumerate(('heavy','cold')):
                path=PARENT/f'histories/{model}/{grid}/complete.json'
                record=read(path)
                assert not record['failed_checks']
                assert abs(record['coordinate']-original.epochs[0].coordinate)<1e-13
                state=record['current']
                profiles.append(np.array([float(value) for value in state['profile']]))
                gases.append(float(state['gas']))
                old_profile=original.epochs[0].original[model]
                increments.append(np.array([float(mp.mpf(value)-mp.mpf(float(old))) for value,old in zip(state['profile'],old_profile)]))
                gas_increments.append(float(mp.mpf(state['gas'])-mp.mpf(float(original.gas[model_index]))))
                original.inputs.append(path)
        absolute=joined(original,profiles,gases,False)
        photon=joined(original,increments,[0.,0.],True)
        gas=joined(original,[np.zeros(96),np.zeros(96)],gas_increments,True)
        increment_parts.extend([photon,gas])
        absolutes.append(absolute)
        before=original.epochs[0].values
        expected=before+photon.epochs[0].values
        scale=np.linalg.norm(absolute.epochs[0].values)
        check(rows,grid+':joined increment identity',np.linalg.norm(absolute.epochs[0].values-expected)/scale,1e-10)
        for model_index in range(2):
            check(rows,f'{grid}:{model_index}:gas increment identity',
                abs(original.gas[model_index]+gas_increments[model_index]-gases[model_index])/max(abs(gases[model_index]),1e-300),1e-10)
    zero=joined(original,[np.zeros(96),np.zeros(96)],[0.,0.],True)
    increment_parts.append(zero)
    probes=np.geomspace(1e-6,60,79)
    for grid_index,grid in enumerate(GRIDS):
        photon=increment_parts[2*grid_index]
        direct=absolutes[grid_index+1]
        difference=direct.functions(probes)[...,1:]-original.functions(probes)[...,1:]
        prediction=photon.functions(probes)[...,1:]
        check(rows,grid+':sampled increment prediction',np.linalg.norm(prediction-difference)/np.linalg.norm(difference),.01)
        derivative_original=np.array([original.derivatives(value)[1:] for value in probes])
        derivative_direct=np.array([direct.derivatives(value)[1:] for value in probes])
        derivative_prediction=np.array([photon.derivatives(value)[1:] for value in probes])
        check(rows,grid+':sampled derivative prediction',np.linalg.norm(derivative_prediction-(derivative_direct-derivative_original))/np.linalg.norm(derivative_direct-derivative_original),.01)
    return original,theta,increment_parts,absolutes,rows


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    original,theta,increments,absolutes,rows=histories()
    assert all(row['passed'] for row in rows),rows
    nodes=microscopic.event_common.nodes(theta,14.)
    assert len(nodes)==36
    inventory=read(PARENT/'results/next-source-cache.json')
    loops=[]
    for node_index,node in enumerate(nodes):
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        identity=source.physics.event_owner.inherited.virtual_identity(parameters)
        key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
        entry=next(row for row in inventory['records'] if row['frequency']==14 and row['event']==node_index)
        assert entry['exact_virtual_cached'] and entry['identity_key']==key
        saved.register(inputs,entry['path'],entry['sha256'])
        data=read(entry['path'])
        assert data['identity']==identity and data['finite']
        loops.append(dict(path=entry['path'],sha256=entry['sha256'],identity_key=key,weight=weight))
    for path in original.inputs:
        saved.register(inputs,path)
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',dict(stage=201,started_utc=datetime.now(timezone.utc).isoformat(),parent_sha256=PARENT_SHA,
        target_fraction=.90625,theta=theta,frequency=14.,nodes=nodes,loops=loops,
        prediction_groups=['photon-half','gas-half','photon-quarter','gas-quarter','zero'],
        actual_groups=['original','repaired-half','repaired-quarter'],
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        protocol_hashes={name:digest(ROOT/name) for name in ('source201.py','ACCEPTANCE.md','DERIVATION.md')},
        bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}))
    save(ROOT/'frozen/history-representation.npz',
        increment_values=np.array([part.epochs[0].values for part in increments]),
        increment_gases=np.array([part.gas for part in increments]),
        absolute_values=np.array([part.epochs[0].values for part in absolutes]),absolute_gases=np.array([part.gas for part in absolutes]))
    write(ROOT/'results/representation.json',dict(checks=rows,failed_checks=[],sha256=digest(ROOT/'frozen/history-representation.npz')))
    write(ROOT/'progress.json',dict(state='prepared',cached_virtuals=36,inputs=len(inputs)))
    print(json.dumps(dict(state='prepared',checks=len(rows),cached_virtuals=36,inputs=len(inputs))),flush=True)


def events(kind,seconds,limit):
    config=protocol()
    if kind=='actual':
        frozen=read(ROOT/'frozen/prediction-manifest.json')
        for name,value in frozen['files'].items():
            assert digest(ROOT/name)==value,name
    original,theta,increments,absolutes,rows=histories()
    assert theta==config['theta'] and all(row['passed'] for row in rows)
    representation=packet(ROOT/'frozen/history-representation.npz')
    for key,parts,attribute in [('increment_values',increments,'values'),('absolute_values',absolutes,'values')]:
        assert np.array_equal(representation[key],np.array([getattr(part.epochs[0],attribute) for part in parts]))
    for key,parts in [('increment_gases',increments),('absolute_gases',absolutes)]:
        assert np.array_equal(representation[key],np.array([part.gas for part in parts]))
    parts=increments if kind=='prediction' else absolutes
    bundle=microscopic.crossed.HistoryGroup(parts)
    evaluators=source.models(bundle)
    began=time.monotonic();completed=0
    for index,node in enumerate(config['nodes']):
        path=ROOT/f'{kind}/event-{index:02d}.npz'
        if path.exists():
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256']
            assert not record['failed_checks']
            continue
        if completed>=limit or time.monotonic()-began>=seconds:
            write(ROOT/'progress.json',dict(state='safe_restart',phase=kind,next_event=index))
            return
        started=time.monotonic()
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        entry=config['loops'][index]
        assert weight==entry['weight'] and digest(entry['path'])==entry['sha256']
        loop=read(entry['path'])
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        high,low,diagnostics=microscopic.weighted(parameters,bundle,evaluators,loop['scalar'],weight)
        assert high.shape==low.shape==(len(parts),6,98,4)
        checks=[]
        for name,value in diagnostics.items():
            check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
        if kind=='prediction':
            check(checks,'zero history gives exactly zero source',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'identity')
        save(path,high=high,low=low,theta=theta,weight=weight,node=json.dumps(node,sort_keys=True))
        failed=[row for row in checks if not row['passed']]
        write(path.with_suffix('.json'),dict(checks=checks,failed_checks=failed,sha256=digest(path),
            loop_path=entry['path'],loop_sha256=entry['sha256'],seconds=time.monotonic()-started,
            finished_utc=datetime.now(timezone.utc).isoformat(),new_virtual_integrals=0))
        write(ROOT/'progress.json',dict(state='evaluating',phase=kind,done=index+1,total=36))
        print(json.dumps(dict(phase=kind,event=index,seconds=time.monotonic()-started,failed=failed)),flush=True)
        assert not failed,failed
        completed+=1
    write(ROOT/'progress.json',dict(state=kind+'_events_complete',done=36))


def combine(pair_list):
    return saved.parts_sum(np.stack([pair[0] for pair in pair_list]),np.stack([pair[1] for pair in pair_list]))


def freeze():
    config=protocol()
    assert not (ROOT/'actual').exists()
    assert not (ROOT/'frozen/prediction-manifest.json').exists()
    files={}
    for index in range(36):
        path=ROOT/f'prediction/event-{index:02d}.npz'
        record=read(path.with_suffix('.json'))
        assert digest(path)==record['sha256'] and not record['failed_checks']
        data=packet(path)
        pairs=[combine([(data['high'][2*index],data['low'][2*index]),
                        (data['high'][2*index+1],data['low'][2*index+1])]) for index in range(2)]
        destination=ROOT/f'frozen/event-{index:02d}-prediction.npz'
        save(destination,high=np.array([pair[0] for pair in pairs]),low=np.array([pair[1] for pair in pairs]))
        for entry in (path,path.with_suffix('.json'),destination):
            files[str(entry.relative_to(ROOT)).replace('\\','/')]=digest(entry)
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),files=files,
        prediction='full fixed-temperature photon response plus gas response',actual_sources_evaluated=False,
        independent_temperature_test=False,no_free_coefficients=True))
    write(ROOT/'progress.json',dict(state='full_increment_predictions_frozen'))
    print(json.dumps(dict(state='full_increment_predictions_frozen',events=36)),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','prediction','freeze','actual'])
    parser.add_argument('--seconds',type=float,default=2400)
    parser.add_argument('--max-events',type=int,default=36)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.phase=='freeze':freeze()
    else:events(args.phase,args.seconds,args.max_events)
