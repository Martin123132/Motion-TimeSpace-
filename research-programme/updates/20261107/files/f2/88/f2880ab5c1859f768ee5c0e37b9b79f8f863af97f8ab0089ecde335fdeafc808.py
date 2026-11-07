from __future__ import annotations

from datetime import datetime, timezone
import json

import mpmath as mp
import numpy as np
import psutil
from scipy.integrate import solve_ivp
import sympy as sy

from causal_system import ROOT, digest
from run_pulses import pulse_solution


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    path = ROOT/'results/spectrum/body-256.npz'
    with np.load(path, allow_pickle=False) as archive:
        model = {key: archive[key] for key in archive.files}
    duration, carrier, modes_kept = 4., .25, 8
    summary, sampled = pulse_solution(model, duration, carrier, 1025, modes_kept)
    time_symbol = sy.symbols('time', real=True)
    forcing = sy.sin(sy.pi*time_symbol/duration)**6*sy.cos(carrier*time_symbol)
    derivatives = sy.lambdify(time_symbol, [sy.diff(forcing, time_symbol, order) for order in range(3)], 'numpy')
    eigenvalues, coupling = model['eigenvalues'][:modes_kept], model['coupling'][:modes_kept]
    norm, static = float(model['norm']), float(model['static_impedance'])

    def source(time):
        return np.asarray(derivatives(time)) if 0 < time < duration else np.zeros(3)

    def equation(time, state):
        port, port_dot, port_second = source(time)
        positions, velocities = state[:modes_kept], state[modes_kept:2*modes_kept]
        accelerations = -eigenvalues*positions-coupling*port_second
        traction = static*port+norm*port_second+np.dot(coupling, accelerations)
        return np.r_[velocities, accelerations, port_dot*traction]

    sample_times = np.r_[np.linspace(-1., 0., 9)[:-1], sampled['time']]
    solution = solve_ivp(equation, (-1., sample_times[-1]), np.zeros(2*modes_kept+1), t_eval=sample_times,
                         method='DOP853', rtol=2e-11, atol=2e-14, max_step=.015)
    assert solution.success, solution.message
    energies, tractions = [], []
    for time, state in zip(solution.t, solution.y.T):
        port, port_dot, port_second = source(time)
        positions, velocities = state[:modes_kept], state[modes_kept:2*modes_kept]
        accelerations = -eigenvalues*positions-coupling*port_second
        tractions.append(static*port+norm*port_second+np.dot(coupling, accelerations))
        energies.append(.5*(norm*port_dot**2+2*port_dot*np.dot(coupling, velocities)+np.dot(velocities, velocities)
                           +np.dot(eigenvalues, positions**2)+static*port**2))
    energies, tractions = np.array(energies), np.array(tractions)
    peak_energy = np.max(sampled['energy'])
    integration = {'ODE_function_evaluations': solution.nfev, 'modes_kept': modes_kept,
                   'pre_forcing_maximum_state': float(np.max(np.abs(solution.y[:, solution.t < 0]))),
                   'initial_time': float(solution.t[0]), 'source_switch_on_time': 0.,
                   'energy_solution_difference_over_peak': float(np.max(np.abs(energies[8:]-sampled['energy']))/peak_energy),
                   'traction_solution_difference_over_peak': float(np.max(np.abs(tractions[8:]-sampled['p']))/np.max(np.abs(sampled['p']))),
                   'ODE_work_energy_error_over_peak': float(np.max(np.abs(solution.y[-1]-energies))/peak_energy),
                   'reference': 'Direct DOP853 integration driven by independently differentiated sin^6 pulse, versus modal cosine convolution.'}
    assert integration['pre_forcing_maximum_state'] == 0, integration
    assert max(integration[key] for key in ['energy_solution_difference_over_peak',
               'traction_solution_difference_over_peak', 'ODE_work_energy_error_over_peak']) < 2e-8, integration
    mp.mp.dps = 80
    high_precision_rows = []
    prior = json.loads((ROOT/'results/pulses/status.json').read_text(encoding='utf-8'))
    for duration in [4, 16, 64]:
        end = mp.mpf(duration)
        carrier_mp = mp.mpf('0.25')
        frequencies = [carrier_mp+multiple*mp.pi/end for multiple in [0, 2, -2, 4, -4, 6, -6]]
        coefficients = [mp.mpf(numerator)/denominator for numerator, denominator in [(10, 32), (-15, 64), (-15, 64),
                                                                                   (3, 32), (3, 32), (-1, 64), (-1, 64)]]
        energy = mp.mpf(0)
        for eigenvalue, amplitude in zip(model['eigenvalues'][:128], model['coupling'][:128]):
            eigenvalue, amplitude = mp.mpf(str(eigenvalue)), mp.mpf(str(amplitude))
            natural = mp.sqrt(eigenvalue)
            position, velocity = mp.mpf(0), mp.mpf(0)
            for frequency, coefficient in zip(frequencies, coefficients):
                factor = amplitude*coefficient*frequency**2/(eigenvalue-frequency**2)
                position += factor*(mp.cos(frequency*end)-mp.cos(natural*end))
                velocity += factor*(-frequency*mp.sin(frequency*end)+natural*mp.sin(natural*end))
            energy += (velocity**2+eigenvalue*position**2)/2
        binary = next(row['energy_after_pulse'] for row in prior['rows']
                      if row['duration'] == duration and row['cells'] == 256 and row['time_samples'] == 8193)
        high_precision_rows.append({'duration': duration, 'energy_after_pulse_80digit_algebra': str(energy),
                                    'binary64_relative_error': float(abs(mp.mpf(str(binary))/energy-1))})
    output = ROOT/'results/time-domain-control'
    output.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(output/'direct-ODE.npz', time=solution.t, states=solution.y, energy=energies, traction=tractions)
    inputs = [path, ROOT/'run_pulses.py', ROOT/'results/pulses/status.json']
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in inputs},
              'integration_control': integration, 'high_precision_controls': high_precision_rows,
              'archive_sha256': digest(output/'direct-ODE.npz'),
              'precision_scope': '80-digit final modal algebra with binary64 spectral inputs; not80-digit continuum eigenvalues.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(integration))
    print(json.dumps(high_precision_rows))


if __name__ == '__main__':
    main()
