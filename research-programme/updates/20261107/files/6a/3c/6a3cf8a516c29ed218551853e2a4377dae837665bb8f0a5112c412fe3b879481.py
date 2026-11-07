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
    output = ROOT/'results/reduction'
    output.mkdir(parents=True, exist_ok=False)
    data = json.loads((ROOT/'results/derivation-v3/status.json').read_text())
    radius, alpha, frequency, sigma = sp.symbols('radius alpha frequency sigma', real=True)
    names = ['metric', 'lapse', 'field', 'amplitude', 'radial', 'angular', 'shift', 'response', 'phase', 'potential']
    environment = {name: sp.Function(name) for name in names}
    environment.update({str(value): value for value in [radius, alpha, frequency, sigma]})
    metric, lapse, field, amplitude, angular, shift, response, phase = [environment[name](radius) for name in ['metric', 'lapse', 'field', 'amplitude', 'angular', 'shift', 'response', 'phase']]
    potential = environment['potential'](field)
    parse = lambda value: sp.sympify(value, locals=environment)
    equations = {parse(key): parse(value) for key, value in data['evolution'].items()}
    background = {parse(key): parse(value) for key, value in data['background_rules'].items()}
    amplitude_solution = parse(data['amplitude_constraint_solution'])
    checks = []

    def exact(name, expression):
        assert sp.factor(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    first = (1+metric-2*alpha*radius**2*potential)/(radius*metric)
    rotation = frequency**2*sp.exp(-2*lapse)
    lapse_prime = background[sp.diff(lapse, radius)]
    drive = sp.diff(potential, field)-2*rotation*field-2*metric*lapse_prime*sp.diff(field, radius)
    angular_prime = (lapse_prime-1/radius)*angular+amplitude/radius+(3/radius**2-2*alpha*rotation*field**2)*shift+2*alpha*frequency*field**2*sp.diff(phase, radius)-2*alpha*sp.diff(field, radius)*response
    shift_prime = (amplitude+angular-4*alpha*frequency*field**2*phase)/metric-(first-2/radius)*shift
    response_prime2 = -first*sp.diff(response, radius)+(6/radius**2+sp.diff(potential, field, 2)-rotation+4*alpha*metric*sp.diff(field, radius)**2-sigma**2*sp.exp(-2*lapse))*response/metric+drive*amplitude/metric-2*frequency*field*sigma**2*sp.exp(-2*lapse)*phase/metric
    phase_prime2 = -(first+2*sp.diff(field, radius)/field)*sp.diff(phase, radius)+(6/radius**2-(sigma**2+4*alpha*frequency**2*field**2)*sp.exp(-2*lapse))*phase/metric-2*frequency*sp.exp(-2*lapse)*response/(metric*field)+2*frequency*sp.exp(-2*lapse)*(1/radius-lapse_prime+sp.diff(field, radius)/field)*shift
    for name, variable, proposed in [('angular', angular, angular_prime), ('shift', shift, shift_prime), ('amplitude_scalar', response, response_prime2), ('phase_scalar', phase, phase_prime2)]:
        order = 1 if name in ['angular', 'shift'] else 2
        exact('compact_'+name, equations[sp.diff(variable, radius, order)]-proposed)
    preservation = sp.diff(amplitude_solution, radius).subs(equations, simultaneous=True).subs(background, simultaneous=True)-equations[sp.diff(amplitude, radius)]
    preservation = preservation.subs(amplitude, amplitude_solution)
    exact('algebraic_constraint_preserved_by_six_equation_flow', preservation)
    print('constraint preservation checked', flush=True)
    flat_static = {sigma: 0, alpha: 0, metric: 1, lapse: 0}
    exact('vacuum_flat_static_H_equals_K', amplitude_solution.subs(flat_static)-angular)
    geometric_mass = sp.Symbol('geometric_mass', real=True)
    vacuum_metric = 1-2*geometric_mass/radius
    vacuum = {field: 0, sp.diff(field, radius): 0, potential: 0, sp.diff(potential, field): 0,
              response: 0, sp.diff(response, radius): 0, phase: 0, sp.diff(phase, radius): 0,
              metric: vacuum_metric, lapse: sp.log(vacuum_metric)/2}
    vacuum_H = sp.factor(amplitude_solution.subs(vacuum, simultaneous=True))
    master = sp.Function('master')(radius)
    master_prime = sp.diff(master, radius)
    vacuum_potential = vacuum_metric*(24*radius**3+24*geometric_mass*radius**2+36*geometric_mass**2*radius+18*geometric_mass**3)/(radius**3*(2*radius+3*geometric_mass)**2)
    vacuum_K = (6*radius**2+6*geometric_mass*radius+6*geometric_mass**2)/(radius**2*(2*radius+3*geometric_mass))*master+vacuum_metric*master_prime
    vacuum_J = (2*radius**2-6*geometric_mass*radius-3*geometric_mass**2)/((radius-2*geometric_mass)*(2*radius+3*geometric_mass))*master+radius*master_prime
    master_rule = {sp.diff(master, radius, 2): -(sp.diff(vacuum_metric, radius)*master_prime/vacuum_metric)+(vacuum_potential-sigma**2)*master/vacuum_metric**2}
    vacuum_H_master = vacuum_H.subs({angular: vacuum_K, shift: vacuum_J})
    for variable, proposed, name in [(angular, vacuum_K, 'angular'), (shift, vacuum_J, 'shift')]:
        expected = equations[sp.diff(variable, radius)].subs(vacuum, simultaneous=True).subs({amplitude: vacuum_H_master, angular: vacuum_K, shift: vacuum_J})
        exact('vacuum_Zerilli_'+name, sp.diff(proposed, radius).subs(master_rule)-expected)
    expected = equations[sp.diff(amplitude, radius)].subs(vacuum, simultaneous=True).subs({amplitude: vacuum_H_master, angular: vacuum_K, shift: vacuum_J})
    exact('vacuum_Zerilli_time_metric', sp.diff(vacuum_H_master, radius).subs(master_rule)-expected)
    static_coefficient = (-4*alpha*radius**2*potential-6-(1-metric+2*alpha*radius**2*((metric*sp.diff(field, radius)**2+rotation*field**2)/2-potential))**2/metric+8*alpha*radius**2*rotation*field**2)/(radius**2*metric)
    static_prime2 = -first*sp.diff(amplitude, radius)-static_coefficient*amplitude+4*alpha*drive*response/metric
    static_tt = parse(data['projected_equations']['tt']).subs(sigma, 0)
    static_angular = sp.diff(amplitude, radius)+2*sp.diff(lapse, radius)*amplitude-4*alpha*sp.diff(field, radius)*response
    exact('static_time_metric_recovers_parent', static_tt.subs({sp.diff(angular, radius): static_angular, sp.diff(amplitude, radius, 2): static_prime2}, simultaneous=True).subs(background, simultaneous=True))
    scalar_names = 'r F N2 h hp W Wp Wpp a w z'.split()
    scalar_values = sp.symbols(' '.join(scalar_names), real=True)
    substitutions = dict(zip([radius, metric, sp.exp(2*lapse), field, sp.diff(field, radius), potential, sp.diff(potential, field), sp.diff(potential, field, 2), alpha, frequency, sigma**2], scalar_values))
    state = [angular, shift, response, sp.diff(response, radius), phase, sp.diff(phase, radius)]
    coefficients = [sp.factor(sp.diff(amplitude_solution, variable).subs(substitutions, simultaneous=True)) for variable in state]
    denominators = [str(sp.factor(sp.denom(value))) for value in coefficients]
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'exact_check_count': len(checks), 'coefficient_symbols': scalar_names,
              'state_order': ['K', 'J', 'u', 'uprime', 's', 'sprime'],
              'H_coefficients': [str(value) for value in coefficients], 'H_denominators': denominators,
              'vacuum_H': str(vacuum_H), 'vacuum_potential': str(vacuum_potential),
              'compact_evolution': {'Kprime': str(angular_prime), 'Jprime': str(shift_prime), 'uprime2': str(response_prime2), 'sprime2': str(phase_prime2)},
              'vacuum_K': str(vacuum_K), 'vacuum_J': str(vacuum_J),
              'parent_derivation_sha256': hashlib.sha256((ROOT/'results/derivation-v3/status.json').read_bytes()).hexdigest()}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}), flush=True)


if __name__ == '__main__':
    main()
