from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_quadratic_core_20261002 import core_forms, source_geometry
from annular_source_flat_native_20261002 import movements
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_zero_rate_euler_20261001 import zero_rate_system, endpoint_traction, direct_momentum_jacobian
from decimal import Decimal, localcontext
from scipy.sparse import save_npz
import gc
import numpy as np


def coupled_system(evidence, loads, action, packet, branch, name, spatial, material, deadline, progress):
    progress(name + ':Hessian')
    system = zero_rate_system(action, spatial, material, deadline, progress)
    engine = NativeKernel(action.mesh, packet['gram_support'], branch == 'primary')
    points, weights = np.polynomial.legendre.leggauss(material)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    native_force = np.zeros_like(system['force'])
    energies, shapes, slopes, curvatures = [], [], [], []
    jump_errors, jump_scales, point_errors, point_scales = [], [], [], []
    interpolation_error = 0.
    with localcontext() as context:
        context.prec = 64
        for count, (label, weight) in enumerate(zip(points, weights)):
            data = physical_data(engine, loads, action, label)
            result = engine.evaluate(data['edges'], data['field'], data['beta'])
            source_force = sum(result['edge_gradient'] * data['displacement'], Decimal(0))
            source_force += sum(result['load'] * data['beta_radial'] * data['displacement'][engine.native_edges], Decimal(0))
            native_force -= weight * np.outer(data['cardinal'], np.r_[np.asarray(result['field_gradient'], float), float(source_force)])
            energies.append(float(result['energy']))
            shapes.append(core_forms(engine, data, data['field'][:, None], movements(engine, data['edges'], data['source']))[0][:, 0, 0])
            atom = result['atoms']
            selected = engine.native_edges[1:-1]
            indices = np.r_[engine.indices[:, 0], engine.indices[-1, 2]][engine.native_edges][1:-1]
            before, after = atom['slope_right'][selected - 1], atom['slope_left'][selected]
            field_load = result['field_gradient'][indices]
            shape_load = result['edge_gradient'][selected] + result['load'][1:-1] * data['beta_radial'][1:-1]
            point = field_load * (before + after) / 2 + shape_load
            jump = data['beta'][1:-1] * (after - before) - field_load
            jump_errors.append(float(maximum(jump)))
            jump_scales.append(float(maximum(field_load)))
            point_errors.append(float(maximum(point)))
            point_scales.append(float(maximum(abs(field_load * (before + after) / 2) + abs(shape_load))))
            slopes.append([float(atom['slope_right'][engine.anchor - 1]), float(atom['slope_left'][engine.anchor])])
            curvatures.append([float(atom['second'][engine.anchor - 1]), float(atom['second'][engine.anchor])])
            approximate = np.polynomial.chebyshev.chebval(2 * label, loads.native_factor_coefficients)
            image_scale = float(maximum(result['image']))
            image_error = float(np.max(abs(approximate - np.asarray(result['image'], float))))
            interpolation_error = max(interpolation_error, image_error / image_scale if image_scale else image_error)
            if count % 16 == 15:
                progress(name + ':native layer ' + str(count + 1))
    force = system['force'] + native_force
    acceleration = system['inverse'].solve(force.ravel()).reshape(force.shape)
    for repeat in range(2):
        residual = (system['matrix'] @ acceleration.ravel()).reshape(force.shape) - force
        acceleration -= system['inverse'].solve(residual.ravel()).reshape(force.shape)
    residual = (system['matrix'] @ acceleration.ravel()).reshape(force.shape) - force
    relative = float(system['inverse'].residual_norm(residual) / system['inverse'].residual_norm(force))
    evidence.check(name + ':complete_Euler', relative < 2e-11, relative)
    evidence.check(name + ':native_factor_interpolation', interpolation_error < 2e-8, interpolation_error)
    boundary = endpoint_traction(action, material)
    evidence.check(name + ':exact_outer_flux', not np.any(boundary))
    radial_nodes = action.solver.nodes
    beta = radial_nodes**2 * np.exp(action.solution['state'][1]) * np.sqrt(1 - 2 * action.solution['state'][0] / radial_nodes)
    radial_energy = float(action.solver.integrated(beta.ravel() * action.solver.fields['gram'][branch])[-1, -1])
    native_energy = float(weights @ np.array(energies))
    energy_error = abs(native_energy - radial_energy) / abs(native_energy) if native_energy else abs(radial_energy)
    evidence.check(name + ':native_energy_closure', energy_error < 2e-8, energy_error)
    direction = np.zeros_like(acceleration)
    direction[:, :-1] = .01 * np.sin(action.knots)[None, :]
    direction[:, -1] = .02
    direct = direct_momentum_jacobian(action, direction, spatial, material, deadline)
    expected = (system['matrix'] @ direction.ravel()).reshape(direction.shape)
    oracle_error = float(np.max(abs(direct - expected)) / np.max(abs(expected)))
    evidence.check(name + ':momentum_Jacobian', oracle_error < 2e-11, oracle_error)
    cardinal, speed, drift = source_geometry(action, points)
    source_acceleration = cardinal @ acceleration[:, -1]
    slopes, curvatures = np.array(slopes), np.array(curvatures)
    trace = speed[:, None] * curvatures + (drift + source_acceleration)[:, None] * slopes
    arrays = dict(acceleration=acceleration, force=force, native_force=native_force, wave_source_force=system['force'],
        residual=residual, labels=points, weights=weights, slopes=slopes, curvatures=curvatures, trace=trace,
        speed_square=speed, drift=drift, source_acceleration=source_acceleration, native_energy_layers=energies,
        shape_layers=shapes, jump_errors=jump_errors, jump_scales=jump_scales, point_errors=point_errors,
        point_scales=point_scales, boundary_force=boundary)
    path = evidence.output / (name + '-acceleration.npz')
    np.savez_compressed(path, **arrays)
    evidence.own(path, 'outputs')
    matrix_path = evidence.output / (name + '-mass.npz')
    save_npz(matrix_path, system['matrix'])
    evidence.own(matrix_path, 'outputs')
    item = dict(name=name, branch=branch, spatial=spatial, material=material, path=str(path.relative_to(evidence.root)),
        matrix_path=str(matrix_path.relative_to(evidence.root)), Euler_relative=relative,
        maximum_trace_residual=float(np.max(abs(trace))), maximum_acceleration=float(np.max(abs(acceleration))),
        maximum_shape_force=float(np.max(abs(shapes))), integrated_shape_force_max=float(np.max(abs(weights @ np.array(shapes)))),
        native_energy=native_energy, maximum_point_residual=max(point_errors), maximum_jump_residual=max(jump_errors),
        relative_point_residual=max(point_errors) / max(point_scales) if max(point_scales) else None,
        relative_jump_residual=max(jump_errors) / max(jump_scales) if max(jump_scales) else None,
        zero_native_load_normalization='not_applicable' if not max(jump_scales) else 'native_load', valid_for_claim=False)
    matrix = system['matrix']
    del system
    gc.collect()
    return arrays, matrix, item
