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

import Y5_R2FR_4934_completed_combined_flow as completed_flow


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_4934 = POST / "source-intake" / "functional_rg" / "4934"
SOURCE_4935 = POST / "source-intake" / "functional_rg" / "4935"
INPUT = SOURCE_4934 / "completed_combined_flow_results.json"
OUTPUT = SOURCE_4935 / "completed_fixed_point_trajectory_results.json"
TRACE_OUTPUT = SOURCE_4935 / "completed_fixed_point_GR_branch_trace.csv"

MARKER = "MTS_4935_COMPLETED_FIXED_POINT_TRAJECTORY"
EXPECTED_INPUT_HASH = "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978"
COORDINATE_NAMES = ("g", "g_plus", "g_minus", "g_CFF", "h_C3")
SEED_RELATIVE_AMPLITUDES = (1.0e-4, 3.0e-5, 1.0e-5, 3.0e-6, 1.0e-6)
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
POLE_STOP = 0.95 * 2.0 * math.pi
SCALED_NORM_STOP = 100.0
LOG_SUBTRACTION_SCALE = 16.0 * math.pi


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [
        {"real": float(value.real), "imag": float(value.imag)}
        for value in values
    ]


def equilibrated_condition(matrix: np.ndarray) -> float:
    scaled = np.asarray(matrix, dtype=float).copy()
    for _ in range(12):
        row_norms = np.max(np.abs(scaled), axis=1)
        column_norms = np.max(np.abs(scaled), axis=0)
        if np.any(row_norms == 0.0) or np.any(column_norms == 0.0):
            return math.inf
        scaled = scaled / np.sqrt(row_norms)[:, None]
        column_norms = np.max(np.abs(scaled), axis=0)
        scaled = scaled / np.sqrt(column_norms)[None, :]
    return float(np.linalg.cond(scaled))


def solve_metrics(
    system: Callable[[np.ndarray], tuple[np.ndarray, np.ndarray]],
    solve_unknowns: Callable[[np.ndarray], tuple[np.ndarray, float]],
    point: np.ndarray,
) -> dict[str, float]:
    matrix, vector = system(point)
    unknowns, raw_condition = solve_unknowns(point)
    residual = matrix @ unknowns - vector
    denominator = (
        np.linalg.norm(matrix, ord=np.inf) * np.linalg.norm(unknowns, ord=np.inf)
        + np.linalg.norm(vector, ord=np.inf)
    )
    return {
        "raw_condition_number": float(raw_condition),
        "equilibrated_condition_number": equilibrated_condition(matrix),
        "absolute_linear_residual_infinity_norm": float(
            np.linalg.norm(residual, ord=np.inf)
        ),
        "backward_relative_linear_residual": float(
            np.linalg.norm(residual, ord=np.inf) / max(denominator, 1.0e-300)
        ),
    }


def make_event(function: Callable[[float, np.ndarray], float]) -> Callable[[float, np.ndarray], float]:
    function.terminal = True
    function.direction = 0
    return function


def wilson_coordinates(point: np.ndarray, c3_log_source: float) -> dict[str, float]:
    g_value, plus_value, minus_value, cff_value, h_value = (
        float(value) for value in point
    )
    photon_denominator = (16.0 * math.pi * g_value) ** 2
    c3_log_coefficient = c3_log_source / 2.0
    return {
        "W_plus": plus_value / photon_denominator,
        "W_minus_cl16pi": (
            minus_value / g_value**2
            + (548.0 / 15.0) * math.log(LOG_SUBTRACTION_SCALE * g_value)
        )
        / (16.0 * math.pi) ** 2,
        "W_C": cff_value / (16.0 * math.pi * g_value),
        "A_C3": h_value / g_value - c3_log_coefficient * math.log(g_value),
        "raw_h_over_g": h_value / g_value,
        "raw_gplus_over_g2": plus_value / g_value**2,
        "raw_gminus_over_g2": minus_value / g_value**2,
        "raw_gCFF_over_g": cff_value / g_value,
    }


def estimate_gaussian_sources(beta: Callable[[np.ndarray], np.ndarray]) -> dict[str, Any]:
    g_values = np.logspace(-9, -6, 10)
    rows = []
    design = []
    c3_values = []
    minus_values = []
    plus_values = []
    for g_value in g_values:
        point = np.array([g_value, 0.0, 0.0, 0.0, 0.0], dtype=float)
        beta_value = beta(point)
        c3_source = float(beta_value[4] / g_value)
        minus_source = float(beta_value[2] / g_value**2)
        plus_source = float(beta_value[1] / g_value**2)
        rows.append(
            {
                "g": float(g_value),
                "beta_g_over_g": float(beta_value[0] / g_value),
                "beta_plus_over_g2": plus_source,
                "beta_minus_over_g2": minus_source,
                "beta_CFF_over_g2": float(beta_value[3] / g_value**2),
                "beta_h_over_g": c3_source,
            }
        )
        design.append([1.0, g_value * math.log(g_value), g_value])
        c3_values.append(c3_source)
        minus_values.append(minus_source)
        plus_values.append(plus_source)
    design_matrix = np.asarray(design, dtype=float)
    c3_intercept = float(np.linalg.lstsq(design_matrix, c3_values, rcond=None)[0][0])
    minus_intercept = float(np.linalg.lstsq(design_matrix, minus_values, rcond=None)[0][0])
    plus_intercept = float(np.linalg.lstsq(design_matrix, plus_values, rcond=None)[0][0])
    return {
        "ray_rows": rows,
        "c3_source_limit": c3_intercept,
        "c3_log_coefficient_in_h_over_g": c3_intercept / 2.0,
        "minus_source_limit": minus_intercept,
        "minus_expected_source": -1096.0 / 15.0,
        "plus_source_limit": plus_intercept,
        "fit_basis": "intercept + g log(g) + g on the zero-interaction Gaussian ray",
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    if digest(INPUT) != EXPECTED_INPUT_HASH:
        raise RuntimeError("checkpoint 4934 input hash mismatch")
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    fixed = source["source_complete_selected_row_fixed_point"]
    fixed_point = np.asarray(
        fixed["coordinates_g_gplus_gminus_gCFF_h"], dtype=float
    )
    stability_matrix = np.asarray(fixed["stability_matrix"], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eig(stability_matrix)
    relevant_indices = [index for index, value in enumerate(eigenvalues) if value.real < 0]
    if len(relevant_indices) != 1:
        raise RuntimeError(f"expected one relevant beta direction, found {relevant_indices}")
    relevant_index = relevant_indices[0]
    relevant_eigenvalue = eigenvalues[relevant_index]
    relevant_vector = np.real(eigenvectors[:, relevant_index])
    if relevant_vector[0] < 0:
        relevant_vector *= -1.0
    relative_norm = float(np.max(np.abs(relevant_vector / fixed_point)))
    relative_unit_vector = relevant_vector / relative_norm

    system, solve_unknowns, beta, _, _, _ = completed_flow.build_completed_solver()
    gaussian_sources = estimate_gaussian_sources(beta)
    c3_log_source = float(gaussian_sources["c3_source_limit"])
    scale = np.maximum(np.abs(fixed_point), np.array([1.0e-3, 1.0e-3, 1.0e-3, 1.0e-6, 1.0e-8]))

    def integrate_branch(sign: int, relative_amplitude: float) -> tuple[dict[str, Any], Any]:
        initial_point = fixed_point + sign * relative_amplitude * relative_unit_vector
        calls = 0

        def rhs(_time: float, point: np.ndarray) -> np.ndarray:
            nonlocal calls
            calls += 1
            value = beta(point)
            if not np.all(np.isfinite(value)):
                raise FloatingPointError("nonfinite beta value")
            return value

        @make_event
        def infrared_event(_time: float, point: np.ndarray) -> float:
            return float(point[0] - IR_G_TARGET)

        @make_event
        def pole_event(_time: float, point: np.ndarray) -> float:
            return float(POLE_STOP - point[0])

        @make_event
        def norm_event(_time: float, point: np.ndarray) -> float:
            return float(SCALED_NORM_STOP - np.max(np.abs(point / scale)))

        solution = solve_ivp(
            rhs,
            (0.0, T_IR_LIMIT),
            initial_point,
            method="DOP853",
            rtol=2.0e-9,
            atol=np.array([1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19]),
            max_step=0.08,
            dense_output=True,
            events=(infrared_event, pole_event, norm_event),
        )
        event_names = ("IR_G_TARGET", "NEWTON_POLE_MARGIN", "SCALED_NORM_LIMIT")
        event_name = "T_IR_LIMIT"
        for name, event_times in zip(event_names, solution.t_events):
            if len(event_times):
                event_name = name
                break
        if not solution.success and event_name == "T_IR_LIMIT":
            event_name = "INTEGRATOR_FAILURE"
        endpoint = np.asarray(solution.y[:, -1], dtype=float)
        endpoint_beta = beta(endpoint)
        endpoint_solve_metrics = solve_metrics(system, solve_unknowns, endpoint)
        branch = {
            "sign": sign,
            "relative_seed_amplitude": relative_amplitude,
            "initial_point": initial_point.tolist(),
            "success": bool(solution.success),
            "message": str(solution.message),
            "termination": event_name,
            "t_endpoint": float(solution.t[-1]),
            "steps": int(len(solution.t)),
            "beta_calls": calls,
            "endpoint": endpoint.tolist(),
            "endpoint_beta": endpoint_beta.tolist(),
            "endpoint_beta_over_coordinate": (
                endpoint_beta / np.where(np.abs(endpoint) > 0.0, endpoint, 1.0)
            ).tolist(),
            "endpoint_solve_metrics": endpoint_solve_metrics,
            "endpoint_wilson_coordinates": wilson_coordinates(endpoint, c3_log_source)
            if endpoint[0] > 0.0
            else None,
            "positive_Newton_through_stored_steps": bool(np.all(solution.y[0] > 0.0)),
            "finite_stored_trajectory": bool(np.all(np.isfinite(solution.y))),
        }
        return branch, solution

    physical_runs = []
    physical_solutions = []
    for amplitude in SEED_RELATIVE_AMPLITUDES:
        branch, solution = integrate_branch(-1, amplitude)
        physical_runs.append(branch)
        physical_solutions.append(solution)
        print(
            f"{MARKER}_PHYSICAL_SEED={amplitude:.1e}_TERM={branch['termination']}_G={branch['endpoint'][0]:.6e}",
            flush=True,
        )
    divergent_run, _ = integrate_branch(+1, SEED_RELATIVE_AMPLITUDES[-1])
    print(
        f"{MARKER}_OPPOSITE_TERM={divergent_run['termination']}_G={divergent_run['endpoint'][0]:.6e}",
        flush=True,
    )

    physical_wilsons = [run["endpoint_wilson_coordinates"] for run in physical_runs]
    convergence: dict[str, Any] = {}
    for name in ("W_plus", "W_minus_cl16pi", "W_C", "A_C3"):
        values = np.array([row[name] for row in physical_wilsons], dtype=float)
        reference = float(values[-1])
        convergence[name] = {
            "values_by_seed": values.tolist(),
            "reference_smallest_seed": reference,
            "max_absolute_difference": float(np.max(np.abs(values - reference))),
            "max_relative_difference": float(
                np.max(np.abs(values - reference)) / max(abs(reference), 1.0e-30)
            ),
        }

    representative_solution = physical_solutions[-1]
    sample_times = np.linspace(0.0, representative_solution.t[-1], 241)
    sample_points = representative_solution.sol(sample_times)
    trace_rows = []
    max_raw_condition = 0.0
    max_equilibrated_condition = 0.0
    max_backward_residual = 0.0
    for index, time_value in enumerate(sample_times):
        point = sample_points[:, index]
        beta_value = beta(point)
        metrics = solve_metrics(system, solve_unknowns, point)
        max_raw_condition = max(max_raw_condition, metrics["raw_condition_number"])
        max_equilibrated_condition = max(
            max_equilibrated_condition, metrics["equilibrated_condition_number"]
        )
        max_backward_residual = max(
            max_backward_residual, metrics["backward_relative_linear_residual"]
        )
        wilsons = wilson_coordinates(point, c3_log_source)
        trace_rows.append(
            {
                "t_log_k_over_seed": float(time_value),
                **dict(zip(COORDINATE_NAMES, (float(value) for value in point))),
                **{
                    f"beta_{name}": float(value)
                    for name, value in zip(COORDINATE_NAMES, beta_value)
                },
                "projection_condition_number": metrics["raw_condition_number"],
                "equilibrated_projection_condition_number": metrics[
                    "equilibrated_condition_number"
                ],
                "backward_relative_linear_residual": metrics[
                    "backward_relative_linear_residual"
                ],
                **wilsons,
                "checkpoint_marker": MARKER,
                "valid_for_claim": False,
            }
        )

    checks = {
        "input_hash_locked": digest(INPUT) == EXPECTED_INPUT_HASH,
        "one_relevant_direction": len(relevant_indices) == 1,
        "all_negative_sign_runs_reach_IR_target": all(
            run["termination"] == "IR_G_TARGET" for run in physical_runs
        ),
        "all_negative_sign_runs_finite_positive_Newton": all(
            run["finite_stored_trajectory"] and run["positive_Newton_through_stored_steps"]
            for run in physical_runs
        ),
        "opposite_sign_does_not_reach_IR_target": divergent_run["termination"] != "IR_G_TARGET",
        "Gaussian_Newton_scaling_recovered": abs(
            gaussian_sources["ray_rows"][0]["beta_g_over_g"] - 2.0
        ) < 1.0e-6,
        "photon_minus_log_source_recovered": abs(
            gaussian_sources["minus_source_limit"] + 1096.0 / 15.0
        ) < 1.0e-4,
        "seed_converged_W_C": convergence["W_C"]["max_relative_difference"] < 5.0e-3,
        "seed_converged_W_plus": convergence["W_plus"]["max_relative_difference"] < 5.0e-3,
        "seed_converged_A_C3": convergence["A_C3"]["max_relative_difference"] < 5.0e-3,
        "finite_projection_condition_on_representative_branch": math.isfinite(
            max_raw_condition
        )
        and math.isfinite(max_equilibrated_condition),
        "small_backward_linear_residual_on_representative_branch": max_backward_residual
        < 1.0e-12,
    }
    if not all(checks.values()):
        raise RuntimeError(f"trajectory checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            INPUT.relative_to(ROOT).as_posix(): digest(INPUT),
        },
        "flow_contract": {
            "coordinates": list(COORDINATE_NAMES),
            "RG_time": "t=ln(k/k_seed); integrate toward decreasing t",
            "fixed_point": fixed_point.tolist(),
            "beta_residual_infinity_norm": fixed["beta_residual_infinity_norm"],
            "relevant_beta_eigenvalue": {
                "real": float(relevant_eigenvalue.real),
                "imag": float(relevant_eigenvalue.imag),
            },
            "relevant_critical_exponent": float(-relevant_eigenvalue.real),
            "relevant_relative_unit_vector": relative_unit_vector.tolist(),
            "negative_sign_is_candidate_GR_branch": True,
            "IR_g_target": IR_G_TARGET,
            "source_Newton_pole": 2.0 * math.pi,
        },
        "gaussian_source_extraction": gaussian_sources,
        "physical_branch_seed_runs": physical_runs,
        "opposite_branch_run": divergent_run,
        "seed_convergence": convergence,
        "representative_branch": {
            "relative_seed_amplitude": SEED_RELATIVE_AMPLITUDES[-1],
            "trace_rows": len(trace_rows),
            "trace_path": TRACE_OUTPUT.relative_to(ROOT).as_posix(),
            "maximum_raw_projection_condition_number": max_raw_condition,
            "maximum_equilibrated_projection_condition_number": max_equilibrated_condition,
            "maximum_backward_relative_linear_residual": max_backward_residual,
            "endpoint": physical_runs[-1]["endpoint"],
            "endpoint_wilson_coordinates": physical_runs[-1]["endpoint_wilson_coordinates"],
        },
        "checks": checks,
        "claim_boundary": {
            "GR_connected_minimal_trajectory_derived": True,
            "source_complete_minimal_point_has_Gaussian_IR_branch": True,
            "full_MTS_trajectory_derived": False,
            "motion_sector_included": False,
            "local_GR_Newton_Maxwell_promoted": False,
            "reason": "the trajectory is for the completed minimal C3-CFF-F4 source truncation; the parent motion/time/source Hessian and enlarged trajectory remain to be calculated",
        },
    }
    SOURCE_4935.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with TRACE_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(trace_rows[0]))
        writer.writeheader()
        writer.writerows(trace_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_TRACE_SHA256={digest(TRACE_OUTPUT)}", flush=True)
    print(f"{MARKER}_WILSONS={physical_runs[-1]['endpoint_wilson_coordinates']}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
