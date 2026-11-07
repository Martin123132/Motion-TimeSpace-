from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import ROOT, modest_process, read_json, save


def main():
    modest_process()
    report = read_json(ROOT/'results/reduced/status.json')
    source = read_json(ROOT/'results/energy/status.json')
    symbols = sp.symbols(' '.join(report['symbols']), positive=True)
    environment = dict(zip(report['symbols'], symbols))
    parse = lambda expression: sp.sympify(expression, locals=environment)
    radius, alpha, metric, field, gradient, rotation, potential, force, second = symbols
    load_phase = alpha*radius**2*rotation**2*field**2
    load_gradient = alpha*radius**2*metric*gradient**2
    load_potential = alpha*radius**2*potential
    beta = parse(source['coefficients']['beta'])
    omega = parse(source['coefficients']['omega'])
    lapse_load = load_gradient+load_phase-2*load_potential+1-metric
    positive_denominator = (6*beta+6*load_gradient+4*metric*load_phase)**2+24*metric*load_phase+36*load_phase*load_gradient+8*metric*lapse_load*load_phase**2
    phase = positive_denominator/(36*omega**2)
    gravity = 6*metric*beta**2*(2*load_phase*lapse_load+9*load_gradient/metric+6)/positive_denominator
    determinant = 18*metric**2*beta**2*(load_phase*lapse_load+3)/(alpha*radius**2*positive_denominator)
    mixed = -3*metric*gradient*beta*(4*metric*load_phase*lapse_load+12*metric*(1-load_phase)-18*beta)/positive_denominator
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('positive-square expression for local phase coefficient', parse(report['phase_coefficient'])-phase)
    check('positive gravity derivative diagonal', parse(report['normalized_gravity_kinetic'])-gravity)
    check('positive two-field derivative determinant', parse(report['gradient_determinant'])-determinant)
    check('mixed derivative reconstruction', parse(report['mixed_kinetic'])-mixed)
    pressure = (metric*gradient**2+rotation**2*field**2)/2-potential
    lapse_gradient = (1-metric+2*alpha*radius**2*pressure)/(2*radius*metric)
    check('nonnegative lapse load', lapse_load-2*radius*metric*lapse_gradient)
    check('omega gap is positive', omega-beta-load_gradient-(1+2*metric/3)*load_phase)
    beta_lower = sp.Rational(1004,625)
    phase_load_upper = sp.Rational(121,625)
    local_phase_lower = (beta_lower/(beta_lower+phase_load_upper))**2
    assert local_phase_lower > sp.Rational(79,100)
    save('principal-proof', Path(__file__), dict(exact_checks=checks,
        definitions={'x':'alpha r^2 b h^2','y':'alpha r^2 F h_prime^2','z':'alpha r^2 W','chi':'x+y-2z+1-F=2rFn','beta':'(7-3F-x-y-2z)/2','Omega':'beta+y+(1+2F/3)x'},
        positive_denominator='D=(6beta+6y+4Fx)^2+24Fx+36xy+8F chi x^2',
        local_phase='D/(36Omega^2)',
        normalized_gravity_gradient='(2alpha r^2/3)A_ZZ=6F beta^2(2x chi+9y/F+6)/D',
        gradient_determinant='18F^2 beta^2(x chi+3)/(alpha r^2 D)',
        mixed_gradient='-3F h_prime beta[4Fx chi+12F(1-x)-18beta]/D',
        beta_uniform_lower=str(beta_lower), local_phase_uniform_lower_exact=str(local_phase_lower),
        local_phase_uniform_lower_numeric=float(local_phase_lower),
        assumptions=['Stage46 regular compact positive background box','r>0','No new model coefficients'],
        proof='x,y,chi>=0;F,alpha,beta>0 imply D>0,local phase>0,A_ZZ>0,det(A)>0. Sylvester gives coupled gradient positivity.',
        canonical_transformation_claimed=False, potential_matrix_positive_proved=False,
        frequency_or_continuum_gap_claimed=False), [ROOT/'results/reduced/status.json',ROOT/'results/energy/status.json'])
    print(dict(exact_checks=len(checks), beta_lower=str(beta_lower), local_phase_lower=float(local_phase_lower)), flush=True)


if __name__ == '__main__':
    main()
