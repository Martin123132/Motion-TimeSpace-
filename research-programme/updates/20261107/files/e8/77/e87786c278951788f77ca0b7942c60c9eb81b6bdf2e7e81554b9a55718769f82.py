from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from dynamic_system import Profile, ROOT
from dynamic_system_v2 import DynamicProblem as ComplexProblem
from dynamic_system_v3 import DynamicProblem as RealProblem


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/solver-comparison'
    output.mkdir(exist_ok=False)
    rows = []
    profile = Profile(20., .03)
    for name, constructor in [('complex', ComplexProblem), ('realified', RealProblem)]:
        problem = constructor(profile, .0204566-1e-6j, .005, 2e-9)
        solution = problem.solve()
        order = np.argsort(solution.rms_residuals)[-8:]
        np.savez_compressed(output/f'{name}.npz', spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p, residuals=solution.rms_residuals, mesh=solution.x)
        rows.append({'method': name, 'converged': bool(solution.success), 'nodes': len(solution.x), 'maximum_rms_residual': float(max(solution.rms_residuals)),
                     'worst_residual_locations': solution.x[order].tolist(), 'boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p))))})
        print(json.dumps(rows[-1]), flush=True)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'rows': rows,
              'scope': 'Numerical implementation diagnostic; any nonconverged solution is excluded from physics conclusions.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
