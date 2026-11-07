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
    output = ROOT/'results/compact-constraint'
    output.mkdir(exist_ok=False)
    data = json.loads((ROOT/'results/derivation-v3/status.json').read_text())
    radius, alpha, frequency, sigma = sp.symbols('radius alpha frequency sigma', real=True)
    environment = {name: sp.Function(name) for name in ['metric', 'lapse', 'field', 'amplitude', 'radial', 'angular', 'shift', 'response', 'phase', 'potential']}
    environment.update({str(value): value for value in [radius, alpha, frequency, sigma]})
    metric, lapse, field, amplitude, angular, shift, response, phase = [environment[name](radius) for name in ['metric', 'lapse', 'field', 'amplitude', 'angular', 'shift', 'response', 'phase']]
    potential = environment['potential'](field)
    parse = lambda value: sp.sympify(value, locals=environment)
    projected = {name: parse(value) for name, value in data['projected_equations'].items()}
    background = {parse(key): parse(value) for key, value in data['background_rules'].items()}
    evolution = {parse(key): parse(value) for key, value in data['evolution'].items()}
    angular_prime = sp.solve(projected['ra'], sp.diff(angular, radius))[0]
    replacements = {sp.diff(angular, radius, 2): sp.diff(angular_prime, radius), sp.diff(angular, radius): angular_prime}
    time_equation = projected['tt'].subs(replacements, simultaneous=True)
    time_second = sp.solve(time_equation, sp.diff(amplitude, radius, 2))[0]
    constraint = projected['aa'].subs(replacements, simultaneous=True).subs(sp.diff(amplitude, radius, 2), time_second)
    constraint = constraint.subs(sp.diff(shift, radius), evolution[sp.diff(shift, radius)]).subs(background, simultaneous=True)
    constraint = sp.factor(constraint)
    factor = sp.factor(sp.diff(constraint, angular).subs(sigma, 0))
    constraint = sp.factor(constraint/factor)
    static = sp.factor(constraint.subs(sigma, 0))
    correction = sp.factor((constraint-static)/sigma**2)
    static_parent_path = ROOT.parent/'gravitating-tides-20261004/results/derivation/status.json'
    parent = json.loads(static_parent_path.read_text())
    parent_environment = dict(environment)
    parent_environment.update({'alpha': sp.Symbol('alpha', positive=True), 'frequency': sp.Symbol('frequency', positive=True)})
    static_angular = sp.sympify(parent['expressions']['angular_constraint'], locals=parent_environment).subs({parent_environment['alpha']: alpha, parent_environment['frequency']: frequency})
    assert sp.factor(static-angular+static_angular) == 0
    lapse_prime = sp.Symbol('lapse_prime')
    short_correction = sp.factor(correction.subs(potential, (metric*lapse_prime/radius-(1-metric)/(2*radius**2))/(-alpha)+(metric*sp.diff(field, radius)**2+frequency**2*sp.exp(-2*lapse)*field**2)/2))
    print('dynamic correction', short_correction, flush=True)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'static_constraint': str(static), 'dynamic_coefficient_of_sigma_squared': str(correction),
              'compact_dynamic_coefficient': str(short_correction), 'identity': '0 = K - K_static(H,Hprime,u,uprime) + sigma^2 * correction',
              'checks': [{'name': 'full_dynamic_angular_constraint_static_part_equals_previous_K_constraint', 'passed': True}],
              'source_paths': [str(ROOT/'results/derivation-v3/status.json'), str(static_parent_path)]}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
