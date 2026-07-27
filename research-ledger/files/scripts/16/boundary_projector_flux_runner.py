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
    "compact_corner_free_domain_signed",
    "relative_cohomology_trivial_signed",
    "B_imp_exact_primitive_signed",
    "kernel_derivative_zero_signed",
    "no_vector_tensor_boundary_hair_signed",
    "boundary_reference_silent_signed",
    "projector_definition_signed",
    "edge_mass_independence_signed",
    "source_edge_symplectic_orthogonal_signed",
    "PiM_reference_silence_signed",
    "no_double_count_split_signed",
    "M_H_ref_positive_signed",
    "no_readout_mask_signed",
    "no_measured_GM_absorption_signed",
)

DIRECT_FIELDS = (
    "B_zero_flux_abs",
    "boundary_vector_flux_abs",
    "boundary_tensor_flux_abs",
    "kernel_derivative_flux_abs",
    "projector_boundary_flux_abs",
    "PiM_Q_edge_abs",
    "K_boundary_abs",
)

COMPONENT_FIELDS = (
    "B_zero_flux_abs",
    "boundary_vector_flux_abs",
    "boundary_tensor_flux_abs",
    "boundary_shear_flux_abs",
    "boundary_marker_flux_abs",
    "kernel_derivative_flux_abs",
    "boundary_counterterm_flux_abs",
    "projector_commutator_abs",
    "projector_variation_abs",
    "projector_boundary_flux_abs",
    "PiM_Q_edge_abs",
    "K_boundary_abs",
    "Delta_domain_boundary_abs",
)

FORBIDDEN_SOURCE_TOKENS = (
    "BARE_MASS_DENOMINATOR",
    "BOUND_AS_SOURCE",
    "CANCEL_UNKNOWN_COMPONENTS",
    "CLOSURE_ONLY_QUOTIENT",
    "DROP_PROJECTOR_STRESS",
    "FIT_TO_BOUND",
    "GR_IMPORT",
    "MEASURED_GM_AS_SOURCE",
    "MEASURED_G_ABSORPTION",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_MASK",
    "REFERENCE_ONLY_ZERO",
    "SYMBOLIC_EDGE_ZERO",
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


def optional_nonnegative(row: dict[str, Any], field: str, missing: list[str]) -> float:
    value = parse_float(row.get(field))
    if value is None:
        return 0.0
    if value < 0.0:
        missing.append(f"NEGATIVE_{field}")
        return 0.0
    return value


def normalize(value: float | None, denominator: float | None) -> float | None:
    if value is None or denominator is None or denominator <= 0.0:
        return None
    return value / denominator


def observable_map(epsilon: float | None, row: dict[str, Any], missing: list[str]) -> tuple[float | None, float | None, float | None, float | None, float | None]:
    if epsilon is None:
        return None, None, None, None, None
    C_beta = optional_nonnegative(row, "C_beta_flux_abs", missing)
    C_gamma = optional_nonnegative(row, "C_gamma_flux_abs", missing)
    C_alpha3 = optional_nonnegative(row, "C_alpha3_flux_abs", missing)
    C_xi = optional_nonnegative(row, "C_xi_flux_abs", missing)
    tau = optional_nonnegative(row, "tau_BY5_boundary_abs", missing)
    return C_beta * epsilon, C_gamma * epsilon, C_alpha3 * epsilon, C_xi * epsilon, tau * epsilon


def zero_result(passed: bool, missing: list[str]) -> dict[str, Any]:
    zero = "0.000000000000000e+00" if passed else "MISSING_NUMERIC_VALUE"
    return {
        "B_zero_flux_over_MH_abs": zero,
        "projector_boundary_flux_over_MH_abs": zero,
        "Q_edge_over_MH_abs": zero,
        "K_boundary_over_MH_abs": zero,
        "component_sum_abs": zero,
        "epsilon_boundary_projector_abs": zero,
        "beta_flux_equiv_abs": zero,
        "gamma_flux_equiv_abs": zero,
        "alpha3_flux_equiv_abs": zero,
        "xi_flux_equiv_abs": zero,
        "BY5_boundary_projector_feed_abs": zero,
        "boundary_projector_status": "BOUNDARY_PROJECTOR_ZERO_CERTIFICATE_SIGNED" if passed else "BOUNDARY_PROJECTOR_ZERO_CERTIFICATE_UNSIGNED",
        "route_pass": passed,
        "runner_status": "BOUNDARY_PROJECTOR_ZERO_PASS_NONCLAIM" if passed else "BLOCKED_BOUNDARY_PROJECTOR_ZERO_CLAUSES",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_zero(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    for field in ZERO_FIELDS:
        if not bool_text(row.get(field)):
            missing.append(f"MISSING_{field}")
    return zero_result(not missing, missing)


def evaluate_direct_flux(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    values = {field: nonnegative(row, field, missing) for field in DIRECT_FIELDS}
    component_sum = sum(value for value in values.values() if value is not None)
    epsilon = normalize(component_sum, M_H_ref) if not missing else None
    beta, gamma, alpha3, xi, BY5 = observable_map(epsilon, row, missing)
    passed = not missing
    return {
        "B_zero_flux_over_MH_abs": fmt(normalize(values["B_zero_flux_abs"], M_H_ref)),
        "projector_boundary_flux_over_MH_abs": fmt(normalize(values["projector_boundary_flux_abs"], M_H_ref)),
        "Q_edge_over_MH_abs": fmt(normalize(values["PiM_Q_edge_abs"], M_H_ref)),
        "K_boundary_over_MH_abs": fmt(normalize(values["K_boundary_abs"], M_H_ref)),
        "component_sum_abs": fmt(component_sum if passed else None),
        "epsilon_boundary_projector_abs": fmt(epsilon),
        "beta_flux_equiv_abs": fmt(beta),
        "gamma_flux_equiv_abs": fmt(gamma),
        "alpha3_flux_equiv_abs": fmt(alpha3),
        "xi_flux_equiv_abs": fmt(xi),
        "BY5_boundary_projector_feed_abs": fmt(BY5),
        "boundary_projector_status": "FINITE_DIRECT_BOUNDARY_PROJECTOR_FLUX_READY" if passed else "FINITE_DIRECT_BOUNDARY_PROJECTOR_FLUX_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "DIRECT_BOUNDARY_PROJECTOR_FLUX_PASS_NONCLAIM" if passed else "BLOCKED_DIRECT_BOUNDARY_PROJECTOR_FLUX_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def evaluate_component_flux(row: dict[str, Any]) -> dict[str, Any]:
    missing = base_missing(row)
    M_H_ref = positive(row, "M_H_ref_abs", missing)
    values = {field: nonnegative(row, field, missing) for field in COMPONENT_FIELDS}
    component_sum = sum(value for value in values.values() if value is not None)
    epsilon = normalize(component_sum, M_H_ref) if not missing else None
    beta, gamma, alpha3, xi, BY5 = observable_map(epsilon, row, missing)
    passed = not missing
    return {
        "B_zero_flux_over_MH_abs": fmt(normalize(values["B_zero_flux_abs"], M_H_ref)),
        "projector_boundary_flux_over_MH_abs": fmt(normalize(values["projector_boundary_flux_abs"], M_H_ref)),
        "Q_edge_over_MH_abs": fmt(normalize(values["PiM_Q_edge_abs"], M_H_ref)),
        "K_boundary_over_MH_abs": fmt(normalize(values["K_boundary_abs"], M_H_ref)),
        "component_sum_abs": fmt(component_sum if passed else None),
        "epsilon_boundary_projector_abs": fmt(epsilon),
        "beta_flux_equiv_abs": fmt(beta),
        "gamma_flux_equiv_abs": fmt(gamma),
        "alpha3_flux_equiv_abs": fmt(alpha3),
        "xi_flux_equiv_abs": fmt(xi),
        "BY5_boundary_projector_feed_abs": fmt(BY5),
        "boundary_projector_status": "FINITE_COMPONENT_BOUNDARY_PROJECTOR_FLUX_READY" if passed else "FINITE_COMPONENT_BOUNDARY_PROJECTOR_FLUX_MISSING_INPUTS",
        "route_pass": passed,
        "runner_status": "COMPONENT_BOUNDARY_PROJECTOR_FLUX_PASS_NONCLAIM" if passed else "BLOCKED_COMPONENT_BOUNDARY_PROJECTOR_FLUX_INPUTS",
        "missing_for_claim": "" if passed else ";".join(dict.fromkeys(missing)),
    }


def forbidden_result(row_id: str, route_type: str, route: Any) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "route_type": route_type,
        "route": route,
        "valid_for_claim": False,
        "claim_allowed": False,
        "B_zero_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "projector_boundary_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "Q_edge_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "K_boundary_over_MH_abs": "MISSING_NUMERIC_VALUE",
        "component_sum_abs": "MISSING_NUMERIC_VALUE",
        "epsilon_boundary_projector_abs": "MISSING_NUMERIC_VALUE",
        "beta_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
        "gamma_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
        "alpha3_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
        "xi_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
        "BY5_boundary_projector_feed_abs": "MISSING_NUMERIC_VALUE",
        "boundary_projector_status": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "route_pass": False,
        "runner_status": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
    }


def evaluate_row(row: dict[str, Any]) -> dict[str, Any]:
    row_id = str(row.get("row_id", "")).strip() or "UNNAMED_BOUNDARY_PROJECTOR_ROW"
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
    if route_type == "boundary_projector_zero":
        result = evaluate_zero(row)
    elif route_type == "direct_flux_coefficients":
        result = evaluate_direct_flux(row)
    elif route_type == "component_flux_pack":
        result = evaluate_component_flux(row)
    else:
        result = {
            "B_zero_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "projector_boundary_flux_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "Q_edge_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "K_boundary_over_MH_abs": "MISSING_NUMERIC_VALUE",
            "component_sum_abs": "MISSING_NUMERIC_VALUE",
            "epsilon_boundary_projector_abs": "MISSING_NUMERIC_VALUE",
            "beta_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
            "gamma_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
            "alpha3_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
            "xi_flux_equiv_abs": "MISSING_NUMERIC_VALUE",
            "BY5_boundary_projector_feed_abs": "MISSING_NUMERIC_VALUE",
            "boundary_projector_status": "UNKNOWN_ROUTE_TYPE",
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
        print("Usage: boundary_projector_flux_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    rows = [evaluate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
