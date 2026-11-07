import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path
import sympy as symbolic
import psutil
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([int(os.environ.get('MTS_CPU', '2'))])
coordinate = symbolic.symbols('u', real=True)
step = symbolic.symbols('epsilon', nonzero=True, real=True)
varying = lambda name: symbolic.Function(name)(coordinate)
basis = symbolic.Matrix([[varying('V11'), varying('V12')], [varying('V21'), varying('V22')]])
coefficient = symbolic.Matrix([varying('B1'), varying('B2')])
hessian = symbolic.Matrix([[varying('H11'), varying('H12')], [varying('H12'), varying('H22')]])
field = basis * coefficient
quadratic = lambda vector: (vector.T * hessian * vector)[0] / 2
source = quadratic(field)
history_term = (field.T * hessian * basis * coefficient.diff(coordinate))[0]
basis_term = (field.T * hessian * basis.diff(coordinate) * coefficient)[0]
operator_term = (field.T * hessian.diff(coordinate) * field)[0] / 2
tangent = symbolic.Matrix(symbolic.symbols('tangent1 tangent2'))
central = (quadratic(field + step * tangent) - quadratic(field - step * tangent)) / (2 * step)
wave = symbolic.Matrix([varying('wave1'), varying('wave2')])
wave_source = (field.T * hessian * wave)[0]
wave_rule = (field.diff(coordinate).T * hessian * wave + field.T * hessian.diff(coordinate) * wave
    + field.T * hessian * wave.diff(coordinate))[0]
checks = {
    'quadratic_chain_rule_including_moving_basis': symbolic.simplify(source.diff(coordinate) - history_term - basis_term - operator_term) == 0,
    'frozen_quadratic_central_directional_derivative': symbolic.expand(central - (field.T * hessian * tangent)[0]) == 0,
    'mixed_wave_history_operator_chain_rule': symbolic.simplify(wave_source.diff(coordinate) - wave_rule) == 0,
    'omitted_basis_term_is_not_identically_zero': symbolic.simplify(basis_term) != 0,
    'constant_basis_recovers_fixed_basis_rule': symbolic.simplify((source.diff(coordinate) - history_term - operator_term).subs(
        {entry.diff(coordinate): 0 for entry in basis})) == 0,
}
assert all(checks.values()), checks
result = dict(checks=checks, passed=len(checks), scope='Exact chain-rule checks for an arbitrary symmetric bilinear source and moving basis; no new existence theorem')
print(json.dumps(result), flush=True)
destination = Path(__file__).resolve().parent / 'results/algebra.json'
assert not destination.exists()
destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
