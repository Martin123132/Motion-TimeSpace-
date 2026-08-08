from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5319"

SCRIPT_5318 = SCRIPTS / "Y5_R2FR_5318_regulator_specific_squared_event_outer_repair.py"
RESULT_5318 = FUNCTIONAL_RG / "5318" / "regulator_specific_squared_event_outer_repair_result.json"
VALIDATION_5318 = FUNCTIONAL_RG / "5318" / "regulator_specific_squared_event_outer_repair_validation.csv"
LADDER_5318 = FUNCTIONAL_RG / "5318" / "five_regulator_fixed_decay_convergence.csv"
EVENTS_5318 = FUNCTIONAL_RG / "5318" / "regulator_specific_panel_nine_events.csv"
DOCUMENT_5315 = POST / "5315-Y5-R2FR-squared-event-coordinate-collar-repair.md"

DRY_RUN = SOURCE / "regulator_zero_asymptotic_gate_dry_run.json"
INPUT_AUDIT = SOURCE / "five_regulator_zero_fit_input_audit.csv"
NORMAL_FORMS = SOURCE / "regulator_zero_local_normal_form_contract.csv"
MODEL_FITS = SOURCE / "regulator_zero_model_fits.csv"
STABILITY = SOURCE / "regulator_zero_fit_stability.csv"
RICHARDSON = SOURCE / "regulator_zero_pairwise_richardson.csv"
SUMMARY = SOURCE / "regulator_zero_limit_summary.csv"
RESULT = SOURCE / "regulator_zero_asymptotic_gate_result.json"
VALIDATION = SOURCE / "regulator_zero_asymptotic_gate_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5319_VALIDATION.csv"
DOCUMENT = POST / "5319-Y5-R2FR-regulator-zero-asymptotic-gate.md"

CHECKPOINT = 5319
PARENT_CHECKPOINT = 5318
MARKER = "MTS_5319_REGULATOR_ZERO_ASYMPTOTIC_GATE"
REVISION = "regulator-zero-asymptotic-gate-v1"
EPSILON_REFERENCE = 0.01
NORMALIZED_RESIDUAL_LIMIT = 1.0
CONDITION_TIMES_MACHINE_EPSILON_LIMIT = 1.0e-8
ZERO_LIMIT_RELATIVE_BOUND_LIMIT = 1.0e-2
EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT = 2.0e-2
MINIMUM_TRANSVERSE_SLOPE = 1.0e-3
EXPECTED_IDS = ("E0025", "E005", "E010", "E020", "E040")
REFERENCE_MODEL_ID = "M1_ANALYTIC_LINEAR"
CLAIM_FIELDS = (
    "valid_for_fixed_decay_regulator_zero_limit",
    "valid_for_full_regulator_zero_limit",
    "valid_for_decay_angle_integration",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5318 = load_module("mts_5318_for_5319", SCRIPT_5318)
M5283 = M5318.M5283


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for field in leading_fields or []:
        if field not in fields:
            fields.append(field)
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": passed, "detail": detail}


MODEL_SPECS = (
    {
        "model_id": "M1_ANALYTIC_LINEAR",
        "role": "REFERENCE_LEADING",
        "basis_terms": "1|epsilon",
        "required_for_leading_gate": True,
        "required_for_remainder_gate": True,
    },
    {
        "model_id": "M2_ANALYTIC_QUADRATIC",
        "role": "ANALYTIC_CURVATURE_STRESS",
        "basis_terms": "1|epsilon|epsilon^2",
        "required_for_leading_gate": True,
        "required_for_remainder_gate": True,
    },
    {
        "model_id": "M3_TRANSVERSE_ENDPOINT_LOG",
        "role": "DERIVED_LEADING_ENDPOINT_NORMAL_FORM",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)",
        "required_for_leading_gate": True,
        "required_for_remainder_gate": True,
    },
    {
        "model_id": "M4_ENDPOINT_LOG_PLUS_E2",
        "role": "DERIVED_ANALYTIC_REMAINDER_STRESS",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2",
        "required_for_leading_gate": False,
        "required_for_remainder_gate": True,
    },
    {
        "model_id": "M5_ENDPOINT_LOG_PLUS_E2LOG",
        "role": "DERIVED_LOGARITHMIC_REMAINDER_STRESS",
        "basis_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2*log(epsilon/epsilon_ref)",
        "required_for_leading_gate": False,
        "required_for_remainder_gate": True,
    },
)


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
    else:
        raise KeyError(model_id)
    return np.column_stack(columns)


def input_arrays() -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, np.ndarray]:
    rows = sorted(read_csv(LADDER_5318), key=lambda row: float(row["epsilon"]))
    audited: list[dict[str, Any]] = []
    epsilon_values: list[float] = []
    integral_values: list[complex] = []
    disk_bounds: list[float] = []
    for row in rows:
        epsilon = float(row["epsilon"])
        value = complex(
            float(row["fixed_decay_integral_real"]),
            float(row["fixed_decay_integral_imaginary"]),
        )
        relative_bound = float(row["fixed_decay_error_relative_conservative"])
        disk_bound = relative_bound * abs(value)
        valid = (
            epsilon > 0.0
            and math.isfinite(epsilon)
            and math.isfinite(value.real)
            and math.isfinite(value.imag)
            and disk_bound > 0.0
            and math.isfinite(disk_bound)
            and parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
        )
        audited.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": epsilon,
                **complex_fields("fixed_decay_integral", value),
                "relative_conservative_bound": relative_bound,
                "absolute_complex_disk_bound": disk_bound,
                "finite_regulator_input_valid": valid,
                "source_path": str(LADDER_5318),
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


def normal_form_rows() -> list[dict[str, Any]]:
    event_rows = read_csv(EVENTS_5318)
    support_rows = [
        row
        for row in event_rows
        if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
    ]
    minimum_slope = min(float(row["crossing_slope_magnitude"]) for row in support_rows)
    parent_text = DOCUMENT_5315.read_text(encoding="utf-8")
    logarithmic_parent_signature = (
        "A log|x-x_event| + regular" in parent_text
        and "kappa != 0" in parent_text
        and minimum_slope >= MINIMUM_TRANSVERSE_SLOPE
        and all(parse_bool(row["event_contract_passes"]) for row in support_rows)
    )
    common = {
        "parent_logarithmic_signature_present": logarithmic_parent_signature,
        "minimum_observed_crossing_slope_magnitude": minimum_slope,
        "source_path": str(DOCUMENT_5315),
        **{field: False for field in CLAIM_FIELDS},
    }
    return [
        {
            "normal_form_id": "NF1_INTERIOR_SIMPLE_POLE",
            "local_form": "log(Delta+i*epsilon)+regular",
            "integrated_correction": "epsilon+O(epsilon^2)",
            "allowed_fit_terms": "1|epsilon|epsilon^2",
            "contract_passes": logarithmic_parent_signature,
            **common,
        },
        {
            "normal_form_id": "NF2_TRANSVERSE_SUPPORT_EVENT",
            "local_form": "log(kappa*(x-x_event)+i*epsilon)+regular; kappa!=0",
            "integrated_correction": "epsilon*log(epsilon/epsilon_ref)+epsilon+O(epsilon^2*log(epsilon))",
            "allowed_fit_terms": "1|epsilon|epsilon*log(epsilon/epsilon_ref)|epsilon^2|epsilon^2*log(epsilon/epsilon_ref)",
            "contract_passes": logarithmic_parent_signature,
            **common,
        },
        {
            "normal_form_id": "NF3_NO_HALF_POWER",
            "local_form": "transverse logarithmic crossing, not a degenerate algebraic branch",
            "integrated_correction": "no sqrt(epsilon) term admitted",
            "allowed_fit_terms": "exclude epsilon^(1/2)",
            "contract_passes": logarithmic_parent_signature,
            **common,
        },
    ]


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5318)
    parent_validation = read_csv(VALIDATION_5318)
    inputs, epsilon, _, bounds = input_arrays()
    forms = normal_form_rows()
    designs = []
    for specification in MODEL_SPECS:
        matrix = design_matrix(str(specification["model_id"]), epsilon)
        designs.append(
            {
                **specification,
                "point_count": len(epsilon),
                "parameter_count": matrix.shape[1],
                "degrees_of_freedom": len(epsilon) - matrix.shape[1],
                "matrix_rank": int(np.linalg.matrix_rank(matrix / bounds[:, None])),
                "weighted_condition_number": float(np.linalg.cond(matrix / bounds[:, None])),
            }
        )
    acceptance = (
        bool(parent["acceptance_passed"])
        and parent["decision"] == "FIVE_FINITE_REGULATORS_CONVERGED__FIT_REGULATOR_ZERO_LIMIT"
        and all(parse_bool(row["passed"]) for row in parent_validation)
        and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
        and len(inputs) == 5
        and all(bool(row["finite_regulator_input_valid"]) for row in inputs)
        and np.all(np.diff(epsilon) > 0.0)
        and all(bool(row["contract_passes"]) for row in forms)
        and all(
            int(row["matrix_rank"]) == int(row["parameter_count"])
            and int(row["degrees_of_freedom"]) >= 1
            for row in designs
        )
    )
    write_csv(INPUT_AUDIT, inputs, ["epsilon_id"])
    write_csv(NORMAL_FORMS, forms, ["normal_form_id"])
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": acceptance,
        "decision": (
            "DRY_RUN_ACCEPTED__FIT_COMPLETE_REGULATOR_ZERO_NORMAL_FORM_FAMILY"
            if acceptance
            else "REGULATOR_ZERO_ASYMPTOTIC_GATE_DRY_RUN_BLOCKED"
        ),
        "input_count": len(inputs),
        "normal_form_count": len(forms),
        "model_designs": designs,
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def solve_weighted(
    matrix: np.ndarray,
    values: np.ndarray,
    bounds: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int, float, np.ndarray]:
    weighted_matrix = matrix / bounds[:, None]
    weighted_values = values / bounds
    coefficients, _, rank, _ = np.linalg.lstsq(weighted_matrix, weighted_values, rcond=None)
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
    numerical_bound = float(np.sum(np.abs(influence[0]) * bounds))
    normalized_residuals = np.abs(prediction - values) / bounds
    unweighted_intercept = complex(np.linalg.lstsq(matrix, values, rcond=None)[0][0])
    stability_rows: list[dict[str, Any]] = []
    leave_one_out_shifts: list[float] = []
    for omitted in range(len(epsilon)):
        selected = np.arange(len(epsilon)) != omitted
        reduced_matrix = design_matrix(model_id, epsilon[selected])
        if np.linalg.matrix_rank(reduced_matrix) < reduced_matrix.shape[1]:
            continue
        reduced = solve_weighted(
            reduced_matrix, values[selected], bounds[selected]
        )[0]
        reduced_intercept = complex(reduced[0])
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
        window = solve_weighted(
            window_matrix,
            values[:retained_count],
            bounds[:retained_count],
        )[0]
        window_intercept = complex(window[0])
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
    condition_gate = condition * np.finfo(float).eps <= CONDITION_TIMES_MACHINE_EPSILON_LIMIT
    fit_gate = (
        rank == matrix.shape[1]
        and degrees_of_freedom >= 1
        and condition_gate
        and float(np.max(normalized_residuals)) <= NORMALIZED_RESIDUAL_LIMIT
        and len(leave_one_out_shifts) == len(epsilon)
        and all(math.isfinite(value) for value in leave_one_out_shifts)
        and math.isfinite(numerical_bound)
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
        "deterministic_input_disk_intercept_bound": numerical_bound,
        "maximum_normalized_complex_residual": float(np.max(normalized_residuals)),
        "rms_normalized_complex_residual": float(
            np.sqrt(np.mean(normalized_residuals**2))
        ),
        "maximum_leave_one_out_intercept_shift": max(leave_one_out_shifts),
        "maximum_small_epsilon_window_intercept_shift": max(window_shifts, default=0.0),
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
            upper_epsilon * values[index] - lower_epsilon * values[index + 1]
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
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5318,
        RESULT_5318,
        VALIDATION_5318,
        LADDER_5318,
        EVENTS_5318,
        DOCUMENT_5315,
        DRY_RUN,
        INPUT_AUDIT,
        NORMAL_FORMS,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5319 dry run did not pass")
    inputs, epsilon, values, bounds = input_arrays()
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
        row["family_intercept_shift_from_reference"] = abs(intercept - reference)
        row["model_conservative_zero_bound"] = (
            float(row["family_intercept_shift_from_reference"])
            + float(row["deterministic_input_disk_intercept_bound"])
            + float(row["maximum_leave_one_out_intercept_shift"])
            + float(row["maximum_small_epsilon_window_intercept_shift"])
            + float(row["weighting_choice_intercept_shift"])
        )
        row["model_relative_zero_bound"] = float(
            row["model_conservative_zero_bound"]
        ) / abs(reference)
    leading_rows = [row for row in fit_rows if row["required_for_leading_gate"]]
    remainder_rows = [row for row in fit_rows if row["required_for_remainder_gate"]]
    leading_bound = max(float(row["model_conservative_zero_bound"]) for row in leading_rows) + pairwise_shift
    full_bound = max(float(row["model_conservative_zero_bound"]) for row in remainder_rows) + pairwise_shift
    leading_relative = leading_bound / abs(reference)
    full_relative = full_bound / abs(reference)
    all_models_pass = all(bool(row["model_fit_gate_passes"]) for row in fit_rows)
    leading_gate = all_models_pass and leading_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    remainder_gate = all_models_pass and full_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    accepted = leading_gate and remainder_gate
    next_epsilon = float(epsilon[0] / 2.0)
    if accepted:
        decision = "FIXED_DECAY_REGULATOR_ZERO_LIMIT_ACCEPTED__BUILD_DECAY_ANGLE_LADDER"
    elif leading_gate and full_relative <= EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT:
        decision = "LEADING_ZERO_LIMIT_STABLE__ADD_E00125_TO_CLOSE_REMAINDER_ENVELOPE"
    else:
        decision = "REGULATOR_ZERO_LIMIT_UNRESOLVED__EXTEND_SMALL_EPSILON_LADDER"
    write_csv(MODEL_FITS, fit_rows, ["model_id"])
    write_csv(STABILITY, stability_rows, ["model_id", "stability_test"])
    write_csv(RICHARDSON, richardson, ["pair_id"])
    summary_rows = [
        {
            "summary_id": "FIXED_DECAY_REGULATOR_ZERO",
            **complex_fields("reference_zero_limit", reference),
            "pairwise_richardson_maximum_shift": pairwise_shift,
            "leading_family_absolute_bound": leading_bound,
            "leading_family_relative_bound": leading_relative,
            "complete_remainder_absolute_bound": full_bound,
            "complete_remainder_relative_bound": full_relative,
            "relative_acceptance_limit": ZERO_LIMIT_RELATIVE_BOUND_LIMIT,
            "leading_family_gate_passes": leading_gate,
            "complete_remainder_gate_passes": remainder_gate,
            "fixed_decay_regulator_zero_limit_accepted": accepted,
            "required_next_epsilon": "" if accepted else next_epsilon,
            "decision": decision,
            "valid_for_fixed_decay_regulator_zero_limit": accepted,
            "valid_for_full_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS[2:]},
        }
    ]
    write_csv(SUMMARY, summary_rows, ["summary_id"])
    parent = read_json(RESULT_5318)
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "regulator-zero-asymptotic-normal-form-gate",
        "acceptance_passed": accepted,
        "checkpoint_execution_passed": True,
        "decision": decision,
        "input_regulator_count": len(inputs),
        "fitted_model_count": len(fit_rows),
        "all_model_fit_gates_pass": all_models_pass,
        **complex_fields("reference_zero_limit", reference),
        "pairwise_richardson_maximum_shift": pairwise_shift,
        "leading_family_absolute_bound": leading_bound,
        "leading_family_relative_bound": leading_relative,
        "complete_remainder_absolute_bound": full_bound,
        "complete_remainder_relative_bound": full_relative,
        "relative_acceptance_limit": ZERO_LIMIT_RELATIVE_BOUND_LIMIT,
        "leading_family_gate_passes": leading_gate,
        "complete_remainder_gate_passes": remainder_gate,
        "required_next_regulator_epsilon": None if accepted else next_epsilon,
        "required_next_regulator_id": None if accepted else "E00125",
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == parent["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_fixed_decay_regulator_zero_limit": accepted,
            "valid_for_full_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS[2:]},
            "reason": (
                "Only a fixed-decay regulator-zero value is at issue. Decay-angle, "
                "full phase-space, UV, local-GR, and full-MTS claims remain locked."
            ),
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    return result


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    accepted = bool(result["acceptance_passed"])
    lines = [
        "# 5319 - Regulator-zero asymptotic normal-form gate",
        "",
        "## Derivation",
        "",
        "Checkpoint 5315 established a transverse support crossing with `kappa != 0`",
        "and outer primitive `A log|x-x_event| + regular`.  With the regulator,",
        "the local complex normal form is `log(kappa y + i epsilon)`.  Its one-sided",
        "integral admits `epsilon log epsilon`, `epsilon`, and quadratic-logarithmic",
        "remainders.  It does not admit a `sqrt(epsilon)` term: the squared coordinate",
        "used in 5315 regularizes a logarithm and is not a half-power physical branch.",
        "",
        "The five complex finite-regulator values are fitted with the full enumerated",
        "normal-form family.  Input uncertainties are conservative complex disks, not",
        "statistical standard deviations.  The intercept error uses the exact linear",
        "influence map `sum_i |h_i| delta_i`, plus family, leave-one-out, small-window,",
        "weighting-choice, and pairwise Richardson stability envelopes.",
        "",
        "## Result",
        "",
        f"- reference zero intercept: `{result['reference_zero_limit_real']:.12g}` "
        f"`{result['reference_zero_limit_imaginary']:+.12g} i`;",
        f"- leading-family relative bound: `{result['leading_family_relative_bound']:.12g}`;",
        f"- complete-remainder relative bound: `{result['complete_remainder_relative_bound']:.12g}`;",
        f"- acceptance limit: `{result['relative_acceptance_limit']:.12g}`;",
        f"- fixed-decay zero limit accepted: `{accepted}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if validation_passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "This checkpoint cannot establish decay-angle integration, the full phase-space",
        "coefficient, a UV prediction, local GR, or the full MTS theory.  If the complete",
        "remainder envelope misses the inherited one-percent gate, the next action is an",
        "actual smaller-regulator computation, not deletion of the remainder family.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    inputs = read_csv(INPUT_AUDIT)
    forms = read_csv(NORMAL_FORMS)
    models = read_csv(MODEL_FITS)
    stability = read_csv(STABILITY)
    richardson = read_csv(RICHARDSON)
    summary = read_csv(SUMMARY)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    correctly_bounded = (
        bool(result["acceptance_passed"])
        == (
            bool(result["leading_family_gate_passes"])
            and bool(result["complete_remainder_gate_passes"])
        )
    )
    nonclaim_blocker = (
        bool(result["acceptance_passed"])
        or (
            result["decision"]
            in {
                "LEADING_ZERO_LIMIT_STABLE__ADD_E00125_TO_CLOSE_REMAINDER_ENVELOPE",
                "REGULATOR_ZERO_LIMIT_UNRESOLVED__EXTEND_SMALL_EPSILON_LADDER",
            }
            and not any(
                bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS
            )
            and result["required_next_regulator_id"] == "E00125"
        )
    )
    gates = [
        validation_gate(
            "parent_five_regulator_ladder_validated",
            bool(dry["acceptance_passed"]),
            dry["decision"],
        ),
        validation_gate(
            "five_positive_sourced_input_disks_valid",
            len(inputs) == 5
            and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
            and all(parse_bool(row["finite_regulator_input_valid"]) for row in inputs),
            f"rows={len(inputs)}",
        ),
        validation_gate(
            "transverse_logarithmic_normal_form_closes_family",
            len(forms) == 3 and all(parse_bool(row["contract_passes"]) for row in forms),
            "sqrt(epsilon) excluded by nondegenerate logarithmic parent normal form",
        ),
        validation_gate(
            "all_required_fit_families_resolved",
            len(models) == len(MODEL_SPECS)
            and all(parse_bool(row["model_fit_gate_passes"]) for row in models),
            f"models={len(models)}",
        ),
        validation_gate(
            "leave_one_out_and_window_stability_recorded",
            bool(stability)
            and {row["model_id"] for row in stability}
            == {str(row["model_id"]) for row in MODEL_SPECS},
            f"rows={len(stability)}",
        ),
        validation_gate(
            "pairwise_richardson_ladder_complete",
            len(richardson) == 4,
            f"rows={len(richardson)}",
        ),
        validation_gate(
            "zero_limit_decision_matches_complete_envelope",
            correctly_bounded and len(summary) == 1,
            result["decision"],
        ),
        validation_gate(
            "blocked_limit_remains_nonclaim_and_actionable",
            nonclaim_blocker,
            str(result["required_next_regulator_id"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
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
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS[2:]
            ),
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
            "VALIDATED_REGULATOR_ZERO_ASYMPTOTIC_GATE"
            if passed
            else "REGULATOR_ZERO_ASYMPTOTIC_GATE_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    return parser.parse_args()


def main() -> int:
    M5318.M5312.set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
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
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
