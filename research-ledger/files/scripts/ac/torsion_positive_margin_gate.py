from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "ready", "proved", "signed"}


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and Path(text).exists()


def url_recorded(value: object) -> bool:
    text = str(value).strip().lower()
    return text.startswith("https://") or text.startswith("http://")


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


def evaluate_margin_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    stability_clause = as_bool(row.get("stability_clause_written", "False"))
    margin_formula = as_bool(row.get("margin_formula_written", "False"))
    excludes_critical = as_bool(row.get("excludes_critical_surface", "False"))
    parent_signed = as_bool(row.get("parent_signed", "False"))
    numeric_margin = as_bool(row.get("numeric_margin_available", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and stability_clause and margin_formula and excludes_critical and parent_signed and numeric_margin:
        status = "PARENT_POSITIVE_MARGIN_NUMERIC_READY"
    elif source_ok and stability_clause and margin_formula and excludes_critical:
        status = "PARENT_POSITIVE_MARGIN_CONTRACT_READY_SIGNATURE_OR_NUMERIC_MARGIN_MISSING"
    elif source_ok and stability_clause:
        status = "STABILITY_CLAUSE_READY_MARGIN_FORMULA_OPEN"
    elif source_ok:
        status = "SOURCE_PRESENT_MARGIN_CONTRACT_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and stability_clause and margin_formula and excludes_critical and parent_signed and numeric_margin and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not stability_clause:
        reasons.append("STABILITY_CLAUSE_WRITTEN_FALSE")
    if not margin_formula:
        reasons.append("MARGIN_FORMULA_WRITTEN_FALSE")
    if not excludes_critical:
        reasons.append("EXCLUDES_CRITICAL_SURFACE_FALSE")
    if not parent_signed:
        reasons.append("PARENT_SIGNED_FALSE")
    if not numeric_margin:
        reasons.append("NUMERIC_MARGIN_AVAILABLE_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "margin_id": row.get("margin_id", ""),
        "channel": row.get("channel", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "stability_clause": row.get("stability_clause", ""),
        "margin_formula": row.get("margin_formula", ""),
        "critical_surface": row.get("critical_surface", ""),
        "stability_clause_written": stability_clause,
        "margin_formula_written": margin_formula,
        "excludes_critical_surface": excludes_critical,
        "parent_signed": parent_signed,
        "numeric_margin_available": numeric_margin,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_source_row(row: Dict[str, str]) -> Dict[str, object]:
    url_ok = url_recorded(row.get("source_url", ""))
    source_verified = as_bool(row.get("source_verified", "False"))
    observable_mapped = as_bool(row.get("observable_mapped", "False"))
    numeric_extracted = as_bool(row.get("numeric_extracted", "False"))
    unit_converted = as_bool(row.get("unit_converted", "False"))
    projection_ready = as_bool(row.get("projection_to_lambda_margin_ready", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if url_ok and source_verified and observable_mapped and numeric_extracted and unit_converted and projection_ready:
        status = "SOURCE_BOUND_NUMERIC_PROJECTION_READY"
    elif url_ok and source_verified and observable_mapped:
        status = "SOURCE_BOUND_ROW_READY_NUMERIC_EXTRACTION_OR_PROJECTION_MISSING"
    elif url_ok and source_verified:
        status = "SOURCE_VERIFIED_MAPPING_OPEN"
    elif url_ok:
        status = "SOURCE_URL_RECORDED_UNVERIFIED"
    else:
        status = "SOURCE_URL_MISSING"

    valid_for_claim = url_ok and source_verified and observable_mapped and numeric_extracted and unit_converted and projection_ready and not public_claim_false
    reasons = []
    if not url_ok:
        reasons.append("SOURCE_URL_MISSING")
    if not source_verified:
        reasons.append("SOURCE_VERIFIED_FALSE")
    if not observable_mapped:
        reasons.append("OBSERVABLE_MAPPED_FALSE")
    if not numeric_extracted:
        reasons.append("NUMERIC_EXTRACTED_FALSE")
    if not unit_converted:
        reasons.append("UNIT_CONVERTED_FALSE")
    if not projection_ready:
        reasons.append("PROJECTION_TO_LAMBDA_MARGIN_READY_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "source_row_id": row.get("source_row_id", ""),
        "source_name": row.get("source_name", ""),
        "source_url": row.get("source_url", ""),
        "source_url_recorded": url_ok,
        "source_verified": source_verified,
        "observable": row.get("observable", ""),
        "observable_mapped": observable_mapped,
        "bound_use": row.get("bound_use", ""),
        "numeric_extracted": numeric_extracted,
        "unit_converted": unit_converted,
        "projection_to_lambda_margin_ready": projection_ready,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate parent-positive torsion margin and spin-contact source rows.")
    parser.add_argument("--mode", choices=["margin", "source"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_csv(args.input)
    output = [evaluate_margin_row(row) for row in rows] if args.mode == "margin" else [evaluate_source_row(row) for row in rows]
    write_csv(args.output, output)


if __name__ == "__main__":
    main()
