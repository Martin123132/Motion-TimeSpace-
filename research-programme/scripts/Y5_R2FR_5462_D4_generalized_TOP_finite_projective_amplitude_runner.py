from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
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
OUTPUT = FUNCTIONAL_RG / "5462"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5461 = (
    SCRIPTS
    / "Y5_R2FR_5461_D4_TOP_minimum_gap_finite_projective_amplitude_cover.py"
)
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
RESULT_5459 = (
    FUNCTIONAL_RG / "5459" / "D4_TOP_left_external41_projective_edge_result.json"
)
CERTIFICATE_5459 = (
    FUNCTIONAL_RG / "5459" / "D4_TOP_parent_amplitude_combined_certificate.csv"
)
RESULT_5461 = (
    FUNCTIONAL_RG / "5461" / "D4_TOP_minimum_gap_finite_cover_result.json"
)
CERTIFICATE_5461 = (
    FUNCTIONAL_RG / "5461" / "D4_TOP_minimum_gap_representative_certificate.csv"
)

DOCUMENT = POST / "5462-Y5-R2FR-D4-generalized-TOP-finite-projective-amplitude-runner.md"
TARGET_STATUS = OUTPUT / "D4_TOP_generalized_target_status.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5462_VALIDATION.csv"
RESULT = OUTPUT / "D4_TOP_generalized_runner_result.json"

CHECKPOINT = 5462
REVISION = "D4-generalized-TOP-finite-projective-amplitude-runner-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
PREDECESSOR_TARGETS = {
    "E01__U017__TOP__MAXIMUM_PHYSICAL_PATH_AREA": (
        "checkpoint_5459",
        RESULT_5459,
        CERTIFICATE_5459,
        "valid_for_target_TOP_parent_amplitude_cover",
    ),
    "E01__U017__TOP__MINIMUM_CERTIFIED_OUTER_GAP": (
        "checkpoint_5461",
        RESULT_5461,
        CERTIFICATE_5461,
        "valid_for_target_outer_representative",
    ),
}


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


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(
        path,
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n",
    )


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


def truth(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def target_key(target_job_id: str) -> str:
    event_id, mapped_cell_id, path_segment, role = target_job_id.split("__", 3)
    role_key = (
        "MAX_AREA"
        if role == "MAXIMUM_PHYSICAL_PATH_AREA"
        else "MIN_GAP"
    )
    return "_".join((event_id, mapped_cell_id, path_segment, role_key))


def top_targets() -> list[dict[str, str]]:
    targets = [
        row
        for row in read_csv(REPRESENTATIVES_5456)
        if row["path_segment"] == "TOP"
    ]
    if len(targets) != 25 or len({row["smoke_job_id"] for row in targets}) != 25:
        raise RuntimeError("expected exactly 25 unique TOP representatives")
    return targets


def generic_output(target_job_id: str) -> Path:
    return OUTPUT / target_key(target_job_id)


def status_for_target(target: dict[str, str]) -> dict[str, Any]:
    target_job_id = target["smoke_job_id"]
    if target_job_id in PREDECESSOR_TARGETS:
        route, result_path, certificate_path, validity_field = PREDECESSOR_TARGETS[
            target_job_id
        ]
    else:
        route = "checkpoint_5462_generic"
        target_output = generic_output(target_job_id)
        result_path = target_output / "result.json"
        certificate_path = target_output / "representative_certificate.csv"
        validity_field = "valid_for_target_outer_representative"
    result_payload = read_json(result_path) if result_path.is_file() else {}
    certified = (
        truth(result_payload.get(validity_field, False))
        and certificate_path.is_file()
    )
    first_failure = str(result_payload.get("first_failure_type", ""))
    cover_certified = truth(
        result_payload.get("valid_for_target_TOP_finite_projective_pivot_cover", False)
    )
    if certified:
        status = "CERTIFIED"
    elif first_failure:
        status = "FIRST_FAILURE_REQUIRES_DERIVATION"
    elif cover_certified:
        status = "PROJECTIVE_COVER_CERTIFIED_AMPLITUDE_PENDING"
    elif result_path.is_file():
        status = "PROJECTIVE_COVER_NOT_CLOSED"
    else:
        status = "UNRUN"
    return {
        "checkpoint": CHECKPOINT,
        "target_job_id": target_job_id,
        "target_key": target_key(target_job_id),
        "event_id": target["event_id"],
        "mapped_cell_id": target["mapped_cell_id"],
        "selection_role": target["selection_role"],
        "epsilon_bin_index": int(target["epsilon_bin_index"]),
        "epsilon_real_lower": float(target["epsilon_real_lower"]),
        "epsilon_real_upper": float(target["epsilon_real_upper"]),
        "x_width": float(target["x_width"]),
        "t_width": float(target["t_width"]),
        "route": route,
        "status": status,
        "completed_cell_count": int(result_payload.get("completed_cell_count", 0)),
        "remaining_cell_count": int(result_payload.get("remaining_cell_count", 0)),
        "minimum_owner_pivot_abs_lower": result_payload.get(
            "minimum_owner_pivot_abs_lower", ""
        ),
        "minimum_amplitude_denominator_abs_lower": result_payload.get(
            "minimum_amplitude_denominator_abs_lower", ""
        ),
        "first_failure_type": first_failure,
        "first_failure_cell_id": result_payload.get("first_failure_cell_id", ""),
        "result_path": str(result_path.resolve()),
        "certificate_path": str(certificate_path.resolve()),
        "valid_for_target_outer_representative": certified,
        "valid_for_full_outer_parent_leaf_enclosure": False,
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


def render_aggregate(payload: dict[str, Any]) -> None:
    lines = [
        "# 5462: Generalized D4 TOP finite projective amplitude runner",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Construction",
        "",
        "Checkpoint 5462 applies the exact massless determinant identity and the finite `16 x 32` projective-owner partition independently to each unresolved TOP extreme representative. Selector choices, pivot margins and all parent-v51 amplitude bounds are recomputed for each target; no numerical margin is transferred between epsilon bins or events.",
        "",
        f"Certified TOP representatives: `{payload['certified_target_count']}/{payload['target_count']}`. Projective-cover-only targets: `{payload['cover_only_target_count']}`. Unrun targets: `{payload['unrun_target_count']}`. First failures: `{payload['first_failure_target_count']}`.",
        "",
        "## Claim boundary",
        "",
        "This runner closes only the finite extreme-representative smoke rows that finish with sourced certificates. It does not by itself certify all outer leaves, the full event-cell cover, event-local W3, the regulator limit, local GR or full MTS.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def refresh_aggregate() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    targets = top_targets()
    rows = [status_for_target(target) for target in targets]
    certified = [row for row in rows if row["status"] == "CERTIFIED"]
    cover_only = [
        row
        for row in rows
        if row["status"] == "PROJECTIVE_COVER_CERTIFIED_AMPLITUDE_PENDING"
    ]
    failed = [
        row
        for row in rows
        if row["status"] == "FIRST_FAILURE_REQUIRES_DERIVATION"
    ]
    unrun = [row for row in rows if row["status"] == "UNRUN"]
    all_certified = len(certified) == len(rows)
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "ALL_TOP_EXTREME_REPRESENTATIVES_CERTIFIED__RECONCILE_5460"
            if all_certified
            else (
                "TOP_GENERALIZATION_FIRST_FAILURE__DERIVE"
                if failed
                else "TOP_GENERALIZATION_PARTIAL__RESUME"
            )
        ),
        "target_count": len(rows),
        "certified_target_count": len(certified),
        "cover_only_target_count": len(cover_only),
        "first_failure_target_count": len(failed),
        "unrun_target_count": len(unrun),
        "valid_for_all_TOP_extreme_representatives": all_certified,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    result_paths = [Path(row["result_path"]) for row in rows if Path(row["result_path"]).is_file()]
    validations = [
        check("all_static_sources_exist", all(path.is_file() for path in (Path(__file__), SCRIPT_5461, REPRESENTATIVES_5456, RESULT_5459, CERTIFICATE_5459)), 5),
        check("manifest_has_25_unique_TOP_targets", len(rows) == 25 and len({row["target_job_id"] for row in rows}) == 25, len(rows)),
        check("two_predecessor_routes_are_explicit", sum(row["route"].startswith("checkpoint_54") and row["route"] != "checkpoint_5462_generic" for row in rows) == 2, sorted(row["target_job_id"] for row in rows if row["route"] != "checkpoint_5462_generic")),
        check("every_materialized_result_preserves_broad_claim_boundary", all(not truth(read_json(path).get("valid_for_full_outer_parent_leaf_enclosure", False)) and not truth(read_json(path).get("valid_for_D4_event_local_W3_bound", False)) and not truth(read_json(path).get("valid_for_all_operator_local_GR_claim", False)) and not truth(read_json(path).get("valid_for_full_MTS_claim", False)) for path in result_paths), len(result_paths)),
        check("aggregate_broad_claims_remain_false", not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "TOP representatives only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    source_paths = [
        Path(__file__),
        SCRIPT_5461,
        REPRESENTATIVES_5456,
        RESULT_5459,
        CERTIFICATE_5459,
        RESULT_5461,
        CERTIFICATE_5461,
    ]
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths
    ]
    atomic_csv(TARGET_STATUS, rows)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(RESULT, payload)
    render_aggregate(payload)
    return payload, rows


def target_document_writer(base: Any, target_job_id: str) -> Any:
    def render(payload: dict[str, Any]) -> None:
        lines = [
            f"# 5462 target: {target_job_id}",
            "",
            "## Decision",
            "",
            f"**{payload['decision']}**",
            "",
            "The exact determinant theorem is reused, but this target's selector, projective pivot margins and parent-v51 amplitude cells are recomputed on its own epsilon/x/t domain.",
            "",
            f"Projective rows passed: `{payload['passed_projective_owner_row_count']}/{payload['projective_owner_row_count']}`. Amplitude cells completed: `{payload['completed_cell_count']}/{payload['manifest_cell_count']}`; failed: `{payload['failed_cell_count']}`.",
            "",
            "This is one extreme-representative certificate only; all broader MTS and local-GR claims remain false.",
            "",
        ]
        base.atomic_text(base.DOCUMENT, "\n".join(lines))

    return render


def configure_base(target_job_id: str) -> Any:
    base = load_module("mts_5461_for_5462", SCRIPT_5461)
    target_output = generic_output(target_job_id)
    base.CHECKPOINT = CHECKPOINT
    base.REVISION = REVISION
    base.TARGET_JOB_ID = target_job_id
    base.OUTPUT = target_output
    base.WORK = target_output / "work-v1"
    base.DOCUMENT = target_output / "README.md"
    base.COVER = target_output / "projective_pivot_cover.csv"
    base.OWNER_SUMMARY = target_output / "projective_owner_summary.csv"
    base.MANIFEST = target_output / "amplitude_manifest.csv"
    base.CELL_RESULTS = target_output / "amplitude_cells.csv"
    base.REPRESENTATIVE_CERTIFICATE = target_output / "representative_certificate.csv"
    base.SOURCE_REGISTER = target_output / "source_register.csv"
    base.VALIDATION = target_output / "validation.csv"
    base.STATUS = target_output / "status.json"
    base.RESULT = target_output / "result.json"
    original_source_paths = base.source_paths
    original_manifest = base.amplitude_manifest
    original_certificate = base.representative_certificate

    def source_paths() -> list[Path]:
        paths = [Path(__file__), SCRIPT_5461, *original_source_paths()]
        return list(dict.fromkeys(paths))

    def amplitude_manifest(
        target: dict[str, str], cover: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        rows = original_manifest(target, cover)
        for row in rows:
            row["smoke_job_id"] = row["smoke_job_id"].replace("5461__", "5462__", 1)
            row["valid_for_5462_amplitude_manifest"] = row.pop(
                "valid_for_5461_amplitude_manifest"
            )
        return rows

    def representative_certificate(
        target: dict[str, str],
        cells: list[dict[str, Any]],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        row = original_certificate(target, cells, payload)
        row["certificate_source"] = (
            "checkpoint_5462_generalized_finite_projective_amplitude_cover"
        )
        return row

    base.source_paths = source_paths
    base.amplitude_manifest = amplitude_manifest
    base.representative_certificate = representative_certificate
    base.render_document = target_document_writer(base, target_job_id)
    return base


def normalized_decision(payload: dict[str, Any]) -> tuple[str, str]:
    if truth(payload.get("valid_for_target_outer_representative", False)):
        return (
            "TOP_TARGET_FINITE_PROJECTIVE_AMPLITUDE_COVER_CERTIFIED__RECONCILE_5460",
            "REFRESH_5462_AGGREGATE_AND_RECONCILE_5460",
        )
    if payload.get("first_failure_type"):
        return (
            "TOP_TARGET_AMPLITUDE_FIRST_FAILURE__DERIVE",
            "DERIVE_FIRST_FAILED_AMPLITUDE_DENOMINATOR",
        )
    if truth(payload.get("valid_for_target_TOP_finite_projective_pivot_cover", False)):
        return (
            "TOP_TARGET_PROJECTIVE_COVER_CERTIFIED__AMPLITUDE_RESUME_REQUIRED",
            "RESUME_FINITE_AMPLITUDE_CELLS",
        )
    return "TOP_TARGET_PROJECTIVE_COVER_NOT_CLOSED", "DERIVE_PROJECTIVE_COVER"


def choose_next(rows: list[dict[str, Any]]) -> str:
    failures = [
        row for row in rows if row["status"] == "FIRST_FAILURE_REQUIRES_DERIVATION"
    ]
    if failures:
        raise RuntimeError(
            "derive the recorded first failure before scheduling another TOP target: "
            + failures[0]["target_job_id"]
        )
    candidates = [
        row
        for row in rows
        if row["route"] == "checkpoint_5462_generic"
        and row["status"] != "CERTIFIED"
    ]
    if not candidates:
        raise RuntimeError("no unresolved checkpoint-5462 TOP target remains")
    epsilon_priority = {-1: 0, 0: 1, 8: 2, 7: 3}
    candidates.sort(
        key=lambda row: (
            0
            if row["status"] == "PROJECTIVE_COVER_CERTIFIED_AMPLITUDE_PENDING"
            else 1,
            epsilon_priority.get(int(row["epsilon_bin_index"]), 9),
            row["target_job_id"],
        )
    )
    return str(candidates[0]["target_job_id"])


def run_target(
    target_job_id: str, max_jobs: int, cover_only: bool
) -> dict[str, Any]:
    valid_ids = {row["smoke_job_id"] for row in top_targets()}
    if target_job_id not in valid_ids:
        raise ValueError(f"unknown TOP representative: {target_job_id}")
    if target_job_id in PREDECESSOR_TARGETS:
        raise ValueError(f"target is owned by a predecessor checkpoint: {target_job_id}")
    before_formalization = {
        str(path.relative_to(FORMALIZATION)): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    } if FORMALIZATION.is_dir() else {}
    base = configure_base(target_job_id)
    payload = base.run(max_jobs, cover_only)
    decision, next_target = normalized_decision(payload)
    payload["checkpoint"] = CHECKPOINT
    payload["revision"] = REVISION
    payload["decision"] = decision
    payload["next_target"] = next_target
    payload["generic_target_key"] = target_key(target_job_id)
    after_formalization = {
        str(path.relative_to(FORMALIZATION)): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    } if FORMALIZATION.is_dir() else {}
    if before_formalization != after_formalization:
        raise RuntimeError("formalization-workbench changed during checkpoint 5462")
    base.atomic_json(base.RESULT, payload)
    base.atomic_json(base.STATUS, payload)
    base.render_document(payload)
    refresh_aggregate()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-job-id")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--cover-only", action="store_true")
    parser.add_argument("--refresh-only", action="store_true")
    parser.add_argument("--list-targets", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_jobs < 0:
        raise ValueError("--max-jobs must be nonnegative")
    aggregate, rows = refresh_aggregate()
    if arguments.list_targets:
        print(json.dumps(rows, indent=2, sort_keys=True, allow_nan=True))
        return 0
    if arguments.refresh_only:
        print(json.dumps(aggregate, indent=2, sort_keys=True, allow_nan=True))
        return 0 if aggregate["failed_validation_count"] == 0 else 1
    if arguments.target_job_id and arguments.next:
        raise ValueError("choose either --target-job-id or --next")
    target_job_id = arguments.target_job_id or choose_next(rows)
    payload = run_target(target_job_id, arguments.max_jobs, arguments.cover_only)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
