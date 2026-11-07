from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'dynamical-tides-20261004'
sys.path.insert(0, str(PARENT))
from dynamic_system import Profile
from outgoing_modes_v4 import DynamicProblem, asymptotic_coefficients
sys.path.insert(0, str(BRANCH/'gravitating-tides-20261004'))
from solve_tides import exterior_basis


def potential(radius, mass):
    metric = 1-2*mass/radius
    return metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)


def propagate(radius_from, radius_to, mass, sigma, vectors, tolerance=3e-12):
    if radius_from == radius_to:
        return np.asarray(vectors, dtype=complex)
    shape = np.shape(vectors)

    def equation(position, flattened):
        state = flattened.reshape(shape)
        metric = 1-2*mass/position
        return (np.array([[0., 1.], [potential(position, mass)-sigma**2, 0.]])@state/metric).ravel()

    solution = solve_ivp(equation, (radius_from, radius_to), np.asarray(vectors, dtype=complex).ravel(), method='DOP853', rtol=tolerance, atol=tolerance/100)
    assert solution.success, solution.message
    return solution.y[:, -1].reshape(shape)


def static_master_basis(position, mass, reference_radius):
    growing, growing_prime, decaying, decaying_prime = exterior_basis(position, mass)
    metric = 1-2*mass/position
    lapse_prime = mass/(position**2*metric)
    amplitudes = np.array([growing, reference_radius**5*decaying])
    derivatives = np.array([growing_prime, reference_radius**5*decaying_prime])
    angular = ((3-metric)/2+position**2*metric*lapse_prime**2)*amplitudes+position**2*metric*lapse_prime*derivatives/2
    angular_prime = derivatives+2*lapse_prime*amplitudes
    shift = position**2/3*(angular_prime-(lapse_prime-1/position)*angular-amplitudes/position)
    transform = np.array([[(6*position**2+6*mass*position+6*mass**2)/(position**2*(2*position+3*mass)), 1.],
                          [(2*position**2-6*mass*position-3*mass**2)/((position-2*mass)*(2*position+3*mass)), position/metric]])
    return np.linalg.solve(transform, np.vstack([angular, shift]))


def outgoing_state(position, mass, sigma, far_phase=40., order=10, tolerance=2e-12):
    if sigma == 0:
        return static_master_basis(position, mass, 1.)[:, 1].astype(complex), {'far_phase': None, 'series_order': None, 'flux_error': 0.}
    assert sigma.real > 0
    outer = max(10*position, far_phase/sigma.real)
    coefficients = asymptotic_coefficients(mass*sigma, order)
    argument = sigma*outer
    indices = np.arange(order+1)
    series = np.sum(coefficients*argument**(-indices))
    derivative = np.sum(-indices*coefficients*argument**(-indices-1))
    metric = 1-2*mass/outer
    initial = np.array([1.+0j, 1j*sigma+metric*sigma*derivative/series])
    state = propagate(outer, position, mass, sigma, initial, tolerance)
    diagnostics = {'far_phase': far_phase, 'series_order': order, 'outer_radius': outer}
    if sigma.imag == 0:
        flux = initial[1].imag
        direct = np.imag(np.conj(state[0])*state[1])
        diagnostics['flux_error'] = float(abs(direct/flux-1))
        diagnostics['conserved_flux'] = float(flux)
        logarithm = complex((state[1]/state[0]).real, flux/abs(state[0])**2)
        state[1] = state[0]*logarithm
    state = np.array([1.+0j, logarithm if sigma.imag == 0 else state[1]/state[0]])
    return state, diagnostics


def determinant(first, second):
    return first[0]*second[1]-first[1]*second[0]


class ResponseProblem:
    def __init__(self, distance=.02, tolerance=2e-8, far_phase=40., order=10):
        self.profile = Profile(20., .03)
        self.radius = self.profile.radius
        self.mass = self.profile.alpha*self.profile.mass
        self.distance, self.tolerance, self.far_phase, self.order = distance, tolerance, far_phase, order
        self.previous = None

    def interior(self, sigma):
        problem = DynamicProblem(self.profile, complex(sigma), self.distance, self.tolerance)
        solution = problem.solve(self.previous)
        assert solution.success, solution.message
        self.previous = solution
        time_value, time_prime, master, master_star_prime = problem.surface(solution)
        return np.array([master, master_star_prime]), solution, problem

    def evaluate(self, sigma, buffers=(2., 3., 4.), shells=(10., 20., 40.)):
        sigma = complex(sigma)
        inside, solution, problem = self.interior(sigma)
        outgoing, diagnostics = outgoing_state(self.radius, self.mass, sigma, self.far_phase, self.order)
        rows = []
        for fraction in buffers:
            match_radius = fraction*self.radius
            seed = static_master_basis(match_radius, self.mass, self.radius)
            basis = propagate(match_radius, self.radius, self.mass, sigma, seed)
            inside_coefficients = np.linalg.solve(basis, inside)
            outside_coefficients = np.linalg.solve(basis, outgoing)
            ratio = outside_coefficients[0]/outside_coefficients[1]
            if sigma.imag == 0 and sigma.real > 0:
                logarithm = outgoing[1]/outgoing[0]
                denominator = logarithm*basis[0, 0]-basis[1, 0]
                ratio = complex(ratio.real, -np.linalg.det(basis).real*logarithm.imag/abs(denominator)**2)
            numerator = self.radius**5*inside_coefficients[1]/3
            denominator = inside_coefficients[0]-inside_coefficients[1]*ratio
            susceptibility = numerator/denominator
            conservative = self.radius**5*inside_coefficients[1]/(3*inside_coefficients[0])
            normalized_outgoing = outgoing/outside_coefficients[1]
            reference_green = basis[0, 0]*outgoing[0]/determinant(basis[:, 0], outgoing)
            total_green = inside[0]*outgoing[0]/determinant(inside, outgoing)
            excess_green = 3*susceptibility/self.radius**5*normalized_outgoing[0]**2/np.linalg.det(basis)
            identity_error = abs(total_green-reference_green-excess_green)/(1+abs(total_green)+abs(reference_green)+abs(excess_green))
            optical = susceptibility.imag-3*ratio.imag/self.radius**5*abs(susceptibility)**2
            rows.append({'buffer_over_radius': fraction, 'susceptibility': susceptibility,
                         'conservative_lambda': conservative, 'outgoing_mixing': ratio/self.radius**5,
                         'numerator': numerator, 'denominator': denominator,
                         'wronskian_scaled_basis': np.linalg.det(basis), 'green_identity_error': identity_error,
                         'optical_identity_scaled_error': abs(optical)/(1+abs(susceptibility.imag)),
                         'total_green_surface_surface': total_green,
                         'reference_green_surface_surface': reference_green,
                         'excess_green_surface_surface': excess_green})
        shell_rows = []
        wronskian = determinant(inside, outgoing)
        for fraction in shells:
            shell_radius = fraction*self.radius
            outward = propagate(self.radius, shell_radius, self.mass, sigma, outgoing)
            shell_rows.append({'source_radius_over_body_radius': fraction,
                               'master_surface_per_unit_source_jump': inside[0]*outward[0]/wronskian})
        return {'sigma': sigma, 'rows': rows, 'shell_rows': shell_rows, 'outgoing_diagnostics': diagnostics,
                'interior_nodes': len(solution.x), 'interior_maximum_residual': float(max(solution.rms_residuals)),
                'interior_boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p))))}, solution


def encode(value):
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, (complex, np.complexfloating)):
        return {'real': float(value.real), 'imaginary': float(value.imag)}
    if isinstance(value, np.generic):
        return value.item()
    return value
