from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'near-circular-inspiral-20261005'
PRIOR = BRANCH/'near-circular-quadrupole-20261005'
sys.path.insert(0, str(PRIOR))
from sidebands import AnalyticWave, symbolic_coefficients, digest, read_json, write_json, modest_process, orbit_constants
from analyze_limit import damping


def orbit_series(semilatus):
    time_linear = 2/(semilatus-2)-2+1/(semilatus-6)
    time_constant = -2/(semilatus-2)**2
    time_cosine = (4/(semilatus-2)**2+3+1.5/(semilatus-6)**2-4/(semilatus-2)
                   +2/((semilatus-2)*(semilatus-6))-2/(semilatus-6))
    time_mean = time_constant+time_cosine/2
    phase_mean = .75/(semilatus-6)**2
    return dict(time_linear=time_linear, time_constant=time_constant, time_cosine=time_cosine,
                time_mean=time_mean, radial_frequency_fraction=-time_mean,
                angular_frequency_fraction=phase_mean-time_mean,
                phase_wobble=2*np.sqrt(semilatus/(semilatus-6))*(semilatus-3)/(semilatus-2))


@lru_cache(maxsize=2)
def geometry_expressions(sector):
    arguments, expressions = symbolic_coefficients(sector)
    radius, mass, energy, angular, azimuth, frequency, harmonic_value = arguments
    delta, delta_prime, velocity_imaginary = expressions[:3]
    metric = 1-2*mass/radius
    small_lambda = 2+3*mass/radius
    polynomial = 8+12*mass/radius+84*mass**2/radius**2
    strength = 8*sp.pi*energy*harmonic_value/metric
    if sector == 'polar':
        velocity_squared = strength*(sp.diff(metric, radius)/(3*small_lambda*metric)+2/(3*small_lambda*radius)
                            +2*mass/(small_lambda**2*radius**2)+polynomial/(12*small_lambda**2*metric*radius)
                            -sp.diff(small_lambda, radius)/(3*small_lambda**2))
        slope_velocity_squared = delta_prime/metric**2
        potential = metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)
    else:
        velocity_squared = sp.Integer(0)
        slope_velocity_squared = sp.Integer(0)
        potential = metric*(6/radius**2-6*mass/radius**3)
    vacuum = (potential-frequency**2)/metric
    first_master = sp.diff(delta, radius)-delta_prime*vacuum
    first_slope = delta/metric-sp.diff(delta_prime, radius)
    second_master = sp.diff(first_master, radius)+first_slope*vacuum
    second_slope = first_master/metric+sp.diff(first_slope, radius)
    semilatus = radius/mass
    time_linear = 2/(semilatus-2)-2+1/(semilatus-6)
    wobble = 2*sp.sqrt(semilatus/(semilatus-6))*(semilatus-3)/(semilatus-2)
    radial_frequency = sp.sqrt(mass/radius**3)*sp.sqrt(1-6/semilatus)
    energy_second = energy*(1/(2*(semilatus-3))-2/(semilatus-2)**2)
    angular_second = angular/(2*(semilatus-3))
    master = (energy_second*sp.diff(delta, energy)+angular_second*sp.diff(delta, angular)
              +radius*(1-time_linear)*first_master/2+radius**2*second_master/4
              +radius**2*radial_frequency**2*velocity_squared/2
              +azimuth*wobble*radius*radial_frequency*velocity_imaginary/2
              -azimuth**2*wobble**2*delta/4)
    slope = (-energy_second*sp.diff(delta_prime, energy)-angular_second*sp.diff(delta_prime, angular)
             +radius*(1-time_linear)*first_slope/2+radius**2*second_slope/4
             +radius**2*radial_frequency**2*slope_velocity_squared/2
             +azimuth**2*wobble**2*delta_prime/4)
    return arguments, (delta, -delta_prime, master, slope, velocity_squared, slope_velocity_squared)


@lru_cache(maxsize=2)
def numerical_geometry(sector):
    arguments, expressions = geometry_expressions(sector)
    return sp.lambdify(arguments, expressions, 'numpy', cse=True)


def source_geometry(sector, mass, semilatus, azimuth, frequency):
    energy, angular = orbit_constants(mass, semilatus, 0.)
    harmonic_value = np.sqrt(15/(32*np.pi))
    values = numerical_geometry(sector)(mass*semilatus, mass, energy, angular, azimuth, frequency, harmonic_value)
    return np.asarray(values[:4], dtype=float).reshape(2, 2)


def pair(value):
    return [float(value.real), float(value.imag)]


def complex_value(row, key, order=0):
    return complex(*row['responses'][order][key])


class CarrierWave(AnalyticWave):
    def evaluate_frequency(self, frequency):
        azimuth = 2 if self.sector == 'polar' else 1
        source = source_geometry(self.sector, self.mass, self.semilatus, azimuth, frequency)
        chosen = self.settings
        positions = np.array([self.radius, self.orbit])
        outgoing, outgoing_norm, outdiag = self.vacuum.outgoing_samples(self.mass, frequency, positions,
                               chosen['far_phase'], chosen['outer_order'], chosen['exterior_tolerance'])
        horizon, horizon_norm, horizon_diag = self.vacuum.horizon_samples(self.mass, frequency, positions,
                               chosen['horizon_epsilon'], chosen['horizon_order'], chosen['exterior_tolerance'])
        alpha_out, alpha_horizon = outgoing[self.radius][1].real, horizon[self.radius][1].real
        beta_out, beta_horizon = frequency/abs(outgoing_norm)**2, -frequency/abs(horizon_norm)**2
        real_out = np.array([outgoing[position].real for position in positions])
        dirichlet = self.propagate([0., 1.], frequency).real
        body_slope, interior, archive = self.interior(frequency)
        direct = self.propagate([1., body_slope], frequency).real
        body_w = complex(alpha_out-body_slope, beta_out)
        horizon_w = complex(alpha_out-alpha_horizon, beta_out-beta_horizon)
        delta_w = complex(alpha_horizon-body_slope, beta_horizon)
        responses = []
        for coefficients in source:
            real_overlap = float(coefficients@real_out[-1])
            dirichlet_overlap = float(coefficients@dirichlet[-1])
            outgoing_source = complex(real_overlap, beta_out*dirichlet_overlap)
            horizon_source = complex(real_overlap+(alpha_horizon-alpha_out)*dirichlet_overlap, beta_horizon*dirichlet_overlap)
            reference_amplitude = horizon_source/(horizon_w*outgoing_norm)
            difference_coefficient = -delta_w*outgoing_source/(body_w*horizon_w)
            delta_amplitude = difference_coefficient/outgoing_norm
            horizon_amplitude = outgoing_source/(horizon_w*horizon_norm)
            action = -3/(8*np.pi)*difference_coefficient*outgoing_source
            factor = 3*frequency**2/(4*np.pi)
            difference_power = factor*(2*(np.conj(reference_amplitude)*delta_amplitude).real+abs(delta_amplitude)**2)
            horizon_power = factor*abs(horizon_amplitude)**2
            direct_amplitude = (coefficients@direct[-1])/(body_w*outgoing_norm)
            responses.append(dict(reference_amplitude=pair(reference_amplitude), delta_amplitude=pair(delta_amplitude),
                 horizon_amplitude=pair(horizon_amplitude), outgoing_source=pair(outgoing_source),
                 difference_coefficient=pair(difference_coefficient), action=pair(action),
                 difference_power=float(difference_power), horizon_power=float(horizon_power),
                 optical_error=float(abs(2*frequency*action.imag-difference_power+horizon_power)/max(abs(difference_power)+horizon_power, 1e-300)),
                 direct_error=float(abs(direct_amplitude-reference_amplitude-delta_amplitude)/max(abs(reference_amplitude+delta_amplitude), 1e-300))))
        row = dict(sector=self.sector, azimuth=azimuth, frequency=float(frequency),
                   mass=self.mass, radius=self.radius, semilatus=self.semilatus, separation=self.orbit/self.radius,
                   source_coefficients=source.tolist(), responses=responses, **interior,
                   Wronskian_error=float(max(abs(real_out[:, 0]*dirichlet[:, 1]-real_out[:, 1]*dirichlet[:, 0]-1))),
                   outgoing_diagnostic=outdiag, horizon_diagnostic=horizon_diag)
        archive.update(positions=positions, real_outgoing=real_out, dirichlet=dirichlet, direct_body=direct,
                       frequency=frequency, source_coefficients=source)
        return row, archive


def imported_hashes():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values()) if getattr(module, '__file__', None)
             and Path(module.__file__).suffix == '.py' and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    return {str(path): digest(path) for path in sorted(paths)}

