from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'companion-source-20261004'
sys.path.insert(0, str(PARENT))
from companion_system import CompanionProblem, ResponseProblem, reference_wave, outgoing_samples, determinant, static_master_basis, potential, encode


def jumps(orbit, mass, azimuth, particle=1.):
    harmonic = -np.sqrt(5/(16*np.pi)) if azimuth == 0 else np.sqrt(15/(32*np.pi))
    common = 8*np.pi*particle*harmonic/np.sqrt(1-3*mass/orbit)
    jump_a = common*(orbit-2*mass)/(3*(2*orbit+3*mass))
    jump_b = -common*(12*orbit**3-16*orbit**2*mass-24*orbit*mass**2-33*mass**3)/(6*orbit**2*(2*orbit+3*mass)**2)
    jump_b += common*mass*(azimuth**2-4)/(6*orbit**2)
    return jump_a, jump_b, harmonic


def metric_helical(state, orbit, mass, azimuth):
    metric = 1-2*mass/orbit
    sigma_squared = azimuth**2*mass/orbit**3
    numerator = 6*orbit**2+6*mass*orbit+6*mass**2
    denominator = orbit**2*(2*orbit+3*mass)
    coefficient = numerator/denominator
    coefficient_prime = ((12*orbit+6*mass)*denominator-numerator*(6*orbit**2+6*mass*orbit))/denominator**2
    master, slope = state
    angular = coefficient*master+slope
    angular_prime = coefficient_prime*master+coefficient*slope/metric+(potential(orbit, mass)-sigma_squared)*master/metric
    lapse = (2+3*mass/orbit)/metric*(3*master/orbit-angular)+orbit*angular_prime
    return metric*lapse+mass/orbit*angular


def static_action(orbit, mass, tidal_lambda):
    basis = static_master_basis(orbit, mass, 1.)
    decaying = basis[:, 1]
    jump_a, jump_b, harmonic = jumps(orbit, mass, 0)
    overlap = jump_b*decaying[0]-jump_a*decaying[1]
    coefficient = 3*tidal_lambda*overlap/np.linalg.det(basis)
    action = -3/(16*np.pi)*coefficient*overlap
    helical = harmonic*metric_helical(coefficient*decaying, orbit, mass, 0)
    reconstruction = helical/(4*np.sqrt(1-3*mass/orbit))
    return float(np.real(action)), float(abs(reconstruction/action-1))


def action_from_wave(row, tidal_lambda, settings):
    orbit, radius, mass, sigma = (row[key] for key in ['orbit', 'radius', 'mass', 'sigma'])
    outgoing, surface, _ = outgoing_samples(mass, sigma, [radius, orbit], settings['far_phase'], settings['outer_order'], settings['tolerance'])
    excess = row['amplitude_ratio_minus_one']
    reference_amplitude = row['reference_amplitude_infinity']
    if isinstance(excess, dict):
        excess = complex(excess['real'], excess['imaginary'])
        reference_amplitude = complex(reference_amplitude['real'], reference_amplitude['imaginary'])
    delta_coefficient = excess*reference_amplitude*surface
    jump_a, jump_b, harmonic = jumps(orbit, mass, 2)
    overlap = jump_b*outgoing[orbit][0]-jump_a*outgoing[orbit][1]
    action_pair = -3/(8*np.pi)*np.real(delta_coefficient*overlap)
    helical_pair = 2*np.real(harmonic*metric_helical(delta_coefficient*outgoing[orbit], orbit, mass, 2))
    reconstructed = helical_pair/(4*np.sqrt(1-3*mass/orbit))
    action_zero, zero_error = static_action(orbit, mass, tidal_lambda)
    leading = 1.5*tidal_lambda/orbit**6
    total = action_zero+action_pair
    return {'separation_over_radius': orbit/radius, 'orbit': orbit, 'omega': sigma/2,
            'tidal_lambda': tidal_lambda, 'action_m0_per_particle_squared': action_zero,
            'action_pair_per_particle_squared': float(action_pair), 'action_per_particle_squared': float(total),
            'action_over_leading': float(total/leading), 'static_mode_fraction': float(action_zero/total),
            'm0_metric_reciprocity_error': zero_error, 'pair_metric_reciprocity_error': float(abs(reconstructed/action_pair-1)),
            'helical_metric_pair_per_particle': float(helical_pair),
            'leading_relative_error': float(abs(total/leading-1)),
            'first_PN_relative_error': float(abs(total/(leading*(1+4*mass/orbit))-1)),
            'inferred_first_PN_action_coefficient': float((total/leading-1)/(mass/orbit))}


def static_lambda(problem):
    inside, solution, _ = problem.interior.interior(0.)
    coefficients = np.linalg.solve(static_master_basis(problem.radius, problem.mass, problem.radius), inside)
    value = problem.radius**5*coefficients[1]/(3*coefficients[0])
    assert abs(value.imag) < 1e-9
    return float(value.real), solution
