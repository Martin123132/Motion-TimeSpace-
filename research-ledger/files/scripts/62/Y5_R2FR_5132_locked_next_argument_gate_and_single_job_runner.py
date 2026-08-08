from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5128 = (
    POST
    / "scripts"
    / "Y5_R2FR_5128_argument_local_outer_collinear_preflight_and_A11_replay.py"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5128 = load_module("mts_5128_for_locked_next", SCRIPT_5128)


def output_path(job: dict[str, Any]) -> Path:
    if job["stratum"] == "full_remainder":
        return M5128.M5125.full_output_path(M5128.RUN, job)
    return M5128.M5125.topological_output_path(M5128.RUN, job)


def first_incomplete_job(
    schedule: list[dict[str, Any]], config_digest: str
) -> dict[str, Any]:
    for job in schedule:
        path = output_path(job)
        if not path.exists():
            return job
        row = M5128.read_json(path)
        if (
            row.get("config_digest") != config_digest
            or row.get("status") != "COMPLETED_CONVERGED"
            or (
                job["stratum"] == "full_remainder"
                and row.get("strict_adaptive_validated") is not True
            )
        ):
            return job
    raise RuntimeError("locked schedule is already complete")


def expected_counts_after(
    counts: dict[str, int], job: dict[str, Any], config_digest: str
) -> dict[str, int]:
    expected = dict(counts)
    path = output_path(job)
    if not path.exists():
        expected["missing"] -= 1
    else:
        row = M5128.read_json(path)
        if row.get("config_digest") != config_digest:
            expected["missing"] -= 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            expected["completed_unconverged"] -= 1
        elif row.get("status") == "FAILED":
            expected["failed"] -= 1
        elif row.get("status") == "COMPLETED_CONVERGED":
            return expected
        else:
            expected["missing"] -= 1
    expected["completed_converged"] += 1
    if any(value < 0 for value in expected.values()):
        raise RuntimeError(f"invalid expected count transition: {expected}")
    return expected


def configure(arguments: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    config = M5128.read_json(M5128.CONFIG)
    schedule = M5128.read_json(M5128.SCHEDULE)["jobs"]
    first = first_incomplete_job(schedule, config["config_digest"])
    if arguments.job_key is None:
        job = first
    else:
        job = next(
            row for row in schedule if row["job_key"] == arguments.job_key
        )
        if arguments.mode != "finalize-existing" and job != first:
            raise RuntimeError(
                "requested job is not the first incomplete locked row: "
                f"requested={job['job_key']};first={first['job_key']}"
            )
    if job["stratum"] != "full_remainder" or job["profile"] != "primary24":
        raise RuntimeError(
            "argument-local outer-collinear runner only supports locked "
            "primary24 full-remainder rows"
        )
    counts = M5128.M5125.run_counts(
        M5128.RUN, config["config_digest"], schedule
    )
    target_output = output_path(job)
    target_existing = (
        M5128.read_json(target_output) if target_output.exists() else {}
    )
    repairing_first_incomplete_unconverged = bool(
        job == first
        and counts["failed"] == 0
        and counts["completed_unconverged"] == 1
        and target_existing.get("config_digest") == config["config_digest"]
        and target_existing.get("status") == "COMPLETED_UNCONVERGED"
    )
    if (
        counts["failed"]
        or counts["completed_unconverged"]
    ) and not repairing_first_incomplete_unconverged:
        raise RuntimeError(
            "refusing forward selection while a failed or unconverged row exists: "
            f"{counts}"
        )
    checkpoint_id = str(arguments.checkpoint_id)
    base_argument_id = str(job["base_argument_id"])
    source = (
        POST / "source-intake" / "functional_rg" / checkpoint_id
    )
    marker = (
        f"MTS_{checkpoint_id}_ARGUMENT_LOCAL_OUTER_COLLINEAR_"
        f"{base_argument_id}"
    )
    initial_rejected_gate = (
        source
        / f"{base_argument_id}_initial_rejected_chart_gate.json"
    )
    M5128.CHECKPOINT_ID = checkpoint_id
    M5128.MARKER = marker
    M5128.REVISION = "locked-next-argument-log-cauchy-chart-v1"
    M5128.CHECKED_DATE = str(arguments.checked_date)
    M5128.JOB_KEY = str(job["job_key"])
    M5128.EVENT_ID = str(job["event_id"])
    M5128.EPSILON_ID = str(job["epsilon_id"])
    M5128.BASE_ARGUMENT_ID = base_argument_id
    M5128.SOURCE = source
    M5128.PREFLIGHT_JSON = (
        source
        / f"{base_argument_id}_argument_local_outer_collinear_preflight.json"
    )
    M5128.GATE_JSON = (
        source
        / f"{base_argument_id}_argument_local_outer_collinear_chart_gate.json"
    )
    M5128.CATALOG_CSV = (
        source
        / f"{base_argument_id}_argument_local_outer_collinear_catalog.csv"
    )
    M5128.RESULT_JSON = (
        source
        / f"{base_argument_id}_argument_local_outer_collinear_replay_result.json"
    )
    M5128.STATUS_JSON = (
        source
        / f"{base_argument_id}_argument_local_outer_collinear_replay_status.json"
    )
    M5128.VALIDATION_CSV = (
        POST
        / "source-intake"
        / "mts_residuals"
        / f"P8_Y5_BRR545_{checkpoint_id}_VALIDATION.csv"
    )
    M5128.DOCUMENT = (
        POST
        / (
            f"{checkpoint_id}-Y5-R2FR-argument-local-outer-collinear-"
            f"{base_argument_id}-replay.md"
        )
    )
    M5128.INITIAL_REJECTED_GATE = initial_rejected_gate
    M5128.EXPECTED_COUNTS_AFTER = expected_counts_after(
        counts, job, config["config_digest"]
    )
    M5128.M5127.JOB_KEY = M5128.JOB_KEY
    M5128.M5127.MARKER = marker
    M5128.M5127.REVISION = M5128.REVISION
    M5128.M5127.CHECKED_DATE = M5128.CHECKED_DATE
    if arguments.precision == "nested":
        M5128.PRECISION_POLICY = {
            "low_boundary_nodes": 48,
            "low_global_nodes": 64,
            "low_global_residue_nodes": 96,
            "high_boundary_nodes": 64,
            "high_global_nodes": 96,
            "high_global_residue_nodes": 128,
            "selection": (
                "nested precision is allowed only after a preserved default "
                "gate rejects residue agreement while isolation, Laurent order, "
                "and regular-part uncertainty pass"
            ),
            "acceptance_threshold_changed": False,
        }
        M5128.M5127.LOW_BOUNDARY_NODES = 48
        M5128.M5127.LOW_GLOBAL_NODES = 64
        M5128.M5127.LOW_RESIDUE_NODES = 96
        M5128.M5127.HIGH_BOUNDARY_NODES = 64
        M5128.M5127.HIGH_GLOBAL_NODES = 96
        M5128.M5127.HIGH_RESIDUE_NODES = 128
    configuration = M5128.tagged(
        {
            "job": job,
            "first_incomplete_job": first["job_key"],
            "counts_before": counts,
            "expected_counts_after": M5128.EXPECTED_COUNTS_AFTER,
            "precision": arguments.precision,
            "mode": arguments.mode,
            "single_job_only": True,
            "bulk_resume_authorized": False,
            "repairing_first_incomplete_unconverged": (
                repairing_first_incomplete_unconverged
            ),
        }
    )
    M5128.atomic_json(
        source / "locked_next_job_configuration.json", configuration
    )
    return job, configuration


def preserve_rejected_gate() -> None:
    path = M5128.INITIAL_REJECTED_GATE
    if (
        path is None
        or path.exists()
        or not M5128.GATE_JSON.exists()
    ):
        return
    gate = M5128.read_json(M5128.GATE_JSON)
    if not bool(gate.get("gate_accepted")):
        M5128.atomic_json(path, gate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-id", default="5132")
    parser.add_argument("--checked-date", default="2026-07-20")
    parser.add_argument("--job-key")
    parser.add_argument(
        "--precision", choices=("default", "nested"), default="default"
    )
    parser.add_argument(
        "--mode",
        choices=("dry-run", "gate", "execute", "finalize-existing"),
        default="dry-run",
    )
    arguments = parser.parse_args()
    _, configuration = configure(arguments)
    preserve_rejected_gate()
    if arguments.mode == "dry-run":
        _, result = M5128.structural_preflight()
    elif arguments.mode == "gate":
        result = M5128.gate_only()
    elif arguments.mode == "execute":
        result = M5128.execute()
    else:
        result = M5128.finalize_existing()
    preserve_rejected_gate()
    print(
        json.dumps(
            {"configuration": configuration, "result": result},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
