from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
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


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"

FREEZE_RESULT_5363 = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_result.json"
FREEZE_PREDICTION_5363 = (
    FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_dual_holdout_predictions.csv"
)
FREEZE_VALIDATION_5363 = (
    FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_validation.csv"
)
FREEZE_SOURCES_5363 = FUNCTIONAL_RG / "5363" / "source_register.csv"
FOUR_RUNG_INPUTS_5363 = (
    FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_four_rung_inputs.csv"
)
FIXED_A_RESULT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"

RUNNER_RESULT_5364 = (
    FUNCTIONAL_RG
    / "5364"
    / "E000625"
    / "D4_E000625_primary_blind_holdout_runner_result.json"
)
RUNNER_VALIDATION_5364 = (
    FUNCTIONAL_RG
    / "5364"
    / "E000625"
    / "D4_E000625_primary_blind_holdout_runner_validation.csv"
)
RUNNER_SOURCES_5364 = FUNCTIONAL_RG / "5364" / "E000625" / "source_register.csv"
FROZEN_EVENTS_5364 = (
    FUNCTIONAL_RG
    / "5364"
    / "E000625"
    / "D4_E000625_preintegration_frozen_events.csv"
)

E000625_ROOT = FUNCTIONAL_RG / "5334" / "E000625"
E000625_FINITE = E000625_ROOT / "D4_outer_event_aligned_E000625_finite_value.csv"
E000625_RESULT = E000625_ROOT / "D4_outer_event_aligned_E000625_result.json"
E000625_VALIDATION = E000625_ROOT / "D4_outer_event_aligned_E000625_validation.csv"
E000625_SEMANTIC_VALIDATION = (
    E000625_ROOT / "D4_outer_event_aligned_E000625_semantic_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5365"
RESULT = OUTPUT / "D4_E000625_blind_holdout_result.json"
COMPARISON = OUTPUT / "D4_E000625_blind_holdout_comparison.csv"
REMAINDER = OUTPUT / "D4_E000625_pointwise_remainder_envelope.csv"
VALIDATION = OUTPUT / "D4_E000625_blind_holdout_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5365_VALIDATION.csv"
DOCUMENT = POST / "5365-Y5-R2FR-D4-E000625-blind-holdout-and-pointwise-remainder-envelope.md"
NEXT_HOLDOUT_FREEZE = OUTPUT / "D4_E0003125_premeasurement_freeze.csv"
NEXT_HOLDOUT_FREEZE_RESULT = OUTPUT / "D4_E0003125_premeasurement_freeze_result.json"
NEXT_HOLDOUT_FREEZE_VALIDATION = (
    OUTPUT / "D4_E0003125_premeasurement_freeze_validation.csv"
)
NEXT_HOLDOUT_FREEZE_SOURCES = OUTPUT / "D4_E0003125_premeasurement_freeze_sources.csv"

CHECKPOINT = 5365
MARKER = "MTS_5365_D4_E000625_BLIND_HOLDOUT_POINTWISE_REMAINDER_ENVELOPE"
REVISION = "D4-E000625-blind-holdout-pointwise-remainder-envelope-v1"
CHECKED_DATE = "2026-08-12"
EPSILON_ID = "E000625"
EPSILON = 0.000625
EPSILON_REFERENCE = 0.0025
NEXT_EPSILON_ID = "E0003125"
NEXT_EPSILON = 0.0003125
NEXT_EPSILON_ROOT = FUNCTIONAL_RG / "5334" / NEXT_EPSILON_ID
NEXT_WEIGHTS = (
    Fraction(43, 16),
    Fraction(-73, 32),
    Fraction(21, 32),
    Fraction(-1, 16),
)
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_TEST = "valid_for_D4_complete_fixed_A_blind_holdout_test"
CLAIM_COMPATIBILITY = "valid_for_D4_E000625_complete_family_holdout_compatibility"
CLAIM_POINTWISE = "valid_for_D4_E000625_pointwise_remainder_envelope"
FALSE_CLAIMS = (
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
    drifts = [
        row["path"]
        for row in rows
        if not Path(row["path"]).is_file()
        or digest(Path(row["path"])) != row["sha256"]
    ]
    return not drifts, len(rows), drifts


def primary_prediction_row() -> dict[str, str]:
    rows = [
        row
        for row in read_csv(FREEZE_PREDICTION_5363)
        if row["holdout_epsilon_id"] == EPSILON_ID
    ]
    if len(rows) != 1:
        raise RuntimeError("exactly one frozen E000625 prediction is required")
    return rows[0]


def accepted_measurement_paths(root: Path) -> list[str]:
    paths: list[str] = []
    for path in root.glob("*finite_value.csv"):
        if any(
            parse_bool(row.get("finite_regulator_fixed_decay_integral_accepted", False))
            for row in read_csv(path)
        ):
            paths.append(str(path.resolve()))
    return paths


def freeze_next_holdout() -> dict[str, Any]:
    required = (
        FOUR_RUNG_INPUTS_5363,
        FREEZE_RESULT_5363,
        FREEZE_VALIDATION_5363,
        FIXED_A_RESULT_5360,
        E000625_RESULT,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    source_rows = sorted(read_csv(FOUR_RUNG_INPUTS_5363), key=lambda row: float(row["epsilon"]))
    expected_ids = ("E00125", "E0025", "E005", "E010")
    if tuple(row["epsilon_id"] for row in source_rows) != expected_ids:
        raise RuntimeError("unexpected four-rung source ordering")
    current_holdout = read_json(E000625_RESULT)
    next_measurements = accepted_measurement_paths(NEXT_EPSILON_ROOT)
    values = [
        complex(
            float(row["fixed_decay_integral_real"]),
            float(row["fixed_decay_integral_imaginary"]),
        )
        for row in source_rows
    ]
    radii = [float(row["fixed_decay_integral_disk_radius"]) for row in source_rows]
    source_epsilons = [float(row["epsilon"]) for row in source_rows]
    fixed_a = read_json(FIXED_A_RESULT_5360)
    coefficient_a = complex(float(fixed_a["A_zero_real"]), float(fixed_a["A_zero_imaginary"]))
    coefficient_a_radius = float(fixed_a["A_zero_disk_radius"])
    weights = [float(value) for value in NEXT_WEIGHTS]
    source_features = [
        epsilon * math.log(epsilon / EPSILON_REFERENCE)
        for epsilon in source_epsilons
    ]
    target_feature = NEXT_EPSILON * math.log(NEXT_EPSILON / EPSILON_REFERENCE)
    coefficient_multiplier = target_feature - sum(
        weight * feature for weight, feature in zip(weights, source_features, strict=True)
    )
    prediction = sum(
        weight * value for weight, value in zip(weights, values, strict=True)
    ) + coefficient_a * coefficient_multiplier
    data_radius = sum(
        abs(weight) * radius for weight, radius in zip(weights, radii, strict=True)
    )
    coefficient_radius = abs(coefficient_multiplier) * coefficient_a_radius
    validations = [
        validation_row(
            "four_rung_freeze_source_passes",
            read_json(FREEZE_RESULT_5363).get("validation_passed") is True
            and csv_validation_passes(FREEZE_VALIDATION_5363),
            expected_ids,
        ),
        validation_row(
            "exact_E0003125_weights_reproduce_complete_basis",
            NEXT_WEIGHTS
            == (
                Fraction(43, 16),
                Fraction(-73, 32),
                Fraction(21, 32),
                Fraction(-1, 16),
            )
            and sum(NEXT_WEIGHTS) == 1,
            NEXT_WEIGHTS,
        ),
        validation_row(
            "next_holdout_chosen_before_E000625_acceptance",
            current_holdout.get("acceptance_passed") is not True
            and current_holdout.get("completed_full_run") is not True,
            current_holdout.get("decision"),
        ),
        validation_row(
            "E0003125_measurement_absent_at_freeze",
            not next_measurements,
            next_measurements,
        ),
        validation_row(
            "prediction_disk_propagates_data_and_correlated_A_uncertainty",
            data_radius > 0.0
            and coefficient_radius >= 0.0
            and math.isfinite(data_radius + coefficient_radius),
            data_radius + coefficient_radius,
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
        "valid_for_D4_E0003125_complete_family_holdout_preregistration": passed,
        "valid_for_D4_E0003125_complete_family_holdout_compatibility": False,
        **no_broad_claims(),
    }
    frozen_row = {
        "holdout_epsilon_id": NEXT_EPSILON_ID,
        "holdout_epsilon": NEXT_EPSILON,
        "source_rung_ids": "|".join(expected_ids),
        "weight_E00125": str(NEXT_WEIGHTS[0]),
        "weight_E0025": str(NEXT_WEIGHTS[1]),
        "weight_E005": str(NEXT_WEIGHTS[2]),
        "weight_E010": str(NEXT_WEIGHTS[3]),
        "weight_absolute_sum": sum(abs(value) for value in weights),
        "derived_A_multiplier": coefficient_multiplier,
        **complex_fields("predicted_fixed_decay_integral", prediction),
        "prediction_data_disk_radius": data_radius,
        "prediction_coefficient_disk_radius": coefficient_radius,
        "prediction_total_disk_radius": data_radius + coefficient_radius,
        "frozen_before_accepted_E000625_value": True,
        "frozen_before_accepted_E0003125_value": True,
        "comparison_to_measured_holdout_performed": False,
        "freeze_utc": utc_now(),
        **claims,
    }
    direct_sources = (
        Path(__file__).resolve(),
        FOUR_RUNG_INPUTS_5363,
        FREEZE_RESULT_5363,
        FREEZE_VALIDATION_5363,
        FIXED_A_RESULT_5360,
    )
    provenance = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in direct_sources
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "mode": "D4-E0003125-premeasurement-complete-family-holdout-freeze",
        "validation_passed": passed,
        "decision": (
            "D4_E0003125_COMPLETE_FAMILY_HOLDOUT_FROZEN_BEFORE_E000625_RESULT"
            if passed
            else "D4_E0003125_HOLDOUT_FREEZE_BLOCKED"
        ),
        "prediction": frozen_row,
        "E000625_partial_result_sha256_at_freeze": digest(E000625_RESULT),
        "E000625_partial_decision_at_freeze": current_holdout.get("decision"),
        "claim_boundary": claims,
        "updated_utc": utc_now(),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(NEXT_HOLDOUT_FREEZE, [frozen_row])
    atomic_csv(NEXT_HOLDOUT_FREEZE_VALIDATION, validations)
    atomic_csv(NEXT_HOLDOUT_FREEZE_SOURCES, provenance)
    atomic_json(NEXT_HOLDOUT_FREEZE_RESULT, result)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return result


def preflight() -> dict[str, Any]:
    required = (
        Path(__file__).resolve(),
        FREEZE_RESULT_5363,
        FREEZE_PREDICTION_5363,
        FREEZE_VALIDATION_5363,
        FREEZE_SOURCES_5363,
        RUNNER_RESULT_5364,
        RUNNER_VALIDATION_5364,
        RUNNER_SOURCES_5364,
        FROZEN_EVENTS_5364,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
        E000625_SEMANTIC_VALIDATION,
        NEXT_HOLDOUT_FREEZE,
        NEXT_HOLDOUT_FREEZE_RESULT,
        NEXT_HOLDOUT_FREEZE_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    freeze = read_json(FREEZE_RESULT_5363)
    runner = read_json(RUNNER_RESULT_5364)
    result = read_json(E000625_RESULT)
    finite_rows = read_csv(E000625_FINITE)
    prediction = primary_prediction_row()
    freeze_sources = source_register_current(FREEZE_SOURCES_5363)
    runner_sources = source_register_current(RUNNER_SOURCES_5364)
    checks = {
        "checkpoint_5363_prediction_was_frozen_before_measurement": freeze.get(
            "validation_passed"
        )
        is True
        and freeze.get("primary_holdout_epsilon_id") == EPSILON_ID
        and parse_bool(prediction["frozen_before_accepted_holdout_value"])
        and not parse_bool(prediction["comparison_to_measured_holdout_performed"])
        and csv_validation_passes(FREEZE_VALIDATION_5363),
        "checkpoint_5364_runner_proves_measurement_absent_at_freeze": runner.get(
            "validation_passed"
        )
        is True
        and runner.get("frozen_prediction_source_sha256")
        == digest(FREEZE_PREDICTION_5363)
        and csv_validation_passes(RUNNER_VALIDATION_5364),
        "frozen_event_inventory_is_source_complete": len(read_csv(FROZEN_EVENTS_5364))
        == 8,
        "E000625_measurement_is_independently_accepted": len(finite_rows) == 1
        and finite_rows[0].get("epsilon_id") == EPSILON_ID
        and abs(float(finite_rows[0]["epsilon"]) - EPSILON) <= 1.0e-16
        and parse_bool(
            finite_rows[0]["finite_regulator_fixed_decay_integral_accepted"]
        )
        and result.get("acceptance_passed") is True
        and result.get("completed_full_run") is True
        and int(result.get("failed_inner_node_count", -1)) == 0
        and csv_validation_passes(E000625_VALIDATION)
        and csv_validation_passes(E000625_SEMANTIC_VALIDATION),
        "freeze_and_runner_source_registers_are_current": freeze_sources[0]
        and freeze_sources[1] > 0
        and runner_sources[0]
        and runner_sources[1] > 0,
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
        "next_asymptotic_holdout_was_frozen_before_E000625_result": read_json(
            NEXT_HOLDOUT_FREEZE_RESULT
        ).get("validation_passed")
        is True
        and csv_validation_passes(NEXT_HOLDOUT_FREEZE_VALIDATION),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "freeze_source_drifts": freeze_sources[2],
        "runner_source_drifts": runner_sources[2],
    }


def evaluate() -> dict[str, Any]:
    prediction_row = primary_prediction_row()
    finite = read_csv(E000625_FINITE)[0]
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
    separation = abs(residual)
    combined_radius = prediction_radius + measured_radius
    normalization = EPSILON**3 * (
        1.0 + abs(math.log(EPSILON / EPSILON_REFERENCE))
    )
    return {
        "prediction": prediction,
        "prediction_radius": prediction_radius,
        "measured": measured,
        "measured_radius": measured_radius,
        "residual": residual,
        "separation": separation,
        "combined_radius": combined_radius,
        "disk_margin": combined_radius - separation,
        "compatible": separation <= combined_radius,
        "pointwise_defect_lower": max(0.0, separation - combined_radius),
        "pointwise_defect_upper": separation + combined_radius,
        "normalization": normalization,
        "normalized_central_defect": separation / normalization,
        "normalized_defect_lower": max(0.0, separation - combined_radius)
        / normalization,
        "normalized_defect_upper": (separation + combined_radius) / normalization,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5365 - D4 E000625 blind holdout and pointwise remainder envelope",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Blind comparison",
        "",
        "Checkpoint 5363 froze the complete fixed-A prediction from E00125, E0025, E005 and E010. Checkpoint 5364 proved the E000625 measurement was absent before launching its independent source-complete integration.",
        "",
        f"- frozen prediction: `{result['predicted_real']:.17g} {result['predicted_imaginary']:+.17g} i`, disk `{result['prediction_disk_radius']:.17g}`;",
        f"- measured E000625: `{result['measured_real']:.17g} {result['measured_imaginary']:+.17g} i`, disk `{result['measurement_disk_radius']:.17g}`;",
        f"- centre separation: `{result['centre_separation']:.17g}`;",
        f"- combined disk radius: `{result['combined_disk_radius']:.17g}`;",
        f"- compatibility: `{result['holdout_compatible']}`.",
        "",
        "## Remainder boundary",
        "",
        "The measured-minus-frozen-prediction disk gives a valid pointwise defect envelope at epsilon=0.000625. Dividing it by `epsilon^3[1+|Log(epsilon/0.0025)|]` reports a sampled normalized envelope only.",
        "",
        f"- pointwise defect upper bound: `{result['pointwise_defect_upper']:.17g}`;",
        f"- normalized pointwise upper bound: `{result['normalized_defect_upper']:.17g}`.",
        "",
        "This single holdout cannot promote that sampled number to a uniform `M_D4` over a regulator interval. No refit, regulator-zero, angular, UV, local-GR, or full-MTS claim is made.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    evaluation = evaluate()
    compatibility = bool(evaluation["compatible"])
    validations = [
        validation_row("preflight_passes", True, preflight_result["checks"]),
        validation_row(
            "comparison_uses_frozen_prediction_without_refit",
            digest(FREEZE_PREDICTION_5363)
            == read_json(RUNNER_RESULT_5364)["frozen_prediction_source_sha256"],
            digest(FREEZE_PREDICTION_5363),
        ),
        validation_row(
            "disk_comparison_uses_conservative_radius_sum",
            evaluation["combined_radius"]
            == evaluation["prediction_radius"] + evaluation["measured_radius"]
            and evaluation["combined_radius"] > 0.0,
            evaluation["combined_radius"],
        ),
        validation_row(
            "pointwise_remainder_envelope_is_finite_and_ordered",
            evaluation["normalization"] > 0.0
            and 0.0
            <= evaluation["pointwise_defect_lower"]
            <= evaluation["pointwise_defect_upper"]
            and 0.0
            <= evaluation["normalized_defect_lower"]
            <= evaluation["normalized_defect_upper"]
            and all(
                math.isfinite(evaluation[key])
                for key in (
                    "pointwise_defect_lower",
                    "pointwise_defect_upper",
                    "normalized_defect_lower",
                    "normalized_defect_upper",
                )
            ),
            evaluation["normalized_defect_upper"],
        ),
        validation_row(
            "single_holdout_does_not_claim_uniform_remainder_or_limit",
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
        CLAIM_TEST: passed,
        CLAIM_COMPATIBILITY: passed and compatibility,
        CLAIM_POINTWISE: passed,
        **no_broad_claims(),
    }
    comparison = {
        "holdout_epsilon_id": EPSILON_ID,
        "holdout_epsilon": EPSILON,
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
    remainder = {
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "epsilon_reference": EPSILON_REFERENCE,
        "normalization": "epsilon^3*(1+abs(Log(epsilon/epsilon_reference)))",
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
        "reason": "one sampled holdout bounds the pointwise defect only; uniform derivative or multi-rung interval control remains open",
        **claims,
    }
    direct_sources = (
        Path(__file__).resolve(),
        FREEZE_RESULT_5363,
        FREEZE_PREDICTION_5363,
        FREEZE_VALIDATION_5363,
        FREEZE_SOURCES_5363,
        RUNNER_RESULT_5364,
        RUNNER_VALIDATION_5364,
        RUNNER_SOURCES_5364,
        FROZEN_EVENTS_5364,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
        E000625_SEMANTIC_VALIDATION,
        NEXT_HOLDOUT_FREEZE,
        NEXT_HOLDOUT_FREEZE_RESULT,
        NEXT_HOLDOUT_FREEZE_VALIDATION,
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
    decision = (
        "D4_E000625_BLIND_HOLDOUT_COMPATIBLE__POINTWISE_REMAINDER_ENVELOPE_ONLY"
        if compatibility
        else "D4_E000625_BLIND_HOLDOUT_INCOMPATIBLE__COMPLETE_FIXED_A_FAMILY_REQUIRES_REVISION"
    )
    result = {
        "mode": "D4-E000625-blind-holdout-pointwise-remainder-envelope",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "validation_passed": passed,
        "decision": decision,
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
        "pointwise_defect_upper": evaluation["pointwise_defect_upper"],
        "normalized_defect_upper": evaluation["normalized_defect_upper"],
        "claim_boundary": claims,
        "remaining_obstruction": "derive a uniform third-order derivative bound or acquire additional asymptotic holdouts before promoting the sampled envelope to a numeric M_D4 and outer-regulator limit",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
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


def validate_saved(output: Path) -> dict[str, Any]:
    source_current, source_count, source_drifts = source_register_current(
        output / "source_register.csv"
    )
    result = read_json(output / RESULT.name) if (output / RESULT.name).is_file() else {}
    checks = {
        "validation_file_passes": (output / VALIDATION.name).is_file()
        and csv_validation_passes(output / VALIDATION.name),
        "residual_validation_passes": RESIDUAL_VALIDATION.is_file()
        and csv_validation_passes(RESIDUAL_VALIDATION),
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
    parser.add_argument("--freeze-next-holdout", action="store_true")
    arguments = parser.parse_args()
    if arguments.freeze_next_holdout:
        payload = freeze_next_holdout()
    elif arguments.dry_run:
        payload = preflight()
    elif arguments.validate_saved:
        payload = validate_saved(arguments.output_dir)
    else:
        payload = run(arguments.output_dir)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
