from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


C_LIGHT = 299_792_458.0


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING") or text.upper() in {"NA", "N/A", "NONE"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def format_float(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def compute_e00_integral_bound(row: dict[str, Any]) -> tuple[float | None, str]:
    integral_bound = parse_float(row.get("E00_integral_abs_m"))
    if integral_bound is not None:
        return abs(integral_bound), "E00_INTEGRAL_INPUT"

    e00_sup = parse_float(row.get("E00_sup_abs_m_minus2"))
    support_radius = parse_float(row.get("support_radius_m"))
    if e00_sup is None or support_radius is None:
        return None, "MISSING_E00_INTEGRAL_OR_SUP_RADIUS"
    if e00_sup < 0 or support_radius <= 0:
        return None, "INVALID_E00_SUP_OR_RADIUS"

    volume = (4.0 * math.pi / 3.0) * support_radius**3
    return e00_sup * volume, "E00_SUP_SPHERE_BOUND"


def compute_row(row: dict[str, Any]) -> dict[str, Any]:
    arena_id = str(row.get("arena_id", "")).strip() or "UNNAMED_ARENA"
    gravitational_parameter = parse_float(row.get("mu_ref_m3_s2"))
    calibrated_gravitational_constant = parse_float(row.get("G_cal_m3_kg_s2"))
    hamiltonian_mass = parse_float(row.get("M_H_dress_kg"))
    tolerance_eta = parse_float(row.get("tolerance_eta"))
    support_radius = parse_float(row.get("support_radius_m"))

    output: dict[str, Any] = {
        "arena_id": arena_id,
        "row_status_input": row.get("row_status", ""),
        "input_valid_for_claim": bool_text(row.get("valid_for_claim")),
        "valid_for_claim": False,
        "claim_allowed": False,
    }

    if gravitational_parameter is None or gravitational_parameter <= 0:
        output.update(
            {
                "M_GM_cal_kg": "MISSING_POSITIVE_MU_REF",
                "Delta_MH_rel": "NOT_COMPUTED",
                "eta_E00_abs": "NOT_COMPUTED",
                "eta_total_abs": "NOT_COMPUTED",
                "E00_sup_required_m_minus2": "NOT_COMPUTED",
                "runner_status": "FAILED_MISSING_POSITIVE_MU_REF",
            }
        )
        return output

    if calibrated_gravitational_constant is None or calibrated_gravitational_constant <= 0:
        output.update(
            {
                "M_GM_cal_kg": "MISSING_POSITIVE_G_CAL",
                "Delta_MH_rel": "NOT_COMPUTED",
                "eta_E00_abs": "NOT_COMPUTED",
                "eta_total_abs": "NOT_COMPUTED",
                "E00_sup_required_m_minus2": "NOT_COMPUTED",
                "runner_status": "FAILED_MISSING_POSITIVE_G_CAL",
            }
        )
        return output

    mass_comparator = gravitational_parameter / calibrated_gravitational_constant
    delta_mass_relative: float | None = None
    if hamiltonian_mass is not None:
        delta_mass_relative = abs((hamiltonian_mass - mass_comparator) / mass_comparator)

    e00_integral_bound, e00_source = compute_e00_integral_bound(row)
    eta_e00: float | None = None
    if e00_integral_bound is not None:
        eta_e00 = C_LIGHT**2 * e00_integral_bound / (8.0 * math.pi * gravitational_parameter)

    boundary_shift = abs(parse_float(row.get("delta_mu_boundary_abs_m3_s2")) or 0.0)
    profile_shift = abs(parse_float(row.get("delta_mu_profile_abs_m3_s2")) or 0.0)
    readout_shift = abs(parse_float(row.get("delta_mu_readout_abs_m3_s2")) or 0.0)
    eta_other = (boundary_shift + profile_shift + readout_shift) / gravitational_parameter

    e00_sup_required: float | None = None
    if tolerance_eta is not None and tolerance_eta >= 0 and support_radius is not None and support_radius > 0:
        e00_sup_required = 6.0 * gravitational_parameter * tolerance_eta / (C_LIGHT**2 * support_radius**3)

    eta_total: float | None = None
    if delta_mass_relative is not None and eta_e00 is not None:
        eta_total = delta_mass_relative + eta_e00 + eta_other

    if delta_mass_relative is None and eta_e00 is None:
        runner_status = "BLOCKED_MISSING_MHDRESS_AND_E00_BOUND"
    elif delta_mass_relative is None:
        runner_status = "BLOCKED_MISSING_MHDRESS"
    elif eta_e00 is None:
        runner_status = "BLOCKED_MISSING_E00_BOUND"
    elif eta_total is not None and tolerance_eta is not None and eta_total <= tolerance_eta:
        runner_status = "RUNNER_NUMERIC_PASS_NONCLAIM"
    else:
        runner_status = "RUNNER_NUMERIC_FAIL_OR_TOLERANCE_MISSING_NONCLAIM"

    if str(row.get("row_status", "")).strip().lower().startswith("counterfactual") and runner_status == "RUNNER_NUMERIC_PASS_NONCLAIM":
        runner_status = "RUNNER_SMOKE_PASS_NONCLAIM"

    output.update(
        {
            "M_GM_cal_kg": format_float(mass_comparator),
            "Delta_MH_rel": format_float(delta_mass_relative),
            "E00_integral_abs_m": format_float(e00_integral_bound),
            "E00_integral_source": e00_source,
            "eta_E00_abs": format_float(eta_e00),
            "eta_boundary_profile_readout_abs": format_float(eta_other),
            "eta_total_abs": format_float(eta_total),
            "tolerance_eta": format_float(tolerance_eta),
            "E00_sup_required_m_minus2": format_float(e00_sup_required),
            "runner_status": runner_status,
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
        print("usage: MHdress_E00_open_arena_runner.py INPUT.csv OUTPUT.csv", file=sys.stderr)
        return 2
    run(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
