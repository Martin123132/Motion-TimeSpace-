from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal
import numpy as np


ZERO = Decimal(0)
ONE = Decimal(1)


def field_radii(kernel, edges, count):
    positions = np.full(count, ZERO, dtype=object)
    for cell, indices in enumerate(kernel.elements):
        radii = [edges[cell], (edges[cell] + edges[cell + 1]) / 2, edges[cell + 1]]
        for column, radius in zip(indices, radii):
            if column >= 0:
                positions[column] = radius
    return positions


def profile(radius, power):
    if power == 0:
        return ONE if np.ndim(radius) == 0 else np.full(np.shape(radius), ONE, dtype=object)
    return (radius - Decimal(6))**power


def primitive(radius, source, power):
    return ((radius - Decimal(6))**(power + 1) - (source - Decimal(6))**(power + 1)) / (power + 1)


def leaf_shift(integral, amplitude, omega):
    if not omega:
        return amplitude * integral
    return np.array([((amplitude * omega * value).exp() - ONE) / omega for value in integral], dtype=object)


def finite_gram_action(kernel, edges, field, rate, beta, lapse_squared_metric, velocity, power, omega, amplitude):
    source = edges[kernel.anchor]
    native_radii = edges[kernel.native]
    nodal_radii = field_radii(kernel, edges, len(field))
    field_times = leaf_shift(primitive(nodal_radii, source, power), amplitude, omega)
    native_integrals = primitive(native_radii, source, power)
    native_times = leaf_shift(native_integrals, amplitude, omega)
    time_jacobian = np.array([(amplitude * omega * value).exp() for value in native_integrals], dtype=object)
    time_jacobian *= ONE - amplitude * profile(source, power) * velocity
    connection = amplitude * (ONE + omega * native_times) * profile(native_radii, power)
    shift = np.array([2 * connection_value * scale / (ONE + (ONE + 4 * connection_value**2 * scale).sqrt())
                      for connection_value, scale in zip(connection, lapse_squared_metric)], dtype=object)
    coefficient = beta * time_jacobian * (ONE - shift**2 / lapse_squared_metric)
    if min(coefficient) <= 0:
        raise ValueError('Finite horizontal coefficient must stay positive')
    return -kernel.evaluate(edges, field + rate * field_times, coefficient)['energy']


def endpoint_functional(kernel, edges, field, rate, beta, beta_radial, mesh_velocity, velocity, power, omega, time):
    moved_edges = edges + time * mesh_velocity
    moved_beta = beta + time * beta_radial * mesh_velocity[kernel.native]
    if min(np.diff(moved_edges)) <= 0 or min(moved_beta) <= 0:
        raise ValueError('Temporal jet left the physical chart')
    result = kernel.evaluate(moved_edges, field + time * rate, moved_beta)
    integrals = primitive(moved_edges[kernel.native], moved_edges[kernel.anchor], power)
    return -(ONE + omega * time) * sum(moved_beta * result['load'] * integrals, ZERO)


def current_terms(field_gradient, rate, nodal_integrals, energy, atom_rate, native_integrals, native_velocity, native_profile):
    field_terms = -field_gradient * rate * nodal_integrals
    bulk_terms = atom_rate * native_integrals
    local_terms = energy * native_velocity * native_profile
    return dict(field=sum(field_terms, ZERO), bulk=sum(bulk_terms, ZERO), local=sum(local_terms, ZERO),
                total=sum(field_terms, ZERO) + sum(bulk_terms, ZERO) + sum(local_terms, ZERO),
                absolute_scale=sum(abs(field_terms), ZERO) + sum(abs(bulk_terms), ZERO) + sum(abs(local_terms), ZERO))


def wave_mesh_momentum(kernel, edges, field, rate, edge_velocity, tests, solver, solution, order):
    abscissae, weights = np.polynomial.legendre.leggauss(order)
    local = np.array([Decimal.from_float(float((value + 1) / 2)) for value in abscissae], dtype=object)
    weights = np.array([Decimal.from_float(float(value / 2)) for value in weights], dtype=object)
    widths = np.diff(edges)
    radius = edges[:-1, None] + widths[:, None] * local
    metric_values = solver.values(solution, np.asarray(radius, float).ravel())[0]
    mass = metric_values[0].reshape(radius.shape)
    lapse = np.exp(metric_values[1].reshape(radius.shape))
    metric = 1 - 2 * mass / np.asarray(radius, float)
    alpha_float = np.asarray(radius, float)**2 / (lapse * np.sqrt(metric))
    beta_float = np.asarray(radius, float)**2 * lapse * np.sqrt(metric)
    alpha = np.array([Decimal.from_float(float(value)) for value in alpha_float.ravel()], dtype=object).reshape(radius.shape)
    beta = np.array([Decimal.from_float(float(value)) for value in beta_float.ravel()], dtype=object).reshape(radius.shape)
    basis = np.array([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)], dtype=object)
    derivative = np.array([-3 + 4 * local, 4 - 8 * local, -1 + 4 * local], dtype=object)
    values, speeds = [np.full(kernel.elements.shape, ZERO, dtype=object) for unused in range(2)]
    selected = kernel.elements >= 0
    values[selected], speeds[selected] = field[kernel.elements[selected]], rate[kernel.elements[selected]]
    gradient = (values @ derivative) / widths[:, None]
    nodal_rate = speeds @ basis
    mesh_rate = edge_velocity[:-1, None] * (1 - local) + edge_velocity[1:, None] * local
    temporal = nodal_rate - mesh_rate * gradient
    measure = widths[:, None] * weights
    momentum_density = -measure * alpha * temporal * gradient
    momentum = np.full(len(edges), ZERO, dtype=object)
    momentum[:-1] += np.sum(momentum_density * (1 - local), axis=1)
    momentum[1:] += np.sum(momentum_density * local, axis=1)
    rows = []
    for test, values in enumerate(tests):
        generator = values[:-1, None] * (1 - local) + values[1:, None] * local
        predicted = sum(momentum * values, ZERO)
        step = Decimal('0.0001')
        actions = []
        for sign in [1, -1]:
            changed = temporal - sign * step * generator * gradient
            actions.append(np.sum(measure * (alpha * changed**2 - beta * gradient**2)) / 2)
        measured = (actions[0] - actions[1]) / (2 * step)
        scale = np.sum(abs(momentum_density * generator))
        rows.append(dict(test=test, order=order, predicted=str(predicted), measured=str(measured),
                         error=str(abs(measured - predicted)), tolerance=str(Decimal('1e-22') + Decimal('2e-7') * scale)))
    return rows
