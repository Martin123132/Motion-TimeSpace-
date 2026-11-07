from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import psutil
from scipy.integrate import cumulative_simpson, simpson
from scipy.interpolate import PPoly
import sympy as sp

from solve_self_gravity import BodySolver, potential


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'finite-charge-20261003'
OUTPUT = ROOT/'results/validation'


def flat_binding_coefficients(radius, count):
    report = json.loads((PARENT/'results/regular-center-bodies/status.json').read_text(encoding='utf-8'))
    row = next(item for item in report['rows'] if item['support_radius'] == radius)
    archive = np.load(PARENT/f'results/regular-center-bodies/profile-R{radius:g}.npz')
    spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
    cut = float(archive['cut_radius'])
    position = np.linspace(0, radius, count)
    inside = position <= cut
    amplitude = np.zeros_like(position)
    derivative = np.zeros_like(position)
    amplitude[inside], derivative[inside] = spline(position[inside]/cut)
    derivative /= cut
    outside_distance = radius-position[~inside]
    amplitude[~inside] = 12**(-1.5)*outside_distance**3
    derivative[~inside] = -3*12**(-1.5)*outside_distance**2
    rotation = .5*row['frequency']**2*amplitude**2
    gradient = .5*derivative**2
    rho = rotation+gradient+potential(amplitude)
    pressure = rotation+gradient-potential(amplitude)
    mass = cumulative_simpson(position**2*rho, x=position, initial=0)
    exact = -4*np.pi*simpson(position*mass*(rho+pressure), x=position)
    density_only = -4*np.pi*simpson(position*mass*rho, x=position)
    return {'grid_points': count, 'full_stress_binding_coefficient': float(exact),
            'density_only_Newton_coefficient': float(density_only),
            'radial_pressure_correction_relative_to_Newton': float(exact/density_only-1),
            'replayed_flat_energy_relative_error': float(abs(4*np.pi*mass[-1]-row['energy'])/row['energy'])}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    fine = json.loads((ROOT/'results/fine/status.json').read_text(encoding='utf-8'))
    coarse = json.loads((ROOT/'results/coarse/status.json').read_text(encoding='utf-8'))
    third = json.loads((ROOT/'results/third-resolution/status.json').read_text(encoding='utf-8'))
    assert fine['state'] == coarse['state'] == third['state'] == 'complete'
    comparisons = []
    for row in fine['rows']:
        baseline = next(item for item in coarse['rows'] if item['base_radius'] == row['base_radius']
                        and item['nominal_flat_compactness'] == row['nominal_flat_compactness'])
        differences = {key: abs(row[key]-baseline[key])/max(abs(row[key]), 1e-20)
                       for key in ['radius', 'frequency_at_infinity', 'adm_energy', 'central_amplitude', 'central_lapse']}
        assert max(differences.values()) < 1e-8
        assert row['charge_relative_error'] < 1e-11 and row['mass_quadrature_relative_error'] < 1e-11
        assert row['komar_adm_relative_error_without_tiny_tail'] < 1e-10
        assert row['minimum_F'] > .95 and row['central_lapse'] > .95 and row['min_amplitude_interior'] > 0
        assert row['angular_Einstein_relative_residual'] < 1e-4
        comparisons.append({'base_radius': row['base_radius'], 'nominal': row['nominal_flat_compactness'],
                            'relative_observable_differences': differences})
    weak_tests = []
    for radius in [8., 20., 80.]:
        sequence = [row for row in fine['rows'] if row['base_radius'] == radius]
        assert abs(sequence[0]['radius']/radius-1) < 1e-9
        assert abs(sequence[0]['adm_energy']/sequence[0]['flat_energy']-1) < 1e-10
        for left, right in zip(sequence, sequence[1:]):
            assert right['radius'] < left['radius'] and right['adm_energy'] < left['adm_energy']
            assert right['frequency_at_infinity'] < left['frequency_at_infinity']
        estimates = [flat_binding_coefficients(radius, count) for count in [16001, 32001]]
        predicted = estimates[-1]['full_stress_binding_coefficient']
        assert abs(estimates[0]['full_stress_binding_coefficient']/predicted-1) < 1e-8
        zero_energy = sequence[0]['adm_energy']
        slopes = [(row['adm_energy']-zero_energy)/row['alpha'] for row in sequence[1:3]]
        ratio = sequence[2]['alpha']/sequence[1]['alpha']
        extrapolated = (ratio*slopes[0]-slopes[1])/(ratio-1)
        error = abs(extrapolated/predicted-1)
        density_error = abs(extrapolated/estimates[-1]['density_only_Newton_coefficient']-1)
        assert error < 2e-6 and density_error > 100*error
        weak_tests.append({'base_radius': radius, 'independent_flat_quadratures': estimates,
                           'small_coupling_secant_slopes': slopes, 'zero_coupling_extrapolated_slope': extrapolated,
                           'full_stress_prediction_relative_error': error,
                           'density_only_Newton_relative_error': density_error,
                           'first_secant_prediction_relative_error': abs(slopes[0]/predicted-1)})
    last_third = third['rows'][-1]
    last_fine = next(row for row in fine['rows'] if row['base_radius'] == 8 and row['nominal_flat_compactness'] == .03)
    assert last_third['angular_Einstein_relative_residual'] < last_fine['angular_Einstein_relative_residual']/20
    assert abs(last_third['adm_energy']/last_fine['adm_energy']-1) < 1e-10

    derivation = json.loads((ROOT/'results/derivation/status.json').read_text(encoding='utf-8'))
    symbols = sp.symbols('radius compactness frequency2')
    coefficients = sp.lambdify(symbols, [sp.sympify(value, locals=dict(zip(derivation['edge_symbols'], symbols)))
                                        for value in derivation['edge_u_coefficients_orders_2_to_5']], 'numpy')
    first_law = []
    for radius in [8., 20., 80.]:
        reference = next(row for row in fine['rows'] if row['base_radius'] == radius and row['nominal_flat_compactness'] == .03)
        archive = np.load(ROOT/'results/fine'/reference['archive'])
        original_spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        levels = []
        for step in [.001, .0005]:
            branches = []
            for sign in [-1, 1]:
                offset = sign*step
                body = BodySolver(radius, 1e-11, 2e-9, coefficients)
                body.flat['charge'] *= 1+offset
                body.charge_scale = body.flat['charge']/(4*np.pi)
                def seed_profile(coordinate, offset=offset):
                    fields = original_spline(coordinate)
                    fields[4] /= 1+offset
                    return fields
                seed = SimpleNamespace(p=archive['parameters'].copy(), sol=seed_profile)
                solution = body.solve(.03, seed)
                assert solution.success
                row = body.observables(solution)
                assert abs(body.alpha/reference['alpha']-1) < 1e-14
                name = f'first-law-R{radius:g}-offset{offset:g}'.replace('.', 'p')
                np.savez_compressed(OUTPUT/(name+'.npz'), spline_coefficients=solution.sol.c,
                                    spline_knots=solution.sol.x, parameters=solution.p, alpha=body.alpha,
                                    target_charge=body.flat['charge'], base_radius=radius)
                branches.append({'relative_charge_offset': offset, 'charge': row['charge'],
                                 'target_charge': row['target_charge'], 'adm_energy': row['adm_energy'],
                                 'frequency': row['frequency_at_infinity'], 'charge_error': row['charge_relative_error'],
                                 'komar_error': row['komar_adm_relative_error_without_tiny_tail'], 'archive': name+'.npz'})
            slope = (branches[1]['adm_energy']-branches[0]['adm_energy'])/(2*step*reference['target_charge'])
            error = abs(slope/reference['frequency_at_infinity']-1)
            levels.append({'relative_charge_step': step, 'mass_charge_derivative': slope,
                           'frequency_at_infinity': reference['frequency_at_infinity'], 'relative_error': error, 'branches': branches})
        assert levels[-1]['relative_error'] < 1e-7
        assert levels[-1]['relative_error'] < levels[0]['relative_error']/2
        first_law.append({'base_radius': radius, 'alpha_held_fixed': reference['alpha'], 'levels': levels})
        print(json.dumps({'radius': radius, 'binding_prediction_error': next(row['full_stress_prediction_relative_error'] for row in weak_tests if row['base_radius'] == radius),
                          'first_law_error': levels[-1]['relative_error']}), flush=True)
    largest = next(row for row in fine['rows'] if row['base_radius'] == 80 and row['nominal_flat_compactness'] == .03)
    assert largest['adm_energy'] < largest['target_charge'] and largest['central_local_frequency'] > 1 > largest['frequency_at_infinity']
    report = {'state': 'complete', 'coarse_fine_comparisons': comparisons, 'weak_binding_tests': weak_tests,
              'first_law_tests': first_law,
              'third_resolution_check': {'angular_relative_error_coarse': next(row['angular_Einstein_relative_residual'] for row in coarse['rows'] if row['base_radius'] == 8 and row['nominal_flat_compactness'] == .03),
                                         'angular_relative_error_fine': last_fine['angular_Einstein_relative_residual'],
                                         'angular_relative_error_third': last_third['angular_Einstein_relative_residual']},
              'largest_body_gravity_example': {'adm_energy_per_charge': largest['adm_energy']/largest['target_charge'],
                                               'radius_contraction_fraction': 1-largest['radius']/80,
                                               'energy_reduction_fraction': 1-largest['adm_energy']/largest['flat_energy'],
                                               'frequency_infinity': largest['frequency_at_infinity'],
                                               'frequency_center_proper': largest['central_local_frequency']},
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'input_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                               for name in ['solve_self_gravity.py', 'results/coarse/status.json', 'results/fine/status.json', 'results/third-resolution/status.json', 'results/derivation/status.json']},
              'no_dynamical_stability_inference_from_stationary_convergence': True}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'fixed_charge_profiles_compared': len(comparisons),
                      'independent_binding_predictions': len(weak_tests), 'first_law_profiles': 12}))


if __name__ == '__main__':
    main()
