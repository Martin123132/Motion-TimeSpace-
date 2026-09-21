import numpy as np

from annular_independent_continuum_20260914 import ContinuumEvolution


LEFT_ROWS = (
    (-24/17, 59/34, -4/17, -3/34, 0., 0.),
    (-.5, 0., .5, 0., 0., 0.),
    (4/43, -59/86, 0., 59/86, -4/43, 0.),
    (3/98, 0., -59/98, 0., 32/49, -4/49),
)


def boundary_weights(count, spacing):
    weights = np.ones(count)
    weights[:4] = [17/48, 59/48, 43/48, 49/48]
    weights[-4:] = weights[:4][::-1]
    return spacing*weights


def boundary_derivative(values, spacing):
    values = np.asarray(values)
    if values.ndim != 1 or len(values) < 17:
        raise ValueError('A one-dimensional array with at least17 nodes is required.')
    result = np.empty_like(values)
    result[4:-4] = (values[2:-6]-8*values[3:-5]+8*values[5:-3]-values[6:-2])/(12*spacing)
    for index, coefficients in enumerate(LEFT_ROWS):
        result[index] = np.dot(coefficients, values[:6])/spacing
        result[-1-index] = -np.dot(coefficients, values[-1:-7:-1])/spacing
    return result


class ReflectingContinuum(ContinuumEvolution):
    def rhs(self, time, state):
        self.calls += 1
        scalar, gradient, momentum = self.unpack(state)
        geometry = self.geometry(state)
        scalar_rate = geometry['L']*momentum/self.radii**2
        gradient_rate = boundary_derivative(scalar_rate, self.spacing)
        momentum_rate = boundary_derivative(self.radii**2*geometry['L']*gradient, self.spacing)
        gradient_rate[0] = 0.
        momentum_rate[-1] = 0.
        scalar_rate[-1] = 0.
        return np.concatenate([scalar_rate, gradient_rate, momentum_rate])
