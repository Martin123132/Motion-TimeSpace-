import numpy as numerical

from annular_parent_coefficient_box_20260910 import Box, concatenate
from annular_parent_root_residence_20260910 import canonical_maps
from annular_joint_weak_action_20260910 import joint_prototype
from annular_shift_source_schur_20260910 import matrix_solve
from annular_adm_mixed_action_20260909 import linear_value_gradient


def block(rows):
    return concatenate([concatenate(row, axis=1) for row in rows], axis=0)


def initial_gr_jet(system, packed, configuration, clock, endpoint_acceleration):
    basis, count = system.basis, system.node_count
    if system.kappa != .1 or any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the canonical zero-nonlinearity bulk GR control is implemented.')
    prototype = joint_prototype(system, Box(packed.midpoint), Box(configuration), False)
    value, gradient = canonical_maps(basis)
    face, face_gradient = basis.face_value, basis.face_gradient
    mass_map = numerical.concatenate([face, prototype['mass_lift'].midpoint], axis=1)
    mass_gradient = numerical.concatenate([face_gradient, prototype['mass_lift_gradient'].midpoint], axis=1)
    shift_map = numerical.concatenate([face, prototype['shift_test_remainder'].midpoint], axis=1)
    endpoint_nodes, endpoint_node_gradient = linear_value_gradient(basis.radii, basis.radii[:1])
    center_lapse = packed.midpoint[system.slices[1]]
    endpoint_f = 1 - 2 * packed.midpoint[0] / basis.radii[0]
    endpoint_zeta = endpoint_f * ((endpoint_nodes @ center_lapse)[:, None] * endpoint_node_gradient[:, 1:-1] - (endpoint_node_gradient @ center_lapse)[:, None] * endpoint_nodes[:, 1:-1])
    endpoint_remainder = endpoint_zeta[0] - prototype['shift_projection_coefficients'].midpoint[0]
    endpoint_shift = numerical.concatenate([numerical.eye(system.face_count)[0], endpoint_remainder])
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    radius, weights, kappa = Box(basis.quadrature), Box(basis.quadrature_weights), Box(1.) / 10
    mass_q, mass_r = Box(face) @ mass, Box(face_gradient) @ mass
    lapse_q = Box(basis.node_value) @ lapse
    velocity_coeff = packed[system.slices[2].start:]
    velocity, velocity_r = Box(value) @ velocity_coeff, Box(gradient) @ velocity_coeff
    scalar_gradient = Box(gradient) @ Box(configuration)
    spatial_f = 1 - 2 * mass_q / radius
    rho = 1 / (kappa * lapse_q * spatial_f**1.5)
    kinetic = radius**2 / (lapse_q * spatial_f**.5)
    spatial = radius**2 * lapse_q * spatial_f**.5
    flux = kappa * radius**2 * spatial_f * velocity * scalar_gradient
    pairing = Box(shift_map.T) @ ((weights * rho)[:, None] * Box(mass_map))
    mass_rate, mass_diagnostic = matrix_solve(pairing, Box(shift_map.T) @ (weights * rho * flux))
    mass_speed, mass_speed_r = Box(mass_map) @ mass_rate, Box(mass_gradient) @ mass_rate
    mass_density = lapse_q * mass_r / (kappa * radius * spatial_f**1.5) + radius * velocity**2 / (2 * lapse_q * spatial_f**1.5) + radius * lapse_q * scalar_gradient**2 / (2 * spatial_f**.5)
    mass_force = Box(mass_map.T) @ (weights * mass_density) + Box(mass_gradient.T) @ (weights * lapse_q / (kappa * spatial_f**.5))
    outer = numerical.zeros(mass_map.shape[1])
    outer[system.face_count - 1] = 1
    mass_force = mass_force - Box(outer) * clock / kappa
    bordered = concatenate([pairing[:, 1:].T, Box(endpoint_shift[None, :])], axis=0)
    loads = numerical.zeros((mass_map.shape[1], 2))
    loads[-1, 1] = 1
    lower, upper = loads.copy(), loads.copy()
    lower[:-1, 0], upper[:-1, 0] = mass_force.lo[1:], mass_force.hi[1:]
    shift_rate, shift_diagnostic = matrix_solve(bordered, Box(lower, upper))
    shift_speed = Box(shift_map) @ shift_rate
    endpoints = numerical.array([0, count - 1])
    free_scalar = numerical.array([index for index in range(2 * count) if index not in endpoints])
    free_values, end_values, lapse_values = Box(value[:, free_scalar]), Box(value[:, endpoints]), Box(basis.node_value)
    scalar_matrix = free_values.T @ ((weights * kinetic)[:, None] * free_values)
    end_matrix = free_values.T @ ((weights * kinetic)[:, None] * end_values)
    lapse_mixing = free_values.T @ ((weights * kinetic * velocity / lapse_q)[:, None] * lapse_values)
    end_mixing = end_values.T @ ((weights * kinetic * velocity / lapse_q)[:, None] * lapse_values)
    shift_mixing = free_values.T @ ((weights * kinetic * scalar_gradient)[:, None] * Box(shift_map))
    lapse_matrix = lapse_values.T @ ((weights * kinetic * velocity**2 / lapse_q**2)[:, None] * lapse_values)
    defect_mixing = lapse_values.T @ ((weights * rho * (mass_speed - flux) / lapse_q)[:, None] * Box(shift_map))
    force = -(Box(gradient[:, free_scalar].T) @ (weights * spatial * scalar_gradient))
    scalar_source = force - free_values.T @ (weights * kinetic * velocity * mass_speed / (radius * spatial_f)) - end_matrix @ Box(endpoint_acceleration)
    lapse_source_density = mass_speed_r / (kappa * spatial_f**.5) + (mass_r / (kappa * radius * spatial_f**1.5) - radius * velocity**2 / (2 * lapse_q**2 * spatial_f**1.5) + radius * scalar_gradient**2 / (2 * spatial_f**.5)) * mass_speed - radius**2 * spatial_f**.5 * scalar_gradient * velocity_r
    lapse_source = -(lapse_values.T @ (weights * lapse_source_density)) + end_mixing.T @ Box(endpoint_acceleration)
    scalar_load = shift_mixing @ shift_rate + concatenate([scalar_source[:, None], Box(numerical.zeros((free_scalar.size, 1)))], axis=1)
    lapse_load = defect_mixing @ shift_rate + concatenate([lapse_source[:, None], Box(numerical.zeros((count, 1)))], axis=1)
    coupled = block([[scalar_matrix, -lapse_mixing], [-lapse_mixing.T, lapse_matrix]])
    jet, jet_diagnostic = matrix_solve(coupled, concatenate([scalar_load, lapse_load], axis=0))
    acceleration_lower, acceleration_upper = numerical.zeros((2 * count, 2)), numerical.zeros((2 * count, 2))
    acceleration_lower[free_scalar], acceleration_upper[free_scalar] = jet.lo[:free_scalar.size], jet.hi[:free_scalar.size]
    acceleration_lower[endpoints, 0], acceleration_upper[endpoints, 0] = endpoint_acceleration, endpoint_acceleration
    acceleration = Box(acceleration_lower, acceleration_upper)
    lapse_rate = jet[free_scalar.size:]
    mass_residual = mass_force[1:, None] - pairing[:, 1:].T @ shift_rate[:, :1]
    mass_parameter_residual = -(pairing[:, 1:].T @ shift_rate[:, 1:])
    scalar_residual = scalar_matrix @ jet[:free_scalar.size] - lapse_mixing @ lapse_rate - scalar_load
    lapse_residual = -lapse_mixing.T @ jet[:free_scalar.size] + lapse_matrix @ lapse_rate - lapse_load
    return {'mass_map': mass_map, 'mass_gradient': mass_gradient, 'shift_map': shift_map, 'endpoint_shift': endpoint_shift, 'pairing': pairing, 'mass_rate': mass_rate, 'mass_speed': mass_speed, 'mass_speed_gradient': mass_speed_r, 'mass_force': mass_force, 'shift_rate': shift_rate, 'shift_speed': shift_speed, 'acceleration': acceleration, 'lapse_rate': lapse_rate, 'coupled_matrix': coupled, 'coupled_jet': jet, 'scalar_matrix': scalar_matrix, 'lapse_mixing': lapse_mixing, 'lapse_matrix': lapse_matrix, 'defect_mixing': defect_mixing, 'mass_residual': mass_residual, 'mass_parameter_residual': mass_parameter_residual, 'scalar_residual': scalar_residual, 'lapse_residual': lapse_residual, 'shift_residual': pairing @ mass_rate - Box(shift_map.T) @ (weights * rho * flux), 'boundary_trace_residual': Box(endpoint_shift) @ shift_rate - Box(numerical.array([0., 1.])), 'inner_mass_reaction': concatenate([mass_force[:1], Box(numerical.zeros(1))]) - pairing[:, 0] @ shift_rate, 'diagnostics': {'mass_rate': mass_diagnostic, 'shift_rate': shift_diagnostic, 'scalar_lapse_jet': jet_diagnostic}, 'free_scalar': free_scalar}


def differential_controls(system, packed, configuration, data, boundary_rate):
    basis = system.basis
    value, gradient = canonical_maps(basis)
    count = system.node_count
    center = packed.midpoint
    mass = basis.face_value @ center[system.slices[0]]
    mass_r = basis.face_gradient @ center[system.slices[0]]
    lapse = basis.node_value @ center[system.slices[1]]
    lapse_r = basis.node_gradient @ center[system.slices[1]]
    velocity = value @ center[system.slices[2].start:]
    scalar_gradient = gradient @ configuration
    velocity_r = gradient @ center[system.slices[2].start:]
    combine = numerical.array([1., boundary_rate])
    shift_time = data['shift_speed'].midpoint @ combine
    lapse_time = basis.node_value @ (data['lapse_rate'].midpoint @ combine)
    lapse_r_time = basis.node_gradient @ (data['lapse_rate'].midpoint @ combine)
    acceleration = value @ (data['acceleration'].midpoint @ combine)
    radius, weights = basis.quadrature, basis.quadrature_weights

    def observables(time):
        local_mass = mass + time * data['mass_speed'].midpoint
        local_mass_r = mass_r + time * data['mass_speed_gradient'].midpoint
        local_lapse, local_lapse_r = lapse + time * lapse_time, lapse_r + time * lapse_r_time
        local_velocity, local_gradient = velocity + time * acceleration, scalar_gradient + time * velocity_r
        shift = time * shift_time
        spatial_f = 1 - 2 * local_mass / radius
        scale = spatial_f**-.5
        scale_r = (local_mass_r / radius - local_mass / radius**2) * spatial_f**-1.5
        rho = 1 / (.1 * local_lapse * spatial_f**1.5)
        kinetic = radius**2 * scale / local_lapse
        momentum = value.T @ (weights * kinetic * (local_velocity - shift * local_gradient))
        mass_momentum = data['mass_map'].T @ (weights * rho * shift)
        lapse_density = local_mass_r * scale / .1 - rho * shift * data['mass_speed'].midpoint / local_lapse
        lapse_density += radius * shift**2 / .2 * (scale_r / local_lapse**2 + 2 * scale * local_lapse_r / local_lapse**3)
        lapse_density -= kinetic * (local_velocity - shift * local_gradient)**2 / (2 * local_lapse) + radius**2 * local_gradient**2 / (2 * scale)
        lapse_gradient_density = -radius * scale * shift**2 / (.2 * local_lapse**2)
        lapse_covector = basis.node_value.T @ (weights * lapse_density) + basis.node_gradient.T @ (weights * lapse_gradient_density)
        return momentum, mass_momentum, lapse_covector

    step = 1e-25
    scalar_time, mass_momentum_time, constraint_time = [quantity.imag / step for quantity in observables(1j * step)]
    spatial_f = 1 - 2 * mass / radius
    force = -(gradient.T @ (weights * radius**2 * lapse * spatial_f**.5 * scalar_gradient))
    free_scalar = data['free_scalar']
    return {'boundary_rate': boundary_rate, 'scalar_EL_midpoint_error': float(abs((scalar_time - force)[free_scalar]).max()), 'mass_EL_midpoint_error': float(abs((mass_momentum_time - data['mass_force'].midpoint)[1:]).max()), 'lapse_preservation_midpoint_error': float(abs(constraint_time).max()), 'minimum_F': float(spatial_f.min()), 'maximum_shift_rate': float(abs(shift_time).max()), 'maximum_lapse_rate': float(abs(lapse_time).max()), 'maximum_scalar_acceleration': float(abs(acceleration).max())}
