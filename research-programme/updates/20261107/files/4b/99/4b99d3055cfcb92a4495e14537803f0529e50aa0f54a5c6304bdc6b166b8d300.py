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
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    radius, polar, azimuth, time = sp.symbols('r theta phi time', real=True)
    alpha, omega = sp.symbols('alpha omega', positive=True)
    metric, lapse, field, response = [sp.Function(name)(radius) for name in ['F', 'nu', 'h', 'q']]
    potential = sp.Function('W')(field)
    spatial = [1/metric, radius**2, radius**2*sp.sin(polar)**2]
    coordinates = [radius, polar, azimuth]
    connection = {}
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                numerator = (sp.diff(spatial[upper], coordinates[left]) if upper == right else 0)
                numerator += sp.diff(spatial[upper], coordinates[right]) if upper == left else 0
                numerator -= sp.diff(spatial[left], coordinates[upper]) if left == right else 0
                connection[upper, left, right] = sp.simplify(numerator/(2*spatial[upper]))
    checks = []

    def exact(name, expression):
        reduced = sp.factor(sp.trigsimp(expression))
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    log_shift_weight = sp.diff(lapse, radius)-sp.diff(metric, radius)/(2*metric)
    for degree in [2, 3]:
        harmonic = sp.sin(polar)*sp.diff(sp.legendre(degree, sp.cos(polar)), polar)
        shift = [0, 0, response*harmonic]
        extrinsic = sp.zeros(3)
        for left in range(3):
            for right in range(3):
                numerator = sp.diff(shift[right], coordinates[left])+sp.diff(shift[left], coordinates[right])
                numerator -= sum(2*connection[index, left, right]*shift[index] for index in range(3))
                extrinsic[left, right] = sp.simplify(numerator/(2*sp.exp(lapse)))
        exact('zero_extrinsic_trace_l'+str(degree), sum(extrinsic[index, index]/spatial[index] for index in range(3)))
        mixed = sp.diag(*(1/value for value in spatial))*extrinsic
        momentum = []
        for lower in range(3):
            value = sum(sp.diff(mixed[upper, lower], coordinates[upper]) for upper in range(3))
            for upper in range(3):
                for other in range(3):
                    value += connection[upper, upper, other]*mixed[other, lower]
                    value -= connection[other, upper, lower]*mixed[upper, other]
            momentum.append(sp.trigsimp(value))
        expected = sp.diff(response, radius, 2)-log_shift_weight*sp.diff(response, radius)
        expected += (2*log_shift_weight/radius-2/radius**2-(degree*(degree+1)-2)/(radius**2*metric))*response
        exact('ADM_momentum_equation_l'+str(degree), momentum[2]*2*sp.exp(lapse)/(metric*harmonic)-expected)
        exact('ADM_radial_constraint_l'+str(degree), momentum[0])
        exact('ADM_polar_constraint_l'+str(degree), momentum[1])
    kinetic_time = omega**2*field**2*sp.exp(-2*lapse)
    kinetic_radius = metric*sp.diff(field, radius)**2
    density = (kinetic_time+kinetic_radius)/2+potential
    radial_pressure = (kinetic_time+kinetic_radius)/2-potential
    tangential_pressure = (kinetic_time-kinetic_radius)/2-potential
    trace_stress = kinetic_time-kinetic_radius-4*potential
    exact('trace_reversed_axial_stress', tangential_pressure-trace_stress/2-potential)
    axial_metric = sp.symbols('axial_metric')
    shift_angular = axial_metric/(radius**2*sp.sin(polar)**2)
    delta_time_angular_stress = tangential_pressure*axial_metric
    background_angular_stress = tangential_pressure*radius**2*sp.sin(polar)**2
    exact('Eulerian_axial_momentum_zero', delta_time_angular_stress-shift_angular*background_angular_stress)
    current_time = omega*field**2*sp.exp(-2*lapse)
    current_angular = -omega*field**2*shift_angular*sp.exp(-2*lapse)
    exact('coordinate_current_follows_shift', current_angular+shift_angular*current_time)
    metric_prime = (1-metric)/radius-2*alpha*radius*density
    lapse_prime = ((1-metric)/2+alpha*radius**2*radial_pressure)/(radius*metric)
    scalar_second = (sp.diff(potential, field)-omega**2*sp.exp(-2*lapse)*field)/metric
    scalar_second -= (2/radius+lapse_prime+metric_prime/(2*metric))*sp.diff(field, radius)
    rules = {sp.diff(metric, radius): metric_prime, sp.diff(lapse, radius): lapse_prime,
             sp.diff(field, radius, 2): scalar_second}
    rules[sp.diff(lapse, radius, 2)] = sp.diff(lapse_prime, radius).subs(rules, simultaneous=True)
    exact('background_shift_coefficient', log_shift_weight.subs(rules)-alpha*radius*(density+radial_pressure)/metric)
    coordinates4 = [time, radius, polar, azimuth]
    background = [-sp.exp(2*lapse), *spatial]
    perturbation = sp.zeros(4)
    harmonic = sp.sin(polar)*sp.diff(sp.legendre(2, sp.cos(polar)), polar)
    perturbation[0, 3] = perturbation[3, 0] = response*harmonic
    inverse_delta = sp.Matrix(4, 4, lambda left, right: -perturbation[left, right]/(background[left]*background[right]))
    gamma, delta_gamma = {}, {}
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                first, second = 0, 0
                for other in range(4):
                    ordinary = (sp.diff(background[other], coordinates4[left]) if other == right else 0)
                    ordinary += sp.diff(background[other], coordinates4[right]) if other == left else 0
                    ordinary -= sp.diff(background[left], coordinates4[other]) if left == right else 0
                    changed = sp.diff(perturbation[other, right], coordinates4[left])+sp.diff(perturbation[other, left], coordinates4[right])-sp.diff(perturbation[left, right], coordinates4[other])
                    first += ordinary/background[upper]/2 if other == upper else 0
                    second += inverse_delta[upper, other]*ordinary/2
                    second += changed/background[upper]/2 if other == upper else 0
                gamma[upper, left, right] = sp.simplify(first)
                delta_gamma[upper, left, right] = sp.simplify(second)

    def ricci(left, right):
        value = 0
        for contracted in range(4):
            value += sp.diff(delta_gamma[contracted, left, right], coordinates4[contracted])
            value -= sp.diff(delta_gamma[contracted, left, contracted], coordinates4[right])
            for other in range(4):
                value += delta_gamma[contracted, left, right]*gamma[other, contracted, other]
                value += gamma[contracted, left, right]*delta_gamma[other, contracted, other]
                value -= delta_gamma[other, left, contracted]*gamma[contracted, right, other]
                value -= gamma[other, left, contracted]*delta_gamma[contracted, right, other]
        return sp.trigsimp(value)

    expected = sp.diff(response, radius, 2)-log_shift_weight*sp.diff(response, radius)
    expected += (2*log_shift_weight/radius-2/radius**2-4/(radius**2*metric))*response
    direct = ricci(0, 3)/harmonic-2*alpha*potential*response
    exact('independent_4D_Ricci_matches_ADM', (direct+metric*expected/2).subs(rules, simultaneous=True))
    for left, right in [(0, 0), (1, 1), (2, 2), (3, 3), (1, 3), (2, 3), (0, 1), (0, 2), (1, 2)]:
        exact('remaining_Ricci_'+str(left)+str(right), ricci(left, right))
    mass, center_density, center_pressure = sp.symbols('M rho0 p0', real=True)
    vacuum = expected.subs({log_shift_weight: 0})
    growing = radius**3-2*mass*radius**2
    vacuum_operator = lambda value: sp.diff(value, radius, 2)-(6*radius-4*mass)*value/(radius**2*(radius-2*mass))
    exact('vacuum_growing_solution', vacuum_operator(growing))
    center_coefficient = sp.symbols('a2')
    center_solution = radius**3*(1+center_coefficient*radius**2)
    center_equation = sp.diff(center_solution, radius, 2)-alpha*radius*(center_density+center_pressure)*sp.diff(center_solution, radius)
    center_equation -= (6/radius**2+alpha*(sp.Rational(8, 3)*center_density-2*(center_density+center_pressure)))*center_solution
    exact('regular_center_coefficient', sp.expand(center_equation).coeff(radius, 3).subs(center_coefficient, alpha*(sp.Rational(11, 3)*center_density+center_pressure)/14))
    mass_profile, weak_y = sp.Function('m')(radius), sp.Function('y')(radius)
    weak_density, weak_pressure = sp.Function('rho')(radius), sp.Function('p')(radius)
    weak_operator = sp.diff(radius**3*weak_y, radius, 2)-6*radius*weak_y
    exact('weak_radial_integrating_factor', radius**3*weak_operator-sp.diff(radius**6*sp.diff(weak_y, radius), radius))
    weak_rhs = radius**6*(weak_density+weak_pressure)+8*radius**3*mass_profile
    identity = sp.diff(2*radius**4*mass_profile, radius)+radius**6*(weak_pressure-weak_density)
    exact('weak_moment_integration_by_parts', (weak_rhs-identity).subs(sp.diff(mass_profile, radius), radius**2*weak_density))
    exact('weak_response_potential_only', density-radial_pressure-2*potential)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'radial_equation': str(expected), 'direct_Ricci_tphi_over_harmonic': str(direct),
              'matter_coefficient': 'A=alpha*r*(rho+p_r)/F=nu_prime-F_prime/(2F)',
              'regular_center': 'q=r^3[1+alpha*(11*rho0/3+p_r0)*r^2/14+O(r^4)]',
              'vacuum_basis': 'P=r^3*(1-2M/r); Q=r^-2*hypergeom(1,4;6;2M/r); W(P,Q)=-5',
              'weak_response': 'lim_alpha_to_zero (b/a)/alpha = (1/5)*integral r^6*(rho-p_r)dr = (2/5)*integral r^6 W(h)dr >0',
              'current': 'delta j^A=-beta^A*j^t, whereas Eulerian momentum density S_A=0',
              'assumptions': ['Static linear odd-parity perturbation of the same nonrotating spherical complex scalar.', 'No axial scalar harmonic or vortical matter mode introduced.', 'Retained Einstein-Hilbert dynamics, not an emergent derivation of G.']}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'weak_response': report['weak_response']}))


if __name__ == '__main__':
    main()
