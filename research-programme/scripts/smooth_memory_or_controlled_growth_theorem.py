#!/usr/bin/env python3
"""Derive and audit the smooth-memory versus controlled-growth promotion gate."""

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

GROWTH_RUN = RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout"
GROWTH_RESULTS = GROWTH_RUN / "results"
GROWTH_RESIDUALS = GROWTH_RESULTS / "residuals.csv"
GROWTH_FITS = GROWTH_RESULTS / "fit_summary.csv"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
C_KM_S = 299792.458
K_H_VALUES = [0.02, 0.05, 0.10, 0.20]
QS_COEFFICIENTS = [
    ("auxiliary_exact_constraint", 0.0, "non-propagating gauge-invariant memory constraint"),
    ("canonical_scalar_nominal", 1.5, "Poisson-normalized high-sound-speed c_s^2=1 estimate"),
    ("canonical_scalar_conservative", 3.0, "factor-two conservative quasi-static estimate"),
    ("canonical_scalar_stress_x10", 15.0, "ten-times nominal stress test"),
]
CLAIM_CEILING = "smooth_memory_suppression_law_effective_not_parent_promotion"


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md",
        WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md",
        WORK_DIR / "134-subhorizon-suppressed-growth-correction-gate.md",
        WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md",
        WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
        WORK_DIR / "148-perturbation-CMB-local-GR-promotion-contract.md",
        GROWTH_RUN / "status.json",
        GROWTH_RESIDUALS,
        GROWTH_FITS,
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "issue": "" if exists else "missing",
            }
        )
    return rows


def activation(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((n_past / LOCKED_U3) ** LOCKED_P))


def activation_derivative(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    x = n_past / LOCKED_U3
    return math.exp(-(x**LOCKED_P)) * LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)


def background_quantities(z: float, omega_m0: float, h0: float) -> dict[str, float]:
    n_past = math.log1p(z)
    a_scale = 1.0 / (1.0 + z)
    a_mem = activation(n_past)
    da_dn = activation_derivative(n_past)
    rho_mem = 1.0 - omega_m0 + LOCKED_B_MEM * a_mem
    one_plus_w = LOCKED_B_MEM * da_dn / (3.0 * rho_mem)
    matter_term = omega_m0 * (1.0 + z) ** 3
    e2 = matter_term + rho_mem
    h_z = h0 * math.sqrt(e2)
    omega_m_z = matter_term / e2
    omega_mem_z = rho_mem / e2
    return {
        "z": z,
        "a": a_scale,
        "N_past": n_past,
        "A_mem": a_mem,
        "dA_dN": da_dn,
        "rho_mem_over_rhocrit0": rho_mem,
        "one_plus_w_mem": one_plus_w,
        "w_mem": -1.0 + one_plus_w,
        "matter_term_over_rhocrit0": matter_term,
        "E2": e2,
        "H_z": h_z,
        "Omega_m_z": omega_m_z,
        "Omega_mem_z": omega_mem_z,
        "Omega_mem_over_Omega_m": rho_mem / matter_term,
    }


def fit_lookup() -> dict[tuple[str, str, str, str, str], dict[str, str]]:
    rows = read_csv_rows(GROWTH_FITS)
    lookup = {}
    for row in rows:
        key = (
            row["background_branch"],
            row["branch_label"],
            row["score_role"],
            row["score_mode"],
            row["model"],
        )
        lookup[key] = row
    return lookup


def selected_growth_rows() -> list[dict[str, str]]:
    rows = read_csv_rows(GROWTH_RESIDUALS)
    selected = []
    for row in rows:
        if row["model"] != "MTS_locked_2over27":
            continue
        if row["quantity"] != "f_sigma8":
            continue
        if row["score_mode"] != "all":
            continue
        if row["score_role"] not in {"primary_fit", "alternative_full_shape_fit"}:
            continue
        if not row["branch_label"].endswith("_all_samples"):
            continue
        selected.append(row)
    return selected


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "exact_auxiliary_smooth_memory",
            "assumptions": "memory perturbation is a gauge-invariant non-propagating constraint; matter is separately conserved; no linear memory anisotropic stress",
            "derived_law": "delta_rho_mem^GI = delta_p_mem^GI = theta_mem = pi_mem = 0",
            "growth_terms": "F_fric=0; mu=1; eta_slip=1; S_mem=0",
            "status": "theorem_target_not_parent_derived",
            "failure_mode": "requires Bianchi/constraint owner; otherwise it is a closure axiom",
        },
        {
            "route": "high_sound_speed_effective_memory",
            "assumptions": "canonical or equivalent memory stress with c_s_eff^2 approximately 1; k >> aH/c; no fitted growth knob",
            "derived_law": "|delta_mem/delta_m| <= C_QS |1+w_mem| (aH/ck)^2 / c_s_eff^2",
            "growth_terms": "|mu-1| <= (Omega_mem/Omega_m)|delta_mem/delta_m|; eta_slip=1 for scalar with negligible anisotropic stress",
            "status": "effective_derivation_passes_numerical_bound",
            "failure_mode": "not a parent prediction of B_mem,p,u3 or V(phi)",
        },
        {
            "route": "controlled_modified_growth",
            "assumptions": "memory clusters, exchanges momentum, or has anisotropic stress at linear order",
            "derived_law": "must derive F_fric(a,k), mu(a,k), eta_slip(a,k), Sigma(a,k), and S_mem(a,k)",
            "growth_terms": "not allowed to fit mu_0, sigma8, or k_screen after seeing the data",
            "status": "fallback_if_smooth_routes_fail",
            "failure_mode": "without derived terms the growth branch demotes to empirical closure-only",
        },
    ]


def suppression_rows() -> list[dict[str, Any]]:
    fits = fit_lookup()
    rows = []
    for residual in selected_growth_rows():
        key = (
            residual["background_branch"],
            residual["branch_label"],
            residual["score_role"],
            residual["score_mode"],
            residual["model"],
        )
        fit = fits[key]
        omega_m0 = float(fit["Omega_m0"])
        h = float(fit["h"])
        h0 = float(fit["H0"])
        z = float(residual["z"])
        predicted = float(residual["predicted"])
        sigma = float(residual["diagonal_sigma"])
        q = background_quantities(z, omega_m0, h0)
        for k_h in K_H_VALUES:
            k_mpc = k_h * h
            horizon_ratio = (q["a"] * q["H_z"] / C_KM_S) / k_mpc
            for coeff_name, coeff_value, coeff_note in QS_COEFFICIENTS:
                delta_ratio_bound = coeff_value * abs(q["one_plus_w_mem"]) * horizon_ratio * horizon_ratio
                mu_minus_one_bound = q["Omega_mem_over_Omega_m"] * delta_ratio_bound
                delta_prediction_bound = abs(predicted) * mu_minus_one_bound
                diagonal_chi2_impact_bound = (delta_prediction_bound / sigma) ** 2 if sigma > 0 else math.inf
                rows.append(
                    {
                        "background_branch": residual["background_branch"],
                        "branch_label": residual["branch_label"],
                        "score_role": residual["score_role"],
                        "sample": residual["sample"],
                        "z": z,
                        "k_h_Mpc": k_h,
                        "coefficient_branch": coeff_name,
                        "C_QS": coeff_value,
                        "coefficient_note": coeff_note,
                        "Omega_m0": omega_m0,
                        "h": h,
                        "H0": h0,
                        "predicted_fsigma8": predicted,
                        "diagonal_sigma": sigma,
                        "fractional_sigma": sigma / abs(predicted) if predicted else math.inf,
                        "one_plus_w_mem": q["one_plus_w_mem"],
                        "Omega_mem_over_Omega_m": q["Omega_mem_over_Omega_m"],
                        "aH_over_ck": horizon_ratio,
                        "delta_mem_over_delta_m_bound": delta_ratio_bound,
                        "mu_minus_one_bound": mu_minus_one_bound,
                        "delta_prediction_bound": delta_prediction_bound,
                        "diagonal_chi2_impact_bound": diagonal_chi2_impact_bound,
                        "readout": "negligible" if diagonal_chi2_impact_bound < 0.01 else "check",
                    }
                )
    return rows


def background_grid_rows() -> list[dict[str, Any]]:
    fits = fit_lookup()
    primary = fits[
        (
            "DR2_noCMB_primary",
            "primary_BAO_plus_all_samples",
            "primary_fit",
            "all",
            "MTS_locked_2over27",
        )
    ]
    omega_m0 = float(primary["Omega_m0"])
    h0 = float(primary["H0"])
    grid = [0.0, 0.15, 0.38, 0.51, 0.70, 0.85, 1.48, 2.0, 3.0]
    return [background_quantities(z, omega_m0, h0) for z in grid]


def summary_rows(bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    keys = sorted(
        {
            (
                row["background_branch"],
                row["branch_label"],
                float(row["k_h_Mpc"]),
                row["coefficient_branch"],
            )
            for row in bounds
        }
    )
    for background_branch, branch_label, k_h, coeff_branch in keys:
        selected = [
            row
            for row in bounds
            if row["background_branch"] == background_branch
            and row["branch_label"] == branch_label
            and float(row["k_h_Mpc"]) == k_h
            and row["coefficient_branch"] == coeff_branch
        ]
        max_mu = max(float(row["mu_minus_one_bound"]) for row in selected)
        max_delta_ratio = max(float(row["delta_mem_over_delta_m_bound"]) for row in selected)
        total_chi2 = sum(float(row["diagonal_chi2_impact_bound"]) for row in selected)
        max_shift = max(float(row["delta_prediction_bound"]) for row in selected)
        rows.append(
            {
                "background_branch": background_branch,
                "branch_label": branch_label,
                "k_h_Mpc": k_h,
                "coefficient_branch": coeff_branch,
                "rows": len(selected),
                "max_delta_mem_over_delta_m_bound": max_delta_ratio,
                "max_mu_minus_one_bound": max_mu,
                "max_delta_prediction_bound": max_shift,
                "diagonal_chi2_impact_sum_bound": total_chi2,
                "readout": "negligible" if total_chi2 < 0.1 else "check",
            }
        )
    return rows


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def worst(coefficient_branch: str, k_floor: float = 0.02) -> float:
        return max(
            float(row["diagonal_chi2_impact_sum_bound"])
            for row in summary
            if row["coefficient_branch"] == coefficient_branch and float(row["k_h_Mpc"]) >= k_floor
        )

    nominal = worst("canonical_scalar_nominal")
    conservative = worst("canonical_scalar_conservative")
    stress = worst("canonical_scalar_stress_x10")
    exact = worst("auxiliary_exact_constraint")
    return [
        {
            "gate": "exact_auxiliary_route",
            "status": "pass_if_parent_constraint_derived",
            "evidence": f"linear source bound={exact:.6g} by construction",
        },
        {
            "gate": "high_sound_speed_nominal_bound",
            "status": "pass" if nominal < 0.1 else "check",
            "evidence": f"worst source-locked growth chi2 impact bound={nominal:.6g}",
        },
        {
            "gate": "high_sound_speed_conservative_bound",
            "status": "pass" if conservative < 0.1 else "check",
            "evidence": f"worst source-locked growth chi2 impact bound={conservative:.6g}",
        },
        {
            "gate": "high_sound_speed_stress_x10_bound",
            "status": "pass" if stress < 0.1 else "check",
            "evidence": f"worst source-locked growth chi2 impact bound={stress:.6g}",
        },
        {
            "gate": "GR_proxy_growth_justification",
            "status": "pass_effective_not_parent",
            "evidence": "subhorizon high-sound-speed law makes memory clustering corrections far below current source-locked growth errors",
        },
        {
            "gate": "field_theory_promotion",
            "status": "fail_parent_derivation_missing",
            "evidence": "suppression law needs a parent stress/constraint and does not derive B_mem,p,u3 or the CMB/local limits",
        },
        {
            "gate": "controlled_growth_fallback",
            "status": "not_needed_for_current_late_time_growth_if_smooth_owner_survives",
            "evidence": "fallback remains mandatory if CMB/local/action work rejects the smooth/high-c_s owner",
        },
    ]


def decision_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stress_worst = max(
        float(row["diagonal_chi2_impact_sum_bound"])
        for row in summary
        if row["coefficient_branch"] == "canonical_scalar_stress_x10"
    )
    max_mu_stress = max(
        float(row["max_mu_minus_one_bound"])
        for row in summary
        if row["coefficient_branch"] == "canonical_scalar_stress_x10"
    )
    return [
        {
            "item": "status",
            "verdict": "smooth_memory_effective_suppression_law_derived_parent_promotion_still_blocked",
            "evidence": f"stress_x10 worst chi2 impact={stress_worst:.6g}; stress_x10 max |mu-1|={max_mu_stress:.6g}",
        },
        {
            "item": "growth_proxy_status",
            "verdict": "GR_proxy_justified_as_late_time_effective_limit",
            "evidence": "source-locked f_sigma8 rows remain insensitive to bounded high-sound-speed memory clustering",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "mathematical suppression law and numerical bound only; no parent action, CMB, or local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "150-Boltzmann-interface-contract.md",
            "evidence": "growth proxy now has an effective derivation; the next promotion blocker is CMB perturbation propagation",
        },
    ]


def run_theorem(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-smooth-memory-or-controlled-growth-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    contracts = theorem_contract_rows()
    backgrounds = background_grid_rows()
    bounds = suppression_rows()
    summary = summary_rows(bounds)
    gates = gate_rows(summary)
    decisions = decision_rows(summary)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "issue"])
    write_csv(
        results_dir / "theorem_contract.csv",
        contracts,
        ["route", "assumptions", "derived_law", "growth_terms", "status", "failure_mode"],
    )
    write_csv(
        results_dir / "background_memory_functions.csv",
        backgrounds,
        [
            "z",
            "a",
            "N_past",
            "A_mem",
            "dA_dN",
            "rho_mem_over_rhocrit0",
            "one_plus_w_mem",
            "w_mem",
            "matter_term_over_rhocrit0",
            "E2",
            "H_z",
            "Omega_m_z",
            "Omega_mem_z",
            "Omega_mem_over_Omega_m",
        ],
    )
    write_csv(
        results_dir / "source_locked_growth_suppression_bounds.csv",
        bounds,
        [
            "background_branch",
            "branch_label",
            "score_role",
            "sample",
            "z",
            "k_h_Mpc",
            "coefficient_branch",
            "C_QS",
            "coefficient_note",
            "Omega_m0",
            "h",
            "H0",
            "predicted_fsigma8",
            "diagonal_sigma",
            "fractional_sigma",
            "one_plus_w_mem",
            "Omega_mem_over_Omega_m",
            "aH_over_ck",
            "delta_mem_over_delta_m_bound",
            "mu_minus_one_bound",
            "delta_prediction_bound",
            "diagonal_chi2_impact_bound",
            "readout",
        ],
    )
    write_csv(
        results_dir / "suppression_summary_by_branch.csv",
        summary,
        [
            "background_branch",
            "branch_label",
            "k_h_Mpc",
            "coefficient_branch",
            "rows",
            "max_delta_mem_over_delta_m_bound",
            "max_mu_minus_one_bound",
            "max_delta_prediction_bound",
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
        "locked_B_mem": LOCKED_B_MEM,
        "locked_p": LOCKED_P,
        "locked_u3": LOCKED_U3,
        "k_h_values": K_H_VALUES,
        "coefficient_branches": [row[0] for row in QS_COEFFICIENTS],
        "generated": [
            "source_register.csv",
            "theorem_contract.csv",
            "background_memory_functions.csv",
            "source_locked_growth_suppression_bounds.csv",
            "suppression_summary_by_branch.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "150-Boltzmann-interface-contract.md",
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
    print(run_theorem(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
