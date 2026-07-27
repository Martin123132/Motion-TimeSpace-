from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

BOUND_REQUIRED_COLUMNS = [
    "bound_id",
    "dataset_id",
    "lambda_value",
    "lambda_units",
    "alpha_bound",
    "alpha_bound_source",
    "digitization_method",
    "source_file",
    "valid_for_claim",
    "notes",
]

UNIT_TO_METERS = {
    "m": 1.0,
    "meter": 1.0,
    "meters": 1.0,
    "km": 1.0e3,
    "cm": 1.0e-2,
    "mm": 1.0e-3,
    "um": 1.0e-6,
    "µm": 1.0e-6,
    "micron": 1.0e-6,
    "microns": 1.0e-6,
    "nm": 1.0e-9,
}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()}) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: str) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def parse_lambda_meters(value: str, units: str) -> float | None:
    numeric = parse_float(value)
    if numeric is None or numeric <= 0:
        return None
    multiplier = UNIT_TO_METERS.get(str(units).strip())
    if multiplier is None:
        return None
    return numeric * multiplier


def is_true(value: str) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, str]) -> bool:
    joined = json.dumps(row, sort_keys=True)
    return "MISSING" in joined or "fill_" in joined or "template_invalid" in joined


def validate_schema(rows: list[dict[str, str]], required_columns: list[str]) -> list[str]:
    if not rows:
        return ["file_has_no_rows"]
    columns = set(rows[0].keys())
    return [f"missing_column:{column}" for column in required_columns if column not in columns]


def validate_mts_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    schema_errors = validate_schema(rows, MTS_REQUIRED_COLUMNS)
    out: list[dict[str, Any]] = []
    if schema_errors:
        return [
            {
                "row_index": "schema",
                "curve_id": "",
                "lambda_m": "",
                "alpha_predicted": "",
                "valid_for_claim": "false",
                "validation_status": "invalid_schema",
                "issues": ";".join(schema_errors),
            }
        ]
    for index, row in enumerate(rows):
        lambda_m = parse_lambda_meters(row.get("lambda_value", ""), row.get("lambda_units", ""))
        alpha_predicted = parse_float(row.get("alpha_predicted", ""))
        issues: list[str] = []
        if lambda_m is None:
            issues.append("lambda_not_positive_numeric_or_units_unknown")
        if alpha_predicted is None:
            issues.append("alpha_predicted_not_numeric")
        if not is_true(row.get("valid_for_claim", "")):
            issues.append("valid_for_claim_not_true")
        if has_missing_marker(row):
            issues.append("placeholder_or_missing_marker_present")
        source_file = row.get("source_file", "")
        if is_true(row.get("valid_for_claim", "")) and source_file and source_file != "MISSING_SOURCE_FILE":
            if not (ROOT / source_file).exists():
                issues.append("claim_source_file_missing")
        out.append(
            {
                "row_index": index,
                "curve_id": row.get("curve_id", ""),
                "branch_id": row.get("branch_id", ""),
                "lambda_m": lambda_m if lambda_m is not None else "",
                "alpha_predicted": alpha_predicted if alpha_predicted is not None else "",
                "valid_for_claim": row.get("valid_for_claim", ""),
                "validation_status": "valid" if not issues else "invalid",
                "issues": ";".join(issues),
            }
        )
    return out


def validate_bound_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    schema_errors = validate_schema(rows, BOUND_REQUIRED_COLUMNS)
    out: list[dict[str, Any]] = []
    if schema_errors:
        return [
            {
                "row_index": "schema",
                "bound_id": "",
                "lambda_m": "",
                "alpha_bound": "",
                "valid_for_claim": "false",
                "validation_status": "invalid_schema",
                "issues": ";".join(schema_errors),
            }
        ]
    for index, row in enumerate(rows):
        lambda_m = parse_lambda_meters(row.get("lambda_value", ""), row.get("lambda_units", ""))
        alpha_bound = parse_float(row.get("alpha_bound", ""))
        issues: list[str] = []
        if lambda_m is None:
            issues.append("lambda_not_positive_numeric_or_units_unknown")
        if alpha_bound is None or (alpha_bound is not None and alpha_bound <= 0):
            issues.append("alpha_bound_not_positive_numeric")
        if not is_true(row.get("valid_for_claim", "")):
            issues.append("valid_for_claim_not_true")
        if has_missing_marker(row):
            issues.append("placeholder_or_missing_marker_present")
        source_file = row.get("source_file", "")
        if is_true(row.get("valid_for_claim", "")) and source_file and source_file != "MISSING_SOURCE_FILE":
            if not (ROOT / source_file).exists() and not source_file.startswith(("http://", "https://")):
                issues.append("claim_source_file_missing")
        out.append(
            {
                "row_index": index,
                "bound_id": row.get("bound_id", ""),
                "dataset_id": row.get("dataset_id", ""),
                "lambda_m": lambda_m if lambda_m is not None else "",
                "alpha_bound": alpha_bound if alpha_bound is not None else "",
                "valid_for_claim": row.get("valid_for_claim", ""),
                "validation_status": "valid" if not issues else "invalid",
                "issues": ";".join(issues),
            }
        )
    return out


def interpolate_bound(lambda_m: float, valid_bounds: list[dict[str, Any]]) -> tuple[float | None, str]:
    points = sorted(
        (
            (float(row["lambda_m"]), float(row["alpha_bound"]), row["bound_id"])
            for row in valid_bounds
            if row.get("validation_status") == "valid"
        ),
        key=lambda item: item[0],
    )
    if not points:
        return None, "no_valid_bound_rows"
    for point_lambda, point_alpha, bound_id in points:
        if math.isclose(lambda_m, point_lambda, rel_tol=1e-12, abs_tol=0.0):
            return point_alpha, f"exact:{bound_id}"
    if lambda_m < points[0][0] or lambda_m > points[-1][0]:
        return None, "lambda_outside_bound_range"
    for left, right in zip(points, points[1:]):
        left_lambda, left_alpha, left_id = left
        right_lambda, right_alpha, right_id = right
        if left_lambda <= lambda_m <= right_lambda:
            if left_alpha <= 0 or right_alpha <= 0:
                return None, "nonpositive_bound_blocks_log_interpolation"
            t = (math.log(lambda_m) - math.log(left_lambda)) / (math.log(right_lambda) - math.log(left_lambda))
            log_alpha = math.log(left_alpha) + t * (math.log(right_alpha) - math.log(left_alpha))
            return math.exp(log_alpha), f"log_interp:{left_id}->{right_id}"
    return None, "interpolation_failed"


def compare_curves(
    mts_validation: list[dict[str, Any]],
    bound_validation: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    valid_mts = [row for row in mts_validation if row.get("validation_status") == "valid"]
    valid_bounds = [row for row in bound_validation if row.get("validation_status") == "valid"]
    if not valid_mts:
        return [
            {
                "comparison_id": "R10_COMPARE_NO_VALID_MTS_ROWS",
                "lambda_m": "",
                "alpha_predicted": "",
                "alpha_bound": "",
                "comparison_status": "not_run",
                "pass_for_claim": "false",
                "issues": "no valid MTS alpha(lambda) rows",
            }
        ]
    if not valid_bounds:
        return [
            {
                "comparison_id": "R10_COMPARE_NO_VALID_BOUND_ROWS",
                "lambda_m": "",
                "alpha_predicted": "",
                "alpha_bound": "",
                "comparison_status": "not_run",
                "pass_for_claim": "false",
                "issues": "no valid bound alpha(lambda) rows",
            }
        ]
    rows: list[dict[str, Any]] = []
    for index, mts_row in enumerate(valid_mts):
        lambda_m = float(mts_row["lambda_m"])
        alpha_predicted = abs(float(mts_row["alpha_predicted"]))
        alpha_bound, bound_method = interpolate_bound(lambda_m, valid_bounds)
        if alpha_bound is None:
            rows.append(
                {
                    "comparison_id": f"R10_COMPARE_{index}",
                    "lambda_m": lambda_m,
                    "alpha_predicted": alpha_predicted,
                    "alpha_bound": "",
                    "bound_method": bound_method,
                    "comparison_status": "not_comparable",
                    "pass_for_claim": "false",
                    "issues": bound_method,
                }
            )
            continue
        rows.append(
            {
                "comparison_id": f"R10_COMPARE_{index}",
                "lambda_m": lambda_m,
                "alpha_predicted": alpha_predicted,
                "alpha_bound": alpha_bound,
                "bound_method": bound_method,
                "comparison_status": "pass" if alpha_predicted <= alpha_bound else "fail",
                "pass_for_claim": "true" if alpha_predicted <= alpha_bound else "false",
                "issues": "" if alpha_predicted <= alpha_bound else "alpha_predicted_exceeds_bound",
            }
        )
    return rows


def run_runner(mts_curve: Path, bound_curve: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    mts_rows = read_csv(mts_curve)
    bound_rows = read_csv(bound_curve)
    mts_validation = validate_mts_rows(mts_rows)
    bound_validation = validate_bound_rows(bound_rows)
    comparisons = compare_curves(mts_validation, bound_validation)
    passed_rows = [row for row in comparisons if row.get("pass_for_claim") == "true"]
    failed_or_blocked_rows = [row for row in comparisons if row.get("pass_for_claim") != "true"]
    all_claim_ready = bool(comparisons) and bool(passed_rows) and not failed_or_blocked_rows
    write_csv(output_dir / "R10_runner_mts_validation.csv", mts_validation)
    write_csv(output_dir / "R10_runner_bound_validation.csv", bound_validation)
    write_csv(output_dir / "R10_runner_comparison.csv", comparisons)
    status = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mts_curve": rel(mts_curve),
        "bound_curve": rel(bound_curve),
        "output_dir": rel(output_dir),
        "mts_rows": len(mts_rows),
        "bound_rows": len(bound_rows),
        "valid_mts_rows": len([row for row in mts_validation if row.get("validation_status") == "valid"]),
        "valid_bound_rows": len([row for row in bound_validation if row.get("validation_status") == "valid"]),
        "comparison_rows": len(comparisons),
        "passed_rows": len(passed_rows),
        "blocked_or_failed_rows": len(failed_or_blocked_rows),
        "R10_pass_for_claim": all_claim_ready,
        "claim_allowed": all_claim_ready,
    }
    (output_dir / "R10_runner_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return {
        "status": status,
        "mts_validation": mts_validation,
        "bound_validation": bound_validation,
        "comparisons": comparisons,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mts-curve",
        default=str(ROOT / "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv"),
    )
    parser.add_argument(
        "--bound-curve",
        default=str(ROOT / "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv"),
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "runs" / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-R10-alpha-lambda-bound-prediction-runner" / "results"),
    )
    args = parser.parse_args()
    result = run_runner(Path(args.mts_curve), Path(args.bound_curve), Path(args.output_dir))
    print(json.dumps(result["status"], indent=2))


if __name__ == "__main__":
    main()
