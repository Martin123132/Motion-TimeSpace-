from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import re
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
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5466"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5463 = SCRIPTS / "Y5_R2FR_5463_D4_generalized_connector_finite_projective_amplitude_runner.py"
SCRIPT_5465 = SCRIPTS / "Y5_R2FR_5465_D4_minimal_depth_connector_finite_projective_amplitude_runner.py"
REPRESENTATIVES_5456 = FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"

DOCUMENT = POST / "5466-Y5-R2FR-D4-locally-refined-connector-finite-projective-amplitude-runner.md"
TARGET_STATUS = OUTPUT / "D4_local_refined_connector_target_status.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5466_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_local_refined_connector_runner_result.json"

CHECKPOINT = 5466
REVISION = "D4-locally-refined-connector-finite-projective-amplitude-runner-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
COARSE_X_SUBDIVISIONS = 8
FINE_X_SUBDIVISIONS = 16
T_SUBDIVISIONS = 32
COARSE_DEPTH = 8
FINE_DEPTH = 9
GLOBAL_ARC_COUNT = 4


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any], compact: bool = False) -> None:
    value = json.dumps(
        payload,
        indent=None if compact else 2,
        sort_keys=True,
        separators=(",", ":") if compact else None,
    )
    atomic_text(path, value + ("" if compact else "\n"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def truth(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def set_below_normal_priority() -> None:
    if os.name == "nt":
        process = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    if not FORMALIZATION.is_dir():
        return {}
    return {
        str(path.relative_to(FORMALIZATION)): (
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def target_key(target_job_id: str) -> str:
    event_id, mapped_cell_id, path_segment, role = target_job_id.split("__", 3)
    segment_key = "LEFT" if path_segment == "LEFT_CONNECTOR" else "RIGHT"
    role_key = "MAX_AREA" if role == "MAXIMUM_PHYSICAL_PATH_AREA" else "MIN_GAP"
    return "_".join((event_id, mapped_cell_id, segment_key, role_key))


def target_output(target_job_id: str) -> Path:
    return OUTPUT / target_key(target_job_id)


def connector_targets() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(REPRESENTATIVES_5456)
        if row["path_segment"] in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
    ]


def target_row(target_job_id: str) -> dict[str, str]:
    rows = [row for row in connector_targets() if row["smoke_job_id"] == target_job_id]
    if len(rows) != 1:
        raise RuntimeError(f"expected one connector target {target_job_id}, found {len(rows)}")
    return rows[0]


def source_target_paths(target_job_id: str) -> dict[str, Path]:
    key = target_key(target_job_id)
    coarse = FUNCTIONAL_RG / "5465" / key
    fine = FUNCTIONAL_RG / "5463" / key
    return {
        "coarse_result": coarse / "result.json",
        "coarse_validation": coarse / "validation.csv",
        "coarse_cover": coarse / "projective_pivot_cover.csv",
        "coarse_manifest": coarse / "amplitude_manifest.csv",
        "coarse_work": coarse / "work-v1",
        "fine_result": fine / "result.json",
        "fine_validation": fine / "validation.csv",
        "fine_cover": fine / "projective_pivot_cover.csv",
        "fine_manifest": fine / "amplitude_manifest.csv",
        "fine_work": fine / "work-v1",
    }


def source_paths(target_job_id: str) -> list[Path]:
    sources = source_target_paths(target_job_id)
    return [
        Path(__file__),
        SCRIPT_5396,
        SCRIPT_5456,
        SCRIPT_5463,
        SCRIPT_5465,
        REPRESENTATIVES_5456,
        sources["coarse_result"],
        sources["coarse_validation"],
        sources["coarse_cover"],
        sources["coarse_manifest"],
        sources["fine_result"],
        sources["fine_validation"],
        sources["fine_cover"],
        sources["fine_manifest"],
    ]


def parse_cell_id(cell_id: str) -> tuple[int, int]:
    match = re.fullmatch(r"x(\d+)_t(\d+)", cell_id)
    if match is None:
        raise ValueError(f"invalid finite cell id: {cell_id}")
    return int(match.group(1)), int(match.group(2))


def transformed_manifest_row(
    target: dict[str, str],
    source: dict[str, str],
    source_checkpoint: int,
    depth: int,
    projective_rows: list[dict[str, str]],
) -> dict[str, Any]:
    cell_id = source["projective_owner_cell_id"]
    area_divisor = COARSE_X_SUBDIVISIONS * T_SUBDIVISIONS if depth == COARSE_DEPTH else FINE_X_SUBDIVISIONS * T_SUBDIVISIONS
    return {
        **target,
        "smoke_job_id": f"5466__d{depth}__{cell_id}",
        "parent_target_job_id": target["smoke_job_id"],
        "projective_owner_cell_id": cell_id,
        "selection_role": "5466_LOCALLY_REFINED_FINITE_PROJECTIVE_OWNER_CELL",
        "x_lower": float(source["x_lower"]),
        "x_upper": float(source["x_upper"]),
        "t_lower": float(source["t_lower"]),
        "t_upper": float(source["t_upper"]),
        "physical_path_area_abs_upper": float(target["physical_path_area_abs_upper"]) / area_divisor,
        "refinement_depth": depth,
        "refinement_path": f"{cell_id}__mixed_depth_{depth}",
        "certified_configuration_roles": "|".join(sorted({row["configuration_role"] for row in projective_rows})),
        "certified_owner_pivots": "|".join(sorted({row["owner_pivot"] for row in projective_rows})),
        "minimum_projective_owner_pivot_abs_lower": min(float(row["owner_pivot_abs_lower"]) for row in projective_rows),
        "minimum_projective_unit_circle_abs_lower": min(float(row["unit_circle_abs_lower"]) for row in projective_rows),
        "projective_owner_arc_count": len(projective_rows),
        "source_checkpoint": source_checkpoint,
        "source_smoke_job_id": source["smoke_job_id"],
        "source_projective_owner_cell_id": cell_id,
        "parent_revision": PARENT_REVISION,
        "valid_for_5466_amplitude_manifest": True,
    }


def build_hybrid_cover_and_manifest(
    target_job_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    target = target_row(target_job_id)
    sources = source_target_paths(target_job_id)
    coarse_result = read_json(sources["coarse_result"])
    fine_result = read_json(sources["fine_result"])
    coarse_cover = read_csv(sources["coarse_cover"])
    fine_cover = read_csv(sources["fine_cover"])
    coarse_manifest = read_csv(sources["coarse_manifest"])
    fine_manifest = read_csv(sources["fine_manifest"])
    coarse_manifest_by_cell = {
        row["projective_owner_cell_id"]: row for row in coarse_manifest
    }
    initial_failure_cell_id = str(coarse_result.get("first_failure_cell_id", ""))
    refined_parent_cell_ids = {initial_failure_cell_id}
    existing_work = target_output(target_job_id) / "work-v1"
    if existing_work.is_dir():
        for path in existing_work.glob("*.json"):
            result = read_json(path)
            cell_id = str(result.get("projective_owner_cell_id", ""))
            if (
                not truth(result.get("probe_passed", False))
                and int(result.get("refinement_depth", 0)) == COARSE_DEPTH
                and cell_id in coarse_manifest_by_cell
            ):
                refined_parent_cell_ids.add(cell_id)
    refined_parent_cell_ids.discard("")
    fine_children_by_parent: dict[str, set[str]] = {}
    for parent_cell_id in refined_parent_cell_ids:
        coarse_x_index, t_index = parse_cell_id(parent_cell_id)
        fine_children_by_parent[parent_cell_id] = {
            f"x{2 * coarse_x_index:02d}_t{t_index:02d}",
            f"x{2 * coarse_x_index + 1:02d}_t{t_index:02d}",
        }
    fine_cell_ids = set().union(*fine_children_by_parent.values())
    selected_cover = [
        {**row, "hybrid_refinement_depth": COARSE_DEPTH, "hybrid_source_checkpoint": 5465}
        for row in coarse_cover
        if row["cell_id"] not in refined_parent_cell_ids
    ] + [
        {**row, "hybrid_refinement_depth": FINE_DEPTH, "hybrid_source_checkpoint": 5463}
        for row in fine_cover
        if row["cell_id"] in fine_cell_ids
    ]
    cover_by_cell: dict[str, list[dict[str, Any]]] = {}
    for row in selected_cover:
        cover_by_cell.setdefault(str(row["cell_id"]), []).append(row)
    selected_manifest: list[dict[str, Any]] = []
    for row in coarse_manifest:
        cell_id = row["projective_owner_cell_id"]
        if cell_id in refined_parent_cell_ids:
            continue
        selected_manifest.append(
            transformed_manifest_row(target, row, 5465, COARSE_DEPTH, cover_by_cell[cell_id])
        )
    for row in fine_manifest:
        cell_id = row["projective_owner_cell_id"]
        if cell_id not in fine_cell_ids:
            continue
        selected_manifest.append(
            transformed_manifest_row(target, row, 5463, FINE_DEPTH, cover_by_cell[cell_id])
        )
    selected_manifest.sort(
        key=lambda row: (
            float(row["x_lower"]),
            float(row["t_lower"]),
            float(row["x_upper"]),
        )
    )
    fine_manifest_by_cell = {
        row["projective_owner_cell_id"]: row for row in fine_manifest
    }
    split_checks: list[bool] = []
    area_checks: list[bool] = []
    parent_area = 0.0
    child_area = 0.0
    for parent_cell_id, child_cell_ids in fine_children_by_parent.items():
        parent = coarse_manifest_by_cell[parent_cell_id]
        fine_children = [fine_manifest_by_cell[cell_id] for cell_id in child_cell_ids]
        fine_children.sort(key=lambda row: float(row["x_lower"]))
        split_checks.append(
            math.isclose(float(parent["x_lower"]), float(fine_children[0]["x_lower"]), rel_tol=0.0, abs_tol=1e-15)
            and math.isclose(float(fine_children[0]["x_upper"]), float(fine_children[1]["x_lower"]), rel_tol=0.0, abs_tol=1e-15)
            and math.isclose(float(parent["x_upper"]), float(fine_children[1]["x_upper"]), rel_tol=0.0, abs_tol=1e-15)
            and all(math.isclose(float(parent[key]), float(child[key]), rel_tol=0.0, abs_tol=1e-15) for child in fine_children for key in ("t_lower", "t_upper"))
        )
        current_parent_area = float(parent["physical_path_area_abs_upper"])
        current_child_area = sum(float(row["physical_path_area_abs_upper"]) for row in fine_children)
        area_checks.append(
            math.isclose(current_parent_area, current_child_area, rel_tol=1e-14, abs_tol=1e-24)
        )
        parent_area += current_parent_area
        child_area += current_child_area
    diagnostics = {
        "coarse_first_failure_cell_id": initial_failure_cell_id,
        "refined_parent_cell_ids": sorted(refined_parent_cell_ids),
        "local_refinement_parent_count": len(refined_parent_cell_ids),
        "fine_child_cell_ids": sorted(fine_cell_ids),
        "coarse_source_decision": coarse_result.get("decision", ""),
        "fine_source_decision": fine_result.get("decision", ""),
        "local_split_exact": bool(split_checks) and all(split_checks),
        "local_area_partition_exact": bool(area_checks) and all(area_checks),
        "coarse_parent_area_abs_upper": parent_area,
        "fine_children_area_abs_upper": child_area,
    }
    return selected_cover, selected_manifest, diagnostics


def source_work_path(target_job_id: str, row: dict[str, Any]) -> Path:
    sources = source_target_paths(target_job_id)
    work = sources["coarse_work"] if int(row["source_checkpoint"]) == 5465 else sources["fine_work"]
    return work / f"{row['source_smoke_job_id']}.json"


def certificate_row(
    target: dict[str, str],
    cells: list[dict[str, Any]],
    payload: dict[str, Any],
) -> dict[str, Any]:
    reconstructed_area = sum(float(row["reconstructed_physical_path_area_abs_upper"]) for row in cells)
    geometry_area = float(target["physical_path_area_abs_upper"])
    return {
        "smoke_job_id": target["smoke_job_id"],
        "selection_role": target["selection_role"],
        "event_id": target["event_id"],
        "mapped_cell_id": target["mapped_cell_id"],
        "term_id": target["term_id"],
        "branch_owner_id": target["branch_owner_id"],
        "epsilon_bin_index": int(target["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(target["epsilon_subdivision_index"]),
        "epsilon_subdivision_count": int(target["epsilon_subdivision_count"]),
        "path_segment": target["path_segment"],
        "x_lower": float(target["x_lower"]),
        "x_upper": float(target["x_upper"]),
        "t_lower": float(target["t_lower"]),
        "t_upper": float(target["t_upper"]),
        "geometry_gap_abs_lower": float(target["gap_abs_lower"]),
        "geometry_physical_path_area_abs_upper": geometry_area,
        "probe_passed": True,
        "failure_type": "",
        "failure_message": "",
        "integrated_regular_path_abs_upper": payload["integrated_regular_path_abs_upper"],
        "minimum_amplitude_denominator_abs_lower": payload["minimum_amplitude_denominator_abs_lower"],
        "relative_root_abs_lower": min(float(row["relative_root_abs_lower"]) for row in cells),
        "selected_global_root_abs_lower": min(float(row["selected_global_root_abs_lower"]) for row in cells),
        "collision_jacobian_abs_lower": min(float(row["collision_jacobian_abs_lower"]) for row in cells),
        "active_material_branch_count": max(int(row["active_material_branch_count"]) for row in cells),
        "active_material_branch_ids": "|".join(sorted({branch_id for row in cells for branch_id in str(row["active_material_branch_ids"]).split("|") if branch_id})),
        "path_integral_enclosure_method": "MIXED_DEPTH_8_PLUS_LOCAL_DEPTH_9_POINTWISE_SUPREMUM_SUM",
        "reconstructed_physical_path_area_abs_upper": reconstructed_area,
        "physical_path_area_absolute_error": abs(reconstructed_area - geometry_area),
        "physical_path_area_excess": max(0.0, reconstructed_area - geometry_area),
        "adaptive_subleaf_count": len(cells),
        "refinement_witness_count": 1,
        "maximum_refinement_depth": FINE_DEPTH,
        "unresolved_subleaf_count": 0,
        "runtime_seconds": payload["runtime_seconds"],
        "event_principal_pole_owned_separately": True,
        "certificate_source": "checkpoint_5466_locally_refined_connector_finite_projective_amplitude_cover",
        "parent_revision": PARENT_REVISION,
        "valid_for_outer_parent_leaf_transplant_smoke": True,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_target_document(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# 5466 locally refined connector target: {payload['target_job_id']}",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "The parent-admissible depth-eight cover is retained everywhere except demonstrated coarse amplitude cells whose collision-Jacobian intervals reach zero. Each such parent is replaced exactly by its two depth-nine x-children at fixed t. No threshold, pole ownership or action coefficient is changed.",
        "",
        f"Hybrid leaves completed: `{payload['completed_cell_count']}/{payload['manifest_cell_count']}`. Imported passing depth-eight leaves: `{payload['imported_cell_count']}`. Newly evaluated leaves: `{payload['processed_this_run']}`. Failed leaves: `{payload['failed_cell_count']}`.",
        "",
        "All broader claims remain false.",
        "",
    ]
    atomic_text(path, "\n".join(lines))


def run_target(target_job_id: str, max_jobs: int, cover_only: bool) -> dict[str, Any]:
    set_below_normal_priority()
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths(target_job_id) if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    target = target_row(target_job_id)
    selected_cover, manifest, diagnostics = build_hybrid_cover_and_manifest(target_job_id)
    output = target_output(target_job_id)
    work = output / "work-v1"
    work.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "hybrid_projective_pivot_cover.csv", selected_cover)
    atomic_csv(output / "amplitude_manifest.csv", manifest)
    stable = load_module("mts_5456_for_5466", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5466", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5466", module_5449.PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}")
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    stable.GLOBAL_ARC_COUNT = GLOBAL_ARC_COUNT
    mapped_cells = {row["mapped_cell_id"]: row for row in parent.read_csv(parent.MAPPED_5393)}
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    processed = 0
    imported = 0
    if not cover_only:
        for row in manifest:
            path = work / f"{row['smoke_job_id']}.json"
            if path.is_file():
                existing = read_json(path)
                if not truth(existing.get("probe_passed", False)):
                    break
                continue
            source_path = source_work_path(target_job_id, row)
            if source_path.is_file():
                source_result = read_json(source_path)
                if truth(source_result.get("probe_passed", False)):
                    result = dict(source_result)
                    result.update(
                        {
                            "smoke_job_id": row["smoke_job_id"],
                            "selection_role": row["selection_role"],
                            "parent_target_job_id": target_job_id,
                            "projective_owner_cell_id": row["projective_owner_cell_id"],
                            "refinement_depth": row["refinement_depth"],
                            "refinement_path": row["refinement_path"],
                            "source_checkpoint": row["source_checkpoint"],
                            "source_smoke_job_id": row["source_smoke_job_id"],
                            "certificate_source": "checkpoint_5466_retained_passing_source_cell",
                            "parent_revision": PARENT_REVISION,
                        }
                    )
                    atomic_json(path, result, compact=True)
                    imported += 1
                    continue
            if max_jobs > 0 and processed >= max_jobs:
                break
            result = stable.evaluate_representative(
                parent,
                mapped_cells,
                support_segments,
                branches,
                row,
            )
            result.update(
                {
                    "parent_target_job_id": target_job_id,
                    "projective_owner_cell_id": row["projective_owner_cell_id"],
                    "certified_configuration_roles": row["certified_configuration_roles"],
                    "certified_owner_pivots": row["certified_owner_pivots"],
                    "minimum_projective_owner_pivot_abs_lower": row["minimum_projective_owner_pivot_abs_lower"],
                    "minimum_projective_unit_circle_abs_lower": row["minimum_projective_unit_circle_abs_lower"],
                    "refinement_depth": row["refinement_depth"],
                    "refinement_path": row["refinement_path"],
                    "source_checkpoint": row["source_checkpoint"],
                    "source_smoke_job_id": row["source_smoke_job_id"],
                    "parent_revision": PARENT_REVISION,
                    "certificate_source": "checkpoint_5466_parent_v51_mixed_depth_finite_cell",
                }
            )
            atomic_json(path, result, compact=True)
            processed += 1
            atomic_json(
                output / "status.json",
                {
                    "checkpoint": CHECKPOINT,
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "processed_this_run": processed,
                    "imported_this_run": imported,
                    "last_cell_id": row["projective_owner_cell_id"],
                },
            )
            if not truth(result.get("probe_passed", False)):
                break
    completed = [
        read_json(work / f"{row['smoke_job_id']}.json")
        for row in manifest
        if (work / f"{row['smoke_job_id']}.json").is_file()
    ]
    passed = [row for row in completed if truth(row.get("probe_passed", False))]
    failed = [row for row in completed if not truth(row.get("probe_passed", False))]
    complete = len(completed) == len(manifest) and bool(manifest)
    all_pass = complete and not failed
    projective_passed = [row for row in selected_cover if truth(row["projective_owner_cell_passes"])]
    covered_cells = {row["cell_id"] for row in selected_cover}
    covered_arcs = {int(row["global_arc_index"]) for row in selected_cover}
    minimum_owner_margin = min(float(row["owner_pivot_abs_lower"]) for row in projective_passed)
    minimum_denominator = min((float(row["minimum_amplitude_denominator_abs_lower"]) for row in passed), default=math.nan)
    integrated_upper = sum(float(row["integrated_regular_path_abs_upper"]) for row in passed)
    first_failure = failed[0] if failed else None
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "LOCALLY_REFINED_CONNECTOR_FINITE_COVER_CERTIFIED__RECONCILE_5460" if all_pass else ("LOCALLY_REFINED_CONNECTOR_FIRST_FAILURE__DERIVE" if first_failure is not None else "LOCALLY_REFINED_CONNECTOR_COVER_CERTIFIED__AMPLITUDE_RESUME_REQUIRED"),
        "target_job_id": target_job_id,
        "generic_target_key": target_key(target_job_id),
        **diagnostics,
        "coarse_x_subdivision_count": COARSE_X_SUBDIVISIONS,
        "fine_x_subdivision_count": FINE_X_SUBDIVISIONS,
        "t_subdivision_count": T_SUBDIVISIONS,
        "coarse_binary_partition_depth": COARSE_DEPTH,
        "maximum_binary_partition_depth": FINE_DEPTH,
        "hybrid_parent_cell_count": COARSE_X_SUBDIVISIONS * T_SUBDIVISIONS,
        "hybrid_leaf_cell_count": len(manifest),
        "projective_owner_row_count": len(selected_cover),
        "passed_projective_owner_row_count": len(projective_passed),
        "failed_projective_owner_row_count": len(selected_cover) - len(projective_passed),
        "covered_hybrid_cell_count": len(covered_cells),
        "covered_global_arc_count": len(covered_arcs),
        "minimum_owner_pivot_abs_lower": minimum_owner_margin,
        "manifest_cell_count": len(manifest),
        "completed_cell_count": len(completed),
        "passed_cell_count": len(passed),
        "failed_cell_count": len(failed),
        "remaining_cell_count": len(manifest) - len(completed),
        "imported_cell_count": sum(row.get("certificate_source") == "checkpoint_5466_retained_passing_source_cell" for row in completed),
        "imported_this_run": imported,
        "processed_this_run": processed,
        "minimum_amplitude_denominator_abs_lower": minimum_denominator,
        "integrated_regular_path_abs_upper": integrated_upper,
        "first_failure_cell_id": first_failure["projective_owner_cell_id"] if first_failure is not None else "",
        "first_failure_type": first_failure["failure_type"] if first_failure is not None else "",
        "first_failure_message": first_failure["failure_message"] if first_failure is not None else "",
        "runtime_seconds": time.perf_counter() - started,
        "next_target": "REFRESH_5466_AND_RECONCILE_5460" if all_pass else ("DERIVE_FIRST_FAILED_LOCAL_REFINEMENT_CELL" if first_failure is not None else "RESUME_MIXED_DEPTH_AMPLITUDE_CELLS"),
        "valid_for_target_connector_finite_projective_pivot_cover": len(projective_passed) == len(selected_cover) and bool(selected_cover),
        "valid_for_target_connector_parent_amplitude_cover": all_pass,
        "valid_for_target_outer_representative": all_pass,
        "valid_for_outer_parent_leaf_transplant_smoke": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    expected_area = float(target["physical_path_area_abs_upper"])
    manifest_area = sum(float(row["physical_path_area_abs_upper"]) for row in manifest)
    validations = [
        check("all_sources_exist", not missing, len(source_paths(target_job_id))),
        check("parent_revision_v51_loaded", parent.REVISION == PARENT_REVISION, parent.REVISION),
        check("coarse_source_has_one_local_enclosure_failure", diagnostics["coarse_first_failure_cell_id"] != "" and read_json(source_target_paths(target_job_id)["coarse_result"]).get("failed_cell_count") == 1, diagnostics["coarse_first_failure_cell_id"]),
        check("fine_source_projective_cover_is_complete", read_json(source_target_paths(target_job_id)["fine_result"]).get("valid_for_target_connector_finite_projective_pivot_cover") is True, diagnostics["fine_source_decision"]),
        check("fine_children_exactly_partition_every_failed_parent", diagnostics["local_split_exact"], diagnostics["refined_parent_cell_ids"]),
        check("fine_children_preserve_every_parent_area_weight", diagnostics["local_area_partition_exact"], f"parent={diagnostics['coarse_parent_area_abs_upper']};children={diagnostics['fine_children_area_abs_upper']}"),
        check("hybrid_manifest_has_one_extra_leaf_per_refined_parent", len(manifest) == 256 + diagnostics["local_refinement_parent_count"] and len({row["projective_owner_cell_id"] for row in manifest}) == len(manifest), len(manifest)),
        check("hybrid_manifest_preserves_total_area_weight", math.isclose(manifest_area, expected_area, rel_tol=1e-13, abs_tol=1e-22), f"manifest={manifest_area};target={expected_area}"),
        check("hybrid_projective_cover_has_four_arcs_per_leaf", len(selected_cover) == len(manifest) * GLOBAL_ARC_COUNT and all(len(rows) == GLOBAL_ARC_COUNT for rows in ({cell_id: [row for row in selected_cover if row['cell_id'] == cell_id] for cell_id in covered_cells}).values()), len(selected_cover)),
        check("every_hybrid_projective_owner_row_passes", len(projective_passed) == len(selected_cover) and bool(selected_cover), f"{len(projective_passed)}/{len(selected_cover)}"),
        check("hybrid_depth_contract_is_eight_plus_local_nine", {int(row["refinement_depth"]) for row in manifest} == {COARSE_DEPTH, FINE_DEPTH} and sum(int(row["refinement_depth"]) == FINE_DEPTH for row in manifest) == 2 * diagnostics["local_refinement_parent_count"], sorted({int(row["refinement_depth"]) for row in manifest})),
        check("completed_cells_pass_or_preserve_first_failure", len(completed) == len(passed) + len(failed), f"completed={len(completed)};passed={len(passed)};failed={len(failed)}"),
        check("all_passing_cells_have_positive_finite_denominators", all(math.isfinite(float(row["minimum_amplitude_denominator_abs_lower"])) and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0 for row in passed), minimum_denominator),
        check("complete_certificate_has_every_hybrid_leaf_passing", not all_pass or (len(passed) == len(manifest) and not failed), len(passed)),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_outer_parent_leaf_transplant_smoke"] and not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "single representative only"),
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
        for path in source_paths(target_job_id)
    ]
    atomic_csv(output / "amplitude_cells.csv", completed)
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(output / "validation.csv", validations)
    atomic_json(output / "result.json", payload)
    atomic_json(output / "status.json", payload)
    if all_pass and payload["failed_validation_count"] == 0:
        atomic_csv(output / "representative_certificate.csv", [certificate_row(target, passed, payload)])
    render_target_document(output / "README.md", payload)
    refresh_aggregate()
    return payload


def target_status_row(target: dict[str, str]) -> dict[str, Any]:
    target_job_id = target["smoke_job_id"]
    output = target_output(target_job_id)
    result_path = output / "result.json"
    certificate_path = output / "representative_certificate.csv"
    result = read_json(result_path) if result_path.is_file() else {}
    certified = truth(result.get("valid_for_target_outer_representative", False)) and certificate_path.is_file()
    return {
        "checkpoint": CHECKPOINT,
        "target_job_id": target_job_id,
        "target_key": target_key(target_job_id),
        "event_id": target["event_id"],
        "mapped_cell_id": target["mapped_cell_id"],
        "path_segment": target["path_segment"],
        "selection_role": target["selection_role"],
        "route": "checkpoint_5466_local_refinement",
        "status": "CERTIFIED_LOCAL_REFINEMENT_5466" if certified else ("FIRST_FAILURE" if result.get("first_failure_type") else ("INCOMPLETE" if result else "NOT_RUN")),
        "manifest_cell_count": result.get("manifest_cell_count", ""),
        "completed_cell_count": result.get("completed_cell_count", ""),
        "remaining_cell_count": result.get("remaining_cell_count", ""),
        "minimum_owner_pivot_abs_lower": result.get("minimum_owner_pivot_abs_lower", ""),
        "minimum_amplitude_denominator_abs_lower": result.get("minimum_amplitude_denominator_abs_lower", ""),
        "first_failure_type": result.get("first_failure_type", ""),
        "first_failure_cell_id": result.get("first_failure_cell_id", ""),
        "result_path": str(result_path.resolve()),
        "certificate_path": str(certificate_path.resolve()),
        "valid_for_target_outer_representative": certified,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def render_aggregate(payload: dict[str, Any]) -> None:
    lines = [
        "# 5466: Locally refined D4 connector finite projective amplitude runner",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "A failed depth-eight amplitude cell is replaced exactly by its two depth-nine x-children while every passing depth-eight cell is retained. This realizes finite additivity on a nonuniform dyadic partition and avoids a global depth-nine restart.",
        "",
        f"Certified locally refined targets: `{payload['locally_refined_certified_target_count']}`. Incomplete targets: `{payload['incomplete_target_count']}`. First failures: `{payload['first_failure_target_count']}`.",
        "",
        "All broad claims remain false.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def refresh_aggregate() -> dict[str, Any]:
    rows = [target_status_row(target) for target in connector_targets()]
    certified = [row for row in rows if row["status"] == "CERTIFIED_LOCAL_REFINEMENT_5466"]
    incomplete = [row for row in rows if row["status"] == "INCOMPLETE"]
    failures = [row for row in rows if row["status"] == "FIRST_FAILURE"]
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "LOCAL_REFINEMENT_CERTIFICATES_AVAILABLE__RECONCILE_5460" if certified else ("LOCAL_REFINEMENT_FIRST_FAILURE__DERIVE" if failures else "LOCAL_REFINEMENT_RUNNER_READY"),
        "target_count": len(rows),
        "locally_refined_certified_target_count": len(certified),
        "incomplete_target_count": len(incomplete),
        "first_failure_target_count": len(failures),
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("manifest_has_52_unique_connector_targets", len(rows) == 52 and len({row["target_job_id"] for row in rows}) == 52, len(rows)),
        check("every_local_refinement_certificate_has_a_valid_result", all(truth(row["valid_for_target_outer_representative"]) and Path(row["certificate_path"]).is_file() for row in certified), len(certified)),
        check("aggregate_broad_claims_remain_false", not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "connector representatives only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    static_sources = [Path(__file__), SCRIPT_5456, SCRIPT_5463, SCRIPT_5465, REPRESENTATIVES_5456]
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in static_sources
    ]
    atomic_csv(TARGET_STATUS, rows)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(STATUS, payload)
    atomic_json(RESULT, payload)
    render_aggregate(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-job-id")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--cover-only", action="store_true")
    parser.add_argument("--refresh-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    if arguments.refresh_only:
        print(json.dumps(refresh_aggregate(), indent=2, sort_keys=True))
        return 0
    if not arguments.target_job_id:
        raise ValueError("--target-job-id is required")
    payload = run_target(arguments.target_job_id, arguments.max_jobs, arguments.cover_only)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
