from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3118_BALPHA_PRODUCT_BOUND_RUNNER_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3118_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(value: object) -> bool:
    text = str(value)
    return any(marker in text for marker in ("MISSING", "PLACEHOLDER", "template_invalid"))


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return OUT / path


def find_row(rows: list[dict[str, str]], row_id: str) -> dict[str, str] | None:
    if not row_id:
        return None
    for row in rows:
        if row_id in row.values():
            return row
    return None


def source_bound(row: dict[str, str]) -> tuple[str, str, str, str]:
    source_file = row.get("source_bound_file", "")
    source_row_id = row.get("source_row_id", "")
    path = source_path(source_file)
    source_rows = read_csv(path)
    source = find_row(source_rows, source_row_id)
    if source is None:
        return "", "", "source_row_missing", str(path)

    arena = row.get("arena", "")
    if arena == "clock":
        return (
            source.get("product_bound_1sigma_yr_inv", ""),
            "yr^-1",
            "clock_product_bound_1sigma",
            str(path),
        )
    if arena == "WEP":
        return (
            source.get("eta_bound", ""),
            "eta_dimensionless",
            "WEP_eta_bound_anchor_not_direct_product",
            str(path),
        )
    if arena == "R10":
        return (
            source.get("formula", ""),
            "formula_not_numeric",
            "R10_product_law_not_bound_value",
            str(path),
        )
    return "", "", "no_numeric_bound_for_arena", str(path)


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    issues: list[str] = []
    product_value = parse_float(row.get("product_value", ""))
    product_text = row.get("product_value", "")
    bound_value, bound_units, bound_status, bound_path = source_bound(row)
    numeric_bound = parse_float(bound_value)

    if has_missing_marker(product_text):
        issues.append("MISSING_MTS_PRODUCT_VALUE")
    if product_value is None:
        issues.append("NON_NUMERIC_PRODUCT_VALUE")
    if not is_true(row.get("valid_for_claim", "")):
        issues.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if "MISSING" in row.get("mts_inputs_status", ""):
        issues.append(row.get("mts_inputs_status", "MISSING_MTS_INPUTS"))
    if not Path(bound_path).exists():
        issues.append("BOUND_SOURCE_FILE_MISSING")
    if bound_status.endswith("not_direct_product") or bound_status.endswith("not_bound_value"):
        issues.append("BOUND_NOT_DIRECT_PRODUCT_LIMIT")
    if numeric_bound is None:
        issues.append("BOUND_NOT_NUMERIC")

    score = ""
    margin = ""
    if product_value is not None and numeric_bound is not None and numeric_bound >= 0:
        score = "pass_if_abs_product_le_bound" if abs(product_value) <= numeric_bound else "fail_if_abs_product_gt_bound"
        margin = numeric_bound - abs(product_value)
    else:
        score = "not_scoreable"

    claim_allowed = not issues
    return {
        "product_id": row.get("product_id", ""),
        "arena": row.get("arena", ""),
        "product_expression": row.get("product_expression", ""),
        "product_value": row.get("product_value", ""),
        "product_units": row.get("product_units", ""),
        "source_bound_value": bound_value,
        "source_bound_units": bound_units,
        "bound_status": bound_status,
        "score": score,
        "margin_to_bound": margin,
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "issues": ";".join(issues),
        "source_bound_path": bound_path,
        "source_row_id": row.get("source_row_id", ""),
        "required_inputs": row.get("required_inputs", ""),
        "generated_utc": stamp(),
    }


def validate(rows: list[dict[str, str]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    required = [
        "product_id",
        "arena",
        "product_expression",
        "product_value",
        "product_units",
        "required_inputs",
        "mts_inputs_status",
        "source_bound_file",
        "source_row_id",
        "valid_for_claim",
    ]
    columns = set(rows[0].keys()) if rows else set()
    missing_columns = [column for column in required if column not in columns]
    validations.append(
        {
            "check_id": "VAL3118_0_input_schema",
            "status": "pass" if rows and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    validations.append(
        {
            "check_id": "VAL3118_1_all_outputs_nonclaim",
            "status": "pass" if all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    validations.append(
        {
            "check_id": "VAL3118_2_missing_inputs_detected",
            "status": "pass" if any("MISSING" in row.get("issues", "") for row in outputs) else "fail",
            "details": json.dumps({row["product_id"]: row.get("issues", "") for row in outputs}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return validations


def main() -> None:
    rows = read_csv(INPUT)
    outputs = [evaluate_row(row) for row in rows]
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validate(rows, outputs))
    print(json.dumps({"input_rows": len(rows), "output_rows": len(outputs), "output": str(OUTPUT), "validation": str(VALIDATION)}, indent=2))


if __name__ == "__main__":
    main()
