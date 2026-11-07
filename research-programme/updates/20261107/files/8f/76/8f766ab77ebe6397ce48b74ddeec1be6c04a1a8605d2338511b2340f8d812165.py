from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    radius = sp.symbols('radius', positive=True)
    frequency, harmonic = sp.symbols('frequency harmonic', real=True)
    field = sp.Function('field')(radius)
    force = sp.Function('force')
    background = sp.diff(field, radius, 2)+2*sp.diff(field, radius)/radius-force(field)+frequency**2*field
    translation = -sp.diff(field, radius, 3)-2*sp.diff(field, radius, 2)/radius+(2/radius**2+sp.diff(force(field), field)-frequency**2)*sp.diff(field, radius)
    checks = []

    def exact(name, expression):
        assert sp.simplify(expression) == 0, name
        checks.append({'name': name, 'passed': True})

    exact('translation_operator_identity', translation+sp.diff(background, radius))
    phase_zero = -sp.diff(field, radius, 2)-2*sp.diff(field, radius)/radius+(force(field)/field-frequency**2)*field
    exact('phase_ground_state_identity', phase_zero+background)
    ground = sp.Function('ground')(radius)
    ratio = sp.Function('ratio')(radius)
    amplitude = ground*ratio
    ground_potential = (sp.diff(ground, radius, 2)+2*sp.diff(ground, radius)/radius)/ground
    integrand = radius**2*(sp.diff(amplitude, radius)**2+ground_potential*amplitude**2)
    boundary = radius**2*ground*sp.diff(ground, radius)*ratio**2
    exact('weighted_ground_state_square', integrand-radius**2*ground**2*sp.diff(ratio, radius)**2-sp.diff(boundary, radius))
    exact('angular_lift_from_translation', harmonic*(harmonic+1)-2-(harmonic-1)*(harmonic+2))

    potential, gradient_squared, rotation_squared, perturbation = sp.symbols('potential gradient_squared rotation_squared perturbation')
    lapse = 1+perturbation
    spatial_scale = 1-2*perturbation
    grand_density = lapse*spatial_scale**sp.Rational(3, 2)*(gradient_squared/(2*spatial_scale)+potential-rotation_squared/(2*lapse**2))
    exact('weak_metric_grand_potential_source', sp.diff(grand_density, perturbation).subs(perturbation, 0)-(2*rotation_squared-2*potential))
    amplitude_symbol = sp.symbols('amplitude', positive=True)
    potential_function = sp.Function('potential_function')(amplitude_symbol)
    exact('quadrupole_source_from_variation', -sp.diff(2*frequency**2*amplitude_symbol**2-2*potential_function, amplitude_symbol)
          -2*(sp.diff(potential_function, amplitude_symbol)-2*frequency**2*amplitude_symbol))
    lower_amplitude, lower_phase, squared = sp.symbols('lower_amplitude lower_phase squared', positive=True)
    threshold = lower_amplitude+lower_phase+4*frequency**2
    exact('gyro_gap_polynomial', (lower_amplitude-squared)*(lower_phase-squared)-4*frequency**2*squared
          -(squared**2-threshold*squared+lower_amplitude*lower_phase))

    distance, support, frequency2, edge_amplitude = sp.symbols('distance support frequency2 edge_amplitude', positive=True)
    parent_path = BRANCH/'self-gravity-20261003/results/derivation/status.json'
    parent = json.loads(parent_path.read_text(encoding='utf-8'))
    symbols = sp.symbols(' '.join(parent['edge_symbols']))
    replacements = {symbol: {'radius': support, 'compactness': 0, 'frequency2': frequency2}[str(symbol)] for symbol in symbols}
    coefficients = [sp.sympify(value, locals=dict(zip(parent['edge_symbols'], symbols))).subs(replacements)
                    for value in parent['edge_u_coefficients_orders_2_to_5']]
    background_edge = distance+sum(value*distance**order for order, value in enumerate(coefficients, 2))
    constant = sp.Rational(1, 12)**sp.Rational(3, 2)
    unknown = sp.symbols('edge_three edge_four edge_five')
    response = edge_amplitude*distance**2+sum(value*distance**order for order, value in enumerate(unknown, 3))
    stiffness = 2/background_edge**2+sp.Rational(3, 2)*constant**2*background_edge**6-frequency2+6/(support-distance)**2
    source = (support-distance)**2*(constant**sp.Rational(1, 3)*background_edge+constant**3*background_edge**9-4*frequency2*constant*background_edge**3)
    residual = -sp.diff(response, distance, 2)+2*sp.diff(response, distance)/(support-distance)+stiffness*response-source
    series = sp.series(residual, distance, 0, 4).removeO().expand()
    solution = sp.solve([series.coeff(distance, order) for order in [1, 2, 3]], unknown, dict=True)[0]
    exact('forced_edge_coefficients', sum(sp.simplify(series.coeff(distance, order).subs(solution)) for order in [1, 2, 3]))
    exact('forced_cubic_edge_term_is_metric_response', solution[unknown[0]]-4*edge_amplitude/(5*support)+3*constant*support**2)
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'edge_parent_path': str(parent_path), 'edge_parent_sha256': hashlib.sha256(parent_path.read_bytes()).hexdigest(),
              'checks': checks, 'exact_check_count': len(checks),
              'response_edge_symbols': ['support', 'frequency2', 'edge_amplitude'],
              'response_edge_coefficients_orders_3_to_5': [str(solution[value]) for value in unknown],
              'scope': 'Flat monotone compact background; external static weak-metric drive; no induced metric self-gravity included.',
              'static_amplitude_lower_bound': '(ell-1)*(ell+2)/R^2 for ell>=2',
              'static_phase_lower_bound': 'ell*(ell+1)/R^2 for ell>=1'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'edge_cubic': str(solution[unknown[0]])}))


if __name__ == '__main__':
    main()
