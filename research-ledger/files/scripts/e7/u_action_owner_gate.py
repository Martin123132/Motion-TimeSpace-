from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "branch",
    "parent_action_owner_signed",
    "u_field_owner_signed",
    "s_field_owner_signed",
    "riemann_symmetry_signed",
    "transverse_symmetric_s_signed",
    "electric_projector_identity_signed",
    "residual_density_identity_signed",
    "static_branch_signed",
    "time_derivative_silence_signed",
    "pressure_aniso_zero_or_bounded",
    "curvature_remainder_zero_or_bounded",
    "affine_boundary_pairings_pass",
    "ward_conservation_owned",
    "matter_coupling_quotient_owned",
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
    failed_clauses = [field for field, value in bool_values.items() if not value]
    passed = not missing_fields and source_exists and all(bool_values.values())
    if missing_fields:
        status = "U_OWNER_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "U_OWNER_GATE_SOURCE_MISSING"
    elif passed:
        status = "U_OWNER_GATE_PASS_CANDIDATE"
    else:
        status = "U_OWNER_GATE_BLOCKED_CLAUSES_OPEN"
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
        "u_owner_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_u_owner_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate electric-projector U/action owner candidates.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate U/action owner CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_u_owner_rows(args.input))


if __name__ == "__main__":
    main()
