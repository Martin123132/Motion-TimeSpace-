from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import time
import numpy as np
from scipy import sparse, linalg, integrate, special
from scipy.sparse import linalg as spla

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'angular-thermal-source-20261007'
THERMAL = BRANCH / 'thermal-recoil-and-spectral-response-20261007'
WAVES = BRANCH / 'coupled-finite-wave-evolution-20261007'
sys.path.insert(0, str(PARENT))
import angular_common as inherited
modest = inherited.modest
digest = inherited.digest
write_json = inherited.write_json
NATIVE = inherited.NATIVE
HISTORY = inherited.HISTORY
I3_PLANCK = inherited.I3_PLANCK


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'step_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


class AxisymmetricMaps:
    def __init__(self, polar=10):
        self.polar = polar
        self.azimuthal = 2 * (polar + 2)
        self.kernel = inherited.AngularKernel(polar, self.azimuthal)
        self.cosine, weights = np.polynomial.legendre.leggauss(polar)
        self.weights = weights / 2
        directions = self.kernel.directions
        cosine = directions[:, 2]
        sine = np.sqrt(1 - cosine ** 2)
        meridian = np.column_stack([cosine * directions[:, 0] / sine,
                                   cosine * directions[:, 1] / sine, -sine])
        azimuth = np.column_stack([-directions[:, 1] / sine, directions[:, 0] / sine, np.zeros(len(sine))])
        self.polarization = np.einsum('ni,nj->nij', meridian, meridian) - np.einsum('ni,nj->nij', azimuth, azimuth)
        self.dimension = 2 * polar
        self.scalar = np.r_[np.ones(polar), np.zeros(polar)]
        self.flow = np.r_[self.cosine, np.zeros(polar)]
        self.number = np.r_[self.weights, np.zeros(polar)]
        self.flux = np.r_[self.weights * self.cosine, np.zeros(polar)]
        self.metric = np.r_[self.weights, self.weights] / 2
        basis = self.lift(np.eye(self.dimension))
        self.scatter = self.lower(self.kernel.scatter(basis)).T.real
        self.recoil = self.lower(self.kernel.recoil_angular(basis)).T.real
        self.thermal = self.lower(self.kernel.thermal_angular(basis)).T.real
        for matrix in [self.scatter, self.recoil, self.thermal]:
            matrix[abs(matrix) < 1e-15] = 0

    def lift(self, values):
        intensity = np.repeat(values[..., :self.polar], self.azimuthal, axis=-1)
        polarization = np.repeat(values[..., self.polar:], self.azimuthal, axis=-1)
        return .5 * (intensity[..., None, None] * self.kernel.projector
                     + polarization[..., None, None] * self.polarization)

    def lower(self, values):
        intensity = np.trace(values, axis1=-2, axis2=-1)
        polarization = np.einsum('nij,...nij->...n', self.polarization, values)
        shape = intensity.shape[:-1] + (self.polar, self.azimuthal)
        return np.concatenate([intensity.reshape(shape).mean(axis=-1),
                               polarization.reshape(shape).mean(axis=-1)], axis=-1)


class CollisionStep:
    def __init__(self, points, polar, theta, heat_capacity, inertia, minimum=1e-3, maximum=30.):
        self.grid = inherited.inherited.SpectralGrid(points, minimum, maximum)
        self.angular = AxisymmetricMaps(polar)
        self.points, self.theta = points, theta
        self.heat_capacity, self.inertia = heat_capacity, inertia
        self.dimension = self.angular.dimension
        self.size = points * self.dimension
        self.diffusion = sparse.diags([self.grid.lower, self.grid.diagonal, self.grid.upper], [-1, 0, 1], format='csc')
        frequency = self.grid.frequency
        occupation = inherited.inherited.planck(frequency)
        weight = occupation * (1 + occupation)
        local = 2 * frequency * (1 + 2 * occupation) - 2 * frequency ** 2 * weight
        identity = sparse.eye(self.dimension, format='csc')
        angular_scatter = sparse.csc_matrix(self.angular.scatter)
        angular_recoil = sparse.csc_matrix(self.angular.recoil)
        angular_thermal = sparse.csc_matrix(self.angular.thermal)
        self.photon = (sparse.kron(sparse.eye(points), angular_scatter - identity, format='csc')
                       + theta * (sparse.kron(self.diffusion, angular_recoil, format='csc')
                         + sparse.kron(sparse.eye(points), angular_thermal + 2 * angular_recoil, format='csc')
                         + sparse.kron(sparse.diags(local), identity - angular_recoil, format='csc')))
        self.temperature_equilibrium = np.kron(2 * frequency, self.angular.scalar)
        self.velocity_equilibrium = np.kron(2 * frequency, self.angular.flow)
        self.chemical_equilibrium = np.kron(np.ones(points), self.angular.scalar)
        self.temperature_column = np.kron(2 * theta * self.grid.temperature_source, self.angular.scalar)
        self.velocity_column = -(self.photon @ self.velocity_equilibrium)
        self.number = np.kron(self.grid.mass, self.angular.number) / (2 * I3_PLANCK)
        self.energy = np.kron(self.grid.mass * frequency, self.angular.number) / (2 * I3_PLANCK)
        self.flux = np.kron(self.grid.mass * frequency, self.angular.flux) / (2 * I3_PLANCK)
        self.entropy_metric = np.kron(self.grid.mass, self.angular.metric) / (2 * I3_PLANCK)
        self.cached_alpha = None
        self.cached_factors = None

    def source(self, potential, temperature, velocity):
        return self.photon @ potential + self.temperature_column * temperature + self.velocity_column * velocity

    def invariants(self, potential, temperature, velocity):
        return np.array([self.number @ potential, self.energy @ potential + self.heat_capacity * temperature,
                         self.flux @ potential + self.inertia * velocity])

    def entropy(self, potential, temperature, velocity):
        return .5 * (np.vdot(potential, self.entropy_metric * potential).real
                     + self.heat_capacity * abs(temperature) ** 2 + self.inertia * abs(velocity) ** 2)

    def symmetric_photon(self):
        scale = np.sqrt(self.entropy_metric)
        return sparse.diags(scale) @ self.photon @ sparse.diags(1 / scale)

    def solve(self, alpha, history, temperature_history, velocity_history):
        if self.cached_alpha != alpha:
            factor = spla.splu((alpha * sparse.eye(self.size, format='csc') - self.photon).astype(complex))
            temperature_response = factor.solve(self.temperature_column.astype(complex))
            velocity_response = factor.solve(self.velocity_column.astype(complex))
            schur = np.array([[self.heat_capacity + self.energy @ temperature_response, self.energy @ velocity_response],
                              [self.flux @ temperature_response, self.inertia + self.flux @ velocity_response]])
            self.cached_factors = factor, temperature_response, velocity_response, schur
            self.cached_alpha = alpha
        factor, temperature_response, velocity_response, schur = self.cached_factors
        particular = factor.solve(history.astype(complex))
        right = np.array([(self.heat_capacity * temperature_history + self.energy @ history) / alpha - self.energy @ particular,
                          (self.inertia * velocity_history + self.flux @ history) / alpha - self.flux @ particular])
        temperature, velocity = np.linalg.solve(schur, right)
        potential = particular + temperature * temperature_response + velocity * velocity_response
        return potential, temperature, velocity
