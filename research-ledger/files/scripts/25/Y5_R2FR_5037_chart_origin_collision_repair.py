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
SCRIPT_5037 = (
    POST / "scripts" / "Y5_R2FR_5037_paired_outer_precision_reflection_control.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUNS = SOURCE / "runs"
REPAIRS = SOURCE / "repairs"
MARKER = "MTS_5037_CHART_ORIGIN_COLLISION_REPAIR"
REVISION = "pair-local-chart-origin-filtered-residue-v5"
CANDIDATE_FRACTIONS = (0.1, 0.05, 0.025, 0.0125, 0.2)
CHART_PAIR_SUFFIXES = {
    frozenset(("plus_u", "minus_u")),
    frozenset(("plus_v", "minus_v")),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5037 = load_module("mts_5037_for_chart_origin_repair", SCRIPT_5037)
M5036 = M5037.M5036
N5030 = M5036.N5030
M5035 = M5036.M5035
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
CURRENT_JOB = ""
EXCLUSION_AUDIT: list[dict[str, Any]] = []
RADIUS_AUDIT: list[dict[str, Any]] = []


def serialized_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def chart_pair(pair: tuple[str, str] | list[str]) -> bool:
    first_source, first_suffix = str(pair[0]).rsplit(":", 1)
    second_source, second_suffix = str(pair[1]).rsplit(":", 1)
    return (
        first_source == second_source
        and frozenset((first_suffix, second_suffix)) in CHART_PAIR_SUFFIXES
    )


def chart_origin_evidence(
    group: dict[str, Any], root: complex
) -> dict[str, Any] | None:
    pairs = [tuple(pair) for pair in group["pairs"]]
    if not pairs or not all(chart_pair(pair) for pair in pairs):
        return None
    rationals = N5030.M5029.root_rationals(
        N5030.SOFT_ENERGY,
        N5030.SOFT_COSINE,
        N5030.DECAY_COSINE,
        N5030.TARGET_COSINE,
    )
    values: dict[str, complex] = {}
    for pair in pairs:
        for label in pair:
            try:
                values[label] = N5030.M5029.rational_value(
                    rationals[label], root
                )
            except (KeyError, ZeroDivisionError, FloatingPointError):
                return None
    maximum_modulus = max(abs(value) for value in values.values())
    if maximum_modulus >= 1.0e-7:
        return None
    return {
        "root": serialized_complex(root),
        "pairs": [list(pair) for pair in pairs],
        "global_factor_roots": {
            label: serialized_complex(value) for label, value in values.items()
        },
        "maximum_global_factor_root_modulus": maximum_modulus,
        "classification": "same-source stereographic chart-origin coalescence",
    }


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
    retained_groups: list[dict[str, Any]] = []
    for group in target_groups:
        root = complex(group["root"])
        required = any(
            abs(root - candidate)
            < 2.0e-5 * max(1.0, abs(root), abs(candidate))
            for candidate in required_roots
        )
        evidence = chart_origin_evidence(group, root)
        if evidence is not None and not required:
            EXCLUSION_AUDIT.append(
                {
                    "job_key": CURRENT_JOB,
                    **evidence,
                    "required_for_homotopy": False,
                    "reason": (
                        "both same-source global factor roots coalesce at the "
                        "stereographic chart origin without a tracked cycle crossing"
                    ),
                }
            )
            continue
        retained_groups.append(group)
    all_roots = [complex(group["root"]) for group in retained_groups]
    selected: list[dict[str, Any]] = []
    for group in retained_groups:
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
                    "pairs": [list(pair) for pair in row["pairs"]],
                    "safe_scale": safe_scale,
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
                "residue": 0.0j if chosen["numerically_zero"] else chosen["inner"],
                "residue_stability": chosen["stability"],
                "numerically_zero": chosen["numerically_zero"],
                "stable": chosen["stable"],
                "included_as_pole_model": row["near_path"]
                and not chosen["numerically_zero"]
                and chosen["stable"],
            }
        )
    return catalog, all_stable


def copy_topology(
    run_directory: Path,
    scratch_run: Path,
    job: dict[str, Any],
) -> None:
    source = M5035.M5034.topology_path(
        run_directory, job["event_id"], job["argument_id"]
    )
    target = M5035.M5034.topology_path(
        scratch_run, job["event_id"], job["argument_id"]
    )
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def repair_candidates(
    run_directory: Path, requested: set[str]
) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((run_directory / "jobs").glob("*.json")):
        job = json.loads(path.read_text(encoding="utf-8"))
        if requested and job["job_key"] not in requested:
            continue
        if job.get("status") not in {"FAILED", "COMPLETED_UNCONVERGED"}:
            continue
        if job.get("status") == "COMPLETED_UNCONVERGED":
            kernel_path = run_directory / "kernels" / path.name
            if not kernel_path.exists():
                continue
            kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
            if kernel["fixed_event_integral_gate"].get("all_residues_stable"):
                continue
        rows.append((path, job))
    return rows


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    global CURRENT_JOB
    run_directory = RUNS / arguments.run_id
    config = json.loads((run_directory / "config.json").read_text(encoding="utf-8"))
    recorded_digest = config["source_files"].get(str(SCRIPT_5037))
    if recorded_digest != M5036.file_digest(SCRIPT_5037):
        raise RuntimeError("5037 production runner changed after its locked run")
    requested = {
        value.strip() for value in arguments.jobs.split(",") if value.strip()
    }
    candidates = repair_candidates(run_directory, requested)
    repair_directory = REPAIRS / arguments.repair_id
    scratch_run = repair_directory / "scratch_run"
    original_directory = repair_directory / "original"
    repaired_directory = repair_directory / "repaired"
    started = time.monotonic()
    repaired: list[str] = []
    still_open: list[dict[str, Any]] = []
    per_job_exclusions: dict[str, list[dict[str, Any]]] = {}
    per_job_radius: dict[str, list[dict[str, Any]]] = {}
    N5030.chamber_residue_catalog = repaired_chamber_residue_catalog
    try:
        for original_path, original_job in candidates:
            if time.monotonic() - started >= arguments.max_wall_seconds:
                break
            CURRENT_JOB = original_job["job_key"]
            EXCLUSION_AUDIT.clear()
            RADIUS_AUDIT.clear()
            original_directory.mkdir(parents=True, exist_ok=True)
            M5036.atomic_json(original_directory / original_path.name, original_job)
            original_kernel_path = run_directory / "kernels" / original_path.name
            if original_kernel_path.exists():
                shutil.copy2(
                    original_kernel_path,
                    original_directory / f"kernel__{original_path.name}",
                )
            copy_topology(run_directory, scratch_run, original_job)
            expected = {
                key: original_job[key]
                for key in (
                    "job_key",
                    "epsilon_id",
                    "evaluation_epsilon",
                    "event_id",
                    "argument_id",
                    "base_argument_id",
                    "tier",
                )
            }
            try:
                result = M5035.execute_job(scratch_run, config, expected)
            except Exception as error:
                still_open.append(
                    {
                        "job_key": CURRENT_JOB,
                        "error_type": type(error).__name__,
                        "error": str(error),
                    }
                )
                continue
            per_job_exclusions[CURRENT_JOB] = list(EXCLUSION_AUDIT)
            per_job_radius[CURRENT_JOB] = list(RADIUS_AUDIT)
            scratch_kernel_path = scratch_run / "kernels" / original_path.name
            if result.get("status") != "COMPLETED_CONVERGED":
                still_open.append(
                    {
                        "job_key": CURRENT_JOB,
                        "status": result.get("status"),
                        "chart_exclusions": len(EXCLUSION_AUDIT),
                        "unstable_radius_rows": len(RADIUS_AUDIT),
                    }
                )
                continue
            repaired_kernel = json.loads(
                scratch_kernel_path.read_text(encoding="utf-8")
            )
            repair_contract = {
                "checkpoint_marker": MARKER,
                "repair_revision": REVISION,
                "repair_script": str(Path(__file__).resolve()),
                "repair_script_sha256": M5036.file_digest(Path(__file__).resolve()),
                "original_job_sha256": M5036.file_digest(original_path),
                "original_kernel_sha256": (
                    M5036.file_digest(original_kernel_path)
                    if original_kernel_path.exists()
                    else None
                ),
                "chart_origin_exclusions": list(EXCLUSION_AUDIT),
                "radius_audit": list(RADIUS_AUDIT),
                "reason": (
                    "remove same-source factor-root coalescences at the global "
                    "stereographic chart origin only when no tracked homotopy "
                    "crossing owns the root"
                ),
                "valid_for_full_MTS_claim": False,
            }
            result["repair_contract"] = repair_contract
            result["residue_radius_contract"] = {
                "revision": REVISION,
                "chart_origin_exclusion_count": len(EXCLUSION_AUDIT),
                "adjustment_count": len(RADIUS_AUDIT),
                "repair_script": str(Path(__file__).resolve()),
                "repair_script_sha256": M5036.file_digest(Path(__file__).resolve()),
                "valid_for_full_MTS_claim": False,
            }
            repaired_kernel["repair_contract"] = repair_contract
            repaired_kernel["residue_radius_contract"] = result[
                "residue_radius_contract"
            ]
            repaired_kernel["fixed_event_integral_gate"][
                "relative_residue_revision"
            ] = REVISION
            repaired_directory.mkdir(parents=True, exist_ok=True)
            M5036.atomic_json(repaired_directory / original_path.name, result)
            M5036.atomic_json(
                repaired_directory / f"kernel__{original_path.name}",
                repaired_kernel,
            )
            M5036.atomic_json(original_path, result)
            M5036.atomic_json(original_kernel_path, repaired_kernel)
            repaired.append(CURRENT_JOB)
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
    jobs = M5036.load_jobs(run_directory)
    expected_count = len(M5036.expected_jobs(config))
    numeric_count = sum(M5036.numeric_job(job) for job in jobs.values())
    state = "PAUSED_AFTER_CHART_ORIGIN_REPAIR"
    summary = M5037.write_augmented_status(
        run_directory, config, jobs, state, started
    )
    M5037.write_checkpoint_artifacts(config, summary, run_directory)
    M5036.append_log(
        run_directory,
        f"chart-origin repair repaired={repaired} still_open={still_open}",
    )
    repair_summary = {
        "checkpoint_marker": MARKER,
        "repair_revision": REVISION,
        "run_id": arguments.run_id,
        "config_digest": config["config_digest"],
        "candidate_jobs": [job["job_key"] for _, job in candidates],
        "repaired_jobs": repaired,
        "still_open": still_open,
        "chart_origin_exclusions": per_job_exclusions,
        "radius_audit": per_job_radius,
        "terminal_jobs": summary["terminal_jobs"],
        "numeric_jobs": numeric_count,
        "expected_jobs": expected_count,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(repair_directory / "repair_summary.json", repair_summary)
    return repair_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="paired_outer_precision_s4_v1")
    parser.add_argument("--repair-id", default="chart_origin_collision_v1")
    parser.add_argument("--jobs", default="")
    parser.add_argument("--max-wall-seconds", type=float, default=2700.0)
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    result = run(arguments)
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "candidate_jobs": result["candidate_jobs"],
                "repaired_jobs": result["repaired_jobs"],
                "still_open": result["still_open"],
                "terminal_jobs": result["terminal_jobs"],
                "numeric_jobs": result["numeric_jobs"],
                "expected_jobs": result["expected_jobs"],
                "valid_for_full_MTS_claim": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
