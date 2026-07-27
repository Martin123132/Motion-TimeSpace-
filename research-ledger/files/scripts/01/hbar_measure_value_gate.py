from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}
SCHEMA_PREFIXES = ("SCHEMA_", "MISSING_", "BOUND_", "NOT_PRIMARY_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_number(value: object) -> bool:
    try:
        float(str(value).strip())
        return True
    except ValueError:
        return False


def is_schema_value(value: object) -> bool:
    return str(value).strip().startswith(SCHEMA_PREFIXES)


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and not is_schema_value(text) and Path(text).exists()


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


def evaluate_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "single_phase_line",
        "universal_hbar_parent",
        "common_path_integral_measure",
        "species_blind_measure_jacobian",
        "ordinary_matter_same_phase_bundle",
        "no_species_hbar_A",
        "action_density_line_owner",
        "hbar_measure_current_owner",
        "tau_projectable",
        "Req_route_ready",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    phase_line = as_bool(row.get("single_phase_line"))
    universal_hbar = as_bool(row.get("universal_hbar_parent"))
    common_measure = as_bool(row.get("common_path_integral_measure"))
    species_blind = as_bool(row.get("species_blind_measure_jacobian"))
    same_bundle = as_bool(row.get("ordinary_matter_same_phase_bundle"))
    no_species_hbar = as_bool(row.get("no_species_hbar_A"))
    action_density = as_bool(row.get("action_density_line_owner"))
    current_owner = as_bool(row.get("hbar_measure_current_owner"))
    tau_projectable = as_bool(row.get("tau_projectable"))
    req_ready = as_bool(row.get("Req_route_ready"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    hbar_measure_ready = universal_hbar and common_measure and species_blind and no_species_hbar
    matter_owner_ready = same_bundle and action_density and current_owner
    route_ready = tau_projectable and req_ready
    owner_ready = phase_line and hbar_measure_ready and matter_owner_ready and route_ready and source_ok and not missing
    claim_ready = owner_ready and input_valid and requested_claim

    if claim_ready:
        status = "UNIVERSAL_HBAR_MEASURE_PARENT_SIGNED"
    elif owner_ready:
        status = "UNIVERSAL_HBAR_MEASURE_CONTRACT_READY_NONCLAIM"
    elif phase_line and not hbar_measure_ready:
        status = "PHASE_LINE_READY_HBAR_MEASURE_OPEN"
    elif phase_line and hbar_measure_ready and not matter_owner_ready:
        status = "HBAR_MEASURE_READY_MATTER_OWNER_OPEN"
    elif phase_line and hbar_measure_ready and matter_owner_ready and not route_ready:
        status = "HBAR_MEASURE_OWNER_READY_TAU_REQ_OPEN"
    elif source_ok:
        status = "UNIVERSAL_HBAR_MEASURE_BLOCKED"
    else:
        status = "UNIVERSAL_HBAR_MEASURE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("single_phase_line", phase_line),
        ("universal_hbar_parent", universal_hbar),
        ("common_path_integral_measure", common_measure),
        ("species_blind_measure_jacobian", species_blind),
        ("ordinary_matter_same_phase_bundle", same_bundle),
        ("no_species_hbar_A", no_species_hbar),
        ("action_density_line_owner", action_density),
        ("hbar_measure_current_owner", current_owner),
        ("tau_projectable", tau_projectable),
        ("Req_route_ready", req_ready),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "hbar_measure_ready": str(hbar_measure_ready),
        "matter_owner_ready": str(matter_owner_ready),
        "route_ready": str(route_ready),
        "owner_ready": str(owner_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_value_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "value_id",
        "quantity",
        "arena",
        "normal_form",
        "predicted_value",
        "prediction_source",
        "projection_source",
        "comparator_value",
        "comparator_source",
        "units",
        "parent_coefficient_source",
        "official_numeric_source",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    predicted_value = row.get("predicted_value", "")
    comparator_value = row.get("comparator_value", "")
    predicted_numeric = is_number(predicted_value)
    comparator_numeric = is_number(comparator_value)
    predicted_schema = is_schema_value(predicted_value)
    comparator_schema = is_schema_value(comparator_value)
    prediction_source_ok = path_exists(row.get("prediction_source"))
    projection_source_ok = path_exists(row.get("projection_source"))
    comparator_source_ok = path_exists(row.get("comparator_source"))
    parent_source_ok = path_exists(row.get("parent_coefficient_source"))
    official_source_ok = path_exists(row.get("official_numeric_source"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    schema_ready = (
        comparator_source_ok
        and not missing
        and (predicted_numeric or predicted_schema)
        and (comparator_numeric or comparator_schema)
    )
    score_ready = (
        schema_ready
        and predicted_numeric
        and comparator_numeric
        and prediction_source_ok
        and projection_source_ok
        and parent_source_ok
        and official_source_ok
        and input_valid
    )
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "FINITE_PREDICTION_VALUE_SCORE_READY"
    elif score_ready:
        status = "FINITE_PREDICTION_VALUE_SCORE_READY_NONCLAIM"
    elif schema_ready and comparator_numeric and not predicted_numeric:
        status = "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM"
    elif schema_ready:
        status = "PREDICTION_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    elif comparator_source_ok or prediction_source_ok:
        status = "FINITE_PREDICTION_VALUE_BLOCKED_MISSING_INPUT"
    else:
        status = "FINITE_PREDICTION_VALUE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("schema_ready", schema_ready),
        ("predicted_numeric", predicted_numeric),
        ("comparator_numeric", comparator_numeric),
        ("prediction_source_exists", prediction_source_ok),
        ("projection_source_exists", projection_source_ok),
        ("comparator_source_exists", comparator_source_ok),
        ("parent_coefficient_source_exists", parent_source_ok),
        ("official_numeric_source_exists", official_source_ok),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "predicted_numeric": str(predicted_numeric),
        "comparator_numeric": str(comparator_numeric),
        "prediction_source_exists": str(prediction_source_ok),
        "projection_source_exists": str(projection_source_ok),
        "comparator_source_exists": str(comparator_source_ok),
        "parent_coefficient_source_exists": str(parent_source_ok),
        "official_numeric_source_exists": str(official_source_ok),
        "schema_ready": str(schema_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_value_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_value_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate universal hbar/measure owner or first prediction-value rows.")
    parser.add_argument("--mode", choices=["owner", "value"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_owner_rows(args.input) if args.mode == "owner" else evaluate_value_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
