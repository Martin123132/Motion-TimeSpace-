from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "diffeomorphism_invariant_parent_action",
    "metric_hilbert_variation_included",
    "U_or_S_field_equations_owned",
    "tau_coframe_variation_owned",
    "exchange_current_formula_written",
    "divergence_cancels_on_shell",
    "boundary_symplectic_flux_silent",
    "curvature_commutator_payload_bounded",
    "pressure_aniso_payload_bounded",
    "EM_double_count_guard",
    "same_support_as_R_S_row",
    "no_fixed_post_readout_U",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

BOOLEAN_FIELDS = [
    field
    for field in REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "parent_authority", "source_path", "notes"}
]

FORMULA_FIELDS = [
    "diffeomorphism_invariant_parent_action",
    "metric_hilbert_variation_included",
    "exchange_current_formula_written",
    "no_fixed_post_readout_U",
]

ON_SHELL_FIELDS = [
    "U_or_S_field_equations_owned",
    "tau_coframe_variation_owned",
    "divergence_cancels_on_shell",
]

PAYLOAD_FIELDS = [
    "boundary_symplectic_flux_silent",
    "curvature_commutator_payload_bounded",
    "pressure_aniso_payload_bounded",
    "EM_double_count_guard",
    "same_support_as_R_S_row",
]


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


def evaluate_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    bool_values = {field: bool_text(row.get(field, "False")) for field in BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    authority = str(row.get("parent_authority", "")).strip()
    parent_authority_ready = authority.startswith("PARENT_SIGNED_")
    input_valid = bool_values["input_valid_for_claim"]

    formula_ready = all(bool_values[field] for field in FORMULA_FIELDS)
    on_shell_ready = all(bool_values[field] for field in ON_SHELL_FIELDS)
    payload_ready = all(bool_values[field] for field in PAYLOAD_FIELDS)
    ward_certificate_ready = (
        not missing_fields
        and source_exists
        and formula_ready
        and on_shell_ready
        and payload_ready
        and parent_authority_ready
        and input_valid
    )

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if ward_certificate_ready:
        status = "WARD_EXCHANGE_CERTIFICATE_READY"
        exchange_authority = authority
    elif formula_ready and not on_shell_ready:
        status = "WARD_FORMULA_READY_PARENT_EQUATIONS_UNSIGNED"
        exchange_authority = "CONDITIONAL_WARD_FORMULA_PARENT_EQUATIONS_UNSIGNED"
    elif formula_ready:
        status = "WARD_FORMULA_READY_PAYLOADS_OR_AUTHORITY_UNSIGNED"
        exchange_authority = "CONDITIONAL_WARD_FORMULA_PAYLOADS_UNSIGNED"
    else:
        status = "WARD_EXCHANGE_CERTIFICATE_BLOCKED"
        exchange_authority = "NO_WARD_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "formula_ready": str(formula_ready),
        "on_shell_ready": str(on_shell_ready),
        "payload_ready": str(payload_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "ward_certificate_ready": str(ward_certificate_ready),
        "exchange_authority": exchange_authority,
        "valid_for_claim": str(ward_certificate_ready),
        "claim_allowed": str(ward_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_ward_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate Ward/exchange-current candidates for the electric U/S route.")
    parser.add_argument("--input", required=True, type=Path, help="Ward/exchange input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Ward/exchange output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_ward_rows(args.input))


if __name__ == "__main__":
    main()
