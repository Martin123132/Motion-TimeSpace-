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

DESCENT_ZERO_FIELDS = (
    "parent_action_diffeomorphic_signed",
    "q_observed_map_signed",
    "matter_action_pullback_signed",
    "variation_before_readout_signed",
    "same_frame_tau_n_dSigma_signed",
    "Hilbert_density_qbasic_signed",
    "compact_worldtube_support_signed",
    "Hamiltonian_surface_charge_match_signed",
    "H_ref_branch_fixed_signed",
    "PiM_identity_chainmap_signed",
    "ordinary_EM_stress_included_once_signed",
    "no_source_only_weights_signed",
    "no_nonHilbert_source_bypass_signed",
    "no_boundary_source_layer_signed",
    "positive_MHref_signed",
    "no_measured_GM_absorption_signed",
)

DESCENT_BOUND_FIELDS = (
    "E_action_pullback_abs",
    "E_variation_readout_abs",
    "E_measure_qbasic_abs",
    "E_tau_frame_abs",
    "E_EM_once_abs",
    "E_theta_constants_abs",
    "E_worldtube_boundary_abs",
    "E_nonHilbert_current_abs",
    "E_PiM_Htau_abs",
    "E_readout_mask_abs",
    "P_Newton_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_MHref_abs",
)

DIRECT_MHREF_FIELDS = (
    "H_tau_outer_abs",
    "H_ref_abs",
    "integral_rhoH_abs",
    "M_H_ref_abs",
    "reference_tolerance_abs",
    "volume_tolerance_abs",
    "P_Newton_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_MHref_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_SHORTCUT",
    "CANCEL_UNKNOWN_COMPONENTS",
    "DENSITY_QBASIC_BY_ASSERTION",
    "EM_STRESS_DROPPED",
    "GR_IMPORT",
    "HILBERT_CURRENT_BY_NAME_ONLY",
    "MEASURED_GM_AS_SOURCE",
    "MHREF_FROM_FIT",
    "NONHILBERT_BYPASS_IGNORED",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
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


def positive(row: dict[str, Any], field: str, missing: list[str]) -> float | None:
    value = nonnegative(row, field, missing)
    if value is not None and value <= 0.0:
        missing.append(f"NONPOSITIVE_{field}")
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
        "source_descent_residual_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_surface_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_volume_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "delta_MHref_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_MHref_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_MHref_feed_abs": "MISSING_NUMERIC_VALUE",
        "source_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_descent_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in DESCENT_ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    mhref = "THEOREM_POSITIVE_DEFINED" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "source_descent_residual_abs": zero,
        "M_H_ref_abs": mhref,
        "M_H_ref_calc_abs": mhref,
        "M_H_ref_surface_mismatch_abs": zero,
        "M_H_ref_volume_mismatch_abs": zero,
        "delta_MHref_abs": zero,
        "qbar_XT_MHref_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_MHref_feed_abs": zero,
        "source_status": "HILBERT_SOURCE_MHREF_DESCENT_ZERO_SIGNED" if passed else "HILBERT_SOURCE_MHREF_DESCENT_ZERO_UNSIGNED",
        "route_pass": passed,
        "runner_status": "HILBERT_SOURCE_DESCENT_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_HILBERT_SOURCE_DESCENT_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_descent_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in DESCENT_BOUND_FIELDS}
    residual = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        residual = sum(values[field] for field in DESCENT_BOUND_FIELDS[:10])
        projection = projection_outputs(
            residual,
            values["P_Newton_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_MHref_abs"],
        )
    passed = not missing
    return {
        "source_descent_residual_abs": fmt(residual),
        "M_H_ref_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_surface_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_volume_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "delta_MHref_abs": fmt(residual),
        "qbar_XT_MHref_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_MHref_feed_abs": fmt(projection["BY5"]),
        "source_status": "FINITE_HILBERT_SOURCE_DESCENT_ROW_READY" if passed else "FINITE_HILBERT_SOURCE_DESCENT_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "HILBERT_SOURCE_DESCENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_HILBERT_SOURCE_DESCENT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_direct_mhref_source(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in DIRECT_MHREF_FIELDS}
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    M_calc = None
    surface_mismatch = None
    volume_mismatch = None
    delta = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if values["H_tau_outer_abs"] is not None and values["H_ref_abs"] is not None:
        M_calc = values["H_tau_outer_abs"] - values["H_ref_abs"]
        if M_calc <= 0.0:
            missing.append("NONPOSITIVE_H_tau_minus_H_ref")
            M_calc = None
    if M_calc is not None and M_H_ref is not None:
        surface_mismatch = abs(M_calc - M_H_ref)
        if values["reference_tolerance_abs"] is not None and surface_mismatch > values["reference_tolerance_abs"]:
            missing.append("SURFACE_MHREF_MISMATCH")
    if values["integral_rhoH_abs"] is not None and M_H_ref is not None:
        volume_mismatch = abs(values["integral_rhoH_abs"] - M_H_ref)
        if values["volume_tolerance_abs"] is not None and volume_mismatch > values["volume_tolerance_abs"]:
            missing.append("VOLUME_MHREF_MISMATCH")
    if surface_mismatch is not None and volume_mismatch is not None and M_H_ref is not None:
        delta = (surface_mismatch + volume_mismatch) / M_H_ref
        projection = projection_outputs(
            delta,
            values["P_Newton_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_MHref_abs"],
        )
    passed = not missing
    return {
        "source_descent_residual_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "M_H_ref_abs": fmt(M_H_ref),
        "M_H_ref_calc_abs": fmt(M_calc),
        "M_H_ref_surface_mismatch_abs": fmt(surface_mismatch),
        "M_H_ref_volume_mismatch_abs": fmt(volume_mismatch),
        "delta_MHref_abs": fmt(delta),
        "qbar_XT_MHref_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_MHref_feed_abs": fmt(projection["BY5"]),
        "source_status": "DIRECT_MHREF_SOURCE_ROW_READY" if passed else "DIRECT_MHREF_SOURCE_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_MHREF_SOURCE_ROW_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_MHREF_SOURCE_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_HILBERT_SOURCE_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "source_descent_zero":
        result = evaluate_descent_zero(row)
    elif route_type == "source_descent_bound":
        result = evaluate_descent_bound(row)
    elif route_type == "direct_MHref_source":
        result = evaluate_direct_mhref_source(row)
    else:
        result = {
            "source_descent_residual_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_surface_mismatch_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_volume_mismatch_abs": "MISSING_NUMERIC_VALUE",
            "delta_MHref_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_MHref_feed_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_MHref_feed_abs": "MISSING_NUMERIC_VALUE",
            "source_status": "UNKNOWN_ROUTE_TYPE",
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
        raise SystemExit("usage: hilbert_source_MHref_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
