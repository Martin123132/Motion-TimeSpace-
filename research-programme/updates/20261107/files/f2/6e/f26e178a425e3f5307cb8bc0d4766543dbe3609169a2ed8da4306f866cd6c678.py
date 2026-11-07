from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, (path, key)
            result[key] = value
        return result

    def reject(value):
        raise ValueError(value)

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    labels = ['derivation', 'pilot', 'quadratic-convergence', 'quadratic-fine', 'quadratic-gyro',
              'static-bvp', 'static-bvp-tight', 'finite-energy', 'surface-limit']
    paths = {label: ROOT/f'results/{label}/status.json' for label in labels}
    reports = {label: strict_json(path) for label, path in paths.items()}
    scripts = ['derive_shape.py', 'solve_shape.py', 'solve_shape_v2.py', 'solve_shape_v2.py', 'solve_shape_v2.py',
               'solve_static_bvp.py', 'solve_static_bvp.py', 'test_tidal_energy.py', 'check_surface_limit.py']
    for label, script in zip(labels, scripts):
        report = reports[label]
        assert report['script_sha256'] == digest(ROOT/script)
        assert report['state'] == ('failed' if label == 'static-bvp-tight' else 'complete')
        for row in report.get('rows', []):
            for stem in ['profile', 'archive']:
                if f'{stem}_path' in row:
                    assert digest(row[f'{stem}_path']) == row[f'{stem}_sha256']
            if 'archive' in row:
                assert (paths[label].parent/row['archive']).is_file()
        for path, expected in report.get('input_hashes', {}).items():
            assert digest(path) == expected
    for label in ['quadratic-convergence', 'quadratic-fine', 'quadratic-gyro']:
        assert reports[label]['elements_sha256'] == digest(ROOT/'shape_elements.py')
    for label in ['pilot', 'quadratic-convergence', 'quadratic-fine', 'quadratic-gyro']:
        assert reports[label]['parent_seal_sha256'] == digest(ROOT.parent/'collective-motion-20261004/results/stage-integrity.json')
    derivation = reports['derivation']
    assert digest(derivation['edge_parent_path']) == derivation['edge_parent_sha256']
    for label in ['static-bvp', 'static-bvp-tight']:
        assert reports[label]['edge_derivation_sha256'] == digest(paths['derivation'])
    energy = reports['finite-energy']
    assert digest(energy['source_path']) == energy['source_sha256']
    assert energy['helper_sha256'] == digest(ROOT/'solve_static_bvp.py')
    exact_count = 0
    for label, count in [('derivation', 9), ('surface-limit', 4)]:
        assert reports[label]['exact_check_count'] == len(reports[label]['checks']) == count
        assert all(row['passed'] for row in reports[label]['checks'])
        exact_count += count
    numerical_checks = []
    fine = reports['quadratic-fine']['rows']
    coarse = reports['quadratic-convergence']['rows']
    static = reports['static-bvp']['rows']
    assert len(fine) == 3 and len(coarse) == 9 and len(static) == 9
    for row in fine:
        radius = row['radius']
        sequence = sorted([entry for entry in coarse if entry['radius'] == radius]+[row], key=lambda value: value['cells'])
        assert [entry['cells'] for entry in sequence] == [64, 128, 256, 512]
        translation = [abs(entry['translation_static_eigenvalue']) for entry in sequence]
        assert all(first > second for first, second in zip(translation[:-1], translation[1:]))
        assert translation[-1] < 1e-8 and row['translation_mode_overlap'] > .99999999
        assert row['static_eigenvalues'][0] >= 4/radius**2
        assert row['phase_stiffness_minimum'] >= 6/radius**2
        assert row['frequencies'][0] > row['analytic_frequency_lower_bound'] > 0
        assert 0 < row['susceptibility'] < row['susceptibility_upper_bound']
        assert row['linear_solve_relative_residual'] < 1e-8
        sources = [entry for entry in static if entry['radius'] == radius]
        assert len(sources) == 3 and all(entry['converged'] for entry in sources)
        assert max(entry['maximum_rms_residual'] for entry in sources) < 2.01e-9
        assert max(entry['maximum_boundary_residual'] for entry in sources) < 1e-12
        reference = next(entry for entry in sources if entry['cutoff_distance'] == .005)
        difference = abs(row['susceptibility']/reference['susceptibility']-1)
        cutoff_change = max(abs(entry['susceptibility']/reference['susceptibility']-1) for entry in sources)
        edge_change = max(abs(entry['edge_amplitude']/reference['edge_amplitude']-1) for entry in sources)
        frequency_change = abs(row['frequencies'][0]/sequence[-2]['frequencies'][0]-1)
        assert difference < 2e-6 and cutoff_change < 1e-8 and edge_change < 1e-6
        assert frequency_change < 1e-5
        numerical_checks.append({'radius': radius, 'finite_element_bvp_relative_difference': difference,
                                 'last_frequency_mesh_relative_change': frequency_change,
                                 'bvp_cutoff_susceptibility_relative_change': cutoff_change,
                                 'bvp_cutoff_edge_amplitude_relative_change': edge_change,
                                 'translation_final_stiffness': row['translation_static_eigenvalue']})
    gyro = [row['independent_gyro_check'] for row in reports['quadratic-gyro']['rows']]
    assert len(gyro) == 3
    assert max(row['maximum_relative_frequency_difference'] for row in gyro) < 1e-6
    assert max(row['maximum_absolute_real_part'] for row in gyro) < 1e-10
    assert len(energy['rows']) == 6
    energy_quadrature_changes = []
    for row in energy['rows']:
        assert row['background_charge_relative_error'] < 1e-9
        assert len(row['tests']) == 4
        assert all(entry['symmetric_energy_difference'] < 0 and entry['charge_relative_error'] < 1e-12 for entry in row['tests'])
        errors = [entry['relative_difference'] for entry in row['tests']]
        assert all(first > 3*second for first, second in zip(errors[:-1], errors[1:]))
        assert errors[-1] < .005
        if row['radial_cells'] == 2048:
            earlier = next(entry for entry in energy['rows'] if entry['radius'] == row['radius'] and entry['radial_cells'] == 1024)
            energy_quadrature_changes.extend(abs(first['relative_difference']-second['relative_difference'])
                                             for first, second in zip(earlier['tests'], row['tests']))
    assert max(energy_quadrature_changes) < 1e-5
    surface = reports['surface-limit']
    assert .18 < surface['dimensionless_tension_from_same_potential'] < .181
    assert surface['quadrature_error_estimate'] < 1e-11
    assert len(surface['rows']) == 3
    for key in ['field_over_liquid_susceptibility', 'field_over_liquid_frequency']:
        errors = [abs(row[key]-1) for row in surface['rows']]
        assert all(first > second for first, second in zip(errors[:-1], errors[1:]))
    assert abs(surface['rows'][-1]['field_over_liquid_frequency']-1) < .01
    assert abs(surface['rows'][-1]['field_over_liquid_susceptibility']-1) < .04
    tight = reports['static-bvp-tight']
    assert len(tight['rows']) == 2 and 'maximum number of mesh nodes' in tight['error']
    failed_archive = ROOT/'results/static-bvp-tight/R80-d0.005-t2e-10.npz'
    with np.load(failed_archive) as archive:
        assert max(archive['rms_residuals']) > tight['arguments']['tolerance']
        failed_maximum = float(max(archive['rms_residuals']))
        failed_nodes = len(archive['mesh'])
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            for key in archive.files:
                assert np.isfinite(archive[key]).all(), (path, key)
            if 'spline_knots' in archive:
                assert np.all(np.diff(archive['spline_knots']) > 0)
            if 'nodal_position' in archive:
                assert np.all(np.diff(archive['nodal_position']) > 0)
        archives.append(str(path.relative_to(ROOT)))
    result = {'state': 'complete', 'script_sha256': digest(__file__),
              'input_hashes': {str(path.relative_to(ROOT)): digest(path) for path in paths.values()},
              'exact_identity_checks': exact_count, 'flat_backgrounds': 3,
              'spectral_rows_including_pilot_and_gyro_controls': 18,
              'primary_quadratic_spectral_rows': 12, 'independent_quadratic_gyro_checks': 3,
              'primary_static_bvp_rows': 9, 'finite_energy_tests': 24,
              'numerical_checks': numerical_checks, 'finite_archives': archives,
              'maximum_independent_gyro_relative_difference': max(row['maximum_relative_frequency_difference'] for row in gyro),
              'maximum_fine_small_step_energy_relative_error': max(row['tests'][-1]['relative_difference'] for row in energy['rows'] if row['radial_cells'] == 2048),
              'maximum_energy_quadrature_change_in_relative_error': max(energy_quadrature_changes),
              'excluded_tight_attempt': {'state': 'failed_at_R80', 'two_completed_rows_preserved_as_secondary_only': True,
                                        'failed_archive': str(failed_archive), 'failed_nodes': failed_nodes, 'failed_maximum_rms_residual': failed_maximum},
              'analytic_flat_angular_bound_conditional_on_monotone_solution_and_energy_domain': True,
              'computed_full_self_gravitating_love_number': False,
              'computed_self_gravitating_quadrupole_frequency': False,
              'calibrated_physical_units': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
