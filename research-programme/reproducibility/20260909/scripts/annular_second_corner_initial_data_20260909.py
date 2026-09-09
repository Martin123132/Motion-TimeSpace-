import numpy as numerical
from numpy.polynomial import Polynomial, chebyshev

from annular_continuum_initial_data_20260909 import constraint_gradients


DISTANCE = Polynomial([0, 1])
CUTOFF = Polynomial([1, -1])**4
PROFILES = [(0, 4, 1, DISTANCE**2 * CUTOFF / 2), (0, 8, -1, DISTANCE**2 * CUTOFF / 2), (3, 8, -1, -DISTANCE * CUTOFF), (0, 4, 1, DISTANCE**3 * CUTOFF / 6), (0, 8, -1, DISTANCE**3 * CUTOFF / 6), (3, 8, -1, DISTANCE**2 * CUTOFF / 2)]


def profile_values(radii, order=0):
    values = numerical.zeros((6, 4, radii.size))
    for position, (component, endpoint, orientation, polynomial) in enumerate(PROFILES):
        distance = orientation * (radii - endpoint)
        values[position, component] = numerical.where((distance >= 0) & (distance <= 1), polynomial.deriv(order)(distance) * orientation**order, 0)
    return values


def build_family(evaluator, degree=64):
    abscissae = numerical.cos(numerical.pi * numerical.arange(degree + 1) / degree)
    vandermonde = chebyshev.chebvander(abscissae, degree)
    derivative = numerical.stack([chebyshev.chebval(abscissae, chebyshev.chebder(column)) for column in numerical.eye(degree + 1)], axis=1) * 2
    boundary = numerical.zeros(7)
    panels = []
    for left in [7, 6, 5, 4]:
        radii = left + (abscissae + 1) / 2
        snapshot = evaluator.evaluate(numerical.zeros_like(radii), radii, 0.1)
        gradient = constraint_gradients(snapshot, radii, evaluator)
        profiles = profile_values(radii)
        profiles_radial = profile_values(radii, 1)
        forcing = numerical.zeros((degree + 1, 7))
        forcing[:, 0] = -snapshot["initial_constraint"][0]
        forcing[:, 1:] = (numerical.einsum("in,bin->bn", gradient[:4], profiles) + gradient[4] * profiles_radial[:, 0]).T
        matrix = derivative - gradient[2, :, None] * vandermonde
        matrix[0] = vandermonde[0]
        forcing[0] = boundary
        coefficients = numerical.linalg.solve(matrix, forcing).T
        boundary = chebyshev.chebval(-1, coefficients.T)
        panels.append({"left": left, "right": left + 1, "basis_coefficients": coefficients.tolist(), "collocation_condition_number": float(numerical.linalg.cond(matrix))})
    return {"case": evaluator.case["name"], "degree": degree, "epsilon": 0.1, "sigma": evaluator.sigma, "kind": "ordinary_second_corner", "amplitude_order": ["inner_scalar_jet2", "outer_scalar_jet2", "outer_lapse_jet1", "inner_scalar_jet3", "outer_scalar_jet3", "outer_lapse_jet2"], "panels": panels, "valid_for_physics_claim": False}


def family_lift(payload, radii):
    result = []
    for order in range(3):
        values = numerical.zeros((7, 4, radii.size))
        values[1:] = profile_values(radii, order)
        for panel in payload["panels"]:
            mask = (radii >= panel["left"]) & (radii <= panel["right"])
            coordinate = 2 * (radii[mask] - panel["left"]) - 1
            coefficients = chebyshev.chebder(numerical.array(panel["basis_coefficients"]).T, m=order, axis=0) * 2**order
            values[:, 2, mask] = chebyshev.chebval(coordinate, coefficients)
        result.append(values)
    return result


def lift(payload, radii):
    coefficients = numerical.r_[1., numerical.array(payload["amplitudes"])]
    return [numerical.einsum("b,bin->in", coefficients, values)[None, ...] for values in family_lift(payload, radii)]
