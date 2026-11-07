from __future__ import annotations

from pathlib import Path
import sympy as sp

from bound_common import modest_process, save


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    radius, alpha, frequency, eigenvalue = sp.symbols('r alpha w L', positive=True)
    field, amplitude, radial, angular, phase_momentum, sigma = sp.symbols('h u H K pi_v sigma')
    lapse, potential, force, second = sp.symbols('N W W_h W_hh', positive=True)
    rotation2 = frequency**2/lapse**2
    trace = radial/2+angular
    charge = (phase_momentum**2-2*frequency/lapse*phase_momentum*(2*amplitude+field*trace)+rotation2*(3*amplitude**2+2*field*amplitude*trace+field**2*(3*radial**2/8+angular**2+radial*angular/2)))/2
    completed = sigma**2/2+rotation2*(-amplitude**2-2*field*amplitude*trace+field**2*(radial**2/8-radial*angular/2))/2
    check('local canonical charge square', charge.subs(phase_momentum, sigma+frequency/lapse*(2*amplitude+field*trace))-completed)
    potential_energy = second*amplitude**2/2+force*amplitude*trace+potential*(radial*angular/2-radial**2/8)
    completed_potential = sigma**2/2+(second-rotation2)*amplitude**2/2+(force-rotation2*field)*amplitude*trace+(potential-rotation2*field**2/2)*(radial*angular/2-radial**2/8)
    check('combined square and scalar potential', completed+potential_energy-completed_potential)
    metric, field_prime, amplitude_prime, geometric, geometric_prime, conformal_derivative = sp.symbols('F hp up Q Qp D_K')
    old_source = -metric*geometric_prime/radius-((eigenvalue/2+1)/radius**2-2*alpha*potential)*geometric+2*alpha*((force-rotation2*field)*amplitude+metric*field_prime*amplitude_prime+frequency*field*phase_momentum/lapse)
    shifted_source = -metric*geometric_prime/radius-((eigenvalue/2+1)/radius**2-alpha*(2*potential+rotation2*field**2))*geometric+2*alpha*((force+rotation2*field)*amplitude+metric*field_prime*amplitude_prime+frequency*field*sigma/lapse)
    substituted = old_source.subs(phase_momentum, sigma+frequency/lapse*(2*amplitude+field*(geometric/2+3*angular/2)))
    check('square changes conformal constraint operator', substituted-shifted_source-3*alpha*rotation2*field**2*angular)
    density = frequency*field*phase_momentum/lapse-rotation2*field**2*(radial+2*angular)/2-rotation2*field*amplitude-metric*field_prime**2*radial/2+metric*field_prime*amplitude_prime+force*amplitude
    check('completed momentum cancels charge metric density variation', density.subs(phase_momentum, sigma+frequency/lapse*(2*amplitude+field*trace))-(frequency*field*sigma/lapse+(force+rotation2*field)*amplitude+metric*field_prime*amplitude_prime-metric*field_prime**2*radial/2))
    radial_coordinate = sp.symbols('x', positive=True)
    background_metric = sp.Function('F')(radial_coordinate)
    log_gradient = sp.Function('n')(radial_coordinate)
    rotation = sp.Function('b')(radial_coordinate)
    background_field = sp.Function('h')(radial_coordinate)
    force_function = sp.Function('W_h')(background_field)
    derivative = sp.diff(background_field, radial_coordinate)
    second_derivative = sp.diff(background_field, radial_coordinate, 2)
    transport = 2*background_metric/radial_coordinate+background_metric*log_gradient+sp.diff(background_metric, radial_coordinate)/2
    background_equation = background_metric*second_derivative+transport*derivative-force_function+rotation*background_field
    translation = sp.sqrt(background_metric)*derivative
    scalar_operator_translation = -background_metric*sp.diff(translation, radial_coordinate, 2)-transport*sp.diff(translation, radial_coordinate)+(sp.diff(force_function, background_field)-rotation+eigenvalue/radial_coordinate**2)*translation
    remainder = (eigenvalue-2*background_metric)/radial_coordinate**2+sp.diff(background_metric, radial_coordinate)/radial_coordinate+sp.diff(background_metric, radial_coordinate)*log_gradient/2+background_metric*sp.diff(log_gradient, radial_coordinate)+sp.diff(rotation, radial_coordinate)*background_field/derivative
    check('curved translation scalar factorization', scalar_operator_translation-translation*remainder+sp.sqrt(background_metric)*sp.diff(background_equation, radial_coordinate))
    metric_prime, log_prime, background_energy = sp.symbols('Fp np W')
    symbols_remainder = (eigenvalue-2*metric)/radius**2+metric_prime/radius+metric_prime*sp.Symbol('n')/2+metric*log_prime-2*rotation2*sp.Symbol('n')*field/field_prime
    lapse_gradient = sp.Symbol('n')
    mass_equation = (1-metric)/radius-alpha*radius*(metric*field_prime**2+rotation2*field**2+2*background_energy)
    lapse_equation = 2*alpha*(rotation2*field**2-background_energy)/metric-lapse_gradient**2-(2/radius+metric_prime/(2*metric))*lapse_gradient
    pressure_equation = ((1-metric)/2+alpha*radius**2*((metric*field_prime**2+rotation2*field**2)/2-background_energy))/(radius*metric)
    simplified = (eigenvalue-2*metric)/radius**2-2*alpha*(metric*field_prime**2+background_energy)-metric*lapse_gradient**2-2*rotation2*lapse_gradient*field/field_prime
    check('Einstein simplification of scalar coercivity potential', (symbols_remainder.subs(log_prime, lapse_equation)-simplified).subs({metric_prime:mass_equation, lapse_gradient:pressure_equation}))
    weight_gradient = sp.Function('a')(radial_coordinate)
    seed = sp.Function('z')(radial_coordinate)
    test = sp.Function('u')(radial_coordinate)
    scalar_remainder = sp.Function('B')(radial_coordinate)
    scalar_potential = sp.diff(weight_gradient*sp.diff(seed, radial_coordinate), radial_coordinate)/seed+scalar_remainder
    check('scalar ground state energy including contact', weight_gradient*sp.diff(test, radial_coordinate)**2+scalar_potential*test**2-weight_gradient*seed**2*sp.diff(test/seed, radial_coordinate)**2-scalar_remainder*test**2-sp.diff(weight_gradient*sp.diff(seed, radial_coordinate)/seed*test**2, radial_coordinate))
    assert sp.expand(substituted-shifted_source).coeff(angular) != 0
    report = save('completion', Path(__file__), dict(exact_checks=checks,
        phase_completed_operator='Dtilde_l = D_l - 3 alpha b h^2',
        shifted_source=str(shifted_source),
        scalar_coercivity_potential=str(simplified),
        scalar_seed='sqrt(F)*h_prime',
        phase_operator_sufficient_condition='sup 3 alpha r^2 b h^2 < L',
        scalar_sufficient_condition='h_prime<0, n>=0, F<=1, sup [2 alpha r^2(F h_prime^2+W)+r^2 F n^2] < L-2',
        frozen_K_completion_negative_control_detected=True,
        full_reduced_phase_Schur_diagonalized_by_local_sigma=False,
        mixed_interior_energy_bound_proved=False))
    print(dict(state=report['state'], exact_checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()
