from source_pair_common import *


def main():
    modest()
    folder=ROOT/'results/finite-adjoint'
    folder.mkdir(parents=True,exist_ok=False)
    bank_path=ROOT/'results/balanced-coefficients/bank.npz'
    bank=read_npz(bank_path)
    offsets,spacing=bank['offsets'],float(bank['spacing'])
    checks,rows,inputs=[],[],[bank_path]
    for model in ['heavy','cold']:
        path=ROOT/'results'/f'replay-{model}-balanced/prediction.npz'
        replay=read_npz(path)
        inputs.append(path)
        frequency=replay['frequency']
        weight=spacing*frequency**2
        count=len(frequency)
        grid_index=np.arange(count)
        for epoch in [0,16,32]:
            values=bank['low'][epoch]
            eigen=float(bank['eigenvalue'][epoch])
            generator=sparse.diags(values,offsets,shape=(count,count),format='csr')+eigen*sparse.eye(count,format='csr')
            defect=replay['defect'][epoch]
            for power in [0.,1.,.3+2j]:
                test=frequency**power
                bulk=symbol(offsets*spacing,values,np.array([-power-2]),eigen)[0]*test
                lost=np.zeros(count,dtype=complex)
                for offset,coefficient in zip(offsets,values):
                    if offset==0 or coefficient==0:
                        continue
                    outside=(grid_index-offset<0)|(grid_index-offset>=count)
                    lost[outside]+=coefficient*np.exp(-(power+2)*offset*spacing)*test[outside]
                adjoint=(generator.T@(weight*test))/weight
                row_scale=max(np.max(abs(bulk)+abs(lost)),eigen*np.max(abs(test)),1e-300)
                error=float(np.max(abs(adjoint-(bulk-lost)))/row_scale)
                lhs=(weight*test)@(generator@defect)
                bulk_integral=(weight*bulk)@defect
                boundary=(weight*lost)@defect
                expected=bulk_integral-boundary
                absolute_scale=(weight*abs(test))@(abs(generator)@abs(defect))+abs(bulk_integral)+abs(boundary)
                relative=np.max(abs(lhs-expected)/np.maximum(absolute_scale,1e-300))
                name=f'{model}:{epoch}:{power}'
                checks.extend([check('Weighted adjoint:'+name,error,1e-9),check('Finite boundary identity:'+name,relative,1e-9)])
                rows.append(dict(model=model,epoch=epoch,power=str(power),adjoint_error=error,identity_error=float(relative),
                    lhs_real=lhs.real.tolist(),lhs_imag=lhs.imag.tolist(),bulk_real=bulk_integral.real.tolist(),
                    boundary_real=boundary.real.tolist(),boundary_imag=boundary.imag.tolist(),
                    physical_inflow_included=False))
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,rows=rows,finite_grid_identity_verified=True,full_evolution_flux_budget=False,
        scope='Restricted Compton generator on saved defects;physical boundary inflow and DC/BR remain separate.'),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),max_residual=max(row['value'] for row in checks))),flush=True)


if __name__=='__main__':
    main()
