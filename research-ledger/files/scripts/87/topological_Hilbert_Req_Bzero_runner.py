from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ZERO_FIELDS = (
    "worldtube_fixed_signed",
    "source_measure_owned_signed",
    "topological_representative_PD_signed",
    "same_deRham_class_signed",
    "Hilbert_to_PiM_charge_map_signed",
    "boundary_zero_flux_signed",
    "commutator_zero_signed",
    "projector_stress_silence_signed",
    "no_extra_exchange_signed",
    "calibration_PPN_stable_signed",
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
    "R_eq_integral_abs",
    "B_zero_flux_abs",
    "I_commutator_abs",
    "Delta_worldtube_domain_abs",
    "Delta_extra_vector_abs",
    "projector_stress_beta_equiv_abs",
    "A_parent_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_SHORTCUT",
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


def normalize(value: float | None, M_H_ref: float | None, missing: list[str]) -> float | None:
    if value is None or M_H_ref is None:
        return None
    if M_H_ref <= 0.0:
        missing.append("ZERO_M_H_ref_abs")
        return None
    return value / M_H_ref


def BY5_feed(epsilon: float | None, row: dict[str, Any], missing: list[str]) -> float | None:
    tau = parse_float(row.get("tau_BY5_Req_abs"))
    if tau is None:
        return None
    if tau < 0.0:
        missing.append("NEGATIVE_tau_BY5_Req_abs")
        return None
    if epsilon is None:
        return None
    return tau * epsilon


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    return {
        "R_eq_norm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "B_zero_norm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "epsilon_eq_Meff_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "BY5_equality_feed_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "equality_status": "ZERO_CERTIFICATE_SIGNED" if passed else "ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "REQ_BZERO_EQUALITY_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_REQ_BZERO_EQUALITY_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    R_eq = nonnegative(row, "R_eq_integral_abs", missing)
    B_zero = nonnegative(row, "B_zero_flux_abs", missing)
    M_H_ref = nonnegative(row, "M_H_ref_abs", missing)
    R_norm = normalize(R_eq, M_H_ref, missing)
    B_norm = normalize(B_zero, M_H_ref, missing)
    epsilon = None if R_norm is None or B_norm is None else R_norm + B_norm
    BY5 = BY5_feed(epsilon, row, missing)
    if BY5 is None and not missing:
        missing.append("MISSING_tau_BY5_Req_abs")
    passed = not missing
    return {
        "R_eq_norm_abs": fmt(R_norm),
        "B_zero_norm_abs": fmt(B_norm),
        "epsilon_eq_Meff_abs": fmt(epsilon),
        "BY5_equality_feed_abs": fmt(BY5),
        "equality_status": "FINITE_DIRECT_REQ_BZERO_READY" if passed else "FINITE_DIRECT_REQ_BZERO_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "REQ_BZERO_DIRECT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_REQ_BZERO_DIRECT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = nonnegative(row, "M_H_ref_abs", missing)
    total = 0.0
    for field in COMPONENT_FIELDS:
        value = nonnegative(row, field, missing)
        if value is not None:
            total += value
    R_eq = parse_float(row.get("R_eq_integral_abs"))
    B_zero = parse_float(row.get("B_zero_flux_abs"))
    if R_eq is not None and R_eq < 0.0:
        missing.append("NEGATIVE_R_eq_integral_abs")
    if B_zero is not None and B_zero < 0.0:
        missing.append("NEGATIVE_B_zero_flux_abs")
    R_norm = normalize(R_eq if R_eq is not None and R_eq >= 0.0 else None, M_H_ref, missing)
    B_norm = normalize(B_zero if B_zero is not None and B_zero >= 0.0 else None, M_H_ref, missing)
    epsilon = normalize(total if not missing else None, M_H_ref, missing)
    BY5 = BY5_feed(epsilon, row, missing)
    if BY5 is None and not missing:
        missing.append("MISSING_tau_BY5_Req_abs")
    passed = not missing
    return {
        "R_eq_norm_abs": fmt(R_norm),
        "B_zero_norm_abs": fmt(B_norm),
        "epsilon_eq_Meff_abs": fmt(epsilon),
        "BY5_equality_feed_abs": fmt(BY5),
        "equality_status": "FINITE_COMPONENT_REQ_BZERO_READY" if passed else "FINITE_COMPONENT_REQ_BZERO_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "REQ_BZERO_COMPONENT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_REQ_BZERO_COMPONENT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_REQ_BZERO_ROW"
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
                "R_eq_norm_abs": "MISSING_NUMERIC_VALUE",
                "B_zero_norm_abs": "MISSING_NUMERIC_VALUE",
                "epsilon_eq_Meff_abs": "MISSING_NUMERIC_VALUE",
                "BY5_equality_feed_abs": "MISSING_NUMERIC_VALUE",
                "equality_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "equality_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "component_bound":
        result = evaluate_component_bound(row)
    else:
        result = {
            "R_eq_norm_abs": "MISSING_NUMERIC_VALUE",
            "B_zero_norm_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_eq_Meff_abs": "MISSING_NUMERIC_VALUE",
            "BY5_equality_feed_abs": "MISSING_NUMERIC_VALUE",
            "equality_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: topological_Hilbert_Req_Bzero_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
