from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_directional_coupled_Euler_20260928 import layer, evaluate_wave, CHANNELS
from annular_support_shift_jet_20260928 import make_packet, wave_current, gram_block, perturb, interpolate
from annular_moving_Legendre_current_20260921 import samples
from annular_old_field_reaction_20260929 import coefficient_data
from annular_physical_native_kernel_20260928 import decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal
import numpy as np


def move_metric_packet(packet, row, action, instantaneous, time_response, baseline_time, amount):
    radius = packet['radius']
    values, radial = action.solver.values(action.solution, radius)
    if instantaneous is not None:
        change, change_r = instantaneous.solver.values(instantaneous.solution, radius)
        values = values + amount * change
        radial = radial + amount * change_r
    alpha, beta, alpha_r, beta_r = coefficient_data(radius, values, radial)
    metric_time = baseline_time.values(radius) + amount * time_response.values(radius)
    metric = 1 - 2 * values[0] / radius
    alpha_t = -alpha * (metric_time[1] - metric_time[0] / (radius * metric))
    return dict(packet, alpha=alpha, beta=beta, alpha_r=alpha_r, beta_r=beta_r, alpha_t=alpha_t)


def face_variation(packet, data, native, action, velocity_response, direction, amount):
    radius = np.asarray(data['edges'][1:-1], float)
    values, radial = action.solver.values(action.solution, radius)
    changed_values = values + amount * velocity_response.values(radius)
    alpha, beta, unused, unused2 = coefficient_data(radius, changed_values, radial)
    atoms = native.atoms(data['edges'], data['field'])
    left, right = np.asarray(atoms['slope_right'][:-1], float), np.asarray(atoms['slope_left'][1:], float)
    indices = native.indices[:-1, 2]
    selected = indices >= 0
    rates = (packet['node_rate'] + amount * direction['node_rate'])[np.maximum(indices, 0)] * selected
    speeds = np.asarray(data['displacement'][1:-1], float) * float(data['source_velocity'])
    speeds = speeds + amount * direction['edge_speed'][1:-1]
    left_time, right_time = rates - speeds * left, rates - speeds * right
    return (left - right) * (-alpha * speeds * (left_time + right_time) - beta * (left + right)) / 2


def native_columns(native, data, base, action, velocity_response, field_direction, edge_direction,
                   test_field, test_edges, amount=Decimal('1e-12')):
    edge_velocity = data['displacement'] * data['source_velocity']
    rate_change = native.tangent(data['edges'], data['field'], decimals(edge_direction), decimals(field_direction))
    base_change = native.tangent(data['edges'], data['field'], edge_velocity, data['rate'])
    base_current, direct_rate = [], []
    for power in range(3):
        base_current.append(gram_block(native, data, base, data['rate'], edge_velocity, power, base_change)['total'])
        direct_rate.append(gram_block(native, data, base, decimals(field_direction), decimals(edge_direction), power, rate_change)['total'])
    if not native.enabled:
        return np.asarray(base_current, float), np.zeros(4), 0.
    radius = np.asarray(data['edges'][native.native_edges], float)
    values, radial = action.solver.values(action.solution, radius)
    change, change_r = velocity_response.solver.values(velocity_response.solution, radius)
    unused, beta, unused2, beta_r = coefficient_data(radius, values + 1e-25j * change, radial + 1e-25j * change_r)
    beta_delta, beta_r_delta = decimals(beta.imag / 1e-25), decimals(beta_r.imag / 1e-25)
    coefficient_only, complete = [], []
    for sign in [-1, 1]:
        shifted = dict(data, beta=data['beta'] + sign * amount * beta_delta,
            beta_radial=data['beta_radial'] + sign * amount * beta_r_delta)
        result = native.evaluate(data['edges'], data['field'], shifted['beta'])
        force = sum(result['field_gradient'] * decimals(test_field), Decimal(0))
        force += sum(result['edge_gradient'] * decimals(test_edges), Decimal(0))
        force += sum(result['load'] * shifted['beta_radial'] * decimals(test_edges[native.native_edges]), Decimal(0))
        coefficients, totals = [force], [force]
        for power in range(3):
            coefficients.append(gram_block(native, shifted, result, data['rate'], edge_velocity, power, base_change)['total'])
            totals.append(gram_block(native, shifted, result,
                data['rate'] + sign * amount * decimals(field_direction),
                edge_velocity + sign * amount * decimals(edge_direction), power,
                base_change + sign * amount * rate_change)['total'])
        coefficient_only.append(np.asarray(coefficients, dtype=object))
        complete.append(np.asarray(totals, dtype=object))
    analytic = (coefficient_only[1] - coefficient_only[0]) / (2 * amount)
    analytic[1:] += np.asarray(direct_rate, dtype=object)
    direct = (complete[1] - complete[0]) / (2 * amount)
    return np.asarray(base_current, float), np.asarray(analytic, float), float(max(abs(direct - analytic)))


def columns_layer(native, loads, action, tangent, acceleration, polynomial, directions, correction,
                  acceleration_change, velocity_response, corrected_time, baseline_time, label, order=12, step=1e-25,
                  acceleration_uncertainty=None, metric_uncertainty=None):
    baseline, raw, unused = layer(native, loads, action, tangent, acceleration, polynomial,
        directions['edge_vertices'], directions['field_vertices'], label, order)
    row = samples(action, label, order)
    data = physical_data(native, loads, action, label)
    cardinal = data['cardinal']
    source_direction = -float(cardinal @ correction[:, -1])
    field_direction = cardinal @ (directions['field_vertices'] - correction[:, :-1])
    edge_direction = cardinal @ directions['edge_vertices'] + np.asarray(data['displacement'], float) * source_direction
    packet, direction = make_packet(native, data, raw, row, acceleration, field_direction, edge_direction, source_direction)
    direction['edge_speed'] = edge_direction
    amount = 1j * step
    changed = perturb(packet, direction, amount)
    acceleration_nodes = cardinal @ acceleration_change[:, :-1]
    acceleration_source = float(cardinal @ acceleration_change[:, -1])
    changed['acceleration'] = packet['acceleration'] + amount * interpolate(packet, acceleration_nodes)[0]
    changed['acceleration_r'] = packet['acceleration_r'] + amount * interpolate(packet, acceleration_nodes)[1]
    changed['speed_rate'] = packet['speed_rate'] + amount * row['geometry']['displacement'] * acceleration_source
    changed['source_acceleration'] = packet['source_acceleration'] + amount * acceleration_source
    changed['node_acceleration'] = packet['node_acceleration'] + amount * acceleration_nodes
    changed = move_metric_packet(changed, row, action, velocity_response, corrected_time, baseline_time, amount)
    changed['face_density_jump'] = face_variation(packet, data, native, action, velocity_response, direction, amount)
    acceleration_packet = perturb(packet, direction, amount, True)
    acceleration_packet = move_metric_packet(acceleration_packet, row, action, None, velocity_response, baseline_time, amount)
    changed_force, acceleration_force = evaluate_wave(changed), evaluate_wave(acceleration_packet)
    base_native = native.evaluate(data['edges'], data['field'], data['beta'])
    native_current, native_column, native_error = native_columns(native, data, base_native, action, velocity_response,
        field_direction, edge_direction, cardinal @ directions['field_vertices'], cardinal @ directions['edge_vertices'])
    source = float(data['source'])
    source_values = action.solver.values(action.solution, np.array([source]))[0][:, 0]
    source_change = velocity_response.values(np.array([source]))[:, 0]
    source_velocity = float(data['source_velocity'])

    def dust_current(values, speed):
        lapse, metric = np.exp(values[1]), 1 - 2 * values[0] / source
        return action.owner.source_mass * lapse**2 * speed / np.sqrt(lapse**2 - speed**2 / metric)

    dust_base = dust_current(source_values, source_velocity)
    dust_column = dust_current(source_values + amount * source_change, source_velocity + amount * source_direction).imag / step
    base = np.r_[baseline[CHANNELS.index('coupled_direct')],
        [wave_current(packet, power) + native_current[power] + dust_base * (source - 6)**power for power in range(3)]]
    column1 = np.r_[changed_force['wave_direct'].imag / step,
        [wave_current(changed, power).imag / step + dust_column * (source - 6)**power for power in range(3)]] + native_column
    column2 = np.r_[acceleration_force['wave_direct'].imag / step,
        [wave_current(acceleration_packet, power).imag / step for power in range(3)]]
    identity_error = float(abs(changed_force['wave_direct'].imag - changed_force['wave_identity'].imag) / step)
    reaction_delta = np.zeros(4)
    if acceleration_uncertainty is not None:
        altered = dict(packet)
        nodes = cardinal @ acceleration_uncertainty[:, :-1]
        source = float(cardinal @ acceleration_uncertainty[:, -1])
        altered['acceleration'] = packet['acceleration'] + amount * interpolate(packet, nodes)[0]
        altered['speed_rate'] = packet['speed_rate'] + amount * row['geometry']['displacement'] * source
        altered = move_metric_packet(altered, row, action, None, metric_uncertainty, baseline_time, amount)
        reaction_delta = np.r_[evaluate_wave(altered)['wave_direct'].imag / step,
            [wave_current(altered, power).imag / step for power in range(3)]]
    return dict(baseline=base, column1=column1, column2=column2, native_linear_error=native_error,
        face_identity_error=identity_error, native_column=native_column, reaction_column_delta=reaction_delta)


def gravity_columns(action, velocity_response, corrected_time, baseline_time, order):
    solver = velocity_response.solver
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = (solver.centers[:, None] + solver.lengths[:, None] * points / 2).ravel()
    measure = (solver.lengths[:, None] * weights / 2).ravel()
    values = action.solver.values(action.solution, radius)[0]
    metric = 1 - 2 * values[0] / radius
    coefficient = np.exp(values[1]) / (action.owner.coupling * np.sqrt(metric))
    base_time = baseline_time.values(radius)[0]
    variation = velocity_response.values(radius)
    variation_time = corrected_time.values(radius)[0]
    density = variation_time + base_time * (variation[1] + variation[0] / (radius * metric))
    rows = [base_time, density, variation[0]]
    return np.array([[measure @ (coefficient * row * (radius - 6)**power) for power in range(3)] for row in rows])


def compatibility(first, second, first_error, second_error):
    matrix = np.column_stack([second[1], second[2]])
    scales = np.max(abs(matrix), axis=0)
    if np.any(scales == 0):
        return dict(status='zero_column', finite_amplitude_solution_established=False)
    normalized = matrix / scales
    target_scale = max(float(np.max(abs(second[0]))), 1e-300)
    normalized_amplitude, unused, rank, singular = np.linalg.lstsq(normalized, -second[0] / target_scale, rcond=None)
    amplitudes = normalized_amplitude * target_scale / scales
    residual = second[0] + matrix @ amplitudes
    uncertainty = second_error[0] + abs(amplitudes[0]) * second_error[1] + abs(amplitudes[1]) * second_error[2]
    uncertainty += 64 * np.finfo(float).eps * (abs(second[0]) + abs(matrix) @ abs(amplitudes))
    coarse_matrix = np.column_stack([first[1], first[2]])
    coarse_amplitudes = np.linalg.lstsq(coarse_matrix / scales, -first[0] / target_scale, rcond=None)[0] * target_scale / scales
    perturbation = float(np.linalg.norm(np.column_stack([second_error[1], second_error[2]]) / scales, 2))
    paired = []
    for row in range(1, 4):
        block = normalized[[0, row]]
        determinant = float(np.linalg.det(block))
        if determinant == 0:
            paired.append(dict(current_power=row - 1, status='singular'))
            continue
        fitted = np.linalg.solve(block, -second[0, [0, row]] / target_scale) * target_scale / scales
        paired_residual = second[0] + matrix @ fitted
        paired_uncertainty = second_error[0] + abs(fitted[0]) * second_error[1] + abs(fitted[1]) * second_error[2]
        paired_uncertainty += 64 * np.finfo(float).eps * (abs(second[0]) + abs(matrix) @ abs(fitted))
        paired.append(dict(current_power=row - 1, status='force_and_one_current_solved',
            normalized_determinant=determinant, amplitudes=fitted.tolist(), residual=paired_residual.tolist(),
            sampled_uncertainty=paired_uncertainty.tolist(),
            all_rows_within_sampled_uncertainty=bool(np.all(abs(paired_residual) <= paired_uncertainty))))
    eliminated = None
    if matrix[0, 1] != 0:
        ratio = matrix[1:, 1] / matrix[0, 1]
        eliminated = dict(intercept=(second[0, 1:] - ratio * second[0, 0]).tolist(),
            slope=(matrix[1:, 0] - ratio * matrix[0, 0]).tolist())
    return dict(status='diagnostic_least_squares', normalized_rank=int(rank), singular_values=singular.tolist(),
        normalized_column_uncertainty=perturbation, rank_resolved=bool(singular[-1] > 5 * perturbation),
        amplitudes=amplitudes.tolist(), coarse_amplitudes=coarse_amplitudes.tolist(),
        residual=residual.tolist(), propagated_numerical_uncertainty=uncertainty.tolist(),
        residual_within_sampled_uncertainty=bool(np.all(abs(residual) <= uncertainty)),
        exact_force_current_pairs=paired, force_eliminated_currents=eliminated,
        uncertainty_is_rigorous_bound=False, finite_amplitude_solution_established=False)
