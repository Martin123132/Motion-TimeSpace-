from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "route",
    "parent_delta_source_declared",
    "topological_density_before_readout",
    "hilbert_density_before_readout",
    "common_tau_coframe_support",
    "stress_improvement_U_owned",
    "riemann_symmetry_or_electric_projector",
    "deltaT_double_divergence_identity",
    "density_projection_matches_delta_rho",
    "sigma_constraint_links_improvement",
    "ward_conservation_or_exchange_current",
    "boundary_mass_silence",
    "em_double_count_guard",
    "no_post_readout_fit",
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

SOURCE_FIELDS = [
    "parent_delta_source_declared",
    "topological_density_before_readout",
    "hilbert_density_before_readout",
    "common_tau_coframe_support",
]

IMPROVEMENT_FIELDS = [
    "riemann_symmetry_or_electric_projector",
    "deltaT_double_divergence_identity",
    "density_projection_matches_delta_rho",
    "sigma_constraint_links_improvement",
]

CONSERVATION_FIELDS = [
    "ward_conservation_or_exchange_current",
    "boundary_mass_silence",
    "em_double_count_guard",
    "no_post_readout_fit",
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

    source_owner_ready = all(bool_values[field] for field in SOURCE_FIELDS)
    improvement_ready = all(bool_values[field] for field in IMPROVEMENT_FIELDS)
    conservation_ready = all(bool_values[field] for field in CONSERVATION_FIELDS)
    owner_certificate_ready = (
        not missing_fields
        and source_exists
        and source_owner_ready
        and improvement_ready
        and bool_values["stress_improvement_U_owned"]
        and conservation_ready
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

    if owner_certificate_ready:
        status = "SOURCE_OWNER_IMPROVEMENT_CERTIFICATE_READY"
        theorem_zero_authority = authority
    elif improvement_ready and not source_owner_ready:
        status = "IMPROVEMENT_MECHANISM_READY_SOURCE_OWNER_UNSIGNED"
        theorem_zero_authority = "CONDITIONAL_IMPROVEMENT_SOURCE_OWNER_UNSIGNED"
    elif improvement_ready:
        status = "IMPROVEMENT_MECHANISM_READY_CONSERVATION_OR_AUTHORITY_UNSIGNED"
        theorem_zero_authority = "CONDITIONAL_IMPROVEMENT_CONSERVATION_UNSIGNED"
    else:
        status = "SOURCE_OWNER_IMPROVEMENT_CERTIFICATE_BLOCKED"
        theorem_zero_authority = "NO_THEOREM_ZERO_AUTHORITY"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "route": str(row.get("route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "source_owner_ready": str(source_owner_ready),
        "improvement_ready": str(improvement_ready),
        "conservation_ready": str(conservation_ready),
        "parent_authority_ready": str(parent_authority_ready),
        "owner_certificate_ready": str(owner_certificate_ready),
        "theorem_zero_authority": theorem_zero_authority,
        "valid_for_claim": str(owner_certificate_ready),
        "claim_allowed": str(owner_certificate_ready),
        "failed_clauses": ";".join(failed_clauses),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate parent source-owner stress-improvement candidates for delta rho_topH.")
    parser.add_argument("--input", required=True, type=Path, help="Source-owner input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Source-owner output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_owner_rows(args.input))


if __name__ == "__main__":
    main()
