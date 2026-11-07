from overlap_common import *
from solve_balanced_overlap import high_stencils


def main():
    modest()
    folder=ROOT/'results/background-scattering'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,ROOT/'WELL-BALANCED-EXTENSION.md']
    histories=[read_prediction(model,'fine') for model in ['heavy','cold']]
    for history in histories:
        inputs.extend(history[3])
    profiles=np.concatenate([history[1] for history in histories],axis=2)
    gas=np.concatenate([history[2] for history in histories],axis=1)
    checks,rows=[],[]
    for variant in ['space','fine']:
        prediction,unused_profiles,unused_gas,dependencies=read_prediction('heavy',variant)
        inputs.extend(dependencies)
        grid=prediction['frequency']
        spacing=float(np.log(grid[1]/grid[0]))
        locations=np.searchsorted(grid,[.011,.018,.027,.039])
        points=grid[locations]
        margin=int(max(abs(prediction['offsets'])))+4
        for epoch in [0,32,64]:
            path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'/f'epoch-{epoch:02d}.npz'
            inputs.append(path)
            events=read_npz(path)
            ratios,rates=events['ratios'],events['rates']
            central=basis.evaluate(points)
            profile=profiles[epoch]
            exact=np.zeros((len(points),6))
            for begin in range(0,len(ratios),64):
                ratio=ratios[begin:begin+64]
                shifted=ratio[:,None]*points
                differences=basis.evaluate(shifted.ravel()).reshape(len(ratio),len(points),basis.count)-central
                differences[:,:,0]=0.
                differences[:,:,1]=points[None,:]*(ratio[:,None]-1)/basis.norms[1]
                delta=np.einsum('efi,ik->efk',differences,profile)-points[None,:,None]*(ratio[:,None,None]-1)*gas[epoch]
                exact+=np.einsum('e,efk->fk',rates[begin:begin+64]/ratio,delta)/points[:,None]
            approximations={}
            for count in [2,4,6]:
                offsets,bank,chemical,weights=high_stencils([events],spacing,count,margin)
                shifted=points[:,None]*np.exp(offsets[None,:]*spacing)
                slope=np.einsum('fsi,ik->fsk',basis.evaluate(shifted),profile)/shifted[:,:,None]
                centre=(central@profile)/points[:,None]
                transport=np.einsum('s,fsk->fk',bank[0],slope-centre[:,None,:])
                eigenvalue=float(rates@(-np.expm1(-np.log(ratios))))
                approximations[count]=transport+eigenvalue*(centre-gas[epoch])
            lower_error=np.max(abs(approximations[2]-exact),axis=0)
            fourth_error=np.max(abs(approximations[4]-exact),axis=0)
            sixth_error=np.max(abs(approximations[6]-exact),axis=0)
            scale=np.maximum(lower_error,1e-300)
            checks.append(check(f'Six-point improves background scattering:{variant}:e{epoch}',
                np.max(sixth_error/scale),1.))
            rows.append(dict(variant=variant,epoch=epoch,frequency=points.tolist(),
                physical_compton=exact.tolist(),two_point_error=lower_error.tolist(),
                four_point_error=fourth_error.tolist(),six_point_error=sixth_error.tolist(),
                four_over_two=(fourth_error/scale).tolist(),six_over_two=(sixth_error/scale).tolist(),
                column_labels=['heavy baseline','heavy join1','heavy join2','cold baseline','cold join1','cold join2']))
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,exact_physical_shift_spot_check=True,
        no_shift_deposition_in_reference=True,new_thermal_events=0,
        whole_operator_error_bound=False),__file__,inputs)
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']],
        worst_four_over_two=max(max(row['four_over_two']) for row in rows),
        worst_six_over_two=max(max(row['six_over_two']) for row in rows))),flush=True)


if __name__=='__main__':
    main()
