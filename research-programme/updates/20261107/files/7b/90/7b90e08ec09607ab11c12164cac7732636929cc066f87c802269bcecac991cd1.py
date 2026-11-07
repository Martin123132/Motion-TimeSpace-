from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import ROOT, modest_process, read_json, save


def main():
    modest_process()
    report = read_json(ROOT/'results/reduced-v2/status.json')
    source = read_json(ROOT/'results/energy-v2/status.json')
    symbols = sp.symbols(' '.join(report['symbols']), positive=True)
    environment = dict(zip(report['symbols'], symbols))
    parse = lambda expression: sp.sympify(expression, locals=environment)
    radius, alpha, metric, field, gradient, rotation, potential, force, second = symbols
    phase_load = alpha*radius**2*rotation**2*field**2
    gradient_load = alpha*radius**2*metric*gradient**2
    beta = parse(source['coefficients']['beta'])
    omega = parse(source['coefficients']['omega'])
    denominator = 3*(beta+gradient_load)**2+phase_load*(3*gradient_load+2*metric)
    phase = denominator/(3*omega**2)
    gravity = 9*beta**2*(3*gradient_load+2*metric)/(4*alpha*radius**2*denominator)
    mixed = 3*metric*gradient*beta*(3*beta-2*metric)/(2*denominator)
    determinant = 9*metric**2*beta**2/(2*alpha*radius**2*denominator)
    scalar_pivot = 2*metric**2/(3*gradient_load+2*metric)
    square_shift = 2*alpha*radius**2*metric*gradient*(3*beta-2*metric)/(3*beta*(3*gradient_load+2*metric))
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('phase positive-denominator identity', parse(report['phase_coefficient'])-phase)
    check('gravity principal coefficient identity', parse(report['normalized_gravity_kinetic'])*3/(2*alpha*radius**2)-gravity)
    check('mixed principal coefficient identity', parse(report['mixed_kinetic'])-mixed)
    check('two-field principal determinant identity', parse(report['gradient_determinant'])-determinant)
    check('scalar Schur pivot cancels all beta denominators', determinant/gravity-scalar_pivot)
    check('gradient square shift', mixed/gravity-square_shift)
    check('scalar principal square completion', parse(report['scalar_kinetic'])-gravity*square_shift**2-scalar_pivot)
    check('reconstruction denominator omega', omega-beta-phase_load-gradient_load)
    check('phase first lower bound residual', phase-((beta+gradient_load)/omega)**2-phase_load*(3*gradient_load+2*metric)/(3*omega**2))
    beta_lower = sp.Rational(1004,625)
    phase_load_upper = sp.Rational(121,625)
    local_phase_lower = (beta_lower/(beta_lower+phase_load_upper))**2
    assert local_phase_lower > sp.Rational(79,100)
    metric_lower = sp.Rational(7376,10000)
    gradient_load_upper = sp.Rational(246,625)*2
    pivot_lower = 2*metric_lower**2/(3*gradient_load_upper+2*metric_lower)
    save('principal-proof-v2', Path(__file__), dict(exact_checks=checks,
        definitions={'x':'alpha r^2 b h^2','y':'alpha r^2 F h_prime^2','beta':'(7-3F-x-y-2alpha r^2 W)/2','Omega':'beta+x+y'},
        positive_denominator='D=3(beta+y)^2+x(3y+2F)',
        phase_coefficient='D/(3Omega^2)',
        gravity_gradient='A_ZZ=9beta^2(3y+2F)/(4alpha r^2 D)',
        mixed_gradient='A_Zw=3F h_prime beta(3beta-2F)/(2D)',
        gradient_determinant='9F^2 beta^2/(2alpha r^2 D)',
        completed_gradient='A_ZZ*(Zprime+eta*wprime)^2 + [2F^2/(3y+2F)]*wprime^2',
        eta='2alpha r^2 F h_prime(3beta-2F)/(3beta(3y+2F))',
        minimal_assumptions=['r>0','alpha>0','F>0','beta>0','real h,h_prime,s'],
        background_box_source='Stage46 assumptions imply beta>=1004/625,x<=121/625,F>=.7376,y<=492/625 in the body; exterior has x=y=0,beta>=2.',
        beta_uniform_lower=str(beta_lower), local_phase_uniform_lower_exact=str(local_phase_lower),
        local_phase_uniform_lower_numeric=float(local_phase_lower),
        scalar_principal_pivot_lower_exact=str(pivot_lower), scalar_principal_pivot_lower_numeric=float(pivot_lower),
        proof='x,y>=0 and F,beta>0 imply D>0. The phase coefficient and both completed gradient-square coefficients are positive. This is a pointwise continuum principal-sector statement, not inferred from samples.',
        canonical_transformation_claimed=False, potential_matrix_positive_proved=False,
        full_energy_positive_claimed=False, frequency_or_continuum_gap_claimed=False),
        [ROOT/'results/reduced-v2/status.json',ROOT/'results/energy-v2/status.json'])
    print(dict(exact_checks=len(checks), local_phase_lower=float(local_phase_lower), scalar_pivot_lower=float(pivot_lower)), flush=True)


if __name__ == '__main__':
    main()
