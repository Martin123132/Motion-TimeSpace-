from stage164_common import *


def main():
    modest()
    source=verify_packet(ROOT/'results/sources')
    legacy=verify_packet(ROOT/'results/legacy-update')
    reference=verify_packet(ROOT/'results/reference')
    baseline=verify_packet(ROOT/'results/baseline-check')
    diagnosis=verify_packet(ROOT/'results/phase-diagnosis')
    probe=verify_packet(ROOT/'results/state-roundoff-probe')
    assert baseline['all_checks_passed']
    comparison=verify_packet(ROOT/'results/comparison') if (ROOT/'results/comparison/status.json').exists() else None
    groups={}
    for name,selector in [('complete_sources',':source'),('physical_steps',':step')]:
        rows=[value for key,value in source['summary']['source_precision'].items() if selector in key]
        groups[name]=dict(columns=len(rows),pair_pass=sum(value['pair']<1e-10 for value in rows),
            spectral_pass=sum(value['moment']<1e-10 for value in rows),
            largest_pair=max(value['pair'] for value in rows),largest_spectral=max(value['moment'] for value in rows))
    if comparison:
        target='Assess final-epoch integration uncertainty with the separated physical54/65 response channels and saved interior-band responses;keep the temperature curve fixed and distinguish numerical-reference repair from the MTS correction.'
    elif reference['reference_replay_qualified']:
        target='Run the qualified two-window numerical-reference plus physical-increment replay with the saved baseline/MTS and existing2048/4096 response steps;keep both channels separate and earlier sealed data immutable.'
    else:
        target='Extend the independently checked50/80-digit Born/state-moment evaluator to the saved virtual/state bank,then recheck the unchanged cubic phase gates before replaying the reference. Audit the real-event Born contribution separately:the12-event probe does not certify the full bank. Reconstruct interpolated low moments at high precision to resolve the separate float spectral cancellation;keep the temperature curve and1e-10 limits fixed.'
    worst=diagnosis['records']['terminal-cubic-65']['pair']
    state_defect=sum(Decimal(value['pair']) for name,value in worst['components'].items() if name.endswith('-state'))
    total_defect=Decimal(worst['exact_pair'])
    state_share=float(state_defect/total_defect)
    remaining_pair=float(abs((total_defect-state_defect)/Decimal(worst['exact_energy'])))
    summary=dict(**source['summary'],precision_groups=groups,
        reference_replay_qualified=reference['reference_replay_qualified'],reference_records=reference['records'],phase_records=reference['phase_records'],
        source_reconciliation_completed=reference['source_reconciliation_completed'],
        reference_history_replayed=comparison is not None,reference_history_verified=bool(comparison and comparison['all_checks_passed']),
        reference_history_adopted=False,paired_baseline_mts_checks=baseline['count'],
        paired_baseline_mts_passed=baseline['all_checks_passed'],
        phase_diagnosis_checks_passed=diagnosis['all_checks_passed'],
        phase_diagnosis=diagnosis['records'],
        worst_cubic_state_fraction=state_share,
        worst_cubic_pair_after_hypothetical_state_only_removal=remaining_pair,
        state_roundoff_probe_passed=probe['all_checks_passed'],
        state_roundoff_probe_events=probe['probes'],
        state_roundoff_probe_records=probe['records'],
        state_roundoff_full_bank_adopted=False,
        legacy_failures_retained=[row for row in legacy['checks'] if not row['passed']],
        reference_failures_retained=[row for row in reference['checks'] if not row['passed']],
        new_response_evolutions=16 if comparison else 0,
        response_records=comparison['records'] if comparison else None,
        accepted_scope='Complete correlated soft-subtraction repair of7560 endpoint event moments;independent endpoint source gates and explicit legacy-reference defect accounting;paired baseline/MTS verification;12-event independent state-moment precision probe. Two sampled cubic increment phase gates block response replay;no refitting or saved-history replacement.',
        next_target=target)
    summary['response_propagation_allowed']=reference['reference_replay_qualified']
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(groups=groups,reference_qualified=reference['reference_replay_qualified'],
        reference_failed_checks=summary['reference_failures_retained'],response_evolutions=summary['new_response_evolutions'])),flush=True)


if __name__=='__main__':
    main()
