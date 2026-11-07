from seven_eighths_history_common import *
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
        assert local_packet(folder)['all_checks_passed']
        print(json.dumps(dict(reused=str(folder))),flush=True)
        return
    folder.mkdir(parents=True,exist_ok=True)
    parent_path=PARENT/'results'/f'weak-m{int(args.upper*1000)}/bank.npz'
    bank_path=ROOT/'results/coefficients/bank.npz'
    unit_path=P133/'results/linear-source-cache'/f'unit-m{int(args.upper*1000)}.npz'
    parent,bank,unit=map(read_npz,[parent_path,bank_path,unit_path])
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    active=bank['offsets']!=0
    assert np.array_equal(bank['offsets'][active],unit['offsets'])
    assert np.array_equal(parent['frequency'],unit['frequency']) and np.array_equal(parent['weights'],unit['weights'])
    assert float(bank['spacing'])==float(unit['spacing'])
    grid_ratios=unit['ratios']
    cached=np.einsum('tj,jkl->tkl',bank['stencil'][:,active],unit['unit_adjoint'],optimize=True)
    factor=linalg.cholesky(basis.mass,lower=True)
    paths=[event_path(int(step)) for step in SOURCE_STEPS]
    inputs=[parent_path,parent_path.parent/'status.json',bank_path,bank_path.parent/'status.json',unit_path,
        unit_path.parent/'status.json',*paths,*ladder.inputs]
    fingerprint={str(path):digest(path) for path in [*inputs,Path(__file__).resolve(),ROOT/'seven_eighths_history_common.py',ROOT/'ACCEPTANCE.md',ROOT/'DERIVATION.md']}
    fingerprint_hash=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()).hexdigest()
    if (folder/'INPUTS.json').exists():
        assert json.loads((folder/'INPUTS.json').read_text())==fingerprint
    else:
        write_json(folder/'INPUTS.json',fingerprint)
    records=[]
    for index,(step,path) in enumerate(zip(SOURCE_STEPS,paths)):
        archive=folder/f'epoch-{index:03d}.npz'
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
        cubic=cached[index].copy()
        if index==0:
            physical=parent['physical'][-1].copy()
            endpoint_scale=max(float(linalg.norm(parent['cubic'][-1])),1e-300)
            endpoint_error=float(linalg.norm(cubic-parent['cubic'][-1]))/endpoint_scale
            checks.append(check('Cached endpoint versus saved Stage139 source',endpoint_error,1e-12))
            cubic=parent['cubic'][-1].copy()
            moment=2*float(bank['eigenvalue'][index])
            raw_physical_error=None
        else:
            physical,moment,diagnostic=stable_adjoint(basis,unit['frequency'],unit['weights'],unique,rates)
            raw_physical_error=diagnostic['raw_energy_error']
            checks.append(check(f'Raw physical energy:{step}',raw_physical_error,1e-8))
        cached_moment=float(np.sum(bank['stencil'][index,active]*(grid_ratios-1)**2*(grid_ratios+1)/grid_ratios**3))
        checks.append(check(f'Common unscaled energy:{step}',abs(cached_moment-moment)/moment,1e-9))
        expected=unit['weights']*unit['frequency']*moment/(2*I3)
        for label,action in [('physical',physical),('cubic',cubic)]:
            checks.extend([check(f'Weak energy:{label}:{step}',np.linalg.norm(basis.temperature@action-expected)/np.linalg.norm(expected),1e-9),
                check(f'Weak number:{label}:{step}',np.max(abs(basis.chemical@action)),1e-14)])
        cache_error=None
        if index%16==0:
            direct,direct_moment,direct_diagnostic=stable_adjoint(basis,unit['frequency'],unit['weights'],grid_ratios,bank['stencil'][index,active])
            cache_error=float(linalg.norm(cubic-direct))/max(float(linalg.norm(direct)),1e-300)
            checks.extend([check(f'Independent common-kernel evaluation:{step}',cache_error,1e-11),
                check(f'Raw direct common energy:{step}',direct_diagnostic['raw_energy_error'],1e-8)])
        scale=max(float(linalg.norm(linalg.solve_triangular(factor,physical,lower=True))),1e-300)
        error=float(linalg.norm(linalg.solve_triangular(factor,cubic-physical,lower=True)))/scale
        checks.append(check(f'Sensitivity1percent:weak:{step}',error,.01))
        assert all(row['passed'] for row in checks if not row['name'].startswith('Sensitivity1percent:'))
        np.savez_compressed(archive,physical=physical,cubic=cubic,coordinate=bank['coordinate'][index],step=step)
        record=dict(index=index,step=int(step),checks=checks,weak_relative=error,
            raw_physical_energy_error=raw_physical_error,independent_cache_error=cache_error,
            archive=archive.name,archive_sha256=digest(archive),fingerprint_sha256=fingerprint_hash)
        write_json(record_path,record)
        records.append(record)
        write_json(folder/'progress.json',dict(state='running',completed=len(records),total=len(SOURCE_STEPS),seconds=time.monotonic()-started))
        if index%8==0:
            print(json.dumps(dict(upper=args.upper,index=index,total=len(SOURCE_STEPS),seconds=time.monotonic()-started)),flush=True)
        deadline=os.environ.get('MTS_DEADLINE_UTC')
        if deadline and datetime.now(timezone.utc)>=datetime.fromisoformat(deadline) and len(records)<len(SOURCE_STEPS):
            raise SystemExit(75)
    values=[read_npz(folder/record['archive']) for record in records]
    np.savez_compressed(folder/'bank.npz',coordinate=bank['coordinate'],steps=SOURCE_STEPS,
        frequency=unit['frequency'],weights=unit['weights'],physical=np.array([row['physical'] for row in values]),
        cubic=np.array([row['cubic'] for row in values]))
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=[check_row for row in records for check_row in row['checks']],rows=records,upper=args.upper,
        physical_event_order=6,physical_reference_sites=len(SOURCE_STEPS),independent_cache_sites=len(SOURCE_STEPS[::16]),
        full_new_block_physical_references=True,temperature_fit=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(upper=args.upper,max_weak=max(record['weak_relative'] for record in records),seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
