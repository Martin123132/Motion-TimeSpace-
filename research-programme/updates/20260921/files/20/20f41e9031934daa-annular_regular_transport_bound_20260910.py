import numpy as numerical
from scipy.linalg import solve

from annular_endpoint_commutator_bound_20260910 import endpoint_defect_bound
from annular_spatial_clock_energy_20260909 import linear_series, profile
from annular_uniform_energy_bounds_20260909 import projection_map


def weak_commutator_parts(system, packed, speed, result):
    basis = system.basis
    free = result['free']
    selection = numerical.ix_(free, free)
    data = result['volume']
    value, radial = data['maps'][:2]
    theta_nodes = profile(system, packed, speed, basis.radii)['theta'][0]
    product = projection_map(basis, theta_nodes)[selection]
    value_error = data['theta'][:, None] * value - value @ product
    derivative_error = data['theta_r'][:, None] * value + data['theta'][:, None] * radial - radial @ product
    weighted_mass = basis.quadrature_weights * basis.quadrature**2 / data['c']
    weighted_radial = basis.quadrature_weights * basis.quadrature**2 * data['c']
    bulk = derivative_error.T @ (weighted_radial[:, None] * (radial @ result['potential']))
    load = value_error.T @ (weighted_mass[:, None] * value)
    gram = (result['matrices']['K_Gram_dot'][selection] - product.T @ result['matrices']['K_Gram'][selection]) @ result['potential']
    reconstructed = solve(result['mass'], bulk - load + gram, assume_a='sym')
    direct = result['operators']['C'] + result['operators']['A'] - result['projection'] @ data['gradient']
    lift_values = numerical.stack([1 - (basis.quadrature - basis.radii[0]) / (basis.radii[-1] - basis.radii[0]), (basis.quadrature - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])], axis=1)
    zero_trace_volume = result['projection'] @ (data['gradient'] - lift_values @ result['endpoint']['gradient'])
    return {'product': product, 'value_error': value_error, 'derivative_error': derivative_error, 'bulk': bulk, 'load': load, 'gram': gram, 'direct': direct, 'reconstructed': reconstructed, 'zero_trace_volume': zero_trace_volume}


def regular_transport_bounds(system, packed, speed, include_gram, result):
    inherited = endpoint_defect_bound(system, packed, speed, include_gram)
    envelope, curvature, elliptic = inherited['envelope'], inherited['curvature'], inherited['transport']
    length, m_min, m_max, p_min, p_max, p_lipschitz = [envelope[name] for name in ['length', 'm_min', 'm_max', 'p_min', 'p_max', 'p_lipschitz']]
    first, second, derivative_sup = [elliptic[name] for name in ['elliptic_H1_constant', 'elliptic_H2_constant', 'elliptic_derivative_sup_constant']]
    theta_lipschitz = envelope['theta_lipschitz']
    theta_first, theta_second, theta_jump, theta_curvature = [curvature[name] for name in ['theta_R_L2_bound', 'theta_RR_broken_L2_bound', 'theta_R_jump_radius', 'clock_curvature_radius']]
    center, radius = inherited['theta_center'], inherited['theta_radius']
    gram_gradient = 2 * p_max if include_gram else 0.
    projection_h1 = 2 + 32 * numerical.sqrt(m_max / m_min)
    poincare = length * numerical.sqrt(m_max / p_min)
    flux_derivative = p_lipschitz * first + p_max * second
    flux_sup = p_max * derivative_sup
    commutator_bulk = 30 * theta_lipschitz * flux_derivative + 104 * flux_sup * theta_second
    commutator_load = 3 * m_max * theta_lipschitz / numerical.sqrt(m_min)
    commutator_gram = 128 * p_max * theta_lipschitz * second if include_gram else 0.
    commutator_mass = (commutator_bulk + commutator_load + commutator_gram) / numerical.sqrt(m_min)
    inverse_gradient = 16 * numerical.sqrt((p_max + gram_gradient) / m_min)
    commutator_energy = inverse_gradient * commutator_mass
    speed_squared = p_max / m_min
    mass_values = packed[system.slices[0]]
    lapse_values = packed[system.slices[1]]
    knots = curvature['knots']
    nodal_mass = linear_series(system.basis.faces, mass_values, knots, 'right')[0]
    nodal_lapse = linear_series(system.basis.radii, lapse_values, knots, 'right')[0]
    widths = numerical.diff(knots)
    mass_gradient = numerical.diff(nodal_mass) / widths
    lapse_gradient = numerical.diff(nodal_lapse) / widths
    f_gradient = numerical.max(abs(2 * (nodal_mass[:-1] - mass_gradient * knots[:-1])) / knots[:-1]**2)
    speed_squared_gradient = 2 * envelope['N_max'] * numerical.max(abs(lapse_gradient)) * envelope['F_max'] + envelope['N_max']**2 * f_gradient
    endpoint = result['endpoint']
    trace_upper = derivative_sup * numerical.linalg.norm(endpoint['c']**2 * endpoint['theta_r'])
    gradient_volume = derivative_sup * (speed_squared_gradient * theta_first + speed_squared * theta_second) + speed_squared * theta_lipschitz * second
    gradient_jump = speed_squared * derivative_sup * theta_jump
    gradient_lift = numerical.sqrt(2 / length) * trace_upper
    zero_trace_radius = gradient_volume + numerical.sqrt(6) * gradient_jump + gradient_lift
    zero_trace_energy = numerical.sqrt(p_max + gram_gradient) * projection_h1 * zero_trace_radius
    configuration_remainder = 2 * elliptic['alpha_A_bound'] + poincare * (zero_trace_energy + commutator_energy)
    product_first = first * (radius + numerical.sqrt(length) * theta_first)
    product_second = numerical.sqrt(length) * first * theta_curvature + 2 * derivative_sup * theta_first + radius * second
    graph_constants = inherited['projection_constants']
    product_graph = graph_constants['first_constant'] * product_first + graph_constants['curvature_constant'] * product_second
    velocity_remainder = elliptic['alpha_L_bound'] + radius + product_graph
    regular_growth = max(0., 5 * center + radius + 2 * max(configuration_remainder, velocity_remainder))
    return {'theta_center': float(center), 'theta_radius': float(radius), 'theta_lipschitz': float(theta_lipschitz), 'theta_R_L2_upper': float(theta_first), 'theta_RR_broken_L2_upper': float(theta_second), 'theta_R_jump_radius': float(theta_jump), 'clock_curvature_radius': float(theta_curvature), 'p_lipschitz': float(p_lipschitz), 'speed_squared_upper': float(speed_squared), 'speed_squared_gradient_upper': float(speed_squared_gradient), 'elliptic_first': float(first), 'elliptic_second': float(second), 'elliptic_derivative_sup': float(derivative_sup), 'commutator_bulk_bilinear_over_h_upper': float(commutator_bulk), 'commutator_load_bilinear_over_h_upper': float(commutator_load), 'commutator_Gram_bilinear_over_h_upper': float(commutator_gram), 'commutator_M_norm_over_h_upper': float(commutator_mass), 'commutator_M_to_K_upper': float(commutator_energy), 'gradient_broken_derivative_M_upper': float(gradient_volume), 'gradient_value_jump_M_upper': float(gradient_jump), 'gradient_lift_derivative_M_upper': float(gradient_lift), 'zero_trace_broken_radius_M_upper': float(zero_trace_radius), 'zero_trace_M_to_K_upper': float(zero_trace_energy), 'configuration_centered_K_norm_upper': float(configuration_remainder), 'velocity_centered_M_norm_upper': float(velocity_remainder), 'regular_growth_upper': float(regular_growth), 'poincare_M_over_K': float(poincare), 'projection_H1_with_value_jumps_constant': float(projection_h1), 'scope': 'Derived analytic bound conditional on positive coefficient, Lipschitz clock, and broken curvature/jump bounds; no parent time propagation or interval certificate.'}
