from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial import Chebyshev

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH/'postcircular-clock-20261005'
PRIOR = BRANCH/'near-circular-quadrupole-20261005'
sys.path.insert(0, str(PARENT))
from carrier import numerical_geometry, orbit_series, complex_value, digest, read_json, write_json, modest_process
from sidebands import AnalyticWave, orbit_constants, polar_vacuum
from polar_radiation import coefficients, metric_and_boundary, quadrature_nodes, anomaly_solution, source_samples
from secular import geometry


def save(directory, script, report):
    directory = ROOT/'results'/directory
    directory.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', script_sha256=digest(script), time_utc=datetime.now(timezone.utc).isoformat(), **report)
    write_json(directory/'status.json', report, exclusive=True)
    (directory/'COMPLETE').write_text(report['time_utc']+'\n', encoding='utf-8')
    return report


def dependencies():
    paths = {Path(module.__file__).resolve() for module in list(sys.modules.values())
             if getattr(module, '__file__', None) and Path(module.__file__).suffix == '.py'
             and BRANCH in Path(module.__file__).resolve().parents}
    paths.add(PARENT/'results/stage-integrity.json')
    return {str(path): digest(path) for path in sorted(paths)}


def carrier_action(rows, step=.0005):
    lookup = {row['fractional_frequency_shift']: row for row in rows}
    center = lookup[0.]
    derivative = (complex_value(lookup[-2*step], 'action')-8*complex_value(lookup[-step], 'action')
                  +8*complex_value(lookup[step], 'action')-complex_value(lookup[2*step], 'action'))/(12*step)
    geometric = -3/(8*np.pi)*(complex_value(center, 'difference_coefficient', 1)*complex_value(center, 'outgoing_source')
                            +complex_value(center, 'difference_coefficient')*complex_value(center, 'outgoing_source', 1))
    frequency_term = orbit_series(center['semilatus'])['angular_frequency_fraction']*derivative
    return dict(action0=complex_value(center, 'action').real, action2=(geometric+frequency_term).real,
                geometric2=geometric.real, frequency2=frequency_term.real)


def static_law(mass, semilatus, tidal_lambda):
    energy, angular = orbit_constants(mass, semilatus, 0.)
    harmonic_value = -np.sqrt(5/(16*np.pi))
    values = numerical_geometry('polar')(mass*semilatus, mass, energy, angular, 0, 0., harmonic_value)
    basis = polar_vacuum.static_master_basis(mass*semilatus, mass, 1.).real
    overlap0, overlap2 = np.asarray(values[:4], dtype=float).reshape(2, 2)@basis[:, 1]
    factor = -9*tidal_lambda/(16*np.pi*np.linalg.det(basis))
    return dict(action0=float(factor*overlap0**2), action2=float(2*factor*overlap0*overlap2),
                overlap0=float(overlap0), overlap2=float(overlap2), wronskian=float(np.linalg.det(basis)))


def finite_static(mass, semilatus, eccentricity, tidal_lambda, order=32, panels=24):
    trajectory = anomaly_solution(mass, semilatus, eccentricity, 3e-13)
    period = 2*trajectory.sol(np.pi)[0]
    anomaly, weights = quadrature_nodes(order, panels*2, 0., 2*np.pi)
    samples = source_samples(anomaly, trajectory, mass, semilatus, eccentricity)
    energy, angular = orbit_constants(mass, semilatus, eccentricity)
    source = coefficients(samples, mass, energy, angular, 0)
    basis = np.array([polar_vacuum.static_master_basis(float(position), mass, 1.) for position in samples['radius']]).real
    master, slope = basis[:, :, 1].T
    normalized = weights*samples['time_anomaly']/period
    overlap = np.dot(normalized, source['delta']*master-source['delta_prime']*slope)
    contraction, boundary = metric_and_boundary(samples, source, mass, 0., master, slope)
    metric_overlap = np.dot(normalized, -source['strength']*contraction/6)
    wronskians = np.linalg.det(basis)
    action = -9*tidal_lambda/(16*np.pi*wronskians[0])*overlap**2
    report = dict(eccentricity=eccentricity, action=float(action.real), overlap=float(overlap.real),
                  imaginary_overlap=float(abs(overlap.imag)), normalized_weight_error=float(abs(sum(normalized)-1)),
                  metric_reciprocity_error=float(abs(metric_overlap/overlap-1)),
                  wronskian_error=float(max(abs(wronskians/wronskians[0]-1))))
    archive = dict(anomaly=anomaly, weights=normalized, radius=samples['radius'], decaying_master=master,
                   decaying_slope=slope, source_delta=source['delta'], source_delta_prime=source['delta_prime'])
    return report, archive


class ActionCurve:
    def __init__(self, rows, component='total'):
        self.rows = sorted(rows, key=lambda row: row['separation'])
        self.mass = self.rows[0]['mass']
        self.radius = self.rows[0]['radius']
        self.tidal_lambda = self.rows[0]['tidal_lambda']
        self.component = component
        self.polynomial = Chebyshev.fit([row['separation'] for row in self.rows],
            [row[component+'0']/self.normal(row['separation']) for row in self.rows], len(rows)-1, domain=[5., 10.])

    def normal(self, separation):
        return 1.5*self.tidal_lambda/(separation*self.radius)**6

    def derivative_p(self, separation):
        normal = self.normal(separation)
        return float(normal*(self.polynomial.deriv()(separation)-6*self.polynomial(separation)/separation)*self.mass/self.radius)

    def frequency_law(self, row):
        semilatus = row['semilatus']
        state = geometry(self.mass, semilatus, 0.)
        action_coefficient = self.mass*semilatus**1.5*np.sqrt(semilatus-6)/(2*(semilatus-2)*np.sqrt(semilatus-3))
        derivative = self.derivative_p(row['separation'])
        angular2 = state['angular_z']
        angular_shift = -derivative/state['angular_p']
        radial_shift = -(row[self.component+'2']-angular2*derivative/state['angular_p'])/action_coefficient
        angular_frequency = 1/(self.mass*semilatus**1.5)
        radial_frequency = angular_frequency*np.sqrt(1-6/semilatus)
        angular_prime = -1.5*angular_frequency/semilatus
        radial_prime = radial_frequency*(-1.5/semilatus+3/(semilatus*(semilatus-6)))
        fixed_frequency_radial = radial_shift-radial_prime/angular_prime*angular_shift
        return dict(separation=row['separation'], component=self.component, action0=row[self.component+'0'],
                    action2=row[self.component+'2'], action0_prime=derivative,
                    delta_Omega_phi_per_mu_fixed_actions=angular_shift,
                    delta_Omega_r_per_mu_fixed_actions=radial_shift,
                    delta_K_over_K_per_eta_fixed_actions=self.mass*(angular_shift/angular_frequency-radial_shift/radial_frequency),
                    delta_K_over_K_per_eta_fixed_Omega_phi=-self.mass*fixed_frequency_radial/radial_frequency,
                    delta_energy_per_mu_squared_fixed_Omega_phi=angular_frequency*derivative/angular_prime-row[self.component+'0'],
                    delta_angular_per_mu_squared_fixed_Omega_phi=derivative/angular_prime,
                    delta_energy_per_mu_squared_fixed_actions=-row[self.component+'0'],
                    weak_precession_per_eta=22.5*self.tidal_lambda/(self.mass*semilatus)**5,
                    Omega_phi=angular_frequency, Omega_r=radial_frequency, K0=angular_frequency/radial_frequency)
