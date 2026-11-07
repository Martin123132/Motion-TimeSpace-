from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'retarded-response-20261004'
sys.path.insert(0, str(PARENT))
from response_system_v2 import asymptotic_coefficients, potential, determinant, static_master_basis, propagate
from response_system_v3 import ResponseProblem, encode


def source_jumps(orbit, mass, particle_mass=1.):
    angular_value = np.sqrt(15/(32*np.pi))
    common = 4*np.pi*angular_value*particle_mass/(3*np.sqrt(1-3*mass/orbit))
    jump_value = common*2*(orbit-2*mass)/(2*orbit+3*mass)
    jump_slope = -common*(12*orbit**3-16*orbit**2*mass-24*orbit*mass**2-33*mass**3)/(orbit**2*(2*orbit+3*mass)**2)
    return jump_value, jump_slope


def tortoise(radius, mass):
    return radius+2*mass*np.log(radius/(2*mass)-1)


def sample_vacuum(start, finish, initial, mass, sigma, positions, tolerance):
    def equation(radius, state):
        return np.array([state[1], (potential(radius, mass)-sigma**2)*state[0]])/(1-2*mass/radius)

    solution = solve_ivp(equation, (start, finish), np.asarray(initial, dtype=complex), t_eval=positions,
                         method='DOP853', rtol=tolerance, atol=tolerance/100)
    assert solution.success, solution.message
    return solution.y.T


def outgoing_samples(mass, sigma, positions, far_phase=40., order=10, tolerance=2e-12):
    positions = np.array(sorted(set(positions), reverse=True))
    assert sigma > 0 and positions[-1] > 2*mass
    outer = max(1.1*positions[0], far_phase/sigma)
    coefficients = asymptotic_coefficients(mass*sigma, order)
    indices = np.arange(order+1)
    argument = sigma*outer
    series = np.sum(coefficients*argument**(-indices))
    derivative = np.sum(-indices*coefficients*argument**(-indices-1))
    phase = np.exp(1j*sigma*tortoise(outer, mass))
    initial = phase*np.array([series, 1j*sigma*series+(1-2*mass/outer)*sigma*derivative])
    initial_flux = np.imag(np.conj(initial[0])*initial[1])
    samples = sample_vacuum(outer, positions[-1], initial, mass, sigma, positions, tolerance)
    surface_value = samples[-1, 0]
    normalized = {}
    for position, state in zip(positions, samples):
        value = state[0]/surface_value
        logarithm = complex((state[1]/state[0]).real, initial_flux/abs(state[0])**2)
        normalized[float(position)] = value*np.array([1., logarithm])
    normalized[float(positions[-1])][0] = 1.+0j
    return normalized, surface_value, {'outer': outer, 'series_order': order,
                                        'infinity_flux_normalization_error': abs(initial_flux/sigma-1)}


def horizon_coefficients(mass, sigma, order):
    scaled_frequency = 2*mass*sigma
    second = [0, 49, 154, 177, 88, 16]
    first = np.array([49, 105, 72, 16, 0, 0], dtype=complex)-2j*scaled_frequency*np.array([49, 203, 331, 265, 104, 16])
    zeroth = [-189, -420, -336, -96]

    def coefficient(polynomial, index):
        return polynomial[index] if 0 <= index < len(polynomial) else 0.

    coefficients = [1.+0j]
    for level in range(order):
        known = 0j
        for index, value in enumerate(coefficients):
            known += value*(index*(index-1)*coefficient(second, level-index+2)
                            +index*coefficient(first, level-index+1)+coefficient(zeroth, level-index))
        coefficients.append(-known/(49*(level+1)*(level+1-2j*scaled_frequency)))
    return np.array(coefficients)


def horizon_samples(mass, sigma, positions, epsilon=1e-5, order=6, tolerance=2e-12):
    positions = np.array(sorted(set(positions)))
    start = 2*mass*(1+epsilon)
    assert positions[0] > start
    coefficients = horizon_coefficients(mass, sigma, order)
    indices = np.arange(order+1)
    series = np.sum(coefficients*epsilon**indices)
    derivative = np.sum(indices[1:]*coefficients[1:]*epsilon**(indices[1:]-1))
    phase = np.exp(-1j*sigma*tortoise(start, mass))
    initial = phase*np.array([series, (epsilon/(1+epsilon)*derivative-2j*mass*sigma*series)/(2*mass)])
    samples = sample_vacuum(start, positions[-1], initial, mass, sigma, positions, tolerance)
    surface_value = samples[0, 0]
    normalized = {}
    for position, state in zip(positions, samples):
        value = state[0]/surface_value
        logarithm = complex((state[1]/state[0]).real, -sigma/abs(state[0])**2)
        normalized[float(position)] = value*np.array([1., logarithm])
    normalized[float(positions[0])][0] = 1.+0j
    initial_flux = np.imag(np.conj(initial[0])*initial[1])
    return normalized, surface_value, {'epsilon': epsilon, 'order': order,
                                      'horizon_flux_normalization_error': abs(initial_flux/(-sigma)-1) if sigma else 0.}


def reference_wave(orbit, mass, match_radius=None, far_phase=40., outer_order=10, horizon_epsilon=1e-5, horizon_order=6, tolerance=2e-12):
    if match_radius is None:
        match_radius = min(3*mass, orbit/2)
    assert 2*mass < match_radius < orbit
    sigma = 2*np.sqrt(mass/orbit**3)
    outgoing, outgoing_at_match, out_diagnostic = outgoing_samples(mass, sigma, [match_radius, orbit], far_phase, outer_order, tolerance)
    horizon, horizon_at_match, in_diagnostic = horizon_samples(mass, sigma, [match_radius, orbit], horizon_epsilon, horizon_order, tolerance)
    jump_value, jump_slope = source_jumps(orbit, mass)
    wronskian = determinant(horizon[match_radius], outgoing[match_radius])
    coefficient = (jump_slope*horizon[orbit][0]-jump_value*horizon[orbit][1])/wronskian
    inward = (jump_slope*outgoing[orbit][0]-jump_value*outgoing[orbit][1])/wronskian
    infinity_amplitude = coefficient/outgoing_at_match
    horizon_amplitude = inward/horizon_at_match
    power_factor = 3/(4*np.pi)*sigma**2
    return {'sigma': sigma, 'amplitude_infinity': infinity_amplitude, 'amplitude_horizon': horizon_amplitude,
            'pair_power_infinity_per_geometric_particle_mass_squared': power_factor*abs(infinity_amplitude)**2,
            'pair_power_horizon_per_geometric_particle_mass_squared': power_factor*abs(horizon_amplitude)**2,
            'jump_value_error': abs(coefficient*outgoing[orbit][0]-inward*horizon[orbit][0]-jump_value)/(1+abs(jump_value)),
            'jump_slope_error': abs(coefficient*outgoing[orbit][1]-inward*horizon[orbit][1]-jump_slope)/(1+abs(jump_slope)),
            'outgoing': outgoing, 'horizon': horizon, 'wronskian': wronskian,
            'outgoing_at_match': outgoing_at_match, 'diagnostics': [out_diagnostic, in_diagnostic]}


class CompanionProblem:
    def __init__(self, distance=.02, interior_tolerance=2e-8, far_phase=40., outer_order=10, horizon_epsilon=1e-5, horizon_order=6, tolerance=2e-12):
        self.interior = ResponseProblem(distance, interior_tolerance)
        self.radius, self.mass = self.interior.radius, self.interior.mass
        self.far_phase, self.outer_order = far_phase, outer_order
        self.horizon_epsilon, self.horizon_order, self.tolerance = horizon_epsilon, horizon_order, tolerance

    def evaluate(self, separation):
        orbit = separation*self.radius
        reference = reference_wave(orbit, self.mass, self.radius, self.far_phase, self.outer_order,
                                   self.horizon_epsilon, self.horizon_order, self.tolerance)
        sigma = reference['sigma']
        inside, solution, problem = self.interior.interior(sigma)
        inside /= inside[0]
        outgoing = reference['outgoing']
        horizon = reference['horizon']
        jump_value, jump_slope = source_jumps(orbit, self.mass)
        body_wronskian = determinant(inside, outgoing[self.radius])
        inner_difference = determinant(inside, horizon[self.radius])
        source_outgoing = jump_slope*outgoing[orbit][0]-jump_value*outgoing[orbit][1]
        source_horizon = jump_slope*horizon[orbit][0]-jump_value*horizon[orbit][1]
        amplitude_excess = -inner_difference*source_outgoing/(body_wronskian*source_horizon)
        body_at_orbit = propagate(self.radius, orbit, self.mass, sigma, inside)
        body_coefficient = (jump_slope*body_at_orbit[0]-jump_value*body_at_orbit[1])/body_wronskian
        direct_amplitude = body_coefficient/reference['outgoing_at_match']
        exact_amplitude = reference['amplitude_infinity']*(1+amplitude_excess)
        body_inward = source_outgoing/body_wronskian
        value_jump = body_coefficient*outgoing[orbit][0]-body_inward*body_at_orbit[0]
        slope_jump = body_coefficient*outgoing[orbit][1]-body_inward*body_at_orbit[1]
        flux_excess = 2*amplitude_excess.real+abs(amplitude_excess)**2
        row = {'separation_over_radius': separation, 'radius': self.radius, 'mass': self.mass, 'orbit': orbit,
               'sigma': sigma, 'amplitude_ratio_minus_one': amplitude_excess, 'pair_flux_ratio_minus_one': flux_excess,
               'reference_amplitude_infinity': reference['amplitude_infinity'], 'body_amplitude_infinity': exact_amplitude,
               'reference_pair_power_infinity': reference['pair_power_infinity_per_geometric_particle_mass_squared'],
               'body_pair_power_infinity': reference['pair_power_infinity_per_geometric_particle_mass_squared']*(1+flux_excess),
               'reference_pair_power_horizon': reference['pair_power_horizon_per_geometric_particle_mass_squared'],
               'direct_to_stable_amplitude_relative_error': abs(direct_amplitude/exact_amplitude-1),
               'value_jump_error': abs(value_jump-jump_value)/(1+abs(jump_value)),
               'slope_jump_error': abs(slope_jump-jump_slope)/(1+abs(jump_slope)),
               'reference_value_jump_error': reference['jump_value_error'], 'reference_slope_jump_error': reference['jump_slope_error'],
               'interior_nodes': len(solution.x), 'interior_maximum_residual': float(max(solution.rms_residuals)),
               'interior_boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
               'diagnostics': reference['diagnostics']}
        return row, solution
