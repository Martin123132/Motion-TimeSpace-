from transient_common import *
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
    frozen_output=[error.copy()]
    initial_audit={}
    frozen_error=error.copy()
    frozen_previous=error.copy()
    frozen_solve_errors=np.zeros(3)
    slope_endpoint=min(float(baseline['expansion'][np.searchsorted(baseline['expansion'],start,side='right')]),
        float(window['coordinate'][np.searchsorted(window['coordinate'],start,side='right')]))
    initial_outer_derivative=(driver(slope_endpoint)[2:2+count,:3]-driver(float(start))[2:2+count,:3])/(slope_endpoint-start)
    first_interval_end=float(start+(end-start)*640/args.steps)
    initial_audit['driver_first_linear_segment_end']=slope_endpoint
    initial_audit['baseline_knots_inside_first_interval']=int(np.count_nonzero((baseline['expansion']>start)&(baseline['expansion']<first_interval_end)))
    initial_audit['window_knots_inside_first_interval']=int(np.count_nonzero((window['coordinate']>start)&(window['coordinate']<first_interval_end)))
    for index in range(0,stop_index+1):
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
        generator=clock_rate*(sparse.diags(stencil,offsets,shape=(count,count),format='csc')+sparse.diags(eigenvalue-dc-br,format='csc'))
        if index==0:
            frozen_generator=generator.copy()
            initial_drive=source-initial_outer_derivative
            frozen_be_matrix=identity-step*frozen_generator
            frozen_bdf_matrix=1.5*identity-step*frozen_generator
            frozen_be=sparse_linalg.splu(frozen_be_matrix)
            frozen_bdf=sparse_linalg.splu(frozen_bdf_matrix)
            initial_audit['zero_saved_initial_defect']=not bool(np.count_nonzero(error))
            initial_audit['inner_coordinate_step']=float(step)
            initial_audit['maximum_generator_row_sum']=float(np.max(np.asarray(generator.sum(axis=1))))
            initial_audit['absolute_diagonal_rate_range']=[float(np.min(abs(generator.diagonal()))),float(np.max(abs(generator.diagonal())))]
            np.savez_compressed(folder/'initial-law.npz',initial_drive=initial_drive,outer_derivative=initial_outer_derivative,
                initial_source=source,initial_error=error,step=step,frequency=frequency)
            sparse.save_npz(folder/'initial-generator.npz',generator)
            continue
        if index:
            leading,previous,older=(1.,-1.,0.) if index==1 else (1.5,-2.,.5)
            matrix=leading*identity-step*generator
            right=-previous*error-older*previous_error+step*source-(leading*outer+previous*old_outer+older*older_outer)
            updated=sparse_linalg.splu(matrix).solve(right)
            scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
            solve_errors=np.maximum(solve_errors,np.max(abs(matrix@updated-right),axis=0)/scale)
            frozen_right=-previous*frozen_error-older*frozen_previous+step*initial_drive
            frozen_updated=(frozen_be if index==1 else frozen_bdf).solve(frozen_right)
            frozen_matrix=frozen_be_matrix if index==1 else frozen_bdf_matrix
            frozen_scale=np.maximum(np.max(abs(frozen_matrix)@abs(frozen_updated)+abs(frozen_right),axis=0),1e-300)
            frozen_solve_errors=np.maximum(frozen_solve_errors,np.max(abs(frozen_matrix@frozen_updated-frozen_right),axis=0)/frozen_scale)
            if index==1:
                discrete_drive=source-(outer-old_outer)/step
                law_scale=np.maximum(np.max(abs(updated)+step*(abs(generator)@abs(updated)+abs(discrete_drive)),axis=0),1e-300)
                law_error=np.max(abs(updated-step*(generator@updated+discrete_drive)),axis=0)/law_scale
                checks.extend(check('Exact first-step resolvent:'+column,value,1e-10) for column,value in zip(['baseline','join1','join2'],law_error))
                initial_audit['first_step_resolvent_errors']=law_error.tolist()
                initial_audit['naive_slope_error_relative_to_frozen_step']=(np.max(abs(frozen_updated-step*initial_drive),axis=0)/np.maximum(np.max(abs(frozen_updated),axis=0),1e-300)).tolist()
                np.savez_compressed(folder/'first-step-law.npz',generator_source=source,outer=outer,old_outer=old_outer,
                    actual=updated,frozen=frozen_updated,discrete_drive=discrete_drive)
                sparse.save_npz(folder/'first-generator.npz',generator)
            frozen_previous,frozen_error=frozen_error,frozen_updated
            previous_error,error=error,updated
            older_outer,old_outer=old_outer,outer
        if index in SAMPLE_STEPS:
            for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error),('lower_target',lower)]:
                output[key].append(np.array(value).copy())
            saved_indices.append(index)
            frozen_output.append(frozen_error.copy())
        if index%640==0:
            epoch=index//640
            checks.append(dict(name='Bitwise replay endpoint:'+str(epoch),passed=
                np.array_equal(error,parent['defect'][epoch]) and
                np.array_equal(outer,parent['outer_slope'][epoch]) and
                np.array_equal(lower,parent['lower_target'][epoch])))
            progress=dict(state='running',model=args.model,restart_step=args.restart_step,step=index,stop=stop_index,seconds=time.monotonic()-started)
            write_json(folder/'progress.json',progress)
            print(json.dumps(progress),flush=True)
    old_probe_path=PARENT/'results'/f'replay-{args.model}-s00000/prediction.npz'
    old_probe=read_npz(old_probe_path)
    inputs.extend([old_probe_path,old_probe_path.parent/'status.json'])
    for old_index,old_step in enumerate(old_probe['saved_step_indices']):
        new_index=saved_indices.index(int(old_step))
        checks.append(dict(name='Bitwise quarter replay:'+str(old_step),passed=
            np.array_equal(output['defect'][new_index],old_probe['defect'][old_index]) and
            np.array_equal(output['outer_slope'][new_index],old_probe['outer_slope'][old_index])))
    checks.extend(check('Frozen solve:'+branch,value,1e-10) for branch,value in zip(['baseline','join1','join2'],frozen_solve_errors))
    checks.append(dict(name='Initial matching unchanged',passed=initial_audit['zero_saved_initial_defect']))
    np.savez_compressed(folder/'frozen-reference.npz',coordinate=np.array(output['coordinate']),
        saved_step_indices=np.array(saved_indices),defect=np.array(frozen_output))
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
        inner_coefficient_interpolation_unchanged=True,new_parent_history=False,initial_audit=initial_audit,
        output_profile_metadata_interpolated_not_used_as_forcing=True,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(model=args.model,restart_step=args.restart_step,checks=len(checks),
        failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
