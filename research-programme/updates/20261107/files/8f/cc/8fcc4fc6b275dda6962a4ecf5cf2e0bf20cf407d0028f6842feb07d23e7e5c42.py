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
PARENT=BRANCH/'cold-complete-seven-frequency-source-20261024'
WARM=BRANCH/'colder-source-continuation-20261022'
HISTORY=BRANCH/'farther-cold-operator-bridge-20261023'
PARENT_SHA='fcba3d1a0e110fd0efc45650140a1ea69055e5614f74fe2b10df309db0a02c15'
sys.path[:0]=[str(PARENT),str(HISTORY)]
import source207 as prior
import evolve200 as evolution
import cached201 as cached
import precise_history201 as precise
np,mp,linear=prior.np,prior.mp,prior.linear
source,microscopic,saved=prior.source,prior.microscopic,prior.saved
read,write,packet,save,digest,check=prior.read,prior.write,prior.packet,prior.save,prior.digest,prior.check
combine,metrics=prior.combine,prior.metrics
COMPONENTS=prior.COMPONENTS
GRIDS=prior.GRIDS


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['implementation_hashes'].items():
        assert digest(name)==value,name
    for name,value in config['frozen_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def scaled(pair,coefficient):
    high=coefficient*pair[0]
    error=np.fromiter((math.fma(coefficient,float(value),-float(product)) for value,product in zip(pair[0].flat,high.flat)),
                      dtype=float,count=high.size).reshape(high.shape)
    return high,coefficient*pair[1]+error


def weighted_sum(pairs,weights):
    return metrics.primitives([scaled(pair,weight) for pair,weight in zip(pairs,weights)])


def weights(target,nodes):
    return [math.prod((target-other)/(node-other) for index,other in enumerate(nodes) if index!=ordinal)
            for ordinal,node in enumerate(nodes)]


def warm_increment(path,inputs):
    saved.register(inputs,path)
    report=read(path.with_suffix('.json'))
    saved.register(inputs,path.with_suffix('.json'))
    assert digest(path)==report['sha256'] and not report['failed_checks']
    values=packet(path)
    assert values['high'].shape==values['low'].shape==(3,6,98,4)
    pairs=[metrics.subtract((values['high'][index],values['low'][index]),
                            (values['high'][0],values['low'][0])) for index in (1,2)]
    return (np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs])),values


def cold_increment(path,inputs):
    saved.register(inputs,path)
    saved.register(inputs,path.with_suffix('.json'))
    report=read(path.with_suffix('.json'))
    assert digest(path)==report['sha256'] and not report['failed_checks']
    values=packet(path)
    assert values['high'].shape==values['low'].shape==(5,6,98,4)
    pairs=[combine([(values['high'][2*index],values['low'][2*index]),
                    (values['high'][2*index+1],values['low'][2*index+1])]) for index in range(2)]
    return (np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs])),values


def sample_history(model,grid,target,inputs):
    seed_path=WARM/f'histories/{model}/{grid}/complete.json'
    saved.register(inputs,seed_path)
    seed,previous_coordinate,unused=evolution.schedule(model,grid)
    points=[dict(coordinate=previous_coordinate,state=seed['older']),
            dict(coordinate=seed['coordinate'],state=seed['current'])]
    chain=digest(seed_path)
    for path in sorted((HISTORY/f'histories/{model}/{grid}/blocks').glob('*.json')):
        saved.register(inputs,path)
        block=read(path)
        assert block['previous_chain']==chain and all(row['passed'] for row in block['checks'])
        chain=hashlib.sha256((chain+digest(path)).encode()).hexdigest()
        points.extend(block['states'])
    complete_path=HISTORY/f'histories/{model}/{grid}/complete.json'
    saved.register(inputs,complete_path)
    assert read(complete_path)['chain']==chain
    earlier=[point for point in points if point['coordinate']<=target]
    assert len(earlier)>=2
    older,current=earlier[-2:]
    rows=[]
    with mp.workdps(80):
        state=evolution.history.parse_state(current['state'])
        old_state=evolution.history.parse_state(older['state'])
        if current['coordinate']==target:
            output=current['state']
            method='exact saved state'
        else:
            equation=evolution.Equation(model)
            delta=mp.mpf(target)-mp.mpf(current['coordinate'])
            previous_delta=mp.mpf(current['coordinate'])-mp.mpf(older['coordinate'])
            updated,diagnostic=equation.advance(state,old_state,mp.mpf(target),delta,previous_delta)
            rows.extend(evolution.history.identity_rows([dict(diagnostic,ordinal=0)]))
            with mp.workdps(100):
                audit_equation=evolution.Equation(model)
                audit,unused=audit_equation.advance(state,old_state,mp.mpf(target),delta,previous_delta)
                norm=lambda value:mp.sqrt(mp.fsum(element*element for element in value))
                check(rows,'80/100 profile',norm(audit['profile']-updated['profile'])/norm(audit['profile']),1e-10,'identity')
                check(rows,'80/100 gas',abs(audit['gas']-updated['gas'])/max(abs(audit['gas']),mp.mpf('1e-90')),1e-10,'identity')
            output=evolution.history.previous.serial_state(updated)
            method='one original-equation variable BDF2 step from saved pair'
    record=dict(model=model,grid=grid,coordinate=target,current=output,previous_coordinate=current['coordinate'],
                source_chain=chain,method=method,checks=rows,failed_checks=[row for row in rows if not row['passed']])
    write(ROOT/f'histories/{model}-{grid}.json',record)
    assert not record['failed_checks']
    return record


def coefficient_bundle(original,histories):
    groups=[]
    with mp.workdps(80):
        for grid in GRIDS:
            columns=[]
            for index,model in enumerate(('heavy','cold')):
                current=histories[(model,grid)]['current']
                before=[mp.mpf(float(value)) for value in original.epochs[0].original[model]]
                delta=[mp.mpf(value)-old for value,old in zip(current['profile'],before)]
                gas=mp.mpf(current['gas'])-mp.mpf(float(original.gas[index]))
                vector=delta+[mp.mpf(0),mp.mpf(0),gas]
                columns.extend([vector,vector])
            groups.extend(columns)
        groups.extend([[mp.mpf(0)]*99 for unused in range(4)])
    return cached.CachedBundle(cached.CachedFeatures(original),groups,original.inputs)


def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    parent=read(seal_path)
    assert parent['full_original_8_20_panel_qualified']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in parent['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    history_config=read(HISTORY/'configuration.json')
    cold=history_config['offset']
    warm=-.015
    target=(cold+warm)/2
    fraction=.875-target/history_config['expansion_span']
    original,theta=source.context(fraction)
    for path in original.inputs:saved.register(inputs,path)
    rows=[]
    check(rows,'temperature-coordinate consistency',theta/(history_config['theta0']*math.exp(target))-1,1e-10,'identity')
    assert not read(HISTORY/'results/qualification.json')['failed_checks']
    histories={(model,grid):sample_history(model,grid,fraction*history_config['expansion_span'],inputs)
               for model in ('heavy','cold') for grid in GRIDS}
    with mp.workdps(80):
        mass=evolution.smooth.corner.mp_matrix(original.basis.mass)
        norm=lambda vector:mp.sqrt((vector.T*mass*vector)[0])
        for index,model in enumerate(('heavy','cold')):
            half=evolution.history.parse_state(histories[(model,'half')]['current'])
            quarter=evolution.history.parse_state(histories[(model,'quarter')]['current'])
            reference=mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].original[model]])
            check(rows,model+':history profile correction mesh',norm(half['profile']-quarter['profile'])/norm(quarter['profile']-reference),.01,'mesh')
            check(rows,model+':history gas correction mesh',abs((half['gas']-quarter['gas'])/(quarter['gas']-mp.mpf(float(original.gas[index])))),.01,'mesh')
    bundle=coefficient_bundle(original,histories)
    save(ROOT/'frozen/history-coefficients.npz',high=bundle.high,low=bundle.low)
    panel=read(PARENT/'configuration.json')['original_panel']
    cold_roots={prior.leaf_frequency(path):path.parent.parent for path in (*prior.LEAVES,PARENT/'results/neighbour-source.npz')}
    nodes_by_frequency={item['frequency']:microscopic.event_common.nodes(theta,item['frequency']) for item in panel}
    quad_nodes=[cold,warm,-.0125]
    quad_weights=weights(target,quad_nodes)
    linear_weights=weights(target,[cold,warm])
    for power in range(3):
        check(rows,f'quadratic reproduces degree{power}',sum(weight*node**power for weight,node in zip(quad_weights,quad_nodes))-target**power,1e-10,'identity')
    for power in range(2):
        check(rows,f'secant reproduces degree{power}',sum(weight*node**power for weight,node in zip(linear_weights,[cold,warm]))-target**power,1e-10,'identity')
    check(rows,'original seven-band weight sum',sum(item['seed_weight'] for item in panel)-12,1e-13,'identity')
    anchors=[[],[],[]]
    events=[]
    for frequency_index,item in enumerate(panel):
        frequency=item['frequency']
        for event_index,node in enumerate(nodes_by_frequency[frequency]):
            pairs=[]
            cold_path=cold_roots[frequency]/f'prediction/event-{event_index:02d}.npz'
            pair,cold_values=cold_increment(cold_path,inputs)
            assert float(cold_values['theta'])==read(PARENT/'configuration.json')['theta']
            pairs.append(pair)
            for directory,offset in [(WARM,warm),(WARM/'cold-side-midpoint',-.0125)]:
                path=directory/f'events/frequency-{frequency_index}/node-{event_index:02d}.npz'
                pair,values=warm_increment(path,inputs)
                anchor_node=json.loads(str(values['node']))
                assert anchor_node['frequency']==frequency
                assert abs(float(values['theta'])/(history_config['theta0']*math.exp(offset))-1)<1e-10
                pairs.append(pair)
            for slot,pair in enumerate(pairs):anchors[slot].append(pair)
            quad=weighted_sum(pairs,quad_weights)
            secant=weighted_sum(pairs[:2],linear_weights)
            save(ROOT/f'frozen/frequency-{frequency_index}/event-{event_index:02d}.npz',
                 quadratic_high=quad[0],quadratic_low=quad[1],linear_high=secant[0],linear_low=secant[1])
            events.append(dict(frequency_index=frequency_index,event=event_index,node=node))
    for method,pairs,coefficients in [('quadratic',anchors,quad_weights),('linear',anchors[:2],linear_weights)]:
        sums=[metrics.primitives(values) for values in pairs]
        result=weighted_sum(sums,coefficients)
        save(ROOT/f'frozen/{method}-panel.npz',high=result[0],low=result[1])
    cold_sum=metrics.primitives(anchors[0])
    cold_reference=packet(PARENT/'results/seven-frequency-source.npz')
    difference=metrics.subtract(cold_sum,(cold_reference['prediction_high'],cold_reference['prediction_low']))
    factor=linear.cholesky(original.basis.mass,lower=True)
    check(rows,'cold full-panel replay',np.max(metrics.norms(difference[0]+difference[1],factor)/np.maximum(metrics.norms(cold_sum[0]+cold_sum[1],factor),1e-300)),1e-10,'identity')
    for model,grid in histories:
        rows.extend(dict(row,name=f'{model}:{grid}:'+row['name']) for row in histories[(model,grid)]['checks'])
    assert all(row['passed'] for row in rows),[row for row in rows if not row['passed']]
    implementation={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(BRANCH) and not Path(name).resolve().is_relative_to(ROOT):
            saved.register(inputs,name)
            implementation[str(Path(name).resolve())]=digest(name)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,value in bookmarks.items():
            archive.writestr(Path(name).name,Path(name).read_bytes())
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[]))
    frozen_hashes={str(path.relative_to(ROOT)):digest(path) for folder in ('frozen','histories') for path in (ROOT/folder).rglob('*') if path.is_file()}
    config=dict(stage=208,started_at=datetime.now(timezone.utc).isoformat(),parent_sha256=PARENT_SHA,
                target_fraction=fraction,theta=theta,offset=target,anchor_offsets=quad_nodes,
                quadratic_weights=quad_weights,linear_weights=linear_weights,primary_prediction='quadratic',
                source_prediction_tolerance=.01,identity_tolerance=1e-10,panel=panel,events=events,
                protocol_hashes={name:digest(ROOT/name) for name in ('connection208.py','assess208.py','ACCEPTANCE.md','DERIVATION.md')},
                frozen_hashes=frozen_hashes,implementation_hashes=implementation,bookmarks=bookmarks,
                weights_reapplied=False,original_bank_changed=False,original_curve_changed=False,
                prior_goal_turn='progress: Stage207 completed cold full-band source',
                collision_operator_at_target_previously_tested=True,new_source_at_target_previously_tested=False,
                maximum_event_workers=2,numerical_threads_per_worker=1)
    write(ROOT/'configuration.json',config)
    write(ROOT/'frozen/prediction-manifest.json',dict(frozen_at=datetime.now(timezone.utc).isoformat(),
          configuration_sha256=digest(ROOT/'configuration.json'),files=frozen_hashes,
          new_source_evaluations_at_freeze=0,primary_prediction='quadratic',secondary_prediction='linear diagnostic'))
    write(ROOT/'progress.json',dict(state='predictions_frozen',completed_events=0,total=252))
    print(json.dumps(dict(state='predictions_frozen',theta=theta,fraction=fraction,offset=target,quadratic_weights=quad_weights,checks=len(rows),inputs=len(inputs))),flush=True)


def virtual(parameters):
    identity=source.physics.event_owner.inherited.virtual_identity(parameters)
    key=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    matches=[]
    for directory in sorted(set([*BRANCH.glob('*/virtual-cache'),ROOT/'virtual-cache'])):
        path=directory/key[:2]/(key+'.json')
        if path.exists():
            values=read(path)
            assert values['identity']==identity and values['finite'] and np.isfinite(values['scalar'])
            matches.append((path,values))
    if matches:
        assert all(item[1]['scalar']==matches[0][1]['scalar'] for item in matches)
        return matches[0][1]['scalar'],matches[0][0],False
    tensor,response=source.physics.weak.source.virtual_map(parameters,2)
    assert np.isfinite(tensor).all() and np.isfinite(response).all()
    path=ROOT/'virtual-cache'/key[:2]/(key+'.json')
    write(path,dict(identity=identity,scalar=float(response[0,0]),finite=True))
    return float(response[0,0]),path,True


def run(worker,seconds,central_only):
    config=protocol()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert digest(ROOT/'configuration.json')==manifest['configuration_sha256']
    original,theta=source.context(config['target_fraction'])
    histories={(model,grid):read(ROOT/f'histories/{model}-{grid}.json') for model in ('heavy','cold') for grid in GRIDS}
    bundle=coefficient_bundle(original,histories)
    frozen=packet(ROOT/'frozen/history-coefficients.npz')
    assert np.array_equal(bundle.high,frozen['high']) and np.array_equal(bundle.low,frozen['low'])
    source.physics.precise_state=precise.precise_state
    evaluators=cached.models(bundle)
    order=[3] if central_only else [3,4,2,1,5,0,6]
    events=[row for frequency_index in order for row in config['events'] if row['frequency_index']==frequency_index]
    began=time.monotonic()
    done=0
    for ordinal,row in enumerate(events):
        if ordinal%2!=worker:continue
        path=ROOT/f"events/frequency-{row['frequency_index']}/event-{row['event']:02d}.npz"
        if path.exists():
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            continue
        if time.monotonic()-began>=seconds:break
        started=datetime.now(timezone.utc).isoformat()
        assert datetime.fromisoformat(started)>datetime.fromisoformat(manifest['frozen_at'])
        tick=time.monotonic()
        parameters,weight=source.physics.parameters_and_weight(theta,row['node'])
        scalar,loop_path,new_loop=virtual(parameters)
        high,low,diagnostics=microscopic.weighted(parameters,bundle,evaluators,scalar,weight)
        checks=[]
        for name,value in diagnostics.items():check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
        check(checks,'shape',int(high.shape!=low.shape or high.shape!=(3,6,98,4)),0,'integrity')
        check(checks,'zero-history source exactly zero',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'negative_control')
        save(path,high=high,low=low,theta=theta,weight=weight,node=json.dumps(row['node'],sort_keys=True))
        failed=[record for record in checks if not record['passed']]
        write(path.with_suffix('.json'),dict(sha256=digest(path),checks=checks,failed_checks=failed,
              started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),seconds=time.monotonic()-tick,
              worker=worker,loop_path=str(loop_path),loop_sha256=digest(loop_path),new_virtual_integral=new_loop))
        done+=1
        write(ROOT/f'workers/worker-{worker}.json',dict(state='running',completed_this_call=done,last_frequency=row['frequency_index'],last_event=row['event']))
        print(json.dumps(dict(worker=worker,frequency=row['node']['frequency'],event=row['event'],seconds=time.monotonic()-tick,failed_checks=len(failed))),flush=True)
        assert not failed,failed
    write(ROOT/f'workers/worker-{worker}.json',dict(state='stopped',completed_this_call=done,central_only=central_only,stopped_at=datetime.now(timezone.utc).isoformat()))


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0)
    parser.add_argument('--seconds',type=float,default=7200)
    parser.add_argument('--central-only',action='store_true')
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    else:run(args.worker,args.seconds,args.central_only)
