from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import psutil
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

from axial_system import ROOT, BRANCH, AxialProblem, Profile, Quadrature, basis


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, (path, key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def published_kappa(compactness, logarithmic_derivative):
    compactness, logarithmic_derivative = mp.mpf(str(compactness)), mp.mpf(str(logarithmic_derivative))
    numerator = 2*compactness*(logarithmic_derivative-2)-logarithmic_derivative+3
    denominator = 2*compactness*(2*compactness**3*(logarithmic_derivative+1)+2*compactness**2*logarithmic_derivative
                                +3*compactness*(logarithmic_derivative-1)-3*logarithmic_derivative+9)
    denominator += 3*numerator*mp.log(1-2*compactness)
    return mp.mpf(8)/5*numerator/denominator


def independent_riccati(problem):
    start = 2e-6
    initial = [2*problem.center_coefficient*(problem.radius*start)**2]

    def equation(coordinate, state):
        density, pressure, mass, metric = problem.background(coordinate)
        radial = problem.radius*coordinate
        return [(8*mass/(radial*metric)-5*state[0]-problem.alpha*state[0]**2
                 +radial**2*(density+pressure)/metric*(1+problem.alpha*state[0]))/coordinate]

    solution = solve_ivp(equation, [start, 1.], initial, rtol=2e-12, atol=1e-13, max_step=1/260, method='DOP853')
    assert solution.success
    scaled_logarithm = solution.y[0, -1]
    exterior = basis(1., problem.compactness)
    normalized = ((1-problem.compactness)*scaled_logarithm-2*problem.profile.mass/problem.radius)
    normalized /= exterior[1, 1]-exterior[0, 1]*(3+problem.alpha*scaled_logarithm)
    return float(normalized*problem.radius**5)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(parents=True, exist_ok=False)
    mp.mp.dps = 80
    fine, coarse = [strict_json(ROOT/f'results/{label}/status.json') for label in ['fine', 'coarse']]
    derivation = strict_json(ROOT/'results/derivation/status.json')
    matching = strict_json(ROOT/'results/matching/status.json')
    checks, input_hashes = [], {}

    def check(name, passed):
        assert passed, name
        checks.append({'name': name, 'passed': True})

    scripts = {digest(path) for path in ROOT.glob('*.py')}
    for name, report in [('fine', fine), ('coarse', coarse), ('derivation', derivation), ('matching', matching)]:
        path = ROOT/f'results/{name}/status.json'
        input_hashes[path.relative_to(ROOT).as_posix()] = digest(path)
        check('complete_and_source_owned_'+name, report['state'] == 'complete' and report['script_sha256'] in scripts)
        if 'system_sha256' in report:
            check('current_axial_system_'+name, report['system_sha256'] == digest(ROOT/'axial_system.py'))
        if 'checks' in report:
            check('all_exact_checks_'+name, all(row['passed'] for row in report['checks']))
        for path, expected in report.get('parent_input_hashes', report.get('input_hashes', {})).items():
            check('unchanged_input_'+name+'_'+Path(path).name, digest(path) == expected)
    comparison = []
    for index, (first, second) in enumerate(zip(coarse['rows'], fine['rows'])):
        change = abs(first['response_over_alpha']/second['response_over_alpha']-1)
        check('resolution_'+str(index), change < 1e-7)
        check('positive_response_integral_'+str(index), second['response_over_alpha'] > 0)
        check('nonpositive_magnetic_sigma_'+str(index), second['geometric_sigma_bar'] <= 0)
        check('exterior_extraction_invariance_'+str(index), max(row['relative_response_difference'] for row in second['exterior_controls']) < 1e-7)
        problem = AxialProblem(second['nominal_flat_compactness'])
        logarithmic_result = independent_riccati(problem)
        independent_error = abs(logarithmic_result/second['response_over_alpha']-1)
        check('independent_Riccati_'+str(index), independent_error < 2e-8)
        archive = ROOT/'results/fine'/second['archive']
        with np.load(archive, allow_pickle=False) as arrays:
            check('finite_archive_'+str(index), all(np.all(np.isfinite(arrays[key])) for key in arrays.files))
            grid, state = arrays['coordinate'], arrays['state']
        check('saved_surface_match_'+str(index), abs(problem.match(1., state[:, -1])['response_over_alpha']/second['response_over_alpha']-1) < 1e-13)
        spline = CubicSpline(grid, state[0])
        quadrature = Quadrature(problem.radius, 180, 10)
        position, weights = quadrature.position, quadrature.weights/problem.radius
        coordinate = position/problem.radius
        field, derivative, mass, metric, xi, rotation = problem.profile.values(position)
        correction = spline(coordinate)
        correction_prime = spline(coordinate, 1)
        physical_shift = coordinate*(1+problem.alpha*problem.radius**2*correction)
        physical_shift_prime = 1+problem.alpha*problem.radius**2*(correction+coordinate*correction_prime)
        integrand = coordinate**4/xi*physical_shift_prime**2+4*coordinate**2/(metric*xi)*physical_shift**2
        surface_shift = 1+problem.alpha*problem.radius**2*state[0, -1]
        surface_prime = 1+problem.alpha*problem.radius**2*(state[0, -1]+state[1, -1])
        integral = float(np.dot(weights, integrand))
        boundary = surface_shift*surface_prime
        energy_error = abs(integral/boundary-1)
        check('positive_static_energy_balance_'+str(index), np.all(integrand > 0) and energy_error < 2e-8)
        published_error = None
        if problem.mass:
            surface = problem.match(1., state[:, -1])
            published = published_kappa(problem.mass/problem.radius, surface['surface_log_derivative'])
            published_error = abs(float(published)/second['k2B_mass_normalized']-1)
            check('published_asymptotic_normalization_'+str(index), published_error < 2e-7)
        comparison.append({'nominal': second['nominal_flat_compactness'], 'resolution_relative_change': change,
                           'Riccati_relative_difference': independent_error, 'static_energy_relative_difference': energy_error,
                           'published_normalization_relative_difference': published_error})
    weak_target = fine['weak_integral_fine']
    check('weak_quadrature_refinement', abs(fine['weak_integral_coarse']/weak_target-1) < 1e-9)
    check('flat_response_zero', fine['rows'][0]['response'] == 0)
    check('weak_analytic_integral_matches_independent_ODE', abs(fine['rows'][0]['response_over_alpha']/weak_target-1) < 1e-8)
    weak_coordinates = np.array([row['alpha'] for row in fine['rows'][1:4]])
    weak_values = np.array([row['response_over_alpha'] for row in fine['rows'][1:4]])
    extrapolated = float(np.polynomial.polynomial.polyfit(weak_coordinates/weak_coordinates[-1], weak_values, 2)[0])
    check('weak_nonzero_coupling_extrapolation', abs(extrapolated/weak_target-1) < 1e-7)
    basis_controls = []
    for compactness in [.0001, .03, .2, .7]:
        for coordinate in [1., 1.7, 3.]:
            numeric = basis(coordinate, compactness)
            wronskian = float(np.linalg.det(numeric))
            check('basis_Wronskian_'+str(compactness)+'_'+str(coordinate), abs(wronskian/(-5)-1) < 2e-13)
            position = mp.mpf(str(coordinate))
            comp = mp.mpf(str(compactness))
            decaying = lambda argument: mp.hyp2f1(1, 4, 6, comp/argument)/argument**2
            exact_basis = [decaying(position), mp.diff(decaying, position)]
            check('basis_high_precision_'+str(compactness)+'_'+str(coordinate), max(abs(float(value)/numeric[index, 1]-1) for index, value in enumerate(exact_basis)) < 2e-13)
            residual = mp.diff(decaying, position, 2)-(6-2*comp/position)/(position**2*(1-comp/position))*decaying(position)
            check('basis_vacuum_equation_'+str(compactness)+'_'+str(coordinate), abs(residual) < mp.mpf('1e-60'))
            basis_controls.append({'compactness': compactness, 'coordinate': coordinate, 'Wronskian': wronskian})
    horizon_regular = lambda radial: radial**3-2*radial**2
    horizon_slope = lambda radial: 3*radial**2-4*radial
    vacuum = solve_ivp(lambda radial, state: [state[1], (6*radial-4)*state[0]/(radial**2*(radial-2))],
                      [3., 6.], [horizon_regular(3.), horizon_slope(3.)], method='DOP853', rtol=2e-13, atol=1e-13, max_step=.01)
    extracted = np.linalg.solve(basis(6., 2.), vacuum.y[:, -1])
    black_hole_response = float(extracted[1]/extracted[0])
    check('BH_regular_branch_zero_response', vacuum.success and abs(black_hole_response) < 1e-7)
    problem = AxialProblem(.03)

    def hydrostatic_mutation(coordinate, state):
        density, pressure, mass, metric = problem.background(coordinate)
        original = problem.equation(coordinate, state)
        original[1] += 4*(density+pressure)/metric*(1+problem.alpha*problem.radius**2*state[0])
        return original

    start = 5e-6
    mutated_center = problem.center_coefficient+2*sum(problem.background(start)[:2])/7
    mutated = solve_ivp(hydrostatic_mutation, [start, 1.], [mutated_center*start**2, 2*mutated_center*start],
                       method='DOP853', rtol=2e-11, atol=1e-12, max_step=1/240)
    wrong_response = problem.match(1., mutated.y[:, -1])['response']
    check('static_fluid_sign_mutation_detected', mutated.success and wrong_response < 0 < fine['rows'][-1]['response'])
    provenance = strict_json(ROOT/'sources/provenance.json')
    check('source_acquisition_owned', provenance['script_sha256'] in scripts)
    for row in provenance['sources']:
        check('source_pdf_'+Path(row['path']).stem, digest(row['path']) == row['sha256'])
    for label in ['coarse', 'fine']:
        path = ROOT/f'results/{label}/coefficients.csv'
        with path.open(newline='', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
        check('csv_rows_'+label, len(rows) == 7 and all(None not in row and None not in row.values() for row in rows))
        input_hashes[path.relative_to(ROOT).as_posix()] = digest(path)
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    check('no_bytecode_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': input_hashes,
              'exact_checks': len(derivation['checks'])+len(matching['checks']), 'comparison_rows': comparison,
              'weak_integral': weak_target, 'weak_extrapolated': extrapolated,
              'weak_integral_ODE_relative_difference': abs(fine['rows'][0]['response_over_alpha']/weak_target-1),
              'basis_controls': basis_controls, 'BH_response_over_mass_fifth': black_hole_response,
              'rejected_hydrostatic_mutation_response': wrong_response, 'new_axial_solves': 14,
              'independent_Riccati_solves': 7, 'new_background_solves': 0,
              'scope': 'ODE and convention controls on inherited background profiles; not a full background error certificate, dynamical spectrum or observation.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': report['exact_checks'],
                      'maximum_resolution_difference': max(row['resolution_relative_change'] for row in comparison),
                      'maximum_Riccati_difference': max(row['Riccati_relative_difference'] for row in comparison),
                      'weak_ODE_error': report['weak_integral_ODE_relative_difference'],
                      'weak_extrapolation_error': abs(extrapolated/weak_target-1), 'BH_response': black_hole_response,
                      'wrong_static_fluid_response': wrong_response}))


if __name__ == '__main__':
    main()
