from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "branch",
    "residual_density_defined",
    "sigma_or_s_parent_field_signed",
    "laplacian_or_double_divergence_identity_signed",
    "pre_readout_lock_signed",
    "green_operator_parent_owned",
    "zero_mode_gauge_fixed",
    "affine_boundary_pairings_pass",
    "static_tau_silence_pass",
    "curvature_payload_zero_or_bounded",
    "ward_conservation_owned",
    "em_double_count_guard_signed",
    "source_path",
]

BOOLEAN_FIELDS = [field for field in REQUIRED_FIELDS if field not in {"candidate_id", "branch", "source_path"}]


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


def evaluate_candidate(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    bool_values = {field: bool_text(row.get(field, "False")) for field in BOOLEAN_FIELDS}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    owner_identity_ready = (
        bool_values["residual_density_defined"]
        and bool_values["sigma_or_s_parent_field_signed"]
        and bool_values["laplacian_or_double_divergence_identity_signed"]
        and bool_values["pre_readout_lock_signed"]
    )
    green_route_safe = bool_values["green_operator_parent_owned"] and bool_values["zero_mode_gauge_fixed"]
    boundary_static_ready = bool_values["affine_boundary_pairings_pass"] and bool_values["static_tau_silence_pass"]
    payload_ready = bool_values["curvature_payload_zero_or_bounded"] and bool_values["ward_conservation_owned"]
    passed = (
        not missing_fields
        and source_exists
        and owner_identity_ready
        and green_route_safe
        and boundary_static_ready
        and payload_ready
        and bool_values["em_double_count_guard_signed"]
    )
    failed_clauses = [field for field, value in bool_values.items() if not value]
    if missing_fields:
        status = "SIGMA_S_OWNER_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "SIGMA_S_OWNER_GATE_SOURCE_MISSING"
    elif passed:
        status = "SIGMA_S_OWNER_GATE_PASS_CANDIDATE"
    elif owner_identity_ready and not green_route_safe:
        status = "OWNER_IDENTITY_READY_GREEN_ZERO_MODE_OPEN"
    elif owner_identity_ready:
        status = "OWNER_IDENTITY_READY_PAYLOADS_OPEN"
    else:
        status = "SIGMA_S_OWNER_GATE_BLOCKED_CLAUSES_OPEN"
    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "branch": str(row.get("branch", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "missing_fields": ";".join(missing_fields),
        "failed_clauses": ";".join(failed_clauses),
        "closed_clause_count": str(sum(1 for value in bool_values.values() if value)),
        "total_clause_count": str(len(bool_values)),
        "owner_identity_ready": str(owner_identity_ready),
        "green_route_safe": str(green_route_safe),
        "boundary_static_ready": str(boundary_static_ready),
        "payload_ready": str(payload_ready),
        "sigma_s_owner_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_sigma_s_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate sigma/S residual-owner candidates for electric U.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate sigma/S owner CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_sigma_s_owner_rows(args.input))


if __name__ == "__main__":
    main()
