from __future__ import annotations

import math
import numpy as np
from ward_core import WardCandidate
from operator_core import Candidate, BASIS, TRANSPOSE_PARITY, rectangle_log_integral


class TensorRegulatedCandidate:
    def __init__(self, scale=4., angular_order=32):
        self.model = WardCandidate(scale)
        self.bare = Candidate()
        self.cubics = self.model.cubics
        self.sound = self.model.sound
        self.angular_nodes, self.angular_weights = np.polynomial.legendre.leggauss(angular_order)

    def propagator(self, frequency, momentum):
        return self.model.propagator(frequency, np.asarray(momentum)**2)

    def source_factor(self, frequency, momentum):
        return self.model.derivative_factor(np.asarray(frequency)**2 + np.asarray(momentum)**2)

    def exchange_l2(self, frequency, first, second):
        frequency, first, second = np.broadcast_arrays(frequency, first, second)
        if self.model.scale is None:
            return self.bare.exchange_l2(frequency, first, second)
        original_shape = frequency.shape
        frequency, first, second = frequency.ravel(), first.ravel(), second.ravel()
        angular_scale = 2 * first * second
        near = (frequency**2 + (first - second)**2) / angular_scale < .2
        spatial_squared = (first[:, None] - second[:, None])**2 + angular_scale[:, None] * (1 - self.angular_nodes[None, :])
        regulated = self.model.propagator(frequency[:, None], spatial_squared)
        weighted = self.angular_weights * (3 * self.angular_nodes**2 - 1) / 4
        answer = np.einsum("q,nqab->nab", weighted, regulated, optimize=True)
        if np.any(near):
            bare = self.bare.propagator(frequency[near, None], np.sqrt(spatial_squared[near]))
            regulator = self.model.regulator(frequency[near, None]**2 + spatial_squared[near])
            smooth_difference = -regulator[..., None, None] * (regulated[near] @ bare)
            answer[near] = self.bare.exchange_l2(frequency[near], first[near], second[near]) + np.einsum(
                "q,nqab->nab", weighted, smooth_difference, optimize=True)
        return answer.reshape(original_shape + (2, 2))

    def coupling_blocks(self, frequency, momentum):
        propagator = self.propagator(frequency, momentum)
        varied = np.einsum("nac,Bcd,nde->nBae", propagator, BASIS, propagator, optimize=True)
        output = np.empty((len(propagator), 2, 2, 4, 4))
        for first in range(2):
            for second in range(2):
                response = self.cubics[:, :, first] @ varied @ self.cubics[:, :, second].T
                output[:, first, second] = np.einsum("Aab,nBab->nAB", BASIS, response, optimize=True)
        return output


def assemble(model, edges, order=4):
    edges = np.asarray(edges, dtype=float)
    cells = len(edges) - 1
    centers = (edges[:-1] + edges[1:]) / 2
    halfwidths = np.diff(edges) / 2
    nodes, weights = np.polynomial.legendre.leggauss(order)
    one_nodes = centers[:, None] + halfwidths[:, None] * nodes
    one_weights = halfwidths[:, None] * weights
    frequencies = np.broadcast_to(one_nodes[:, None, :, None], (cells, cells, order, order)).reshape(cells**2, order**2)
    momenta = np.broadcast_to(one_nodes[None, :, None, :], (cells, cells, order, order)).reshape(cells**2, order**2)
    integration_weights = (one_weights[:, None, :, None] * one_weights[None, :, None, :]).reshape(cells**2, order**2)
    flat_frequency, flat_momentum = frequencies.ravel(), momenta.ravel()
    positive_blocks = model.coupling_blocks(flat_frequency, flat_momentum)
    negative_blocks = model.coupling_blocks(-flat_frequency, flat_momentum)
    source_in = model.source_factor(flat_frequency, flat_momentum)
    matrix = np.empty((cells**2, 4, cells**2, 4))
    for external_index in range(cells**2):
        frequency_index, radial_index = divmod(external_index, cells)
        frequency, momentum = centers[frequency_index], centers[radial_index]
        source_out = model.source_factor(frequency, momentum)
        first_exchange = model.exchange_l2(frequency - flat_frequency, momentum, flat_momentum)
        second_exchange = model.exchange_l2(frequency + flat_frequency, momentum, flat_momentum)
        first_term = np.einsum("ndf,ndfAB->nAB", first_exchange, positive_blocks, optimize=True)
        second_term = np.einsum("ndf,ndfAB->nAB", second_exchange, negative_blocks, optimize=True)
        second_term *= TRANSPOSE_PARITY[None, None, :]
        scale = flat_momentum**4 / momentum**2 * source_in / source_out
        first_term = (first_term * scale[:, None, None]).reshape(cells**2, order**2, 4, 4)
        second_term = (second_term * scale[:, None, None]).reshape(cells**2, order**2, 4, 4)
        singular_source = model.coupling_blocks(np.array([frequency]), np.array([momentum]))[0, 1, 1] / 4
        distance = ((frequencies[external_index] - frequency) / model.sound)**2 + (momenta[external_index] - momentum)**2
        first_term[external_index] -= np.log(4 * momentum**2 / distance)[:, None, None] * singular_source
        integrated = np.einsum("nq,nqAB->nAB", integration_weights, first_term + second_term, optimize=True)
        integrated[external_index] += rectangle_log_integral(halfwidths[radial_index], halfwidths[frequency_index], model.sound, momentum) * singular_source
        matrix[external_index] = integrated.transpose(1, 0, 2) / (4 * math.pi**3)
    return matrix.reshape(4 * cells**2, 4 * cells**2), centers
