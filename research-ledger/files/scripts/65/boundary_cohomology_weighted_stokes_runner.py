from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


DOMAIN_CLAUSES = (
    "surface_manifold_signed",
    "boundary_class_signed",
    "relative_cohomology_signed",
    "epsilon_domain_signed",
    "kernel_weight_signed",
    "BX_primitive_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

STOKES_CLAUSES = (
    "decomposition_signed",
    "weighted_stokes_identity_signed",
    "corner_zero_or_bound_signed",
    "harmonic_zero_or_bound_signed",
    "residual_zero_or_bound_signed",
    "kernel_derivative_zero_or_bound_signed",
    "projector_bound_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "STOKES_ZERO_WITHOUT_WEIGHT",
    "DELETE_HARMONIC_BY_ASSUMPTION",
    "CORNER_SILENCE_BY_FIAT",
    "SYMBOLIC_BX_EXACT",
    "REFERENCE_ONLY_ZERO",
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
        for field in ("certificate_id", "theorem_id", "row_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def domain_certificate_row(row: dict[str, Any]) -> dict[str, Any]:
    certificate_id = str(row.get("certificate_id", "")).strip() or "UNNAMED_DOMAIN"
    output: dict[str, Any] = {"certificate_id": certificate_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"domain_status": "FAILED_DOMAIN_CERTIFICATE_GATE", "domain_theorem": False, "missing_domain_inputs": "FORBIDDEN_DOMAIN_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, DOMAIN_CLAUSES)
    status = "DOMAIN_CERTIFICATE_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_DOMAIN_CERTIFICATE_INPUTS"
    output.update({"domain_status": status, "domain_theorem": not missing, "missing_domain_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def weighted_stokes_row(row: dict[str, Any]) -> dict[str, Any]:
    theorem_id = str(row.get("theorem_id", "")).strip() or "UNNAMED_STOKES"
    output: dict[str, Any] = {"theorem_id": theorem_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"stokes_status": "FAILED_WEIGHTED_STOKES_GATE", "zero_theorem": False, "missing_stokes_inputs": "FORBIDDEN_STOKES_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, STOKES_CLAUSES)
    status = "WEIGHTED_STOKES_ZERO_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_WEIGHTED_STOKES_INPUTS"
    output.update({"stokes_status": status, "zero_theorem": not missing, "missing_stokes_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def edge_bound_values(row: dict[str, Any]) -> tuple[float | None, float | None, list[str]]:
    missing: list[str] = []
    c_corner = parse_float(row.get("C_corner_abs"))
    norm_weight = parse_float(row.get("norm_dS_Feps_abs"))
    norm_bx = parse_float(row.get("norm_bX_abs"))
    harmonic = parse_float(row.get("harmonic_edge_abs"))
    residual = parse_float(row.get("residual_edge_abs"))
    pim_norm = parse_float(row.get("PiM_norm_abs"))
    mh_ref = parse_float(row.get("M_H_ref_min_abs"))
    values = {
        "C_corner_abs": c_corner,
        "norm_dS_Feps_abs": norm_weight,
        "norm_bX_abs": norm_bx,
        "harmonic_edge_abs": harmonic,
        "residual_edge_abs": residual,
        "PiM_norm_abs": pim_norm,
        "M_H_ref_min_abs": mh_ref,
    }
    for name, value in values.items():
        if value is None or value < 0.0:
            missing.append(f"MISSING_{name}")
    if mh_ref is not None and mh_ref <= 0.0:
        missing.append("MISSING_POSITIVE_M_H_ref_min_abs")
    if missing:
        return None, None, missing
    q_edge = c_corner + norm_weight * norm_bx + harmonic + residual
    qbar = pim_norm * q_edge / mh_ref
    return q_edge, qbar, []


def edge_bound_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_EDGE_BOUND"
    output: dict[str, Any] = {"row_id": row_id, "quantity": row.get("quantity", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"Q_edge_bound_abs": "MISSING_NUMERIC_VALUE", "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "bound_status": "FAILED_EDGE_BOUND_GATE", "missing_bound_inputs": "FORBIDDEN_EDGE_BOUND_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    q_edge, qbar, missing = edge_bound_values(row)
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or qbar is None:
        output.update({"Q_edge_bound_abs": format_float(q_edge), "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "bound_status": "BLOCKED_MISSING_EDGE_BOUND_INPUTS", "missing_bound_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = qbar <= required
    status = "EDGE_BOUND_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "EDGE_BOUND_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "EDGE_BOUND_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"Q_edge_bound_abs": format_float(q_edge), "Qbar_edge_XH_bound_abs": format_float(qbar), "required_abs_max": format_float(required), "numeric_window_pass": passes, "bound_status": status, "missing_bound_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"domain", "stokes", "bound"}:
        print("Usage: boundary_cohomology_weighted_stokes_runner.py domain|stokes|bound INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    if sys.argv[1] == "domain":
        outputs = [domain_certificate_row(row) for row in rows]
    elif sys.argv[1] == "stokes":
        outputs = [weighted_stokes_row(row) for row in rows]
    else:
        outputs = [edge_bound_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
