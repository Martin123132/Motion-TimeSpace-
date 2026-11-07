from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import psutil

from orbit_system import ROOT, PARENT, CompanionProblem, action_from_wave, static_lambda, encode


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def archive(output, name, solution, sigma):
    path = output/(name+'.npz')
    np.savez_compressed(path, spline_knots=solution.sol.x, spline_coefficients=solution.sol.c,
                        parameters=solution.p, sigma=sigma)
    return path.name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--control', action='store_true')
    parser.add_argument('--derivatives', action='store_true')
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    settings = dict(distance=.02 if arguments.control else .04, interior_tolerance=2e-8 if arguments.control else 5e-9,
                    far_phase=40. if arguments.control else 60., outer_order=10 if arguments.control else 12,
                    horizon_epsilon=1e-5 if arguments.control else 3e-6, horizon_order=6 if arguments.control else 8,
                    tolerance=2e-12 if arguments.control else 5e-13)
    problem = CompanionProblem(**settings)
    tidal_lambda, solution = static_lambda(problem)
    archive(output, 'static', solution, 0.)
    report = {'state': 'running', 'script_sha256': digest(__file__), 'system_sha256': digest(ROOT/'orbit_system.py'),
              'arguments': vars(arguments), 'settings': settings, 'tidal_lambda': tidal_lambda,
              'radius': problem.radius, 'mass': problem.mass, 'rows': [], 'derivative_rows': [], 'new_interiors': 1,
              'parent_input_hashes': {}, 'started_utc': datetime.now(timezone.utc).isoformat()}

    def save():
        (output/'status.json').write_text(json.dumps(encode(report), indent=2, allow_nan=False), encoding='utf-8')

    save()
    for parent_label in (['main', 'wide-control'] if arguments.control else ['fine', 'wide']):
        path = PARENT/f'results/{parent_label}/status.json'
        parent = json.loads(path.read_text())
        report['parent_input_hashes'][str(path)] = digest(path)
        for row in parent['rows']:
            result = action_from_wave(row, tidal_lambda, settings)
            result['parent_label'] = parent_label
            report['rows'].append(result)
            save()
            print(json.dumps({'kind': 'saved_wave_reconstruction', **result}), flush=True)
    if arguments.derivatives:
        for center in [2., 5., 10.]:
            values = {}
            for offset in [-4, -2, -1, 0, 1, 2, 4]:
                logarithmic_offset = .005*offset
                separation = center*np.exp(-2*logarithmic_offset/3)
                wave, solution = problem.evaluate(separation)
                result = action_from_wave(wave, tidal_lambda, settings)
                result['offset_log_omega'] = logarithmic_offset
                result['center_separation_over_radius'] = center
                result['archive'] = archive(output, f'D{center:g}-offset{offset:+d}', solution, wave['sigma'])
                result['wave'] = wave
                values[offset] = result
                report['derivative_rows'].append(result)
                report['new_interiors'] += 1
                save()
                print(json.dumps({'kind': 'frequency_derivative_node', 'center': center, 'offset': offset, 'ratio': result['action_over_leading']}), flush=True)
            derivatives = []
            for stride in [1, 2]:
                step = .005*stride
                ratio = lambda index: values[index]['action_over_leading']
                first = (ratio(-2*stride)-8*ratio(-stride)+8*ratio(stride)-ratio(2*stride))/(12*step)
                second = (-ratio(-2*stride)+16*ratio(-stride)-30*ratio(0)+16*ratio(stride)-ratio(2*stride))/(12*step**2)
                central = values[0]
                leading = 1.5*tidal_lambda/central['orbit']**6
                derivatives.append({'log_omega_step': step, 'ratio_first_derivative': first, 'ratio_second_derivative': second,
                                    'energy_over_leading_static_energy': ratio(0)+first/3,
                                    'angular_momentum_over_leading_static_angular_momentum': ratio(0)+first/4,
                                    'energy_per_particle_squared': leading*(3*ratio(0)+first),
                                    'angular_momentum_per_particle_squared': leading/central['omega']*(4*ratio(0)+first),
                                    'd_energy_d_log_omega_per_particle_squared': leading*(12*ratio(0)+7*first+second)})
            report.setdefault('derivatives', []).append({'separation_over_radius': center, 'estimates': derivatives})
            save()
    report['state'] = 'complete'
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    save()
    (output/'COMPLETE').write_text('Completed conservative action and selected frequency derivatives.\n', encoding='utf-8')
    print(json.dumps({'state': 'complete', 'label': arguments.label, 'new_interiors': report['new_interiors']}))


if __name__ == '__main__':
    main()
