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
    output = ROOT/'results/edge-weak'
    output.mkdir(exist_ok=False)
    distance, radius, compactness, frequency2, amplitude, tide, tide_prime = sp.symbols('distance radius compactness frequency2 amplitude tide tide_prime', real=True)
    parent_path = ROOT.parent/'self-gravity-20261003/results/derivation/status.json'
    parent = json.loads(parent_path.read_text(encoding='utf-8'))
    symbols = sp.symbols(' '.join(parent['edge_symbols']))
    replacements = {symbol: {'radius': radius, 'compactness': compactness, 'frequency2': frequency2}[str(symbol)] for symbol in symbols}
    coefficients = [sp.sympify(value, locals=dict(zip(parent['edge_symbols'], symbols))).subs(replacements)
                    for value in parent['edge_u_coefficients_orders_2_to_5']]
    edge_coordinate = distance+sum(value*distance**order for order, value in enumerate(coefficients[:3], 2))
    position = radius-distance
    metric = 1-compactness*radius/position
    surface = 1-compactness
    constant = (12*surface)**(-sp.Rational(3, 2))
    first = (1+metric)/(position*metric)
    metric_coefficient = -6/(position**2*metric)-(1-metric)**2/(position**2*metric**2)
    tide_second = (-first*tide_prime-metric_coefficient*tide).subs(distance, 0)
    tide_series = tide-tide_prime*distance+tide_second*distance**2/2
    radial_metric_prime = compactness*radius/position**2
    background_prime = -3*constant*edge_coordinate**2*sp.diff(edge_coordinate, distance)
    drive = edge_coordinate/(2*sp.sqrt(12*surface))-2*frequency2*constant*edge_coordinate**3/metric-radial_metric_prime*background_prime
    singular = sp.series(2*surface/(metric*(edge_coordinate/distance)**2), distance, 0, 4).removeO()/distance**2
    regular = sp.series(6/(position**2*metric)-frequency2/metric**2, distance, 0, 2).removeO()
    first_series = sp.series(first, distance, 0, 3).removeO()
    force_series = sp.series(drive*tide_series/metric, distance, 0, 4).removeO()
    unknowns = sp.symbols('cubic quartic quintic')
    response = amplitude*distance**2+sum(value*distance**order for order, value in enumerate(unknowns, 3))
    residual = sp.expand(sp.diff(response, distance, 2)-first_series*sp.diff(response, distance)-(singular+regular)*response-force_series)
    solved = {}
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    for power, unknown in zip([1, 2, 3], unknowns):
        equation = residual.coeff(distance, power).subs(solved)
        solved[unknown] = sp.factor(sp.solve(equation, unknown)[0])
        exact(f'edge_order_{power}', equation.subs(unknown, solved[unknown]))
    flat_path = ROOT.parent/'quadrupole-response-20261004/results/derivation/status.json'
    flat = json.loads(flat_path.read_text(encoding='utf-8'))
    flat_symbols = sp.symbols(' '.join(flat['response_edge_symbols']), positive=True)
    flat_rules = dict(zip(flat_symbols, [radius, frequency2, amplitude]))
    for order, unknown in enumerate(unknowns, 3):
        expected = sp.sympify(flat['response_edge_coefficients_orders_3_to_5'][order-3], locals=dict(zip(flat['response_edge_symbols'], flat_symbols))).subs(flat_rules)
        exact(f'flat_edge_order_{order}', solved[unknown].subs({compactness: 0, tide: -2*radius**2, tide_prime: -4*radius})-expected)
    coordinate = sp.symbols('coordinate', positive=True)
    mass = sp.Function('mass')(coordinate)
    density = sp.Function('density')(coordinate)
    field = sp.Function('field')(coordinate)
    potential = sp.Function('potential')(coordinate)
    response_function = sp.Function('response')(coordinate)
    drive_function = sp.Function('drive')(coordinate)
    first_correction = 2*mass/coordinate**2-2*coordinate*potential
    metric_correction = -12*mass/coordinate**3-4*potential+8*frequency2*field**2
    source = 4*coordinate*first_correction+2*coordinate**2*metric_correction+4*drive_function*response_function
    metric_reference = 4*coordinate*mass
    laplace_reference = sp.diff(metric_reference, coordinate, 2)+2*sp.diff(metric_reference, coordinate)/coordinate-6*metric_reference/coordinate**2
    laplace_reference = laplace_reference.subs({sp.diff(mass, coordinate, 2): 2*coordinate*density+coordinate**2*sp.diff(density, coordinate), sp.diff(mass, coordinate): coordinate**2*density})
    compact_source = 16*coordinate**2*(frequency2*field**2-potential)-24*coordinate**2*density-4*coordinate**3*sp.diff(density, coordinate)+4*drive_function*response_function
    exact('weak_gravity_compact_metric_source', source-laplace_reference-compact_source)
    weighted_integrand = coordinate**4*compact_source+sp.diff(4*coordinate**7*density, coordinate)
    expected_integrand = coordinate**6*(16*frequency2*field**2-16*potential+4*density)+4*coordinate**4*drive_function*response_function
    exact('weak_response_integration_by_parts', weighted_integrand-expected_integrand)
    exact('weak_direct_term_after_density_substitution', expected_integrand.subs(density, (sp.diff(field, coordinate)**2+frequency2*field**2)/2+potential)
          -(coordinate**6*(18*frequency2*field**2+2*sp.diff(field, coordinate)**2-12*potential)+4*coordinate**4*drive_function*response_function))
    geometric_mass = sp.symbols('geometric_mass', positive=True)
    vacuum_metric = 1-2*geometric_mass/coordinate
    growing = coordinate**2*vacuum_metric
    vacuum_first = (1+vacuum_metric)/(coordinate*vacuum_metric)
    vacuum_second = -6/(coordinate**2*vacuum_metric)-(1-vacuum_metric)**2/(coordinate**2*vacuum_metric**2)
    exact('exact_schwarzschild_growing_mode', sp.diff(growing, coordinate, 2)+vacuum_first*sp.diff(growing, coordinate)+vacuum_second*growing)
    exact('exterior_wronskian_transport', sp.diff(-5/growing, coordinate)+vacuum_first*(-5/growing))
    result = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'source_hashes': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [parent_path, flat_path]},
              'checks': checks, 'exact_check_count': len(checks),
              'edge_symbols': ['radius', 'compactness', 'frequency2', 'amplitude', 'tide', 'tide_prime'],
              'edge_coefficients_orders_3_to_5': [str(solved[value]) for value in unknowns],
              'weak_geometric_lambda_over_alpha': '(2*chi_relax + integral r^6*(18*w^2*h^2+2*hp^2-12*W)dr)/30',
              'convention': 'Growing exterior H coefficient -2; decaying coefficient B; geometric lambda=-B/6; self coupling alpha=4pi G_R v_star^2.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'cubic': str(solved[unknowns[0]])}))


if __name__ == '__main__':
    main()
