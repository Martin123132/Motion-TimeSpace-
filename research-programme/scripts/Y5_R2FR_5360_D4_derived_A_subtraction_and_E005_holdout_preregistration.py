from __future__ import annotations

import argparse
import cmath
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
OUTPUT = FUNCTIONAL_RG / "5360"
DOCUMENT = (
    POST
    / "5360-Y5-R2FR-D4-derived-A-subtraction-and-E005-holdout-preregistration.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5360_VALIDATION.csv"

CONTRACT_5345 = (
    FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
)
DOCUMENT_5345 = (
    POST
    / "5345-Y5-R2FR-D4-regulator-zero-endpoint-asymptotic-and-fit-preregistration.md"
)
RESULT_5358 = (
    FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
)
VALIDATION_5358 = (
    FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_validation.csv"
)
RESULT_5359 = (
    FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
)
VALIDATION_5359 = (
    FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
)
SUM_5359 = (
    FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_sum_comparison.csv"
)
E00125_FINITE = (
    FUNCTIONAL_RG
    / "5334"
    / "E00125"
    / "D4_outer_event_aligned_E00125_finite_value.csv"
)
E00125_RESULT = (
    FUNCTIONAL_RG
    / "5334"
    / "E00125"
    / "D4_outer_event_aligned_E00125_result.json"
)
E0025_FINITE = FUNCTIONAL_RG / "5340" / "D4_E0025_log_corrected_finite_value.csv"
E0025_RESULT = (
    FUNCTIONAL_RG / "5340" / "D4_E0025_log_corrected_canonical_result.json"
)
E005_ROOT = FUNCTIONAL_RG / "5334" / "E005"
E005_STATUS = E005_ROOT / "status.json"
E005_RESULT = E005_ROOT / "D4_outer_event_aligned_E005_result.json"
E005_MANIFEST = E005_ROOT / "D4_outer_event_aligned_E005_node_manifest.csv"

CHECKPOINT = 5360
MARKER = "MTS_5360_D4_DERIVED_A_SUBTRACTION_E005_HOLDOUT_PREREGISTRATION"
REVISION = "D4-derived-A-subtraction-E005-holdout-preregistration-v1"
CHECKED_DATE = "2026-08-11"
EPSILON_REFERENCE = 0.0025
E005_EPSILON = 0.005
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_SUBTRACTION = "valid_for_D4_derived_A_integral_subtraction"
CLAIM_PREREGISTRATION = "valid_for_D4_E005_fixed_A_holdout_preregistration"
CLAIM_REMAINDER_FORM = "valid_for_D4_conditional_fixed_A_remainder_normal_form"
FALSE_CLAIMS = (
    "valid_for_D4_E005_fixed_A_holdout_compatibility",
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

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


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


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


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


def no_broad_claims() -> dict[str, bool]:
    return {claim: False for claim in FALSE_CLAIMS}


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def source_chain_current(payload: dict[str, Any]) -> tuple[bool, int]:
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0
    for row in rows:
        path = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if not path.is_file() or len(expected) != 64 or digest(path) != expected:
            return False, len(rows)
    return True, len(rows)


def csv_validation_passes(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row.get("passed", False)) for row in rows)


def load_coefficient() -> dict[str, Any]:
    payload = read_json(RESULT_5359)
    value = complex(
        float(payload["A_total_zero_real"]),
        float(payload["A_total_zero_imaginary"]),
    )
    radius = float(payload["A_total_zero_disk_radius"])
    sources_current, source_count = source_chain_current(payload)
    checks = {
        "validation_passed": payload.get("validation_passed") is True,
        "coefficient_limit_signed": payload.get("claim_boundary", {}).get(
            "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
        )
        is True,
        "value_finite": finite_complex(value),
        "radius_finite_nonnegative": math.isfinite(radius) and radius >= 0.0,
        "source_chain_current": sources_current and source_count > 0,
        "saved_validation_passes": csv_validation_passes(VALIDATION_5359),
        "integrated_limit_still_false": payload.get("claim_boundary", {}).get(
            "valid_for_D4_outer_regulator_zero_limit"
        )
        is False,
    }
    return {
        "value": value,
        "radius": radius,
        "payload": payload,
        "checks": checks,
        "valid": all(checks.values()),
    }


def load_rung(
    epsilon_id: str,
    epsilon: float,
    finite_path: Path,
    result_path: Path,
) -> dict[str, Any]:
    rows = read_csv(finite_path)
    if len(rows) != 1:
        raise RuntimeError(f"expected one finite row in {finite_path}, found {len(rows)}")
    row = rows[0]
    payload = read_json(result_path)
    value = complex(
        float(row["fixed_decay_integral_real"]),
        float(row["fixed_decay_integral_imaginary"]),
    )
    radius = float(row["total_error_absolute_conservative"])
    claim = f"valid_for_D4_outer_{epsilon_id}_fixed_decay_integral"
    sources_current, source_count = source_chain_current(payload)
    payload_value = complex(
        float(payload["fixed_decay_integral_real"]),
        float(payload["fixed_decay_integral_imaginary"]),
    )
    payload_radius = float(payload["total_error_absolute_conservative"])
    checks = {
        "epsilon_identity_matches": row.get("epsilon_id") == epsilon_id
        and abs(float(row["epsilon"]) - epsilon) <= 1.0e-15,
        "finite_row_accepted": parse_bool(
            row.get("finite_regulator_fixed_decay_integral_accepted", False)
        ),
        "finite_row_claim_signed": parse_bool(row.get(claim, False)),
        "value_and_radius_finite": finite_complex(value)
        and math.isfinite(radius)
        and radius >= 0.0,
        "result_completed_and_accepted": parse_bool(
            payload.get("completed_full_run", False)
        )
        and parse_bool(payload.get("acceptance_passed", False)),
        "result_claim_signed": parse_bool(
            payload.get("claim_boundary", {}).get(claim, False)
        ),
        "finite_and_result_values_match": abs(value - payload_value)
        <= 1.0e-14 * max(abs(value), 1.0)
        and abs(radius - payload_radius) <= 1.0e-14 * max(radius, 1.0),
        "source_chain_current": sources_current and source_count > 0,
        "regulator_zero_claim_false": not parse_bool(
            payload.get("claim_boundary", {}).get(
                "valid_for_D4_outer_regulator_zero_limit", False
            )
        ),
    }
    return {
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "value": value,
        "radius": radius,
        "finite_path": finite_path.resolve(),
        "result_path": result_path.resolve(),
        "checks": checks,
        "valid": all(checks.values()),
    }


def model_log(epsilon: float) -> float:
    return epsilon * math.log(epsilon / EPSILON_REFERENCE)


def evaluate_two_rung_prediction(
    coefficient: dict[str, Any], rungs: list[dict[str, Any]]
) -> dict[str, Any]:
    first, second = rungs
    first_function = model_log(first["epsilon"])
    second_function = model_log(second["epsilon"])
    target_function = model_log(E005_EPSILON)
    coefficient_value = coefficient["value"]
    coefficient_radius = coefficient["radius"]
    first_corrected = first["value"] - coefficient_value * first_function
    second_corrected = second["value"] - coefficient_value * second_function
    separation = second["epsilon"] - first["epsilon"]
    first_prediction_weight = (second["epsilon"] - E005_EPSILON) / separation
    second_prediction_weight = (E005_EPSILON - first["epsilon"]) / separation
    first_intercept_weight = second["epsilon"] / separation
    second_intercept_weight = -first["epsilon"] / separation
    slope = (second_corrected - first_corrected) / separation
    intercept = (
        first_intercept_weight * first_corrected
        + second_intercept_weight * second_corrected
    )
    corrected_prediction = (
        first_prediction_weight * first_corrected
        + second_prediction_weight * second_corrected
    )
    integral_prediction = corrected_prediction + coefficient_value * target_function
    coefficient_multiplier = (
        target_function
        - first_prediction_weight * first_function
        - second_prediction_weight * second_function
    )
    prediction_data_radius = (
        abs(first_prediction_weight) * first["radius"]
        + abs(second_prediction_weight) * second["radius"]
    )
    prediction_coefficient_radius = abs(coefficient_multiplier) * coefficient_radius
    prediction_radius = prediction_data_radius + prediction_coefficient_radius
    intercept_coefficient_multiplier = -(
        first_intercept_weight * first_function
        + second_intercept_weight * second_function
    )
    intercept_radius = (
        abs(first_intercept_weight) * first["radius"]
        + abs(second_intercept_weight) * second["radius"]
        + abs(intercept_coefficient_multiplier) * coefficient_radius
    )
    corrected_rows = []
    for rung, function_value, corrected in (
        (first, first_function, first_corrected),
        (second, second_function, second_corrected),
    ):
        corrected_rows.append(
            {
                "epsilon_id": rung["epsilon_id"],
                "epsilon": rung["epsilon"],
                "epsilon_log_epsilon_over_reference": function_value,
                **complex_fields("fixed_decay_integral", rung["value"]),
                "fixed_decay_integral_disk_radius": rung["radius"],
                **complex_fields("derived_A_log_subtracted_J", corrected),
                "derived_A_log_subtracted_disk_radius": rung["radius"]
                + abs(function_value) * coefficient_radius,
                "source_path": str(rung["finite_path"]),
                "source_sha256": digest(rung["finite_path"]),
            }
        )
    prediction_row = {
        "holdout_epsilon_id": "E005",
        "holdout_epsilon": E005_EPSILON,
        "frozen_before_accepted_E005_value": True,
        "source_rung_ids": "E00125|E0025",
        "first_prediction_weight": first_prediction_weight,
        "second_prediction_weight": second_prediction_weight,
        "coefficient_multiplier": coefficient_multiplier,
        **complex_fields("predicted_fixed_decay_integral", integral_prediction),
        "prediction_data_disk_radius": prediction_data_radius,
        "prediction_coefficient_disk_radius": prediction_coefficient_radius,
        "prediction_total_disk_radius": prediction_radius,
        "comparison_to_measured_E005_performed": False,
        "measured_E005_value": "NOT_YET_ACCEPTED",
    }
    fit_row = {
        "model_id": "D4_FIXED_A_TWO_RUNG_AFFINE_J",
        "basis_terms": "1|epsilon",
        "input_rung_ids": "E00125|E0025",
        "parameter_count": 2,
        "point_count": 2,
        "degrees_of_freedom": 0,
        **complex_fields("provisional_I0", intercept),
        "provisional_I0_input_disk_radius": intercept_radius,
        "provisional_I0_relative_input_disk_radius": intercept_radius
        / max(abs(intercept), 1.0e-300),
        **complex_fields("provisional_B", slope),
        "fit_is_exactly_determined": True,
        "residual_test_available": False,
        "outer_regulator_zero_limit_claimed": False,
    }
    return {
        "corrected_rows": corrected_rows,
        "prediction_row": prediction_row,
        "fit_row": fit_row,
        "intercept": intercept,
        "intercept_radius": intercept_radius,
        "slope": slope,
        "prediction": integral_prediction,
        "prediction_radius": prediction_radius,
        "weights": (
            first_prediction_weight,
            second_prediction_weight,
            first_intercept_weight,
            second_intercept_weight,
        ),
    }


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "DA5360_00_parent_local_integrand",
            "hypotheses": "separated transverse event; affine numerator; analytic event branch",
            "derived_statement": "F_e(delta,epsilon)=s_e(C0_e+C1_e delta) Log(z0_e+z1_e delta)",
            "consequence": "the endpoint primitive is elementary and its logarithmic coefficient is parent-owned",
            "status": "DERIVED_BY_5342_5345_5358_5359",
        },
        {
            "contract_id": "DA5360_01_exact_endpoint_primitive",
            "hypotheses": "u=z0+z1 delta; z1 nonzero",
            "derived_statement": "Phi=s[(C0/z1-C1*z0/z1^2)(u Log u-u)+(C1/z1^2)(u^2 Log u/2-u^2/4)]",
            "consequence": "dPhi/ddelta=s(C0+C1 delta) Log(z0+z1 delta)",
            "status": "EXACT_ALGEBRA",
        },
        {
            "contract_id": "DA5360_02_lower_log_coefficient",
            "hypotheses": "evaluate minus the primitive at u=z0",
            "derived_statement": "H_e=-s_e[C0_e z0_e/z1_e-(C1_e/2)(z0_e/z1_e)^2]",
            "consequence": "H_e=A_e epsilon+C_e epsilon^2+O(epsilon^3)",
            "status": "EXACT_ALGEBRA_PLUS_ANALYTIC_EXPANSION",
        },
        {
            "contract_id": "DA5360_03_derived_A_subtraction",
            "hypotheses": "A=sum_e lim H_e/epsilon is the checkpoint-5359 coefficient",
            "derived_statement": "J(epsilon)=I(epsilon)-A epsilon Log(epsilon/epsilon_ref)",
            "consequence": "J=I0+B epsilon+C epsilon^2 Log(epsilon/epsilon_ref)+D epsilon^2+R3",
            "status": "DERIVED_COEFFICIENT_NOT_FITTED",
        },
        {
            "contract_id": "DA5360_04_conditional_remainder_existence",
            "hypotheses": "event branches analytic on a common closed regulator interval; denominators uniformly nonzero; away region compact and C3",
            "derived_statement": "there exists finite M_D4 with |R3|<=M_D4 epsilon^3[1+|Log(epsilon/epsilon_ref)|]",
            "consequence": "existence follows by finite event cover and Taylor remainder, but no numerical M_D4 is supplied",
            "status": "CONDITIONAL_THEOREM_NUMERIC_CONSTANT_OPEN",
        },
        {
            "contract_id": "DA5360_05_claim_boundary",
            "hypotheses": "only two accepted integrated rungs and no numerical M_D4",
            "derived_statement": "the fixed-A affine line supplies a frozen E005 prediction only",
            "consequence": "no complete second-order fit or outer-regulator limit may be claimed",
            "status": "ENFORCED",
        },
    ]


def rung_count_rows() -> list[dict[str, Any]]:
    rows = []
    for count in range(2, 8):
        leading_status = (
            "EXACTLY_DETERMINED_NO_RESIDUAL_TEST"
            if count == 2
            else "OVERDETERMINED"
        )
        if count < 4:
            complete_status = "UNDERDETERMINED"
        elif count == 4:
            complete_status = "EXACTLY_DETERMINED_NO_RESIDUAL_TEST"
        else:
            complete_status = "OVERDETERMINED"
        if count == 2:
            decision = "FREEZE_NEXT_RUNG_HOLDOUT_PREDICTION"
        elif count == 3:
            decision = "FIXED_A_LEADING_FAMILY_HOLDOUT_GATE"
        elif count == 4:
            decision = "COMPLETE_FAMILY_EXACT_NO_COMPLETE_RESIDUAL_TEST"
        elif count == 5:
            decision = "MINIMUM_COMPLETE_FIXED_A_OVERDETERMINED_GATE"
        else:
            decision = "PREFERRED_FIXED_A_STABILITY_LADDER"
        rows.append(
            {
                "accepted_rung_count": count,
                "fixed_A_leading_parameter_count": 2,
                "fixed_A_leading_status": leading_status,
                "fixed_A_complete_parameter_count": 4,
                "fixed_A_complete_status": complete_status,
                "allowed_decision": decision,
            }
        )
    return rows


def primitive(
    delta: complex,
    coefficient_0: complex,
    coefficient_1: complex,
    z_0: complex,
    z_1: complex,
    sign: int,
) -> complex:
    u = z_0 + z_1 * delta
    return sign * (
        (coefficient_0 / z_1 - coefficient_1 * z_0 / z_1**2)
        * (u * cmath.log(u) - u)
        + (coefficient_1 / z_1**2)
        * (0.5 * u**2 * cmath.log(u) - 0.25 * u**2)
    )


def algebra_self_test() -> dict[str, Any]:
    coefficient_0 = 1.3 - 0.2j
    coefficient_1 = -0.7 + 0.1j
    z_0 = 0.2 + 0.3j
    z_1 = 1.1 - 0.4j
    delta = 0.37
    step = 1.0e-6
    derivative = (
        primitive(delta + step, coefficient_0, coefficient_1, z_0, z_1, -1)
        - primitive(delta - step, coefficient_0, coefficient_1, z_0, z_1, -1)
    ) / (2.0 * step)
    expected = -(
        coefficient_0 + coefficient_1 * delta
    ) * cmath.log(z_0 + z_1 * delta)
    intercept = 2.0 - 0.4j
    coefficient = 0.1 + 0.47j
    slope = -3.0 + 0.2j
    epsilon_1 = 0.00125
    epsilon_2 = 0.0025
    epsilon_3 = 0.005
    values = [
        intercept + coefficient * model_log(epsilon) + slope * epsilon
        for epsilon in (epsilon_1, epsilon_2)
    ]
    corrected = [
        value - coefficient * model_log(epsilon)
        for value, epsilon in zip(values, (epsilon_1, epsilon_2), strict=True)
    ]
    weight_1 = (epsilon_2 - epsilon_3) / (epsilon_2 - epsilon_1)
    weight_2 = (epsilon_3 - epsilon_1) / (epsilon_2 - epsilon_1)
    prediction = (
        weight_1 * corrected[0]
        + weight_2 * corrected[1]
        + coefficient * model_log(epsilon_3)
    )
    truth = intercept + coefficient * model_log(epsilon_3) + slope * epsilon_3
    checks = {
        "primitive_derivative_recovers_integrand": abs(derivative - expected) <= 1.0e-9,
        "dyadic_prediction_weights_are_minus_two_three": abs(weight_1 + 2.0)
        <= 1.0e-15
        and abs(weight_2 - 3.0) <= 1.0e-15,
        "fixed_A_two_rung_prediction_recovers_synthetic_truth": abs(prediction - truth)
        <= 1.0e-13,
        "broad_claims_default_false": all(
            value is False for value in no_broad_claims().values()
        ),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def preflight() -> dict[str, Any]:
    required = [
        Path(__file__).resolve(),
        CONTRACT_5345,
        DOCUMENT_5345,
        RESULT_5358,
        VALIDATION_5358,
        RESULT_5359,
        VALIDATION_5359,
        SUM_5359,
        E00125_FINITE,
        E00125_RESULT,
        E0025_FINITE,
        E0025_RESULT,
        E005_STATUS,
        E005_RESULT,
        E005_MANIFEST,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    coefficient = load_coefficient()
    rungs = [
        load_rung("E00125", 0.00125, E00125_FINITE, E00125_RESULT),
        load_rung("E0025", 0.0025, E0025_FINITE, E0025_RESULT),
    ]
    status = read_json(E005_STATUS)
    partial_result = read_json(E005_RESULT)
    contract = read_csv(CONTRACT_5345)
    result_5358 = read_json(RESULT_5358)
    tests = algebra_self_test()
    checks = {
        "coefficient_is_source_complete": coefficient["valid"],
        "two_integrated_rungs_are_accepted": all(rung["valid"] for rung in rungs),
        "checkpoint_5345_contract_passes": bool(contract)
        and all(parse_bool(row.get("contract_passes", False)) for row in contract),
        "checkpoint_5358_continuation_passes": result_5358.get(
            "validation_passed"
        )
        is True
        and csv_validation_passes(VALIDATION_5358),
        "E005_is_not_yet_an_accepted_measurement": status.get("state")
        == "PAUSED_RESUMABLE"
        and not parse_bool(partial_result.get("acceptance_passed", False))
        and not parse_bool(partial_result.get("completed_full_run", False)),
        "algebra_self_test_passes": tests["all_pass"],
        "formal_workbench_inventory_unchanged": formal_inventory_digest()
        == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "coefficient_checks": coefficient["checks"],
        "rung_checks": {rung["epsilon_id"]: rung["checks"] for rung in rungs},
        "E005_state": status,
    }


def render_document(result: dict[str, Any]) -> None:
    prediction = complex(
        result["E005_frozen_prediction_real"],
        result["E005_frozen_prediction_imaginary"],
    )
    intercept = complex(
        result["provisional_I0_real"], result["provisional_I0_imaginary"]
    )
    lines = [
        "# 5360 - D4 derived-A subtraction and E005 holdout preregistration",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Actual derivation",
        "",
        "For each endpoint normal form, substituting `u=z0+z1 delta` gives the exact primitive",
        "",
        "`Phi=s[(C0/z1-C1 z0/z1^2)(u Log u-u)+(C1/z1^2)(u^2 Log u/2-u^2/4)]`.",
        "",
        "Its lower-end logarithmic coefficient is",
        "",
        "`H_e=-s_e[C0_e z0_e/z1_e-(C1_e/2)(z0_e/z1_e)^2]`.",
        "",
        "The analytic event continuations imply `H_e=A_e epsilon+C_e epsilon^2+O(epsilon^3)`.  Therefore checkpoint 5359's directly derived total `A` is subtracted rather than fitted:",
        "",
        "`J(epsilon)=I(epsilon)-A epsilon Log(epsilon/0.0025)`.",
        "",
        "The fixed-A family has four remaining complex coefficients:",
        "",
        "`J=I0+B epsilon+C epsilon^2 Log(epsilon/0.0025)+D epsilon^2+R3`.",
        "",
        "## Frozen E005 holdout",
        "",
        "Only the independently accepted `E00125` and corrected `E0025` integrated rungs are used.  Their fixed-A affine line was frozen before an accepted E005 value existed.",
        "",
        f"- predicted E005 integral: `{prediction.real:.17g} {prediction.imag:+.17g} i`;",
        f"- conservative prediction disk: `{result['E005_frozen_prediction_disk_radius']:.17g}`;",
        f"- provisional affine intercept: `{intercept.real:.17g} {intercept.imag:+.17g} i`;",
        f"- input-only intercept disk: `{result['provisional_I0_input_disk_radius']:.17g}`.",
        "",
        "The E005 comparison has not been performed.  Its integration is resumably paused, so no compatibility result is implied by the prediction.",
        "",
        "## Remainder boundary",
        "",
        "A finite `M_D4` exists conditionally on a common closed analytic regulator interval, uniformly nonzero denominators, and a compact `C3` away region:",
        "",
        "`|R3| <= M_D4 epsilon^3[1+|Log(epsilon/0.0025)|]`.",
        "",
        "This checkpoint does not calculate a numerical `M_D4`.  Consequently the provisional intercept is not a regulator-zero result.",
        "",
        "## Claim boundary",
        "",
        f"- derived-A subtraction: `{result['claim_boundary'][CLAIM_SUBTRACTION]}`;",
        f"- pre-measurement E005 holdout freeze: `{result['claim_boundary'][CLAIM_PREREGISTRATION]}`;",
        f"- conditional remainder normal form: `{result['claim_boundary'][CLAIM_REMAINDER_FORM]}`;",
        "- E005 compatibility, numeric remainder, complete second-order fit, outer-regulator, decay-angle, UV, local-GR and full-MTS claims: `False`.",
        "",
        "## Next obstruction",
        "",
        "Resume the saved E005 shards, validate the accepted finite value, and compare it to this frozen disk before any refit.  If compatible, use the three fixed-A rungs as the first overdetermined leading-family test.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    coefficient = load_coefficient()
    rungs = [
        load_rung("E00125", 0.00125, E00125_FINITE, E00125_RESULT),
        load_rung("E0025", 0.0025, E0025_FINITE, E0025_RESULT),
    ]
    evaluation = evaluate_two_rung_prediction(coefficient, rungs)
    status = read_json(E005_STATUS)
    partial_result = read_json(E005_RESULT)
    manifest_rows = read_csv(E005_MANIFEST)
    snapshot_rows = [
        {
            "snapshot_role": "PRE_ACCEPTED_E005_HOLDOUT_FREEZE",
            "source_status_path": str(E005_STATUS.resolve()),
            "source_status_sha256_at_freeze": digest(E005_STATUS),
            "source_partial_result_path": str(E005_RESULT.resolve()),
            "source_partial_result_sha256_at_freeze": digest(E005_RESULT),
            "source_manifest_path": str(E005_MANIFEST.resolve()),
            "source_manifest_sha256_at_freeze": digest(E005_MANIFEST),
            "state": status.get("state", ""),
            "decision": status.get("decision", ""),
            "encountered_node_count": status.get("encountered_node_count", ""),
            "completed_node_count": status.get("completed_node_count", ""),
            "manifest_row_count": len(manifest_rows),
            "completed_full_run": partial_result.get("completed_full_run", False),
            "acceptance_passed": partial_result.get("acceptance_passed", False),
            "accepted_E005_numeric_value_read_by_checkpoint": False,
            "snapshot_utc": utc_now(),
        }
    ]
    contract = contract_rows()
    rung_counts = rung_count_rows()
    direct_sources = [
        Path(__file__).resolve(),
        CONTRACT_5345.resolve(),
        DOCUMENT_5345.resolve(),
        RESULT_5358.resolve(),
        VALIDATION_5358.resolve(),
        RESULT_5359.resolve(),
        VALIDATION_5359.resolve(),
        SUM_5359.resolve(),
        E00125_FINITE.resolve(),
        E00125_RESULT.resolve(),
        E0025_FINITE.resolve(),
        E0025_RESULT.resolve(),
    ]
    direct_sources = sorted(set(direct_sources), key=lambda path: str(path).lower())
    prediction = evaluation["prediction_row"]
    fit = evaluation["fit_row"]
    first_weight, second_weight, first_intercept, second_intercept = evaluation[
        "weights"
    ]
    validations = [
        validation_row("preflight_passes", preflight_result["all_pass"], preflight_result["checks"]),
        validation_row("derived_A_is_source_complete_and_not_fitted", coefficient["valid"], coefficient["checks"]),
        validation_row("exactly_two_accepted_integrated_input_rungs", [rung["epsilon_id"] for rung in rungs] == ["E00125", "E0025"] and all(rung["valid"] for rung in rungs), [rung["checks"] for rung in rungs]),
        validation_row("E005_prediction_is_frozen_before_measurement_acceptance", status.get("state") == "PAUSED_RESUMABLE" and partial_result.get("acceptance_passed") is False and prediction["comparison_to_measured_E005_performed"] is False, snapshot_rows[0]),
        validation_row("dyadic_prediction_weights_are_exact", abs(first_weight + 2.0) <= 1.0e-15 and abs(second_weight - 3.0) <= 1.0e-15, (first_weight, second_weight)),
        validation_row("dyadic_intercept_weights_are_exact", abs(first_intercept - 2.0) <= 1.0e-15 and abs(second_intercept + 1.0) <= 1.0e-15, (first_intercept, second_intercept)),
        validation_row("prediction_disk_propagates_both_input_disks_and_correlated_A_disk", prediction["prediction_total_disk_radius"] >= prediction["prediction_data_disk_radius"] >= 0.0 and prediction["prediction_coefficient_disk_radius"] >= 0.0, prediction),
        validation_row("fixed_A_rung_count_reduction_is_enforced", rung_counts[0]["accepted_rung_count"] == 2 and rung_counts[1]["allowed_decision"] == "FIXED_A_LEADING_FAMILY_HOLDOUT_GATE" and rung_counts[3]["allowed_decision"] == "MINIMUM_COMPLETE_FIXED_A_OVERDETERMINED_GATE", len(rung_counts)),
        validation_row("remainder_is_conditional_and_numeric_constant_remains_open", contract[4]["status"] == "CONDITIONAL_THEOREM_NUMERIC_CONSTANT_OPEN" and no_broad_claims()["valid_for_D4_numeric_remainder_bound"] is False, contract[4]),
        validation_row("algebra_self_test_passes", algebra_self_test()["all_pass"], algebra_self_test()["checks"]),
        validation_row("all_broader_claims_remain_false", all(value is False for value in no_broad_claims().values()), no_broad_claims()),
        validation_row("formal_workbench_remains_unchanged", formal_inventory_digest() == FORMAL_DIGEST, formal_inventory_digest()),
        validation_row("scripts_cache_remains_absent", not (SCRIPTS / "__pycache__").exists(), SCRIPTS / "__pycache__"),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_SUBTRACTION: passed,
        CLAIM_PREREGISTRATION: passed,
        CLAIM_REMAINDER_FORM: passed,
        **no_broad_claims(),
    }
    for collection in (
        contract,
        rung_counts,
        evaluation["corrected_rows"],
        [prediction],
        [fit],
        snapshot_rows,
    ):
        for row in collection:
            row.update(claims)
    source_rows = [
        {
            "path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in direct_sources
    ]
    result = {
        "mode": "D4-derived-A-subtraction-and-E005-holdout-preregistration",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "validation_passed": passed,
        "decision": (
            "D4_DERIVED_A_SUBTRACTION_AND_E005_HOLDOUT_FROZEN__RESUME_E005"
            if passed
            else "D4_DERIVED_A_SUBTRACTION_OR_HOLDOUT_FREEZE_BLOCKED"
        ),
        "accepted_integrated_rung_ids": [rung["epsilon_id"] for rung in rungs],
        "accepted_integrated_rung_count": len(rungs),
        "A_zero_real": coefficient["value"].real,
        "A_zero_imaginary": coefficient["value"].imag,
        "A_zero_disk_radius": coefficient["radius"],
        "E005_frozen_prediction_real": evaluation["prediction"].real,
        "E005_frozen_prediction_imaginary": evaluation["prediction"].imag,
        "E005_frozen_prediction_disk_radius": evaluation["prediction_radius"],
        "provisional_I0_real": evaluation["intercept"].real,
        "provisional_I0_imaginary": evaluation["intercept"].imag,
        "provisional_I0_input_disk_radius": evaluation["intercept_radius"],
        "provisional_I0_is_outer_regulator_limit": False,
        "E005_measurement_comparison_performed": False,
        "numeric_remainder_constant_available": False,
        "claim_boundary": claims,
        "remaining_obstruction": "complete and validate the resumable E005 integration, then compare its accepted disk to this frozen prediction before any refit",
        "formalization_workbench_modified_file_count": 0,
        "source_files": [
            {"path": str(path), "sha256": digest(path)} for path in direct_sources
        ],
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_fixed_A_integral_subtraction_contract.csv", contract)
    atomic_csv(output / "D4_fixed_A_accepted_integrated_inputs.csv", [
        {
            "epsilon_id": rung["epsilon_id"],
            "epsilon": rung["epsilon"],
            **complex_fields("fixed_decay_integral", rung["value"]),
            "total_error_absolute_conservative": rung["radius"],
            "source_path": str(rung["finite_path"]),
            "source_sha256": digest(rung["finite_path"]),
            **claims,
        }
        for rung in rungs
    ])
    atomic_csv(output / "D4_fixed_A_log_subtracted_rungs.csv", evaluation["corrected_rows"])
    atomic_csv(output / "D4_fixed_A_E005_frozen_prediction.csv", [prediction])
    atomic_csv(output / "D4_fixed_A_two_rung_affine_fit.csv", [fit])
    atomic_csv(output / "D4_fixed_A_rung_count_gate.csv", rung_counts)
    atomic_csv(output / "D4_E005_pre_measurement_execution_snapshot.csv", snapshot_rows)
    atomic_csv(output / "D4_fixed_A_subtraction_validation.csv", validations)
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_fixed_A_subtraction_result.json", result)
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
    validation_path = output / "D4_fixed_A_subtraction_validation.csv"
    result_path = output / "D4_fixed_A_subtraction_result.json"
    source_path = output / "source_register.csv"
    checks = {
        "validation_file_passes": validation_path.is_file()
        and csv_validation_passes(validation_path),
        "residual_validation_passes": VALIDATION.is_file()
        and csv_validation_passes(VALIDATION),
        "result_validation_passes": result_path.is_file()
        and read_json(result_path).get("validation_passed") is True,
        "registered_immutable_sources_are_current": source_path.is_file()
        and all(
            Path(row["path"]).is_file()
            and digest(Path(row["path"])) == row["sha256"]
            for row in read_csv(source_path)
        ),
        "document_exists": DOCUMENT.is_file(),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"mode": "validate-saved", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    set_below_normal_priority()
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        tests = algebra_self_test()
        payload = {"mode": "self-test", **tests}
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
