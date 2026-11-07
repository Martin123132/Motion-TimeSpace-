from __future__ import annotations

import csv
from datetime import datetime, timezone
import json

import numpy as np
import psutil
from scipy.integrate import cumulative_simpson

from causal_system import ROOT, digest


def pulse_solution(model, duration, carrier, count, modes_kept):
    time = np.linspace(0., 1.25*duration, count)
    eigenvalues = model['eigenvalues'][:modes_kept]
    coupling = model['coupling'][:modes_kept]
    natural = np.sqrt(eigenvalues)
    frequencies = carrier+np.pi/duration*np.array([0., 2., -2., 4., -4., 6., -6.])
    coefficients = np.array([10/32, -15/64, -15/64, 3/32, 3/32, -1/64, -1/64])
    assert np.min(np.abs(eigenvalues[:, None]-frequencies[None, :]**2)) > 1e-5
    clipped = np.minimum(time, duration)
    derivatives = np.array([np.sum(coefficients[:, None]*frequencies[:, None]**order*
                                  np.cos(frequencies[:, None]*clipped+order*np.pi/2), axis=0) for order in range(7)])
    derivatives[:, time >= duration] = 0.
    port, port_dot, port_second, port_third, port_fourth = derivatives[:5]
    positions, velocities = np.zeros((modes_kept, count)), np.zeros((modes_kept, count))
    for frequency, coefficient in zip(frequencies, coefficients):
        response = coupling*coefficient*frequency**2/(eigenvalues-frequency**2)
        positions += response[:, None]*(np.cos(frequency*clipped)-np.cos(natural[:, None]*clipped))
        velocities += response[:, None]*(-frequency*np.sin(frequency*clipped)+natural[:, None]*np.sin(natural[:, None]*clipped))
    after = time >= duration
    elapsed = time[after]-duration
    at_end, speed_end = positions[:, after][:, 0].copy(), velocities[:, after][:, 0].copy()
    positions[:, after] = at_end[:, None]*np.cos(natural[:, None]*elapsed)+speed_end[:, None]/natural[:, None]*np.sin(natural[:, None]*elapsed)
    velocities[:, after] = -at_end[:, None]*natural[:, None]*np.sin(natural[:, None]*elapsed)+speed_end[:, None]*np.cos(natural[:, None]*elapsed)
    accelerations = -eigenvalues[:, None]*positions-coupling[:, None]*port_second
    norm = float(model['norm'])
    static = float(model['static_impedance'])
    moment = float(model['moment'])
    traction = static*port+norm*port_second+coupling@accelerations
    energy = .5*(norm*port_dot**2+2*port_dot*(coupling@velocities)+np.sum(velocities**2, axis=0)
                  +np.sum(eigenvalues[:, None]*positions**2, axis=0)+static*port**2)
    energy_slope = norm*port_dot*port_second+port_second*(coupling@velocities)+port_dot*(coupling@accelerations)
    energy_slope += np.sum(velocities*accelerations+eigenvalues[:, None]*positions*velocities, axis=0)+static*port*port_dot
    power = port_dot*traction
    work = cumulative_simpson(power, x=time, initial=0.)
    quadratic = static*port+norm*port_second
    quartic = quadratic-moment*port_fourth
    approximate_energy = .5*(norm*port_dot**2+static*port**2+moment*(port_second**2-2*port_dot*port_third))
    projected_moment = float(np.sum(coupling**2/eigenvalues))
    projected_quartic = quadratic-projected_moment*port_fourth
    inverse_root_moment = float(np.sum(coupling**2/eigenvalues**1.5))
    history_bound = inverse_root_moment*cumulative_simpson(np.abs(derivatives[6]), x=time, initial=0.)
    unresolved_norm = norm-float(np.sum(coupling**2))
    omitted_weight = float(np.sum(model['coupling'][modes_kept:]**2))
    next_eigenvalue = float(model['eigenvalues'][modes_kept])
    tail_bound = omitted_weight/np.sqrt(next_eigenvalue)*cumulative_simpson(np.abs(port_fourth), x=time, initial=0.)
    peak_energy = float(np.max(energy))
    peak_traction = float(np.max(np.abs(traction)))
    energy_scale = max(peak_energy, 1e-30)
    final_values = energy[after]
    summary = {'duration': duration, 'carrier': carrier, 'time_samples': count, 'modes_kept': modes_kept,
               'maximum_harmonic_frequency': float(np.max(np.abs(frequencies))),
               'kinetic_remainder': unresolved_norm,
               'energy_minimum': float(np.min(energy)), 'energy_maximum': peak_energy,
               'energy_after_pulse': float(np.mean(final_values)),
               'post_pulse_energy_relative_drift': float(np.ptp(final_values)/max(np.mean(final_values), 1e-300)),
               'work_integral_error_over_peak_energy': float(np.max(np.abs(work-energy))/energy_scale),
               'instantaneous_work_identity_error': float(np.max(np.abs(energy_slope-power))/max(np.max(np.abs(power)), 1e-30)),
               'quadratic_traction_error_over_peak': float(np.max(np.abs(traction-quadratic))/peak_traction),
               'quartic_traction_error_over_peak': float(np.max(np.abs(traction-quartic))/peak_traction),
               'quartic_stored_energy_error_over_peak': float(np.max(np.abs(energy-approximate_energy))/energy_scale),
               'causal_quartic_remainder_bound_maximum': float(np.max(history_bound)),
               'projected_quartic_error_maximum': float(np.max(np.abs(traction-projected_quartic))),
               'modal_tail_bound_maximum': float(np.max(tail_bound)),
               'omitted_spectral_weight': omitted_weight, 'next_eigenvalue': next_eigenvalue,
               'pre_forcing_response': 0., 'initial_mode_amplitude': float(np.max(np.abs(positions[:, 0]))),
               'initial_mode_velocity': float(np.max(np.abs(velocities[:, 0])))}
    samples = {'time': time, 'q': port, 'q_dot': port_dot, 'p': traction, 'energy': energy, 'power': power,
               'integrated_work': work, 'quadratic_traction': quadratic, 'quartic_traction': quartic,
               'quartic_energy': approximate_energy, 'quartic_remainder_bound': history_bound, 'modal_tail_bound': tail_bound}
    return summary, samples


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/pulses'
    output.mkdir(parents=True, exist_ok=False)
    reports, inputs = [], {}
    settings = [(256, duration, count, modes) for duration in [4., 16., 64.]
                for count, modes in [(4097, 64), (8193, 128)]]
    settings.extend([(128, 16., 8193, 128), (256, 4., 16385, 128)])
    for cells, duration, count, modes in settings:
        path = ROOT/f'results/spectrum/body-{cells}.npz'
        inputs[str(path)] = digest(path)
        with np.load(path, allow_pickle=False) as archive:
            model = {key: archive[key] for key in archive.files}
        summary, samples = pulse_solution(model, duration, .25, count, modes)
        label = f'cells{cells}-T{int(duration)}-n{count}-m{modes}'
        summary['label'], summary['cells'] = label, cells
        np.savez_compressed(output/f'{label}.npz', **samples)
        summary['archive_sha256'] = digest(output/f'{label}.npz')
        reports.append(summary)
        print(json.dumps({key: summary[key] for key in ['label', 'energy_after_pulse',
              'work_integral_error_over_peak_energy', 'quadratic_traction_error_over_peak', 'quartic_traction_error_over_peak']}), flush=True)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': inputs, 'rows': reports,
              'forcing': 'q=sin(pi*tau/T)^6*cos(0.25*tau) on0<tau<T, zero otherwise; initially unexcited interior',
              'scope': 'Driven interior surface port, not a self-consistently evolving binary trajectory.',
              'pulse_energy_units': 'multiply by kappa/R, kappa=3/(4*pi), for the m=+/-1 pair quadratures',
              'solution_method': 'Analytic causal convolution with modes of actual Galerkin interior; no stiff time integrator.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    with (output/'pulse-summary.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(reports[0]))
        writer.writeheader()
        writer.writerows(reports)
    (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
