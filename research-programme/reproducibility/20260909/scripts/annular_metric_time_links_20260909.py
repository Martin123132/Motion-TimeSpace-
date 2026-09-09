import numpy as numerical
from scipy.integrate import solve_ivp

from annular_adm_mixed_action_20260909 import coefficient_jets, linear_value_gradient, real_linear
from annular_adm_clock_quadratic_20260909 import FactorLinks
from annular_constraint_routhian_20260909 import ConstraintRouthian
from annular_local_ward_identity_20260909 import LocalWardIdentity
from annular_gram_joint_action_20260909 import gram_matrices


def metric_link_matrix(system, packed, order=8):
    basis = system.basis
    links = FactorLinks(basis.radii)
    mass, lapse = [packed[field] for field in system.slices[:2]]
    gauss, weights = numerical.polynomial.legendre.leggauss(order)
    result = numerical.zeros((links.node.size, system.face_count), dtype=numerical.result_type(packed))
    all_knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
    for pair, (anchor, target) in enumerate(zip(links.anchors, links.targets)):
        lower, upper = min(anchor, target), max(anchor, target)
        knots = numerical.concatenate([[lower], all_knots[(all_knots > lower) & (all_knots < upper)], [upper]])
        for left, right in zip(knots[:-1], knots[1:]):
            points = (left + right) / 2 + (right - left) * gauss / 2
            signed_weights = numerical.sign(target - anchor) * (right - left) * weights / 2
            face_value = linear_value_gradient(basis.faces, points)[0]
            node_value = linear_value_gradient(basis.radii, points)[0]
            local_mass, local_lapse = real_linear(face_value, mass), real_linear(node_value, lapse)
            spatial_f = 1 - 2 * local_mass / points - system.constants['Lambda'] * points**2 / 3
            result[pair] += real_linear(face_value.T, signed_weights / (local_lapse**2 * spatial_f))
    return result


class MetricLinkRouthian(ConstraintRouthian):
    def shift_mass_velocity(self, packed, include_gram):
        mass_speed, pairing, matter, gram = super().shift_mass_velocity(packed, False)
        if not include_gram:
            return mass_speed, pairing, matter, gram
        basis = self.basis
        mass = real_linear(basis.face_to_node, packed[self.slices[0]])
        lapse, velocity = packed[self.slices[1]], packed[self.slices[2]]
        coefficient, gradient, unused_hessian = coefficient_jets(velocity, self.gradient_node, mass, lapse, basis.radii, self.constants)
        factors, sampling = gram_matrices(self.node_count)
        links = FactorLinks(basis.radii)
        factor_scalar = real_linear(factors, self.scalar)
        factor_velocity = real_linear(factors, velocity)
        factor_coefficient = real_linear(sampling, coefficient)
        current = coefficient[links.node] * links.sweight * factor_scalar[links.factor] * factor_velocity[links.factor] / basis.spacing
        current -= velocity[links.node] * links.tweight * factor_coefficient[links.factor] * factor_scalar[links.factor] / basis.spacing
        gram = real_linear(basis.face_to_node.T, self.density * gradient[4]) - real_linear(metric_link_matrix(self, packed).T, current)
        return numerical.linalg.solve(pairing, gram - matter), pairing, matter, gram


class MetricLinkWardIdentity(LocalWardIdentity):
    def connection_transport(self):
        return metric_link_matrix(self.system, self.arrays['corrected'])


def finite_metric_link_potential(system, arrays, probe, amplitude):
    basis, constants = system.basis, system.constants
    links = FactorLinks(basis.radii)
    mass, lapse, scalar_time = [arrays['corrected'][field] for field in system.slices]
    mass_time, lapse_time, scalar_second = [arrays['packed_speed'][field] for field in system.slices]
    gradient = real_linear(basis.derivative, arrays['scalar']) + arrays['defect']
    gradient_time = real_linear(basis.derivative, scalar_time) + arrays['defect_time']
    gradient_second = real_linear(basis.derivative, scalar_second) + arrays['defect_acceleration']
    distance = links.targets - links.anchors
    count = links.node.size

    def right_hand_side(position, values):
        times, jacobian = values.reshape(2, count)
        points = links.anchors + position * distance
        face_value = linear_value_gradient(basis.faces, points)[0]
        node_value = linear_value_gradient(basis.radii, points)[0]
        local_mass = real_linear(face_value, mass) + times * real_linear(face_value, mass_time)
        local_lapse = real_linear(node_value, lapse) + times * real_linear(node_value, lapse_time)
        local_shift = amplitude * real_linear(face_value, probe)
        spatial_f = 1 - 2 * local_mass / points - constants['Lambda'] * points**2 / 3
        inverse_clock = 1 / (local_lapse**2 * spatial_f)
        inverse_time = inverse_clock * (2 * real_linear(face_value, mass_time) / (points * spatial_f) - 2 * real_linear(node_value, lapse_time) / local_lapse)
        denominator = 1 - inverse_clock * local_shift**2
        connection = -inverse_clock * local_shift / denominator
        connection_time = -inverse_time * local_shift / denominator - inverse_clock * local_shift * inverse_time * local_shift**2 / denominator**2
        return numerical.concatenate([-distance * connection, -distance * jacobian * connection_time])

    solution = solve_ivp(right_hand_side, (0, 1), numerical.concatenate([numerical.zeros(count), numerical.ones(count)]), method='DOP853', rtol=2e-12, atol=2e-14)
    if not solution.success:
        raise RuntimeError(solution.message)
    times, jacobian = solution.y[:, -1].reshape(2, count)
    node = links.node
    node_mass = real_linear(basis.face_to_node, mass)[node] + times * real_linear(basis.face_to_node, mass_time)[node]
    node_lapse = lapse[node] + times * lapse_time[node]
    node_shift = amplitude * real_linear(basis.face_to_node, probe)[node]
    scalar = arrays['scalar'][node] + times * scalar_time[node] + times**2 * scalar_second[node] / 2
    velocity = scalar_time[node] + times * scalar_second[node]
    spatial_gradient = gradient[node] + times * gradient_time[node] + times**2 * gradient_second[node] / 2
    spatial_f = 1 - 2 * node_mass / basis.radii[node] - constants['Lambda'] * basis.radii[node]**2 / 3
    kinetic = -(velocity - node_shift * spatial_gradient)**2 / node_lapse**2 + spatial_f * spatial_gradient**2
    principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
    slope = -4 * constants['b2'] - 12 * constants['b3'] * kinetic
    raised_radial = spatial_f * spatial_gradient + node_shift * (velocity - node_shift * spatial_gradient) / node_lapse**2
    coefficient = basis.radii[node]**2 * node_lapse / numerical.sqrt(spatial_f) * (principal * (spatial_f - node_shift**2 / node_lapse**2) + 2 * slope * raised_radial**2)
    leading = links.collect(links.tweight * scalar)
    density = links.collect(links.sweight * coefficient * jacobian)
    return numerical.sum(density * leading**2) / (2 * basis.spacing)
