from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5224"
RUN_DIRECTORY = SOURCE / "runs" / "replacement_scaled_controlled_v1"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5221 = (
    POST
    / "scripts"
    / "Y5_R2FR_5221_scaled_controlled_two_stratum_coefficient_run.py"
)
SCRIPT_5222 = (
    POST
    / "scripts"
    / "Y5_R2FR_5222_sequential_owned_direct_zero_classifier.py"
)
SCRIPT_5223 = (
    POST
    / "scripts"
    / "Y5_R2FR_5223_sequential_zero_failed_job_replay.py"
)
SOURCE_5221 = POST / "source-intake" / "functional_rg" / "5221"
SOURCE_5222 = POST / "source-intake" / "functional_rg" / "5222"
SOURCE_5223 = POST / "source-intake" / "functional_rg" / "5223"
MANIFEST_5221 = SOURCE_5221 / "frozen_scaled_controlled_manifest.json"
CONFIG_5221 = SOURCE_5221 / "frozen_scaled_controlled_config.json"
SCHEDULE_5221 = SOURCE_5221 / "frozen_scaled_controlled_schedule.csv"
LOCK_5221 = SOURCE_5221 / "frozen_scaled_controlled_protocol_lock.json"
RESULT_5221 = SOURCE_5221 / "scaled_controlled_two_stratum_results.json"
CLASSIFIER_AUDIT_5221 = (
    SOURCE_5221 / "general_grouped_classifier_runtime_audit.json"
)
RUN_5221 = SOURCE_5221 / "runs" / "scaled_controlled_two_stratum_v1"
GATE_5222 = SOURCE_5222 / "sequential_owned_direct_zero_classifier_gate.json"
RESULT_5222 = SOURCE_5222 / "sequential_owned_direct_zero_classifier.json"
RESULT_5223 = SOURCE_5223 / "sequential_zero_failed_job_replay.json"
RUN_5223 = SOURCE_5223 / "runs" / "sequential_zero_failed_job_replay"
TOPOLOGIES_5220 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5220"
    / "runs"
    / "fresh_grouped_classifier_A00_pilot_v1"
    / "topologies"
)

MANIFEST = SOURCE / "frozen_replacement_manifest.json"
FROZEN_CONFIG = SOURCE / "frozen_replacement_config.json"
FROZEN_SCHEDULE = SOURCE / "frozen_replacement_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_replacement_protocol_lock.json"
ACTIVATION = SOURCE / "replacement_activation.json"
MIGRATION = SOURCE / "converged_job_migration.json"
TOPOLOGY_MIGRATION = SOURCE / "topology_cache_migration.json"
RESULT = SOURCE / "replacement_scaled_controlled_results.json"
EVENT_ROWS = SOURCE / "replacement_event_rows.csv"
CONTROL_ROWS = SOURCE / "replacement_A00_control_rows.csv"
CLASSIFIER_AUDIT = SOURCE / "replacement_classifier_runtime_audit.json"
STATUS = RUN_DIRECTORY / "status.json"
RESUME = SOURCE / "RESUME.md"
DOCUMENT = POST / "5224-Y5-R2FR-replacement-scaled-controlled-run.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5224_VALIDATION.csv"

MARKER = "MTS_5224_REPLACEMENT_SCALED_CONTROLLED_RUN"
REVISION = "replacement-scaled-controlled-sequential-zero-v1"
RUN_ID = "replacement_scaled_controlled_v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MAXIMUM_WALL_HOURS = 4.0
TARGET_REPLAY_KEY = "TOP__E020__S522121_N0000__A03__primary24"
EXPECTED_5221_MIGRATED = 233
EXPECTED_5223_MIGRATED = 1
EXPECTED_TOTAL_MIGRATED = 234
RUNTIME_ROWS: list[dict[str, Any]] = []


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5221 = load_module(SCRIPT_5221, "mts_5221_for_5224")
M5222 = load_module(SCRIPT_5222, "mts_5222_for_5224")
M5223 = load_module(SCRIPT_5223, "mts_5223_for_5224")
M5220 = M5221.M5220
M5215 = M5221.M5215
M5212 = M5221.M5212


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
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
    os.replace(temporary, path)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5221,
        SCRIPT_5222,
        SCRIPT_5223,
        MANIFEST_5221,
        CONFIG_5221,
        SCHEDULE_5221,
        LOCK_5221,
        RESULT_5221,
        CLASSIFIER_AUDIT_5221,
        GATE_5222,
        RESULT_5222,
        RESULT_5223,
    )
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    return [
        {"path": relative(path), "sha256": digest(path)} for path in paths
    ]


def make_manifest() -> dict[str, Any]:
    source = read_json(MANIFEST_5221)
    result_5221 = read_json(RESULT_5221)
    gate_5222 = read_json(GATE_5222)
    result_5223 = read_json(RESULT_5223)
    if not (
        result_5221["state"] == "BLOCKED_JOB_FAILURE"
        and result_5221["counts"]["completed_converged"]
        == EXPECTED_5221_MIGRATED
        and result_5221["counts"]["completed_unconverged"] == 1
    ):
        raise RuntimeError("checkpoint-5221 source state changed")
    if not (
        gate_5222["passed"]
        and gate_5222["runtime_classifier_authorized"]
        and result_5223["passed"]
        and result_5223["replacement_scaled_run_authorized"]
    ):
        raise RuntimeError("5222/5223 did not authorize replacement")
    return {
        **source,
        "checkpoint": 5224,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_date": "2026-07-25",
        "design_source": relative(RESULT_5223),
        "locked_sources": source_rows(),
        "replacement_of_checkpoint": 5221,
        "replacement_reason": (
            "checkpoint-5221 stopped on an all-zero grouped direct residue "
            "that is now proven by the checkpoint-5222 sequential L32/L48/"
            "L64 classifier; checkpoint-5223 replay converged"
        ),
        "source_outcomes_known_at_lock": True,
        "new_replacement_outcomes_present_at_lock": False,
        "migration_rule": (
            "migrate only checkpoint-5221 COMPLETED_CONVERGED jobs for which "
            "the changed classifier was never invoked, plus the single "
            "checkpoint-5223 converged replay; preserve numerical payloads "
            "and source digests exactly"
        ),
        "expected_checkpoint_5221_migrated_jobs": EXPECTED_5221_MIGRATED,
        "expected_checkpoint_5223_migrated_jobs": EXPECTED_5223_MIGRATED,
        "expected_total_migrated_jobs": EXPECTED_TOTAL_MIGRATED,
        "sequential_zero_classifier": {
            "runner": relative(SCRIPT_5222),
            "runner_sha256": digest(SCRIPT_5222),
            "gate": relative(GATE_5222),
            "gate_sha256": digest(GATE_5222),
            "unresolved_action": "fail_closed",
        },
        "topology_cache_owner": relative(RUN_DIRECTORY),
        "allocation_changed": False,
        "acceptance_thresholds_changed": False,
        "threshold_retuning_after_outcomes_allowed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def make_config(manifest: dict[str, Any]) -> dict[str, Any]:
    config = read_json(CONFIG_5221)
    gate = read_json(GATE_5222)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["run_id"] = RUN_ID
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["sequential_zero_classifier"] = {
        "runner": str(SCRIPT_5222),
        "runner_sha256": digest(SCRIPT_5222),
        "gate": str(GATE_5222),
        "gate_sha256": digest(GATE_5222),
        "contract": gate["classifier_contract"],
        "unresolved_action": "fail_closed",
    }
    config["topology_cache_scope_correction"] = {
        "manager_run_directory": str(RUN_DIRECTORY),
        "source_checkpoint": 5221,
        "topology_generating_contract_unchanged": True,
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    for row in manifest["locked_sources"]:
        config["source_files"][str(ROOT / row["path"])] = row["sha256"]
    config.pop("config_digest", None)
    config["config_digest"] = M5215.canonical_digest(config)
    return config


def schedule_rows(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"schedule_index": index, **job}
        for index, job in enumerate(jobs, start=1)
    ]


def protocol_lock(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    if PROTOCOL_LOCK.exists():
        lock = read_json(PROTOCOL_LOCK)
        contract = lock["contract"]
        current = {
            "manifest_sha256": digest(MANIFEST),
            "config_sha256": digest(FROZEN_CONFIG),
            "schedule_sha256": digest(FROZEN_SCHEDULE),
            "runner_sha256": digest(Path(__file__).resolve()),
        }
        if any(contract[key] != value for key, value in current.items()):
            raise RuntimeError("checkpoint-5224 protocol digest changed")
        return lock
    outcome_files = [
        *RUN_DIRECTORY.glob("jobs/*.json"),
        *RUN_DIRECTORY.glob("topological-jobs/*.json"),
    ]
    if outcome_files:
        raise RuntimeError("replacement outcomes exist before protocol lock")
    lock = {
        "checkpoint": 5224,
        "checkpoint_marker": MARKER,
        "contract": {
            "manifest_sha256": digest(MANIFEST),
            "config_sha256": digest(FROZEN_CONFIG),
            "schedule_sha256": digest(FROZEN_SCHEDULE),
            "runner_sha256": digest(Path(__file__).resolve()),
            "source_5221_lock_sha256": digest(LOCK_5221),
            "gate_5222_sha256": digest(GATE_5222),
            "result_5223_sha256": digest(RESULT_5223),
            "expected_schedule_jobs": len(jobs),
            "expected_migrated_jobs": EXPECTED_TOTAL_MIGRATED,
            "allocation_changed": False,
            "acceptance_thresholds_changed": False,
        },
        "source_outcomes_known_at_lock": True,
        "new_replacement_outcomes_present_at_lock": False,
        "threshold_retuning_after_outcomes_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(PROTOCOL_LOCK, lock)
    return lock


def physics_job_digest(value: dict[str, Any]) -> str:
    ignored = {
        "checkpoint_marker",
        "revision",
        "owning_checkpoint_marker",
        "config_digest",
        "resumed_from_cache",
        "kernel_file",
        "topology_file",
        "migrated_from_checkpoint",
        "migration_source",
        "migration_source_sha256",
        "migration_physics_digest",
        "schedule_key",
        "stratum",
        "tranche_event_order",
        "valid_for_numeric_UV_claim",
        "valid_for_local_GR_claim",
        "valid_for_full_MTS_claim",
    }
    payload = {key: item for key, item in value.items() if key not in ignored}
    return M5215.canonical_digest(payload)


def copy_kernel(source: Path) -> Path:
    target = RUN_DIRECTORY / "migrated-kernels" / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if digest(target) != digest(source):
            raise RuntimeError(f"kernel collision at {target}")
    else:
        shutil.copy2(source, target)
    return target


def migrate_job(
    source_path: Path,
    source_row: dict[str, Any],
    job: dict[str, Any],
    config: dict[str, Any],
    source_checkpoint: int,
) -> dict[str, Any]:
    if source_row["status"] != "COMPLETED_CONVERGED":
        raise RuntimeError(f"refusing nonconverged migration {source_path}")
    migrated = dict(source_row)
    if migrated.get("kernel_file"):
        kernel_source = Path(migrated["kernel_file"])
        if not kernel_source.exists():
            raise FileNotFoundError(kernel_source)
        migrated["kernel_file"] = str(copy_kernel(kernel_source))
    topology_source = Path(migrated["topology_file"])
    if not topology_source.exists():
        raise FileNotFoundError(topology_source)
    topology_target = RUN_DIRECTORY / "topologies" / topology_source.name
    if not topology_target.exists():
        raise FileNotFoundError(
            f"topology migration must precede jobs: {topology_target}"
        )
    migrated["topology_file"] = str(topology_target)
    source_physics = physics_job_digest(source_row)
    migrated.update(
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "owning_checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **job,
            "resumed_from_cache": True,
            "migrated_from_checkpoint": source_checkpoint,
            "migration_source": str(source_path),
            "migration_source_sha256": digest(source_path),
            "migration_physics_digest": source_physics,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    if physics_job_digest(migrated) != source_physics:
        raise RuntimeError(f"job physics payload changed for {job['job_key']}")
    output = M5212.output_path(RUN_DIRECTORY, job)
    atomic_json(output, migrated)
    return {
        "job_key": job["job_key"],
        "source_checkpoint": source_checkpoint,
        "source": str(source_path),
        "source_sha256": digest(source_path),
        "target": str(output),
        "target_sha256": digest(output),
        "physics_digest": source_physics,
        "status": migrated["status"],
        "valid_for_numeric_UV_claim": False,
    }


def migrate_topologies(config: dict[str, Any]) -> dict[str, Any]:
    source_config = read_json(CONFIG_5221)
    source_contract = M5223.topology_config_contract(source_config)
    target_contract = M5223.topology_config_contract(config)
    if source_contract != target_contract:
        raise RuntimeError("topology-generating config contract changed")
    event_seeds = {
        int(row["seed"])
        for row in config["events"]
        if int(row["seed"]) <= 522121
    }
    candidates = [
        path
        for path in TOPOLOGIES_5220.glob("S*_N0000__*.json")
        if any(path.name.startswith(f"S{seed}_N0000__") for seed in event_seeds)
    ]
    if len(candidates) != 294:
        raise RuntimeError(f"expected 294 source topologies, got {len(candidates)}")
    target_directory = RUN_DIRECTORY / "topologies"
    target_directory.mkdir(parents=True, exist_ok=True)
    rows = []
    for source_path in sorted(candidates):
        source_document = read_json(source_path)
        physics_digest = M5223.topology_physics_digest(source_document)
        target_path = target_directory / source_path.name
        migrated = {
            **source_document,
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "config_digest": config["config_digest"],
            "topology_runtime_seconds": 0.0,
            "migrated_topology_cache": {
                "source": str(source_path),
                "source_sha256": digest(source_path),
                "physics_digest": physics_digest,
                "topology_config_contract_digest": target_contract,
            },
        }
        if target_path.exists():
            existing = read_json(target_path)
            if (
                M5223.topology_physics_digest(existing) != physics_digest
                or existing.get("config_digest") != config["config_digest"]
            ):
                raise RuntimeError(f"topology collision at {target_path}")
        else:
            atomic_json(target_path, migrated)
        rows.append(
            {
                "source": str(source_path),
                "target": str(target_path),
                "source_sha256": digest(source_path),
                "target_sha256": digest(target_path),
                "physics_digest": physics_digest,
            }
        )
    result = {
        "checkpoint": 5224,
        "topology_count": len(rows),
        "source_config_contract_digest": source_contract,
        "target_config_contract_digest": target_contract,
        "all_physics_payloads_match": all(
            M5223.topology_physics_digest(read_json(Path(row["source"])))
            == M5223.topology_physics_digest(read_json(Path(row["target"])))
            == row["physics_digest"]
            for row in rows
        ),
        "rows": rows,
        "source_files_deleted": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(TOPOLOGY_MIGRATION, result)
    return result


def migrate_jobs(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, Any]:
    classifier_audit = read_json(CLASSIFIER_AUDIT_5221)
    invoked_keys = {
        row.get("job_key") for row in classifier_audit["invocation_rows"]
    }
    if invoked_keys != {TARGET_REPLAY_KEY}:
        raise RuntimeError(f"unexpected 5221 classifier keys {invoked_keys}")
    jobs_by_key = {job["job_key"]: job for job in jobs}
    rows: list[dict[str, Any]] = []
    for job in jobs:
        source_path = M5212.output_path(RUN_5221, job)
        if not source_path.exists():
            continue
        source_row = read_json(source_path)
        if source_row.get("status") != "COMPLETED_CONVERGED":
            continue
        if job["job_key"] in invoked_keys:
            raise RuntimeError(
                "changed classifier was invoked in a purportedly unaffected job"
            )
        rows.append(
            migrate_job(source_path, source_row, job, config, 5221)
        )
    replay_path = (
        RUN_5223
        / "topological-jobs"
        / f"{TARGET_REPLAY_KEY}.json"
    )
    replay_row = read_json(replay_path)
    rows.append(
        migrate_job(
            replay_path,
            replay_row,
            jobs_by_key[TARGET_REPLAY_KEY],
            config,
            5223,
        )
    )
    count_5221 = sum(row["source_checkpoint"] == 5221 for row in rows)
    count_5223 = sum(row["source_checkpoint"] == 5223 for row in rows)
    if (
        count_5221 != EXPECTED_5221_MIGRATED
        or count_5223 != EXPECTED_5223_MIGRATED
        or len(rows) != EXPECTED_TOTAL_MIGRATED
    ):
        raise RuntimeError(
            f"unexpected migration counts {count_5221}, {count_5223}"
        )
    result = {
        "checkpoint": 5224,
        "checkpoint_5221_migrated_jobs": count_5221,
        "checkpoint_5223_migrated_jobs": count_5223,
        "total_migrated_jobs": len(rows),
        "changed_classifier_invocation_keys_5221": sorted(invoked_keys),
        "all_migrated_jobs_converged": all(
            row["status"] == "COMPLETED_CONVERGED" for row in rows
        ),
        "all_physics_payload_digests_reproduced": all(
            physics_job_digest(read_json(Path(row["target"])))
            == row["physics_digest"]
            for row in rows
        ),
        "rows": rows,
        "source_files_deleted": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(MIGRATION, result)
    return result


def copy_classifier_cache() -> None:
    CLASSIFIER_CACHE.mkdir(parents=True, exist_ok=True)
    for source_cache in (
        M5221.CLASSIFIER_CACHE,
        RUN_5223 / "grouped-classifier-cache",
    ):
        if not source_cache.exists():
            continue
        for source_path in source_cache.rglob("*.json"):
            target = CLASSIFIER_CACHE / source_path.relative_to(source_cache)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if digest(target) != digest(source_path):
                    raise RuntimeError(f"classifier cache collision {target}")
            else:
                shutil.copy2(source_path, target)


def prepare() -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, Any]
]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        manifest = make_manifest()
        atomic_json(MANIFEST, manifest)
    if FROZEN_CONFIG.exists():
        config = read_json(FROZEN_CONFIG)
    else:
        config = make_config(manifest)
        atomic_json(FROZEN_CONFIG, config)
    jobs = M5221.build_schedule(config, manifest)
    if len(jobs) != 520:
        raise RuntimeError(f"replacement schedule has {len(jobs)} jobs")
    if not FROZEN_SCHEDULE.exists():
        write_csv(FROZEN_SCHEDULE, schedule_rows(jobs))
    lock = protocol_lock(manifest, config, jobs)
    topology_migration = migrate_topologies(config)
    copy_classifier_cache()
    migration = migrate_jobs(config, jobs)
    activation = {
        "checkpoint": 5224,
        "checkpoint_marker": MARKER,
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "manifest_sha256": digest(MANIFEST),
        "config_sha256": digest(FROZEN_CONFIG),
        "schedule_sha256": digest(FROZEN_SCHEDULE),
        "source_outcomes_known_at_lock": True,
        "replacement_outcomes_present_at_lock": False,
        "migrated_job_count": migration["total_migrated_jobs"],
        "migrated_topology_count": topology_migration["topology_count"],
        "allocation_changed": False,
        "acceptance_thresholds_changed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(ACTIVATION, activation)
    if lock["contract"]["expected_migrated_jobs"] != migration[
        "total_migrated_jobs"
    ]:
        raise RuntimeError("migration count differs from lock")
    return manifest, config, jobs, activation


def sequential_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, stable = M5220.ORIGINAL_CATALOG(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    if stable:
        return catalog, stable
    event = M5212.M5077.CURRENT_EVENT
    argument = M5212.M5077.CURRENT_ARGUMENT
    job_key = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    if event is None or argument is None or job_key is None:
        return catalog, False
    repaired_rows = []
    for row in catalog:
        if bool(row["stable"]):
            repaired_rows.append(row)
            continue
        replacement, audit = (
            M5222.resolve_sequential_grouped_owned_direct_row(
                row,
                ownership,
                job_key,
                event,
                argument,
                CLASSIFIER_CACHE,
            )
        )
        RUNTIME_ROWS.append(audit)
        repaired_rows.append(replacement)
    return repaired_rows, all(bool(row["stable"]) for row in repaired_rows)


def install_runtime(config: dict[str, Any]) -> Any:
    M5220.RUN_DIRECTORY = RUN_DIRECTORY
    M5220.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5220.RUNTIME_CLASSIFIER_ROWS.clear()
    manager = M5220.install_runtime(config)
    M5212.certified_5212_catalog = sequential_catalog
    M5212.M5077.certified_primary_catalog = sequential_catalog
    return manager


def run_counts(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, int]:
    return M5212.run_counts(RUN_DIRECTORY, config, jobs)


def tranche_counts(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, dict[str, int]]:
    return {
        str(tranche): run_counts(
            config, [job for job in jobs if int(job["tranche"]) == tranche]
        )
        for tranche in (1, 2)
    }


def state_from_counts(
    counts: dict[str, int],
    by_tranche: dict[str, dict[str, int]],
    requested_tranche: str | None = None,
    paused: str | None = None,
) -> str:
    if counts["failed"] or counts["completed_unconverged"]:
        return "BLOCKED_JOB_FAILURE"
    if counts["completed_converged"] == 520:
        return "COMPLETE_DESIGN"
    if paused:
        return paused
    if (
        by_tranche["1"]["completed_converged"] == 260
        and requested_tranche == "1"
    ):
        return "TRANCHE_1_COMPLETE"
    return "FROZEN_REPLACEMENT_INCOMPLETE"


def configure_analysis_paths() -> None:
    M5221.RUN_DIRECTORY = RUN_DIRECTORY
    M5221.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5221.EVENT_ROWS = EVENT_ROWS
    M5221.CONTROL_ROWS = CONTROL_ROWS
    M5221.CLASSIFIER_AUDIT = CLASSIFIER_AUDIT
    M5220.RUNTIME_CLASSIFIER_ROWS.clear()
    M5220.RUNTIME_CLASSIFIER_ROWS.extend(RUNTIME_ROWS)


def analyse(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    configure_analysis_paths()
    analysis = M5221.analyse(state, manifest, config, jobs)
    analysis["replacement_checkpoint"] = 5224
    analysis["source_checkpoint_5221_preserved"] = True
    analysis["migration"] = {
        "job_migration": str(MIGRATION),
        "job_migration_sha256": digest(MIGRATION),
        "topology_migration": str(TOPOLOGY_MIGRATION),
        "topology_migration_sha256": digest(TOPOLOGY_MIGRATION),
    }
    analysis["sequential_zero_classifier_runtime_rows"] = len(RUNTIME_ROWS)
    analysis["valid_for_numeric_UV_claim"] = False
    analysis["valid_for_local_GR_claim"] = False
    analysis["valid_for_full_MTS_claim"] = False
    return analysis


def validation_rows(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    analysis: dict[str, Any],
) -> list[tuple[str, bool, str]]:
    counts = analysis["counts"]
    lock = read_json(PROTOCOL_LOCK)["contract"]
    migration = read_json(MIGRATION)
    topology = read_json(TOPOLOGY_MIGRATION)
    locked_sources_current = all(
        (ROOT / row["path"]).exists()
        and digest(ROOT / row["path"]) == row["sha256"]
        for row in manifest["locked_sources"]
    )
    return [
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
        (
            "replacement_protocol_matches_lock",
            digest(MANIFEST) == lock["manifest_sha256"]
            and digest(FROZEN_CONFIG) == lock["config_sha256"]
            and digest(FROZEN_SCHEDULE) == lock["schedule_sha256"]
            and digest(Path(__file__).resolve()) == lock["runner_sha256"],
            digest(PROTOCOL_LOCK),
        ),
        (
            "locked_sources_are_current",
            locked_sources_current,
            str(len(manifest["locked_sources"])),
        ),
        (
            "exactly_234_converged_jobs_migrated",
            migration["total_migrated_jobs"] == EXPECTED_TOTAL_MIGRATED
            and migration["all_migrated_jobs_converged"]
            and migration["all_physics_payload_digests_reproduced"],
            str(migration["total_migrated_jobs"]),
        ),
        (
            "changed_classifier_not_used_by_233_source_jobs",
            migration["changed_classifier_invocation_keys_5221"]
            == [TARGET_REPLAY_KEY],
            str(migration["changed_classifier_invocation_keys_5221"]),
        ),
        (
            "topology_migration_preserves_physics",
            topology["topology_count"] == 294
            and topology["all_physics_payloads_match"],
            str(topology["topology_count"]),
        ),
        (
            "no_failed_or_unconverged_replacement_jobs",
            counts["failed"] == 0
            and counts["completed_unconverged"] == 0,
            str(counts),
        ),
        (
            "completed_plus_missing_equals_schedule",
            counts["completed_converged"] + counts["missing"] == len(jobs),
            str(counts),
        ),
        (
            "complete_state_requires_520_jobs",
            state != "COMPLETE_DESIGN"
            or counts["completed_converged"] == 520,
            str(counts["completed_converged"]),
        ),
        (
            "allocation_and_thresholds_unchanged",
            not manifest["allocation_changed"]
            and not manifest["acceptance_thresholds_changed"]
            and not manifest["threshold_retuning_after_outcomes_allowed"],
            "unchanged",
        ),
        (
            "all_claim_flags_remain_false",
            not analysis["valid_for_numeric_UV_claim"]
            and not analysis["valid_for_local_GR_claim"]
            and not analysis["valid_for_full_MTS_claim"],
            "numeric UV, local GR and full MTS remain false",
        ),
    ]


def render_document(
    state: str, analysis: dict[str, Any], validations_passed: bool
) -> None:
    counts = analysis["counts"]
    pooled = analysis.get("pooled_estimate")
    lines = [
        "# 5224 - Replacement scaled controlled run",
        "",
        "## Protocol",
        "",
        "Checkpoint 5221 remains frozen as a failed run. This replacement",
        "keeps its seeds, allocation, estimator and acceptance thresholds,",
        "adds only the checkpoint-5222 sequential all-zero classifier, and",
        "corrects topology-cache ownership.",
        "",
        "Exactly 233 unaffected converged jobs are migrated from 5221. The",
        "changed classifier was invoked only in the failed job, which is",
        "instead migrated from the independently converged 5223 replay.",
        "Every migrated numerical payload and topology payload is checked",
        "by a metadata-independent digest.",
        "",
        "## Current state",
        "",
        f"- State: `{state}`.",
        f"- Converged jobs: `{counts['completed_converged']}/520`.",
        f"- Missing jobs: `{counts['missing']}`.",
        (
            "- Failed or unconverged jobs: "
            f"`{counts['failed'] + counts['completed_unconverged']}`."
        ),
        (
            "- Complete fresh events: "
            f"`{analysis['fresh_complete_full_events']}/2` full and "
            f"`{analysis['fresh_complete_topological_events']}/24` "
            "topological."
        ),
        f"- Decision: `{analysis['decision']}`.",
        f"- Validation passed: `{validations_passed}`.",
        "",
        "## Estimate",
        "",
    ]
    if pooled is None:
        lines.append("No compatibility-gated pooled estimate is available.")
    else:
        candidate = pooled["candidate_K_mu"]
        value = candidate["value"]
        lines.extend(
            [
                (
                    f"- Provisional pooled `K_mu={value['real']:.10g}"
                    f"{value['imaginary']:+.10g} i`."
                ),
                (
                    "- Real/imaginary SE: "
                    f"`{candidate['real_standard_error']:.8g}` / "
                    f"`{candidate['imaginary_standard_error']:.8g}`."
                ),
                (
                    "- Tail/precision gates: "
                    f"`{pooled['controlled_real_tail_gate']}` / "
                    f"`{pooled['coefficient_precision_gate']}`."
                ),
            ]
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This replacement can close only the crossed-hhh coefficient",
            "statistic. Numeric UV, local GR and full MTS remain unclaimed.",
            "",
            "## Evidence",
            "",
            f"- Protocol lock: `{PROTOCOL_LOCK}`",
            f"- Job migration: `{MIGRATION}`",
            f"- Topology migration: `{TOPOLOGY_MIGRATION}`",
            f"- Result: `{RESULT}`",
            f"- Validation: `{VALIDATION}`",
            f"- Resume: `{RESUME}`",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def finalize(
    state: str,
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    analysis = analyse(state, manifest, config, jobs)
    validations = validation_rows(
        state, manifest, config, jobs, analysis
    )
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    validation_passed = all(row[1] for row in validations)
    result = {
        "checkpoint": 5224,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "state": state,
        "counts": analysis["counts"],
        "analysis": analysis,
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "migration_sha256": digest(MIGRATION),
        "topology_migration_sha256": digest(TOPOLOGY_MIGRATION),
        "validation_all_passed": validation_passed,
        "validation_check_count": len(validations),
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    render_document(state, analysis, validation_passed)
    by_tranche = analysis["tranche_counts"]
    atomic_text(
        RESUME,
        "\n".join(
            [
                "# Checkpoint 5224 resume",
                "",
                f"- State: `{state}`.",
                (
                    "- Counts: "
                    f"`{analysis['counts']['completed_converged']}/520` "
                    "converged."
                ),
                (
                    "- Tranche 1 missing: "
                    f"`{by_tranche['1']['missing']}` jobs."
                ),
                (
                    "- Tranche 2 missing: "
                    f"`{by_tranche['2']['missing']}` jobs."
                ),
                "- Resume tranche 1:",
                (
                    f"  `{sys.executable} {Path(__file__).resolve()} "
                    "--mode run --tranche 1 --wall-cap-hours 4`"
                ),
                "- Resume tranche 2:",
                (
                    f"  `{sys.executable} {Path(__file__).resolve()} "
                    "--mode run --tranche 2 --wall-cap-hours 4`"
                ),
                "",
            ]
        ),
    )
    atomic_json(
        STATUS,
        {
            "checkpoint": 5224,
            "state": state,
            "counts": analysis["counts"],
            "tranche_counts": by_tranche,
            "decision": analysis["decision"],
            "updated_unix_time": time.time(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def execute(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    requested_tranche: str,
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must be in (0, 4] hours")
    selected = (
        {1, 2}
        if requested_tranche == "all"
        else {int(requested_tranche)}
    )
    selected_jobs = [
        job for job in jobs if int(job["tranche"]) in selected
    ]
    manager = install_runtime(config)
    started = time.monotonic()
    newly_executed = 0
    paused: str | None = None
    for index, job in enumerate(selected_jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            paused = "PAUSED_WALL_CAP"
            break
        cached = M5212.cached_result(RUN_DIRECTORY, config, job)
        if (
            job["stratum"] == "topological"
            and job["base_argument_id"] == "A00"
        ):
            row = M5215.execute_job(
                RUN_DIRECTORY, config, manager, job
            )
        else:
            row = M5212.execute_job(
                RUN_DIRECTORY, config, manager, job
            )
        if cached is None:
            newly_executed += 1
        row = {
            **row,
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "owning_checkpoint_marker": MARKER,
            "tranche": job["tranche"],
            "sequential_zero_classifier_predeclared": True,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(M5212.output_path(RUN_DIRECTORY, job), row)
        counts = run_counts(config, jobs)
        by_tranche = tranche_counts(config, jobs)
        atomic_json(
            STATUS,
            {
                "checkpoint": 5224,
                "state": "RUNNING",
                "requested_tranche": requested_tranche,
                "current_schedule_index": index,
                "current_schedule_key": job["schedule_key"],
                "last_job_status": row["status"],
                "counts": counts,
                "tranche_counts": by_tranche,
                "elapsed_seconds": time.monotonic() - started,
                "updated_unix_time": time.time(),
            },
        )
        print(
            json.dumps(
                {
                    "schedule_index": index,
                    "schedule_key": job["schedule_key"],
                    "status": row["status"],
                    "resumed_from_cache": bool(
                        row.get("resumed_from_cache")
                    ),
                    "elapsed_seconds": time.monotonic() - started,
                    "counts": counts,
                }
            ),
            flush=True,
        )
        if row["status"] != "COMPLETED_CONVERGED":
            paused = "BLOCKED_JOB_FAILURE"
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            paused = "PAUSED_JOB_CAP"
            break
    counts = run_counts(config, jobs)
    by_tranche = tranche_counts(config, jobs)
    state = state_from_counts(
        counts,
        by_tranche,
        requested_tranche=requested_tranche,
        paused=paused,
    )
    return finalize(state, manifest, config, jobs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("prepare", "run", "analyse"), default="prepare"
    )
    parser.add_argument(
        "--tranche", choices=("1", "2", "all"), default="1"
    )
    parser.add_argument(
        "--wall-cap-hours", type=float, default=MAXIMUM_WALL_HOURS
    )
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    manifest, config, jobs, activation = prepare()
    if arguments.mode == "prepare":
        counts = run_counts(config, jobs)
        state = state_from_counts(counts, tranche_counts(config, jobs))
        result = finalize(state, manifest, config, jobs)
        print(
            json.dumps(
                {
                    "prepared": True,
                    "activation": activation,
                    "state": result["state"],
                    "counts": result["counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if arguments.mode == "analyse":
        counts = run_counts(config, jobs)
        state = state_from_counts(counts, tranche_counts(config, jobs))
        finalize(state, manifest, config, jobs)
        return
    execute(
        manifest,
        config,
        jobs,
        arguments.tranche,
        arguments.wall_cap_hours,
        arguments.maximum_new_jobs,
    )


if __name__ == "__main__":
    main()
