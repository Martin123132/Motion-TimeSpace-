import math

import numpy as numerical

from sbp4_derived_operator_20260909 import derivative


def exponential_moments(argument):
    first = numerical.zeros_like(argument)
    weighted = numerical.zeros_like(argument)
    small = numerical.abs(argument) < 0.1
    selected = argument[small]
    for degree in range(13):
        term = selected**degree / math.factorial(degree)
        first[small] += term / (degree + 1)
        weighted[small] += term / (degree + 2)
    selected = argument[~small]
    first[~small] = numerical.expm1(selected) / selected
    weighted[~small] = ((selected - 1) * numerical.exp(selected) + 1) / selected**2
    return first, weighted


def derivative_moments(count):
    matrix = derivative(numerical.eye(count), 1.0).T
    distances = numerical.abs(numerical.arange(count)[:, None] - numerical.arange(count)[None, :])
    return numerical.sum(numerical.abs(matrix) * distances / 2, axis=1), numerical.sum(numerical.abs(matrix) * distances**2 / 2, axis=1)


def integrate_source(coefficient, forcing, spacing, boundary=0.0):
    if coefficient.shape != forcing.shape or coefficient.ndim != 1 or coefficient.size < 9 or spacing <= 0:
        raise ValueError("Uniform one-dimensional source grid required")
    if not numerical.all(numerical.isfinite(coefficient)) or not numerical.all(numerical.isfinite(forcing)) or not math.isfinite(boundary):
        raise ValueError("Finite source inputs required")
    midpoint = (coefficient[:-1] + coefficient[1:]) / 2
    argument = -spacing * midpoint
    first, weighted = exponential_moments(argument)
    left_weight, right_weight = spacing * (first - weighted), spacing * weighted
    propagation = numerical.exp(argument)
    result = numerical.empty_like(forcing)
    result[-1] = boundary
    for position in range(forcing.size - 2, -1, -1):
        result[position] = propagation[position] * result[position + 1] - left_weight[position] * forcing[position] - right_weight[position] * forcing[position + 1]
    if not numerical.all(numerical.isfinite(result)):
        raise ValueError("Nonfinite Volterra source integration")
    return result


def residual_bound(coefficient, forcing, spacing, boundary=0.0, moments=None):
    count = forcing.size
    length = spacing * (count - 1)
    maximum_coefficient = float(numerical.max(numerical.abs(coefficient)))
    maximum_forcing = float(numerical.max(numerical.abs(forcing)))
    coefficient_lipschitz = float(numerical.max(numerical.abs(numerical.diff(coefficient)))) / spacing
    forcing_lipschitz = float(numerical.max(numerical.abs(numerical.diff(forcing)))) / spacing
    amplitude_bound = math.exp(maximum_coefficient * length) * (abs(boundary) + length * maximum_forcing)
    derivative_bound = maximum_coefficient * amplitude_bound + maximum_forcing
    first, second = derivative_moments(count) if moments is None else moments
    bound = spacing * ((maximum_coefficient * derivative_bound + coefficient_lipschitz * amplitude_bound + forcing_lipschitz) * second + coefficient_lipschitz * amplitude_bound * first)
    return bound, {"amplitude_bound": amplitude_bound, "derivative_bound": derivative_bound, "coefficient_max": maximum_coefficient, "forcing_max": maximum_forcing, "coefficient_lipschitz": coefficient_lipschitz, "forcing_lipschitz": forcing_lipschitz}


def complete_without_scalar_projection(sources, gradient, spacing, moments=None):
    if sources.shape[0] != 4 or gradient.shape != (5, sources.shape[1]):
        raise ValueError("Coordinate source order chi,q,mu,delta required")
    if numerical.any(sources[0] != 0):
        raise ValueError("This completion requires S_chi=S_w=0")
    forcing = gradient[1] * sources[1] + gradient[3] * sources[3]
    result = sources.copy()
    result[2] = integrate_source(gradient[2], forcing, spacing)
    residual = derivative(result[2], spacing) - gradient[2] * result[2] - forcing
    bound, constants = residual_bound(gradient[2], forcing, spacing, moments=moments)
    return result, {"residual": residual, "bound": bound, **constants}
