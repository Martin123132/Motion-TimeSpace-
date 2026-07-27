from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
MANIFEST = POST / "source-intake" / "functional_rg" / "5076" / "locked_central_anchor_pilot_manifest.json"
SENSITIVITY = POST / "source-intake" / "functional_rg" / "5076" / "central_anchor_delete_one_sensitivity.json"
RUNNER_GATE = POST / "source-intake" / "functional_rg" / "5077" / "central_anchor_pilot_runner_gate.json"
TOPOLOGY_SMOKE = POST / "source-intake" / "functional_rg" / "5078" / "fresh_central_anchor_topology_cost_smoke.json"
RESOLUTION_GATE = POST / "source-intake" / "functional_rg" / "5081" / "fresh_projective_resolution_extension_gate.json"
LOCAL_ZERO_CERTIFICATE = POST / "source-intake" / "functional_rg" / "5083" / "owned_g2_local_cauchy_zero_certificate.json"
RECOIL_THEOREM_GATE = POST / "source-intake" / "functional_rg" / "5084" / "recoil_source_local_cauchy_theorem.json"
REMOVABLE_EXTENSION_GATE = POST / "source-intake" / "functional_rg" / "5085" / "same_source_global_collision_removable_extension.json"
OUTWARD_CONTOUR_GATE = POST / "source-intake" / "functional_rg" / "5086" / "outward_same_source_residue_contour_gate.json"
DOUBLE_ZERO_COLLISION_GATE = POST / "source-intake" / "functional_rg" / "5088" / "exact_same_source_double_zero_collision_certificate.json"
DOUBLE_ZERO_RUNNER_INTEGRATION = POST / "source-intake" / "functional_rg" / "5089" / "exact_double_zero_runner_integration_smoke.json"
MULTI_DOUBLE_ZERO_COLLISION_GATE = POST / "source-intake" / "functional_rg" / "5091" / "E040_A11_coarse_multi_double_zero_certificate.json"
SAME_SIDE_CLUSTER_CYCLE_GATE = POST / "source-intake" / "functional_rg" / "5095" / "same_side_global_cluster_cycle_certificate.json"
PROJECTIVE_CLUSTER_ZERO_GATE = POST / "source-intake" / "functional_rg" / "5097" / "E040_S507622_A00_projective_cross_source_cluster_zero.json"
CONTINUOUS_SUBMINIMUM_CYCLE_GATE = POST / "source-intake" / "functional_rg" / "5099" / "E040_S507622_A10_continuous_subminimum_cycle_certificate.json"
ARGUMENT_INDEPENDENT_PROJECTIVE_GATE = POST / "source-intake" / "functional_rg" / "5101" / "S507622_projective_cluster_argument_independence.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5079"
RUNS = SOURCE / "runs"
ACTIVATION_JSON = SOURCE / "bounded_central_anchor_pilot_activation.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5079_VALIDATION.csv"
MARKER = "MTS_5079_BOUNDED_CENTRAL_ANCHOR_PILOT_RUNNER"
REVISION = "guarded-argument-independent-projective-pilot-v12"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
MAXIMUM_ALLOWED_WALL_HOURS = 10.0


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5079", SCRIPT_5077)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def activation_record(
    manifest: dict[str, Any], config: dict[str, Any], jobs: list[dict[str, Any]]
) -> dict[str, Any]:
    sensitivity = read_json(SENSITIVITY)
    runner = read_json(RUNNER_GATE)
    topology = read_json(TOPOLOGY_SMOKE)
    resolution = read_json(RESOLUTION_GATE)
    local_zero = read_json(LOCAL_ZERO_CERTIFICATE)
    recoil_theorem = read_json(RECOIL_THEOREM_GATE)
    removable_extension = read_json(REMOVABLE_EXTENSION_GATE)
    outward_contour = read_json(OUTWARD_CONTOUR_GATE)
    double_zero_collision = read_json(DOUBLE_ZERO_COLLISION_GATE)
    double_zero_integration = read_json(DOUBLE_ZERO_RUNNER_INTEGRATION)
    multi_double_zero_collision = read_json(MULTI_DOUBLE_ZERO_COLLISION_GATE)
    same_side_cluster_cycle = read_json(SAME_SIDE_CLUSTER_CYCLE_GATE)
    projective_cluster_zero = read_json(PROJECTIVE_CLUSTER_ZERO_GATE)
    continuous_subminimum_cycle = read_json(CONTINUOUS_SUBMINIMUM_CYCLE_GATE)
    argument_independent_projective = read_json(
        ARGUMENT_INDEPENDENT_PROJECTIVE_GATE
    )
    projected_hours = float(
        sensitivity["robust_joint_statistical_cost_allocation"][
            "maximum_runtime_hours"
        ]
    )
    prerequisites = {
        "statistical_design_locked": bool(manifest["statistical_design_locked"]),
        "manifest_execution_cap_is_ten_hours": float(
            manifest["execution_cap_hours"]
        )
        == MAXIMUM_ALLOWED_WALL_HOURS,
        "runner_integration_complete": bool(
            runner["runner_integration_complete"]
        ),
        "runner_resume_contract_exercised": bool(
            runner["resume_contract_exercised"]
        ),
        "fresh_topology_structure_passed": bool(
            topology["fresh_topology_structure_passed"]
        ),
        "fresh_topology_resume_exercised": bool(
            topology["resume_contract_exercised"]
        ),
        "fresh_topology_cost_envelope_supported": bool(
            topology["historical_topology_cost_envelope_supported"]
        ),
        "projective_resolution_extension_supported": bool(
            resolution["production_resolution_extension_supported"]
        ),
        "event_local_g2_zero_certificate_accepted": bool(
            local_zero["accepted_local_zero_certificate"]
        ),
        "local_certificate_does_not_claim_family_theorem": not bool(
            local_zero["general_g2_family_theorem_claimed"]
        ),
        "guarded_recoil_cauchy_theorem_accepted": bool(
            recoil_theorem["corrected_recoil_theorem_accepted"]
        ),
        "guarded_recoil_theorem_excludes_broad_5041_scope": not bool(
            recoil_theorem["broad_5041_theorem_reinstated"]
        ),
        "same_source_removable_extension_accepted": bool(
            removable_extension[
                "same_source_collision_removable_extension_accepted"
            ]
        ),
        "failed_A11_recomputed_with_extension": bool(
            removable_extension["failed_A11_gate_converged"]
        ),
        "outward_same_source_contour_gate_accepted": bool(
            outward_contour["outward_same_source_contour_gate_accepted"]
        ),
        "failed_A12_recomputed_with_outward_contours": bool(
            outward_contour["recomputed_gate_converged"]
            and outward_contour["recomputed_gate_all_residues_stable"]
        ),
        "exact_double_zero_collision_certificate_accepted": bool(
            double_zero_collision["double_zero_certificate_passed"]
            and double_zero_collision["exact_collision_gate_accepted"]
        ),
        "exact_double_zero_runner_integration_accepted": bool(
            double_zero_integration["runner_exact_guard_integration_accepted"]
            and double_zero_integration["pilot_resume_authorized"]
        ),
        "multi_double_zero_collision_certificate_accepted": bool(
            multi_double_zero_collision["all_exact_collision_roots_certified"]
            and multi_double_zero_collision["exact_collision_gate_accepted"]
            and multi_double_zero_collision["runner_integration_authorized"]
        ),
        "same_side_cluster_cycle_certificate_accepted": bool(
            same_side_cluster_cycle[
                "same_side_cluster_cycle_certificate_passed"
            ]
        ),
        "same_side_cluster_cycle_scope_is_exact": config[
            "same_side_global_cluster_cycle_policy"
        ]["job_scopes"]
        == [M5077.SAME_SIDE_CLUSTER_JOB_KEY],
        "projective_cluster_zero_certificate_accepted": bool(
            projective_cluster_zero["projective_cluster_zero_certificate_passed"]
            and projective_cluster_zero["runner_integration_authorized"]
        ),
        "projective_cluster_zero_scope_is_exact": config[
            "projective_cross_source_cluster_zero_policy"
        ]["job_scopes"]
        == [M5077.PROJECTIVE_CLUSTER_ZERO_JOB_KEY],
        "projective_cluster_zero_does_not_enable_broad_theorem": not bool(
            config["projective_cross_source_cluster_zero_policy"][
                "broad_cross_source_theorem_allowed"
            ]
        ),
        "argument_independent_projective_zero_accepted": bool(
            argument_independent_projective[
                "argument_independent_projective_cluster_zero_passed"
            ]
            and argument_independent_projective["runner_integration_authorized"]
        ),
        "argument_independent_projective_scope_is_exact": config[
            "argument_independent_projective_cluster_zero_policy"
        ]["job_scopes"]
        == [M5077.ARGUMENT_INDEPENDENT_PROJECTIVE_JOB_KEY],
        "argument_independent_projective_does_not_enable_broad_theorem": not bool(
            config["argument_independent_projective_cluster_zero_policy"][
                "broad_cross_source_theorem_allowed"
            ]
        ),
        "continuous_subminimum_cycle_certificate_accepted": bool(
            continuous_subminimum_cycle[
                "continuous_subminimum_cycle_certificate_passed"
            ]
            and continuous_subminimum_cycle["runner_integration_authorized"]
        ),
        "continuous_subminimum_cycle_scope_is_exact": config[
            "continuous_subminimum_global_cycle_policy"
        ]["job_scopes"]
        == [M5077.CONTINUOUS_SUBMINIMUM_CYCLE_JOB_KEY],
        "exact_guards_are_narrowly_scoped": config[
            "exact_double_zero_global_collision_policy"
        ]["job_scopes"]
        == [M5077.DOUBLE_ZERO_JOB_KEY, M5077.MULTI_DOUBLE_ZERO_JOB_KEY],
        "broad_5041_theorem_disabled": not bool(
            config["residue_certificate_policy"]["broad_5041_theorem_allowed"]
        ),
        "coarse_theorem_scope_is_restricted": config[
            "residue_certificate_policy"
        ]["coarse_theorem_scope"]
        == "5084_guarded_owned_direct_g1_g2",
        "uncertified_topology_falls_back_to_full_homotopy": config[
            "uncertified_topology_action"
        ]
        == "full_homotopy_fallback",
        "projected_delete_one_runtime_within_cap": projected_hours
        <= MAXIMUM_ALLOWED_WALL_HOURS,
        "job_matrix_complete": len(jobs) == 360,
    }
    authorized = all(prerequisites.values())
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "config_digest": config["config_digest"],
        "schedule_digest": M5077.M5036.canonical_digest(jobs),
        "expected_job_count": len(jobs),
        "expected_primary24_job_count": sum(
            job["profile"] == "primary24" for job in jobs
        ),
        "expected_coarse12_job_count": sum(
            job["profile"] == "coarse12" for job in jobs
        ),
        "high_unit_count": int(manifest["high_units"]),
        "low_unit_count": int(manifest["low_units"]),
        "projected_maximum_delete_one_runtime_hours": projected_hours,
        "declared_wall_cap_hours": MAXIMUM_ALLOWED_WALL_HOURS,
        "projected_wall_margin_hours": MAXIMUM_ALLOWED_WALL_HOURS
        - projected_hours,
        "prerequisites": prerequisites,
        "pilot_execution_authorized": authorized,
        "authorization_scope": "run the locked numerical pilot only",
        "default_enabled": False,
        "stop_on_first_failed_or_unconverged_job": True,
        "resume_completed_converged_jobs": True,
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }


def write_validation(activation: dict[str, Any]) -> None:
    prerequisites = activation["prerequisites"]
    checks = [
        (
            "source_paths_exist",
            all(
                path.exists()
                for path in (
                    SCRIPT_5077,
                    MANIFEST,
                    SENSITIVITY,
                    RUNNER_GATE,
                    TOPOLOGY_SMOKE,
                    RESOLUTION_GATE,
                    LOCAL_ZERO_CERTIFICATE,
                    RECOIL_THEOREM_GATE,
                    REMOVABLE_EXTENSION_GATE,
                    OUTWARD_CONTOUR_GATE,
                    DOUBLE_ZERO_COLLISION_GATE,
                    DOUBLE_ZERO_RUNNER_INTEGRATION,
                    MULTI_DOUBLE_ZERO_COLLISION_GATE,
                    SAME_SIDE_CLUSTER_CYCLE_GATE,
                    PROJECTIVE_CLUSTER_ZERO_GATE,
                    CONTINUOUS_SUBMINIMUM_CYCLE_GATE,
                    ARGUMENT_INDEPENDENT_PROJECTIVE_GATE,
                )
            ),
            "all activation sources exist",
        ),
        (
            "prerequisites_complete",
            all(prerequisites.values()),
            "; ".join(f"{key}={value}" for key, value in prerequisites.items()),
        ),
        (
            "job_counts",
            activation["expected_job_count"] == 360
            and activation["expected_primary24_job_count"] == 120
            and activation["expected_coarse12_job_count"] == 240,
            f"total={activation['expected_job_count']}; primary={activation['expected_primary24_job_count']}; coarse={activation['expected_coarse12_job_count']}",
        ),
        (
            "runtime_margin_positive",
            activation["projected_wall_margin_hours"] > 0.0,
            f"margin_h={activation['projected_wall_margin_hours']}",
        ),
        (
            "authorization_consistent",
            activation["pilot_execution_authorized"]
            == all(prerequisites.values()),
            f"authorized={activation['pilot_execution_authorized']}",
        ),
        (
            "default_off",
            not activation["default_enabled"],
            "execution requires explicit --mode run",
        ),
        (
            "stop_and_resume_contract",
            activation["stop_on_first_failed_or_unconverged_job"]
            and activation["resume_completed_converged_jobs"],
            "fail closed and resume only completed converged jobs",
        ),
        (
            "formalization_unchanged",
            activation["formalization_workbench_tree_sha256"]
            == FORMAL_BASELINE,
            activation["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not activation["valid_for_full_MTS_claim"],
            "execution authorization is not MTS evidence",
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
                    "check_id": f"V5079_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5079 validation failed: {failed}")


def run_counts(
    run_directory: Path, config: dict[str, Any], jobs: list[dict[str, Any]]
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
        if row.get("config_digest") != config["config_digest"]:
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
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    run_id: str,
    wall_cap_hours: float,
    maximum_new_jobs: int,
) -> dict[str, Any]:
    if not activation["pilot_execution_authorized"]:
        raise RuntimeError("pilot prerequisites are not complete")
    if not (0.0 < wall_cap_hours <= MAXIMUM_ALLOWED_WALL_HOURS):
        raise RuntimeError("wall cap must be positive and no greater than ten hours")
    run_directory = RUNS / run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    config_path = run_directory / "config.json"
    if config_path.exists():
        existing = read_json(config_path)
        if existing["config_digest"] != config["config_digest"]:
            raise RuntimeError("pilot config changed; use a new run id")
    else:
        atomic_json(config_path, config)
    atomic_json(run_directory / "activation.json", activation)
    M5077.install_history_invariant_breakpoints(M5077.M5036.N5030)
    M5077.install_history_invariant_breakpoints(M5077.M5043.N5030)
    manager = M5077.CentralTopologyManager(run_directory, config)
    log_path = run_directory / "log.jsonl"
    started = time.monotonic()
    newly_executed = 0
    resumed = 0
    invocation_state = "RUNNING"
    last_job_key: str | None = None
    blocking_job: dict[str, Any] | None = None
    for index, job in enumerate(jobs, start=1):
        elapsed_hours = (time.monotonic() - started) / 3600.0
        if elapsed_hours >= wall_cap_hours:
            invocation_state = "PAUSED_WALL_CAP"
            break
        row = M5077.execute_kernel(run_directory, config, manager, job)
        last_job_key = job["job_key"]
        was_resumed = bool(row["resumed_from_cache"])
        if was_resumed:
            resumed += 1
        else:
            newly_executed += 1
        log_row = {
            "checkpoint_marker": MARKER,
            "schedule_index": index,
            "expected_job_count": len(jobs),
            "job_key": job["job_key"],
            "status": row["status"],
            "resumed_from_cache": was_resumed,
            "recorded_job_runtime_seconds": row["job_runtime_seconds"],
            "invocation_elapsed_seconds": time.monotonic() - started,
        }
        append_jsonl(log_path, log_row)
        counts = run_counts(run_directory, config, jobs)
        status = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "run_id": run_id,
            "state": "RUNNING",
            "schedule_index": index,
            "last_job_key": last_job_key,
            "newly_executed_this_invocation": newly_executed,
            "resumed_this_invocation": resumed,
            "invocation_elapsed_seconds": time.monotonic() - started,
            **counts,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(run_directory / "status.json", status)
        print(json.dumps(log_row), flush=True)
        if row["status"] != "COMPLETED_CONVERGED":
            invocation_state = "BLOCKED_JOB_FAILURE"
            blocking_job = row
            break
        if maximum_new_jobs > 0 and newly_executed >= maximum_new_jobs:
            invocation_state = "PAUSED_JOB_CAP"
            break
    counts = run_counts(run_directory, config, jobs)
    if counts["completed_converged"] == len(jobs):
        invocation_state = "COMPLETE"
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": run_id,
        "state": invocation_state,
        "expected_job_count": len(jobs),
        "newly_executed_this_invocation": newly_executed,
        "resumed_this_invocation": resumed,
        "last_job_key": last_job_key,
        "blocking_job": blocking_job,
        "invocation_elapsed_seconds": time.monotonic() - started,
        "wall_cap_hours": wall_cap_hours,
        "maximum_new_jobs": maximum_new_jobs,
        **counts,
        "pilot_numerical_matrix_complete": invocation_state == "COMPLETE",
        "statistical_analysis_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(run_directory / "status.json", result)
    if invocation_state == "COMPLETE":
        atomic_json(run_directory / "COMPLETED.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run"), default="dry-run")
    parser.add_argument("--run-id", default="bounded_central_anchor_pilot_v8")
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    manifest = read_json(MANIFEST)
    config = M5077.make_config(manifest, arguments.run_id)
    jobs = M5077.pilot_jobs(config, manifest)
    activation = activation_record(manifest, config, jobs)
    atomic_json(ACTIVATION_JSON, activation)
    write_validation(activation)
    if arguments.mode == "dry-run":
        result = {
            **activation,
            "dry_run": True,
            "execution_started": False,
        }
    else:
        result = execute(
            activation,
            manifest,
            config,
            jobs,
            arguments.run_id,
            arguments.wall_cap_hours,
            arguments.maximum_new_jobs,
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
