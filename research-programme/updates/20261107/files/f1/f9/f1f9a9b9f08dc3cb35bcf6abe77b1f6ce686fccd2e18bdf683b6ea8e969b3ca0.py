from stage162_common import *


def main():
    modest()
    raw=verify_packet(ROOT/'results/sources')
    moment=verify_packet(ROOT/'results/moment-repair')
    diagnosis=verify_packet(ROOT/'results/conditioning')
    baseline=verify_packet(ROOT/'results/baseline-check')
    probe=verify_packet(ROOT/'results/stable-jump-probe')
    assert probe['all_checks_passed']
    assert diagnosis['all_checks_passed'] and baseline['all_checks_passed']
    raw_failures=[row for row in raw['checks'] if not row['passed']]
    assert raw_failures and all(row['name'].startswith(('Endpoint unprojected moment:','Endpoint photon/gas exchange:')) for row in raw_failures)
    moment_failures=[row for row in moment['checks'] if not row['passed']]
    assert moment_failures
    summary=dict(**raw['summary'],paired_baseline_mts=dict(saved_readout_checks=baseline['count'],
        all_checks_passed=baseline['all_checks_passed'],new_endpoint_response=False,
        baseline_preserved=True,mts_preserved=True,inner_histories_rerun=False),
        atomic_precision=dict(raw_failed_checks=raw_failures,sixty_digit_failed_checks=moment_failures,
            largest_pair_relative=diagnosis['diagnosis']['largest_atomic_pair_relative'],
            largest_moment_relative=diagnosis['diagnosis']['largest_atomic_moment_relative'],
            tolerance_unchanged=1e-10,reaggregation_resolves_input_error=False),
        stable_jump_probe=dict(checks=probe['count'],all_checks_passed=probe['all_checks_passed'],
            records=probe['records'],full_source_recomputed=False),
        spectral_quadrature_diagnostics_complete=True,all_numerical_gates_passed=False,
        moment_readiness_passed=False,response_propagation_allowed=False,new_response_evolutions=0,
        next_target='Build a moment-only evaluator using the derived stable photon jump and analytic low test functions;verify against these four full-event probes,then rebuild all7560 endpoint order4/5/6 event moments with saved virtual coefficients and unchanged histories. Keep the independent electron moment and1e-10 gate;propagate only after the full source passes.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(complete_accuracy_experiment=True,raw_failures=len(raw_failures),
        atomic_failures=len(moment_failures),response_allowed=False)),flush=True)


if __name__=='__main__':
    main()
