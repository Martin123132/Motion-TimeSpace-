from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


PROJECTOR_REQUIRED_FIELDS = [
    "projector_id",
    "projector_class",
    "variation_axis",
    "pi_descends_through_q_eobs_tau",
    "support_weights_descend",
    "boundary_transport_lc_eobs_or_topology",
    "source_current_silent",
    "no_gamma_ind_transport",
    "no_prevariation_feedback",
    "no_calibration_feedback",
    "metric_stress_separate",
    "flux_closure_separate",
    "parent_policy_signed",
    "source_path",
    "input_valid",
    "valid_for_claim",
    "notes",
]


KERNEL_REQUIRED_FIELDS = [
    "kernel_id",
    "arena",
    "residual_symbol",
    "normal_form",
    "lipschitz_factor",
    "protocol_leak",
    "K_projective",
    "J_norm",
    "comparator_bound",
    "source_path",
    "no_cancellation_guard",
    "official_numeric_source",
    "parent_coefficient_source",
    "input_valid",
    "valid_for_claim",
    "issues",
]


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "passed", "closed", "signed", "zero"}
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


def missing_fields(row: Mapping[str, str], required: Iterable[str]) -> str:
    return ";".join(field for field in required if field not in row or is_missing(row.get(field, "")))


def source_exists(row: Mapping[str, str]) -> bool:
    source = str(row.get("source_path", "")).strip()
    return bool(source) and not source.upper().startswith("MISSING") and Path(source).exists()


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def positive_float(value: object) -> bool:
    numeric = as_float(value)
    return numeric is not None and numeric > 0.0


def evaluate_projector_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, PROJECTOR_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    pi_descends = as_bool(row.get("pi_descends_through_q_eobs_tau"))
    support_descends = as_bool(row.get("support_weights_descend"))
    boundary_descends = as_bool(row.get("boundary_transport_lc_eobs_or_topology"))
    source_current_silent = as_bool(row.get("source_current_silent"))
    no_gamma_transport = as_bool(row.get("no_gamma_ind_transport"))
    no_prevariation_feedback = as_bool(row.get("no_prevariation_feedback"))
    no_calibration_feedback = as_bool(row.get("no_calibration_feedback"))
    metric_stress_separate = as_bool(row.get("metric_stress_separate"))
    flux_closure_separate = as_bool(row.get("flux_closure_separate"))
    parent_policy_signed = as_bool(row.get("parent_policy_signed"))
    input_valid = as_bool(row.get("input_valid"))

    chain_rule_pi_zero = pi_descends and support_descends and boundary_descends and no_gamma_transport
    product_commutator_zero = (
        chain_rule_pi_zero
        and source_current_silent
        and no_prevariation_feedback
        and no_calibration_feedback
    )
    scope_guard_ready = metric_stress_separate and flux_closure_separate
    branch_zero_ready = product_commutator_zero and scope_guard_ready and source_ok and not missing
    public_ready = branch_zero_ready and parent_policy_signed and input_valid
    valid_for_claim = public_ready and as_bool(row.get("valid_for_claim"))

    if missing or not source_ok:
        status = "PROJECTOR_COMMUTATOR_BLOCKED_MISSING_INPUT"
    elif public_ready:
        status = "PROJECTOR_COMMUTATOR_PUBLIC_READY"
    elif branch_zero_ready:
        status = "PROJECTOR_COMMUTATOR_BRANCH_ZERO_NONCLAIM"
    elif chain_rule_pi_zero:
        status = "PROJECTOR_CHAIN_RULE_ZERO_FEEDBACK_OR_SOURCE_OPEN"
    else:
        status = "PROJECTOR_COMMUTATOR_BLOCKED_FEEDBACK_OR_SUPPORT"

    clauses = [
        ("pi_descends_through_q_eobs_tau", pi_descends),
        ("support_weights_descend", support_descends),
        ("boundary_transport_lc_eobs_or_topology", boundary_descends),
        ("source_current_silent", source_current_silent),
        ("no_gamma_ind_transport", no_gamma_transport),
        ("no_prevariation_feedback", no_prevariation_feedback),
        ("no_calibration_feedback", no_calibration_feedback),
        ("metric_stress_separate", metric_stress_separate),
        ("flux_closure_separate", flux_closure_separate),
        ("parent_policy_signed", parent_policy_signed),
        ("input_valid", input_valid),
    ]

    return {
        **{key: str(value) for key, value in row.items()},
        "input_path": str(input_path),
        "missing_fields": missing,
        "source_exists": str(source_ok),
        "chain_rule_pi_zero": str(chain_rule_pi_zero),
        "product_commutator_zero": str(product_commutator_zero),
        "scope_guard_ready": str(scope_guard_ready),
        "branch_zero_ready": str(branch_zero_ready),
        "public_ready": str(public_ready),
        "open_clauses": ";".join(name for name, ok in clauses if not ok),
        "current_status": status,
        "valid_for_claim": str(valid_for_claim),
    }


def evaluate_kernel_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing = missing_fields(row, KERNEL_REQUIRED_FIELDS)
    source_ok = source_exists(row)
    normal_form_ready = not is_missing(row.get("normal_form"))
    lipschitz_ready = positive_float(row.get("lipschitz_factor")) or str(row.get("lipschitz_factor", "")).startswith("SCHEMA_")
    protocol_leak_ready = positive_float(row.get("protocol_leak")) or str(row.get("protocol_leak", "")).startswith("SCHEMA_")
    k_ready = positive_float(row.get("K_projective"))
    j_ready = positive_float(row.get("J_norm"))
    comparator_ready = positive_float(row.get("comparator_bound"))
    no_cancellation = as_bool(row.get("no_cancellation_guard"))
    official_numeric = as_bool(row.get("official_numeric_source"))
    parent_coeff = as_bool(row.get("parent_coefficient_source"))
    input_valid = as_bool(row.get("input_valid"))
    numeric_ready = k_ready and j_ready and comparator_ready
    schema_ready = source_ok and normal_form_ready and lipschitz_ready and protocol_leak_ready and no_cancellation and not missing
    score_ready = schema_ready and numeric_ready and official_numeric and parent_coeff and input_valid
    claim_ready = score_ready and as_bool(row.get("valid_for_claim"))

    if claim_ready:
        status = "KPROJECTIVE_VALUES_READY"
    elif score_ready:
        status = "KPROJECTIVE_SCORE_READY_NONCLAIM"
    elif schema_ready:
        status = "KPROJECTIVE_SCHEMA_READY_VALUES_MISSING_NONCLAIM"
    elif source_ok:
        status = "KPROJECTIVE_BLOCKED_MISSING_PARENT_OR_OFFICIAL_INPUT"
    else:
        status = "KPROJECTIVE_BLOCKED_MISSING_SOURCE"

    blockers = []
    if missing:
        blockers.append(f"missing:{missing}")
    for name, ok in [
        ("source_exists", source_ok),
        ("normal_form", normal_form_ready),
        ("lipschitz_factor", lipschitz_ready),
        ("protocol_leak", protocol_leak_ready),
        ("K_projective", k_ready),
        ("J_norm", j_ready),
        ("comparator_bound", comparator_ready),
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
        "numeric_ready": str(numeric_ready),
        "score_ready": str(score_ready),
        "blockers": ";".join(blockers),
        "current_status": status,
        "valid_for_claim": str(claim_ready),
    }


def evaluate_projector_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_projector_row(row, input_path) for row in read_csv(input_path)]


def evaluate_kernel_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_kernel_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate readout/projector commutator rows or Kprojective fallback rows.")
    parser.add_argument("--mode", choices=["projector", "kernel"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = evaluate_projector_rows(args.input) if args.mode == "projector" else evaluate_kernel_rows(args.input)
    write_csv(args.output, rows)


if __name__ == "__main__":
    main()
