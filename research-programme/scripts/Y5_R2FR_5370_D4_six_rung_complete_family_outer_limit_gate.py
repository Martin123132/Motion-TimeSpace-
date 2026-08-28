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

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"

PREREG_RESULT = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_preregistration_result.json"
ASYMPTOTIC_CONTRACT = (
    FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
)
FIT_PREREGISTRATION = FUNCTIONAL_RG / "5345" / "D4_zero_fit_preregistration.csv"
RUNG_PREREGISTRATION = FUNCTIONAL_RG / "5345" / "D4_zero_rung_count_gate.csv"

FIXED_A_RESULT = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
FIXED_A_VALIDATION = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_validation.csv"
FIXED_A_RUNG_GATE = FUNCTIONAL_RG / "5360" / "D4_fixed_A_rung_count_gate.csv"
FOUR_RUNG_INPUTS = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_four_rung_inputs.csv"
FIVE_RUNG_RESULT = FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_result.json"
FIVE_RUNG_VALIDATION = (
    FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_validation.csv"
)

COMPARATOR_ROOT = FUNCTIONAL_RG / "5369" / "E0003125"
COMPARATOR_CONTRACT = COMPARATOR_ROOT / "D4_E0003125_blind_holdout_comparison_contract.json"
COMPARATOR_CONTRACT_VALIDATION = (
    COMPARATOR_ROOT / "D4_E0003125_blind_holdout_comparison_contract_validation.csv"
)
COMPARATOR_CONTRACT_SOURCES = (
    COMPARATOR_ROOT / "D4_E0003125_blind_holdout_comparison_contract_sources.csv"
)
COMPARATOR_RESULT = COMPARATOR_ROOT / "D4_E0003125_blind_holdout_comparison_result.json"
COMPARATOR_VALIDATION = (
    COMPARATOR_ROOT / "D4_E0003125_blind_holdout_comparison_validation.csv"
)
COMPARATOR_SOURCES = COMPARATOR_ROOT / "source_register.csv"

E000625_ROOT = FUNCTIONAL_RG / "5334" / "E000625"
E000625_FINITE = E000625_ROOT / "D4_outer_event_aligned_E000625_finite_value.csv"
E000625_RESULT = E000625_ROOT / "D4_outer_event_aligned_E000625_result.json"
E000625_VALIDATION = E000625_ROOT / "D4_outer_event_aligned_E000625_validation.csv"

E0003125_ROOT = FUNCTIONAL_RG / "5334" / "E0003125"
E0003125_FINITE = E0003125_ROOT / "D4_outer_event_aligned_E0003125_finite_value.csv"
E0003125_RESULT = E0003125_ROOT / "D4_outer_event_aligned_E0003125_result.json"
E0003125_VALIDATION = (
    E0003125_ROOT / "D4_outer_event_aligned_E0003125_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5370"
GATE_CONTRACT = OUTPUT / "D4_six_rung_outer_limit_gate_contract.json"
GATE_CONTRACT_VALIDATION = OUTPUT / "D4_six_rung_outer_limit_gate_contract_validation.csv"
GATE_CONTRACT_SOURCES = OUTPUT / "D4_six_rung_outer_limit_gate_contract_sources.csv"
RESULT = OUTPUT / "D4_six_rung_outer_limit_result.json"
INPUTS = OUTPUT / "D4_six_rung_inputs.csv"
FIXED_A_FIT = OUTPUT / "D4_six_rung_fixed_A_complete_fit.csv"
FREE_A_FIT = OUTPUT / "D4_six_rung_free_A_complete_fit.csv"
RESIDUALS_TABLE = OUTPUT / "D4_six_rung_model_residuals.csv"
LOO_TABLE = OUTPUT / "D4_six_rung_leave_one_out_stability.csv"
DIAGNOSTICS = OUTPUT / "D4_six_rung_intercept_diagnostics.csv"
GATES = OUTPUT / "D4_six_rung_outer_limit_gates.csv"
VALIDATION = OUTPUT / "D4_six_rung_outer_limit_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5370_VALIDATION.csv"
DOCUMENT = POST / "5370-Y5-R2FR-D4-six-rung-complete-family-outer-limit-gate.md"

CHECKPOINT = 5370
MARKER = "MTS_5370_D4_SIX_RUNG_COMPLETE_FAMILY_OUTER_LIMIT_GATE"
REVISION = "D4-six-rung-complete-family-outer-limit-gate-v1"
EPSILON_REFERENCE = 0.0025
EXPECTED_IDS = ("E0003125", "E000625", "E00125", "E0025", "E005", "E010")
RESIDUAL_DISK_LIMIT = 1.0
RELATIVE_INTERCEPT_LIMIT = 0.01
CONDITION_TIMES_EPSILON_LIMIT = 1.0e-8
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

FIXED_A_MODEL = "I=A_source*e*Log(e/e_ref)+I0+B*e+C*e^2*Log(e/e_ref)+D*e^2"
FREE_A_MODEL = "I=I0+A*e*Log(e/e_ref)+B*e+C*e^2*Log(e/e_ref)+D*e^2"
HALF_POWER_MODEL = "I=H0+H1*sqrt(e)+H2*e__FALSIFIER_ONLY"

CLAIM_CONTRACT = "valid_for_D4_six_rung_outer_limit_gate_contract"
CLAIM_FIT = "valid_for_D4_integral_six_rung_complete_second_order_fit"
CLAIM_CONDITIONAL_LIMIT = "valid_for_D4_conditional_six_rung_outer_regulator_zero_limit"
CLAIM_LIMIT = "valid_for_D4_outer_regulator_zero_limit"
FALSE_CLAIMS = (
    "valid_for_D4_numeric_uniform_remainder_bound",
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
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def E0003125_measurement_accepted() -> bool:
    if E0003125_RESULT.is_file():
        result = read_json(E0003125_RESULT)
        if result.get("acceptance_passed") is True and result.get("completed_full_run") is True:
            return True
    if E0003125_FINITE.is_file():
        return any(
            parse_bool(row.get("finite_regulator_fixed_decay_integral_accepted", False))
            for row in read_csv(E0003125_FINITE)
        )
    return False


def contract_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        PREREG_RESULT,
        ASYMPTOTIC_CONTRACT,
        FIT_PREREGISTRATION,
        RUNG_PREREGISTRATION,
        FIXED_A_RESULT,
        FIXED_A_VALIDATION,
        FIXED_A_RUNG_GATE,
        FOUR_RUNG_INPUTS,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
        COMPARATOR_CONTRACT,
        COMPARATOR_CONTRACT_VALIDATION,
        COMPARATOR_CONTRACT_SOURCES,
    )


def render_contract_document(contract: dict[str, Any]) -> None:
    lines = [
        "# 5370 - D4 six-rung complete-family outer-limit gate",
        "",
        "## Frozen decision",
        "",
        f"`{contract['decision']}`",
        "",
        "The scientific gates and numerical thresholds were saved while no accepted E0003125 measurement existed. Both the parent free-A family and the source-constrained fixed-A family are mandatory.",
        "",
        f"- residual-disk limit: `{contract['residual_disk_limit']}`;",
        f"- relative intercept-envelope limit: `{contract['relative_intercept_limit']}`;",
        f"- conditioning limit: `{contract['condition_times_epsilon_limit']}`;",
        "- gate executed: `False`.",
        "",
        "The half-power model is a reported falsifier only. No numerical uniform remainder, regulator-zero, angular, UV, local-GR, or full-MTS claim is made at contract freeze.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def freeze_gate_contract() -> dict[str, Any]:
    required = contract_source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    prereg = read_json(PREREG_RESULT)
    fixed_a = read_json(FIXED_A_RESULT)
    comparator = read_json(COMPARATOR_CONTRACT)
    asymptotic = read_csv(ASYMPTOTIC_CONTRACT)
    fit_rows = read_csv(FIT_PREREGISTRATION)
    rung_rows = read_csv(RUNG_PREREGISTRATION)
    fixed_rung_rows = read_csv(FIXED_A_RUNG_GATE)
    comparator_sources = source_register_current(COMPARATOR_CONTRACT_SOURCES)
    complete_six = [
        row
        for row in fit_rows
        if row["model_id"] == "D4_Q5_COMPLETE_SECOND_ORDER"
        and int(row["point_count"]) == 6
    ]
    six_gate = [row for row in rung_rows if int(row["accepted_rung_count"]) == 6]
    fixed_six_gate = [
        row for row in fixed_rung_rows if int(row["accepted_rung_count"]) == 6
    ]
    measurement_absent = not E0003125_measurement_accepted()
    checks = {
        "checkpoint_5345_six_rung_free_A_gate_is_preregistered": len(complete_six) == 1
        and parse_bool(complete_six[0]["full_rank"])
        and int(complete_six[0]["degrees_of_freedom"]) == 1
        and len(six_gate) == 1
        and six_gate[0]["allowed_decision"]
        == "FULL_ZERO_LIMIT_ACCEPTANCE_GATE_ELIGIBLE",
        "checkpoint_5345_complete_normal_form_is_parent_derived": any(
            row["contract_id"] == "NF5345_03_complete_second_order_family"
            and parse_bool(row["contract_passes"])
            for row in asymptotic
        )
        and prereg.get("acceptance_contract", {}).get(
            "minimum_complete_second_order_overdetermined_rungs"
        )
        == 6
        and prereg.get("acceptance_contract", {}).get("relative_zero_bound_limit")
        == RELATIVE_INTERCEPT_LIMIT,
        "checkpoint_5360_source_A_and_fixed_A_family_pass": fixed_a.get(
            "validation_passed"
        )
        is True
        and fixed_a.get("claim_boundary", {}).get(
            "valid_for_D4_derived_A_integral_subtraction"
        )
        is True
        and fixed_a.get("claim_boundary", {}).get(
            "valid_for_D4_conditional_fixed_A_remainder_normal_form"
        )
        is True
        and csv_validation_passes(FIXED_A_VALIDATION)
        and len(fixed_six_gate) == 1
        and fixed_six_gate[0]["allowed_decision"]
        == "PREFERRED_FIXED_A_STABILITY_LADDER",
        "checkpoint_5366_five_rung_precursor_passes": read_json(
            FIVE_RUNG_RESULT
        ).get("validation_passed")
        is True
        and csv_validation_passes(FIVE_RUNG_VALIDATION),
        "checkpoint_5369_comparison_contract_is_frozen_and_current": comparator.get(
            "validation_passed"
        )
        is True
        and comparator.get("measurement_absent_at_freeze") is True
        and comparator.get("comparison_executed") is False
        and csv_validation_passes(COMPARATOR_CONTRACT_VALIDATION)
        and comparator_sources[0]
        and comparator_sources[1] > 0,
        "E0003125_measurement_is_absent_at_gate_freeze": measurement_absent,
        "numeric_gates_are_fixed_before_measurement": RESIDUAL_DISK_LIMIT == 1.0
        and RELATIVE_INTERCEPT_LIMIT == 0.01
        and CONDITION_TIMES_EPSILON_LIMIT == 1.0e-8,
        "both_parent_free_A_and_source_constrained_fixed_A_models_are_required": FREE_A_MODEL.startswith(
            "I=I0+A*e*Log"
        )
        and FIXED_A_MODEL.startswith("I=A_source*e*Log")
        and "FALSIFIER_ONLY" in HALF_POWER_MODEL,
        "broad_claims_are_locked_false": all(
            value is False for value in no_broad_claims().values()
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    validations = [validation_row(key, value, value) for key, value in checks.items()]
    passed = all(checks.values())
    claims = {CLAIM_CONTRACT: passed, CLAIM_LIMIT: False, **no_broad_claims()}
    contract = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-six-rung-complete-family-outer-limit-gate-contract",
        "validation_passed": passed,
        "decision": (
            "D4_SIX_RUNG_OUTER_LIMIT_GATE_FROZEN__AWAIT_E0003125_COMPARISON"
            if passed
            else "D4_SIX_RUNG_OUTER_LIMIT_GATE_CONTRACT_BLOCKED"
        ),
        "measurement_absent_at_freeze": measurement_absent,
        "gate_executed": False,
        "expected_epsilon_ids": list(EXPECTED_IDS),
        "fixed_A_model": FIXED_A_MODEL,
        "free_A_model": FREE_A_MODEL,
        "half_power_model": HALF_POWER_MODEL,
        "residual_disk_limit": RESIDUAL_DISK_LIMIT,
        "relative_intercept_limit": RELATIVE_INTERCEPT_LIMIT,
        "condition_times_epsilon_limit": CONDITION_TIMES_EPSILON_LIMIT,
        "required_scientific_gates": [
            "E0003125 frozen blind holdout compatible",
            "fixed-A and free-A designs full rank",
            "fixed-A and free-A residuals inside conservative input disks",
            "free-A coefficient compatible with source-derived A",
            "fixed-A and free-A intercept disks compatible",
            "conservative intercept envelope below one percent",
            "half-power falsifier reported but not selected",
        ],
        "limit_scope": "conditional numerical D4_OUTER regulator-zero extrapolation under the parent normal-form hypotheses; a separate numeric uniform M_D4 is not claimed",
        "claim_boundary": claims,
        "comparator_contract_sha256": digest(COMPARATOR_CONTRACT),
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
    atomic_csv(GATE_CONTRACT_VALIDATION, validations)
    atomic_csv(GATE_CONTRACT_SOURCES, source_rows)
    atomic_json(GATE_CONTRACT, contract)
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


def load_inputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(FOUR_RUNG_INPUTS):
        source_path = Path(row["source_path"])
        source_rows = read_csv(source_path) if source_path.is_file() else []
        source_row = source_rows[0] if len(source_rows) == 1 else {}
        value = complex(
            float(row["fixed_decay_integral_real"]),
            float(row["fixed_decay_integral_imaginary"]),
        )
        radius = float(row["fixed_decay_integral_disk_radius"])
        source_value = complex(
            float(source_row.get("fixed_decay_integral_real", math.nan)),
            float(source_row.get("fixed_decay_integral_imaginary", math.nan)),
        )
        source_radius = float(
            source_row.get("total_error_absolute_conservative", math.nan)
        )
        claim_field = f"valid_for_D4_outer_{row['epsilon_id']}_fixed_decay_integral"
        source_accepted = (
            len(source_rows) == 1
            and source_row.get("epsilon_id") == row["epsilon_id"]
            and abs(float(source_row.get("epsilon", math.nan)) - float(row["epsilon"]))
            <= 1.0e-16
            and parse_bool(
                source_row.get("finite_regulator_fixed_decay_integral_accepted", False)
            )
            and parse_bool(source_row.get(claim_field, False))
            and abs(source_value - value) <= 1.0e-15
            and abs(source_radius - radius) <= 1.0e-15
        )
        rows.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": float(row["epsilon"]),
                "value": value,
                "radius": radius,
                "source_path": source_path,
                "source_sha256": row["source_sha256"],
                "accepted": source_path.is_file()
                and digest(source_path) == row["source_sha256"],
                "finite_row_accepted_and_value_matches": source_accepted,
            }
        )
    for path in (E000625_FINITE, E0003125_FINITE):
        finite = read_csv(path)
        if len(finite) != 1:
            raise RuntimeError(f"exactly one finite row required: {path}")
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
                "source_path": path,
                "source_sha256": digest(path),
                "accepted": parse_bool(
                    row["finite_regulator_fixed_decay_integral_accepted"]
                ),
                "finite_row_accepted_and_value_matches": parse_bool(
                    row["finite_regulator_fixed_decay_integral_accepted"]
                )
                and parse_bool(
                    row.get(
                        f"valid_for_D4_outer_{row['epsilon_id']}_fixed_decay_integral",
                        False,
                    )
                ),
            }
        )
    return sorted(rows, key=lambda item: item["epsilon"])


def fit_projection(
    design: np.ndarray, values: np.ndarray, weights: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    normal = design.T @ (weights[:, None] * design)
    projection = np.linalg.solve(normal, design.T * weights)
    return projection @ values, projection


def normalized_condition(design: np.ndarray) -> float:
    norms = np.linalg.norm(design, axis=0)
    return float(np.linalg.cond(design / norms))


def fit_model(
    design: np.ndarray, values: np.ndarray, radii: np.ndarray
) -> dict[str, Any]:
    weighted, weighted_projection = fit_projection(
        design, values, 1.0 / radii**2
    )
    unweighted, unweighted_projection = fit_projection(
        design, values, np.ones(len(values))
    )
    predictions = design @ weighted
    residuals = values - predictions
    return {
        "weighted": weighted,
        "unweighted": unweighted,
        "weighted_projection": weighted_projection,
        "unweighted_projection": unweighted_projection,
        "predictions": predictions,
        "residuals": residuals,
        "maximum_absolute_residual": float(np.max(np.abs(residuals))),
        "maximum_normalized_residual": float(np.max(np.abs(residuals) / radii)),
        "rank": int(np.linalg.matrix_rank(design)),
        "condition": normalized_condition(design),
        "condition_times_epsilon": normalized_condition(design)
        * np.finfo(float).eps,
        "degrees_of_freedom": int(len(values) - design.shape[1]),
    }


def leave_one_out(
    design: np.ndarray,
    values: np.ndarray,
    radii: np.ndarray,
    inputs: list[dict[str, Any]],
    model_id: str,
    reference_intercept: complex,
) -> tuple[list[dict[str, Any]], float, float]:
    rows: list[dict[str, Any]] = []
    intercepts: list[complex] = []
    for omitted in range(len(inputs)):
        selected = np.asarray(
            [index for index in range(len(inputs)) if index != omitted], dtype=int
        )
        coefficients, _ = fit_projection(
            design[selected], values[selected], 1.0 / radii[selected] ** 2
        )
        intercept = complex(coefficients[0])
        intercepts.append(intercept)
        rows.append(
            {
                "model_id": model_id,
                "omitted_epsilon_id": inputs[omitted]["epsilon_id"],
                **complex_fields("intercept", intercept),
                "distance_from_six_rung_weighted_intercept": abs(
                    intercept - reference_intercept
                ),
            }
        )
    spread = max(abs(value - reference_intercept) for value in intercepts)
    smallest_window_shift = abs(intercepts[-1] - reference_intercept)
    return rows, float(spread), float(smallest_window_shift)


def evaluate(inputs: list[dict[str, Any]]) -> dict[str, Any]:
    epsilon = np.asarray([row["epsilon"] for row in inputs], dtype=float)
    values = np.asarray([row["value"] for row in inputs], dtype=complex)
    radii = np.asarray([row["radius"] for row in inputs], dtype=float)
    logarithm = np.log(epsilon / EPSILON_REFERENCE)
    x = epsilon / EPSILON_REFERENCE
    log_feature = epsilon * logarithm
    fixed_a_result = read_json(FIXED_A_RESULT)
    source_a = complex(
        float(fixed_a_result["A_zero_real"]),
        float(fixed_a_result["A_zero_imaginary"]),
    )
    source_a_radius = float(fixed_a_result["A_zero_disk_radius"])
    corrected = values - source_a * log_feature

    fixed_design = np.column_stack(
        (np.ones(len(x)), x, x**2 * logarithm, x**2)
    )
    free_design = np.column_stack(
        (np.ones(len(x)), x * logarithm, x, x**2 * logarithm, x**2)
    )
    leading_design = np.column_stack((np.ones(len(x)), x))
    half_power_design = np.column_stack((np.ones(len(x)), np.sqrt(x), x))

    fixed = fit_model(fixed_design, corrected, radii)
    free = fit_model(free_design, values, radii)
    leading = fit_model(leading_design, corrected, radii)
    half_power = fit_model(half_power_design, values, radii)
    fixed_predictions = fixed["predictions"] + source_a * log_feature
    fixed_residuals = values - fixed_predictions
    fixed["predictions"] = fixed_predictions
    fixed["residuals"] = fixed_residuals
    fixed["maximum_absolute_residual"] = float(np.max(np.abs(fixed_residuals)))
    fixed["maximum_normalized_residual"] = float(
        np.max(np.abs(fixed_residuals) / radii)
    )

    fixed_intercept = complex(fixed["weighted"][0])
    free_intercept = complex(free["weighted"][0])
    fixed_unweighted_intercept = complex(fixed["unweighted"][0])
    free_unweighted_intercept = complex(free["unweighted"][0])
    leading_intercept = complex(leading["weighted"][0])
    half_power_intercept = complex(half_power["weighted"][0])

    fixed_loo_rows, fixed_loo_spread, fixed_smallest_shift = leave_one_out(
        fixed_design, corrected, radii, inputs, "FIXED_A_COMPLETE", fixed_intercept
    )
    free_loo_rows, free_loo_spread, free_smallest_shift = leave_one_out(
        free_design, values, radii, inputs, "FREE_A_COMPLETE", free_intercept
    )

    fixed_intercept_projection = fixed["weighted_projection"][0]
    free_intercept_projection = free["weighted_projection"][0]
    fixed_input_disk = float(np.sum(np.abs(fixed_intercept_projection) * radii))
    fixed_a_multiplier = float(np.sum(fixed_intercept_projection * log_feature))
    fixed_a_disk = abs(fixed_a_multiplier) * source_a_radius
    fixed_base_disk = fixed_input_disk + fixed_a_disk
    free_base_disk = float(np.sum(np.abs(free_intercept_projection) * radii))

    fitted_a = complex(free["weighted"][1]) / EPSILON_REFERENCE
    fitted_a_projection = free["weighted_projection"][1] / EPSILON_REFERENCE
    fitted_a_disk = float(np.sum(np.abs(fitted_a_projection) * radii))
    a_separation = abs(fitted_a - source_a)
    a_combined_disk = fitted_a_disk + source_a_radius
    intercept_separation = abs(free_intercept - fixed_intercept)
    intercept_combined_disk = fixed_base_disk + free_base_disk

    weighted_unweighted_shift = max(
        abs(fixed_intercept - fixed_unweighted_intercept),
        abs(free_intercept - free_unweighted_intercept),
    )
    loo_spread = max(fixed_loo_spread, free_loo_spread)
    leading_shift = abs(leading_intercept - fixed_intercept)
    complete_model_shift = intercept_separation
    maximum_absolute_residual = max(
        fixed["maximum_absolute_residual"], free["maximum_absolute_residual"]
    )
    base_intercept_disk = max(fixed_base_disk, free_base_disk)
    intercept_envelope = (
        base_intercept_disk
        + weighted_unweighted_shift
        + loo_spread
        + leading_shift
        + complete_model_shift
        + maximum_absolute_residual
    )
    relative_envelope = intercept_envelope / max(abs(fixed_intercept), 1.0e-300)

    return {
        "epsilon": epsilon,
        "values": values,
        "radii": radii,
        "source_a": source_a,
        "source_a_radius": source_a_radius,
        "fitted_a": fitted_a,
        "fitted_a_disk": fitted_a_disk,
        "a_separation": a_separation,
        "a_combined_disk": a_combined_disk,
        "a_compatible": a_separation <= a_combined_disk,
        "fixed": fixed,
        "free": free,
        "leading": leading,
        "half_power": half_power,
        "fixed_intercept": fixed_intercept,
        "free_intercept": free_intercept,
        "fixed_unweighted_intercept": fixed_unweighted_intercept,
        "free_unweighted_intercept": free_unweighted_intercept,
        "leading_intercept": leading_intercept,
        "half_power_intercept": half_power_intercept,
        "fixed_base_disk": fixed_base_disk,
        "free_base_disk": free_base_disk,
        "fixed_a_multiplier": fixed_a_multiplier,
        "fixed_a_disk": fixed_a_disk,
        "intercept_separation": intercept_separation,
        "intercept_combined_disk": intercept_combined_disk,
        "intercepts_compatible": intercept_separation <= intercept_combined_disk,
        "weighted_unweighted_shift": weighted_unweighted_shift,
        "fixed_loo_spread": fixed_loo_spread,
        "free_loo_spread": free_loo_spread,
        "loo_spread": loo_spread,
        "fixed_smallest_window_shift": fixed_smallest_shift,
        "free_smallest_window_shift": free_smallest_shift,
        "leading_shift": leading_shift,
        "complete_model_shift": complete_model_shift,
        "maximum_absolute_residual": maximum_absolute_residual,
        "base_intercept_disk": base_intercept_disk,
        "intercept_envelope": intercept_envelope,
        "relative_envelope": relative_envelope,
        "loo_rows": fixed_loo_rows + free_loo_rows,
    }


def run_preflight() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    required = (
        GATE_CONTRACT,
        GATE_CONTRACT_VALIDATION,
        GATE_CONTRACT_SOURCES,
        COMPARATOR_RESULT,
        COMPARATOR_VALIDATION,
        COMPARATOR_SOURCES,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
        E0003125_FINITE,
        E0003125_RESULT,
        E0003125_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    contract = read_json(GATE_CONTRACT)
    comparator = read_json(COMPARATOR_RESULT)
    contract_sources = source_register_current(GATE_CONTRACT_SOURCES)
    comparator_sources = source_register_current(COMPARATOR_SOURCES)
    E000625_result = read_json(E000625_RESULT)
    E0003125_result = read_json(E0003125_RESULT)
    inputs = load_inputs()
    checks = {
        "gate_contract_was_frozen_before_measurement_and_is_current": contract.get(
            "validation_passed"
        )
        is True
        and contract.get("measurement_absent_at_freeze") is True
        and contract.get("gate_executed") is False
        and csv_validation_passes(GATE_CONTRACT_VALIDATION)
        and contract_sources[0]
        and contract_sources[1] > 0,
        "E0003125_frozen_blind_holdout_is_valid_and_compatible": comparator.get(
            "validation_passed"
        )
        is True
        and comparator.get("holdout_compatible") is True
        and csv_validation_passes(COMPARATOR_VALIDATION)
        and comparator_sources[0]
        and comparator_sources[1] > 0,
        "exactly_six_accepted_source_current_rungs_are_present": len(inputs) == 6
        and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
        and all(row["accepted"] for row in inputs)
        and all(row["finite_row_accepted_and_value_matches"] for row in inputs)
        and all(
            row["radius"] > 0.0
            and math.isfinite(row["radius"])
            and math.isfinite(row["value"].real)
            and math.isfinite(row["value"].imag)
            for row in inputs
        ),
        "E000625_and_E0003125_integrals_are_independently_accepted": E000625_result.get(
            "acceptance_passed"
        )
        is True
        and E000625_result.get("completed_full_run") is True
        and E0003125_result.get("acceptance_passed") is True
        and E0003125_result.get("completed_full_run") is True
        and int(E0003125_result.get("failed_inner_node_count", -1)) == 0
        and E0003125_result.get("all_adaptive_leaf_gates_pass") is True
        and csv_validation_passes(E000625_VALIDATION)
        and csv_validation_passes(E0003125_VALIDATION),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    if not all(checks.values()):
        raise RuntimeError(f"six-rung preflight failed: {checks}")
    return contract, inputs


def final_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        GATE_CONTRACT,
        GATE_CONTRACT_VALIDATION,
        GATE_CONTRACT_SOURCES,
        PREREG_RESULT,
        ASYMPTOTIC_CONTRACT,
        FIT_PREREGISTRATION,
        RUNG_PREREGISTRATION,
        FIXED_A_RESULT,
        FIXED_A_VALIDATION,
        FIXED_A_RUNG_GATE,
        FOUR_RUNG_INPUTS,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
        COMPARATOR_RESULT,
        COMPARATOR_VALIDATION,
        COMPARATOR_SOURCES,
        E000625_FINITE,
        E000625_RESULT,
        E000625_VALIDATION,
        E0003125_FINITE,
        E0003125_RESULT,
        E0003125_VALIDATION,
    )


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5370 - D4 six-rung complete-family outer-limit gate",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "The gate was frozen before the E0003125 measurement. It tests both the checkpoint-5345 free-A complete second-order family and the stronger checkpoint-5360 source-constrained fixed-A family.",
        "",
        f"- fixed-A maximum normalized residual: `{result['fixed_A_maximum_normalized_residual']:.17g}`;",
        f"- free-A maximum normalized residual: `{result['free_A_maximum_normalized_residual']:.17g}`;",
        f"- source-A compatibility: `{result['source_A_compatible_with_free_fit']}`;",
        f"- fixed/free intercept compatibility: `{result['fixed_free_intercepts_compatible']}`;",
        f"- relative conservative intercept envelope: `{result['relative_intercept_envelope']:.17g}`;",
        f"- full frozen gate passes: `{result['outer_limit_gate_passes']}`.",
        "",
        "## Claim boundary",
        "",
        "A passing result is a conditional numerical D4_OUTER regulator-zero extrapolation under the parent normal-form hypotheses. The separate uniform numerical M_D4 remainder constant, decay-angle limit, full phase-space coefficient, UV result, local GR, and full MTS theory remain unclaimed.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def execute_gate() -> dict[str, Any]:
    contract, inputs = run_preflight()
    evaluation = evaluate(inputs)
    fixed = evaluation["fixed"]
    free = evaluation["free"]
    scientific_gates = {
        "sixth_frozen_blind_holdout_compatible": read_json(COMPARATOR_RESULT).get(
            "holdout_compatible"
        )
        is True,
        "fixed_A_design_full_rank_and_resolved": fixed["rank"] == 4
        and fixed["degrees_of_freedom"] == 2
        and fixed["condition_times_epsilon"] < CONDITION_TIMES_EPSILON_LIMIT,
        "free_A_design_full_rank_and_resolved": free["rank"] == 5
        and free["degrees_of_freedom"] == 1
        and free["condition_times_epsilon"] < CONDITION_TIMES_EPSILON_LIMIT,
        "fixed_A_residuals_inside_conservative_disks": fixed[
            "maximum_normalized_residual"
        ]
        <= RESIDUAL_DISK_LIMIT,
        "free_A_residuals_inside_conservative_disks": free[
            "maximum_normalized_residual"
        ]
        <= RESIDUAL_DISK_LIMIT,
        "free_A_fit_is_disk_compatible_with_source_A": evaluation["a_compatible"],
        "fixed_A_and_free_A_intercepts_are_disk_compatible": evaluation[
            "intercepts_compatible"
        ],
        "preregistered_relative_intercept_envelope_below_one_percent": evaluation[
            "relative_envelope"
        ]
        <= RELATIVE_INTERCEPT_LIMIT,
        "half_power_falsifier_is_reported_but_not_selected": True,
    }
    outer_gate_passes = all(scientific_gates.values())
    validations = [
        validation_row(
            "premeasurement_gate_contract_passes",
            contract.get("validation_passed") is True
            and contract.get("measurement_absent_at_freeze") is True,
            contract.get("updated_utc"),
        ),
        validation_row(
            "six_source_current_inputs_are_finite_and_ordered",
            len(inputs) == 6
            and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
            and all(row["accepted"] for row in inputs),
            EXPECTED_IDS,
        ),
        validation_row(
            "fixed_and_free_design_dimensions_match_preregistration",
            fixed["rank"] == 4
            and fixed["degrees_of_freedom"] == 2
            and free["rank"] == 5
            and free["degrees_of_freedom"] == 1,
            {
                "fixed": (fixed["rank"], fixed["degrees_of_freedom"]),
                "free": (free["rank"], free["degrees_of_freedom"]),
            },
        ),
        validation_row(
            "all_reported_fit_diagnostics_are_finite",
            all(
                math.isfinite(value)
                for value in (
                    fixed["maximum_normalized_residual"],
                    free["maximum_normalized_residual"],
                    evaluation["a_separation"],
                    evaluation["a_combined_disk"],
                    evaluation["intercept_separation"],
                    evaluation["intercept_combined_disk"],
                    evaluation["intercept_envelope"],
                    evaluation["relative_envelope"],
                    evaluation["half_power"]["maximum_normalized_residual"],
                )
            ),
            evaluation["relative_envelope"],
        ),
        validation_row(
            "half_power_falsifier_does_not_select_reported_intercept",
            "FALSIFIER_ONLY" in HALF_POWER_MODEL,
            HALF_POWER_MODEL,
        ),
        validation_row(
            "uniform_remainder_and_broad_claims_remain_separate",
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
    artifact_passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_CONTRACT: artifact_passed,
        CLAIM_FIT: artifact_passed,
        CLAIM_CONDITIONAL_LIMIT: artifact_passed and outer_gate_passes,
        CLAIM_LIMIT: artifact_passed and outer_gate_passes,
        **no_broad_claims(),
    }

    input_rows = [
        {
            "epsilon_id": row["epsilon_id"],
            "epsilon": row["epsilon"],
            **complex_fields("fixed_decay_integral", row["value"]),
            "input_disk_radius": row["radius"],
            "source_path": str(row["source_path"].resolve()),
            "source_sha256": row["source_sha256"],
            "accepted_and_source_current": row["accepted"],
            "finite_row_accepted_and_value_matches": row[
                "finite_row_accepted_and_value_matches"
            ],
            **claims,
        }
        for row in inputs
    ]
    fixed_names = ("I0", "B_scaled", "C_log_scaled", "D_scaled")
    free_names = ("I0", "A_scaled", "B_scaled", "C_log_scaled", "D_scaled")
    fixed_rows = [
        {
            "coefficient": name,
            **complex_fields("weighted_value", complex(fixed["weighted"][index])),
            **complex_fields("unweighted_value", complex(fixed["unweighted"][index])),
            **claims,
        }
        for index, name in enumerate(fixed_names)
    ]
    free_rows = [
        {
            "coefficient": name,
            **complex_fields("weighted_value", complex(free["weighted"][index])),
            **complex_fields("unweighted_value", complex(free["unweighted"][index])),
            **claims,
        }
        for index, name in enumerate(free_names)
    ]
    residual_rows: list[dict[str, Any]] = []
    for index, row in enumerate(inputs):
        residual_rows.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": row["epsilon"],
                "input_disk_radius": row["radius"],
                **complex_fields("fixed_A_prediction", complex(fixed["predictions"][index])),
                **complex_fields("fixed_A_residual", complex(fixed["residuals"][index])),
                "fixed_A_normalized_residual": abs(fixed["residuals"][index])
                / row["radius"],
                **complex_fields("free_A_prediction", complex(free["predictions"][index])),
                **complex_fields("free_A_residual", complex(free["residuals"][index])),
                "free_A_normalized_residual": abs(free["residuals"][index])
                / row["radius"],
                **claims,
            }
        )
    for row in evaluation["loo_rows"]:
        row.update(claims)
    diagnostic_row = {
        **complex_fields("fixed_A_weighted_intercept", evaluation["fixed_intercept"]),
        **complex_fields("free_A_weighted_intercept", evaluation["free_intercept"]),
        **complex_fields("fixed_A_unweighted_intercept", evaluation["fixed_unweighted_intercept"]),
        **complex_fields("free_A_unweighted_intercept", evaluation["free_unweighted_intercept"]),
        **complex_fields("leading_family_intercept", evaluation["leading_intercept"]),
        **complex_fields("half_power_falsifier_intercept", evaluation["half_power_intercept"]),
        **complex_fields("source_A", evaluation["source_a"]),
        "source_A_disk_radius": evaluation["source_a_radius"],
        **complex_fields("free_fitted_A", evaluation["fitted_a"]),
        "free_fitted_A_disk_radius": evaluation["fitted_a_disk"],
        "source_A_separation": evaluation["a_separation"],
        "source_A_combined_disk_radius": evaluation["a_combined_disk"],
        "source_A_compatible": evaluation["a_compatible"],
        "fixed_free_intercept_separation": evaluation["intercept_separation"],
        "fixed_free_intercept_combined_disk_radius": evaluation[
            "intercept_combined_disk"
        ],
        "fixed_free_intercepts_compatible": evaluation["intercepts_compatible"],
        "fixed_A_base_intercept_disk": evaluation["fixed_base_disk"],
        "free_A_base_intercept_disk": evaluation["free_base_disk"],
        "weighted_unweighted_shift": evaluation["weighted_unweighted_shift"],
        "fixed_A_leave_one_out_spread": evaluation["fixed_loo_spread"],
        "free_A_leave_one_out_spread": evaluation["free_loo_spread"],
        "fixed_A_smallest_window_shift": evaluation["fixed_smallest_window_shift"],
        "free_A_smallest_window_shift": evaluation["free_smallest_window_shift"],
        "leading_vs_fixed_A_shift": evaluation["leading_shift"],
        "fixed_vs_free_complete_model_shift": evaluation["complete_model_shift"],
        "maximum_absolute_complete_fit_residual": evaluation[
            "maximum_absolute_residual"
        ],
        "conservative_intercept_envelope": evaluation["intercept_envelope"],
        "relative_intercept_envelope": evaluation["relative_envelope"],
        "preregistered_relative_limit": RELATIVE_INTERCEPT_LIMIT,
        "half_power_maximum_normalized_residual": evaluation["half_power"][
            "maximum_normalized_residual"
        ],
        "half_power_role": "FALSIFIER_ONLY_NOT_SELECTED",
        **claims,
    }
    gate_rows = [
        {
            "gate": gate,
            "passed": passed,
            "detail": str(passed),
            **claims,
        }
        for gate, passed in scientific_gates.items()
    ]
    gate_rows.append(
        {
            "gate": "D4_outer_regulator_zero_limit",
            "passed": outer_gate_passes,
            "detail": "conditional numerical limit under parent normal-form hypotheses; numeric uniform M_D4 remains separate",
            **claims,
        }
    )
    decision = (
        "D4_SIX_RUNG_COMPLETE_FAMILY_GATE_PASSES__CONDITIONAL_OUTER_REGULATOR_ZERO_LIMIT_ACCEPTED"
        if outer_gate_passes
        else "D4_SIX_RUNG_COMPLETE_FAMILY_GATE_FAILS__OUTER_REGULATOR_ZERO_LIMIT_REMAINS_BLOCKED"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-six-rung-complete-family-outer-limit-gate",
        "validation_passed": artifact_passed,
        "decision": decision,
        "accepted_rung_count": len(inputs),
        "fixed_A_fit_parameter_count": 4,
        "fixed_A_fit_degrees_of_freedom": fixed["degrees_of_freedom"],
        "free_A_fit_parameter_count": 5,
        "free_A_fit_degrees_of_freedom": free["degrees_of_freedom"],
        **complex_fields("intercept", evaluation["fixed_intercept"]),
        "intercept_envelope": evaluation["intercept_envelope"],
        "relative_intercept_envelope": evaluation["relative_envelope"],
        "preregistered_relative_limit": RELATIVE_INTERCEPT_LIMIT,
        "fixed_A_maximum_normalized_residual": fixed[
            "maximum_normalized_residual"
        ],
        "free_A_maximum_normalized_residual": free["maximum_normalized_residual"],
        "source_A_compatible_with_free_fit": evaluation["a_compatible"],
        "fixed_free_intercepts_compatible": evaluation["intercepts_compatible"],
        "half_power_falsifier_maximum_normalized_residual": evaluation["half_power"][
            "maximum_normalized_residual"
        ],
        "half_power_falsifier_selected": False,
        "outer_limit_gate_passes": outer_gate_passes,
        "uniform_numeric_remainder_bound_available": False,
        "limit_scope": contract["limit_scope"],
        "claim_boundary": claims,
        "scientific_gates": scientific_gates,
        "remaining_obstruction": (
            "derive or numerically bound the uniform M_D4 remainder constant and then continue to the independent decay-angle limit"
            if outer_gate_passes
            else "inspect the failed preregistered gate without changing its thresholds, then derive the missing normal-form or numerical control"
        ),
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
    atomic_csv(INPUTS, input_rows)
    atomic_csv(FIXED_A_FIT, fixed_rows)
    atomic_csv(FREE_A_FIT, free_rows)
    atomic_csv(RESIDUALS_TABLE, residual_rows)
    atomic_csv(LOO_TABLE, evaluation["loo_rows"])
    atomic_csv(DIAGNOSTICS, [diagnostic_row])
    atomic_csv(GATES, gate_rows)
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete",
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
    claims = result.get("claim_boundary", {})
    checks = {
        "artifact_validation_passes": csv_validation_passes(VALIDATION),
        "residual_validation_passes": csv_validation_passes(RESIDUAL_VALIDATION),
        "result_validation_passes": result.get("validation_passed") is True,
        "all_fit_and_gate_outputs_exist": all(
            path.is_file()
            for path in (
                INPUTS,
                FIXED_A_FIT,
                FREE_A_FIT,
                RESIDUALS_TABLE,
                LOO_TABLE,
                DIAGNOSTICS,
                GATES,
            )
        ),
        "registered_sources_are_current": sources_current and source_count > 0,
        "limit_claim_matches_frozen_gate_result": claims.get(CLAIM_LIMIT)
        is bool(result.get("outer_limit_gate_passes")),
        "uniform_remainder_and_broad_claims_remain_false": all(
            claims.get(field) is False for field in FALSE_CLAIMS
        ),
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
    parser.add_argument("--mode", choices=("preflight", "run", "validate"), required=True)
    arguments = parser.parse_args()
    if arguments.mode == "preflight":
        payload = freeze_gate_contract()
    elif arguments.mode == "run":
        payload = execute_gate()
    else:
        payload = validate_saved()
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
