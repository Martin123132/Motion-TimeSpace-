import numpy as numerical

from annular_gram_joint_action_20260909 import gram_matrices


def real_matrix_action(matrix, values):
    if numerical.iscomplexobj(values):
        return matrix @ values.real + 1j * (matrix @ values.imag)
    return matrix @ values


def clock_covector(scalar, velocity, coefficient, spacing):
    factors, sampling = gram_matrices(scalar.size)
    factor_scalar = real_matrix_action(factors, scalar)
    factor_velocity = real_matrix_action(factors, velocity)
    factor_coefficient = real_matrix_action(sampling, coefficient)
    force = real_matrix_action(factors.T, factor_coefficient * factor_scalar) / spacing
    density_time = real_matrix_action(sampling.T, factor_scalar * factor_velocity) / spacing
    return -velocity * force + coefficient * density_time
