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

ZERO_FLAGS = (
    "corrected_gamma_normalization_signed",
    "candidate_action_adopted_private_signed",
    "response_doublet_parent_owned_signed",
    "exchange_symmetry_signed",
    "ordinary_matter_exchange_even_signed",
    "no_linear_even_Z_source_signed",
    "positive_operator_gap_signed",
    "local_odd_source_zero_signed",
    "boundary_flux_zero_signed",
    "zero_mode_removed_signed",
    "on_shell_Euler_signed",
    "Gamma0_local_constant_signed",
    "same_action_metric_response_signed",
    "coefficients_regular_at_origin_signed",
    "no_direct_Z_readout_signed",
    "background_force_retained_or_bounded_signed",
)

BOUND_FIELDS = (
    "J_Z_norm_m2",
    "boundary_lift_norm_m2",
    "lambda_gap_m2",
    "C_Sigma_quad_m2",
    "R_higher_m2",
    "radius_m",
    "GM_m3_s2",
)

FORBIDDEN_TOKENS = (
    "BACKGROUND_SUBTRACTION_DROPS_FORCE",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "EXCHANGE_SYMMETRY_KILLS_EVEN_STRESS",
    "MEASURED_GM_AS_SOURCE",
    "QLOC_ZERO_IMPLIES_SIGMA_ZERO",
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


def required_flags(row: dict[str, Any], fields: tuple[str, ...], missing: list[str]) -> None:
    for field in fields:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")


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
        "Z_H1_bound": "MISSING_NUMERIC_VALUE",
        "Gamma_active_bound_m2": "MISSING_NUMERIC_VALUE",
        "Pi_active_bound_m2": "MISSING_NUMERIC_VALUE",
        "Sigma_active_bound_m2": "MISSING_NUMERIC_VALUE",
        "q_Gamma_bound_m3": "MISSING_NUMERIC_VALUE",
        "fractional_acceleration_bound": "MISSING_NUMERIC_VALUE",
        "Gamma0_background_m2": "MISSING_NUMERIC_VALUE",
        "background_fractional_acceleration": "MISSING_NUMERIC_VALUE",
        "exchange_balance_residual_m3": "MISSING_NUMERIC_VALUE",
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        **empty_numbers(),
        "local_suppression_status": "FORBIDDEN_ROUTE",
        "exchange_status": "FORBIDDEN_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_ROUTE_USED",
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    required_flags(row, ZERO_FLAGS, missing)
    passed = not missing
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "Z_H1_bound": zero,
        "Gamma_active_bound_m2": zero,
        "Pi_active_bound_m2": zero,
        "Sigma_active_bound_m2": zero,
        "q_Gamma_bound_m3": zero,
        "fractional_acceleration_bound": zero,
        "Gamma0_background_m2": "RETAINED_SEPARATELY" if passed else "MISSING_NUMERIC_VALUE",
        "background_fractional_acceleration": "RETAINED_SEPARATELY" if passed else "MISSING_NUMERIC_VALUE",
        "exchange_balance_residual_m3": zero,
        "local_suppression_status": "RESPONSE_DOUBLET_ACTIVE_ZERO_PRIVATE_NONCLAIM" if passed else "RESPONSE_DOUBLET_ZERO_CLAUSES_BLOCKED",
        "exchange_status": "ON_SHELL_Q_GAMMA_ZERO" if passed else "EXCHANGE_GATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "GAMMA_ACTIVE_LOCAL_ZERO_PASS_PRIVATE_NONCLAIM" if passed else "BLOCKED_GAMMA_ACTIVE_LOCAL_ZERO",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    if not bool_text(row.get("candidate_action_adopted_private_signed")):
        missing.append("MISSING_candidate_action_adopted_private_signed")
    if not bool_text(row.get("same_action_metric_response_signed")):
        missing.append("MISSING_same_action_metric_response_signed")
    values = {field: number(row, field, missing, nonnegative=True) for field in BOUND_FIELDS}
    if values.get("lambda_gap_m2") == 0.0:
        missing.append("ZERO_lambda_gap_m2")
    if values.get("radius_m") == 0.0:
        missing.append("ZERO_radius_m")
    if values.get("GM_m3_s2") == 0.0:
        missing.append("ZERO_GM_m3_s2")
    z_bound = None
    gamma_bound = None
    pi_bound = None
    sigma_bound = None
    acceleration_bound = None
    if not missing:
        z_bound = (values["J_Z_norm_m2"] + values["boundary_lift_norm_m2"]) / values["lambda_gap_m2"]
        gamma_bound = 0.5 * values["C_Sigma_quad_m2"] * z_bound**2
        pi_bound = 0.5 * values["C_Sigma_quad_m2"] * z_bound**2
        sigma_bound = values["C_Sigma_quad_m2"] * z_bound**2 + values["R_higher_m2"]
        acceleration_bound = (C_LIGHT**2) * sigma_bound * values["radius_m"] ** 3 / (3.0 * values["GM_m3_s2"])
    passed = not missing
    return {
        "Z_H1_bound": fmt(z_bound),
        "Gamma_active_bound_m2": fmt(gamma_bound),
        "Pi_active_bound_m2": fmt(pi_bound),
        "Sigma_active_bound_m2": fmt(sigma_bound),
        "q_Gamma_bound_m3": "REQUIRES_SOURCE_GRADIENT_OR_ON_SHELL_WARD_ROW" if passed else "MISSING_NUMERIC_VALUE",
        "fractional_acceleration_bound": fmt(acceleration_bound),
        "Gamma0_background_m2": "RETAINED_SEPARATELY" if passed else "MISSING_NUMERIC_VALUE",
        "background_fractional_acceleration": "RETAINED_SEPARATELY" if passed else "MISSING_NUMERIC_VALUE",
        "exchange_balance_residual_m3": "SEPARATE_GATE_REQUIRED" if passed else "MISSING_NUMERIC_VALUE",
        "local_suppression_status": "QUADRATIC_SOURCE_SUPPRESSION_BOUND_PASS_NONCLAIM" if passed else "QUADRATIC_SOURCE_SUPPRESSION_INPUTS_MISSING",
        "exchange_status": "SEPARATE_ON_SHELL_OR_EXCHANGE_GATE",
        "route_pass": passed,
        "runner_status": "GAMMA_QUADRATIC_SUPPRESSION_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_GAMMA_QUADRATIC_SUPPRESSION_BOUND",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_background(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    gamma0 = number(row, "Gamma0_background_m2", missing)
    radius = number(row, "radius_m", missing, nonnegative=True)
    gm = number(row, "GM_m3_s2", missing, nonnegative=True)
    if radius == 0.0:
        missing.append("ZERO_radius_m")
    if gm == 0.0:
        missing.append("ZERO_GM_m3_s2")
    fraction = None if missing else (C_LIGHT**2) * abs(gamma0) * radius**3 / (3.0 * gm)
    passed = not missing
    return {
        "Z_H1_bound": "NOT_THIS_ROUTE",
        "Gamma_active_bound_m2": "NOT_THIS_ROUTE",
        "Pi_active_bound_m2": "NOT_THIS_ROUTE",
        "Sigma_active_bound_m2": "NOT_THIS_ROUTE",
        "q_Gamma_bound_m3": "0_IF_GAMMA0_CONSTANT",
        "fractional_acceleration_bound": "NOT_THIS_ROUTE",
        "Gamma0_background_m2": fmt(gamma0),
        "background_fractional_acceleration": fmt(fraction),
        "exchange_balance_residual_m3": "0_IF_GAMMA0_CONSTANT",
        "local_suppression_status": "CONSTANT_BACKGROUND_RETAINED_AND_SCORED" if passed else "BACKGROUND_PROFILE_INPUTS_MISSING",
        "exchange_status": "CONSTANT_BACKGROUND_Q_ZERO" if passed else "BACKGROUND_EXCHANGE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "GAMMA0_BACKGROUND_PROFILE_PASS_NONCLAIM" if passed else "BLOCKED_GAMMA0_BACKGROUND_PROFILE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_exchange(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    div_x = number(row, "div_X_Gamma_m3", missing)
    kappa_div_t = number(row, "kappa_div_Tmatter_m3", missing)
    tolerance = number(row, "exchange_tolerance_m3", missing, nonnegative=True)
    residual = None if missing else abs(div_x - kappa_div_t)
    passed = not missing and residual <= tolerance
    if not missing and not passed:
        missing.append("EXCHANGE_SIGN_OR_MAGNITUDE_MISMATCH")
    return {
        "Z_H1_bound": "NOT_THIS_ROUTE",
        "Gamma_active_bound_m2": "NOT_THIS_ROUTE",
        "Pi_active_bound_m2": "NOT_THIS_ROUTE",
        "Sigma_active_bound_m2": "NOT_THIS_ROUTE",
        "q_Gamma_bound_m3": fmt(abs(div_x) if div_x is not None else None),
        "fractional_acceleration_bound": "NOT_THIS_ROUTE",
        "Gamma0_background_m2": "NOT_THIS_ROUTE",
        "background_fractional_acceleration": "NOT_THIS_ROUTE",
        "exchange_balance_residual_m3": fmt(residual),
        "local_suppression_status": "SEPARATE_GATE_REQUIRED",
        "exchange_status": "POSITIVE_SIGN_EXCHANGE_BALANCE_PASS" if passed else "EXCHANGE_BALANCE_BLOCKED",
        "route_pass": passed,
        "runner_status": "GAMMA_EXCHANGE_BALANCE_PASS_NONCLAIM" if passed else "BLOCKED_GAMMA_EXCHANGE_BALANCE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_GAMMA_SUPPRESSION_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "active_zero":
        result = evaluate_zero(row)
    elif route_type == "quadratic_bound":
        result = evaluate_bound(row)
    elif route_type == "constant_background":
        result = evaluate_background(row)
    elif route_type == "exchange_balance":
        result = evaluate_exchange(row)
    else:
        result = {
            **empty_numbers(),
            "local_suppression_status": "UNKNOWN_ROUTE_TYPE",
            "exchange_status": "UNKNOWN_ROUTE_TYPE",
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
        raise SystemExit("usage: gamma_response_doublet_local_suppression_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
