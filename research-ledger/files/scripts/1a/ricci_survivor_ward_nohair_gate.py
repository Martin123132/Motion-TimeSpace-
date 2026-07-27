from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


IDENTITY_REQUIRED_FIELDS = [
    "identity_id",
    "route",
    "diffeo_parent_action",
    "observed_coframe_owned",
    "Hilbert_source_only",
    "Bianchi_Ward_identity_written",
    "metric_response_helmholtz_closed",
    "Euler_on_shell_closed",
    "positive_self_adjoint_operator",
    "mass_gap_or_fixed_zero_mode",
    "source_current_zero",
    "boundary_no_flux",
    "projector_domain_silent",
    "Lambda_eff_zero_or_bound",
    "component_vector_covered",
    "no_cross_cancellation",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

IDENTITY_BOOLEAN_FIELDS = [
    field
    for field in IDENTITY_REQUIRED_FIELDS
    if field not in {"identity_id", "route", "source_path", "notes"}
]

COVERAGE_REQUIRED_FIELDS = [
    "coverage_id",
    "component",
    "required_by_vector",
    "represented_in_parent_identity",
    "positive_operator_slot",
    "no_independent_source_slot",
    "same_support",
    "boundary_projection_silent",
    "lambda_projector_silent",
    "identity_id",
    "source_path",
    "input_valid_for_claim",
    "notes",
]

COVERAGE_BOOLEAN_FIELDS = [
    field
    for field in COVERAGE_REQUIRED_FIELDS
    if field not in {"coverage_id", "component", "identity_id", "source_path", "notes"}
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


def existing_path(value: object) -> bool:
    text = str(value).strip()
    return bool(text and "MISSING" not in text.upper() and Path(text).exists())


def evaluate_identity_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [
        field
        for field in IDENTITY_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    booleans = {field: bool_text(row.get(field, "False")) for field in IDENTITY_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = existing_path(source_path)
    input_valid = booleans["input_valid_for_claim"]

    ward_identity_ready = all(
        booleans[field]
        for field in [
            "diffeo_parent_action",
            "observed_coframe_owned",
            "Hilbert_source_only",
            "Bianchi_Ward_identity_written",
        ]
    )
    response_ready = booleans["metric_response_helmholtz_closed"]
    nohair_energy_ready = all(
        booleans[field]
        for field in [
            "Euler_on_shell_closed",
            "positive_self_adjoint_operator",
            "mass_gap_or_fixed_zero_mode",
            "source_current_zero",
            "boundary_no_flux",
            "projector_domain_silent",
            "Lambda_eff_zero_or_bound",
            "component_vector_covered",
            "no_cross_cancellation",
        ]
    )
    zero_certificate_ready = (
        not missing_fields
        and source_exists
        and ward_identity_ready
        and response_ready
        and nohair_energy_ready
        and input_valid
    )
    schema_zero_ready = (
        not missing_fields
        and source_exists
        and ward_identity_ready
        and response_ready
        and nohair_energy_ready
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    for field, value in booleans.items():
        if not value and field != "input_valid_for_claim":
            reasons.append(f"OPEN_{field.upper()}")
    if ward_identity_ready and not nohair_energy_ready:
        reasons.append("WARD_DIVERGENCE_DOES_NOT_IMPLY_ZERO")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if zero_certificate_ready:
        status = "WARD_NOHAIR_RICCI_SURVIVOR_ZERO_READY"
        theorem_output = "R_uu_survivor=0"
    elif schema_zero_ready:
        status = "WARD_NOHAIR_ZERO_SCHEMA_READY_NONCLAIM"
        theorem_output = "conditional_R_uu_survivor_zero_schema"
    elif ward_identity_ready:
        status = "WARD_IDENTITY_DIVERGENCE_ONLY_NOT_ZERO"
        theorem_output = "nabla_mu_E_surv_mu_nu=0_only"
    else:
        status = "WARD_NOHAIR_ZERO_BLOCKED"
        theorem_output = "no_zero_theorem"

    return {
        "identity_id": str(row.get("identity_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "ward_identity_ready": str(ward_identity_ready),
        "metric_response_ready": str(response_ready),
        "nohair_energy_ready": str(nohair_energy_ready),
        "schema_zero_ready": str(schema_zero_ready),
        "zero_certificate_ready": str(zero_certificate_ready),
        "theorem_output": theorem_output,
        "valid_for_claim": str(zero_certificate_ready),
        "claim_allowed": str(zero_certificate_ready),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_identity_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_identity_row(row, input_path) for row in read_csv(input_path)]


def identity_lookup(identity_rows: List[Mapping[str, str]]) -> Dict[str, Mapping[str, str]]:
    return {str(row.get("identity_id", "")): row for row in identity_rows}


def evaluate_coverage_row(
    row: Mapping[str, str],
    input_path: Path,
    identity_rows: List[Mapping[str, str]],
    identity_output_path: Path,
) -> Dict[str, str]:
    missing_fields = [
        field
        for field in COVERAGE_REQUIRED_FIELDS
        if field not in row or str(row.get(field, "")).strip() == ""
    ]
    booleans = {field: bool_text(row.get(field, "False")) for field in COVERAGE_BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = existing_path(source_path)
    input_valid = booleans["input_valid_for_claim"]
    identities = identity_lookup(identity_rows)
    identity_id = str(row.get("identity_id", ""))
    identity = identities.get(identity_id)
    identity_exists = identity is not None
    identity_zero_ready = bool_text(identity.get("zero_certificate_ready", "False")) if identity else False
    identity_schema_ready = bool_text(identity.get("schema_zero_ready", "False")) if identity else False
    component_covered = all(
        booleans[field]
        for field in [
            "required_by_vector",
            "represented_in_parent_identity",
            "positive_operator_slot",
            "no_independent_source_slot",
            "same_support",
            "boundary_projection_silent",
            "lambda_projector_silent",
        ]
    )
    coverage_ready = (
        not missing_fields
        and source_exists
        and identity_zero_ready
        and component_covered
        and input_valid
    )
    coverage_schema_ready = (
        not missing_fields
        and source_exists
        and identity_schema_ready
        and component_covered
    )

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not identity_exists:
        reasons.append("MISSING_IDENTITY_OUTPUT_ROW")
    elif not identity_zero_ready:
        reasons.append("IDENTITY_NOT_CLAIM_READY")
    for field, value in booleans.items():
        if not value and field != "input_valid_for_claim":
            reasons.append(f"OPEN_{field.upper()}")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")

    if coverage_ready:
        status = "COMPONENT_COVERED_BY_WARD_NOHAIR_ZERO"
    elif coverage_schema_ready:
        status = "COMPONENT_COVERAGE_SCHEMA_READY_NONCLAIM"
    elif booleans["required_by_vector"] and not booleans["represented_in_parent_identity"]:
        status = "COMPONENT_REQUIRED_BUT_NOT_IN_IDENTITY"
    else:
        status = "COMPONENT_COVERAGE_BLOCKED"

    return {
        "coverage_id": str(row.get("coverage_id", "")),
        "component": str(row.get("component", "")),
        "identity_id": identity_id,
        "input_path": str(input_path),
        "identity_output_path": str(identity_output_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "identity_exists": str(identity_exists),
        "identity_zero_ready": str(identity_zero_ready),
        "identity_schema_ready": str(identity_schema_ready),
        "component_covered": str(component_covered),
        "coverage_schema_ready": str(coverage_schema_ready),
        "coverage_ready": str(coverage_ready),
        "valid_for_claim": str(coverage_ready),
        "claim_allowed": str(coverage_ready),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_coverage_rows(
    coverage_input_path: Path,
    identity_output_path: Path,
) -> List[Dict[str, str]]:
    identity_rows = read_csv(identity_output_path)
    return [
        evaluate_coverage_row(row, coverage_input_path, identity_rows, identity_output_path)
        for row in read_csv(coverage_input_path)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate a parent Ward/no-hair identity for the local Ricci survivor vector.")
    parser.add_argument("--mode", choices=["identity", "coverage"], required=True)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--identity-output", type=Path)
    args = parser.parse_args()
    if args.mode == "identity":
        write_csv(args.output, evaluate_identity_rows(args.input))
    else:
        if args.identity_output is None:
            raise SystemExit("--identity-output is required in coverage mode")
        write_csv(args.output, evaluate_coverage_rows(args.input, args.identity_output))


if __name__ == "__main__":
    main()
