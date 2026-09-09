import numpy as numerical
from scipy.linalg import eigvalsh

from annular_adm_mixed_action_20260909 import coefficient_jets, real_linear
from annular_action_boundary_current_20260909 import changed_system
from annular_gram_joint_action_20260909 import gram_matrices


def affine_lift_matrix(basis):
    fraction = (basis.radii - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])
    scalar = numerical.stack([1 - fraction, fraction], axis=1)
    gradient = numerical.broadcast_to(numerical.array([-1., 1.]) / (basis.radii[-1] - basis.radii[0]), scalar.shape)
    slope = basis.spacing * (gradient - real_linear(basis.derivative, scalar))
    return numerical.concatenate([scalar, slope], axis=0)


def canonical_matrices(system, packed, packed_speed, include_gram):
    basis = system.basis
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    mass, lapse = real_linear(basis.face_value, packed[system.slices[0]]), real_linear(basis.node_value, packed[system.slices[1]])
    mass_time = real_linear(basis.face_value, packed_speed[system.slices[0]])
    lapse_time = real_linear(basis.node_value, packed_speed[system.slices[1]])
    radius = basis.quadrature
    spatial_f = 1 - 2 * mass / radius - system.constants['Lambda'] * radius**2 / 3
    mass_density = radius**2 / (lapse * numerical.sqrt(spatial_f))
    radial_density = radius**2 * lapse * numerical.sqrt(spatial_f)
    potential_density = radius**2 * lapse / numerical.sqrt(spatial_f) * system.constants['m_chi']**2
    ratio_lapse, ratio_mass = lapse_time / lapse, mass_time / (radius * spatial_f)
    mass_matrix = value.T @ ((basis.quadrature_weights * mass_density)[:, None] * value)
    mass_rate = value.T @ ((basis.quadrature_weights * mass_density * (-ratio_lapse + ratio_mass))[:, None] * value)
    stiffness = radial.T @ ((basis.quadrature_weights * radial_density)[:, None] * radial)
    stiffness += value.T @ ((basis.quadrature_weights * potential_density)[:, None] * value)
    stiffness_rate = radial.T @ ((basis.quadrature_weights * radial_density * (ratio_lapse - ratio_mass))[:, None] * radial)
    stiffness_rate += value.T @ ((basis.quadrature_weights * potential_density * (ratio_lapse + ratio_mass))[:, None] * value)
    gram_stiffness, gram_rate = numerical.zeros_like(stiffness), numerical.zeros_like(stiffness_rate)
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        node_mass = real_linear(basis.face_to_node, packed[system.slices[0]])
        node_mass_time = real_linear(basis.face_to_node, packed_speed[system.slices[0]])
        node_lapse = packed[system.slices[1]]
        node_f = 1 - 2 * node_mass / basis.radii - system.constants['Lambda'] * basis.radii**2 / 3
        coefficient = basis.radii**2 * node_lapse * numerical.sqrt(node_f)
        coefficient_time = coefficient * (packed_speed[system.slices[1]] / node_lapse - node_mass_time / (basis.radii * node_f))
        gram_stiffness[:system.node_count, :system.node_count] = factors.T @ (real_linear(sampling, coefficient)[:, None] * factors) / basis.spacing
        gram_rate[:system.node_count, :system.node_count] = factors.T @ (real_linear(sampling, coefficient_time)[:, None] * factors) / basis.spacing
        stiffness += gram_stiffness
        stiffness_rate += gram_rate
    return {'M': mass_matrix, 'K': stiffness, 'M_dot': mass_rate, 'K_dot': stiffness_rate, 'K_Gram': gram_stiffness, 'K_Gram_dot': gram_rate, 'radial_density': radial_density}


def nonlinear_momentum_force(system, packed, include_gram):
    count = system.node_count
    dtype = numerical.result_type(packed, system.scalar)
    momentum, force = numerical.zeros(2 * count, dtype=dtype), numerical.zeros(2 * count, dtype=dtype)
    if system.constants['b2'] == 0 and system.constants['b3'] == 0:
        return momentum, force
    basis = system.basis
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    radius, lapse, velocity, spatial_f, scale, kinetic, unused_principal, unused_derivative = system.bulk_scalar_data(packed)
    correction = -4 * system.constants['b2'] * kinetic - 6 * system.constants['b3'] * kinetic**2
    momentum += real_linear(value.T, basis.quadrature_weights * radius**2 * scale * correction * velocity / lapse)
    force -= real_linear(radial.T, basis.quadrature_weights * radius**2 * lapse * numerical.sqrt(spatial_f) * correction * system.gradient_q)
    if include_gram:
        factors, sampling = gram_matrices(count)
        mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in system.node_maps]
        node_f = 1 - 2 * mass / basis.radii - system.constants['Lambda'] * basis.radii**2 / 3
        coefficient, gradient, unused_hessian = coefficient_jets(node_velocity, system.gradient_node, mass, node_lapse, basis.radii, system.constants)
        delta = coefficient - basis.radii**2 * node_lapse * numerical.sqrt(node_f)
        force[:count] -= real_linear(factors.T, real_linear(sampling, delta) * real_linear(factors, system.scalar)) / basis.spacing
        force[:count] -= real_linear(basis.derivative.T, system.density * gradient[1])
        force[count:] -= system.density * gradient[1] / basis.spacing
        momentum[:count] -= system.density * gradient[0]
    return momentum, force


def nonlinear_euler_force(system, packed, tangent, include_gram, clock_rate):
    momentum, force = nonlinear_momentum_force(system, packed, include_gram)
    step = 1e-25
    changed = changed_system(system, packed, tangent, 1j * step, clock_rate)
    momentum_time = nonlinear_momentum_force(changed, packed + 1j * step * tangent['packed_speed'], include_gram)[0].imag / step
    return {'momentum': momentum, 'force': force, 'momentum_time': momentum_time, 'Euler_force': force - momentum_time}


def graph_energy(mass, stiffness, displacement, velocity):
    graph = numerical.linalg.solve(mass, real_linear(stiffness, displacement))
    energy = (numerical.dot(velocity, real_linear(stiffness, velocity)) + numerical.dot(graph, real_linear(mass, graph))) / 2
    return energy, graph


def growth_rates(mass, stiffness, mass_time, stiffness_time):
    def norm(form, metric):
        return float(numerical.max(numerical.abs(eigvalsh((form + form.T) / 2, metric))))

    mass_transport = numerical.linalg.solve(mass, mass_time)
    stiffness_transport = stiffness_time @ numerical.linalg.solve(stiffness, mass)
    rates = {'alpha_M': norm(mass_time, mass), 'alpha_K': norm(stiffness_time, stiffness), 'alpha_A': norm(stiffness @ mass_transport, stiffness), 'alpha_L': norm(stiffness_transport, mass)}
    rates['energy_growth_rate'] = max(2 * rates['alpha_A'] + rates['alpha_K'], 2 * rates['alpha_L'] + rates['alpha_M'])
    return rates


def energy_work(mass, stiffness, mass_time, stiffness_time, displacement, velocity, graph, forcing):
    force_velocity = numerical.linalg.solve(mass, forcing)
    transport = numerical.linalg.solve(mass, real_linear(mass_time, velocity))
    force_work = numerical.dot(force_velocity, real_linear(stiffness, velocity))
    pieces = {'force_work': force_work, 'mass_transport_work': -numerical.dot(transport, real_linear(stiffness, velocity)), 'stiffness_time_displacement_work': numerical.dot(graph, real_linear(stiffness_time, displacement)), 'mass_time_graph_work': -numerical.dot(graph, real_linear(mass_time, graph)) / 2, 'stiffness_time_velocity_work': numerical.dot(velocity, real_linear(stiffness_time, velocity)) / 2}
    pieces['forcing_graph_norm'] = numerical.sqrt(max(float(numerical.dot(force_velocity, real_linear(stiffness, force_velocity))), 0.0))
    return pieces


def energy_diagnostic(system, packed, tangent, balance, include_gram, clock_rate):
    count = system.node_count
    free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
    selection = numerical.ix_(free, free)
    lift_map = affine_lift_matrix(system.basis)
    configuration = numerical.concatenate([system.scalar, system.slope])
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    acceleration = numerical.concatenate([tangent['packed_speed'][system.slices[2]], tangent['packed_speed'][system.slope_slice]])
    lift = real_linear(lift_map, system.scalar[[0, -1]])
    lift_velocity = real_linear(lift_map, packed[system.slices[2]][[0, -1]])
    lift_acceleration = real_linear(lift_map, tangent['packed_speed'][system.slices[2]][[0, -1]])
    displacement, speed = (configuration - lift)[free], (velocity - lift_velocity)[free]
    speed_time = (acceleration - lift_acceleration)[free]
    matrices = canonical_matrices(system, packed, tangent['packed_speed'], include_gram)
    mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
    correction = nonlinear_euler_force(system, packed, tangent, include_gram, clock_rate)
    lift_force = -(real_linear(matrices['M'], lift_acceleration) + real_linear(matrices['M_dot'], lift_velocity) + real_linear(matrices['K'], lift))[free]
    scalar_euler = numerical.concatenate([balance['scalar_Euler'], balance['slope_Euler']])
    forces = {'boundary_lift': lift_force, 'nonlinear': correction['Euler_force'][free], 'scalar_equation_residual': -scalar_euler[free]}
    forcing = sum(forces.values())
    equation_residual = real_linear(mass, speed_time) + real_linear(mass_time, speed) + real_linear(stiffness, displacement) - forcing
    energy, graph = graph_energy(mass, stiffness, displacement, speed)
    work = energy_work(mass, stiffness, mass_time, stiffness_time, displacement, speed, graph, forcing)
    forcing_work = {name: float(numerical.dot(numerical.linalg.solve(mass, force), real_linear(stiffness, speed))) for name, force in forces.items()}
    direct_time = (numerical.dot(speed_time, real_linear(stiffness, speed)) + numerical.dot(speed, real_linear(stiffness_time, speed)) / 2 + numerical.dot(graph, real_linear(stiffness_time, displacement) + real_linear(stiffness, speed)) - numerical.dot(graph, real_linear(mass_time, graph)) / 2)
    predicted_time = sum(value for name, value in work.items() if name != 'forcing_graph_norm')
    rates = growth_rates(mass, stiffness, mass_time, stiffness_time)
    upper = rates['energy_growth_rate'] * energy + numerical.sqrt(2 * energy) * work['forcing_graph_norm']
    step = 1e-25
    moved = canonical_matrices(system, packed + 1j * step * tangent['packed_speed'], tangent['packed_speed'], include_gram)
    complex_energy = graph_energy(moved['M'][selection], moved['K'][selection], displacement + 1j * step * speed, speed + 1j * step * speed_time)[0]
    mismatch_rate = numerical.zeros_like(tangent['packed_speed'])
    mismatch_rate[system.slices[0]] = tangent['packed_speed'][system.slices[0]] - tangent['shift_mass_speed']
    mismatch_matrices = canonical_matrices(system, packed, mismatch_rate, include_gram)
    mismatch_force = -real_linear(mismatch_matrices['M_dot'], lift_velocity)[free]
    mismatch_work = energy_work(mass, stiffness, mismatch_matrices['M_dot'][selection], mismatch_matrices['K_dot'][selection], displacement, speed, graph, mismatch_force)
    full_radial = numerical.concatenate([system.basis.scalar_gradient, system.basis.lift_gradient / system.basis.spacing], axis=1)
    free_radial = real_linear(full_radial[:, free], speed)
    lift_radial = real_linear(full_radial, lift_velocity)
    radial_lower = numerical.min(matrices['radial_density'])
    norm_speed = numerical.sqrt(numerical.dot(system.basis.quadrature_weights, free_radial**2))
    norm_lift = numerical.sqrt(numerical.dot(system.basis.quadrature_weights, lift_radial**2))
    return {'M': mass, 'K': stiffness, 'M_dot': mass_time, 'K_dot': stiffness_time, 'free': free, 'displacement': displacement, 'velocity': speed, 'velocity_time': speed_time, 'graph': graph, 'lift': lift, 'lift_velocity': lift_velocity, 'lift_acceleration': lift_acceleration, 'energy': numerical.asarray(energy), 'energy_time_direct': numerical.asarray(direct_time), 'energy_time_complex': numerical.asarray(complex_energy.imag / step), 'energy_time_predicted': numerical.asarray(predicted_time), 'energy_rate_upper_bound': numerical.asarray(upper), 'free_equation_residual': equation_residual, 'nonlinear_force': correction['Euler_force'], 'full_scalar_Euler': scalar_euler, 'nonlinear_momentum': correction['momentum'], 'full_M': matrices['M'], 'full_K': matrices['K'], 'matrix_M_rate_error': moved['M'].imag / step - matrices['M_dot'], 'matrix_K_rate_error': moved['K'].imag / step - matrices['K_dot'], 'velocity_radial_norm_free': numerical.asarray(norm_speed), 'velocity_radial_norm_lift': numerical.asarray(norm_lift), 'velocity_radial_norm_upper_bound': numerical.asarray(numerical.sqrt(2 * energy / radial_lower) + norm_lift), 'direct_mass_mismatch_energy_work': numerical.asarray(sum(value for name, value in mismatch_work.items() if name != 'forcing_graph_norm'))} | {'force_' + name: value for name, value in forces.items()} | {'work_' + name: numerical.asarray(value) for name, value in work.items()} | {'forcing_work_' + name: numerical.asarray(value) for name, value in forcing_work.items()} | {name: numerical.asarray(value) for name, value in rates.items()}
