import numpy as numerical

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
from annular_gram_joint_action_20260909 import gram_matrices


class InheritedKnotLinkQuadrature(MetricLinkQuadrature):
    def __init__(self, basis, inherited_knots, order=8):
        factors, sampling = gram_matrices(basis.radii.size)
        self.factor, self.node = numerical.nonzero((factors != 0) | (sampling != 0))
        self.count = factors.shape[0]
        self.tweight = factors[self.factor, self.node]
        self.sweight = sampling[self.factor, self.node]
        self.anchors = (sampling @ basis.radii)[self.factor]
        self.targets = basis.radii[self.node]
        gauss, weights = numerical.polynomial.legendre.leggauss(order)
        primitive = numerical.empty((order, order))
        for column in range(order):
            others = numerical.delete(gauss, column)
            polynomial = numerical.polynomial.Polynomial.fromroots(others) / numerical.prod(gauss[column] - others)
            integral = polynomial.integ()
            primitive[:, column] = integral(gauss) - integral(-1)
        self.knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces, inherited_knots]))
        if self.knots[0] != basis.radii[0] or self.knots[-1] != basis.radii[-1]:
            raise ValueError('Inherited breakpoints must remain inside the shared annulus.')
        points, signed_weights, pairs = [], [], []
        self.blocks = []
        offset = 0
        for pair, (anchor, target) in enumerate(zip(self.anchors, self.targets)):
            if anchor == target:
                continue
            lower, upper = min(anchor, target), max(anchor, target)
            knots = numerical.concatenate([[lower], self.knots[(self.knots > lower) & (self.knots < upper)], [upper]])
            if target < anchor:
                knots = knots[::-1]
            halfwidth = numerical.diff(knots) / 2
            centers = (knots[1:] + knots[:-1]) / 2
            local_points = (centers[:, None] + halfwidth[:, None] * gauss).ravel()
            local_weights = (halfwidth[:, None] * weights).ravel()
            size = local_points.size
            partial = numerical.zeros((size, size))
            for segment, half in enumerate(halfwidth):
                selected = slice(segment * order, (segment + 1) * order)
                partial[selected, :segment * order] = local_weights[:segment * order]
                partial[selected, selected] = half * primitive
            self.blocks.append((pair, slice(offset, offset + size), partial))
            points.extend(local_points)
            signed_weights.extend(local_weights)
            pairs.extend([pair] * size)
            offset += size
        self.points = numerical.asarray(points)
        self.weights = numerical.asarray(signed_weights)
        self.pairs = numerical.asarray(pairs, dtype=int)
        self.face_value = linear_value_gradient(basis.faces, self.points)[0]
        self.node_value = linear_value_gradient(basis.radii, self.points)[0]
