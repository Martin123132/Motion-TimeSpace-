import numpy as numerical

from annular_adm_mixed_action_20260909 import coefficient_jets, hermite_matrices, real_linear
from annular_adm_clock_quadratic_20260909 import FactorLinks
from annular_constraint_routhian_20260909 import bulk_evaluator
from annular_gram_joint_action_20260909 import gram_matrices


class LocalWardIdentity:
    def __init__(self, system, arrays):
        self.system, self.arrays = system, arrays
        self.basis = system.basis
        self.node_count = system.node_count
        self.generator_count = 2 * self.node_count
        self.node_value = numerical.concatenate([numerical.eye(self.node_count), numerical.zeros((self.node_count, self.node_count))], axis=1)
        self.node_gradient = numerical.concatenate([numerical.zeros((self.node_count, self.node_count)), numerical.eye(self.node_count) / self.basis.spacing], axis=1)
        self.quad_value, self.quad_gradient = self.generator_maps(self.basis.quadrature)
        self.face_value, self.face_gradient = self.generator_maps(self.basis.faces)
        self.links = FactorLinks(self.basis.radii)
        self.anchor_value = self.generator_maps(self.links.anchors)[0]
        self.factors, self.sampling = gram_matrices(self.node_count)

    def generator_maps(self, targets):
        value, gradient, lift, lift_gradient = hermite_matrices(self.basis.radii, targets, numerical.zeros((self.node_count, self.node_count)))
        return value @ self.node_value + lift @ self.node_gradient, gradient @ self.node_value + lift_gradient @ self.node_gradient

    def connection_transport(self):
        mass = real_linear(self.basis.face_to_node, self.arrays['corrected'][self.system.slices[0]])
        lapse = self.arrays['corrected'][self.system.slices[1]]
        spatial_f = 1 - 2 * mass / self.basis.radii - self.system.constants['Lambda'] * self.basis.radii**2 / 3
        return -self.links.first @ (self.basis.face_to_node / (lapse**2 * spatial_f)[:, None])

    def state(self, time=0.0):
        basis, arrays, system = self.basis, self.arrays, self.system
        packed = arrays['corrected'] + time * arrays['packed_speed']
        mass, lapse, scalar_time = [packed[field] for field in system.slices]
        mass_time, lapse_time, scalar_second = [arrays['packed_speed'][field] for field in system.slices]
        scalar = arrays['scalar'] + time * arrays['corrected'][system.slices[2]] + time**2 * scalar_second / 2
        defect = arrays['defect'] + time * arrays['defect_time'] + time**2 * arrays['defect_acceleration'] / 2
        defect_time = arrays['defect_time'] + time * arrays['defect_acceleration']
        scalar_q = real_linear(basis.scalar_value, scalar) + real_linear(basis.lift_value, defect)
        velocity_q = real_linear(basis.scalar_value, scalar_time) + real_linear(basis.lift_value, defect_time)
        acceleration_q = real_linear(basis.scalar_value, scalar_second) + real_linear(basis.lift_value, arrays['defect_acceleration'])
        gradient_q = real_linear(basis.scalar_gradient, scalar) + real_linear(basis.lift_gradient, defect)
        gradient_time_q = real_linear(basis.scalar_gradient, scalar_time) + real_linear(basis.lift_gradient, defect_time)
        mass_q, mass_r, mass_time_q, mass_time_r = [real_linear(mapping, values) for mapping, values in [(basis.face_value, mass), (basis.face_gradient, mass), (basis.face_value, mass_time), (basis.face_gradient, mass_time)]]
        lapse_q, lapse_time_q = real_linear(basis.node_value, lapse), real_linear(basis.node_value, lapse_time)
        constants, radius = system.constants, basis.quadrature
        spatial_f = 1 - 2 * mass_q / radius - constants['Lambda'] * radius**2 / 3
        scale = spatial_f**(-0.5)
        raw = bulk_evaluator()(mass_q, mass_r, lapse_q, velocity_q, radius, scalar_q, gradient_q, system.kappa, constants['b2'], constants['b3'], constants['m_chi'], constants['Lambda'])
        values = numerical.stack([numerical.broadcast_to(value, radius.shape) for value in raw])
        kinetic = -velocity_q**2 / lapse_q**2 + spatial_f * gradient_q**2
        principal = 1 - 4 * constants['b2'] * kinetic - 6 * constants['b3'] * kinetic**2
        scalar_derivative = -radius**2 * lapse_q * scale * constants['m_chi']**2 * scalar_q
        gradient_derivative = -radius**2 * lapse_q * scale * principal * spatial_f * gradient_q
        shift_derivative = mass_time_q / (system.kappa * lapse_q * spatial_f**1.5) - radius**2 * scale * principal * velocity_q * gradient_q / lapse_q
        face_lapse = real_linear(basis.node_to_face, lapse)
        face_f = 1 - 2 * mass / basis.faces - constants['Lambda'] * basis.faces**2 / 3
        shift_generator = -(face_lapse**2 * face_f)[:, None] * self.face_gradient
        gradient_node = real_linear(basis.derivative, scalar) + defect
        gradient_time_node = real_linear(basis.derivative, scalar_time) + defect_time
        lifting_generator = gradient_time_node[:, None] * self.node_value + scalar_time[:, None] * self.node_gradient - real_linear(basis.derivative, scalar_time[:, None] * self.node_value)
        lifting_generator_time = (real_linear(basis.derivative, scalar_second) + arrays['defect_acceleration'])[:, None] * self.node_value + scalar_second[:, None] * self.node_gradient - real_linear(basis.derivative, scalar_second[:, None] * self.node_value)
        scalar_generator = scalar_time[:, None] * self.node_value
        actual_scalar = real_linear(basis.scalar_value, scalar_generator) + real_linear(basis.lift_value, lifting_generator)
        actual_velocity = real_linear(basis.scalar_value, scalar_second[:, None] * self.node_value) + real_linear(basis.lift_value, lifting_generator_time)
        actual_gradient = real_linear(basis.scalar_gradient, scalar_generator) + real_linear(basis.lift_gradient, lifting_generator)
        errors = {
            'mass_product': real_linear(basis.face_value, mass_time[:, None] * self.face_value) - mass_time_q[:, None] * self.quad_value,
            'mass_radial_product': real_linear(basis.face_gradient, mass_time[:, None] * self.face_value) - mass_time_r[:, None] * self.quad_value - mass_time_q[:, None] * self.quad_gradient,
            'lapse_product': real_linear(basis.node_value, lapse_time[:, None] * self.node_value) - lapse_time_q[:, None] * self.quad_value,
            'scalar_product': actual_scalar - velocity_q[:, None] * self.quad_value,
            'velocity_product': actual_velocity - acceleration_q[:, None] * self.quad_value,
            'scalar_radial_product': actual_gradient - gradient_time_q[:, None] * self.quad_value - velocity_q[:, None] * self.quad_gradient,
            'shift_product': real_linear(basis.face_value, shift_generator) + (lapse_q**2 * spatial_f)[:, None] * self.quad_gradient,
        }
        derivatives = [values[1], values[2], values[3], scalar_derivative, values[4], gradient_derivative, shift_derivative]
        amplitude_parts = {name: real_linear(error.T, basis.quadrature_weights * derivative) for (name, error), derivative in zip(errors.items(), derivatives)}
        time_parts = {
            'lapse_product': real_linear((real_linear(basis.node_value, lapse[:, None] * self.node_value) - lapse_q[:, None] * self.quad_value).T, basis.quadrature_weights * values[3]),
            'scalar_product': real_linear(errors['scalar_product'].T, basis.quadrature_weights * values[4]),
        }
        lift_force = real_linear(basis.lift_value.T, basis.quadrature_weights * scalar_derivative) + real_linear(basis.lift_gradient.T, basis.quadrature_weights * gradient_derivative)
        lift_momentum = real_linear(basis.lift_value.T, basis.quadrature_weights * values[4])
        return {'packed': packed, 'scalar': scalar, 'defect': defect, 'defect_time': defect_time, 'scalar_time': scalar_time, 'scalar_second': scalar_second, 'mass_time': mass_time, 'lapse_time': lapse_time, 'gradient_node': gradient_node, 'gradient_time_node': gradient_time_node, 'amplitude_parts': amplitude_parts, 'time_parts': time_parts, 'shift_generator': shift_generator, 'lifting_generator': lifting_generator, 'lifting_generator_time': lifting_generator_time, 'lift_force_bulk': lift_force, 'lift_momentum': lift_momentum, 'bulk_density': values[0]}

    def evaluate(self, include_gram):
        basis, arrays, system = self.basis, self.arrays, self.system
        state, derivative_state = self.state(), self.state(1j * 1e-25)
        time_derivatives = {name: value.imag / 1e-25 for name, value in derivative_state['time_parts'].items()}
        bulk_remainder = sum(state['amplitude_parts'].values()) - sum(time_derivatives.values())
        lift_euler = state['lift_force_bulk'] - derivative_state['lift_momentum'].imag / 1e-25
        gram_remainder = numerical.zeros(self.generator_count)
        coefficient_remainder = gram_remainder.copy()
        link_remainder = gram_remainder.copy()
        if include_gram:
            mass = real_linear(basis.face_to_node, arrays['corrected'][system.slices[0]])
            mass_time = real_linear(basis.face_to_node, state['mass_time'])
            lapse = arrays['corrected'][system.slices[1]]
            coefficient, gradient, unused_hessian = coefficient_jets(state['scalar_time'], state['gradient_node'], mass, lapse, basis.radii, system.constants)
            node_f = 1 - 2 * mass / basis.radii - system.constants['Lambda'] * basis.radii**2 / 3
            gamma = lapse**2 * node_f
            shift_node = real_linear(basis.face_to_node, state['shift_generator'])
            mass_error = real_linear(basis.face_to_node, state['mass_time'][:, None] * self.face_value) - mass_time[:, None] * self.node_value
            shift_error = shift_node + gamma[:, None] * self.node_gradient
            coefficient_error = gradient[2, :, None] * mass_error + gradient[4, :, None] * shift_error
            link = real_linear(self.connection_transport(), state['shift_generator'])
            link_error = link + self.node_value[self.links.node] - self.anchor_value
            factor_scalar = real_linear(self.factors, arrays['scalar'])
            factor_velocity = real_linear(self.factors, state['scalar_time'])
            factor_coefficient = real_linear(self.sampling, coefficient)
            current = coefficient[self.links.node] * self.links.sweight * factor_scalar[self.links.factor] * factor_velocity[self.links.factor] / basis.spacing
            current -= state['scalar_time'][self.links.node] * self.links.tweight * factor_coefficient[self.links.factor] * factor_scalar[self.links.factor] / basis.spacing
            coefficient_remainder = real_linear(coefficient_error.T, system.density)
            link_remainder = -real_linear(link_error.T, current)
            gram_remainder = coefficient_remainder + link_remainder
            lift_euler -= system.density * gradient[1]
        lifting_work = real_linear(state['lifting_generator'].T, lift_euler)
        complete_derivative = real_linear(arrays['Hessian_final'], arrays['packed_speed']) + arrays['data_derivative']
        scalar_euler = system.scalar_force(arrays['corrected'], include_gram) - complete_derivative[system.slices[2]] - arrays['momentum_speed']
        mass_euler = arrays['gradient_final'][system.slices[0]].copy()
        mass_euler[-1] += system.outer_clock / system.kappa
        lapse_euler_time = complete_derivative[system.slices[1]]
        scalar_work = real_linear(self.node_value.T, state['scalar_time'] * scalar_euler)
        mass_work = real_linear(self.face_value.T, state['mass_time'] * mass_euler)
        lapse_work = -real_linear(self.node_value.T, arrays['corrected'][system.slices[1]] * lapse_euler_time)
        shift_work = real_linear(state['shift_generator'].T, arrays['shift_residual'])
        predicted_shift_work = bulk_remainder - gram_remainder - lifting_work - scalar_work - mass_work - lapse_work
        return {'bulk_amplitude_' + name: value for name, value in state['amplitude_parts'].items()} | {'bulk_time_derivative_' + name: value for name, value in time_derivatives.items()} | {'bulk_remainder': bulk_remainder, 'Gram_coefficient_remainder': coefficient_remainder, 'Gram_link_remainder': link_remainder, 'Gram_remainder': gram_remainder, 'lifting_euler': lift_euler, 'lifting_work': lifting_work, 'scalar_euler': scalar_euler, 'scalar_endpoint_and_bulk_work': scalar_work, 'mass_boundary_and_bulk_work': mass_work, 'lapse_constraint_derivative_work': lapse_work, 'shift_generator': state['shift_generator'], 'shift_work': shift_work, 'predicted_shift_work': predicted_shift_work, 'identity_error': shift_work - predicted_shift_work}
