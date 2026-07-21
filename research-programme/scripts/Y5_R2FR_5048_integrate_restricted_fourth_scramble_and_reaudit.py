from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5047 = (
    POST / "scripts" / "Y5_R2FR_5047_restricted_fourth_scramble_scratch_matrix.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5048"
CANDIDATE = SOURCE / "candidate_live_replacements"
BACKUP = SOURCE / "live_backup_before_restricted_recompute"
STAGE_JSON = SOURCE / "staged_replacement_manifest.json"
RESULT_JSON = SOURCE / "restricted_fourth_scramble_integration.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5048_VALIDATION.csv"
)
MARKER = "MTS_5048_INTEGRATE_RESTRICTED_FOURTH_SCRAMBLE_AND_REAUDIT"
REVISION = "restricted-fourth-scramble-live-integration-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5047 = load_module("mts_5047_for_live_integration", SCRIPT_5047)
M5043 = M5047.M5043
M5040 = M5043.M5040
M5037 = M5040.M5037
M5036 = M5040.M5036
M5034 = M5047.M5034
RUN_5040 = M5047.RUN_5040
SCRATCH_RUN = M5047.RUN
MATRIX_JSON = M5047.MATRIX_JSON


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_value(value: dict[str, float]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def matrix() -> dict[str, Any]:
    if not MATRIX_JSON.exists():
        raise FileNotFoundError(MATRIX_JSON)
    document = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    if not (
        document.get("scratch_matrix_valid")
        and document.get("live_5040_replacement_authorized")
        and document.get("completed_jobs") == 45
        and document.get("converged_jobs") == 45
        and document.get("total_theorem_zero_residues") == 0
    ):
        raise RuntimeError("5047 scratch matrix does not authorize integration")
    return document


def live_name(epsilon_id: str, base_id: str) -> str:
    return f"{epsilon_id}__{M5047.EVENT_ID}__{base_id}__primary24.json"


def scratch_name(epsilon_id: str, base_id: str) -> str:
    return f"{epsilon_id}__{M5047.EVENT_ID}__{base_id}.json"


def replacement_contract(
    live_job_path: Path,
    live_kernel_path: Path,
    scratch_job_path: Path,
    scratch_kernel_path: Path,
    previous_cross_source_contract: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "integration_script": str(Path(__file__).resolve()),
        "integration_script_sha256": digest(Path(__file__).resolve()),
        "scope_audit": str(M5047.M5046.SCRIPT_5045_SCOPE),
        "scope_audit_sha256": digest(M5047.M5046.SCRIPT_5045_SCOPE),
        "restricted_benchmark": str(M5047.M5046.BENCHMARK_JSON),
        "restricted_benchmark_sha256": digest(M5047.M5046.BENCHMARK_JSON),
        "scratch_matrix": str(MATRIX_JSON),
        "scratch_matrix_sha256": digest(MATRIX_JSON),
        "scratch_job": str(scratch_job_path),
        "scratch_job_sha256": digest(scratch_job_path),
        "scratch_kernel": str(scratch_kernel_path),
        "scratch_kernel_sha256": digest(scratch_kernel_path),
        "previous_live_job_sha256": digest(live_job_path),
        "previous_live_kernel_sha256": digest(live_kernel_path),
        "previous_cross_source_contract_sha256": (
            hashlib.sha256(
                json.dumps(
                    previous_cross_source_contract,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()
            if previous_cross_source_contract is not None
            else None
        ),
        "previous_status": "SUPERSEDED_OVERBROAD_EXACT_ZERO_SCOPE",
        "replacement_rule": (
            "replace the entire S503404 fixed-event gate with the independently "
            "recomputed primary24 numeric-residue gate; apply no exact cross-source zeros"
        ),
        "restricted_exact_zero_count": 0,
        "valid_for_full_MTS_claim": False,
    }


def stage() -> dict[str, Any]:
    matrix_document = matrix()
    rows = []
    for scratch_summary in matrix_document["jobs"]:
        epsilon_id = str(scratch_summary["epsilon_id"])
        base_id = str(scratch_summary["base_argument_id"])
        live_job_path = RUN_5040 / "jobs" / live_name(epsilon_id, base_id)
        live_kernel_path = RUN_5040 / "kernels" / live_name(epsilon_id, base_id)
        scratch_job_path = SCRATCH_RUN / "jobs" / scratch_name(epsilon_id, base_id)
        scratch_kernel_path = SCRATCH_RUN / "kernels" / scratch_name(epsilon_id, base_id)
        for path in (
            live_job_path,
            live_kernel_path,
            scratch_job_path,
            scratch_kernel_path,
        ):
            if not path.exists():
                raise FileNotFoundError(path)
        live_job = json.loads(live_job_path.read_text(encoding="utf-8"))
        live_kernel = json.loads(live_kernel_path.read_text(encoding="utf-8"))
        scratch_job = json.loads(scratch_job_path.read_text(encoding="utf-8"))
        scratch_kernel = json.loads(scratch_kernel_path.read_text(encoding="utf-8"))
        if scratch_job.get("status") != "COMPLETED_CONVERGED":
            raise RuntimeError(f"scratch job is not converged: {scratch_job_path}")
        if int(scratch_job.get("theorem_zero_residue_count", -1)) != 0:
            raise RuntimeError(f"scratch job contains an exact zero: {scratch_job_path}")
        if int(scratch_job.get("unstable_numeric_residue_count", -1)) != 0:
            raise RuntimeError(f"scratch job contains an unstable residue: {scratch_job_path}")
        if live_job["event_id"] != scratch_job["event_id"]:
            raise RuntimeError(f"event mismatch: {live_job_path}")
        if live_job["argument_id"] != scratch_job["argument_id"]:
            raise RuntimeError(f"argument mismatch: {live_job_path}")
        contract = replacement_contract(
            live_job_path,
            live_kernel_path,
            scratch_job_path,
            scratch_kernel_path,
            live_job.get("cross_source_zero_contract"),
        )
        new_cross_source_contract = {
            "checkpoint_marker": MARKER,
            "status": "SUPERSEDED_OVERBROAD_SCOPE_AND_NUMERICALLY_RECOMPUTED",
            "previous_contract_available_in_backup": True,
            "restricted_exact_zero_count": 0,
            "numeric_residue_count": int(scratch_job["numeric_residue_count"]),
            "rule": "no cross-source exact-zero theorem was applied in this replacement",
            "valid_for_full_MTS_claim": False,
        }
        replacement_job = dict(live_job)
        replacement_job.update(
            {
                "status": "COMPLETED_CONVERGED",
                "integral_converged": True,
                "raw_fixed_event_kernel": scratch_job["raw_fixed_event_kernel"],
                "normalized_direct_D_hhh_over_G3": scratch_job[
                    "normalized_direct_D_hhh_over_G3"
                ],
                "highest_two_order_relative_residual": scratch_job[
                    "highest_two_order_relative_residual"
                ],
                "kernel_runtime_seconds": scratch_job["kernel_runtime_seconds"],
                "job_runtime_seconds": float(live_job["topology_runtime_seconds"])
                + float(scratch_job["kernel_runtime_seconds"]),
                "completed_at": M5036.utc_now(),
                "residue_radius_contract": {
                    "revision": M5047.REVISION,
                    "numeric_residue_count": int(scratch_job["numeric_residue_count"]),
                    "unstable_numeric_residue_count": 0,
                    "chart_origin_exclusion_count": int(
                        scratch_job["chart_origin_exclusion_count"]
                    ),
                    "scratch_kernel": str(scratch_kernel_path),
                    "scratch_kernel_sha256": digest(scratch_kernel_path),
                    "valid_for_full_MTS_claim": False,
                },
                "cross_source_zero_contract": new_cross_source_contract,
                "restricted_scope_recompute_contract": contract,
                "valid_for_full_MTS_claim": False,
            }
        )
        replacement_kernel = dict(live_kernel)
        replacement_kernel.update(
            {
                "fixed_event_integral_gate": scratch_kernel[
                    "fixed_event_integral_gate"
                ],
                "residue_radius_contract": replacement_job["residue_radius_contract"],
                "cross_source_zero_contract": new_cross_source_contract,
                "restricted_scope_recompute_contract": contract,
                "valid_for_full_MTS_claim": False,
            }
        )
        candidate_job_path = CANDIDATE / "jobs" / live_job_path.name
        candidate_kernel_path = CANDIDATE / "kernels" / live_kernel_path.name
        atomic_json(candidate_job_path, replacement_job)
        atomic_json(candidate_kernel_path, replacement_kernel)
        candidate_direct = complex_value(
            replacement_job["normalized_direct_D_hhh_over_G3"]
        )
        scratch_direct = complex_value(
            scratch_job["normalized_direct_D_hhh_over_G3"]
        )
        gate_kernel = M5034.highest_value(
            replacement_kernel["fixed_event_integral_gate"]
        )
        gate_direct = M5034.KERNEL_MULTIPLIER * gate_kernel
        passed = bool(
            candidate_direct == scratch_direct
            and abs(gate_direct - scratch_direct) < 1.0e-12 * max(1.0, abs(scratch_direct))
            and replacement_kernel["fixed_event_integral_gate"][
                "fixed_event_crossed_integral_converged"
            ]
            and replacement_kernel["fixed_event_integral_gate"]["all_residues_stable"]
        )
        rows.append(
            {
                "job_key": live_job["job_key"],
                "live_job": str(live_job_path),
                "live_kernel": str(live_kernel_path),
                "original_live_job_sha256": digest(live_job_path),
                "original_live_kernel_sha256": digest(live_kernel_path),
                "candidate_job": str(candidate_job_path),
                "candidate_kernel": str(candidate_kernel_path),
                "candidate_job_sha256": digest(candidate_job_path),
                "candidate_kernel_sha256": digest(candidate_kernel_path),
                "scratch_job_sha256": digest(scratch_job_path),
                "scratch_kernel_sha256": digest(scratch_kernel_path),
                "candidate_validation_passed": passed,
            }
        )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "staged_jobs": len(rows),
        "all_candidate_validations_passed": len(rows) == 45
        and all(row["candidate_validation_passed"] for row in rows),
        "rows": rows,
        "live_files_modified": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(STAGE_JSON, result)
    return result


def apply() -> dict[str, Any]:
    staged = json.loads(STAGE_JSON.read_text(encoding="utf-8")) if STAGE_JSON.exists() else stage()
    if not (
        staged.get("staged_jobs") == 45
        and staged.get("all_candidate_validations_passed")
    ):
        raise RuntimeError("staged candidates do not authorize live integration")
    applied = []
    for row in staged["rows"]:
        live_job_path = Path(row["live_job"])
        live_kernel_path = Path(row["live_kernel"])
        candidate_job_path = Path(row["candidate_job"])
        candidate_kernel_path = Path(row["candidate_kernel"])
        current_job_hash = digest(live_job_path)
        current_kernel_hash = digest(live_kernel_path)
        candidate_job_hash = digest(candidate_job_path)
        candidate_kernel_hash = digest(candidate_kernel_path)
        if current_job_hash == candidate_job_hash and current_kernel_hash == candidate_kernel_hash:
            applied.append({"job_key": row["job_key"], "status": "ALREADY_APPLIED"})
            continue
        if current_job_hash != row["original_live_job_sha256"]:
            raise RuntimeError(f"live job changed after staging: {live_job_path}")
        if current_kernel_hash != row["original_live_kernel_sha256"]:
            raise RuntimeError(f"live kernel changed after staging: {live_kernel_path}")
        backup_job_path = BACKUP / "jobs" / live_job_path.name
        backup_kernel_path = BACKUP / "kernels" / live_kernel_path.name
        backup_job_path.parent.mkdir(parents=True, exist_ok=True)
        backup_kernel_path.parent.mkdir(parents=True, exist_ok=True)
        if not backup_job_path.exists():
            shutil.copy2(live_job_path, backup_job_path)
        if not backup_kernel_path.exists():
            shutil.copy2(live_kernel_path, backup_kernel_path)
        if digest(backup_job_path) != row["original_live_job_sha256"]:
            raise RuntimeError(f"backup job hash mismatch: {backup_job_path}")
        if digest(backup_kernel_path) != row["original_live_kernel_sha256"]:
            raise RuntimeError(f"backup kernel hash mismatch: {backup_kernel_path}")
        os.replace(shutil.copy2(candidate_job_path, live_job_path.with_suffix(".json.tmp")), live_job_path)
        os.replace(
            shutil.copy2(candidate_kernel_path, live_kernel_path.with_suffix(".json.tmp")),
            live_kernel_path,
        )
        applied.append({"job_key": row["job_key"], "status": "APPLIED"})
    config = json.loads((RUN_5040 / "config.json").read_text(encoding="utf-8"))
    jobs = M5036.load_jobs(RUN_5040)
    started = time.monotonic()
    summary = M5037.write_augmented_status(
        RUN_5040,
        config,
        jobs,
        "COMPLETE_RESTRICTED_SCOPE_REPAIR",
        started,
    )
    audit = M5040.write_5040_artifacts(config, summary, RUN_5040)
    M5036.append_log(
        RUN_5040,
        "5048 restricted-scope repair replaced all 45 S503404 primary24 jobs from hash-linked scratch gates",
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "applied_jobs": sum(row["status"] == "APPLIED" for row in applied),
        "already_applied_jobs": sum(row["status"] == "ALREADY_APPLIED" for row in applied),
        "backup_jobs": len(list((BACKUP / "jobs").glob("*.json"))),
        "backup_kernels": len(list((BACKUP / "kernels").glob("*.json"))),
        "run_state": summary["run_state"],
        "terminal_jobs": summary["terminal_jobs"],
        "remaining_jobs": summary["remaining_jobs"],
        "failed_jobs": summary["failed_jobs"],
        "unconverged_jobs": summary["unconverged_jobs"],
        "nested_variance_decision": audit.get("decision"),
        "nested_variance_gate": audit.get("gate"),
        "applied": applied,
        "formalization_workbench_tree_sha256": tree_digest(
            POST.parent / "formalization-workbench"
        ),
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    write_validation(result, staged)
    return result


def analyze() -> dict[str, Any]:
    staged = json.loads(STAGE_JSON.read_text(encoding="utf-8"))
    applied_rows = []
    for row in staged["rows"]:
        live_job_path = Path(row["live_job"])
        live_kernel_path = Path(row["live_kernel"])
        applied_rows.append(
            {
                "job_key": row["job_key"],
                "job_matches_candidate": digest(live_job_path)
                == row["candidate_job_sha256"],
                "kernel_matches_candidate": digest(live_kernel_path)
                == row["candidate_kernel_sha256"],
            }
        )
    result = json.loads(RESULT_JSON.read_text(encoding="utf-8")) if RESULT_JSON.exists() else {}
    return {
        **result,
        "live_match_rows": applied_rows,
        "all_live_files_match_candidates": all(
            row["job_matches_candidate"] and row["kernel_matches_candidate"]
            for row in applied_rows
        ),
        "valid_for_full_MTS_claim": False,
    }


def write_validation(result: dict[str, Any], staged: dict[str, Any]) -> None:
    checks = [
        ("forty_five_candidates_valid", staged["staged_jobs"] == 45 and staged["all_candidate_validations_passed"], str(staged["staged_jobs"])),
        ("forty_five_backups_each", result["backup_jobs"] == 45 and result["backup_kernels"] == 45, f"{result['backup_jobs']}/{result['backup_kernels']}"),
        ("all_378_jobs_terminal", result["terminal_jobs"] == 378 and result["remaining_jobs"] == 0, f"{result['terminal_jobs']}/{result['remaining_jobs']}"),
        ("no_failed_or_unconverged", result["failed_jobs"] == 0 and result["unconverged_jobs"] == 0, f"{result['failed_jobs']}/{result['unconverged_jobs']}"),
        ("claim_remains_false", not result["valid_for_full_MTS_claim"], "required false"),
        ("formalization_workbench_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(
            {
                "check": name,
                "passed": str(bool(passed)).lower(),
                "evidence": evidence,
            }
            for name, passed, evidence in checks
        )


def dry_run() -> dict[str, Any]:
    matrix_document = matrix()
    expected = [
        (epsilon_id, base_id)
        for epsilon_id in M5047.EPSILON_IDS
        for base_id in M5047.BASE_IDS
    ]
    paths = [
        RUN_5040 / "jobs" / live_name(epsilon_id, base_id)
        for epsilon_id, base_id in expected
    ] + [
        RUN_5040 / "kernels" / live_name(epsilon_id, base_id)
        for epsilon_id, base_id in expected
    ]
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scratch_matrix_valid": matrix_document["scratch_matrix_valid"],
        "scratch_jobs": matrix_document["completed_jobs"],
        "expected_live_files": len(paths),
        "all_live_files_exist": all(path.exists() for path in paths),
        "formalization_workbench_tree_sha256": tree_digest(
            POST.parent / "formalization-workbench"
        ),
        "valid_for_full_MTS_claim": False,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "stage", "apply", "analyze"), default="dry-run")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "stage":
        result = stage()
    elif arguments.mode == "apply":
        result = apply()
    else:
        result = analyze()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
