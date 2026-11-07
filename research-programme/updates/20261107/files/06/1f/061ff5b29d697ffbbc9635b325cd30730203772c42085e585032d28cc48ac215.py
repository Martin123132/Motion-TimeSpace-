from __future__ import annotations

import math
import numpy as np


BASIS = np.array([[[1., 0.], [0., 0.]], [[0., 0.], [0., 1.]],
                  [[0., 1.], [1., 0.]], [[0., 1.], [-1., 0.]]])
BASIS[2:] /= math.sqrt(2)
TRANSPOSE_PARITY = np.array([1., 1., 1., -1.])


def q2(argument):
    values = np.asarray(argument, dtype=complex)
    output = np.empty_like(values)
    large = np.abs(values) > 3
    inverse = 1 / values[large]
    power = inverse**3
    series = np.zeros_like(inverse)
    for degree in range(1, 26):
        series += (2 * degree / ((2 * degree + 1) * (2 * degree + 3))) * power
        power *= inverse**2
    output[large] = series
    small = values[~large]
    output[~large] = (3 * small**2 - 1) * np.log1p(2 / (small - 1)) / 4 - 1.5 * small
    return output


def q2_derivative(argument):
    values = np.asarray(argument, dtype=complex)
    output = np.empty_like(values)
    large = np.abs(values) > 3
    inverse = 1 / values[large]
    power = inverse**4
    series = np.zeros_like(inverse)
    for degree in range(1, 26):
        series -= (2 * degree / (2 * degree + 3)) * power
        power *= inverse**2
    output[large] = series
    small = values[~large]
    output[~large] = (1.5 * small * np.log1p(2 / (small - 1))
                     - (3 * small**2 - 1) / (2 * (small**2 - 1)) - 1.5)
    return output


class Candidate:
    def __init__(self, epsilon=0.01, ratio=2.0, chemical=1.0):
        if ratio <= 1 or epsilon < 0 or chemical <= 0:
            raise ValueError("This experiment is restricted to y>1, epsilon>=0, mu>0.")
        self.epsilon = float(epsilon)
        self.ratio = float(ratio)
        self.chemical = float(chemical)
        self.mass_squared = chemical**2 * (2 * ratio - 2 / 3) / (1 + ratio)
        self.gap_squared = self.mass_squared + 4 * chemical**2
        self.sound = math.sqrt(self.mass_squared / self.gap_squared)
        cubic_radial = chemical * math.sqrt(epsilon) * (6 * ratio - 2 / 9) / (1 + ratio)
        cubic_mixed = chemical * math.sqrt(epsilon) * (2 * ratio - 2 / 3) / (1 + ratio)
        self.cubics = np.array([[[cubic_radial, 0.], [0., cubic_mixed]],
                               [[0., cubic_mixed], [cubic_mixed, 0.]]]).transpose(1, 2, 0)

    def propagator(self, frequency, momentum):
        frequency, momentum = np.broadcast_arrays(frequency, momentum)
        squared = frequency**2 + momentum**2
        determinant = squared * (squared + self.mass_squared) + 4 * self.chemical**2 * frequency**2
        result = np.empty(frequency.shape + (2, 2))
        result[..., 0, 0] = squared / determinant
        result[..., 0, 1] = 2 * self.chemical * frequency / determinant
        result[..., 1, 0] = -result[..., 0, 1]
        result[..., 1, 1] = (squared + self.mass_squared) / determinant
        return result

    def exchange_l2(self, frequency, first, second):
        frequency, first, second = np.broadcast_arrays(frequency, first, second)
        if np.any(first <= 0) or np.any(second <= 0):
            raise ValueError("Projection nodes must have positive radial momentum.")
        angular_scale = 2 * first * second
        offset = -frequency**2 - first**2 - second**2
        discriminant = self.mass_squared**2 - 16 * self.chemical**2 * frequency**2
        radical = np.sqrt(discriminant.astype(complex))
        high = (self.mass_squared + radical) / 2
        low = (self.mass_squared - radical) / 2
        repeated = np.abs(discriminant) < 1e-12 * self.mass_squared**2
        safe_radical = np.where(repeated, 1., radical)
        high_q = q2((high - offset) / angular_scale)
        low_q = q2((low - offset) / angular_scale)
        divided = (high_q - low_q) / safe_radical
        weighted = (high * high_q - low * low_q) / safe_radical
        if np.any(repeated):
            root = self.mass_squared / 2
            value = (root - offset[repeated]) / angular_scale[repeated]
            derivative = q2_derivative(value) / angular_scale[repeated]
            divided[repeated] = derivative
            weighted[repeated] = q2(value) + root * derivative
        result = np.empty(frequency.shape + (2, 2), dtype=complex)
        result[..., 0, 0] = weighted / angular_scale
        result[..., 1, 1] = (weighted - self.mass_squared * divided) / angular_scale
        result[..., 0, 1] = -2 * self.chemical * frequency * divided / angular_scale
        result[..., 1, 0] = -result[..., 0, 1]
        if np.max(np.abs(result.imag), initial=0) > 2e-10 * max(1., np.max(np.abs(result.real), initial=0)):
            raise ArithmeticError("Imaginary residual in a Euclidean real matrix.")
        return result.real

    def coupling_blocks(self, frequency, momentum):
        propagators = self.propagator(frequency, momentum)
        varied = np.einsum("nac,Bcd,nde->nBae", propagators, BASIS, propagators, optimize=True)
        output = np.empty((len(propagators), 2, 2, 4, 4))
        for first in range(2):
            for second in range(2):
                response = self.cubics[:, :, first] @ varied @ self.cubics[:, :, second].T
                output[:, first, second] = np.einsum("Aab,nBab->nAB", BASIS, response, optimize=True)
        return output


def rectangle_log_integral(radial_halfwidth, frequency_halfwidth, sound, momentum):
    first = radial_halfwidth
    second = frequency_halfwidth / sound
    return 4 * sound * (first * second * math.log(4 * momentum**2 / (first**2 + second**2))
                        + 3 * first * second - first**2 * math.atan(second / first)
                        - second**2 * math.atan(first / second))


def assemble(candidate, cells=8, order=4, cutoff=4., mesh_power=1.5):
    edges = cutoff * np.linspace(0, 1, cells + 1)**mesh_power
    centers = (edges[:-1] + edges[1:]) / 2
    halfwidths = np.diff(edges) / 2
    abscissae, weights = np.polynomial.legendre.leggauss(order)
    frequency_nodes = centers[:, None] + halfwidths[:, None] * abscissae
    radial_nodes = frequency_nodes.copy()
    one_weights = halfwidths[:, None] * weights
    frequencies = np.broadcast_to(frequency_nodes[:, None, :, None], (cells, cells, order, order)).reshape(cells**2, order**2)
    momenta = np.broadcast_to(radial_nodes[None, :, None, :], (cells, cells, order, order)).reshape(cells**2, order**2)
    integration_weights = (one_weights[:, None, :, None] * one_weights[None, :, None, :]).reshape(cells**2, order**2)
    flat_frequency, flat_momentum = frequencies.ravel(), momenta.ravel()
    positive_blocks = candidate.coupling_blocks(flat_frequency, flat_momentum)
    negative_blocks = candidate.coupling_blocks(-flat_frequency, flat_momentum)
    matrix = np.empty((cells**2, 4, cells**2, 4))
    for outer_index in range(cells**2):
        frequency_index, radial_index = divmod(outer_index, cells)
        frequency = centers[frequency_index]
        momentum = centers[radial_index]
        exchange_positive = candidate.exchange_l2(frequency - flat_frequency, momentum, flat_momentum)
        exchange_negative = candidate.exchange_l2(frequency + flat_frequency, momentum, flat_momentum)
        plus = np.einsum("ndf,ndfAB->nAB", exchange_positive, positive_blocks, optimize=True)
        minus = np.einsum("ndf,ndfAB->nAB", exchange_negative, negative_blocks, optimize=True)
        minus *= TRANSPOSE_PARITY[None, None, :]
        scale = flat_momentum**4 / momentum**2
        plus = (plus * scale[:, None, None]).reshape(cells**2, order**2, 4, 4)
        minus = (minus * scale[:, None, None]).reshape(cells**2, order**2, 4, 4)
        diagonal_source = candidate.coupling_blocks(np.array([frequency]), np.array([momentum]))[0, 1, 1] / 4
        distance_squared = ((frequencies[outer_index] - frequency) / candidate.sound)**2 + (momenta[outer_index] - momentum)**2
        singular_log = np.log(4 * momentum**2 / distance_squared)
        plus[outer_index] -= singular_log[:, None, None] * diagonal_source
        integrated = np.einsum("nq,nqAB->nAB", integration_weights, plus + minus, optimize=True)
        exact_log = rectangle_log_integral(halfwidths[radial_index], halfwidths[frequency_index], candidate.sound, momentum)
        integrated[outer_index] += exact_log * diagonal_source
        matrix[outer_index] = integrated.transpose(1, 0, 2) / (4 * math.pi**3)
    return matrix.reshape(4 * cells**2, 4 * cells**2), centers
