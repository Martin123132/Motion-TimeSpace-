import numpy as numerical

from annular_adm_mixed_action_20260909 import coefficient_jets, linear_value_gradient, real_linear
from annular_boundary_ramp_bound_20260909 import affine_link_bound
from annular_constraint_routhian_20260909 import bulk_evaluator


def cell_index(knots, points):
    return numerical.clip(numerical.searchsorted(knots, points, side='right') - 1, 0, knots.size - 2)


def metric_cell_bounds(system, packed):
    basis = system.basis
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    cosmological, kappa = system.constants['Lambda'], system.kappa
    if kappa <= 0 or basis.radii[0] <= 0:
        raise ValueError('Positive coupling and annulus required.')
    bounds = {name: [] for name in ['F_lower', 'F_upper', 'lapse_lower', 'lapse_upper', 'A_radial_bound']}
    for cell, (left, right) in enumerate(zip(basis.faces[:-1], basis.faces[1:])):
        knots = numerical.concatenate([[left], basis.radii[(basis.radii > left) & (basis.radii < right)], [right]])
        local_lapse = real_linear(linear_value_gradient(basis.radii, knots)[0], lapse)
        lapse_low, lapse_high = numerical.min(local_lapse), numerical.max(local_lapse)
        mass_high = max(abs(mass[cell]), abs(mass[cell + 1]))
        mass_slope = abs((mass[cell + 1] - mass[cell]) / (right - left))
        lower = 1 - 2 * mass_high / left - abs(cosmological) * right**2 / 3
        upper = 1 + 2 * mass_high / left + abs(cosmological) * right**2 / 3
        if min(lower, lapse_low) <= 0:
            raise ValueError('Sufficient positive-chart condition failed.')
        lapse_slope = numerical.max(numerical.abs(numerical.diff(local_lapse) / numerical.diff(knots)))
        spatial_derivative = 2 * mass_slope / left + 2 * mass_high / left**2 + 2 * abs(cosmological) * right / 3
        radial_bound = (lapse_slope / numerical.sqrt(lower) + lapse_high * spatial_derivative / (2 * lower**1.5)) / kappa
        for name, value in [('F_lower', lower), ('F_upper', upper), ('lapse_lower', lapse_low), ('lapse_upper', lapse_high), ('A_radial_bound', radial_bound)]:
            bounds[name].append(value)
    return {name: numerical.asarray(value) for name, value in bounds.items()}


def mass_trace_bound(system, packed, tangent):
    basis, kappa = system.basis, system.kappa
    length = basis.radii[-1] - basis.radii[0]
    cells = metric_cell_bounds(system, packed)
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    mass_q, lapse_q = real_linear(basis.face_value, mass), real_linear(basis.node_value, lapse)
    spatial_f = 1 - 2 * mass_q / basis.quadrature - system.constants['Lambda'] * basis.quadrature**2 / 3
    density = 1 / (kappa * lapse_q * spatial_f**1.5)
    pairing = basis.face_value.T @ ((basis.quadrature_weights * density)[:, None] * basis.face_value)
    gamma_face = real_linear(basis.node_to_face, lapse)**2 * (1 - 2 * mass / basis.faces - system.constants['Lambda'] * basis.faces**2 / 3)
    gamma_q = real_linear(basis.face_value, gamma_face)
    weights = real_linear(basis.face_value.T, basis.quadrature_weights * density * gamma_q / length)
    mismatch = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
    physical_norm = numerical.max(numerical.abs(mismatch))
    coefficient = numerical.sum(weights)
    lower_f, upper_f = numerical.min(cells['F_lower']), numerical.max(cells['F_upper'])
    lower_lapse, upper_lapse = numerical.min(lapse), numerical.max(lapse)
    uniform_coefficient = upper_lapse**2 * upper_f / (kappa * lower_lapse * lower_f**1.5)
    pairing_lower = 1 / (kappa * upper_lapse * upper_f**1.5)
    pairing_upper = 1 / (kappa * lower_lapse * lower_f**1.5)
    unweighted = basis.face_value.T @ (basis.quadrature_weights[:, None] * basis.face_value)
    return {'pairing': pairing, 'unweighted_pairing': unweighted, 'pairing_density': density, 'trace_weights': weights, 'affine_shift_generator': -gamma_face / length, 'mass_rate_mismatch': mismatch, 'mass_rate_norm': numerical.asarray(physical_norm), 'signed_trace': numerical.asarray(numerical.dot(weights, mismatch)), 'coefficient_exact': numerical.asarray(coefficient), 'coefficient_uniform_bound': numerical.asarray(uniform_coefficient), 'trace_bound': numerical.asarray(coefficient * physical_norm), 'uniform_trace_bound': numerical.asarray(uniform_coefficient * physical_norm), 'pairing_lower_bound': numerical.asarray(pairing_lower), 'pairing_upper_bound': numerical.asarray(pairing_upper), 'F_lower': numerical.asarray(lower_f), 'lapse_lower': numerical.asarray(lower_lapse)}


def bulk_jet(system, packed, tangent, time=0):
    basis, constants = system.basis, system.constants
    changed = packed + time * tangent['packed_speed']
    scalar = system.scalar + time * packed[system.slices[2]]
    slope = system.slope + time * packed[system.slope_slice]
    scalar_q = real_linear(basis.scalar_value, scalar) + real_linear(basis.lift_value, slope / basis.spacing)
    gradient_q = real_linear(basis.scalar_gradient, scalar) + real_linear(basis.lift_gradient, slope / basis.spacing)
    mass_q = real_linear(basis.face_value, changed[system.slices[0]])
    mass_radial = real_linear(basis.face_gradient, changed[system.slices[0]])
    lapse_q = real_linear(basis.node_value, changed[system.slices[1]])
    velocity_q = real_linear(basis.scalar_value, changed[system.slices[2]]) + real_linear(basis.lift_value, changed[system.slope_slice] / basis.spacing)
    raw = bulk_evaluator()(mass_q, mass_radial, lapse_q, velocity_q, basis.quadrature, scalar_q, gradient_q, system.kappa, constants['b2'], constants['b3'], constants['m_chi'], constants['Lambda'])
    values = numerical.stack([numerical.broadcast_to(value, basis.quadrature.shape) for value in raw])
    spatial_f = 1 - 2 * mass_q / basis.quadrature - constants['Lambda'] * basis.quadrature**2 / 3
    kinetic = -velocity_q**2 / lapse_q**2 + spatial_f * gradient_q**2
    principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
    scalar_derivative = -basis.quadrature**2 * lapse_q / numerical.sqrt(spatial_f) * constants['m_chi']**2 * scalar_q
    gradient_derivative = -basis.quadrature**2 * lapse_q * numerical.sqrt(spatial_f) * principal * gradient_q
    mass_time = real_linear(basis.face_value, tangent['packed_speed'][system.slices[0]])
    shift_derivative = mass_time / (system.kappa * lapse_q * spatial_f**1.5) - basis.quadrature**2 * principal * velocity_q * gradient_q / (lapse_q * numerical.sqrt(spatial_f))
    return {'values': values, 'scalar_derivative': scalar_derivative, 'gradient_derivative': gradient_derivative, 'shift_derivative': shift_derivative, 'gamma': lapse_q**2 * spatial_f}


def affine_bulk_remainder_bound(system, packed, tangent, link_bound):
    basis = system.basis
    points, weights = basis.quadrature, basis.quadrature_weights
    length = basis.radii[-1] - basis.radii[0]
    face_cell, scalar_cell = cell_index(basis.faces, points), cell_index(basis.radii, points)
    face_left, face_right = basis.faces[face_cell], basis.faces[face_cell + 1]
    node_left, node_right = basis.radii[scalar_cell], basis.radii[scalar_cell + 1]
    mass_time = tangent['packed_speed'][system.slices[0]]
    mass_time_slope = numerical.diff(mass_time) / numerical.diff(basis.faces)
    lapse = packed[system.slices[1]]
    lapse_slope = numerical.diff(lapse) / numerical.diff(basis.radii)
    velocity = packed[system.slices[2]]
    velocity_radial = real_linear(basis.derivative, velocity) + packed[system.slope_slice] / basis.spacing
    width = numerical.diff(basis.radii)
    velocity_third = 12 * (velocity[:-1] - velocity[1:]) / width**3 + 6 * (velocity_radial[:-1] + velocity_radial[1:]) / width**2
    mass_error = mass_time_slope[face_cell] * (points - face_left) * (face_right - points) / length
    mass_radial_error = mass_time_slope[face_cell] * (face_left + face_right - 2 * points) / length
    lapse_error = lapse_slope[scalar_cell] * (points - node_left) * (node_right - points) / length
    scalar_error = -velocity_third[scalar_cell] * (points - node_left)**2 * (points - node_right)**2 / (6 * length)
    scalar_radial_error = -velocity_third[scalar_cell] * (points - node_left) * (points - node_right) * (2 * points - node_left - node_right) / (3 * length)
    jet = bulk_jet(system, packed, tangent)
    jet_time = bulk_jet(system, packed, tangent, 1j * 1e-25)['values'].imag / 1e-25
    gamma_face = -link_bound['affine_shift_generator'] * length
    shift_error = (jet['gamma'] - real_linear(basis.face_value, gamma_face)) / length
    kernels = {'mass_product': jet['values'][1] * mass_error, 'mass_radial_product': jet['values'][2] * mass_radial_error, 'lapse_commutator': -jet_time[3] * lapse_error, 'scalar_commutator': (jet['scalar_derivative'] - jet_time[4]) * scalar_error, 'scalar_radial_product': jet['gradient_derivative'] * scalar_radial_error, 'shift_product': jet['shift_derivative'] * shift_error}
    signed = {name: numerical.dot(weights, value) for name, value in kernels.items()}
    cells = metric_cell_bounds(system, packed)
    centers = (basis.faces[1:] + basis.faces[:-1]) / 2
    center_mass = real_linear(linear_value_gradient(basis.faces, centers)[0], packed[system.slices[0]])
    center_lapse = real_linear(linear_value_gradient(basis.radii, centers)[0], lapse)
    center_f = 1 - 2 * center_mass / centers - system.constants['Lambda'] * centers**2 / 3
    center_coefficient = center_lapse / (system.kappa * numerical.sqrt(center_f))
    mass_derivative_bound = numerical.dot(weights, cells['A_radial_bound'][face_cell] * numerical.abs(points - centers[face_cell]) * numerical.abs(mass_radial_error))
    bounds = {name: numerical.dot(weights, numerical.abs(value)) for name, value in kernels.items()}
    bounds['mass_radial_product'] = mass_derivative_bound
    bounds['shift_product'] = numerical.dot(weights, numerical.abs(jet['shift_derivative']) * link_bound['cell_gamma_interpolation_bound'][face_cell] / length)
    zero_moments = numerical.zeros(centers.size)
    numerical.add.at(zero_moments, face_cell, weights * mass_radial_error)
    centered_radial = numerical.dot(weights, (jet['values'][2] - center_coefficient[face_cell]) * mass_radial_error)
    return {'signed_' + name: numerical.asarray(value) for name, value in signed.items()} | {'bound_' + name: numerical.asarray(value) for name, value in bounds.items()} | {'bulk_remainder': numerical.asarray(sum(signed.values())), 'bulk_bound': numerical.asarray(sum(bounds.values())), 'mass_error': mass_error, 'mass_radial_error': mass_radial_error, 'lapse_error': lapse_error, 'scalar_error': scalar_error, 'scalar_radial_error': scalar_radial_error, 'shift_error': shift_error, 'mass_radial_zero_moments': zero_moments, 'centered_mass_radial_term': numerical.asarray(centered_radial), 'mass_radial_coefficient': jet['values'][2], 'mass_radial_center_coefficient': center_coefficient[face_cell], 'mass_radial_coefficient_difference_bound': cells['A_radial_bound'][face_cell] * numerical.abs(points - centers[face_cell]), 'velocity_third': velocity_third, 'mass_time_radial': mass_time_slope, 'lapse_radial': lapse_slope, 'lapse_force_time': jet_time[3], 'scalar_force_time': jet_time[4], 'scalar_Euler_density': jet['scalar_derivative'] - jet_time[4], 'scalar_radial_force': jet['gradient_derivative'], 'shift_force': jet['shift_derivative'], 'max_gamma_variation_over_cell_width': numerical.asarray(numerical.max(link_bound['cell_gamma_derivative_variation_bound'] / numerical.diff(basis.faces)))}


def affine_gram_coefficient_bound(system, packed, tangent, link_bound):
    basis = system.basis
    length = basis.radii[-1] - basis.radii[0]
    mass = real_linear(basis.face_to_node, packed[system.slices[0]])
    lapse, velocity = packed[system.slices[1]], packed[system.slices[2]]
    unused_coefficient, gradient, unused_hessian = coefficient_jets(velocity, system.gradient_node, mass, lapse, basis.radii, system.constants)
    cells = cell_index(basis.faces, basis.radii)
    left, right = basis.faces[cells], basis.faces[cells + 1]
    mass_time_slope = numerical.diff(tangent['packed_speed'][system.slices[0]]) / numerical.diff(basis.faces)
    mass_error = mass_time_slope[cells] * (basis.radii - left) * (right - basis.radii) / length
    gamma = lapse**2 * (1 - 2 * mass / basis.radii - system.constants['Lambda'] * basis.radii**2 / 3)
    shift_error = gamma / length + real_linear(basis.face_to_node, link_bound['affine_shift_generator'])
    actual = numerical.dot(system.density, gradient[2] * mass_error + gradient[4] * shift_error)
    bound = numerical.dot(numerical.abs(system.density), numerical.abs(gradient[2] * mass_error) + numerical.abs(gradient[4]) * link_bound['cell_gamma_interpolation_bound'][cells] / length)
    return {'coefficient_remainder': numerical.asarray(actual), 'coefficient_bound': numerical.asarray(bound)}
