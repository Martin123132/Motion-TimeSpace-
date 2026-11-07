from overlap_common import *
from measure_overlap import evaluate
import argparse
import time


def high_stencils(events,spacing,points,margin):
    offsets=np.arange(-margin,margin+1)
    bank=[]
    moment_error,weight_error=0.,0.
    for saved in events:
        ratio,rates=saved['ratios'],saved['rates']
        shift=np.log(ratio)/spacing
        first=np.floor(shift).astype(int)-(points//2-1)
        locations=first[:,None]+np.arange(points)
        relative=locations-first[:,None]
        nodes=np.exp(-relative*spacing)
        target=np.exp(-(shift-first)*spacing)
        weights=np.ones_like(nodes)
        for column in range(points):
            for other in range(points):
                if column!=other:
                    weights[:,column]*=(target-nodes[:,other])/(nodes[:,column]-nodes[:,other])
        weight_error=max(weight_error,float(np.max(abs(weights.sum(axis=1)-1))))
        values=np.zeros(len(offsets))
        assert locations.min()>=-margin and locations.max()<=margin
        np.add.at(values,(locations+margin).ravel(),(rates[:,None]*weights).ravel())
        values[margin]=0.
        values[margin]=-values.sum()
        eigenvalue=float(rates@(-np.expm1(-np.log(ratio))))
        chemical=float(values@np.expm1(-offsets*spacing)+eigenvalue)
        moment_error=max(moment_error,abs(chemical)/max(abs(eigenvalue),1e-300))
        bank.append(values)
    return offsets,np.array(bank),moment_error,weight_error


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--variant',choices=['fine','space'],default='fine')
    parser.add_argument('--points',type=int,choices=[4,6],default=4)
    parser.add_argument('--steps',type=int,choices=[5120,10240],default=5120)
    args=parser.parse_args()
    modest()
    label=f'balanced-{args.model}-{args.variant}-p{args.points}-n{args.steps}'
    folder=ROOT/'results'/label
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prediction,unused_profiles,unused_gas,inputs=read_prediction(args.model,args.variant)
    baseline,window,history_inputs=load_histories(args.model)
    inputs.extend([*ladder.inputs,*history_inputs,ROOT/'WELL-BALANCED-EXTENSION.md'])
    events=[]
    for epoch in range(65):
        path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'/f'epoch-{epoch:02d}.npz'
        inputs.append(path)
        events.append(read_npz(path))
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    original=prediction['frequency']
    begin=int(np.searchsorted(original,.0025))
    frequency=original[begin:]
    spacing=float(np.log(original[1]/original[0]))
    offsets=prediction['offsets']
    low_margin=int(max(-offsets[0],offsets[-1]))
    margin=low_margin+4
    count=len(frequency)
    all_grid=original[0]*np.exp(spacing*np.arange(begin-margin,len(original)+margin))
    driver,normalization=make_drivers(basis,baseline,window,all_grid,.1)
    high_offsets,high_bank,chemical,weights=high_stencils(events,spacing,args.points,margin)
    high_at=interpolate.interp1d(prediction['coordinate'],high_bank,axis=0,bounds_error=True)
    coefficients=prediction['coefficient_bank']
    prefix=len(offsets)+3
    retained=np.c_[coefficients[:,:prefix],coefficients[:,prefix+begin+low_margin:prefix+len(original)+low_margin]]
    bank=interpolate.interp1d(prediction['coefficient_knots'],retained,axis=0,bounds_error=True)
    start,end=prediction['coordinate'][[0,-1]]
    step=(end-start)/args.steps
    old_outer=driver(float(start))[2+margin:2+margin+count,:3]
    older_outer=old_outer.copy()
    error=np.zeros_like(old_outer)
    previous_error=error.copy()
    output=dict(coordinate=[start],slope=[old_outer.copy()],outer_slope=[old_outer.copy()],defect_correction=[error.copy()])
    identity=sparse.eye(count,format='csc')
    errors=np.zeros(3)
    maximum_state=np.zeros(3)
    started=time.monotonic()
    for index in range(1,args.steps+1):
        coordinate=float(start+(end-start)*index/args.steps)
        values=bank(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):prefix]
        br=values[prefix:]
        dc=dc_constant/frequency**2
        drives=driver(coordinate)[:,:3]
        gas,hard=drives[0],drives[1]
        all_outer=drives[2:]
        outer=all_outer[margin:margin+count]
        transport=np.zeros_like(outer)
        for offset,coefficient in zip(high_offsets,high_at(coordinate)):
            if offset and coefficient:
                transport+=coefficient*(all_outer[margin+offset:margin+offset+count]-outer)
        source=clock_rate*(transport+eigenvalue*(outer-gas)+dc[:,None]*(hard-outer)+br[:,None]*(gas-outer))
        internal=split_matrix(stencil,offsets,count)[0]
        generator=clock_rate*(internal+sparse.diags(eigenvalue-dc-br,format='csc'))
        leading,previous,older=(1.,-1.,0.) if index==1 else (1.5,-2.,.5)
        matrix=leading*identity-step*generator
        right=-previous*error-older*previous_error+step*source-(leading*outer+previous*old_outer+older*older_outer)
        updated=sparse_linalg.splu(matrix).solve(right)
        scale=np.maximum(np.max(abs(matrix)@abs(updated)+abs(right),axis=0),1e-300)
        errors=np.maximum(errors,np.max(abs(matrix@updated-right),axis=0)/scale)
        previous_error,error=error,updated
        older_outer,old_outer=old_outer,outer
        maximum_state=np.maximum(maximum_state,np.max(abs(error),axis=0))
        if index%(args.steps//64)==0:
            for key,value in [('coordinate',coordinate),('slope',outer+error),('outer_slope',outer),('defect_correction',error)]:
                output[key].append(np.array(value).copy())
        if index%(args.steps//2)==0:
            print(json.dumps(dict(case=label,step=index,total=args.steps,seconds=time.monotonic()-started)),flush=True)
    checks=[check('High-order chemical invariant',chemical,1e-9),check('High-order constant invariant',weights,1e-12)]
    checks.extend(check('BDF solve:'+branch,value,1e-10) for branch,value in zip(['baseline','join1','join2'],errors))
    np.savez_compressed(folder/'overlap.npz',frequency=frequency,**{key:np.array(value) for key,value in output.items()},
        steps=args.steps,forcing_points=args.points,high_offsets=high_offsets,high_stencils=high_bank)
    fine,profiles,unused,dependencies=read_prediction(args.model,'fine')
    inputs.extend(dependencies)
    outputs,local_checks,rows=evaluate(folder,basis,fine,profiles)
    checks.extend(local_checks)
    np.savez_compressed(folder/'readout.npz',**outputs)
    finish(folder,dict(checks=checks,rows=rows,model=args.model,variant=args.variant,points=args.points,steps=args.steps,
        discretization='BDF2 after one BE start;positive low-order operator on defect;higher-order known background forcing',
        positive_BE_envelope_claim=False,small_defect_only_evolved=True,
        future_inner_spectrum_used_as_driver=False,physical_coefficients_fitted=False,
        full_frequency_matching_complete=False,new_scattering_events=0,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(case=label,rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
