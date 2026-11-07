from __future__ import annotations

from datetime import datetime, timezone
import json
import time

import numpy as np
from numpy.polynomial.legendre import leggauss
import psutil
from scipy.integrate import solve_ivp

from wave_network import ROOT, BRANCH, WaveBody, outgoing_samples, horizon_samples, wave_potential, digest


def source_transform(frequency):
    duration, carrier = 12., .5
    harmonics = carrier+np.pi/duration*np.array([0., 2., -2., 4., -4., 6., -6.])
    coefficients = np.array([10/32, -15/64, -15/64, 3/32, 3/32, -1/64, -1/64])
    arguments_plus = (frequency+harmonics)*duration/2
    arguments_minus = (frequency-harmonics)*duration/2
    return duration/2*np.sum(coefficients*(np.exp(1j*arguments_plus)*np.sinc(arguments_plus/np.pi)
                                          +np.exp(1j*arguments_minus)*np.sinc(arguments_minus/np.pi)))


def infinite_pair(body, frequency):
    source_radius = 2.5*body.radius
    compactness = 2*body.mass/body.radius
    source_tortoise = 1.5+compactness*np.log((2.5-compactness)/(1-compactness))
    physical = frequency/body.radius
    outgoing, raw_out, _ = outgoing_samples(body.mass, physical, [source_radius], 65., 16, 8e-14)
    horizon, raw_horizon, _ = horizon_samples(body.mass, physical, [source_radius], 2e-6, 16, 8e-14)
    outgoing_slope = body.radius*complex(outgoing[source_radius][1].real, physical/abs(raw_out)**2)
    horizon_slope = body.radius*complex(horizon[source_radius][1].real, -physical/abs(raw_horizon)**2)
    response, _ = body.solve(frequency, tolerance=8e-14, max_step=1/360, start=5e-6)

    def equation(position, state):
        return [state[1], (wave_potential(position, compactness)-frequency**2)*state[0]]

    solution = solve_ivp(equation, [0., source_tortoise], [1., response['Y']], method='DOP853', rtol=8e-14, atol=8e-16)
    assert solution.success
    body_slope = solution.y[1, -1]/solution.y[0, -1]
    body_green = 1/(body_slope-outgoing_slope)
    horizon_green = 1/(horizon_slope-outgoing_slope)
    difference = (horizon_slope-body_slope)/((body_slope-outgoing_slope)*(horizon_slope-outgoing_slope))
    return body_green, horizon_green, difference


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    body = WaveBody(.03)
    output = ROOT/'results/spectral-work'
    output.mkdir(parents=True, exist_ok=False)
    rows, settings = [], []
    started = time.monotonic()
    for order, intervals in [(24, [(0., 3.), (3., 6.), (6., 9.)]),
                              (36, [(0., 3.), (3., 6.), (6., 9.), (9., 12.)])]:
        abscissas, weights = leggauss(order)
        total_body, total_horizon, total_difference = 0., 0., 0.
        bands = []
        for lower, upper in intervals:
            sums = np.zeros(3)
            for node, weight in zip(abscissas, weights):
                frequency = (upper+lower)/2+(upper-lower)*node/2
                greens = infinite_pair(body, float(frequency))
                multiplier = frequency*abs(source_transform(frequency))**2/np.pi
                integrands = np.array([value.imag for value in greens])*multiplier
                sums += weight*(upper-lower)/2*integrands
                rows.append({'order': order, 'frequency_R': float(frequency), 'body_integrand': float(integrands[0]),
                             'BH_integrand': float(integrands[1]), 'difference_integrand': float(integrands[2])})
            total_body += sums[0]
            total_horizon += sums[1]
            total_difference += sums[2]
            bands.append({'lower': lower, 'upper': upper, 'body_work': float(sums[0]), 'BH_work': float(sums[1]),
                          'difference_work': float(sums[2])})
            print(json.dumps({'state': 'running', 'order': order, 'band': [lower, upper],
                              'body_work': float(sums[0]), 'difference_work': float(sums[2])}), flush=True)
        settings.append({'order_per_band': order, 'cutoff_frequency_R': intervals[-1][-1],
                         'body_work': float(total_body), 'BH_work': float(total_horizon),
                         'difference_work': float(total_difference), 'bands': bands})
    inputs = [body.profile.path, ROOT/'wave_network.py', BRANCH/'dynamical-axial-20261004/axial_wave.py',
              BRANCH/'axial-companion-20261005/axial_binary.py']
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': {str(path): digest(path) for path in inputs},
              'settings': settings, 'sampled_integrands': rows, 'elapsed_seconds': time.monotonic()-started,
              'formula': 'W=(1/pi)*integral_0^infinity k*ImG(k)*abs(g_transform(k))^2 dk',
              'scope': 'Independent continuum, true-outgoing/ingoing ODE comparison. Finite quadrature cutoff tested, not a rigorous infinite-frequency tail bound.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(json.dumps({'state': 'complete', 'elapsed_seconds': report['elapsed_seconds'], 'work': settings[-1]}))


if __name__ == '__main__':
    main()
