from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'axial-companion-20261005'))
from axial_binary import WaveBody, determinant, source_jumps, outgoing_samples, horizon_samples, sample_vacuum


def reciprocal_action(inside, horizon, outgoing, overlap):
    difference = -determinant(inside, horizon)*overlap/(determinant(inside, outgoing)*determinant(horizon, outgoing))
    return -3/(8*np.pi)*difference*overlap, difference


class ActionProblem:
    def __init__(self, interior_settings, exterior_settings):
        self.body = WaveBody(.03)
        self.radius, self.mass = self.body.radius, self.body.mass
        self.interior_settings, self.exterior_settings = interior_settings, exterior_settings
        static, _ = self.body.solve(0., **interior_settings)
        self.sigma = -self.body.recover_static(static['Y'])/6

    def evaluate(self, separation):
        orbit = separation*self.radius
        frequency = np.sqrt(self.mass/orbit**3)
        settings = self.exterior_settings
        outgoing, outgoing_surface, outgoing_diagnostic = outgoing_samples(self.mass, frequency, [self.radius, orbit],
                                                                           settings['far_phase'], settings['order'], settings['tolerance'])
        horizon, horizon_surface, horizon_diagnostic = horizon_samples(self.mass, frequency, [self.radius, orbit],
                                                                       settings['horizon_epsilon'], settings['order'], settings['tolerance'])
        response, _ = self.body.solve(frequency*self.radius, **self.interior_settings)
        inside = np.array([1.+0j, response['Y']/self.radius])
        boundary_body = inside[1].real
        original_horizon = horizon[self.radius][1]
        original_outgoing = outgoing[self.radius][1]
        boundary_horizon = complex(original_horizon.real, -frequency/abs(horizon_surface)**2)
        boundary_outgoing = complex(original_outgoing.real, frequency/abs(outgoing_surface)**2)
        horizon_boundary = np.array([1.+0j, boundary_horizon])
        outgoing_boundary = np.array([1.+0j, boundary_outgoing])
        quadrature_solution, quadrature_evaluations = sample_vacuum(self.radius, orbit, [0., 1.], self.mass, frequency, [orbit], settings['tolerance'])
        quadrature = quadrature_solution[0].real
        real_outgoing = outgoing[orbit].real
        stable_outgoing = real_outgoing+1j*boundary_outgoing.imag*quadrature
        stable_horizon = real_outgoing+(boundary_horizon.real-boundary_outgoing.real)*quadrature+1j*boundary_horizon.imag*quadrature
        jump, jump_slope = source_jumps(orbit, self.mass)
        overlap_outgoing = jump_slope*stable_outgoing[0]-jump*stable_outgoing[1]
        overlap_horizon = jump_slope*stable_horizon[0]-jump*stable_horizon[1]
        wronskian_body = determinant(inside, outgoing_boundary)
        wronskian_horizon = determinant(horizon_boundary, outgoing_boundary)
        boundary_difference = determinant(inside, horizon_boundary)
        retarded, delta_coefficient = reciprocal_action(inside, horizon_boundary, outgoing_boundary, overlap_outgoing)
        control_action, control_coefficient = reciprocal_action(horizon_boundary, horizon_boundary, outgoing_boundary, overlap_outgoing)
        difference = delta_coefficient*stable_outgoing
        metric = 1-2*self.mass/orbit
        helical_pair = 2*frequency*np.sqrt(15/(8*np.pi))*(metric*difference[0]+orbit*difference[1])
        ut = 1/np.sqrt(1-3*self.mass/orbit)
        metric_action = ut*helical_pair/4
        reference_coefficient = overlap_horizon/wronskian_horizon
        excess = delta_coefficient/reference_coefficient
        reference_amplitude = reference_coefficient/outgoing_surface
        inward_amplitude = overlap_outgoing/wronskian_horizon/horizon_surface
        power_factor = 3*frequency**2/(4*np.pi)
        reference_infinity_power = power_factor*abs(reference_amplitude)**2
        infinity_difference = reference_infinity_power*(2*excess.real+abs(excess)**2)
        horizon_power = power_factor*abs(inward_amplitude)**2
        net_power = infinity_difference-horizon_power
        optical_power = 2*frequency*retarded.imag
        old_overlap = jump_slope*outgoing[orbit][0]-jump*outgoing[orbit][1]
        old_retarded = 3/(8*np.pi)*boundary_difference*old_overlap**2/(wronskian_body*wronskian_horizon)
        old_optical_power = 2*frequency*old_retarded.imag
        leading = 6*self.sigma*frequency**2/orbit**4
        parameter = self.mass/orbit
        static_prediction = leading*(1+16/3*parameter)
        identity_scale = abs(infinity_difference)+horizon_power
        redshift = -ut*helical_pair.real/2
        normalized_outgoing_current = np.imag(np.conj(stable_outgoing[0])*stable_outgoing[1])
        return {'separation_over_radius': float(separation), 'orbit': float(orbit), 'Omega': float(frequency), 'x': float(parameter),
                'body_Y': response['Y'], 'action_real_per_mu_squared': float(retarded.real), 'action_imag_per_mu_squared': float(retarded.imag),
                'leading_action_per_mu_squared': float(leading), 'action_over_leading': float(retarded.real/leading),
                'first_PN_action_ratio': float(1+16/3*parameter),
                'first_PN_action_relative_error': float(abs(retarded.real/static_prediction-1)),
                'inferred_first_PN_action_coefficient': float((retarded.real/leading-1)/parameter),
                'metric_overlap_relative_error': float(abs(metric_action/retarded-1)),
                'redshift_per_mu': float(redshift), 'mass_first_law_relative_error': float(abs(redshift/(-2*retarded.real)-1)),
                'infinity_power_difference_per_mu_squared': float(infinity_difference),
                'reference_horizon_power_per_mu_squared': float(horizon_power),
                'net_loss_difference_per_mu_squared': float(net_power),
                'optical_power_from_action_per_mu_squared': float(optical_power),
                'optical_identity_error_over_component_sum': float(abs(optical_power-net_power)/identity_scale),
                'old_phase_optical_error_over_component_sum': float(abs(old_optical_power-net_power)/identity_scale),
                'phase_repair_real_action_relative_change': float(abs(old_retarded.real/retarded.real-1)),
                'outgoing_quadrature_Wronskian_error': float(abs(determinant(real_outgoing, quadrature)-1)),
                'outgoing_current_relative_error': float(abs(normalized_outgoing_current/boundary_outgoing.imag-1)),
                'horizon_reconstruction_relative_error': float(np.linalg.norm(stable_horizon-horizon[orbit])/np.linalg.norm(horizon[orbit])),
                'outgoing_phase_reconstruction_absolute_change': float(np.max(np.abs(stable_outgoing-outgoing[orbit]))),
                'original_outgoing_surface_current_relative_error': float(abs(original_outgoing.imag/boundary_outgoing.imag-1)),
                'original_horizon_surface_current_relative_error': float(abs(original_horizon.imag/boundary_horizon.imag-1)),
                'BH_boundary_control_action': float(abs(control_action)),
                'BH_boundary_control_coefficient': float(abs(control_coefficient)),
                'source_phase_method': 'Exact signed asymptotic currents set normalized surface slopes; real inward solution plus outward Dirichlet fundamental solution propagates the phase',
                'interior_function_evaluations': response['function_evaluations'],
                'quadrature_function_evaluations': quadrature_evaluations,
                'outgoing_diagnostic': outgoing_diagnostic, 'horizon_diagnostic': horizon_diagnostic,
                'surface_data': {'body_slope': float(boundary_body), 'outgoing_slope_real': float(boundary_outgoing.real),
                                 'outgoing_slope_imag': float(boundary_outgoing.imag), 'horizon_slope_real': float(boundary_horizon.real),
                                 'horizon_slope_imag': float(boundary_horizon.imag)},
                'source_data': {'J': float(jump), 'K': float(jump_slope),
                                'real_outgoing_value': float(real_outgoing[0]), 'real_outgoing_slope': float(real_outgoing[1]),
                                'dirichlet_value': float(quadrature[0]), 'dirichlet_slope': float(quadrature[1])}}
