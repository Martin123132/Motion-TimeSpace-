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
import itertools
import numpy as np
from scipy import integrate, special

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'thermal-recoil-and-spectral-response-20261007'
WAVES = BRANCH / 'coupled-finite-wave-evolution-20261007'
sys.path.insert(0, str(PARENT))
import thermal_common as inherited
modest = inherited.modest
digest = inherited.digest
write_json = inherited.write_json
NATIVE = inherited.NATIVE
HISTORY = inherited.HISTORY
I3_PLANCK = inherited.I3_PLANCK


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'angular_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def epsilon_tensor():
    result = np.zeros((3, 3, 3))
    for permutation in itertools.permutations(range(3)):
        inversions = sum(permutation[left] > permutation[right] for left in range(3) for right in range(left + 1, 3))
        result[permutation] = (-1) ** inversions
    return result


EPSILON = epsilon_tensor()


def screen(directions):
    return np.eye(3) - np.einsum('...i,...j->...ij', directions, directions)


def transverse_traceless(matrix, projector):
    projected = projector @ matrix @ projector
    return projected - .5 * np.trace(projected, axis1=-2, axis2=-1)[..., None, None] * projector


def stf3(tensor):
    symmetric = sum(tensor.transpose(tuple(range(tensor.ndim - 3)) + tuple(tensor.ndim - 3 + axis for axis in permutation))
                    for permutation in itertools.permutations(range(3))) / 6
    trace = np.einsum('...iik->...k', symmetric)
    identity = np.eye(3)
    return symmetric - (np.einsum('ij,...k->...ijk', identity, trace)
                        + np.einsum('ik,...j->...ijk', identity, trace)
                        + np.einsum('jk,...i->...ijk', identity, trace)) / 5


class AngularKernel:
    def __init__(self, polar=10, azimuthal=20):
        self.directions, self.weights = inherited.inherited.collision.angular_grid(polar, azimuthal)
        self.projector = screen(self.directions)
        self.epsilon = np.einsum('ijk,nk->nij', EPSILON, self.directions)
        self.count = len(self.weights)

    def average(self, values):
        return np.einsum('n,...nij->...ij', self.weights, values)

    def moments(self, values):
        intensity = np.trace(values, axis1=-2, axis2=-1)
        return (np.einsum('n,...n->...', self.weights, intensity),
                np.einsum('n,ni,...n->...i', self.weights, self.directions, intensity))

    def scatter(self, values):
        return 1.5 * self.projector @ self.average(values)[..., None, :, :] @ self.projector

    def recoil_angular(self, values):
        dipole = np.einsum('n,nk,...nij->...kij', self.weights, self.directions, values)
        integrated = self.average(values)[..., None, :, :] - np.einsum('nk,...kij->...nij', self.directions, dipole)
        return 1.5 * self.projector @ integrated @ self.projector

    def thermal_angular(self, values):
        directions = self.directions
        projector = self.projector
        intensity = np.trace(values, axis1=-2, axis2=-1)
        linear = .5 * (values + np.swapaxes(values, -1, -2)) - .5 * intensity[..., None, None] * projector
        circular = 1j * np.einsum('nij,...nij->...n', self.epsilon, values)
        monopole = np.einsum('n,...n->...', self.weights, intensity)
        dipole = 3 * np.einsum('n,ni,...n->...i', self.weights, directions, intensity)
        quadrupole = 7.5 * (np.einsum('n,ni,nj,...n->...ij', self.weights, directions, directions, intensity)
                           - monopole[..., None, None] * np.eye(3) / 3)
        octupole = 17.5 * stf3(np.einsum('n,ni,nj,nk,...n->...ijk', self.weights, directions, directions, directions, intensity))
        electric2 = 2.5 * self.average(linear)
        electric3 = 10.5 * stf3(np.einsum('n,nk,...nij->...ijk', self.weights, directions, linear))
        scalar = (-2 * monopole[..., None] + .4 * np.einsum('...i,ni->...n', dipole, directions)
                  + np.einsum('...ij,ni,nj->...n', 3.6 * electric2 - .8 * quadrupole, directions, directions)
                  + np.einsum('...ijk,ni,nj,nk->...n', 9 / 35 * octupole - 6 / 7 * electric3, directions, directions, directions))
        polarization = ((.6 * quadrupole - 2.4 * electric2)[..., None, :, :]
                        + np.einsum('...ijk,nk->...nij', -9 / 35 * octupole + 6 / 7 * electric3, directions))
        circular0 = np.einsum('n,...n->...', self.weights, circular)
        circular1 = 3 * np.einsum('n,ni,...n->...i', self.weights, directions, circular)
        circular2 = 7.5 * (np.einsum('n,ni,nj,...n->...ij', self.weights, directions, directions, circular)
                          - circular0[..., None, None] * np.eye(3) / 3)
        circular_result = (circular0[..., None] - 2 * np.einsum('...i,ni->...n', circular1, directions)
                           + .4 * np.einsum('...ij,ni,nj->...n', circular2, directions, directions))
        return (.5 * scalar[..., None, None] * projector + transverse_traceless(polarization, projector)
                - .5j * circular_result[..., None, None] * self.epsilon)

    def collision(self, frequency, value, logarithmic_first, logarithmic_second, electron_ratio=1.):
        scatter = self.scatter(value) - value
        thermal = self.recoil_angular(logarithmic_second + 3 * logarithmic_first + 2 * value) + self.thermal_angular(value)
        shifted = self.recoil_angular(logarithmic_first + 2 * value)
        stimulated = value + .5 * self.projector
        recoil = frequency[..., None, None, None] * (stimulated @ shifted + shifted @ stimulated + 2 * value)
        return dict(thomson=scatter, thermal=thermal, recoil=recoil, correction=electron_ratio * thermal + recoil)
