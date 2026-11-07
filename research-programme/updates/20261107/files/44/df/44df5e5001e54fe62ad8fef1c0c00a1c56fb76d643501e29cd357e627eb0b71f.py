from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
import psutil


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'eccentric-source-20261005'))
from eccentric_source import anomaly_solution, source_samples
sys.path.insert(0, str(BRANCH/'axial-companion-20261005'))
from axial_binary import WaveBody, outgoing_samples, horizon_samples, sample_vacuum


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def save_json(path, report):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)


def report_header(script):
    return {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
            'script_sha256': digest(script)}


def settings(label):
    fine = label != 'coarse'
    return {'interior': {'tolerance': 8e-14 if fine else 3e-12, 'max_step': 1/360 if fine else 1/240,
                         'start': 5e-6 if fine else 1e-5},
            'exterior': {'tolerance': 8e-14 if fine else 3e-12, 'far_phase': 65. if fine else 80.,
                         'order': 16 if fine else 14, 'horizon_epsilon': 2e-6 if fine else 3e-6},
            'source_order': 40 if label == 'quadrature' else (32 if fine else 24),
            'source_panels_per_half': 32 if label == 'quadrature' else (24 if fine else 16),
            'orbit_tolerance': 3e-13 if fine else 3e-11}


def paired_flux(frequency, amplitude):
    factor = 3/(4*np.pi)
    return factor*frequency**2*abs(amplitude)**2, factor*frequency*abs(amplitude)**2


class EccentricRadiation:
    def __init__(self, chosen_settings, eccentricity):
        self.settings = chosen_settings
        self.body = WaveBody(.03)
        self.mass, self.radius = self.body.mass, self.body.radius
        self.eccentricity = eccentricity
        self.semilatus = 5*self.radius*(1+eccentricity)/self.mass
        self.trajectory = anomaly_solution(self.mass, self.semilatus, eccentricity, chosen_settings['orbit_tolerance'])
        self.period, self.phase_advance = 2*self.trajectory.sol(np.pi)[:2]
        self.half, self.half_weights = self.source_nodes(chosen_settings['source_order'], 0., np.pi)
        self.full, self.full_weights = self.source_nodes(chosen_settings['source_order'], 0., 2*np.pi)
        radii = np.concatenate([[self.radius], self.half['radius'], self.full['radius']])
        self.positions = np.array(sorted(set(radii)))
        self.half_indices = np.searchsorted(self.positions, self.half['radius'])
        self.full_indices = np.searchsorted(self.positions, self.full['radius'])

    def source_nodes(self, order, lower, upper):
        points, weights = leggauss(order)
        panels = self.settings['source_panels_per_half']*(2 if upper-lower > np.pi+.1 else 1)
        edges = np.linspace(lower, upper, panels+1)
        midpoints = (edges[:-1]+edges[1:])/2
        jacobians = np.diff(edges)/2
        anomaly = (midpoints[:, None]+jacobians[:, None]*points).ravel()
        samples = source_samples(anomaly, self.trajectory, self.mass, self.semilatus, self.eccentricity)
        weights = (jacobians[:, None]*weights).ravel()*samples['time_anomaly']/self.period
        return samples, weights

    def real_overlap(self, radial, frequency):
        samples = self.half
        value, slope = radial[self.half_indices].T
        phase = frequency*samples['time']-samples['phase']
        amplitude = np.abs(samples['jump'])
        terms = -2*amplitude*((samples['metric']/samples['radius']*value+slope)*np.cos(phase)
                             -frequency*samples['tortoise_velocity']*value*np.sin(phase))
        result = np.dot(self.half_weights, terms)
        absolute_scale = np.dot(self.half_weights, np.abs(terms))
        return float(result), float(absolute_scale)

    def full_overlap(self, radial, frequency):
        samples = self.full
        value, slope = radial[self.full_indices].T
        phase = np.exp(1j*frequency*samples['time'])
        direct = phase*(samples['delta']*value-samples['delta_prime']*slope)
        weak = -phase*samples['jump']*((samples['metric']/samples['radius']+1j*frequency*samples['tortoise_velocity'])*value+slope)
        return np.dot(self.full_weights, direct), np.dot(self.full_weights, weak), float(np.dot(self.full_weights, np.abs(direct)+np.abs(weak)))

    def evaluate(self, harmonic):
        frequency = (self.phase_advance+2*np.pi*harmonic)/self.period
        assert frequency != 0, 'An exactly static mode needs a separate static field solve; radiative flux is zero.'
        positive = abs(frequency)
        sign = 1. if frequency > 0 else -1.
        exterior = self.settings['exterior']
        outgoing, outgoing_norm, outgoing_diagnostic = outgoing_samples(self.mass, positive, self.positions,
            exterior['far_phase'], exterior['order'], exterior['tolerance'])
        horizon, horizon_norm, horizon_diagnostic = horizon_samples(self.mass, positive, self.positions,
            exterior['horizon_epsilon'], exterior['order'], exterior['tolerance'])
        if sign < 0:
            outgoing_norm, horizon_norm = np.conj(outgoing_norm), np.conj(horizon_norm)
        alpha_out = outgoing[self.radius][1].real
        alpha_horizon = horizon[self.radius][1].real
        beta_out = frequency/abs(outgoing_norm)**2
        beta_horizon = -frequency/abs(horizon_norm)**2
        real_outgoing = np.array([outgoing[position].real for position in self.positions])
        quadrature, evaluations = sample_vacuum(self.radius, self.positions[-1], [0., 1.], self.mass,
                                               positive, self.positions, exterior['tolerance'])
        quadrature = quadrature.real
        outgoing_states = real_outgoing+1j*beta_out*quadrature
        horizon_states = real_outgoing+(alpha_horizon-alpha_out+1j*beta_horizon)*quadrature
        response, _ = self.body.solve(positive*self.radius, **self.settings['interior'])
        body_slope = response['Y']/self.radius
        real_source, real_scale = self.real_overlap(real_outgoing, frequency)
        quadrature_source, quadrature_scale = self.real_overlap(quadrature, frequency)
        overlap_out = complex(real_source, beta_out*quadrature_source)
        overlap_horizon = complex(real_source+(alpha_horizon-alpha_out)*quadrature_source,
                                  beta_horizon*quadrature_source)
        overlap_body = real_source+(body_slope-alpha_out)*quadrature_source
        wronskian_body = complex(alpha_out-body_slope, beta_out)
        wronskian_horizon = complex(alpha_out-alpha_horizon, beta_out-beta_horizon)
        difference_wronskian = complex(alpha_horizon-body_slope, beta_horizon)
        reference_coefficient = overlap_horizon/wronskian_horizon
        delta_coefficient = -difference_wronskian*overlap_out/(wronskian_body*wronskian_horizon)
        reference_amplitude = reference_coefficient/outgoing_norm
        delta_amplitude = delta_coefficient/outgoing_norm
        body_amplitude = reference_amplitude+delta_amplitude
        horizon_amplitude = overlap_out/wronskian_horizon/horizon_norm
        reference_power, reference_angular = paired_flux(frequency, reference_amplitude)
        horizon_power, horizon_angular = paired_flux(frequency, horizon_amplitude)
        factor = 3/(4*np.pi)*frequency**2
        difference_power = factor*(2*(np.conj(reference_amplitude)*delta_amplitude).real+abs(delta_amplitude)**2)
        difference_angular = difference_power/frequency
        retarded_action = -3/(8*np.pi)*delta_coefficient*overlap_out
        optical_power = 2*frequency*retarded_action.imag
        net_power = difference_power-horizon_power
        optical_scale = abs(difference_power)+horizon_power
        full_errors = []
        for radial, expected in [(real_outgoing, real_source), (quadrature, quadrature_source)]:
            raw, weak, scale = self.full_overlap(radial, frequency)
            full_errors.append(float(max(abs(raw-weak), abs(weak-expected))/max(scale, 1e-300)))
        wronskians = real_outgoing[:, 0]*quadrature[:, 1]-real_outgoing[:, 1]*quadrature[:, 0]
        direct_states, direct_evaluations = sample_vacuum(self.radius, self.positions[-1], [1., body_slope], self.mass,
                                                       positive, self.positions, exterior['tolerance'])
        direct_overlap, direct_scale = self.real_overlap(direct_states.real, frequency)
        direct_amplitude = direct_overlap/wronskian_body/outgoing_norm
        amplitude_scale = max(abs(body_amplitude), (real_scale+abs(body_slope-alpha_out)*quadrature_scale)/abs(wronskian_body*outgoing_norm), 1e-300)
        control = -0.*overlap_out/(wronskian_horizon*wronskian_horizon)
        signed_reconstruction = np.array([horizon[position] if sign > 0 else np.conj(horizon[position]) for position in self.positions])
        reconstruction_error = np.max(np.abs(horizon_states-signed_reconstruction))/max(np.max(np.abs(signed_reconstruction)), 1e-300)
        saved = {'positions': self.positions, 'real_outgoing': real_outgoing, 'dirichlet': quadrature,
                 'direct_body': direct_states.real, 'half_anomaly': self.half['anomaly'],
                 'half_time': self.half['time'], 'half_phase': self.half['phase'],
                 'half_radius': self.half['radius'], 'half_weights': self.half_weights}
        row = {'eccentricity': self.eccentricity, 'harmonic': harmonic, 'frequency': float(frequency),
               'frequency_R': float(frequency*self.radius), 'body_Y': response['Y'],
               'source_real_basis': real_source, 'source_Dirichlet_basis': quadrature_source,
               'source_real_absolute_scale': real_scale, 'source_Dirichlet_absolute_scale': quadrature_scale,
               'alpha_out': float(alpha_out), 'beta_out': float(beta_out),
               'alpha_horizon': float(alpha_horizon), 'beta_horizon': float(beta_horizon),
               'outgoing_norm_real': float(outgoing_norm.real), 'outgoing_norm_imag': float(outgoing_norm.imag),
               'horizon_norm_real': float(horizon_norm.real), 'horizon_norm_imag': float(horizon_norm.imag),
               'reference_amplitude_real': float(reference_amplitude.real), 'reference_amplitude_imag': float(reference_amplitude.imag),
               'delta_amplitude_real': float(delta_amplitude.real), 'delta_amplitude_imag': float(delta_amplitude.imag),
               'horizon_amplitude_real': float(horizon_amplitude.real), 'horizon_amplitude_imag': float(horizon_amplitude.imag),
               'BH_infinity_energy': float(reference_power), 'body_infinity_energy': float(reference_power+difference_power),
               'difference_infinity_energy': float(difference_power), 'BH_horizon_energy': float(horizon_power),
               'difference_total_energy': float(net_power), 'BH_infinity_angular': float(reference_angular),
               'body_infinity_angular': float(reference_angular+difference_angular),
               'difference_infinity_angular': float(difference_angular), 'BH_horizon_angular': float(horizon_angular),
               'difference_total_angular': float(difference_angular-horizon_angular),
               'retarded_action_real': float(retarded_action.real), 'retarded_action_imag': float(retarded_action.imag),
               'optical_energy_difference': float(optical_power),
               'optical_error_over_component_sum': float(abs(optical_power-net_power)/max(optical_scale, 1e-300)),
               'full_source_integral_error_over_absolute_scale': max(full_errors),
               'direct_body_amplitude_error_over_source_scale': float(abs(direct_amplitude-body_amplitude)/amplitude_scale),
               'Wronskian_error': float(np.max(np.abs(wronskians-1))),
               'BH_reconstruction_relative_error': float(reconstruction_error), 'BH_boundary_control': float(abs(control)),
               'outgoing_diagnostic': outgoing_diagnostic, 'horizon_diagnostic': horizon_diagnostic,
               'interior_evaluations': response['function_evaluations'], 'Dirichlet_evaluations': evaluations,
               'direct_body_evaluations': direct_evaluations}
        return row, saved
