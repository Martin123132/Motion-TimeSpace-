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
OUTPUT = FUNCTIONAL_RG / "5460"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5459 = SCRIPTS / "Y5_R2FR_5459_D4_TOP_left_external41_projective_edge_transplant.py"
SCRIPT_5461 = SCRIPTS / "Y5_R2FR_5461_D4_TOP_minimum_gap_finite_projective_amplitude_cover.py"
SCRIPT_5462 = SCRIPTS / "Y5_R2FR_5462_D4_generalized_TOP_finite_projective_amplitude_runner.py"
SCRIPT_5463 = SCRIPTS / "Y5_R2FR_5463_D4_generalized_connector_finite_projective_amplitude_runner.py"
SCRIPT_5464 = SCRIPTS / "Y5_R2FR_5464_D4_minimal_depth_TOP_finite_projective_amplitude_runner.py"
SCRIPT_5465 = SCRIPTS / "Y5_R2FR_5465_D4_minimal_depth_connector_finite_projective_amplitude_runner.py"
SCRIPT_5466 = SCRIPTS / "Y5_R2FR_5466_D4_locally_refined_connector_finite_projective_amplitude_runner.py"
DOCUMENT_5456 = POST / "5456-Y5-R2FR-D4-outer-parent-leaf-transplant-smoke.md"
DOCUMENT_5459 = POST / "5459-Y5-R2FR-D4-TOP-left-external41-projective-edge-transplant.md"
DOCUMENT_5461 = POST / "5461-Y5-R2FR-D4-TOP-minimum-gap-finite-projective-amplitude-cover.md"
DOCUMENT_5462 = POST / "5462-Y5-R2FR-D4-generalized-TOP-finite-projective-amplitude-runner.md"
DOCUMENT_5463 = POST / "5463-Y5-R2FR-D4-generalized-connector-finite-projective-amplitude-runner.md"
DOCUMENT_5464 = POST / "5464-Y5-R2FR-D4-minimal-depth-TOP-finite-projective-amplitude-runner.md"
DOCUMENT_5465 = POST / "5465-Y5-R2FR-D4-minimal-depth-connector-finite-projective-amplitude-runner.md"
DOCUMENT_5466 = POST / "5466-Y5-R2FR-D4-locally-refined-connector-finite-projective-amplitude-runner.md"
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
RESULT_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_transplant_smoke_result.json"
)
RESULT_5459 = (
    FUNCTIONAL_RG / "5459" / "D4_TOP_left_external41_projective_edge_result.json"
)
COMBINED_5459 = (
    FUNCTIONAL_RG / "5459" / "D4_TOP_parent_amplitude_combined_certificate.csv"
)
VALIDATION_5459 = FUNCTIONAL_RG / "5459" / "P8_Y5_BRR545_5459_VALIDATION.csv"
RESULT_5461 = (
    FUNCTIONAL_RG / "5461" / "D4_TOP_minimum_gap_finite_cover_result.json"
)
CERTIFICATE_5461 = (
    FUNCTIONAL_RG / "5461" / "D4_TOP_minimum_gap_representative_certificate.csv"
)
VALIDATION_5461 = FUNCTIONAL_RG / "5461" / "P8_Y5_BRR545_5461_VALIDATION.csv"
STATUS_5462 = FUNCTIONAL_RG / "5462" / "D4_TOP_generalized_target_status.csv"
RESULT_5462 = FUNCTIONAL_RG / "5462" / "D4_TOP_generalized_runner_result.json"
VALIDATION_5462 = FUNCTIONAL_RG / "5462" / "P8_Y5_BRR545_5462_VALIDATION.csv"
STATUS_5463 = FUNCTIONAL_RG / "5463" / "D4_connector_finite_fallback_status.csv"
RESULT_5463 = FUNCTIONAL_RG / "5463" / "D4_connector_finite_fallback_result.json"
VALIDATION_5463 = FUNCTIONAL_RG / "5463" / "P8_Y5_BRR545_5463_VALIDATION.csv"
STATUS_5464 = FUNCTIONAL_RG / "5464" / "D4_minimal_depth_TOP_target_status.csv"
RESULT_5464 = FUNCTIONAL_RG / "5464" / "D4_minimal_depth_TOP_runner_result.json"
VALIDATION_5464 = FUNCTIONAL_RG / "5464" / "P8_Y5_BRR545_5464_VALIDATION.csv"
STATUS_5465 = FUNCTIONAL_RG / "5465" / "D4_minimal_depth_connector_target_status.csv"
RESULT_5465 = FUNCTIONAL_RG / "5465" / "D4_minimal_depth_connector_runner_result.json"
VALIDATION_5465 = FUNCTIONAL_RG / "5465" / "P8_Y5_BRR545_5465_VALIDATION.csv"
STATUS_5466 = FUNCTIONAL_RG / "5466" / "D4_local_refined_connector_target_status.csv"
RESULT_5466 = FUNCTIONAL_RG / "5466" / "D4_local_refined_connector_runner_result.json"
VALIDATION_5466 = FUNCTIONAL_RG / "5466" / "P8_Y5_BRR545_5466_VALIDATION.csv"
OLD_WORK_5456 = FUNCTIONAL_RG / "5456" / "work-v1"

DOCUMENT = POST / "5460-Y5-R2FR-D4-outer-representative-reconciliation-and-resume.md"
MANIFEST = OUTPUT / "D4_outer_representative_resume_manifest.csv"
RESOLVED_SEED = OUTPUT / "D4_outer_representative_resolved_seed.csv"
COMBINED_RESULTS = OUTPUT / "D4_outer_representative_combined_results.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5460_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_outer_representative_resume_result.json"

CHECKPOINT = 5460
REVISION = "D4-outer-representative-reconciliation-and-resume-v8"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
TARGET_TOP_JOB_ID = "E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA"
TARGET_TOP_MINIMUM_JOB_ID = "E01__U017__TOP__MINIMUM_CERTIFIED_OUTER_GAP"
EXPECTED_REPRESENTATIVE_COUNT = 77
EXPECTED_DIRECT_SEED_COUNT = 4
EXPECTED_PRE_5462_SEED_COUNT = 6
DIRECT_SEED_JOB_IDS = {
    "E01__U017__LEFT_CONNECTOR__MAXIMUM_PHYSICAL_PATH_AREA",
    "E01__U017__LEFT_CONNECTOR__MINIMUM_CERTIFIED_OUTER_GAP",
    "E01__U017__RIGHT_CONNECTOR__MAXIMUM_PHYSICAL_PATH_AREA",
    "E01__U017__RIGHT_CONNECTOR__MINIMUM_CERTIFIED_OUTER_GAP",
}


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


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


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


def direct_seed_paths() -> list[Path]:
    return [OLD_WORK_5456 / f"{job_id}.json" for job_id in DIRECT_SEED_JOB_IDS]


def generic_5462_certificate_paths() -> list[Path]:
    if not STATUS_5462.is_file():
        return []
    return [
        Path(row["certificate_path"])
        for row in read_csv(STATUS_5462)
        if row["route"] == "checkpoint_5462_generic"
        and row["status"] == "CERTIFIED"
        and truth(row["valid_for_target_outer_representative"])
    ]


def finite_5463_certificate_paths() -> list[Path]:
    if not STATUS_5463.is_file():
        return []
    return [
        Path(row["certificate_path"])
        for row in read_csv(STATUS_5463)
        if row["route"] == "checkpoint_5463_finite"
        and row["status"] == "CERTIFIED_FINITE_5463"
        and truth(row["valid_for_target_outer_representative"])
    ]


def minimal_depth_5464_certificate_paths() -> list[Path]:
    if not STATUS_5464.is_file():
        return []
    return [
        Path(row["certificate_path"])
        for row in read_csv(STATUS_5464)
        if row["route"] == "checkpoint_5464_minimal_depth"
        and row["status"] == "CERTIFIED_MINIMAL_DEPTH_5464"
        and truth(row["valid_for_target_outer_representative"])
    ]


def minimal_depth_5465_certificate_paths() -> list[Path]:
    if not STATUS_5465.is_file():
        return []
    return [
        Path(row["certificate_path"])
        for row in read_csv(STATUS_5465)
        if row["route"] == "checkpoint_5465_minimal_depth"
        and row["status"] == "CERTIFIED_MINIMAL_DEPTH_5465"
        and truth(row["valid_for_target_outer_representative"])
    ]


def local_refined_5466_certificate_paths() -> list[Path]:
    if not STATUS_5466.is_file():
        return []
    return [
        Path(row["certificate_path"])
        for row in read_csv(STATUS_5466)
        if row["route"] == "checkpoint_5466_local_refinement"
        and row["status"] == "CERTIFIED_LOCAL_REFINEMENT_5466"
        and truth(row["valid_for_target_outer_representative"])
    ]


def source_paths() -> list[Path]:
    return [
        SCRIPT_5396,
        SCRIPT_5456,
        SCRIPT_5459,
        SCRIPT_5461,
        SCRIPT_5462,
        SCRIPT_5463,
        SCRIPT_5464,
        SCRIPT_5465,
        SCRIPT_5466,
        DOCUMENT_5456,
        DOCUMENT_5459,
        DOCUMENT_5461,
        DOCUMENT_5462,
        DOCUMENT_5463,
        DOCUMENT_5464,
        DOCUMENT_5465,
        DOCUMENT_5466,
        REPRESENTATIVES_5456,
        RESULT_5456,
        RESULT_5459,
        COMBINED_5459,
        VALIDATION_5459,
        RESULT_5461,
        CERTIFICATE_5461,
        VALIDATION_5461,
        STATUS_5462,
        RESULT_5462,
        VALIDATION_5462,
        STATUS_5463,
        RESULT_5463,
        VALIDATION_5463,
        STATUS_5464,
        RESULT_5464,
        VALIDATION_5464,
        STATUS_5465,
        RESULT_5465,
        VALIDATION_5465,
        STATUS_5466,
        RESULT_5466,
        VALIDATION_5466,
        *generic_5462_certificate_paths(),
        *finite_5463_certificate_paths(),
        *minimal_depth_5464_certificate_paths(),
        *minimal_depth_5465_certificate_paths(),
        *local_refined_5466_certificate_paths(),
        *direct_seed_paths(),
    ]


def top_certificate_row(
    representative: dict[str, str],
    result_5459: dict[str, Any],
    combined_5459: list[dict[str, str]],
) -> dict[str, Any]:
    reconstructed_area = float(
        result_5459["reconstructed_physical_path_area_abs_upper"]
    )
    geometry_area = float(representative["physical_path_area_abs_upper"])
    return {
        "smoke_job_id": TARGET_TOP_JOB_ID,
        "selection_role": representative["selection_role"],
        "event_id": representative["event_id"],
        "mapped_cell_id": representative["mapped_cell_id"],
        "term_id": representative["term_id"],
        "branch_owner_id": representative["branch_owner_id"],
        "epsilon_bin_index": int(representative["epsilon_bin_index"]),
        "epsilon_subdivision_index": int(
            representative["epsilon_subdivision_index"]
        ),
        "epsilon_subdivision_count": int(
            representative["epsilon_subdivision_count"]
        ),
        "path_segment": representative["path_segment"],
        "x_lower": float(representative["x_lower"]),
        "x_upper": float(representative["x_upper"]),
        "t_lower": float(representative["t_lower"]),
        "t_upper": float(representative["t_upper"]),
        "geometry_gap_abs_lower": float(representative["gap_abs_lower"]),
        "geometry_physical_path_area_abs_upper": geometry_area,
        "probe_passed": True,
        "failure_type": "",
        "failure_message": "",
        "integrated_regular_path_abs_upper": float(
            result_5459["integrated_regular_path_abs_upper"]
        ),
        "minimum_amplitude_denominator_abs_lower": float(
            result_5459["minimum_amplitude_denominator_abs_lower"]
        ),
        "relative_root_abs_lower": min(
            float(row["relative_root_abs_lower"]) for row in combined_5459
        ),
        "selected_global_root_abs_lower": min(
            float(row["selected_global_root_abs_lower"])
            for row in combined_5459
        ),
        "collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"])
            for row in combined_5459
        ),
        "active_material_branch_count": max(
            int(float(row["active_material_branch_count"]))
            for row in combined_5459
        ),
        "active_material_branch_ids": "|".join(
            sorted(
                {
                    branch_id
                    for row in combined_5459
                    for branch_id in row["active_material_branch_ids"].split("|")
                    if branch_id
                }
            )
        ),
        "path_integral_enclosure_method": "FINITE_16X32_POINTWISE_SUPREMUM_SUM",
        "reconstructed_physical_path_area_abs_upper": reconstructed_area,
        "physical_path_area_absolute_error": abs(
            reconstructed_area - geometry_area
        ),
        "physical_path_area_excess": max(
            0.0, reconstructed_area - geometry_area
        ),
        "adaptive_subleaf_count": len(combined_5459),
        "refinement_witness_count": 133,
        "maximum_refinement_depth": 9,
        "unresolved_subleaf_count": 0,
        "runtime_seconds": float(result_5459["runtime_seconds"]),
        "event_principal_pole_owned_separately": True,
        "certificate_source": "checkpoint_5459_finite_TOP_replacement",
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
        "# 5460: D4 outer-representative reconciliation and resume",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Reconciliation",
        "",
        "The four committed checkpoint-5456 connector certificates are preserved. Checkpoints 5459 and 5461 replace both E01/U017 TOP extremes, checkpoint 5462 contributes every independently completed generalized TOP certificate, checkpoint 5463 contributes depth-nine connector certificates, checkpoint 5464 contributes minimal parent-admissible depth-eight TOP certificates, checkpoint 5465 contributes independently complete depth-eight connector certificates, and checkpoint 5466 contributes exact mixed-depth connector certificates that refine only demonstrated coarse interval obstructions. Every finite result recomputes or source-hash-locks its complete parent-domain cover; this is finite additivity, not a new fit or closure.",
        "",
        f"Resolved representatives: `{payload['resolved_representative_count']}/{payload['representative_count']}`. Passed: `{payload['passed_representative_count']}`. Failed: `{payload['failed_representative_count']}`. Remaining: `{payload['remaining_representative_count']}`.",
        "",
        "## Claim boundary",
        "",
        "Completion of all 77 extreme representatives certifies only the outer-representative smoke. It does not by itself certify all 606,990 outer leaves, the full event-cell cover, event-local W3, the regulator limit, local GR or full MTS.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(
    max_jobs: int,
    status_only: bool = False,
    requested_job_ids: list[str] | None = None,
) -> dict[str, Any]:
    set_below_normal_priority()
    started = time.perf_counter()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    representatives = read_csv(REPRESENTATIVES_5456)
    representative_by_id = {row["smoke_job_id"]: row for row in representatives}
    result_5459 = read_json(RESULT_5459)
    combined_5459 = read_csv(COMBINED_5459)
    validation_5459 = read_csv(VALIDATION_5459)
    result_5461 = read_json(RESULT_5461)
    certificate_5461 = read_csv(CERTIFICATE_5461)
    validation_5461 = read_csv(VALIDATION_5461)
    status_5462 = read_csv(STATUS_5462)
    result_5462 = read_json(RESULT_5462)
    validation_5462 = read_csv(VALIDATION_5462)
    certificate_paths_5462 = generic_5462_certificate_paths()
    certificates_5462: list[dict[str, str]] = []
    for path in certificate_paths_5462:
        rows = read_csv(path)
        if len(rows) != 1:
            raise RuntimeError(
                f"expected one checkpoint-5462 certificate in {path}, found {len(rows)}"
            )
        certificates_5462.append(rows[0])
    status_5463 = read_csv(STATUS_5463)
    result_5463 = read_json(RESULT_5463)
    validation_5463 = read_csv(VALIDATION_5463)
    certificate_paths_5463 = finite_5463_certificate_paths()
    certificates_5463: list[dict[str, str]] = []
    for path in certificate_paths_5463:
        rows = read_csv(path)
        if len(rows) != 1:
            raise RuntimeError(
                f"expected one checkpoint-5463 certificate in {path}, found {len(rows)}"
            )
        certificates_5463.append(rows[0])
    status_5464 = read_csv(STATUS_5464)
    result_5464 = read_json(RESULT_5464)
    validation_5464 = read_csv(VALIDATION_5464)
    certificate_paths_5464 = minimal_depth_5464_certificate_paths()
    certificates_5464: list[dict[str, str]] = []
    for path in certificate_paths_5464:
        rows = read_csv(path)
        if len(rows) != 1:
            raise RuntimeError(
                f"expected one checkpoint-5464 certificate in {path}, found {len(rows)}"
            )
        certificates_5464.append(rows[0])
    status_5465 = read_csv(STATUS_5465)
    result_5465 = read_json(RESULT_5465)
    validation_5465 = read_csv(VALIDATION_5465)
    certificate_paths_5465 = minimal_depth_5465_certificate_paths()
    certificates_5465: list[dict[str, str]] = []
    for path in certificate_paths_5465:
        rows = read_csv(path)
        if len(rows) != 1:
            raise RuntimeError(
                f"expected one checkpoint-5465 certificate in {path}, found {len(rows)}"
            )
        certificates_5465.append(rows[0])
    status_5466 = read_csv(STATUS_5466)
    result_5466 = read_json(RESULT_5466)
    validation_5466 = read_csv(VALIDATION_5466)
    certificate_paths_5466 = local_refined_5466_certificate_paths()
    certificates_5466: list[dict[str, str]] = []
    for path in certificate_paths_5466:
        rows = read_csv(path)
        if len(rows) != 1:
            raise RuntimeError(
                f"expected one checkpoint-5466 certificate in {path}, found {len(rows)}"
            )
        certificates_5466.append(rows[0])
    if len(certificate_5461) != 1:
        raise RuntimeError(
            f"expected one checkpoint-5461 certificate, found {len(certificate_5461)}"
        )
    direct_seed = [read_json(path) for path in direct_seed_paths()]
    for row in direct_seed:
        row["certificate_source"] = "checkpoint_5456_committed_direct_seed"
        row["parent_revision"] = "D4-deformed-contour-regular-away-W3-v49"
    target_top = top_certificate_row(
        representative_by_id[TARGET_TOP_JOB_ID],
        result_5459,
        combined_5459,
    )
    raw_seed = direct_seed + [
        target_top,
        certificate_5461[0],
        *certificates_5462,
        *certificates_5463,
        *certificates_5464,
        *certificates_5465,
        *certificates_5466,
    ]
    preferred_seed_by_id: dict[str, dict[str, Any]] = {}
    seed_occurrence_count: dict[str, int] = {}
    for row in raw_seed:
        job_id = row["smoke_job_id"]
        seed_occurrence_count[job_id] = seed_occurrence_count.get(job_id, 0) + 1
        preferred_seed_by_id[job_id] = row
    seed = [
        preferred_seed_by_id[row["smoke_job_id"]]
        for row in representatives
        if row["smoke_job_id"] in preferred_seed_by_id
    ]
    superseded_seed_certificate_ids = sorted(
        job_id for job_id, count in seed_occurrence_count.items() if count > 1
    )
    seed_ids = {row["smoke_job_id"] for row in seed}
    remaining_manifest = [
        dict(row) for row in representatives if row["smoke_job_id"] not in seed_ids
    ]
    for row in remaining_manifest:
        row["selection_role_5460"] = "UNRESOLVED_AFTER_5459_5461_5462_5463_5464_5465_5466_RECONCILIATION"
        row["parent_revision"] = PARENT_REVISION
    atomic_csv(MANIFEST, remaining_manifest)
    atomic_csv(RESOLVED_SEED, seed)
    stable = load_module("mts_5456_for_5460", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5460", stable.SCRIPT_5449)
    parent = stable.load_module("mts_5396_for_5460", module_5449.PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
        )
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    cells = {
        row["mapped_cell_id"]: row
        for row in parent.read_csv(parent.MAPPED_5393)
    }
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    requested = list(requested_job_ids or [])
    if requested:
        unknown = sorted(set(requested) - {row["smoke_job_id"] for row in remaining_manifest})
        if unknown:
            raise ValueError(f"requested jobs are not unresolved representatives: {unknown}")
        schedule_by_id = {row["smoke_job_id"]: row for row in remaining_manifest}
        schedule = [schedule_by_id[job_id] for job_id in requested]
    else:
        schedule = remaining_manifest
    WORK.mkdir(parents=True, exist_ok=True)
    processed = 0
    for row in schedule:
        path = WORK / f"{row['smoke_job_id']}.json"
        if path.is_file():
            continue
        if status_only:
            break
        if max_jobs > 0 and processed >= max_jobs:
            break
        result = stable.adaptive_evaluate_representative(
            parent,
            cells,
            support_segments,
            branches,
            row,
        )
        result.update(
            {
                "certificate_source": "checkpoint_5460_parent_v51_adaptive_resume",
                "parent_revision": PARENT_REVISION,
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
                "last_job_id": row["smoke_job_id"],
            },
        )
        if not result["probe_passed"]:
            break
    resumed = [
        read_json(WORK / f"{row['smoke_job_id']}.json")
        for row in remaining_manifest
        if (WORK / f"{row['smoke_job_id']}.json").is_file()
    ]
    combined = seed + resumed
    passed = [row for row in combined if truth(row["probe_passed"])]
    failed = [row for row in combined if not truth(row["probe_passed"])]
    combined_ids = [row["smoke_job_id"] for row in combined]
    remaining_ids = [
        row["smoke_job_id"]
        for row in remaining_manifest
        if row["smoke_job_id"] not in set(combined_ids)
    ]
    complete = (
        len(combined) == len(representatives)
        and len(set(combined_ids)) == len(representatives)
    )
    all_pass = complete and not failed
    first_failure = failed[0] if failed else None
    next_target = (
        "OUTER_REPRESENTATIVE_SMOKE_COMPLETE__BUILD_ALL_LEAF_TRANSPLANT"
        if all_pass
        else (
            first_failure["smoke_job_id"]
            if first_failure is not None
            else (remaining_ids[0] if remaining_ids else "RECONCILIATION_AUDIT")
        )
    )
    minimum_denominator = min(
        (
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in passed
        ),
        default=math.nan,
    )
    maximum_integrated_upper = max(
        (
            float(row["integrated_regular_path_abs_upper"])
            for row in passed
        ),
        default=math.nan,
    )
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "OUTER_REPRESENTATIVE_SMOKE_CERTIFIED__BUILD_ALL_LEAF_TRANSPLANT"
            if all_pass
            else (
                "OUTER_REPRESENTATIVE_RESUME_STOPPED_AT_FIRST_FAILURE"
                if first_failure is not None
                else "OUTER_REPRESENTATIVE_RESUME_PARTIAL"
            )
        ),
        "representative_count": len(representatives),
        "seed_representative_count": len(seed),
        "raw_seed_certificate_count": len(raw_seed),
        "superseded_seed_certificate_count": len(raw_seed) - len(seed),
        "superseded_seed_certificate_ids": superseded_seed_certificate_ids,
        "checkpoint_5462_seed_representative_count": len(certificates_5462),
        "checkpoint_5463_seed_representative_count": len(certificates_5463),
        "checkpoint_5464_seed_representative_count": len(certificates_5464),
        "checkpoint_5465_seed_representative_count": len(certificates_5465),
        "checkpoint_5466_seed_representative_count": len(certificates_5466),
        "resume_manifest_count": len(remaining_manifest),
        "resolved_representative_count": len(combined),
        "passed_representative_count": len(passed),
        "failed_representative_count": len(failed),
        "remaining_representative_count": len(representatives) - len(combined),
        "processed_this_run": processed,
        "requested_job_count": len(requested),
        "minimum_amplitude_denominator_abs_lower": minimum_denominator,
        "maximum_integrated_regular_path_abs_upper": maximum_integrated_upper,
        "first_failure_job_id": (
            first_failure["smoke_job_id"] if first_failure is not None else ""
        ),
        "first_failure_type": (
            first_failure["failure_type"] if first_failure is not None else ""
        ),
        "first_failure_message": (
            first_failure["failure_message"] if first_failure is not None else ""
        ),
        "runtime_seconds": time.perf_counter() - started,
        "next_target": next_target,
        "valid_for_outer_parent_leaf_transplant_smoke": all_pass,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("parent_revision_v51_loaded", parent.REVISION == PARENT_REVISION, parent.REVISION),
        check(
            "representative_manifest_has_77_unique_jobs",
            len(representatives) == EXPECTED_REPRESENTATIVE_COUNT
            and len(representative_by_id) == EXPECTED_REPRESENTATIVE_COUNT,
            len(representatives),
        ),
        check(
            "four_checkpoint_5456_direct_seeds_pass",
            len(direct_seed) == EXPECTED_DIRECT_SEED_COUNT
            and {row["smoke_job_id"] for row in direct_seed} == DIRECT_SEED_JOB_IDS
            and all(row["probe_passed"] for row in direct_seed),
            len(direct_seed),
        ),
        check(
            "checkpoint_5459_TOP_certificate_is_complete",
            result_5459.get("valid_for_target_TOP_parent_amplitude_cover") is True
            and len(combined_5459) == 512
            and all(truth(row["probe_passed"]) for row in combined_5459)
            and all(truth(row["passed"]) for row in validation_5459),
            result_5459.get("decision"),
        ),
        check(
            "checkpoint_5461_TOP_certificate_is_complete",
            result_5461.get("valid_for_target_outer_representative") is True
            and certificate_5461[0].get("smoke_job_id")
            == TARGET_TOP_MINIMUM_JOB_ID
            and truth(certificate_5461[0].get("probe_passed"))
            and all(truth(row["passed"]) for row in validation_5461),
            result_5461.get("decision"),
        ),
        check(
            "checkpoint_5462_generic_certificates_are_complete",
            len(status_5462) == 25
            and result_5462.get("certified_target_count")
            == len(certificates_5462) + 2
            and all(truth(row["passed"]) for row in validation_5462)
            and all(truth(row["probe_passed"]) for row in certificates_5462)
            and {
                row["smoke_job_id"] for row in certificates_5462
            }
            == {
                row["target_job_id"]
                for row in status_5462
                if row["route"] == "checkpoint_5462_generic"
                and row["status"] == "CERTIFIED"
            },
            len(certificates_5462),
        ),
        check(
            "checkpoint_5463_finite_certificates_are_complete",
            len(status_5463) == 52
            and result_5463.get("finite_certified_target_count")
            == len(certificates_5463)
            and all(truth(row["passed"]) for row in validation_5463)
            and all(truth(row["probe_passed"]) for row in certificates_5463)
            and {
                row["smoke_job_id"] for row in certificates_5463
            }
            == {
                row["target_job_id"]
                for row in status_5463
                if row["route"] == "checkpoint_5463_finite"
                and row["status"] == "CERTIFIED_FINITE_5463"
            },
            len(certificates_5463),
        ),
        check(
            "checkpoint_5464_minimal_depth_certificates_are_complete",
            len(status_5464) == 25
            and result_5464.get("minimal_depth_certified_target_count")
            == len(certificates_5464)
            and result_5464.get("certified_binary_partition_depth") == 8
            and all(truth(row["passed"]) for row in validation_5464)
            and all(truth(row["probe_passed"]) for row in certificates_5464)
            and {
                row["smoke_job_id"] for row in certificates_5464
            }
            == {
                row["target_job_id"]
                for row in status_5464
                if row["route"] == "checkpoint_5464_minimal_depth"
                and row["status"] == "CERTIFIED_MINIMAL_DEPTH_5464"
            },
            len(certificates_5464),
        ),
        check(
            "checkpoint_5465_minimal_depth_certificates_are_complete",
            len(status_5465) == 52
            and result_5465.get("minimal_depth_certified_target_count")
            == len(certificates_5465)
            and result_5465.get("certified_binary_partition_depth") == 8
            and all(truth(row["passed"]) for row in validation_5465)
            and all(truth(row["probe_passed"]) for row in certificates_5465)
            and {
                row["smoke_job_id"] for row in certificates_5465
            }
            == {
                row["target_job_id"]
                for row in status_5465
                if row["route"] == "checkpoint_5465_minimal_depth"
                and row["status"] == "CERTIFIED_MINIMAL_DEPTH_5465"
            },
            len(certificates_5465),
        ),
        check(
            "checkpoint_5466_local_refinement_certificates_are_complete",
            len(status_5466) == 52
            and result_5466.get("locally_refined_certified_target_count")
            == len(certificates_5466)
            and all(truth(row["passed"]) for row in validation_5466)
            and all(truth(row["probe_passed"]) for row in certificates_5466)
            and {
                row["smoke_job_id"] for row in certificates_5466
            }
            == {
                row["target_job_id"]
                for row in status_5466
                if row["route"] == "checkpoint_5466_local_refinement"
                and row["status"] == "CERTIFIED_LOCAL_REFINEMENT_5466"
            },
            len(certificates_5466),
        ),
        check(
            "all_seed_representatives_are_unique_and_passing",
            len(raw_seed)
            == EXPECTED_PRE_5462_SEED_COUNT
            + len(certificates_5462)
            + len(certificates_5463)
            + len(certificates_5464)
            + len(certificates_5465)
            + len(certificates_5466)
            and len(seed_ids) == len(seed)
            and seed_ids == set(preferred_seed_by_id)
            and all(truth(row["probe_passed"]) for row in seed),
            sorted(seed_ids),
        ),
        check(
            "overlapping_certificates_are_deduplicated_by_job_id",
            len(raw_seed) - len(seed)
            == sum(count - 1 for count in seed_occurrence_count.values())
            and all(
                preferred_seed_by_id[job_id]["certificate_source"]
                == next(
                    row["certificate_source"]
                    for row in reversed(raw_seed)
                    if row["smoke_job_id"] == job_id
                )
                for job_id in superseded_seed_certificate_ids
            ),
            superseded_seed_certificate_ids,
        ),
        check(
            "remaining_manifest_matches_dynamic_seed_count",
            len(remaining_manifest) == EXPECTED_REPRESENTATIVE_COUNT - len(seed)
            and len({row["smoke_job_id"] for row in remaining_manifest})
            == EXPECTED_REPRESENTATIVE_COUNT - len(seed),
            len(remaining_manifest),
        ),
        check(
            "combined_results_have_no_duplicate_jobs",
            len(combined_ids) == len(set(combined_ids)),
            len(combined_ids),
        ),
        check(
            "all_passing_results_have_positive_finite_denominators",
            all(
                math.isfinite(float(row["minimum_amplitude_denominator_abs_lower"]))
                and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                for row in passed
            ),
            minimum_denominator,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_full_event_cell_finite_cover"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "representative smoke only",
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
    parser.add_argument("--job-id", action="append", default=[])
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    payload = run(arguments.max_jobs, arguments.status_only, arguments.job_id)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
