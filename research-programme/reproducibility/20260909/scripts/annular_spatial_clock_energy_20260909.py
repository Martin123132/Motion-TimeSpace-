import math

import numpy as numerical


def multiply(first, second):
    result = numerical.zeros_like(first + second)
    for order in range(first.shape[0]):
        for split in range(order + 1):
            result[order] += first[split] * second[order - split]
    return result


def power(series, exponent):
    normalized = series / series[0]
    normalized = normalized.copy()
    normalized[0] -= 1
    term = numerical.zeros_like(series)
    term[0] = 1
    result = term.copy()
    coefficient = 1.0
    for order in range(1, series.shape[0]):
        term = multiply(term, normalized)
        coefficient *= (exponent - order + 1) / order
        result += coefficient * term
    return result * series[0]**exponent


def radial_derivative(series):
    result = numerical.zeros_like(series)
    for order in range(series.shape[0] - 1):
        result[order] = (order + 1) * series[order + 1]
    return result


def linear_series(knots, values, points, side):
    left = numerical.clip(numerical.searchsorted(knots, points, side=side) - 1, 0, knots.size - 2)
    width = knots[left + 1] - knots[left]
    slope = (values[left + 1] - values[left]) / width
    result = numerical.zeros((4, points.size), dtype=numerical.result_type(values))
    result[0], result[1] = values[left] + slope * (points - knots[left]), slope
    return result


def scalar_series(basis, values, slope_coordinates, points, side):
    left = numerical.clip(numerical.searchsorted(basis.radii, points, side=side) - 1, 0, basis.radii.size - 2)
    fraction = (points - basis.radii[left]) / basis.spacing
    derivative = basis.derivative @ values + slope_coordinates / basis.spacing
    first, second = values[left], values[left + 1]
    tangent_first, tangent_second = derivative[left], derivative[left + 1]
    spacing = basis.spacing
    polynomial = numerical.stack([first, spacing * tangent_first, -3 * first + 3 * second - spacing * (2 * tangent_first + tangent_second), 2 * first - 2 * second + spacing * (tangent_first + tangent_second)])
    result = numerical.zeros_like(polynomial)
    for order in range(4):
        for degree in range(order, 4):
            result[order] += math.comb(degree, order) * polynomial[degree] * fraction**(degree - order) / spacing**order
    return result


def profile(system, packed, speed, points, side='right'):
    if any(system.constants[name] != 0 for name in ['b2', 'b3', 'm_chi', 'Lambda']):
        raise ValueError('Canonical branch only.')
    basis = system.basis
    radius = numerical.zeros((4, points.size))
    radius[0], radius[1] = points, 1
    mass = linear_series(basis.faces, packed[system.slices[0]], points, side)
    lapse = linear_series(basis.radii, packed[system.slices[1]], points, side)
    mass_rate = linear_series(basis.faces, speed[system.slices[0]], points, side)
    lapse_rate = linear_series(basis.radii, speed[system.slices[1]], points, side)
    spatial_f = -2 * multiply(mass, power(radius, -1))
    spatial_f[0] += 1
    characteristic = multiply(lapse, power(spatial_f, .5))
    inverse = power(characteristic, -1)
    theta = multiply(lapse_rate, power(lapse, -1)) - multiply(mass_rate, power(multiply(radius, spatial_f), -1))
    scalar = scalar_series(basis, system.scalar, system.slope, points, side)
    velocity = scalar_series(basis, packed[system.slices[2]], packed[system.slope_slice], points, side)
    acceleration = scalar_series(basis, speed[system.slices[2]], speed[system.slope_slice], points, side)
    normalized = multiply(velocity, inverse)
    gradient = radial_derivative(scalar)
    normalized_time = multiply(acceleration, inverse) - multiply(theta, normalized)
    gradient_time = radial_derivative(velocity)
    characteristic_r = radial_derivative(characteristic)
    upper = characteristic_r + 2 * multiply(characteristic, power(radius, -1))
    remainder_v = normalized_time - multiply(characteristic, radial_derivative(gradient)) - multiply(upper, gradient)
    remainder_w = gradient_time - multiply(characteristic, radial_derivative(normalized)) - multiply(characteristic_r, normalized)
    factors = numerical.array([1., 1., 2., 6.])[:, None]
    return {'v': factors * normalized, 'w': factors * gradient, 'v_time': factors * normalized_time, 'w_time': factors * gradient_time, 'c': factors * characteristic, 'theta': factors * theta, 'B_upper': factors * upper, 'B_lower': factors * characteristic_r, 'r_v': factors * remainder_v, 'r_w': factors * remainder_w}


def energy(system, packed, speed, points, weights):
    data = profile(system, packed, speed, points)
    characteristic = data['c'][0]
    energy_levels = .5 * numerical.sum(weights[None, :] / characteristic[None, :] * (data['v'][:3]**2 + data['w'][:3]**2), axis=1)
    direct_levels = numerical.sum(weights[None, :] / characteristic[None, :] * (data['v'][:3] * data['v_time'][:3] + data['w'][:3] * data['w_time'][:3] - .5 * data['theta'][0] * (data['v'][:3]**2 + data['w'][:3]**2)), axis=1)
    commuted_v, commuted_w = numerical.zeros_like(data['v'][:3]), numerical.zeros_like(data['w'][:3])
    for order in range(3):
        for split in range(1, order + 1):
            coefficient = math.comb(order, split) * data['c'][split]
            commuted_v[order] += coefficient * data['w'][order + 1 - split]
            commuted_w[order] += coefficient * data['v'][order + 1 - split]
        for split in range(order + 1):
            coefficient = math.comb(order, split)
            commuted_v[order] += coefficient * data['B_upper'][split] * data['w'][order - split]
            commuted_w[order] += coefficient * data['B_lower'][split] * data['v'][order - split]
    reaction = numerical.sum(weights[None, :] / characteristic[None, :] * (data['v'][:3] * commuted_v + data['w'][:3] * commuted_w - .5 * data['theta'][0] * (data['v'][:3]**2 + data['w'][:3]**2)), axis=1)
    residual_work = numerical.sum(weights[None, :] / characteristic[None, :] * (data['v'][:3] * data['r_v'][:3] + data['w'][:3] * data['r_w'][:3]), axis=1)
    principal = numerical.sum(weights[None, :] * (data['v'][:3] * data['w'][1:4] + data['w'][:3] * data['v'][1:4]), axis=1)
    knots = numerical.unique(numerical.concatenate([system.basis.radii, system.basis.faces]))
    left = profile(system, packed, speed, knots, 'left')
    right = profile(system, packed, speed, knots, 'right')
    left_flux = left['v'][:3] * left['w'][:3]
    right_flux = right['v'][:3] * right['w'][:3]
    outer_flux = left_flux[:, -1] - right_flux[:, 0]
    interface_flux = numerical.sum(left_flux[:, 1:-1] - right_flux[:, 1:-1], axis=1)
    quadrature_ibp = principal - outer_flux - interface_flux
    residual_norm = numerical.sqrt(numerical.sum(weights[None, :] / characteristic[None, :] * (data['r_v'][:3]**2 + data['r_w'][:3]**2)))
    return {'energy_levels': energy_levels, 'direct_rate_levels': direct_levels, 'reaction_levels': reaction, 'residual_work_levels': residual_work, 'outer_flux_levels': outer_flux, 'interface_flux_levels': interface_flux, 'quadrature_ibp_levels': quadrature_ibp, 'residual_norm': residual_norm, 'r_v': data['r_v'][:3], 'r_w': data['r_w'][:3], 'v': data['v'][:3], 'w': data['w'][:3], 'c': data['c'], 'theta': data['theta'][0], 'interface_v_jump': left['v'][:3, 1:-1] - right['v'][:3, 1:-1], 'interface_w_jump': left['w'][:3, 1:-1] - right['w'][:3, 1:-1], 'commuted_v_error': data['v_time'][:3] - data['c'][0] * data['w'][1:4] - commuted_v - data['r_v'][:3], 'commuted_w_error': data['w_time'][:3] - data['c'][0] * data['v'][1:4] - commuted_w - data['r_w'][:3]}


def bulk_bounds(lapse_radial_sup, theta_sup):
    inner, length = 47 / 8, .25
    f_min, f_max, lapse_max, lapse_min, mass_radial = .65, .68, .84, .8, .002
    f_first = (1 - f_min + 2 * mass_radial) / inner
    f_second, f_third = 2 * f_first / inner, 6 * f_first / inner**2
    root_first = f_first / (2 * numerical.sqrt(f_min))
    root_second = f_second / (2 * numerical.sqrt(f_min)) + f_first**2 / (4 * f_min**1.5)
    root_third = f_third / (2 * numerical.sqrt(f_min)) + 3 * f_first * f_second / (4 * f_min**1.5) + 3 * f_first**3 / (8 * f_min**2.5)
    characteristic_min, characteristic_max = lapse_min * numerical.sqrt(f_min), lapse_max * numerical.sqrt(f_max)
    first = lapse_radial_sup * numerical.sqrt(f_max) + lapse_max * root_first
    second = 2 * lapse_radial_sup * root_first + lapse_max * root_second
    third = 3 * lapse_radial_sup * root_second + lapse_max * root_third
    b_zero = first + 2 * characteristic_max / inner
    b_first = second + 2 * first / inner + 2 * characteristic_max / inner**2
    b_second_l2 = numerical.sqrt(length) * (third + 2 * second / inner + 4 * first / inner**2 + 4 * characteristic_max / inner**3)
    amplitude = numerical.hypot(.02 / characteristic_min, .03)
    growth = theta_sup + 2 * b_zero + 4 * first + second + 3 * b_first
    source = amplitude * b_second_l2 / numerical.sqrt(characteristic_min)
    return {name: float(value) for name, value in {'c_min': characteristic_min, 'c_max': characteristic_max, 'c_R_sup_broken': first, 'c_RR_sup_broken': second, 'c_RRR_sup_broken': third, 'B0_bound': b_zero, 'B1_bound': b_first, 'B2_L2_broken_bound': b_second_l2, 'growth_bound': growth, 'known_coefficient_source_bound': source}.items()}
