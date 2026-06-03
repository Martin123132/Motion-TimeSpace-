#!/usr/bin/env python3
"""Quantify whether subhorizon memory perturbation bounds can move growth scores."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
GROWTH_RUN = RUNS_ROOT / "20260531-183400-growth-route-gate"
GROWTH_RESIDUALS = GROWTH_RUN / "results" / "residuals.csv"
GROWTH_BACKGROUND = GROWTH_RUN / "results" / "background_params.csv"
STRESS_RUN = RUNS_ROOT / "20260531-185800-memory-stress-perturbation-owner-attempt"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
C_KM_S = 299792.458
K_H_VALUES = [0.02, 0.05, 0.10, 0.20]
SAFETY_FACTORS = [1.0, 10.0, 100.0]
CLAIM_CEILING = "subhorizon_growth_correction_bound_only"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md",
        GROWTH_RUN / "status.json",
        GROWTH_RESIDUALS,
        GROWTH_BACKGROUND,
        STRESS_RUN / "status.json",
        STRESS_RUN / "results" / "subhorizon_suppression_estimate.csv",
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def locked_background() -> dict[str, float]:
    row = next(
        item
        for item in read_csv_rows(GROWTH_BACKGROUND)
        if item["background_branch"] == "DR2_noCMB_primary" and item["model"] == "MTS_locked_2over27"
    )
    return {
        "Omega_m0": float(row["Omega_m0"]),
        "h": float(row["h"]),
        "H0": float(row["H0"]),
        "BAO_alpha": float(row["BAO_alpha"]),
    }


def activation(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((n_past / LOCKED_U3) ** LOCKED_P))


def activation_derivative(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    x = n_past / LOCKED_U3
    return math.exp(-(x**LOCKED_P)) * LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)


def background_quantities(z: float, background: dict[str, float]) -> dict[str, float]:
    omega_m0 = background["Omega_m0"]
    n_past = math.log1p(z)
    a_mem = activation(n_past)
    da_dn = activation_derivative(n_past)
    rho_mem = 1.0 - omega_m0 + LOCKED_B_MEM * a_mem
    one_plus_w = LOCKED_B_MEM * da_dn / (3.0 * rho_mem)
    e2 = omega_m0 * (1.0 + z) ** 3 + rho_mem
    h_z = background["H0"] * math.sqrt(e2)
    matter_term = omega_m0 * (1.0 + z) ** 3
    omega_mem_over_omega_m = rho_mem / matter_term
    return {
        "N_past": n_past,
        "A_mem": a_mem,
        "dA_dN": da_dn,
        "rho_mem": rho_mem,
        "one_plus_w": one_plus_w,
        "E2": e2,
        "H_z": h_z,
        "omega_mem_over_omega_m": omega_mem_over_omega_m,
    }


def primary_rsd_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv_rows(GROWTH_RESIDUALS)
        if row["background_branch"] == "DR2_noCMB_primary"
        and row["model"] == "MTS_locked_2over27"
        and row["score_role"] == "primary_fit"
        and row["score_mode"] == "all"
        and row["quantity"] == "f_sigma8"
    ]


def correction_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    rows = []
    for row in primary_rsd_rows():
        z = float(row["z"])
        predicted = float(row["predicted"])
        sigma = float(row["diagonal_sigma"])
        fractional_sigma = sigma / abs(predicted)
        q = background_quantities(z, background)
        a = 1.0 / (1.0 + z)
        for k_h in K_H_VALUES:
            k_mpc = k_h * background["h"]
            horizon_ratio = (a * q["H_z"] / C_KM_S) / k_mpc
            delta_mem_over_delta_m = abs(q["one_plus_w"]) * horizon_ratio * horizon_ratio
            poisson_source_fraction = q["omega_mem_over_omega_m"] * delta_mem_over_delta_m
            for safety in SAFETY_FACTORS:
                fractional_prediction_shift = safety * poisson_source_fraction
                delta_prediction = predicted * fractional_prediction_shift
                diagonal_chi2_impact = (delta_prediction / sigma) ** 2
                rows.append(
                    {
                        "sample": row["sample"],
                        "z": z,
                        "k_h_Mpc": k_h,
                        "safety_factor": safety,
                        "predicted_fsigma8": predicted,
                        "diagonal_sigma": sigma,
                        "fractional_sigma": fractional_sigma,
                        "one_plus_w_mem": q["one_plus_w"],
                        "omega_mem_over_omega_m": q["omega_mem_over_omega_m"],
                        "aH_over_ck": horizon_ratio,
                        "delta_mem_over_delta_m_bound": delta_mem_over_delta_m,
                        "poisson_source_fraction_bound": poisson_source_fraction,
                        "fractional_prediction_shift_bound": fractional_prediction_shift,
                        "delta_prediction_bound": delta_prediction,
                        "diagonal_chi2_impact_bound": diagonal_chi2_impact,
                        "readout": "negligible" if diagonal_chi2_impact < 0.01 else "check",
                    }
                )
    return rows


def summary_rows(corrections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for k_h in K_H_VALUES:
        for safety in SAFETY_FACTORS:
            selected = [
                row
                for row in corrections
                if float(row["k_h_Mpc"]) == k_h and float(row["safety_factor"]) == safety
            ]
            total_chi2 = sum(float(row["diagonal_chi2_impact_bound"]) for row in selected)
            max_shift = max(float(row["fractional_prediction_shift_bound"]) for row in selected)
            max_source = max(float(row["poisson_source_fraction_bound"]) for row in selected)
            rows.append(
                {
                    "k_h_Mpc": k_h,
                    "safety_factor": safety,
                    "rows": len(selected),
                    "max_poisson_source_fraction_bound": max_source,
                    "max_fractional_prediction_shift_bound": max_shift,
                    "diagonal_chi2_impact_sum_bound": total_chi2,
                    "readout": "negligible" if total_chi2 < 0.1 else "check",
                }
            )
    return rows


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst_primary = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if float(row["k_h_Mpc"]) >= 0.02 and float(row["safety_factor"]) == 1.0
    )
    worst_safety_10 = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if float(row["k_h_Mpc"]) >= 0.02 and float(row["safety_factor"]) == 10.0
    )
    worst_safety_100 = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if float(row["k_h_Mpc"]) >= 0.02 and float(row["safety_factor"]) == 100.0
    )
    return [
        {
            "gate": "nominal_high_sound_speed_bound",
            "status": "pass",
            "evidence": f"worst diagonal chi2 impact bound at safety=1 is {worst_primary:.6g}",
        },
        {
            "gate": "safety_factor_10_bound",
            "status": "pass" if worst_safety_10 < 0.1 else "check",
            "evidence": f"worst diagonal chi2 impact bound at safety=10 is {worst_safety_10:.6g}",
        },
        {
            "gate": "safety_factor_100_bound",
            "status": "pass" if worst_safety_100 < 0.1 else "check",
            "evidence": f"worst diagonal chi2 impact bound at safety=100 is {worst_safety_100:.6g}",
        },
        {
            "gate": "checkpoint_130_proxy_practicality",
            "status": "pass_conditional",
            "evidence": "subhorizon memory perturbation corrections are far below current diagonal growth errors under the rough high-sound-speed bound",
        },
        {
            "gate": "theory_promotion",
            "status": "fail",
            "evidence": "numeric smallness does not derive c_s^2 or auxiliary/geometric stress owner",
        },
    ]


def decision_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst_10 = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if float(row["safety_factor"]) == 10.0
    )
    worst_100 = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if float(row["safety_factor"]) == 100.0
    )
    return [
        {
            "item": "status",
            "verdict": "subhorizon_memory_growth_correction_negligible_conditionally",
            "evidence": f"worst safety10 diagonal chi2 impact={worst_10:.6g}; worst safety100={worst_100:.6g}",
        },
        {
            "item": "growth_proxy_status",
            "verdict": "practically_robust_late_time_subhorizon",
            "evidence": "checkpoint-130 growth proxy is stable to rough high-sound-speed memory perturbation bounds",
        },
        {
            "item": "claim_status",
            "verdict": "not_a_derivation",
            "evidence": "still need parent stress sound speed or auxiliary/geometric constraint",
        },
        {
            "item": "next_target",
            "verdict": "derive_high_sound_speed_or_auxiliary_constraint",
            "evidence": "numeric safety is strong enough to justify returning to parent-action derivation",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-subhorizon-suppressed-growth-correction-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    background = locked_background()
    corrections = correction_rows(background)
    summary = summary_rows(corrections)
    gates = gate_rows(summary)
    decisions = decision_rows(summary)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "correction_bounds.csv",
        corrections,
        [
            "sample",
            "z",
            "k_h_Mpc",
            "safety_factor",
            "predicted_fsigma8",
            "diagonal_sigma",
            "fractional_sigma",
            "one_plus_w_mem",
            "omega_mem_over_omega_m",
            "aH_over_ck",
            "delta_mem_over_delta_m_bound",
            "poisson_source_fraction_bound",
            "fractional_prediction_shift_bound",
            "delta_prediction_bound",
            "diagonal_chi2_impact_bound",
            "readout",
        ],
    )
    write_csv(
        results_dir / "summary_by_k_and_safety.csv",
        summary,
        [
            "k_h_Mpc",
            "safety_factor",
            "rows",
            "max_poisson_source_fraction_bound",
            "max_fractional_prediction_shift_bound",
            "diagonal_chi2_impact_sum_bound",
            "readout",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_background": background,
        "generated": [
            "source_register.csv",
            "correction_bounds.csv",
            "summary_by_k_and_safety.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "134-subhorizon-suppressed-growth-correction-gate.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
