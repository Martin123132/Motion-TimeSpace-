from __future__ import annotations

import sympy as sp

from budget import ROOT, BRANCH, read_json, digest, save, dependencies, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.factor(sp.cancel(expression))
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, residual=str(residual), passed=True))

    alpha, beta, slope, sigma, real_source, dirichlet, normalization = sp.symbols('alpha beta slope sigma real_source dirichlet normalization', real=True)
    wronskian = alpha-slope+sp.I*beta
    overlap = real_source+sp.I*beta*dirichlet
    direct = real_source+(slope-alpha)*dirichlet
    full = direct/(wronskian*normalization)
    frozen = (direct+sigma*dirichlet)/((wronskian-sigma)*normalization)
    exact('finite boundary-response replacement', frozen-full-sigma*overlap/(wronskian*(wronskian-sigma)*normalization))
    current = beta/((alpha-slope)**2+beta**2)
    exact('outgoing current quadratic', current*beta**2-beta+current*(alpha-slope)**2)
    semilatus, geometric, action_z, epsilon = sp.symbols('p e2 zeta eps')
    shrink, second, gamma, derivative, displacement, displacement_prime, conversion, conversion_prime = sp.symbols('P P2 G Pprime f fprime g gprime')
    direct_frequency_rate = shrink+geometric*(second+displacement_prime*shrink+displacement*gamma)
    transformed = direct_frequency_rate.subs(shrink, shrink-displacement*geometric*derivative).expand()
    transformed = sp.series(transformed, geometric, 0, 2).removeO().subs(geometric, action_z/conversion)
    frequency_second = (second+displacement_prime*shrink+displacement*gamma-displacement*derivative)/conversion
    exact('fixed azimuthal-frequency rate with endpoint displacement', transformed-shrink-action_z*frequency_second)
    action_rate = geometric*(conversion*gamma+conversion_prime*shrink)
    exact('action eccentricity conversion', action_rate.subs(geometric, action_z/conversion)-action_z*(gamma+conversion_prime*shrink/conversion))
    tidal, amplitude = sp.symbols('ell K')
    parent37 = BRANCH/'postcircular-clock-20261005/results/weak-field/status.json'
    parent35 = BRANCH/'near-circular-quadrupole-20261005/results/stage-integrity.json'
    tidal_second = sp.sympify(read_json(parent37)['tidal_P2_coefficient'])
    tidal_gamma = sp.sympify(read_json(parent35)['outgoing_tidal_coefficient'])
    normal = -amplitude/semilatus**3
    newtonian_shrink = normal*(1+6*tidal)
    radial_derivative = sp.diff(normal, semilatus)*(1+6*tidal)+normal*6*(-5*tidal/semilatus)
    newtonian_gamma = sp.Rational(19, 6)*normal/semilatus*(1+tidal_gamma*tidal)
    mapped = frequency_second.subs({second:normal*(-sp.Rational(5, 8)+tidal_second*tidal),
        shrink:newtonian_shrink, gamma:newtonian_gamma, derivative:radial_derivative,
        displacement:semilatus, displacement_prime:1, conversion:1})
    exact('Newtonian fixed-frequency eccentric chirp', mapped/normal-sp.Rational(157, 24)-sp.Rational(837, 4)*tidal)
    delta_shrink, delta_second, delta_gamma, delta_log, transport = sp.symbols('dP dX dG dL Z')
    exact('first-order log-transport difference',
        sp.diff((gamma+epsilon*delta_gamma)/(shrink+epsilon*delta_shrink), epsilon).subs(epsilon, 0)
        -(delta_gamma*shrink-gamma*delta_shrink)/shrink**2)
    exact('first-order circular clock difference',
        sp.diff(1/(shrink+epsilon*delta_shrink), epsilon).subs(epsilon, 0)+delta_shrink/shrink**2)
    eccentric_kernel = -transport*(1+epsilon*delta_log)*(second+epsilon*delta_second)/(shrink+epsilon*delta_shrink)**2
    exact('first-order mixed clock difference', sp.diff(eccentric_kernel, epsilon).subs(epsilon, 0)
        +transport/shrink**2*(delta_second+second*delta_log-2*second*delta_shrink/shrink))
    report = save('derivation', __file__, dict(checks=checks, exact_checks=len(checks),
        input_hashes={**dependencies(), str(parent37):digest(parent37), str(parent35):digest(parent35)},
        coordinate_map='x=D/M=p+f(p)e_geo^2, f=-2p alpha_phi/3; zeta=g(p)e_geo^2, g=sqrt(p(p-6))/(p-2)',
        frequency_rate='P0+zeta*(P2+fprime*P0+f*Gamma0-f*P0prime)/g',
        action_damping='Gamma0+(gprime/g)*P0',
        caveat='Frozen real master slope at the inherited surface is an operational split, not a unique covariant matter/geometry separation.'))
    print(len(checks), 'exact identities passed', flush=True)


if __name__ == '__main__':
    main()
