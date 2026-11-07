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
from scipy import special, integrate, sparse, linalg

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'conservative-spectral-collision-step-20261007'
SOURCE = BRANCH / 'angular-thermal-source-20261007'
sys.path.insert(0, str(PARENT))
import step_common as previous
angular = previous.inherited
modest, digest, write_json = previous.modest, previous.digest, previous.write_json
NATIVE, HISTORY = previous.NATIVE, previous.HISTORY
PAULI = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex)


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'kernel_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def spin(vector):
    return np.einsum('...i,ijk->...jk', vector, PAULI)


def frames(directions):
    directions = np.asarray(directions)
    references = np.broadcast_to(np.array([0., 0., 1.]), directions.shape).copy()
    references[abs(directions[..., 2]) > .8] = np.array([1., 0., 0.])
    first = np.cross(directions, references)
    first /= np.linalg.norm(first, axis=-1)[..., None]
    return np.stack([first, np.cross(directions, first)], axis=-1)


def boost(directions, velocity):
    speed_squared = velocity @ velocity
    if speed_squared == 0:
        return np.array(directions, copy=True), np.ones(np.shape(directions)[:-1]), np.eye(3)
    gamma = 1 / np.sqrt(1 - speed_squared)
    spatial = np.eye(3) + (gamma - 1) * np.outer(velocity, velocity) / speed_squared
    doppler = gamma * (1 - np.einsum('...i,i->...', directions, velocity))
    rest = (np.einsum('ij,...j->...i', spatial, directions) - gamma * velocity) / doppler[..., None]
    return rest, doppler, spatial


def transport_frames(directions, original_frames, spatial):
    return angular.screen(directions) @ spatial @ original_frames


def rest_channels(energy, initial, final, initial_frame=None, final_frame=None):
    if initial_frame is None:
        initial_frame = frames(initial)
    if final_frame is None:
        final_frame = frames(final)
    cosine = np.einsum('...i,...i->...', initial, final)
    ratio = 1 / (1 + energy * (1 - cosine))
    outgoing_energy = energy * ratio
    electron_energy = 1 + energy - outgoing_energy
    electron_momentum = energy * initial - outgoing_energy[..., None] * final
    momentum_spin = spin(electron_momentum)
    initial_spin, final_spin = spin(initial), spin(final)
    shape = np.shape(cosine)
    amplitudes = np.empty(shape + (2, 2, 2, 2), dtype=complex)
    for outgoing in range(2):
        outgoing_vector = final_frame[..., :, outgoing]
        outgoing_spin = spin(outgoing_vector)
        for incoming in range(2):
            incoming_vector = initial_frame[..., :, incoming]
            incoming_spin = spin(incoming_vector)
            overlap = np.einsum('...i,...i->...', outgoing_vector, incoming_vector)
            triple = outgoing_spin @ initial_spin @ incoming_spin + incoming_spin @ final_spin @ outgoing_spin
            amplitudes[..., outgoing, incoming, :, :] = np.sqrt((electron_energy + 1) / 2)[..., None, None] * (
                overlap[..., None, None] * np.eye(2) + momentum_spin @ triple / (2 * (electron_energy + 1)[..., None, None]))
    axes = list(range(len(shape))) + [len(shape) + 2, len(shape) + 3, len(shape), len(shape) + 1]
    channels = amplitudes.transpose(axes).reshape(shape + (4, 2, 2)) / np.sqrt(2)
    return channels, ratio


def gain(channels, values):
    return np.einsum('...sai,...ij,...sbj->...ab', channels, values, channels.conj())


def adjoint(channels, values):
    return np.einsum('...sai,...ab,...sbj->...ij', channels.conj(), values, channels)


def juttner_rule(theta, radial=8):
    nodes, weights = special.roots_genlaguerre(radial, .5)
    gamma = 1 + theta * nodes
    momentum = np.sqrt(theta * nodes * (2 + theta * nodes))
    weights = weights * gamma * np.sqrt(2 + theta * nodes)
    weights /= weights.sum()
    return momentum / gamma, weights


def fixture(directions, kind):
    projector = angular.screen(directions)
    if kind == 'intensity':
        scalar = 1 + .2 * directions[..., 0] + .1 * directions[..., 1] * directions[..., 2] + .07 * special.eval_legendre(4, directions[..., 2])
        return .5 * scalar[..., None, None] * projector
    if kind == 'linear':
        tensor = np.array([[.4, .1, -.2], [.1, -.3, .13], [-.2, .13, -.1]])
        return angular.transverse_traceless(tensor, projector) * (.3 + .2 * directions[..., 2] + .1 * directions[..., 0] * directions[..., 1])[..., None, None]
    if kind == 'circular':
        circular = 1 + .2 * directions[..., 0] + .1 * directions[..., 1] * directions[..., 2]
        epsilon = np.einsum('ijk,...k->...ij', angular.EPSILON, directions)
        return -.5j * circular[..., None, None] * epsilon
    raise ValueError(kind)
