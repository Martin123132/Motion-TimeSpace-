from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


B_ZERO_FIELDS = (
    "B826_zero",
    "BWeyl_zero",
    "BY5_zero",
    "BY6_zero",
    "Bsrc_boundary_zero",
    "Bsrc_readout_zero",
)

J_ZERO_FIELDS = (
    "J_source_kernel_zero",
    "J_EM_open_zero",
    "J_nonHilbert_zero",
    "J_dyn_exchange_zero",
    "J_boundary_readout_zero",
)

Q_ZERO_FIELDS = (
    "Q_boundary_mem_zero",
    "boundary_reference_neutral",
    "no_incoming_flux",
)

B_VALUE_FIELDS = (
    "B826_abs",
    "BWeyl_abs",
    "BY5_abs",
    "BY6_abs",
    "Bsrc_boundary_abs",
    "Bsrc_readout_abs",
)

J_VALUE_FIELDS = (
    "J_source_kernel_abs",
    "J_EM_open_abs",
    "J_nonHilbert_abs",
    "J_dyn_exchange_abs",
    "J_boundary_readout_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ALPHA_OBS_AS_DERIVATION",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POYNTING_DOUBLE_COUNT",
    "STANDARD_BRANCH_AS_GLOBAL",
    "WEP_ONLY_AS_ZERO",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}


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
        for field in ("row_id", "route_type", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


def source_ok(row: dict[str, Any]) -> bool:
    text = str(row.get("source_path", "")).strip()
    return bool(text) and not missing_text(text) and Path(text).exists()


def common_missing(row: dict[str, Any]) -> list[str]:
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in ("source_signed", "units_signed", "same_branch_signed", "no_cancellation_guard"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    return missing


def nonnegative(row: dict[str, Any], field: str, missing: list[str]) -> float | None:
    value = parse_float(row.get(field))
    if value is None:
        missing.append(f"MISSING_{field}")
        return None
    if value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return None
    return value


def component_values(row: dict[str, Any]) -> tuple[float | None, float | None, float | None, list[str]]:
    missing = common_missing(row)
    B_total = 0.0
    J_total = 0.0
    for field in B_VALUE_FIELDS:
        value = nonnegative(row, field, missing)
        if value is not None:
            B_total += value
    for field in J_VALUE_FIELDS:
        value = nonnegative(row, field, missing)
        if value is not None:
            J_total += value
    Q_boundary = nonnegative(row, "Q_boundary_mem_abs", missing)
    if missing:
        return None, None, None, list(dict.fromkeys(missing))
    return B_total, J_total, Q_boundary, []


def evaluate_component_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in ("source_signed", "units_signed", "same_branch_signed", "parent_object_language_signed", "no_cancellation_guard"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    for field in B_ZERO_FIELDS + J_ZERO_FIELDS + Q_ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    return {
        "B_mem_eff_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "J_mem_live_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "Q_boundary_mem_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "rho_mem_reduced_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "BJQ_COMPONENT_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_BJQ_COMPONENT_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    B_total, J_total, Q_boundary, missing = component_values(row)
    passed = not missing
    return {
        "B_mem_eff_abs": fmt(B_total),
        "J_mem_live_abs": fmt(J_total),
        "Q_boundary_mem_abs": fmt(Q_boundary),
        "rho_mem_reduced_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "BJQ_COMPONENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_BJQ_COMPONENT_INPUTS",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_rho_feed(row: dict[str, Any]) -> dict[str, Any]:
    B_total, J_total, Q_boundary, missing = component_values(row)
    R_obs_norm = nonnegative(row, "R_obs_norm", missing)
    Cmem_final_abs = nonnegative(row, "Cmem_final_abs", missing)
    T_obs_norm = nonnegative(row, "T_obs_norm", missing)
    rho = None
    if not missing and B_total is not None and J_total is not None and R_obs_norm is not None and Cmem_final_abs is not None and T_obs_norm is not None:
        rho = B_total * R_obs_norm + Cmem_final_abs * T_obs_norm + J_total
    passed = not missing
    return {
        "B_mem_eff_abs": fmt(B_total),
        "J_mem_live_abs": fmt(J_total),
        "Q_boundary_mem_abs": fmt(Q_boundary),
        "rho_mem_reduced_abs": fmt(rho),
        "route_pass": passed,
        "runner_status": "BJQ_RHO_FEED_PASS_NONCLAIM" if passed else "BLOCKED_BJQ_RHO_FEED_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_BJQ_COMPONENT_ROW"
    route_type = str(row.get("route_type", "")).strip()
    output: dict[str, Any] = {
        "row_id": row_id,
        "route_type": route_type,
        "route": row.get("route", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "B_mem_eff_abs": "MISSING_NUMERIC_VALUE",
                "J_mem_live_abs": "MISSING_NUMERIC_VALUE",
                "Q_boundary_mem_abs": "MISSING_NUMERIC_VALUE",
                "rho_mem_reduced_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "component_zero":
        result = evaluate_component_zero(row)
    elif route_type == "component_bound":
        result = evaluate_component_bound(row)
    elif route_type == "rho_feed":
        result = evaluate_rho_feed(row)
    else:
        result = {
            "B_mem_eff_abs": "MISSING_NUMERIC_VALUE",
            "J_mem_live_abs": "MISSING_NUMERIC_VALUE",
            "Q_boundary_mem_abs": "MISSING_NUMERIC_VALUE",
            "rho_mem_reduced_abs": "MISSING_NUMERIC_VALUE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    output.update(result)
    output["anti_circularity_status"] = "PASS_NO_FORBIDDEN_SOURCE_USED"
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
        print("Usage: Bmem_Jmem_Qboundary_component_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
