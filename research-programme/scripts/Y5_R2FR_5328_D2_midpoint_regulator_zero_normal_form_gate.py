from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5328"

SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
SCRIPT_5326 = SCRIPTS / "Y5_R2FR_5326_D2_midpoint_event_aligned_E0025_refinement.py"
SCRIPT_5237 = SCRIPTS / "Y5_R2FR_5237_bounded_multi_event_direct_A00_causal_runner.py"
RESULT_5327 = FUNCTIONAL_RG / "5327" / "D2_midpoint_regulator_ladder_controller_result.json"
VALIDATION_5327 = FUNCTIONAL_RG / "5327" / "D2_midpoint_regulator_ladder_controller_validation.csv"
LADDER_5327 = FUNCTIONAL_RG / "5327" / "D2_midpoint_finite_regulator_ladder.csv"
SCRIPT_5319 = SCRIPTS / "Y5_R2FR_5319_regulator_zero_asymptotic_gate.py"
NORMAL_FORMS_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_local_normal_form_contract.csv"

INPUT_AUDIT = SOURCE / "D2_midpoint_zero_fit_input_audit.csv"
EVENT_CERTIFICATE = SOURCE / "D2_midpoint_event_normal_form_certificate.csv"
NORMAL_FORM_CONTRACT = SOURCE / "D2_midpoint_regulator_zero_normal_form_contract.csv"
MODEL_FITS = SOURCE / "D2_midpoint_regulator_zero_model_fits.csv"
STABILITY = SOURCE / "D2_midpoint_regulator_zero_fit_stability.csv"
RICHARDSON = SOURCE / "D2_midpoint_regulator_zero_pairwise_richardson.csv"
SUMMARY = SOURCE / "D2_midpoint_regulator_zero_summary.csv"
RESULT = SOURCE / "D2_midpoint_regulator_zero_normal_form_result.json"
VALIDATION = SOURCE / "D2_midpoint_regulator_zero_normal_form_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5328_VALIDATION.csv"
DOCUMENT = POST / "5328-Y5-R2FR-D2-midpoint-regulator-zero-normal-form-gate.md"

CHECKPOINT = 5328
PARENT_CHECKPOINT = 5327
MARKER = "MTS_5328_D2_MIDPOINT_REGULATOR_ZERO_NORMAL_FORM_GATE"
REVISION = "D2-midpoint-regulator-zero-normal-form-gate-v1"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EXPECTED_IDS = (
    "E000625",
    "E00125",
    "E0025",
    "E005",
    "E010",
    "E020",
    "E040",
)
EPSILON_REFERENCE = 0.01
REFERENCE_MODEL_ID = "M3_TRANSVERSE_ENDPOINT_LOG"
ZERO_LIMIT_RELATIVE_BOUND_LIMIT = 1.0e-2
EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT = 2.0e-2
NORMALIZED_RESIDUAL_LIMIT = 1.0
CONDITION_TIMES_MACHINE_EPSILON_LIMIT = 1.0e-8
CONTACT_RESIDUAL_LIMIT = 1.0e-8
TRANSVERSE_SLOPE_FLOOR = 1.0e-3
BRANCH_SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT = 0.5
NEXT_EPSILON_ID = "E0003125"
CLAIM_FIELDS = (
    "valid_for_D2_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)

MODEL_SPECS = (
    {
        "model_id": "M1_ANALYTIC_LINEAR",
        "role": "ANALYTIC_LEADING_STRESS",
        "basis_terms": "1|epsilon",
        "derived_family": True,
        "leading_family": True,
    },
    {
        "model_id": "M2_ANALYTIC_QUADRATIC",
        "role": "ANALYTIC_CURVATURE_STRESS",
        "basis_terms": "1|epsilon|epsilon^2",
        "derived_family": True,
        "leading_family": True,
    },
    {
        "model_id": "M3_TRANSVERSE_ENDPOINT_LOG",
        "role": "DERIVED_REFERENCE_NORMAL_FORM",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)",
        "derived_family": True,
        "leading_family": True,
    },
    {
        "model_id": "M4_ENDPOINT_LOG_PLUS_E2",
        "role": "DERIVED_ANALYTIC_REMAINDER_STRESS",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2",
        "derived_family": True,
        "leading_family": False,
    },
    {
        "model_id": "M5_ENDPOINT_LOG_PLUS_E2LOG",
        "role": "DERIVED_LOGARITHMIC_REMAINDER_STRESS",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2*log(epsilon/epsilon_ref)",
        "derived_family": True,
        "leading_family": False,
    },
    {
        "model_id": "M6_FOLD_SQRT_STRESS",
        "role": "TOPOLOGY_EXCLUDED_HALF_POWER_FALSIFIER",
        "basis_terms": "1|sqrt(epsilon)|epsilon",
        "derived_family": False,
        "leading_family": False,
    },
    {
        "model_id": "M7_FOLD_SQRT_LOG_STRESS",
        "role": "TOPOLOGY_EXCLUDED_HALF_POWER_LOG_FALSIFIER",
        "basis_terms": "1|sqrt(epsilon)|epsilon|epsilon*log(epsilon/epsilon_ref)",
        "derived_family": False,
        "leading_family": False,
    },
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5327 = load_module("mts_5327_for_5328", SCRIPT_5327)
M5283 = M5327.M5283


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
    kernel32.SetPriorityClass.restype = ctypes.c_int
    process = kernel32.GetCurrentProcess()
    if not kernel32.SetPriorityClass(process, 0x00004000):
        raise ctypes.WinError()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    leading = list(leading_fields or [])
    remaining = sorted(
        {key for row in rows for key in row}
        - set(leading)
    )
    fields = leading + remaining
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": passed, "detail": detail}


def regulator_paths(epsilon_id: str) -> tuple[Path, Path]:
    if epsilon_id == "E0025":
        directory = FUNCTIONAL_RG / "5326"
        return (
            directory / "D2_midpoint_refined_support_events.csv",
            directory / "D2_midpoint_support_event_state_scan.csv",
        )
    directory = FUNCTIONAL_RG / "5327" / epsilon_id
    return (
        directory / "refined_support_events.csv",
        directory / "support_event_state_scan.csv",
    )


def input_arrays() -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, np.ndarray]:
    source_rows = sorted(read_csv(LADDER_5327), key=lambda row: float(row["epsilon"]))
    audited: list[dict[str, Any]] = []
    epsilon_values: list[float] = []
    integral_values: list[complex] = []
    disk_bounds: list[float] = []
    for row in source_rows:
        epsilon = float(row["epsilon"])
        value = complex(
            float(row["fixed_decay_integral_real"]),
            float(row["fixed_decay_integral_imaginary"]),
        )
        disk_bound = float(row["fixed_decay_error_absolute_conservative"])
        source_path = Path(row["finite_source_path"])
        result_path = Path(row["result_source_path"])
        validation_path = Path(row["validation_source_path"])
        valid = (
            epsilon > 0.0
            and math.isfinite(epsilon)
            and math.isfinite(value.real)
            and math.isfinite(value.imag)
            and disk_bound > 0.0
            and math.isfinite(disk_bound)
            and parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
            and parse_bool(row["valid_for_D2_regulator_zero_fit_input"])
            and source_path.exists()
            and result_path.exists()
            and validation_path.exists()
        )
        audited.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": epsilon,
                **complex_fields("fixed_decay_integral", value),
                "absolute_complex_disk_bound": disk_bound,
                "finite_regulator_input_valid": valid,
                "finite_source_path": str(source_path),
                "result_source_path": str(result_path),
                "validation_source_path": str(validation_path),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        epsilon_values.append(epsilon)
        integral_values.append(value)
        disk_bounds.append(disk_bound)
    return (
        audited,
        np.asarray(epsilon_values, dtype=float),
        np.asarray(integral_values, dtype=np.complex128),
        np.asarray(disk_bounds, dtype=float),
    )


def through_origin_slope(points: list[tuple[float, float]]) -> float:
    denominator = sum(delta * delta for delta, _ in points)
    if denominator <= 0.0:
        return math.nan
    return sum(delta * margin for delta, margin in points) / denominator


def event_certificate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in EXPECTED_IDS:
        events_path, states_path = regulator_paths(epsilon_id)
        events = read_csv(events_path)
        states = read_csv(states_path)
        for event in events:
            event_type = event["event_type"]
            event_coordinate = float(event["event_coordinate"])
            pole_real = float(event["event_pole_real"])
            support_lower = float(event["event_support_lower"])
            support_upper = float(event["event_support_upper"])
            lower_contact = abs(pole_real - support_lower)
            upper_contact = abs(pole_real - support_upper)
            contact_residual = min(lower_contact, upper_contact)
            contact_boundary = "LOWER" if lower_contact <= upper_contact else "UPPER"
            broad_slope = math.nan
            near_slope = math.nan
            slope_relative_change = math.nan
            broad_count = 0
            near_count = 0
            opposite_side_absence_witness = False
            if event_type in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}:
                broad_slope = abs(float(event["source_crossing_slope"]))
                near_slope = broad_slope
                slope_relative_change = 0.0
                broad_count = 1
                near_count = 1
                opposite_side_absence_witness = True
                normal_form_class = "TWO_SIDED_TRANSVERSE_SUPPORT_CONTACT"
                passes = (
                    parse_bool(event["event_contract_passes"])
                    and contact_residual <= CONTACT_RESIDUAL_LIMIT
                    and broad_slope >= TRANSVERSE_SLOPE_FLOOR
                )
            elif event_type == "BRANCH_DEATH":
                matching_states = [
                    state
                    for state in states
                    if state["term_id"] == event["term_id"]
                    and state["primary_surface_id"] == event["primary_surface_id"]
                ]
                points: list[tuple[float, float]] = []
                for state in matching_states:
                    if not parse_bool(state["branch_exists"]):
                        continue
                    delta = abs(event_coordinate - float(state["absolute_soft_cosine"]))
                    margin_text = state["signed_support_margin"]
                    if not margin_text:
                        continue
                    margin = float(margin_text)
                    if 1.0e-6 <= delta <= 1.0e-3 and margin > 0.0:
                        points.append((delta, margin))
                near_points = [point for point in points if point[0] <= 1.0e-4]
                broad_count = len(points)
                near_count = len(near_points)
                broad_slope = through_origin_slope(points)
                near_slope = through_origin_slope(near_points)
                if math.isfinite(broad_slope) and math.isfinite(near_slope):
                    slope_relative_change = abs(broad_slope - near_slope) / max(
                        abs(broad_slope), abs(near_slope), 1.0e-300
                    )
                opposite_side_absence_witness = any(
                    not parse_bool(state["branch_exists"])
                    and abs(event_coordinate - float(state["absolute_soft_cosine"]))
                    <= 1.0e-3
                    for state in matching_states
                )
                normal_form_class = "ONE_SIDED_TRANSVERSE_SUPPORT_CONTACT"
                passes = (
                    parse_bool(event["event_contract_passes"])
                    and contact_residual <= CONTACT_RESIDUAL_LIMIT
                    and contact_boundary == "UPPER"
                    and broad_count >= 3
                    and near_count >= 2
                    and math.isfinite(broad_slope)
                    and math.isfinite(near_slope)
                    and broad_slope >= TRANSVERSE_SLOPE_FLOOR
                    and near_slope >= TRANSVERSE_SLOPE_FLOOR
                    and slope_relative_change
                    <= BRANCH_SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT
                    and opposite_side_absence_witness
                )
            else:
                normal_form_class = "UNCLASSIFIED_EVENT"
                passes = False
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "event_id": event["event_id"],
                    "event_type": event_type,
                    "term_id": event["term_id"],
                    "primary_surface_id": event["primary_surface_id"],
                    "event_coordinate": event_coordinate,
                    "contact_boundary": contact_boundary,
                    "contact_residual": contact_residual,
                    "broad_transverse_slope_magnitude": broad_slope,
                    "near_transverse_slope_magnitude": near_slope,
                    "slope_window_relative_change": slope_relative_change,
                    "broad_slope_point_count": broad_count,
                    "near_slope_point_count": near_count,
                    "opposite_side_branch_absence_witness": opposite_side_absence_witness,
                    "normal_form_class": normal_form_class,
                    "event_normal_form_contract_passes": passes,
                    "events_source_path": str(events_path),
                    "states_source_path": str(states_path),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def normal_form_rows(event_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    root_source = SCRIPT_5237.read_text(encoding="utf-8")
    simple_root_guard_present = (
        "if abs(derivative) < 1.0e-10:" in root_source
        and "pole = complex(center) - center_value / derivative" in root_source
    )
    topology_passes = (
        bool(event_rows)
        and all(bool(row["event_normal_form_contract_passes"]) for row in event_rows)
        and simple_root_guard_present
    )
    common = {
        "event_certificate_row_count": len(event_rows),
        "event_topology_contract_passes": topology_passes,
        "parent_simple_root_guard_present": simple_root_guard_present,
        "event_certificate_source_path": str(EVENT_CERTIFICATE),
        **{field: False for field in CLAIM_FIELDS},
    }
    return [
        {
            "normal_form_id": "NF1_SIMPLE_POLE_IMPLICIT_FUNCTION",
            "hypotheses": "F(E,x,epsilon)=0 smooth; partial_E F nonzero; material pole simple",
            "conclusion": "E_p(x,epsilon)=E_p(x,0)+i*a(x)*epsilon+O(epsilon^2)",
            "contract_passes": topology_passes,
            **common,
        },
        {
            "normal_form_id": "NF2_TRANSVERSE_SUPPORT_CONTACT",
            "hypotheses": "m(x)=E_boundary(x)-E_p(x,0); m(x0)=0; kappa=m'(x0) nonzero",
            "conclusion": "energy primitive contains A(x)*log(kappa*(x-x0)+i*a*epsilon)+regular",
            "contract_passes": topology_passes,
            **common,
        },
        {
            "normal_form_id": "NF3_INTEGRATED_REGULATOR_ASYMPTOTIC",
            "hypotheses": "NF1 and NF2 with smooth compact local amplitude",
            "conclusion": "I(epsilon)=I0+c1*epsilon*log(epsilon/epsilon_ref)+c2*epsilon+O(epsilon^2*log(epsilon))",
            "contract_passes": topology_passes,
            **common,
        },
        {
            "normal_form_id": "NF4_NO_FOLD_HALF_POWER",
            "hypotheses": "all apparent branch deaths are certified upper-support contacts with nonzero one-sided slope",
            "conclusion": "sqrt(epsilon) is excluded from the derived family; retained only as an adversarial fit diagnostic",
            "contract_passes": topology_passes,
            **common,
        },
    ]


def design_matrix(model_id: str, epsilon: np.ndarray) -> np.ndarray:
    ones = np.ones(len(epsilon), dtype=float)
    logarithm = np.log(epsilon / EPSILON_REFERENCE)
    if model_id == "M1_ANALYTIC_LINEAR":
        columns = (ones, epsilon)
    elif model_id == "M2_ANALYTIC_QUADRATIC":
        columns = (ones, epsilon, epsilon**2)
    elif model_id == "M3_TRANSVERSE_ENDPOINT_LOG":
        columns = (ones, epsilon, epsilon * logarithm)
    elif model_id == "M4_ENDPOINT_LOG_PLUS_E2":
        columns = (ones, epsilon, epsilon * logarithm, epsilon**2)
    elif model_id == "M5_ENDPOINT_LOG_PLUS_E2LOG":
        columns = (ones, epsilon, epsilon * logarithm, epsilon**2 * logarithm)
    elif model_id == "M6_FOLD_SQRT_STRESS":
        columns = (ones, np.sqrt(epsilon), epsilon)
    elif model_id == "M7_FOLD_SQRT_LOG_STRESS":
        columns = (ones, np.sqrt(epsilon), epsilon, epsilon * logarithm)
    else:
        raise KeyError(model_id)
    return np.column_stack(columns)


def solve_weighted(
    matrix: np.ndarray,
    values: np.ndarray,
    bounds: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int, float, np.ndarray]:
    weighted_matrix = matrix / bounds[:, None]
    weighted_values = values / bounds
    coefficients, _, rank, _ = np.linalg.lstsq(
        weighted_matrix, weighted_values, rcond=None
    )
    prediction = matrix @ coefficients
    gram = matrix.T @ (matrix / bounds[:, None] ** 2)
    influence = np.linalg.solve(gram, matrix.T / bounds[None, :] ** 2)
    return (
        coefficients,
        prediction,
        int(rank),
        float(np.linalg.cond(weighted_matrix)),
        influence,
    )


def fit_model(
    specification: dict[str, Any],
    epsilon: np.ndarray,
    values: np.ndarray,
    bounds: np.ndarray,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    model_id = str(specification["model_id"])
    matrix = design_matrix(model_id, epsilon)
    coefficients, prediction, rank, condition, influence = solve_weighted(
        matrix, values, bounds
    )
    intercept = complex(coefficients[0])
    deterministic_bound = float(np.sum(np.abs(influence[0]) * bounds))
    normalized_residuals = np.abs(prediction - values) / bounds
    unweighted_intercept = complex(np.linalg.lstsq(matrix, values, rcond=None)[0][0])
    stability_rows: list[dict[str, Any]] = []
    leave_one_out_shifts: list[float] = []
    for omitted in range(len(epsilon)):
        selected = np.arange(len(epsilon)) != omitted
        reduced_matrix = design_matrix(model_id, epsilon[selected])
        if np.linalg.matrix_rank(reduced_matrix) < reduced_matrix.shape[1]:
            continue
        reduced_intercept = complex(
            solve_weighted(
                reduced_matrix, values[selected], bounds[selected]
            )[0][0]
        )
        shift = abs(reduced_intercept - intercept)
        leave_one_out_shifts.append(float(shift))
        stability_rows.append(
            {
                "model_id": model_id,
                "stability_test": "LEAVE_ONE_OUT",
                "omitted_epsilon_id": EXPECTED_IDS[omitted],
                "retained_point_count": int(np.sum(selected)),
                **complex_fields("intercept", reduced_intercept),
                "intercept_shift_from_full_fit": float(shift),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    window_shifts: list[float] = []
    for retained_count in range(matrix.shape[1] + 1, len(epsilon)):
        window_matrix = design_matrix(model_id, epsilon[:retained_count])
        window_intercept = complex(
            solve_weighted(
                window_matrix,
                values[:retained_count],
                bounds[:retained_count],
            )[0][0]
        )
        shift = abs(window_intercept - intercept)
        window_shifts.append(float(shift))
        stability_rows.append(
            {
                "model_id": model_id,
                "stability_test": "SMALLEST_EPSILON_WINDOW",
                "omitted_epsilon_id": "",
                "retained_point_count": retained_count,
                "maximum_retained_epsilon": float(epsilon[retained_count - 1]),
                **complex_fields("intercept", window_intercept),
                "intercept_shift_from_full_fit": float(shift),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    degrees_of_freedom = len(epsilon) - matrix.shape[1]
    condition_gate = (
        condition * np.finfo(float).eps
        <= CONDITION_TIMES_MACHINE_EPSILON_LIMIT
    )
    fit_gate = (
        rank == matrix.shape[1]
        and degrees_of_freedom >= 1
        and condition_gate
        and float(np.max(normalized_residuals)) <= NORMALIZED_RESIDUAL_LIMIT
        and len(leave_one_out_shifts) == len(epsilon)
        and all(math.isfinite(value) for value in leave_one_out_shifts)
        and math.isfinite(deterministic_bound)
    )
    row = {
        **specification,
        "point_count": len(epsilon),
        "parameter_count": matrix.shape[1],
        "degrees_of_freedom": degrees_of_freedom,
        "matrix_rank": rank,
        "weighted_condition_number": condition,
        "condition_times_machine_epsilon": condition * np.finfo(float).eps,
        "condition_gate_passes": condition_gate,
        **complex_fields("weighted_zero_intercept", intercept),
        **complex_fields("unweighted_zero_intercept", unweighted_intercept),
        "weighting_choice_intercept_shift": abs(unweighted_intercept - intercept),
        "deterministic_input_disk_intercept_bound": deterministic_bound,
        "maximum_normalized_complex_residual": float(np.max(normalized_residuals)),
        "rms_normalized_complex_residual": float(
            np.sqrt(np.mean(normalized_residuals**2))
        ),
        "maximum_leave_one_out_intercept_shift": max(leave_one_out_shifts),
        "maximum_small_epsilon_window_intercept_shift": max(
            window_shifts, default=0.0
        ),
        "model_fit_gate_passes": fit_gate,
        **{
            f"coefficient_{index}_real": float(complex(value).real)
            for index, value in enumerate(coefficients)
        },
        **{
            f"coefficient_{index}_imaginary": float(complex(value).imag)
            for index, value in enumerate(coefficients)
        },
        **{field: False for field in CLAIM_FIELDS},
    }
    return row, stability_rows


def richardson_rows(
    inputs: list[dict[str, Any]],
    epsilon: np.ndarray,
    values: np.ndarray,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(len(epsilon) - 1):
        lower_epsilon = float(epsilon[index])
        upper_epsilon = float(epsilon[index + 1])
        intercept = (
            upper_epsilon * values[index]
            - lower_epsilon * values[index + 1]
        ) / (upper_epsilon - lower_epsilon)
        rows.append(
            {
                "pair_id": f"R{index + 1}",
                "lower_epsilon_id": inputs[index]["epsilon_id"],
                "upper_epsilon_id": inputs[index + 1]["epsilon_id"],
                "lower_epsilon": lower_epsilon,
                "upper_epsilon": upper_epsilon,
                **complex_fields("linear_richardson_intercept", complex(intercept)),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5327,
        SCRIPT_5326,
        SCRIPT_5237,
        RESULT_5327,
        VALIDATION_5327,
        LADDER_5327,
        SCRIPT_5319,
        NORMAL_FORMS_5319,
        INPUT_AUDIT,
        EVENT_CERTIFICATE,
        NORMAL_FORM_CONTRACT,
    ]
    for epsilon_id in EXPECTED_IDS:
        paths.extend(regulator_paths(epsilon_id))
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5327)
    parent_validation = read_csv(VALIDATION_5327)
    inputs, epsilon, values, bounds = input_arrays()
    event_rows = event_certificate_rows()
    form_rows = normal_form_rows(event_rows)
    input_gate = (
        bool(parent["acceptance_passed"])
        and parent["decision"]
        == "D2_SEVEN_POINT_FINITE_REGULATOR_LADDER_COMPLETE__FIT_ZERO_LIMIT"
        and all(parse_bool(row["passed"]) for row in parent_validation)
        and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
        and len(inputs) == len(EXPECTED_IDS)
        and all(bool(row["finite_regulator_input_valid"]) for row in inputs)
        and np.all(np.diff(epsilon) > 0.0)
    )
    topology_gate = (
        len(event_rows) == 7 * len(EXPECTED_IDS)
        and all(bool(row["event_normal_form_contract_passes"]) for row in event_rows)
        and len(form_rows) == 4
        and all(bool(row["contract_passes"]) for row in form_rows)
    )
    if not input_gate:
        raise RuntimeError("D2 seven-point regulator-zero input gate failed")
    write_csv(INPUT_AUDIT, inputs, ["epsilon_id"])
    write_csv(EVENT_CERTIFICATE, event_rows, ["epsilon_id", "event_id"])
    write_csv(NORMAL_FORM_CONTRACT, form_rows, ["normal_form_id"])
    fit_rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    for specification in MODEL_SPECS:
        fit, stability = fit_model(specification, epsilon, values, bounds)
        fit_rows.append(fit)
        stability_rows.extend(stability)
    reference_row = next(
        row for row in fit_rows if row["model_id"] == REFERENCE_MODEL_ID
    )
    reference = complex(
        float(reference_row["weighted_zero_intercept_real"]),
        float(reference_row["weighted_zero_intercept_imaginary"]),
    )
    richardson = richardson_rows(inputs, epsilon, values)
    pairwise_shift = max(
        abs(
            complex(
                float(row["linear_richardson_intercept_real"]),
                float(row["linear_richardson_intercept_imaginary"]),
            )
            - reference
        )
        for row in richardson
    )
    for row in fit_rows:
        intercept = complex(
            float(row["weighted_zero_intercept_real"]),
            float(row["weighted_zero_intercept_imaginary"]),
        )
        family_shift = abs(intercept - reference)
        model_bound = (
            family_shift
            + float(row["deterministic_input_disk_intercept_bound"])
            + float(row["maximum_leave_one_out_intercept_shift"])
            + float(row["maximum_small_epsilon_window_intercept_shift"])
            + float(row["weighting_choice_intercept_shift"])
        )
        row["family_intercept_shift_from_reference"] = family_shift
        row["model_conservative_zero_bound"] = model_bound
        row["model_relative_zero_bound"] = model_bound / abs(reference)
    derived_rows = [row for row in fit_rows if bool(row["derived_family"])]
    leading_rows = [row for row in derived_rows if bool(row["leading_family"])]
    half_power_rows = [row for row in fit_rows if not bool(row["derived_family"])]
    leading_bound = (
        max(float(row["model_conservative_zero_bound"]) for row in leading_rows)
        + pairwise_shift
    )
    full_bound = (
        max(float(row["model_conservative_zero_bound"]) for row in derived_rows)
        + pairwise_shift
    )
    leading_relative = leading_bound / abs(reference)
    full_relative = full_bound / abs(reference)
    half_power_shift = max(
        float(row["family_intercept_shift_from_reference"])
        for row in half_power_rows
    )
    half_power_relative_shift = half_power_shift / abs(reference)
    derived_models_pass = all(
        bool(row["model_fit_gate_passes"]) for row in derived_rows
    )
    leading_gate = (
        topology_gate
        and derived_models_pass
        and leading_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    )
    remainder_gate = (
        topology_gate
        and derived_models_pass
        and full_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    )
    accepted = input_gate and leading_gate and remainder_gate
    next_epsilon = float(epsilon[0] / 2.0)
    if accepted:
        decision = "D2_MIDPOINT_REGULATOR_ZERO_ACCEPTED__BUILD_DECAY_ANGLE_QUADRATURE"
    elif not topology_gate:
        decision = "D2_ZERO_LIMIT_BLOCKED__DERIVE_NONTRANSVERSE_EVENT_NORMAL_FORM"
    elif leading_gate and full_relative <= EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT:
        decision = "D2_ZERO_LIMIT_STABLE__ADD_E0003125_TO_CLOSE_REMAINDER_ENVELOPE"
    else:
        decision = "D2_ZERO_LIMIT_UNRESOLVED__EXTEND_SMALL_EPSILON_LADDER"
    write_csv(MODEL_FITS, fit_rows, ["model_id"])
    write_csv(STABILITY, stability_rows, ["model_id", "stability_test"])
    write_csv(RICHARDSON, richardson, ["pair_id"])
    write_csv(
        SUMMARY,
        [
            {
                "summary_id": "D2_MIDPOINT_REGULATOR_ZERO",
                **complex_fields("reference_zero_limit", reference),
                "pairwise_richardson_maximum_shift": pairwise_shift,
                "leading_family_absolute_bound": leading_bound,
                "leading_family_relative_bound": leading_relative,
                "complete_remainder_absolute_bound": full_bound,
                "complete_remainder_relative_bound": full_relative,
                "topology_excluded_half_power_intercept_shift": half_power_shift,
                "topology_excluded_half_power_relative_shift": half_power_relative_shift,
                "relative_acceptance_limit": ZERO_LIMIT_RELATIVE_BOUND_LIMIT,
                "event_topology_gate_passes": topology_gate,
                "leading_family_gate_passes": leading_gate,
                "complete_remainder_gate_passes": remainder_gate,
                "D2_regulator_zero_limit_accepted": accepted,
                "required_next_epsilon": "" if accepted else next_epsilon,
                "decision": decision,
                "valid_for_D2_regulator_zero_limit": accepted,
                **{field: False for field in CLAIM_FIELDS[1:]},
            }
        ],
        ["summary_id"],
    )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D2-midpoint-regulator-zero-normal-form-gate",
        "acceptance_passed": accepted,
        "checkpoint_execution_passed": True,
        "decision": decision,
        "input_regulator_count": len(inputs),
        "event_certificate_row_count": len(event_rows),
        "event_topology_gate_passes": topology_gate,
        "fitted_model_count": len(fit_rows),
        "derived_model_fit_gates_pass": derived_models_pass,
        **complex_fields("reference_zero_limit", reference),
        "pairwise_richardson_maximum_shift": pairwise_shift,
        "leading_family_absolute_bound": leading_bound,
        "leading_family_relative_bound": leading_relative,
        "complete_remainder_absolute_bound": full_bound,
        "complete_remainder_relative_bound": full_relative,
        "topology_excluded_half_power_intercept_shift": half_power_shift,
        "topology_excluded_half_power_relative_shift": half_power_relative_shift,
        "relative_acceptance_limit": ZERO_LIMIT_RELATIVE_BOUND_LIMIT,
        "leading_family_gate_passes": leading_gate,
        "complete_remainder_gate_passes": remainder_gate,
        "required_next_regulator_epsilon": None if accepted else next_epsilon,
        "required_next_regulator_id": None if accepted else NEXT_EPSILON_ID,
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == FORMAL_DIGEST else -1
        ),
        "claim_boundary": {
            "valid_for_D2_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS[1:]},
            "reason": (
                "Only the fixed D2_MID regulator-zero envelope is tested. "
                "Decay-angle, full angular, phase-space, UV, local-GR, and "
                "full-MTS claims remain separate."
            ),
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    return result


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    lines = [
        "# 5328 - D2 midpoint regulator-zero normal-form gate",
        "",
        "## Local derivation",
        "",
        "The three events previously labelled `BRANCH_DEATH` are not admitted as",
        "unexplained fold singularities. Across all seven regulators, each pole reaches",
        "the fixed upper energy support with a nonzero one-sided margin slope before",
        "the scan branch disappears. The parent root finder also rejects zero channel",
        "derivative roots. Together with the validated simple-pole fits, the",
        "implicit-function theorem gives a smooth regulated pole trajectory.",
        "",
        "Writing `m(x)=E_upper-E_p(x,0)=kappa(x0-x)+...`, `kappa != 0`, the energy",
        "primitive has local form `A log(m+i a epsilon)+regular`. Its outer integral",
        "obeys `integral_0^L log(kappa y+i a epsilon)dy = [(kappa y+i a epsilon)",
        "(log(kappa y+i a epsilon)-1)]_0^L/kappa`. The lower endpoint is therefore",
        "proportional to `epsilon log epsilon`; the upper endpoint is analytic. The",
        "complete local integral has `epsilon log epsilon`, `epsilon`, and quadratic-logarithmic",
        "remainders. A `sqrt(epsilon)` fold term is not part of the derived family; it",
        "is nevertheless fitted as an adversarial sensitivity diagnostic.",
        "",
        "## Result",
        "",
        f"- reference zero intercept: `{result['reference_zero_limit_real']:.12g}` "
        f"`{result['reference_zero_limit_imaginary']:+.12g} i`;",
        f"- leading-family relative bound: `{result['leading_family_relative_bound']:.12g}`;",
        f"- complete-remainder relative bound: `{result['complete_remainder_relative_bound']:.12g}`;",
        "- excluded half-power diagnostic relative shift: "
        f"`{result['topology_excluded_half_power_relative_shift']:.12g}`;",
        f"- event topology gate: `{result['event_topology_gate_passes']}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if validation_passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "Acceptance applies only to the fixed `D2_MID` decay-angle node. It does not",
        "establish the decay-angle integral, full phase space, UV coefficient, local",
        "GR, or the full MTS framework.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    inputs = read_csv(INPUT_AUDIT)
    events = read_csv(EVENT_CERTIFICATE)
    forms = read_csv(NORMAL_FORM_CONTRACT)
    models = read_csv(MODEL_FITS)
    stability = read_csv(STABILITY)
    richardson = read_csv(RICHARDSON)
    summary = read_csv(SUMMARY)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    derived_models = [row for row in models if parse_bool(row["derived_family"])]
    decision_consistent = bool(result["acceptance_passed"]) == (
        bool(result["event_topology_gate_passes"])
        and bool(result["leading_family_gate_passes"])
        and bool(result["complete_remainder_gate_passes"])
    )
    nonclaim_consistent = bool(result["acceptance_passed"]) or (
        result["required_next_regulator_id"] == NEXT_EPSILON_ID
        and not any(bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS)
    )
    gates = [
        validation_gate(
            "seven_valid_finite_regulator_inputs",
            len(inputs) == len(EXPECTED_IDS)
            and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
            and all(parse_bool(row["finite_regulator_input_valid"]) for row in inputs),
            f"rows={len(inputs)}",
        ),
        validation_gate(
            "all_regulator_event_contacts_are_transverse",
            len(events) == 7 * len(EXPECTED_IDS)
            and all(parse_bool(row["event_normal_form_contract_passes"]) for row in events),
            f"rows={len(events)}",
        ),
        validation_gate(
            "implicit_function_and_integrated_normal_forms_close",
            len(forms) == 4
            and all(parse_bool(row["contract_passes"]) for row in forms),
            f"rows={len(forms)}",
        ),
        validation_gate(
            "complete_derived_model_family_resolved",
            len(derived_models) == 5
            and all(parse_bool(row["model_fit_gate_passes"]) for row in derived_models),
            f"derived_models={len(derived_models)}",
        ),
        validation_gate(
            "half_power_falsifiers_retained_as_diagnostics",
            len(models) == len(MODEL_SPECS)
            and sum(not parse_bool(row["derived_family"]) for row in models) == 2,
            f"models={len(models)}",
        ),
        validation_gate(
            "stability_tree_and_richardson_pairs_complete",
            bool(stability)
            and {row["model_id"] for row in stability}
            == {str(row["model_id"]) for row in MODEL_SPECS}
            and len(richardson) == len(EXPECTED_IDS) - 1,
            f"stability={len(stability)}; richardson={len(richardson)}",
        ),
        validation_gate(
            "decision_matches_topology_and_remainder_envelope",
            decision_consistent and len(summary) == 1,
            result["decision"],
        ),
        validation_gate(
            "unclosed_result_is_nonclaim_and_actionable",
            nonclaim_consistent,
            str(result["required_next_regulator_id"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            source_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS[1:]),
            "decay-angle and broader claims remain false",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates, ["gate"])
    write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_D2_MIDPOINT_REGULATOR_ZERO_NORMAL_FORM_GATE"
            if passed
            else "D2_MIDPOINT_REGULATOR_ZERO_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    return parser.parse_args()


def main() -> int:
    set_below_normal_priority()
    arguments = parse_args()
    result = execute() if arguments.mode == "run" else validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result.get("checkpoint_execution_passed", result["acceptance_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
