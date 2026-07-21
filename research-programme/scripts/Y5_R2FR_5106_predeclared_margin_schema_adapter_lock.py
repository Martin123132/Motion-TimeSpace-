from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5040 = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SCRIPT_5080 = POST / "scripts" / "Y5_R2FR_5080_locked_fresh_pilot_analysis.py"
SCRIPT_5105 = POST / "scripts" / "Y5_R2FR_5105_execute_predeclared_5080_analysis_v12.py"
SCRIPT_5107 = POST / "scripts" / "Y5_R2FR_5107_execute_5080_v12_with_margin_adapter.py"
ORIGINAL_V12_LOCK = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_lock_v12.json"
ADAPTER_LOCK = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_lock_v12_margin_adapter.json"
HISTORICAL_CONFIG = POST / "source-intake" / "functional_rg" / "5040" / "runs" / "nested_sobol_power1_s4_v1" / "config.json"
MARGIN_SOURCE = POST / "source-intake" / "functional_rg" / "5018" / "known_master_without_hhh_and_matched_hhh_target.csv"
TARGET_OUTPUTS = (
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_v12.json",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_channels_v12.csv",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_event_costs_v12.csv",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_jackknife_v12.csv",
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5080_V12_VALIDATION.csv",
)
FAILURE_SOURCE = POST / "source-intake" / "functional_rg" / "5105"
FAILURE_JSON = FAILURE_SOURCE / "predeclared_5080_v12_schema_failure.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5106"
RESULT_JSON = SOURCE / "predeclared_margin_schema_adapter_lock.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5106_VALIDATION.csv"
MARKER = "MTS_5106_PREDECLARED_MARGIN_SCHEMA_ADAPTER_LOCK"
REVISION = "historical-5040-budget-row-schema-adapter-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def derive_budget_rows() -> list[dict[str, Any]]:
    with MARGIN_SOURCE.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        residual = float(source["known_nonlocal_residual"])
        target = float(source["required_matched_hhh_nonlocal_cyclic_D_over_G3"])
        error = float(source["known_master_error"])
        if not math.isclose(target, -0.5 * residual, rel_tol=0.0, abs_tol=1.0e-12):
            raise RuntimeError("5018 target no longer equals the signed half-residual")
        margin = 0.5 * error
        rows.append(
            {
                "physical_s_channel_cosine": float(source["physical_s_channel_cosine"]),
                "fixed_target": target,
                "known_master_error": error,
                "target_equivalence_margin": margin,
                "statistical_halfwidth_budget": 0.5 * margin,
                "epsilon_bias_budget": 0.5 * margin,
                "margin_derivation": "target=-known_nonlocal_residual/2; margin=known_master_error/2",
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def main() -> None:
    required = [
        SCRIPT_5040,
        SCRIPT_5080,
        SCRIPT_5105,
        SCRIPT_5107,
        ORIGINAL_V12_LOCK,
        HISTORICAL_CONFIG,
        MARGIN_SOURCE,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    if ADAPTER_LOCK.exists():
        raise RuntimeError("margin-adapter analysis lock already exists")
    outputs_absent = all(not path.exists() for path in TARGET_OUTPUTS)
    if not outputs_absent:
        raise RuntimeError("aggregate outputs exist after the failed schema attempt")
    original_lock = read_json(ORIGINAL_V12_LOCK)
    historical_config = read_json(HISTORICAL_CONFIG)
    historical_rows = historical_config.get("target_precision_budgets", [])
    derived_rows = derive_budget_rows()
    formal_digest = tree_digest(FORMAL)
    guards = {
        "first_wrapper_was_hash_locked": original_lock.get("execution_wrapper_sha256")
        == digest(SCRIPT_5105),
        "unchanged_analysis_script_retained": original_lock.get("analysis_script_sha256")
        == digest(SCRIPT_5080),
        "failed_before_any_aggregate_output": outputs_absent,
        "historical_budget_has_five_rows": len(historical_rows) == 5,
        "historical_budget_rederived_exactly": historical_rows == derived_rows,
        "historical_budget_is_nonclaim": all(
            not bool(row.get("valid_for_full_MTS_claim")) for row in historical_rows
        ),
        "target_central_values_still_excluded": not bool(
            original_lock.get("target_central_values_used")
        ),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    adapter_authorized = all(guards.values())
    failure_record = {
        "checkpoint_marker": "MTS_5105_EXECUTE_PREDECLARED_5080_ANALYSIS_V12",
        "revision": "one-shot-unchanged-analysis-code-execution-v1",
        "outcome": "SCHEMA_FAILURE_BEFORE_RESULT_WRITE",
        "error_type": "KeyError",
        "missing_key": "target_precision_budgets",
        "failed_source_line": "Y5_R2FR_5080_locked_fresh_pilot_analysis.py:304",
        "aggregate_outputs_absent_after_failure": outputs_absent,
        "statistical_result_obtained": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(FAILURE_JSON, failure_record)
    candidate = copy.deepcopy(original_lock)
    candidate.update(
        {
            "binding_checkpoint_marker": MARKER,
            "binding_revision": REVISION,
            "execution_wrapper_path": str(SCRIPT_5107),
            "execution_wrapper_sha256": digest(SCRIPT_5107),
            "prior_failed_wrapper_path": str(SCRIPT_5105),
            "prior_failed_wrapper_sha256": digest(SCRIPT_5105),
            "prior_failure_record": str(FAILURE_JSON),
            "prior_failure_record_sha256": digest(FAILURE_JSON),
            "margin_schema_adapter": {
                "field": "target_precision_budgets",
                "historical_config_path": str(HISTORICAL_CONFIG),
                "historical_config_sha256": digest(HISTORICAL_CONFIG),
                "historical_rows_sha256": canonical_digest(historical_rows),
                "source_5018_path": str(MARGIN_SOURCE),
                "source_5018_sha256": digest(MARGIN_SOURCE),
                "derivation_script_path": str(SCRIPT_5040),
                "derivation_script_sha256": digest(SCRIPT_5040),
                "formula": "target=-known_nonlocal_residual/2; margin=known_master_error/2",
                "row_count": len(historical_rows),
                "analysis_semantics_changed": False,
            },
            "schema_adapter_authorized": adapter_authorized,
            "aggregate_outputs_absent_before_adapter_lock": outputs_absent,
        }
    )
    if adapter_authorized:
        atomic_json(ADAPTER_LOCK, candidate)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "original_v12_lock": str(ORIGINAL_V12_LOCK),
        "adapter_lock": str(ADAPTER_LOCK),
        "adapter_lock_sha256": digest(ADAPTER_LOCK) if ADAPTER_LOCK.exists() else None,
        "failure_record": str(FAILURE_JSON),
        "historical_rows_sha256": canonical_digest(historical_rows),
        "derived_rows_sha256": canonical_digest(derived_rows),
        "margin_values": [
            float(row["target_equivalence_margin"]) for row in historical_rows
        ],
        "guards": guards,
        "adapter_authorized": adapter_authorized,
        "aggregate_analysis_executed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5106 sources exist"),
        *[(name, passed, str(passed)) for name, passed in guards.items()],
        ("adapter_authorized", adapter_authorized, canonical_digest(historical_rows)),
        ("adapter_lock_written", ADAPTER_LOCK.exists(), str(ADAPTER_LOCK)),
        ("failure_record_written", FAILURE_JSON.exists(), str(FAILURE_JSON)),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "schema repair is not evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5106_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5106 validation failed: {failed}")


if __name__ == "__main__":
    main()
