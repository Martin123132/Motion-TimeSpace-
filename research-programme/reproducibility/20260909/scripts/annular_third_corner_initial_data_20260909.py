import math

import numpy as numerical
from numpy.polynomial import Polynomial, chebyshev

from annular_continuum_initial_data_20260909 import constraint_gradients


DISTANCE = Polynomial([0, 1])
CUTOFF = Polynomial([1, -1])**6
PROFILES = []
for corner_order in range(1, 4):
    for component, endpoint, orientation, degree in [(0, 4, 1, corner_order + 1), (0, 8, -1, corner_order + 1), (3, 8, -1, corner_order)]:
        PROFILES.append((component, endpoint, orientation, orientation**degree * DISTANCE**degree * CUTOFF / math.factorial(degree)))


def profile_values(radii, order=0):
    values = numerical.zeros((9, 4, radii.size))
    for position, (component, endpoint, orientation, polynomial) in enumerate(PROFILES):
        distance = orientation * (radii - endpoint)
        values[position, component] = numerical.where((distance >= 0) & (distance <= 1), polynomial.deriv(order)(distance) * orientation**order, 0)
    return values


def build_family(evaluator, degree=64):
    nodes = numerical.cos(numerical.pi * numerical.arange(degree + 1) / degree)
    vandermonde = chebyshev.chebvander(nodes, degree)
    derivative = numerical.stack([chebyshev.chebval(nodes, chebyshev.chebder(column)) for column in numerical.eye(degree + 1)], axis=1) * 2
    boundary = numerical.zeros(10)
    panels = []
    for left in [7, 6, 5, 4]:
        radii = left + (nodes + 1) / 2
        snapshot = evaluator.evaluate(numerical.zeros_like(radii), radii, .1)
        gradient = constraint_gradients(snapshot, radii, evaluator)
        profiles, radial = profile_values(radii), profile_values(radii, 1)
        forcing = numerical.zeros((degree + 1, 10))
        forcing[:, 0] = -snapshot["initial_constraint"][0]
        forcing[:, 1:] = (numerical.einsum("in,bin->bn", gradient[:4], profiles) + gradient[4] * radial[:, 0]).T
        matrix = derivative - gradient[2, :, None] * vandermonde
        matrix[0] = vandermonde[0]
        forcing[0] = boundary
        coefficients = numerical.linalg.solve(matrix, forcing).T
        boundary = chebyshev.chebval(-1, coefficients.T)
        panels.append({"left": left, "right": left + 1, "basis_coefficients": coefficients.tolist(), "collocation_condition_number": float(numerical.linalg.cond(matrix))})
    return {"case": evaluator.case["name"], "degree": degree, "epsilon": .1, "sigma": evaluator.sigma, "kind": "ordinary_analytic_third_corner", "cutoff_power": 6, "amplitude_order": [name + str(order) for order in range(1, 4) for name in ["inner_scalar_corner", "outer_scalar_corner", "outer_lapse_corner"]], "panels": panels, "valid_for_physics_claim": False}


def family_derivatives(payload, radii, maximum=4):
    result = []
    for order in range(maximum + 1):
        values = numerical.zeros((10, 4, radii.size))
        values[1:] = profile_values(radii, order)
        for panel in payload["panels"]:
            mask = (radii >= panel["left"]) & (radii <= panel["right"])
            coordinate = 2 * (radii[mask] - panel["left"]) - 1
            coefficients = chebyshev.chebder(numerical.array(panel["basis_coefficients"]).T, m=order, axis=0) * 2**order
            values[:, 2, mask] = chebyshev.chebval(coordinate, coefficients)
        result.append(values)
    return numerical.array(result)


def initial_derivatives(payload, radii, maximum=4):
    weights = numerical.r_[1., numerical.array(payload["amplitudes"])]
    return numerical.einsum("b,dbin->din", weights, family_derivatives(payload, radii, maximum))[:, None]


def lift(payload, radii):
    return list(initial_derivatives(payload, radii, 2))
