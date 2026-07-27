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
    "EH_or_linearized_operator_signed",
    "Hilbert_source_current_signed",
    "kappa_constant_or_parent_owned_signed",
    "Gref_to_GN_readout_signed",
    "MHref_positive_same_frame_signed",
    "PiM_Htau_chainmap_signed",
    "worldtube_support_signed",
    "EM_stress_included_once_signed",
    "no_nonHilbert_bypass_signed",
    "no_source_prefactor_signed",
    "Poisson_Gauss_limit_signed",
    "PPN_residual_vector_zero_signed",
    "no_measured_GM_absorption_signed",
)

SOURCE_BOUND_FIELDS = (
    "delta_kappa_abs",
    "delta_Gref_abs",
    "delta_MHref_abs",
    "delta_PiM_Htau_abs",
    "delta_worldtube_abs",
    "delta_EM_stress_abs",
    "delta_nonHilbert_abs",
    "delta_source_prefactor_abs",
    "delta_Poisson_operator_abs",
    "delta_PPN_vector_abs",
    "P_Newton_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_Newton_abs",
)

POISSON_COEFFICIENT_FIELDS = (
    "delta_kappa_abs",
    "delta_ZH_abs",
    "delta_GN_readout_abs",
    "delta_E00_abs",
    "delta_MH_abs",
    "P_Newton_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_Newton_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "CALIBRATED_G_AS_DERIVED",
    "CANCEL_UNKNOWN_COMPONENTS",
    "EM_STRESS_DOUBLE_COUNT",
    "GR_IMPORT",
    "KAPPA_CONSTANT_BY_ASSERTION",
    "MEASURED_GM_AS_SOURCE",
    "MISSING_DENOMINATOR_FILLED_BY_FIT",
    "NONHILBERT_BYPASS_IGNORED",
    "ORBITAL_GM_AS_SOURCE",
    "PIM_HTAU_BY_ASSERTION",
    "PPN_ZERO_BY_POLICY_ONLY",
    "SOURCE_PREFACTOR_IGNORED",
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


def projection_outputs(total: float | None, P: float | None, Qbar: float | None, K: float | None, tau: float | None) -> dict[str, float | None]:
    if None in (total, P, Qbar, K, tau):
        return {"qbar": None, "alpha": None, "BY5": None}
    qbar = P * total
    return {"qbar": qbar, "alpha": K * Qbar * qbar, "BY5": tau * qbar}


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "source_denominator_residual_abs": "MISSING_NUMERIC_VALUE",
        "Newton_Poisson_residual_abs": "MISSING_NUMERIC_VALUE",
        "PPN_local_residual_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_Newton_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_Newton_feed_abs": "MISSING_NUMERIC_VALUE",
        "G_eff_coefficient_residual_abs": "MISSING_NUMERIC_VALUE",
        "Newton_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def zero_result(row: dict[str, Any], passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "source_denominator_residual_abs": zero,
        "Newton_Poisson_residual_abs": zero,
        "PPN_local_residual_abs": zero,
        "qbar_XT_Newton_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_Newton_feed_abs": zero,
        "G_eff_coefficient_residual_abs": zero,
        "Newton_status": "KAPPA_G_SOURCE_NEWTON_ZERO_SIGNED" if passed else "KAPPA_G_SOURCE_NEWTON_ZERO_UNSIGNED",
        "route_pass": passed,
        "runner_status": "NEWTON_SOURCE_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_NEWTON_SOURCE_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    return zero_result(row, not missing, missing)


def evaluate_source_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in SOURCE_BOUND_FIELDS}
    source_denominator = None
    newton_poisson = None
    ppn_local = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        source_denominator = (
            values["delta_kappa_abs"]
            + values["delta_Gref_abs"]
            + values["delta_MHref_abs"]
            + values["delta_PiM_Htau_abs"]
            + values["delta_worldtube_abs"]
            + values["delta_EM_stress_abs"]
            + values["delta_nonHilbert_abs"]
            + values["delta_source_prefactor_abs"]
        )
        newton_poisson = source_denominator + values["delta_Poisson_operator_abs"]
        ppn_local = newton_poisson + values["delta_PPN_vector_abs"]
        projection = projection_outputs(
            ppn_local,
            values["P_Newton_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_Newton_abs"],
        )
    passed = not missing
    return {
        "source_denominator_residual_abs": fmt(source_denominator),
        "Newton_Poisson_residual_abs": fmt(newton_poisson),
        "PPN_local_residual_abs": fmt(ppn_local),
        "qbar_XT_Newton_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_Newton_feed_abs": fmt(projection["BY5"]),
        "G_eff_coefficient_residual_abs": "MISSING_NUMERIC_VALUE",
        "Newton_status": "FINITE_NEWTON_SOURCE_RESIDUAL_ROW_READY" if passed else "FINITE_NEWTON_SOURCE_RESIDUAL_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "NEWTON_SOURCE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_NEWTON_SOURCE_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_poisson_coefficient_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in POISSON_COEFFICIENT_FIELDS}
    coefficient = None
    newton_poisson = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        coefficient = values["delta_kappa_abs"] + values["delta_ZH_abs"] + values["delta_GN_readout_abs"]
        newton_poisson = coefficient + values["delta_E00_abs"] + values["delta_MH_abs"]
        projection = projection_outputs(
            newton_poisson,
            values["P_Newton_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_Newton_abs"],
        )
    passed = not missing
    return {
        "source_denominator_residual_abs": fmt(values.get("delta_MH_abs") if not missing else None),
        "Newton_Poisson_residual_abs": fmt(newton_poisson),
        "PPN_local_residual_abs": fmt(newton_poisson),
        "qbar_XT_Newton_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_Newton_feed_abs": fmt(projection["BY5"]),
        "G_eff_coefficient_residual_abs": fmt(coefficient),
        "Newton_status": "FINITE_POISSON_COEFFICIENT_ROW_READY" if passed else "FINITE_POISSON_COEFFICIENT_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "POISSON_COEFFICIENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_POISSON_COEFFICIENT_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip()
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "newton_zero":
        result = evaluate_zero(row)
    elif route_type == "newton_source_bound":
        result = evaluate_source_bound(row)
    elif route_type == "poisson_coefficient_bound":
        result = evaluate_poisson_coefficient_bound(row)
    else:
        result = {
            "source_denominator_residual_abs": "MISSING_NUMERIC_VALUE",
            "Newton_Poisson_residual_abs": "MISSING_NUMERIC_VALUE",
            "PPN_local_residual_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_Newton_feed_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_Newton_feed_abs": "MISSING_NUMERIC_VALUE",
            "G_eff_coefficient_residual_abs": "MISSING_NUMERIC_VALUE",
            "Newton_status": "UNKNOWN_ROUTE_TYPE",
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
        raise SystemExit("usage: kappa_G_source_Newton_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
