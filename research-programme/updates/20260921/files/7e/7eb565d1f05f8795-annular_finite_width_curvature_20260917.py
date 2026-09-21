import numpy as np
from scipy.special import roots_legendre


class CurvatureKernel:
    def __init__(self, offsets, coefficients):
        self.offsets = np.asarray(offsets, dtype=float)
        self.coefficients = np.asarray(coefficients, dtype=float)
        if self.coefficients.ndim != 2 or self.coefficients.shape[1] != len(self.offsets):
            raise ValueError('Rows must act on the supplied actual nodal coordinates.')
        self.moments = np.column_stack([
            self.coefficients @ np.minimum(self.offsets, 0.),
            self.coefficients @ np.maximum(self.offsets, 0.)])

    def values(self, points, side):
        points = np.asarray(points)
        if side == 0:
            hinges = np.maximum(points[:, None]-self.offsets[None, :], 0.)
            hinges[:, self.offsets >= 0.] = 0.
        elif side == 1:
            hinges = np.maximum(self.offsets[None, :]-points[:, None], 0.)
            hinges[:, self.offsets <= 0.] = 0.
        else:
            raise ValueError('Side must be zero or one.')
        return self.coefficients @ hinges.T

    def quadrature(self, side, order):
        selected = self.offsets < 0. if side == 0 else self.offsets > 0.
        breaks = np.unique(np.append(self.offsets[selected], 0.))
        nodes, weights = roots_legendre(order)
        if len(breaks) < 2:
            return np.empty(0), np.empty((len(self.coefficients), 0))
        half = np.diff(breaks)/2
        points = ((breaks[:-1]+half)[:, None]+half[:, None]*nodes).ravel()
        weights = (half[:, None]*weights).ravel()
        return points, self.values(points, side)*weights[None, :]

    def absolute_integrals(self):
        totals = np.zeros((len(self.coefficients), 2))
        for side in range(2):
            selected = self.offsets < 0. if side == 0 else self.offsets > 0.
            breaks = np.unique(np.append(self.offsets[selected], 0.))
            values = self.values(breaks, side)
            for index, width in enumerate(np.diff(breaks)):
                first, second = values[:, index], values[:, index+1]
                same = first*second >= 0.
                totals[same, side] += width*(abs(first[same])+abs(second[same]))/2
                opposite = ~same
                totals[opposite, side] += width*(first[opposite]**2+second[opposite]**2)/(2*(abs(first[opposite])+abs(second[opposite])))
        return totals

    def chebyshev_maps(self, degree, lengths, order):
        maps = []
        for side, length in enumerate(lengths):
            points, weights = self.quadrature(side, order)
            mapped = 1+2*points/length if side == 0 else -1+2*points/length
            basis = np.polynomial.chebyshev.chebvander(mapped, degree-1)
            maps.append(weights @ basis)
        return np.stack(maps, axis=1)


def source_curvature_kernel(system):
    original = system.original.tocsr()
    rows = []
    for index in range(original.shape[0]):
        columns = original.indices[original.indptr[index]:original.indptr[index+1]]
        offsets = system.radii[columns]-system.anchor
        if len(offsets) and min(offsets)<0.<max(offsets):
            rows.append(index)
    restricted = system.lifted[rows].tocsr()
    columns = np.unique(restricted.indices)
    return np.array(rows), columns, CurvatureKernel(system.radii[columns]-system.anchor, restricted[:, columns].toarray())
