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


def is_number(value: object) -> bool:
    try:
        float(str(value).strip())
        return True
    except ValueError:
        return False


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


def missing_required(row: Mapping[str, str], required: List[str]) -> str:
    return ";".join(name for name in required if str(row.get(name, "")).strip() == "")


def evaluate_edge_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "edge",
        "source_node",
        "target_node",
        "template_edge_present",
        "visible_action_term_present",
        "same_parent_action_line",
        "parent_owned_morphism",
        "nonzero_coupling",
        "action_density_functor_owned",
        "source_current_owner",
        "no_species_prefactor",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    template = as_bool(row.get("template_edge_present"))
    action_term = as_bool(row.get("visible_action_term_present"))
    same_line = as_bool(row.get("same_parent_action_line"))
    parent_owned = as_bool(row.get("parent_owned_morphism"))
    nonzero = as_bool(row.get("nonzero_coupling"))
    functor = as_bool(row.get("action_density_functor_owned"))
    current = as_bool(row.get("source_current_owner"))
    no_species = as_bool(row.get("no_species_prefactor"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        template
        and action_term
        and same_line
        and parent_owned
        and nonzero
        and functor
        and current
        and no_species
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    conditional_action_domain = source_ok and template and action_term and nonzero and no_species and not parent_owned
    parent_signature_missing = source_ok and template and not parent_owned
    source_current_gap = source_ok and template and action_term and parent_owned and not current
    partial = source_ok and (template or action_term or nonzero)

    if claim_ready:
        status = "ACTION_DENSITY_EDGE_CERTIFICATE_CLAIM_READY"
    elif score_ready:
        status = "ACTION_DENSITY_EDGE_CERTIFICATE_READY_NONCLAIM"
    elif contract_ready:
        status = "ACTION_DENSITY_EDGE_CERTIFICATE_CONTRACT_READY_NONCLAIM"
    elif source_current_gap:
        status = "ACTION_DENSITY_EDGE_SOURCE_CURRENT_OWNER_MISSING"
    elif conditional_action_domain:
        status = "ACTION_DENSITY_EDGE_CONDITIONAL_ACTION_DOMAIN_PARENT_UNSIGNED"
    elif parent_signature_missing:
        status = "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING"
    elif partial:
        status = "ACTION_DENSITY_EDGE_PARTIAL"
    elif source_ok:
        status = "ACTION_DENSITY_EDGE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "ACTION_DENSITY_EDGE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("template_edge_present", template),
        ("visible_action_term_present", action_term),
        ("same_parent_action_line", same_line),
        ("parent_owned_morphism", parent_owned),
        ("nonzero_coupling", nonzero),
        ("action_density_functor_owned", functor),
        ("source_current_owner", current),
        ("no_species_prefactor", no_species),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_ready": str(contract_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_k_source_leg_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "product",
        "coefficient_value",
        "units",
        "parent_coefficient_source",
        "source_leg",
        "source_leg_units",
        "projection",
        "bound_value",
        "no_bound_inversion_guard",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    value = str(row.get("coefficient_value", "")).strip()
    numeric = is_number(value)
    derived_zero = value.upper() == "DERIVED_ZERO"
    bound_only = value.upper().startswith("BOUND_ONLY")
    common = value.upper() == "COMMON_CALIBRATION_ONLY"
    units_ok = not is_missing_like(row.get("units"))
    parent_ok = not is_missing_like(row.get("parent_coefficient_source"))
    leg_ok = not is_missing_like(row.get("source_leg"))
    leg_units_ok = not is_missing_like(row.get("source_leg_units"))
    projection_ok = not is_missing_like(row.get("projection"))
    bound_ok = is_number(row.get("bound_value"))
    guard = as_bool(row.get("no_bound_inversion_guard"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = source_ok and units_ok and projection_ok and bound_ok and guard and not missing
    numeric_ready = contract_ready and (numeric or derived_zero or common) and parent_ok and leg_ok and leg_units_ok
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "K_ACTION_SOURCE_LEG_CLAIM_READY"
    elif score_ready:
        status = "K_ACTION_SOURCE_LEG_READY_NONCLAIM"
    elif numeric_ready:
        status = "K_ACTION_SOURCE_LEG_INPUT_INVALID_NONCLAIM"
    elif bound_only and contract_ready:
        status = "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY"
    elif contract_ready:
        status = "K_ACTION_SOURCE_LEG_CONTRACT_ONLY"
    elif source_ok:
        status = "K_ACTION_SOURCE_LEG_PARTIAL"
    else:
        status = "K_ACTION_SOURCE_LEG_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_zero_or_common_value", numeric or derived_zero or common),
        ("units", units_ok),
        ("parent_coefficient_source", parent_ok),
        ("source_leg", leg_ok),
        ("source_leg_units", leg_units_ok),
        ("projection", projection_ok),
        ("bound_value_numeric", bound_ok),
        ("no_bound_inversion_guard", guard),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_ready": str(contract_ready),
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_edge_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_edge_row(row, input_path) for row in read_csv(input_path)]


def evaluate_k_source_leg_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_k_source_leg_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4435 action-density edge/source-leg rows.")
    parser.add_argument("--kind", choices=["edge", "kleg"], required=True)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.kind == "edge":
        rows = evaluate_edge_rows(args.input)
    else:
        rows = evaluate_k_source_leg_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
