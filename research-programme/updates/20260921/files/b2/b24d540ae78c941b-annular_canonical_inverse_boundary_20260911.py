import numpy as numerical

from annular_canonical_nodal_data_20260911 import CanonicalInitialNodalData
from annular_canonical_mass_reduction_20260911 import MassConstraintReduction


class InverseBoundaryInitialData(CanonicalInitialNodalData):
    def __init__(self, *arguments, normalize_clock, **keywords):
        super().__init__(*arguments, **keywords)
        self.normalize_clock = normalize_clock
        self.original_lapse = self.fixed_lapse.copy()
        self.data_count = 2 * self.count + 3
        self.inner_gradient = self.basis.derivative[0] @ self.configuration[:self.count] + self.configuration[self.count] / self.basis.spacing
        inner_f = 1 - 2 * self.mass_coeff_seed[0] / self.basis.radii[0]
        self.bulk_trace_coefficient = .1 * self.basis.radii[0]**2 * inner_f * self.inner_gradient
        if abs(self.bulk_trace_coefficient) < 1e-12:
            raise ValueError('This inverse boundary chart requires a nonzero original scalar gradient.')
        if self.include_gram:
            selected = self.links.node == 0
            if not numerical.all(self.links.sweight[selected] == 0):
                raise ValueError('Endpoint current identity requires zero inner sampling weights.')

    def set_state(self, data):
        result = super().set_state(data)
        if self.normalize_clock:
            self.fixed_lapse = self.original_lapse * self.system.outer_clock * numerical.sqrt(self.node_f[-1]) / self.original_lapse[-1]
        else:
            self.fixed_lapse = self.original_lapse.copy()
        return result

    def trace_terms(self, evaluation):
        scalar_force = evaluation['sources']['scalar_force'][0] if self.include_gram else 0.
        correction = .1 * numerical.sqrt(self.node_f[0]) * scalar_force / self.fixed_lapse[0]
        coefficient = self.bulk_trace_coefficient + correction
        velocity = evaluation['scalar_velocity'][0]
        return {'coefficient': coefficient, 'Gram_coefficient': correction, 'predicted_flux': coefficient * velocity, 'Gram_P_trace': -correction * velocity}

    def data_residual(self, data):
        unused_mass, unused_pi, reactions = self.set_state(data)
        if min(numerical.real(array).min() for array in [self.spatial_f, self.node_f, self.link_f]) <= .1:
            raise ValueError('Initial geometry left the positive chart.')
        evaluation = self.evaluate(numerical.concatenate([self.fixed_lapse, reactions]))
        trace = self.trace_terms(evaluation)
        boundary = numerical.array([
            evaluation['mass_rate'][0] - self.boundary_velocity[0],
            (trace['predicted_flux'] - self.boundary_velocity[0]) / self.bulk_trace_coefficient,
            evaluation['scalar_velocity'][self.count - 1] - self.boundary_velocity[2],
        ])
        return numerical.concatenate([self.constraint(), evaluation['constraint_rate'], boundary])

    def diagnostics(self, state):
        unused_mass, pi_coefficients, reactions = self.set_state(state)
        evaluation = self.evaluate(numerical.concatenate([self.fixed_lapse, reactions]))
        trace = self.trace_terms(evaluation)
        radii = self.basis.radii[[0, -1]]
        original_mass = self.packed[self.system.slices[0]][[0, -1]]
        seed_f = 1 - 2 * original_mass / radii
        pi_endpoint = radii**2 * pi_coefficients[[0, self.count - 1]] / (self.lapse_seed[[0, -1]] * numerical.sqrt(seed_f))
        local_q = self.fixed_lapse[[0, -1]] * numerical.sqrt(self.node_f[[0, -1]]) * pi_endpoint / radii**2
        weak_q = evaluation['scalar_velocity'][[0, self.count - 1]]
        endpoint_gradient = numerical.array([self.inner_gradient, self.basis.derivative[-1] @ self.configuration[:self.count] + self.configuration[-1] / self.basis.spacing])
        scalar_flux = radii**2 * self.fixed_lapse[[0, -1]] * numerical.sqrt(self.node_f[[0, -1]]) * endpoint_gradient
        gram_force = evaluation['sources']['scalar_force'][[0, self.count - 1]] if self.include_gram else numerical.zeros(2)
        reaction_expected = numerical.array([
            self.fixed_lapse[0] / (.1 * numerical.sqrt(self.node_f[0])),
            -scalar_flux[0] - gram_force[0],
            scalar_flux[1] - gram_force[1],
        ])
        local_ep_flux = self.bulk_trace_coefficient * local_q[0] - trace['Gram_P_trace']
        return evaluation, {
            'inner_scalar_velocity': float(weak_q[0]),
            'old_inner_scalar_velocity': float(self.boundary_velocity[1]),
            'inner_scalar_velocity_change': float(weak_q[0] - self.boundary_velocity[1]),
            'inner_mass_drive': float(self.boundary_velocity[0]),
            'inner_trace_coefficient': float(trace['coefficient']),
            'Gram_P_trace': float(trace['Gram_P_trace']),
            'combined_trace_gap': float(evaluation['mass_rate'][0] - trace['predicted_flux']),
            'local_EP_trace_gap': float(evaluation['mass_rate'][0] - local_ep_flux),
            'endpoint_Legendre_gaps': (weak_q - local_q).tolist(),
            'outer_clock_gap': float(self.fixed_lapse[-1] / numerical.sqrt(self.node_f[-1]) - self.system.outer_clock),
            'lapse_normalization': float(self.fixed_lapse[-1] / self.original_lapse[-1]),
            'spatial_boundary_reaction_gaps': (reactions - reaction_expected).tolist(),
            'spatial_boundary_reactions_expected': reaction_expected.tolist(),
            'minimum_F': float(min(self.spatial_f.min(), self.node_f.min(), self.link_f.min())),
            'minimum_lapse': float(self.fixed_lapse.min()),
        }


class InverseBoundaryMassReduction(MassConstraintReduction):
    def __init__(self, model, mass_tolerance=2e-14):
        if type(model) is not InverseBoundaryInitialData:
            raise TypeError('Only the declared inverse-boundary initializer is covered.')
        if model.face_count != model.count + 1 or model.system.kappa != .1:
            raise ValueError('Unexpected canonical mass/phase dimensions or coupling.')
        self.model = model
        self.mass_count = model.count
        self.mass_tolerance = mass_tolerance
