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
    "parent_LThetaQ_boundary_momentum_signed",
    "boundary_counterterm_owner_signed",
    "compact_corner_free_domain_signed",
    "BX_exact_primitive_signed",
    "overlap_compatibility_signed",
    "pure_gauge_part_zero_signed",
    "harmonic_edge_zero_signed",
    "residual_edge_zero_signed",
    "kernel_weight_closed_signed",
    "K_boundary_cocycle_zero_signed",
    "PiM_projector_bound_signed",
    "M_H_ref_min_signed",
    "no_physical_charge_removed_signed",
    "no_measured_GM_absorption_signed",
)

DIRECT_FIELDS = (
    "C_corner_abs",
    "norm_dS_Feps_abs",
    "norm_bX_abs",
    "harmonic_edge_abs",
    "residual_edge_abs",
    "K_boundary_abs",
)

DIRECT_FACTORS = (
    "M_H_ref_min_abs",
    "PiM_norm_abs",
    "K_edge_abs",
    "qbar_XT_abs",
    "tau_BY5_edge_abs",
    "lambda_edge_abs",
)

COMPONENT_FIELDS = (
    "corner_outer_abs",
    "corner_inner_abs",
    "kernel_weight_derivative_abs",
    "bX_norm_abs",
    "harmonic_mode_abs",
    "residual_mode_abs",
    "counterterm_mismatch_abs",
    "cocycle_abs",
)

COMPONENT_FACTORS = (
    "M_H_ref_min_abs",
    "projector_norm_abs",
    "K_edge_abs",
    "qbar_XT_abs",
    "tau_BY5_edge_abs",
    "lambda_edge_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CLOSURE_ONLY_QUOTIENT",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "HARMONIC_SILENCE_BY_ASSUMPTION",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "REFERENCE_ONLY_ZERO",
    "STOKES_ZERO_WITH_OPEN_WEIGHT",
    "SYMBOLIC_BX_EXACTNESS",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed", "derived_zero"}


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


def zero_result(passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "Q_edge_bound_abs": zero,
        "Qbar_edge_XH_bound_abs": zero,
        "alpha_edge_abs": zero,
        "BY5_edge_feed_abs": zero,
        "K_boundary_abs": zero,
        "component_sum_abs": zero,
        "BX_cocycle_status": "BX_PRIMITIVE_COCYCLE_ZERO_CERTIFICATE_SIGNED" if passed else "BX_PRIMITIVE_COCYCLE_ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "BX_PRIMITIVE_COCYCLE_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_BX_PRIMITIVE_COCYCLE_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    return zero_result(not missing, missing)


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in DIRECT_FIELDS}
    factors = {
        "M_H_ref_min_abs": positive(row, "M_H_ref_min_abs", missing),
        "PiM_norm_abs": nonnegative(row, "PiM_norm_abs", missing),
        "K_edge_abs": nonnegative(row, "K_edge_abs", missing),
        "qbar_XT_abs": nonnegative(row, "qbar_XT_abs", missing),
        "tau_BY5_edge_abs": nonnegative(row, "tau_BY5_edge_abs", missing),
        "lambda_edge_abs": positive(row, "lambda_edge_abs", missing),
    }
    Q_edge = None
    Qbar = None
    alpha = None
    BY5 = None
    component_sum = None
    if not missing:
        component_sum = (
            values["C_corner_abs"]
            + values["norm_dS_Feps_abs"] * values["norm_bX_abs"]
            + values["harmonic_edge_abs"]
            + values["residual_edge_abs"]
            + values["K_boundary_abs"]
        )
        Q_edge = component_sum
        Qbar = factors["PiM_norm_abs"] * Q_edge / factors["M_H_ref_min_abs"]
        alpha = factors["K_edge_abs"] * Qbar * factors["qbar_XT_abs"]
        BY5 = factors["tau_BY5_edge_abs"] * Qbar
    passed = not missing
    return {
        "Q_edge_bound_abs": fmt(Q_edge),
        "Qbar_edge_XH_bound_abs": fmt(Qbar),
        "alpha_edge_abs": fmt(alpha),
        "BY5_edge_feed_abs": fmt(BY5),
        "K_boundary_abs": fmt(values.get("K_boundary_abs")),
        "component_sum_abs": fmt(component_sum),
        "BX_cocycle_status": "FINITE_DIRECT_EDGE_BOUND_READY" if passed else "FINITE_DIRECT_EDGE_BOUND_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_EDGE_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_EDGE_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_pack(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    values = {field: nonnegative(row, field, missing) for field in COMPONENT_FIELDS}
    factors = {
        "M_H_ref_min_abs": positive(row, "M_H_ref_min_abs", missing),
        "projector_norm_abs": nonnegative(row, "projector_norm_abs", missing),
        "K_edge_abs": nonnegative(row, "K_edge_abs", missing),
        "qbar_XT_abs": nonnegative(row, "qbar_XT_abs", missing),
        "tau_BY5_edge_abs": nonnegative(row, "tau_BY5_edge_abs", missing),
        "lambda_edge_abs": positive(row, "lambda_edge_abs", missing),
    }
    Q_edge = None
    Qbar = None
    alpha = None
    BY5 = None
    component_sum = None
    if not missing:
        component_sum = (
            values["corner_outer_abs"]
            + values["corner_inner_abs"]
            + values["kernel_weight_derivative_abs"] * values["bX_norm_abs"]
            + values["harmonic_mode_abs"]
            + values["residual_mode_abs"]
            + values["counterterm_mismatch_abs"]
            + values["cocycle_abs"]
        )
        Q_edge = component_sum
        Qbar = factors["projector_norm_abs"] * Q_edge / factors["M_H_ref_min_abs"]
        alpha = factors["K_edge_abs"] * Qbar * factors["qbar_XT_abs"]
        BY5 = factors["tau_BY5_edge_abs"] * Qbar
    passed = not missing
    return {
        "Q_edge_bound_abs": fmt(Q_edge),
        "Qbar_edge_XH_bound_abs": fmt(Qbar),
        "alpha_edge_abs": fmt(alpha),
        "BY5_edge_feed_abs": fmt(BY5),
        "K_boundary_abs": fmt(values.get("cocycle_abs")),
        "component_sum_abs": fmt(component_sum),
        "BX_cocycle_status": "FINITE_COMPONENT_EDGE_PACK_READY" if passed else "FINITE_COMPONENT_EDGE_PACK_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_EDGE_PACK_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_EDGE_PACK_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
        "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE",
        "alpha_edge_abs": "MISSING_NUMERIC_VALUE",
        "BY5_edge_feed_abs": "MISSING_NUMERIC_VALUE",
        "K_boundary_abs": "MISSING_NUMERIC_VALUE",
        "component_sum_abs": "MISSING_NUMERIC_VALUE",
        "BX_cocycle_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_BX_EDGE_ROW"
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
    if route_type == "BX_cocycle_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_edge_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "component_edge_pack":
        result = evaluate_component_pack(row)
    else:
        result = {
            "Q_edge_bound_abs": "MISSING_NUMERIC_VALUE",
            "Qbar_edge_XH_bound_abs": "MISSING_NUMERIC_VALUE",
            "alpha_edge_abs": "MISSING_NUMERIC_VALUE",
            "BY5_edge_feed_abs": "MISSING_NUMERIC_VALUE",
            "K_boundary_abs": "MISSING_NUMERIC_VALUE",
            "component_sum_abs": "MISSING_NUMERIC_VALUE",
            "BX_cocycle_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: BX_primitive_cocycle_edge_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
