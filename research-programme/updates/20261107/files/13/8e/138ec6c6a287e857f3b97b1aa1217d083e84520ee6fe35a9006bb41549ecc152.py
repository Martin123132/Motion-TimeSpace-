from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import psutil
from scipy.interpolate import PPoly

from response_system_v2 import DynamicProblem, Profile, determinant, outgoing_state
from response_system_v3 import ROOT, BRANCH, encode


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(values):
        result = {}
        for key, value in values:
            assert key not in result, (path, key)
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    labels = ['derivation', 'radiation-law', 'response', 'residue', 'low-frequency', 'controls']
    reports = {label: strict_json(ROOT/f'results/{label}/status.json') for label in labels}
    checks = []

    def check(name, condition):
        assert condition, name
        checks.append({'name': name, 'passed': True})

    scripts = {digest(path) for path in ROOT.glob('*.py')}
    for label, report in reports.items():
        check('complete_script_owned_'+label, report['state'] == 'complete' and report['script_sha256'] in scripts)
        if 'system_sha256' in report:
            check('current_system_'+label, report['system_sha256'] in scripts)
        for key in ['parent_pole_path', 'residue_path']:
            if key in report:
                check('unchanged_source_'+label+'_'+key, Path(report[key]).is_file() and digest(report[key]) == report[key.replace('_path', '_sha256')])
    for label in ['derivation', 'radiation-law']:
        check('all_recorded_algebra_'+label, all(row['passed'] for row in reports[label]['checks']))
    check('recorded_algebra_count', sum(len(reports[label]['checks']) for label in ['derivation', 'radiation-law']) == 17)
    scan, residue, low, controls = (reports[key] for key in ['response', 'residue', 'low-frequency', 'controls'])
    evaluated = scan['rows']+residue['evaluations']+low['evaluations']+controls['main_evaluations']+controls['alternate_evaluations']
    check('stored_interior_residuals', all(row['interior_maximum_residual'] < 2.01e-8 and row['interior_boundary_residual'] < 1e-7 for row in evaluated))
    check('finite_evaluations', all(np.isfinite(decode(row['susceptibility'])) for item in evaluated for row in item['rows']))
    check('Green_rank_one_identity', max(row['green_identity_error'] for item in evaluated for row in item['rows']) < 2e-11)
    real_evaluations = [item for item in evaluated if decode(item['sigma']).imag == 0]
    check('optical_identity', max(row['optical_identity_scaled_error'] for item in real_evaluations for row in item['rows']) < 1e-10)
    check('nonnegative_radiative_response', all(decode(row['susceptibility']).imag >= 0 for item in real_evaluations for row in item['rows']))
    static = [decode(row['susceptibility']).real for row in low['evaluations'][0]['rows']]
    static_source_path = BRANCH/'gravitating-tides-20261004/results/refined/status.json'
    static_source = strict_json(static_source_path)
    reference = next(row['geometric_tidal_lambda'] for row in static_source['rows'] if row['nominal_flat_compactness'] == .03)
    static_error = abs(static[0]/reference-1)
    check('recovered_static_tidal_response', static_error < 3e-8)
    check('static_matching_radius_independence', np.ptp(static)/static[0] < 1e-11)
    profile = Profile(20., .03)
    replay_errors = []
    for index, row in enumerate(scan['rows']):
        archive = ROOT/'results/response'/row['archive']
        with np.load(archive, allow_pickle=False) as arrays:
            check('finite_archive_'+str(index), all(np.all(np.isfinite(arrays[key])) for key in arrays.files))
            spline = PPoly(arrays['spline_coefficients'], arrays['spline_knots'])
            parameters = arrays['parameters'].copy()
        sigma = decode(row['sigma'])
        problem = DynamicProblem(profile, sigma, .02, 2e-8)
        solution = SimpleNamespace(p=parameters, sol=spline)
        boundary = problem.boundary(spline(spline.x[0]), spline(spline.x[-1]), parameters)
        check('archive_boundary_'+str(index), max(abs(boundary)) < 1e-7)
        _, _, master, derivative = problem.surface(solution)
        outgoing, _ = outgoing_state(profile.radius, profile.alpha*profile.mass, sigma)
        replay = master*outgoing[0]/determinant(np.array([master, derivative]), outgoing)
        replay_errors.append(abs(replay/decode(row['rows'][0]['total_green_surface_surface'])-1))
    check('archive_surface_response_replay', max(replay_errors) < 1e-12)
    circle_coarse, circle_fine = residue['contour_controls']
    circle_errors = [abs(decode(first)/decode(second)-1) for first, second in zip(circle_coarse['residues'], circle_fine['residues'])]
    check('contour_residue_convergence', max(circle_errors) < 1e-8)
    check('contour_Green_residue_convergence', abs(decode(circle_coarse['surface_green_residue'])/decode(circle_fine['surface_green_residue'])-1) < 1e-8)
    derivative_coarse, derivative_fine = residue['derivative_controls'][-2:]
    richardson = [(4*decode(fine)-decode(coarse))/3 for coarse, fine in zip(derivative_coarse['residues'], derivative_fine['residues'])]
    derivative_errors = [abs(value/decode(target)-1) for value, target in zip(richardson, circle_fine['residues'])]
    check('independent_derivative_contour_agreement', max(derivative_errors) < 2e-8)
    alternate_coarse, alternate_fine = controls['alternate_pole_derivative_controls']
    alternate = [(4*decode(fine)-decode(coarse))/3 for coarse, fine in zip(alternate_coarse['residues'], alternate_fine['residues'])]
    alternate_errors = [abs(value/decode(target)-1) for value, target in zip(alternate, circle_fine['residues'])]
    check('alternate_join_outer_residue_control', max(alternate_errors) < 5e-7)
    for index, row in enumerate(controls['flat_outgoing_controls']):
        check('flat_exact_real_'+str(index), row['real_logarithm_relative_error'] < 1e-10)
        check('flat_exact_imaginary_'+str(index), row['imaginary_logarithm_relative_error'] < 1e-9)
    check('fixed_basis_extraction_independence', max(row['coefficient_scaled_error'] for row in controls['fixed_basis_extraction_controls']) < 1e-11)
    check('Wronskian_transport', max(row['Wronskian_relative_error'] for row in controls['fixed_basis_extraction_controls']) < 1e-10)
    check('source_continuity', max(row['continuity_absolute_error'] for row in controls['independent_source_jump_controls']) < 1e-10)
    check('source_unit_jump', max(row['jump_absolute_error'] for row in controls['independent_source_jump_controls']) < 1e-10)
    check('independent_source_matching', max(row['independent_source_match_relative_error'] for row in controls['independent_source_jump_controls']) < 1e-8)
    for index, row in enumerate(controls['precision_controls']):
        tolerance = 3e-5 if row['sigma'] > .02 else 3e-7
        check('interior_exterior_precision_'+str(index), max(row['susceptibility_relative_differences']+row['shell_relative_differences']) < tolerance)
        check('imaginary_precision_'+str(index), max(row['imaginary_susceptibility_relative_differences']) < 5e-7)
    quadratic_errors = []
    for index, row in enumerate(low['buffer_response_decomposition']):
        values = [item['quadratic_coefficient'] for item in row['quadratic_controls']]
        quadratic_errors.append(np.ptp(values)/abs(values[0]))
        check('low_frequency_quadratic_resolution_'+str(index), quadratic_errors[-1] < 1e-6)
        check('static_pole_remainder_accounting_'+str(index), abs(row['pole_pair_static_contribution']+row['regular_remainder_static']-row['lambda_static']) < 1e-8)
        check('quadratic_pole_remainder_accounting_'+str(index), abs(row['pole_pair_quadratic_contribution']+row['regular_remainder_quadratic']-values[0]) < 1e-5)
    for buffer_index in range(3):
        values = [row['inverse_radiation_coefficient_by_buffer'][buffer_index] for row in low['radiation_controls']]
        check('fifth_power_inverse_coefficient_'+str(buffer_index), abs(values[0]/.4-1) < 1e-4 and all(abs(first-.4) < abs(second-.4) for first, second in zip(values, values[1:])))
    check('fifth_power_response_loss', abs(low['radiation_controls'][0]['loss_over_static_lambda_squared_sigma_fifth'][0]/.4-1) < 2e-4)
    for index, row in enumerate(low['source_owned_benchmarks']):
        check('heldout_source_prediction_'+str(index), row['quadratic_green_prediction_relative_error'] < 1e-5)
        check('heldout_susceptibility_prediction_'+str(index), row['quadratic_susceptibility_prediction_relative_error'] < 1e-6)
    check('preliminary_precision_exclusion_documented', (ROOT/'results/pilot/LOW_FREQUENCY_IMAGINARY_PRECISION.md').is_file())
    pole = decode(residue['pole'])
    cancellation = []
    for fraction, value in zip([2., 3., 4.], circle_fine['residues']):
        strength = decode(value)
        cancellation.append({'buffer_over_radius': fraction, 'pole_imaginary_linear': -2*(strength/pole**2).imag,
                             'pole_imaginary_cubic': -2*(strength/pole**4).imag,
                             'required_remainder_imaginary_linear': 2*(strength/pole**2).imag,
                             'required_remainder_imaginary_cubic': 2*(strength/pole**4).imag})
    inputs = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path.suffix in ['.py', '.json', '.npz'] and output not in path.parents}
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': inputs,
              'accepted_interior_evaluations': 61, 'retained_pilot_interior_evaluations': 11,
              'recorded_algebra_checks': 17, 'substantive_algebra_checks': 14,
              'elementary_residue_sign_coefficient_bookkeeping_checks': 3,
              'static_source_path': str(static_source_path), 'static_source_sha256': digest(static_source_path),
              'static_limit_relative_error': static_error, 'archive_replay_errors': replay_errors,
              'contour_relative_errors': circle_errors, 'derivative_contour_relative_errors': derivative_errors,
              'alternate_residue_relative_errors': alternate_errors, 'quadratic_resolution_relative_errors': quadratic_errors,
              'pole_remainder_low_frequency_cancellations': cancellation,
              'pole': encode(pole), 'surface_Green_residue': circle_fine['surface_green_residue'],
              'scope': 'Finite-grid and asymptotic/numerical controls. Green source is a specified Zerilli delta jump, not yet a companion stress tensor. Matching-scheme coefficients are not standalone physical EFT parameters.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'static_error': static_error,
                      'derivative_residue_errors': derivative_errors, 'alternate_residue_errors': alternate_errors,
                      'cancellation': cancellation}))


if __name__ == '__main__':
    main()
