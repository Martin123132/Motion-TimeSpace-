import numpy as np
from scipy.linalg import lstsq, solve, svd

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_rate_completion_20260911 import bubbles


def polynomial_completion(model, modes):
    old, weights, pairing = model.frame, model.context.weights, model.pairings['quad']
    values, gradients = {}, {}
    for surface, data in model.data.items():
        hats, hats_r = linear_value_gradient(model.context.knots, data['R'])
        bubble, bubble_r = bubbles(model.context.knots, data['R'], modes)
        values[surface] = np.concatenate([hats, bubble], axis=1)
        gradients[surface] = np.concatenate([hats_r, bubble_r], axis=1)
    scale = np.sqrt(weights @ values['quad']**2)
    values = {surface: array / scale for surface, array in values.items()}
    gradients = {surface: array / scale for surface, array in gradients.items()}
    projection = solve(pairing, old['quad']['p'].T @ (weights[:, None] * values['quad']))
    remainder = {surface: values[surface] - old[surface]['q'] @ projection for surface in old}
    remainder_r = {surface: gradients[surface] - old[surface]['qr'] @ projection for surface in old}
    unused_left, singular, right = svd(np.sqrt(weights)[:, None] * remainder['quad'], full_matrices=False)
    cutoff = 1e-10 * singular[0]
    retained = singular > cutoff
    transform = right[retained].T / singular[retained]
    added = {surface: remainder[surface] @ transform for surface in old}
    added_r = {surface: remainder_r[surface] @ transform for surface in old}
    for unused_pass in range(2):
        correction = solve(pairing, old['quad']['p'].T @ (weights[:, None] * added['quad']))
        for surface in old:
            added[surface] -= old[surface]['q'] @ correction
            added_r[surface] -= old[surface]['qr'] @ correction
    coordinate_projection = lstsq(np.sqrt(weights)[:, None] * old['quad']['q'], np.sqrt(weights)[:, None] * added['quad'], cond=1e-13, lapack_driver='gelsd')[0]
    dual = {surface: added[surface] - old[surface]['q'] @ coordinate_projection for surface in old}
    dual_pair = dual['quad'].T @ (weights[:, None] * added['quad'])
    dual_transform = solve(dual_pair.T, np.eye(dual_pair.shape[0]))
    frame = {surface: {'q': np.concatenate([old[surface]['q'], added[surface]], axis=1), 'qr': np.concatenate([old[surface]['qr'], added_r[surface]], axis=1), 'p': np.concatenate([old[surface]['p'], dual[surface] @ dual_transform], axis=1)} for surface in old}
    new_pair = frame['quad']['p'].T @ (weights[:, None] * frame['quad']['q'])
    expected = np.block([[pairing, np.zeros((pairing.shape[0], dual_pair.shape[0]))], [np.zeros((dual_pair.shape[0], pairing.shape[1])), np.eye(dual_pair.shape[0])]])
    representation = lstsq(np.sqrt(weights)[:, None] * frame['quad']['q'], np.sqrt(weights)[:, None] * values['quad'], cond=1e-13, lapack_driver='gelsd')[0]
    errors = {surface: float(abs(frame[surface]['q'] @ representation - values[surface]).max()) for surface in ['quad', 'check', 'nodes']}
    diagnostics = {'bubble_modes': modes, 'polynomial_degree': modes + 1, 'requested_polynomial_directions': values['quad'].shape[1], 'retained_added_directions': int(retained.sum()), 'new_phase_dimension': new_pair.shape[0], 'discarded_near_dependent_singular_count': int((~retained).sum()), 'rank_cutoff_relative': 1e-10, 'residual_singular_values': singular.tolist(), 'polynomial_representation_errors': errors, 'pairing_condition': float(np.linalg.cond(new_pair)), 'dual_pair_condition': float(np.linalg.cond(dual_pair)), 'canonical_block_error': float(abs(new_pair - expected).max()), 'all_old_columns_exactly_retained': True, 'basis_selection_independent_of_regenerated_current': True, 'scalar_grid_and_Gram_factors_unchanged': True}
    return frame, diagnostics


def gauge_budget(model, result, surface='quad'):
    weights = model.context.weights if surface == 'quad' else model.context.check_weights
    values, nodes = result['fields'][surface], result['fields']['nodes']
    phase, node_phase = model.frame[surface], model.frame['nodes']
    lapse, root_f = values['N'], np.sqrt(values['F'])
    theta = values['eta'] / lapse[:, None]
    theta_r = values['eta_r'] / lapse[:, None] - values['eta'] * (values['N_r'] / lapse**2)[:, None]
    node_theta = nodes['eta'] / nodes['N'][:, None]
    momentum_rate = phase['p'] @ result['P_coeff']
    delta = result['mu_first'] - result['raw_mu']
    configuration_test = theta * result['mu_first'][:, None]
    node_configuration_test = node_theta * result['mu_nodes'][:, None]
    momentum_test = theta * momentum_rate[:, None] - (lapse / (.1 * root_f))[:, None] * theta_r
    unused_coefficients, unused_force, regular, nodal = model.metric_momentum(result['fields'], result['energy'], surface)
    euler_density = regular - momentum_rate
    coordinate_work = configuration_test.T @ (weights * euler_density) + node_configuration_test.T @ nodal
    momentum_work = momentum_test.T @ (weights * delta)
    graph_matrix = np.concatenate([np.sqrt(weights)[:, None] * phase['q'], np.sqrt(model.node_weights)[:, None] * node_phase['q']])
    graph_target = np.concatenate([np.sqrt(weights)[:, None] * configuration_test, np.sqrt(model.node_weights)[:, None] * node_configuration_test])
    q_coefficients = lstsq(graph_matrix, graph_target, cond=1e-13, lapack_driver='gelsd')[0]
    graph_residual = graph_target - graph_matrix @ q_coefficients
    q_residual = configuration_test - phase['q'] @ q_coefficients
    node_q_residual = node_configuration_test - node_phase['q'] @ q_coefficients
    metric_residual_work = q_residual.T @ (weights * euler_density) + node_q_residual.T @ nodal
    p_coefficients = lstsq(np.sqrt(weights)[:, None] * phase['p'], np.sqrt(weights)[:, None] * momentum_test, cond=1e-13, lapack_driver='gelsd')[0]
    p_residual = momentum_test - phase['p'] @ p_coefficients
    momentum_residual_work = p_residual.T @ (weights * delta)
    euler_dual_norm = np.sqrt(weights @ euler_density**2 + (nodal**2 / model.node_weights).sum())
    q_bounds = euler_dual_norm * np.linalg.norm(graph_residual, axis=0)
    p_bounds = np.sqrt(weights @ p_residual**2) * np.sqrt(weights @ delta**2)
    dropped_gradient = (theta * momentum_rate[:, None]).T @ (weights * delta)
    return {'theta': theta, 'theta_r': theta_r, 'coordinate_work': coordinate_work, 'momentum_work': momentum_work, 'metric_residual_work': metric_residual_work, 'momentum_residual_work': momentum_residual_work, 'q_graph_error': np.linalg.norm(graph_residual, axis=0), 'p_error': np.sqrt(weights @ p_residual**2), 'q_bound': q_bounds, 'p_bound': p_bounds, 'bound': q_bounds + p_bounds, 'identity_error': result['C1'] - coordinate_work - momentum_work, 'q_weak_equation_error': coordinate_work - metric_residual_work, 'p_weak_equation_error': momentum_work - momentum_residual_work, 'missing_gradient_negative_control': coordinate_work + dropped_gradient - result['C1'], 'euler_dual_norm': float(euler_dual_norm), 'mass_velocity_L2_error': float(np.sqrt(weights @ delta**2))}
