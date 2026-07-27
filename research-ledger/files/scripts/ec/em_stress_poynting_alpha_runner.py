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
    "observed_hodge_coframe_signed",
    "minimal_maxwell_action_signed",
    "unique_F2_parent_owner_signed",
    "fixed_charge_current_normalization_signed",
    "alpha_superselection_signed",
    "no_nonminimal_XF2_signed",
    "poynting_boundary_flux_zero_signed",
    "matter_EM_exchange_total_stress_signed",
    "readout_radiative_closure_signed",
    "no_unit_rescaling_alpha_signed",
    "no_measured_GM_absorption_signed",
)

EM_RESIDUAL_FIELDS = (
    "epsilon_EM_bound_abs",
    "Delta_Hodge_EM_abs",
    "w_EM_abs",
    "C_XF2_abs",
    "C_JQ_abs",
    "Phi_EM_rad_abs",
    "C_EM_readout_abs",
    "epsilon_internal_exchange_abs",
    "P_EM_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_EM_abs",
)

ALPHA_IDENTITY_FIELDS = (
    "z_g_abs",
    "z_lambda_abs",
    "C_EM_readout_abs",
    "K_alpha_clock_abs",
    "tau_clock_abs",
    "beta_source_alpha_abs",
    "tau_WEP_abs",
    "P_alpha_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_alpha_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ALPHA_ZERO_BY_POLICY_ONLY",
    "BOUND_FIELD_MASS_DOUBLE_COUNT",
    "CALIBRATED_ALPHA_AS_DERIVED",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CHARGE_NORMALIZATION_CHEAT",
    "DROPPED_XF2",
    "GR_IMPORT",
    "HODGE_MATCH_BY_ASSERTION",
    "MEASURED_GM_AS_SOURCE",
    "POYNTING_FLUX_IGNORED",
    "READOUT_ABSORPTION",
    "UNIQUE_F2_BY_AESTHETIC",
    "UNIT_RESCALING_AS_ZERO",
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


def zero_outputs(status: str, passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "maxwell_stress_residual_abs": zero,
        "poynting_flux_residual_abs": zero,
        "alpha_drift_residual_abs": zero,
        "EM_total_residual_abs": zero,
        "qbar_XT_EM_feed_abs": zero,
        "alpha_source_abs": zero,
        "BY5_EM_feed_abs": zero,
        "EM_status": status,
        "route_pass": passed,
        "runner_status": "EM_STRESS_ALPHA_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_EM_STRESS_ALPHA_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def projection_outputs(total: float | None, P: float | None, Qbar: float | None, K: float | None, tau: float | None) -> dict[str, float | None]:
    if None in (total, P, Qbar, K, tau):
        return {"qbar": None, "alpha": None, "BY5": None}
    qbar = P * total
    return {"qbar": qbar, "alpha": K * Qbar * qbar, "BY5": tau * qbar}


def evaluate_em_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    status = "MAXWELL_STRESS_POYNTING_ALPHA_OWNER_SIGNED" if passed else "MAXWELL_STRESS_POYNTING_ALPHA_OWNER_UNSIGNED"
    return zero_outputs(status, passed, missing)


def evaluate_em_residual_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in EM_RESIDUAL_FIELDS}
    maxwell = None
    poynting = None
    alpha_drift = None
    total = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        maxwell = (
            values["epsilon_EM_bound_abs"]
            + values["Delta_Hodge_EM_abs"]
            + values["w_EM_abs"]
            + values["C_JQ_abs"]
            + values["epsilon_internal_exchange_abs"]
        )
        poynting = values["Phi_EM_rad_abs"]
        alpha_drift = values["C_XF2_abs"] + values["w_EM_abs"] + values["C_JQ_abs"] + values["C_EM_readout_abs"]
        total = maxwell + poynting + alpha_drift
        projection = projection_outputs(
            total,
            values["P_EM_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_EM_abs"],
        )
    passed = not missing
    return {
        "maxwell_stress_residual_abs": fmt(maxwell),
        "poynting_flux_residual_abs": fmt(poynting),
        "alpha_drift_residual_abs": fmt(alpha_drift),
        "EM_total_residual_abs": fmt(total),
        "qbar_XT_EM_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_EM_feed_abs": fmt(projection["BY5"]),
        "EM_status": "FINITE_EM_STRESS_POYNTING_ALPHA_ROW_READY" if passed else "FINITE_EM_STRESS_POYNTING_ALPHA_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "EM_RESIDUAL_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_EM_RESIDUAL_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_alpha_identity_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in ALPHA_IDENTITY_FIELDS}
    b_alpha = None
    clock_product = None
    WEP_product = None
    total = None
    projection = {"qbar": None, "alpha": None, "BY5": None}
    if not missing:
        b_alpha = 2.0 * values["z_g_abs"] + values["z_lambda_abs"] + values["C_EM_readout_abs"]
        clock_product = values["K_alpha_clock_abs"] * values["tau_clock_abs"] * b_alpha
        WEP_product = values["beta_source_alpha_abs"] * values["tau_WEP_abs"] * b_alpha
        total = b_alpha + clock_product + WEP_product
        projection = projection_outputs(
            total,
            values["P_alpha_qbar_abs"],
            values["Qbar_source_XH_bound_abs"],
            values["K_source_abs"],
            values["tau_BY5_alpha_abs"],
        )
    passed = not missing
    return {
        "maxwell_stress_residual_abs": "MISSING_NUMERIC_VALUE" if passed else "MISSING_NUMERIC_VALUE",
        "poynting_flux_residual_abs": fmt(clock_product),
        "alpha_drift_residual_abs": fmt(b_alpha),
        "EM_total_residual_abs": fmt(total),
        "qbar_XT_EM_feed_abs": fmt(projection["qbar"]),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_EM_feed_abs": fmt(projection["BY5"]),
        "EM_status": "FINITE_ALPHA_IDENTITY_PRODUCT_ROW_READY" if passed else "FINITE_ALPHA_IDENTITY_PRODUCT_ROW_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "ALPHA_IDENTITY_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_ALPHA_IDENTITY_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "maxwell_stress_residual_abs": "MISSING_NUMERIC_VALUE",
        "poynting_flux_residual_abs": "MISSING_NUMERIC_VALUE",
        "alpha_drift_residual_abs": "MISSING_NUMERIC_VALUE",
        "EM_total_residual_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_EM_feed_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_EM_feed_abs": "MISSING_NUMERIC_VALUE",
        "EM_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_EM_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    if forbidden_source_used(row):
        return forbidden_result(row_id, route_type, route)
    output: dict[str, Any] = {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if route_type == "em_zero":
        result = evaluate_em_zero(row)
    elif route_type == "em_residual_bound":
        result = evaluate_em_residual_bound(row)
    elif route_type == "alpha_identity_bound":
        result = evaluate_alpha_identity_bound(row)
    else:
        result = {
            "maxwell_stress_residual_abs": "MISSING_NUMERIC_VALUE",
            "poynting_flux_residual_abs": "MISSING_NUMERIC_VALUE",
            "alpha_drift_residual_abs": "MISSING_NUMERIC_VALUE",
            "EM_total_residual_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_EM_feed_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_EM_feed_abs": "MISSING_NUMERIC_VALUE",
            "EM_status": "UNKNOWN_ROUTE_TYPE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    output.update(result)
    output["anti_circularity_status"] = "PASS_NO_FORBIDDEN_SOURCE_USED" if output["route_pass"] else output.get(
        "anti_circularity_status", "PASS_NO_FORBIDDEN_SOURCE_USED"
    )
    return output


def read_csv(path: Path) -> list[dict[str, Any]]:
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
        print("Usage: em_stress_poynting_alpha_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
