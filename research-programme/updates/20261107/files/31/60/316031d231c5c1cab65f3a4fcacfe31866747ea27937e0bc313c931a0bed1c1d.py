from quadrature_common import *


def main():
    summary = json.loads((ROOT / 'NUMERICAL-SUMMARY.json').read_text())
    assert summary['checks'] == 1746 and summary['passes'] == 1718
    assert summary['failure_categories'] == {'Response': 28}
    assert all(name.startswith('Response:') and name.endswith(':gas')
        for names in summary['expected_failed_by_packet'].values() for name in names)
    comparisons = summary['comparisons']
    maxima = dict(
        arithmetic_endpoint=max(max(row['variants']['stable']['comparisons']['legacy']['gas_endpoint_relative']) for row in comparisons),
        event_endpoint=max(max(row['variants'][variant]['comparisons'][reference]['gas_endpoint_relative'])
            for row in comparisons for variant, reference in [('event1', 'stable'), ('event2', 'event1')]),
        frequency_final_increment_endpoint=max(max(row['variants']['frequency2']['comparisons']['frequency1']['gas_endpoint_relative']) for row in comparisons),
        refined_total_endpoint_baseline=max(row['variants']['frequency2']['versus_legacy']['gas_endpoint_relative'][0] for row in comparisons),
        refined_total_endpoint_mts=max(max(row['variants']['frequency2']['versus_legacy']['gas_endpoint_relative'][1:]) for row in comparisons),
        refined_total_radiation=max(max(row['variants']['frequency2']['versus_legacy']['radiation_relative']) for row in comparisons),
        source_component_relative=max(max(diagnostic['maximum_relative_to_components']) for row in comparisons
            for variant in row['variants'].values() for diagnostic in variant['source_comparisons'].values()),
        raw_gas_residual=max(max([row['legacy_control']['response_errors']['gas'],
            *[variant['response_errors']['gas'] for variant in row['variants'].values()]]) for row in comparisons),
        mixed_peak_relative=max(max(row['interaction_peak_relative']) for row in comparisons),
        mixed_endpoint_relative=max(float(np.max(abs(np.array(row['interaction_endpoint'])) /
            abs(np.array(row['variants']['stable']['comparisons']['legacy']['gas_endpoint'])))) for row in comparisons),
        pre_replacement_energy=max(row['maximum_raw_energy_error'] for row in summary['banks']))
    ratios = [value for row in comparisons for value in row['refinement']['frequency']['endpoint_difference_ratio']]
    assert all(value < 1 for value in ratios)
    assert all(row['total_domain_crossing_pairs'] == 0 for row in summary['banks'])
    assert all(all(metric['endpoint_sign_preserved']) for row in comparisons
        for variant in row['variants'].values() for metric in variant['comparisons'].values())
    next_target = ('Derive and test the temperature-interpolation contribution to the direct-versus-assembled Compton source, '
        'using the saved first-interval operators and histories. Separate operator curvature, unresolved-state evolution, '
        'and interpolation of their product; propagate signed terms identically for baseline/MTS and both windows/backgrounds. '
        'Then refine the initial-interval inner collision coefficients consistently with the source, using the saved restart '
        'rather than another blanket time or frequency refinement. Keep the response grid fixed for that isolation test; '
        'continuous-time response accuracy, remaining intervals and initial-memory ownership stay separate follow-ups.')
    conclusion = ('The paired arithmetic and tested event/frequency refinements are stable at the preregistered1percent '
        'source/response thresholds for all four cases. The largest total q32-to-q128 MTS gas endpoint change is4.254e-5 '
        'relative (0.004254percent of the small correction), much smaller than the prior source-time refinement change. '
        'Frequency increments shrink in every case; event increments are near numerical reproducibility and do not '
        'establish a convergence order. None of the tested endpoint signs changes. The tested operator quadrature '
        'therefore does not explain the earlier large source-time sensitivity at these16 sites. Move to temperature '
        'interpolation and inner/source consistency, not a higher quadrature order by default. All28 raw gas1e-7 '
        'diagnostic failures and inherited failures remain visible; this is not a physical-signal error certificate.')
    review = dict(stage=127, accepted_scope=summary['scope'],
        scientific_checks=summary['checks'], passing_scientific_checks=summary['passes'],
        retained_failed_checks=summary['retained_failed_checks'],
        expected_failed_by_packet=summary['expected_failed_by_packet'],
        combined_original_response_failures=summary['combined_original_response_failures'],
        prior_stage_failed_checks_retained=summary['prior_stage_failed_checks_retained'],
        maxima=maxima, frequency_endpoint_increment_ratio_range=[min(ratios), max(ratios)],
        previous_failure_counts_not_directly_comparable=True,
        conclusion=conclusion, next_target=next_target,
        physical_time_accuracy_certified=False, inner_source_joint_refinement=False,
        new_high_precision='80digit kernel arithmetic reference only;no new high-precision response evolution',
        highest_joint_quadrature_rule_tested=False, common_kernel_bias_excluded=False,
        goal_turn_classification='progress', independent_validation_required=True)
    write_json(ROOT / 'ACCURACY-REVIEW.json', review)
    print(json.dumps(dict(maxima=maxima, frequency_ratio_range=review['frequency_endpoint_increment_ratio_range'])), flush=True)


if __name__ == '__main__':
    main()
