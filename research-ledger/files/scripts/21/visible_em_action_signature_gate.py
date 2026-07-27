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


def evaluate_signature_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required_fields = [
        "row_id",
        "branch",
        "action_block_present",
        "observed_hodge_owned",
        "same_parent_action_line",
        "parent_owned_action_domain",
        "unique_F2_no_extra_prefactor",
        "charge_current_owner",
        "fixed_representation_constants",
        "no_species_source_prefactor",
        "readout_after_variation",
        "radiative_closure",
        "poynting_once_only",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required_fields)
    source_ok = path_exists(row.get("source_path"))
    action_block = as_bool(row.get("action_block_present"))
    hodge_owned = as_bool(row.get("observed_hodge_owned"))
    same_line = as_bool(row.get("same_parent_action_line"))
    parent_owned = as_bool(row.get("parent_owned_action_domain"))
    unique_f2 = as_bool(row.get("unique_F2_no_extra_prefactor"))
    current_owner = as_bool(row.get("charge_current_owner"))
    fixed_representation = as_bool(row.get("fixed_representation_constants"))
    no_species = as_bool(row.get("no_species_source_prefactor"))
    readout_after_variation = as_bool(row.get("readout_after_variation"))
    radiative_closure = as_bool(row.get("radiative_closure"))
    poynting_once = as_bool(row.get("poynting_once_only"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    edge_signature_ready = (
        source_ok
        and action_block
        and hodge_owned
        and same_line
        and parent_owned
        and fixed_representation
        and no_species
        and readout_after_variation
        and poynting_once
        and not missing
    )
    scale_current_ready = edge_signature_ready and unique_f2 and current_owner and radiative_closure
    score_ready = scale_current_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "VISIBLE_EM_EDGE_AND_SCALE_CLAIM_READY"
    elif score_ready:
        status = "VISIBLE_EM_EDGE_AND_SCALE_READY_NONCLAIM"
    elif scale_current_ready:
        status = "VISIBLE_EM_EDGE_SCALE_READY_INPUT_INVALID_NONCLAIM"
    elif edge_signature_ready:
        status = "VISIBLE_EM_EDGE_SIGNATURE_READY_SCALE_GATES_OPEN"
    elif source_ok and action_block and hodge_owned and poynting_once and not parent_owned:
        status = "VISIBLE_EM_ACTION_CONDITIONAL_GLOBAL_PARENT_UNSIGNED"
    elif source_ok and parent_owned and not unique_f2:
        status = "VISIBLE_EM_EDGE_PARENT_BRANCH_SIGNED_UNIQUE_F2_OPEN"
    elif source_ok and action_block:
        status = "VISIBLE_EM_ACTION_PARTIAL"
    elif source_ok:
        status = "VISIBLE_EM_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "VISIBLE_EM_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for field_name, ok in [
        ("source_exists", source_ok),
        ("action_block_present", action_block),
        ("observed_hodge_owned", hodge_owned),
        ("same_parent_action_line", same_line),
        ("parent_owned_action_domain", parent_owned),
        ("unique_F2_no_extra_prefactor", unique_f2),
        ("charge_current_owner", current_owner),
        ("fixed_representation_constants", fixed_representation),
        ("no_species_source_prefactor", no_species),
        ("readout_after_variation", readout_after_variation),
        ("radiative_closure", radiative_closure),
        ("poynting_once_only", poynting_once),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(field_name)

    return {
        **{field_name: str(value) for field_name, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "edge_signature_ready": str(edge_signature_ready),
        "scale_current_ready": str(scale_current_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_signature_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_signature_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4436 visible EM action-edge parent signature rows.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_csv(args.output, evaluate_signature_rows(args.input))


if __name__ == "__main__":
    main()
