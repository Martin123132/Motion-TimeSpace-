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

OWNER_FIELDS = (
    "theta_Y_signed",
    "omega_Y_signed",
    "DC_X_operator_signed",
    "DCdagger_formula_signed",
    "omega_flat_match_signed",
    "vertical_action_all_fields_signed",
    "boundary_differentiability_signed",
    "Bct_cancels_boundary_covector_signed",
    "reduced_nondegeneracy_signed",
    "matter_quotient_signed",
    "constant_sector_descends_signed",
    "no_physical_charge_removed_signed",
    "no_measured_GM_absorption_signed",
)

DIRECT_FIELDS = (
    "omega_DC_mismatch_abs",
    "unmapped_vertical_action_abs",
    "boundary_covector_abs",
    "Bct_mismatch_abs",
    "reduced_degeneracy_residual_abs",
    "matter_quotient_residual_abs",
    "constant_marker_residual_abs",
    "M_H_ref_min_abs",
    "PiM_norm_abs",
    "K_source_abs",
    "tau_BY5_source_abs",
)

COMPONENT_FIELDS = (
    "theta_gap_abs",
    "omega_gap_abs",
    "DC_operator_gap_abs",
    "DCdagger_gap_abs",
    "omega_flat_match_gap_abs",
    "vertical_map_gap_abs",
    "boundary_differentiability_gap_abs",
    "Bct_mismatch_abs",
    "matter_descent_gap_abs",
    "constant_descent_gap_abs",
    "M_H_ref_min_abs",
    "PiM_norm_abs",
    "K_source_abs",
    "tau_BY5_source_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CLOSURE_ONLY_QUOTIENT",
    "CONSTANTS_SILENT_BY_ASSERTION",
    "DC_DAGGER_EQUALS_VECTOR",
    "DC_OPERATOR_INSERTED",
    "FIT_TO_BOUND",
    "FORMULA_ONLY_THETA",
    "GR_IMPORT",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "OMEGA_BY_ANALOGY",
    "ORBITAL_GM_AS_SOURCE",
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


def positive(row: dict[str, Any], field: str, missing: list[str]) -> float | None:
    value = nonnegative(row, field, missing)
    if value is not None and value <= 0.0:
        missing.append(f"NONPOSITIVE_{field}")
        return None
    return value


def zero_outputs(status: str, passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "source_coupling_residual_abs": zero,
        "Qbar_source_XH_bound_abs": zero,
        "qbar_XT_bound_abs": zero,
        "alpha_source_abs": zero,
        "BY5_source_feed_abs": zero,
        "theta_omega_DC_status": status,
        "route_pass": passed,
        "runner_status": "THETA_OMEGA_DC_OWNER_PASS_NONCLAIM" if passed else "BLOCKED_THETA_OMEGA_DC_OWNER_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_owner(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in OWNER_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    status = "THETA_OMEGA_DC_OWNER_SIGNED" if passed else "THETA_OMEGA_DC_OWNER_UNSIGNED"
    return zero_outputs(status, passed, missing)


def projection_outputs(
    residual: float | None,
    qbar_test: float | None,
    M_H_ref: float | None,
    PiM_norm: float | None,
    K_source: float | None,
    tau: float | None,
) -> dict[str, float | None]:
    if None in (residual, qbar_test, M_H_ref, PiM_norm, K_source, tau) or M_H_ref <= 0.0:
        return {"Qbar": None, "alpha": None, "BY5": None}
    Qbar = PiM_norm * residual / M_H_ref
    return {
        "Qbar": Qbar,
        "alpha": K_source * Qbar * qbar_test,
        "BY5": tau * Qbar,
    }


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {
        field: positive(row, field, missing) if field == "M_H_ref_min_abs" else nonnegative(row, field, missing)
        for field in DIRECT_FIELDS
    }
    residual = None
    qbar = None
    projection = {"Qbar": None, "alpha": None, "BY5": None}
    if not missing:
        qbar = values["matter_quotient_residual_abs"] + values["constant_marker_residual_abs"]
        residual = (
            values["omega_DC_mismatch_abs"]
            + values["unmapped_vertical_action_abs"]
            + values["boundary_covector_abs"]
            + values["Bct_mismatch_abs"]
            + values["reduced_degeneracy_residual_abs"]
            + qbar
        )
        projection = projection_outputs(
            residual,
            qbar,
            values["M_H_ref_min_abs"],
            values["PiM_norm_abs"],
            values["K_source_abs"],
            values["tau_BY5_source_abs"],
        )
    passed = not missing
    return {
        "source_coupling_residual_abs": fmt(residual),
        "Qbar_source_XH_bound_abs": fmt(projection["Qbar"]),
        "qbar_XT_bound_abs": fmt(qbar),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_source_feed_abs": fmt(projection["BY5"]),
        "theta_omega_DC_status": "FINITE_DIRECT_SOURCE_COUPLING_BOUND_READY" if passed else "FINITE_DIRECT_SOURCE_COUPLING_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_SOURCE_COUPLING_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {
        field: positive(row, field, missing) if field == "M_H_ref_min_abs" else nonnegative(row, field, missing)
        for field in COMPONENT_FIELDS
    }
    residual = None
    qbar = None
    projection = {"Qbar": None, "alpha": None, "BY5": None}
    if not missing:
        qbar = values["matter_descent_gap_abs"] + values["constant_descent_gap_abs"]
        residual = (
            values["theta_gap_abs"]
            + values["omega_gap_abs"]
            + values["DC_operator_gap_abs"]
            + values["DCdagger_gap_abs"]
            + values["omega_flat_match_gap_abs"]
            + values["vertical_map_gap_abs"]
            + values["boundary_differentiability_gap_abs"]
            + values["Bct_mismatch_abs"]
            + qbar
        )
        projection = projection_outputs(
            residual,
            qbar,
            values["M_H_ref_min_abs"],
            values["PiM_norm_abs"],
            values["K_source_abs"],
            values["tau_BY5_source_abs"],
        )
    passed = not missing
    return {
        "source_coupling_residual_abs": fmt(residual),
        "Qbar_source_XH_bound_abs": fmt(projection["Qbar"]),
        "qbar_XT_bound_abs": fmt(qbar),
        "alpha_source_abs": fmt(projection["alpha"]),
        "BY5_source_feed_abs": fmt(projection["BY5"]),
        "theta_omega_DC_status": "FINITE_COMPONENT_SOURCE_COUPLING_BOUND_READY" if passed else "FINITE_COMPONENT_SOURCE_COUPLING_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_SOURCE_COUPLING_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "source_coupling_residual_abs": "MISSING_NUMERIC_VALUE",
        "Qbar_source_XH_bound_abs": "MISSING_NUMERIC_VALUE",
        "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
        "alpha_source_abs": "MISSING_NUMERIC_VALUE",
        "BY5_source_feed_abs": "MISSING_NUMERIC_VALUE",
        "theta_omega_DC_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_THETA_OMEGA_DC_ROW"
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
    if route_type == "theta_omega_DC_owner":
        result = evaluate_owner(row)
    elif route_type == "direct_source_coupling_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "component_source_coupling_bound":
        result = evaluate_component_bound(row)
    else:
        result = {
            "source_coupling_residual_abs": "MISSING_NUMERIC_VALUE",
            "Qbar_source_XH_bound_abs": "MISSING_NUMERIC_VALUE",
            "qbar_XT_bound_abs": "MISSING_NUMERIC_VALUE",
            "alpha_source_abs": "MISSING_NUMERIC_VALUE",
            "BY5_source_feed_abs": "MISSING_NUMERIC_VALUE",
            "theta_omega_DC_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: parent_theta_omega_DC_operator_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
