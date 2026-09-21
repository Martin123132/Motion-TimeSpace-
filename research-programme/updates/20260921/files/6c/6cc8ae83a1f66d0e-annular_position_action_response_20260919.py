from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.sparse.linalg import LinearOperator, expm_multiply
import numpy as np


class PositionGenerator(LinearOperator):
    def __init__(self, action, first_force, slope, scale):
        self.action, self.first_force, self.slope, self.scale = action, first_force, slope, float(scale)
        self.calls = 0
        super().__init__(dtype=np.dtype(float), shape=(2*action.count+2, 2*action.count+2))

    def _matmat(self, values):
        self.calls += values.shape[1]
        count = self.action.count
        velocity = self.scale*values[count:2*count]
        acceleration = (-self.action.acceleration_operator(values[:count])/self.scale
            +self.slope[:,None]*values[-2]+self.first_force[:,None]*values[-1])
        return np.vstack([velocity, acceleration, values[-1][None,:], np.zeros((1,values.shape[1]))])

    def _rmatmat(self, values):
        count = self.action.count
        position = -self.action.acceleration_transpose(values[count:2*count])/self.scale
        velocity = self.scale*values[:count]
        time = self.slope @ values[count:2*count]
        constant = self.first_force @ values[count:2*count]+values[-2]
        return np.vstack([position, velocity, time[None,:], constant[None,:]])

    def _matvec(self, values):
        return self._matmat(values.reshape(-1,1))[:,0]

    def _rmatvec(self, values):
        return self._rmatmat(values.reshape(-1,1))[:,0]


def propagate_position(action, position, velocity, first_force, last_force, step, constants, scale=1e6):
    generator = PositionGenerator(action, first_force, (last_force-first_force)/step, scale)
    values = np.vstack([scale*position, velocity, np.zeros((1,position.shape[1])), np.asarray(constants)[None,:]])
    result = expm_multiply(step*generator, values, traceA=0.)
    count = action.count
    return dict(position=result[:count]/scale, velocity=result[count:2*count],
        local_time=result[-2], constants=result[-1], operator_products=generator.calls)
