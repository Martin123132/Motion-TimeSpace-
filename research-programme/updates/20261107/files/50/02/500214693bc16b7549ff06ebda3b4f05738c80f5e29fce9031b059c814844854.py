from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import time

import numpy as np
import psutil
from scipy.interpolate import PPoly

from explore_compact_profiles import endpoint_series
from solve_finite_family import solve, observables


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/refined-family'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    coefficients, series = endpoint_series()
    prior = json.loads((ROOT/'results/family/progress.json').read_text(encoding='utf-8'))
    failure = {'state': 'incomplete', 'runner': 'solve_finite_family.py',
               'reason': 'fine R40 continuation from fine R20 exceeded 60000 collocation nodes',
               'retained_completed_profiles': len(prior),
               'remedy': 'seed each high-accuracy profile from the independently converged coarse profile at the SAME support radius',
               'previous_results_modified': False}
    (OUTPUT/'prior-attempt.json').write_text(json.dumps(failure, indent=2), encoding='utf-8')
    coexistence = json.loads((ROOT.parent/'conserved-stress-20261003/results/charge-coexistence/status.json').read_text(encoding='utf-8'))
    last = coexistence['quadrature_estimates'][-1]
    amplitude = float(last['critical_amplitude'])
    chemical = float(last['critical_chemical_potential'])
    sigma = float(last['planar_grand_potential_surface_tension'])/(amplitude**2*chemical)
    rows = []
    comparisons = []
    for radius in [6., 8., 12., 20., 40., 80., 160.]:
        archive = np.load(ROOT/f'results/family/coarse-R{radius:g}.npz')
        seed = SimpleNamespace(sol=PPoly(archive['spline_coefficients'], archive['spline_knots']),
                               p=np.array([float(archive['frequency2'])]))
        seed_cut = float(archive['cut_radius'])
        solution, cut, distance = solve(radius, 1e-9, 2e-9, coefficients, (radius, seed_cut, seed))
        attempt = {'radius': radius, 'success': bool(solution.success), 'message': solution.message,
                   'nodes': len(solution.x), 'rms': float(np.max(solution.rms_residuals))}
        (OUTPUT/f'solver-R{radius:g}.json').write_text(json.dumps(attempt, indent=2), encoding='utf-8')
        assert solution.success, attempt
        row = observables(radius, cut, solution, coefficients, sigma)
        row.update(label='refined', floor=1e-9, tolerance=2e-9, endpoint_distance=distance)
        np.savez_compressed(OUTPUT/f'profile-R{radius:g}.npz', spline_coefficients=solution.sol.c,
                            spline_knots=solution.sol.x, radius=radius, cut_radius=cut,
                            frequency2=solution.p[0], floor=1e-9)
        rows.append(row)
        coarse = next(item for item in prior if item['label'] == 'coarse' and item['support_radius'] == radius)
        differences = {key: abs(coarse[key]-row[key])/abs(row[key])
                       for key in ['frequency', 'charge', 'energy', 'central_amplitude', 'gradient_energy']}
        comparisons.append({'radius': radius, 'relative_differences': differences})
        print(json.dumps({'radius': radius, 'frequency': row['frequency'], 'virial': row['virial_relative'],
                          'surface_ratio': row['surface_excess_ratio'], 'nodes': row['nodes'],
                          'max_convergence_change': max(differences.values())}), flush=True)
        (OUTPUT/'progress.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    assert all(row['virial_relative'] < 1e-7 for row in rows)
    assert all(row['independent_quadrature_relative_error'] < 1e-8 for row in rows)
    assert all(max(row['relative_differences'].values()) < 2e-6 for row in comparisons)
    assert all(row['energy'] > row['frequency']*row['charge'] > row['charge'] for row in rows)
    assert all(row['max_increase'] < 1e-9 and row['min_amplitude'] > 0 for row in rows)
    assert all(rows[index+1]['charge'] > rows[index]['charge'] and rows[index+1]['frequency'] < rows[index]['frequency']
               for index in range(len(rows)-1))
    report = {'state': 'complete', 'rows': rows, 'convergence': comparisons,
              'dimensionless_surface_tension': sigma, 'series_coefficients': series,
              'physical_conversion': {'v_star': amplitude, 'mu_star': chemical,
                                      'energy_factor': amplitude**2/chemical,
                                      'charge_factor': amplitude**2/chemical**2, 'radius_factor': 1/chemical},
              'parent_seal_sha256': hashlib.sha256((ROOT.parent/'conserved-stress-20261003/results/stage-integrity.json').read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'imported_source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                        for name in ['explore_compact_profiles.py', 'solve_finite_family.py']},
              'prior_incomplete_attempt_recorded': True, 'elapsed_seconds': time.monotonic()-started}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'profiles': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
