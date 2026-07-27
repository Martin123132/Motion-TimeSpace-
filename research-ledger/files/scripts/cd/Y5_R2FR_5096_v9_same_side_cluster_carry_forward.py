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
SCRIPT_5079 = POST / "scripts" / "Y5_R2FR_5079_bounded_central_anchor_pilot_runner.py"
SOURCE_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v8"
)
TARGET_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v9"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5096"
RESULT_JSON = SOURCE / "v9_same_side_cluster_carry_forward_result.json"
MANIFEST_JSON = SOURCE / "v9_same_side_cluster_carry_forward_manifest.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5096_VALIDATION.csv"
)
MARKER = "MTS_5096_V9_SAME_SIDE_CLUSTER_CARRY_FORWARD"
REVISION = "job-scoped-same-side-cluster-cycle-carry-forward-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
SOURCE_DIGEST = "06df9ddc2bcfb27e4bfd8c302c069ddc4776165207cd11d9cce79449fda9a033"
TARGET_DIGEST = "adf27b2fe3dde8a8e93ff80de6802d4be2fdcbfbab1f1b8539327629b398e30d"
TARGET_JOB = "E040__S507615_N0000__A14__coarse12"
ALLOWED_CONFIG_DELTAS = {
    "config_digest",
    "run_id",
    "same_side_global_cluster_cycle_policy",
    "schema_revision",
    "source_files",
}


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def transformed_record(
    source_path: Path,
    target_path: Path,
    replacements: dict[str, str] | None = None,
) -> dict[str, Any]:
    value = json.loads(source_path.read_text(encoding="utf-8"))
    if value.get("config_digest") != SOURCE_DIGEST:
        raise RuntimeError(f"source digest mismatch: {source_path}")
    value["config_digest"] = TARGET_DIGEST
    for field, replacement in (replacements or {}).items():
        value[field] = replacement
    value["5096_carry_forward"] = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_path": str(source_path),
        "source_sha256": digest(source_path),
        "source_config_digest": SOURCE_DIGEST,
        "target_config_digest": TARGET_DIGEST,
        "reason": (
            f"5095 clustered-cycle activation is job-scoped to {TARGET_JOB}; "
            "this converged record is outside that scope"
        ),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(target_path, value)
    return {
        "source_path": str(source_path),
        "source_sha256": digest(source_path),
        "target_path": str(target_path),
        "target_sha256": digest(target_path),
    }


def main() -> None:
    required = [SCRIPT_5079, SOURCE_RUN / "config.json", SOURCE_RUN / "status.json", FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5096 inputs: {missing}")
    module_5079 = load_module("mts_5079_for_5096", SCRIPT_5079)
    manifest = module_5079.read_json(module_5079.MANIFEST)
    source_config = json.loads((SOURCE_RUN / "config.json").read_text(encoding="utf-8"))
    source_status = json.loads((SOURCE_RUN / "status.json").read_text(encoding="utf-8"))
    target_config = module_5079.M5077.make_config(
        manifest, "bounded_central_anchor_pilot_v9"
    )
    jobs = module_5079.M5077.pilot_jobs(target_config, manifest)
    activation = module_5079.activation_record(manifest, target_config, jobs)
    changed_fields = sorted(
        key
        for key in set(source_config) | set(target_config)
        if source_config.get(key) != target_config.get(key)
    )
    contract_delta_valid = bool(
        set(changed_fields) == ALLOWED_CONFIG_DELTAS
        and source_config["config_digest"] == SOURCE_DIGEST
        and target_config["config_digest"] == TARGET_DIGEST
        and source_status["completed_converged"] == 254
        and source_status["completed_unconverged"] == 1
        and source_status["failed"] == 0
        and source_status["blocking_job"]["job_key"] == TARGET_JOB
        and target_config["same_side_global_cluster_cycle_policy"]["job_scopes"]
        == [TARGET_JOB]
    )
    if not contract_delta_valid:
        raise RuntimeError(f"5096 contract delta rejected: {changed_fields}")
    source_jobs = []
    for source_path in sorted((SOURCE_RUN / "jobs").glob("*.json")):
        row = json.loads(source_path.read_text(encoding="utf-8"))
        if row.get("status") == "COMPLETED_CONVERGED":
            source_jobs.append((source_path, row))
    if len(source_jobs) != 254 or any(
        row["job_key"] == TARGET_JOB for _, row in source_jobs
    ):
        raise RuntimeError("5096 source converged set is not the expected 254 unaffected jobs")
    TARGET_RUN.mkdir(parents=True, exist_ok=True)
    atomic_json(TARGET_RUN / "config.json", target_config)
    atomic_json(TARGET_RUN / "activation.json", activation)
    topology_manifest: dict[str, dict[str, Any]] = {}
    kernel_manifest = []
    job_manifest = []
    for source_job_path, source_job in source_jobs:
        source_topology = Path(source_job["topology_file"])
        target_topology = TARGET_RUN / "topologies" / source_topology.name
        if source_topology.name not in topology_manifest:
            topology_manifest[source_topology.name] = transformed_record(
                source_topology,
                target_topology,
            )
        source_kernel = Path(source_job["kernel_file"])
        target_kernel = TARGET_RUN / "kernels" / source_kernel.name
        kernel_manifest.append(
            transformed_record(
                source_kernel,
                target_kernel,
                {"topology_file": str(target_topology)},
            )
        )
        target_job = TARGET_RUN / "jobs" / source_job_path.name
        job_manifest.append(
            transformed_record(
                source_job_path,
                target_job,
                {
                    "topology_file": str(target_topology),
                    "kernel_file": str(target_kernel),
                },
            )
        )
    status = {
        "checkpoint_marker": module_5079.MARKER,
        "revision": module_5079.REVISION,
        "run_id": "bounded_central_anchor_pilot_v9",
        "state": "PAUSED_CERTIFIED_CARRY_FORWARD",
        "expected_job_count": 360,
        "completed_converged": 254,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 106,
        "last_job_key": source_jobs[-1][1]["job_key"],
        "blocking_job": None,
        "pilot_numerical_matrix_complete": False,
        "statistical_analysis_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(TARGET_RUN / "status.json", status)
    carry_manifest = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_run": str(SOURCE_RUN),
        "target_run": str(TARGET_RUN),
        "changed_config_fields": changed_fields,
        "source_config_digest": SOURCE_DIGEST,
        "target_config_digest": TARGET_DIGEST,
        "targeted_uncarried_job": TARGET_JOB,
        "carried_job_count": len(job_manifest),
        "carried_kernel_count": len(kernel_manifest),
        "carried_topology_count": len(topology_manifest),
        "jobs": job_manifest,
        "kernels": kernel_manifest,
        "topologies": list(topology_manifest.values()),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, carry_manifest)
    formal_digest = tree_digest(FORMAL)
    target_jobs = sorted((TARGET_RUN / "jobs").glob("*.json"))
    target_kernels = sorted((TARGET_RUN / "kernels").glob("*.json"))
    target_topologies = sorted((TARGET_RUN / "topologies").glob("*.json"))
    target_records_valid = all(
        json.loads(path.read_text(encoding="utf-8")).get("config_digest")
        == TARGET_DIGEST
        for path in target_jobs + target_kernels + target_topologies
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "contract_delta_valid": contract_delta_valid,
        "changed_config_fields": changed_fields,
        "source_completed_converged": source_status["completed_converged"],
        "source_blocking_job": source_status["blocking_job"],
        "target_completed_converged": len(target_jobs),
        "target_failed": 0,
        "target_missing": 360 - len(target_jobs),
        "carried_topology_count": len(target_topologies),
        "target_records_valid": target_records_valid,
        "manifest_path": str(MANIFEST_JSON),
        "manifest_sha256": digest(MANIFEST_JSON),
        "next_job": TARGET_JOB,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5096 sources exist"),
        ("contract_delta_exact", contract_delta_valid, str(changed_fields)),
        (
            "source_failure_excluded",
            not (TARGET_RUN / "jobs" / f"{TARGET_JOB}.json").exists(),
            TARGET_JOB,
        ),
        (
            "carried_counts",
            len(target_jobs) == 254 and len(target_kernels) == 254,
            f"jobs={len(target_jobs)}; kernels={len(target_kernels)}",
        ),
        ("target_records_valid", target_records_valid, TARGET_DIGEST),
        (
            "schedule_unchanged",
            activation["schedule_digest"]
            == "da19db9b4d7f5c1ca41babe2f1fcfafc2f9ed92a043cc4298f1fb5c4bee3f956",
            activation["schedule_digest"],
        ),
        (
            "cluster_scope_exact",
            target_config["same_side_global_cluster_cycle_policy"]["job_scopes"]
            == [TARGET_JOB],
            str(target_config["same_side_global_cluster_cycle_policy"]["job_scopes"]),
        ),
        (
            "activation_authorized",
            activation["pilot_execution_authorized"],
            str(activation["prerequisites"]),
        ),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "carry-forward is not physical evidence",
        ),
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
                    "check_id": f"V5096_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5096 validation failed: {failed}")


if __name__ == "__main__":
    main()
