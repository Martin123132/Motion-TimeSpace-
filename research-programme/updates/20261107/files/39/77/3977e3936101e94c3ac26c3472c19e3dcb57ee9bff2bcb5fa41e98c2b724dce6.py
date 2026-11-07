from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_old_field_reaction_20260929 import coefficient_data, dust_covectors, wave_packet
from annular_position_time_loads_20260929 import MixedJet
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_physical_native_kernel_20260928 import decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal
from time import perf_counter
import numpy as np


class ResponseSum:
    def __init__(self, *responses):
        self.responses = responses

    def at(self, radius):
        pairs = [response.solver.values(response.solution, radius) for response in self.responses]
        return tuple(sum(pair[index] for pair in pairs) for index in range(2))

    def values(self, radius):
        return self.at(radius)[0]


def second_radial(solver, solution, radius):
    indices = np.clip(np.searchsorted(solver.edges, np.asarray(radius).real, side='right') - 1,
        0, len(solver.lengths) - 1)
    coordinate = 2 * (radius - solver.centers[indices]) / solver.lengths[indices]
    return np.array([np.polynomial.chebyshev.chebval(coordinate,
        np.polynomial.chebyshev.chebder(values[indices].T, axis=0), tensor=False)
        * 2 / solver.lengths[indices] for values in solution['rhs_coefficients']])


def jet_exp(jet):
    base, position, time, mixed = jet.parts
    value = np.exp(base)
    return MixedJet(value, value * position, value * time, value * (mixed + position * time))


def metric_jets(values, radial, second, position, position_r, time, time_r, mixed,
                movement, speed, movement_rate):
    return [MixedJet(values[index], position[index] + radial[index] * movement,
        time[index] + radial[index] * speed,
        mixed[index] + position_r[index] * speed + time_r[index] * movement
        + second[index] * movement * speed + radial[index] * movement_rate) for index in range(2)]


def native_position_force(native, loads, action, label, field_direction, source_direction,
                          edge_vertices, position, step=Decimal('1e-12')):
    zero = np.zeros(loads.rates.shape[1])
    if not native.enabled:
        return zero, zero, zero
    data = physical_data(native, loads, action, label)
    cardinal = data['cardinal']
    field_change = decimals(cardinal @ field_direction)
    edge_change = decimals(cardinal @ edge_vertices) + data['displacement'] * Decimal.from_float(float(cardinal @ source_direction))
    radius = np.asarray(data['edges'][native.native_edges], float)
    movement = np.asarray(edge_change[native.native_edges], float)
    values, radial = action.solver.values(action.solution, radius)
    second = second_radial(action.solver, action.solution, radius)
    variation, variation_r = position.at(radius)
    amount = 1e-25j
    unused, beta, unused2, beta_r = coefficient_data(radius + amount * movement,
        values + amount * (variation + radial * movement),
        radial + amount * (variation_r + second * movement))
    beta_change, beta_r_change = decimals(beta.imag / 1e-25), decimals(beta_r.imag / 1e-25)

    def force(amount):
        result = native.evaluate(data['edges'] + amount * edge_change,
            data['field'] + amount * field_change, data['beta'] + amount * beta_change)
        source = -sum(result['edge_gradient'] * data['displacement'], Decimal(0))
        source -= sum(result['load'] * (data['beta_radial'] + amount * beta_r_change)
            * data['displacement'][native.native_edges], Decimal(0))
        return np.r_[-result['field_gradient'], source]

    first = (force(step) - force(-step)) / (2 * step)
    half = step / 2
    refined = (force(half) - force(-half)) / (2 * half)
    return np.asarray(first, float), np.asarray(refined - first, float), np.asarray(force(Decimal(0)), float)


def material_position_reaction(loads, action, native, directions, correction, mode_rate, acceleration,
                               position, metric_time, mixed_time, order, deadline, progress,
                               acceleration_change=None, reference_order=12, include_native=True):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    names = ['momentum_rate', 'oracle_momentum_rate', 'force_wave', 'force_native',
        'native_halving_difference', 'base_momentum', 'base_force_wave', 'base_force_native']
    output = {name: np.zeros_like(loads.rates) for name in names}
    amount, step = 1e-25j, 1e-25
    field_direction = directions['field_vertices'] - correction[:, :-1]
    source_direction = -correction[:, -1]
    acceleration_change = np.zeros_like(acceleration) if acceleration_change is None else acceleration_change
    reference_edges = np.asarray([float(value) for value in action.edges])
    for index, (label, weight) in enumerate(zip(labels, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Safe position reaction material boundary')
        row = samples(action, label, reference_order)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        radius, jacobian = geometry['radius'], geometry['jacobian']
        indices = np.asarray(action.mesh['elements'])[quad['cells']]
        selected = indices >= 0
        widths = np.diff(reference_edges)[quad['cells']] * jacobian
        interpolate = lambda array: interpolate_nodal(cardinal @ array, indices, quad['local'], widths)
        unused, field_r = interpolate(field_direction)
        transported, transported_r = interpolate(mode_rate[:, :-1])
        old_accel = interpolate(acceleration[:, :-1])[0]
        changed_accel = interpolate(acceleration_change[:, :-1])[0]
        source_mode = float(cardinal @ source_direction)
        source_rate = float(cardinal @ mode_rate[:, -1])
        source_accel = float(cardinal @ acceleration[:, -1])
        source_accel_change = float(cardinal @ acceleration_change[:, -1])
        edge = cardinal @ directions['edge_vertices']
        cells, local = quad['cells'], quad['local']
        eta = (1 - local) * edge[cells] + local * edge[cells + 1]
        eta_r = (edge[cells + 1] - edge[cells]) / widths
        displacement = geometry['displacement']
        displacement_r = geometry['jacobian_source'] / jacobian
        movement = eta + displacement * source_mode
        movement_r = eta_r + displacement_r * source_mode
        speed = displacement * row['velocity']
        speed_r = displacement_r * row['velocity']
        movement_rate = displacement * source_rate
        movement_rate_r = displacement_r * source_rate
        values, radial = action.solver.values(action.solution, radius)
        second = second_radial(action.solver, action.solution, radius)
        pos, pos_r = position.at(radius)
        time, time_r = metric_time.at(radius)
        mixed = mixed_time.values(radius)
        changed_jacobian = jacobian * (1 + amount * movement_r)
        changed_geometry = dict(geometry, radius=radius + amount * movement, jacobian=changed_jacobian)
        changed_row = dict(row, geometry=changed_geometry, gradient=row['gradient'] + amount * field_r * jacobian)
        base = wave_packet(row, values, radial, time, row['rate'], row['rate_gradient'] / jacobian,
            old_accel, speed, speed_r, displacement * source_accel)
        changed = wave_packet(changed_row, values + amount * (pos + radial * movement),
            radial + amount * (pos_r + second * movement), time + amount * (mixed + time_r * movement),
            row['rate'] + amount * transported,
            (row['rate_gradient'] + amount * transported_r * jacobian) / changed_jacobian,
            old_accel + amount * changed_accel, speed + amount * movement_rate,
            (speed_r + amount * movement_rate_r) / (1 + amount * movement_r),
            displacement * (source_accel + amount * source_accel_change))
        radius_jet = MixedJet(radius, movement, speed, movement_rate)
        jacobian_jet = MixedJet(jacobian, movement_r * jacobian, speed_r * jacobian, movement_rate_r * jacobian)
        gradient_jet = MixedJet(row['gradient'], field_r * jacobian, row['rate_gradient'], transported_r * jacobian) / jacobian_jet
        speed_jet = MixedJet(speed, movement_rate, displacement * source_accel, displacement * source_accel_change)
        rate_jet = MixedJet(row['rate'], transported, old_accel, changed_accel)
        mass_jet, nu_jet = metric_jets(values, radial, second, pos, pos_r, time, time_r, mixed, movement, speed, movement_rate)
        metric_jet = 1. - 2 * mass_jet / radius_jet
        alpha_jet = radius_jet**2 / (jet_exp(nu_jet) * metric_jet**.5)
        momentum_jet = jacobian_jet * alpha_jet * (rate_jet - speed_jet * gradient_jet)
        source_jet = -displacement * gradient_jet * momentum_jet
        source_radius = np.array([row['source']])
        source_values, source_radial = action.solver.values(action.solution, source_radius)
        source_second = second_radial(action.solver, action.solution, source_radius)
        source_pos, source_pos_r = position.at(source_radius)
        source_time, source_time_r = metric_time.at(source_radius)
        source_mixed = mixed_time.values(source_radius)
        dust_base = dust_covectors(row['source'], row['velocity'], source_values[:, 0], source_radial[:, 0],
            action.owner.source_mass, source_accel, source_time[:, 0])
        dust_changed = dust_covectors(row['source'] + amount * source_mode, row['velocity'] + amount * source_rate,
            (source_values + amount * (source_pos + source_radial * source_mode))[:, 0],
            (source_radial + amount * (source_pos_r + source_second * source_mode))[:, 0],
            action.owner.source_mass, source_accel + amount * source_accel_change,
            (source_time + amount * (source_mixed + source_time_r * source_mode))[:, 0])
        dust_radius_jet = MixedJet(row['source'], source_mode, row['velocity'], source_rate)
        dust_velocity_jet = MixedJet(row['velocity'], source_rate, source_accel, source_accel_change)
        dust_mass_jet, dust_nu_jet = metric_jets(source_values[:, 0], source_radial[:, 0], source_second[:, 0],
            source_pos[:, 0], source_pos_r[:, 0], source_time[:, 0], source_time_r[:, 0], source_mixed[:, 0],
            source_mode, row['velocity'], source_rate)
        dust_metric_jet = 1. - 2 * dust_mass_jet / dust_radius_jet
        dust_clock_jet = (jet_exp(2 * dust_nu_jet) - dust_velocity_jet**2 / dust_metric_jet)**.5
        dust_momentum_jet = action.owner.source_mass * dust_velocity_jet / (dust_metric_jet * dust_clock_jet)
        field_basis = row['shape']
        gradient_basis = quad['radial'] / jacobian[:, None]
        changed_gradient_basis = quad['radial'] / changed_jacobian[:, None]
        targets = [
            ('momentum_rate', (changed_jacobian * changed['momentum_rate']).imag / step,
                (changed_jacobian * changed['source_momentum_rate']).imag / step, dust_changed[2].imag / step, field_basis),
            ('oracle_momentum_rate', momentum_jet.parts[3], source_jet.parts[3], float(dust_momentum_jet.parts[3]), field_basis),
            ('force_wave', (changed_jacobian[:, None] * changed['force_field'][:, None] * changed_gradient_basis).imag / step,
                (changed_jacobian * changed['force_source']).imag / step, dust_changed[1].imag / step, None),
            ('base_momentum', jacobian * base['momentum'], -displacement * row['gradient'] * base['momentum'], dust_base[0], field_basis),
            ('base_force_wave', jacobian * base['force_field'], jacobian * base['force_source'], dust_base[1], gradient_basis)]
        for name, density, source_density, dust, basis in targets:
            field_covector = np.zeros(loads.rates.shape[1] - 1)
            local_covector = quad['measure'][:, None] * (density if basis is None else density[:, None] * basis)
            np.add.at(field_covector, indices[selected], local_covector[selected])
            source_covector = quad['measure'] @ source_density + dust
            output[name] += weight * np.outer(cardinal, np.r_[field_covector, source_covector])
        if include_native:
            force, halving, baseline = native_position_force(native, loads, action, label,
                field_direction, source_direction, directions['edge_vertices'], position)
            for name, value in [('force_native', force), ('native_halving_difference', halving), ('base_force_native', baseline)]:
                output[name] += weight * np.outer(cardinal, value)
        if index % 8 == 7:
            progress('material' + str(order) + '-label' + str(index + 1))
    output['force'] = output['force_wave'] + output['force_native']
    output['residual'] = output['momentum_rate'] - output['force']
    output['oracle_difference'] = output['oracle_momentum_rate'] - output['momentum_rate']
    return output
