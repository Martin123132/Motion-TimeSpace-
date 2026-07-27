from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_number(value: object) -> bool:
    try:
        float(str(value).strip())
        return True
    except ValueError:
        return False


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


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


def evaluate_constructor_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "motion_primitive_declared",
        "time_space_exchange_declared",
        "observed_metric_constructed",
        "matter_action_constructor_declared",
        "parent_generate_map_defined",
        "constructor_image_exhaustive",
        "hom_species_source_empty",
        "hidden_invariant_algebra_trivial",
        "no_extension_marker",
        "radiative_readout_closure",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    motion = as_bool(row.get("motion_primitive_declared"))
    time_space = as_bool(row.get("time_space_exchange_declared"))
    metric = as_bool(row.get("observed_metric_constructed"))
    matter_action = as_bool(row.get("matter_action_constructor_declared"))
    parent_generate = as_bool(row.get("parent_generate_map_defined"))
    exhaustive = as_bool(row.get("constructor_image_exhaustive"))
    hom_empty = as_bool(row.get("hom_species_source_empty"))
    hidden_trivial = as_bool(row.get("hidden_invariant_algebra_trivial"))
    no_marker = as_bool(row.get("no_extension_marker"))
    readout = as_bool(row.get("radiative_readout_closure"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    primitive_atlas_ready = motion and time_space and metric and matter_action and parent_generate
    no_slot_ready = primitive_atlas_ready and exhaustive and hom_empty
    no_reentry_ready = hidden_trivial and no_marker and readout
    constructor_exhaustion_ready = no_slot_ready and no_reentry_ready and source_ok and not missing
    claim_ready = constructor_exhaustion_ready and input_valid and requested_claim

    if claim_ready:
        status = "PARENT_CONSTRUCTOR_EXHAUSTION_SIGNED"
    elif constructor_exhaustion_ready:
        status = "PARENT_CONSTRUCTOR_EXHAUSTION_CONTRACT_READY_NONCLAIM"
    elif primitive_atlas_ready and not exhaustive:
        status = "PRIMITIVE_CONSTRUCTOR_ATLAS_READY_EXHAUSTION_OPEN"
    elif no_slot_ready and not no_reentry_ready:
        status = "HOM_NO_SLOT_READY_HIDDEN_READOUT_REENTRY_OPEN"
    elif primitive_atlas_ready and exhaustive and not hom_empty:
        status = "CONSTRUCTOR_EXHAUSTION_READY_HOM_OPEN"
    elif source_ok:
        status = "CONSTRUCTOR_EXHAUSTION_PARTIAL"
    else:
        status = "CONSTRUCTOR_EXHAUSTION_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("motion_primitive_declared", motion),
        ("time_space_exchange_declared", time_space),
        ("observed_metric_constructed", metric),
        ("matter_action_constructor_declared", matter_action),
        ("parent_generate_map_defined", parent_generate),
        ("constructor_image_exhaustive", exhaustive),
        ("hom_species_source_empty", hom_empty),
        ("hidden_invariant_algebra_trivial", hidden_trivial),
        ("no_extension_marker", no_marker),
        ("radiative_readout_closure", readout),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "primitive_atlas_ready": str(primitive_atlas_ready),
        "no_slot_ready": str(no_slot_ready),
        "no_reentry_ready": str(no_reentry_ready),
        "constructor_exhaustion_ready": str(constructor_exhaustion_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_coefficient_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "coefficient",
        "coefficient_kind",
        "value",
        "units",
        "source_path",
        "comparator_source",
        "independent_of_bound",
        "parent_basis_declared",
        "sign_convention_declared",
        "zero_certificate_source",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    value = str(row.get("value", "")).strip()
    numeric = is_number(value)
    derived_zero = value == "DERIVED_ZERO"
    missing_value = is_missing_like(value)
    source_ok = path_exists(row.get("source_path"))
    comparator_ok = path_exists(row.get("comparator_source"))
    zero_source_ok = path_exists(row.get("zero_certificate_source"))
    parent_coefficient = str(row.get("coefficient_kind", "")).strip() == "parent_coefficient"
    independent = as_bool(row.get("independent_of_bound"))
    basis = as_bool(row.get("parent_basis_declared"))
    sign = as_bool(row.get("sign_convention_declared"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    numeric_parent_ready = numeric and parent_coefficient and source_ok and comparator_ok and independent and basis and sign and not missing
    zero_parent_ready = derived_zero and parent_coefficient and zero_source_ok and independent and basis and sign and not missing
    score_ready = (numeric_parent_ready or zero_parent_ready) and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "PARENT_WEP_COEFFICIENT_CLAIM_READY"
    elif score_ready:
        status = "PARENT_WEP_COEFFICIENT_SCORE_READY_NONCLAIM"
    elif numeric and not parent_coefficient:
        status = "NUMERIC_COMPONENT_NOT_PARENT_COEFFICIENT"
    elif numeric_parent_ready:
        status = "SOURCE_BACKED_PARENT_COEFFICIENT_READY_INPUT_INVALID_NONCLAIM"
    elif zero_parent_ready:
        status = "DERIVED_ZERO_PARENT_COEFFICIENT_READY_INPUT_INVALID_NONCLAIM"
    elif missing_value and source_ok:
        status = "PARENT_COEFFICIENT_VALUE_MISSING_NONCLAIM"
    elif source_ok or comparator_ok:
        status = "PARENT_COEFFICIENT_BLOCKED_MISSING_INPUT"
    else:
        status = "PARENT_COEFFICIENT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("comparator_source_exists", comparator_ok),
        ("parent_coefficient_kind", parent_coefficient),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("independent_of_bound", independent),
        ("parent_basis_declared", basis),
        ("sign_convention_declared", sign),
        ("zero_certificate_source_exists_if_zero", True if not derived_zero else zero_source_ok),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "numeric_value": str(numeric),
        "derived_zero": str(derived_zero),
        "missing_value": str(missing_value),
        "source_exists": str(source_ok),
        "comparator_source_exists": str(comparator_ok),
        "zero_certificate_source_exists": str(zero_source_ok),
        "numeric_parent_ready": str(numeric_parent_ready),
        "zero_parent_ready": str(zero_parent_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_constructor_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_constructor_row(row, input_path) for row in read_csv(input_path)]


def evaluate_coefficient_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_coefficient_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate parent constructor exhaustion and WEP coefficient rows.")
    parser.add_argument("--mode", choices=["constructor", "coefficient"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_constructor_rows(args.input) if args.mode == "constructor" else evaluate_coefficient_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
