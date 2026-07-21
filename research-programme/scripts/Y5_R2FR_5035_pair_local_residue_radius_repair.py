from __future__ import annotations

import argparse
import importlib.util
import json
import math
import shutil
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5035 = (
    POST
    / "scripts"
    / "Y5_R2FR_5035_paired_epsilon_outer_scramble_ladder.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5035"
REPAIRS = SOURCE / "repairs"
MARKER = "MTS_5035_PAIR_LOCAL_RESIDUE_SHRINKING_RADIUS_REPAIR"
REVISION = "pair-local-double-residue-shrinking-radius-v4"
CANDIDATE_FRACTIONS = (0.1, 0.05, 0.025, 0.0125, 0.2)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5035 = load_module("mts_5035_for_residue_repair", SCRIPT_5035)
N5030 = M5035.M5034.M5030
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
CURRENT_JOB = ""
RADIUS_AUDIT: list[dict[str, Any]] = []


def serialized_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def repaired_chamber_residue_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    target_groups = N5030.collision_groups(N5030.TARGET_COSINE, ownership)
    all_roots = [complex(group["root"]) for group in target_groups]
    selected: list[dict[str, Any]] = []
    for group in target_groups:
        root = complex(group["root"])
        log_point, distance, projection, copy_index = (
            N5030.nearest_log_copy_to_segment(root, start, end)
        )
        near_path = distance < model_distance and -0.25 < projection < 1.25
        required = any(
            abs(root - candidate)
            < 2.0e-5 * max(1.0, abs(root), abs(candidate))
            for candidate in required_roots
        )
        if not near_path and not required:
            continue
        selected.append(
            {
                "root": root,
                "pairs": group["pairs"],
                "log_point": log_point,
                "log_distance": distance,
                "segment_projection": projection,
                "copy_index": copy_index,
                "near_path": near_path,
                "required_for_homotopy": required,
            }
        )
    catalog: list[dict[str, Any]] = []
    all_stable = True
    for row in selected:
        root = row["root"]
        separations = [
            abs(root - other)
            for other in all_roots
            if abs(root - other)
            > 1.0e-7 * max(1.0, abs(root), abs(other))
        ]
        safe_scale = min([abs(root)] + separations)

        def residue_pair(fraction: float) -> dict[str, Any]:
            radius = fraction * safe_scale
            outer = N5030.pair_local_relative_residue(
                root,
                radius,
                max(32, relative_residue_nodes + 8),
                row["pairs"],
                ownership,
                max(32, global_residue_nodes + 8),
            )
            inner = N5030.pair_local_relative_residue(
                root,
                radius / 2.0,
                max(48, relative_residue_nodes + 24),
                row["pairs"],
                ownership,
                max(48, global_residue_nodes + 16),
            )
            magnitude = max(abs(inner), abs(outer))
            stability = abs(inner - outer) / max(magnitude, 1.0e-30)
            numerically_zero = magnitude < 1.0e-7
            stable = numerically_zero or stability < 5.0e-3
            return {
                "fraction": fraction,
                "radius": radius,
                "outer": outer,
                "inner": inner,
                "stability": stability,
                "numerically_zero": numerically_zero,
                "stable": stable,
            }

        candidates = [residue_pair(0.1)]
        if not candidates[0]["stable"]:
            for fraction in CANDIDATE_FRACTIONS[1:4]:
                candidates.append(residue_pair(fraction))
                if candidates[-1]["stable"]:
                    break
            if not any(candidate["stable"] for candidate in candidates):
                candidates.append(residue_pair(0.2))
        stable_candidates = [
            candidate for candidate in candidates if candidate["stable"]
        ]
        chosen = (
            stable_candidates[0]
            if stable_candidates
            else min(candidates, key=lambda candidate: candidate["stability"])
        )
        if not candidates[0]["stable"]:
            RADIUS_AUDIT.append(
                {
                    "job_key": CURRENT_JOB,
                    "root": serialized_complex(root),
                    "pairs": row["pairs"],
                    "safe_scale": safe_scale,
                    "nearest_distinct_root_separation": (
                        min(separations) if separations else None
                    ),
                    "candidate_rows": [
                        {
                            "fraction": candidate["fraction"],
                            "radius": candidate["radius"],
                            "outer": serialized_complex(candidate["outer"]),
                            "inner": serialized_complex(candidate["inner"]),
                            "stability": candidate["stability"],
                            "numerically_zero": candidate["numerically_zero"],
                            "stable": candidate["stable"],
                        }
                        for candidate in candidates
                    ],
                    "selected_fraction": chosen["fraction"],
                    "selected_stable": chosen["stable"],
                    "selection_rule": (
                        "first_stable_nested_pair_while_shrinking_from_0.1; "
                        "0.2_is_diagnostic_last_resort_only"
                    ),
                }
            )
        all_stable = all_stable and bool(chosen["stable"])
        catalog.append(
            {
                **row,
                "outer_radius": chosen["radius"],
                "residue_method": REVISION,
                "residue_contour_fraction": chosen["fraction"],
                "outer_residue": chosen["outer"],
                "inner_residue": chosen["inner"],
                "residue": (
                    0.0j if chosen["numerically_zero"] else chosen["inner"]
                ),
                "residue_stability": chosen["stability"],
                "numerically_zero": chosen["numerically_zero"],
                "stable": chosen["stable"],
                "included_as_pole_model": row["near_path"]
                and not chosen["numerically_zero"]
                and chosen["stable"],
            }
        )
    return catalog, all_stable


def repairable_job(
    run_directory: Path, job_path: Path
) -> tuple[bool, dict[str, Any], dict[str, Any]]:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    if job.get("status") != "COMPLETED_UNCONVERGED":
        return False, job, {}
    kernel_path = run_directory / "kernels" / job_path.name
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    gate = kernel["fixed_event_integral_gate"]
    repairable = (
        job.get("status") == "COMPLETED_UNCONVERGED"
        and bool(job.get("topology_passed"))
        and not bool(gate.get("all_residues_stable"))
        and all(
            bool(row.get("adaptive_quadrature_converged"))
            for row in gate.get("order_rows", [])
        )
    )
    return repairable, job, kernel


def copy_topology(
    run_directory: Path,
    repair_run: Path,
    job: dict[str, Any],
) -> None:
    source = M5035.M5034.topology_path(
        run_directory, job["event_id"], job["argument_id"]
    )
    target = M5035.M5034.topology_path(
        repair_run, job["event_id"], job["argument_id"]
    )
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    global CURRENT_JOB
    run_directory = M5035.RUNS / arguments.run_id
    config_path = run_directory / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(config_path)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    recorded_script_digest = config["source_files"].get(str(SCRIPT_5035))
    current_script_digest = M5035.file_digest(SCRIPT_5035)
    if recorded_script_digest != current_script_digest:
        raise RuntimeError("5035 production runner changed after the locked run")
    repair_directory = REPAIRS / arguments.repair_id
    repair_run = repair_directory / "scratch_run"
    repair_directory.mkdir(parents=True, exist_ok=True)
    original_directory = repair_directory / "original"
    repaired_directory = repair_directory / "repaired"
    candidates: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
    for path in sorted((run_directory / "jobs").glob("*.json")):
        repairable, job, kernel = repairable_job(run_directory, path)
        if repairable:
            candidates.append((path, job, kernel))
    started = time.monotonic()
    repaired: list[str] = []
    still_unconverged: list[str] = []
    N5030.chamber_residue_catalog = repaired_chamber_residue_catalog
    try:
        for original_job_path, original_job, original_kernel in candidates:
            if time.monotonic() - started >= arguments.max_wall_seconds:
                break
            CURRENT_JOB = original_job["job_key"]
            original_directory.mkdir(parents=True, exist_ok=True)
            M5035.atomic_json(
                original_directory / original_job_path.name, original_job
            )
            M5035.atomic_json(
                original_directory / f"kernel__{original_job_path.name}",
                original_kernel,
            )
            copy_topology(run_directory, repair_run, original_job)
            expected = {
                key: original_job[key]
                for key in (
                    "job_key",
                    "epsilon_id",
                    "evaluation_epsilon",
                    "event_id",
                    "argument_id",
                    "tier",
                )
            }
            result = M5035.execute_job(repair_run, config, expected)
            scratch_kernel_path = repair_run / "kernels" / original_job_path.name
            if result.get("status") != "COMPLETED_CONVERGED":
                still_unconverged.append(original_job["job_key"])
                continue
            repaired_kernel = json.loads(
                scratch_kernel_path.read_text(encoding="utf-8")
            )
            repair_contract = {
                "checkpoint_marker": MARKER,
                "repair_revision": REVISION,
                "repair_script": str(Path(__file__).resolve()),
                "repair_script_sha256": M5035.file_digest(
                    Path(__file__).resolve()
                ),
                "original_job_sha256": M5035.file_digest(original_job_path),
                "original_kernel_sha256": M5035.file_digest(
                    run_directory / "kernels" / original_job_path.name
                ),
                "candidate_fractions": list(CANDIDATE_FRACTIONS),
                "reason": (
                    "the v3 fallback enlarged an unstable local contour; v4 "
                    "shrinks until two nested pole-isolating contours agree"
                ),
                "valid_for_full_MTS_claim": False,
            }
            result["repair_contract"] = repair_contract
            repaired_kernel["repair_contract"] = repair_contract
            repaired_kernel["fixed_event_integral_gate"][
                "relative_residue_revision"
            ] = REVISION
            repaired_directory.mkdir(parents=True, exist_ok=True)
            M5035.atomic_json(repaired_directory / original_job_path.name, result)
            M5035.atomic_json(
                repaired_directory / f"kernel__{original_job_path.name}",
                repaired_kernel,
            )
            M5035.atomic_json(original_job_path, result)
            M5035.atomic_json(
                run_directory / "kernels" / original_job_path.name,
                repaired_kernel,
            )
            repaired.append(original_job["job_key"])
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
    jobs = M5035.load_jobs(run_directory)
    expected_count = len(M5035.expected_jobs(config))
    complete_count = sum(
        M5035.numeric_job(job) for job in jobs.values()
    )
    state = (
        "COMPLETE_WITH_RESIDUE_RADIUS_REPAIR"
        if complete_count == expected_count
        else "REPAIR_INCOMPLETE"
    )
    summary = M5035.build_summary(config, jobs, state)
    M5035.atomic_json(run_directory / "partial_results.json", summary)
    M5035.atomic_json(
        run_directory / "status.json",
        {
            "checkpoint_marker": M5035.MARKER,
            "run_id": config["run_id"],
            "config_digest": config["config_digest"],
            "state": state,
            "elapsed_seconds_this_invocation": time.monotonic() - started,
            "expected_jobs": summary["expected_jobs"],
            "terminal_jobs": summary["terminal_jobs"],
            "remaining_jobs": summary["remaining_jobs"],
            "failed_jobs": summary["failed_jobs"],
            "unconverged_jobs": summary["unconverged_jobs"],
            "updated_at": M5035.utc_now(),
        },
    )
    M5035.write_checkpoint_artifacts(config, summary, run_directory)
    repair_summary = {
        "checkpoint_marker": MARKER,
        "repair_revision": REVISION,
        "run_id": arguments.run_id,
        "repair_id": arguments.repair_id,
        "candidate_jobs": [job["job_key"] for _, job, _ in candidates],
        "repaired_jobs": repaired,
        "still_unconverged_jobs": still_unconverged,
        "remaining_unrepaired_candidates": [
            job["job_key"]
            for _, job, _ in candidates
            if job["job_key"] not in repaired
            and job["job_key"] not in still_unconverged
        ],
        "radius_audit": RADIUS_AUDIT,
        "elapsed_seconds": time.monotonic() - started,
        "resulting_run_state": state,
        "valid_for_full_MTS_claim": False,
    }
    M5035.atomic_json(repair_directory / "repair_summary.json", repair_summary)
    if state.startswith("COMPLETE"):
        M5035.atomic_text(
            run_directory / "COMPLETE",
            json.dumps(
                {
                    "checkpoint_marker": M5035.MARKER,
                    "completed_at": M5035.utc_now(),
                    "repair_marker": MARKER,
                    "failed_jobs": summary["failed_jobs"],
                    "unconverged_jobs": summary["unconverged_jobs"],
                },
                indent=2,
            )
            + "\n",
        )
    print(json.dumps(repair_summary, indent=2, allow_nan=False))
    return repair_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="central_eps008_004_002_s4_v1")
    parser.add_argument("--repair-id", default="pair_local_shrinking_radius_v1")
    parser.add_argument("--max-wall-seconds", type=float, default=3000.0)
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    run(arguments)


if __name__ == "__main__":
    main()
