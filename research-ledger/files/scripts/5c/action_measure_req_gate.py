from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed"}
SCHEMA_PREFIX = "SCHEMA_"


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
    return text.startswith(SCHEMA_PREFIX) or text.startswith("MISSING_") or text.startswith("BOUND_")


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


def evaluate_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "owner_id",
        "branch",
        "single_parent_action_phase",
        "universal_hbar_parent",
        "common_variational_measure",
        "species_blind_measure_jacobian",
        "variation_before_readout",
        "hilbert_current_from_same_action",
        "ordinary_matter_functor_exhausted",
        "connected_matter_coproduct_or_no_direct_sum_weights",
        "derivative_silence_of_common_mode",
        "no_hidden_source_scalar",
        "same_current_req_route_ready",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    phase = as_bool(row.get("single_parent_action_phase"))
    hbar = as_bool(row.get("universal_hbar_parent"))
    measure = as_bool(row.get("common_variational_measure"))
    jacobian = as_bool(row.get("species_blind_measure_jacobian"))
    variation = as_bool(row.get("variation_before_readout"))
    hilbert = as_bool(row.get("hilbert_current_from_same_action"))
    functor = as_bool(row.get("ordinary_matter_functor_exhausted"))
    connected = as_bool(row.get("connected_matter_coproduct_or_no_direct_sum_weights"))
    derivative_silent = as_bool(row.get("derivative_silence_of_common_mode"))
    no_hidden = as_bool(row.get("no_hidden_source_scalar"))
    req_route = as_bool(row.get("same_current_req_route_ready"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    phase_clock_ready = phase and hbar
    measure_ready = measure and jacobian
    current_owner_ready = variation and hilbert
    species_lock_ready = functor and connected and derivative_silent and no_hidden
    req_ready = req_route
    action_measure_owner_ready = (
        phase_clock_ready
        and measure_ready
        and current_owner_ready
        and species_lock_ready
        and req_ready
        and source_ok
        and not missing
    )
    delta_w_zero_ready = phase_clock_ready and measure_ready and current_owner_ready and species_lock_ready
    local_source_ready = action_measure_owner_ready
    claim_ready = action_measure_owner_ready and input_valid and requested_claim

    if claim_ready:
        status = "ACTION_MEASURE_CURRENT_OWNER_PARENT_SIGNED"
    elif action_measure_owner_ready:
        status = "ACTION_MEASURE_CURRENT_OWNER_CONTRACT_READY_NONCLAIM"
    elif phase and not phase_clock_ready:
        status = "PHASE_OWNER_PRESENT_UNIVERSAL_HBAR_OPEN"
    elif phase_clock_ready and not measure_ready:
        status = "PHASE_CLOCK_READY_MEASURE_OWNER_OPEN"
    elif phase_clock_ready and measure_ready and not species_lock_ready:
        status = "ACTION_MEASURE_READY_FUNCTOR_EXHAUSTION_OPEN"
    elif delta_w_zero_ready and not req_ready:
        status = "DELTAW_ZERO_ROUTE_READY_REQ_ROUTE_OPEN"
    elif source_ok:
        status = "ACTION_MEASURE_CURRENT_OWNER_BLOCKED"
    else:
        status = "ACTION_MEASURE_CURRENT_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("single_parent_action_phase", phase),
        ("universal_hbar_parent", hbar),
        ("common_variational_measure", measure),
        ("species_blind_measure_jacobian", jacobian),
        ("variation_before_readout", variation),
        ("hilbert_current_from_same_action", hilbert),
        ("ordinary_matter_functor_exhausted", functor),
        ("connected_matter_coproduct_or_no_direct_sum_weights", connected),
        ("derivative_silence_of_common_mode", derivative_silent),
        ("no_hidden_source_scalar", no_hidden),
        ("same_current_req_route_ready", req_route),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "phase_clock_ready": str(phase_clock_ready),
        "measure_ready": str(measure_ready),
        "current_owner_ready": str(current_owner_ready),
        "species_lock_ready": str(species_lock_ready),
        "req_ready": str(req_ready),
        "delta_w_zero_ready": str(delta_w_zero_ready),
        "action_measure_owner_ready": str(action_measure_owner_ready),
        "local_source_ready": str(local_source_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_bound_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "bound_id",
        "residual",
        "arena",
        "normal_form",
        "Delta_w_AB",
        "tau_WEP",
        "R_eq_moment",
        "B_zero_flux",
        "source_worldtube_response",
        "material_response",
        "comparator_bound",
        "source_path",
        "no_cancellation_guard",
        "official_numeric_source",
        "parent_coefficient_source",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = source_exists(row)
    no_cancellation = as_bool(row.get("no_cancellation_guard"))
    official_numeric = as_bool(row.get("official_numeric_source"))
    parent_coeff = as_bool(row.get("parent_coefficient_source"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))
    value_fields = [
        "Delta_w_AB",
        "tau_WEP",
        "R_eq_moment",
        "B_zero_flux",
        "source_worldtube_response",
        "material_response",
        "comparator_bound",
    ]
    schema_ready = (
        source_ok
        and no_cancellation
        and not missing
        and all(is_number(row.get(name, "")) or is_schema_value(row.get(name, "")) for name in value_fields)
    )
    values_numeric = all(is_number(row.get(name, "")) for name in value_fields)
    score_ready = schema_ready and values_numeric and official_numeric and parent_coeff and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "ACTION_REQ_BOUND_VALUES_READY"
    elif score_ready:
        status = "ACTION_REQ_BOUND_SCORE_READY_NONCLAIM"
    elif schema_ready:
        status = "ACTION_REQ_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    elif source_ok:
        status = "ACTION_REQ_BOUND_BLOCKED_MISSING_INPUT"
    else:
        status = "ACTION_REQ_BOUND_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("schema_ready", schema_ready),
        ("values_numeric", values_numeric),
        ("no_cancellation_guard", no_cancellation),
        ("official_numeric_source", official_numeric),
        ("parent_coefficient_source", parent_coeff),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "schema_ready": str(schema_ready),
        "values_numeric": str(values_numeric),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_bound_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate action-measure owner or R_eq/Delta_w bound rows.")
    parser.add_argument("--mode", choices=["owner", "bound"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_owner_rows(args.input) if args.mode == "owner" else evaluate_bound_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
