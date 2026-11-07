from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_joint_flow_derivative_20260922 import JointMetricTangent, symbolic_checks
from decimal import Decimal, localcontext
import numpy as np


class DecimalSparseResidual:
    def __init__(self, matrix):
        self.matrix = matrix.tocsr()
        self.entries = [Decimal.from_float(float(value)) for value in self.matrix.data]

    def evaluate(self, direction, coupling, rhs):
        shape = rhs.shape
        vector = [Decimal.from_float(float(value)) for value in np.asarray(direction).ravel()]
        coupled = [Decimal.from_float(float(value)) for value in np.asarray(coupling).ravel()]
        target = [Decimal.from_float(float(value)) for value in np.asarray(rhs).ravel()]
        result = np.empty(self.matrix.shape[0])
        with localcontext() as context:
            context.prec = 64
            for row in range(self.matrix.shape[0]):
                start, stop = self.matrix.indptr[row:row + 2]
                value = coupled[row] - target[row]
                for offset in range(start, stop):
                    value += self.entries[offset] * vector[self.matrix.indices[offset]]
                result[row] = float(value)
        return result.reshape(shape)


def solve_joint_rhs(system, response, momentum_response, rhs, record):
    inverse = system['inverse']
    arithmetic = DecimalSparseResidual(system['matrix'])
    direction = inverse.solve(rhs.ravel()).reshape(rhs.shape)
    scale = max(inverse.residual_norm(rhs), 1e-30)
    history = []
    for index in range(24):
        metric = response.apply(direction)
        coupling = momentum_response.accumulate(metric.values)
        residual = arithmetic.evaluate(direction, coupling, rhs)
        correction = inverse.solve(residual.ravel()).reshape(rhs.shape)
        row = dict(iteration=index, relative_residual=inverse.residual_norm(residual) / scale,
            maximum_residual=float(np.max(abs(residual))), maximum_correction=float(np.max(abs(correction))),
            radial_linear_residual=metric.residual, residual_arithmetic='Decimal64 over represented binary64 inputs')
        row['residual_ratio'] = None if not history else row['relative_residual'] / max(history[-1]['relative_residual'], 1e-300)
        history.append(row)
        record(row, direction, coupling, residual, metric)
        if row['relative_residual'] <= 2e-11 and row['maximum_correction'] <= 2e-12:
            return direction, metric, coupling, rhs, history
        if index >= 2 and row['relative_residual'] > 1.25 * history[-2]['relative_residual']:
            raise RuntimeError('Compensated joint jerk lost contraction; retain saved iterate')
        direction -= correction
    raise RuntimeError('Compensated joint jerk did not reach unchanged stopping gates')
