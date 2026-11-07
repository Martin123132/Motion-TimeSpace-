from source_pair_common import *
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
    data=load_operator_inputs('heavy',args.upper,basis)
    candidate_path=ROOT/'results/balanced-coefficients/bank.npz'
    total_path=PARENT/'results/balanced-coefficients/bank.npz'
    raw_path=PARENT/'results/coefficients/bank.npz'
    candidate,total,raw=map(read_npz,[candidate_path,total_path,raw_path])
    active=candidate['offsets']!=0
    ratios=np.exp(candidate['offsets'][active]*float(candidate['spacing']))
    factor=linalg.cholesky(basis.mass,lower=True)
    inputs=[candidate_path,total_path,raw_path,*ladder.inputs,*data['inputs']]
    field={}
    for model in ['heavy','cold']:
        path=PARENT/'results'/f'replay-{model}-balanced/prediction.npz'
        replay=read_npz(path)
        field[model]=np.array([compact_defect(data['frequency'],replay['frequency'],value,args.upper) for value in replay['defect']])
        inputs.append(path)
    rows,checks=[],[]
    operators={label:[] for label in ['source','total']}
    for index in range(33):
        physical=data['operators'][index]
        physical_dual=linalg.solve_triangular(factor,physical,lower=True)
        row=dict(index=index,comparisons={})
        for label,bank in [('source',candidate),('total',total)]:
            action,moment,diagnostic=stable_adjoint(basis,data['frequency'],data['weights'],ratios,bank['low'][index,active])
            difference=action-physical
            dual=linalg.solve_triangular(factor,difference,lower=True)
            relative=float(np.linalg.norm(dual)/max(np.linalg.norm(physical_dual),1e-300))
            checks.extend([check(f'Bulk source energy:{label}:{index}',abs(moment-2*candidate['eigenvalue'][index])/(2*candidate['eigenvalue'][index]),1e-9),
                check(f'Unrepaired energy evaluation:{label}:{index}',diagnostic['raw_energy_error'],1e-8),
                check(f'Sensitivity1percent:weak:{label}:{index}',relative,.01)])
            action_rows={}
            for model,values in field.items():
                physical_value=physical_dual@values[index]
                delta=dual@values[index]
                scale=np.linalg.norm(physical_value,axis=0)
                rel=np.linalg.norm(delta,axis=0)/np.maximum(scale,1e-300)
                if not np.any(values[index]):
                    rel=np.zeros(3)
                action_rows[model]=rel.tolist()
                checks.extend(check(f'Sensitivity1percent:state:{label}:{model}:{index}:{column}',value,.01)
                    for column,value in zip(['baseline','join1','join2'],rel))
            row['comparisons'][label]=dict(weak_dual_frobenius_relative=relative,physical_state_action_relative=action_rows,
                raw_energy_error=diagnostic['raw_energy_error'],quadrature_basis_extrapolates=True)
            operators[label].append(action)
        rows.append(row)
        if index%8==0:
            print(json.dumps(dict(upper=args.upper,index=index,seconds=time.monotonic()-started)),flush=True)
    np.savez_compressed(folder/'bank.npz',frequency=data['frequency'],weights=data['weights'],coordinate=data['coordinate'],
        physical=data['operators'],source=np.array(operators['source']),total=np.array(operators['total']),
        physical_event_order=8 if args.upper==.04 else 6,inner_event_order=6)
    chain=ancestors()
    for path in inputs:
        if not path.is_relative_to(ROOT):
            verify_source(path,chain)
    assert all(row['passed'] for row in checks if not row['name'].startswith('Sensitivity1percent:'))
    finish(folder,dict(checks=checks,rows=rows,upper=args.upper,physical_reference='saved physical event weak matrices',
        baseline_and_mts=True,basis_count=96,quadrature_order_difference_explicit=args.upper==.04,
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(upper=args.upper,checks=len(checks),failures=sum(not row['passed'] for row in checks),
        max_weak_error={label:max(row['comparisons'][label]['weak_dual_frobenius_relative'] for row in rows) for label in operators})),flush=True)


if __name__=='__main__':
    main()
