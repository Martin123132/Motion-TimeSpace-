import math

import numpy as numerical
from scipy.linalg import eigvalsh, solve

from annular_spatial_clock_energy_20260909 import profile


def symmetric(matrix):
    return (matrix + matrix.T) / 2


def scalar_maps(basis, points):
    count = basis.radii.size
    left = numerical.clip(numerical.searchsorted(basis.radii, points, side='right') - 1, 0, count - 2)
    fraction = (points - basis.radii[left]) / basis.spacing
    values = numerical.concatenate([numerical.eye(count), numerical.zeros((count, count))], axis=1)
    slopes = numerical.concatenate([basis.derivative, numerical.eye(count) / basis.spacing], axis=1)
    first, second = values[left], values[left + 1]
    tangent_first, tangent_second = slopes[left], slopes[left + 1]
    spacing = basis.spacing
    coefficients = numerical.stack([first, spacing * tangent_first, -3 * first + 3 * second - spacing * (2 * tangent_first + tangent_second), 2 * first - 2 * second + spacing * (tangent_first + tangent_second)])
    result = numerical.zeros_like(coefficients)
    for order in range(4):
        for degree in range(order, 4):
            result[order] += math.factorial(degree) / math.factorial(degree - order) * coefficients[degree] * fraction[:, None]**(degree - order) / spacing**order
    return result


def spatial_forms(system, packed, speed):
    basis = system.basis
    data = profile(system, packed, speed, basis.quadrature)
    maps = scalar_maps(basis, basis.quadrature)
    characteristic, first, second = data['c'][:3]
    inverse = numerical.stack([1 / characteristic, -first / characteristic**2, 2 * first**2 / characteristic**3 - second / characteristic**2])
    normalized = numerical.zeros_like(maps[:3])
    normalized_time = normalized.copy()
    for order in range(3):
        for split in range(order + 1):
            normalized[order] += math.comb(order, split) * inverse[split, :, None] * maps[order - split]
    for order in range(3):
        for split in range(order + 1):
            normalized_time[order] -= math.comb(order, split) * data['theta'][split, :, None] * normalized[order - split]
    weight = basis.quadrature_weights / characteristic
    stiffness, kinetic, stiffness_time, kinetic_time = [numerical.zeros((maps.shape[2], maps.shape[2]), dtype=numerical.result_type(packed)) for unused in range(4)]
    for order in range(3):
        derivative, velocity, velocity_time = maps[order + 1], normalized[order], normalized_time[order]
        stiffness += derivative.T @ (weight[:, None] * derivative)
        kinetic += velocity.T @ (weight[:, None] * velocity)
        stiffness_time -= derivative.T @ ((weight * data['theta'][0])[:, None] * derivative)
        kinetic_time += velocity_time.T @ (weight[:, None] * velocity) + velocity.T @ (weight[:, None] * velocity_time) - velocity.T @ ((weight * data['theta'][0])[:, None] * velocity)
    return {'S': stiffness, 'T': kinetic, 'S_dot': stiffness_time, 'T_dot': kinetic_time, 'scalar_maps': maps, 'normalized_maps': normalized, 'normalized_time_maps': normalized_time, 'weight': weight, 'theta': data['theta'][0]}


def paired_work(forms, matrices, configuration, velocity, acceleration, free):
    selection = numerical.ix_(free, free)
    endpoints = numerical.array([index for index in range(configuration.size) if index not in set(free)])
    mass = matrices['M'][selection]
    gradient = numerical.einsum('kij,j->ki', forms['scalar_maps'][1:4], configuration)
    gradient_rate = numerical.einsum('kij,j->ki', forms['scalar_maps'][1:4], velocity)
    normalized = numerical.einsum('kij,j->ki', forms['normalized_maps'], velocity)
    normalized_metric_rate = numerical.einsum('kij,j->ki', forms['normalized_time_maps'], velocity)
    kinetic_dual = numerical.einsum('kij,ki,i->j', forms['normalized_maps'], normalized, forms['weight'])
    test = solve(mass, kinetic_dual[free], assume_a='sym')
    euler = (matrices['M'] @ acceleration + matrices['M_dot'] @ velocity + matrices['K'] @ configuration)[free]
    principal = numerical.sum(forms['weight'] * gradient_rate * gradient) - test @ (matrices['K'] @ configuration)[free]
    clock = numerical.sum(forms['weight'] * (normalized * normalized_metric_rate - .5 * forms['theta'] * (gradient**2 + normalized**2))) - test @ (matrices['M_dot'] @ velocity)[free]
    endpoint = (kinetic_dual[endpoints] - matrices['M'][numerical.ix_(endpoints, free)] @ test) @ acceleration[endpoints]
    equation_error = test @ euler
    return {'principal_commutation_work': float(principal), 'clock_work': float(clock), 'prescribed_endpoint_acceleration_work': float(endpoint), 'weak_equation_error_work': float(equation_error), 'variational_rate': float(principal + clock + endpoint + equation_error), 'test': test, 'free_Euler': euler}


def graph_operators(mass, stiffness, mass_time, stiffness_time):
    operator = solve(mass, stiffness, assume_a='sym')
    inverse_operator = solve(stiffness, mass, assume_a='sym')
    mass_transport = solve(mass, mass_time, assume_a='sym')
    stiffness_transport = solve(mass, stiffness_time @ inverse_operator, assume_a='sym')
    configuration_transport = stiffness_transport - mass_transport
    velocity_transport = configuration_transport - operator @ mass_transport @ inverse_operator
    configuration_form = symmetric(stiffness @ configuration_transport) + .5 * stiffness_time
    velocity_form = symmetric(mass @ velocity_transport) + .5 * mass_time
    configuration_rate = float(eigvalsh(symmetric(configuration_form), stiffness)[-1])
    velocity_rate = float(eigvalsh(symmetric(velocity_form), mass)[-1])
    return {'L': operator, 'A': mass_transport, 'C': stiffness_transport, 'configuration_transport': configuration_transport, 'velocity_transport': velocity_transport, 'configuration_form': configuration_form, 'velocity_form': velocity_form, 'growth_rate': max(0., 2 * configuration_rate, 2 * velocity_rate), 'configuration_rate': configuration_rate, 'velocity_rate': velocity_rate}


def higher_energy(mass, stiffness, displacement, velocity, boundary_force):
    graph = solve(mass, stiffness @ displacement - boundary_force, assume_a='sym')
    graph_velocity = solve(mass, stiffness @ velocity, assume_a='sym')
    return .5 * (graph @ stiffness @ graph + graph_velocity @ mass @ graph_velocity), graph, graph_velocity


def higher_work(mass, stiffness, mass_time, stiffness_time, displacement, velocity, acceleration, boundary_force, boundary_force_time, residual_force):
    operators = graph_operators(mass, stiffness, mass_time, stiffness_time)
    energy, graph, graph_velocity = higher_energy(mass, stiffness, displacement, velocity, boundary_force)
    boundary = solve(mass, boundary_force, assume_a='sym')
    source_configuration = operators['C'] @ boundary - solve(mass, boundary_force_time, assume_a='sym')
    source_velocity = operators['L'] @ solve(mass, residual_force, assume_a='sym')
    graph_time = solve(mass, stiffness_time @ displacement + stiffness @ velocity - boundary_force_time - mass_time @ graph, assume_a='sym')
    graph_velocity_time = solve(mass, stiffness_time @ velocity + stiffness @ acceleration - mass_time @ graph_velocity, assume_a='sym')
    expected_graph_time = graph_velocity + operators['configuration_transport'] @ graph + source_configuration
    expected_velocity_time = -operators['L'] @ graph + operators['velocity_transport'] @ graph_velocity + source_velocity
    direct = graph @ stiffness @ graph_time + .5 * graph @ stiffness_time @ graph + graph_velocity @ mass @ graph_velocity_time + .5 * graph_velocity @ mass_time @ graph_velocity
    transport = graph @ operators['configuration_form'] @ graph + graph_velocity @ operators['velocity_form'] @ graph_velocity
    forcing = graph @ stiffness @ source_configuration + graph_velocity @ mass @ source_velocity
    source_squared = source_configuration @ stiffness @ source_configuration + source_velocity @ mass @ source_velocity
    source_norm = float(numerical.sqrt(max(float(source_squared), 0.)))
    return {'energy': float(energy), 'direct_rate': float(direct), 'transport_work': float(transport), 'source_work': float(forcing), 'source_norm': source_norm, 'growth_rate': operators['growth_rate'], 'rate_upper': float(operators['growth_rate'] * energy + numerical.sqrt(2 * energy) * source_norm), 'graph': graph, 'graph_velocity': graph_velocity, 'graph_time': graph_time, 'expected_graph_time': expected_graph_time, 'graph_velocity_time': graph_velocity_time, 'expected_velocity_time': expected_velocity_time, 'source_configuration': source_configuration, 'source_velocity': source_velocity, 'configuration_rate': operators['configuration_rate'], 'velocity_rate': operators['velocity_rate']}


def frozen_spatial_growth(stiffness_form, kinetic_form, mass, stiffness):
    operator = solve(mass, stiffness, assume_a='sym')
    defect = stiffness_form - kinetic_form @ operator
    lower_stiffness = numerical.linalg.cholesky(symmetric(stiffness_form))
    lower_kinetic = numerical.linalg.cholesky(symmetric(kinetic_form))
    whitened = numerical.linalg.solve(lower_kinetic, defect)
    whitened = numerical.linalg.solve(lower_stiffness, whitened.T).T
    left, singular, right = numerical.linalg.svd(whitened, full_matrices=False)
    configuration = numerical.linalg.solve(lower_stiffness.T, right[0])
    velocity = numerical.linalg.solve(lower_kinetic.T, left[:, 0])
    return {'max_logarithmic_energy_rate': float(singular[0]), 'configuration': configuration, 'velocity': velocity, 'defect': defect}
