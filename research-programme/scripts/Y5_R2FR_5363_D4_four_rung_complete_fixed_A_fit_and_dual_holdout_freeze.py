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
OUTPUT = FUNCTIONAL_RG / "5363"
DOCUMENT = POST / "5363-Y5-R2FR-D4-four-rung-complete-fixed-A-fit-and-dual-holdout-freeze.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5363_VALIDATION.csv"

RESULT_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
VALIDATION_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
RESULT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
VALIDATION_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_validation.csv"
RESULT_5361 = FUNCTIONAL_RG / "5361" / "D4_E005_holdout_result.json"
VALIDATION_5361 = FUNCTIONAL_RG / "5361" / "D4_E005_holdout_validation.csv"
RESULT_5362 = FUNCTIONAL_RG / "5362" / "D4_E010_source_complete_runner_result.json"
VALIDATION_5362 = FUNCTIONAL_RG / "5362" / "D4_E010_source_complete_runner_validation.csv"

E00125_FINITE = FUNCTIONAL_RG / "5334" / "E00125" / "D4_outer_event_aligned_E00125_finite_value.csv"
E00125_RESULT = FUNCTIONAL_RG / "5334" / "E00125" / "D4_outer_event_aligned_E00125_result.json"
E0025_FINITE = FUNCTIONAL_RG / "5340" / "D4_E0025_log_corrected_finite_value.csv"
E0025_RESULT = FUNCTIONAL_RG / "5340" / "D4_E0025_log_corrected_canonical_result.json"
E005_FINITE = FUNCTIONAL_RG / "5334" / "E005" / "D4_outer_event_aligned_E005_finite_value.csv"
E005_RESULT = FUNCTIONAL_RG / "5334" / "E005" / "D4_outer_event_aligned_E005_result.json"
E005_VALIDATION = FUNCTIONAL_RG / "5334" / "E005" / "D4_outer_event_aligned_E005_validation.csv"
E010_FINITE = FUNCTIONAL_RG / "5334" / "E010" / "D4_outer_event_aligned_E010_finite_value.csv"
E010_RESULT = FUNCTIONAL_RG / "5334" / "E010" / "D4_outer_event_aligned_E010_result.json"
E010_VALIDATION = FUNCTIONAL_RG / "5334" / "E010" / "D4_outer_event_aligned_E010_validation.csv"

E000625_ROOT = FUNCTIONAL_RG / "5334" / "E000625"
E020_ROOT = FUNCTIONAL_RG / "5334" / "E020"

CHECKPOINT = 5363
MARKER = "MTS_5363_D4_FOUR_RUNG_COMPLETE_FIXED_A_FIT_DUAL_HOLDOUT_FREEZE"
REVISION = "D4-four-rung-complete-fixed-A-fit-dual-holdout-freeze-v1"
CHECKED_DATE = "2026-08-12"
EPSILON_H = 0.00125
EPSILON_REFERENCE = 0.0025
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

SOURCE_RUNGS = (
    ("E00125", 0.00125, E00125_FINITE, E00125_RESULT, None),
    ("E0025", 0.0025, E0025_FINITE, E0025_RESULT, None),
    ("E005", 0.005, E005_FINITE, E005_RESULT, E005_VALIDATION),
    ("E010", 0.01, E010_FINITE, E010_RESULT, E010_VALIDATION),
)
HOLDOUTS = (
    ("E000625", 0.000625, E000625_ROOT, (Fraction(2), Fraction(-21, 16), Fraction(11, 32), Fraction(-1, 32))),
    ("E020", 0.02, E020_ROOT, (Fraction(-32), Fraction(64), Fraction(-42), Fraction(11))),
)

DESIGN = (
    (Fraction(1), Fraction(1), Fraction(-1), Fraction(1)),
    (Fraction(1), Fraction(2), Fraction(0), Fraction(4)),
    (Fraction(1), Fraction(4), Fraction(16), Fraction(16)),
    (Fraction(1), Fraction(8), Fraction(128), Fraction(64)),
)
DESIGN_INVERSE = (
    (Fraction(32, 9), Fraction(-32, 9), Fraction(10, 9), Fraction(-1, 9)),
    (Fraction(-4), Fraction(6), Fraction(-9, 4), Fraction(1, 4)),
    (Fraction(-1, 3), Fraction(7, 12), Fraction(-7, 24), Fraction(1, 24)),
    (Fraction(10, 9), Fraction(-67, 36), Fraction(61, 72), Fraction(-7, 72)),
)

CLAIM_FIT = "valid_for_D4_four_rung_complete_fixed_A_interpolation"
CLAIM_FREEZE = "valid_for_D4_dual_complete_family_holdout_preregistration"
FALSE_CLAIMS = (
    "valid_for_D4_E000625_complete_family_holdout_compatibility",
    "valid_for_D4_E020_complete_family_holdout_compatibility",
    "valid_for_D4_numeric_remainder_bound",
    "valid_for_D4_complete_family_overdetermined_fit",
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


def matrix_product(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(4))
            for column in range(4)
        )
        for row in range(4)
    )


def algebra_self_test() -> dict[str, Any]:
    identity = matrix_product(DESIGN_INVERSE, DESIGN)
    expected_identity = tuple(
        tuple(Fraction(int(row == column)) for column in range(4))
        for row in range(4)
    )
    source_x = (Fraction(1), Fraction(2), Fraction(4), Fraction(8))
    source_k = (0, 1, 2, 3)
    checks: dict[str, bool] = {
        "exact_design_inverse": identity == expected_identity,
        "holdout_weights_reproduce_complete_basis": True,
        "broad_claims_default_false": all(
            value is False for value in no_broad_claims().values()
        ),
    }
    for _, epsilon, _, weights in HOLDOUTS:
        x = Fraction(str(epsilon)) / Fraction(str(EPSILON_H))
        k = int(round(math.log2(float(x))))
        target_basis = (Fraction(1), x, Fraction(k - 1) * x * x, x * x)
        for column in range(4):
            reproduced = sum(
                weights[index]
                * (
                    Fraction(1),
                    source_x[index],
                    Fraction(source_k[index] - 1) * source_x[index] ** 2,
                    source_x[index] ** 2,
                )[column]
                for index in range(4)
            )
            checks["holdout_weights_reproduce_complete_basis"] &= (
                reproduced == target_basis[column]
            )
    return {"checks": checks, "all_pass": all(checks.values())}


def target_has_no_accepted_measurement(root: Path) -> tuple[bool, list[str]]:
    accepted_paths: list[str] = []
    for path in root.glob("*finite_value.csv"):
        for row in read_csv(path):
            if parse_bool(
                row.get("finite_regulator_fixed_decay_integral_accepted", False)
            ):
                accepted_paths.append(str(path.resolve()))
    return not accepted_paths, accepted_paths


def load_rung(
    epsilon_id: str,
    epsilon: float,
    finite_path: Path,
    result_path: Path,
    validation_path: Path | None,
) -> dict[str, Any]:
    rows = read_csv(finite_path)
    result = read_json(result_path)
    checks = {
        "one_finite_row": len(rows) == 1,
        "epsilon_identity": len(rows) == 1
        and rows[0].get("epsilon_id") == epsilon_id
        and abs(float(rows[0].get("epsilon", math.inf)) - epsilon) <= 1.0e-16,
        "finite_row_accepted": len(rows) == 1
        and parse_bool(
            rows[0].get("finite_regulator_fixed_decay_integral_accepted", False)
        ),
        "result_accepted_and_complete": result.get("acceptance_passed") is True
        and result.get("completed_full_run", True) is True,
        "validation_passes": validation_path is None
        or csv_validation_passes(validation_path),
    }
    row = rows[0] if rows else {}
    return {
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "value": complex(
            float(row.get("fixed_decay_integral_real", math.nan)),
            float(row.get("fixed_decay_integral_imaginary", math.nan)),
        ),
        "radius": float(row.get("total_error_absolute_conservative", math.inf)),
        "finite_path": finite_path,
        "result_path": result_path,
        "validation_path": validation_path,
        "checks": checks,
        "valid": all(checks.values()),
    }


def preflight() -> dict[str, Any]:
    required = [
        Path(__file__).resolve(),
        RESULT_5359,
        VALIDATION_5359,
        RESULT_5360,
        VALIDATION_5360,
        RESULT_5361,
        VALIDATION_5361,
        RESULT_5362,
        VALIDATION_5362,
    ]
    for _, _, finite, result, validation in SOURCE_RUNGS:
        required.extend((finite, result))
        if validation is not None:
            required.append(validation)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    rungs = [load_rung(*row) for row in SOURCE_RUNGS]
    unmeasured = {
        epsilon_id: target_has_no_accepted_measurement(root)
        for epsilon_id, _, root, _ in HOLDOUTS
    }
    checks = {
        "all_four_integrated_rungs_are_accepted": all(
            rung["valid"] for rung in rungs
        ),
        "checkpoint_5359_derived_A_passes": read_json(RESULT_5359).get(
            "validation_passed"
        )
        is True
        and csv_validation_passes(VALIDATION_5359),
        "checkpoint_5360_fixed_A_contract_passes": read_json(RESULT_5360).get(
            "validation_passed"
        )
        is True
        and csv_validation_passes(VALIDATION_5360),
        "checkpoint_5361_blind_E005_holdout_passes": read_json(RESULT_5361).get(
            "validation_passed"
        )
        is True
        and read_json(RESULT_5361).get("holdout_compatible") is True
        and csv_validation_passes(VALIDATION_5361),
        "checkpoint_5362_E010_setup_passes": read_json(RESULT_5362).get(
            "validation_passed"
        )
        is True
        and csv_validation_passes(VALIDATION_5362),
        "both_holdouts_are_unmeasured": all(value[0] for value in unmeasured.values()),
        "exact_algebra_self_test_passes": algebra_self_test()["all_pass"],
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "rung_checks": {rung["epsilon_id"]: rung["checks"] for rung in rungs},
        "unmeasured_holdouts": unmeasured,
    }


def evaluate() -> dict[str, Any]:
    result_5360 = read_json(RESULT_5360)
    coefficient_A = complex(
        float(result_5360["A_zero_real"]),
        float(result_5360["A_zero_imaginary"]),
    )
    coefficient_A_radius = float(result_5360["A_zero_disk_radius"])
    rungs = [load_rung(*row) for row in SOURCE_RUNGS]
    values = [rung["value"] for rung in rungs]
    radii = [rung["radius"] for rung in rungs]
    log_features = [
        rung["epsilon"] * math.log(rung["epsilon"] / EPSILON_REFERENCE)
        for rung in rungs
    ]
    corrected = [
        value - coefficient_A * feature
        for value, feature in zip(values, log_features, strict=True)
    ]
    scaled_coefficients = [
        sum(float(weight) * corrected[index] for index, weight in enumerate(row))
        for row in DESIGN_INVERSE
    ]
    scaled_radii = []
    for row in DESIGN_INVERSE:
        data_radius = sum(
            abs(float(weight)) * radii[index]
            for index, weight in enumerate(row)
        )
        coefficient_multiplier = sum(
            float(weight) * log_features[index]
            for index, weight in enumerate(row)
        )
        scaled_radii.append(
            data_radius + abs(coefficient_multiplier) * coefficient_A_radius
        )
    coefficient_values = (
        scaled_coefficients[0],
        scaled_coefficients[1] / EPSILON_H,
        scaled_coefficients[2] / (EPSILON_H**2 * math.log(2.0)),
        scaled_coefficients[3] / EPSILON_H**2,
    )
    coefficient_radii = (
        scaled_radii[0],
        scaled_radii[1] / EPSILON_H,
        scaled_radii[2] / (EPSILON_H**2 * math.log(2.0)),
        scaled_radii[3] / EPSILON_H**2,
    )
    reconstruction_errors = []
    for index, rung in enumerate(rungs):
        x = rung["epsilon"] / EPSILON_H
        k = int(round(math.log2(x)))
        reconstructed = (
            scaled_coefficients[0]
            + scaled_coefficients[1] * x
            + scaled_coefficients[2] * (k - 1) * x**2
            + scaled_coefficients[3] * x**2
        )
        reconstruction_errors.append(abs(reconstructed - corrected[index]))
    predictions = []
    for epsilon_id, epsilon, root, weights_fraction in HOLDOUTS:
        weights = [float(value) for value in weights_fraction]
        feature = epsilon * math.log(epsilon / EPSILON_REFERENCE)
        coefficient_multiplier = feature - sum(
            weights[index] * log_features[index] for index in range(4)
        )
        prediction = sum(weights[index] * values[index] for index in range(4))
        prediction += coefficient_A * coefficient_multiplier
        data_radius = sum(
            abs(weights[index]) * radii[index] for index in range(4)
        )
        coefficient_radius = abs(coefficient_multiplier) * coefficient_A_radius
        predictions.append(
            {
                "holdout_epsilon_id": epsilon_id,
                "holdout_epsilon": epsilon,
                "source_rung_ids": "|".join(rung["epsilon_id"] for rung in rungs),
                "weight_E00125": str(weights_fraction[0]),
                "weight_E0025": str(weights_fraction[1]),
                "weight_E005": str(weights_fraction[2]),
                "weight_E010": str(weights_fraction[3]),
                "weight_absolute_sum": sum(abs(value) for value in weights),
                "derived_A_multiplier": coefficient_multiplier,
                **complex_fields("predicted_fixed_decay_integral", prediction),
                "prediction_data_disk_radius": data_radius,
                "prediction_coefficient_disk_radius": coefficient_radius,
                "prediction_total_disk_radius": data_radius + coefficient_radius,
                "frozen_before_accepted_holdout_value": target_has_no_accepted_measurement(root)[0],
                "comparison_to_measured_holdout_performed": False,
                "measured_holdout_value": "NOT_YET_ACCEPTED",
            }
        )
    return {
        "A": coefficient_A,
        "A_radius": coefficient_A_radius,
        "rungs": rungs,
        "values": values,
        "radii": radii,
        "corrected": corrected,
        "scaled_coefficients": scaled_coefficients,
        "scaled_radii": scaled_radii,
        "coefficient_values": coefficient_values,
        "coefficient_radii": coefficient_radii,
        "reconstruction_errors": reconstruction_errors,
        "predictions": predictions,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5363 - D4 four-rung complete fixed-A fit and dual holdout freeze",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Complete fixed-A family",
        "",
        "With `A` derived independently, four accepted rungs determine the four remaining complex coefficients in",
        "",
        "`J(epsilon)=I0+B epsilon+C epsilon^2 Log(epsilon/0.0025)+D epsilon^2`,",
        "",
        "where `J=I-A epsilon Log(epsilon/0.0025)`. This is an exact four-point interpolation, not an overdetermined fit and not a regulator-zero proof.",
        "",
        "## Frozen holdouts",
        "",
    ]
    for prediction in result["holdout_predictions"]:
        lines.extend(
            [
                f"- `{prediction['holdout_epsilon_id']}` prediction: `{prediction['predicted_fixed_decay_integral_real']:.17g} {prediction['predicted_fixed_decay_integral_imaginary']:+.17g} i`, disk `{prediction['prediction_total_disk_radius']:.17g}`, absolute weight sum `{prediction['weight_absolute_sum']:.8g}`;",
            ]
        )
    lines.extend(
        [
            "",
            "The E000625 prediction is the primary asymptotic holdout because its exact weights `(2,-21/16,11/32,-1/32)` have absolute sum `59/16`. E020 is retained as a deliberately severe outward extrapolation; its weights `(-32,64,-42,11)` have absolute sum `149`, so its conservative disk is expected to be much broader.",
            "",
            "## Claim boundary",
            "",
            "Neither holdout has been read or fitted. A fifth accepted rung is required for an overdetermined complete-family test; additional rungs and a numerical remainder constant are required for the D4 regulator-zero limit.",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    evaluation = evaluate()
    maximum_reconstruction_error = max(evaluation["reconstruction_errors"])
    predictions = evaluation["predictions"]
    validations = [
        validation_row("preflight_passes", True, preflight_result["checks"]),
        validation_row(
            "exact_design_inverse_and_holdout_weights_pass",
            algebra_self_test()["all_pass"],
            algebra_self_test()["checks"],
        ),
        validation_row(
            "four_rungs_reconstruct_to_roundoff",
            maximum_reconstruction_error <= 2.0e-13,
            maximum_reconstruction_error,
        ),
        validation_row(
            "both_holdouts_are_frozen_before_measurement",
            len(predictions) == 2
            and all(row["frozen_before_accepted_holdout_value"] for row in predictions)
            and all(not row["comparison_to_measured_holdout_performed"] for row in predictions),
            [row["holdout_epsilon_id"] for row in predictions],
        ),
        validation_row(
            "prediction_disks_propagate_data_and_correlated_A_uncertainty",
            all(
                row["prediction_total_disk_radius"]
                == row["prediction_data_disk_radius"]
                + row["prediction_coefficient_disk_radius"]
                and row["prediction_total_disk_radius"] > 0.0
                for row in predictions
            ),
            [row["prediction_total_disk_radius"] for row in predictions],
        ),
        validation_row(
            "four_point_fit_does_not_claim_overdetermination_or_limit",
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
        CLAIM_FIT: passed,
        CLAIM_FREEZE: passed,
        **no_broad_claims(),
    }
    coefficient_names = ("I0", "B", "C", "D")
    coefficient_rows = []
    for index, name in enumerate(coefficient_names):
        coefficient_rows.append(
            {
                "coefficient": name,
                **complex_fields("value", evaluation["coefficient_values"][index]),
                "conservative_disk_radius": evaluation["coefficient_radii"][index],
                "scaled_basis_value_real": evaluation["scaled_coefficients"][index].real,
                "scaled_basis_value_imaginary": evaluation["scaled_coefficients"][index].imag,
                "scaled_basis_disk_radius": evaluation["scaled_radii"][index],
                **claims,
            }
        )
    rung_rows = []
    for index, rung in enumerate(evaluation["rungs"]):
        rung_rows.append(
            {
                "epsilon_id": rung["epsilon_id"],
                "epsilon": rung["epsilon"],
                **complex_fields("fixed_decay_integral", evaluation["values"][index]),
                "fixed_decay_integral_disk_radius": evaluation["radii"][index],
                **complex_fields("derived_A_corrected_J", evaluation["corrected"][index]),
                "source_path": str(rung["finite_path"].resolve()),
                "source_sha256": digest(rung["finite_path"]),
                **claims,
            }
        )
    for row in predictions:
        row.update(claims)
    snapshot_rows = [
        {
            "holdout_epsilon_id": epsilon_id,
            "holdout_root": str(root.resolve()),
            "accepted_measurement_present_at_freeze": not target_has_no_accepted_measurement(root)[0],
            "accepted_measurement_paths": "|".join(target_has_no_accepted_measurement(root)[1]),
            "snapshot_utc": utc_now(),
            **claims,
        }
        for epsilon_id, _, root, _ in HOLDOUTS
    ]
    direct_sources = [
        Path(__file__).resolve(),
        RESULT_5359,
        VALIDATION_5359,
        RESULT_5360,
        VALIDATION_5360,
        RESULT_5361,
        VALIDATION_5361,
        RESULT_5362,
        VALIDATION_5362,
    ]
    for _, _, finite, result, validation in SOURCE_RUNGS:
        direct_sources.extend((finite, result))
        if validation is not None:
            direct_sources.append(validation)
    direct_sources = sorted(set(direct_sources), key=lambda path: str(path).lower())
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
        "mode": "D4-four-rung-complete-fixed-A-fit-dual-holdout-freeze",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "validation_passed": passed,
        "decision": (
            "D4_COMPLETE_FIXED_A_FOUR_RUNG_INTERPOLATION_AND_DUAL_HOLDOUT_FROZEN__RUN_E000625_PRIMARY"
            if passed
            else "D4_COMPLETE_FIXED_A_FIT_OR_HOLDOUT_FREEZE_BLOCKED"
        ),
        "source_rung_ids": [rung["epsilon_id"] for rung in evaluation["rungs"]],
        "source_rung_count": len(evaluation["rungs"]),
        "complete_family_complex_parameter_count_after_derived_A": 4,
        "fit_degrees_of_freedom": 0,
        "maximum_source_reconstruction_error": maximum_reconstruction_error,
        "holdout_predictions": predictions,
        "primary_holdout_epsilon_id": "E000625",
        "claim_boundary": claims,
        "remaining_obstruction": "accept E000625 as the fifth complete-family rung, compare it without refit, then acquire additional rungs for a numerical remainder bound",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_complete_fixed_A_four_rung_inputs.csv", rung_rows)
    atomic_csv(output / "D4_complete_fixed_A_four_rung_coefficients.csv", coefficient_rows)
    atomic_csv(output / "D4_complete_fixed_A_dual_holdout_predictions.csv", predictions)
    atomic_csv(output / "D4_complete_fixed_A_holdout_freeze_snapshot.csv", snapshot_rows)
    atomic_csv(output / "D4_complete_fixed_A_fit_validation.csv", validations)
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_complete_fixed_A_fit_result.json", result)
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


def source_register_current(path: Path) -> tuple[bool, list[str]]:
    if not path.is_file():
        return False, [str(path)]
    drifts = [
        row["path"]
        for row in read_csv(path)
        if not Path(row["path"]).is_file()
        or digest(Path(row["path"])) != row["sha256"]
    ]
    return not drifts, drifts


def validate_saved(output: Path) -> dict[str, Any]:
    result_path = output / "D4_complete_fixed_A_fit_result.json"
    validation_path = output / "D4_complete_fixed_A_fit_validation.csv"
    source_path = output / "source_register.csv"
    source_current, drifts = source_register_current(source_path)
    checks = {
        "result_validation_passes": result_path.is_file()
        and read_json(result_path).get("validation_passed") is True,
        "validation_file_passes": validation_path.is_file()
        and csv_validation_passes(validation_path),
        "residual_validation_passes": VALIDATION.is_file()
        and csv_validation_passes(VALIDATION),
        "registered_sources_are_current": source_current,
        "document_exists": DOCUMENT.is_file(),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "validate-saved",
        "checks": checks,
        "source_drifts": drifts,
        "all_pass": all(checks.values()),
    }


def main() -> int:
    set_below_normal_priority()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        payload = {"mode": "self-test", **algebra_self_test()}
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
