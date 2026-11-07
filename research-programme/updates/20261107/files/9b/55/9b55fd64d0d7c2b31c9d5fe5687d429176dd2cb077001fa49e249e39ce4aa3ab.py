from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'conservative-eccentric-action-20261005'


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, report, exclusive=False):
    with Path(path).open('x' if exclusive else 'w', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)


def save(name, script, report):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(), script_sha256=digest(script), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def input_hashes():
    return {str(path):digest(path) for path in [ROOT/'balance.py', PARENT/'results/stage-integrity.json']}


def circular_radius(conservative):
    return brentq(lambda radius:radius+6*conservative/radius**4-1, .95, 1.05, xtol=5e-15)


def scalar_flux(radius, velocity, conservative, induced):
    radial_force = radius**-3-radius**-2-6*conservative*radius**-7
    force_prime = -3*radius**-4+2*radius**-3+42*conservative*radius**-8
    amplitude = radius**2+induced*radius**-3
    amplitude_r = 2*radius-3*induced*radius**-4
    amplitude_rr = 2+12*induced*radius**-5
    amplitude_rrr = -60*induced*radius**-6
    amplitude_first = amplitude_r*velocity
    amplitude_second = amplitude_rr*velocity**2+amplitude_r*radial_force
    amplitude_third = amplitude_rrr*velocity**3+3*amplitude_rr*velocity*radial_force+amplitude_r*force_prime*velocity
    phase_first = 2/radius**2
    phase_second = -4*velocity/radius**3
    phase_third = -4*radial_force/radius**3+12*velocity**2/radius**4
    rotating_second = complex(amplitude_second-phase_first**2*amplitude,
                              2*phase_first*amplitude_first+phase_second*amplitude)
    rotating_third = complex(amplitude_third-3*phase_first**2*amplitude_first-3*phase_first*phase_second*amplitude,
        3*phase_first*amplitude_second+3*phase_second*amplitude_first+phase_third*amplitude-phase_first**3*amplitude)
    power = amplitude_third**2/30+abs(rotating_third)**2/10
    torque = (rotating_second.conjugate()*rotating_third).imag/5
    return np.array([power, torque])/(32/5)


def orbit_average(conservative, induced, amplitude, tolerance):
    center = circular_radius(conservative)
    periapsis = center*(1-amplitude)

    def derivative(time, state):
        radius, velocity = state[:2]
        force = radius**-3-radius**-2-6*conservative*radius**-7
        power, torque = scalar_flux(radius, velocity, conservative, induced)
        return [velocity, force, power, torque, velocity**2, radius**-2,
                radius-center, (radius-center)**2]

    def apocenter(time, state):
        return state[1]

    apocenter.direction = -1
    apocenter.terminal = True
    solution = solve_ivp(derivative, (0., 5.), [periapsis, 0., 0., 0., 0., 0., 0., 0.],
                         method='DOP853', rtol=tolerance, atol=tolerance*.01,
                         events=apocenter, dense_output=True, max_step=.12)
    assert solution.success and len(solution.t_events[0]) == 1
    half_period = float(solution.t_events[0][0])
    state = solution.y_events[0][0]
    action = float(state[4]/np.pi)
    sample_times = np.linspace(0., half_period, 129)
    samples = solution.sol(sample_times)
    energies = samples[1]**2/2+1/(2*samples[0]**2)-1/samples[0]-conservative/samples[0]**6
    row = dict(conservative=conservative, induced=induced, radial_amplitude=amplitude,
        circular_radius=center, half_period=half_period, specific_radial_action=action, z=2*action,
        energy_flux_ratio=float(state[2]/half_period), angular_flux_ratio=float(state[3]/half_period),
        circular_energy_flux_ratio=float(scalar_flux(center, 0., conservative, induced)[0]),
        circular_angular_flux_ratio=float(scalar_flux(center, 0., conservative, induced)[1]),
        Omega_r=float(np.pi/half_period), Omega_phi=float(state[5]/half_period),
        mean_radial_offset=float(state[6]/half_period), mean_offset_squared=float(state[7]/half_period),
        mean_radial_velocity_squared=float(state[4]/half_period),
        energy_conservation_error=float(np.max(abs(energies-energies[0]))),
        apocenter_velocity_residual=float(abs(state[1])), function_evaluations=solution.nfev)
    archive = dict(time=sample_times, state=samples, energy=energies, solver_times=solution.t, solver_states=solution.y)
    return row, archive
