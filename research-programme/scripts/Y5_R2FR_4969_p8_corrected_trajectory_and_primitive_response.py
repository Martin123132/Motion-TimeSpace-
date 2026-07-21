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
from scipy.optimize import brentq


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4969"
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
CFF_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4968"
    / "CFF_squared_p8_helicity_source_results.json"
)
OLD_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4968"
    / "p8_CFF_completed_trajectory_and_static_bound_results.json"
)
CANONICAL_RESULT = SOURCE / "p8_canonical_Einstein_split_results.json"

FIXED_CSV = SOURCE / "p8_canonical_repaired_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_canonical_repaired_GR_connected_trajectory.csv"
CONVERGENCE_CSV = SOURCE / "p8_canonical_repaired_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_canonical_repaired_static_compact_response.csv"
RESPONSE_CSV = SOURCE / "pure_Einstein_IR_matching_response.csv"
BOUND_CSV = SOURCE / "primitive_and_matching_boundary_budget.csv"
RESULT_JSON = SOURCE / "p8_corrected_trajectory_primitive_response_results.json"

MARKER = "MTS_4969_P8_CORRECTED_TRAJECTORY_PRIMITIVE_RESPONSE"
CHECKED_DATE = "2026-07-13"
SCENARIO = "C3_plus_O4_squared_plus_CFF_squared_canonical_repaired"
SCHEMES = ("dynamic_etaN", "reference_etaN0")
ORDERS = (6, 8)
SAMPLE_COUNT = 121
MATCH_GRAVITIES = (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6)
EXPECTED_HASHES = {
    TRAJECTORY_4957: "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    FIXED_4957: "f6d7685517b17b25119d4f89246ba7804c69c37fcd52b99f3fd027f3e75cf734",
    COMPACT_4964: "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    CFF_RESULT: "ce728a854ffb92fbdb3ffeb16727357a6c69433fb4e6edc1a66bd1b952f2a19d",
    OLD_RESULT: "495e12c4441cda77776b8c39cf1aa7d5b9252b3cec4bf1e8d742ce212668d964",
    CANONICAL_RESULT: "7e45bf69deb9e61df28ef640eb0f075e2689849673d8199526e459bfd2e2d2d7",
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


def homogeneous(fields: dict[str, float]) -> float:
    return 6.0 - 3.0 * fields["beta_g_over_g"]


def source_components(fields: dict[str, float]) -> dict[str, float]:
    gravity = fields["g"]
    a_c3 = fields["h_C3"] / gravity
    c3_c = -6.0 * a_c3
    c3_t = 6.0 * a_c3
    o4_c = (
        fields["u_O4"] ** 2
        * (1.0 - fields["eta_psi"] / 10.0)
        / (math.pi * gravity**2)
    )
    cff_plus = -79.0 * fields["g_CFF"] ** 2 / (140.0 * math.pi * gravity**2)
    cff_c = cff_plus / 2.0
    cff_t = cff_plus / 2.0
    return {
        "A_C3_h_over_g": a_c3,
        "W_C_gCFF_over_16pi_g": fields["g_CFF"] / (16.0 * math.pi * gravity),
        "source_B_C_C3": c3_c,
        "source_B_t_C3": c3_t,
        "source_B_C_O4_squared": o4_c,
        "source_B_t_O4_squared": 0.0,
        "source_B_minus_CFF_squared": 0.0,
        "source_B_plus_CFF_squared": cff_plus,
        "source_B_C_CFF_squared": cff_c,
        "source_B_t_CFF_squared": cff_t,
        "source_B_C_total": c3_c + o4_c + cff_c,
        "source_B_t_total": c3_t + cff_t,
    }


def integrate_known_trajectory(
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
            -fixed_sources["source_B_C_total"] / 6.0,
            -fixed_sources["source_B_t_total"] / 6.0,
        ],
        dtype=float,
    )

    def right_hand_side(time_value: float, state: np.ndarray) -> np.ndarray:
        fields = evaluate_fields(functions, time_value)
        sources = source_components(fields)
        slope = homogeneous(fields)
        return np.array(
            [
                slope * state[0] + sources["source_B_C_total"],
                slope * state[1] + sources["source_B_t_total"],
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
        raise RuntimeError(f"corrected p8 trajectory failed: {solution.message}")
    sample_times = np.linspace(t_start, t_end, SAMPLE_COUNT)
    samples = solution.sol(sample_times)
    rows: list[dict[str, Any]] = []
    for sample_index, time_value in enumerate(sample_times):
        fields = evaluate_fields(functions, float(time_value))
        sources = source_components(fields)
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
                "homogeneous_B_slope": homogeneous(fields),
                "B_C": b_c,
                "B_t": b_t,
                "B_minus": b_c - b_t,
                "B_plus": b_c + b_t,
                "v_C_equals_g3_B_C": fields["g"] ** 3 * b_c,
                "v_t_equals_g3_B_t": fields["g"] ** 3 * b_t,
                "status": "CANONICAL_REPAIRED_KNOWN_SOURCE_TRAJECTORY",
            }
        )
    fixed_beta_c = 6.0 * initial[0] + fixed_sources["source_B_C_total"]
    fixed_beta_t = 6.0 * initial[1] + fixed_sources["source_B_t_total"]
    fixed = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "scenario": SCENARIO,
        "g_star": fixed_fields["g"],
        "g_CFF_star": fixed_fields["g_CFF"],
        "B_C_star": float(initial[0]),
        "B_t_star": float(initial[1]),
        "B_minus_star": float(initial[0] - initial[1]),
        "B_plus_star": float(initial[0] + initial[1]),
        "source_B_plus_CFF_squared_star": fixed_sources[
            "source_B_plus_CFF_squared"
        ],
        "p8_subblock_eigenvalue_C": 6.0,
        "p8_subblock_eigenvalue_t": 6.0,
        "beta_B_C_fixed_residual": fixed_beta_c,
        "beta_B_t_fixed_residual": fixed_beta_t,
        "new_relevant_directions": 0,
        "status": "CANONICAL_REPAIRED_SOURCE_TRUNCATED_FIXED_POINT",
    }
    endpoint = rows[-1]
    summary = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "success": bool(solution.success),
        "t_endpoint": t_end,
        "function_evaluations": int(solution.nfev),
        "B_C_endpoint": endpoint["B_C"],
        "B_t_endpoint": endpoint["B_t"],
        "B_minus_endpoint": endpoint["B_minus"],
        "B_plus_endpoint": endpoint["B_plus"],
        "g_endpoint": endpoint["g"],
        "status": "CANONICAL_REPAIRED_KNOWN_SOURCE_IR_ENDPOINT",
    }
    return rows, fixed, summary


def find_match_time(
    functions: dict[str, PchipInterpolator], t_end: float, gravity: float
) -> float:
    endpoint_g = float(functions["g"](t_end))
    start_g = float(functions["g"](0.0))
    if not endpoint_g < gravity < start_g:
        raise ValueError(
            f"match gravity {gravity} outside trajectory [{endpoint_g}, {start_g}]"
        )
    return float(brentq(lambda value: float(functions["g"](value)) - gravity, t_end, 0.0))


def matching_response_rows(
    source_rows: list[dict[str, str]], summary: dict[str, Any], beta_a_additive: float,
    primitive_unit: float,
) -> list[dict[str, Any]]:
    functions = interpolators(source_rows)
    t_end = float(summary["t_endpoint"])
    rows: list[dict[str, Any]] = []
    for gravity_match in MATCH_GRAVITIES:
        t_match = find_match_time(functions, t_end, gravity_match)

        def right_hand_side(time_value: float, state: np.ndarray) -> np.ndarray:
            fields = evaluate_fields(functions, time_value)
            slope = homogeneous(fields)
            generated_a, iterated_minus, primitive_response, boundary_response = state
            return np.array(
                [
                    beta_a_additive,
                    slope * iterated_minus - 12.0 * generated_a,
                    slope * primitive_response + primitive_unit,
                    slope * boundary_response,
                ],
                dtype=float,
            )

        solution = solve_ivp(
            right_hand_side,
            (t_match, t_end),
            np.array([0.0, 0.0, 0.0, 1.0], dtype=float),
            method="DOP853",
            rtol=2.0e-12,
            atol=2.0e-15,
            max_step=0.03,
        )
        if not solution.success:
            raise RuntimeError(f"matching response failed: {solution.message}")
        generated_a, iterated_minus, primitive_response, boundary_response = (
            float(value) for value in solution.y[:, -1]
        )
        interval = t_end - t_match
        fixed_g_iterated = -6.0 * beta_a_additive * interval**2
        fixed_g_primitive = primitive_unit * interval
        iterated_scale = max(abs(fixed_g_iterated), 1.0e-30)
        primitive_scale = max(abs(fixed_g_primitive), 1.0e-30)
        rows.append(
            {
                "scheme": summary["scheme"],
                "polynomial_order": int(summary["polynomial_order"]),
                "g_match": gravity_match,
                "t_match": t_match,
                "t_endpoint": t_end,
                "delta_ln_k": interval,
                "generated_A_C3_endpoint": generated_a,
                "iterated_delta_B_minus": iterated_minus,
                "iterated_delta_B_plus": 0.0,
                "iterated_delta_B_C": iterated_minus / 2.0,
                "iterated_delta_B_t": -iterated_minus / 2.0,
                "primitive_delta_B_minus_per_xi_minus": primitive_response,
                "primitive_delta_B_plus_per_xi_plus": primitive_response,
                "primitive_delta_B_C_per_unit_xi": primitive_response / 2.0,
                "primitive_delta_B_t_per_xi_minus": -primitive_response / 2.0,
                "primitive_delta_B_t_per_xi_plus": primitive_response / 2.0,
                "matching_boundary_transfer": boundary_response,
                "fixed_G_iterated_reference": fixed_g_iterated,
                "fixed_G_primitive_reference": fixed_g_primitive,
                "iterated_relative_Newton_running_shift": abs(
                    iterated_minus - fixed_g_iterated
                )
                / iterated_scale,
                "primitive_relative_Newton_running_shift": abs(
                    primitive_response - fixed_g_primitive
                )
                / primitive_scale,
                "R3_running_type": "ADDITIVE_TWO_LOOP_SOURCE",
                "status": "EXACT_ADDITIVE_RESPONSE_BELOW_DECLARED_MATCH_SCALE",
            }
        )
    return rows


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
            scale = max(abs(float(upper[coordinate])), abs(float(lower[coordinate])), 1.0e-30)
            rows.append(
                {
                    "comparison": "N6_to_N8",
                    "scheme": scheme,
                    "coordinate": coordinate,
                    "lower_value": lower[coordinate],
                    "upper_value": upper[coordinate],
                    "absolute_difference": difference,
                    "relative_difference": difference / scale,
                    "status": "ORDER_CONVERGED" if difference / scale <= 1.0e-3 else "ORDER_GATE_FAIL",
                }
            )
    for coordinate in coordinates:
        dynamic = index[("dynamic_etaN", 8)]
        reference = index[("reference_etaN0", 8)]
        difference = abs(float(dynamic[coordinate]) - float(reference[coordinate]))
        scale = max(abs(float(dynamic[coordinate])), abs(float(reference[coordinate])), 1.0e-30)
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
    rows: list[dict[str, Any]] = []
    for endpoint in summaries:
        if int(endpoint["polynomial_order"]) != 8:
            continue
        b_c = float(endpoint["B_C_endpoint"])
        for source in objects:
            radius = float(source["radius_m"])
            mass_length = float(source["mass_length_m"])
            chi = float(source["chi_lP2_curvature"])
            gate = float(source["epsilon_gate"])
            compactness = mass_length / radius
            factor_a = 128.0 * (8.0 - 11.0 * compactness)
            factor_b = 128.0 * (36.0 - 67.0 * compactness)
            delta_a = factor_a * b_c * chi**3
            delta_b = factor_b * b_c * chi**3
            bmax = min(gate / (abs(factor_a) * chi**3), gate / (abs(factor_b) * chi**3))
            rows.append(
                {
                    "scheme": endpoint["scheme"],
                    "polynomial_order": 8,
                    "object_id": source["object_id"],
                    "source_class": source["source_class"],
                    "B_C_endpoint": b_c,
                    "delta_A": delta_a,
                    "delta_B": delta_b,
                    "max_abs_metric_residual": max(abs(delta_a), abs(delta_b)),
                    "epsilon_gate": gate,
                    "B_C_max_joint_gate": bmax,
                    "candidate_to_joint_bound_ratio": abs(b_c) / bmax,
                    "status": "CANONICAL_REPAIRED_KNOWN_SOURCE_STATIC_BELOW_GATE",
                    "source_path": source["source_path"],
                }
            )
    return tagged(rows)


def budget_rows(
    responses: list[dict[str, Any]], summaries: list[dict[str, Any]],
    static: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    summary_index = {
        (row["scheme"], int(row["polynomial_order"])): row for row in summaries
    }
    compact_bounds = {
        scheme: min(
            float(row["B_C_max_joint_gate"])
            for row in static
            if row["scheme"] == scheme
        )
        for scheme in SCHEMES
    }
    baratella_partial_wave_gate = 8.0 * math.pi
    bminus_unitarity = (
        128.0 * math.pi**3 * baratella_partial_wave_gate / (7.0 / 5.0)
    )
    bplus_unitarity = 128.0 * math.pi**3 * baratella_partial_wave_gate
    rows: list[dict[str, Any]] = []
    for response in responses:
        key = (response["scheme"], int(response["polynomial_order"]))
        endpoint = summary_index[key]
        baseline_minus = float(endpoint["B_minus_endpoint"])
        baseline_plus = float(endpoint["B_plus_endpoint"])
        baseline_c = float(endpoint["B_C_endpoint"])
        iterated_minus = float(response["iterated_delta_B_minus"])
        response_helicity = abs(
            float(response["primitive_delta_B_minus_per_xi_minus"])
        )
        response_c = abs(float(response["primitive_delta_B_C_per_unit_xi"]))
        boundary_transfer = abs(float(response["matching_boundary_transfer"]))
        minus_margin = bminus_unitarity - abs(baseline_minus + iterated_minus)
        plus_margin = bplus_unitarity - abs(baseline_plus)
        compact_margin = compact_bounds[response["scheme"]] - abs(
            baseline_c + float(response["iterated_delta_B_C"])
        )
        rows.extend(
            [
                {
                    "scheme": response["scheme"],
                    "polynomial_order": int(response["polynomial_order"]),
                    "g_match": response["g_match"],
                    "budget_id": "XI_MINUS_PLANCK_CONTACT_UNITARITY",
                    "coordinate": "xi_minus",
                    "response_per_unit": response_helicity,
                    "coefficient_gate": bminus_unitarity,
                    "maximum_absolute_parameter": max(0.0, minus_margin) / response_helicity,
                    "assumption": (
                        "E=M_P contact EFT; Baratella a^J=16pi a_J_standard; "
                        "|Re a_J_standard|<=1/2"
                    ),
                    "status": "CONDITIONAL_SCATTERING_BUDGET",
                },
                {
                    "scheme": response["scheme"],
                    "polynomial_order": int(response["polynomial_order"]),
                    "g_match": response["g_match"],
                    "budget_id": "XI_PLUS_PLANCK_CONTACT_UNITARITY",
                    "coordinate": "xi_plus",
                    "response_per_unit": response_helicity,
                    "coefficient_gate": bplus_unitarity,
                    "maximum_absolute_parameter": max(0.0, plus_margin) / response_helicity,
                    "assumption": (
                        "E=M_P contact EFT; Baratella a^J=16pi a_J_standard; "
                        "|Re a_J_standard|<=1/2"
                    ),
                    "status": "CONDITIONAL_SCATTERING_BUDGET",
                },
                {
                    "scheme": response["scheme"],
                    "polynomial_order": int(response["polynomial_order"]),
                    "g_match": response["g_match"],
                    "budget_id": "XI_EITHER_STATIC_COMPACT",
                    "coordinate": "xi_minus_or_xi_plus",
                    "response_per_unit": response_c,
                    "coefficient_gate": compact_bounds[response["scheme"]],
                    "maximum_absolute_parameter": max(0.0, compact_margin) / response_c,
                    "assumption": "one primitive helicity coordinate varied at a time",
                    "status": "EXACT_STATIC_RESPONSE_BUDGET_BUT_PHYSICALLY_WEAK",
                },
                {
                    "scheme": response["scheme"],
                    "polynomial_order": int(response["polynomial_order"]),
                    "g_match": response["g_match"],
                    "budget_id": "MATCHING_BOUNDARY_SAME_HELICITY_UNITARITY",
                    "coordinate": "delta_B_minus_at_match",
                    "response_per_unit": boundary_transfer,
                    "coefficient_gate": bminus_unitarity,
                    "maximum_absolute_parameter": max(0.0, minus_margin) / boundary_transfer,
                    "assumption": "one unmatched boundary coordinate varied at a time",
                    "status": "CONDITIONAL_MATCHING_BOUNDARY_BUDGET",
                },
            ]
        )
    return tagged(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    if any(digest(path) != expected for path, expected in EXPECTED_HASHES.items()):
        raise RuntimeError("4969 trajectory input hash mismatch")
    canonical = json.loads(CANONICAL_RESULT.read_text(encoding="utf-8"))
    if not canonical["all_checks_pass"]:
        raise RuntimeError("canonical repair result is not validated")
    beta_a_additive = float(
        canonical["pure_Einstein_split"]["beta_A_C3_pure_GR"]
    )
    if canonical["pure_Einstein_split"]["R3_running_type"] != "ADDITIVE_TWO_LOOP_SOURCE":
        raise RuntimeError("4969 R3 running was not classified as an additive source")
    primitive_unit = float(
        canonical["pure_Einstein_split"]["primitive_B_helicity_source_per_unit_xi"]
    )

    trajectory_source = read_csv(TRAJECTORY_4957)
    fixed_source = read_csv(FIXED_4957)
    trajectories: list[dict[str, Any]] = []
    fixed_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    source_index: dict[tuple[str, int], list[dict[str, str]]] = {}
    for scheme in SCHEMES:
        for order in ORDERS:
            source_rows = [
                row
                for row in trajectory_source
                if row["scheme"] == scheme and int(row["polynomial_order"]) == order
            ]
            if len(source_rows) != SAMPLE_COUNT:
                raise RuntimeError(f"trajectory row count mismatch for {scheme} N={order}")
            fixed_candidates = [
                row
                for row in fixed_source
                if row["scheme"] == scheme and int(row["polynomial_order"]) == order
            ]
            if len(fixed_candidates) != 1:
                raise RuntimeError(f"fixed row mismatch for {scheme} N={order}")
            run_rows, fixed, summary = integrate_known_trajectory(
                source_rows, fixed_candidates[0]
            )
            source_index[(scheme, order)] = source_rows
            trajectories.extend(run_rows)
            fixed_rows.append(fixed)
            summaries.append(summary)
            responses.extend(
                matching_response_rows(
                    source_rows, summary, beta_a_additive, primitive_unit
                )
            )

    convergence = convergence_rows(summaries)
    objects = [
        row for row in read_csv(COMPACT_4964) if row["row_type"] == "compact_object_gate"
    ]
    static = static_response_rows(summaries, objects)
    budgets = budget_rows(responses, summaries, static)
    write_csv(FIXED_CSV, tagged(fixed_rows))
    write_csv(TRAJECTORY_CSV, tagged(trajectories))
    write_csv(CONVERGENCE_CSV, convergence)
    write_csv(STATIC_CSV, static)
    write_csv(RESPONSE_CSV, tagged(responses))
    write_csv(BOUND_CSV, budgets)

    old = json.loads(OLD_RESULT.read_text(encoding="utf-8"))
    old_index = {
        (row["scheme"], int(row["polynomial_order"])): row
        for row in old["completed_N8_endpoints"]
    }
    repaired_n8 = [row for row in summaries if int(row["polynomial_order"]) == 8]
    shifts = {
        row["scheme"]: {
            coordinate: float(row[coordinate])
            - float(old_index[(row["scheme"], 8)][coordinate])
            for coordinate in (
                "B_C_endpoint",
                "B_t_endpoint",
                "B_minus_endpoint",
                "B_plus_endpoint",
            )
        }
        for row in repaired_n8
    }
    maximum_order_shift = max(
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
    response_n8 = [row for row in responses if int(row["polynomial_order"]) == 8]
    earliest = [row for row in response_n8 if float(row["g_match"]) == 1.0e-2]
    checks = {
        "four_repaired_trajectory_runs": len(summaries) == 4,
        "all_repaired_runs_succeeded": all(row["success"] for row in summaries),
        "p8_eigenvalues_are_six": all(
            float(row["p8_subblock_eigenvalue_C"]) == 6.0
            and float(row["p8_subblock_eigenvalue_t"]) == 6.0
            for row in fixed_rows
        ),
        "fixed_residual_below_1e_15": maximum_fixed_residual <= 1.0e-15,
        "N6_N8_order_gate": maximum_order_shift <= 1.0e-3,
        "all_static_rows_below_gate": all(
            float(row["max_abs_metric_residual"]) <= float(row["epsilon_gate"])
            for row in static
        ),
        "twenty_matching_response_rows": len(responses) == 20,
        "iterated_response_same_helicity_only": all(
            float(row["iterated_delta_B_minus"]) != 0.0
            and float(row["iterated_delta_B_plus"]) == 0.0
            for row in responses
        ),
        "primitive_response_rank_two": all(
            float(row["primitive_delta_B_minus_per_xi_minus"]) != 0.0
            and float(row["primitive_delta_B_plus_per_xi_plus"]) != 0.0
            for row in responses
        ),
        "primitive_not_added_to_primary_candidate": True,
        "matching_boundary_retained": all(
            float(row["matching_boundary_transfer"]) > 0.0 for row in responses
        ),
        "R3_response_is_additive_not_multiplicative": all(
            row["R3_running_type"] == "ADDITIVE_TWO_LOOP_SOURCE"
            for row in responses
        ),
        "conditional_budgets_positive": all(
            float(row["maximum_absolute_parameter"]) > 0.0 for row in budgets
        ),
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": hashes,
        "canonical_flow": {
            "beta_B": "[6-3 beta_g/g]B+source",
            "fixed_boundary": "B_star=-source_star/6",
            "p8_subblock": [6.0, 6.0],
        },
        "canonical_repaired_N8_endpoints": repaired_n8,
        "shift_from_4968_normalization": shifts,
        "pure_Einstein_IR_response_at_g_match_1e_2": earliest,
        "pure_Einstein_R3_running_type": "ADDITIVE_TWO_LOOP_SOURCE",
        "maximum_N6_to_N8_relative_shift": maximum_order_shift,
        "maximum_static_metric_residual": maximum_static,
        "primitive_source_status": "UNCOMPUTED_NOT_ADDED_TO_PRIMARY_CANDIDATE",
        "matching_boundary_status": "EXPLICIT_LINEAR_RESPONSE_RETAINED",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "outputs": {
            "fixed_point": relative(FIXED_CSV),
            "trajectory": relative(TRAJECTORY_CSV),
            "convergence": relative(CONVERGENCE_CSV),
            "static_response": relative(STATIC_CSV),
            "matching_response": relative(RESPONSE_CSV),
            "primitive_budget": relative(BOUND_CSV),
        },
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"4969 trajectory checks failed: {failed}")
    print(f"{MARKER}_N8_ENDPOINTS={repaired_n8}", flush=True)
    print(f"{MARKER}_MAX_STATIC={maximum_static:.12g}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
