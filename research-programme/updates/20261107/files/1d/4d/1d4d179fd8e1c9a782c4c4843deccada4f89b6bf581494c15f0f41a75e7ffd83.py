from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import psutil

from sequence_tools import digest


ROOT = Path(__file__).resolve().parent


def read(relative):
    return json.loads((ROOT/relative).read_text(encoding='utf-8'))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    sources = sorted(ROOT.glob('results/*/status.json'))
    sequences, accepted, failed = [], [], []
    for path in sources:
        report = json.loads(path.read_text(encoding='utf-8'))
        if 'attempts' not in report:
            continue
        assert report['state'] in ['complete', 'failed']
        helper = next(candidate for candidate in ROOT.glob('sequence_tools*.py') if digest(candidate) == report['helper_sha256'])
        driver = next(candidate for candidate in ROOT.glob('continue_sequence*.py') if digest(candidate) == report['script_sha256'])
        assert helper.is_file() and driver.is_file()
        seed = Path(report['seed_path'])
        if not seed.is_absolute():
            seed = ROOT/seed
        assert digest(seed) == report['seed_sha256']
        assert report['fixed_alpha'] == 0.00019661998915671979
        converged_names = {attempt['archive'] for attempt in report['attempts'] if attempt['converged']}
        for row in report['rows']:
            assert row['converged'] and row['archive'] in converged_names
            assert row['alpha'] == row['fixed_alpha'] == report['fixed_alpha']
            assert row['minimum_F'] > 0 and row['min_amplitude_interior'] > 0
            assert row['mass_quadrature_relative_error'] < 1e-7
            assert row['charge_accumulation_relative_error'] < 1e-7
            assert row['komar_adm_relative_error_without_tiny_tail'] < 1e-6
            assert row['max_rms_residual'] < 1.001*report['arguments']['tol']
            assert row['boundary_max_residual'] < 1e-10
            if row['control_kind'] == 'central':
                assert abs(row['central_amplitude']-row['control_value']) < 1e-7
            else:
                assert row['target_charge_relative_error'] < 1e-7
            assert (path.parent/row['archive']).is_file()
            assert (path.parent/row['spectrum_archive']).is_file()
            assert row['spectrum']['phase_null_relative_residual'] < 1e-12
            accepted.append(row)
        failures = [attempt for attempt in report['attempts'] if not attempt['converged']]
        assert bool(failures) == (report['state'] == 'failed')
        for attempt in failures:
            assert (path.parent/attempt['archive']).is_file()
            failed.append({'run': path.parent.name, 'target': attempt['target'], 'message': attempt['message'],
                           'archive': str((path.parent/attempt['archive']).relative_to(ROOT)), 'used_for_prediction': False})
        sequences.append({'run': path.parent.name, 'state': report['state'], 'accepted_rows': len(report['rows']),
                          'failed_attempts': len(failures), 'driver': driver.name, 'helper': helper.name})
    coarse = read('results/central-sequence/status.json')
    assert coarse['state'] == 'complete' and len(coarse['rows']) == 19
    assert all(row['spectrum']['frequency_squared'][0] > 0 for row in coarse['rows'])
    refined = read('results/signed-refinement/status.json')
    narrow = read('results/narrow-bracket/status.json')
    tangent = read('results/tangent-refinement/status.json')
    tangent_fine = read('results/tangent-fine/status.json')
    assert all(report['state'] == 'complete' for report in [refined, narrow, tangent, tangent_fine])
    assert len(refined['rows']) == 9 and len(narrow['rows']) == 6
    fine_spectra = []
    roots = []
    for cells in [512, 1024, 1536]:
        pair = [next(row for row in narrow['rows'] if row['central_target'] == center and row['spectrum']['cells'] == cells)
                for center in [1.982, 1.986]]
        values = [row['spectrum']['frequency_squared'][0] for row in pair]
        if cells >= 1024:
            assert values[0] > 0 > values[1]
        assert all(row['spectrum']['frequency_squared'][1] > .001 for row in pair)
        root = 1.982-values[0]*.004/(values[1]-values[0])
        roots.append({'cells': cells, 'linear_spectral_zero': root,
                      'inside_sample_pair': 1.982 < root < 1.986})
        if cells == 1536:
            fine_spectra = pair
    turning = read('results/turning-location/status.json')
    assert turning['state'] == 'complete'
    center = turning['selected_center']
    assert 1.982 < center < 1.986
    assert all(row['charge_second_derivative'] < 0 for row in turning['comparisons'])
    assert max(abs(row['charge_turning_center']-row['mass_turning_center']) for row in turning['comparisons']) < 2e-9
    assert turning['comparisons'][-1]['maximum_first_law_residual_over_window_derivative_scale'] < 1e-7
    tangent_rows = tangent['rows']+tangent_fine['rows']
    values = np.array([row['frequency_squared'][0] for row in tangent_rows])
    assert len(tangent_rows) == 4 and np.all(values > 0) and np.all(np.diff(values) < 0)
    last_tangent = tangent_rows[-1]['tangent_checks'][-1]
    assert last_tangent['overlap_with_lowest_mode'] > .9999999
    assert last_tangent['charge_tangency_error_over_absolute_density_variation'] < 2e-7
    assert max(row['maximum_scaled_eigen_equation_residual'] for row in tangent_rows) < .01
    for row in tangent_rows:
        checks = row['tangent_checks']
        assert 3.9 < checks[0]['charge_tangency_error_over_absolute_density_variation']/checks[1]['charge_tangency_error_over_absolute_density_variation'] < 4.1
    extrapolated_zero = (1536**2*roots[-1]['linear_spectral_zero']-1024**2*roots[-2]['linear_spectral_zero'])/(1536**2-1024**2)
    assert abs(extrapolated_zero-center) < 2e-5
    first_order = read('results/first-order-growth/status.json')
    assert first_order['state'] == 'complete' and first_order['relative_growth_rate_difference'] < 1e-5
    quadrature = read('results/quadrature/status.json')
    profile_control = read('results/profile-control/status.json')
    assert quadrature['state'] == profile_control['state'] == 'complete'
    quad_differences = []
    for row in quadrature['rows']:
        match = next(item for item in refined['rows'] if item['central_target'] == row['central_target'] and item['spectrum']['cells'] == row['spectrum']['cells'])
        delta = max(abs(np.array(row['spectrum']['frequency_squared'])-np.array(match['spectrum']['frequency_squared'])))
        quad_differences.append(float(delta))
    assert max(quad_differences) < 1e-9
    profile_row = profile_control['rows'][0]
    match = next(item for item in refined['rows'] if item['central_target'] == 2 and item['spectrum']['cells'] == 512)
    profile_delta = float(max(abs(np.array(profile_row['spectrum']['frequency_squared'])-np.array(match['spectrum']['frequency_squared']))))
    assert profile_delta < 1e-9
    refined_rows = refined['rows']+narrow['rows']+quadrature['rows']+profile_control['rows']
    for row in refined_rows:
        path = Path(row['profile_path'])
        if not path.is_absolute():
            path = ROOT/path
        assert digest(path) == row['profile_sha256']
        assert np.isfinite(row['spectrum']['frequency_squared']).all()
        assert row['spectrum']['maximum_scaled_eigen_equation_residual'] < .01
    report = {'state': 'complete', 'script_sha256': digest(Path(__file__)),
              'input_hashes': {str(path.relative_to(ROOT)): digest(path) for path in sources},
              'sequences': sequences, 'accepted_equilibrium_rows': len(accepted), 'failed_attempts_preserved': failed,
              'fixed_alpha': coarse['fixed_alpha'], 'refinement_spectral_calculations': len(refined_rows),
              'turning_tangent_spectral_calculations': len(tangent_rows), 'first_order_generator_checks': 1,
              'mass_charge_turning_center': center, 'resolved_spectral_bracket': [1.982, 1.986],
              'spectral_zero_estimates': roots, 'two_mesh_quadratic_extrapolated_spectral_zero': extrapolated_zero,
              'extrapolation_not_a_certified_bound': True, 'finest_bracket_spectra': fine_spectra,
              'turning_point_frequency_squared_refinement': values.tolist(), 'finest_tangent_check': last_tangent,
              'maximum_quadrature_absolute_frequency_squared_change': max(quad_differences),
              'maximum_profile_refinement_absolute_frequency_squared_change': profile_delta,
              'maximum_accepted_mass_quadrature_error': max(row['mass_quadrature_relative_error'] for row in accepted),
              'maximum_accepted_komar_error': max(row['komar_adm_relative_error_without_tiny_tail'] for row in accepted),
              'maximum_accepted_angular_second_derivative_residual': max(row['angular_Einstein_relative_residual'] for row in accepted),
              'maximum_fine_angular_second_derivative_residual': max(row['angular_Einstein_relative_residual'] for row in accepted if row['max_rms_residual'] < 3e-9),
              'coarse_positive_value_at_h2_superseded_by_refined_negative': True,
              'strong_tangent_operator_residual_certified_small': False,
              'continuum_or_nonlinear_stability_certified': False}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
