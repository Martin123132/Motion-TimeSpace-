import numpy as numerical
from scipy.linalg import block_diag, cholesky, eigvalsh, solve, solve_triangular

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_paired_variational_energy_20260910 import scalar_maps


def endpoint_clock_functionals(system, packed, speed, second):
    points = system.basis.radii[[0, -1]]
    mass_map = linear_value_gradient(system.basis.faces, points)[0]
    lapse_map = linear_value_gradient(system.basis.radii, points)[0]
    mass, mass_first, mass_second = [mass_map @ order[system.slices[0]] for order in [packed, speed, second]]
    lapse, lapse_first, lapse_second = [lapse_map @ order[system.slices[1]] for order in [packed, speed, second]]
    denominator = points - 2 * mass
    if min(numerical.min(lapse), numerical.min(denominator)) <= 0:
        raise ValueError('Endpoint metric outside positive chart.')
    functional = numerical.zeros((2, system.count))
    functional[:, system.slices[0]] = -mass_map / denominator[:, None]
    functional[:, system.slices[1]] = lapse_map / lapse[:, None]
    lower = -3 * lapse_first * lapse_second / lapse**2 + 2 * (lapse_first / lapse)**3
    lower -= 6 * mass_first * mass_second / denominator**2 + 8 * (mass_first / denominator)**3
    return functional, lower


def metric_schur_response(system, packed, speed, second, third, known_third, include_gram):
    if any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Canonical zero-potential branch only.')
    basis = system.basis
    jacobian = system.evaluate(packed, include_gram)[2]
    metric = system.free[system.free < system.slices[2].start]
    velocity = system.free[system.free >= system.slices[2].start]
    full_free = numerical.concatenate([metric, velocity])
    metric_block = jacobian[numerical.ix_(metric, metric)]
    coupling = jacobian[numerical.ix_(metric, velocity)]
    kinetic = jacobian[numerical.ix_(velocity, velocity)]
    cholesky(kinetic)
    fixed = numerical.zeros_like(packed)
    fixed[system.fixed] = third[system.fixed]
    forcing = -(known_third + jacobian @ fixed)
    kinetic_coupling = solve(kinetic, coupling.T, assume_a='pos')
    kinetic_forcing = solve(kinetic, forcing[velocity], assume_a='pos')
    schur = metric_block - coupling @ kinetic_coupling
    reduced_forcing = forcing[metric] - coupling @ kinetic_forcing
    metric_third = solve(schur, reduced_forcing, assume_a='sym')
    velocity_third = solve(kinetic, forcing[velocity] - coupling.T @ metric_third, assume_a='pos')
    functional, lower = endpoint_clock_functionals(system, packed, speed, second)
    target = functional[:, metric]
    adjoint = solve(schur.T, target.T, assume_a='sym')
    full_adjoint = numerical.concatenate([adjoint, -kinetic_coupling @ adjoint], axis=0)
    offset = lower + functional @ fixed
    predicted = offset + adjoint.T @ reduced_forcing
    value_maps = block_diag(basis.face_value.T @ (basis.quadrature_weights[:, None] * basis.face_value), basis.node_value.T @ (basis.quadrature_weights[:, None] * basis.node_value))
    weight = value_maps[numerical.ix_(metric, metric)]
    root = cholesky(weight, lower=False)
    inverse_root = solve_triangular(root, numerical.eye(root.shape[0]), lower=False)
    normalized = inverse_root.T @ schur @ inverse_root
    normalized_forcing = inverse_root.T @ reduced_forcing
    normalized_target = target @ inverse_root
    normalized_adjoint = root @ adjoint
    spectrum = eigvalsh(normalized)
    inverse_norm = float(1 / min(abs(spectrum)))
    adjoint_norms = numerical.linalg.norm(normalized_adjoint, axis=0)
    upper_schur = abs(offset) + abs(adjoint.T) @ abs(reduced_forcing)
    upper_full = abs(offset) + abs(full_adjoint.T) @ abs(forcing[full_free])
    upper_natural = abs(offset) + adjoint_norms * numerical.linalg.norm(normalized_forcing)
    scalar_local = velocity - system.slices[2].start
    maps = scalar_maps(basis, basis.quadrature)[0]
    lapse_q = basis.node_value @ packed[system.slices[1]]
    mass_q = basis.face_value @ packed[system.slices[0]]
    characteristic = lapse_q * numerical.sqrt(1 - 2 * mass_q / basis.quadrature)
    density = basis.quadrature_weights * basis.quadrature**2 / characteristic
    scalar_map = maps[:, scalar_local]
    velocity_q = maps @ packed[system.slices[2].start:]
    lapse_product = (velocity_q / lapse_q)[:, None] * basis.node_value
    lapse_projection = solve(kinetic, scalar_map.T @ (density[:, None] * lapse_product), assume_a='pos')
    projection_error = lapse_product - scalar_map @ lapse_projection
    lapse_residual_gram = projection_error.T @ (density[:, None] * projection_error)
    lapse_positions = numerical.nonzero(metric >= system.slices[1].start)[0]
    return {'jacobian': jacobian, 'metric_indices': metric, 'velocity_indices': velocity, 'full_free': full_free, 'metric_block': metric_block, 'coupling': coupling, 'kinetic': kinetic, 'schur': schur, 'forcing': forcing, 'reduced_forcing': reduced_forcing, 'fixed': fixed, 'metric_third': metric_third, 'velocity_third': velocity_third, 'functional': functional, 'lower': lower, 'target': target, 'adjoint': adjoint, 'full_adjoint': full_adjoint, 'offset': offset, 'predicted_theta_tt': predicted, 'theta_schur_component_upper': upper_schur, 'theta_full_component_upper': upper_full, 'theta_natural_upper': upper_natural, 'metric_weight': weight, 'normalized_schur': normalized, 'normalized_forcing': normalized_forcing, 'normalized_target': normalized_target, 'normalized_adjoint': normalized_adjoint, 'normalized_spectrum': spectrum, 'normalized_inverse_norm': inverse_norm, 'adjoint_natural_norms': adjoint_norms, 'lapse_positions': lapse_positions, 'lapse_residual_gram': lapse_residual_gram, 'lapse_projection_error': projection_error, 'kinetic_quadrature_matrix': scalar_map.T @ (density[:, None] * scalar_map)}


def response_neighborhood_bound(inverse_norm, adjoint_norm, forcing_norm, matrix_change, target_change, forcing_change, offset_change):
    quantities = [inverse_norm, adjoint_norm, forcing_norm, matrix_change, target_change, forcing_change, offset_change]
    if not all(numerical.isfinite(value) and value >= 0 for value in quantities):
        raise ValueError('Perturbation majorants must be finite and nonnegative.')
    contraction = inverse_norm * matrix_change
    if contraction >= 1:
        return {'gate': False, 'contraction': float(contraction), 'reason': 'No inverse-persistence conclusion at or beyond the Neumann threshold.'}
    adjoint_change = inverse_norm / (1 - contraction) * (target_change + matrix_change * adjoint_norm)
    response_change = offset_change + adjoint_norm * forcing_change + adjoint_change * (forcing_norm + forcing_change)
    return {'gate': True, 'contraction': float(contraction), 'adjoint_change_upper': float(adjoint_change), 'response_change_upper': float(response_change), 'adjoint_norm_upper': float(adjoint_norm + adjoint_change), 'scope': 'Conditional finite-mesh matrix/forcing neighborhood, not a certified physical time interval.'}
