from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_TOKENS = (
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "R10_ANCHOR_AS_PARENT",
    "ORBITAL_GM_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "GR_IMPORT",
)

REQUIRED_NUMERIC_FIELDS = (
    "F1_abs",
    "F1_tol",
    "Z_raw",
    "M2_raw",
    "Z_cross_norm",
    "M2_cross_norm",
    "Z_aux_min",
    "M2_aux_min",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def missing_text(value: Any) -> bool:
    text = str(value or "").strip()
    return not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE", "NOT_COMPUTED"}


def parse_float(value: Any) -> float | None:
    if missing_text(value):
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def fmt(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in (
            "row_id",
            "branch",
            "source_path",
            "equation_ref",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_numeric(row: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_NUMERIC_FIELDS:
        if parse_float(row.get(field)) is None:
            missing.append(f"MISSING_{field}")
    return missing


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_HESSIAN_ROW"
    output: dict[str, Any] = {
        "row_id": row_id,
        "branch": row.get("branch", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Z_eff_min": "MISSING_NUMERIC_VALUE",
                "M2_eff_min": "MISSING_NUMERIC_VALUE",
                "lambda_eff": "MISSING_NUMERIC_VALUE",
                "branch_extremum_pass": False,
                "positive_hessian_pass": False,
                "range_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_numeric(row)
    source_signed = bool_text(row.get("source_signed"))
    same_branch = bool_text(row.get("same_branch_signed"))
    units_signed = bool_text(row.get("units_signed"))
    domain_signed = bool_text(row.get("domain_signed"))
    if not source_signed:
        missing.append("MISSING_SOURCE_SIGNED")
    if not same_branch:
        missing.append("MISSING_SAME_BRANCH_LOCK")
    if not units_signed:
        missing.append("MISSING_UNITS_SIGNED")
    if not domain_signed:
        missing.append("MISSING_DOMAIN_SIGNED")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_SOURCE_PATH")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_EQUATION_REF")

    f1_abs = parse_float(row.get("F1_abs"))
    f1_tol = parse_float(row.get("F1_tol"))
    z_raw = parse_float(row.get("Z_raw"))
    m2_raw = parse_float(row.get("M2_raw"))
    z_cross = parse_float(row.get("Z_cross_norm"))
    m2_cross = parse_float(row.get("M2_cross_norm"))
    z_aux = parse_float(row.get("Z_aux_min"))
    m2_aux = parse_float(row.get("M2_aux_min"))

    branch_extremum = bool(
        f1_abs is not None
        and f1_tol is not None
        and f1_tol >= 0.0
        and f1_abs <= f1_tol
    )
    if z_aux is not None and z_aux <= 0.0:
        missing.append("NONPOSITIVE_Z_AUX_MIN")
    if m2_aux is not None and m2_aux <= 0.0:
        missing.append("NONPOSITIVE_M2_AUX_MIN")

    z_eff = None
    m2_eff = None
    if z_raw is not None and z_cross is not None and z_aux is not None and z_aux > 0.0:
        z_eff = z_raw - (z_cross * z_cross) / z_aux
    if m2_raw is not None and m2_cross is not None and m2_aux is not None and m2_aux > 0.0:
        m2_eff = m2_raw - (m2_cross * m2_cross) / m2_aux
    if z_eff is not None and z_eff <= 0.0:
        missing.append("NONPOSITIVE_Z_EFF_MIN")
    if m2_eff is not None and m2_eff <= 0.0:
        missing.append("NONPOSITIVE_M2_EFF_MIN")
    if not branch_extremum:
        missing.append("BRANCH_EXTREMUM_NOT_PROVED")

    positive_hessian = bool(
        z_eff is not None
        and m2_eff is not None
        and z_eff > 0.0
        and m2_eff > 0.0
        and branch_extremum
        and source_signed
        and same_branch
        and units_signed
        and domain_signed
    )
    lambda_eff = math.sqrt(z_eff / m2_eff) if positive_hessian else None

    if positive_hessian:
        status = "PARENT_HESSIAN_RANGE_PASS_NONCLAIM"
        missing_for_claim = ""
    elif missing:
        status = "BLOCKED_MISSING_PARENT_HESSIAN_INPUTS"
        missing_for_claim = ";".join(dict.fromkeys(missing))
    else:
        status = "PARENT_HESSIAN_RANGE_FAIL"
        missing_for_claim = "SCHUR_COMPLEMENT_NOT_POSITIVE"

    output.update(
        {
            "Z_eff_min": fmt(z_eff),
            "M2_eff_min": fmt(m2_eff),
            "lambda_eff": fmt(lambda_eff),
            "branch_extremum_pass": branch_extremum,
            "positive_hessian_pass": positive_hessian,
            "range_pass": positive_hessian,
            "runner_status": status,
            "missing_for_claim": missing_for_claim,
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: parent_hessian_zx_mx2_range_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
