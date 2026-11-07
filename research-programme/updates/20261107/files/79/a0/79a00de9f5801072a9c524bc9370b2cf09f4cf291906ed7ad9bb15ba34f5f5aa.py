from precise_history201 import *
import source201 as base
import assess201 as assessment
OWN=ROOT/'precision-representation'


def frozen():
    base.protocol()
    config=read(OWN/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(OWN/name)==value,name
    return config


def setup():
    original,theta=source.context(.90625)
    features=Features(original)
    prediction=Bundle(features,coefficients(original,'prediction'),original.inputs)
    actual=Bundle(features,coefficients(original,'actual'),original.inputs)
    return original,theta,prediction,actual


def prepare():
    assert not (OWN/'configuration.json').exists()
    config=copy.deepcopy(base.protocol())
    original,theta,prediction,actual=setup()
    rows=[]
    probes=np.geomspace(1e-6,60.,79)
    unused,unused_theta,old_predictions,old_actuals,unused_rows=base.histories()
    old_group=microscopic.crossed.HistoryGroup(old_actuals)
    check(rows,'same sampled spectrum map to roundoff',np.linalg.norm(actual.functions(probes)-old_group.functions(probes))/np.linalg.norm(old_group.functions(probes)),1e-10,'identity')
    for join in range(2):
        features=prediction.features.evaluate(probes[30:33],join)
        sample_rows=np.column_stack([features,np.array([.5,-.5,1.])])
        output=actual.apply(sample_rows,join)
        columns=np.arange(join,actual.high.shape[1],2)
        with mp.workdps(80):
            reference=np.array([[float(mp.fsum(mp.mpf(float(value))*(mp.mpf(float(high))+mp.mpf(float(low))) for value,high,low in zip(row,actual.high[:,column],actual.low[:,column]))) for column in columns] for row in sample_rows])
        check(rows,f'join{join}:compensated contraction versus80digit',np.linalg.norm(output-reference)/np.linalg.norm(reference),1e-10,'identity')
    config['protocol_hashes']={('../'+name):digest(ROOT/name) for name in ('source201.py','assess201.py','precise_history201.py','repair201.py','ACCEPTANCE.md','ANALYSIS-CONTRACT.md','PRECISION-REPRESENTATION.md')}
    config['precision_repair']=True
    config['retained_failed_attempt']=str(ROOT/'results/source-assessment.json')
    config['retained_failed_attempt_sha256']=digest(ROOT/'results/source-assessment.json')
    write(OWN/'configuration.json',config)
    write(OWN/'results/representation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    assert all(row['passed'] for row in rows),rows
    write(OWN/'frozen/analysis-protocol.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),hashes={('../'+name):digest(ROOT/name) for name in ('assess201.py','ANALYSIS-CONTRACT.md')}))
    write(OWN/'progress.json',dict(state='precision_representation_prepared'))
    print(json.dumps(dict(checks=rows)),flush=True)


def event(bundle,theta,node_index,kind):
    config=frozen();node=config['nodes'][node_index]
    parameters,weight=source.physics.parameters_and_weight(theta,node)
    entry=config['loops'][node_index]
    assert digest(entry['path'])==entry['sha256'] and weight==entry['weight']
    loop=read(entry['path'])
    assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
    source.physics.precise_state=precise_state
    began=time.monotonic()
    high,low,diagnostics=microscopic.weighted(parameters,bundle,models(bundle),loop['scalar'],weight)
    checks=[]
    for name,value in diagnostics.items():check(checks,name,value,1e-10,'identity')
    if kind=='prediction':check(checks,'zero history gives exactly zero source',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'identity')
    check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
    return (high,low),dict(checks=checks,failed_checks=[row for row in checks if not row['passed']],
        loop_path=entry['path'],loop_sha256=entry['sha256'],new_virtual_integrals=0,
        seconds=time.monotonic()-began,finished_utc=datetime.now(timezone.utc).isoformat())


def pilot():
    config=frozen();original,theta,prediction,actual=setup()
    outputs=[]
    for kind,bundle in [('prediction',prediction),('actual',actual)]:
        pair,record=event(bundle,theta,0,kind)
        path=OWN/f'pilot/{kind}.npz'
        save(path,high=pair[0],low=pair[1]);record['sha256']=digest(path)
        write(path.with_suffix('.json'),record)
        assert not record['failed_checks'],record['failed_checks']
        outputs.append(pair)
        print(json.dumps(dict(pilot=kind,seconds=record['seconds'])),flush=True)
    predicted=tuple(np.stack([combine([(outputs[0][0][2*grid],outputs[0][1][2*grid]),
                  (outputs[0][0][2*grid+1],outputs[0][1][2*grid+1])])[component] for grid in range(2)]) for component in (0,1))
    observed=tuple(np.stack([combine([(outputs[1][0][grid+1],outputs[1][1][grid+1]),
                  (-outputs[1][0][0],-outputs[1][1][0])])[component] for grid in range(2)]) for component in (0,1))
    difference=assessment.subtract(predicted,observed)
    factor=linear.cholesky(original.basis.mass,lower=True)
    rows=[]
    for label,measure in [('photon',lambda values:assessment.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        relative=measure(difference[0]+difference[1])/np.maximum(measure(outputs[1][0][1:]+outputs[1][1][1:]),1e-300)
        correction=measure(difference[0]+difference[1])/np.maximum(measure(observed[0]+observed[1]),1e-300)
        check(rows,label+':pilot absolute reconstruction',relative.max(),1e-10)
        check(rows,label+':pilot correction prediction',correction.max(),.01)
    write(OWN/'pilot/validation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],post_test_diagnostic=True))
    print(json.dumps(dict(pilot_checks=rows)),flush=True)


def run(kind,seconds,limit):
    config=frozen()
    assert not read(OWN/'pilot/validation.json')['failed_checks']
    if kind=='actual':
        manifest=read(OWN/'frozen/prediction-manifest.json')
        for name,value in manifest['files'].items():assert digest(OWN/name)==value
    original,theta,prediction,actual=setup()
    bundle=prediction if kind=='prediction' else actual
    began=time.monotonic();completed=0
    for index in range(36):
        path=OWN/f'{kind}/event-{index:02d}.npz'
        if path.exists():
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            continue
        if completed>=limit or time.monotonic()-began>=seconds:
            write(OWN/'progress.json',dict(state='safe_restart',phase=kind,next_event=index));return
        pair,record=event(bundle,theta,index,kind)
        save(path,high=pair[0],low=pair[1],theta=theta,weight=config['loops'][index]['weight'],node=json.dumps(config['nodes'][index],sort_keys=True))
        record['sha256']=digest(path)
        write(path.with_suffix('.json'),record)
        assert not record['failed_checks'],record['failed_checks']
        completed+=1
        write(OWN/'progress.json',dict(state='evaluating',phase=kind,done=index+1,total=36))
        print(json.dumps(dict(phase=kind,event=index,seconds=record['seconds'])),flush=True)
    write(OWN/'progress.json',dict(state=kind+'_complete'))


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','pilot','prediction','freeze','actual','assess'])
    parser.add_argument('--seconds',type=float,default=3600)
    parser.add_argument('--max-events',type=int,default=36)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.phase=='pilot':pilot()
    elif args.phase=='freeze':
        base.ROOT=OWN;base.freeze()
    elif args.phase=='assess':
        base.ROOT=OWN;assessment.ROOT=OWN;assessment.main()
    else:run(args.phase,args.seconds,args.max_events)
