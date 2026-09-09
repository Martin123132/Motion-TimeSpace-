import numpy as numerical
import sympy as symbolic
from scipy.integrate import solve_ivp

from annular_gram_joint_action_20260909 import gram_matrices, principal_coefficient


class ReferenceGeometry:
    def __init__(self, case, epsilon=0.1, sigma=0.05):
        advanced, radius = symbolic.symbols('v r', real=True)
        self.sigma = sigma
        self.domain = case['domain']['v']
        self.constants = {key: float(symbolic.sympify(value)) for key, value in case['parameters'].items()}
        self.functions = {}
        for name in ['scalar_ref', 'mass_ref', 'shift_ref']:
            expression = symbolic.S.Zero
            for order, harmonics in case['fields'][name].items():
                for harmonic, amplitude in harmonics.items():
                    mode = int(harmonic[3:])
                    phase = symbolic.cos(mode * advanced / symbolic.Rational(str(epsilon))) if harmonic.startswith('cos') else symbolic.sin(mode * advanced / symbolic.Rational(str(epsilon)))
                    expression += symbolic.Rational(str(epsilon))**int(order) * symbolic.sympify(amplitude, locals={'v': advanced, 'r': radius}) * phase
            expressions = [expression, symbolic.diff(expression, advanced), symbolic.diff(expression, advanced, 2), symbolic.diff(expression, radius) + symbolic.Rational(str(sigma)) * symbolic.diff(expression, advanced)]
            self.functions[name] = symbolic.lambdify((advanced, radius), expressions, 'numpy', cse=True, docstring_limit=0)
        self.minimum_advanced = float('inf')
        self.maximum_advanced = -float('inf')

    def fields(self, time, radius):
        time, radius = numerical.broadcast_arrays(time, radius)
        advanced = time + self.sigma * (radius - 4)
        self.minimum_advanced = min(self.minimum_advanced, float(numerical.min(advanced)))
        self.maximum_advanced = max(self.maximum_advanced, float(numerical.max(advanced)))
        if numerical.min(advanced) < self.domain[0] or numerical.max(advanced) > self.domain[1]:
            raise ValueError('Transport left the owned advanced-time domain; no extrapolation allowed')
        return {name: numerical.stack([numerical.broadcast_to(value, time.shape) for value in function(advanced, radius)]) for name, function in self.functions.items()}

    def connection(self, time, radius):
        data = self.fields(time, radius)
        mass, mass_time, mass_second = data['mass_ref'][:3]
        shift, shift_time, shift_second = data['shift_ref'][:3]
        exponential = numerical.exp(shift)
        lapse = 1 - 2 * mass / radius - self.constants['Lambda'] * radius**2 / 3
        if numerical.any(lapse <= 0):
            raise ValueError('This exterior coframe chart requires positive F')
        lapse_time, lapse_second = -2 * mass_time / radius, -2 * mass_second / radius
        inverse = 1 / (exponential * lapse)
        log_time = shift_time + lapse_time / lapse
        log_second = shift_second + lapse_second / lapse - (lapse_time / lapse)**2
        return self.sigma - inverse, inverse * log_time, inverse * (log_second - log_time**2)

    def matter(self, time, radius):
        data = self.fields(time, radius)
        scalar, velocity, acceleration, gradient = data['scalar_ref']
        primitive = numerical.stack([scalar, velocity, gradient, data['mass_ref'][0], data['shift_ref'][0], numerical.zeros_like(scalar)])
        density = principal_coefficient(primitive, radius, self.constants, self.sigma)
        return scalar, velocity, density


def coordinate_map(time, radius, size):
    epsilon = 0.03 * numerical.sin(0.7 * radius) * (1 + time) + 0.02 * numerical.cos(1.1 * radius) * time**2
    epsilon_time = 0.03 * numerical.sin(0.7 * radius) + 0.04 * numerical.cos(1.1 * radius) * time
    epsilon_radius = 0.021 * numerical.cos(0.7 * radius) * (1 + time) - 0.022 * numerical.sin(1.1 * radius) * time**2
    epsilon_second = 0.04 * numerical.cos(1.1 * radius)
    epsilon_mixed = 0.021 * numerical.cos(0.7 * radius) - 0.044 * numerical.sin(1.1 * radius) * time
    return time + size * epsilon, 1 + size * epsilon_time, size * epsilon_radius, size * epsilon_second, size * epsilon_mixed


def perturbation(time, radius):
    return 0.04 * numerical.sin(1.3 * radius) * (1 + time + time**2), 0.04 * numerical.sin(1.3 * radius) * (1 + 2 * time)


def layout(radii):
    factors, sampling = gram_matrices(radii.size)
    factor_index, node_index = numerical.nonzero((factors != 0) | (sampling != 0))
    anchors = sampling @ radii
    return factors, sampling, factor_index, node_index, anchors


def transport(reference, anchor_time, anchors, targets, coordinate_size=0.0, forcing_size=0.0, sensitivity=False, tolerance=2e-12):
    anchor_time, anchors, targets = numerical.broadcast_arrays(anchor_time, anchors, targets)
    shape = anchor_time.shape
    anchor_time, anchors, targets = [value.ravel() for value in [anchor_time, anchors, targets]]
    distance = targets - anchors
    count = distance.size
    initial = numerical.concatenate([anchor_time, numerical.ones(count), numerical.zeros(2 * count)])

    def right_hand_side(position, state):
        times, jacobian, varied_time, varied_jacobian = state.reshape(4, count)
        radius = anchors + position * distance
        mapped, map_time, map_radius, map_second, map_mixed = coordinate_map(times, radius, coordinate_size)
        connection, connection_time, connection_second = reference.connection(mapped, radius)
        if coordinate_size:
            connection_time = connection_time + map_mixed / map_time - (connection + map_radius) * map_second / map_time**2
            connection = (connection + map_radius) / map_time
        source, source_time = perturbation(times, radius)
        connection = connection + forcing_size * source
        connection_time = connection_time + forcing_size * source_time
        if sensitivity and (coordinate_size or forcing_size):
            raise ValueError('Tangent solver is evaluated only at the actual untransformed background')
        time_rhs = -distance * connection
        jacobian_rhs = -distance * connection_time * jacobian
        varied_time_rhs = -distance * (connection_time * varied_time + source) if sensitivity else numerical.zeros(count)
        varied_jacobian_rhs = -distance * (connection_time * varied_jacobian + (connection_second * varied_time + source_time) * jacobian) if sensitivity else numerical.zeros(count)
        return numerical.concatenate([time_rhs, jacobian_rhs, varied_time_rhs, varied_jacobian_rhs])

    solution = solve_ivp(right_hand_side, (0, 1), initial, method='DOP853', rtol=tolerance, atol=tolerance / 50)
    if not solution.success:
        raise RuntimeError(solution.message)
    values = solution.y[:, -1].reshape(4, *shape)
    if numerical.any(values[1] <= 0):
        raise ValueError('Orientation-preserving time transport required')
    return values, solution.nfev


def factor_action(reference, anchor_time, radii, coordinate_size=0.0, forcing_size=0.0, sensitivity=False, tolerance=2e-12):
    factors, sampling, factor_index, node_index, anchor_radii = layout(radii)
    spacing = float(radii[1] - radii[0])
    anchor_time = numerical.broadcast_to(anchor_time, (factors.shape[0],))
    transported, evaluations = transport(reference, anchor_time[factor_index], anchor_radii[factor_index], radii[node_index], coordinate_size, forcing_size, sensitivity, tolerance)
    times, jacobian, varied_time, varied_jacobian = transported
    mapped, map_time, unused_radius, unused_second, unused_mixed = coordinate_map(times, radii[node_index], coordinate_size)
    scalar, velocity, density = reference.matter(mapped, radii[node_index])
    velocity = velocity * map_time
    density = density * map_time
    pull_density = jacobian * density
    pull_velocity = jacobian * velocity
    factor_scalar = numerical.bincount(factor_index, weights=factors[factor_index, node_index] * scalar, minlength=factors.shape[0])
    factor_velocity = numerical.bincount(factor_index, weights=factors[factor_index, node_index] * pull_velocity, minlength=factors.shape[0])
    factor_density = numerical.bincount(factor_index, weights=sampling[factor_index, node_index] * pull_density, minlength=factors.shape[0])
    value = factor_density * factor_scalar**2 / (2 * spacing)
    scalar_covector = factor_density[factor_index] * factor_scalar[factor_index] * factors[factor_index, node_index] / spacing
    density_covector = sampling[factor_index, node_index] * factor_scalar[factor_index]**2 / (2 * spacing)
    density_covector_time = sampling[factor_index, node_index] * factor_scalar[factor_index] * factor_velocity[factor_index] / spacing
    current = pull_density * density_covector_time - pull_velocity * scalar_covector
    integrated_connection_direction = -varied_time / jacobian
    bulk_variation = numerical.bincount(factor_index, weights=current * integrated_connection_direction, minlength=factors.shape[0])
    boundary_variation = numerical.bincount(factor_index, weights=density_covector * density * varied_time, minlength=factors.shape[0])
    return {'value': value, 'transport': transported, 'factor_index': factor_index, 'node_index': node_index, 'current': current, 'bulk_variation': bulk_variation, 'boundary_variation': boundary_variation, 'evaluations': evaluations, 'anchors': anchor_radii, 'factor_scalar': factor_scalar, 'factor_density': factor_density}
