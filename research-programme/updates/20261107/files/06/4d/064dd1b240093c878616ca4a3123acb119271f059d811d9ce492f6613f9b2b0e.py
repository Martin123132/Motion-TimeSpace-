from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction
from datetime import datetime,timezone
import argparse

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'two-sided-physical-source-matching-20261026'
WARM=BRANCH/'panel-correction-saved-response-20261022'
REFERENCE=BRANCH/'endpoint-twofold-response-20261019'
BUDGET=BRANCH/'final-spectrum-uncertainty-20261019'
sys.path.insert(0,str(PARENT))
import common223 as parent
np,mp,math,json=parent.np,parent.mp,parent.math,parent.json
read,write,save,packet,digest,check=parent.read,parent.write,parent.save,parent.packet,parent.digest,parent.check
response=parent.old.matched.saved.response
PARENT_SHA='a1c0e08bfbfec38e23d8774b2179a1c8e21fe20fc3a3c94262e1c205a51037f6'

def now():
    return datetime.now(timezone.utc).isoformat()

def capture(inputs,path):
    path=Path(path).resolve()
    assert path.is_file(),str(path)
    actual=digest(path)
    assert str(path) in inputs,str(path)
    assert inputs[str(path)]==actual,str(path)
    return path

def load(inputs,path):
    return packet(capture(inputs,path))

def prepare():
    assert not (ROOT/'configuration.json').exists()
    seal_path=PARENT/'results/stage-integrity.json'
    assert digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    assert seal['state']=='complete' and seal['qualified']
    inputs=dict(seal['consumed_and_immediate_rehashed'])
    inputs.update({str(PARENT/name):value for name,value in seal['file_hashes'].items()})
    inputs[str(seal_path)]=PARENT_SHA
    for name,value in inputs.items():
        assert digest(name)==value,name
    warm_config=read(capture(inputs,WARM/'configuration.json'))
    cold_config=read(capture(inputs,PARENT/'configuration.json'))
    assert warm_config['interval'][1]<cold_config['source_window'][0]
    for model in parent.MODELS:
        capture(inputs,WARM/f'readouts/{model}-4096.npz')
        capture(inputs,PARENT/f'tail/{model}-4096/increment-readout.npz')
        for route in ('local','cubic'):
            for matching in (20,40):
                capture(inputs,REFERENCE/f'results/comparison/{model}-{route}-4096-m{matching}.npz')
                capture(inputs,BUDGET/f'results/budget-ready/{model}-{route}-m{matching}.npz')
                capture(inputs,WARM/f'comparisons/{model}-{route}-m{matching}.npz')
    config=dict(stage=224,turn_start='2026-10-26T14:34:32+00:00',frozen_at=now(),parent_sha256=PARENT_SHA,
        previous_goal_turn='progress',warm_interval=warm_config['interval'],cold_interval=cold_config['source_window'],
        reference='Stage166 retained original; Stage167 budget-ready; Stage197 conditional warm repair',
        source_ownership='Stage223 already contains retained linear operator times repaired-minus-original history',
        counts=[2048,4096],models=['heavy','cold'],routes=['local','cubic'],matching=[20,40],
        profiles=['quadratic','endpoint_secant'],histories=['quarter','eighth'],identity_tolerance=1e-10,
        comparison_tolerance=.01,precision=80,full_history_adopted=False,
        protocol_hashes={name:digest(ROOT/name) for name in ('reconcile224.py','ACCEPTANCE.md','DERIVATION.md')},
        original_bookmarks={str(path):digest(path) for path in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')})
    write(ROOT/'configuration.json',config)
    write(ROOT/'inputs.json',inputs)
    print(json.dumps(dict(state='prepared',inputs=len(inputs),intervals=[config['warm_interval'],config['cold_interval']])),flush=True)

def protocol():
    config=read(ROOT/'configuration.json')
    for name,value in config['protocol_hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def compare(rows,label,actual,expected):
    actual=np.asarray(actual);expected=np.asarray(expected)
    check(rows,label,np.max(abs(actual-expected))/max(float(np.max(abs(expected))),1e-300),1e-10,'identity')

def exact_add(*arrays):
    assert all(array.shape==arrays[0].shape for array in arrays)
    high=np.empty_like(arrays[0]);low=high.copy()
    for index in np.ndindex(high.shape):
        value=sum((Fraction.from_float(float(array[index])) for array in arrays),Fraction())
        upper=float(value)
        high[index]=upper
        low[index]=float(value-Fraction.from_float(upper))
    return high,low

def norm_changes(original,delta,measure,heat):
    result=[]
    with mp.workdps(80):
        weights=[mp.mpf(float(value)) for value in measure]
        for column in range(original.shape[1]):
            old=[mp.mpf(float(value)) for value in original[:,column]]
            change=[mp.mpf(float(value)) for value in delta[:,column]]
            squared=mp.fsum(weight*value*value for weight,value in zip(weights,old))
            cross=mp.fsum(2*weight*value*addition+weight*addition*addition for weight,value,addition in zip(weights,old,change))
            delta_squared=mp.fsum(weight*addition*addition for weight,addition in zip(weights,change))
            norm=mp.sqrt(squared)
            after=mp.sqrt(squared+cross)
            shift=cross/(after+norm) if after+norm else mp.mpf(0)
            result.append(dict(before=float(abs(heat)*norm),after=float(abs(heat)*after),
                signed_change=float(abs(heat)*shift),addition_norm=float(abs(heat)*mp.sqrt(delta_squared)),
                reverse_triangle_ratio=float(abs(shift)/max(mp.sqrt(delta_squared),mp.mpf('1e-300')))))
    return result

def source_vector(solver,source):
    factor,permutation=mp.mp.LU_decomp(solver.mass)
    result=mp.matrix(100,parent.WIDTH)
    for column in range(parent.WIDTH):
        result[:96,column]=mp.mp.U_solve(factor,mp.mp.L_solve(factor,source['force'][:,column],permutation))
        result[96,column]=(source['pair'][column]-result[0,column])/solver.heat
        result[98,column]=source['number'][column]
        result[99,column]=source['pair'][column]
    return result

def boundary_audit(inputs,rows):
    summaries=[]
    with mp.workdps(80):
        for model in parent.MODELS:
            for count in parent.COUNTS:
                system=parent.old.matched.System(model,count,inputs)
                first,last,target=parent.indices(count)
                spacing=mp.mpf(float(system.step))
                alpha_b=mp.mpf('1.5')/spacing
                alpha_t=2/spacing
                for side,index in (('left',first+1),('right',last+1)):
                    path=PARENT/f'window/{model}-{count}/step-{index}.npz'
                    data=load(inputs,path)
                    current=(parent.matrix(data['high'])+parent.matrix(data['low']))[:,2*parent.WIDTH:]
                    previous=(parent.matrix(data['previous_high'])+parent.matrix(data['previous_low']))[:,2*parent.WIDTH:]
                    solver=parent.Physical(system,system.make_step(index),alpha_b)
                    if side=='left':
                        older=mp.matrix(100,parent.WIDTH)
                        sources=parent.add_sources(parent.source_at(model,count,first,system,rows),parent.source_at(model,count,index,system,rows))
                        derived=source_vector(solver,sources)+(alpha_b-alpha_t)*current
                        naive=source_vector(solver,parent.source_at(model,count,index,system,rows))
                    else:
                        before=load(inputs,PARENT/f'window/{model}-{count}/step-{last}.npz')
                        older=(parent.matrix(before['previous_high'])+parent.matrix(before['previous_low']))[:,2*parent.WIDTH:]
                        generator=parent.Physical(system,system.make_step(last),alpha_b)
                        derived=(alpha_b-alpha_t)*current+alpha_t*previous+generator.derivative(previous)-(2*previous-older/2)/spacing
                        naive=mp.matrix(100,parent.WIDTH)
                    direct=alpha_b*current-(2*previous-older/2)/spacing-solver.derivative(current)
                    for column,label in enumerate(parent.LABELS):
                        check(rows,f'{model}:{count}:{side}:{column}:BDF equivalent forcing',
                            parent.relative(direct[:,column],derived[:,column]),1e-10,'identity')
                    negative=float(parent.relative(naive,derived))
                    check(rows,f'{model}:{count}:{side}:naive forcing distinguishable',int(negative<=1e-10),0,'negative_control')
                    high,low=parent.split(derived)
                    save(ROOT/f'boundaries/{model}-{count}-{side}.npz',high=high,low=low,index=index,step=float(spacing))
                    summaries.append(dict(model=model,count=count,side=side,naive_relative_difference=negative))
    return summaries

def spectrum_audit(config,inputs,rows):
    summaries=[]
    for model in parent.MODELS:
        ladder,background,emission=parent.old.matched.saved.setup(model,inputs)
        reader=response.ShapeReadout(ladder.basis,canonical=True)
        heat=float(background.chi)
        cold=load(inputs,PARENT/f'tail/{model}-4096/increment-readout.npz')
        warm=load(inputs,WARM/f'readouts/{model}-4096.npz')
        for label,data in (('cold',cold),('warm',warm)):
            check(rows,f'{model}:{label}:heat',int(float(data['heat'])!=heat),0,'integrity')
            check(rows,f'{model}:{label}:frequency',int(not np.array_equal(data['frequency'],reader.frequency)),0,'integrity')
            check(rows,f'{model}:{label}:measure',int(not np.array_equal(data['measure'],reader.measure)),0,'integrity')
        warm_delta=reader.split_values(warm['potential'][:,24:30],warm['energy'][24:30])
        for route in config['routes']:
            for matching in config['matching']:
                reference=load(inputs,REFERENCE/f'results/comparison/{model}-{route}-4096-m{matching}.npz')
                budget=load(inputs,BUDGET/f'results/budget-ready/{model}-{route}-m{matching}.npz')
                prior=load(inputs,WARM/f'comparisons/{model}-{route}-m{matching}.npz')
                for label,data in (('reference',reference),('budget',budget),('prior',prior)):
                    check(rows,f'{model}:{route}:{matching}:{label}:heat',int(float(data['heat'])!=heat),0,'integrity')
                    check(rows,f'{model}:{route}:{matching}:{label}:frequency',int(not np.array_equal(data['frequency'],reader.frequency)),0,'integrity')
                    check(rows,f'{model}:{route}:{matching}:{label}:measure',int(not np.array_equal(data['measure'],reader.measure)),0,'integrity')
                check(rows,'unchanged ready-budget baseline',int(not np.array_equal(reference['potential'][:,0],budget['central_potential'][:,0])),0,'integrity')
                check(rows,'unchanged ready-budget MTS',int(not np.array_equal(reference['potential'][:,3:5],budget['central_potential'][:,5:7])),0,'integrity')
                columns=[0,0,3,4,7,8]
                saved=reader.split_values(reference['potential'][:,columns],reference['energy'][columns])
                compare(rows,f'{model}:{route}:{matching}:prior original spectrum',saved['potential'],prior['saved_potential'])
                compare(rows,f'{model}:{route}:{matching}:warm delta replay',warm_delta['potential'],prior['delta_potential'])
                for profile in config['profiles']:
                    for history in config['histories']:
                        selected=[next(index for index,label in enumerate(parent.LABELS) if label==dict(profile=profile,grid=history,component=component,join=join))
                                  for component in ('baseline','MTS','total') for join in (0,1)]
                        addition=reader.split_values(cold['potential'][:,selected],cold['energy'][selected])
                        combined_high,combined_low=exact_add(warm_delta['potential'],addition['potential'])
                        energy_high,energy_low=exact_add(warm_delta['energy'],addition['energy'])
                        delta=reader.split_values(combined_high,energy_high)
                        lower=reader.split_values(combined_low,energy_low)
                        for key in ('potential','residual','amplitudes','eta_standard'):
                            delta[key]=delta[key]+lower[key]
                            compare(rows,f'{model}:{route}:{matching}:{profile}:{history}:linear {key}',delta[key],warm_delta[key]+addition[key])
                        final_high,final_low=exact_add(saved['potential'],warm_delta['potential'],addition['potential'])
                        final_energy_high,final_energy_low=exact_add(saved['energy'],warm_delta['energy'],addition['energy'])
                        final=reader.split_values(final_high,final_energy_high)
                        final_lower=reader.split_values(final_low,final_energy_low)
                        for key in ('potential','residual','amplitudes','eta_standard'):
                            compare(rows,f'{model}:{route}:{matching}:{profile}:{history}:conditional projection {key}',
                                final[key]+final_lower[key],saved[key]+delta[key])
                        compare(rows,f'{model}:{route}:{matching}:{profile}:{history}:delta components',
                            delta['potential'][:,4:6],delta['potential'][:,:2]+delta['potential'][:,2:4])
                        compare(rows,f'{model}:{route}:{matching}:{profile}:{history}:conditional components',
                            final_high[:,4:6]+final_low[:,4:6],final_high[:,:2]+final_low[:,:2]+final_high[:,2:4]+final_low[:,2:4])
                        delta_metrics=response.metrics(delta,heat,reader.measure)
                        cold_metrics=response.metrics(addition,heat,reader.measure)
                        changes=norm_changes(saved['residual'],delta['residual'],reader.measure,heat)
                        for index,change in enumerate(changes):
                            check(rows,f'{model}:{route}:{matching}:{profile}:{history}:{index}:reverse triangle',change['reverse_triangle_ratio'],1+1e-10,'bound')
                        label=f'{model}-{route}-m{matching}-{profile}-{history}'
                        save(ROOT/f'spectra/{label}.npz',frequency=reader.frequency,measure=reader.measure,heat=heat,
                            saved_potential=saved['potential'],saved_energy=saved['energy'],warm_delta=warm_delta['potential'],
                            cold_delta=addition['potential'],delta_high=combined_high,delta_low=combined_low,
                            conditional_high=final_high,conditional_low=final_low,conditional_energy_high=final_energy_high,
                            conditional_energy_low=final_energy_low,delta_residual=delta['residual'],
                            delta_metrics=delta_metrics,cold_metrics=cold_metrics,partial_MTS_allowance=budget['allowance'])
                        summaries.append(dict(label=label,model=model,route=route,matching=matching,profile=profile,history=history,
                            residual_changes=changes,combined_temperature_mu_y=delta_metrics[:3].tolist(),
                            cold_residual_over_MTS_allowance=(cold_metrics[3,2:4]/budget['allowance'][3]).tolist(),
                            combined_residual_over_MTS_allowance=(delta_metrics[3,2:4]/budget['allowance'][3]).tolist(),
                            MTS_residual_fraction=[entry['addition_norm']/entry['before'] for entry in changes[2:4]],
                            baseline_residual_fraction=[entry['addition_norm']/entry['before'] for entry in changes[:2]],
                            direct_cold_baseline_MTS_total_residual=cold_metrics[3].tolist()))
        print(json.dumps(dict(model=model,cases=sum(row['model']==model for row in summaries))),flush=True)
    return summaries

def run():
    config=protocol()
    assert not (ROOT/'results/status.json').exists()
    inputs=read(ROOT/'inputs.json');rows=[]
    boundary=boundary_audit(inputs,rows)
    summaries=spectrum_audit(config,inputs,rows)
    for name,value in inputs.items():
        assert digest(name)==value,name
    protected=BRANCH.parent.parent/'formalization-workbench'
    since=datetime.fromisoformat(config['turn_start']).timestamp()
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=since]
    check(rows,'protected-workbench recent mtime count',len(changed),0,'integrity')
    check(rows,'no bytecode or partial files',len(list(ROOT.rglob('__pycache__')))+len(list(ROOT.rglob('*.partial'))),0,'integrity')
    compile(Path(__file__).read_text(encoding='utf-8'),str(__file__),'exec')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-final.json',inputs)
    write(ROOT/'results/status.json',dict(stage=224,finished_at=now(),qualified=not failed,checks=rows,failed_checks=failed,
        summaries=summaries,boundary_audit=boundary,inputs_rehashed=len(inputs),protected_recent_mtime_count=len(changed),
        full_history_adopted=False,missing_complement_remains_explicit=True,new_integrals=0,new_evolutions=0,
        scope='Conditional signed sum of two disjoint repair intervals on the retained full reference; not a full-history correction'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),inputs=len(inputs),failures=failed[:12],
        combined_MTS_over_partial_allowance=max(max(row['combined_residual_over_MTS_allowance']) for row in summaries),
        combined_MTS_fraction=max(max(row['MTS_residual_fraction']) for row in summaries))),flush=True)

def seal():
    protocol()
    report=read(ROOT/'results/status.json')
    for name in ('RESULTS.md','NEXT.md'):
        assert (ROOT/name).is_file()
    inputs=read(ROOT/'inputs-final.json')
    for name,value in inputs.items():
        assert digest(name)==value,name
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    write(path,dict(stage=224,state='complete',qualified=report['qualified'],sealed_at=now(),
        consumed_and_immediate_rehashed=inputs,file_hashes={file.relative_to(ROOT).as_posix():digest(file) for file in ROOT.rglob('*') if file.is_file() and file!=path},
        bookmarks={str(file):digest(file) for file in (BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md')},scope=report['scope']))
    print(json.dumps(dict(seal=str(path),sha256=digest(path),qualified=report['qualified'])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run','seal'])
    globals()[parser.parse_args().phase]()
