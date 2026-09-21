import numpy as numerical
from scipy.linalg import solve

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_parent_coefficient_box_20260910 import Box
from annular_parent_root_residence_20260910 import canonical_maps
from annular_joint_weak_action_20260910 import joint_prototype
from annular_gram_joint_action_20260909 import gram_matrices
from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature


def frozen_maps(system, packed, configuration):
    basis = system.basis
    data = joint_prototype(system, Box(packed), Box(configuration), False)
    mass_map = numerical.concatenate([basis.face_value, data['mass_lift'].midpoint], axis=1)
    mass_gradient = numerical.concatenate([basis.face_gradient, data['mass_lift_gradient'].midpoint], axis=1)
    shift_map = numerical.concatenate([basis.face_value, data['shift_test_remainder'].midpoint], axis=1)
    lapse = packed[system.slices[1]]
    endpoint, endpoint_gradient = linear_value_gradient(basis.radii, basis.radii[:1])
    endpoint_f = 1 - 2 * packed[0] / basis.radii[0]
    endpoint_zeta = endpoint_f * ((endpoint @ lapse)[:, None] * endpoint_gradient[:, 1:-1] - (endpoint_gradient @ lapse)[:, None] * endpoint[:, 1:-1])
    trace = numerical.concatenate([numerical.eye(system.face_count)[0], endpoint_zeta[0] - data['shift_projection_coefficients'].midpoint[0]])
    return {'mass_map': mass_map, 'mass_gradient': mass_gradient, 'shift_map': shift_map, 'trace': trace, 'projection': data['shift_projection_coefficients'].midpoint}


def slice_sources(system, packed, configuration, maps, shift_rate, order=8):
    basis, count = system.basis, system.node_count
    links = MetricLinkQuadrature(basis, order)
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    q_node = packed[system.slices[2]]
    factors, sampling = gram_matrices(count)
    coefficient = basis.radii**2 * lapse * numerical.sqrt(1 - 2 * (basis.face_to_node @ mass) / basis.radii)
    leading = factors @ configuration[:count]
    local_lapse = links.node_value @ lapse
    local_lapse_r = linear_value_gradient(basis.radii, links.points)[1] @ lapse
    local_f = 1 - 2 * (links.face_value @ mass) / links.points
    local_eta, local_eta_r = linear_value_gradient(basis.radii, links.points)
    zeta = local_f[:, None] * (local_lapse[:, None] * local_eta_r[:, 1:-1] - local_lapse_r[:, None] * local_eta[:, 1:-1])
    shift_map = numerical.concatenate([links.face_value, zeta - links.face_value @ maps['projection']], axis=1)
    beta_time = shift_map @ shift_rate
    generator = beta_time / (local_lapse**2 * local_f)
    endpoint_log = links.integrate(generator)
    partial_log = links.partial(generator)
    endpoint_jacobian, partial_jacobian = numerical.exp(endpoint_log), numerical.exp(partial_log)
    density = links.collect(links.sweight * coefficient[links.node] * endpoint_jacobian)
    leading_time = links.collect(links.tweight * q_node[links.node] * endpoint_jacobian)
    current = leading[links.factor] * (links.sweight * coefficient[links.node] * leading_time[links.factor] - links.tweight * q_node[links.node] * density[links.factor]) / basis.spacing
    kernel = links.integrate(shift_map / (local_lapse**2 * local_f * partial_jacobian**2)[:, None])
    weighted_current = current * endpoint_jacobian
    shift_force = kernel.T @ weighted_current
    scalar_force = numerical.zeros(2 * count)
    numerical.add.at(scalar_force, links.node, -links.tweight * leading[links.factor] * density[links.factor] / (basis.spacing * endpoint_jacobian))
    density_time = numerical.zeros(count)
    numerical.add.at(density_time, links.node, links.sweight * leading[links.factor] * leading_time[links.factor] / (basis.spacing * endpoint_jacobian))
    transport_weight = 2 * beta_time / local_lapse
    lapse_transport_kernel = links.integrate(local_eta * (transport_weight / (local_lapse**2 * local_f * partial_jacobian**2))[:, None])
    lapse_transport_time = -(lapse_transport_kernel.T @ weighted_current)
    raw_potential = numerical.sum(density * leading**2) / (2 * basis.spacing)
    anchor_cancellation = links.collect(weighted_current)
    return {'shift_force': shift_force, 'scalar_force': scalar_force, 'density_time': density_time, 'lapse_transport_time': lapse_transport_time, 'endpoint_jacobian': endpoint_jacobian, 'partial_jacobian': partial_jacobian, 'anchor_cancellation': anchor_cancellation, 'raw_potential': raw_potential, 'weighted_current': weighted_current, 'current': current, 'kernel': kernel, 'link_shift_map': shift_map, 'endpoint_log': endpoint_log, 'density': density, 'leading_time': leading_time, 'source_order': order}


def coupled_slice_jet(system, packed, configuration, endpoint_acceleration, maps, include_gram, boundary_rate=0., order=8):
    basis, count = system.basis, system.node_count
    radius, weights = basis.quadrature, basis.quadrature_weights
    value, gradient = canonical_maps(basis)
    mass_map, mass_gradient, shift_map = maps['mass_map'], maps['mass_gradient'], maps['shift_map']
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    mass_q, mass_r = basis.face_value @ mass, basis.face_gradient @ mass
    lapse_q = basis.node_value @ lapse
    q_coeff = packed[system.slices[2].start:]
    velocity, velocity_r, scalar_gradient = value @ q_coeff, gradient @ q_coeff, gradient @ configuration
    spatial_f = 1 - 2 * mass_q / radius
    kinetic = radius**2 / (lapse_q * numerical.sqrt(spatial_f))
    spatial = radius**2 * lapse_q * numerical.sqrt(spatial_f)
    rho = 1 / (.1 * lapse_q * spatial_f**1.5)
    flux = .1 * radius**2 * spatial_f * velocity * scalar_gradient
    pairing = shift_map.T @ ((weights * rho)[:, None] * mass_map)
    mass_density = lapse_q * mass_r / (.1 * radius * spatial_f**1.5) + radius * velocity**2 / (2 * lapse_q * spatial_f**1.5) + radius * lapse_q * scalar_gradient**2 / (2 * numerical.sqrt(spatial_f))
    mass_force = mass_map.T @ (weights * mass_density) + mass_gradient.T @ (weights * lapse_q / (.1 * numerical.sqrt(spatial_f)))
    mass_force[system.face_count - 1] -= system.outer_clock / .1
    factors, sampling = gram_matrices(count)
    gram_density = sampling.T @ (factors @ configuration[:count])**2 / (2 * basis.spacing)
    node_f = 1 - 2 * (basis.face_to_node @ mass) / basis.radii
    if include_gram:
        mass_force[:system.face_count] += basis.face_to_node.T @ (basis.radii * lapse * gram_density / numerical.sqrt(node_f))
    bordered = numerical.vstack([pairing[:, 1:].T, maps['trace']])
    shift_rate = solve(bordered, numerical.concatenate([mass_force[1:], [boundary_rate]]))
    sources = slice_sources(system, packed, configuration, maps, shift_rate, order)
    shift_load = shift_map.T @ (weights * rho * flux)
    if include_gram:
        shift_load -= sources['shift_force']
    mass_rate = solve(pairing, shift_load)
    mass_speed, mass_speed_r = mass_map @ mass_rate, mass_gradient @ mass_rate
    endpoints = numerical.array([0, count - 1])
    free = numerical.array([index for index in range(2 * count) if index not in endpoints])
    free_values, end_values, node_values = value[:, free], value[:, endpoints], basis.node_value
    scalar_matrix = free_values.T @ ((weights * kinetic)[:, None] * free_values)
    mixing = free_values.T @ ((weights * kinetic * velocity / lapse_q)[:, None] * node_values)
    projection = solve(scalar_matrix, mixing, assume_a='sym')
    projection_remainder = (velocity / lapse_q)[:, None] * node_values - free_values @ projection
    schur = projection_remainder.T @ ((weights * kinetic)[:, None] * projection_remainder)
    scalar_source = -(gradient[:, free].T @ (weights * spatial * scalar_gradient))
    if include_gram:
        scalar_source += sources['scalar_force'][free]
    scalar_source -= free_values.T @ (weights * kinetic * velocity * mass_speed / (radius * spatial_f))
    scalar_source -= (free_values.T @ ((weights * kinetic)[:, None] * end_values)) @ endpoint_acceleration
    scalar_source += free_values.T @ (weights * kinetic * scalar_gradient * (shift_map @ shift_rate))
    lapse_source_density = mass_speed_r / (.1 * numerical.sqrt(spatial_f))
    lapse_source_density += (mass_r / (.1 * radius * spatial_f**1.5) - radius * velocity**2 / (2 * lapse_q**2 * spatial_f**1.5) + radius * scalar_gradient**2 / (2 * numerical.sqrt(spatial_f))) * mass_speed
    lapse_source_density -= radius**2 * numerical.sqrt(spatial_f) * scalar_gradient * velocity_r
    lapse_source = -(node_values.T @ (weights * lapse_source_density))
    lapse_source += (node_values.T @ ((weights * kinetic * velocity / lapse_q)[:, None] * end_values)) @ endpoint_acceleration
    lapse_source += node_values.T @ (weights * rho * (mass_speed - flux) * (shift_map @ shift_rate) / lapse_q)
    gram_lapse_time = numerical.zeros(count)
    if include_gram:
        node_speed = basis.face_to_node @ mass_rate[:system.face_count]
        gram_lapse_time = -basis.radii**2 * numerical.sqrt(node_f) * sources['density_time'] + basis.radii * gram_density * node_speed / numerical.sqrt(node_f) + sources['lapse_transport_time']
        lapse_source -= gram_lapse_time
    particular = solve(scalar_matrix, scalar_source, assume_a='sym')
    lapse_rate = solve(schur, lapse_source + mixing.T @ particular, assume_a='sym')
    acceleration = numerical.zeros(2 * count)
    acceleration[endpoints] = endpoint_acceleration
    acceleration[free] = particular + projection @ lapse_rate
    lapse_matrix = node_values.T @ ((weights * kinetic * velocity**2 / lapse_q**2)[:, None] * node_values)
    residuals = {'mass': float(abs((mass_force - pairing.T @ shift_rate)[1:]).max()), 'shift': float(abs(pairing @ mass_rate - shift_load).max()), 'scalar': float(abs(scalar_matrix @ acceleration[free] - mixing @ lapse_rate - scalar_source).max()), 'lapse_preservation': float(abs(-mixing.T @ acceleration[free] + lapse_matrix @ lapse_rate - lapse_source).max()), 'boundary': float(abs(maps['trace'] @ shift_rate - boundary_rate))}
    return {'shift_rate': shift_rate, 'mass_rate': mass_rate, 'lapse_rate': lapse_rate, 'acceleration': acceleration, 'mass_speed': mass_speed, 'shift_speed': shift_map @ shift_rate, 'sources': sources, 'gram_lapse_time': gram_lapse_time, 'schur': schur, 'projection_remainder': projection_remainder, 'residuals': residuals, 'full_Gram_evolution_proved': False, 'numerical_scope': 'Midpoint evaluation of analytically derived continuous-time transport adjoints using radial Gauss/collocation quadratures. Not a certified discrete nonlinear time-link action or a residence proof.'}
