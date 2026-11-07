from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent


def configure_worker():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def write_new_json(path, report):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)


def zero_check(checks, name, expression):
    residual = sp.factor(sp.trigsimp(sp.expand(expression)))
    checks.append({'name': name, 'residual': str(residual), 'passed': residual == 0})
    assert residual == 0, (name, residual)


def stf(matrix):
    symmetric = (matrix+matrix.T)/2
    return symmetric-sp.eye(3)*sp.trace(symmetric)/3


def contraction(first, second):
    return sum(first[row, column]*second[row, column]
               for row in range(3) for column in range(3))
