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
OUTPUT = FUNCTIONAL_RG / "5459"
WORK = OUTPUT / "work-v2"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5457 = SCRIPTS / "Y5_R2FR_5457_D4_TOP_finite_projective_pivot_cover.py"
SCRIPT_5458 = SCRIPTS / "Y5_R2FR_5458_D4_TOP_projective_owner_amplitude_transplant.py"
DOCUMENT_5430 = POST / "5430-Y5-R2FR-D4-representative-external41-mirror-disk-gate.md"
DOCUMENT_5431 = POST / "5431-Y5-R2FR-D4-v46-bounded-production-progress-gate.md"
DOCUMENT_5457 = POST / "5457-Y5-R2FR-D4-TOP-finite-projective-pivot-cover.md"
DOCUMENT_5458 = POST / "5458-Y5-R2FR-D4-TOP-projective-owner-amplitude-transplant.md"
MANIFEST_5458 = (
    FUNCTIONAL_RG / "5458" / "D4_TOP_projective_owner_amplitude_manifest.csv"
)
CELLS_5458 = (
    FUNCTIONAL_RG / "5458" / "D4_TOP_projective_owner_amplitude_cells.csv"
)
RESULT_5457 = (
    FUNCTIONAL_RG / "5457" / "D4_TOP_finite_projective_pivot_cover_result.json"
)
RESULT_5458 = (
    FUNCTIONAL_RG / "5458" / "D4_TOP_projective_owner_amplitude_result.json"
)
SOURCE_REGISTER_5458 = FUNCTIONAL_RG / "5458" / "source_register.csv"

DOCUMENT = POST / "5459-Y5-R2FR-D4-TOP-left-external41-projective-edge-transplant.md"
RERUN_MANIFEST = OUTPUT / "D4_TOP_left_external41_rerun_manifest.csv"
RERUN_RESULTS = OUTPUT / "D4_TOP_left_external41_rerun_cells.csv"
COMBINED_RESULTS = OUTPUT / "D4_TOP_parent_amplitude_combined_certificate.csv"
DERIVATION = OUTPUT / "D4_left_external41_exact_projective_identities.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5459_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_TOP_left_external41_projective_edge_result.json"

CHECKPOINT = 5459
REVISION = "D4-TOP-left-external41-projective-edge-transplant-v2"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
TARGET_JOB_ID = "E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA"
GLOBAL_ARC_COUNT = 4
CERTIFIED_BINARY_PARTITION_DEPTH = 9
EXPECTED_5458_FAILURE_COUNT = 133
EXPECTED_FAILURE = (
    "IntervalSingularity:interval denominator reaches zero: "
    "away_arc_left_K5:s2:c0:right0:edge_1_4_1:stable_edge"
)


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
        SCRIPT_5458,
        DOCUMENT_5430,
        DOCUMENT_5431,
        DOCUMENT_5457,
        DOCUMENT_5458,
        MANIFEST_5458,
        CELLS_5458,
        RESULT_5457,
        RESULT_5458,
        SOURCE_REGISTER_5458,
    ]


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "L41_1_fixed_left_external4_momentum",
            "projective_family": "all",
            "chirality": "all",
            "input": "p4_left=(-1,0,0,+1)",
            "derived_spinor_or_edge": "lambda4=(0,-2); tilde_lambda4=(0,1)",
            "proof_role": "direct rational massless-spinor chart",
            "status": "EXACT",
            "valid_for_claim": True,
        },
        {
            "identity_id": "L41_2_plus_family_angle",
            "projective_family": "plus",
            "chirality": "angle",
            "input": "lambda1=(p1_plus,p1_holomorphic)",
            "derived_spinor_or_edge": "<1,4>=-2*p1_plus",
            "proof_role": "two-component determinant",
            "status": "EXACT",
            "valid_for_claim": True,
        },
        {
            "identity_id": "L41_3_plus_family_square",
            "projective_family": "plus",
            "chirality": "square",
            "input": "tilde_lambda1=(1,q1)",
            "derived_spinor_or_edge": "[1,4]=1",
            "proof_role": "two-component determinant",
            "status": "EXACT",
            "valid_for_claim": True,
        },
        {
            "identity_id": "L41_4_minus_family_angle",
            "projective_family": "minus",
            "chirality": "angle",
            "input": "lambda1=(p1_antiholomorphic,p1_minus)",
            "derived_spinor_or_edge": "<1,4>=-2*p1_antiholomorphic",
            "proof_role": "two-component determinant",
            "status": "EXACT",
            "valid_for_claim": True,
        },
        {
            "identity_id": "L41_5_minus_family_square",
            "projective_family": "minus",
            "chirality": "square",
            "input": "tilde_lambda1=(q1,1)",
            "derived_spinor_or_edge": "[1,4]=q1",
            "proof_role": "two-component determinant",
            "status": "EXACT",
            "valid_for_claim": True,
        },
        {
            "identity_id": "L41_6_subcover_transplant",
            "projective_family": "selector_owned",
            "chirality": "both",
            "input": "checkpoint-5457 closed projective owner cell",
            "derived_spinor_or_edge": "hull of exact subcell determinants",
            "proof_role": "finite interval union; no denominator deletion",
            "status": "CERTIFIED_IF_ALL_SUBCELL_EDGE_LOWER_BOUNDS_POSITIVE",
            "valid_for_claim": True,
        },
    ]


def rerun_manifest_rows() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    manifest = read_csv(MANIFEST_5458)
    old_cells = read_csv(CELLS_5458)
    failed_ids = {
        row["projective_owner_cell_id"]
        for row in old_cells
        if not truth(row["probe_passed"])
    }
    rows: list[dict[str, Any]] = []
    for row in manifest:
        cell_id = row["projective_owner_cell_id"]
        if cell_id not in failed_ids:
            continue
        current: dict[str, Any] = dict(row)
        current.update(
            {
                "smoke_job_id": f"5459__{cell_id}",
                "selection_role": "5459_LEFT_EXTERNAL41_PROJECTIVE_EDGE_RERUN",
                "refinement_depth": CERTIFIED_BINARY_PARTITION_DEPTH,
                "refinement_path": f"{cell_id}__left_external41_v50",
                "parent_revision": PARENT_REVISION,
                "binary_partition_depth_derivation": "log2(16)+log2(32)=9",
                "valid_for_5459_left_external41_rerun_manifest": True,
            }
        )
        rows.append(current)
    return rows, old_cells


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def finite_partition_is_closed(manifest: list[dict[str, str]]) -> bool:
    x_intervals = sorted(
        {(float(row["x_lower"]), float(row["x_upper"])) for row in manifest}
    )
    t_intervals = sorted(
        {(float(row["t_lower"]), float(row["t_upper"])) for row in manifest}
    )
    if len(x_intervals) != 16 or len(t_intervals) != 32:
        return False
    if any(
        not math.isclose(x_intervals[index][1], x_intervals[index + 1][0])
        for index in range(len(x_intervals) - 1)
    ):
        return False
    if any(
        not math.isclose(t_intervals[index][1], t_intervals[index + 1][0])
        for index in range(len(t_intervals) - 1)
    ):
        return False
    cells = {
        (
            float(row["x_lower"]),
            float(row["x_upper"]),
            float(row["t_lower"]),
            float(row["t_upper"]),
        )
        for row in manifest
    }
    expected = {
        (x_lower, x_upper, t_lower, t_upper)
        for x_lower, x_upper in x_intervals
        for t_lower, t_upper in t_intervals
    }
    return cells == expected


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5459: D4 TOP left external-41 projective edge transplant",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Derived repair",
        "",
        "Checkpoint 5458 removed the first-spinor pivot obstruction but preserved 133 failures of the same left-cut edge. The failed edge is not the right-cut external-41 object treated by checkpoints 5430-5431. On the left cut, `p4=(-1,0,0,+1)` has exact rational spinors `lambda4=(0,-2)` and `tilde_lambda4=(0,1)`. Therefore `<1,4>=-2 p1_plus` in the plus family and `<1,4>=-2 p1_antiholomorphic` in the minus family; the matching square edges follow from the same two-component determinants.",
        "",
        "Parent revision v51 evaluates those exact determinants on a finite subcover of each already-certified checkpoint-5457 projective cell. When the coarse normalization obscures an edge, it rebuilds the complete first-spinor pair in one surviving projective family before any amplitude factor is evaluated. It installs an edge-only fallback only when the family is unchanged. No pole is deleted, no fitted parameter is introduced, and the amplitude is unchanged.",
        "",
        "## Result",
        "",
        f"Rerun cells completed: `{payload['rerun_completed_cell_count']}/{payload['rerun_manifest_cell_count']}`; passed: `{payload['rerun_passed_cell_count']}`; failed: `{payload['rerun_failed_cell_count']}`.",
        f"Combined TOP cells certified: `{payload['combined_passed_cell_count']}/{payload['combined_cell_count']}`. Minimum projective margin: `{payload['minimum_projective_owner_pivot_abs_lower']}`. Minimum amplitude denominator: `{payload['minimum_amplitude_denominator_abs_lower']}`.",
        "",
        "## Claim boundary",
        "",
        "A complete pass closes only the E01/U017 TOP parent-amplitude box. The remaining checkpoint-5456 outer representatives, full event-cell cover, event-local W3, regulator limit, local GR and full MTS claims remain open.",
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
    result_5458 = read_json(RESULT_5458)
    manifest_5458 = read_csv(MANIFEST_5458)
    rerun_manifest, old_cells = rerun_manifest_rows()
    old_passed = [dict(row) for row in old_cells if truth(row["probe_passed"])]
    old_failed = [row for row in old_cells if not truth(row["probe_passed"])]
    old_failure_counts: dict[str, int] = {}
    for row in old_failed:
        category = f"{row['failure_type']}:{row['failure_message']}"
        old_failure_counts[category] = old_failure_counts.get(category, 0) + 1
    atomic_csv(RERUN_MANIFEST, rerun_manifest)
    atomic_csv(DERIVATION, derivation_rows())
    stable = load_module("mts_5456_for_5459", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5459", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5459", module_5449.PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
        )
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
    for row in rerun_manifest:
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
                "projective_owner_cell_id": row["projective_owner_cell_id"],
                "certified_configuration_roles": row[
                    "certified_configuration_roles"
                ],
                "certified_owner_pivots": row["certified_owner_pivots"],
                "minimum_projective_owner_pivot_abs_lower": float(
                    row["minimum_projective_owner_pivot_abs_lower"]
                ),
                "minimum_projective_unit_circle_abs_lower": float(
                    row["minimum_projective_unit_circle_abs_lower"]
                ),
                "parent_revision": PARENT_REVISION,
                "certificate_source": "5459_v51_left_external41_projective_subcover",
                "valid_for_5459_left_external41_rerun_cell": bool(
                    result["probe_passed"]
                ),
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
        for row in rerun_manifest
        if (WORK / f"{row['smoke_job_id']}.json").is_file()
    ]
    rerun_passed = [row for row in completed if row["probe_passed"]]
    rerun_failures: dict[str, int] = {}
    for row in completed:
        if row["probe_passed"]:
            continue
        category = f"{row['failure_type']}:{row['failure_message']}"
        rerun_failures[category] = rerun_failures.get(category, 0) + 1
    for row in old_passed:
        row["certificate_source"] = "5458_v49_unchanged_direct_pass"
        row["parent_revision"] = "D4-deformed-contour-regular-away-W3-v49"
    combined = old_passed + completed
    combined_ids = [row["projective_owner_cell_id"] for row in combined]
    combined_complete = (
        len(combined) == len(manifest_5458)
        and len(set(combined_ids)) == len(manifest_5458)
    )
    combined_passed = [row for row in combined if truth(row["probe_passed"])]
    all_pass = combined_complete and len(combined_passed) == len(manifest_5458)
    minimum_projective_margin = min(
        (
            float(row["minimum_projective_owner_pivot_abs_lower"])
            for row in combined
        ),
        default=math.nan,
    )
    minimum_amplitude_denominator = min(
        (
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in combined_passed
        ),
        default=math.nan,
    )
    integrated_upper = sum(
        float(row["integrated_regular_path_abs_upper"])
        for row in combined_passed
    )
    reconstructed_area = sum(
        float(row["reconstructed_physical_path_area_abs_upper"])
        for row in combined_passed
    )
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "TOP_PARENT_AMPLITUDE_COVER_CERTIFIED_BY_LEFT_EXTERNAL41_SUBCOVER__RESUME_OUTER_SMOKE"
            if all_pass
            else (
                "TOP_LEFT_EXTERNAL41_SUBCOVER_EXPOSES_NEXT_DENOMINATOR"
                if len(completed) == len(rerun_manifest) or rerun_failures
                else "TOP_LEFT_EXTERNAL41_SUBCOVER_RESUME_REQUIRED"
            )
        ),
        "old_5458_passed_cell_count": len(old_passed),
        "old_5458_failed_cell_count": len(old_failed),
        "old_5458_failure_counts": old_failure_counts,
        "rerun_manifest_cell_count": len(rerun_manifest),
        "rerun_completed_cell_count": len(completed),
        "rerun_remaining_cell_count": len(rerun_manifest) - len(completed),
        "rerun_passed_cell_count": len(rerun_passed),
        "rerun_failed_cell_count": len(completed) - len(rerun_passed),
        "rerun_failure_counts": rerun_failures,
        "processed_this_run": processed,
        "combined_cell_count": len(combined),
        "combined_passed_cell_count": len(combined_passed),
        "minimum_projective_owner_pivot_abs_lower": minimum_projective_margin,
        "minimum_amplitude_denominator_abs_lower": minimum_amplitude_denominator,
        "integrated_regular_path_abs_upper": integrated_upper,
        "reconstructed_physical_path_area_abs_upper": reconstructed_area,
        "runtime_seconds": time.perf_counter() - started,
        "next_target": (
            "RESUME_CHECKPOINT_5456_REMAINING_OUTER_REPRESENTATIVES"
            if all_pass
            else "DERIVE_FIRST_REMAINING_LEFT_EXTERNAL41_FAILURE"
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
        check(
            "parent_revision_v51_loaded",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        check(
            "checkpoint_5457_projective_cover_valid",
            result_5457.get("valid_for_target_TOP_finite_projective_pivot_cover")
            is True,
            result_5457.get("decision"),
        ),
        check(
            "checkpoint_5458_preserved_exactly_133_single_category_failures",
            len(old_failed) == EXPECTED_5458_FAILURE_COUNT
            and old_failure_counts == {EXPECTED_FAILURE: EXPECTED_5458_FAILURE_COUNT},
            old_failure_counts,
        ),
        check(
            "rerun_manifest_matches_all_5458_failures",
            len(rerun_manifest) == EXPECTED_5458_FAILURE_COUNT
            and {
                row["projective_owner_cell_id"] for row in rerun_manifest
            }
            == {row["projective_owner_cell_id"] for row in old_failed},
            len(rerun_manifest),
        ),
        check(
            "checkpoint_5458_manifest_is_closed_16_by_32_partition",
            finite_partition_is_closed(manifest_5458),
            len(manifest_5458),
        ),
        check(
            "all_exact_projective_identity_rows_valid",
            all(row["valid_for_claim"] for row in derivation_rows()),
            len(derivation_rows()),
        ),
        check(
            "completed_rerun_cells_pass_or_preserve_failure",
            len(completed)
            == len(rerun_passed) + sum(rerun_failures.values()),
            f"completed={len(completed)};passed={len(rerun_passed)};failed={sum(rerun_failures.values())}",
        ),
        check(
            "all_combined_passing_cells_have_positive_finite_denominators",
            all(
                math.isfinite(float(row["minimum_amplitude_denominator_abs_lower"]))
                and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                for row in combined_passed
            ),
            minimum_amplitude_denominator,
        ),
        check(
            "all_combined_cells_retain_positive_projective_margin",
            all(
                float(row["minimum_projective_owner_pivot_abs_lower"]) > 0.0
                for row in combined
            ),
            minimum_projective_margin,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_outer_parent_leaf_transplant_smoke"]
            and not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "single TOP target only",
        ),
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
        atomic_csv(RERUN_RESULTS, completed)
    if combined:
        atomic_csv(COMBINED_RESULTS, combined)
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
