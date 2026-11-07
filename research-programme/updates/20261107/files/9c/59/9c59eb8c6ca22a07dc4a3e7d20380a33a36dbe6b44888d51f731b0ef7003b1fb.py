from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.interpolate import PPoly

from dynamic_system import BRANCH, DynamicProblem, Profile, ROOT


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(values):
        answer = {}
        for key, value in values:
            assert key not in answer, (path, key)
            answer[key] = value
        return answer

    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    modes = ['mode-coarse', 'mode-edge002', 'mode-edge004', 'mode-main-real', 'mode-weak001', 'mode-weak0001-real']
    reports = {label: strict_json(ROOT/f'results/{label}/status.json') for label in modes+['derivation-v3', 'reduction', 'compact-constraint', 'flat-mode', 'edge-vacuum', 'dynamic-curvature', 'pilot', 'low-frequency', 'solver-comparison']}
    checks = []

    def check(name, passed):
        assert passed, name
        checks.append({'name': name, 'passed': True})

    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for label, report in reports.items():
        check('complete_and_script_owned_'+label, report['state'] == 'complete' and report['script_sha256'] in script_hashes)
        if 'system_sha256' in report:
            check('current_system_'+label, report['system_sha256'] == digest(ROOT/'dynamic_system.py'))
        for key in ['profile_path', 'previous_spectrum_path', 'parent_edge_path']:
            if key in report:
                check('source_'+label+'_'+key, Path(report[key]).is_file() and digest(report[key]) == report[key.replace('_path', '_sha256')])
    exact_count = 0
    for label, key in [('derivation-v3', 'checks'), ('reduction', 'checks'), ('compact-constraint', 'checks'), ('edge-vacuum', 'exact_checks')]:
        check('all_exact_'+label, all(row['passed'] for row in reports[label][key]))
        exact_count += len(reports[label][key])
    check('exact_count', exact_count == 30)
    for label in ['pilot', 'low-frequency']:
        check('all_interior_'+label, all(row['converged'] and row['boundary_residual'] < 1e-7 for row in reports[label]['rows']))
    parent = strict_json(BRANCH/'gravitating-tides-20261004/results/refined/status.json')
    static_value = next(row['geometric_tidal_lambda'] for row in parent['rows'] if row['nominal_flat_compactness'] == .03)
    recovered = reports['low-frequency']['rows'][0]['static_basis_lambda_diagnostic']
    static_error = abs(recovered/static_value-1)
    check('static_tidal_limit', static_error < 3e-8)
    flat_source = strict_json(reports['flat-mode']['previous_spectrum_path'])
    flat_reference = next(row['frequencies'][0] for row in flat_source['rows'] if 19 < row['radius'] < 21)
    flat_frequency = reports['flat-mode']['sigma']
    check('flat_gyro_independent_agreement', abs(flat_frequency/flat_reference-1) < 3e-8)
    reference = reports['mode-edge004']
    real_reference, imag_reference = reference['sigma']['real'], reference['sigma']['imaginary']
    mode_controls = []
    for label in modes:
        report = reports[label]
        check('outgoing_root_'+label, report['sigma']['real'] > 0 and report['sigma']['imaginary'] < 0 and np.linalg.norm(report['mismatch_times_radius']) < 1e-8)
        check('no_box_'+label, report['zero_frequency_continuum_present'] and not report['finite_outer_box_eigencondition_used'])
        check('interior_convergence_'+label, max(row['maximum_rms_residual'] for row in report['iterations']) <= report['arguments']['tolerance']*1.0001)
        if report['arguments']['nominal'] == .03:
            real_error, imag_error = abs(report['sigma']['real']/real_reference-1), abs(report['sigma']['imaginary']/imag_reference-1)
            check('real_frequency_resolution_'+label, real_error < 3e-9)
            check('radiation_width_resolution_'+label, imag_error < 2e-6)
            mode_controls.append({'label': label, 'frequency_relative_difference': real_error, 'width_relative_difference': imag_error})
    curvature = reports['dynamic-curvature']
    curvature_maxima = {key: max(row['variations'][-1][key] for row in curvature['rows']) for key in ['einstein_residual', 'scalar_residual', 'current_residual']}
    check('independent_nonlinear_tensor_and_field_tests', max(curvature_maxima.values()) < 1e-5)
    for row in curvature['input_sources']:
        check('curvature_source_'+Path(row['path']).name, digest(row['path']) == row['sha256'])
    edges = reports['edge-vacuum']
    check('static_endpoint_replay', max(row['relative_static_edge_difference'] for row in edges['static_edge_checks']) < 1e-12)
    check('outgoing_vacuum_controls', max(row['absolute_logarithmic_derivative_error'] for row in edges['vacuum_checks']) < 1e-10)
    for compactness in [0., .03]:
        rows = [row for row in edges['dynamic_edge_residuals'] if row['compactness'] == compactness]
        check('phase_edge_quadratic_remainder_'+str(compactness), all(3.8 < before['phase_equation_residual']/after['phase_equation_residual'] < 4.2 for before, after in zip(rows, rows[1:])))
        check('amplitude_edge_small_remainder_'+str(compactness), rows[-1]['amplitude_equation_residual'] < 1e-10)
    weak_large, weak_small = reports['mode-weak001'], reports['mode-weak0001-real']
    ratio = weak_large['alpha']/weak_small['alpha']
    extrapolated = (ratio*weak_small['sigma']['real']-weak_large['sigma']['real'])/(ratio-1)
    extrapolation_error = abs(extrapolated/flat_frequency-1)
    check('weak_gravity_extrapolation_to_flat_mode', extrapolation_error < 1e-6)
    dimensionless_denominators = []
    overlaps = []
    flat_archive = np.load(ROOT/'results/flat-mode/mode.npz')
    flat_spline = PPoly.construct_fast(flat_archive['spline_coefficients'], flat_archive['spline_knots'], axis=1)
    nodes, weights = np.polynomial.legendre.leggauss(240)
    coordinate = (nodes+1)/2*.99
    weights = weights*.99/2*coordinate**2
    flat_amplitude = flat_spline(coordinate)[0]
    for label in ['mode-edge004', 'mode-weak001', 'mode-weak0001-real']:
        report = reports[label]
        profile = Profile(20., report['arguments']['nominal'])
        problem = DynamicProblem(profile, complex(report['sigma']['real'], report['sigma']['imaginary']))
        position = profile.radius*np.linspace(.0001, .999, 2000)
        field, gradient, metric, lapse2, energy, energy_prime, energy_second, rotation, lapse_prime, first = problem.background(position)
        denominator = (7-3*metric+profile.alpha*position**2*(3*metric*gradient**2-rotation*field**2-2*energy))/4
        check('regular_metric_constraint_'+label, np.min(denominator) > .5)
        dimensionless_denominators.append({'label': label, 'minimum_D_H': float(np.min(denominator))})
        archive = np.load(ROOT/f'results/{label}/mode.npz')
        spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        amplitude = spline(coordinate)[2]
        overlap = abs(np.sum(weights*flat_amplitude*amplitude))/np.sqrt(np.sum(weights*flat_amplitude**2)*np.sum(weights*abs(amplitude)**2))
        check('flat_shape_continuation_overlap_'+label, overlap > .99)
        overlaps.append({'label': label, 'normalized_radial_amplitude_overlap_with_flat': float(overlap)})
    orbital_rows = []
    for separation in [10., 20., 40.]:
        distance = separation*reference['radius']
        orbital_frequency = np.sqrt(2*reference['geometric_mass']/distance**3)
        orbital_rows.append({'separation_over_radius': separation, 'leading_equal_mass_orbital_frequency': orbital_frequency,
                             'quadrupole_drive_frequency': 2*orbital_frequency, 'drive_over_computed_mode_frequency': 2*orbital_frequency/real_reference,
                             'timescale_comparison_only_not_a_full_response_error_bound': True})
    excluded = ['derivation', 'derivation-v2', 'mode-pilot', 'mode-fine', 'mode-refined', 'mode-weak0001', 'mode-weak0001-scaled']
    for label in excluded:
        check('preserved_excluded_'+label, (ROOT/f'results/{label}/FAILED.md').is_file())
        path = ROOT/f'results/{label}/status.json'
        if path.is_file():
            check('excluded_not_promoted_'+label, strict_json(path)['state'] == 'failed')
    check('failed_precision_controls_recorded', all(not row['converged'] for row in reports['solver-comparison']['rows']))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_bytecode_cache', not list(ROOT.rglob('__pycache__')))
    result = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks,
              'input_hashes': {path.relative_to(ROOT).as_posix(): digest(path) for path in ROOT.rglob('*') if path.is_file() and path.suffix in ['.json', '.npz']},
              'exact_identity_checks': exact_count, 'accepted_interior_real_frequency_solutions': sum(len(reports[label]['rows']) for label in ['pilot', 'low-frequency']),
              'accepted_outgoing_mode_controls': len(modes), 'accepted_mode_solver_evaluations': sum(len(reports[label]['iterations']) for label in modes),
              'independent_flat_collocation_frequency': flat_frequency, 'previous_flat_frequency': flat_reference,
              'weak_gravity_extrapolated_frequency': extrapolated, 'weak_extrapolation_relative_difference': extrapolation_error,
              'static_lambda_recovered': recovered, 'previous_static_lambda': static_value, 'static_limit_relative_difference': static_error,
              'main_mode': reference['sigma'], 'mode_resolution_controls': mode_controls, 'main_quality_factor': reference['quality_factor'],
              'main_amplitude_damping_time': reference['damping_amplitude_time'], 'main_oscillation_period': 2*np.pi/real_reference,
              'amplitude_e_folding_in_cycles': -real_reference/(2*np.pi*imag_reference),
              'constraint_denominators': dimensionless_denominators, 'mode_shape_overlaps': overlaps,
              'finite_nonlinear_tests': len(curvature['rows'])*3, 'finite_test_small_step_maxima': curvature_maxima,
              'static_edge_replays': len(edges['static_edge_checks']), 'vacuum_outgoing_controls': len(edges['vacuum_checks']),
              'orbital_timescale_examples': orbital_rows, 'preserved_excluded_attempts': excluded,
              'solver_comparison_nonconverged_control_count': 2, 'compiled_scripts': sorted(compiled),
              'global_gravitational_gap_claimed': False, 'finite_frequency_Love_or_full_binary_error_bound_claimed': False,
              'physical_units_or_Newton_constant_fitted': False}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ['checks', 'input_hashes', 'compiled_scripts']}, indent=2))


if __name__ == '__main__':
    main()
