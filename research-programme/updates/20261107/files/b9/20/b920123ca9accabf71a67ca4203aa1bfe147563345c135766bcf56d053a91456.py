from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'eccentric-polar-radiation-20261005'))
from polar_radiation import PolarRadiation, settings as polar_settings, digest, read_json, write_json, modest_process
from eccentric_source import anomaly_solution, orbit_constants
import companion_system as polar_vacuum
sys.path.insert(0, str(BRANCH/'eccentric-radiation-20261005'))
from eccentric_radiation import settings as odd_settings
import axial_binary as odd_vacuum


def symbolic_coefficients(sector):
    radius, mass, energy, angular, azimuth, frequency, harmonic_value = sp.symbols('r M E h m omega Y', real=True)
    metric = 1-2*mass/radius
    metric_prime = sp.diff(metric, radius)
    if sector == 'polar':
        small_lambda = 2+3*mass/radius
        lambda_prime = sp.diff(small_lambda, radius)
        speed = metric*angular/(energy*radius**2)
        strength = 8*sp.pi*energy*harmonic_value/metric
        polynomial = 8+12*mass/radius+84*mass**2/radius**2
        delta = strength*(-radius*speed**2*(3-azimuth**2)/6
                  +(-metric*metric_prime-2*metric**2/radius+radius*metric*speed**2)/(3*small_lambda)
                  +metric**2*lambda_prime/(3*small_lambda**2)-metric*polynomial/(12*radius*small_lambda**2))
        delta_prime = strength*metric/(3*small_lambda)
        velocity_imaginary = -2*azimuth*strength*speed/(3*small_lambda)
    elif sector == 'odd':
        jump = 4*sp.pi*angular/(3*radius)*sp.sqrt(15/(8*sp.pi))
        delta = -jump*metric/radius
        delta_prime = jump
        velocity_imaginary = -jump*frequency/metric
    else:
        raise ValueError(sector)
    arguments = (radius, mass, energy, angular, azimuth, frequency, harmonic_value)
    expressions = tuple(sp.factor(expression) for expression in
                        (delta, delta_prime, velocity_imaginary, sp.diff(delta, radius), sp.diff(delta_prime, radius)))
    return arguments, expressions


@lru_cache(maxsize=2)
def numeric_coefficients(sector):
    arguments, expressions = symbolic_coefficients(sector)
    return sp.lambdify(arguments, expressions, 'numpy', cse=True)


def source_law(sector, mass, semilatus, azimuth, harmonic):
    assert harmonic in [-1, 0, 1]
    assert azimuth in ([0, 2] if sector == 'polar' else [1])
    assert not (azimuth == 0 and harmonic == 0)
    radius = mass*semilatus
    omega_phi = 1/(mass*semilatus**1.5)
    omega_r = omega_phi*np.sqrt(1-6/semilatus)
    frequency = azimuth*omega_phi+harmonic*omega_r
    phase_wobble = 2*np.sqrt(semilatus/(semilatus-6))*(semilatus-3)/(semilatus-2)
    energy, angular = orbit_constants(mass, semilatus, 0.)
    harmonic_value = -np.sqrt(5/(16*np.pi)) if azimuth == 0 else np.sqrt(15/(32*np.pi))
    delta, delta_prime, velocity_imaginary, delta_radial, delta_prime_radial = numeric_coefficients(sector)(
                 radius, mass, energy, angular, azimuth, frequency, harmonic_value)
    metric = 1-2*mass/radius
    potential = (polar_vacuum if sector == 'polar' else odd_vacuum).potential(radius, mass)
    if harmonic == 0:
        master_coefficient, slope_coefficient = delta, -delta_prime
    else:
        master_coefficient = (-radius*(delta_radial-delta_prime*(potential-frequency**2)/metric)
                               -harmonic*radius*omega_r*velocity_imaginary+harmonic*azimuth*phase_wobble*delta)/2
        slope_coefficient = (-radius*(delta/metric-delta_prime_radial)
                              -harmonic*azimuth*phase_wobble*delta_prime)/2
    return {'master_coefficient': float(master_coefficient), 'slope_coefficient': float(slope_coefficient),
            'delta_at_circle': float(delta), 'delta_prime_at_circle': float(delta_prime),
            'velocity_imaginary_coefficient': float(velocity_imaginary), 'delta_radial_derivative': float(delta_radial),
            'delta_prime_radial_derivative': float(delta_prime_radial), 'phase_wobble': float(phase_wobble),
            'frequency': float(frequency), 'omega_phi': float(omega_phi), 'omega_r': float(omega_r)}


class FixedPolar(PolarRadiation):
    def __init__(self, chosen, eccentricity):
        super().__init__(chosen, eccentricity)
        self.semilatus = 5*self.radius/self.mass
        self.energy, self.angular = orbit_constants(self.mass, self.semilatus, eccentricity)
        self.trajectory = anomaly_solution(self.mass, self.semilatus, eccentricity, chosen['orbit_tolerance'])
        self.period, self.phase_advance = 2*self.trajectory.sol(np.pi)[:2]
        self.omega_r, self.omega_phi = 2*np.pi/self.period, self.phase_advance/self.period
        self.half, self.half_weights = self.source_nodes(False)
        self.full, self.full_weights = self.source_nodes(True)
        self.positions = np.unique(np.concatenate([[self.radius], self.half['radius'], self.full['radius']]))
        self.half_indices = np.searchsorted(self.positions, self.half['radius'])
        self.full_indices = np.searchsorted(self.positions, self.full['radius'])


class AnalyticWave:
    def __init__(self, sector, label, separation=5.):
        self.sector, self.label = sector, label
        self.settings = polar_settings(label)
        self.vacuum = polar_vacuum if sector == 'polar' else odd_vacuum
        self.body = polar_vacuum.ResponseProblem(self.settings['distance'], self.settings['interior_tolerance']) if sector == 'polar' else odd_vacuum.WaveBody(.03)
        self.mass, self.radius = self.body.mass, self.body.radius
        self.semilatus = separation*self.radius/self.mass
        self.orbit = self.mass*self.semilatus

    def interior(self, frequency):
        if self.sector == 'polar':
            state, solution, problem = self.body.interior(abs(frequency))
            slope = state[1]/state[0]
            assert abs(slope.imag) < 1e-12
            report = {'interior_nodes': len(solution.x), 'interior_maximum_residual': float(max(solution.rms_residuals)),
                      'interior_boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p))))}
            archive = {'spline_knots': solution.sol.x, 'spline_coefficients': solution.sol.c,
                       'parameters': solution.p, 'scales': problem.scales}
            return float(slope.real), report, archive
        response, solution = self.body.solve(abs(frequency)*self.radius, **odd_settings(self.label)['interior'])
        return response['Y']/self.radius, {'interior_evaluations': response['function_evaluations']}, {'interior_mesh': solution.t, 'interior_values': solution.y}

    def propagate(self, initial, frequency):
        value = self.vacuum.sample_vacuum(self.radius, self.orbit, initial, self.mass, abs(frequency),
                                         np.array([self.radius, self.orbit]), self.settings['exterior_tolerance'])
        return value if self.sector == 'polar' else value[0]

    def evaluate(self, azimuth, harmonic):
        law = source_law(self.sector, self.mass, self.semilatus, azimuth, harmonic)
        frequency = law['frequency']
        assert frequency != 0
        chosen = self.settings
        positions = np.array([self.radius, self.orbit])
        outgoing, outgoing_norm, outdiag = self.vacuum.outgoing_samples(self.mass, abs(frequency), positions,
                            chosen['far_phase'], chosen['outer_order'], chosen['exterior_tolerance'])
        horizon, horizon_norm, horizon_diag = self.vacuum.horizon_samples(self.mass, abs(frequency), positions,
                            chosen['horizon_epsilon'], chosen['horizon_order'], chosen['exterior_tolerance'])
        if frequency < 0:
            outgoing_norm, horizon_norm = np.conj(outgoing_norm), np.conj(horizon_norm)
        alpha_out, alpha_horizon = outgoing[self.radius][1].real, horizon[self.radius][1].real
        beta_out, beta_horizon = frequency/abs(outgoing_norm)**2, -frequency/abs(horizon_norm)**2
        real_out = np.array([outgoing[position].real for position in positions])
        dirichlet = self.propagate([0., 1.], frequency).real
        body_slope, interior, archive = self.interior(frequency)
        coefficients = np.array([law['master_coefficient'], law['slope_coefficient']])
        real_overlap, dirichlet_overlap = float(coefficients@real_out[-1]), float(coefficients@dirichlet[-1])
        outgoing_source = complex(real_overlap, beta_out*dirichlet_overlap)
        horizon_source = complex(real_overlap+(alpha_horizon-alpha_out)*dirichlet_overlap, beta_horizon*dirichlet_overlap)
        body_w = complex(alpha_out-body_slope, beta_out)
        horizon_w = complex(alpha_out-alpha_horizon, beta_out-beta_horizon)
        delta_w = complex(alpha_horizon-body_slope, beta_horizon)
        reference_coefficient = horizon_source/horizon_w
        difference_coefficient = -delta_w*outgoing_source/(body_w*horizon_w)
        reference_amplitude, delta_amplitude = reference_coefficient/outgoing_norm, difference_coefficient/outgoing_norm
        horizon_amplitude = outgoing_source/(horizon_w*horizon_norm)
        factor = 3/(4*np.pi)*frequency**2
        reference_power, horizon_power = factor*abs(reference_amplitude)**2, factor*abs(horizon_amplitude)**2
        difference_power = factor*(2*(np.conj(reference_amplitude)*delta_amplitude).real+abs(delta_amplitude)**2)
        action = -3/(8*np.pi)*difference_coefficient*outgoing_source
        direct = self.propagate([1., body_slope], frequency).real
        direct_amplitude = (coefficients@direct[-1])/(body_w*outgoing_norm)
        row = {'sector': self.sector, 'azimuth': azimuth, 'harmonic': harmonic, 'mass': self.mass, 'radius': self.radius,
               'semilatus': self.semilatus, 'separation_over_radius': self.orbit/self.radius, 'eccentricity_order_amplitude': int(harmonic != 0),
               'power_normalization': 'per mu squared' if harmonic == 0 else 'leading coefficient per mu squared e squared',
               **law, **interior, 'body_slope': body_slope, 'source_real_basis': real_overlap,
               'source_dirichlet_basis': dirichlet_overlap, 'BH_infinity_energy': float(reference_power),
               'BH_horizon_energy': float(horizon_power), 'body_infinity_energy': float(reference_power+difference_power),
               'difference_infinity_energy': float(difference_power), 'difference_total_energy': float(difference_power-horizon_power),
               'retarded_action_real': float(action.real), 'retarded_action_imag': float(action.imag),
               'optical_error_over_component_sum': float(abs(2*frequency*action.imag-difference_power+horizon_power)/max(abs(difference_power)+horizon_power, 1e-300)),
               'direct_body_amplitude_relative_error': float(abs(direct_amplitude-reference_amplitude-delta_amplitude)/max(abs(reference_amplitude+delta_amplitude), 1e-300)),
               'Wronskian_error': float(max(abs(real_out[:, 0]*dirichlet[:, 1]-real_out[:, 1]*dirichlet[:, 0]-1))),
               'outgoing_diagnostic': outdiag, 'horizon_diagnostic': horizon_diag}
        for prefix, value in [('reference_amplitude', reference_amplitude), ('delta_amplitude', delta_amplitude), ('horizon_amplitude', horizon_amplitude)]:
            row[prefix+'_real'], row[prefix+'_imag'] = float(value.real), float(value.imag)
        archive.update(positions=positions, real_outgoing=real_out, dirichlet=dirichlet, direct_body=direct, frequency=frequency)
        return row, archive
