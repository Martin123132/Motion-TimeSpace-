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


def evaluate_signature_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "signature_piece",
        "one_total_matter_action",
        "total_hilbert_derivative",
        "source_domain_total_current",
        "no_source_shadow",
        "no_species_hom",
        "no_hidden_marker_return",
        "nonhilbert_bypass_zero",
        "exchange_connected_or_common",
        "common_calibration_removed",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    total_action = as_bool(row.get("one_total_matter_action"))
    hilbert = as_bool(row.get("total_hilbert_derivative"))
    domain = as_bool(row.get("source_domain_total_current"))
    shadow = as_bool(row.get("no_source_shadow"))
    no_species_hom = as_bool(row.get("no_species_hom"))
    no_hidden = as_bool(row.get("no_hidden_marker_return"))
    no_nonhilbert = as_bool(row.get("nonhilbert_bypass_zero"))
    exchange = as_bool(row.get("exchange_connected_or_common"))
    calibration = as_bool(row.get("common_calibration_removed"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        total_action
        and hilbert
        and domain
        and shadow
        and no_species_hom
        and no_hidden
        and no_nonhilbert
        and exchange
        and calibration
        and source_ok
        and not missing
    )
    partial_owner = total_action and hilbert and domain and exchange and calibration and source_ok
    no_weight_core = total_action and hilbert and shadow and exchange and calibration and source_ok
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "SOURCE_OWNER_SIGNATURE_CLAIM_READY"
    elif score_ready:
        status = "SOURCE_OWNER_SIGNATURE_READY_NONCLAIM"
    elif contract_ready:
        status = "SOURCE_OWNER_SIGNATURE_CONTRACT_READY_NONCLAIM"
    elif partial_owner and no_weight_core and not no_hidden and not no_nonhilbert:
        status = "SOURCE_OWNER_SIGNATURE_REDUCES_TO_HIDDEN_NONHILBERT_RETURNS"
    elif partial_owner and not shadow:
        status = "TOTAL_HILBERT_OWNER_SOURCE_SHADOW_OPEN"
    elif no_weight_core:
        status = "NO_SOURCE_WEIGHT_CORE_READY_MARKER_NONHILBERT_OPEN"
    elif partial_owner:
        status = "TOTAL_HILBERT_OWNER_PARTIAL"
    elif source_ok:
        status = "SOURCE_OWNER_SIGNATURE_BLOCKED_CURRENT_CORPUS"
    else:
        status = "SOURCE_OWNER_SIGNATURE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("one_total_matter_action", total_action),
        ("total_hilbert_derivative", hilbert),
        ("source_domain_total_current", domain),
        ("no_source_shadow", shadow),
        ("no_species_hom", no_species_hom),
        ("no_hidden_marker_return", no_hidden),
        ("nonhilbert_bypass_zero", no_nonhilbert),
        ("exchange_connected_or_common", exchange),
        ("common_calibration_removed", calibration),
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
        "partial_owner": str(partial_owner),
        "no_weight_core": str(no_weight_core),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_dd_map_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "dd_quantity",
        "map_formula",
        "material_delta_Q",
        "coefficient_values_present",
        "source_leg_present",
        "alloy_policy_present",
        "sign_policy_present",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    delta_ok = not is_missing_like(row.get("material_delta_Q"))
    values = as_bool(row.get("coefficient_values_present"))
    source_leg = as_bool(row.get("source_leg_present"))
    alloy = as_bool(row.get("alloy_policy_present"))
    sign = as_bool(row.get("sign_policy_present"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    symbolic_ready = source_ok and delta_ok and not missing
    numeric_ready = symbolic_ready and values and source_leg and alloy and sign
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "DD_MAP_CLAIM_READY"
    elif score_ready:
        status = "DD_MAP_READY_NONCLAIM"
    elif numeric_ready:
        status = "DD_MAP_INPUT_INVALID_NONCLAIM"
    elif symbolic_ready and not values:
        status = "DD_SYMBOLIC_MAP_READY_VALUES_MISSING"
    elif symbolic_ready:
        status = "DD_MAP_PARTIAL_SOURCE_LEG_OR_POLICY_MISSING"
    elif source_ok:
        status = "DD_MAP_CONTRACT_ONLY"
    else:
        status = "DD_MAP_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("material_delta_Q_declared", delta_ok),
        ("coefficient_values_present", values),
        ("source_leg_present", source_leg),
        ("alloy_policy_present", alloy),
        ("sign_policy_present", sign),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "symbolic_ready": str(symbolic_ready),
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_envelope_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "envelope",
        "bound_value",
        "units",
        "source_path",
        "numeric_bound_present",
        "theory_values_present",
        "no_cancellation_policy",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    numeric_bound = as_bool(row.get("numeric_bound_present")) and is_number(row.get("bound_value"))
    theory_values = as_bool(row.get("theory_values_present"))
    no_cancel = as_bool(row.get("no_cancellation_policy"))
    units_ok = not is_missing_like(row.get("units"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    target_ready = source_ok and numeric_bound and units_ok and no_cancel and not missing
    score_ready = target_ready and theory_values and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "DD_ENVELOPE_CLAIM_READY"
    elif score_ready:
        status = "DD_ENVELOPE_SCORE_READY_NONCLAIM"
    elif target_ready and not theory_values:
        status = "DD_ENVELOPE_TARGET_READY_THEORY_VALUES_MISSING"
    elif source_ok:
        status = "DD_ENVELOPE_PARTIAL"
    else:
        status = "DD_ENVELOPE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_bound_present", numeric_bound),
        ("units_declared", units_ok),
        ("no_cancellation_policy", no_cancel),
        ("theory_values_present", theory_values),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "target_ready": str(target_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_signature_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_signature_row(row, input_path) for row in read_csv(input_path)]


def evaluate_dd_map_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_dd_map_row(row, input_path) for row in read_csv(input_path)]


def evaluate_envelope_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_envelope_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate total-Hilbert source signature and DD source maps.")
    parser.add_argument("--signature-input", type=Path)
    parser.add_argument("--signature-output", type=Path)
    parser.add_argument("--dd-input", type=Path)
    parser.add_argument("--dd-output", type=Path)
    parser.add_argument("--envelope-input", type=Path)
    parser.add_argument("--envelope-output", type=Path)
    args = parser.parse_args()

    if args.signature_input and args.signature_output:
        write_csv(args.signature_output, evaluate_signature_rows(args.signature_input))
    if args.dd_input and args.dd_output:
        write_csv(args.dd_output, evaluate_dd_map_rows(args.dd_input))
    if args.envelope_input and args.envelope_output:
        write_csv(args.envelope_output, evaluate_envelope_rows(args.envelope_input))


if __name__ == "__main__":
    main()
