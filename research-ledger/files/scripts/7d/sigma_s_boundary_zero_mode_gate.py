from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "laplacian_operator_declared",
    "W_H_domain_parent_owned",
    "tau_coframe_same_as_readout",
    "source_density_parent_owned",
    "sigma_boundary_condition_signed",
    "zero_mode_fixed_or_compatibility_signed",
    "lambda_boundary_condition_signed",
    "lambda_zero_mode_fixed",
    "boundary_variation_silent",
    "kernel_stress_zero_or_bounded",
    "no_post_readout_green_solve",
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

ELLIPTIC_FIELDS = [
    "laplacian_operator_declared",
    "sigma_boundary_condition_signed",
    "zero_mode_fixed_or_compatibility_signed",
    "lambda_boundary_condition_signed",
    "lambda_zero_mode_fixed",
    "no_post_readout_green_solve",
]

SUPPORT_FIELDS = [
    "W_H_domain_parent_owned",
    "tau_coframe_same_as_readout",
    "boundary_variation_silent",
    "kernel_stress_zero_or_bounded",
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

    elliptic_ready = all(bool_values[field] for field in ELLIPTIC_FIELDS)
    support_ready = all(bool_values[field] for field in SUPPORT_FIELDS)
    source_owner_ready = bool_values["source_density_parent_owned"]
    parent_ready = parent_authority_ready and input_valid and source_exists
    boundary_certificate_ready = (
        not missing_fields
        and elliptic_ready
        and support_ready
        and source_owner_ready
        and parent_ready
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

    if boundary_certificate_ready:
        status = "BOUNDARY_ZERO_MODE_CERTIFICATE_READY"
        theorem_zero_authority = authority
    elif elliptic_ready and not source_owner_ready:
        status = "ELLIPTIC_ZERO_MODE_MECHANISM_READY_SOURCE_OWNER_UNSIGNED"
        theorem_zero_authority = "CONDITIONAL_ELLIPTIC_ZERO_MODE_SOURCE_OWNER_UNSIGNED"
    elif elliptic_ready:
        status = "ELLIPTIC_ZERO_MODE_MECHANISM_READY_PARENT_UNSIGNED"
        theorem_zero_authority = "CONDITIONAL_ELLIPTIC_ZERO_MODE_PARENT_UNSIGNED"
    else:
        status = "BOUNDARY_ZERO_MODE_CERTIFICATE_BLOCKED"
        theorem_zero_authority = "NO_THEOREM_ZERO_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "elliptic_ready": str(elliptic_ready),
        "support_ready": str(support_ready),
        "source_owner_ready": str(source_owner_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "boundary_certificate_ready": str(boundary_certificate_ready),
        "theorem_zero_authority": theorem_zero_authority,
        "valid_for_claim": str(boundary_certificate_ready),
        "claim_allowed": str(boundary_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_boundary_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate sigma_S boundary/zero-mode theorem-zero certificates.")
    parser.add_argument("--input", required=True, type=Path, help="Boundary/zero-mode input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Boundary/zero-mode output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_boundary_rows(args.input))


if __name__ == "__main__":
    main()
