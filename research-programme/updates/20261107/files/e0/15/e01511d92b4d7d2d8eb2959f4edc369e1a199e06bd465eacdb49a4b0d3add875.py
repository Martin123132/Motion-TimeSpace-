from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import PPoly
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'transient-energy-20261006'
TANGENT = BRANCH/'surface-susceptibility-20261006'
sys.path.insert(0, str(TANGENT))
from susceptibility import Profile, TangentProblem, digest, read_json, write_json, modest_process
from dynamic_system import edge_state, vacuum_data


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.update([PARENT/'results/stage-integrity.json', TANGENT/'results/tangent/status.json'])
    return {str(path):digest(path) for path in sorted(paths)}


def save(name, script, report):
    directory = ROOT/'results'/name
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


class Interior:
    def __init__(self, label):
        parent = read_json(TANGENT/'results/tangent/status.json')
        self.row = next(row for row in parent['rows'] if row['label'] == label)
        self.archive_path = TANGENT/'results/tangent'/(label+'.npz')
        with np.load(self.archive_path) as data:
            self.spline = PPoly.construct_fast(data['spline_coefficients'], data['spline_knots'], axis=1)
            self.parameters = data['parameters']
            self.scales = data['scales']
        self.profile = Profile(20., .03)
        self.problem = TangentProblem(self.profile, self.row['distance'], self.row['tolerance']).base
        self.radius, self.mass = self.problem.radius, self.problem.mass
        self.alpha, self.frequency = self.profile.alpha, self.profile.frequency
        self.master_surface = self.row['static_master'][0]

    def fields(self, position):
        position = np.asarray(position)
        scaled = self.spline(position/self.radius)
        state = scaled[:6]*self.scales[:, None]
        edge = position > self.radius-self.row['distance']
        for index in np.flatnonzero(edge):
            amplitude, phase0, angular, shift = self.parameters[:4]*self.problem.parameter_scales
            state[:, index] = edge_state(self.radius, self.mass, self.frequency, 0.,
                self.radius-position[index], amplitude, phase0, np.array([angular, shift]))
        flow, metric_time, metric_time_prime = self.problem.physical_evolution(position, state)
        field, gradient, metric, lapse2, energy, energy_prime, energy_second, rotation, lapse_prime, first = self.problem.background(position)
        metric_prime = 2*metric*(first-2/position-lapse_prime)
        return state, flow, metric_time, (field, gradient, metric, np.sqrt(lapse2), metric_prime)

    def density(self, position):
        state, flow, metric_time, background = self.fields(position)
        angular, shift, response, response_prime, phase, phase_prime = state
        field, gradient, metric, lapse, metric_prime = background
        first = metric_time-2*metric*flow[1]-metric_prime*shift
        second = angular-2*metric*shift/position
        measure = position**2/(lapse*np.sqrt(metric))
        gravity = measure/(8*self.alpha)*(-4*first*second-2*second**2+12*metric*shift**2/position**2)
        amplitude = measure*(response-metric*shift*gradient)**2
        phase_cross = measure*2*self.frequency*phase*(2*field*response+field**2*(metric_time+angular))
        shift_cross = measure*2*self.frequency*metric*shift*field**2*phase_prime
        phase_gradient = -measure*lapse**2*field**2*(metric*phase_prime**2+6*phase**2/position**2)
        return np.array([gravity, amplitude, phase_cross, shift_cross, phase_gradient])

    def integral(self, order=48, cells=80):
        nodes, weights = leggauss(order)
        lower = self.problem.lower*self.radius
        edges = np.unique(np.r_[np.linspace(lower, self.radius-self.row['distance'], cells+1), self.radius])
        positions = ((edges[1:]+edges[:-1])[:, None]/2+np.diff(edges)[:, None]*nodes/2).ravel()
        factors = (np.diff(edges)[:, None]*weights/2).ravel()
        return self.density(positions)@factors

