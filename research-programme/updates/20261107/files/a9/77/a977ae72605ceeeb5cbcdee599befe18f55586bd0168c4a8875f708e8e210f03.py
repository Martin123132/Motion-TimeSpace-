from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/far-orbit-derivation-v2'
    output.mkdir(exist_ok=False)
    radius, mass, square_frequency, epsilon, orbit = sp.symbols('r M omega_squared epsilon D', positive=True)
    first_growing, second_growing, first_decaying, second_decaying = sp.symbols('p1 p2 q1 q2')
    metric = 1-2*mass/radius
    potential = metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)
    growing = radius**3/6+first_growing*mass*radius**2+second_growing*square_frequency*radius**5
    decaying = radius**(-2)+first_decaying*mass*radius**(-3)+second_decaying*square_frequency

    def first_order(value):
        return sp.diff(value.subs({mass: epsilon*mass, square_frequency: epsilon*square_frequency}), epsilon).subs(epsilon, 0).expand()

    def residual(value):
        return metric**2*sp.diff(value, radius, 2)+metric*sp.diff(metric, radius)*sp.diff(value, radius)+(square_frequency-potential)*value

    growing_equation = first_order(residual(growing))
    decaying_equation = first_order(residual(decaying))
    solved_growing = sp.solve([growing_equation.coeff(mass), growing_equation.coeff(square_frequency)], [first_growing, second_growing])
    solved_decaying = sp.solve([decaying_equation.coeff(mass), decaying_equation.coeff(square_frequency)], [first_decaying, second_decaying])
    growing, decaying = growing.subs(solved_growing), decaying.subs(solved_decaying)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('first_order_growing_wave_equation', first_order(residual(growing)))
    exact('first_order_decaying_wave_equation', first_order(residual(decaying)))
    source_constant = sp.Symbol('C_source', nonzero=True)
    jump_a = source_constant/3*(orbit-2*mass)/(2*orbit+3*mass)
    jump_b = -source_constant/6*(12*orbit**3-16*orbit**2*mass-24*orbit*mass**2-33*mass**3)/(orbit**2*(2*orbit+3*mass)**2)

    def source_overlap(value):
        return (jump_b*value-jump_a*metric*sp.diff(value, radius)).subs(radius, orbit).subs(square_frequency, 4*mass/orbit**3)

    ratio = sp.series(orbit**5*source_overlap(decaying)/source_overlap(growing), mass, 0, 2).removeO()
    exact('far_orbit_tidal_amplitude_first_PN', ratio-1-sp.Rational(85, 21)*mass/orbit)
    horizon_x, horizon_frequency = sp.symbols('x k')
    radius_scaled = 1+horizon_x
    metric_scaled = horizon_x/radius_scaled
    potential_over_metric = (96*radius_scaled**3+48*radius_scaled**2+36*radius_scaled+9)/(radius_scaled**3*(4*radius_scaled+3)**2)
    multiplier = radius_scaled**3*(4*radius_scaled+3)**2
    second_polynomial = sp.expand(multiplier*metric_scaled)
    first_polynomial = sp.Poly(sp.cancel(multiplier*(1/radius_scaled**2-2*sp.I*horizon_frequency)), horizon_x).as_expr()
    zeroth_polynomial = sp.cancel(-multiplier*potential_over_metric)
    exact('horizon_second_polynomial', second_polynomial-(49*horizon_x+154*horizon_x**2+177*horizon_x**3+88*horizon_x**4+16*horizon_x**5))
    exact('horizon_first_polynomial', first_polynomial-(49+105*horizon_x+72*horizon_x**2+16*horizon_x**3-2*sp.I*horizon_frequency*(49+203*horizon_x+331*horizon_x**2+265*horizon_x**3+104*horizon_x**4+16*horizon_x**5)))
    exact('horizon_zeroth_polynomial', zeroth_polynomial-(-189-420*horizon_x-336*horizon_x**2-96*horizon_x**3))
    level = sp.Symbol('n', integer=True, nonnegative=True)
    leading_recurrence = (level+1)*level*second_polynomial.coeff(horizon_x, 1)+(level+1)*first_polynomial.coeff(horizon_x, 0)
    exact('horizon_recursion_denominator', leading_recurrence-49*(level+1)*(level+1-2*sp.I*horizon_frequency))
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'growing_near_zone': str(growing), 'decaying_near_zone': str(decaying),
              'circular_source_overlap_ratio_times_D_fifth': str(ratio),
              'amplitude_difference_law': 'Delta A/A_BH = 3 lambda_static/D^5 [1 + (85/21) M/D + ...] in the fixed-body wide circular orbit limit.',
              'power_difference_leading': 'Delta P22/P22_BH = 6 lambda_static/D^5 + ...',
              'scope': 'First relative M/D correction derived from vacuum near-zone equations and conserved source. Body finite-frequency terms enter at sigma^2 proportional to D^-3 at fixed body. Higher orders and imaginary terms not fixed by this expansion.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
