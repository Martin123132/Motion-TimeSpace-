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
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5361"
DOCUMENT = POST / "5361-Y5-R2FR-D4-E005-frozen-holdout-and-three-rung-curvature-gate.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5361_VALIDATION.csv"

RESULT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
VALIDATION_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_validation.csv"
SOURCE_REGISTER_5360 = FUNCTIONAL_RG / "5360" / "source_register.csv"
PREDICTION_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_E005_frozen_prediction.csv"
RUNGS_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_log_subtracted_rungs.csv"
SNAPSHOT_5360 = FUNCTIONAL_RG / "5360" / "D4_E005_pre_measurement_execution_snapshot.csv"

E005 = FUNCTIONAL_RG / "5334" / "E005"
E005_STATUS = E005 / "status.json"
E005_DRY_RUN = E005 / "D4_outer_event_aligned_E005_dry_run.json"
E005_EVENTS = E005 / "D4_outer_refined_support_events.csv"
E005_FINITE = E005 / "D4_outer_event_aligned_E005_finite_value.csv"
E005_RESULT = E005 / "D4_outer_event_aligned_E005_result.json"
E005_VALIDATION = E005 / "D4_outer_event_aligned_E005_validation.csv"
E005_RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5334_E005_VALIDATION.csv"

CHECKPOINT = 5361
MARKER = "MTS_5361_D4_E005_FROZEN_HOLDOUT_AND_THREE_RUNG_CURVATURE_GATE"
REVISION = "D4-E005-frozen-holdout-three-rung-curvature-gate-v1"
CHECKED_DATE = "2026-08-12"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EXPECTED_E005_PLAN_SHA256 = "dbc0979e72a9db04ed6b892d6e466f5323567af487c021487651b1ee06262049"
EPSILON_REFERENCE = 0.0025
EPSILON_H = 0.00125
EXPECTED_EVENT_COORDINATES = {
    "E02": 0.8088885244418536,
    "E08": 0.8708639340229474,
}

CLAIM_HOLDOUT = "valid_for_D4_E005_fixed_A_holdout_compatibility"
CLAIM_CURVATURE = "valid_for_D4_three_rung_composite_curvature_measurement"
FALSE_CLAIMS = (
    "valid_for_D4_separate_C_and_D_coefficients",
    "valid_for_D4_numeric_remainder_bound",
    "valid_for_D4_integral_six_rung_complete_second_order_fit",
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
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row["passed"]) for row in rows)


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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def no_broad_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    if not path.is_file():
        return False, 0, [str(path)]
    rows = read_csv(path)
    drifts = [
        row["path"]
        for row in rows
        if not Path(row["path"]).is_file()
        or digest(Path(row["path"])) != row["sha256"]
    ]
    return bool(rows) and not drifts, len(rows), drifts


def accepted_e005_contract() -> tuple[bool, dict[str, Any]]:
    required = (
        E005_STATUS,
        E005_DRY_RUN,
        E005_EVENTS,
        E005_FINITE,
        E005_RESULT,
        E005_VALIDATION,
        E005_RESIDUAL_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return False, {"missing": missing}
    status = read_json(E005_STATUS)
    dry = read_json(E005_DRY_RUN)
    events = read_csv(E005_EVENTS)
    finite_rows = read_csv(E005_FINITE)
    result = read_json(E005_RESULT)
    event_by_id = {row["event_id"]: row for row in events}
    checks = {
        "status_is_complete_diagnostic": status.get("state") == "COMPLETE_DIAGNOSTIC",
        "result_is_complete_and_accepted": result.get("completed_full_run") is True
        and result.get("acceptance_passed") is True,
        "one_finite_row_is_accepted": len(finite_rows) == 1
        and parse_bool(
            finite_rows[0].get(
                "finite_regulator_fixed_decay_integral_accepted", False
            )
        )
        and parse_bool(
            finite_rows[0].get("valid_for_D4_outer_E005_fixed_decay_integral", False)
        ),
        "conservative_budget_is_below_one_percent": len(finite_rows) == 1
        and float(finite_rows[0].get("total_error_relative_conservative", math.inf))
        <= 1.0e-2,
        "eight_event_dry_contract_is_exact": dry.get("acceptance_passed") is True
        and int(dry.get("refined_event_count", -1)) == 8
        and int(dry.get("initial_segment_count", -1)) == 26
        and int(dry.get("maximum_adaptive_depth", -1)) == 6
        and dry.get("node_plan_sha256") == EXPECTED_E005_PLAN_SHA256
        and dry.get("event_source_mode") == "CHECKPOINT_5337_EIGHT_EVENT_TRANSFER",
        "missing_contacts_are_explicit": len(events) == 8
        and all(
            event_id in event_by_id
            and abs(
                float(event_by_id[event_id]["event_coordinate"])
                - expected_coordinate
            )
            <= 1.0e-14
            for event_id, expected_coordinate in EXPECTED_EVENT_COORDINATES.items()
        ),
        "target_validation_passes": csv_validation_passes(E005_VALIDATION)
        and csv_validation_passes(E005_RESIDUAL_VALIDATION),
    }
    return all(checks.values()), {
        "checks": checks,
        "status": status,
        "dry": dry,
        "finite": finite_rows[0] if finite_rows else {},
        "result": result,
    }


def preflight() -> dict[str, Any]:
    required = (
        Path(__file__).resolve(),
        RESULT_5360,
        VALIDATION_5360,
        SOURCE_REGISTER_5360,
        PREDICTION_5360,
        RUNGS_5360,
        SNAPSHOT_5360,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    result_5360 = read_json(RESULT_5360)
    prediction_rows = read_csv(PREDICTION_5360)
    snapshots = read_csv(SNAPSHOT_5360)
    source_current, source_count, source_drifts = source_register_current(
        SOURCE_REGISTER_5360
    )
    e005_valid, e005_detail = accepted_e005_contract()
    checks = {
        "checkpoint_5360_preregistration_passes": result_5360.get(
            "validation_passed"
        )
        is True
        and result_5360.get("E005_measurement_comparison_performed") is False
        and csv_validation_passes(VALIDATION_5360),
        "checkpoint_5360_sources_remain_current": source_current
        and source_count > 0,
        "prediction_was_frozen_without_measurement": len(prediction_rows) == 1
        and parse_bool(prediction_rows[0]["frozen_before_accepted_E005_value"])
        and not parse_bool(
            prediction_rows[0]["comparison_to_measured_E005_performed"]
        )
        and len(snapshots) == 1
        and not parse_bool(
            snapshots[0]["accepted_E005_numeric_value_read_by_checkpoint"]
        ),
        "E005_measurement_is_now_independently_accepted": e005_valid,
        "formal_workbench_inventory_unchanged": formal_inventory_digest()
        == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "checkpoint_5360_source_count": source_count,
        "checkpoint_5360_source_drifts": source_drifts,
        "E005_detail": e005_detail,
    }


def evaluate_holdout() -> dict[str, Any]:
    prediction_row = read_csv(PREDICTION_5360)[0]
    rung_rows = sorted(read_csv(RUNGS_5360), key=lambda row: float(row["epsilon"]))
    finite = read_csv(E005_FINITE)[0]
    result_5360 = read_json(RESULT_5360)
    prediction = complex(
        float(prediction_row["predicted_fixed_decay_integral_real"]),
        float(prediction_row["predicted_fixed_decay_integral_imaginary"]),
    )
    prediction_radius = float(prediction_row["prediction_total_disk_radius"])
    measured = complex(
        float(finite["fixed_decay_integral_real"]),
        float(finite["fixed_decay_integral_imaginary"]),
    )
    measured_radius = float(finite["total_error_absolute_conservative"])
    residual = measured - prediction
    combined_radius = prediction_radius + measured_radius
    separation = abs(residual)
    compatible = separation <= combined_radius

    coefficient = complex(
        float(result_5360["A_zero_real"]),
        float(result_5360["A_zero_imaginary"]),
    )
    coefficient_radius = float(result_5360["A_zero_disk_radius"])
    epsilon_3 = float(finite["epsilon"])
    correction_3 = coefficient * epsilon_3 * math.log(
        epsilon_3 / EPSILON_REFERENCE
    )
    corrected_3 = measured - correction_3
    corrected_3_radius = measured_radius + abs(
        epsilon_3 * math.log(epsilon_3 / EPSILON_REFERENCE)
    ) * coefficient_radius
    corrected = [
        complex(
            float(row["derived_A_log_subtracted_J_real"]),
            float(row["derived_A_log_subtracted_J_imaginary"]),
        )
        for row in rung_rows
    ]
    corrected_radii = [
        float(row["derived_A_log_subtracted_disk_radius"]) for row in rung_rows
    ]
    affine_prediction = -2.0 * corrected[0] + 3.0 * corrected[1]
    corrected_residual = corrected_3 - affine_prediction
    affine_radius = 2.0 * corrected_radii[0] + 3.0 * corrected_radii[1]
    corrected_combined_radius = corrected_3_radius + affine_radius
    composite_curvature = corrected_residual / EPSILON_H**2
    composite_curvature_radius = corrected_combined_radius / EPSILON_H**2
    divided_difference = composite_curvature / 6.0
    divided_difference_radius = composite_curvature_radius / 6.0
    identity_error = abs(corrected_residual - residual)
    identity_tolerance = 64.0 * math.ulp(max(abs(residual), 1.0))

    return {
        "prediction": prediction,
        "prediction_radius": prediction_radius,
        "measured": measured,
        "measured_radius": measured_radius,
        "residual": residual,
        "separation": separation,
        "combined_radius": combined_radius,
        "disk_margin": combined_radius - separation,
        "compatible": compatible,
        "corrected_3": corrected_3,
        "corrected_3_radius": corrected_3_radius,
        "affine_prediction": affine_prediction,
        "affine_radius": affine_radius,
        "corrected_residual": corrected_residual,
        "corrected_combined_radius": corrected_combined_radius,
        "composite_curvature": composite_curvature,
        "composite_curvature_radius": composite_curvature_radius,
        "divided_difference": divided_difference,
        "divided_difference_radius": divided_difference_radius,
        "identity_error": identity_error,
        "identity_tolerance": identity_tolerance,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5361 - D4 E005 frozen holdout and three-rung curvature gate",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Blind comparison",
        "",
        "Checkpoint 5360 froze the E005 prediction using only E00125 and E0025. This checkpoint reads E005 only after its independent eight-event integration and validation pass.",
        "",
        f"- frozen prediction: `{result['predicted_real']:.17g} {result['predicted_imaginary']:+.17g} i`, disk `{result['prediction_disk_radius']:.17g}`;",
        f"- measured E005: `{result['measured_real']:.17g} {result['measured_imaginary']:+.17g} i`, disk `{result['measurement_disk_radius']:.17g}`;",
        f"- centre separation: `{result['centre_separation']:.17g}`;",
        f"- combined disk radius: `{result['combined_disk_radius']:.17g}`;",
        f"- compatibility: `{result['holdout_compatible']}`.",
        "",
        "## Derived curvature combination",
        "",
        "For dyadic regulators `(h,2h,4h)` with `h=0.00125`, define `J=I-A epsilon Log(epsilon/0.0025)`. The preregistered affine residual is exactly",
        "",
        "`Delta3 = J(4h)+2J(h)-3J(2h)`.",
        "",
        "For the complete second-order normal form this obeys",
        "",
        "`Delta3/h^2 = 14 Log(2) C + 6 D + [R3(4h)+2R3(h)-3R3(2h)]/h^2`.",
        "",
        f"The measured composite curvature is `{result['composite_curvature_real']:.17g} {result['composite_curvature_imaginary']:+.17g} i` with conservative disk `{result['composite_curvature_disk_radius']:.17g}`.",
        "",
        "## Claim boundary",
        "",
        "This is a genuine frozen leading-family holdout and one measured composite curvature combination. Three rungs cannot separate `C` from `D`, cannot numerically upper-bound `R3`, and cannot establish the regulator-zero limit. More accepted rungs remain mandatory.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    evaluation = evaluate_holdout()
    compatibility = bool(evaluation["compatible"])
    validations = [
        validation_row("preflight_passes", True, preflight_result["checks"]),
        validation_row(
            "frozen_and_corrected_residuals_are_identical",
            evaluation["identity_error"] <= evaluation["identity_tolerance"],
            (evaluation["identity_error"], evaluation["identity_tolerance"]),
        ),
        validation_row(
            "disk_comparison_uses_conservative_radius_sum",
            evaluation["combined_radius"]
            == evaluation["prediction_radius"] + evaluation["measured_radius"]
            and evaluation["combined_radius"] > 0.0,
            evaluation["combined_radius"],
        ),
        validation_row(
            "three_rung_curvature_is_finite",
            math.isfinite(evaluation["composite_curvature"].real)
            and math.isfinite(evaluation["composite_curvature"].imag)
            and math.isfinite(evaluation["composite_curvature_radius"]),
            evaluation["composite_curvature"],
        ),
        validation_row(
            "three_rungs_do_not_overclaim_complete_family",
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
        CLAIM_HOLDOUT: passed and compatibility,
        CLAIM_CURVATURE: passed,
        **no_broad_claims(),
    }
    comparison = {
        "holdout_epsilon_id": "E005",
        "holdout_epsilon": 0.005,
        **complex_fields("predicted", evaluation["prediction"]),
        "prediction_disk_radius": evaluation["prediction_radius"],
        **complex_fields("measured", evaluation["measured"]),
        "measurement_disk_radius": evaluation["measured_radius"],
        **complex_fields("measurement_minus_prediction", evaluation["residual"]),
        "centre_separation": evaluation["separation"],
        "combined_disk_radius": evaluation["combined_radius"],
        "disk_margin": evaluation["disk_margin"],
        "holdout_compatible": compatibility,
        "comparison_rule": "ABS_MEASURED_MINUS_FROZEN_PREDICTION_LE_RADIUS_SUM",
        **claims,
    }
    curvature = {
        "epsilon_h": EPSILON_H,
        "identity": "DELTA3_OVER_H2_EQUALS_14_LOG2_C_PLUS_6_D_PLUS_REMAINDER_COMBINATION",
        **complex_fields("corrected_E005", evaluation["corrected_3"]),
        "corrected_E005_disk_radius": evaluation["corrected_3_radius"],
        **complex_fields("affine_corrected_prediction", evaluation["affine_prediction"]),
        "affine_corrected_prediction_disk_radius": evaluation["affine_radius"],
        **complex_fields("delta3", evaluation["corrected_residual"]),
        "delta3_disk_radius": evaluation["corrected_combined_radius"],
        **complex_fields("composite_curvature", evaluation["composite_curvature"]),
        "composite_curvature_disk_radius": evaluation["composite_curvature_radius"],
        **complex_fields("second_divided_difference", evaluation["divided_difference"]),
        "second_divided_difference_disk_radius": evaluation[
            "divided_difference_radius"
        ],
        "C_and_D_separately_identifiable": False,
        "numeric_R3_upper_bound_available": False,
        **claims,
    }
    direct_sources = (
        Path(__file__).resolve(),
        RESULT_5360,
        VALIDATION_5360,
        SOURCE_REGISTER_5360,
        PREDICTION_5360,
        RUNGS_5360,
        SNAPSHOT_5360,
        E005_STATUS,
        E005_DRY_RUN,
        E005_EVENTS,
        E005_FINITE,
        E005_RESULT,
        E005_VALIDATION,
        E005_RESIDUAL_VALIDATION,
    )
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in direct_sources
    ]
    result = {
        "mode": "D4-E005-frozen-holdout-and-three-rung-curvature-gate",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "validation_passed": passed,
        "decision": (
            "D4_E005_FROZEN_HOLDOUT_COMPATIBLE__ACQUIRE_E010_FOR_COMPLETE_FIXED_A_FAMILY"
            if compatibility
            else "D4_E005_FROZEN_HOLDOUT_INCOMPATIBLE__RETAIN_SECOND_ORDER_TERMS_AND_ACQUIRE_E010"
        ),
        "holdout_compatible": compatibility,
        "predicted_real": evaluation["prediction"].real,
        "predicted_imaginary": evaluation["prediction"].imag,
        "prediction_disk_radius": evaluation["prediction_radius"],
        "measured_real": evaluation["measured"].real,
        "measured_imaginary": evaluation["measured"].imag,
        "measurement_disk_radius": evaluation["measured_radius"],
        "centre_separation": evaluation["separation"],
        "combined_disk_radius": evaluation["combined_radius"],
        "disk_margin": evaluation["disk_margin"],
        "composite_curvature_real": evaluation["composite_curvature"].real,
        "composite_curvature_imaginary": evaluation["composite_curvature"].imag,
        "composite_curvature_disk_radius": evaluation[
            "composite_curvature_radius"
        ],
        "claim_boundary": claims,
        "remaining_obstruction": "accept at least E010 and further source-complete rungs to separate second-order coefficients and bound the analytic remainder",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_E005_frozen_holdout_comparison.csv", [comparison])
    atomic_csv(output / "D4_three_rung_fixed_A_curvature_combination.csv", [curvature])
    atomic_csv(output / "D4_E005_holdout_validation.csv", validations)
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_E005_holdout_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result)
    return result


def validate_saved(output: Path) -> dict[str, Any]:
    validation_path = output / "D4_E005_holdout_validation.csv"
    result_path = output / "D4_E005_holdout_result.json"
    source_path = output / "source_register.csv"
    source_current, source_count, source_drifts = source_register_current(source_path)
    result = read_json(result_path) if result_path.is_file() else {}
    checks = {
        "validation_file_passes": validation_path.is_file()
        and csv_validation_passes(validation_path),
        "residual_validation_passes": VALIDATION.is_file()
        and csv_validation_passes(VALIDATION),
        "result_validation_passes": result.get("validation_passed") is True,
        "registered_sources_are_current": source_current and source_count > 0,
        "document_exists": DOCUMENT.is_file(),
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
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        payload = preflight()
    elif arguments.validate_saved:
        payload = validate_saved(arguments.output_dir)
    else:
        payload = run(arguments.output_dir)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
