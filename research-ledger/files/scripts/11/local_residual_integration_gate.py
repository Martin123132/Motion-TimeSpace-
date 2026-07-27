from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_", "UNKNOWN_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return not text or any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and not is_missing_like(text) and Path(text).exists()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def missing_required(row: Mapping[str, str], required_fields: List[str]) -> str:
    return ";".join(field_name for field_name in required_fields if str(row.get(field_name, "")).strip() == "")


def evaluate_local_residual_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required_fields = [
        "row_id",
        "branch",
        "owner_tail_deleted",
        "fixed_branch_EM_zero",
        "open_EM_retained",
        "source_charge_closed",
        "coupling_no_drift_closed",
        "geometry_projection_closed",
        "nonEH_closed",
        "parent_selector_adopted",
        "empirical_projection_ready",
        "source_path",
        "input_valid",
        "valid_for_claim",
        "notes",
    ]
    missing = missing_required(row, required_fields)
    source_ok = path_exists(row.get("source_path"))
    owner_tail_deleted = as_bool(row.get("owner_tail_deleted"))
    fixed_branch_em_zero = as_bool(row.get("fixed_branch_EM_zero"))
    open_em_retained = as_bool(row.get("open_EM_retained"))
    source_charge_closed = as_bool(row.get("source_charge_closed"))
    coupling_no_drift_closed = as_bool(row.get("coupling_no_drift_closed"))
    geometry_projection_closed = as_bool(row.get("geometry_projection_closed"))
    noneh_closed = as_bool(row.get("nonEH_closed"))
    parent_selector_adopted = as_bool(row.get("parent_selector_adopted"))
    empirical_projection_ready = as_bool(row.get("empirical_projection_ready"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    fixed_branch_vector_rewired = (
        source_ok
        and owner_tail_deleted
        and fixed_branch_em_zero
        and open_em_retained
        and not missing
    )
    nonem_blockers_closed = (
        source_charge_closed
        and coupling_no_drift_closed
        and geometry_projection_closed
        and noneh_closed
        and parent_selector_adopted
        and empirical_projection_ready
    )
    score_ready = fixed_branch_vector_rewired and input_valid
    claim_ready = score_ready and nonem_blockers_closed and requested_claim

    if claim_ready:
        status = "LOCAL_GR_RESIDUAL_CLAIM_READY"
    elif fixed_branch_vector_rewired and not nonem_blockers_closed:
        status = "FIXED_BRANCH_EM_DELETED_NONEM_BLOCKERS_REMAIN"
    elif source_ok and open_em_retained and not fixed_branch_em_zero:
        status = "OPEN_EM_BRANCH_RETAINED"
    elif source_ok and fixed_branch_em_zero and not open_em_retained:
        status = "BRANCH_DOMAIN_UNSAFE_OPEN_EM_NOT_RETAINED"
    elif source_ok:
        status = "LOCAL_RESIDUAL_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "LOCAL_RESIDUAL_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for field_name, ok in [
        ("source_exists", source_ok),
        ("owner_tail_deleted", owner_tail_deleted),
        ("fixed_branch_EM_zero", fixed_branch_em_zero),
        ("open_EM_retained", open_em_retained),
        ("source_charge_closed", source_charge_closed),
        ("coupling_no_drift_closed", coupling_no_drift_closed),
        ("geometry_projection_closed", geometry_projection_closed),
        ("nonEH_closed", noneh_closed),
        ("parent_selector_adopted", parent_selector_adopted),
        ("empirical_projection_ready", empirical_projection_ready),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(field_name)

    return {
        **{field_name: str(value) for field_name, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "fixed_branch_vector_rewired": str(fixed_branch_vector_rewired),
        "nonEM_blockers_closed": str(nonem_blockers_closed),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_local_residual_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_local_residual_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4439 local residual integration rows.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_csv(args.output, evaluate_local_residual_rows(args.input))


if __name__ == "__main__":
    main()
