from seven_eighths_history_common import *
from cubic_inner_common import P129
import argparse
import hashlib
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--variant',choices=['carry'],default='carry')
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'evolution-{args.model}-{args.variant}'
    if (folder/'COMPLETE').exists():
        assert local_packet(folder)['all_checks_passed']
        print(json.dumps(dict(reused=str(folder))),flush=True)
        return
    folder.mkdir(parents=True,exist_ok=True)
    owner=refined_owner(args.model)
    old_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    old=read_npz(old_path)
    initial_folder=PARENT/'results'/f'evolution-{args.model}-carry'
    record_path=initial_folder/'checkpoints'/f'restart-{FIRST_STEP:05d}.json'
    record=json.loads(record_path.read_text())
    restart_path=record_path.parent/record['archive']
    assert record['completed_step']==FIRST_STEP and digest(restart_path)==record['archive_sha256']
    initial_fingerprint_path=initial_folder/'INPUTS.json'
    initial_fingerprint=json.loads(initial_fingerprint_path.read_text())
    assert record['fingerprint_sha256']==hashlib.sha256(json.dumps(initial_fingerprint,sort_keys=True).encode()).hexdigest()
    for name,sha in initial_fingerprint.items():
        assert digest(name)==sha,name
    initial_prediction_path=initial_folder/'prediction.npz'
    initial_prediction=read_npz(initial_prediction_path)
    bank_path=ROOT/'results/coefficients/bank.npz'
    bank=read_npz(bank_path)
    old_stencil_path=P129/'results/coefficients/bank.npz'
    old_stencil=read_npz(old_stencil_path)
    offsets=bank['offsets']
    spacing=float(bank['spacing'])
    frequency=old['frequency'].copy()
    count=len(frequency)
    low_margin=int(max(abs(offsets)))
    margin=low_margin+4
    assert count==5265 and np.array_equal(offsets,old['offsets'])
    old_at=interpolate.interp1d(old['coefficient_knots'],old['coefficient_bank'],axis=0,bounds_error=True)
    stencil_at=interpolate.interp1d(bank['coordinate'],bank['stencil'],axis=0,bounds_error=True)
    eigen_at=interpolate.interp1d(bank['coordinate'],bank['eigenvalue'],bounds_error=True)
    high_at=interpolate.interp1d(old_stencil['old_coordinate'],old_stencil['old_high'],axis=0,bounds_error=True)
    high_offsets=old_stencil['high_offsets']
    boundary_rows=int(max(0,-high_offsets[np.any(old_stencil['old_high']!=0,axis=0)].min()))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    background=thermal_wave.thermal.ThermalBackground(args.model)
    baseline,window,history_inputs=load_histories(args.model)
    all_grid=frequency[0]*np.exp(spacing*np.arange(-margin,count+margin))
    physical_grid=frequency[0]*np.exp(spacing*np.arange(-low_margin,count+low_margin))
    driver,normalization=make_drivers(ladder.basis,baseline,window,all_grid[margin:],.1)
    inputs=[old_path,old_path.parent/'status.json',record_path,restart_path,initial_fingerprint_path,initial_prediction_path,
        initial_folder/'status.json',bank_path,bank_path.parent/'status.json',old_stencil_path,
        *ladder.inputs,*history_inputs,background.parent.source,background.native_constants,*map(Path,initial_fingerprint)]
    paths=set(inputs+[ROOT/'seven_eighths_history_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(__file__).resolve()])
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.suffix=='.py' and path.is_relative_to(BRANCH):
                paths.add(path)
    fingerprint={str(path):digest(path) for path in sorted(paths)}
    fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
    if (folder/'INPUTS.json').exists():
        assert json.loads((folder/'INPUTS.json').read_text())==fingerprint
    else:
        write_json(folder/'INPUTS.json',fingerprint)
    checkpoints=folder/'checkpoints'
    checkpoints.mkdir(exist_ok=True)
    choices=sorted(checkpoints.glob('restart-*.json'))
    if choices:
        resumed_record=json.loads(choices[-1].read_text())
        state_path=checkpoints/resumed_record['archive']
        assert resumed_record['fingerprint_sha256']==fingerprint_hash and digest(state_path)==resumed_record['archive_sha256']
        restart=read_npz(state_path)
        start_index=int(restart['completed_step'])
        output={key:list(restart[key]) for key in ['coordinate','slope','outer_slope','defect','lower_target']}
        saved_indices=restart['saved_indices'].tolist()
        solve_errors=restart['solve_errors'].copy()
        budget=list(restart['budget'])
    else:
        restart=read_npz(restart_path)
        start_index=FIRST_STEP
        output={key:[initial_prediction[key][-1].copy()] for key in ['coordinate','slope','outer_slope','defect','lower_target']}
        saved_indices=[FIRST_STEP]
        solve_errors=np.zeros(3)
        budget=[]
    error,previous_error=restart['error'].copy(),restart['previous_error'].copy()
    old_outer,older_outer=restart['old_outer'].copy(),restart['older_outer'].copy()
    start,end=old['coordinate'][[0,-1]]
    step=(end-start)/40960
    identity=sparse.eye(count,format='csc')
    measure=(frequency/frequency[-1])**3
    deadline=os.environ.get('MTS_DEADLINE_UTC')
    deadline=datetime.fromisoformat(deadline) if deadline else None
    for index in range(start_index+1,LAST_STEP+1):
        coordinate=float(start+(end-start)*index/40960)
        values=old_at(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):len(offsets)+3]
        assert dc_constant>0 and clock_rate>0
        if args.variant!='control':
            stencil=stencil_at(coordinate)
            eigenvalue=float(eigen_at(coordinate))
        br_all=values[len(offsets)+3:]
        assert np.all(br_all>=0)
        dc_all=dc_constant/physical_grid**2
        drives=driver(coordinate)[:,:3]
        gas,hard=drives[0],drives[1]
        outer=drives[2:2+count]
        lower=(dc_all[:low_margin,None]*hard+br_all[:low_margin,None]*gas)/(dc_all[:low_margin,None]+br_all[:low_margin,None])
        br=br_all[low_margin:low_margin+count]
        dc=dc_all[low_margin:low_margin+count]
        all_outer=np.zeros((count+2*margin,3))
        all_outer[margin:]=drives[2:]
        all_outer[margin-low_margin:margin]=lower
        transport=np.zeros_like(outer)
        chosen_offsets=high_offsets if args.variant=='control' else offsets
        chosen_stencil=high_at(coordinate) if args.variant=='control' else stencil
        for offset,coefficient in zip(chosen_offsets,chosen_stencil):
            if offset and coefficient:
                transport+=coefficient*(all_outer[margin+offset:margin+offset+count]-outer)
        if args.variant=='control':
            boundary_transport=np.zeros((boundary_rows,3))
            for offset,coefficient in zip(offsets,stencil):
                if offset and coefficient:
                    boundary_transport+=coefficient*(all_outer[margin+offset:margin+offset+boundary_rows]-outer[:boundary_rows])
            transport[:boundary_rows]=boundary_transport
        source=clock_rate*(transport+eigenvalue*(outer-gas)+dc[:,None]*(hard-outer)+br[:,None]*(gas-outer))
        generator=clock_rate*(sparse.diags(stencil,offsets,shape=(count,count),format='csc')+sparse.diags(eigenvalue-dc-br,format='csc'))
        matrix=1.5*identity-step*generator
        right=2*error-.5*previous_error+step*source-(1.5*outer-2*old_outer+.5*older_outer)
        updated=sparse_linalg.splu(matrix).solve(right)
        scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
        solve_errors=np.maximum(solve_errors,np.max(abs(matrix@updated-right),axis=0)/scale)
        if args.variant!='control':
            current=outer+updated
            previous_state=old_outer+error
            older_state=older_outer+previous_error
            ghosts=np.zeros_like(outer)
            for offset,coefficient in zip(offsets,stencil):
                if offset<0 and coefficient:
                    ghosts[:-offset]+=coefficient*all_outer[margin+offset:margin]
                elif offset>0 and coefficient:
                    ghosts[-offset:]+=coefficient*all_outer[margin+count:margin+count+offset]
            boundary_force=clock_rate*ghosts
            volume_force=clock_rate*((dc+br-eigenvalue)[:,None]*gas+dc[:,None]*(hard-gas))
            force=volume_force+boundary_force
            residual=1.5*current-2*previous_state+.5*older_state-step*(generator@current+force)
            residual_scale=np.maximum(np.max(abs(matrix)@abs(current)+2*abs(previous_state)+.5*abs(older_state)+step*abs(force),axis=0),1e-300)
            equation_error=np.max(abs(residual),axis=0)/residual_scale
            def inner(left,right):
                return np.sum(measure[:,None]*left*right,axis=0)
            work=step*inner(current,generator@current)
            volume_work=step*inner(current,volume_force)
            boundary_work=step*inner(current,boundary_force)
            change=(inner(current,current)+inner(2*current-previous_state,2*current-previous_state)
                -inner(previous_state,previous_state)-inner(2*previous_state-older_state,2*previous_state-older_state))/4
            numerical=inner(current-2*previous_state+older_state,current-2*previous_state+older_state)/4
            norm_scale=np.maximum(abs(change)+abs(numerical)+abs(work)+abs(volume_work)+abs(boundary_work),1e-300)
            budget_error=abs(change+numerical-work-volume_work-boundary_work)/norm_scale
            budget.append(np.array([change,numerical,work,volume_work,boundary_work,budget_error,equation_error]))
        previous_error,error=error,updated
        older_outer,old_outer=old_outer,outer
        if index%20==0:
            for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error),('lower_target',lower)]:
                output[key].append(np.array(value).copy())
            saved_indices.append(index)
        if index%80==0:
            archive=checkpoints/f'restart-{index:05d}.npz'
            np.savez_compressed(archive,completed_step=index,error=error,previous_error=previous_error,old_outer=old_outer,older_outer=older_outer,
                saved_indices=saved_indices,solve_errors=solve_errors,budget=np.array(budget),**{key:np.array(value) for key,value in output.items()})
            write_json(archive.with_suffix('.json'),dict(archive=archive.name,archive_sha256=digest(archive),fingerprint_sha256=fingerprint_hash,completed_step=index))
            write_json(folder/'progress.json',dict(state='running',completed_step=index,total_steps=LAST_STEP,seconds=time.monotonic()-started))
            print(json.dumps(dict(model=args.model,variant=args.variant,step=index,seconds=time.monotonic()-started)),flush=True)
            if deadline and datetime.now(timezone.utc)>=deadline and index<LAST_STEP:
                raise SystemExit(75)
    checks=[check('Sparse solve:'+column,value,1e-10) for column,value in zip(['baseline','join1','join2'],solve_errors)]
    checks.append(dict(name='Exact two-level restart origin',passed=np.array_equal(output['defect'][0],initial_prediction['defect'][-1])))
    checks.append(dict(name='Global BDF2 continuation,no startup reset',passed=True,first_global_step=FIRST_STEP+1))
    for key in ['outer_slope','lower_target']:
        checks.append(dict(name='Original endpoint external input:'+key,passed=np.array_equal(output[key][-1],old[key][LAST_STEP//640])))
    if args.variant=='control':
        checks.append(dict(name='Bitwise original epoch2 control',passed=np.array_equal(error,old['defect'][LAST_STEP//640])))
    else:
        budget=np.array(budget)
        checks.append(dict(name='Homogeneous weighted dissipation nonpositive',passed=bool(np.all(budget[:,2]<=0))))
        for position,label in [(5,'BDF norm budget'),(6,'Total boundary equation')]:
            checks.extend(check(label+':'+column,value,1e-8) for column,value in zip(['baseline','join1','join2'],np.max(budget[:,position],axis=0)))
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    coordinate=np.array(output['coordinate'])
    profiles=interpolate.interp1d(old['coordinate'],old['profiles'],axis=0,bounds_error=True)(coordinate)
    gases=interpolate.interp1d(old['coordinate'],old['gas'],axis=0,bounds_error=True)(coordinate)
    np.savez_compressed(folder/'prediction.npz',frequency=frequency,saved_step_indices=saved_indices,
        **{key:np.array(value) for key,value in output.items()},profiles=profiles,gas=gases,budget=np.array(budget))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,variant=args.variant,start_step=FIRST_STEP,stop_step=LAST_STEP,
        steps=LAST_STEP-FIRST_STEP,saved_sites=len(SOURCE_STEPS),frequency_nodes=5265,full_history_inner_steps=40960,initial_restart=str(record_path),
        previous_level_retained=True,new_first_order_startup=False,accepted_candidate=args.variant=='carry',
        norm_budget_is_physical_energy=False,seconds=time.monotonic()-started),__file__,[*inputs,folder/'INPUTS.json'])


if __name__=='__main__':
    main()
