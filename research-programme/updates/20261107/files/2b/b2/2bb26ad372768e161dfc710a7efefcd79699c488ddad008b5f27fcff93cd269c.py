from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import psutil

from sequence_tools_v3 import SequenceBody, load_solution


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    path = ROOT/'results/critical-remapped/status.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    source = path.parent/report['attempts'][-1]['archive']
    solution = load_solution(source)
    body = SequenceBody(report['arguments']['floor'], report['arguments']['tol'])
    body.target_central = 2.
    body.charge_scale = solution.charge_scale
    knots = solution.sol.x
    coordinate = (knots[:-1, None]+np.diff(knots)[:, None]*np.array([.211324865405187, .788675134594813])).ravel()
    fields = solution.sol(coordinate)
    right = body.equation(coordinate, fields, solution.p)
    normalized = abs(solution.sol(coordinate, 1)-right)/(1+abs(right))
    maximum = np.max(normalized, axis=0)
    largest = np.argsort(maximum)[-12:]
    result = {'state': 'complete', 'source': str(source), 'knots': len(knots),
              'parameters': solution.p.tolist(), 'minimum_amplitude': float(np.min(fields[0])),
              'boundary_residuals': body.boundary(solution.sol(knots[0]), solution.sol(1.), solution.p).tolist(),
              'component_maximum_residuals': np.max(normalized, axis=1).tolist(),
              'worst': [{'coordinate': float(coordinate[index]), 'amplitude': float(fields[0, index]),
                         'residual': float(maximum[index]), 'component': int(np.argmax(normalized[:, index]))} for index in largest]}
    output = ROOT/'results/bvp-diagnostic.json'
    assert not output.exists()
    output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
