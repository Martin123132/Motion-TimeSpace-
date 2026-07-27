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


def evaluate_rho_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "field_block",
        "rho_formula",
        "q_component",
        "parent_owned",
        "field_action_complete",
        "Dq_rho_zero",
        "source_readout_silent",
        "theta_marker_silent",
        "boundary_tau_silent",
        "contributes_to_kernel_span",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    parent_owned = as_bool(row.get("parent_owned"))
    action_complete = as_bool(row.get("field_action_complete"))
    dq_zero = as_bool(row.get("Dq_rho_zero"))
    source_silent = as_bool(row.get("source_readout_silent"))
    theta_silent = as_bool(row.get("theta_marker_silent"))
    boundary_silent = as_bool(row.get("boundary_tau_silent"))
    span = as_bool(row.get("contributes_to_kernel_span"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    component_closed = (
        parent_owned
        and action_complete
        and dq_zero
        and source_silent
        and theta_silent
        and boundary_silent
        and source_ok
        and not missing
    )
    span_closed = component_closed and span
    score_ready = span_closed and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "RHO_COMPONENT_CLAIM_READY"
    elif score_ready:
        status = "RHO_COMPONENT_SPAN_READY_NONCLAIM"
    elif span_closed:
        status = "RHO_COMPONENT_SPAN_CONTRACT_READY_NONCLAIM"
    elif component_closed:
        status = "RHO_COMPONENT_DQ_ZERO_NOT_KERNEL_SPAN"
    elif action_complete and dq_zero and not parent_owned:
        status = "RHO_COMPONENT_FORMAL_DQ_ZERO_PARENT_UNSIGNED"
    elif action_complete and not dq_zero:
        status = "RHO_COMPONENT_LEAK_RETAINED"
    elif source_ok:
        status = "RHO_COMPONENT_ACTION_INCOMPLETE"
    else:
        status = "RHO_COMPONENT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("parent_owned", parent_owned),
        ("field_action_complete", action_complete),
        ("Dq_rho_zero", dq_zero),
        ("source_readout_silent", source_silent),
        ("theta_marker_silent", theta_silent),
        ("boundary_tau_silent", boundary_silent),
        ("contributes_to_kernel_span", span),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "component_closed": str(component_closed),
        "span_closed": str(span_closed),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_span_branch(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "branch_id",
        "branch_name",
        "q_map_signed",
        "rho_components_complete",
        "all_Dq_zero",
        "im_rho_equals_kernel",
        "rank_bracket_integrable",
        "connected_fibres",
        "matter_readout_closed",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    q_ok = as_bool(row.get("q_map_signed"))
    components = as_bool(row.get("rho_components_complete"))
    dq_zero = as_bool(row.get("all_Dq_zero"))
    span = as_bool(row.get("im_rho_equals_kernel"))
    rank = as_bool(row.get("rank_bracket_integrable"))
    connected = as_bool(row.get("connected_fibres"))
    matter = as_bool(row.get("matter_readout_closed"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = q_ok and components and dq_zero and span and rank and connected and matter and source_ok and not missing
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "RHO_SPAN_CLAIM_READY"
    elif score_ready:
        status = "RHO_SPAN_READY_NONCLAIM"
    elif contract_ready:
        status = "RHO_SPAN_CONTRACT_READY_NONCLAIM"
    elif q_ok and components and dq_zero and not span:
        status = "RHO_GAUGE_SUBDISTRIBUTION_ONLY"
    elif q_ok and not components:
        status = "RHO_SPAN_TARGET_COMPONENTS_MISSING"
    elif source_ok:
        status = "RHO_SPAN_PARTIAL"
    else:
        status = "RHO_SPAN_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("q_map_signed", q_ok),
        ("rho_components_complete", components),
        ("all_Dq_zero", dq_zero),
        ("im_rho_equals_kernel", span),
        ("rank_bracket_integrable", rank),
        ("connected_fibres", connected),
        ("matter_readout_closed", matter),
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


def evaluate_cspecies_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "route",
        "coefficient_symbol",
        "value",
        "units",
        "theorem_or_numeric_source",
        "projection_formula",
        "source_path",
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
    theorem_ok = not is_missing_like(row.get("theorem_or_numeric_source"))
    projection_ok = not is_missing_like(row.get("projection_formula"))
    independent = as_bool(row.get("independent_of_bound"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    value_ready = (numeric or derived_zero) and source_ok and units_ok and theorem_ok and projection_ok and independent and not missing
    score_ready = value_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "CSPECIES_CLAIM_READY"
    elif score_ready:
        status = "CSPECIES_SCORE_READY_NONCLAIM"
    elif value_ready:
        status = "CSPECIES_INPUT_INVALID_NONCLAIM"
    elif bound_only and source_ok:
        status = "CSPECIES_BOUND_INTERFACE_ONLY"
    elif source_ok:
        status = "CSPECIES_CONTRACT_ONLY"
    else:
        status = "CSPECIES_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("units_declared", units_ok),
        ("theorem_or_numeric_source_declared", theorem_ok),
        ("projection_formula_declared", projection_ok),
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


def evaluate_rho_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_rho_row(row, input_path) for row in read_csv(input_path)]


def evaluate_span_branches(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_span_branch(row, input_path) for row in read_csv(input_path)]


def evaluate_cspecies_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_cspecies_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate rho field-map, span, and C_species rows.")
    parser.add_argument("--rho-input", type=Path)
    parser.add_argument("--rho-output", type=Path)
    parser.add_argument("--span-input", type=Path)
    parser.add_argument("--span-output", type=Path)
    parser.add_argument("--cspecies-input", type=Path)
    parser.add_argument("--cspecies-output", type=Path)
    args = parser.parse_args()

    if args.rho_input and args.rho_output:
        write_csv(args.rho_output, evaluate_rho_rows(args.rho_input))
    if args.span_input and args.span_output:
        write_csv(args.span_output, evaluate_span_branches(args.span_input))
    if args.cspecies_input and args.cspecies_output:
        write_csv(args.cspecies_output, evaluate_cspecies_rows(args.cspecies_input))


if __name__ == "__main__":
    main()
