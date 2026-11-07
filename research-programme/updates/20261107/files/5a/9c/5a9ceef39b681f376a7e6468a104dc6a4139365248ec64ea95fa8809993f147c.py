import numpy as numerical

from sbp4_compatible_second_operator_20260909 import norm_weights


def linear_basis(source, target):
    if numerical.any(numerical.diff(source) <= 0) or numerical.any(target < source[0] - 1e-13) or numerical.any(target > source[-1] + 1e-13):
        raise ValueError('Ordered basis with no extrapolation required')
    left = numerical.clip(numerical.searchsorted(source, target, side='right') - 1, 0, source.size - 2)
    fraction = (target - source[left]) / (source[left + 1] - source[left])
    matrix = numerical.zeros((target.size, source.size))
    matrix[numerical.arange(target.size), left] = 1 - fraction
    matrix[numerical.arange(target.size), left + 1] = fraction
    return matrix


def mixed_basis(radii):
    spacing = float(radii[1] - radii[0])
    weights = spacing * norm_weights(radii.size)
    faces = numerical.concatenate([[radii[0]], radii[0] + numerical.cumsum(weights)])
    faces[-1] = radii[-1]
    incidence = numerical.zeros((radii.size, faces.size))
    incidence[numerical.arange(radii.size), numerical.arange(radii.size)] = -1
    incidence[numerical.arange(radii.size), numerical.arange(radii.size) + 1] = 1
    return faces, weights, linear_basis(faces, radii), linear_basis(radii, faces), incidence


def weak_gravity(mass, mass_time, shift, basis, sigma, kappa):
    faces, weights, mass_to_node, unused_shift_to_face, incidence = basis
    return numerical.dot(numerical.exp(shift), incidence @ mass - sigma * weights * (mass_to_node @ mass_time)) / kappa


def weak_gravity_covectors(mass, mass_time, shift, shift_time, basis, sigma, kappa):
    faces, weights, mass_to_node, unused_shift_to_face, incidence = basis
    exponential = numerical.exp(shift)
    radial = exponential * (incidence @ mass - sigma * weights * (mass_to_node @ mass_time)) / kappa
    mass_euler = (incidence.T @ exponential + sigma * mass_to_node.T @ (weights * exponential * shift_time)) / kappa
    momentum = -sigma * mass_to_node.T @ (weights * exponential) / kappa
    physical_boundary = numerical.zeros(faces.size)
    physical_boundary[0], physical_boundary[-1] = -exponential[0] / kappa, exponential[-1] / kappa
    return radial, mass_euler, momentum, physical_boundary
