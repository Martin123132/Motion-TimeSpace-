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


def is_number(value: object) -> bool:
    try:
        float(str(value).strip())
        return True
    except ValueError:
        return False


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


def evaluate_hidden_rho_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "sector",
        "hidden_variable",
        "parent_phase_space_declared",
        "constraint_or_aux_equation_declared",
        "constraint_origin_parent_owned",
        "generator_or_solve_declared",
        "first_class_or_auxiliary_closed",
        "zero_boundary_charge_or_no_tail",
        "Dq_after_elimination_zero",
        "matter_readout_descends",
        "source_species_silent",
        "kernel_span_or_eliminated",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    phase = as_bool(row.get("parent_phase_space_declared"))
    equation = as_bool(row.get("constraint_or_aux_equation_declared"))
    owned = as_bool(row.get("constraint_origin_parent_owned"))
    generator = as_bool(row.get("generator_or_solve_declared"))
    class_closed = as_bool(row.get("first_class_or_auxiliary_closed"))
    boundary = as_bool(row.get("zero_boundary_charge_or_no_tail"))
    dq_zero = as_bool(row.get("Dq_after_elimination_zero"))
    matter = as_bool(row.get("matter_readout_descends"))
    species = as_bool(row.get("source_species_silent"))
    eliminated = as_bool(row.get("kernel_span_or_eliminated"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        phase
        and equation
        and owned
        and generator
        and class_closed
        and boundary
        and dq_zero
        and matter
        and species
        and eliminated
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "HIDDEN_RHO_CONSTRAINT_CLAIM_READY"
    elif score_ready:
        status = "HIDDEN_RHO_CONSTRAINT_READY_NONCLAIM"
    elif contract_ready:
        status = "HIDDEN_RHO_CONSTRAINT_CONTRACT_READY_NONCLAIM"
    elif phase and equation and owned and generator and class_closed and not boundary:
        status = "HIDDEN_RHO_BOUNDARY_TAIL_OPEN"
    elif phase and equation and not owned:
        status = "HIDDEN_RHO_CONSTRAINT_ORIGIN_UNSIGNED"
    elif phase and equation and owned and not generator:
        status = "HIDDEN_RHO_GENERATOR_OR_SOLVE_MISSING"
    elif phase or equation:
        status = "HIDDEN_RHO_CONSTRAINT_PARTIAL"
    elif source_ok:
        status = "HIDDEN_RHO_CONSTRAINT_BLOCKED_BY_CURRENT_CORPUS"
    else:
        status = "HIDDEN_RHO_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("parent_phase_space_declared", phase),
        ("constraint_or_aux_equation_declared", equation),
        ("constraint_origin_parent_owned", owned),
        ("generator_or_solve_declared", generator),
        ("first_class_or_auxiliary_closed", class_closed),
        ("zero_boundary_charge_or_no_tail", boundary),
        ("Dq_after_elimination_zero", dq_zero),
        ("matter_readout_descends", matter),
        ("source_species_silent", species),
        ("kernel_span_or_eliminated", eliminated),
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


def evaluate_cspecies_zero_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "theorem_piece",
        "total_hilbert_owner",
        "source_domain_label_forgotten",
        "no_source_only_weights",
        "no_hidden_marker_return",
        "nonhilbert_bypass_excluded",
        "exchange_connected_or_common",
        "common_calibration_only",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    hilbert = as_bool(row.get("total_hilbert_owner"))
    label = as_bool(row.get("source_domain_label_forgotten"))
    weights = as_bool(row.get("no_source_only_weights"))
    hidden = as_bool(row.get("no_hidden_marker_return"))
    nonhilbert = as_bool(row.get("nonhilbert_bypass_excluded"))
    exchange = as_bool(row.get("exchange_connected_or_common"))
    common = as_bool(row.get("common_calibration_only"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = hilbert and label and weights and hidden and nonhilbert and exchange and common and source_ok and not missing
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    partial_collapse = hilbert and weights and exchange and common and source_ok and not hidden and not nonhilbert

    if claim_ready:
        status = "CSPECIES_ZERO_CLAIM_READY"
    elif score_ready:
        status = "CSPECIES_ZERO_READY_NONCLAIM"
    elif contract_ready:
        status = "CSPECIES_ZERO_CONTRACT_READY_NONCLAIM"
    elif partial_collapse:
        status = "CSPECIES_COLLAPSES_TO_SHADOW_AND_NONHILBERT_RESIDUALS"
    elif hilbert and label and not weights:
        status = "CSPECIES_SOURCE_WEIGHT_SLOT_OPEN"
    elif hilbert or label:
        status = "CSPECIES_ZERO_PARTIAL"
    elif source_ok:
        status = "CSPECIES_ZERO_BLOCKED_CURRENT_CORPUS"
    else:
        status = "CSPECIES_ZERO_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("total_hilbert_owner", hilbert),
        ("source_domain_label_forgotten", label),
        ("no_source_only_weights", weights),
        ("no_hidden_marker_return", hidden),
        ("nonhilbert_bypass_excluded", nonhilbert),
        ("exchange_connected_or_common", exchange),
        ("common_calibration_only", common),
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
        "partial_collapse": str(partial_collapse),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_bound_map_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "coefficient",
        "value",
        "units",
        "projection_formula",
        "source_path",
        "mts_coefficient_map_present",
        "source_leg_present",
        "independent_of_bound",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    value = str(row.get("value", "")).strip()
    numeric = is_number(value)
    derived_zero = value == "DERIVED_ZERO"
    bound_only = value.startswith("BOUND_ONLY:")
    source_ok = path_exists(row.get("source_path"))
    units_ok = not is_missing_like(row.get("units"))
    projection_ok = not is_missing_like(row.get("projection_formula"))
    map_ok = as_bool(row.get("mts_coefficient_map_present"))
    source_leg_ok = as_bool(row.get("source_leg_present"))
    independent = as_bool(row.get("independent_of_bound"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    value_ready = (numeric or derived_zero) and source_ok and units_ok and projection_ok and map_ok and source_leg_ok and independent and not missing
    score_ready = value_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "CSPECIES_BOUND_MAP_CLAIM_READY"
    elif score_ready:
        status = "CSPECIES_BOUND_MAP_READY_NONCLAIM"
    elif value_ready:
        status = "CSPECIES_BOUND_MAP_INPUT_INVALID_NONCLAIM"
    elif bound_only and source_ok and projection_ok:
        status = "CSPECIES_BOUND_INTERFACE_MTS_MAP_MISSING"
    elif source_ok:
        status = "CSPECIES_BOUND_MAP_CONTRACT_ONLY"
    else:
        status = "CSPECIES_BOUND_MAP_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("units_declared", units_ok),
        ("projection_formula_declared", projection_ok),
        ("mts_coefficient_map_present", map_ok),
        ("source_leg_present", source_leg_ok),
        ("independent_of_bound", independent),
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
        "bound_only": str(bound_only),
        "source_exists": str(source_ok),
        "value_ready": str(value_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_hidden_rho_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_hidden_rho_row(row, input_path) for row in read_csv(input_path)]


def evaluate_cspecies_zero_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_cspecies_zero_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_map_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_bound_map_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate hidden rho constraint routes and C_species zero/bound rows.")
    parser.add_argument("--rho-input", type=Path)
    parser.add_argument("--rho-output", type=Path)
    parser.add_argument("--cspecies-input", type=Path)
    parser.add_argument("--cspecies-output", type=Path)
    parser.add_argument("--bound-input", type=Path)
    parser.add_argument("--bound-output", type=Path)
    args = parser.parse_args()

    if args.rho_input and args.rho_output:
        write_csv(args.rho_output, evaluate_hidden_rho_rows(args.rho_input))
    if args.cspecies_input and args.cspecies_output:
        write_csv(args.cspecies_output, evaluate_cspecies_zero_rows(args.cspecies_input))
    if args.bound_input and args.bound_output:
        write_csv(args.bound_output, evaluate_bound_map_rows(args.bound_input))


if __name__ == "__main__":
    main()
