#!/usr/bin/env python3
"""Attempt the smooth-memory theorem behind the checkpoint-130 growth proxy."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
GROWTH_RUN = RUNS_ROOT / "20260531-183400-growth-route-gate"
GROWTH_BACKGROUND = GROWTH_RUN / "results" / "background_params.csv"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
SAMPLE_Z = [0.0, 0.15, 0.38, 0.51, 0.698, 1.48, 2.33]
CLAIM_CEILING = "smooth_memory_theorem_attempt_conditional_only"


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
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "57-memory-action-owner-contract.md",
        WORK_DIR / "68-chiD-gated-memory-conservation-contract.md",
        WORK_DIR / "70-Ccoh-variation-and-boundary-current-audit.md",
        WORK_DIR / "72-relative-current-action-owner-attempt.md",
        WORK_DIR / "73-local-route-blocker-ledger-and-promotion-gate.md",
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "131-growth-perturbation-contract.md",
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


def load_locked_background() -> dict[str, float]:
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
        "rd_inferred_from_alpha_h": float(row["rd_inferred_from_alpha_h"]),
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


def effective_fluid_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    omega_m = background["Omega_m0"]
    rows = []
    for z in SAMPLE_Z:
        n_past = math.log1p(z)
        a_mem = activation(n_past)
        da_dn = activation_derivative(n_past)
        rho_x = 1.0 - omega_m + LOCKED_B_MEM * a_mem
        w_x = -1.0 + LOCKED_B_MEM * da_dn / (3.0 * rho_x)
        e2 = omega_m * (1.0 + z) ** 3 + rho_x
        omega_m_a = omega_m * (1.0 + z) ** 3 / e2
        rows.append(
            {
                "z": z,
                "N_past": n_past,
                "A_mem": a_mem,
                "dA_dN": da_dn,
                "rho_memory_effective_over_rhocrit0": rho_x,
                "w_memory_if_separately_conserved": w_x,
                "one_plus_w_memory": 1.0 + w_x,
                "E2_locked": e2,
                "Omega_m_of_a": omega_m_a,
            }
        )
    return rows


def linear_coherence_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "Ccoh_linear_variation",
            "mathematical_statement": "For theta=theta0+epsilon*dtheta, sigma^2=O(epsilon^2), omega^2=O(epsilon^2), and eps_D=0, dCcoh/depsilon at epsilon=0 is exactly zero.",
            "derivation": "Both <theta>^2 and <theta^2> have the same linear term 2 theta0 <dtheta>; their ratio changes only at second order.",
            "status": "pass_conditional",
            "blocker": "requires eps_D not to contribute at first order and requires a domain average meaningful for the perturbation mode",
        },
        {
            "condition": "shear_vorticity_entry",
            "mathematical_statement": "sigma^2 and omega^2 enter Ccoh quadratically in scalar/vector perturbation amplitude.",
            "derivation": "The background FLRW shear and vorticity vanish, so their squared norms have no first-order piece.",
            "status": "pass_linear_order",
            "blocker": "second-order backreaction remains outside the linear growth gate",
        },
        {
            "condition": "auxiliary_selector",
            "mathematical_statement": "If chi_D is constrained algebraically to Ccoh, then delta chi_D^(1)=0 in the FLRW bulk linear branch.",
            "derivation": "checkpoint 67/68 auxiliary selector route plus the Ccoh linear cancellation",
            "status": "pass_conditional",
            "blocker": "constraint action and boundary exchange current are not fully derived",
        },
        {
            "condition": "memory_exposure",
            "mathematical_statement": "If I_M=det(Q_coh) is a coherent-domain/global invariant, nonzero-k linear perturbations do not source an independent local delta I_M.",
            "derivation": "domain determinant responds to coherent/background load; non-coherent linear modes average out or enter Ccoh only at second order",
            "status": "pass_conditional",
            "blocker": "Q_coh parent field and representative selection are not derived",
        },
        {
            "condition": "smooth_stress_tensor",
            "mathematical_statement": "A smooth memory stress has delta rho_mem=delta p_mem=theta_mem=pi_mem=0 at leading quasi-static order in the selected memory/comoving gauge.",
            "derivation": "there is no independent scalar perturbation after the auxiliary/domain constraints are imposed",
            "status": "open_conditional",
            "blocker": "stress tensor S_stress and gauge-invariant perturbation statement are not yet derived",
        },
        {
            "condition": "Bianchi_identity",
            "mathematical_statement": "nabla_mu(T_matter^munu+T_mem^munu+T_aux^munu)=0 must hold on shell.",
            "derivation": "action-level Noether identity if the missing parent action exists",
            "status": "fail_not_derived",
            "blocker": "boundary exchange/current and S_stress are still missing",
        },
    ]


def perturbation_proxy_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "F_fric",
            "checkpoint_130_value": 0.0,
            "smooth_memory_condition": "no independent memory momentum perturbation and separately conserved matter",
            "status": "allowed_conditionally",
        },
        {
            "term": "mu",
            "checkpoint_130_value": 1.0,
            "smooth_memory_condition": "no memory density perturbation contributes to subhorizon Poisson equation",
            "status": "allowed_conditionally",
        },
        {
            "term": "S_mem",
            "checkpoint_130_value": 0.0,
            "smooth_memory_condition": "memory perturbation is constrained away or second-order in Ccoh",
            "status": "allowed_conditionally",
        },
        {
            "term": "eta_slip",
            "checkpoint_130_value": 1.0,
            "smooth_memory_condition": "no memory anisotropic stress at linear order",
            "status": "open_not_derived",
        },
    ]


def gate_rows(condition_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "linear_Ccoh_cancellation",
            "status": "pass_conditional",
            "evidence": "dCcoh/depsilon vanishes at FLRW linear order when eps_D is not a first-order source",
        },
        {
            "gate": "auxiliary_nonpropagating_selector",
            "status": "pass_contract",
            "evidence": "prior checkpoints allow chi_D as auxiliary/constrained, not a propagating scalar",
        },
        {
            "gate": "memory_density_perturbation_removed",
            "status": "open_conditional",
            "evidence": "requires S_stress and gauge-invariant stress perturbation derivation",
        },
        {
            "gate": "Bianchi_conservation",
            "status": "fail_not_derived",
            "evidence": "boundary exchange/current and total stress owner remain open",
        },
        {
            "gate": "GR_growth_proxy_promoted",
            "status": "fail",
            "evidence": "smooth memory theorem is conditional, not action-derived",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "evidence": "conditional theorem target only; no public claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "smooth_memory_theorem_conditional_not_derived",
            "evidence": "linear Ccoh cancellation supports smooth memory, but stress/Bianchi/gauge ownership is not derived",
        },
        {
            "item": "usefulness",
            "verdict": "strong_theorem_target",
            "evidence": "the FLRW coherent-domain invariant can be first-order silent without arbitrary tuning",
        },
        {
            "item": "growth_proxy_status",
            "verdict": "conditionally_supported_not_promoted",
            "evidence": "checkpoint-130 F_fric=0, mu=1, S_mem=0 follows if smooth stress conditions are later derived",
        },
        {
            "item": "next_target",
            "verdict": "derive_stress_owner_or_modified_growth",
            "evidence": "need S_stress perturbation variation; if it fails, derive controlled mu(a,k)/friction/source",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-smooth-memory-growth-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in source_rows if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    background = load_locked_background()
    fluid_rows = effective_fluid_rows(background)
    condition_rows = linear_coherence_rows()
    proxy_rows = perturbation_proxy_rows()
    gates = gate_rows(condition_rows)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "locked_effective_fluid.csv",
        fluid_rows,
        [
            "z",
            "N_past",
            "A_mem",
            "dA_dN",
            "rho_memory_effective_over_rhocrit0",
            "w_memory_if_separately_conserved",
            "one_plus_w_memory",
            "E2_locked",
            "Omega_m_of_a",
        ],
    )
    write_csv(
        results_dir / "linear_smoothness_conditions.csv",
        condition_rows,
        ["condition", "mathematical_statement", "derivation", "status", "blocker"],
    )
    write_csv(
        results_dir / "growth_proxy_terms.csv",
        proxy_rows,
        ["term", "checkpoint_130_value", "smooth_memory_condition", "status"],
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
            "locked_effective_fluid.csv",
            "linear_smoothness_conditions.csv",
            "growth_proxy_terms.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "132-smooth-memory-growth-theorem-attempt.md",
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
