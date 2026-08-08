from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


RECOGNIZED_ROUTE_TYPES = {
    "positive_operator",
    "algebraic_zero",
    "source_grammar",
    "finite_source_row",
}

SECTOR_REQUIRED_FIELDS = [
    "component_id",
    "component",
    "route_type",
    "parent_variable_owned",
    "action_or_constraint_written",
    "maps_to_component",
    "self_adjoint_or_algebraic",
    "positive_or_invertible",
    "mass_gap_or_constraint_rank",
    "zero_source_or_no_hypermomentum",
    "boundary_no_flux_or_no_boundary",
    "metric_response_owned",
    "same_support",
    "uu_trace_projection_owned",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

SECTOR_BOOLEAN_FIELDS = [
    field
    for field in SECTOR_REQUIRED_FIELDS
    if field not in {"component_id", "component", "route_type", "source_path", "notes"}
]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def existing_path(value: object) -> bool:
    text = str(value).strip()
    return bool(text and "MISSING" not in text.upper() and Path(text).exists())


def evaluate_sector_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in SECTOR_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    booleans = {field: bool_text(row.get(field, "False")) for field in SECTOR_BOOLEAN_FIELDS}
    route_type = str(row.get("route_type", "")).strip()
    source_path = str(row.get("source_path", "")).strip()
    source_exists = existing_path(source_path)
    route_recognized = route_type in RECOGNIZED_ROUTE_TYPES
    input_valid = booleans["input_valid_for_claim"]

    map_ready = (
        booleans["maps_to_component"]
        and booleans["same_support"]
        and booleans["uu_trace_projection_owned"]
        and source_exists
    )
    operator_core_ready = (
        booleans["parent_variable_owned"]
        and booleans["action_or_constraint_written"]
        and booleans["self_adjoint_or_algebraic"]
        and booleans["positive_or_invertible"]
        and booleans["mass_gap_or_constraint_rank"]
        and booleans["zero_source_or_no_hypermomentum"]
        and booleans["boundary_no_flux_or_no_boundary"]
        and booleans["metric_response_owned"]
        and map_ready
    )
    positive_operator_ready = route_type == "positive_operator" and operator_core_ready
    algebraic_zero_ready = route_type == "algebraic_zero" and operator_core_ready
    source_grammar_ready = route_type == "source_grammar" and operator_core_ready
    finite_row_ready = route_type == "finite_source_row" and map_ready and input_valid
    zero_schema_ready = route_type in {
        "positive_operator",
        "algebraic_zero",
        "source_grammar",
    } and operator_core_ready

    claim_zero_ready = (
        input_valid
        and (positive_operator_ready or algebraic_zero_ready or source_grammar_ready)
    )
    claim_ready = claim_zero_ready or finite_row_ready

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not route_recognized:
        reasons.append("UNRECOGNIZED_ROUTE_TYPE")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    for field, value in booleans.items():
        if not value and field != "input_valid_for_claim":
            reasons.append(f"OPEN_{field.upper()}")
    if route_type == "positive_operator" and not operator_core_ready:
        reasons.append("POSITIVE_OPERATOR_CONTRACT_INCOMPLETE")
    if route_type == "algebraic_zero" and not operator_core_ready:
        reasons.append("ALGEBRAIC_ZERO_CONTRACT_INCOMPLETE")
    if route_type == "source_grammar" and not operator_core_ready:
        reasons.append("SOURCE_GRAMMAR_CONTRACT_INCOMPLETE")
    if route_type == "finite_source_row" and not finite_row_ready:
        reasons.append("FINITE_SOURCE_ROW_NOT_FILLED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if claim_zero_ready:
        status = "SECTOR_ZERO_READY"
    elif zero_schema_ready:
        status = "SECTOR_ZERO_SCHEMA_READY_NONCLAIM"
    elif route_type == "positive_operator":
        status = "POSITIVE_OPERATOR_ACTIVATION_BLOCKED"
    elif route_type == "algebraic_zero":
        status = "ALGEBRAIC_ZERO_ROUTE_CONDITIONAL_BLOCKED"
    elif route_type == "source_grammar":
        status = "SOURCE_GRAMMAR_ROUTE_REQUIRED_BLOCKED"
    elif route_type == "finite_source_row":
        status = "FINITE_SOURCE_ROW_REQUIRED"
    else:
        status = "SECTOR_ROUTE_UNCLASSIFIED"

    return {
        "component_id": str(row.get("component_id", "")),
        "component": str(row.get("component", "")),
        "route_type": route_type,
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "route_recognized": str(route_recognized),
        "map_ready": str(map_ready),
        "operator_core_ready": str(operator_core_ready),
        "zero_schema_ready": str(zero_schema_ready),
        "claim_zero_ready": str(claim_zero_ready),
        "finite_row_ready": str(finite_row_ready),
        "valid_for_claim": str(claim_ready),
        "claim_allowed": str(claim_ready),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_sector_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_sector_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify Ricci survivor slots by positive-operator, algebraic-zero, source-grammar, or finite-row route.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_csv(args.output, evaluate_sector_rows(args.input))


if __name__ == "__main__":
    main()
