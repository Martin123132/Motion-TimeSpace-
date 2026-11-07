from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_canonical_response_20260920 import solve_tangent
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_radial_time_forcing_20260928 import explicit_time_forcing
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_background_time_tangent_20260928 import FIELD_NAMES
import numpy as np


def traced_labels(engine, radius, side, reference, tolerance):
    lower, upper = engine.material.node_geometry(reference, np.array([-.5, .5]))[0]
    near_lower, near_upper = abs(radius - lower) <= tolerance, abs(radius - upper) <= tolerance
    selected = (radius > lower) & (radius < upper)
    selected |= (near_lower & (side > 0)) | (near_upper & (side < 0))
    selected &= ~((near_lower & (side < 0)) | (near_upper & (side > 0)))
    labels = engine.material.inverse_node(radius[selected], reference)
    labels[near_lower[selected]], labels[near_upper[selected]] = -.5, .5
    return selected, labels


def endpoint_traces(engine, radius, side, tolerance):
    gram_rate = np.zeros(len(radius))
    if engine.extension != 'reference':
        coefficients = engine.loads.factor_coefficients[engine.extension]
        coefficient_labels = 2 * np.polynomial.chebyshev.chebder(coefficients, axis=0)
        for index, reference in enumerate(engine.loads.knots):
            start, end = engine.loads.sampling.indptr[index:index + 2]
            if start == end:
                continue
            selected, labels = traced_labels(engine, radius, side, reference, tolerance)
            if not np.any(selected):
                continue
            unused, spatial, label_jacobian, displacement, slope, direction = engine.mapping(reference, labels)
            unused, source_label, second, unused2, direction_label, unused3, unused4, unused5 = engine.source(labels)
            label_rate = -displacement * direction / label_jacobian
            spatial_rate = slope * (direction + (source_label - engine.owner.width) * label_rate)
            jacobian_rate = displacement * (direction_label + second * label_rate)
            factors, weights = engine.loads.sampling.indices[start:end], engine.loads.sampling.data[start:end]
            image = np.polynomial.chebyshev.chebval(2 * labels, coefficients[:, factors])
            image_rate = np.polynomial.chebyshev.chebval(2 * labels, engine.factor_direction_coefficients[:, factors])
            image_rate += np.polynomial.chebyshev.chebval(2 * labels, coefficient_labels[:, factors]) * label_rate
            load = np.sum(weights[:, None] * image**2, axis=0) / 2
            load_rate = np.sum(weights[:, None] * image * image_rate, axis=0)
            density = material_weight(labels) * load / (spatial * label_jacobian)
            derivative = (material_weight(labels) * load_rate - 12 * labels * label_rate * load) / (spatial * label_jacobian)
            derivative -= density * (spatial_rate / spatial + jacobian_rate / label_jacobian)
            gram_rate[selected] += derivative
    selected, labels = traced_labels(engine, radius, side, engine.owner.model.anchor, tolerance)
    unused, jacobian, second, direction, direction_label, velocity, velocity_label, velocity_direction = engine.source(labels)
    label_rate = -direction / jacobian
    density = material_weight(labels) / jacobian
    source_rate, source_velocity, source_velocity_rate = [np.zeros(len(radius)) for unused in range(3)]
    source_rate[selected] = -12 * labels * label_rate / jacobian - density * (direction_label + second * label_rate) / jacobian
    source_velocity[selected] = velocity
    source_velocity_rate[selected] = velocity_direction + velocity_label * label_rate
    return gram_rate, source_rate, source_velocity, source_velocity_rate


def repair_background(engine, action, archive):
    solver, unused = reconstructed_solver(archive)
    solver.rule, solver.nodes = ChebyshevRule(22), archive['nodes']
    solver.loads, solver.owner = engine.loads, engine.owner
    fields = {key: archive['base_' + key].copy() for key in FIELD_NAMES}
    field_rates = {key: archive['tangent_' + key].copy() for key in FIELD_NAMES}
    indices = np.arange(solver.nodes.size).reshape(solver.nodes.shape)[:, [0, -1]].ravel()
    side = np.tile([1., -1.], len(solver.lengths))
    tolerance = 32 * np.finfo(float).eps * max(1., max(abs(solver.edges)))
    gram_rate, source_rate, source_velocity, source_velocity_rate = endpoint_traces(engine, solver.nodes.ravel()[indices], side, tolerance)
    field_rates['gram'][indices], field_rates['source_density'][indices] = gram_rate, source_rate
    field_rates['velocity'][indices], fields['velocity'][indices] = source_velocity_rate, source_velocity
    solver.fields = dict(fields, gram={engine.extension: fields['gram']})
    state = action.solution['state']
    forcing = explicit_time_forcing(solver.nodes.ravel(), *state.reshape(2, -1), fields['source_density'], fields['velocity'],
        *[field_rates[key] for key in FIELD_NAMES], engine.owner.coupling, engine.owner.source_mass)
    tangent, residual, history = solve_tangent(solver, state, engine.extension, forcing)
    unused, local = solver.rhs(state, engine.extension, True)
    rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(2, *solver.nodes.shape)
    coefficients = rhs @ solver.rule.inverse.T
    primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T * solver.lengths[:, None] / 2 for values in coefficients])
    for component in range(2):
        primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
    increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
    outer = -sum(increments[0]) / (solver.edges[-1] - 2 * state[0, -1, -1])
    left = np.array([np.r_[0., np.cumsum(increments[0, :-1])],
        outer - sum(increments[1]) + np.r_[0., np.cumsum(increments[1, :-1])]])
    response = MetricResponse(solver, dict(state=tangent, rhs_coefficients=coefficients, primitives=primitives, left=left), forcing, residual, history)
    response.fields, response.field_rates = fields, field_rates
    response.background_residual = float(np.max(abs(solver.residual(state, engine.extension))))
    return response
