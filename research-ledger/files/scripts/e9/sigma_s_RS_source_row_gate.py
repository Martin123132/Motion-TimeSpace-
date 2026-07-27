from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List, Mapping, Tuple


REQUIRED_FIELDS = [
    "candidate_id",
    "target",
    "theorem_zero",
    "theorem_zero_authority",
    "R_S_weighted_norm",
    "R_S_units",
    "M_H",
    "M_H_units",
    "K_N",
    "lambda_stress_score",
    "kernel_stress_score",
    "delta_threshold",
    "source_path",
    "source_row_id",
    "equation_ref",
    "W_H_geometry_source",
    "same_tau_coframe_certificate",
    "no_cancellation_guard",
    "input_valid_for_claim",
    "notes",
]

NUMERIC_FIELDS = [
    "R_S_weighted_norm",
    "M_H",
    "K_N",
    "lambda_stress_score",
    "kernel_stress_score",
    "delta_threshold",
]

RECOGNIZED_RS_UNITS = {
    "kg",
    "kg_effective",
    "same_units_as_M_H",
    "source_norm_same_as_M_H",
    "dimensionless_weighted_fraction",
    "theorem_zero_dimensionless",
}

RECOGNIZED_MH_UNITS = {
    "kg",
    "kg_effective",
    "same_units_as_R_S_norm",
    "dimensionless_normalized_mass",
}


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


def has_missing_marker(value: object) -> bool:
    text = str(value).strip()
    return not text or "MISSING" in text.upper()


def parse_nonnegative(row: Mapping[str, str], field: str) -> Tuple[float, str]:
    value = str(row.get(field, "")).strip()
    if has_missing_marker(value):
        return math.nan, f"MISSING_{field.upper()}"
    try:
        number = float(value)
    except ValueError:
        return math.nan, f"NON_NUMERIC_{field.upper()}"
    if not math.isfinite(number) or number < 0:
        return math.nan, f"INVALID_{field.upper()}"
    return number, ""


def path_exists(value: str) -> bool:
    return bool(value.strip()) and "MISSING" not in value.upper() and Path(value).exists()


def evaluate_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    reasons: List[str] = []
    numeric: Dict[str, float] = {}

    for field in NUMERIC_FIELDS:
        numeric[field], error = parse_nonnegative(row, field)
        if error:
            reasons.append(error)

    source_path = str(row.get("source_path", "")).strip()
    geometry_source = str(row.get("W_H_geometry_source", "")).strip()
    tau_certificate = str(row.get("same_tau_coframe_certificate", "")).strip()
    source_exists = path_exists(source_path)
    geometry_exists = path_exists(geometry_source)
    tau_exists = path_exists(tau_certificate)
    theorem_zero = bool_text(row.get("theorem_zero", "False"))
    theorem_authority = str(row.get("theorem_zero_authority", "")).strip()
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    no_cancellation = bool_text(row.get("no_cancellation_guard", "False"))
    rs_units = str(row.get("R_S_units", "")).strip()
    mh_units = str(row.get("M_H_units", "")).strip()

    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not geometry_exists:
        reasons.append("MISSING_W_H_GEOMETRY_SOURCE")
    if not tau_exists:
        reasons.append("MISSING_SAME_TAU_COFRAME_CERTIFICATE")
    if has_missing_marker(row.get("source_row_id", "")):
        reasons.append("MISSING_SOURCE_ROW_ID")
    if has_missing_marker(row.get("equation_ref", "")):
        reasons.append("MISSING_EQUATION_REF")
    if rs_units not in RECOGNIZED_RS_UNITS:
        reasons.append("UNRECOGNIZED_R_S_UNITS")
    if mh_units not in RECOGNIZED_MH_UNITS:
        reasons.append("UNRECOGNIZED_M_H_UNITS")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not no_cancellation:
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if numeric.get("M_H", math.nan) <= 0:
        reasons.append("M_H_MUST_BE_POSITIVE")
    if numeric.get("delta_threshold", math.nan) <= 0:
        reasons.append("DELTA_THRESHOLD_MUST_BE_POSITIVE")

    theorem_zero_allowed = theorem_zero and theorem_authority.startswith("PARENT_SIGNED_")
    if theorem_zero and not theorem_zero_allowed:
        reasons.append("THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED")

    numeric_complete = all(math.isfinite(numeric.get(field, math.nan)) for field in NUMERIC_FIELDS)
    source_detail_complete = not has_missing_marker(row.get("source_row_id", "")) and not has_missing_marker(row.get("equation_ref", ""))
    unit_ready = rs_units in RECOGNIZED_RS_UNITS and mh_units in RECOGNIZED_MH_UNITS
    source_ready = source_exists and geometry_exists and tau_exists and source_detail_complete
    schema_ready = not missing_fields and numeric_complete and unit_ready and source_ready
    theorem_or_finite_payload = theorem_zero_allowed or (numeric_complete and numeric.get("M_H", 0.0) > 0)
    ready_for_bound_runner = schema_ready and theorem_or_finite_payload and no_cancellation and input_valid and not reasons

    if ready_for_bound_runner:
        status = "RS_SOURCE_ROW_READY_FOR_BOUND_RUNNER"
    elif schema_ready and not input_valid:
        status = "RS_SOURCE_ROW_SCHEMA_READY_NONCLAIM"
    elif theorem_zero and not theorem_zero_allowed:
        status = "RS_THEOREM_ZERO_REFUSED_PARENT_AUTHORITY"
    else:
        status = "RS_SOURCE_ROW_BLOCKED"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "target": str(row.get("target", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "geometry_source_exists": str(geometry_exists),
        "tau_certificate_exists": str(tau_exists),
        "schema_ready": str(schema_ready),
        "source_ready": str(source_ready),
        "unit_ready": str(unit_ready),
        "numeric_complete": str(numeric_complete),
        "theorem_zero_allowed": str(theorem_zero_allowed),
        "ready_for_bound_runner": str(ready_for_bound_runner),
        "valid_for_claim": str(ready_for_bound_runner),
        "claim_allowed": str(ready_for_bound_runner),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_source_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate first real sigma_S residual source rows before the bound runner.")
    parser.add_argument("--input", required=True, type=Path, help="R_S source row input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="R_S source row gate output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_source_rows(args.input))


if __name__ == "__main__":
    main()
