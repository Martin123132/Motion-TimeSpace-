from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal, localcontext
import numpy as np


def decimal_array(values):
    array = np.asarray(values)
    return np.array([Decimal.from_float(float(value)) for value in array.ravel()], dtype=object).reshape(array.shape)


def mixed_current(packet, direction, ratio, power):
    with localcontext() as context:
        context.prec = 70
        keys = ['local', 'widths', 'radius', 'source', 'source_velocity', 'measure',
            'node_radius', 'node_rate', 'node_acceleration', 'node_speed',
            'alpha', 'beta', 'alpha_t', 'alpha_r', 'beta_r', 'gradient', 'rate', 'rate_r',
            'acceleration', 'acceleration_r', 'speed', 'speed_r', 'speed_rate', 'shift_scale']
        base = {key: decimal_array(packet[key]) for key in keys}
        base['source'] = base['source'].item()
        base['source_velocity'] = base['source_velocity'].item()
        local, widths = base['local'], base['widths']
        shapes = np.array([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)], dtype=object).T
        gradients = np.array([4 * local - 3, 4 - 8 * local, 4 * local - 1], dtype=object).T / widths[:, None]
        indices = packet['indices']

        def interpolate(values):
            selected = values[np.maximum(indices, 0)] * (indices >= 0)
            return np.sum(shapes * selected, axis=1), np.sum(gradients * selected, axis=1)

        def integral(radius, source):
            return ((radius - 6)**(power + 1) - (source - 6)**(power + 1)) / (power + 1)

        def evaluate(data, amount):
            primitive = integral(data['radius'], data['source'])
            node_primitive = integral(data['node_radius'], data['source'])
            test, node_test = (data['radius'] - 6)**power, (data['node_radius'] - 6)**power
            source_test = (data['source'] - 6)**power
            time_jacobian = 1 - amount * source_test * data['source_velocity']
            node_times = amount * node_primitive
            field_increment = data['node_rate'] * node_times + data['node_acceleration'] * node_times**2 / 2
            moved_gradient = data['gradient'] + interpolate(field_increment)[1]
            moved_rate_nodes = (data['node_rate'] + data['node_acceleration'] * node_times) * (time_jacobian + amount * node_test * data['node_speed'])
            moved_rate = data['rate'] + interpolate(moved_rate_nodes - data['node_rate'])[0]
            connection = amount * test
            root = np.array([(1 + 4 * value**2 * scale).sqrt() for value, scale in zip(connection, data['shift_scale'])], dtype=object)
            shift = 2 * connection * data['shift_scale'] / (1 + root)
            beta_t = -data['beta'] * data['alpha_t'] / data['alpha']
            moved_beta = (data['beta'] + beta_t * amount * primitive) * time_jacobian * (1 - shift**2 / data['shift_scale'])
            moved_alpha = data['alpha'] * data['beta'] / moved_beta
            temporal = moved_rate - data['speed'] * moved_gradient
            action = np.sum(data['measure'] * (moved_alpha * temporal**2 - moved_beta * moved_gradient**2)) / 2
            span = 1 + amount * data['speed_r']
            moved_gradient = (data['gradient'] + amount * data['rate_r'] + amount**2 * data['acceleration_r'] / 2) / span
            moved_alpha = data['alpha'] + amount * (data['alpha_t'] + data['speed'] * data['alpha_r'])
            moved_beta = data['beta'] + amount * (beta_t + data['speed'] * data['beta_r'])
            temporal = data['rate'] + amount * data['acceleration'] - (data['speed'] + amount * data['speed_rate']) * moved_gradient
            moved_source = data['source'] + amount * data['source_velocity']
            moved_nodes = data['node_radius'] + amount * data['node_speed']
            moved_radius = data['radius'] + amount * data['speed']
            weighted = interpolate((data['node_rate'] + amount * data['node_acceleration']) * integral(moved_nodes, moved_source))[0]
            energy = (moved_alpha * temporal**2 + moved_beta * moved_gradient**2) / 2
            endpoint = np.sum(data['measure'] * span * (moved_alpha * temporal * weighted - energy * integral(moved_radius, moved_source)))
            return action - endpoint

        changes = {key: decimal_array(direction[value]) for key, value in
            [('acceleration', 'rate'), ('acceleration_r', 'rate_r'), ('node_acceleration', 'node_rate'), ('speed_rate', 'speed')]}
        changes['alpha_t'] = base['alpha'] * decimal_array(ratio)
        amplitude = Decimal('.25')
        estimates = []
        for step in [Decimal('1e-9'), Decimal('5e-10')]:
            outer = []
            for sign in [1, -1]:
                changed = dict(base)
                for key, value in changes.items():
                    changed[key] = base[key] + sign * amplitude * value
                outer.append((evaluate(changed, step) - evaluate(changed, -step)) / (2 * step))
            estimates.append((outer[0] - outer[1]) / (2 * amplitude))
        extrapolated = (4 * estimates[1] - estimates[0]) / 3
        rate_mismatch = max(abs(interpolate(base['node_rate'])[0] - base['rate']))
        return extrapolated, abs(estimates[1] - estimates[0]), rate_mismatch
