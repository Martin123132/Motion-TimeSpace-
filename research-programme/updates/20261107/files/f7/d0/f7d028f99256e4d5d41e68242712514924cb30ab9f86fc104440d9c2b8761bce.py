from cubic_inner_common import *
import argparse
import hashlib
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--variant',choices=['control','cubic'],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'replay-{args.model}-{args.variant}'
    if (folder/'COMPLETE').exists():
        assert local_packet(folder)['all_checks_passed']
        print(json.dumps(dict(reused=str(folder))),flush=True)
        return
    folder.mkdir(parents=True,exist_ok=True)
    owner=refined_owner(args.model)
    parent_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
    parent=read_npz(parent_path)
    parent_status=local_packet(parent_path.parent)
    reference_path=P130/'results'/f'replay-{args.model}-balanced/prediction.npz'
    reference=read_npz(reference_path)
    prior_bank_path=P130/'results/balanced-coefficients/bank.npz'
    prior=read_npz(prior_bank_path)
    bank_path=ROOT/'results/coefficients/bank.npz'
    bank=read_npz(bank_path)
    assert local_packet(bank_path.parent)['all_checks_passed']
    frequency=parent['frequency'].copy()
    count=len(frequency)
    offsets=bank['offsets']
    low_margin=int(max(abs(offsets)))
    margin=low_margin+4
    spacing=float(bank['spacing'])
    assert count==5265 and spacing==float(parent_status['spacing'])
    assert np.array_equal(offsets,parent['offsets']) and np.array_equal(offsets,prior['offsets'])
    old_bank=interpolate.interp1d(parent['coefficient_knots'],parent['coefficient_bank'],axis=0,bounds_error=True)
    stencil_at=interpolate.interp1d(bank['coordinate'],bank['stencil'],axis=0,bounds_error=True)
    eigen_at=interpolate.interp1d(bank['coordinate'],bank['eigenvalue'],bounds_error=True)
    control_at=interpolate.interp1d(prior['coordinate'],prior['low'],axis=0,bounds_error=True)
    control_eigen=interpolate.interp1d(prior['coordinate'],prior['eigenvalue'],bounds_error=True)
    high_at=interpolate.interp1d(prior['coordinate'],prior['high'],axis=0,bounds_error=True)
    high_offsets=prior['high_offsets']
    boundary_rows=int(max(0,-high_offsets[np.any(prior['old_high']!=0,axis=0)].min()))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    baseline,window,history_inputs=load_histories(args.model)
    all_grid=frequency[0]*np.exp(spacing*np.arange(-margin,count+margin))
    physical_grid=frequency[0]*np.exp(spacing*np.arange(-low_margin,count+low_margin))
    driver,normalization=make_drivers(basis,baseline,window,all_grid[margin:],.1)
    record_path=parent_path.parent/'checkpoints/restart-00000.json'
    record=json.loads(record_path.read_text())
    restart_path=record_path.parent/record['archive']
    assert digest(restart_path)==record['archive_sha256']
    assert record['completed_step']==0 and record['steps']==40960
    assert digest(owner/'refine_inner_again.py')==record['script_sha256']
    inputs=[parent_path,parent_path.parent/'status.json',reference_path,reference_path.parent/'status.json',
        prior_bank_path,bank_path,bank_path.parent/'status.json',record_path,restart_path,
        owner/'refine_inner_again.py',*ladder.inputs,*history_inputs,background.parent.source,background.native_constants]
    for name,sha in record['input_hashes'].items():
        assert digest(name)==sha,name
        inputs.append(Path(name))
    paths=set(inputs+[ROOT/'cubic_inner_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md',Path(__file__).resolve()])
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
        saved_record=json.loads(choices[-1].read_text())
        assert saved_record['fingerprint_sha256']==fingerprint_hash
        state_path=checkpoints/saved_record['archive']
        assert digest(state_path)==saved_record['archive_sha256']
        restart=read_npz(state_path)
        start_index=int(restart['completed_step'])
        output={key:list(restart[key]) for key in ['coordinate','slope','outer_slope','defect','lower_target']}
        saved_indices=restart['saved_indices'].tolist()
        solve_errors=restart['solve_errors'].copy()
        budget=list(restart['budget'])
    else:
        restart=read_npz(restart_path)
        start_index=0
        output={key:[reference[key][0].copy()] for key in ['coordinate','slope','outer_slope','defect','lower_target']}
        saved_indices=[0]
        solve_errors=np.zeros(3)
        budget=[]
    error,previous_error=restart['error'].copy(),restart['previous_error'].copy()
    old_outer,older_outer=restart['old_outer'].copy(),restart['older_outer'].copy()
    start,end=parent['coordinate'][[0,-1]]
    step=(end-start)/40960
    identity=sparse.eye(count,format='csc')
    measure=(frequency/frequency[-1])**3
    deadline=os.environ.get('MTS_DEADLINE_UTC')
    deadline=datetime.fromisoformat(deadline) if deadline else None
    for index in range(start_index+1,641):
        coordinate=float(start+(end-start)*index/40960)
        values=old_bank(coordinate)
        unused_eigen,dc_constant,clock_rate=values[len(offsets):len(offsets)+3]
        assert dc_constant>0 and clock_rate>0
        if args.variant=='control':
            stencil=control_at(coordinate)
            eigenvalue=float(control_eigen(coordinate))
        else:
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
        leading,previous,older=(1.,-1.,0.) if index==1 else (1.5,-2.,.5)
        matrix=leading*identity-step*generator
        right=-previous*error-older*previous_error+step*source-(leading*outer+previous*old_outer+older*older_outer)
        updated=sparse_linalg.splu(matrix).solve(right)
        scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
        solve_errors=np.maximum(solve_errors,np.max(abs(matrix@updated-right),axis=0)/scale)
        if args.variant=='cubic':
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
            residual=leading*current+previous*previous_state+older*older_state-step*(generator@current+force)
            residual_scale=np.maximum(np.max(abs(matrix)@abs(current)+abs(previous*previous_state)+abs(older*older_state)+step*abs(force),axis=0),1e-300)
            total_equation_error=np.max(abs(residual),axis=0)/residual_scale
            def inner(left,right):
                return np.sum(measure[:,None]*left*right,axis=0)
            dissipation=step*inner(current,generator@current)
            volume_work=step*inner(current,volume_force)
            boundary_work=step*inner(current,boundary_force)
            if index==1:
                change=(inner(current,current)-inner(previous_state,previous_state))/2
                numerical=inner(current-previous_state,current-previous_state)/2
            else:
                change=(inner(current,current)+inner(2*current-previous_state,2*current-previous_state)
                    -inner(previous_state,previous_state)-inner(2*previous_state-older_state,2*previous_state-older_state))/4
                numerical=inner(current-2*previous_state+older_state,current-2*previous_state+older_state)/4
            scale_budget=np.maximum(abs(change)+abs(numerical)+abs(dissipation)+abs(volume_work)+abs(boundary_work),1e-300)
            budget_error=abs(change+numerical-dissipation-volume_work-boundary_work)/scale_budget
            budget.append(np.array([change,numerical,dissipation,volume_work,boundary_work,budget_error,total_equation_error]))
        previous_error,error=error,updated
        older_outer,old_outer=old_outer,outer
        if index%20==0:
            for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error),('lower_target',lower)]:
                output[key].append(np.array(value).copy())
            saved_indices.append(index)
        if index%80==0:
            path=checkpoints/f'restart-{index:05d}.npz'
            np.savez_compressed(path,completed_step=index,error=error,previous_error=previous_error,old_outer=old_outer,older_outer=older_outer,
                saved_indices=saved_indices,solve_errors=solve_errors,budget=np.array(budget),**{key:np.array(value) for key,value in output.items()})
            write_json(path.with_suffix('.json'),dict(archive=path.name,archive_sha256=digest(path),fingerprint_sha256=fingerprint_hash,completed_step=index))
            write_json(folder/'progress.json',dict(state='running',completed_step=index,total_steps=640,seconds=time.monotonic()-started))
            print(json.dumps(dict(model=args.model,variant=args.variant,step=index,seconds=time.monotonic()-started)),flush=True)
            if deadline and datetime.now(timezone.utc)>=deadline and index<640:
                raise SystemExit(75)
    checks=[check('Sparse solve:'+column,value,1e-10) for column,value in zip(['baseline','join1','join2'],solve_errors)]
    for key in ['coordinate','outer_slope','lower_target']:
        checks.append(dict(name='Unchanged driver/boundary:'+key,passed=np.array_equal(np.array(output[key]),reference[key])))
    checks.append(dict(name='Unchanged initial defect',passed=np.array_equal(output['defect'][0],reference['defect'][0])))
    if args.variant=='control':
        checks.append(dict(name='Bitwise Stage130 control',passed=np.array_equal(np.array(output['defect']),reference['defect'])))
    else:
        budget=np.array(budget)
        checks.append(dict(name='All steps homogeneous weighted dissipation nonpositive',passed=bool(np.all(budget[:,2]<=0))))
        for position,label in [(5,'BDF norm budget'),(6,'Total-field boundary equation')]:
            checks.extend(check(label+':'+column,value,1e-8) for column,value in zip(['baseline','join1','join2'],np.max(budget[:,position],axis=0)))
    delta=np.array(output['defect'])-reference['defect']
    assert all(row['passed'] for row in checks),checks
    np.savez_compressed(folder/'prediction.npz',frequency=frequency,saved_step_indices=saved_indices,
        **{key:np.array(value) for key,value in output.items()},profiles=reference['profiles'],gas=reference['gas'],budget=np.array(budget))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,model=args.model,variant=args.variant,steps=640,saved_sites=33,
        frequency_nodes=5265,full_history_inner_steps=40960,solve_errors=solve_errors.tolist(),
        endpoint_defect_difference_max=np.max(abs(delta[-1]),axis=0).tolist(),
        endpoint_defect_relative=(np.max(abs(delta[-1]),axis=0)/np.maximum(np.max(abs(reference['defect'][-1]),axis=0),1e-300)).tolist(),
        budget_columns=['change','numerical_dissipation','generator_work','volume_work','boundary_work','relative_budget_error','relative_total_equation_error'],
        norm_budget_is_physical_energy=False,later_history_carried=False,endpoint_restart_saved=True,seconds=time.monotonic()-started),__file__,[*inputs,folder/'INPUTS.json'])


if __name__=='__main__':
    main()
