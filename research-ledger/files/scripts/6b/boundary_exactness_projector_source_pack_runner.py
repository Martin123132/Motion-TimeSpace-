from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


EXACTNESS_CLAUSES = (
    "boundary_domain_signed",
    "BX_exact_signed",
    "Stokes_kernel_silent_signed",
    "proper_gauge_signed",
    "counterterm_signed",
    "cocycle_zero_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

PROJECTOR_CLAUSES = (
    "PiM_definition_signed",
    "edge_mass_independence_signed",
    "symplectic_block_signed",
    "reference_silence_signed",
    "tau_frame_lock_signed",
    "source_measure_lock_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_COMPONENTS = (
    "FB5540_abs",
    "bulk_X_abs",
    "edge_X_abs",
    "R11_abs",
    "projector_edge_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "REFERENCE_ONLY_ZERO",
    "SYMBOLIC_EDGE_ZERO",
    "CANCEL_UNKNOWN_COMPONENTS",
    "DELETE_EDGE_BY_DOMAIN_FIAT",
    "POST_READOUT_PROJECTOR",
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
        for field in ("clause_id", "projector_id", "pack_id", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any], clauses: tuple[str, ...]) -> list[str]:
    return [clause for clause in clauses if not bool_text(row.get(clause))]


def source_guard(row: dict[str, Any]) -> tuple[float | None, list[str]]:
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


def exactness_row(row: dict[str, Any]) -> dict[str, Any]:
    clause_id = str(row.get("clause_id", "")).strip() or "UNNAMED_EXACTNESS"
    output: dict[str, Any] = {"clause_id": clause_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"exactness_status": "FAILED_EXACTNESS_GATE", "exactness_theorem": False, "missing_exactness_inputs": "FORBIDDEN_EXACTNESS_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, EXACTNESS_CLAUSES)
    status = "BOUNDARY_EXACTNESS_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_BOUNDARY_EXACTNESS_INPUTS"
    output.update({"exactness_status": status, "exactness_theorem": not missing, "missing_exactness_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def projector_row(row: dict[str, Any]) -> dict[str, Any]:
    projector_id = str(row.get("projector_id", "")).strip() or "UNNAMED_PROJECTOR"
    output: dict[str, Any] = {"projector_id": projector_id, "route": row.get("route", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"projector_status": "FAILED_PROJECTOR_GATE", "projector_theorem": False, "missing_projector_inputs": "FORBIDDEN_PROJECTOR_SOURCE", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    missing = missing_clauses(row, PROJECTOR_CLAUSES)
    status = "PROJECTOR_ORTHOGONALITY_SIGNED_CONDITIONAL_NONCLAIM" if not missing else "BLOCKED_MISSING_PROJECTOR_INPUTS"
    output.update({"projector_status": status, "projector_theorem": not missing, "missing_projector_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
    return output


def source_pack_row(row: dict[str, Any]) -> dict[str, Any]:
    pack_id = str(row.get("pack_id", "")).strip() or "UNNAMED_SOURCE_PACK"
    output: dict[str, Any] = {"pack_id": pack_id, "component_expr": row.get("component_expr", ""), "valid_for_claim": False, "claim_allowed": False}
    if forbidden_source_used(row):
        output.update({"source_pack_guard_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(parse_float(row.get("required_abs_max"))), "numeric_window_pass": False, "source_pack_status": "FAILED_SOURCE_PACK_GATE", "missing_source_pack_inputs": "FORBIDDEN_SOURCE_PACK", "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED"})
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("source_pack_guard_abs"))
    computed_value, computed_missing = source_guard(row)
    value = direct_value if direct_value is not None else computed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(computed_missing or ["MISSING_source_pack_guard_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update({"source_pack_guard_abs": "MISSING_NUMERIC_VALUE", "required_abs_max": format_float(required), "numeric_window_pass": False, "source_pack_status": "BLOCKED_MISSING_SOURCE_PACK_INPUTS", "missing_source_pack_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
        return output
    passes = value <= required
    status = "SOURCE_PACK_NUMERIC_WINDOW_FAIL"
    if passes:
        status = "SOURCE_PACK_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
        if bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
            status = "SOURCE_PACK_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    output.update({"source_pack_guard_abs": format_float(value), "required_abs_max": format_float(required), "numeric_window_pass": passes, "source_pack_status": status, "missing_source_pack_inputs": ";".join(missing), "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED"})
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"exactness", "projector", "source"}:
        print("Usage: boundary_exactness_projector_source_pack_runner.py exactness|projector|source INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = read_csv(Path(sys.argv[2]))
    mode = sys.argv[1]
    if mode == "exactness":
        outputs = [exactness_row(row) for row in rows]
    elif mode == "projector":
        outputs = [projector_row(row) for row in rows]
    else:
        outputs = [source_pack_row(row) for row in rows]
    write_csv(Path(sys.argv[3]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
