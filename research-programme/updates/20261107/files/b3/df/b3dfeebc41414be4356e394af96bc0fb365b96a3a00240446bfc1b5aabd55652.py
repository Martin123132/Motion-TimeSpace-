from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import time

import numpy as np
import psutil
from scipy.optimize import approx_fprime

from acquire_source import digest
from axial_action import ROOT, BRANCH, ActionProblem


def derivatives(samples, step):
    ordered = np.array(samples)
    first = np.dot(np.array([-1, 9, -45, 0, 45, -9, 1], dtype=float), ordered)/(60*step)
    second = np.dot(np.array([2, -27, 270, -490, 270, -27, 2], dtype=float), ordered)/(180*step**2)
    return first, second


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    fine = arguments.label == 'fine'
    interior = {'tolerance': 8e-14 if fine else 3e-12, 'max_step': 1/360 if fine else 1/240, 'start': 5e-6 if fine else 1e-5}
    exterior = {'tolerance': 8e-14 if fine else 3e-12, 'far_phase': 65. if fine else 80.,
                'order': 16 if fine else 14, 'horizon_epsilon': 2e-6 if fine else 3e-6}
    problem = ActionProblem(interior, exterior)
    cache = {}
    started = time.monotonic()

    def evaluate(separation):
        key = float(separation)
        if key not in cache:
            cache[key] = problem.evaluate(key)
        return cache[key]

    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        rows = []
        for separation in [1.1, 1.5, 2., 3., 5., 10., 20., 40., 80., 160.]:
            row = evaluate(separation)
            rows.append(row)
            message = {'state': 'running', 'stage': 'radial_grid', 'D_over_R': separation,
                       'action_ratio': row['action_over_leading'], 'optical_error': row['optical_identity_error_over_component_sum']}
            log.write(json.dumps(message)+'\n')
            print(json.dumps(message), flush=True)
        derivative_rows = []
        step = .01
        offsets = [-6, -4, -3, -2, -1, 0, 1, 2, 3, 4, 6]
        for separation in [2., 5., 10.]:
            center = evaluate(separation)
            nodes = {offset: evaluate(separation*np.exp(-2*offset*step/3)) for offset in offsets}
            for multiplier in [1, 2]:
                actual_step = multiplier*step
                selected = [nodes[index*multiplier]['action_real_per_mu_squared'] for index in range(-3, 4)]
                first, second = derivatives(selected, actual_step)
                energy = first-center['action_real_per_mu_squared']
                momentum = first/center['Omega']
                energy_log_slope = second-first
                leading = center['leading_action_per_mu_squared']
                leading_energy = 11/3*leading
                leading_momentum = 14/3*leading/center['Omega']
                row = {'separation_over_radius': separation, 'log_frequency_step': actual_step,
                       'Omega': center['Omega'], 'action_per_mu_squared': center['action_real_per_mu_squared'],
                       'log_frequency_action_derivative': float(first), 'log_frequency_second_derivative': float(second),
                       'energy_per_mu_squared': float(energy), 'angular_momentum_per_mu_squared': float(momentum),
                       'energy_log_frequency_slope_per_mu_squared': float(energy_log_slope),
                       'energy_over_leading': float(energy/leading_energy),
                       'angular_momentum_over_leading': float(momentum/leading_momentum),
                       'energy_first_PN_ratio': float(1+208/33*center['x']),
                       'momentum_first_PN_ratio': float(1+128/21*center['x']),
                       'redshift_legendre_identity_error': float(abs((center['Omega']*momentum-energy)/center['action_real_per_mu_squared']-1)),
                       'minimum_sampled_D_over_R': min(node['separation_over_radius'] for node in nodes.values())}
                derivative_rows.append(row)
            message = {'state': 'running', 'stage': 'frequency_derivatives', 'D_over_R': separation, 'completed_wave_solves': len(cache)}
            log.write(json.dumps(message)+'\n')
            print(json.dumps(message), flush=True)
        inputs = [problem.body.profile.path, BRANCH/'axial-companion-20261005/axial_binary.py',
                  BRANCH/'dynamical-axial-20261004/axial_wave.py', BRANCH/'axial-tail-balance-20261005/results/stage-integrity.json',
                  ROOT/'axial_action.py']
        report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': digest(__file__), 'system_sha256': digest(ROOT/'axial_action.py'),
                  'input_hashes': {str(path): digest(path) for path in inputs},
                  'body_mass': problem.mass, 'body_radius': problem.radius, 'sigma_bar': problem.sigma,
                  'interior_settings': interior, 'exterior_settings': exterior,
                  'grid_rows': rows, 'derivative_rows': derivative_rows, 'all_wave_rows': list(cache.values()),
                  'new_background_solves': 0, 'new_fitted_coefficients': 0, 'elapsed_seconds': time.monotonic()-started}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        for name, selected in [('action-grid', rows), ('frequency-derivatives', derivative_rows)]:
            fields = [key for key, value in selected[0].items() if not isinstance(value, dict)]
            with (output/f'{name}.csv').open('x', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(selected)
        (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
        log.write(json.dumps({'state': 'complete', 'wave_solves': len(cache), 'elapsed_seconds': report['elapsed_seconds']})+'\n')
    print(json.dumps({'state': 'complete', 'wave_solves': len(cache), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
