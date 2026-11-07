from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from response_system_v3 import ResponseProblem, ROOT, encode


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--sigmas', nargs='+', type=float, default=[0., .0001, .0002, .0004, .002, .01, .018, .0204, .0204566, .0205, .023])
    parser.add_argument('--distance', type=float, default=.02)
    parser.add_argument('--tolerance', type=float, default=2e-8)
    parser.add_argument('--far-phase', type=float, default=40.)
    parser.add_argument('--order', type=int, default=10)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    problem = ResponseProblem(args.distance, args.tolerance, args.far_phase, args.order)
    report = {'state': 'running', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'response_system_v3.py').read_bytes()).hexdigest(), 'arguments': vars(args), 'rows': []}
    try:
        for sigma in args.sigmas:
            row, solution = problem.evaluate(sigma)
            archive = f'sigma{sigma:g}.npz'
            np.savez_compressed(output/archive, spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p, sigma=sigma)
            row['archive'] = archive
            report['rows'].append(encode(row))
            (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
            print(json.dumps(encode({'sigma': sigma, 'responses': [item['susceptibility'] for item in row['rows']],
                                    'green_errors': [item['green_identity_error'] for item in row['rows']], 'diagnostics': row['outgoing_diagnostics']})), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error)})
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
