from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import solve_bvp

from dynamic_system import DynamicProblem, Profile, ROOT, edge_state


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--distance', type=float, default=.005)
    parser.add_argument('--tolerance', type=float, default=2e-9)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    profile = Profile(20., 0.)
    problem = DynamicProblem(profile, .01881, args.distance, args.tolerance)
    scales = problem.scales[2:]

    def equation(coordinate, state, parameters):
        problem.square = parameters[2]**2
        full = np.vstack([np.zeros((2, len(coordinate))), state*scales[:, None]])
        derivative = problem.physical_evolution(profile.radius*coordinate, full)[0][2:]
        return derivative*profile.radius/scales[:, None]

    def boundary(left, right, parameters):
        expected = edge_state(profile.radius, 0., profile.frequency, parameters[2]**2, args.distance, parameters[0]*profile.radius**4, parameters[1]*profile.radius**6, np.zeros(2))[2:]/scales
        residual = right-expected
        residual[0] /= args.distance**2
        residual[1] /= profile.radius*args.distance
        return np.r_[left[1]-2*left[0]/problem.lower, left[3]-2*left[2]/problem.lower, residual, parameters[0]+.01]

    mesh = np.unique(np.r_[np.linspace(problem.lower, problem.upper, 500), np.linspace(.4, problem.upper, 500)])
    guess = np.vstack([-.01*mesh**2*(1-mesh)**2, -.02*mesh*(1-mesh)*(1-2*mesh), -.002*mesh**2, -.004*mesh])
    solution = solve_bvp(equation, boundary, mesh, guess, p=[-.01, -.002, .0188117], tol=args.tolerance, bc_tol=args.tolerance/10, max_nodes=16000)
    np.savez_compressed(output/'mode.npz', spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p, scales=scales)
    assert solution.success, solution.message
    source = ROOT.parent/'quadrupole-response-20261004/results/quadratic-fine/status.json'
    data = json.loads(source.read_text())
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'dynamic_system.py').read_bytes()).hexdigest(),
              'arguments': vars(args), 'sigma': float(solution.p[2]), 'nodes': len(solution.x), 'maximum_rms_residual': float(max(solution.rms_residuals)),
              'maximum_boundary_residual': float(max(abs(boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
              'previous_spectrum_path': str(source), 'previous_spectrum_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'prior_reported_flat_frequency': .0188117251133, 'relative_frequency_difference': float(abs(solution.p[2]/.0188117251133-1)),
              'scope': 'Independent moving-edge collocation of the flat gyroscopic eigenproblem; metric perturbations zero, no exterior gravity mode substituted for scalar mode.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
