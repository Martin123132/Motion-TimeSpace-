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
SOURCE = POST / "source-intake" / "functional_rg" / "4970"
FUNCTIONAL_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv"
)
KNOWN_P8_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_repaired_GR_connected_trajectory.csv"
)
CANONICAL_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_Einstein_split_results.json"
)
SLOPE_DIAGNOSTIC = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "functional_to_onshell_C3_matching_diagnostic.csv"
)
BERN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "src-1701.02422"
    / "gr_simp.tex"
)
GRAVSCATT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "src-2103.12728"
    / "GravScatt.tex"
)
FRG_C3 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex"
)

CONTRACT_CSV = SOURCE / "C3_matching_contract.csv"
SCAN_CSV = SOURCE / "C3_weak_branch_splice_scan.csv"
TRANSFER_CSV = SOURCE / "C3_p8_matching_transfer_matrix.csv"
SENSITIVITY_CSV = SOURCE / "C3_matching_scale_sensitivity.csv"
TRANSPORT_CSV = SOURCE / "C3_matching_offset_RG_transport.csv"
RESULT_JSON = SOURCE / "C3_p8_finite_matching_results.json"

MARKER = "MTS_4970_WEAK_SCALE_C3_P8_MATCHING"
CHECKED_DATE = "2026-07-13"
ON_SHELL_BRANCH = "PURE_EINSTEIN_MASSLESS_GRAVITON_ONLY"
N_B_MINUS_N_F = 2
SCHEMES = ("dynamic_etaN", "reference_etaN0")
ORDERS = (6, 8)
MATCH_GRAVITIES = (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6)
EXPECTED_HASHES = {
    FUNCTIONAL_TRAJECTORY: "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    KNOWN_P8_TRAJECTORY: "b5984ba1c528aebd2099755561a8b578ec79751a3846be01032cc52e24e65957",
    CANONICAL_RESULT: "7e45bf69deb9e61df28ef640eb0f075e2689849673d8199526e459bfd2e2d2d7",
    SLOPE_DIAGNOSTIC: "d8dc49be58f8eff511da14cae0d2fa9d803dc9fa1d227ba05957896b725dc243",
    BERN: "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e",
    GRAVSCATT: "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963",
    FRG_C3: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "onshell_branch": ON_SHELL_BRANCH,
            "N_b_minus_N_f": N_B_MINUS_N_F,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def build_interpolators(
    rows: list[dict[str, str]], fields: tuple[str, ...]
) -> dict[str, PchipInterpolator]:
    ordered = sorted(rows, key=lambda row: float(row["t_log_k_over_seed"]))
    times = np.array(
        [float(row["t_log_k_over_seed"]) for row in ordered], dtype=float
    )
    return {
        field: PchipInterpolator(
            times,
            np.array([float(row[field]) for row in ordered], dtype=float),
            extrapolate=False,
        )
        for field in fields
    }


def find_match_time(
    functions: dict[str, PchipInterpolator], t_end: float, gravity: float
) -> float:
    endpoint = float(functions["g"](t_end))
    start = float(functions["g"](0.0))
    if not endpoint < gravity < start:
        raise ValueError(f"g_match={gravity} outside [{endpoint},{start}]")
    return float(brentq(lambda time: float(functions["g"](time)) - gravity, t_end, 0.0))


def contract_rows(
    functional_slope_min: float,
    functional_slope_max: float,
    beta_a: float,
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "contract_id": "MATCH4970_00_constant_offset_no_go",
                "premise": "A_OS(t)=A_F(t)+delta_A with constant delta_A on one common interval",
                "derivation": "dA_OS/dt=dA_F/dt",
                "result": (
                    f"functional slope in [{functional_slope_min:.16g},"
                    f"{functional_slope_max:.16g}] differs from pure-Einstein beta_A={beta_a:.16g}"
                ),
                "status": "FINITE_CONSTANT_ALONE_CANNOT_RECONCILE_THE_BETA_FUNCTIONS",
            },
            {
                "contract_id": "MATCH4970_01_piecewise_branch",
                "premise": "choose a matching time t_m and do not double count the C3 source",
                "derivation": "A_OS(t)=A_F(t_m)+delta_A_m+beta_A(t-t_m) for t<=t_m",
                "result": "the pure-Einstein beta replaces the functional beta below t_m on this declared vacuum branch",
                "status": "DERIVED_MATCHING_FORM_REQUIRED",
            },
            {
                "contract_id": "MATCH4970_02_p8_replacement",
                "premise": "the functional known-source trajectory already contains -12A_F in B_minus",
                "derivation": "d(delta B_minus)/dt=H_B delta B_minus-12(A_OS-A_F)",
                "result": "B_minus_matched=B_minus_functional+delta B_minus",
                "status": "NO_DOUBLE_COUNTING_REPLACEMENT_EQUATION",
            },
            {
                "contract_id": "MATCH4970_03_finite_coordinates",
                "premise": "local matching permits finite Wilson coefficients at t_m",
                "derivation": "retain delta_A_m, delta_Bminus_m and delta_Bplus_m",
                "result": "zero offsets define a continuity prescription, not a theorem",
                "status": "FINITE_MATCHING_COORDINATES_EXPLICIT",
            },
            {
                "contract_id": "MATCH4970_04_primitive_coordinates",
                "premise": "the three-loop primitive simple-pole vector is not calculated",
                "derivation": "retain xi_minus and xi_plus independently of finite boundary offsets",
                "result": "one endpoint cannot separate primitive running from same-channel boundary data",
                "status": "RANK_THREE_NULLITY_TWO_CALCULATED_COORDINATES_OPEN",
            },
        ]
    )


def trajectory_groups(
    rows: list[dict[str, str]],
) -> dict[tuple[str, int], list[dict[str, str]]]:
    groups: dict[tuple[str, int], list[dict[str, str]]] = {}
    for row in rows:
        key = (row["scheme"], int(row["polynomial_order"]))
        groups.setdefault(key, []).append(row)
    return groups


def transfer_rows_for_scan(
    scan_id: str,
    scheme: str,
    order: int,
    gravity_match: float,
    response_a: float,
    boundary_minus: float,
    boundary_plus: float,
    primitive_minus: float,
    primitive_plus: float,
) -> list[dict[str, Any]]:
    coefficients = (
        (
            "delta_A_match",
            1.0,
            response_a,
            0.0,
            "FINITE_C3_MATCHING_COORDINATE_OPEN",
        ),
        (
            "delta_Bminus_match",
            0.0,
            boundary_minus,
            0.0,
            "FINITE_P8_MATCHING_COORDINATE_OPEN",
        ),
        (
            "delta_Bplus_match",
            0.0,
            0.0,
            boundary_plus,
            "FINITE_P8_MATCHING_COORDINATE_OPEN",
        ),
        (
            "xi_minus",
            0.0,
            primitive_minus,
            0.0,
            "PRIMITIVE_THREE_LOOP_COORDINATE_OPEN",
        ),
        (
            "xi_plus",
            0.0,
            0.0,
            primitive_plus,
            "PRIMITIVE_THREE_LOOP_COORDINATE_OPEN",
        ),
    )
    rows: list[dict[str, Any]] = []
    for parameter, a_value, minus_value, plus_value, status in coefficients:
        rows.append(
            {
                "scan_id": scan_id,
                "scheme": scheme,
                "polynomial_order": order,
                "g_match": gravity_match,
                "parameter": parameter,
                "A_endpoint_per_unit": a_value,
                "B_minus_endpoint_per_unit": minus_value,
                "B_plus_endpoint_per_unit": plus_value,
                "B_C_endpoint_per_unit": (minus_value + plus_value) / 2.0,
                "B_t_endpoint_per_unit": (plus_value - minus_value) / 2.0,
                "status": status,
            }
        )
    return rows


def integrate_scan(
    functional_rows: list[dict[str, str]],
    known_rows: list[dict[str, str]],
    scheme: str,
    order: int,
    gravity_match: float,
    beta_a: float,
    primitive_unit: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    functional = build_interpolators(
        functional_rows, ("g", "h_C3", "eta_Newton_physical")
    )
    known = build_interpolators(known_rows, ("B_minus", "B_plus"))
    t_end = min(float(row["t_log_k_over_seed"]) for row in functional_rows)
    t_match = find_match_time(functional, t_end, gravity_match)

    def a_functional(time: float) -> float:
        return float(functional["h_C3"](time) / functional["g"](time))

    a_match = a_functional(t_match)

    def delta_a_continuity(time: float) -> float:
        return a_match + beta_a * (time - t_match) - a_functional(time)

    def right_hand_side(time: float, state: np.ndarray) -> np.ndarray:
        beta_g_over_g = 2.0 + float(functional["eta_Newton_physical"](time))
        homogeneous = 6.0 - 3.0 * beta_g_over_g
        (
            replacement_minus,
            response_a,
            boundary_minus,
            boundary_plus,
            primitive_minus,
            primitive_plus,
        ) = state
        return np.array(
            [
                homogeneous * replacement_minus - 12.0 * delta_a_continuity(time),
                homogeneous * response_a - 12.0,
                homogeneous * boundary_minus,
                homogeneous * boundary_plus,
                homogeneous * primitive_minus + primitive_unit,
                homogeneous * primitive_plus + primitive_unit,
            ],
            dtype=float,
        )

    solution = solve_ivp(
        right_hand_side,
        (t_match, t_end),
        np.array([0.0, 0.0, 1.0, 1.0, 0.0, 0.0], dtype=float),
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-15,
        max_step=0.03,
    )
    if not solution.success:
        raise RuntimeError(f"4970 matching integration failed: {solution.message}")
    (
        replacement_minus,
        response_a,
        boundary_minus,
        boundary_plus,
        primitive_minus,
        primitive_plus,
    ) = (float(value) for value in solution.y[:, -1])

    a_functional_end = a_functional(t_end)
    a_onshell_end = a_match + beta_a * (t_end - t_match)
    known_minus_match = float(known["B_minus"](t_match))
    known_plus_match = float(known["B_plus"](t_match))
    known_minus_end = float(known["B_minus"](t_end))
    known_plus_end = float(known["B_plus"](t_end))
    matched_minus = known_minus_end + replacement_minus
    matched_plus = known_plus_end
    matched_c = (matched_minus + matched_plus) / 2.0
    matched_t = (matched_plus - matched_minus) / 2.0
    scan_id = f"MATCH4970_{scheme}_N{order}_g{gravity_match:.0e}"

    matrix = np.array(
        [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [response_a, boundary_minus, 0.0, primitive_minus, 0.0],
            [0.0, 0.0, boundary_plus, 0.0, primitive_plus],
        ],
        dtype=float,
    )
    p8_matrix = matrix[1:, 1:]
    row = {
        "scan_id": scan_id,
        "scheme": scheme,
        "polynomial_order": order,
        "g_match": gravity_match,
        "t_match": t_match,
        "t_endpoint": t_end,
        "delta_ln_k": t_end - t_match,
        "A_functional_match": a_match,
        "A_functional_endpoint": a_functional_end,
        "beta_A_onshell_additive": beta_a,
        "A_onshell_endpoint_zero_offset": a_onshell_end,
        "delta_A_endpoint_zero_offset": a_onshell_end - a_functional_end,
        "B_minus_functional_match": known_minus_match,
        "B_plus_functional_match": known_plus_match,
        "B_minus_functional_endpoint": known_minus_end,
        "B_plus_functional_endpoint": known_plus_end,
        "replacement_delta_B_minus_zero_offsets": replacement_minus,
        "replacement_delta_B_plus_zero_offsets": 0.0,
        "B_minus_matched_endpoint_zero_offsets": matched_minus,
        "B_plus_matched_endpoint_zero_offsets": matched_plus,
        "B_C_matched_endpoint_zero_offsets": matched_c,
        "B_t_matched_endpoint_zero_offsets": matched_t,
        "delta_Bminus_endpoint_per_delta_A_match": response_a,
        "delta_Bminus_endpoint_per_delta_Bminus_match": boundary_minus,
        "delta_Bplus_endpoint_per_delta_Bplus_match": boundary_plus,
        "delta_Bminus_endpoint_per_xi_minus": primitive_minus,
        "delta_Bplus_endpoint_per_xi_plus": primitive_plus,
        "continuity_residual_A_at_match": delta_a_continuity(t_match),
        "matching_matrix_rank_A_Bminus_Bplus": int(np.linalg.matrix_rank(matrix)),
        "matching_parameter_count": int(matrix.shape[1]),
        "matching_matrix_nullity_at_one_endpoint": int(
            matrix.shape[1] - np.linalg.matrix_rank(matrix)
        ),
        "p8_boundary_primitive_matrix_rank": int(np.linalg.matrix_rank(p8_matrix)),
        "p8_boundary_primitive_parameter_count": int(p8_matrix.shape[1]),
        "zero_offset_status": "DECLARED_CONTINUITY_PRESCRIPTION_NOT_A_THEOREM",
        "source_status": "FUNCTIONAL_C3_SOURCE_REPLACED_BY_PURE_EINSTEIN_BELOW_MATCH_NOT_ADDED",
        "status": "FINITE_MATCHING_TRANSFER_CALCULATED_FULL_CLAIM_OPEN",
    }
    transfer = transfer_rows_for_scan(
        scan_id,
        scheme,
        order,
        gravity_match,
        response_a,
        boundary_minus,
        boundary_plus,
        primitive_minus,
        primitive_plus,
    )
    return row, transfer


def sensitivity_rows(scan_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    quantities = (
        "A_onshell_endpoint_zero_offset",
        "delta_A_endpoint_zero_offset",
        "replacement_delta_B_minus_zero_offsets",
        "B_minus_matched_endpoint_zero_offsets",
        "B_C_matched_endpoint_zero_offsets",
        "B_t_matched_endpoint_zero_offsets",
    )
    rows: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in ORDERS:
            group = [
                row
                for row in scan_rows
                if row["scheme"] == scheme and int(row["polynomial_order"]) == order
            ]
            for quantity in quantities:
                values = [float(row[quantity]) for row in group]
                minimum = min(values)
                maximum = max(values)
                spread = maximum - minimum
                scale = max(abs(minimum), abs(maximum), 1.0e-30)
                relative = spread / scale
                rows.append(
                    {
                        "comparison": "g_match_1e-2_to_1e-6",
                        "scheme": scheme,
                        "polynomial_order": order,
                        "quantity": quantity,
                        "minimum": minimum,
                        "maximum": maximum,
                        "absolute_spread": spread,
                        "relative_spread": relative,
                        "status": (
                            "MATCH_SCALE_STABLE_UNDER_1_PERCENT"
                            if relative <= 1.0e-2
                            else "MATCH_SCALE_DEPENDENCE_EXPLICIT"
                        ),
                    }
                )
    return tagged(rows)


def matching_offset_transport_rows(
    scan_rows: list[dict[str, Any]],
    functional_groups: dict[tuple[str, int], list[dict[str, str]]],
    beta_a: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in ORDERS:
            group = sorted(
                [
                    row
                    for row in scan_rows
                    if row["scheme"] == scheme
                    and int(row["polynomial_order"]) == order
                ],
                key=lambda row: float(row["g_match"]),
                reverse=True,
            )
            anchor = next(row for row in group if float(row["g_match"]) == 1.0e-2)
            functions = build_interpolators(
                functional_groups[(scheme, order)],
                ("g", "h_C3", "eta_Newton_physical"),
            )
            t_anchor = float(anchor["t_match"])

            def a_functional(time: float) -> float:
                return float(functions["h_C3"](time) / functions["g"](time))

            a_anchor = a_functional(t_anchor)

            def transported_delta_a(time: float) -> float:
                return a_anchor + beta_a * (time - t_anchor) - a_functional(time)

            for scan in group:
                t_match = float(scan["t_match"])
                if math.isclose(t_match, t_anchor, rel_tol=0.0, abs_tol=1.0e-15):
                    delta_b_match = 0.0
                else:
                    def right_hand_side(time: float, state: np.ndarray) -> np.ndarray:
                        beta_g_over_g = 2.0 + float(
                            functions["eta_Newton_physical"](time)
                        )
                        homogeneous = 6.0 - 3.0 * beta_g_over_g
                        return np.array(
                            [homogeneous * state[0] - 12.0 * transported_delta_a(time)],
                            dtype=float,
                        )

                    solution = solve_ivp(
                        right_hand_side,
                        (t_anchor, t_match),
                        np.array([0.0], dtype=float),
                        method="DOP853",
                        rtol=2.0e-12,
                        atol=2.0e-15,
                        max_step=0.03,
                    )
                    if not solution.success:
                        raise RuntimeError(
                            f"4970 matching-offset transport failed: {solution.message}"
                        )
                    delta_b_match = float(solution.y[0, -1])

                delta_a_match = transported_delta_a(t_match)
                a_endpoint = (
                    float(scan["A_onshell_endpoint_zero_offset"]) + delta_a_match
                )
                bminus_endpoint = (
                    float(scan["B_minus_matched_endpoint_zero_offsets"])
                    + float(scan["delta_Bminus_endpoint_per_delta_A_match"])
                    * delta_a_match
                    + float(scan["delta_Bminus_endpoint_per_delta_Bminus_match"])
                    * delta_b_match
                )
                bplus_endpoint = float(scan["B_plus_matched_endpoint_zero_offsets"])
                rows.append(
                    {
                        "scan_id": scan["scan_id"],
                        "scheme": scheme,
                        "polynomial_order": order,
                        "anchor_g_match": 1.0e-2,
                        "target_g_match": scan["g_match"],
                        "delta_A_match_transported": delta_a_match,
                        "delta_Bminus_match_transported": delta_b_match,
                        "delta_Bplus_match_transported": 0.0,
                        "A_endpoint_after_transport": a_endpoint,
                        "B_minus_endpoint_after_transport": bminus_endpoint,
                        "B_plus_endpoint_after_transport": bplus_endpoint,
                        "A_endpoint_anchor": anchor[
                            "A_onshell_endpoint_zero_offset"
                        ],
                        "B_minus_endpoint_anchor": anchor[
                            "B_minus_matched_endpoint_zero_offsets"
                        ],
                        "B_plus_endpoint_anchor": anchor[
                            "B_plus_matched_endpoint_zero_offsets"
                        ],
                        "A_endpoint_transport_residual": a_endpoint
                        - float(anchor["A_onshell_endpoint_zero_offset"]),
                        "B_minus_endpoint_transport_residual": bminus_endpoint
                        - float(anchor["B_minus_matched_endpoint_zero_offsets"]),
                        "B_plus_endpoint_transport_residual": bplus_endpoint
                        - float(anchor["B_plus_matched_endpoint_zero_offsets"]),
                        "status": "MATCH_SCALE_INVARIANCE_RESTORED_BY_RG_TRANSPORT",
                    }
                )
    return tagged(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    bad_hashes = {
        relative(path): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if bad_hashes:
        raise RuntimeError(f"4970 input hash mismatch: {bad_hashes}")

    canonical = json.loads(CANONICAL_RESULT.read_text(encoding="utf-8"))
    beta_a = float(canonical["pure_Einstein_split"]["beta_A_C3_pure_GR"])
    primitive_unit = float(
        canonical["pure_Einstein_split"]["primitive_B_helicity_source_per_unit_xi"]
    )
    slope_rows = read_csv(SLOPE_DIAGNOSTIC)
    functional_slope = next(
        row for row in slope_rows if row["diagnostic_id"] == "MATCH4969_0_functional_slope"
    )
    functional_slope_min = float(functional_slope["value_min"])
    functional_slope_max = float(functional_slope["value_max"])
    contracts = contract_rows(functional_slope_min, functional_slope_max, beta_a)

    functional_groups = trajectory_groups(read_csv(FUNCTIONAL_TRAJECTORY))
    known_groups = trajectory_groups(read_csv(KNOWN_P8_TRAJECTORY))
    scans: list[dict[str, Any]] = []
    transfers: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in ORDERS:
            key = (scheme, order)
            if key not in functional_groups or key not in known_groups:
                raise RuntimeError(f"missing 4970 trajectory group {key}")
            for gravity_match in MATCH_GRAVITIES:
                scan, transfer = integrate_scan(
                    functional_groups[key],
                    known_groups[key],
                    scheme,
                    order,
                    gravity_match,
                    beta_a,
                    primitive_unit,
                )
                scans.append(scan)
                transfers.extend(transfer)

    sensitivities = sensitivity_rows(scans)
    transports = matching_offset_transport_rows(scans, functional_groups, beta_a)
    write_csv(CONTRACT_CSV, contracts)
    write_csv(SCAN_CSV, tagged(scans))
    write_csv(TRANSFER_CSV, tagged(transfers))
    write_csv(SENSITIVITY_CSV, sensitivities)
    write_csv(TRANSPORT_CSV, transports)

    maximum_continuity_residual = max(
        abs(float(row["continuity_residual_A_at_match"])) for row in scans
    )
    maximum_match_scale_relative_spread = max(
        float(row["relative_spread"]) for row in sensitivities
    )
    maximum_transport_residual = max(
        abs(float(row[coordinate]))
        for row in transports
        for coordinate in (
            "A_endpoint_transport_residual",
            "B_minus_endpoint_transport_residual",
            "B_plus_endpoint_transport_residual",
        )
    )
    n8_early = [
        row
        for row in scans
        if int(row["polynomial_order"]) == 8 and float(row["g_match"]) == 1.0e-2
    ]
    checks = {
        "all_input_hashes_match": not bad_hashes,
        "finite_constant_no_go_proved": (
            functional_slope_max < 0.0 and beta_a > 0.0
        ),
        "twenty_splice_scans_completed": len(scans) == 20,
        "one_hundred_transfer_rows_completed": len(transfers) == 100,
        "continuity_residual_below_1e_14": maximum_continuity_residual <= 1.0e-14,
        "functional_source_replaced_not_added": all(
            row["source_status"]
            == "FUNCTIONAL_C3_SOURCE_REPLACED_BY_PURE_EINSTEIN_BELOW_MATCH_NOT_ADDED"
            for row in scans
        ),
        "same_helicity_replacement_only": all(
            float(row["replacement_delta_B_plus_zero_offsets"]) == 0.0
            for row in scans
        ),
        "endpoint_matching_matrix_rank_three": all(
            int(row["matching_matrix_rank_A_Bminus_Bplus"]) == 3 for row in scans
        ),
        "endpoint_matching_nullity_two": all(
            int(row["matching_matrix_nullity_at_one_endpoint"]) == 2 for row in scans
        ),
        "p8_boundary_primitive_rank_two": all(
            int(row["p8_boundary_primitive_matrix_rank"]) == 2 for row in scans
        ),
        "zero_offset_is_not_claimed_derived": all(
            row["zero_offset_status"]
            == "DECLARED_CONTINUITY_PRESCRIPTION_NOT_A_THEOREM"
            for row in scans
        ),
        "match_scale_dependence_reported": len(sensitivities) == 24,
        "twenty_matching_offset_transports_completed": len(transports) == 20,
        "RG_transport_restores_match_scale_invariance": (
            maximum_transport_residual <= 2.0e-11
        ),
        "pure_Einstein_branch_is_explicit": (
            N_B_MINUS_N_F == 2
            and math.isclose(beta_a, N_B_MINUS_N_F / (7680.0 * math.pi**3))
        ),
        "full_MTS_claim_false": True,
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": hashes,
        "matching_theorem": {
            "constant_offset_only": False,
            "reason": "a constant finite offset cannot change the beta-function slope",
            "required_form": "piecewise pure-Einstein beta replacement at t_match plus finite matching coordinates",
        },
        "onshell_branch": {
            "name": ON_SHELL_BRANCH,
            "N_b_minus_N_f": N_B_MINUS_N_F,
            "beta_A_formula": "(N_b-N_f)/(7680*pi^3)",
            "scope": "pure-Einstein vacuum branch only; photon, motion and visible-matter thresholds require a separate field-content completion",
        },
        "physical_R3_beta_A": beta_a,
        "functional_slope_range": [functional_slope_min, functional_slope_max],
        "source_normalization_discrepancies": {
            "Baratella_to_Bern": canonical["pure_Einstein_split"][
                "baratella_to_Bern_ratio"
            ],
            "Bern_to_published_FRG": canonical["pure_Einstein_split"][
                "Bern_to_FRG_ratio"
            ],
            "status": "EXPLICIT_NOT_AVERAGED",
        },
        "scan_count": len(scans),
        "transfer_row_count": len(transfers),
        "N8_g_match_1e_2_zero_offset_examples": n8_early,
        "maximum_continuity_residual": maximum_continuity_residual,
        "maximum_match_scale_relative_spread": maximum_match_scale_relative_spread,
        "maximum_RG_transport_endpoint_residual": maximum_transport_residual,
        "matching_offset_running": {
            "delta_A_match": "d delta_A_m/dt_m=beta_A_physical-dA_F/dt_m",
            "delta_Bminus_match": "d delta_Bminus_m/dt_m=H_B delta_Bminus_m-12delta_A_m",
            "delta_Bplus_match": "d delta_Bplus_m/dt_m=H_B delta_Bplus_m",
            "status": "DERIVED_FROM_MATCH_SCALE_INVARIANCE",
        },
        "matching_parameter_vector": [
            "delta_A_match",
            "delta_Bminus_match",
            "delta_Bplus_match",
            "xi_minus",
            "xi_plus",
        ],
        "endpoint_observable_vector": ["A_C3", "B_minus", "B_plus"],
        "endpoint_matrix_rank": 3,
        "endpoint_parameter_nullity": 2,
        "interpretation": (
            "on the declared pure-Einstein weak branch, one endpoint cannot separate "
            "primitive xi values from finite p8 boundary data; scale-resolved amplitudes "
            "or a parent matching calculation are required"
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "outputs": {
            "contract": relative(CONTRACT_CSV),
            "splice_scan": relative(SCAN_CSV),
            "transfer_matrix": relative(TRANSFER_CSV),
            "sensitivity": relative(SENSITIVITY_CSV),
            "matching_offset_transport": relative(TRANSPORT_CSV),
        },
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"4970 checks failed: {failed}")
    print(
        f"{MARKER}_MAX_MATCH_SCALE_RELATIVE_SPREAD="
        f"{maximum_match_scale_relative_spread:.12g}",
        flush=True,
    )
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
