import numpy as numerical
from numpy.polynomial import chebyshev, Polynomial

from annular_coordinate_evolution_operator_20260909 import coefficients, local_jacobians


SCALAR_PROFILE = Polynomial([0, 0, 0.5, -2, 3, -2, 0.5])
LAPSE_PROFILE = Polynomial([0, -1, 4, -6, 4, -1])


def profiles(radii, order=0):
    result = []
    for polynomial, distance, sign in [(SCALAR_PROFILE, radii - 4, 1), (SCALAR_PROFILE, 8 - radii, -1), (LAPSE_PROFILE, 8 - radii, -1)]:
        result.append(numerical.where((distance >= 0) & (distance <= 1), polynomial.deriv(order)(distance) * sign**order, 0))
    return numerical.stack(result)


def constraint_gradients(snapshot, radii, evaluator):
    base, spatial = snapshot["state"][0], snapshot["state_space"][0]
    columns = []
    for selected, component in [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]:
        arguments = [base, spatial]
        arguments[selected] = arguments[selected].astype(complex)
        arguments[selected][component] += 1j * 1e-30
        data = coefficients(*arguments, radii, evaluator.constants, evaluator.kappa, evaluator.sigma)
        columns.append((data["R"] + evaluator.sigma * data["C"]).imag / 1e-30)
    return numerical.stack(columns)


def build(evaluator, epsilon, degree):
    abscissae = numerical.cos(numerical.pi * numerical.arange(degree + 1) / degree)
    vandermonde = chebyshev.chebvander(abscissae, degree)
    derivative_matrix = numerical.stack([chebyshev.chebval(abscissae, chebyshev.chebder(column)) for column in numerical.eye(degree + 1)], axis=1) * 2
    boundary = numerical.zeros(5)
    panels = []
    for left in [7, 6, 5, 4]:
        radii = left + (abscissae + 1) / 2
        snapshot = evaluator.evaluate(numerical.zeros_like(radii), radii, epsilon)
        gradient = constraint_gradients(snapshot, radii, evaluator)
        shape, shape_radial = profiles(radii), profiles(radii, 1)
        forcing = numerical.stack([-snapshot["initial_constraint"][0], -snapshot["initial_constraint"][1], gradient[0] * shape[0] + gradient[4] * shape_radial[0], gradient[0] * shape[1] + gradient[4] * shape_radial[1], gradient[3] * shape[2]], axis=1)
        matrix = derivative_matrix - gradient[2, :, None] * vandermonde
        matrix[0] = vandermonde[0]
        forcing[0] = boundary
        basis_coefficients = numerical.linalg.solve(matrix, forcing).T
        boundary = chebyshev.chebval(-1, basis_coefficients.T)
        panels.append({"left": left, "right": left + 1, "basis_coefficients": basis_coefficients.tolist(), "collocation_condition_number": float(numerical.linalg.cond(matrix))})

    endpoints = numerical.array([4.0, 8.0])
    snapshot = evaluator.evaluate(numerical.zeros_like(endpoints), endpoints, epsilon)
    zero_order, first_order, second_order = local_jacobians(snapshot["state"][0], snapshot["state_space"][0], snapshot["state_second"][0], endpoints, evaluator.constants, evaluator.kappa, evaluator.sigma)
    inner_basis = boundary
    outer_lapse = evaluator.sigma * snapshot["defect"][:, 3, 1]
    outer_scalar = (snapshot["defect"][:, 1, 1] - first_order[1, 3, 1] * outer_lapse) / second_order[1, 0, 1]
    denominator = second_order[1, 0, 0] + zero_order[1, 2, 0] * inner_basis[2]
    inner_scalar = (snapshot["defect"][:, 1, 0] - zero_order[1, 2, 0] * (inner_basis[:2] + outer_scalar * inner_basis[3] + outer_lapse * inner_basis[4])) / denominator
    amplitudes = numerical.stack([inner_scalar, outer_scalar, outer_lapse], axis=1)
    for panel in panels:
        basis = numerical.array(panel["basis_coefficients"])
        panel["mass_coefficients"] = (basis[:2] + amplitudes @ basis[2:]).tolist()
    return {"case": evaluator.case["name"], "epsilon": epsilon, "sigma": evaluator.sigma, "degree": degree, "amplitude_order": ["inner_scalar", "outer_scalar", "outer_lapse"], "amplitudes": amplitudes.tolist(), "panels": panels, "inner_denominator": float(denominator), "inner_unperturbed_denominator": float(second_order[1, 0, 0]), "outer_denominator": float(second_order[1, 0, 1]), "meaning": "One grid-independent initial-data lift. Mass is a spectrally approximated continuum constraint solution, not a certified exact function. Profiles are a declared data choice; amplitudes solve the first corner equations.", "valid_for_physics_claim": False}


def lift(payload, radii):
    amplitudes = numerical.array(payload["amplitudes"])
    result = []
    for order in range(3):
        values = numerical.zeros((2, 4, radii.size))
        shape = profiles(radii, order)
        values[:, 0] = amplitudes[:, :2] @ shape[:2]
        values[:, 3] = amplitudes[:, 2, None] * shape[2]
        for panel in payload["panels"]:
            mask = (radii >= panel["left"]) & (radii <= panel["right"])
            coordinate = 2 * (radii[mask] - panel["left"]) - 1
            mass_coefficients = chebyshev.chebder(numerical.array(panel["mass_coefficients"]).T, m=order, axis=0) * 2**order
            values[:, 2, mask] = chebyshev.chebval(coordinate, mass_coefficients)
        result.append(values)
    return result


def initial_diagnostics(payload, evaluator, radii):
    initial, initial_radial, initial_second = lift(payload, radii)
    snapshot = evaluator.evaluate(numerical.zeros_like(radii), radii, payload["epsilon"])
    gradient = constraint_gradients(snapshot, radii, evaluator)
    residual = snapshot["initial_constraint"] + initial_radial[:, 2] - numerical.einsum("in,bin->bn", gradient[:4], initial) - gradient[4] * initial_radial[:, 0]
    endpoints = numerical.array([4.0, 8.0])
    point = evaluator.evaluate(numerical.zeros_like(endpoints), endpoints, payload["epsilon"])
    state, first, second = lift(payload, endpoints)
    matrices = local_jacobians(point["state"][0], point["state_space"][0], point["state_second"][0], endpoints, evaluator.constants, evaluator.kappa, evaluator.sigma)
    bulk = sum(numerical.einsum("ijn,bjn->bin", matrix, argument) for matrix, argument in zip(matrices, [state, first, second])) - point["defect"]
    return {"mass_residual": float(numerical.max(numerical.abs(residual))), "mass_residual_scale": float(numerical.max(numerical.abs(snapshot["initial_constraint"]))), "scalar_corner": bulk[:, 1].tolist(), "lapse_corner": bulk[:, 3, -1].tolist(), "outer_mass": state[:, 2, -1].tolist(), "outer_lapse": state[:, 3, -1].tolist(), "scalar_boundary_value": state[:, 0].tolist(), "scalar_boundary_radial": first[:, 0].tolist(), "initial_scalar_max": numerical.max(numerical.abs(initial[:, 0]), axis=1).tolist()}
