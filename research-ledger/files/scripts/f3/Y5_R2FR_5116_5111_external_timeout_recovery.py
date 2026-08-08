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
SCRIPT_5111 = (
    POST
    / "scripts"
    / "Y5_R2FR_5111_E020_primary_control_extension_runner.py"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
CONFIG = RUN / "config.json"
DESIGN_LOCK = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_design_lock.json"
)
STATUS = RUN / "status.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5116"
RESULT_JSON = SOURCE / "5111_external_timeout_recovery.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5116_VALIDATION.csv"
)
MARKER = "MTS_5116_5111_EXTERNAL_TIMEOUT_RECOVERY"
REVISION = "durable-exact-digest-resume-reconciliation-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5111 = load_module("mts_5111_for_5116", SCRIPT_5111)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def main() -> None:
    config = M5111.read_json(CONFIG)
    design = M5111.read_json(DESIGN_LOCK)
    jobs = M5111.build_jobs(config, design)
    config_digest = str(config["config_digest"])
    durable: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    nonconverged: list[str] = []
    wrong_digest: list[str] = []
    missing: list[tuple[int, dict[str, Any]]] = []
    for index, job in enumerate(jobs, start=1):
        path = RUN / "jobs" / f"{job['job_key']}.json"
        if not path.exists():
            missing.append((index, job))
            continue
        row = M5111.read_json(path)
        if row.get("config_digest") != config_digest:
            wrong_digest.append(job["job_key"])
        elif row.get("status") == "COMPLETED_CONVERGED":
            durable.append((index, job, row))
        else:
            nonconverged.append(job["job_key"])
    durable_indices = [row[0] for row in durable]
    contiguous = durable_indices == list(range(1, len(durable_indices) + 1))
    last_index, last_job, _ = durable[-1]
    next_index, next_job = missing[0]
    next_job_path = RUN / "jobs" / f"{next_job['job_key']}.json"
    next_kernel_path = RUN / "kernels" / f"{next_job['job_key']}.json"
    formal_hash = M5111.tree_digest(FORMAL)
    counts = {
        "completed_converged": len(durable),
        "completed_unconverged": len(nonconverged),
        "failed": 0,
        "missing": len(missing),
    }
    recovered_status = {
        "checkpoint_marker": M5111.MARKER,
        "revision": M5111.REVISION,
        "run_id": M5111.DEFAULT_RUN_ID,
        "state": "PAUSED_EXTERNAL_TIMEOUT_RECOVERED",
        "expected_job_count": len(jobs),
        "last_job_key": last_job["job_key"],
        "last_schedule_index": last_index,
        "next_job_key": next_job["job_key"],
        "next_schedule_index": next_index,
        "external_timeout_recovery": {
            "checkpoint_marker": MARKER,
            "recovery_record": str(RESULT_JSON.resolve()),
            "interrupted_job_has_no_job_record": not next_job_path.exists(),
            "interrupted_job_has_no_kernel_record": not next_kernel_path.exists(),
            "resume_rule": "recompute the first missing job; accept only exact-digest COMPLETED_CONVERGED rows",
        },
        **counts,
        "control_matrix_complete": False,
        "statistical_analysis_complete": False,
        "independent_efficiency_claim_allowed": False,
        "valid_for_full_MTS_claim": False,
    }
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("exact_job_scope", len(jobs) == 180, str(len(jobs))),
        ("durable_prefix_is_contiguous", contiguous, str(last_index)),
        ("durable_converged_count_is_74", len(durable) == 74, str(len(durable))),
        ("no_nonconverged_records", not nonconverged, json.dumps(nonconverged)),
        ("no_wrong_digest_records", not wrong_digest, json.dumps(wrong_digest)),
        ("missing_count_is_106", len(missing) == 106, str(len(missing))),
        (
            "next_job_is_S507615_A14",
            next_job["job_key"] == "E020__S507615_N0000__A14__primary24",
            next_job["job_key"],
        ),
        (
            "interrupted_job_left_no_partial_outputs",
            not next_job_path.exists() and not next_kernel_path.exists(),
            f"job={next_job_path.exists()}; kernel={next_kernel_path.exists()}",
        ),
    ]
    passed = all(check[1] for check in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run": str(RUN.resolve()),
        "run_config_sha256": digest(CONFIG),
        "durable_completed_converged": len(durable),
        "missing": len(missing),
        "last_durable_job": last_job["job_key"],
        "last_durable_schedule_index": last_index,
        "next_job": next_job["job_key"],
        "next_schedule_index": next_index,
        "status_reconciled": passed,
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    if passed:
        atomic_json(STATUS, recovered_status)
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, check_passed, detail in checks:
            writer.writerow((name, str(bool(check_passed)).lower(), detail))
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
