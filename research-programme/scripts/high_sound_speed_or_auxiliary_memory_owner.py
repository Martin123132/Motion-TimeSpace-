#!/usr/bin/env python3
"""Audit high-sound-speed and auxiliary owner routes for memory perturbations."""

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
GROWTH_BACKGROUND = GROWTH_RUN / "results" / "background_params.csv"
STRESS_RUN = RUNS_ROOT / "20260531-185800-memory-stress-perturbation-owner-attempt"
CORRECTION_RUN = RUNS_ROOT / "20260531-191200-subhorizon-suppressed-growth-correction-gate"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
CLAIM_CEILING = "effective_high_sound_speed_owner_not_parent_derivation"


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
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md",
        WORK_DIR / "134-subhorizon-suppressed-growth-correction-gate.md",
        GROWTH_RUN / "status.json",
        GROWTH_BACKGROUND,
        STRESS_RUN / "status.json",
        STRESS_RUN / "results" / "stress_owner_candidates.csv",
        CORRECTION_RUN / "status.json",
        CORRECTION_RUN / "results" / "summary_by_k_and_safety.csv",
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


def canonical_reconstruction_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    omega_m0 = background["Omega_m0"]
    n_max = math.log1p(3.0)
    samples = 700
    rows: list[dict[str, Any]] = []
    phi = 0.0
    last_dphi_dn = 0.0
    last_n = 0.0
    for index in range(samples + 1):
        n_past = n_max * index / samples
        z = math.exp(n_past) - 1.0
        a_mem = activation(n_past)
        da_dn = activation_derivative(n_past)
        rho_mem = 1.0 - omega_m0 + LOCKED_B_MEM * a_mem
        one_plus_w = LOCKED_B_MEM * da_dn / (3.0 * rho_mem)
        w_mem = -1.0 + one_plus_w
        e2 = omega_m0 * math.exp(3.0 * n_past) + rho_mem
        omega_mem_a = rho_mem / e2
        kinetic = 0.5 * rho_mem * one_plus_w
        potential = 0.5 * rho_mem * (1.0 - w_mem)
        dphi_dn = math.sqrt(max(0.0, 3.0 * omega_mem_a * one_plus_w))
        if index > 0:
            delta_n = n_past - last_n
            phi += 0.5 * (last_dphi_dn + dphi_dn) * delta_n
        rows.append(
            {
                "index": index,
                "z": z,
                "N_past": n_past,
                "A_mem": a_mem,
                "rho_mem_over_rhocrit0": rho_mem,
                "w_mem": w_mem,
                "one_plus_w_mem": one_plus_w,
                "Omega_mem_of_a": omega_mem_a,
                "canonical_K_over_rhocrit0": kinetic,
                "canonical_V_over_rhocrit0": potential,
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


def mechanism_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism": "canonical_reconstructed_memory_scalar",
            "action_sketch": "S_mem = integral sqrt(-g)[-1/2 (partial phi)^2 - V(phi)] with V reconstructed from B_mem A(a)",
            "background": "passes_effective_reconstruction",
            "sound_speed_or_constraint": "c_s^2 = 1 from canonical kinetic term",
            "perturbation_status": "subhorizon_suppressed_not_exactly_silent",
            "local_GR_risk": "low_if_only_gravitationally_coupled_but_cosmological_scalar_still_exists",
            "verdict": "best_effective_owner_not_parent_derivation",
        },
        {
            "mechanism": "k_essence_memory_scalar",
            "action_sketch": "S_mem = integral sqrt(-g) P(X,phi_or_I_M)",
            "background": "possible",
            "sound_speed_or_constraint": "c_s^2 = P_X/(P_X+2XP_XX), can be set high but must be derived",
            "perturbation_status": "controllable_if_P_function_parent_derived",
            "local_GR_risk": "medium_new_function_can_become_fudge",
            "verdict": "open_more_flexible_less_clean",
        },
        {
            "mechanism": "auxiliary_constrained_memory",
            "action_sketch": "S_mem plus lambda_M enforcing I_M = I_M[C_coh,Q] with no independent delta I_M",
            "background": "possible",
            "sound_speed_or_constraint": "no propagating scalar; constraint removes delta memory",
            "perturbation_status": "could_be_exact_smooth",
            "local_GR_risk": "depends_on_Bianchi_and_boundary_exchange",
            "verdict": "best_exact_route_not_derived",
        },
        {
            "mechanism": "geometric_divergence_free_counterstress",
            "action_sketch": "move memory to geometric tensor E_mem^mu_nu with nabla_mu E_mem^mu_nu=0 on shell",
            "background": "possible",
            "sound_speed_or_constraint": "no fluid sound speed; geometric identity controls perturbations",
            "perturbation_status": "could_cancel_perfect_fluid_obstruction",
            "local_GR_risk": "high_unless_identity_and_local_limit_derived",
            "verdict": "open_but_heavy",
        },
        {
            "mechanism": "controlled_exchange_Qnu",
            "action_sketch": "derive Q^nu from parent memory-matter coupling",
            "background": "possible",
            "sound_speed_or_constraint": "not a sound speed; exchange cancels source terms",
            "perturbation_status": "dangerous",
            "local_GR_risk": "high_must_prove_Qnu_to_zero_locally",
            "verdict": "last_resort",
        },
    ]


def reconstruction_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    phi_values = [float(row["phi_minus_phi0_Mpl"]) for row in rows]
    w_values = [float(row["w_mem"]) for row in rows]
    one_plus_w_values = [float(row["one_plus_w_mem"]) for row in rows]
    kinetic_values = [float(row["canonical_K_over_rhocrit0"]) for row in rows]
    potential_values = [float(row["canonical_V_over_rhocrit0"]) for row in rows]
    dphi_values = [float(row["abs_dphi_dN_Mpl"]) for row in rows]
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
            "readout": "mild_roll",
        },
        {
            "item": "max_canonical_K_over_rhocrit0",
            "value": max(kinetic_values),
            "readout": "positive_kinetic",
        },
        {
            "item": "min_canonical_V_over_rhocrit0",
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


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_item = {row["item"]: row for row in summary}
    failed_checks = int(float(by_item["failed_reconstruction_checks"]["value"]))
    field_excursion = float(by_item["field_excursion_0_to_z3_Mpl"]["value"])
    return [
        {
            "gate": "canonical_background_reconstruction",
            "status": "pass" if failed_checks == 0 else "fail",
            "evidence": f"failed reconstruction checks={failed_checks}",
        },
        {
            "gate": "high_sound_speed_owner",
            "status": "pass_effective",
            "evidence": "canonical scalar has rest-frame c_s^2=1",
        },
        {
            "gate": "field_excursion_reasonable",
            "status": "pass" if field_excursion < 1.0 else "check",
            "evidence": f"Delta phi/Mpl from z=0 to z=3 is {field_excursion:.6g}",
        },
        {
            "gate": "parent_derivation_of_p_u3_Bmem",
            "status": "fail",
            "evidence": "potential is reconstructed from locked A(a); it does not derive B_mem=2/27, p=3, or u3=1/4",
        },
        {
            "gate": "exact_auxiliary_smoothness",
            "status": "open",
            "evidence": "auxiliary/geometric route could remove scalar mode but Bianchi/boundary owner is not derived",
        },
        {
            "gate": "growth_proxy_status",
            "status": "retained_not_promoted",
            "evidence": "effective high-sound-speed owner explains why checkpoint-130 proxy is safe, not why the parent theory predicts it",
        },
    ]


def decision_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_item = {row["item"]: row for row in summary}
    return [
        {
            "item": "status",
            "verdict": "effective_high_sound_speed_owner_exists_parent_derivation_missing",
            "evidence": f"canonical reconstruction passes with Delta phi/Mpl={float(by_item['field_excursion_0_to_z3_Mpl']['value']):.6g} and c_s^2=1",
        },
        {
            "item": "exact_smooth_route",
            "verdict": "auxiliary_or_geometric_route_open",
            "evidence": "only nonpropagating auxiliary/geometric memory can give exact smoothness through activation",
        },
        {
            "item": "growth_proxy_status",
            "verdict": "effective_EFT_supported_not_fundamental",
            "evidence": "high sound speed justifies late-time subhorizon suppression but does not derive locked amplitude/activation",
        },
        {
            "item": "next_target",
            "verdict": "derive_memory_action_or_lock_as_EFT_closure",
            "evidence": "next step should try to own V(phi)/I_M from S_cell/S_stress rather than merely reconstruct it",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-high-sound-speed-or-auxiliary-memory-owner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    background = locked_background()
    reconstruction = canonical_reconstruction_rows(background)
    mechanisms = mechanism_rows()
    summary = reconstruction_summary_rows(reconstruction)
    gates = gate_rows(summary)
    decisions = decision_rows(summary)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "canonical_reconstruction.csv",
        reconstruction,
        [
            "index",
            "z",
            "N_past",
            "A_mem",
            "rho_mem_over_rhocrit0",
            "w_mem",
            "one_plus_w_mem",
            "Omega_mem_of_a",
            "canonical_K_over_rhocrit0",
            "canonical_V_over_rhocrit0",
            "phi_minus_phi0_Mpl",
            "abs_dphi_dN_Mpl",
            "cs2_rest_frame",
            "ghost_check",
            "gradient_check",
            "potential_positive_check",
        ],
    )
    write_csv(
        results_dir / "mechanism_ledger.csv",
        mechanisms,
        [
            "mechanism",
            "action_sketch",
            "background",
            "sound_speed_or_constraint",
            "perturbation_status",
            "local_GR_risk",
            "verdict",
        ],
    )
    write_csv(results_dir / "reconstruction_summary.csv", summary, ["item", "value", "readout"])
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
            "canonical_reconstruction.csv",
            "mechanism_ledger.csv",
            "reconstruction_summary.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "135-high-sound-speed-or-auxiliary-memory-owner.md",
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
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
