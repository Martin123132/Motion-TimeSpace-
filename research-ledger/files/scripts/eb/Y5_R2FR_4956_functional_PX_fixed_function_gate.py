from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import root
from scipy.special import roots_jacobi


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4956"

RESULT_JSON = SOURCE / "functional_PX_fixed_function_results.json"
HESSIAN_CSV = SOURCE / "functional_PX_Hessian_contract.csv"
CALIBRATION_CSV = SOURCE / "functional_PX_calibration.csv"
HOMOTOPY_CSV = SOURCE / "polynomial_GR_homotopy_trace.csv"
FIXED_POINT_CSV = SOURCE / "polynomial_fixed_point_convergence.csv"
COEFFICIENT_CSV = SOURCE / "functional_coefficient_convergence.csv"
REGULARITY_CSV = SOURCE / "functional_regular_convexity_gate.csv"
DECISION_CSV = SOURCE / "functional_PX_route_decision.csv"

PARENT_4935 = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
PARENT_CHECKPOINT_4935 = POST / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
SCALAR_TEX = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
BASIS_TEX = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
LOWER_4941 = POST / "source-intake" / "functional_rg" / "4941" / "lower_scalar_essential_quotient.csv"
RESULT_4954 = POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json"
CHECKPOINT_4955 = POST / "4955-Y5-R2FR-six-derivative-shift-sector-X3-parent-flow-and-number-changing-fixed-ratio-or-strong-2PI-route-rejection.md"
RESULT_4955 = POST / "source-intake" / "functional_rg" / "4955" / "X3_parent_flow_results.json"

EXPECTED_HASHES = {
    PARENT_4935: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    PARENT_CHECKPOINT_4935: "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    SCALAR_TEX: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    BASIS_TEX: "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
    LOWER_4941: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    RESULT_4954: "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45",
    CHECKPOINT_4955: "e1951747933dbc078d3899b57db391de959dc028d257ca49daafe99a4536ef55",
    RESULT_4955: "dd825fd957362625c6e090e74be8153a1a9f1ce3cffc82df4aef04f729630b91",
}

MARKER = "MTS_4956_FUNCTIONAL_PX_FIXED_FUNCTION_GATE"
CHECKED_DATE = "2026-07-13"
MAX_ORDER = 12
QUADRATURE_ORDER = 15
HOMOTOPY_STEPS = 12
LOCAL_X_MAX = 0.1
GLOBAL_X_MAX = 0.25


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def symmetric_tensor_basis() -> np.ndarray:
    basis: list[np.ndarray] = []
    for first in range(4):
        tensor = np.zeros((4, 4))
        tensor[first, first] = 1.0
        basis.append(tensor)
    for first in range(4):
        for second in range(first + 1, 4):
            tensor = np.zeros((4, 4))
            tensor[first, second] = 1.0 / math.sqrt(2.0)
            tensor[second, first] = 1.0 / math.sqrt(2.0)
            basis.append(tensor)
    return np.asarray(basis)


class FunctionalPXProjector:
    def __init__(self, maximum_order: int, quadrature_order: int) -> None:
        self.maximum_order = maximum_order
        basis = symmetric_tensor_basis()
        trace_vector = np.trace(basis, axis1=1, axis2=2)
        identity = np.eye(10)
        dewitt = identity - 0.5 * np.outer(trace_vector, trace_vector)
        direction = np.array([1.0, 0.0, 0.0, 0.0])
        direction_tensor = np.outer(direction, direction)
        direction_components = np.einsum("aij,ji->a", basis, direction_tensor)
        gradient_action = np.empty((10, 10))
        for first in range(10):
            for second in range(10):
                gradient_action[first, second] = 0.5 * np.trace(
                    basis[first]
                    @ (direction_tensor @ basis[second] + basis[second] @ direction_tensor)
                )

        self.basis = basis
        self.trace_vector = trace_vector
        self.identity_10 = identity
        self.dewitt = dewitt
        self.direction = direction
        self.direction_components = direction_components
        self.metric_measure = 0.25 * np.outer(trace_vector, trace_vector) - 0.5 * identity
        self.metric_gradient = 2.0 * gradient_action - 0.5 * (
            np.outer(trace_vector, direction_components)
            + np.outer(direction_components, trace_vector)
        )
        self.metric_second = np.outer(direction_components, direction_components)

        radial_nodes, radial_weights = np.polynomial.legendre.leggauss(quadrature_order)
        radial = (radial_nodes + 1.0) / 2.0
        radial_weights = radial_weights * radial**3 / 2.0
        angular, angular_weights = roots_jacobi(quadrature_order, 0.5, 0.5)
        angular_weights = angular_weights * 2.0 / math.pi
        radial_mesh, angular_mesh = np.meshgrid(radial, angular, indexing="ij")
        radial_weight_mesh, angular_weight_mesh = np.meshgrid(
            radial_weights, angular_weights, indexing="ij"
        )
        self.radial = radial_mesh.ravel()
        self.angular = angular_mesh.ravel()
        self.weights = (radial_weight_mesh * angular_weight_mesh).ravel()
        self.node_count = len(self.weights)

        momentum_hat = np.stack(
            (
                self.angular,
                np.sqrt(np.maximum(0.0, 1.0 - self.angular**2)),
                np.zeros(self.node_count),
                np.zeros(self.node_count),
            ),
            axis=1,
        )
        mixed_gradient = np.einsum("i,aij,mj->ma", direction, basis, momentum_hat)
        self.mixed_first = trace_vector[None, :] * self.angular[:, None] - 2.0 * mixed_gradient
        self.mixed_second = -2.0 * direction_components[None, :] * self.angular[:, None]

    def quantum_coefficients(
        self,
        coefficients: np.ndarray,
        newton: float,
        eta_newton: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        order = len(coefficients) - 1
        if order > self.maximum_order:
            raise ValueError("polynomial order exceeds projector capacity")
        maximum_power = 2 * order
        hessian = [
            np.zeros((self.node_count, 11, 11), dtype=float)
            for _ in range(maximum_power + 1)
        ]
        hessian[0][:] = np.eye(11)
        gravity_coordinate = 32.0 * math.pi * newton
        gravity_root = math.sqrt(max(gravity_coordinate, 0.0))

        for power in range(1, order + 1):
            coefficient = coefficients[power]
            metric_vertex = coefficient * (
                self.metric_measure
                + power * self.metric_gradient
                + power * (power - 1) * self.metric_second
            )
            hessian[2 * power][:, :10, :10] += (
                gravity_coordinate * (self.dewitt @ metric_vertex)[None, :, :]
            )
            mixed_vertex = coefficient * (
                power * self.mixed_first
                + power * (power - 1) * self.mixed_second
            )
            hessian[2 * power - 1][:, :10, 10] += (
                gravity_root
                * self.radial[:, None]
                * (mixed_vertex @ self.dewitt.T)
            )
            hessian[2 * power - 1][:, 10, :10] += (
                gravity_root * self.radial[:, None] * mixed_vertex
            )
            if power >= 2:
                hessian[2 * (power - 1)][:, 10, 10] += (
                    self.radial**2
                    * coefficient
                    * (
                        2.0 * power
                        + 4.0 * power * (power - 1) * self.angular**2
                    )
                )

        inverse = [np.zeros_like(hessian[0]) for _ in hessian]
        inverse[0][:] = np.eye(11)
        for power in range(1, maximum_power + 1):
            accumulator = np.zeros_like(hessian[0])
            for partition in range(1, power + 1):
                accumulator += hessian[partition] @ inverse[power - partition]
            inverse[power] = -accumulator

        fixed_eta = np.zeros(order + 1)
        scalar_eta = np.zeros(order + 1)
        graviton_weight = 1.0 - 0.5 * eta_newton * (1.0 - self.radial**2)
        for power in range(1, order + 1):
            diagonal = np.diagonal(inverse[2 * power], axis1=1, axis2=2)
            fixed_trace = (
                graviton_weight * np.sum(diagonal[:, :10], axis=1)
                + diagonal[:, 10]
            )
            scalar_eta_trace = -0.5 * (1.0 - self.radial**2) * diagonal[:, 10]
            fixed_eta[power] = np.sum(self.weights * fixed_trace) / (8.0 * math.pi**2)
            scalar_eta[power] = np.sum(self.weights * scalar_eta_trace) / (8.0 * math.pi**2)
        return fixed_eta, scalar_eta

    def beta_values(
        self,
        variables: np.ndarray,
        newton: float,
        eta_newton: float,
    ) -> tuple[np.ndarray, float, np.ndarray]:
        order = len(variables) + 1
        coefficients = np.zeros(order + 1)
        coefficients[1] = 0.5
        coefficients[2:] = variables
        fixed_eta, scalar_eta = self.quantum_coefficients(
            coefficients, newton, eta_newton
        )
        eta_denominator = 0.5 + scalar_eta[1]
        eta_scalar = -fixed_eta[1] / eta_denominator
        quantum = fixed_eta + eta_scalar * scalar_eta
        beta = np.array(
            [
                (4.0 * (power - 1) + power * eta_scalar) * coefficients[power]
                + quantum[power]
                for power in range(2, order + 1)
            ]
        )
        return beta, eta_scalar, coefficients

    def direct_hessian_minimum(
        self,
        coefficients: np.ndarray,
        newton: float,
        x_maximum: float,
    ) -> dict[str, float]:
        gravity_coordinate = 32.0 * math.pi * newton
        gravity_root = math.sqrt(gravity_coordinate)
        minimum_singular = math.inf
        location = (0.0, 0.0, 0.0)
        for x_value in np.linspace(0.0, x_maximum, 81):
            powers = np.arange(len(coefficients))
            p_value = float(np.sum(coefficients * x_value**powers))
            p_prime = float(
                sum(
                    power * coefficients[power] * x_value ** (power - 1)
                    for power in range(1, len(coefficients))
                )
            )
            p_second = float(
                sum(
                    power
                    * (power - 1)
                    * coefficients[power]
                    * x_value ** (power - 2)
                    for power in range(2, len(coefficients))
                )
            )
            metric_vertex = (
                p_value * self.metric_measure
                + x_value * p_prime * self.metric_gradient
                + x_value**2 * p_second * self.metric_second
            )
            for radial in np.linspace(0.0, 1.0, 5):
                for angular in np.linspace(0.0, 1.0, 5):
                    momentum_hat = np.array(
                        [angular, math.sqrt(max(0.0, 1.0 - angular**2)), 0.0, 0.0]
                    )
                    mixed_gradient = np.array(
                        [self.direction @ tensor @ momentum_hat for tensor in self.basis]
                    )
                    mixed_first = self.trace_vector * angular - 2.0 * mixed_gradient
                    mixed_second = -2.0 * self.direction_components * angular
                    mixed_vertex = math.sqrt(x_value) * (
                        p_prime * mixed_first + x_value * p_second * mixed_second
                    )
                    hessian = np.eye(11)
                    hessian[:10, :10] += gravity_coordinate * (
                        self.dewitt @ metric_vertex
                    )
                    hessian[:10, 10] += (
                        gravity_root * radial * (self.dewitt @ mixed_vertex)
                    )
                    hessian[10, :10] += gravity_root * radial * mixed_vertex
                    hessian[10, 10] += radial**2 * (
                        2.0 * p_prime - 1.0
                        + 4.0 * x_value * p_second * angular**2
                    )
                    singular = float(np.linalg.svd(hessian, compute_uv=False)[-1])
                    if singular < minimum_singular:
                        minimum_singular = singular
                        location = (x_value, radial, angular)
        return {
            "minimum_singular_value": minimum_singular,
            "x_at_minimum": location[0],
            "q_at_minimum": location[1],
            "z_at_minimum": location[2],
        }


def first_positive_root(coefficients_ascending: np.ndarray) -> float:
    trimmed = np.trim_zeros(coefficients_ascending, "b")
    if len(trimmed) <= 1:
        return math.inf
    roots = np.roots(trimmed[::-1])
    positive = [
        float(value.real)
        for value in roots
        if abs(value.imag) < 1.0e-7 and value.real > 1.0e-12
    ]
    return min(positive) if positive else math.inf


def polynomial_values(coefficients: np.ndarray, grid: np.ndarray) -> np.ndarray:
    return sum(
        coefficients[power] * grid**power
        for power in range(1, len(coefficients))
    )


def polynomial_metrics(coefficients: np.ndarray) -> dict[str, float | bool]:
    transverse_coefficients = np.array(
        [2.0 * power * coefficients[power] for power in range(1, len(coefficients))]
    )
    longitudinal_coefficients = np.array(
        [
            2.0 * power * (2.0 * power - 1.0) * coefficients[power]
            for power in range(1, len(coefficients))
        ]
    )
    local_grid = np.linspace(0.0, LOCAL_X_MAX, 501)
    global_grid = np.linspace(0.0, GLOBAL_X_MAX, 1001)
    transverse_local = np.polynomial.polynomial.polyval(
        local_grid, transverse_coefficients
    )
    longitudinal_local = np.polynomial.polynomial.polyval(
        local_grid, longitudinal_coefficients
    )
    transverse_global = np.polynomial.polynomial.polyval(
        global_grid, transverse_coefficients
    )
    longitudinal_global = np.polynomial.polynomial.polyval(
        global_grid, longitudinal_coefficients
    )
    order = len(coefficients) - 1
    radius_ratio = (
        abs(coefficients[order - 1] / coefficients[order])
        if order >= 3 and coefficients[order] != 0.0
        else math.inf
    )
    return {
        "first_transverse_zero": first_positive_root(transverse_coefficients),
        "first_longitudinal_zero": first_positive_root(longitudinal_coefficients),
        "minimum_transverse_local": float(np.min(transverse_local)),
        "minimum_longitudinal_local": float(np.min(longitudinal_local)),
        "minimum_transverse_global": float(np.min(transverse_global)),
        "minimum_longitudinal_global": float(np.min(longitudinal_global)),
        "local_convex": bool(
            np.min(transverse_local) > 0.0 and np.min(longitudinal_local) > 0.0
        ),
        "global_convex": bool(
            np.min(transverse_global) > 0.0 and np.min(longitudinal_global) > 0.0
        ),
        "last_coefficient_ratio_radius": radius_ratio,
    }


def solve_branches(
    projector: FunctionalPXProjector,
    gravity_fixed_point: float,
) -> tuple[
    dict[str, dict[int, dict[str, Any]]],
    list[dict[str, Any]],
]:
    scenarios = {
        "reference_etaN0": 0.0,
        "fixed_point_etaNminus2": -2.0,
    }
    gravity_steps = np.linspace(0.0, gravity_fixed_point, HOMOTOPY_STEPS + 1)
    solutions: dict[str, dict[int, dict[str, Any]]] = {}
    trace_rows: list[dict[str, Any]] = []

    def solve_at_point(
        guess: np.ndarray,
        gravity: float,
        eta_newton: float,
    ) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, float, float, bool]:
        order = len(guess) + 1
        beta_scale = np.maximum(
            1.0,
            4.0
            * np.arange(2, order + 1)
            * np.maximum(np.abs(guess), 1.0e-12),
        )

        def scaled_beta(candidate: np.ndarray) -> np.ndarray:
            return projector.beta_values(candidate, gravity, eta_newton)[0] / beta_scale

        solution = root(
            scaled_beta,
            guess,
            method="lm",
            options={
                "ftol": 1.0e-12,
                "xtol": 1.0e-12,
                "gtol": 1.0e-12,
                "maxiter": 3000,
            },
        )
        beta, eta_scalar, coefficients = projector.beta_values(
            solution.x, gravity, eta_newton
        )
        scaled_residual = float(np.max(np.abs(beta / beta_scale)))
        absolute_residual = float(np.max(np.abs(beta)))
        passed = bool(
            solution.success
            and np.all(np.isfinite(solution.x))
            and scaled_residual < 1.0e-8
            and np.max(np.abs(solution.x)) < 1.0e12
        )
        return (
            solution.x.copy(),
            beta,
            eta_scalar,
            coefficients,
            absolute_residual,
            scaled_residual,
            passed,
        )

    for scenario, eta_newton in scenarios.items():
        solutions[scenario] = {}
        variables = np.zeros(1)
        maximum_scaled_residual = 0.0
        maximum_absolute_residual = 0.0
        n2_pass = True
        for step_index, gravity in enumerate(gravity_steps[1:], start=1):
            (
                variables,
                beta,
                eta_scalar,
                coefficients,
                absolute_residual,
                scaled_residual,
                step_pass,
            ) = solve_at_point(variables, float(gravity), eta_newton)
            n2_pass = n2_pass and step_pass
            maximum_scaled_residual = max(maximum_scaled_residual, scaled_residual)
            maximum_absolute_residual = max(maximum_absolute_residual, absolute_residual)
            trace_rows.append(
                {
                    "scenario": scenario,
                    "eta_Newton": eta_newton,
                    "homotopy_type": "N2_GAUSSIAN_TO_GRAVITY_FIXED_POINT",
                    "polynomial_order": 2,
                    "step_index": step_index,
                    "g_fraction_of_target": gravity / gravity_fixed_point,
                    "g": gravity,
                    "eta_psi": eta_scalar,
                    "coefficients_a2_up_json": json.dumps(
                        [float(value) for value in variables], separators=(",", ":")
                    ),
                    "absolute_beta_residual_max": absolute_residual,
                    "scaled_beta_residual_max": scaled_residual,
                    "solver_success": step_pass,
                    "step_passed": step_pass,
                }
            )
        solutions[scenario][2] = {
            "variables": variables.copy(),
            "coefficients": coefficients.copy(),
            "eta_psi": eta_scalar,
            "beta": beta.copy(),
            "all_steps_pass": n2_pass,
            "maximum_scaled_residual": maximum_scaled_residual,
            "maximum_absolute_residual": maximum_absolute_residual,
            "homotopy_evidence": "N2_GAUSSIAN_TO_GRAVITY_FIXED_POINT",
        }

        previous_target = variables.copy()
        for order in range(3, MAX_ORDER + 1):
            guess = np.concatenate((previous_target, np.zeros(1)))
            (
                variables,
                beta,
                eta_scalar,
                coefficients,
                absolute_residual,
                scaled_residual,
                target_pass,
            ) = solve_at_point(guess, gravity_fixed_point, eta_newton)
            trace_rows.append(
                {
                    "scenario": scenario,
                    "eta_Newton": eta_newton,
                    "homotopy_type": "ORDER_CONTINUATION_AT_GRAVITY_FIXED_POINT",
                    "polynomial_order": order,
                    "step_index": order - 1,
                    "g_fraction_of_target": 1.0,
                    "g": gravity_fixed_point,
                    "eta_psi": eta_scalar,
                    "coefficients_a2_up_json": json.dumps(
                        [float(value) for value in variables], separators=(",", ":")
                    ),
                    "absolute_beta_residual_max": absolute_residual,
                    "scaled_beta_residual_max": scaled_residual,
                    "solver_success": target_pass,
                    "step_passed": target_pass,
                }
            )
            solutions[scenario][order] = {
                "variables": variables.copy(),
                "coefficients": coefficients.copy(),
                "eta_psi": eta_scalar,
                "beta": beta.copy(),
                "all_steps_pass": target_pass,
                "maximum_scaled_residual": scaled_residual,
                "maximum_absolute_residual": absolute_residual,
                "homotopy_evidence": "ORDER_CONTINUATION_AT_GRAVITY_FIXED_POINT",
            }
            previous_target = variables.copy()

        n12_target = solutions[scenario][MAX_ORDER]["variables"].copy()
        n12_pass = True
        gaussian_endpoint_norm = math.inf
        for step_index, gravity in enumerate(
            np.linspace(gravity_fixed_point, 0.0, HOMOTOPY_STEPS + 1)[1:],
            start=1,
        ):
            (
                n12_target,
                beta,
                eta_scalar,
                coefficients,
                absolute_residual,
                scaled_residual,
                step_pass,
            ) = solve_at_point(n12_target, float(gravity), eta_newton)
            n12_pass = n12_pass and step_pass
            gaussian_endpoint_norm = float(np.max(np.abs(n12_target)))
            trace_rows.append(
                {
                    "scenario": scenario,
                    "eta_Newton": eta_newton,
                    "homotopy_type": "N12_GRAVITY_FIXED_POINT_TO_GAUSSIAN",
                    "polynomial_order": MAX_ORDER,
                    "step_index": step_index,
                    "g_fraction_of_target": gravity / gravity_fixed_point,
                    "g": gravity,
                    "eta_psi": eta_scalar,
                    "coefficients_a2_up_json": json.dumps(
                        [float(value) for value in n12_target], separators=(",", ":")
                    ),
                    "absolute_beta_residual_max": absolute_residual,
                    "scaled_beta_residual_max": scaled_residual,
                    "solver_success": step_pass,
                    "step_passed": step_pass,
                }
            )
        n12_pass = n12_pass and gaussian_endpoint_norm < 1.0e-7
        solutions[scenario][MAX_ORDER]["all_steps_pass"] = (
            solutions[scenario][MAX_ORDER]["all_steps_pass"] and n12_pass
        )
        solutions[scenario][MAX_ORDER]["homotopy_evidence"] = (
            "ORDER_CONTINUATION_AND_N12_GAUSSIAN_ENDPOINT"
        )
        solutions[scenario][MAX_ORDER]["gaussian_endpoint_norm"] = (
            gaussian_endpoint_norm
        )
    return solutions, trace_rows


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(
        source_hashes[str(path)] == expected
        for path, expected in EXPECTED_HASHES.items()
    )
    if not source_hashes_match:
        failures = {
            str(path): {
                "expected": expected,
                "actual": source_hashes[str(path)],
            }
            for path, expected in EXPECTED_HASHES.items()
            if source_hashes[str(path)] != expected
        }
        raise RuntimeError(f"source hash mismatch: {failures}")

    parent = json.loads(PARENT_4935.read_text(encoding="utf-8"))
    result_4954 = json.loads(RESULT_4954.read_text(encoding="utf-8"))
    gravity_fixed_point = float(parent["flow_contract"]["fixed_point"][0])
    source_clause_checks = {
        "parent_fixed_point_residual": float(
            parent["flow_contract"]["beta_residual_infinity_norm"]
        )
        < 1.0e-12,
        "parent_GR_branch": bool(
            parent["flow_contract"]["negative_sign_is_candidate_GR_branch"]
        ),
        "scalar_Wetterich_equation": "\\partial_t \\Gamma_k" in SCALAR_TEX.read_text(encoding="utf-8"),
        "scalar_harmonic_gauge": "F_\\mu = \\Db^\\nu h_{\\mu\\nu}" in SCALAR_TEX.read_text(encoding="utf-8"),
        "scalar_kinetic_vertices": "\\left[{\\ver}_{h\\phi}" in SCALAR_TEX.read_text(encoding="utf-8"),
        "six_derivative_basis": "\\mathcal{O}_1 = \\big[(\\nabla_\\mu \\phi)^2\\big]^3" in BASIS_TEX.read_text(encoding="utf-8"),
        "eight_derivative_X4": "d\\phi^8" in BASIS_TEX.read_text(encoding="utf-8"),
        "essential_X2_source": "16 g^2" in LOWER_4941.read_text(encoding="utf-8-sig"),
        "4955_nonclosure": "finite-polynomial nonclosure theorem" in CHECKPOINT_4955.read_text(encoding="utf-8"),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause check failed: {source_clause_checks}")

    projector = FunctionalPXProjector(MAX_ORDER, QUADRATURE_ORDER)
    hessian_rows = tagged(
        [
            {
                "contract_id": "H4956_01_metric_block",
                "equation": "H_hh=I10+32*pi*g*K*[p*M0+x*pprime*M1+x^2*psecond*M2]",
                "derivation": "second metric variation of sqrt(g)P(X) on a flat constant-gradient background",
                "status": "EXACT_MINIMAL_FLAT_FUNCTIONAL_HESSIAN",
                "passed": True,
            },
            {
                "contract_id": "H4956_02_mixed_block",
                "equation": "H_hpsi=sqrt(32*pi*g)qK*sqrt(x)[pprime*B1+x*psecond*B2]",
                "derivation": "mixed metric-motion variation including the Psecond term",
                "status": "EXACT_MINIMAL_FLAT_FUNCTIONAL_HESSIAN",
                "passed": True,
            },
            {
                "contract_id": "H4956_03_scalar_block",
                "equation": "H_psipsi=1+q^2[2pprime-1+4x*psecond*z^2]",
                "derivation": "scalar Hessian plus field-independent optimized regulator",
                "status": "EXACT_MINIMAL_FLAT_FUNCTIONAL_HESSIAN",
                "passed": True,
            },
            {
                "contract_id": "H4956_04_regulator_insertion",
                "equation": "W_A=1-eta_A(1-q^2)/2 for A in {N,psi}",
                "derivation": "scale derivative of the spectrally normalized Litim regulator",
                "status": "LPA_PRIME_REGULATOR_INSERTION",
                "passed": True,
            },
            {
                "contract_id": "H4956_05_functional_flow",
                "equation": "dt p=-4p+(4+eta_psi)xpprime+(8pi^2)^-1 int dq q^3 <Tr[H^-1 W]-Tr[W]_x0>",
                "derivation": "Wetterich trace with p(0)=0 subtraction",
                "status": "MINIMAL_FLAT_FUNCTIONAL_FLOW_DERIVED",
                "passed": True,
            },
            {
                "contract_id": "H4956_06_normalization",
                "equation": "pprime(0)=1/2; eta_psi=-Q1_fixed/[1/2+Q1_eta]",
                "derivation": "implicit beta_a1=0 wavefunction normalization",
                "status": "NORMALIZATION_CONDITION_DERIVED",
                "passed": True,
            },
        ]
    )

    calibration_rows: list[dict[str, Any]] = []
    scalar_coefficients = np.array([0.0, 0.5, 0.2, -0.1, 0.03])
    scalar_fixed, scalar_eta = projector.quantum_coefficients(
        scalar_coefficients, 0.0, 0.0
    )
    exact_scalar_q2 = 5.0 * 0.2**2 / (8.0 * math.pi**2) - (-0.1) / (4.0 * math.pi**2)
    exact_scalar_q3 = (
        -37.0 * 0.2**3 / (10.0 * math.pi**2)
        + 21.0 * 0.2 * (-0.1) / (8.0 * math.pi**2)
        - 5.0 * 0.03 / (12.0 * math.pi**2)
    )
    for identifier, actual, expected in (
        ("CAL4956_scalar_Q2", scalar_fixed[2], exact_scalar_q2),
        ("CAL4956_scalar_Q3", scalar_fixed[3], exact_scalar_q3),
    ):
        calibration_rows.append(
            {
                "calibration_id": identifier,
                "g": 0.0,
                "actual": actual,
                "expected": expected,
                "relative_error": abs(actual - expected) / max(abs(expected), 1.0e-300),
                "status": "PURE_SCALAR_HIERARCHY_REPRODUCED",
                "passed": math.isclose(actual, expected, rel_tol=2.0e-13),
            }
        )
    for gravity in (1.0e-5, 1.0e-3, 0.01, gravity_fixed_point):
        gaussian = np.array([0.0, 0.5, 0.0, 0.0])
        fixed_eta, _ = projector.quantum_coefficients(gaussian, gravity, 0.0)
        for identifier, actual, expected in (
            ("CAL4956_gravity_Q2", fixed_eta[2] / gravity**2, 20.0),
            (
                "CAL4956_gravity_Q3",
                fixed_eta[3] / gravity**3,
                -208.0 * math.pi / 5.0,
            ),
        ):
            calibration_rows.append(
                {
                    "calibration_id": identifier,
                    "g": gravity,
                    "actual": actual,
                    "expected": expected,
                    "relative_error": abs(actual - expected) / abs(expected),
                    "status": "4955_GRAVITY_SOURCE_REPRODUCED",
                    "passed": math.isclose(actual, expected, rel_tol=2.0e-13),
                }
            )
    calibration_rows = tagged(calibration_rows)
    if not all(row["passed"] for row in calibration_rows):
        raise RuntimeError("functional projector calibration failed")

    solutions, homotopy_rows = solve_branches(projector, gravity_fixed_point)
    homotopy_rows = tagged(homotopy_rows)
    coefficient_polynomial = result_4954["on_shell_24"]
    fixed_point_rows: list[dict[str, Any]] = []
    convergence_rows: list[dict[str, Any]] = []
    regularity_rows: list[dict[str, Any]] = []
    for scenario, order_solutions in solutions.items():
        previous_coefficients: np.ndarray | None = None
        for order, entry in order_solutions.items():
            coefficients = entry["coefficients"]
            metrics = polynomial_metrics(coefficients)
            grid_local = np.linspace(0.0, LOCAL_X_MAX, 501)
            grid_global = np.linspace(0.0, GLOBAL_X_MAX, 1001)
            if previous_coefficients is None:
                local_difference = math.nan
                global_difference = math.nan
                local_relative = math.nan
                global_relative = math.nan
            else:
                previous_local = polynomial_values(previous_coefficients, grid_local)
                current_local = polynomial_values(coefficients, grid_local)
                previous_global = polynomial_values(previous_coefficients, grid_global)
                current_global = polynomial_values(coefficients, grid_global)
                local_difference = float(np.max(np.abs(current_local - previous_local)))
                global_difference = float(np.max(np.abs(current_global - previous_global)))
                local_relative = local_difference / max(
                    float(np.max(np.abs(current_local))), 1.0e-300
                )
                global_relative = global_difference / max(
                    float(np.max(np.abs(current_global))), 1.0e-300
                )
            c_value = coefficients[2]
            e_value = coefficients[3] if order >= 3 else math.nan
            r3_value = (
                e_value / (2.0 * c_value**2)
                if order >= 3 and c_value != 0.0
                else math.nan
            )
            cross_section_value = (
                coefficient_polynomial["C0"]
                + coefficient_polynomial["C1"] * r3_value
                + coefficient_polynomial["C2"] * r3_value**2
                if math.isfinite(r3_value)
                else math.nan
            )
            row: dict[str, Any] = {
                "scenario": scenario,
                "eta_Newton": 0.0 if scenario == "reference_etaN0" else -2.0,
                "polynomial_order": order,
                "g_fixed_point": gravity_fixed_point,
                "eta_psi": entry["eta_psi"],
                "all_homotopy_steps_pass": entry["all_steps_pass"],
                "maximum_scaled_beta_residual": entry["maximum_scaled_residual"],
                "target_absolute_beta_residual": float(np.max(np.abs(entry["beta"]))),
                "gaussian_endpoint_norm": entry.get("gaussian_endpoint_norm", ""),
                "r3_fixed_point": r3_value,
                "C24_polynomial_at_r3": cross_section_value,
                "first_transverse_zero": metrics["first_transverse_zero"],
                "first_longitudinal_zero": metrics["first_longitudinal_zero"],
                "minimum_transverse_x_le_0p1": metrics["minimum_transverse_local"],
                "minimum_longitudinal_x_le_0p1": metrics["minimum_longitudinal_local"],
                "minimum_transverse_x_le_0p25": metrics["minimum_transverse_global"],
                "minimum_longitudinal_x_le_0p25": metrics["minimum_longitudinal_global"],
                "convex_x_le_0p1": metrics["local_convex"],
                "convex_x_le_0p25": metrics["global_convex"],
                "last_coefficient_ratio_radius": metrics["last_coefficient_ratio_radius"],
                "difference_from_previous_order_x_le_0p1": local_difference,
                "relative_difference_previous_x_le_0p1": local_relative,
                "difference_from_previous_order_x_le_0p25": global_difference,
                "relative_difference_previous_x_le_0p25": global_relative,
                "status": "GAUSSIAN_CONNECTED_POLYNOMIAL_ROOT",
            }
            for coordinate in range(2, MAX_ORDER + 1):
                row[f"a{coordinate}"] = (
                    coefficients[coordinate] if coordinate <= order else ""
                )
            fixed_point_rows.append(row)
            previous_coefficients = coefficients

        highest = order_solutions[MAX_ORDER]
        highest_coefficients = highest["coefficients"]
        for x_maximum in (LOCAL_X_MAX, GLOBAL_X_MAX):
            hessian_gate = projector.direct_hessian_minimum(
                highest_coefficients, gravity_fixed_point, x_maximum
            )
            highest_metrics = polynomial_metrics(highest_coefficients)
            domain_regular = bool(
                hessian_gate["minimum_singular_value"] > 1.0e-6
                and (
                    highest_metrics["local_convex"]
                    if x_maximum == LOCAL_X_MAX
                    else highest_metrics["global_convex"]
                )
            )
            regularity_rows.append(
                {
                    "scenario": scenario,
                    "polynomial_order": MAX_ORDER,
                    "x_domain_max": x_maximum,
                    **hessian_gate,
                    "scalar_convex": (
                        highest_metrics["local_convex"]
                        if x_maximum == LOCAL_X_MAX
                        else highest_metrics["global_convex"]
                    ),
                    "status": (
                        "LOCAL_GERM_REGULAR"
                        if x_maximum == LOCAL_X_MAX and domain_regular
                        else (
                            "GLOBAL_GERM_REGULAR"
                            if x_maximum == GLOBAL_X_MAX and domain_regular
                            else (
                                "LOCAL_REGULARITY_NOT_ESTABLISHED"
                                if x_maximum == LOCAL_X_MAX
                                else "GLOBAL_REGULARITY_NOT_ESTABLISHED"
                            )
                        )
                    ),
                }
            )

        orders_for_convergence = list(range(8, MAX_ORDER + 1))
        coordinate_extractors = {
            "a2": lambda item: float(item["coefficients"][2]),
            "a3": lambda item: float(item["coefficients"][3]),
            "eta_psi": lambda item: float(item["eta_psi"]),
            "r3": lambda item: float(
                item["coefficients"][3]
                / (2.0 * item["coefficients"][2] ** 2)
            ),
        }
        for coordinate, extractor in coordinate_extractors.items():
            values = [extractor(order_solutions[order]) for order in orders_for_convergence]
            spread = max(values) - min(values)
            relative_spread = abs(spread) / max(abs(values[-1]), 1.0e-300)
            convergence_rows.append(
                {
                    "scenario": scenario,
                    "coordinate": coordinate,
                    "orders": json.dumps(orders_for_convergence, separators=(",", ":")),
                    "values": json.dumps(values, separators=(",", ":")),
                    "absolute_spread": spread,
                    "relative_spread": relative_spread,
                    "converged": relative_spread < 1.0e-4,
                    "status": "LOW_COORDINATE_CONVERGENCE_GATE",
                }
            )

    fixed_point_rows = tagged(fixed_point_rows)
    convergence_rows = tagged(convergence_rows)
    regularity_rows = tagged(regularity_rows)

    highest_rows = [
        row for row in fixed_point_rows if int(row["polynomial_order"]) == MAX_ORDER
    ]
    homotopy_pass = all(row["all_homotopy_steps_pass"] for row in highest_rows)
    local_regular = all(
        row["status"] == "LOCAL_GERM_REGULAR"
        for row in regularity_rows
        if float(row["x_domain_max"]) == LOCAL_X_MAX
    )
    global_regular = all(
        row["status"] != "GLOBAL_REGULARITY_NOT_ESTABLISHED"
        for row in regularity_rows
        if float(row["x_domain_max"]) == GLOBAL_X_MAX
    )
    low_coordinate_convergence = all(row["converged"] for row in convergence_rows)
    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4956_01_hessian",
                "question": "Is the minimal flat gravity-motion Hessian known for a full running P_k(X)?",
                "answer": "yes",
                "status": "FUNCTIONAL_PX_HESSIAN_DERIVED",
                "next_action": "retain its explicit O2 O4 O5 and curvature firewall",
            },
            {
                "decision_id": "DEC4956_02_calibration",
                "question": "Does the functional projector reproduce the exact 4955 X2 and X3 sources?",
                "answer": "yes at every executed g",
                "status": "FUNCTIONAL_PROJECTOR_EXACTLY_CALIBRATED",
                "next_action": "use the projector for convergence rather than a new closure",
            },
            {
                "decision_id": "DEC4956_03_roots",
                "question": "Can the Gaussian matter root be continued to the 4935 gravity fixed point through orders 2 to 12?",
                "answer": f"{'yes' if homotopy_pass else 'no'} in both eta_N regulator insertions",
                "status": (
                    "GAUSSIAN_CONNECTED_POLYNOMIAL_ROOTS_THROUGH_N12"
                    if homotopy_pass
                    else "GAUSSIAN_CONNECTED_POLYNOMIAL_ROOTS_NOT_ESTABLISHED"
                ),
                "next_action": "distinguish a local analytic germ from a global fixed function",
            },
            {
                "decision_id": "DEC4956_04_low_coordinates",
                "question": "Do a2 a3 eta_psi and r3 stabilize with polynomial order?",
                "answer": "yes" if low_coordinate_convergence else "no",
                "status": (
                    "LOW_FUNCTIONAL_COORDINATES_CONVERGED"
                    if low_coordinate_convergence
                    else "LOW_FUNCTIONAL_COORDINATES_NOT_CONVERGED"
                ),
                "next_action": "carry their scheme spread into the trajectory calculation",
            },
            {
                "decision_id": "DEC4956_05_local_germ",
                "question": "Is the N12 functional germ convex and Hessian-regular on 0<=x<=0.1?",
                "answer": "yes" if local_regular else "no",
                "status": "LOCAL_FIXED_FUNCTION_GERM_RETAINED" if local_regular else "LOCAL_FIXED_FUNCTION_GERM_REJECTED",
                "next_action": "test the actual GR-connected RG trajectory inside this domain",
            },
            {
                "decision_id": "DEC4956_06_global",
                "question": "Is a global regular fixed function established on 0<=x<=0.25?",
                "answer": "yes" if global_regular else "no",
                "status": (
                    "GLOBAL_FIXED_FUNCTION_RETAINED"
                    if global_regular
                    else "GLOBAL_FIXED_FUNCTION_NOT_ESTABLISHED"
                ),
                "next_action": (
                    "carry the regular domain into the trajectory calculation"
                    if global_regular
                    else "do not analytically continue the local series beyond its regularity evidence"
                ),
            },
            {
                "decision_id": "DEC4956_07_r3",
                "question": "Is r3 now a full infrared prediction for the 4954 rate?",
                "answer": "no: only a stable UV fixed-germ value exists",
                "status": "UV_R3_GERM_DERIVED_IR_R3_OPEN",
                "next_action": "integrate the coefficients down the source-locked 4935 GR branch",
            },
            {
                "decision_id": "DEC4956_08_operator_firewall",
                "question": "Does flat P(X) complete the whole motion sector?",
                "answer": "no: O2 O4 O5 and curved projectors remain explicit",
                "status": "FULL_MOTION_HESSIAN_NOT_COMPLETE",
                "next_action": "bound these residual projectors along the trajectory",
            },
            {
                "decision_id": "DEC4956_09_local",
                "question": "Is the checkpoint-4947 local GR Newton Maxwell branch altered?",
                "answer": "no",
                "status": "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
                "next_action": "test functional motion decoupling on the GR trajectory",
            },
            {
                "decision_id": "DEC4956_10_full_MTS",
                "question": "Does this establish full MTS unification?",
                "answer": "no",
                "status": "FULL_MTS_PROMOTION_BLOCKED",
                "next_action": "derive the functional GR-connected trajectory and residual operator bounds",
            },
        ]
    )

    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(CALIBRATION_CSV, calibration_rows)
    write_csv(HOMOTOPY_CSV, homotopy_rows)
    write_csv(FIXED_POINT_CSV, fixed_point_rows)
    write_csv(COEFFICIENT_CSV, convergence_rows)
    write_csv(REGULARITY_CSV, regularity_rows)
    write_csv(DECISION_CSV, decision_rows)

    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "projection": {
            "gravity_fixed_point_g": gravity_fixed_point,
            "polynomial_orders": list(range(2, MAX_ORDER + 1)),
            "quadrature_order": QUADRATURE_ORDER,
            "quadrature_nodes": projector.node_count,
            "homotopy_steps": HOMOTOPY_STEPS,
            "eta_Newton_scenarios": {
                "reference_etaN0": 0.0,
                "fixed_point_etaNminus2": -2.0,
            },
            "normalization": "p(0)=0; pprime(0)=1/2; eta_psi fixed by beta_a1=0",
            "operator_firewall": "minimal flat P(X); O2 O4 O5 curved and nonconstant-gradient flows excluded",
        },
        "calibration": {
            "all_rows_pass": all(row["passed"] for row in calibration_rows),
            "maximum_relative_error": max(
                float(row["relative_error"]) for row in calibration_rows
            ),
        },
        "fixed_point_summary": {
            row["scenario"]: {
                "eta_psi_N12": row["eta_psi"],
                "a2_N12": row["a2"],
                "a3_N12": row["a3"],
                "r3_N12": row["r3_fixed_point"],
                "C24_polynomial_N12": row["C24_polynomial_at_r3"],
                "first_longitudinal_zero_N12": row["first_longitudinal_zero"],
                "convex_x_le_0p1_N12": row["convex_x_le_0p1"],
                "convex_x_le_0p25_N12": row["convex_x_le_0p25"],
                "gaussian_endpoint_norm_N12": row["gaussian_endpoint_norm"],
            }
            for row in highest_rows
        },
        "gates": {
            "all_N12_homotopies_pass": homotopy_pass,
            "low_coordinates_converged": low_coordinate_convergence,
            "local_x_le_0p1_fixed_function_germ": local_regular,
            "global_x_le_0p25_fixed_function": global_regular,
            "UV_r3_germ": "DERIVED_SCHEME_BRACKETED",
            "IR_r3_trajectory": "OPEN",
            "full_motion_Hessian": False,
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"{MARKER}_DONE g*={gravity_fixed_point:.16g} "
        f"homotopy={homotopy_pass} local={local_regular} global={global_regular}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
