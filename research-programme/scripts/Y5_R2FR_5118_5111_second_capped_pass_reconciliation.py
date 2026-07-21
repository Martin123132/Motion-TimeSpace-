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
SCRIPT_5111 = POST / "scripts" / "Y5_R2FR_5111_E020_primary_control_extension_runner.py"
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
CLUSTER_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5117"
    / "E020_S507615_A14_same_side_cluster_cycle_certificate.json"
)
CLUSTER_JOB_KEY = "E020__S507615_N0000__A14__primary24"
SOURCE = POST / "source-intake" / "functional_rg" / "5118"
RESULT_JSON = SOURCE / "5111_second_capped_pass_reconciliation.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5118_VALIDATION.csv"
)
MARKER = "MTS_5118_5111_SECOND_CAPPED_PASS_RECONCILIATION"
REVISION = "durable-prefix-after-derived-cluster-repair-v1"
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


M5111 = load_module("mts_5111_for_5118", SCRIPT_5111)


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
    status = M5111.read_json(STATUS)
    cluster_gate = M5111.read_json(CLUSTER_GATE)
    jobs = M5111.build_jobs(config, design)
    config_digest = str(config["config_digest"])
    durable: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    nonconverged: list[str] = []
    failed: list[str] = []
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
        elif row.get("status") == "FAILED":
            failed.append(job["job_key"])
        else:
            nonconverged.append(job["job_key"])
    durable_indices = [row[0] for row in durable]
    contiguous = durable_indices == list(range(1, len(durable_indices) + 1))
    last_index, last_job, _ = durable[-1]
    next_index, next_job = missing[0]
    cluster_job = M5111.read_json(RUN / "jobs" / f"{CLUSTER_JOB_KEY}.json")
    cluster_kernel = M5111.read_json(RUN / "kernels" / f"{CLUSTER_JOB_KEY}.json")
    cluster_audit = cluster_kernel["profile_audit"]["same_side_cluster_cycle_audit"]
    formal_hash = M5111.tree_digest(FORMAL)
    cache_directories = list((POST / "scripts").glob("__pycache__"))
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("exact_job_scope", len(jobs) == 180, str(len(jobs))),
        ("durable_prefix_is_contiguous", contiguous, str(last_index)),
        ("durable_converged_count_is_126", len(durable) == 126, str(len(durable))),
        ("no_nonconverged_records", not nonconverged, json.dumps(nonconverged)),
        ("no_failed_records", not failed, json.dumps(failed)),
        ("no_wrong_digest_records", not wrong_digest, json.dumps(wrong_digest)),
        ("missing_count_is_54", len(missing) == 54, str(len(missing))),
        (
            "next_job_is_S507619_A06",
            next_job["job_key"] == "E020__S507619_N0000__A06__primary24",
            next_job["job_key"],
        ),
        (
            "clean_wall_cap_pause",
            status["state"] == "PAUSED_WALL_CAP",
            str(status["state"]),
        ),
        (
            "5117_cluster_gate_passed",
            cluster_gate["same_side_cluster_cycle_certificate_passed"]
            and cluster_gate["production_integration_authorized"],
            str(cluster_gate["cross_node_relative_residual"]),
        ),
        (
            "A14_replay_converged_with_cluster",
            cluster_job["status"] == "COMPLETED_CONVERGED"
            and cluster_audit is not None
            and int(cluster_audit["cluster_count"]) > 0,
            f"status={cluster_job['status']}; clusters={cluster_audit['cluster_count']}",
        ),
        ("no_python_cache", not cache_directories, json.dumps([str(p) for p in cache_directories])),
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
        "run_state": status["state"],
        "A14_cluster_gate": str(CLUSTER_GATE.resolve()),
        "A14_cluster_gate_sha256": digest(CLUSTER_GATE),
        "A14_cluster_count": int(cluster_audit["cluster_count"]),
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "statistical_analysis_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
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
