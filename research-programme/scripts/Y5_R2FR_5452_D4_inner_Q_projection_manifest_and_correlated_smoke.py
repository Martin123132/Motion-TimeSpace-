from __future__ import annotations

import argparse
import csv
import ctypes
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5452"
WORK = OUTPUT / "work-v2"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5450 = (
    SCRIPTS
    / "Y5_R2FR_5450_D4_event_endpoint_Cauchy_subtraction_and_correlated_probe.py"
)
SCRIPT_5451 = (
    SCRIPTS / "Y5_R2FR_5451_D4_event_endpoint_xt_overlap_geometry_cover.py"
)
COVER_5451 = FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_cover.csv"
RESULT_5451 = (
    FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_geometry_result.json"
)
THEOREM_5450 = FUNCTIONAL_RG / "5450" / "D4_event_endpoint_Cauchy_subtraction_bounds.csv"
RESULT_5450 = FUNCTIONAL_RG / "5450" / "D4_event_endpoint_Cauchy_subtraction_result.json"

DOCUMENT = POST / "5452-Y5-R2FR-D4-inner-Q-projection-manifest-and-correlated-smoke.md"
MANIFEST = OUTPUT / "D4_inner_Q_x_epsilon_projection_manifest.csv"
SMOKE_SUMMARY = OUTPUT / "D4_inner_Q_correlated_smoke_summary.csv"
SMOKE_ARCS = OUTPUT / "D4_inner_Q_correlated_smoke_arcs.csv"
SMOKE_X_LEAVES = OUTPUT / "D4_inner_Q_correlated_smoke_x_leaves.csv"
SMOKE_REFINEMENT = OUTPUT / "D4_inner_Q_correlated_smoke_refinement_witnesses.csv"
SOURCES = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5450_5452_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_inner_Q_projection_smoke_result.json"

CHECKPOINT = 5452
REVISION = "D4-inner-Q-projection-manifest-correlated-smoke-v2"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
ENERGY_CONTOUR_RADIUS = 1.0e-5
INNER_RADIUS = 7.5e-6
MERGE_TOLERANCE = 1.0e-15
MAXIMUM_X_REFINEMENT_DEPTH = 10
MINIMUM_X_WIDTH = 1.0e-10


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def compact_job_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5450,
        SCRIPT_5451,
        COVER_5451,
        RESULT_5451,
        THEOREM_5450,
        RESULT_5450,
    )


def manifest_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str, int, int, int], dict[str, Any]] = {}
    inner_leaf_count = 0
    with COVER_5451.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["cover_owner"] != "INNER_CAUCHY_REGULAR_PART":
                continue
            inner_leaf_count += 1
            key = (
                row["event_id"],
                row["mapped_cell_id"],
                int(row["epsilon_bin_index"]),
                int(row["epsilon_subdivision_index"]),
                int(row["epsilon_subdivision_count"]),
            )
            group = groups.setdefault(
                key,
                {
                    "intervals": [],
                    "leaf_count": 0,
                    "epsilon_real_lower": float(row["epsilon_real_lower"]),
                    "epsilon_real_upper": float(row["epsilon_real_upper"]),
                    "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
                    "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
                    "path_segments": set(),
                },
            )
            epsilon_values = (
                float(row["epsilon_real_lower"]),
                float(row["epsilon_real_upper"]),
                float(row["epsilon_imaginary_lower"]),
                float(row["epsilon_imaginary_upper"]),
            )
            declared_values = (
                group["epsilon_real_lower"],
                group["epsilon_real_upper"],
                group["epsilon_imaginary_lower"],
                group["epsilon_imaginary_upper"],
            )
            if epsilon_values != declared_values:
                raise RuntimeError(f"inconsistent epsilon box in inner group {key}")
            group["intervals"].append(
                (float(row["x_lower"]), float(row["x_upper"]))
            )
            group["leaf_count"] += 1
            group["path_segments"].add(row["path_segment"])
    rows: list[dict[str, Any]] = []
    maximum_components = 0
    for key, group in sorted(groups.items()):
        event_id, cell_id, epsilon_bin, subdivision_index, subdivision_count = key
        intervals = sorted(group["intervals"])
        merged: list[list[float]] = []
        for lower, upper in intervals:
            if merged and lower <= merged[-1][1] + MERGE_TOLERANCE:
                merged[-1][1] = max(merged[-1][1], upper)
            else:
                merged.append([lower, upper])
        maximum_components = max(maximum_components, len(merged))
        epsilon_label = str(epsilon_bin).replace("-", "m")
        for component_index, (x_lower, x_upper) in enumerate(merged):
            job_id = (
                f"{event_id}__{cell_id}__e{epsilon_label}__"
                f"s{subdivision_index:04d}of{subdivision_count:04d}__"
                f"x{component_index:02d}"
            )
            rows.append(
                {
                    "projection_job_id": job_id,
                    "event_id": event_id,
                    "mapped_cell_id": cell_id,
                    "epsilon_bin_index": epsilon_bin,
                    "epsilon_subdivision_index": subdivision_index,
                    "epsilon_subdivision_count": subdivision_count,
                    "epsilon_real_lower": group["epsilon_real_lower"],
                    "epsilon_real_upper": group["epsilon_real_upper"],
                    "epsilon_imaginary_lower": group["epsilon_imaginary_lower"],
                    "epsilon_imaginary_upper": group["epsilon_imaginary_upper"],
                    "x_component_index": component_index,
                    "x_component_count": len(merged),
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "x_width": x_upper - x_lower,
                    "source_inner_leaf_count": group["leaf_count"],
                    "source_path_segments": "|".join(sorted(group["path_segments"])),
                    "Q_energy_contour_radius": ENERGY_CONTOUR_RADIUS,
                    "inner_radius": INNER_RADIUS,
                    "status": "PENDING_CORRELATED_Q_ENCLOSURE",
                    "valid_for_correlated_inner_Q_full_cover": False,
                    "valid_for_full_event_cell_finite_cover": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    diagnostics = {
        "inner_leaf_count": inner_leaf_count,
        "epsilon_group_count": len(groups),
        "projection_job_count": len(rows),
        "maximum_x_component_count_per_epsilon_group": maximum_components,
    }
    return rows, diagnostics


def representative_smoke_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    representatives: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in manifest if row["event_id"] == event_id]
        if not selected:
            raise RuntimeError(f"no inner-Q projection for {event_id}")
        representatives.append(
            max(
                selected,
                key=lambda row: (
                    float(row["x_width"]),
                    int(row["source_inner_leaf_count"]),
                ),
            )
        )
    return representatives


def correlated_projection_job(
    parent: Any,
    module_5450: Any,
    references: Any,
    events: dict[str, dict[str, str]],
    branches: dict[str, dict[str, str]],
    projection: dict[str, Any],
) -> dict[str, Any]:
    started = time.perf_counter()
    event_id = projection["event_id"]
    stack = [
        (
            float(projection["x_lower"]),
            float(projection["x_upper"]),
            0,
            "R",
        )
    ]
    arcs: list[dict[str, Any]] = []
    x_leaves: list[dict[str, Any]] = []
    refinement_witnesses: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    while stack:
        x_lower, x_upper, depth, refinement_path = stack.pop()
        ratio_row = {
            "epsilon_bin_index": str(projection["epsilon_bin_index"]),
            "epsilon_real_lower": str(projection["epsilon_real_lower"]),
            "epsilon_real_upper": str(projection["epsilon_real_upper"]),
            "epsilon_imaginary_lower": str(projection["epsilon_imaginary_lower"]),
            "epsilon_imaginary_upper": str(projection["epsilon_imaginary_upper"]),
            "custom_x_lower": str(x_lower),
            "custom_x_upper": str(x_upper),
        }
        node_arcs: list[dict[str, Any]] = []
        failed_arc: dict[str, Any] | None = None
        for arc_index in range(ENERGY_ARC_COUNT):
            arc = module_5450.correlated_arc_probe(
                parent,
                references,
                events[event_id],
                branches[event_id],
                ratio_row,
                arc_index,
            )
            arc.update(
                {
                    "projection_job_id": projection["projection_job_id"],
                    "mapped_cell_id": projection["mapped_cell_id"],
                    "epsilon_subdivision_index": projection[
                        "epsilon_subdivision_index"
                    ],
                    "epsilon_subdivision_count": projection[
                        "epsilon_subdivision_count"
                    ],
                    "x_component_index": projection["x_component_index"],
                    "x_subleaf_lower": x_lower,
                    "x_subleaf_upper": x_upper,
                    "x_refinement_depth": depth,
                    "x_refinement_path": refinement_path,
                }
            )
            if not arc["probe_passed"]:
                failed_arc = arc
                break
            node_arcs.append(arc)
        if failed_arc is not None:
            refinement_witnesses.append(failed_arc)
            x_width = x_upper - x_lower
            if depth >= MAXIMUM_X_REFINEMENT_DEPTH or x_width <= MINIMUM_X_WIDTH:
                unresolved.append(
                    {
                        "projection_job_id": projection["projection_job_id"],
                        "event_id": event_id,
                        "x_lower": x_lower,
                        "x_upper": x_upper,
                        "x_width": x_width,
                        "x_refinement_depth": depth,
                        "x_refinement_path": refinement_path,
                        "failure_type": failed_arc["failure_type"],
                        "failure_message": failed_arc["failure_message"],
                    }
                )
                continue
            midpoint = 0.5 * (x_lower + x_upper)
            stack.append((midpoint, x_upper, depth + 1, refinement_path + "R"))
            stack.append((x_lower, midpoint, depth + 1, refinement_path + "L"))
            continue
        leaf_maximum_Q = max(
            float(row["event_integrand_abs_upper_without_physical_multiplier"])
            for row in node_arcs
        )
        leaf_minimum_denominator = min(
            float(row["minimum_denominator_lower"]) for row in node_arcs
        )
        x_leaves.append(
            {
                "projection_job_id": projection["projection_job_id"],
                "event_id": event_id,
                "mapped_cell_id": projection["mapped_cell_id"],
                "x_lower": x_lower,
                "x_upper": x_upper,
                "x_width": x_upper - x_lower,
                "x_refinement_depth": depth,
                "x_refinement_path": refinement_path,
                "energy_arc_count": len(node_arcs),
                "maximum_Q_boundary_abs_upper": leaf_maximum_Q,
                "minimum_denominator_lower": leaf_minimum_denominator,
                "x_leaf_correlated_Q_passes": len(node_arcs) == ENERGY_ARC_COUNT,
                "valid_for_correlated_inner_Q_full_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        arcs.extend(node_arcs)
    all_pass = (
        not unresolved
        and bool(x_leaves)
        and len(arcs) == len(x_leaves) * ENERGY_ARC_COUNT
        and all(row["probe_passed"] for row in arcs)
    )
    maximum_Q = max(
        (
            float(row["event_integrand_abs_upper_without_physical_multiplier"])
            for row in arcs
        ),
        default=math.nan,
    )
    covered_x_width = sum(float(row["x_width"]) for row in x_leaves)
    expected_x_width = float(projection["x_width"])
    return {
        "projection_job_id": projection["projection_job_id"],
        "event_id": event_id,
        "mapped_cell_id": projection["mapped_cell_id"],
        "epsilon_bin_index": projection["epsilon_bin_index"],
        "epsilon_subdivision_index": projection["epsilon_subdivision_index"],
        "epsilon_subdivision_count": projection["epsilon_subdivision_count"],
        "x_lower": projection["x_lower"],
        "x_upper": projection["x_upper"],
        "x_width": projection["x_width"],
        "source_inner_leaf_count": projection["source_inner_leaf_count"],
        "x_subleaf_count": len(x_leaves),
        "maximum_x_refinement_depth": max(
            (int(row["x_refinement_depth"]) for row in x_leaves),
            default=-1,
        ),
        "covered_x_width": covered_x_width,
        "x_width_absolute_error": abs(covered_x_width - expected_x_width),
        "energy_arc_count": len(arcs),
        "passed_arc_count": sum(row["probe_passed"] for row in arcs),
        "failed_arc_count": len(unresolved),
        "refinement_witness_count": len(refinement_witnesses),
        "maximum_Q_boundary_abs_upper": maximum_Q,
        "inner_regular_part_abs_upper": (
            maximum_Q / (ENERGY_CONTOUR_RADIUS - INNER_RADIUS)
            if all_pass and math.isfinite(maximum_Q)
            else math.nan
        ),
        "minimum_denominator_lower": min(
            (float(row["minimum_denominator_lower"]) for row in arcs),
            default=math.nan,
        ),
        "refined_failure_classes": sorted(
            {
                row["failure_type"] or "FAILED_GATE"
                for row in refinement_witnesses
            }
        ),
        "unresolved_failure_classes": sorted(
            {row["failure_type"] for row in unresolved}
        ),
        "runtime_seconds": time.perf_counter() - started,
        "correlated_Q_projection_smoke_passes": all_pass,
        "valid_for_correlated_inner_Q_full_cover": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "arcs": arcs,
        "x_leaves": x_leaves,
        "refinement_witnesses": refinement_witnesses,
        "unresolved": unresolved,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5452: D4 inner-Q projection manifest and correlated smoke",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Exact reduction",
        "",
        "The inner Cauchy bound depends on `(x,epsilon)` and the fixed `|delta|=1e-5` circle, not on the connector/top path parameter `t`. The 64,732 inner geometry leaves can therefore be projected and merged before the expensive parent amplitude call. The projection is lossless because every source leaf retains its full epsilon box and the union of its x interval.",
        "",
        f"The complete 5451 atlas reduces to `{payload['projection_job_count']}` inner `x×epsilon` jobs across `{payload['epsilon_group_count']}` epsilon groups. Maximum connected x components per group is `{payload['maximum_x_component_count_per_epsilon_group']}`.",
        "",
        "## Correlated smoke",
        "",
        f"One widest projection per event was sent through all 32 exact 5450 parent `Q` arcs. A node that failed an interval chart was bisected only in `x`; every accepted x leaf then had to pass all 32 arcs. Passed projections: `{payload['passed_smoke_job_count']}/{payload['smoke_job_count']}` across `{payload['smoke_x_subleaf_count']}` accepted x leaves.",
        "",
        "## Claim boundary",
        "",
        "This checkpoint validates the compression and a cross-event transplant of the exact parent contour. It does not yet evaluate all projection jobs. Full correlated inner-Q coverage, the outer parent amplitude atlas, event-local W3, combined W3, the D4 regulator limit, all-operator local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(mode: str, max_jobs: int) -> dict[str, Any]:
    set_below_normal_priority()
    started_utc = datetime.now(timezone.utc)
    started = time.perf_counter()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5450 = read_json(RESULT_5450)
    result_5451 = read_json(RESULT_5451)
    if result_5450.get("failed_validation_count") != 0:
        raise RuntimeError("checkpoint 5450 is not validated")
    if (
        result_5451.get("failed_validation_count") != 0
        or result_5451.get("valid_for_endpoint_xt_overlap_geometry_atlas") is not True
    ):
        raise RuntimeError("checkpoint 5451 geometry atlas is not validated")
    manifest, manifest_diagnostics = manifest_rows()
    atomic_csv(MANIFEST, manifest)
    if mode == "manifest":
        payload = {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "decision": "INNER_Q_PROJECTION_MANIFEST_BUILT__CORRELATED_SMOKE_PENDING",
            **manifest_diagnostics,
            "runtime_seconds": time.perf_counter() - started,
            "valid_for_correlated_inner_Q_smoke": False,
            "valid_for_correlated_inner_Q_full_cover": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(STATUS, payload)
        return payload
    representatives = representative_smoke_rows(manifest)
    WORK.mkdir(parents=True, exist_ok=True)
    module_5450 = load_module("mts_5450_for_5452", SCRIPT_5450)
    parent = load_module("mts_5395_for_5452", module_5450.SCRIPT_5395)
    parent.set_below_normal_priority()
    parent.M5386.iv.dps = parent.M5386.INTERVAL_DIGITS
    module_5450.ratio_coordinate_bounds = lambda _parent, row: (
        float(row["custom_x_lower"]),
        float(row["custom_x_upper"]),
    )
    references, _ = parent.M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {row["event_id"]: row for row in module_5450.read_csv(module_5450.EVENTS)}
    branches = module_5450.event_branch_map()
    processed = 0
    for projection in representatives:
        path = WORK / f"{projection['projection_job_id']}.json"
        if path.is_file():
            continue
        if max_jobs > 0 and processed >= max_jobs:
            break
        compact_job_json(
            path,
            correlated_projection_job(
                parent,
                module_5450,
                references,
                events,
                branches,
                projection,
            ),
        )
        processed += 1
    completed_payloads = [
        read_json(WORK / f"{row['projection_job_id']}.json")
        for row in representatives
        if (WORK / f"{row['projection_job_id']}.json").is_file()
    ]
    smoke_complete = len(completed_payloads) == len(representatives)
    passed = [
        row for row in completed_payloads if row["correlated_Q_projection_smoke_passes"]
    ]
    arc_rows = [arc for row in completed_payloads for arc in row["arcs"]]
    x_leaf_rows = [leaf for row in completed_payloads for leaf in row["x_leaves"]]
    refinement_rows = [
        witness
        for row in completed_payloads
        for witness in row["refinement_witnesses"]
    ]
    nested_fields = {"arcs", "x_leaves", "refinement_witnesses", "unresolved"}
    summaries = [
        {key: value for key, value in row.items() if key not in nested_fields}
        for row in completed_payloads
    ]
    if summaries:
        atomic_csv(SMOKE_SUMMARY, summaries)
    if arc_rows:
        atomic_csv(SMOKE_ARCS, arc_rows)
    if x_leaf_rows:
        atomic_csv(SMOKE_X_LEAVES, x_leaf_rows)
    if refinement_rows:
        atomic_csv(SMOKE_REFINEMENT, refinement_rows)
    expected_smoke_arc_count = sum(
        int(row["x_subleaf_count"]) * ENERGY_ARC_COUNT
        for row in completed_payloads
    )
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "INNER_Q_PROJECTION_COMPRESSION_CERTIFIED__EIGHT_EVENT_CORRELATED_SMOKE_PASSES__RUN_FULL_RESUME_SAFE_COVER"
            if smoke_complete and len(passed) == len(representatives)
            else (
                "INNER_Q_CORRELATED_SMOKE_EXPOSES_FAILURES"
                if smoke_complete
                else "INNER_Q_CORRELATED_SMOKE_RESUME_REQUIRED"
            )
        ),
        **manifest_diagnostics,
        "smoke_job_count": len(representatives),
        "completed_smoke_job_count": len(completed_payloads),
        "passed_smoke_job_count": len(passed),
        "failed_smoke_job_count": len(completed_payloads) - len(passed),
        "smoke_x_subleaf_count": len(x_leaf_rows),
        "smoke_refinement_witness_count": len(refinement_rows),
        "smoke_arc_count": len(arc_rows),
        "expected_smoke_arc_count": expected_smoke_arc_count,
        "runtime_seconds": time.perf_counter() - started,
        "next_target": "FULL_RESUME_SAFE_CORRELATED_INNER_Q_PROJECTION_COVER",
        "valid_for_correlated_inner_Q_smoke": (
            smoke_complete and len(passed) == len(representatives)
        ),
        "valid_for_correlated_inner_Q_full_cover": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5450_is_valid", result_5450.get("valid_for_correlated_event_curve_contour_smoke") is True, result_5450.get("decision")),
        check("checkpoint_5451_geometry_atlas_is_valid", result_5451.get("valid_for_endpoint_xt_overlap_geometry_atlas") is True, result_5451.get("decision")),
        check("all_5451_inner_leaves_are_projected", manifest_diagnostics["inner_leaf_count"] == int(result_5451["inner_leaf_count"]), f"{manifest_diagnostics['inner_leaf_count']}/{result_5451['inner_leaf_count']}"),
        check("every_epsilon_group_has_one_connected_x_projection", manifest_diagnostics["maximum_x_component_count_per_epsilon_group"] == 1 and manifest_diagnostics["projection_job_count"] == manifest_diagnostics["epsilon_group_count"], manifest_diagnostics["projection_job_count"]),
        check("one_smoke_projection_exists_per_event", len(representatives) == len(EVENT_IDS), len(representatives)),
        check("all_adaptive_x_partitions_reconstruct_projection_intervals", smoke_complete and all(float(row["x_width_absolute_error"]) <= 1.0e-14 * max(float(row["x_width"]), 1.0) for row in completed_payloads), max((float(row["x_width_absolute_error"]) for row in completed_payloads), default=math.nan)),
        check("smoke_matrix_is_complete", smoke_complete and len(arc_rows) == expected_smoke_arc_count and expected_smoke_arc_count >= len(EVENT_IDS) * ENERGY_ARC_COUNT, f"{len(arc_rows)}/{expected_smoke_arc_count}"),
        check("all_correlated_projection_smoke_arcs_pass", smoke_complete and len(passed) == len(representatives), f"{len(passed)}/{len(representatives)}"),
        check("broad_claims_remain_false", not payload["valid_for_correlated_inner_Q_full_cover"] and not payload["valid_for_full_event_cell_finite_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "smoke only"),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started_utc
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
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
    atomic_csv(SOURCES, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("manifest", "smoke"), default="smoke")
    parser.add_argument("--max-jobs", type=int, default=8)
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.mode, arguments.max_jobs)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("failed_validation_count", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
