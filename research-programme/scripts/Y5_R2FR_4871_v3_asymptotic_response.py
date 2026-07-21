from __future__ import annotations

import argparse
import json
import math
from functools import lru_cache

import numpy as np
import sympy as sp
from scipy.integrate import simpson, solve_bvp

from Y5_R2FR_4868_fixed_background_variational_remainder import (
    numeric_euler_matrices,
    numeric_lagrangians,
    radial_grid,
    reduced_lagrangians,
    tolman_vii_background,
)


def matrix_values(
    functions: list,
    arguments: tuple[np.ndarray | float, ...],
) -> np.ndarray:
    size = np.asarray(arguments[0]).size
    values: list[np.ndarray] = []
    for function in functions:
        value = np.asarray(function(*arguments), dtype=float)
        if value.ndim == 0:
            value = np.full(size, float(value))
        values.append(np.broadcast_to(value, (size,)))
    return np.asarray(values).reshape(2, 2, size)


@lru_cache(maxsize=1)
def numeric_v3_source() -> tuple:
    _, lagrangian_4, arguments = reduced_lagrangians()
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
    radial_metric_prime, lapse_second = sp.symbols(
        "A_prime N_second", real=True
    )
    radial_flow_second, angular_flow_second = sp.symbols(
        "a_second b_second", real=True
    )
    flow = (radial_flow, angular_flow)
    flow_prime = (radial_flow_prime, angular_flow_prime)
    flow_second = (radial_flow_second, angular_flow_second)

    def total_derivative(expression: sp.Expr) -> sp.Expr:
        return (
            sp.diff(expression, radius)
            + sp.diff(expression, lapse) * lapse_prime
            + sp.diff(expression, radial_metric) * radial_metric_prime
            + sp.diff(expression, lapse_prime) * lapse_second
            + sum(
                sp.diff(expression, flow[index]) * flow_prime[index]
                + sp.diff(expression, flow_prime[index]) * flow_second[index]
                for index in range(2)
            )
        )

    source = tuple(
        total_derivative(sp.diff(lagrangian_4, flow_prime[index]))
        - sp.diff(lagrangian_4, flow[index])
        for index in range(2)
    )
    source_arguments = (
        radius,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        radial_metric_prime,
        lapse_second,
        radial_flow,
        angular_flow,
        radial_flow_prime,
        angular_flow_prime,
        radial_flow_second,
        angular_flow_second,
    )
    return tuple(
        sp.lambdify(source_arguments, component, "numpy", cse=True)
        for component in source
    )


@lru_cache(maxsize=1)
def numeric_l2_first_variation() -> tuple:
    lagrangian_2, _, arguments = reduced_lagrangians()
    (
        _,
        _,
        _,
        _,
        _,
        radial_flow,
        angular_flow,
        radial_flow_prime,
        angular_flow_prime,
    ) = arguments
    q3_radial, q3_angular, q3_radial_prime, q3_angular_prime = sp.symbols(
        "q3_radial q3_angular q3_radial_prime q3_angular_prime", real=True
    )
    variation = (
        sp.diff(lagrangian_2, radial_flow) * q3_radial
        + sp.diff(lagrangian_2, angular_flow) * q3_angular
        + sp.diff(lagrangian_2, radial_flow_prime) * q3_radial_prime
        + sp.diff(lagrangian_2, angular_flow_prime) * q3_angular_prime
    )
    variation_arguments = (
        *arguments,
        q3_radial,
        q3_angular,
        q3_radial_prime,
        q3_angular_prime,
    )
    return sp.lambdify(variation_arguments, variation, "numpy", cse=True)


def euler_coefficients(
    compactness: float,
    ratio: float,
    radii: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[np.ndarray, ...]]:
    background = tolman_vii_background(compactness, radii)
    arguments = (radii, ratio, *background)
    matrices = numeric_euler_matrices()
    derivative_matrix = matrix_values(matrices[0], arguments)
    derivative_matrix_prime = matrix_values(matrices[1], arguments)
    mixed_matrix = matrix_values(matrices[2], arguments)
    mixed_matrix_prime = matrix_values(matrices[3], arguments)
    flow_matrix = matrix_values(matrices[4], arguments)
    first_derivative_matrix = (
        derivative_matrix_prime
        + mixed_matrix
        - np.swapaxes(mixed_matrix, 0, 1)
    )
    field_matrix = mixed_matrix_prime - flow_matrix
    return (
        derivative_matrix,
        first_derivative_matrix,
        field_matrix,
        background,
    )


def solve_leading_profile(
    compactness: float,
    ratio: float,
    maximum_radius: float,
    tolerance: float,
) -> solve_bvp:
    interior_mesh = np.linspace(1.0e-3, 1.0, 180)
    exterior_mesh = np.geomspace(1.0 + 1.0e-6, maximum_radius, 420)
    mesh = np.concatenate([interior_mesh, exterior_mesh])

    def equations(radii: np.ndarray, state: np.ndarray) -> np.ndarray:
        derivative, first_derivative, field, _ = euler_coefficients(
            compactness, ratio, radii
        )
        right_hand_side = -np.einsum(
            "ijn,jn->in", first_derivative, state[2:]
        ) - np.einsum("ijn,jn->in", field, state[:2])
        second = np.empty_like(state[:2])
        for index in range(radii.size):
            second[:, index] = np.linalg.solve(
                derivative[:, :, index], right_hand_side[:, index]
            )
        return np.vstack([state[2:], second])

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
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
        equations,
        boundary,
        mesh,
        initial,
        tol=tolerance,
        max_nodes=30000,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def solve_residual_profile(
    compactness: float,
    ratio: float,
    maximum_radius: float,
    tolerance: float,
    leading_solution: solve_bvp,
) -> solve_bvp:
    mesh = leading_solution.x
    source_functions = numeric_v3_source()

    def equations(radii: np.ndarray, state: np.ndarray) -> np.ndarray:
        derivative, first_derivative, field, background = euler_coefficients(
            compactness, ratio, radii
        )
        leading = leading_solution.sol(radii)
        leading_second = np.empty_like(leading[:2])
        leading_rhs = -np.einsum(
            "ijn,jn->in", first_derivative, leading[2:]
        ) - np.einsum("ijn,jn->in", field, leading[:2])
        for index in range(radii.size):
            leading_second[:, index] = np.linalg.solve(
                derivative[:, :, index], leading_rhs[:, index]
            )
        source_arguments = (
            radii,
            ratio,
            *background,
            leading[0],
            leading[1],
            leading[2],
            leading[3],
            leading_second[0],
            leading_second[1],
        )
        source = np.vstack(
            [
                np.broadcast_to(
                    np.asarray(function(*source_arguments), dtype=float),
                    radii.shape,
                )
                for function in source_functions
            ]
        )
        right_hand_side = (
            -source
            - np.einsum("ijn,jn->in", first_derivative, state[2:])
            - np.einsum("ijn,jn->in", field, state[:2])
        )
        second = np.empty_like(state[:2])
        for index in range(radii.size):
            second[:, index] = np.linalg.solve(
                derivative[:, :, index], right_hand_side[:, index]
            )
        return np.vstack([state[2:], second])

    def boundary(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        return np.array(
            [
                left[0] - left[1],
                left[2],
                maximum_radius * right[2] + right[0],
                maximum_radius * right[3] + right[1],
            ]
        )

    initial = np.zeros((4, mesh.size))
    solution = solve_bvp(
        equations,
        boundary,
        mesh,
        initial,
        tol=tolerance,
        max_nodes=40000,
        verbose=0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution


def asymptotic_tail(
    value: float,
    derivative: float,
    maximum_radius: float,
    constant: float,
) -> float:
    return 0.5 * (
        maximum_radius * (value - constant)
        - maximum_radius**2 * derivative
    )


def solve_v3_profile(
    compactness: float,
    ratio: float,
    maximum_radius: float = 200.0,
    tolerance: float = 1.0e-7,
) -> dict[str, float | int]:
    leading_solution = solve_leading_profile(
        compactness, ratio, maximum_radius, tolerance
    )
    residual_solution = solve_residual_profile(
        compactness,
        ratio,
        maximum_radius,
        tolerance,
        leading_solution,
    )
    radii = radial_grid(maximum_radius, 1000, 3000)
    background = tolman_vii_background(compactness, radii)
    leading = leading_solution.sol(radii)
    residual = residual_solution.sol(radii)
    lagrangian_2, lagrangian_4 = numeric_lagrangians()
    common = (
        radii,
        ratio,
        background[0],
        background[1],
        background[2],
        leading[0],
        leading[1],
        leading[2],
        leading[3],
    )
    energy_2 = float(simpson(lagrangian_2(*common), x=radii))
    energy_4 = float(simpson(lagrangian_4(*common), x=radii))
    variation_density = numeric_l2_first_variation()(
        *common,
        residual[0],
        residual[1],
        residual[2],
        residual[3],
    )
    first_variation = float(simpson(variation_density, x=radii))
    leading_outer = leading_solution.y[:, -1]
    residual_outer = residual_solution.y[:, -1]
    return {
        "compactness": compactness,
        "ratio": ratio,
        "maximum_radius": maximum_radius,
        "leading_nodes": leading_solution.x.size,
        "residual_nodes": residual_solution.x.size,
        "leading_maximum_rms_residual": float(
            np.max(leading_solution.rms_residuals)
        ),
        "v3_maximum_rms_residual": float(
            np.max(residual_solution.rms_residuals)
        ),
        "energy_2": energy_2,
        "energy_4": energy_4,
        "f_action": -energy_2 / (8 * math.pi * compactness),
        "kappa4_action": energy_4 / (16 * math.pi * compactness),
        "l2_first_variation_q3": first_variation,
        "q1_radial_tail": asymptotic_tail(
            leading_outer[0], leading_outer[2], maximum_radius, 1.0
        ),
        "q1_angular_tail": asymptotic_tail(
            leading_outer[1], leading_outer[3], maximum_radius, 1.0
        ),
        "q3_radial_tail": asymptotic_tail(
            residual_outer[0], residual_outer[2], maximum_radius, 0.0
        ),
        "q3_angular_tail": asymptotic_tail(
            residual_outer[1], residual_outer[3], maximum_radius, 0.0
        ),
        "q3_center_radial": float(residual_solution.y[0, 0]),
        "q3_center_angular": float(residual_solution.y[1, 0]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compactness", type=float, default=0.3)
    parser.add_argument("--ratio", type=float, default=1 / 3)
    parser.add_argument("--maximum-radius", type=float, default=200.0)
    parser.add_argument("--tolerance", type=float, default=1.0e-7)
    arguments = parser.parse_args()
    result = solve_v3_profile(
        arguments.compactness,
        arguments.ratio,
        arguments.maximum_radius,
        arguments.tolerance,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
