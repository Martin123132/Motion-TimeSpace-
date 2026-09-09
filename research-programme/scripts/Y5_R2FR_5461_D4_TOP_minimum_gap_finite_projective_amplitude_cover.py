from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
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
OUTPUT = FUNCTIONAL_RG / "5461"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5457 = SCRIPTS / "Y5_R2FR_5457_D4_TOP_finite_projective_pivot_cover.py"
SCRIPT_5459 = SCRIPTS / "Y5_R2FR_5459_D4_TOP_left_external41_projective_edge_transplant.py"
DOCUMENT_5457 = POST / "5457-Y5-R2FR-D4-TOP-finite-projective-pivot-cover.md"
DOCUMENT_5459 = POST / "5459-Y5-R2FR-D4-TOP-left-external41-projective-edge-transplant.md"
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
RESULT_5457 = (
    FUNCTIONAL_RG / "5457" / "D4_TOP_finite_projective_pivot_cover_result.json"
)
RESULT_5459 = (
    FUNCTIONAL_RG / "5459" / "D4_TOP_left_external41_projective_edge_result.json"
)

DOCUMENT = POST / "5461-Y5-R2FR-D4-TOP-minimum-gap-finite-projective-amplitude-cover.md"
COVER = OUTPUT / "D4_TOP_minimum_gap_projective_pivot_cover.csv"
OWNER_SUMMARY = OUTPUT / "D4_TOP_minimum_gap_projective_owner_summary.csv"
MANIFEST = OUTPUT / "D4_TOP_minimum_gap_amplitude_manifest.csv"
CELL_RESULTS = OUTPUT / "D4_TOP_minimum_gap_amplitude_cells.csv"
REPRESENTATIVE_CERTIFICATE = OUTPUT / "D4_TOP_minimum_gap_representative_certificate.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5461_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_TOP_minimum_gap_finite_cover_result.json"

CHECKPOINT = 5461
REVISION = "D4-TOP-minimum-gap-finite-projective-amplitude-cover-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
TARGET_JOB_ID = "E01__U017__TOP__MINIMUM_CERTIFIED_OUTER_GAP"
X_SUBDIVISIONS = 16
T_SUBDIVISIONS = 32
GLOBAL_ARC_COUNT = 4
CERTIFIED_BINARY_PARTITION_DEPTH = 9


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
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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
    fields: list[str] = []
    known: set[str] = set()
    for row in rows:
        for field in row:
            if field not in known:
                fields.append(field)
                known.add(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


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


def source_paths() -> list[Path]:
    return [
        SCRIPT_5396,
        SCRIPT_5456,
        SCRIPT_5457,
        SCRIPT_5459,
        DOCUMENT_5457,
        DOCUMENT_5459,
        REPRESENTATIVES_5456,
        RESULT_5457,
        RESULT_5459,
    ]


def target_row() -> dict[str, str]:
    matches = [
        row
        for row in read_csv(REPRESENTATIVES_5456)
        if row["smoke_job_id"] == TARGET_JOB_ID
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one {TARGET_JOB_ID} representative, found {len(matches)}"
        )
    return matches[0]


def amplitude_manifest(
    target: dict[str, str], cover: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in cover:
        grouped.setdefault(str(row["cell_id"]), []).append(row)
    manifest: list[dict[str, Any]] = []
    for cell_id, rows in sorted(grouped.items()):
        if not rows or not all(row["projective_owner_cell_passes"] for row in rows):
            raise RuntimeError(f"uncertified projective cell {cell_id}")
        first = rows[0]
        manifest.append(
            {
                **target,
                "smoke_job_id": f"5461__{cell_id}",
                "parent_target_job_id": TARGET_JOB_ID,
                "projective_owner_cell_id": cell_id,
                "selection_role": "5461_FINITE_PROJECTIVE_OWNER_CELL",
                "x_lower": float(first["x_lower"]),
                "x_upper": float(first["x_upper"]),
                "t_lower": float(first["t_lower"]),
                "t_upper": float(first["t_upper"]),
                "physical_path_area_abs_upper": float(
                    target["physical_path_area_abs_upper"]
                )
                / (X_SUBDIVISIONS * T_SUBDIVISIONS),
                "refinement_depth": CERTIFIED_BINARY_PARTITION_DEPTH,
                "refinement_path": f"{cell_id}__finite_projective_depth9",
                "certified_configuration_roles": "|".join(
                    sorted({str(row["configuration_role"]) for row in rows})
                ),
                "certified_owner_pivots": "|".join(
                    sorted({str(row["owner_pivot"]) for row in rows})
                ),
                "minimum_projective_owner_pivot_abs_lower": min(
                    float(row["owner_pivot_abs_lower"]) for row in rows
                ),
                "minimum_projective_unit_circle_abs_lower": min(
                    float(row["unit_circle_abs_lower"]) for row in rows
                ),
                "projective_owner_arc_count": len(rows),
                "parent_revision": PARENT_REVISION,
                "valid_for_5461_amplitude_manifest": True,
            }
        )
    return manifest


def representative_certificate(
    target: dict[str, str],
    cells: list[dict[str, Any]],
    payload: dict[str, Any],
) -> dict[str, Any]:
    reconstructed_area = sum(
        float(row["reconstructed_physical_path_area_abs_upper"]) for row in cells
    )
    geometry_area = float(target["physical_path_area_abs_upper"])
    return {
        "smoke_job_id": TARGET_JOB_ID,
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
        "integrated_regular_path_abs_upper": payload[
            "integrated_regular_path_abs_upper"
        ],
        "minimum_amplitude_denominator_abs_lower": payload[
            "minimum_amplitude_denominator_abs_lower"
        ],
        "relative_root_abs_lower": min(
            float(row["relative_root_abs_lower"]) for row in cells
        ),
        "selected_global_root_abs_lower": min(
            float(row["selected_global_root_abs_lower"]) for row in cells
        ),
        "collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in cells
        ),
        "active_material_branch_count": max(
            int(row["active_material_branch_count"]) for row in cells
        ),
        "active_material_branch_ids": "|".join(
            sorted(
                {
                    branch_id
                    for row in cells
                    for branch_id in str(row["active_material_branch_ids"]).split("|")
                    if branch_id
                }
            )
        ),
        "path_integral_enclosure_method": "FINITE_16X32_POINTWISE_SUPREMUM_SUM",
        "reconstructed_physical_path_area_abs_upper": reconstructed_area,
        "physical_path_area_absolute_error": abs(reconstructed_area - geometry_area),
        "physical_path_area_excess": max(0.0, reconstructed_area - geometry_area),
        "adaptive_subleaf_count": len(cells),
        "refinement_witness_count": 0,
        "maximum_refinement_depth": CERTIFIED_BINARY_PARTITION_DEPTH,
        "unresolved_subleaf_count": 0,
        "runtime_seconds": payload["runtime_seconds"],
        "event_principal_pole_owned_separately": True,
        "certificate_source": "checkpoint_5461_finite_projective_amplitude_cover",
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


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5461: D4 TOP minimum-gap finite projective amplitude cover",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Construction",
        "",
        "The exact checkpoint-5457 massless determinant theorem is reused at epsilon bin 7, but every selector, pivot margin and amplitude cell is recomputed for this representative. The same `16 x 32` x/t partition and four contour arcs are used; no checkpoint-5459 numerical margin is copied across epsilon bins.",
        "",
        f"Projective rows passed: `{payload['passed_projective_owner_row_count']}/{payload['projective_owner_row_count']}`. Amplitude cells completed: `{payload['completed_cell_count']}/{payload['manifest_cell_count']}`; passed: `{payload['passed_cell_count']}`; failed: `{payload['failed_cell_count']}`.",
        "",
        "## Claim boundary",
        "",
        "A complete pass certifies only `E01__U017__TOP__MINIMUM_CERTIFIED_OUTER_GAP`. The other outer representatives, all outer leaves, event-local W3, the regulator limit, local GR and full MTS remain open.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(max_jobs: int, cover_only: bool = False) -> dict[str, Any]:
    set_below_normal_priority()
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    target = target_row()
    stable = load_module("mts_5456_for_5461", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5461", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5461", module_5449.PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
        )
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    stable.GLOBAL_ARC_COUNT = GLOBAL_ARC_COUNT
    cover_module = load_module("mts_5457_for_5461", SCRIPT_5457)
    cover_module.TARGET_JOB_ID = TARGET_JOB_ID
    cover_module.X_SUBDIVISIONS = X_SUBDIVISIONS
    cover_module.T_SUBDIVISIONS = T_SUBDIVISIONS
    cover_module.GLOBAL_ARC_COUNT = GLOBAL_ARC_COUNT
    symbolic = cover_module.symbolic_massless_determinant_certificate()
    cover, cover_diagnostics = cover_module.projective_cover(parent, stable, target)
    owner_summary = cover_module.owner_summary(cover)
    passed_cover = [row for row in cover if row["projective_owner_cell_passes"]]
    covered_cells = {row["cell_id"] for row in cover}
    covered_arcs = {int(row["global_arc_index"]) for row in cover}
    cover_pass = (
        bool(cover)
        and len(passed_cover) == len(cover)
        and cover_diagnostics["selector_failure_count"] == 0
        and len(covered_cells) == X_SUBDIVISIONS * T_SUBDIVISIONS
        and len(covered_arcs) == GLOBAL_ARC_COUNT
        and symbolic["symbolic_massless_determinant_identity_valid"]
    )
    atomic_csv(COVER, cover)
    atomic_csv(OWNER_SUMMARY, owner_summary)
    manifest = amplitude_manifest(target, cover) if cover_pass else []
    if manifest:
        atomic_csv(MANIFEST, manifest)
    mapped_cells = {
        row["mapped_cell_id"]: row
        for row in parent.read_csv(parent.MAPPED_5393)
    }
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    WORK.mkdir(parents=True, exist_ok=True)
    processed = 0
    if not cover_only and cover_pass:
        for row in manifest:
            path = WORK / f"{row['smoke_job_id']}.json"
            if path.is_file():
                existing = read_json(path)
                if not existing["probe_passed"]:
                    break
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
                    "parent_target_job_id": TARGET_JOB_ID,
                    "projective_owner_cell_id": row["projective_owner_cell_id"],
                    "certified_configuration_roles": row[
                        "certified_configuration_roles"
                    ],
                    "certified_owner_pivots": row["certified_owner_pivots"],
                    "minimum_projective_owner_pivot_abs_lower": row[
                        "minimum_projective_owner_pivot_abs_lower"
                    ],
                    "minimum_projective_unit_circle_abs_lower": row[
                        "minimum_projective_unit_circle_abs_lower"
                    ],
                    "parent_revision": PARENT_REVISION,
                    "certificate_source": "checkpoint_5461_parent_v51_finite_cell",
                }
            )
            atomic_json(path, result, compact=True)
            processed += 1
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "updated_utc": datetime.now(timezone.utc).isoformat(),
                    "processed_this_run": processed,
                    "last_cell_id": row["projective_owner_cell_id"],
                },
            )
            if not result["probe_passed"]:
                break
    completed = [
        read_json(WORK / f"{row['smoke_job_id']}.json")
        for row in manifest
        if (WORK / f"{row['smoke_job_id']}.json").is_file()
    ]
    passed = [row for row in completed if row["probe_passed"]]
    failed = [row for row in completed if not row["probe_passed"]]
    complete = len(completed) == len(manifest) and bool(manifest)
    all_pass = cover_pass and complete and not failed
    minimum_owner_margin = min(
        (float(row["owner_pivot_abs_lower"]) for row in passed_cover),
        default=math.nan,
    )
    minimum_denominator = min(
        (float(row["minimum_amplitude_denominator_abs_lower"]) for row in passed),
        default=math.nan,
    )
    integrated_upper = sum(
        float(row["integrated_regular_path_abs_upper"]) for row in passed
    )
    first_failure = failed[0] if failed else None
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "TOP_MINIMUM_GAP_FINITE_PROJECTIVE_AMPLITUDE_COVER_CERTIFIED__RECONCILE_5460"
            if all_pass
            else (
                "TOP_MINIMUM_GAP_AMPLITUDE_FIRST_FAILURE__DERIVE"
                if first_failure is not None
                else (
                    "TOP_MINIMUM_GAP_PROJECTIVE_COVER_CERTIFIED__AMPLITUDE_RESUME_REQUIRED"
                    if cover_pass
                    else "TOP_MINIMUM_GAP_PROJECTIVE_COVER_NOT_CLOSED"
                )
            )
        ),
        **symbolic,
        **cover_diagnostics,
        "target_job_id": TARGET_JOB_ID,
        "projective_owner_row_count": len(cover),
        "passed_projective_owner_row_count": len(passed_cover),
        "failed_projective_owner_row_count": len(cover) - len(passed_cover),
        "covered_xt_cell_count": len(covered_cells),
        "covered_global_arc_count": len(covered_arcs),
        "minimum_owner_pivot_abs_lower": minimum_owner_margin,
        "manifest_cell_count": len(manifest),
        "completed_cell_count": len(completed),
        "passed_cell_count": len(passed),
        "failed_cell_count": len(failed),
        "remaining_cell_count": len(manifest) - len(completed),
        "processed_this_run": processed,
        "minimum_amplitude_denominator_abs_lower": minimum_denominator,
        "integrated_regular_path_abs_upper": integrated_upper,
        "first_failure_cell_id": (
            first_failure["projective_owner_cell_id"]
            if first_failure is not None
            else ""
        ),
        "first_failure_type": (
            first_failure["failure_type"] if first_failure is not None else ""
        ),
        "first_failure_message": (
            first_failure["failure_message"] if first_failure is not None else ""
        ),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": (
            "RECONCILE_TARGET_IN_CHECKPOINT_5460"
            if all_pass
            else (
                "DERIVE_FIRST_FAILED_AMPLITUDE_DENOMINATOR"
                if first_failure is not None
                else "RESUME_FINITE_AMPLITUDE_CELLS"
            )
        ),
        "valid_for_target_TOP_finite_projective_pivot_cover": cover_pass,
        "valid_for_target_TOP_parent_amplitude_cover": all_pass,
        "valid_for_target_outer_representative": all_pass,
        "valid_for_outer_parent_leaf_transplant_smoke": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("parent_revision_v51_loaded", parent.REVISION == PARENT_REVISION, parent.REVISION),
        check("massless_determinant_identity_exact", symbolic["symbolic_massless_determinant_identity_valid"], symbolic["groebner_remainder"]),
        check("all_512_xt_cells_covered", len(covered_cells) == X_SUBDIVISIONS * T_SUBDIVISIONS, len(covered_cells)),
        check("all_four_global_arcs_covered", len(covered_arcs) == GLOBAL_ARC_COUNT, sorted(covered_arcs)),
        check("selector_has_no_uncovered_cell", cover_diagnostics["selector_failure_count"] == 0, cover_diagnostics["selector_failure_count"]),
        check("every_projective_owner_row_passes", len(passed_cover) == len(cover) and bool(cover), f"{len(passed_cover)}/{len(cover)}"),
        check("owned_pivot_margin_is_positive", minimum_owner_margin > 0.0, minimum_owner_margin),
        check("manifest_covers_every_unique_grid_cell_if_cover_passes", not cover_pass or (len(manifest) == X_SUBDIVISIONS * T_SUBDIVISIONS and len({row["projective_owner_cell_id"] for row in manifest}) == X_SUBDIVISIONS * T_SUBDIVISIONS), len(manifest)),
        check("completed_cells_pass_or_preserve_first_failure", len(completed) == len(passed) + len(failed), f"completed={len(completed)};passed={len(passed)};failed={len(failed)}"),
        check("all_passing_cells_have_positive_finite_denominators", all(math.isfinite(float(row["minimum_amplitude_denominator_abs_lower"])) and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0 for row in passed), minimum_denominator),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_outer_parent_leaf_transplant_smoke"] and not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "single representative only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    if completed:
        atomic_csv(CELL_RESULTS, completed)
    if all_pass:
        atomic_csv(
            REPRESENTATIVE_CERTIFICATE,
            [representative_certificate(target, completed, payload)],
        )
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--cover-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.max_jobs, arguments.cover_only)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
