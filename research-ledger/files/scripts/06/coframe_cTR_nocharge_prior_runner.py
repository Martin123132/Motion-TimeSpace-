from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


NOCHARGE_CLAUSES = (
    "gauss_law_signed",
    "bulk_source_neutrality_signed",
    "boundary_charge_zero_signed",
    "counterterm_zero_signed",
    "same_matter_coframe_signed",
    "no_hidden_clock_or_source_reentry_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "OBSERVED_RESIDUAL_CANCEL",
    "CTR_BY_DECLARATION",
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


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(str(row.get(field, "")) for field in ("nocharge_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in NOCHARGE_CLAUSES if not bool_text(row.get(clause))]


def nocharge_row(row: dict[str, Any]) -> dict[str, Any]:
    nocharge_id = str(row.get("nocharge_id", "")).strip() or "UNNAMED_NOCHARGE"
    output: dict[str, Any] = {
        "nocharge_id": nocharge_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "Q_ext_bound_abs": "MISSING_NUMERIC_VALUE",
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "nocharge_theorem": False,
                "runner_status": "FAILED_CTR_NOCHARGE_GATE",
                "missing_nocharge_inputs": "FORBIDDEN_NOCHARGE_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    missing = missing_clauses(row)
    fields = ("Q_bulk_abs", "Q_boundary_abs", "Q_counterterm_abs", "Q_reentry_abs")
    values: dict[str, float] = {}
    numeric_missing: list[str] = []
    for field in fields:
        value = parse_float(row.get(field))
        if value is None or value < 0.0:
            numeric_missing.append(f"MISSING_{field}")
        else:
            values[field] = value

    if numeric_missing:
        output.update(
            {
                "Q_ext_bound_abs": "MISSING_NUMERIC_VALUE",
                "cTR_bound_abs": "MISSING_NUMERIC_VALUE",
                "nocharge_theorem": False,
                "runner_status": "BLOCKED_MISSING_CTR_NOCHARGE_INPUTS",
                "missing_nocharge_inputs": ";".join([*missing, *numeric_missing]),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    q_bound = values["Q_bulk_abs"] + values["Q_boundary_abs"] + values["Q_counterterm_abs"] + values["Q_reentry_abs"]
    if not missing and q_bound <= 1.0e-15:
        status = "CTR_GAUSS_NOCHARGE_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif q_bound <= 1.0e-15:
        status = "CTR_GAUSS_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "CTR_GAUSS_FINITE_HAIR_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "Q_ext_bound_abs": format_float(q_bound),
            "cTR_bound_abs": format_float(q_bound),
            "nocharge_theorem": theorem,
            "runner_status": status,
            "missing_nocharge_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_CTR_PRIOR"
    output: dict[str, Any] = {
        "prior_id": prior_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "cTR_abs_value": "MISSING_NUMERIC_VALUE",
                "required_abs_max": row.get("required_abs_max", ""),
                "numeric_window_pass": False,
                "runner_status": "FAILED_CTR_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_CTR_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    required = parse_float(row.get("required_abs_max"))
    value = parse_float(row.get("cTR_abs_value"))
    source_signed = bool_text(row.get("source_signed"))
    theorem_zero = bool_text(row.get("theorem_zero_signed"))
    source_path = str(row.get("source_path", "")).strip()
    equation_ref = str(row.get("equation_ref", "")).strip()
    missing: list[str] = []
    if required is None or required < 0.0:
        missing.append("MISSING_required_abs_max")

    if theorem_zero and required is not None:
        output.update(
            {
                "cTR_abs_value": "0.000000000000000e+00",
                "required_abs_max": format_float(required),
                "numeric_window_pass": True,
                "runner_status": "CTR_THEOREM_ZERO_CONDITIONAL_NONCLAIM",
                "missing_prior_inputs": "",
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    if value is None:
        missing.append("MISSING_cTR_abs_value")
    if not source_signed:
        missing.append("MISSING_source_signed")
    if not source_path:
        missing.append("MISSING_source_path")
    if not equation_ref:
        missing.append("MISSING_equation_ref")

    if value is None or required is None:
        output.update(
            {
                "cTR_abs_value": format_float(value),
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_CTR_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output

    numeric_pass = abs(value) <= abs(required)
    if numeric_pass and missing:
        status = "CTR_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    elif numeric_pass:
        status = "CTR_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM_UNLESS_INPUT_VALID"
    else:
        status = "CTR_PRIOR_NUMERIC_WINDOW_FAIL"
    output.update(
        {
            "cTR_abs_value": format_float(abs(value)),
            "required_abs_max": format_float(abs(required)),
            "numeric_window_pass": numeric_pass,
            "runner_status": status,
            "missing_prior_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            "claim_allowed": bool_text(row.get("valid_for_claim")) and not missing and numeric_pass,
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: coframe_cTR_nocharge_prior_runner.py <nocharge|prior> <input.csv> <output.csv>", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    if mode == "nocharge":
        rows = [nocharge_row(row) for row in read_csv(Path(sys.argv[2]))]
    elif mode == "prior":
        rows = [prior_row(row) for row in read_csv(Path(sys.argv[2]))]
    else:
        raise ValueError(f"unknown mode: {mode}")
    write_csv(Path(sys.argv[3]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
