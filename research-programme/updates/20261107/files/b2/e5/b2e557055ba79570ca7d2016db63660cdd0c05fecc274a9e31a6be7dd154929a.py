from response_sites_common import *
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--steps',type=int,choices=[40960],default=40960)
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--restart-step',type=int,choices=RESTART_STEPS,default=0)
    args=parser.parse_args()
    modest()
    folder=ROOT/'results'/(f'preflight-{args.model}' if args.dry_run else f'replay-{args.model}-s{args.restart_step:05d}')
    assert not (folder/'COMPLETE').exists()
    folder.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    owner=refined_owner(args.model)
    parent_path=owner/'results'/f'inner-{args.model}-n40960/prediction.npz'
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
    record_path=parent_path.parent/'checkpoints'/f'restart-{args.restart_step:05d}.json'
    record=json.loads(record_path.read_text())
    restart_path=record_path.parent/record['archive']
    assert record['archive_sha256']==digest(restart_path)
    assert record['script_sha256']==digest(owner/'refine_inner_again.py')
    assert record['steps']==40960 and record['completed_step']==args.restart_step
    inputs.extend([record_path,restart_path,owner/'refine_inner_again.py'])
    for path,sha in record['input_hashes'].items():
        assert digest(path)==sha,path
        inputs.append(Path(path))
    restart=read_npz(restart_path)
    assert int(restart['completed_step'])==args.restart_step
    start,end=parent['coordinate'][[0,-1]]
    step=(end-start)/args.steps
    error,previous_error=restart['error'].copy(),restart['previous_error'].copy()
    old_outer,older_outer=restart['old_outer'].copy(),restart['older_outer'].copy()
    identity=sparse.eye(count,format='csc')
    solve_errors=np.zeros(3)
    output={key:[restart['saved_'+key][-1].copy()] for key in ['coordinate','slope','outer_slope','defect','lower_target']}
    saved_indices=[args.restart_step]
    stop_index=40960 if args.restart_step==35840 else args.restart_step+640
    for index in range(args.restart_step+1,stop_index+1):
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
        if index%20==0:
            for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error),('lower_target',lower)]:
                output[key].append(np.array(value).copy())
            saved_indices.append(index)
        if index%640==0:
            epoch=index//640
            checks.append(dict(name='Bitwise replay endpoint:'+str(epoch),passed=
                np.array_equal(error,parent['defect'][epoch]) and
                np.array_equal(outer,parent['outer_slope'][epoch]) and
                np.array_equal(lower,parent['lower_target'][epoch])))
            progress=dict(state='running',model=args.model,restart_step=args.restart_step,step=index,stop=stop_index,seconds=time.monotonic()-started)
            write_json(folder/'progress.json',progress)
            print(json.dumps(progress),flush=True)
    previous_path=PARENT/'results'/f'replay-{args.model}-s00000/prediction.npz'
    previous_prediction=read_npz(previous_path)
    assert local_packet(previous_path.parent)['all_checks_passed']
    inputs.extend([previous_path,previous_path.parent/'status.json'])
    for previous_index,previous_step in enumerate(previous_prediction['saved_step_indices']):
        if previous_step%20:
            continue
        current_index=saved_indices.index(int(previous_step))
        checks.append(dict(name='Bitwise saved site:'+str(previous_step),passed=
            all(np.array_equal(output[key][current_index],previous_prediction[key][previous_index])
                for key in ['coordinate','slope','outer_slope','defect','lower_target'])))
    checks.extend(check('Per-column solve:'+branch,value,1e-10) for branch,value in zip(['baseline','join1','join2'],solve_errors))
    coordinates=np.array(output['coordinate'])
    profiles=interpolate.interp1d(parent['coordinate'],parent['profiles'],axis=0,bounds_error=True)(coordinates)
    gases=interpolate.interp1d(parent['coordinate'],parent['gas'],axis=0,bounds_error=True)(coordinates)
    np.savez_compressed(folder/'prediction.npz',frequency=frequency,
        **{key:np.array(value) for key,value in output.items()},profiles=profiles,gas=gases,
        steps=40960,start_step=args.restart_step,stop_step=stop_index,saved_step_indices=np.array(saved_indices),
        coefficient_knots=parent['coefficient_knots'],coefficient_bank=coefficients,offsets=offsets)
    finish(folder,dict(checks=checks,model=args.model,nodes=count,steps=40960,start_step=args.restart_step,
        stop_step=stop_index,replayed_steps=stop_index-args.restart_step,original_restart=str(record_path),
        inner_coefficient_interpolation_unchanged=True,new_parent_history=False,
        output_profile_metadata_interpolated_not_used_as_forcing=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,restart_step=args.restart_step,checks=len(checks),
        failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
