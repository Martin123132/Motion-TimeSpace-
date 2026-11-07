from __future__ import annotations

import sympy as sp

from susceptibility import ROOT, BRANCH, read_json, digest, save, dependencies, modest_process


def main():
    modest_process()
    source = BRANCH/'dynamical-tides-20261004/results/reduction/status.json'
    report = read_json(source)
    symbols = sp.symbols(' '.join(report['coefficient_symbols']), real=True)
    namespace = dict(zip(report['coefficient_symbols'], symbols))
    radius, metric, lapse2, field, gradient, potential, potential_prime, potential_second, coupling, frequency, square = symbols
    coefficients = [sp.sympify(value, locals=namespace) for value in report['H_coefficients']]
    denominator = -3*metric*lapse2*coupling*gradient**2*radius**2+3*metric*lapse2+2*lapse2*potential*coupling*radius**2-7*lapse2+coupling*field**2*radius**2*frequency**2
    expected = [2*radius**2/denominator, -2*metric*radius/denominator, 0, 0,
                -4*coupling*field**2*radius**2*frequency/denominator, 0]
    checks = []

    def exact(name, expression):
        residual = sp.factor(sp.cancel(expression))
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    for index, value in enumerate(coefficients):
        exact('parent constraint derivative '+str(index), sp.diff(value, square)-expected[index])
        exact('affine frequency-square constraint '+str(index), sp.diff(value, square, 2))
    theta, radius_scale, omega = sp.symbols('theta R omega', real=True)
    master0, slope0, master_t, slope_t = sp.symbols('U0 V0 Ut Vt', real=True)
    ratio = (slope0+theta*slope_t)/(master0+theta*master_t)
    derivative = (slope_t-slope0/master0*master_t)/master0
    exact('surface quotient tangent', sp.diff(ratio, theta).subs(theta, 0)-derivative)
    exact('physical omega-squared coefficient', sp.diff(ratio.subs(theta, (omega*radius_scale)**2), omega, 2).subs(omega, 0)/2-radius_scale**2*derivative)
    exact('vanishing odd surface derivative', sp.diff(ratio.subs(theta, (omega*radius_scale)**2), omega).subs(omega, 0))
    static, quadratic, velocity, acceleration, value, slope = sp.symbols('s0 s2 velocity acceleration value slope', real=True)
    inertia = -quadratic
    lagrangian = (inertia*velocity**2-static*value**2)/2
    variation = sp.diff(lagrangian, value)-sp.diff(lagrangian, velocity, 2)*acceleration
    boundary_residual = slope+variation
    exact('matched canonical boundary action', boundary_residual-(slope-static*value+quadratic*acceleration))
    exact('Fourier boundary slope', boundary_residual.subs({slope:(static+quadratic*omega**2)*value, acceleration:-omega**2*value}))
    energy = velocity*sp.diff(lagrangian, velocity)-lagrangian
    exact('positive-form boundary energy expression', energy-(inertia*velocity**2+static*value**2)/2)
    energy_derivative = sp.diff(energy, value)*velocity+sp.diff(energy, velocity)*acceleration
    exact('surface work equals stored-energy rate', energy_derivative-velocity*(static*value-quadratic*acceleration))
    save('derivation', __file__, dict(input_hashes={**dependencies(), str(source):digest(source)}, checks=checks,
        exact_checks=len(checks), H_square_derivative=[str(value) for value in expected],
        tangent_equations='Y0prime=A0 Y0; Ytheta_prime=A0 Ytheta+A_theta Y0; B0[Ytheta,ptheta]=-Btheta[Y0,p0]',
        surface_law='s2=R^2*(Vtheta-s0*Utheta)/U0; theta=(omega R)^2',
        canonical_boundary_action='N/2 integral dt [(-s2)*(partial_t U_R)^2-s0*U_R^2], inherited positive modal normalization N',
        scope='Local analytic continuation conditional on a nonsingular normalized static BVP; no global spectral theorem or all-frequency stability claim.'))
    print(len(checks), 'exact identities passed', flush=True)


if __name__ == '__main__':
    main()
