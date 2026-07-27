from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


SOURCE_ZERO_FIELDS = (
    "curvature_zero",
    "matter_trace_zero",
    "em_invariant_zero",
    "poynting_zero",
    "wave_stress_zero",
    "hidden_current_zero",
)

BOUNDARY_ZERO_FIELDS = (
    "boundary_flux_zero",
    "boundary_reference_neutral",
    "no_incoming_flux",
)

CHANNEL_FIELDS = (
    ("beta_R_abs", "R_obs_norm"),
    ("beta_T_abs", "T_obs_norm"),
    ("beta_F_abs", "F2_norm"),
    ("beta_G_abs", "FstarF_norm"),
    ("beta_gw_abs", "rho_gw_eff_norm"),
)

POYNTING_MODES = {"zero", "volume", "boundary"}

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
    for flag in ("source_signed", "units_signed", "same_branch_signed"):
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


def source_norms(row: dict[str, Any]) -> tuple[float | None, float | None, list[str]]:
    missing = common_missing(row)
    rho_norm = 0.0
    q_boundary_norm = 0.0
    for coeff_field, source_field in CHANNEL_FIELDS:
        coeff = nonnegative(row, coeff_field, missing)
        source = nonnegative(row, source_field, missing)
        if coeff is not None and source is not None:
            rho_norm += coeff * source
    J_hidden = nonnegative(row, "J_hidden_norm", missing)
    if J_hidden is not None:
        rho_norm += J_hidden
    beta_S = nonnegative(row, "beta_S_abs", missing)
    poynting_mode = str(row.get("poynting_mode", "")).strip().lower()
    if poynting_mode not in POYNTING_MODES:
        missing.append("MISSING_poynting_mode")
    divS = parse_float(row.get("divS_norm"))
    S_boundary = parse_float(row.get("S_boundary_flux_abs"))
    if poynting_mode == "volume":
        if divS is None or divS < 0.0:
            missing.append("MISSING_divS_norm")
        elif beta_S is not None:
            rho_norm += beta_S * divS
        if S_boundary is not None and S_boundary > 0.0:
            missing.append("POYNTING_DOUBLE_COUNT_VOLUME_AND_BOUNDARY")
    elif poynting_mode == "boundary":
        if S_boundary is None or S_boundary < 0.0:
            missing.append("MISSING_S_boundary_flux_abs")
        elif beta_S is not None:
            q_boundary_norm += beta_S * S_boundary
        if divS is not None and divS > 0.0:
            missing.append("POYNTING_DOUBLE_COUNT_VOLUME_AND_BOUNDARY")
    elif poynting_mode == "zero":
        if (divS is not None and divS > 0.0) or (S_boundary is not None and S_boundary > 0.0):
            missing.append("NONZERO_POYNTING_IN_ZERO_MODE")
    Q_boundary = nonnegative(row, "Q_boundary_mem_abs", missing)
    if Q_boundary is not None:
        q_boundary_norm += Q_boundary
    if missing:
        return None, None, list(dict.fromkeys(missing))
    return rho_norm, q_boundary_norm, []


def evaluate_source_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in ("source_signed", "units_signed", "same_branch_signed", "parent_object_language_signed"):
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    for field in SOURCE_ZERO_FIELDS + BOUNDARY_ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    return {
        "rho_mem_norm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "q_boundary_mem_norm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "Delta_v_m_mem_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "RHOMEM_QBOUNDARY_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_RHOMEM_QBOUNDARY_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_source_bound(row: dict[str, Any]) -> dict[str, Any]:
    rho_norm, q_boundary_norm, missing = source_norms(row)
    passed = not missing
    return {
        "rho_mem_norm_abs": fmt(rho_norm),
        "q_boundary_mem_norm_abs": fmt(q_boundary_norm),
        "Delta_v_m_mem_bound_abs": "MISSING_NUMERIC_VALUE",
        "route_pass": passed,
        "runner_status": "RHOMEM_QBOUNDARY_SOURCE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_RHOMEM_QBOUNDARY_SOURCE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(missing),
    }


def evaluate_amplitude_feed(row: dict[str, Any]) -> dict[str, Any]:
    rho_norm, q_boundary_norm, missing = source_norms(row)
    Z_mem = nonnegative(row, "Z_mem_min", missing)
    M2_mem = nonnegative(row, "M2_mem_min", missing)
    C_omega = nonnegative(row, "C_omega", missing)
    delta_bound = None
    if Z_mem is not None and Z_mem <= 0.0:
        missing.append("NONPOSITIVE_Z_mem_min")
    if M2_mem is not None and M2_mem <= 0.0:
        missing.append("NONPOSITIVE_M2_mem_min")
    if not missing and rho_norm is not None and q_boundary_norm is not None and Z_mem is not None and M2_mem is not None and C_omega is not None:
        delta_bound = C_omega * (rho_norm + q_boundary_norm) / min(Z_mem, M2_mem)
    passed = not missing
    return {
        "rho_mem_norm_abs": fmt(rho_norm),
        "q_boundary_mem_norm_abs": fmt(q_boundary_norm),
        "Delta_v_m_mem_bound_abs": fmt(delta_bound),
        "route_pass": passed,
        "runner_status": "RHOMEM_QBOUNDARY_AMPLITUDE_FEED_PASS_NONCLAIM" if passed else "BLOCKED_RHOMEM_QBOUNDARY_AMPLITUDE_FEED_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_RHOMEM_QBOUNDARY_ROW"
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
                "rho_mem_norm_abs": "MISSING_NUMERIC_VALUE",
                "q_boundary_mem_norm_abs": "MISSING_NUMERIC_VALUE",
                "Delta_v_m_mem_bound_abs": "MISSING_NUMERIC_VALUE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "source_zero":
        result = evaluate_source_zero(row)
    elif route_type == "source_bound":
        result = evaluate_source_bound(row)
    elif route_type == "amplitude_feed":
        result = evaluate_amplitude_feed(row)
    else:
        result = {
            "rho_mem_norm_abs": "MISSING_NUMERIC_VALUE",
            "q_boundary_mem_norm_abs": "MISSING_NUMERIC_VALUE",
            "Delta_v_m_mem_bound_abs": "MISSING_NUMERIC_VALUE",
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
        print("Usage: rho_mem_Qboundary_source_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    write_csv(Path(sys.argv[2]), [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
