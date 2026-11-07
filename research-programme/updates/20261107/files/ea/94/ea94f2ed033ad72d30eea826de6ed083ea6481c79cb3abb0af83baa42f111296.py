import math
import numpy as np
from operator_core import TRANSPOSE_PARITY, rectangle_log_integral


def assemble_explicit(candidate, edges, order=6):
    edges = np.asarray(edges, dtype=float)
    if edges[0] != 0 or not np.all(np.diff(edges) > 0):
        raise ValueError('Ordered positive cells starting at zero are required.')
    cells = len(edges) - 1
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
