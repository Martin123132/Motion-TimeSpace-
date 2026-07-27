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
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5079 = POST / "scripts" / "Y5_R2FR_5079_bounded_central_anchor_pilot_runner.py"
PILOT_V6 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v6"
)
INTEGRATION_5089 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5089"
    / "exact_double_zero_runner_integration_smoke.json"
)
INTEGRATION_RUN_5089 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5089"
    / "exact_double_zero_runner_integration_smoke"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5090"
PILOT_V7 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v7"
)
MANIFEST_JSON = SOURCE / "v7_certified_carry_forward_manifest.json"
RESULT_JSON = SOURCE / "v7_certified_carry_forward_result.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5090_VALIDATION.csv"
)
MARKER = "MTS_5090_V7_PILOT_CERTIFIED_CARRY_FORWARD"
REVISION = "hash-locked-v6-plus-5089-carry-forward-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
RUN_ID = "bounded_central_anchor_pilot_v7"
EXACT_JOB_KEY = "E020__S507603_N0000__A07__primary24"
NONNUMERICAL_CONFIG_KEYS = {
    "config_digest",
    "run_id",
    "schema_revision",
    "source_files",
    "exact_double_zero_global_collision_policy",
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


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def numerical_config(config: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in config.items()
        if key not in NONNUMERICAL_CONFIG_KEYS
    }


def carried_document(
    source_path: Path,
    source: dict[str, Any],
    target_config_digest: str,
    kind: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = dict(source)
    result["config_digest"] = target_config_digest
    result["5090_carry_forward"] = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "kind": kind,
        "source_path": str(source_path),
        "source_sha256": digest(source_path),
        "source_config_digest": source.get("config_digest"),
        "target_config_digest": target_config_digest,
        "numerical_contract_unchanged": True,
        "valid_for_full_MTS_claim": False,
        **(extra or {}),
    }
    return result


def main() -> None:
    required = [
        SCRIPT_5077,
        SCRIPT_5079,
        PILOT_V6 / "config.json",
        PILOT_V6 / "status.json",
        INTEGRATION_5089,
        INTEGRATION_RUN_5089 / "jobs" / f"{EXACT_JOB_KEY}.json",
        INTEGRATION_RUN_5089 / "kernels" / f"{EXACT_JOB_KEY}.json",
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5090 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5090", SCRIPT_5077)
    module_5079 = load_module("mts_5079_for_5090", SCRIPT_5079)
    manifest = read_json(module_5077.MANIFEST)
    config_v6 = read_json(PILOT_V6 / "config.json")
    config_v7 = module_5077.make_config(manifest, RUN_ID)
    jobs = module_5077.pilot_jobs(config_v7, manifest)
    numerical_v6 = numerical_config(config_v6)
    numerical_v7 = numerical_config(config_v7)
    numerical_contract_equal = numerical_v6 == numerical_v7
    numerical_contract_digest = canonical_digest(numerical_v7)
    if not numerical_contract_equal:
        raise RuntimeError("v6 and v7 numerical configurations differ")
    PILOT_V7.mkdir(parents=True, exist_ok=True)
    config_path = PILOT_V7 / "config.json"
    if config_path.exists():
        existing = read_json(config_path)
        if existing["config_digest"] != config_v7["config_digest"]:
            raise RuntimeError("existing v7 config differs from current v7 config")
    atomic_json(config_path, config_v7)
    topology_rows: list[dict[str, Any]] = []
    for source_path in sorted((PILOT_V6 / "topologies").glob("*.json")):
        source = read_json(source_path)
        output = PILOT_V7 / "topologies" / source_path.name
        carried = carried_document(
            source_path,
            source,
            config_v7["config_digest"],
            "causal_topology",
            {
                "reason": (
                    "the 5088 repair changes only a target-local global "
                    "collision value, not transported roots or topology"
                )
            },
        )
        atomic_json(output, carried)
        topology_rows.append(
            {
                "source": str(source_path),
                "source_sha256": digest(source_path),
                "output": str(output),
                "output_sha256": digest(output),
            }
        )
    carried_job_rows: list[dict[str, Any]] = []
    for source_job_path in sorted((PILOT_V6 / "jobs").glob("*.json")):
        source_job = read_json(source_job_path)
        if source_job.get("status") != "COMPLETED_CONVERGED":
            continue
        if source_job["job_key"] == EXACT_JOB_KEY:
            raise RuntimeError("v6 unexpectedly contains a converged exact target row")
        source_kernel_path = PILOT_V6 / "kernels" / source_job_path.name
        if not source_kernel_path.exists():
            raise FileNotFoundError(source_kernel_path)
        output_kernel_path = PILOT_V7 / "kernels" / source_job_path.name
        output_job_path = PILOT_V7 / "jobs" / source_job_path.name
        topology_name = Path(source_job["topology_file"]).name
        output_topology_path = PILOT_V7 / "topologies" / topology_name
        source_kernel = read_json(source_kernel_path)
        carried_kernel = carried_document(
            source_kernel_path,
            source_kernel,
            config_v7["config_digest"],
            "completed_kernel",
            {"algorithm_change_outside_job_scope": True},
        )
        carried_kernel["topology_file"] = str(output_topology_path)
        atomic_json(output_kernel_path, carried_kernel)
        carried_job = carried_document(
            source_job_path,
            source_job,
            config_v7["config_digest"],
            "completed_job",
            {"algorithm_change_outside_job_scope": True},
        )
        carried_job["topology_file"] = str(output_topology_path)
        carried_job["kernel_file"] = str(output_kernel_path)
        atomic_json(output_job_path, carried_job)
        carried_job_rows.append(
            {
                "job_key": source_job["job_key"],
                "source_job": str(source_job_path),
                "source_job_sha256": digest(source_job_path),
                "source_kernel": str(source_kernel_path),
                "source_kernel_sha256": digest(source_kernel_path),
                "output_job": str(output_job_path),
                "output_job_sha256": digest(output_job_path),
                "output_kernel": str(output_kernel_path),
                "output_kernel_sha256": digest(output_kernel_path),
            }
        )
    integration_5089 = read_json(INTEGRATION_5089)
    exact_source_job_path = (
        INTEGRATION_RUN_5089 / "jobs" / f"{EXACT_JOB_KEY}.json"
    )
    exact_source_kernel_path = (
        INTEGRATION_RUN_5089 / "kernels" / f"{EXACT_JOB_KEY}.json"
    )
    exact_source_job = read_json(exact_source_job_path)
    exact_source_kernel = read_json(exact_source_kernel_path)
    exact_topology_name = Path(exact_source_job["topology_file"]).name
    exact_output_topology = PILOT_V7 / "topologies" / exact_topology_name
    exact_output_kernel = PILOT_V7 / "kernels" / f"{EXACT_JOB_KEY}.json"
    exact_output_job = PILOT_V7 / "jobs" / f"{EXACT_JOB_KEY}.json"
    carried_exact_kernel = carried_document(
        exact_source_kernel_path,
        exact_source_kernel,
        config_v7["config_digest"],
        "5089_certified_exact_kernel",
        {
            "5089_integration_path": str(INTEGRATION_5089),
            "5089_integration_sha256": digest(INTEGRATION_5089),
        },
    )
    carried_exact_kernel["topology_file"] = str(exact_output_topology)
    atomic_json(exact_output_kernel, carried_exact_kernel)
    carried_exact_job = carried_document(
        exact_source_job_path,
        exact_source_job,
        config_v7["config_digest"],
        "5089_certified_exact_job",
        {
            "5089_integration_path": str(INTEGRATION_5089),
            "5089_integration_sha256": digest(INTEGRATION_5089),
        },
    )
    carried_exact_job["topology_file"] = str(exact_output_topology)
    carried_exact_job["kernel_file"] = str(exact_output_kernel)
    atomic_json(exact_output_job, carried_exact_job)
    exact_row = {
        "job_key": EXACT_JOB_KEY,
        "source_job": str(exact_source_job_path),
        "source_job_sha256": digest(exact_source_job_path),
        "source_kernel": str(exact_source_kernel_path),
        "source_kernel_sha256": digest(exact_source_kernel_path),
        "output_job": str(exact_output_job),
        "output_job_sha256": digest(exact_output_job),
        "output_kernel": str(exact_output_kernel),
        "output_kernel_sha256": digest(exact_output_kernel),
    }
    carry_forward_manifest = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_run": str(PILOT_V6),
        "target_run": str(PILOT_V7),
        "source_config_digest": config_v6["config_digest"],
        "target_config_digest": config_v7["config_digest"],
        "numerical_contract_digest": numerical_contract_digest,
        "numerical_contract_equal": numerical_contract_equal,
        "exact_guard_job_scope": module_5077.DOUBLE_ZERO_JOB_KEY,
        "v6_completed_job_count": len(carried_job_rows),
        "5089_exact_job_count": 1,
        "total_carried_completed_job_count": len(carried_job_rows) + 1,
        "topology_count": len(topology_rows),
        "topologies": topology_rows,
        "v6_completed_jobs": carried_job_rows,
        "certified_5089_job": exact_row,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, carry_forward_manifest)
    counts = module_5079.run_counts(PILOT_V7, config_v7, jobs)
    next_missing_job = next(
        (
            job["job_key"]
            for job in jobs
            if not (PILOT_V7 / "jobs" / f"{job['job_key']}.json").exists()
        ),
        None,
    )
    formal_digest = tree_digest(FORMAL)
    accepted = bool(
        numerical_contract_equal
        and len(jobs) == 360
        and len(carried_job_rows) == 112
        and integration_5089["runner_exact_guard_integration_accepted"]
        and integration_5089["pilot_resume_authorized"]
        and exact_source_job["status"] == "COMPLETED_CONVERGED"
        and exact_source_kernel["profile_audit"][
            "exact_double_zero_collision_extension_count"
        ]
        == 2
        and counts
        == {
            "completed_converged": 113,
            "completed_unconverged": 0,
            "failed": 0,
            "missing": 247,
        }
        and formal_digest == FORMAL_BASELINE
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "run_directory": str(PILOT_V7),
        "config_digest": config_v7["config_digest"],
        "schedule_digest": module_5077.M5036.canonical_digest(jobs),
        "expected_job_count": len(jobs),
        "carry_forward_manifest": str(MANIFEST_JSON),
        "carry_forward_manifest_sha256": digest(MANIFEST_JSON),
        "numerical_contract_equal": numerical_contract_equal,
        "numerical_contract_digest": numerical_contract_digest,
        "counts": counts,
        "next_missing_job": next_missing_job,
        "certified_carry_forward_accepted": accepted,
        "pilot_resume_authorized": accepted,
        "pilot_matrix_complete": False,
        "statistical_analysis_authorized": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    atomic_json(
        PILOT_V7 / "status.json",
        {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "run_id": RUN_ID,
            "state": "PAUSED_AFTER_CERTIFIED_CARRY_FORWARD",
            "last_job_key": EXACT_JOB_KEY,
            "blocking_job": None,
            "expected_job_count": len(jobs),
            **counts,
            "next_missing_job": next_missing_job,
            "pilot_numerical_matrix_complete": False,
            "statistical_analysis_complete": False,
            "valid_for_full_MTS_claim": False,
        },
    )
    checks = [
        ("source_paths_exist", not missing, "all carry-forward inputs exist"),
        (
            "numerical_contract_equal",
            numerical_contract_equal,
            numerical_contract_digest,
        ),
        (
            "schedule_unchanged",
            len(jobs) == 360,
            f"jobs={len(jobs)}",
        ),
        (
            "v6_rows_exclude_repaired_target",
            len(carried_job_rows) == 112
            and all(row["job_key"] != EXACT_JOB_KEY for row in carried_job_rows),
            f"v6_converged={len(carried_job_rows)}",
        ),
        (
            "exact_row_from_accepted_5089",
            integration_5089["runner_exact_guard_integration_accepted"]
            and exact_source_job["status"] == "COMPLETED_CONVERGED"
            and exact_source_kernel["profile_audit"][
                "exact_double_zero_collision_extension_count"
            ]
            == 2,
            EXACT_JOB_KEY,
        ),
        (
            "v7_counts",
            counts
            == {
                "completed_converged": 113,
                "completed_unconverged": 0,
                "failed": 0,
                "missing": 247,
            },
            str(counts),
        ),
        (
            "resume_authorization_consistent",
            result["pilot_resume_authorized"] == accepted,
            f"accepted={accepted}",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["pilot_matrix_complete"]
            and not result["statistical_analysis_authorized"]
            and not result["valid_for_full_MTS_claim"],
            "carry-forward is resumability plumbing, not evidence",
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
                    "check_id": f"V5090_{index:02d}_{name}",
                    "passed": bool(passed),
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5090 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
