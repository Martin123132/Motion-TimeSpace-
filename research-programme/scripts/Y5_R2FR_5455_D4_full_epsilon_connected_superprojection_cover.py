from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
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
OUTPUT = FUNCTIONAL_RG / "5455"
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
SCRIPT_5454 = (
    POST / "scripts" / "Y5_R2FR_5454_D4_epsilon_connected_superprojection_smoke.py"
)
RESULT_5454 = (
    FUNCTIONAL_RG / "5454" / "D4_epsilon_connected_superprojection_smoke_result.json"
)
VALIDATION_5454 = FUNCTIONAL_RG / "5454" / "P8_Y5_BRR5452_5454_VALIDATION.csv"
SUPERMANIFEST_5454 = (
    FUNCTIONAL_RG / "5454" / "D4_epsilon_connected_superprojection_manifest.csv"
)
SOURCE_MAP_5454 = (
    FUNCTIONAL_RG / "5454" / "D4_epsilon_connected_superprojection_source_map.csv"
)
SMOKE_WORK_5454 = FUNCTIONAL_RG / "5454" / "work-v1"

DOCUMENT = POST / "5455-Y5-R2FR-D4-full-epsilon-connected-superprojection-cover.md"
SUMMARY = OUTPUT / "D4_full_epsilon_connected_superprojection_summary.csv"
EVENT_BOUNDS = OUTPUT / "D4_full_epsilon_connected_event_bounds.csv"
CERTIFICATE_MAP = OUTPUT / "D4_full_inner_Q_source_projection_certificate_map.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5454_5455_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_full_epsilon_connected_superprojection_cover_result.json"
COMPLETE = OUTPUT / "COMPLETE.json"

CHECKPOINT = 5455
REVISION = "D4-full-epsilon-connected-superprojection-cover-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
NESTED_FIELDS = {"arcs", "x_leaves", "refinement_witnesses", "unresolved"}
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
    "x_lower",
    "x_upper",
    "x_width",
    "source_projection_job_count",
    "source_projection_job_ids",
)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any], compact: bool = False) -> None:
    value = (
        json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n"
        if compact
        else json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n"
    )
    atomic_text(path, value)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    fieldnames = list(rows[0])
    known_fields = set(fieldnames)
    for row in rows[1:]:
        for field in row:
            if field not in known_fields:
                fieldnames.append(field)
                known_fields.add(field)
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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
        SCRIPT_5454,
        RESULT_5454,
        VALIDATION_5454,
        SUPERMANIFEST_5454,
        SOURCE_MAP_5454,
    )


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    return {
        str(path): (path.stat().st_mtime_ns, path.stat().st_size)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def validate_payload(
    payload: dict[str, Any], projection: dict[str, Any], manifest_sha256: str
) -> None:
    job_id = projection["projection_job_id"]
    if payload.get("projection_job_id") != job_id:
        raise RuntimeError(f"work payload id mismatch for {job_id}")
    if payload.get("runner_revision") != REVISION:
        raise RuntimeError(f"stale runner revision for {job_id}")
    if payload.get("supermanifest_sha256") != manifest_sha256:
        raise RuntimeError(f"stale supermanifest digest for {job_id}")
    if payload.get("projection_fingerprint") != projection_fingerprint(projection):
        raise RuntimeError(f"projection fingerprint mismatch for {job_id}")


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
            "supermanifest_sha256": manifest_sha256,
            "projection_fingerprint": projection_fingerprint(projection),
            "correlated_Q_superprojection_passes": passed,
            "source_projection_job_count": int(
                projection["source_projection_job_count"]
            ),
            "source_projection_job_ids": projection["source_projection_job_ids"],
            "superprojection_epsilon_width": float(
                projection["superprojection_epsilon_width"]
            ),
            "seeded_from_checkpoint_5454": seed_path is not None,
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
    for seed_path in sorted(SMOKE_WORK_5454.glob("*.json")):
        payload = read_json(seed_path)
        job_id = payload.get("projection_job_id", "")
        if job_id not in by_id:
            raise RuntimeError(f"5454 smoke output absent from supermanifest: {job_id}")
        projection = by_id[job_id]
        if not payload.get("correlated_Q_projection_smoke_passes"):
            raise RuntimeError(f"5454 smoke seed is not certified: {job_id}")
        for field in ("event_id", "mapped_cell_id"):
            if str(payload[field]) != str(projection[field]):
                raise RuntimeError(f"5454 smoke {field} mismatch for {job_id}")
        for field in ("x_lower", "x_upper", "x_width"):
            expected = float(projection[field])
            actual = float(payload[field])
            if abs(actual - expected) > 1.0e-14 * max(abs(expected), 1.0):
                raise RuntimeError(f"5454 smoke {field} mismatch for {job_id}")
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
    manifest: list[dict[str, str]], completed_ids: set[str], exception_ids: set[str]
) -> list[dict[str, str]]:
    buckets = {
        event_id: sorted(
            (
                row
                for row in manifest
                if row["event_id"] == event_id
                and row["projection_job_id"] not in completed_ids
                and row["projection_job_id"] not in exception_ids
            ),
            key=lambda row: (
                -int(row["source_projection_job_count"]),
                -float(row["superprojection_epsilon_width"]),
                -float(row["x_width"]),
                row["projection_job_id"],
            ),
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


def load_parent_context() -> tuple[Any, Any, Any, Any, Any, Any]:
    module_5452 = load_module("mts_5452_for_5455", SCRIPT_5452)
    module_5450 = module_5452.load_module("mts_5450_for_5455", module_5452.SCRIPT_5450)
    parent = module_5452.load_module("mts_5395_for_5455", module_5450.SCRIPT_5395)
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
    return module_5452, parent, module_5450, references, events, branches


def work_state(
    manifest: list[dict[str, str]],
    by_id: dict[str, dict[str, str]],
    manifest_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    completed: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    for projection in manifest:
        job_id = projection["projection_job_id"]
        completed_path = WORK / f"{job_id}.json"
        exception_path = WORK / f"{job_id}.failed.json"
        if completed_path.is_file() and exception_path.is_file():
            raise RuntimeError(f"both completed and exception payloads exist for {job_id}")
        if completed_path.is_file():
            payload = read_json(completed_path)
            validate_payload(payload, by_id[job_id], manifest_sha256)
            completed.append(payload)
        elif exception_path.is_file():
            payload = read_json(exception_path)
            validate_payload(payload, by_id[job_id], manifest_sha256)
            exceptions.append(payload)
    return completed, exceptions


def event_bound_rows(completed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in completed if row["event_id"] == event_id]
        passing = [row for row in selected if row["correlated_Q_superprojection_passes"]]
        rows.append(
            {
                "event_id": event_id,
                "completed_superprojection_count": len(selected),
                "passed_superprojection_count": len(passing),
                "certified_source_projection_count": sum(
                    int(row["source_projection_job_count"]) for row in passing
                ),
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
    manifest: list[dict[str, str]], completed: list[dict[str, Any]], exception_ids: set[str]
) -> float:
    all_runtimes = [float(row["runtime_seconds"]) for row in completed]
    fallback = statistics.median(all_runtimes) if all_runtimes else math.nan
    medians: dict[str, float] = {}
    for event_id in EVENT_IDS:
        values = [
            float(row["runtime_seconds"])
            for row in completed
            if row["event_id"] == event_id
        ]
        medians[event_id] = statistics.median(values) if values else fallback
    completed_ids = {row["projection_job_id"] for row in completed}
    estimates = [
        medians[row["event_id"]]
        for row in manifest
        if row["projection_job_id"] not in completed_ids
        and row["projection_job_id"] not in exception_ids
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
        "# 5455: D4 full epsilon-connected superprojection cover",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Resume-safe cover",
        "",
        f"The exact checkpoint-5454 source map replaces `{payload['source_projection_job_count']}` repeated slab evaluations with `{payload['total_superprojection_job_count']}` connected superprojections. Completed superprojections: `{payload['completed_superprojection_job_count']}`; certified source projections: `{payload['certified_source_projection_job_count']}`; pending superprojections: `{payload['pending_superprojection_job_count']}`.",
        "",
        f"Every job is atomic and source-locked. The controller imported `{payload['seeded_superprojection_job_count']}` certified checkpoint-5454 smoke jobs and schedules the remainder round-robin across events.",
        "",
        "## Claim boundary",
        "",
        f"Full correlated inner-Q coverage is `{payload['valid_for_correlated_inner_Q_full_cover']}`. Until all source projections are certified, the outer parent atlas, event-local W3, D4 regulator limit, all-operator local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(mode: str, max_jobs: int, max_runtime_hours: float) -> dict[str, Any]:
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5452 = read_json(RESULT_5452)
    result_5454 = read_json(RESULT_5454)
    if result_5452.get("valid_for_correlated_inner_Q_smoke") is not True:
        raise RuntimeError("checkpoint 5452 is not a valid parent smoke")
    if (
        result_5454.get("failed_validation_count") != 0
        or result_5454.get("valid_for_epsilon_connected_superprojection_smoke")
        is not True
    ):
        raise RuntimeError("checkpoint 5454 superprojection smoke is not validated")
    manifest = read_csv(SUPERMANIFEST_5454)
    source_map = read_csv(SOURCE_MAP_5454)
    by_id = {row["projection_job_id"]: row for row in manifest}
    manifest_sha256 = digest(SUPERMANIFEST_5454)
    if len(manifest) != len(by_id):
        raise RuntimeError("supermanifest contains duplicate job ids")
    seeded_this_run = seed_smoke_outputs(by_id, manifest_sha256)
    completed, exceptions = work_state(manifest, by_id, manifest_sha256)
    processed_this_run = 0
    if mode == "full":
        module_5452, parent, module_5450, references, events, branches = (
            load_parent_context()
        )
        completed_ids = {row["projection_job_id"] for row in completed}
        exception_ids = {row["projection_job_id"] for row in exceptions}
        pending = scheduled_pending_rows(manifest, completed_ids, exception_ids)
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
            try:
                payload = module_5452.correlated_projection_job(
                    parent,
                    module_5450,
                    references,
                    events,
                    branches,
                    projection,
                )
                atomic_json(
                    WORK / f"{job_id}.json",
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
                atomic_json(WORK / f"{job_id}.failed.json", failure, compact=True)
            processed_this_run += 1
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "revision": REVISION,
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "last_job_id": job_id,
                    "processed_this_run": processed_this_run,
                },
            )
        completed, exceptions = work_state(manifest, by_id, manifest_sha256)
    failed_certificates = [
        row for row in completed if not row["correlated_Q_superprojection_passes"]
    ]
    passing = [row for row in completed if row["correlated_Q_superprojection_passes"]]
    completed_ids = {row["projection_job_id"] for row in completed}
    exception_ids = {row["projection_job_id"] for row in exceptions}
    pending_count = len(manifest) - len(completed) - len(exceptions)
    certified_ids = [
        source_id
        for row in passing
        for source_id in str(row["source_projection_job_ids"]).split("|")
        if source_id
    ]
    expected_source_ids = [row["source_projection_job_id"] for row in source_map]
    full_source_map_certified = (
        len(certified_ids) == len(set(certified_ids))
        and sorted(certified_ids) == sorted(expected_source_ids)
    )
    all_pass = (
        pending_count == 0
        and not exceptions
        and not failed_certificates
        and full_source_map_certified
    )
    summaries = [
        {key: value for key, value in row.items() if key not in NESTED_FIELDS}
        for row in completed
    ]
    if summaries:
        atomic_csv(SUMMARY, summaries)
    atomic_csv(EVENT_BOUNDS, event_bound_rows(completed))
    certificate_rows: list[dict[str, Any]] = []
    for row in passing:
        for source_id in str(row["source_projection_job_ids"]).split("|"):
            if source_id:
                certificate_rows.append(
                    {
                        "source_projection_job_id": source_id,
                        "certifying_superprojection_job_id": row[
                            "projection_job_id"
                        ],
                        "event_id": row["event_id"],
                        "mapped_cell_id": row["mapped_cell_id"],
                        "maximum_Q_boundary_abs_upper": row[
                            "maximum_Q_boundary_abs_upper"
                        ],
                        "inner_regular_part_abs_upper": row[
                            "inner_regular_part_abs_upper"
                        ],
                        "minimum_denominator_lower": row[
                            "minimum_denominator_lower"
                        ],
                        "valid_for_correlated_inner_Q_full_cover": all_pass,
                        "valid_for_D4_event_local_W3_bound": False,
                        "valid_for_all_operator_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    if certificate_rows:
        atomic_csv(CERTIFICATE_MAP, certificate_rows)
    after_formalization = formalization_snapshot()
    estimated_remaining = runtime_estimate_seconds(manifest, completed, exception_ids)
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "FULL_EPSILON_CONNECTED_INNER_Q_COVER_CERTIFIED__EVALUATE_OUTER_PARENT"
            if all_pass
            else (
                "EPSILON_CONNECTED_INNER_Q_COVER_EXPOSES_FAILURES"
                if exceptions or failed_certificates
                else "EPSILON_CONNECTED_INNER_Q_COVER_RESUME_REQUIRED"
            )
        ),
        "supermanifest_sha256": manifest_sha256,
        "total_superprojection_job_count": len(manifest),
        "completed_superprojection_job_count": len(completed),
        "passed_superprojection_job_count": len(passing),
        "certificate_failure_job_count": len(failed_certificates),
        "exception_job_count": len(exceptions),
        "pending_superprojection_job_count": pending_count,
        "source_projection_job_count": len(expected_source_ids),
        "certified_source_projection_job_count": len(certified_ids),
        "certified_source_projection_unique_id_count": len(set(certified_ids)),
        "full_source_map_certified": full_source_map_certified,
        "processed_this_run": processed_this_run,
        "seeded_superprojection_job_count": sum(
            bool(row.get("seeded_from_checkpoint_5454")) for row in completed
        ),
        "seeded_this_run": seeded_this_run,
        "completed_arc_count": sum(int(row["energy_arc_count"]) for row in completed),
        "completed_x_subleaf_count": sum(int(row["x_subleaf_count"]) for row in completed),
        "refinement_witness_count": sum(
            int(row["refinement_witness_count"]) for row in completed
        ),
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
        "estimated_remaining_runtime_seconds": estimated_remaining,
        "runtime_seconds": time.perf_counter() - started,
        "next_pending_job_id": next(
            (
                row["projection_job_id"]
                for row in scheduled_pending_rows(
                    manifest, completed_ids, exception_ids
                )
            ),
            "",
        ),
        "next_target": (
            "OUTER_PARENT_LEAF_ENCLOSURE"
            if all_pass
            else "RESUME_85_JOB_EPSILON_CONNECTED_INNER_Q_COVER"
        ),
        "valid_for_correlated_inner_Q_full_cover": all_pass,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    width_reconstruction_passes = all(
        float(row["x_width_absolute_error"])
        <= 1.0e-14 * max(float(row["x_width"]), 1.0)
        for row in completed
    )
    arc_matrix_passes = all(
        int(row["energy_arc_count"])
        == int(row["x_subleaf_count"]) * ENERGY_ARC_COUNT
        for row in passing
    )
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5452_parent_smoke_is_valid", result_5452.get("valid_for_correlated_inner_Q_smoke") is True, result_5452.get("decision")),
        check("checkpoint_5454_superprojection_smoke_is_valid", result_5454.get("valid_for_epsilon_connected_superprojection_smoke") is True, result_5454.get("decision")),
        check("supermanifest_has_85_unique_jobs", len(manifest) == 85 and len(manifest) == len(by_id), len(manifest)),
        check("source_map_has_2074_unique_source_jobs", len(expected_source_ids) == 2074 and len(expected_source_ids) == len(set(expected_source_ids)), len(expected_source_ids)),
        check("saved_payload_accounting_reconstructs_supermanifest", len(completed) + len(exceptions) + pending_count == len(manifest), f"{len(completed)}+{len(exceptions)}+{pending_count}"),
        check("completed_x_partitions_reconstruct", width_reconstruction_passes, max((float(row["x_width_absolute_error"]) for row in completed), default=0.0)),
        check("completed_passing_arc_matrices_are_complete", arc_matrix_passes, payload["completed_arc_count"]),
        check("no_exception_markers_are_present", not exceptions, len(exceptions)),
        check("no_completed_superprojection_has_certificate_failure", not failed_certificates, len(failed_certificates)),
        check("certified_source_ids_are_unique", len(certified_ids) == len(set(certified_ids)), f"{len(certified_ids)}/{len(set(certified_ids))}"),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("partial_progress_does_not_promote_full_cover", pending_count == 0 or not payload["valid_for_correlated_inner_Q_full_cover"], f"pending={pending_count}"),
        check("broad_claims_remain_false", not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "inner-Q only"),
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
                "supermanifest_sha256": manifest_sha256,
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
