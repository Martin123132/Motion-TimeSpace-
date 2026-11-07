from cubic_inner_common import *
from fractions import Fraction
import time


def exact_checks():
    checks=[]
    nodes=[Fraction(3,4),Fraction(7,8),Fraction(9,8),Fraction(5,4)]
    center=Fraction(17,16)
    left,right=nodes[1:3]
    probability=(right-center)/(right-left)
    variance=(right-center)*(center-left)
    third=variance*(right+left-2*center)
    for power in range(4):
        lagrange=[]
        for column in range(4):
            value=Fraction(1)
            for other in range(4):
                if column!=other:
                    value*=(center-nodes[other])/(nodes[column]-nodes[other])
            lagrange.append(value)
        actual=sum(weight*node**power for weight,node in zip(lagrange,nodes))
        second=Fraction(power*(power-1))*center**(power-2) if power>=2 else Fraction(0)
        third_derivative=Fraction(power*(power-1)*(power-2))*center**(power-3) if power>=3 else Fraction(0)
        positive=probability*left**power+(1-probability)*right**power
        checks.append(dict(name=f'Exact cubic reproduction:{power}',passed=actual==center**power))
        checks.append(dict(name=f'Exact discrete variance/skewness identity:{power}',passed=positive-actual==variance*second/2+third*third_derivative/6))
    for current,previous,older in [(Fraction(3,7),Fraction(-4,11),Fraction(5,13)),(Fraction(-1),Fraction(2),Fraction(3))]:
        left=current*(Fraction(3,2)*current-2*previous+older/2)
        right=(current**2+(2*current-previous)**2-previous**2-(2*previous-older)**2+(current-2*previous+older)**2)/4
        checks.append(dict(name='Exact BDF2 norm identity:'+str(current),passed=left==right))
    return checks


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/coefficients'
    folder.mkdir(parents=True,exist_ok=False)
    prior_path=P129/'results/coefficients/bank.npz'
    prior=read_npz(prior_path)
    offsets,spacing=prior['offsets'],float(prior['spacing'])
    nonzero=offsets!=0
    center=int(np.flatnonzero(offsets==0)[0])
    checks=exact_checks()
    rows,stencils,raws,eigenvalues=[],[],[],[]
    paths=event_paths()
    for index,path in enumerate(paths):
        event=read_npz(path)
        ratios,rates=event['ratios'],event['rates']
        raw,weights,errors=deposit_cubic(ratios,rates,offsets,spacing)
        candidate=pair_cubic(raw,offsets,spacing)
        inverse=1/ratios
        eigen=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3)/2)
        discrete_eigen=float(np.sum(raw*(np.exp(offsets*spacing)-1)**2*(np.exp(offsets*spacing)+1)/np.exp(offsets*spacing)**3)/2)
        powers=np.array([-1.,-2.,-3.,0.])
        moments=np.sum(candidate[nonzero,None]*np.expm1(offsets[nonzero,None]*spacing*powers),axis=0)+eigen
        expected=np.array([0.,0.,eigen,eigen])
        moment_error=float(np.max(abs(moments-expected))/eigen)
        bound=symbol_bound(candidate,offsets,spacing,eigen)
        raw_check=prior['high'][index,4:-4].copy()
        raw_check[center]=raw[center]
        checks.extend([check(f'Cubic monomials:{index}',max(errors),1e-12),
            check(f'Independent prior cubic deposition:{index}',np.max(abs(raw-raw_check))/max(np.max(abs(raw)),1e-300),1e-10),
            check(f'Physical eigen unchanged:{index}',abs(eigen-prior['eigenvalue'][index])/eigen,1e-8),
            check(f'Unscaled cubic eigen:{index}',abs(discrete_eigen-eigen)/eigen,1e-9),
            check(f'Inner moment contracts:{index}',moment_error,1e-9),
            dict(name=f'All-frequency finite-grid dissipativity:{index}',passed=bound['upper_bound']<0,value=bound['upper_bound']),
            check(f'Reciprocity:{index}',np.max(abs(candidate[:center][::-1]-candidate[center+1:]/np.exp(offsets[center+1:]*spacing)**3)),1e-14)])
        matrix=sparse.diags(candidate,offsets,shape=(197,197),format='csc')+eigen*sparse.eye(197,format='csc')
        frequency=np.exp(spacing*np.arange(197))
        similarity=sparse.diags(frequency**1.5)@matrix@sparse.diags(frequency**-1.5)
        eigmax=float(linalg.eigvalsh(similarity.toarray(),subset_by_index=[196,196])[0])
        checks.append(dict(name=f'Independent finite matrix below bound:{index}',passed=eigmax<=bound['upper_bound']+1e-12,value=eigmax))
        weak=candidate*np.exp(-offsets*spacing)
        weak[center]=candidate[center]+eigen
        adjoint=sparse.diags(weak,offsets,shape=(197,197),format='csc')
        pairing=sparse.diags(frequency**2)@matrix-adjoint.T@sparse.diags(frequency**2)
        adjoint_error=float(np.max(abs(pairing.data))) if pairing.nnz else 0.
        checks.append(check(f'Finite restricted weighted adjoint:{index}',adjoint_error,1e-12))
        rows.append(dict(index=index,eigenvalue=eigen,moment_error=moment_error,bound=bound,
            negative_event_weights=int(np.count_nonzero(weights<0)),
            negative_offdiagonal_coefficients=int(np.count_nonzero(candidate[nonzero]<0)),
            negative_rate_l1_fraction=float(np.sum(abs(candidate[nonzero][candidate[nonzero]<0]))/np.sum(abs(candidate[nonzero]))),
            finite_matrix_max_eigenvalue=eigmax,adjoint_error=adjoint_error))
        stencils.append(candidate)
        raws.append(raw)
        eigenvalues.append(eigen)
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    np.savez_compressed(folder/'bank.npz',coordinate=prior['coordinate'],temperature=prior['temperature'],
        offsets=offsets,spacing=spacing,stencil=np.array(stencils),raw=np.array(raws),eigenvalue=np.array(eigenvalues))
    chain=ancestors()
    inputs=[prior_path,prior_path.parent/'status.json',*paths]
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,normalization_fitted=False,normalization_applied=False,
        stability_scope='All finite principal truncations;analytic symbol remainder plus conservative floating allowance,not formal interval certificate.',
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),upper_max=max(row['bound']['upper_bound'] for row in rows),
        max_negative_rates=max(row['negative_offdiagonal_coefficients'] for row in rows),
        max_moment_error=max(row['moment_error'] for row in rows))),flush=True)


if __name__=='__main__':
    main()
