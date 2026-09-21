import numpy as numerical
from scipy.linalg import solve, svd, lstsq
from annular_canonical_rate_completion_20260911 import normalized_transform


def full_family_trace_extension(context, base, family):
    weights = context.weights
    coordinate, momentum = base['quad']['q'], base['quad']['p']
    pairing = momentum.T @ (weights[:, None] * coordinate)
    coordinate_gram = coordinate.T @ (weights[:, None] * coordinate)
    family_scale = numerical.sqrt(weights @ family['quad']**2)
    projection = solve(coordinate_gram, coordinate.T @ (weights[:, None] * (family['quad'] / family_scale)))
    residual = family['quad'] / family_scale - coordinate @ projection
    unused_left, singular, right = svd(numerical.sqrt(weights)[:, None] * residual, full_matrices=False)
    selected = singular > 1e-10
    if not numerical.any(selected):
        raise ValueError('No new trace direction was resolved.')
    weak_coefficients = solve(pairing, momentum.T @ (weights[:, None] * family['quad']))
    endpoint_map = base['nodes']['q'][[0, -1]]
    discrepancy = family['nodes'][[0, -1]] - endpoint_map @ weak_coefficients
    residual_basis = {}
    for surface in base:
        residual_basis[surface] = ((family[surface] / family_scale - base[surface]['q'] @ projection) @ right[selected].T) / singular[selected]
    for unused_pass in range(2):
        correction = solve(coordinate_gram, coordinate.T @ (weights[:, None] * residual_basis['quad']))
        for surface in base:
            residual_basis[surface] -= base[surface]['q'] @ correction
    normalization = normalized_transform(residual_basis['quad'], weights)
    for surface in base:
        residual_basis[surface] = residual_basis[surface] @ normalization
    family_moments = residual_basis['quad'].T @ (weights[:, None] * (family['quad'] / family_scale))
    representer_coefficients, unused_residuals, retained_rank, unused_values = lstsq(family_moments.T, (discrepancy / family_scale).T, lapack_driver='gelsy')
    representer_error = float(abs(family_moments.T @ representer_coefficients - (discrepancy / family_scale).T).max())
    if representer_error > 1e-9:
        raise ValueError('Dependent parent-family trace conditions are inconsistent: ' + str(representer_error))
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
    return extended, {'parent_family_dimension': family['quad'].shape[1], 'parent_family_singular_values': singular.tolist(), 'no_parent_family_modes_discarded': True, 'resolved_residual_rank': int(selected.sum()), 'dependent_directions_checked_not_removed_from_parent': True, 'representer_residual': representer_error, 'new_phase_dimension': new_pair.shape[0], 'new_pairing_condition': float(numerical.linalg.cond(new_pair)), 'block_pairing_error': float(abs(new_pair - expected).max()), 'all_kernel_family_trace_error': float(abs(trace_error).max()), 'all_old_moments_preserved_error': float(abs(old_equation_error).max()), 'new_coordinate_interior_node_max': float(abs(extended['nodes']['q'][1:-1, -2:]).max()), 'dual_lift_rank': int(rank), 'dual_lift_required_rank': moments.shape[0], 'moment_constraints_error': float(abs(moments @ lift_coefficients - target).max())}
