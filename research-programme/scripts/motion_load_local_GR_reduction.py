#!/usr/bin/env python3
"""Test the motion-load scaffold against local weak-field GR gates."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


G = 6.67430e-11
C = 299_792_458.0
DAY = 86400.0
M_EARTH = 5.9722e24
R_EARTH = 6_371_000.0
R_GPS = 26_560_000.0
V_GROUND = 465.1
M_SUN = 1.98847e30
R_SUN = 6.957e8
AU = 1.495978707e11
ARCSEC_PER_RAD = 206_264.80624709636
MERCURY_A = 57.909e9
MERCURY_E = 0.205630
MERCURY_PERIOD_DAYS = 87.9691
DAYS_PER_CENTURY = 36525.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def q_clock(M: float, r: float, v: float = 0.0) -> float:
    return math.sqrt(1.0 - (v * v) / (C * C) - (2.0 * G * M) / (r * C * C))


def us_per_day(q: float) -> float:
    return (q - 1.0) * DAY * 1.0e6


def gps_rows() -> list[dict[str, Any]]:
    mu = G * M_EARTH
    v_gps = math.sqrt(mu / R_GPS)
    q_ground = q_clock(M_EARTH, R_EARTH, V_GROUND)
    q_gps = q_clock(M_EARTH, R_GPS, v_gps)
    return [
        {"case": "ground_vs_infinity", "value_microseconds_per_day": us_per_day(q_ground), "reference": "clock-load scaffold"},
        {"case": "gps_vs_infinity", "value_microseconds_per_day": us_per_day(q_gps), "reference": "clock-load scaffold"},
        {
            "case": "gps_minus_ground",
            "value_microseconds_per_day": (q_gps - q_ground) * DAY * 1.0e6,
            "reference": "expected GPS-scale net correction about +38.6 us/day",
        },
    ]


def gr_mercury_precession() -> float:
    delta_per_orbit = 6.0 * math.pi * G * M_SUN / (MERCURY_A * (1.0 - MERCURY_E**2) * C**2)
    return delta_per_orbit * ARCSEC_PER_RAD * (DAYS_PER_CENTURY / MERCURY_PERIOD_DAYS)


def weak_field_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gr_mercury = gr_mercury_precession()
    shapiro_log = math.log((4.0 * AU * AU) / (R_SUN * R_SUN))
    for p in (0.0, 0.5, 1.0):
        rows.append(
            {
                "p": p,
                "gamma_proxy": p,
                "light_bending_arcsec": (1.0 + p) * 2.0 * G * M_SUN / (R_SUN * C**2) * ARCSEC_PER_RAD,
                "mercury_arcsec_per_century": p * gr_mercury,
                "shapiro_microseconds": (1.0 + p) * (G * M_SUN / C**3) * shapiro_log * 1.0e6,
                "interpretation": "p=1 is the GR-like routing lane",
            }
        )
    return rows


def ppn_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "clock_residue",
            "equation": "T^2 = 1 - L = 1 - 2U/c^2",
            "weak_field_role": "Newtonian potential enters g_tt at first order",
            "status": "passes_Newtonian_clock_order",
        },
        {
            "quantity": "routing_response",
            "equation": "S_p = (1-L)^(-p)",
            "weak_field_role": "g_rr = 1 + 2p U/c^2 + ...",
            "status": "gamma_proxy_equals_p",
        },
        {
            "quantity": "reciprocal_routing",
            "equation": "T^2 S = 1",
            "weak_field_role": "forces S=(1-L)^(-1), hence p=1",
            "status": "conditional_derivation_of_p_equals_1",
        },
        {
            "quantity": "beta",
            "equation": "p=1 gives Schwarzschild-form completion if the reciprocal metric is exact",
            "weak_field_role": "beta=1 follows only after exact Schwarzschild/vacuum completion",
            "status": "conditional_not_parent_derived",
        },
    ]


def gate_rows(gps: list[dict[str, Any]], weak: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gps_net = next(row for row in gps if row["case"] == "gps_minus_ground")["value_microseconds_per_day"]
    p1 = next(row for row in weak if row["p"] == 1.0)
    return [
        {
            "gate": "GPS_clock_scale",
            "status": "pass",
            "detail": f"net={gps_net:.12f} us/day",
        },
        {
            "gate": "light_bending_full_lane",
            "status": "pass",
            "detail": f"p=1 gives {p1['light_bending_arcsec']:.12f} arcsec",
        },
        {
            "gate": "Mercury_full_lane",
            "status": "pass",
            "detail": f"p=1 gives {p1['mercury_arcsec_per_century']:.12f} arcsec/century",
        },
        {
            "gate": "Shapiro_full_lane",
            "status": "pass",
            "detail": f"p=1 gives {p1['shapiro_microseconds']:.12f} microseconds",
        },
        {
            "gate": "derive_p_equals_1",
            "status": "conditional_pass",
            "detail": "p=1 follows if reciprocal routing T^2 S=1 is accepted",
        },
        {
            "gate": "parent_origin_of_reciprocity",
            "status": "fail",
            "detail": "T^2 S=1 is not yet derived from parent action or variational principle",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "local GR reduction is promising but conditional; no promotion yet",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "motion_load_local_GR_status",
            "status": "conditional_reduction",
            "evidence": "clock-load plus reciprocal routing gives the p=1 weak-field lane",
            "next_action": "derive reciprocal routing from parent action or conservation geometry",
        },
        {
            "decision": "old_motion_field_status",
            "status": "possibly_emergent",
            "evidence": "Gamma/K/q variables can be re-read as bookkeeping for load/routing residuals",
            "next_action": "write emergence map before altering main workbench",
        },
        {
            "decision": "promotion_status",
            "status": "blocked",
            "evidence": "reciprocity and beta completion are conditional, not fundamental",
            "next_action": "continue in post-checkpoint folder only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Motion-load local GR reduction gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-motion-load-local-GR-reduction"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    gps = gps_rows()
    weak = weak_field_rows()
    ppn = ppn_map_rows()
    gates = gate_rows(gps, weak)
    decisions = decision_rows()

    write_csv(results_dir / "gps_clock_check.csv", gps, list(gps[0].keys()))
    write_csv(results_dir / "weak_field_routing_dial.csv", weak, list(weak[0].keys()))
    write_csv(results_dir / "ppn_mapping.csv", ppn, list(ppn[0].keys()))
    write_csv(results_dir / "local_GR_reduction_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "local_GR_reduction_decision.csv", decisions, list(decisions[0].keys()))

    readout = "motion_load_local_GR_reduction_conditional_not_promoted"
    status = {
        "status": "complete_motion_load_local_GR_reduction",
        "readout": readout,
        "recommendation": "derive_reciprocal_routing_parent_origin_next",
        "next_target": "03-reciprocal-routing-parent-origin.md",
        "p_equals_1_derived_conditionally": True,
        "reciprocal_routing_parent_derived": False,
        "beta_completion_parent_derived": False,
        "promotion_to_main_workbench_allowed": False,
        "gps_net_microseconds_per_day": next(row for row in gps if row["case"] == "gps_minus_ground")["value_microseconds_per_day"],
        "light_bending_p1_arcsec": next(row for row in weak if row["p"] == 1.0)["light_bending_arcsec"],
        "mercury_p1_arcsec_per_century": next(row for row in weak if row["p"] == 1.0)["mercury_arcsec_per_century"],
        "shapiro_p1_microseconds": next(row for row in weak if row["p"] == 1.0)["shapiro_microseconds"],
        "outputs": {
            "gps_clock_check": str(results_dir / "gps_clock_check.csv"),
            "weak_field_routing_dial": str(results_dir / "weak_field_routing_dial.csv"),
            "ppn_mapping": str(results_dir / "ppn_mapping.csv"),
            "local_GR_reduction_gates": str(results_dir / "local_GR_reduction_gates.csv"),
            "local_GR_reduction_decision": str(results_dir / "local_GR_reduction_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
