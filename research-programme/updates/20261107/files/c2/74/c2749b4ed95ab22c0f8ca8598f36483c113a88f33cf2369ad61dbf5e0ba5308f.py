from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import solve_ivp

from axial_system import ROOT, BRANCH, AxialProblem, basis, weak_integral


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--tolerance', type=float, default=2e-12)
    parser.add_argument('--max-step', type=float, default=1/240)
    parser.add_argument('--start', type=float, default=5e-6)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    inputs = {}
    for nominal in [0., .00001, .0001, .001, .003, .01, .03]:
        problem = AxialProblem(nominal)
        solution = problem.solve(args.tolerance, args.max_step, args.start)
        matched = problem.match(1., solution.y[:, -1])
        exterior = solve_ivp(problem.equation, [1., 2.], solution.y[:, -1], method='DOP853',
                             rtol=args.tolerance, atol=args.tolerance/20, max_step=args.max_step, dense_output=True)
        assert exterior.success
        controls = []
        for coordinate in [1.25, 1.5, 2.]:
            current = problem.match(coordinate, exterior.sol(coordinate))
            controls.append({'extraction_over_radius': coordinate, 'response_over_alpha': current['response_over_alpha'],
                             'relative_response_difference': float(abs(current['response_over_alpha']/matched['response_over_alpha']-1))})
        archive = 'C'+str(nominal).replace('.', 'p')+'.npz'
        grid = np.linspace(args.start, 1, 1201)
        np.savez_compressed(output/archive, coordinate=grid, state=solution.sol(grid),
                            radius=problem.radius, alpha=problem.alpha, mass=problem.mass)
        sigma_bar = -matched['response']/6
        row = {'nominal_flat_compactness': nominal, 'radius': problem.radius, 'alpha': problem.alpha,
               'mass': problem.mass, 'actual_2M_over_R': problem.compactness, **matched,
               'geometric_sigma_bar': sigma_bar, 'geometric_sigma_BV': sigma_bar/2,
               'k2B_mass_normalized': sigma_bar/problem.mass**5 if problem.mass else None,
               'k2B_radius_normalized': sigma_bar/problem.radius**5,
               'function_evaluations': solution.nfev, 'archive': archive, 'exterior_controls': controls,
               'parent_archive': str(problem.profile.path), 'parent_archive_sha256': digest(problem.profile.path)}
        inputs[str(problem.profile.path)] = digest(problem.profile.path)
        rows.append(row)
        print(json.dumps({key: row[key] for key in ['nominal_flat_compactness', 'response', 'response_over_alpha', 'geometric_sigma_bar']}), flush=True)
    columns = ['nominal_flat_compactness', 'radius', 'alpha', 'mass', 'actual_2M_over_R', 'response',
               'response_over_alpha', 'geometric_sigma_bar', 'geometric_sigma_BV', 'k2B_radius_normalized']
    with (output/'coefficients.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows({key: row[key] for key in columns} for row in rows)
    background_report = BRANCH/'self-gravity-20261003/results/fine/status.json'
    inputs[str(background_report)] = digest(background_report)
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'system_sha256': digest(ROOT/'axial_system.py'),
              'settings': vars(args), 'parent_input_hashes': inputs, 'rows': rows,
              'weak_integral_coarse': weak_integral(120, 10), 'weak_integral_fine': weak_integral(240, 12),
              'derivation_sha256': digest(ROOT/'results/derivation/status.json'),
              'meaning_of_alpha_scan': 'Numerical weak-coupling control at fixed charge, not an astrophysical mass sequence.',
              'response_definition': 'b/a for q=a*r^3*(1-2M/r)+b*r^-2*2F1(1,4;6;2M/r), units length^5.',
              'convention': 'Sij=sigma_bar Bij, G*sigma_bar=-response/6; sigma_BV=sigma_bar/2 with c=1.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'weak_integral': report['weak_integral_fine'], 'rows': len(rows)}))


if __name__ == '__main__':
    main()
