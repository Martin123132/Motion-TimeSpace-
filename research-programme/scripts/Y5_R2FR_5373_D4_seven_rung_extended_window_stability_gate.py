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

SCRIPT_5370 = SCRIPTS / "Y5_R2FR_5370_D4_six_rung_complete_family_outer_limit_gate.py"
SCRIPT_5371 = SCRIPTS / "Y5_R2FR_5371_D4_E020_preregistered_seventh_rung_runner.py"
SCRIPT_5372 = SCRIPTS / "Y5_R2FR_5372_D4_E020_blind_holdout_comparator.py"

PREREG_RESULT = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_preregistration_result.json"
FIT_PREREGISTRATION = FUNCTIONAL_RG / "5345" / "D4_zero_fit_preregistration.csv"
RUNG_PREREGISTRATION = FUNCTIONAL_RG / "5345" / "D4_zero_rung_count_gate.csv"
ASYMPTOTIC_CONTRACT = FUNCTIONAL_RG / "5345" / "D4_regulator_zero_endpoint_asymptotic_contract.csv"
FIXED_A_RESULT = FUNCTIONAL_RG / "5360" / "D4_fixed_A_subtraction_result.json"

SIX_GATE_CONTRACT = FUNCTIONAL_RG / "5370" / "D4_six_rung_outer_limit_gate_contract.json"
SIX_GATE_RESULT = FUNCTIONAL_RG / "5370" / "D4_six_rung_outer_limit_result.json"
SIX_GATE_VALIDATION = FUNCTIONAL_RG / "5370" / "D4_six_rung_outer_limit_validation.csv"

RUNNER_ROOT = FUNCTIONAL_RG / "5371" / "E020"
RUNNER_RESULT = RUNNER_ROOT / "D4_E020_seventh_rung_runner_result.json"
RUNNER_VALIDATION = RUNNER_ROOT / "D4_E020_seventh_rung_runner_validation.csv"
RUNNER_SOURCES = RUNNER_ROOT / "source_register.csv"

COMPARATOR_ROOT = FUNCTIONAL_RG / "5372" / "E020"
COMPARATOR_CONTRACT = COMPARATOR_ROOT / "D4_E020_blind_holdout_comparison_contract.json"
COMPARATOR_CONTRACT_VALIDATION = COMPARATOR_ROOT / "D4_E020_blind_holdout_comparison_contract_validation.csv"
COMPARATOR_CONTRACT_SOURCES = COMPARATOR_ROOT / "D4_E020_blind_holdout_comparison_contract_sources.csv"
COMPARATOR_RESULT = COMPARATOR_ROOT / "D4_E020_blind_holdout_comparison_result.json"
COMPARATOR_VALIDATION = COMPARATOR_ROOT / "D4_E020_blind_holdout_comparison_validation.csv"
COMPARATOR_SOURCES = COMPARATOR_ROOT / "source_register.csv"

E020_ROOT = FUNCTIONAL_RG / "5334" / "E020"
E020_FINITE = E020_ROOT / "D4_outer_event_aligned_E020_finite_value.csv"
E020_RESULT = E020_ROOT / "D4_outer_event_aligned_E020_result.json"
E020_VALIDATION = E020_ROOT / "D4_outer_event_aligned_E020_validation.csv"
E020_SEMANTIC_VALIDATION = E020_ROOT / "D4_outer_event_aligned_E020_semantic_validation.csv"

OUTPUT = FUNCTIONAL_RG / "5373"
GATE_CONTRACT = OUTPUT / "D4_seven_rung_extended_window_gate_contract.json"
GATE_CONTRACT_VALIDATION = OUTPUT / "D4_seven_rung_extended_window_gate_contract_validation.csv"
GATE_CONTRACT_SOURCES = OUTPUT / "D4_seven_rung_extended_window_gate_contract_sources.csv"
RESULT = OUTPUT / "D4_seven_rung_extended_window_result.json"
INPUTS = OUTPUT / "D4_seven_rung_inputs.csv"
FIXED_A_FIT = OUTPUT / "D4_seven_rung_fixed_A_complete_fit.csv"
FREE_A_FIT = OUTPUT / "D4_seven_rung_free_A_complete_fit.csv"
RESIDUALS_TABLE = OUTPUT / "D4_seven_rung_model_residuals.csv"
LOO_TABLE = OUTPUT / "D4_seven_rung_leave_one_out_stability.csv"
DIAGNOSTICS = OUTPUT / "D4_seven_rung_intercept_diagnostics.csv"
GATES = OUTPUT / "D4_seven_rung_stability_gates.csv"
VALIDATION = OUTPUT / "D4_seven_rung_extended_window_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5373_VALIDATION.csv"
DOCUMENT = POST / "5373-Y5-R2FR-D4-seven-rung-extended-window-stability-gate.md"

CHECKPOINT = 5373
MARKER = "MTS_5373_D4_SEVEN_RUNG_EXTENDED_WINDOW_STABILITY_GATE"
REVISION = "D4-seven-rung-extended-window-stability-gate-v1"
EXPECTED_IDS = (
    "E0003125",
    "E000625",
    "E00125",
    "E0025",
    "E005",
    "E010",
    "E020",
)
EPSILON_REFERENCE = 0.0025
RESIDUAL_DISK_LIMIT = 1.0
RELATIVE_INTERCEPT_LIMIT = 0.01
CONDITION_TIMES_EPSILON_LIMIT = 1.0e-8
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
FIXED_A_MODEL = "I=A_source*e*Log(e/e_ref)+I0+B*e+C*e^2*Log(e/e_ref)+D*e^2"
FREE_A_MODEL = "I=I0+A*e*Log(e/e_ref)+B*e+C*e^2*Log(e/e_ref)+D*e^2"
HALF_POWER_MODEL = "I=H0+H1*sqrt(e)+H2*e__FALSIFIER_ONLY"
WINDOW_DISCLOSURE = (
    "Seven accepted points E0003125..E020 form an extended-small-epsilon stability window. "
    "This is not the identical E000625..E040 seven-point window tabulated at checkpoint 5345."
)

CLAIM_CONTRACT = "valid_for_D4_seven_rung_extended_window_gate_contract"
CLAIM_FIT = "valid_for_D4_seven_rung_complete_second_order_fit"
CLAIM_CONDITIONAL_LIMIT = "valid_for_D4_conditional_seven_rung_outer_regulator_zero_limit"
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


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5370 = load_module("mts_5370_for_5373", SCRIPT_5370)


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


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if hasattr(value, "item"):
        return normalize(value.item())
    return value


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
    rows = [normalize(row) for row in rows]
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
    payload = normalize(payload)
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


def accepted_E020_measurement_available() -> bool:
    if E020_RESULT.is_file():
        result = read_json(E020_RESULT)
        if result.get("acceptance_passed") is True and result.get("completed_full_run") is True:
            return True
    if E020_FINITE.is_file():
        return any(
            parse_bool(row.get("finite_regulator_fixed_decay_integral_accepted", False))
            for row in read_csv(E020_FINITE)
        )
    return False


def contract_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5370,
        SCRIPT_5371,
        SCRIPT_5372,
        PREREG_RESULT,
        FIT_PREREGISTRATION,
        RUNG_PREREGISTRATION,
        ASYMPTOTIC_CONTRACT,
        FIXED_A_RESULT,
        SIX_GATE_CONTRACT,
        SIX_GATE_RESULT,
        SIX_GATE_VALIDATION,
        RUNNER_RESULT,
        RUNNER_VALIDATION,
        RUNNER_SOURCES,
        COMPARATOR_CONTRACT,
        COMPARATOR_CONTRACT_VALIDATION,
        COMPARATOR_CONTRACT_SOURCES,
    )


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5373 - D4 seven-rung extended-window stability gate",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        WINDOW_DISCLOSURE,
        "",
    ]
    if payload.get("gate_executed"):
        lines.extend(
            [
                f"- fixed-A maximum normalized residual: `{payload['fixed_A_maximum_normalized_residual']}`;",
                f"- free-A maximum normalized residual: `{payload['free_A_maximum_normalized_residual']}`;",
                f"- relative intercept envelope: `{payload['relative_intercept_envelope']}`;",
                f"- strict gate passes: `{payload['outer_limit_gate_passes']}`.",
                "",
            ]
        )
    lines.append(
        "A pass is conditional on the parent normal-form hypotheses. It does not supply the separate numeric uniform remainder, angular, UV, local-GR, or full-MTS proof."
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def freeze_gate_contract() -> dict[str, Any]:
    required = contract_source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    runner = read_json(RUNNER_RESULT)
    comparator = read_json(COMPARATOR_CONTRACT)
    six_contract = read_json(SIX_GATE_CONTRACT)
    runner_sources = source_register_current(RUNNER_SOURCES)
    comparator_sources = source_register_current(COMPARATOR_CONTRACT_SOURCES)
    seven_rung_rows = [
        row for row in read_csv(RUNG_PREREGISTRATION) if int(row["accepted_rung_count"]) == 7
    ]
    seven_fit_rows = [
        row
        for row in read_csv(FIT_PREREGISTRATION)
        if row["model_id"] == "D4_Q5_COMPLETE_SECOND_ORDER"
        and int(row["point_count"]) == 7
    ]
    measurement_absent = not accepted_E020_measurement_available()
    checks = {
        "checkpoint_5345_has_preferred_seven_rung_model_family": len(seven_rung_rows) == 1
        and seven_rung_rows[0]["allowed_decision"] == "PREFERRED_FULL_LADDER_GATE"
        and len(seven_fit_rows) == 1
        and parse_bool(seven_fit_rows[0]["full_rank"]),
        "extended_window_difference_is_explicit": "not the identical" in WINDOW_DISCLOSURE
        and tuple(EXPECTED_IDS) != (
            "E000625",
            "E00125",
            "E0025",
            "E005",
            "E010",
            "E020",
            "E040",
        ),
        "checkpoint_5370_supplies_unchanged_models_and_thresholds": six_contract.get(
            "validation_passed"
        )
        is True
        and six_contract.get("fixed_A_model") == FIXED_A_MODEL
        and six_contract.get("free_A_model") == FREE_A_MODEL
        and six_contract.get("half_power_model") == HALF_POWER_MODEL
        and six_contract.get("residual_disk_limit") == RESIDUAL_DISK_LIMIT
        and six_contract.get("relative_intercept_limit") == RELATIVE_INTERCEPT_LIMIT
        and six_contract.get("condition_times_epsilon_limit")
        == CONDITION_TIMES_EPSILON_LIMIT
        and csv_passes(SIX_GATE_VALIDATION),
        "checkpoint_5371_runner_setup_is_source_current": runner.get("validation_passed") is True
        and csv_passes(RUNNER_VALIDATION)
        and runner_sources[0]
        and runner_sources[1] > 0,
        "checkpoint_5372_comparison_contract_is_frozen_and_current": comparator.get(
            "validation_passed"
        )
        is True
        and comparator.get("measurement_absent_at_freeze") is True
        and comparator.get("comparison_executed") is False
        and csv_passes(COMPARATOR_CONTRACT_VALIDATION)
        and comparator_sources[0]
        and comparator_sources[1] > 0,
        "accepted_E020_measurement_is_absent_at_gate_freeze": measurement_absent,
        "numeric_gates_are_fixed_before_measurement": RESIDUAL_DISK_LIMIT == 1.0
        and RELATIVE_INTERCEPT_LIMIT == 0.01
        and CONDITION_TIMES_EPSILON_LIMIT == 1.0e-8,
        "both_complete_models_and_half_power_falsifier_are_fixed": FIXED_A_MODEL.startswith(
            "I=A_source*e*Log"
        )
        and FREE_A_MODEL.startswith("I=I0+A*e*Log")
        and "FALSIFIER_ONLY" in HALF_POWER_MODEL,
        "broad_claims_are_locked_false": all(value is False for value in false_claims().values()),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    validations = [validation_row(key, value, value) for key, value in checks.items()]
    passed = all(checks.values())
    claims = {
        CLAIM_CONTRACT: passed,
        CLAIM_FIT: False,
        CLAIM_CONDITIONAL_LIMIT: False,
        CLAIM_LIMIT: False,
        **false_claims(),
    }
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-seven-rung-extended-window-gate-contract",
        "validation_passed": passed,
        "decision": (
            "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_FROZEN__AWAIT_E020_MEASUREMENT"
            if passed
            else "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_CONTRACT_BLOCKED"
        ),
        "measurement_absent_at_freeze": measurement_absent,
        "gate_executed": False,
        "expected_epsilon_ids": list(EXPECTED_IDS),
        "window_disclosure": WINDOW_DISCLOSURE,
        "fixed_A_model": FIXED_A_MODEL,
        "free_A_model": FREE_A_MODEL,
        "half_power_model": HALF_POWER_MODEL,
        "residual_disk_limit": RESIDUAL_DISK_LIMIT,
        "relative_intercept_limit": RELATIVE_INTERCEPT_LIMIT,
        "condition_times_epsilon_limit": CONDITION_TIMES_EPSILON_LIMIT,
        "required_scientific_gates": [
            "E020 frozen blind holdout compatible",
            "fixed-A and free-A designs full rank",
            "fixed-A and free-A residuals inside conservative disks",
            "free-A coefficient disk-compatible with source A",
            "fixed-A and free-A intercept disks compatible",
            "conservative intercept envelope below one percent",
            "half-power falsifier reported but not selected",
        ],
        "limit_scope": "conditional numerical D4_OUTER stability result under parent normal-form hypotheses; numeric uniform M_D4 remains separate",
        "runner_node_plan_sha256": runner["node_plan_sha256"],
        "comparator_contract_sha256": digest(COMPARATOR_CONTRACT),
        "claim_boundary": claims,
        "runner_source_drifts": runner_sources[2],
        "comparator_source_drifts": comparator_sources[2],
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in required
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(GATE_CONTRACT_VALIDATION, validations)
    atomic_csv(GATE_CONTRACT_SOURCES, source_rows)
    atomic_json(GATE_CONTRACT, payload)
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


def load_inputs() -> list[dict[str, Any]]:
    rows = list(M5370.load_inputs())
    finite_rows = read_csv(E020_FINITE)
    if len(finite_rows) != 1:
        raise RuntimeError("exactly one accepted E020 finite row is required")
    finite = finite_rows[0]
    rows.append(
        {
            "epsilon_id": finite["epsilon_id"],
            "epsilon": float(finite["epsilon"]),
            "value": complex(
                float(finite["fixed_decay_integral_real"]),
                float(finite["fixed_decay_integral_imaginary"]),
            ),
            "radius": float(finite["total_error_absolute_conservative"]),
            "source_path": E020_FINITE,
            "source_sha256": digest(E020_FINITE),
            "accepted": parse_bool(
                finite["finite_regulator_fixed_decay_integral_accepted"]
            ),
            "finite_row_accepted_and_value_matches": parse_bool(
                finite["finite_regulator_fixed_decay_integral_accepted"]
            )
            and parse_bool(finite["valid_for_D4_outer_E020_fixed_decay_integral"]),
        }
    )
    return sorted(rows, key=lambda row: row["epsilon"])


def run_preflight() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    required = (
        GATE_CONTRACT,
        GATE_CONTRACT_VALIDATION,
        GATE_CONTRACT_SOURCES,
        COMPARATOR_RESULT,
        COMPARATOR_VALIDATION,
        COMPARATOR_SOURCES,
        E020_FINITE,
        E020_RESULT,
        E020_VALIDATION,
        E020_SEMANTIC_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    contract = read_json(GATE_CONTRACT)
    comparator = read_json(COMPARATOR_RESULT)
    E020_result = read_json(E020_RESULT)
    contract_sources = source_register_current(GATE_CONTRACT_SOURCES)
    comparator_sources = source_register_current(COMPARATOR_SOURCES)
    inputs = load_inputs()
    checks = {
        "gate_contract_was_frozen_before_measurement_and_is_current": contract.get(
            "validation_passed"
        )
        is True
        and contract.get("measurement_absent_at_freeze") is True
        and contract.get("gate_executed") is False
        and contract.get("expected_epsilon_ids") == list(EXPECTED_IDS)
        and csv_passes(GATE_CONTRACT_VALIDATION)
        and contract_sources[0]
        and contract_sources[1] > 0,
        "E020_frozen_blind_holdout_is_valid_and_compatible": comparator.get(
            "validation_passed"
        )
        is True
        and comparator.get("holdout_compatible") is True
        and csv_passes(COMPARATOR_VALIDATION)
        and comparator_sources[0]
        and comparator_sources[1] > 0,
        "exactly_seven_accepted_source_current_rungs_are_present": len(inputs) == 7
        and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
        and all(row["accepted"] for row in inputs)
        and all(row["finite_row_accepted_and_value_matches"] for row in inputs)
        and all(
            row["source_path"].is_file()
            and digest(row["source_path"]) == row["source_sha256"]
            and row["radius"] > 0.0
            and math.isfinite(row["radius"])
            and math.isfinite(row["value"].real)
            and math.isfinite(row["value"].imag)
            for row in inputs
        ),
        "E020_integral_is_independently_accepted": E020_result.get(
            "acceptance_passed"
        )
        is True
        and E020_result.get("completed_full_run") is True
        and int(E020_result.get("failed_inner_node_count", -1)) == 0
        and E020_result.get("all_adaptive_leaf_gates_pass") is True
        and csv_passes(E020_VALIDATION)
        and csv_passes(E020_SEMANTIC_VALIDATION),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"seven-rung preflight failed: {checks}; contract drifts={contract_sources[2]}; comparator drifts={comparator_sources[2]}"
        )
    return contract, inputs


def execute_gate() -> dict[str, Any]:
    contract, inputs = run_preflight()
    evaluation = M5370.evaluate(inputs)
    fixed = evaluation["fixed"]
    free = evaluation["free"]
    scientific_gates = {
        "seventh_frozen_blind_holdout_compatible": read_json(COMPARATOR_RESULT).get(
            "holdout_compatible"
        )
        is True,
        "fixed_A_design_full_rank_and_resolved": fixed["rank"] == 4
        and fixed["degrees_of_freedom"] == 3
        and fixed["condition_times_epsilon"] < CONDITION_TIMES_EPSILON_LIMIT,
        "free_A_design_full_rank_and_resolved": free["rank"] == 5
        and free["degrees_of_freedom"] == 2
        and free["condition_times_epsilon"] < CONDITION_TIMES_EPSILON_LIMIT,
        "fixed_A_residuals_inside_conservative_disks": fixed[
            "maximum_normalized_residual"
        ]
        <= RESIDUAL_DISK_LIMIT,
        "free_A_residuals_inside_conservative_disks": free[
            "maximum_normalized_residual"
        ]
        <= RESIDUAL_DISK_LIMIT,
        "free_A_fit_is_disk_compatible_with_source_A": bool(evaluation["a_compatible"]),
        "fixed_A_and_free_A_intercepts_are_disk_compatible": bool(
            evaluation["intercepts_compatible"]
        ),
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
            contract.get("measurement_absent_at_freeze") is True,
            contract["updated_utc"],
        ),
        validation_row(
            "seven_source_current_inputs_are_finite_and_ordered",
            len(inputs) == 7
            and tuple(row["epsilon_id"] for row in inputs) == EXPECTED_IDS
            and all(row["accepted"] for row in inputs),
            EXPECTED_IDS,
        ),
        validation_row(
            "fixed_and_free_design_dimensions_match_frozen_contract",
            fixed["rank"] == 4
            and fixed["degrees_of_freedom"] == 3
            and free["rank"] == 5
            and free["degrees_of_freedom"] == 2,
            {
                "fixed": (fixed["rank"], fixed["degrees_of_freedom"]),
                "free": (free["rank"], free["degrees_of_freedom"]),
            },
        ),
        validation_row(
            "all_reported_fit_diagnostics_are_finite",
            all(
                math.isfinite(float(value))
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
            "extended_window_is_not_mislabeled_as_exact_5345_window",
            "not the identical" in contract["window_disclosure"],
            contract["window_disclosure"],
        ),
        validation_row(
            "uniform_remainder_and_broad_claims_remain_separate",
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
    artifact_passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_CONTRACT: artifact_passed,
        CLAIM_FIT: artifact_passed,
        CLAIM_CONDITIONAL_LIMIT: artifact_passed and outer_gate_passes,
        CLAIM_LIMIT: artifact_passed and outer_gate_passes,
        **false_claims(),
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
                "fixed_A_normalized_residual": float(
                    abs(fixed["residuals"][index]) / row["radius"]
                ),
                **complex_fields("free_A_prediction", complex(free["predictions"][index])),
                **complex_fields("free_A_residual", complex(free["residuals"][index])),
                "free_A_normalized_residual": float(
                    abs(free["residuals"][index]) / row["radius"]
                ),
                **claims,
            }
        )
    loo_rows = []
    for row in evaluation["loo_rows"]:
        copied = dict(row)
        if "distance_from_six_rung_weighted_intercept" in copied:
            copied["distance_from_seven_rung_weighted_intercept"] = copied.pop(
                "distance_from_six_rung_weighted_intercept"
            )
        copied.update(claims)
        loo_rows.append(copied)
    diagnostic_row = {
        **complex_fields("fixed_A_weighted_intercept", evaluation["fixed_intercept"]),
        **complex_fields("free_A_weighted_intercept", evaluation["free_intercept"]),
        **complex_fields("source_A", evaluation["source_a"]),
        "source_A_disk_radius": evaluation["source_a_radius"],
        **complex_fields("free_fitted_A", evaluation["fitted_a"]),
        "free_fitted_A_disk_radius": evaluation["fitted_a_disk"],
        "source_A_separation": evaluation["a_separation"],
        "source_A_combined_disk_radius": evaluation["a_combined_disk"],
        "source_A_compatible": bool(evaluation["a_compatible"]),
        "fixed_free_intercept_separation": evaluation["intercept_separation"],
        "fixed_free_intercept_combined_disk_radius": evaluation[
            "intercept_combined_disk"
        ],
        "fixed_free_intercepts_compatible": bool(evaluation["intercepts_compatible"]),
        "fixed_A_base_intercept_disk": evaluation["fixed_base_disk"],
        "free_A_base_intercept_disk": evaluation["free_base_disk"],
        "weighted_unweighted_shift": evaluation["weighted_unweighted_shift"],
        "fixed_A_leave_one_out_spread": evaluation["fixed_loo_spread"],
        "free_A_leave_one_out_spread": evaluation["free_loo_spread"],
        "leading_vs_fixed_A_shift": evaluation["leading_shift"],
        "fixed_vs_free_complete_model_shift": evaluation["complete_model_shift"],
        "maximum_absolute_complete_fit_residual": evaluation["maximum_absolute_residual"],
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
        {"gate": gate, "passed": bool(passed), "detail": str(bool(passed)), **claims}
        for gate, passed in scientific_gates.items()
    ]
    gate_rows.append(
        {
            "gate": "D4_outer_regulator_zero_limit",
            "passed": outer_gate_passes,
            "detail": "conditional extended-window numerical gate; numeric uniform M_D4 remains separate",
            **claims,
        }
    )
    decision = (
        "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_PASSES__CONDITIONAL_OUTER_LIMIT_ACCEPTED"
        if artifact_passed and outer_gate_passes
        else "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_FAILS__OUTER_LIMIT_REMAINS_BLOCKED"
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-seven-rung-extended-window-stability-gate",
        "validation_passed": artifact_passed,
        "decision": decision,
        "gate_executed": True,
        "accepted_rung_count": len(inputs),
        "accepted_epsilon_ids": list(EXPECTED_IDS),
        "window_disclosure": WINDOW_DISCLOSURE,
        "fixed_A_fit_parameter_count": 4,
        "fixed_A_fit_degrees_of_freedom": fixed["degrees_of_freedom"],
        "free_A_fit_parameter_count": 5,
        "free_A_fit_degrees_of_freedom": free["degrees_of_freedom"],
        **complex_fields("intercept", evaluation["fixed_intercept"]),
        "intercept_envelope": evaluation["intercept_envelope"],
        "relative_intercept_envelope": evaluation["relative_envelope"],
        "preregistered_relative_limit": RELATIVE_INTERCEPT_LIMIT,
        "fixed_A_maximum_normalized_residual": fixed["maximum_normalized_residual"],
        "free_A_maximum_normalized_residual": free["maximum_normalized_residual"],
        "source_A_compatible_with_free_fit": bool(evaluation["a_compatible"]),
        "fixed_free_intercepts_compatible": bool(evaluation["intercepts_compatible"]),
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
            "derive or numerically bound uniform M_D4, then continue to the independent decay-angle limit"
            if outer_gate_passes
            else "inspect the failed frozen gate without changing its thresholds"
        ),
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    final_sources = tuple(
        dict.fromkeys(
            (
                *contract_source_paths(),
                GATE_CONTRACT,
                GATE_CONTRACT_VALIDATION,
                GATE_CONTRACT_SOURCES,
                COMPARATOR_RESULT,
                COMPARATOR_VALIDATION,
                COMPARATOR_SOURCES,
                E020_FINITE,
                E020_RESULT,
                E020_VALIDATION,
                E020_SEMANTIC_VALIDATION,
                *(row["source_path"] for row in inputs),
            )
        )
    )
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in final_sources
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(INPUTS, input_rows)
    atomic_csv(FIXED_A_FIT, fixed_rows)
    atomic_csv(FREE_A_FIT, free_rows)
    atomic_csv(RESIDUALS_TABLE, residual_rows)
    atomic_csv(LOO_TABLE, loo_rows)
    atomic_csv(DIAGNOSTICS, [diagnostic_row])
    atomic_csv(GATES, gate_rows)
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete",
            "decision": decision,
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return normalize(payload)


def validate_saved() -> dict[str, Any]:
    required = (RESULT, VALIDATION, SOURCE_REGISTER, GATE_CONTRACT, GATE_CONTRACT_VALIDATION, GATE_CONTRACT_SOURCES)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    payload = read_json(RESULT)
    sources = source_register_current(SOURCE_REGISTER)
    contract_sources = source_register_current(GATE_CONTRACT_SOURCES)
    checks = {
        "saved_result_validates": payload.get("validation_passed") is True,
        "saved_validation_passes": csv_passes(VALIDATION),
        "saved_sources_are_current": sources[0] and sources[1] > 0,
        "frozen_gate_sources_are_current": contract_sources[0]
        and contract_sources[1] > 0,
        "window_disclosure_is_preserved": "not the identical"
        in payload.get("window_disclosure", ""),
        "uniform_and_broad_claims_remain_false": payload.get(
            "uniform_numeric_remainder_bound_available"
        )
        is False
        and all(
            payload.get("claim_boundary", {}).get(field) is False for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "validation_passed": all(checks.values()),
        "decision": "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_VALIDATED" if all(checks.values()) else "D4_SEVEN_RUNG_EXTENDED_WINDOW_GATE_VALIDATION_FAILED",
        "checks": checks,
        "source_drifts": sources[2],
        "contract_source_drifts": contract_sources[2],
        "outer_limit_gate_passes": payload.get("outer_limit_gate_passes"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("freeze", "run", "validate"), required=True)
    arguments = parser.parse_args()
    set_below_normal_priority()
    if arguments.mode == "freeze":
        payload = freeze_gate_contract()
    elif arguments.mode == "run":
        payload = execute_gate()
    else:
        payload = validate_saved()
    print(json.dumps(normalize(payload), indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("validation_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
