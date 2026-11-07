from __future__ import annotations

import argparse
import csv
import json

import numpy as np
from numpy.polynomial.legendre import leggauss

from eccentric_source import (ROOT, BRANCH, BACKGROUND, WaveBody, anomaly_solution, source_samples,
                              independent_geodesic, orbit_constants, radial_probe, source_jumps,
                              digest, modest_process, write_report)


def integrate_kernel(trajectory, mass, semilatus, eccentricity, reference_radius, kind, frequency,
                     order, lower=0., upper=2*np.pi):
    points, weights = leggauss(order)
    anomaly = (upper+lower)/2+(upper-lower)*points/2
    weights = weights*(upper-lower)/2
    data = source_samples(anomaly, trajectory, mass, semilatus, eccentricity)
    value, derivative = radial_probe(data['radius'], data['metric'], reference_radius, kind)
    phase = np.exp(1j*frequency*data['time'])
    raw = phase*(data['delta']*value-data['delta_prime']*derivative)
    weak = -data['jump']*phase*((data['metric']/data['radius']+1j*frequency*data['tortoise_velocity'])*value+derivative)
    raw_integral = np.sum(weights*data['time_anomaly']*raw)
    weak_integral = np.sum(weights*data['time_anomaly']*weak)
    scale = np.sum(weights*data['time_anomaly']*(np.abs(raw)+np.abs(weak)))
    endpoints = source_samples(np.array([lower, upper]), trajectory, mass, semilatus, eccentricity)
    endpoint_value = radial_probe(endpoints['radius'], endpoints['metric'], reference_radius, kind)[0]
    endpoint = endpoints['tortoise_velocity']*endpoints['jump']*np.exp(1j*frequency*endpoints['time'])*endpoint_value
    boundary = endpoint[-1]-endpoint[0]
    return raw_integral, weak_integral, boundary, scale


def main():
    modest_process()
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    settings = {'coarse': {'samples': 257, 'order': 128, 'tolerance': 3e-10},
                'fine': {'samples': 1025, 'order': 256, 'tolerance': 3e-12}}[arguments.label]
    output = ROOT/'results'/arguments.label
    assert not output.exists()
    output.mkdir(parents=True)
    body = WaveBody(.03)
    mass, reference_radius = body.mass, body.radius
    checks, rows, orbit_rows, files = [], [], [], []

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def residual(name, values, scale, threshold):
        measured = float(np.max(np.abs(values))/scale)
        check(name, measured < threshold, scaled_error=measured, threshold=threshold)
        return measured

    for eccentricity in [0., .3, .6]:
        label = f'e{eccentricity:.1f}'.replace('.', 'p')
        semilatus = 5*reference_radius*(1+eccentricity)/mass
        energy, momentum = orbit_constants(mass, semilatus, eccentricity)
        trajectory = anomaly_solution(mass, semilatus, eccentricity, settings['tolerance'])
        anomaly = np.linspace(0., 2*np.pi, settings['samples'])
        data = source_samples(anomaly, trajectory, mass, semilatus, eccentricity)
        independent, evaluations = independent_geodesic(mass, semilatus, eccentricity, data, settings['tolerance'])
        duration, total_phase, proper_duration = trajectory.y[:, -1]
        radial_frequency, azimuthal_frequency = 2*np.pi/duration, total_phase/duration
        check(f'{label}_periapsis_outside_body', float(np.min(data['radius'])) >= 4.999999*reference_radius)
        check(f'{label}_timelike', float(np.max(np.abs(data['tortoise_velocity']))) < 1)
        state_errors = []
        for index, (key, scale) in enumerate([('radius', np.max(data['radius'])), ('proper_velocity', np.sqrt(mass/(5*reference_radius))),
                                            ('time', duration), ('phase', total_phase)]):
            state_errors.append(residual(f'{label}_independent_geodesic_{key}', independent[index]-data[key], scale, 2e-8))
        independent_metric = 1-2*mass/independent[0]
        independent_energy2 = independent[1]**2+independent_metric*(1+momentum**2/independent[0]**2)
        residual(f'{label}_independent_energy_constant', independent_energy2-energy**2, energy**2, 2e-10)
        residual(f'{label}_radial_energy', data['proper_velocity']**2+data['metric']*(1+momentum**2/data['radius']**2)-energy**2, energy**2, 2e-14)
        source_scale = float(np.max(np.abs(data['strength'])))
        jump_scale = float(np.max(np.abs(data['jump'])))
        slope_scale = source_scale
        margin = 1-data['tortoise_velocity']**2
        residual(f'{label}_positive_timelike_margin', margin-data['metric']*(1+momentum**2/data['radius']**2)/energy**2, 1., 2e-14)
        residual(f'{label}_Bianchi_delta', data['strength_dot']+2*data['coordinate_velocity']*data['strength']/data['radius']+1j*data['angular_velocity']*data['strength'], source_scale*azimuthal_frequency, 2e-13)
        residual(f'{label}_delta_prime_jump', margin*data['jump']-data['delta_prime'], jump_scale, 2e-14)
        residual(f'{label}_delta_jump', margin*data['derivative_jump']+2*data['tortoise_velocity']*data['jump_dot']+data['tortoise_acceleration']*data['jump']-data['delta'], slope_scale, 2e-13)
        residual(f'{label}_jump_chain_rule', data['time_jump']+data['tortoise_velocity']*data['derivative_jump']-data['jump_dot'], jump_scale*azimuthal_frequency, 2e-13)
        residual(f'{label}_radial_tortoise_delta', data['radial_delta']/data['metric']+data['radial_delta_prime']*data['metric_prime']/data['metric']**2-data['delta'], slope_scale, 2e-13)
        residual(f'{label}_radial_tortoise_delta_prime', data['radial_delta_prime']/data['metric']**2-data['delta_prime'], jump_scale, 2e-13)
        residual(f'{label}_metric_pullback_continuity', data['time_metric_jump']+data['coordinate_velocity']*data['radial_metric_jump'], jump_scale*azimuthal_frequency*reference_radius, 2e-12)
        residual(f'{label}_time_contact', data['metric']*data['radius']*data['jump']/2-data['radius']**2*data['metric']*data['strength']/4, source_scale*np.max(data['radius'])**2, 2e-14)
        residual(f'{label}_radial_contact', -data['radius']*data['coordinate_velocity']*data['jump']/(2*data['metric'])+data['radius']**2*data['strength']*data['coordinate_velocity']/(4*data['metric']), source_scale*np.max(data['radius'])**2, 2e-14)
        if eccentricity == 0:
            circular_value, circular_slope = source_jumps(5*reference_radius, mass)
            residual('old_stage25_circular_value', data['jump']*np.exp(1j*data['phase'])-circular_value, abs(circular_value), 2e-14)
            residual('old_stage25_circular_slope', data['derivative_jump']*np.exp(1j*data['phase'])-circular_slope, abs(circular_slope), 2e-14)
            residual('circular_orbital_frequency', data['angular_velocity']-np.sqrt(mass/(5*reference_radius)**3), azimuthal_frequency, 2e-14)
        else:
            wrong_slope = -data['metric']*data['jump']/data['radius']
            wrong_jump_residual = margin*wrong_slope+2*data['tortoise_velocity']*data['jump_dot']+data['tortoise_acceleration']*data['jump']-data['delta']
            wrong_error = float(np.max(np.abs(wrong_jump_residual))/slope_scale)
            check(f'{label}_circular_jump_shortcut_rejected', wrong_error > 1e-5, scaled_error=wrong_error)
            missing_radial = float(np.max(np.abs(data['strength']*data['coordinate_velocity']))/source_scale)
            check(f'{label}_omitted_Pr_rejected', missing_radial > 1e-4, delta_prime_residual=missing_radial)
            window_dot = 2*np.pi/duration*np.cos(2*np.pi*data['time']/duration)
            window_error = float(np.max(np.abs(window_dot*data['strength']))/(source_scale*azimuthal_frequency))
            check(f'{label}_windowed_source_not_conserved', window_error > .1, scaled_residual=window_error)
        for kind in ['growing', 'decaying']:
            for harmonic in range(-3, 4):
                frequency = azimuthal_frequency+harmonic*radial_frequency
                raw, weak, boundary, scale = integrate_kernel(trajectory, mass, semilatus, eccentricity, reference_radius, kind, frequency, settings['order'])
                error = float(abs(raw-weak-boundary)/scale)
                check(f'{label}_{kind}_n{harmonic}_weak_kernel', error < 2e-10, scaled_error=error)
                floquet = abs(np.exp(1j*(frequency*duration-total_phase))-1)
                check(f'{label}_{kind}_n{harmonic}_Floquet', floquet < 1e-13, residual=float(floquet))
                if eccentricity == 0:
                    probe, probe_derivative = radial_probe(5*reference_radius, 1-2*mass/(5*reference_radius), reference_radius, kind)
                    expected = circular_slope*probe-circular_value*probe_derivative if harmonic == 0 else 0.
                    check(f'circular_{kind}_n{harmonic}_old_kernel', abs(weak/duration-expected) < 2e-10*scale/duration,
                          scaled_error=float(abs(weak-duration*expected)/scale))
                rows.append({'eccentricity': eccentricity, 'probe': kind, 'radial_harmonic': harmonic,
                             'frequency': float(frequency), 'raw_real': float(raw.real/duration),
                             'raw_imag': float(raw.imag/duration), 'weak_real': float(weak.real/duration),
                             'weak_imag': float(weak.imag/duration), 'scale': float(scale/duration),
                             'weak_identity_error': error, 'physical_wave_amplitude': False})
            if eccentricity > 0:
                raw, weak, boundary, scale = integrate_kernel(trajectory, mass, semilatus, eccentricity, reference_radius, kind,
                                                            1.7*azimuthal_frequency, settings['order'], .4, 2.0)
                check(f'{label}_{kind}_finite_interval_endpoint', abs(raw-weak-boundary)/scale < 2e-10,
                      scaled_error=float(abs(raw-weak-boundary)/scale))
                check(f'{label}_{kind}_endpoint_omission_rejected', abs(raw-weak)/scale > 100*2e-10,
                      scaled_error=float(abs(raw-weak)/scale))
        archive = output/f'{label}.npz'
        np.savez_compressed(archive, **data, independent_geodesic=independent)
        files.append({'path': str(archive), 'sha256': digest(archive)})
        orbit_rows.append({'eccentricity': eccentricity, 'semilatus_over_M': semilatus, 'specific_energy': energy,
                           'specific_angular_momentum': momentum, 'periastron_over_R': float(np.min(data['radius'])/reference_radius),
                           'apastron_over_R': float(np.max(data['radius'])/reference_radius), 'radial_period_over_R': duration/reference_radius,
                           'azimuth_advance': total_phase, 'precession': total_phase-2*np.pi,
                           'radial_frequency_R': radial_frequency*reference_radius,
                           'azimuthal_frequency_R': azimuthal_frequency*reference_radius,
                           'maximum_tortoise_speed': float(np.max(np.abs(data['tortoise_velocity']))),
                           'geodesic_comparison_maximum_scaled_error': max(state_errors),
                           'independent_geodesic_evaluations': evaluations})
    csv_path = output/'kernels.csv'
    with csv_path.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    files.append({'path': str(csv_path), 'sha256': digest(csv_path)})
    sources = [ROOT/'eccentric_source.py', BACKGROUND, BRANCH/'axial-companion-20261005/axial_binary.py',
               BRANCH/'causal-exterior-20261005/results/stage-integrity.json']
    write_report(output, __file__, {'settings': settings, 'checks': checks, 'orbits': orbit_rows, 'files': files,
                 'mass': mass, 'radius': reference_radius, 'particle_mass': 1., 'linear_mass_scaling': True,
                 'input_hashes': {str(path): digest(path) for path in sources},
                 'new_background_solves': 0, 'new_fitted_parameters': 0,
                 'radial_probes_are_not_finite_frequency_wave_solutions': True,
                 'orbital_radiation_reaction_derived': False})
    print(json.dumps({'state': 'complete', 'label': arguments.label, 'checks': len(checks), 'orbits': orbit_rows}))


if __name__ == '__main__':
    main()
