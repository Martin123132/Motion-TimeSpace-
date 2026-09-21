import numpy as numerical

from annular_canonical_boundary_20260911 import CanonicalBoundarySystem
from annular_joint_weak_action_20260910 import joint_prototype
from annular_parent_coefficient_box_20260910 import Box


class CanonicalInitialData(CanonicalBoundarySystem):
    def __init__(self, *arguments, **keywords):
        super().__init__(*arguments, **keywords)
        self.mass_coeff_seed = numerical.concatenate([self.mass, numerical.zeros(self.count - 2)])
        self.pi_coeff_seed = self.packed[self.system.slices[2].start:].copy()
        self.fixed_lapse = self.lapse_seed.copy()
        self.endpoints = numerical.array([0, self.count - 1])
        self.data_count = self.mass_coeff_seed.size - 1 + 2 + 3
        prototype = joint_prototype(self.system, Box(self.packed), Box(self.configuration), False)
        knots = numerical.unique(numerical.concatenate([self.basis.radii, self.basis.faces]))
        points = self.links.points
        segment = numerical.searchsorted(knots, points, side='right') - 1
        fraction = (points - knots[segment]) / (knots[segment + 1] - knots[segment])
        bubble = numerical.zeros((points.size, 2 * (knots.size - 1)))
        rows = numerical.arange(points.size)
        bubble[rows, 2 * segment] = 4 * fraction * (1 - fraction)
        bubble[rows, 2 * segment + 1] = 4 * fraction * (1 - fraction) * (2 * fraction - 1)
        self.link_mass_map = numerical.concatenate([self.links.face_value, bubble @ prototype['bubble_lift_coefficients'].midpoint], axis=1)

    def seed(self, reactions):
        return numerical.concatenate([self.mass_coeff_seed[1:], self.pi_coeff_seed[self.endpoints], reactions])

    def set_state(self, data):
        free_mass_count = self.mass_coeff_seed.size - 1
        mass_coeff = numerical.concatenate([self.mass_coeff_seed[:1], data[:free_mass_count]])
        pi_coeff = self.pi_coeff_seed.astype(numerical.result_type(data)).copy()
        pi_coeff[self.endpoints] = data[free_mass_count:free_mass_count + 2]
        self.mass = mass_coeff[:self.face_count]
        self.mass_q = self.maps['mass_map'] @ mass_coeff
        self.mass_r = self.maps['mass_gradient'] @ mass_coeff
        self.spatial_f = 1 - 2 * self.mass_q / self.radius
        self.node_f = 1 - 2 * (self.basis.face_to_node @ self.mass) / self.basis.radii
        self.link_f = 1 - 2 * (self.link_mass_map @ mass_coeff) / self.links.points
        self.pi = self.pi_map @ pi_coeff
        return mass_coeff, pi_coeff, data[-3:]

    def constraint(self):
        density = self.mass_r / (.1 * numerical.sqrt(self.spatial_f))
        density -= numerical.sqrt(self.spatial_f) * (self.pi**2 / (2 * self.radius**2) + self.radius**2 * self.scalar_gradient**2 / 2)
        value = self.basis.node_value.T @ (self.weights * density)
        if self.include_gram:
            value -= self.basis.radii**2 * numerical.sqrt(self.node_f) * self.gram_density
        return value

    def data_residual(self, data):
        unused_mass, unused_pi, reactions = self.set_state(data)
        if min(numerical.real(self.spatial_f).min(), numerical.real(self.node_f).min(), numerical.real(self.link_f).min()) <= .1:
            raise ValueError('Initial geometry left the positive chart.')
        evaluation = self.evaluate(numerical.concatenate([self.fixed_lapse, reactions]))
        return numerical.concatenate([self.constraint(), evaluation['residual']])

    def data_jacobian(self, data):
        matrix = numerical.empty((self.data_count, self.data_count))
        for column in range(self.data_count):
            changed = data.astype(complex)
            changed[column] += 1e-25j
            matrix[:, column] = self.data_residual(changed).imag / 1e-25
        self.set_state(data)
        return matrix
