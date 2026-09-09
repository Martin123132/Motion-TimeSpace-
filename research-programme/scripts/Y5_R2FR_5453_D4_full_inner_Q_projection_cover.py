from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(variable, "1")


POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5453"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5452 = (
    POST
    / "scripts"
    / "Y5_R2FR_5452_D4_inner_Q_projection_manifest_and_correlated_smoke.py"
)
RESULT_5452 = (
    FUNCTIONAL_RG / "5452" / "D4_inner_Q_projection_smoke_result.json"
)
VALIDATION_5452 = FUNCTIONAL_RG / "5452" / "P8_Y5_BRR5450_5452_VALIDATION.csv"
SOURCES_5452 = FUNCTIONAL_RG / "5452" / "source_register.csv"
MANIFEST_5452 = (
    FUNCTIONAL_RG / "5452" / "D4_inner_Q_x_epsilon_projection_manifest.csv"
)
SMOKE_WORK_5452 = FUNCTIONAL_RG / "5452" / "work-v2"

DOCUMENT = POST / "5453-Y5-R2FR-D4-full-inner-Q-projection-cover.md"
SUMMARY = OUTPUT / "D4_full_inner_Q_projection_summary.csv"
EVENT_BOUNDS = OUTPUT / "D4_full_inner_Q_event_bounds.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5452_5453_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_full_inner_Q_projection_cover_result.json"
COMPLETE = OUTPUT / "COMPLETE.json"

CHECKPOINT = 5453
REVISION = "D4-full-inner-Q-projection-cover-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
FINGERPRINT_FIELDS = (
    "projection_job_id",
    "event_id",
    "mapped_cell_id",
    "epsilon_bin_index",
    "epsilon_subdivision_index",
    "epsilon_subdivision_count",
    "epsilon_real_lower",
    "epsilon_real_upper",
    "epsilon_imaginary_lower",
    "epsilon_imaginary_upper",
    "x_component_index",
    "x_component_count",
    "x_lower",
    "x_upper",
    "x_width",
    "source_inner_leaf_count",
)
NESTED_FIELDS = {"arcs", "x_leaves", "refinement_witnesses", "unresolved"}


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any], compact: bool = False) -> None:
    if compact:
        value = json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n"
    else:
        value = json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n"
    atomic_text(path, value)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def projection_fingerprint(row: dict[str, Any]) -> str:
    encoded = json.dumps(
        {field: str(row[field]) for field in FINGERPRINT_FIELDS},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5452,
        RESULT_5452,
        VALIDATION_5452,
        SOURCES_5452,
        MANIFEST_5452,
    )


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    return {
        str(path): (path.stat().st_mtime_ns, path.stat().st_size)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def load_manifest() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], str]:
    rows = read_csv(MANIFEST_5452)
    by_id = {row["projection_job_id"]: row for row in rows}
    if len(rows) != len(by_id):
        raise RuntimeError("checkpoint-5452 manifest contains duplicate job ids")
    return rows, by_id, digest(MANIFEST_5452)


def validate_payload(
    payload: dict[str, Any],
    projection: dict[str, Any],
    manifest_sha256: str,
) -> None:
    expected_id = projection["projection_job_id"]
    if payload.get("projection_job_id") != expected_id:
        raise RuntimeError(f"work payload id mismatch for {expected_id}")
    if payload.get("runner_revision") != REVISION:
        raise RuntimeError(f"stale runner revision for {expected_id}")
    if payload.get("manifest_sha256") != manifest_sha256:
        raise RuntimeError(f"stale manifest digest for {expected_id}")
    if payload.get("projection_fingerprint") != projection_fingerprint(projection):
        raise RuntimeError(f"projection fingerprint mismatch for {expected_id}")


def normalize_payload(
    payload: dict[str, Any],
    projection: dict[str, Any],
    manifest_sha256: str,
    seed_path: Path | None,
) -> dict[str, Any]:
    normalized = dict(payload)
    passed = bool(normalized.get("correlated_Q_projection_smoke_passes"))
    normalized.update(
        {
            "checkpoint": CHECKPOINT,
            "runner_revision": REVISION,
            "manifest_sha256": manifest_sha256,
            "projection_fingerprint": projection_fingerprint(projection),
            "correlated_Q_projection_passes": passed,
            "seeded_from_checkpoint_5452": seed_path is not None,
            "seed_source_path": str(seed_path.resolve()) if seed_path else "",
            "seed_source_sha256": digest(seed_path) if seed_path else "",
            "valid_for_correlated_inner_Q_full_cover": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    return normalized


def seed_smoke_outputs(
    by_id: dict[str, dict[str, str]], manifest_sha256: str
) -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    seeded = 0
    for seed_path in sorted(SMOKE_WORK_5452.glob("*.json")):
        payload = read_json(seed_path)
        job_id = payload.get("projection_job_id", "")
        if job_id not in by_id:
            raise RuntimeError(f"5452 smoke output is absent from manifest: {job_id}")
        projection = by_id[job_id]
        for field in ("event_id", "mapped_cell_id"):
            if str(payload[field]) != str(projection[field]):
                raise RuntimeError(f"5452 smoke {field} mismatch for {job_id}")
        for field in ("x_lower", "x_upper", "x_width"):
            expected = float(projection[field])
            actual = float(payload[field])
            if abs(actual - expected) > 1.0e-14 * max(abs(expected), 1.0):
                raise RuntimeError(f"5452 smoke {field} mismatch for {job_id}")
        if not payload.get("correlated_Q_projection_smoke_passes"):
            raise RuntimeError(f"5452 smoke seed is not certified: {job_id}")
        target = WORK / f"{job_id}.json"
        if target.is_file():
            validate_payload(read_json(target), projection, manifest_sha256)
            continue
        atomic_json(
            target,
            normalize_payload(payload, projection, manifest_sha256, seed_path),
            compact=True,
        )
        seeded += 1
    return seeded


def scheduled_pending_rows(
    manifest: list[dict[str, str]], completed_ids: set[str], failed_ids: set[str]
) -> list[dict[str, str]]:
    buckets = {
        event_id: sorted(
            (
                row
                for row in manifest
                if row["event_id"] == event_id
                and row["projection_job_id"] not in completed_ids
                and row["projection_job_id"] not in failed_ids
            ),
            key=lambda row: (-float(row["x_width"]), row["projection_job_id"]),
        )
        for event_id in EVENT_IDS
    }
    scheduled: list[dict[str, str]] = []
    offset = 0
    while any(offset < len(buckets[event_id]) for event_id in EVENT_IDS):
        for event_id in EVENT_IDS:
            if offset < len(buckets[event_id]):
                scheduled.append(buckets[event_id][offset])
        offset += 1
    return scheduled


def load_parent_context(module_5452: Any) -> tuple[Any, Any, Any, Any, Any]:
    module_5450 = module_5452.load_module("mts_5450_for_5453", module_5452.SCRIPT_5450)
    parent = module_5452.load_module("mts_5395_for_5453", module_5450.SCRIPT_5395)
    parent.set_below_normal_priority()
    parent.M5386.iv.dps = parent.M5386.INTERVAL_DIGITS
    module_5450.ratio_coordinate_bounds = lambda _parent, row: (
        float(row["custom_x_lower"]),
        float(row["custom_x_upper"]),
    )
    references, _ = parent.M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {
        row["event_id"]: row for row in module_5450.read_csv(module_5450.EVENTS)
    }
    branches = module_5450.event_branch_map()
    return parent, module_5450, references, events, branches


def work_state(
    manifest: list[dict[str, str]],
    by_id: dict[str, dict[str, str]],
    manifest_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    completed: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for projection in manifest:
        job_id = projection["projection_job_id"]
        completed_path = WORK / f"{job_id}.json"
        failed_path = WORK / f"{job_id}.failed.json"
        if completed_path.is_file() and failed_path.is_file():
            raise RuntimeError(f"both completed and failed payloads exist for {job_id}")
        if completed_path.is_file():
            payload = read_json(completed_path)
            validate_payload(payload, by_id[job_id], manifest_sha256)
            completed.append(payload)
        elif failed_path.is_file():
            payload = read_json(failed_path)
            validate_payload(payload, by_id[job_id], manifest_sha256)
            failures.append(payload)
    return completed, failures


def event_bound_rows(completed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in completed if row["event_id"] == event_id]
        passing = [row for row in selected if row["correlated_Q_projection_passes"]]
        rows.append(
            {
                "event_id": event_id,
                "completed_projection_count": len(selected),
                "passed_projection_count": len(passing),
                "failed_projection_count": len(selected) - len(passing),
                "maximum_Q_boundary_abs_upper": max(
                    (float(row["maximum_Q_boundary_abs_upper"]) for row in passing),
                    default=math.nan,
                ),
                "maximum_inner_regular_part_abs_upper": max(
                    (float(row["inner_regular_part_abs_upper"]) for row in passing),
                    default=math.nan,
                ),
                "minimum_denominator_lower": min(
                    (float(row["minimum_denominator_lower"]) for row in passing),
                    default=math.nan,
                ),
                "maximum_x_refinement_depth": max(
                    (int(row["maximum_x_refinement_depth"]) for row in passing),
                    default=-1,
                ),
                "valid_for_correlated_inner_Q_full_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def runtime_estimate_seconds(
    manifest: list[dict[str, str]], completed: list[dict[str, Any]], failed_ids: set[str]
) -> float:
    medians: dict[str, float] = {}
    all_runtimes = [
        float(row["runtime_seconds"])
        for row in completed
        if math.isfinite(float(row["runtime_seconds"]))
    ]
    fallback = statistics.median(all_runtimes) if all_runtimes else math.nan
    for event_id in EVENT_IDS:
        values = [
            float(row["runtime_seconds"])
            for row in completed
            if row["event_id"] == event_id
            and math.isfinite(float(row["runtime_seconds"]))
        ]
        medians[event_id] = statistics.median(values) if values else fallback
    completed_ids = {row["projection_job_id"] for row in completed}
    estimates = [
        medians[row["event_id"]]
        for row in manifest
        if row["projection_job_id"] not in completed_ids
        and row["projection_job_id"] not in failed_ids
    ]
    return sum(estimates) if estimates and all(math.isfinite(x) for x in estimates) else math.nan


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5453: D4 full inner-Q projection cover",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Resume-safe cover",
        "",
        f"The exact checkpoint-5452 adaptive x evaluator is now scheduled over all `{payload['total_projection_job_count']}` source-locked manifest rows. Each projection is written atomically before the next begins. Completed projections: `{payload['completed_projection_job_count']}`; pending: `{payload['pending_projection_job_count']}`; exception markers: `{payload['exception_job_count']}`.",
        "",
        f"The controller imported `{payload['seeded_projection_job_count']}` already-certified checkpoint-5452 smoke outputs without recomputation. Remaining work is interleaved across all eight events and ordered widest-first within each event, so a new branch-specific obstruction is exposed early rather than after a complete easy-event sweep.",
        "",
        "## Claim boundary",
        "",
        f"Full correlated inner-Q coverage is `{payload['valid_for_correlated_inner_Q_full_cover']}`. Partial progress never promotes this flag. The outer parent atlas, event-local W3, combined W3, regulator limit, all-operator local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(mode: str, max_jobs: int, max_runtime_hours: float) -> dict[str, Any]:
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5452 = read_json(RESULT_5452)
    if (
        result_5452.get("failed_validation_count") != 0
        or result_5452.get("valid_for_correlated_inner_Q_smoke") is not True
    ):
        raise RuntimeError("checkpoint 5452 correlated smoke is not validated")
    manifest, by_id, manifest_sha256 = load_manifest()
    expected_count = int(result_5452["projection_job_count"])
    if len(manifest) != expected_count:
        raise RuntimeError(f"manifest count mismatch: {len(manifest)}/{expected_count}")
    seeded_this_run = seed_smoke_outputs(by_id, manifest_sha256)
    completed, failures = work_state(manifest, by_id, manifest_sha256)
    processed_this_run = 0
    if mode == "full":
        module_5452 = __import__("importlib.util").util.spec_from_file_location(
            "mts_5452_for_5453", SCRIPT_5452
        )
        if module_5452 is None or module_5452.loader is None:
            raise ImportError(f"cannot load {SCRIPT_5452}")
        loaded_5452 = __import__("importlib.util").util.module_from_spec(module_5452)
        module_5452.loader.exec_module(loaded_5452)
        parent, module_5450, references, events, branches = load_parent_context(
            loaded_5452
        )
        completed_ids = {row["projection_job_id"] for row in completed}
        failed_ids = {row["projection_job_id"] for row in failures}
        pending = scheduled_pending_rows(manifest, completed_ids, failed_ids)
        deadline = (
            time.perf_counter() + max_runtime_hours * 3600.0
            if max_runtime_hours > 0.0
            else math.inf
        )
        for projection in pending:
            if max_jobs > 0 and processed_this_run >= max_jobs:
                break
            if processed_this_run > 0 and time.perf_counter() >= deadline:
                break
            job_id = projection["projection_job_id"]
            completed_path = WORK / f"{job_id}.json"
            failed_path = WORK / f"{job_id}.failed.json"
            try:
                payload = loaded_5452.correlated_projection_job(
                    parent,
                    module_5450,
                    references,
                    events,
                    branches,
                    projection,
                )
                atomic_json(
                    completed_path,
                    normalize_payload(payload, projection, manifest_sha256, None),
                    compact=True,
                )
            except Exception as error:
                failure = normalize_payload(
                    {
                        "projection_job_id": job_id,
                        "event_id": projection["event_id"],
                        "mapped_cell_id": projection["mapped_cell_id"],
                        "runtime_seconds": 0.0,
                        "correlated_Q_projection_smoke_passes": False,
                        "failure_type": type(error).__name__,
                        "failure_message": str(error).splitlines()[0][:1000],
                    },
                    projection,
                    manifest_sha256,
                    None,
                )
                atomic_json(failed_path, failure, compact=True)
            processed_this_run += 1
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "revision": REVISION,
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "last_job_id": job_id,
                    "processed_this_run": processed_this_run,
                    "message": "job output committed atomically",
                },
            )
        completed, failures = work_state(manifest, by_id, manifest_sha256)
    failed_certificates = [
        row for row in completed if not row["correlated_Q_projection_passes"]
    ]
    completed_ids = {row["projection_job_id"] for row in completed}
    failed_ids = {row["projection_job_id"] for row in failures}
    pending_count = len(manifest) - len(completed) - len(failures)
    all_complete = pending_count == 0 and not failures
    all_pass = all_complete and not failed_certificates
    summaries = [
        {key: value for key, value in row.items() if key not in NESTED_FIELDS}
        for row in completed
    ]
    if summaries:
        atomic_csv(SUMMARY, summaries)
    bounds = event_bound_rows(completed)
    atomic_csv(EVENT_BOUNDS, bounds)
    after_formalization = formalization_snapshot()
    formalization_unchanged = before_formalization == after_formalization
    estimated_remaining = runtime_estimate_seconds(manifest, completed, failed_ids)
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "FULL_CORRELATED_INNER_Q_PROJECTION_COVER_CERTIFIED__EVALUATE_OUTER_PARENT"
            if all_pass
            else (
                "CORRELATED_INNER_Q_PROJECTION_COVER_EXPOSES_FAILURES"
                if failures or failed_certificates
                else "CORRELATED_INNER_Q_PROJECTION_COVER_RESUME_REQUIRED"
            )
        ),
        "manifest_sha256": manifest_sha256,
        "total_projection_job_count": len(manifest),
        "completed_projection_job_count": len(completed),
        "passed_projection_job_count": len(completed) - len(failed_certificates),
        "certificate_failure_job_count": len(failed_certificates),
        "exception_job_count": len(failures),
        "pending_projection_job_count": pending_count,
        "processed_this_run": processed_this_run,
        "seeded_projection_job_count": sum(
            bool(row.get("seeded_from_checkpoint_5452")) for row in completed
        ),
        "seeded_this_run": seeded_this_run,
        "completed_arc_count": sum(int(row["energy_arc_count"]) for row in completed),
        "completed_x_subleaf_count": sum(int(row["x_subleaf_count"]) for row in completed),
        "refinement_witness_count": sum(
            int(row["refinement_witness_count"]) for row in completed
        ),
        "maximum_Q_boundary_abs_upper": max(
            (
                float(row["maximum_Q_boundary_abs_upper"])
                for row in completed
                if row["correlated_Q_projection_passes"]
            ),
            default=math.nan,
        ),
        "maximum_inner_regular_part_abs_upper": max(
            (
                float(row["inner_regular_part_abs_upper"])
                for row in completed
                if row["correlated_Q_projection_passes"]
            ),
            default=math.nan,
        ),
        "minimum_denominator_lower": min(
            (
                float(row["minimum_denominator_lower"])
                for row in completed
                if row["correlated_Q_projection_passes"]
            ),
            default=math.nan,
        ),
        "estimated_remaining_runtime_seconds": estimated_remaining,
        "runtime_seconds": time.perf_counter() - started,
        "next_pending_job_id": next(
            (
                row["projection_job_id"]
                for row in scheduled_pending_rows(manifest, completed_ids, failed_ids)
            ),
            "",
        ),
        "next_target": (
            "OUTER_PARENT_LEAF_ENCLOSURE"
            if all_pass
            else "RESUME_FULL_CORRELATED_INNER_Q_PROJECTION_COVER"
        ),
        "valid_for_correlated_inner_Q_full_cover": all_pass,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    width_tolerance_passes = all(
        float(row["x_width_absolute_error"])
        <= 1.0e-14 * max(float(row["x_width"]), 1.0)
        for row in completed
    )
    arc_matrix_passes = all(
        int(row["energy_arc_count"])
        == int(row["x_subleaf_count"]) * ENERGY_ARC_COUNT
        for row in completed
        if row["correlated_Q_projection_passes"]
    )
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5452_smoke_is_valid",
            result_5452.get("valid_for_correlated_inner_Q_smoke") is True,
            result_5452.get("decision"),
        ),
        check("manifest_count_matches_5452", len(manifest) == expected_count, f"{len(manifest)}/{expected_count}"),
        check("manifest_job_ids_are_unique", len(manifest) == len(by_id), len(by_id)),
        check("all_saved_payloads_match_revision_and_manifest", len(completed) + len(failures) + pending_count == len(manifest), len(completed) + len(failures)),
        check("completed_x_partitions_reconstruct_projection_widths", width_tolerance_passes, max((float(row["x_width_absolute_error"]) for row in completed), default=0.0)),
        check("completed_passing_arc_matrices_are_complete", arc_matrix_passes, payload["completed_arc_count"]),
        check("no_exception_markers_are_present", not failures, len(failures)),
        check("no_completed_projection_has_unresolved_certificate_failure", not failed_certificates, len(failed_certificates)),
        check("formalization_workbench_untouched", formalization_unchanged, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "inner-Q only"),
        check("partial_progress_does_not_promote_full_cover", all_complete or not payload["valid_for_correlated_inner_Q_full_cover"], f"pending={pending_count}"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    if all_pass and payload["failed_validation_count"] == 0:
        atomic_json(
            COMPLETE,
            {
                "checkpoint": CHECKPOINT,
                "revision": REVISION,
                "completed_utc": datetime.now(timezone.utc).isoformat(),
                "decision": payload["decision"],
                "manifest_sha256": manifest_sha256,
            },
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("status", "full"), default="status")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--max-runtime-hours", type=float, default=0.0)
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    if arguments.max_runtime_hours < 0.0:
        raise ValueError("--max-runtime-hours must be nonnegative")
    payload = run(arguments.mode, arguments.max_jobs, arguments.max_runtime_hours)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
