import numpy as numerical
from scipy.linalg import solve, svd, lstsq

from annular_canonical_rate_completion_20260911 import normalized_transform


class GlobalPrimitive:
    def __init__(self, knots, values, order):
        self.knots = knots
        nodes, weights = numerical.polynomial.legendre.leggauss(order)
        matrix = numerical.polynomial.legendre.legvander(nodes, order - 1)
        coefficients = solve(matrix, values.reshape(knots.size - 1, order).T)
        self.integrals = numerical.polynomial.legendre.legint(coefficients, axis=0)
        self.left_value = numerical.polynomial.legendre.legval(-1., self.integrals)
        cell_integrals = numerical.diff(knots) / 2 * (values.reshape(knots.size - 1, order) @ weights)
        self.prefix = numerical.concatenate([[0.], numerical.cumsum(cell_integrals)])

    def evaluate(self, points):
        segment = numerical.clip(numerical.searchsorted(self.knots, points, side='right') - 1, 0, self.knots.size - 2)
        halfwidth = (self.knots[segment + 1] - self.knots[segment]) / 2
        fraction = (points - (self.knots[segment] + self.knots[segment + 1]) / 2) / halfwidth
        matrix = numerical.polynomial.legendre.legvander(fraction, self.integrals.shape[0] - 1)
        local = numerical.sum(matrix * self.integrals[:, segment].T, axis=1) - self.left_value[segment]
        return self.prefix[segment] + halfwidth * local


def kernel_family(context, data, frame, momentum_coeff, order=12, surface='quad'):
    values = data[surface]
    momentum_time = frame[surface]['p'] @ momentum_coeff
    generator = .1 * numerical.sqrt(values['F']) * momentum_time / values['N']
    primitive = GlobalPrimitive(context.knots, generator, order)
    family, carrier = {}, {}
    for name, points in context.surfaces.items():
        current = data[name]
        multiplier = .1 * numerical.sqrt(current['F']) / current['N'] * numerical.exp(-2 * primitive.evaluate(points))
        cell = numerical.clip(numerical.searchsorted(context.basis.radii, points, side='right') - 1, 0, context.basis.radii.size - 2)
        matrix = numerical.zeros((points.size, context.basis.radii.size - 1))
        matrix[numerical.arange(points.size), cell] = multiplier
        family[name] = matrix
        carrier[name] = multiplier
    return family, primitive, carrier


def trace_extension(context, base, family):
    weights = context.weights
    coordinate, momentum = base['quad']['q'], base['quad']['p']
    pairing = momentum.T @ (weights[:, None] * coordinate)
    coordinate_gram = coordinate.T @ (weights[:, None] * coordinate)
    family_scale = numerical.sqrt(weights @ family['quad']**2)
    projection = solve(coordinate_gram, coordinate.T @ (weights[:, None] * (family['quad'] / family_scale)))
    residual = family['quad'] / family_scale - coordinate @ projection
    unused_left, singular, right = svd(numerical.sqrt(weights)[:, None] * residual, full_matrices=False)
    if singular[-1] < 1e-13:
        raise ValueError('Full parent cell-kernel family has unresolved numerical rank; no force mode is discarded.')
    weak_coefficients = solve(pairing, momentum.T @ (weights[:, None] * family['quad']))
    endpoint_map = base['nodes']['q'][[0, -1]]
    discrepancy = family['nodes'][[0, -1]] - endpoint_map @ weak_coefficients
    residual_basis = {}
    for surface in base:
        residual_basis[surface] = ((family[surface] / family_scale - base[surface]['q'] @ projection) @ right.T) / singular
    for unused_pass in range(2):
        correction = solve(coordinate_gram, coordinate.T @ (weights[:, None] * residual_basis['quad']))
        for surface in base:
            residual_basis[surface] -= base[surface]['q'] @ correction
    normalization = normalized_transform(residual_basis['quad'], weights)
    for surface in base:
        residual_basis[surface] = residual_basis[surface] @ normalization
    family_moments = residual_basis['quad'].T @ (weights[:, None] * (family['quad'] / family_scale))
    representer_coefficients = solve(family_moments.T, (discrepancy / family_scale).T)
    raw_momentum = {}
    for surface in base:
        raw_momentum[surface] = residual_basis[surface] @ representer_coefficients
    momentum_transform = normalized_transform(raw_momentum['quad'], weights)
    new_momentum = {surface: value @ momentum_transform for surface, value in raw_momentum.items()}
    trace_target = solve(momentum_transform.T, numerical.eye(2))
    bubble_scale = numerical.sqrt(weights @ context.reservoir['quad']['q']**2)
    endpoint_hats, endpoint_hat_gradients = {}, {}
    for surface, points in context.surfaces.items():
        from annular_adm_mixed_action_20260909 import linear_value_gradient
        value, gradient = linear_value_gradient(context.basis.radii, points)
        endpoint_hats[surface] = value[:, [0, -1]] @ trace_target
        endpoint_hat_gradients[surface] = gradient[:, [0, -1]] @ trace_target
    all_momentum = numerical.concatenate([momentum, new_momentum['quad']], axis=1)
    moments = all_momentum.T @ (weights[:, None] * (context.reservoir['quad']['q'] / bubble_scale))
    target = numerical.concatenate([numerical.zeros((momentum.shape[1], 2)), numerical.eye(2)]) - all_momentum.T @ (weights[:, None] * endpoint_hats['quad'])
    lift_coefficients, unused_residual, rank, unused_singular = lstsq(moments, target, lapack_driver='gelsy')
    if rank != moments.shape[0]:
        raise ValueError('Continuous endpoint lifts do not have full dual-moment rank.')
    extended = {}
    for surface, maps in base.items():
        lift = endpoint_hats[surface] + context.reservoir[surface]['q'] / bubble_scale @ lift_coefficients
        lift_r = endpoint_hat_gradients[surface] + context.reservoir[surface]['qr'] / bubble_scale @ lift_coefficients
        extended[surface] = {'q': numerical.concatenate([maps['q'], lift], axis=1), 'qr': numerical.concatenate([maps['qr'], lift_r], axis=1), 'p': numerical.concatenate([maps['p'], new_momentum[surface]], axis=1)}
    new_pair = extended['quad']['p'].T @ (weights[:, None] * extended['quad']['q'])
    expected = numerical.block([[pairing, numerical.zeros((pairing.shape[0], 2))], [numerical.zeros((2, pairing.shape[1])), numerical.eye(2)]])
    family_coefficients = solve(new_pair, extended['quad']['p'].T @ (weights[:, None] * family['quad']))
    trace_error = extended['nodes']['q'][[0, -1]] @ family_coefficients - family['nodes'][[0, -1]]
    old_equation_error = momentum.T @ (weights[:, None] * (extended['quad']['q'] @ family_coefficients - family['quad']))
    return extended, {'parent_family_dimension': family['quad'].shape[1], 'parent_family_singular_values': singular.tolist(), 'no_parent_family_modes_discarded': True, 'new_phase_dimension': new_pair.shape[0], 'new_pairing_condition': float(numerical.linalg.cond(new_pair)), 'block_pairing_error': float(abs(new_pair - expected).max()), 'all_kernel_family_trace_error': float(abs(trace_error).max()), 'all_old_moments_preserved_error': float(abs(old_equation_error).max()), 'new_coordinate_interior_node_max': float(abs(extended['nodes']['q'][1:-1, -2:]).max()), 'dual_lift_rank': int(rank), 'dual_lift_required_rank': moments.shape[0], 'moment_constraints_error': float(abs(moments @ lift_coefficients - target).max())}


def gram_density_control(context, data, result, family, primitive):
    from annular_gram_joint_action_20260909 import gram_matrices

    links, basis = context.links, context.basis
    nodes = data['nodes']
    factors, unused_sampling = gram_matrices(basis.radii.size)
    amplitude = factors @ nodes['chi']
    endpoint = numerical.exp(result['endpoint_log'])
    coefficient = basis.radii**2 * nodes['N'] * numerical.sqrt(nodes['F'])
    density = links.collect(links.sweight * endpoint * coefficient[links.node])
    amplitude_time = links.collect(links.tweight * endpoint * result['q_nodes'][links.node])
    current = amplitude[links.factor] * (links.sweight * coefficient[links.node] * amplitude_time[links.factor] - links.tweight * result['q_nodes'][links.node] * density[links.factor]) / basis.spacing
    global_weights = current * numerical.exp(primitive.evaluate(links.targets) + primitive.evaluate(links.anchors))
    cell_points = basis.radii[:-1] + .371 * numerical.diff(basis.radii)
    interior = (cell_points[:, None] > numerical.minimum(links.anchors, links.targets)) & (cell_points[:, None] < numerical.maximum(links.anchors, links.targets))
    coefficients = interior @ (global_weights * numerical.sign(links.targets - links.anchors))
    other_points = basis.radii[:-1] + .729 * numerical.diff(basis.radii)
    alternate = ((other_points[:, None] > numerical.minimum(links.anchors, links.targets)) & (other_points[:, None] < numerical.maximum(links.anchors, links.targets))) @ (global_weights * numerical.sign(links.targets - links.anchors))
    gp = family['quad'] @ coefficients
    expected_endpoints = numerical.array([-1., 1.]) * .1 * numerical.sqrt(nodes['F'][[0, -1]]) * result['q_nodes'][[0, -1]] * result['gram_scalar'][[0, -1]] / nodes['N'][[0, -1]]
    return coefficients, gp, {'anchor_cancellation_max': float(abs(links.collect(current * endpoint)).max()), 'same_cell_amplitude_difference': float(abs(coefficients - alternate).max()), 'global_vs_link_log_difference': float(abs(primitive.evaluate(links.targets) - primitive.evaluate(links.anchors) - result['endpoint_log']).max()), 'one_sided_kernel_trace_error': float(abs(family['nodes'][[0, -1]] @ coefficients - expected_endpoints).max())}
