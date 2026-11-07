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

    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    labels = ['derivation', 'edge-weak-v2', 'pilot', 'coarse', 'fine', 'refined', 'limits', 'curvature-v2', 'tidal-mechanics']
    scripts = ['derive_tides.py', 'derive_edge_and_weak_limit_v2.py', *['solve_tides.py']*4, 'check_limits.py', 'test_curvature_v2.py', 'match_tidal_mechanics.py']
    paths = {label: ROOT/f'results/{label}/status.json' for label in labels}
    reports = {label: strict_json(path) for label, path in paths.items()}
    for label, script in zip(labels, scripts):
        report = reports[label]
        assert report['state'] == 'complete' and report['script_sha256'] == digest(ROOT/script)
        for mapping in ['source_hashes', 'input_hashes']:
            for path, expected in report.get(mapping, {}).items():
                assert digest(path) == expected
        if 'source_path' in report:
            assert digest(report['source_path']) == report['source_sha256']
    exact = 0
    for label, expected in [('derivation', 11), ('edge-weak-v2', 11), ('tidal-mechanics', 5)]:
        report = reports[label]
        assert len(report['checks']) == report['exact_check_count'] == expected
        assert all(row['passed'] for row in report['checks'])
        exact += expected
    curvature = reports['curvature-v2']
    assert curvature['compact_angular_constraint_exactly_verified']
    exact += 1
    assert len(curvature['rows']) == 16
    assert all(len(row['variations']) == 3 for row in curvature['rows'])
    small_step_curvature = max(row['variations'][-1]['normalized_linearized_einstein_residual'] for row in curvature['rows'])
    scalar_residual = max(row['scalar_equation_spline_residual'] for row in curvature['rows'])
    angular_residual = max(row['angular_constraint_finite_difference_residual'] for row in curvature['rows'])
    assert small_step_curvature < 4e-6 and scalar_residual < 2e-6 and angular_residual < 5e-7
    all_rows = []
    extraction_changes = []
    for label, count in [('pilot', 2), ('coarse', 7), ('fine', 7), ('refined', 3)]:
        report = reports[label]
        assert len(report['rows']) == count
        assert report['derivation_sha256'] == digest(paths['derivation'])
        assert report['edge_weak_sha256'] == digest(paths['edge-weak-v2'])
        assert report['parent_seal_sha256'] == digest(ROOT.parent/'quadrupole-response-20261004/results/stage-integrity.json')
        for row in report['rows']:
            assert row['converged'] and row['maximum_rms_residual'] < 1.01*report['arguments']['tolerance']
            assert row['maximum_boundary_residual'] < 1e-10
            assert digest(row['profile_path']) == row['profile_sha256']
            assert (paths[label].parent/row['archive']).is_file()
            assert abs(row['growing_coefficient']+2) < 1e-10
            assert 0 <= row['surface_compactness'] < .031
            if row['alpha'] > 0:
                assert row['geometric_tidal_lambda'] > 0 and row['k2'] > 0 and row['dimensionless_Lambda'] > 0
                assert abs(row['k2']/(1.5*row['geometric_tidal_lambda']/row['radius']**5)-1) < 1e-12
                for control in row['exterior_controls']:
                    extraction_changes.append(abs(control['decaying_coefficient']/row['decaying_coefficient']-1))
            else:
                assert abs(row['decaying_coefficient'])/row['radius']**5 < 1e-12
                assert row['dimensionless_Lambda'] is None
            assert all(control['growing_relative_change'] < 1e-10 for control in row['exterior_controls'])
        all_rows.extend(report['rows'])
    assert max(extraction_changes) < 1e-6
    limits = reports['limits']
    assert limits['weak_limit']['relative_extrapolation_difference'] < 1e-6
    assert .03 < limits['weak_limit']['metric_contribution_fraction_of_total'] < .05
    assert limits['flat_limit']['relative_scalar_profile_l2_difference'] < 1e-8
    assert limits['flat_limit']['relative_edge_amplitude_difference'] < 1e-7
    assert limits['flat_limit']['maximum_normalized_metric_difference'] < 1e-12
    assert limits['maximum_wronskian_relative_error'] < 1e-12
    coarse_changes = [row['relative_lambda_change'] for row in limits['mesh_rows'] if row['relative_lambda_change'] is not None]
    assert max(coarse_changes) < 1e-7
    third_changes = []
    for row in reports['refined']['rows']:
        earlier = next(entry for entry in reports['fine']['rows'] if entry['alpha'] == row['alpha'])
        if row['alpha'] > 0:
            third_changes.append(abs(row['geometric_tidal_lambda']/earlier['geometric_tidal_lambda']-1))
    assert max(third_changes) < 1e-8
    mechanics = reports['tidal-mechanics']
    assert len(mechanics['rows']) == 4
    assert not mechanics['gravitating_quadrupole_gap_calculated'] and not mechanics['physical_scale_fitted']
    for row in mechanics['rows']:
        assert 0 < row['static_tidal_energy_over_newtonian_magnitude'] < 1e-6
        assert 0 < row['maximum_surface_displacement_over_radius'] < .001
        assert not row['binary_time_dependence_or_resonance_tested']
    for first, second in zip(mechanics['rows'][:-1], mechanics['rows'][1:]):
        assert abs(first['static_tidal_energy_over_newtonian_magnitude']/second['static_tidal_energy_over_newtonian_magnitude']-32) < 1e-10
        assert abs(first['maximum_surface_displacement_over_radius']/second['maximum_surface_displacement_over_radius']-8) < 1e-10
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            assert np.all(np.diff(archive['spline_knots']) > 0)
            for key in archive.files:
                assert np.isfinite(archive[key]).all(), (path, key)
        archives.append(path.relative_to(ROOT).as_posix())
    assert len(archives) == 19
    assert (ROOT/'results/edge-weak/INTERRUPTED.md').is_file()
    assert (ROOT/'results/curvature/FAILED.md').is_file()
    assert not (ROOT/'results/edge-weak/status.json').exists()
    assert not (ROOT/'results/curvature/status.json').exists()
    result = {'state': 'complete', 'script_sha256': digest(__file__),
              'input_hashes': {path.relative_to(ROOT).as_posix(): digest(path) for path in paths.values()},
              'exact_identity_checks': exact, 'primary_fine_solutions': 7, 'third_resolution_controls': 3,
              'all_tidal_solutions_including_pilot': len(all_rows), 'exterior_extraction_controls': 4*len(all_rows),
              'finite_perturbation_curvature_tests': 48, 'static_mechanics_examples': 4,
              'maximum_fine_coarse_lambda_relative_change': max(coarse_changes),
              'maximum_third_resolution_lambda_relative_change': max(third_changes),
              'maximum_exterior_decaying_coefficient_relative_change': max(extraction_changes),
              'weak_limit_relative_extrapolation_difference': limits['weak_limit']['relative_extrapolation_difference'],
              'maximum_small_step_nonlinear_ricci_test_residual': small_step_curvature,
              'maximum_scalar_spline_equation_residual': scalar_residual,
              'maximum_angular_constraint_derivative_residual': angular_residual,
              'finite_archives': archives, 'preserved_excluded_attempts': ['edge-weak symbolic expansion stopped', 'curvature symbolic-name parser failure'],
              'static_einstein_scalar_tidal_matching_completed': True,
              'nonradial_time_evolution_or_resonance_spectrum_computed': False,
              'global_gravitational_frequency_gap_claimed': False,
              'newton_constant_or_physical_units_fitted': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
