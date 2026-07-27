from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Mapping


REQUIRED_FIELDS = [
    "candidate_id",
    "branch",
    "action_signature_written",
    "parent_origin_signed",
    "residual_density_object_parent_owned",
    "sigma_pre_readout_lock",
    "lambda_boundary_anchor_signed",
    "elliptic_operator_positive_or_gauge_fixed",
    "zero_mode_removed",
    "multiplier_null_theorem_available",
    "metric_variation_payload_zero_or_bounded",
    "static_tau_silence_pass",
    "affine_boundary_pairings_pass",
    "ward_conservation_owned",
    "no_late_green_inverse",
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
    signature_ready = (
        bool_values["action_signature_written"]
        and bool_values["parent_origin_signed"]
        and bool_values["residual_density_object_parent_owned"]
        and bool_values["sigma_pre_readout_lock"]
        and bool_values["no_late_green_inverse"]
    )
    multiplier_safe = (
        bool_values["lambda_boundary_anchor_signed"]
        and bool_values["elliptic_operator_positive_or_gauge_fixed"]
        and bool_values["zero_mode_removed"]
        and bool_values["multiplier_null_theorem_available"]
    )
    payload_safe = (
        bool_values["metric_variation_payload_zero_or_bounded"]
        and bool_values["static_tau_silence_pass"]
        and bool_values["affine_boundary_pairings_pass"]
        and bool_values["ward_conservation_owned"]
        and bool_values["em_double_count_guard_signed"]
    )
    passed = not missing_fields and source_exists and signature_ready and multiplier_safe and payload_safe
    failed_clauses = [field for field, value in bool_values.items() if not value]
    if missing_fields:
        status = "SIGMAS_ACTION_GATE_MISSING_FIELDS"
    elif not source_exists:
        status = "SIGMAS_ACTION_GATE_SOURCE_MISSING"
    elif passed:
        status = "SIGMAS_ACTION_GATE_PASS_CANDIDATE"
    elif signature_ready and multiplier_safe:
        status = "ACTION_SIGNATURE_MULTIPLIER_SAFE_PAYLOADS_OPEN"
    elif signature_ready:
        status = "ACTION_SIGNATURE_READY_MULTIPLIER_OR_PAYLOAD_OPEN"
    else:
        status = "SIGMAS_ACTION_GATE_BLOCKED_CLAUSES_OPEN"
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
        "signature_ready": str(signature_ready),
        "multiplier_safe": str(multiplier_safe),
        "payload_safe": str(payload_safe),
        "sigma_s_action_pass": str(passed),
        "valid_for_claim": str(passed),
        "claim_allowed": str(passed),
        "current_status": status,
    }


def evaluate_sigma_s_action_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_candidate(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate parent sigma_S action/constraint candidates.")
    parser.add_argument("--input", required=True, type=Path, help="Candidate sigma_S action CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_sigma_s_action_rows(args.input))


if __name__ == "__main__":
    main()
