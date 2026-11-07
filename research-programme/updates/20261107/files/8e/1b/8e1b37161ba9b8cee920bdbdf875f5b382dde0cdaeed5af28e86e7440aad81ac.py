from connection208 import *


def setup():
    config=protocol()
    original,theta=source.context(config['target_fraction'])
    target=packet(ROOT/'frozen/history-coefficients.npz')
    pairs=[]
    paths=[]
    for offset,directory in zip(config['anchor_offsets'],(HISTORY,WARM,WARM/'cold-side-midpoint')):
        fraction=.875-offset/math.log(10)
        anchor,unused=source.context(fraction)
        assert np.array_equal(anchor.basis.mass,original.basis.mass)
        assert np.array_equal(anchor.epochs[0].frequency,original.epochs[0].frequency)
        histories={}
        for model in ('heavy','cold'):
            for grid in GRIDS:
                path=directory/f'histories/{model}/{grid}/complete.json'
                histories[(model,grid)]=read(path)
                assert not histories[(model,grid)]['failed_checks']
                assert abs(histories[(model,grid)]['coordinate']-anchor.epochs[0].coordinate)<1e-13
                paths.append(path)
        bundle=coefficient_bundle(anchor,histories)
        pairs.append((bundle.high,bundle.low))
        paths.extend(anchor.inputs)
    errors={}
    for method,coefficients,anchors in [('quadratic',config['quadratic_weights'],pairs),('linear',config['linear_weights'],pairs[:2])]:
        curve=combine([scaled(pair,weight) for pair,weight in zip(anchors,coefficients)])
        errors[method]=metrics.subtract(curve,(target['high'],target['low']))
    groups=[]
    with mp.workdps(80):
        for grid in range(2):
            for sector in ('photon','gas'):
                for column in range(4*grid,4*grid+4):
                    values=[mp.mpf(float(high))+mp.mpf(float(low)) for high,low in zip(errors['quadratic'][0][:,column],errors['quadratic'][1][:,column])]
                    if sector=='photon':values[-1]=mp.mpf(0)
                    else:values=[mp.mpf(0)]*98+[values[-1]]
                    groups.append(values)
        for column in range(8):
            groups.append([mp.mpf(float(high))+mp.mpf(float(low)) for high,low in zip(errors['linear'][0][:,column],errors['linear'][1][:,column])])
        groups.extend([[mp.mpf(0)]*99 for unused in range(4)])
    bundle=cached.CachedBundle(cached.CachedFeatures(original),groups,original.inputs)
    return original,theta,bundle,errors,paths


def prepare():
    assert not (ROOT/'diagnostic/configuration.json').exists()
    failed=read(ROOT/'results/assessment-036.json')
    assert failed['state']=='forecast_rejected' and not failed['permission_to_propagate']
    original,theta,bundle,errors,paths=setup()
    save(ROOT/'diagnostic/frozen/coefficients.npz',high=bundle.high,low=bundle.low)
    records=[]
    mass=original.basis.mass
    target=packet(ROOT/'frozen/history-coefficients.npz')
    for method,pair in errors.items():
        values=pair[0]+pair[1]
        for grid in range(2):
            for index,model in enumerate(('heavy','cold')):
                column=4*grid+2*index
                reference=target['high'][:,column]+target['low'][:,column]
                norm=lambda value:math.sqrt(float(value[:96]@mass@value[:96]))
                records.append(dict(method=method,grid=GRIDS[grid],model=model,
                    profile_relative=norm(values[:,column])/norm(reference),
                    gas_relative=float(abs(values[-1,column]/reference[-1]))))
    write(ROOT/'diagnostic/history-errors.json',dict(post_test_diagnostic=True,records=records))
    inputs={str(path):digest(path) for path in set(paths)}
    config=dict(prepared_at=datetime.now(timezone.utc).isoformat(),post_test_diagnostic=True,
                source_assessment_sha256=digest(ROOT/'results/assessment-036.json'),
                parent_configuration_sha256=digest(ROOT/'configuration.json'),
                script_sha256=digest(Path(__file__)),derivation_sha256=digest(ROOT/'ERROR-DECOMPOSITION.md'),
                coefficient_sha256=digest(ROOT/'diagnostic/frozen/coefficients.npz'),input_hashes=inputs,
                new_virtual_integrals_allowed=0,original_forecast_still_rejected=True)
    write(ROOT/'diagnostic/configuration.json',config)
    print(json.dumps(dict(state='diagnostic_prepared',history_errors=records)),flush=True)


def verify():
    config=read(ROOT/'diagnostic/configuration.json')
    assert digest(Path(__file__))==config['script_sha256']
    assert digest(ROOT/'ERROR-DECOMPOSITION.md')==config['derivation_sha256']
    assert digest(ROOT/'results/assessment-036.json')==config['source_assessment_sha256']
    assert digest(ROOT/'configuration.json')==config['parent_configuration_sha256']
    assert digest(ROOT/'diagnostic/frozen/coefficients.npz')==config['coefficient_sha256']
    for name,value in config['input_hashes'].items():assert digest(name)==value,name
    return config


def run(worker,seconds):
    verify()
    config=protocol()
    original,theta,bundle,unused,paths=setup()
    frozen=packet(ROOT/'diagnostic/frozen/coefficients.npz')
    assert np.array_equal(bundle.high,frozen['high']) and np.array_equal(bundle.low,frozen['low'])
    source.physics.precise_state=precise.precise_state
    evaluators=cached.models(bundle)
    started=time.monotonic()
    for event in range(worker,36,2):
        path=ROOT/f'diagnostic/events/event-{event:02d}.npz'
        if path.exists():
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            continue
        if time.monotonic()-started>=seconds:break
        row=next(row for row in config['events'] if row['frequency_index']==3 and row['event']==event)
        control=read(ROOT/f'events/frequency-3/event-{event:02d}.json')
        parameters,weight=source.physics.parameters_and_weight(theta,row['node'])
        loop=read(control['loop_path'])
        assert digest(control['loop_path'])==control['loop_sha256']
        assert loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        tick=time.monotonic()
        high,low,diagnostics=microscopic.weighted(parameters,bundle,evaluators,loop['scalar'],weight)
        checks=[]
        for name,value in diagnostics.items():check(checks,name,value,1e-10,'identity')
        check(checks,'finite',int(not np.isfinite(high+low).all()),0,'integrity')
        check(checks,'shape',int(high.shape!=low.shape or high.shape!=(7,6,98,4)),0,'integrity')
        check(checks,'zero history exactly zero',np.max(abs(high[-1]))+np.max(abs(low[-1])),0,'negative_control')
        save(path,high=high,low=low)
        failed=[item for item in checks if not item['passed']]
        write(path.with_suffix('.json'),dict(sha256=digest(path),checks=checks,failed_checks=failed,
              loop_path=control['loop_path'],loop_sha256=control['loop_sha256'],new_virtual_integrals=0,seconds=time.monotonic()-tick,worker=worker))
        print(json.dumps(dict(worker=worker,event=event,seconds=time.monotonic()-tick,failed_checks=len(failed))),flush=True)
        assert not failed,failed


def assess():
    verify();config=protocol()
    parts=[];checks=[]
    for event in range(36):
        path=ROOT/f'diagnostic/events/event-{event:02d}.npz'
        record=read(path.with_suffix('.json'))
        assert digest(path)==record['sha256'] and not record['failed_checks']
        values=packet(path);parts.append((values['high'],values['low']))
        checks.extend(dict(row,name=f'{event}:'+row['name']) for row in record['checks'])
    source_parts=metrics.primitives(parts)
    actual_data=packet(ROOT/'results/source-3.npz')
    actual=(actual_data['high'],actual_data['low'])
    original,unused=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    measurements=[('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]
    records=[];outputs={}
    for method in ('quadratic','linear'):
        frozen=[packet(ROOT/f'frozen/frequency-3/event-{event:02d}.npz') for event in range(36)]
        predicted=metrics.primitives([(value[method+'_high'],value[method+'_low']) for value in frozen])
        error=metrics.subtract(predicted,actual)
        if method=='quadratic':
            pairs=[combine([(source_parts[0][2*grid],source_parts[1][2*grid]),(source_parts[0][2*grid+1],source_parts[1][2*grid+1])]) for grid in range(2)]
            history=(np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs]))
        else:history=(source_parts[0][4:6],source_parts[1][4:6])
        remainder=metrics.subtract(error,history)
        closure=metrics.subtract(error,combine([history,remainder]))
        for name,operation in measurements:
            denominator=np.maximum(operation(actual[0]+actual[1]),1e-300)
            check(checks,method+':'+name+':decomposition arithmetic',np.max(operation(closure[0]+closure[1])/denominator),1e-10,'identity')
            values={label:operation(pair[0]+pair[1])/denominator for label,pair in [('total_error',error),('history',history),('remaining',remainder)]}
            for grid,component,column in np.ndindex(denominator.shape):
                records.append(dict(method=method,measure=name,grid=GRIDS[grid],component=COMPONENTS[component],
                    model=('heavy','cold')[column//2],join=column%2,**{label:float(value[grid,component,column]) for label,value in values.items()}))
        for label,pair in [('error',error),('history',history),('remaining',remainder)]:
            outputs[method+'_'+label+'_high']=pair[0];outputs[method+'_'+label+'_low']=pair[1]
    save(ROOT/'diagnostic/decomposition.npz',**outputs,parts_high=source_parts[0],parts_low=source_parts[1])
    write(ROOT/'diagnostic/assessment.json',dict(checks=checks,failed_checks=[row for row in checks if not row['passed']],records=records,
          post_test_diagnostic=True,original_forecast_still_rejected=True,permission_to_propagate=False,new_virtual_integrals=0,
          remainder_includes_operator_change_and_anchor_arithmetic=True))
    print(json.dumps(dict(checks=len(checks),failed=sum(not row['passed'] for row in checks),
          summary={method:{component:max(row['remaining'] for row in records if row['method']==method and row['component']==component) for component in ('baseline','MTS','total')} for method in ('quadratic','linear')})),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','run','assess'])
    parser.add_argument('--worker',type=int,choices=[0,1],default=0);parser.add_argument('--seconds',type=float,default=5400)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.phase=='assess':assess()
    else:run(args.worker,args.seconds)
