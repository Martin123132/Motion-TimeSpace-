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


def evaluate_hbar_owner_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "single_phase_line",
        "universal_hbar_parent",
        "common_path_measure",
        "species_blind_jacobian",
        "ordinary_same_phase_bundle",
        "no_species_hbar_A",
        "action_density_owner",
        "current_owner",
        "variation_before_readout",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    phase = as_bool(row.get("single_phase_line"))
    hbar = as_bool(row.get("universal_hbar_parent"))
    measure = as_bool(row.get("common_path_measure"))
    jacobian = as_bool(row.get("species_blind_jacobian"))
    same_bundle = as_bool(row.get("ordinary_same_phase_bundle"))
    no_hbar_a = as_bool(row.get("no_species_hbar_A"))
    density = as_bool(row.get("action_density_owner"))
    current = as_bool(row.get("current_owner"))
    variation_order = as_bool(row.get("variation_before_readout"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        phase
        and hbar
        and measure
        and jacobian
        and same_bundle
        and no_hbar_a
        and density
        and current
        and variation_order
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    phase_seed_only = phase and source_ok and not (same_bundle or current or density) and not hbar
    hbar_measure_open = phase and source_ok and (same_bundle or current or density) and (not hbar or not measure or not jacobian)
    owner_ready_graph_open = contract_ready and not input_valid
    partial = source_ok and (phase or current or density)

    if claim_ready:
        status = "HBAR_MEASURE_OWNER_CLAIM_READY"
    elif score_ready:
        status = "HBAR_MEASURE_OWNER_READY_NONCLAIM"
    elif owner_ready_graph_open:
        status = "HBAR_MEASURE_OWNER_CONTRACT_READY_NONCLAIM"
    elif hbar_measure_open:
        status = "HBAR_MEASURE_OWNER_HBAR_MEASURE_JACOBIAN_OPEN"
    elif phase_seed_only:
        status = "HBAR_MEASURE_OWNER_PHASE_SEED_ONLY"
    elif partial:
        status = "HBAR_MEASURE_OWNER_PARTIAL"
    elif source_ok:
        status = "HBAR_MEASURE_OWNER_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "HBAR_MEASURE_OWNER_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("single_phase_line", phase),
        ("universal_hbar_parent", hbar),
        ("common_path_measure", measure),
        ("species_blind_jacobian", jacobian),
        ("ordinary_same_phase_bundle", same_bundle),
        ("no_species_hbar_A", no_hbar_a),
        ("action_density_owner", density),
        ("current_owner", current),
        ("variation_before_readout", variation_order),
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


def evaluate_connected_graph_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "nodes_declared",
        "template_connected",
        "parent_owned_edges",
        "nonzero_morphisms",
        "action_density_functor_owned",
        "source_label_forgetting",
        "material_projection_sourced",
        "decoupled_inventory_closed",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    nodes = as_bool(row.get("nodes_declared"))
    template = as_bool(row.get("template_connected"))
    parent_edges = as_bool(row.get("parent_owned_edges"))
    morphisms = as_bool(row.get("nonzero_morphisms"))
    functor = as_bool(row.get("action_density_functor_owned"))
    label_forgetting = as_bool(row.get("source_label_forgetting"))
    material = as_bool(row.get("material_projection_sourced"))
    inventory = as_bool(row.get("decoupled_inventory_closed"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = (
        nodes
        and template
        and parent_edges
        and morphisms
        and functor
        and label_forgetting
        and material
        and inventory
        and source_ok
        and not missing
    )
    score_ready = contract_ready and input_valid
    claim_ready = score_ready and requested_claim
    template_only = source_ok and nodes and template and not parent_edges
    parent_edge_gap = source_ok and nodes and template and not (parent_edges and morphisms and functor)
    material_gap = source_ok and nodes and template and parent_edges and morphisms and functor and not material
    decoupled_gap = source_ok and nodes and template and parent_edges and morphisms and functor and material and not inventory
    partial = source_ok and (nodes or template or label_forgetting)

    if claim_ready:
        status = "CONNECTED_GRAPH_CERTIFICATE_CLAIM_READY"
    elif score_ready:
        status = "CONNECTED_GRAPH_CERTIFICATE_READY_NONCLAIM"
    elif contract_ready:
        status = "CONNECTED_GRAPH_CERTIFICATE_CONTRACT_READY_NONCLAIM"
    elif material_gap:
        status = "CONNECTED_GRAPH_CERTIFICATE_MATERIAL_PROJECTION_MISSING"
    elif decoupled_gap:
        status = "CONNECTED_GRAPH_CERTIFICATE_DECOUPLED_INVENTORY_MISSING"
    elif parent_edge_gap:
        status = "CONNECTED_GRAPH_CERTIFICATE_PARENT_EDGES_MISSING"
    elif template_only:
        status = "CONNECTED_GRAPH_CERTIFICATE_PHYSICAL_TEMPLATE_ONLY"
    elif partial:
        status = "CONNECTED_GRAPH_CERTIFICATE_PARTIAL"
    elif source_ok:
        status = "CONNECTED_GRAPH_CERTIFICATE_SOURCE_PRESENT_CLAUSES_OPEN"
    else:
        status = "CONNECTED_GRAPH_CERTIFICATE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("nodes_declared", nodes),
        ("template_connected", template),
        ("parent_owned_edges", parent_edges),
        ("nonzero_morphisms", morphisms),
        ("action_density_functor_owned", functor),
        ("source_label_forgetting", label_forgetting),
        ("material_projection_sourced", material),
        ("decoupled_inventory_closed", inventory),
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


def evaluate_k_action_value_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "product",
        "value",
        "units",
        "parent_coefficient_source",
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
    numeric = is_number(value)
    derived_zero = value.upper() == "DERIVED_ZERO"
    bound_only = value.upper().startswith("BOUND_ONLY")
    common = value.upper() == "COMMON_CALIBRATION_ONLY"
    units_ok = not is_missing_like(row.get("units"))
    parent_ok = not is_missing_like(row.get("parent_coefficient_source"))
    leg_ok = not is_missing_like(row.get("source_leg"))
    projection_ok = not is_missing_like(row.get("projection"))
    bound_ok = is_number(row.get("bound_value"))
    guard = as_bool(row.get("no_bound_inversion_guard"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    contract_ready = source_ok and units_ok and projection_ok and bound_ok and guard and not missing
    numeric_ready = contract_ready and (numeric or derived_zero or common) and parent_ok and leg_ok
    score_ready = numeric_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "K_ACTION_VALUE_CLAIM_READY"
    elif score_ready:
        status = "K_ACTION_VALUE_READY_NONCLAIM"
    elif numeric_ready:
        status = "K_ACTION_VALUE_INPUT_INVALID_NONCLAIM"
    elif bound_only and contract_ready:
        status = "K_ACTION_VALUE_BOUND_TARGET_ONLY"
    elif contract_ready:
        status = "K_ACTION_VALUE_CONTRACT_ONLY"
    elif source_ok:
        status = "K_ACTION_VALUE_PARTIAL"
    else:
        status = "K_ACTION_VALUE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_zero_or_common_value", numeric or derived_zero or common),
        ("units", units_ok),
        ("parent_coefficient_source", parent_ok),
        ("source_leg", leg_ok),
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


def evaluate_hbar_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_hbar_owner_row(row, input_path) for row in read_csv(input_path)]


def evaluate_connected_graph_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_connected_graph_row(row, input_path) for row in read_csv(input_path)]


def evaluate_k_action_value_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_k_action_value_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate 4434 hbar/measure owner and connected graph rows.")
    parser.add_argument("--kind", choices=["hbar", "graph", "kvalue"], required=True)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if args.kind == "hbar":
        rows = evaluate_hbar_owner_rows(args.input)
    elif args.kind == "graph":
        rows = evaluate_connected_graph_rows(args.input)
    else:
        rows = evaluate_k_action_value_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
