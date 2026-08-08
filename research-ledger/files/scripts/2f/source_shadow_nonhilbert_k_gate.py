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


def evaluate_shadow_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "single_parent_action",
        "no_independent_source_functional",
        "no_weighted_duplicate_action",
        "constructor_no_hom",
        "exchange_graph_connected",
        "hidden_readout_no_return",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    single_action = as_bool(row.get("single_parent_action"))
    no_independent = as_bool(row.get("no_independent_source_functional"))
    no_weighted = as_bool(row.get("no_weighted_duplicate_action"))
    no_hom = as_bool(row.get("constructor_no_hom"))
    exchange = as_bool(row.get("exchange_graph_connected"))
    no_return = as_bool(row.get("hidden_readout_no_return"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        single_action
        and no_independent
        and no_weighted
        and no_hom
        and exchange
        and no_return
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    countermodel_survives = source_ok and (not no_independent or not no_weighted)
    reduces_to_return = single_action and no_independent and no_weighted and exchange and source_ok and (not no_hom or not no_return)
    partial = source_ok and (single_action or no_independent or no_weighted or exchange)

    if claim_ready:
        status = "SOURCE_SHADOW_BAN_CLAIM_READY"
    elif score_ready:
        status = "SOURCE_SHADOW_BAN_READY_NONCLAIM"
    elif contract_ready:
        status = "SOURCE_SHADOW_BAN_CONTRACT_READY_NONCLAIM"
    elif reduces_to_return:
        status = "SOURCE_SHADOW_REDUCES_TO_BLOCK_AND_HIDDEN_RETURN"
    elif countermodel_survives:
        status = "SOURCE_SHADOW_COUNTERMODEL_SURVIVES"
    elif partial:
        status = "SOURCE_SHADOW_PARTIAL"
    elif source_ok:
        status = "SOURCE_SHADOW_BAN_CONTRACT_ONLY"
    else:
        status = "SOURCE_SHADOW_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("single_parent_action", single_action),
        ("no_independent_source_functional", no_independent),
        ("no_weighted_duplicate_action", no_weighted),
        ("constructor_no_hom", no_hom),
        ("exchange_graph_connected", exchange),
        ("hidden_readout_no_return", no_return),
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


def evaluate_nonhilbert_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "total_noether_identity",
        "hilbert_current_owner",
        "spin_boundary_improvement_owned",
        "readout_projector_after_variation",
        "J_NH_decomposition_declared",
        "J_NH_zero_or_exact_divergence",
        "compact_flux_zero",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    total_noether = as_bool(row.get("total_noether_identity"))
    hilbert_owner = as_bool(row.get("hilbert_current_owner"))
    spin_boundary = as_bool(row.get("spin_boundary_improvement_owned"))
    readout_after = as_bool(row.get("readout_projector_after_variation"))
    decomposition = as_bool(row.get("J_NH_decomposition_declared"))
    zero_or_divergence = as_bool(row.get("J_NH_zero_or_exact_divergence"))
    compact_flux = as_bool(row.get("compact_flux_zero"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        total_noether
        and hilbert_owner
        and spin_boundary
        and readout_after
        and decomposition
        and zero_or_divergence
        and compact_flux
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    exact_divergence_open = total_noether and hilbert_owner and decomposition and zero_or_divergence and source_ok and not compact_flux
    residual_retained = total_noether and hilbert_owner and decomposition and source_ok and not zero_or_divergence
    partial = source_ok and (total_noether or hilbert_owner or decomposition)

    if claim_ready:
        status = "NONHILBERT_BYPASS_ZERO_CLAIM_READY"
    elif score_ready:
        status = "NONHILBERT_BYPASS_ZERO_READY_NONCLAIM"
    elif contract_ready:
        status = "NONHILBERT_BYPASS_ZERO_CONTRACT_READY_NONCLAIM"
    elif exact_divergence_open:
        status = "NONHILBERT_EXACT_DIVERGENCE_BOUNDARY_OPEN"
    elif residual_retained:
        status = "NONHILBERT_RESIDUAL_ROW_RETAINED"
    elif partial:
        status = "NONHILBERT_PARTIAL"
    elif source_ok:
        status = "NONHILBERT_BYPASS_ZERO_CONTRACT_ONLY"
    else:
        status = "NONHILBERT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("total_noether_identity", total_noether),
        ("hilbert_current_owner", hilbert_owner),
        ("spin_boundary_improvement_owned", spin_boundary),
        ("readout_projector_after_variation", readout_after),
        ("J_NH_decomposition_declared", decomposition),
        ("J_NH_zero_or_exact_divergence", zero_or_divergence),
        ("compact_flux_zero", compact_flux),
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


def evaluate_kproduct_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "product",
        "dd_channel",
        "value",
        "units",
        "parent_coefficient_source",
        "K_source",
        "source_leg",
        "projection_formula",
        "bound_value",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    value = str(row.get("value", "")).strip()
    value_numeric = is_number(value)
    derived_zero = value.upper() == "DERIVED_ZERO"
    bound_only = value.upper().startswith("BOUND_ONLY")
    units_ok = not is_missing_like(row.get("units"))
    parent_source_ok = not is_missing_like(row.get("parent_coefficient_source"))
    k_source_ok = not is_missing_like(row.get("K_source"))
    source_leg_ok = not is_missing_like(row.get("source_leg"))
    projection_ok = not is_missing_like(row.get("projection_formula"))
    bound_ok = is_number(row.get("bound_value"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_base = source_ok and units_ok and projection_ok and bound_ok and not missing
    numeric_ready = contract_base and (value_numeric or derived_zero) and parent_source_ok and k_source_ok and source_leg_ok
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "DD_K_PRODUCT_CLAIM_READY"
    elif score_ready:
        status = "DD_K_PRODUCT_READY_NONCLAIM"
    elif numeric_ready:
        status = "DD_K_PRODUCT_INPUT_INVALID_NONCLAIM"
    elif bound_only and contract_base:
        status = "DD_K_PRODUCT_BOUND_TARGET_ONLY"
    elif contract_base:
        status = "DD_K_PRODUCT_CONTRACT_ONLY"
    elif source_ok:
        status = "DD_K_PRODUCT_PARTIAL"
    else:
        status = "DD_K_PRODUCT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_derived_zero_value", value_numeric or derived_zero),
        ("units", units_ok),
        ("parent_coefficient_source", parent_source_ok),
        ("K_source", k_source_ok),
        ("source_leg", source_leg_ok),
        ("projection_formula", projection_ok),
        ("bound_value_numeric", bound_ok),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "contract_base": str(contract_base),
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_shadow_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_shadow_row(row, input_path) for row in read_csv(input_path)]


def evaluate_nonhilbert_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_nonhilbert_row(row, input_path) for row in read_csv(input_path)]


def evaluate_kproduct_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_kproduct_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4431 source-shadow/non-Hilbert/K-product rows.")
    parser.add_argument("--kind", choices=["shadow", "nonhilbert", "kproduct"], required=True)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.kind == "shadow":
        rows = evaluate_shadow_rows(args.input)
    elif args.kind == "nonhilbert":
        rows = evaluate_nonhilbert_rows(args.input)
    else:
        rows = evaluate_kproduct_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
