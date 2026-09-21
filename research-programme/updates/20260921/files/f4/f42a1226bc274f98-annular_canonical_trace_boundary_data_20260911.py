import numpy as numerical
from scipy.linalg import solve

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_reference_fields_20260911 import SavedCanonicalFields
from annular_canonical_rate_completion_20260911 import evaluate_initial
from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension
from annular_gram_joint_action_20260909 import gram_matrices


class BoundaryPreparation:
    def __init__(self, context):
        if context.branch != 'metric_Gram':
            raise ValueError('This constructor prepares the retained MTS state; GR uses its separate formula reference.')
        self.context = context
        basis = context.basis
        self.face_count = basis.faces.size
        fraction = (basis.radii - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])
        value = numerical.column_stack([1 - 3 * fraction**2 + 2 * fraction**3, 3 * fraction**2 - 2 * fraction**3])
        derivative = numerical.column_stack([-6 * fraction + 6 * fraction**2, 6 * fraction - 6 * fraction**2]) / (basis.radii[-1] - basis.radii[0])
        self.pi_lifts = numerical.concatenate([value, basis.spacing * (derivative - basis.derivative @ value)])
        self.face, self.face_r = linear_value_gradient(basis.faces, context.points)
        self.face_nodes = linear_value_gradient(basis.faces, basis.radii)[0]
        self.eta = linear_value_gradient(basis.radii, context.points)[0]
        factors, sampling = gram_matrices(basis.radii.size)
        self.gram_density = sampling.T @ (factors @ context.saved['configuration'][:basis.radii.size])**2 / (2 * basis.spacing)
        self.calls = 0

    def candidate(self, amplitudes):
        selected = {key: value.copy() for key, value in self.context.saved.items()}
        selected['pi_coefficients'] += self.pi_lifts @ amplitudes
        return selected

    def mass_equations(self, selected):
        context = self.context
        physical = SavedCanonicalFields(context.model, selected)
        values = physical.evaluate(context.points)
        nodes = physical.evaluate(context.basis.radii)
        radius, weights, geometry = context.points, context.weights, values['F']
        if numerical.real(geometry).min() <= .1 or numerical.real(nodes['F']).min() <= .1:
            raise ValueError('Trial leaves the positive annular chart.')
        energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
        constraint = self.eta.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy))
        constraint -= context.basis.radii**2 * numerical.sqrt(nodes['F']) * self.gram_density
        coefficient = values['mu_r'] / (.1 * radius * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
        derivative = self.eta.T @ (weights[:, None] * (self.face_r[:, 1:] / (.1 * numerical.sqrt(geometry))[:, None] + coefficient[:, None] * self.face[:, 1:]))
        derivative += (context.basis.radii * self.gram_density / numerical.sqrt(nodes['F']))[:, None] * self.face_nodes[:, 1:]
        return constraint, derivative

    def project_mass(self, selected):
        history = []
        for unused_iteration in range(12):
            residual, derivative = self.mass_equations(selected)
            merit = float(abs(residual).max())
            history.append(merit)
            if merit < 2e-14:
                geometry_outer = 1 - 2 * (self.face_nodes[-1] @ selected['mass_coefficients'][:self.face_count]) / self.context.basis.radii[-1]
                selected['fixed_lapse'] = self.context.model.original_lapse * self.context.system.outer_clock * numerical.sqrt(geometry_outer) / self.context.model.original_lapse[-1]
                return history
            update = solve(derivative, -residual)
            accepted = False
            for power in range(16):
                trial = {key: value.copy() for key, value in selected.items()}
                trial['mass_coefficients'][1:self.face_count] += update * 2.**(-power)
                try:
                    trial_merit = float(abs(self.mass_equations(trial)[0]).max())
                except ValueError:
                    continue
                if trial_merit < merit:
                    selected.update(trial)
                    accepted = True
                    break
            if not accepted:
                raise RuntimeError('Boundary-data mass projection stalled.')
        raise RuntimeError('Boundary-data mass iteration limit.')

    def evaluate(self, amplitudes):
        self.calls += 1
        selected = self.candidate(amplitudes)
        history = self.project_mass(selected)
        data, frames, completion = self.context.build(selected)
        baseline = evaluate_initial(frames['mass'], frames['scalar'], data, self.context.basis, self.context.weights, self.context.links, True, self.context.system.outer_clock)
        family, unused_primitive, unused_carrier = kernel_family(self.context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, diagnostics = trace_extension(self.context, frames['mass'], family)
        actual = evaluate_initial(extended, frames['scalar'], data, self.context.basis, self.context.weights, self.context.links, True, self.context.system.outer_clock)
        nodes = data['nodes']
        parent_inner = .1 * nodes['N'][0] * nodes['F'][0]**1.5 * nodes['pi'][0] * nodes['w'][0]
        parent_inner += .1 * numerical.sqrt(nodes['F'][0]) * actual['q_nodes'][0] * actual['gram_scalar'][0] / nodes['N'][0]
        bulk_coefficient = .1 * nodes['R'][0]**2 * nodes['F'][0] * nodes['w'][0]
        residual = numerical.array([(parent_inner - selected['boundary_velocity'][0]) / bulk_coefficient, actual['q_nodes'][-1] - selected['boundary_velocity'][2]])
        selected['state'][:self.context.basis.radii.size] = selected['mass_coefficients'][1:self.face_count]
        selected['state'][self.context.basis.radii.size:2 * self.context.basis.radii.size] = selected['pi_coefficients'][:self.context.basis.radii.size]
        selected['state'][-3:] = actual['reactions']
        return {'residual': residual, 'saved': selected, 'data': data, 'frames': {'mass': extended, 'scalar': frames['scalar']}, 'baseline': baseline, 'actual': actual, 'mass_history': history, 'completion': completion, 'extension': diagnostics, 'parent_inner_mass_rate': float(parent_inner)}

    def solve(self, maximum_iterations=6):
        amplitudes = numerical.zeros(2)
        history = []
        result = self.evaluate(amplitudes)
        for iteration in range(maximum_iterations + 1):
            residual = result['residual']
            history.append({'iteration': iteration, 'amplitudes': amplitudes.tolist(), 'boundary_residual': residual.tolist(), 'mass_history': result['mass_history']})
            if abs(residual).max() < 2e-12:
                return amplitudes, result, history
            if iteration == maximum_iterations:
                raise RuntimeError('Two-amplitude boundary preparation failed to converge.')
            step = 1e-7
            jacobian = numerical.column_stack([(self.evaluate(amplitudes + step * direction)['residual'] - self.evaluate(amplitudes - step * direction)['residual']) / (2 * step) for direction in numerical.eye(2)])
            history[-1]['boundary_jacobian'] = jacobian.tolist()
            history[-1]['boundary_jacobian_condition'] = float(numerical.linalg.cond(jacobian))
            update = solve(jacobian, -residual)
            accepted = False
            for power in range(12):
                candidate = amplitudes + update * 2.**(-power)
                trial = self.evaluate(candidate)
                if abs(trial['residual']).max() < abs(residual).max():
                    amplitudes, result, accepted = candidate, trial, True
                    break
            if not accepted:
                raise RuntimeError('Two-amplitude boundary line search failed.')
        raise RuntimeError('Unreachable boundary state.')
