from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_INPUTS_TEMPLATE.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3121_DELTAJ_GM_BRIDGE_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3121_VALIDATION.csv"


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
    return any(marker in text for marker in ("MISSING", "PLACEHOLDER", "SMOKE"))


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str) -> dict[str, str] | None:
    if not row_id:
        return None
    for row in rows:
        if row_id in row.values():
            return row
    return None


def source_bound(row: dict[str, str]) -> tuple[str, str, str, str]:
    path = source_path(row.get("source_bound_file", ""))
    source = find_row(read_csv(path), row.get("source_row_id", ""))
    if source is None:
        return "", "", "source_row_missing", str(path)
    bound_column = row.get("bound_column", "")
    if bound_column not in source:
        return "", "", "bound_column_missing", str(path)
    value = source.get(bound_column, "")
    units = source.get("units", row.get("bound_units_expected", ""))
    if bound_column == "upper_bound":
        return value, units, "direct_empirical_anchor_requires_projection_kernel", str(path)
    if bound_column == "theorem_or_failure":
        return value, "text_not_numeric", "theorem_or_bridge_text_not_numeric", str(path)
    return value, units, "nonstandard_bound_column", str(path)


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    issues: list[str] = []
    delta_j = parse_float(row.get("deltaJ_value", ""))
    source_kernel = parse_float(row.get("source_kernel_CJ", ""))
    calibration_kernel = parse_float(row.get("calibration_kernel_CJ", ""))
    bound_value, bound_units, bound_status, bound_path = source_bound(row)
    numeric_bound = parse_float(bound_value)

    residual: float | str = ""
    kernel_difference: float | str = ""
    if delta_j is not None and source_kernel is not None and calibration_kernel is not None:
        kernel_difference = source_kernel - calibration_kernel
        residual = abs(kernel_difference * delta_j)

    if delta_j is None:
        issues.append("NON_NUMERIC_DELTAJ_VALUE")
    if source_kernel is None:
        issues.append("NON_NUMERIC_SOURCE_KERNEL_CJ")
    if calibration_kernel is None:
        issues.append("NON_NUMERIC_CALIBRATION_KERNEL_CJ")
    if has_missing_marker(row.get("deltaJ_value", "")):
        issues.append("MISSING_DELTAJ_VALUE")
    if has_missing_marker(row.get("source_kernel_CJ", "")):
        issues.append("MISSING_SOURCE_KERNEL_CJ")
    if has_missing_marker(row.get("calibration_kernel_CJ", "")):
        issues.append("MISSING_CALIBRATION_KERNEL_CJ")
    if has_missing_marker(row.get("assumptions_status", "")):
        issues.append(row.get("assumptions_status", "MISSING_ASSUMPTIONS"))
    if not is_true(row.get("valid_for_claim", "")):
        issues.append("INPUT_VALID_FOR_CLAIM_FALSE")
    if not Path(bound_path).exists():
        issues.append("BOUND_SOURCE_FILE_MISSING")
    if numeric_bound is None:
        issues.append("BOUND_NOT_NUMERIC")
    if "direct_empirical_anchor_requires_projection_kernel" in bound_status and (
        source_kernel is None or calibration_kernel is None or has_missing_marker(row.get("assumptions_status", ""))
    ):
        issues.append("EMPIRICAL_ANCHOR_NOT_DIRECT_WITHOUT_KERNEL")

    score = "not_scoreable"
    margin: float | str = ""
    if isinstance(residual, float) and numeric_bound is not None and numeric_bound >= 0:
        score = "pass_if_abs_residual_le_bound" if residual <= numeric_bound else "fail_if_abs_residual_gt_bound"
        margin = numeric_bound - residual

    claim_allowed = not issues
    return {
        "bridge_id": row.get("bridge_id", ""),
        "arena": row.get("arena", ""),
        "observable": row.get("observable", ""),
        "bridge_expression": row.get("bridge_expression", ""),
        "deltaJ_value": row.get("deltaJ_value", ""),
        "source_kernel_CJ": row.get("source_kernel_CJ", ""),
        "calibration_kernel_CJ": row.get("calibration_kernel_CJ", ""),
        "kernel_difference": kernel_difference,
        "predicted_residual_abs": residual,
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
    required = [
        "bridge_id",
        "arena",
        "observable",
        "bridge_expression",
        "deltaJ_value",
        "source_kernel_CJ",
        "calibration_kernel_CJ",
        "required_inputs",
        "assumptions_status",
        "source_bound_file",
        "source_row_id",
        "bound_column",
        "valid_for_claim",
    ]
    columns = set(rows[0].keys()) if rows else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        row.get("bridge_id", ""): Path(row.get("source_bound_path", "")).exists()
        for row in outputs
    }
    validations: list[dict[str, Any]] = [
        {
            "check_id": "VAL3121_0_input_schema",
            "status": "pass" if rows and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3121_1_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3121_2_missing_or_smoke_inputs_detected",
            "status": "pass" if any(("MISSING" in row.get("issues", "") or "SMOKE" in row.get("issues", "")) for row in outputs) else "fail",
            "details": json.dumps({row["bridge_id"]: row.get("issues", "") for row in outputs}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3121_3_source_paths_resolve",
            "status": "pass" if outputs and all(source_status.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3121_4_smoke_math_computed",
            "status": "pass" if any(row.get("bridge_id") == "DGB3121_7" and row.get("score") != "not_scoreable" for row in outputs) else "fail",
            "details": "numeric smoke row must compute but remain nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return validations


def main() -> None:
    rows = read_csv(INPUT)
    outputs = [evaluate_row(row) for row in rows]
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validate(rows, outputs))
    print(
        json.dumps(
            {
                "input_rows": len(rows),
                "output_rows": len(outputs),
                "output": str(OUTPUT),
                "validation": str(VALIDATION),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
