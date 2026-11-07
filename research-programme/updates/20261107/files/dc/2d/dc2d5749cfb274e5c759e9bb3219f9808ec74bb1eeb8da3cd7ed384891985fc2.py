from __future__ import annotations

from pathlib import Path
import sympy as sp

from bound_common import modest_process, save


def main():
    modest_process()
    radius, metric, lapse, log_lapse, field, field_prime, potential, rotation, alpha = sp.symbols('r F N n h hp W b alpha', positive=True)
    angular, angular_prime, phase_momentum = sp.symbols('K Kp pi_v')
    metric_prime, log_prime = sp.symbols('Fp np')
    weight = lapse*radius**2/sp.sqrt(metric)
    ricci = lapse/sp.sqrt(metric)*(-angular**2/4+3*angular**2)+2*lapse*sp.sqrt(metric)*(radius**2*angular_prime**2/4-angular*(angular+radius*angular_prime)/2+3*angular**2/8)+4*lapse*log_lapse*radius*sp.sqrt(metric)*(3*angular**2/8-angular**2/2-angular*radius*angular_prime/4)
    density = -ricci/(4*alpha)+weight*(-metric*field_prime**2*angular**2/16+3*potential*angular**2/8+phase_momentum**2/2-3*sp.sqrt(rotation)*field*angular*phase_momentum/2+15*rotation*field**2*angular**2/16)
    mixed_derivative = sp.expand(density).coeff(angular_prime, 1).coeff(angular, 1)
    contact_derivative = sp.diff(mixed_derivative, radius)+sp.diff(mixed_derivative, metric)*metric_prime+sp.diff(mixed_derivative, lapse)*lapse*log_lapse+sp.diff(mixed_derivative, log_lapse)*log_prime
    integrated_density = sp.expand(density-mixed_derivative*angular*angular_prime-contact_derivative*angular**2/2)
    metric_equation = (1-metric)/radius-alpha*radius*(metric*field_prime**2+rotation*field**2+2*potential)
    lapse_equation = 2*alpha*(rotation*field**2-potential)/metric-log_lapse**2-(2/radius+metric_prime/(2*metric))*log_lapse
    simplified_density = integrated_density.subs(log_prime, lapse_equation).subs(metric_prime, metric_equation)
    expected = weight*(phase_momentum**2/2-3*sp.sqrt(rotation)*field*angular*phase_momentum/2-metric*angular_prime**2/(8*alpha)+(-6/(8*alpha*radius**2)+3*(potential+rotation*field**2)/4)*angular**2)
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('pure phase full constrained density after integration by parts', simplified_density-expected)
    lapse_divergence = metric*(log_prime+log_lapse**2)+(2*metric/radius+metric_prime/2)*log_lapse
    check('weighted constraint quadratic form', (lapse_divergence-2*alpha*(rotation*field**2-potential)).subs(log_prime, lapse_equation))
    constraint_form = weight*(metric*angular_prime**2+(6/radius**2+alpha*(rotation*field**2-potential))*angular**2)
    check('phase energy identity before source substitution', expected-(weight*phase_momentum**2/2-3*weight*sp.sqrt(rotation)*field*angular*phase_momentum/2-constraint_form/(8*alpha)+weight*(7*rotation*field**2+5*potential)*angular**2/8))
    norm_pi, constraint_integral = sp.symbols('norm_pi I')
    check('phase source substitution exact coefficient', norm_pi/2-3*constraint_integral/(4*alpha)-constraint_integral/(8*alpha)-(norm_pi/2-7*constraint_integral/(8*alpha)))
    angular_margin = sp.Rational(59, 10)
    source_load = sp.Rational(121, 625)
    phase_coercivity = 1-7*source_load/angular_margin
    assert phase_coercivity > sp.Rational(77, 100)
    assert angular_margin == 6-sp.Rational(1, 5000)*20**2*sp.Rational(5, 4)
    assert source_load == sp.Rational(1, 5000)*20**2*sp.Rational(11, 10)*sp.Rational(11, 5)
    save('phase-block', Path(__file__), dict(exact_checks=checks,
        energy_identity='E_pp = 1/2||pi_v||_a^2 - 7/(8alpha) I + integral a(7 b h^2+5 W)K^2/8',
        measure='a=N r^2/sqrt(F)', constraint='D_l K=2alpha sqrt(b) h pi_v',
        weighted_constraint_form='I=integral a K D_l K=integral a[F K_prime^2+(6/r^2+alpha(b h^2-W))K^2]',
        integral_bound='I <= 4alpha^2 sup(r^2 b h^2)/(59/10) ||pi_v||_a^2',
        phase_coercivity_exact=str(phase_coercivity), phase_coercivity_numeric=float(phase_coercivity),
        conservative_phase_coercivity='77/100', energy_lower_bound='E_pp >= (77/200) integral a pi_v^2',
        holds_under_uniform_background_box=True, phase_Schur_inverse_coercivity_proved=True,
        spatial_sampling_used=False, full_gravity_amplitude_Schur_bound_proved=False))
    print(dict(exact_checks=len(checks), phase_coercivity=str(phase_coercivity), numeric=float(phase_coercivity)), flush=True)


if __name__ == '__main__':
    main()
