from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


BRANCH_CLAUSES = (
    "branch_separated_signed",
    "quotient_attempt_selected_signed",
    "scalar_demoted_to_fallback_signed",
    "source_residual_last_resort_signed",
    "no_route_mixing_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

VERTICAL_CLAUSES = (
    "q_map_signed",
    "action_descent_signed",
    "matter_descent_signed",
    "vertical_generator_signed",
    "momentum_map_signed",
    "boundary_silence_signed",
    "degree_count_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "operator_self_adjoint_signed",
    "Z_positive_signed",
    "M2_positive_signed",
    "J_zero_signed",
    "boundary_flux_zero_signed",
    "energy_identity_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FALLBACK_TERMS = (
    "quotient_certificate_abs",
    "scalar_operator_abs",
    "sourced_alpha_abs",
    "edge_bound_abs",
    "total_guard_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_QUOTIENT",
    "SCALAR_NOHAIR_AS_EDGE_EXACTNESS",
    "SOURCE_FREE_BY_ASSERTION",
    "CANCEL_UNKNOWN_COMPONENTS",
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
    text = " ".join(str(row.get(field, "")) for field in ("branch_id", "clause_id", "row_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def clause_row(row: dict[str, Any], id_field: str, status_field: str, theorem_field: str, missing_field: str, clauses: tuple[str, ...], fail_status: str, blocked_status: str, signed_status: str) -> dict[str, Any]:
    row_id = str(row.get(id_field, "")).strip() or f"UNNAMED_{id_field.upper()}"
    output: dict[str, Any] = {id_field: row_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({status_field: fail_status, theorem_field: False, missing_field: "FORBIDDEN_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, clauses)
    status = signed_status if not missing else blocked_status
    output.update({status_field: status, theorem_field: not missing, missing_field: ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def branch_decision_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "branch_id", "branch_status", "branch_theorem", "missing_branch_inputs", BRANCH_CLAUSES, "FAILED_BRANCH_CHOICE_GATE", "BLOCKED_MISSING_BRANCH_CHOICE_INPUTS", "BRANCH_CHOICE_SIGNED_NONCLAIM")


def vertical_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "clause_id", "vertical_status", "vertical_theorem", "missing_vertical_inputs", VERTICAL_CLAUSES, "FAILED_VERTICAL_QUOTIENT_GATE", "BLOCKED_MISSING_VERTICAL_QUOTIENT_INPUTS", "VERTICAL_QUOTIENT_SIGNED_CONDITIONAL_NONCLAIM")


def scalar_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "clause_id", "scalar_status", "scalar_theorem", "missing_scalar_inputs", SCALAR_CLAUSES, "FAILED_SCALAR_NOHAIR_GATE", "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "SCALAR_NOHAIR_SIGNED_CONDITIONAL_NONCLAIM")


def fallback_value(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for term in FALLBACK_TERMS:
        value = parse_float(row.get(term))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{term}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def fallback_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_FALLBACK"
    output: dict[str, Any] = {"row_id": row_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"fallback_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "fallback_status": "FAILED_FALLBACK_SOURCE_GATE", "missing_fallback_inputs": "FORBIDDEN_FALLBACK_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    value, missing = fallback_value(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"fallback_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "fallback_status": "BLOCKED_MISSING_FALLBACK_SOURCE_INPUTS", "missing_fallback_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "FALLBACK_SOURCE_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "FALLBACK_SOURCE_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "FALLBACK_SOURCE_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"fallback_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "fallback_status": status, "missing_fallback_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({field for row in rows for field in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"branch", "vertical", "scalar", "fallback"}:
        print("Usage: vertical_quotient_scalar_branch_choice_runner.py branch|vertical|scalar|fallback INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "branch":
        outputs = [branch_decision_row(row) for row in rows]
    elif mode == "vertical":
        outputs = [vertical_clause_row(row) for row in rows]
    elif mode == "scalar":
        outputs = [scalar_clause_row(row) for row in rows]
    else:
        outputs = [fallback_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
