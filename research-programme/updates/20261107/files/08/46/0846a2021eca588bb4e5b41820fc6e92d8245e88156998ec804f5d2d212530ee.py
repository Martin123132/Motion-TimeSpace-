from __future__ import annotations

from pathlib import Path
import sympy as sp

from bound_common import Background, BRANCH, modest_process, save


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    field, gradient, metric, metric_prime, radius, alpha, rotation, force, log_lapse, pressure, mass = sp.symbols('h hp F Fp r alpha b Wh n P m', positive=True)
    potential = 3*field**sp.Rational(4, 3)/8+field**4/8
    potential_force = sp.diff(potential, field)
    acceleration = (force-rotation*field)/metric-(2/radius+log_lapse+metric_prime/(2*metric))*gradient
    pressure_prime = metric_prime*gradient**2/2+metric*gradient*acceleration-rotation*log_lapse*field**2+rotation*field*gradient-force*gradient
    expected = -2*metric*gradient**2/radius-log_lapse*(metric*gradient**2+rotation*field**2)
    check('radial pressure balance', pressure_prime-expected)
    source = -2*metric*gradient**2/radius-mass/(radius**2*metric)*(metric*gradient**2+rotation*field**2)
    check('backward positive pressure integrating factor', expected.subs(log_lapse, mass/(radius**2*metric)+alpha*radius*pressure/metric)+alpha*radius/metric*(metric*gradient**2+rotation*field**2)*pressure-source)
    local_force_ratio = potential_force/field
    check('stationary minimum requires h at least one', 2*potential/field**2-local_force_ratio-(field**(-sp.Rational(2, 3))-field**2)/4)
    check('high branch force monotonicity', sp.diff(local_force_ratio, field)-field+field**(-sp.Rational(5, 3))/3)
    check('maximum amplitude inequality from positive potential term', local_force_ratio-field**2/2-field**(-sp.Rational(2, 3))/2)
    alpha_upper = sp.Rational(1, 5000)
    radius_upper = sp.Integer(20)
    rotation_upper = sp.Rational(11, 10)
    amplitude_square_upper = 2*rotation_upper
    pressure_upper = rotation_upper**2
    potential_upper = sp.Rational(5, 4)
    fractional_power_upper = sp.Rational(43, 25)
    assert fractional_power_upper**3 > amplitude_square_upper**2
    check('rational potential majorant', 3*fractional_power_upper/8+amplitude_square_upper**2/8-potential_upper)
    kinetic_upper = 2*pressure_upper+2*potential_upper
    density_upper = kinetic_upper/2+rotation_upper*amplitude_square_upper/2+potential_upper
    metric_lower = 1-2*alpha_upper*radius_upper**2*density_upper/3
    phase_load_upper = 3*alpha_upper*radius_upper**2*rotation_upper*amplitude_square_upper
    scalar_load_upper = 2*alpha_upper*radius_upper**2*(kinetic_upper+potential_upper)+alpha_upper**2*radius_upper**4*(density_upper/3+pressure_upper)**2/metric_lower
    assert metric_lower > 0
    assert phase_load_upper < sp.Rational(3, 5)
    assert scalar_load_upper < sp.Rational(53, 50)
    bounds = {name:dict(exact=str(value), numeric=float(value)) for name, value in dict(alpha_upper=alpha_upper, radius_upper=radius_upper, central_rotation_square_upper=rotation_upper, amplitude_square_upper=amplitude_square_upper, pressure_upper=pressure_upper, potential_upper=potential_upper, kinetic_upper=kinetic_upper, density_upper=density_upper, metric_lower=metric_lower, phase_load_upper=phase_load_upper, scalar_load_upper=scalar_load_upper, phase_barrier_lower=sp.Rational(27, 5), scalar_barrier_lower=sp.Rational(147, 50)).items()}
    background = Background()
    central_rotation = background.profile.row['central_local_frequency']**2
    membership = dict(alpha=background.alpha, radius=background.radius, central_rotation_square=central_rotation,
        inside_box=bool(background.alpha <= float(alpha_upper) and background.radius <= float(radius_upper) and central_rotation <= float(rotation_upper)),
        basis='Saved converged background parameters, not a new interval existence enclosure.')
    assert membership['inside_box']
    save('uniform', Path(__file__), dict(exact_checks=checks, rational_bounds=bounds, saved_background_membership=membership,
         theorem_hypotheses=['Regular static solution with F,N positive and alpha>0', 'h>0 on 0<r<R; h=h_prime=0 at finite surface', 'W=3h^(4/3)/8+h^4/8 and no surface stress shell', 'alpha<=1/5000, R<=20, b(0)<=11/10'],
         conclusions=['Pressure nonnegative from backward integrating factor', 'N nondecreasing, b nonincreasing', 'h strictly decreasing for a nontrivial positive compact profile', 'Uniform phase-completed elliptic angular margin 27/(5r^2)', 'Bare amplitude ground-state energy margin 147/(50r^2)'],
         background_existence_proved=False, full_mixed_Hamiltonian_bound_proved=False,
         spatial_sampling_used_for_analytic_bound=False), [background.profile.path, BRANCH/'self-gravity-20261003/results/fine/status.json'])
    print(dict(exact_checks=len(checks), bounds=bounds, saved_membership=membership), flush=True)


if __name__ == '__main__':
    main()
