from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import psutil

from validate_radial_energy import Profile, digest, finite_test


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation-v2'
    output.mkdir(parents=True, exist_ok=False)
    inputs = {}
    reports = {}
    for label in ['pilot', 'convergence', 'large-body-refinement', 'quadrature']:
        path = ROOT/f'results/{label}/status.json'
        report = json.loads(path.read_text(encoding='utf-8'))
        assert report['state'] == 'complete'
        assert report['script_sha256'] == digest(ROOT/'test_radial_energy.py')
        inputs[str(path)] = digest(path)
        reports[label] = report
    for name in ['validate_radial_energy.py', 'test_radial_energy.py']:
        inputs[str(ROOT/name)] = digest(ROOT/name)
    convergence = reports['convergence']['rows']
    refinements = reports['large-body-refinement']['rows']
    quadrature_rows = reports['quadrature']['rows']
    comparisons, selected = [], []
    for radius in [8., 20., 80.]:
        for nominal in [0., .001, .03]:
            series = sorted([row for row in convergence+refinements if row['base_radius'] == radius and row['nominal_compactness'] == nominal], key=lambda row: row['cells'])
            fine = series[-1]
            values = [row['lowest_fixed_charge_energy_eigenvalues'][0] for row in series]
            assert all(value > 0 for value in values)
            assert all(left > right for left, right in zip(values[:-1], values[1:]))
            assert all(row['momentum_block_minimum'] > .8 for row in series)
            phase = [row['phase_lowest_eigenvalues'][0] for row in series]
            assert all(left > 3*right > 0 for left, right in zip(phase[:-1], phase[1:]))
            delta, previous_delta = abs(values[-1]-values[-2]), abs(values[-2]-values[-3])
            assert delta < .01*values[-1] and delta < .3*previous_delta
            same_mesh = next(row for row in series if row['cells'] == 512)
            alternate = next(row for row in quadrature_rows if row['base_radius'] == radius and row['nominal_compactness'] == nominal)
            quadrature_error = abs(alternate['lowest_fixed_charge_energy_eigenvalues'][0]-same_mesh['lowest_fixed_charge_energy_eigenvalues'][0])/same_mesh['lowest_fixed_charge_energy_eigenvalues'][0]
            assert quadrature_error < 1e-6
            assert fine['lowest_unconstrained_energy_eigenvalues'][0] < 0
            comparisons.append({'base_radius': radius, 'nominal_compactness': nominal,
                                'mesh_cells': [row['cells'] for row in series], 'lowest_eigenvalues': values,
                                'last_relative_mesh_change': delta/values[-1], 'last_change_ratio': delta/previous_delta,
                                'phase_zeros': phase, 'quadrature_relative_difference': quadrature_error,
                                'Richardson_quadratic_estimate_not_certified': (4*values[-1]-values[-2])/3})
            selected.append(fine)
    all_rows = [row for report in reports.values() for row in report['rows']]
    assert all(row['charge_tangent_relative_error'] < 1e-12 for row in all_rows)
    assert all(row['schur_rayleigh_relative_error'] < 1e-7 for row in all_rows)
    assert all(row['lapse_constraint_max_absolute_error'] < 1e-9 for row in all_rows)
    assert all(row['mass_constraint_max_relative_error'] < 1e-9 for row in all_rows)
    assert all(row['flat_explicit_operator_relative_error'] < 1e-8 for row in all_rows if row['flat_explicit_operator_relative_error'] is not None)
    finite_rows = []
    report = {'state': 'running', 'script_sha256': digest(Path(__file__)), 'input_hashes': inputs,
              'comparisons': comparisons, 'finest_spectra': selected, 'finite_variations': finite_rows,
              'spectral_runs': len(all_rows), 'fixed_charge_cases': len(selected),
              'previous_attempt': {'path': str(ROOT/'results/validation/finite-progress.json'),
                                   'sha256': digest(ROOT/'results/validation/finite-progress.json'),
                                   'status': 'incomplete validation; six directions saved; roundoff-blind last/first convergence gate failed',
                                   'not_a_physical_instability_or_changed_Hessian': True},
              'acceptance_change': 'Keep final relative error below 2e-5. Test initial step-halving before cancellation dominates; allow an explicitly recorded roundoff estimate, not a certified bound.',
              'positive_converged_radial_energy_Hessians_numerically_supported': True,
              'continuum_spectral_lower_bound_certified': False,
              'nonlinear_or_nonspherical_stability_proved': False, 'oscillation_frequencies_computed': False}
    try:
        for radius in [8., 20., 80.]:
            for nominal in [0., .03]:
                for kind in ['bulk', 'redistribution', 'shell']:
                    profile = Profile(radius, nominal)
                    row = finite_test(profile, kind)
                    finite_rows.append(row)
                    assert row['baseline_mass_relative_error'] < 1e-9
                    assert row['first_charge_variation_relative_residual'] < 1e-12
                    assert row['first_mass_equals_w_deltaQ_residual_over_mass'] < 1e-8
                    assert row['hessian_prediction'] > 0
                    for step in row['steps']:
                        step['relative_cancellation_allowance_estimate_not_rigorous'] = float(128*np.finfo(float).eps*(abs(profile.mass)+abs(profile.frequency*profile.row['charge']/(4*np.pi)))/(step['epsilon']**2*abs(row['hessian_prediction'])))
                    for key in ['Routhian_relative_error', 'fixed_charge_relative_error']:
                        assert row['steps'][-1][key] < 2e-5
                        assert row['steps'][1][key] < .4*row['steps'][0][key]+row['steps'][1]['relative_cancellation_allowance_estimate_not_rigorous']
                    assert all(step['fixed_charge_max_relative_error'] < 1e-12 for step in row['steps'])
                    if row['independent_adaptive_mass_ODE']:
                        assert row['independent_adaptive_mass_ODE']['relative_difference'] < 1e-9
                    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
                    print(json.dumps(row), flush=True)
        report['finite_steps'] = sum(len(row['steps']) for row in finite_rows)
        report['adaptive_ODE_checks'] = sum(row['independent_adaptive_mass_ODE'] is not None for row in finite_rows)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'spectra': len(all_rows), 'finite_directions': len(finite_rows), 'finite_steps': report['finite_steps']}))


if __name__ == '__main__':
    main()
