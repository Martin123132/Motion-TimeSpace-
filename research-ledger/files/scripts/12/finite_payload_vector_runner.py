from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


REQUIRED_FIELDS = [
    "payload_id",
    "target",
    "R_S_score",
    "J_U_score",
    "pressure_aniso_score",
    "curvature_boundary_score",
    "lambda_kernel_score",
    "EM_overlap_score",
    "lambda_curvature_source_score",
    "delta_threshold",
    "source_path",
    "same_support_certificate",
    "no_cancellation_guard",
    "input_valid_for_claim",
    "notes",
]

SCORE_FIELDS = [
    "R_S_score",
    "J_U_score",
    "pressure_aniso_score",
    "curvature_boundary_score",
    "lambda_kernel_score",
    "EM_overlap_score",
    "lambda_curvature_source_score",
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


def parse_float(value: object) -> Tuple[bool, float]:
    text = str(value).strip()
    if not text or "MISSING" in text.upper():
        return False, math.nan
    try:
        number = float(text)
    except ValueError:
        return False, math.nan
    return math.isfinite(number), number


def evaluate_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    parsed_scores = {field: parse_float(row.get(field, "")) for field in SCORE_FIELDS}
    threshold_ok, threshold = parse_float(row.get("delta_threshold", ""))
    numeric_scores_ready = all(ok and value >= 0.0 for ok, value in parsed_scores.values())
    threshold_ready = threshold_ok and threshold > 0.0
    schema_ready = not missing_fields and numeric_scores_ready and threshold_ready

    score_values = [abs(value) for ok, value in parsed_scores.values() if ok]
    total_payload_score = sum(score_values) if numeric_scores_ready else math.nan
    max_component_score = max(score_values) if score_values else math.nan

    source_path = str(row.get("source_path", "")).strip()
    certificate_path = str(row.get("same_support_certificate", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    certificate_exists = Path(certificate_path).exists() if certificate_path and "MISSING" not in certificate_path.upper() else False
    support_ready = source_exists and certificate_exists
    no_cancellation = bool_text(row.get("no_cancellation_guard", "False"))
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    payload_within_threshold = schema_ready and total_payload_score <= threshold
    valid_for_claim = schema_ready and support_ready and no_cancellation and input_valid and payload_within_threshold

    reasons: List[str] = []
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    for field, (ok, value) in parsed_scores.items():
        if not ok:
            reasons.append(f"MISSING_OR_NONNUMERIC_{field}")
        elif value < 0:
            reasons.append(f"NEGATIVE_{field}")
    if not threshold_ready:
        reasons.append("MISSING_OR_INVALID_DELTA_THRESHOLD")
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not certificate_exists:
        reasons.append("MISSING_SAME_SUPPORT_CERTIFICATE")
    if not no_cancellation:
        reasons.append("NO_CANCELLATION_GUARD_FALSE")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if schema_ready and not payload_within_threshold:
        reasons.append("PAYLOAD_VECTOR_EXCEEDS_THRESHOLD")

    if valid_for_claim:
        status = "FINITE_PAYLOAD_VECTOR_ACCEPTS"
    elif schema_ready and support_ready and no_cancellation and total_payload_score > threshold:
        status = "FINITE_PAYLOAD_VECTOR_FAILS_THRESHOLD"
    elif schema_ready:
        status = "FINITE_PAYLOAD_VECTOR_SCHEMA_READY_NONCLAIM"
    else:
        status = "FINITE_PAYLOAD_VECTOR_BLOCKED"

    return {
        "payload_id": str(row.get("payload_id", "")),
        "target": str(row.get("target", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "same_support_certificate": certificate_path,
        "certificate_exists": str(certificate_exists),
        "schema_ready": str(schema_ready),
        "support_ready": str(support_ready),
        "no_cancellation_guard": str(no_cancellation),
        "input_valid_for_claim": str(input_valid),
        "total_payload_score": "" if math.isnan(total_payload_score) else f"{total_payload_score:.12g}",
        "max_component_score": "" if math.isnan(max_component_score) else f"{max_component_score:.12g}",
        "delta_threshold": "" if not threshold_ready else f"{threshold:.12g}",
        "payload_within_threshold": str(payload_within_threshold),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_payload_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run finite local-GR payload vector checks without cancellation.")
    parser.add_argument("--input", required=True, type=Path, help="Finite payload vector input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="Finite payload vector output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_payload_rows(args.input))


if __name__ == "__main__":
    main()
