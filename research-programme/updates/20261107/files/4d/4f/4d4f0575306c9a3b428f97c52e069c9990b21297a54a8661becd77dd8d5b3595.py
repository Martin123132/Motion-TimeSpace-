from quadrature_common import *


def main():
    modest()
    packets = sorted((ROOT / 'results').glob('*/status.json'))
    packets = [path for path in packets if path.parent.name != 'validation']
    assert len(packets) == 17
    checks, failed, source_hashes = [], {}, {}
    banks, comparisons = [], []
    for path in packets:
        packet = local_packet(path.parent)
        source_hashes[str(path)] = digest(path)
        checks.extend(packet['checks'])
        names = [row['name'] for row in packet['checks'] if not row['passed']]
        if names:
            failed[path.parent.name] = names
        if path.parent.name.startswith('bank-'):
            rows = packet['rows']
            banks.append(dict(name=path.parent.name, event_order=packet['event_order'],
                frequency_panel_order=packet['frequency_panel_order'], sites=len(rows),
                event_count_per_site=[row['events'] for row in rows],
                maximum_raw_energy_error=max(row['diagnostics']['raw_energy_error'] for row in rows),
                total_domain_crossing_pairs=sum(row['diagnostics']['domain_crossing_pairs'] for row in rows),
                maximum_domain_weight_fraction=max(row['diagnostics']['positive_weight_crossing_fraction'] for row in rows),
                arithmetic_operator_relative_changes=[row['arithmetic_operator_relative_change'] for row in rows]))
        elif path.parent.name.startswith('comparison-'):
            variants = {}
            for name, variant in packet['variants'].items():
                compact = {key: value for key, value in variant.items() if key != 'source_comparisons'}
                compact['source_comparisons'] = {}
                for reference, diagnostic in variant['source_comparisons'].items():
                    compact['source_comparisons'][reference] = dict(
                        maximum_relative_to_components=np.max(diagnostic['relative_to_components'], axis=0).tolist(),
                        maximum_relative_to_total=np.max(diagnostic['relative_to_total'], axis=0).tolist(),
                        maximum_energy_moment_absolute=np.max(np.abs(diagnostic['energy_moment']), axis=(0, 1)).tolist(),
                        maximum_number_moment_absolute=np.max(np.abs(diagnostic['number_moment']), axis=(0, 1)).tolist())
                variants[name] = compact
            comparisons.append(dict(model=packet['model'], upper=packet['upper'],
                variants=variants, legacy_control=packet['legacy_control'], refinement=packet['refinement'],
                interaction_endpoint=packet['interaction_endpoint'],
                interaction_peak_relative=packet['interaction_peak_relative'],
                original_failed_checks=packet['original_failed_checks']))
    assert len(banks) == 12 and len(comparisons) == 4
    categories = {}
    for row in checks:
        if not row['passed']:
            category = row['name'].split(':')[0]
            categories[category] = categories.get(category, 0) + 1
    prior = json.loads((PARENT / 'ACCURACY-REVIEW.json').read_text())
    result = dict(stage=127, state='calculated',
        scope='Paired arithmetic and separate event/frequency quadrature tests at16 saved odd sites of interval0;both backgrounds,windows and baseline/MTS joins.',
        checks=len(checks), passes=sum(bool(row['passed']) for row in checks),
        retained_failed_checks=sum(not row['passed'] for row in checks),
        expected_failed_by_packet=failed, failure_categories=categories,
        combined_original_response_failures=prior['combined_original_response_failures'],
        prior_stage_failed_checks_retained=prior['retained_failed_checks'],
        arithmetic_proof={key: value for key, value in local_packet(ROOT / 'results/arithmetic-proof').items()
            if key not in ['input_hashes', 'checks', 'rows']},
        banks=banks, comparisons=comparisons, source_packet_hashes=source_hashes,
        fixed_evolution_frequency_nodes=5265, fixed_inner_steps=40960, fixed_response_steps=2048,
        source_knots=138, changed_odd_source_sites=16, new_inner_steps=0,
        highest_joint_rule_tested=False, physical_signal_certified=False)
    write_json(ROOT / 'NUMERICAL-SUMMARY.json', result)
    print(json.dumps(dict(checks=result['checks'], passes=result['passes'],
        failures=result['retained_failed_checks'], categories=categories)), flush=True)
    for comparison in comparisons:
        print(json.dumps(dict(model=comparison['model'], upper=comparison['upper'],
            refinement=comparison['refinement'],
            metrics={name: {reference: {key: metric[key] for key in
                ['radiation_relative', 'gas_peak_relative', 'gas_endpoint_relative', 'gas_endpoint', 'endpoint_sign_preserved']}
                for reference, metric in variant['comparisons'].items()}
                for name, variant in comparison['variants'].items()})), flush=True)


if __name__ == '__main__':
    main()
