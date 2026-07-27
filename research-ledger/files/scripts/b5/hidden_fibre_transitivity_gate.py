from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


TRUE_VALUES = {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}
MISSING_PREFIXES = ("MISSING_", "PENDING_", "PLACEHOLDER_", "SCHEMA_", "NOT_")


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing_like(value: object) -> bool:
    text = str(value).strip()
    return any(text.startswith(prefix) for prefix in MISSING_PREFIXES)


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


def evaluate_transitivity_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "clause",
        "q_map_defined",
        "vertical_distribution_defined",
        "gauge_action_parent_signed",
        "action_spans_kernel",
        "fibre_connected_regular",
        "invariant_observable_policy",
        "generator_elimination_complete",
        "radiative_readout_closure",
        "source_path",
        "input_valid",
        "valid_for_claim",
    ]
    missing = missing_required(row, required)
    source_ok = path_exists(row.get("source_path"))
    q_map = as_bool(row.get("q_map_defined"))
    vertical = as_bool(row.get("vertical_distribution_defined"))
    gauge_action = as_bool(row.get("gauge_action_parent_signed"))
    spans = as_bool(row.get("action_spans_kernel"))
    connected = as_bool(row.get("fibre_connected_regular"))
    invariant_policy = as_bool(row.get("invariant_observable_policy"))
    generators_killed = as_bool(row.get("generator_elimination_complete"))
    readout_closed = as_bool(row.get("radiative_readout_closure"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))

    fibre_theorem_ready = q_map and vertical and gauge_action and spans and connected and invariant_policy and source_ok and not missing
    invariant_triviality_ready = fibre_theorem_ready and generators_killed and readout_closed
    score_ready = invariant_triviality_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "HIDDEN_FIBRE_TRANSITIVITY_TRIVIALITY_CLAIM_READY"
    elif score_ready:
        status = "HIDDEN_FIBRE_TRANSITIVITY_TRIVIALITY_READY_NONCLAIM"
    elif invariant_triviality_ready:
        status = "HIDDEN_FIBRE_TRIVIALITY_CONTRACT_READY_NONCLAIM"
    elif fibre_theorem_ready and not generators_killed:
        status = "TRANSITIVE_FIBRE_THEOREM_READY_GENERATOR_DEBTS_SURVIVE"
    elif q_map and vertical and not gauge_action:
        status = "VERTICAL_KERNEL_DEFINED_GAUGE_ACTION_UNSIGNED"
    elif gauge_action and not spans:
        status = "GAUGE_ACTION_DECLARED_KERNEL_SPAN_UNSIGNED"
    elif q_map and vertical and generators_killed and not readout_closed:
        status = "GENERATOR_KILL_LIST_READY_READOUT_OPEN"
    elif source_ok:
        status = "TRANSITIVITY_PROOF_PARTIAL"
    else:
        status = "TRANSITIVITY_PROOF_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("q_map_defined", q_map),
        ("vertical_distribution_defined", vertical),
        ("gauge_action_parent_signed", gauge_action),
        ("action_spans_kernel", spans),
        ("fibre_connected_regular", connected),
        ("invariant_observable_policy", invariant_policy),
        ("generator_elimination_complete", generators_killed),
        ("radiative_readout_closure", readout_closed),
        ("input_valid", input_valid),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "fibre_theorem_ready": str(fibre_theorem_ready),
        "invariant_triviality_ready": str(invariant_triviality_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_vector_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    required = [
        "row_id",
        "component",
        "generator",
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
    basis_ok = not is_missing_like(row.get("parent_variation_basis"))
    projection_ok = not is_missing_like(row.get("observable_projection"))
    independent = as_bool(row.get("independent_of_bound"))
    input_valid = as_bool(row.get("input_valid"))
    requested_claim = as_bool(row.get("valid_for_claim"))
    value_ready = (numeric or derived_zero) and source_ok and basis_ok and projection_ok and independent and not missing
    score_ready = value_ready and input_valid
    claim_ready = score_ready and requested_claim

    if claim_ready:
        status = "FINITE_CSOURCE_VECTOR_COMPONENT_CLAIM_READY"
    elif score_ready:
        status = "FINITE_CSOURCE_VECTOR_COMPONENT_SCORE_READY_NONCLAIM"
    elif value_ready:
        status = "FINITE_CSOURCE_VECTOR_COMPONENT_INPUT_INVALID_NONCLAIM"
    elif source_ok:
        status = "FINITE_CSOURCE_VECTOR_COMPONENT_CONTRACT_ONLY"
    else:
        status = "FINITE_CSOURCE_VECTOR_COMPONENT_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("numeric_or_derived_zero", numeric or derived_zero),
        ("parent_variation_basis_declared", basis_ok),
        ("observable_projection_declared", projection_ok),
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


def evaluate_transitivity_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_transitivity_row(row, input_path) for row in read_csv(input_path)]


def evaluate_vector_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_vector_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate hidden-fibre transitivity and finite C_source vector rows.")
    parser.add_argument("--mode", choices=["transitivity", "vector"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_transitivity_rows(args.input) if args.mode == "transitivity" else evaluate_vector_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
