import numpy as numerical
from scipy.integrate import solve_ivp

from annular_adm_mixed_action_20260909 import coefficient_jets, linear_value_gradient, real_linear
from annular_gram_joint_action_20260909 import gram_matrices


def primitive_basis(radii, targets):
    result = numerical.zeros((targets.size, radii.size))
    for row, target in enumerate(targets):
        for index, width in enumerate(numerical.diff(radii)):
            fraction = numerical.clip((target - radii[index]) / width, 0, 1)
            result[row, index] += width * (fraction - fraction**2 / 2)
            result[row, index + 1] += width * fraction**2 / 2
    return result


class FactorLinks:
    def __init__(self, radii):
        self.radii = radii
        factors, sampling = gram_matrices(radii.size)
        self.factor, self.node = numerical.nonzero((factors != 0) | (sampling != 0))
        self.count = factors.shape[0]
        self.tweight = factors[self.factor, self.node]
        self.sweight = sampling[self.factor, self.node]
        self.anchors = real_linear(sampling, radii)[self.factor]
        self.targets = radii[self.node]
        self.first = -(primitive_basis(radii, self.targets) - primitive_basis(radii, self.anchors))
        self.second = numerical.zeros((self.node.size, radii.size, radii.size))
        gauss, weights = numerical.polynomial.legendre.leggauss(2)
        for pair, (anchor, target) in enumerate(zip(self.anchors, self.targets)):
            lower, upper = min(anchor, target), max(anchor, target)
            knots = numerical.concatenate([[lower], radii[(radii > lower) & (radii < upper)], [upper]])
            for left, right in zip(knots[:-1], knots[1:]):
                points = (left + right) / 2 + (right - left) * gauss / 2
                signed_weights = numerical.sign(target - anchor) * (right - left) * weights / 2
                value = linear_value_gradient(radii, points)[0]
                local_primitive = -(primitive_basis(radii, points) - primitive_basis(radii, numerical.full(2, anchor)))
                self.second[pair] -= value.T @ (signed_weights[:, None] * local_primitive)

    def collect(self, values):
        result = numerical.zeros(self.count, dtype=numerical.result_type(values))
        numerical.add.at(result, self.factor, values)
        return result

    def quadratic_map(self, first, second):
        return numerical.einsum('pij,i,j->p', self.second, first, second)


class LocalQuadraticPath:
    def __init__(self, basis, nodal, facial, constants):
        self.basis, self.constants = basis, constants
        self.links = FactorLinks(basis.radii)
        self.initial_position = [nodal['scalar'], facial['mass'], nodal['lapse'], numerical.zeros_like(facial['mass'])]
        self.initial_velocity = [nodal['scalar_time'], facial['mass_time'], nodal['lapse_time'], numerical.zeros_like(facial['mass'])]
        self.acceleration = nodal['scalar_second']
        self.gradient, self.gradient_time = nodal['gradient'], nodal['gradient_time']

    def path(self, time):
        position = [value + time * speed for value, speed in zip(self.initial_position, self.initial_velocity)]
        position[0] = position[0] + time**2 * self.acceleration / 2
        velocity = self.initial_velocity.copy()
        velocity[0] = velocity[0] + time * self.acceleration
        defect = self.gradient + time * self.gradient_time - real_linear(self.basis.derivative, position[0])
        defect_time = self.gradient_time - real_linear(self.basis.derivative, velocity[0])
        return position, velocity, defect, defect_time

    def components(self, time, displacement, speed):
        position, velocity, unused_defect, unused_defect_time = self.path(time)
        direction = [value + time * rate for value, rate in zip(displacement, speed)]
        radius = self.basis.radii
        scalar, mass_face, lapse, unused_shift = position
        scalar_time, mass_time_face, lapse_time, unused_shift_time = velocity
        mass = real_linear(self.basis.face_to_node, mass_face)
        mass_time = real_linear(self.basis.face_to_node, mass_time_face)
        gradient = self.gradient + time * self.gradient_time
        coefficient, coefficient_gradient, coefficient_hessian = coefficient_jets(scalar_time, gradient, mass, lapse, radius, self.constants)
        perturbation = numerical.stack([speed[0], real_linear(self.basis.derivative, direction[0]), real_linear(self.basis.face_to_node, direction[1]), direction[2], real_linear(self.basis.face_to_node, direction[3])])
        background_time = numerical.stack([self.acceleration, self.gradient_time, mass_time, lapse_time, numerical.zeros_like(radius)])
        coefficient_time = numerical.sum(coefficient_gradient * background_time, axis=0)
        first_coefficient = numerical.sum(coefficient_gradient * perturbation, axis=0)
        second_coefficient = numerical.einsum('ijn,in,jn->n', coefficient_hessian, perturbation, perturbation) / 2
        spatial_f = 1 - 2 * mass / radius - self.constants['Lambda'] * radius**2 / 3
        inverse_clock = 1 / (spatial_f * lapse**2)
        inverse_clock_time = inverse_clock * (2 * mass_time / (radius * spatial_f) - 2 * lapse_time / lapse)
        shift, shift_time = perturbation[4], real_linear(self.basis.face_to_node, speed[3])
        first_connection = -inverse_clock * shift
        first_connection_time = -inverse_clock_time * shift - inverse_clock * shift_time
        second_connection = -inverse_clock * shift * (2 * perturbation[2] / (radius * spatial_f) - 2 * perturbation[3] / lapse)
        first_link = real_linear(self.links.first, first_connection)
        first_link_time = real_linear(self.links.first, first_connection_time)
        second_link = real_linear(self.links.first, second_connection) + self.links.quadratic_map(first_connection_time, first_connection)
        return scalar, scalar_time, coefficient, coefficient_time, first_coefficient, second_coefficient, direction[0], speed[0], first_link, first_link_time, second_link

    def quadratic(self, time, displacement, speed, raw=False):
        scalar, velocity, coefficient, coefficient_time, first_coefficient, second_coefficient, perturbation, perturbation_time, first_link, first_link_time, second_link = self.components(time, displacement, speed)
        links = self.links
        node, factor = links.node, links.factor
        spacing = self.basis.spacing
        leading = links.collect(links.tweight * scalar[node])
        leading_time = links.collect(links.tweight * velocity[node])
        first_scalar = perturbation[node] + velocity[node] * first_link
        first = links.collect(links.tweight * first_scalar)
        quadratic_scalar = perturbation_time[node] * first_link + self.acceleration[node] * first_link**2 / 2
        factor_coefficient = links.collect(links.sweight * coefficient[node])
        first_density = links.collect(links.sweight * (first_coefficient[node] + coefficient_time[node] * first_link + coefficient[node] * first_link_time))
        density_dual = leading**2 / (2 * spacing)
        density_dual_time = leading * leading_time / spacing
        current = coefficient[node] * links.sweight * density_dual_time[factor] - velocity[node] * links.tweight * factor_coefficient[factor] * leading[factor] / spacing
        boundary_pair = first_coefficient[node] * first_link + coefficient[node] * second_link + coefficient_time[node] * first_link**2 / 2
        boundary = numerical.dot(density_dual, links.collect(links.sweight * boundary_pair))
        first_terms = numerical.sum(factor_coefficient * (first**2 + 2 * leading * links.collect(links.tweight * quadratic_scalar)) / (2 * spacing) + first_density * leading * first / spacing + links.collect(links.sweight * second_coefficient[node]) * density_dual)
        reduced = first_terms - numerical.dot(density_dual_time, links.collect(links.sweight * (first_coefficient[node] * first_link + coefficient_time[node] * first_link**2 / 2))) - numerical.dot(current, second_link)
        if not raw:
            return reduced, boundary
        step = 1e-25
        complex_parts = self.components(time + 1j * step, displacement, speed)
        unused_scalar, unused_velocity, changed_coefficient, changed_coefficient_time, changed_first, unused_second, unused_perturbation, unused_speed, changed_link, unused_link_time, changed_second_link = complex_parts
        derivative_pair = (changed_first[node] * changed_link + changed_coefficient[node] * changed_second_link + changed_coefficient_time[node] * changed_link**2 / 2).imag / step
        full_second_scalar = quadratic_scalar + velocity[node] * second_link
        unreduced = numerical.sum(factor_coefficient * (first**2 + 2 * leading * links.collect(links.tweight * full_second_scalar)) / (2 * spacing) + first_density * leading * first / spacing + links.collect(links.sweight * (second_coefficient[node] + derivative_pair)) * density_dual)
        return reduced, boundary, unreduced

    def exact_potential(self, time, displacement, speed, amplitude):
        links, radius = self.links, self.basis.radii
        face_to_node = self.basis.face_to_node
        mass0, mass_t = [real_linear(face_to_node, value) for value in [self.initial_position[1], self.initial_velocity[1]]]
        mass_variation, mass_rate = [real_linear(face_to_node, value) for value in [displacement[1], speed[1]]]
        shift0, shift_rate = [real_linear(face_to_node, value) for value in [displacement[3], speed[3]]]
        lapse0, lapse_t = self.initial_position[2], self.initial_velocity[2]

        def nodal_geometry(times):
            mass = mass0[None, :] + times[:, None] * mass_t + amplitude * (mass_variation + times[:, None] * mass_rate)
            lapse = lapse0[None, :] + times[:, None] * lapse_t + amplitude * (displacement[2] + times[:, None] * speed[2])
            shift = amplitude * (shift0 + times[:, None] * shift_rate)
            spatial_f = 1 - 2 * mass / radius - self.constants['Lambda'] * radius**2 / 3
            inverse = 1 / (spatial_f * lapse**2)
            inverse_time = inverse * (2 * (mass_t + amplitude * mass_rate) / (radius * spatial_f) - 2 * (lapse_t + amplitude * speed[2]) / lapse)
            denominator = 1 - inverse * shift**2
            connection = -inverse * shift / denominator
            connection_time = -(inverse_time * shift + inverse * amplitude * shift_rate) / denominator - inverse * shift * (inverse_time * shift**2 + 2 * inverse * shift * amplitude * shift_rate) / denominator**2
            return mass, lapse, shift, spatial_f, connection, connection_time

        distance = links.targets - links.anchors
        count = links.node.size

        def right_hand_side(position, values):
            times, jacobian = values.reshape(2, count)
            points = links.anchors + position * distance
            interpolation = linear_value_gradient(radius, points)[0]
            unused_mass, unused_lapse, unused_shift, unused_f, connection, connection_time = nodal_geometry(times)
            return numerical.concatenate([-distance * numerical.sum(interpolation * connection, axis=1), -distance * jacobian * numerical.sum(interpolation * connection_time, axis=1)])

        initial = numerical.concatenate([numerical.full(count, time), numerical.ones(count)])
        solution = solve_ivp(right_hand_side, (0, 1), initial, method='DOP853', rtol=2e-12, atol=2e-14)
        if not solution.success:
            raise RuntimeError(solution.message)
        times, jacobian = solution.y[:, -1].reshape(2, count)
        mass, lapse, shift, spatial_f, unused_connection, unused_time = nodal_geometry(times)
        row, node = numerical.arange(count), links.node
        lapse, shift, spatial_f = lapse[row, node], shift[row, node], spatial_f[row, node]
        scalar = self.initial_position[0][node] + times * self.initial_velocity[0][node] + times**2 * self.acceleration[node] / 2 + amplitude * (displacement[0][node] + times * speed[0][node])
        velocity = self.initial_velocity[0][node] + times * self.acceleration[node] + amplitude * speed[0][node]
        gradient = self.gradient[node] + times * self.gradient_time[node] + amplitude * (real_linear(self.basis.derivative, displacement[0])[node] + times * real_linear(self.basis.derivative, speed[0])[node])
        kinetic = -(velocity - shift * gradient)**2 / lapse**2 + spatial_f * gradient**2
        principal = 1 - 4 * self.constants['b2'] * kinetic - 6 * self.constants['b3'] * kinetic**2
        slope = -4 * self.constants['b2'] - 12 * self.constants['b3'] * kinetic
        raised = spatial_f * gradient + shift * (velocity - shift * gradient) / lapse**2
        coefficient = radius[node]**2 * lapse / numerical.sqrt(spatial_f) * (principal * (spatial_f - shift**2 / lapse**2) + 2 * slope * raised**2)
        leading = links.collect(links.tweight * scalar)
        density = links.collect(links.sweight * jacobian * coefficient)
        return numerical.sum(density * leading**2) / (2 * self.basis.spacing)
