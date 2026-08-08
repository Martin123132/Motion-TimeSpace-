from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import inspect
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
DESIGN_LOCK = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_design_lock.json"
)
DESIGN_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_feasibility.json"
)
V12_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
CONFIG = V12_RUN / "config.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5111"
RUNS = SOURCE / "runs"
ACTIVATION_JSON = SOURCE / "E020_primary_control_extension_activation.json"
DRY_RUN_JSON = SOURCE / "E020_primary_control_extension_dry_run.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5111_VALIDATION.csv"
)
MARKER = "MTS_5111_E020_PRIMARY_CONTROL_EXTENSION_RUNNER"
REVISION = "restartable-separate-run-topology-reuse-v1"
DEFAULT_RUN_ID = "E020_primary_complex_control_extension_v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MAXIMUM_INVOCATION_HOURS = 4.0
EXPECTED_JOB_COUNT = 180


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5111", SCRIPT_5077)


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


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def validate_wall_cap(hours: float) -> None:
    if not 0.0 < hours <= MAXIMUM_INVOCATION_HOURS:
        raise ValueError(
            f"wall cap must be in (0,{MAXIMUM_INVOCATION_HOURS}] hours"
        )


def resumable(row: dict[str, Any], config_digest: str) -> bool:
    return (
        row.get("config_digest") == config_digest
        and row.get("status") == "COMPLETED_CONVERGED"
    )


def build_jobs(
    config: dict[str, Any], design_lock: dict[str, Any]
) -> list[dict[str, Any]]:
    events = {int(row["seed"]): row for row in config["events"]}
    base_ids = [str(row["argument_id"]) for row in config["base_arguments"]]
    rows: list[dict[str, Any]] = []
    for seed in [int(value) for value in design_lock["low_seeds"]]:
        event = events[seed]
        for base_id in base_ids:
            rows.append(
                {
                    "job_key": f"E020__{event['event_id']}__{base_id}__primary24",
                    "profile": "primary24",
                    "epsilon_id": "E020",
                    "event_id": str(event["event_id"]),
                    "base_argument_id": base_id,
                    "seed": seed,
                }
            )
    return rows


def source_topology_path(job: dict[str, Any]) -> Path:
    return (
        V12_RUN
        / "topologies"
        / f"{job['event_id']}__E040_{job['base_argument_id']}.json"
    )


def destination_topology_path(
    run_directory: Path, job: dict[str, Any]
) -> Path:
    return (
        run_directory
        / "topologies"
        / f"{job['event_id']}__E040_{job['base_argument_id']}.json"
    )


def validate_source_topologies(
    jobs: list[dict[str, Any]], config_digest: str
) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    seen: set[Path] = set()
    for job in jobs:
        path = source_topology_path(job)
        if path in seen:
            continue
        seen.add(path)
        if not path.exists():
            failures.append(f"missing:{path}")
            continue
        document = read_json(path)
        identity_valid = (
            document.get("config_digest") == config_digest
            and document.get("event_id") == job["event_id"]
            and document.get("argument_id")
            == f"E040_{job['base_argument_id']}"
            and bool(document.get("assignment_tracking_passed"))
        )
        reusable = identity_valid and bool(
            document.get("crossing_groups_consistent")
        )
        rows.append(
            {
                "path": str(path),
                "sha256": digest(path),
                "event_id": job["event_id"],
                "argument_id": f"E040_{job['base_argument_id']}",
                "identity_valid": identity_valid,
                "reusable": reusable,
                "reconstruction_required": identity_valid and not reusable,
            }
        )
        if not identity_valid:
            failures.append(f"invalid:{path}")
    return rows, failures


def validate_high_sources(
    config: dict[str, Any], design_lock: dict[str, Any]
) -> tuple[int, list[str]]:
    events = {int(row["seed"]): row for row in config["events"]}
    base_ids = [str(row["argument_id"]) for row in config["base_arguments"]]
    failures: list[str] = []
    count = 0
    for seed in [int(value) for value in design_lock["high_seeds"]]:
        event_id = str(events[seed]["event_id"])
        for epsilon_id in ("E020", "E040"):
            for base_id in base_ids:
                path = (
                    V12_RUN
                    / "jobs"
                    / f"{epsilon_id}__{event_id}__{base_id}__primary24.json"
                )
                if not path.exists():
                    failures.append(f"missing:{path}")
                    continue
                row = read_json(path)
                if not resumable(row, config["config_digest"]):
                    failures.append(f"not_converged:{path}")
                    continue
                count += 1
    return count, failures


def target_absence_in_v12(jobs: list[dict[str, Any]]) -> list[str]:
    return [
        str(V12_RUN / "jobs" / f"{job['job_key']}.json")
        for job in jobs
        if (V12_RUN / "jobs" / f"{job['job_key']}.json").exists()
    ]


def cache_contract_smoke(config_digest: str) -> dict[str, bool]:
    return {
        "accept_exact_converged": resumable(
            {
                "config_digest": config_digest,
                "status": "COMPLETED_CONVERGED",
            },
            config_digest,
        ),
        "reject_wrong_digest": not resumable(
            {
                "config_digest": "wrong",
                "status": "COMPLETED_CONVERGED",
            },
            config_digest,
        ),
        "reject_unconverged": not resumable(
            {
                "config_digest": config_digest,
                "status": "COMPLETED_UNCONVERGED",
            },
            config_digest,
        ),
        "reject_failed": not resumable(
            {"config_digest": config_digest, "status": "FAILED"},
            config_digest,
        ),
    }


def cap_contract_smoke() -> dict[str, bool]:
    result: dict[str, bool] = {}
    for name, value, expected in (
        ("accept_four", 4.0, True),
        ("accept_small_positive", 0.01, True),
        ("reject_zero", 0.0, False),
        ("reject_over_four", 4.000001, False),
    ):
        try:
            validate_wall_cap(value)
            accepted = True
        except ValueError:
            accepted = False
        result[name] = accepted == expected
    return result


def dry_run() -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    required = [SCRIPT_5077, DESIGN_LOCK, DESIGN_RESULT, CONFIG, FORMAL, V12_RUN]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    design_lock = read_json(DESIGN_LOCK)
    design_result = read_json(DESIGN_RESULT)
    config = read_json(CONFIG)
    jobs = build_jobs(config, design_lock)
    topology_rows, topology_failures = validate_source_topologies(
        jobs, config["config_digest"]
    )
    high_source_count, high_source_failures = validate_high_sources(
        config, design_lock
    )
    overlapping_targets = target_absence_in_v12(jobs)
    formal_digest = tree_digest(FORMAL)
    v12_digest = tree_digest(V12_RUN)
    cache_smoke = cache_contract_smoke(config["config_digest"])
    cap_smoke = cap_contract_smoke()
    execute_source = inspect.getsource(M5077.execute_kernel)
    upstream_resume_guard_present = all(
        needle in execute_source
        for needle in (
            'existing.get("config_digest") == config["config_digest"]',
            'existing.get("status") == "COMPLETED_CONVERGED"',
            '"resumed_from_cache": True',
        )
    )
    exact_scope = (
        len(jobs) == EXPECTED_JOB_COUNT
        and len({job["job_key"] for job in jobs}) == EXPECTED_JOB_COUNT
        and all(job["epsilon_id"] == "E020" for job in jobs)
        and all(job["profile"] == "primary24" for job in jobs)
        and len({job["seed"] for job in jobs}) == 12
        and len({job["base_argument_id"] for job in jobs}) == 15
    )
    source_result_hash_matches = (
        digest(DESIGN_RESULT) == design_lock["source_result_sha256"]
    )
    prerequisites = {
        "design_marker_correct": design_lock["checkpoint_marker"]
        == "MTS_5110_E020_PRIMARY_COMPLEX_CONTROL_DESIGN_LOCK",
        "design_result_hash_matches": source_result_hash_matches,
        "runner_implementation_authorized": bool(
            design_lock["runner_implementation_authorized"]
        ),
        "design_lock_did_not_pre_authorize_execution": not bool(
            design_lock["numerical_execution_authorized"]
        ),
        "fixed_complex_beta_is_one": float(design_lock["fixed_beta_real"])
        == 1.0
        and float(design_lock["fixed_beta_imaginary"]) == 1.0,
        "ratio_is_three": float(design_lock["low_to_high_ratio"]) == 3.0,
        "config_digest_matches": config["config_digest"]
        == design_lock["pilot_config_digest"],
        "exact_180_job_scope": exact_scope,
        "all_180_E040_source_topology_records_valid": len(topology_rows)
        == EXPECTED_JOB_COUNT
        and not topology_failures,
        "all_120_high_source_jobs_converged": high_source_count == 120
        and not high_source_failures,
        "extension_targets_absent_from_v12": not overlapping_targets,
        "cache_contract_passed": all(cache_smoke.values())
        and upstream_resume_guard_present,
        "four_hour_cap_contract_passed": all(cap_smoke.values()),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
        "design_is_not_independent_claim": not bool(
            design_lock["independent_efficiency_claim_allowed"]
        ),
        "claim_discipline": not bool(design_lock["valid_for_full_MTS_claim"]),
    }
    execution_authorized = all(prerequisites.values())
    activation = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "design_lock": str(DESIGN_LOCK),
        "design_lock_sha256": digest(DESIGN_LOCK),
        "design_result": str(DESIGN_RESULT),
        "design_result_sha256": digest(DESIGN_RESULT),
        "config": str(CONFIG),
        "config_sha256": digest(CONFIG),
        "config_digest": config["config_digest"],
        "expected_job_count": len(jobs),
        "expected_source_topology_count": len(topology_rows),
        "reusable_source_topology_count": sum(
            bool(row["reusable"]) for row in topology_rows
        ),
        "reconstructed_source_topology_count": sum(
            bool(row["reconstruction_required"]) for row in topology_rows
        ),
        "expected_high_source_job_count": high_source_count,
        "run_id": DEFAULT_RUN_ID,
        "run_directory": str(RUNS / DEFAULT_RUN_ID),
        "separate_from_v12": True,
        "v12_run_tree_sha256_before_execution": v12_digest,
        "formalization_workbench_tree_sha256": formal_digest,
        "maximum_invocation_wall_hours": MAXIMUM_INVOCATION_HOURS,
        "stop_on_first_failed_or_unconverged_job": True,
        "resume_completed_converged_jobs_only": True,
        "reuse_verified_E040_topologies_read_only": True,
        "prerequisites": prerequisites,
        "execution_authorized": execution_authorized,
        "default_enabled": False,
        "independent_efficiency_claim_allowed": False,
        "valid_for_full_MTS_claim": False,
    }
    dry = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "dry_run": True,
        "execution_started": False,
        "execution_authorized": execution_authorized,
        "expected_job_count": len(jobs),
        "unique_job_count": len({job["job_key"] for job in jobs}),
        "event_count": len({job["event_id"] for job in jobs}),
        "argument_count": len({job["base_argument_id"] for job in jobs}),
        "source_topology_failures": topology_failures,
        "high_source_failures": high_source_failures,
        "overlapping_v12_target_jobs": overlapping_targets,
        "cache_contract_smoke": cache_smoke,
        "cap_contract_smoke": cap_smoke,
        "upstream_resume_guard_present": upstream_resume_guard_present,
        "jobs": jobs,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(ACTIVATION_JSON, activation)
    atomic_json(DRY_RUN_JSON, dry)
    checks = [
        (name, passed, str(passed)) for name, passed in prerequisites.items()
    ]
    checks.extend(
        [
            (
                "execution_authorization_consistent",
                execution_authorized == all(prerequisites.values()),
                str(execution_authorized),
            ),
            ("default_off", not activation["default_enabled"], "explicit --mode run required"),
            ("dry_run_only", not dry["execution_started"], "no numerical job started"),
        ]
    )
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
                    "check_id": f"V5111_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5111 dry-run failed: {failed}")
    return activation, dry, jobs


def seed_topologies(
    run_directory: Path, jobs: list[dict[str, Any]], config_digest: str
) -> tuple[int, int]:
    copied = 0
    skipped_for_reconstruction = 0
    for job in jobs:
        source = source_topology_path(job)
        destination = destination_topology_path(run_directory, job)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source_document = read_json(source)
        if not bool(source_document.get("crossing_groups_consistent")):
            skipped_for_reconstruction += 1
            continue
        if destination.exists():
            document = read_json(destination)
            if (
                document.get("config_digest") != config_digest
                or document.get("event_id") != job["event_id"]
                or document.get("argument_id")
                != f"E040_{job['base_argument_id']}"
            ):
                raise RuntimeError(f"invalid existing topology cache: {destination}")
            continue
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
        copied += 1
    return copied, skipped_for_reconstruction


def run_counts(
    run_directory: Path, config_digest: str, jobs: list[dict[str, Any]]
) -> dict[str, int]:
    counts = {
        "completed_converged": 0,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 0,
    }
    for job in jobs:
        path = run_directory / "jobs" / f"{job['job_key']}.json"
        if not path.exists():
            counts["missing"] += 1
            continue
        row = read_json(path)
        if row.get("config_digest") != config_digest:
            counts["missing"] += 1
        elif row.get("status") == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        elif row.get("status") == "FAILED":
            counts["failed"] += 1
        else:
            counts["missing"] += 1
    return counts


def execute(
    activation: dict[str, Any],
    jobs: list[dict[str, Any]],
    run_id: str,
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not activation["execution_authorized"]:
        raise RuntimeError("5111 dry-run prerequisites did not authorize execution")
    validate_wall_cap(wall_cap_hours)
    config = read_json(CONFIG)
    if run_id != DEFAULT_RUN_ID:
        raise RuntimeError(f"locked run id is {DEFAULT_RUN_ID}")
    run_directory = RUNS / run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    config_path = run_directory / "config.json"
    if config_path.exists():
        existing = read_json(config_path)
        if existing.get("config_digest") != config["config_digest"]:
            raise RuntimeError("extension config changed; use no alternate run id")
    else:
        atomic_json(config_path, config)
    atomic_json(run_directory / "activation.json", activation)
    copied_topologies, reconstructed_topologies = seed_topologies(
        run_directory, jobs, config["config_digest"]
    )
    M5077.install_history_invariant_breakpoints(M5077.M5036.N5030)
    M5077.install_history_invariant_breakpoints(M5077.M5043.N5030)
    manager = M5077.CentralTopologyManager(run_directory, config)
    started = time.monotonic()
    newly_executed = 0
    resumed = 0
    state = "RUNNING"
    last_job_key: str | None = None
    blocking_job: dict[str, Any] | None = None
    for schedule_index, job in enumerate(jobs, start=1):
        if (time.monotonic() - started) / 3600.0 >= wall_cap_hours:
            state = "PAUSED_WALL_CAP"
            break
        row = M5077.execute_kernel(run_directory, config, manager, job)
        last_job_key = job["job_key"]
        if bool(row["resumed_from_cache"]):
            resumed += 1
        else:
            newly_executed += 1
        log_row = {
            "checkpoint_marker": MARKER,
            "schedule_index": schedule_index,
            "expected_job_count": len(jobs),
            "job_key": job["job_key"],
            "status": row["status"],
            "resumed_from_cache": bool(row["resumed_from_cache"]),
            "recorded_job_runtime_seconds": float(row["job_runtime_seconds"]),
            "invocation_elapsed_seconds": time.monotonic() - started,
        }
        append_jsonl(run_directory / "log.jsonl", log_row)
        counts = run_counts(run_directory, config["config_digest"], jobs)
        atomic_json(
            run_directory / "status.json",
            {
                **log_row,
                "revision": REVISION,
                "run_id": run_id,
                "state": "RUNNING",
                "newly_executed_this_invocation": newly_executed,
                "resumed_this_invocation": resumed,
                **counts,
                "valid_for_full_MTS_claim": False,
            },
        )
        print(json.dumps(log_row), flush=True)
        if row["status"] != "COMPLETED_CONVERGED":
            state = "BLOCKED_JOB_FAILURE"
            blocking_job = row
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            state = "PAUSED_JOB_CAP"
            break
    counts = run_counts(run_directory, config["config_digest"], jobs)
    if counts["completed_converged"] == len(jobs):
        state = "COMPLETE"
    v12_digest_after = tree_digest(V12_RUN)
    formal_digest_after = tree_digest(FORMAL)
    if v12_digest_after != activation["v12_run_tree_sha256_before_execution"]:
        raise RuntimeError("protected v12 run changed during 5111 execution")
    if formal_digest_after != FORMAL_BASELINE:
        raise RuntimeError("formalization-workbench changed during 5111 execution")
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "state": state,
        "expected_job_count": len(jobs),
        "newly_executed_this_invocation": newly_executed,
        "resumed_this_invocation": resumed,
        "seeded_E040_topology_count_this_invocation": copied_topologies,
        "E040_topologies_left_for_guarded_reconstruction": reconstructed_topologies,
        "last_job_key": last_job_key,
        "blocking_job": blocking_job,
        "invocation_elapsed_seconds": time.monotonic() - started,
        "wall_cap_hours": wall_cap_hours,
        "maximum_new_jobs": maximum_new_jobs,
        **counts,
        "control_matrix_complete": state == "COMPLETE",
        "statistical_analysis_complete": False,
        "independent_efficiency_claim_allowed": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(run_directory / "status.json", result)
    if state == "COMPLETE":
        atomic_json(run_directory / "COMPLETED.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run"), default="dry-run")
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    activation, dry, jobs = dry_run()
    if arguments.mode == "dry-run":
        result: dict[str, Any] = dry
    else:
        result = execute(
            activation,
            jobs,
            arguments.run_id,
            arguments.wall_cap_hours,
            arguments.maximum_new_jobs,
        )
    printable = (
        {key: value for key, value in result.items() if key != "jobs"}
        if arguments.mode == "dry-run"
        else result
    )
    print(json.dumps(printable, indent=2))


if __name__ == "__main__":
    main()
