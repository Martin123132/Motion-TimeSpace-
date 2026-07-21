from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

import Y5_R2FR_4934_completed_combined_flow as completed_flow
import Y5_R2FR_4956_functional_PX_fixed_function_gate as functional_px


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4957"

RESULT_JSON = SOURCE / "functional_PX_O4_GR_trajectory_results.json"
FIXED_CSV = SOURCE / "combined_functional_fixed_point_convergence.csv"
SPECTRUM_CSV = SOURCE / "combined_functional_stability_spectrum.csv"
TRAJECTORY_CSV = SOURCE / "functional_PX_O4_GR_trajectory.csv"
ENDPOINT_CSV = SOURCE / "infrared_motion_coordinate_convergence.csv"
REGULARITY_CSV = SOURCE / "trajectory_functional_regularity_gate.csv"
RESIDUAL_CSV = SOURCE / "local_operator_residual_gate.csv"
DECISION_CSV = SOURCE / "functional_trajectory_decision.csv"

PARENT_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
PARENT_RESULT = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
O4_RESULT = POST / "source-intake" / "functional_rg" / "4941" / "typeII_direct_O4_zero_and_lower_quotient_results.json"
O4_FAMILY = POST / "source-intake" / "functional_rg" / "4940" / "O4_kernel_GR_family.csv"
LOCAL_4942 = POST / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md"
LOCAL_4943 = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
LOCAL_4947 = POST / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
RATE_4954 = POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json"
SCRIPT_4956 = POST / "scripts" / "Y5_R2FR_4956_functional_PX_fixed_function_gate.py"
RESULT_4956 = POST / "source-intake" / "functional_rg" / "4956" / "functional_PX_fixed_function_results.json"
FIXED_4956 = POST / "source-intake" / "functional_rg" / "4956" / "polynomial_fixed_point_convergence.csv"
CHECKPOINT_4956 = POST / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md"

EXPECTED_HASHES = {
    PARENT_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    PARENT_RESULT: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    O4_RESULT: "e234f85376912f5a9da919f32dd7db855d1ff45f39faa693a01a74677590b57f",
    O4_FAMILY: "d6f6fd98c06cdf29ef842a8ab99aea1642ceb3e0a188d3c449b4d66ff6a97723",
    LOCAL_4942: "64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f",
    LOCAL_4943: "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    LOCAL_4947: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    RATE_4954: "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45",
    SCRIPT_4956: "b72f494961a83171520098dedd166c0af66f187060f9be52aafde3befb126333",
    RESULT_4956: "06ee62bfba50e5b1411e59e5cc707110a52f893c556331ba178032748d7563fb",
    FIXED_4956: "a074d8436d14ed9af6697c56a274407758fb5116a0ca36e90ddc9427786eb018",
    CHECKPOINT_4956: "c3cdc970258583882c13d6544e17c8cef2620d89002ee7998825566ce6630367",
}

MARKER = "MTS_4957_FUNCTIONAL_PX_O4_GR_TRAJECTORY"
CHECKED_DATE = "2026-07-13"
MAX_ORDER = 8
TRAJECTORY_ORDERS = (6, 8)
QUADRATURE_ORDER = 11
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
RELATIVE_SEED = 1.0e-6
SAMPLE_COUNT = 121
LOCAL_X_MAX = 0.1
C2_ROW = 4
RC2_ROW = 7
GAMMA_C2_INDEX = 7
C6_SCALAR = 1.0 / (483840.0 * math.pi**2)
PARENT_COORDINATES = ("g", "g_plus", "g_minus", "g_CFF", "h_C3", "u_O4")
SCHEMES = {
    "dynamic_etaN": "fixed_point_etaNminus2",
    "reference_etaN0": "reference_etaN0",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def numerical_jacobian(
    function: Callable[[np.ndarray], np.ndarray],
    point: np.ndarray,
    floors: np.ndarray,
) -> np.ndarray:
    jacobian = np.zeros((len(point), len(point)), dtype=float)
    for column in range(len(point)):
        step = 2.0e-5 * max(abs(point[column]), floors[column])
        plus = point.copy()
        minus = point.copy()
        plus[column] += step
        minus[column] -= step
        jacobian[:, column] = (function(plus) - function(minus)) / (2.0 * step)
    return jacobian


class CombinedFunctionalFlow:
    def __init__(self, projector: functional_px.FunctionalPXProjector) -> None:
        self.projector = projector
        self.system, _, _, _, _, _ = completed_flow.build_completed_solver()

    def parent_beta(self, parent: np.ndarray, eta_psi: float) -> tuple[np.ndarray, dict[str, float]]:
        point = parent[:5]
        u_o4 = float(parent[5])
        matrix, vector = self.system(point)
        newton_weight = 1.0 - eta_psi / 4.0
        c2_weight = 1.0 - eta_psi / 8.0
        rc2_weight = 1.0 - eta_psi / 6.0
        delta_beta_g = point[0] ** 2 * newton_weight / (6.0 * math.pi)
        delta_beta_h = eta_psi * C6_SCALAR
        augmented = (
            vector
            + matrix[:, 0] * delta_beta_g
            + matrix[:, 1] * delta_beta_h
        )
        augmented[C2_ROW] += -u_o4 * c2_weight / (24.0 * math.pi**2)
        augmented[RC2_ROW] += -u_o4 * rc2_weight / (96.0 * math.pi**2)
        unknowns = np.linalg.solve(matrix, augmented)
        beta_parent = np.array(
            [
                unknowns[0],
                (unknowns[13] + unknowns[14]) / 2.0,
                (unknowns[13] - unknowns[14]) / 2.0,
                unknowns[15],
                unknowns[1],
                (4.0 + eta_psi) * u_o4 - 0.5 * unknowns[GAMMA_C2_INDEX],
            ],
            dtype=float,
        )
        residual = matrix @ unknowns - augmented
        return beta_parent, {
            "gamma_C2": float(unknowns[GAMMA_C2_INDEX]),
            "delta_beta_g_scalar": delta_beta_g,
            "delta_beta_h_scalar": delta_beta_h,
            "newton_regulator_weight": newton_weight,
            "O4_C2_regulator_weight": c2_weight,
            "O4_RC2_regulator_weight": rc2_weight,
            "parent_linear_residual": float(np.linalg.norm(residual, ord=np.inf)),
        }

    def original_beta(
        self,
        state: np.ndarray,
        scheme: str,
    ) -> tuple[np.ndarray, dict[str, float]]:
        parent = state[:6]
        variables = state[6:]
        gravity = float(parent[0])
        parent_zero, details_zero = self.parent_beta(parent, 0.0)
        parent_one, _ = self.parent_beta(parent, 1.0)
        parent_slope = parent_one - parent_zero
        physical_eta_newton_zero = parent_zero[0] / gravity - 2.0

        if scheme == "dynamic_etaN":
            beta_a, eta_a, _ = self.projector.beta_values(
                variables, gravity, physical_eta_newton_zero
            )
            beta_b, eta_b, _ = self.projector.beta_values(
                variables, gravity, physical_eta_newton_zero + 1.0
            )
            eta_slope = eta_b - eta_a
            eta_newton_slope = parent_slope[0] / gravity
            denominator = 1.0 - eta_slope * eta_newton_slope
            eta_psi = eta_a / denominator
            eta_newton_regulator = (
                physical_eta_newton_zero + eta_newton_slope * eta_psi
            )
            beta_motion = beta_a + (
                eta_newton_regulator - physical_eta_newton_zero
            ) * (beta_b - beta_a)
            self_consistency_residual = abs(
                eta_psi
                - (
                    eta_a
                    + (eta_newton_regulator - physical_eta_newton_zero)
                    * eta_slope
                )
            )
        elif scheme == "reference_etaN0":
            beta_motion, eta_psi, _ = self.projector.beta_values(
                variables, gravity, 0.0
            )
            eta_newton_regulator = 0.0
            denominator = 1.0
            self_consistency_residual = 0.0
        else:
            raise ValueError(f"unknown scheme: {scheme}")

        beta_parent = parent_zero + eta_psi * parent_slope
        physical_eta_newton = beta_parent[0] / gravity - 2.0
        details = {
            **details_zero,
            "eta_psi": float(eta_psi),
            "eta_Newton_regulator": float(eta_newton_regulator),
            "eta_Newton_physical": float(physical_eta_newton),
            "eta_self_consistency_denominator": float(denominator),
            "eta_self_consistency_residual": float(self_consistency_residual),
        }
        return np.concatenate([beta_parent, beta_motion]), details

    def ratio_state(self, original_state: np.ndarray) -> np.ndarray:
        gravity = float(original_state[0])
        powers = np.arange(2, len(original_state) - 4, dtype=float)
        return np.concatenate(
            [original_state[:6], original_state[6:] / gravity**powers]
        )

    def original_state(self, ratio_state: np.ndarray) -> np.ndarray:
        gravity = float(ratio_state[0])
        powers = np.arange(2, len(ratio_state) - 4, dtype=float)
        return np.concatenate(
            [ratio_state[:6], ratio_state[6:] * gravity**powers]
        )

    def ratio_beta(
        self,
        ratio_state: np.ndarray,
        scheme: str,
    ) -> np.ndarray:
        original = self.original_state(ratio_state)
        beta_original, _ = self.original_beta(original, scheme)
        gravity = float(original[0])
        beta_gravity_over_gravity = beta_original[0] / gravity
        powers = np.arange(2, len(ratio_state) - 4, dtype=float)
        beta_ratios = (
            beta_original[6:] / gravity**powers
            - powers * ratio_state[6:] * beta_gravity_over_gravity
        )
        return np.concatenate([beta_original[:6], beta_ratios])


def solve_fixed_points(
    flow: CombinedFunctionalFlow,
    parent_initial: np.ndarray,
    source_rows: list[dict[str, str]],
) -> tuple[dict[str, dict[int, np.ndarray]], list[dict[str, Any]]]:
    source_map = {
        (row["scenario"], int(row["polynomial_order"])): row
        for row in source_rows
    }
    solutions: dict[str, dict[int, np.ndarray]] = {}
    rows: list[dict[str, Any]] = []
    for scheme, source_scenario in SCHEMES.items():
        solutions[scheme] = {}
        previous: np.ndarray | None = None
        for order in range(2, MAX_ORDER + 1):
            source_row = source_map[(source_scenario, order)]
            if previous is None:
                guess = np.concatenate(
                    [parent_initial, np.array([float(source_row["a2"])])]
                )
            else:
                guess = np.concatenate(
                    [previous, np.array([float(source_row[f"a{order}"])])]
                )
            canonical = np.concatenate(
                [np.ones(6), 4.0 * np.arange(2, order + 1)]
            )
            beta_scale = np.maximum(1.0, np.abs(guess) * canonical)
            solution = root(
                lambda candidate: flow.original_beta(candidate, scheme)[0]
                / beta_scale,
                guess,
                method="lm",
                options={
                    "maxiter": 5000,
                    "ftol": 1.0e-12,
                    "xtol": 1.0e-12,
                    "gtol": 1.0e-12,
                },
            )
            state = np.asarray(solution.x, dtype=float)
            beta, details = flow.original_beta(state, scheme)
            scaled_residual = float(np.max(np.abs(beta / beta_scale)))
            if (
                not solution.success
                or not np.all(np.isfinite(state))
                or scaled_residual >= 1.0e-8
            ):
                raise RuntimeError(
                    f"combined fixed point failed: {scheme} N={order} "
                    f"success={solution.success} residual={scaled_residual}"
                )
            variables = state[6:]
            coefficients = np.concatenate([np.array([0.0, 0.5]), variables])
            metrics = functional_px.polynomial_metrics(coefficients)
            row: dict[str, Any] = {
                "scheme": scheme,
                "polynomial_order": order,
                **dict(zip(PARENT_COORDINATES, state[:6])),
                "eta_psi": details["eta_psi"],
                "eta_Newton_regulator": details["eta_Newton_regulator"],
                "eta_Newton_physical": details["eta_Newton_physical"],
                "eta_self_consistency_residual": details[
                    "eta_self_consistency_residual"
                ],
                "scaled_beta_residual": scaled_residual,
                "absolute_beta_residual": float(np.max(np.abs(beta))),
                "r3_raw": (
                    variables[1] / (2.0 * variables[0] ** 2)
                    if order >= 3
                    else math.nan
                ),
                "convex_x_le_0p1": metrics["local_convex"],
                "first_longitudinal_zero": metrics["first_longitudinal_zero"],
                "status": "SELF_CONSISTENT_COMBINED_FIXED_POINT",
            }
            for coordinate in range(2, MAX_ORDER + 1):
                row[f"a{coordinate}"] = (
                    variables[coordinate - 2] if coordinate <= order else ""
                )
            rows.append(row)
            solutions[scheme][order] = state
            previous = state
            print(
                f"{MARKER}_FIXED scheme={scheme} N={order} "
                f"g={state[0]:.12g} residual={scaled_residual:.3e}",
                flush=True,
            )
    return solutions, rows


def stability_data(
    flow: CombinedFunctionalFlow,
    fixed_original: np.ndarray,
    scheme: str,
    order: int,
) -> tuple[np.ndarray, list[dict[str, Any]], int]:
    fixed_ratio = flow.ratio_state(fixed_original)
    floors = np.concatenate(
        [
            np.array([1.0e-3, 1.0e-3, 1.0e-3, 1.0e-6, 1.0e-8, 1.0e-5]),
            np.ones(order - 1),
        ]
    )
    matrix = numerical_jacobian(
        lambda state: flow.ratio_beta(state, scheme), fixed_ratio, floors
    )
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    relevant_indices = [
        index for index, value in enumerate(eigenvalues) if value.real < 0.0
    ]
    gravity_index = int(
        min(
            range(len(eigenvalues)),
            key=lambda index: abs(eigenvalues[index].real + 1.8927)
            + abs(eigenvalues[index].imag),
        )
    )
    gravity_vector = np.real(eigenvectors[:, gravity_index])
    if gravity_vector[0] < 0.0:
        gravity_vector *= -1.0
    relative_scale = np.maximum(np.abs(fixed_ratio), floors)
    gravity_vector /= float(np.max(np.abs(gravity_vector / relative_scale)))
    rows = []
    for mode_index, value in enumerate(
        sorted(eigenvalues, key=lambda item: (item.real, item.imag))
    ):
        rows.append(
            {
                "scheme": scheme,
                "polynomial_order": order,
                "mode_index": mode_index,
                "beta_eigenvalue_real": float(value.real),
                "beta_eigenvalue_imag": float(value.imag),
                "critical_exponent_real": float(-value.real),
                "critical_exponent_imag": float(-value.imag),
                "relevant": bool(value.real < 0.0),
                "gravity_connected_mode": bool(
                    abs(value - eigenvalues[gravity_index]) < 1.0e-8
                ),
                "status": "COMBINED_RATIO_COORDINATE_STABILITY",
            }
        )
    return gravity_vector, rows, len(relevant_indices)


def integrate_trajectory(
    flow: CombinedFunctionalFlow,
    fixed_original: np.ndarray,
    gravity_vector: np.ndarray,
    scheme: str,
    order: int,
    rate_polynomial: dict[str, float],
) -> tuple[Any, list[dict[str, Any]], dict[str, Any]]:
    fixed_ratio = flow.ratio_state(fixed_original)

    def event(_time: float, state: np.ndarray) -> float:
        return float(state[0] - IR_G_TARGET)

    event.terminal = True
    event.direction = -1
    candidates = []
    for sign in (-1.0, 1.0):
        initial = fixed_ratio + sign * RELATIVE_SEED * gravity_vector
        solution = solve_ivp(
            lambda _time, state: flow.ratio_beta(state, scheme),
            (0.0, T_IR_LIMIT),
            initial,
            method="DOP853",
            rtol=3.0e-8,
            atol=np.concatenate(
                [
                    np.array(
                        [1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19, 1.0e-25]
                    ),
                    np.full(order - 1, 1.0e-10),
                ]
            ),
            max_step=0.12,
            dense_output=True,
            events=event,
        )
        candidates.append((sign, solution))
        if solution.success and len(solution.t_events[0]):
            break
    sign, solution = next(
        (
            candidate_sign,
            candidate_solution,
        )
        for candidate_sign, candidate_solution in candidates
        if candidate_solution.success and len(candidate_solution.t_events[0])
    )
    sample_times = np.linspace(0.0, float(solution.t_events[0][0]), SAMPLE_COUNT)
    sample_ratio = solution.sol(sample_times)
    rows: list[dict[str, Any]] = []
    maximum_eta_residual = 0.0
    minimum_scalar_transverse = math.inf
    minimum_scalar_longitudinal = math.inf
    for sample_index, time_value in enumerate(sample_times):
        ratio_state = sample_ratio[:, sample_index]
        original = flow.original_state(ratio_state)
        beta, details = flow.original_beta(original, scheme)
        variables = original[6:]
        coefficients = np.concatenate([np.array([0.0, 0.5]), variables])
        metrics = functional_px.polynomial_metrics(coefficients)
        minimum_scalar_transverse = min(
            minimum_scalar_transverse, float(metrics["minimum_transverse_local"])
        )
        minimum_scalar_longitudinal = min(
            minimum_scalar_longitudinal, float(metrics["minimum_longitudinal_local"])
        )
        maximum_eta_residual = max(
            maximum_eta_residual, details["eta_self_consistency_residual"]
        )
        r3_raw = variables[1] / (2.0 * variables[0] ** 2)
        c24 = (
            rate_polynomial["C0"]
            + rate_polynomial["C1"] * r3_raw
            + rate_polynomial["C2"] * r3_raw**2
        )
        row: dict[str, Any] = {
            "scheme": scheme,
            "polynomial_order": order,
            "sample_index": sample_index,
            "t_log_k_over_seed": float(time_value),
            **dict(zip(PARENT_COORDINATES, original[:6])),
            "eta_psi": details["eta_psi"],
            "eta_Newton_regulator": details["eta_Newton_regulator"],
            "eta_Newton_physical": details["eta_Newton_physical"],
            "eta_self_consistency_residual": details[
                "eta_self_consistency_residual"
            ],
            "parent_linear_residual": details["parent_linear_residual"],
            "W_O4_u_over_g2": original[5] / original[0] ** 2,
            "r3_raw": r3_raw,
            "C24_raw_polynomial": c24,
            "dimensionless_sigma24_raw_kernel": variables[0] ** 4 * c24,
            "convex_x_le_0p1": metrics["local_convex"],
            "minimum_transverse_x_le_0p1": metrics[
                "minimum_transverse_local"
            ],
            "minimum_longitudinal_x_le_0p1": metrics[
                "minimum_longitudinal_local"
            ],
            "beta_infinity_norm": float(np.max(np.abs(beta))),
            "selected_relevant_sign": sign,
            "status": "GR_CONNECTED_FUNCTIONAL_TRAJECTORY",
        }
        for coordinate in range(2, order + 1):
            row[f"a{coordinate}"] = variables[coordinate - 2]
            row[f"A{coordinate}_a_over_g_power"] = ratio_state[
                6 + coordinate - 2
            ]
        rows.append(row)
    endpoint = rows[-1]
    summary = {
        "scheme": scheme,
        "polynomial_order": order,
        "success": bool(solution.success),
        "termination": "IR_G_TARGET",
        "selected_relevant_sign": sign,
        "t_endpoint": float(solution.t_events[0][0]),
        "steps": int(len(solution.t)),
        "function_evaluations": int(solution.nfev),
        "g_endpoint": float(endpoint["g"]),
        "eta_psi_endpoint": float(endpoint["eta_psi"]),
        "eta_Newton_physical_endpoint": float(
            endpoint["eta_Newton_physical"]
        ),
        "W_O4_endpoint": float(endpoint["W_O4_u_over_g2"]),
        "A2_endpoint": float(endpoint["A2_a_over_g_power"]),
        "A3_endpoint": float(endpoint["A3_a_over_g_power"]),
        "r3_raw_endpoint": float(endpoint["r3_raw"]),
        "C24_raw_endpoint": float(endpoint["C24_raw_polynomial"]),
        "dimensionless_sigma24_raw_kernel_endpoint": float(
            endpoint["dimensionless_sigma24_raw_kernel"]
        ),
        "maximum_eta_self_consistency_residual": maximum_eta_residual,
        "minimum_scalar_transverse_x_le_0p1": minimum_scalar_transverse,
        "minimum_scalar_longitudinal_x_le_0p1": minimum_scalar_longitudinal,
        "all_sampled_scalar_convex": all(
            bool(row["convex_x_le_0p1"]) for row in rows
        ),
    }
    print(
        f"{MARKER}_TRAJECTORY scheme={scheme} N={order} "
        f"g={summary['g_endpoint']:.3e} r3={summary['r3_raw_endpoint']:.6e} "
        f"W_O4={summary['W_O4_endpoint']:.9g}",
        flush=True,
    )
    return solution, rows, summary


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(
        source_hashes[str(path)] == expected
        for path, expected in EXPECTED_HASHES.items()
    )
    if not source_hashes_match:
        raise RuntimeError(
            f"source hash mismatch: "
            f"{[str(path) for path, expected in EXPECTED_HASHES.items() if source_hashes[str(path)] != expected]}"
        )

    parent_text_4942 = LOCAL_4942.read_text(encoding="utf-8")
    parent_text_4943 = LOCAL_4943.read_text(encoding="utf-8")
    parent_text_4947 = LOCAL_4947.read_text(encoding="utf-8")
    source_clause_checks = {
        "O4_local_zero_branch": "T_mn^(O4)|psi=0=0" in parent_text_4942,
        "O2_degree_four": "O2: degree 4" in parent_text_4943,
        "O5_reflection_forbidden": "u_O5=0" in parent_text_4943,
        "matter_tadpole_zero": "delta Gamma_eff/delta psi|psi=0=0" in parent_text_4943,
        "local_GR_Newton_chain": "Einstein -> Poisson -> inverse-square force" in parent_text_4947,
        "local_Maxwell_stress_chain": "Maxwell -> Lorentz -> stress -> Poynting chain" in parent_text_4947,
        "4956_functional_germ": "local fixed-function germ retained" in CHECKPOINT_4956.read_text(encoding="utf-8"),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause failure: {source_clause_checks}")

    parent_result = json.loads(O4_RESULT.read_text(encoding="utf-8"))
    parent_coordinates = parent_result["minimal_O4_completed_point"]["coordinates"]
    parent_initial = np.array(list(parent_coordinates.values()), dtype=float)
    source_fixed_rows = read_csv(FIXED_4956)
    rate_result = json.loads(RATE_4954.read_text(encoding="utf-8"))
    rate_polynomial = {
        key: float(rate_result["on_shell_24"][key])
        for key in ("C0", "C1", "C2")
    }

    projector = functional_px.FunctionalPXProjector(
        MAX_ORDER, QUADRATURE_ORDER
    )
    flow = CombinedFunctionalFlow(projector)
    fixed_solutions, fixed_rows = solve_fixed_points(
        flow, parent_initial, source_fixed_rows
    )

    spectrum_rows: list[dict[str, Any]] = []
    trajectory_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    regularity_rows: list[dict[str, Any]] = []
    relevant_counts: dict[str, dict[int, int]] = {}
    for scheme in SCHEMES:
        relevant_counts[scheme] = {}
        for order in TRAJECTORY_ORDERS:
            fixed = fixed_solutions[scheme][order]
            gravity_vector, spectrum, relevant_count = stability_data(
                flow, fixed, scheme, order
            )
            relevant_counts[scheme][order] = relevant_count
            spectrum_rows.extend(spectrum)
            solution, rows, summary = integrate_trajectory(
                flow,
                fixed,
                gravity_vector,
                scheme,
                order,
                rate_polynomial,
            )
            trajectory_rows.extend(rows)
            endpoint_rows.append(
                {
                    **summary,
                    "status": "IR_ENDPOINT_RAW_FUNCTIONAL_COORDINATES",
                }
            )
            if order == MAX_ORDER:
                selected_indices = (0, 30, 60, 90, 120)
                selected_rows = [rows[index] for index in selected_indices]
                for selected in selected_rows:
                    coefficients = np.array(
                        [0.0, 0.5]
                        + [float(selected[f"a{coordinate}"]) for coordinate in range(2, order + 1)]
                    )
                    gate = projector.direct_hessian_minimum(
                        coefficients, float(selected["g"]), LOCAL_X_MAX
                    )
                    regularity_rows.append(
                        {
                            "scheme": scheme,
                            "polynomial_order": order,
                            "sample_index": selected["sample_index"],
                            "t_log_k_over_seed": selected[
                                "t_log_k_over_seed"
                            ],
                            "g": selected["g"],
                            **gate,
                            "scalar_convex": selected["convex_x_le_0p1"],
                            "status": (
                                "TRAJECTORY_LOCAL_HESSIAN_REGULAR"
                                if gate["minimum_singular_value"] > 1.0e-6
                                and selected["convex_x_le_0p1"]
                                else "TRAJECTORY_LOCAL_REGULARITY_FAILED"
                            ),
                        }
                    )

    fixed_rows = tagged(fixed_rows)
    spectrum_rows = tagged(spectrum_rows)
    trajectory_rows = tagged(trajectory_rows)
    endpoint_rows = tagged(endpoint_rows)
    regularity_rows = tagged(regularity_rows)

    convergence_rows: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        endpoints = {
            int(row["polynomial_order"]): row
            for row in endpoint_rows
            if row["scheme"] == scheme
        }
        lower = endpoints[TRAJECTORY_ORDERS[0]]
        upper = endpoints[TRAJECTORY_ORDERS[1]]
        for coordinate in (
            "A2_endpoint",
            "A3_endpoint",
            "r3_raw_endpoint",
            "dimensionless_sigma24_raw_kernel_endpoint",
            "W_O4_endpoint",
        ):
            lower_value = float(lower[coordinate])
            upper_value = float(upper[coordinate])
            relative = abs(upper_value - lower_value) / max(
                abs(upper_value), 1.0e-300
            )
            convergence_rows.append(
                {
                    "scheme": scheme,
                    "coordinate": coordinate,
                    "lower_order": TRAJECTORY_ORDERS[0],
                    "upper_order": TRAJECTORY_ORDERS[1],
                    "lower_value": lower_value,
                    "upper_value": upper_value,
                    "relative_difference": relative,
                    "converged_below_1e_minus_3": relative < 1.0e-3,
                    "status": "IR_ORDER_CONVERGENCE_GATE",
                }
            )
    convergence_rows = tagged(convergence_rows)

    minimum_hessian = min(
        float(row["minimum_singular_value"]) for row in regularity_rows
    )
    all_trajectories_reach_ir = all(
        row["termination"] == "IR_G_TARGET" for row in endpoint_rows
    )
    all_local_regular = all(
        row["status"] == "TRAJECTORY_LOCAL_HESSIAN_REGULAR"
        for row in regularity_rows
    )
    low_ir_converged = all(
        bool(row["converged_below_1e_minus_3"])
        for row in convergence_rows
        if row["coordinate"] in {"A2_endpoint", "A3_endpoint", "W_O4_endpoint"}
    )
    one_relevant = all(
        count == 1
        for scheme_counts in relevant_counts.values()
        for count in scheme_counts.values()
    )

    residual_rows = tagged(
        [
            {
                "operator": "P(X)_n_ge_2",
                "local_psi0_variation": "first and quadratic variations vanish for n>=2",
                "trajectory_treatment": "functional coefficients N6/N8 integrated self-consistently",
                "local_GR_status": "EXACTLY_SILENT_ON_PSI_ZERO",
                "nonzero_state_status": "LOCAL_X_LE_0P1_TRAJECTORY_REGULAR",
                "remaining_residual": "global fixed function and essential quotient",
            },
            {
                "operator": "O2=X(nabla_nabla_psi)^2",
                "local_psi0_variation": "quadratic Hessian zero by scalar field degree four",
                "trajectory_treatment": "not required by the psi=0 local linearized Hessian",
                "local_GR_status": "EXACTLY_SILENT_ON_PSI_ZERO",
                "nonzero_state_status": "BETA_FUNCTION_OPEN",
                "remaining_residual": "nonzero-background motion states",
            },
            {
                "operator": "O4=C2 X",
                "local_psi0_variation": "stress and scalar source vanish; scalar cone remains metric",
                "trajectory_treatment": "eta_psi weighted Newton C2 RC2 and beta_u terms included",
                "local_GR_status": "EXACTLY_SILENT_ON_PSI_ZERO",
                "nonzero_state_status": "SELF_CONSISTENT_TRAJECTORY_INCLUDED",
                "remaining_residual": "none in declared natural TypeII local branch",
            },
            {
                "operator": "O5=C(nabla_psi)^2(nabla_nabla_psi)",
                "local_psi0_variation": "odd under selected motion reflection",
                "trajectory_treatment": "u_O5=0 invariant under reflection-preserving flow",
                "local_GR_status": "EXACTLY_FORBIDDEN",
                "nonzero_state_status": "REFLECTION_BREAKING_BRANCH_EXCLUDED",
                "remaining_residual": "only if parent reflection is abandoned",
            },
            {
                "operator": "raw_to_essential_X2_X3_map",
                "local_psi0_variation": "irrelevant to local massless metric residue",
                "trajectory_treatment": "raw functional r3 and invariant raw rate kernel recorded",
                "local_GR_status": "NO_LOCAL_GR_OBSTRUCTION",
                "nonzero_state_status": "PHYSICAL_RATE_PROMOTION_BLOCKED",
                "remaining_residual": "six-derivative essential quotient and amplitude-consistent matching",
            },
        ]
    )

    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4957_01_combined_fixed",
                "question": "Does the functional motion sector coexist with the scalar-backreacted C3-CFF-F4-O4 fixed point?",
                "answer": "yes through N8 in both regulator schemes",
                "status": "SELF_CONSISTENT_COMBINED_FIXED_POINTS_RETAINED",
                "next_action": "use the GR-connected relevant mode",
            },
            {
                "decision_id": "DEC4957_02_relevant",
                "question": "Does the combined massless block retain one GR-connected relevant direction?",
                "answer": "yes" if one_relevant else "no",
                "status": "ONE_GR_CONNECTED_RELEVANT_DIRECTION_RETAINED" if one_relevant else "RELEVANT_INDEX_GATE_FAILED",
                "next_action": "integrate only the source-selected separatrix",
            },
            {
                "decision_id": "DEC4957_03_trajectory",
                "question": "Do the N6 and N8 functional trajectories reach the Gaussian GR regime?",
                "answer": "yes" if all_trajectories_reach_ir else "no",
                "status": "FUNCTIONAL_GR_CONNECTED_TRAJECTORY_RETAINED" if all_trajectories_reach_ir else "FUNCTIONAL_TRAJECTORY_FAILED",
                "next_action": "retain order and regulator uncertainty",
            },
            {
                "decision_id": "DEC4957_04_regularity",
                "question": "Does the trajectory remain regular on the proven x<=0.1 domain?",
                "answer": "yes" if all_local_regular else "no",
                "status": "TRAJECTORY_LOCAL_REGULARITY_RETAINED" if all_local_regular else "TRAJECTORY_LOCAL_REGULARITY_FAILED",
                "next_action": "forbid extrapolation beyond the supported domain",
            },
            {
                "decision_id": "DEC4957_05_O2",
                "question": "Must the open O2 beta block the psi=0 local GR branch?",
                "answer": "no: its quadratic Hessian vanishes by field degree",
                "status": "O2_LOCAL_LINEAR_RESIDUAL_EXACT_ZERO",
                "next_action": "retain O2 only for nonzero motion states",
            },
            {
                "decision_id": "DEC4957_06_O4",
                "question": "Is O4 included with the functional anomalous dimension?",
                "answer": "yes in the declared natural TypeII source scheme",
                "status": "O4_ETA_WEIGHTED_TRAJECTORY_INCLUDED",
                "next_action": "carry its Wilson endpoint as a derived coefficient",
            },
            {
                "decision_id": "DEC4957_07_O5",
                "question": "Does O5 survive the selected reflection-even parent?",
                "answer": "no",
                "status": "O5_REFLECTION_FORBIDDEN",
                "next_action": "do not add an odd closure",
            },
            {
                "decision_id": "DEC4957_08_ratio",
                "question": "Is the raw infrared r3 already the physical 4954 amplitude ratio?",
                "answer": "no",
                "status": "RAW_IR_RATIO_DERIVED_ESSENTIAL_RATE_MAP_OPEN",
                "next_action": "derive the six-derivative essential quotient or compute the invariant amplitude directly",
            },
            {
                "decision_id": "DEC4957_09_local",
                "question": "Is the 4947 local GR Newton Maxwell source chain obstructed?",
                "answer": "no",
                "status": "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
                "next_action": "advance to physical higher-gradient residual matching",
            },
            {
                "decision_id": "DEC4957_10_full",
                "question": "Does this establish full MTS unification?",
                "answer": "no",
                "status": "FULL_MTS_PROMOTION_BLOCKED",
                "next_action": "close the essential amplitude map and empirical residuals",
            },
        ]
    )

    write_csv(FIXED_CSV, fixed_rows)
    write_csv(SPECTRUM_CSV, spectrum_rows)
    write_csv(TRAJECTORY_CSV, trajectory_rows)
    write_csv(ENDPOINT_CSV, convergence_rows)
    write_csv(REGULARITY_CSV, regularity_rows)
    write_csv(RESIDUAL_CSV, residual_rows)
    write_csv(DECISION_CSV, decision_rows)

    endpoint_summary = {
        f"{row['scheme']}_N{row['polynomial_order']}": {
            key: row[key]
            for key in (
                "g_endpoint",
                "eta_psi_endpoint",
                "eta_Newton_physical_endpoint",
                "W_O4_endpoint",
                "A2_endpoint",
                "A3_endpoint",
                "r3_raw_endpoint",
                "C24_raw_endpoint",
                "dimensionless_sigma24_raw_kernel_endpoint",
                "all_sampled_scalar_convex",
            )
        }
        for row in endpoint_rows
    }
    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "flow_contract": {
            "parent_coordinates": list(PARENT_COORDINATES),
            "motion_orders_fixed": list(range(2, MAX_ORDER + 1)),
            "motion_orders_trajectory": list(TRAJECTORY_ORDERS),
            "schemes": list(SCHEMES),
            "quadrature_order": QUADRATURE_ORDER,
            "IR_g_target": IR_G_TARGET,
            "eta_Newton_dynamic_identity": "eta_N=beta_g/g-2",
            "eta_psi_self_consistency": "solved algebraically from affine regulator and parent source insertions",
            "scalar_Newton_weight": "1-eta_psi/4",
            "O4_C2_weight": "1-eta_psi/8",
            "O4_RC2_weight": "1-eta_psi/6",
            "O4_beta": "beta_u=(4+eta_psi)u-gamma_C2/2",
        },
        "combined_fixed_points": {
            scheme: {
                "N8": next(
                    row
                    for row in fixed_rows
                    if row["scheme"] == scheme
                    and int(row["polynomial_order"]) == MAX_ORDER
                )
            }
            for scheme in SCHEMES
        },
        "relevant_direction_counts": relevant_counts,
        "endpoint_summary": endpoint_summary,
        "gates": {
            "combined_fixed_points_through_N8": True,
            "one_GR_connected_relevant_direction": one_relevant,
            "all_functional_trajectories_reach_IR": all_trajectories_reach_ir,
            "low_IR_coordinates_order_converged": low_ir_converged,
            "trajectory_local_x_le_0p1_regular": all_local_regular,
            "minimum_trajectory_Hessian_singular_value": minimum_hessian,
            "O2_local_linear_residual": "EXACT_ZERO_BY_FIELD_DEGREE",
            "O4_functional_eta_trajectory": "INCLUDED",
            "O5": "FORBIDDEN_BY_REFLECTION",
            "raw_IR_r3": "DERIVED",
            "physical_essential_IR_r3": "OPEN",
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"{MARKER}_DONE fixed=True relevant={one_relevant} "
        f"IR={all_trajectories_reach_ir} regular={all_local_regular} "
        f"essential_r3=False",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

