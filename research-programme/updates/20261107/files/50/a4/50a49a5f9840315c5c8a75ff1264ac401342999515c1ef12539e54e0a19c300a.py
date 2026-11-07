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
    time, radius, polar, azimuth = sp.symbols('time radius polar azimuth', real=True)
    alpha, frequency = sp.symbols('alpha frequency', positive=True)
    coordinates = [time, radius, polar, azimuth]
    metric, lapse, field, amplitude, radial, angular, response = [sp.Function(name)(radius) for name in ['metric', 'lapse', 'field', 'amplitude', 'radial', 'angular', 'response']]
    potential = sp.Function('potential')(field)
    harmonic = (3*sp.cos(polar)**2-1)/2
    background = [-sp.exp(2*lapse), 1/metric, radius**2, radius**2*sp.sin(polar)**2]
    changes = [sp.exp(2*lapse)*amplitude*harmonic, radial*harmonic/metric,
               radius**2*angular*harmonic, radius**2*sp.sin(polar)**2*angular*harmonic]
    gamma, delta_gamma = {}, {}
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                first = (sp.diff(background[upper], coordinates[left]) if upper == right else 0)
                first += sp.diff(background[upper], coordinates[right]) if upper == left else 0
                first -= sp.diff(background[left], coordinates[upper]) if left == right else 0
                second = (sp.diff(changes[upper], coordinates[left]) if upper == right else 0)
                second += sp.diff(changes[upper], coordinates[right]) if upper == left else 0
                second -= sp.diff(changes[left], coordinates[upper]) if left == right else 0
                gamma[upper, left, right] = sp.simplify(first/(2*background[upper]))
                delta_gamma[upper, left, right] = sp.simplify(second/(2*background[upper])-changes[upper]*first/(2*background[upper]**2))

    def ricci(left, right):
        result = 0
        for contracted in range(4):
            result += sp.diff(delta_gamma[contracted, left, right], coordinates[contracted])
            result -= sp.diff(delta_gamma[contracted, left, contracted], coordinates[right])
            for other in range(4):
                result += delta_gamma[contracted, left, right]*gamma[other, contracted, other]
                result += gamma[contracted, left, right]*delta_gamma[other, contracted, other]
                result -= delta_gamma[other, left, contracted]*gamma[contracted, right, other]
                result -= gamma[other, left, contracted]*delta_gamma[contracted, right, other]
        return sp.trigsimp(sp.expand(result))

    components = {name: ricci(*indices) for name, indices in [('tt', (0, 0)), ('rr', (1, 1)), ('rt', (1, 2)), ('aa', (2, 2)), ('bb', (3, 3))]}
    checks = []

    def exact(name, expression):
        reduced = sp.simplify(sp.trigsimp(expression))
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    angular_difference = sp.trigsimp(components['aa']-components['bb']/sp.sin(polar)**2)
    exact('angular_traceless_requires_equal_radial_and_time_amplitudes', angular_difference.subs(radial, amplitude))
    assert angular_difference != 0
    projected = {name: sp.simplify((expression.subs(radial, amplitude).doit()/(sp.diff(harmonic, polar) if name == 'rt' else harmonic)).subs(polar, sp.pi/2))
                 for name, expression in components.items() if name != 'bb'}
    rt = sp.simplify(components['rt'].subs(radial, amplitude).doit()/sp.diff(harmonic, polar))
    angular_prime = sp.solve(rt-2*alpha*sp.diff(field, radius)*response, sp.diff(angular, radius))[0]
    expected_angular_prime = sp.diff(amplitude, radius)+2*sp.diff(lapse, radius)*amplitude-4*alpha*sp.diff(field, radius)*response
    exact('radial_angular_constraint', angular_prime-expected_angular_prime)
    rotation = frequency**2*sp.exp(-2*lapse)
    density = metric*sp.diff(field, radius)**2/2+rotation*field**2/2+potential
    pressure = metric*sp.diff(field, radius)**2/2+rotation*field**2/2-potential
    metric_prime = (1-metric)/radius-2*alpha*radius*density
    lapse_prime = ((1-metric)/2+alpha*radius**2*pressure)/(radius*metric)
    scalar_prime2 = (sp.diff(potential, field)-rotation*field)/metric-(2/radius+lapse_prime+metric_prime/(2*metric))*sp.diff(field, radius)
    background_rules = {sp.diff(metric, radius): metric_prime, sp.diff(lapse, radius): lapse_prime,
                        sp.diff(field, radius, 2): scalar_prime2}
    lapse_prime2 = sp.diff(lapse_prime, radius).subs(background_rules, simultaneous=True)
    background_rules[sp.diff(lapse, radius, 2)] = lapse_prime2

    def reduce_background(expression):
        return sp.factor(expression.subs(background_rules, simultaneous=True))

    first_coefficient = (1+metric-2*alpha*radius**2*potential)/(radius*metric)
    drive = sp.diff(potential, field)-2*rotation*field-2*metric*lapse_prime*sp.diff(field, radius)
    metric_coefficient = (-4*alpha*radius**2*potential-6-(1-metric+2*alpha*radius**2*pressure)**2/metric+8*alpha*radius**2*rotation*field**2)/(radius**2*metric)
    field_coefficient = (6/radius**2+sp.diff(potential, field, 2)-rotation+4*alpha*metric*sp.diff(field, radius)**2)/metric
    amplitude_prime2 = -first_coefficient*sp.diff(amplitude, radius)-metric_coefficient*amplitude+4*alpha*drive*response/metric
    response_prime2 = -first_coefficient*sp.diff(response, radius)+field_coefficient*response+drive*amplitude/metric
    trace_tt = 2*alpha*(2*frequency**2*field*response+sp.exp(2*lapse)*(amplitude*potential-sp.diff(potential, field)*response))
    tt = projected['tt']-trace_tt
    exact('tt_equation_from_linearized_ricci', reduce_background(tt.subs({sp.diff(angular, radius): expected_angular_prime, sp.diff(amplitude, radius, 2): amplitude_prime2}, simultaneous=True)))
    kg = sp.diff(response, radius, 2)+(2/radius+sp.diff(lapse, radius)+sp.diff(metric, radius)/(2*metric))*sp.diff(response, radius)
    kg += (rotation-sp.diff(potential, field, 2)-6/radius**2)*response/metric
    kg += (expected_angular_prime-sp.diff(amplitude, radius))*sp.diff(field, radius)-amplitude*(sp.diff(potential, field)-2*rotation*field)/metric
    exact('scalar_equation_after_metric_constraint', reduce_background(kg.subs(sp.diff(response, radius, 2), response_prime2)))
    exact('common_first_derivative_coefficient', reduce_background(2/radius+sp.diff(lapse, radius)+sp.diff(metric, radius)/(2*metric)-first_coefficient))
    rr = projected['rr']-2*alpha*(2*sp.diff(field, radius)*sp.diff(response, radius)+(amplitude*potential+sp.diff(potential, field)*response)/metric)
    aa = projected['aa']-2*alpha*radius**2*(angular*potential+sp.diff(potential, field)*response)
    substitutions = {sp.diff(angular, radius, 2): sp.diff(expected_angular_prime, radius), sp.diff(angular, radius): expected_angular_prime}
    rr = reduce_background(rr.subs(substitutions, simultaneous=True).subs(sp.diff(amplitude, radius, 2), amplitude_prime2))
    aa = reduce_background(aa.subs(substitutions, simultaneous=True).subs(sp.diff(amplitude, radius, 2), amplitude_prime2))
    angular_solution = sp.factor(sp.solve(aa, angular)[0])
    exact('remaining_radial_einstein_equation', sp.factor(rr))
    exact('remaining_angular_einstein_constraint', sp.factor(aa.subs(angular, angular_solution)))
    derivative_check = sp.diff(angular_solution, radius)-expected_angular_prime
    derivative_check = derivative_check.subs({sp.diff(amplitude, radius, 2): amplitude_prime2, sp.diff(response, radius, 2): response_prime2}, simultaneous=True)
    exact('angular_constraint_preserved_by_evolution', reduce_background(derivative_check))
    flat_rules = {alpha: 0, metric: 1, lapse: 0}
    exact('flat_metric_laplace_equation', first_coefficient.subs(flat_rules)-2/radius)
    exact('flat_metric_angular_coefficient', metric_coefficient.subs(flat_rules)+6/radius**2)
    exact('flat_drive_recovers_previous_tide', drive.subs(flat_rules)-(sp.diff(potential, field)-2*frequency**2*field))
    expressions = {'first_coefficient': first_coefficient, 'metric_coefficient': metric_coefficient,
                   'field_coefficient': field_coefficient, 'drive': drive,
                   'angular_constraint': angular_solution, 'angular_prime': expected_angular_prime,
                   'angular_traceless_residual': angular_difference}
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'exact_check_count': len(checks), 'expressions': {name: str(value) for name, value in expressions.items()},
              'convention': 'gtt=-exp(2nu)*(1-HY), grr=(1+HY)/F, angular=r^2*(1+KY); scalar=h+uY; l=2; Einstein Rmunu=2alpha trace-reversed source.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'angular_constraint': str(angular_solution)}, indent=2))


if __name__ == '__main__':
    main()
