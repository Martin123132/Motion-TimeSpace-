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
        for field in ("H_tau_source", "H_ref_source", "M_lower_source", "component_source", "provenance")
    ).upper()
    return any(token in source_text for token in FORBIDDEN_SOURCE_TOKENS)


def residual_abs_sum(row: dict[str, Any]) -> float | None:
    residual_fields = (
        "H_tau_curl_abs_kg",
        "H_tau_flux_abs_kg",
        "H_tau_sector_abs_kg",
        "H_tau_surface_abs_kg",
        "H_ref_drift_abs_kg",
        "H_ref_selector_abs_kg",
    )
    total = 0.0
    for field in residual_fields:
        value = parse_float(row.get(field))
        if value is None:
            return None
        total += abs(value)
    return total


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    charge_id = str(row.get("charge_id", "")).strip() or "UNNAMED_PARENT_CHARGE_ROW"
    h_tau_bulk = parse_float(row.get("H_tau_bulk_kg"))
    h_tau_surface = parse_float(row.get("H_tau_surface_kg"))
    h_ref = parse_float(row.get("H_ref_kg"))
    m_lower = parse_float(row.get("M_lower_kg"))
    mass_comparator = parse_float(row.get("M_GM_cal_kg"))
    residual_radius = residual_abs_sum(row)
    counterfactual = row_is_counterfactual(row)
    circular_source = forbidden_source_used(row)

    output: dict[str, Any] = {
        "charge_id": charge_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if circular_source and not counterfactual:
        output.update(
            {
                "H_tau_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_low_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_high_kg": "MISSING_NUMERIC_VALUE",
                "H_charge_radius_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Hcharge_abs": "MISSING_NUMERIC_VALUE",
                "Delta_MH_center_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "FAILED_CIRCULAR_PARENT_CHARGE_SOURCE",
                "anti_circularity_status": "FAIL_ORBITAL_GM_USED_AS_CHARGE_SOURCE",
            }
        )
        return output

    if h_tau_bulk is None or h_tau_surface is None or h_ref is None:
        output.update(
            {
                "H_tau_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_low_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_high_kg": "MISSING_NUMERIC_VALUE",
                "H_charge_radius_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Hcharge_abs": "MISSING_NUMERIC_VALUE",
                "Delta_MH_center_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_PARENT_CHARGE_COMPONENTS",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    if residual_radius is None:
        output.update(
            {
                "H_tau_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_center_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_low_kg": "MISSING_NUMERIC_VALUE",
                "M_H_dress_high_kg": "MISSING_NUMERIC_VALUE",
                "H_charge_radius_abs_kg": "MISSING_NUMERIC_VALUE",
                "epsilon_Hcharge_abs": "MISSING_NUMERIC_VALUE",
                "Delta_MH_center_rel": "MISSING_NUMERIC_VALUE",
                "runner_status": "BLOCKED_MISSING_CHARGE_RESIDUAL_RADIUS",
                "anti_circularity_status": "PASS_NO_GM_BACKFILL",
            }
        )
        return output

    h_tau_center = h_tau_bulk + h_tau_surface
    m_center = h_tau_center - h_ref
    m_low = m_center - residual_radius
    m_high = m_center + residual_radius
    epsilon = residual_radius / m_lower if m_lower is not None and m_lower > 0 else None
    delta_rel = (m_center - mass_comparator) / mass_comparator if mass_comparator is not None and mass_comparator > 0 else None

    if m_lower is None or m_lower <= 0:
        runner_status = "BOUND_COMPUTED_BLOCKED_MISSING_POSITIVE_MLOWER"
    elif m_high <= 0:
        runner_status = "FAILED_NONPOSITIVE_PARENT_CHARGE_INTERVAL"
    elif counterfactual:
        runner_status = "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
    elif m_low <= 0:
        runner_status = "PARENT_CHARGE_INTERVAL_WIDE_OR_SIGN_UNRESOLVED_NONCLAIM"
    elif residual_radius == 0:
        runner_status = "PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM"
    else:
        runner_status = "PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM"

    output.update(
        {
            "H_tau_center_kg": format_float(h_tau_center),
            "M_H_dress_center_kg": format_float(m_center),
            "M_H_dress_low_kg": format_float(m_low),
            "M_H_dress_high_kg": format_float(m_high),
            "H_charge_radius_abs_kg": format_float(residual_radius),
            "epsilon_Hcharge_abs": format_float(epsilon),
            "Delta_MH_center_rel": format_float(delta_rel),
            "runner_status": runner_status,
            "anti_circularity_status": "PASS_PARENT_COMPONENTS_USED_NO_GM_BACKFILL",
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
        print("usage: parent_charge_Htau_Href_bound_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
