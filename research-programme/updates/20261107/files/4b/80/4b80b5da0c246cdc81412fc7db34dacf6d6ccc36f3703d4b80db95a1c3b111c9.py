from spatial_defect_common import *
import argparse
import time
import hashlib


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    parser.add_argument('--max-sites',type=int,default=33)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'operator-m{int(args.upper*1000)}'
    folder.mkdir(parents=True,exist_ok=True)
    if (folder/'COMPLETE').exists():
        print(json.dumps(dict(reused=str(folder))),flush=True)
        return
    preflight=local_packet(ROOT/'results/preflight')
    assert preflight['all_checks_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    grid_path=PARENT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    coefficient_path=PARENT/'results/balanced-coefficients/bank.npz'
    grid,coefficients=map(read_npz,[grid_path,coefficient_path])
    spacing=float(coefficients['spacing'])
    factor=linalg.cholesky(basis.mass,lower=True)
    paths=event_paths()
    inputs=[grid_path,coefficient_path,*paths,*ladder.inputs,ROOT/'results/preflight/status.json']
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    fingerprint={str(path):digest(path) for path in [*inputs,Path(__file__).resolve(),ROOT/'spatial_defect_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']}
    fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
    if (folder/'INPUTS.json').exists():
        assert json.loads((folder/'INPUTS.json').read_text())==fingerprint
    else:
        write_json(folder/'INPUTS.json',fingerprint)
    records=[]
    completed=0
    for index,path in enumerate(paths):
        archive=folder/f'epoch-{index:02d}.npz'
        record_path=archive.with_suffix('.json')
        if record_path.exists():
            record=json.loads(record_path.read_text())
            assert record['fingerprint_sha256']==fingerprint_hash and record['archive_sha256']==digest(archive)
            records.append(record)
            continue
        event=read_npz(path)
        operators,diagnostics=event_defects(basis,grid['frequency'],grid['weights'],event['ratios'],event['rates'],spacing)
        scale=float(coefficients['normalization'][index])
        physical,second,third=[operators[key] for key in ['physical','second','third']]
        unnormalised=grid['source'][index]/scale
        second_corrected=unnormalised-second
        third_corrected=second_corrected-third
        values=dict(physical=physical,second=second,third=third,corrected2=second_corrected,corrected3=third_corrected,
            grid=grid['source'][index],inherited_physical=grid['physical'][index])
        physical_norm=max(float(linalg.norm(linalg.solve_triangular(factor,physical,lower=True))),1e-300)
        old_error_norm=max(float(linalg.norm(linalg.solve_triangular(factor,grid['source'][index]-physical,lower=True))),1e-300)
        comparisons={}
        checks=[]
        for label in ['physical','second','third']:
            checks.extend([check(f'Raw energy:{label}:{index}',diagnostics[label+'_raw_energy_error'],1e-8),
                check(f'Raw number:{label}:{index}',diagnostics[label+'_raw_number_error'],1e-8)])
        checks.extend([check(f'Exact deposition bias:{index}',diagnostics['bias_identity'],1e-10),
            dict(name=f'Nonnegative variance:{index}',passed=diagnostics['minimum_variance']>=0)])
        for label in ['corrected2','corrected3']:
            residual=float(linalg.norm(linalg.solve_triangular(factor,values[label]-physical,lower=True)))
            comparisons[label]=dict(weak_relative=residual/physical_norm,remaining_grid_error=residual/old_error_norm)
            checks.extend([check(f'Sensitivity1percent:weak:{label}:{index}',residual/physical_norm,.01),
                check(f'Explained90percent:weak:{label}:{index}',residual/old_error_norm,.1)])
        same_order=float(linalg.norm(linalg.solve_triangular(factor,physical-grid['physical'][index],lower=True)))/physical_norm
        if args.upper==.02:
            checks.append(check(f'Physical source matched-order reproduction:{index}',same_order,1e-8))
        physical_eigen=diagnostics['physical_eigen']
        predicted2=coefficients['eigenvalue'][index]/scale-diagnostics['second_eigen']
        for label,expected_eigen in [('corrected2',predicted2),('corrected3',physical_eigen)]:
            expected=grid['weights']*grid['frequency']*expected_eigen/I3
            moment_error=float(np.linalg.norm(basis.temperature@values[label]-expected)/np.linalg.norm(expected))
            checks.append(check(f'Derived energy row:{label}:{index}',moment_error,1e-10))
            comparisons[label]['energy_defect_over_physical']=(expected_eigen-physical_eigen)/physical_eigen
        np.savez_compressed(archive,**values,index=index,coordinate=grid['coordinate'][index],normalization=scale)
        record=dict(index=index,archive=archive.name,archive_sha256=digest(archive),fingerprint_sha256=fingerprint_hash,
            diagnostics=diagnostics,comparisons=comparisons,reference_difference=same_order,checks=checks)
        write_json(record_path,record)
        records.append(record)
        completed+=1
        write_json(folder/'progress.json',dict(state='running',completed_sites=len(records),total_sites=33,seconds=time.monotonic()-started))
        print(json.dumps(dict(upper=args.upper,index=index,seconds=time.monotonic()-started,comparisons=comparisons)),flush=True)
        if completed>=args.max_sites:
            break
        deadline=os.environ.get('MTS_DEADLINE_UTC')
        if deadline and datetime.now(timezone.utc)>=datetime.fromisoformat(deadline):
            print('Safe temperature checkpoint;remaining sites pending',flush=True)
            return
    if len(records)<33:
        print(json.dumps(dict(state='checkpointed',completed_sites=len(records),total_sites=33)),flush=True)
        return
    rows=[read_npz(folder/record['archive']) for record in records]
    np.savez_compressed(folder/'bank.npz',frequency=grid['frequency'],weights=grid['weights'],coordinate=grid['coordinate'],
        **{key:np.array([row[key] for row in rows]) for key in ['physical','second','third','corrected2','corrected3','grid','inherited_physical']})
    checks=[check_row for row in records for check_row in row['checks']]
    assert all(row['passed'] for row in checks if not row['name'].startswith(('Sensitivity1percent:','Explained90percent:'))),[row for row in checks if not row['passed']]
    finish(folder,dict(checks=checks,rows=records,upper=args.upper,matched_event_order=6,
        inherited_event_order=8 if args.upper==.04 else 6,new_physical_temperature_integrals=0,
        fixed_frequency_grid=True,correction_uses_measured_reference_difference=False,
        seconds=time.monotonic()-started),__file__,[*inputs,folder/'INPUTS.json'])
    print(json.dumps(dict(state='complete',upper=args.upper,checks=len(checks),failures=sum(not row['passed'] for row in checks))),flush=True)


if __name__=='__main__':
    main()
