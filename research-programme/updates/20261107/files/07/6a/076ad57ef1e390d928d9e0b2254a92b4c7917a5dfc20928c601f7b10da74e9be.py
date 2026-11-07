from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import time

import numpy as np
import psutil
from scipy.interpolate import PPoly
from scipy.linalg import eigh_tridiagonal
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh, LinearOperator, splu

from explore_compact_profiles import endpoint_series
from solve_finite_family import solve, observables, tail_state


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/validated-bodies'


def spectral_test(radius, cut, solution, coefficients, spacing):
    intervals = int(np.ceil(radius/spacing))
    step = radius/intervals
    position = step*np.arange(1, intervals)
    interior = position <= cut
    amplitude = np.empty_like(position)
    amplitude[interior] = solution.sol(position[interior]/cut)[0]
    amplitude[~interior] = tail_state(radius-position[~interior], radius, solution.p[0], coefficients)[0]
    frequency2 = float(solution.p[0])
    potential_plus = amplitude**(-2/3)/6+1.5*amplitude**2-frequency2
    potential_minus = .5*amplitude**(-2/3)+.5*amplitude**2-frequency2
    off_diagonal = np.full(intervals-2, -1/step**2)
    base_diagonal = 2/step**2+potential_plus
    amplitude_radial = eigh_tridiagonal(base_diagonal, off_diagonal, select='i', select_range=(0, 3), eigvals_only=True)
    phase = eigh_tridiagonal(2/step**2+potential_minus, off_diagonal, select='i', select_range=(0, 2), eigvals_only=True)
    translations = eigh_tridiagonal(base_diagonal+2/position**2, off_diagonal, select='i', select_range=(0, 2), eigvals_only=True)
    quadrupole = eigh_tridiagonal(base_diagonal+6/position**2, off_diagonal, select='i', select_range=(0, 1), eigvals_only=True)
    direction = position*amplitude*np.sqrt(step)
    norm = float(np.dot(direction, direction))
    rank_coefficient = 4*frequency2/norm
    base = diags([off_diagonal, base_diagonal, off_diagonal], [-1, 0, 1], format='csc')
    shift = -frequency2-1
    shifted = base-diags(np.full(intervals-1, shift), format='csc')
    factor = splu(shifted)
    inverse_direction = factor.solve(direction)
    denominator = 1+rank_coefficient*np.dot(direction, inverse_direction)
    def multiply(vector):
        return base@vector+rank_coefficient*direction*np.dot(direction, vector)
    def inverse(vector):
        result = factor.solve(vector)
        return result-inverse_direction*(rank_coefficient*np.dot(direction, result)/denominator)
    operator = LinearOperator(base.shape, matvec=multiply, dtype=float)
    inverse_operator = LinearOperator(base.shape, matvec=inverse, dtype=float)
    eigenvalues, eigenvectors = eigsh(operator, k=3, sigma=shift, which='LM', OPinv=inverse_operator,
                                     tol=1e-10, maxiter=10000, v0=np.sin(np.pi*position/radius))
    residuals = [float(np.linalg.norm(multiply(vector)-value*vector))
                 for value, vector in zip(eigenvalues, eigenvectors.T)]
    return {'requested_spacing': spacing, 'actual_spacing': step, 'interior_points': len(position),
            'amplitude_radial_unconstrained': amplitude_radial.tolist(), 'fixed_charge_radial': eigenvalues.tolist(),
            'phase_l0': phase.tolist(), 'amplitude_l1_translation': translations.tolist(),
            'amplitude_l2': quadrupole.tolist(), 'fixed_charge_eigenpair_residuals': residuals,
            'discretization': 'second-order radial reduced Dirichlet stencil on full compact support; singular endpoint inside potential'}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    coefficients, series = endpoint_series()
    prior = json.loads((ROOT/'results/family/progress.json').read_text(encoding='utf-8'))
    attempts = [
        {'runner': 'solve_finite_family.py', 'outcome': 'incomplete',
         'reason': 'fine R40 continuation from fine R20 exceeded 60000 nodes; seven coarse and four fine profiles retained'},
        {'runner': 'refine_finite_family.py', 'outcome': 'implementation_error_before_profile',
         'reason': 'PPoly reconstruction omitted axis=1; corrected in this daughter, prior evidence unchanged'}]
    (OUTPUT/'prior-attempts.json').write_text(json.dumps(attempts, indent=2), encoding='utf-8')
    coexistence = json.loads((ROOT.parent/'conserved-stress-20261003/results/charge-coexistence/status.json').read_text(encoding='utf-8'))
    last = coexistence['quadrature_estimates'][-1]
    amplitude = float(last['critical_amplitude'])
    chemical = float(last['critical_chemical_potential'])
    sigma = float(last['planar_grand_potential_surface_tension'])/(amplitude**2*chemical)
    rows = []
    spectra = []
    comparisons = []
    for radius in [6., 8., 12., 20., 40., 80., 160.]:
        archive = np.load(ROOT/f'results/family/coarse-R{radius:g}.npz')
        seed = SimpleNamespace(sol=PPoly(archive['spline_coefficients'], archive['spline_knots'], axis=1),
                               p=np.array([float(archive['frequency2'])]))
        seed_cut = float(archive['cut_radius'])
        solution, cut, distance = solve(radius, 1e-9, 2e-9, coefficients, (radius, seed_cut, seed))
        attempt = {'radius': radius, 'success': bool(solution.success), 'message': solution.message,
                   'nodes': len(solution.x), 'rms': float(np.max(solution.rms_residuals))}
        (OUTPUT/f'solver-R{radius:g}.json').write_text(json.dumps(attempt, indent=2), encoding='utf-8')
        assert solution.success, attempt
        row = observables(radius, cut, solution, coefficients, sigma)
        row.update(label='validated', floor=1e-9, tolerance=2e-9, endpoint_distance=distance)
        np.savez_compressed(OUTPUT/f'profile-R{radius:g}.npz', spline_coefficients=solution.sol.c,
                            spline_knots=solution.sol.x, radius=radius, cut_radius=cut,
                            frequency2=solution.p[0], floor=1e-9)
        rows.append(row)
        coarse = next(item for item in prior if item['label'] == 'coarse' and item['support_radius'] == radius)
        differences = {key: abs(coarse[key]-row[key])/abs(row[key])
                       for key in ['frequency', 'charge', 'energy', 'central_amplitude', 'gradient_energy']}
        comparisons.append({'radius': radius, 'relative_differences': differences})
        levels = [spectral_test(radius, cut, solution, coefficients, spacing) for spacing in [.04, .02, .01]]
        spectra.append({'radius': radius, 'levels': levels})
        (OUTPUT/f'spectra-R{radius:g}.json').write_text(json.dumps(spectra[-1], indent=2), encoding='utf-8')
        print(json.dumps({'radius': radius, 'frequency': row['frequency'], 'virial': row['virial_relative'],
                          'surface_ratio': row['surface_excess_ratio'], 'nodes': row['nodes'],
                          'max_convergence_change': max(differences.values()),
                          'fixed_charge_lowest': levels[-1]['fixed_charge_radial'][0],
                          'translation_zero_error': levels[-1]['amplitude_l1_translation'][0]}), flush=True)
        (OUTPUT/'progress.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    assert all(row['virial_relative'] < 1e-7 for row in rows)
    assert all(row['independent_quadrature_relative_error'] < 1e-8 for row in rows)
    assert all(max(row['relative_differences'].values()) < 2e-6 for row in comparisons)
    assert all(row['energy'] > row['frequency']*row['charge'] > row['charge'] for row in rows)
    assert all(row['max_increase'] < 1e-9 and row['min_amplitude'] > 0 for row in rows)
    assert all(rows[index+1]['charge'] > rows[index]['charge'] and rows[index+1]['frequency'] < rows[index]['frequency']
               for index in range(len(rows)-1))
    for row in spectra:
        final = row['levels'][-1]
        assert final['amplitude_radial_unconstrained'][0] < 0 < final['amplitude_radial_unconstrained'][1]
        assert final['fixed_charge_radial'][0] > 0 and final['amplitude_l2'][0] > 0
        assert max(final['fixed_charge_eigenpair_residuals']) < 1e-7
        for key in ['phase_l0', 'amplitude_l1_translation']:
            errors = [abs(level[key][0]) for level in row['levels']]
            assert errors[-1] < errors[0]/8, (row['radius'], key, errors)
    report = {'state': 'complete', 'rows': rows, 'spectra': spectra, 'convergence': comparisons,
              'dimensionless_surface_tension': sigma, 'series_coefficients': series,
              'physical_conversion': {'v_star': amplitude, 'mu_star': chemical,
                                      'energy_factor': amplitude**2/chemical,
                                      'charge_factor': amplitude**2/chemical**2, 'radius_factor': 1/chemical},
              'parent_seal_sha256': hashlib.sha256((ROOT.parent/'conserved-stress-20261003/results/stage-integrity.json').read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'imported_source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                        for name in ['explore_compact_profiles.py', 'solve_finite_family.py']},
              'prior_incomplete_attempts_recorded': True, 'elapsed_seconds': time.monotonic()-started}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'profiles': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))


if __name__ == '__main__':
    main()
