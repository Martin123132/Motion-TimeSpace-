from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import solve_ivp

from test_radial_energy import Profile, Quadrature, potential, potential_prime


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape_values(coordinate, kind, radius):
    if kind == 'bulk':
        return np.ones_like(coordinate), np.zeros_like(coordinate)
    if kind == 'redistribution':
        return 1-3*coordinate**2, -6*coordinate/radius
    if kind == 'shell':
        return coordinate**2*(1-coordinate**2), (2*coordinate-4*coordinate**3)/radius
    raise ValueError(kind)


def finite_test(profile, kind):
    quadrature = Quadrature(profile.radius, 768, 12)
    position = quadrature.position
    amplitude, gradient, mass, metric, xi, rotation = profile.values(position)
    shape, shape_prime = shape_values(position/profile.radius, kind, profile.radius)
    perturbation = amplitude*shape
    gradient_perturbation = gradient*shape+amplitude*shape_prime
    momentum_perturbation = rotation*(.25+(position/profile.radius)**2)
    inertia = quadrature.integrate(position**2*amplitude**2)
    correction = quadrature.integrate(position**2*(rotation*perturbation+amplitude*momentum_perturbation))/inertia
    momentum_perturbation -= correction*amplitude
    kinetic_variation = 2*(gradient*gradient_perturbation+rotation*momentum_perturbation)
    mass_variation = quadrature.cumulative(xi*position**2*(metric*kinetic_variation/2+potential_prime(amplitude)*perturbation))/xi
    second_potential = amplitude**(-2/3)/6+1.5*amplitude**2
    local_hessian = quadrature.integrate(xi*position**2*(metric*(gradient_perturbation**2+momentum_perturbation**2)+second_potential*perturbation**2))
    gravity_hessian = -2*profile.alpha*quadrature.integrate(xi*position*kinetic_variation*mass_variation)
    charge_hessian = -2*profile.frequency*quadrature.integrate(position**2*perturbation*momentum_perturbation)
    predicted = float(local_hessian+gravity_hessian+charge_hessian)
    base_charge = quadrature.integrate(position**2*amplitude*rotation)

    def energy(epsilon, fixed_charge):
        shifted_amplitude = amplitude+epsilon*perturbation
        shifted_gradient = gradient+epsilon*gradient_perturbation
        shifted_rotation = rotation+epsilon*momentum_perturbation
        exact_correction = 0.
        if fixed_charge:
            raw_charge = quadrature.integrate(position**2*shifted_amplitude*shifted_rotation)
            exact_correction = (base_charge-raw_charge)/quadrature.integrate(position**2*shifted_amplitude*amplitude)
            shifted_rotation += exact_correction*amplitude
        kinetic = shifted_gradient**2+shifted_rotation**2
        log_factor = quadrature.cumulative(profile.alpha*position*kinetic)
        total_factor = quadrature.integrate(profile.alpha*position*kinetic)
        energy_value = quadrature.integrate(np.exp(log_factor-total_factor)*position**2*(kinetic/2+potential(shifted_amplitude)))
        charge = quadrature.integrate(position**2*shifted_amplitude*shifted_rotation)
        return float(energy_value), float(charge), float(exact_correction)

    base_energy = energy(0., False)[0]
    rows = []
    for epsilon in [.01, .005, .0025, .00125]:
        free_plus, free_minus = energy(epsilon, False), energy(-epsilon, False)
        fixed_plus, fixed_minus = energy(epsilon, True), energy(-epsilon, True)
        routhian_second = ((free_plus[0]-base_energy)+(free_minus[0]-base_energy)
                           -profile.frequency*((free_plus[1]-base_charge)+(free_minus[1]-base_charge)))/epsilon**2
        fixed_second = ((fixed_plus[0]-base_energy)+(fixed_minus[0]-base_energy))/epsilon**2
        rows.append({'epsilon': epsilon, 'nonlinear_Routhian_second_difference': float(routhian_second),
                     'nonlinear_fixed_charge_ADM_second_difference': float(fixed_second),
                     'Routhian_relative_error': float(abs(routhian_second-predicted)/abs(predicted)),
                     'fixed_charge_relative_error': float(abs(fixed_second-predicted)/abs(predicted)),
                     'fixed_charge_max_relative_error': float(max(abs(fixed_plus[1]/base_charge-1), abs(fixed_minus[1]/base_charge-1)))})

    ode_check = None
    if kind == 'redistribution':
        epsilon = .005
        target_energy, target_charge, exact_correction = energy(epsilon, True)

        def ode(position_scalar, state):
            if position_scalar == 0 or position_scalar >= profile.radius:
                return [0.]
            points = np.array([position_scalar])
            field, field_gradient, _, _, _, field_rotation = profile.values(points)
            shape_value, derivative_value = shape_values(points/profile.radius, kind, profile.radius)
            field_shift = field*shape_value
            gradient_shift = field_gradient*shape_value+field*derivative_value
            momentum_shift = field_rotation*(.25+(points/profile.radius)**2)-correction*field
            shifted_field = field+epsilon*field_shift
            shifted_gradient = field_gradient+epsilon*gradient_shift
            shifted_rotation = field_rotation+epsilon*momentum_shift+exact_correction*field
            kinetic = shifted_gradient**2+shifted_rotation**2
            metric_value = 1-2*profile.alpha*state[0]/position_scalar
            return [float(position_scalar**2*(metric_value*kinetic[0]/2+potential(shifted_field)[0]))]

        solution = solve_ivp(ode, (0., profile.radius), [0.], method='DOP853', rtol=2e-11, atol=2e-12, max_step=.08)
        assert solution.success
        ode_check = {'epsilon': epsilon, 'adaptive_ODE_mass': float(solution.y[0, -1]),
                     'integrating_factor_mass': target_energy,
                     'relative_difference': float(abs(solution.y[0, -1]-target_energy)/abs(target_energy)),
                     'ODE_evaluations': solution.nfev}
    return {'base_radius': profile.row['base_radius'], 'nominal_compactness': profile.row['nominal_flat_compactness'],
            'direction': kind, 'hessian_prediction': predicted, 'local_H_second': float(local_hessian),
            'nonlocal_gravity_second': float(gravity_hessian), 'minus_w_Q_second': float(charge_hessian),
            'first_charge_variation_relative_residual': float(abs(quadrature.integrate(position**2*(rotation*perturbation+amplitude*momentum_perturbation)))/base_charge),
            'first_mass_equals_w_deltaQ_residual_over_mass': float(abs(mass_variation[-1])/profile.mass),
            'baseline_mass_relative_error': float(abs(base_energy-profile.mass)/profile.mass),
            'steps': rows, 'independent_adaptive_mass_ODE': ode_check}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
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
    convergence = reports['convergence']['rows']
    refinements = reports['large-body-refinement']['rows']
    quadrature_rows = reports['quadrature']['rows']
    comparisons = []
    selected = []
    for radius in [8., 20., 80.]:
        for nominal in [0., .001, .03]:
            series = sorted([row for row in convergence+refinements if row['base_radius'] == radius and row['nominal_compactness'] == nominal], key=lambda row: row['cells'])
            fine, previous, older = series[-1], series[-2], series[-3]
            values = [row['lowest_fixed_charge_energy_eigenvalues'][0] for row in series]
            assert all(value > 0 for value in values)
            assert all(left > right for left, right in zip(values[:-1], values[1:]))
            assert all(row['momentum_block_minimum'] > .8 for row in series)
            phase = [row['phase_lowest_eigenvalues'][0] for row in series]
            assert all(left > 3*right > 0 for left, right in zip(phase[:-1], phase[1:]))
            delta = abs(values[-1]-values[-2])
            prior_delta = abs(values[-2]-values[-3])
            assert delta < .01*values[-1] and delta < .3*prior_delta
            same_mesh = next(row for row in series if row['cells'] == 512)
            alternate = next(row for row in quadrature_rows if row['base_radius'] == radius and row['nominal_compactness'] == nominal)
            quadrature_error = abs(alternate['lowest_fixed_charge_energy_eigenvalues'][0]-same_mesh['lowest_fixed_charge_energy_eigenvalues'][0])/same_mesh['lowest_fixed_charge_energy_eigenvalues'][0]
            assert quadrature_error < 1e-6
            assert fine['lowest_unconstrained_energy_eigenvalues'][0] < 0
            comparisons.append({'base_radius': radius, 'nominal_compactness': nominal,
                                'mesh_cells': [row['cells'] for row in series], 'lowest_eigenvalues': values,
                                'last_relative_mesh_change': delta/values[-1], 'last_change_ratio': delta/prior_delta,
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
    for radius in [8., 20., 80.]:
        for nominal in [0., .03]:
            for kind in ['bulk', 'redistribution', 'shell']:
                row = finite_test(Profile(radius, nominal), kind)
                finite_rows.append(row)
                (output/'finite-progress.json').write_text(json.dumps({'state': 'running', 'rows': finite_rows}, indent=2, allow_nan=False), encoding='utf-8')
                print(json.dumps(row), flush=True)
                assert row['baseline_mass_relative_error'] < 1e-9
                assert row['first_charge_variation_relative_residual'] < 1e-12
                assert row['first_mass_equals_w_deltaQ_residual_over_mass'] < 1e-8
                assert row['hessian_prediction'] > 0
                for key in ['Routhian_relative_error', 'fixed_charge_relative_error']:
                    assert row['steps'][-1][key] < 2e-5
                    assert row['steps'][-1][key] < row['steps'][0][key]/10
                assert all(step['fixed_charge_max_relative_error'] < 1e-12 for step in row['steps'])
                if row['independent_adaptive_mass_ODE']:
                    assert row['independent_adaptive_mass_ODE']['relative_difference'] < 1e-9
    (output/'finite-progress.json').write_text(json.dumps({'state': 'complete', 'rows': finite_rows}, indent=2, allow_nan=False), encoding='utf-8')
    report = {'state': 'complete', 'script_sha256': digest(Path(__file__)), 'input_hashes': inputs,
              'comparisons': comparisons, 'finest_spectra': selected, 'finite_variations': finite_rows,
              'spectral_runs': len(all_rows), 'fixed_charge_cases': len(selected),
              'finite_steps': sum(len(row['steps']) for row in finite_rows),
              'adaptive_ODE_checks': sum(row['independent_adaptive_mass_ODE'] is not None for row in finite_rows),
              'positive_converged_radial_energy_Hessians_numerically_supported': True,
              'continuum_spectral_lower_bound_certified': False,
              'nonlinear_or_nonspherical_stability_proved': False,
              'oscillation_frequencies_computed': False}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'spectra': len(all_rows), 'finite_directions': len(finite_rows), 'finite_steps': report['finite_steps']}))


if __name__ == '__main__':
    main()
