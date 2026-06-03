#!/usr/bin/env python3
"""Benchmark the honest local closure route against PPN-style gates."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_12_STATUS = Path("runs/20260530-230810-gauge-noether-origin-audit/status.json")

G = 6.67430e-11
C = 299_792_458.0
DAY = 86400.0
ARCSEC_PER_RAD = 206_264.80624709636

M_EARTH = 5.9722e24
R_EARTH = 6_371_000.0
R_GPS = 26_560_000.0
V_GROUND = 465.1

M_SUN = 1.98847e30
R_SUN = 6.957e8
AU = 1.495978707e11
MERCURY_A = 57.909e9
MERCURY_E = 0.205630
MERCURY_PERIOD_DAYS = 87.9691
DAYS_PER_CENTURY = 36525.0

INTERNAL_GAMMA_GATE = 1.0e-5
INTERNAL_BETA_GATE = 1.0e-4


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def q_clock(mass: float, radius: float, speed: float = 0.0) -> float:
    return math.sqrt(1.0 - speed * speed / (C * C) - 2.0 * G * mass / (radius * C * C))


def microseconds_per_day(q_factor: float) -> float:
    return (q_factor - 1.0) * DAY * 1.0e6


def gr_mercury_precession_arcsec_century() -> float:
    delta_per_orbit = 6.0 * math.pi * G * M_SUN / (MERCURY_A * (1.0 - MERCURY_E**2) * C**2)
    return delta_per_orbit * ARCSEC_PER_RAD * (DAYS_PER_CENTURY / MERCURY_PERIOD_DAYS)


def assumptions_rows() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "clock_load",
            "equation": "T^2 = 1 - L, L=2GM/(rc^2)",
            "role": "sets local Newtonian clock/load factor",
            "status": "scaffold_assumption_not_full_parent_derivation",
        },
        {
            "assumption": "reciprocity_closure",
            "equation": "R_AB=ln(T^2 S)=0",
            "role": "forces S=1/T^2 and p=1",
            "status": "explicit_closure_not_derived",
        },
        {
            "assumption": "areal_radius",
            "equation": "angular sector = r^2 dOmega^2",
            "role": "makes the local closure identical to Schwarzschild exterior form",
            "status": "benchmark_completion",
        },
        {
            "assumption": "universal_matter_coupling",
            "equation": "matter sees the same observer coframe theta_0, theta_1",
            "role": "needed for equivalence-principle consistency",
            "status": "assumed_for_benchmark_not_parent_derived",
        },
        {
            "assumption": "no_reciprocal_hair",
            "equation": "Q_R=0",
            "role": "prevents gamma residuals from R_AB hair",
            "status": "implied_by_closure_not_current_theorem",
        },
    ]


def ppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "gamma",
            "benchmark_value": 1.0,
            "residual": 0.0,
            "internal_gate": INTERNAL_GAMMA_GATE,
            "status": "pass_under_closure",
            "derivation_status": "follows_from_R_AB_zero_closure",
        },
        {
            "quantity": "beta",
            "benchmark_value": 1.0,
            "residual": 0.0,
            "internal_gate": INTERNAL_BETA_GATE,
            "status": "pass_under_exact_schwarzschild_completion",
            "derivation_status": "benchmark_only_requires_exact_A_1_minus_L_and_areal_completion",
        },
        {
            "quantity": "preferred_frame_terms",
            "benchmark_value": 0.0,
            "residual": 0.0,
            "internal_gate": "not_set_in_this_script",
            "status": "assumed_absent_in_static_closure",
            "derivation_status": "not_parent_derived",
        },
        {
            "quantity": "reciprocal_hair_Q_R",
            "benchmark_value": 0.0,
            "residual": 0.0,
            "internal_gate": INTERNAL_GAMMA_GATE,
            "status": "pass_only_because_closure_sets_Q_R_zero",
            "derivation_status": "not_parent_derived",
        },
    ]


def solar_system_rows(gamma: float = 1.0, beta: float = 1.0) -> list[dict[str, Any]]:
    mu_earth = G * M_EARTH
    v_gps = math.sqrt(mu_earth / R_GPS)
    q_ground = q_clock(M_EARTH, R_EARTH, V_GROUND)
    q_gps = q_clock(M_EARTH, R_GPS, v_gps)

    light_bending = (1.0 + gamma) * 2.0 * G * M_SUN / (R_SUN * C**2) * ARCSEC_PER_RAD
    shapiro_log = math.log((4.0 * AU * AU) / (R_SUN * R_SUN))
    shapiro = (1.0 + gamma) * (G * M_SUN / C**3) * shapiro_log * 1.0e6
    ppn_perihelion_factor = (2.0 + 2.0 * gamma - beta) / 3.0
    mercury = ppn_perihelion_factor * gr_mercury_precession_arcsec_century()

    return [
        {
            "observable": "GPS_ground_vs_infinity",
            "value": microseconds_per_day(q_ground),
            "unit": "microseconds_per_day",
            "depends_on": "clock_load_T",
            "status": "benchmark_value",
        },
        {
            "observable": "GPS_satellite_vs_infinity",
            "value": microseconds_per_day(q_gps),
            "unit": "microseconds_per_day",
            "depends_on": "clock_load_T_plus_orbital_speed",
            "status": "benchmark_value",
        },
        {
            "observable": "GPS_satellite_minus_ground",
            "value": (q_gps - q_ground) * DAY * 1.0e6,
            "unit": "microseconds_per_day",
            "depends_on": "clock_load_T_plus_orbital_speed",
            "status": "benchmark_value",
        },
        {
            "observable": "solar_light_bending_limb",
            "value": light_bending,
            "unit": "arcsec",
            "depends_on": "gamma",
            "status": "passes_only_as_GR_equivalent_closure",
        },
        {
            "observable": "solar_shapiro_round_trip_scale",
            "value": shapiro,
            "unit": "microseconds",
            "depends_on": "gamma",
            "status": "passes_only_as_GR_equivalent_closure",
        },
        {
            "observable": "mercury_perihelion",
            "value": mercury,
            "unit": "arcsec_per_century",
            "depends_on": "gamma_beta",
            "status": "passes_only_as_GR_equivalent_closure",
        },
    ]


def deviation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gr_light = solar_system_rows(1.0, 1.0)[3]["value"]
    gr_shapiro = solar_system_rows(1.0, 1.0)[4]["value"]
    gr_mercury = solar_system_rows(1.0, 1.0)[5]["value"]
    for q_r in (-1.0e-4, -1.0e-5, 0.0, 1.0e-5, 1.0e-4):
        gamma = 1.0 + q_r
        beta = 1.0
        light = solar_system_rows(gamma, beta)[3]["value"]
        shapiro = solar_system_rows(gamma, beta)[4]["value"]
        mercury = solar_system_rows(gamma, beta)[5]["value"]
        rows.append(
            {
                "q_R_proxy": q_r,
                "gamma_proxy": gamma,
                "beta_proxy": beta,
                "light_bending_delta_arcsec": light - gr_light,
                "shapiro_delta_microseconds": shapiro - gr_shapiro,
                "mercury_delta_arcsec_per_century": mercury - gr_mercury,
                "internal_gamma_gate": INTERNAL_GAMMA_GATE,
                "status": "pass" if abs(q_r) <= INTERNAL_GAMMA_GATE else "fail",
            }
        )
    return rows


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "R_AB_zero",
            "tested_or_derived": "assumed_as_closure",
            "consequence": "p=1 and gamma=1",
            "claim_allowed": "benchmark_pass_not_parent_derivation",
        },
        {
            "item": "Schwarzschild_equivalence",
            "tested_or_derived": "mathematical_equivalence_under_closure",
            "consequence": "beta=1 if exact areal exterior is accepted",
            "claim_allowed": "closure_matches_GR_local_exterior",
        },
        {
            "item": "local_observables",
            "tested_or_derived": "computed",
            "consequence": "same values as GR closure",
            "claim_allowed": "sanity_check_only",
        },
        {
            "item": "parent_origin",
            "tested_or_derived": "not_derived",
            "consequence": "no fundamental claim",
            "claim_allowed": "must_remain_open",
        },
        {
            "item": "empirical_novelty",
            "tested_or_derived": "none_in_local_vacuum_closure",
            "consequence": "look to deviations, cosmology, galaxies, EM, or parent action",
            "claim_allowed": "closure_is_control_baseline",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_12_complete",
            "status": "pass" if source.get("readout") == "gauge_noether_origin_not_derived_closure_only" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "closure_assumptions_explicit",
            "status": "pass",
            "detail": "R_AB=0, Q_R=0, areal completion, and universal coupling are labeled assumptions",
        },
        {
            "gate": "gamma_passes_under_closure",
            "status": "pass",
            "detail": "gamma=1 exactly when R_AB=0",
        },
        {
            "gate": "beta_passes_under_exact_completion",
            "status": "conditional_pass",
            "detail": "beta=1 if closure is completed as exact Schwarzschild exterior in areal radius",
        },
        {
            "gate": "closure_not_mislabeled_as_derivation",
            "status": "pass",
            "detail": "outputs separate benchmark consequences from parent derivation",
        },
        {
            "gate": "novel_local_prediction",
            "status": "fail",
            "detail": "the closure reproduces GR locally by construction; novelty must come from derivation or controlled deviations",
        },
        {
            "gate": "promotion_to_main_workbench_as_derived",
            "status": "fail",
            "detail": "allowed only as future benchmark/control, not as derived GR",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "local_closure_status",
            "status": "valid_control_baseline",
            "evidence": "closure gives GR-equivalent local PPN values",
            "next_action": "use it as null benchmark for deviations and parent-action tests",
        },
        {
            "decision": "claim_status",
            "status": "not_fundamental_derivation",
            "evidence": "R_AB=0 and Q_R=0 are assumptions in the benchmark",
            "next_action": "do not promote as proof",
        },
        {
            "decision": "next_target",
            "status": "deviation_sensitivity",
            "evidence": "q_R residuals directly perturb gamma-like observables",
            "next_action": "create 14-closure-deviation-PPN-sensitivity.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Local closure PPN benchmark.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_12_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-local-closure-PPN-benchmark"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    assumptions = assumptions_rows()
    ppn = ppn_rows()
    solar = solar_system_rows()
    deviations = deviation_rows()
    statuses = status_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "closure_assumptions.csv", assumptions, list(assumptions[0].keys()))
    write_csv(results_dir / "closure_ppn_coefficients.csv", ppn, list(ppn[0].keys()))
    write_csv(results_dir / "closure_solar_system_benchmarks.csv", solar, list(solar[0].keys()))
    write_csv(results_dir / "closure_deviation_sensitivity.csv", deviations, list(deviations[0].keys()))
    write_csv(results_dir / "closure_claim_status.csv", statuses, list(statuses[0].keys()))
    write_csv(results_dir / "closure_ppn_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "closure_ppn_decision.csv", decisions, list(decisions[0].keys()))

    readout = "local_closure_ppn_benchmark_valid_control_not_derivation"
    status = {
        "status": "complete_local_closure_ppn_benchmark",
        "readout": readout,
        "recommendation": "run_closure_deviation_sensitivity_next",
        "next_target": "14-closure-deviation-PPN-sensitivity.md",
        "closure_is_valid_control_baseline": True,
        "closure_is_parent_derivation": False,
        "promotion_to_main_workbench_as_derived_allowed": False,
        "benchmark_numbers": {
            "gamma": 1.0,
            "beta": 1.0,
            "gps_net_microseconds_per_day": next(row for row in solar if row["observable"] == "GPS_satellite_minus_ground")["value"],
            "solar_light_bending_arcsec": next(row for row in solar if row["observable"] == "solar_light_bending_limb")["value"],
            "solar_shapiro_microseconds": next(row for row in solar if row["observable"] == "solar_shapiro_round_trip_scale")["value"],
            "mercury_arcsec_per_century": next(row for row in solar if row["observable"] == "mercury_perihelion")["value"],
        },
        "outputs": {
            "closure_assumptions": str(results_dir / "closure_assumptions.csv"),
            "closure_ppn_coefficients": str(results_dir / "closure_ppn_coefficients.csv"),
            "closure_solar_system_benchmarks": str(results_dir / "closure_solar_system_benchmarks.csv"),
            "closure_deviation_sensitivity": str(results_dir / "closure_deviation_sensitivity.csv"),
            "closure_claim_status": str(results_dir / "closure_claim_status.csv"),
            "closure_ppn_gates": str(results_dir / "closure_ppn_gates.csv"),
            "closure_ppn_decision": str(results_dir / "closure_ppn_decision.csv"),
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
