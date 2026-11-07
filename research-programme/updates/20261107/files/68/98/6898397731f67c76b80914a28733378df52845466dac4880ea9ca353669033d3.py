from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_candidate_canonical_response_20260920 import solve_tangent
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from decimal import localcontext
from copy import copy
from time import perf_counter
import numpy as np


FIELD_NAMES = ['temporal_square', 'gradient_square', 'gram', 'source_density', 'velocity']


def interpolation_derivative(owner, labels):
    return np.polynomial.chebyshev.chebval(2 * labels,
        2 * np.polynomial.chebyshev.chebder(owner.layer_rule.inverse, axis=0)).T


class BackgroundLoads:
    def __init__(self, loads, action, coordinate_direction=None, velocity_direction=None):
        self.loads, self.action = loads, action
        self.owner, self.material = loads.owner, loads.material
        self.direction = loads.rates if coordinate_direction is None else coordinate_direction
        self.velocity_direction = np.zeros_like(loads.rates) if velocity_direction is None else velocity_direction
        self.extension = 'reference' if not loads.factor.shape[0] else 'primary'
        with localcontext() as context:
            context.prec = 64
            unused, self.direction_gradient = local_polynomials(action.mesh, decimal_array(self.direction[:, :-1].T))
            unused, self.rate_gradient = local_polynomials(action.mesh, decimal_array(loads.rates[:, :-1].T))
            self.factor_direction = np.asarray(loads.factor.apply(decimal_array(self.direction[:, :-1].T)).T, float)
        self.factor_direction_coefficients = self.owner.layer_rule.inverse @ self.factor_direction
        self.source_direction_coefficients = self.owner.layer_rule.inverse @ self.direction[:, -1]
        self.source_rate_coefficients = self.owner.layer_rule.inverse @ loads.rates[:, -1]
        self.source_velocity_direction_coefficients = self.owner.layer_rule.inverse @ self.velocity_direction[:, -1]

    def source(self, labels):
        base = self.material.coefficients[:, -1]
        value = lambda coeff: np.polynomial.chebyshev.chebval(2 * labels, coeff)
        first = lambda coeff: value(2 * np.polynomial.chebyshev.chebder(coeff))
        return (value(base), first(base), value(4 * np.polynomial.chebyshev.chebder(base, 2)),
            value(self.source_direction_coefficients), first(self.source_direction_coefficients),
            value(self.source_rate_coefficients), first(self.source_rate_coefficients),
            value(self.source_velocity_direction_coefficients))

    def mapping(self, reference, labels):
        model = self.owner.model
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        slope = np.where(reference < model.anchor, 1 / (model.anchor - model.radii[0]),
            -1 / (model.radii[-1] - model.anchor))
        source, source_label, unused3, direction, unused4, unused5, unused6, unused7 = self.source(labels)
        spatial = 1 + slope * (source - model.anchor - self.owner.width * labels)
        label_jacobian = (1 - displacement) * self.owner.width + displacement * source_label
        position = reference + displacement * (source - model.anchor) + (1 - displacement) * self.owner.width * labels
        return position, spatial, label_jacobian, displacement, slope, direction

    def label_partition(self, radius, radius_rate, freeze_cuts=False):
        model = self.owner.model
        endpoints = np.array([self.material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
        rows, columns = np.nonzero((radius[:, None] > endpoints[0]) & (radius[:, None] < endpoints[1]))
        counts = np.bincount(rows, minlength=len(radius))
        starts = np.cumsum(counts) - counts
        local = np.arange(len(rows)) - np.repeat(starts, counts)
        cuts = np.full((len(radius), int(max(counts)) + 2), np.nan)
        cut_rates = np.zeros_like(cuts)
        cuts[:, :2] = [-.5, .5]
        labels = self.material.inverse_node(radius[rows], model.edges[columns])
        unused, unused2, label_jacobian, displacement, unused3, direction = self.mapping(model.edges[columns], labels)
        cuts[rows, local + 2] = labels
        cut_rates[rows, local + 2] = (radius_rate[rows] - displacement * direction) / label_jacobian
        order = np.argsort(cuts, axis=1)
        cuts = np.take_along_axis(cuts, order, axis=1)
        cut_rates = np.take_along_axis(cut_rates, order, axis=1)
        lengths = np.diff(cuts, axis=1)
        segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths > 1e-13))
        lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
        lower_rate, upper_rate = cut_rates[segment_rows, segment_columns], cut_rates[segment_rows, segment_columns + 1]
        if freeze_cuts:
            lower_rate, upper_rate = np.zeros_like(lower_rate), np.zeros_like(upper_rate)
        points, weights = np.polynomial.legendre.leggauss(self.owner.label_order)
        labels = (lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2
        label_rates = (lower_rate[:, None] + upper_rate[:, None]) / 2 + (upper_rate - lower_rate)[:, None] * points / 2
        base_measure = (upper - lower)[:, None] * weights / 2
        measure = base_measure * material_weight(labels)
        measure_rate = (upper_rate - lower_rate)[:, None] * weights * material_weight(labels) / 2
        measure_rate -= base_measure * 12 * labels * label_rates
        return np.repeat(segment_rows, len(points)), labels.ravel(), label_rates.ravel(), measure.ravel(), measure_rate.ravel()

    def wave(self, radius, radius_rate, freeze_cuts=False):
        rows, labels, label_rates, measure, measure_rate = self.label_partition(radius, radius_rate, freeze_cuts)
        model = self.owner.model
        interpolation = self.material.interpolation(labels)
        interpolation_rate = interpolation_derivative(self.owner, labels) * label_rates[:, None]
        source, source_label, unused, direction, unused2, velocity, velocity_label, velocity_direction = self.source(labels)
        inner, outer = model.radii[0] + self.owner.width * labels, model.radii[-1] + self.owner.width * labels
        left = radius[rows] < source
        spatial = np.where(left, (source - inner) / (model.anchor - model.radii[0]),
            (outer - source) / (model.radii[-1] - model.anchor))
        reference = np.where(left, model.radii[0] + (radius[rows] - inner) / spatial,
            model.radii[-1] - (outer - radius[rows]) / spatial)
        unused, unused2, label_jacobian, displacement, slope, unused3 = self.mapping(reference, labels)
        reference_rate = (radius_rate[rows] - displacement * direction - label_jacobian * label_rates) / spatial
        spatial_rate = slope * (direction + (source_label - self.owner.width) * label_rates)
        indices, shape, shape_radial = model.features_quadratic(reference)
        cells = np.clip(np.searchsorted(model.edges, reference, side='right') - 1, 0, len(model.edges) - 2)
        widths = np.diff(model.edges)[cells]
        local = (reference - model.edges[cells]) / widths
        interpolate = lambda values, basis=interpolation: np.einsum('ql,qpl->qp', basis, values[cells], optimize=False)
        coefficients = interpolate(self.material.gradient_coefficients)
        coefficient_rates = interpolate(self.direction_gradient) + interpolate(self.material.gradient_coefficients, interpolation_rate)
        gradient = (coefficients[:, 0] + coefficients[:, 1] * local) / spatial
        gradient_rate = (coefficient_rates[:, 0] + coefficient_rates[:, 1] * local + coefficients[:, 1] * reference_rate / widths) / spatial
        gradient_rate -= gradient * spatial_rate / spatial
        sampled_rates = indexed_label_values(interpolation, self.loads.rates[:, :-1], indices)
        sampled_rate_derivatives = indexed_label_values(interpolation_rate, self.loads.rates[:, :-1], indices)
        sampled_rate_derivatives += indexed_label_values(interpolation, self.velocity_direction[:, :-1], indices)
        rate_coefficients = interpolate(self.rate_gradient)
        temporal = np.sum(shape * sampled_rates, axis=1) - displacement * velocity * gradient
        temporal_rate = np.sum(shape * sampled_rate_derivatives, axis=1)
        temporal_rate += (rate_coefficients[:, 0] + rate_coefficients[:, 1] * local) * reference_rate
        temporal_rate -= slope * reference_rate * velocity * gradient
        temporal_rate -= displacement * ((velocity_direction + velocity_label * label_rates) * gradient + velocity * gradient_rate)
        outside = (radius[rows] < inner) | (radius[rows] > outer)
        for values in [gradient, gradient_rate, temporal, temporal_rate]:
            values[outside] = 0.
        reduce = lambda values: np.bincount(rows, weights=values, minlength=len(radius))
        return (reduce(measure * temporal**2), reduce(measure * gradient**2),
            reduce(measure_rate * temporal**2 + 2 * measure * temporal * temporal_rate),
            reduce(measure_rate * gradient**2 + 2 * measure * gradient * gradient_rate))

    def gram(self, radius, radius_rate):
        base, tangent = np.zeros_like(radius), np.zeros_like(radius)
        if self.extension == 'reference':
            return base, tangent
        coefficients = self.loads.factor_coefficients[self.extension]
        coefficient_labels = 2 * np.polynomial.chebyshev.chebder(coefficients, axis=0)
        for index, reference in enumerate(self.loads.knots):
            start, end = self.loads.sampling.indptr[index:index + 2]
            if start == end:
                continue
            lower, upper = self.material.node_geometry(reference, np.array([-.5, .5]))[0]
            selected = (radius >= lower) & (radius <= upper)
            if not np.any(selected):
                continue
            labels = self.material.inverse_node(radius[selected], reference)
            unused, spatial, label_jacobian, displacement, slope, direction = self.mapping(reference, labels)
            source, source_label, source_label2, unused, direction_label, unused2, unused3, unused4 = self.source(labels)
            label_rate = (radius_rate[selected] - displacement * direction) / label_jacobian
            spatial_rate = slope * (direction + (source_label - self.owner.width) * label_rate)
            jacobian_rate = displacement * (direction_label + source_label2 * label_rate)
            factors, weights = self.loads.sampling.indices[start:end], self.loads.sampling.data[start:end]
            image = np.polynomial.chebyshev.chebval(2 * labels, coefficients[:, factors])
            image_rate = np.polynomial.chebyshev.chebval(2 * labels, self.factor_direction_coefficients[:, factors])
            image_rate += np.polynomial.chebyshev.chebval(2 * labels, coefficient_labels[:, factors]) * label_rate
            load = np.sum(weights[:, None] * image**2, axis=0) / 2
            load_rate = np.sum(weights[:, None] * image * image_rate, axis=0)
            measure = material_weight(labels)
            value = measure * load / (spatial * label_jacobian)
            derivative = (measure * load_rate - 12 * labels * label_rate * load) / (spatial * label_jacobian)
            derivative -= value * (spatial_rate / spatial + jacobian_rate / label_jacobian)
            base[selected] += value
            tangent[selected] += derivative
        return base, tangent

    def sample(self, radius, radius_rate=None, chunk_size=32, progress=lambda stage: None):
        radius = np.asarray(radius).ravel()
        radius_rate = np.zeros_like(radius) if radius_rate is None else np.asarray(radius_rate).ravel()
        fields = {name: np.zeros(len(radius)) for name in FIELD_NAMES}
        rates = {name: np.zeros(len(radius)) for name in FIELD_NAMES}
        for start in range(0, len(radius), chunk_size):
            if perf_counter() > self.loads.deadline:
                raise RuntimeError('Safe boundary in direct background-time density assembly')
            section = slice(start, start + chunk_size)
            temporal, gradient, temporal_rate, gradient_rate = self.wave(radius[section], radius_rate[section])
            fields['temporal_square'][section], fields['gradient_square'][section] = temporal, gradient
            rates['temporal_square'][section], rates['gradient_square'][section] = temporal_rate, gradient_rate
            if start % 4096 == 0:
                progress('analytic-density-' + str(start) + '-of-' + str(len(radius)))
        fields['gram'], rates['gram'] = self.gram(radius, radius_rate)
        selected = (radius >= self.material.coordinates[0, -1]) & (radius <= self.material.coordinates[-1, -1])
        labels = self.material.inverse_node(radius[selected], self.owner.model.anchor)
        unused, jacobian, second, direction, direction_label, velocity, velocity_label, velocity_direction = self.source(labels)
        label_rate = (radius_rate[selected] - direction) / jacobian
        density = material_weight(labels) / jacobian
        fields['source_density'][selected] = density
        fields['velocity'][selected] = velocity
        rates['source_density'][selected] = -12 * labels * label_rate / jacobian
        rates['source_density'][selected] -= density * (direction_label + second * label_rate) / jacobian
        rates['velocity'][selected] = velocity_direction + velocity_label * label_rate
        return fields, rates

    def moving_edges(self, archived_edges):
        active = np.asarray(abs(self.loads.sampling).sum(axis=0)).ravel() > 0
        references = np.unique(np.r_[self.owner.model.edges, self.loads.knots[active]])
        positions, rates = [], []
        for label in [-.5, .5]:
            position, unused, unused2, displacement, unused3, direction = self.mapping(references, label)
            positions.extend(position)
            rates.extend(displacement * direction)
        positions, rates = np.array(positions), np.array(rates)
        order = np.argsort(positions)
        positions, rates = positions[order], rates[order]
        tolerance = 32 * np.finfo(float).eps * max(1., max(abs(positions)))
        starts = [0]
        for index in range(1, len(positions)):
            if positions[index] - positions[starts[-1]] > tolerance:
                starts.append(index)
        starts.append(len(positions))
        edges = np.array([np.mean(positions[lower:upper]) for lower, upper in zip(starts[:-1], starts[1:])])
        edge_rates = np.array([np.mean(rates[lower:upper]) for lower, upper in zip(starts[:-1], starts[1:])])
        spread = max(np.ptp(rates[lower:upper]) for lower, upper in zip(starts[:-1], starts[1:]))
        if edges.shape != archived_edges.shape or np.max(abs(edges - archived_edges)) > tolerance:
            raise RuntimeError('Moving-grid topology does not replay the archived grid')
        if spread > 5e-13 * max(1., np.max(abs(edge_rates))):
            raise RuntimeError('Merged radial interfaces have incompatible velocities')
        if np.max(abs(edge_rates[[0, -1]])) > 1e-15:
            raise RuntimeError('This tangent requires fixed physical outer boundaries')
        return edge_rates, float(spread)


class MovingGridMetricResponse(MetricResponse):
    def __init__(self, solver, solution, forcing, residual, history, base_solution, edge_rates):
        super().__init__(solver, solution, forcing, residual, history)
        self.base_solution, self.edge_rates = base_solution, edge_rates

    def grid_velocity(self, radius):
        return np.interp(radius, self.solver.edges, self.edge_rates)

    def values(self, radius):
        radius = np.asarray(radius)
        moving = self.solver.values(self.solution, radius)[0]
        radial = self.solver.values(self.base_solution, radius)[1]
        return moving - radial * self.grid_velocity(radius)


def assemble_background(engine, action, progress):
    solver = copy(action.solver)
    solver.loads, solver.owner = engine.loads, engine.owner
    solver.rule, solver.label_order = ChebyshevRule(22), 28
    engine.owner.label_order = solver.label_order
    solver.nodes = solver.centers[:, None] + solver.lengths[:, None] * solver.rule.points / 2
    edge_rates, spread = engine.moving_edges(solver.edges)
    length_rates = np.diff(edge_rates)
    center_rates = (edge_rates[1:] + edge_rates[:-1]) / 2
    grid_rate = center_rates[:, None] + length_rates[:, None] * solver.rule.points / 2
    fields, field_rates = engine.sample(solver.nodes.ravel(), grid_rate.ravel(), progress=progress)
    solver.fields = dict(fields, gram={engine.extension: fields['gram']})
    state = action.solution['state']
    radius, radial_rate = solver.nodes.ravel(), grid_rate.ravel()
    mass, lapse = state.reshape(2, -1)
    explicit = explicit_time_forcing(radius, mass, lapse, fields['source_density'], fields['velocity'],
        *[field_rates[name] for name in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
    step = 1e-28
    radial_partial = radial_rhs(radius + 1j * step * radial_rate, mass, lapse,
        *[fields[name] for name in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass).imag / step
    rhs, local = solver.rhs(state, engine.extension, True)
    forcing = explicit + radial_partial + rhs * np.repeat(length_rates / solver.lengths, solver.nodes.shape[1])
    tangent, residual, history = solve_tangent(solver, state, engine.extension, forcing)
    derivative_rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(2, *solver.nodes.shape)
    coefficients = derivative_rhs @ solver.rule.inverse.T
    primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T * solver.lengths[:, None] / 2 for values in coefficients])
    for component in range(2):
        primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
    increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
    outer = -sum(increments[0]) / (solver.edges[-1] - 2 * state[0, -1, -1])
    left = np.array([np.r_[0., np.cumsum(increments[0, :-1])],
        outer - sum(increments[1]) + np.r_[0., np.cumsum(increments[1, :-1])]])
    solution = dict(state=tangent, rhs_coefficients=coefficients, primitives=primitives, left=left)
    response = MovingGridMetricResponse(solver, solution, forcing, residual, history, action.solution, edge_rates)
    response.fields, response.field_rates, response.grid_rate = fields, field_rates, grid_rate
    response.edge_velocity_spread = spread
    response.background_residual = float(np.max(abs(solver.residual(state, engine.extension))))
    return response
