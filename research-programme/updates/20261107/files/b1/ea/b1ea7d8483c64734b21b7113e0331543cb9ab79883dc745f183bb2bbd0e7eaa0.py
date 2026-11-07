from cubic_inner_common import *


def main():
    modest()
    folder=ROOT/'results/boundary-contract'
    folder.mkdir(parents=True,exist_ok=False)
    bank_path=ROOT/'results/coefficients/bank.npz'
    bank=read_npz(bank_path)
    offsets,spacing=bank['offsets'],float(bank['spacing'])
    margin=int(max(abs(offsets)))
    count=263
    extended=np.exp(spacing*np.arange(-margin,count+margin))
    frequency=extended[margin:margin+count]
    field=np.exp(-.4*extended)*np.cos(2*np.log(extended))
    test=1+.2*extended+np.sin(3*np.log(extended))
    window=np.exp(-((np.log(extended)-.21)/.13)**4)
    interior=field[margin:margin+count]
    test_inside=test[margin:margin+count]
    window_inside=window[margin:margin+count]
    measure=frequency**2*spacing
    checks,rows=[],[]
    for index in [0,8,16,24,32]:
        stencil=bank['stencil'][index]
        eigen=float(bank['eigenvalue'][index])
        generator=sparse.diags(stencil,offsets,shape=(count,count),format='csc')+eigen*sparse.eye(count,format='csc')
        weak=stencil*np.exp(-offsets*spacing)
        weak[offsets==0]+=eigen
        weak_matrix=sparse.diags(weak,offsets,shape=(count,count),format='csc')
        full=eigen*interior.copy()
        full_window=eigen*window_inside*interior
        inflow=np.zeros(count)
        commutator=np.zeros(count)
        for offset,coefficient in zip(offsets,stencil):
            shifted=field[margin+offset:margin+offset+count]
            shifted_window=window[margin+offset:margin+offset+count]
            full+=coefficient*shifted
            full_window+=coefficient*shifted_window*shifted
            commutator+=coefficient*(shifted_window-window_inside)*shifted
            if offset<0:
                inflow[:-offset]+=coefficient*field[margin+offset:margin]
            elif offset>0:
                inflow[-offset:]+=coefficient*field[margin+count:margin+count+offset]
        reconstruction=generator@interior+inflow
        scale=max(float(np.max(abs(stencil)))*float(np.max(abs(field))),1e-300)
        boundary_error=float(np.max(abs(full-reconstruction))/scale)
        commutator_error=float(np.max(abs(full_window-window_inside*full-commutator))/scale)
        left=float(np.sum(measure*test_inside*full))
        restricted=float(np.sum(measure*(weak_matrix@test_inside)*interior))
        edge=float(np.sum(measure*test_inside*inflow))
        dual_error=abs(left-restricted-edge)/max(abs(left)+abs(restricted)+abs(edge),1e-300)
        checks.extend([check(f'Explicit ghost reconstruction:{index}',boundary_error,1e-12),
            check(f'Matching-window commutator:{index}',commutator_error,1e-12),
            check(f'Finite adjoint plus boundary work:{index}',dual_error,1e-12)])
        rows.append(dict(index=index,boundary_error=boundary_error,window_error=commutator_error,
            adjoint_error=dual_error,left=left,restricted=restricted,boundary_work=edge,
            missing_edge_absolute_error=abs(left-restricted)))
    assert all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,rows=rows,physical_boundaries_not_assumed_silent=True,
        projection_scope='Same continuous shift kernel;feedback basis/quadrature and finite inner nodes are different representations,not a bitwise-identical projection.'),
        __file__,[bank_path,bank_path.parent/'status.json'])
    print(json.dumps(dict(checks=len(checks),max_boundary_error=max(row['boundary_error'] for row in rows),
        max_window_error=max(row['window_error'] for row in rows))),flush=True)


if __name__=='__main__':
    main()
