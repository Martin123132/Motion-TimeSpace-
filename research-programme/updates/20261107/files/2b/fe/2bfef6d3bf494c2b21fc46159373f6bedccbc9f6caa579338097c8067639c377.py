from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil

from dynamic_system import BRANCH, DynamicProblem, Profile, ROOT


sys.path.insert(0, str(BRANCH/'gravitating-tides-20261004'))
from solve_tides import exterior_coefficients


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--nominal', type=float, default=.03)
    parser.add_argument('--sigmas', nargs='+', type=float, default=[0., .005, .01, .015, .02, .025, .03])
    parser.add_argument('--distance', type=float, default=.01)
    parser.add_argument('--tolerance', type=float, default=2e-7)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    profile = Profile(20., args.nominal)
    report = {'state': 'running', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'dynamic_system.py').read_bytes()).hexdigest(),
              'arguments': vars(args), 'profile_path': str(profile.path), 'profile_sha256': hashlib.sha256(profile.path.read_bytes()).hexdigest(), 'rows': []}
    previous = None
    try:
        for sigma in args.sigmas:
            problem = DynamicProblem(profile, sigma, args.distance, args.tolerance)
            solution = problem.solve(previous)
            archive = f'sigma{sigma:g}.npz'
            np.savez_compressed(output/archive, spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p, scales=problem.scales, radius=profile.radius, alpha=profile.alpha, sigma=sigma)
            row = {'sigma': sigma, 'converged': bool(solution.success), 'message': solution.message, 'nodes': len(solution.x), 'archive': archive,
                   'maximum_rms_residual': float(max(solution.rms_residuals)), 'boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p))))}
            if solution.success:
                time_value, time_derivative, master, master_star_prime = problem.surface(solution)
                growing, decaying = exterior_coefficients(profile.radius, problem.mass, time_value, time_derivative)
                row.update({'H_surface': float(time_value), 'Hprime_surface': float(time_derivative), 'master_surface': float(master), 'master_star_prime_surface': float(master_star_prime),
                            'master_log_derivative': float(master_star_prime/master),
                            'static_basis_lambda_diagnostic': float(decaying/(3*growing)), 'static_basis_valid_as_Love_only_at_zero_sigma': True,
                            'phase_surface': float(solution.p[1]*profile.radius**6), 'edge_amplitude': float(solution.p[0]*profile.radius**4)})
                previous = solution
            report['rows'].append(row)
            (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
            print(json.dumps(row), flush=True)
            assert solution.success, solution.message
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
