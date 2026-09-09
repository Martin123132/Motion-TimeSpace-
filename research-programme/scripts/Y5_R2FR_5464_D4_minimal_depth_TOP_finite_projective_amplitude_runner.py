from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
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
OUTPUT = FUNCTIONAL_RG / "5464"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5396 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
SCRIPT_5461 = (
    SCRIPTS
    / "Y5_R2FR_5461_D4_TOP_minimum_gap_finite_projective_amplitude_cover.py"
)
SCRIPT_5462 = (
    SCRIPTS
    / "Y5_R2FR_5462_D4_generalized_TOP_finite_projective_amplitude_runner.py"
)
REPRESENTATIVES_5456 = (
    FUNCTIONAL_RG / "5456" / "D4_outer_parent_leaf_representatives.csv"
)
STATUS_5462 = FUNCTIONAL_RG / "5462" / "D4_TOP_generalized_target_status.csv"

DOCUMENT = POST / "5464-Y5-R2FR-D4-minimal-depth-TOP-finite-projective-amplitude-runner.md"
TARGET_STATUS = OUTPUT / "D4_minimal_depth_TOP_target_status.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR545_5464_VALIDATION.csv"
RESULT = OUTPUT / "D4_minimal_depth_TOP_runner_result.json"

CHECKPOINT = 5464
REVISION = "D4-minimal-depth-TOP-finite-projective-amplitude-runner-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
X_SUBDIVISIONS = 8
T_SUBDIVISIONS = 32
X_BINARY_DEPTH = 3
T_BINARY_DEPTH = 5
CERTIFIED_BINARY_PARTITION_DEPTH = 8
PARENT_MINIMUM_SPECIAL_BRANCH_DEPTH = 8


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


def top_targets() -> list[dict[str, str]]:
    targets = [
        row
        for row in read_csv(REPRESENTATIVES_5456)
        if row["path_segment"] == "TOP"
    ]
    if len(targets) != 25 or len({row["smoke_job_id"] for row in targets}) != 25:
        raise RuntimeError("expected exactly 25 unique TOP representatives")
    return targets


def target_key(target_job_id: str) -> str:
    event_id, mapped_cell_id, path_segment, role = target_job_id.split("__", 3)
    role_key = (
        "MAX_AREA"
        if role == "MAXIMUM_PHYSICAL_PATH_AREA"
        else "MIN_GAP"
    )
    return "_".join((event_id, mapped_cell_id, path_segment, role_key))


def target_output(target_job_id: str) -> Path:
    return OUTPUT / target_key(target_job_id)


def external_status_by_id() -> dict[str, dict[str, str]]:
    return {
        row["target_job_id"]: row
        for row in read_csv(STATUS_5462)
    }


def target_status(
    target: dict[str, str], external_rows: dict[str, dict[str, str]]
) -> dict[str, Any]:
    target_job_id = target["smoke_job_id"]
    finite_output = target_output(target_job_id)
    finite_result = finite_output / "result.json"
    finite_certificate = finite_output / "representative_certificate.csv"
    result_payload = read_json(finite_result) if finite_result.is_file() else {}
    finite_certified = (
        truth(result_payload.get("valid_for_target_outer_representative", False))
        and finite_certificate.is_file()
    )
    external = external_rows[target_job_id]
    external_certified = (
        external["status"] == "CERTIFIED"
        and truth(external["valid_for_target_outer_representative"])
        and Path(external["certificate_path"]).is_file()
    )
    first_failure = str(result_payload.get("first_failure_type", ""))
    cover_certified = truth(
        result_payload.get("valid_for_target_TOP_finite_projective_pivot_cover", False)
    )
    if finite_certified:
        status = "CERTIFIED_MINIMAL_DEPTH_5464"
        route = "checkpoint_5464_minimal_depth"
    elif external_certified:
        status = "CERTIFIED_EXTERNAL"
        route = external["route"]
    elif first_failure:
        status = "FIRST_FAILURE_REQUIRES_16X32_FALLBACK_OR_DERIVATION"
        route = "checkpoint_5464_minimal_depth"
    elif cover_certified:
        status = "PROJECTIVE_COVER_CERTIFIED_AMPLITUDE_PENDING"
        route = "checkpoint_5464_minimal_depth"
    elif finite_result.is_file():
        status = "PROJECTIVE_COVER_NOT_CLOSED__USE_16X32_FALLBACK"
        route = "checkpoint_5464_minimal_depth"
    else:
        status = "UNRUN"
        route = "unresolved"
    return {
        "checkpoint": CHECKPOINT,
        "target_job_id": target_job_id,
        "target_key": target_key(target_job_id),
        "event_id": target["event_id"],
        "mapped_cell_id": target["mapped_cell_id"],
        "selection_role": target["selection_role"],
        "epsilon_bin_index": int(target["epsilon_bin_index"]),
        "route": route,
        "status": status,
        "x_subdivision_count": X_SUBDIVISIONS,
        "t_subdivision_count": T_SUBDIVISIONS,
        "certified_binary_partition_depth": CERTIFIED_BINARY_PARTITION_DEPTH,
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
        "result_path": str(finite_result.resolve()),
        "certificate_path": str(finite_certificate.resolve()),
        "external_certificate_path": external["certificate_path"],
        "valid_for_target_outer_representative": finite_certified or external_certified,
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
        "# 5464: Minimal-depth D4 TOP finite projective amplitude runner",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Derived depth rule",
        "",
        "Parent v51 enables its special correlated/projective reconstruction only at `refinement_depth >= 8`. The established `16 x 32` dyadic grid has depth `4 + 5 = 9`. This checkpoint uses `8 x 32`, whose exact dyadic depth is `3 + 5 = 8`: the minimum depth that retains the parent gate while preserving the previous 32-way path-parameter resolution.",
        "",
        "Every selector, projective owner and amplitude interval is recomputed. A failed minimal-depth cell is not evidence against the target and is never promoted; it routes to the established `16 x 32` certificate or a local derivation.",
        "",
        f"Externally certified TOP targets: `{payload['external_certified_target_count']}`. Minimal-depth certificates: `{payload['minimal_depth_certified_target_count']}`. Pending minimal-depth amplitude targets: `{payload['cover_only_target_count']}`. First failures: `{payload['first_failure_target_count']}`.",
        "",
        "## Claim boundary",
        "",
        "A completed row certifies one extreme representative only. It does not certify all outer leaves, event-local W3, the regulator limit, local GR or full MTS.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def refresh_aggregate() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    external_rows = external_status_by_id()
    rows = [target_status(target, external_rows) for target in top_targets()]
    finite = [
        row for row in rows if row["status"] == "CERTIFIED_MINIMAL_DEPTH_5464"
    ]
    external = [row for row in rows if row["status"] == "CERTIFIED_EXTERNAL"]
    cover_only = [
        row
        for row in rows
        if row["status"] == "PROJECTIVE_COVER_CERTIFIED_AMPLITUDE_PENDING"
    ]
    failed = [
        row
        for row in rows
        if row["status"]
        == "FIRST_FAILURE_REQUIRES_16X32_FALLBACK_OR_DERIVATION"
    ]
    parent_text = SCRIPT_5396.read_text(encoding="utf-8")
    parent_depth_gate_count = parent_text.count("refinement_depth\"]) >= 8") + parent_text.count("refinement_depth\", 0)) >= 8")
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "MINIMAL_DEPTH_TOP_FIRST_FAILURE__USE_16X32_FALLBACK_OR_DERIVE"
            if failed
            else "MINIMAL_DEPTH_TOP_PARTIAL__RESUME"
        ),
        "target_count": len(rows),
        "external_certified_target_count": len(external),
        "minimal_depth_certified_target_count": len(finite),
        "cover_only_target_count": len(cover_only),
        "first_failure_target_count": len(failed),
        "x_subdivision_count": X_SUBDIVISIONS,
        "t_subdivision_count": T_SUBDIVISIONS,
        "x_binary_depth": X_BINARY_DEPTH,
        "t_binary_depth": T_BINARY_DEPTH,
        "certified_binary_partition_depth": CERTIFIED_BINARY_PARTITION_DEPTH,
        "parent_minimum_special_branch_depth": PARENT_MINIMUM_SPECIAL_BRANCH_DEPTH,
        "parent_depth_gate_occurrence_count": parent_depth_gate_count,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    finite_results = [
        Path(row["result_path"])
        for row in rows
        if Path(row["result_path"]).is_file()
    ]
    validations = [
        check("all_static_sources_exist", all(path.is_file() for path in (Path(__file__), SCRIPT_5396, SCRIPT_5461, SCRIPT_5462, REPRESENTATIVES_5456, STATUS_5462)), 6),
        check("manifest_has_25_unique_TOP_targets", len(rows) == 25 and len({row["target_job_id"] for row in rows}) == 25, len(rows)),
        check("eight_by_thirtytwo_grid_has_exact_binary_depth_eight", X_SUBDIVISIONS == 2 ** X_BINARY_DEPTH and T_SUBDIVISIONS == 2 ** T_BINARY_DEPTH and X_BINARY_DEPTH + T_BINARY_DEPTH == CERTIFIED_BINARY_PARTITION_DEPTH == PARENT_MINIMUM_SPECIAL_BRANCH_DEPTH, f"{X_BINARY_DEPTH}+{T_BINARY_DEPTH}={CERTIFIED_BINARY_PARTITION_DEPTH}"),
        check("parent_v51_contains_depth_eight_special_branch_gates", parent_depth_gate_count >= 2, parent_depth_gate_count),
        check("every_minimal_depth_certificate_has_a_valid_result", all(Path(row["certificate_path"]).is_file() and truth(read_json(Path(row["result_path"])).get("valid_for_target_outer_representative", False)) for row in finite), len(finite)),
        check("every_materialized_result_preserves_broad_claim_boundary", all(not truth(read_json(path).get("valid_for_full_outer_parent_leaf_enclosure", False)) and not truth(read_json(path).get("valid_for_D4_event_local_W3_bound", False)) and not truth(read_json(path).get("valid_for_all_operator_local_GR_claim", False)) and not truth(read_json(path).get("valid_for_full_MTS_claim", False)) for path in finite_results), len(finite_results)),
        check("aggregate_broad_claims_remain_false", not payload["valid_for_full_outer_parent_leaf_enclosure"] and not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "TOP representatives only"),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    source_paths = [Path(__file__), SCRIPT_5396, SCRIPT_5461, SCRIPT_5462, REPRESENTATIVES_5456, STATUS_5462]
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


def configure_base(target_job_id: str) -> Any:
    helper = load_module("mts_5462_for_5464", SCRIPT_5462)
    helper.CHECKPOINT = CHECKPOINT
    helper.REVISION = REVISION
    helper.generic_output = lambda unused_job_id: target_output(target_job_id)
    base = helper.configure_base(target_job_id)
    base.X_SUBDIVISIONS = X_SUBDIVISIONS
    base.T_SUBDIVISIONS = T_SUBDIVISIONS
    base.CERTIFIED_BINARY_PARTITION_DEPTH = CERTIFIED_BINARY_PARTITION_DEPTH
    original_source_paths = base.source_paths
    original_manifest = base.amplitude_manifest
    original_certificate = base.representative_certificate

    def source_paths() -> list[Path]:
        return list(dict.fromkeys([Path(__file__), SCRIPT_5396, SCRIPT_5462, *original_source_paths()]))

    def amplitude_manifest(
        target: dict[str, str], cover: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        rows = original_manifest(target, cover)
        for row in rows:
            row["smoke_job_id"] = row["smoke_job_id"].replace("5462__", "5464__", 1)
            row["valid_for_5464_amplitude_manifest"] = row.pop(
                "valid_for_5462_amplitude_manifest"
            )
        return rows

    def representative_certificate(
        target: dict[str, str],
        cells: list[dict[str, Any]],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        row = original_certificate(target, cells, payload)
        row["path_integral_enclosure_method"] = (
            "FINITE_8X32_MINIMAL_DEPTH_POINTWISE_SUPREMUM_SUM"
        )
        row["certificate_source"] = (
            "checkpoint_5464_minimal_depth_TOP_projective_amplitude_cover"
        )
        return row

    def render_document(payload: dict[str, Any]) -> None:
        lines = [
            f"# 5464 minimal-depth TOP target: {target_job_id}",
            "",
            "## Decision",
            "",
            f"**{payload['decision']}**",
            "",
            "This target uses the exact minimum parent-admissible dyadic depth: `8 x 32` cells give `3 + 5 = 8`, matching the parent-v51 special-branch threshold. Selector, projective-owner and amplitude bounds are recomputed on every cell.",
            "",
            f"Projective rows passed: `{payload['passed_projective_owner_row_count']}/{payload['projective_owner_row_count']}`. Amplitude cells completed: `{payload['completed_cell_count']}/{payload['manifest_cell_count']}`; failed: `{payload['failed_cell_count']}`.",
            "",
            "A failure routes to the established `16 x 32` runner or a local derivation; it is not treated as physical evidence. All broader claims remain false.",
            "",
        ]
        base.atomic_text(base.DOCUMENT, "\n".join(lines))

    base.source_paths = source_paths
    base.amplitude_manifest = amplitude_manifest
    base.representative_certificate = representative_certificate
    base.render_document = render_document
    return base


def normalize_payload(payload: dict[str, Any], target_job_id: str) -> dict[str, Any]:
    payload["checkpoint"] = CHECKPOINT
    payload["revision"] = REVISION
    payload["generic_target_key"] = target_key(target_job_id)
    payload["x_binary_depth"] = X_BINARY_DEPTH
    payload["t_binary_depth"] = T_BINARY_DEPTH
    payload["certified_binary_partition_depth"] = CERTIFIED_BINARY_PARTITION_DEPTH
    if truth(payload.get("valid_for_target_outer_representative", False)):
        payload["decision"] = (
            "MINIMAL_DEPTH_TOP_FINITE_COVER_CERTIFIED__RECONCILE_5460"
        )
        payload["next_target"] = "REFRESH_5464_AND_RECONCILE_5460"
    elif payload.get("first_failure_type"):
        payload["decision"] = (
            "MINIMAL_DEPTH_TOP_FIRST_FAILURE__USE_16X32_FALLBACK_OR_DERIVE"
        )
        payload["next_target"] = "RUN_ESTABLISHED_16X32_TARGET_OR_DERIVE"
    elif truth(payload.get("valid_for_target_TOP_finite_projective_pivot_cover", False)):
        payload["decision"] = (
            "MINIMAL_DEPTH_TOP_PROJECTIVE_COVER_CERTIFIED__AMPLITUDE_RESUME_REQUIRED"
        )
        payload["next_target"] = "RESUME_MINIMAL_DEPTH_AMPLITUDE_CELLS"
    else:
        payload["decision"] = (
            "MINIMAL_DEPTH_TOP_PROJECTIVE_COVER_NOT_CLOSED__USE_16X32_FALLBACK"
        )
        payload["next_target"] = "RUN_ESTABLISHED_16X32_TARGET"
    return payload


def run_target(
    target_job_id: str,
    max_jobs: int,
    cover_only: bool,
    allow_external_recheck: bool,
) -> dict[str, Any]:
    valid_ids = {row["smoke_job_id"] for row in top_targets()}
    if target_job_id not in valid_ids:
        raise ValueError(f"unknown TOP representative: {target_job_id}")
    external = external_status_by_id()[target_job_id]
    if external["status"] == "CERTIFIED" and not allow_external_recheck:
        raise ValueError(f"target already has an external passing certificate: {target_job_id}")
    before_formalization = {
        str(path.relative_to(FORMALIZATION)): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    } if FORMALIZATION.is_dir() else {}
    base = configure_base(target_job_id)
    payload = normalize_payload(base.run(max_jobs, cover_only), target_job_id)
    payload["external_certificate_recheck_requested"] = allow_external_recheck
    payload["preserved_external_certificate_path"] = (
        external["certificate_path"] if external["status"] == "CERTIFIED" else ""
    )
    after_formalization = {
        str(path.relative_to(FORMALIZATION)): (path.stat().st_size, path.stat().st_mtime_ns)
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    } if FORMALIZATION.is_dir() else {}
    if before_formalization != after_formalization:
        raise RuntimeError("formalization-workbench changed during checkpoint 5464")
    base.atomic_json(base.RESULT, payload)
    base.atomic_json(base.STATUS, payload)
    base.render_document(payload)
    refresh_aggregate()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-job-id")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--cover-only", action="store_true")
    parser.add_argument("--refresh-only", action="store_true")
    parser.add_argument("--list-targets", action="store_true")
    parser.add_argument("--allow-external-recheck", action="store_true")
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
    if not arguments.target_job_id:
        raise ValueError("--target-job-id is required for a minimal-depth run")
    payload = run_target(
        arguments.target_job_id,
        arguments.max_jobs,
        arguments.cover_only,
        arguments.allow_external_recheck,
    )
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
