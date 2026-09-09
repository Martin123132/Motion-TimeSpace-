from types import SimpleNamespace

import numpy as numerical
import sympy as symbolic

from annular_clock_spatial_bound_20260909 import spatial_bounds
from annular_uniform_energy_bounds_20260909 import affine_norms


def local_certificates():
    coordinate = symbolic.Symbol('coordinate', real=True)
    shape = 3 * coordinate**2 - 2 * coordinate**3
    energy = symbolic.integrate(symbolic.diff(shape, coordinate)**2, (coordinate, 0, 1))
    return {'zero_slope_shape_derivative_squared': str(energy), 'derivative_constant_two_valid': bool(energy <= 4), 'error_constant_two_argument': 'Both nodal-value convex interpolation and the H1 function differ from the left value by at most sqrt(h)||f_prime||cell; hence pointwise error<=2sqrt(h)||f_prime||cell and Q-error<=2h||f_prime||.', 'projection_derivative_constant': '2+32sqrt(m_plus/m_minus)', 'quadrature_flux_constant': '1+2*16=33', 'Gram_H2_dual_constant': '32/sqrt(3)', 'scope': 'One-dimensional C1 cubic space with zero endpoint values and every slope free; actual positive composite Gauss4 projection.'}


def transport_bounds(length, m_min, m_max, p_min, p_max, p_lipschitz, theta_center, theta_radius, theta_gradient_l2, include_gram):
    if min(length, m_min, m_max, p_min, p_max) <= 0 or min(p_lipschitz, theta_radius, theta_gradient_l2) < 0:
        raise ValueError('Positive coefficient bounds and nonnegative norms required.')
    gram = 2 * p_max if include_gram else 0.0
    projection = 2 + 32 * numerical.sqrt(m_max / m_min)
    continuous_first = length / p_min
    continuous_second = (1 + p_lipschitz * continuous_first) / p_min
    interpolant_first = continuous_first + 2 * length * continuous_second
    consistency = 2 * p_max * continuous_second + 2 * p_lipschitz * interpolant_first + gram / numerical.sqrt(3) * continuous_second
    elliptic_error = consistency / p_min
    first = numerical.sqrt(m_max) * length / p_min
    second = m_max / numerical.sqrt(m_min) * (4 * continuous_second + 16 * elliptic_error)
    derivative_sup = first / numerical.sqrt(length) + numerical.sqrt(length) * second
    alpha_a = abs(theta_center) + numerical.sqrt((p_max + gram) / p_min) * projection * (theta_radius + numerical.sqrt(length) * theta_gradient_l2)
    bulk = 33 * (theta_radius * (p_lipschitz * first + p_max * second) + p_max * theta_gradient_l2 * derivative_sup) / numerical.sqrt(m_min)
    gram_transport = 32 / numerical.sqrt(3) * p_max * theta_radius * second / numerical.sqrt(m_min) if include_gram else 0.0
    alpha_l = abs(theta_center) + bulk + gram_transport
    theta_sup = abs(theta_center) + theta_radius
    return {name: float(value) for name, value in {'projection_H1_constant': projection, 'elliptic_H1_constant': first, 'elliptic_H2_constant': second, 'elliptic_derivative_sup_constant': derivative_sup, 'alpha_A_bound': alpha_a, 'alpha_L_bound': alpha_l, 'alpha_M_bound': theta_sup, 'alpha_K_bound': theta_sup, 'growth_bound': max(2 * alpha_a + theta_sup, 2 * alpha_l + theta_sup), 'bulk_transport_bound': bulk, 'Gram_transport_bound': gram_transport, 'theta_sup_bound': theta_sup, 'theta_gradient_L2_input': theta_gradient_l2}.items()}


def zero_slope_lift(basis, nodal_values):
    return numerical.concatenate([nodal_values, -basis.spacing * (basis.derivative @ nodal_values)])


def boundary_bounds(length, m_min, m_max, p_max, p_lipschitz, theta_sup, theta_gradient_l2, theta_time_qnorm, endpoint_values, endpoint_velocity, endpoint_acceleration):
    unused_norm, lift_gradient = affine_norms(endpoint_values, length)
    rate_norm, rate_gradient = affine_norms(endpoint_velocity, length)
    acceleration_norm, unused_gradient = affine_norms(endpoint_acceleration, length)
    rate_sup = float(max(abs(endpoint_velocity)))
    force = numerical.sqrt(m_max) * (acceleration_norm + theta_sup * rate_norm) + 33 * p_lipschitz * lift_gradient / numerical.sqrt(m_min)
    force_time = 2 * numerical.sqrt(m_max) * theta_sup * acceleration_norm
    force_time += m_max / numerical.sqrt(m_min) * (theta_sup**2 * rate_norm + rate_sup * theta_time_qnorm)
    force_time += 33 / numerical.sqrt(m_min) * ((p_lipschitz * theta_sup + p_max * theta_gradient_l2 / numerical.sqrt(length)) * lift_gradient + p_lipschitz * rate_gradient)
    return {'force_M_dual_bound': float(force), 'force_time_M_dual_bound': float(force_time), 'theta_time_Q_L2_input': float(theta_time_qnorm), 'theta_time_coefficient_in_force_time': float(m_max / numerical.sqrt(m_min) * rate_sup)}


def adapted_energy_feedback(system, scalar_data, static_residual, time_residual, inner_bound, clock_rate, endpoint_acceleration, include_gram, response_error=0.0, scalar_error=0.0):
    arguments = (static_residual, time_residual, inner_bound, clock_rate, endpoint_acceleration, include_gram, response_error, scalar_error)
    offset_data = dict(scalar_data, energy=0.0)
    offset = spatial_bounds(system, offset_data, *arguments)
    homogeneous_system = SimpleNamespace(basis=system.basis, scalar=numerical.zeros(system.node_count), node_count=system.node_count)
    homogeneous_data = {'energy': .5, 'velocity': numerical.zeros(2 * system.node_count)}
    slope = spatial_bounds(homogeneous_system, homogeneous_data, static_residual, numerical.zeros_like(time_residual), 0.0, 0.0, numerical.zeros(2), include_gram)
    m_max, m_min = 60025 / 1024, (47 / 8)**2 / (.84 * numerical.sqrt(.68))
    length = 1 / 4
    unused, lift_gradient = affine_norms(system.scalar[[0, -1]], length)
    rate_norm, unused = affine_norms(scalar_data['velocity'][:system.node_count][[0, -1]], length)
    acceleration_norm, unused = affine_norms(endpoint_acceleration, length)
    multiplier = numerical.sqrt(m_max) * rate_norm
    feedback = multiplier * slope['theta_sup_bound']
    constant = numerical.sqrt(m_max) * acceleration_norm + 33 * offset['p_radial_sup_bound'] * lift_gradient / numerical.sqrt(m_min) + multiplier * offset['theta_sup_bound']
    return {'theta_sup_offset': offset['theta_sup_bound'], 'theta_sup_slope': slope['theta_sup_bound'], 'theta_gradient_L2_offset': offset['theta_radial_L2_bound'], 'theta_gradient_L2_slope': slope['theta_radial_L2_bound'], 'p_lipschitz_derived': offset['p_radial_sup_bound'], 'raw_to_adapted_boundary_offset': float(constant), 'raw_to_adapted_feedback': float(feedback), 'absorption_gate': bool(feedback < 1), 'scope': 'Positive homogeneous majorant evaluation, not altered physical fields. If feedback<1: sqrt(2E_raw)<=(sqrt(2E_adapted)+offset)/(1-feedback).'}
