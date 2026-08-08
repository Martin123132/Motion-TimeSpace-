from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


OWNER_CLAUSES = (
    "LX_parent_owned_signed",
    "Theta_QX_variation_signed",
    "omega_integrability_signed",
    "quotient_or_constraint_route_signed",
    "B_ref_fixed_signed",
    "B_class_boundary_silence_signed",
    "tau_functor_signed",
    "M_H_ref_owner_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "delta_H_tau_nonintegrable_abs",
    "Delta_ref_abs",
    "symplectic_boundary_flux_abs",
    "B_zero_flux_abs",
    "Delta_tau_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "BARE_MASS_SHORTCUT",
    "NEWTON_G_AS_INPUT",
    "CANCEL_UNKNOWN_COMPONENTS",
    "SYMBOLIC_LX_ONLY",
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
        for field in ("owner_id", "route_id", "row_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_owner_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in OWNER_CLAUSES if not bool_text(row.get(clause))]


def component_guard(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in SOURCE_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    mh_ref = parse_float(row.get("M_H_ref_abs"))
    if mh_ref is None or mh_ref <= 0.0:
        missing.append("MISSING_M_H_ref_abs")
    if missing:
        return None, missing
    return sum(values) / mh_ref, []


def owner_clause_row(row: dict[str, Any]) -> dict[str, Any]:
    owner_id = str(row.get("owner_id", "")).strip() or "UNNAMED_OWNER_ROW"
    output: dict[str, Any] = {
        "owner_id": owner_id,
        "owner_target": row.get("owner_target", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "owner_gate_status": "FAILED_OWNER_GATE",
                "owner_theorem": False,
                "missing_owner_inputs": "FORBIDDEN_OWNER_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    missing = missing_owner_clauses(row)
    if missing:
        status = "BLOCKED_MISSING_OWNER_SIGNATURES"
        theorem = False
    else:
        status = "OWNER_ROUTE_SIGNED_CONDITIONAL_NONCLAIM"
        theorem = True
    output.update(
        {
            "owner_gate_status": status,
            "owner_theorem": theorem,
            "missing_owner_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def route_test_row(row: dict[str, Any]) -> dict[str, Any]:
    route_id = str(row.get("route_id", "")).strip() or "UNNAMED_ROUTE"
    output: dict[str, Any] = {
        "route_id": route_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "route_status": "FAILED_ROUTE_GATE",
                "route_theorem": False,
                "missing_route_inputs": "FORBIDDEN_ROUTE_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = [field.strip() for field in str(row.get("required_signatures", "")).split(";") if field.strip()]
    missing = [field for field in required if not bool_text(row.get(field))]
    if missing:
        status = "ROUTE_BLOCKED_MISSING_SIGNATURES"
        theorem = False
    else:
        status = "ROUTE_SIGNED_CONDITIONAL_NONCLAIM"
        theorem = True
    output.update(
        {
            "route_status": status,
            "route_theorem": theorem,
            "missing_route_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def source_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_FB5540_ROW"
    output: dict[str, Any] = {
        "row_id": row_id,
        "component_expr": row.get("component_expr", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "FB5540_guard_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "source_row_status": "FAILED_FB5540_SOURCE_ROW_GATE",
                "missing_source_inputs": "FORBIDDEN_SOURCE_ROW",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("FB5540_guard_abs"))
    computed_value, computed_missing = component_guard(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_FB5540_guard_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "FB5540_guard_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "source_row_status": "BLOCKED_MISSING_FB5540_SOURCE_INPUTS",
                "missing_source_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    status = "FB5540_SOURCE_ROW_NUMERIC_WINDOW_FAIL"
    if passes:
        status = (
            "FB5540_SOURCE_ROW_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
            if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim"))
            else "FB5540_SOURCE_ROW_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        )
    output.update(
        {
            "FB5540_guard_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "source_row_status": status,
            "missing_source_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"owner", "route", "source"}:
        print("Usage: sector_Lagrangian_boundary_owner_runner.py owner|route|source INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    rows = read_csv(Path(sys.argv[2]))
    if mode == "owner":
        outputs = [owner_clause_row(row) for row in rows]
    elif mode == "route":
        outputs = [route_test_row(row) for row in rows]
    else:
        outputs = [source_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
