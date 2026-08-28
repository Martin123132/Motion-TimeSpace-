from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"

SCRIPT_5350 = SCRIPTS / "Y5_R2FR_5350_D4_E0025_read_only_holdout_preregistration.py"
SCRIPT_5352 = SCRIPTS / "Y5_R2FR_5352_D4_E0025_branch_coordinate_refinement.py"
SCRIPT_5353 = (
    SCRIPTS / "Y5_R2FR_5353_D4_E0025_refined_all_eight_endpoint_coefficient.py"
)
BASELINE = FUNCTIONAL_RG / "5349"
BASELINE_RESULT = BASELINE / "D4_three_regulator_coefficient_result.json"
BASELINE_INPUTS = BASELINE / "D4_three_regulator_coefficient_inputs.csv"
BASELINE_VALIDATION = BASELINE / "D4_three_regulator_coefficient_validation.csv"
PREREG = FUNCTIONAL_RG / "5350" / "E0025"
PREREG_RESULT = PREREG / "D4_E0025_affine_holdout_preregistration_result.json"
PREDICTIONS = PREREG / "D4_E0025_affine_holdout_predictions.csv"
PREREG_VALIDATION = PREREG / "D4_E0025_affine_holdout_preregistration_validation.csv"
PREREG_SOURCE_REGISTER = PREREG / "source_register.csv"
REFINEMENT = FUNCTIONAL_RG / "5352" / "E0025" / "branch-geometry"
REFINEMENT_RESULT = REFINEMENT / "D4_E0025_branch_coordinate_refinement_result.json"
REFINEMENT_VALIDATION = REFINEMENT / "D4_E0025_branch_coordinate_refinement_validation.csv"
REFINED_EVENTS = REFINEMENT / "D4_E0025_bracket_refined_events.csv"
COEFFICIENT = FUNCTIONAL_RG / "5353" / "E0025" / "all-eight"
COEFFICIENT_RESULT = COEFFICIENT / "D4_E0025_all_eight_endpoint_result.json"
COEFFICIENT_TOTAL = COEFFICIENT / "D4_E0025_all_eight_endpoint_log_coefficient.csv"
COEFFICIENT_VALIDATION = COEFFICIENT / "D4_E0025_all_eight_endpoint_validation.csv"
COEFFICIENT_SOURCE_REGISTER = COEFFICIENT / "source_register.csv"

EPSILON_ID = "E0025"
EPSILON = 0.0025
PREDICTION_IDS = [
    "WIDE_BRACKET_2H_8H",
    "SMALL_EXTRAPOLATION_H_2H",
    "OUTER_BRACKET_H_8H",
]
PREREG_CLAIM = "valid_for_D4_E0025_affine_holdout_preregistration"
COEFFICIENT_CLAIM = "valid_for_D4_E0025_all_eight_endpoint_coefficients"
HOLDOUT_CLAIM = "valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout"
REGULATOR_ZERO_CLAIM = "valid_for_D4_endpoint_coefficient_regulator_zero_limit"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def no_claims() -> dict[str, bool]:
    return {
        HOLDOUT_CLAIM: False,
        REGULATOR_ZERO_CLAIM: False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_angular_convergence": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def source_chain_current(payload: dict[str, Any]) -> tuple[bool, int, list[str]]:
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0, ["missing_or_malformed_source_files"]
    failures: list[str] = []
    count = 0
    for row in rows:
        path = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if not path.is_file():
            failures.append(f"missing:{path}")
        elif expected == "MISSING" or digest(path) != expected:
            failures.append(f"stale:{path}")
        else:
            count += 1
    return not failures, count, failures


def parse_weights(text: str) -> dict[str, float]:
    weights: dict[str, float] = {}
    for term in text.split("|"):
        epsilon_id, value = term.split(":", maxsplit=1)
        weights[epsilon_id] = float(value)
    return weights


def finite_number(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def prediction_integrity(
    predictions: list[dict[str, str]], training: dict[str, dict[str, str]]
) -> tuple[bool, list[dict[str, Any]]]:
    audit: list[dict[str, Any]] = []
    all_pass = True
    for row in predictions:
        weights = parse_weights(row["source_weights"])
        expected = sum(
            weight
            * complex(
                float(training[epsilon_id]["A_finite_epsilon_real"]),
                float(training[epsilon_id]["A_finite_epsilon_imaginary"]),
            )
            for epsilon_id, weight in weights.items()
        )
        expected_radius = math.fsum(
            abs(weight)
            * float(training[epsilon_id]["A_diagnostic_disk_radius"])
            for epsilon_id, weight in weights.items()
        )
        frozen = complex(
            float(row["predicted_A_real"]), float(row["predicted_A_imaginary"])
        )
        frozen_radius = float(row["predicted_A_disk_radius"])
        centre_error = abs(frozen - expected)
        radius_error = abs(frozen_radius - expected_radius)
        row_pass = (
            centre_error <= 2.0e-15
            and radius_error <= 2.0e-15
            and abs(float(row["predicted_A_magnitude"]) - abs(frozen)) <= 2.0e-15
        )
        all_pass = all_pass and row_pass
        audit.append(
            {
                "prediction_id": row["prediction_id"],
                "frozen_prediction_integrity_passes": row_pass,
                "frozen_centre_recalculation_error": centre_error,
                "frozen_radius_recalculation_error": radius_error,
            }
        )
    return all_pass, audit


def input_state() -> dict[str, Any]:
    required = [
        Path(__file__),
        SCRIPT_5350,
        SCRIPT_5352,
        SCRIPT_5353,
        BASELINE_RESULT,
        BASELINE_INPUTS,
        BASELINE_VALIDATION,
        PREREG_RESULT,
        PREDICTIONS,
        PREREG_VALIDATION,
        PREREG_SOURCE_REGISTER,
        REFINEMENT_RESULT,
        REFINEMENT_VALIDATION,
        REFINED_EVENTS,
        COEFFICIENT_RESULT,
        COEFFICIENT_TOTAL,
        COEFFICIENT_VALIDATION,
        COEFFICIENT_SOURCE_REGISTER,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"required": required, "missing": missing, "checks": {"all_input_paths_exist": False}}

    baseline = read_json(BASELINE_RESULT)
    prereg = read_json(PREREG_RESULT)
    refinement = read_json(REFINEMENT_RESULT)
    coefficient = read_json(COEFFICIENT_RESULT)
    training_rows = read_csv(BASELINE_INPUTS)
    training = {row["epsilon_id"]: row for row in training_rows}
    predictions = read_csv(PREDICTIONS)
    total_rows = read_csv(COEFFICIENT_TOTAL)
    baseline_validation = read_csv(BASELINE_VALIDATION)
    prereg_validation = read_csv(PREREG_VALIDATION)
    refinement_validation = read_csv(REFINEMENT_VALIDATION)
    coefficient_validation = read_csv(COEFFICIENT_VALIDATION)
    baseline_current = source_chain_current(baseline)
    prereg_current = source_chain_current(prereg)
    refinement_current = source_chain_current(refinement)
    coefficient_current = source_chain_current(coefficient)
    integrity_pass, integrity_audit = prediction_integrity(predictions, training)
    historical_drifts = prereg.get("historical_recursive_E0025_source_drifts", [])
    total = total_rows[0] if len(total_rows) == 1 else {}
    checks = {
        "all_input_paths_exist": True,
        "baseline_three_rung_gate_passes": baseline.get("validation_passed") is True
        and baseline.get("claim_boundary", {}).get(
            "valid_for_D4_three_regulator_affine_endpoint_coefficient_stability"
        )
        is True
        and bool(baseline_validation)
        and all(parse_bool(row.get("passed")) for row in baseline_validation),
        "baseline_source_chain_is_current": baseline_current[0]
        and baseline_current[1] > 0,
        "preregistration_passes": prereg.get("validation_passed") is True
        and prereg.get("claim_boundary", {}).get(PREREG_CLAIM) is True
        and prereg.get("future_acceptance_rule")
        == "all three preregistered propagated contrast disks must contain zero"
        and bool(prereg_validation)
        and all(parse_bool(row.get("passed")) for row in prereg_validation),
        "preregistration_source_chain_is_current": prereg_current[0]
        and prereg_current[1] > 0,
        "historical_recursive_drift_is_disclosed": prereg.get(
            "historical_recursive_E0025_source_chain_current"
        )
        is False
        and int(prereg.get("historical_recursive_E0025_source_drift_count", -1))
        == len(historical_drifts)
        == 3
        and prereg.get(
            "holdout_uses_revalidated_current_event_contracts_not_historical_deep_chain"
        )
        is True,
        "refinement_gate_passes": refinement.get("validation_passed") is True
        and refinement.get("claim_boundary", {}).get(
            "valid_for_D4_E0025_branch_event_coordinate_refinement"
        )
        is True
        and refinement_current[0]
        and bool(refinement_validation)
        and all(parse_bool(row.get("passed")) for row in refinement_validation),
        "coefficient_gate_passes": coefficient.get("validation_passed") is True
        and coefficient.get("claim_boundary", {}).get(COEFFICIENT_CLAIM) is True
        and coefficient_current[0]
        and bool(coefficient_validation)
        and all(parse_bool(row.get("passed")) for row in coefficient_validation),
        "coefficient_total_is_finite_and_contract_valid": len(total_rows) == 1
        and total.get("epsilon_id") == EPSILON_ID
        and math.isclose(float(total.get("epsilon", math.nan)), EPSILON, abs_tol=1.0e-15)
        and all(
            finite_number(total.get(field))
            for field in [
                "A_total_finite_epsilon_estimator_real",
                "A_total_finite_epsilon_estimator_imaginary",
                "A_total_diagnostic_disk_radius",
            ]
        )
        and float(total.get("A_total_diagnostic_disk_radius", -1.0)) >= 0.0
        and parse_bool(total.get("all_event_coefficient_contracts_pass"))
        and parse_bool(total.get(COEFFICIENT_CLAIM))
        and not parse_bool(total.get("total_A_multi_regulator_limit_complete")),
        "three_predictions_are_frozen_and_nonclaim": [
            row.get("prediction_id") for row in predictions
        ]
        == PREDICTION_IDS
        and all(
            row.get("target_epsilon_id") == EPSILON_ID
            and math.isclose(
                float(row.get("target_epsilon", math.nan)), EPSILON, abs_tol=1.0e-15
            )
            and parse_bool(row.get(PREREG_CLAIM))
            and not parse_bool(row.get(HOLDOUT_CLAIM))
            and row.get("future_contrast_definition")
            == "A_E0025_minus_preregistered_prediction"
            and row.get("future_acceptance_rule")
            == "abs(contrast)<=E0025_radius+predicted_A_disk_radius"
            and all(
                finite_number(row.get(field))
                for field in [
                    "predicted_A_real",
                    "predicted_A_imaginary",
                    "predicted_A_disk_radius",
                ]
            )
            and float(row.get("predicted_A_disk_radius", -1.0)) >= 0.0
            for row in predictions
        ),
        "frozen_predictions_match_training_inputs": integrity_pass,
        "preregistration_precedes_refined_coefficient": datetime.fromisoformat(
            prereg["updated_utc"]
        )
        < datetime.fromisoformat(coefficient["updated_utc"]),
        "formal_workbench_is_unchanged_in_inputs": all(
            payload.get("formalization_workbench_modified_file_count") == 0
            for payload in [baseline, prereg, refinement, coefficient]
        ),
    }
    return {
        "required": required,
        "missing": [],
        "checks": checks,
        "baseline": baseline,
        "prereg": prereg,
        "refinement": refinement,
        "coefficient": coefficient,
        "training_rows": training_rows,
        "predictions": predictions,
        "total": total,
        "integrity_audit": integrity_audit,
        "source_chain_audit": {
            "baseline": baseline_current,
            "preregistration": prereg_current,
            "refinement": refinement_current,
            "coefficient": coefficient_current,
        },
    }


def source_rows(paths: list[Path]) -> tuple[list[dict[str, Any]], str]:
    rows: list[dict[str, Any]] = []
    signature = hashlib.sha256()
    for path in paths:
        resolved = path.resolve()
        sha256 = digest(resolved)
        signature.update(f"{resolved}|{sha256}\n".encode("utf-8"))
        rows.append(
            {
                "path": str(resolved),
                "sha256": sha256,
                "exists": True,
                **no_claims(),
            }
        )
    return rows, signature.hexdigest()


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    state = input_state()
    if not state.get("checks") or not all(state["checks"].values()):
        raise RuntimeError(f"holdout preflight failed: {state.get('checks')} {state.get('missing')}")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    contrast_path = output / "D4_E0025_four_regulator_affine_holdout_contrasts.csv"
    input_path = output / "D4_E0025_four_regulator_affine_holdout_inputs.csv"
    source_path = output / "source_register.csv"
    validation_path = output / "D4_E0025_four_regulator_affine_holdout_validation.csv"
    result_path = output / "D4_E0025_four_regulator_affine_holdout_result.json"
    status_path = output / "status.json"

    total = state["total"]
    measured = complex(
        float(total["A_total_finite_epsilon_estimator_real"]),
        float(total["A_total_finite_epsilon_estimator_imaginary"]),
    )
    measured_radius = float(total["A_total_diagnostic_disk_radius"])
    contrasts: list[dict[str, Any]] = []
    for prediction in state["predictions"]:
        predicted = complex(
            float(prediction["predicted_A_real"]),
            float(prediction["predicted_A_imaginary"]),
        )
        predicted_radius = float(prediction["predicted_A_disk_radius"])
        contrast = measured - predicted
        radius = measured_radius + predicted_radius
        contains_zero = abs(contrast) <= radius
        contrasts.append(
            {
                "prediction_id": prediction["prediction_id"],
                "source_weights": prediction["source_weights"],
                "measured_A_real": measured.real,
                "measured_A_imaginary": measured.imag,
                "measured_A_disk_radius": measured_radius,
                "frozen_predicted_A_real": predicted.real,
                "frozen_predicted_A_imaginary": predicted.imag,
                "frozen_predicted_A_disk_radius": predicted_radius,
                "contrast_real": contrast.real,
                "contrast_imaginary": contrast.imag,
                "contrast_magnitude": abs(contrast),
                "propagated_contrast_disk_radius": radius,
                "contrast_radius_ratio": abs(contrast) / max(radius, 1.0e-300),
                "contrast_disk_margin": radius - abs(contrast),
                "contrast_disk_contains_zero": contains_zero,
                **no_claims(),
            }
        )
    holdout_passes = all(row["contrast_disk_contains_zero"] for row in contrasts)
    for row in contrasts:
        row[HOLDOUT_CLAIM] = holdout_passes

    inputs: list[dict[str, Any]] = []
    for row in state["training_rows"]:
        inputs.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": float(row["epsilon"]),
                "role": "AFFINE_TRAINING_RUNG",
                "A_real": float(row["A_finite_epsilon_real"]),
                "A_imaginary": float(row["A_finite_epsilon_imaginary"]),
                "A_disk_radius": float(row["A_diagnostic_disk_radius"]),
                **no_claims(),
            }
        )
    inputs.append(
        {
            "epsilon_id": EPSILON_ID,
            "epsilon": EPSILON,
            "role": "PREREGISTERED_READ_ONLY_HOLDOUT_RUNG",
            "A_real": measured.real,
            "A_imaginary": measured.imag,
            "A_disk_radius": measured_radius,
            **no_claims(),
        }
    )

    sources, signature = source_rows(state["required"])
    gates = [
        validation_row("preflight_passes", all(state["checks"].values()), state["checks"]),
        validation_row("all_sources_exist_and_are_hashed", all(row["sha256"] for row in sources), len(sources)),
        validation_row("exactly_three_frozen_contrasts_present", [row["prediction_id"] for row in contrasts] == PREDICTION_IDS, len(contrasts)),
        validation_row("all_preregistered_contrast_disks_contain_zero", holdout_passes, max(row["contrast_radius_ratio"] for row in contrasts)),
        validation_row("finite_four_rung_holdout_only", all(not parse_bool(row.get(REGULATOR_ZERO_CLAIM)) for row in contrasts), False),
        validation_row("historical_recursive_drift_remains_disclosed", state["checks"]["historical_recursive_drift_is_disclosed"], state["prereg"].get("historical_recursive_E0025_source_drifts")),
        validation_row("formal_workbench_unchanged", state["checks"]["formal_workbench_is_unchanged_in_inputs"], 0),
        validation_row("scripts_cache_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    claims = no_claims()
    claims[HOLDOUT_CLAIM] = passed
    result = {
        "mode": "D4-E0025-four-regulator-preregistered-affine-holdout",
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "validation_passed": passed,
        "decision": (
            "D4_E0025_FOUR_REGULATOR_AFFINE_HOLDOUT_PASS__REGULATOR_ZERO_REMAINS_UNPROVEN"
            if passed
            else "D4_E0025_FOUR_REGULATOR_AFFINE_HOLDOUT_BLOCKED"
        ),
        "holdout_prediction_count": len(contrasts),
        "all_preregistered_contrast_disks_contain_zero": holdout_passes,
        "maximum_contrast_radius_ratio": max(row["contrast_radius_ratio"] for row in contrasts),
        "minimum_contrast_disk_margin": min(row["contrast_disk_margin"] for row in contrasts),
        "A_E0025_real": measured.real,
        "A_E0025_imaginary": measured.imag,
        "A_E0025_magnitude": abs(measured),
        "A_E0025_diagnostic_disk_radius": measured_radius,
        "coefficient_regulator_zero_limit_complete": False,
        "next_required_gate": "SOURCE_DERIVED_REMAINDER_BOUND_OR_TWO_ADDITIONAL_REGULATOR_RUNGS",
        "historical_recursive_E0025_source_chain_current": state["prereg"].get("historical_recursive_E0025_source_chain_current"),
        "historical_recursive_E0025_source_drifts": state["prereg"].get("historical_recursive_E0025_source_drifts"),
        "holdout_uses_revalidated_current_event_contracts_not_historical_deep_chain": True,
        "source_signature": signature,
        "claim_boundary": claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_csv(contrast_path, contrasts)
    atomic_csv(input_path, inputs)
    atomic_csv(source_path, sources)
    atomic_csv(validation_path, gates)
    atomic_json(result_path, result)
    atomic_json(
        status_path,
        {
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": result["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def dry_run() -> dict[str, Any]:
    state = input_state()
    checks = state.get("checks", {})
    return {
        "mode": "dry-run",
        "checks": checks,
        "all_pass": bool(checks) and all(checks.values()),
        **no_claims(),
    }


def self_test() -> dict[str, Any]:
    inside = abs(complex(3.0, 4.0)) <= 5.0
    outside = abs(complex(3.0, 4.0)) <= 4.999
    checks = {
        "closed_disk_boundary_is_accepted": inside,
        "outside_disk_is_rejected": not outside,
        "downstream_claims_start_false": all(value is False for value in no_claims().values()),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        result = dry_run()
    else:
        if arguments.output_dir is None:
            parser.error("--output-dir is required")
        result = run(arguments.output_dir)
    if arguments.self_test or arguments.dry_run:
        print(json.dumps(result, indent=2, sort_keys=True))
    passed = result.get("all_pass", result.get("validation_passed", False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
