import numpy as numerical
from fractions import Fraction

from annular_first_derivative_energy_20260909 import affine_lift_matrix, canonical_matrices
from annular_gram_joint_action_20260909 import gram_matrices
from annular_metric_schur_bound_20260909 import field_envelopes
from annular_uniform_energy_bounds_20260909 import affine_norms, metric_envelope


def exact_lapse_margin():
    margin = (Fraction(123, 100) * Fraction(527, 2304) - Fraction(1, 50) * Fraction(59, 48)) / Fraction(1, 10)
    return {'margin': str(margin), 'greater_than_5_over_2': margin > Fraction(5, 2)}


def scalar_source_data(system, packed, include_gram, endpoint_acceleration):
    if any(system.constants[name] != 0 for name in ['b2', 'b3', 'm_chi', 'Lambda']):
        raise ValueError('Canonical branch only.')
    basis = system.basis
    count = system.node_count
    matrices = canonical_matrices(system, packed, numerical.zeros_like(packed), include_gram)
    free = system.free_velocity_indices - system.slices[2].start
    selection = numerical.ix_(free, free)
    mass_free, stiffness_free = matrices['M'][selection], matrices['K'][selection]
    configuration = numerical.concatenate([system.scalar, system.slope])
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    lift_map = affine_lift_matrix(basis)
    lift = lift_map @ system.scalar[[0, -1]]
    velocity_lift = lift_map @ packed[system.slices[2]][[0, -1]]
    displacement = (configuration - lift)[free]
    speed = (velocity - velocity_lift)[free]
    graph = numerical.linalg.solve(mass_free, stiffness_free @ displacement)
    energy = float((speed @ stiffness_free @ speed + graph @ mass_free @ graph) / 2)
    graph_force = numerical.linalg.solve(mass_free, (matrices['K'] @ configuration)[free])
    lift_force = numerical.linalg.solve(mass_free, (matrices['K'] @ lift)[free])
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    q_radial = radial @ velocity
    q_gradient_norm = float(numerical.sqrt(basis.quadrature_weights @ q_radial**2))
    factors, sampling = gram_matrices(count)
    factor_scalar, factor_q = factors @ system.scalar, factors @ packed[system.slices[2]]
    rho_q = sampling.T @ factor_q**2 / (2 * basis.spacing)
    rho_time = sampling.T @ (factor_scalar * factor_q) / basis.spacing
    velocity_boundary = lift_map @ endpoint_acceleration
    free_value = value[:, free]
    return {'matrices': matrices, 'mass_free': mass_free, 'stiffness_free': stiffness_free, 'free': free, 'configuration': configuration, 'velocity': velocity, 'value': value, 'radial': radial, 'free_value': free_value, 'energy': energy, 'graph_force': graph_force, 'graph_force_norm': float(numerical.sqrt(graph_force @ mass_free @ graph_force)), 'lift_force_norm': float(numerical.sqrt(lift_force @ mass_free @ lift_force)), 'q_radial': q_radial, 'q_gradient_norm': q_gradient_norm, 'rho_q': rho_q, 'rho_time': rho_time, 'rho_time_norm': float(numerical.sqrt(numerical.sum(rho_time**2) / basis.spacing)), 'velocity_boundary': velocity_boundary}


def source_bound(system, packed, include_gram, scalar, inner_mass_rate, clock_rate, endpoint_acceleration, use_common_box=False):
    basis = system.basis
    envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], numerical.zeros(system.face_count), numerical.zeros(system.node_count))
    fields = field_envelopes(system, packed)
    if use_common_box:
        inside = basis.radii[0] == 47 / 8 and basis.radii[-1] == 49 / 8 and system.kappa == .1 and system.node_count >= 17
        inside = inside and envelope['F_min'] >= .65 and envelope['F_max'] <= .68 and envelope['N_min'] >= .8 and envelope['N_max'] <= .84
        inside = inside and fields['q_max'] <= .02 and fields['w_max'] <= .03 and numerical.max(abs(numerical.diff(packed[system.slices[0]]) / numerical.diff(basis.faces))) <= .002
        if not inside:
            raise ValueError('Configuration not in the common inverse box.')
        f_min, n_min, n_max = .65, .8, .84
        m_max, p_max = 60025 / 1024, 16807 / 640
        q_max, w_max, mass_r = .02, .03, .002
        sigma_center, sigma_radius = 1.23, .02
        inverse_bound = 175 / 118
    else:
        raise ValueError('Use the certified common box; no sampled inverse promotion.')
    length, inner, kappa = envelope['length'], basis.radii[0], system.kappa
    denominator = inner * f_min
    root_length = numerical.sqrt(length)
    node_length = 17 * length / 16
    node_root = numerical.sqrt(node_length)
    poincare = numerical.sqrt(17 / 16) * length
    gram = float(include_gram)
    energy_root = numerical.sqrt(max(0.0, 2 * scalar['energy']))
    unused_velocity_norm, velocity_gradient = affine_norms(packed[system.slices[2]][[0, -1]], length)
    unused_lift_norm, lift_gradient = affine_norms(system.scalar[[0, -1]], length)
    acceleration_norm, unused_acceleration_gradient = affine_norms(endpoint_acceleration, length)
    q_gradient_bound = energy_root / numerical.sqrt(envelope['p_min']) + velocity_gradient
    affine_force_bound = 33 * envelope['p_lipschitz'] * lift_gradient / numerical.sqrt(envelope['m_min'])
    graph_bound = energy_root + affine_force_bound
    scalar_drive = graph_bound + numerical.sqrt(m_max) * acceleration_norm
    c_mass = numerical.sqrt(m_max) * q_max * length / denominator
    c_lapse = numerical.sqrt(m_max) * q_max / n_min
    gravity_cross = n_max / (kappa * inner * f_min**1.5)
    gravity_diagonal = 3 * n_max * mass_r / (kappa * inner**2 * f_min**2.5)
    a_density = gravity_diagonal + 1.5 * m_max * q_max**2 / denominator**2 + .5 * p_max * w_max**2 / denominator**2
    a_gram_density = gram * 2 * p_max * w_max**2 / denominator**2
    b_density = mass_r / (kappa * inner * f_min**1.5) + .5 * (m_max * q_max**2 + p_max * w_max**2) / (denominator * n_min)
    b_gram_density = gram * 2 * p_max * w_max**2 / (denominator * n_min)
    lift_mass_coefficient = a_density * length * root_length + gravity_cross * root_length + a_gram_density * poincare * node_root
    lift_lapse_coefficient = b_density * root_length + b_gram_density * node_root
    direct_mass = p_max * w_max / denominator * (length + gram * numerical.sqrt(8) * poincare) * q_gradient_bound + root_length * abs(clock_rate) / kappa
    direct_lapse = p_max * w_max / n_min * (1 + gram * numerical.sqrt(8)) * q_gradient_bound
    mass_source = direct_mass + c_mass * scalar_drive + lift_mass_coefficient * abs(inner_mass_rate)
    lapse_source = direct_lapse + c_lapse * scalar_drive + lift_lapse_coefficient * abs(inner_mass_rate)
    source_dual = numerical.hypot(mass_source, lapse_source)
    response = inverse_bound * source_dual
    mass_sup = abs(inner_mass_rate) + root_length * response
    width_max, row_gap = 59 / 48, 527 / 2304
    principal_margin = (sigma_center * row_gap - sigma_radius * width_max) / kappa
    row_direct = width_max * (p_max * w_max / denominator * (root_length + gram * numerical.sqrt(8) * node_root) * q_gradient_bound + abs(clock_rate) / kappa + numerical.sqrt(m_max) * q_max * root_length / denominator * scalar_drive)
    row_mass = width_max * (a_density * length * mass_sup + gravity_cross * (mass_sup + root_length * response) + a_gram_density * node_length * mass_sup)
    row_lapse_lower = width_max * (b_density * root_length + b_gram_density * node_root) * response
    lapse_sup = (row_direct + row_mass + row_lapse_lower) / principal_margin
    theta_sup = lapse_sup / n_min + mass_sup / denominator
    return {'energy': scalar['energy'], 'q_gradient_bound': float(q_gradient_bound), 'affine_force_bound': float(affine_force_bound), 'graph_force_bound': float(graph_bound), 'velocity_boundary_m_norm_bound': float(numerical.sqrt(m_max) * acceleration_norm), 'rho_time_norm_bound': float(numerical.sqrt(8) * w_max * q_gradient_bound), 'source_mass_dual_bound': float(mass_source), 'source_lapse_dual_bound': float(lapse_source), 'source_dual_bound': float(source_dual), 'metric_response_bound': float(response), 'mass_rate_sup_bound': float(mass_sup), 'lapse_rate_sup_bound': float(lapse_sup), 'clock_log_rate_sup_bound': float(theta_sup), 'lapse_principal_margin': float(principal_margin), 'normalized_row_direct_bound': float(row_direct), 'normalized_row_mass_bound': float(row_mass), 'normalized_row_lapse_lower_bound': float(row_lapse_lower), 'coefficient_spatial_Lipschitz_input': envelope['p_lipschitz'], 'inner_mass_rate_input': float(inner_mass_rate), 'outer_clock_rate_input': float(clock_rate), 'mass_lift_dual_bound': float(abs(inner_mass_rate) * numerical.hypot(lift_mass_coefficient, lift_lapse_coefficient)), 'direct_metric_source_bound': float(numerical.hypot(direct_mass, direct_lapse)), 'C_operator_bound': float(numerical.hypot(c_mass, c_lapse)), 'envelope': envelope}


def independent_first_source(system, packed, include_gram, blocks, scalar, lift, clock_rate):
    basis = system.basis
    radius, weights = basis.quadrature, basis.quadrature_weights
    mass = basis.face_value @ packed[system.slices[0]]
    lapse = basis.node_value @ packed[system.slices[1]]
    spatial_f = 1 - 2 * mass / radius
    denominator = radius * spatial_f
    density = radius**2 * lapse * numerical.sqrt(spatial_f)
    scalar_gradient = scalar['radial'] @ scalar['configuration']
    mass_source = basis.face_value[:, 1:].T @ (weights * density / denominator * scalar_gradient * scalar['q_radial'])
    lapse_source = -basis.node_value.T @ (weights * density / lapse * scalar_gradient * scalar['q_radial'])
    if include_gram:
        node_f = 1 - 2 * basis.face_to_node @ packed[system.slices[0]] / basis.radii
        node_lapse = packed[system.slices[1]]
        node_density = basis.radii**2 * node_lapse * numerical.sqrt(node_f)
        mass_source += basis.face_to_node[:, 1:].T @ (scalar['rho_time'] * node_density / (basis.radii * node_f))
        lapse_source -= scalar['rho_time'] * node_density / node_lapse
    mass_source[-1] -= clock_rate / system.kappa
    metric_data = numerical.concatenate([mass_source, lapse_source])
    metric_indices, velocity_indices = blocks['metric_indices'], blocks['velocity_indices']
    metric_lift = blocks['jacobian'][metric_indices, :] @ lift
    velocity_lift = blocks['jacobian'][velocity_indices, :] @ lift
    effective = -metric_data + blocks['coupling'] @ scalar['graph_force'] - metric_lift + blocks['coupling'] @ numerical.linalg.solve(blocks['scalar_mass'], velocity_lift)
    return {'metric_data': metric_data, 'source': effective}


def normalized_mass_rows(basis, vector):
    widths = numerical.diff(basis.faces)
    return widths / basis.spacing * numerical.cumsum(vector[::-1])[::-1]
