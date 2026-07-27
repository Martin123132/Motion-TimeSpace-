from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5080 = POST / "scripts" / "Y5_R2FR_5080_locked_fresh_pilot_analysis.py"
PILOT_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v12"
CONFIG_JSON = PILOT_RUN / "config.json"
LOCK_JSON = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_lock_v12_margin_adapter.json"
HISTORICAL_CONFIG = POST / "source-intake" / "functional_rg" / "5040" / "runs" / "nested_sobol_power1_s4_v1" / "config.json"
ANALYSIS_JSON = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_v12.json"
CHANNEL_CSV = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_channels_v12.csv"
EVENT_CSV = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_event_costs_v12.csv"
JACKKNIFE_CSV = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_jackknife_v12.csv"
ANALYSIS_VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5080_V12_VALIDATION.csv"
SOURCE = POST / "source-intake" / "functional_rg" / "5107"
RESULT_JSON = SOURCE / "predeclared_5080_v12_margin_adapter_execution.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5107_VALIDATION.csv"
MARKER = "MTS_5107_EXECUTE_5080_V12_WITH_MARGIN_ADAPTER"
REVISION = "one-shot-historical-budget-schema-adapter-execution-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
OUTPUTS = (ANALYSIS_JSON, CHANNEL_CSV, EVENT_CSV, JACKKNIFE_CSV, ANALYSIS_VALIDATION_CSV)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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


def main() -> None:
    required = [
        SCRIPT_5080,
        LOCK_JSON,
        HISTORICAL_CONFIG,
        CONFIG_JSON,
        PILOT_RUN / "COMPLETED.json",
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    if any(path.exists() for path in OUTPUTS):
        raise RuntimeError("v12 aggregate output already exists; one-shot execution refused")
    lock = read_json(LOCK_JSON)
    historical_config = read_json(HISTORICAL_CONFIG)
    budget_rows = historical_config["target_precision_budgets"]
    adapter = lock.get("margin_schema_adapter", {})
    wrapper_hash = digest(Path(__file__).resolve())
    preflight = {
        "adapter_authorized": bool(lock.get("schema_adapter_authorized")),
        "wrapper_hash_locked": lock.get("execution_wrapper_sha256") == wrapper_hash,
        "analysis_script_hash_locked": lock.get("analysis_script_sha256")
        == digest(SCRIPT_5080),
        "historical_config_hash_locked": adapter.get("historical_config_sha256")
        == digest(HISTORICAL_CONFIG),
        "historical_rows_hash_locked": adapter.get("historical_rows_sha256")
        == canonical_digest(budget_rows),
        "budget_rows_are_five_nonclaim_rows": len(budget_rows) == 5
        and all(not bool(row.get("valid_for_full_MTS_claim")) for row in budget_rows),
        "aggregate_outputs_were_absent_at_lock": bool(
            lock.get("aggregate_outputs_absent_before_adapter_lock")
        ),
        "target_values_excluded": not bool(lock.get("target_central_values_used")),
    }
    if not all(preflight.values()):
        raise RuntimeError(f"5107 preflight rejected: {preflight}")
    module = load_module("mts_5080_for_5107", SCRIPT_5080)
    original_read_json = module.read_json

    def read_json_with_budget_adapter(path: Path) -> dict[str, Any]:
        value = original_read_json(path)
        if Path(path).resolve() == CONFIG_JSON.resolve():
            if "target_precision_budgets" in value:
                raise RuntimeError("pilot config unexpectedly gained precision budgets")
            value = dict(value)
            value["target_precision_budgets"] = budget_rows
        return value

    module.PILOT_RUN = PILOT_RUN
    module.LOCK_JSON = LOCK_JSON
    module.RESULT_JSON = ANALYSIS_JSON
    module.CHANNEL_CSV = CHANNEL_CSV
    module.EVENT_CSV = EVENT_CSV
    module.JACKKNIFE_CSV = JACKKNIFE_CSV
    module.VALIDATION_CSV = ANALYSIS_VALIDATION_CSV
    module.read_json = read_json_with_budget_adapter
    analysis = module.analyze(lock)
    with ANALYSIS_VALIDATION_CSV.open(newline="", encoding="utf-8") as handle:
        analysis_checks = list(csv.DictReader(handle))
    formal_digest = tree_digest(FORMAL)
    guards = {
        **preflight,
        "all_outputs_written": all(path.exists() for path in OUTPUTS),
        "analysis_validation_passed": all(
            row["passed"].lower() == "true" for row in analysis_checks
        ),
        "matrix_complete": bool(analysis.get("pilot_matrix_complete")),
        "fixed_control_unchanged": analysis.get("fixed_control_real") == 1.0
        and analysis.get("fixed_control_imaginary") == 0.0
        and not bool(analysis.get("fresh_data_used_to_fit_control")),
        "target_values_not_used": not bool(analysis.get("target_central_values_used")),
        "decision_is_predeclared_branch": analysis.get("decision")
        in ("LOCKED_FRESH_PILOT_PASSES", "LOCKED_FRESH_PILOT_DOES_NOT_PASS"),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    execution_valid = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "analysis_lock": str(LOCK_JSON),
        "analysis_lock_sha256": digest(LOCK_JSON),
        "analysis_result": str(ANALYSIS_JSON),
        "analysis_result_sha256": digest(ANALYSIS_JSON),
        "analysis_script_sha256": digest(SCRIPT_5080),
        "execution_wrapper_sha256": wrapper_hash,
        "margin_rows_sha256": canonical_digest(budget_rows),
        "analysis_validation_check_count": len(analysis_checks),
        "realized_cost_normalized_score_ratio": analysis.get(
            "realized_cost_normalized_score_ratio"
        ),
        "predeclared_efficiency_threshold": analysis.get(
            "predeclared_efficiency_threshold"
        ),
        "direct_recorded_job_runtime_hours": analysis.get(
            "direct_recorded_job_runtime_hours"
        ),
        "locked_numerical_efficiency_gate_passed": analysis.get(
            "locked_numerical_efficiency_gate_passed"
        ),
        "decision": analysis.get("decision"),
        "maximum_delete_one_shift_in_full_standard_errors": analysis.get(
            "maximum_delete_one_shift_in_full_standard_errors"
        ),
        "guards": guards,
        "execution_valid": execution_valid,
        "formalization_workbench_tree_sha256": formal_digest,
        "result_scope": "predeclared fresh numerical estimator efficiency only",
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5107 sources exist"),
        *[(name, passed, str(passed)) for name, passed in guards.items()],
        ("execution_valid", execution_valid, str(analysis.get("decision"))),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], result["result_scope"]),
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
                    "check_id": f"V5107_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5107 validation failed: {failed}")


if __name__ == "__main__":
    main()
