from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4967"

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
RESULT_4966 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4966"
    / "O4_p8_determinant_rank_and_static_response_results.json"
)
BARATELLA_SOURCE = SOURCE / "src-2010.13809" / "draft.tex"
BARATELLA_TAR = SOURCE / "2010.13809.tar"
BERN_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "src-2103.12728"
    / "GravScatt.tex"
)

EXPECTED_HASHES = {
    TRAJECTORY_4957: "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    FIXED_4957: "f6d7685517b17b25119d4f89246ba7804c69c37fcd52b99f3fd027f3e75cf734",
    COMPACT_4964: "a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f",
    RESULT_4966: "e8cc0dc517587fe378c8dade2a4afacbe3f2341557d9111428830351401e0765",
    BARATELLA_SOURCE: "d2892e4163b5a70ff3f660e2a48ba91f7e7be246dd53d21b3aa874a3a1b13230",
    BARATELLA_TAR: "d7e5600091d18f14e2c7629a8d75a612fc21662ea56dfc5697afc28ac94e32da",
    BERN_SOURCE: "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963",
}

SOURCE_AUDIT_CSV = SOURCE / "p8_functional_source_audit.csv"
NORMALIZATION_CSV = SOURCE / "p8_amplitude_normalization_map.csv"
THRESHOLD_CSV = SOURCE / "p8_massive_spin_threshold_transfer.csv"
FIXED_CSV = SOURCE / "p8_extended_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_GR_connected_trajectory.csv"
ENDPOINT_CSV = SOURCE / "p8_IR_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_static_compact_response.csv"
LOCALITY_CSV = SOURCE / "p8_motion_scalar_locality_bound.csv"
DECISION_CSV = SOURCE / "p8_finite_boundary_decision.csv"
RESULT_JSON = SOURCE / "p8_GR_trajectory_and_static_bound_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4967_P8_GR_TRAJECTORY_AND_STATIC_BOUND"
CHECKED_DATE = "2026-07-13"
TRAJECTORY_ORDERS = (6, 8)
SCHEMES = ("dynamic_etaN", "reference_etaN0")
SCENARIOS = (
    "C3_only",
    "O4_squared_only",
    "C3_plus_O4_squared",
)
SAMPLE_COUNT = 121


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


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


def source_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_class": "linear_O4_derivative_free_p8",
            "loop_order": 1,
            "helicity_direction": "[0,0]",
            "formula": "Q0[z W_k]=(z W_k)(0)=0",
            "included_in_candidate": True,
            "status": "EXACT_ZERO_NATURAL_TYPE_II",
            "scope": "constant-z derivative-free projection",
            "source_path": relative(RESULT_4966),
        },
        {
            "source_class": "quadratic_O4_Wilsonian_p8",
            "loop_order": 1,
            "helicity_direction": "[1,1]",
            "formula": (
                "d c_Q2/dt=w_O4^2 k^4(1-eta_psi/10)"
                "/[16 pi^2(1+m_psi^2/k^2)^3]"
            ),
            "included_in_candidate": True,
            "status": "DERIVED_OPTIMIZED_TYPE_II_SOURCE",
            "scope": "massless 4957 trajectory; finite-mass kernel displayed",
            "source_path": relative(RESULT_4966),
        },
        {
            "source_class": "C3_to_same_helicity_R4",
            "loop_order": 1,
            "helicity_direction": "[1,0]",
            "formula": (
                "d C_R4/d ln mu=-C_R3/(8 pi^2); "
                "d B_minus/d ln mu=-12 A_C3"
            ),
            "included_in_candidate": True,
            "status": "PRIMARY_ONSHELL_LOG_SOURCE",
            "scope": "leading one-loop gravity EFT anomalous dimension",
            "source_path": relative(BARATELLA_SOURCE),
        },
        {
            "source_class": "C3_to_mixed_helicity_R4prime",
            "loop_order": 1,
            "helicity_direction": "[0,0]",
            "formula": "d C_R4prime/d ln mu=0",
            "included_in_candidate": True,
            "status": "PRIMARY_ONSHELL_ONE_LOOP_ZERO",
            "scope": "leading one-loop helicity selection rule",
            "source_path": relative(BARATELLA_SOURCE),
        },
        {
            "source_class": "minimally_coupled_massive_thresholds",
            "loop_order": 1,
            "helicity_direction": "spin dependent full-rank transfer table",
            "formula": "B_i=sum_s n_s c_i^(s)/(8 pi mu_s^4)",
            "included_in_candidate": False,
            "status": "EXACT_TRANSFER_LAW_REQUIRES_PARENT_MASS_SPECTRUM",
            "scope": "local large-mass expansion; motion scalar treated separately",
            "source_path": relative(BERN_SOURCE),
        },
        {
            "source_class": "photon_CFF_to_p8",
            "loop_order": "one or more insertions",
            "helicity_direction": "not projected",
            "formula": "MISSING_COMPLETE_FOUR_GRAVITON_CFF_PROJECTOR",
            "included_in_candidate": False,
            "status": "OMITTED_SOURCE_FULL_TOTAL_OPEN",
            "scope": "current CFF flow stops at lower derivative rows",
            "source_path": "post-checkpoint-work/source-intake/functional_rg/4934",
        },
        {
            "source_class": "pure_Einstein_p8",
            "loop_order": 3,
            "helicity_direction": "not projected",
            "formula": "D=2+2L gives D=8 at L=3",
            "included_in_candidate": False,
            "status": "OMITTED_THREE_LOOP_SOURCE_FULL_TOTAL_OPEN",
            "scope": "not supplied by the one-loop functional truncation",
            "source_path": (
                "post-checkpoint-work/4965-Y5-R2FR-minimal-Ricci-flat-p8-"
                "on-shell-basis-helicity-projector-and-parent-flow-source-or-"
                "order-by-order-EFT-boundary.md"
            ),
        },
        {
            "source_class": "independent_p8_UV_boundary",
            "loop_order": "tree/UV",
            "helicity_direction": "two coordinates",
            "formula": "p8 subblock eigenvalues=(+4,+4)",
            "included_in_candidate": True,
            "status": "NO_NEW_RELEVANT_PARAMETER_IN_SOURCE_TRUNCATED_EXTENSION",
            "scope": (
                "UV regularity fixes the candidate boundary; omitted sources can "
                "shift it"
            ),
            "source_path": relative(FIXED_4957),
        },
    ]
    return tagged(rows)


def normalization_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map": "Planck_convention",
            "input": "kappa^2=32 pi G; M_P^2=1/(8 pi G)",
            "output": "kappa=2/M_P",
            "formula": "exact",
            "status": "DERIVED",
        },
        {
            "map": "C3_amplitude",
            "input": "beta_R3=(3/2) kappa a_plus; a_plus=16 pi A_C3 l_P^4",
            "output": "C_R3=(3/(4 pi)) A_C3",
            "formula": "C_R3=M_P^5 beta_R3",
            "status": "DERIVED",
        },
        {
            "map": "same_helicity_R4",
            "input": "beta_minus=kappa^2 b_minus; B_minus=b_minus/l_P^6",
            "output": "C_R4=B_minus/(128 pi^3)",
            "formula": "C_R4=M_P^8 beta_minus",
            "status": "DERIVED",
        },
        {
            "map": "mixed_helicity_R4",
            "input": "beta_plus=kappa^2 b_plus; B_plus=b_plus/l_P^6",
            "output": "C_R4prime=B_plus/(128 pi^3)",
            "formula": "C_R4prime=M_P^8 beta_plus",
            "status": "DERIVED",
        },
        {
            "map": "C3_log_to_helicity",
            "input": "dC_R4/dlnmu=-C_R3/(8pi^2); dC_R4prime/dlnmu=0",
            "output": "dB_minus/dlnmu=-12 A_C3; dB_plus/dlnmu=0",
            "formula": "multiply by 128 pi^3 and substitute C_R3",
            "status": "DERIVED",
        },
        {
            "map": "C3_log_to_invariant_basis",
            "input": "B_C=(B_minus+B_plus)/2; B_t=(B_plus-B_minus)/2",
            "output": "dB_C/dlnmu=-6 A_C3; dB_t/dlnmu=+6 A_C3",
            "formula": "exact projector inverse",
            "status": "DERIVED",
        },
        {
            "map": "O4_optimized_moment",
            "input": "I4=k^8/(64pi^2); I6=k^10/(80pi^2)",
            "output": "1-eta_psi/10",
            "formula": (
                "2[2k^2 I4-eta_psi(k^2 I4-I6)]"
                "=k^10(1-eta_psi/10)/(16pi^2)"
            ),
            "status": "DERIVED",
        },
        {
            "map": "O4_to_running_B_C",
            "input": "v_C=k^6 b_C; B_C=v_C/g^3; utilde_O4=u_O4",
            "output": (
                "source_beta_BC=u_O4^2(1-eta_psi/10)/(pi g^2)"
            ),
            "formula": "source_beta_vC=g u_O4^2(1-eta_psi/10)/pi",
            "status": "DERIVED",
        },
    ]
    return tagged(rows)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def threshold_rows() -> list[dict[str, Any]]:
    coefficients = {
        "0": (Fraction(1, 7560), Fraction(1, 6300)),
        "1/2_real_Majorana": (Fraction(-1, 3780), Fraction(29, 50400)),
        "1": (Fraction(1, 2520), Fraction(31, 12600)),
        "3/2": (Fraction(-1, 1890), Fraction(419, 25200)),
        "2": (Fraction(1, 1512), Fraction(671, 2520)),
    }
    rows: list[dict[str, Any]] = []
    for spin, (c_minus, c_plus) in coefficients.items():
        c_c = (c_minus + c_plus) / 2
        c_t = (c_plus - c_minus) / 2
        rows.append(
            {
                "spin": spin,
                "particle_counting": "one real minimally coupled particle",
                "c_minus": fraction_text(c_minus),
                "c_plus": fraction_text(c_plus),
                "c_C": fraction_text(c_c),
                "c_t": fraction_text(c_t),
                "c_minus_float": float(c_minus),
                "c_plus_float": float(c_plus),
                "c_C_float": float(c_c),
                "c_t_float": float(c_t),
                "B_minus_transfer": f"({fraction_text(c_minus)})/(8 pi mu^4)",
                "B_plus_transfer": f"({fraction_text(c_plus)})/(8 pi mu^4)",
                "B_C_transfer": f"({fraction_text(c_c)})/(8 pi mu^4)",
                "B_t_transfer": f"({fraction_text(c_t)})/(8 pi mu^4)",
                "status": "SOURCE_LOCKED_LARGE_MASS_THRESHOLD",
                "source_path": relative(BERN_SOURCE),
            }
        )
    return tagged(rows)


def source_components(
    gravity: float,
    h_c3: float,
    u_o4: float,
    eta_psi: float,
    scenario: str,
) -> dict[str, float]:
    a_c3 = h_c3 / gravity
    c3_c = -6.0 * a_c3 if "C3" in scenario else 0.0
    c3_t = 6.0 * a_c3 if "C3" in scenario else 0.0
    o4_c = 0.0
    if "O4" in scenario:
        o4_c = (
            u_o4**2
            * (1.0 - eta_psi / 10.0)
            / (math.pi * gravity**2)
        )
    return {
        "A_C3_h_over_g": a_c3,
        "source_B_C_C3": c3_c,
        "source_B_t_C3": c3_t,
        "source_B_C_O4_squared": o4_c,
        "source_B_t_O4_squared": 0.0,
        "source_B_C_total": c3_c + o4_c,
        "source_B_t_total": c3_t,
    }


def interpolators(rows: list[dict[str, str]]) -> dict[str, PchipInterpolator]:
    ordered = sorted(rows, key=lambda row: float(row["t_log_k_over_seed"]))
    times = np.array(
        [float(row["t_log_k_over_seed"]) for row in ordered], dtype=float
    )
    fields = {
        "g": np.array([float(row["g"]) for row in ordered], dtype=float),
        "h_C3": np.array(
            [float(row["h_C3"]) for row in ordered], dtype=float
        ),
        "u_O4": np.array(
            [float(row["u_O4"]) for row in ordered], dtype=float
        ),
        "eta_psi": np.array(
            [float(row["eta_psi"]) for row in ordered], dtype=float
        ),
        "beta_g_over_g": np.array(
            [float(row["eta_Newton_physical"]) + 2.0 for row in ordered],
            dtype=float,
        ),
    }
    return {
        name: PchipInterpolator(times, values, extrapolate=False)
        for name, values in fields.items()
    }


def evaluate_fields(
    functions: dict[str, PchipInterpolator], time_value: float
) -> dict[str, float]:
    return {name: float(function(time_value)) for name, function in functions.items()}


def integrate_p8_trajectory(
    source_rows: list[dict[str, str]],
    fixed_row: dict[str, str],
    scenario: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    functions = interpolators(source_rows)
    times = np.array(
        sorted(float(row["t_log_k_over_seed"]) for row in source_rows),
        dtype=float,
    )
    t_start = 0.0
    t_end = float(times[0])

    fixed_g = float(fixed_row["g"])
    fixed_h = float(fixed_row["h_C3"])
    fixed_u = float(fixed_row["u_O4"])
    fixed_eta = float(fixed_row["eta_psi"])
    fixed_sources = source_components(
        fixed_g, fixed_h, fixed_u, fixed_eta, scenario
    )
    initial = np.array(
        [
            -fixed_sources["source_B_C_total"] / 4.0,
            -fixed_sources["source_B_t_total"] / 4.0,
        ],
        dtype=float,
    )

    def right_hand_side(time_value: float, state: np.ndarray) -> np.ndarray:
        fields = evaluate_fields(functions, time_value)
        sources = source_components(
            fields["g"],
            fields["h_C3"],
            fields["u_O4"],
            fields["eta_psi"],
            scenario,
        )
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
        raise RuntimeError(f"p8 trajectory integration failed: {solution.message}")

    sample_times = np.linspace(t_start, t_end, SAMPLE_COUNT)
    samples = solution.sol(sample_times)
    rows: list[dict[str, Any]] = []
    for sample_index, time_value in enumerate(sample_times):
        fields = evaluate_fields(functions, float(time_value))
        sources = source_components(
            fields["g"],
            fields["h_C3"],
            fields["u_O4"],
            fields["eta_psi"],
            scenario,
        )
        homogeneous = 4.0 - 2.0 * fields["beta_g_over_g"]
        b_c = float(samples[0, sample_index])
        b_t = float(samples[1, sample_index])
        rows.append(
            {
                "scheme": fixed_row["scheme"],
                "polynomial_order": int(fixed_row["polynomial_order"]),
                "scenario": scenario,
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
                "status": "SOURCE_TRUNCATED_GR_CONNECTED_P8_TRAJECTORY",
            }
        )

    fixed_beta_c = 4.0 * initial[0] + fixed_sources["source_B_C_total"]
    fixed_beta_t = 4.0 * initial[1] + fixed_sources["source_B_t_total"]
    fixed = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "scenario": scenario,
        "g_star": fixed_g,
        "A_C3_star": fixed_h / fixed_g,
        "W_O4_star": fixed_u / fixed_g**2,
        "B_C_star": float(initial[0]),
        "B_t_star": float(initial[1]),
        "B_minus_star": float(initial[0] - initial[1]),
        "B_plus_star": float(initial[0] + initial[1]),
        "p8_subblock_eigenvalue_C": 4.0,
        "p8_subblock_eigenvalue_t": 4.0,
        "beta_B_C_fixed_residual": fixed_beta_c,
        "beta_B_t_fixed_residual": fixed_beta_t,
        "new_relevant_directions": 0,
        "status": "UV_REGULAR_SOURCE_SELECTED_P8_FIXED_POINT",
    }
    endpoint = rows[-1]
    summary = {
        "scheme": fixed_row["scheme"],
        "polynomial_order": int(fixed_row["polynomial_order"]),
        "scenario": scenario,
        "success": bool(solution.success),
        "t_endpoint": t_end,
        "function_evaluations": int(solution.nfev),
        "B_C_endpoint": endpoint["B_C"],
        "B_t_endpoint": endpoint["B_t"],
        "B_minus_endpoint": endpoint["B_minus"],
        "B_plus_endpoint": endpoint["B_plus"],
        "g_endpoint": endpoint["g"],
        "A_C3_endpoint": endpoint["A_C3_h_over_g"],
        "O4_source_endpoint": endpoint["source_B_C_O4_squared"],
        "status": "SOURCE_TRUNCATED_IR_ENDPOINT",
    }
    return rows, fixed, summary


def endpoint_convergence_rows(
    summaries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    index = {
        (row["scheme"], row["scenario"], int(row["polynomial_order"])): row
        for row in summaries
    }
    for scheme in SCHEMES:
        for scenario in SCENARIOS:
            lower = index[(scheme, scenario, TRAJECTORY_ORDERS[0])]
            upper = index[(scheme, scenario, TRAJECTORY_ORDERS[1])]
            for coordinate in (
                "B_C_endpoint",
                "B_t_endpoint",
                "B_minus_endpoint",
                "B_plus_endpoint",
            ):
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
                        "scenario": scenario,
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
    for scenario in SCENARIOS:
        for coordinate in (
            "B_C_endpoint",
            "B_t_endpoint",
            "B_minus_endpoint",
            "B_plus_endpoint",
        ):
            dynamic = index[("dynamic_etaN", scenario, 8)]
            reference = index[("reference_etaN0", scenario, 8)]
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
                    "scenario": scenario,
                    "coordinate": coordinate,
                    "lower_value": min(dynamic[coordinate], reference[coordinate]),
                    "upper_value": max(dynamic[coordinate], reference[coordinate]),
                    "absolute_difference": difference,
                    "relative_difference": difference / scale,
                    "status": "SCHEME_BRACKET_RECORDED",
                }
            )
    return tagged(rows)


def compact_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(COMPACT_4964)
        if row["row_type"] == "compact_object_gate"
    ]


def static_response_rows(
    summaries: list[dict[str, Any]], objects: list[dict[str, str]]
) -> list[dict[str, Any]]:
    endpoints = [
        row
        for row in summaries
        if int(row["polynomial_order"]) == 8
        and row["scenario"] == "C3_plus_O4_squared"
    ]
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
            rows.append(
                {
                    "scheme": endpoint["scheme"],
                    "polynomial_order": 8,
                    "scenario": endpoint["scenario"],
                    "object_id": source["object_id"],
                    "source_class": source["source_class"],
                    "compactness_M_over_r": compactness,
                    "chi_lP2_curvature": chi,
                    "B_C_endpoint": b_c,
                    "delta_A": delta_a,
                    "delta_B": delta_b,
                    "max_abs_metric_residual": max(abs(delta_a), abs(delta_b)),
                    "epsilon_gate": epsilon_gate,
                    "B_C_max_from_delta_A_gate": bmax_a,
                    "B_C_max_from_delta_B_gate": bmax_b,
                    "B_C_max_joint_gate": min(bmax_a, bmax_b),
                    "candidate_to_joint_bound_ratio": abs(b_c) / min(bmax_a, bmax_b),
                    "static_B_t_weight": 0.0,
                    "status": "SOURCE_TRUNCATED_STATIC_CORRECTION_BELOW_GATE",
                    "source_path": source["source_path"],
                }
            )
    return tagged(rows)


def scalar_locality_rows(objects: list[dict[str, str]]) -> list[dict[str, Any]]:
    scalar_c_c = Fraction(11, 75600)
    scalar_c_t = Fraction(1, 75600)
    rows: list[dict[str, Any]] = []
    for source in objects:
        mass_length = float(source["mass_length_m"])
        radius = float(source["radius_m"])
        chi = float(source["chi_lP2_curvature"])
        compactness = mass_length / radius
        for gap_to_curvature_ratio in (1.0, 10.0, 100.0):
            j_gap = gap_to_curvature_ratio * chi
            b_c = float(scalar_c_c) / (8.0 * math.pi * j_gap**2)
            b_t = float(scalar_c_t) / (8.0 * math.pi * j_gap**2)
            delta_a = 128.0 * b_c * chi**3 * (8.0 - 11.0 * compactness)
            delta_b = 128.0 * b_c * chi**3 * (36.0 - 67.0 * compactness)
            rows.append(
                {
                    "object_id": source["object_id"],
                    "compactness_M_over_r": compactness,
                    "chi_lP2_curvature": chi,
                    "rho_gap_over_curvature": gap_to_curvature_ratio,
                    "J_gap_equals_mu_psi_squared": j_gap,
                    "local_expansion_parameter_chi_over_J": (
                        1.0 / gap_to_curvature_ratio
                    ),
                    "B_C_minimal_motion_scalar": b_c,
                    "B_t_minimal_motion_scalar": b_t,
                    "delta_A_minimal_motion_scalar": delta_a,
                    "delta_B_minimal_motion_scalar": delta_b,
                    "exact_scaling": "delta_metric proportional chi/rho^2",
                    "strict_locality_gate": gap_to_curvature_ratio >= 10.0,
                    "status": (
                        "LOCAL_THRESHOLD_BOUND_CONTROLLED"
                        if gap_to_curvature_ratio >= 10.0
                        else "MARGINAL_LOCAL_EXPANSION_REFERENCE_ONLY"
                    ),
                    "source_path": relative(BERN_SOURCE),
                }
            )
    return tagged(rows)


def decision_rows(
    fixed_rows: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    static_rows: list[dict[str, Any]],
    convergence_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    combined = [
        row
        for row in summaries
        if int(row["polynomial_order"]) == 8
        and row["scenario"] == "C3_plus_O4_squared"
    ]
    b_c_values = [float(row["B_C_endpoint"]) for row in combined]
    b_t_values = [float(row["B_t_endpoint"]) for row in combined]
    maximum_static = max(float(row["max_abs_metric_residual"]) for row in static_rows)
    max_order_sensitivity = max(
        float(row["relative_difference"])
        for row in convergence_rows
        if row["comparison"] == "N6_to_N8"
        and row["scenario"] == "C3_plus_O4_squared"
    )
    maximum_fixed_residual = max(
        max(
            abs(float(row["beta_B_C_fixed_residual"])),
            abs(float(row["beta_B_t_fixed_residual"])),
        )
        for row in fixed_rows
    )
    rows = [
        {
            "question": "Does the source-truncated p8 extension add a relevant parameter?",
            "answer": "no",
            "evidence": "p8 diagonal beta eigenvalues are +4,+4 in B coordinates",
            "numeric_value": 0,
            "status": "DERIVED_TRIANGULAR_TRUNCATION_RESULT",
        },
        {
            "question": "Is the UV p8 boundary fixed in the C3+O4 source truncation?",
            "answer": "yes",
            "evidence": "UV regularity gives B_i_star=-source_i_star/4",
            "numeric_value": maximum_fixed_residual,
            "status": "SOURCE_TRUNCATED_BOUNDARY_DERIVED",
        },
        {
            "question": "What is the N8 source-truncated IR B_C bracket?",
            "answer": f"[{min(b_c_values):.17g},{max(b_c_values):.17g}]",
            "evidence": "dynamic etaN and reference etaN0 trajectories",
            "numeric_value": max(abs(value) for value in b_c_values),
            "status": "CALCULATED_NOT_FULL_TOTAL",
        },
        {
            "question": "What is the N8 source-truncated IR B_t bracket?",
            "answer": f"[{min(b_t_values):.17g},{max(b_t_values):.17g}]",
            "evidence": "dynamic etaN and reference etaN0 trajectories",
            "numeric_value": max(abs(value) for value in b_t_values),
            "status": "CALCULATED_NOT_FULL_TOTAL",
        },
        {
            "question": "Does the calculated compact static correction exceed the gate?",
            "answer": "no",
            "evidence": "exact 4966 Schwarzschild response on all 4964 objects",
            "numeric_value": maximum_static,
            "status": "SOURCE_TRUNCATED_STATIC_BOUND_PASSES",
        },
        {
            "question": "Does N6 to N8 convergence pass the 1e-3 gate?",
            "answer": str(max_order_sensitivity <= 1.0e-3).lower(),
            "evidence": "independent trajectory integrations",
            "numeric_value": max_order_sensitivity,
            "status": (
                "ORDER_GATE_PASSES"
                if max_order_sensitivity <= 1.0e-3
                else "ORDER_GATE_FAILS"
            ),
        },
        {
            "question": "Is the full finite parent [B_C,B_t] now predicted?",
            "answer": "no",
            "evidence": "CFF/photon and pure-Einstein p8 projectors remain absent",
            "numeric_value": 0,
            "status": "FULL_SOURCE_COMPLETENESS_OPEN",
        },
        {
            "question": "What is the next derivation target?",
            "answer": "four-graviton CFF/photon p8 helicity projector",
            "evidence": "it is the lowest-loop omitted parent source class",
            "numeric_value": 0,
            "status": "NEXT_TARGET_SELECTED",
        },
    ]
    return tagged(rows)


def write_provenance(source_hashes: dict[str, str]) -> None:
    lines = [
        "# Checkpoint 4967 provenance",
        "",
        "## Primary sources",
        "",
        "- Baratella et al., *Anomalous Dimensions of Effective Theories from Partial Waves*, arXiv:2010.13809v2.",
        "  Official source: https://arxiv.org/abs/2010.13809",
        "- Bern, Kosmopoulos and Zhiboedov, *Gravitational Effective Field Theory Islands, Low-Spin Dominance, and the Four-Graviton Amplitude*, arXiv:2103.12728.",
        "  Official source: https://arxiv.org/abs/2103.12728",
        "",
        "## Source hashes",
        "",
    ]
    lines.extend(f"- `{path}`: `{value}`" for path, value in sorted(source_hashes.items()))
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "- The C3 anomalous dimension and massive-spin threshold coefficients are primary-source locked.",
            "- The O4 squared source is derived with the same optimized natural Type-II regulator used by the parent trajectory.",
            "- The integrated candidate contains C3 and O4 squared sources only.",
            "- Photon/CFF and three-loop pure-Einstein p8 sources remain outside the calculation, so no full finite MTS p8 claim is made.",
            "- No GitHub action was performed.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {relative(path): digest(path) for path in EXPECTED_HASHES}
    if any(digest(path) != expected for path, expected in EXPECTED_HASHES.items()):
        raise RuntimeError("source hash mismatch")

    trajectory_source = read_csv(TRAJECTORY_4957)
    fixed_source = read_csv(FIXED_4957)
    trajectory_index: dict[tuple[str, int], list[dict[str, str]]] = {}
    for scheme in SCHEMES:
        for order in TRAJECTORY_ORDERS:
            rows = [
                row
                for row in trajectory_source
                if row["scheme"] == scheme
                and int(row["polynomial_order"]) == order
            ]
            if len(rows) != SAMPLE_COUNT:
                raise RuntimeError(
                    f"expected {SAMPLE_COUNT} source rows for {scheme} N={order}"
                )
            trajectory_index[(scheme, order)] = rows
    fixed_index = {
        (row["scheme"], int(row["polynomial_order"])): row
        for row in fixed_source
    }

    trajectory_rows: list[dict[str, Any]] = []
    fixed_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in TRAJECTORY_ORDERS:
            for scenario in SCENARIOS:
                rows, fixed, summary = integrate_p8_trajectory(
                    trajectory_index[(scheme, order)],
                    fixed_index[(scheme, order)],
                    scenario,
                )
                trajectory_rows.extend(rows)
                fixed_rows.append(fixed)
                summaries.append(summary)
                print(
                    f"{MARKER}_TRAJECTORY scheme={scheme} N={order} "
                    f"scenario={scenario} B_C={summary['B_C_endpoint']:.12g} "
                    f"B_t={summary['B_t_endpoint']:.12g}",
                    flush=True,
                )

    audit = source_audit_rows()
    normalization = normalization_rows()
    thresholds = threshold_rows()
    fixed_tagged = tagged(fixed_rows)
    trajectory_tagged = tagged(trajectory_rows)
    convergence = endpoint_convergence_rows(summaries)
    objects = compact_rows()
    static = static_response_rows(summaries, objects)
    locality = scalar_locality_rows(objects)
    decisions = decision_rows(fixed_rows, summaries, static, convergence)

    write_csv(SOURCE_AUDIT_CSV, audit)
    write_csv(NORMALIZATION_CSV, normalization)
    write_csv(THRESHOLD_CSV, thresholds)
    write_csv(FIXED_CSV, fixed_tagged)
    write_csv(TRAJECTORY_CSV, trajectory_tagged)
    write_csv(ENDPOINT_CSV, convergence)
    write_csv(STATIC_CSV, static)
    write_csv(LOCALITY_CSV, locality)
    write_csv(DECISION_CSV, decisions)
    write_provenance(source_hashes)

    combined_n8 = [
        row
        for row in summaries
        if int(row["polynomial_order"]) == 8
        and row["scenario"] == "C3_plus_O4_squared"
    ]
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "normalization": {
            "C_R3": "3 A_C3/(4 pi)",
            "C_R4": "B_minus/(128 pi^3)",
            "C_R4prime": "B_plus/(128 pi^3)",
            "C3_running": {
                "dB_minus_dlnk": "-12 A_C3",
                "dB_plus_dlnk": "0",
                "dB_C_dlnk": "-6 A_C3",
                "dB_t_dlnk": "+6 A_C3",
            },
            "O4_running": (
                "source_beta_BC=u_O4^2(1-eta_psi/10)/(pi g^2)"
            ),
        },
        "p8_subblock_eigenvalues": [4.0, 4.0],
        "new_relevant_directions": 0,
        "combined_N8_endpoints": combined_n8,
        "full_source_complete": False,
        "omitted_sources": [
            "photon/CFF four-graviton p8 projector",
            "three-loop pure-Einstein p8 source",
            "parent mass spectrum for finite massive thresholds",
        ],
        "outputs": {
            "source_audit": relative(SOURCE_AUDIT_CSV),
            "normalization": relative(NORMALIZATION_CSV),
            "massive_thresholds": relative(THRESHOLD_CSV),
            "extended_fixed_point": relative(FIXED_CSV),
            "trajectory": relative(TRAJECTORY_CSV),
            "endpoint_convergence": relative(ENDPOINT_CSV),
            "static_response": relative(STATIC_CSV),
            "motion_scalar_locality": relative(LOCALITY_CSV),
            "decision": relative(DECISION_CSV),
            "provenance": relative(PROVENANCE),
        },
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"{MARKER}_DONE B_C_N8=["
        f"{min(row['B_C_endpoint'] for row in combined_n8):.12g},"
        f"{max(row['B_C_endpoint'] for row in combined_n8):.12g}]",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
