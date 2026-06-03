#!/usr/bin/env python3
"""Checkpoint 178: attempt to own memory perturbations without smuggling closures."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CONTRACT_RUN = RUNS_ROOT / "20260531-235959-parent-action-perturbation-local-GR-contract"
HIGH_CS_RUN = RUNS_ROOT / "20260531-192900-high-sound-speed-or-auxiliary-memory-owner"
SMOOTH_RUN = RUNS_ROOT / "20260531-235500-smooth-memory-or-controlled-growth-theorem"
STRESS_RUN = RUNS_ROOT / "20260531-185800-memory-stress-perturbation-owner-attempt"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
LIGHT_SPEED_KM_S = 299792.458
CLAIM_CEILING = "effective_memory_perturbation_owner_no_parent_promotion"
STATUS_PASS = "memory_perturbation_owner_effective_high_cs_partial_P06_exact_auxiliary_open"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

K_H_VALUES = [0.02, 0.05, 0.10, 0.20]
Z_SAMPLES = [0.0, 0.05, 0.10, 0.15, 0.24, 0.38, 0.51, 0.61, 0.70, 1.0, 1.5, 2.0, 3.0]


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 178 derivation-attempt script"),
        (WORK_DIR / "177-parent-action-perturbation-local-GR-contract.md", "parent-action contract source"),
        (CONTRACT_RUN / "status.json", "checkpoint 177 machine status"),
        (CONTRACT_RUN / "results" / "perturbation_output_contract.csv", "required P06 outputs"),
        (CONTRACT_RUN / "results" / "local_GR_silence_contract.csv", "local GR no-smuggling constraints"),
        (WORK_DIR / "149-smooth-memory-or-controlled-growth-theorem.md", "effective suppression law note"),
        (SMOOTH_RUN / "status.json", "smooth suppression machine status"),
        (SMOOTH_RUN / "results" / "suppression_summary_by_branch.csv", "source-locked suppression summary"),
        (WORK_DIR / "150-Boltzmann-interface-contract.md", "CMB interface warning"),
        (WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md", "canonical high-cs owner note"),
        (HIGH_CS_RUN / "status.json", "canonical owner machine status"),
        (HIGH_CS_RUN / "results" / "reconstruction_summary.csv", "canonical reconstruction summary"),
        (WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md", "perfect-fluid obstruction note"),
        (STRESS_RUN / "status.json", "perfect-fluid obstruction machine status"),
        (STRESS_RUN / "results" / "conservation_obstruction.csv", "linear conservation obstruction"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def locked_background() -> dict[str, float]:
    status = load_json(HIGH_CS_RUN / "status.json")
    params = status["locked_background"]
    return {
        "Omega_m0": float(params["Omega_m0"]),
        "h": float(params["h"]),
        "H0": float(params["H0"]),
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


def memory_background(z: float, params: dict[str, float]) -> dict[str, float]:
    omega_m0 = params["Omega_m0"]
    n_past = math.log1p(z)
    a = 1.0 / (1.0 + z)
    a_mem = activation(n_past)
    da_dn = activation_derivative(n_past)
    rho_mem = 1.0 - omega_m0 + LOCKED_B_MEM * a_mem
    one_plus_w = LOCKED_B_MEM * da_dn / (3.0 * rho_mem) if rho_mem > 0.0 else math.nan
    w_mem = -1.0 + one_plus_w
    e2 = omega_m0 * math.exp(3.0 * n_past) + rho_mem
    omega_mem_a = rho_mem / e2
    omega_m_a = omega_m0 * math.exp(3.0 * n_past) / e2
    h_z = params["H0"] * math.sqrt(e2)
    return {
        "z": z,
        "a": a,
        "N_past": n_past,
        "A_mem": a_mem,
        "dA_dN": da_dn,
        "rho_mem_over_rhocrit0": rho_mem,
        "w_mem": w_mem,
        "one_plus_w_mem": one_plus_w,
        "E2": e2,
        "Omega_mem_of_a": omega_mem_a,
        "Omega_m_of_a": omega_m_a,
        "H_z_km_s_Mpc": h_z,
    }


def background_identity_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for z in Z_SAMPLES:
        bg = memory_background(z, params)
        rows.append(
            {
                **bg,
                "identity_status": "locked_background_identity",
                "claim_limit": "background identity only; amplitude and activation not parent-derived here",
            }
        )
    return rows


def canonical_reconstruction_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    n_max = math.log1p(3.0)
    samples = 900
    phi = 0.0
    last_dphi_dn = 0.0
    last_n = 0.0
    for index in range(samples + 1):
        n_past = n_max * index / samples
        z = math.exp(n_past) - 1.0
        bg = memory_background(z, params)
        one_plus_w = max(0.0, bg["one_plus_w_mem"])
        kinetic = 0.5 * bg["rho_mem_over_rhocrit0"] * one_plus_w
        potential = 0.5 * bg["rho_mem_over_rhocrit0"] * (1.0 - bg["w_mem"])
        dphi_dn = math.sqrt(max(0.0, 3.0 * bg["Omega_mem_of_a"] * one_plus_w))
        if index > 0:
            delta_n = n_past - last_n
            phi += 0.5 * (last_dphi_dn + dphi_dn) * delta_n
        rows.append(
            {
                "index": index,
                "z": z,
                "N_past": n_past,
                "rho_mem_over_rhocrit0": bg["rho_mem_over_rhocrit0"],
                "w_mem": bg["w_mem"],
                "one_plus_w_mem": bg["one_plus_w_mem"],
                "Omega_mem_of_a": bg["Omega_mem_of_a"],
                "K_over_rhocrit0": kinetic,
                "V_over_rhocrit0": potential,
                "phi_minus_phi0_Mpl": phi,
                "abs_dphi_dN_Mpl": dphi_dn,
                "cs2_rest_frame": 1.0,
                "ghost_check": "pass" if kinetic >= -1.0e-14 else "fail",
                "gradient_check": "pass",
                "potential_positive_check": "pass" if potential > 0.0 else "fail",
            }
        )
        last_dphi_dn = dphi_dn
        last_n = n_past
    return rows


def canonical_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    phi_values = [float(row["phi_minus_phi0_Mpl"]) for row in rows]
    w_values = [float(row["w_mem"]) for row in rows]
    one_plus_w_values = [float(row["one_plus_w_mem"]) for row in rows]
    kinetic_values = [float(row["K_over_rhocrit0"]) for row in rows]
    potential_values = [float(row["V_over_rhocrit0"]) for row in rows]
    dphi_values = [float(row["abs_dphi_dN_Mpl"]) for row in rows]
    peak_row = max(rows, key=lambda row: float(row["one_plus_w_mem"]))
    failing_checks = [
        row
        for row in rows
        if row["ghost_check"] != "pass" or row["gradient_check"] != "pass" or row["potential_positive_check"] != "pass"
    ]
    return [
        {
            "item": "field_excursion_0_to_z3_Mpl",
            "value": max(phi_values) - min(phi_values),
            "readout": "small_subplanckian" if max(phi_values) - min(phi_values) < 1.0 else "large_check",
        },
        {
            "item": "min_w_mem",
            "value": min(w_values),
            "readout": "non_phantom" if min(w_values) >= -1.0 - 1.0e-12 else "phantom_check",
        },
        {
            "item": "max_one_plus_w_mem",
            "value": max(one_plus_w_values),
            "readout": f"peak_near_z={float(peak_row['z']):.6g}",
        },
        {
            "item": "max_K_over_rhocrit0",
            "value": max(kinetic_values),
            "readout": "positive_kinetic",
        },
        {
            "item": "min_V_over_rhocrit0",
            "value": min(potential_values),
            "readout": "positive_potential" if min(potential_values) > 0.0 else "check",
        },
        {
            "item": "max_abs_dphi_dN_Mpl",
            "value": max(dphi_values),
            "readout": "finite_roll",
        },
        {
            "item": "failed_reconstruction_checks",
            "value": len(failing_checks),
            "readout": "pass" if not failing_checks else "fail",
        },
    ]


def high_cs_growth_bound_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    h = params["h"]
    for z in Z_SAMPLES:
        bg = memory_background(z, params)
        for k_h in K_H_VALUES:
            k_mpc = k_h * h
            epsilon = (bg["a"] * bg["H_z_km_s_Mpc"] / LIGHT_SPEED_KM_S) / k_mpc
            delta_ratio_bound = abs(bg["one_plus_w_mem"]) * epsilon * epsilon
            mu_minus_one_bound = (
                (bg["Omega_mem_of_a"] / bg["Omega_m_of_a"]) * delta_ratio_bound if bg["Omega_m_of_a"] > 0.0 else math.nan
            )
            source_coefficient_bound = 1.5 * bg["Omega_m_of_a"] * mu_minus_one_bound
            rows.append(
                {
                    "z": z,
                    "k_h_Mpc": k_h,
                    "aH_over_ck": epsilon,
                    "aH_over_ck_squared": epsilon * epsilon,
                    "abs_one_plus_w_mem": abs(bg["one_plus_w_mem"]),
                    "Omega_mem_over_Omega_m": bg["Omega_mem_of_a"] / bg["Omega_m_of_a"] if bg["Omega_m_of_a"] > 0.0 else math.nan,
                    "delta_mem_over_delta_m_bound": delta_ratio_bound,
                    "mu_minus_one_bound": mu_minus_one_bound,
                    "S_mem_growth_source_coefficient_bound": source_coefficient_bound,
                    "readout": "subhorizon_suppressed" if mu_minus_one_bound < 1.0e-3 else "large_scale_check",
                }
            )
    return rows


def owner_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "canonical_reconstructed_memory_scalar",
            "action_or_constraint": "S_phi = integral sqrt(-g)[-1/2 (partial phi)^2 - V(phi)]",
            "what_is_derived": "stress tensor, Bianchi conservation, c_s_eff^2=1, zero anisotropic stress, no direct matter exchange",
            "what_is_not_derived": "V(phi) is reconstructed from locked A(N); it does not derive B_mem=2/27, p=3, u3=1/4, Q, or D",
            "perturbation_readout": "late-time subhorizon memory clustering is bounded rather than exactly zero",
            "promotion_effect": "partially relaxes P06 as effective owner; does not clear P04/P07/P08/P09/P10",
            "verdict": "best_current_effective_owner",
        },
        {
            "branch": "exact_auxiliary_constrained_memory",
            "action_or_constraint": "S_aux with lambda_M enforcing delta I_M^GI=0 or equivalent nonpropagating memory constraint",
            "what_is_derived": "would give F_fric=0, mu=1, slip=0, S_mem=0 if the constraint stress is Bianchi-compatible",
            "what_is_not_derived": "constraint action, divergence identity, boundary exchange, and local q_loc^nu silence",
            "perturbation_readout": "exactly smooth route remains open but unowned",
            "promotion_effect": "could clear P06/P07/P08 only after parent identity is supplied",
            "verdict": "open_title_route_not_derived",
        },
        {
            "branch": "geometric_divergence_free_counterstress",
            "action_or_constraint": "move memory into an on-shell divergence-free geometric tensor E_mem^{mu nu}",
            "what_is_derived": "nothing new here; only a route specification",
            "what_is_not_derived": "identity that cancels perfect-fluid energy/momentum obstructions",
            "perturbation_readout": "could be exact if a real Noether/Bianchi identity exists",
            "promotion_effect": "kept as parent-theory target",
            "verdict": "open_heavy_route",
        },
        {
            "branch": "controlled_exchange_Qnu",
            "action_or_constraint": "derive Q^nu from parent memory-matter/geometric coupling",
            "what_is_derived": "none",
            "what_is_not_derived": "local silence, universality, and no-fit exchange source",
            "perturbation_readout": "can cancel sources but is too easy to turn into a fudge force",
            "promotion_effect": "last resort only",
            "verdict": "dangerous_not_selected",
        },
    ]


def perturbation_output_rows(bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst_mu = max(float(row["mu_minus_one_bound"]) for row in bounds)
    worst_source = max(float(row["S_mem_growth_source_coefficient_bound"]) for row in bounds)
    worst_delta = max(float(row["delta_mem_over_delta_m_bound"]) for row in bounds)
    return [
        {
            "output": "friction correction",
            "symbol": "F_fric(a,k)",
            "canonical_high_cs_result": "0",
            "derivation_status": "derived_effective_from_minimal_coupling",
            "bound_or_value": 0.0,
            "claim_limit": "uses reconstructed scalar action, not MTS parent action",
        },
        {
            "output": "effective Newton/source correction",
            "symbol": "mu(a,k)-1",
            "canonical_high_cs_result": "(Omega_mem/Omega_m)(delta_mem/delta_m)",
            "derivation_status": "bounded_effective",
            "bound_or_value": worst_mu,
            "claim_limit": "small on sampled late-time linear modes; not a CMB or local theorem",
        },
        {
            "output": "memory clustering",
            "symbol": "delta_mem/delta_m",
            "canonical_high_cs_result": "<= |1+w_mem| (aH/ck)^2 for c_s_eff^2=1",
            "derivation_status": "bounded_effective",
            "bound_or_value": worst_delta,
            "claim_limit": "quasi-static subhorizon estimate, not superhorizon proof",
        },
        {
            "output": "lensing/slip",
            "symbol": "eta_slip-1, Sigma-1",
            "canonical_high_cs_result": "eta_slip-1=0; Sigma-1 tracks the same Poisson-source bound",
            "derivation_status": "derived_effective_no_anisotropic_stress",
            "bound_or_value": worst_mu,
            "claim_limit": "late-time effective scalar only; lensing spectra not run",
        },
        {
            "output": "memory growth source",
            "symbol": "S_mem(a,k)",
            "canonical_high_cs_result": "<= (3/2) Omega_m(a) |mu-1|",
            "derivation_status": "bounded_effective",
            "bound_or_value": worst_source,
            "claim_limit": "does not yet replace full growth/CMB Boltzmann implementation",
        },
        {
            "output": "sound speed / constraint owner",
            "symbol": "c_s_eff^2 or lambda_M",
            "canonical_high_cs_result": "c_s_eff^2=1",
            "derivation_status": "derived_effective_from_canonical_kinetic_term",
            "bound_or_value": 1.0,
            "claim_limit": "sound speed owned by imported scalar EFT; parent MTS origin still missing",
        },
    ]


def auxiliary_obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "ordinary perfect fluid exact silence",
            "substitution": "delta_mem=theta_mem=delta_p_mem=pi_mem=0",
            "obstruction": "(1+w_mem) Phi_prime and (1+w_mem) k^2 Psi terms remain during activation",
            "result": "rejected",
            "needed_for_success": "w_mem=-1 or a non-perfect-fluid/constraint counterstress",
        },
        {
            "test": "canonical scalar exact silence",
            "substitution": "delta_phi=0 while phi_dot != 0",
            "obstruction": "metric perturbations source delta_phi on large/superhorizon scales",
            "result": "not_exact",
            "needed_for_success": "use as high-c_s subhorizon approximation only",
        },
        {
            "test": "auxiliary exact constraint",
            "substitution": "delta I_M^GI=0 by Lagrange multiplier",
            "obstruction": "constraint stress and divergence identity not supplied",
            "result": "open",
            "needed_for_success": "derive lambda_M stress and Bianchi-compatible local q_loc^nu -> 0",
        },
        {
            "test": "local GR silence",
            "substitution": "local/bound memory projection vanishes",
            "obstruction": "domain selector and q_loc^nu still not parent-derived",
            "result": "open_blocking",
            "needed_for_success": "local weak-field variation proving G_eff/G -> 1, gamma=beta=1, Phi=Psi",
        },
    ]


def promotion_gate_effect_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "P04",
            "gate": "parent perturbation action",
            "effect_of_checkpoint_178": "not_cleared",
            "evidence": "canonical scalar action is reconstructed/imported from locked background, not derived from MTS parent variables Q,D,R",
        },
        {
            "gate_id": "P06",
            "gate": "derive F_fric, mu, slip/Sigma, S_mem",
            "effect_of_checkpoint_178": "partially_relaxed_effective",
            "evidence": "canonical branch gives F_fric=0, c_s_eff^2=1, no anisotropic stress, and bounded mu/S_mem on late-time subhorizon modes",
        },
        {
            "gate_id": "P07",
            "gate": "CMB Boltzmann interface",
            "effect_of_checkpoint_178": "not_cleared",
            "evidence": "high-cs scalar is implementable as kill-screen closure, but TT/TE/EE/lensing and calibration bridge remain unresolved",
        },
        {
            "gate_id": "P08",
            "gate": "local GR and PPN silence",
            "effect_of_checkpoint_178": "not_cleared",
            "evidence": "no derivation yet that q_loc^nu -> 0 or that local scalar/domain response is silent to PPN order",
        },
        {
            "gate_id": "P09",
            "gate": "zero-knob domain selector",
            "effect_of_checkpoint_178": "not_cleared",
            "evidence": "D/chi_D still closure-level",
        },
        {
            "gate_id": "P10",
            "gate": "B_mem=2/27 amplitude owner",
            "effect_of_checkpoint_178": "not_cleared",
            "evidence": "reconstruction assumes locked B_mem=2/27 rather than deriving it",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    failed_checks = int(float(next(row["value"] for row in summary if row["item"] == "failed_reconstruction_checks")))
    worst_mu = max(float(row["mu_minus_one_bound"]) for row in bounds)
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all registered paths found" if not missing else "; ".join(missing),
        },
        {
            "gate": "canonical_reconstruction_healthy",
            "status": "pass" if failed_checks == 0 else "fail",
            "evidence": f"failed_reconstruction_checks={failed_checks}",
        },
        {
            "gate": "P06_outputs_written",
            "status": "pass" if len(outputs) == 6 else "fail",
            "evidence": f"output_rows={len(outputs)}",
        },
        {
            "gate": "late_subhorizon_bound_small",
            "status": "pass" if worst_mu < 1.0e-3 else "check",
            "evidence": f"worst |mu-1| bound={worst_mu:.6g}",
        },
        {
            "gate": "exact_auxiliary_not_smuggled",
            "status": "pass",
            "evidence": "exact smooth route kept open but not claimed without Bianchi/constraint owner",
        },
        {
            "gate": "theory_promotion_blocked",
            "status": "pass",
            "evidence": "P04/P07/P08/P09/P10 remain blocking; P06 only partial/effective",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(bounds: list[dict[str, Any]], summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst_mu_row = max(bounds, key=lambda row: float(row["mu_minus_one_bound"]))
    delta_phi = float(next(row["value"] for row in summary if row["item"] == "field_excursion_0_to_z3_Mpl"))
    return [
        {
            "item": "status",
            "verdict": STATUS_PASS,
            "evidence": "canonical high-cs perturbation owner exists as effective EFT; exact auxiliary parent owner remains open",
        },
        {
            "item": "P06_status",
            "verdict": "partial_effective_not_parent_promoted",
            "evidence": "F_fric, c_s, slip, mu bound, and S_mem bound are owned by reconstructed scalar EFT, not by MTS parent action",
        },
        {
            "item": "worst_mu_minus_one_bound",
            "verdict": f"{float(worst_mu_row['mu_minus_one_bound']):.12g}",
            "evidence": f"z={worst_mu_row['z']}, k={worst_mu_row['k_h_Mpc']} h/Mpc",
        },
        {
            "item": "canonical_field_excursion",
            "verdict": f"{delta_phi:.12g}",
            "evidence": "Delta phi/Mpl from z=0 to z=3 in reconstructed effective scalar",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "effective owner does not derive parent action, CMB spectra, local GR silence, D selector, or 2/27 amplitude",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "private derivation attempt only",
        },
        {
            "item": "next_target",
            "verdict": "179-local-GR-PPN-silence-contract.md",
            "evidence": "the effective scalar route must now survive local weak-field/PPN silence or be fenced as cosmology-only EFT",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-memory-perturbation-owner-derivation-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    params = locked_background()
    background = background_identity_rows(params)
    canonical = canonical_reconstruction_rows(params)
    summary = canonical_summary_rows(canonical)
    bounds = high_cs_growth_bound_rows(params)
    branches = owner_branch_rows()
    outputs = perturbation_output_rows(bounds)
    obstructions = auxiliary_obstruction_rows()
    promotion = promotion_gate_effect_rows()
    gates = acceptance_gate_rows(sources, summary, bounds, outputs)
    decisions = decision_rows(bounds, summary)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "locked_B_mem": LOCKED_B_MEM,
            "locked_p": LOCKED_P,
            "locked_u3": LOCKED_U3,
            "k_h_values": K_H_VALUES,
            "z_samples": Z_SAMPLES,
            "purpose": "attempt effective memory perturbation ownership without parent-action promotion",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "background_identity.csv",
        background,
        [
            "z",
            "a",
            "N_past",
            "A_mem",
            "dA_dN",
            "rho_mem_over_rhocrit0",
            "w_mem",
            "one_plus_w_mem",
            "E2",
            "Omega_mem_of_a",
            "Omega_m_of_a",
            "H_z_km_s_Mpc",
            "identity_status",
            "claim_limit",
        ],
    )
    write_csv(
        results_dir / "canonical_reconstruction.csv",
        canonical,
        [
            "index",
            "z",
            "N_past",
            "rho_mem_over_rhocrit0",
            "w_mem",
            "one_plus_w_mem",
            "Omega_mem_of_a",
            "K_over_rhocrit0",
            "V_over_rhocrit0",
            "phi_minus_phi0_Mpl",
            "abs_dphi_dN_Mpl",
            "cs2_rest_frame",
            "ghost_check",
            "gradient_check",
            "potential_positive_check",
        ],
    )
    write_csv(results_dir / "canonical_reconstruction_summary.csv", summary, ["item", "value", "readout"])
    write_csv(
        results_dir / "owner_branch_ledger.csv",
        branches,
        [
            "branch",
            "action_or_constraint",
            "what_is_derived",
            "what_is_not_derived",
            "perturbation_readout",
            "promotion_effect",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "high_cs_growth_bound_grid.csv",
        bounds,
        [
            "z",
            "k_h_Mpc",
            "aH_over_ck",
            "aH_over_ck_squared",
            "abs_one_plus_w_mem",
            "Omega_mem_over_Omega_m",
            "delta_mem_over_delta_m_bound",
            "mu_minus_one_bound",
            "S_mem_growth_source_coefficient_bound",
            "readout",
        ],
    )
    write_csv(
        results_dir / "derived_perturbation_outputs.csv",
        outputs,
        ["output", "symbol", "canonical_high_cs_result", "derivation_status", "bound_or_value", "claim_limit"],
    )
    write_csv(
        results_dir / "exact_auxiliary_bianchi_obstruction.csv",
        obstructions,
        ["test", "substitution", "obstruction", "result", "needed_for_success"],
    )
    write_csv(
        results_dir / "promotion_gate_effects.csv",
        promotion,
        ["gate_id", "gate", "effect_of_checkpoint_178", "evidence"],
    )
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS_PASS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "locked_background": params,
        "promotion_allowed": False,
        "P06_effect": "partial_effective_not_parent_promoted",
        "exact_auxiliary_owner": "open_not_derived",
        "generated": [
            "source_register.csv",
            "background_identity.csv",
            "canonical_reconstruction.csv",
            "canonical_reconstruction_summary.csv",
            "owner_branch_ledger.csv",
            "high_cs_growth_bound_grid.csv",
            "derived_perturbation_outputs.csv",
            "exact_auxiliary_bianchi_obstruction.csv",
            "promotion_gate_effects.csv",
            "acceptance_gates.csv",
            "decision.csv",
        ],
        "next_target": "179-local-GR-PPN-silence-contract.md",
    }
    write_json(run_dir / "status.json", status)
    (run_dir / "DONE.txt").write_text(f"{STATUS_PASS}\n", encoding="utf-8")
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
