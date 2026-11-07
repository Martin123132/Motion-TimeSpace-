from coefficient_common import *


def main():
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert summary['checks']==1180 and summary['passes']==1111
    assert summary['failure_categories']=={'Low exact moment':33,'Response':28,'Sensitivity1percent':8}
    feedback=[row for row in summary['rows'] if row['packet'].startswith('feedback-')]
    replays=[row for row in summary['rows'] if row['packet'].startswith('replay-')]
    maxima={}
    for variant in ['dense-direct','balanced-direct','balanced-factored']:
        maxima[variant]=dict(
            baseline_endpoint=max(row['variants'][variant]['comparison']['gas_endpoint_relative'][0] for row in feedback),
            mts_endpoint=max(max(row['variants'][variant]['comparison']['gas_endpoint_relative'][1:]) for row in feedback),
            radiation=max(max(row['variants'][variant]['comparison']['radiation_relative']) for row in feedback))
    maxima['raw_gas_residual']=max(max(variant['response_errors']['gas'] for variant in row['variants'].values()) for row in feedback)
    maxima['sparse_solve']=max(max(row['solve_errors']) for row in replays)
    maxima['endpoint_state_baseline']=max(row['endpoint_defect_relative'][0] for row in replays)
    maxima['endpoint_state_mts']=max(max(row['endpoint_defect_relative'][1:]) for row in replays)
    assert all(all(variant['comparison']['endpoint_sign_preserved']) for row in feedback for variant in row['variants'].values())
    prior=json.loads((PARENT/'ACCURACY-REVIEW.json').read_text())
    next_target=('Compare the source-adjoint-derived positive pairing with the current pair-total-preserving repair '
        'before selecting a production discretization. Derive and measure their full weak actions/symbols,not only '
        'their matched moments,then run paired first-interval tests if the difference matters. Reuse saved events and '
        'restart points. After selecting and testing the operator,carry the altered endpoint state continuously into '
        'later intervals for both backgrounds,with explicit finite-boundary flux accounting and joint source/inner '
        'checks. Do not treat the current139-knot local splice as a globally self-consistent history.')
    conclusion=('The physical source moment and inner eigenvalue satisfy m=2lambda on the saved kernels. A derived '
        'positive reciprocal-pair repair removes the measured0.44percent bulk energy deposition bias while retaining '
        'positivity and chemical subinvariance. All six prefix replays complete;old controls reproduce saved states '
        'bitwise. Denser temperature samples shift the wide MTS gas endpoint by1.08–1.13percent,leaving eight '
        'unchanged1percent sensitivity flags;the repair itself changes that correction by at most0.2314percent '
        'relative to dense-unrepaired evolution. The positive repair is a declared numerical candidate,not a unique '
        'collision law;the source-aligned pairing is derived as the next discriminator. Changed endpoint states '
        'are saved and must be carried rather than silently reset for a physical full-history prediction.')
    review=dict(stage=129,accepted_scope=summary['scope'],scientific_checks=summary['checks'],
        passing_scientific_checks=summary['passes'],retained_failed_checks=summary['retained_failed_checks'],
        expected_failed_by_packet=summary['expected_failed_by_packet'],failure_categories=summary['failure_categories'],
        combined_original_response_failures=prior['combined_original_response_failures'],
        prior_stage_failed_checks_retained=prior['retained_failed_checks'],maxima=maxima,
        conclusion=conclusion,next_target=next_target,independent_validation_required=True,
        new_fundamental_collision_law=False,positive_aggregate_candidate=True,
        source_aligned_pairing_derived_not_evaluated=True,later_state_carried=False,
        finite_boundary_flux_certificate=False,new_high_precision=False,goal_turn_classification='progress')
    write_json(ROOT/'ACCURACY-REVIEW.json',review)
    print(json.dumps(maxima),flush=True)


if __name__=='__main__':
    main()
