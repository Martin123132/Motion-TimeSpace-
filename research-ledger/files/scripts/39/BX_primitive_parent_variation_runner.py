from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


TEMPLATE_CLAUSES = (
    "parent_LX_signed",
    "Theta_X_signed",
    "Q_X_signed",
    "P_X_signed",
    "B_ct_signed",
    "same_parent_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PRIMITIVE_CLAUSES = (
    "same_parent_origin_signed",
    "counterterm_owner_signed",
    "exact_surface_pullback_signed",
    "harmonic_zero_or_bound_signed",
    "kernel_norm_zero_or_bound_signed",
    "overlap_compatibility_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SCALAR_CLAUSES = (
    "Z_X_positive_signed",
    "M_X2_positive_signed",
    "J_X_zero_signed",
    "boundary_flux_zero_signed",
    "matter_coupling_zero_signed",
    "nohair_domain_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FILL_TERMS = (
    "norm_bX_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "norm_dS_Feps_abs",
    "C_corner_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "SYMBOLIC_BX_EXACT",
    "SCALAR_NOHAIR_AS_EDGE_PRIMITIVE",
    "SOURCE_FREE_BY_ASSERTION",
    "COUNTERTERM_BY_READOUT",
    "DELETE_HARMONIC_BY_ASSUMPTION",
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
    source_text = " ".join(
        str(row.get(field, ""))
        for field in ("template_id", "gate_id", "branch_id", "fill_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


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


def parent_template_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "template_id", "template_status", "template_theorem", "missing_template_inputs", TEMPLATE_CLAUSES, "FAILED_PARENT_TEMPLATE_GATE", "BLOCKED_MISSING_PARENT_VARIATION_INPUTS", "PARENT_VARIATION_TEMPLATE_SIGNED_CONDITIONAL_NONCLAIM")


def primitive_gate_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "gate_id", "primitive_status", "primitive_theorem", "missing_primitive_inputs", PRIMITIVE_CLAUSES, "FAILED_BX_PRIMITIVE_GATE", "BLOCKED_MISSING_BX_PRIMITIVE_INPUTS", "BX_PRIMITIVE_SIGNED_CONDITIONAL_NONCLAIM")


def scalar_branch_row(row: dict[str, Any]) -> dict[str, Any]:
    return clause_row(row, "branch_id", "scalar_status", "scalar_theorem", "missing_scalar_inputs", SCALAR_CLAUSES, "FAILED_SCALAR_BRANCH_GATE", "BLOCKED_MISSING_SCALAR_NOHAIR_INPUTS", "SCALAR_NOHAIR_SIGNED_CONDITIONAL_NONCLAIM")


def fill_values(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    missing: list[str] = []
    values: list[float] = []
    for term in FILL_TERMS:
        value = parse_float(row.get(term))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{term}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def edge_fill_row(row: dict[str, Any]) -> dict[str, Any]:
    fill_id = str(row.get("fill_id", "")).strip() or "UNNAMED_EDGE_FILL"
    output: dict[str, Any] = {"fill_id": fill_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"edge_fill_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "fill_status": "FAILED_EDGE_FILL_GATE", "missing_fill_inputs": "FORBIDDEN_EDGE_FILL_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    value, missing = fill_values(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"edge_fill_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "fill_status": "BLOCKED_MISSING_EDGE_FILL_INPUTS", "missing_fill_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "EDGE_FILL_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "EDGE_FILL_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "EDGE_FILL_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"edge_fill_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "fill_status": status, "missing_fill_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"template", "primitive", "scalar", "fill"}:
        print("Usage: BX_primitive_parent_variation_runner.py template|primitive|scalar|fill INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "template":
        outputs = [parent_template_row(row) for row in rows]
    elif mode == "primitive":
        outputs = [primitive_gate_row(row) for row in rows]
    elif mode == "scalar":
        outputs = [scalar_branch_row(row) for row in rows]
    else:
        outputs = [edge_fill_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
