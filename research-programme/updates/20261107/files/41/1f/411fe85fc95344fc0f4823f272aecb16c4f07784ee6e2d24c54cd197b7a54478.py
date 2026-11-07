import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[variable] = '1'
import ast
import hashlib
import io
import json
import math
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import psutil
import numpy as np

sys.dont_write_bytecode = True
process = psutil.Process()
process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
process.cpu_affinity([4])
root = Path(__file__).resolve().parent
source = root / 'final_epoch_real_source.py'
namespace = dict(np=np)
names = {'accumulate', 'resolved', 'checks_for'}
statements = [statement for statement in ast.parse(source.read_text()).body
              if isinstance(statement, ast.FunctionDef) and statement.name in names]
assert {statement.name for statement in statements} == names
exec(compile(ast.Module(body=statements, type_ignores=[]), str(source), 'exec'), namespace)
checks = []
sequences = [
    [np.array([1e16, -1e16, 1e-30]), np.ones(3), np.array([-1e16, 1e16, -1e-30])],
    [np.array([2.0**exponent, -2.0**exponent, 1e-70]) for exponent in range(-50, 51, 5)],
]
generator = np.random.default_rng(244)
sequences.append([generator.normal(size=32) * 10.0**generator.integers(-12, 13) for index in range(42)])
for case, values in enumerate(sequences):
    totals, corrections = {}, {}
    for value in values:
        namespace['accumulate'](totals, corrections, {'test': value})
    high, low = namespace['resolved'](totals, corrections)
    expected = [math.fsum(column) for column in zip(*values)]
    checks.append(dict(name=f'case{case}:correctly-rounded-sum', passed=np.array_equal(high['test'], expected)))
    for column, target in enumerate(zip(*values)):
        exact = sum((Fraction.from_float(float(value)) for value in target), Fraction())
        reconstructed = Fraction.from_float(float(high['test'][column])) + Fraction.from_float(float(low['test'][column]))
        relative = float(abs(reconstructed - exact) / max(abs(exact), Fraction(1, 10**300)))
        checks.append(dict(name=f'case{case}:lane{column}:split-sum', passed=relative <= 1e-14, relative=relative))
    first, second = {}, {}
    midpoint = len(values) // 2
    for value in values[:midpoint]:
        namespace['accumulate'](first, second, {'test': value})
    buffer = io.BytesIO()
    np.savez_compressed(buffer, total=first['test'], correction=second['test'])
    buffer.seek(0)
    with np.load(buffer, allow_pickle=False) as saved:
        first, second = {'test': saved['total'].copy()}, {'test': saved['correction'].copy()}
    for value in values[midpoint:]:
        namespace['accumulate'](first, second, {'test': value})
    checks.append(dict(name=f'case{case}:serialized-resume-exact',
                       passed=np.array_equal(first['test'], totals['test']) and np.array_equal(second['test'], corrections['test'])))
actions = np.zeros((19, 98, 18))
actions[:, 0, :] = generator.normal(size=(19, 18))
actions[:, -1, :] = -actions[:, 0, :]
checks.append(dict(name='all342-exchange-entries', passed=all(row['passed'] and row['entries'] == 342
                   for row in namespace['checks_for']({'control:join0:l0:actions': actions}))))
actions[17, -1, 16] += .01
checks.append(dict(name='isolated-exchange-defect-rejected', passed=not all(row['passed']
                   for row in namespace['checks_for']({'control:join0:l0:actions': actions}))))
actions[0, 1, 0] = np.nan
try:
    namespace['checks_for']({'control:join0:l0:actions': actions})
except FloatingPointError:
    checks.append(dict(name='nonfinite-rejected', passed=True))
else:
    checks.append(dict(name='nonfinite-rejected', passed=False))
record = dict(passed=all(row['passed'] for row in checks), checks=checks, finished_at=datetime.now(timezone.utc).isoformat(),
              process=dict(pid=process.pid, created_time=process.create_time(), command=process.cmdline()),
              inputs={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in (source, Path(__file__))},
              physical_evolution=False, source_integrated=False)
with (root / 'final-source-sum-controls.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2, allow_nan=False)
print(json.dumps(dict(passed=record['passed'], checks=len(checks), failed=[row for row in checks if not row['passed']])))
raise SystemExit(0 if record['passed'] else 1)
