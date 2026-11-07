from __future__ import annotations

from datetime import datetime, timezone
import time

import numpy as np

from susceptibility import ROOT, BRANCH, Profile, TangentProblem, read_json, write_json, digest, dependencies, modest_process


def main():
    modest_process()
    directory = ROOT/'results/tangent'
    directory.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    profile = Profile(20., .03)
    inputs = {str(profile.path):digest(profile.path)}
    cases = [('coarse', .02, 2e-8, 'coarse'), ('fine', .04, 5e-9, 'fine'),
             ('refined', .04, 1e-9, 'fine'), ('edge_check', .03, 3e-9, 'fine')]
    rows = []
    for label, distance, tolerance, archived_label in cases:
        archive = BRANCH/'conservative-eccentric-action-20261005/results/archives'/('static-interior-'+archived_label+'.npz')
        inputs[str(archive)] = digest(archive)
        problem = TangentProblem(profile, distance, tolerance)
        solution = problem.solve(archive)
        assert solution.success, (label, solution.message)
        result = problem.surface(solution)
        points = (solution.x[:-1]+solution.x[1:])/2
        residual = solution.sol(points, 1)-problem.equation(points, solution.sol(points), solution.p)
        scale = 1+abs(problem.equation(points, solution.sol(points), solution.p))
        row = dict(label=label, distance=distance, tolerance=tolerance, nodes=len(solution.x), iterations=solution.niter,
            maximum_rms_residual=float(max(solution.rms_residuals)),
            midpoint_scaled_ode_residual=float(np.max(abs(residual)/scale)),
            maximum_boundary_residual=float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
            normalization_derivative=float(solution.p[6]), **result)
        payload = directory/(label+'.npz')
        with payload.open('xb') as handle:
            np.savez_compressed(handle, spline_knots=solution.sol.x, spline_coefficients=solution.sol.c,
                parameters=solution.p, scales=problem.base.scales, boundary_tangent=problem.tangent_parameter,
                radius=profile.radius, mass=profile.alpha*profile.mass)
        rows.append(row)
        print(row, flush=True)
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-started,
        script_sha256=digest(__file__), input_hashes={**inputs, **dependencies()}, rows=rows,
        mass=profile.alpha*profile.mass, radius=profile.radius, background_frequency=profile.frequency,
        parameter='theta=(omega R)^2, s2=R^2 ds/dtheta at theta=0; not a fit to finite-frequency solutions.',
        new_augmented_static_tangent_BVP_solves=len(rows), new_finite_frequency_or_exterior_wave_solves=0,
        output_hashes={path.name:digest(path) for path in directory.glob('*.npz')})
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    print(dict(state='complete', elapsed_seconds=report['elapsed_seconds'], rows=len(rows)), flush=True)


if __name__ == '__main__':
    main()
