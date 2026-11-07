from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import numpy as np
import psutil
from scipy.integrate import solve_bvp, simpson
from scipy.optimize import brentq

from explore_compact_profiles import COEFFICIENT, endpoint_series


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/family'
PARENT = ROOT.parent / 'conserved-stress-20261003/results/stage-integrity.json'


def tail_state(distance, radius, frequency2, coefficients):
    values = [1.0, *coefficients(radius, frequency2)]
    variable = sum(value*distance**order for order, value in enumerate(values, 1))
    derivative = sum(order*value*distance**(order-1) for order, value in enumerate(values, 1))
    return COEFFICIENT*variable**3, -3*COEFFICIENT*variable**2*derivative


def cut_distance(radius, frequency2, floor, coefficients):
    leading = (floor/COEFFICIENT)**(1/3)
    return brentq(lambda distance: tail_state(distance, radius, frequency2, coefficients)[0]-floor,
                  .5*leading, 1.5*leading, xtol=1e-14)


def solve(radius, floor, tolerance, coefficients, previous=None):
    mesh = np.linspace(0, 1, max(250, int(25*radius)))
    if previous is None:
        frequency2 = (1+.36/radius)**2
        width = COEFFICIENT**(-1/3)
        cut = radius-cut_distance(radius, frequency2, floor, coefficients)
        position = cut*mesh
        left = np.tanh((radius-position)/width)
        right = np.tanh((radius+position)/width)
        initial = np.array([(left*right)**3,
                            3*(left*right)**2*((1-right**2)*left-(1-left**2)*right)*cut/width])
    else:
        old_radius, old_cut, old_solution = previous
        frequency2 = 1+(old_solution.p[0]-1)*old_radius/radius
        cut = radius-cut_distance(radius, frequency2, floor, coefficients)
        old_position = np.clip((old_radius-(radius-cut*mesh))/old_cut, 0, 1)
        initial = old_solution.sol(old_position)
        initial[1] *= cut/old_cut
        initial[1, old_position == 0] = 0
        initial[0, -1] = floor
    def equation(position, fields, parameter):
        cut = radius-cut_distance(radius, parameter[0], floor, coefficients)
        amplitude, derivative = fields
        force = .5*(np.cbrt(amplitude)+amplitude**3)-parameter[0]*amplitude
        return np.array([derivative, cut**2*force])
    def boundary(left, right, parameter):
        distance = cut_distance(radius, parameter[0], floor, coefficients)
        slope = tail_state(distance, radius, parameter[0], coefficients)[1]
        return np.array([left[1], right[0]-floor, right[1]-(radius-distance)*slope])
    solution = solve_bvp(equation, boundary, mesh, initial, p=[frequency2],
                         S=np.array([[0., 0.], [0., -2.]]), tol=tolerance, bc_tol=2e-12, max_nodes=60000)
    distance = cut_distance(radius, solution.p[0], floor, coefficients)
    return solution, radius-distance, distance


def observables(radius, cut, solution, coefficients, sigma):
    frequency2 = float(solution.p[0])
    frequency = np.sqrt(frequency2)
    nodes, weights = np.polynomial.legendre.leggauss(8)
    midpoints = .5*(solution.x[1:]+solution.x[:-1])
    halves = .5*np.diff(solution.x)
    mesh = (midpoints[:, None]+halves[:, None]*nodes).ravel()
    integration_weights = (cut*halves[:, None]*weights).ravel()
    position = cut*mesh
    amplitude, derivative = solution.sol(mesh)
    derivative /= cut
    tail_distance = .5*(radius-cut)*(1+nodes)
    tail_weights = .5*(radius-cut)*weights
    tail_amplitude, tail_derivative = tail_state(tail_distance, radius, frequency2, coefficients)
    position = np.concatenate([position, radius-tail_distance])
    amplitude = np.concatenate([amplitude, tail_amplitude])
    derivative = np.concatenate([derivative, tail_derivative])
    integration_weights = np.concatenate([integration_weights, tail_weights])
    measure = 4*np.pi*position**2*integration_weights
    potential_density = .375*amplitude**(4/3)+.125*amplitude**4
    charge = float(frequency*np.dot(measure, amplitude**2))
    gradient = float(np.dot(measure, .5*derivative**2))
    potential = float(np.dot(measure, potential_density))
    rotation = .5*frequency*charge
    energy = gradient+potential+rotation
    omega_action = gradient+potential-rotation
    virial = gradient+3*(potential-rotation)
    charge_radius = (3*charge/(4*np.pi))**(1/3)
    central = float(solution.sol(0)[0])
    central_pressure = .5*frequency2*central**2-.375*central**(4/3)-.125*central**4
    sample_mesh = np.linspace(0, 1, max(12001, int(400*radius)+1))
    sampled, sampled_derivative = solution.sol(sample_mesh)
    sample_position = cut*sample_mesh
    sample_density = .5*(sampled_derivative/cut)**2+.5*frequency2*sampled**2+.375*sampled**(4/3)+.125*sampled**4
    independent_energy = simpson(4*np.pi*sample_position**2*sample_density, x=sample_position)
    radial_pressure = .5*derivative**2+.5*frequency2*amplitude**2-potential_density
    tangential_pressure = -.5*derivative**2+.5*frequency2*amplitude**2-potential_density
    integrated_trace = float(np.dot(measure, radial_pressure+2*tangential_pressure))
    wall_gradient_tension = 2*gradient/(4*np.pi*charge_radius**2)
    return {'support_radius': radius, 'cut_radius': cut, 'frequency': float(frequency),
            'central_amplitude': central, 'central_charge_density': float(frequency*central**2),
            'charge': charge, 'energy': energy, 'gradient_energy': gradient,
            'potential_energy': potential, 'rotation_energy': rotation, 'grand_potential': omega_action,
            'charge_radius': charge_radius, 'energy_per_charge': energy/charge,
            'surface_excess_ratio': (energy-charge)/(4*np.pi*sigma*charge_radius**2),
            'chemical_shift_ratio': (frequency-1)*charge_radius/(2*sigma),
            'central_laplace_ratio': central_pressure*charge_radius/(2*sigma),
            'wall_gradient_tension_ratio': wall_gradient_tension/sigma,
            'virial_relative': abs(virial)/gradient,
            'integrated_pressure_trace': integrated_trace,
            'active_to_inertial_mass_ratio': (energy+integrated_trace)/energy,
            'virial_stress_identity_error': abs(virial+integrated_trace)/gradient,
            'independent_quadrature_relative_error': abs(independent_energy-energy)/energy,
            'min_amplitude': float(np.min(sampled)), 'max_increase': float(np.max(sampled_derivative/cut)),
            'bvp_success': bool(solution.success), 'bvp_message': solution.message,
            'nodes': len(solution.x), 'max_rms_residual': float(np.max(solution.rms_residuals))}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    coefficients, series = endpoint_series()
    parent = json.loads((PARENT.parent/'charge-coexistence/status.json').read_text(encoding='utf-8'))
    last = parent['quadrature_estimates'][-1]
    amplitude_star = float(last['critical_amplitude'])
    chemical_star = float(last['critical_chemical_potential'])
    sigma_physical = float(last['planar_grand_potential_surface_tension'])
    sigma = sigma_physical/(amplitude_star**2*chemical_star)
    all_rows = []
    for label, floor, tolerance in [('coarse', 1e-6, 2e-7), ('fine', 1e-9, 2e-9)]:
        previous = None
        for radius in [6., 8., 12., 20., 40., 80., 160.]:
            solution, cut, distance = solve(radius, floor, tolerance, coefficients, previous)
            assert solution.success, (label, radius, solution.message)
            row = observables(radius, cut, solution, coefficients, sigma)
            row.update(label=label, floor=floor, tolerance=tolerance, endpoint_distance=distance)
            np.savez_compressed(OUTPUT/f'{label}-R{radius:g}.npz',
                                spline_coefficients=solution.sol.c, spline_knots=solution.sol.x,
                                radius=radius, cut_radius=cut, frequency2=solution.p[0], floor=floor)
            all_rows.append(row)
            print(json.dumps(row), flush=True)
            (OUTPUT/'progress.json').write_text(json.dumps(all_rows, indent=2), encoding='utf-8')
            previous = radius, cut, solution
    comparisons = []
    for coarse, fine in zip(all_rows[:7], all_rows[7:]):
        assert coarse['support_radius'] == fine['support_radius']
        differences = {key: abs(coarse[key]-fine[key])/max(abs(fine[key]), 1e-30)
                       for key in ['frequency', 'charge', 'energy', 'central_amplitude', 'gradient_energy']}
        comparisons.append({'radius': fine['support_radius'], 'relative_differences': differences})
    fine_rows = all_rows[7:]
    assert all(row['virial_relative'] < 1e-7 for row in fine_rows)
    assert all(row['independent_quadrature_relative_error'] < 1e-8 for row in fine_rows)
    assert all(max(row['relative_differences'].values()) < 2e-6 for row in comparisons)
    assert all(row['energy'] > row['frequency']*row['charge'] > row['charge'] for row in fine_rows)
    assert all(row['max_increase'] < 1e-9 and row['min_amplitude'] > 0 for row in fine_rows)
    assert all(fine_rows[index+1]['charge'] > fine_rows[index]['charge'] and
               fine_rows[index+1]['frequency'] < fine_rows[index]['frequency'] for index in range(6))
    report = {'state': 'complete', 'units': 'r=mu_star*r_physical, h=f/v_star, w=omega/mu_star',
              'physical_conversion': {'v_star': amplitude_star, 'mu_star': chemical_star,
                                      'energy_factor': amplitude_star**2/chemical_star,
                                      'charge_factor': amplitude_star**2/chemical_star**2,
                                      'radius_factor': 1/chemical_star},
              'dimensionless_surface_tension': sigma, 'rows': all_rows, 'convergence': comparisons,
              'series_coefficients': series, 'elapsed_seconds': time.monotonic()-started,
              'parent_seal_sha256': hashlib.sha256(PARENT.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'solver_source_sha256': hashlib.sha256((ROOT/'explore_compact_profiles.py').read_bytes()).hexdigest()}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'profiles': len(all_rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
