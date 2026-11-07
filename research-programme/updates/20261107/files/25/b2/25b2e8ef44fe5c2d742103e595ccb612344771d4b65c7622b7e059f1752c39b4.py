from lift214 import *
import lift214 as pilot
EXT=ROOT/'full-node'


def node_protocol():
    config=protocol()
    extension=read(EXT/'configuration.json')
    for name,value in extension['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    assert digest(ROOT/'results/assessment.json')==extension['pilot_assessment_sha256']
    assert read(ROOT/'results/assessment.json')['qualified']
    return config,extension


def prepare_node():
    config=protocol()
    assert not (EXT/'configuration.json').exists()
    assert read(ROOT/'results/assessment.json')['qualified']
    previous=read(PARENT/'configuration.json')
    events=[]
    for row in previous['target']:
        report_path=PARENT/f"target/frequency-6/event-{row['event']:02d}.json"
        report=read(report_path)
        assert not report['failed_checks']
        assert digest(report_path.with_suffix('.npz'))==report['sha256']
        assert digest(report['loop_path'])==report['loop_sha256']
        events.append(dict(**row,loop_path=report['loop_path'],loop_sha256=report['loop_sha256'],
                           direct_path=str(report_path.with_suffix('.npz')),direct_sha256=report['sha256']))
    assert len(events)==36 and [row['event'] for row in events]==list(range(36))
    write(EXT/'configuration.json',dict(stage=214,scope='complete36-event one-frequency operator',
          frozen_at=now(),pilot_assessment_sha256=digest(ROOT/'results/assessment.json'),
          events=events,safe_stop_utc='2026-10-25T20:00:00+00:00',
          protocol_hashes={name:digest(ROOT/name) for name in ('node214.py','FULL-NODE-CONTRACT.md')},
          reused_pilot_matrix_sha256=digest(ROOT/'results/operator.npz'),single_worker=True,
          original_bank_changed=False,grids_changed=False,tolerances_changed=False))
    write(EXT/'progress.json',dict(state='prepared',events_complete=1,pilot_event_reused=0))
    print(json.dumps(dict(state='full_node_prepared',new_events=35,reused_events=1)),flush=True)


def event_operator(row,bundle,evaluators):
    parameters,weight=source.physics.parameters_and_weight(row['theta'],row['node'])
    assert weight==row['weight'] and digest(row['loop_path'])==row['loop_sha256']
    loop=read(row['loop_path'])
    assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    started=now()
    began=time.monotonic()
    high,low,diagnostics=source.evaluate(parameters,bundle,evaluators,loop['scalar'])
    high,low=source.precise_combine([(high,low)],[-weight])
    assert high.shape==low.shape==(6,98,196)
    high,low=high.reshape(6,98,98,2),low.reshape(6,98,98,2)
    rows=[]
    for name,value in diagnostics.items():
        check(rows,name,value,1e-10,'identity')
    check(rows,'padded zero input',np.max(abs(high[:,:,97]))+np.max(abs(low[:,:,97])),0,'negative_control')
    high,low=high[:,:,:97,:],low[:,:,:97,:]
    check(rows,'matrix finite',int(not np.isfinite(high+low).all()),0,'integrity')
    path=EXT/f"events/event-{row['event']:02d}.npz"
    save(path,high=high,low=low,theta=row['theta'],weight=weight)
    report=dict(started_at=started,finished_at=now(),seconds=time.monotonic()-began,
                checks=rows,failed_checks=[entry for entry in rows if not entry['passed']],
                sha256=digest(path),loop_path=row['loop_path'],loop_sha256=row['loop_sha256'],
                new_virtual_integrals=0,event=row['event'])
    write(path.with_suffix('.json'),report)
    print(json.dumps(dict(event=row['event'],seconds=report['seconds'],failed=len(report['failed_checks']))),flush=True)
    assert not report['failed_checks'],report['failed_checks']


def run_node():
    config,extension=node_protocol()
    original,theta=source.context(config['target_fraction'])
    bundle=OperatorBundle(cached.CachedFeatures(original),original.inputs)
    evaluators=cached.models(bundle)
    source.physics.precise_state=precise.precise_state
    for row in extension['events'][1:]:
        path=EXT/f"events/event-{row['event']:02d}.npz"
        if path.exists():
            report=read(path.with_suffix('.json'))
            assert digest(path)==report['sha256'] and not report['failed_checks']
            continue
        if datetime.now(timezone.utc)>=datetime.fromisoformat(extension['safe_stop_utc']):
            break
        event_operator(row,bundle,evaluators)
        write(EXT/'progress.json',dict(state='running',events_complete=len(list((EXT/'events').glob('*.npz')))+1,last_event=row['event'],pid=os.getpid()))
    import psutil
    memory=psutil.Process().memory_info()
    complete=len(list((EXT/'events').glob('*.npz')))+1
    write(EXT/'progress.json',dict(state='constructed' if complete==36 else 'saved_partial',events_complete=complete,
          peak_working_set_bytes=getattr(memory,'peak_wset',memory.rss),active_worker=False,stopped_at=now()))
    print(json.dumps(dict(events_complete=complete,peak_working_set_bytes=getattr(memory,'peak_wset',memory.rss))),flush=True)


def pairs():
    config,extension=node_protocol()
    output=[]
    provenance={}
    for row in extension['events']:
        path=ROOT/'results/operator.npz' if row['event']==0 else EXT/f"events/event-{row['event']:02d}.npz"
        expected=extension['reused_pilot_matrix_sha256'] if row['event']==0 else read(path.with_suffix('.json'))['sha256']
        assert digest(path)==expected
        values=packet(path)
        output.append((values['high'],values['low']))
        provenance[str(path)]=expected
    return output,provenance


def matrix_sum(values):
    total=metrics.combine([(high[:4],low[:4]) for high,low in values])
    parts=[(total[0][index],total[1][index]) for index in range(4)]
    parts.extend([metrics.combine(parts[1:4]),metrics.combine(parts[:4])])
    return tuple(np.stack([part[index] for part in parts]) for index in range(2))


def freeze_node():
    config,extension=node_protocol()
    assert not (EXT/'frozen/manifest.json').exists()
    matrices,hashes=pairs()
    coefficients=packet(ROOT/'frozen/history-coefficients.npz')
    prediction_pairs=[]
    for event,matrix in enumerate(matrices):
        if event==0:
            values=packet(ROOT/'frozen/replay-prediction.npz')
            prediction=(values['high'],values['low'])
        else:
            prediction=contract(*matrix,coefficients)
        path=EXT/f'frozen/prediction-{event:02d}.npz'
        save(path,high=prediction[0],low=prediction[1])
        hashes[str(path)]=digest(path)
        prediction_pairs.append(prediction)
    total=matrix_sum(matrices)
    path=EXT/'results/operator-node.npz'
    save(path,high=total[0],low=total[1],active=np.array(ACTIVE),theta=config['theta'],frequency=config['event']['frequency'])
    hashes[str(path)]=digest(path)
    prediction=contract(*total,coefficients)
    path=EXT/'frozen/node-prediction.npz'
    save(path,high=prediction[0],low=prediction[1])
    hashes[str(path)]=digest(path)
    summed=metrics.primitives(prediction_pairs)
    path=EXT/'frozen/event-first-prediction.npz'
    save(path,high=summed[0],low=summed[1])
    hashes[str(path)]=digest(path)
    write(EXT/'frozen/manifest.json',dict(frozen_at=now(),files=hashes,configuration_sha256=digest(EXT/'configuration.json'),
                replay_not_holdout=True,events=36,contraction_digits=80))
    print(json.dumps(dict(state='full_node_predictions_frozen',events=36)),flush=True)


def compare(scope,prediction,actual,factor,checks,records):
    error=metrics.subtract(prediction,actual)
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            records.append(dict(scope=scope,grid=('half','quarter')[grid],component=COMPONENTS[component],
                    background=('heavy','cold')[column//2],join=column%2,measure=name,relative=value))
            check(checks,f'{scope}:{grid}:{component}:{column}:{name}',value,1e-10,'representation')
    check(checks,scope+':zero history',np.max(abs(prediction[0][-1]))+np.max(abs(prediction[1][-1])),0,'negative_control')


def matrix_identities(matrix,basis,checks):
    with mp.workdps(80):
        norm0,norm1=[mp.mpf(float(value)) for value in basis['norms'][:2]]
        mean=mp.mpf(float(basis['mean']))
        maxima={'moment':0.,'exchange':0.,'component_sum':0.}
        for component,index,join in np.ndindex(6,97,2):
            values={row:mp.mpf(float(matrix['high'][component,row,index,join]))+mp.mpf(float(matrix['low'][component,row,index,join])) for row in (0,1,2,97)}
            terms=[values[0],-mean*norm0*values[1],-norm1*values[2]]
            maxima['moment']=max(maxima['moment'],float(abs(mp.fsum(terms))/max(sum(abs(value) for value in terms),mp.mpf('1e-300'))))
            maxima['exchange']=max(maxima['exchange'],float(abs(values[0]+values[97])/max(abs(values[0]),abs(values[97]),mp.mpf('1e-300'))))
        for component,members in ((4,[1,2,3]),(5,[0,1,2,3])):
            expected=metrics.combine([(matrix['high'][index],matrix['low'][index]) for index in members])
            difference=metrics.subtract((matrix['high'][component],matrix['low'][component]),expected)
            scale=np.max(abs(expected[0]+expected[1]))
            maxima['component_sum']=max(maxima['component_sum'],float(np.max(abs(difference[0]+difference[1]))/max(scale,1e-300)))
    for name,value in maxima.items():
        check(checks,'full operator column '+name,value,1e-10,'identity')
    return maxima


def assess_node():
    config,extension=node_protocol()
    assert not (EXT/'results/assessment.json').exists()
    manifest=read(EXT/'frozen/manifest.json')
    assert digest(EXT/'configuration.json')==manifest['configuration_sha256']
    for name,value in manifest['files'].items():
        assert digest(name)==value,name
    basis=packet(ROOT/'frozen/basis-metric.npz')
    factor=linear.cholesky(basis['mass'],lower=True)
    checks=[]
    records=[]
    direct_pairs=[]
    for row in extension['events']:
        event=row['event']
        if event!=0:
            checks.extend(dict(entry,name=f"construction{event}:"+entry['name']) for entry in read(EXT/f'events/event-{event:02d}.json')['checks'])
        assert digest(row['direct_path'])==row['direct_sha256']
        direct=packet(row['direct_path'])
        actual=(direct['high'],direct['low'])
        direct_pairs.append(actual)
        prediction=packet(EXT/f'frozen/prediction-{event:02d}.npz')
        compare(f'event-{event}',(prediction['high'],prediction['low']),actual,factor,checks,records)
    direct_sum=metrics.primitives(direct_pairs)
    saved_node=packet(PARENT/'results/source-node-6.npz')
    compare('saved-source-reconstruction',direct_sum,(saved_node['actual_high'],saved_node['actual_low']),factor,checks,records)
    prediction=packet(EXT/'frozen/node-prediction.npz')
    predicted=(prediction['high'],prediction['low'])
    compare('full-node',predicted,direct_sum,factor,checks,records)
    event_first=packet(EXT/'frozen/event-first-prediction.npz')
    compare('contract-before-after-sum',predicted,(event_first['high'],event_first['low']),factor,checks,records)
    column_identities=matrix_identities(packet(EXT/'results/operator-node.npz'),basis,checks)
    failed=[entry for entry in checks if not entry['passed']]
    report=dict(stage=214,state='full_node_operator_qualified' if not failed else 'full_node_representation_rejected',
                qualified=not failed,checks=checks,failed_checks=failed,records=records,column_identities=column_identities,
                events=36,reused_events=1,new_events=35,new_virtual_integrals=0,
                original_bank_changed=False,grids_changed=False,tolerances_changed=False,
                all_frequency_operator=False,uniform_temperature_operator=False,permission_to_propagate=False)
    write(EXT/'results/assessment.json',report)
    write(EXT/'progress.json',dict(state=report['state'],events_complete=36,active_worker=False,finished_at=now()))
    print(json.dumps(dict(state=report['state'],checks=len(checks),failed=len(failed),
        full_node={component:max(row['relative'] for row in records if row['scope']=='full-node' and row['component']==component) for component in COMPONENTS},
        column_identities=column_identities)),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run','freeze','assess'])
    args=parser.parse_args()
    {'prepare':prepare_node,'run':run_node,'freeze':freeze_node,'assess':assess_node}[args.phase]()
