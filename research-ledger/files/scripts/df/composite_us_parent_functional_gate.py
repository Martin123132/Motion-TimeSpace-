from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "parent_functional_declared",
    "base_parent_fields_declared",
    "functional_derivative_written",
    "no_independent_U_variation",
    "sigma_constraint_coupled",
    "multiplier_null_survives_curvature_coupling",
    "curvature_sourced_lambda_bound_declared",
    "same_tau_coframe_support",
    "density_projection_matches_R_S",
    "Phi_equations_owned",
    "Ward_exchange_closes_on_shell",
    "boundary_flux_terms_declared",
    "pressure_curvature_payload_declared",
    "EM_double_count_guard",
    "finite_payload_fallback_declared",
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

FUNCTIONAL_FIELDS = [
    "parent_functional_declared",
    "base_parent_fields_declared",
    "functional_derivative_written",
    "no_independent_U_variation",
]

PROJECTION_FIELDS = [
    "same_tau_coframe_support",
    "density_projection_matches_R_S",
]

DYNAMICS_FIELDS = [
    "Phi_equations_owned",
    "Ward_exchange_closes_on_shell",
]

PAYLOAD_FIELDS = [
    "boundary_flux_terms_declared",
    "pressure_curvature_payload_declared",
    "EM_double_count_guard",
    "finite_payload_fallback_declared",
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

    functional_ready = all(bool_values[field] for field in FUNCTIONAL_FIELDS)
    projection_ready = all(bool_values[field] for field in PROJECTION_FIELDS)
    dynamics_ready = all(bool_values[field] for field in DYNAMICS_FIELDS)
    lambda_safe = (
        not bool_values["sigma_constraint_coupled"]
        or bool_values["multiplier_null_survives_curvature_coupling"]
        or bool_values["curvature_sourced_lambda_bound_declared"]
    )
    payload_ready = all(bool_values[field] for field in PAYLOAD_FIELDS) and lambda_safe
    curvature_sourced_lambda_obstruction = (
        bool_values["sigma_constraint_coupled"]
        and bool_values["parent_functional_declared"]
        and not bool_values["multiplier_null_survives_curvature_coupling"]
        and not bool_values["curvature_sourced_lambda_bound_declared"]
    )

    certificate_ready = (
        not missing_fields
        and source_exists
        and functional_ready
        and projection_ready
        and dynamics_ready
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
    if curvature_sourced_lambda_obstruction:
        reasons.append("CURVATURE_SOURCED_LAMBDA_PAYLOAD_UNBOUND")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if certificate_ready:
        status = "COMPOSITE_US_PARENT_FUNCTIONAL_CERTIFICATE_READY"
        authority_out = authority
    elif curvature_sourced_lambda_obstruction:
        status = "COMPOSITE_SIGMA_U_CURVATURE_SOURCED_LAMBDA_OBSTRUCTION"
        authority_out = "NO_AUTHORITY_LAMBDA_CURVATURE_SOURCE_UNBOUND"
    elif functional_ready and projection_ready and dynamics_ready:
        status = "COMPOSITE_US_FORM_READY_PAYLOADS_OR_AUTHORITY_UNSIGNED"
        authority_out = "CONDITIONAL_COMPOSITE_US_DYNAMICS_PAYLOADS_UNSIGNED"
    elif functional_ready and projection_ready:
        status = "COMPOSITE_US_FORM_READY_DYNAMICS_UNSIGNED"
        authority_out = "CONDITIONAL_COMPOSITE_US_FUNCTIONAL_DYNAMICS_UNSIGNED"
    elif bool_values["parent_functional_declared"]:
        status = "COMPOSITE_US_TEMPLATE_WRITTEN_INCOMPLETE"
        authority_out = "TEMPLATE_ONLY_COMPOSITE_US"
    else:
        status = "COMPOSITE_US_CERTIFICATE_BLOCKED"
        authority_out = "NO_COMPOSITE_US_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "functional_ready": str(functional_ready),
        "projection_ready": str(projection_ready),
        "dynamics_ready": str(dynamics_ready),
        "lambda_safe": str(lambda_safe),
        "payload_ready": str(payload_ready),
        "curvature_sourced_lambda_obstruction": str(curvature_sourced_lambda_obstruction),
        "parent_authority_ready": str(parent_authority_ready),
        "composite_certificate_ready": str(certificate_ready),
        "composite_authority": authority_out,
        "valid_for_claim": str(certificate_ready),
        "claim_allowed": str(certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_composite_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate composite U/S[Phi] parent-functional candidates.")
    parser.add_argument("--input", required=True, type=Path, help="Composite U/S input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Composite U/S gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_composite_rows(args.input))


if __name__ == "__main__":
    main()
