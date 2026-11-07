from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_high_order_native_v2_20261003 import zero_system, maximum
from annular_source_flat_native_20261002 import movements
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_quadratic_core_20261002 import source_geometry
from annular_zero_rate_euler_20261001 import endpoint_traction
from decimal import Decimal, localcontext
from scipy.sparse import save_npz
from time import perf_counter
import gc
import numpy as np


def transport_shapes(engine, result, movement):
    atom, degree = result['atoms'], engine.basis.degree
    count = engine.count
    gradient = np.full(count, Decimal(0), dtype=object)
    velocity = np.full((count, movement.shape[1]), Decimal(0), dtype=object)
    counts = np.zeros(count, dtype=int)
    for local_index in range(degree + 1):
        local = Decimal(local_index) / degree
        slope = np.zeros(len(engine.indices), dtype=object)
        for power in reversed(range(1, degree + 1)):
            slope = slope * local + power * atom['polynomial'][:, power]
        slope /= atom['widths']
        shift = (1 - local) * movement[:-1] + local * movement[1:]
        indices = engine.indices[:, local_index]
        selected = indices >= 0
        np.add.at(gradient, indices[selected], slope[selected])
        np.add.at(velocity, indices[selected], shift[selected])
        np.add.at(counts, indices[selected], 1)
    selected = result['field_gradient'] != 0
    field_work = (result['field_gradient'][selected] * gradient[selected] / counts[selected]**2) @ velocity[selected]
    return np.asarray(field_work + result['edge_gradient'] @ movement, float)


def momentum_oracle(action, direction, spatial, material, deadline):
    result = np.zeros_like(direction, dtype=complex)
    step = 1e-20j
    points, weights = np.polynomial.legendre.leggauss(material)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    for label, weight in zip(points, weights):
        if perf_counter() > deadline:
            raise RuntimeError('Safe high-order momentum oracle boundary')
        row = action.samples(label, spatial)
        quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        velocity = step * (cardinal @ direction[:, -1])
        nodal_rate = step * (cardinal @ direction[:, :-1])
        temporal = np.sum(quad['shape'] * nodal_rate[quad['indices']], axis=1) + velocity * row['motion']
        integrand = quad['measure'] * geometry['kinetic'] * temporal
        field = np.zeros(len(action.knots), dtype=complex)
        np.add.at(field, quad['indices'].ravel(), (integrand[:, None] * quad['shape']).ravel())
        metric_value = action.solver.values(action.solution, np.array([row['source']]))[0][:, 0]
        lapse, metric = np.exp(metric_value[1]), 1 - 2 * metric_value[0] / row['source']
        source = integrand @ row['motion'] + action.owner.source_mass * velocity / (metric * np.sqrt(lapse**2 - velocity**2 / metric))
        result += weight * np.outer(cardinal, np.r_[field, source])
    return result.imag / step.imag


def coupled_high(evidence, loads, action, branch, name, spatial, material, deadline, progress):
    progress(name + ':Hessian')
    system = zero_system(action, spatial, material, deadline, progress)
    engine = loads.native_engine
    points, weights = np.polynomial.legendre.leggauss(material)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    native_force = np.zeros_like(system['force'])
    energy, shape_rows, source_slopes, source_curvatures = [], [], [], []
    jump_errors, jump_scales, point_errors, point_scales = [], [], [], []
    native_slope_jumps, native_curvature_jumps, native_speeds, native_drifts, native_displacements = [], [], [], [], []
    interpolation_error = 0.
    with localcontext() as context:
        context.prec = 64
        for index, (label, weight) in enumerate(zip(points, weights)):
            if perf_counter() > deadline:
                raise RuntimeError('Safe high-order native layer boundary')
            data = physical_data(engine, loads, action, label)
            result = engine.evaluate(data['edges'], data['field'], data['beta'], data['beta_radial'])
            source_force = sum(result['edge_gradient'] * data['displacement'], Decimal(0))
            native_force -= weight * np.outer(data['cardinal'], np.r_[np.asarray(result['field_gradient'], float), float(source_force)])
            energy.append(float(result['energy']))
            shape_rows.append(transport_shapes(engine, result, movements(engine, data['edges'], data['source'])))
            atom = result['atoms']
            selected = engine.native_edges[1:-1]
            indices = engine.native_indices[1:-1]
            before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
            field_load = result['field_gradient'][indices]
            shape_load = result['edge_gradient'][selected]
            point = field_load * (before + after) / 2 + shape_load
            jump = data['beta'][1:-1] * (after - before) - field_load
            jump_errors.append(float(maximum(jump)))
            jump_scales.append(float(maximum(field_load)))
            point_errors.append(float(maximum(point)))
            point_scales.append(float(maximum(abs(field_load * (before + after) / 2) + abs(shape_load))))
            source_slopes.append([float(atom['slope_right'][engine.anchor - 1]), float(atom['slope_left'][engine.anchor])])
            source_curvatures.append([float(atom['curvature_right'][engine.anchor - 1]), float(atom['curvature_left'][engine.anchor])])
            native_slope_jumps.append(np.asarray(after - before, float))
            native_curvature_jumps.append(np.asarray(atom['curvature_left'][selected] - atom['curvature_right'][selected - 1], float))
            native_displacements.append(np.asarray(data['displacement'][selected], float))
            radius = np.asarray(data['edges'][selected], float)
            values, derivatives = action.solver.values(action.solution, radius)
            metric = 1 - 2 * values[0] / radius
            metric_radial = -2 * derivatives[0] / radius + 2 * values[0] / radius**2
            speed = np.exp(2 * values[1]) * metric
            native_speeds.append(speed)
            native_drifts.append(speed * (2 / radius + derivatives[1] + metric_radial / (2 * metric)))
            approximate = np.polynomial.chebyshev.chebval(2 * label, loads.native_factor_coefficients)
            image_scale = float(maximum(result['image']))
            image_error = float(np.max(abs(approximate - np.asarray(result['image'], float))))
            interpolation_error = max(interpolation_error, image_error / image_scale if image_scale else image_error)
            if index % 16 == 15:
                progress(name + ':native layer ' + str(index + 1))
    force = system['force'] + native_force
    acceleration = system['inverse'].solve(force.ravel()).reshape(force.shape)
    for repeat in range(2):
        residual = (system['matrix'] @ acceleration.ravel()).reshape(force.shape) - force
        acceleration -= system['inverse'].solve(residual.ravel()).reshape(force.shape)
    residual = (system['matrix'] @ acceleration.ravel()).reshape(force.shape) - force
    relative = float(system['inverse'].residual_norm(residual) / system['inverse'].residual_norm(force))
    boundary = endpoint_traction(action, material)
    radial_nodes = action.solver.nodes
    beta = radial_nodes**2 * np.exp(action.solution['state'][1]) * np.sqrt(1 - 2 * action.solution['state'][0] / radial_nodes)
    radial_energy = float(action.solver.integrated(beta.ravel() * action.solver.fields['gram'][branch])[-1, -1])
    native_energy = float(weights @ np.array(energy))
    energy_error = abs(native_energy - radial_energy) / abs(native_energy) if native_energy else abs(radial_energy)
    direction = np.zeros_like(acceleration)
    direction[:, :-1] = .01 * np.sin(action.knots)[None, :]
    direction[:, -1] = .02
    direct = momentum_oracle(action, direction, spatial, material, deadline)
    expected = (system['matrix'] @ direction.ravel()).reshape(direction.shape)
    oracle_error = float(np.max(abs(direct - expected)) / np.max(abs(expected)))
    cardinal, speed, drift = source_geometry(action, points)
    source_acceleration = cardinal @ acceleration[:, -1]
    source_slopes, source_curvatures = np.array(source_slopes), np.array(source_curvatures)
    trace = speed[:, None] * source_curvatures + (drift + source_acceleration)[:, None] * source_slopes
    corner = np.array(native_speeds) * np.array(native_curvature_jumps)
    corner += (np.array(native_drifts) + np.array(native_displacements) * source_acceleration[:, None]) * np.array(native_slope_jumps)
    arrays = dict(acceleration=acceleration, force=force, native_force=native_force, wave_source_force=system['force'],
        residual=residual, labels=points, weights=weights, slopes=source_slopes, curvatures=source_curvatures, trace=trace,
        speed_square=speed, drift=drift, source_acceleration=source_acceleration, native_energy_layers=energy,
        shape_layers=shape_rows, jump_errors=jump_errors, jump_scales=jump_scales, point_errors=point_errors,
        point_scales=point_scales, boundary_force=boundary, native_corner=corner, native_slope_jumps=native_slope_jumps,
        native_curvature_jumps=native_curvature_jumps, native_speed_square=native_speeds, native_drift=native_drifts,
        native_displacement=native_displacements, momentum_direction=direction, momentum_direct=direct)
    path = evidence.output / (name + '-acceleration.npz')
    np.savez_compressed(path, **arrays)
    evidence.own(path, 'outputs')
    matrix_path = evidence.output / (name + '-mass.npz')
    save_npz(matrix_path, system['matrix'])
    evidence.own(matrix_path, 'outputs')
    point_relative = max(point_errors) / max(point_scales) if max(point_scales) else None
    jump_relative = max(jump_errors) / max(jump_scales) if max(jump_scales) else None
    item = dict(name=name, branch=branch, spatial=spatial, material=material, path=str(path.relative_to(evidence.root)),
        matrix_path=str(matrix_path.relative_to(evidence.root)), Euler_relative=relative,
        maximum_trace_residual=float(np.max(abs(trace))), maximum_native_curvature_corner=float(np.max(abs(corner))),
        maximum_acceleration=float(np.max(abs(acceleration))), maximum_shape_force=float(np.max(abs(np.array(shape_rows)))),
        integrated_shape_force_max=float(np.max(abs(weights @ np.array(shape_rows)))), native_energy=native_energy,
        maximum_point_residual=max(point_errors), maximum_jump_residual=max(jump_errors),
        relative_point_residual=point_relative, relative_jump_residual=jump_relative,
        native_energy_closure=energy_error, native_factor_interpolation=interpolation_error,
        momentum_Jacobian_error=oracle_error, valid_for_claim=False)
    item['initial_gates'] = dict(source=item['maximum_trace_residual'] < 1e-9,
        native_curvature=item['maximum_native_curvature_corner'] < 1e-9,
        point=point_relative is not None and point_relative < 1e-8,
        jump=jump_relative is not None and jump_relative < 1e-7)
    item['initial_candidate'] = branch == 'primary' and all(item['initial_gates'].values())
    evidence.report['results'].append(item)
    evidence.save()
    evidence.check(name + ':complete_Euler', relative < 2e-11, relative)
    evidence.check(name + ':native_factor_interpolation', interpolation_error < 2e-8, interpolation_error)
    evidence.check(name + ':exact_outer_flux', not np.any(boundary))
    evidence.check(name + ':native_energy_closure', energy_error < 2e-8, energy_error)
    evidence.check(name + ':momentum_Jacobian', oracle_error < 2e-11, oracle_error)
    del system
    gc.collect()
    return arrays, item
