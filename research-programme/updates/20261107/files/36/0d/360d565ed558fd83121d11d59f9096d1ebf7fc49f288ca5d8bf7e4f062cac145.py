import numpy as numerical

from annular_adm_mixed_action_20260909 import coefficient_jets, real_linear
from annular_metric_link_quadratic_20260909 import CachedMetricLinkRouthian


class ReleasedHermiteRouthian(CachedMetricLinkRouthian):
    def __init__(self, basis, scalar, slope, constants, kappa, momentum, slope_momentum, outer_clock, links):
        super().__init__(basis, scalar, slope / basis.spacing, numerical.zeros_like(slope), constants, kappa, momentum, outer_clock, links=links)
        self.slope, self.slope_momentum = slope, slope_momentum
        previous_count = self.count
        self.count += self.node_count
        self.slope_slice = slice(previous_count, self.count)
        self.maps = [numerical.pad(mapping, ((0, 0), (0, self.node_count))) for mapping in self.maps]
        self.node_maps = [numerical.pad(mapping, ((0, 0), (0, self.node_count))) for mapping in self.node_maps]
        self.maps[3][:, self.slope_slice] = basis.lift_value / basis.spacing
        self.free = numerical.array([index for index in range(self.count) if index not in self.fixed])
        self.velocity_indices = numerical.arange(self.slices[2].start, self.count)
        self.free_velocity_indices = numerical.array([index for index in self.velocity_indices if index not in self.fixed])

    def evaluate(self, packed, include_gram, hessian=True):
        value, gradient, matrix = super().evaluate(packed, include_gram, hessian)
        value -= numerical.dot(self.slope_momentum, packed[self.slope_slice])
        gradient[self.slope_slice] -= self.slope_momentum
        return value, gradient, matrix

    def bulk_scalar_data(self, packed):
        mass, unused_mass_r, lapse, velocity = [real_linear(mapping, packed) for mapping in self.maps]
        radius, constants = self.basis.quadrature, self.constants
        spatial_f = 1 - 2 * mass / radius - constants['Lambda'] * radius**2 / 3
        scale = spatial_f**(-0.5)
        kinetic = -velocity**2 / lapse**2 + spatial_f * self.gradient_q**2
        principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
        derivative = -4 * constants['b2'] - 12 * constants['b3'] * kinetic
        return radius, lapse, velocity, spatial_f, scale, kinetic, principal, derivative

    def kinetic_matrix(self, packed, include_gram):
        radius, lapse, velocity, unused_f, scale, unused_kinetic, principal, derivative = self.bulk_scalar_data(packed)
        reconstruction = numerical.concatenate([self.basis.scalar_value, self.basis.lift_value / self.basis.spacing], axis=1)
        weight = self.basis.quadrature_weights * radius**2 * scale / lapse * (principal - 2 * derivative * velocity**2 / lapse**2)
        matrix = reconstruction.T @ (weight[:, None] * reconstruction)
        if include_gram:
            mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
            unused_coefficient, unused_gradient, hessian = coefficient_jets(node_velocity, self.gradient_node, mass, node_lapse, self.basis.radii, self.constants)
            matrix[:self.node_count, :self.node_count] -= numerical.diag(self.density * hessian[0, 0])
        return matrix

    def slope_canonical_momentum(self, packed):
        radius, lapse, velocity, unused_f, scale, unused_kinetic, principal, unused_derivative = self.bulk_scalar_data(packed)
        density = self.basis.quadrature_weights * radius**2 * scale * principal * velocity / lapse
        return real_linear((self.basis.lift_value / self.basis.spacing).T, density)

    def slope_force(self, packed, include_gram):
        radius, lapse, unused_velocity, spatial_f, scale, unused_kinetic, principal, unused_derivative = self.bulk_scalar_data(packed)
        measure = self.basis.quadrature_weights * radius**2 * lapse * scale
        force = -real_linear((self.basis.lift_value / self.basis.spacing).T, measure * self.constants['m_chi']**2 * self.scalar_q)
        force -= real_linear((self.basis.lift_gradient / self.basis.spacing).T, measure * principal * spatial_f * self.gradient_q)
        if include_gram:
            mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
            unused_coefficient, gradient, unused_hessian = coefficient_jets(node_velocity, self.gradient_node, mass, node_lapse, self.basis.radii, self.constants)
            force -= self.density * gradient[1] / self.basis.spacing
        return force

    def admissible(self, packed, include_gram):
        if not numerical.all(numerical.isfinite(packed)):
            return False, {'reason': 'nonfinite_state'}
        radius, lapse, unused_velocity, spatial_f, unused_scale, kinetic, principal, derivative = self.bulk_scalar_data(packed)
        node_mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
        node_f = 1 - 2 * node_mass / self.basis.radii - self.constants['Lambda'] * self.basis.radii**2 / 3
        if min(numerical.min(lapse), numerical.min(node_lapse), numerical.min(spatial_f), numerical.min(node_f)) <= 0:
            return False, {'reason': 'metric_chart_boundary'}
        coefficient = coefficient_jets(node_velocity, self.gradient_node, node_mass, node_lapse, self.basis.radii, self.constants)[0]
        hyperbolic = principal + 2 * kinetic * derivative
        if min(numerical.min(principal), numerical.min(hyperbolic), numerical.min(coefficient)) <= 0:
            return False, {'reason': 'principal_branch_boundary'}
        matrix = self.kinetic_matrix(packed, include_gram)
        eigenvalues = numerical.linalg.eigvalsh(matrix)
        return bool(eigenvalues[0] > 0), {'minimum_full_scalar_Legendre_eigenvalue': float(eigenvalues[0]), 'scalar_Legendre_condition': float(eigenvalues[-1] / eigenvalues[0]), 'minimum_F': float(min(numerical.min(spatial_f), numerical.min(node_f))), 'minimum_lapse': float(min(numerical.min(lapse), numerical.min(node_lapse))), 'minimum_hyperbolicity_factor': float(numerical.min(hyperbolic))}

    def scaling(self, seed):
        scalar_scale = max(numerical.max(numerical.abs(seed[self.slices[2]])), numerical.max(numerical.abs(seed[self.slope_slice])), 0.001)
        scales = numerical.concatenate([numerical.full(self.face_count, max(numerical.max(numerical.abs(seed[self.slices[0]])), 1)), numerical.full(self.node_count, max(numerical.max(numerical.abs(seed[self.slices[1]])), 0.1)), numerical.full(2 * self.node_count, scalar_scale)])[self.free]
        baseline = self.evaluate(seed, False)[2][numerical.ix_(self.free, self.free)]
        row_scale = numerical.maximum(numerical.max(numerical.abs(baseline * scales[None, :]), axis=1), 1e-12)
        return scales, row_scale

    def constraint_tangent(self, packed, include_gram, endpoint_acceleration, outer_clock_time):
        mass_speed, pairing, matter, gram = self.shift_mass_velocity(packed, include_gram)
        scalar_speed = packed[self.slices[2]]
        slope_speed = packed[self.slope_slice]
        momentum_speed = self.scalar_force(packed, include_gram)
        momentum_speed[[0, -1]] = 0
        slope_momentum_speed = self.slope_force(packed, include_gram)
        step = 1e-25
        changed = ReleasedHermiteRouthian(self.basis, self.scalar + 1j * step * scalar_speed, self.slope + 1j * step * slope_speed, self.constants, self.kappa, self.momentum + 1j * step * momentum_speed, self.slope_momentum + 1j * step * slope_momentum_speed, self.outer_clock + 1j * step * outer_clock_time, self.links)
        data_derivative = changed.evaluate(packed, include_gram, hessian=False)[1].imag / step
        jacobian = self.evaluate(packed, include_gram)[2]
        speed = numerical.zeros_like(packed)
        speed[self.fixed] = [mass_speed[0], endpoint_acceleration[0], endpoint_acceleration[-1]]
        forcing = real_linear(jacobian, speed) + data_derivative
        speed[self.free] = numerical.linalg.solve(jacobian[numerical.ix_(self.free, self.free)], -forcing[self.free])
        derivative_residual = (real_linear(jacobian, speed) + data_derivative)[self.free]
        shift_residual = real_linear(pairing, speed[self.slices[0]]) + matter - gram
        return {'packed_speed': speed, 'shift_mass_speed': mass_speed, 'momentum_speed': momentum_speed, 'slope_momentum_speed': slope_momentum_speed, 'constraint_derivative_residual': derivative_residual, 'shift_residual': shift_residual, 'pairing': pairing, 'matter_shift': matter, 'Gram_shift': gram, 'data_derivative': data_derivative}

    def independent_action(self, packed, include_gram):
        basis = self.basis
        mass, lapse, velocity = [packed[selected] for selected in self.slices]
        zero_face, zero_node = numerical.zeros(self.face_count), numerical.zeros(self.node_count)
        position = [self.scalar, mass, lapse, zero_face]
        speed = [velocity, zero_face, zero_node, zero_face]
        action = basis.action(position, speed, self.slope / basis.spacing, packed[self.slope_slice] / basis.spacing, self.constants, self.kappa)
        if include_gram:
            node_mass = real_linear(basis.face_to_node, mass)
            spatial_f = 1 - 2 * node_mass / basis.radii - self.constants['Lambda'] * basis.radii**2 / 3
            kinetic = -velocity**2 / lapse**2 + spatial_f * self.gradient_node**2
            principal = 1 - 4 * self.constants['b2'] * kinetic - 6 * self.constants['b3'] * kinetic**2
            derivative = -4 * self.constants['b2'] - 12 * self.constants['b3'] * kinetic
            coefficient = basis.radii**2 * lapse / numerical.sqrt(spatial_f) * (principal * spatial_f + 2 * derivative * (spatial_f * self.gradient_node)**2)
            action -= numerical.dot(self.density, coefficient)
        return action - numerical.dot(self.momentum, velocity) - numerical.dot(self.slope_momentum, packed[self.slope_slice]) - self.outer_clock * mass[-1] / self.kappa
