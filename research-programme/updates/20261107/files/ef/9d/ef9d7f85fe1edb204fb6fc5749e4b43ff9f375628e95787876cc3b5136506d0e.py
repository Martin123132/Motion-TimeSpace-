from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    sources = {label: ROOT/f'results/{label}/status.json' for label in ['derivation', 'weak-metric', 'flat-motion', 'adm-boost', 'binary-scales']}
    reports = {label: json.loads(path.read_text(encoding='utf-8')) for label, path in sources.items()}
    assert all(report['state'] == 'complete' for report in reports.values())
    scripts = dict(zip(sources, ['derive_motion.py', 'derive_weak_metric.py', 'test_flat_motion.py', 'test_adm_boost.py', 'match_binary_scales.py']))
    for label, report in reports.items():
        assert report['script_sha256'] == digest(ROOT/scripts[label])
    exact_count = 0
    for label, count in [('derivation', 17), ('weak-metric', 6)]:
        assert reports[label]['exact_check_count'] == len(reports[label]['checks']) == count
        assert all(row['passed'] for row in reports[label]['checks'])
        exact_count += count
    flat = reports['flat-motion']
    assert len(flat['rows']) == 6 and len(flat['sources']) == 3
    for source in flat['sources']:
        assert Path(source['path']).is_file() and digest(source['path']) == source['sha256']
    fine = [row for row in flat['rows'] if row['radial_cells'] == 512]
    coarse = [row for row in flat['rows'] if row['radial_cells'] == 256]
    all_boosts = [entry for row in flat['rows'] for entry in row['boosts']]
    fine_exchange = [entry for row in fine for entry in row['extended_source_exchange']]
    assert len(all_boosts) == 30 and len(fine_exchange) == 15
    boost_error = max(max(row[key] for key in ['relative_energy_lorentz_error', 'momentum_error_over_gamma_energy',
                                             'relative_charge_error', 'relative_fixed_charge_routhian_error', 'relative_mass_shell_error']) for row in all_boosts)
    exchange_error = max(max(row['relative_energy_monopole_error'], row['relative_force_monopole_error']) for row in fine_exchange)
    assert boost_error < 1e-10 and exchange_error < 1e-10
    quadrature_changes = []
    for fine_row in fine:
        coarse_row = next(row for row in coarse if row['flat_radius'] == fine_row['flat_radius'])
        for coarse_entry, fine_entry in zip(coarse_row['extended_source_exchange'], fine_row['extended_source_exchange']):
            assert coarse_entry['separation'] == fine_entry['separation'] and fine_entry['surface_gap'] > 0
            quadrature_changes.append(abs(coarse_entry['force_magnitude_over_G_source_mass']/fine_entry['force_magnitude_over_G_source_mass']-1))
        assert 0 < fine_row['naive_unreduced_action_mass_fraction'] < .06
        assert fine_row['relative_rest_energy_source_difference'] < 1e-9
    assert max(quadrature_changes) < 1e-7
    adm = reports['adm-boost']
    assert digest(adm['source_path']) == adm['source_sha256']
    assert len(adm['rows']) == 24 and len(adm['extrapolations']) == 4
    adm_error = max(max(row[key] for key in ['relative_energy_lorentz_error', 'momentum_error_over_gamma_mass', 'relative_mass_shell_error'])
                    for row in adm['extrapolations'])
    adm_angular = max(max(row['angular_refinement_energy_difference_over_mass'], row['angular_refinement_momentum_difference_over_mass'])
                      for row in adm['extrapolations'])
    assert adm_error < 1e-9 and adm_angular < 1e-10
    for speed in [0., .2, .5, .8]:
        rows = [row for row in adm['rows'] if row['speed'] == speed]
        errors = [row['relative_energy_error'] for row in rows]
        assert all(first > second for first, second in zip(errors[:-1], errors[1:]))
    scales = reports['binary-scales']
    for path, expected in scales['source_hashes'].items():
        assert digest(path) == expected
    assert scales['fixed_alpha'] == adm['alpha'] == .00019661998915671979
    assert scales['body_adm_energy'] == adm['body_adm_energy']
    assert len(scales['rows']) == 4 and not scales['physical_units_calibrated']
    for row in scales['rows']:
        assert row['each_body_speed'] < .03 and row['companion_potential_magnitude'] < .002
        assert row['interaction_energy'] < 0 and row['force_magnitude'] > 0
        assert not row['quadrupole_adiabaticity_established']
    for first, second in zip(scales['rows'][:-1], scales['rows'][1:]):
        assert abs(first['force_magnitude']/second['force_magnitude']-4) < 1e-12
        assert abs(first['interaction_energy']/second['interaction_energy']-2) < 1e-12
    result = {'state': 'complete', 'script_sha256': digest(__file__),
              'input_hashes': {str(path.relative_to(ROOT)): digest(path) for path in sources.values()},
              'exact_identity_checks': exact_count, 'flat_physical_profiles': 3, 'flat_quadrature_configurations': 6,
              'flat_boost_checks': 30, 'extended_source_exchange_checks': 30, 'adm_surface_integrals': 28,
              'binary_scale_examples': 4, 'maximum_flat_boost_normalized_error': boost_error,
              'maximum_fine_extended_source_error': exchange_error, 'maximum_force_quadrature_change': max(quadrature_changes),
              'maximum_adm_extrapolated_normalized_error': adm_error, 'maximum_adm_angular_normalized_change': adm_angular,
              'maximum_finite_radius_adm_energy_error': max(row['relative_energy_error'] for row in adm['rows']),
              'proper_matter_over_adm_energy': adm['matter_proper_energy']/adm['body_adm_energy'],
              'unreduced_action_mass_fractions': [{'radius': row['flat_radius'], 'fraction': row['naive_unreduced_action_mass_fraction']} for row in fine],
              'physical_precision_not_inferred_from_algebraic_agreement': True,
              'leading_body_action_matched_at_fixed_charge': True,
              'newton_interaction_from_retained_einstein_action': True,
              'newton_constant_microscopically_derived': False,
              'tidal_response_coefficient_or_nonradial_stability_established': False,
              'binary_evolution_performed': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
