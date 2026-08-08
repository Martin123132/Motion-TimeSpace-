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

SELECTOR_ZERO_FIELDS = (
    "parent_action_covariant_signed",
    "observed_tau_signed",
    "same_frame_source_measure_signed",
    "compact_worldtube_support_signed",
    "linking_surfaces_fixed_signed",
    "Htau_integrability_signed",
    "H_ref_fixed_signed",
    "M_H_ref_positive_signed",
    "PiM_Hamiltonian_map_signed",
    "boundary_reference_lock_signed",
    "coupling_descent_silence_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

SELECTOR_COMPONENT_FIELDS = (
    "B_zero_flux_abs",
    "Delta_symp_abs",
    "H_ref_shift_abs",
    "Delta_worldtube_domain_abs",
    "Delta_frame_source_abs",
    "coupling_residual_abs",
    "R_eq_integral_abs",
    "I_commutator_abs",
    "T_PiM_norm_abs",
    "A_parent_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_SHORTCUT",
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "LATE_EQUALITY_MULTIPLIER",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "REFERENCE_ROW_AS_ZERO",
    "SCHWARZSCHILD_AB_IMPORT",
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


def evaluate_selector_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in SELECTOR_ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    return {
        "M_H_ref_abs": "THEOREM_POSITIVE_DEFINED" if passed else "MISSING_NUMERIC_VALUE",
        "M_H_ref_calc_abs": "THEOREM_POSITIVE_DEFINED" if passed else "MISSING_NUMERIC_VALUE",
        "M_H_ref_mismatch_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "component_sum_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "epsilon_selector_Meff_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "BY5_selector_feed_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "selector_status": "SELECTOR_MHREF_ZERO_CERTIFICATE_SIGNED" if passed else "SELECTOR_MHREF_ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "PARENT_SELECTOR_MHREF_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_PARENT_SELECTOR_MHREF_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_direct_mhref(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    H_tau = nonnegative(row, "H_tau_outer_abs", missing)
    H_ref = nonnegative(row, "H_ref_abs", missing)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    tolerance = nonnegative(row, "reference_tolerance_abs", missing)
    M_calc: float | None = None
    mismatch: float | None = None
    if H_tau is not None and H_ref is not None:
        M_calc = H_tau - H_ref
        if M_calc <= 0.0:
            missing.append("NONPOSITIVE_H_tau_minus_H_ref")
            M_calc = None
    if M_calc is not None and M_H_ref is not None:
        mismatch = abs(M_calc - M_H_ref)
        if tolerance is not None and mismatch > tolerance:
            missing.append("REFERENCE_MHREF_MISMATCH")
    passed = not missing
    return {
        "M_H_ref_abs": fmt(M_H_ref),
        "M_H_ref_calc_abs": fmt(M_calc),
        "M_H_ref_mismatch_abs": fmt(mismatch),
        "component_sum_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "epsilon_selector_Meff_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "BY5_selector_feed_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "selector_status": "MHREF_DENOMINATOR_READY_NONCLAIM" if passed else "MHREF_DENOMINATOR_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_MHREF_ROW_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_MHREF_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_selector(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    tau = nonnegative(row, "tau_BY5_MHref_abs", missing)
    component_sum = 0.0
    for field in SELECTOR_COMPONENT_FIELDS:
        value = nonnegative(row, field, missing)
        if value is not None:
            component_sum += value
    epsilon = component_sum / M_H_ref if M_H_ref is not None and not missing else None
    BY5 = tau * epsilon if tau is not None and epsilon is not None else None
    passed = not missing
    return {
        "M_H_ref_abs": fmt(M_H_ref),
        "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "component_sum_abs": fmt(component_sum if passed else None),
        "epsilon_selector_Meff_abs": fmt(epsilon),
        "BY5_selector_feed_abs": fmt(BY5),
        "selector_status": "FINITE_SELECTOR_COMPONENTS_READY" if passed else "FINITE_SELECTOR_COMPONENTS_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_SELECTOR_ROW_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_SELECTOR_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "M_H_ref_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
        "M_H_ref_mismatch_abs": "MISSING_NUMERIC_VALUE",
        "component_sum_abs": "MISSING_NUMERIC_VALUE",
        "epsilon_selector_Meff_abs": "MISSING_NUMERIC_VALUE",
        "BY5_selector_feed_abs": "MISSING_NUMERIC_VALUE",
        "selector_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_MHREF_ROW"
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
    if route_type == "selector_zero":
        result = evaluate_selector_zero(row)
    elif route_type == "direct_MHref":
        result = evaluate_direct_mhref(row)
    elif route_type == "component_selector":
        result = evaluate_component_selector(row)
    else:
        result = {
            "M_H_ref_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_calc_abs": "MISSING_NUMERIC_VALUE",
            "M_H_ref_mismatch_abs": "MISSING_NUMERIC_VALUE",
            "component_sum_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_selector_Meff_abs": "MISSING_NUMERIC_VALUE",
            "BY5_selector_feed_abs": "MISSING_NUMERIC_VALUE",
            "selector_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: parent_worldtube_MHref_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
