from functools import lru_cache

import numpy as numerical
from scipy.integrate import solve_ivp

from annular_adm_clock_quadratic_20260909 import LocalQuadraticPath
from annular_adm_mixed_action_20260909 import coefficient_jets, linear_value_gradient, real_linear
from annular_constraint_routhian_20260909 import ConstraintRouthian
from annular_gram_joint_action_20260909 import gram_matrices


class MetricLinkQuadrature:
    def __init__(self, basis, order=8):
        factors, sampling = gram_matrices(basis.radii.size)
        self.factor, self.node = numerical.nonzero((factors != 0) | (sampling != 0))
        self.count = factors.shape[0]
        self.tweight = factors[self.factor, self.node]
        self.sweight = sampling[self.factor, self.node]
        self.anchors = real_linear(sampling, basis.radii)[self.factor]
        self.targets = basis.radii[self.node]
        gauss, weights = numerical.polynomial.legendre.leggauss(order)
        primitive = numerical.empty((order, order))
        for column in range(order):
            others = numerical.delete(gauss, column)
            polynomial = numerical.polynomial.Polynomial.fromroots(others) / numerical.prod(gauss[column] - others)
            integral = polynomial.integ()
            primitive[:, column] = integral(gauss) - integral(-1)
        all_knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
        points, signed_weights, pairs = [], [], []
        self.blocks = []
        offset = 0
        for pair, (anchor, target) in enumerate(zip(self.anchors, self.targets)):
            if anchor == target:
                continue
            lower, upper = min(anchor, target), max(anchor, target)
            knots = numerical.concatenate([[lower], all_knots[(all_knots > lower) & (all_knots < upper)], [upper]])
            if target < anchor:
                knots = knots[::-1]
            halfwidth = numerical.diff(knots) / 2
            centers = (knots[1:] + knots[:-1]) / 2
            local_points = (centers[:, None] + halfwidth[:, None] * gauss).ravel()
            local_weights = (halfwidth[:, None] * weights).ravel()
            size = local_points.size
            partial = numerical.zeros((size, size))
            for segment, half in enumerate(halfwidth):
                selected = slice(segment * order, (segment + 1) * order)
                partial[selected, :segment * order] = local_weights[:segment * order]
                partial[selected, selected] = half * primitive
            self.blocks.append((pair, slice(offset, offset + size), partial))
            points.extend(local_points)
            signed_weights.extend(local_weights)
            pairs.extend([pair] * size)
            offset += size
        self.points = numerical.asarray(points)
        self.weights = numerical.asarray(signed_weights)
        self.pairs = numerical.asarray(pairs, dtype=int)
        self.face_value = linear_value_gradient(basis.faces, self.points)[0]
        self.node_value = linear_value_gradient(basis.radii, self.points)[0]

    def collect(self, values):
        result = numerical.zeros((self.count,) + values.shape[1:], dtype=numerical.result_type(values))
        numerical.add.at(result, self.factor, values)
        return result

    def integrate(self, values):
        result = numerical.zeros((self.node.size,) + values.shape[1:], dtype=numerical.result_type(values))
        numerical.add.at(result, self.pairs, self.weights.reshape((-1,) + (1,) * (values.ndim - 1)) * values)
        return result

    def partial(self, values):
        result = numerical.empty_like(values)
        for unused_pair, selected, matrix in self.blocks:
            result[selected] = real_linear(matrix, values[selected])
        return result

    def inverse_clock(self, mass, lapse, constants):
        local_mass = real_linear(self.face_value, mass)
        local_lapse = real_linear(self.node_value, lapse)
        spatial_f = 1 - 2 * local_mass / self.points - constants['Lambda'] * self.points**2 / 3
        return 1 / (local_lapse**2 * spatial_f), spatial_f, local_lapse

    def matrix(self, mass, lapse, constants):
        inverse = self.inverse_clock(mass, lapse, constants)[0]
        return self.integrate(inverse[:, None] * self.face_value)


class CachedMetricLinkRouthian(ConstraintRouthian):
    def __init__(self, *arguments, links, **keywords):
        super().__init__(*arguments, **keywords)
        self.links = links

    def shift_mass_velocity(self, packed, include_gram):
        mass_speed, pairing, matter, gram = super().shift_mass_velocity(packed, False)
        if not include_gram:
            return mass_speed, pairing, matter, gram
        basis, links = self.basis, self.links
        mass, lapse, velocity = [packed[selected] for selected in self.slices]
        coefficient, gradient, unused_hessian = coefficient_jets(velocity, self.gradient_node, real_linear(basis.face_to_node, mass), lapse, basis.radii, self.constants)
        leading = links.collect(links.tweight * self.scalar[links.node])
        leading_time = links.collect(links.tweight * velocity[links.node])
        factor_coefficient = links.collect(links.sweight * coefficient[links.node])
        current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / basis.spacing
        current -= velocity[links.node] * links.tweight * factor_coefficient[links.factor] * leading[links.factor] / basis.spacing
        matrix = links.matrix(mass, lapse, self.constants)
        gram = real_linear(basis.face_to_node.T, self.density * gradient[4]) - real_linear(matrix.T, current)
        return numerical.linalg.solve(pairing, gram - matter), pairing, matter, gram


class MetricQuadraticPath(LocalQuadraticPath):
    def __init__(self, system, arrays, links=None):
        self.basis, self.constants = system.basis, system.constants
        self.links = links if links is not None else MetricLinkQuadrature(system.basis)
        mass, lapse, scalar_time = [arrays['corrected'][selected].copy() for selected in system.slices]
        mass_time, lapse_time, self.acceleration = [arrays['packed_speed'][selected].copy() for selected in system.slices]
        self.initial_position = [arrays['scalar'].copy(), mass, lapse, numerical.zeros_like(mass)]
        self.initial_velocity = [scalar_time, mass_time, lapse_time, numerical.zeros_like(mass)]
        self.gradient = real_linear(self.basis.derivative, arrays['scalar']) + arrays['defect']
        self.gradient_time = real_linear(self.basis.derivative, scalar_time) + arrays['defect_time']
        self.gradient_second = real_linear(self.basis.derivative, self.acceleration) + arrays['defect_acceleration']

    def path(self, time):
        position = [value + time * speed for value, speed in zip(self.initial_position, self.initial_velocity)]
        position[0] = position[0] + time**2 * self.acceleration / 2
        velocity = self.initial_velocity.copy()
        velocity[0] = velocity[0] + time * self.acceleration
        gradient = self.gradient + time * self.gradient_time + time**2 * self.gradient_second / 2
        gradient_time = self.gradient_time + time * self.gradient_second
        return position, velocity, gradient - real_linear(self.basis.derivative, position[0]), gradient_time - real_linear(self.basis.derivative, velocity[0])

    @lru_cache(maxsize=8)
    def background(self, time):
        position, velocity, unused_defect, unused_defect_time = self.path(time)
        basis, links = self.basis, self.links
        scalar, mass_face, lapse, unused_shift = position
        scalar_time, mass_time_face, lapse_time, unused_shift_time = velocity
        mass = real_linear(basis.face_to_node, mass_face)
        mass_time = real_linear(basis.face_to_node, mass_time_face)
        gradient = self.gradient + time * self.gradient_time + time**2 * self.gradient_second / 2
        gradient_time = self.gradient_time + time * self.gradient_second
        coefficient, coefficient_gradient, coefficient_hessian = coefficient_jets(scalar_time, gradient, mass, lapse, basis.radii, self.constants)
        coefficient_time = numerical.sum(coefficient_gradient * numerical.stack([self.acceleration, gradient_time, mass_time, lapse_time, numerical.zeros_like(lapse)]), axis=0)
        inverse, spatial_f, local_lapse = links.inverse_clock(mass_face, lapse, self.constants)
        inverse_time = inverse * (2 * real_linear(links.face_value, mass_time_face) / (links.points * spatial_f) - 2 * real_linear(links.node_value, lapse_time) / local_lapse)
        return scalar, scalar_time, coefficient, coefficient_time, coefficient_gradient, coefficient_hessian, inverse, inverse_time, spatial_f, local_lapse

    def components(self, time, displacement, speed):
        basis, links = self.basis, self.links
        scalar, scalar_time, coefficient, coefficient_time, coefficient_gradient, coefficient_hessian, inverse, inverse_time, spatial_f, lapse = self.background(time)
        direction = [value + time * rate for value, rate in zip(displacement, speed)]
        perturbation = numerical.stack([speed[0], real_linear(basis.derivative, direction[0]), real_linear(basis.face_to_node, direction[1]), direction[2], real_linear(basis.face_to_node, direction[3])])
        first_coefficient = numerical.sum(coefficient_gradient * perturbation, axis=0)
        second_coefficient = numerical.einsum('ijn,in,jn->n', coefficient_hessian, perturbation, perturbation) / 2
        shift = real_linear(links.face_value, direction[3])
        shift_time = real_linear(links.face_value, speed[3])
        relative = 2 * real_linear(links.face_value, direction[1]) / (links.points * spatial_f) - 2 * real_linear(links.node_value, direction[2]) / lapse
        generator = inverse * shift
        generator_time = inverse_time * shift + inverse * shift_time
        first_link = links.integrate(generator)
        first_link_time = links.integrate(generator_time)
        second_link = links.integrate(generator * relative + generator_time * links.partial(generator))
        return scalar, scalar_time, coefficient, coefficient_time, first_coefficient, second_coefficient, direction[0], speed[0], first_link, first_link_time, second_link

    def metric_velocity_position_block(self):
        scalar, scalar_time, coefficient, unused_time, unused_gradient, unused_hessian, inverse, unused_inverse_time, unused_f, unused_lapse = self.background(0)
        links, spacing = self.links, self.basis.spacing
        integrand = inverse[:, None] * links.face_value
        matrix = links.integrate(integrand)
        primitive = links.partial(integrand)
        leading = links.collect(links.tweight * scalar[links.node])
        leading_time = links.collect(links.tweight * scalar_time[links.node])
        factor_coefficient = links.collect(links.sweight * coefficient[links.node])
        density_map = links.collect((links.sweight * coefficient[links.node])[:, None] * matrix)
        scalar_map = links.collect((links.tweight * scalar_time[links.node])[:, None] * matrix)
        current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / spacing
        current -= scalar_time[links.node] * links.tweight * factor_coefficient[links.factor] * leading[links.factor] / spacing
        potential_block = density_map.T @ ((leading / spacing)[:, None] * scalar_map)
        potential_block -= integrand.T @ ((links.weights * current[links.pairs])[:, None] * primitive)
        return -potential_block

    def exact_potential(self, time, displacement, speed, amplitude):
        basis, links, constants = self.basis, self.links, self.constants
        mass, lapse = self.initial_position[1:3]
        mass_time, lapse_time = self.initial_velocity[1:3]
        distance, count = links.targets - links.anchors, links.node.size

        def geometry(points, times):
            face_value = linear_value_gradient(basis.faces, points)[0]
            node_value = linear_value_gradient(basis.radii, points)[0]
            mass_rate = real_linear(face_value, mass_time + amplitude * speed[1])
            lapse_rate = real_linear(node_value, lapse_time + amplitude * speed[2])
            local_mass = real_linear(face_value, mass + amplitude * displacement[1]) + times * mass_rate
            local_lapse = real_linear(node_value, lapse + amplitude * displacement[2]) + times * lapse_rate
            shift_rate = amplitude * real_linear(face_value, speed[3])
            local_shift = amplitude * real_linear(face_value, displacement[3]) + times * shift_rate
            spatial_f = 1 - 2 * local_mass / points - constants['Lambda'] * points**2 / 3
            inverse = 1 / (local_lapse**2 * spatial_f)
            inverse_time = inverse * (2 * mass_rate / (points * spatial_f) - 2 * lapse_rate / local_lapse)
            denominator = 1 - inverse * local_shift**2
            connection = -inverse * local_shift / denominator
            connection_time = -(inverse_time * local_shift + inverse * shift_rate) / denominator - inverse * local_shift * (inverse_time * local_shift**2 + 2 * inverse * local_shift * shift_rate) / denominator**2
            return local_lapse, local_shift, spatial_f, connection, connection_time

        def right_hand_side(parameter, values):
            times, jacobian = values.reshape(2, count)
            points = links.anchors + parameter * distance
            unused_lapse, unused_shift, unused_f, connection, connection_time = geometry(points, times)
            return numerical.concatenate([-distance * connection, -distance * jacobian * connection_time])

        initial = numerical.concatenate([numerical.full(count, time), numerical.ones(count)])
        solution = solve_ivp(right_hand_side, (0, 1), initial, method='DOP853', rtol=2e-13, atol=2e-15, max_step=0.05)
        if not solution.success:
            raise RuntimeError(solution.message)
        times, jacobian = solution.y[:, -1].reshape(2, count)
        node = links.node
        local_lapse, local_shift, spatial_f, unused_connection, unused_time = geometry(basis.radii[node], times)
        scalar = self.initial_position[0][node] + times * self.initial_velocity[0][node] + times**2 * self.acceleration[node] / 2 + amplitude * (displacement[0][node] + times * speed[0][node])
        velocity = self.initial_velocity[0][node] + times * self.acceleration[node] + amplitude * speed[0][node]
        gradient = self.gradient[node] + times * self.gradient_time[node] + times**2 * self.gradient_second[node] / 2 + amplitude * (real_linear(basis.derivative, displacement[0])[node] + times * real_linear(basis.derivative, speed[0])[node])
        kinetic = -(velocity - local_shift * gradient)**2 / local_lapse**2 + spatial_f * gradient**2
        principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
        slope = -4 * constants['b2'] - 12 * constants['b3'] * kinetic
        raised = spatial_f * gradient + local_shift * (velocity - local_shift * gradient) / local_lapse**2
        coefficient = basis.radii[node]**2 * local_lapse / numerical.sqrt(spatial_f) * (principal * (spatial_f - local_shift**2 / local_lapse**2) + 2 * slope * raised**2)
        leading = links.collect(links.tweight * scalar)
        density = links.collect(links.sweight * jacobian * coefficient)
        return numerical.sum(density * leading**2) / (2 * basis.spacing)
