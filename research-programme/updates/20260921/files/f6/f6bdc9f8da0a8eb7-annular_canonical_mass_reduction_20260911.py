import numpy as numerical
from scipy.linalg import solve

from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData


class MassConstraintReduction:
    def __init__(self, model, mass_tolerance=2e-14):
        if type(model) is not CanonicalInitialNodalData:
            raise TypeError('Only the fixed released-correction initializer is covered.')
        if model.face_count != model.count + 1 or model.system.kappa != .1:
            raise ValueError('Unexpected canonical mass/phase dimensions or coupling.')
        self.model = model
        self.mass_count = model.count
        self.mass_tolerance = mass_tolerance

    def constraint_value(self, state):
        model = self.model
        model.set_state(state)
        face_f = 1 - 2 * model.mass / model.basis.faces
        minimum = min(numerical.real(array).min() for array in [model.spatial_f, model.node_f, model.link_f, face_f])
        if minimum <= .1:
            raise ValueError('Mass projection left the positive metric chart.')
        residual = model.constraint()
        if not numerical.all(numerical.isfinite(residual)):
            raise ValueError('Nonfinite mass constraint.')
        return residual

    def constraint_blocks(self, state):
        self.constraint_value(state)
        model = self.model
        radius, weights, spatial_f = model.radius, model.weights, model.spatial_f
        energy = model.pi**2 / (2 * radius**2) + radius**2 * model.scalar_gradient**2 / 2
        local_mass = model.mass_r / (.1 * radius * spatial_f**1.5) + energy / (radius * numerical.sqrt(spatial_f))
        mass_basis = model.basis.face_value[:, 1:]
        gradient_basis = model.basis.face_gradient[:, 1:]
        node_basis = model.basis.node_value
        mass_block = node_basis.T @ (weights[:, None] * (gradient_basis / (.1 * numerical.sqrt(spatial_f))[:, None] + local_mass[:, None] * mass_basis))
        if model.include_gram:
            mass_block += (model.basis.radii * model.gram_density / numerical.sqrt(model.node_f))[:, None] * model.basis.face_to_node[:, 1:]
        momentum_block = -(node_basis.T @ ((weights * numerical.sqrt(spatial_f) * model.pi / radius**2)[:, None] * model.pi_map[:, :model.count]))
        other_block = numerical.concatenate([momentum_block, numerical.zeros((model.count, 3))], axis=1)
        return mass_block, other_block

    def project(self, initial_state, maximum_iterations=15):
        state = initial_state.copy()
        history = []
        for iteration in range(maximum_iterations + 1):
            residual = self.constraint_value(state)
            merit = float(abs(residual).max())
            history.append(merit)
            if merit <= self.mass_tolerance:
                return state, history
            if iteration == maximum_iterations:
                raise RuntimeError('Inner mass-constraint iteration limit.')
            mass_block, unused_other = self.constraint_blocks(state)
            correction = solve(mass_block, -residual)
            accepted = False
            for power in range(22):
                trial = state.copy()
                trial[:self.mass_count] += correction * 2.**(-power)
                try:
                    candidate = float(abs(self.constraint_value(trial)).max())
                except ValueError:
                    continue
                if candidate < merit or candidate <= self.mass_tolerance:
                    state, accepted = trial, True
                    break
            if not accepted:
                self.model.set_state(state)
                raise RuntimeError('Inner mass-constraint line search failed.')
        raise RuntimeError('Unreachable inner solver state.')

    def reduced_jacobian(self, state):
        mass_block, other_block = self.constraint_blocks(state)
        response = -solve(mass_block, other_block)
        tangent = numerical.concatenate([response, numerical.eye(other_block.shape[1])], axis=0)
        reduced = numerical.empty((other_block.shape[1], other_block.shape[1]))
        try:
            for column in range(other_block.shape[1]):
                changed = state.astype(complex) + 1e-25j * tangent[:, column]
                reduced[:, column] = self.model.data_residual(changed)[self.mass_count:].imag / 1e-25
        finally:
            self.model.set_state(state)
        return reduced, tangent, mass_block

    def solve(self, initial_state, row_scales, callback=None, maximum_iterations=35):
        if row_scales.shape != initial_state.shape or numerical.any(row_scales <= 0) or not numerical.all(numerical.isfinite(row_scales)):
            raise ValueError('Positive inherited full row scales are required.')
        state = initial_state.copy()
        history = []
        failure = None
        converged = False
        last_tangent = None
        last_reduced = None
        projected_steps = 0
        try:
            state, initial_projection = self.project(state)
            projected_steps += len(initial_projection) - 1
            for iteration in range(maximum_iterations + 1):
                residual = self.model.data_residual(state)
                if not numerical.all(numerical.isfinite(residual)):
                    raise ValueError('Nonfinite reduced residual.')
                merit = float(abs(residual[self.mass_count:] / row_scales[self.mass_count:]).max())
                history.append({'iteration': iteration, 'mass_residual': float(abs(residual[:self.mass_count]).max()), 'reduced_scaled_residual': merit, 'full_scaled_residual': float(abs(residual / row_scales).max()), 'absolute_residual': float(abs(residual).max()), 'accepted_mass_Newton_updates': projected_steps})
                if callback:
                    callback(history, state)
                if history[-1]['full_scaled_residual'] < 1e-10 and history[-1]['absolute_residual'] < 1e-9:
                    converged = True
                    break
                if iteration == maximum_iterations:
                    raise RuntimeError('Reduced Newton iteration limit.')
                reduced, tangent, mass_block = self.reduced_jacobian(state)
                last_reduced, last_tangent = reduced, tangent
                history[-1]['mass_block_condition'] = float(numerical.linalg.cond(mass_block))
                scaled_jacobian = reduced / row_scales[self.mass_count:, None]
                history[-1]['reduced_condition'] = float(numerical.linalg.cond(scaled_jacobian))
                correction = solve(scaled_jacobian, -residual[self.mass_count:] / row_scales[self.mass_count:])
                full_correction = tangent @ correction
                accepted = False
                rejection_causes = []
                for power in range(22):
                    trial = state + full_correction * 2.**(-power)
                    try:
                        projected, inner_history = self.project(trial)
                        trial_residual = self.model.data_residual(projected)
                        trial_merit = float(abs(trial_residual[self.mass_count:] / row_scales[self.mass_count:]).max())
                    except (ValueError, RuntimeError) as error:
                        rejection_causes.append(repr(error))
                        continue
                    if numerical.isfinite(trial_merit) and trial_merit < merit:
                        projected_steps += len(inner_history) - 1
                        state, accepted = projected, True
                        history[-1]['step_fraction'] = 2.**(-power)
                        history[-1]['trial_projection_updates'] = len(inner_history) - 1
                        break
                history[-1]['chart_or_inner_solver_rejections'] = rejection_causes
                if not accepted:
                    raise RuntimeError('Reduced positive-chart line search failed.')
        except (ValueError, RuntimeError, numerical.linalg.LinAlgError) as error:
            failure = repr(error)
        self.model.set_state(state)
        return {'state': state, 'history': history, 'converged': converged, 'failure': failure, 'last_reduced_jacobian': last_reduced, 'last_tangent': last_tangent, 'accepted_mass_Newton_updates': projected_steps}
