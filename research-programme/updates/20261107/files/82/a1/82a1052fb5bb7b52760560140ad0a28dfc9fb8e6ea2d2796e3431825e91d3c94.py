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
    parameter = sp.Symbol('parameter')
    field_one, field_two = sp.symbols('field_one field_two')
    coordinates = [field_one, field_two]
    path = [sp.Function('first')(parameter), sp.Function('second')(parameter)]
    frequency = sp.Function('frequency')(parameter)
    energy = sp.Function('energy')(field_one, field_two)
    charge = sp.Function('charge')(field_one, field_two)
    substitution = dict(zip(coordinates, path))
    tangent = sp.Matrix([sp.diff(value, parameter) for value in path])
    gradient_charge = sp.Matrix([sp.diff(charge, value).subs(substitution) for value in coordinates])
    residual = sp.Matrix([(sp.diff(energy, value)-frequency*sp.diff(charge, value)).subs(substitution) for value in coordinates])
    hessian = sp.hessian(energy-frequency*charge, coordinates).subs(substitution)
    checks = []

    def exact(name, expression):
        entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
        assert all(sp.simplify(entry.doit()) == 0 for entry in entries), name
        checks.append({'name': name, 'passed': True})

    exact('first_law_remainder_is_stationarity_residual', sp.diff(energy.subs(substitution), parameter)
          -frequency*sp.diff(charge.subs(substitution), parameter)-(residual.T*tangent)[0])
    exact('differentiated_stationarity', residual.diff(parameter)-hessian*tangent+sp.diff(frequency, parameter)*gradient_charge)
    exact('charge_tangent_chain_rule', sp.diff(charge.subs(substitution), parameter)-(gradient_charge.T*tangent)[0])
    curvature_difference = sp.diff(energy.subs(substitution), parameter, 2)-frequency*sp.diff(charge.subs(substitution), parameter, 2)
    exact('second_first_law_remainder', curvature_difference-sp.diff(frequency, parameter)*sp.diff(charge.subs(substitution), parameter)
          -sp.diff((residual.T*tangent)[0], parameter))
    distance, edge_metric, edge_radius = sp.symbols('distance edge_metric edge_radius', positive=True)
    edge_field = distance**3/(12*edge_metric)**sp.Rational(3, 2)
    edge_tangent = sp.diff(edge_field, distance)
    amplitude_weight = edge_field**sp.Rational(-2, 3)/6
    exact('moving_edge_tangent_has_finite_potential_form', amplitude_weight*edge_tangent**2-distance**2/(96*edge_metric**2))
    report = {'state': 'complete', 'checks': checks, 'exact_check_count': len(checks),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'conditional_statement': 'On a differentiable stationary fixed-action family with admissible nonzero tangent, Qprime=0 makes its tangent a constrained Hessian null direction. It does not by itself count growing modes.',
              'fixed_alpha_required': True, 'compact_edge_domain_argument_in_derivation_document': True}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks)}))


if __name__ == '__main__':
    main()
