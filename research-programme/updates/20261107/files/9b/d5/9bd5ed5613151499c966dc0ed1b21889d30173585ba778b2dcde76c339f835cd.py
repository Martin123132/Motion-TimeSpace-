from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import time

import numpy as np
import psutil

from wave_network import ROOT, BRANCH, build_network, continuum_response, digest, evolve, harmonic_response


SETTINGS = {
    'coarse': {'outer': 40., 'inner': -2., 'exterior_step': .1, 'interior_step': .004, 'modes': 32, 'time_step': .01},
    'fine': {'outer': 40., 'inner': -2., 'exterior_step': .05, 'interior_step': .002, 'modes': 64, 'time_step': .005},
    'far': {'outer': 60., 'inner': -2.1, 'exterior_step': .05, 'interior_step': .002, 'modes': 64, 'time_step': .005},
    'time-control': {'outer': 40., 'inner': -2., 'exterior_step': .05, 'interior_step': .002, 'modes': 64, 'time_step': .0025}
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=list(SETTINGS), required=True)
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    rows, inputs = [], {}
    settings = SETTINGS[arguments.label]
    with (output/'log.txt').open('x', encoding='utf-8', buffering=1) as log:
        for kind in ['body', 'BH']:
            network = build_network(kind, settings)
            print(json.dumps({'state': 'running', 'label': arguments.label, 'kind': kind, 'unknowns': network['mass'].shape[0]}), flush=True)
            arrays, summary = evolve(network, settings['time_step'])
            np.savez_compressed(output/f'{kind}.npz', **arrays)
            summary.update({'kind': kind, 'harmonic_rows': [harmonic_response(network, frequency) for frequency in [.3, .6, 1.2]],
                            'continuum_rows': [continuum_response(network, frequency) for frequency in [.3, .6, 1.2]],
                            'source_tortoise': network['source_tortoise'], 'compactness': network['compactness'],
                            'archive_sha256': digest(output/f'{kind}.npz')})
            if kind == 'body':
                summary['wrong_surface_contact_control'] = harmonic_response(network, .6, wrong_surface_contact=True)
            rows.append(summary)
            inputs[str(network['archive_path'])] = digest(network['archive_path'])
            log.write(json.dumps({'kind': kind, 'final_work': summary['final_work'],
                                  'balance_error': summary['total_balance_error_over_peak_work']})+'\n')
            print(json.dumps({'kind': kind, 'final_work': summary['final_work'], 'outer_loss': summary['final_outer_loss'],
                              'horizon_loss': summary['final_horizon_loss'], 'balance_error': summary['total_balance_error_over_peak_work']}), flush=True)
        for path in [ROOT/'wave_network.py', BRANCH/'causal-axial-20261005/results/stage-integrity.json',
                     BRANCH/'dynamical-axial-20261004/axial_wave.py', BRANCH/'axial-companion-20261005/axial_binary.py']:
            inputs[str(path)] = digest(path)
        report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': digest(__file__), 'input_hashes': inputs, 'settings': settings, 'rows': rows,
                  'elapsed_seconds': time.monotonic()-started, 'new_background_solves': 0, 'new_fitted_parameters': 0,
                  'forcing': 'unit delta source at r/R=2.5 with sin^6 windowT12,carrier0.5,starttau2; one real quadrature',
                  'source_scope': 'Externally driven master-source experiment, not an orbiting-companion stress tensor.',
                  'boundary_scope': 'Finite Sommerfeld extraction surfaces; exact-infinity comparison is separately recorded.',
                  'energy_units': 'Ehat; physical energy=kappa/R times Ehat, kappa=3/(4*pi).'}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        (output/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(json.dumps({'state': 'complete', 'label': arguments.label, 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
