from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_background_time_tangent_20260928 import BackgroundLoads, FIELD_NAMES, interpolation_derivative
from annular_background_trace_20260928 import traced_labels
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_physical_native_kernel_20260928 import decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from time import perf_counter
import numpy as np


class PositionLoads(BackgroundLoads):
    def __init__(self, loads, action, native, directions, correction):
        direction = np.column_stack([directions['field_vertices'] - correction[:, :-1], -correction[:, -1]])
        super().__init__(loads, action, coordinate_direction=direction)
        self.native = native
        self.edge_vertices = directions['edge_vertices']
        self.image_coefficients = None

    def source(self, labels):
        values = list(super().source(labels))
        cardinal = self.material.interpolation(np.atleast_1d(labels))
        values[0] = cardinal @ self.material.coordinates[:, -1]
        values[3] = cardinal @ self.direction[:, -1]
        values[5] = cardinal @ self.loads.rates[:, -1]
        if np.ndim(labels) == 0:
            values = [np.asarray(value).item() for value in values]
        return tuple(values)

    def support(self, reference, labels):
        reference, labels = np.broadcast_arrays(reference, labels)
        shape = reference.shape
        reference, labels = reference.ravel(), labels.ravel()
        model = self.owner.model
        cells = np.clip(np.searchsorted(model.edges, reference.real, side='right') - 1, 0, len(model.edges) - 2)
        widths = np.diff(model.edges)[cells]
        local = (reference - model.edges[cells]) / widths
        indices = np.column_stack([cells, cells + 1])
        cardinal = self.material.interpolation(labels)
        cardinal_label = interpolation_derivative(self.owner, labels)
        edges = indexed_label_values(cardinal, self.edge_vertices, indices)
        edge_labels = indexed_label_values(cardinal_label, self.edge_vertices, indices)
        value = (1 - local) * edges[:, 0] + local * edges[:, 1]
        spatial = (edges[:, 1] - edges[:, 0]) / widths
        label = (1 - local) * edge_labels[:, 0] + local * edge_labels[:, 1]
        return tuple(values.reshape(shape) for values in [value, spatial, label])

    def movement(self, reference, labels):
        unused, unused2, unused3, displacement, slope, direction = self.mapping(reference, labels)
        support, spatial, label = self.support(reference, labels)
        direction_label = self.source(labels)[4]
        return support + displacement * direction, spatial + slope * direction, label + displacement * direction_label

    def label_partition(self, radius, radius_rate, freeze_cuts=False):
        model = self.owner.model
        endpoints = np.array([self.material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
        rows, columns = np.nonzero((radius[:, None] > endpoints[0]) & (radius[:, None] < endpoints[1]))
        counts = np.bincount(rows, minlength=len(radius))
        starts = np.cumsum(counts) - counts
        local = np.arange(len(rows)) - np.repeat(starts, counts)
        cuts = np.full((len(radius), int(max(counts)) + 2), np.nan)
        rates = np.zeros_like(cuts)
        cuts[:, :2] = [-.5, .5]
        labels = self.material.inverse_node(radius[rows], model.edges[columns])
        jacobian = self.mapping(model.edges[columns], labels)[2]
        movement = self.movement(model.edges[columns], labels)[0]
        cuts[rows, local + 2] = labels
        rates[rows, local + 2] = (radius_rate[rows] - movement) / jacobian
        order = np.argsort(cuts, axis=1)
        cuts, rates = [np.take_along_axis(values, order, axis=1) for values in [cuts, rates]]
        lengths = np.diff(cuts, axis=1)
        segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths > 1e-13))
        lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
        lower_rate, upper_rate = rates[segment_rows, segment_columns], rates[segment_rows, segment_columns + 1]
        if freeze_cuts:
            lower_rate, upper_rate = np.zeros_like(lower_rate), np.zeros_like(upper_rate)
        points, weights = np.polynomial.legendre.leggauss(self.owner.label_order)
        labels = (lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2
        label_rates = (lower_rate[:, None] + upper_rate[:, None]) / 2 + (upper_rate - lower_rate)[:, None] * points / 2
        measure = (upper - lower)[:, None] * weights / 2
        measure_rate = (upper_rate - lower_rate)[:, None] * weights * material_weight(labels) / 2
        measure_rate -= measure * 12 * labels * label_rates
        return np.repeat(segment_rows, len(points)), labels.ravel(), label_rates.ravel(), (measure * material_weight(labels)).ravel(), measure_rate.ravel()

    def wave(self, radius, radius_rate, freeze_cuts=False):
        rows, labels, label_rates, measure, measure_rate = self.label_partition(radius, radius_rate, freeze_cuts)
        model = self.owner.model
        cardinal = self.material.interpolation(labels)
        cardinal_rate = interpolation_derivative(self.owner, labels) * label_rates[:, None]
        source, source_label, unused, unused2, unused3, velocity, velocity_label, unused4 = self.source(labels)
        inner, outer = model.radii[0] + self.owner.width * labels, model.radii[-1] + self.owner.width * labels
        left = radius[rows] < source
        spatial = np.where(left, (source - inner) / (model.anchor - model.radii[0]), (outer - source) / (model.radii[-1] - model.anchor))
        reference = np.where(left, model.radii[0] + (radius[rows] - inner) / spatial, model.radii[-1] - (outer - radius[rows]) / spatial)
        unused, unused2, label_jacobian, displacement, slope, unused3 = self.mapping(reference, labels)
        movement, movement_spatial, unused = self.movement(reference, labels)
        reference_rate = (radius_rate[rows] - movement - label_jacobian * label_rates) / spatial
        spatial_rate = movement_spatial + slope * (source_label - self.owner.width) * label_rates
        indices, shape, unused = model.features_quadratic(reference)
        cells = np.clip(np.searchsorted(model.edges, reference, side='right') - 1, 0, len(model.edges) - 2)
        widths = np.diff(model.edges)[cells]
        local = (reference - model.edges[cells]) / widths
        interpolate = lambda values, basis=cardinal: np.einsum('ql,qpl->qp', basis, values[cells], optimize=False)
        coefficients = interpolate(self.material.gradient_coefficients)
        changed_coefficients = interpolate(self.direction_gradient) + interpolate(self.material.gradient_coefficients, cardinal_rate)
        gradient = (coefficients[:, 0] + coefficients[:, 1] * local) / spatial
        gradient_rate = (changed_coefficients[:, 0] + changed_coefficients[:, 1] * local + coefficients[:, 1] * reference_rate / widths) / spatial
        gradient_rate -= gradient * spatial_rate / spatial
        rate_nodes = indexed_label_values(cardinal, self.loads.rates[:, :-1], indices)
        rate_nodes_dot = indexed_label_values(cardinal_rate, self.loads.rates[:, :-1], indices)
        rate_coefficients = interpolate(self.rate_gradient)
        temporal = np.sum(shape * rate_nodes, axis=1) - displacement * velocity * gradient
        temporal_rate = np.sum(shape * rate_nodes_dot, axis=1) + (rate_coefficients[:, 0] + rate_coefficients[:, 1] * local) * reference_rate
        temporal_rate -= slope * reference_rate * velocity * gradient
        temporal_rate -= displacement * (velocity_label * label_rates * gradient + velocity * gradient_rate)
        outside = (radius[rows] < inner) | (radius[rows] > outer)
        for values in [gradient, gradient_rate, temporal, temporal_rate]:
            values[outside] = 0.
        reduce = lambda values: np.bincount(rows, weights=values, minlength=len(radius))
        return reduce(measure * temporal**2), reduce(measure * gradient**2), reduce(measure_rate * temporal**2 + 2 * measure * temporal * temporal_rate), reduce(measure_rate * gradient**2 + 2 * measure * gradient * gradient_rate)

    def native_direct(self, label):
        data = physical_data(self.native, self.loads, self.action, label)
        cardinal = decimals(data['cardinal'])
        field_direction = decimals(self.direction[:, :-1].T) @ cardinal
        source_direction = decimals(self.direction[:, -1]) @ cardinal
        edge_direction = decimals(self.edge_vertices.T) @ cardinal + data['displacement'] * source_direction
        atoms = self.native.atoms(data['edges'], data['field'])
        image = self.native.apply('template', self.native.kernel_values(data['edges'], atoms))
        tangent = self.native.tangent(data['edges'], data['field'], edge_direction, field_direction)
        return image, tangent, data, edge_direction, field_direction

    def prepare_native(self, degree, progress):
        labels = np.cos(np.arange(degree + 1) * np.pi / degree) / 2
        images, rates = [], []
        for index, label in enumerate(labels):
            if index % 8 == 0:
                progress('native-label-' + str(index) + '-of-' + str(degree + 1))
            image, tangent, unused, unused2, unused3 = self.native_direct(label)
            images.append(np.asarray(image, float))
            rates.append(np.asarray(tangent, float))
        self.image_coefficients = np.polynomial.chebyshev.chebfit(2 * labels, np.array(images), degree)
        self.image_direction_coefficients = np.polynomial.chebyshev.chebfit(2 * labels, np.array(rates), degree)
        return dict(labels=labels, images=np.array(images), derivatives=np.array(rates), image_coefficients=self.image_coefficients, image_direction_coefficients=self.image_direction_coefficients)

    def gram(self, radius, radius_rate, side=None):
        base, tangent = np.zeros_like(radius), np.zeros_like(radius)
        if self.extension == 'reference':
            return base, tangent
        coefficient_labels = 2 * np.polynomial.chebyshev.chebder(self.image_coefficients, axis=0)
        tolerance = 32 * np.finfo(float).eps * max(1., max(abs(self.action.solver.edges)))
        for index, reference in enumerate(self.loads.knots):
            start, end = self.loads.sampling.indptr[index:index + 2]
            if start == end:
                continue
            if side is None:
                lower, upper = self.material.node_geometry(reference, np.array([-.5, .5]))[0]
                selected = (radius >= lower) & (radius <= upper)
                labels = self.material.inverse_node(radius[selected], reference)
            else:
                selected, labels = traced_labels(self, radius, side, reference, tolerance)
            if not np.any(selected):
                continue
            unused, unused2, label_jacobian, displacement, unused3, unused4 = self.mapping(reference, labels)
            movement, unused, movement_label = self.movement(reference, labels)
            label_rate = (radius_rate[selected] - movement) / label_jacobian
            jacobian_rate = movement_label + displacement * self.source(labels)[2] * label_rate
            factors, weights = self.loads.sampling.indices[start:end], self.loads.sampling.data[start:end]
            image = np.polynomial.chebyshev.chebval(2 * labels, self.image_coefficients[:, factors])
            image_rate = np.polynomial.chebyshev.chebval(2 * labels, self.image_direction_coefficients[:, factors])
            image_rate += np.polynomial.chebyshev.chebval(2 * labels, coefficient_labels[:, factors]) * label_rate
            load = np.sum(weights[:, None] * image**2, axis=0) / 2
            load_rate = np.sum(weights[:, None] * image * image_rate, axis=0)
            value = material_weight(labels) * load / label_jacobian
            derivative = (material_weight(labels) * load_rate - 12 * labels * label_rate * load) / label_jacobian
            derivative -= value * jacobian_rate / label_jacobian
            base[selected] += value
            tangent[selected] += derivative
        return base, tangent

    def sample(self, radius, radius_rate=None, chunk_size=32, progress=lambda stage: None):
        return super().sample(radius, radius_rate, chunk_size, progress)

    def trace(self, radius, side):
        tolerance = 32 * np.finfo(float).eps * max(1., max(abs(self.action.solver.edges)))
        gram, gram_rate = self.gram(radius, np.zeros_like(radius), side)
        selected, labels = traced_labels(self, radius, side, self.owner.model.anchor, tolerance)
        unused, jacobian, second, direction, direction_label, velocity, velocity_label, unused2 = self.source(labels)
        label_rate = -direction / jacobian
        density = material_weight(labels) / jacobian
        source_rate, source_velocity, velocity_rate = [np.zeros(len(radius)) for unused in range(3)]
        source_rate[selected] = -12 * labels * label_rate / jacobian - density * (direction_label + second * label_rate) / jacobian
        source_velocity[selected], velocity_rate[selected] = velocity, velocity_label * label_rate
        return gram, gram_rate, source_rate, source_velocity, velocity_rate

    def weak(self, material_order):
        labels, weights = np.polynomial.legendre.leggauss(material_order)
        labels, weights = labels / 2, weights / 2
        weights *= material_weight(labels)
        points, spatial_weights = np.polynomial.legendre.leggauss(8)
        local = (points + 1) / 2
        model = self.owner.model
        widths = np.diff(model.edges)
        reference = model.edges[:-1, None] + widths[:, None] * local
        measure = widths[:, None] * spatial_weights / 2
        answer = np.zeros((4, 3))
        for label, weight in zip(labels, weights):
            cardinal = self.material.interpolation(np.array([label]))[0]
            coefficients = np.einsum('cpl,l->cp', self.material.gradient_coefficients, cardinal)
            direction = np.einsum('cpl,l->cp', self.direction_gradient, cardinal)
            rate_coefficients = np.einsum('cpl,l->cp', self.action.rate_polynomial, cardinal)
            radius, jacobian, unused, displacement, unused2, unused3 = self.mapping(reference, label)
            movement, jacobian_rate, unused = self.movement(reference, label)
            velocity = self.source(label)[5]
            gradient = (coefficients[:, :1] + coefficients[:, 1:] * local) / jacobian
            gradient_rate = (direction[:, :1] + direction[:, 1:] * local) / jacobian - gradient * jacobian_rate / jacobian
            rate = rate_coefficients[:, :1] + local * (rate_coefficients[:, 1:2] + local * rate_coefficients[:, 2:3])
            temporal = rate - displacement * velocity * gradient
            temporal_rate = -displacement * velocity * gradient_rate
            for power in range(3):
                profile = radius**power
                profile_rate = np.zeros_like(radius) if power == 0 else power * radius**(power - 1) * movement
                answer[0, power] += weight * np.sum(measure * (profile * (jacobian_rate * temporal**2 + 2 * jacobian * temporal * temporal_rate) + profile_rate * jacobian * temporal**2))
                answer[1, power] += weight * np.sum(measure * (profile * (jacobian_rate * gradient**2 + 2 * jacobian * gradient * gradient_rate) + profile_rate * jacobian * gradient**2))
            if self.extension != 'reference':
                image = np.polynomial.chebyshev.chebval(2 * label, self.image_coefficients)
                image_rate = np.polynomial.chebyshev.chebval(2 * label, self.image_direction_coefficients)
                load = np.asarray(self.loads.sampling.T @ (image**2 / 2)).ravel()
                load_rate = np.asarray(self.loads.sampling.T @ (image * image_rate)).ravel()
                radius = self.mapping(self.loads.knots, label)[0]
                movement = self.movement(self.loads.knots, label)[0]
                for power in range(3):
                    answer[2, power] += weight * np.sum(radius**power * load_rate)
                    if power:
                        answer[2, power] += weight * np.sum(power * radius**(power - 1) * movement * load)
            source, unused, unused2, source_direction, unused3, unused4, unused5, unused6 = self.source(label)
            for power in [1, 2]:
                answer[3, power] += weight * power * source**(power - 1) * source_direction
        return answer
