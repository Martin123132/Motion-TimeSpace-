from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'eccentric-source-20261005'))
from eccentric_source import anomaly_solution, orbit_constants, source_samples


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save_report(directory, script, report):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(script), **report}
    with (directory/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def harmonic_value(azimuth):
    assert azimuth in [-2, 0, 2]
    return -np.sqrt(5/(16*np.pi)) if azimuth == 0 else np.sqrt(15/(32*np.pi))


def coefficients(samples, mass, energy, angular, azimuth, particle=1.):
    radius, velocity = samples['radius'], samples['coordinate_velocity']
    metric = 1-2*mass/radius
    metric_prime = 2*mass/radius**2
    small_lambda = 2+3*mass/radius
    large_lambda = 2*small_lambda
    lambda_prime = -3*mass/radius**2
    angular_speed = metric*angular/(energy*radius**2)
    strength = 8*np.pi*particle*energy/metric*harmonic_value(azimuth)*np.exp(-1j*azimuth*samples['phase'])
    trace = strength*(velocity**2/metric-metric)/radius**2
    trace_prime = strength*(-velocity**2*metric_prime/metric**2-metric_prime)/radius**2-2*trace/radius
    qrr = strength*velocity**2/radius**2
    qr = -1j*azimuth*strength*angular_speed*velocity/3
    qflat = strength*angular_speed**2
    qsharp = strength*radius**2*angular_speed**2*(3-azimuth**2)/6
    polynomial = 8+12*mass/radius+84*mass**2/radius**2
    raw_F = strength*metric*(metric**2-velocity**2)/(3*small_lambda)
    radial_F_prime = strength/(3*small_lambda)*(metric_prime*(3*metric**2-velocity**2)
                      -metric*(metric**2-velocity**2)*lambda_prime/small_lambda)
    raw_G = metric*(4*qr/large_lambda-qsharp/radius+(-2*radius**2*metric*trace_prime
                +24*mass*qrr/large_lambda+2*radius*metric*qflat+radius*polynomial*trace/large_lambda)/(3*large_lambda))
    canonical_G = raw_G-radial_F_prime
    delta_prime = raw_F/metric**2
    delta = canonical_G/metric+raw_F*metric_prime/metric**2
    tortoise_speed = velocity/metric
    acceleration = -metric*metric_prime/2+3*metric_prime*velocity**2/(2*metric)+metric*radius*angular_speed**2
    tortoise_acceleration = acceleration/metric-velocity**2*metric_prime/metric**2
    jump = strength*metric/(3*small_lambda)
    jump_rate = jump*(-1j*azimuth*angular_speed-lambda_prime*velocity/small_lambda)
    slope_jump = (delta-2*tortoise_speed*jump_rate-tortoise_acceleration*jump)/(1-tortoise_speed**2)
    temporal_jump = jump_rate-tortoise_speed*slope_jump
    effective = metric*(1+angular**2/radius**2)
    phase_strength = 8*np.pi*particle*harmonic_value(azimuth)*np.exp(-1j*azimuth*samples['phase'])
    martel_F = phase_strength/3*metric**2*effective/(small_lambda*energy)
    effective_prime = metric_prime*(1+angular**2/radius**2)-2*metric*angular**2/radius**3
    martel_F_prime = phase_strength/(3*energy*small_lambda)*(2*metric*metric_prime*effective
                           +metric**2*effective_prime-metric**2*effective*lambda_prime/small_lambda)
    martel_G = phase_strength/3*metric**2/(radius*small_lambda**2)*(6*mass/radius*energy
               -small_lambda/energy*(3-3*mass/radius+angular**2/radius**2*(5-7*mass/radius)))
    martel_G += -1j*azimuth*2*phase_strength/3*angular/energy*metric**2/(radius**2*small_lambda)*samples['proper_velocity']
    martel_G += phase_strength/3*angular**2/energy*metric**3/(radius**3*small_lambda)
    martel_G += -phase_strength/6*angular**2/energy*metric**2/radius**3*(3-azimuth**2)
    return dict(strength=strength, angular_speed=angular_speed, metric=metric, raw_F=raw_F, raw_G=raw_G,
                radial_F_prime=radial_F_prime, canonical_F=raw_F, canonical_G=canonical_G,
                delta=delta, delta_prime=delta_prime, jump=jump, jump_rate=jump_rate,
                slope_jump=slope_jump, temporal_jump=temporal_jump, tortoise_speed=tortoise_speed,
                tortoise_acceleration=tortoise_acceleration, martel_F=martel_F,
                martel_canonical_G=martel_G-martel_F_prime, acceleration=acceleration)


def potential(radius, mass):
    metric = 1-2*mass/radius
    return metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)


def vacuum_probes(mass, reference_radius, maximum_radius, frequency, tolerance):
    def equation(radius, state):
        metric = 1-2*mass/radius
        first, first_slope, second, second_slope = state
        coefficient = potential(radius, mass)-frequency**2
        return np.array([first_slope, coefficient*first, second_slope, coefficient*second])/metric
    solution = solve_ivp(equation, (reference_radius, maximum_radius*1.000001),
                        [1., 2/reference_radius, 1., -3/reference_radius], method='DOP853',
                        rtol=tolerance, atol=tolerance/100, max_step=reference_radius/5, dense_output=True)
    assert solution.success, solution.message
    return solution


def metric_and_boundary(samples, source, mass, frequency, master, slope):
    radius, velocity = samples['radius'], samples['coordinate_velocity']
    metric, angular_speed, strength = source['metric'], source['angular_speed'], source['strength']
    numerator = 6*radius**2+6*mass*radius+6*mass**2
    denominator = radius**2*(2*radius+3*mass)
    angular_coefficient = numerator/denominator
    coefficient_prime = ((12*radius+6*mass)*denominator-numerator*(6*radius**2+6*mass*radius))/denominator**2
    shift_coefficient = (2*radius**2-6*mass*radius-3*mass**2)/(radius*(radius-2*mass)*(2*radius+3*mass))
    angular_metric = angular_coefficient*master+slope
    angular_prime = coefficient_prime*master+angular_coefficient*slope/metric+(potential(radius, mass)-frequency**2)*master/metric
    lapse = (2+3*mass/radius)/metric*(3*master/radius-angular_metric)+radius*angular_prime
    shift_dual = 1j*frequency*radius*(shift_coefficient*master+slope/metric)
    contraction = (metric+velocity**2/metric)*lapse+2*velocity*shift_dual+radius**2*angular_speed**2*angular_metric
    strength_log_rate = source['jump_rate']/source['jump']-velocity*2*mass/(radius**2*metric)
    strength_log_rate += velocity*(-3*mass/radius**2)/(2+3*mass/radius)
    boundary = strength*radius*(source['tortoise_speed']*slope
                 +(1j*frequency-strength_log_rate-velocity/radius+2*velocity*shift_coefficient)*master)
    return contraction, boundary


def quadrature_nodes(order, panels, lower, upper):
    points, weights = leggauss(order)
    edges = np.linspace(lower, upper, panels+1)
    halfwidth = np.diff(edges)/2
    nodes = ((edges[:-1]+edges[1:])[:, None]/2+halfwidth[:, None]*points).ravel()
    return nodes, (halfwidth[:, None]*weights).ravel()
