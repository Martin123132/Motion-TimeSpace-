from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import time

import numpy as np
import psutil

from acquire_source import digest
from axial_binary import ROOT, BRANCH, AxialCompanion, outgoing_samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    fine = arguments.label == 'fine'
    interior = {'tolerance': 3e-12 if fine else 1e-10, 'max_step': 1/240 if fine else 1/100, 'start': 1e-5 if fine else 2e-5}
    exterior = {'tolerance': 3e-12 if fine else 1e-10, 'far_phase': 80. if fine else 50., 'order': 14 if fine else 10,
                'horizon_epsilon': 3e-6 if fine else 1e-5}
    problem = AxialCompanion(interior, exterior)
    inputs = [problem.body.profile.path, BRANCH/'dynamical-axial-20261004/results/stage-integrity.json',
              BRANCH/'axial-tides-20261004/results/fine-v2/status.json',
              BRANCH/'dynamical-axial-20261004/axial_wave.py', ROOT/'axial_binary.py']
    rows = []
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for separation in [5., 10., 20., 40., 80., 160.]:
            row = problem.evaluate(separation)
            rows.append(row)
            progress = {'state': 'running', 'completed_rows': len(rows), 'elapsed_seconds': time.monotonic()-started,
                        'separation_over_radius': separation, 'infinity_increment_to_leading': row['infinity_increment_to_leading_magnetic']}
            log.write(json.dumps(progress)+'\n')
            (output/'progress.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
            print(json.dumps(progress), flush=True)
        flat_checks = []
        for frequency in [.003, .03, .3]:
            samples, normalization, diagnostics = outgoing_samples(0., frequency, [1., 10.], exterior['far_phase'], exterior['order'], exterior['tolerance'])
            for radius in [1., 10.]:
                argument = frequency*radius
                exact = np.exp(1j*argument)*(1+3j/argument-3/argument**2)
                flat_checks.append({'frequency': frequency, 'radius': radius,
                                    'outgoing_amplitude_error': float(abs(samples[radius][0]*normalization/exact-1)),
                                    'flux_normalization_error': diagnostics['infinity_flux_normalization_error']})
        report = {'state': 'complete', 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': digest(__file__), 'system_sha256': digest(ROOT/'axial_binary.py'),
                  'input_hashes': {str(path): digest(path) for path in inputs},
                  'interior_settings': interior, 'exterior_settings': exterior,
                  'body_mass': problem.mass, 'body_radius': problem.radius,
                  'response_R_B': problem.response, 'sigma_bar': problem.sigma,
                  'rows': rows, 'flat_checks': flat_checks,
                  'particle_mass_convention': 'Powers divided by geometric mu^2; test-mass limit, not mu=1 physical binary.',
                  'fixed_geodesic_Omega_squared': 'M/D^3, no total-mass replacement or fitted orbit correction',
                  'asymptotic_normalization_input_to_wave_solve': False, 'elapsed_seconds': time.monotonic()-started}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        with (output/'rows.csv').open('x', newline='', encoding='utf-8') as handle:
            keys = [key for key in rows[0] if not isinstance(rows[0][key], dict)]
            writer = csv.DictWriter(handle, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        progress = {'state': 'complete', 'script_sha256': digest(__file__), 'completed_rows': len(rows), 'elapsed_seconds': time.monotonic()-started}
        (output/'progress.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
        (output/'COMPLETE').write_text(report['completed_at_utc']+'\n', encoding='utf-8')
        log.write(json.dumps(progress)+'\n')
    print(json.dumps(progress), flush=True)


if __name__ == '__main__':
    main()
