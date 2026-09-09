import numpy as numerical

from annular_clock_connection_20260909 import clock_offsets
from annular_gram_joint_action_20260909 import coefficient_pairing, gram_matrices, remainder


def clock_hessian_matrix(scalar, velocity, acceleration, coefficient, spacing):
    factors, sampling = gram_matrices(scalar.size)
    offsets, factor_coefficient, allocation = clock_offsets(coefficient, numerical.zeros_like(scalar))
    factor_scalar = factors @ scalar
    linear = -factors * velocity[None, :] + (factors @ velocity)[:, None] * allocation
    result = linear.T @ ((factor_coefficient / spacing)[:, None] * linear)
    acceleration_rows = factors * acceleration[None, :]
    weighted_scalar = factor_coefficient * factor_scalar / spacing
    result += numerical.diag(weighted_scalar @ acceleration_rows)
    result -= acceleration_rows.T @ (weighted_scalar[:, None] * allocation)
    result -= allocation.T @ (weighted_scalar[:, None] * acceleration_rows)
    result += allocation.T @ ((weighted_scalar * (factors @ acceleration))[:, None] * allocation)
    return result


def clock_covector(scalar, velocity, coefficient, spacing):
    return -velocity * remainder(scalar, coefficient, spacing) + coefficient * coefficient_pairing(scalar, velocity, spacing)


def clock_field_cross(scalar, velocity, coefficient, scalar_variation, velocity_variation, coefficient_variation, spacing):
    result = -velocity_variation * remainder(scalar, coefficient, spacing)
    result -= velocity * remainder(scalar_variation, coefficient, spacing)
    result -= velocity * remainder(scalar, coefficient_variation, spacing)
    result += coefficient_variation * coefficient_pairing(scalar, velocity, spacing)
    result += coefficient * (coefficient_pairing(scalar_variation, velocity, spacing) + coefficient_pairing(scalar, velocity_variation, spacing))
    return result


def connection_integration(edge_lengths):
    return numerical.tril(numerical.ones((edge_lengths.size + 1, edge_lengths.size)), k=-1) * edge_lengths[None, :]


def connection_metric_jets(exponential, lapse, radii):
    gradient = numerical.stack([-2 / (radii * exponential * lapse**2), 1 / (exponential * lapse)])
    hessian = numerical.empty((2, 2, radii.size))
    hessian[0, 0] = -8 / (radii**2 * exponential * lapse**3)
    hessian[0, 1] = hessian[1, 0] = 2 / (radii * exponential * lapse**2)
    hessian[1, 1] = -1 / (exponential * lapse)
    return gradient, hessian
