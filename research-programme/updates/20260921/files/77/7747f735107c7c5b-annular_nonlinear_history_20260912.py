import numpy as numerical
import sympy as symbolic
from scipy.integrate import solve_ivp

from annular_gram_joint_action_20260909 import gram_matrices


class CanonicalGeometry:
    def __init__(self):
        radius, mass, lapse, momentum = symbolic.symbols('radius mass lapse momentum', positive=True)
        kappa = symbolic.Rational(1, 10)
        geometry = 1 - 2 * mass / radius
        chart = 1 - kappa**2 * geometry**2 * momentum**2
        connection = kappa * symbolic.sqrt(geometry) * momentum / (lapse * chart)
        coefficient = radius**2 * lapse * symbolic.sqrt(geometry) * chart
        variables = [mass, lapse, momentum]
        expressions = [connection, coefficient, geometry, chart]
        expressions += [symbolic.diff(connection, variable) for variable in variables]
        expressions += [symbolic.diff(connection, first, second) for first in variables for second in variables]
        expressions += [symbolic.diff(coefficient, variable) for variable in variables]
        self.evaluator = symbolic.lambdify([radius] + variables, expressions, 'numpy', cse=True, docstring_limit=0)

    def evaluate(self, radius, fields):
        shape = numerical.broadcast_shapes(numerical.shape(radius), fields.shape[1:])
        evaluated = numerical.array([numerical.broadcast_to(value, shape) for value in self.evaluator(radius, *fields[:3])])
        if evaluated[2].real.min() <= 0 or evaluated[3].real.min() <= 0 or fields[1].real.min() <= 0:
            raise ValueError('Nonlinear history leaves F>0, N>0, or 1-kappa^2 F^2 P^2>0.')
        return {'c': evaluated[0], 'C': evaluated[1], 'F': evaluated[2], 'chart': evaluated[3], 'c_y': evaluated[4:7], 'c_yy': evaluated[7:16].reshape((3, 3) + shape), 'C_y': evaluated[16:19]}


class ManufacturedHistory:
    def __init__(self, soluble=False):
        self.soluble = soluble
        time, radius = symbolic.symbols('time radius', real=True)
        fraction = (radius - 6) * 8
        mass = 1 + symbolic.Rational(4, 1000) * fraction
        lapse = symbolic.Rational(9, 10) + symbolic.Rational(15, 1000) * fraction
        if soluble:
            connection = symbolic.Rational(3, 20) * (1 + fraction / 10) * (time + symbolic.Rational(4, 5))
            geometry = 1 - 2 * mass / radius
            scaled = lapse * symbolic.sqrt(geometry) * connection
            momentum = 20 * scaled / (geometry * (1 + symbolic.sqrt(1 + 4 * scaled**2)))
        else:
            mass += symbolic.Rational(3, 1000) * time + fraction * time / 1000 + symbolic.Rational(3, 10000) * time**2
            lapse += time / 100 + symbolic.Rational(3, 1000) * fraction * time**2
            momentum = symbolic.Rational(3, 5) + fraction / 10 + symbolic.Rational(3, 20) * time + fraction * time / 25 + time**2 / 50
        scalar = symbolic.Rational(1, 5) + symbolic.Rational(12, 1000) * fraction + fraction**3 / 200 + symbolic.Rational(3, 1000) * fraction**4
        scalar += symbolic.Rational(18, 1000) * time + symbolic.Rational(11, 1000) * fraction * time + symbolic.Rational(6, 1000) * fraction**2 * time + time**2 * (1 + fraction / 5) / 250
        fields = [mass, lapse, momentum, scalar]
        directions = [symbolic.Rational(3, 1000) * (1 - fraction / 5) * (1 + time * 3 / 10), (1 + fraction / 10) * (1 - time / 5 + time**2 / 10) / 50, (1 + fraction / 5) * (1 + time / 4) / 5, symbolic.Rational(9, 1000) * (fraction**3 - fraction * 3 / 10 + fraction**4 / 5) * (1 + time + time**2 / 10)]
        expressions = fields + [symbolic.diff(value, time) for value in fields] + [symbolic.diff(value, time, 2) for value in fields]
        expressions += directions + [symbolic.diff(value, time) for value in directions] + [symbolic.diff(value, time, 2) for value in directions]
        self.evaluator = symbolic.lambdify([time, radius], expressions, 'numpy', cse=True, docstring_limit=0)

    def evaluate(self, time, radius, direction, amplitude=0):
        shape = numerical.broadcast_shapes(numerical.shape(time), numerical.shape(radius))
        values = numerical.array([numerical.broadcast_to(value, shape) for value in self.evaluator(time, radius)])
        mask = numerical.asarray(direction).reshape((4,) + (1,) * len(shape))
        perturbations = [values[12 + 4 * order:16 + 4 * order] * mask for order in range(3)]
        fields = [values[4 * order:4 * order + 4] + amplitude * perturbations[order] for order in range(3)]
        return fields + perturbations

    def primitive(self, radius):
        offset = radius - 6
        return .15 * (offset + .4 * offset**2)

    def exact_transport(self, time, anchor, radius):
        jacobian = numerical.exp(self.primitive(radius) - self.primitive(anchor))
        return (time + .8) * jacobian - .8, jacobian


class HistoryAction:
    def __init__(self, history):
        self.history = history
        self.geometry = CanonicalGeometry()
        self.radii = numerical.linspace(5.875, 6.125, 17)
        self.spacing = self.radii[1] - self.radii[0]
        self.factors, self.sampling = gram_matrices(self.radii.size)
        self.factor, self.node = numerical.nonzero((self.factors != 0) | (self.sampling != 0))
        self.anchors = (self.sampling @ self.radii)[self.factor]
        self.targets = self.radii[self.node]
        self.distance = self.targets - self.anchors
        self.factor_weight = self.factors[self.factor, self.node]
        self.sample_weight = self.sampling[self.factor, self.node]

    def collect(self, values):
        return numerical.stack([numerical.sum(values[..., self.factor == index], axis=-1) for index in range(self.factors.shape[0])], axis=-1)

    def transport(self, times, direction, amplitude=0, tolerance=2e-12):
        shape = (len(times), len(self.node))
        initial = numerical.stack([numerical.broadcast_to(times[:, None], shape), numerical.ones(shape), numerical.zeros(shape), numerical.zeros(shape)])

        def right_hand_side(fraction, packed):
            transported, jacobian, variation, variation_rate = packed.reshape((4,) + shape)
            radius = self.anchors + fraction * self.distance
            fields, rates, accelerations, delta, delta_rate, unused_delta_acceleration = self.history.evaluate(transported, radius, direction, amplitude)
            geometry = self.geometry.evaluate(radius, fields)
            connection_time = numerical.sum(geometry['c_y'] * rates[:3], axis=0)
            connection_second = numerical.sum(geometry['c_y'] * accelerations[:3], axis=0) + numerical.einsum('ij...,i...,j...->...', geometry['c_yy'], rates[:3], rates[:3])
            source = numerical.sum(geometry['c_y'] * delta[:3], axis=0)
            source_time = numerical.sum(geometry['c_y'] * delta_rate[:3], axis=0) + numerical.einsum('ij...,i...,j...->...', geometry['c_yy'], rates[:3], delta[:3])
            return (self.distance * numerical.stack([geometry['c'], connection_time * jacobian, connection_time * variation + source, connection_time * variation_rate + (connection_second * variation + source_time) * jacobian])).ravel()

        result = solve_ivp(right_hand_side, (0, 1), initial.ravel(), method='DOP853', rtol=tolerance, atol=tolerance / 100, max_step=.125)
        if not result.success:
            raise RuntimeError(result.message)
        final = result.y[:, -1].reshape((4,) + shape)
        if final[1].min() <= 0:
            raise ValueError('Noninvertible manufactured time map.')
        return final

    def integrands(self, times, direction, amplitude=0, tolerance=2e-12):
        transported, jacobian, variation, variation_rate = self.transport(times, direction, amplitude, tolerance)
        fields, rates, unused_accelerations, delta, unused_delta_rate, unused_delta_acceleration = self.history.evaluate(transported, self.targets, direction, amplitude)
        geometry = self.geometry.evaluate(self.targets, fields)
        coefficient, scalar, scalar_time = geometry['C'], fields[3], rates[3]
        coefficient_time = numerical.sum(geometry['C_y'] * rates[:3], axis=0)
        direct_coefficient = numerical.sum(geometry['C_y'] * delta[:3], axis=0)
        leading = self.collect(self.factor_weight * scalar)
        density = self.collect(self.sample_weight * jacobian * coefficient)
        leading_time = self.collect(self.factor_weight * jacobian * scalar_time)
        current = leading[:, self.factor] * (self.sample_weight * coefficient * leading_time[:, self.factor] - self.factor_weight * scalar_time * density[:, self.factor]) / self.spacing
        scalar_covector = leading[:, self.factor] * density[:, self.factor] * self.factor_weight / self.spacing
        coefficient_covector = leading[:, self.factor]**2 * self.sample_weight / (2 * self.spacing)
        raw = -numerical.sum(scalar_covector * (delta[3] + scalar_time * variation) + coefficient_covector * (coefficient * variation_rate + jacobian * (coefficient_time * variation + direct_coefficient)), axis=-1)
        direct = -numerical.sum(scalar_covector * delta[3] + coefficient_covector * jacobian * direct_coefficient, axis=-1)
        transport = numerical.sum(current * variation, axis=-1)
        boundary = -numerical.sum(coefficient_covector * coefficient * variation, axis=-1)
        return {'action': -numerical.sum(density * leading**2, axis=-1) / (2 * self.spacing), 'raw': raw, 'direct': direct, 'transport': transport, 'boundary': boundary, 'weighted_current_identity': self.collect(jacobian * current), 'T': transported, 'J': jacobian, 'F_min': float(geometry['F'].min()), 'chart_min': float(geometry['chart'].min()), 'P_max': float(abs(fields[2]).max())}

    def integrated(self, direction, amplitude=0, order=20):
        points, weights = numerical.polynomial.legendre.leggauss(order)
        times, weights = .05 + .35 * points, .35 * weights
        result = self.integrands(numerical.concatenate([times, [-.3, .4]]), direction, amplitude)
        output = {key: float(weights @ result[key][:-2]) for key in ['action', 'raw', 'direct', 'transport']}
        output['boundary'] = float(result['boundary'][-1] - result['boundary'][-2])
        output['adjoint'] = output['direct'] + output['transport'] + output['boundary']
        output['weighted_current_error'] = float(abs(result['weighted_current_identity']).max())
        output['minimum_J'] = float(result['J'].min())
        output['maximum_time_displacement'] = float(abs(result['T'] - numerical.concatenate([times, [-.3, .4]])[:, None]).max())
        for key in ['F_min', 'chart_min', 'P_max']:
            output[key] = result[key]
        if self.history.soluble and amplitude == 0:
            exact_time, exact_jacobian = self.history.exact_transport(numerical.concatenate([times, [-.3, .4]])[:, None], self.anchors, self.targets)
            output['analytic_transport_error'] = float(max(abs(result['T'] - exact_time).max(), abs(result['J'] - exact_jacobian).max()))
        return output

    def physical_time_pullback(self, direction, order=16):
        if not self.history.soluble:
            raise ValueError('This independent quadrature uses an analytically invertible manufactured history.')
        nodes, weights = numerical.polynomial.legendre.leggauss(order)
        total, wrong_jacobian, wrong_time = 0., 0., 0.
        for factor_index in range(self.factors.shape[0]):
            mask = self.factor == factor_index
            node_index = self.node[mask]
            target_radii = self.targets[mask]
            factor_weights = self.factor_weight[mask]
            sample_weights = self.sample_weight[mask]
            anchor = self.anchors[mask][0]
            unused_times, endpoint_jacobian = self.history.exact_transport(0, anchor, target_radii)

            def current_at(anchor_time):
                endpoint_time, unused_jacobian = self.history.exact_transport(anchor_time[..., None], anchor, target_radii)
                fields, rates, unused_accel, unused_delta, unused_rate, unused_second = self.history.evaluate(endpoint_time, target_radii, direction)
                geometry = self.geometry.evaluate(target_radii, fields)
                leading = numerical.sum(factor_weights * fields[3], axis=-1)
                density = numerical.sum(sample_weights * endpoint_jacobian * geometry['C'], axis=-1)
                leading_time = numerical.sum(factor_weights * endpoint_jacobian * rates[3], axis=-1)
                return leading[..., None] * (sample_weights * geometry['C'] * leading_time[..., None] - factor_weights * rates[3] * density[..., None]) / self.spacing

            for local_index, target in enumerate(target_radii):
                radius = (anchor + target) / 2 + (target - anchor) * nodes / 2
                radial_weights = (target - anchor) * weights / 2
                lower, partial_jacobian = self.history.exact_transport(-.3, anchor, radius)
                upper, unused_jacobian = self.history.exact_transport(.4, anchor, radius)
                physical_times = (lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * nodes / 2
                time_weights = (upper - lower)[:, None] * weights / 2
                inverse_anchor_time = (physical_times + .8) / partial_jacobian[:, None] - .8
                fields, unused_rate, unused_accel, delta, unused_delta_rate, unused_delta_second = self.history.evaluate(physical_times, radius[:, None], direction)
                geometry = self.geometry.evaluate(radius[:, None], fields)
                direct_connection = numerical.sum(geometry['c_y'] * delta[:3], axis=0)
                kernel = current_at(inverse_anchor_time)[..., local_index] * endpoint_jacobian[local_index]
                integrand = kernel * direct_connection / partial_jacobian[:, None]**2
                total += float(radial_weights @ numerical.sum(time_weights * integrand, axis=-1))
                wrong_jacobian += float(radial_weights @ numerical.sum(time_weights * integrand * partial_jacobian[:, None], axis=-1))
                incorrect_kernel = current_at(physical_times)[..., local_index] * endpoint_jacobian[local_index]
                wrong_time += float(radial_weights @ numerical.sum(time_weights * incorrect_kernel * direct_connection / partial_jacobian[:, None]**2, axis=-1))
        return {'transport': total, 'wrong_single_J': wrong_jacobian, 'wrong_unpulled_anchor_time': wrong_time}
