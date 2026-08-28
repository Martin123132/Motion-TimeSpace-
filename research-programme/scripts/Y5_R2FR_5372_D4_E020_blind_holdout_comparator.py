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
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
MTS_RESIDUALS = POST / "source-intake" / "mts_residuals"

HOLDOUT_ROWS = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_dual_holdout_predictions.csv"
HOLDOUT_RESULT = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_result.json"
HOLDOUT_VALIDATION = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_validation.csv"
HOLDOUT_SOURCES = FUNCTIONAL_RG / "5363" / "source_register.csv"

RUNNER_SCRIPT = SCRIPTS / "Y5_R2FR_5371_D4_E020_preregistered_seventh_rung_runner.py"
RUNNER_ROOT = FUNCTIONAL_RG / "5371" / "E020"
RUNNER_RESULT = RUNNER_ROOT / "D4_E020_seventh_rung_runner_result.json"
RUNNER_VALIDATION = RUNNER_ROOT / "D4_E020_seventh_rung_runner_validation.csv"
RUNNER_SOURCES = RUNNER_ROOT / "source_register.csv"

MEASUREMENT_ROOT = FUNCTIONAL_RG / "5334" / "E020"
MEASUREMENT_FINITE = MEASUREMENT_ROOT / "D4_outer_event_aligned_E020_finite_value.csv"
MEASUREMENT_RESULT = MEASUREMENT_ROOT / "D4_outer_event_aligned_E020_result.json"
MEASUREMENT_VALIDATION = MEASUREMENT_ROOT / "D4_outer_event_aligned_E020_validation.csv"
MEASUREMENT_SEMANTIC_VALIDATION = (
    MEASUREMENT_ROOT / "D4_outer_event_aligned_E020_semantic_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5372" / "E020"
CONTRACT = OUTPUT / "D4_E020_blind_holdout_comparison_contract.json"
CONTRACT_VALIDATION = OUTPUT / "D4_E020_blind_holdout_comparison_contract_validation.csv"
CONTRACT_SOURCES = OUTPUT / "D4_E020_blind_holdout_comparison_contract_sources.csv"
RESULT = OUTPUT / "D4_E020_blind_holdout_comparison_result.json"
VALIDATION = OUTPUT / "D4_E020_blind_holdout_comparison_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5372_VALIDATION.csv"
DOCUMENT = POST / "5372-Y5-R2FR-D4-E020-blind-holdout-comparator.md"

CHECKPOINT = 5372
MARKER = "MTS_5372_D4_E020_BLIND_HOLDOUT_COMPARATOR"
REVISION = "D4-E020-blind-holdout-comparator-v1"
EPSILON_ID = "E020"
EPSILON = 0.02
COMPARISON_RULE = "ABS_MEASURED_MINUS_FROZEN_PREDICTION_LE_RADIUS_SUM"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_CONTRACT = "valid_for_D4_E020_blind_holdout_comparison_contract"
CLAIM_COMPATIBILITY = "valid_for_D4_E020_complete_family_holdout_compatibility"
FALSE_CLAIMS = (
    "valid_for_D4_seven_rung_complete_second_order_fit",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def csv_passes(path: Path) -> bool:
    if not path.is_file():
        return False
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row.get("passed", False)) for row in rows)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def false_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    if not path.is_file():
        return False, 0, [str(path)]
    rows = read_csv(path)
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def result_sources_current(payload: dict[str, Any]) -> tuple[bool, int, list[str]]:
    rows = payload.get("source_files", [])
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return bool(rows) and not drifts, len(rows), drifts


def prediction_row() -> dict[str, str]:
    rows = [row for row in read_csv(HOLDOUT_ROWS) if row["holdout_epsilon_id"] == EPSILON_ID]
    if len(rows) != 1:
        raise RuntimeError("exactly one frozen E020 prediction is required")
    return rows[0]


def accepted_measurement_available() -> bool:
    if MEASUREMENT_RESULT.is_file():
        result = read_json(MEASUREMENT_RESULT)
        if result.get("acceptance_passed") is True and result.get("completed_full_run") is True:
            return True
    if MEASUREMENT_FINITE.is_file():
        return any(
            parse_bool(row.get("finite_regulator_fixed_decay_integral_accepted", False))
            for row in read_csv(MEASUREMENT_FINITE)
        )
    return False


def contract_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        HOLDOUT_ROWS,
        HOLDOUT_RESULT,
        HOLDOUT_VALIDATION,
        HOLDOUT_SOURCES,
        RUNNER_SCRIPT,
        RUNNER_RESULT,
        RUNNER_VALIDATION,
        RUNNER_SOURCES,
    )


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5372 - D4 E020 blind holdout comparator",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        "The E020 prediction and radius-sum disk rule were frozen before an accepted E020 D4 measurement existed. Compatibility is a holdout check, not a regulator-zero proof.",
        "",
    ]
    if payload.get("comparison_executed"):
        lines.extend(
            [
                f"- centre separation: `{payload['centre_separation']}`;",
                f"- combined disk: `{payload['combined_disk_radius']}`;",
                f"- normalized disk separation: `{payload['normalized_disk_separation']}`;",
                f"- compatible: `{payload['holdout_compatible']}`.",
                "",
            ]
        )
    lines.append(
        "No numerical uniform remainder, regulator-zero, angular, UV, local-GR, or full-MTS claim is made here."
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def freeze_contract() -> dict[str, Any]:
    required = contract_source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    prediction = prediction_row()
    holdout = read_json(HOLDOUT_RESULT)
    runner = read_json(RUNNER_RESULT)
    holdout_sources = source_register_current(HOLDOUT_SOURCES)
    runner_sources = source_register_current(RUNNER_SOURCES)
    measurement_absent = not accepted_measurement_available()
    numeric_prediction = all(
        math.isfinite(float(prediction[field]))
        for field in (
            "predicted_fixed_decay_integral_real",
            "predicted_fixed_decay_integral_imaginary",
            "prediction_total_disk_radius",
        )
    ) and float(prediction["prediction_total_disk_radius"]) > 0.0
    checks = {
        "E020_prediction_is_unique_numeric_and_frozen": abs(
            float(prediction["holdout_epsilon"]) - EPSILON
        )
        <= 1.0e-16
        and parse_bool(prediction["frozen_before_accepted_holdout_value"])
        and not parse_bool(prediction["comparison_to_measured_holdout_performed"])
        and numeric_prediction,
        "checkpoint_5363_freeze_passes_and_sources_are_current": holdout.get(
            "validation_passed"
        )
        is True
        and csv_passes(HOLDOUT_VALIDATION)
        and holdout_sources[0]
        and holdout_sources[1] > 0,
        "checkpoint_5371_runner_setup_passes_and_sources_are_current": runner.get(
            "validation_passed"
        )
        is True
        and runner.get("epsilon_id") == EPSILON_ID
        and csv_passes(RUNNER_VALIDATION)
        and runner_sources[0]
        and runner_sources[1] > 0,
        "accepted_E020_measurement_is_absent_at_freeze": measurement_absent,
        "radius_sum_comparison_rule_is_frozen": COMPARISON_RULE
        == "ABS_MEASURED_MINUS_FROZEN_PREDICTION_LE_RADIUS_SUM",
        "broad_claims_are_locked_false": all(value is False for value in false_claims().values()),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    validations = [validation_row(key, value, value) for key, value in checks.items()]
    passed = all(checks.values())
    claims = {CLAIM_CONTRACT: passed, CLAIM_COMPATIBILITY: False, **false_claims()}
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E020-blind-holdout-comparison-contract",
        "validation_passed": passed,
        "decision": (
            "D4_E020_BLIND_HOLDOUT_COMPARISON_FROZEN__AWAIT_ACCEPTED_MEASUREMENT"
            if passed
            else "D4_E020_BLIND_HOLDOUT_COMPARISON_CONTRACT_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "measurement_absent_at_freeze": measurement_absent,
        "comparison_executed": False,
        "comparison_rule": COMPARISON_RULE,
        "frozen_prediction_source_sha256": digest(HOLDOUT_ROWS),
        "runner_setup_sha256": digest(RUNNER_RESULT),
        "runner_node_plan_sha256": runner["node_plan_sha256"],
        "claim_boundary": claims,
        "holdout_source_drifts": holdout_sources[2],
        "runner_source_drifts": runner_sources[2],
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in required
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(CONTRACT_VALIDATION, validations)
    atomic_csv(CONTRACT_SOURCES, source_rows)
    atomic_json(CONTRACT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "frozen_waiting_measurement" if passed else "blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return payload


def comparison_preflight() -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    required = (
        CONTRACT,
        CONTRACT_VALIDATION,
        CONTRACT_SOURCES,
        MEASUREMENT_FINITE,
        MEASUREMENT_RESULT,
        MEASUREMENT_VALIDATION,
        MEASUREMENT_SEMANTIC_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    contract = read_json(CONTRACT)
    measurement = read_json(MEASUREMENT_RESULT)
    finite_rows = read_csv(MEASUREMENT_FINITE)
    contract_sources = source_register_current(CONTRACT_SOURCES)
    measurement_sources = result_sources_current(measurement)
    finite = finite_rows[0] if len(finite_rows) == 1 else {}
    expected_plan = contract.get("runner_node_plan_sha256")
    plan_counts = measurement.get("node_plan_sha256_counts", {})
    broad_claims = measurement.get("claim_boundary", {})
    checks = {
        "premeasurement_contract_passes_and_is_current": contract.get(
            "validation_passed"
        )
        is True
        and contract.get("measurement_absent_at_freeze") is True
        and contract.get("comparison_executed") is False
        and contract.get("comparison_rule") == COMPARISON_RULE
        and contract.get("frozen_prediction_source_sha256") == digest(HOLDOUT_ROWS)
        and csv_passes(CONTRACT_VALIDATION)
        and contract_sources[0]
        and contract_sources[1] > 0,
        "accepted_E020_measurement_is_unique_and_valid": len(finite_rows) == 1
        and finite.get("epsilon_id") == EPSILON_ID
        and abs(float(finite.get("epsilon", math.nan)) - EPSILON) <= 1.0e-16
        and parse_bool(finite.get("finite_regulator_fixed_decay_integral_accepted", False))
        and parse_bool(finite.get("valid_for_D4_outer_E020_fixed_decay_integral", False))
        and measurement.get("acceptance_passed") is True
        and measurement.get("completed_full_run") is True
        and int(measurement.get("failed_inner_node_count", -1)) == 0
        and measurement.get("all_adaptive_leaf_gates_pass") is True
        and csv_passes(MEASUREMENT_VALIDATION)
        and csv_passes(MEASUREMENT_SEMANTIC_VALIDATION),
        "accepted_measurement_uses_frozen_node_plan": set(plan_counts) == {expected_plan}
        and sum(int(value) for value in plan_counts.values())
        == int(measurement.get("encountered_node_count", -1)),
        "accepted_measurement_sources_are_current": measurement_sources[0]
        and measurement_sources[1] > 0,
        "measurement_broad_claims_remain_false": all(
            broad_claims.get(field) is not True for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"E020 comparison preflight failed: {checks}; contract drifts={contract_sources[2]}; measurement drifts={measurement_sources[2]}"
        )
    return contract, measurement, finite


def compare() -> dict[str, Any]:
    contract, measurement, finite = comparison_preflight()
    prediction = prediction_row()
    predicted = complex(
        float(prediction["predicted_fixed_decay_integral_real"]),
        float(prediction["predicted_fixed_decay_integral_imaginary"]),
    )
    measured = complex(
        float(finite["fixed_decay_integral_real"]),
        float(finite["fixed_decay_integral_imaginary"]),
    )
    prediction_radius = float(prediction["prediction_total_disk_radius"])
    measurement_radius = float(finite["total_error_absolute_conservative"])
    residual = measured - predicted
    separation = abs(residual)
    combined_radius = prediction_radius + measurement_radius
    compatible = separation <= combined_radius
    validations = [
        validation_row(
            "premeasurement_contract_is_preserved",
            contract.get("measurement_absent_at_freeze") is True,
            contract["updated_utc"],
        ),
        validation_row(
            "comparison_uses_radius_sum_rule",
            combined_radius == prediction_radius + measurement_radius,
            COMPARISON_RULE,
        ),
        validation_row(
            "comparison_outputs_are_finite",
            all(
                math.isfinite(value)
                for value in (
                    predicted.real,
                    predicted.imag,
                    measured.real,
                    measured.imag,
                    separation,
                    combined_radius,
                )
            )
            and combined_radius > 0.0,
            separation,
        ),
        validation_row(
            "broad_claims_remain_false",
            all(value is False for value in false_claims().values()),
            false_claims(),
        ),
        validation_row(
            "formal_workbench_unchanged",
            formal_inventory_digest() == FORMAL_DIGEST,
            formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_CONTRACT: passed,
        CLAIM_COMPATIBILITY: passed and compatible,
        **false_claims(),
    }
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E020-blind-holdout-comparison",
        "validation_passed": passed,
        "decision": (
            "D4_E020_FROZEN_BLIND_HOLDOUT_COMPATIBLE__PROCEED_TO_SEVEN_RUNG_GATE"
            if passed and compatible
            else "D4_E020_FROZEN_BLIND_HOLDOUT_INCOMPATIBLE__DO_NOT_RUN_LIMIT_GATE"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "comparison_executed": True,
        "comparison_rule": COMPARISON_RULE,
        "predicted_real": predicted.real,
        "predicted_imaginary": predicted.imag,
        "prediction_disk_radius": prediction_radius,
        "measured_real": measured.real,
        "measured_imaginary": measured.imag,
        "measurement_disk_radius": measurement_radius,
        "residual_real": residual.real,
        "residual_imaginary": residual.imag,
        "centre_separation": separation,
        "combined_disk_radius": combined_radius,
        "normalized_disk_separation": separation / combined_radius,
        "disk_margin": combined_radius - separation,
        "holdout_compatible": compatible,
        "contract_sha256": digest(CONTRACT),
        "measurement_result_sha256": digest(MEASUREMENT_RESULT),
        "claim_boundary": claims,
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    final_sources = tuple(dict.fromkeys((*contract_source_paths(), CONTRACT, CONTRACT_VALIDATION, CONTRACT_SOURCES, MEASUREMENT_FINITE, MEASUREMENT_RESULT, MEASUREMENT_VALIDATION, MEASUREMENT_SEMANTIC_VALIDATION)))
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in final_sources
    ]
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return payload


def validate_saved() -> dict[str, Any]:
    required = (RESULT, VALIDATION, SOURCE_REGISTER, CONTRACT, CONTRACT_VALIDATION, CONTRACT_SOURCES)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    payload = read_json(RESULT)
    sources = source_register_current(SOURCE_REGISTER)
    contract_sources = source_register_current(CONTRACT_SOURCES)
    checks = {
        "saved_result_validates": payload.get("validation_passed") is True,
        "saved_validation_passes": csv_passes(VALIDATION),
        "saved_sources_are_current": sources[0] and sources[1] > 0,
        "frozen_contract_sources_are_current": contract_sources[0]
        and contract_sources[1] > 0,
        "broad_claims_remain_false": all(
            payload.get("claim_boundary", {}).get(field) is False for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "validation_passed": all(checks.values()),
        "decision": "D4_E020_BLIND_COMPARISON_VALIDATED" if all(checks.values()) else "D4_E020_BLIND_COMPARISON_VALIDATION_FAILED",
        "checks": checks,
        "source_drifts": sources[2],
        "contract_source_drifts": contract_sources[2],
        "holdout_compatible": payload.get("holdout_compatible"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("freeze", "compare", "validate"), required=True)
    arguments = parser.parse_args()
    set_below_normal_priority()
    if arguments.mode == "freeze":
        payload = freeze_contract()
    elif arguments.mode == "compare":
        payload = compare()
    else:
        payload = validate_saved()
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("validation_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
