from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,math,time,zipfile
from datetime import datetime,timezone
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'complete-panel-operator-final-20261026'
PARENT_SHA='4b59f1e708a6d22dc4fc616e2f1f9d6b1905aaae0a76defc007156cc14bbee24'
RESPONSE=BRANCH/'operator-response-injection-20261025'
MATCHED=BRANCH/'temperature-history-response-matching-20261022'
sys.path[:0]=[str(PARENT),str(RESPONSE)]
import batch220 as panel
import response217 as injection
np,mp,linear=panel.np,panel.mp,panel.linear
source,api,metrics=panel.source,panel.api,panel.metrics
history=injection.inherited.history
matched=injection.matched
read,write,save,packet,digest,check=panel.read,panel.write,panel.save,panel.packet,panel.digest,panel.check
register=panel.register
COMPONENTS=panel.COMPONENTS
MODELS=('heavy','cold')
PROFILES=('quadratic','endpoint_secant')
GRIDS=('half','quarter','zero')
START=0.90234375
STOP=0.90625
FINE=4096
FIRST=2496
LAST=2560
WIDTH=72


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['implementation'].items():
        assert digest(name)==value,name
    return config


def point_folder(model,index):
    return ROOT/f'sources/{model}/step-{index:04d}'


def flatten(values):
    return np.moveaxis(values,3,0).reshape(98,WIDTH)


def pair_source(values,system,rows,label):
    basis=SimpleNamespace(mass=system.basis.mass,temperature=system.basis.temperature,others=system.coordinates.others)
    return injection.supplied_source((flatten(values['high']),flatten(values['low'])),basis,rows,label)


def prepare():
    assert not (ROOT/'configuration.json').exists()
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    parent=read(PARENT/'results/stage-integrity.json')
    assert parent['qualified'] and parent['full_seven_node_operator_complete']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    for name,value in parent['file_hashes'].items():
        register(inputs,PARENT/name,value)
    register(inputs,PARENT/'results/stage-integrity.json',PARENT_SHA)
    previous=read(PARENT/'configuration.json')
    rows=[];incoming={}
    for label in panel.LABELS:
        register(inputs,PARENT/f'results/operator-panel-{label}.npz')
    original,theta=source.context(STOP)
    basis=packet(PARENT/'frozen/basis-metric.npz')
    check(rows,'fixed source mass',int(not np.array_equal(original.basis.mass,basis['mass'])),0,'integrity')
    for path in original.inputs:
        register(inputs,path)
    for model in MODELS:
        incoming[model]={}
        for count in (2048,4096):
            system=matched.System(model,count,inputs)
            check(rows,f'{model}:{count}:same mass',np.max(abs(system.basis.mass-basis['mass'])),0,'integrity')
            start=round((START-.75)*count/.25)
            stop=round((STOP-.75)*count/.25)
            check(rows,f'{model}:{count}:start on original grid',.75+start*.25/count-START,0,'integrity')
            check(rows,f'{model}:{count}:end on original grid',.75+stop*.25/count-STOP,0,'integrity')
            assert system.stop<start<stop and stop==system.target
            folder=MATCHED/f'runs-matched/{model}-{count}'
            boundary=register(inputs,folder/f'interfaces/step-{system.stop}.npz')
            target=register(inputs,folder/f'transfer/step-{stop}.npz')
            register(inputs,folder/'status.json')
            stored=packet(boundary)
            assert float(stored['fraction'])==system.config['interval'][1]
            assert float(stored['step'])==system.step and int(stored['index'])==system.stop
            incoming[model][str(count)]=dict(boundary_path=str(boundary),boundary_sha256=digest(boundary),
                target_path=str(target),target_sha256=digest(target),start_index=start,stop_index=stop)
    assert FIRST==round((START-.75)*FINE/.25) and LAST==round((STOP-.75)*FINE/.25)
    implementation={}
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs,path);implementation[str(path)]=digest(path)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in bookmarks:
            archive.writestr(Path(name).name,Path(name).read_bytes())
    config=dict(stage=221,turn_start='2026-10-26T06:47:58+00:00',prepared_at=now(),
        interval=[START,STOP],counts=[2048,4096],fine_indices=[FIRST,LAST],source_points_per_model=64,
        profiles=list(PROFILES),grids=list(GRIDS),components=COMPONENTS,models=list(MODELS),
        anchor_offsets=previous['anchor_offsets'],anchor_thetas=previous['anchor_thetas'],
        parent_basis=str(PARENT/'frozen/basis-metric.npz'),incoming=incoming,
        bookmarks=bookmarks,implementation=implementation,source_digits=80,audit_digits=100,
        protocol_hashes={name:digest(ROOT/name) for name in ('response221.py','ACCEPTANCE.md','DERIVATION.md')},
        identity_tolerance=1e-10,comparison_tolerance=.01,unchanged_response_gates=dict(photon=1e-7,gas=1e-8,spectral=1.),
        ledger_tolerance=1e-7,scattering_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        startup='original response schedule; no new restart at the diagnostic interval start',
        source_scope='complete original8-20 panel, retained97-input repair, not all frequencies',
        incoming_scope='saved Stage198 known interval contribution plus explicit arbitrary incoming two-state maps',
        no_source_only_closure=True,no_feedback_iteration=True)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']]))
    assert all(row['passed'] for row in rows)
    write(ROOT/'progress.json',dict(state='prepared',source_points_required=128))
    print(json.dumps(dict(state='prepared',inputs=len(inputs),source_points=128,interval=[START,STOP],steps=[32,64])),flush=True)


def coefficients_at(model,index,inputs,rows):
    fraction=.75+index*.25/FINE
    coordinate=fraction*math.log(10)
    original,theta=source.context(fraction)
    for path in original.inputs:
        register(inputs,path)
    basis=packet(PARENT/'frozen/basis-metric.npz')
    check(rows,'same retained basis mass',int(not np.array_equal(original.basis.mass,basis['mass'])),0,'integrity')
    old_root=history.ROOT
    try:
        history.ROOT=point_folder(model,index)
        records={grid:history.sample_history(model,grid,coordinate,inputs) for grid in ('half','quarter')}
    finally:
        history.ROOT=old_root
    high=np.zeros((97,3));low=high.copy()
    with mp.workdps(80):
        before=[mp.mpf(float(value)) for value in original.epochs[0].original[model]]
        original_gas=mp.mpf(float(original.gas[MODELS.index(model)]))
        for grid_index,grid in enumerate(('half','quarter')):
            record=records[grid]
            rows.extend(dict(row,name=grid+':'+row['name']) for row in record['checks'])
            vector=[mp.mpf(value)-old for value,old in zip(record['current']['profile'],before)]
            vector.append(mp.mpf(record['current']['gas'])-original_gas)
            assert len(vector)==97
            for entry,value in enumerate(vector):
                high[entry,grid_index]=float(value)
                low[entry,grid_index]=float(value-mp.mpf(float(value)))
    return (high,low),theta,fraction


def verify_point(model,index):
    folder=point_folder(model,index)
    report=read(folder/'result.json')
    assert report['model']==model and report['fine_index']==index
    for name,value in report['file_hashes'].items():
        assert digest(folder/name)==value,name
    values=packet(folder/'source.npz')
    assert values['high'].shape==values['low'].shape==(2,3,6,98,2)
    return values,report


def generate(model,stop_at):
    config=protocol();deadline=datetime.fromisoformat(stop_at);inputs=read(ROOT/'inputs.json')
    anchors=[]
    for label in panel.LABELS:
        values=packet(PARENT/f'results/operator-panel-{label}.npz')
        anchors.append((values['high'],values['low']))
    started=now();began=time.monotonic()
    write(ROOT/f'workers/{model}.json',dict(state='running',pid=os.getpid(),started_at=started,stop_at=stop_at))
    for index in range(FIRST+1,LAST+1):
        folder=point_folder(model,index)
        if (folder/'result.json').exists():
            verify_point(model,index);continue
        if datetime.now(timezone.utc)>=deadline:
            break
        tick=time.monotonic();rows=[];records=[]
        coefficients,theta,fraction=coefficients_at(model,index,inputs,rows)
        offset=(.875-fraction)*math.log(10)
        nodes=config['anchor_offsets']
        weights=history.weights(offset,nodes)
        secant=history.weights(offset,[nodes[0],nodes[2]])
        all_weights=[weights,[secant[0],0.,secant[1]]]
        high=np.zeros((2,3,6,98,2));low=high.copy()
        for profile,weights in enumerate(all_weights):
            for power in range(3 if profile==0 else 2):
                check(rows,f'{PROFILES[profile]} degree{power}',sum(weight*node**power for weight,node in zip(weights,nodes))-offset**power,1e-14,'identity')
            matrix=panel.weighted_matrix(anchors,weights)
            for join in (0,1):
                output=api.apply_coefficients(matrix,coefficients,join,80)
                high[profile,...,join]=np.moveaxis(output[0],2,0)
                low[profile,...,join]=np.moveaxis(output[1],2,0)
        check(rows,'finite source',int(not np.isfinite(high).all() or not np.isfinite(low).all()),0,'integrity')
        check(rows,'zero history control',np.max(abs(high[:,2]))+np.max(abs(low[:,2])),0,'identity')
        with mp.workdps(100):
            mass=packet(PARENT/'frozen/basis-metric.npz')
            temperature0=mp.mpf(float(mass['mean']))*mp.mpf(float(mass['norms'][0]))
            temperature1=mp.mpf(float(mass['norms'][1]))
            for profile,grid,component,join in np.ndindex(2,2,6,2):
                exact=lambda row:mp.mpf(float(high[profile,grid,component,row,join]))+mp.mpf(float(low[profile,grid,component,row,join]))
                energy=exact(0);scale=max(abs(energy),mp.mpf('1e-300'))
                check(rows,f'moment:{profile}:{grid}:{component}:{join}',(temperature0*exact(1)+temperature1*exact(2)-energy)/scale,1e-10,'identity')
                check(rows,f'pair:{profile}:{grid}:{component}:{join}',(energy+exact(97))/scale,1e-10,'identity')
        save(folder/'source.npz',high=high,low=low,theta=theta,fraction=fraction)
        save(folder/'coefficients.npz',high=coefficients[0],low=coefficients[1],theta=theta,fraction=fraction)
        write(folder/'result.json',dict(model=model,fine_index=index,fraction=fraction,theta=theta,weights=all_weights,
            seconds=time.monotonic()-tick,finished_at=now(),checks=rows,failed_checks=[row for row in rows if not row['passed']],
            file_hashes={path.relative_to(folder).as_posix():digest(path) for path in folder.rglob('*') if path.is_file() and path.name!='result.json'}))
        write(ROOT/f'inputs-{model}.json',inputs)
        write(ROOT/f'workers/{model}.json',dict(state='running',pid=os.getpid(),last_index=index,updated_at=now(),stop_at=stop_at))
        print(json.dumps(dict(model=model,index=index,done=index-FIRST,total=64,seconds=time.monotonic()-tick,failed=sum(not row['passed'] for row in rows))),flush=True)
        assert all(row['passed'] for row in rows)
    write(ROOT/f'workers/{model}.json',dict(state='stopped',pid=os.getpid(),finished_at=now(),seconds=time.monotonic()-began))
    print(json.dumps(dict(model=model,source_points=len(list((ROOT/'sources'/model).glob('step-*/result.json'))))),flush=True)


def compare_state(label,actual,expected,system,rows,tolerance=1e-10):
    actual=matched.collapsed(actual);expected=matched.collapsed(expected)
    factor=linear.cholesky(system.basis.mass,lower=True)
    error=system.coordinates.transform@(actual[:96]-expected[:96])
    target=system.coordinates.transform@expected[:96]
    ratios=[('photon',np.linalg.norm(factor.T@error,axis=0)/np.maximum(np.linalg.norm(factor.T@target,axis=0),1e-300))]
    ratios.extend((name,abs(actual[index]-expected[index])/np.maximum(abs(expected[index]),1e-300))
                  for name,index in [('energy',0),('gas',96),('work',97),('number',98),('injection',99)])
    for field,values in ratios:
        check(rows,label+':'+field,np.max(values),tolerance,'identity')


def expand_incoming(stored):
    result=np.zeros((100,2*WIDTH))
    for profile,grid,component,join in np.ndindex(2,3,6,2):
        if grid==2 or component not in (0,4,5):
            continue
        version=3 if grid==0 else 4
        kind={0:0,4:1,5:2}[component]
        source_column=version*6+kind*2+join
        target_column=np.ravel_multi_index((profile,grid,component,join),(2,3,6,2))
        result[:,target_column]=stored[:,source_column]
        result[:,target_column+WIDTH]=stored[:,source_column+74]
    return result


def ledger_checks(label,state,system,rows):
    values=matched.collapsed(state);heat=system.background.chi
    ledger=values[0]+heat*values[96]+values[97]-values[99]
    scale=abs(values[0])+abs(heat*values[96])+abs(values[97])+abs(values[99])
    check(rows,label+':energy/work/pair',np.max(abs(ledger)/np.maximum(scale,1e-300)),1e-7,'equation')
    number=system.basis.number@(system.coordinates.transform@values[:96])
    check(rows,label+':number balance',np.max(abs(number-values[98])/np.maximum(abs(number)+abs(values[98]),1e-300)),1e-7,'equation')


def evolve(model,count):
    config=protocol();inputs=read(ROOT/'inputs.json');inputs.update(read(ROOT/f'inputs-{model}.json'))
    destination=ROOT/f'responses/{model}-{count}'
    assert not (destination/'result.json').exists()
    rows=[];system=matched.System(model,count,inputs)
    owner=config['incoming'][model][str(count)]
    assert digest(owner['boundary_path'])==owner['boundary_sha256']
    boundary=packet(owner['boundary_path'])
    current=boundary['current'].copy();previous=boundary['previous'].copy()
    start=owner['start_index'];stop=owner['stop_index']
    for index in range(system.stop+1,start+1):
        updated,unused=system.advance(current,previous,system.make_step(index))
        previous,current=current,updated
    incoming=expand_incoming(current);incoming_previous=expand_incoming(previous)
    save(destination/'incoming.npz',current=incoming,previous=incoming_previous,index=start,fraction=START)
    homogeneous=incoming.copy();homogeneous_previous=incoming_previous.copy()
    joint=incoming.copy();joint_previous=incoming_previous.copy()
    increment=np.zeros_like(incoming);increment_previous=increment.copy()
    transfer=np.column_stack([np.eye(100),np.zeros((100,100))])
    transfer_previous=np.column_stack([np.zeros((100,100)),np.eye(100)])
    maximum=dict(photon=0.,gas=0.,spectral=0.)
    checkpoints={}
    for index in range(start+1,stop+1):
        step=system.make_step(index)
        assert not step['restart']
        fine_index=index*(FINE//count)
        values,report=verify_point(model,fine_index)
        assert not report['failed_checks']
        supplied=pair_source(values,system,rows,f'step{index}')
        new_increment,diagnostic=system.advance(increment,increment_previous,step,supplied,True)
        new_joint,unused=system.advance(joint,joint_previous,step,supplied)
        new_homogeneous,unused=system.advance(homogeneous,homogeneous_previous,step)
        new_transfer,unused=system.advance(transfer,transfer_previous,step)
        increment_previous,increment=increment,new_increment
        joint_previous,joint=joint,new_joint
        homogeneous_previous,homogeneous=homogeneous,new_homogeneous
        transfer_previous,transfer=transfer,new_transfer
        for name,value in diagnostic.items():
            maximum[name]=max(maximum[name],value)
        compare_state(f'step{index}:incoming plus increment',joint,homogeneous+increment,system,rows)
        ledger_checks(f'step{index}:increment',increment,system,rows)
        ledger_checks(f'step{index}:joint',joint,system,rows)
        collapsed=matched.collapsed(increment).reshape(100,2,3,6,2)
        check(rows,f'step{index}:zero history',np.max(abs(collapsed[:,:,2])),0,'identity')
        for component,parts in [(4,[1,2,3]),(5,[0,1,2,3])]:
            left=collapsed[:,:,:,component,:];right=sum(collapsed[:,:,:,part,:] for part in parts)
            check(rows,f'step{index}:component{component}',np.linalg.norm(left-right)/max(np.linalg.norm(right),1e-300),1e-10,'identity')
        if index in (start+(stop-start)//2,stop):
            path=destination/f'step-{index}.npz'
            save(path,current=increment,previous=increment_previous,joint=joint,joint_previous=joint_previous,
                 homogeneous=homogeneous,homogeneous_previous=homogeneous_previous,
                 current_map=transfer[:,:100],previous_map=transfer[:,100:],index=index,fraction=step['fraction'])
            checkpoints[index]=str(path)
    for field,limit in config['unchanged_response_gates'].items():
        check(rows,'response equation:'+field,maximum[field],limit,'equation')
    mapped=transfer[:,:100]@incoming+transfer[:,100:]@incoming_previous
    compare_state('arbitrary incoming map on saved states',mapped,homogeneous,system,rows)
    assert digest(owner['target_path'])==owner['target_sha256']
    target=expand_incoming(packet(owner['target_path'])['current'][:,:148])
    compare_state('unchanged Stage198 homogeneous replay',homogeneous,target,system,rows)
    midpoint=start+(stop-start)//2
    saved_mid=packet(checkpoints[midpoint]);rejoined=saved_mid['current'];older=saved_mid['previous']
    for index in range(midpoint+1,stop+1):
        supplied=pair_source(verify_point(model,index*(FINE//count))[0],system,rows,f'rejoin{index}')
        updated,unused=system.advance(rejoined,older,system.make_step(index),supplied)
        older,rejoined=rejoined,updated
    compare_state('two-state midpoint restart',rejoined,increment,system,rows)
    altered=saved_mid['current'].copy();older=altered.copy()
    for index in range(midpoint+1,stop+1):
        supplied=pair_source(verify_point(model,index*(FINE//count))[0],system,rows,f'negative{index}')
        updated,unused=system.advance(altered,older,system.make_step(index),supplied)
        older,altered=altered,updated
    negative_error=matched.relative(matched.collapsed(altered),matched.collapsed(increment))
    check(rows,'erasing previous state is detected',int(negative_error<=1e-10),0,'negative_control')
    for component in (0,4):
        columns=[np.ravel_multi_index((0,1,component,join),(2,3,6,2)) for join in (0,1)]
        component_error=matched.relative(matched.collapsed(altered)[:,columns],matched.collapsed(increment)[:,columns])
        check(rows,'erased previous detected:'+COMPONENTS[component],int(component_error<=1e-10),0,'negative_control')
    save(destination/'negative-erased-previous.npz',wrong=altered,expected=increment)
    reader=matched.saved.response.ShapeReadout(system.basis,canonical=True)
    for label,state in [('increment',increment),('joint',joint),('incoming_continued',homogeneous)]:
        values=matched.collapsed(state)
        shapes=reader.apply(system.coordinates.transform@values[:96],values[0])
        save(destination/f'{label}-readout.npz',**shapes,frequency=reader.frequency,measure=reader.measure,
             gas=values[96],work=values[97],energy=values[0],number=values[98],injection=values[99],heat=system.background.chi)
    failed=[row for row in rows if not row['passed']]
    write(destination/'result.json',dict(model=model,count=count,finished_at=now(),checks=rows,failed_checks=failed,
        qualified=not failed,maximum_equation_residuals=maximum,negative_erased_previous_relative=negative_error,
        interval=[START,STOP],steps=stop-start,checkpoints=checkpoints,
        file_hashes={path.name:digest(path) for path in destination.glob('*.npz')}))
    write(ROOT/f'inputs-response-{model}-{count}.json',inputs)
    print(json.dumps(dict(model=model,count=count,checks=len(rows),failed=len(failed),maximum=maximum,negative_error=negative_error)),flush=True)


def compare_readouts(label,first,second,columns_first,columns_second,rows,records,model,kind):
    measure=second['measure']
    for field in ('residual','gas','energy','work','number'):
        left=first[field][...,columns_first];right=second[field][...,columns_second]
        if field=='residual':
            numerator=matched.saved.response.norm(left-right,measure)
            denominator=matched.saved.response.norm(right,measure)
        else:
            numerator=abs(left-right);denominator=abs(right)
        relative=numerator/np.maximum(denominator,1e-300)
        for join,value in enumerate(np.asarray(relative).reshape(-1)):
            records.append(dict(scope=label,model=model,component=kind,field=field,join=join,relative=float(value)))
            check(rows,f'{label}:{model}:{kind}:{field}:{join}',value,.01,'comparison')


def assess():
    config=protocol();rows=list(read(ROOT/'results/preparation.json')['checks']);records=[]
    inputs=read(ROOT/'inputs.json')
    for model in MODELS:
        inputs.update(read(ROOT/f'inputs-{model}.json'))
        for index in range(FIRST+1,LAST+1):
            values,report=verify_point(model,index)
            rows.extend(dict(row,name=f'{model}:{index}:'+row['name']) for row in report['checks'])
        for count in config['counts']:
            folder=ROOT/f'responses/{model}-{count}'
            report=read(folder/'result.json')
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in report['checks'])
            inputs.update(read(ROOT/f'inputs-response-{model}-{count}.json'))
        coarse=packet(ROOT/f'responses/{model}-2048/increment-readout.npz')
        fine=packet(ROOT/f'responses/{model}-4096/increment-readout.npz')
        for component in (0,4,5):
            kind=COMPONENTS[component]
            for profile in (0,1):
                columns=[np.ravel_multi_index((profile,1,component,join),(2,3,6,2)) for join in (0,1)]
                compare_readouts('response_step:'+PROFILES[profile],coarse,fine,columns,columns,rows,records,model,kind)
                half=[np.ravel_multi_index((profile,0,component,join),(2,3,6,2)) for join in (0,1)]
                compare_readouts('history_step:'+PROFILES[profile],fine,fine,half,columns,rows,records,model,kind)
            quadratic=[np.ravel_multi_index((0,1,component,join),(2,3,6,2)) for join in (0,1)]
            secant=[np.ravel_multi_index((1,1,component,join),(2,3,6,2)) for join in (0,1)]
            compare_readouts('operator_continuation_sensitivity',fine,fine,secant,quadratic,rows,records,model,kind)
    for name,value in inputs.items():
        assert digest(name)==value,name
    check(rows,'consumed/immediate inputs unchanged',0,0,'integrity')
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected recent mtime count',len(changed),0,'integrity')
    check(rows,'no bytecode or temporary files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial')))+len(list(ROOT.rglob('*.tmp'))),0,'integrity')
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    failed=[row for row in rows if not row['passed']]
    implementation_failed=[row for row in failed if row['category']!='comparison']
    write(ROOT/'inputs-final.json',inputs)
    write(ROOT/'results/assessment.json',dict(stage=221,checks=rows,failed_checks=failed,records=records,
        qualified=not failed,implementation_qualified=not implementation_failed,inputs_rehashed=len(inputs),
        interval=[START,STOP],source_points=128,physical_global_history_complete=False,
        interpolation_sensitivity_is_not_certified_error_bound=True,
        protected_recent_mtime_count=len(changed),guard_scope='recent mtime, not a full content snapshot',
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),implementation_failed=len(implementation_failed),inputs=len(inputs),
        maxima={scope:max(row['relative'] for row in records if row['scope']==scope) for scope in sorted({row['scope'] for row in records})})),flush=True)


def seal():
    config=protocol();assessment=read(ROOT/'results/assessment.json')
    for name in ('RESULTS.md','NEXT.md'):
        assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            before=archive.read(Path(name).name)
            assert hashlib.sha256(before).hexdigest()==value and Path(name).read_bytes().endswith(before)
            bookmarks.append(dict(path=name,previous_sha256=value,current_sha256=digest(name),previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',qualified=assessment['qualified'],implementation_qualified=assessment['implementation_qualified'],
        source_points=128,response_cases=4,active_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json';assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=221,state='complete',qualified=assessment['qualified'],implementation_qualified=assessment['implementation_qualified'],
        sealed_at=now(),parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=read(ROOT/'inputs-final.json'),file_hashes=hashes,
        retained_current_failures=len(assessment['failed_checks']),active_workers_at_seal=0,
        original_bank_changed=False,global_curve_changed=False,grids_changed=False,tolerances_changed=False,
        github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(sha256=digest(destination),payloads=len(hashes),qualified=assessment['qualified'])),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','generate','evolve','assess','seal'])
    parser.add_argument('--model',choices=MODELS)
    parser.add_argument('--count',type=int,choices=[2048,4096])
    parser.add_argument('--stop-at',default='2026-10-26T10:10:00+00:00')
    args=parser.parse_args()
    if args.phase=='generate':
        generate(args.model,args.stop_at)
    elif args.phase=='evolve':
        evolve(args.model,args.count)
    else:
        {'prepare':prepare,'assess':assess,'seal':seal}[args.phase]()
