from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_position_time_loads_20260929 import MixedJet
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_physical_native_kernel_20260928 import decimals
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
from time import perf_counter
import numpy as np


def take(jet, key):
    return MixedJet(*[value[key] for value in jet.parts])


def reshape(jet, shape):
    return MixedJet(*[value.reshape(shape) for value in jet.parts])


def choose(mask, first, second):
    first, second = MixedJet.cast(first), MixedJet.cast(second)
    return MixedJet(*[np.where(mask, left, right) for left, right in zip(first.parts, second.parts)])


def contract(pattern, first, second):
    first, second = MixedJet.cast(first), MixedJet.cast(second)
    multiply = lambda left, right: np.einsum(pattern, first.parts[left], second.parts[right], optimize=False)
    return MixedJet(multiply(0, 0), multiply(1, 0) + multiply(0, 1),
        multiply(2, 0) + multiply(0, 2),
        multiply(3, 0) + multiply(1, 2) + multiply(2, 1) + multiply(0, 3))


def chebyshev(coefficients, argument):
    coefficients, argument = MixedJet.cast(coefficients), MixedJet.cast(argument)
    count = len(coefficients.parts[0])
    last, previous = MixedJet(0.), MixedJet(0.)
    for index in range(count - 1, 0, -1):
        last, previous = take(coefficients, index) + 2 * argument * last - previous, last
    return take(coefficients, 0) + argument * last - previous


def label_derivative_jet(coefficients):
    return MixedJet(*[2 * np.polynomial.chebyshev.chebder(value, axis=0) for value in coefficients.parts])


def nodal_values(cardinal, values, indices):
    multiply = lambda left, right: indexed_label_values(cardinal.parts[left], values.parts[right], indices)
    return MixedJet(multiply(0, 0), multiply(1, 0) + multiply(0, 1),
        multiply(2, 0) + multiply(0, 2),
        multiply(3, 0) + multiply(1, 2) + multiply(2, 1) + multiply(0, 3))


class PositionTimeLoads:
    def __init__(self, position_engine, mode_rate, acceleration, native_coefficients=None):
        self.engine = position_engine
        self.loads, self.material, self.owner = position_engine.loads, position_engine.material, position_engine.owner
        self.model = self.owner.model
        self.native_coefficients = None if native_coefficients is None else MixedJet(*native_coefficients)
        self.native_references = np.asarray(position_engine.native.references, float)[position_engine.native.native_edges]
        self.native_bounds = np.array([self.material.node_geometry(self.native_references, label)[0] for label in [-.5, .5]])
        self.sampling = position_engine.native.sampling.tocsc()
        inverse = self.owner.layer_rule.inverse
        self.source_coefficients = MixedJet(self.material.coefficients[:, -1],
            inverse @ position_engine.direction[:, -1], inverse @ self.loads.rates[:, -1], inverse @ mode_rate[:, -1])
        self.source_label_coefficients = label_derivative_jet(self.source_coefficients)
        self.support_coefficients = inverse @ position_engine.edge_vertices
        self.support_label_coefficients = 2 * np.polynomial.chebyshev.chebder(self.support_coefficients, axis=0)
        self.velocity = MixedJet(self.loads.rates, mode_rate, acceleration)
        self.position_parameter = MixedJet(0., 1.)
        unused, mixed_gradient = local_polynomials(position_engine.action.mesh, decimals(mode_rate[:, :-1].T))
        self.gradients = MixedJet(self.material.gradient_coefficients, position_engine.direction_gradient,
            position_engine.rate_gradient, np.asarray(mixed_gradient, float))

    def cardinal(self, labels):
        return chebyshev(self.owner.layer_rule.inverse, 2 * take(labels, (slice(None), None)))

    def source(self, labels):
        return chebyshev(self.source_coefficients, 2 * labels)

    def support(self, reference, labels):
        cells = np.clip(np.searchsorted(self.model.edges, reference.parts[0], side='right') - 1, 0, len(self.model.edges) - 2)
        widths = np.diff(self.model.edges)[cells]
        local = (reference - self.model.edges[cells]) / widths
        left = chebyshev(self.support_coefficients[:, cells], 2 * labels)
        right = chebyshev(self.support_coefficients[:, cells + 1], 2 * labels)
        left_label = chebyshev(self.support_label_coefficients[:, cells], 2 * labels)
        right_label = chebyshev(self.support_label_coefficients[:, cells + 1], 2 * labels)
        return (1 - local) * left + local * right, (right - left) / widths, (1 - local) * left_label + local * right_label

    def geometry(self, reference, labels):
        reference, labels = MixedJet.cast(reference), MixedJet.cast(labels)
        left = reference.parts[0] <= self.model.anchor
        displacement = choose(left, (reference - self.model.radii[0]) / (self.model.anchor - self.model.radii[0]),
            (self.model.radii[-1] - reference) / (self.model.radii[-1] - self.model.anchor))
        slope = np.where(left, 1 / (self.model.anchor - self.model.radii[0]), -1 / (self.model.radii[-1] - self.model.anchor))
        source = self.source(labels)
        source_label = chebyshev(self.source_label_coefficients, 2 * labels)
        support, support_spatial, support_label = self.support(reference, labels)
        radius = reference + displacement * (source - self.model.anchor) + (1 - displacement) * self.owner.width * labels
        radius += self.position_parameter * support
        spatial = 1 + slope * (source - self.model.anchor - self.owner.width * labels) + self.position_parameter * support_spatial
        label_jacobian = (1 - displacement) * self.owner.width + displacement * source_label + self.position_parameter * support_label
        return radius, spatial, label_jacobian, displacement

    def inverse(self, radius, reference, initial):
        labels = MixedJet(initial)
        for unused in range(6):
            position, unused2, jacobian, unused3 = self.geometry(reference, labels)
            labels -= (position - radius) / jacobian
        return labels

    def wave(self, radius):
        endpoints = np.array([self.material.node_geometry(self.model.edges, label)[0] for label in [-.5, .5]])
        rows, columns = np.nonzero((radius[:, None] > endpoints[0]) & (radius[:, None] < endpoints[1]))
        counts = np.bincount(rows, minlength=len(radius))
        starts = np.cumsum(counts) - counts
        indices = np.arange(len(rows)) - np.repeat(starts, counts)
        base = np.full((len(radius), int(max(counts)) + 2), np.nan)
        base[:, :2] = [-.5, .5]
        cuts = MixedJet(base, np.zeros_like(base), np.zeros_like(base), np.zeros_like(base))
        initial = self.material.inverse_node(radius[rows], self.model.edges[columns])
        solved = self.inverse(radius[rows], self.model.edges[columns], initial)
        for component, values in enumerate(cuts.parts):
            values[rows, indices + 2] = solved.parts[component]
        ordering = np.argsort(cuts.parts[0], axis=1)
        cuts = MixedJet(*[np.take_along_axis(value, ordering, axis=1) for value in cuts.parts])
        lengths = np.diff(cuts.parts[0], axis=1)
        segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths > 1e-13))
        lower, upper = take(cuts, (segment_rows, segment_columns)), take(cuts, (segment_rows, segment_columns + 1))
        points, weights = np.polynomial.legendre.leggauss(self.owner.label_order)
        labels = (take(lower + upper, (slice(None), None)) + take(upper - lower, (slice(None), None)) * points) / 2
        measure = take(upper - lower, (slice(None), None)) * weights / 2 * (1.5 - 6 * labels**2)
        labels, measure = reshape(labels, (-1,)), reshape(measure, (-1,))
        rows = np.repeat(segment_rows, len(points))
        source = self.source(labels)
        inner, outer = self.model.radii[0] + self.owner.width * labels, self.model.radii[-1] + self.owner.width * labels
        left = radius[rows] < source.parts[0]
        spatial = choose(left, (source - inner) / (self.model.anchor - self.model.radii[0]),
            (outer - source) / (self.model.radii[-1] - self.model.anchor))
        reference = choose(left, self.model.radii[0] + (radius[rows] - inner) / spatial,
            self.model.radii[-1] - (outer - radius[rows]) / spatial)
        for unused in range(3):
            position, spatial, unused2, unused3 = self.geometry(reference, labels)
            reference -= (position - radius[rows]) / spatial
        unused, spatial, unused2, displacement = self.geometry(reference, labels)
        cells = np.clip(np.searchsorted(self.model.edges, reference.parts[0], side='right') - 1, 0, len(self.model.edges) - 2)
        local = (reference - self.model.edges[cells]) / np.diff(self.model.edges)[cells]
        shape = [(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)]
        element_indices = self.model.element_indices[cells]
        cardinal = self.cardinal(labels)
        coefficients = contract('ql,qpl->qp', cardinal, take(self.gradients, cells))
        gradient = (take(coefficients, (slice(None), 0)) + take(coefficients, (slice(None), 1)) * local) / spatial
        sampled = nodal_values(cardinal, take(self.velocity, (slice(None), slice(None, -1))), element_indices)
        temporal = sum(shape[index] * take(sampled, (slice(None), index)) * (element_indices[:, index] >= 0) for index in range(3))
        velocity = contract('ql,l->q', cardinal, take(self.velocity, (slice(None), -1)))
        temporal -= displacement * velocity * gradient
        outside = (radius[rows] < inner.parts[0]) | (radius[rows] > outer.parts[0])
        temporal, gradient = choose(outside, 0., temporal), choose(outside, 0., gradient)
        reduce = lambda density: np.array([np.bincount(rows, weights=value, minlength=len(radius)) for value in density.parts])
        return reduce(measure * temporal**2), reduce(measure * gradient**2)

    def sample(self, radius):
        radius = np.asarray(radius)
        temporal, gradient = self.wave(radius)
        result = dict(temporal_square=temporal, gradient_square=gradient,
            gram=np.zeros((4, len(radius))), source_density=np.zeros((4, len(radius))), velocity=np.zeros((4, len(radius))))
        selected = (radius > self.material.coordinates[0, -1]) & (radius < self.material.coordinates[-1, -1])
        labels = self.inverse(radius[selected], np.full(np.count_nonzero(selected), self.model.anchor),
            self.material.inverse_node(radius[selected], self.model.anchor))
        jacobian = self.geometry(np.full(np.count_nonzero(selected), self.model.anchor), labels)[2]
        density = (1.5 - 6 * labels**2) / jacobian
        velocity = contract('ql,l->q', self.cardinal(labels), take(self.velocity, (slice(None), -1)))
        result['source_density'][:, selected], result['velocity'][:, selected] = density.parts, velocity.parts
        if self.native_coefficients is not None:
            active = np.any((radius[:, None] > self.native_bounds[0]) & (radius[:, None] < self.native_bounds[1]), axis=0)
            for native_index in np.flatnonzero(active):
                reference = self.native_references[native_index]
                sampling = self.sampling
                start, end = sampling.indptr[native_index:native_index + 2]
                if start == end:
                    continue
                reference = float(reference)
                lower, upper = self.material.node_geometry(reference, np.array([-.5, .5]))[0]
                selected = (radius > lower) & (radius < upper)
                if not np.any(selected):
                    continue
                labels = self.inverse(radius[selected], np.full(np.count_nonzero(selected), reference),
                    self.material.inverse_node(radius[selected], reference))
                jacobian = self.geometry(np.full(np.count_nonzero(selected), reference), labels)[2]
                factors, weights = sampling.indices[start:end], sampling.data[start:end]
                images = chebyshev(take(self.native_coefficients, (slice(None), factors)), 2 * take(labels, (slice(None), None)))
                load = images**2 / 2
                load = MixedJet(*[value @ weights for value in load.parts])
                density = (1.5 - 6 * labels**2) * load / jacobian
                result['gram'][:, selected] += np.array(density.parts)
        return result
