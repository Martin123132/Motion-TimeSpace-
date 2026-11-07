from stage165_common import *


def main():
    modest()
    refined=(ROOT/'results/sources-refined/COMPLETE').exists()
    suffix='-refined' if refined else ''
    source=verify_packet(ROOT/'results'/('sources'+suffix))
    legacy=verify_packet(ROOT/'results'/('legacy-update'+suffix))
    reference=verify_packet(ROOT/'results'/('reference'+suffix))
    initial_reference=verify_packet(ROOT/'results/reference')
    baseline=verify_packet(ROOT/'results/baseline-check')
    stable=verify_packet(ROOT/'results/reference-stable') if (ROOT/'results/reference-stable/status.json').exists() else None
    certified=verify_packet(ROOT/'results/reference-certified') if (ROOT/'results/reference-certified/status.json').exists() else None
    basis_diagnosis=verify_packet(ROOT/'results/basis-representation-diagnosis') if (ROOT/'results/basis-representation-diagnosis/status.json').exists() else None
    comparison=verify_packet(ROOT/'results/comparison') if (ROOT/'results/comparison/status.json').exists() else None
    diagnosis=verify_packet(ROOT/'results/phase-diagnosis') if (ROOT/'results/phase-diagnosis/status.json').exists() else None
    qualification=certified or stable or reference
    groups={}
    for name,selector in [('complete_sources',':source'),('physical_steps',':step')]:
        rows=[value for key,value in source['summary']['source_precision'].items() if selector in key]
        groups[name]=dict(columns=len(rows),pair_pass=sum(value['pair']<1e-10 for value in rows),spectral_pass=sum(value['moment']<1e-10 for value in rows),
            largest_pair=max(value['pair'] for value in rows),largest_spectral=max(value['moment'] for value in rows))
    if comparison:
        target='Use the separately propagated reference and physical54/65 channels to quantify final-epoch integration uncertainty before changing the frozen temperature curve.'
    elif qualification['reference_replay_qualified']:
        target='Run the qualified two-window reference and physical-increment replay at the saved response-step counts,checking baseline and MTS without changing the frequency bands or temperature curve.'
    else:
        target='Carry the tested twofold representation of the frozen analytic basis product and low moments through source/reference forcing;recheck every actual response phase and baseline/MTS with the unchanged1e-10 gate before replay. Reuse the repaired bank;do not repeat expensive event integration or change the temperature curve.' if basis_diagnosis and basis_diagnosis['all_checks_passed'] else 'Resolve the recorded residual raw cancellation using the saved basis/phase diagnosis before another bank calculation;do not refit the curve or relax tolerance.'
    summary=dict(**source['summary'],precision_groups=groups,reference_records=reference['records'],phase_records=reference['phase_records'],
        reference_replay_qualified=qualification['reference_replay_qualified'],source_reconciliation_completed=reference['source_reconciliation_completed'],
        source_owner=str(ROOT/'results'/('sources'+suffix)),reference_owner=str(ROOT/'results'/('reference'+suffix)),
        initial_born_state_reference_failures=[row for row in initial_reference['checks'] if not row['passed']],
        reference_history_replayed=comparison is not None,reference_history_verified=bool(comparison and comparison['all_checks_passed']),reference_history_adopted=False,
        paired_baseline_mts_checks=baseline['count'],paired_baseline_mts_passed=baseline['all_checks_passed'],
        legacy_failures_retained=[row for row in legacy['checks'] if not row['passed']],reference_failures_retained=[row for row in reference['checks'] if not row['passed']],
        stable_phase_records=stable if stable else None,certified_phase_records=certified if certified else None,
        basis_representation_diagnosis=basis_diagnosis if basis_diagnosis else None,
        phase_diagnosis=diagnosis['records'] if diagnosis else None,
        new_response_evolutions=16 if comparison else 0,response_records=comparison['records'] if comparison else None,
        accepted_scope='Independent state/Born precision repair across7560 saved endpoint events,adaptive independent real-shift precision where recorded,unchanged precision gates and reference accounting;actual baseline/MTS re-evaluated;response scope as recorded.',next_target=target)
    summary['response_propagation_allowed']=qualification['reference_replay_qualified']
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(groups=groups,reference_qualified=summary['reference_replay_qualified'],phase_records=reference['phase_records'],
        reference_failures=summary['reference_failures_retained'],response_evolutions=summary['new_response_evolutions'])),flush=True)


if __name__=='__main__':
    main()
