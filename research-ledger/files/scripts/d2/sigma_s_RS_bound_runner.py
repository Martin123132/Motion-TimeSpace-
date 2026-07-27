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
    "M_H",
    "K_N",
    "lambda_stress_score",
    "kernel_stress_score",
    "delta_threshold",
    "source_path",
    "equation_ref",
    "no_cancellation_guard",
    "input_valid_for_claim",
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


def parse_positive_float(row: Mapping[str, str], field: str) -> Tuple[float, str]:
    value = str(row.get(field, "")).strip()
    if not value or "MISSING" in value.upper():
        return math.nan, f"MISSING_{field.upper()}"
    try:
        number = float(value)
    except ValueError:
        return math.nan, f"NON_NUMERIC_{field.upper()}"
    if not math.isfinite(number) or number < 0:
        return math.nan, f"INVALID_{field.upper()}"
    return number, ""


def evaluate_row(row: Mapping[str, str], input_path: Path) -> Dict[str, str]:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in row or str(row.get(field, "")).strip() == ""]
    theorem_zero = bool_text(row.get("theorem_zero", "False"))
    authority = str(row.get("theorem_zero_authority", "")).strip()
    input_valid = bool_text(row.get("input_valid_for_claim", "False"))
    no_cancellation = bool_text(row.get("no_cancellation_guard", "False"))
    source_path = str(row.get("source_path", "")).strip()
    source_exists = Path(source_path).exists() if source_path and "MISSING" not in source_path.upper() else False
    reasons: List[str] = []
    numeric: Dict[str, float] = {}
    for field in ["R_S_weighted_norm", "M_H", "K_N", "lambda_stress_score", "kernel_stress_score", "delta_threshold"]:
        numeric[field], error = parse_positive_float(row, field)
        if error:
            reasons.append(error)
    if missing_fields:
        reasons.extend([f"MISSING_FIELD_{field}" for field in missing_fields])
    if not source_exists:
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if not input_valid:
        reasons.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not no_cancellation:
        reasons.append("MISSING_NO_CANCELLATION_GUARD")

    theorem_zero_allowed = theorem_zero and authority.startswith("PARENT_SIGNED_") and source_exists and input_valid
    if theorem_zero and not theorem_zero_allowed:
        reasons.append("THEOREM_ZERO_AUTHORITY_NOT_PARENT_SIGNED")

    if theorem_zero_allowed:
        residual_score = 0.0
        total_score = numeric.get("lambda_stress_score", math.nan) + numeric.get("kernel_stress_score", math.nan)
    elif numeric.get("M_H", 0.0) > 0 and math.isfinite(numeric.get("R_S_weighted_norm", math.nan)) and math.isfinite(numeric.get("K_N", math.nan)):
        residual_score = numeric["K_N"] * numeric["R_S_weighted_norm"] / numeric["M_H"]
        total_score = residual_score + numeric.get("lambda_stress_score", math.nan) + numeric.get("kernel_stress_score", math.nan)
    else:
        residual_score = math.nan
        total_score = math.nan
        reasons.append("MISSING_POSITIVE_M_H_OR_NUMERIC_RESIDUAL")

    if not math.isfinite(total_score):
        pass_bound = False
        reasons.append("TOTAL_SCORE_NOT_FINITE")
    else:
        pass_bound = total_score <= numeric.get("delta_threshold", math.nan)
    valid_for_claim = pass_bound and source_exists and input_valid and no_cancellation and not reasons
    if theorem_zero_allowed:
        status = "THEOREM_ZERO_ROW_ACCEPTED" if valid_for_claim else "THEOREM_ZERO_ROW_PAYLOAD_OPEN"
    elif valid_for_claim:
        status = "FINITE_RS_BOUND_PASS"
    elif source_exists and input_valid:
        status = "FINITE_RS_BOUND_FAIL_OR_INCOMPLETE"
    else:
        status = "REFUSED_NONCLAIM_OR_MISSING_INPUTS"

    return {
        "candidate_id": str(row.get("candidate_id", "")),
        "target": str(row.get("target", "")),
        "input_path": str(input_path),
        "source_path": source_path,
        "source_exists": str(source_exists),
        "residual_score": "" if not math.isfinite(residual_score) else f"{residual_score:.16e}",
        "lambda_stress_score": str(row.get("lambda_stress_score", "")),
        "kernel_stress_score": str(row.get("kernel_stress_score", "")),
        "total_score": "" if not math.isfinite(total_score) else f"{total_score:.16e}",
        "delta_threshold": str(row.get("delta_threshold", "")),
        "pass_bound": str(pass_bound),
        "valid_for_claim": str(valid_for_claim),
        "claim_allowed": str(valid_for_claim),
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
        "current_status": status,
    }


def evaluate_bound_rows(input_path: Path) -> List[Dict[str, str]]:
    return [evaluate_row(row, input_path) for row in read_csv(input_path)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Score sigma_S residual and multiplier-stress bound rows.")
    parser.add_argument("--input", required=True, type=Path, help="R_S bound input CSV.")
    parser.add_argument("--output", required=True, type=Path, help="R_S bound output CSV.")
    args = parser.parse_args()
    write_csv(args.output, evaluate_bound_rows(args.input))


if __name__ == "__main__":
    main()
