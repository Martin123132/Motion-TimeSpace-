#!/usr/bin/env python3
"""Quantify local PPN sensitivity to leaks away from the closure benchmark."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_13_STATUS = Path("runs/20260530-231158-local-closure-PPN-benchmark/status.json")

G = 6.67430e-11
C = 299_792_458.0
DAY = 86400.0
ARCSEC_PER_RAD = 206_264.80624709636

M_EARTH = 5.9722e24
R_EARTH = 6_371_000.0
R_GPS = 26_560_000.0

M_SUN = 1.98847e30
R_SUN = 6.957e8
AU = 1.495978707e11
MERCURY_A = 57.909e9
MERCURY_E = 0.205630
MERCURY_PERIOD_DAYS = 87.9691
DAYS_PER_CENTURY = 36525.0

INTERNAL_GAMMA_GATE = 1.0e-5
INTERNAL_BETA_GATE = 1.0e-4
INTERNAL_CLOCK_GATE = 1.0e-5
INTERNAL_EP_GATE = 1.0e-8


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def gr_mercury_precession_arcsec_century() -> float:
    delta_per_orbit = 6.0 * math.pi * G * M_SUN / (MERCURY_A * (1.0 - MERCURY_E**2) * C**2)
    return delta_per_orbit * ARCSEC_PER_RAD * (DAYS_PER_CENTURY / MERCURY_PERIOD_DAYS)


def light_bending_arcsec(gamma: float) -> float:
    return (1.0 + gamma) * 2.0 * G * M_SUN / (R_SUN * C**2) * ARCSEC_PER_RAD


def shapiro_microseconds(gamma: float) -> float:
    shapiro_log = math.log((4.0 * AU * AU) / (R_SUN * R_SUN))
    return (1.0 + gamma) * (G * M_SUN / C**3) * shapiro_log * 1.0e6


def mercury_arcsec_century(gamma: float, beta: float) -> float:
    ppn_factor = (2.0 + 2.0 * gamma - beta) / 3.0
    return ppn_factor * gr_mercury_precession_arcsec_century()


def gravitational_gps_redshift_us_day() -> float:
    ground = math.sqrt(1.0 - 2.0 * G * M_EARTH / (R_EARTH * C * C))
    gps = math.sqrt(1.0 - 2.0 * G * M_EARTH / (R_GPS * C * C))
    return (gps - ground) * DAY * 1.0e6


def perturbation_dictionary_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": "q_R",
            "meaning": "reciprocal hair coefficient in R_AB approximately q_R L",
            "primary_mapping": "gamma-1 approximately q_R",
            "main_observables": "light_bending; Shapiro; Mercury via gamma",
            "internal_gate": INTERNAL_GAMMA_GATE,
        },
        {
            "parameter": "delta_beta",
            "meaning": "nonlinear temporal/spatial completion drift beta-1",
            "primary_mapping": "Mercury perihelion factor shifts by -delta_beta/3",
            "main_observables": "perihelion/orbital dynamics",
            "internal_gate": INTERNAL_BETA_GATE,
        },
        {
            "parameter": "alpha_clock",
            "meaning": "gravitational clock-redshift anomaly",
            "primary_mapping": "GPS redshift anomaly approximately alpha_clock times gravitational redshift",
            "main_observables": "clock comparisons; GPS-like redshift tests",
            "internal_gate": INTERNAL_CLOCK_GATE,
        },
        {
            "parameter": "epsilon_matter",
            "meaning": "matter-sector coupling spread relative to the common observer coframe",
            "primary_mapping": "Eotvos-like differential acceleration proxy",
            "main_observables": "equivalence-principle tests",
            "internal_gate": INTERNAL_EP_GATE,
        },
        {
            "parameter": "Q_R",
            "meaning": "conserved reciprocal charge from a kinetic/current route",
            "primary_mapping": "creates exterior R_AB hair and therefore q_R-like residuals",
            "main_observables": "same as gamma residual plus source-dependent signatures",
            "internal_gate": "must be zero under closure",
        },
    ]


def q_r_sensitivity_rows() -> list[dict[str, Any]]:
    base_light = light_bending_arcsec(1.0)
    base_shapiro = shapiro_microseconds(1.0)
    base_mercury = mercury_arcsec_century(1.0, 1.0)
    rows: list[dict[str, Any]] = []
    for q_r in (-1.0e-3, -1.0e-4, -1.0e-5, -1.0e-6, 0.0, 1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3):
        gamma = 1.0 + q_r
        rows.append(
            {
                "q_R": q_r,
                "gamma_proxy": gamma,
                "light_bending_delta_arcsec": light_bending_arcsec(gamma) - base_light,
                "shapiro_delta_microseconds": shapiro_microseconds(gamma) - base_shapiro,
                "mercury_delta_arcsec_per_century": mercury_arcsec_century(gamma, 1.0) - base_mercury,
                "internal_gamma_gate": INTERNAL_GAMMA_GATE,
                "status": "pass_internal_gate" if abs(q_r) <= INTERNAL_GAMMA_GATE else "fail_internal_gate",
            }
        )
    return rows


def beta_sensitivity_rows() -> list[dict[str, Any]]:
    base_mercury = mercury_arcsec_century(1.0, 1.0)
    rows: list[dict[str, Any]] = []
    for delta_beta in (-1.0e-3, -1.0e-4, -1.0e-5, 0.0, 1.0e-5, 1.0e-4, 1.0e-3):
        beta = 1.0 + delta_beta
        rows.append(
            {
                "delta_beta": delta_beta,
                "beta_proxy": beta,
                "mercury_delta_arcsec_per_century": mercury_arcsec_century(1.0, beta) - base_mercury,
                "internal_beta_gate": INTERNAL_BETA_GATE,
                "status": "pass_internal_gate" if abs(delta_beta) <= INTERNAL_BETA_GATE else "fail_internal_gate",
            }
        )
    return rows


def combined_gamma_beta_rows() -> list[dict[str, Any]]:
    base_mercury = mercury_arcsec_century(1.0, 1.0)
    rows: list[dict[str, Any]] = []
    for q_r in (-1.0e-4, -1.0e-5, 0.0, 1.0e-5, 1.0e-4):
        for delta_beta in (-1.0e-4, 0.0, 1.0e-4):
            gamma = 1.0 + q_r
            beta = 1.0 + delta_beta
            rows.append(
                {
                    "q_R": q_r,
                    "delta_beta": delta_beta,
                    "ppn_perihelion_factor_minus_1": (2.0 * q_r - delta_beta) / 3.0,
                    "mercury_delta_arcsec_per_century": mercury_arcsec_century(gamma, beta) - base_mercury,
                    "status": "pass_internal_gates"
                    if abs(q_r) <= INTERNAL_GAMMA_GATE and abs(delta_beta) <= INTERNAL_BETA_GATE
                    else "fail_one_or_more_internal_gates",
                }
            )
    return rows


def clock_matter_rows() -> list[dict[str, Any]]:
    redshift = gravitational_gps_redshift_us_day()
    rows: list[dict[str, Any]] = []
    for alpha_clock in (-1.0e-4, -1.0e-5, 0.0, 1.0e-5, 1.0e-4):
        rows.append(
            {
                "parameter": "alpha_clock",
                "value": alpha_clock,
                "gps_gravitational_redshift_delta_us_day": alpha_clock * redshift,
                "eotvos_proxy": "",
                "internal_gate": INTERNAL_CLOCK_GATE,
                "status": "pass_internal_gate" if abs(alpha_clock) <= INTERNAL_CLOCK_GATE else "fail_internal_gate",
            }
        )
    for epsilon_matter in (-1.0e-7, -1.0e-8, 0.0, 1.0e-8, 1.0e-7):
        rows.append(
            {
                "parameter": "epsilon_matter",
                "value": epsilon_matter,
                "gps_gravitational_redshift_delta_us_day": "",
                "eotvos_proxy": abs(epsilon_matter),
                "internal_gate": INTERNAL_EP_GATE,
                "status": "pass_internal_gate" if abs(epsilon_matter) <= INTERNAL_EP_GATE else "fail_internal_gate",
            }
        )
    return rows


def observable_coefficients_rows() -> list[dict[str, Any]]:
    base_light = light_bending_arcsec(1.0)
    base_shapiro = shapiro_microseconds(1.0)
    base_mercury = mercury_arcsec_century(1.0, 1.0)
    redshift = gravitational_gps_redshift_us_day()
    return [
        {
            "observable": "solar_light_bending",
            "parameter": "q_R",
            "linear_coefficient": base_light / 2.0,
            "unit": "arcsec per unit q_R",
            "interpretation": "delta light bending = coefficient * q_R",
        },
        {
            "observable": "solar_shapiro",
            "parameter": "q_R",
            "linear_coefficient": base_shapiro / 2.0,
            "unit": "microseconds per unit q_R",
            "interpretation": "delta Shapiro = coefficient * q_R",
        },
        {
            "observable": "mercury_perihelion_gamma",
            "parameter": "q_R",
            "linear_coefficient": 2.0 * base_mercury / 3.0,
            "unit": "arcsec/century per unit q_R",
            "interpretation": "delta Mercury = coefficient * q_R when beta fixed",
        },
        {
            "observable": "mercury_perihelion_beta",
            "parameter": "delta_beta",
            "linear_coefficient": -base_mercury / 3.0,
            "unit": "arcsec/century per unit delta_beta",
            "interpretation": "delta Mercury = coefficient * delta_beta when gamma fixed",
        },
        {
            "observable": "gps_gravitational_redshift",
            "parameter": "alpha_clock",
            "linear_coefficient": redshift,
            "unit": "microseconds/day per unit alpha_clock",
            "interpretation": "delta redshift = coefficient * alpha_clock",
        },
        {
            "observable": "eotvos_proxy",
            "parameter": "epsilon_matter",
            "linear_coefficient": 1.0,
            "unit": "dimensionless proxy per unit coupling spread",
            "interpretation": "eta proxy = |epsilon_A-epsilon_B|",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_13_complete",
            "status": "pass" if source.get("readout") == "local_closure_ppn_benchmark_valid_control_not_derivation" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "q_R_sensitivity_quantified",
            "status": "pass",
            "detail": "q_R maps to gamma-1 and shifts light bending, Shapiro, and Mercury",
        },
        {
            "gate": "beta_sensitivity_quantified",
            "status": "pass",
            "detail": "delta_beta shifts Mercury through -(delta_beta/3) of the GR perihelion scale",
        },
        {
            "gate": "clock_matter_sensitivity_quantified",
            "status": "pass",
            "detail": "alpha_clock and epsilon_matter are separated into redshift and Eotvos-like proxies",
        },
        {
            "gate": "uses_real_literature_bounds",
            "status": "fail",
            "detail": "this is an internal sensitivity budget only; current observational bounds are not imported here",
        },
        {
            "gate": "closure_promoted_to_derivation",
            "status": "fail",
            "detail": "deviation budget tests closure leakage; it does not derive R_AB=0",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "local_deviation_budget_status",
            "status": "usable_internal_budget",
            "evidence": "each closure leak has a mapped observable channel and internal gate",
            "next_action": "connect these channels to real data/bounds before making empirical claims",
        },
        {
            "decision": "most_dangerous_leak",
            "status": "q_R_or_matter_coupling",
            "evidence": "q_R immediately shifts gamma-like observables; epsilon_matter breaks universal coupling",
            "next_action": "treat Q_R=0 and universal coupling as high-priority parent-action gates",
        },
        {
            "decision": "next_target",
            "status": "local_observables_data_map",
            "evidence": "sensitivity is quantified but not tied to current measurement datasets",
            "next_action": "create 15-local-observables-data-map.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Closure-deviation PPN sensitivity budget.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_13_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-closure-deviation-PPN-sensitivity"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    dictionary = perturbation_dictionary_rows()
    q_r = q_r_sensitivity_rows()
    beta = beta_sensitivity_rows()
    combined = combined_gamma_beta_rows()
    clock_matter = clock_matter_rows()
    coefficients = observable_coefficients_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "perturbation_dictionary.csv", dictionary, list(dictionary[0].keys()))
    write_csv(results_dir / "qR_gamma_observable_sensitivity.csv", q_r, list(q_r[0].keys()))
    write_csv(results_dir / "beta_perihelion_sensitivity.csv", beta, list(beta[0].keys()))
    write_csv(results_dir / "combined_gamma_beta_perihelion_grid.csv", combined, list(combined[0].keys()))
    write_csv(results_dir / "clock_matter_coupling_sensitivity.csv", clock_matter, list(clock_matter[0].keys()))
    write_csv(results_dir / "observable_linear_coefficients.csv", coefficients, list(coefficients[0].keys()))
    write_csv(results_dir / "closure_deviation_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "closure_deviation_decision.csv", decisions, list(decisions[0].keys()))

    readout = "closure_deviation_ppn_sensitivity_internal_budget_complete"
    status = {
        "status": "complete_closure_deviation_ppn_sensitivity",
        "readout": readout,
        "recommendation": "map_local_observables_to_real_data_next",
        "next_target": "15-local-observables-data-map.md",
        "internal_budget_complete": True,
        "uses_real_literature_bounds": False,
        "closure_is_parent_derivation": False,
        "key_linear_coefficients": {
            row["observable"] + "_vs_" + row["parameter"]: row["linear_coefficient"]
            for row in coefficients
        },
        "outputs": {
            "perturbation_dictionary": str(results_dir / "perturbation_dictionary.csv"),
            "qR_gamma_observable_sensitivity": str(results_dir / "qR_gamma_observable_sensitivity.csv"),
            "beta_perihelion_sensitivity": str(results_dir / "beta_perihelion_sensitivity.csv"),
            "combined_gamma_beta_perihelion_grid": str(results_dir / "combined_gamma_beta_perihelion_grid.csv"),
            "clock_matter_coupling_sensitivity": str(results_dir / "clock_matter_coupling_sensitivity.csv"),
            "observable_linear_coefficients": str(results_dir / "observable_linear_coefficients.csv"),
            "closure_deviation_gates": str(results_dir / "closure_deviation_gates.csv"),
            "closure_deviation_decision": str(results_dir / "closure_deviation_decision.csv"),
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
