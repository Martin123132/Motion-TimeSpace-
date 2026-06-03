#!/usr/bin/env python3
"""Audit whether the smooth-memory lemma can be owned by a stress tensor."""

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
SMOOTH_RUN = RUNS_ROOT / "20260531-184700-smooth-memory-growth-theorem-attempt"
SMOOTH_FLUID = SMOOTH_RUN / "results" / "locked_effective_fluid.csv"
GROWTH_RUN = RUNS_ROOT / "20260531-183400-growth-route-gate"
GROWTH_BACKGROUND = GROWTH_RUN / "results" / "background_params.csv"

K_H_VALUES = [0.02, 0.05, 0.10, 0.20]
C_KM_S = 299792.458
CLAIM_CEILING = "memory_stress_owner_attempt_no_growth_promotion"


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
        WORK_DIR / "57-memory-action-owner-contract.md",
        WORK_DIR / "68-chiD-gated-memory-conservation-contract.md",
        WORK_DIR / "70-Ccoh-variation-and-boundary-current-audit.md",
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md",
        SMOOTH_RUN / "status.json",
        SMOOTH_FLUID,
        GROWTH_RUN / "status.json",
        GROWTH_BACKGROUND,
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
    rows = read_csv_rows(GROWTH_BACKGROUND)
    row = next(
        item
        for item in rows
        if item["background_branch"] == "DR2_noCMB_primary" and item["model"] == "MTS_locked_2over27"
    )
    return {
        "Omega_m0": float(row["Omega_m0"]),
        "h": float(row["h"]),
        "H0": float(row["H0"]),
        "BAO_alpha": float(row["BAO_alpha"]),
    }


def stress_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "pure_cosmological_constant",
            "stress_form": "T_mem^mu_nu = -rho_Lambda delta^mu_nu",
            "background_reproduction": "fails_transition",
            "linear_smoothness": "passes_exactly",
            "conservation": "passes",
            "verdict": "rejected_for_locked_A_of_a",
            "reason": "locked memory has w_mem != -1 during activation, so it cannot be only a cosmological constant",
        },
        {
            "candidate": "separately_conserved_perfect_fluid",
            "stress_form": "T_mem^mu_nu = (rho+p)u^mu u_nu + p delta^mu_nu",
            "background_reproduction": "passes",
            "linear_smoothness": "fails_exact_silence",
            "conservation": "fails_if_delta_theta_pi_all_zero_and_w_not_minus_one",
            "verdict": "rejected_as_exact_smooth_theorem",
            "reason": "Euler/energy equations source perturbations through (1+w) gravitational potentials unless w=-1 or counterterms exist",
        },
        {
            "candidate": "canonical_or_k_essence_high_sound_speed",
            "stress_form": "scalar-field-like smooth dark sector with c_s^2 ~ 1",
            "background_reproduction": "possible",
            "linear_smoothness": "subhorizon_suppressed_not_zero",
            "conservation": "passes_if_action_derived",
            "verdict": "viable_approximation_if_sound_speed_derived",
            "reason": "memory perturbations scale like (1+w)(aH/kc)^2 on SDSS/eBOSS subhorizon modes",
        },
        {
            "candidate": "auxiliary_constrained_memory",
            "stress_form": "chi_D/C_coh constrained sector with no propagating memory scalar",
            "background_reproduction": "possible",
            "linear_smoothness": "possible_exactly",
            "conservation": "open",
            "verdict": "best_exact_route_but_not_derived",
            "reason": "could make delta memory a constraint rather than a fluid perturbation, but S_stress and Bianchi bookkeeping are missing",
        },
        {
            "candidate": "geometric_counterstress",
            "stress_form": "memory term moved into geometric side E_mem^mu_nu with divergence-free completion",
            "background_reproduction": "possible",
            "linear_smoothness": "possible_if_completion_cancels_sources",
            "conservation": "open",
            "verdict": "viable_but_requires_real_parent_identity",
            "reason": "would avoid perfect-fluid Euler obstruction only if the geometric tensor is divergence-free on shell",
        },
        {
            "candidate": "controlled_exchange_Qnu",
            "stress_form": "nabla_mu T_mem^mu_nu = -Q_nu, nabla_mu T_m^mu_nu = Q_nu",
            "background_reproduction": "possible",
            "linear_smoothness": "possible_with_exchange",
            "conservation": "possible",
            "verdict": "dangerous_last_resort",
            "reason": "can cancel perturbation sources but risks becoming a fitted force unless Qnu is parent-derived and locally silent",
        },
    ]


def conservation_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "equation": "background_continuity",
            "silent_substitution": "rho'_N = 3(rho+p)",
            "obstruction": "none",
            "condition_for_exact_silence": "background defines w_mem(N)",
            "status": "passes_background",
        },
        {
            "equation": "linear_energy_conservation",
            "silent_substitution": "delta_mem=theta_mem=delta_p_mem=0",
            "obstruction": "3(1+w_mem) Phi_prime",
            "condition_for_exact_silence": "w_mem=-1 or Phi_prime=0 or non-perfect-fluid counterterm",
            "status": "fails_generically_during_activation",
        },
        {
            "equation": "linear_momentum_conservation",
            "silent_substitution": "theta_mem=delta_p_mem=pi_mem=0",
            "obstruction": "(1+w_mem) k^2 Psi",
            "condition_for_exact_silence": "w_mem=-1 or Psi=0 or constrained/geometric counterstress",
            "status": "fails_generically_during_activation",
        },
        {
            "equation": "Poisson_source",
            "silent_substitution": "delta_rho_mem=0",
            "obstruction": "none if a true constraint removes physical delta_rho_mem",
            "condition_for_exact_silence": "gauge-invariant delta_rho_mem is constrained, not merely gauge-set",
            "status": "open",
        },
        {
            "equation": "anisotropic_stress",
            "silent_substitution": "pi_mem=0",
            "obstruction": "depends on S_stress variation",
            "condition_for_exact_silence": "memory stress has no linear shear response",
            "status": "open",
        },
    ]


def suppression_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    rows = []
    h = background["h"]
    h0 = background["H0"]
    for item in read_csv_rows(SMOOTH_FLUID):
        z = float(item["z"])
        a = 1.0 / (1.0 + z)
        e2 = float(item["E2_locked"])
        h_z = h0 * math.sqrt(e2)
        one_plus_w = abs(float(item["one_plus_w_memory"]))
        for k_h in K_H_VALUES:
            k_mpc = k_h * h
            horizon_ratio = (a * h_z / C_KM_S) / k_mpc
            suppression = one_plus_w * horizon_ratio * horizon_ratio
            rows.append(
                {
                    "z": z,
                    "k_h_Mpc": k_h,
                    "aH_over_ck": horizon_ratio,
                    "aH_over_ck_squared": horizon_ratio * horizon_ratio,
                    "abs_one_plus_w_mem": one_plus_w,
                    "rough_delta_mem_over_delta_m_bound": suppression,
                    "readout": "subhorizon_suppressed" if suppression < 1.0e-3 else "check_large_scale",
                }
            )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "background_stress_reproduction",
            "status": "pass_effective",
            "evidence": "w_mem(N) can be defined from rho_mem(N)",
        },
        {
            "gate": "exact_smooth_perfect_fluid",
            "status": "fail",
            "evidence": "linear energy/momentum conservation sources perturbations when w_mem != -1",
        },
        {
            "gate": "subhorizon_suppression_viable",
            "status": "pass_conditional",
            "evidence": "for c_s^2~1-like behavior, rough (1+w)(aH/kc)^2 suppression is tiny on SDSS/eBOSS k >= 0.02 h/Mpc modes",
        },
        {
            "gate": "exact_auxiliary_or_geometric_owner",
            "status": "open",
            "evidence": "would evade perfect-fluid obstruction, but S_stress/Bianchi identity is not derived",
        },
        {
            "gate": "checkpoint_130_growth_proxy_promoted",
            "status": "fail",
            "evidence": "growth proxy remains conditional until stress owner derives smoothness or controlled modified growth",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "evidence": "internal theorem audit only",
        },
    ]


def decision_rows(suppression: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst_suppression = max(float(row["rough_delta_mem_over_delta_m_bound"]) for row in suppression)
    return [
        {
            "item": "status",
            "verdict": "perfect_fluid_exact_smooth_memory_rejected_subhorizon_route_open",
            "evidence": "exact silence fails for separately conserved perfect fluid with w_mem != -1; high-sound-speed or auxiliary/geometric owner remains viable",
        },
        {
            "item": "subhorizon_suppression_scale",
            "verdict": "small_on_tested_linear_modes",
            "evidence": f"max rough bound over sample z and k>=0.02 h/Mpc is {worst_suppression:.6g}",
        },
        {
            "item": "growth_proxy_status",
            "verdict": "not_promoted_but_not_killed",
            "evidence": "checkpoint-130 proxy can be an excellent approximation if the parent stress derives c_s^2~1 or a nonpropagating auxiliary memory constraint",
        },
        {
            "item": "next_target",
            "verdict": "test_subhorizon_suppressed_growth_or_derive_auxiliary_counterstress",
            "evidence": "choose between an approximate high-sound-speed growth correction and a stricter auxiliary/geometric stress derivation",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-memory-stress-perturbation-owner-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    background = locked_background()
    candidates = stress_candidate_rows()
    obstructions = conservation_obstruction_rows()
    suppression = suppression_rows(background)
    gates = gate_rows()
    decisions = decision_rows(suppression)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "stress_owner_candidates.csv",
        candidates,
        ["candidate", "stress_form", "background_reproduction", "linear_smoothness", "conservation", "verdict", "reason"],
    )
    write_csv(
        results_dir / "conservation_obstruction.csv",
        obstructions,
        ["equation", "silent_substitution", "obstruction", "condition_for_exact_silence", "status"],
    )
    write_csv(
        results_dir / "subhorizon_suppression_estimate.csv",
        suppression,
        [
            "z",
            "k_h_Mpc",
            "aH_over_ck",
            "aH_over_ck_squared",
            "abs_one_plus_w_mem",
            "rough_delta_mem_over_delta_m_bound",
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
            "stress_owner_candidates.csv",
            "conservation_obstruction.csv",
            "subhorizon_suppression_estimate.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "133-memory-stress-perturbation-owner-attempt.md",
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
    print(run_attempt(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
