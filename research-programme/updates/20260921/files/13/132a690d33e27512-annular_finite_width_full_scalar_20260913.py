import numpy as np
from scipy.integrate import solve_ivp

from annular_covariant_scalar_action_20260912 import CovariantScalarAction


def smear_rule(order, shape):
    points, weights = np.polynomial.legendre.leggauss(order)
    fractions = (points + 1) / 2
    if shape == 'beta22':
        density = 6 * fractions * (1 - fractions)
    elif shape == 'beta23':
        density = 12 * fractions * (1 - fractions)**2
    else:
        raise ValueError(shape)
    return points / 2, weights * density / 2


class TranslatedScalarAction(CovariantScalarAction):
    def __init__(self, history, gram, displacement=0., geometry=None):
        super().__init__(history, gram)
        if geometry is not None:
            self.geometry = geometry
        self.radii = self.radii + displacement
        self.anchors = (self.sampling @ self.radii)[self.factor]
        self.targets = self.radii[self.node]
        self.distance = self.targets - self.anchors


class LayerModeHistory:
    def __init__(self, base):
        self.base = base
        self.soluble = False

    def evaluate(self, time, radius, direction, amplitude=0):
        fields, rates, second, unused_delta, unused_delta_rate, unused_delta_second = self.base.evaluate(time, radius, [0, 0, 0, 0])
        shape = np.sin(np.pi * (radius - 5.875) * 64)**2
        zeros = np.zeros_like(fields)
        delta, delta_rate, delta_second = zeros.copy(), zeros.copy(), zeros.copy()
        delta[3] = .01 * (1 + time) * shape * direction[3]
        delta_rate[3] = .01 * shape * direction[3]
        return [fields + amplitude * delta, rates + amplitude * delta_rate, second, delta, delta_rate, delta_second]


class ZeroShiftHistory:
    def __init__(self, base):
        self.base = base
        self.soluble = False

    def evaluate(self, time, radius, direction, amplitude=0):
        fields, rates, second, delta, delta_rate, delta_second = self.base.evaluate(time, radius, direction, amplitude)
        for values, changes in [(fields, delta), (rates, delta_rate), (second, delta_second)]:
            values[2] = amplitude * changes[2]
        return [fields, rates, second, delta, delta_rate, delta_second]


class FiniteWidthScalar:
    def __init__(self, history, gram, width, shape='beta22', smear_order=6):
        if width < 0 or width >= 1 / 64:
            raise ValueError('This pilot requires zero <= width < unchanged h.')
        self.history = history
        self.gram = gram
        self.width = width
        self.shape = shape
        self.offsets, self.weights = smear_rule(smear_order, shape)
        first = TranslatedScalarAction(history, gram, width * self.offsets[0])
        self.actions = [first] + [TranslatedScalarAction(history, gram, width * offset, first.geometry) for offset in self.offsets[1:]]

    def integrated(self, direction, amplitude=0, time_order=14):
        rows = [action.full_integrated(direction, amplitude, time_order) for action in self.actions]
        output = {}
        minimum = {'minimum_J', 'minimum_F', 'minimum_chart_d'}
        maximum = {'maximum_nonzero_P', 'weighted_current_error'}
        for key in rows[0]:
            values = np.array([row[key] for row in rows])
            output[key] = float(values.min() if key in minimum else values.max() if key in maximum else self.weights @ values)
        output['smear_weight_sum_error'] = float(abs(self.weights.sum() - 1))
        return output

    def zero_shift_energy_variation(self, direction, time_order=20):
        gauss, gauss_weights = np.polynomial.legendre.leggauss(time_order)
        times, time_weights = .05 + .35 * gauss, .35 * gauss_weights
        total, all_energy = 0., []
        for weight, action in zip(self.weights, self.actions):
            fields, rates, unused_second, delta, unused_delta_rate, unused_delta_second = action.history.evaluate(times[:, None], action.radii, direction)
            geometry = action.geometry.evaluate(action.radii, fields)
            coefficient = geometry['C']
            momentum = action.radii**4 * rates[3] / coefficient
            amplitude = fields[3] @ action.factors.T
            nodal_d = amplitude**2 @ action.sampling / (2 * action.spacing)
            energy = action.node_weights * momentum**2 / (2 * action.radii**2) + action.radii**2 * nodal_d
            root_f = np.sqrt(geometry['F'])
            source = np.sum(fields[1] * energy * delta[0] / (action.radii * root_f) - root_f * energy * delta[1], axis=1)
            total += weight * (time_weights @ source)
            all_energy.append(energy)
        return float(total), np.array(all_energy)


def proper_clock_integral(action):
    if not action.history.soluble:
        raise ValueError('Independent proper-clock test requires the analytic transport history.')
    nodes = action.radii
    anchors = action.sampling @ nodes
    sites = np.concatenate([nodes, anchors])
    count = sites.size
    gauss, weights = np.polynomial.legendre.leggauss(40)
    times, weights = .05 + .35 * gauss, .35 * weights
    fields = action.history.evaluate(times[:, None], sites, [0, 0, 0, 0])[0]
    geometry = action.geometry.evaluate(sites, fields)
    proper_lapse = fields[1] * np.sqrt(geometry['chart'])
    spans = weights @ proper_lapse
    node_count = nodes.size

    def rates(fraction, state):
        clock_time = state[:count]
        values, first, unused_second, unused_delta, unused_rate, unused_second_delta = action.history.evaluate(clock_time, sites, [0, 0, 0, 0])
        metric = action.geometry.evaluate(sites, values)
        local_lapse = values[1] * np.sqrt(metric['chart'])
        radial = 1 / np.sqrt(metric['F'] * metric['chart'])
        node_velocity = first[3, :node_count] / local_lapse[:node_count]
        kinetic = action.node_weights * nodes**2 * radial[:node_count] * node_velocity**2 / 2
        factor_time = clock_time[node_count:][action.factor]
        transported, jacobian = action.history.exact_transport(factor_time, action.anchors, action.targets)
        endpoint_values, unused_first, unused_second, unused_delta, unused_rate, unused_second_delta = action.history.evaluate(transported, action.targets, [0, 0, 0, 0])
        endpoint_metric = action.geometry.evaluate(action.targets, endpoint_values)
        endpoint_lapse = endpoint_values[1] * np.sqrt(endpoint_metric['chart'])
        endpoint_radial = 1 / np.sqrt(endpoint_metric['F'] * endpoint_metric['chart'])
        proper_transfer = endpoint_lapse * jacobian / local_lapse[node_count:][action.factor]
        amplitude = action.collect(action.factor_weight * endpoint_values[3])
        density = action.collect(action.sample_weight * proper_transfer * action.targets**2 / endpoint_radial)
        potential = -amplitude**2 * density / (2 * action.spacing)
        return np.concatenate([spans / local_lapse, spans * np.concatenate([kinetic, potential])])

    initial = np.concatenate([np.full(count, -.3), np.zeros(count)])
    solution = solve_ivp(rates, (0, 1), initial, method='DOP853', rtol=2e-12, atol=2e-14, max_step=1 / 16)
    if not solution.success:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]
    return {'action': float(final[count:].sum()), 'endpoint_coordinate_time_error': float(abs(final[:count] - .4).max()), 'minimum_proper_clock_span': float(spans.min()), 'ode_steps': solution.t.size - 1}


def covariance_control(base, pulled, order=16):
    gauss, weights = np.polynomial.legendre.leggauss(order)
    times, weights = .05 + .35 * gauss, .35 * weights
    transformed, jacobian, unused_Y, unused_Z = pulled.transport(times, [0, 0, 0, 0])
    anchor_H, anchor_Ht, unused_Hr, unused_Hrt = pulled.history.map(times[:, None], base.anchors)
    endpoint_H, endpoint_Ht, unused_Hr, unused_Hrt = pulled.history.map(transformed, base.targets)
    expected_T, expected_J = base.history.exact_transport(anchor_H, base.anchors, base.targets)
    fields = base.history.evaluate(expected_T, base.targets, [0, 0, 0, 0])[0]
    coefficient = base.geometry.evaluate(base.targets, fields)['C']
    amplitude = base.collect(base.factor_weight * fields[3])
    density = base.collect(base.sample_weight * expected_J * coefficient)
    factor_Ht = pulled.history.map(times[:, None], base.sampling @ base.radii)[1]
    spatial_reference = -np.sum(factor_Ht * density * amplitude**2, axis=1) / (2 * base.spacing)
    spatial_actual = pulled.integrands(times, [0, 0, 0, 0])['action']
    node_H, node_Ht, unused_Hr, unused_Hrt = pulled.history.map(times[:, None], base.radii)
    node_fields, node_rates, unused_second, unused_delta, unused_rate, unused_second_delta = base.history.evaluate(node_H, base.radii, [0, 0, 0, 0])
    node_C = base.geometry.evaluate(base.radii, node_fields)['C']
    kinetic_reference = (.5 * node_Ht * base.radii**4 * node_rates[3]**2 / node_C) @ base.node_weights
    kinetic_actual = pulled.kinetic(times, [0, 0, 0, 0])['action']
    endpoint_fields = pulled.history.evaluate(transformed, pulled.targets, [0, 0, 0, 0])[0]
    endpoint_C = pulled.geometry.evaluate(pulled.targets, endpoint_fields)['C']
    wrong_density = pulled.collect(pulled.sample_weight * endpoint_C)
    moved_amplitude = pulled.collect(pulled.factor_weight * endpoint_fields[3])
    wrong_spatial = -np.sum(wrong_density * moved_amplitude**2, axis=1) / (2 * pulled.spacing)
    return {'time_map_conjugacy_error': float(max(abs(endpoint_H - expected_T).max(), abs(endpoint_Ht * jacobian - expected_J * anchor_Ht).max())),
            'spatial_covariance_error': float(abs(spatial_actual - spatial_reference).max()),
            'kinetic_covariance_error': float(abs(kinetic_actual - kinetic_reference).max()),
            'integrated_covariance_error': float(abs(weights @ (spatial_actual + kinetic_actual - spatial_reference - kinetic_reference))),
            'drop_transport_J_negative_control': float(abs(wrong_spatial - spatial_reference).max())}
