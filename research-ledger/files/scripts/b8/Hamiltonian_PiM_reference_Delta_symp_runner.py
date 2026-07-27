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
    "parent_L_theta_Q_signed",
    "covariant_phase_space_identity_signed",
    "Hamiltonian_PiM_map_signed",
    "integrability_curl_zero_signed",
    "reference_superselection_signed",
    "H_ref_derivative_silent_signed",
    "boundary_class_exact_signed",
    "symplectic_boundary_flux_zero_signed",
    "projector_silence_signed",
    "tau_lock_signed",
    "M_H_ref_positive_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

DIRECT_FIELDS = (
    "Delta_symp_abs",
    "H_ref_shift_abs",
    "B_zero_flux_abs",
    "symplectic_boundary_flux_abs",
)

COMPONENT_FIELDS = (
    "delta_H_tau_nonintegrable_abs",
    "reference_curl_abs",
    "H_ref_shift_abs",
    "B_zero_flux_abs",
    "Delta_symp_abs",
    "symplectic_boundary_flux_abs",
    "projector_boundary_flux_abs",
    "tau_mismatch_abs",
    "Delta_PiM_abs",
    "Delta_nonEH_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BARE_MASS_SHORTCUT",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "EH_IMPORT_AS_MTS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "REFERENCE_ROW_AS_ZERO",
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


def normalize(value: float | None, denominator: float | None) -> float | None:
    if value is None or denominator is None or denominator <= 0.0:
        return None
    return value / denominator


def tau_feed(epsilon: float | None, row: dict[str, Any], missing: list[str]) -> float | None:
    tau = nonnegative(row, "tau_BY5_ref_abs", missing)
    if epsilon is None or tau is None:
        return None
    return tau * epsilon


def zero_result(passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "Delta_symp_over_MH_abs": zero,
        "Delta_ref_over_MH_abs": zero,
        "B_zero_flux_over_MH_abs": zero,
        "symplectic_boundary_flux_over_MH_abs": zero,
        "component_sum_abs": zero,
        "epsilon_ref_boundary_abs": zero,
        "epsilon_HPiM_integrability_abs": zero,
        "BY5_reference_lock_feed_abs": zero,
        "reference_status": "REFERENCE_LOCK_ZERO_CERTIFICATE_SIGNED" if passed else "REFERENCE_LOCK_ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "REFERENCE_LOCK_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_REFERENCE_LOCK_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    return zero_result(not missing, missing)


def evaluate_direct_delta_symp(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    values = {field: nonnegative(row, field, missing) for field in DIRECT_FIELDS}
    component_sum = sum(value for value in values.values() if value is not None)
    Delta_symp_norm = normalize(values["Delta_symp_abs"], M_H_ref)
    Delta_ref_norm = normalize(values["H_ref_shift_abs"], M_H_ref)
    B_zero_norm = normalize(values["B_zero_flux_abs"], M_H_ref)
    symp_norm = normalize(values["symplectic_boundary_flux_abs"], M_H_ref)
    epsilon = normalize(component_sum, M_H_ref) if not missing else None
    BY5 = tau_feed(epsilon, row, missing)
    passed = not missing
    return {
        "Delta_symp_over_MH_abs": fmt(Delta_symp_norm),
        "Delta_ref_over_MH_abs": fmt(Delta_ref_norm),
        "B_zero_flux_over_MH_abs": fmt(B_zero_norm),
        "symplectic_boundary_flux_over_MH_abs": fmt(symp_norm),
        "component_sum_abs": fmt(component_sum if passed else None),
        "epsilon_ref_boundary_abs": fmt(epsilon),
        "epsilon_HPiM_integrability_abs": fmt(epsilon),
        "BY5_reference_lock_feed_abs": fmt(BY5),
        "reference_status": "FINITE_DIRECT_DELTA_SYMP_READY" if passed else "FINITE_DIRECT_DELTA_SYMP_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_DELTA_SYMP_ROW_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_DELTA_SYMP_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_fb5540(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    values = {field: nonnegative(row, field, missing) for field in COMPONENT_FIELDS}
    component_sum = sum(value for value in values.values() if value is not None)
    Delta_symp_norm = normalize(values["Delta_symp_abs"], M_H_ref)
    Delta_ref_norm = normalize(values["H_ref_shift_abs"], M_H_ref)
    B_zero_norm = normalize(values["B_zero_flux_abs"], M_H_ref)
    symp_norm = normalize(values["symplectic_boundary_flux_abs"], M_H_ref)
    epsilon = normalize(component_sum, M_H_ref) if not missing else None
    ref_boundary_total = sum(
        value
        for field, value in values.items()
        if field in {"H_ref_shift_abs", "B_zero_flux_abs", "Delta_symp_abs", "symplectic_boundary_flux_abs"} and value is not None
    )
    epsilon_ref = normalize(ref_boundary_total, M_H_ref) if not missing else None
    BY5 = tau_feed(epsilon, row, missing)
    passed = not missing
    return {
        "Delta_symp_over_MH_abs": fmt(Delta_symp_norm),
        "Delta_ref_over_MH_abs": fmt(Delta_ref_norm),
        "B_zero_flux_over_MH_abs": fmt(B_zero_norm),
        "symplectic_boundary_flux_over_MH_abs": fmt(symp_norm),
        "component_sum_abs": fmt(component_sum if passed else None),
        "epsilon_ref_boundary_abs": fmt(epsilon_ref),
        "epsilon_HPiM_integrability_abs": fmt(epsilon),
        "BY5_reference_lock_feed_abs": fmt(BY5),
        "reference_status": "FINITE_COMPONENT_FB5540_READY" if passed else "FINITE_COMPONENT_FB5540_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_FB5540_ROW_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_FB5540_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "Delta_symp_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "Delta_ref_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "B_zero_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "symplectic_boundary_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "component_sum_abs": "MISSING_NUMERIC_VALUE",
        "epsilon_ref_boundary_abs": "MISSING_NUMERIC_VALUE",
        "epsilon_HPiM_integrability_abs": "MISSING_NUMERIC_VALUE",
        "BY5_reference_lock_feed_abs": "MISSING_NUMERIC_VALUE",
        "reference_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_REFERENCE_LOCK_ROW"
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
    if route_type == "reference_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_Delta_symp":
        result = evaluate_direct_delta_symp(row)
    elif route_type == "component_FB5540":
        result = evaluate_component_fb5540(row)
    else:
        result = {
            "Delta_symp_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "Delta_ref_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "B_zero_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "symplectic_boundary_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "component_sum_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_ref_boundary_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_HPiM_integrability_abs": "MISSING_NUMERIC_VALUE",
            "BY5_reference_lock_feed_abs": "MISSING_NUMERIC_VALUE",
            "reference_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: Hamiltonian_PiM_reference_Delta_symp_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
