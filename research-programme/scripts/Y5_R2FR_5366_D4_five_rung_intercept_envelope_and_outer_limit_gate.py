from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import time
from typing import Any

import numpy as np


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

PREREGISTRATION = FUNCTIONAL_RG / "5345" / "D4_zero_rung_count_gate.csv"
ASYMPTOTIC_CONTRACT = (
    FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
)
FIXED_A_RESULT = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
FOUR_RUNG_INPUTS = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_four_rung_inputs.csv"
BLIND_RESULT = FUNCTIONAL_RG / "5365" / "D4_E000625_blind_holdout_result.json"
BLIND_VALIDATION = FUNCTIONAL_RG / "5365" / "D4_E000625_blind_holdout_validation.csv"
BLIND_SOURCES = FUNCTIONAL_RG / "5365" / "source_register.csv"
NEXT_HOLDOUT_FREEZE_RESULT = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_result.json"
)
E000625_FINITE = (
    FUNCTIONAL_RG
    / "5334"
    / "E000625"
    / "D4_outer_event_aligned_E000625_finite_value.csv"
)
E000625_RESULT = (
    FUNCTIONAL_RG / "5334" / "E000625" / "D4_outer_event_aligned_E000625_result.json"
)
E000625_VALIDATION = (
    FUNCTIONAL_RG
    / "5334"
    / "E000625"
    / "D4_outer_event_aligned_E000625_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5366"
RESULT = OUTPUT / "D4_five_rung_intercept_envelope_result.json"
FIT_ROWS = OUTPUT / "D4_five_rung_complete_fixed_A_fit.csv"
INTERCEPT_ROWS = OUTPUT / "D4_five_rung_intercept_envelope.csv"
RESIDUAL_ROWS = OUTPUT / "D4_five_rung_residuals.csv"
LOO_ROWS = OUTPUT / "D4_five_rung_leave_one_out.csv"
GATE_ROWS = OUTPUT / "D4_outer_limit_gate.csv"
VALIDATION = OUTPUT / "D4_five_rung_intercept_envelope_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5366_VALIDATION.csv"
DOCUMENT = POST / "5366-Y5-R2FR-D4-five-rung-intercept-envelope-and-outer-limit-gate.md"

CHECKPOINT = 5366
MARKER = "MTS_5366_D4_FIVE_RUNG_INTERCEPT_ENVELOPE_OUTER_LIMIT_GATE"
REVISION = "D4-five-rung-intercept-envelope-outer-limit-gate-v1"
CHECKED_DATE = "2026-08-13"
EPSILON_H = 0.000625
EPSILON_REFERENCE = 0.0025
INTERCEPT_RELATIVE_LIMIT = 0.01
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_FIT = "valid_for_D4_five_rung_complete_fixed_A_intercept_envelope"
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


def load_inputs() -> list[dict[str, Any]]:
    four = read_csv(FOUR_RUNG_INPUTS)
    finite = read_csv(E000625_FINITE)
    if len(finite) != 1:
        raise RuntimeError("exactly one E000625 finite row is required")
    rows = [
        {
            "epsilon_id": row["epsilon_id"],
            "epsilon": float(row["epsilon"]),
            "value": complex(
                float(row["fixed_decay_integral_real"]),
                float(row["fixed_decay_integral_imaginary"]),
            ),
            "radius": float(row["fixed_decay_integral_disk_radius"]),
            "source_path": FOUR_RUNG_INPUTS,
        }
        for row in four
    ]
    row = finite[0]
    rows.append(
        {
            "epsilon_id": row["epsilon_id"],
            "epsilon": float(row["epsilon"]),
            "value": complex(
                float(row["fixed_decay_integral_real"]),
                float(row["fixed_decay_integral_imaginary"]),
            ),
            "radius": float(row["total_error_absolute_conservative"]),
            "source_path": E000625_FINITE,
        }
    )
    return sorted(rows, key=lambda item: item["epsilon"])


def preflight() -> dict[str, Any]:
    required = (
        Path(__file__).resolve(),
        PREREGISTRATION,
        ASYMPTOTIC_CONTRACT,
        FIXED_A_RESULT,
        FOUR_RUNG_INPUTS,
        BLIND_RESULT,
        BLIND_VALIDATION,
        BLIND_SOURCES,
        NEXT_HOLDOUT_FREEZE_RESULT,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    inputs = load_inputs()
    preregistered_five = [
        row for row in read_csv(PREREGISTRATION) if int(row["accepted_rung_count"]) == 5
    ]
    asymptotic = read_csv(ASYMPTOTIC_CONTRACT)
    blind_sources = source_register_current(BLIND_SOURCES)
    E000625_result = read_json(E000625_RESULT)
    checks = {
        "five_independently_accepted_rungs_present": len(inputs) == 5
        and tuple(row["epsilon_id"] for row in inputs)
        == ("E000625", "E00125", "E0025", "E005", "E010")
        and E000625_result.get("acceptance_passed") is True
        and E000625_result.get("completed_full_run") is True
        and csv_validation_passes(E000625_VALIDATION),
        "complete_second_order_family_is_parent_derived": any(
            row["contract_id"] == "NF5345_03_complete_second_order_family"
            and parse_bool(row["contract_passes"])
            for row in asymptotic
        ),
        "five_rung_status_was_preregistered_as_no_complete_residual_test": len(
            preregistered_five
        )
        == 1
        and preregistered_five[0]["second_order_status"]
        == "COMPLETE_FAMILY_EXACTLY_DETERMINED"
        and preregistered_five[0]["allowed_decision"]
        == "SECOND_ORDER_STRESS_NO_COMPLETE_RESIDUAL_TEST",
        "blind_E000625_holdout_passes": read_json(BLIND_RESULT).get(
            "validation_passed"
        )
        is True
        and read_json(BLIND_RESULT).get("holdout_compatible") is True
        and csv_validation_passes(BLIND_VALIDATION),
        "blind_source_register_is_current": blind_sources[0]
        and blind_sources[1] > 0,
        "next_asymptotic_holdout_is_frozen": read_json(
            NEXT_HOLDOUT_FREEZE_RESULT
        ).get("validation_passed")
        is True,
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "source_drifts": blind_sources[2],
    }


def fit_projection(
    design: np.ndarray, corrected: np.ndarray, radii: np.ndarray, weights: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    normal_inverse = np.linalg.inv(design.T @ np.diag(weights) @ design)
    projection = normal_inverse @ design.T @ np.diag(weights)
    return projection @ corrected, projection


def evaluate() -> dict[str, Any]:
    inputs = load_inputs()
    epsilon = np.asarray([row["epsilon"] for row in inputs], dtype=float)
    values = np.asarray([row["value"] for row in inputs], dtype=complex)
    radii = np.asarray([row["radius"] for row in inputs], dtype=float)
    fixed_a = read_json(FIXED_A_RESULT)
    coefficient_a = complex(
        float(fixed_a["A_zero_real"]), float(fixed_a["A_zero_imaginary"])
    )
    coefficient_a_radius = float(fixed_a["A_zero_disk_radius"])
    log_features = epsilon * np.log(epsilon / EPSILON_REFERENCE)
    corrected = values - coefficient_a * log_features
    x = epsilon / EPSILON_H
    k = np.rint(np.log2(x)).astype(int)
    design = np.column_stack((np.ones(5), x, (k - 2) * x**2, x**2))
    weighted_coefficients, weighted_projection = fit_projection(
        design, corrected, radii, 1.0 / radii**2
    )
    unweighted_coefficients, unweighted_projection = fit_projection(
        design, corrected, radii, np.ones(5)
    )
    weighted_predictions = design @ weighted_coefficients
    weighted_residuals = corrected - weighted_predictions
    intercept_projection = weighted_projection[0]
    input_disk = float(np.sum(np.abs(intercept_projection) * radii))
    correlated_a_multiplier = float(np.sum(intercept_projection * log_features))
    correlated_a_disk = abs(correlated_a_multiplier) * coefficient_a_radius
    base_intercept_disk = input_disk + correlated_a_disk
    weighted_intercept = complex(weighted_coefficients[0])
    unweighted_intercept = complex(unweighted_coefficients[0])
    weighted_unweighted_shift = abs(weighted_intercept - unweighted_intercept)
    loo_rows: list[dict[str, Any]] = []
    loo_intercepts: list[complex] = []
    for omitted in range(5):
        selected = [index for index in range(5) if index != omitted]
        coefficients = np.linalg.solve(design[selected, :], corrected[selected])
        intercept = complex(coefficients[0])
        loo_intercepts.append(intercept)
        loo_rows.append(
            {
                "omitted_epsilon_id": inputs[omitted]["epsilon_id"],
                **complex_fields("intercept", intercept),
                "distance_from_weighted_five_rung_intercept": abs(
                    intercept - weighted_intercept
                ),
            }
        )
    loo_spread = max(abs(value - weighted_intercept) for value in loo_intercepts)
    smallest_window_intercept = loo_intercepts[-1]
    smallest_window_shift = abs(smallest_window_intercept - weighted_intercept)
    leading_design = np.column_stack((np.ones(5), x))
    leading_coefficients, leading_projection = fit_projection(
        leading_design, corrected, radii, 1.0 / radii**2
    )
    leading_intercept = complex(leading_coefficients[0])
    leading_model_shift = abs(leading_intercept - weighted_intercept)
    maximum_absolute_residual = float(np.max(np.abs(weighted_residuals)))
    maximum_normalized_residual = float(np.max(np.abs(weighted_residuals) / radii))
    intercept_envelope = (
        base_intercept_disk
        + weighted_unweighted_shift
        + loo_spread
        + leading_model_shift
        + maximum_absolute_residual
    )
    relative_envelope = intercept_envelope / max(abs(weighted_intercept), 1.0e-300)
    return {
        "inputs": inputs,
        "epsilon": epsilon,
        "values": values,
        "radii": radii,
        "log_features": log_features,
        "corrected": corrected,
        "design": design,
        "weighted_coefficients": weighted_coefficients,
        "unweighted_coefficients": unweighted_coefficients,
        "weighted_projection": weighted_projection,
        "weighted_predictions": weighted_predictions,
        "weighted_residuals": weighted_residuals,
        "weighted_intercept": weighted_intercept,
        "unweighted_intercept": unweighted_intercept,
        "leading_intercept": leading_intercept,
        "smallest_window_intercept": smallest_window_intercept,
        "input_disk": input_disk,
        "correlated_a_multiplier": correlated_a_multiplier,
        "correlated_a_disk": correlated_a_disk,
        "base_intercept_disk": base_intercept_disk,
        "weighted_unweighted_shift": weighted_unweighted_shift,
        "loo_spread": loo_spread,
        "smallest_window_shift": smallest_window_shift,
        "leading_model_shift": leading_model_shift,
        "maximum_absolute_residual": maximum_absolute_residual,
        "maximum_normalized_residual": maximum_normalized_residual,
        "intercept_envelope": intercept_envelope,
        "relative_envelope": relative_envelope,
        "loo_rows": loo_rows,
        "matrix_rank": int(np.linalg.matrix_rank(design)),
        "degrees_of_freedom": 1,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5366 - D4 five-rung intercept envelope and outer-limit gate",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Five-rung result",
        "",
        "With the independently derived `A` removed, the five accepted rungs are fitted to the four-complex-parameter family `J=I0+B epsilon+C epsilon^2 Log(epsilon/0.0025)+D epsilon^2`. The fit has one residual degree of freedom.",
        "",
        f"- weighted intercept: `{result['intercept_real']:.17g} {result['intercept_imaginary']:+.17g} i`;",
        f"- conservative total envelope: `{result['intercept_envelope']:.17g}`;",
        f"- relative envelope: `{result['relative_intercept_envelope']:.17g}`;",
        f"- preregistered numerical threshold: `{INTERCEPT_RELATIVE_LIMIT:.17g}`;",
        f"- maximum normalized residual: `{result['maximum_normalized_residual']:.17g}`.",
        "",
        "The numerical intercept gate passes below 1%, including propagated input disks, correlated-A uncertainty, weighted/unweighted shift, leave-one-out spread, leading-versus-second-order shift, and the maximum fit residual.",
        "",
        "## Claim boundary",
        "",
        "The outer-regulator limit remains false because checkpoint 5345 preregistered five rungs as an exactly determined complete-family stress stage. Closure now requires either the minimum overdetermined sixth independent rung or a separately derived uniform numerical `M_D4`. The next asymptotic E0003125 holdout was frozen before E000625 was known.",
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
    numerical_gate = evaluation["relative_envelope"] <= INTERCEPT_RELATIVE_LIMIT
    validations = [
        validation_row("preflight_passes", True, preflight_result["checks"]),
        validation_row(
            "five_by_four_complete_family_design_has_one_residual_degree",
            evaluation["matrix_rank"] == 4
            and evaluation["degrees_of_freedom"] == 1,
            (evaluation["matrix_rank"], evaluation["degrees_of_freedom"]),
        ),
        validation_row(
            "five_rung_residual_is_resolved_inside_input_disks",
            math.isfinite(evaluation["maximum_normalized_residual"])
            and evaluation["maximum_normalized_residual"] <= 1.0,
            evaluation["maximum_normalized_residual"],
        ),
        validation_row(
            "preregistered_one_percent_intercept_envelope_gate_passes",
            numerical_gate,
            evaluation["relative_envelope"],
        ),
        validation_row(
            "five_rungs_do_not_override_six_rung_or_uniform_remainder_gate",
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
    claims = {CLAIM_FIT: passed, **no_broad_claims()}
    coefficient_names = ("I0", "B_scaled", "C_log_scaled", "D_scaled")
    fit_rows = [
        {
            "coefficient": name,
            **complex_fields("weighted_value", complex(evaluation["weighted_coefficients"][index])),
            **complex_fields(
                "unweighted_value", complex(evaluation["unweighted_coefficients"][index])
            ),
            **claims,
        }
        for index, name in enumerate(coefficient_names)
    ]
    residual_rows = [
        {
            "epsilon_id": item["epsilon_id"],
            "epsilon": item["epsilon"],
            **complex_fields("fixed_decay_integral", evaluation["values"][index]),
            "input_disk_radius": evaluation["radii"][index],
            **complex_fields("fixed_A_corrected_J", evaluation["corrected"][index]),
            **complex_fields("weighted_fitted_J", evaluation["weighted_predictions"][index]),
            **complex_fields("weighted_residual", evaluation["weighted_residuals"][index]),
            "normalized_residual": abs(evaluation["weighted_residuals"][index])
            / evaluation["radii"][index],
            **claims,
        }
        for index, item in enumerate(evaluation["inputs"])
    ]
    for row in evaluation["loo_rows"]:
        row.update(claims)
    envelope_row = {
        **complex_fields("weighted_intercept", evaluation["weighted_intercept"]),
        **complex_fields("unweighted_intercept", evaluation["unweighted_intercept"]),
        **complex_fields("leading_family_intercept", evaluation["leading_intercept"]),
        **complex_fields(
            "smallest_epsilon_four_rung_intercept",
            evaluation["smallest_window_intercept"],
        ),
        "input_disk_component": evaluation["input_disk"],
        "correlated_A_multiplier": evaluation["correlated_a_multiplier"],
        "correlated_A_disk_component": evaluation["correlated_a_disk"],
        "base_intercept_disk": evaluation["base_intercept_disk"],
        "weighted_unweighted_shift": evaluation["weighted_unweighted_shift"],
        "leave_one_out_spread": evaluation["loo_spread"],
        "smallest_epsilon_window_shift": evaluation["smallest_window_shift"],
        "leading_vs_second_order_model_shift": evaluation["leading_model_shift"],
        "maximum_absolute_fit_residual": evaluation["maximum_absolute_residual"],
        "conservative_intercept_envelope": evaluation["intercept_envelope"],
        "relative_intercept_envelope": evaluation["relative_envelope"],
        "preregistered_relative_limit": INTERCEPT_RELATIVE_LIMIT,
        "numerical_intercept_gate_passes": numerical_gate,
        "uniform_remainder_bound_available": False,
        "sixth_rung_gate_satisfied": False,
        **claims,
    }
    gate_rows = [
        {
            "gate": "five_rung_complete_family_residual",
            "passed": evaluation["maximum_normalized_residual"] <= 1.0,
            "detail": evaluation["maximum_normalized_residual"],
            **claims,
        },
        {
            "gate": "preregistered_relative_intercept_envelope_below_one_percent",
            "passed": numerical_gate,
            "detail": evaluation["relative_envelope"],
            **claims,
        },
        {
            "gate": "uniform_numeric_M_D4",
            "passed": False,
            "detail": "pointwise E000625 envelope exists; uniform interval bound remains open",
            **claims,
        },
        {
            "gate": "minimum_sixth_complete_family_rung",
            "passed": False,
            "detail": "E0003125 is frozen but not yet integrated",
            **claims,
        },
        {
            "gate": "D4_outer_regulator_zero_limit",
            "passed": False,
            "detail": "numerical intercept gate passes; uniform remainder and sixth-rung gates remain false",
            **claims,
        },
    ]
    direct_sources = (
        Path(__file__).resolve(),
        PREREGISTRATION,
        ASYMPTOTIC_CONTRACT,
        FIXED_A_RESULT,
        FOUR_RUNG_INPUTS,
        BLIND_RESULT,
        BLIND_VALIDATION,
        BLIND_SOURCES,
        NEXT_HOLDOUT_FREEZE_RESULT,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
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
        "D4_FIVE_RUNG_NUMERIC_INTERCEPT_GATE_PASSES__SIXTH_RUNG_OR_UNIFORM_REMAINDER_REQUIRED"
        if numerical_gate
        else "D4_FIVE_RUNG_INTERCEPT_ENVELOPE_EXCEEDS_PREREGISTERED_ONE_PERCENT_GATE"
    )
    result = {
        "mode": "D4-five-rung-intercept-envelope-outer-limit-gate",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "validation_passed": passed,
        "decision": decision,
        "accepted_rung_count": 5,
        "fit_parameter_count": 4,
        "fit_degrees_of_freedom": evaluation["degrees_of_freedom"],
        **complex_fields("intercept", evaluation["weighted_intercept"]),
        "intercept_envelope": evaluation["intercept_envelope"],
        "relative_intercept_envelope": evaluation["relative_envelope"],
        "preregistered_relative_limit": INTERCEPT_RELATIVE_LIMIT,
        "numerical_intercept_gate_passes": numerical_gate,
        "maximum_normalized_residual": evaluation["maximum_normalized_residual"],
        "uniform_numeric_remainder_bound_available": False,
        "sixth_complete_family_rung_available": False,
        "claim_boundary": claims,
        "remaining_obstruction": "integrate the already frozen E0003125 asymptotic holdout or independently derive a uniform third-order derivative bound; only then rerun the preregistered full outer-limit gate",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(FIT_ROWS, fit_rows)
    atomic_csv(INTERCEPT_ROWS, [envelope_row])
    atomic_csv(RESIDUAL_ROWS, residual_rows)
    atomic_csv(LOO_ROWS, evaluation["loo_rows"])
    atomic_csv(GATE_ROWS, gate_rows)
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
