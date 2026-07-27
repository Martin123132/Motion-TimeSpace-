from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


C_LIGHT = 299_792_458.0

COMMON_FLAGS = (
    "source_signed",
    "units_signed",
    "same_branch_signed",
    "no_cancellation_guard",
)

FORBIDDEN_TOKENS = (
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "IGNORE_FACTOR_TWO",
    "RAW_E00_WITHOUT_TRACE_REVERSE",
    "VARIABLE_EXTERNAL_GAMMA_NO_EXCHANGE",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "signed", "derived"}


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


def source_ok(row: dict[str, Any]) -> bool:
    path = str(row.get("source_path", "")).strip()
    return bool(path) and not missing_text(path) and Path(path).exists()


def forbidden_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in ("row_id", "route_type", "route", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    normalized = text.replace(" ", "_").replace("-", "_")
    return any(token in normalized for token in FORBIDDEN_TOKENS)


def base_missing(row: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in COMMON_FLAGS:
        if not bool_text(row.get(flag)):
            missing.append(f"MISSING_{flag}")
    return missing


def number(row: dict[str, Any], field: str, missing: list[str], nonnegative: bool = False) -> float | None:
    value = parse_float(row.get(field))
    if value is None:
        missing.append(f"MISSING_{field}")
        return None
    if nonnegative and value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return None
    return value


def empty_numbers() -> dict[str, str]:
    return {
        "a_gamma_action": "MISSING_NUMERIC_VALUE",
        "field_equation_gamma_coefficient": "MISSING_NUMERIC_VALUE",
        "normalization_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "Sigma_Gamma_m2": "MISSING_NUMERIC_VALUE",
        "Delta_Poisson_Gamma_s2": "MISSING_NUMERIC_VALUE",
        "delta_acceleration_m_s2": "MISSING_NUMERIC_VALUE",
        "fractional_acceleration_abs": "MISSING_NUMERIC_VALUE",
        "Sigma_Gamma_bound_m2": "MISSING_NUMERIC_VALUE",
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        **empty_numbers(),
        "normalization_status": "FORBIDDEN_ROUTE",
        "trace_reverse_status": "FORBIDDEN_ROUTE",
        "bianchi_status": "FORBIDDEN_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_ROUTE_USED",
    }


def evaluate_normalization(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    action_coefficient = number(row, "a_gamma_action", missing)
    target = number(row, "target_field_equation_coefficient", missing)
    mismatch = None if missing else abs(action_coefficient - target)
    matches = mismatch is not None and mismatch <= 1e-14
    detected = not missing
    return {
        "a_gamma_action": fmt(action_coefficient),
        "field_equation_gamma_coefficient": fmt(action_coefficient),
        "normalization_mismatch_abs": fmt(mismatch),
        "Sigma_Gamma_m2": "NOT_THIS_ROUTE",
        "Delta_Poisson_Gamma_s2": "NOT_THIS_ROUTE",
        "delta_acceleration_m_s2": "NOT_THIS_ROUTE",
        "fractional_acceleration_abs": "NOT_THIS_ROUTE",
        "Sigma_Gamma_bound_m2": "NOT_THIS_ROUTE",
        "normalization_status": "ACTION_NORMALIZATION_MATCH" if matches else "ACTION_NORMALIZATION_MISMATCH_DETECTED" if detected else "ACTION_NORMALIZATION_INPUTS_MISSING",
        "trace_reverse_status": "NOT_THIS_ROUTE",
        "bianchi_status": "NOT_THIS_ROUTE",
        "route_pass": matches,
        "runner_status": "ACTION_NORMALIZATION_PASS_NONCLAIM" if matches else "ACTION_NORMALIZATION_MISMATCH_DETECTED" if detected else "BLOCKED_ACTION_NORMALIZATION_INPUTS",
        "missing_for_claim": "" if detected else ";".join(dict.fromkeys(missing)),
    }


def trace_source(row: dict[str, Any], missing: list[str]) -> tuple[float | None, float | None, float | None]:
    action_coefficient = number(row, "a_gamma_action", missing)
    gamma = number(row, "Gamma_G_m2", missing)
    pi00 = number(row, "Pi_Gamma_00_m2", missing)
    pi_trace = number(row, "Pi_Gamma_trace_m2", missing)
    if missing:
        return action_coefficient, None, None
    sigma = action_coefficient * (gamma - 2.0 * pi00 - pi_trace)
    delta_poisson = -(C_LIGHT**2) * sigma
    return action_coefficient, sigma, delta_poisson


def evaluate_trace_source(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    action_coefficient, sigma, delta_poisson = trace_source(row, missing)
    passed = not missing
    return {
        "a_gamma_action": fmt(action_coefficient),
        "field_equation_gamma_coefficient": fmt(action_coefficient),
        "normalization_mismatch_abs": "NOT_THIS_ROUTE",
        "Sigma_Gamma_m2": fmt(sigma),
        "Delta_Poisson_Gamma_s2": fmt(delta_poisson),
        "delta_acceleration_m_s2": "NOT_THIS_ROUTE",
        "fractional_acceleration_abs": "NOT_THIS_ROUTE",
        "Sigma_Gamma_bound_m2": "NOT_THIS_ROUTE",
        "normalization_status": "TRACE_SOURCE_USES_SUPPLIED_A_GAMMA" if passed else "TRACE_SOURCE_INPUTS_MISSING",
        "trace_reverse_status": "TRACE_REVERSED_GAMMA_SOURCE_PASS_NONCLAIM" if passed else "TRACE_REVERSED_GAMMA_SOURCE_BLOCKED",
        "bianchi_status": "SEPARATE_GATE_REQUIRED",
        "route_pass": passed,
        "runner_status": "TRACE_REVERSED_GAMMA_SOURCE_PASS_NONCLAIM" if passed else "BLOCKED_TRACE_REVERSED_GAMMA_SOURCE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_constant_profile(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    action_coefficient, sigma, delta_poisson = trace_source(row, missing)
    radius = number(row, "radius_m", missing, nonnegative=True)
    gm = number(row, "GM_m3_s2", missing, nonnegative=True)
    if radius == 0.0:
        missing.append("ZERO_radius_m")
    if gm == 0.0:
        missing.append("ZERO_GM_m3_s2")
    delta_acceleration = None
    fraction = None
    if not missing:
        delta_acceleration = (C_LIGHT**2) * abs(sigma) * radius / 3.0
        fraction = (C_LIGHT**2) * abs(sigma) * radius**3 / (3.0 * gm)
    passed = not missing
    return {
        "a_gamma_action": fmt(action_coefficient),
        "field_equation_gamma_coefficient": fmt(action_coefficient),
        "normalization_mismatch_abs": "NOT_THIS_ROUTE",
        "Sigma_Gamma_m2": fmt(sigma),
        "Delta_Poisson_Gamma_s2": fmt(delta_poisson),
        "delta_acceleration_m_s2": fmt(delta_acceleration),
        "fractional_acceleration_abs": fmt(fraction),
        "Sigma_Gamma_bound_m2": "NOT_THIS_ROUTE",
        "normalization_status": "TRACE_SOURCE_USES_SUPPLIED_A_GAMMA" if passed else "PROFILE_INPUTS_MISSING",
        "trace_reverse_status": "CONSTANT_SPHERICAL_PROFILE_PASS_NONCLAIM" if passed else "CONSTANT_SPHERICAL_PROFILE_BLOCKED",
        "bianchi_status": "REQUIRES_CONSTANT_OR_EXCHANGE_GATE",
        "route_pass": passed,
        "runner_status": "CONSTANT_GAMMA_PROFILE_PASS_NONCLAIM" if passed else "BLOCKED_CONSTANT_GAMMA_PROFILE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_threshold(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    tolerance = number(row, "fractional_acceleration_tolerance", missing, nonnegative=True)
    radius = number(row, "radius_m", missing, nonnegative=True)
    gm = number(row, "GM_m3_s2", missing, nonnegative=True)
    if radius == 0.0:
        missing.append("ZERO_radius_m")
    if gm == 0.0:
        missing.append("ZERO_GM_m3_s2")
    bound = None if missing else 3.0 * tolerance * gm / ((C_LIGHT**2) * radius**3)
    passed = not missing
    return {
        "a_gamma_action": "NOT_THIS_ROUTE",
        "field_equation_gamma_coefficient": "NOT_THIS_ROUTE",
        "normalization_mismatch_abs": "NOT_THIS_ROUTE",
        "Sigma_Gamma_m2": "NOT_A_PREDICTION",
        "Delta_Poisson_Gamma_s2": "NOT_THIS_ROUTE",
        "delta_acceleration_m_s2": "NOT_THIS_ROUTE",
        "fractional_acceleration_abs": fmt(tolerance),
        "Sigma_Gamma_bound_m2": fmt(bound),
        "normalization_status": "NOT_THIS_ROUTE",
        "trace_reverse_status": "COMPARATOR_THRESHOLD_ONLY" if passed else "COMPARATOR_INPUTS_MISSING",
        "bianchi_status": "NOT_THIS_ROUTE",
        "route_pass": passed,
        "runner_status": "LOCAL_SIGMA_GAMMA_THRESHOLD_PASS_NONCLAIM" if passed else "BLOCKED_LOCAL_SIGMA_GAMMA_THRESHOLD",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_bianchi(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    matter_conserved = bool_text(row.get("matter_separately_conserved_signed"))
    gamma_constant = bool_text(row.get("Gamma_G_local_constant_signed"))
    response_exchange = bool_text(row.get("metric_response_or_exchange_signed"))
    if not matter_conserved:
        missing.append("MISSING_matter_separately_conserved_signed")
    if not gamma_constant and not response_exchange:
        missing.append("MISSING_Gamma_constant_or_metric_response_exchange")
    passed = not missing
    return {
        **empty_numbers(),
        "normalization_status": "SEPARATE_GATE_REQUIRED",
        "trace_reverse_status": "SEPARATE_GATE_REQUIRED",
        "bianchi_status": "BIANCHI_LOCAL_CONSISTENCY_PASS_NONCLAIM" if passed else "BIANCHI_LOCAL_CONSISTENCY_BLOCKED",
        "route_pass": passed,
        "runner_status": "BIANCHI_GAMMA_GATE_PASS_NONCLAIM" if passed else "BLOCKED_BIANCHI_GAMMA_GATE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_GAMMA_E00_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "action_normalization":
        result = evaluate_normalization(row)
    elif route_type == "trace_reversed_source":
        result = evaluate_trace_source(row)
    elif route_type == "constant_spherical_profile":
        result = evaluate_constant_profile(row)
    elif route_type == "local_sigma_threshold":
        result = evaluate_threshold(row)
    elif route_type == "bianchi_gate":
        result = evaluate_bianchi(row)
    else:
        result = {
            **empty_numbers(),
            "normalization_status": "UNKNOWN_ROUTE_TYPE",
            "trace_reverse_status": "UNKNOWN_ROUTE_TYPE",
            "bianchi_status": "UNKNOWN_ROUTE_TYPE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        **result,
        "anti_circularity_status": "PASS_NO_FORBIDDEN_ROUTE_USED",
    }


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    outputs = [evaluate_row(row) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in outputs for field in row))
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(outputs)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: gamma_action_E00_trace_reverse_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
