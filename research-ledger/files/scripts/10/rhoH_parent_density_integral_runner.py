from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


C_LIGHT = 299_792_458.0

FORBIDDEN_SOURCE_TOKENS = (
    "ORBITAL_GM_DEFINITION",
    "GM_AS_SOURCE",
    "FITTED_ACCELERATION",
    "OBSERVED_GM_SOURCE",
    "POSTFIT_REFERENCE",
    "OBSERVED_RESIDUAL_CANCEL",
)


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def row_is_counterfactual(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("counterfactual") or "counterfactual" in text


def row_is_private(row: dict[str, Any]) -> bool:
    text = str(row.get("row_status", "")).strip().lower()
    return text.startswith("private") or "private" in text


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "rho_H_source",
            "T_total_nn_source",
            "H_tau_surface_source",
            "H_ref_source",
            "M0_source",
            "epsilon_source",
            "residual_source",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def all_density_clauses_signed(row: dict[str, Any]) -> bool:
    clause_fields = (
        "parent_action_signed",
        "variation_before_readout_signed",
        "same_frame_signed",
        "qbasic_density_signed",
        "compact_support_signed",
        "positive_energy_signed",
        "poynting_once_signed",
        "no_flux_or_flux_row_signed",
        "no_species_prefactor_signed",
        "no_postfit_signed",
    )
    return all(bool_text(row.get(field)) for field in clause_fields)


def residual_abs_sum(row: dict[str, Any]) -> float | None:
    residual_fields = (
        "R_eq_abs_kg",
        "B_zero_abs_kg",
        "boundary_flux_abs_kg",
        "open_EM_abs_kg",
        "nonEM_owner_gap_abs_kg",
        "projector_comm_abs_kg",
        "domain_shadow_abs_kg",
        "kappa_drift_abs_kg",
    )
    total = 0.0
    for field in residual_fields:
        value = parse_float(row.get(field))
        if value is None:
            return None
        total += abs(value)
    return total


def resolve_rho_integral(row: dict[str, Any]) -> tuple[float | None, str]:
    rho_integral = parse_float(row.get("rho_H_integral_kg"))
    if rho_integral is not None:
        return rho_integral, "RHO_H_INTEGRAL_INPUT"

    tnn_integral = parse_float(row.get("T_total_nn_integral_J"))
    c_value = parse_float(row.get("c_m_s")) or C_LIGHT
    if tnn_integral is not None and c_value > 0:
        return tnn_integral / (c_value * c_value), "T_TOTAL_NN_INTEGRAL_OVER_C2"

    return None, "MISSING_RHO_H_OR_TNN_INTEGRAL"


def resolve_surface(row: dict[str, Any]) -> tuple[float | None, str]:
    surface = parse_float(row.get("H_tau_surface_center_kg"))
    if surface is not None:
        return surface, "SURFACE_INPUT"
    if bool_text(row.get("surface_zero_signed")):
        return 0.0, "SURFACE_ZERO_SIGNED"
    return None, "MISSING_SURFACE_OR_ZERO_CERTIFICATE"


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    density_id = str(row.get("density_id", "")).strip() or "UNNAMED_RHOH_ROW"
    rho_integral, rho_mode = resolve_rho_integral(row)
    surface, surface_mode = resolve_surface(row)
    h_ref = parse_float(row.get("H_ref_kg"))
    residual_radius = residual_abs_sum(row)
    m0_input = parse_float(row.get("M0_kg"))
    epsilon_input = parse_float(row.get("epsilon_abs"))
    mass_comparator = parse_float(row.get("M_GM_cal_kg"))
    counterfactual = row_is_counterfactual(row)
    private = row_is_private(row)
    circular_source = forbidden_source_used(row)
    clauses_signed = all_density_clauses_signed(row)
    self_m0_signed = bool_text(row.get("M0_from_density_signed"))
    epsilon_from_residuals_signed = bool_text(row.get("epsilon_from_residual_radius_signed"))

    output: dict[str, Any] = {
        "density_id": density_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
        "density_clauses_signed": clauses_signed,
        "rho_integral_mode": rho_mode,
        "surface_mode": surface_mode,
    }

    if circular_source and not counterfactual:
        output.update(
            {
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                "H_tau_surface_center_kg": "MISSING_NUMERIC_VALUE",
                "H_tau_bulk_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_kg": "MISSING_NUMERIC_VALUE",
                "M0_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_abs": "MISSING_NUMERIC_VALUE",
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "Delta_density_vs_comparator_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_RHOH_OR_M0_SOURCE",
                "anti_circularity_status": "FAIL_ORBITAL_GM_OR_POSTFIT_USED_AS_DENSITY_SOURCE",
            }
        )
        return output

    if rho_integral is None:
        output.update(
            {
                "rho_H_integral_kg": "MISSING_NUMERIC_VALUE",
                "H_tau_surface_center_kg": format_float(surface),
                "H_tau_bulk_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_kg": format_float(h_ref),
                "M0_kg": format_float(m0_input),
                "epsilon_abs": format_float(epsilon_input),
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": format_float(residual_radius),
                "Delta_density_vs_comparator_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    if surface is None or h_ref is None:
        output.update(
            {
                "rho_H_integral_kg": format_float(rho_integral),
                "H_tau_surface_center_kg": format_float(surface),
                "H_tau_bulk_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_kg": format_float(h_ref),
                "M0_kg": format_float(m0_input),
                "epsilon_abs": format_float(epsilon_input),
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": format_float(residual_radius),
                "Delta_density_vs_comparator_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_SURFACE_OR_HREF",
                "anti_circularity_status": "PASS_PARENT_DENSITY_USED_NO_GM_BACKFILL",
            }
        )
        return output

    h_tau_bulk = rho_integral + surface
    m_center = h_tau_bulk - h_ref
    delta_rel = (h_tau_bulk - mass_comparator) / mass_comparator if mass_comparator is not None and mass_comparator > 0 else None

    if residual_radius is None:
        output.update(
            {
                "rho_H_integral_kg": format_float(rho_integral),
                "H_tau_surface_center_kg": format_float(surface),
                "H_tau_bulk_kg": format_float(h_tau_bulk),
                "H_ref_kg": format_float(h_ref),
                "M0_kg": format_float(m0_input),
                "epsilon_abs": format_float(epsilon_input),
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "Delta_density_vs_comparator_rel": format_float(delta_rel),
                "runner_status": "BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS",
                "anti_circularity_status": "PASS_PARENT_DENSITY_USED_NO_GM_BACKFILL",
            }
        )
        return output

    m0_source_mode = "M0_INPUT"
    m0 = m0_input
    if m0 is None and self_m0_signed and bool_text(row.get("positive_energy_signed")) and m_center > 0:
        m0 = m_center
        m0_source_mode = "SELF_FROM_POSITIVE_HILBERT_DENSITY"
    elif m0 is None:
        m0_source_mode = "MISSING_M0_SOURCE_OR_SELF_DENOMINATOR"

    epsilon_source_mode = "EPSILON_INPUT"
    epsilon_abs = epsilon_input
    if epsilon_abs is None and epsilon_from_residuals_signed and m0 is not None and m0 > 0:
        epsilon_abs = residual_radius / m0
        epsilon_source_mode = "RESIDUAL_RADIUS_OVER_M0"
    elif epsilon_abs is None:
        epsilon_source_mode = "MISSING_EPSILON_SOURCE_OR_RESIDUAL_RADIUS_RULE"

    m_lower: float | None = None
    if m0 is not None and epsilon_abs is not None and m0 > 0 and 0 <= epsilon_abs < 1:
        m_lower = m0 * (1.0 - epsilon_abs)

    if m0 is None:
        runner_status = "RHOH_COMPUTED_BLOCKED_M0_SOURCE_OR_SELF_DENOMINATOR"
    elif epsilon_abs is None:
        runner_status = "RHOH_COMPUTED_BLOCKED_EPSILON"
    elif m_lower is None or m_lower <= 0:
        runner_status = "FAILED_NONPOSITIVE_RHOH_MLOWER"
    elif counterfactual:
        runner_status = "RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif private and residual_radius == 0 and clauses_signed:
        runner_status = "RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM"
    elif residual_radius == 0 and clauses_signed:
        runner_status = "RHOH_PARENT_INTEGRAL_EXACT_COMPUTED_NONCLAIM"
    elif clauses_signed:
        runner_status = "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM"
    else:
        runner_status = "RHOH_NUMERIC_COMPUTED_PARENT_UNSIGNED_NONCLAIM"

    output.update(
        {
            "rho_H_integral_kg": format_float(rho_integral),
            "H_tau_surface_center_kg": format_float(surface),
            "H_tau_bulk_kg": format_float(h_tau_bulk),
            "H_ref_kg": format_float(h_ref),
            "M0_kg": format_float(m0),
            "M0_source_mode": m0_source_mode,
            "epsilon_abs": format_float(epsilon_abs),
            "epsilon_source_mode": epsilon_source_mode,
            "M_lower_kg": format_float(m_lower),
            "Delta_H_abs_kg": format_float(residual_radius),
            "Delta_density_vs_comparator_rel": format_float(delta_rel),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_PARENT_DENSITY_USED_NO_GM_BACKFILL",
        }
    )
    return output


def run(input_csv: Path, output_csv: Path) -> None:
    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"input CSV has no rows: {input_csv}")

    outputs = [compute_row(row) for row in rows]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for output in outputs:
        for key in output:
            if key not in fieldnames:
                fieldnames.append(key)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: rhoH_parent_density_integral_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
