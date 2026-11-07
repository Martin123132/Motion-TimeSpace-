from __future__ import annotations

import argparse
import json
import time

import numpy as np

from polar_source import ROOT, BRANCH, coefficients, digest, read_json, save_report, modest_process
from polar_source import anomaly_solution, orbit_constants, source_samples, vacuum_probes, metric_and_boundary, quadrature_nodes


def integral_test(trajectory, mass, semilatus, eccentricity, energy, angular, azimuth, frequency,
                  solution, order, panels, lower, upper):
    nodes, weights = quadrature_nodes(order, panels, lower, upper)
    samples = source_samples(nodes, trajectory, mass, semilatus, eccentricity)
    source = coefficients(samples, mass, energy, angular, azimuth)
    weight_time = weights*samples['time_anomaly']
    phase = np.exp(1j*frequency*samples['time'])
    states = solution.sol(samples['radius'])
    endpoint_samples = source_samples(np.array([lower, upper]), trajectory, mass, semilatus, eccentricity)
    endpoint_source = coefficients(endpoint_samples, mass, energy, angular, azimuth)
    endpoint_states = solution.sol(endpoint_samples['radius'])
    tests = []
    for basis in [0, 1]:
        master, slope = states[2*basis:2*basis+2]
        overlap = source['delta']*master-source['delta_prime']*slope
        metric_contraction, boundary = metric_and_boundary(samples, source, mass, frequency, master, slope)
        metric_integrand = source['strength']*metric_contraction
        integrated = np.dot(weight_time, phase*overlap)
        metric_integrated = np.dot(weight_time, phase*metric_integrand)
        scale = float(np.dot(weight_time, np.abs(metric_integrand)+6*np.abs(overlap)))
        _, endpoints = metric_and_boundary(endpoint_samples, endpoint_source, mass, frequency,
                                           *endpoint_states[2*basis:2*basis+2])
        endpoints *= np.exp(1j*frequency*endpoint_samples['time'])
        endpoint = endpoints[-1]-endpoints[0]
        relative = abs(metric_integrated+6*integrated-endpoint)/max(scale, 1e-300)
        independent = (source['martel_canonical_G']*master/source['metric']
                       -source['martel_F']*(slope-master*2*mass/samples['radius']**2)/source['metric']**2)
        independent_integral = np.dot(weight_time, phase*independent)
        source_scale = float(np.dot(weight_time, np.abs(source['delta']*master)+np.abs(source['delta_prime']*slope)))
        opposite = coefficients(samples, mass, energy, angular, -azimuth)
        conjugate_integral = np.dot(weight_time, np.conj(phase)*(opposite['delta']*master-opposite['delta_prime']*slope))
        tests.append({'basis': basis, 'overlap_real': float(integrated.real), 'overlap_imag': float(integrated.imag),
                      'source_absolute_scale': source_scale, 'metric_reciprocity_error': float(relative),
                      'endpoint_over_scale': float(abs(endpoint)/max(scale, 1e-300)),
                      'Martel_integral_error': float(abs(independent_integral-integrated)/max(source_scale, 1e-300)),
                      'reality_error': float(abs(conjugate_integral-np.conj(integrated))/max(source_scale, 1e-300))})
    return tests


def finite_derivatives(trajectory, mass, semilatus, eccentricity, energy, angular):
    nodes = np.linspace(.2, 2.9, 11)
    base = source_samples(nodes, trajectory, mass, semilatus, eccentricity)
    source = coefficients(base, mass, energy, angular, 2)
    derivatives = []
    for step in [1e-4, 5e-5]:
        left = source_samples(nodes-step, trajectory, mass, semilatus, eccentricity)
        right = source_samples(nodes+step, trajectory, mass, semilatus, eccentricity)
        left_source, right_source = (coefficients(sample, mass, energy, angular, 2) for sample in [left, right])
        derivatives.append({key: (right_source[key]-left_source[key])/(2*step*base['time_anomaly'])
                            for key in ['strength', 'jump', 'angular_speed']})
        derivatives[-1]['velocity'] = (right['coordinate_velocity']-left['coordinate_velocity'])/(2*step*base['time_anomaly'])
    derivative = {key: (4*derivatives[1][key]-derivatives[0][key])/3 for key in derivatives[0]}
    radius, velocity = base['radius'], base['coordinate_velocity']
    metric, strength, omega = source['metric'], source['strength'], source['angular_speed']
    metric_prime = 2*mass/radius**2
    time_terms = [derivative['strength'], strength*velocity*metric_prime/metric, 2j*strength*omega]
    radial_terms = [derivative['strength']*velocity, strength*derivative['velocity'],
                    strength*metric*metric_prime/2, -strength*metric_prime*velocity**2/(2*metric),
                    -strength*metric*radius*omega**2, 2j*strength*omega*velocity]
    angular_terms = [-2j/3*(derivative['strength']*omega+strength*derivative['angular_speed']),
                     -4j*strength*omega*velocity/(3*radius), 4*strength*omega**2/3]
    return {'time_Bianchi_error': float(np.max(np.abs(sum(time_terms))/np.maximum(sum(map(np.abs, time_terms)), 1e-300))),
            'radial_Bianchi_error': float(np.max(np.abs(sum(radial_terms))/np.maximum(sum(map(np.abs, radial_terms)), 1e-300))),
            'angular_Bianchi_error': float(np.max(np.abs(sum(angular_terms))/np.maximum(sum(map(np.abs, angular_terms)), 1e-300))),
            'jump_derivative_error': float(np.max(np.abs(derivative['jump']-source['jump_rate'])/np.maximum(np.abs(source['jump_rate']), 1e-300)))}


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    fine = arguments.label == 'fine'
    tolerance = 2e-13 if fine else 2e-11
    order, panels = (28, 24) if fine else (20, 12)
    parent_path = BRANCH/'secular-actions-20261005/results/analysis/status.json'
    parent = read_json(parent_path)
    mass, radius = parent['main_rates'][0]['mass'], parent['main_rates'][0]['radius']
    rows, orbit_rows, finite_rows = [], [], []
    started = time.monotonic()
    for eccentricity in [0., .3, .6]:
        semilatus = 5*radius*(1+eccentricity)/mass
        trajectory = anomaly_solution(mass, semilatus, eccentricity, tolerance)
        period, phase_advance = trajectory.sol(2*np.pi)[:2]
        energy, angular = orbit_constants(mass, semilatus, eccentricity)
        periapsis = mass*semilatus/(1+eccentricity)
        apoapsis = mass*semilatus/(1-eccentricity)
        finite_rows.append({'eccentricity': eccentricity, **finite_derivatives(trajectory, mass, semilatus, eccentricity, energy, angular)})
        orbit_rows.append({'eccentricity': eccentricity, 'mass': mass, 'radius': radius, 'semilatus': semilatus,
                           'period': float(period), 'phase_advance': float(phase_advance)})
        for azimuth, harmonics in [(0, [-3, -1, 0, 1, 3]), (2, [-5, -3, -2, -1, 0, 1, 3])]:
            for harmonic in harmonics:
                frequency = (azimuth*phase_advance+2*np.pi*harmonic)/period
                solution = vacuum_probes(mass, periapsis, apoapsis, frequency, tolerance)
                full = integral_test(trajectory, mass, semilatus, eccentricity, energy, angular, azimuth,
                                     frequency, solution, order, 2*panels, 0, 2*np.pi)
                half = integral_test(trajectory, mass, semilatus, eccentricity, energy, angular, azimuth,
                                     frequency, solution, order, panels, 0, np.pi)
                partial = integral_test(trajectory, mass, semilatus, eccentricity, energy, angular, azimuth,
                                     frequency, solution, order, panels, .31, 2.37)
                for full_row, half_row in zip(full, half):
                    full_row['half_orbit_symmetry_error'] = abs(complex(full_row['overlap_real'], full_row['overlap_imag'])
                              -2*half_row['overlap_real'])/max(full_row['source_absolute_scale'], 1e-300)
                samples = source_samples(np.linspace(0, 2*np.pi, 33), trajectory, mass, semilatus, eccentricity)
                source = coefficients(samples, mass, energy, angular, azimuth)
                jump_delta = ((1-source['tortoise_speed']**2)*source['slope_jump']
                            +2*source['tortoise_speed']*source['jump_rate']+source['tortoise_acceleration']*source['jump'])
                jump_error = np.max(np.abs(jump_delta-source['delta'])/np.maximum(np.abs(source['delta']), 1e-300))
                row = {'eccentricity': eccentricity, 'azimuth': azimuth, 'harmonic': harmonic,
                       'frequency': float(frequency), 'full': full, 'partial': partial,
                       'jump_delta_error': float(jump_error), 'basis_evaluations': solution.nfev,
                       'purpose': 'Homogeneous vacuum test functions, not physical body/BH outgoing wave amplitudes'}
                rows.append(row)
        print(json.dumps({'eccentricity': eccentricity, 'completed_source_modes': len(rows)}), flush=True)
    inputs = [parent_path, ROOT/'polar_source.py', BRANCH/'eccentric-source-20261005/eccentric_source.py',
              BRANCH/'secular-actions-20261005/results/stage-integrity.json']
    report = save_report(ROOT/'results'/arguments.label, __file__, {'rows': rows, 'orbits': orbit_rows,
                'finite_derivatives': finite_rows, 'settings': {'tolerance': tolerance, 'order': order, 'panels_per_half': panels},
                'elapsed_seconds': time.monotonic()-started,
                'input_hashes': {str(path): digest(path) for path in inputs},
                'new_background_solves': 0, 'new_physical_fluxes': 0, 'new_fitted_coefficients': 0})
    print(json.dumps({'state': 'complete', 'source_modes': len(rows), 'elapsed_seconds': report['elapsed_seconds'],
         'max_full_reciprocity': max(item['metric_reciprocity_error'] for row in rows for item in row['full']),
         'max_partial_reciprocity': max(item['metric_reciprocity_error'] for row in rows for item in row['partial'])}))


if __name__ == '__main__':
    main()
