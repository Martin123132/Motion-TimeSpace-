from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "branch",
    "u_from_tau_coframe_formula",
    "coframe_descent_signed",
    "tau_generator_signed",
    "tau_killing_signed",
    "s_tensor_parent_owned",
    "lie_tau_s_signed",
    "hypersurface_static_signed",
    "acceleration_shift_zero_or_bounded",
    "curvature_commutator_zero_or_bounded",
    "ward_conservation_owned",
    "boundary_flux_silent",
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
    u_parent_owned = (
        bool_values["u_from_tau_coframe_formula"]
        and bool_values["coframe_descent_signed"]
        and bool_values["tau_generator_signed"]
    )
    leading_time_pressure_zero = (
        u_parent_owned
        and bool_values["tau_killing_signed"]
        and bool_values["s_tensor_parent_owned"]
        and bool_values["lie_tau_s_signed"]
        and bool_values["hypersurface_static_signed"]
        and bool_values["acceleration_shift_zero_or_bounded"]
    )
    full_static_silence = leading_time_pressure_zero and bool_values["curvature_commutator_zero_or_bounded"]
    passed = (
        not missing_fields
        and source_exists
        and full_static_silence
        and bool_values["ward_conservation_owned"]
        and bool_values["boundary_flux_silent"]
    )
    failed_clauses = [field for field, value in bool_values.items() if not value]
    if missing_fields:
        status = "STATIC_TIME_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "STATIC_TIME_GATE_SOURCE_MISSING"
    elif passed:
        status = "STATIC_TIME_GATE_PASS_CANDIDATE"
    elif leading_time_pressure_zero:
        status = "LEADING_TIME_PRESSURE_ZERO_BUT_GLOBAL_PAYLOAD_OPEN"
    else:
        status = "STATIC_TIME_GATE_BLOCKED_CLAUSES_OPEN"
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
        "u_parent_owned": str(u_parent_owned),
        "leading_time_pressure_zero": str(leading_time_pressure_zero),
        "full_static_silence": str(full_static_silence),
        "static_time_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_static_time_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate static/time-silence candidates for electric U branches.")
    parser.add_argument("--input", required=True, type=Path, help="Static/time candidate CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_static_time_rows(args.input))


if __name__ == "__main__":
    main()
