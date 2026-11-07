from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import eigh, solve


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'dynamical-axial-20261004'))
from axial_wave import WaveBody


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_model(cells, nominal=.03, quadrature_order=8):
    body = WaveBody(nominal)
    points, weights = leggauss(quadrature_order)
    basis = np.array([points*(points-1)/2, 1-points**2, points*(points+1)/2]).T
    slopes = np.array([points-.5, -2*points, points+.5]).T*2*cells
    size = 2*cells+1
    stiffness, inertia = np.zeros((size, size)), np.zeros((size, size))
    for element in range(cells):
        coordinates = (element+(points+1)/2)/cells
        coefficients = np.array([body.coefficients(float(position)) for position in coordinates])
        speed, material = coefficients[:, 0], coefficients[:, 2]
        measure = weights/(2*cells)
        local_stiffness = np.einsum('q,qi,qj->ij', measure*speed*coordinates**6, slopes, slopes)
        local_stiffness += np.einsum('q,qi,qj->ij', measure*speed*coordinates**6*material, basis, basis)
        local_inertia = np.einsum('q,qi,qj->ij', measure*coordinates**6/speed, basis, basis)
        indices = np.arange(2*element, 2*element+3)
        stiffness[np.ix_(indices, indices)] += local_stiffness
        inertia[np.ix_(indices, indices)] += local_inertia
    diagonal = 1/np.sqrt(np.diag(inertia[:-1, :-1]))
    balanced_stiffness = diagonal[:, None]*stiffness[:-1, :-1]*diagonal[None, :]
    balanced_inertia = diagonal[:, None]*inertia[:-1, :-1]*diagonal[None, :]
    eigenvalues, balanced_modes = eigh(balanced_stiffness, balanced_inertia, driver='gvd')
    modes = diagonal[:, None]*balanced_modes
    static = np.r_[diagonal*solve(balanced_stiffness, -diagonal*stiffness[:-1, -1], assume_a='pos'), 1.]
    coupling = modes.T@(inertia[:-1, :]@static)
    norm = float(static@inertia@static)
    surface_term = 3*(1-body.compactness)
    static_impedance = float(surface_term+static@stiffness@static)
    moment = float(np.sum(coupling**2/eigenvalues))
    gram_error = float(np.max(np.abs(modes.T@inertia[:-1, :-1]@modes-np.eye(size-1))))
    residual = balanced_stiffness@balanced_modes-(balanced_inertia@balanced_modes)*eigenvalues
    eigen_error = float(np.max(np.linalg.norm(residual, axis=0)/
                              (np.linalg.norm(balanced_stiffness@balanced_modes, axis=0)+
                               np.abs(eigenvalues)*np.linalg.norm(balanced_inertia@balanced_modes, axis=0))))
    return {'body': body, 'cells': cells, 'eigenvalues': eigenvalues, 'coupling': coupling,
            'norm': norm, 'moment': moment, 'static_impedance': static_impedance,
            'unresolved_kinetic_norm': norm-float(np.sum(coupling**2)),
            'stiffness': stiffness, 'inertia': inertia, 'static_profile': static,
            'surface_term': surface_term, 'modes': modes, 'gram_error': gram_error, 'eigen_error': eigen_error}


def response(model, frequency):
    squared = frequency**2
    weights = model['coupling']**2
    eigenvalues = model['eigenvalues']
    spectral = model['static_impedance']-squared*model['norm']-squared**2*np.sum(weights/(eigenvalues-squared))
    derivative = -model['norm']-2*squared*np.sum(weights/(eigenvalues-squared))-squared**2*np.sum(weights/(eigenvalues-squared)**2)
    matrix = model['stiffness']-squared*model['inertia']
    diagonal = 1/np.sqrt(np.diag(model['inertia'][:-1, :-1]))
    solution = np.r_[diagonal*solve(diagonal[:, None]*matrix[:-1, :-1]*diagonal[None, :],
                                    -diagonal*matrix[:-1, -1], assume_a='pos'), 1.]
    direct = model['surface_term']+solution@matrix@solution
    direct_norm = solution@model['inertia']@solution
    direct_energy = .5*(squared*direct_norm+model['surface_term']+solution@model['stiffness']@solution)
    legendre_energy = .5*(spectral-2*squared*derivative)
    return {'frequency_R': frequency, 'spectral_Y': float(spectral), 'direct_Y': float(direct),
            'dY_ds': float(derivative), 'direct_norm': float(direct_norm),
            'direct_energy_without_kappa_over_R': float(direct_energy),
            'Legendre_energy_without_kappa_over_R': float(legendre_energy)}
