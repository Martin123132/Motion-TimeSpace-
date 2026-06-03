#!/usr/bin/env python3
"""Attempt the post-checkpoint early-time memory decoupling/calibration derivation."""

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
from growth_CMB_first_scoring_run import N_EFF, OMEGA_B_H2, load_background_params, z_star  # noqa: E402
from post_checkpoint_CMB_distance_prior_implementation_audit import cmb_prediction_variant  # noqa: E402


SOURCE_34_STATUS = Path("runs/20260531-003434-CMB-compatible-MTS-limit-contract/status.json")
LOCKED_BRANCH = "MTS_C0_minimal_smooth_memory"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def radiation_density(params: dict[str, float]) -> float:
    h = float(params.get("h0", 70.0)) / 100.0
    omega_gamma = 2.469e-5 / (h * h)
    return omega_gamma * (1.0 + 0.22710731766 * N_EFF)


def activation_diagnostics(z: float, params: dict[str, float]) -> dict[str, float]:
    u_s, nu_act = activation_shape_params(params)
    n_load = math.log1p(z) / u_s
    log_survival = -(n_load**nu_act)
    survival = 0.0 if log_survival < -745.0 else math.exp(log_survival)
    activation = 1.0 - survival
    if z <= 0.0:
        derivative_dz = 0.0 if nu_act > 1.0 else (1.0 / u_s if nu_act == 1.0 else math.inf)
        derivative_dN = 0.0 if nu_act > 1.0 else (1.0 / u_s if nu_act == 1.0 else math.inf)
    else:
        derivative_dN = survival * nu_act * (n_load ** (nu_act - 1.0)) / u_s
        derivative_dz = derivative_dN / (1.0 + z)
    return {
        "z": z,
        "N_ln_1_plus_z": math.log1p(z),
        "u_s": u_s,
        "nu_act": nu_act,
        "N_over_u_s": n_load,
        "F_memory": activation,
        "survival_1_minus_F": survival,
        "log10_survival": log_survival / math.log(10.0),
        "dF_dN": derivative_dN,
        "dF_dz": derivative_dz,
    }


def memory_limit_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    omega_m = float(params["omega_m0"])
    omega_r = radiation_density(params)
    b_mem = float(params.get("b_mem", 0.0))
    zs = z_star(params, OMEGA_B_H2)
    sample_z = [0.0, 0.5, 1.0, 10.0, 100.0, zs, 1.0e4, 1.0e5]
    rows: list[dict[str, Any]] = []
    for z in sample_z:
        diag = activation_diagnostics(z, params)
        zp1 = 1.0 + z
        e2_matter = omega_m * zp1**3
        e2_radiation = omega_r * zp1**4
        e2_lambda = 1.0 - omega_m
        e2_memory = b_mem * diag["F_memory"]
        e2_total = float(e2_array("M6", np.asarray([z]), params)[0] + e2_radiation)
        e2_without_memory = e2_total - e2_memory
        fractional_h2 = abs(e2_memory) / max(abs(e2_without_memory), 1.0e-300)
        rows.append(
            {
                "z": z,
                "N_ln_1_plus_z": diag["N_ln_1_plus_z"],
                "F_memory": diag["F_memory"],
                "survival_1_minus_F": diag["survival_1_minus_F"],
                "log10_survival": diag["log10_survival"],
                "dF_dN": diag["dF_dN"],
                "Omega_mem_E2": e2_memory,
                "Omega_matter_E2": e2_matter,
                "Omega_radiation_E2": e2_radiation,
                "Omega_lambda_E2": e2_lambda,
                "E2_total_with_radiation": e2_total,
                "fractional_memory_in_H2": fractional_h2,
                "fractional_memory_in_H": 0.5 * fractional_h2,
            }
        )
    return rows


def recombination_bound_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    omega_m = float(params["omega_m0"])
    omega_r = radiation_density(params)
    b_mem = float(params.get("b_mem", 0.0))
    zs = z_star(params, OMEGA_B_H2)
    zp1 = 1.0 + zs
    denominator = omega_m * zp1**3 + omega_r * zp1**4 + (1.0 - omega_m)
    exact_diag = activation_diagnostics(zs, params)
    exact_mem = b_mem * exact_diag["F_memory"]
    exact_fraction = abs(exact_mem) / denominator
    worst_fraction = abs(b_mem) / denominator
    return [
        {
            "bound": "exact_recombination_fraction",
            "expression": "|b_mem F(z_star)| / [Omega_m(1+z_star)^3 + Omega_r(1+z_star)^4 + 1-Omega_m]",
            "value": exact_fraction,
            "status": "pass" if exact_fraction < 1.0e-6 else "fail",
            "interpretation": "direct memory contribution to H^2 at recombination is negligible for plasma/source physics",
        },
        {
            "bound": "worst_case_high_z_fraction",
            "expression": "|b_mem| / [Omega_m(1+z_star)^3 + Omega_r(1+z_star)^4 + 1-Omega_m]",
            "value": worst_fraction,
            "status": "pass" if worst_fraction < 1.0e-6 else "fail",
            "interpretation": "even saturated memory is tiny against matter+radiation at z_star",
        },
        {
            "bound": "H_fraction_upper_bound",
            "expression": "delta H/H <= 0.5 delta H^2/H^2",
            "value": 0.5 * worst_fraction,
            "status": "pass" if 0.5 * worst_fraction < 5.0e-7 else "fail",
            "interpretation": "sound-horizon integrand perturbation from direct high-z memory is bounded at sub-ppm size",
        },
        {
            "bound": "activation_source_at_recombination",
            "expression": "b_mem dF/dN at z_star",
            "value": abs(b_mem * exact_diag["dF_dN"]),
            "status": "pass" if abs(b_mem * exact_diag["dF_dN"]) < 1.0e-30 else "warn",
            "interpretation": "transition source has effectively switched off by recombination for the frozen Weibull shape",
        },
    ]


def cmb_integral_sensitivity_rows(params: dict[str, float]) -> list[dict[str, Any]]:
    locked = dict(params)
    no_memory = dict(params)
    no_memory["b_mem"] = 0.0
    locked_prediction = cmb_prediction_variant("M6", locked, "scale_factor_quad", np.inf, True, True)
    no_memory_prediction = cmb_prediction_variant("M6", no_memory, "scale_factor_quad", np.inf, True, True)
    rows: list[dict[str, Any]] = []
    for quantity in ["R", "l_A", "z_star", "r_s_star", "D_M_star"]:
        with_memory = float(locked_prediction[quantity])
        without_memory = float(no_memory_prediction[quantity])
        delta = with_memory - without_memory
        rows.append(
            {
                "quantity": quantity,
                "with_locked_b_mem": with_memory,
                "with_b_mem_zero_same_h0_omega": without_memory,
                "delta": delta,
                "fractional_delta": delta / without_memory if without_memory != 0.0 else "",
                "interpretation": (
                    "line_of_sight_distance_sensitive"
                    if quantity in {"R", "l_A", "D_M_star"}
                    else "early_sound_horizon_or_source_quantity"
                ),
            }
        )
    return rows


def calibration_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "direct_recombination_decoupling",
            "status": "conditionally_passed_for_background_only",
            "derivation": "F(z_star) is saturated and b_mem is constant, but |b_mem| is overwhelmed by matter+radiation in H^2 at z_star",
            "remaining_gap": "does not solve the low-redshift part of D_M(z_star)",
        },
        {
            "route": "absorb_memory_into_matter_or_radiation",
            "status": "rejected_as_exact_identity",
            "derivation": "b_mem F(N) tends to a constant in E^2, not an a^-3 or a^-4 scaling term",
            "remaining_gap": "can be ignored at high z by small fraction, but not exactly redefined as Omega_m or Omega_r",
        },
        {
            "route": "calibrate_H0_Omega_m0_b_mem",
            "status": "closure_only",
            "derivation": "compressed CMB distance priors can be fit by retuning these variables",
            "remaining_gap": "parent map from motion-load variables to calibrated CMB parameters is missing",
        },
        {
            "route": "official_CMB_likelihood",
            "status": "not_implemented",
            "derivation": "current check only treats background distance priors",
            "remaining_gap": "perturbations, lensing, damping tail, and model-dependent priors remain outside this test",
        },
    ]


def gate_rows(source_34: dict[str, Any], bounds: list[dict[str, Any]], sensitivity: list[dict[str, Any]]) -> list[dict[str, Any]]:
    direct_bound = next(row for row in bounds if row["bound"] == "worst_case_high_z_fraction")
    d_m_row = next(row for row in sensitivity if row["quantity"] == "D_M_star")
    return [
        {
            "gate": "source_34_contract_complete",
            "status": "pass" if source_34.get("readout") == "CMB_compatible_MTS_limit_contract_locked_parent_derivation_required" else "fail",
            "detail": str(source_34.get("readout")),
        },
        {
            "gate": "exact_M6_memory_formula_identified",
            "status": "pass",
            "detail": "E2_M6=Omega_m(1+z)^3+1-Omega_m+b_mem[1-exp(-(ln(1+z)/u_s)^nu)]",
        },
        {
            "gate": "direct_recombination_H2_bound",
            "status": "pass" if direct_bound["status"] == "pass" else "fail",
            "detail": f"worst_fraction={direct_bound['value']}",
        },
        {
            "gate": "CMB_line_of_sight_distance_decouples",
            "status": "fail" if abs(float(d_m_row["fractional_delta"])) > 1.0e-8 else "pass",
            "detail": f"D_M fractional delta from b_mem at fixed h0/omega={d_m_row['fractional_delta']}",
        },
        {
            "gate": "parent_calibration_map_derived",
            "status": "fail",
            "detail": "no parent-derived map for H0, Omega_m0, and b_mem across SN/BAO/growth/CMB splits",
        },
        {
            "gate": "CMB_support_claim_allowed",
            "status": "fail",
            "detail": "background high-z decoupling is bounded, but CMB-distance calibration remains closure-only",
        },
        {
            "gate": "C0_death_claim_allowed",
            "status": "fail",
            "detail": "fixed branch is demoted, not a parent-theory death test",
        },
    ]


def decision_rows(bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    worst = next(row for row in bounds if row["bound"] == "worst_case_high_z_fraction")
    return [
        {
            "decision": "early_time_memory_plasma_decoupling",
            "status": "bounded_as_safe_for_background_recombination" if worst["status"] == "pass" else "not_bounded",
            "evidence": f"worst fractional H2 contribution at z_star={worst['value']}",
            "next_action": "do not use direct high-z memory as the CMB failure explanation",
        },
        {
            "decision": "CMB_distance_calibration_status",
            "status": "closure_only_not_support",
            "evidence": "D_M(z_star) still samples late-time expansion, and H0/Omega_m0/b_mem map is not parent-derived",
            "next_action": "derive parent calibration map or keep CMB-calibrated branch secondary",
        },
        {
            "decision": "public_claim_status",
            "status": "forbidden",
            "evidence": "compressed distance-prior and closure-only calibration",
            "next_action": "official likelihood and perturbation closure before public CMB language",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-checkpoint early-time decoupling/calibration derivation attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_34 = load_json(POST_CHECKPOINT / SOURCE_34_STATUS)
    background = load_background_params(MAIN_WORKBENCH)
    entry = background[LOCKED_BRANCH]
    params = {key: float(value) for key, value in entry["params"].items()}

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-early-time-decoupling-or-calibration-derivation"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    memory_limits = memory_limit_rows(params)
    recombination_bounds = recombination_bound_rows(params)
    cmb_sensitivity = cmb_integral_sensitivity_rows(params)
    calibration_contract = calibration_contract_rows()
    gates = gate_rows(source_34, recombination_bounds, cmb_sensitivity)
    decisions = decision_rows(recombination_bounds)

    write_csv(results_dir / "early_time_memory_limit.csv", memory_limits, list(memory_limits[0].keys()))
    write_csv(results_dir / "recombination_memory_bound.csv", recombination_bounds, list(recombination_bounds[0].keys()))
    write_csv(results_dir / "CMB_integral_memory_sensitivity.csv", cmb_sensitivity, list(cmb_sensitivity[0].keys()))
    write_csv(results_dir / "calibration_absorption_contract.csv", calibration_contract, list(calibration_contract[0].keys()))
    write_csv(results_dir / "derivation_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    worst_bound = next(row for row in recombination_bounds if row["bound"] == "worst_case_high_z_fraction")
    dm_row = next(row for row in cmb_sensitivity if row["quantity"] == "D_M_star")
    readout = "early_time_memory_bound_passes_CMB_distance_calibration_remains_closure_only"
    status = {
        "status": "complete_early_time_decoupling_or_calibration_derivation",
        "readout": readout,
        "recommendation": "derive_parent_CMB_calibration_map_or_keep_CMB_branch_secondary_next",
        "next_target": "36-parent-CMB-calibration-map-attempt.md",
        "locked_branch": LOCKED_BRANCH,
        "physics_model": entry["physics_model"],
        "params": params,
        "z_star": z_star(params, OMEGA_B_H2),
        "worst_recombination_fraction_H2": worst_bound["value"],
        "D_M_star_fractional_delta_from_b_mem_fixed_params": dm_row["fractional_delta"],
        "early_time_memory_plasma_decoupling_status": decisions[0]["status"],
        "CMB_distance_calibration_status": decisions[1]["status"],
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "early_time_memory_limit": str(results_dir / "early_time_memory_limit.csv"),
            "recombination_memory_bound": str(results_dir / "recombination_memory_bound.csv"),
            "CMB_integral_memory_sensitivity": str(results_dir / "CMB_integral_memory_sensitivity.csv"),
            "calibration_absorption_contract": str(results_dir / "calibration_absorption_contract.csv"),
            "derivation_gate_criteria": str(results_dir / "derivation_gate_criteria.csv"),
            "decision": str(results_dir / "decision.csv"),
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
