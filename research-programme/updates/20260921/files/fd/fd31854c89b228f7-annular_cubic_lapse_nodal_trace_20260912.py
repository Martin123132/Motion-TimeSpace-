import numpy as numerical
from scipy.linalg import solve, lstsq

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_rate_completion_20260911 import normalized_transform
from annular_cubic_lapse_boundary_polynomial_20260912 import CubicContext as PolynomialContext, CubicPreparation, CubicFields, evaluate_cubic_initial


def complete_nodal_momentum_trace(context, base):
    weights = context.weights
    coordinate, momentum = base['quad']['q'], base['quad']['p']
    pairing = momentum.T @ (weights[:, None] * coordinate)
    interior = numerical.arange(1, context.basis.radii.size - 1)
    loads = base['nodes']['q'][interior].T
    discrepancy = base['nodes']['p'][[0, -1]] @ solve(pairing.T, loads)
    nodal_values = numerical.zeros((context.basis.radii.size, 2))
    nodal_values[interior] = -discrepancy.T
    bubble_scale = numerical.sqrt(weights @ context.reservoir['quad']['q']**2)
    hats = {surface: linear_value_gradient(context.basis.radii, points) for surface, points in context.surfaces.items()}
    raw_coordinate = hats['quad'][0] @ nodal_values
    moments = momentum.T @ (weights[:, None] * (context.reservoir['quad']['q'] / bubble_scale))
    target = -momentum.T @ (weights[:, None] * raw_coordinate)
    coefficients, unused_residual, rank, unused_singular = lstsq(moments, target, lapack_driver='gelsy')
    if rank != moments.shape[0]:
        raise ValueError('Nodal coordinate dual has unresolved rank; no old variation is removed.')
    raw = {}
    for surface in base:
        raw[surface] = hats[surface][0] @ nodal_values + context.reservoir[surface]['q'] / bubble_scale @ coefficients
        raw[surface + '_gradient'] = hats[surface][1] @ nodal_values + context.reservoir[surface]['qr'] / bubble_scale @ coefficients
    transform = normalized_transform(raw['quad'], weights)
    added_coordinate = {surface: raw[surface] @ transform for surface in base}
    endpoint_target = solve(transform.T, numerical.eye(2))
    endpoint_seed = {surface: hats[surface][0][:, [0, -1]] @ endpoint_target for surface in base}
    all_coordinate = numerical.concatenate([coordinate, added_coordinate['quad']], axis=1)
    dual_moments = all_coordinate.T @ (weights[:, None] * (context.reservoir['quad']['q'] / bubble_scale))
    dual_target = numerical.concatenate([numerical.zeros((coordinate.shape[1], 2)), numerical.eye(2)]) - all_coordinate.T @ (weights[:, None] * endpoint_seed['quad'])
    dual_coefficients, unused_residual, dual_rank, unused_singular = lstsq(dual_moments, dual_target, lapack_driver='gelsy')
    if dual_rank != dual_moments.shape[0]:
        raise ValueError('Nodal momentum dual has unresolved rank; no source direction is removed.')
    extended = {}
    for surface, maps in base.items():
        added_momentum = endpoint_seed[surface] + context.reservoir[surface]['q'] / bubble_scale @ dual_coefficients
        extended[surface] = {'q': numerical.concatenate([maps['q'], added_coordinate[surface]], axis=1), 'qr': numerical.concatenate([maps['qr'], raw[surface + '_gradient'] @ transform], axis=1), 'p': numerical.concatenate([maps['p'], added_momentum], axis=1)}
    new_pair = extended['quad']['p'].T @ (weights[:, None] * extended['quad']['q'])
    expected = numerical.block([[pairing, numerical.zeros((pairing.shape[0], 2))], [numerical.zeros((2, pairing.shape[1])), numerical.eye(2)]])
    source_projection = solve(new_pair.T, extended['nodes']['q'][interior].T)
    source_trace = extended['nodes']['p'][[0, -1]] @ source_projection
    old_covector_error = new_pair.T[:pairing.shape[1]] @ source_projection - loads
    return extended, {'all_interior_nodal_source_directions': len(interior), 'original_modes_removed': 0, 'coordinate_dual_rank': int(rank), 'momentum_dual_rank': int(dual_rank), 'phase_dimension': int(new_pair.shape[0]), 'block_pairing_error': float(abs(new_pair - expected).max()), 'pairing_condition': float(numerical.linalg.cond(new_pair)), 'all_nodal_source_trace_error': float(abs(source_trace).max()), 'old_nodal_covector_error': float(abs(old_covector_error).max()), 'new_coordinate_endpoint_max': float(abs(extended['nodes']['q'][[0, -1], -2:]).max()), 'not_source_amplitude_fitted': True}


class CubicContext(PolynomialContext):
    def build(self, selected=None):
        data, frames, diagnostics = super().build(selected)
        frames['mass'], trace_diagnostics = complete_nodal_momentum_trace(self, frames['mass'])
        diagnostics['mass']['nodal_trace_completion'] = trace_diagnostics
        return data, frames, diagnostics
