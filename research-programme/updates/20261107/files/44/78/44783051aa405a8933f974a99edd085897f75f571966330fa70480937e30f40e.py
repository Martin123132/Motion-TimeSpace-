from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'finite-mass-tidal-balance-20261006'
sys.path.insert(0, str(PARENT))
from balance import digest, read_json, write_json, modest_process


def save(name, script, report):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(), script_sha256=digest(script), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def dependencies():
    paths = [ROOT/'inspiral.py', PARENT/'balance.py', PARENT/'results/stage-integrity.json',
             PARENT/'results/chirp/status.json', PARENT/'results/derivation/status.json']
    return {str(path):digest(path) for path in paths}


def coefficients(mass_ratio):
    eccentric = 157/24
    circular_tide = 6+72*mass_ratio
    eccentric_tide = 837/4+20721*mass_ratio/16
    gamma_tide = 459/19+8547*mass_ratio/76
    transport = 23/2+205*mass_ratio/8
    mixed = 2*eccentric*circular_tide-eccentric_tide+eccentric*transport
    return dict(eccentric=eccentric, circular_tide=circular_tide, eccentric_tide=eccentric_tide,
                gamma_tide=gamma_tide, transport=transport, mixed=mixed, power=19/6)


def power_integral(exponent, ratio):
    return np.expm1((exponent+1)*np.log(ratio))/(exponent+1)


def analytic_coefficients(mass_ratio, ratio):
    constants = coefficients(mass_ratio)
    eccentric, tide, transport, mixed, power = [constants[key] for key in
                                               ['eccentric', 'circular_tide', 'transport', 'mixed', 'power']]
    zero_transport = ratio**power
    tide_transport = -transport*np.expm1(-5*np.log(ratio))*zero_transport
    result = [zero_transport, tide_transport]
    for exponent in [3., 1.5]:
        result.extend([-power_integral(exponent, ratio),
                       eccentric*power_integral(exponent+power, ratio),
                       tide*power_integral(exponent-5, ratio),
                       -mixed*power_integral(exponent+power-5, ratio)
                       +eccentric*transport*power_integral(exponent+power, ratio)])
    return np.array(result, dtype=float)


def variational_solution(mass_ratio, final_ratio, tolerance=3e-13):
    constants = coefficients(mass_ratio)
    eccentric, tide, mixed_source, gamma, power = [constants[key] for key in
                 ['eccentric', 'circular_tide', 'eccentric_tide', 'gamma_tide', 'power']]

    def derivative(ratio, state):
        zero, response = state[:2]
        values = [power*zero/ratio, power*response/ratio+power*(gamma-tide)*zero/ratio**6]
        for exponent in [3., 1.5]:
            values.extend([-ratio**exponent, eccentric*ratio**exponent*zero,
                tide*ratio**(exponent-5), eccentric*ratio**exponent*response
                                          -(2*eccentric*tide-mixed_source)*ratio**(exponent-5)*zero])
        return values

    solution = solve_ivp(derivative, (1., final_ratio), [1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                         method='DOP853', rtol=tolerance, atol=tolerance*.1, dense_output=True)
    assert solution.success
    return solution


def resummed_control(mass_ratio, final_ratio, initial_z, initial_tide, tolerance=3e-13):
    constants = coefficients(mass_ratio)

    def derivative(ratio, state):
        squared = state[0]
        tide = initial_tide/ratio**5
        factor = 1+constants['eccentric']*squared+constants['circular_tide']*tide+constants['eccentric_tide']*tide*squared
        assert factor > 0
        return [constants['power']*squared/ratio*(1+constants['gamma_tide']*tide)/factor,
                -ratio**3/factor, -ratio**1.5/factor]

    solution = solve_ivp(derivative, (1., final_ratio), [initial_z, 0., 0.],
                         method='DOP853', rtol=tolerance, atol=tolerance*.01, dense_output=True)
    assert solution.success
    return solution


def normalized_endpoint(mass_ratio, final_ratio, initial_z, initial_tide):
    values = analytic_coefficients(mass_ratio, final_ratio)
    weights = np.array([1., initial_z, initial_tide, initial_z*initial_tide])
    return np.array([initial_z*(values[0]+initial_tide*values[1]),
                     values[2:6]@weights, values[6:10]@weights])


def physical_row(mass, radius, deformability, mass_ratio, initial_z, outer, ratio):
    assert mass_ratio > 0 and 0 < ratio <= 1 and initial_z >= 0 and deformability >= 0
    companion = mass*mass_ratio
    total_mass = mass+companion
    reduced = mass*companion/total_mass
    symmetric_ratio = reduced/total_mass
    initial_distance = outer*radius
    initial_tide = deformability/initial_distance**5
    initial_x = initial_distance/total_mass
    vector = analytic_coefficients(mass_ratio, ratio)
    weights = np.array([1., initial_z, initial_tide, initial_z*initial_tide])
    clock_parts = vector[2:6]*weights*(5/64)*initial_x**4
    phase_parts = vector[6:10]*weights*(5/64)*initial_x**2.5
    point_time, difference_time = float(sum(clock_parts[:2])), float(sum(clock_parts[2:]))
    point_phase, difference_phase = float(sum(phase_parts[:2])), float(sum(phase_parts[2:]))
    point_z = initial_z*vector[0]
    difference_z = initial_z*initial_tide*vector[1]
    fractional_z = float(initial_tide*vector[1]/vector[0])
    frequency = np.sqrt(total_mass/(initial_distance*ratio)**3)
    return dict(mass_ratio=mass_ratio, symmetric_mass_ratio=symmetric_ratio, initial_z=initial_z,
                frequency_radius_over_R=outer*ratio, initial_frequency_radius_over_R=outer,
                frequency=frequency, initial_tide=initial_tide, local_tide=initial_tide/ratio**5,
                scaled_time_point=point_time, scaled_time_body=point_time+difference_time,
                scaled_time_difference=difference_time, scaled_phase_point=point_phase,
                scaled_phase_body=point_phase+difference_phase, scaled_phase_difference=difference_phase,
                fractional_time_difference=difference_time/point_time if ratio < 1 else 0.,
                fractional_phase_difference=difference_phase/point_phase if ratio < 1 else 0.,
                clock_circular_point=float(clock_parts[0]), clock_point_eccentricity=float(clock_parts[1]),
                clock_circular_tide=float(clock_parts[2]), clock_mixed=float(clock_parts[3]),
                phase_circular_point=float(phase_parts[0]), phase_point_eccentricity=float(phase_parts[1]),
                phase_circular_tide=float(phase_parts[2]), phase_mixed=float(phase_parts[3]),
                z_point=float(point_z), z_body=float(point_z+difference_z), z_difference=float(difference_z),
                fractional_z_difference=fractional_z,
                action_eccentricity_amplitude_fractional_change=fractional_z/2 if initial_z > 0 else None,
                geometric_time_point=point_time*total_mass**2/reduced,
                geometric_time_difference=difference_time*total_mass**2/reduced,
                orbital_phase_point=point_phase/symmetric_ratio,
                orbital_phase_difference=difference_phase/symmetric_ratio,
                dominant_m2_carrier_phase_difference=2*difference_phase/symmetric_ratio,
                central_weak_field_parameter=total_mass/(initial_distance*ratio))
