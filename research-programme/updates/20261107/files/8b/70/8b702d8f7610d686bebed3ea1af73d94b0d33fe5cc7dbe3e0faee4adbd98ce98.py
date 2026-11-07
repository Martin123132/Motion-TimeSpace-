from functools import lru_cache

import numpy as numerical

from annular_adm_mixed_action_20260909 import coefficient_jets, linear_value_gradient, real_linear
from annular_gram_joint_action_20260909 import gram_matrices
from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian


def canonical_momenta(system, packed, include_gram):
    radius, lapse, velocity, unused_f, scale, unused_kinetic, principal, unused_derivative = system.bulk_scalar_data(packed)
    weighted = system.basis.quadrature_weights * radius**2 * scale * principal * velocity / lapse
    scalar_momentum = real_linear(system.basis.scalar_value.T, weighted)
    slope_momentum = real_linear((system.basis.lift_value / system.basis.spacing).T, weighted)
    if include_gram:
        mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in system.node_maps]
        unused_coefficient, gradient, unused_hessian = coefficient_jets(node_velocity, system.gradient_node, mass, node_lapse, system.basis.radii, system.constants)
        scalar_momentum -= system.density * gradient[0]
    return scalar_momentum, slope_momentum


def total_canonical_energy(system, packed, include_gram):
    momenta = canonical_momenta(system, packed, include_gram)
    scalar_rate, slope_rate = packed[system.slices[2]], packed[system.slope_slice]
    total_lagrangian = system.independent_action(packed, include_gram) + numerical.dot(system.momentum, scalar_rate) + numerical.dot(system.slope_momentum, slope_rate)
    return numerical.dot(momenta[0], scalar_rate) + numerical.dot(momenta[1], slope_rate) - total_lagrangian


def changed_system(system, packed, tangent, time, outer_clock_time):
    return ReleasedHermiteRouthian(system.basis, system.scalar + time * packed[system.slices[2]], system.slope + time * packed[system.slope_slice], system.constants, system.kappa, system.momentum + time * tangent['momentum_speed'], system.slope_momentum + time * tangent['slope_momentum_speed'], system.outer_clock + time * outer_clock_time, system.links)


@lru_cache(maxsize=8)
def cut_quadrature(basis, links):
    knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces, links.anchors]))
    gauss, weight = numerical.polynomial.legendre.leggauss(8)
    centers, halves = (knots[1:] + knots[:-1]) / 2, numerical.diff(knots) / 2
    points = (centers[:, None] + halves[:, None] * gauss).ravel()
    weights = (halves[:, None] * weight).ravel()
    lower, upper = numerical.minimum(links.anchors, links.targets), numerical.maximum(links.anchors, links.targets)
    crossing = ((points[:, None] > lower) & (points[:, None] < upper)) * numerical.sign(links.targets - links.anchors)
    face_value = linear_value_gradient(basis.faces, points)[0]
    node_value = linear_value_gradient(basis.radii, points)[0]
    return points, weights, crossing, face_value, node_value


def gram_current(system, packed, tangent):
    basis, links = system.basis, system.links
    factors, sampling = gram_matrices(system.node_count)
    mass, lapse, velocity = [real_linear(mapping, packed) for mapping in system.node_maps]
    mass_time = real_linear(basis.face_to_node, tangent['packed_speed'][system.slices[0]])
    lapse_time = tangent['packed_speed'][system.slices[1]]
    velocity_time = tangent['packed_speed'][system.slices[2]]
    gradient_time = real_linear(basis.derivative, velocity) + packed[system.slope_slice] / basis.spacing
    coefficient, gradient, hessian = coefficient_jets(velocity, system.gradient_node, mass, lapse, basis.radii, system.constants)
    leading, leading_time = real_linear(factors, system.scalar), real_linear(factors, velocity)
    sampled = real_linear(sampling, coefficient)
    density_time = real_linear(sampling.T, leading * leading_time) / basis.spacing
    primitive_time = numerical.stack([velocity_time, gradient_time, mass_time, lapse_time, numerical.zeros_like(lapse)])
    momentum_correction_time = density_time * gradient[0] + system.density * numerical.sum(hessian[0] * primitive_time, axis=0)
    scalar_gradient_force = real_linear(factors.T, sampled * leading) / basis.spacing
    coefficient_force = real_linear(basis.derivative.T, system.density * gradient[1])
    gram_euler = -scalar_gradient_force - coefficient_force + momentum_correction_time
    current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / basis.spacing
    current -= velocity[links.node] * links.tweight * sampled[links.factor] * leading[links.factor] / basis.spacing
    node_current = numerical.zeros(system.node_count)
    numerical.add.at(node_current, links.node, current)
    orientation = numerical.array([-1, 1])
    link_boundary = orientation * node_current[[0, -1]]
    correction_boundary = orientation * (-coefficient[[0, -1]] * density_time[[0, -1]] + velocity[[0, -1]] * (-coefficient_force[[0, -1]] + momentum_correction_time[[0, -1]]))
    reaction_boundary = orientation * velocity[[0, -1]] * gram_euler[[0, -1]]
    points, weights, crossing, face_value, node_value = cut_quadrature(basis, links)
    cut_current = real_linear(crossing, current)
    mass_q = real_linear(face_value, packed[system.slices[0]])
    lapse_q = real_linear(node_value, packed[system.slices[1]])
    spatial_f = 1 - 2 * mass_q / points - system.constants['Lambda'] * points**2 / 3
    cut_shift_covector = -real_linear(face_value.T, weights * cut_current / (lapse_q**2 * spatial_f))
    endpoint_shift_covector = -real_linear(links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants).T, current)
    return {'pair_current': current, 'factor_current_sum': links.collect(current), 'node_current': node_current, 'Gram_scalar_Euler': gram_euler, 'Gram_boundary_reaction_flux': reaction_boundary, 'Gram_boundary_link_flux': link_boundary, 'Gram_boundary_coefficient_flux': correction_boundary, 'cut_points': points, 'cut_current': cut_current, 'cut_shift_covector': cut_shift_covector, 'endpoint_shift_covector': endpoint_shift_covector, 'Gram_scalar_coefficient_force': coefficient_force, 'Gram_scalar_momentum_correction_time': momentum_correction_time, 'endpoint_sampling_weights': sampling[:, [0, -1]]}


def linear_time_boundary(system, packed, tangent, probe, time=0):
    basis, links = system.basis, system.links
    evolved = changed_system(system, packed, tangent, time, 0)
    changed = packed + time * tangent['packed_speed']
    mass, lapse, velocity = [real_linear(mapping, changed) for mapping in evolved.node_maps]
    coefficient = coefficient_jets(velocity, evolved.gradient_node, mass, lapse, basis.radii, system.constants)[0]
    leading = links.collect(links.tweight * evolved.scalar[links.node])
    displacement = real_linear(links.matrix(changed[system.slices[0]], changed[system.slices[1]], system.constants), probe)
    return numerical.dot(leading**2 / (2 * basis.spacing), links.collect(links.sweight * coefficient[links.node] * displacement))


def boundary_balance(system, packed, tangent, include_gram, outer_clock_time):
    basis, kappa = system.basis, system.kappa
    value, gradient, hessian = system.evaluate(packed, include_gram)
    gradient_time = real_linear(hessian, tangent['packed_speed']) + tangent['data_derivative']
    velocity, slope_velocity = packed[system.slices[2]], packed[system.slope_slice]
    mass_velocity = tangent['packed_speed'][system.slices[0]]
    lapse, lapse_velocity = packed[system.slices[1]], tangent['packed_speed'][system.slices[1]]
    step = 1e-25
    evolved = changed_system(system, packed, tangent, 1j * step, outer_clock_time)
    changed = packed + 1j * step * tangent['packed_speed']
    momentum_time, slope_momentum_time = [momentum.imag / step for momentum in canonical_momenta(evolved, changed, include_gram)]
    scalar_euler = system.scalar_force(packed, include_gram) - momentum_time
    slope_euler = system.slope_force(packed, include_gram) - slope_momentum_time
    orientation = numerical.array([-1, 1])
    flux = orientation * velocity[[0, -1]] * scalar_euler[[0, -1]]
    clocks = numerical.array([-kappa * gradient[system.slices[0]][0], system.outer_clock])
    local_balance = clocks * mass_velocity[[0, -1]] / kappa + flux
    remainder = -numerical.dot(velocity[1:-1], scalar_euler[1:-1]) - numerical.dot(slope_velocity, slope_euler)
    remainder -= numerical.dot(mass_velocity[1:], gradient[system.slices[0]][1:])
    remainder += numerical.dot(lapse, gradient_time[system.slices[1]])
    energy = total_canonical_energy(system, packed, include_gram)
    energy_time = total_canonical_energy(evolved, changed, include_gram).imag / step
    explicit_clock_work = outer_clock_time * packed[system.slices[0]][-1] / kappa
    euler_work = numerical.dot(velocity, scalar_euler) + numerical.dot(slope_velocity, slope_euler)
    euler_work += numerical.dot(mass_velocity, gradient[system.slices[0]]) + numerical.dot(lapse_velocity, gradient[system.slices[1]])
    boundary_energy = system.outer_clock * packed[system.slices[0]][-1] / kappa - numerical.dot(lapse, gradient[system.slices[1]])
    node_mass = real_linear(basis.face_to_node, packed[system.slices[0]])
    spatial_f = 1 - 2 * node_mass / basis.radii - system.constants['Lambda'] * basis.radii**2 / 3
    kinetic = -velocity**2 / lapse**2 + spatial_f * system.gradient_node**2
    principal = 1 - 4 * system.constants['b2'] * kinetic - 6 * system.constants['b3'] * kinetic**2
    continuum_flux = -basis.radii**2 * lapse * numerical.sqrt(spatial_f) * principal * velocity * system.gradient_node
    physical_clock = lapse / numerical.sqrt(spatial_f)
    continuum_mass_rate = kappa * basis.radii**2 * spatial_f * principal * velocity * system.gradient_node
    return {'scalar_Euler': scalar_euler, 'slope_Euler': slope_euler, 'reaction_flux_positive_R': flux, 'variational_boundary_clocks': clocks, 'physical_boundary_clocks': physical_clock[[0, -1]], 'local_boundary_balance': local_balance, 'global_boundary_remainder': numerical.asarray(remainder), 'global_boundary_identity_error': numerical.asarray(local_balance[-1] - local_balance[0] - remainder), 'canonical_energy': numerical.asarray(energy), 'homogeneous_boundary_energy': numerical.asarray(boundary_energy), 'energy_homogeneity_error': numerical.asarray(energy - boundary_energy), 'canonical_energy_time': numerical.asarray(energy_time), 'explicit_clock_work': numerical.asarray(explicit_clock_work), 'full_energy_work_identity_error': numerical.asarray(energy_time + euler_work - explicit_clock_work), 'continuum_GR_flux_positive_R': continuum_flux[[0, -1]], 'continuum_GR_mass_rate': continuum_mass_rate[[0, -1]], 'continuum_GR_normalization_error': physical_clock[[0, -1]] * continuum_mass_rate[[0, -1]] / kappa + continuum_flux[[0, -1]], 'free_constraint': gradient[system.free], 'free_constraint_rate': gradient_time[system.free]}
