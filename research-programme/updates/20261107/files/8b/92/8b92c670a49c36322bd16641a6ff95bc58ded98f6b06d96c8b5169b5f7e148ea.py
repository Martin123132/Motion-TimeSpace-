from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
BACKGROUND = BRANCH/'self-gravity-20261003/results/fine/R20-C0p03.npz'
sys.path.insert(0, str(BRANCH/'axial-companion-20261005'))
from axial_binary import WaveBody, source_jumps


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def write_report(directory, script, report):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(script), **report}
    with (directory/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)


def orbit_constants(mass, semilatus, eccentricity):
    assert 0 <= eccentricity < 1 and semilatus > 6+2*eccentricity
    denominator = semilatus-3-eccentricity**2
    energy = np.sqrt(((semilatus-2)**2-4*eccentricity**2)/(semilatus*denominator))
    angular_momentum = mass*semilatus/np.sqrt(denominator)
    return energy, angular_momentum


def anomaly_rates(anomaly, mass, semilatus, eccentricity):
    cosine = np.cos(anomaly)
    radial_factor = 1+eccentricity*cosine
    turning_factor = semilatus-6-2*eccentricity*cosine
    time_rate = mass*semilatus**2*np.sqrt((semilatus-2)**2-4*eccentricity**2)
    time_rate /= (semilatus-2-2*eccentricity*cosine)*radial_factor**2*np.sqrt(turning_factor)
    phase_rate = np.sqrt(semilatus/turning_factor)
    proper_rate = mass*semilatus**1.5*np.sqrt(semilatus-3-eccentricity**2)
    proper_rate /= radial_factor**2*np.sqrt(turning_factor)
    return np.array([time_rate, phase_rate, proper_rate])


def anomaly_solution(mass, semilatus, eccentricity, tolerance):
    solution = solve_ivp(lambda anomaly, state: anomaly_rates(anomaly, mass, semilatus, eccentricity),
                         (0., 2*np.pi), np.zeros(3), method='DOP853', rtol=tolerance,
                         atol=tolerance/100, max_step=.08, dense_output=True)
    assert solution.success, solution.message
    return solution


def source_samples(anomaly, trajectory, mass, semilatus, eccentricity, particle_mass=1.):
    energy, angular_momentum = orbit_constants(mass, semilatus, eccentricity)
    time, phase, proper = trajectory.sol(anomaly)
    radius = mass*semilatus/(1+eccentricity*np.cos(anomaly))
    metric = 1-2*mass/radius
    metric_prime = 2*mass/radius**2
    rates = anomaly_rates(anomaly, mass, semilatus, eccentricity)
    radius_anomaly = mass*semilatus*eccentricity*np.sin(anomaly)/(1+eccentricity*np.cos(anomaly))**2
    proper_velocity = radius_anomaly/rates[2]
    proper_acceleration = -mass/radius**2+angular_momentum**2/radius**3-3*mass*angular_momentum**2/radius**4
    coordinate_velocity = metric*proper_velocity/energy
    tortoise_velocity = proper_velocity/energy
    coordinate_acceleration = metric*metric_prime*proper_velocity**2/energy**2+metric**2*proper_acceleration/energy**2
    tortoise_acceleration = metric*proper_acceleration/energy**2
    angular_velocity = metric*angular_momentum/(energy*radius**2)
    strength = (8*np.pi/3)*particle_mass*angular_momentum/radius**2*np.sqrt(15/(8*np.pi))*np.exp(-1j*phase)
    strength_dot = strength*(-2*coordinate_velocity/radius-1j*angular_velocity)
    jump = radius*strength/2
    jump_dot = jump*(-coordinate_velocity/radius-1j*angular_velocity)
    gap = 1-tortoise_velocity**2
    derivative_jump = -metric*jump/radius+1j*tortoise_velocity*angular_velocity*jump/gap
    time_jump = -1j*angular_velocity*jump/gap
    delta_prime = gap*jump
    delta = tortoise_acceleration*jump-metric*jump*(1+tortoise_velocity**2)/radius-1j*angular_velocity*tortoise_velocity*jump
    radial_delta_prime = radius*strength*(metric**2-coordinate_velocity**2)/2
    radial_delta = strength*(radius*coordinate_acceleration-coordinate_velocity**2-1j*radius*coordinate_velocity*angular_velocity-metric)/2
    time_metric_jump = (metric*jump+radius*derivative_jump)/2
    radial_metric_jump = radius*time_jump/(2*metric)
    return dict(anomaly=np.asarray(anomaly), time=time, phase=phase, proper_time=proper,
                radius=radius, metric=metric, metric_prime=metric_prime,
                time_anomaly=rates[0], proper_velocity=proper_velocity,
                proper_acceleration=proper_acceleration, coordinate_velocity=coordinate_velocity,
                coordinate_acceleration=coordinate_acceleration, tortoise_velocity=tortoise_velocity,
                tortoise_acceleration=tortoise_acceleration, angular_velocity=angular_velocity,
                strength=strength, strength_dot=strength_dot, jump=jump, jump_dot=jump_dot,
                derivative_jump=derivative_jump, time_jump=time_jump,
                delta=delta, delta_prime=delta_prime, radial_delta=radial_delta,
                radial_delta_prime=radial_delta_prime, time_metric_jump=time_metric_jump,
                radial_metric_jump=radial_metric_jump)


def independent_geodesic(mass, semilatus, eccentricity, samples, tolerance):
    energy, angular_momentum = orbit_constants(mass, semilatus, eccentricity)

    def equation(proper_time, state):
        radius, radial_velocity, time, phase = state
        metric = 1-2*mass/radius
        acceleration = -mass/radius**2+angular_momentum**2/radius**3-3*mass*angular_momentum**2/radius**4
        return [radial_velocity, acceleration, energy/metric, angular_momentum/radius**2]

    initial = [mass*semilatus/(1+eccentricity), 0., 0., 0.]
    duration = samples['proper_time'][-1]
    solution = solve_ivp(equation, (0., duration), initial, method='DOP853', rtol=tolerance,
                         atol=tolerance/100, t_eval=samples['proper_time'], max_step=duration/150)
    assert solution.success, solution.message
    return solution.y, solution.nfev


def radial_probe(radius, metric, reference_radius, kind):
    if kind == 'growing':
        return (radius/reference_radius)**3, 3*metric*radius**2/reference_radius**3
    if kind == 'decaying':
        return (reference_radius/radius)**2, -2*metric*reference_radius**2/radius**3
    raise ValueError(kind)
