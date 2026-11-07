from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_support_shift_jet_20260928 import integrals, interpolate, wave_terms
from annular_old_field_reaction_20260929 import coefficient_data
from annular_native_position_precision_20260929 import Directional
from annular_physical_native_kernel_20260928 import decimals
from annular_native_time_current_20260928 import field_radii, primitive, profile
from decimal import Decimal
from types import SimpleNamespace
import numpy as np


def dust_rows(source, velocity, values, mass):
    lapse_squared = np.exp(2 * values[1])
    metric = 1 - 2 * values[0] / source
    current = mass * lapse_squared * velocity / np.sqrt(lapse_squared - velocity**2 / metric)
    return current * np.array([(source - 6)**power for power in range(3)])


def dust_position_column(source, velocity, values, mass, source_change, velocity_change, material_values):
    lapse_squared = np.exp(2 * values[1])
    metric = 1 - 2 * values[0] / source
    metric_change = -2 * material_values[0] / source + 2 * values[0] * source_change / source**2
    clock_squared = lapse_squared - velocity**2 / metric
    clock_squared_change = 2 * lapse_squared * material_values[1] - 2 * velocity * velocity_change / metric
    clock_squared_change += velocity**2 * metric_change / metric**2
    numerator = mass * lapse_squared * velocity
    numerator_change = mass * lapse_squared * (velocity_change + 2 * velocity * material_values[1])
    current = numerator / np.sqrt(clock_squared)
    current_change = numerator_change / np.sqrt(clock_squared) - numerator * clock_squared_change / (2 * clock_squared**1.5)
    return np.array([current_change * (source - 6)**power
        + (0 if power == 0 else current * power * (source - 6)**(power - 1) * source_change) for power in range(3)])


def gravity_position_rows(action, position, metric_time, mixed_time, order):
    from annular_registered_metric_coordinates_20260929 import metric_at_offset, response_at_offset
    anchor = float(action.owner.model.anchor)
    responses = [item for group in [position, metric_time, mixed_time]
        for item in getattr(group, 'responses', (group,))]
    lower, upper = action.solver.edges[[0, -1]] - anchor
    cuts = np.unique(np.concatenate([action.solver.edges - anchor] + [item.solver.edges - anchor for item in responses]))
    cuts = cuts[(cuts >= lower) & (cuts <= upper)]
    points, weights = np.polynomial.legendre.leggauss(order)
    widths = np.diff(cuts)
    offsets = (cuts[:-1, None] + widths[:, None] * (points + 1) / 2).ravel()
    measure = (widths[:, None] * weights / 2).ravel()
    radius = anchor + offsets
    values = metric_at_offset(action.solver, action.solution, offsets, anchor)[0]
    variation = response_at_offset(position, offsets, anchor)[0]
    time = response_at_offset(metric_time, offsets, anchor)[0][0]
    mixed = response_at_offset(mixed_time, offsets, anchor)[0][0]
    metric = 1 - 2 * values[0] / radius
    coefficient = np.exp(values[1]) / (action.owner.coupling * np.sqrt(metric))
    density = coefficient * (mixed + time * (variation[1] + variation[0] / (radius * metric)))
    amount = 1e-25j
    moved_coefficient = np.exp(values[1] + amount * variation[1])
    moved_coefficient /= action.owner.coupling * np.sqrt(1 - 2 * (values[0] + amount * variation[0]) / radius)
    oracle = (moved_coefficient * (time + amount * mixed)).imag / amount.imag
    return dict(base=np.array([measure @ (coefficient * time * (radius - 6)**power) for power in range(3)]),
        column=np.array([measure @ (density * (radius - 6)**power) for power in range(3)]),
        oracle=np.array([measure @ (oracle * (radius - 6)**power) for power in range(3)]))


def wave_densities(packet):
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux = wave_terms(packet)
    eta, eta_r, test, test_r = [packet[key] for key in ['eta', 'eta_r', 'field', 'field_r']]
    force = momentum_rate * (test - gradient * eta) + flux * test_r
    force -= alpha * temporal * gradient_rate * eta
    force -= (packet['alpha_r'] * temporal**2 - packet['beta_r'] * gradient**2) * eta / 2
    force -= (energy + alpha * speed * temporal * gradient) * eta_r
    result = [force]
    for power in range(3):
        integral = integrals(packet['radius'], packet['source'], power)
        weighted, weighted_r = interpolate(packet, packet['node_rate'] * integrals(packet['node_radius'], packet['source'], power))
        coefficient = energy_dot + (speed_r + packet['alpha_t'] / alpha) * energy
        result.append(-momentum_rate * weighted - flux * weighted_r + coefficient * integral
            + energy * speed * (packet['radius'] - 6)**power)
    return np.array(result)


def moved_packet(packet, direction, amount):
    span = 1 + amount * direction['movement_r']
    moved = dict(packet)
    moved['measure'] = packet['measure'] * span
    moved['widths'] = packet['widths'] * span
    for key, change in [('radius', 'movement'), ('source', 'source'), ('node_radius', 'node_movement'),
            ('rate', 'rate'), ('node_rate', 'node_rate'), ('acceleration', 'acceleration'),
            ('speed', 'speed'), ('speed_rate', 'speed_rate')]:
        moved[key] = packet[key] + amount * direction[change]
    for key in ['gradient', 'rate_r', 'speed_r']:
        moved[key] = (packet[key] + amount * direction[key]) / span
    for key in ['eta_r', 'field_r']:
        moved[key] = packet[key] / span
    radius = moved['radius']
    values = direction['values'] + amount * direction['material_values']
    radial = direction['radial'] + amount * direction['material_radial']
    time = direction['time'] + amount * direction['material_time']
    alpha, beta, alpha_r, beta_r = coefficient_data(radius, values, radial)
    metric = 1 - 2 * values[0] / radius
    moved.update(alpha=alpha, beta=beta, alpha_r=alpha_r, beta_r=beta_r,
        alpha_t=-alpha * (time[1] - time[0] / (radius * metric)))
    return moved


def coefficient_changes(packet, direction):
    radius, movement = packet['radius'], direction['movement']
    values, radial, time = [direction[key] for key in ['values', 'radial', 'time']]
    change, change_r, change_t = [direction[key] for key in ['material_values', 'material_radial', 'material_time']]
    metric = 1 - 2 * values[0] / radius
    metric_change = -2 * change[0] / radius + 2 * values[0] * movement / radius**2
    metric_r = -2 * radial[0] / radius + 2 * values[0] / radius**2
    metric_r_change = -2 * change_r[0] / radius + 2 * radial[0] * movement / radius**2
    metric_r_change += 2 * change[0] / radius**2 - 4 * values[0] * movement / radius**3
    alpha, beta = packet['alpha'], packet['beta']
    alpha_change = alpha * (2 * movement / radius - change[1] - metric_change / (2 * metric))
    beta_change = beta * (2 * movement / radius + change[1] + metric_change / (2 * metric))
    ratio_change = metric_r_change / metric - metric_r * metric_change / metric**2
    alpha_r_change = alpha_change * packet['alpha_r'] / alpha
    alpha_r_change += alpha * (-2 * movement / radius**2 - change_r[1] - ratio_change / 2)
    beta_r_change = beta_change * packet['beta_r'] / beta
    beta_r_change += beta * (-2 * movement / radius**2 + change_r[1] + ratio_change / 2)
    temporal_log = time[1] - time[0] / (radius * metric)
    temporal_log_change = change_t[1] - change_t[0] / (radius * metric)
    temporal_log_change += time[0] * (movement * metric + radius * metric_change) / (radius * metric)**2
    return dict(alpha=alpha_change, beta=beta_change, alpha_r=alpha_r_change, beta_r=beta_r_change,
        alpha_t=-alpha_change * temporal_log - alpha * temporal_log_change)


def analytic_volume_column(packet, direction):
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux = wave_terms(packet)
    delta = coefficient_changes(packet, direction)
    dilation = direction['movement_r']
    for key in ['gradient', 'rate_r', 'speed_r']:
        delta[key] = direction[key] - dilation * packet[key]
    for key in ['rate', 'speed', 'speed_rate', 'acceleration']:
        delta[key] = direction[key]
    temporal_change = delta['rate'] - delta['speed'] * gradient - speed * delta['gradient']
    gradient_rate_change = delta['rate_r'] - delta['speed_r'] * gradient - speed_r * delta['gradient']
    temporal_rate_change = delta['acceleration'] - delta['speed_rate'] * gradient
    temporal_rate_change -= packet['speed_rate'] * delta['gradient'] + delta['speed'] * gradient_rate + speed * gradient_rate_change
    alpha_dot_change = delta['alpha_t'] + delta['speed'] * packet['alpha_r'] + speed * delta['alpha_r']
    beta_dot_change = -delta['beta'] * packet['alpha_t'] / alpha - beta * delta['alpha_t'] / alpha
    beta_dot_change += beta * packet['alpha_t'] * delta['alpha'] / alpha**2
    beta_dot_change += delta['speed'] * packet['beta_r'] + speed * delta['beta_r']
    momentum_change = (alpha_dot_change + delta['speed_r'] * alpha + speed_r * delta['alpha']) * temporal
    momentum_change += (alpha_dot + speed_r * alpha) * temporal_change
    momentum_change += delta['alpha'] * temporal_rate + alpha * temporal_rate_change
    flux_change = (delta['alpha'] * speed + alpha * delta['speed']) * temporal + alpha * speed * temporal_change
    flux_change += delta['beta'] * gradient + beta * delta['gradient']
    energy_change = (delta['alpha'] * temporal**2 + delta['beta'] * gradient**2) / 2
    energy_change += alpha * temporal * temporal_change + beta * gradient * delta['gradient']
    energy_dot_change = (alpha_dot_change * temporal**2 + beta_dot_change * gradient**2) / 2
    energy_dot_change += alpha_dot * temporal * temporal_change + beta_dot * gradient * delta['gradient']
    energy_dot_change += delta['alpha'] * temporal * temporal_rate + alpha * temporal_change * temporal_rate + alpha * temporal * temporal_rate_change
    energy_dot_change += delta['beta'] * gradient * gradient_rate + beta * delta['gradient'] * gradient_rate + beta * gradient * gradient_rate_change
    eta, eta_r, test, test_r = [packet[key] for key in ['eta', 'eta_r', 'field', 'field_r']]
    force_change = momentum_change * (test - gradient * eta) - momentum_rate * delta['gradient'] * eta
    force_change += (flux_change - dilation * flux) * test_r
    force_change -= (delta['alpha'] * temporal * gradient_rate + alpha * temporal_change * gradient_rate + alpha * temporal * gradient_rate_change) * eta
    potential_change = delta['alpha_r'] * temporal**2 + 2 * packet['alpha_r'] * temporal * temporal_change
    potential_change -= delta['beta_r'] * gradient**2 + 2 * packet['beta_r'] * gradient * delta['gradient']
    force_change -= potential_change * eta / 2
    mixed_change = (delta['alpha'] * speed + alpha * delta['speed']) * temporal * gradient
    mixed_change += alpha * speed * (temporal_change * gradient + temporal * delta['gradient'])
    force_change -= (energy_change + mixed_change - dilation * (energy + alpha * speed * temporal * gradient)) * eta_r
    result = [force_change]
    for power in range(3):
        test = (packet['radius'] - 6)**power
        test_change = np.zeros_like(test) if power == 0 else power * (packet['radius'] - 6)**(power - 1) * direction['movement']
        integral = integrals(packet['radius'], packet['source'], power)
        integral_change = test * direction['movement'] - (packet['source'] - 6)**power * direction['source']
        node_integral = integrals(packet['node_radius'], packet['source'], power)
        node_integral_change = (packet['node_radius'] - 6)**power * direction['node_movement']
        node_integral_change -= (packet['source'] - 6)**power * direction['source']
        weighted, weighted_r = interpolate(packet, packet['node_rate'] * node_integral)
        weighted_change, weighted_r_change = interpolate(packet,
            direction['node_rate'] * node_integral + packet['node_rate'] * node_integral_change)
        weighted_r_change -= dilation * weighted_r
        logarithm = speed_r + packet['alpha_t'] / alpha
        logarithm_change = delta['speed_r'] + delta['alpha_t'] / alpha - packet['alpha_t'] * delta['alpha'] / alpha**2
        coefficient = energy_dot + logarithm * energy
        coefficient_change = energy_dot_change + logarithm_change * energy + logarithm * energy_change
        current = -momentum_change * weighted - momentum_rate * weighted_change
        current -= flux_change * weighted_r + flux * weighted_r_change
        current += coefficient_change * integral + coefficient * integral_change
        current += (energy_change * speed + energy * delta['speed']) * test + energy * speed * test_change
        result.append(current)
    return np.array(result) + dilation * wave_densities(packet)


def native_rows(engine, data, field_test, edge_test):
    result = engine.evaluate(data['edges'], data['field'], data['beta'])
    force = sum(result['field_gradient'] * field_test, Decimal(0))
    force += sum(result['edge_gradient'] * edge_test, Decimal(0))
    force += sum(result['load'] * data['beta_radial'] * edge_test[engine.native_edges], Decimal(0))
    velocity = data['displacement'] * data['source_velocity']
    change = engine.tangent(data['edges'], data['field'], velocity, data['rate'])
    dot_load = engine.apply('sampling', result['image'] * change, True)
    atom_rate = data['beta'] * dot_load + data['beta_radial'] * velocity[engine.native_edges] * result['load']
    node_radius = field_radii(SimpleNamespace(elements=engine.indices), data['edges'], engine.count)
    native_radius = data['edges'][engine.native_edges]
    rows = [force]
    for power in range(3):
        current = -sum(result['field_gradient'] * data['rate'] * primitive(node_radius, data['source'], power), Decimal(0))
        current += sum(atom_rate * primitive(native_radius, data['source'], power), Decimal(0))
        current += sum(data['beta'] * result['load'] * velocity[engine.native_edges] * profile(native_radius, power), Decimal(0))
        rows.append(current)
    return rows


def native_position_probe(precision, mode_rate, raw_directions, label, steps=(Decimal('1e-16'), Decimal('1e-18'))):
    data, field_change, edge_change, beta_change, beta_r_change = precision.packet(label, 'decimal_tangents')
    cardinal = data['cardinal']
    source_change = sum(cardinal * precision.decimal_source, Decimal(0))
    rate_change = cardinal @ decimals(mode_rate[:, :-1])
    source_rate_change = sum(cardinal * decimals(mode_rate[:, -1]), Decimal(0))
    field_test = cardinal @ decimals(raw_directions['field_vertices'])
    edge_test = cardinal @ decimals(raw_directions['edge_vertices'])
    changes = dict(edges=edge_change, field=field_change, beta=beta_change, beta_radial=beta_r_change,
        rate=rate_change, source=source_change, source_velocity=source_rate_change)
    lifted = dict(data)
    for name, tangent in changes.items():
        if np.ndim(tangent):
            lifted[name] = np.array([Directional(value, change) for value, change in zip(data[name], tangent)], dtype=object)
        else:
            lifted[name] = Directional(data[name], tangent)
    rows = native_rows(precision.native, lifted, field_test, edge_test)
    base = np.array([Directional.lift(value).value for value in rows], dtype=object)
    derivative = np.array([Directional.lift(value).tangent for value in rows], dtype=object)
    replay = np.asarray(native_rows(precision.native, data, field_test, edge_test), dtype=object)
    differences = []
    for step in steps:
        shifted = []
        for sign in [-1, 1]:
            family = dict(data)
            for name, tangent in changes.items():
                family[name] = data[name] + sign * step * tangent
            shifted.append(np.asarray(native_rows(precision.native, family, field_test, edge_test), dtype=object))
        estimate = (shifted[1] - shifted[0]) / (2 * step)
        differences.append(np.array(estimate - derivative, float))
    return dict(base=np.array(base, float), derivative=np.array(derivative, float),
        baseline_replay=np.array(base-replay, float), finite_differences=np.array(differences),
        steps=np.array(steps, float))
