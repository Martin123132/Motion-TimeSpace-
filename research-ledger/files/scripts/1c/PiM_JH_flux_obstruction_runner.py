from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


OBSTRUCTION_CLAUSES = (
    "same_frame_JH_signed",
    "PiM_parent_origin_signed",
    "extra_projection_zero_signed",
    "PiM_commutator_zero_signed",
    "parent_anomaly_zero_signed",
    "topological_Hilbert_equality_signed",
    "boundary_zero_flux_signed",
    "projector_stress_silence_signed",
    "worldtube_glue_signed",
    "absolute_calibration_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

OBSTRUCTION_COMPONENTS = (
    "delta_extra_current_abs",
    "I_commutator_abs",
    "A_parent_abs",
    "R_eq_abs",
    "B_zero_flux_abs",
    "T_PiM_abs",
    "flux_leak_abs",
    "Delta_cal_PPN_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "SCHWARZSCHILD_AB_IMPORT",
    "EINSTEIN_VACUUM_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
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
    source_text = " ".join(str(row.get(field, "")) for field in ("obstruction_id", "prior_id", "source_path", "equation_ref", "notes", "provenance")).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in OBSTRUCTION_CLAUSES if not bool_text(row.get(clause))]


def obstruction_sum(row: dict[str, Any]) -> tuple[float | None, list[str]]:
    values: list[float] = []
    missing: list[str] = []
    for component in OBSTRUCTION_COMPONENTS:
        value = parse_float(row.get(component))
        if value is None or value < 0.0:
            missing.append(f"MISSING_{component}")
        else:
            values.append(value)
    if missing:
        return None, missing
    return sum(values), []


def obstruction_row(row: dict[str, Any]) -> dict[str, Any]:
    obstruction_id = str(row.get("obstruction_id", "")).strip() or "UNNAMED_PIM_OBSTRUCTION"
    output: dict[str, Any] = {
        "obstruction_id": obstruction_id,
        "route": row.get("route", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "pim_flux_theorem": False,
                "runner_status": "FAILED_PIM_OBSTRUCTION_GATE",
                "missing_obstruction_inputs": "FORBIDDEN_PIM_OBSTRUCTION_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    total, numeric_missing = obstruction_sum(row)
    missing = [*missing_clauses(row), *numeric_missing]
    if total is None:
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "pim_flux_theorem": False,
                "runner_status": "BLOCKED_MISSING_PIM_OBSTRUCTION_INPUTS",
                "missing_obstruction_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if not missing and total <= 1.0e-15:
        status = "PIM_FLUX_OBSTRUCTION_ZERO_CONDITIONAL_THEOREM_NONCLAIM"
        theorem = True
    elif total <= 1.0e-15:
        status = "PIM_FLUX_OBSTRUCTION_ZERO_NUMERIC_PARENT_UNSIGNED_NONCLAIM"
        theorem = False
    else:
        status = "PIM_FLUX_OBSTRUCTION_FINITE_BOUND_COMPUTED_NONCLAIM"
        theorem = False
    output.update(
        {
            "pim_obstruction_abs": format_float(total),
            "pim_flux_theorem": theorem,
            "runner_status": status,
            "missing_obstruction_inputs": ";".join(missing),
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def prior_row(row: dict[str, Any]) -> dict[str, Any]:
    prior_id = str(row.get("prior_id", "")).strip() or "UNNAMED_PIM_PRIOR"
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
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(parse_float(row.get("required_abs_max"))),
                "numeric_window_pass": False,
                "runner_status": "FAILED_PIM_OBSTRUCTION_PRIOR_GATE",
                "missing_prior_inputs": "FORBIDDEN_PIM_PRIOR_SOURCE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    required = parse_float(row.get("required_abs_max"))
    direct_value = parse_float(row.get("pim_obstruction_abs"))
    summed_value, summed_missing = obstruction_sum(row)
    value = direct_value if direct_value is not None else summed_value
    missing: list[str] = []
    if required is None or required <= 0.0:
        missing.append("MISSING_required_abs_max")
    if value is None:
        missing.extend(summed_missing or ["MISSING_pim_obstruction_abs"])
    if missing_text(row.get("source_path")):
        missing.append("MISSING_source_path")
    if missing_text(row.get("equation_ref")):
        missing.append("MISSING_equation_ref")
    if not bool_text(row.get("source_signed")):
        missing.append("MISSING_source_signed")
    if required is None or required <= 0.0 or value is None:
        output.update(
            {
                "pim_obstruction_abs": "MISSING_NUMERIC_VALUE",
                "required_abs_max": format_float(required),
                "numeric_window_pass": False,
                "runner_status": "BLOCKED_MISSING_PIM_OBSTRUCTION_PRIOR_INPUTS",
                "missing_prior_inputs": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    passes = value <= required
    if not passes:
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_FAIL"
    elif bool_text(row.get("source_signed")) and bool_text(row.get("valid_for_claim")):
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_SIGNED_NONCLAIM"
    else:
        status = "PIM_OBSTRUCTION_PRIOR_NUMERIC_WINDOW_PASS_SOURCE_UNSIGNED_NONCLAIM"
    output.update(
        {
            "pim_obstruction_abs": format_float(value),
            "required_abs_max": format_float(required),
            "numeric_window_pass": passes,
            "runner_status": status,
            "missing_prior_inputs": ";".join(missing),
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
    if len(sys.argv) != 4 or sys.argv[1] not in {"obstruction", "prior"}:
        print("Usage: PiM_JH_flux_obstruction_runner.py obstruction|prior INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])
    rows = read_csv(input_path)
    outputs = [obstruction_row(row) for row in rows] if mode == "obstruction" else [prior_row(row) for row in rows]
    write_csv(output_path, outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
