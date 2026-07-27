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


def evaluate_action_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "one_parent_action_object",
        "universal_hbar_parent",
        "common_measure_jacobian",
        "species_blind_action_density",
        "hilbert_current_owner",
        "ordinary_matter_connected",
        "variation_before_readout",
        "common_mode_calibrated",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    one_parent = as_bool(row.get("one_parent_action_object"))
    hbar = as_bool(row.get("universal_hbar_parent"))
    measure = as_bool(row.get("common_measure_jacobian"))
    species_blind = as_bool(row.get("species_blind_action_density"))
    hilbert = as_bool(row.get("hilbert_current_owner"))
    connected = as_bool(row.get("ordinary_matter_connected"))
    variation_order = as_bool(row.get("variation_before_readout"))
    common_mode = as_bool(row.get("common_mode_calibrated"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        one_parent
        and hbar
        and measure
        and species_blind
        and hilbert
        and connected
        and variation_order
        and common_mode
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    common_mode_route = hilbert and connected and common_mode and source_ok and not hbar
    hbar_measure_gap = one_parent and hilbert and common_mode and source_ok and (not hbar or not measure)
    countermodel_survives = source_ok and (not one_parent or not species_blind or not variation_order)
    partial = source_ok and (one_parent or hilbert or connected or common_mode)

    if claim_ready:
        status = "ACTION_SCALE_OWNER_CLAIM_READY"
    elif score_ready:
        status = "ACTION_SCALE_OWNER_READY_NONCLAIM"
    elif contract_ready:
        status = "ACTION_SCALE_OWNER_CONTRACT_READY_NONCLAIM"
    elif common_mode_route:
        status = "ACTION_SCALE_OWNER_REDUCES_TO_COMMON_MODE_PLUS_HBAR_MEASURE_GAP"
    elif hbar_measure_gap:
        status = "ACTION_SCALE_OWNER_CURRENT_GAP_HBAR_MEASURE_OPEN"
    elif countermodel_survives:
        status = "ACTION_SCALE_OWNER_COUNTERMODEL_SURVIVES"
    elif partial:
        status = "ACTION_SCALE_OWNER_PARTIAL"
    elif source_ok:
        status = "ACTION_SCALE_OWNER_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "ACTION_SCALE_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("one_parent_action_object", one_parent),
        ("universal_hbar_parent", hbar),
        ("common_measure_jacobian", measure),
        ("species_blind_action_density", species_blind),
        ("hilbert_current_owner", hilbert),
        ("ordinary_matter_connected", connected),
        ("variation_before_readout", variation_order),
        ("common_mode_calibrated", common_mode),
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


def evaluate_action_mode_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "mode",
        "definition",
        "all_species_same",
        "derivative_silent",
        "relative_component_zero",
        "absorbed_in_G_calibration",
        "observable_residual",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    same = as_bool(row.get("all_species_same"))
    silent = as_bool(row.get("derivative_silent"))
    relative_zero = as_bool(row.get("relative_component_zero"))
    absorbed = as_bool(row.get("absorbed_in_G_calibration"))
    observable = as_bool(row.get("observable_residual"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    calibration_only = source_ok and same and silent and relative_zero and absorbed and not observable and not missing
    relative_retained = source_ok and (not same or not relative_zero or observable)
    derivative_open = source_ok and same and not silent
    score_ready = calibration_only and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "ACTION_SCALE_COMMON_MODE_CLAIM_READY"
    elif score_ready:
        status = "ACTION_SCALE_COMMON_MODE_READY_NONCLAIM"
    elif calibration_only:
        status = "ACTION_SCALE_COMMON_MODE_CALIBRATION_ONLY_NONCLAIM"
    elif derivative_open:
        status = "ACTION_SCALE_MODE_DERIVATIVE_OPEN"
    elif relative_retained:
        status = "ACTION_SCALE_RELATIVE_MODE_RETAINED"
    elif source_ok:
        status = "ACTION_SCALE_MODE_PARTIAL"
    else:
        status = "ACTION_SCALE_MODE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    if not source_ok:
        blockers.append("source_exists")
    if not same:
        blockers.append("all_species_same")
    if not silent:
        blockers.append("derivative_silent")
    if not relative_zero:
        blockers.append("relative_component_zero")
    if not absorbed:
        blockers.append("absorbed_in_G_calibration")
    if observable:
        blockers.append("observable_residual")
    if not input_valid:
        blockers.append("input_valid")

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "calibration_only": str(calibration_only),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_k_action_scale_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "product",
        "subcomponent",
        "value",
        "units",
        "parent_source",
        "source_leg",
        "projection",
        "bound_value",
        "no_bound_inversion_guard",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    value = str(row.get("value", "")).strip()
    numeric_value = is_number(value)
    derived_zero = value.upper() == "DERIVED_ZERO"
    common_calibration = value.upper() == "COMMON_CALIBRATION_ONLY"
    bound_only = value.upper().startswith("BOUND_ONLY")
    units_ok = not is_missing_like(row.get("units"))
    parent_ok = not is_missing_like(row.get("parent_source"))
    source_leg_ok = not is_missing_like(row.get("source_leg"))
    projection_ok = not is_missing_like(row.get("projection"))
    bound_ok = is_number(row.get("bound_value"))
    guard = as_bool(row.get("no_bound_inversion_guard"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = source_ok and units_ok and projection_ok and bound_ok and guard and not missing
    numeric_ready = contract_ready and (numeric_value or derived_zero or common_calibration) and parent_ok and source_leg_ok
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "K_ACTION_SCALE_PRODUCT_CLAIM_READY"
    elif score_ready:
        status = "K_ACTION_SCALE_PRODUCT_READY_NONCLAIM"
    elif numeric_ready:
        status = "K_ACTION_SCALE_PRODUCT_INPUT_INVALID_NONCLAIM"
    elif bound_only and contract_ready:
        status = "K_ACTION_SCALE_PRODUCT_BOUND_TARGET_ONLY"
    elif contract_ready:
        status = "K_ACTION_SCALE_PRODUCT_CONTRACT_ONLY"
    elif source_ok:
        status = "K_ACTION_SCALE_PRODUCT_PARTIAL"
    else:
        status = "K_ACTION_SCALE_PRODUCT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_zero_or_common_calibration_value", numeric_value or derived_zero or common_calibration),
        ("units", units_ok),
        ("parent_source", parent_ok),
        ("source_leg", source_leg_ok),
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


def evaluate_action_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_action_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_action_mode_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_action_mode_row(row, input_path) for row in read_csv(input_path)]


def evaluate_k_action_scale_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_k_action_scale_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4433 action-scale/constant-sector rows.")
    parser.add_argument("--kind", choices=["owner", "mode", "kproduct"], required=True)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.kind == "owner":
        rows = evaluate_action_owner_rows(args.input)
    elif args.kind == "mode":
        rows = evaluate_action_mode_rows(args.input)
    else:
        rows = evaluate_k_action_scale_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
