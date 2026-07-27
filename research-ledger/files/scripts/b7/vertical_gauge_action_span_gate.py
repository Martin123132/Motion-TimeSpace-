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


def evaluate_span_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "q_map_declared",
        "field_chart_declared",
        "vertical_distribution_declared",
        "generator_list_declared",
        "parent_action_declared",
        "infinitesimal_action_map_declared",
        "Dq_generator_zero",
        "span_equals_kernel",
        "integrability_connected_fibre",
        "matter_readout_invariant",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    q_map = as_bool(row.get("q_map_declared"))
    field_chart = as_bool(row.get("field_chart_declared"))
    vertical = as_bool(row.get("vertical_distribution_declared"))
    generators = as_bool(row.get("generator_list_declared"))
    parent_action = as_bool(row.get("parent_action_declared"))
    action_map = as_bool(row.get("infinitesimal_action_map_declared"))
    dq_zero = as_bool(row.get("Dq_generator_zero"))
    span = as_bool(row.get("span_equals_kernel"))
    connected = as_bool(row.get("integrability_connected_fibre"))
    matter_readout = as_bool(row.get("matter_readout_invariant"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        q_map
        and field_chart
        and vertical
        and generators
        and parent_action
        and action_map
        and dq_zero
        and span
        and connected
        and matter_readout
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "VERTICAL_ACTION_SPAN_CLAIM_READY"
    elif score_ready:
        status = "VERTICAL_ACTION_SPAN_READY_NONCLAIM"
    elif contract_ready:
        status = "VERTICAL_ACTION_SPAN_CONTRACT_READY_NONCLAIM"
    elif q_map and field_chart and vertical and generators and not parent_action:
        status = "GENERATOR_LIST_READY_ACTION_UNSIGNED"
    elif parent_action and action_map and dq_zero and not span:
        status = "PARENT_ACTION_DECLARED_SPAN_UNSIGNED"
    elif q_map and field_chart and vertical and not generators:
        status = "FIELD_CHART_DQ_READY_ACTION_UNSIGNED"
    elif q_map or field_chart:
        status = "Q_MAP_PARTIAL"
    elif source_ok:
        status = "VERTICAL_ACTION_SPAN_PARTIAL"
    else:
        status = "SPAN_GATE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("q_map_declared", q_map),
        ("field_chart_declared", field_chart),
        ("vertical_distribution_declared", vertical),
        ("generator_list_declared", generators),
        ("parent_action_declared", parent_action),
        ("infinitesimal_action_map_declared", action_map),
        ("Dq_generator_zero", dq_zero),
        ("span_equals_kernel", span),
        ("integrability_connected_fibre", connected),
        ("matter_readout_invariant", matter_readout),
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


def evaluate_component_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "component",
        "coefficient_symbol",
        "value",
        "units",
        "parent_variation_basis",
        "observable_projection",
        "source_path",
        "empirical_anchor",
        "independent_of_bound",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    value = str(row.get("value", "")).strip()
    numeric = is_number(value)
    derived_zero = value == "DERIVED_ZERO"
    source_ok = path_exists(row.get("source_path"))
    units_ok = not is_missing_like(row.get("units"))
    basis_ok = not is_missing_like(row.get("parent_variation_basis"))
    projection_ok = not is_missing_like(row.get("observable_projection"))
    empirical_ok = not is_missing_like(row.get("empirical_anchor"))
    independent = as_bool(row.get("independent_of_bound"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    value_ready = (
        (numeric or derived_zero)
        and source_ok
        and units_ok
        and basis_ok
        and projection_ok
        and empirical_ok
        and independent
        and not missing
    )
    score_ready = value_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "FIRST_CSOURCE_COMPONENT_CLAIM_READY"
    elif score_ready:
        status = "FIRST_CSOURCE_COMPONENT_SCORE_READY_NONCLAIM"
    elif value_ready:
        status = "FIRST_CSOURCE_COMPONENT_INPUT_INVALID_NONCLAIM"
    elif source_ok:
        status = "FIRST_CSOURCE_COMPONENT_CONTRACT_ONLY"
    else:
        status = "FIRST_CSOURCE_COMPONENT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("units_declared", units_ok),
        ("parent_variation_basis_declared", basis_ok),
        ("observable_projection_declared", projection_ok),
        ("empirical_anchor_declared", empirical_ok),
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
        "source_exists": str(source_ok),
        "value_ready": str(value_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_span_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_span_row(row, input_path) for row in read_csv(input_path)]


def evaluate_component_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_component_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate parent vertical-gauge action span and first C_source rows.")
    parser.add_argument("--span-input", type=Path)
    parser.add_argument("--span-output", type=Path)
    parser.add_argument("--component-input", type=Path)
    parser.add_argument("--component-output", type=Path)
    args = parser.parse_args()

    if args.span_input and args.span_output:
        write_csv(args.span_output, evaluate_span_rows(args.span_input))
    if args.component_input and args.component_output:
        write_csv(args.component_output, evaluate_component_rows(args.component_input))


if __name__ == "__main__":
    main()
