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

ZERO_FIELDS = (
    "parent_matter_category_signed",
    "single_action_density_line_signed",
    "common_measure_normalization_signed",
    "connected_ordinary_matter_category_signed",
    "species_label_no_source_hom_signed",
    "hidden_marker_no_source_hom_signed",
    "readout_selector_no_source_hom_signed",
    "theta_constants_separated_signed",
    "current_normalization_representation_signed",
    "variation_before_readout_signed",
    "source_functor_total_Hilbert_signed",
    "common_mode_projector_signed",
    "no_species_only_jacobian_signed",
    "no_post_variation_selector_signed",
    "no_bound_as_source_signed",
    "no_G_or_GM_absorption_signed",
)

DELTA_W_FIELDS = (
    "epsilon_A_vector_norm_abs",
    "P_perp_common_mode_abs",
    "composition_weight_uncertainty_abs",
    "common_mode_leak_abs",
    "P_source_delta_w_abs",
    "P_DqZ_delta_w_abs",
    "P_density_from_delta_w_abs",
    "P_delta_w_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_delta_w_abs",
)

NOHOM_FIELDS = (
    "R_species_hom_abs",
    "R_hidden_hom_abs",
    "R_readout_hom_abs",
    "R_action_line_abs",
    "P_delta_w_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_delta_w_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "COMMON_MODE_HIDES_RELATIVE_WEIGHT",
    "CONSTANT_OWNER_AS_SOURCE_OWNER",
    "G_ABSORPTION",
    "KAPPA_A_SOURCE_SELECTOR",
    "MEASURED_GM_AS_SOURCE",
    "NOHOM_BY_DECLARATION",
    "POST_VARIATION_SELECTOR",
    "READOUT_MASK_AS_SOURCE",
    "SOURCE_ONLY_WEIGHT_ASSERTED_ZERO",
    "SPECIES_LABEL_FIT",
    "UNIT_RESCALING",
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
        "delta_w_species_abs": "MISSING_NUMERIC_VALUE",
        "relative_weight_residual_abs": "MISSING_NUMERIC_VALUE",
        "JH_DqZ_injection_abs": "MISSING_NUMERIC_VALUE",
        "density_qbasic_feed_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_delta_w_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_delta_w_feed_abs": "MISSING_NUMERIC_VALUE",
        "delta_w_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "delta_w_species_abs": zero,
        "relative_weight_residual_abs": zero,
        "JH_DqZ_injection_abs": zero,
        "density_qbasic_feed_abs": zero,
        "qbar_XT_delta_w_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_delta_w_feed_abs": zero,
        "delta_w_status": "SINGLE_ACTION_DENSITY_NO_SOURCE_WEIGHT_ZERO_SIGNED" if passed else "SINGLE_ACTION_DENSITY_NO_SOURCE_WEIGHT_ZERO_UNSIGNED",
        "route_pass": passed,
        "runner_status": "DELTA_W_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_DELTA_W_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_delta_w_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in DELTA_W_FIELDS}
    delta_w = None
    injection = None
    density = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        delta_w = (
            values["P_perp_common_mode_abs"] * values["epsilon_A_vector_norm_abs"]
            + values["composition_weight_uncertainty_abs"]
            + values["common_mode_leak_abs"]
        )
        injection = (values["P_source_delta_w_abs"] + values["P_DqZ_delta_w_abs"]) * delta_w
        density = values["P_density_from_delta_w_abs"] * delta_w + injection
        projection = projection_outputs(
            density,
            values["P_delta_w_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_delta_w_abs"],
        )
    passed = not missing
    return {
        "delta_w_species_abs": fmt(delta_w),
        "relative_weight_residual_abs": fmt(delta_w),
        "JH_DqZ_injection_abs": fmt(injection),
        "density_qbasic_feed_abs": fmt(density),
        "qbar_XT_delta_w_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_delta_w_feed_abs": fmt(projection["BY5"]),
        "delta_w_status": "FINITE_DELTA_W_SPECIES_ROW_READY" if passed else "FINITE_DELTA_W_SPECIES_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DELTA_W_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_DELTA_W_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_nohom_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in NOHOM_FIELDS}
    residual = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        residual = (
            values["R_species_hom_abs"]
            + values["R_hidden_hom_abs"]
            + values["R_readout_hom_abs"]
            + values["R_action_line_abs"]
        )
        projection = projection_outputs(
            residual,
            values["P_delta_w_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_delta_w_abs"],
        )
    passed = not missing
    return {
        "delta_w_species_abs": fmt(residual),
        "relative_weight_residual_abs": fmt(residual),
        "JH_DqZ_injection_abs": "MISSING_NUMERIC_VALUE",
        "density_qbasic_feed_abs": fmt(residual),
        "qbar_XT_delta_w_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_delta_w_feed_abs": fmt(projection["BY5"]),
        "delta_w_status": "FINITE_NOHOM_RESIDUAL_ROW_READY" if passed else "FINITE_NOHOM_RESIDUAL_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "NOHOM_RESIDUAL_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_NOHOM_RESIDUAL_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_DELTA_W_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "delta_w_zero":
        result = evaluate_zero(row)
    elif route_type == "delta_w_bound":
        result = evaluate_delta_w_bound(row)
    elif route_type == "nohom_residual_bound":
        result = evaluate_nohom_bound(row)
    else:
        result = {
            "delta_w_species_abs": "MISSING_NUMERIC_VALUE",
            "relative_weight_residual_abs": "MISSING_NUMERIC_VALUE",
            "JH_DqZ_injection_abs": "MISSING_NUMERIC_VALUE",
            "density_qbasic_feed_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_delta_w_feed_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_delta_w_feed_abs": "MISSING_NUMERIC_VALUE",
            "delta_w_status": "UNKNOWN_ROUTE_TYPE",
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
        raise SystemExit("usage: single_action_density_delta_w_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
