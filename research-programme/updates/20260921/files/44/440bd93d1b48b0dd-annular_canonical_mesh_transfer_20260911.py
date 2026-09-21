import numpy as numerical
from scipy.linalg import lstsq, solve

from annular_adm_mixed_action_20260909 import hermite_matrices, linear_value_gradient


def scalar_maps(basis, points):
    value, gradient, lift, lift_gradient = hermite_matrices(basis.radii, points, basis.derivative)
    return numerical.concatenate([value, lift / basis.spacing], axis=1), numerical.concatenate([gradient, lift_gradient / basis.spacing], axis=1)


def kinetic_weight(model, points):
    mass_value, mass_gradient = linear_value_gradient(model.basis.faces, points)
    lapse_value, lapse_gradient = linear_value_gradient(model.basis.radii, points)
    seed_mass = model.packed[model.system.slices[0]]
    mass, mass_r = mass_value @ seed_mass, mass_gradient @ seed_mass
    lapse, lapse_r = lapse_value @ model.lapse_seed, lapse_gradient @ model.lapse_seed
    spatial_f = 1 - 2 * mass / points
    spatial_f_r = -2 * mass_r / points + 2 * mass / points**2
    weight = points**2 / (lapse * numerical.sqrt(spatial_f))
    derivative = weight * (2 / points - lapse_r / lapse - spatial_f_r / (2 * spatial_f))
    return weight, derivative


def fields(model, mass_coeff, pi_coeff, points, scalar_velocity=None):
    if numerical.any(mass_coeff[model.face_count:] != 0):
        raise ValueError('This transfer covers zero initial mass bubbles only.')
    mass_value, mass_gradient = linear_value_gradient(model.basis.faces, points)
    value, gradient = scalar_maps(model.basis, points)
    weight, weight_r = kinetic_weight(model, points)
    auxiliary = value @ pi_coeff
    result = {
        'mass': mass_value @ mass_coeff[:model.face_count],
        'mass_gradient': mass_gradient @ mass_coeff[:model.face_count],
        'pi': weight * auxiliary,
        'pi_gradient': weight_r * auxiliary + weight * (gradient @ pi_coeff),
        'chi': value @ model.configuration,
        'chi_gradient': gradient @ model.configuration,
        'lapse': linear_value_gradient(model.basis.radii, points)[0] @ model.fixed_lapse,
    }
    if scalar_velocity is not None:
        result['q'] = value @ scalar_velocity
        result['q_gradient'] = gradient @ scalar_velocity
    spatial_f = 1 - 2 * result['mass'] / points
    result['F'] = spatial_f
    result['bulk_density'] = result['mass_gradient'] / (.1 * numerical.sqrt(spatial_f)) - numerical.sqrt(spatial_f) * (result['pi']**2 / (2 * points**2) + points**2 * result['chi_gradient']**2 / 2)
    return result


def split_quadrature(models, order):
    knots = numerical.unique(numerical.concatenate([array for model in models for array in [model.basis.radii, model.basis.faces]]))
    nodes, weights = numerical.polynomial.legendre.leggauss(order)
    centers, halfwidth = (knots[1:] + knots[:-1]) / 2, numerical.diff(knots) / 2
    return (centers[:, None] + halfwidth[:, None] * nodes).ravel(), (halfwidth[:, None] * weights).ravel()


def project_momentum(coarse, fine, mass_coeff, pi_coeff, order=8):
    if not numerical.array_equal(coarse.basis.radii[[0, -1]], fine.basis.radii[[0, -1]]):
        raise ValueError('Meshes cover different physical annuli.')
    points, weights = split_quadrature([coarse, fine], order)
    target = fields(coarse, mass_coeff, pi_coeff, points)['pi']
    reconstruction = scalar_maps(fine.basis, points)[0] * kinetic_weight(fine, points)[0][:, None]
    endpoints = numerical.array([0, fine.count - 1])
    endpoint_points = fine.basis.radii[endpoints]
    coefficients = numerical.zeros(2 * fine.count)
    coefficients[endpoints] = fields(coarse, mass_coeff, pi_coeff, endpoint_points)['pi'] / kinetic_weight(fine, endpoint_points)[0]
    free = numerical.setdiff1d(numerical.arange(coefficients.size), endpoints)
    matrix = numerical.sqrt(weights)[:, None] * reconstruction[:, free]
    load = numerical.sqrt(weights) * (target - reconstruction @ coefficients)
    column_scale = numerical.linalg.norm(matrix, axis=0)
    solution, unused_residual, rank, unused_singular = lstsq(matrix / column_scale, load, lapack_driver='gelsy')
    if rank != free.size:
        raise ValueError('Momentum transfer has deficient rank.')
    coefficients[free] = solution / column_scale
    normal_residual = matrix.T @ (matrix @ coefficients[free] - load)
    return coefficients, {'rank': int(rank), 'free_count': int(free.size), 'normal_residual_max': float(abs(normal_residual).max()), 'projection_order': order, 'endpoint_constraint_max': float(abs((scalar_maps(fine.basis, endpoint_points)[0] @ coefficients) * kinetic_weight(fine, endpoint_points)[0] - fields(coarse, mass_coeff, pi_coeff, endpoint_points)['pi']).max())}


def newton_initial_data(model, state, callback=None, maximum_iterations=35):
    state = state.copy()
    scales = numerical.maximum(numerical.max(abs(model.data_jacobian(state)), axis=1), 1e-12)
    history = []
    failure = None
    converged = False
    for iteration in range(maximum_iterations + 1):
        try:
            residual = model.data_residual(state)
            merit = float(abs(residual / scales).max())
            absolute = float(abs(residual).max())
            if not numerical.all(numerical.isfinite(residual)):
                raise ValueError('Nonfinite residual.')
            history.append({'iteration': iteration, 'scaled_residual': merit, 'absolute_residual': absolute})
            if callback:
                callback(history, state, scales)
            if merit < 1e-10 and absolute < 1e-9:
                converged = True
                break
            if iteration == maximum_iterations:
                raise RuntimeError('Newton iteration limit.')
            derivative = model.data_jacobian(state)
            correction = solve(derivative / scales[:, None], -residual / scales)
            accepted = False
            for power in range(22):
                trial = state + correction * 2.**(-power)
                try:
                    trial_merit = float(abs(model.data_residual(trial) / scales).max())
                except ValueError:
                    continue
                if numerical.isfinite(trial_merit) and trial_merit < merit:
                    history[-1]['step_fraction'] = 2.**(-power)
                    state, accepted = trial, True
                    break
            if not accepted:
                raise RuntimeError('Newton positive-chart line search failed.')
        except Exception as error:
            failure = repr(error)
            break
    model.set_state(state)
    return state, scales, history, converged, failure


def compare_fields(coarse_fields, fine_fields, weights):
    result = {}
    for name in coarse_fields.keys() & fine_fields.keys():
        difference = fine_fields[name] - coarse_fields[name]
        result[name + '_difference_max_sampled'] = float(abs(difference).max())
        result[name + '_difference_L2'] = float(numerical.sqrt(weights @ difference**2))
    return result
