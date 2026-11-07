from __future__ import annotations

import sympy as sy

from eccentric_radiation import ROOT, BRANCH, digest, modest_process, save_json, report_header


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sy.simplify(sy.expand(expression))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    mass, particle, radius, radial_speed, transverse_speed, momentum = sy.symbols('M mu r vr vt h', positive=True)
    jerk_squared = mass**2/radius**6*(4*radial_speed**2+transverse_speed**2)
    current_tensor_squared = particle**2*momentum**2/2*jerk_squared
    power = sy.Rational(16, 45)*current_tensor_squared
    check('current_quadrupole_STF_norm', power-sy.Rational(8, 45)*particle**2*momentum**2*mass**2/radius**6*(4*radial_speed**2+transverse_speed**2))
    circular = power.subs({radial_speed: 0, transverse_speed: sy.sqrt(mass/radius), momentum: sy.sqrt(mass*radius)})
    check('independent_circular_current_power', circular-sy.Rational(8, 45)*particle**2*mass**4/radius**6)
    anomaly, eccentricity = sy.symbols('chi e', real=True)
    integrand = (1+eccentricity*sy.cos(anomaly))**6+4*eccentricity**2*sy.sin(anomaly)**2*(1+eccentricity*sy.cos(anomaly))**4
    averaged = sy.integrate(sy.expand_trig(sy.expand(integrand)), (anomaly, 0, 2*sy.pi))/(2*sy.pi)
    polynomial = 1+sy.Rational(19, 2)*eccentricity**2+sy.Rational(69, 8)*eccentricity**4+sy.Rational(9, 16)*eccentricity**6
    check('Kepler_eccentric_average_polynomial', averaged-polynomial)
    check('circular_eccentric_limit', polynomial.subs(eccentricity, 0)-1)
    source = BRANCH/'axial-companion-20261005/25-axial-companion-source-and-radiated-power.md'
    output = ROOT/'results/newtonian-control'
    output.mkdir(parents=True, exist_ok=False)
    save_json(output/'status.json', {**report_header(__file__), 'checks': checks, 'exact_checks': len(checks),
              'input_hashes': {str(source): digest(source)},
              'averaged_power': '(8/45) mu^2 M^4/[a^6 (1-e^2)^(9/2)] * [1+19e^2/2+69e^4/8+9e^6/16]',
              'meaning': 'Independent leading STF current-quadrupole control on a Newtonian Kepler ellipse, same areal periapsis and e; finite Schwarzschild corrections expected.',
              'not_a_fitted_or_exact_finite_compactness_baseline': True})
    print({'state': 'complete', 'exact_checks': len(checks), 'polynomial': str(polynomial)})


if __name__ == '__main__':
    main()
