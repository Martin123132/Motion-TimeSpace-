from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from companion_system import CompanionProblem, ROOT, encode, reference_wave


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--separations', type=float, nargs='+', default=[1.1, 1.5, 2., 3., 5., 10., 20., 40.])
    parser.add_argument('--reference-only', action='store_true')
    parser.add_argument('--distance', type=float, default=.02)
    parser.add_argument('--interior-tolerance', type=float, default=2e-8)
    parser.add_argument('--far-phase', type=float, default=40.)
    parser.add_argument('--outer-order', type=int, default=10)
    parser.add_argument('--horizon-epsilon', type=float, default=1e-5)
    parser.add_argument('--horizon-order', type=int, default=6)
    parser.add_argument('--tolerance', type=float, default=2e-12)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    report = {'state': 'running', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'companion_system.py').read_bytes()).hexdigest(), 'arguments': vars(args), 'rows': []}
    try:
        if args.reference_only:
            for orbit, reference_flux in [(7.9456, 1.7063e-4), (46.062, 2.8650e-8), (1000., None), (4000., None)]:
                full = reference_wave(orbit, 1., far_phase=args.far_phase, outer_order=args.outer_order,
                                      horizon_epsilon=args.horizon_epsilon, horizon_order=args.horizon_order, tolerance=args.tolerance)
                row = {key: value for key, value in full.items() if key not in ['outgoing', 'horizon']}
                row.update({'orbit_over_mass': orbit, 'published_pair_flux': reference_flux,
                            'quadrupole_ratio': full['pair_power_infinity_per_geometric_particle_mass_squared']/(32/5/orbit**5),
                            'published_relative_difference': abs(full['pair_power_infinity_per_geometric_particle_mass_squared']/reference_flux-1) if reference_flux else None})
                report['rows'].append(encode(row))
                print(json.dumps(encode(row)), flush=True)
        else:
            problem = CompanionProblem(args.distance, args.interior_tolerance, args.far_phase, args.outer_order,
                                       args.horizon_epsilon, args.horizon_order, args.tolerance)
            for separation in args.separations:
                row, solution = problem.evaluate(separation)
                archive = f'D{separation:g}.npz'
                np.savez_compressed(output/archive, spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p, sigma=row['sigma'])
                row['archive'] = archive
                report['rows'].append(encode(row))
                print(json.dumps(encode(row)), flush=True)
                (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        report['state'] = 'complete'
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error)})
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
