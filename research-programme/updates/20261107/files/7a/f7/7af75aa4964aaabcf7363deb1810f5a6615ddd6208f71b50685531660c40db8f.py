from __future__ import annotations

from datetime import datetime, timezone
import json

import psutil
import sympy as sy

from causal_system import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, residual):
        value = sy.factor(sy.expand(residual))
        assert value == 0, (name, value)
        checks.append({'name': name, 'passed': True, 'residual': str(value)})

    time, coordinate = sy.symbols('tau x', real=True)
    eigenvalue, coupling, norm, static_impedance, spectral_moment = sy.symbols('lambda a I Y0 J1', real=True)
    port, mode = sy.Function('q')(time), sy.Function('eta')(time)
    port_dot, mode_dot = sy.diff(port, time), sy.diff(mode, time)
    lagrangian = (norm*port_dot**2+2*coupling*port_dot*mode_dot+mode_dot**2-eigenvalue*mode**2-static_impedance*port**2)/2
    mode_equation = sy.diff(sy.diff(lagrangian, mode_dot), time)-sy.diff(lagrangian, mode)
    check('lifted_mode_equation', mode_equation-sy.diff(mode, time, 2)-eigenvalue*mode-coupling*sy.diff(port, time, 2))
    traction = static_impedance*port+norm*sy.diff(port, time, 2)+coupling*sy.diff(mode, time, 2)
    check('surface_variation_minus_traction', sy.diff(lagrangian, port)-sy.diff(sy.diff(lagrangian, port_dot), time)+traction)
    energy = (norm*port_dot**2+2*coupling*port_dot*mode_dot+mode_dot**2+eigenvalue*mode**2+static_impedance*port**2)/2
    check('modal_Noether_energy', port_dot*sy.diff(lagrangian, port_dot)+mode_dot*sy.diff(lagrangian, mode_dot)-lagrangian-energy)
    check('positive_completed_square', energy-((norm-coupling**2)*port_dot**2+(mode_dot+coupling*port_dot)**2
                                             +eigenvalue*mode**2+static_impedance*port**2)/2)
    check('work_storage_identity', (sy.diff(energy, time)-port_dot*traction).subs(
        sy.diff(mode, time, 2), -eigenvalue*mode-coupling*sy.diff(port, time, 2)))
    squared, frequency = sy.symbols('s k', positive=True)
    response = static_impedance-squared*norm-squared**2*coupling**2/(eigenvalue-squared)
    amplitude = coupling*squared/(eigenvalue-squared)
    harmonic_norm = norm+2*coupling*amplitude+amplitude**2
    check('spectral_norm_derivative', -sy.diff(response, squared)-harmonic_norm)
    averaged_energy = (squared*harmonic_norm+eigenvalue*amplitude**2+static_impedance)/2
    check('periodic_storage_Legendre_recovery', averaged_energy-(response-2*squared*sy.diff(response, squared))/2)
    check('periodic_boundary_action_derivative', frequency*sy.diff(-response.subs(squared, frequency**2)/2, frequency)
          +response.subs(squared, frequency**2)/2-averaged_energy.subs(squared, frequency**2))
    check('quartic_remainder_identity', response-static_impedance+squared*norm+squared**2*coupling**2/eigenvalue
          +squared**3*coupling**2/(eigenvalue*(eigenvalue-squared)))
    approximate_lagrangian = (norm*port_dot**2-static_impedance*port**2+spectral_moment*sy.diff(port, time, 2)**2)/2
    approximate_traction = static_impedance*port+norm*sy.diff(port, time, 2)-spectral_moment*sy.diff(port, time, 4)
    variation = sy.diff(approximate_lagrangian, port)-sy.diff(sy.diff(approximate_lagrangian, port_dot), time)
    variation += sy.diff(sy.diff(approximate_lagrangian, sy.diff(port, time, 2)), time, 2)
    check('derived_local_derivative_action', variation+approximate_traction)
    approximate_energy = (norm*port_dot**2+static_impedance*port**2+
                          spectral_moment*(sy.diff(port, time, 2)**2-2*port_dot*sy.diff(port, time, 3)))/2
    check('derivative_expansion_work_identity', sy.diff(approximate_energy, time)-port_dot*approximate_traction)
    forced_frequency = sy.symbols('beta', positive=True)
    forced_mode = coupling*forced_frequency**2/(eigenvalue-forced_frequency**2)*(
        sy.cos(forced_frequency*time)-sy.cos(sy.sqrt(eigenvalue)*time))
    check('exact_causal_harmonic_convolution', sy.diff(forced_mode, time, 2)+eigenvalue*forced_mode
          -coupling*forced_frequency**2*sy.cos(forced_frequency*time))
    check('zero_initial_mode', forced_mode.subs(time, 0))
    check('zero_initial_mode_velocity', sy.diff(forced_mode, time).subs(time, 0))
    duration, carrier = sy.symbols('T carrier', positive=True)
    coefficients = [sy.Rational(10, 32), -sy.Rational(15, 64), -sy.Rational(15, 64),
                    sy.Rational(3, 32), sy.Rational(3, 32), -sy.Rational(1, 64), -sy.Rational(1, 64)]
    frequencies = [carrier, carrier+2*sy.pi/duration, carrier-2*sy.pi/duration,
                   carrier+4*sy.pi/duration, carrier-4*sy.pi/duration,
                   carrier+6*sy.pi/duration, carrier-6*sy.pi/duration]
    for power in [0, 2, 4]:
        check(f'pulse_start_derivative_{power}', sum(weight*value**power for weight, value in zip(coefficients, frequencies)))
    check('pulse_sixth_derivative_normalization', -sum(weight*value**6 for weight, value in zip(coefficients, frequencies))-720*(sy.pi/duration)**6)
    grid_early, grid_late, diagonal, past_weight = sy.symbols('q0 q1 diag past', real=True)
    matrix = sy.Matrix([[diagonal, 0], [past_weight, diagonal]])
    history = sy.Matrix([grid_early, grid_late])
    single_action = (history.T*matrix*history)[0]/2
    single_gradient = sy.Matrix([sy.diff(single_action, entry) for entry in history])
    check('single_history_symmetrizes_kernel', (single_gradient-(matrix+matrix.T)*history/2).dot(sy.ones(2, 1)))
    difference_early, difference_late = sy.symbols('qm0 qm1', real=True)
    doubled_action = (sy.Matrix([difference_early, difference_late]).T*matrix*history)[0]
    double_gradient = sy.Matrix([sy.diff(doubled_action, entry) for entry in [difference_early, difference_late]])
    check('doubled_history_keeps_retarded_kernel', (double_gradient-matrix*history).dot(sy.ones(2, 1)))
    envelope, speed, potential = [sy.Function(name)(coordinate) for name in ['w', 'f', 'V']]
    full_master = coordinate**3*envelope
    material = 6/coordinate**2+3*sy.diff(speed, coordinate)/(coordinate*speed)-potential/speed**2
    full_density = speed*sy.diff(full_master, coordinate)**2+potential*full_master**2/speed
    envelope_density = speed*coordinate**6*sy.diff(envelope, coordinate)**2-speed*coordinate**6*material*envelope**2
    check('regular_envelope_surface_contact', full_density-envelope_density-sy.diff(3*speed*coordinate**5*envelope**2, coordinate))
    chi = sy.symbols('chi', positive=True)
    companion_fraction = 1-chi
    radius_flux = 32*companion_fraction/chi
    induced_mass_flux = sy.Rational(16, 3)*companion_fraction/chi
    current_flux = (1-2*chi)/(3*chi)
    energy_slope = -308*companion_fraction/chi
    flux = radius_flux+induced_mass_flux+current_flux
    check('inherited_finite_mass_flux_regression', flux-(114*companion_fraction-1)/(3*chi))
    check('inherited_finite_mass_chirp_regression', flux-energy_slope-(1038*companion_fraction-1)/(3*chi))
    check('testmass_source_limit_regression', flux.subs(chi, 1)+sy.Rational(1, 3))
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'checks': checks, 'exact_checks': len(checks), 'new_free_response_parameters': 0,
              'traction': 'p=Y0*q+I*q_ddot+sum(a_n*eta_n_ddot)',
              'mode_equation': 'eta_n_ddot+lambda_n*eta_n=-a_n*q_ddot',
              'energy_law': 'dE/dtau=q_dot*p, before multiplying by kappa/R',
              'derivative_action': 'L=(I*q_dot^2-Y0*q^2+J1*q_ddot^2)/2',
              'derivative_energy': 'E=(I*q_dot^2+Y0*q^2+J1*(q_ddot^2-2*q_dot*q_third))/2',
              'finite_mass_coefficients_role': 'Regression of stage23, not a new finite-frequency two-body flux calculation.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
