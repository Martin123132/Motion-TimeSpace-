from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
FORMALIZATION = POST.parent / "formalization-workbench"
OUTPUT = FUNCTIONAL_RG / "5468"
WORK = OUTPUT / "work-v1"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
MANIFEST_5467 = FUNCTIONAL_RG / "5467" / "D4_outer_leaf_epsilon_fiber_manifest.csv"
RESULT_5467 = FUNCTIONAL_RG / "5467" / "D4_outer_leaf_epsilon_fiber_transplant_result.json"
VALIDATION_5467 = FUNCTIONAL_RG / "5467" / "P8_Y5_BRR5460_5467_VALIDATION.csv"
CERTIFICATES_5467 = FUNCTIONAL_RG / "5467" / "D4_outer_leaf_epsilon_fiber_certificates.csv"

MANIFEST = OUTPUT / "D4_exact_outer_cuboid_manifest.csv"
MEMBERSHIP = OUTPUT / "D4_exact_outer_cuboid_membership.csv"
CERTIFICATES = OUTPUT / "D4_exact_outer_cuboid_certificates.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5467_5468_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_exact_outer_cuboid_coalescence_result.json"
DOCUMENT = POST / "5468-Y5-R2FR-D4-exact-outer-cuboid-coalescence-runner.md"

CHECKPOINT = 5468
REVISION = "D4-exact-outer-cuboid-coalescence-runner-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
EXPECTED_FIBER_COUNT = 99_522
EXPECTED_SOURCE_LEAF_COUNT = 606_990
OUTER_RADIUS = 5.0e-6
AXES = ("epsilon", "x", "t")
BOUNDS = {
    "epsilon": ("epsilon_real_lower", "epsilon_real_upper"),
    "x": ("x_lower", "x_upper"),
    "t": ("t_lower", "t_upper"),
}
SEMANTIC_FIELDS = (
    "event_id",
    "event_type",
    "branch_owner_id",
    "mapped_cell_id",
    "term_id",
    "primary_surface_id",
    "path_segment",
    "gap_enclosure_method",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def canonical_float(value: Any) -> float:
    result = float(value)
    return 0.0 if result == 0.0 else result


def exact_key(value: Any) -> str:
    return canonical_float(value).hex()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5467,
        MANIFEST_5467,
        RESULT_5467,
        VALIDATION_5467,
        CERTIFICATES_5467,
    )


def initial_box(row: dict[str, str]) -> dict[str, Any]:
    fiber_id = row["fiber_job_id"]
    return {
        **{field: row[field] for field in SEMANTIC_FIELDS},
        "epsilon_imaginary_lower": canonical_float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": canonical_float(row["epsilon_imaginary_upper"]),
        "epsilon_real_lower": canonical_float(row["epsilon_real_lower"]),
        "epsilon_real_upper": canonical_float(row["epsilon_real_upper"]),
        "x_lower": canonical_float(row["x_lower"]),
        "x_upper": canonical_float(row["x_upper"]),
        "t_lower": canonical_float(row["t_lower"]),
        "t_upper": canonical_float(row["t_upper"]),
        "source_fiber_ids": [fiber_id],
        "source_fiber_count": 1,
        "source_leaf_count": int(row["source_leaf_count"]),
        "source_epsilon_bin_index_lower": int(row["epsilon_bin_index"]),
        "source_epsilon_bin_index_upper": int(row["epsilon_bin_index"]),
        "source_partition_minimum_gap_abs_lower": float(
            row["source_partition_minimum_gap_abs_lower"]
        ),
        "source_partition_maximum_gap_abs_upper": float(
            row["source_partition_maximum_gap_abs_upper"]
        ),
        "source_partition_minimum_material_root_denominator_abs_lower": float(
            row["source_partition_minimum_material_root_denominator_abs_lower"]
        ),
        "source_partition_minimum_implicit_material_derivative_abs_lower": float(
            row["source_partition_minimum_implicit_material_derivative_abs_lower"]
        ),
        "source_piecewise_physical_path_area_abs_upper": float(
            row["physical_path_area_abs_upper"]
        ),
        "source_maximum_path_speed_abs_upper": float(row["path_speed_abs_upper"]),
        "exact_axis_merge_count": 0,
        "merge_generation": 0,
    }


def semantic_key(box: dict[str, Any]) -> tuple[str, ...]:
    return (
        *(str(box[field]) for field in SEMANTIC_FIELDS),
        exact_key(box["epsilon_imaginary_lower"]),
        exact_key(box["epsilon_imaginary_upper"]),
    )


def merge_group_key(box: dict[str, Any], axis: str) -> tuple[str, ...]:
    other_axes = [candidate for candidate in AXES if candidate != axis]
    values: list[str] = list(semantic_key(box))
    for other_axis in other_axes:
        lower_field, upper_field = BOUNDS[other_axis]
        values.extend((exact_key(box[lower_field]), exact_key(box[upper_field])))
    return tuple(values)


def merge_pair(left: dict[str, Any], right: dict[str, Any], axis: str) -> dict[str, Any]:
    lower_field, upper_field = BOUNDS[axis]
    merged = dict(left)
    merged[lower_field] = min(float(left[lower_field]), float(right[lower_field]))
    merged[upper_field] = max(float(left[upper_field]), float(right[upper_field]))
    merged["source_fiber_ids"] = left["source_fiber_ids"] + right["source_fiber_ids"]
    merged["source_fiber_count"] = int(left["source_fiber_count"]) + int(
        right["source_fiber_count"]
    )
    merged["source_leaf_count"] = int(left["source_leaf_count"]) + int(
        right["source_leaf_count"]
    )
    merged["source_epsilon_bin_index_lower"] = min(
        int(left["source_epsilon_bin_index_lower"]),
        int(right["source_epsilon_bin_index_lower"]),
    )
    merged["source_epsilon_bin_index_upper"] = max(
        int(left["source_epsilon_bin_index_upper"]),
        int(right["source_epsilon_bin_index_upper"]),
    )
    for field in (
        "source_partition_minimum_gap_abs_lower",
        "source_partition_minimum_material_root_denominator_abs_lower",
        "source_partition_minimum_implicit_material_derivative_abs_lower",
    ):
        merged[field] = min(float(left[field]), float(right[field]))
    merged["source_partition_maximum_gap_abs_upper"] = max(
        float(left["source_partition_maximum_gap_abs_upper"]),
        float(right["source_partition_maximum_gap_abs_upper"]),
    )
    merged["source_piecewise_physical_path_area_abs_upper"] = float(
        left["source_piecewise_physical_path_area_abs_upper"]
    ) + float(right["source_piecewise_physical_path_area_abs_upper"])
    merged["source_maximum_path_speed_abs_upper"] = max(
        float(left["source_maximum_path_speed_abs_upper"]),
        float(right["source_maximum_path_speed_abs_upper"]),
    )
    merged["exact_axis_merge_count"] = int(left["exact_axis_merge_count"]) + int(
        right["exact_axis_merge_count"]
    ) + 1
    merged["merge_generation"] = max(
        int(left["merge_generation"]), int(right["merge_generation"])
    ) + 1
    return merged


def merge_axis(
    boxes: list[dict[str, Any]], axis: str
) -> tuple[list[dict[str, Any]], int, int]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for box in boxes:
        groups[merge_group_key(box, axis)].append(box)
    lower_field, upper_field = BOUNDS[axis]
    merged_boxes: list[dict[str, Any]] = []
    merge_count = 0
    interior_overlap_merge_count = 0
    for group in groups.values():
        ordered = sorted(
            group,
            key=lambda box: (
                float(box[lower_field]),
                float(box[upper_field]),
                min(box["source_fiber_ids"]),
            ),
        )
        current = ordered[0]
        for candidate in ordered[1:]:
            current_upper = float(current[upper_field])
            candidate_lower = float(candidate[lower_field])
            if candidate_lower <= current_upper:
                if candidate_lower < current_upper:
                    interior_overlap_merge_count += 1
                current = merge_pair(current, candidate, axis)
                merge_count += 1
            else:
                merged_boxes.append(current)
                current = candidate
        merged_boxes.append(current)
    return merged_boxes, merge_count, interior_overlap_merge_count


def coalesce(
    source_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    boxes = [initial_box(row) for row in source_rows]
    axis_merge_counts = {axis: 0 for axis in AXES}
    overlap_merge_count = 0
    cycle_count = 0
    cycle_rows: list[dict[str, int]] = []
    for cycle in range(1, 33):
        cycle_count = cycle
        cycle_start = len(boxes)
        cycle_merges = 0
        for axis in AXES:
            boxes, merge_count, axis_overlap_count = merge_axis(boxes, axis)
            axis_merge_counts[axis] += merge_count
            cycle_merges += merge_count
            overlap_merge_count += axis_overlap_count
        cycle_rows.append(
            {
                "cycle": cycle,
                "start_count": cycle_start,
                "merge_count": cycle_merges,
                "end_count": len(boxes),
            }
        )
        if cycle_merges == 0:
            break
    else:
        raise RuntimeError("exact cuboid coalescence did not reach a fixed point")
    return boxes, {
        "coalescence_cycle_count": cycle_count,
        "axis_merge_counts": axis_merge_counts,
        "interior_overlap_merge_count": overlap_merge_count,
        "cycle_rows": cycle_rows,
    }


def cuboid_identifier(box: dict[str, Any]) -> tuple[str, str]:
    member_ids = sorted(box["source_fiber_ids"])
    member_digest = hashlib.sha256("\n".join(member_ids).encode("utf-8")).hexdigest()
    payload = [
        *semantic_key(box),
        *(exact_key(box[field]) for axis in AXES for field in BOUNDS[axis]),
        member_digest,
    ]
    suffix = hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return (
        f"{box['event_id']}__{box['mapped_cell_id']}__{box['path_segment']}__CUBOID__{suffix}",
        member_digest,
    )


def finalize_manifest(
    boxes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    membership: list[dict[str, Any]] = []
    for box in boxes:
        cuboid_id, member_digest = cuboid_identifier(box)
        epsilon_width = float(box["epsilon_real_upper"]) - float(
            box["epsilon_real_lower"]
        )
        x_width = float(box["x_upper"]) - float(box["x_lower"])
        t_width = float(box["t_upper"]) - float(box["t_lower"])
        row = {
            "cuboid_job_id": cuboid_id,
            **{field: box[field] for field in SEMANTIC_FIELDS},
            "epsilon_real_lower": box["epsilon_real_lower"],
            "epsilon_real_upper": box["epsilon_real_upper"],
            "epsilon_imaginary_lower": box["epsilon_imaginary_lower"],
            "epsilon_imaginary_upper": box["epsilon_imaginary_upper"],
            "epsilon_width": epsilon_width,
            "x_lower": box["x_lower"],
            "x_upper": box["x_upper"],
            "x_width": x_width,
            "t_lower": box["t_lower"],
            "t_upper": box["t_upper"],
            "t_width": t_width,
            "parameter_area": x_width * t_width,
            "source_fiber_count": box["source_fiber_count"],
            "source_leaf_count": box["source_leaf_count"],
            "source_fiber_membership_sha256": member_digest,
            "source_epsilon_bin_index_lower": box[
                "source_epsilon_bin_index_lower"
            ],
            "source_epsilon_bin_index_upper": box[
                "source_epsilon_bin_index_upper"
            ],
            "source_partition_minimum_gap_abs_lower": box[
                "source_partition_minimum_gap_abs_lower"
            ],
            "source_partition_maximum_gap_abs_upper": box[
                "source_partition_maximum_gap_abs_upper"
            ],
            "source_partition_minimum_material_root_denominator_abs_lower": box[
                "source_partition_minimum_material_root_denominator_abs_lower"
            ],
            "source_partition_minimum_implicit_material_derivative_abs_lower": box[
                "source_partition_minimum_implicit_material_derivative_abs_lower"
            ],
            "source_piecewise_physical_path_area_abs_upper": box[
                "source_piecewise_physical_path_area_abs_upper"
            ],
            "source_maximum_path_speed_abs_upper": box[
                "source_maximum_path_speed_abs_upper"
            ],
            "exact_axis_merge_count": box["exact_axis_merge_count"],
            "merge_generation": box["merge_generation"],
            "exact_cuboid_union": True,
            "transplant_method": "FIXED_POINT_EXACT_AXIS_ALIGNED_CUBOID_COALESCENCE",
            "valid_for_exact_outer_cuboid_transplant": False,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        rows.append(row)
        for fiber_id in sorted(box["source_fiber_ids"]):
            membership.append(
                {
                    "cuboid_job_id": cuboid_id,
                    "source_fiber_job_id": fiber_id,
                }
            )
    rows.sort(
        key=lambda row: (
            -int(row["source_leaf_count"]),
            float(row["source_partition_minimum_gap_abs_lower"]),
            row["cuboid_job_id"],
        )
    )
    for index, row in enumerate(rows, start=1):
        row["evaluation_priority"] = index
    membership.sort(
        key=lambda row: (row["cuboid_job_id"], row["source_fiber_job_id"])
    )
    return rows, membership


def full_cell_path_speed_bound(
    parent: Any,
    cell: dict[str, Any],
    path_segment: str,
) -> float:
    if path_segment != "TOP":
        return float(parent.DEFAULT_ENERGY_DEFORMATION)
    x_lower = float(cell["lower_absolute_soft_cosine"])
    x_upper = float(cell["upper_absolute_soft_cosine"])
    lower_energy, _ = parent.interval_boundary_energy(
        cell["lower_energy_boundary"], x_lower, x_upper
    )
    upper_energy, _ = parent.interval_boundary_energy(
        cell["upper_energy_boundary"], x_lower, x_upper
    )
    bound = float(parent.M5258.upper_abs(upper_energy - lower_energy))
    if not math.isfinite(bound) or bound <= 0.0:
        raise RuntimeError("full-cell TOP path-speed bound is not finite and positive")
    return bound


def evaluate_cuboid(
    base: Any,
    stable: Any,
    parent: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, Any]:
    cell = cells[row["mapped_cell_id"]]
    path_speed_bound = full_cell_path_speed_bound(
        parent, cell, row["path_segment"]
    )
    physical_area_bound = float(row["parameter_area"]) * path_speed_bound
    probe = {
        "smoke_job_id": row["cuboid_job_id"],
        "selection_role": "EXACT_AXIS_ALIGNED_OUTER_CUBOID_HULL",
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "branch_owner_id": row["branch_owner_id"],
        "epsilon_bin_index": int(row["source_epsilon_bin_index_lower"]),
        "epsilon_subdivision_index": 0,
        "epsilon_subdivision_count": 1,
        "epsilon_real_lower": float(row["epsilon_real_lower"]),
        "epsilon_real_upper": float(row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
        "path_segment": row["path_segment"],
        "x_lower": float(row["x_lower"]),
        "x_upper": float(row["x_upper"]),
        "t_lower": float(row["t_lower"]),
        "t_upper": float(row["t_upper"]),
        "refinement_depth": 0,
        "refinement_path": "R",
        "gap_abs_lower": float(row["source_partition_minimum_gap_abs_lower"]),
        "physical_path_area_abs_upper": physical_area_bound,
    }
    result = stable.adaptive_evaluate_representative(
        parent,
        cells,
        support_segments,
        branches,
        probe,
    )
    passed = truth(result.get("probe_passed"))
    result.update(
        {
            "cuboid_job_id": row["cuboid_job_id"],
            "source_fiber_count": int(row["source_fiber_count"]),
            "source_leaf_count": int(row["source_leaf_count"]),
            "source_fiber_membership_sha256": row[
                "source_fiber_membership_sha256"
            ],
            "epsilon_cuboid_real_lower": float(row["epsilon_real_lower"]),
            "epsilon_cuboid_real_upper": float(row["epsilon_real_upper"]),
            "full_cell_path_speed_abs_upper": path_speed_bound,
            "evaluation_physical_path_area_abs_upper": physical_area_bound,
            "exact_cuboid_union": True,
            "transplant_method": row["transplant_method"],
            "certificate_source": "checkpoint_5468_parent_v51_exact_cuboid_hull",
            "parent_revision": PARENT_REVISION,
            "valid_for_exact_outer_cuboid_transplant": passed,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    return result


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5468: D4 exact outer-cuboid coalescence runner",
        "",
        "## Derivation",
        "",
        "Two closed axis-aligned boxes with identical semantic ownership and identical intervals on two axes have union equal to their interval hull when their intervals on the third axis touch or overlap. Repeating this identity over epsilon, x and t to a fixed point produces a lossless cuboid cover; no representative margin and no untested gap region is imported.",
        "",
        "```text",
        "B1 = I1 x J x K, B2 = I2 x J x K, inf(I2) <= sup(I1)",
        "B1 union B2 = hull(I1 union I2) x J x K",
        "repeat over epsilon, x, t until no exact merge remains",
        "```",
        "",
        "A failed cuboid is a compression failure only. It must be split through its recorded source-fiber membership; it is not evidence that any constituent checkpoint-5451 leaf fails.",
        "",
        "## Current state",
        "",
        f"Input fibers: `{payload['input_fiber_count']}` covering `{payload['input_source_leaf_count']}` source leaves. Fixed-point cuboids: `{payload['cuboid_manifest_count']}`. Fiber-to-cuboid compression: `{payload['fiber_to_cuboid_compression_factor']:.12g}`. Total leaf-to-cuboid compression: `{payload['leaf_to_cuboid_compression_factor']:.12g}`.",
        "",
        f"Certified cuboids: `{payload['certified_cuboid_count']}/{payload['cuboid_manifest_count']}` covering `{payload['certified_source_leaf_count']}/{payload['input_source_leaf_count']}` source leaves. Failed cuboids: `{payload['failed_cuboid_count']}`. Remaining cuboids: `{payload['remaining_cuboid_count']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "Full outer enclosure becomes true only when every exact cuboid is certified or every failed cuboid is losslessly split to certified descendants. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    base = load_module("mts_5467_doc_helpers", SCRIPT_5467)
    base.atomic_text(DOCUMENT, "\n".join(lines))


def run(
    requested_job_id: str | None,
    choose_next: bool,
    max_jobs: int,
    status_only: bool,
    list_next: int,
) -> dict[str, Any]:
    base = load_module("mts_5467_for_5468", SCRIPT_5467)
    base.set_below_normal_priority()
    before_formalization = base.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5467 = read_json(RESULT_5467)
    validation_5467 = read_csv(VALIDATION_5467)
    source_rows = read_csv(MANIFEST_5467)
    boxes, diagnostics = coalesce(source_rows)
    manifest, membership = finalize_manifest(boxes)
    base.atomic_csv(MANIFEST, manifest)
    base.atomic_csv(MEMBERSHIP, membership)
    manifest_by_id = {row["cuboid_job_id"]: row for row in manifest}
    if len(manifest_by_id) != len(manifest):
        raise RuntimeError("cuboid job identifiers are not unique")
    WORK.mkdir(parents=True, exist_ok=True)
    completed_ids = {path.stem for path in WORK.glob("*.json") if path.is_file()}
    pending = [
        row for row in manifest if row["cuboid_job_id"] not in completed_ids
    ]
    if list_next > 0:
        print(
            json.dumps(
                [
                    {
                        "cuboid_job_id": row["cuboid_job_id"],
                        "source_fiber_count": int(row["source_fiber_count"]),
                        "source_leaf_count": int(row["source_leaf_count"]),
                        "event_id": row["event_id"],
                        "mapped_cell_id": row["mapped_cell_id"],
                        "path_segment": row["path_segment"],
                        "minimum_gap": float(
                            row["source_partition_minimum_gap_abs_lower"]
                        ),
                    }
                    for row in pending[:list_next]
                ],
                indent=2,
            )
        )
    schedule: list[dict[str, Any]] = []
    if requested_job_id:
        if requested_job_id not in manifest_by_id:
            raise ValueError(f"unknown cuboid job id: {requested_job_id}")
        if requested_job_id not in completed_ids:
            schedule = [manifest_by_id[requested_job_id]]
    elif choose_next:
        schedule = pending
    if status_only:
        schedule = []
    if schedule and max_jobs <= 0:
        raise ValueError("--max-jobs must be positive when evaluating cuboids")
    processed = 0
    if schedule:
        stable, parent, cells, support_segments, branches = base.load_parent()
        if parent.REVISION != PARENT_REVISION:
            raise RuntimeError(
                f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
            )
        for row in schedule:
            if processed >= max_jobs:
                break
            result = evaluate_cuboid(
                base,
                stable,
                parent,
                cells,
                support_segments,
                branches,
                row,
            )
            base.atomic_json(
                WORK / f"{row['cuboid_job_id']}.json", result, compact=True
            )
            processed += 1
            if not truth(result["valid_for_exact_outer_cuboid_transplant"]):
                break
    completed: list[dict[str, Any]] = []
    for row in manifest:
        path = WORK / f"{row['cuboid_job_id']}.json"
        if path.is_file():
            completed.append(read_json(path))
    certified = [
        row
        for row in completed
        if truth(row.get("valid_for_exact_outer_cuboid_transplant"))
    ]
    failed = [row for row in completed if row not in certified]
    certified_ids = {row["cuboid_job_id"] for row in certified}
    certified_source_leaf_count = sum(
        int(row["source_leaf_count"]) for row in certified
    )
    remaining = [
        row for row in manifest if row["cuboid_job_id"] not in certified_ids
    ]
    complete = len(certified) == len(manifest) and not failed
    if certified:
        base.atomic_csv(
            CERTIFICATES,
            sorted(certified, key=lambda row: row["cuboid_job_id"]),
        )
    input_fiber_ids = [row["fiber_job_id"] for row in source_rows]
    membership_fiber_ids = [row["source_fiber_job_id"] for row in membership]
    after_formalization = base.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "ALL_EXACT_OUTER_CUBOIDS_CERTIFIED__AGGREGATE_INNER_AND_PRINCIPAL"
            if complete
            else (
                "EXACT_CUBOID_HULL_FAILURE__SPLIT_RECORDED_FIBER_MEMBERSHIP"
                if failed
                else "EXACT_OUTER_CUBOID_TRANSPLANT_PARTIAL__RESUME"
            )
        ),
        "input_fiber_count": len(source_rows),
        "input_source_leaf_count": sum(
            int(row["source_leaf_count"]) for row in source_rows
        ),
        "cuboid_manifest_count": len(manifest),
        "membership_row_count": len(membership),
        "fiber_to_cuboid_compression_factor": len(source_rows) / len(manifest),
        "leaf_to_cuboid_compression_factor": EXPECTED_SOURCE_LEAF_COUNT
        / len(manifest),
        "maximum_cuboid_source_fiber_count": max(
            int(row["source_fiber_count"]) for row in manifest
        ),
        "maximum_cuboid_source_leaf_count": max(
            int(row["source_leaf_count"]) for row in manifest
        ),
        **diagnostics,
        "completed_cuboid_count": len(completed),
        "certified_cuboid_count": len(certified),
        "failed_cuboid_count": len(failed),
        "remaining_cuboid_count": len(manifest) - len(certified),
        "certified_source_leaf_count": certified_source_leaf_count,
        "remaining_source_leaf_count": EXPECTED_SOURCE_LEAF_COUNT
        - certified_source_leaf_count,
        "processed_this_run": processed,
        "minimum_certified_amplitude_denominator_abs_lower": min(
            (
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in certified
            ),
            default=math.nan,
        ),
        "first_failed_cuboid_job_id": (
            failed[0]["cuboid_job_id"] if failed else ""
        ),
        "first_failed_cuboid_type": (
            failed[0].get("failure_type", "") if failed else ""
        ),
        "first_failed_cuboid_message": (
            failed[0].get("failure_message", "") if failed else ""
        ),
        "next_target": (
            "COMBINE_CERTIFIED_OUTER_WITH_INNER_Q_AND_PRINCIPAL_PART"
            if complete
            else (
                failed[0]["cuboid_job_id"]
                if failed
                else (remaining[0]["cuboid_job_id"] if remaining else "")
            )
        ),
        "valid_for_exact_outer_cuboid_transplant": complete,
        "valid_for_full_outer_parent_leaf_enclosure": complete,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5467_partition_is_source_complete",
            int(result_5467.get("fiber_manifest_count", -1))
            == EXPECTED_FIBER_COUNT
            and int(result_5467.get("outer_source_leaf_count", -1))
            == EXPECTED_SOURCE_LEAF_COUNT
            and int(result_5467.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5467),
            result_5467.get("decision"),
        ),
        check(
            "all_99522_input_fibers_are_unique",
            len(input_fiber_ids) == EXPECTED_FIBER_COUNT
            and len(set(input_fiber_ids)) == EXPECTED_FIBER_COUNT,
            len(set(input_fiber_ids)),
        ),
        check(
            "input_source_leaf_sum_is_606990",
            payload["input_source_leaf_count"] == EXPECTED_SOURCE_LEAF_COUNT,
            payload["input_source_leaf_count"],
        ),
        check(
            "fiber_membership_is_lossless_and_unique",
            len(membership_fiber_ids) == EXPECTED_FIBER_COUNT
            and len(set(membership_fiber_ids)) == EXPECTED_FIBER_COUNT
            and set(membership_fiber_ids) == set(input_fiber_ids),
            len(set(membership_fiber_ids)),
        ),
        check(
            "cuboid_source_leaf_sum_is_606990",
            sum(int(row["source_leaf_count"]) for row in manifest)
            == EXPECTED_SOURCE_LEAF_COUNT,
            sum(int(row["source_leaf_count"]) for row in manifest),
        ),
        check(
            "every_merge_is_an_exact_axis_hull",
            bool(manifest)
            and all(truth(row["exact_cuboid_union"]) for row in manifest),
            f"overlap_merges={diagnostics['interior_overlap_merge_count']}",
        ),
        check(
            "coalescence_reaches_fixed_point",
            diagnostics["cycle_rows"][-1]["merge_count"] == 0,
            diagnostics["cycle_rows"][-1],
        ),
        check(
            "exact_cuboid_compression_improves_fiber_manifest",
            0 < len(manifest) < EXPECTED_FIBER_COUNT,
            len(manifest),
        ),
        check(
            "every_cuboid_remains_source_outer",
            all(
                float(row["source_partition_minimum_gap_abs_lower"])
                >= OUTER_RADIUS
                for row in manifest
            ),
            min(
                float(row["source_partition_minimum_gap_abs_lower"])
                for row in manifest
            ),
        ),
        check(
            "all_certified_cuboids_have_positive_parent_factors",
            all(
                truth(row.get("probe_passed"))
                and truth(row.get("exact_cuboid_union"))
                and all(
                    math.isfinite(float(row[field])) and float(row[field]) > 0.0
                    for field in (
                        "minimum_amplitude_denominator_abs_lower",
                        "relative_root_abs_lower",
                        "selected_global_root_abs_lower",
                        "collision_jacobian_abs_lower",
                    )
                )
                for row in certified
            ),
            len(certified),
        ),
        check(
            "failed_cuboids_remain_nonclaim",
            all(
                not truth(row.get("valid_for_full_outer_parent_leaf_enclosure"))
                and not truth(row.get("valid_for_D4_event_local_W3_bound"))
                and not truth(row.get("valid_for_all_operator_local_GR_claim"))
                and not truth(row.get("valid_for_full_MTS_claim"))
                for row in failed
            ),
            len(failed),
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_event_cell_finite_cover"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "outer cuboid layer only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    register = [
        {
            "checkpoint": CHECKPOINT,
            "source_path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
            "source_role": "exact-cuboid-parent-input",
        }
        for path in source_paths()
    ]
    base.atomic_csv(SOURCE_REGISTER, register)
    base.atomic_csv(VALIDATION, validations)
    base.atomic_json(STATUS, payload)
    base.atomic_json(RESULT, payload)
    render_document(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--max-jobs", type=int, default=1)
    parser.add_argument("--status-only", action="store_true")
    parser.add_argument("--list-next", type=int, default=0)
    arguments = parser.parse_args()
    payload = run(
        arguments.job_id,
        arguments.next,
        arguments.max_jobs,
        arguments.status_only,
        arguments.list_next,
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "input_fiber_count",
                    "cuboid_manifest_count",
                    "fiber_to_cuboid_compression_factor",
                    "maximum_cuboid_source_leaf_count",
                    "certified_cuboid_count",
                    "certified_source_leaf_count",
                    "failed_cuboid_count",
                    "remaining_cuboid_count",
                    "next_target",
                    "failed_validation_count",
                )
            },
            indent=2,
        )
    )
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
