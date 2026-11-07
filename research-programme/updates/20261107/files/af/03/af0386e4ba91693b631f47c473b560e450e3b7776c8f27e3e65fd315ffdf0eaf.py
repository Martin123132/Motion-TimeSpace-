from refine222 import *
from bisect import bisect_right
sys.path.insert(0,str(PARENT))
import response221 as old
from types import SimpleNamespace
linear=old.linear
MODELS=old.MODELS
FIRST,LAST,FINE,WIDTH=old.FIRST,old.LAST,old.FINE,old.WIDTH

def prepare_response():
    protocol()
    path=ROOT/'response-configuration.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),script_sha256=digest(__file__),derivation_sha256=digest(ROOT/'RESPONSE-DERIVATION.md'),
        parent_config_sha256=digest(PARENT/'configuration.json'),counts=[2048,4096],
        profiles=list(old.PROFILES),history_slots=['quarter','eighth','zero'],
        quarter_forecast={model:{str(count):digest(PARENT/f'causal-startup/responses/{model}-{count}/increment-readout.npz')
                            for count in (2048,4096)} for model in MODELS},
        comparison_tolerance=.01,identity_tolerance=1e-10,bank_changed=False,temperature_curve_changed=False))

def response_protocol():
    protocol()
    config=read(ROOT/'response-configuration.json')
    assert digest(__file__)==config['script_sha256']
    assert digest(ROOT/'RESPONSE-DERIVATION.md')==config['derivation_sha256']
    assert digest(PARENT/'configuration.json')==config['parent_config_sha256']
    for model,counts in config['quarter_forecast'].items():
        for count,value in counts.items():
            assert digest(PARENT/f'causal-startup/responses/{model}-{count}/increment-readout.npz')==value
    return config

def history_points(model):
    config=protocol()
    folder=ROOT/f'histories/{model}/eighth'
    complete=read(folder/'complete.json')
    seed_path=ROOT/f'frozen/{model}-seed.json'
    verify_restart(folder,complete,digest(seed_path))
    seed=read(seed_path)
    points=[dict(coordinate=seed['previous_coordinate'],state=seed['older']),dict(coordinate=seed['coordinate'],state=seed['current'])]
    for path in sorted((folder/'blocks').glob('*.json')):
        points.extend(read(path)['states'])
    assert len(points)==complete['done']+2
    return points

def sample(points,target,equation,transition,model):
    coordinates=[point['coordinate'] for point in points]
    left=bisect_right(coordinates,target)-1
    assert left>=1
    current=history.parse_state(points[left]['state'])
    older=history.parse_state(points[left-1]['state'])
    rows=[]
    if coordinates[left]==target:
        result=current
        method='exact saved eighth-grid state'
    else:
        delta=mp.mpf(target)-mp.mpf(coordinates[left])
        previous_delta=mp.mpf(coordinates[left])-mp.mpf(coordinates[left-1])
        result,diagnostic=equation.advance(current,older,mp.mpf(target),delta,previous_delta)
        rows.extend(history.identity_rows([dict(diagnostic,ordinal=left)]))
        with mp.workdps(100):
            audit_equation=Equation(model,transition)
            audit,unused=audit_equation.advance(current,older,mp.mpf(target),delta,previous_delta)
            norm=lambda value:mp.sqrt(mp.fsum(entry*entry for entry in value))
            check(rows,'sample80/100 profile',norm(result['profile']-audit['profile'])/norm(audit['profile']),1e-10)
            check(rows,'sample80/100 gas',(result['gas']-audit['gas'])/max(abs(audit['gas']),mp.mpf('1e-90')),1e-10)
        method='one original-equation partial step from saved eighth BDF2 pair'
    return dict(current=history.previous.serial_state(result),coordinate=target,left_coordinate=coordinates[left],
                previous_coordinate=coordinates[left-1],method=method,checks=rows)

def old_values(model,index):
    if index==FIRST:
        folder=PARENT/f'causal-startup/left/{model}'
        report=read(folder/'result.json')
        assert digest(folder/'source.npz')==report['source_sha256']
        assert digest(folder/'coefficients.npz')==report['coefficients_sha256']
        return packet(folder/'source.npz'),packet(folder/'coefficients.npz')
    values,report=old.verify_point(model,index)
    assert not report['failed_checks']
    return values,packet(old.point_folder(model,index)/'coefficients.npz')

def verify_source(model,index):
    folder=ROOT/f'sources/{model}/step-{index:04d}'
    report=read(folder/'result.json')
    for name,value in report['file_hashes'].items():
        assert digest(folder/name)==value
    assert not report['failed_checks']
    return packet(folder/'source.npz')

def sources(model):
    response_protocol()
    points=history_points(model)
    config=protocol()
    transition=config['schedules'][model]['transition']
    inputs=read(ROOT/'inputs.json')
    nodes=read(PARENT/'configuration.json')['anchor_offsets']
    anchors=[packet(old.PARENT/f'results/operator-panel-{label}.npz') for label in old.panel.LABELS]
    pairs=[(value['high'],value['low']) for value in anchors]
    began=time.monotonic()
    with mp.workdps(80):
        equation=Equation(model,transition)
        for index in range(FIRST,LAST+1):
            folder=ROOT/f'sources/{model}/step-{index:04d}'
            if (folder/'result.json').exists():
                verify_source(model,index)
                continue
            rows=[]
            fraction=.75+index*.25/FINE
            target=fraction*math.log(10)
            record=sample(points,target,equation,transition,model)
            rows.extend(record['checks'])
            write(folder/'sample.json',record)
            original,theta=old.source.context(fraction)
            basis=packet(old.PARENT/'frozen/basis-metric.npz')
            check(rows,'same retained basis mass',int(not np.array_equal(original.basis.mass,basis['mass'])),0,'integrity')
            for path in original.inputs:
                old.register(inputs,path)
            before=[mp.mpf(float(value)) for value in original.epochs[0].original[model]]
            original_gas=mp.mpf(float(original.gas[MODELS.index(model)]))
            vector=[mp.mpf(value)-reference for value,reference in zip(record['current']['profile'],before)]
            vector.append(mp.mpf(record['current']['gas'])-original_gas)
            coefficients=np.array([[float(value)] for value in vector])
            coefficient_low=np.array([[float(value-mp.mpf(float(value)))] for value in vector])
            prior,prior_coefficients=old_values(model,index)
            high=np.zeros_like(prior['high'])
            low=np.zeros_like(high)
            high[:,0]=prior['high'][:,1]
            low[:,0]=prior['low'][:,1]
            offset=(.875-fraction)*math.log(10)
            quadratic=old.history.weights(offset,nodes)
            secant=old.history.weights(offset,[nodes[0],nodes[2]])
            weights=[quadratic,[secant[0],0.,secant[1]]]
            for profile,weight in enumerate(weights):
                matrix=old.panel.weighted_matrix(pairs,weight)
                for join in (0,1):
                    output=old.api.apply_coefficients(matrix,(coefficients,coefficient_low),join,80)
                    high[profile,1,:,:,join]=output[0][:,:,0]
                    low[profile,1,:,:,join]=output[1][:,:,0]
            check(rows,'quarter source reused exactly',np.max(abs(high[:,0]-prior['high'][:,1]))+np.max(abs(low[:,0]-prior['low'][:,1])),0,'integrity')
            check(rows,'zero source',np.max(abs(high[:,2]))+np.max(abs(low[:,2])),0,'identity')
            check(rows,'finite source',int(not np.isfinite(high).all() or not np.isfinite(low).all()),0,'integrity')
            for component,parts in ((4,[1,2,3]),(5,[0,1,2,3])):
                for profile,grid,join in np.ndindex(2,2,2):
                    actual=old.injection.as_mp(high[profile,grid,component,:,join,None])+old.injection.as_mp(low[profile,grid,component,:,join,None])
                    expected=mp.matrix(98,1)
                    for part in parts:
                        expected+=old.injection.as_mp(high[profile,grid,part,:,join,None])+old.injection.as_mp(low[profile,grid,part,:,join,None])
                    norm=lambda values:mp.sqrt(mp.fsum(value*value for value in values))
                    check(rows,f'component sum:{profile}:{grid}:{component}:{join}',norm(actual-expected)/max(norm(expected),mp.mpf('1e-300')),1e-10,'identity')
            for profile,grid,component,join in np.ndindex(2,2,6,2):
                exact=lambda row:mp.mpf(float(high[profile,grid,component,row,join]))+mp.mpf(float(low[profile,grid,component,row,join]))
                energy=exact(0)
                temperature=original.basis.temperature
                check(rows,f'protected moment:{profile}:{grid}:{component}:{join}',
                      (mp.mpf(float(temperature[0]))*exact(1)+mp.mpf(float(temperature[1]))*exact(2)-energy)/max(abs(energy),mp.mpf('1e-300')),1e-10,'identity')
                check(rows,f'pair:{profile}:{grid}:{component}:{join}',(energy+exact(97))/max(abs(energy),mp.mpf('1e-300')),1e-10,'identity')
            save(folder/'source.npz',high=high,low=low,fraction=fraction,theta=theta)
            save(folder/'eighth-coefficients.npz',high=coefficients,low=coefficient_low)
            write(folder/'result.json',dict(model=model,index=index,checks=rows,failed_checks=[row for row in rows if not row['passed']],
                file_hashes={path.name:digest(path) for path in folder.iterdir() if path.is_file() and path.name!='result.json'}))
            assert all(row['passed'] for row in rows)
            print(json.dumps(dict(model=model,source=index-FIRST+1,total=65,seconds=time.monotonic()-began)),flush=True)
    write(ROOT/f'inputs-source-{model}.json',inputs)

def evolve(model,count):
    response_protocol()
    folder=ROOT/f'responses/{model}-{count}'
    if (folder/'result.json').exists():
        report=read(folder/'result.json')
        for name,value in report['file_hashes'].items():
            assert digest(folder/name)==value
        return
    inputs=read(ROOT/f'inputs-source-{model}.json')
    system=old.matched.System(model,count,inputs)
    left=verify_source(model,FIRST)
    start=round((old.START-.75)*count/.25)
    stop=round((old.STOP-.75)*count/.25)
    current=np.zeros((100,2*WIDTH));previous=current.copy()
    rows=[];maximum=dict(photon=0.,gas=0.,spectral=0.)
    for index in range(start+1,stop+1):
        step=system.make_step(index)
        right=verify_source(model,index*(FINE//count))
        if index==start+1:
            local0=system.background.at(old.START*system.background.end)
            rate0=local0['coefficient']/local0['thermal_parameter']
            combined=old.history.combine([(right['high'],right['low']),old.history.scaled((left['high'],left['low']),rate0/step['rate'])])
            values=dict(high=combined[0],low=combined[1])
            step=dict(step,alpha=2/system.step,restart=True)
            matrix=step['alpha']*system.coordinates.mass-step['rate']*system.coordinates.tests@step['stiffness']@system.coordinates.transform
            step['factor']=linear.lu_factor(matrix)
            step['gas_response']=linear.lu_solve(step['factor'],step['coupling'])
            step['denominator']=step['heat']*(step['alpha']+1)+step['alpha']*step['gas_response'][0]
            assert step['denominator']>0
        else:
            values=right
        supplied=old.pair_source(values,system,rows,f'step{index}')
        updated,diagnostic=system.advance(current,previous,step,supplied,True)
        previous,current=current,updated
        for name,value in diagnostic.items():
            maximum[name]=max(maximum[name],value)
        old.ledger_checks(f'step{index}',current,system,rows)
        collapsed=old.matched.collapsed(current).reshape(100,2,3,6,2)
        check(rows,f'step{index}:zero history',np.max(abs(collapsed[:,:,2])),0,'identity')
        for component,parts in ((4,[1,2,3]),(5,[0,1,2,3])):
            expected=sum(collapsed[:,:,:,part,:] for part in parts)
            check(rows,f'step{index}:component{component}',np.linalg.norm(collapsed[:,:,:,component,:]-expected)/max(np.linalg.norm(expected),1e-300),1e-10,'identity')
        if index in (start+1,start+(stop-start)//2,stop):
            save(folder/f'step-{index}.npz',current=current,previous=previous,index=index)
    for name,limit in read(PARENT/'configuration.json')['unchanged_response_gates'].items():
        check(rows,'response equation:'+name,maximum[name],limit,'equation')
    prior=packet(PARENT/f'causal-startup/responses/{model}-{count}/step-{stop}.npz')
    left_columns=[np.ravel_multi_index((profile,0,component,join),(2,3,6,2)) for profile,component,join in np.ndindex(2,6,2)]
    right_columns=[np.ravel_multi_index((profile,1,component,join),(2,3,6,2)) for profile,component,join in np.ndindex(2,6,2)]
    old.compare_state('quarter branch replay',np.column_stack([current[:,left_columns],current[:,np.array(left_columns)+WIDTH]]),
                      np.column_stack([prior['current'][:,right_columns],prior['current'][:,np.array(right_columns)+WIDTH]]),system,rows)
    reader=old.matched.saved.response.ShapeReadout(system.basis,canonical=True)
    collapsed=old.matched.collapsed(current)
    shapes=reader.apply(system.coordinates.transform@collapsed[:96],collapsed[0])
    save(folder/'increment-readout.npz',**shapes,frequency=reader.frequency,measure=reader.measure,gas=collapsed[96],
         work=collapsed[97],number=collapsed[98],injection=collapsed[99],heat=system.background.chi)
    write(folder/'result.json',dict(model=model,count=count,checks=rows,failed_checks=[row for row in rows if not row['passed']],
        maximum=maximum,file_hashes={path.name:digest(path) for path in folder.glob('*.npz')}))
    write(ROOT/f'inputs-response-{model}-{count}.json',inputs)
    print(json.dumps(dict(model=model,count=count,checks=len(rows),failed=sum(not row['passed'] for row in rows))),flush=True)

def assess():
    response_protocol();rows=[];records=[]
    for model in MODELS:
        for index in range(FIRST,LAST+1):
            verify_source(model,index)
            rows.extend(read(ROOT/f'sources/{model}/step-{index:04d}/result.json')['checks'])
        for count in (2048,4096):
            report=read(ROOT/f'responses/{model}-{count}/result.json')
            for name,value in report['file_hashes'].items():
                assert digest(ROOT/f'responses/{model}-{count}'/name)==value
            rows.extend(report['checks'])
        coarse=packet(ROOT/f'responses/{model}-2048/increment-readout.npz')
        fine=packet(ROOT/f'responses/{model}-4096/increment-readout.npz')
        for component in (0,4,5):
            for profile in (0,1):
                eighth=[np.ravel_multi_index((profile,1,component,join),(2,3,6,2)) for join in (0,1)]
                quarter=[np.ravel_multi_index((profile,0,component,join),(2,3,6,2)) for join in (0,1)]
                old.compare_readouts('response_step:'+old.PROFILES[profile],coarse,fine,eighth,eighth,rows,records,model,old.COMPONENTS[component])
                old.compare_readouts('history_quarter_eighth:'+old.PROFILES[profile],fine,fine,quarter,eighth,rows,records,model,old.COMPONENTS[component])
        before=packet(PARENT/f'causal-startup/responses/{model}-4096/increment-readout.npz')
        for profile,component in np.ndindex(2,6):
            if component not in (0,4,5):
                continue
            for join in (0,1):
                index_half=np.ravel_multi_index((profile,0,component,join),(2,3,6,2))
                index_quarter=np.ravel_multi_index((profile,1,component,join),(2,3,6,2))
                for field in ('gas','energy'):
                    old_change=abs(before[field][index_half]-before[field][index_quarter])
                    new_change=abs(fine[field][index_half]-fine[field][index_quarter])
                    records.append(dict(scope='observed_difference_shrinkage',model=model,profile=old.PROFILES[profile],
                        component=old.COMPONENTS[component],join=join,field=field,
                        ratio=float(new_change/max(old_change,1e-300)),not_a_certified_error_bound=True))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/response-assessment.json',dict(checks=rows,failed_checks=failed,records=records,qualified=not failed,
          original_bank_unchanged=True,temperature_curve_unchanged=True,tolerances_unchanged=True,
          shared_seed_uncertainty_bounded=False,causal_matching_still_separate=True))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),
        maxima={scope:max(row['relative'] for row in records if row['scope']==scope) for scope in sorted({row['scope'] for row in records if 'relative' in row})})),flush=True)

if __name__=='__main__':
    old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run','assess'])
    parser.add_argument('--model',choices=MODELS)
    args=parser.parse_args()
    if args.phase=='prepare':
        prepare_response()
    elif args.phase=='assess':
        assess()
    else:
        sources(args.model)
        for count in (2048,4096):
            evolve(args.model,count)

