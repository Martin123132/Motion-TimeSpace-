import numpy as numerical
from scipy.linalg import solve

from annular_cubic_lapse_reference_gravity_20260912 import CubicContext, CubicFields, evaluate_cubic_initial, GRAVITY_REFERENCE_ROOT
from annular_cubic_lapse_reference_gravity_20260912 import CubicPreparation as ReferencePreparation


class CubicPreparation(ReferencePreparation):
    def project_mass(self, selected):
        history = []
        for unused_iteration in range(12):
            residual, jacobian = self.mass_equations(selected)
            merit = float(abs(residual).max())
            history.append(merit)
            if merit < 2e-13:
                nodes = CubicFields(self.context, selected).evaluate(self.context.basis.radii)
                selected['fixed_lapse'] = self.context.model.original_lapse * self.context.system.outer_clock * numerical.sqrt(nodes['F'][-1]) / self.context.model.original_lapse[-1]
                selected['lapse_boundary_amplitudes'] = numerical.zeros(2)
                if self.correction:
                    values = CubicFields(self.context, selected).evaluate(self.context.basis.radii)
                    radius = self.context.basis.radii
                    energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
                    required = values['N'] * (.1 * energy / radius + values['mu'] / (radius**2 * values['F']))
                    selected['lapse_boundary_amplitudes'] = (required - values['N_r'])[[0, -1]]
                return history
            update = solve(jacobian, -residual)
            accepted = False
            for power in range(16):
                trial = {key: value.copy() for key, value in selected.items()}
                trial['mass_coefficients'][1:self.face_count] += update[:self.face_count - 1] * 2.**(-power)
                trial['mass_lift_coefficients'] += update[-2:] * 2.**(-power)
                try:
                    next_merit = float(abs(self.mass_equations(trial)[0]).max())
                except ValueError:
                    continue
                if next_merit < merit:
                    selected.update(trial)
                    accepted = True
                    break
            if not accepted:
                raise RuntimeError('Nineteen-row mass preparation stalled.')
        raise RuntimeError('Nineteen-row mass preparation iteration limit.')
