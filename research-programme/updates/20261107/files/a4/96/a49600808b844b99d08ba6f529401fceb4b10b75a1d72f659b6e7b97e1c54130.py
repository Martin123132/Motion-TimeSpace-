from derive_annular_source_gravity_20260914 import EvidenceRun
from fractions import Fraction
import numpy as np


def reference_offsets(action):
    anchor = Fraction(action.mesh['anchor'])
    return np.asarray([float(Fraction(value) - anchor) for value in action.mesh['edges']])


class CenteredLabelDensity:
    def __init__(self, action, radius_offset, order):
        self.action, self.radius_offset = action, np.asarray(radius_offset)
        self.anchor = float(Fraction(action.mesh['anchor']))
        self.references = reference_offsets(action)
        self.source_coefficients = action.owner.layer_rule.inverse @ (action.source - self.anchor)
        self.source_derivative = 2 * np.polynomial.chebyshev.chebder(self.source_coefficients)
        endpoints = np.array([self.geometry(self.references, label)[0] for label in [-.5, .5]])
        rows, columns = np.nonzero((self.radius_offset[:, None] > endpoints[0]) & (self.radius_offset[:, None] < endpoints[1]))
        counts = np.bincount(rows, minlength=len(self.radius_offset))
        starts = np.cumsum(counts) - counts
        local = np.arange(len(rows)) - np.repeat(starts, counts)
        cuts = np.full((len(self.radius_offset), int(max(counts)) + 2), np.nan)
        cuts[:, :2] = [-.5, .5]
        cuts[rows, local + 2] = self.inverse(self.radius_offset[rows], self.references[columns])
        cuts.sort(axis=1)
        lengths = np.diff(cuts, axis=1)
        selected = np.isfinite(lengths) & (lengths > 1e-13)
        segment_rows, segment_columns = np.nonzero(selected)
        lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
        points, weights = np.polynomial.legendre.leggauss(order)
        labels = (lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2
        measures = (upper - lower)[:, None] * weights * 6 * (labels + .5) * (.5 - labels) / 2
        self.offsets, self.label_weights = labels.ravel(), measures.ravel()
        self.indices = np.repeat(segment_rows, order)
        self.interpolation = np.polynomial.chebyshev.chebvander(2 * self.offsets, action.owner.layer_degree) @ action.owner.layer_rule.inverse

    def source_offset(self, labels):
        return np.polynomial.chebyshev.chebval(2 * labels, self.source_coefficients)

    def geometry(self, reference_offset, labels):
        displacement = np.where(reference_offset < 0., 1 + reference_offset / (-self.references[0]),
            1 - reference_offset / self.references[-1])
        source = self.source_offset(labels)
        location = reference_offset + displacement * source + (1 - displacement) * self.action.owner.width * labels
        derivative = (1 - displacement) * self.action.owner.width
        derivative += displacement * np.polynomial.chebyshev.chebval(2 * labels, self.source_derivative)
        return location, derivative

    def inverse(self, radius_offset, reference_offset):
        lower = self.geometry(reference_offset, -.5)[0]
        upper = self.geometry(reference_offset, .5)[0]
        labels = (radius_offset - lower) / (upper - lower) - .5
        for unused in range(8):
            value, derivative = self.geometry(reference_offset, labels)
            labels -= (value - radius_offset) / derivative
        return np.clip(labels, -.5, .5)


def metric_at_offset(solver, solution, radius_offset, anchor, second=False):
    edges = solver.edges - anchor
    indices = np.clip(np.searchsorted(edges, radius_offset, side='right') - 1, 0, len(edges) - 2)
    centers = (edges[:-1] + edges[1:]) / 2
    coordinate = 2 * (radius_offset - centers[indices]) / solver.lengths[indices]
    if second:
        return np.array([np.polynomial.chebyshev.chebval(coordinate,
            np.polynomial.chebyshev.chebder(values[indices].T, axis=0), tensor=False)
            * 2 / solver.lengths[indices] for values in solution['rhs_coefficients']])
    values = np.array([solution['left'][component, indices] + np.polynomial.chebyshev.chebval(coordinate,
        solution['primitives'][component, indices].T, tensor=False) for component in range(2)])
    radial = np.array([np.polynomial.chebyshev.chebval(coordinate,
        solution['rhs_coefficients'][component, indices].T, tensor=False) for component in range(2)])
    return values, radial


def response_at_offset(response, radius_offset, anchor):
    responses = getattr(response, 'responses', (response,))
    pairs = [metric_at_offset(item.solver, item.solution, radius_offset, anchor) for item in responses]
    return tuple(sum(pair[index] for pair in pairs) for index in range(2))
