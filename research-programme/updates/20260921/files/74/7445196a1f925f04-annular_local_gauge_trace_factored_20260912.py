import numpy as np
from scipy.linalg import lstsq, svd

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_rate_completion_20260911 import bubbles


def polynomial_completion(model, modes):
    old, weights, pairing = model.frame, model.context.weights, model.pairings['quad']
    candidates, gradients, momenta = {}, {}, {}
    endpoint_values = None
    momentum_endpoints = None
    for surface in ['nodes'] + [name for name in model.data if name != 'nodes']:
        radii = model.data[surface]['R']
        hats, hats_r = linear_value_gradient(model.context.knots, radii)
        bubble, bubble_r = bubbles(model.context.knots, radii, modes)
        extra = bubbles(model.context.knots, radii, modes + 2)[0]
        raw = np.concatenate([old[surface]['q'], hats, bubble], axis=1)
        raw_r = np.concatenate([old[surface]['qr'], hats_r, bubble_r], axis=1)
        raw_p = np.concatenate([old[surface]['p'], hats, extra], axis=1)
        if surface == 'nodes':
            endpoint_values = raw[[0, -1]].copy()
            momentum_endpoints = raw_p[[0, -1]].copy()
        linear, linear_r = linear_value_gradient(model.radii[[0, -1]], radii)
        candidates[surface] = raw - linear @ endpoint_values
        gradients[surface] = raw_r - linear_r @ endpoint_values
        momenta[surface] = raw_p - linear @ momentum_endpoints
    if np.any(candidates['nodes'][[0, -1]]) or np.any(momenta['nodes'][[0, -1]]):
        raise ValueError('Algebraic trace factorization was not exact at the endpoints.')
    scale = np.sqrt(weights @ candidates['quad']**2)
    active = scale > 1e-12
    candidates = {surface: values[:, active] / scale[active] for surface, values in candidates.items()}
    gradients = {surface: values[:, active] / scale[active] for surface, values in gradients.items()}
    constraints = old['quad']['p'].T @ (weights[:, None] * candidates['quad'])
    row_scale = np.linalg.norm(constraints, axis=1)
    normalized = constraints / row_scale[:, None]
    unused_left, singular, right = svd(normalized, full_matrices=True)
    rank = int((singular > 1e-12 * singular[0]).sum())
    if rank != constraints.shape[0]:
        raise ValueError('Old momentum moments lost rank.')
    nullspace = right[rank:].T
    null_values = candidates['quad'] @ nullspace
    unused_left, residual_singular, residual_right = svd(np.sqrt(weights)[:, None] * null_values, full_matrices=False)
    retained = residual_singular > 1e-10 * residual_singular[0]
    coefficients = nullspace @ (residual_right[retained].T / residual_singular[retained])
    lift = lstsq(normalized, np.eye(rank), cond=1e-13, lapack_driver='gelsd')[0]
    for unused_pass in range(2):
        coefficients -= lift @ (normalized @ coefficients)
    added = {surface: values @ coefficients for surface, values in candidates.items()}
    added_r = {surface: values @ coefficients for surface, values in gradients.items()}
    coordinate = {surface: np.concatenate([old[surface]['q'], added[surface]], axis=1) for surface in old}
    momentum_scale = np.sqrt(weights @ momenta['quad']**2)
    active_p = momentum_scale > 1e-12
    momenta = {surface: values[:, active_p] / momentum_scale[active_p] for surface, values in momenta.items()}
    conditions = coordinate['quad'].T @ (weights[:, None] * momenta['quad'])
    added_count = added['quad'].shape[1]
    target = np.concatenate([np.zeros((pairing.shape[1], added_count)), np.eye(added_count)])
    dual_scale = np.linalg.norm(conditions, axis=1)
    dual_coefficients, unused_residual, dual_rank, dual_singular = lstsq(conditions / dual_scale[:, None], target / dual_scale[:, None], cond=1e-13, lapack_driver='gelsd')
    error = conditions @ dual_coefficients - target
    if dual_rank != conditions.shape[0] or abs(error).max() > 1e-8:
        raise ValueError('Trace-factorized dual moments failed: ' + str((dual_rank, abs(error).max())))
    added_p = {surface: values @ dual_coefficients for surface, values in momenta.items()}
    frames = {surface: {'q': coordinate[surface], 'qr': np.concatenate([old[surface]['qr'], added_r[surface]], axis=1), 'p': np.concatenate([old[surface]['p'], added_p[surface]], axis=1)} for surface in old}
    new_pairing = frames['quad']['p'].T @ (weights[:, None] * frames['quad']['q'])
    expected = np.block([[pairing, np.zeros((pairing.shape[0], added_count))], [np.zeros((added_count, pairing.shape[1])), np.eye(added_count)]])
    diagnostics = {'bubble_modes': modes, 'polynomial_degree': modes + 1, 'old_phase_dimension': pairing.shape[0], 'retained_added_directions': added_count, 'new_phase_dimension': new_pairing.shape[0], 'both_added_coordinate_traces_zero': float(abs(added['nodes'][[0, -1]]).max()), 'both_added_momentum_traces_zero': float(abs(added_p['nodes'][[0, -1]]).max()), 'coordinate_moment_rank': rank, 'coordinate_moment_rows': constraints.shape[0], 'dual_moment_rank': int(dual_rank), 'dual_moment_rows': conditions.shape[0], 'dual_error': float(abs(error).max()), 'canonical_block_error': float(abs(new_pairing - expected).max()), 'pairing_condition': float(np.linalg.cond(new_pairing)), 'rank_cutoff_relative': 1e-10, 'discarded_near_dependent_singular_count': int((~retained).sum()), 'residual_singular_values': residual_singular.tolist(), 'coordinate_constraint_singular_values': singular.tolist(), 'momentum_constraint_singular_values': dual_singular.tolist(), 'zero_endpoint_interior_space_not_full_polynomial_space_claim': True, 'all_old_columns_exactly_retained': True, 'source_independent_enrichment_not_current_fitting': True, 'scalar_grid_and_Gram_factors_unchanged': True, 'traces_factored_before_nullspace_and_dual_solve': True}
    if max(diagnostics['both_added_coordinate_traces_zero'], diagnostics['both_added_momentum_traces_zero']) != 0:
        raise ValueError('Factored traces changed.')
    return frames, diagnostics
