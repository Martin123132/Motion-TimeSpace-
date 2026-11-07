from functools import lru_cache

import numpy as numerical
import sympy as symbolic

from annular_adm_mixed_action_20260909 import coefficient_jets, real_linear
from annular_gram_joint_action_20260909 import gram_matrices


@lru_cache(maxsize=1)
def bulk_evaluator():
    mass, mass_r, lapse, velocity, radius, scalar, gradient, kappa, quartic, sextic, potential_mass, cosmological = symbolic.symbols('mu mur N q r chi w kappa b2 b3 mc Lambda', real=True)
    spatial_f = 1 - 2 * mass / radius - cosmological * radius**2 / 3
    scale = spatial_f**(-symbolic.Rational(1, 2))
    kinetic = -velocity**2 / lapse**2 + spatial_f * gradient**2
    matter = -kinetic / 2 - potential_mass**2 * scalar**2 / 2 + quartic * kinetic**2 + sextic * kinetic**3
    lagrangian = lapse * scale * mass_r / kappa + radius**2 * lapse * scale * matter
    variables = [mass, mass_r, lapse, velocity]
    expressions = [lagrangian] + [symbolic.diff(lagrangian, variable) for variable in variables]
    expressions += [symbolic.diff(lagrangian, first, second) for first in variables for second in variables]
    return symbolic.lambdify([mass, mass_r, lapse, velocity, radius, scalar, gradient, kappa, quartic, sextic, potential_mass, cosmological], expressions, 'numpy', cse=True, docstring_limit=0)


class ConstraintRouthian:
    def __init__(self, basis, scalar, defect, defect_time, constants, kappa, momentum, outer_clock):
        self.basis, self.scalar = basis, scalar
        self.defect, self.defect_time = defect, defect_time
        self.constants, self.kappa = constants, kappa
        self.momentum, self.outer_clock = momentum, outer_clock
        self.node_count, self.face_count = basis.radii.size, basis.faces.size
        self.count = self.face_count + 2 * self.node_count
        face_slice = slice(0, self.face_count)
        lapse_slice = slice(self.face_count, self.face_count + self.node_count)
        velocity_slice = slice(self.face_count + self.node_count, self.count)
        self.slices = face_slice, lapse_slice, velocity_slice
        self.maps = [numerical.zeros((basis.quadrature.size, self.count)) for unused in range(4)]
        self.maps[0][:, face_slice] = basis.face_value
        self.maps[1][:, face_slice] = basis.face_gradient
        self.maps[2][:, lapse_slice] = basis.node_value
        self.maps[3][:, velocity_slice] = basis.scalar_value
        self.node_maps = [numerical.zeros((self.node_count, self.count)) for unused in range(3)]
        self.node_maps[0][:, face_slice] = basis.face_to_node
        self.node_maps[1][:, lapse_slice] = numerical.eye(self.node_count)
        self.node_maps[2][:, velocity_slice] = numerical.eye(self.node_count)
        self.scalar_q = real_linear(basis.scalar_value, scalar) + real_linear(basis.lift_value, defect)
        self.gradient_q = real_linear(basis.scalar_gradient, scalar) + real_linear(basis.lift_gradient, defect)
        self.gradient_node = real_linear(basis.derivative, scalar) + defect
        factors, sampling = gram_matrices(self.node_count)
        self.density = real_linear(sampling.T, real_linear(factors, scalar)**2) / (2 * basis.spacing)
        fixed = [0, self.face_count + self.node_count, self.count - 1]
        self.free = numerical.array([index for index in range(self.count) if index not in fixed])
        self.fixed = numerical.array(fixed)

    def evaluate(self, packed, include_gram, hessian=True):
        mass, mass_r, lapse, velocity = [real_linear(mapping, packed) for mapping in self.maps]
        velocity = velocity + real_linear(self.basis.lift_value, self.defect_time)
        radius = self.basis.quadrature
        constants = self.constants
        raw = bulk_evaluator()(mass, mass_r, lapse, velocity, radius, self.scalar_q, self.gradient_q, self.kappa, constants['b2'], constants['b3'], constants['m_chi'], constants['Lambda'])
        values = numerical.stack([numerical.broadcast_to(value, radius.shape) for value in raw])
        weights = self.basis.quadrature_weights
        value = numerical.dot(weights, values[0])
        gradient = sum(real_linear(mapping.T, weights * derivative) for mapping, derivative in zip(self.maps, values[1:5]))
        matrix = numerical.zeros((self.count, self.count), dtype=numerical.result_type(packed))
        if hessian:
            second = values[5:].reshape(4, 4, radius.size)
            for first in range(4):
                for other in range(4):
                    matrix += self.maps[first].T @ ((weights * second[first, other])[:, None] * self.maps[other])
        if include_gram:
            node_mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
            coefficient, coefficient_gradient, coefficient_hessian = coefficient_jets(node_velocity, self.gradient_node, node_mass, node_lapse, self.basis.radii, constants)
            value -= numerical.dot(self.density, coefficient)
            indices = [2, 3, 0]
            for selected, mapping in zip(indices, self.node_maps):
                gradient -= real_linear(mapping.T, self.density * coefficient_gradient[selected])
            if hessian:
                for first, first_map in zip(indices, self.node_maps):
                    for second, second_map in zip(indices, self.node_maps):
                        matrix -= first_map.T @ ((self.density * coefficient_hessian[first, second])[:, None] * second_map)
        face_slice, lapse_slice, velocity_slice = self.slices
        value -= self.outer_clock * packed[self.face_count - 1] / self.kappa + numerical.dot(self.momentum, packed[velocity_slice])
        gradient[self.face_count - 1] -= self.outer_clock / self.kappa
        gradient[velocity_slice] -= self.momentum
        return value, gradient, matrix

    def admissible(self, packed, include_gram):
        if not numerical.all(numerical.isfinite(packed)):
            return False, {'reason': 'nonfinite_state'}
        mass, unused_mass_r, lapse, velocity = [real_linear(mapping, packed) for mapping in self.maps]
        velocity += real_linear(self.basis.lift_value, self.defect_time)
        node_mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
        spatial_f = 1 - 2 * mass / self.basis.quadrature - self.constants['Lambda'] * self.basis.quadrature**2 / 3
        node_f = 1 - 2 * node_mass / self.basis.radii - self.constants['Lambda'] * self.basis.radii**2 / 3
        if min(numerical.min(lapse), numerical.min(node_lapse), numerical.min(spatial_f), numerical.min(node_f)) <= 0:
            return False, {'reason': 'metric_chart_boundary'}
        kinetic = -velocity**2 / lapse**2 + spatial_f * self.gradient_q**2
        principal = 1 - 4 * self.constants['b2'] * kinetic - 6 * self.constants['b3'] * kinetic**2
        slope = -4 * self.constants['b2'] - 12 * self.constants['b3'] * kinetic
        hyperbolic = principal + 2 * kinetic * slope
        coefficient = coefficient_jets(node_velocity, self.gradient_node, node_mass, node_lapse, self.basis.radii, self.constants)[0]
        if min(numerical.min(principal), numerical.min(hyperbolic), numerical.min(coefficient)) <= 0:
            return False, {'reason': 'principal_branch_boundary'}
        matrix = self.evaluate(packed, include_gram)[2]
        velocity_indices = numerical.arange(self.face_count + self.node_count + 1, self.count - 1)
        minimum = float(numerical.linalg.eigvalsh(matrix[numerical.ix_(velocity_indices, velocity_indices)])[0])
        return minimum > 0, {'minimum_scalar_Legendre_eigenvalue': minimum, 'minimum_F': float(min(numerical.min(spatial_f), numerical.min(node_f))), 'minimum_lapse': float(min(numerical.min(lapse), numerical.min(node_lapse))), 'minimum_hyperbolicity_factor': float(numerical.min(hyperbolic))}

    def scaling(self, seed):
        scales = numerical.concatenate([numerical.full(self.face_count, max(numerical.max(numerical.abs(seed[self.slices[0]])), 1)), numerical.full(self.node_count, max(numerical.max(numerical.abs(seed[self.slices[1]])), 0.1)), numerical.full(self.node_count, max(numerical.max(numerical.abs(seed[self.slices[2]])), 0.001))])[self.free]
        baseline = self.evaluate(seed, False)[2][numerical.ix_(self.free, self.free)]
        row_scale = numerical.maximum(numerical.max(numerical.abs(baseline * scales[None, :]), axis=1), 1e-12)
        return scales, row_scale

    def scalar_force(self, packed, include_gram):
        mass, unused_mass_r, lapse, velocity = [real_linear(mapping, packed) for mapping in self.maps]
        velocity += real_linear(self.basis.lift_value, self.defect_time)
        radius = self.basis.quadrature
        spatial_f = 1 - 2 * mass / radius - self.constants['Lambda'] * radius**2 / 3
        kinetic = -velocity**2 / lapse**2 + spatial_f * self.gradient_q**2
        principal = 1 - 4 * self.constants['b2'] * kinetic - 6 * self.constants['b3'] * kinetic**2
        measure = self.basis.quadrature_weights * radius**2 * lapse / numerical.sqrt(spatial_f)
        force = -real_linear(self.basis.scalar_value.T, measure * self.constants['m_chi']**2 * self.scalar_q)
        force -= real_linear(self.basis.scalar_gradient.T, measure * principal * spatial_f * self.gradient_q)
        if include_gram:
            node_mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
            coefficient, gradient, unused_hessian = coefficient_jets(node_velocity, self.gradient_node, node_mass, node_lapse, self.basis.radii, self.constants)
            factors, sampling = gram_matrices(self.node_count)
            force -= real_linear(factors.T, real_linear(sampling, coefficient) * real_linear(factors, self.scalar)) / self.basis.spacing
            force -= real_linear(self.basis.derivative.T, self.density * gradient[1])
        return force

    def shift_mass_velocity(self, packed, include_gram):
        from annular_adm_clock_quadratic_20260909 import FactorLinks

        mass, unused_mass_r, lapse, velocity = [real_linear(mapping, packed) for mapping in self.maps]
        velocity += real_linear(self.basis.lift_value, self.defect_time)
        radius = self.basis.quadrature
        spatial_f = 1 - 2 * mass / radius - self.constants['Lambda'] * radius**2 / 3
        kinetic = -velocity**2 / lapse**2 + spatial_f * self.gradient_q**2
        principal = 1 - 4 * self.constants['b2'] * kinetic - 6 * self.constants['b3'] * kinetic**2
        pairing = self.basis.face_value.T @ ((self.basis.quadrature_weights / (self.kappa * lapse * spatial_f**1.5))[:, None] * self.basis.face_value)
        matter = -real_linear(self.basis.face_value.T, self.basis.quadrature_weights * radius**2 * principal * velocity * self.gradient_q / (lapse * numerical.sqrt(spatial_f)))
        gram = numerical.zeros(self.face_count)
        if include_gram:
            node_mass, node_lapse, node_velocity = [real_linear(mapping, packed) for mapping in self.node_maps]
            coefficient, gradient, unused_hessian = coefficient_jets(node_velocity, self.gradient_node, node_mass, node_lapse, self.basis.radii, self.constants)
            factors, sampling = gram_matrices(self.node_count)
            factor_scalar = real_linear(factors, self.scalar)
            factor_velocity = real_linear(factors, node_velocity)
            factor_coefficient = real_linear(sampling, coefficient)
            links = FactorLinks(self.basis.radii)
            current = coefficient[links.node] * links.sweight * factor_scalar[links.factor] * factor_velocity[links.factor] / self.basis.spacing
            current -= node_velocity[links.node] * links.tweight * factor_coefficient[links.factor] * factor_scalar[links.factor] / self.basis.spacing
            node_f = 1 - 2 * node_mass / self.basis.radii - self.constants['Lambda'] * self.basis.radii**2 / 3
            connection = real_linear(links.first.T, current) / (node_f * node_lapse**2)
            gram = real_linear(self.basis.face_to_node.T, self.density * gradient[4] + connection)
        return numerical.linalg.solve(pairing, gram - matter), pairing, matter, gram

    def constraint_tangent(self, packed, include_gram, defect_acceleration, endpoint_acceleration, outer_clock_time):
        mass_speed, pairing, matter, gram = self.shift_mass_velocity(packed, include_gram)
        scalar_speed = packed[self.slices[2]]
        momentum_speed = self.scalar_force(packed, include_gram)
        momentum_speed[[0, -1]] = 0
        step = 1e-25
        changed = ConstraintRouthian(self.basis, self.scalar + 1j * step * scalar_speed, self.defect + 1j * step * self.defect_time, self.defect_time + 1j * step * defect_acceleration, self.constants, self.kappa, self.momentum + 1j * step * momentum_speed, self.outer_clock + 1j * step * outer_clock_time)
        data_derivative = changed.evaluate(packed, include_gram, hessian=False)[1].imag / step
        jacobian = self.evaluate(packed, include_gram)[2]
        speed = numerical.zeros_like(packed)
        speed[self.fixed] = [mass_speed[0], endpoint_acceleration[0], endpoint_acceleration[-1]]
        fixed_forcing = real_linear(jacobian, speed) + data_derivative
        speed[self.free] = numerical.linalg.solve(jacobian[numerical.ix_(self.free, self.free)], -fixed_forcing[self.free])
        derivative_residual = (real_linear(jacobian, speed) + data_derivative)[self.free]
        shift_residual = real_linear(pairing, speed[self.slices[0]]) + matter - gram
        return {'packed_speed': speed, 'shift_mass_speed': mass_speed, 'momentum_speed': momentum_speed, 'constraint_derivative_residual': derivative_residual, 'shift_residual': shift_residual, 'pairing': pairing, 'matter_shift': matter, 'Gram_shift': gram, 'data_derivative': data_derivative}

    def solve(self, seed, include_gram, scaling, maximum_steps=10, tolerance=1e-12):
        packed = seed.copy()
        scales, row_scale = scaling
        history = []
        for iteration in range(maximum_steps + 1):
            admissible, branch = self.admissible(packed, include_gram)
            if not admissible:
                return packed, history, False, {'reason': 'inadmissible_iterate', 'branch': branch}
            value, gradient, matrix = self.evaluate(packed, include_gram)
            residual = gradient[self.free]
            scaled_residual = residual / row_scale
            jacobian = matrix[numerical.ix_(self.free, self.free)]
            scaled_jacobian = jacobian * scales[None, :] / row_scale[:, None]
            singular_values = numerical.linalg.svd(scaled_jacobian, compute_uv=False)
            condition = float(singular_values[0] / singular_values[-1])
            norm = float(numerical.max(numerical.abs(scaled_residual)))
            history.append({'iteration': iteration, 'scaled_residual_max': norm, 'unscaled_residual_max': float(numerical.max(numerical.abs(residual))), 'condition_number': condition, 'scaled_smallest_singular_value': float(singular_values[-1]), 'action': float(value), 'branch': branch})
            if norm < tolerance:
                return packed, history, True, {'reason': 'all_free_equations_solved'}
            if condition > 1e13 or not numerical.isfinite(condition):
                return packed, history, False, {'reason': 'rank_or_condition_gate'}
            if iteration == maximum_steps:
                break
            scaled_step = numerical.linalg.solve(scaled_jacobian, -scaled_residual)
            linear_residual = float(numerical.max(numerical.abs(scaled_jacobian @ scaled_step + scaled_residual)))
            history[-1]['linear_solve_residual_max'] = linear_residual
            accepted = False
            for power in range(13):
                fraction = 0.5**power
                trial = packed.copy()
                trial[self.free] += fraction * scales * scaled_step
                valid, unused_branch = self.admissible(trial, include_gram)
                if not valid:
                    continue
                trial_residual = self.evaluate(trial, include_gram, hessian=False)[1][self.free] / row_scale
                trial_norm = float(numerical.max(numerical.abs(trial_residual)))
                if trial_norm < (1 - 1e-4 * fraction) * norm or trial_norm < tolerance:
                    history[-1]['accepted_fraction'] = fraction
                    history[-1]['scaled_step_max'] = float(numerical.max(numerical.abs(fraction * scaled_step)))
                    packed, accepted = trial, True
                    break
            if not accepted:
                return packed, history, False, {'reason': 'line_search_failed'}
        return packed, history, False, {'reason': 'iteration_budget_reached'}
