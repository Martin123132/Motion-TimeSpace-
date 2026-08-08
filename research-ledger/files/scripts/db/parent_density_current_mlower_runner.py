from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_SOURCE_TOKENS = ("ORBITAL_GM_DEFINITION", "GM_AS_SOURCE", "FITTED_ACCELERATION", "OBSERVED_GM_SOURCE")


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


def forbidden_source_used(row: dict[str, Any]) -> bool:
    source_text = " ".join(
        str(row.get(field, ""))
        for field in (
            "rho_H_source",
            "H_tau_surface_source",
            "H_ref_source",
            "M0_source",
            "component_source",
            "provenance",
        )
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


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


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    density_id = str(row.get("density_id", "")).strip() or "UNNAMED_DENSITY_CURRENT_ROW"
    rho_integral = parse_float(row.get("rho_H_integral_kg"))
    h_tau_surface = parse_float(row.get("H_tau_surface_center_kg"))
    h_ref = parse_float(row.get("H_ref_kg"))
    residual_radius = residual_abs_sum(row)
    m0 = parse_float(row.get("M0_kg"))
    epsilon_abs = parse_float(row.get("epsilon_abs"))
    mass_comparator = parse_float(row.get("M_GM_cal_kg"))
    counterfactual = row_is_counterfactual(row)
    circular_source = forbidden_source_used(row)

    output: dict[str, Any] = {
        "density_id": density_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if circular_source and not counterfactual:
        output.update(
            {
                "H_tau_bulk_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_kg": "MISSING_NUMERIC_VALUE",
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_density_current_abs": "MISSING_NUMERIC_VALUE",
                "Delta_density_vs_comparator_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE",
                "anti_circularity_status": "FAIL_ORBITAL_GM_USED_AS_DENSITY_SOURCE",
            }
        )
        return output

    if rho_integral is None or h_tau_surface is None or h_ref is None:
        output.update(
            {
                "H_tau_bulk_kg": "MISSING_NUMERIC_VALUE",
                "H_ref_kg": "MISSING_NUMERIC_VALUE",
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_density_current_abs": "MISSING_NUMERIC_VALUE",
                "Delta_density_vs_comparator_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    h_tau_bulk = rho_integral + h_tau_surface
    delta_rel = (h_tau_bulk - mass_comparator) / mass_comparator if mass_comparator is not None and mass_comparator > 0 else None

    if residual_radius is None:
        output.update(
            {
                "H_tau_bulk_kg": format_float(h_tau_bulk),
                "H_ref_kg": format_float(h_ref),
                "M_lower_kg": "MISSING_NUMERIC_VALUE",
                "Delta_H_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_density_current_abs": "MISSING_NUMERIC_VALUE",
                "Delta_density_vs_comparator_rel": format_float(delta_rel),
                "runner_status": "BLOCKED_MISSING_DENSITY_CURRENT_RESIDUALS",
                "anti_circularity_status": "PASS_PARENT_DENSITY_USED_NO_GM_BACKFILL",
            }
        )
        return output

    m_lower: float | None = None
    if m0 is not None and epsilon_abs is not None and m0 > 0 and 0 <= epsilon_abs < 1:
        m_lower = m0 * (1 - epsilon_abs)

    epsilon_density = residual_radius / m_lower if m_lower is not None and m_lower > 0 else None

    if m_lower is None:
        runner_status = "DENSITY_CURRENT_COMPUTED_BLOCKED_MLOWER"
    elif h_tau_bulk - h_ref + residual_radius <= 0:
        runner_status = "FAILED_NONPOSITIVE_DENSITY_CURRENT_INTERVAL"
    elif counterfactual:
        runner_status = "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif residual_radius == 0:
        runner_status = "DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM"
    else:
        runner_status = "DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM"

    output.update(
        {
            "H_tau_bulk_kg": format_float(h_tau_bulk),
            "H_ref_kg": format_float(h_ref),
            "M_lower_kg": format_float(m_lower),
            "Delta_H_abs_kg": format_float(residual_radius),
            "epsilon_density_current_abs": format_float(epsilon_density),
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
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(outputs[0].keys()))
        writer.writeheader()
        writer.writerows(outputs)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: parent_density_current_mlower_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
