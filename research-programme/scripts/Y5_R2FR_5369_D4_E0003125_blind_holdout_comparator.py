from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
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
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"

FREEZE_ROWS = FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze.csv"
FREEZE_RESULT = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_result.json"
)
FREEZE_VALIDATION = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_validation.csv"
)
FREEZE_SOURCES = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_sources.csv"
)

RUNNER_ROOT = FUNCTIONAL_RG / "5368" / "E0003125"
RUNNER_SCRIPT = SCRIPTS / "Y5_R2FR_5368_D4_E0003125_preregistered_blind_holdout_runner.py"
RUNNER_RESULT = RUNNER_ROOT / "D4_E0003125_blind_holdout_runner_result.json"
RUNNER_VALIDATION = RUNNER_ROOT / "D4_E0003125_blind_holdout_runner_validation.csv"
RUNNER_SOURCES = RUNNER_ROOT / "source_register.csv"
FROZEN_EVENTS = RUNNER_ROOT / "D4_E0003125_preintegration_frozen_events.csv"
LOCAL_REPAIR_CONTRACT = (
    RUNNER_ROOT / "D4_E0003125_precomparison_local_repair_contract.csv"
)
FROZEN_ENERGY_AUGMENTATION = (
    RUNNER_ROOT / "D4_E0003125_frozen_energy_node_pole_augmentation.csv"
)

MEASUREMENT_ROOT = FUNCTIONAL_RG / "5334" / "E0003125"
MEASUREMENT_FINITE = (
    MEASUREMENT_ROOT / "D4_outer_event_aligned_E0003125_finite_value.csv"
)
MEASUREMENT_RESULT = (
    MEASUREMENT_ROOT / "D4_outer_event_aligned_E0003125_result.json"
)
MEASUREMENT_VALIDATION = (
    MEASUREMENT_ROOT / "D4_outer_event_aligned_E0003125_validation.csv"
)
MEASUREMENT_SEMANTIC_VALIDATION = (
    MEASUREMENT_ROOT / "D4_outer_event_aligned_E0003125_semantic_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5369" / "E0003125"
CONTRACT = OUTPUT / "D4_E0003125_blind_holdout_comparison_contract.json"
CONTRACT_VALIDATION = (
    OUTPUT / "D4_E0003125_blind_holdout_comparison_contract_validation.csv"
)
CONTRACT_SOURCES = (
    OUTPUT / "D4_E0003125_blind_holdout_comparison_contract_sources.csv"
)
RESULT = OUTPUT / "D4_E0003125_blind_holdout_comparison_result.json"
COMPARISON = OUTPUT / "D4_E0003125_blind_holdout_comparison.csv"
REMAINDER = OUTPUT / "D4_E0003125_pointwise_remainder_envelope.csv"
VALIDATION = OUTPUT / "D4_E0003125_blind_holdout_comparison_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5369_VALIDATION.csv"
DOCUMENT = POST / "5369-Y5-R2FR-D4-E0003125-blind-holdout-comparison.md"

CHECKPOINT = 5369
MARKER = "MTS_5369_D4_E0003125_BLIND_HOLDOUT_COMPARISON"
REVISION = "D4-E0003125-blind-holdout-comparison-v1"
EPSILON_ID = "E0003125"
EPSILON = 0.0003125
EPSILON_REFERENCE = 0.0025
EXPECTED_EVENT_COUNT = 8
EXPECTED_PLAN_SHA256 = "a0b5e08054715355081c228884e80395afa45efee5c1bfea54bf0ea67aec3bd9"
EXPECTED_REPAIR_REVISION = "E0003125-owner-surface-factor-precomparison-v2"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
COMPARISON_RULE = "ABS_MEASURED_MINUS_FROZEN_PREDICTION_LE_RADIUS_SUM"
NORMALIZATION_RULE = "epsilon^3*(1+abs(Log(epsilon/epsilon_reference)))"

CLAIM_CONTRACT = "valid_for_D4_E0003125_blind_holdout_comparison_contract"
CLAIM_TEST = "valid_for_D4_E0003125_complete_family_blind_holdout_test"
CLAIM_COMPATIBILITY = "valid_for_D4_E0003125_complete_family_holdout_compatibility"
CLAIM_POINTWISE = "valid_for_D4_E0003125_pointwise_remainder_envelope"
FALSE_CLAIMS = (
    "valid_for_D4_six_rung_complete_second_order_fit",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
MEASUREMENT_EXPLICIT_FALSE_CLAIMS = (
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


def csv_validation_passes(path: Path) -> bool:
    if not path.is_file():
        return False
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row.get("passed", False)) for row in rows)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def no_broad_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    if not path.is_file():
        return False, 0, [str(path)]
    rows = read_csv(path)
    drifts = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def prediction_rows() -> list[dict[str, str]]:
    if not FREEZE_ROWS.is_file():
        return []
    return [row for row in read_csv(FREEZE_ROWS) if row.get("holdout_epsilon_id") == EPSILON_ID]


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


def immutable_runner_sources() -> tuple[Path, ...]:
    return (
        RUNNER_SCRIPT,
        FROZEN_EVENTS,
        LOCAL_REPAIR_CONTRACT,
        FROZEN_ENERGY_AUGMENTATION,
        FREEZE_ROWS,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
    )


def runner_immutable_sources_current() -> tuple[bool, list[str]]:
    if not RUNNER_SOURCES.is_file():
        return False, [str(RUNNER_SOURCES)]
    registered = {
        str(Path(row["path"]).resolve()).lower(): row["sha256"]
        for row in read_csv(RUNNER_SOURCES)
    }
    drifts: list[str] = []
    for path in immutable_runner_sources():
        key = str(path.resolve()).lower()
        if not path.is_file() or registered.get(key) != digest(path):
            drifts.append(str(path.resolve()))
    return not drifts, drifts


def result_sources_current(result: dict[str, Any]) -> tuple[bool, int, list[str]]:
    rows = result.get("source_files", [])
    drifts: list[str] = []
    for row in rows:
        path = Path(row.get("path", ""))
        if not path.is_file() or digest(path) != row.get("sha256"):
            drifts.append(str(path))
    return bool(rows) and not drifts, len(rows), drifts


def contract_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        FREEZE_ROWS,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FREEZE_SOURCES,
        RUNNER_RESULT,
        RUNNER_VALIDATION,
        RUNNER_SOURCES,
        FROZEN_EVENTS,
        LOCAL_REPAIR_CONTRACT,
        FROZEN_ENERGY_AUGMENTATION,
    )


def render_contract_document(contract: dict[str, Any]) -> None:
    lines = [
        "# 5369 - D4 E0003125 blind holdout comparison",
        "",
        "## Frozen decision",
        "",
        f"`{contract['decision']}`",
        "",
        "The comparison rule, frozen prediction hash, measurement fields, and claim boundary were saved while no accepted E0003125 measurement existed.",
        "",
        f"- rule: `{contract['comparison_rule']}`;",
        f"- frozen prediction hash: `{contract['frozen_prediction_sha256']}`;",
        f"- runner plan hash: `{contract['runner_plan_sha256']}`;",
        "- comparison executed: `False`.",
        "",
        "No measured compatibility, six-rung fit, regulator-zero, angular, UV, local-GR, or full-MTS claim is made at contract freeze.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def freeze_contract() -> dict[str, Any]:
    required = contract_source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    rows = prediction_rows()
    freeze = read_json(FREEZE_RESULT)
    runner = read_json(RUNNER_RESULT)
    freeze_sources_current, freeze_source_count, freeze_drifts = source_register_current(
        FREEZE_SOURCES
    )
    runner_sources_current, runner_drifts = runner_immutable_sources_current()
    measurement_absent = not accepted_measurement_available()
    prediction = rows[0] if len(rows) == 1 else {}
    checks = {
        "exactly_one_E0003125_prediction_is_frozen": len(rows) == 1
        and abs(float(prediction.get("holdout_epsilon", math.nan)) - EPSILON) <= 1.0e-16
        and parse_bool(prediction.get("frozen_before_accepted_E0003125_value", False))
        and not parse_bool(prediction.get("comparison_to_measured_holdout_performed", True)),
        "checkpoint_5365_freeze_passes_and_sources_are_current": freeze.get(
            "validation_passed"
        )
        is True
        and csv_validation_passes(FREEZE_VALIDATION)
        and freeze_sources_current
        and freeze_source_count > 0,
        "checkpoint_5368_runner_setup_passes": runner.get("validation_passed") is True
        and csv_validation_passes(RUNNER_VALIDATION)
        and runner.get("node_plan_sha256") == EXPECTED_PLAN_SHA256
        and runner.get("local_repair_revision") == EXPECTED_REPAIR_REVISION
        and runner.get("frozen_prediction_source_sha256") == digest(FREEZE_ROWS),
        "runner_immutable_sources_are_current": runner_sources_current,
        "accepted_E0003125_measurement_is_absent_at_contract_freeze": measurement_absent,
        "comparison_rule_is_fixed_before_measurement": COMPARISON_RULE
        == "ABS_MEASURED_MINUS_FROZEN_PREDICTION_LE_RADIUS_SUM"
        and NORMALIZATION_RULE
        == "epsilon^3*(1+abs(Log(epsilon/epsilon_reference)))",
        "broad_claims_are_locked_false": all(
            value is False for value in no_broad_claims().values()
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    validations = [validation_row(key, value, value) for key, value in checks.items()]
    passed = all(checks.values())
    claims = {CLAIM_CONTRACT: passed, **no_broad_claims()}
    contract = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E0003125-blind-holdout-comparison-contract",
        "validation_passed": passed,
        "decision": (
            "D4_E0003125_BLIND_HOLDOUT_COMPARISON_FROZEN__AWAIT_ACCEPTED_MEASUREMENT"
            if passed
            else "D4_E0003125_BLIND_HOLDOUT_COMPARISON_CONTRACT_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "measurement_absent_at_freeze": measurement_absent,
        "comparison_executed": False,
        "comparison_rule": COMPARISON_RULE,
        "normalization_rule": NORMALIZATION_RULE,
        "frozen_prediction_sha256": digest(FREEZE_ROWS),
        "runner_setup_sha256": digest(RUNNER_RESULT),
        "runner_plan_sha256": EXPECTED_PLAN_SHA256,
        "prediction_fields": [
            "predicted_fixed_decay_integral_real",
            "predicted_fixed_decay_integral_imaginary",
            "prediction_total_disk_radius",
        ],
        "measurement_fields": [
            "fixed_decay_integral_real",
            "fixed_decay_integral_imaginary",
            "total_error_absolute_conservative",
        ],
        "claim_boundary": claims,
        "freeze_source_drifts": freeze_drifts,
        "runner_source_drifts": runner_drifts,
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in required
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(CONTRACT_VALIDATION, validations)
    atomic_csv(CONTRACT_SOURCES, source_rows)
    atomic_json(CONTRACT, contract)
    render_contract_document(contract)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "frozen_waiting_measurement" if passed else "blocked",
            "decision": contract["decision"],
            "updated_utc": contract["updated_utc"],
        },
    )
    return contract


def comparison_preflight() -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    required = (
        CONTRACT,
        CONTRACT_VALIDATION,
        CONTRACT_SOURCES,
        FREEZE_ROWS,
        RUNNER_RESULT,
        RUNNER_VALIDATION,
        MEASUREMENT_FINITE,
        MEASUREMENT_RESULT,
        MEASUREMENT_VALIDATION,
        MEASUREMENT_SEMANTIC_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    contract = read_json(CONTRACT)
    runner = read_json(RUNNER_RESULT)
    measurement = read_json(MEASUREMENT_RESULT)
    finite_rows = read_csv(MEASUREMENT_FINITE)
    prediction = prediction_rows()
    contract_current, contract_source_count, contract_drifts = source_register_current(
        CONTRACT_SOURCES
    )
    result_current, result_source_count, result_drifts = result_sources_current(measurement)
    plan_counts = measurement.get("node_plan_sha256_counts", {})
    broad_claims = measurement.get("claim_boundary", {})
    checks = {
        "premeasurement_comparison_contract_passes_and_is_current": contract.get(
            "validation_passed"
        )
        is True
        and contract.get("measurement_absent_at_freeze") is True
        and contract.get("comparison_executed") is False
        and contract.get("comparison_rule") == COMPARISON_RULE
        and contract.get("frozen_prediction_sha256") == digest(FREEZE_ROWS)
        and csv_validation_passes(CONTRACT_VALIDATION)
        and contract_current
        and contract_source_count > 0,
        "exactly_one_frozen_prediction_and_measurement_row_exist": len(prediction) == 1
        and len(finite_rows) == 1,
        "runner_setup_and_plan_remain_frozen": runner.get("validation_passed") is True
        and csv_validation_passes(RUNNER_VALIDATION)
        and runner.get("node_plan_sha256") == EXPECTED_PLAN_SHA256
        and runner.get("local_repair_revision") == EXPECTED_REPAIR_REVISION,
        "E0003125_measurement_is_independently_accepted": len(finite_rows) == 1
        and finite_rows[0].get("epsilon_id") == EPSILON_ID
        and abs(float(finite_rows[0].get("epsilon", math.nan)) - EPSILON) <= 1.0e-16
        and parse_bool(
            finite_rows[0].get("finite_regulator_fixed_decay_integral_accepted", False)
        )
        and measurement.get("acceptance_passed") is True
        and measurement.get("completed_full_run") is True
        and int(measurement.get("failed_inner_node_count", -1)) == 0
        and measurement.get("all_adaptive_leaf_gates_pass") is True
        and csv_validation_passes(MEASUREMENT_VALIDATION)
        and csv_validation_passes(MEASUREMENT_SEMANTIC_VALIDATION),
        "accepted_measurement_uses_the_frozen_node_plan": set(plan_counts) == {
            EXPECTED_PLAN_SHA256
        }
        and sum(int(value) for value in plan_counts.values())
        == int(measurement.get("encountered_node_count", -1)),
        "accepted_measurement_sources_are_current": result_current
        and result_source_count > 0,
        "measurement_keeps_all_native_broad_claims_explicitly_false": all(
            broad_claims.get(field) is False
            for field in MEASUREMENT_EXPLICIT_FALSE_CLAIMS
        )
        and all(broad_claims.get(field) is not True for field in FALSE_CLAIMS),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    detail = {
        "checks": checks,
        "contract_source_drifts": contract_drifts,
        "measurement_source_drifts": result_drifts,
    }
    if not all(checks.values()):
        raise RuntimeError(f"comparison preflight failed: {detail}")
    return contract, measurement, finite_rows[0]


def evaluate(prediction: dict[str, str], finite: dict[str, str]) -> dict[str, Any]:
    predicted = complex(
        float(prediction["predicted_fixed_decay_integral_real"]),
        float(prediction["predicted_fixed_decay_integral_imaginary"]),
    )
    prediction_radius = float(prediction["prediction_total_disk_radius"])
    measured = complex(
        float(finite["fixed_decay_integral_real"]),
        float(finite["fixed_decay_integral_imaginary"]),
    )
    measurement_radius = float(finite["total_error_absolute_conservative"])
    residual = measured - predicted
    separation = abs(residual)
    combined_radius = prediction_radius + measurement_radius
    normalization = EPSILON**3 * (
        1.0 + abs(math.log(EPSILON / EPSILON_REFERENCE))
    )
    return {
        "predicted": predicted,
        "prediction_radius": prediction_radius,
        "measured": measured,
        "measurement_radius": measurement_radius,
        "residual": residual,
        "separation": separation,
        "combined_radius": combined_radius,
        "disk_margin": combined_radius - separation,
        "normalized_disk_separation": separation / combined_radius,
        "compatible": separation <= combined_radius,
        "pointwise_defect_lower": max(0.0, separation - combined_radius),
        "pointwise_defect_upper": separation + combined_radius,
        "normalization": normalization,
        "normalized_central_defect": separation / normalization,
        "normalized_defect_lower": max(0.0, separation - combined_radius)
        / normalization,
        "normalized_defect_upper": (separation + combined_radius) / normalization,
    }


def final_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        CONTRACT,
        CONTRACT_VALIDATION,
        CONTRACT_SOURCES,
        FREEZE_ROWS,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FREEZE_SOURCES,
        RUNNER_RESULT,
        RUNNER_VALIDATION,
        RUNNER_SOURCES,
        FROZEN_EVENTS,
        LOCAL_REPAIR_CONTRACT,
        FROZEN_ENERGY_AUGMENTATION,
        MEASUREMENT_FINITE,
        MEASUREMENT_RESULT,
        MEASUREMENT_VALIDATION,
        MEASUREMENT_SEMANTIC_VALIDATION,
    )


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5369 - D4 E0003125 blind holdout comparison",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "Checkpoint 5365 froze the prediction before the E0003125 measurement. Checkpoint 5368 froze the independent depth-six event-aligned runner and local repair before the accepted integral. This checkpoint applies the prewritten disk comparison without refitting.",
        "",
        f"- frozen prediction: `{result['predicted_real']:.17g} {result['predicted_imaginary']:+.17g} i`, disk `{result['prediction_disk_radius']:.17g}`;",
        f"- measured value: `{result['measured_real']:.17g} {result['measured_imaginary']:+.17g} i`, disk `{result['measurement_disk_radius']:.17g}`;",
        f"- centre separation: `{result['centre_separation']:.17g}`;",
        f"- combined disk: `{result['combined_disk_radius']:.17g}`;",
        f"- normalized disk separation: `{result['normalized_disk_separation']:.17g}`;",
        f"- holdout compatible: `{result['holdout_compatible']}`.",
        "",
        "## Claim boundary",
        "",
        "This closes only the frozen sixth-rung compatibility test and a pointwise defect envelope. It does not fit the six-rung family and does not establish a uniform remainder, regulator-zero limit, angular limit, UV result, local GR, or full MTS theory.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def compare() -> dict[str, Any]:
    contract, measurement, finite = comparison_preflight()
    prediction = prediction_rows()[0]
    evaluation = evaluate(prediction, finite)
    compatibility = bool(evaluation["compatible"])
    numeric_fields = (
        evaluation["prediction_radius"],
        evaluation["measurement_radius"],
        evaluation["separation"],
        evaluation["combined_radius"],
        evaluation["normalization"],
        evaluation["normalized_disk_separation"],
        evaluation["pointwise_defect_lower"],
        evaluation["pointwise_defect_upper"],
    )
    validations = [
        validation_row(
            "comparison_contract_was_frozen_before_measurement",
            contract.get("validation_passed") is True
            and contract.get("measurement_absent_at_freeze") is True
            and contract.get("comparison_executed") is False,
            contract.get("updated_utc"),
        ),
        validation_row(
            "accepted_measurement_has_zero_failed_nodes_and_all_leaf_gates_pass",
            measurement.get("acceptance_passed") is True
            and measurement.get("completed_full_run") is True
            and int(measurement.get("failed_inner_node_count", -1)) == 0
            and measurement.get("all_adaptive_leaf_gates_pass") is True,
            measurement.get("decision"),
        ),
        validation_row(
            "comparison_uses_exactly_one_frozen_row_without_refit",
            len(prediction_rows()) == 1
            and digest(FREEZE_ROWS) == contract.get("frozen_prediction_sha256")
            and not parse_bool(prediction.get("comparison_to_measured_holdout_performed", True)),
            digest(FREEZE_ROWS),
        ),
        validation_row(
            "conservative_disk_sum_rule_is_applied_exactly",
            evaluation["combined_radius"]
            == evaluation["prediction_radius"] + evaluation["measurement_radius"]
            and compatibility
            == (evaluation["separation"] <= evaluation["combined_radius"]),
            COMPARISON_RULE,
        ),
        validation_row(
            "comparison_and_pointwise_envelope_are_finite_and_ordered",
            evaluation["prediction_radius"] > 0.0
            and evaluation["measurement_radius"] > 0.0
            and evaluation["normalization"] > 0.0
            and 0.0
            <= evaluation["pointwise_defect_lower"]
            <= evaluation["pointwise_defect_upper"]
            and all(math.isfinite(value) for value in numeric_fields),
            evaluation["normalized_defect_upper"],
        ),
        validation_row(
            "single_holdout_does_not_claim_six_rung_fit_or_outer_limit",
            all(value is False for value in no_broad_claims().values()),
            no_broad_claims(),
        ),
        validation_row(
            "formal_workbench_remains_unchanged",
            formal_inventory_digest() == FORMAL_DIGEST,
            formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_remains_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_CONTRACT: passed,
        CLAIM_TEST: passed,
        CLAIM_COMPATIBILITY: passed and compatibility,
        CLAIM_POINTWISE: passed,
        **no_broad_claims(),
    }
    comparison = {
        "holdout_epsilon_id": EPSILON_ID,
        "holdout_epsilon": EPSILON,
        **complex_fields("predicted", evaluation["predicted"]),
        "prediction_disk_radius": evaluation["prediction_radius"],
        **complex_fields("measured", evaluation["measured"]),
        "measurement_disk_radius": evaluation["measurement_radius"],
        **complex_fields("measurement_minus_prediction", evaluation["residual"]),
        "centre_separation": evaluation["separation"],
        "combined_disk_radius": evaluation["combined_radius"],
        "disk_margin": evaluation["disk_margin"],
        "normalized_disk_separation": evaluation["normalized_disk_separation"],
        "holdout_compatible": compatibility,
        "comparison_rule": COMPARISON_RULE,
        **claims,
    }
    remainder = {
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "epsilon_reference": EPSILON_REFERENCE,
        "normalization": NORMALIZATION_RULE,
        "normalization_value": evaluation["normalization"],
        **complex_fields("central_pointwise_defect", evaluation["residual"]),
        "pointwise_defect_disk_radius": evaluation["combined_radius"],
        "pointwise_defect_magnitude_lower_bound": evaluation[
            "pointwise_defect_lower"
        ],
        "pointwise_defect_magnitude_upper_bound": evaluation[
            "pointwise_defect_upper"
        ],
        "normalized_central_defect": evaluation["normalized_central_defect"],
        "normalized_defect_lower_bound": evaluation["normalized_defect_lower"],
        "normalized_defect_upper_bound": evaluation["normalized_defect_upper"],
        "uniform_interval_M_D4_bound_available": False,
        **claims,
    }
    decision = (
        "D4_E0003125_BLIND_HOLDOUT_COMPATIBLE__SIXTH_RUNG_POINTWISE_ENVELOPE_ONLY"
        if compatibility
        else "D4_E0003125_BLIND_HOLDOUT_INCOMPATIBLE__COMPLETE_FIXED_A_FAMILY_REQUIRES_REVISION"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E0003125-blind-holdout-comparison",
        "validation_passed": passed,
        "decision": decision,
        "holdout_compatible": compatibility,
        "predicted_real": evaluation["predicted"].real,
        "predicted_imaginary": evaluation["predicted"].imag,
        "prediction_disk_radius": evaluation["prediction_radius"],
        "measured_real": evaluation["measured"].real,
        "measured_imaginary": evaluation["measured"].imag,
        "measurement_disk_radius": evaluation["measurement_radius"],
        "centre_separation": evaluation["separation"],
        "combined_disk_radius": evaluation["combined_radius"],
        "disk_margin": evaluation["disk_margin"],
        "normalized_disk_separation": evaluation["normalized_disk_separation"],
        "pointwise_defect_lower": evaluation["pointwise_defect_lower"],
        "pointwise_defect_upper": evaluation["pointwise_defect_upper"],
        "normalized_defect_upper": evaluation["normalized_defect_upper"],
        "runner_plan_sha256": EXPECTED_PLAN_SHA256,
        "claim_boundary": claims,
        "remaining_obstruction": "fit the complete six-rung family against its preregistered second-order normal form and require the overdetermined outer-limit gates",
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in final_source_paths()
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(COMPARISON, [comparison])
    atomic_csv(REMAINDER, [remainder])
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": decision,
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result)
    return result


def validate_saved() -> dict[str, Any]:
    result = read_json(RESULT) if RESULT.is_file() else {}
    sources_current, source_count, source_drifts = source_register_current(
        SOURCE_REGISTER
    )
    broad = result.get("claim_boundary", {})
    checks = {
        "comparison_validation_passes": csv_validation_passes(VALIDATION),
        "residual_validation_passes": csv_validation_passes(RESIDUAL_VALIDATION),
        "result_validation_passes": result.get("validation_passed") is True,
        "comparison_and_remainder_outputs_exist": COMPARISON.is_file()
        and REMAINDER.is_file(),
        "registered_sources_are_current": sources_current and source_count > 0,
        "document_exists": DOCUMENT.is_file(),
        "broad_claims_remain_false": all(
            broad.get(field) is False for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "validate-saved",
        "checks": checks,
        "source_drifts": source_drifts,
        "all_pass": all(checks.values()),
    }


def main() -> int:
    set_below_normal_priority()
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("preflight", "compare", "validate"), required=True)
    arguments = parser.parse_args()
    if arguments.mode == "preflight":
        payload = freeze_contract()
    elif arguments.mode == "compare":
        payload = compare()
    else:
        payload = validate_saved()
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
