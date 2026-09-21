import numpy as numerical
from scipy.linalg import solve

from annular_metric_flux_jets_20260909 import SecondJet, canonical_constraint_jet
from annular_gram_joint_action_20260909 import gram_matrices
from annular_first_derivative_energy_20260909 import affine_lift_matrix
from annular_paired_variational_energy_20260910 import scalar_maps
from annular_spatial_clock_energy_20260909 import linear_series, profile
from annular_endpoint_commutator_bound_20260910 import clock_curvature
from annular_H1_clock_energy_20260909 import transport_bounds, boundary_bounds
from annular_uniform_energy_bounds_20260909 import metric_envelope


def weighted_matrix(jet, first, second, weights):
    return SecondJet(*[first.T @ ((weights * getattr(jet, name))[:, None] * second) for name in ['value', 'first', 'second']])


def matrix_product(matrix, vector):
    return SecondJet(matrix.value @ vector.value, matrix.first @ vector.value + matrix.value @ vector.first, matrix.second @ vector.value + 2 * matrix.first @ vector.first + matrix.value @ vector.second)


def matrix_solve(matrix, vector):
    value = solve(matrix.value, vector.value, assume_a='sym')
    first = solve(matrix.value, vector.first - matrix.first @ value, assume_a='sym')
    second = solve(matrix.value, vector.second - matrix.second @ value - 2 * matrix.first @ first, assume_a='sym')
    return SecondJet(value, first, second)


def canonical_matrix_jets(system, packed, speed, second, include_gram):
    if any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Canonical zero-potential branch only.')
    basis = system.basis
    mass = SecondJet(packed[system.slices[0]], speed[system.slices[0]], second[system.slices[0]])
    lapse = SecondJet(packed[system.slices[1]], speed[system.slices[1]], second[system.slices[1]])
    mass_q, lapse_q = mass.mapped(basis.face_value), lapse.mapped(basis.node_value)
    spatial_f = 1 - 2 * mass_q / basis.quadrature
    density = basis.quadrature**2 / (lapse_q * spatial_f**.5)
    radial_density = basis.quadrature**2 * lapse_q * spatial_f**.5
    maps = scalar_maps(basis, basis.quadrature)
    mass_matrix = weighted_matrix(density, maps[0], maps[0], basis.quadrature_weights)
    stiffness = weighted_matrix(radial_density, maps[1], maps[1], basis.quadrature_weights)
    gram = SecondJet(numerical.zeros_like(stiffness.value))
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        coefficient = basis.radii**2 * lapse * (1 - 2 * mass.mapped(basis.face_to_node) / basis.radii)**.5
        sampled = coefficient.mapped(sampling)
        embed = numerical.pad(factors, ((0, 0), (0, system.node_count)))
        gram = weighted_matrix(sampled, embed, embed, numerical.ones(factors.shape[0]) / basis.spacing)
        stiffness += gram
    return {'M': mass_matrix, 'K': stiffness, 'Gram': gram}


def shift_second_jet(system, packed, speed, second, include_gram):
    basis, links = system.basis, system.links
    mass = SecondJet(packed[system.slices[0]], speed[system.slices[0]], second[system.slices[0]])
    lapse = SecondJet(packed[system.slices[1]], speed[system.slices[1]], second[system.slices[1]])
    velocity = SecondJet(numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]]), numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]]), numerical.concatenate([second[system.slices[2]], second[system.slope_slice]]))
    configuration = SecondJet(numerical.concatenate([system.scalar, system.slope]), velocity.value, velocity.first)
    maps = scalar_maps(basis, basis.quadrature)
    lapse_q = lapse.mapped(basis.node_value)
    spatial_f = 1 - 2 * mass.mapped(basis.face_value) / basis.quadrature
    pairing = weighted_matrix(1 / (system.kappa * lapse_q * spatial_f**1.5), basis.face_value, basis.face_value, basis.quadrature_weights)
    matter = (-basis.quadrature_weights * basis.quadrature**2 * velocity.mapped(maps[0]) * configuration.mapped(maps[1]) / (lapse_q * spatial_f**.5)).mapped(basis.face_value.T)
    gram = SecondJet(numerical.zeros(system.face_count))
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        scalar = configuration.selected(slice(0, system.node_count))
        nodal_velocity = velocity.selected(slice(0, system.node_count))
        coefficient = basis.radii**2 * lapse * (1 - 2 * mass.mapped(basis.face_to_node) / basis.radii)**.5
        leading, leading_time, sampled = scalar.mapped(factors), nodal_velocity.mapped(factors), coefficient.mapped(sampling)
        current = coefficient.selected(links.node) * links.sweight * leading.selected(links.factor) * leading_time.selected(links.factor) / basis.spacing
        current -= nodal_velocity.selected(links.node) * links.tweight * sampled.selected(links.factor) * leading.selected(links.factor) / basis.spacing
        inverse = 1 / (lapse.mapped(links.node_value)**2 * (1 - 2 * mass.mapped(links.face_value) / links.points))
        matrix = SecondJet(*[links.integrate(getattr(inverse, name)[:, None] * links.face_value).T for name in ['value', 'first', 'second']])
        gram = -matrix_product(matrix, current)
    return {'speed': matrix_solve(pairing, gram - matter), 'pairing': pairing, 'matter': matter, 'Gram': gram}


def parent_third_jet(system, packed, speed, second, clock_rate, include_gram):
    matrices = canonical_matrix_jets(system, packed, speed, second, include_gram)
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    acceleration = numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]])
    jerk = numerical.concatenate([second[system.slices[2]], second[system.slope_slice]])
    configuration = numerical.concatenate([system.scalar, system.slope])
    momentum = numerical.concatenate([system.momentum, system.slope_momentum])
    momentum_rate = -matrices['K'].value @ configuration
    momentum_second = -matrices['K'].first @ configuration - matrices['K'].value @ velocity
    momentum_third = -matrices['K'].second @ configuration - 2 * matrices['K'].first @ velocity - matrices['K'].value @ acceleration
    endpoints = [0, system.node_count - 1]
    for vector in [momentum_rate, momentum_second, momentum_third]:
        vector[endpoints] = 0.
    shift = shift_second_jet(system, packed, speed, second, include_gram)
    step = 1e-25

    def residual(third):
        packed_jet = SecondJet(packed + 1j * step * speed, speed + 1j * step * second, second + 1j * step * third)
        configuration_jet = SecondJet(configuration + 1j * step * velocity, velocity + 1j * step * acceleration, acceleration + 1j * step * jerk)
        momentum_jet = SecondJet(momentum + 1j * step * momentum_rate, momentum_rate + 1j * step * momentum_second, momentum_second + 1j * step * momentum_third)
        clock = SecondJet(system.outer_clock + 1j * step * clock_rate, clock_rate)
        return canonical_constraint_jet(system, packed_jet, configuration_jet, momentum_jet, clock, include_gram)

    known = residual(numerical.zeros_like(packed)).second.imag / step
    jacobian = system.evaluate(packed, include_gram)[2]
    third = numerical.zeros_like(packed)
    third[system.fixed] = [shift['speed'].second[0], 0., 0.]
    forced = (known + jacobian @ third)[system.free]
    free_jacobian = jacobian[numerical.ix_(system.free, system.free)]
    third[system.free] = solve(free_jacobian, -forced, assume_a='sym')
    completed = residual(third)
    inverse = solve(free_jacobian, numerical.eye(system.free.size), assume_a='sym')
    bound = max(float(max(abs(third[system.fixed]))), float(numerical.linalg.norm(inverse, numerical.inf) * max(abs(forced))))
    return {'third': third, 'known_third': known, 'third_constraint_residual': completed.second.imag / step, 'second_constraint_residual': completed.second.real, 'first_constraint_residual': completed.first.real, 'third_sup_upper': bound, 'free_inverse_infinity_norm': float(numerical.linalg.norm(inverse, numerical.inf)), 'shift': shift, 'matrices': matrices, 'momentum_rate': momentum_rate, 'momentum_second': momentum_second, 'momentum_third': momentum_third, 'configuration_jet': [configuration, velocity, acceleration, jerk], 'momentum_jet': [momentum, momentum_rate, momentum_second, momentum_third]}


def boundary_source(system, packed, speed, second, include_gram, lift, lift_time, lift_second):
    basis = system.basis
    count = system.node_count
    free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
    selection = numerical.ix_(free, free)
    matrices = canonical_matrix_jets(system, packed, speed, second, include_gram)
    force = -(matrices['M'].value @ lift_second + matrices['M'].first @ lift_time + matrices['K'].value @ lift)[free]
    force_time = -(2 * matrices['M'].first @ lift_second + matrices['M'].second @ lift_time + matrices['K'].first @ lift + matrices['K'].value @ lift_time)[free]
    potential = numerical.zeros(2 * count, dtype=numerical.result_type(packed, speed, second))
    potential[free] = solve(matrices['K'].value[selection], force, assume_a='sym')
    potential_time = numerical.zeros_like(potential)
    potential_time[free] = solve(matrices['K'].value[selection], force_time - matrices['K'].first[selection] @ potential[free], assume_a='sym')

    def data(points):
        maps = scalar_maps(basis, points)
        clock = profile(system, packed, speed, points)
        mass = linear_series(basis.faces, packed[system.slices[0]], points, 'right')[0]
        mass_time = linear_series(basis.faces, speed[system.slices[0]], points, 'right')[0]
        mass_second = linear_series(basis.faces, second[system.slices[0]], points, 'right')[0]
        lapse = linear_series(basis.radii, packed[system.slices[1]], points, 'right')[0]
        lapse_time = linear_series(basis.radii, speed[system.slices[1]], points, 'right')[0]
        lapse_second = linear_series(basis.radii, second[system.slices[1]], points, 'right')[0]
        theta_time = lapse_second / lapse - (lapse_time / lapse)**2 - mass_second / (points - 2 * mass) - 2 * (mass_time / (points - 2 * mass))**2
        characteristic, characteristic_r = clock['c'][:2]
        theta, theta_r = clock['theta'][:2]
        ratio = 2 * characteristic**2 / points + characteristic * characteristic_r
        coefficient = characteristic**2 * theta_r
        ell_time, ell_second, ell_time_r = maps[0] @ lift_time, maps[0] @ lift_second, maps[1] @ lift_time
        full_potential_r = maps[1] @ (potential + lift)
        potential_rr = maps[2] @ potential
        old_beta = -(ratio * theta + coefficient) * full_potential_r - characteristic**2 * theta * potential_rr - ratio * ell_time_r - 2 * theta * ell_second + (theta**2 - theta_time) * ell_time
        reduced = -coefficient * full_potential_r - ratio * ell_time_r - 3 * theta * ell_second + (2 * theta**2 - theta_time) * ell_time
        return {'old_beta': old_beta, 'beta': reduced, 'maps': maps, 'c': characteristic, 'theta': theta, 'theta_r': theta_r, 'theta_time': theta_time, 'ratio': ratio, 'coefficient': coefficient, 'full_potential_r': full_potential_r, 'potential_rr': potential_rr, 'ell_time': ell_time, 'ell_second': ell_second, 'ell_time_r': ell_time_r}

    interior, endpoint = data(basis.quadrature), data(basis.radii[[0, -1]])
    mass = matrices['M'].value[selection]
    value = interior['maps'][0][:, free]
    weights = basis.quadrature_weights * basis.quadrature**2 / interior['c']
    projection = solve(mass, value.T * weights, assume_a='sym')
    xi = -interior['ell_second'] + interior['theta'] * interior['ell_time']
    gradient = -interior['coefficient'] * interior['full_potential_r']
    weak_remainder = solve(mass, (matrices['K'].first @ (potential + lift))[free], assume_a='sym') - projection @ (interior['theta'] * xi + gradient)
    affine_quadrature = solve(mass, (matrices['K'].value @ lift_time)[free], assume_a='sym') + projection @ (interior['ratio'] * interior['ell_time_r'])
    actual = solve(mass, matrices['K'].first[selection] @ potential[free] - force_time, assume_a='sym')
    lift_map = affine_lift_matrix(basis)
    endpoint_lift = solve(mass, (matrices['M'].value @ lift_map)[free], assume_a='sym')
    regular = projection @ (interior['beta'] - interior['maps'][0] @ lift_map @ endpoint['beta']) + weak_remainder + affine_quadrature
    return {'matrices': matrices, 'free': free, 'force': force, 'force_time': force_time, 'potential': potential, 'potential_time': potential_time, 'interior': interior, 'endpoint': endpoint, 'actual': actual, 'projection': projection, 'weak_remainder': weak_remainder, 'affine_quadrature': affine_quadrature, 'endpoint_lift': endpoint_lift, 'regular': regular, 'xi': xi}


def endpoint_time_data(system, packed, speed, second, third, source, lift, lift_time, lift_second):
    basis = system.basis
    points = basis.radii[[0, -1]]
    fields = []
    for selection, knots in [(system.slices[0], basis.faces), (system.slices[1], basis.radii)]:
        fields.append([linear_series(knots, order[selection], points, 'right') for order in [packed, speed, second, third]])
    mass, mass_time, mass_second, mass_third = fields[0]
    lapse, lapse_time, lapse_second, lapse_third = fields[1]
    denominator, denominator_r = points - 2 * mass[0], 1 - 2 * mass[1]
    theta_tt = lapse_third[0] / lapse[0] - 3 * lapse_time[0] * lapse_second[0] / lapse[0]**2 + 2 * (lapse_time[0] / lapse[0])**3
    theta_tt -= mass_third[0] / denominator + 6 * mass_time[0] * mass_second[0] / denominator**2 + 8 * (mass_time[0] / denominator)**3
    theta_tr = lapse_second[1] / lapse[0] - lapse_second[0] * lapse[1] / lapse[0]**2 - 2 * lapse_time[0] / lapse[0] * (lapse_time[1] / lapse[0] - lapse_time[0] * lapse[1] / lapse[0]**2)
    theta_tr -= mass_second[1] / denominator - mass_second[0] * denominator_r / denominator**2 + 4 * mass_time[0] * mass_time[1] / denominator**2 - 4 * mass_time[0]**2 * denominator_r / denominator**3
    endpoint = source['endpoint']
    theta, theta_r, theta_t, characteristic, ratio, coefficient = [endpoint[name] for name in ['theta', 'theta_r', 'theta_time', 'c', 'ratio', 'coefficient']]
    ratio_time = 2 * theta * ratio + coefficient
    coefficient_time = characteristic**2 * (2 * theta * theta_r + theta_tr)
    flux_ratio_time = ratio * (2 * theta**2 + theta_t) + 3 * characteristic**2 * theta * theta_r + characteristic**2 * theta_tr
    maps = endpoint['maps']
    full_time_r = maps[1] @ (source['potential_time'] + lift_time)
    old_rate = -flux_ratio_time * endpoint['full_potential_r'] - (ratio * theta + coefficient) * full_time_r
    old_rate -= characteristic**2 * (2 * theta**2 + theta_t) * endpoint['potential_rr'] + characteristic**2 * theta * (maps[2] @ source['potential_time'])
    old_rate -= ratio_time * endpoint['ell_time_r'] + ratio * (maps[1] @ lift_second)
    old_rate += (theta**2 - 3 * theta_t) * endpoint['ell_second'] + (2 * theta * theta_t - theta_tt) * endpoint['ell_time']
    reduced_rate = -coefficient_time * endpoint['full_potential_r'] - coefficient * full_time_r - ratio_time * endpoint['ell_time_r'] - ratio * (maps[1] @ lift_second)
    reduced_rate += (2 * theta**2 - 4 * theta_t) * endpoint['ell_second'] + (4 * theta * theta_t - theta_tt) * endpoint['ell_time']
    return {'theta_tt': theta_tt, 'theta_tr': theta_tr, 'coefficient_time': coefficient_time, 'ratio_time': ratio_time, 'old_beta_time': old_rate, 'beta_time': reduced_rate, 'full_potential_time_r': full_time_r}


def variation_bound(system, packed, speed, second, source, rates, lift, lift_time, lift_second, include_gram, parent):
    basis = system.basis
    envelope = metric_envelope(basis, packed[system.slices[0]], packed[system.slices[1]], speed[system.slices[0]], speed[system.slices[1]], second[system.slices[0]], second[system.slices[1]])
    curvature = clock_curvature(system, packed, speed)
    center = (envelope['theta_max'] + envelope['theta_min']) / 2
    radius = (envelope['theta_max'] - envelope['theta_min']) / 2
    theta_sup = abs(center) + radius
    transport = transport_bounds(envelope['length'], envelope['m_min'], envelope['m_max'], envelope['p_min'], envelope['p_max'], envelope['p_lipschitz'], center, radius, curvature['theta_R_L2_bound'], include_gram)
    endpoint_indices = [0, system.node_count - 1]
    bounds = boundary_bounds(envelope['length'], envelope['m_min'], envelope['m_max'], envelope['p_max'], envelope['p_lipschitz'], theta_sup, curvature['theta_R_L2_bound'], numerical.sqrt(envelope['length']) * envelope['theta_time_max'], lift[endpoint_indices], lift_time[endpoint_indices], lift_second[endpoint_indices])
    force = bounds['force_M_dual_bound']
    actual_source = transport['alpha_L_bound'] * force + bounds['force_time_M_dual_bound']
    endpoint = source['endpoint']
    maps = endpoint['maps']
    gradient_lift = float(max(abs(maps[1] @ lift)))
    gradient_time = float(max(abs(maps[1] @ lift_time)))
    gradient_second = abs(maps[1] @ lift_second)
    derivative_sup = transport['elliptic_derivative_sup_constant']
    full_sup = derivative_sup * force + gradient_lift
    full_time_sup = derivative_sup * actual_source + gradient_time
    theta, theta_t, coefficient, ratio = [endpoint[name] for name in ['theta', 'theta_time', 'coefficient', 'ratio']]
    value_upper = abs(coefficient) * full_sup + abs(ratio) * abs(endpoint['ell_time_r']) + 3 * abs(theta) * abs(endpoint['ell_second']) + (2 * theta**2 + abs(theta_t)) * abs(endpoint['ell_time'])
    rate_upper = abs(rates['coefficient_time']) * full_sup + abs(coefficient) * full_time_sup + abs(rates['ratio_time']) * abs(endpoint['ell_time_r']) + abs(ratio) * gradient_second
    rate_upper += (2 * theta**2 + 4 * abs(theta_t)) * abs(endpoint['ell_second']) + (4 * abs(theta * theta_t) + abs(rates['theta_tt'])) * abs(endpoint['ell_time'])
    mass_first, lapse_first = envelope['mass_rate_max'], envelope['lapse_rate_max']
    mass_second, lapse_second = envelope['mass_second_max'], envelope['lapse_second_max']
    denominator = basis.radii[0] * envelope['F_min']
    lapse_min = envelope['N_min']
    third_upper = parent['third_sup_upper']
    theta_tt_upper = third_upper / lapse_min + 3 * lapse_first * lapse_second / lapse_min**2 + 2 * lapse_first**3 / lapse_min**3
    theta_tt_upper += third_upper / denominator + 6 * mass_first * mass_second / denominator**2 + 8 * mass_first**3 / denominator**3
    parent_rate_upper = rate_upper + (theta_tt_upper - abs(rates['theta_tt'])) * abs(endpoint['ell_time'])
    full_first = transport['elliptic_H1_constant'] * force + numerical.sqrt(envelope['length']) * gradient_lift
    full_second = transport['elliptic_H2_constant'] * force
    xi_norm = numerical.sqrt(envelope['length']) * (max(abs(lift_second[endpoint_indices])) + theta_sup * max(abs(lift_time[endpoint_indices])))
    bilinear = 30 * envelope['theta_lipschitz'] * (envelope['p_lipschitz'] * full_first + envelope['p_max'] * full_second) + 104 * envelope['p_max'] * full_sup * curvature['theta_RR_broken_L2_bound'] + 3 * envelope['m_max'] * envelope['theta_lipschitz'] * xi_norm
    if include_gram:
        bilinear += 128 * envelope['p_max'] * envelope['theta_lipschitz'] * full_second
    gram_gradient = 2 * envelope['p_max'] if include_gram else 0.
    remainder_energy = 16 * numerical.sqrt((envelope['p_max'] + gram_gradient) / envelope['m_min']) * bilinear / numerical.sqrt(envelope['m_min'])
    return {'force_M_upper': float(force), 'actual_b_M_upper': float(actual_source), 'full_potential_derivative_upper': float(full_sup), 'full_potential_time_derivative_upper': float(full_time_sup), 'beta_abs_endpoint_upper': value_upper.tolist(), 'beta_time_abs_endpoint_upper': rate_upper.tolist(), 'beta_value_R2_upper': float(numerical.linalg.norm(value_upper)), 'beta_rate_R2_upper': float(numerical.linalg.norm(rate_upper)), 'theta_tt_from_parent_solve_upper': float(theta_tt_upper), 'beta_rate_parent_solve_R2_upper': float(numerical.linalg.norm(parent_rate_upper)), 'repacked_weak_remainder_K_upper': float(remainder_energy), 'scope': 'Pointwise analytic conditional bounds; TV requires an integral/time-uniform bound, not sampled summation. Third parent jet is sourced but no mesh-uniform inverse-Jacobian or interval theorem is claimed.'}
