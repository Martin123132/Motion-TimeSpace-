from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
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

SCRIPT_5359 = SCRIPTS / "Y5_R2FR_5359_D4_zero_regulator_endpoint_coefficient_limit.py"
SCRIPT_5360 = SCRIPTS / "Y5_R2FR_5360_D4_derived_A_subtraction_and_E005_holdout_preregistration.py"
SCRIPT_5370 = SCRIPTS / "Y5_R2FR_5370_D4_six_rung_complete_family_outer_limit_gate.py"
SCRIPT_5373 = SCRIPTS / "Y5_R2FR_5373_D4_seven_rung_extended_window_stability_gate.py"

RESULT_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
VALIDATION_5359 = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_validation.csv"
SOURCES_5359 = FUNCTIONAL_RG / "5359" / "source_register.csv"
RESULT_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"
VALIDATION_5360 = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_validation.csv"
SOURCES_5360 = FUNCTIONAL_RG / "5360" / "source_register.csv"
RESULT_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_result.json"
VALIDATION_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_validation.csv"
SOURCES_5373 = FUNCTIONAL_RG / "5373" / "source_register.csv"
INPUTS_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_inputs.csv"
DIAGNOSTICS_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_intercept_diagnostics.csv"
GATES_5373 = FUNCTIONAL_RG / "5373" / "D4_seven_rung_stability_gates.csv"

OUTPUT = FUNCTIONAL_RG / "5375"
CONTRACT = OUTPUT / "D4_derived_A_primary_role_contract.csv"
COMPONENTS = OUTPUT / "D4_derived_A_fixed_primary_envelope_components.csv"
ESTIMATOR = OUTPUT / "D4_derived_A_fixed_estimator_projection.csv"
RESULT = OUTPUT / "D4_derived_A_primary_role_result.json"
VALIDATION = OUTPUT / "D4_derived_A_primary_role_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5375_VALIDATION.csv"
DOCUMENT = POST / "5375-Y5-R2FR-D4-derived-A-primary-role-separation-gate.md"

CHECKPOINT = 5375
MARKER = "MTS_5375_D4_DERIVED_A_PRIMARY_ROLE_SEPARATION_GATE"
REVISION = "D4-derived-A-primary-role-separation-postmeasurement-v1"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
RELATIVE_LIMIT = 1.0e-2

CLAIM_ROLE = "valid_for_D4_derived_A_primary_role_separation"
CLAIM_DISK = "valid_for_D4_derived_A_fixed_estimator_disk_identity"
CLAIM_STABILITY = "valid_for_D4_conditional_fixed_A_seven_rung_numerical_stability"
CLAIM_CONDITIONAL_LIMIT = "valid_for_D4_conditional_derived_A_outer_regulator_zero_limit"
FALSE_CLAIMS = (
    "valid_for_D4_strict_all_model_one_percent_gate",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
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
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5373 = load_module("mts_5373_for_5375", SCRIPT_5373)
M5370 = M5373.M5370


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5373.set_below_normal_priority()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if hasattr(value, "item"):
        return normalize(value.item())
    if isinstance(value, complex):
        return {"real": float(value.real), "imaginary": float(value.imag)}
    return value


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
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
        json.dumps(normalize(payload), indent=2, sort_keys=True, allow_nan=False) + "\n",
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


def csv_passes(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row["passed"]) for row in rows)


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    rows = read_csv(path)
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def false_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5359,
        SCRIPT_5360,
        SCRIPT_5370,
        SCRIPT_5373,
        RESULT_5359,
        VALIDATION_5359,
        SOURCES_5359,
        RESULT_5360,
        VALIDATION_5360,
        SOURCES_5360,
        RESULT_5373,
        VALIDATION_5373,
        SOURCES_5373,
        INPUTS_5373,
        DIAGNOSTICS_5373,
        GATES_5373,
    )


def contract_rows() -> list[dict[str, Any]]:
    claims = {
        CLAIM_ROLE: True,
        CLAIM_DISK: True,
        CLAIM_STABILITY: False,
        CLAIM_CONDITIONAL_LIMIT: False,
        **false_claims(),
    }
    return [
        {
            "contract_id": "DA5375_00_parent_coefficient_role",
            "premises": "5359 derives the eight-event endpoint coefficient at epsilon=0; 5360 signs it source-complete and not fitted",
            "derived_statement": "A is a parent-owned coefficient with one common correlated disk, not a numerical fit parameter in the primary branch",
            "status": "DERIVED_SOURCE_COMPLETE_CONDITIONAL_ON_PARENT_EVENT_HYPOTHESES",
            **claims,
        },
        {
            "contract_id": "DA5375_01_fixed_estimator",
            "premises": "y_j in Disk(yhat_j,r_j); A in Disk(Ahat,r_A); fixed complete normal form",
            "derived_statement": "I0hat=p^T(yhat-Ahat*l), where p is row zero of (X^T W X)^(-1)X^T W",
            "status": "EXACT_LINEAR_ESTIMATOR_IDENTITY",
            **claims,
        },
        {
            "contract_id": "DA5375_02_minkowski_disk",
            "premises": "independent adversarial complex input disks and one common correlated A disk",
            "derived_statement": "R_I0=sum_j |p_j| r_j + |p^T l| r_A",
            "status": "EXACT_WORST_CASE_DISK_FOR_THE_STATED_INPUT_MODEL",
            **claims,
        },
        {
            "contract_id": "DA5375_03_free_A_role",
            "premises": "A is parent-derived; free-A supermodel is retained",
            "derived_statement": "the free-A branch tests sensitivity and contradiction but its estimator disk is not propagated into the conditional fixed-A estimator",
            "status": "MODEL_ROLE_SEPARATION__STRICT_ALL_MODEL_GATE_REMAINS_FAILED",
            **claims,
        },
        {
            "contract_id": "DA5375_04_postmeasurement_disclosure",
            "premises": "5373 was opened before this role audit and failed its all-model one-percent envelope",
            "derived_statement": "5375 is a transparent post-measurement conditional branch audit, not a preregistered replacement for 5373",
            "status": "POSTMEASUREMENT_DISCLOSED",
            **claims,
        },
        {
            "contract_id": "DA5375_05_claim_boundary",
            "premises": "fixed-A numerical stability can pass while uniform R3 constant remains unavailable",
            "derived_statement": "at most conditional fixed-A numerical outer-limit stability; strict all-model, uniform-remainder, actual regulator-zero, angular, UV, local-GR and full-MTS claims remain false",
            "status": "CONDITIONAL_NUMERICAL_SCOPE_ONLY",
            **claims,
        },
    ]


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5375 - D4 derived-A primary-role separation gate",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        "Checkpoint 5373 remains a valid failed strict all-model gate. Its 1.487155% envelope is dominated by the 0.125430 free-A base disk. Checkpoints 5359 and 5360 independently derive A from all eight endpoint events and sign it source-complete and not fitted.",
        "",
        "For the conditional parent-derived-A branch, the fixed-A intercept is a linear estimator. Its exact adversarial input disk is sum |p_j| r_j plus the one correlated A-disk contribution |p^T l| r_A. The free-A branch remains a sensitivity/falsifier branch; its uncertainty is not silently converted into uncertainty of the fixed-A estimator.",
        "",
        "## Result",
        "",
        f"- fixed-A base estimator disk: `{payload['fixed_A_base_estimator_disk']}`;",
        f"- fixed-A conservative diagnostic envelope: `{payload['fixed_A_conservative_envelope']}`;",
        f"- relative fixed-A envelope: `{payload['relative_fixed_A_envelope']}`;",
        f"- unchanged one-percent gate: `{payload['relative_limit']}`;",
        f"- conditional fixed-A stability passes: `{payload['conditional_fixed_A_stability_passes']}`.",
        "",
        "## Disclosure",
        "",
        "This role-separation audit was defined after the frozen 5373 strict gate failed. It is not labeled preregistered and does not overwrite that failure. It establishes a narrower conditional result whose premise is the parent derivation of A.",
        "",
        "A numeric uniform M_D4 remainder constant is still absent. Therefore the unconditional D4 regulator-zero limit, decay-angle integral, full phase space, UV result, local GR and full MTS theory remain unclaimed.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def execute() -> dict[str, Any]:
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    parent_5359 = read_json(RESULT_5359)
    parent_5360 = read_json(RESULT_5360)
    parent_5373 = read_json(RESULT_5373)
    currents = {
        "5359": source_register_current(SOURCES_5359),
        "5360": source_register_current(SOURCES_5360),
        "5373": source_register_current(SOURCES_5373),
    }
    inputs = M5373.load_inputs()
    evaluation = M5370.evaluate(inputs)
    fixed = evaluation["fixed"]
    projection = fixed["weighted_projection"][0]
    epsilon = evaluation["epsilon"]
    logarithm = M5370.np.log(epsilon / M5370.EPSILON_REFERENCE)
    log_feature = epsilon * logarithm
    values = evaluation["values"]
    radii = evaluation["radii"]
    source_a = complex(evaluation["source_a"])
    source_a_radius = float(evaluation["source_a_radius"])
    direct_intercept = complex(projection @ (values - source_a * log_feature))
    data_disk = float(M5370.np.sum(M5370.np.abs(projection) * radii))
    a_multiplier = complex(projection @ log_feature)
    a_disk = abs(a_multiplier) * source_a_radius
    base_disk = data_disk + a_disk
    fixed_intercept = complex(evaluation["fixed_intercept"])
    fixed_weight_shift = abs(
        fixed_intercept - complex(evaluation["fixed_unweighted_intercept"])
    )
    fixed_loo_spread = float(evaluation["fixed_loo_spread"])
    leading_shift = float(evaluation["leading_shift"])
    cross_family_central_shift = float(evaluation["complete_model_shift"])
    fixed_residual = float(fixed["maximum_absolute_residual"])
    components = [
        ("fixed_A_exact_input_minkowski_disk", base_disk, "ESTIMATOR_DISK"),
        ("fixed_A_weighted_unweighted_shift", fixed_weight_shift, "ROBUSTNESS"),
        ("fixed_A_leave_one_out_spread", fixed_loo_spread, "ROBUSTNESS"),
        ("leading_vs_fixed_A_shift", leading_shift, "MODEL_TRUNCATION_DIAGNOSTIC"),
        (
            "fixed_vs_free_central_intercept_shift",
            cross_family_central_shift,
            "FALSIFIER_CENTRE_DIAGNOSTIC",
        ),
        ("fixed_A_maximum_absolute_fit_residual", fixed_residual, "FIT_DIAGNOSTIC"),
    ]
    envelope = float(sum(value for _, value, _ in components))
    relative_envelope = envelope / max(abs(fixed_intercept), 1.0e-300)
    free_base_disk = float(evaluation["free_base_disk"])
    strict_envelope = float(parent_5373["intercept_envelope"])
    free_fraction = free_base_disk / strict_envelope
    free_a_normalized_separation = float(evaluation["a_separation"]) / max(
        float(evaluation["a_combined_disk"]), 1.0e-300
    )
    role_passes = (
        parent_5359.get("claim_boundary", {}).get(
            "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
        )
        is True
        and parent_5360.get("claim_boundary", {}).get(
            "valid_for_D4_derived_A_integral_subtraction"
        )
        is True
        and parent_5360.get("claim_boundary", {}).get(
            "valid_for_D4_conditional_fixed_A_remainder_normal_form"
        )
        is True
    )
    disk_identity_passes = (
        abs(direct_intercept - fixed_intercept) <= 1.0e-12
        and math.isclose(base_disk, float(evaluation["fixed_base_disk"]), rel_tol=1.0e-12)
        and a_disk <= base_disk
    )
    conditional_stability = (
        role_passes
        and disk_identity_passes
        and relative_envelope <= RELATIVE_LIMIT
        and fixed["maximum_normalized_residual"] <= 1.0
        and evaluation["intercepts_compatible"]
    )
    claims = {
        CLAIM_ROLE: role_passes,
        CLAIM_DISK: disk_identity_passes,
        CLAIM_STABILITY: conditional_stability,
        CLAIM_CONDITIONAL_LIMIT: conditional_stability,
        **false_claims(),
    }
    validations = [
        validation_row(
            "parent_endpoint_A_is_source_complete_and_not_fitted",
            role_passes,
            {
                "A": source_a,
                "disk": source_a_radius,
                "event_count": parent_5359.get("event_count"),
            },
        ),
        validation_row(
            "all_parent_validation_rows_and_sources_are_current",
            csv_passes(VALIDATION_5359)
            and csv_passes(VALIDATION_5360)
            and csv_passes(VALIDATION_5373)
            and all(current[0] and current[1] > 0 for current in currents.values()),
            {key: value[2] for key, value in currents.items()},
        ),
        validation_row(
            "fixed_A_estimator_and_minkowski_disk_identities_hold",
            disk_identity_passes,
            {
                "intercept_difference": abs(direct_intercept - fixed_intercept),
                "recomputed_base_disk": base_disk,
                "parent_base_disk": evaluation["fixed_base_disk"],
            },
        ),
        validation_row(
            "strict_5373_failure_is_preserved_not_relabelled",
            parent_5373.get("outer_limit_gate_passes") is False
            and parent_5373.get("scientific_gates", {}).get(
                "preregistered_relative_intercept_envelope_below_one_percent"
            )
            is False,
            parent_5373.get("relative_intercept_envelope"),
        ),
        validation_row(
            "free_A_is_retained_as_low_power_falsifier_not_primary_error_disk",
            bool(evaluation["a_compatible"])
            and free_a_normalized_separation <= 1.0
            and cross_family_central_shift
            <= float(evaluation["intercept_combined_disk"]),
            {
                "free_A_base_disk": free_base_disk,
                "strict_envelope_fraction": free_fraction,
                "normalized_A_separation": free_a_normalized_separation,
            },
        ),
        validation_row(
            "conditional_fixed_A_envelope_passes_unchanged_one_percent_gate",
            conditional_stability,
            relative_envelope,
        ),
        validation_row(
            "uniform_remainder_and_all_broad_claims_remain_false",
            parent_5360.get("numeric_remainder_constant_available") is False
            and all(claims[field] is False for field in FALSE_CLAIMS),
            false_claims(),
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5370.formal_inventory_digest() == FORMAL_DIGEST,
            M5370.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    artifact_passed = all(parse_bool(row["passed"]) for row in validations)
    component_rows = [
        {
            "component": name,
            "absolute_contribution": value,
            "role": role,
            "included_in_fixed_A_envelope": True,
            **claims,
        }
        for name, value, role in components
    ]
    component_rows.append(
        {
            "component": "unconstrained_free_A_base_disk",
            "absolute_contribution": free_base_disk,
            "role": "FALSIFIER_ESTIMATOR_DISK_NOT_PROPAGATED_INTO_FIXED_A_ESTIMATOR",
            "included_in_fixed_A_envelope": False,
            **claims,
        }
    )
    estimator_rows = [
        {
            "epsilon_id": row["epsilon_id"],
            "epsilon": row["epsilon"],
            "intercept_projection_real": float(complex(projection[index]).real),
            "intercept_projection_imaginary": float(
                complex(projection[index]).imag
            ),
            "input_disk_radius": row["radius"],
            "absolute_disk_contribution": abs(projection[index]) * row["radius"],
            **claims,
        }
        for index, row in enumerate(inputs)
    ]
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-derived-A-primary-role-separation-postmeasurement-gate",
        "validation_passed": artifact_passed,
        "decision": (
            "D4_DERIVED_A_FIXED_PRIMARY_ENVELOPE_PASSES__CONDITIONAL_NUMERICAL_STABILITY_ONLY"
            if artifact_passed and conditional_stability
            else "D4_DERIVED_A_FIXED_PRIMARY_ENVELOPE_BLOCKED"
        ),
        "postmeasurement_role_audit": True,
        "preregistered_before_5373_measurement": False,
        "strict_5373_gate_remains_failed": True,
        **complex_fields("derived_A", source_a),
        "derived_A_disk_radius": source_a_radius,
        **complex_fields("fixed_A_intercept", fixed_intercept),
        "fixed_A_input_data_disk": data_disk,
        "fixed_A_correlated_A_disk": a_disk,
        "fixed_A_base_estimator_disk": base_disk,
        "fixed_A_conservative_envelope": envelope,
        "relative_fixed_A_envelope": relative_envelope,
        "relative_limit": RELATIVE_LIMIT,
        "conditional_fixed_A_stability_passes": conditional_stability,
        "strict_all_model_envelope": strict_envelope,
        "strict_all_model_relative_envelope": parent_5373[
            "relative_intercept_envelope"
        ],
        "free_A_base_disk": free_base_disk,
        "free_A_fraction_of_strict_envelope": free_fraction,
        "free_A_normalized_source_separation": free_a_normalized_separation,
        "fixed_A_maximum_normalized_residual": fixed[
            "maximum_normalized_residual"
        ],
        "uniform_numeric_remainder_bound_available": False,
        "claim_boundary": claims,
        "remaining_obstruction": "derive or numerically bound the uniform M_D4 remainder constant before the unconditional D4 outer-regulator limit",
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    contract = contract_rows()
    final_sources = tuple(dict.fromkeys((*source_paths(), CONTRACT, COMPONENTS, ESTIMATOR)))
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": True,
            **claims,
        }
        for path in final_sources
        if path.is_file()
    ]
    atomic_csv(CONTRACT, contract)
    atomic_csv(COMPONENTS, component_rows)
    atomic_csv(ESTIMATOR, estimator_rows)
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_json(RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if artifact_passed else "blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": True,
            **claims,
        }
        for path in tuple(
            dict.fromkeys((*source_paths(), CONTRACT, COMPONENTS, ESTIMATOR, VALIDATION, RESULT, DOCUMENT))
        )
    ]
    atomic_csv(SOURCE_REGISTER, source_rows)
    return payload


def validate_saved() -> dict[str, Any]:
    required = (CONTRACT, COMPONENTS, ESTIMATOR, RESULT, VALIDATION, SOURCE_REGISTER)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    payload = read_json(RESULT)
    sources = source_register_current(SOURCE_REGISTER)
    checks = {
        "saved_result_passes": payload.get("validation_passed") is True,
        "saved_validation_rows_pass": csv_passes(VALIDATION),
        "saved_sources_are_current": sources[0] and sources[1] > 0,
        "strict_parent_failure_preserved": payload.get(
            "strict_5373_gate_remains_failed"
        )
        is True
        and payload.get("preregistered_before_5373_measurement") is False,
        "conditional_fixed_A_result_passes": payload.get(
            "conditional_fixed_A_stability_passes"
        )
        is True,
        "broad_claims_remain_false": all(
            payload.get("claim_boundary", {}).get(field) is False
            for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": M5370.formal_inventory_digest()
        == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "validation_passed": all(checks.values()),
        "decision": (
            "D4_DERIVED_A_PRIMARY_ROLE_SEPARATION_VALIDATED"
            if all(checks.values())
            else "D4_DERIVED_A_PRIMARY_ROLE_SEPARATION_VALIDATION_FAILED"
        ),
        "checks": checks,
        "source_drifts": sources[2],
        "relative_fixed_A_envelope": payload.get("relative_fixed_A_envelope"),
        "strict_all_model_relative_envelope": payload.get(
            "strict_all_model_relative_envelope"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    arguments = parser.parse_args()
    set_below_normal_priority()
    payload = execute() if arguments.mode == "run" else validate_saved()
    print(json.dumps(normalize(payload), indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("validation_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
