from __future__ import annotations

import argparse
import math
from functools import lru_cache

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_bvp, solve_ivp
from scipy.interpolate import CubicSpline


def _add(*polynomials: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for polynomial in polynomials:
        for order, value in polynomial.items():
            result[order] = result.get(order, 0) + value
    return {order: value for order, value in result.items() if order <= 4 and value != 0}


def _scale(polynomial: dict[int, sp.Expr], coefficient: sp.Expr) -> dict[int, sp.Expr]:
    return {
        order: coefficient * value
        for order, value in polynomial.items()
        if order <= 4 and value != 0
    }


def _multiply(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_order, left_value in left.items():
        for right_order, right_value in right.items():
            order = left_order + right_order
            if order <= 4:
                result[order] = result.get(order, 0) + left_value * right_value
    return {order: value for order, value in result.items() if value != 0}


def _differentiate(polynomial: dict[int, sp.Expr], variable: sp.Symbol) -> dict[int, sp.Expr]:
    return {
        order: sp.diff(value, variable)
        for order, value in polynomial.items()
        if value != 0
    }


@lru_cache(maxsize=1)
def reduced_lagrangians() -> tuple[sp.Expr, sp.Expr, tuple[sp.Symbol, ...]]:
    time, radius, theta, phi = sp.symbols("t R theta phi", real=True)
    ratio = sp.symbols("r", positive=True, real=True)
    lapse = sp.Function("N")(radius)
    radial_metric = sp.Function("A")(radius)
    radial_flow = sp.Function("a")(radius)
    angular_flow = sp.Function("b")(radius)
    sine = sp.sin(theta)
    cosine = sp.cos(theta)
    coordinates = [time, radius, theta, phi]
    metric = [
        -lapse**2,
        radial_metric**2,
        radius**2,
        radius**2 * sine**2,
    ]
    inverse_metric = [
        -1 / lapse**2,
        1 / radial_metric**2,
        1 / radius**2,
        1 / (radius**2 * sine**2),
    ]
    christoffel: dict[tuple[int, int, int], sp.Expr] = {}

    def symmetric(index: int, first: int, second: int, value: sp.Expr) -> None:
        christoffel[(index, first, second)] = value
        christoffel[(index, second, first)] = value

    symmetric(0, 0, 1, sp.diff(lapse, radius) / lapse)
    christoffel[(1, 0, 0)] = lapse * sp.diff(lapse, radius) / radial_metric**2
    christoffel[(1, 1, 1)] = sp.diff(radial_metric, radius) / radial_metric
    christoffel[(1, 2, 2)] = -radius / radial_metric**2
    christoffel[(1, 3, 3)] = -radius * sine**2 / radial_metric**2
    symmetric(2, 1, 2, 1 / radius)
    christoffel[(2, 3, 3)] = -sine * cosine
    symmetric(3, 1, 3, 1 / radius)
    symmetric(3, 2, 3, cosine / sine)

    spatial_norm = radial_flow**2 * cosine**2 + angular_flow**2 * sine**2
    contravariant_flow = [
        {
            0: 1 / lapse,
            2: spatial_norm / (2 * lapse),
            4: (spatial_norm / 2 - spatial_norm**2 / 8) / lapse,
        },
        {
            1: radial_flow * cosine / radial_metric,
            3: radial_flow * cosine / (2 * radial_metric),
        },
        {
            1: -angular_flow * sine / radius,
            3: -angular_flow * sine / (2 * radius),
        },
        {},
    ]
    covariant_flow = [
        _scale(contravariant_flow[index], metric[index]) for index in range(4)
    ]
    covariant_derivative: list[list[dict[int, sp.Expr]]] = []
    for derivative_index in range(4):
        row: list[dict[int, sp.Expr]] = []
        for vector_index in range(4):
            terms = [
                _differentiate(
                    covariant_flow[vector_index], coordinates[derivative_index]
                )
            ]
            terms.extend(
                _scale(
                    covariant_flow[contracted],
                    -christoffel[(contracted, derivative_index, vector_index)],
                )
                for contracted in range(4)
                if (contracted, derivative_index, vector_index) in christoffel
            )
            row.append(_add(*terms))
        covariant_derivative.append(row)

    invariant_1: dict[int, sp.Expr] = {}
    invariant_3: dict[int, sp.Expr] = {}
    for first in range(4):
        for second in range(4):
            weight = inverse_metric[first] * inverse_metric[second]
            invariant_1 = _add(
                invariant_1,
                _scale(
                    _multiply(
                        covariant_derivative[first][second],
                        covariant_derivative[first][second],
                    ),
                    weight,
                ),
            )
            invariant_3 = _add(
                invariant_3,
                _scale(
                    _multiply(
                        covariant_derivative[first][second],
                        covariant_derivative[second][first],
                    ),
                    weight,
                ),
            )

    expansion: dict[int, sp.Expr] = {}
    for index in range(4):
        expansion = _add(
            expansion,
            _differentiate(contravariant_flow[index], coordinates[index]),
        )
        for contracted in range(4):
            if (index, index, contracted) in christoffel:
                expansion = _add(
                    expansion,
                    _scale(
                        contravariant_flow[contracted],
                        christoffel[(index, index, contracted)],
                    ),
                )
    invariant_2 = _multiply(expansion, expansion)

    acceleration: list[dict[int, sp.Expr]] = []
    for vector_index in range(4):
        component: dict[int, sp.Expr] = {}
        for derivative_index in range(4):
            component = _add(
                component,
                _multiply(
                    contravariant_flow[derivative_index],
                    covariant_derivative[derivative_index][vector_index],
                ),
            )
        acceleration.append(component)
    invariant_4: dict[int, sp.Expr] = {}
    for index in range(4):
        invariant_4 = _add(
            invariant_4,
            _scale(
                _multiply(acceleration[index], acceleration[index]),
                inverse_metric[index],
            ),
        )

    c_1 = (1 + ratio) / 2
    c_3 = -c_1
    c_2 = sp.Rational(2, 3) / (1 + ratio)
    c_14 = 2 * ratio / (1 + ratio)
    c_4 = c_14 - c_1
    kinetic = _add(
        _scale(invariant_1, c_1),
        _scale(invariant_2, c_2),
        _scale(invariant_3, c_3),
        _scale(invariant_4, -c_4),
    )
    measure = 2 * sp.pi * lapse * radial_metric * radius**2 * sine
    lagrangian_2 = sp.factor(
        sp.integrate(sp.expand_trig(sp.expand(measure * kinetic[2])), (theta, 0, sp.pi))
    )
    lagrangian_4 = sp.factor(
        sp.integrate(sp.expand_trig(sp.expand(measure * kinetic[4])), (theta, 0, sp.pi))
    )
    lapse_value, radial_metric_value, lapse_prime = sp.symbols(
        "N_value A_value N_prime", positive=True, real=True
    )
    radial_flow_value, angular_flow_value = sp.symbols("a_value b_value", real=True)
    radial_flow_prime, angular_flow_prime = sp.symbols(
        "a_prime b_prime", real=True
    )
    substitutions = {
        lapse: lapse_value,
        radial_metric: radial_metric_value,
        sp.diff(lapse, radius): lapse_prime,
        radial_flow: radial_flow_value,
        angular_flow: angular_flow_value,
        sp.diff(radial_flow, radius): radial_flow_prime,
        sp.diff(angular_flow, radius): angular_flow_prime,
    }
    arguments = (
        radius,
        ratio,
        lapse_value,
        radial_metric_value,
        lapse_prime,
        radial_flow_value,
        angular_flow_value,
        radial_flow_prime,
        angular_flow_prime,
    )
    return (
        sp.factor(lagrangian_2.subs(substitutions)),
        sp.factor(lagrangian_4.subs(substitutions)),
        arguments,
    )


@lru_cache(maxsize=1)
def numeric_lagrangians():
    lagrangian_2, lagrangian_4, arguments = reduced_lagrangians()
    return (
        sp.lambdify(arguments, lagrangian_2, "numpy"),
        sp.lambdify(arguments, lagrangian_4, "numpy"),
    )


@lru_cache(maxsize=1)
def numeric_euler_matrices():
    lagrangian_2, _, arguments = reduced_lagrangians()
    (
        radius,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        radial_flow,
        angular_flow,
        radial_flow_prime,
        angular_flow_prime,
    ) = arguments
    flow = sp.Matrix([radial_flow, angular_flow])
    flow_prime = sp.Matrix([radial_flow_prime, angular_flow_prime])
    derivative_matrix = sp.hessian(lagrangian_2, flow_prime)
    mixed_matrix = sp.Matrix(
        2,
        2,
        lambda first, second: sp.diff(
            lagrangian_2, flow_prime[first], flow[second]
        ),
    )
    flow_matrix = sp.hessian(lagrangian_2, flow)
    radial_metric_prime, lapse_second = sp.symbols(
        "A_prime N_second", real=True
    )

    def total_derivative(matrix: sp.Matrix) -> sp.Matrix:
        return matrix.applyfunc(
            lambda entry: sp.diff(entry, radius)
            + sp.diff(entry, lapse) * lapse_prime
            + sp.diff(entry, radial_metric) * radial_metric_prime
            + sp.diff(entry, lapse_prime) * lapse_second
        )

    derivative_matrix_prime = total_derivative(derivative_matrix)
    mixed_matrix_prime = total_derivative(mixed_matrix)
    matrix_arguments = (
        radius,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        radial_metric_prime,
        lapse_second,
    )

    def entries(matrix: sp.Matrix):
        return [
            sp.lambdify(matrix_arguments, matrix[first, second], "numpy")
            for first in range(2)
            for second in range(2)
        ]

    return (
        entries(derivative_matrix),
        entries(derivative_matrix_prime),
        entries(mixed_matrix),
        entries(mixed_matrix_prime),
        entries(flow_matrix),
    )


def tolman_vii_background(
    compactness: float, radii: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    central_density = 15 * compactness / (8 * math.pi)

    def mass(radius: np.ndarray | float) -> np.ndarray | float:
        return compactness * (5 * np.asarray(radius) ** 3 - 3 * np.asarray(radius) ** 5) / 2

    surface_lapse = math.sqrt(1 - 2 * compactness)

    def equations(radius: float, state: np.ndarray) -> np.ndarray:
        pressure, log_lapse = state
        density = central_density * (1 - radius**2)
        enclosed_mass = float(mass(radius))
        potential = (enclosed_mass + 4 * math.pi * radius**3 * pressure) / (
            radius * (radius - 2 * enclosed_mass)
        )
        return np.array([-(density + pressure) * potential, potential])

    minimum_radius = max(float(np.min(radii[radii > 0])), 1.0e-6)
    interior_solution = solve_ivp(
        equations,
        (1.0, minimum_radius),
        np.array([0.0, math.log(surface_lapse)]),
        rtol=2.0e-11,
        atol=2.0e-13,
        dense_output=True,
        max_step=0.005,
    )
    if not interior_solution.success:
        raise RuntimeError(interior_solution.message)

    lapse = np.empty_like(radii)
    radial_metric = np.empty_like(radii)
    lapse_prime = np.empty_like(radii)
    radial_metric_prime = np.empty_like(radii)
    lapse_second = np.empty_like(radii)
    interior = radii <= 1
    interior_radii = radii[interior]
    pressure, log_lapse = interior_solution.sol(interior_radii)
    density = central_density * (1 - interior_radii**2)
    enclosed_mass = mass(interior_radii)
    enclosed_mass_prime = (
        15 * compactness * interior_radii**2 * (1 - interior_radii**2) / 2
    )
    potential = (enclosed_mass + 4 * math.pi * interior_radii**3 * pressure) / (
        interior_radii * (interior_radii - 2 * enclosed_mass)
    )
    pressure_prime = -(density + pressure) * potential
    potential_numerator = enclosed_mass + 4 * math.pi * interior_radii**3 * pressure
    potential_denominator = interior_radii * (interior_radii - 2 * enclosed_mass)
    numerator_prime = (
        enclosed_mass_prime
        + 12 * math.pi * interior_radii**2 * pressure
        + 4 * math.pi * interior_radii**3 * pressure_prime
    )
    denominator_prime = (
        2 * interior_radii
        - 2 * enclosed_mass
        - 2 * interior_radii * enclosed_mass_prime
    )
    potential_prime = (
        numerator_prime * potential_denominator
        - potential_numerator * denominator_prime
    ) / potential_denominator**2
    lapse[interior] = np.exp(log_lapse)
    radial_metric[interior] = 1 / np.sqrt(1 - 2 * enclosed_mass / interior_radii)
    lapse_prime[interior] = lapse[interior] * potential
    radial_metric_prime[interior] = radial_metric[interior] ** 3 * (
        enclosed_mass_prime / interior_radii
        - enclosed_mass / interior_radii**2
    )
    lapse_second[interior] = lapse[interior] * (
        potential**2 + potential_prime
    )

    exterior_radii = radii[~interior]
    exterior_lapse = np.sqrt(1 - 2 * compactness / exterior_radii)
    lapse[~interior] = exterior_lapse
    radial_metric[~interior] = 1 / exterior_lapse
    lapse_prime[~interior] = compactness / (exterior_radii**2 * exterior_lapse)
    radial_metric_prime[~interior] = -lapse_prime[~interior] / exterior_lapse**2
    lapse_second[~interior] = (
        -2 * compactness / (exterior_radii**3 * exterior_lapse)
        - compactness**2 / (exterior_radii**4 * exterior_lapse**3)
    )
    return lapse, radial_metric, lapse_prime, radial_metric_prime, lapse_second


def radial_grid(maximum_radius: float, interior_points: int, exterior_points: int) -> np.ndarray:
    interior = np.linspace(1.0e-4, 1.0, interior_points)
    exterior = np.geomspace(1.0 + 1.0e-6, maximum_radius, exterior_points)
    return np.concatenate([interior, exterior])


def aether_surface_coefficients(
    compactness: float,
    ratio: float,
    radial_tail: float,
    angular_tail: float,
) -> tuple[float, float]:
    quadratic_numerator = (
        9 * compactness * ratio**2
        - 36 * compactness * ratio
        + 11 * compactness
        + 3 * radial_tail * ratio**2
        + radial_tail
        + 12 * angular_tail * ratio
        + 4 * angular_tail
    )
    quartic_numerator = (
        45 * compactness * ratio**2
        - 135 * compactness * ratio
        + 50 * compactness
        + 12 * radial_tail * ratio**2
        - 9 * radial_tail * ratio
        + 7 * radial_tail
        - 12 * angular_tail * ratio**2
        + 54 * angular_tail * ratio
        - 2 * angular_tail
    )
    return (
        quadratic_numerator / (18 * (1 + ratio)),
        quartic_numerator / (45 * (1 + ratio)),
    )


def basis_arrays(radii: np.ndarray, count: int, maximum_scale: float):
    scales = np.geomspace(0.2, maximum_scale, count)
    functions: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = []
    for scale in scales:
        coordinate = radii / scale
        common = (1 + 2 * coordinate) / (1 + coordinate) ** 2
        common_prime = -2 * coordinate / (scale * (1 + coordinate) ** 3)
        difference = coordinate**2 / (1 + coordinate) ** 3
        difference_prime = coordinate * (2 - coordinate) / (
            scale * (1 + coordinate) ** 4
        )
        functions.append((common, common_prime, common, common_prime))
        functions.append(
            (difference, difference_prime, -difference, -difference_prime)
        )
    return scales, functions


def solve_profile(
    compactness: float,
    ratio: float,
    basis_count: int = 7,
    maximum_radius: float = 300.0,
    interior_points: int = 700,
    exterior_points: int = 1800,
) -> dict[str, object]:
    radii = radial_grid(maximum_radius, interior_points, exterior_points)
    lapse, radial_metric, lapse_prime, _, _ = tolman_vii_background(
        compactness, radii
    )
    lagrangian_2, lagrangian_4 = numeric_lagrangians()
    scales, basis = basis_arrays(radii, basis_count, maximum_radius / 4)

    def fields(coefficients: np.ndarray):
        radial_flow = np.ones_like(radii)
        angular_flow = np.ones_like(radii)
        radial_prime = np.zeros_like(radii)
        angular_prime = np.zeros_like(radii)
        for coefficient, components in zip(coefficients, basis):
            radial_flow += coefficient * components[0]
            radial_prime += coefficient * components[1]
            angular_flow += coefficient * components[2]
            angular_prime += coefficient * components[3]
        return radial_flow, angular_flow, radial_prime, angular_prime

    def integrate_lagrangian(function, coefficients: np.ndarray) -> float:
        flow = fields(coefficients)
        values = function(
            radii,
            ratio,
            lapse,
            radial_metric,
            lapse_prime,
            flow[0],
            flow[1],
            flow[2],
            flow[3],
        )
        return float(simpson(values, x=radii))

    dimension = len(basis)
    zero = np.zeros(dimension)
    energy_zero = integrate_lagrangian(lagrangian_2, zero)
    linear = np.zeros(dimension)
    hessian = np.zeros((dimension, dimension))
    positive_energies = np.zeros(dimension)
    for index in range(dimension):
        positive = zero.copy()
        negative = zero.copy()
        positive[index] = 1
        negative[index] = -1
        energy_positive = integrate_lagrangian(lagrangian_2, positive)
        energy_negative = integrate_lagrangian(lagrangian_2, negative)
        positive_energies[index] = energy_positive
        linear[index] = (energy_positive - energy_negative) / 2
        hessian[index, index] = energy_positive + energy_negative - 2 * energy_zero
    for first in range(dimension):
        for second in range(first + 1, dimension):
            combined = zero.copy()
            combined[first] = 1
            combined[second] = 1
            energy_combined = integrate_lagrangian(lagrangian_2, combined)
            entry = (
                energy_combined
                - positive_energies[first]
                - positive_energies[second]
                + energy_zero
            )
            hessian[first, second] = entry
            hessian[second, first] = entry
    eigenvalues = np.linalg.eigvalsh((hessian + hessian.T) / 2)
    coefficients = np.linalg.solve(hessian, -linear)
    energy_2 = integrate_lagrangian(lagrangian_2, coefficients)
    energy_4 = integrate_lagrangian(lagrangian_4, coefficients)
    radial_flow, angular_flow, radial_prime, angular_prime = fields(coefficients)
    return {
        "compactness": compactness,
        "ratio": ratio,
        "basis_count": basis_count,
        "maximum_radius": maximum_radius,
        "scales": scales,
        "coefficients": coefficients,
        "hessian_eigenvalues": eigenvalues,
        "energy_2": energy_2,
        "energy_4": energy_4,
        "f_action": -energy_2 / (8 * math.pi * compactness),
        "kappa_action": energy_4 / (16 * math.pi * compactness),
        "profile_center": (radial_flow[0], angular_flow[0]),
        "profile_outer": (radial_flow[-1], angular_flow[-1]),
        "derivative_center": (radial_prime[0], angular_prime[0]),
    }


def _matrix_values(functions, arguments: tuple[np.ndarray | float, ...]) -> np.ndarray:
    size = np.asarray(arguments[0]).size
    values: list[np.ndarray] = []
    for function in functions:
        value = np.asarray(function(*arguments), dtype=float)
        if value.ndim == 0:
            value = np.full(size, float(value))
        values.append(np.broadcast_to(value, (size,)))
    return np.asarray(values).reshape(2, 2, size)


def solve_bvp_profile(
    compactness: float,
    ratio: float,
    maximum_radius: float = 200.0,
    tolerance: float = 1.0e-7,
) -> dict[str, object]:
    matrix_functions = numeric_euler_matrices()
    interior_mesh = np.linspace(1.0e-3, 1.0, 180)
    exterior_mesh = np.geomspace(1.0 + 1.0e-6, maximum_radius, 420)
    mesh = np.concatenate([interior_mesh, exterior_mesh])

    def differential_equations(radii: np.ndarray, state: np.ndarray) -> np.ndarray:
        background = tolman_vii_background(compactness, radii)
        arguments = (radii, ratio, *background)
        derivative_matrix = _matrix_values(matrix_functions[0], arguments)
        derivative_matrix_prime = _matrix_values(matrix_functions[1], arguments)
        mixed_matrix = _matrix_values(matrix_functions[2], arguments)
        mixed_matrix_prime = _matrix_values(matrix_functions[3], arguments)
        flow_matrix = _matrix_values(matrix_functions[4], arguments)
        flow = state[:2]
        flow_prime = state[2:]
        right_hand_side = -np.einsum(
            "ijn,jn->in",
            derivative_matrix_prime
            + mixed_matrix
            - np.swapaxes(mixed_matrix, 0, 1),
            flow_prime,
        ) - np.einsum(
            "ijn,jn->in", mixed_matrix_prime - flow_matrix, flow
        )
        flow_second = np.empty_like(flow)
        for index in range(radii.size):
            flow_second[:, index] = np.linalg.solve(
                derivative_matrix[:, :, index], right_hand_side[:, index]
            )
        return np.vstack([flow_prime, flow_second])

    def boundary_conditions(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.array(
            [
                left[0] - left[1],
                left[2],
                maximum_radius * right[2] + right[0] - 1,
                maximum_radius * right[3] + right[1] - 1,
            ]
        )

    initial = np.zeros((4, mesh.size))
    initial[0] = 1
    initial[1] = 1
    solution = solve_bvp(
        differential_equations,
        boundary_conditions,
        mesh,
        initial,
        tol=tolerance,
        max_nodes=25000,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    radii = radial_grid(maximum_radius, 1000, 3000)
    lapse, radial_metric, lapse_prime, _, _ = tolman_vii_background(
        compactness, radii
    )
    state = solution.sol(radii)
    lagrangian_2, lagrangian_4 = numeric_lagrangians()
    common_arguments = (
        radii,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        state[0],
        state[1],
        state[2],
        state[3],
    )
    energy_2 = float(simpson(lagrangian_2(*common_arguments), x=radii))
    energy_4 = float(simpson(lagrangian_4(*common_arguments), x=radii))
    radial_tail = float(
        0.5
        * (
            maximum_radius * (solution.y[0, -1] - 1)
            - maximum_radius**2 * solution.y[2, -1]
        )
    )
    angular_tail = float(
        0.5
        * (
            maximum_radius * (solution.y[1, -1] - 1)
            - maximum_radius**2 * solution.y[3, -1]
        )
    )
    surface_energy_2, surface_energy_4 = aether_surface_coefficients(
        compactness,
        ratio,
        radial_tail,
        angular_tail,
    )
    total_mass_2 = energy_2 / (16 * math.pi) + surface_energy_2
    total_mass_4 = energy_4 / (16 * math.pi) + surface_energy_4
    return {
        "compactness": compactness,
        "ratio": ratio,
        "maximum_radius": maximum_radius,
        "node_count": solution.x.size,
        "maximum_rms_residual": float(np.max(solution.rms_residuals)),
        "energy_2": energy_2,
        "energy_4": energy_4,
        "f_action": -energy_2 / (8 * math.pi * compactness),
        "kappa_action": energy_4 / (16 * math.pi * compactness),
        "surface_energy_2": surface_energy_2,
        "surface_energy_4": surface_energy_4,
        "f_with_surface": -2 * total_mass_2 / compactness,
        "kappa_with_surface": total_mass_4 / compactness,
        "raw_bulk_plus_aether_f_diagnostic": -2 * total_mass_2 / compactness,
        "raw_bulk_plus_aether_kappa_diagnostic": total_mass_4 / compactness,
        "profile_center": (state[0, 0], state[1, 0]),
        "profile_outer": (state[0, -1], state[1, -1]),
        "derivative_center": (state[2, 0], state[3, 0]),
        "radial_tail": radial_tail,
        "angular_tail": angular_tail,
    }


def solve_extrapolated_bvp_profile(
    compactness: float,
    ratio: float,
    base_maximum_radius: float = 200.0,
    tolerance: float = 1.0e-7,
) -> dict[str, object]:
    coarse = solve_bvp_profile(
        compactness,
        ratio,
        maximum_radius=base_maximum_radius,
        tolerance=tolerance,
    )
    fine = solve_bvp_profile(
        compactness,
        ratio,
        maximum_radius=2 * base_maximum_radius,
        tolerance=tolerance,
    )
    extrapolated_keys = (
        "energy_2",
        "energy_4",
        "f_action",
        "kappa_action",
        "surface_energy_2",
        "surface_energy_4",
        "radial_tail",
        "angular_tail",
    )
    result: dict[str, object] = {
        "compactness": compactness,
        "ratio": ratio,
        "base_maximum_radius": base_maximum_radius,
        "coarse_node_count": coarse["node_count"],
        "fine_node_count": fine["node_count"],
        "coarse_maximum_rms_residual": coarse["maximum_rms_residual"],
        "fine_maximum_rms_residual": fine["maximum_rms_residual"],
    }
    for key in extrapolated_keys:
        result[f"coarse_{key}"] = coarse[key]
        result[f"fine_{key}"] = fine[key]
        result[key] = 2 * float(fine[key]) - float(coarse[key])
    total_mass_2 = float(result["energy_2"]) / (16 * math.pi) + float(
        result["surface_energy_2"]
    )
    total_mass_4 = float(result["energy_4"]) / (16 * math.pi) + float(
        result["surface_energy_4"]
    )
    result["raw_bulk_plus_aether_f_diagnostic"] = (
        -2 * total_mass_2 / compactness
    )
    result["raw_bulk_plus_aether_kappa_diagnostic"] = (
        total_mass_4 / compactness
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compactness", type=float, default=0.03)
    parser.add_argument("--ratio", type=float, default=1 / 3)
    parser.add_argument("--basis-count", type=int, default=6)
    parser.add_argument("--maximum-radius", type=float, default=200.0)
    parser.add_argument("--bvp", action="store_true")
    parser.add_argument("--extrapolate", action="store_true")
    args = parser.parse_args()
    if args.extrapolate:
        result = solve_extrapolated_bvp_profile(
            args.compactness,
            args.ratio,
            base_maximum_radius=args.maximum_radius,
        )
    elif args.bvp:
        result = solve_bvp_profile(
            args.compactness,
            args.ratio,
            maximum_radius=args.maximum_radius,
        )
    else:
        result = solve_profile(
            args.compactness,
            args.ratio,
            basis_count=args.basis_count,
            maximum_radius=args.maximum_radius,
        )
    for key, value in result.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
