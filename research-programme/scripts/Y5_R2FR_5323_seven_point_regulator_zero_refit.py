from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5323"

SCRIPT_5319 = SCRIPTS / "Y5_R2FR_5319_regulator_zero_asymptotic_gate.py"
RESULT_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_asymptotic_gate_result.json"
VALIDATION_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_asymptotic_gate_validation.csv"
NORMAL_FORMS_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_local_normal_form_contract.csv"
LADDER_5318 = FUNCTIONAL_RG / "5318" / "five_regulator_fixed_decay_convergence.csv"
SCRIPT_5320 = SCRIPTS / "Y5_R2FR_5320_E00125_finite_regulator_extension.py"
RESULT_5320 = FUNCTIONAL_RG / "5320" / "E00125_finite_regulator_extension_result.json"
VALIDATION_5320 = FUNCTIONAL_RG / "5320" / "E00125_finite_regulator_extension_validation.csv"
FINITE_5320 = FUNCTIONAL_RG / "5320" / "E00125_finite_regulator_fixed_decay_convergence.csv"
SCRIPT_5321 = SCRIPTS / "Y5_R2FR_5321_six_point_regulator_zero_refit.py"
RESULT_5321 = FUNCTIONAL_RG / "5321" / "six_point_regulator_zero_refit_result.json"
VALIDATION_5321 = FUNCTIONAL_RG / "5321" / "six_point_regulator_zero_refit_validation.csv"
SCRIPT_5322 = SCRIPTS / "Y5_R2FR_5322_E000625_finite_regulator_extension.py"
RESULT_5322 = FUNCTIONAL_RG / "5322" / "E000625_finite_regulator_extension_result.json"
VALIDATION_5322 = FUNCTIONAL_RG / "5322" / "E000625_finite_regulator_extension_validation.csv"
FINITE_5322 = FUNCTIONAL_RG / "5322" / "E000625_finite_regulator_fixed_decay_convergence.csv"

INPUT_AUDIT = SOURCE / "seven_regulator_zero_fit_input_audit.csv"
MODEL_FITS = SOURCE / "seven_regulator_zero_model_fits.csv"
STABILITY = SOURCE / "seven_regulator_zero_fit_stability.csv"
RICHARDSON = SOURCE / "seven_regulator_pairwise_richardson.csv"
SUMMARY = SOURCE / "seven_regulator_zero_limit_summary.csv"
RESULT = SOURCE / "seven_point_regulator_zero_refit_result.json"
VALIDATION = SOURCE / "seven_point_regulator_zero_refit_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5323_VALIDATION.csv"
DOCUMENT = POST / "5323-Y5-R2FR-seven-point-regulator-zero-refit.md"

CHECKPOINT = 5323
PARENT_CHECKPOINT = 5322
MARKER = "MTS_5323_SEVEN_POINT_REGULATOR_ZERO_REFIT"
REVISION = "seven-point-regulator-zero-refit-v1"
EXPECTED_IDS = (
    "E000625",
    "E00125",
    "E0025",
    "E005",
    "E010",
    "E020",
    "E040",
)
REFERENCE_MODEL_ID = "M1_ANALYTIC_LINEAR"
ZERO_LIMIT_RELATIVE_BOUND_LIMIT = 1.0e-2
EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT = 2.0e-2
NEXT_EPSILON_ID = "E0003125"
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


M5321 = load_module("mts_5321_for_5323", SCRIPT_5321)
M5319 = M5321.M5319
M5319.EXPECTED_IDS = EXPECTED_IDS
M5283 = M5319.M5283


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5321.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5321.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5321.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5321.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5321.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5321.complex_fields(prefix, value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5321.validation_gate(gate, passed, detail)


def source_for_epsilon(epsilon_id: str) -> Path:
    if epsilon_id == "E000625":
        return FINITE_5322
    if epsilon_id == "E00125":
        return FINITE_5320
    return LADDER_5318


def input_arrays() -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, np.ndarray]:
    rows = read_csv(FINITE_5322) + read_csv(FINITE_5320) + read_csv(LADDER_5318)
    rows.sort(key=lambda row: float(row["epsilon"]))
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
                "source_path": str(source_for_epsilon(row["epsilon_id"])),
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


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5319,
        RESULT_5319,
        VALIDATION_5319,
        NORMAL_FORMS_5319,
        LADDER_5318,
        SCRIPT_5320,
        RESULT_5320,
        VALIDATION_5320,
        FINITE_5320,
        SCRIPT_5321,
        RESULT_5321,
        VALIDATION_5321,
        SCRIPT_5322,
        RESULT_5322,
        VALIDATION_5322,
        FINITE_5322,
        INPUT_AUDIT,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5322)
    parent_validation = read_csv(VALIDATION_5322)
    prior_validation = read_csv(VALIDATION_5319)
    normal_forms = read_csv(NORMAL_FORMS_5319)
    inputs, epsilon, values, bounds = input_arrays()
    input_gate = (
        bool(parent["acceptance_passed"])
        and parent["decision"] == "E000625_FINITE_REGULATOR_CONVERGED__REFIT_ZERO_LIMIT"
        and all(parse_bool(row["passed"]) for row in parent_validation)
        and all(parse_bool(row["passed"]) for row in prior_validation)
        and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
        and all(bool(row["finite_regulator_input_valid"]) for row in inputs)
        and np.all(np.diff(epsilon) > 0.0)
        and len(normal_forms) == 3
        and all(parse_bool(row["contract_passes"]) for row in normal_forms)
    )
    if not input_gate:
        raise RuntimeError("seven-point regulator-zero input gate failed")
    write_csv(INPUT_AUDIT, inputs, ["epsilon_id"])
    fit_rows: list[dict[str, Any]] = []
    stability_rows: list[dict[str, Any]] = []
    for specification in M5319.MODEL_SPECS:
        fit, stability = M5319.fit_model(specification, epsilon, values, bounds)
        fit_rows.append(fit)
        stability_rows.extend(stability)
    reference_row = next(
        row for row in fit_rows if row["model_id"] == REFERENCE_MODEL_ID
    )
    reference = complex(
        float(reference_row["weighted_zero_intercept_real"]),
        float(reference_row["weighted_zero_intercept_imaginary"]),
    )
    richardson = M5319.richardson_rows(inputs, epsilon, values)
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
    leading_rows = [row for row in fit_rows if row["required_for_leading_gate"]]
    remainder_rows = [row for row in fit_rows if row["required_for_remainder_gate"]]
    leading_bound = (
        max(float(row["model_conservative_zero_bound"]) for row in leading_rows)
        + pairwise_shift
    )
    full_bound = (
        max(float(row["model_conservative_zero_bound"]) for row in remainder_rows)
        + pairwise_shift
    )
    leading_relative = leading_bound / abs(reference)
    full_relative = full_bound / abs(reference)
    all_models_pass = all(bool(row["model_fit_gate_passes"]) for row in fit_rows)
    leading_gate = all_models_pass and leading_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    remainder_gate = all_models_pass and full_relative <= ZERO_LIMIT_RELATIVE_BOUND_LIMIT
    accepted = leading_gate and remainder_gate
    next_epsilon = float(epsilon[0] / 2.0)
    if accepted:
        decision = "SEVEN_POINT_FIXED_DECAY_ZERO_LIMIT_ACCEPTED__BUILD_DECAY_ANGLE_LADDER"
    elif leading_gate and full_relative <= EXTENSION_TRIGGER_RELATIVE_BOUND_LIMIT:
        decision = "SEVEN_POINT_LIMIT_STABLE__ADD_E0003125_TO_CLOSE_REMAINDER_ENVELOPE"
    else:
        decision = "SEVEN_POINT_ZERO_LIMIT_UNRESOLVED__EXTEND_SMALL_EPSILON_LADDER"
    write_csv(MODEL_FITS, fit_rows, ["model_id"])
    write_csv(STABILITY, stability_rows, ["model_id", "stability_test"])
    write_csv(RICHARDSON, richardson, ["pair_id"])
    write_csv(
        SUMMARY,
        [
            {
                "summary_id": "SEVEN_POINT_FIXED_DECAY_REGULATOR_ZERO",
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
        ],
        ["summary_id"],
    )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "seven-point-regulator-zero-normal-form-refit",
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
        "required_next_regulator_id": None if accepted else NEXT_EPSILON_ID,
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == parent["formalization_workbench_end_digest"] else -1
        ),
        "claim_boundary": {
            "valid_for_fixed_decay_regulator_zero_limit": accepted,
            "valid_for_full_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS[2:]},
            "reason": (
                "Only the fixed-decay regulator-zero envelope is tested. Decay-angle, "
                "phase-space, UV, local-GR, and full-MTS claims remain locked."
            ),
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    return result


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    lines = [
        "# 5323 - Seven-point regulator-zero refit",
        "",
        "## Method",
        "",
        "The validated E000625 value is appended to the six-point ladder. Every",
        "normal-form family derived in 5319 remains present, including quadratic and",
        "quadratic-logarithmic remainder stresses. The envelope retains conservative",
        "complex input disks, leave-one-out shifts, small-epsilon windows, weighting",
        "changes, family spread, and all adjacent Richardson shifts.",
        "",
        "## Result",
        "",
        f"- reference zero intercept: `{result['reference_zero_limit_real']:.12g}` "
        f"`{result['reference_zero_limit_imaginary']:+.12g} i`;",
        f"- leading-family relative bound: `{result['leading_family_relative_bound']:.12g}`;",
        f"- complete-remainder relative bound: `{result['complete_remainder_relative_bound']:.12g}`;",
        f"- acceptance limit: `{result['relative_acceptance_limit']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if validation_passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "No remainder family or adverse stability branch is removed to force",
        "acceptance. This checkpoint concerns one fixed decay angle only; the",
        "decay-angle ladder and all broader field-theory claims remain separate.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    inputs = read_csv(INPUT_AUDIT)
    models = read_csv(MODEL_FITS)
    stability = read_csv(STABILITY)
    richardson = read_csv(RICHARDSON)
    summary = read_csv(SUMMARY)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    decision_consistent = bool(result["acceptance_passed"]) == (
        bool(result["leading_family_gate_passes"])
        and bool(result["complete_remainder_gate_passes"])
    )
    blocker_consistent = bool(result["acceptance_passed"]) or (
        result["required_next_regulator_id"] == NEXT_EPSILON_ID
        and result["decision"]
        in {
            "SEVEN_POINT_LIMIT_STABLE__ADD_E0003125_TO_CLOSE_REMAINDER_ENVELOPE",
            "SEVEN_POINT_ZERO_LIMIT_UNRESOLVED__EXTEND_SMALL_EPSILON_LADDER",
        }
        and not any(bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS)
    )
    gates = [
        validation_gate(
            "seven_valid_finite_regulator_inputs",
            len(inputs) == 7
            and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
            and all(parse_bool(row["finite_regulator_input_valid"]) for row in inputs),
            f"rows={len(inputs)}",
        ),
        validation_gate(
            "all_complete_normal_form_models_resolved",
            len(models) == len(M5319.MODEL_SPECS)
            and all(parse_bool(row["model_fit_gate_passes"]) for row in models),
            f"models={len(models)}",
        ),
        validation_gate(
            "seven_point_stability_tree_complete",
            bool(stability)
            and {row["model_id"] for row in stability}
            == {row["model_id"] for row in M5319.MODEL_SPECS},
            f"rows={len(stability)}",
        ),
        validation_gate(
            "six_adjacent_richardson_pairs_complete",
            len(richardson) == 6,
            f"rows={len(richardson)}",
        ),
        validation_gate(
            "decision_matches_complete_remainder_envelope",
            decision_consistent and len(summary) == 1,
            result["decision"],
        ),
        validation_gate(
            "unclosed_limit_is_nonclaim_and_actionable",
            blocker_consistent,
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
            "VALIDATED_SEVEN_POINT_REGULATOR_ZERO_REFIT"
            if passed
            else "SEVEN_POINT_REGULATOR_ZERO_REFIT_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    return parser.parse_args()


def main() -> int:
    M5319.M5318.M5312.set_below_normal_priority()
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
