import numpy as np
from scipy.linalg import lstsq, solve, svd

from annular_adm_mixed_action_20260909 import linear_value_gradient


def scaled_solve(matrix, target, label):
    row_scale = np.linalg.norm(matrix, axis=1)
    if row_scale.min() <= 0:
        raise ValueError(label + ' has a zero functional.')
    scaled = matrix / row_scale[:, None]
    right = target / row_scale[:, None]
    coefficients, unused_residual, rank, singular = lstsq(scaled, right, cond=1e-13, lapack_driver='gelsd')
    defect = scaled @ coefficients - right
    if abs(defect).max() > 3e-9:
        raise ValueError(label + ' moment system is inconsistent: ' + str(float(abs(defect).max())))
    return coefficients, {'rows': matrix.shape[0], 'columns': matrix.shape[1], 'rank': int(rank), 'scaled_error': float(abs(defect).max()), 'singular_values': singular.tolist()}


def functionals(model, fields, energy, maps, surface='quad'):
    weights = model.context.weights if surface == 'quad' else model.context.check_weights
    values, nodes = fields[surface], fields['nodes']
    bulk = values['eta'] * (values['mu'] / (.1 * values['R']**2 * values['F']**1.5))[:, None]
    bulk -= values['eta_r'] / (.1 * np.sqrt(values['F']))[:, None]
    nodal = nodes['eta'] * (energy / (model.radii * np.sqrt(nodes['F'])))[:, None]
    nodal = nodal.copy()
    nodal[-1] += nodes['eta'][-1] / (.1 * np.sqrt(nodes['F'][-1]))
    nodal[0] -= nodes['eta'][0] / (.1 * np.sqrt(nodes['F'][0]))
    constraints = bulk.T @ (weights[:, None] * maps[surface]) + nodal.T @ maps['nodes']
    return np.concatenate([constraints, maps['nodes'][[0, -1]]])


def carrier_family(model, result):
    family = {}
    for surface, values in result['fields'].items():
        cells = np.clip(np.searchsorted(model.radii, values['R'], side='right') - 1, 0, model.radii.size - 2)
        multiplier = result['current']['carriers'][surface]
        matrix = np.zeros((values['R'].size, model.radii.size - 1))
        matrix[np.arange(values['R'].size), cells] = multiplier
        family[surface] = matrix
    return family


def complete_flux_moments(model, result):
    weights = model.context.weights
    old = model.frame
    pairing = model.pairings['quad']
    fields, energy = result['fields'], result['energy']
    family = carrier_family(model, result)
    family_scale = np.sqrt(weights @ family['quad']**2)
    family = {surface: values / family_scale for surface, values in family.items()}
    old_projection = solve(pairing, old['quad']['p'].T @ (weights[:, None] * family['quad']))
    projected = {surface: old[surface]['q'] @ old_projection for surface in old}
    discrepancy = functionals(model, fields, energy, family) - functionals(model, fields, energy, projected)
    candidates, candidate_gradients = {}, {}
    for surface, values in fields.items():
        hats, gradients = linear_value_gradient(model.radii, values['R'])
        candidates[surface] = np.concatenate([hats, model.context.reservoir[surface]['q']], axis=1)
        candidate_gradients[surface] = np.concatenate([gradients, model.context.reservoir[surface]['qr']], axis=1)
    scales = np.sqrt(weights @ candidates['quad']**2)
    candidates = {surface: values / scales for surface, values in candidates.items()}
    candidate_gradients = {surface: values / scales for surface, values in candidate_gradients.items()}
    coordinate_conditions = np.concatenate([old['quad']['p'].T @ (weights[:, None] * candidates['quad']), functionals(model, fields, energy, candidates)])
    coordinate_target = np.concatenate([np.zeros((pairing.shape[0], family_scale.size)), discrepancy])
    coordinate_coefficients, coordinate_diagnostics = scaled_solve(coordinate_conditions, coordinate_target, 'continuous coordinate')
    raw_coordinate = {surface: candidates[surface] @ coordinate_coefficients for surface in old}
    unused_left, singular, right = svd(np.sqrt(weights)[:, None] * raw_coordinate['quad'], full_matrices=False)
    if singular[-1] < 1e-12 * singular[0]:
        raise ValueError('The all16 correction family is rank deficient; no force direction is discarded: ' + repr(singular.tolist()))
    transform = right.T / singular
    inverse_transform = solve(transform, np.eye(family_scale.size))
    added_coordinate = {surface: raw_coordinate[surface] @ transform for surface in old}
    added_gradient = {surface: candidate_gradients[surface] @ coordinate_coefficients @ transform for surface in old}
    momentum_candidates = {surface: np.concatenate([candidates[surface], family[surface]], axis=1) for surface in old}
    test_values = np.concatenate([old['quad']['q'], added_coordinate['quad'], family['quad']], axis=1)
    momentum_conditions = np.concatenate([test_values.T @ (weights[:, None] * momentum_candidates['quad']), momentum_candidates['nodes'][[0, -1]]])
    momentum_target = np.concatenate([np.zeros((pairing.shape[1], family_scale.size)), np.eye(family_scale.size), inverse_transform.T, np.zeros((2, family_scale.size))])
    momentum_coefficients, momentum_diagnostics = scaled_solve(momentum_conditions, momentum_target, 'broken momentum')
    added_momentum = {surface: momentum_candidates[surface] @ momentum_coefficients for surface in old}
    extended = {surface: {'q': np.concatenate([old[surface]['q'], added_coordinate[surface]], axis=1), 'qr': np.concatenate([old[surface]['qr'], added_gradient[surface]], axis=1), 'p': np.concatenate([old[surface]['p'], added_momentum[surface]], axis=1)} for surface in old}
    new_pairing = extended['quad']['p'].T @ (weights[:, None] * extended['quad']['q'])
    expected = np.block([[pairing, np.zeros((pairing.shape[0], family_scale.size))], [np.zeros((family_scale.size, pairing.shape[1])), np.eye(family_scale.size)]])
    projection = solve(new_pairing, extended['quad']['p'].T @ (weights[:, None] * family['quad']))
    projected = {surface: extended[surface]['q'] @ projection for surface in old}
    final_error = functionals(model, fields, energy, projected) - functionals(model, fields, energy, family)
    diagnostics = {'family_dimension': family_scale.size, 'old_phase_dimension': pairing.shape[0], 'new_phase_dimension': new_pairing.shape[0], 'new_pairing_condition': float(np.linalg.cond(new_pairing)), 'block_pairing_error': float(abs(new_pairing - expected).max()), 'source_moment_error': float(abs(final_error[:19]).max()), 'endpoint_trace_error': float(abs(final_error[19:]).max()), 'old_source_moment_defect': float(abs(discrepancy[:19]).max()), 'old_endpoint_defect': float(abs(discrepancy[19:]).max()), 'new_momentum_endpoint_error': float(abs(added_momentum['nodes'][[0, -1]]).max()), 'coordinate_system': coordinate_diagnostics, 'momentum_system': momentum_diagnostics, 'coordinate_family_singular_values': singular.tolist(), 'all_old_phase_columns_retained': True, 'discontinuous_carriers_not_inserted_into_continuous_coordinate_space': True, 'no_current_amplitude_fitted': True, 'frozen_geometry_functionals_not_a_neighborhood_certificate': True}
    construction = {'coordinate_coefficients': coordinate_coefficients, 'coordinate_transform': transform, 'momentum_coefficients': momentum_coefficients, 'family_scale': family_scale, 'initial_discrepancy': discrepancy, 'final_moment_error': final_error}
    return extended, family, construction, diagnostics


def install(model, frames):
    model.frame = frames
    model.pairings = {surface: frames[surface]['p'].T @ (weights[:, None] * frames[surface]['q']) for surface, weights in [('quad', model.context.weights), ('check', model.context.check_weights)]}


def energy_balanced(model, result):
    nodes = result['fields']['nodes']
    current = result['current']
    rho = np.zeros(model.radii.size)
    rho[[0, -1]] = -np.array([-1., 1.]) * current['K']['nodes'][[0, -1]] / current['q'][[0, -1]]
    source_work = -nodes['eta'].T @ (rho * current['q'] / nodes['N'])
    constraint_rate = result['C1_no_ports'] + source_work
    boundary_work = -nodes['eta'][[0, -1]].T @ (np.array([-1., 1.]) * current['K']['nodes'][[0, -1]] / nodes['N'][[0, -1]])
    p_first = (current['Gchi'] + rho) / model.node_weights
    return {'rho': rho, 'p_first': p_first, 'C1': constraint_rate, 'boundary_work': boundary_work, 'source_work': source_work, 'Ward_error': constraint_rate - result['projection_work'] - result['metric_work'] - boundary_work - source_work}
