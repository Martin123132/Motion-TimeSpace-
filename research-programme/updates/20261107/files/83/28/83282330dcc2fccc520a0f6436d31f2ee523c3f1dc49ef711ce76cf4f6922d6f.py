import os
for variable in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[variable]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import json
import hashlib
import argparse
ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH/'gas-curvature-energy-balance-20261020'
PARENT_SHA='792eac0e0da0056feac063c4a68de33a11b6c1b54a6f90389bf745a918df7b4d'
STARTED='2026-10-20T21:38:25+00:00'
sys.path.insert(0,str(PARENT))
import check_stage181 as previous
source,saved,np,mp,native,linear=previous.source,previous.saved,previous.np,previous.mp,previous.native,previous.linear
read,write=previous.read,previous.write
SPLIT=previous.PARENT
BANK=BRANCH/'upper-outer-frequency-temperature-test-20261020'
MODELS=['heavy','cold']


def authenticate():
    seal_path=PARENT/'results/stage-integrity.json'
    assert saved.digest(seal_path)==PARENT_SHA
    seal=read(seal_path)
    paths=dict(seal['consumed_and_immediate_rehashed'])
    paths.update({str(PARENT/name):checksum for name,checksum in seal['file_hashes'].items()})
    paths[str(seal_path)]=PARENT_SHA
    for filename,checksum in paths.items():
        assert saved.digest(filename)==checksum,filename
    return paths


def check(rows,name,value,tolerance=1e-10,category='identity'):
    value=float(value)
    rows.append(dict(name=name,value=float(value),tolerance=tolerance,passed=bool(np.isfinite(value) and abs(value)<=tolerance),category=category))


def prepare():
    assert not (ROOT/'configuration.json').exists()
    paths=authenticate()
    parent=read(PARENT/'configuration.json')
    selected=read(BANK/'configuration.json')['selected']
    assert parent['source_prediction_tolerance']==.01 and parent['identity_tolerance']==1e-10
    config=dict(stage=182,started_utc=STARTED,parent_seal_sha256=PARENT_SHA,
        source_prediction_tolerance=.01,identity_tolerance=1e-10,
        primary_start=5569,early_start=5553,end_index=5630,
        branches=['native','half','half_early'],history_tags=parent['history_tags'],offsets=parent['offsets'],
        expansion_span=parent['expansion_span'],anchor_fraction=parent['anchor_fraction'],
        selected=selected,source_operator_tag='anchor',source_scope='fixed-anchor isolated gas response; original full-source results preserved',
        prior_bookmark_normalized_sha256={str(path):hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
            for path in [BRANCH/'RESUME-CURRENT.md',BRANCH.parent/'CURRENT_LOCAL_RESUME.md']})
    assert len(selected)==36
    write(ROOT/'configuration.json',config)
    write(ROOT/'authenticated-inputs.json',paths)
    write(ROOT/'progress.json',dict(state='prepared'))
    print(json.dumps(dict(prepared=True,authenticated_paths=len(paths))),flush=True)


def validate_rule():
    rows=[]
    with mp.workdps(80):
        for ratio in [mp.mpf(1),mp.mpf('0.5')]:
            step=mp.mpf('0.0001')
            older=-step-step/ratio
            alpha=(1+2*ratio)/((1+ratio)*step)
            beta=(1+ratio)/step
            gamma=ratio**2/((1+ratio)*step)
            for degree in range(3):
                actual=alpha*(mp.mpf(0)**degree)-beta*((-step)**degree)+gamma*(older**degree)
                expected=1 if degree==1 else 0
                check(rows,f'BDF2 ratio{ratio} polynomial{degree}',abs(actual-expected))
    assert all(row['passed'] for row in rows)
    write(ROOT/'results/rule-checks.json',dict(checks=rows,all_checks_passed=True))


def evolve():
    config=read(ROOT/'configuration.json')
    paths=read(ROOT/'authenticated-inputs.json')
    validate_rule()
    ladder=native.infrared_ladder.InfraredLadder(native.BACKGROUND/'banks/infrared96-q700')
    basis=ladder.basis
    consumed=set(ladder.inputs)
    for model in MODELS:
        with np.load(PARENT/'results'/model/'state.npz') as packet:
            original={name:packet[name].copy() for name in packet.files}
        background=native.thermal_wave.thermal.ThermalBackground(model)
        emission=native.NonlocalEmission(basis,background,'nonlocal-leading',native.ROOT/'banks/s960-i256')
        consumed.update(emission.inputs)
        consumed.update([background.parent.source,background.native_constants])
        assert np.array_equal(basis.energy,original['energy_row'])
        assert np.array_equal(basis.temperature,original['temperature_template'])
        step=float(original['step'])
        heat=float(original['heat'])
        assert heat==background.chi
        for branch in config['branches']:
            destination=ROOT/'histories'/model/branch
            destination.mkdir(parents=True,exist_ok=True)
            start=config['early_start'] if branch=='half_early' else config['primary_start']
            divisor=1 if branch=='native' else 2
            local_step=step/divisor
            profile=original['profiles'][start].copy()
            older_profile=original['profiles'][start-1].copy()
            gas=float(original['temperature_scaled'][start])
            older_gas=float(original['temperature_scaled'][start-1])
            work=float(original['expansion_work'][start])
            older_work=float(original['expansion_work'][start-1])
            series=[[float(original['expansion'][start]),float(basis.energy@profile),gas,work]]
            profiles=[profile.copy()]
            diagnostics=[]
            for ordinal,tick in enumerate(range(start*divisor+1,config['end_index']*divisor+1),1):
                coordinate=tick*local_step
                local=background.at(coordinate)
                rate=local['coefficient']/local['thermal_parameter']
                stiffness=ladder.at(local['thermal_parameter'],0)[:basis.count,:basis.count]-emission.at(local['thermal_parameter'],'dcbr')
                if ordinal==1 and divisor==2:
                    ratio=.5
                    alpha=(1+2*ratio)/((1+ratio)*local_step)
                    vector=((1+ratio)*profile-ratio**2/(1+ratio)*older_profile)/local_step
                    scalar=((1+ratio)*gas-ratio**2/(1+ratio)*older_gas)/local_step
                    work_history=((1+ratio)*work-ratio**2/(1+ratio)*older_work)/local_step
                else:
                    alpha=1.5/local_step
                    vector=(2*profile-.5*older_profile)/local_step
                    scalar=(2*gas-.5*older_gas)/local_step
                    work_history=(2*work-.5*older_work)/local_step
                thermal_source=-rate*stiffness@basis.temperature
                solution=linear.solve(alpha*basis.mass-rate*stiffness,np.column_stack([basis.mass@vector,thermal_source]),assume_a='pos')
                free,response=solution[:,0],solution[:,1]
                new_gas=(heat*scalar-1-basis.energy@(alpha*free-vector))/(heat*(alpha+1)+alpha*(basis.energy@response))
                new_profile=free+response*new_gas
                new_work=(work_history+1+heat*new_gas)/alpha
                rhs=rate*stiffness@(new_profile-basis.temperature*new_gas)
                kinetic=alpha*basis.mass@new_profile-basis.mass@vector-rhs
                gas_residual=basis.energy@(alpha*new_profile-vector)+heat*((alpha+1)*new_gas-scalar)+1
                diagnostics.append(dict(tick=tick,kinetic_relative=float(np.linalg.norm(kinetic)/np.linalg.norm(rhs)),
                    gas_energy_residual=float(gas_residual),work_residual=float(alpha*new_work-work_history-1-heat*new_gas)))
                older_profile,profile=profile,new_profile
                older_gas,gas=gas,float(new_gas)
                older_work,work=work,float(new_work)
                series.append([coordinate,float(basis.energy@profile),gas,work])
                profiles.append(profile.copy())
            series=np.array(series)
            profiles=np.array(profiles)
            rows=[]
            if branch=='native':
                selected=slice(start,config['end_index']+1)
                for label,actual,expected in [('profiles',profiles,original['profiles'][selected]),
                    ('gas',series[:,2],original['temperature_scaled'][selected]),('work',series[:,3],original['expansion_work'][selected]),
                    ('coordinate',series[:,0],original['expansion'][selected])]:
                    assert np.array_equal(actual,expected),label
                    check(rows,'Native restart bitwise '+label,0)
            check(rows,'Integrated energy balance',np.max(abs(series[:,1]+heat*series[:,2]+series[:,3])))
            for field in ['kinetic_relative','gas_energy_residual','work_residual']:
                check(rows,field,max(abs(row[field]) for row in diagnostics))
            np.savez_compressed(destination/'history.npz',expansion=series[:,0],energy_scaled=series[:,1],temperature_scaled=series[:,2],
                expansion_work=series[:,3],profiles=profiles,heat=heat,step=local_step,start_index=start,end_index=config['end_index'],
                initial_profile=original['profiles'][start],initial_previous_profile=original['profiles'][start-1],
                initial_gas=original['temperature_scaled'][start],initial_previous_gas=original['temperature_scaled'][start-1],
                coordinates=original['coordinates'])
            write(destination/'status.json',dict(state='complete',checks=rows,all_checks_passed=all(row['passed'] for row in rows),
                diagnostics=diagnostics,updates=len(diagnostics),start_index=start,step=local_step,variable_step_startup=(divisor==2)))
            print(json.dumps(dict(model=model,branch=branch,updates=len(diagnostics),max_energy_residual=np.max(abs(series[:,1]+heat*series[:,2]+series[:,3])),
                checks_pass=all(row['passed'] for row in rows))),flush=True)
            write(ROOT/'progress.json',dict(state='histories',model=model,branch=branch,pid=os.getpid()))
    for path in consumed:
        assert str(path) in paths and saved.digest(path)==paths[str(path)],str(path)
    write(ROOT/'bank-inputs.json',{str(path):saved.digest(path) for path in sorted(consumed)})
    write(ROOT/'progress.json',dict(state='histories_complete'))


def curvature(samples):
    with mp.workdps(80):
        values=[mp.mpf(float(value)) for value in samples]
        coarse=(values[1]-2*values[0]+values[2])*10000
        fine=(values[3]-2*values[0]+values[4])*40000
        return np.array([float(coarse),float(fine),float(coarse-fine)])


def assess_histories():
    config=read(ROOT/'configuration.json')
    rows=list(read(ROOT/'results/rule-checks.json')['checks'])
    samples,curves,profile_samples={},{},{}
    outcomes=[]
    for model in MODELS:
        samples[model],curves[model],profile_samples[model]={},{},{}
        for branch in config['branches']:
            folder=ROOT/'histories'/model/branch
            rows.extend([dict(row,name=model+'/'+branch+': '+row['name']) for row in read(folder/'status.json')['checks']])
            with np.load(folder/'history.npz') as packet:
                coordinate,gas,profile=packet['expansion'],packet['temperature_scaled'],packet['profiles']
                targets=packet['coordinates']
                samples[model][branch]=np.interp(targets,coordinate,gas)
                profile_samples[model][branch]=np.stack([np.interp(targets,coordinate,profile[:,column]) for column in range(96)],axis=-1)
                if branch=='half':
                    samples[model]['half_thinned']=np.interp(targets,coordinate[::2],gas[::2])
        for branch,values in samples[model].items():
            curves[model][branch]=curvature(values)
        original=curves[model]['native']
        fine=curves[model]['half']
        thinned=curves[model]['half_thinned']
        early=curves[model]['half_early']
        evolution=thinned-original
        interpolation=fine-thinned
        closure=(fine-original)-evolution-interpolation
        check(rows,model+' refinement split closes',np.max(abs(closure)/np.maximum(abs(original),1e-300)))
        comparison=[]
        for order,label in enumerate(['coarse_curvature','fine_curvature','width_discrepancy']):
            relative=abs((fine[order]-original[order])/fine[order])
            startup=abs((early[order]-fine[order])/early[order])
            check(rows,model+' native/half '+label,relative,.01,'step_comparison')
            check(rows,model+' early/primary half '+label,startup,.01,'startup')
            comparison.append(dict(quantity=label,native=original[order],half=fine[order],half_thinned=thinned[order],half_early=early[order],
                relative_change=relative,startup_relative=startup,evolution_change=evolution[order],interpolation_change=interpolation[order]))
        outcome=dict(model=model,comparison=comparison,
            native_width_relative=abs(original[2]/original[1]),half_width_relative=abs(fine[2]/fine[1]),
            thinned_width_relative=abs(thinned[2]/thinned[1]),early_width_relative=abs(early[2]/early[1]))
        outcomes.append(outcome)
        print(json.dumps(outcome),flush=True)
    labels=['native','half','half_thinned','half_early']
    np.savez_compressed(ROOT/'results/history-curvature.npz',models=np.array(MODELS),branches=np.array(labels),
        profile_branches=np.array(config['branches']),
        samples=np.array([[samples[model][branch] for branch in labels] for model in MODELS]),
        curves=np.array([[curves[model][branch] for branch in labels] for model in MODELS]),
        profiles=np.array([[profile_samples[model][branch] for branch in config['branches']] for model in MODELS]))
    write(ROOT/'results/history-comparison.json',outcomes)
    write(ROOT/'results/history-checks.json',dict(checks=rows,count=len(rows),all_checks_passed=all(row['passed'] for row in rows)))
    write(ROOT/'progress.json',dict(state='history_assessment_complete'))


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','evolve','assess'])
    arguments=parser.parse_args()
    {'prepare':prepare,'evolve':evolve,'assess':assess_histories}[arguments.phase]()
