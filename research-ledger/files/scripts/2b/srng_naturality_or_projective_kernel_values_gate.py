from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


NATURALITY_REQUIRED_FIELDS = [
    "row_id",
    "branch",
    "q_fixed_before_readout",
    "eobs_descends_from_q",
    "action_varied_before_readout",
    "readouts_maps_on_solutions",
    "apparatus_backreaction_in_matter_or_residual",
    "source_current_descends",
    "projector_support_descends",
    "no_gamma_ind_readout_slot",
    "no_projective_trace_readout_slot",
    "same_tau_worldtube_support",
    "boundary_improvement_separate",
    "parent_observation_policy_signed",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "notes",
]


KERNEL_REQUIRED_FIELDS = [
    "kernel_id",
    "residual_component",
    "arena",
    "observable",
    "K_trace",
    "K_trace_units",
    "P_projective",
    "P_projective_units",
    "J_trace_norm",
    "support_certificate",
    "comparator_bound",
    "source_path",
    "no_cancellation_guard",
    "official_numeric_source",
    "parent_coefficient_source",
    "input_valid",
    "valid_for_claim",
    "issues",
]


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "passed", "closed", "signed"}
MISSING_MARKERS = {"", "missing", "missing_*", "none", "null", "na", "n/a", "tbd", "unknown"}


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in materialized:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(materialized)


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def is_missing(value: object) -> bool:
    stripped = str(value).strip()
    return stripped.lower() in MISSING_MARKERS or stripped.upper().startswith("MISSING")


def source_exists(row: Mapping[str, str]) -> bool:
    source = str(row.get("source_path", "")).strip()
    return bool(source) and not source.upper().startswith("MISSING") and Path(source).exists()


def missing_fields(row: Mapping[str, str], required: Iterable[str]) -> str:
    missing = [field for field in required if field not in row or is_missing(row.get(field, ""))]
    return ";".join(missing)


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def positive_float(value: object) -> bool:
    numeric = as_float(value)
    return numeric is not None and numeric > 0.0


def evaluate_naturality_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, NATURALITY_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    q_fixed_before_readout = as_bool(row.get("q_fixed_before_readout"))
    eobs_descends_from_q = as_bool(row.get("eobs_descends_from_q"))
    action_varied_before_readout = as_bool(row.get("action_varied_before_readout"))
    readouts_maps_on_solutions = as_bool(row.get("readouts_maps_on_solutions"))
    apparatus_backreaction_in_matter_or_residual = as_bool(row.get("apparatus_backreaction_in_matter_or_residual"))
    source_current_descends = as_bool(row.get("source_current_descends"))
    projector_support_descends = as_bool(row.get("projector_support_descends"))
    no_gamma_ind_readout_slot = as_bool(row.get("no_gamma_ind_readout_slot"))
    no_projective_trace_readout_slot = as_bool(row.get("no_projective_trace_readout_slot"))
    same_tau_worldtube_support = as_bool(row.get("same_tau_worldtube_support"))
    boundary_improvement_separate = as_bool(row.get("boundary_improvement_separate"))
    parent_observation_policy_signed = as_bool(row.get("parent_observation_policy_signed"))
    input_valid = as_bool(row.get("input_valid"))

    chain_rule_ready = (
        q_fixed_before_readout
        and eobs_descends_from_q
        and action_varied_before_readout
        and readouts_maps_on_solutions
        and no_gamma_ind_readout_slot
    )
    source_term_ready = (
        source_current_descends
        and same_tau_worldtube_support
        and apparatus_backreaction_in_matter_or_residual
    )
    commutator_ready = projector_support_descends
    projective_readout_ready = no_projective_trace_readout_slot
    private_srng_ready = chain_rule_ready and source_term_ready and boundary_improvement_separate
    public_srng_ready = (
        private_srng_ready
        and commutator_ready
        and projective_readout_ready
        and parent_observation_policy_signed
        and source_ok
        and input_valid
        and not missing
    )
    contract_ready_nonclaim = (
        private_srng_ready
        and commutator_ready
        and projective_readout_ready
        and parent_observation_policy_signed
        and source_ok
        and not missing
        and not input_valid
    )

    if missing or not source_ok:
        status = "SRNG_NATURALITY_BLOCKED_MISSING_INPUT"
    elif public_srng_ready:
        status = "SRNG_NATURALITY_PUBLIC_READY"
    elif contract_ready_nonclaim:
        status = "SRNG_NATURALITY_CONTRACT_READY_NONCLAIM"
    elif private_srng_ready:
        status = "SRNG_NATURALITY_PRIVATE_BRANCH_READY_COMMUTATOR_OR_PARENT_OPEN"
    elif chain_rule_ready:
        status = "SRNG_NATURALITY_CHAIN_RULE_READY_SOURCE_OR_PROJECTOR_OPEN"
    else:
        status = "SRNG_NATURALITY_BLOCKED"

    clauses = [
        ("q_fixed_before_readout", q_fixed_before_readout),
        ("eobs_descends_from_q", eobs_descends_from_q),
        ("action_varied_before_readout", action_varied_before_readout),
        ("readouts_maps_on_solutions", readouts_maps_on_solutions),
        ("apparatus_backreaction_in_matter_or_residual", apparatus_backreaction_in_matter_or_residual),
        ("source_current_descends", source_current_descends),
        ("projector_support_descends", projector_support_descends),
        ("no_gamma_ind_readout_slot", no_gamma_ind_readout_slot),
        ("no_projective_trace_readout_slot", no_projective_trace_readout_slot),
        ("same_tau_worldtube_support", same_tau_worldtube_support),
        ("boundary_improvement_separate", boundary_improvement_separate),
        ("parent_observation_policy_signed", parent_observation_policy_signed),
        ("input_valid", input_valid),
    ]

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "chain_rule_ready": str(chain_rule_ready),
        "source_term_ready": str(source_term_ready),
        "commutator_ready": str(commutator_ready),
        "projective_readout_ready": str(projective_readout_ready),
        "private_srng_ready": str(private_srng_ready),
        "public_srng_ready": str(public_srng_ready),
        "open_clauses": ";".join(name for name, ok in clauses if not ok),
        "current_status": status,
        "valid_for_claim": str(public_srng_ready and as_bool(row.get("valid_for_claim"))),
    }


def evaluate_kernel_value_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, KERNEL_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    k_trace_ready = positive_float(row.get("K_trace"))
    p_projective_ready = positive_float(row.get("P_projective"))
    j_trace_ready = positive_float(row.get("J_trace_norm"))
    comparator_ready = positive_float(row.get("comparator_bound"))
    support_ready = not is_missing(row.get("support_certificate"))
    no_cancellation_guard = as_bool(row.get("no_cancellation_guard"))
    official_numeric_source = as_bool(row.get("official_numeric_source"))
    parent_coefficient_source = as_bool(row.get("parent_coefficient_source"))
    input_valid = as_bool(row.get("input_valid"))
    numeric_ready = k_trace_ready and p_projective_ready and j_trace_ready and comparator_ready
    score_ready = (
        numeric_ready
        and support_ready
        and source_ok
        and no_cancellation_guard
        and official_numeric_source
        and parent_coefficient_source
        and input_valid
        and not missing
    )
    claim_ready = score_ready and as_bool(row.get("valid_for_claim"))

    if claim_ready:
        status = "PROJECTIVE_KERNEL_VALUES_READY"
    elif score_ready:
        status = "PROJECTIVE_KERNEL_VALUES_SCORE_READY_NONCLAIM"
    elif source_ok:
        status = "PROJECTIVE_KERNEL_VALUES_BLOCKED_MISSING_PARENT_OR_OFFICIAL_INPUT"
    else:
        status = "PROJECTIVE_KERNEL_VALUES_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("K_trace", k_trace_ready),
        ("P_projective", p_projective_ready),
        ("J_trace_norm", j_trace_ready),
        ("comparator_bound", comparator_ready),
        ("support_certificate", support_ready),
        ("no_cancellation_guard", no_cancellation_guard),
        ("official_numeric_source", official_numeric_source),
        ("parent_coefficient_source", parent_coefficient_source),
        ("input_valid", input_valid),
        ("source_exists", source_ok),
    ]:
        if not ok:
            blockers.append(name)

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "numeric_ready": str(numeric_ready),
        "support_ready": str(support_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_naturality_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_naturality_row(row, input_path) for row in read_csv(input_path)]


def evaluate_kernel_value_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_kernel_value_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate SRNG naturality rows or projective source/readout kernel values.")
    parser.add_argument("--mode", choices=["naturality", "kernel"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_naturality_rows(args.input) if args.mode == "naturality" else evaluate_kernel_value_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
