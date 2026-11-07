from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.integrate import quad


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'eccentric-radiation-20261005'
sys.path.insert(0, str(BRANCH/'eccentric-source-20261005'))
from eccentric_source import anomaly_rates


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
    directory.mkdir(parents=True, exist_ok=True)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(script), **report}
    with (directory/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def geometry(mass, semilatus, squared_eccentricity):
    assert mass > 0 and 0 <= squared_eccentricity < 1
    assert semilatus > 6+2*np.sqrt(squared_eccentricity)
    denominator = semilatus-3-squared_eccentricity
    numerator = (semilatus-2)**2-4*squared_eccentricity
    energy = np.sqrt(numerator/(semilatus*denominator))
    angular = mass*semilatus/np.sqrt(denominator)
    energy_p = (2*(semilatus-2)*semilatus*denominator-numerator*(denominator+semilatus))
    energy_p /= 2*energy*(semilatus*denominator)**2
    energy_z = (semilatus-4)**2/(2*energy*semilatus*denominator**2)
    angular_p = mass*(semilatus-6-2*squared_eccentricity)/(2*denominator**1.5)
    angular_z = mass*semilatus/(2*denominator**1.5)
    determinant = -mass*((semilatus-6)**2-4*squared_eccentricity)/(4*energy*semilatus*denominator**2.5)
    return dict(energy=energy, angular=angular, energy_p=energy_p, energy_z=energy_z,
                angular_p=angular_p, angular_z=angular_z, determinant=determinant)


def radial_action(mass, semilatus, squared_eccentricity):
    eccentricity = np.sqrt(squared_eccentricity)
    denominator = semilatus-3-squared_eccentricity

    def integrand(anomaly):
        cosine = np.cos(anomaly)
        return (np.sin(anomaly)**2*np.sqrt(semilatus-6-2*eccentricity*cosine)
                /((semilatus-2-2*eccentricity*cosine)*(1+eccentricity*cosine)**2))

    integral, error = quad(integrand, 0, np.pi, epsabs=1e-13, epsrel=1e-13)
    prefactor = mass*semilatus**1.5*squared_eccentricity/(np.pi*np.sqrt(denominator))
    return float(prefactor*integral), float(prefactor*error)


def frequencies(mass, semilatus, eccentricity):
    period = 2*quad(lambda anomaly: anomaly_rates(anomaly, mass, semilatus, eccentricity)[0],
                    0, np.pi, epsabs=1e-10, epsrel=1e-13)[0]
    phase = 2*quad(lambda anomaly: anomaly_rates(anomaly, mass, semilatus, eccentricity)[1],
                   0, np.pi, epsabs=1e-13, epsrel=1e-13)[0]
    return float(2*np.pi/period), float(phase/period)


def power_for(row, channel):
    if channel == 'body':
        return row['body_infinity_energy']
    if channel == 'BH':
        return row['BH_infinity_energy']+row['BH_horizon_energy']
    if channel == 'difference':
        return row['difference_total_energy']
    raise ValueError(channel)


def rates(orbit, rows, channel):
    mass, semilatus, eccentricity = orbit['mass'], orbit['semilatus'], orbit['eccentricity']
    radial_frequency = 2*np.pi/orbit['period']
    angular_frequency = orbit['phase_advance']/orbit['period']
    state = geometry(mass, semilatus, eccentricity**2)
    power = math.fsum(power_for(row, channel) for row in rows)
    angular_loss = math.fsum(power_for(row, channel)/row['frequency'] for row in rows)
    radial_loss = math.fsum(row['harmonic']*power_for(row, channel)/row['frequency'] for row in rows)
    action_p = (state['energy_p']-angular_frequency*state['angular_p'])/radial_frequency
    action_z = (state['energy_z']-angular_frequency*state['angular_z'])/radial_frequency
    if eccentricity == 0:
        action_p = 0.
        action_z = mass*semilatus**1.5*np.sqrt(semilatus-6)/(2*(semilatus-2)*np.sqrt(semilatus-3))
    action_det = -state['determinant']/radial_frequency
    radial_rate, angular_rate = -radial_loss, -angular_loss
    semilatus_rate = (angular_rate*action_z-state['angular_z']*radial_rate)/action_det
    squared_rate = (state['angular_p']*radial_rate-angular_rate*action_p)/action_det
    energy_rate = -power
    direct_p = (energy_rate*state['angular_z']-state['energy_z']*angular_rate)/state['determinant']
    direct_z = (state['energy_p']*angular_rate-energy_rate*state['angular_p'])/state['determinant']
    action, action_error = radial_action(mass, semilatus, eccentricity**2)
    return {'eccentricity': eccentricity, 'semilatus': semilatus, 'channel': channel,
            'mass': mass, 'radius': orbit['radius'], 'specific_energy': state['energy'],
            'specific_angular_action': state['angular'], 'specific_radial_action': action,
            'radial_action_quadrature_error_estimate': action_error,
            'Omega_r': radial_frequency, 'Omega_phi': angular_frequency,
            'energy_rate_per_mu': energy_rate, 'angular_rate_per_mu': angular_rate,
            'radial_action_rate_per_mu': radial_rate, 'semilatus_rate_per_mu': semilatus_rate,
            'squared_eccentricity_rate_per_mu': squared_rate,
            'eccentricity_rate_per_mu': squared_rate/(2*eccentricity) if eccentricity else 0.,
            'fractional_squared_eccentricity_rate_per_mu': squared_rate/eccentricity**2 if eccentricity else None,
            'direct_energy_angular_semilatus_rate': direct_p, 'direct_energy_angular_squared_rate': direct_z,
            'action_p': action_p, 'action_z': action_z, 'action_determinant': action_det,
            'energy_angular_determinant': state['determinant'],
            'radial_loss_absolute_sum': math.fsum(abs(row['harmonic']*power_for(row, channel)/row['frequency']) for row in rows),
            'energy_angular_cancellation_radial_rate': -(power-angular_frequency*angular_loss)/radial_frequency,
            'optical_radial_difference_rate': -math.fsum(2*row['harmonic']*row['retarded_action_imag'] for row in rows)
                if channel == 'difference' else None,
            'mode_count': len(rows)}
