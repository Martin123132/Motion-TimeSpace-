from stage166_common import *


def main():
    modest()
    source=verify_packet(ROOT/'results/source-qualification')
    readiness=verify_packet(ROOT/'results/response-readiness-checked')
    comparison=verify_packet(ROOT/'results/comparison')
    cases={}
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                label=f'{model}-{route}-{count}'
                packet=verify_packet(ROOT/'results/response'/label)
                assert packet['all_checks_passed']
                cases[label]=dict(metrics=packet['metrics'],source_maxima=packet['source_maxima'],heat=packet['heat'])
    convergence=[row for row in comparison['checks'] if row['name'].startswith('CONVERGENCE:')]
    if comparison['convergence_passed']:
        target='Use the propagated physical54/65 and arithmetic-reference channels to update the saved final-epoch uncertainty budget;compare the remaining frozen-cubic source discrepancy with its physical mu/y/residual effect before changing the curve.'
    else:
        target='Localize the recorded response-step convergence failure using the saved2048/4096 histories and separate physical54/65 versus arithmetic-reference channels;refine only the necessary response calculation without repeating the event bank or changing the temperature curve.'
    summary=dict(stage=166,source_qualified=source['source_qualified'],source_checks=source['count'],source_phase_records=source['phase_records'],
        readiness_checks=readiness['count'],response_cases=cases,comparison_checks=comparison['count'],
        numerical_integrity_passed=comparison['numerical_integrity_passed'],convergence_passed=comparison['convergence_passed'],
        comparison_failures=[row for row in comparison['checks'] if not row['passed']],response_step_checks=convergence,readout_records=comparison['records'],
        actual_baseline_preserved=True,baseline_inner_history_rerun=False,new_event_evaluations=0,new_virtual_integrations=0,
        new_response_evolutions=16,split_high_low_retained=True,reference_history_replayed=True,reference_history_adopted=False,
        saved_baseline_and_mts_owner=str(READOUT_OWNER),candidate_readout_owner=str(ROOT/'results/comparison'),
        arithmetic_reference_separate=True,temperature_curve_changed=False,band_orders=[6,6,6,8,7,7,6],tolerances_changed=False,
        corrected_test_denominator=True,old_failed_smoke_retained=True,source_adopted=False,next_target=target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(source_checks=source['count'],readiness=readiness['count'],comparison=comparison['count'],
        numerical=comparison['numerical_integrity_passed'],convergence=comparison['convergence_passed'],failed=summary['comparison_failures'])),flush=True)


if __name__=='__main__':
    main()
