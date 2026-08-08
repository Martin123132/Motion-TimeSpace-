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

PRIVATE_ZERO_FLAGS = (
    "declared_full_action_signed",
    "one_matter_action_line_signed",
    "standard_visible_import_signed",
    "hilbert_variation_before_readout_signed",
    "single_public_metric_coframe_signed",
    "common_measure_signed",
    "no_species_source_prefactor_signed",
    "no_material_active_source_reentry_signed",
    "no_hidden_marker_source_signed",
    "no_readout_source_selector_signed",
    "no_second_source_metric_signed",
    "no_post_variation_rescale_signed",
    "common_mode_calibration_only_signed",
    "no_measured_GM_absorption_signed",
)

STRICT_ORIGIN_FLAGS = (
    "motion_time_space_primitive_origin_signed",
    "global_parent_action_exhaustion_signed",
    "global_hidden_visible_interface_signed",
    "global_boundary_nonhilbert_silence_signed",
)

ENVELOPE_FIELDS = (
    "E_action_vertical_abs",
    "E_constant_marker_abs",
    "E_matter_lift_abs",
    "E_Hodge_EM_abs",
    "E_Poynting_boundary_abs",
    "E_nonminimal_EM_abs",
    "E_distributional_shell_abs",
    "E_readout_state_abs",
    "E_nonHilbert_abs",
    "E_PiM_Htau_abs",
    "E_E00_abs",
    "E_PPN_abs",
    "P_Newton_qbar_abs",
    "Qbar_source_XH_bound_abs",
    "K_source_abs",
    "tau_BY5_remaining_abs",
)

FORBIDDEN_TOKENS = (
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "G_ABSORPTION",
    "GM_ABSORPTION",
    "PRIVATE_BRANCH_PUBLIC_PROMOTION",
    "REOPEN_PRIVATE_WA_WITHOUT_REACTIVATION",
    "SOURCE_PREF_ZERO_EQUALS_FULL_DENSITY_ZERO",
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
    source_path = str(row.get("source_path", "")).strip()
    return bool(source_path) and not missing_text(source_path) and Path(source_path).exists()


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


def nonnegative(row: dict[str, Any], field: str, missing: list[str]) -> float | None:
    value = parse_float(row.get(field))
    if value is None:
        missing.append(f"MISSING_{field}")
        return None
    if value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return None
    return value


def source_zero_numbers(zero: bool) -> dict[str, str]:
    value = "0.000000000000000e+00" if zero else "MISSING_NUMERIC_VALUE"
    return {
        "delta_w_species_abs": value,
        "kappaA_source_rel_abs": value,
        "E_source_prefactor_abs": value,
        "density_prefactor_feed_abs": value,
        "delta_MHref_prefactor_abs": value,
        "delta_Newton_source_prefactor_abs": value,
        "alpha_source_prefactor_abs": value,
        "BY5_source_prefactor_abs": value,
    }


def remaining_missing_numbers() -> dict[str, str]:
    return {
        "density_nonprefactor_abs": "RETAINED_SEPARATELY",
        "source_descent_nonprefactor_abs": "RETAINED_SEPARATELY",
        "Newton_nonprefactor_abs": "RETAINED_SEPARATELY",
        "qbar_remaining_abs": "RETAINED_SEPARATELY",
        "alpha_remaining_abs": "RETAINED_SEPARATELY",
        "BY5_remaining_abs": "RETAINED_SEPARATELY",
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "branch_scope": "FORBIDDEN",
        "valid_for_claim": False,
        "claim_allowed": False,
        **source_zero_numbers(False),
        **remaining_missing_numbers(),
        "source_prefactor_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_ROUTE_USED",
    }


def evaluate_private_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    required_flags(row, PRIVATE_ZERO_FLAGS, missing)
    passed = not missing
    return {
        **source_zero_numbers(passed),
        **remaining_missing_numbers(),
        "source_prefactor_status": "ZERO_ON_DECLARED_ACTION_BRANCH" if passed else "PRIVATE_SOURCE_ZERO_REACTIVATED_OR_UNSIGNED",
        "route_pass": passed,
        "runner_status": "SOURCE_UNIVERSALITY_ZERO_PASS_PRIVATE_NONCLAIM" if passed else "BLOCKED_PRIVATE_SOURCE_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_public_origin(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    required_flags(row, PRIVATE_ZERO_FLAGS + STRICT_ORIGIN_FLAGS, missing)
    passed = not missing
    return {
        **source_zero_numbers(passed),
        **remaining_missing_numbers(),
        "source_prefactor_status": "STRICT_PARENT_ORIGIN_CONDITIONALLY_READY" if passed else "STRICT_PARENT_ORIGIN_UNSIGNED",
        "route_pass": passed,
        "runner_status": "STRICT_SOURCE_UNIVERSALITY_SHAPE_PASS_NONCLAIM" if passed else "BLOCKED_STRICT_PRIMITIVE_ORIGIN",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_remaining_envelope(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    if not bool_text(row.get("source_prefactor_zero_signed")):
        missing.append("MISSING_source_prefactor_zero_signed")
    values = {field: nonnegative(row, field, missing) for field in ENVELOPE_FIELDS}
    density = None
    source_descent = None
    newton = None
    qbar = None
    alpha = None
    by5 = None
    if not missing:
        density = sum(values[field] for field in ENVELOPE_FIELDS[:8])
        source_descent = density + values["E_nonHilbert_abs"] + values["E_PiM_Htau_abs"]
        newton = source_descent + values["E_E00_abs"] + values["E_PPN_abs"]
        qbar = values["P_Newton_qbar_abs"] * newton
        alpha = values["K_source_abs"] * values["Qbar_source_XH_bound_abs"] * qbar
        by5 = values["tau_BY5_remaining_abs"] * qbar
    passed = not missing
    return {
        **source_zero_numbers(passed),
        "density_nonprefactor_abs": fmt(density),
        "source_descent_nonprefactor_abs": fmt(source_descent),
        "Newton_nonprefactor_abs": fmt(newton),
        "qbar_remaining_abs": fmt(qbar),
        "alpha_remaining_abs": fmt(alpha),
        "BY5_remaining_abs": fmt(by5),
        "source_prefactor_status": "ZERO_WITH_NONPREFACTOR_ENVELOPE_RETAINED" if passed else "NONPREFACTOR_ENVELOPE_INPUTS_MISSING",
        "route_pass": passed,
        "runner_status": "REMAINING_NEWTON_ENVELOPE_PASS_NONCLAIM" if passed else "BLOCKED_REMAINING_NEWTON_ENVELOPE",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_RECONCILIATION_ROW"
    route_type = str(row.get("route_type", "")).strip()
    route = row.get("route", "")
    branch_scope = row.get("branch_scope", "")
    if forbidden_used(row):
        return forbidden_result(row_id, route_type, route)
    if route_type == "private_source_zero":
        result = evaluate_private_zero(row)
    elif route_type == "strict_parent_origin":
        result = evaluate_public_origin(row)
    elif route_type == "remaining_newton_envelope":
        result = evaluate_remaining_envelope(row)
    else:
        result = {
            **source_zero_numbers(False),
            **remaining_missing_numbers(),
            "source_prefactor_status": "UNKNOWN_ROUTE_TYPE",
            "route_pass": False,
            "runner_status": "FAILED_UNKNOWN_ROUTE_TYPE",
            "missing_for_claim": "UNKNOWN_ROUTE_TYPE",
        }
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "branch_scope": branch_scope,
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
        raise SystemExit("usage: source_universality_reconciliation_runner.py INPUT.csv OUTPUT.csv")
    run(Path(sys.argv[1]), Path(sys.argv[2]))
