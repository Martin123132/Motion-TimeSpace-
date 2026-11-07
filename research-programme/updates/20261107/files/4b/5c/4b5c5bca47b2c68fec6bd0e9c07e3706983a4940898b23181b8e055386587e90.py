from cubic_inner_common import *
import argparse
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'weak-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    prior_path=PARENT/'results'/f'operator-m{int(args.upper*1000)}/bank.npz'
    coefficient_path=ROOT/'results/coefficients/bank.npz'
    prior,bank=map(read_npz,[prior_path,coefficient_path])
    active=bank['offsets']!=0
    ratios=np.exp(bank['offsets'][active]*float(bank['spacing']))
    factor=linalg.cholesky(basis.mass,lower=True)
    operators,rows,checks=[],[],[]
    for index in range(33):
        action,moment,diagnostic=stable_adjoint(basis,prior['frequency'],prior['weights'],ratios,bank['stencil'][index,active])
        physical=prior['physical'][index]
        scale=max(float(linalg.norm(linalg.solve_triangular(factor,physical,lower=True))),1e-300)
        old=float(linalg.norm(linalg.solve_triangular(factor,prior['grid'][index]-physical,lower=True)))
        error=float(linalg.norm(linalg.solve_triangular(factor,action-physical,lower=True)))
        taylor=float(linalg.norm(linalg.solve_triangular(factor,action-prior['corrected3'][index],lower=True)))
        checks.extend([check(f'Unscaled source energy:{index}',abs(moment-2*bank['eigenvalue'][index])/(2*bank['eigenvalue'][index]),1e-9),
            check(f'Raw energy evaluation:{index}',diagnostic['raw_energy_error'],1e-8),
            check(f'Sensitivity1percent:weak:{index}',error/scale,.01),
            check(f'Explained90percent:weak:{index}',error/max(old,1e-300),.1)])
        rows.append(dict(index=index,weak_relative=error/scale,remaining_grid_error=error/max(old,1e-300),
            discrete_versus_continuum_taylor_relative=taylor/scale,raw_energy_error=diagnostic['raw_energy_error']))
        operators.append(action)
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Sensitivity1percent:','Explained90percent:')))
    np.savez_compressed(folder/'bank.npz',frequency=prior['frequency'],weights=prior['weights'],coordinate=prior['coordinate'],
        cubic=np.array(operators),physical=prior['physical'],continuum_taylor=prior['corrected3'])
    inputs=[prior_path,prior_path.parent/'status.json',coefficient_path,coefficient_path.parent/'status.json',*ladder.inputs]
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,upper=args.upper,positive_probability_interpretation=False,
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(upper=args.upper,weak_error=max(row['weak_relative'] for row in rows),
        remaining=max(row['remaining_grid_error'] for row in rows),seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
