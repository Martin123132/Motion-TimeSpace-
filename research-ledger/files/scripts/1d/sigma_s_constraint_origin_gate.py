from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "origin_route",
    "nonpropagating_constraint_family_identified",
    "parent_object_language_signed",
    "origin_principle_derived",
    "residual_density_parent_owned",
    "sigma_lambda_added_before_readout",
    "constraint_rank_or_gauge_count_checked",
    "boundary_zero_mode_owner_signed",
    "same_tau_coframe_signed",
    "no_GR_import_or_fit",
    "no_late_multiplier",
    "source_path",
]

BOOLEAN_FIELDS = [field for field in REQUIRED_FIELDS if field not in {"candidate_id", "origin_route", "source_path"}]


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
    origin_ready = (
        bool_values["nonpropagating_constraint_family_identified"]
        and bool_values["parent_object_language_signed"]
        and bool_values["origin_principle_derived"]
        and bool_values["residual_density_parent_owned"]
        and bool_values["sigma_lambda_added_before_readout"]
        and bool_values["constraint_rank_or_gauge_count_checked"]
    )
    local_payload_ready = bool_values["boundary_zero_mode_owner_signed"] and bool_values["same_tau_coframe_signed"]
    guard_ready = bool_values["no_GR_import_or_fit"] and bool_values["no_late_multiplier"]
    passed = not missing_fields and source_exists and origin_ready and local_payload_ready and guard_ready
    failed_clauses = [field for field, value in bool_values.items() if not value]
    if missing_fields:
        status = "ORIGIN_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "ORIGIN_GATE_SOURCE_MISSING"
    elif passed:
        status = "ORIGIN_GATE_PASS_CANDIDATE"
    elif bool_values["nonpropagating_constraint_family_identified"] and guard_ready:
        status = "CONSTRAINT_FAMILY_IDENTIFIED_PARENT_ORIGIN_OPEN"
    else:
        status = "ORIGIN_GATE_BLOCKED_CLAUSES_OPEN"
    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "origin_route": str(row.get("origin_route", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "missing_fields": ";".join(missing_fields),
        "failed_clauses": ";".join(failed_clauses),
        "closed_clause_count": str(sum(1 for value in bool_values.values() if value)),
        "total_clause_count": str(len(bool_values)),
        "origin_ready": str(origin_ready),
        "local_payload_ready": str(local_payload_ready),
        "guard_ready": str(guard_ready),
        "origin_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_origin_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate parent-origin candidates for sigma/lambda constraints.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate origin CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_origin_rows(args.input))


if __name__ == "__main__":
    main()
