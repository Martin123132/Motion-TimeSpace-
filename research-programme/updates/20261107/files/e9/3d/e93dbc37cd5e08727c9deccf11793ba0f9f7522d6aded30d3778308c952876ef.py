from cold40960_common import *
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['cold'],required=True)
    parser.add_argument('--steps',type=int,choices=[40960],default=40960)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    modest()
    folder=ROOT/'results'/(f'preflight-{args.model}' if args.dry_run else f'inner-{args.model}-n{args.steps}')
    assert not (folder/'COMPLETE').exists()
    folder.mkdir(parents=True,exist_ok=args.resume)
    started=time.monotonic()
    parent_path=INNER_PARENT/'results'/f'inner-{args.model}-n20480/prediction.npz'
    parent_status=local_packet(parent_path.parent)
    parent=read_npz(parent_path)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    background=thermal_wave.thermal.ThermalBackground(args.model)
    baseline,window,history_inputs=load_histories(args.model)
    inputs=[parent_path,parent_path.parent/'status.json',*ladder.inputs,*history_inputs,background.parent.source,background.native_constants]
    events=[]
    for epoch in range(65):
        path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'/f'epoch-{epoch:02d}.npz'
        inputs.append(path)
        events.append(read_npz(path))
    frequency=parent['frequency'].copy()
    count=len(frequency)
    assert count==5265
    spacing=float(parent_status['spacing'])
    low_margin=int(math.ceil(max(float(np.max(abs(np.log(event['ratios'])))) for event in events)/spacing))+2
    margin=low_margin+4
    offsets,low_bank,chemical,constant,minimum=positive_stencils(events,spacing,low_margin)
    high_offsets,high_bank,high_chemical,high_constant=high_stencils(events,spacing,4,margin)
    boundary_rows=int(max(0,-high_offsets[np.any(high_bank!=0,axis=0)].min()))
    all_grid=frequency[0]*np.exp(spacing*np.arange(-margin,count+margin))
    physical_grid=frequency[0]*np.exp(spacing*np.arange(-low_margin,count+low_margin))
    driver,normalization=make_drivers(basis,baseline,window,all_grid[margin:],.1)
    coefficients=parent['coefficient_bank'].copy()
    assert np.array_equal(offsets,parent['offsets'])
    assert np.array_equal(coefficients[:,:len(offsets)],low_bank)
    bank=interpolate.interp1d(parent['coefficient_knots'],coefficients,axis=0,bounds_error=True)
    high_at=interpolate.interp1d(parent['coordinate'],high_bank,axis=0,bounds_error=True)
    checks=[check('Positive interpolation chemical invariant',chemical,1e-9),check('Constant jump invariant',constant,1e-12),
        dict(name='Nonnegative two-point interpolation weights',value=minimum,passed=minimum>=0),
        check('Four-point chemical invariant',high_chemical,1e-9),check('Four-point constant invariant',high_constant,1e-12),
        dict(name='All coefficient and BR banks reused exactly',passed=np.array_equal(coefficients,parent['coefficient_bank']))]
    sparse_error=0.
    for epoch in [0,32,64]:
        direct=sparse.diags(low_bank[epoch],offsets,shape=(count,count),format='csc')
        inherited_matrix,unused_lower,unused_upper=split_matrix(low_bank[epoch],offsets,count)
        sparse_error=max(sparse_error,float(abs(direct-inherited_matrix).max()))
    checks.append(check('Direct diagonal assembly equals inherited slice',sparse_error,1e-14))
    for path in inputs:
        verify_source(path,chain)
    checks.append(dict(name='Frequency grid reused bitwise',passed=np.array_equal(frequency,parent['frequency'])))
    assert all(row['passed'] for row in checks)
    if args.dry_run:
        finish(folder,dict(checks=checks,model=args.model,nodes=count,steps=args.steps,
            dry_run=True,physical_inputs_unchanged=True,seconds=time.monotonic()-started),__file__,inputs)
        print(json.dumps(dict(model=args.model,dry_run=True,checks=len(checks),seconds=time.monotonic()-started)),flush=True)
        return
    start,end=parent['coordinate'][[0,-1]]
    step=(end-start)/args.steps
    old_outer=driver(float(start))[2:2+count,:3]
    older_outer=old_outer.copy()
    error=np.zeros_like(old_outer)
    previous_error=error.copy()
    output=dict(coordinate=[start],slope=[old_outer.copy()],outer_slope=[old_outer.copy()],defect=[error.copy()],lower_target=[])
    identity=sparse.eye(count,format='csc')
    solve_errors=np.zeros(3)
    start_index=0
    run_inputs={str(Path(path).resolve()):digest(path) for path in inputs}
    run_inputs[str(ROOT/'cold40960_common.py')]=digest(ROOT/'cold40960_common.py')
    checkpoint_folder=folder/'checkpoints'
    checkpoint_folder.mkdir(exist_ok=args.resume)
    if args.resume:
        choices=sorted(checkpoint_folder.glob('restart-*.json'))
        assert choices,'No complete restart snapshot exists'
        record=json.loads(choices[-1].read_text())
        restart_path=checkpoint_folder/record['archive']
        assert record['archive_sha256']==digest(restart_path)
        assert record['script_sha256']==digest(__file__)
        assert record['input_hashes']==run_inputs and record['steps']==args.steps
        restart=read_npz(restart_path)
        start_index=int(restart['completed_step'])+1
        error,previous_error=restart['error'],restart['previous_error']
        old_outer,older_outer=restart['old_outer'],restart['older_outer']
        solve_errors=restart['solve_errors']
        output={key:list(restart['saved_'+key]) for key in output}
    for index in range(start_index,args.steps+1):
        coordinate=float(start+(end-start)*index/args.steps)
        values=bank(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):len(offsets)+3]
        br_all=values[len(offsets)+3:]
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
        for offset,coefficient in zip(high_offsets,high_at(coordinate)):
            if offset and coefficient:
                transport+=coefficient*(all_outer[margin+offset:margin+offset+count]-outer)
        boundary_transport=np.zeros((boundary_rows,3))
        for offset,coefficient in zip(offsets,stencil):
            if offset and coefficient:
                boundary_transport+=coefficient*(all_outer[margin+offset:margin+offset+boundary_rows]-outer[:boundary_rows])
        transport[:boundary_rows]=boundary_transport
        source=clock_rate*(transport+eigenvalue*(outer-gas)+dc[:,None]*(hard-outer)+br[:,None]*(gas-outer))
        if index:
            generator=clock_rate*(sparse.diags(stencil,offsets,shape=(count,count),format='csc')+sparse.diags(eigenvalue-dc-br,format='csc'))
            leading,previous,older=(1.,-1.,0.) if index==1 else (1.5,-2.,.5)
            matrix=leading*identity-step*generator
            right=-previous*error-older*previous_error+step*source-(leading*outer+previous*old_outer+older*older_outer)
            updated=sparse_linalg.splu(matrix).solve(right)
            scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
            solve_errors=np.maximum(solve_errors,np.max(abs(matrix@updated-right),axis=0)/scale)
            previous_error,error=error,updated
            older_outer,old_outer=old_outer,outer
        if index%(args.steps//64)==0:
            output['lower_target'].append(lower.copy())
            if index:
                for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error)]:
                    output[key].append(np.array(value).copy())
        if index%(args.steps//8)==0:
            progress=dict(state='running',model=args.model,step=index,total=args.steps,seconds=time.monotonic()-started)
            print(json.dumps(progress),flush=True)
            write_json(folder/'progress.json',progress)
            restart_path=checkpoint_folder/f'restart-{index:05d}.npz'
            np.savez_compressed(restart_path,completed_step=index,error=error,previous_error=previous_error,
                old_outer=old_outer,older_outer=older_outer,solve_errors=solve_errors,
                **{'saved_'+key:np.array(value) for key,value in output.items()})
            write_json(restart_path.with_suffix('.json'),dict(archive=restart_path.name,
                archive_sha256=digest(restart_path),script_sha256=digest(__file__),
                input_hashes=run_inputs,steps=args.steps,completed_step=index))
            if (ROOT/'PAUSE-REQUESTED').exists() and index<args.steps:
                write_json(folder/'progress.json',dict(state='paused',step=index,total=args.steps,
                    restart=str(restart_path),reason='Safe checkpoint requested'))
                print(json.dumps(dict(state='paused',model=args.model,step=index)),flush=True)
                return
    checks.extend(check('Per-column solve:'+branch,value,1e-10) for branch,value in zip(['baseline','join1','join2'],solve_errors))
    checks.append(dict(name='Saved epochs and forcing unchanged',passed=
        np.array_equal(np.array(output['coordinate']),parent['coordinate']) and
        np.array_equal(np.array(output['outer_slope']),parent['outer_slope']) and
        np.array_equal(np.array(output['lower_target']),parent['lower_target'])))
    np.savez_compressed(folder/'prediction.npz',frequency=frequency,**{key:np.array(value) for key,value in output.items()},
        profiles=parent['profiles'],gas=parent['gas'],steps=args.steps,forcing_points=4,
        coefficient_knots=parent['coordinate'],coefficient_bank=coefficients,offsets=offsets)
    write_json(folder/'progress.json',dict(state='complete',model=args.model,step=args.steps,total=args.steps))
    finish(folder,dict(checks=checks,model=args.model,steps=args.steps,nodes=count,spacing=spacing,
        boundary_low_order_rows=boundary_rows,boundary_order_reduction_maximum_frequency=float(frequency[boundary_rows-1]),
        physical_lower_target_retained=True,saved_high_exterior_retained=True,feedback_uses_stored_defect=True,
        rational_reference_minimum_frequency=float(all_grid[margin]),new_scattering_events=0,parent_history_rerun=False,
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,checks=len(checks),failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
