from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.linalg import cholesky, solve_triangular, solve_banded, eigh
from scipy.sparse import csr_matrix
import numpy as np


def dense_mass(bands):
    count = bands.shape[1]
    matrix = np.zeros((count, count))
    for offset in [-2, -1, 0, 1, 2]:
        columns = np.arange(max(0, -offset), min(count, count-offset))
        matrix[columns+offset, columns] = bands[2+offset, columns]
    return matrix


def dense_stiffness(layer, weights):
    indices, radial = layer.reference_indices, layer.reference_radial
    gradient = csr_matrix((radial.ravel(), (np.repeat(np.arange(len(indices)), 3), indices.ravel())),
        shape=(len(indices), layer.count))
    matrix = (gradient.T @ gradient.multiply(weights['gradient'][:, None])).toarray()
    matrix += (layer.lifted.T @ layer.lifted.multiply(weights['gram'][:, None])).toarray()
    return matrix


def right_inverse_transpose(matrix, lower):
    return solve_triangular(lower, matrix.T, lower=True, check_finite=False).T


def whiten(matrix, left_lower, right_lower):
    return right_inverse_transpose(solve_triangular(left_lower, matrix, lower=True, check_finite=False), right_lower)


def operator_bound(matrix):
    if not matrix.size:
        return dict(sharp_squared=0., row_sum_squared_bound=0., eigen_residual=0.), np.zeros(matrix.shape[1])
    normal = matrix @ matrix.T
    asymmetry = float(np.max(abs(normal-normal.T)))
    normal = (normal+normal.T)/2
    eigenvalue, vector = eigh(normal, subset_by_index=[len(normal)-1, len(normal)-1], check_finite=False)
    sharp = float(eigenvalue[0])
    left = vector[:, 0]
    right = matrix.T @ left/np.sqrt(max(sharp, np.finfo(float).tiny))
    return dict(sharp_squared=sharp, row_sum_squared_bound=float(np.max(np.sum(abs(normal), axis=1))),
        eigen_residual=float(np.max(abs(normal @ left-sharp*left))), normal_asymmetry=asymmetry), right


def transfer_constants(coarse_mass_bands, fine_mass, coarse_stiffness, fine_stiffness,
                       indices, shape, coarse_factor, coarse_weights):
    interpolation = csr_matrix((shape.ravel(), (np.repeat(np.arange(len(indices)), 3), indices.ravel())),
        shape=(len(indices), len(coarse_stiffness))).toarray()
    adjoint = solve_banded((2, 2), coarse_mass_bands, interpolation.T @ fine_mass, check_finite=False)
    coarse_lower = cholesky(coarse_stiffness, lower=True, check_finite=False)
    fine_lower = cholesky(fine_stiffness, lower=True, check_finite=False)
    whitened_adjoint = right_inverse_transpose(adjoint, fine_lower)
    stiffness_operator = coarse_lower.T @ whitened_adjoint
    stiffness, maximizing_vector = operator_bound(stiffness_operator)
    gram_operator = np.sqrt(coarse_weights)[:, None]*(coarse_factor @ whitened_adjoint)
    gram, unused = operator_bound(gram_operator)
    maximizer = solve_triangular(fine_lower.T, maximizing_vector, lower=False, check_finite=False)
    return dict(adjoint=adjoint, interpolation=interpolation, stiffness=stiffness, gram=gram,
        fine_lower=fine_lower, coarse_lower=coarse_lower, maximizer=maximizer)


def differentiated_energy(mass, stiffness, mass_rate, stiffness_rate, displacement, velocity, acceleration, residual_rate):
    energy = .5*float(acceleration @ mass @ acceleration+velocity @ stiffness @ velocity)
    channels = dict(residual_derivative=float(acceleration @ residual_rate),
        mass_transport=-.5*float(acceleration @ mass_rate @ acceleration),
        stiffness_displacement_transport=-float(acceleration @ stiffness_rate @ displacement),
        stiffness_velocity_transport=.5*float(velocity @ stiffness_rate @ velocity))
    return dict(energy=energy, rate=sum(channels.values()), channels=channels)


def energy_growth_bound(mass, stiffness, mass_rate, stiffness_rate, displacement, velocity, acceleration, residual_rate):
    mass_lower = cholesky(mass, lower=True, check_finite=False)
    stiffness_lower = cholesky(stiffness, lower=True, check_finite=False)
    mass_transport = whiten(mass_rate, mass_lower, mass_lower)
    stiffness_transport = whiten(stiffness_rate, stiffness_lower, stiffness_lower)
    cross_transport = whiten(stiffness_rate, mass_lower, stiffness_lower)
    mass_constant = float(np.max(np.sum(abs(mass_transport), axis=1)))
    stiffness_constant = float(np.max(np.sum(abs(stiffness_transport), axis=1)))
    cross_constant = float(np.linalg.norm(cross_transport, 'fro'))
    forcing = float(np.linalg.norm(solve_triangular(mass_lower, residual_rate, lower=True, check_finite=False)))
    lower_energy = .5*float(velocity @ mass @ velocity+displacement @ stiffness @ displacement)
    higher_energy = .5*float(acceleration @ mass @ acceleration+velocity @ stiffness @ velocity)
    beta = max(mass_constant, stiffness_constant)
    rate_bound = beta*higher_energy+np.sqrt(2*higher_energy)*(forcing+cross_constant*np.sqrt(2*lower_energy))
    return dict(mass_relative_rate_bound=mass_constant, stiffness_relative_rate_bound=stiffness_constant,
        cross_rate_bound=cross_constant, residual_derivative_dual_norm=forcing, lower_energy=lower_energy,
        higher_energy=higher_energy, energy_rate_upper_bound=float(rate_bound),
        norm_growth_coefficient=beta/2, norm_forcing_bound=float(forcing+cross_constant*np.sqrt(2*lower_energy)))
