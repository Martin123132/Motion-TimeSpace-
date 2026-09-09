import numpy as numerical

from annular_first_derivative_energy_20260909 import canonical_matrices
from annular_gram_joint_action_20260909 import gram_matrices
from annular_uniform_energy_bounds_20260909 import affine_norms


def independent_second_forcing(system, packed, speed, include_gram, clock_second=0.0):
    if any(system.constants[name] != 0 for name in ['b2', 'b3', 'm_chi', 'Lambda']):
        raise ValueError('Canonical branch only.')
    basis = system.basis
    radius, weights = basis.quadrature, basis.quadrature_weights
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    configuration = numerical.concatenate([system.scalar, system.slope])
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    acceleration = numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]])
    mass, mass_r = basis.face_value @ packed[system.slices[0]], basis.face_gradient @ packed[system.slices[0]]
    mass_t, mass_tr = basis.face_value @ speed[system.slices[0]], basis.face_gradient @ speed[system.slices[0]]
    lapse, lapse_t = basis.node_value @ packed[system.slices[1]], basis.node_value @ speed[system.slices[1]]
    spatial_f = 1 - 2 * mass / radius
    ratio_n, ratio_mu = lapse_t / lapse, mass_t / (radius * spatial_f)
    q_value, q_radial = value @ velocity, radial @ velocity
    a_value, a_radial = value @ acceleration, radial @ acceleration
    w_value = radial @ configuration
    gravity_mass = (2 * lapse_t * mass_tr + 6 * ratio_mu * (lapse_t * mass_r + lapse * mass_tr) + 15 * ratio_mu**2 * lapse * mass_r) / (system.kappa * radius * spatial_f**1.5)
    kinetic_mass = radius / (2 * lapse * spatial_f**1.5) * (2 * a_value**2 + 4 * (-ratio_n + 3 * ratio_mu) * q_value * a_value + (2 * ratio_n**2 - 6 * ratio_n * ratio_mu + 15 * ratio_mu**2) * q_value**2)
    gradient_mass = radius * lapse / (2 * numerical.sqrt(spatial_f)) * (2 * (q_radial**2 + w_value * a_radial) + 4 * (ratio_n + ratio_mu) * w_value * q_radial + (2 * ratio_n * ratio_mu + 3 * ratio_mu**2) * w_value**2)
    flux_mass = (2 * lapse_t * ratio_mu + 3 * lapse * ratio_mu**2) / (system.kappa * numerical.sqrt(spatial_f))
    gravity_lapse = (2 * ratio_mu * mass_tr + 3 * ratio_mu**2 * mass_r) / (system.kappa * numerical.sqrt(spatial_f))
    kinetic_lapse = -radius**2 / (2 * lapse**2 * numerical.sqrt(spatial_f)) * (2 * a_value**2 + 4 * (-2 * ratio_n + ratio_mu) * q_value * a_value + (6 * ratio_n**2 - 4 * ratio_n * ratio_mu + 3 * ratio_mu**2) * q_value**2)
    gradient_lapse = -radius**2 * numerical.sqrt(spatial_f) / 2 * (2 * (q_radial**2 + w_value * a_radial) - 4 * ratio_mu * w_value * q_radial - ratio_mu**2 * w_value**2)
    node_f = 1 - 2 * basis.face_to_node @ packed[system.slices[0]] / basis.radii
    node_lapse = packed[system.slices[1]]
    node_n = speed[system.slices[1]] / node_lapse
    node_mu = (basis.face_to_node @ speed[system.slices[0]]) / (basis.radii * node_f)
    factors, sampling = gram_matrices(system.node_count)
    factor_chi, factor_q, factor_a = factors @ system.scalar, factors @ packed[system.slices[2]], factors @ speed[system.slices[2]]
    rho_t = sampling.T @ (factor_chi * factor_q) / basis.spacing
    rho_tt = sampling.T @ (factor_q**2 + factor_chi * factor_a) / basis.spacing
    atom_mass = numerical.zeros(system.node_count)
    atom_lapse = numerical.zeros(system.node_count)
    if include_gram:
        atom_mass = basis.radii * node_lapse / numerical.sqrt(node_f) * (rho_tt + 2 * (node_n + node_mu) * rho_t + (2 * node_n * node_mu + 3 * node_mu**2) * system.density)
        atom_lapse = -basis.radii**2 * numerical.sqrt(node_f) * (rho_tt - 2 * node_mu * rho_t - node_mu**2 * system.density)
    mass_row = basis.face_value.T @ (weights * (gravity_mass + kinetic_mass + gradient_mass)) + basis.face_gradient.T @ (weights * flux_mass) + basis.face_to_node.T @ atom_mass
    mass_row[-1] -= clock_second / system.kappa
    lapse_row = basis.node_value.T @ (weights * (gravity_lapse + kinetic_lapse + gradient_lapse)) + atom_lapse
    matrices = canonical_matrices(system, packed, speed, include_gram)
    density = radius**2 / (lapse * numerical.sqrt(spatial_f))
    mass_known_second = value.T @ ((weights * density * (2 * ratio_n**2 - 2 * ratio_n * ratio_mu + 3 * ratio_mu**2))[:, None] * value)
    velocity_row = mass_known_second @ velocity + 2 * matrices['M_dot'] @ acceleration + matrices['K_dot'] @ configuration + matrices['K'] @ velocity
    return {'metric_mass': mass_row, 'metric_lapse': lapse_row, 'velocity': velocity_row, 'gravity_mass': gravity_mass, 'kinetic_mass': kinetic_mass, 'gradient_mass': gradient_mass, 'flux_mass': flux_mass, 'gravity_lapse': gravity_lapse, 'kinetic_lapse': kinetic_lapse, 'gradient_lapse': gradient_lapse, 'atom_mass': atom_mass, 'atom_lapse': atom_lapse, 'rho_time': rho_t, 'rho_second': rho_tt, 'a_value': a_value, 'a_radial': a_radial, 'q_radial': q_radial, 'mass_known_second': mass_known_second}


def second_source_bound(first, transport, raw_radius, higher_radius, endpoints, shift_bound, include_gram, residual_graph=0.0, shift_time_residual_per_star=0.0, effective_second_residual=0.0, clock_second=0.0):
    if min(raw_radius, higher_radius, shift_bound, residual_graph, shift_time_residual_per_star, effective_second_residual) < 0:
        raise ValueError('Norm bounds must be nonnegative.')
    inner, outer, length, kappa = 47 / 8, 49 / 8, .25, .1
    f_min, f_max, n_min, n_max = .65, .68, .8, .84
    q_max, w_max, mu_radial_max = .02, .03, .002
    m_max, p_max = 60025 / 1024, 16807 / 640
    m_min, p_min = inner**2 / (n_max * numerical.sqrt(f_max)), inner**2 * n_min * numerical.sqrt(f_min)
    denominator, root_length = inner * f_min, numerical.sqrt(length)
    node_length = 17 * length / 16
    poincare = numerical.sqrt(17 / 16) * length
    gram = float(include_gram)
    unused, chi_lift_gradient = affine_norms(endpoints['position'], length)
    unused, q_lift_gradient = affine_norms(endpoints['velocity'], length)
    unused, a_lift_gradient = affine_norms(endpoints['acceleration'], length)
    response = first['metric_response_bound']
    mass_rate, lapse_rate = first['mass_rate_sup_bound'], first['lapse_rate_sup_bound']
    ratio_n, ratio_mu = lapse_rate / n_min, mass_rate / denominator
    theta = ratio_n + ratio_mu
    q_radial_l2 = first['q_radial_L2_bound']
    q_radial_sup = q_lift_gradient / root_length + transport['elliptic_derivative_sup_constant'] * higher_radius
    acceleration_l2 = first['scalar_acceleration_L2_bound']
    acceleration_radial = a_lift_gradient + (higher_radius + transport['alpha_A_bound'] * raw_radius + residual_graph) / numerical.sqrt(p_min)
    acceleration_sup = acceleration_l2 / root_length + root_length * acceleration_radial
    rho_zero = 2 * w_max**2 * numerical.sqrt(node_length)
    rho_time = numerical.sqrt(8) * w_max * q_radial_l2
    rho_second = numerical.sqrt(8) * (q_radial_sup * q_radial_l2 + w_max * acceleration_radial)
    gravity_mass = ((2 * lapse_rate + 6 * ratio_mu * n_max) * response + root_length * (6 * ratio_mu * lapse_rate * mu_radial_max + 15 * ratio_mu**2 * n_max * mu_radial_max)) / (kappa * inner * f_min**1.5)
    kinetic_mass = outer / (2 * n_min * f_min**1.5) * (2 * acceleration_sup * acceleration_l2 + 4 * (ratio_n + 3 * ratio_mu) * q_max * acceleration_l2 + (2 * ratio_n**2 + 6 * ratio_n * ratio_mu + 15 * ratio_mu**2) * q_max**2 * root_length)
    gradient_mass = outer * n_max / (2 * numerical.sqrt(f_min)) * (2 * q_radial_sup * q_radial_l2 + 2 * w_max * acceleration_radial + 4 * (ratio_n + ratio_mu) * w_max * q_radial_l2 + (2 * ratio_n * ratio_mu + 3 * ratio_mu**2) * w_max**2 * root_length)
    flux_mass = root_length * (2 * lapse_rate * ratio_mu + 3 * n_max * ratio_mu**2) / (kappa * numerical.sqrt(f_min))
    gravity_lapse = (2 * ratio_mu * response + 3 * ratio_mu**2 * mu_radial_max * root_length) / (kappa * numerical.sqrt(f_min))
    kinetic_lapse = outer**2 / (2 * n_min**2 * numerical.sqrt(f_min)) * (2 * acceleration_sup * acceleration_l2 + 4 * (2 * ratio_n + ratio_mu) * q_max * acceleration_l2 + (6 * ratio_n**2 + 4 * ratio_n * ratio_mu + 3 * ratio_mu**2) * q_max**2 * root_length)
    gradient_lapse = outer**2 * numerical.sqrt(f_max) / 2 * (2 * q_radial_sup * q_radial_l2 + 2 * w_max * acceleration_radial + 4 * ratio_mu * w_max * q_radial_l2 + ratio_mu**2 * w_max**2 * root_length)
    atom_mass = gram * p_max / denominator * (rho_second + 2 * (ratio_n + ratio_mu) * rho_time + (2 * ratio_n * ratio_mu + 3 * ratio_mu**2) * rho_zero)
    atom_lapse = gram * p_max / n_min * (rho_second + 2 * ratio_mu * rho_time + ratio_mu**2 * rho_zero)
    metric_mass = length * (gravity_mass + kinetic_mass + gradient_mass) + flux_mass + poincare * atom_mass + root_length * abs(clock_second) / kappa
    metric_lapse = gravity_lapse + kinetic_lapse + gradient_lapse + atom_lapse
    mass_known = numerical.sqrt(m_max) * q_max * root_length * (2 * ratio_n**2 + 2 * ratio_n * ratio_mu + 3 * ratio_mu**2)
    mass_transport = 2 * numerical.sqrt(m_max) * theta * acceleration_l2
    stiffness_transport = transport['alpha_L_bound'] * raw_radius + 33 / numerical.sqrt(m_min) * (first['p_radial_sup_bound'] * theta + p_max * first['theta_radial_L2_bound'] / root_length) * chi_lift_gradient
    stiffness_velocity = higher_radius + 33 * first['p_radial_sup_bound'] * q_lift_gradient / numerical.sqrt(m_min)
    velocity_force = mass_known + mass_transport + stiffness_transport + stiffness_velocity
    weight_lower = 1 / (kappa * n_max * f_max * (5 / 6))
    weight_upper = 1 / (kappa * n_min * f_min * (4 / 5))
    pairing_gap = 2 * weight_lower - weight_upper
    matter_time = outer**2 / (n_min * numerical.sqrt(f_min)) * (acceleration_sup * w_max + q_max * q_radial_sup + theta * q_max * w_max)
    gram_time = gram * 68 * p_max / (n_min**2 * f_min) * (acceleration_sup * w_max + q_max * q_radial_sup + 3 * theta * q_max * w_max)
    pairing_time = weight_upper * (ratio_n + 3 * ratio_mu) * shift_bound
    inner_second = 3 / pairing_gap * (matter_time + gram_time + pairing_time) + 6 * shift_time_residual_per_star / pairing_gap
    gravity_cross = n_max / (kappa * inner * f_min**1.5)
    a_density = 3 * n_max * mu_radial_max / (kappa * inner**2 * f_min**2.5) + (3 * m_max * q_max**2 + p_max * w_max**2) / (2 * denominator**2)
    a_gram = gram * 2 * p_max * w_max**2 / denominator**2
    b_density = mu_radial_max / (kappa * inner * f_min**1.5) + (m_max * q_max**2 + p_max * w_max**2) / (2 * denominator * n_min)
    b_gram = gram * 2 * p_max * w_max**2 / (denominator * n_min)
    lift_mass = a_density * length * root_length + gravity_cross * root_length + a_gram * poincare * numerical.sqrt(node_length)
    lift_lapse = b_density * root_length + b_gram * numerical.sqrt(node_length)
    coupling_mass = numerical.sqrt(m_max) * q_max * length / denominator
    coupling_lapse = numerical.sqrt(m_max) * q_max / n_min
    source_mass = metric_mass + coupling_mass * velocity_force + lift_mass * inner_second
    source_lapse = metric_lapse + coupling_lapse * velocity_force + lift_lapse * inner_second
    second_response = 175 / 118 * (numerical.hypot(source_mass, source_lapse) + effective_second_residual)
    theta_second = second_response / n_min + (root_length * inner_second + length * second_response) / denominator + root_length * (ratio_n**2 + 2 * ratio_mu**2)
    return {name: float(item) for name, item in {'higher_spatial_radius_input': higher_radius, 'q_radial_sup': q_radial_sup, 'acceleration_radial_L2': acceleration_radial, 'acceleration_L2': acceleration_l2, 'acceleration_sup': acceleration_sup, 'rho_second_dual': rho_second, 'gravity_mass': gravity_mass, 'kinetic_mass': kinetic_mass, 'gradient_mass': gradient_mass, 'flux_mass': flux_mass, 'gravity_lapse': gravity_lapse, 'kinetic_lapse': kinetic_lapse, 'gradient_lapse': gradient_lapse, 'atom_mass': atom_mass, 'atom_lapse': atom_lapse, 'metric_mass_dual': metric_mass, 'metric_lapse_dual': metric_lapse, 'velocity_force_dual': velocity_force, 'matter_shift_time_density': matter_time, 'Gram_shift_time_density': gram_time, 'pairing_shift_time_density': pairing_time, 'inner_shift_second_bound': inner_second, 'source_mass_dual': source_mass, 'source_lapse_dual': source_lapse, 'effective_source_dual': numerical.hypot(source_mass, source_lapse), 'second_metric_response': second_response, 'theta_time_Q_L2_bound': theta_second}.items()}
