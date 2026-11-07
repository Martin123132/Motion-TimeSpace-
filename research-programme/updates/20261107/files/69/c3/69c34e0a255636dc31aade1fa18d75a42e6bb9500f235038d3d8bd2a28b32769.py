from __future__ import annotations

import numpy as np


class QuadraticQuadrature:
    def __init__(self, radius, cells, order):
        if radius > 16:
            inner_count = cells//4
            edges = np.concatenate([np.linspace(0, radius-12, inner_count+1),
                                    np.linspace(radius-12, radius, cells-inner_count+1)[1:]])
        else:
            edges = np.linspace(0, radius, cells+1)
        widths = np.diff(edges)
        nodes, weights = np.polynomial.legendre.leggauss(order)
        unit = (nodes+1)/2
        self.position = (edges[:-1, None]+widths[:, None]*unit[None, :]).ravel()
        self.weights = (widths[:, None]*weights[None, :]/2).ravel()
        self.nodal_position = np.empty(2*cells+1)
        self.nodal_position[::2] = edges
        self.nodal_position[1::2] = (edges[:-1]+edges[1:])/2
        self.full_basis = np.zeros((cells*order, 2*cells+1))
        self.full_derivative = np.zeros_like(self.full_basis)
        values = [2*unit**2-3*unit+1, 4*unit*(1-unit), 2*unit**2-unit]
        derivatives = [4*unit-3, 4-8*unit, 4*unit-1]
        for cell in range(cells):
            selection = slice(cell*order, (cell+1)*order)
            for offset in range(3):
                self.full_basis[selection, 2*cell+offset] = values[offset]
                self.full_derivative[selection, 2*cell+offset] = derivatives[offset]/widths[cell]
        self.basis = self.full_basis[:, 1:-1]
        self.derivative = self.full_derivative[:, 1:-1]

    def integrate(self, values):
        return np.einsum('q,q...->...', self.weights, values)

    def form(self, left, coefficient, right=None):
        if right is None:
            right = left
        return left.T@((self.weights*coefficient)[:, None]*right)
