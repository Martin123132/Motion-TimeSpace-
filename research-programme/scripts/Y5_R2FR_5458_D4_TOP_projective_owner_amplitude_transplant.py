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
OUTPUT = FUNCTIONAL_RG / "5458"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5457 = SCRIPTS / "Y5_R2FR_5457_D4_TOP_finite_projective_pivot_cover.py"
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
COVER_5457 = FUNCTIONAL_RG / "5457" / "D4_TOP_finite_projective_pivot_cover.csv"
RESULT_5457 = (
    FUNCTIONAL_RG / "5457" / "D4_TOP_finite_projective_pivot_cover_result.json"
)

DOCUMENT = POST / "5458-Y5-R2FR-D4-TOP-projective-owner-amplitude-transplant.md"
MANIFEST = OUTPUT / "D4_TOP_projective_owner_amplitude_manifest.csv"
CELL_RESULTS = OUTPUT / "D4_TOP_projective_owner_amplitude_cells.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5458_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_TOP_projective_owner_amplitude_result.json"

CHECKPOINT = 5458
REVISION = "D4-TOP-projective-owner-amplitude-transplant-v1"
TARGET_JOB_ID = "E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA"
GLOBAL_ARC_COUNT = 4


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
        REPRESENTATIVES_5456,
        COVER_5457,
        RESULT_5457,
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


def manifest_rows(target: dict[str, str]) -> list[dict[str, Any]]:
    cover = read_csv(COVER_5457)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in cover:
        if row["target_job_id"] != TARGET_JOB_ID:
            continue
        grouped.setdefault(row["cell_id"], []).append(row)
    manifest: list[dict[str, Any]] = []
    cell_count = len(grouped)
    for cell_id, rows in sorted(grouped.items()):
        if not all(row["projective_owner_cell_passes"] == "True" for row in rows):
            raise RuntimeError(f"uncertified 5457 owner cell {cell_id}")
        first = rows[0]
        manifest.append(
            {
                **target,
                "smoke_job_id": f"5458__{cell_id}",
                "parent_target_job_id": TARGET_JOB_ID,
                "projective_owner_cell_id": cell_id,
                "selection_role": "5457_PROJECTIVE_OWNER_CELL",
                "x_lower": float(first["x_lower"]),
                "x_upper": float(first["x_upper"]),
                "t_lower": float(first["t_lower"]),
                "t_upper": float(first["t_upper"]),
                "gap_abs_lower": float(target["gap_abs_lower"]),
                "physical_path_area_abs_upper": float(
                    target["physical_path_area_abs_upper"]
                )
                / cell_count,
                "refinement_depth": 1,
                "refinement_path": cell_id,
                "certified_configuration_roles": "|".join(
                    sorted({row["configuration_role"] for row in rows})
                ),
                "certified_owner_pivots": "|".join(
                    sorted({row["owner_pivot"] for row in rows})
                ),
                "minimum_projective_owner_pivot_abs_lower": min(
                    float(row["owner_pivot_abs_lower"]) for row in rows
                ),
                "minimum_projective_unit_circle_abs_lower": min(
                    float(row["unit_circle_abs_lower"]) for row in rows
                ),
                "projective_owner_arc_count": len(rows),
                "valid_for_5458_amplitude_transplant_manifest": True,
            }
        )
    return manifest


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5458: D4 TOP projective-owner amplitude transplant",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Construction",
        "",
        "Checkpoint 5457 proves a finite selector-aware projective cover of the previously blocked E01/U017 TOP box. This checkpoint applies the unchanged checkpoint-5396 amplitude evaluator separately on each of those closed owner cells. The operation is a finite domain partition, not a fitted closure or a change to the amplitude.",
        "",
        f"Completed cells: `{payload['completed_cell_count']}/{payload['manifest_cell_count']}`. Passed cells: `{payload['passed_cell_count']}`. Failed cells: `{payload['failed_cell_count']}`.",
        "",
        "## Claim boundary",
        "",
        "A complete pass certifies only this one TOP representative's parent-amplitude enclosure. The remaining checkpoint-5456 representatives, complete outer atlas, event-local W3, regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(max_jobs: int, status_only: bool = False) -> dict[str, Any]:
    set_below_normal_priority()
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5457 = read_json(RESULT_5457)
    if result_5457.get("valid_for_target_TOP_finite_projective_pivot_cover") is not True:
        raise RuntimeError("checkpoint 5457 projective cover is not valid")
    target = target_row()
    manifest = manifest_rows(target)
    atomic_csv(MANIFEST, manifest)
    stable = load_module("mts_5456_for_5458", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5458", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5458", module_5449.PARENT_SCRIPT)
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    stable.GLOBAL_ARC_COUNT = GLOBAL_ARC_COUNT
    cells = {
        row["mapped_cell_id"]: row
        for row in parent.read_csv(parent.MAPPED_5393)
    }
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    WORK.mkdir(parents=True, exist_ok=True)
    processed = 0
    for row in manifest:
        path = WORK / f"{row['smoke_job_id']}.json"
        if path.is_file():
            continue
        if status_only:
            break
        if max_jobs > 0 and processed >= max_jobs:
            break
        result = stable.evaluate_representative(
            parent,
            cells,
            support_segments,
            branches,
            row,
        )
        result.update(
            {
                "parent_target_job_id": TARGET_JOB_ID,
                "projective_owner_cell_id": row[
                    "projective_owner_cell_id"
                ],
                "certified_configuration_roles": row[
                    "certified_configuration_roles"
                ],
                "certified_owner_pivots": row[
                    "certified_owner_pivots"
                ],
                "minimum_projective_owner_pivot_abs_lower": row[
                    "minimum_projective_owner_pivot_abs_lower"
                ],
                "minimum_projective_unit_circle_abs_lower": row[
                    "minimum_projective_unit_circle_abs_lower"
                ],
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
    completed = [
        read_json(WORK / f"{row['smoke_job_id']}.json")
        for row in manifest
        if (WORK / f"{row['smoke_job_id']}.json").is_file()
    ]
    passed = [row for row in completed if row["probe_passed"]]
    complete = len(completed) == len(manifest)
    all_pass = complete and len(passed) == len(manifest)
    failure_counts: dict[str, int] = {}
    for row in completed:
        if row["probe_passed"]:
            continue
        category = f"{row['failure_type']}:{row['failure_message']}"
        failure_counts[category] = failure_counts.get(category, 0) + 1
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "TOP_PROJECTIVE_OWNER_AMPLITUDE_COVER_CERTIFIED__RESUME_OUTER_SMOKE"
            if all_pass
            else (
                "TOP_PROJECTIVE_OWNER_AMPLITUDE_EXPOSES_NEXT_DENOMINATOR"
                if complete or failure_counts
                else "TOP_PROJECTIVE_OWNER_AMPLITUDE_RESUME_REQUIRED"
            )
        ),
        "manifest_cell_count": len(manifest),
        "completed_cell_count": len(completed),
        "remaining_cell_count": len(manifest) - len(completed),
        "passed_cell_count": len(passed),
        "failed_cell_count": len(completed) - len(passed),
        "failure_counts": failure_counts,
        "processed_this_run": processed,
        "minimum_projective_owner_pivot_abs_lower": min(
            (
                float(row["minimum_projective_owner_pivot_abs_lower"])
                for row in completed
            ),
            default=math.nan,
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            (
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in passed
            ),
            default=math.nan,
        ),
        "integrated_regular_path_abs_upper": sum(
            float(row["integrated_regular_path_abs_upper"])
            for row in passed
        ),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": (
            "RESUME_CHECKPOINT_5456_OUTER_REPRESENTATIVES"
            if all_pass
            else "DERIVE_FIRST_FAILED_AMPLITUDE_DENOMINATOR"
        ),
        "valid_for_target_TOP_parent_amplitude_cover": all_pass,
        "valid_for_outer_parent_leaf_transplant_smoke": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("checkpoint_5457_projective_cover_valid", result_5457.get("valid_for_target_TOP_finite_projective_pivot_cover") is True, result_5457.get("decision")),
        check("manifest_has_512_unique_cells", len(manifest) == 512 and len({row["projective_owner_cell_id"] for row in manifest}) == 512, len(manifest)),
        check("all_completed_cells_pass_or_are_preserved_as_failures", len(completed) == len(passed) + sum(failure_counts.values()), f"completed={len(completed)};passed={len(passed)};failed={sum(failure_counts.values())}"),
        check("all_passing_cells_have_positive_amplitude_denominator", all(float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0 for row in passed), payload["minimum_amplitude_denominator_abs_lower"]),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not payload["valid_for_outer_parent_leaf_transplant_smoke"] and not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "single target only"),
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
    if completed:
        atomic_csv(CELL_RESULTS, completed)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--status-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.max_jobs, arguments.status_only)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
