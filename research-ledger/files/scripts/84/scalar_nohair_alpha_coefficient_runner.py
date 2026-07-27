from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "SOURCE_FREE_BY_ASSERTION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "SCALAR_NOHAIR_AS_EDGE_EXACTNESS",
)

NUMERIC_FIELDS = (
    "Z_X",
    "M_X2",
    "J_X_abs",
    "boundary_flux_abs",
    "K_X",
    "Qbar_XH",
    "qbar_XT",
    "alpha_edge_abs",
    "FB5540_abs",
    "alpha_R11_abs",
    "alpha_bound",
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


def missing_numeric(row: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None:
            missing.append(f"MISSING_{field}")
    return missing


def scalar_missing(row: dict[str, Any]) -> list[str]:
    missing = missing_numeric(row, ("Z_X", "M_X2", "J_X_abs", "boundary_flux_abs"))
    z_value = parse_float(row.get("Z_X"))
    m_value = parse_float(row.get("M_X2"))
    j_value = parse_float(row.get("J_X_abs"))
    b_value = parse_float(row.get("boundary_flux_abs"))
    if z_value is not None and z_value <= 0.0:
        missing.append("NONPOSITIVE_Z_X")
    if m_value is not None and m_value <= 0.0:
        missing.append("NONPOSITIVE_M_X2")
    if j_value is not None and abs(j_value) > 0.0:
        missing.append("NONZERO_J_X")
    if b_value is not None and abs(b_value) > 0.0:
        missing.append("NONZERO_BOUNDARY_FLUX")
    if not bool_text(row.get("operator_domain_signed")):
        missing.append("MISSING_OPERATOR_DOMAIN")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_SOURCE_SIGNED")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_SOURCE_PATH")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_EQUATION_REF")
    return missing


def alpha_missing(row: dict[str, Any]) -> list[str]:
    missing = missing_numeric(row, ("K_X", "Qbar_XH", "qbar_XT", "alpha_edge_abs", "FB5540_abs", "alpha_R11_abs", "alpha_bound"))
    alpha_bound = parse_float(row.get("alpha_bound"))
    if alpha_bound is not None and alpha_bound <= 0.0:
        missing.append("NONPOSITIVE_ALPHA_BOUND")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_SOURCE_SIGNED")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_SOURCE_PATH")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_EQUATION_REF")
    return missing


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_ALPHA_ROW"
    output: dict[str, Any] = {
        "row_id": row_id,
        "branch": row.get("branch", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "lambda_X": "MISSING_NUMERIC_VALUE",
                "alpha_bulk_abs": "MISSING_NUMERIC_VALUE",
                "alpha_total_guard": "MISSING_NUMERIC_VALUE",
                "scalar_nohair_pass": False,
                "alpha_bound_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    z_value = parse_float(row.get("Z_X"))
    m_value = parse_float(row.get("M_X2"))
    lambda_value = math.sqrt(z_value / m_value) if z_value is not None and m_value is not None and z_value > 0.0 and m_value > 0.0 else None
    scalar_blockers = scalar_missing(row)
    scalar_pass = not scalar_blockers

    k_value = parse_float(row.get("K_X"))
    qh_value = parse_float(row.get("Qbar_XH"))
    qt_value = parse_float(row.get("qbar_XT"))
    edge_value = parse_float(row.get("alpha_edge_abs"))
    fb_value = parse_float(row.get("FB5540_abs"))
    r11_value = parse_float(row.get("alpha_R11_abs"))
    bound_value = parse_float(row.get("alpha_bound"))
    alpha_blockers = alpha_missing(row)
    alpha_bulk = abs(k_value * qh_value * qt_value) if k_value is not None and qh_value is not None and qt_value is not None else None
    alpha_total = None
    if alpha_bulk is not None and edge_value is not None and fb_value is not None and r11_value is not None:
        alpha_total = alpha_bulk + abs(edge_value) + abs(fb_value) + abs(r11_value)
    alpha_pass = bool(alpha_total is not None and bound_value is not None and alpha_total <= bound_value and not alpha_blockers)

    if scalar_pass:
        status = "SCALAR_NOHAIR_CONDITIONAL_PASS_NONCLAIM"
        missing = ""
    elif not alpha_blockers and alpha_total is not None and bound_value is not None:
        if alpha_pass:
            status = "ALPHA_GUARD_NUMERIC_PASS_NONCLAIM"
            missing = ""
        else:
            status = "ALPHA_GUARD_NUMERIC_FAIL"
            missing = "ALPHA_TOTAL_EXCEEDS_BOUND"
    else:
        missing_items = list(dict.fromkeys(scalar_blockers + alpha_blockers))
        status = "BLOCKED_MISSING_SCALAR_OR_ALPHA_INPUTS"
        missing = ";".join(missing_items)

    output.update(
        {
            "lambda_X": fmt(lambda_value),
            "alpha_bulk_abs": fmt(alpha_bulk),
            "alpha_total_guard": fmt(alpha_total),
            "scalar_nohair_pass": scalar_pass,
            "alpha_bound_pass": alpha_pass,
            "runner_status": status,
            "missing_for_claim": missing,
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
        print("Usage: scalar_nohair_alpha_coefficient_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
