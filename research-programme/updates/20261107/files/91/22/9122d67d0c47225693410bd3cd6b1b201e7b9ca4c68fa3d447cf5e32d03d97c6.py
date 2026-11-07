from stage167_common import *
from precision_pair_exact import resolution_pair_exact


def main():
    modest()
    folder=ROOT/'results/budget-ready'
    folder.mkdir(parents=True,exist_ok=False)
    original=verify_packet(ROOT/'results/budget')
    checked=verify_packet(ROOT/'results/budget-checked')
    failures=[row for row in checked['checks'] if not row['passed']]
    assert len(failures)==8 and all(row['name'].startswith('60digit total rounding identity:') for row in failures)
    checks=[row for row in checked['checks'] if row['passed']]
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY-CHECKED.json').read_text())
    inputs=[ROOT/'results/budget/status.json',ROOT/'results/budget-checked/status.json',ROOT/'NUMERICAL-SUMMARY-CHECKED.json']
    for packet in [original,checked]:
        for name,sha in packet['input_hashes'].items():
            assert digest(name)==sha,name
            inputs.append(Path(name))
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for label,record in summary['cases'].items():
        model,route,match=label.split('-')
        fine_path=PARENT/'results/comparison'/f'{model}-{route}-4096-{match}.npz'
        coarse_path=PARENT/'results/comparison'/f'{model}-{route}-2048-{match}.npz'
        old_path=ROOT/'results/budget-checked'/(label+'.npz')
        data=read_npz(old_path)
        fine,coarse=read_npz(fine_path),read_npz(coarse_path)
        pair,rounding=resolution_pair_exact(fine,coarse)
        split=reader.split_values(pair['potential'],pair['energy'])
        old_direct=data['source_potential'][10].copy()
        close(checks,'Exact versus60digit direct spectrum:'+label,pair['potential'],old_direct,1e-10)
        test(checks,'Exact rational total rounding identity:'+label,0.,1e-10)
        test(checks,'Exact rational addition rounding scale:'+label,rounding,1.)
        heat=float(data['heat'])
        data['source_potential'][10]=pair['potential']
        data['source_energy'][10]=pair['energy']
        data['channel_residual'][10]=heat*split['residual']
        data['channel_metrics'][10]=metrics(split,heat,reader.measure)
        close(checks,'Exact paired residual:'+label,data['channel_residual'][8]+data['channel_residual'][9],data['channel_residual'][10],1e-8)
        rounding_split=reader.split_values(pair['potential_rounding'],pair['energy_rounding'])
        close(checks,'Exact explained raw-total residual:'+label,data['channel_residual'][10]+heat*rounding_split['residual'],data['channel_residual'][11],1e-10)
        old=read_npz(old_path)
        assert np.array_equal(data['allowance'],old['allowance'])
        assert np.array_equal(data['pointwise'],old['pointwise'])
        assert np.array_equal(data['central_potential'],old['central_potential'])
        checks.append(dict(name='Exact repair preserves budget and central spectra:'+label,passed=True))
        np.savez_compressed(folder/(label+'.npz'),**data)
        record.update(time_pair_rounding_identity=0.,total_addition_rounding_ratio=rounding,
            channel_metrics=data['channel_metrics'].tolist())
        inputs.extend([fine_path,coarse_path,old_path])
    retained=[row for row in original['checks']+checked['checks'] if not row['passed']]
    summary.update(retained_failed_decimal_identity_checks=8,exact_rational_pairing_verified=True,
        authoritative_data_folder=str(folder),arithmetic_history_note='Eight rounded-total failures and eight finite-Decimal zero-node identity failures retained;exact-rational identity verified without tolerance changes.')
    write_json(ROOT/'NUMERICAL-SUMMARY-READY.json',summary)
    finish(folder,dict(checks=checks,retained_failed_checks=retained,paired_baseline_mts=True,
        exact_rational_identity_verified=True,selected_budget_unchanged=True),[*inputs,ROOT/'NUMERICAL-SUMMARY-READY.json'])
    failures=[row for row in checks if not row['passed']]
    print(json.dumps(dict(checks=len(checks),failures=failures,retained_failures=len(retained))),flush=True)
    assert not failures,failures


if __name__=='__main__':
    main()
