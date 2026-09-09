import numpy as numerical

from annular_gram_joint_action_20260909 import coefficient_jets, gram_matrices


def bilinear(first, second, coefficient, spacing):
    factors, sampling = gram_matrices(first.size)
    return numerical.sum((factors @ first) * (sampling @ coefficient) * (factors @ second)) / spacing


def potential_hessian_pair(primitive, first, second, radii, constants, sigma, spacing):
    coefficient, gradient, hessian = coefficient_jets(primitive, radii, constants, sigma)
    first_coefficient = numerical.sum(gradient * first[1:], axis=0)
    second_coefficient = numerical.sum(gradient * second[1:], axis=0)
    mixed_coefficient = numerical.einsum("ijn,in,jn->n", hessian, first[1:], second[1:])
    scalar = primitive[0]
    terms = numerical.array([
        bilinear(first[0], second[0], coefficient, spacing),
        bilinear(first[0], scalar, second_coefficient, spacing),
        bilinear(second[0], scalar, first_coefficient, spacing),
        bilinear(scalar, scalar, mixed_coefficient, spacing) / 2,
    ])
    return terms.sum(), terms
