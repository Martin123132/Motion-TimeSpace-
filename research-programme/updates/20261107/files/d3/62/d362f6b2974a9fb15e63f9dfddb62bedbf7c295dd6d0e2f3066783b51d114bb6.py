from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_native_time_current_20260928 import field_radii, primitive, profile, current_terms
from annular_physical_native_kernel_20260928 import decimals
from decimal import Decimal
from types import SimpleNamespace
import numpy as np
import sympy as sp


ZERO = Decimal(0)
CHANNELS = ['wave_velocity', 'gram_velocity', 'dust_velocity', 'total_velocity',
            'wave_acceleration', 'gram_field', 'gram_bulk', 'gram_local', 'minimal_wave_control']


def symbolic_checks(evidence):
    alpha, beta, temporal, gradient, beta_t, integral, test, speed, anchor, weighted, weighted_r, weighted_t = sp.symbols('alpha beta T g beta_t I h W h_bV a a_R adot')
    momentum_rate, energy_rate, speed_r = sp.symbols('Adot Edot W_R')
    energy = (alpha * temporal**2 + beta * gradient**2) / 2
    flux = alpha * speed * temporal + beta * gradient
    raw = alpha * temporal * weighted_t - flux * weighted_r - energy * (beta_t * integral / beta - anchor)
    endpoint = momentum_rate * weighted + alpha * temporal * weighted_t
    endpoint -= (energy_rate + speed_r * energy) * integral + energy * (speed * test - anchor)
    current = -momentum_rate * weighted - flux * weighted_r
    current += (energy_rate + speed_r * energy - beta_t * energy / beta) * integral + energy * speed * test
    evidence.check('wave_raw_endpoint_identity_with_source_clock', sp.expand(raw - endpoint - current) == 0)
    acceleration, support_acceleration = sp.symbols('chi zeta')
    coefficient = -alpha * (acceleration - support_acceleration * gradient) * weighted
    coefficient += alpha * temporal * (acceleration - support_acceleration * gradient) * integral
    evidence.check('wave_acceleration_block_derived', sp.factor(coefficient - alpha * (acceleration - support_acceleration * gradient) * (temporal * integral - weighted)) == 0)
    radius, lapse, metric, coupling, mass_rate = sp.symbols('R N F kappa mu_t', positive=True)
    radial_scale_rate = mass_rate / (radius * metric**sp.Rational(3, 2))
    gravity_shift = radius * radial_scale_rate / (coupling * lapse)
    evidence.check('ADM_connection_normalization', sp.simplify(gravity_shift * lapse**2 * metric - lapse * mass_rate / (coupling * sp.sqrt(metric))) == 0)
    gravity = sp.diag(2, 3, 5)
    mixed = sp.Matrix(sp.symbols('C0:3'))
    shift_rate = sp.Matrix(sp.symbols('vdot0:3'))
    metric_force = sp.Matrix(sp.symbols('Emu0:3'))
    support_force = sp.symbols('Es')
    evidence.check('gravity_support_mixed_block_keeps_null_direction', gravity.row_join(mixed) * (-gravity.inv() * mixed).col_join(sp.ones(1, 1)) == sp.zeros(3, 1))
    metric_euler = metric_force + gravity.T * shift_rate
    support_euler = support_force + (mixed.T * shift_rate)[0]
    eliminated = support_euler - (mixed.T * gravity.T.inv() * metric_euler)[0]
    evidence.check('derived_shift_reaction_compatibility', sp.expand(eliminated - support_force + (mixed.T * gravity.T.inv() * metric_force)[0]) == 0)


def integrals(radius, source, power):
    return ((radius - 6)**(power + 1) - (source - 6)**(power + 1)) / (power + 1)


def interpolate(packet, nodes):
    return interpolate_nodal(nodes, packet['indices'], packet['local'], packet['widths'])


def wave_current(packet, power):
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux = wave_terms(packet)
    integral = integrals(packet['radius'], packet['source'], power)
    test = (packet['radius'] - 6)**power
    weighted, weighted_r = interpolate(packet, packet['node_rate'] * integrals(packet['node_radius'], packet['source'], power))
    beta_t = -beta * packet['alpha_t'] / alpha
    density = -momentum_rate * weighted - flux * weighted_r
    density += (energy_dot + speed_r * energy - beta_t * energy / beta) * integral + energy * speed * test
    return packet['measure'] @ density


def wave_terms(packet):
    alpha, beta, gradient, speed, speed_r = [packet[key] for key in ['alpha', 'beta', 'gradient', 'speed', 'speed_r']]
    temporal = packet['rate'] - speed * gradient
    gradient_rate = packet['rate_r'] - speed_r * gradient
    temporal_rate = packet['acceleration'] - packet['speed_rate'] * gradient - speed * gradient_rate
    alpha_dot = packet['alpha_t'] + speed * packet['alpha_r']
    beta_dot = -beta * packet['alpha_t'] / alpha + speed * packet['beta_r']
    energy = (alpha * temporal**2 + beta * gradient**2) / 2
    energy_dot = (alpha_dot * temporal**2 + beta_dot * gradient**2) / 2 + alpha * temporal * temporal_rate + beta * gradient * gradient_rate
    momentum_rate = (alpha_dot + speed_r * alpha) * temporal + alpha * temporal_rate
    flux = alpha * speed * temporal + beta * gradient
    return alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux


def wave_blocks(packet, direction, power):
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux = wave_terms(packet)
    integral = integrals(packet['radius'], packet['source'], power)
    test = (packet['radius'] - 6)**power
    node_integral = integrals(packet['node_radius'], packet['source'], power)
    weighted, weighted_r = interpolate(packet, packet['node_rate'] * node_integral)
    delta_weighted, delta_weighted_r = interpolate(packet, direction['node_rate'] * node_integral)
    change = direction['rate'] - direction['speed'] * gradient
    delta_gradient_rate = direction['rate_r'] - direction['speed_r'] * gradient
    delta_temporal_rate = -direction['speed'] * gradient_rate - speed * delta_gradient_rate
    delta_momentum_rate = (direction['speed'] * packet['alpha_r'] + direction['speed_r'] * alpha) * temporal
    delta_momentum_rate += (alpha_dot + speed_r * alpha) * change + alpha * delta_temporal_rate
    delta_flux = alpha * (direction['speed'] * temporal + speed * change)
    delta_energy = alpha * temporal * change
    delta_energy_rate = direction['speed'] * (packet['alpha_r'] * temporal**2 + packet['beta_r'] * gradient**2) / 2
    delta_energy_rate += alpha_dot * temporal * change + alpha * change * temporal_rate + alpha * temporal * delta_temporal_rate
    delta_energy_rate += beta * gradient * delta_gradient_rate
    beta_log_rate = -packet['alpha_t'] / alpha
    delta_coefficient = delta_energy_rate + direction['speed_r'] * energy + (speed_r - beta_log_rate) * delta_energy
    density = -delta_momentum_rate * weighted - momentum_rate * delta_weighted - delta_flux * weighted_r - flux * delta_weighted_r
    density += delta_coefficient * integral + (delta_energy * speed + energy * direction['speed']) * test
    acceleration_density = alpha * change * (temporal * integral - weighted)
    minimal = -beta * gradient * change * test
    return np.array([packet['measure'] @ density, packet['measure'] @ acceleration_density, packet['measure'] @ minimal])


def perturb(packet, direction, amount, acceleration=False):
    moved = dict(packet)
    if acceleration:
        for target, source in [('acceleration', 'rate'), ('speed_rate', 'speed'), ('node_acceleration', 'node_rate'), ('node_speed_rate', 'node_speed')]:
            moved[target] = packet[target] + amount * direction[source]
        moved['acceleration_r'] = packet['acceleration_r'] + amount * direction['rate_r']
        moved['source_acceleration'] = packet['source_acceleration'] + amount * direction['source_velocity']
    else:
        for key in ['rate', 'rate_r', 'speed', 'speed_r', 'node_rate', 'node_speed', 'source_velocity']:
            moved[key] = packet[key] + amount * direction[key]
    return moved


def finite_wave_current(packet, power, step=1e-20):
    amount = 1j * step
    integral = integrals(packet['radius'], packet['source'], power)
    node_integral = integrals(packet['node_radius'], packet['source'], power)
    test = (packet['radius'] - 6)**power
    node_test = (packet['node_radius'] - 6)**power
    source_test = (packet['source'] - 6)**power
    time_jacobian = 1 - amount * source_test * packet['source_velocity']
    node_times = amount * node_integral
    field_change = packet['node_rate'] * node_times + packet['node_acceleration'] * node_times**2 / 2
    unused, gradient_change = interpolate(packet, field_change)
    moved_gradient = packet['gradient'] + gradient_change
    moved_rate_nodes = (packet['node_rate'] + packet['node_acceleration'] * node_times) * (time_jacobian + amount * node_test * packet['node_speed'])
    moved_rate = interpolate(packet, moved_rate_nodes)[0]
    connection = amount * test
    shift = 2 * connection * packet['shift_scale'] / (1 + np.sqrt(1 + 4 * connection**2 * packet['shift_scale']))
    beta_t = -packet['beta'] * packet['alpha_t'] / packet['alpha']
    moved_beta = (packet['beta'] + beta_t * amount * integral) * time_jacobian * (1 - shift**2 / packet['shift_scale'])
    moved_alpha = packet['alpha'] * packet['beta'] / moved_beta
    temporal = moved_rate - packet['speed'] * moved_gradient
    action = packet['measure'] @ ((moved_alpha * temporal**2 - moved_beta * moved_gradient**2) / 2)
    span = 1 + amount * packet['speed_r']
    moved_gradient = (packet['gradient'] + amount * packet['rate_r'] + amount**2 * packet['acceleration_r'] / 2) / span
    moved_alpha = packet['alpha'] + amount * (packet['alpha_t'] + packet['speed'] * packet['alpha_r'])
    moved_beta = packet['beta'] + amount * (beta_t + packet['speed'] * packet['beta_r'])
    temporal = packet['rate'] + amount * packet['acceleration'] - (packet['speed'] + amount * packet['speed_rate']) * moved_gradient
    moved_source = packet['source'] + amount * packet['source_velocity']
    moved_node_radius = packet['node_radius'] + amount * packet['node_speed']
    moved_radius = packet['radius'] + amount * packet['speed']
    weighted = interpolate(packet, (packet['node_rate'] + amount * packet['node_acceleration']) * integrals(moved_node_radius, moved_source, power))[0]
    energy = (moved_alpha * temporal**2 + moved_beta * moved_gradient**2) / 2
    endpoint = packet['measure'] @ (span * (moved_alpha * temporal * weighted - energy * integrals(moved_radius, moved_source, power)))
    return np.array([action.imag / step, endpoint.imag / step, (action.imag - endpoint.imag) / step])


def gram_block(engine, data, result, field_direction, edge_direction, power, change=None):
    node_radius = field_radii(SimpleNamespace(elements=engine.indices), data['edges'], engine.count)
    native_radius = data['edges'][engine.native_edges]
    if change is None:
        change = engine.tangent(data['edges'], data['field'], edge_direction, field_direction)
    dot_load = engine.apply('sampling', result['image'] * change, True)
    atoms = data['beta'] * dot_load + data['beta_radial'] * edge_direction[engine.native_edges] * result['load']
    return current_terms(result['field_gradient'], field_direction, primitive(node_radius, data['source'], power),
        data['beta'] * result['load'], atoms, primitive(native_radius, data['source'], power),
        edge_direction[engine.native_edges], profile(native_radius, power))


def make_packet(engine, data, raw, row, acceleration, direction_nodes, direction_edges, source_direction):
    packet = dict(raw)
    cells, local = row['quadrature']['cells'], row['quadrature']['local']
    indices = engine.indices[cells]
    widths = np.asarray(np.diff(data['edges']), float)[cells]
    node_radius = np.asarray(field_radii(SimpleNamespace(elements=engine.indices), data['edges'], engine.count), float)
    node_displacement = np.zeros(engine.count)
    for cell, columns in enumerate(engine.indices):
        for column, fraction in zip(columns, [data['displacement'][cell], (data['displacement'][cell] + data['displacement'][cell + 1]) / 2, data['displacement'][cell + 1]]):
            if column >= 0:
                node_displacement[column] = float(fraction)
    cardinal = data['cardinal']
    node_acceleration = cardinal @ acceleration[:, :-1]
    source_acceleration = float(cardinal @ acceleration[:, -1])
    packet.update(indices=indices, widths=widths, local=local, radius=row['geometry']['radius'],
        node_radius=node_radius, node_rate=np.asarray(data['rate'], float), node_acceleration=node_acceleration,
        node_speed=node_displacement * float(data['source_velocity']), node_speed_rate=node_displacement * source_acceleration,
        source=float(data['source']), source_velocity=float(data['source_velocity']), source_acceleration=source_acceleration,
        shift_scale=row['geometry']['lapse']**2 * row['geometry']['metric'])
    packet['acceleration_r'] = interpolate(packet, node_acceleration)[1]
    rate, rate_r = interpolate(packet, np.asarray(direction_nodes, float))
    edges = np.asarray(direction_edges, float)
    speed = edges[cells] * (1 - local) + edges[cells + 1] * local
    speed_r = (edges[cells + 1] - edges[cells]) / widths
    node_speed = np.zeros(engine.count)
    for cell, columns in enumerate(engine.indices):
        for column, value in zip(columns, [edges[cell], (edges[cell] + edges[cell + 1]) / 2, edges[cell + 1]]):
            if column >= 0:
                node_speed[column] = value
    direction = dict(node_rate=np.asarray(direction_nodes, float), node_speed=node_speed,
        rate=rate, rate_r=rate_r, speed=speed, speed_r=speed_r, source_velocity=float(source_direction))
    return packet, direction
