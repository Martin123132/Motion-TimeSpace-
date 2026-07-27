from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "residual_identity_signed",
    "parent_u_owner_signed",
    "riemann_symmetry_signed",
    "metric_variation_owned",
    "pre_readout_lock_signed",
    "affine_boundary_pairings_pass",
    "curvature_remainder_zero_or_bounded",
    "pressure_anisotropy_zero_or_bounded",
    "conservation_ward_owned",
    "visible_em_not_double_counted",
    "source_path",
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


def evaluate_candidate(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    boolean_fields = [field for field in REQUIRED_FIELDS if field not in {"candidate_id", "source_path"}]
    bool_values = {field: bool_text(row.get(field, "False")) for field in boolean_fields}
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    passed = not missing_fields and source_exists and all(bool_values.values())
    failed_clauses = [field for field, value in bool_values.items() if not value]
    if missing_fields:
        status = "ADOPTION_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "ADOPTION_GATE_SOURCE_MISSING"
    elif passed:
        status = "ADOPTION_GATE_PASS_CANDIDATE"
    else:
        status = "ADOPTION_GATE_BLOCKED_CLAUSES_OPEN"
    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "missing_fields": ";".join(missing_fields),
        "failed_clauses": ";".join(failed_clauses),
        "closed_clause_count": str(sum(1 for value in bool_values.values() if value)),
        "total_clause_count": str(len(bool_values)),
        "adoption_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_adoption_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate curvature-improvement action adoption candidates.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate adoption CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_adoption_rows(args.input))


if __name__ == "__main__":
    main()
