from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ZERO_FIELDS = (
    "parent_variation_includes_PiM_signed",
    "PiM_parent_owned_signed",
    "metric_independent_topological_signed",
    "domain_homology_fixed_signed",
    "boundary_wall_silent_signed",
    "denominator_reference_silent_signed",
    "Bianchi_total_stress_owned_signed",
    "Hilbert_current_compatibility_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

COMMON_FLAGS = (
    "source_signed",
    "units_signed",
    "same_branch_signed",
    "no_cancellation_guard",
)

COMPONENT_FIELDS = (
    "metric_projector_stress_abs",
    "domain_motion_stress_abs",
    "hodge_green_stress_abs",
    "boundary_wall_stress_abs",
    "denominator_reference_stress_abs",
    "source_readout_stress_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "DROP_PROJECTOR_STRESS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ROW_AS_ZERO",
    "STANDARD_BRANCH_AS_GLOBAL",
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
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


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


def optional_nonnegative(row: dict[str, Any], field: str, missing: list[str]) -> float:
    value = parse_float(row.get(field))
    if value is None:
        return 0.0
    if value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return 0.0
    return value


def ppn_map(T_PiM: float | None, row: dict[str, Any], missing: list[str]) -> tuple[float | None, float | None, float | None, float | None]:
    if T_PiM is None:
        return None, None, None, None
    C_beta = optional_nonnegative(row, "C_beta_TPiM_abs", missing)
    C_gamma = optional_nonnegative(row, "C_gamma_TPiM_abs", missing)
    C_alpha3 = optional_nonnegative(row, "C_alpha3_TPiM_abs", missing)
    C_xi = optional_nonnegative(row, "C_xi_TPiM_abs", missing)
    return C_beta * T_PiM, C_gamma * T_PiM, C_alpha3 * T_PiM, C_xi * T_PiM


def source_feed(T_PiM: float | None, row: dict[str, Any], missing: list[str]) -> float | None:
    tau = parse_float(row.get("tau_BY5_TPiM_abs"))
    if tau is None:
        return None
    if tau < 0.0:
        missing.append("NEGATIVE_tau_BY5_TPiM_abs")
        return None
    if T_PiM is None:
        return None
    return tau * T_PiM


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    return {
        "T_PiM_norm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "projector_stress_beta_equiv_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "projector_stress_gamma_equiv_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "projector_stress_alpha3_equiv_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "projector_stress_xi_equiv_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "BY5_projector_stress_feed_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "stress_status": "ZERO_CERTIFICATE_SIGNED" if passed else "ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "PROJECTOR_STRESS_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_PROJECTOR_STRESS_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    T_PiM = nonnegative(row, "T_PiM_norm_abs", missing)
    beta, gamma, alpha3, xi = ppn_map(T_PiM, row, missing)
    BY5 = source_feed(T_PiM, row, missing)
    if BY5 is None and not missing:
        missing.append("MISSING_tau_BY5_TPiM_abs")
    passed = not missing
    return {
        "T_PiM_norm_abs": fmt(T_PiM),
        "projector_stress_beta_equiv_abs": fmt(beta),
        "projector_stress_gamma_equiv_abs": fmt(gamma),
        "projector_stress_alpha3_equiv_abs": fmt(alpha3),
        "projector_stress_xi_equiv_abs": fmt(xi),
        "BY5_projector_stress_feed_abs": fmt(BY5),
        "stress_status": "FINITE_DIRECT_TPIM_READY" if passed else "FINITE_DIRECT_TPIM_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "PROJECTOR_STRESS_DIRECT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_PROJECTOR_STRESS_DIRECT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    total = 0.0
    for field in COMPONENT_FIELDS:
        value = nonnegative(row, field, missing)
        if value is not None:
            total += value
    T_PiM = None if missing else total
    beta, gamma, alpha3, xi = ppn_map(T_PiM, row, missing)
    BY5 = source_feed(T_PiM, row, missing)
    if BY5 is None and not missing:
        missing.append("MISSING_tau_BY5_TPiM_abs")
    passed = not missing
    return {
        "T_PiM_norm_abs": fmt(T_PiM),
        "projector_stress_beta_equiv_abs": fmt(beta),
        "projector_stress_gamma_equiv_abs": fmt(gamma),
        "projector_stress_alpha3_equiv_abs": fmt(alpha3),
        "projector_stress_xi_equiv_abs": fmt(xi),
        "BY5_projector_stress_feed_abs": fmt(BY5),
        "stress_status": "FINITE_COMPONENT_TPIM_READY" if passed else "FINITE_COMPONENT_TPIM_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "PROJECTOR_STRESS_COMPONENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_PROJECTOR_STRESS_COMPONENT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_TPIM_ROW"
    route_type = str(row.get("route_type", "")).strip()
    output: dict[str, Any] = {
        "row_id": row_id,
        "route_type": route_type,
        "route": row.get("route", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "T_PiM_norm_abs": "MISSING_NUMERIC_VALUE",
                "projector_stress_beta_equiv_abs": "MISSING_NUMERIC_VALUE",
                "projector_stress_gamma_equiv_abs": "MISSING_NUMERIC_VALUE",
                "projector_stress_alpha3_equiv_abs": "MISSING_NUMERIC_VALUE",
                "projector_stress_xi_equiv_abs": "MISSING_NUMERIC_VALUE",
                "BY5_projector_stress_feed_abs": "MISSING_NUMERIC_VALUE",
                "stress_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "stress_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "component_bound":
        result = evaluate_component_bound(row)
    else:
        result = {
            "T_PiM_norm_abs": "MISSING_NUMERIC_VALUE",
            "projector_stress_beta_equiv_abs": "MISSING_NUMERIC_VALUE",
            "projector_stress_gamma_equiv_abs": "MISSING_NUMERIC_VALUE",
            "projector_stress_alpha3_equiv_abs": "MISSING_NUMERIC_VALUE",
            "projector_stress_xi_equiv_abs": "MISSING_NUMERIC_VALUE",
            "BY5_projector_stress_feed_abs": "MISSING_NUMERIC_VALUE",
            "stress_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: projector_stress_TPiM_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
