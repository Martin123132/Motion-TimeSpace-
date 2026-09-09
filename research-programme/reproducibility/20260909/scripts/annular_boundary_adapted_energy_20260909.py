import numpy as numerical

from annular_adm_mixed_action_20260909 import real_linear
from annular_action_boundary_current_20260909 import changed_system
from annular_first_derivative_energy_20260909 import affine_lift_matrix, canonical_matrices


def local_ode_acceleration(system, packed, tangent, endpoint_acceleration, clock_rate, include_gram, step):
    rates = []
    for sign in [-1, 1]:
        offset = sign * step
        changed = changed_system(system, packed, tangent, offset, clock_rate)
        moved = packed + offset * tangent['packed_speed']
        derived = changed.constraint_tangent(moved, include_gram, endpoint_acceleration, clock_rate)
        rates.append(derived['packed_speed'])
    return (rates[1] - rates[0]) / (2 * step)


def canonical_mass_second_rate(system, packed, speed, acceleration):
    basis = system.basis
    radius = basis.quadrature
    mass = real_linear(basis.face_value, packed[system.slices[0]])
    mass_time = real_linear(basis.face_value, speed[system.slices[0]])
    mass_second = real_linear(basis.face_value, acceleration[system.slices[0]])
    lapse = real_linear(basis.node_value, packed[system.slices[1]])
    lapse_time = real_linear(basis.node_value, speed[system.slices[1]])
    lapse_second = real_linear(basis.node_value, acceleration[system.slices[1]])
    spatial_f = 1 - 2 * mass / radius - system.constants['Lambda'] * radius**2 / 3
    density = radius**2 / (lapse * numerical.sqrt(spatial_f))
    ratio = -lapse_time / lapse + mass_time / (radius * spatial_f)
    ratio_time = -lapse_second / lapse + (lapse_time / lapse)**2 + mass_second / (radius * spatial_f) + 2 * (mass_time / (radius * spatial_f))**2
    reconstruction = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    return reconstruction.T @ ((basis.quadrature_weights * density * (ratio**2 + ratio_time))[:, None] * reconstruction)


def adapted_energy(mass, stiffness, displacement, velocity, boundary_force):
    graph = numerical.linalg.solve(mass, real_linear(stiffness, displacement) - boundary_force)
    energy = (numerical.dot(velocity, real_linear(stiffness, velocity)) + numerical.dot(graph, real_linear(mass, graph))) / 2
    return energy, graph


def adapted_diagnostic(system, packed, tangent, acceleration, base, include_gram):
    free = base['free']
    selection = numerical.ix_(free, free)
    matrices = canonical_matrices(system, packed, tangent['packed_speed'], include_gram)
    mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
    mass_second = canonical_mass_second_rate(system, packed, tangent['packed_speed'], acceleration)
    boundary_force = base['force_boundary_lift']
    boundary_rate = -(2 * real_linear(matrices['M_dot'], base['lift_acceleration']) + real_linear(mass_second, base['lift_velocity']) + real_linear(matrices['K_dot'], base['lift']) + real_linear(matrices['K'], base['lift_velocity']))[free]
    displacement, velocity = base['displacement'], base['velocity']
    energy, graph = adapted_energy(mass, stiffness, displacement, velocity, boundary_force)
    residual_force = base['force_nonlinear'] + base['force_scalar_equation_residual']
    force_velocity = numerical.linalg.solve(mass, residual_force)
    source = real_linear(stiffness_time, numerical.linalg.solve(stiffness, boundary_force)) - boundary_rate
    source_norm = numerical.sqrt(max(float(numerical.dot(source, numerical.linalg.solve(mass, source))), 0.))
    residual_norm = numerical.sqrt(max(float(numerical.dot(force_velocity, real_linear(stiffness, force_velocity))), 0.))
    transport = numerical.linalg.solve(mass, real_linear(mass_time, velocity))
    force_work = numerical.dot(force_velocity, real_linear(stiffness, velocity))
    work = {'residual_force_work': force_work, 'mass_transport_work': -numerical.dot(transport, real_linear(stiffness, velocity)), 'stiffness_time_displacement_work': numerical.dot(graph, real_linear(stiffness_time, displacement)), 'boundary_force_rate_work': -numerical.dot(graph, boundary_rate), 'mass_time_graph_work': -numerical.dot(graph, real_linear(mass_time, graph)) / 2, 'stiffness_time_velocity_work': numerical.dot(velocity, real_linear(stiffness_time, velocity)) / 2}
    predicted = sum(work.values())
    step = 1e-25
    moved = canonical_matrices(system, packed + 1j * step * tangent['packed_speed'], tangent['packed_speed'], include_gram)
    complex_energy = adapted_energy(moved['M'][selection], moved['K'][selection], displacement + 1j * step * velocity, velocity + 1j * step * base['velocity_time'], boundary_force + 1j * step * boundary_rate)[0]
    moved_rates = canonical_matrices(system, packed + 1j * step * tangent['packed_speed'], tangent['packed_speed'] + 1j * step * acceleration, include_gram)
    upper = float(base['energy_growth_rate']) * energy + numerical.sqrt(2 * energy) * (source_norm + residual_norm)
    radial_lower = numerical.min(matrices['radial_density'])
    return {'energy': numerical.asarray(energy), 'graph': graph, 'boundary_force': boundary_force, 'boundary_force_time': boundary_rate, 'M_second_rate': mass_second, 'M_second_rate_check_error': moved_rates['M_dot'].imag / step - mass_second, 'boundary_source': source, 'boundary_source_M_dual_norm': numerical.asarray(source_norm), 'residual_force_K_graph_norm': numerical.asarray(residual_norm), 'energy_time_predicted': numerical.asarray(predicted), 'energy_time_complex': numerical.asarray(complex_energy.imag / step), 'energy_growth_rate': base['energy_growth_rate'], 'energy_rate_upper_bound': numerical.asarray(upper), 'velocity_radial_norm_upper_bound': numerical.asarray(numerical.sqrt(2 * energy / radial_lower) + float(base['velocity_radial_norm_lift']))} | {'work_' + name: numerical.asarray(value) for name, value in work.items()}


def quadratic_path_energy(system, packed, tangent, acceleration, base, include_gram, offset):
    count = system.node_count
    configuration = numerical.concatenate([system.scalar, system.slope])
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    scalar_acceleration = numerical.concatenate([tangent['packed_speed'][system.slices[2]], tangent['packed_speed'][system.slope_slice]])
    moved_configuration = configuration + offset * velocity + offset**2 * scalar_acceleration / 2
    moved_packed = packed + offset * tangent['packed_speed'] + offset**2 * acceleration / 2
    moved_speed = tangent['packed_speed'] + offset * acceleration
    moved_velocity = numerical.concatenate([moved_packed[system.slices[2]], moved_packed[system.slope_slice]])
    lift_map = affine_lift_matrix(system.basis)
    lift = real_linear(lift_map, moved_configuration[[0, count - 1]])
    lift_velocity = real_linear(lift_map, moved_velocity[[0, count - 1]])
    lift_acceleration = base['lift_acceleration']
    matrices = canonical_matrices(system, moved_packed, moved_speed, include_gram)
    force = -(real_linear(matrices['M'], lift_acceleration) + real_linear(matrices['M_dot'], lift_velocity) + real_linear(matrices['K'], lift))[base['free']]
    selection = numerical.ix_(base['free'], base['free'])
    return adapted_energy(matrices['M'][selection], matrices['K'][selection], (moved_configuration - lift)[base['free']], (moved_velocity - lift_velocity)[base['free']], force)[0]
