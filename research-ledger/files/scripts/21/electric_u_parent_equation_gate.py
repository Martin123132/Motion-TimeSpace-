from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "parent_action_declared",
    "variation_kind",
    "U_independence_resolved",
    "E_U_or_E_S_equation_written",
    "no_curvature_multiplier_overconstraint",
    "equation_has_source_or_constitutive_term",
    "compatible_with_nonzero_local_curvature",
    "Ward_exchange_formula_linked",
    "boundary_flux_terms_declared",
    "pressure_curvature_payload_vector_declared",
    "EM_double_count_guard",
    "finite_bound_fallback_declared",
    "parent_authority",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

BOOLEAN_FIELDS = [
    field
    for field in REQUIRED_FIELDS
    if field not in {"candidate_id", "route", "variation_kind", "parent_authority", "source_path", "notes"}
]

EQUATION_FIELDS = [
    "parent_action_declared",
    "U_independence_resolved",
    "E_U_or_E_S_equation_written",
    "no_curvature_multiplier_overconstraint",
    "equation_has_source_or_constitutive_term",
    "compatible_with_nonzero_local_curvature",
]

WARD_FIELDS = [
    "Ward_exchange_formula_linked",
    "boundary_flux_terms_declared",
]

PAYLOAD_FIELDS = [
    "pressure_curvature_payload_vector_declared",
    "EM_double_count_guard",
    "finite_bound_fallback_declared",
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
    variation_kind = str(row.get("variation_kind", "")).strip()

    equation_ready = all(bool_values[field] for field in EQUATION_FIELDS)
    ward_ready = all(bool_values[field] for field in WARD_FIELDS)
    payload_ready = all(bool_values[field] for field in PAYLOAD_FIELDS)
    parent_equation_certificate_ready = (
        not missing_fields
        and source_exists
        and equation_ready
        and ward_ready
        and payload_ready
        and parent_authority_ready
        and input_valid
    )

    overconstraint_trap = (
        variation_kind in {"independent_linear_U", "independent_linear_S_electric"}
        and bool_values["parent_action_declared"]
        and bool_values["E_U_or_E_S_equation_written"]
        and not bool_values["no_curvature_multiplier_overconstraint"]
    )

    failed_clauses = [field for field, value in bool_values.items() if not value]
    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if overconstraint_trap:
        reasons.append("PURE_LINEAR_U_OR_S_CURVATURE_MULTIPLIER_OVERCONSTRAINT")
    if not parent_authority_ready:
        reasons.append("PARENT_AUTHORITY_NOT_SIGNED")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    reasons.extend([f"OPEN_{field.upper()}" for field in failed_clauses if field != "input_valid_for_claim"])

    if parent_equation_certificate_ready:
        status = "PARENT_US_EQUATION_CERTIFICATE_READY"
        equation_authority = authority
    elif overconstraint_trap:
        status = "PURE_LINEAR_US_ROUTE_OVERCONSTRAINS_CURVATURE"
        equation_authority = "NO_AUTHORITY_PURE_LINEAR_CURVATURE_MULTIPLIER"
    elif equation_ready and ward_ready:
        status = "PARENT_US_EQUATION_FORM_READY_PAYLOADS_OR_AUTHORITY_UNSIGNED"
        equation_authority = "CONDITIONAL_US_EQUATION_PAYLOADS_UNSIGNED"
    elif bool_values["parent_action_declared"] and bool_values["E_U_or_E_S_equation_written"]:
        status = "PARENT_US_EQUATION_FORM_WRITTEN_BUT_UNSAFE"
        equation_authority = "CONDITIONAL_US_EQUATION_UNSAFE_OR_INCOMPLETE"
    else:
        status = "PARENT_US_EQUATION_CERTIFICATE_BLOCKED"
        equation_authority = "NO_US_EQUATION_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "variation_kind": variation_kind,
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "equation_ready": str(equation_ready),
        "ward_ready": str(ward_ready),
        "payload_ready": str(payload_ready),
        "overconstraint_trap": str(overconstraint_trap),
        "parent_authority_ready": str(parent_authority_ready),
        "parent_equation_certificate_ready": str(parent_equation_certificate_ready),
        "equation_authority": equation_authority,
        "valid_for_claim": str(parent_equation_certificate_ready),
        "claim_allowed": str(parent_equation_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_equation_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate parent U/S equation candidates for the electric improvement route.")
    parser.add_argument("--input", required=True, type=Path, help="Parent U/S equation input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Parent U/S equation output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_equation_rows(args.input))


if __name__ == "__main__":
    main()
