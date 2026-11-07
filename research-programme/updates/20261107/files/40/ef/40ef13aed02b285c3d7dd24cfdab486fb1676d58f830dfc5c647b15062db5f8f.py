from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from response_system_v3 import ResponseProblem, ROOT, PARENT, encode


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/residue'
    output.mkdir(exist_ok=False)
    parent = json.loads((PARENT/'results/mode-main-real/status.json').read_text())
    pole = complex(parent['sigma']['real'], parent['sigma']['imaginary'])
    problem = ResponseProblem()
    center, solution = problem.evaluate(pole)
    np.savez_compressed(output/'pole-interior.npz', spline_knots=solution.sol.x, spline_coefficients=solution.sol.c, parameters=solution.p)
    derivative_rows, contour_rows, evaluations = [], [], [encode(center)]
    try:
        for step in [2e-6, 1e-6, 5e-7]:
            negative, _ = problem.evaluate(pole-step)
            positive, _ = problem.evaluate(pole+step)
            evaluations.extend([encode(negative), encode(positive)])
            residues = []
            for central_row, plus_row, minus_row in zip(center['rows'], positive['rows'], negative['rows']):
                derivative = (plus_row['denominator']-minus_row['denominator'])/(2*step)
                residues.append(central_row['numerator']/derivative)
            green_derivative = (1/positive['rows'][0]['total_green_surface_surface']-1/negative['rows'][0]['total_green_surface_surface'])/(2*step)
            derivative_rows.append(encode({'step': step, 'residues': residues, 'surface_green_residue': 1/green_derivative}))
            print(json.dumps(derivative_rows[-1]), flush=True)
        for circle_radius, count in [(2e-5, 8), (1e-5, 12)]:
            accumulated = np.zeros(3, dtype=complex)
            accumulated_green = 0j
            accumulated_shells = np.zeros(3, dtype=complex)
            for index in range(count):
                offset = circle_radius*np.exp(2j*np.pi*(index+.5)/count)
                value, _ = problem.evaluate(pole+offset)
                evaluations.append(encode(value))
                accumulated += np.array([row['susceptibility'] for row in value['rows']])*offset/count
                accumulated_green += value['rows'][0]['total_green_surface_surface']*offset/count
                accumulated_shells += np.array([row['master_surface_per_unit_source_jump'] for row in value['shell_rows']])*offset/count
            row = encode({'circle_radius': circle_radius, 'points': count, 'residues': accumulated.tolist(),
                          'surface_green_residue': accumulated_green, 'source_shell_green_residues': accumulated_shells.tolist()})
            contour_rows.append(row)
            print(json.dumps(row), flush=True)
        report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'system_sha256': hashlib.sha256((ROOT/'response_system_v3.py').read_bytes()).hexdigest(),
                  'parent_pole_path': str(PARENT/'results/mode-main-real/status.json'), 'parent_pole_sha256': hashlib.sha256((PARENT/'results/mode-main-real/status.json').read_bytes()).hexdigest(),
                  'pole': encode(pole), 'derivative_controls': derivative_rows, 'contour_controls': contour_rows,
                  'evaluations': evaluations, 'scope': 'Residues derived from denominator derivative and independent Cauchy integrals; no one-mode static saturation fit.'}
    except Exception as error:
        report = {'state': 'failed', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'error': repr(error), 'derivative_controls': derivative_rows, 'contour_controls': contour_rows, 'evaluations': evaluations}
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
