from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


SIGNATURE_REQUIRED_FIELDS = [
    "signature_id",
    "branch",
    "ordinary_matter_factors_through_e_obs",
    "spin_connection_is_omega_LC",
    "no_Gamma_ind_argument",
    "no_contorsion_argument",
    "no_hypermomentum_source",
    "EM_Hilbert_no_affine_source",
    "clocks_light_orbits_downstream_metric",
    "projective_trace_guard",
    "boundary_readout_no_torsion_current",
    "same_tau_coframe_support",
    "counterbranch_excluded",
    "parent_selector_signed",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

SIGNATURE_BOOLEAN_FIELDS = [
    field
    for field in SIGNATURE_REQUIRED_FIELDS
    if field not in {"signature_id", "branch", "source_path", "notes"}
]

P4_REQUIRED_FIELDS = [
    "row_id",
    "p4_component",
    "p4_channel",
    "uu_abs",
    "trace_abs",
    "units",
    "projection_matrix",
    "arena_targets",
    "source_path",
    "support_certificate_path",
    "no_cancellation_guard",
    "input_valid_for_claim",
    "notes",
]

P4_NUMERIC_FIELDS = ["uu_abs", "trace_abs"]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def bool_text(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: object) -> Tuple[bool, float]:
    text = str(value).strip()
    if not text or "MISSING" in text.upper():
        return False, math.nan
    try:
        number = float(text)
    except ValueError:
        return False, math.nan
    return math.isfinite(number), number


def existing_path(value: object) -> bool:
    text = str(value).strip()
    return bool(text and "MISSING" not in text.upper() and Path(text).exists())


def fmt(value: float) -> str:
    return "" if math.isnan(value) else f"{value:.12g}"


def evaluate_signature_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in SIGNATURE_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    booleans = {field: bool_text(row.get(field, "False")) for field in SIGNATURE_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = existing_path(source_path)
    input_valid = booleans["input_valid_for_claim"]

    action_factorization_ready = all(
        booleans[field]
        for field in [
            "ordinary_matter_factors_through_e_obs",
            "spin_connection_is_omega_LC",
            "no_Gamma_ind_argument",
            "no_contorsion_argument",
            "EM_Hilbert_no_affine_source",
        ]
    )
    downstream_ready = (
        booleans["clocks_light_orbits_downstream_metric"]
        and booleans["same_tau_coframe_support"]
    )
    affine_safety_ready = (
        booleans["no_hypermomentum_source"]
        and booleans["projective_trace_guard"]
        and booleans["boundary_readout_no_torsion_current"]
    )
    selector_ready = booleans["counterbranch_excluded"] and booleans["parent_selector_signed"]
    zero_schema_ready = (
        not missing_fields
        and source_exists
        and action_factorization_ready
        and downstream_ready
        and affine_safety_ready
        and selector_ready
    )
    zero_certificate_ready = zero_schema_ready and input_valid

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    for field, value in booleans.items():
        if not value and field != "input_valid_for_claim":
            reasons.append(f"OPEN_{field.upper()}")
    if action_factorization_ready and not selector_ready:
        reasons.append("PRIVATE_BRANCH_NOT_PUBLIC_PARENT_SELECTOR")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if zero_certificate_ready:
        status = "SPIN_TORSION_ALGEBRAIC_ZERO_READY"
    elif zero_schema_ready:
        status = "SPIN_TORSION_ZERO_SCHEMA_READY_NONCLAIM"
    elif action_factorization_ready:
        status = "OWNED_COFRAME_BRANCH_READY_SELECTOR_OR_GUARDS_OPEN"
    else:
        status = "SPIN_TORSION_ALGEBRAIC_ZERO_BLOCKED"

    return {
        "signature_id": str(row.get("signature_id", "")),
        "branch": str(row.get("branch", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "action_factorization_ready": str(action_factorization_ready),
        "downstream_ready": str(downstream_ready),
        "affine_safety_ready": str(affine_safety_ready),
        "selector_ready": str(selector_ready),
        "zero_schema_ready": str(zero_schema_ready),
        "zero_certificate_ready": str(zero_certificate_ready),
        "valid_for_claim": str(zero_certificate_ready),
        "claim_allowed": str(zero_certificate_ready),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_p4_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in P4_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    parsed = {field: parse_float(row.get(field, "")) for field in P4_NUMERIC_FIELDS}
    numeric_ready = all(ok and value >= 0.0 for ok, value in parsed.values())
    source_path = str(row.get("source_path", "")).strip()
    support_path = str(row.get("support_certificate_path", "")).strip()
    source_exists = existing_path(source_path)
    support_exists = existing_path(support_path)
    no_cancellation = bool_text(row.get("no_cancellation_guard", "False"))
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    projection_ready = "MISSING" not in str(row.get("projection_matrix", "")).upper()
    schema_ready = not missing_fields and numeric_ready and projection_ready and no_cancellation
    support_ready = source_exists and support_exists
    valid_for_claim = schema_ready and support_ready and input_valid

    if numeric_ready:
        ricci_component_bound = parsed["uu_abs"][1] + 0.5 * parsed["trace_abs"][1]
    else:
        ricci_component_bound = math.nan

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0.0:
            reasons.append(f"NEGATIVE_{field}")
    if not projection_ready:
        reasons.append("MISSING_PROJECTION_MATRIX")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not support_exists:
        reasons.append("MISSING_SUPPORT_CERTIFICATE_PATH")
    if not no_cancellation:
        reasons.append("NO_CANCELLATION_GUARD_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if valid_for_claim:
        status = "P4_RUU_COMPONENT_ROW_READY"
    elif schema_ready and support_ready:
        status = "P4_RUU_COMPONENT_SCHEMA_READY_NONCLAIM"
    elif schema_ready:
        status = "P4_RUU_COMPONENT_SCHEMA_READY_MISSING_SUPPORT_OR_SOURCE"
    else:
        status = "P4_RUU_COMPONENT_ROW_BLOCKED"

    return {
        "row_id": str(row.get("row_id", "")),
        "p4_component": str(row.get("p4_component", "")),
        "p4_channel": str(row.get("p4_channel", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "support_certificate_path": support_path,
        "support_exists": str(support_exists),
        "numeric_ready": str(numeric_ready),
        "projection_ready": str(projection_ready),
        "schema_ready": str(schema_ready),
        "support_ready": str(support_ready),
        "ricci_component_bound": fmt(ricci_component_bound),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_signature_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_signature_row(row, input_path) for row in read_csv(input_path)]


def evaluate_p4_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_p4_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate spin/torsion algebraic zero against P4/R_uu fallback rows.")
    parser.add_argument("--mode", choices=["signature", "p4"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.mode == "signature":
        write_csv(args.output, evaluate_signature_rows(args.input))
    else:
        write_csv(args.output, evaluate_p4_rows(args.input))


if __name__ == "__main__":
    main()
