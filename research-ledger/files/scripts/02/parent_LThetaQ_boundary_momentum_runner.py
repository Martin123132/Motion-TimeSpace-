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

PARENT_FORMULA_FIELDS = (
    "parent_LX_signed",
    "theta_X_signed",
    "Q_X_signed",
    "omega_X_signed",
    "vertical_generator_signed",
    "DC_operator_signed",
    "Bct_reference_owner_signed",
    "boundary_condition_lock_signed",
    "hodge_domain_signed",
    "no_physical_charge_removed_signed",
    "no_measured_GM_absorption_signed",
)

HODGE_FIELDS = (
    "C_hodge_abs",
    "spectral_gap_lambda1_abs",
    "B_exact_norm_abs",
    "norm_dS_Feps_abs",
    "corner_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "K_boundary_abs",
    "M_H_ref_min_abs",
    "PiM_norm_abs",
    "K_edge_abs",
    "qbar_XT_abs",
    "tau_BY5_edge_abs",
)

COMPONENT_FIELDS = (
    "C_hodge_abs",
    "spectral_gap_lambda1_abs",
    "B_parent_pullback_norm_abs",
    "Bct_norm_abs",
    "DC_boundary_covector_norm_abs",
    "reference_mismatch_norm_abs",
    "norm_dS_Feps_abs",
    "corner_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "K_boundary_abs",
    "M_H_ref_min_abs",
    "PiM_norm_abs",
    "K_edge_abs",
    "qbar_XT_abs",
    "tau_BY5_edge_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CLOSURE_ONLY_QUOTIENT",
    "FIT_TO_BOUND",
    "FORMULA_ONLY_LTHETAQ",
    "GR_IMPORT",
    "HODGE_WITH_UNCONTROLLED_HARMONIC",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POINCARE_WITHOUT_SPECTRAL_GAP",
    "REFERENCE_ONLY_ZERO",
    "SYMBOLIC_BX_NORM",
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


def empty_numeric(parent_status: str, passed: bool, missing: list[str]) -> dict[str, Any]:
    return {
        "B_X_pullback_norm_abs": "MISSING_NUMERIC_VALUE",
        "norm_bX_bound_abs": "MISSING_NUMERIC_VALUE",
        "Q_edge_kernel_feed_abs": "MISSING_NUMERIC_VALUE",
        "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
        "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE",
        "alpha_edge_abs": "MISSING_NUMERIC_VALUE",
        "BY5_edge_feed_abs": "MISSING_NUMERIC_VALUE",
        "parent_boundary_status": parent_status,
        "route_pass": passed,
        "runner_status": "PARENT_LTHETAQ_BOUNDARY_MOMENTUM_SIGNED_NONCLAIM" if passed else "BLOCKED_PARENT_LTHETAQ_BOUNDARY_MOMENTUM_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_parent_formula(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in PARENT_FORMULA_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    status = "PARENT_NOETHER_BOUNDARY_FORMULA_OWNED" if passed else "PARENT_NOETHER_BOUNDARY_FORMULA_UNSIGNED"
    return empty_numeric(status, passed, missing)


def compute_bound(
    C_hodge: float,
    spectral_gap: float,
    B_exact_norm: float,
    norm_dS_Feps: float,
    corner: float,
    harmonic: float,
    residual: float,
    K_boundary: float,
    M_H_ref: float,
    PiM_norm: float,
    K_edge: float,
    qbar_XT: float,
    tau_BY5: float,
) -> dict[str, float]:
    norm_bX = C_hodge * B_exact_norm / math.sqrt(spectral_gap)
    kernel_feed = norm_dS_Feps * norm_bX
    Q_edge = corner + kernel_feed + harmonic + residual + K_boundary
    Qbar = PiM_norm * Q_edge / M_H_ref
    alpha = K_edge * Qbar * qbar_XT
    BY5 = tau_BY5 * Qbar
    return {
        "norm_bX": norm_bX,
        "kernel_feed": kernel_feed,
        "Q_edge": Q_edge,
        "Qbar": Qbar,
        "alpha": alpha,
        "BY5": BY5,
    }


def evaluate_hodge_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: positive(row, field, missing) if field in {"C_hodge_abs", "spectral_gap_lambda1_abs", "M_H_ref_min_abs"} else nonnegative(row, field, missing) for field in HODGE_FIELDS}
    result = None
    if not missing:
        result = compute_bound(
            values["C_hodge_abs"],
            values["spectral_gap_lambda1_abs"],
            values["B_exact_norm_abs"],
            values["norm_dS_Feps_abs"],
            values["corner_abs"],
            values["harmonic_edge_abs"],
            values["residual_edge_abs"],
            values["K_boundary_abs"],
            values["M_H_ref_min_abs"],
            values["PiM_norm_abs"],
            values["K_edge_abs"],
            values["qbar_XT_abs"],
            values["tau_BY5_edge_abs"],
        )
    passed = not missing
    return {
        "B_X_pullback_norm_abs": fmt(values.get("B_exact_norm_abs") if passed else None),
        "norm_bX_bound_abs": fmt(result["norm_bX"] if result else None),
        "Q_edge_kernel_feed_abs": fmt(result["kernel_feed"] if result else None),
        "Q_edge_bound_abs": fmt(result["Q_edge"] if result else None),
        "Qbar_edge_XH_bound_abs": fmt(result["Qbar"] if result else None),
        "alpha_edge_abs": fmt(result["alpha"] if result else None),
        "BY5_edge_feed_abs": fmt(result["BY5"] if result else None),
        "parent_boundary_status": "FINITE_HODGE_BX_NORM_BOUND_READY" if passed else "FINITE_HODGE_BX_NORM_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "HODGE_BX_NORM_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_HODGE_BX_NORM_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: positive(row, field, missing) if field in {"C_hodge_abs", "spectral_gap_lambda1_abs", "M_H_ref_min_abs"} else nonnegative(row, field, missing) for field in COMPONENT_FIELDS}
    B_exact_norm = None
    result = None
    if not missing:
        B_exact_norm = (
            values["B_parent_pullback_norm_abs"]
            + values["Bct_norm_abs"]
            + values["DC_boundary_covector_norm_abs"]
            + values["reference_mismatch_norm_abs"]
        )
        result = compute_bound(
            values["C_hodge_abs"],
            values["spectral_gap_lambda1_abs"],
            B_exact_norm,
            values["norm_dS_Feps_abs"],
            values["corner_abs"],
            values["harmonic_edge_abs"],
            values["residual_edge_abs"],
            values["K_boundary_abs"],
            values["M_H_ref_min_abs"],
            values["PiM_norm_abs"],
            values["K_edge_abs"],
            values["qbar_XT_abs"],
            values["tau_BY5_edge_abs"],
        )
    passed = not missing
    return {
        "B_X_pullback_norm_abs": fmt(B_exact_norm),
        "norm_bX_bound_abs": fmt(result["norm_bX"] if result else None),
        "Q_edge_kernel_feed_abs": fmt(result["kernel_feed"] if result else None),
        "Q_edge_bound_abs": fmt(result["Q_edge"] if result else None),
        "Qbar_edge_XH_bound_abs": fmt(result["Qbar"] if result else None),
        "alpha_edge_abs": fmt(result["alpha"] if result else None),
        "BY5_edge_feed_abs": fmt(result["BY5"] if result else None),
        "parent_boundary_status": "FINITE_COMPONENT_BX_NORM_BOUND_READY" if passed else "FINITE_COMPONENT_BX_NORM_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_BX_NORM_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_BX_NORM_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "B_X_pullback_norm_abs": "MISSING_NUMERIC_VALUE",
        "norm_bX_bound_abs": "MISSING_NUMERIC_VALUE",
        "Q_edge_kernel_feed_abs": "MISSING_NUMERIC_VALUE",
        "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
        "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE",
        "alpha_edge_abs": "MISSING_NUMERIC_VALUE",
        "BY5_edge_feed_abs": "MISSING_NUMERIC_VALUE",
        "parent_boundary_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_PARENT_LTHETAQ_ROW"
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
    if route_type == "parent_LThetaQ_formula":
        result = evaluate_parent_formula(row)
    elif route_type == "hodge_bX_norm_bound":
        result = evaluate_hodge_bound(row)
    elif route_type == "component_bX_norm_bound":
        result = evaluate_component_bound(row)
    else:
        result = {
            "B_X_pullback_norm_abs": "MISSING_NUMERIC_VALUE",
            "norm_bX_bound_abs": "MISSING_NUMERIC_VALUE",
            "Q_edge_kernel_feed_abs": "MISSING_NUMERIC_VALUE",
            "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
            "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE",
            "alpha_edge_abs": "MISSING_NUMERIC_VALUE",
            "BY5_edge_feed_abs": "MISSING_NUMERIC_VALUE",
            "parent_boundary_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: parent_LThetaQ_boundary_momentum_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
