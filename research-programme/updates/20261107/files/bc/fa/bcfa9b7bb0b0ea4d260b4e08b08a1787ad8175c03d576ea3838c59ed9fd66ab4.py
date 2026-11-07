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
    output = ROOT/'results/derivation-v2'
    output.mkdir(parents=True, exist_ok=False)
    time, radius, polar, azimuth = sp.symbols('time radius polar azimuth', real=True)
    alpha, frequency, sigma = sp.symbols('alpha frequency sigma', real=True)
    coordinates = [time, radius, polar, azimuth]
    metric, lapse, field, amplitude, radial, angular, shift, response, phase = [sp.Function(name)(radius) for name in
        ['metric', 'lapse', 'field', 'amplitude', 'radial', 'angular', 'shift', 'response', 'phase']]
    potential = sp.Function('potential')(field)
    harmonic = (3*sp.cos(polar)**2-1)/2
    background = sp.diag(-sp.exp(2*lapse), 1/metric, radius**2, radius**2*sp.sin(polar)**2)
    inverse = background.inv()
    changes = sp.diag(sp.exp(2*lapse)*amplitude, radial/metric, radius**2*angular, radius**2*sp.sin(polar)**2*angular)*harmonic
    changes[0, 1] = changes[1, 0] = -sp.I*sigma*shift*harmonic
    inverse_change = -inverse*changes*inverse
    scalar_change = response*harmonic
    phase_change = sp.I*sigma*phase*harmonic

    def derivative(expression, index):
        return -sp.I*sigma*expression if index == 0 else sp.diff(expression, coordinates[index])

    gamma, delta_gamma = {}, {}
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                first, second = 0, 0
                for contracted in range(4):
                    background_part = sp.diff(background[contracted, right], coordinates[left])+sp.diff(background[contracted, left], coordinates[right])-sp.diff(background[left, right], coordinates[contracted])
                    change_part = derivative(changes[contracted, right], left)+derivative(changes[contracted, left], right)-derivative(changes[left, right], contracted)
                    first += inverse[upper, contracted]*background_part/2
                    second += (inverse[upper, contracted]*change_part+inverse_change[upper, contracted]*background_part)/2
                gamma[upper, left, right] = sp.simplify(first)
                delta_gamma[upper, left, right] = sp.simplify(second)
    print('connections derived', flush=True)

    def ricci(left, right):
        result = 0
        for contracted in range(4):
            result += derivative(delta_gamma[contracted, left, right], contracted)-derivative(delta_gamma[contracted, left, contracted], right)
            for other in range(4):
                result += delta_gamma[contracted, left, right]*gamma[other, contracted, other]+gamma[contracted, left, right]*delta_gamma[other, contracted, other]
                result -= delta_gamma[other, left, contracted]*gamma[contracted, right, other]+gamma[other, left, contracted]*delta_gamma[contracted, right, other]
        return sp.trigsimp(sp.expand(result))

    def source(left, right):
        result = (sp.diff(field, radius)*derivative(scalar_change, right) if left == 1 else 0)
        result += sp.diff(field, radius)*derivative(scalar_change, left) if right == 1 else 0
        result += 2*frequency**2*field*scalar_change if left == right == 0 else 0
        result += frequency*field**2*derivative(phase_change, right) if left == 0 else 0
        result += frequency*field**2*derivative(phase_change, left) if right == 0 else 0
        result += changes[left, right]*potential+background[left, right]*sp.diff(potential, field)*scalar_change
        return 2*alpha*result

    components = {name: ricci(*indices)-source(*indices) for name, indices in
                  [('tt', (0, 0)), ('tr', (0, 1)), ('ta', (0, 2)), ('rr', (1, 1)), ('ra', (1, 2)), ('aa', (2, 2)), ('bb', (3, 3))]}
    determinant = sp.exp(lapse)*radius**2*sp.sin(polar)/sp.sqrt(metric)
    volume_change = (inverse*changes).trace()/2
    background_box = sp.diff(determinant*metric*sp.diff(field, radius), radius)/determinant
    scalar_equation = sum(derivative(determinant*inverse[index, index]*derivative(scalar_change, index), index) for index in range(4))/determinant
    scalar_equation += sum(derivative(determinant*(inverse_change[index, 1]+volume_change*inverse[index, 1])*sp.diff(field, radius), index) for index in range(4))/determinant-volume_change*background_box
    scalar_equation += (frequency**2*sp.exp(-2*lapse)-sp.diff(potential, field, 2))*scalar_change-field*frequency**2*inverse_change[0, 0]-2*field*frequency*inverse[0, 0]*derivative(phase_change, 0)
    currents = [2*field*scalar_change*inverse[index, 0]*frequency+field**2*(inverse_change[index, 0]+volume_change*inverse[index, 0])*frequency+field**2*inverse[index, index]*derivative(phase_change, index) for index in range(4)]
    phase_equation = sum(derivative(determinant*currents[index], index) for index in range(4))/determinant
    checks = []

    def exact(name, expression):
        reduced = sp.factor(sp.trigsimp(sp.expand(expression), method='fu'))
        assert reduced == 0, (name, reduced)
        checks.append({'name': name, 'passed': True})

    traceless = sp.trigsimp(components['aa']-components['bb']/sp.sin(polar)**2)
    exact('traceless_angular_equality_with_time_dependence', traceless.subs(radial, amplitude).doit())

    def project(expression, divisor):
        return sp.factor((expression.subs(radial, amplitude).doit()/divisor).subs(polar, sp.pi/4))

    projected = {name: project(expression, sp.diff(harmonic, polar) if name in ['ta', 'ra'] else harmonic) for name, expression in components.items() if name != 'bb'}
    projected['tr'] = sp.cancel(projected['tr']/(-sp.I*sigma))
    projected['ta'] = sp.cancel(projected['ta']/(-sp.I*sigma))
    projected['scalar'] = project(scalar_equation, harmonic)
    projected['phase'] = project(phase_equation, sp.I*sigma*harmonic)/field**2
    for name in ['ra', 'ta', 'tr', 'scalar', 'phase']:
        print(name, str(projected[name]), flush=True)
    rotation = frequency**2*sp.exp(-2*lapse)
    density = (metric*sp.diff(field, radius)**2+rotation*field**2)/2+potential
    pressure = density-2*potential
    metric_prime = (1-metric)/radius-2*alpha*radius*density
    lapse_prime = ((1-metric)/2+alpha*radius**2*pressure)/(radius*metric)
    scalar_prime2 = (sp.diff(potential, field)-rotation*field)/metric-(2/radius+lapse_prime+metric_prime/(2*metric))*sp.diff(field, radius)
    rules = {sp.diff(metric, radius): metric_prime, sp.diff(lapse, radius): lapse_prime, sp.diff(field, radius, 2): scalar_prime2}
    rules[sp.diff(lapse, radius, 2)] = sp.diff(lapse_prime, radius).subs(rules, simultaneous=True)

    def reduce_background(expression):
        return sp.factor(expression.subs(rules, simultaneous=True))

    angular_prime = sp.solve(projected['ra'], sp.diff(angular, radius))[0]
    shift_prime = sp.solve(projected['ta'], sp.diff(shift, radius))[0]
    amplitude_prime = sp.solve(projected['tr'].subs(sp.diff(angular, radius), angular_prime), sp.diff(amplitude, radius))[0]
    evolution = {sp.diff(angular, radius): angular_prime.subs(sp.diff(amplitude, radius), amplitude_prime),
                 sp.diff(shift, radius): shift_prime, sp.diff(amplitude, radius): amplitude_prime}
    evolution[sp.diff(response, radius, 2)] = sp.solve(projected['scalar'].subs(evolution, simultaneous=True), sp.diff(response, radius, 2))[0]
    evolution[sp.diff(phase, radius, 2)] = sp.solve(projected['phase'].subs(evolution, simultaneous=True), sp.diff(phase, radius, 2))[0]
    evolution = {key: reduce_background(value) for key, value in evolution.items()}
    second = {sp.diff(variable, radius, 2): sp.diff(evolution[sp.diff(variable, radius)], radius).subs(evolution, simultaneous=True) for variable in [angular, amplitude, shift]}
    residuals = {name: reduce_background(projected[name].subs(second, simultaneous=True).subs(evolution, simultaneous=True)) for name in ['tt', 'rr', 'aa']}
    constraint = sp.factor(residuals['rr'])
    for name, residual in residuals.items():
        factor = sp.factor(sp.diff(residual, angular)/sp.diff(constraint, angular))
        exact(name+'_residual_is_algebraic_constraint', residual-factor*constraint)
    constraint_solution = sp.factor(sp.solve(constraint, amplitude)[0])
    for name, residual in projected.items():
        if name in ['tr', 'ta', 'ra', 'scalar', 'phase']:
            exact(name+'_recovered_from_evolution', reduce_background(residual.subs(evolution, simultaneous=True)))
    flat_rules = {metric: 1, lapse: 0, amplitude: 0, angular: 0, shift: 0}
    flat_scalar = projected['scalar'].subs(flat_rules).doit()
    expected_scalar = sp.diff(response, radius, 2)+2*sp.diff(response, radius)/radius+(frequency**2+sigma**2-6/radius**2-sp.diff(potential, field, 2))*response+2*field*frequency*sigma**2*phase
    exact('flat_gyroscopic_amplitude', flat_scalar-expected_scalar)
    flat_phase = projected['phase'].subs(flat_rules).doit()
    expected_phase = sp.diff(phase, radius, 2)+(2/radius+2*sp.diff(field, radius)/field)*sp.diff(phase, radius)+(sigma**2-6/radius**2)*phase+2*frequency*response/field
    exact('flat_gyroscopic_phase', flat_phase-expected_phase)
    static_angular_prime = sp.diff(amplitude, radius)+2*sp.diff(lapse, radius)*amplitude-4*alpha*sp.diff(field, radius)*response
    exact('static_radial_angular_constraint', angular_prime.subs(sigma, 0)-static_angular_prime)
    static_scalar = projected['scalar'].subs(sigma, 0).subs(sp.diff(angular, radius), static_angular_prime)
    first = (1+metric-2*alpha*radius**2*potential)/(radius*metric)
    drive = sp.diff(potential, field)-2*rotation*field-2*metric*lapse_prime*sp.diff(field, radius)
    expected_static = metric*(sp.diff(response, radius, 2)+first*sp.diff(response, radius))-(6/radius**2+sp.diff(potential, field, 2)-rotation+4*alpha*metric*sp.diff(field, radius)**2)*response-drive*amplitude
    exact('static_scalar_recovers_parent', reduce_background(static_scalar-expected_static))
    print('evolution and limits checked', flush=True)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'exact_check_count': len(checks),
              'convention': 'exp(-i sigma t); dgtt=N^2 H Y; dgrr=H Y/F; dgtr=-i sigma J Y; dgab=r^2 K Y; dh=uY; dtheta=i sigma sY.',
              'projected_equations': {key: str(value) for key, value in projected.items()},
              'evolution': {str(key): str(value) for key, value in evolution.items()},
              'constraint': str(constraint), 'amplitude_constraint_solution': str(constraint_solution),
              'background_rules': {str(key): str(value) for key, value in rules.items()}}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}), flush=True)


if __name__ == '__main__':
    main()
