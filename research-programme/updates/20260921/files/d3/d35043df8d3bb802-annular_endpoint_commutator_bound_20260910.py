import numpy as numerical
from scipy.linalg import eigvalsh, solve

from annular_H1_clock_energy_20260909 import transport_bounds
from annular_spatial_clock_energy_20260909 import linear_series, profile
from annular_uniform_energy_bounds_20260909 import metric_envelope


def clock_curvature(system, packed, speed):
    basis = system.basis
    knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
    mass = linear_series(basis.faces, packed[system.slices[0]], knots, 'right')[0]
    lapse = linear_series(basis.radii, packed[system.slices[1]], knots, 'right')[0]
    mass_time = linear_series(basis.faces, speed[system.slices[0]], knots, 'right')[0]
    lapse_time = linear_series(basis.radii, speed[system.slices[1]], knots, 'right')[0]
    denominator = knots - 2 * mass
    width = numerical.diff(knots)
    lapse_r, lapse_tr = numerical.diff(lapse) / width, numerical.diff(lapse_time) / width
    denominator_r, mass_tr = numerical.diff(denominator) / width, numerical.diff(mass_time) / width
    first_numerator = lapse_tr * lapse[:-1] - lapse_time[:-1] * lapse_r
    second_numerator = mass_tr * denominator[:-1] - mass_time[:-1] * denominator_r
    lapse_min = numerical.minimum(lapse[:-1], lapse[1:])
    denominator_min = numerical.minimum(denominator[:-1], denominator[1:])
    if min(lapse_min) <= 0 or min(denominator_min) <= 0:
        raise ValueError('Positive annular lapse and R F required.')
    first_sup = abs(first_numerator) / lapse_min**2 + abs(second_numerator) / denominator_min**2
    second_sup = 2 * abs(first_numerator * lapse_r) / lapse_min**3 + 2 * abs(second_numerator * denominator_r) / denominator_min**3
    left = profile(system, packed, speed, knots, 'left')['theta']
    right = profile(system, packed, speed, knots, 'right')['theta']
    jump = left[1, 1:-1] - right[1, 1:-1]
    pieces = []
    for field, field_knots in [(packed[system.slices[1]], basis.radii), (speed[system.slices[1]], basis.radii), (packed[system.slices[0]], basis.faces), (speed[system.slices[0]], basis.faces)]:
        first = linear_series(field_knots, field, knots, 'left')[1, 1:-1]
        second = linear_series(field_knots, field, knots, 'right')[1, 1:-1]
        pieces.append(first - second)
    lapse_jump, lapse_time_jump, mass_jump, mass_time_jump = pieces
    predicted_jump = lapse_time_jump / lapse[1:-1] - lapse_time[1:-1] * lapse_jump / lapse[1:-1]**2 - mass_time_jump / denominator[1:-1] - 2 * mass_time[1:-1] * mass_jump / denominator[1:-1]**2
    jump_norm = float(numerical.linalg.norm(jump) / numerical.sqrt(basis.spacing))
    second_norm = float(numerical.sqrt(numerical.dot(width, second_sup**2)))
    first_norm = float(numerical.sqrt(numerical.dot(width, first_sup**2)))
    return {'knots': knots, 'theta_jump': jump, 'theta_jump_from_parent_fields': predicted_jump, 'parent_slope_jumps': numerical.stack(pieces), 'theta_R_cell_sup': first_sup, 'theta_RR_cell_sup': second_sup, 'theta_R_L2_bound': first_norm, 'theta_RR_broken_L2_bound': second_norm, 'theta_R_jump_radius': jump_norm, 'clock_curvature_radius': second_norm + numerical.sqrt(6) * jump_norm}


def projection_graph_constants(envelope, include_gram):
    length, mass_min, mass_max, radial_max, radial_lipschitz = [envelope[name] for name in ['length', 'm_min', 'm_max', 'p_max', 'p_lipschitz']]
    gram_h1 = 2 * radial_max if include_gram else 0.
    gram_h2 = 32 / numerical.sqrt(3) * radial_max if include_gram else 0.
    first_constant = 33 * radial_lipschitz / numerical.sqrt(mass_min)
    curvature_constant = 14 * (33 * radial_max + gram_h2) / numerical.sqrt(mass_min)
    curvature_constant += 1024 * (radial_max + gram_h1) * numerical.sqrt(mass_max) / mass_min
    curvature_constant += 5 * length * first_constant
    return {'first_constant': float(first_constant), 'curvature_constant': float(curvature_constant)}


def endpoint_defect_bound(system, packed, speed, include_gram):
    envelope = metric_envelope(system.basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]])
    curvature = clock_curvature(system, packed, speed)
    center = (envelope['theta_max'] + envelope['theta_min']) / 2
    radius = (envelope['theta_max'] - envelope['theta_min']) / 2
    transport = transport_bounds(envelope['length'], envelope['m_min'], envelope['m_max'], envelope['p_min'], envelope['p_max'], envelope['p_lipschitz'], 0., radius, curvature['theta_R_L2_bound'], include_gram)
    constants = projection_graph_constants(envelope, include_gram)
    source_size = numerical.sqrt(envelope['m_max'] * envelope['length'] / 2)
    first_elliptic, second_elliptic, sup_elliptic = [transport[name] for name in ['elliptic_H1_constant', 'elliptic_H2_constant', 'elliptic_derivative_sup_constant']]
    source_first = source_size * first_elliptic * (radius + numerical.sqrt(envelope['length']) * curvature['theta_R_L2_bound'])
    source_curvature = source_size * (numerical.sqrt(envelope['length']) * first_elliptic * curvature['clock_curvature_radius'] + 2 * sup_elliptic * curvature['theta_R_L2_bound'] + radius * second_elliptic)
    bound = (3 * abs(center) + radius + transport['alpha_L_bound']) * source_size
    bound += constants['first_constant'] * source_first + constants['curvature_constant'] * source_curvature
    return {'envelope': envelope, 'curvature': curvature, 'transport': transport, 'projection_constants': constants, 'theta_center': float(center), 'theta_radius': float(radius), 'endpoint_lift_M_bound': float(source_size), 'product_first_L2_bound': float(source_first), 'product_curvature_bound': float(source_curvature), 'endpoint_transport_M_bound': float(bound)}


def exact_defect(matrices, free, lift, operators, value, weights, theta, center):
    mass, stiffness = matrices['M'][numerical.ix_(free, free)], matrices['K'][numerical.ix_(free, free)]
    endpoint = solve(mass, (matrices['M'] @ lift)[free], assume_a='sym')
    endpoint_time = solve(mass, (matrices['M_dot'] @ lift)[free] - matrices['M_dot'][numerical.ix_(free, free)] @ endpoint, assume_a='sym')
    direct = endpoint_time - operators['velocity_transport'] @ endpoint
    potential = solve(stiffness, mass @ endpoint, assume_a='sym')
    projected_product = solve(mass, value[:, free].T @ ((weights * (theta - center))[:, None] * (value[:, free] @ potential)), assume_a='sym')
    projected_affine = solve(mass, value[:, free].T @ ((weights * (theta - center))[:, None] * (value @ lift)), assume_a='sym')
    residual_clock = operators['C'] - center * numerical.eye(free.size)
    constant_piece = -3 * center * endpoint
    affine_piece = -projected_affine
    stiffness_piece = -residual_clock @ endpoint
    product_piece = -operators['L'] @ projected_product
    reconstructed = constant_piece + affine_piece + stiffness_piece + product_piece
    operator_norm = numerical.sqrt(max(float(eigvalsh(direct.T @ mass @ direct)[-1]), 0.))
    return {'direct': direct, 'reconstructed': reconstructed, 'endpoint': endpoint, 'potential': potential, 'projected_product': projected_product, 'product_graph': -product_piece, 'pieces': numerical.stack([constant_piece, affine_piece, stiffness_piece, product_piece]), 'M_operator_norm': float(operator_norm)}
