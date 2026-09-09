from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from collections import defaultdict
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
OUTPUT = FUNCTIONAL_RG / "5454"
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
MANIFEST_5452 = (
    FUNCTIONAL_RG / "5452" / "D4_inner_Q_x_epsilon_projection_manifest.csv"
)
SCRIPT_5453 = POST / "scripts" / "Y5_R2FR_5453_D4_full_inner_Q_projection_cover.py"
RESULT_5453 = (
    FUNCTIONAL_RG / "5453" / "D4_full_inner_Q_projection_cover_result.json"
)

DOCUMENT = POST / "5454-Y5-R2FR-D4-epsilon-connected-superprojection-smoke.md"
SUPERMANIFEST = OUTPUT / "D4_epsilon_connected_superprojection_manifest.csv"
SOURCE_MAP = OUTPUT / "D4_epsilon_connected_superprojection_source_map.csv"
SMOKE_SUMMARY = OUTPUT / "D4_epsilon_connected_superprojection_smoke_summary.csv"
SMOKE_ARCS = OUTPUT / "D4_epsilon_connected_superprojection_smoke_arcs.csv"
SMOKE_X_LEAVES = OUTPUT / "D4_epsilon_connected_superprojection_smoke_x_leaves.csv"
SMOKE_REFINEMENT = OUTPUT / "D4_epsilon_connected_superprojection_refinement_witnesses.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5452_5454_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_epsilon_connected_superprojection_smoke_result.json"

CHECKPOINT = 5454
REVISION = "D4-epsilon-connected-superprojection-smoke-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
CONTIGUITY_TOLERANCE = 1.0e-15
NESTED_FIELDS = {"arcs", "x_leaves", "refinement_witnesses", "unresolved"}


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


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5452,
        RESULT_5452,
        MANIFEST_5452,
        SCRIPT_5453,
        RESULT_5453,
    )


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    return {
        str(path): (path.stat().st_mtime_ns, path.stat().st_size)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def build_supermanifest() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(MANIFEST_5452)
    groups: dict[tuple[Any, ...], list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        key = (
            row["event_id"],
            row["mapped_cell_id"],
            int(row["epsilon_bin_index"]),
            int(row["x_component_index"]),
            row["x_lower"],
            row["x_upper"],
            row["epsilon_imaginary_lower"],
            row["epsilon_imaginary_upper"],
        )
        groups[key].append(row)
    components: list[tuple[tuple[Any, ...], list[dict[str, str]]]] = []
    for key, rows in sorted(groups.items()):
        ordered = sorted(rows, key=lambda row: float(row["epsilon_real_lower"]))
        connected = [ordered[0]]
        for row in ordered[1:]:
            gap = float(row["epsilon_real_lower"]) - float(
                connected[-1]["epsilon_real_upper"]
            )
            if abs(gap) <= CONTIGUITY_TOLERANCE:
                connected.append(row)
            else:
                components.append((key, connected))
                connected = [row]
        components.append((key, connected))
    super_rows: list[dict[str, Any]] = []
    map_rows: list[dict[str, Any]] = []
    maximum_tiling_error = 0.0
    for key, rows in components:
        (
            event_id,
            cell_id,
            epsilon_bin,
            x_component_index,
            x_lower_text,
            x_upper_text,
            epsilon_imaginary_lower_text,
            epsilon_imaginary_upper_text,
        ) = key
        ordered = sorted(rows, key=lambda row: float(row["epsilon_real_lower"]))
        source_width = sum(
            float(row["epsilon_real_upper"]) - float(row["epsilon_real_lower"])
            for row in ordered
        )
        epsilon_lower = float(ordered[0]["epsilon_real_lower"])
        epsilon_upper = float(ordered[-1]["epsilon_real_upper"])
        hull_width = epsilon_upper - epsilon_lower
        tiling_error = abs(source_width - hull_width)
        maximum_tiling_error = max(maximum_tiling_error, tiling_error)
        first_index = int(ordered[0]["epsilon_subdivision_index"])
        last_index = int(ordered[-1]["epsilon_subdivision_index"])
        declared_count = int(ordered[0]["epsilon_subdivision_count"])
        epsilon_label = str(epsilon_bin).replace("-", "m")
        job_id = (
            f"{event_id}__{cell_id}__e{epsilon_label}__"
            f"s{first_index:04d}to{last_index:04d}of{declared_count:04d}__"
            f"x{x_component_index:02d}"
        )
        source_ids = [row["projection_job_id"] for row in ordered]
        super_row = {
            "projection_job_id": job_id,
            "event_id": event_id,
            "mapped_cell_id": cell_id,
            "epsilon_bin_index": epsilon_bin,
            "epsilon_subdivision_index": first_index,
            "epsilon_subdivision_count": declared_count,
            "epsilon_real_lower": epsilon_lower,
            "epsilon_real_upper": epsilon_upper,
            "epsilon_imaginary_lower": float(epsilon_imaginary_lower_text),
            "epsilon_imaginary_upper": float(epsilon_imaginary_upper_text),
            "x_component_index": x_component_index,
            "x_component_count": 1,
            "x_lower": float(x_lower_text),
            "x_upper": float(x_upper_text),
            "x_width": float(x_upper_text) - float(x_lower_text),
            "source_inner_leaf_count": sum(
                int(row["source_inner_leaf_count"]) for row in ordered
            ),
            "source_projection_job_count": len(ordered),
            "source_projection_job_ids": "|".join(source_ids),
            "source_epsilon_width": source_width,
            "superprojection_epsilon_width": hull_width,
            "epsilon_tiling_absolute_error": tiling_error,
            "Q_energy_contour_radius": float(ordered[0]["Q_energy_contour_radius"]),
            "inner_radius": float(ordered[0]["inner_radius"]),
            "status": "PENDING_CORRELATED_Q_SUPERPROJECTION_ENCLOSURE",
            "valid_for_correlated_inner_Q_full_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        super_rows.append(super_row)
        for source_id in source_ids:
            map_rows.append(
                {
                    "source_projection_job_id": source_id,
                    "superprojection_job_id": job_id,
                    "event_id": event_id,
                    "mapped_cell_id": cell_id,
                    "epsilon_bin_index": epsilon_bin,
                    "valid_for_correlated_inner_Q_full_cover": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    source_ids = [row["projection_job_id"] for row in source_rows]
    mapped_ids = [row["source_projection_job_id"] for row in map_rows]
    diagnostics = {
        "source_projection_job_count": len(source_rows),
        "source_projection_unique_id_count": len(set(source_ids)),
        "mapped_source_projection_count": len(mapped_ids),
        "mapped_source_projection_unique_id_count": len(set(mapped_ids)),
        "superprojection_job_count": len(super_rows),
        "compression_factor": len(source_rows) / len(super_rows),
        "maximum_epsilon_tiling_absolute_error": maximum_tiling_error,
        "source_map_is_exact": sorted(source_ids) == sorted(mapped_ids),
    }
    return super_rows, map_rows, diagnostics


def representative_rows(supermanifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    representatives: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in supermanifest if row["event_id"] == event_id]
        if not selected:
            raise RuntimeError(f"no superprojection for {event_id}")
        representatives.append(
            max(
                selected,
                key=lambda row: (
                    int(row["source_projection_job_count"]),
                    float(row["superprojection_epsilon_width"]),
                    float(row["x_width"]),
                ),
            )
        )
    return representatives


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5454: D4 epsilon-connected superprojection smoke",
        "",
        "## Exact reduction",
        "",
        f"The `{payload['source_projection_job_count']}` checkpoint-5452 projection rectangles contain only `{payload['superprojection_job_count']}` connected groups with identical event, cell, epsilon bin, x interval and imaginary-epsilon interval. Adjacent real-epsilon slabs in each group tile one closed interval with maximum reconstruction error `{payload['maximum_epsilon_tiling_absolute_error']}`. No interpolation or physical closure is introduced.",
        "",
        f"The exact compression factor is `{payload['compression_factor']}`. Every source projection id occurs exactly once in the source map: `{payload['source_map_is_exact']}`.",
        "",
        "## Correlated smoke",
        "",
        f"One largest merged component per event is evaluated through all 32 exact parent Q arcs with the checkpoint-5452 adaptive x policy. Completed jobs: `{payload['completed_smoke_job_count']}/{payload['smoke_job_count']}`; passed: `{payload['passed_smoke_job_count']}`.",
        "",
        "## Claim boundary",
        "",
        "This checkpoint tests whether exact adjacent-slab merging can replace the measured 178-hour naïve enumeration. It does not certify all superprojections, the outer parent atlas, event-local W3, the D4 regulator limit, local GR or full MTS.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(mode: str, max_jobs: int) -> dict[str, Any]:
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5452 = read_json(RESULT_5452)
    result_5453 = read_json(RESULT_5453)
    if (
        result_5452.get("failed_validation_count") != 0
        or result_5452.get("valid_for_correlated_inner_Q_smoke") is not True
    ):
        raise RuntimeError("checkpoint 5452 correlated smoke is not validated")
    if result_5453.get("failed_validation_count") != 0:
        raise RuntimeError("checkpoint 5453 bounded full-run controller is not validated")
    supermanifest, source_map, diagnostics = build_supermanifest()
    atomic_csv(SUPERMANIFEST, supermanifest)
    atomic_csv(SOURCE_MAP, source_map)
    representatives = representative_rows(supermanifest)
    processed_this_run = 0
    if mode == "smoke":
        WORK.mkdir(parents=True, exist_ok=True)
        module_5452 = load_module("mts_5452_for_5454", SCRIPT_5452)
        module_5450 = module_5452.load_module(
            "mts_5450_for_5454", module_5452.SCRIPT_5450
        )
        parent = module_5452.load_module("mts_5395_for_5454", module_5450.SCRIPT_5395)
        parent.set_below_normal_priority()
        parent.M5386.iv.dps = parent.M5386.INTERVAL_DIGITS
        module_5450.ratio_coordinate_bounds = lambda _parent, row: (
            float(row["custom_x_lower"]),
            float(row["custom_x_upper"]),
        )
        references, _ = parent.M5385.M5380.M5379.M5378.M5359.reference_rows()
        events = {
            row["event_id"]: row
            for row in module_5450.read_csv(module_5450.EVENTS)
        }
        branches = module_5450.event_branch_map()
        for projection in representatives:
            path = WORK / f"{projection['projection_job_id']}.json"
            if path.is_file():
                continue
            if max_jobs > 0 and processed_this_run >= max_jobs:
                break
            payload = module_5452.correlated_projection_job(
                parent,
                module_5450,
                references,
                events,
                branches,
                projection,
            )
            payload.update(
                {
                    "checkpoint": CHECKPOINT,
                    "runner_revision": REVISION,
                    "source_projection_job_count": projection[
                        "source_projection_job_count"
                    ],
                    "source_projection_job_ids": projection[
                        "source_projection_job_ids"
                    ],
                    "superprojection_epsilon_width": projection[
                        "superprojection_epsilon_width"
                    ],
                    "valid_for_correlated_inner_Q_full_cover": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            atomic_json(path, payload, compact=True)
            processed_this_run += 1
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "processed_this_run": processed_this_run,
                    "last_job_id": projection["projection_job_id"],
                },
            )
    completed = [
        read_json(WORK / f"{row['projection_job_id']}.json")
        for row in representatives
        if (WORK / f"{row['projection_job_id']}.json").is_file()
    ]
    complete = len(completed) == len(representatives)
    passed = [
        row for row in completed if row["correlated_Q_projection_smoke_passes"]
    ]
    arcs = [arc for row in completed for arc in row["arcs"]]
    x_leaves = [leaf for row in completed for leaf in row["x_leaves"]]
    refinements = [
        witness for row in completed for witness in row["refinement_witnesses"]
    ]
    summaries = [
        {key: value for key, value in row.items() if key not in NESTED_FIELDS}
        for row in completed
    ]
    if summaries:
        atomic_csv(SMOKE_SUMMARY, summaries)
    if arcs:
        atomic_csv(SMOKE_ARCS, arcs)
    if x_leaves:
        atomic_csv(SMOKE_X_LEAVES, x_leaves)
    if refinements:
        atomic_csv(SMOKE_REFINEMENT, refinements)
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "EXACT_EPSILON_SUPERPROJECTION_REDUCTION_CERTIFIED__EIGHT_EVENT_SMOKE_PASSES__RUN_85_JOB_COVER"
            if complete and len(passed) == len(representatives)
            else (
                "EPSILON_SUPERPROJECTION_SMOKE_REQUIRES_ADAPTIVE_EPSILON_SPLIT"
                if complete
                else "EPSILON_SUPERPROJECTION_SMOKE_RESUME_REQUIRED"
            )
        ),
        **diagnostics,
        "smoke_job_count": len(representatives),
        "completed_smoke_job_count": len(completed),
        "passed_smoke_job_count": len(passed),
        "failed_smoke_job_count": len(completed) - len(passed),
        "smoke_x_subleaf_count": len(x_leaves),
        "smoke_arc_count": len(arcs),
        "smoke_refinement_witness_count": len(refinements),
        "processed_this_run": processed_this_run,
        "runtime_seconds": time.perf_counter() - started,
        "naive_5453_estimated_remaining_runtime_seconds": result_5453.get(
            "estimated_remaining_runtime_seconds"
        ),
        "next_target": (
            "FULL_85_JOB_EPSILON_CONNECTED_SUPERPROJECTION_COVER"
            if complete and len(passed) == len(representatives)
            else (
                "ADAPTIVE_EPSILON_SPLIT_OF_FAILED_SUPERPROJECTIONS"
                if complete
                else "RESUME_EIGHT_EVENT_EPSILON_SUPERPROJECTION_SMOKE"
            )
        ),
        "valid_for_epsilon_connected_superprojection_smoke": (
            complete and len(passed) == len(representatives)
        ),
        "valid_for_correlated_inner_Q_full_cover": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    expected_arc_count = sum(
        int(row["x_subleaf_count"]) * ENERGY_ARC_COUNT for row in completed
    )
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5452_smoke_is_valid", result_5452.get("valid_for_correlated_inner_Q_smoke") is True, result_5452.get("decision")),
        check("checkpoint_5453_controller_state_is_valid", result_5453.get("failed_validation_count") == 0, result_5453.get("decision")),
        check("every_5452_source_projection_is_mapped_exactly_once", diagnostics["source_map_is_exact"] and diagnostics["mapped_source_projection_unique_id_count"] == diagnostics["source_projection_job_count"], diagnostics["mapped_source_projection_unique_id_count"]),
        check("all_connected_epsilon_components_reconstruct_exactly", diagnostics["maximum_epsilon_tiling_absolute_error"] <= CONTIGUITY_TOLERANCE, diagnostics["maximum_epsilon_tiling_absolute_error"]),
        check("one_largest_superprojection_is_selected_per_event", len(representatives) == len(EVENT_IDS), len(representatives)),
        check("completed_x_partitions_reconstruct", all(float(row["x_width_absolute_error"]) <= 1.0e-14 * max(float(row["x_width"]), 1.0) for row in completed), max((float(row["x_width_absolute_error"]) for row in completed), default=0.0)),
        check("completed_arc_matrices_are_complete", len(arcs) == expected_arc_count, f"{len(arcs)}/{expected_arc_count}"),
        check("all_completed_superprojection_arcs_pass", len(passed) == len(completed), f"{len(passed)}/{len(completed)}"),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_correlated_inner_Q_full_cover"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "superprojection smoke only"),
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
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("manifest", "smoke"), default="manifest")
    parser.add_argument("--max-jobs", type=int, default=8)
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.mode, arguments.max_jobs)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
