from repair_common import *
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--variant',choices=['fine','space'],default='fine')
    parser.add_argument('--points',type=int,choices=[4,6],default=4)
    parser.add_argument('--steps',type=int,choices=[5120,10240],default=5120)
    args=parser.parse_args()
    modest()
    label=f'inner-{args.model}-{args.variant}-p{args.points}-n{args.steps}'
    folder=ROOT/'results'/label
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prediction,profiles,gas_history,inputs=read_prediction(args.model,args.variant)
    baseline,window,history_inputs=load_histories(args.model)
    inputs.extend([*ladder.inputs,*history_inputs])
    events=[]
    for epoch in range(65):
        path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'/f'epoch-{epoch:02d}.npz'
        inputs.append(path)
        events.append(read_npz(path))
    for path in inputs:
        verify_source(path,chain)
    frequency=prediction['frequency']
    spacing=float(np.log(frequency[1]/frequency[0]))
    offsets=prediction['offsets']
    low_margin=int(max(abs(offsets)))
    margin=low_margin+4
    count=len(frequency)
    all_grid=frequency[0]*np.exp(spacing*np.arange(-margin,count+margin))
    inside_grid=all_grid[margin:]
    assert inside_grid.min()>=basis.minimum
    driver,normalization=make_drivers(basis,baseline,window,inside_grid,.1)
    high_offsets,high_bank,chemical,weights=high_stencils(events,spacing,args.points,margin)
    boundary_rows=int(max(0,-high_offsets[np.any(high_bank!=0,axis=0)].min()))
    high_at=interpolate.interp1d(prediction['coordinate'],high_bank,axis=0,bounds_error=True)
    prefix=len(offsets)+3
    bank=interpolate.interp1d(prediction['coefficient_knots'],prediction['coefficient_bank'],axis=0,bounds_error=True)
    start,end=prediction['coordinate'][[0,-1]]
    step=(end-start)/args.steps
    old_outer=driver(float(start))[2:2+count,:3]
    older_outer=old_outer.copy()
    error=np.zeros_like(old_outer)
    previous_error=error.copy()
    output=dict(coordinate=[start],slope=[old_outer.copy()],outer_slope=[old_outer.copy()],
                defect=[error.copy()],lower_target=[])
    identity=sparse.eye(count,format='csc')
    errors=np.zeros(3)
    equilibrium_error=0.
    started=time.monotonic()
    for index in range(args.steps+1):
        coordinate=float(start+(end-start)*index/args.steps)
        values=bank(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):prefix]
        br_all=values[prefix:]
        dc_all=dc_constant/(frequency[0]*np.exp(spacing*np.arange(-low_margin,count+low_margin)))**2
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
        internal,lower_matrix,upper_matrix=split_matrix(stencil,offsets,count)
        row_sum=internal@np.ones(count)+lower_matrix@np.ones(low_margin)+upper_matrix@np.ones(low_margin)
        equilibrium_error=max(equilibrium_error,float(np.max(abs(row_sum))))
        if index:
            generator=clock_rate*(internal+sparse.diags(eigenvalue-dc-br,format='csc'))
            leading,previous,older=(1.,-1.,0.) if index==1 else (1.5,-2.,.5)
            matrix=leading*identity-step*generator
            right=-previous*error-older*previous_error+step*source-(leading*outer+previous*old_outer+older*older_outer)
            updated=sparse_linalg.splu(matrix).solve(right)
            scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
            errors=np.maximum(errors,np.max(abs(matrix@updated-right),axis=0)/scale)
            previous_error,error=error,updated
            older_outer,old_outer=old_outer,outer
        if index%(args.steps//64)==0:
            output['lower_target'].append(lower.copy())
            if index:
                for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect',error)]:
                    output[key].append(np.array(value).copy())
        if index%(args.steps//4)==0:
            print(json.dumps(dict(case=label,step=index,total=args.steps,seconds=time.monotonic()-started)),flush=True)
            write_json(folder/'progress.json',dict(state='running',completed_steps=index,total_steps=args.steps))
    checks=[check('High-order chemical invariant',chemical,1e-9),check('High-order constant invariant',weights,1e-12),
            check('Equal-temperature equilibrium transport',equilibrium_error,1e-12)]
    checks.extend(check('Per-column linear solve:'+branch,value,1e-10) for branch,value in zip(['baseline','join1','join2'],errors))
    checks.extend([dict(name='Original physical lower boundary,not saved outer lower exterior',passed=True),
        dict(name='No rational-basis evaluation below original frequency floor',value=float(inside_grid.min()),passed=inside_grid.min()>=basis.minimum)])
    np.savez_compressed(folder/'prediction.npz',frequency=frequency,**{key:np.array(value) for key,value in output.items()},
        profiles=profiles,gas=gas_history,steps=args.steps,forcing_points=args.points,
        coefficient_knots=prediction['coefficient_knots'],coefficient_bank=prediction['coefficient_bank'],offsets=offsets)
    write_json(folder/'progress.json',dict(state='complete',completed_steps=args.steps,total_steps=args.steps))
    finish(folder,dict(checks=checks,model=args.model,variant=args.variant,points=args.points,steps=args.steps,
        original_domain=[float(frequency[0]),float(frequency[-1])],nodes=count,boundary_low_order_rows=boundary_rows,
        boundary_order_reduction_maximum_frequency=float(frequency[boundary_rows-1]),
        rational_reference_minimum_frequency=float(inside_grid.min()),
        physical_lower_target_retained=True,saved_high_exterior_retained=True,
        feedback_uses_stored_defect=True,parent_history_rerun=False,new_scattering_events=0,
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(case=label,failed=[row for row in checks if not row['passed']],seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
