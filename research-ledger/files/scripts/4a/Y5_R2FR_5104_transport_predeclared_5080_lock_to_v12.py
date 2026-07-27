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
SCRIPT_5105 = POST / "scripts" / "Y5_R2FR_5105_execute_predeclared_5080_analysis_v12.py"
PREDECLARED_LOCK = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_lock_v6.json"
TARGET_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v12"
TARGET_LOCK = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_lock_v12.json"
TARGET_OUTPUTS = (
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_v12.json",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_channels_v12.csv",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_event_costs_v12.csv",
    POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_jackknife_v12.csv",
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5080_V12_VALIDATION.csv",
)
SOURCE = POST / "source-intake" / "functional_rg" / "5104"
RESULT_JSON = SOURCE / "predeclared_5080_lock_v12_transport.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5104_VALIDATION.csv"
MARKER = "MTS_5104_TRANSPORT_PREDECLARED_5080_LOCK_TO_V12"
REVISION = "analysis-semantics-preserving-run-binding-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
TARGET_CONFIG_DIGEST = "bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69"
TARGET_SCHEDULE_DIGEST = "da19db9b4d7f5c1ca41babe2f1fcfafc2f9ed92a043cc4298f1fb5c4bee3f956"
SEMANTIC_FIELDS = (
    "expected_job_count",
    "high_seeds",
    "low_seeds",
    "high_units",
    "low_units",
    "high_observable",
    "paired_low_observable",
    "independent_low_observable",
    "projector",
    "fixed_control",
    "estimator",
    "variance_estimator",
    "primary_decision_metric",
    "primary_decision_threshold",
    "runtime_cap_hours",
    "decision_rule",
    "delete_one_high_and_low_panels",
    "target_central_values_used",
    "valid_for_full_MTS_claim",
)


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
        SCRIPT_5105,
        PREDECLARED_LOCK,
        TARGET_RUN / "config.json",
        TARGET_RUN / "status.json",
        TARGET_RUN / "COMPLETED.json",
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    aggregate_outputs_absent = all(not path.exists() for path in TARGET_OUTPUTS)
    if not aggregate_outputs_absent:
        raise RuntimeError("v12 aggregate outputs already exist; lock transport is not pre-analysis")
    if TARGET_LOCK.exists():
        raise RuntimeError("v12 analysis lock already exists")
    module = load_module("mts_5080_for_5104", SCRIPT_5080)
    predeclared = read_json(PREDECLARED_LOCK)
    target_config = read_json(TARGET_RUN / "config.json")
    target_status = read_json(TARGET_RUN / "status.json")
    target_completion = read_json(TARGET_RUN / "COMPLETED.json")
    module.PILOT_RUN = TARGET_RUN
    candidate = module.analysis_lock()
    semantic_mismatches = [
        field
        for field in SEMANTIC_FIELDS
        if predeclared.get(field) != candidate.get(field)
    ]
    formal_digest = tree_digest(FORMAL)
    guards = {
        "predeclared_script_hash_intact": predeclared.get("analysis_script_sha256")
        == digest(SCRIPT_5080),
        "candidate_uses_same_analysis_script": candidate.get("analysis_script_sha256")
        == predeclared.get("analysis_script_sha256"),
        "analysis_semantics_unchanged": not semantic_mismatches,
        "target_config_exact": target_config.get("config_digest")
        == TARGET_CONFIG_DIGEST
        == candidate.get("pilot_config_digest"),
        "target_schedule_exact": candidate.get("pilot_schedule_digest")
        == TARGET_SCHEDULE_DIGEST
        == predeclared.get("pilot_schedule_digest"),
        "target_matrix_complete_before_analysis": target_status.get("state")
        == "COMPLETE"
        and target_status.get("completed_converged") == 360
        and target_completion.get("completed_converged") == 360,
        "aggregate_outputs_absent_before_transport": aggregate_outputs_absent,
        "target_central_values_remain_excluded": not bool(
            candidate.get("target_central_values_used")
        ),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    transport_authorized = all(guards.values())
    candidate.update(
        {
            "binding_checkpoint_marker": MARKER,
            "binding_revision": REVISION,
            "predeclared_lock_path": str(PREDECLARED_LOCK),
            "predeclared_lock_sha256": digest(PREDECLARED_LOCK),
            "execution_wrapper_path": str(SCRIPT_5105),
            "execution_wrapper_sha256": digest(SCRIPT_5105),
            "aggregate_output_paths": [str(path) for path in TARGET_OUTPUTS],
            "analysis_semantic_fields_compared": list(SEMANTIC_FIELDS),
            "analysis_semantic_mismatches": semantic_mismatches,
            "analysis_contract_predeclared_before_aggregate_analysis": True,
            "matrix_complete_when_binding_transported": True,
            "aggregate_outputs_absent_before_transport": aggregate_outputs_absent,
            "transport_authorized": transport_authorized,
        }
    )
    if transport_authorized:
        atomic_json(TARGET_LOCK, candidate)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "predeclared_lock": str(PREDECLARED_LOCK),
        "predeclared_lock_sha256": digest(PREDECLARED_LOCK),
        "target_lock": str(TARGET_LOCK),
        "target_lock_sha256": digest(TARGET_LOCK) if TARGET_LOCK.exists() else None,
        "target_run": str(TARGET_RUN),
        "target_config_digest": target_config.get("config_digest"),
        "target_schedule_digest": candidate.get("pilot_schedule_digest"),
        "analysis_script_sha256": digest(SCRIPT_5080),
        "execution_wrapper_sha256": digest(SCRIPT_5105),
        "semantic_mismatches": semantic_mismatches,
        "guards": guards,
        "transport_authorized": transport_authorized,
        "aggregate_analysis_executed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5104 sources exist"),
        *[(name, passed, str(passed)) for name, passed in guards.items()],
        ("transport_authorized", transport_authorized, str(semantic_mismatches)),
        ("target_lock_written", TARGET_LOCK.exists(), str(TARGET_LOCK)),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "lock transport is not evidence"),
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
                    "check_id": f"V5104_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5104 validation failed: {failed}")


if __name__ == "__main__":
    main()
