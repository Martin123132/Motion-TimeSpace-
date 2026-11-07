from carry_common import *
import argparse
import hashlib
import time


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--upper',type=float,choices=[.02,.04],required=True)
    args=parser.parse_args()
    modest()
    started=time.monotonic()
    folder=ROOT/'results'/f'weak-m{int(args.upper*1000)}'
    if (folder/'COMPLETE').exists():
        print(json.dumps(dict(reused=str(folder))),flush=True)
        return
    folder.mkdir(parents=True,exist_ok=True)
    parent_path=PARENT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    bank_path=ROOT/'results/coefficients/bank.npz'
    parent,bank=map(read_npz,[parent_path,bank_path])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    active=bank['offsets']!=0
    grid_ratios=np.exp(bank['offsets'][active]*float(bank['spacing']))
    factor=linalg.cholesky(basis.mass,lower=True)
    paths=[event_path(int(step)) for step in SOURCE_STEPS]
    inputs=[parent_path,parent_path.parent/'status.json',bank_path,bank_path.parent/'status.json',*paths,*ladder.inputs]
    fingerprint={str(path):digest(path) for path in [*inputs,Path(__file__).resolve(),ROOT/'carry_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']}
    fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
    if (folder/'INPUTS.json').exists():
        assert json.loads((folder/'INPUTS.json').read_text())==fingerprint
    else:
        write_json(folder/'INPUTS.json',fingerprint)
    records=[]
    for index,(step,path) in enumerate(zip(SOURCE_STEPS,paths)):
        archive=folder/f'epoch-{index:02d}.npz'
        record_path=archive.with_suffix('.json')
        if record_path.exists():
            record=json.loads(record_path.read_text())
            assert record['fingerprint_sha256']==fingerprint_hash and digest(archive)==record['archive_sha256']
            records.append(record)
            continue
        event=read_npz(path)
        unique,inverse=np.unique(event['ratios'],return_inverse=True)
        rates=np.bincount(inverse,weights=event['rates'],minlength=len(unique))
        checks=[]
        if index==0:
            physical=parent['physical'][-1].copy()
            cubic=parent['cubic'][-1].copy()
            moment=2*float(bank['eigenvalue'][index])
            raw_physical_error=None
            raw_cubic_error=None
            checks.append(dict(name='Exact Stage132 endpoint weak operators',passed=True))
        else:
            physical,moment,diagnostic=stable_adjoint(basis,parent['frequency'],parent['weights'],unique,rates)
            cubic,cubic_moment,cubic_diagnostic=stable_adjoint(basis,parent['frequency'],parent['weights'],grid_ratios,bank['stencil'][index,active])
            raw_physical_error=diagnostic['raw_energy_error']
            raw_cubic_error=cubic_diagnostic['raw_energy_error']
            checks.extend([check(f'Raw physical energy:{step}',raw_physical_error,1e-8),
                check(f'Raw cubic energy:{step}',raw_cubic_error,1e-8),
                check(f'Common unscaled energy:{step}',abs(cubic_moment-moment)/moment,1e-9)])
        expected=parent['weights']*parent['frequency']*moment/(2*I3)
        for label,action in [('physical',physical),('cubic',cubic)]:
            checks.extend([check(f'Weak energy:{label}:{step}',np.linalg.norm(basis.temperature@action-expected)/np.linalg.norm(expected),1e-9),
                check(f'Weak number:{label}:{step}',np.max(abs(basis.chemical@action)),1e-14)])
        scale=max(float(linalg.norm(linalg.solve_triangular(factor,physical,lower=True))),1e-300)
        error=float(linalg.norm(linalg.solve_triangular(factor,cubic-physical,lower=True)))/scale
        checks.append(check(f'Sensitivity1percent:weak:{step}',error,.01))
        assert all(row['passed'] for row in checks if not row['name'].startswith('Sensitivity1percent:'))
        np.savez_compressed(archive,physical=physical,cubic=cubic,coordinate=bank['coordinate'][index],step=step)
        record=dict(index=index,step=int(step),checks=checks,weak_relative=error,raw_physical_energy_error=raw_physical_error,
            raw_cubic_energy_error=raw_cubic_error,archive=archive.name,archive_sha256=digest(archive),fingerprint_sha256=fingerprint_hash)
        write_json(record_path,record)
        records.append(record)
        write_json(folder/'progress.json',dict(state='running',completed=len(records),total=33,seconds=time.monotonic()-started))
        if index%4==0:
            print(json.dumps(dict(upper=args.upper,index=index,seconds=time.monotonic()-started)),flush=True)
        deadline=os.environ.get('MTS_DEADLINE_UTC')
        if deadline and datetime.now(timezone.utc)>=datetime.fromisoformat(deadline) and len(records)<33:
            raise SystemExit(75)
    values=[read_npz(folder/record['archive']) for record in records]
    np.savez_compressed(folder/'bank.npz',coordinate=bank['coordinate'],steps=SOURCE_STEPS,
        frequency=parent['frequency'],weights=parent['weights'],physical=np.array([row['physical'] for row in values]),
        cubic=np.array([row['cubic'] for row in values]))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=[check_row for row in records for check_row in row['checks']],rows=records,upper=args.upper,
        physical_event_order=6,source_projection_scope='Same continuous kernel;separate basis/quadrature and inner grid.',
        seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(upper=args.upper,max_weak=max(record['weak_relative'] for record in records),seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
