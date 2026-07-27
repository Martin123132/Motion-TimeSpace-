from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


ZERO_FIELDS = (
    "fixed_parent_PiM_signed",
    "source_current_domain_signed",
    "covariant_constancy_signed",
    "Hilbert_topological_equality_signed",
    "boundary_zero_flux_signed",
    "projector_stress_silence_signed",
    "worldtube_glue_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

COMMON_FLAGS = (
    "source_signed",
    "units_signed",
    "same_branch_signed",
    "no_cancellation_guard",
)

FORBIDDEN_SOURCE_TOKENS = (
    "ALPHA_OBS_AS_DERIVATION",
    "BOUND_AS_SOURCE",
    "CALIBRATION_AS_DERIVATION",
    "CANCEL_UNKNOWN_COMPONENTS",
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


def epsilon_from_commutator(I_commutator: float | None, row: dict[str, Any], missing: list[str]) -> float | None:
    c_M = nonnegative(row, "c_M_abs", missing)
    M_eff_ref = nonnegative(row, "M_eff_ref_abs", missing)
    if I_commutator is None or c_M is None or M_eff_ref is None or M_eff_ref <= 0.0:
        if M_eff_ref == 0.0:
            missing.append("ZERO_M_eff_ref_abs")
        return None
    return c_M * I_commutator / M_eff_ref


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    passed = not missing
    status = "PIM_COMMUTATOR_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_PIM_COMMUTATOR_ZERO_CLAUSES"
    return {
        "I_commutator_bound_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "epsilon_radial_Meff_from_Icomm_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "BY5_commutator_feed_abs": "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE",
        "commutator_status": "ZERO_CERTIFICATE_SIGNED" if passed else "ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": status,
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_direct_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    I_commutator = nonnegative(row, "I_commutator_abs", missing)
    epsilon = epsilon_from_commutator(I_commutator, row, missing)
    passed = not missing
    return {
        "I_commutator_bound_abs": fmt(I_commutator),
        "epsilon_radial_Meff_from_Icomm_abs": fmt(epsilon),
        "BY5_commutator_feed_abs": "MISSING_NUMERIC_VALUE",
        "commutator_status": "FINITE_DIRECT_ICOMMUTATOR_READY" if passed else "FINITE_DIRECT_ICOMMUTATOR_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "PIM_COMMUTATOR_DIRECT_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_PIM_COMMUTATOR_DIRECT_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_operator_bound(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    dPiM = nonnegative(row, "dPiM_operator_norm_abs", missing)
    JH = nonnegative(row, "JH_annulus_norm_abs", missing)
    annulus = nonnegative(row, "annulus_measure_abs", missing)
    domain = optional_nonnegative(row, "domain_selector_variation_abs", missing)
    boundary = optional_nonnegative(row, "boundary_transition_abs", missing)
    I_commutator = None
    if dPiM is not None and JH is not None and annulus is not None:
        I_commutator = annulus * JH * (dPiM + domain) + boundary
    epsilon = epsilon_from_commutator(I_commutator, row, missing)
    passed = not missing
    return {
        "I_commutator_bound_abs": fmt(I_commutator),
        "epsilon_radial_Meff_from_Icomm_abs": fmt(epsilon),
        "BY5_commutator_feed_abs": "MISSING_NUMERIC_VALUE",
        "commutator_status": "FINITE_OPERATOR_ICOMMUTATOR_READY" if passed else "FINITE_OPERATOR_ICOMMUTATOR_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "PIM_COMMUTATOR_OPERATOR_BOUND_PASS_NONCLAIM" if passed else "BLOCKED_PIM_COMMUTATOR_OPERATOR_BOUND_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_BY5_feed(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    I_commutator = parse_float(row.get("I_commutator_abs"))
    if I_commutator is None:
        dPiM = nonnegative(row, "dPiM_operator_norm_abs", missing)
        JH = nonnegative(row, "JH_annulus_norm_abs", missing)
        annulus = nonnegative(row, "annulus_measure_abs", missing)
        domain = optional_nonnegative(row, "domain_selector_variation_abs", missing)
        boundary = optional_nonnegative(row, "boundary_transition_abs", missing)
        if dPiM is not None and JH is not None and annulus is not None:
            I_commutator = annulus * JH * (dPiM + domain) + boundary
    elif I_commutator < 0.0:
        missing.append("NEGATIVE_I_commutator_abs")
        I_commutator = None
    epsilon = epsilon_from_commutator(I_commutator, row, missing)
    tau = nonnegative(row, "tau_BY5_commutator_abs", missing)
    BY5 = None
    if epsilon is not None and tau is not None:
        BY5 = tau * epsilon
    passed = not missing
    return {
        "I_commutator_bound_abs": fmt(I_commutator),
        "epsilon_radial_Meff_from_Icomm_abs": fmt(epsilon),
        "BY5_commutator_feed_abs": fmt(BY5),
        "commutator_status": "FINITE_ICOMMUTATOR_FEEDS_BY5" if passed else "FINITE_ICOMMUTATOR_BY5_FEED_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "PIM_COMMUTATOR_BY5_FEED_PASS_NONCLAIM" if passed else "BLOCKED_PIM_COMMUTATOR_BY5_FEED_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_PIM_COMMUTATOR_ROW"
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
                "I_commutator_bound_abs": "MISSING_NUMERIC_VALUE",
                "epsilon_radial_Meff_from_Icomm_abs": "MISSING_NUMERIC_VALUE",
                "BY5_commutator_feed_abs": "MISSING_NUMERIC_VALUE",
                "commutator_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "route_pass": False,
                "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    if route_type == "commutator_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_bound":
        result = evaluate_direct_bound(row)
    elif route_type == "operator_bound":
        result = evaluate_operator_bound(row)
    elif route_type == "BY5_feed":
        result = evaluate_BY5_feed(row)
    else:
        result = {
            "I_commutator_bound_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_radial_Meff_from_Icomm_abs": "MISSING_NUMERIC_VALUE",
            "BY5_commutator_feed_abs": "MISSING_NUMERIC_VALUE",
            "commutator_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: PiM_commutator_obstruction_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    rows = [evaluate_row(row) for row in read_csv(input_path)]
    write_csv(output_path, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
