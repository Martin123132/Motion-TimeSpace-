from coefficient_common import *


def main():
    modest()
    folder=ROOT/'results/balanced-coefficients'
    folder.mkdir(parents=True,exist_ok=False)
    old_path=ROOT/'results/coefficients/bank.npz'
    bank=read_npz(old_path)
    prior=local_packet(old_path.parent)
    assert prior['temporal_replay_permitted']
    offsets,low,spacing=bank['offsets'],bank['low'],float(bank['spacing'])
    center=int(np.flatnonzero(offsets==0)[0])
    positive=offsets>0
    ratios=np.exp(offsets[positive]*spacing)
    repaired=[]
    checks,rows=[],[]
    for index,values in enumerate(low):
        pair_total=values[positive]+values[:center][::-1]
        forward=pair_total/(1+ratios**-3)
        backward=forward/ratios**3
        eigen_before=float(np.sum(forward*(ratios-1)**2*(ratios+1)/ratios**3))
        eigen=float(bank['eigenvalue'][index])
        scale=eigen/eigen_before
        result=np.zeros_like(values)
        result[positive]=scale*forward
        result[:center]=(scale*backward)[::-1]
        result[center]=-result.sum()
        chemical=float(result@np.expm1(-offsets*spacing)+eigen)
        number=float(result@np.expm1(-2*offsets*spacing)+eigen)
        energy=float(result@np.expm1(-3*offsets*spacing))
        reciprocal=np.max(abs(result[:center][::-1]-result[positive]/ratios**3))/max(np.max(result[positive]),1e-300)
        checks.extend([dict(name='Positive repair:'+str(index),passed=bool(np.all(result[np.arange(len(result))!=center]>=0) and scale>0)),
            check(f'Chemical:{index}',abs(chemical)/eigen,1e-9),
            check(f'Number:{index}',abs(number)/eigen,1e-9),
            check(f'Energy:{index}',abs(energy)/eigen,1e-9),
            check(f'Constant:{index}',abs(result.sum()),1e-12),
            check(f'Pair reciprocity:{index}',reciprocal,1e-14)])
        count=5265
        generator=sparse.diags(result,offsets,shape=(count,count),format='csr')+eigen*sparse.eye(count,format='csr')
        chemical_vector=np.exp(-np.arange(count)*spacing)
        weighted_rows=(generator@chemical_vector)/chemical_vector
        positive_error=float(max(0,np.max(weighted_rows))/eigen)
        checks.append(check(f'Restricted chemical subinvariance:{index}',positive_error,1e-9))
        rows.append(dict(index=index,scale=scale,eigenvalue=eigen,unscaled_eigenvalue=eigen_before,
            rate_change_l1_relative=float(np.sum(abs(result-values))/np.sum(abs(values))),
            chemical_residual=chemical/eigen,number_residual=number/eigen,energy_residual=energy/eigen,
            maximum_restricted_weighted_row=float(np.max(weighted_rows))))
        repaired.append(result)
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    np.savez_compressed(folder/'bank.npz',**{key:value for key,value in bank.items() if key!='low'},
        low=np.array(repaired),unrepaired_low=low,normalization=np.array([row['scale'] for row in rows]))
    finish(folder,dict(checks=checks,rows=rows,bulk_moment_contracts_pass=True,
        new_physics_or_fit=False,positive_aggregate_repair=True,pointwise_jump_rule_unchanged=False,
        boundary_flux_certificate=False),__file__,[old_path,old_path.parent/'status.json',ROOT/'DISCRETE-BALANCE-REPAIR.md'])
    print(json.dumps(dict(checks=len(checks),all_pass=True,
        scale_range=[min(row['scale'] for row in rows),max(row['scale'] for row in rows)],
        rate_change_range=[min(row['rate_change_l1_relative'] for row in rows),max(row['rate_change_l1_relative'] for row in rows)],
        maximum_moment_residual=max(max(abs(row[key]) for key in ['chemical_residual','number_residual','energy_residual']) for row in rows))),flush=True)


if __name__=='__main__':
    main()
