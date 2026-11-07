from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time

import numpy as np
import psutil

from sequence_tools_v3 import GRAVITY, PULSATION, SequenceBody, SequenceProfile, digest, load_solution, save_solution, signed_spectrum


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--charge-factors', nargs='*', type=float, default=[1., 1.25, 1.6, 2., 3.])
    parser.add_argument('--central-targets', nargs='*', type=float, default=[])
    parser.add_argument('--start-status')
    parser.add_argument('--start-index', type=int, default=-1)
    parser.add_argument('--tol', type=float, default=2e-7)
    parser.add_argument('--floor', type=float, default=1e-9)
    parser.add_argument('--cells', type=int, default=192)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(parents=True, exist_ok=False)
    body = SequenceBody(args.floor, args.tol)
    if args.start_status:
        start_path = Path(args.start_status)
        start_report = json.loads(start_path.read_text(encoding='utf-8'))
        start_row = start_report['rows'][args.start_index]
        seed_path = start_path.parent/start_row['archive']
    else:
        seed_path = GRAVITY/'results/fine'/body.seed_row['archive']
    previous = load_solution(seed_path)
    fixed_alpha = body.alpha
    started = time.monotonic()
    report = {'state': 'running', 'arguments': vars(args), 'fixed_alpha': fixed_alpha,
              'seed_path': str(seed_path), 'seed_sha256': digest(seed_path),
              'script_sha256': digest(Path(__file__)), 'helper_sha256': digest(ROOT/'sequence_tools_v3.py'), 'base_helper_sha256': digest(ROOT/'sequence_tools.py'),
              'parent_seal_sha256': digest(PULSATION/'results/stage-integrity.json'),
              'started': datetime.now(timezone.utc).isoformat(), 'rows': [], 'attempts': []}
    targets = [('charge', factor*body.seed_row['charge']) for factor in args.charge_factors]
    targets += [('central', target) for target in args.central_targets]
    try:
        for index, (kind, target) in enumerate(targets):
            trial_started = time.monotonic()
            solution = body.continue_from(previous, target_charge=target if kind == 'charge' else None,
                                          target_central=target if kind == 'central' else None)
            archive = f'body-{index:03d}-{kind}-{target:.10g}'.replace('.', 'p')+'.npz'
            save_solution(output/archive, body, solution)
            report['attempts'].append({'index': index, 'kind': kind, 'target': target, 'archive': archive,
                                       'converged': bool(solution.success), 'message': solution.message,
                                       'seconds': time.monotonic()-trial_started})
            if not solution.success:
                raise RuntimeError(f'BVP did not converge: {kind}={target}; {solution.message}')
            row = body.measured(solution)
            row['archive'] = archive
            row['control_kind'] = kind
            row['control_value'] = target
            row['target_charge_relative_error'] = float(abs(row['charge']/target-1)) if kind == 'charge' else None
            assert body.alpha == fixed_alpha and row['minimum_F'] > 0
            assert row['charge_accumulation_relative_error'] < 1e-7
            assert row['mass_quadrature_relative_error'] < 1e-7 and row['komar_adm_relative_error_without_tiny_tail'] < 1e-6
            profile = SequenceProfile(output/archive, row)
            spectrum_name = archive.replace('body-', 'modes-')
            row['spectrum'] = signed_spectrum(profile, args.cells, output=output/spectrum_name)
            row['spectrum_archive'] = spectrum_name
            report['rows'].append(row)
            (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
            print(json.dumps({key: row[key] for key in ['control_kind', 'control_value', 'charge', 'adm_energy', 'radius',
                             'central_amplitude', 'central_density', 'surface_compactness', 'minimum_F', 'spectrum']}), flush=True)
            previous = solution
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        report['elapsed_seconds'] = time.monotonic()-started
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
