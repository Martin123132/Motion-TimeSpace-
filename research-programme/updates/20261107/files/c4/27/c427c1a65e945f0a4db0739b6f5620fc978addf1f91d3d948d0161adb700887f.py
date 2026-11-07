from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'dynamical-axial-20261004'))
from axial_wave import WaveBody


def determinant(first, second):
    return first[0]*second[1]-first[1]*second[0]


def source_jumps(orbit, mass, particle_mass=1.):
    frequency = np.sqrt(mass/orbit**3)
    strength = 8*np.pi/3*particle_mass*frequency/np.sqrt(1-3*mass/orbit)*np.sqrt(15/(8*np.pi))
    metric = 1-2*mass/orbit
    return strength*orbit/2, -strength*metric/2


def tortoise(radius, mass):
    return radius+2*mass*np.log(radius/(2*mass)-1) if mass else radius


def potential(radius, mass):
    return (1-2*mass/radius)*(6/radius**2-6*mass/radius**3)


def sample_vacuum(start, finish, initial, mass, frequency, positions, tolerance):
    def equation(radius, state):
        return np.array([state[1], (potential(radius, mass)-frequency**2)*state[0]])/(1-2*mass/radius)

    solution = solve_ivp(equation, (start, finish), np.asarray(initial, dtype=complex), t_eval=positions,
                         method='DOP853', rtol=tolerance, atol=tolerance/100)
    assert solution.success, solution.message
    return solution.y.T, solution.nfev


def outgoing_samples(mass, frequency, positions, far_phase=60., order=12, tolerance=3e-12):
    positions = np.array(sorted(set(positions), reverse=True))
    assert frequency > 0 and positions[-1] > 2*mass
    outer = max(1.1*positions[0], far_phase/frequency)
    coefficients = [1+0j]
    for index in range(order):
        previous = coefficients[index-1] if index else 0
        coefficients.append(((index*(index+1)-6)*coefficients[index]
                             +2*mass*frequency*(4-index**2)*previous)/(2j*(index+1)))
    indices = np.arange(order+1)
    argument = frequency*outer
    series = np.sum(coefficients*argument**(-indices))
    derivative = np.sum(-indices*coefficients*argument**(-indices-1))
    phase = np.exp(1j*frequency*tortoise(outer, mass))
    initial = phase*np.array([series, 1j*frequency*series+(1-2*mass/outer)*frequency*derivative])
    flux = np.imag(np.conj(initial[0])*initial[1])
    samples, evaluations = sample_vacuum(outer, positions[-1], initial, mass, frequency, positions, tolerance)
    surface_value = samples[-1, 0]
    normalized = {}
    for position, state in zip(positions, samples):
        value = state[0]/surface_value
        logarithm = complex((state[1]/state[0]).real, flux/abs(state[0])**2)
        normalized[float(position)] = value*np.array([1., logarithm])
    normalized[float(positions[-1])][0] = 1.+0j
    return normalized, surface_value, {'outer': outer, 'series_order': order,
                                      'infinity_flux_normalization_error': float(abs(flux/frequency-1)),
                                      'function_evaluations': evaluations}


def horizon_samples(mass, frequency, positions, epsilon=1e-5, order=12, tolerance=3e-12):
    positions = np.array(sorted(set(positions)))
    start = 2*mass*(1+epsilon)
    assert positions[0] > start and mass > 0
    scaled_frequency = 2*mass*frequency
    coefficients = [1.+0j]
    for index in range(1, order+1):
        residual = (2*(index-1)*(index-2)+(1-6j*scaled_frequency)*(index-1)-3)*coefficients[index-1]
        if index >= 2:
            residual += ((index-2)*(index-3)-6j*scaled_frequency*(index-2)-6)*coefficients[index-2]
        if index >= 3:
            residual += -2j*scaled_frequency*(index-3)*coefficients[index-3]
        coefficients.append(-residual/(index*(index-2j*scaled_frequency)))
    indices = np.arange(order+1)
    series = np.sum(coefficients*epsilon**indices)
    derivative = np.sum(indices[1:]*coefficients[1:]*epsilon**(indices[1:]-1))
    phase = np.exp(-1j*frequency*tortoise(start, mass))
    initial = phase*np.array([series, epsilon/(1+epsilon)*derivative/(2*mass)-1j*frequency*series])
    samples, evaluations = sample_vacuum(start, positions[-1], initial, mass, frequency, positions, tolerance)
    surface_value = samples[0, 0]
    normalized = {}
    for position, state in zip(positions, samples):
        value = state[0]/surface_value
        logarithm = complex((state[1]/state[0]).real, -frequency/abs(state[0])**2)
        normalized[float(position)] = value*np.array([1., logarithm])
    normalized[float(positions[0])][0] = 1.+0j
    initial_flux = np.imag(np.conj(initial[0])*initial[1])
    return normalized, surface_value, {'epsilon': epsilon, 'order': order,
                                      'horizon_flux_normalization_error': float(abs(initial_flux/(-frequency)-1)),
                                      'function_evaluations': evaluations}


def stable_excess(inside, horizon_surface, outgoing_surface, source_outgoing, source_horizon):
    return -determinant(inside, horizon_surface)*source_outgoing/(determinant(inside, outgoing_surface)*source_horizon)


class AxialCompanion:
    def __init__(self, interior_settings, exterior_settings):
        self.body = WaveBody(.03)
        self.radius, self.mass = self.body.radius, self.body.mass
        self.interior_settings = interior_settings
        self.exterior_settings = exterior_settings
        static, _ = self.body.solve(0., variations=True, **interior_settings)
        self.static = static
        self.response = self.body.recover_static(static['Y'])
        self.sigma = -self.response/6

    def evaluate(self, separation):
        orbit = separation*self.radius
        frequency = np.sqrt(self.mass/orbit**3)
        settings = self.exterior_settings
        outgoing, out_surface, out_diagnostic = outgoing_samples(self.mass, frequency, [self.radius, orbit],
                                                                settings['far_phase'], settings['order'], settings['tolerance'])
        horizon, horizon_surface, in_diagnostic = horizon_samples(self.mass, frequency, [self.radius, orbit],
                                                                 settings['horizon_epsilon'], settings['order'], settings['tolerance'])
        jump, slope = source_jumps(orbit, self.mass)
        source_horizon = slope*horizon[orbit][0]-jump*horizon[orbit][1]
        source_outgoing = slope*outgoing[orbit][0]-jump*outgoing[orbit][1]
        reference_wronskian = determinant(horizon[self.radius], outgoing[self.radius])
        reference_out = source_horizon/reference_wronskian
        reference_in = source_outgoing/reference_wronskian
        reference_amplitude = reference_out/out_surface
        horizon_amplitude = reference_in/horizon_surface
        response, solution = self.body.solve(frequency*self.radius, **self.interior_settings)
        inside = np.array([1.+0j, response['Y']/self.radius])
        body_wronskian = determinant(inside, outgoing[self.radius])
        excess = stable_excess(inside, horizon[self.radius], outgoing[self.radius], source_outgoing, source_horizon)
        body_amplitude = reference_amplitude*(1+excess)
        body_sample, direct_evaluations = sample_vacuum(self.radius, orbit, inside, self.mass, frequency, [orbit], settings['tolerance'])
        body_at_orbit = body_sample[0]
        direct_out = (slope*body_at_orbit[0]-jump*body_at_orbit[1])/body_wronskian
        direct_amplitude = direct_out/out_surface
        body_in = source_outgoing/body_wronskian
        body_value_jump = direct_out*outgoing[orbit][0]-body_in*body_at_orbit[0]
        body_slope_jump = direct_out*outgoing[orbit][1]-body_in*body_at_orbit[1]
        reference_value_jump = reference_out*outgoing[orbit][0]-reference_in*horizon[orbit][0]
        reference_slope_jump = reference_out*outgoing[orbit][1]-reference_in*horizon[orbit][1]
        factor = 3/(4*np.pi)*frequency**2
        reference_power = factor*abs(reference_amplitude)**2
        horizon_power = factor*abs(horizon_amplitude)**2
        newton_power = 32/5*self.mass**3/orbit**5
        leading_pair_power = 8/45*self.mass**4/orbit**6
        fractional_power = 2*excess.real+abs(excess)**2
        leading_amplitude = -6*self.sigma/orbit**5
        leading_power = -12*self.sigma/orbit**5
        leading_total = -self.mass*self.sigma/(3*orbit**6)
        quadratic_boundary = self.static['Y']-self.static['I_over_R']*(frequency*self.radius)**2
        inside_quadratic = np.array([1.+0j, quadratic_boundary/self.radius])
        quadratic_excess = stable_excess(inside_quadratic, horizon[self.radius], outgoing[self.radius], source_outgoing, source_horizon)
        gap = 3*self.body.central_lapse**2
        remainder = (frequency*self.radius)**4*self.static['I_over_R']/(gap-(frequency*self.radius)**2)
        gap_margin = abs(quadratic_boundary-self.radius*outgoing[self.radius][1])-remainder
        assert gap_margin > 0
        sensitivity_bound = abs(source_outgoing/source_horizon)*abs(self.radius*(outgoing[self.radius][1]-horizon[self.radius][1]))
        sensitivity_bound *= remainder/(abs(quadratic_boundary-self.radius*outgoing[self.radius][1])*gap_margin)
        return {'separation_over_radius': separation, 'orbit': orbit, 'x': self.mass/orbit,
                'frequency': frequency, 'frequency_R': frequency*self.radius,
                'Y_body': response['Y'], 'Y_BH_real': float((self.radius*horizon[self.radius][1]).real),
                'Y_BH_imag': float((self.radius*horizon[self.radius][1]).imag),
                'amplitude_excess_real': float(excess.real), 'amplitude_excess_imag': float(excess.imag),
                'fractional_infinity_pair_power_excess': float(fractional_power),
                'reference_pair_power_infinity_per_mu_squared': float(reference_power),
                'body_pair_power_infinity_per_mu_squared': float(reference_power*(1+fractional_power)),
                'reference_pair_power_horizon_per_mu_squared': float(horizon_power),
                'reference_power_to_STF_leading': float(reference_power/leading_pair_power),
                'amplitude_real_to_leading_magnetic': float(excess.real/leading_amplitude),
                'pair_power_excess_to_leading_magnetic': float(fractional_power/leading_power),
                'infinity_increment_over_Newtonian': float(reference_power/newton_power*fractional_power),
                'leading_magnetic_increment_over_Newtonian': float(leading_total),
                'infinity_increment_to_leading_magnetic': float(reference_power/newton_power*fractional_power/leading_total),
                'reference_horizon_power_over_Newtonian': float(horizon_power/newton_power),
                'total_infinity_plus_absorption_increment_over_Newtonian': float((reference_power*fractional_power-horizon_power)/newton_power),
                'quadratic_boundary_amplitude_error': float(abs(quadratic_excess-excess)),
                'quadratic_boundary_amplitude_error_bound': float(sensitivity_bound),
                'boundary_remainder_bound': float(remainder),
                'negative_control_BH_boundary_excess': float(abs(stable_excess(horizon[self.radius], horizon[self.radius], outgoing[self.radius], source_outgoing, source_horizon))),
                'direct_to_stable_amplitude_relative_error': float(abs(direct_amplitude/body_amplitude-1)),
                'value_jump_relative_error': float(abs(body_value_jump/jump-1)),
                'slope_jump_relative_error': float(abs(body_slope_jump/slope-1)),
                'reference_value_jump_relative_error': float(abs(reference_value_jump/jump-1)),
                'reference_slope_jump_relative_error': float(abs(reference_slope_jump/slope-1)),
                'outgoing_diagnostic': out_diagnostic, 'horizon_diagnostic': in_diagnostic,
                'interior_evaluations': response['function_evaluations'], 'direct_exterior_evaluations': direct_evaluations}
