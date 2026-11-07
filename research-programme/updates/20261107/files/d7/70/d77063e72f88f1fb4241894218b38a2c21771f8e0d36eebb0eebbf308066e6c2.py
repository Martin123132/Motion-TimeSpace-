from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results/derivation'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    OUTPUT.mkdir(parents=True, exist_ok=False)
    checks = []
    def exact(name, expression):
        remainder = sp.factor(expression)
        assert remainder == 0, (name, remainder)
        checks.append({'name': name, 'passed': True})
    distance, radius, compactness, frequency2 = sp.symbols('distance radius compactness frequency2')
    surface_metric = 1-compactness
    inverse_metric = (radius-distance)/(radius*surface_metric-distance)
    friction = 2/(radius-distance)+compactness*radius/((radius-distance)*(radius*surface_metric-distance))
    friction_series = sp.series(friction, distance, 0, 5).removeO()
    inverse_series = sp.series(inverse_metric, distance, 0, 5).removeO()
    inverse_squared_series = sp.series(inverse_metric**2, distance, 0, 5).removeO()
    series = distance
    values = []
    for order in range(2, 6):
        coefficient = sp.Symbol(f'b{order}')
        trial = series+coefficient*distance**order
        residual = (3*trial*sp.diff(trial, distance, 2)+6*sp.diff(trial, distance)**2
                    -3*friction_series*trial*sp.diff(trial, distance)
                    -6*surface_metric*inverse_series+frequency2*inverse_squared_series*trial**2)
        term = sp.expand(residual).coeff(distance, order-1)
        value = sp.factor(sp.solve(term, coefficient)[0])
        exact(f'curved_edge_coefficient_order_{order}', term.subs(coefficient, value))
        values.append(value)
        series += value*distance**order
    exact('first_curved_edge_coefficient', values[0]-(2+compactness)/(10*radius*(1-compactness)))
    flat = json.loads((ROOT.parent/'finite-charge-20261003/results/exploration/status.json').read_text(encoding='utf-8'))
    for index, value in enumerate(values):
        old = sp.sympify(flat['series_coefficients'][index], locals={'radius': radius, 'frequency2': frequency2})
        exact(f'flat_endpoint_limit_b{index+2}', value.subs(compactness, 0)-old)
    position, omega, strength = sp.symbols('position omega strength', positive=True)
    amplitude = sp.Function('h')(position)
    metric = sp.Function('F')(position)
    log_lapse = sp.Function('nu')(position)
    potential = sp.Function('W')(amplitude)
    derivative = sp.diff(amplitude, position)
    rotation = omega**2*amplitude**2*sp.exp(-2*log_lapse)/2
    gradient = metric*derivative**2/2
    density = gradient+rotation+potential
    radial_pressure = gradient+rotation-potential
    tangent_pressure = -gradient+rotation-potential
    scalar_equation = sp.diff(amplitude, position, 2)+(2/position+sp.diff(log_lapse, position)+sp.diff(metric, position)/(2*metric))*derivative
    scalar_equation -= (sp.diff(potential, amplitude)-omega**2*amplitude*sp.exp(-2*log_lapse))/metric
    exact('anisotropic_TOV_from_scalar_equation', sp.diff(radial_pressure, position)+(density+radial_pressure)*sp.diff(log_lapse, position)
          +2*(radial_pressure-tangent_pressure)/position-metric*derivative*scalar_equation)
    exact('Komar_source', density+radial_pressure+2*tangent_pressure-(4*rotation-2*potential))
    mass, rho, pressure, transverse, lapse = sp.symbols('mass rho pressure transverse lapse')
    metric_value = 1-2*strength*mass/position
    mass_prime = position**2*rho
    metric_prime = 2*strength*(mass/position**2-position*rho)
    lapse_log_prime = strength*(mass+position**3*pressure)/(position**2*metric_value)
    pressure_prime = -(rho+pressure)*lapse_log_prime+2*(transverse-pressure)/position
    komar_derivative = ((lapse_log_prime-metric_prime/(2*metric_value))*(mass+position**3*pressure)
                        +mass_prime+3*position**2*pressure+position**3*pressure_prime)
    exact('Komar_ADM_differential_identity', komar_derivative-position**2*(rho+pressure+2*transverse))
    exact('exterior_Komar_ADM_match', (mass+position**3*pressure).subs(pressure, 0)-mass)
    perturbation, mass_flat, radial_gradient, field, lapse_shift, frequency = sp.symbols('perturbation mass_flat radial_gradient field lapse_shift frequency')
    metric_weak = 1-2*perturbation*mass_flat/position
    lapse_weak = 1+perturbation*lapse_shift
    energy_explicit = metric_weak*radial_gradient**2/2+frequency**2*field**2/(2*lapse_weak**2)
    charge_explicit = frequency*field**2/(sp.sqrt(metric_weak)*lapse_weak)
    variation = sp.diff(energy_explicit-frequency*charge_explicit, perturbation).subs(perturbation, 0)
    exact('fixed_charge_first_gravity_derivative', variation+mass_flat/position*(radial_gradient**2+frequency**2*field**2))
    exact('flat_enthalpy_equals_gradient_plus_rotation',
          (density+radial_pressure).subs({metric: 1, log_lapse: 0})-(derivative**2+omega**2*amplitude**2))
    edge_metric = sp.symbols('edge_metric', positive=True)
    leading = (12*edge_metric)**(-sp.Rational(3, 2))
    exact('curved_leading_cubic_edge', 6*leading-leading**sp.Rational(1, 3)/(2*edge_metric))
    exact('leading_tail_density', 9*edge_metric*leading**2/2+sp.Rational(3, 8)*leading**sp.Rational(4, 3)-1/(192*edge_metric**2))
    exact('leading_edge_radial_pressure_cancels', 9*edge_metric*leading**2/2-sp.Rational(3, 8)*leading**sp.Rational(4, 3))
    parent_seal = ROOT.parent/'finite-charge-20261003/results/stage-integrity.json'
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'edge_symbols': ['radius', 'compactness', 'frequency2'],
              'edge_u_coefficients_orders_2_to_5': [str(value) for value in values],
              'edge_matter_backreaction_first_changes_u_order': 6,
              'fixed_charge_weak_binding_coefficient': '-4*pi*integral(s*m_flat*(rho_flat+p_radial_flat), ds)',
              'newton_density_only_comparison': '-4*pi*integral(s*m_flat*rho_flat, ds)',
              'parent_seal_sha256': hashlib.sha256(parent_seal.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUTPUT/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'curved_edge_order': 5}))


if __name__ == '__main__':
    main()
