from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,hashlib,zipfile,time
from datetime import datetime,timezone
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'collision-operator-colder-nonmidpoint-20261025'
PARENT_SHA='1006fa2b1d1ea8aab5c0fc4f01bc3f4a082b0a351550a7bc4ebd30336a1cf2bf'
sys.path[:0]=[str(PARENT),str(BRANCH/'temperature-history-response-matching-20261022')]
import test216 as inherited
import matching198 as matched
np,mp,linear=inherited.np,inherited.mp,inherited.linear
read,write,packet,save,digest,check=inherited.read,inherited.write,inherited.packet,inherited.save,inherited.digest,inherited.check
COMPONENTS=inherited.COMPONENTS
SOURCES={'direct':PARENT/'results/direct-source.npz','operator':PARENT/'results/operator-source.npz',
         'predicted':PARENT/'frozen/predicted-source.npz'}


def now():
    return datetime.now(timezone.utc).isoformat()


def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    for name,value in config['frozen_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config


def register(inputs,path):
    path=Path(path).resolve()
    value=digest(path)
    assert str(path) not in inputs or inputs[str(path)]==value,str(path)
    inputs[str(path)]=value
    return path


def prepare():
    assert not (ROOT/'configuration.json').exists()
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SHA
    parent=read(PARENT/'results/stage-integrity.json')
    assert parent['qualified']
    inputs=dict(parent['consumed_and_immediate_rehashed'])
    for name,value in parent['file_hashes'].items():
        assert digest(PARENT/name)==value,name
        inputs[str(PARENT/name)]=value
    register(inputs,PARENT/'results/stage-integrity.json')
    config216=read(PARENT/'configuration.json')
    rows=[]
    original,theta=inherited.source.context(config216['target_fraction'])
    for path in original.inputs:
        register(inputs,path)
    for path in SOURCES.values():
        register(inputs,path)
    for model in ('heavy','cold'):
        ladder,background,emission=matched.saved.setup(model,inputs)
        basis=ladder.basis
        coordinates=matched.saved.response.EnergyCoordinates(basis)
        local=background.at(config216['target_fraction']*background.end)
        check(rows,model+':same source/response temperature',local['thermal_parameter']/theta-1,1e-10,'integrity')
        check(rows,model+':same source/response mass',np.max(abs(basis.mass-original.basis.mass)),1e-14,'integrity')
        check(rows,model+':same photon basis',np.max(abs(basis.evaluate(original.epochs[0].frequency)-original.basis.evaluate(original.epochs[0].frequency))),1e-14,'integrity')
        check(rows,model+':temperature vector support',np.max(abs(basis.temperature[2:])),0,'integrity')
        stiffness=ladder.at(local['thermal_parameter'],0)[:96,:96]-emission.at(local['thermal_parameter'],'dcbr')
        save(ROOT/f'frozen/{model}.npz',mass=basis.mass,temperature=basis.temperature,energy=basis.energy,
             number=basis.number,chemical=basis.chemical,transform=coordinates.transform,tests=coordinates.tests,
             coordinate_mass=coordinates.mass,others=coordinates.others,stiffness=stiffness,
             rate=local['coefficient']/local['thermal_parameter'],heat=background.chi,span=background.end,
             theta=local['thermal_parameter'],fraction=config216['target_fraction'])
        for count in (2048,4096):
            target_index=round(.625*count)
            path=register(inputs,BRANCH/f'temperature-history-response-matching-20261022/runs-matched/{model}-{count}/transfer/step-{target_index}.npz')
            stored=packet(path)
            current=[];previous=[]
            for grid,component,join in np.ndindex(3,6,2):
                column=24+2*(0 if component==0 else 2 if component==5 else 1)+join
                for name,destination in (('current',current),('previous',previous)):
                    value=stored[name][:100,[column,column+74]].copy()
                    if grid==2:
                        value[:]=0
                    destination.append(value)
            save(ROOT/f'frozen/{model}-{count}-incoming.npz',current=np.stack(current,axis=1),
                 previous=np.stack(previous,axis=1),control_fraction=stored['fraction'])
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs,path)
    bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')}
    (ROOT/'results').mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(ROOT/'results/resume-before.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in bookmarks:
            archive.writestr(Path(name).name,Path(name).read_bytes())
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/preparation.json',dict(checks=rows,failed_checks=failed))
    assert not failed,failed
    config=dict(stage=217,turn_start='2026-10-25T20:50:13+00:00',frozen_at=now(),theta=theta,
                fraction=config216['target_fraction'],counts=[2048,4096],models=['heavy','cold'],
                source_paths={name:str(path) for name,path in SOURCES.items()},bookmarks=bookmarks,
                protocol_hashes={path.name:digest(path) for path in [ROOT/'response217.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']},
                frozen_hashes={str(path.relative_to(ROOT)):digest(path) for path in (ROOT/'frozen').glob('*')},
                identity_tolerance=1e-10,prediction_tolerance=.01,physical_trajectory=False)
    write(ROOT/'inputs.json',inputs)
    write(ROOT/'configuration.json',config)
    write(ROOT/'progress.json',dict(state='frozen_before_response_evaluation',cases_complete=0))
    print(json.dumps(dict(state='prepared',inputs=len(inputs),checks=len(rows),cases=4)),flush=True)


def split_matrix(values):
    high=np.empty((values.rows,values.cols));low=high.copy()
    for row,column in np.ndindex(high.shape):
        high[row,column]=float(values[row,column])
        low[row,column]=float(values[row,column]-mp.mpf(high[row,column]))
    return high,low


def as_mp(values):
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in values])


def supplied_source(pair,basis,rows,label):
    high,low=pair
    factor=linear.cholesky(basis.mass,lower=True)
    with mp.workdps(80):
        original=as_mp(high)+as_mp(low)
        spectral=original[1:97,:].copy()
        temperature=as_mp(basis.temperature[:,None])
        for column in range(original.cols):
            spectral[1,column]=(original[0,column]-temperature[0]*spectral[0,column])/temperature[1]
        spectral_high,spectral_low=split_matrix(spectral)
    force_high=np.vstack([high[0],high[1:97][basis.others]])
    force_low=np.vstack([low[0],low[1:97][basis.others]])
    changed=spectral_high+spectral_low-high[1:97]-low[1:97]
    denominator=np.maximum(np.linalg.norm(linear.solve_triangular(factor,high[1:97]+low[1:97],lower=True),axis=0),1e-300)
    rewrite=np.linalg.norm(linear.solve_triangular(factor,changed,lower=True),axis=0)/denominator
    check(rows,label+':source representation rewrite',np.max(rewrite),1e-10,'identity')
    return dict(original=np.column_stack([high,low]),force=np.column_stack([force_high,force_low]),
                spectral=np.column_stack([spectral_high,spectral_low]))


def system_from_frozen(values,count):
    system=object.__new__(matched.System)
    system.basis=SimpleNamespace(**{name:values[name] for name in ('mass','temperature','energy','number','chemical','others')})
    system.coordinates=SimpleNamespace(transform=values['transform'],tests=values['tests'],mass=values['coordinate_mass'],others=values['others'])
    system.step=.25*float(values['span'])/count
    rate,heat=float(values['rate']),float(values['heat'])
    alpha=1.5/system.step
    coupling=-rate*values['tests']@values['stiffness']@values['temperature']
    factor=linear.lu_factor(alpha*values['coordinate_mass']-rate*values['tests']@values['stiffness']@values['transform'])
    gas_response=linear.lu_solve(factor,coupling)
    denominator=heat*(alpha+1)+alpha*gas_response[0]
    assert np.isfinite(denominator) and denominator>0
    step=dict(alpha=alpha,rate=rate,heat=heat,stiffness=values['stiffness'],restart=False,
              factor=factor,gas_response=gas_response,denominator=denominator)
    return system,step


def compare_response(label,actual,expected,system,rows,records,tolerance=1e-10,category='identity'):
    actual=matched.collapsed(actual);expected=matched.collapsed(expected)
    factor=linear.cholesky(system.basis.mass,lower=True)
    photon_actual=system.coordinates.transform@actual[:96]
    photon_expected=system.coordinates.transform@expected[:96]
    photon_error=np.linalg.norm(factor.T@(photon_actual-photon_expected),axis=0)
    photon_scale=np.linalg.norm(factor.T@photon_expected,axis=0)
    for field,error,scale in [('photon',photon_error,photon_scale),
         *[(name,abs(actual[index]-expected[index]),abs(expected[index])) for name,index in
           [('energy',0),('gas',96),('work',97),('number',98),('injection',99)]]]:
        for column in range(actual.shape[1]):
            value=float(error[column]/max(scale[column],1e-300))
            grid,component,join=np.unravel_index(column,(3,6,2))
            records.append(dict(scope=label,field=field,grid=('half','quarter','zero')[grid],
                component=COMPONENTS[component],join=int(join),relative=value))
            check(rows,f'{label}:{field}:{column}',value,tolerance,category)


def ledgers(label,state,system,step,rows):
    values=matched.collapsed(state)
    heat=step['heat']
    energy=values[0]+heat*values[96]+values[97]-values[99]
    scale=abs(values[0])+abs(heat*values[96])+abs(values[97])+abs(values[99])
    check(rows,label+':energy ledger',np.max(abs(energy)/np.maximum(scale,1e-300)),1e-7,'equation')
    number=system.basis.number@(system.coordinates.transform@values[:96])
    check(rows,label+':number ledger',np.max(abs(number-values[98])/np.maximum(abs(number)+abs(values[98]),1e-300)),1e-7,'equation')


def reference_step(values,count,pair):
    with mp.workdps(80):
        mass,stiffness=as_mp(values['mass']),as_mp(values['stiffness'])
        temperature=as_mp(values['temperature'][:,None])
        rate,heat=mp.mpf(float(values['rate'])),mp.mpf(float(values['heat']))
        step=mp.mpf(float(.25*float(values['span'])/count))
        alpha=mp.mpf(float(1.5/float(step)))
        thermal=stiffness*temperature
        transfer=mp.matrix(97)
        transfer[:96,:96]=alpha*mass-rate*stiffness
        transfer[:96,96]=rate*thermal
        transfer[96,:96]=rate*temperature.T*stiffness
        transfer[96,96]=heat*(alpha+1)-rate*(temperature.T*thermal)[0]
        original=as_mp(pair[0])+as_mp(pair[1])
        spectral=original[1:97,:].copy()
        for column in range(original.cols):
            spectral[1,column]=(original[0,column]-temperature[0]*spectral[0,column])/temperature[1]
        right=mp.matrix(97,original.cols)
        right[:96,:]=rate*spectral
        right[96,:]=rate*original[97,:]
        result=transfer**-1*right
        energy=as_mp(values['energy'][None,:])*result[:96,:]
        actual=mp.matrix(100,original.cols)
        actual[0,:]=energy
        for row,index in enumerate(values['others'],start=1):
            actual[row,:]=result[int(index),:]
        actual[96,:]=result[96,:]
        actual[97,:]=heat/alpha*result[96,:]
        actual[98,:]=rate/alpha*as_mp(values['chemical'][None,:])*(stiffness*(result[:96,:]-temperature*result[96,:])+spectral)
        actual[99,:]=rate/alpha*(original[0,:]+original[97,:])
        return split_matrix(actual)


def source_for_background(path,background):
    values=packet(path)
    selection=slice(0,2) if background=='heavy' else slice(2,4)
    return tuple(np.moveaxis(values[name][...,selection],2,0).reshape(98,36) for name in ('high','low'))


def run():
    config=protocol()
    for model in config['models']:
        values=packet(ROOT/f'frozen/{model}.npz')
        sources={name:source_for_background(path,model) for name,path in SOURCES.items()}
        for count in config['counts']:
            output=ROOT/f'cases/{model}-{count}'
            if (output/'result.json').exists():
                report=read(output/'result.json')
                for name,value in report['file_hashes'].items():
                    assert digest(output/name)==value
                print('Reusing '+str(output),flush=True)
                continue
            started=now();began=time.monotonic();rows=[];records=[]
            system,step=system_from_frozen(values,count)
            zero=np.zeros((100,72))
            responses={}
            for name,pair in sources.items():
                supplied=supplied_source(pair,system.basis,rows,name)
                state,diagnostic=system.advance(zero,zero,step,supplied,diagnostics=True)
                for field,tolerance in [('photon',1e-7),('gas',1e-8),('spectral',1.)]:
                    check(rows,name+':response '+field,diagnostic[field],tolerance,'equation')
                check(rows,name+':zero control',np.max(abs(state[:,np.r_[24:36,60:72]])),0,'identity')
                ledgers(name,state,system,step,rows)
                responses[name]=state
                save(output/f'{name}.npz',state=state)
            compare_response('operator versus direct',responses['operator'],responses['direct'],system,rows,records)
            compare_response('frozen forecast',responses['predicted'],responses['direct'],system,rows,records,.01,'prediction')
            high,low=reference_step(values,count,sources['direct'])
            reference=np.column_stack([high,low])
            save(output/'reference80.npz',state=reference)
            compare_response('independent physical solve',responses['direct'],reference,system,rows,records)
            control=packet(ROOT/f'frozen/{model}-{count}-incoming.npz')
            current=np.column_stack([control['current'][:,:,0],control['current'][:,:,1]])
            previous=np.column_stack([control['previous'][:,:,0],control['previous'][:,:,1]])
            supplied=supplied_source(sources['direct'],system.basis,rows,'nonzero control')
            full,unused=system.advance(current,previous,step,supplied)
            homogeneous,unused=system.advance(current,previous,step)
            compare_response('saved-state additivity',full,homogeneous+responses['direct'],system,rows,records)
            witness_high,witness_low=(array.copy() for array in sources['direct'])
            witness_high[97]+=1e-3*witness_high[0]
            witness_low[97]+=1e-3*witness_low[0]
            witness=supplied_source((witness_high,witness_low),system.basis,rows,'synthetic pair witness')
            actual,unused=system.advance(zero,zero,step,witness)
            expected=step['rate']*(witness['original'][0]+witness['original'][97])/step['alpha']
            check(rows,'measured pair reaches injection ledger',np.max(abs(actual[99]-expected)),0,'identity')
            collapsed_pair=matched.collapsed(actual)[99]
            check(rows,'synthetic pair witness is nonzero',int(not np.any(collapsed_pair[:24]!=0)),0,'negative_control')
            wrong=dict(witness,original=witness['original'].copy())
            wrong['original'][97]=-wrong['original'][0]
            erased,unused=system.advance(zero,zero,step,wrong)
            check(rows,'old forced-pair shortcut erases witness',np.max(abs(erased[99])),0,'negative_control')
            save(output/'controls.npz',nonzero=full,homogeneous=homogeneous,witness=actual,erased=erased)
            failed=[row for row in rows if not row['passed']]
            report=dict(model=model,count=count,started_at=started,finished_at=now(),seconds=time.monotonic()-began,
                checks=rows,failed_checks=failed,records=records,qualified=not failed,
                file_hashes={path.name:digest(path) for path in output.glob('*.npz')})
            write(output/'result.json',report)
            print(json.dumps(dict(model=model,count=count,seconds=report['seconds'],checks=len(rows),failed=len(failed))),flush=True)
            write(ROOT/'progress.json',dict(state='running',cases_complete=len(list((ROOT/'cases').glob('*/result.json')))))


def validate():
    config=protocol()
    rows=list(read(ROOT/'results/preparation.json')['checks']);records=[]
    for model in config['models']:
        for count in config['counts']:
            folder=ROOT/f'cases/{model}-{count}'
            report=read(folder/'result.json')
            assert datetime.fromisoformat(report['started_at'])>datetime.fromisoformat(config['frozen_at'])
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in report['checks'])
            records.extend(dict(row,model=model,count=count) for row in report['records'])
    inputs=read(ROOT/'inputs.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    for name,value in config['bookmarks'].items():
        assert digest(name)==value,name
    for path in ROOT.glob('*.py'):
        compile(path.read_text(encoding='utf-8'),str(path),'exec')
    check(rows,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected recent-mtime count',len(changed),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    report=dict(stage=217,checks=rows,failed_checks=failed,records=records,qualified=not failed,
                inputs_rehashed=len(inputs),protected_recent_mtime_count=len(changed),physical_trajectory=False,
                complete_frequency_operator=False,original_bank_changed=False,tolerances_changed=False)
    write(ROOT/'results/validation.json',report)
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),qualified=report['qualified'])),flush=True)


def seal():
    config=protocol();validation=read(ROOT/'results/validation.json')
    for name in ('RESULTS.md','NEXT.md','RUN-NOTES.md'):
        assert (ROOT/name).is_file()
    bookmarks=[]
    with zipfile.ZipFile(ROOT/'results/resume-before.zip') as archive:
        for name,value in config['bookmarks'].items():
            before=archive.read(Path(name).name)
            assert hashlib.sha256(before).hexdigest()==value and Path(name).read_bytes().endswith(before)
            bookmarks.append(dict(path=name,current_sha256=digest(name),previous_sha256=value,previous_body_preserved=True))
    write(ROOT/'results/bookmarks.json',bookmarks)
    write(ROOT/'progress.json',dict(state='complete',qualified=validation['qualified'],cases_complete=4,active_workers=0,completed_at=now()))
    destination=ROOT/'results/stage-integrity.json'
    assert not destination.exists()
    parent=read(PARENT/'results/stage-integrity.json')
    hashes={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=destination}
    write(destination,dict(stage=217,state='complete',qualified=validation['qualified'],sealed_at=now(),
        parent_seal_path=str(PARENT/'results/stage-integrity.json'),parent_seal_sha256=PARENT_SHA,
        inherited_sealed_payload_count=parent['inherited_sealed_payload_count']+len(parent['file_hashes']),
        consumed_and_immediate_rehashed=read(ROOT/'inputs.json'),file_hashes=hashes,retained_failures=len(validation['failed_checks']),
        original_bank_changed=False,grids_changed=False,tolerances_changed=False,physical_trajectory=False,
        complete_frequency_operator=False,permission_to_propagate=False,active_workers_at_seal=0,
        github_action=False,subagents=False,next_target=str(ROOT/'NEXT.md')))
    print(json.dumps(dict(sha256=digest(destination),payloads=len(hashes),qualified=validation['qualified'])),flush=True)


if __name__=='__main__':
    inherited.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run','validate','seal'])
    args=parser.parse_args()
    {'prepare':prepare,'run':run,'validate':validate,'seal':seal}[args.phase]()
