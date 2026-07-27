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
SOURCE_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v11"
TARGET_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v12"
SOURCE = POST / "source-intake" / "functional_rg" / "5102"
RESULT_JSON = SOURCE / "v12_argument_independent_projective_carry_forward_result.json"
MANIFEST_JSON = SOURCE / "v12_argument_independent_projective_carry_forward_manifest.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5102_VALIDATION.csv"
MARKER = "MTS_5102_V12_ARGUMENT_INDEPENDENT_PROJECTIVE_CARRY_FORWARD"
REVISION = "exact-A14-projective-theorem-carry-forward-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
SOURCE_DIGEST = "31f1640f4c0927462f69ec2e28b909b9942b485e5d3705b800eb9a5d00b7b0e2"
TARGET_DIGEST = "bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69"
TARGET_JOB = "E040__S507622_N0000__A14__coarse12"
EXPECTED_CARRIED_JOBS = 359
ALLOWED_CONFIG_DELTAS = {
    "argument_independent_projective_cluster_zero_policy",
    "config_digest",
    "run_id",
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


def transform(
    source: Path,
    target: Path,
    replacements: dict[str, str] | None = None,
) -> tuple[str, str]:
    value = json.loads(source.read_text(encoding="utf-8"))
    if value.get("config_digest") != SOURCE_DIGEST:
        raise RuntimeError(f"source digest mismatch: {source}")
    source_hash = digest(source)
    value["config_digest"] = TARGET_DIGEST
    for field, replacement in (replacements or {}).items():
        value[field] = replacement
    value["5102_carry_forward"] = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_path": str(source),
        "source_sha256": source_hash,
        "source_config_digest": SOURCE_DIGEST,
        "target_config_digest": TARGET_DIGEST,
        "targeted_uncarried_job": TARGET_JOB,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(target, value)
    return source_hash, digest(target)


def main() -> None:
    required = [
        SCRIPT_5079,
        SOURCE_RUN / "config.json",
        SOURCE_RUN / "status.json",
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    if (TARGET_RUN / "jobs").exists() and any((TARGET_RUN / "jobs").glob("*.json")):
        raise RuntimeError("5102 target already contains jobs")
    module = load_module("mts_5079_for_5102", SCRIPT_5079)
    manifest = module.read_json(module.MANIFEST)
    source_config = json.loads((SOURCE_RUN / "config.json").read_text(encoding="utf-8"))
    source_status = json.loads((SOURCE_RUN / "status.json").read_text(encoding="utf-8"))
    target_config = module.M5077.make_config(manifest, "bounded_central_anchor_pilot_v12")
    jobs = module.M5077.pilot_jobs(target_config, manifest)
    activation = module.activation_record(manifest, target_config, jobs)
    changed_fields = sorted(
        key
        for key in set(source_config) | set(target_config)
        if source_config.get(key) != target_config.get(key)
    )
    contract_valid = bool(
        set(changed_fields) == ALLOWED_CONFIG_DELTAS
        and source_config["config_digest"] == SOURCE_DIGEST
        and target_config["config_digest"] == TARGET_DIGEST
        and source_status["completed_converged"] == EXPECTED_CARRIED_JOBS
        and source_status["completed_unconverged"] == 1
        and source_status["failed"] == 0
        and source_status["blocking_job"]["job_key"] == TARGET_JOB
        and target_config["argument_independent_projective_cluster_zero_policy"][
            "job_scopes"
        ]
        == [TARGET_JOB]
        and activation["pilot_execution_authorized"]
    )
    if not contract_valid:
        raise RuntimeError(f"5102 contract rejected: {changed_fields}")
    source_jobs: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((SOURCE_RUN / "jobs").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        if row.get("status") == "COMPLETED_CONVERGED":
            source_jobs.append((path, row))
    if len(source_jobs) != EXPECTED_CARRIED_JOBS:
        raise RuntimeError("5102 converged source count changed")
    if any(row["job_key"] == TARGET_JOB for _, row in source_jobs):
        raise RuntimeError("5102 target job is unexpectedly converged in source")
    TARGET_RUN.mkdir(parents=True, exist_ok=True)
    atomic_json(TARGET_RUN / "config.json", target_config)
    atomic_json(TARGET_RUN / "activation.json", activation)
    aggregate = hashlib.sha256()
    topology_names: set[str] = set()
    for source_job_path, source_job in source_jobs:
        topology_name = Path(source_job["topology_file"]).name
        source_topology = SOURCE_RUN / "topologies" / topology_name
        target_topology = TARGET_RUN / "topologies" / topology_name
        if topology_name not in topology_names:
            hashes = transform(source_topology, target_topology)
            aggregate.update("".join(hashes).encode("ascii"))
            topology_names.add(topology_name)
        source_kernel = SOURCE_RUN / "kernels" / Path(source_job["kernel_file"]).name
        target_kernel = TARGET_RUN / "kernels" / source_kernel.name
        hashes = transform(
            source_kernel,
            target_kernel,
            {"topology_file": str(target_topology)},
        )
        aggregate.update("".join(hashes).encode("ascii"))
        target_job = TARGET_RUN / "jobs" / source_job_path.name
        hashes = transform(
            source_job_path,
            target_job,
            {
                "topology_file": str(target_topology),
                "kernel_file": str(target_kernel),
            },
        )
        aggregate.update("".join(hashes).encode("ascii"))
    status = {
        "checkpoint_marker": module.MARKER,
        "revision": module.REVISION,
        "run_id": "bounded_central_anchor_pilot_v12",
        "state": "PAUSED_CERTIFIED_CARRY_FORWARD",
        "expected_job_count": 360,
        "completed_converged": EXPECTED_CARRIED_JOBS,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 360 - EXPECTED_CARRIED_JOBS,
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
        "carried_job_count": len(source_jobs),
        "carried_kernel_count": len(source_jobs),
        "carried_topology_count": len(topology_names),
        "aggregate_transformation_sha256": aggregate.hexdigest(),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, carry_manifest)
    formal_digest = tree_digest(FORMAL)
    target_jobs = list((TARGET_RUN / "jobs").glob("*.json"))
    target_kernels = list((TARGET_RUN / "kernels").glob("*.json"))
    target_topologies = list((TARGET_RUN / "topologies").glob("*.json"))
    records_valid = all(
        json.loads(path.read_text(encoding="utf-8")).get("config_digest")
        == TARGET_DIGEST
        for path in target_jobs + target_kernels + target_topologies
    )
    result = {
        **carry_manifest,
        "contract_delta_valid": contract_valid,
        "target_records_valid": records_valid,
        "target_missing": status["missing"],
        "next_job": TARGET_JOB,
        "formalization_workbench_tree_sha256": formal_digest,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5102 sources exist"),
        ("contract_exact", contract_valid, str(changed_fields)),
        ("carried_jobs", len(target_jobs) == EXPECTED_CARRIED_JOBS, str(len(target_jobs))),
        ("target_excluded", not (TARGET_RUN / "jobs" / f"{TARGET_JOB}.json").exists(), TARGET_JOB),
        ("records_valid", records_valid, f"jobs={len(target_jobs)} kernels={len(target_kernels)} topologies={len(target_topologies)}"),
        ("activation_authorized", activation["pilot_execution_authorized"], str(activation["pilot_execution_authorized"])),
        ("status_counts", status["completed_converged"] + status["missing"] == 360, str(status)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "carry-forward is not evidence"),
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
                    "check_id": f"V5102_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5102 validation failed: {failed}")


if __name__ == "__main__":
    main()
