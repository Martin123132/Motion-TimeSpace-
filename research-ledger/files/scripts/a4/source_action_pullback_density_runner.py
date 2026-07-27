from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


COMMON_FLAGS = (
    "source_signed",
    "units_signed",
    "same_branch_signed",
    "no_cancellation_guard",
)

PULLBACK_ZERO_FIELDS = (
    "parent_action_diffeomorphic_signed",
    "q_map_signed",
    "observed_stack_q_owned_signed",
    "source_action_pullback_signed",
    "single_action_density_line_signed",
    "variation_before_readout_signed",
    "measure_coframe_time_qbasic_signed",
    "EM_qbasic_or_flux_retained_signed",
    "theta_representation_superselection_signed",
    "no_source_only_weights_signed",
    "no_kappa_A_source_selector_signed",
    "no_hidden_marker_source_signed",
    "matter_labels_fixed_or_on_shell_signed",
    "no_boundary_source_layer_signed",
    "nonHilbert_current_zero_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

PULLBACK_BOUND_FIELDS = (
    "E_action_pullback_abs",
    "delta_w_species_abs",
    "kappa_A_source_abs",
    "hidden_marker_source_abs",
    "E_measure_qbasic_abs",
    "E_tau_frame_abs",
    "E_EM_qbasic_abs",
    "E_theta_abs",
    "E_matter_lift_abs",
    "E_boundary_source_abs",
    "E_nonHilbert_bypass_abs",
    "E_readout_mask_abs",
    "P_density_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_density_abs",
)

VERTICAL_PROFILE_FIELDS = (
    "rho_vertical_slope_abs",
    "vertical_amplitude_abs",
    "matter_Euler_residual_abs",
    "gauge_fix_residual_abs",
    "boundary_layer_abs",
    "P_density_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_density_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BOUNDARY_LAYER_IGNORED",
    "CANCEL_UNKNOWN_COMPONENTS",
    "DENSITY_QBASIC_BY_ASSERTION",
    "EM_STRESS_DROPPED",
    "GR_IMPORT",
    "KAPPA_A_SOURCE_SELECTOR",
    "MATTER_LIFT_IGNORED",
    "MEASURED_GM_AS_SOURCE",
    "NONHILBERT_BYPASS_IGNORED",
    "POST_VARIATION_SELECTOR",
    "READOUT_MASK_AS_SOURCE",
    "SOURCE_ONLY_WEIGHT_ASSERTED_ZERO",
    "THETA_BY_UNIT_CHOICE",
    "VARIATION_AFTER_READOUT",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed", "derived"}


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
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and not missing_text(source_path) and Path(source_path).exists()


def forbidden_source_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in ("row_id", "route_type", "route", "source_path", "equation_ref", "notes", "provenance")
    ).upper()
    normalized = text.replace(" ", "_").replace("-", "_")
    return any(token in normalized for token in FORBIDDEN_SOURCE_TOKENS)


def base_missing(row: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    if not source_ok(row):
        missing.append("MISSING_source_path")
    for flag in COMMON_FLAGS:
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


def projection_outputs(delta: float | None, P: float | None, Qbar: float | None, K: float | None, tau: float | None) -> dict[str, float | None]:
    if None in (delta, P, Qbar, K, tau):
        return {"qbar": None, "alpha": None, "BY5": None}
    qbar = P * delta
    return {"qbar": qbar, "alpha": K * Qbar * qbar, "BY5": tau * qbar}


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "source_action_residual_abs": "MISSING_NUMERIC_VALUE",
        "density_qbasic_residual_abs": "MISSING_NUMERIC_VALUE",
        "vertical_density_residual_abs": "MISSING_NUMERIC_VALUE",
        "delta_MHref_density_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_density_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_density_feed_abs": "MISSING_NUMERIC_VALUE",
        "density_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_pullback_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in PULLBACK_ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "source_action_residual_abs": zero,
        "density_qbasic_residual_abs": zero,
        "vertical_density_residual_abs": zero,
        "delta_MHref_density_abs": zero,
        "qbar_XT_density_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_density_feed_abs": zero,
        "density_status": "SOURCE_ACTION_PULLBACK_DENSITY_QBASIC_ZERO_SIGNED" if passed else "SOURCE_ACTION_PULLBACK_DENSITY_QBASIC_ZERO_UNSIGNED",
        "route_pass": passed,
        "runner_status": "SOURCE_ACTION_PULLBACK_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_SOURCE_ACTION_PULLBACK_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_pullback_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in PULLBACK_BOUND_FIELDS}
    source_action = None
    density = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        source_action = (
            values["E_action_pullback_abs"]
            + values["delta_w_species_abs"]
            + values["kappa_A_source_abs"]
            + values["hidden_marker_source_abs"]
        )
        density = sum(values[field] for field in PULLBACK_BOUND_FIELDS[:12])
        projection = projection_outputs(
            density,
            values["P_density_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_density_abs"],
        )
    passed = not missing
    return {
        "source_action_residual_abs": fmt(source_action),
        "density_qbasic_residual_abs": fmt(density),
        "vertical_density_residual_abs": "MISSING_NUMERIC_VALUE",
        "delta_MHref_density_abs": fmt(density),
        "qbar_XT_density_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_density_feed_abs": fmt(projection["BY5"]),
        "density_status": "FINITE_SOURCE_ACTION_DENSITY_QBASIC_ROW_READY" if passed else "FINITE_SOURCE_ACTION_DENSITY_QBASIC_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "SOURCE_ACTION_DENSITY_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_SOURCE_ACTION_DENSITY_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_vertical_profile_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in VERTICAL_PROFILE_FIELDS}
    residual = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        residual = (
            values["rho_vertical_slope_abs"] * values["vertical_amplitude_abs"]
            + values["matter_Euler_residual_abs"]
            + values["gauge_fix_residual_abs"]
            + values["boundary_layer_abs"]
        )
        projection = projection_outputs(
            residual,
            values["P_density_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_density_abs"],
        )
    passed = not missing
    return {
        "source_action_residual_abs": "MISSING_NUMERIC_VALUE",
        "density_qbasic_residual_abs": fmt(residual),
        "vertical_density_residual_abs": fmt(residual),
        "delta_MHref_density_abs": fmt(residual),
        "qbar_XT_density_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_density_feed_abs": fmt(projection["BY5"]),
        "density_status": "FINITE_VERTICAL_DENSITY_PROFILE_ROW_READY" if passed else "FINITE_VERTICAL_DENSITY_PROFILE_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "VERTICAL_DENSITY_PROFILE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_VERTICAL_DENSITY_PROFILE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_DENSITY_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "pullback_zero":
        result = evaluate_pullback_zero(row)
    elif route_type == "pullback_bound":
        result = evaluate_pullback_bound(row)
    elif route_type == "vertical_profile_bound":
        result = evaluate_vertical_profile_bound(row)
    else:
        result = {
            "source_action_residual_abs": "MISSING_NUMERIC_VALUE",
            "density_qbasic_residual_abs": "MISSING_NUMERIC_VALUE",
            "vertical_density_residual_abs": "MISSING_NUMERIC_VALUE",
            "delta_MHref_density_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_density_feed_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_density_feed_abs": "MISSING_NUMERIC_VALUE",
            "density_status": "UNKNOWN_ROUTE_TYPE",
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
        "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
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
        raise SystemExit("usage: source_action_pullback_density_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
