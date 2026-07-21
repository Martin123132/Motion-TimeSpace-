from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4968"
TRAJECTORY_4957 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv"
)
FIXED_4957 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "combined_functional_fixed_point_convergence.csv"
)
COMPACT_4964 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4964"
    / "p8plus_tail_norm_gate.csv"
)
RESULT_4967 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4967"
    / "p8_GR_trajectory_and_static_bound_results.json"
)
CFF_RESULT = SOURCE / "CFF_squared_p8_helicity_source_results.json"
FIXED_CSV = SOURCE / "p8_CFF_completed_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_CFF_completed_GR_connected_trajectory.csv"
CONVERGENCE_CSV = SOURCE / "p8_CFF_completed_IR_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_CFF_completed_static_compact_response.csv"
RESULT_JSON = SOURCE / "p8_CFF_completed_trajectory_and_static_bound_results.json"
MARKER = "MTS_4968_CFF_COMPLETED_P8_TRAJECTORY_STATIC_BOUND"
CHECKED_DATE = "2026-07-13"
TRAJECTORY_ORDERS = (6, 8)
SCHEMES = ("dynamic_etaN", "reference_etaN0")
SAMPLE_COUNT = 121
SCENARIO = "C3_plus_O4_squared_plus_CFF_squared"
EXPECTED_HASHES = {
    TRAJECTORY_4957: "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    FIXED_4957: "f6d7685517b17b25119d4f89246ba7804c69c37fcd52b99f3fd027f3e75cf734",
    COMPACT_4964: "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    RESULT_4967: "415f9dbff1b903e6aee5921c6516d8a53fa4373feb4f38fb4d2d0943eda9d694",
    CFF_RESULT: "ce728a854ffb92fbdb3ffeb16727357a6c69433fb4e6edc1a66bd1b952f2a19d",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
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


def interpolators(rows: list[dict[str, str]]) -> dict[str, PchipInterpolator]:
    ordered = sorted(rows, key=lambda row: float(row["t_log_k_over_seed"]))
    times = np.array(
        [float(row["t_log_k_over_seed"]) for row in ordered], dtype=float
    )
    values = {
        "g": [float(row["g"]) for row in ordered],
        "g_CFF": [float(row["g_CFF"]) for row in ordered],
        "h_C3": [float(row["h_C3"]) for row in ordered],
        "u_O4": [float(row["u_O4"]) for row in ordered],
        "eta_psi": [float(row["eta_psi"]) for row in ordered],
        "beta_g_over_g": [
            float(row["eta_Newton_physical"]) + 2.0 for row in ordered
        ],
    }
    return {
        name: PchipInterpolator(times, np.array(field, dtype=float), extrapolate=False)
        for name, field in values.items()
    }


def evaluate_fields(
    functions: dict[str, PchipInterpolator], time_value: float
) -> dict[str, float]:
    return {name: float(function(time_value)) for name, function in functions.items()}


def source_components(fields: dict[str, float]) -> dict[str, float]:
    gravity = fields["g"]
    a_c3 = fields["h_C3"] / gravity
    source_c3_c = -6.0 * a_c3
    source_c3_t = 6.0 * a_c3
    source_o4_c = (
        fields["u_O4"] ** 2
        * (1.0 - fields["eta_psi"] / 10.0)
        / (math.pi * gravity**2)
    )
    source_cff_plus = (
        -79.0 * fields["g_CFF"] ** 2 / (140.0 * math.pi * gravity**2)
    )
    source_cff_c = source_cff_plus / 2.0
    source_cff_t = source_cff_plus / 2.0
    return {
        "A_C3_h_over_g": a_c3,
        "W_C_gCFF_over_16pi_g": fields["g_CFF"] / (16.0 * math.pi * gravity),
        "source_B_C_C3": source_c3_c,
        "source_B_t_C3": source_c3_t,
        "source_B_C_O4_squared": source_o4_c,
        "source_B_t_O4_squared": 0.0,
        "source_B_minus_CFF_squared": 0.0,
        "source_B_plus_CFF_squared": source_cff_plus,
        "source_B_C_CFF_squared": source_cff_c,
        "source_B_t_CFF_squared": source_cff_t,
        "source_B_C_total": source_c3_c + source_o4_c + source_cff_c,
        "source_B_t_total": source_c3_t + source_cff_t,
    }


def integrate_trajectory(
    source_rows: list[dict[str, str]], fixed_row: dict[str, str]
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    functions = interpolators(source_rows)
    times = sorted(float(row["t_log_k_over_seed"]) for row in source_rows)
    t_start = 0.0
    t_end = times[0]
    fixed_fields = {
        "g": float(fixed_row["g"]),
        "g_CFF": float(fixed_row["g_CFF"]),
        "h_C3": float(fixed_row["h_C3"]),
        "u_O4": float(fixed_row["u_O4"]),
        "eta_psi": float(fixed_row["eta_psi"]),
        "beta_g_over_g": 0.0,
    }
    fixed_sources = source_components(fixed_fields)
    initial = np.array(
        [
            -fixed_sources["source_B_C_total"] / 4.0,
            -fixed_sources["source_B_t_total"] / 4.0,
        ],
        dtype=float,
    )

    def right_hand_side(time_value: float, state: np.ndarray) -> np.ndarray:
        fields = evaluate_fields(functions, time_value)
        sources = source_components(fields)
        homogeneous = 4.0 - 2.0 * fields["beta_g_over_g"]
        return np.array(
            [
                homogeneous * state[0] + sources["source_B_C_total"],
                homogeneous * state[1] + sources["source_B_t_total"],
            ],
            dtype=float,
        )

    solution = solve_ivp(
        right_hand_side,
        (t_start, t_end),
        initial,
        method="DOP853",
        rtol=2.0e-11,
        atol=2.0e-14,
        max_step=0.05,
        dense_output=True,
    )
    if not solution.success:
        raise RuntimeError(f"p8 CFF trajectory integration failed: {solution.message}")
    sample_times = np.linspace(t_start, t_end, SAMPLE_COUNT)
    samples = solution.sol(sample_times)
    rows: list[dict[str, Any]] = []
    for sample_index, time_value in enumerate(sample_times):
        fields = evaluate_fields(functions, float(time_value))
        sources = source_components(fields)
        homogeneous = 4.0 - 2.0 * fields["beta_g_over_g"]
        b_c = float(samples[0, sample_index])
        b_t = float(samples[1, sample_index])
        rows.append(
            {
                "scheme": fixed_row["scheme"],
                "polynomial_order": int(fixed_row["polynomial_order"]),
                "scenario": SCENARIO,
                "sample_index": sample_index,
                "t_log_k_over_seed": float(time_value),
                **fields,
                **sources,
                "homogeneous_B_slope": homogeneous,
                "B_C": b_c,
                "B_t": b_t,
                "B_minus": b_c - b_t,
                "B_plus": b_c + b_t,
                "v_C_equals_g3_B_C": fields["g"] ** 3 * b_c,
                "v_t_equals_g3_B_t": fields["g"] ** 3 * b_t,
                "status": "CFF_COMPLETED_SOURCE_TRUNCATED_GR_CONNECTED_P8_TRAJECTORY",
            }
        )
    fixed_beta_c = 4.0 * initial[0] + fixed_sources["source_B_C_total"]
    fixed_beta_t = 4.0 * initial[1] + fixed_sources["source_B_t_total"]
    fixed = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "scenario": SCENARIO,
        "g_star": fixed_fields["g"],
        "g_CFF_star": fixed_fields["g_CFF"],
        "W_C_star": fixed_sources["W_C_gCFF_over_16pi_g"],
        "B_C_star": float(initial[0]),
        "B_t_star": float(initial[1]),
        "B_minus_star": float(initial[0] - initial[1]),
        "B_plus_star": float(initial[0] + initial[1]),
        "source_B_plus_CFF_squared_star": fixed_sources[
            "source_B_plus_CFF_squared"
        ],
        "p8_subblock_eigenvalue_C": 4.0,
        "p8_subblock_eigenvalue_t": 4.0,
        "beta_B_C_fixed_residual": fixed_beta_c,
        "beta_B_t_fixed_residual": fixed_beta_t,
        "new_relevant_directions": 0,
        "status": "CFF_COMPLETED_UV_REGULAR_SOURCE_SELECTED_P8_FIXED_POINT",
    }
    endpoint = rows[-1]
    summary = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "scenario": SCENARIO,
        "success": bool(solution.success),
        "t_endpoint": t_end,
        "function_evaluations": int(solution.nfev),
        "B_C_endpoint": endpoint["B_C"],
        "B_t_endpoint": endpoint["B_t"],
        "B_minus_endpoint": endpoint["B_minus"],
        "B_plus_endpoint": endpoint["B_plus"],
        "g_endpoint": endpoint["g"],
        "g_CFF_endpoint": endpoint["g_CFF"],
        "W_C_endpoint": endpoint["W_C_gCFF_over_16pi_g"],
        "CFF_B_plus_source_endpoint": endpoint["source_B_plus_CFF_squared"],
        "status": "CFF_COMPLETED_SOURCE_TRUNCATED_IR_ENDPOINT",
    }
    return rows, fixed, summary


def convergence_rows(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index = {
        (row["scheme"], int(row["polynomial_order"])): row for row in summaries
    }
    rows: list[dict[str, Any]] = []
    coordinates = (
        "B_C_endpoint",
        "B_t_endpoint",
        "B_minus_endpoint",
        "B_plus_endpoint",
    )
    for scheme in SCHEMES:
        lower = index[(scheme, 6)]
        upper = index[(scheme, 8)]
        for coordinate in coordinates:
            difference = abs(float(upper[coordinate]) - float(lower[coordinate]))
            scale = max(
                abs(float(upper[coordinate])),
                abs(float(lower[coordinate])),
                1.0e-30,
            )
            rows.append(
                {
                    "comparison": "N6_to_N8",
                    "scheme": scheme,
                    "coordinate": coordinate,
                    "lower_value": lower[coordinate],
                    "upper_value": upper[coordinate],
                    "absolute_difference": difference,
                    "relative_difference": difference / scale,
                    "status": (
                        "ORDER_CONVERGED"
                        if difference / scale <= 1.0e-3
                        else "ORDER_SENSITIVITY_EXCEEDS_GATE"
                    ),
                }
            )
    for coordinate in coordinates:
        dynamic = index[("dynamic_etaN", 8)]
        reference = index[("reference_etaN0", 8)]
        difference = abs(float(dynamic[coordinate]) - float(reference[coordinate]))
        scale = max(
            abs(float(dynamic[coordinate])),
            abs(float(reference[coordinate])),
            1.0e-30,
        )
        rows.append(
            {
                "comparison": "N8_scheme_bracket",
                "scheme": "dynamic_vs_reference",
                "coordinate": coordinate,
                "lower_value": min(dynamic[coordinate], reference[coordinate]),
                "upper_value": max(dynamic[coordinate], reference[coordinate]),
                "absolute_difference": difference,
                "relative_difference": difference / scale,
                "status": "SCHEME_BRACKET_RECORDED",
            }
        )
    return tagged(rows)


def static_response_rows(
    summaries: list[dict[str, Any]], objects: list[dict[str, str]]
) -> list[dict[str, Any]]:
    endpoints = [row for row in summaries if int(row["polynomial_order"]) == 8]
    rows: list[dict[str, Any]] = []
    for endpoint in endpoints:
        b_c = float(endpoint["B_C_endpoint"])
        for source in objects:
            mass_length = float(source["mass_length_m"])
            radius = float(source["radius_m"])
            chi = float(source["chi_lP2_curvature"])
            epsilon_gate = float(source["epsilon_gate"])
            compactness = mass_length / radius
            factor_a = 128.0 * (8.0 - 11.0 * compactness)
            factor_b = 128.0 * (36.0 - 67.0 * compactness)
            delta_a = factor_a * b_c * chi**3
            delta_b = factor_b * b_c * chi**3
            bmax_a = epsilon_gate / (abs(factor_a) * chi**3)
            bmax_b = epsilon_gate / (abs(factor_b) * chi**3)
            joint_bound = min(bmax_a, bmax_b)
            rows.append(
                {
                    "scheme": endpoint["scheme"],
                    "polynomial_order": 8,
                    "scenario": SCENARIO,
                    "object_id": source["object_id"],
                    "source_class": source["source_class"],
                    "compactness_M_over_r": compactness,
                    "chi_lP2_curvature": chi,
                    "B_C_endpoint": b_c,
                    "delta_A": delta_a,
                    "delta_B": delta_b,
                    "max_abs_metric_residual": max(abs(delta_a), abs(delta_b)),
                    "epsilon_gate": epsilon_gate,
                    "B_C_max_joint_gate": joint_bound,
                    "candidate_to_joint_bound_ratio": abs(b_c) / joint_bound,
                    "static_B_t_weight": 0.0,
                    "status": "CFF_COMPLETED_SOURCE_TRUNCATED_STATIC_CORRECTION_BELOW_GATE",
                    "source_path": source["source_path"],
                }
            )
    return tagged(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    if any(digest(path) != expected for path, expected in EXPECTED_HASHES.items()):
        raise RuntimeError("4968 trajectory source hash mismatch")
    cff_result = json.loads(CFF_RESULT.read_text(encoding="utf-8"))
    required_formula = "source_beta_Bplus=-79 g_CFF^2/(140 pi g^2)"
    if (
        not cff_result["all_checks_pass"]
        or cff_result["decision"]["running_formula"] != required_formula
    ):
        raise RuntimeError("CFF helicity source result is not valid for trajectory use")
    trajectory_source = read_csv(TRAJECTORY_4957)
    fixed_source = read_csv(FIXED_4957)
    trajectory_rows: list[dict[str, Any]] = []
    fixed_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in TRAJECTORY_ORDERS:
            source_rows = [
                row
                for row in trajectory_source
                if row["scheme"] == scheme
                and int(row["polynomial_order"]) == order
            ]
            if len(source_rows) != SAMPLE_COUNT:
                raise RuntimeError(
                    f"expected {SAMPLE_COUNT} rows for {scheme} N={order}"
                )
            fixed_candidates = [
                row
                for row in fixed_source
                if row["scheme"] == scheme
                and int(row["polynomial_order"]) == order
            ]
            if len(fixed_candidates) != 1:
                raise RuntimeError(f"fixed-point row mismatch for {scheme} N={order}")
            run_rows, fixed, summary = integrate_trajectory(
                source_rows, fixed_candidates[0]
            )
            trajectory_rows.extend(run_rows)
            fixed_rows.append(fixed)
            summaries.append(summary)
    convergence = convergence_rows(summaries)
    objects = [
        row
        for row in read_csv(COMPACT_4964)
        if row["row_type"] == "compact_object_gate"
    ]
    static = static_response_rows(summaries, objects)
    prior = json.loads(RESULT_4967.read_text(encoding="utf-8"))
    prior_index = {
        row["scheme"]: row for row in prior["combined_N8_endpoints"]
    }
    completed_n8 = [
        row for row in summaries if int(row["polynomial_order"]) == 8
    ]
    increments = {
        row["scheme"]: {
            coordinate: float(row[coordinate])
            - float(prior_index[row["scheme"]][coordinate])
            for coordinate in (
                "B_C_endpoint",
                "B_t_endpoint",
                "B_minus_endpoint",
                "B_plus_endpoint",
            )
        }
        for row in completed_n8
    }
    maximum_order_sensitivity = max(
        float(row["relative_difference"])
        for row in convergence
        if row["comparison"] == "N6_to_N8"
    )
    maximum_static = max(float(row["max_abs_metric_residual"]) for row in static)
    maximum_fixed_residual = max(
        max(
            abs(float(row["beta_B_C_fixed_residual"])),
            abs(float(row["beta_B_t_fixed_residual"])),
        )
        for row in fixed_rows
    )
    checks = {
        "four_trajectory_runs": len(summaries) == 4,
        "all_trajectory_runs_succeeded": all(row["success"] for row in summaries),
        "fixed_residual_below_1e_15": maximum_fixed_residual <= 1.0e-15,
        "N6_N8_order_gate": maximum_order_sensitivity <= 1.0e-3,
        "static_rows_complete": len(static) == 2 * len(objects),
        "all_static_rows_below_gate": all(
            float(row["max_abs_metric_residual"]) <= float(row["epsilon_gate"])
            for row in static
        ),
        "CFF_source_nonzero": all(
            float(row["source_B_plus_CFF_squared_star"]) != 0.0
            for row in fixed_rows
        ),
        "same_helicity_coordinate_unchanged_by_direct_CFF_source": all(
            abs(value["B_minus_endpoint"]) <= 2.0e-8
            for value in increments.values()
        ),
        "mixed_helicity_coordinate_shift_nonzero": all(
            abs(value["B_plus_endpoint"]) > 1.0e-4
            for value in increments.values()
        ),
    }
    write_csv(FIXED_CSV, tagged(fixed_rows))
    write_csv(TRAJECTORY_CSV, tagged(trajectory_rows))
    write_csv(CONVERGENCE_CSV, convergence)
    write_csv(STATIC_CSV, static)
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": hashes,
        "CFF_source": {
            "gamma_C_R4": "0",
            "gamma_C_R4prime": "-79 W_C^2/(70 pi^2)",
            "source_beta_Bminus": "0",
            "source_beta_Bplus": "-79 g_CFF^2/(140 pi g^2)",
            "source_beta_BC": "-79 g_CFF^2/(280 pi g^2)",
            "source_beta_Bt": "-79 g_CFF^2/(280 pi g^2)",
        },
        "p8_subblock_eigenvalues": [4.0, 4.0],
        "new_relevant_directions": 0,
        "completed_N8_endpoints": completed_n8,
        "increment_over_4967": increments,
        "maximum_N6_to_N8_relative_shift": maximum_order_sensitivity,
        "maximum_static_metric_residual": maximum_static,
        "full_source_complete": False,
        "remaining_p8_sources": [
            "three-loop pure-Einstein p8 source",
            "unselected parent matter and motion thresholds",
        ],
        "checks": checks,
        "outputs": {
            "fixed_point": relative(FIXED_CSV),
            "trajectory": relative(TRAJECTORY_CSV),
            "convergence": relative(CONVERGENCE_CSV),
            "static_response": relative(STATIC_CSV),
        },
        "all_checks_pass": all(checks.values()),
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{MARKER}_N8_ENDPOINTS={completed_n8}", flush=True)
    print(f"{MARKER}_MAX_STATIC={maximum_static:.12g}", flush=True)
    print(
        f"{MARKER}_MAX_ORDER_SHIFT={maximum_order_sensitivity:.12g}",
        flush=True,
    )
    if not result["all_checks_pass"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"4968 trajectory checks failed: {failed}")
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
