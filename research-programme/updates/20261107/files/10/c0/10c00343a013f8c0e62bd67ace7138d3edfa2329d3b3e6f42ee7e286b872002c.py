from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_background_time_tangent_20260928 import BackgroundLoads, interpolation_derivative, FIELD_NAMES
from annular_background_trace_20260928 import traced_labels
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
from annular_candidate_radial_constraint_20260920 import radial_rhs
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from time import perf_counter
import numpy as np


class CompensationLoads(BackgroundLoads):
    def __init__(self, loads, action, acceleration, directions, correction, transport_rate):
        super().__init__(loads, action, velocity_direction=acceleration)
        self.edges_direction = directions['edge_vertices']
        self.field_direction = directions['field_vertices'] - correction[:, :-1]
        self.field_direction_rate = transport_rate
        self.source_direction = -correction[:, -1]

    def mixed_wave(self, radius, freeze_cuts=False):
        rows, labels, label_rates, measure, measure_rate = self.label_partition(radius, np.zeros_like(radius), freeze_cuts)
        model = self.owner.model
        cardinal = self.material.interpolation(labels)
        cardinal_rate = interpolation_derivative(self.owner, labels) * label_rates[:, None]
        source, source_label, unused, direction, unused2, velocity, velocity_label, acceleration = self.source(labels)
        inner, outer = model.radii[0] + self.owner.width * labels, model.radii[-1] + self.owner.width * labels
        left = radius[rows] < source
        spatial = np.where(left, (source - inner) / (model.anchor - model.radii[0]),
            (outer - source) / (model.radii[-1] - model.anchor))
        reference = np.where(left, model.radii[0] + (radius[rows] - inner) / spatial,
            model.radii[-1] - (outer - radius[rows]) / spatial)
        unused, unused2, label_jacobian, displacement, slope, unused3 = self.mapping(reference, labels)
        reference_rate = (-displacement * direction - label_jacobian * label_rates) / spatial
        spatial_rate = slope * (direction + (source_label - self.owner.width) * label_rates)
        indices, shape, unused = model.features_quadratic(reference)
        cells = np.clip(np.searchsorted(model.edges, reference, side='right') - 1, 0, len(model.edges) - 2)
        widths = np.diff(model.edges)[cells]
        local = (reference - model.edges[cells]) / widths
        shape_reference = np.column_stack([4 * local - 3, 4 - 8 * local, 4 * local - 1]) / widths[:, None]
        shape_reference *= indices >= 0
        coefficients = np.einsum('ql,qpl->qp', cardinal, self.material.gradient_coefficients[cells], optimize=False)
        coefficient_rates = np.einsum('ql,qpl->qp', cardinal, self.direction_gradient[cells], optimize=False)
        coefficient_rates += np.einsum('ql,qpl->qp', cardinal_rate, self.material.gradient_coefficients[cells], optimize=False)
        gradient = (coefficients[:, 0] + coefficients[:, 1] * local) / spatial
        gradient_rate = (coefficient_rates[:, 0] + coefficient_rates[:, 1] * local + coefficients[:, 1] * reference_rate / widths) / spatial
        gradient_rate -= gradient * spatial_rate / spatial
        rate_nodes = indexed_label_values(cardinal, self.loads.rates[:, :-1], indices)
        rate_nodes_dot = indexed_label_values(cardinal_rate, self.loads.rates[:, :-1], indices)
        rate_nodes_dot += indexed_label_values(cardinal, self.velocity_direction[:, :-1], indices)
        temporal = np.sum(shape * rate_nodes, axis=1) - displacement * velocity * gradient
        temporal_rate = np.sum(shape * rate_nodes_dot + shape_reference * rate_nodes * reference_rate[:, None], axis=1)
        temporal_rate -= slope * reference_rate * velocity * gradient
        temporal_rate -= displacement * ((acceleration + velocity_label * label_rates) * gradient + velocity * gradient_rate)
        field_nodes = indexed_label_values(cardinal, self.field_direction, indices)
        field_nodes_dot = indexed_label_values(cardinal_rate, self.field_direction, indices)
        field_nodes_dot += indexed_label_values(cardinal, self.field_direction_rate, indices)
        field = np.sum(shape * field_nodes, axis=1)
        field_rate = np.sum(shape * field_nodes_dot + shape_reference * field_nodes * reference_rate[:, None], axis=1)
        edge_indices = np.column_stack([cells, cells + 1])
        edges = indexed_label_values(cardinal, self.edges_direction, edge_indices)
        edges_dot = indexed_label_values(cardinal_rate, self.edges_direction, edge_indices)
        source_direction = cardinal @ self.source_direction
        source_direction_rate = cardinal_rate @ self.source_direction
        movement = (1 - local) * edges[:, 0] + local * edges[:, 1] + displacement * source_direction
        movement_rate = (1 - local) * edges_dot[:, 0] + local * edges_dot[:, 1]
        movement_rate += (edges[:, 1] - edges[:, 0]) * reference_rate / widths
        movement_rate += slope * reference_rate * source_direction + displacement * source_direction_rate
        defect = field - movement * gradient
        defect_rate = field_rate - movement_rate * gradient - movement * gradient_rate
        outside = (radius[rows] < inner) | (radius[rows] > outer)
        for values in [temporal, temporal_rate, defect, defect_rate]:
            values[outside] = 0.
        aggregate = lambda values: np.bincount(rows, weights=values, minlength=len(radius))
        response = aggregate(2 * measure * temporal * defect)
        rate = aggregate(2 * (measure_rate * temporal * defect + measure * (temporal_rate * defect + temporal * defect_rate)))
        return response, rate

    def mixed_source(self, radius, side=None):
        if side is None:
            selected = (radius >= self.material.coordinates[0, -1]) & (radius <= self.material.coordinates[-1, -1])
            labels = self.material.inverse_node(radius[selected], self.owner.model.anchor)
        else:
            tolerance = 32 * np.finfo(float).eps * max(1., max(abs(radius)))
            selected, labels = traced_labels(self, radius, side, self.owner.model.anchor, tolerance)
        unused, jacobian, unused2, direction, unused3, unused4, unused5, unused6 = self.source(labels)
        cardinal = self.material.interpolation(labels)
        derivative = interpolation_derivative(self.owner, labels)
        response, rate = np.zeros(len(radius)), np.zeros(len(radius))
        response[selected] = cardinal @ self.source_direction
        rate[selected] = (derivative @ self.source_direction) * (-direction / jacobian)
        return response, rate

    def mixed_sample(self, solver, progress):
        radius = solver.nodes.ravel()
        response, rate = np.zeros(len(radius)), np.zeros(len(radius))
        for start in range(0, len(radius), 32):
            if perf_counter() > self.loads.deadline:
                raise RuntimeError('Safe mixed-density block boundary')
            section = slice(start, start + 32)
            response[section], rate[section] = self.mixed_wave(radius[section])
            if start % 4096 == 0:
                progress('mixed-density-' + str(start) + '-of-' + str(len(radius)))
        source, source_rate = self.mixed_source(radius)
        indices = np.arange(len(radius)).reshape(solver.nodes.shape)[:, [0, -1]].ravel()
        side = np.tile([1., -1.], len(solver.lengths))
        source[indices], source_rate[indices] = self.mixed_source(radius[indices], side)
        return dict(temporal=response, temporal_rate=rate, velocity=source, velocity_rate=source_rate)


def linear_solve(solver, local, forcing, outer_factor, boundary=0.):
    tangent = np.zeros((2, *solver.nodes.shape), dtype=np.result_type(local, forcing, boundary))
    history = []
    scale = max(float(np.max(abs(forcing))), abs(boundary), 1e-30)
    for iteration in range(80):
        rhs = np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing
        mass = solver.integrated(rhs[0])
        primitive = solver.integrated(rhs[1])
        lapse = -mass[-1, -1] / outer_factor + boundary + primitive - primitive[-1, -1]
        updated = np.stack([mass, lapse])
        error = float(np.max(abs(updated - tangent)))
        history.append(error)
        tangent = updated
        if error <= 2e-14 * scale:
            break
    else:
        raise RuntimeError('Mixed radial tangent failed to converge')
    rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(tangent.shape)
    integrated = np.array([solver.integrated(values.ravel()) for values in rhs])
    integrated[1] += boundary - integrated[1, -1, -1] - integrated[0, -1, -1] / outer_factor
    residual = float(np.max(abs(integrated - tangent)))
    return tangent, rhs, residual, history


def response_from_rhs(solver, state, rhs, forcing, outer_factor, boundary, residual, history):
    coefficients = rhs @ solver.rule.inverse.T
    primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T * solver.lengths[:, None] / 2 for values in coefficients])
    for component in range(2):
        primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
    increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
    outer = -sum(increments[0]) / outer_factor + boundary
    left = np.array([np.r_[0., np.cumsum(increments[0, :-1])],
        outer - sum(increments[1]) + np.r_[0., np.cumsum(increments[1, :-1])]])
    return MetricResponse(solver, dict(state=state, rhs_coefficients=coefficients, primitives=primitives, left=left), forcing, residual, history)


def mixed_radial(engine, action, background_archive, time_response, support_response, mixed):
    solver = support_response.solver
    radius = solver.nodes.ravel()
    state = action.solution['state'].reshape(2, -1)
    time_state = time_response.values(radius)
    fields = {key: background_archive['base_' + key] for key in FIELD_NAMES}
    rates = {key: background_archive['tangent_' + key].copy() for key in FIELD_NAMES}
    velocity_part = time_response.velocity
    velocity_state = velocity_part.solution['state'].reshape(2, -1)
    rates['temporal_square'] += engine.velocity_response_temporal
    rates['velocity'] += engine.velocity_response_velocity
    step = 1e-25
    changed_state = state + 1j * step * time_state
    changed_fields = {key: fields[key] + 1j * step * rates[key] for key in FIELD_NAMES}
    unused, local = radial_rhs(radius, *state, *[fields[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass, True)
    unused, changed_local = radial_rhs(radius, *changed_state, *[changed_fields[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass, True)
    zeros = np.zeros(len(radius))
    forcing = explicit_time_forcing(radius, *state, fields['source_density'], fields['velocity'],
        mixed['temporal'], zeros, zeros, zeros, mixed['velocity'], engine.owner.coupling, engine.owner.source_mass)
    changed_forcing = explicit_time_forcing(radius, *changed_state, changed_fields['source_density'], changed_fields['velocity'],
        mixed['temporal'] + 1j * step * mixed['temporal_rate'], zeros, zeros, zeros,
        mixed['velocity'] + 1j * step * mixed['velocity_rate'], engine.owner.coupling, engine.owner.source_mass)
    mixed_forcing = np.einsum('abn,bn->an', changed_local.imag / step, support_response.solution['state'].reshape(2, -1))
    mixed_forcing += changed_forcing.imag / step
    outer_factor = solver.edges[-1] - 2 * state[0, -1]
    boundary = -2 * time_state[0, -1] * support_response.solution['state'][0, -1, -1] / outer_factor**2
    tangent, rhs, residual, history = linear_solve(solver, local, mixed_forcing, outer_factor, boundary)
    response = response_from_rhs(solver, tangent, rhs, mixed_forcing, outer_factor, boundary, residual, history)
    complex_state, unused, complex_residual, unused2 = linear_solve(solver, changed_local, changed_forcing,
        outer_factor - 2j * step * time_state[0, -1])
    response.complex_check = complex_state.imag / step
    response.complex_residual = complex_residual
    response.boundary = boundary
    response.local, response.forcing_rate = local, changed_forcing.imag / step
    response.base_forcing = forcing
    response.field_rates = rates
    return response


def dust_response(radius, mass, nu, velocity, source_mass, source_direction, metric_direction):
    metric, lapse = 1 - 2 * mass / radius, np.exp(nu)
    clock_square = lapse**2 - velocity**2 / metric
    inertia = source_mass * lapse**2 / (metric * clock_square**1.5)
    momentum = source_mass * velocity / (metric * np.sqrt(clock_square))
    partial_mass = momentum * (2 / (radius * metric) + velocity**2 / (radius * metric**2 * clock_square))
    partial_nu = -momentum * lapse**2 / clock_square
    return inertia * source_direction + partial_mass * metric_direction[0] + partial_nu * metric_direction[1]


def material_derivative(engine, action, time_response, support_response, mixed_response, order):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    base = np.zeros_like(engine.loads.rates)
    derivative = np.zeros_like(base)
    complex_derivative = np.zeros_like(base)
    direct_derivative = np.zeros_like(base)
    step = 1e-25
    reference_edges = np.array([float(value) for value in action.edges])
    for label, weight in zip(labels, weights):
        if perf_counter() > engine.loads.deadline:
            raise RuntimeError('Safe material compensation derivative boundary')
        row = samples(action, label, 12)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        radius, spatial = geometry['radius'], geometry['jacobian']
        cells, local = quad['cells'], quad['local']
        indices = np.array(action.mesh['elements'])[cells]
        widths = np.diff(reference_edges)[cells] * spatial
        values, radial = action.solver.values(action.solution, radius)
        speed = geometry['displacement'] * row['velocity']
        speed_radial = geometry['jacobian_source'] * row['velocity'] / spatial
        material_metric_rate = time_response.values(radius) + radial * speed
        metric, lapse = geometry['metric'], geometry['lapse']
        metric_rate = -2 * material_metric_rate[0] / radius + 2 * values[0] * speed / radius**2
        alpha = radius**2 / (lapse * np.sqrt(metric))
        alpha_ratio = 2 * speed / radius - material_metric_rate[1] - metric_rate / (2 * metric)
        gradient = row['gradient'] / spatial
        gradient_rate = row['rate_gradient'] / spatial - speed_radial * gradient
        temporal_rate = interpolate_nodal(cardinal @ engine.velocity_direction[:, :-1], indices, local, widths)[0]
        temporal_rate += row['motion'] * (cardinal @ engine.velocity_direction[:, -1]) + row['motion_rate'] * row['velocity']
        edge_values = cardinal @ engine.edges_direction
        source_direction = float(cardinal @ engine.source_direction)
        movement = (1 - local) * edge_values[cells] + local * edge_values[cells + 1] + geometry['displacement'] * source_direction
        field = interpolate_nodal(cardinal @ engine.field_direction, indices, local, widths)[0]
        field_rate = interpolate_nodal(cardinal @ engine.field_direction_rate, indices, local, widths)[0]
        defect = field - movement * gradient
        defect_rate = field_rate - movement * gradient_rate
        variation, variation_radial = support_response.solver.values(support_response.solution, radius)
        variation_rate = mixed_response.values(radius) + variation_radial * speed
        ratio = variation[0] / (radius * metric) - variation[1]
        ratio_rate = variation_rate[0] / (radius * metric) - variation[0] * (speed * metric + radius * metric_rate) / (radius * metric)**2 - variation_rate[1]
        measure = quad['measure'] * spatial * alpha
        density = measure * (defect + row['temporal'] * ratio)
        density_rate = measure * ((speed_radial + alpha_ratio) * (defect + row['temporal'] * ratio)
            + defect_rate + temporal_rate * ratio + row['temporal'] * ratio_rate)
        direct_rate = measure * ((speed_radial + alpha_ratio) * defect + defect_rate)
        amount = 1j * step
        changed_radius = radius + amount * speed
        changed_metric = 1 - 2 * (values[0] + amount * material_metric_rate[0]) / changed_radius
        changed_alpha = changed_radius**2 / (np.exp(values[1] + amount * material_metric_rate[1]) * np.sqrt(changed_metric))
        changed_variation = variation + amount * variation_rate
        changed_ratio = changed_variation[0] / (changed_radius * changed_metric) - changed_variation[1]
        changed_density = quad['measure'] * spatial * (1 + amount * speed_radial) * changed_alpha
        changed_density *= defect + amount * defect_rate + (row['temporal'] + amount * temporal_rate) * changed_ratio
        source_radius = np.array([row['source']])
        source_values, source_radial = action.solver.values(action.solution, source_radius)
        source_time = time_response.values(source_radius) + source_radial * row['velocity']
        source_variation, source_variation_radial = support_response.solver.values(support_response.solution, source_radius)
        source_variation_rate = mixed_response.values(source_radius) + source_variation_radial * row['velocity']
        dust = dust_response(row['source'], *source_values[:, 0], row['velocity'], action.owner.source_mass, source_direction, source_variation[:, 0])
        changed_dust = dust_response(row['source'] + amount * row['velocity'],
            *(source_values[:, 0] + amount * source_time[:, 0]), row['velocity'] + amount * (cardinal @ engine.velocity_direction[:, -1]),
            action.owner.source_mass, source_direction, source_variation[:, 0] + amount * source_variation_rate[:, 0])
        direct_dust = dust_response(row['source'] + amount * row['velocity'],
            *(source_values[:, 0] + amount * source_time[:, 0]), row['velocity'] + amount * (cardinal @ engine.velocity_direction[:, -1]),
            action.owner.source_mass, source_direction, np.zeros(2))
        selected = indices >= 0
        for target, wave, source in [
            (base, density, density @ row['motion'] + dust),
            (derivative, density_rate, density_rate @ row['motion'] + density @ row['motion_rate'] + changed_dust.imag / step),
            (complex_derivative, changed_density.imag / step,
                ((changed_density @ (row['motion'] + amount * row['motion_rate'])) + changed_dust).imag / step),
            (direct_derivative, direct_rate, direct_rate @ row['motion'] + (measure * defect) @ row['motion_rate'] + direct_dust.imag / step)]:
            field_covector = np.zeros(base.shape[1] - 1)
            terms = wave[:, None] * row['shape']
            np.add.at(field_covector, indices[selected], terms[selected])
            target += weight * np.outer(cardinal, np.r_[field_covector, source])
    return dict(base=base, derivative=derivative, complex_derivative=complex_derivative,
        fixed_metric_derivative=direct_derivative, metric_feedback_derivative=derivative - direct_derivative)


class OldResponse:
    def __init__(self, response):
        self.response = response

    def apply(self, direction):
        return self.response.apply(direction, 0.)
