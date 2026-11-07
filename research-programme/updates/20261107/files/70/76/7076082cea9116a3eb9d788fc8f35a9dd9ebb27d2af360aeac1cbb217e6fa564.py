from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import psutil
from scipy import linalg

from solve_pulsations import Profile, build, digest, potential_prime


ROOT = Path(__file__).resolve().parent


def mode_and_time_checks(profile, output):
    system = build(profile, 128, 12)
    values, vectors = linalg.eigh(system['pulsation'], subset_by_index=[0, 0], check_finite=False)
    omega = float(np.sqrt(values[0]))
    mode = system['dynamic_factor']@vectors[:, 0]
    amplitude_count = 127
    amplitude_coefficients = linalg.solve_triangular(system['factor_amplitude'].T, mode[:amplitude_count], lower=False)
    density_coefficients = linalg.solve_triangular(system['factor_phase'].T, system['quotient']@mode[amplitude_count:], lower=False)
    coefficients = np.concatenate([amplitude_coefficients, density_coefficients])
    quadrature = system['quadrature']
    position, weights = quadrature.position, quadrature.weights
    field, gradient, mass, metric, xi, rotation = profile.values(position)
    coefficient = xi*metric
    amplitude = (system['basis']@amplitude_coefficients)/position
    gradient_basis = quadrature.derivative/position[:, None]-system['basis']/position[:, None]**2
    amplitude_gradient = gradient_basis@amplitude_coefficients
    density = system['phase_basis']@density_coefficients
    sigma = position**2*field**2*density
    delta_kinetic = system['kinetic_variation']@coefficients
    delta_mass = system['mass_variation']@coefficients
    integrand = profile.alpha*position*delta_kinetic
    delta_log_xi = quadrature.cumulative(integrand)-quadrature.integrate(integrand)
    delta_log_A = delta_log_xi-2*profile.alpha*delta_mass/(position*metric)
    delta_A = coefficient*delta_log_A
    delta_xi = xi*delta_log_xi
    phase_rate = coefficient*density-2*profile.frequency*amplitude/field+profile.frequency*delta_log_A
    phase_gradient_vector = system['phase_basis'].T@(weights*position**2*field**2*phase_rate)
    phase_rate_white = linalg.solve_triangular(system['factor_phase'], phase_gradient_vector, lower=True)
    force = potential_prime(field)
    second = system['potential_second']
    amplitude_gradient_vector = gradient_basis.T@(weights*position**2*(coefficient*amplitude_gradient+delta_A*gradient))
    local_force = xi*position**2*second*amplitude+delta_xi*position**2*force
    local_force += 3*position**2*profile.frequency**2*amplitude/coefficient-2*profile.frequency*sigma/field
    local_force -= delta_A*position**2*profile.frequency**2*field/coefficient**2
    amplitude_gradient_vector += (system['basis']/position[:, None]).T@(weights*local_force)
    amplitude_gradient_white = linalg.solve_triangular(system['factor_amplitude'], amplitude_gradient_vector, lower=True)
    independent_gradient = np.concatenate([amplitude_gradient_white, system['quotient'].T@phase_rate_white])
    matrix_gradient = system['even']@mode
    gradient_error = linalg.norm(independent_gradient-matrix_gradient)/linalg.norm(matrix_gradient)
    phase_coefficients = linalg.solve_triangular(system['factor_phase'].T, phase_rate_white/omega, lower=False)
    momentum_coefficients = linalg.solve_triangular(system['factor_amplitude'].T, -amplitude_gradient_white/omega, lower=False)
    restored_global_phase_amplitude = float((system['charge_vector']@phase_rate_white)/(omega*(system['charge_vector']@system['charge_vector'])))
    source = xi*position**2*(metric*delta_kinetic/2+force*amplitude)
    outer_mass_relative_residual = abs(quadrature.integrate(source))/max(quadrature.integrate(abs(source)), 1e-30)
    assert gradient_error < 1e-8
    assert outer_mass_relative_residual < 1e-8
    name = f'R{profile.row["base_radius"]:g}-C{profile.row["nominal_flat_compactness"]:g}'.replace('.', 'p')
    np.savez_compressed(output/f'{name}-reconstructed-mode.npz', position=position,
                        frequency=omega, amplitude_cos=amplitude,
                        phase_angle_sin=system['phase_basis']@phase_coefficients,
                        amplitude_momentum_sin=position*(system['basis']@momentum_coefficients),
                        charge_density_cos=sigma, mass_cos=delta_mass,
                        lapse_fraction_cos=delta_log_xi-profile.alpha*delta_mass/(position*metric),
                        constant_phase_component_sin=restored_global_phase_amplitude)
    size = len(mode)
    generator = np.block([[np.zeros((size, size)), system['dynamic']], [-system['even'], np.zeros((size, size))]])
    initial = np.concatenate([mode, np.zeros(size)])
    initial_energy = .5*mode@system['even']@mode
    time_rows = []
    for steps_per_period in [80, 160, 320]:
        step = 2*np.pi/(omega*steps_per_period)
        factor = linalg.lu_factor(np.eye(2*size)-.5*step*generator, check_finite=False)
        right = np.eye(2*size)+.5*step*generator
        state = initial.copy()
        maximum_energy_error = 0.
        traces = []
        for iteration in range(3*steps_per_period):
            state = linalg.lu_solve(factor, right@state, check_finite=False)
            energy = .5*(state[:size]@system['even']@state[:size]+state[size:]@system['dynamic']@state[size:])
            relative_error = abs(energy/initial_energy-1)
            maximum_energy_error = max(maximum_energy_error, relative_error)
            coordinate = float(vectors[:, 0]@linalg.solve_triangular(system['dynamic_factor'], state[:size], lower=True, check_finite=False))
            velocity = float(vectors[:, 0]@(system['dynamic_factor'].T@state[size:]))
            traces.append([step*(iteration+1), coordinate, velocity, energy])
        angle = float(np.arctan2(-velocity/omega, coordinate))
        expected_angle = float(np.angle(np.exp(1j*(3*steps_per_period*2*np.arctan(step*omega/2)))))
        assert maximum_energy_error < 1e-8
        assert abs(angle-expected_angle) < 1e-7
        np.savez_compressed(output/f'{name}-midpoint-{steps_per_period}.npz', trace=np.array(traces),
                            frequency=omega, step=step, initial_energy=initial_energy)
        time_rows.append({'steps_per_period': steps_per_period, 'periods_evolved': 3,
                          'maximum_relative_quadratic_energy_drift': maximum_energy_error,
                          'phase_error_against_continuum': abs(angle),
                          'phase_difference_from_midpoint_dispersion': abs(angle-expected_angle)})
    assert time_rows[-1]['phase_error_against_continuum'] < .08*time_rows[0]['phase_error_against_continuum']
    return {'base_radius': profile.row['base_radius'], 'nominal_compactness': profile.row['nominal_flat_compactness'],
            'cells': 128, 'quadrature_order': 12, 'fundamental_frequency': omega,
            'independently_reconstructed_KG_gradient_relative_difference': float(gradient_error),
            'outer_delta_mass_relative_residual': float(outer_mass_relative_residual),
            'restored_constant_phase_component_amplitude': restored_global_phase_amplitude,
            'time_evolution': time_rows,
            'time_evolution_scope': 'linear charge-reduced Galerkin Hamiltonian, not nonlinear spacetime evolution'}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(parents=True, exist_ok=False)
    reports, input_hashes = {}, {}
    for label in ['pilot', 'convergence', 'large-body-refinement', 'large-body-fine', 'flat-controls', 'flat-controls-fine', 'quadrature']:
        path = ROOT/f'results/{label}/status.json'
        report = json.loads(path.read_text(encoding='utf-8'))
        assert report['state'] == 'complete' and report['script_sha256'] == digest(ROOT/'solve_pulsations.py')
        reports[label] = report
        input_hashes[str(path)] = digest(path)
    rows = [row for report in reports.values() for row in report['rows']]
    physical = reports['convergence']['rows']+reports['large-body-refinement']['rows']+reports['large-body-fine']['rows']
    comparisons, finest, flat_controls = [], [], []
    for radius in [8., 20., 80.]:
        for nominal in [0., .001, .03]:
            series = sorted([row for row in physical if row['base_radius'] == radius and row['nominal_compactness'] == nominal], key=lambda row: row['cells'])
            values = np.array([row['frequencies_at_infinity_in_mu_star_units'] for row in series])
            last_relative = abs(values[-1]-values[-2])/values[-1]
            ratio = abs(values[-1]-values[-2])/abs(values[-2]-values[-3])
            assert np.all(last_relative < .002) and np.all(ratio < .4)
            assert np.all(np.diff(values, axis=0) < 0)
            middle = next(row for row in series if row['cells'] == 256)
            alternate = next(row for row in reports['quadrature']['rows'] if row['base_radius'] == radius and row['nominal_compactness'] == nominal)
            quadrature_error = np.max(abs(np.array(middle['frequency_squared'])-alternate['frequency_squared'])/middle['frequency_squared'])
            assert quadrature_error < 1e-6
            comparisons.append({'base_radius': radius, 'nominal_compactness': nominal,
                                'mesh_cells': [row['cells'] for row in series], 'frequencies': values.tolist(),
                                'last_relative_frequency_mesh_changes': last_relative.tolist(),
                                'last_frequency_change_ratios': ratio.tolist(),
                                'quadrature_relative_omega_squared_difference': float(quadrature_error)})
            finest.append(series[-1])
        controls = sorted([row for row in reports['flat-controls']['rows']+reports['flat-controls-fine']['rows'] if row['base_radius'] == radius], key=lambda row: row['cells'])
        differences = [float(np.max(abs(np.array(row['frequencies_at_infinity_in_mu_star_units'])-row['independent_flat_gyro']['lowest_frequencies'])/row['frequencies_at_infinity_in_mu_star_units'])) for row in controls]
        assert differences[-1] < 1e-4 and differences[-1] < .15*differences[0]
        assert all(row['independent_flat_gyro']['near_zero_count'] == 2 for row in controls)
        flat_controls.append({'base_radius': radius, 'cells': [row['cells'] for row in controls],
                              'maximum_relative_flat_formulation_difference': differences,
                              'finite_space_momentum_projection_difference_not_assumed_exact': True})
    for row in rows:
        assert row['phase_null_relative_residual'] < 1e-12
        assert row['maximum_charge_tangent_relative_residual'] < 1e-12
        assert row['maximum_second_order_relative_residual'] < 1e-4
        if row['direct_first_order_check']:
            assert row['direct_first_order_check']['relative_frequency_difference'] < 1e-6
            assert row['direct_first_order_check']['maximum_absolute_real_part'] < 1e-8
    report = {'state': 'running', 'script_sha256': digest(Path(__file__)), 'input_hashes': input_hashes,
              'solver_sha256': digest(ROOT/'solve_pulsations.py'), 'comparisons': comparisons,
              'finest_spectra': finest, 'flat_formulation_controls': flat_controls, 'dynamic_checks': [],
              'spectral_calculations': len(rows), 'physical_cases': len(finest),
              'oscillation_frequencies_computed': True, 'global_phase_removed_without_changing_stiffness': True,
              'continuum_error_bounds_certified': False, 'nonlinear_stability_or_strong_gravity_endpoint_claimed': False}
    try:
        for radius in [8., 20., 80.]:
            row = mode_and_time_checks(Profile(radius, .03), output)
            report['dynamic_checks'].append(row)
            (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
            print(json.dumps(row), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'spectral_calculations': len(rows), 'dynamical_cases': len(report['dynamic_checks'])}))


if __name__ == '__main__':
    main()
