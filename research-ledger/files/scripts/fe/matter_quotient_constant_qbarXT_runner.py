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
    "q_map_signed",
    "observed_geometry_functor_signed",
    "matter_functor_signed",
    "constants_superselection_signed",
    "no_material_marker_signed",
    "matter_lift_signed",
    "worldtube_support_signed",
    "boundary_no_flux_signed",
    "no_direct_matter_X_vertex_signed",
    "universal_source_current_signed",
    "nonHilbert_current_zero_signed",
    "no_post_readout_EFT_signed",
    "no_physical_charge_removed_signed",
    "no_measured_GM_absorption_signed",
)

DIRECT_FIELDS = (
    "A_geom_matter_abs",
    "A_theta_matter_abs",
    "A_lift_matter_abs",
    "A_marker_matter_abs",
    "A_direct_matter_abs",
    "A_worldtube_matter_abs",
    "A_boundary_matter_abs",
    "A_source_weight_abs",
    "A_nonHilbert_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_qbar_abs",
)

COMPONENT_FIELDS = (
    "common_frame_log_derivative_abs",
    "d_ln_alpha_EM_dXhat_abs",
    "d_ln_mass_ratio_dXhat_abs",
    "marker_coupling_projection_abs",
    "species_source_weight_splitting_abs",
    "nonHilbert_current_projection_abs",
    "direct_vertex_projection_abs",
    "worldtube_support_projection_abs",
    "boundary_tail_projection_abs",
    "P_A_qbarXT_vec_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_qbar_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CLOSURE_ONLY_QUOTIENT",
    "CONSTANTS_SILENT_BY_ASSERTION",
    "DIRECT_VERTEX_DROPPED",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "HIDDEN_FRAME_IGNORED",
    "MARKER_IGNORED",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_EFT_AS_FUNDAMENTAL",
    "QBAR_ZERO_BY_POLICY_ONLY",
    "REFERENCE_ONLY_ZERO",
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
        "matter_descent_residual_abs": zero,
        "constant_marker_residual_abs": zero,
        "qbar_XT_bound_abs": zero,
        "alpha_source_abs": zero,
        "BY5_qbar_feed_abs": zero,
        "qbarXT_status": status,
        "route_pass": passed,
        "runner_status": "QBARXT_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_QBARXT_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    status = "MATTER_QUOTIENT_CONSTANT_ZERO_SIGNED" if passed else "MATTER_QUOTIENT_CONSTANT_ZERO_UNSIGNED"
    return zero_outputs(status, passed, missing)


def alpha_outputs(qbar: float | None, Qbar: float | None, K: float | None, tau: float | None) -> dict[str, float | None]:
    if None in (qbar, Qbar, K, tau):
        return {"alpha": None, "BY5": None}
    return {"alpha": K * Qbar * qbar, "BY5": tau * qbar}


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in DIRECT_FIELDS}
    matter = None
    constants = None
    qbar = None
    projection = {"alpha": None, "BY5": None}
    if not missing:
        matter = (
            values["A_geom_matter_abs"]
            + values["A_lift_matter_abs"]
            + values["A_direct_matter_abs"]
            + values["A_worldtube_matter_abs"]
            + values["A_boundary_matter_abs"]
            + values["A_source_weight_abs"]
            + values["A_nonHilbert_abs"]
        )
        constants = values["A_theta_matter_abs"] + values["A_marker_matter_abs"]
        qbar = matter + constants
        projection = alpha_outputs(qbar, values["Qbar_source_XH_bound_abs"], values["K_source_abs"], values["tau_BY5_qbar_abs"])
    passed = not missing
    return {
        "matter_descent_residual_abs": fmt(matter),
        "constant_marker_residual_abs": fmt(constants),
        "qbar_XT_bound_abs": fmt(qbar),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_qbar_feed_abs": fmt(projection["BY5"]),
        "qbarXT_status": "FINITE_DIRECT_QBARXT_BOUND_READY" if passed else "FINITE_DIRECT_QBARXT_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_QBARXT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_QBARXT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in COMPONENT_FIELDS}
    matter = None
    constants = None
    qbar = None
    projection = {"alpha": None, "BY5": None}
    if not missing:
        geometry = values["common_frame_log_derivative_abs"]
        constants = values["d_ln_alpha_EM_dXhat_abs"] + values["d_ln_mass_ratio_dXhat_abs"] + values["marker_coupling_projection_abs"]
        matter = (
            geometry
            + values["species_source_weight_splitting_abs"]
            + values["nonHilbert_current_projection_abs"]
            + values["direct_vertex_projection_abs"]
            + values["worldtube_support_projection_abs"]
            + values["boundary_tail_projection_abs"]
        )
        qbar = values["P_A_qbarXT_vec_abs"] * (matter + constants)
        projection = alpha_outputs(qbar, values["Qbar_source_XH_bound_abs"], values["K_source_abs"], values["tau_BY5_qbar_abs"])
    passed = not missing
    return {
        "matter_descent_residual_abs": fmt(matter),
        "constant_marker_residual_abs": fmt(constants),
        "qbar_XT_bound_abs": fmt(qbar),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_qbar_feed_abs": fmt(projection["BY5"]),
        "qbarXT_status": "FINITE_COMPONENT_QBARXT_BOUND_READY" if passed else "FINITE_COMPONENT_QBARXT_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_QBARXT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_QBARXT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "matter_descent_residual_abs": "MISSING_NUMERIC_VALUE",
        "constant_marker_residual_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_qbar_feed_abs": "MISSING_NUMERIC_VALUE",
        "qbarXT_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_QBARXT_ROW"
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
    if route_type == "qbarXT_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_qbarXT_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "component_qbarXT_bound":
        result = evaluate_component_bound(row)
    else:
        result = {
            "matter_descent_residual_abs": "MISSING_NUMERIC_VALUE",
            "constant_marker_residual_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_qbar_feed_abs": "MISSING_NUMERIC_VALUE",
            "qbarXT_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: matter_quotient_constant_qbarXT_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
