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
    text = str(value).strip()
    return text.startswith(SCHEMA_PREFIXES)


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
        for row in rows:
            writer.writerow(row)


def source_exists(row: Mapping[str, str]) -> bool:
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and Path(source_path).exists()


def missing_required(row: Mapping[str, str], required: List[str]) -> str:
    return ";".join(name for name in required if str(row.get(name, "")).strip() == "")


def evaluate_phase_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "branch",
        "parent_time_flow_unique",
        "phase_action_line_defined",
        "single_hbar_phase_unit",
        "universal_quantum_statistical_measure",
        "ordinary_matter_same_phase_bundle",
        "no_species_hbar_or_action_clock",
        "tau_projectable_through_q",
        "clock_phase_traversal_split_respected",
        "species_blind_measure_jacobian",
        "variation_before_readout",
        "hilbert_current_same_action",
        "Req_same_current_route",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    time_flow = as_bool(row.get("parent_time_flow_unique"))
    phase_line = as_bool(row.get("phase_action_line_defined"))
    hbar_unit = as_bool(row.get("single_hbar_phase_unit"))
    quantum_measure = as_bool(row.get("universal_quantum_statistical_measure"))
    same_bundle = as_bool(row.get("ordinary_matter_same_phase_bundle"))
    no_species_clock = as_bool(row.get("no_species_hbar_or_action_clock"))
    tau_projectable = as_bool(row.get("tau_projectable_through_q"))
    split_respected = as_bool(row.get("clock_phase_traversal_split_respected"))
    measure_blind = as_bool(row.get("species_blind_measure_jacobian"))
    variation = as_bool(row.get("variation_before_readout"))
    hilbert = as_bool(row.get("hilbert_current_same_action"))
    req_route = as_bool(row.get("Req_same_current_route"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    mts_time_phase_ready = time_flow and phase_line and split_respected
    hbar_owner_ready = hbar_unit and quantum_measure and no_species_clock
    matter_phase_ready = same_bundle and measure_blind and variation and hilbert
    tau_owner_ready = tau_projectable
    single_phase_owner_ready = (
        mts_time_phase_ready
        and hbar_owner_ready
        and matter_phase_ready
        and tau_owner_ready
        and req_route
        and source_ok
        and not missing
    )
    delta_w_zero_ready = mts_time_phase_ready and hbar_owner_ready and matter_phase_ready
    claim_ready = single_phase_owner_ready and input_valid and requested_claim

    if claim_ready:
        status = "SINGLE_PHASE_ACTION_OWNER_PARENT_SIGNED"
    elif single_phase_owner_ready:
        status = "SINGLE_PHASE_ACTION_OWNER_CONTRACT_READY_NONCLAIM"
    elif mts_time_phase_ready and not hbar_owner_ready:
        status = "MTS_TIME_PHASE_READY_HBAR_OWNER_OPEN"
    elif mts_time_phase_ready and hbar_owner_ready and not matter_phase_ready:
        status = "TIME_HBAR_READY_MATTER_PHASE_BUNDLE_OPEN"
    elif delta_w_zero_ready and not tau_owner_ready:
        status = "DELTAW_ZERO_ROUTE_READY_TAU_PROJECTABILITY_OPEN"
    elif delta_w_zero_ready and tau_owner_ready and not req_route:
        status = "DELTAW_ZERO_ROUTE_READY_REQ_ROUTE_OPEN"
    elif source_ok:
        status = "SINGLE_PHASE_ACTION_OWNER_BLOCKED"
    else:
        status = "SINGLE_PHASE_ACTION_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("parent_time_flow_unique", time_flow),
        ("phase_action_line_defined", phase_line),
        ("single_hbar_phase_unit", hbar_unit),
        ("universal_quantum_statistical_measure", quantum_measure),
        ("ordinary_matter_same_phase_bundle", same_bundle),
        ("no_species_hbar_or_action_clock", no_species_clock),
        ("tau_projectable_through_q", tau_projectable),
        ("clock_phase_traversal_split_respected", split_respected),
        ("species_blind_measure_jacobian", measure_blind),
        ("variation_before_readout", variation),
        ("hilbert_current_same_action", hilbert),
        ("Req_same_current_route", req_route),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "mts_time_phase_ready": str(mts_time_phase_ready),
        "hbar_owner_ready": str(hbar_owner_ready),
        "matter_phase_ready": str(matter_phase_ready),
        "tau_owner_ready": str(tau_owner_ready),
        "delta_w_zero_ready": str(delta_w_zero_ready),
        "single_phase_owner_ready": str(single_phase_owner_ready),
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
        "comparator_value",
        "units",
        "source_path",
        "official_numeric_source",
        "parent_coefficient_source",
        "projection_source",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    official = as_bool(row.get("official_numeric_source"))
    parent_coeff = as_bool(row.get("parent_coefficient_source"))
    projection = as_bool(row.get("projection_source"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))
    predicted_value = row.get("predicted_value", "")
    comparator_value = row.get("comparator_value", "")
    predicted_numeric = is_number(predicted_value)
    comparator_numeric = is_number(comparator_value)
    schema_ready = source_ok and not missing and (
        predicted_numeric
        or is_schema_value(predicted_value)
    ) and (
        comparator_numeric
        or is_schema_value(comparator_value)
    )
    score_ready = (
        schema_ready
        and predicted_numeric
        and comparator_numeric
        and official
        and parent_coeff
        and projection
        and input_valid
    )
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "FINITE_VALUE_SCORE_READY"
    elif score_ready:
        status = "FINITE_VALUE_SCORE_READY_NONCLAIM"
    elif schema_ready and comparator_numeric and not predicted_numeric:
        status = "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM"
    elif schema_ready:
        status = "FINITE_VALUE_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    elif source_ok:
        status = "FINITE_VALUE_BLOCKED_MISSING_INPUT"
    else:
        status = "FINITE_VALUE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("schema_ready", schema_ready),
        ("predicted_numeric", predicted_numeric),
        ("comparator_numeric", comparator_numeric),
        ("official_numeric_source", official),
        ("parent_coefficient_source", parent_coeff),
        ("projection_source", projection),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "predicted_numeric": str(predicted_numeric),
        "comparator_numeric": str(comparator_numeric),
        "schema_ready": str(schema_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_phase_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_phase_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_value_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_value_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate single-phase action-owner or finite value rows.")
    parser.add_argument("--mode", choices=["phase-owner", "value"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_phase_owner_rows(args.input) if args.mode == "phase-owner" else evaluate_value_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
