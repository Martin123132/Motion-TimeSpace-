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
from scipy import linalg, special, sparse

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'polarized-finite-shift-kernel-20261007'
STEP = BRANCH / 'conservative-spectral-collision-step-20261007'
SOURCE = BRANCH / 'angular-thermal-source-20261007'
WAVES = BRANCH / 'coupled-finite-wave-evolution-20261007'
sys.path.insert(0, str(PARENT))
import kernel_common as prior
modest, digest, write_json = prior.modest, prior.digest, prior.write_json
NATIVE, HISTORY, angular = prior.NATIVE, prior.HISTORY, prior.angular
I3 = prior.previous.I3_PLANCK
IDENTITY = np.eye(2)
CIRCULAR = prior.PAULI[1]


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'grid_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'results/stage-integrity.json', *extra]
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths})
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def fano_gain(jones, cosine, recoil_extra, values):
    trace = np.trace(values, axis1=-2, axis2=-1)
    circular = np.einsum('ij,...ji->...', CIRCULAR, values)
    correction = (trace[..., None, None] * IDENTITY + (cosine * circular)[..., None, None] * CIRCULAR) / 4
    return jones @ values @ jones.swapaxes(-1, -2) + recoil_extra[..., None, None] * correction


def fano_adjoint(jones, cosine, values):
    trace = np.trace(values, axis1=-2, axis2=-1)
    circular = np.einsum('ij,...ji->...', CIRCULAR, values)
    correction = (trace[..., None, None] * IDENTITY + (cosine * circular)[..., None, None] * CIRCULAR) / 4
    return jones.swapaxes(-1, -2) @ values @ jones, correction


def modal_tensors(direction, axis, degree):
    cosine = np.einsum('...i,i->...', direction, axis)
    projector = angular.screen(direction)
    legendre = special.eval_legendre(degree, cosine)
    epsilon = np.einsum('ijk,...k->...ij', angular.EPSILON, direction)
    result = [legendre[..., None, None] * projector]
    names = ['I']
    if degree >= 2:
        projected = np.einsum('...ij,j->...i', projector, axis)
        derivative = (degree + 1) * (degree + 2) / 4 * special.eval_jacobi(degree - 2, 2, 2, cosine)
        factor = 2 * math.sqrt(math.factorial(degree - 2) / math.factorial(degree + 2))
        electric = factor * derivative[..., None, None] * (np.einsum('...i,...j->...ij', projected, projected)
                                                           - .5 * (1 - cosine ** 2)[..., None, None] * projector)
        magnetic = (epsilon @ electric - electric @ epsilon) / 2
        result.extend([electric, magnetic])
        names.extend(['E', 'B'])
    result.append(-1j * legendre[..., None, None] * epsilon)
    names.append('V')
    return np.stack(result), names


def event_geometry(theta, order):
    speeds, radial_weights = prior.juttner_rule(theta, order)
    electron_cosine, electron_weights = np.polynomial.legendre.leggauss(order)
    scattering_cosine, scattering_weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2 * np.pi * (np.arange(2 * order) + .5) / (2 * order)
    cosine = scattering_cosine[:, None]
    initial = np.array([0., 0., 1.])
    initial_frame = prior.frames(initial)
    result = {key: [] for key in ['incident', 'outgoing', 'cosine', 'weight', 'final_direction', 'final_frame', 'jones']}
    for speed, radial_weight in zip(speeds, radial_weights):
        for electron_node, electron_weight in zip(electron_cosine, electron_weights / 2):
            beta = speed * np.array([np.sqrt(1 - electron_node ** 2), 0., electron_node])
            rest_initial, incident, spatial = prior.boost(initial, beta)
            rest_initial_frame = prior.transport_frames(rest_initial, initial_frame, spatial)
            transverse = np.array([rest_initial[2], 0., -rest_initial[0]])
            second = np.cross(rest_initial, transverse)
            rest_final = cosine[..., None] * rest_initial + np.sqrt(1 - cosine ** 2)[..., None] * (
                np.cos(azimuth)[None, :, None] * transverse + np.sin(azimuth)[None, :, None] * second)
            rest_final = rest_final.reshape(-1, 3)
            final, outgoing, _ = prior.boost(rest_final, -beta)
            rest_final_frame = prior.frames(rest_final)
            final_frame = prior.transport_frames(final, rest_final_frame, spatial)
            jones = rest_final_frame.swapaxes(-1, -2) @ rest_initial_frame
            count = len(rest_final)
            result['incident'].append(np.full(count, incident))
            result['outgoing'].append(outgoing)
            result['cosine'].append(np.repeat(scattering_cosine, len(azimuth)))
            weights = radial_weight * electron_weight * (1 - beta[2]) * scattering_weights / (2 * len(azimuth))
            result['weight'].append(np.repeat(weights, len(azimuth)))
            result['final_direction'].append(final)
            result['final_frame'].append(final_frame)
            result['jones'].append(jones)
    return {key: np.concatenate(value) for key, value in result.items()}


def angular_correlations(events, degree, extra_axis=0):
    axes = angular.AngularKernel(degree + 2 + extra_axis, 2 * (degree + 2 + extra_axis))
    initial = np.array([0., 0., 1.])
    initial_frame = prior.frames(initial)
    names = ['I', 'E', 'B', 'V'] if degree >= 2 else ['I', 'V']
    count = len(names)
    first = np.zeros((count, count, len(events['weight'])), dtype=complex)
    second = np.zeros_like(first)
    for axis, weight in zip(axes.directions, axes.weights):
        source, _ = modal_tensors(initial, axis, degree)
        target, _ = modal_tensors(events['final_direction'], axis, degree)
        source = initial_frame.T @ source @ initial_frame
        final_frame = events['final_frame']
        target = final_frame.swapaxes(-1, -2) @ target @ final_frame
        mapped, correction = fano_adjoint(events['jones'], events['cosine'], target)
        first += weight * np.einsum('aij,bnji->abn', source, mapped)
        second += weight * np.einsum('aij,bnji->abn', source, correction)
    assert max(np.max(abs(first.imag)), np.max(abs(second.imag))) < 1e-12
    return first.real, second.real, names
