from overlap_common import *
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=['heavy','cold'],required=True)
    parser.add_argument('--lower',type=float,choices=[.0025,.005],default=.0025)
    parser.add_argument('--variant',choices=['fine','space'],default='fine')
    parser.add_argument('--steps',type=int,choices=[2560,5120],default=2560)
    args=parser.parse_args()
    modest()
    label=f'{args.model}-{args.variant}-lo{int(args.lower*10000)}-n{args.steps}'
    folder=ROOT/'results'/label
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prediction,unused_profiles,unused_gas,inputs=read_prediction(args.model,args.variant)
    baseline,window,history_inputs=load_histories(args.model)
    inputs.extend([*ladder.inputs,*history_inputs])
    for path in inputs:
        verify_source(path,chain)
    original=prediction['frequency']
    begin=int(np.searchsorted(original,args.lower))
    frequency=original[begin:]
    spacing=float(np.log(original[1]/original[0]))
    offsets=prediction['offsets']
    margin=int(max(-offsets[0],offsets[-1]))
    count=len(frequency)
    all_grid=original[0]*np.exp(spacing*np.arange(begin-margin,len(original)+margin))
    assert begin>margin and np.allclose(all_grid[margin:margin+count],frequency,rtol=1e-12)
    assert all_grid.min()>=basis.minimum and all_grid.max()<=basis.maximum
    driver,normalization=make_drivers(basis,baseline,window,all_grid,.1)
    coefficients=prediction['coefficient_bank']
    prefix=len(offsets)+3
    retained=np.c_[coefficients[:,:prefix],coefficients[:,prefix+begin:prefix+len(original)+2*margin]]
    assert retained.shape[1]==prefix+count+2*margin
    bank=interpolate.interp1d(prediction['coefficient_knots'],retained,axis=0,bounds_error=True)
    start,end=prediction['coordinate'][[0,-1]]
    step=(end-start)/args.steps
    initial=driver(float(start))[2+margin:2+margin+count,:3]
    direct=initial.copy()
    error=np.zeros_like(direct)
    envelope=np.zeros_like(direct)
    old_outer=initial.copy()
    identity=sparse.eye(count,format='csc')
    output=dict(coordinate=[],slope=[],outer_slope=[],defect_correction=[],envelope=[],residual=[])
    errors=dict(linear_solve=0.,equilibrium=0.,chemical=0.,offdiagonal_negative=0.,envelope_violation=0.)
    direct_gap=0.
    correction_scale=0.
    minimum_margin=1e300
    started=time.monotonic()
    for index in range(args.steps+1):
        coordinate=float(start+(end-start)*index/args.steps)
        values=bank(coordinate)
        stencil=values[:len(offsets)]
        eigenvalue,dc_constant,clock_rate=values[len(offsets):prefix]
        br=values[prefix:]
        dc=dc_constant/all_grid**2
        gamma=dc+br
        drives=driver(coordinate)[:,:3]
        gas,hard=drives[0],drives[1]
        outer_all=drives[2:]
        outer=outer_all[margin:margin+count]
        internal,lower_matrix,upper_matrix=split_matrix(stencil,offsets,count)
        local_gamma=gamma[margin:margin+count]
        generator=clock_rate*(internal+sparse.diags(eigenvalue-local_gamma,format='csc'))
        forcing=clock_rate*(dc[margin:margin+count,None]*hard+br[margin:margin+count,None]*gas-eigenvalue*gas
            +lower_matrix@outer_all[:margin]+upper_matrix@outer_all[margin+count:])
        row_sum=internal@np.ones(count)+lower_matrix@np.ones(margin)+upper_matrix@np.ones(margin)
        errors['equilibrium']=max(errors['equilibrium'],float(np.max(abs(row_sum))))
        chemical=stencil@np.exp(-offsets*spacing)+eigenvalue
        errors['chemical']=max(errors['chemical'],abs(float(chemical))/max(abs(float(eigenvalue)),1e-300))
        offdiagonal=internal-sparse.diags(internal.diagonal())
        errors['offdiagonal_negative']=max(errors['offdiagonal_negative'],float(max(0.,-offdiagonal.data.min(initial=0.))))
        matrix=identity-step*generator
        diagonal=matrix.diagonal()
        dominance=diagonal-(np.array(abs(matrix).sum(axis=1)).ravel()-abs(diagonal))
        minimum_margin=min(minimum_margin,float(dominance.min()))
        residual=np.zeros_like(outer)
        if index:
            residual=(outer-old_outer)/step-generator@outer-forcing
            right=np.column_stack([direct+step*forcing,error-step*residual,envelope+step*abs(residual)])
            factor=sparse_linalg.splu(matrix)
            updated=factor.solve(right)
            scale=max(float(np.max(abs(matrix)@abs(updated)+abs(right))),1e-300)
            errors['linear_solve']=max(errors['linear_solve'],float(np.max(abs(matrix@updated-right)))/scale)
            direct,error,envelope=np.split(updated,3,axis=1)
            direct_gap=max(direct_gap,float(np.max(abs(direct-(outer+error)))))
            correction_scale=max(correction_scale,float(np.max(abs(error))))
            env_scale=max(float(np.max(abs(envelope)+abs(error))),1e-300)
            errors['envelope_violation']=max(errors['envelope_violation'],float(np.max(np.maximum(abs(error)-envelope,0)))/env_scale)
        old_outer=outer.copy()
        if index%(args.steps//64)==0:
            for key,value in [('coordinate',coordinate),('slope',direct),('outer_slope',outer),
                              ('defect_correction',error),('envelope',envelope),('residual',residual)]:
                output[key].append(np.array(value).copy())
        if index%(args.steps//4)==0:
            print(json.dumps(dict(case=label,step=index,total=args.steps,seconds=time.monotonic()-started)),flush=True)
            write_json(folder/'progress.json',dict(state='running',steps_completed=index,total_steps=args.steps))
    checks=[check(key,value,1e-10) for key,value in errors.items()]
    equality=direct_gap/max(correction_scale,1e-300)
    checks.append(check('Direct vs defect-driven overlap on correction scale',equality,1e-8))
    checks.append(dict(name='Implicit positive-inverse margin',value=minimum_margin,passed=minimum_margin>0))
    np.savez_compressed(folder/'overlap.npz',frequency=frequency,**{key:np.array(value) for key,value in output.items()},
        steps=args.steps,lower_requested=args.lower,hard_floor=.1,hard_normalization=normalization)
    report=dict(checks=checks,model=args.model,variant=args.variant,steps=args.steps,requested_lower=args.lower,
        actual_domain=[float(frequency[0]),float(frequency[-1])],nodes=count,
        exterior_domain=[float(all_grid[0]),float(all_grid[-1])],initial_error_exact_zero=True,
        future_inner_spectrum_used_as_driver=False,driver_columns=['gas','hard_slope','outer_exterior'],
        common_soft_approximation=True,full_frequency_matching_complete=False,
        direct_defect_relative=equality,minimum_m_matrix_margin=minimum_margin,
        seconds=time.monotonic()-started)
    write_json(folder/'progress.json',dict(state='complete',steps_completed=args.steps,total_steps=args.steps))
    finish(folder,report,__file__,inputs)
    print(json.dumps(dict(case=label,failed=[row for row in checks if not row['passed']],seconds=report['seconds'])),flush=True)


if __name__=='__main__':
    main()
