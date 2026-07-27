from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "ready", "proved", "signed"}


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and Path(text).exists()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    materialized = [{key: str(value) for key, value in row.items()} for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not materialized:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(materialized[0].keys()))
        writer.writeheader()
        writer.writerows(materialized)


def evaluate_projection_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    standard_projection_written = as_bool(row.get("standard_projection_written", "False"))
    mts_coefficient_mapped = as_bool(row.get("mts_coefficient_mapped", "False"))
    full_curve_available = as_bool(row.get("full_curve_available", "False"))
    parent_scale_signed = as_bool(row.get("parent_scale_signed", "False"))
    no_cancellation_guard = as_bool(row.get("no_cancellation_guard", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))
    alpha = as_float(row.get("alpha_standard", ""))
    anchor_exact = alpha is not None and abs(abs(alpha) - 1.0) < 1e-12

    if source_ok and standard_projection_written and mts_coefficient_mapped and full_curve_available:
        status = "ALPHA_LAMBDA_PROJECTION_SCORE_READY"
    elif source_ok and standard_projection_written and parent_scale_signed:
        status = "PARENT_SCALE_SIGNATURE_READY"
    elif source_ok and standard_projection_written:
        status = "STANDARD_ALPHA_LAMBDA_PROJECTION_WRITTEN_MTS_OR_CURVE_MISSING"
    elif source_ok:
        status = "SOURCE_PRESENT_PROJECTION_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and standard_projection_written and no_cancellation_guard and not public_claim_false and (
        (mts_coefficient_mapped and full_curve_available) or parent_scale_signed
    )
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not standard_projection_written:
        reasons.append("STANDARD_PROJECTION_WRITTEN_FALSE")
    if not mts_coefficient_mapped:
        reasons.append("MTS_COEFFICIENT_MAPPED_FALSE")
    if not full_curve_available:
        reasons.append("FULL_CURVE_AVAILABLE_FALSE")
    if not parent_scale_signed:
        reasons.append("PARENT_SCALE_SIGNED_FALSE")
    if not no_cancellation_guard:
        reasons.append("NO_CANCELLATION_GUARD_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "projection_id": row.get("projection_id", ""),
        "mode": row.get("mode", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "alpha_standard": "" if alpha is None else alpha,
        "lambda_symbol": row.get("lambda_symbol", ""),
        "mass_symbol": row.get("mass_symbol", ""),
        "projection_formula": row.get("projection_formula", ""),
        "standard_projection_written": standard_projection_written,
        "anchor_exact_alpha1": anchor_exact,
        "mts_coefficient_mapped": mts_coefficient_mapped,
        "full_curve_available": full_curve_available,
        "parent_scale_signed": parent_scale_signed,
        "no_cancellation_guard": no_cancellation_guard,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_parent_scale_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    hierarchy_written = as_bool(row.get("hierarchy_written", "False"))
    numeric_parent_value = as_bool(row.get("numeric_parent_value", "False"))
    exceeds_anchor = as_bool(row.get("exceeds_anchor_mass", "False"))
    coefficient_zero = as_bool(row.get("coefficient_zero", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and hierarchy_written and ((numeric_parent_value and exceeds_anchor) or coefficient_zero):
        status = "PARENT_SCALE_OR_ZERO_READY"
    elif source_ok and hierarchy_written:
        status = "PARENT_SCALE_SIGNATURE_WRITTEN_NUMERIC_VALUE_OR_ZERO_MISSING"
    elif source_ok:
        status = "SOURCE_PRESENT_PARENT_SCALE_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and hierarchy_written and ((numeric_parent_value and exceeds_anchor) or coefficient_zero) and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not hierarchy_written:
        reasons.append("HIERARCHY_WRITTEN_FALSE")
    if not numeric_parent_value:
        reasons.append("NUMERIC_PARENT_VALUE_FALSE")
    if not exceeds_anchor:
        reasons.append("EXCEEDS_ANCHOR_MASS_FALSE")
    if not coefficient_zero:
        reasons.append("COEFFICIENT_ZERO_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "scale_id": row.get("scale_id", ""),
        "scale_route": row.get("scale_route", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "scale_contract": row.get("scale_contract", ""),
        "hierarchy_written": hierarchy_written,
        "numeric_parent_value": numeric_parent_value,
        "exceeds_anchor_mass": exceeds_anchor,
        "coefficient_zero": coefficient_zero,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate cR2 alpha(lambda) projection and parent scale rows.")
    parser.add_argument("--mode", choices=["projection", "scale"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_csv(args.input)
    output = [evaluate_projection_row(row) for row in rows] if args.mode == "projection" else [evaluate_parent_scale_row(row) for row in rows]
    write_csv(args.output, output)


if __name__ == "__main__":
    main()
