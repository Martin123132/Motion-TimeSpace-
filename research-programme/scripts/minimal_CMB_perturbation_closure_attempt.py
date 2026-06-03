#!/usr/bin/env python3
"""Attempt the minimal perturbation closure needed before official CMB support."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_likelihood_smoke import activation_shape_params, e2_array  # noqa: E402


SOURCE_PATHS = {
    "35_status": Path("runs/20260531-004152-early-time-decoupling-or-calibration-derivation/status.json"),
    "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
    "43_status": Path("runs/20260531-012227-official-CMB-perturbation-contract/status.json"),
    "43_perturbation_contract": Path(
        "runs/20260531-012227-official-CMB-perturbation-contract/results/"
        "perturbation_variable_contract.csv"
    ),
    "43_pass_fail_gates": Path(
        "runs/20260531-012227-official-CMB-perturbation-contract/results/"
        "official_CMB_pass_fail_gates.csv"
    ),
}

N_EFF = 3.046
Z_STAR = 1091.5182931260854


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def read_csv(key: str) -> list[dict[str, str]]:
    with absolute_source(key).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def radiation_density(params: dict[str, float]) -> float:
    h = float(params.get("h0", 70.0)) / 100.0
    omega_gamma = 2.469e-5 / (h * h)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation_and_derivative(z: float, params: dict[str, float]) -> tuple[float, float]:
    u_s, nu_act = activation_shape_params(params)
    if z <= 0.0:
        return 0.0, 0.0 if nu_act > 1.0 else (1.0 / u_s if nu_act == 1.0 else math.inf)
    load = math.log1p(z) / u_s
    survival = math.exp(-(load**nu_act)) if load**nu_act < 745.0 else 0.0
    activation = 1.0 - survival
    derivative_dN = survival * nu_act * (load ** (nu_act - 1.0)) / u_s
    return activation, derivative_dN


def dark_sector_quantities(z: float, params: dict[str, float]) -> dict[str, float]:
    omega_m = float(params["omega_m0"])
    omega_r = radiation_density(params)
    b_mem = float(params["b_mem"])
    activation, derivative_dN = activation_and_derivative(z, params)
    omega_lambda = 1.0 - omega_m
    rho_x_e2 = omega_lambda + b_mem * activation
    d_rho_x_dN = b_mem * derivative_dN
    w_x = -1.0 + d_rho_x_dN / (3.0 * rho_x_e2) if rho_x_e2 > 0.0 else math.nan
    e2_no_radiation = float(e2_array("M6", np.asarray([z], dtype=float), params)[0])
    e2_total = e2_no_radiation + omega_r * (1.0 + z) ** 4
    omega_x_fraction = rho_x_e2 / e2_total if e2_total > 0.0 else math.nan
    kinetic_e2 = 0.5 * (1.0 + w_x) * rho_x_e2
    potential_e2 = 0.5 * (1.0 - w_x) * rho_x_e2
    scalar_integrand = math.sqrt(max(0.0, 3.0 * omega_x_fraction * (1.0 + w_x)))
    return {
        "z": z,
        "N_ln_1_plus_z": math.log1p(z),
        "F": activation,
        "dF_dN": derivative_dN,
        "rho_X_E2": rho_x_e2,
        "d_rho_X_dN": d_rho_x_dN,
        "w_X": w_x,
        "one_plus_w_X": 1.0 + w_x,
        "Omega_X_fraction_with_radiation": omega_x_fraction,
        "E2_total_with_radiation": e2_total,
        "K_scalar_E2_proxy": kinetic_e2,
        "V_scalar_E2_proxy": potential_e2,
        "dphi_dln_a_over_Mpl_abs_proxy": scalar_integrand,
    }


def background_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    sample_z = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, Z_STAR, 1.0e4]
    return [dark_sector_quantities(z, params) for z in sample_z]


def scalar_reconstruction_summary(params: dict[str, float]) -> list[dict[str, Any]]:
    n_grid = np.linspace(0.0, math.log1p(Z_STAR), 4096)
    z_grid = np.expm1(n_grid)
    rows = [dark_sector_quantities(float(z), params) for z in z_grid]
    one_plus_w = np.asarray([row["one_plus_w_X"] for row in rows], dtype=float)
    w_values = np.asarray([row["w_X"] for row in rows], dtype=float)
    omega_x = np.asarray([row["Omega_X_fraction_with_radiation"] for row in rows], dtype=float)
    scalar_integrand = np.asarray([row["dphi_dln_a_over_Mpl_abs_proxy"] for row in rows], dtype=float)
    delta_phi = float(np.trapezoid(scalar_integrand, n_grid))
    max_index = int(np.nanargmax(w_values))
    z_at_max_w = float(z_grid[max_index])
    return [
        {
            "quantity": "min_one_plus_w_X",
            "value": float(np.nanmin(one_plus_w)),
            "status": "pass_canonical_proxy" if float(np.nanmin(one_plus_w)) >= -1.0e-10 else "phantom_crossing",
            "interpretation": "canonical scalar reconstruction requires w_X >= -1",
        },
        {
            "quantity": "max_w_X",
            "value": float(np.nanmax(w_values)),
            "status": "diagnostic",
            "interpretation": f"maximum occurs near z={z_at_max_w:.6g}",
        },
        {
            "quantity": "w_X_at_recombination",
            "value": dark_sector_quantities(Z_STAR, params)["w_X"],
            "status": "near_minus_one",
            "interpretation": "direct recombination source is effectively frozen",
        },
        {
            "quantity": "Omega_X_fraction_at_recombination",
            "value": dark_sector_quantities(Z_STAR, params)["Omega_X_fraction_with_radiation"],
            "status": "small_background_fraction",
            "interpretation": "dark/memory sector is dynamically tiny for primary plasma physics",
        },
        {
            "quantity": "max_Omega_X_fraction_to_recombination",
            "value": float(np.nanmax(omega_x)),
            "status": "late_time_dominant_as_expected",
            "interpretation": "large value occurs at low redshift, so ISW/lensing still need perturbations",
        },
        {
            "quantity": "delta_phi_0_to_zstar_over_Mpl_proxy",
            "value": delta_phi,
            "status": "reconstructable_effective_scalar_proxy",
            "interpretation": "mathematical GR-scalar representation exists if imported as an effective closure",
        },
    ]


def closure_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "homogeneous_smooth_memory",
            "definition": "set delta_X=theta_X=sigma_X=0 while using rho_X(a)=1-Omega_m+b_mem F(N)",
            "mathematical_status": "phenomenological_smooth_DE_limit",
            "parent_status": "not_derived",
            "CMB_use": "background_only_kill_screen_or_rough_smooth_limit",
            "support_claim_allowed": False,
            "failure_mode": "not a gauge-complete perturbation theory unless a parent constraint suppresses perturbations",
        },
        {
            "candidate": "GR_effective_scalar_fluid",
            "definition": "define w_X(a) from background conservation; use c_s^2=1, sigma_X=0, Phi=Psi under GR constraints",
            "mathematical_status": "well_posed_borrowed_effective_field_closure_if_w_X_ge_minus_one",
            "parent_status": "not_derived_from_MTS_parent_action",
            "CMB_use": "official_background_plus_borrowed_perturbation_kill_screen",
            "support_claim_allowed": False,
            "failure_mode": "success would show compatibility with an imported scalar-fluid closure, not MTS derivation",
        },
        {
            "candidate": "parent_memory_field",
            "definition": "derive delta Gamma_eff, delta q_mem, constraints, conservation, and lensing from parent action",
            "mathematical_status": "required_for_support_capable_CMB",
            "parent_status": "missing",
            "CMB_use": "not_runnable_yet",
            "support_claim_allowed": False,
            "failure_mode": "without this, official spectra/lensing cannot crown the branch",
        },
    ]


def perturbation_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "background_effective_dark_sector",
            "equation": "rho_X/H0^2 = 1 - Omega_m0 + b_mem F(N), N=ln(1+z)",
            "status": "derived_from_M6_background_definition",
            "claim_limit": "background_only",
        },
        {
            "sector": "background_conservation",
            "equation": "w_X(N) = -1 + [b_mem dF/dN] / [3(1 - Omega_m0 + b_mem F)]",
            "status": "derived_if_X_is_separately_conserved",
            "claim_limit": "conditional_effective_fluid_identity",
        },
        {
            "sector": "scalar_reconstruction",
            "equation": "K/(3 Mpl^2 H0^2)=0.5(1+w_X)rho_X/H0^2; V/(3 Mpl^2 H0^2)=0.5(1-w_X)rho_X/H0^2",
            "status": "available_if_w_X_ge_minus_one",
            "claim_limit": "borrowed_GR_scalar_representation",
        },
        {
            "sector": "metric_constraints",
            "equation": "k^2 Phi + 3H(Phi'+H Psi) = -4 pi G a^2 delta rho_total",
            "status": "borrowed_from_GR_not_MTS_parent_derived",
            "claim_limit": "kill_screen_only",
        },
        {
            "sector": "slip_lensing",
            "equation": "Phi-Psi = 8 pi G a^2 sigma_total/k^2; scalar-fluid closure sets sigma_X=0",
            "status": "borrowed_from_GR_not_MTS_parent_derived",
            "claim_limit": "cannot support MTS lensing without parent derivation",
        },
        {
            "sector": "fluid_perturbations",
            "equation": "delta_X', theta_X' use w_X(a), c_s^2=1, sigma_X=0 in rest-frame fluid equations",
            "status": "standard_effective_dark_energy_closure",
            "claim_limit": "not parent-derived",
        },
        {
            "sector": "initial_conditions",
            "equation": "early delta_X and theta_X are suppressed because Omega_X(1+w_X) is tiny at z_star",
            "status": "bounded_as_initial_approximation_not_parent_theorem",
            "claim_limit": "needs parent superhorizon mode proof",
        },
    ]


def consistency_gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    min_one_plus_w = next(row for row in summary if row["quantity"] == "min_one_plus_w_X")
    omega_rec = next(row for row in summary if row["quantity"] == "Omega_X_fraction_at_recombination")
    scalar_ok = min_one_plus_w["status"] == "pass_canonical_proxy"
    early_small = float(omega_rec["value"]) < 1.0e-6
    return [
        {
            "gate": "effective_background_conservation_identity",
            "status": "pass_conditional",
            "detail": "w_X(N) can be defined exactly from rho_X(N) if the effective dark sector is separately conserved",
        },
        {
            "gate": "canonical_scalar_proxy_exists",
            "status": "pass_conditional" if scalar_ok else "fail",
            "detail": f"min(1+w_X)={min_one_plus_w['value']}",
        },
        {
            "gate": "early_dark_sector_fraction_small",
            "status": "pass" if early_small else "fail",
            "detail": f"Omega_X(z_star)={omega_rec['value']}",
        },
        {
            "gate": "metric_lensing_parent_derivation",
            "status": "fail",
            "detail": "Phi/Psi constraints and lensing response are still GR-imported unless parent action supplies them",
        },
        {
            "gate": "official_CMB_support_run_ready",
            "status": "fail",
            "detail": "minimal closure is a borrowed effective-fluid route, not a parent MTS perturbation derivation",
        },
        {
            "gate": "official_CMB_kill_screen_possible",
            "status": "pass_conditional",
            "detail": "a fixed-row GR effective scalar-fluid implementation could be used as a non-support failure screen",
        },
    ]


def implementation_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "baseline_reproduction",
            "implementation": "install/use official Boltzmann+likelihood stack and reproduce a reference LambdaCDM spectra likelihood",
            "claim_status": "pipeline_validation_only",
            "blocked_by": "tooling/config not yet installed in this sandbox branch",
        },
        {
            "step": "effective_fluid_background",
            "implementation": "feed H(a), w_X(a), c_s^2=1, sigma_X=0 with checkpoint-38 frozen values",
            "claim_status": "borrowed_closure_kill_screen",
            "blocked_by": "requires a CLASS/CAMB/Cobaya implementation choice",
        },
        {
            "step": "parent_perturbation_replacement",
            "implementation": "replace GR effective-fluid equations with parent-derived delta Gamma_eff/delta q_mem closure",
            "claim_status": "support_capable_only_if_derived",
            "blocked_by": "parent action and constraint equations missing",
        },
        {
            "step": "no_rescue_outputs",
            "implementation": "write configs, parameter freeze manifest, chi2 bands, log.txt, status.json, DONE.txt",
            "claim_status": "required_for_any_interpretation",
            "blocked_by": "none; workflow already specified",
        },
    ]


def decision_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    min_one_plus_w = next(row for row in summary if row["quantity"] == "min_one_plus_w_X")
    return [
        {
            "decision": "minimal_CMB_perturbation_closure",
            "status": "conditional_effective_fluid_closure_found_not_parent_derivation",
            "evidence": f"w_X stays non-phantom in the frozen row: min(1+w_X)={min_one_plus_w['value']}",
            "next_action": "treat official CMB with this closure as kill-screen only unless parent equations are derived",
        },
        {
            "decision": "support_capable_official_CMB",
            "status": "not_ready",
            "evidence": "metric constraints, memory perturbations, conservation exchange, and lensing response remain parent-missing",
            "next_action": "attempt parent scalar/action reconstruction or keep official CMB as background-only stress",
        },
        {
            "decision": "recommended_next_target",
            "status": "45-memory-scalar-reconstruction-gate.md",
            "evidence": "the background admits a canonical scalar proxy, which is the narrowest action-like route to test next",
            "next_action": "try to reconstruct a parent-compatible scalar/action; if it is only imported quintessence, label it closure",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal CMB perturbation closure attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json("38_status")
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-minimal-CMB-perturbation-closure-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    background = background_rows(params)
    summary = scalar_reconstruction_summary(params)
    candidates = closure_candidate_rows()
    equations = perturbation_equation_rows()
    gates = consistency_gate_rows(summary)
    manifest = implementation_manifest_rows()
    decisions = decision_rows(summary)

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "effective_dark_sector_background.csv", background, list(background[0].keys()))
    write_csv(results_dir / "scalar_reconstruction_summary.csv", summary, list(summary[0].keys()))
    write_csv(results_dir / "perturbation_closure_candidates.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "perturbation_equation_contract.csv", equations, list(equations[0].keys()))
    write_csv(results_dir / "minimal_closure_consistency_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "official_CMB_implementation_manifest.csv", manifest, list(manifest[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    summary_lookup = {row["quantity"]: row["value"] for row in summary}
    status = {
        "status": "complete_minimal_CMB_perturbation_closure_attempt",
        "readout": "conditional_effective_fluid_closure_found_parent_perturbation_derivation_still_missing",
        "recommendation": "attempt_memory_scalar_reconstruction_gate_next",
        "next_target": "45-memory-scalar-reconstruction-gate.md",
        "frozen_branch": source_38["frozen_branch"],
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "official_CMB_support_run_ready": False,
        "official_CMB_kill_screen_possible": True,
        "key_metrics": {
            "min_one_plus_w_X": summary_lookup["min_one_plus_w_X"],
            "max_w_X": summary_lookup["max_w_X"],
            "w_X_at_recombination": summary_lookup["w_X_at_recombination"],
            "Omega_X_fraction_at_recombination": summary_lookup["Omega_X_fraction_at_recombination"],
            "delta_phi_0_to_zstar_over_Mpl_proxy": summary_lookup["delta_phi_0_to_zstar_over_Mpl_proxy"],
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "effective_dark_sector_background": str(results_dir / "effective_dark_sector_background.csv"),
            "scalar_reconstruction_summary": str(results_dir / "scalar_reconstruction_summary.csv"),
            "perturbation_closure_candidates": str(results_dir / "perturbation_closure_candidates.csv"),
            "perturbation_equation_contract": str(results_dir / "perturbation_equation_contract.csv"),
            "minimal_closure_consistency_gates": str(results_dir / "minimal_closure_consistency_gates.csv"),
            "official_CMB_implementation_manifest": str(results_dir / "official_CMB_implementation_manifest.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
