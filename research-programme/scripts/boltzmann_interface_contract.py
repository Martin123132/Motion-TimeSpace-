#!/usr/bin/env python3
"""Define the Boltzmann/CMB interface contract for the locked MTS memory branch."""

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

TRANSFER_RUN = RUNS_ROOT / "20260531-162146-locked-2over27-late-CMB-transfer-score"
TRANSFER_RESULTS = TRANSFER_RUN / "results"
TRANSFER_PROFILE = TRANSFER_RESULTS / "transfer_profile.csv"

RED_TEAM_RUN = RUNS_ROOT / "20260531-165759-joint-calibration-red-team"
RED_TEAM_RESULTS = RED_TEAM_RUN / "results"
RED_TEAM_DECISION = RED_TEAM_RESULTS / "decision.csv"
RED_TEAM_GATE_FAILURE = RED_TEAM_RESULTS / "gate_failure_audit.csv"

GROWTH_RUN = RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout"
GROWTH_FITS = GROWTH_RUN / "results" / "fit_summary.csv"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.469e-5
NEUTRINO_FACTOR = 0.22710731766
CLAIM_CEILING = "Boltzmann_interface_contract_only_no_CMB_support_claim"


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
        WORK_DIR / "43-official-CMB-perturbation-contract.md",
        WORK_DIR / "44-minimal-CMB-perturbation-closure-attempt.md",
        WORK_DIR / "117-locked-2over27-late-CMB-transfer-gate.md",
        WORK_DIR / "120-joint-calibration-red-team-and-repair-options.md",
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "149-smooth-memory-or-controlled-growth-theorem.md",
        TRANSFER_RUN / "status.json",
        TRANSFER_PROFILE,
        RED_TEAM_RUN / "status.json",
        RED_TEAM_DECISION,
        RED_TEAM_GATE_FAILURE,
        GROWTH_RUN / "status.json",
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
    x = n_past / LOCKED_U3
    if x**LOCKED_P > 745.0:
        return 1.0
    return 1.0 - math.exp(-(x**LOCKED_P))


def activation_derivative(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    x = n_past / LOCKED_U3
    exponent = x**LOCKED_P
    if exponent > 745.0:
        return 0.0
    return math.exp(-exponent) * LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)


def omega_radiation(h: float) -> float:
    return OMEGA_GAMMA_H2 * (1.0 + NEUTRINO_FACTOR * N_EFF) / (h * h)


def memory_rho(z: float, omega_m0: float) -> float:
    return 1.0 - omega_m0 + LOCKED_B_MEM * activation(math.log1p(z))


def one_plus_w_mem(z: float, omega_m0: float) -> float:
    n_past = math.log1p(z)
    rho = memory_rho(z, omega_m0)
    return LOCKED_B_MEM * activation_derivative(n_past) / (3.0 * rho) if rho > 0.0 else math.nan


def w_mem_from_lna(lna: float, omega_m0: float) -> float:
    z = math.exp(-lna) - 1.0
    return -1.0 + one_plus_w_mem(z, omega_m0)


def dw_dln_a(z: float, omega_m0: float) -> float:
    lna = -math.log1p(z)
    step = 1.0e-4
    if lna + step > 0.0:
        w0 = w_mem_from_lna(lna, omega_m0)
        wm = w_mem_from_lna(lna - step, omega_m0)
        return (w0 - wm) / step
    wp = w_mem_from_lna(lna + step, omega_m0)
    wm = w_mem_from_lna(lna - step, omega_m0)
    return (wp - wm) / (2.0 * step)


def background_quantities(z: float, omega_m0: float, h: float) -> dict[str, Any]:
    n_past = math.log1p(z)
    rho_mem = memory_rho(z, omega_m0)
    one_plus_w = one_plus_w_mem(z, omega_m0)
    w_mem = -1.0 + one_plus_w
    omega_r0 = omega_radiation(h)
    matter = omega_m0 * (1.0 + z) ** 3
    radiation = omega_r0 * (1.0 + z) ** 4
    e2_no_radiation = matter + rho_mem
    e2_with_radiation = matter + radiation + rho_mem
    w_prime = dw_dln_a(z, omega_m0)
    if abs(one_plus_w) > 1.0e-8:
        ca2 = w_mem - w_prime / (3.0 * one_plus_w)
        ca2_status = "finite"
    else:
        ca2 = ""
        ca2_status = "singular_or_frozen_limit_use_scalar_or_PPF_closure"
    return {
        "z": z,
        "a": 1.0 / (1.0 + z),
        "N_past_ln_1_plus_z": n_past,
        "A_mem": activation(n_past),
        "dA_dN_past": activation_derivative(n_past),
        "rho_mem_over_rhocrit0": rho_mem,
        "one_plus_w_mem": one_plus_w,
        "w_mem": w_mem,
        "dw_dln_a": w_prime,
        "c_a2_adiabatic": ca2,
        "c_a2_status": ca2_status,
        "Omega_r0_approx": omega_r0,
        "matter_E2": matter,
        "radiation_E2": radiation,
        "E2_no_radiation": e2_no_radiation,
        "E2_with_radiation": e2_with_radiation,
        "Omega_mem_fraction_no_radiation": rho_mem / e2_no_radiation,
        "Omega_mem_fraction_with_radiation": rho_mem / e2_with_radiation,
        "primary_CMB_relevance": "late_ISW_lensing_epoch" if z < 10.0 else "primary_plasma_negligible_memory_fraction",
    }


def primary_transfer_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv_rows(TRANSFER_PROFILE)
        if row["branch"] == "T1_primary_fullcov_DR2" and row["role"] == "primary"
    ]


def transfer_reference_row() -> dict[str, str]:
    rows = primary_transfer_rows()
    strict = [
        row
        for row in rows
        if row["prior_table"] == "wCDM" and row["score_mode"] == "strict_full4"
    ]
    return strict[0] if strict else rows[0]


def growth_reference_row() -> dict[str, str]:
    rows = read_csv_rows(GROWTH_FITS)
    for row in rows:
        if (
            row["background_branch"] == "DR2_noCMB_primary"
            and row["branch_label"] == "primary_BAO_plus_all_samples"
            and row["score_role"] == "primary_fit"
            and row["score_mode"] == "all"
            and row["model"] == "MTS_locked_2over27"
        ):
            return row
    raise ValueError("missing DR2 source-locked growth reference row")


def interface_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "mode": "exact_auxiliary_smooth_memory",
            "background": "rho_mem(a) supplied by locked branch",
            "perturbation_rule": "delta_mem^GI=theta_mem=delta_p_mem^GI=pi_mem=0",
            "rest_frame_sound_speed": "not_applicable_constraint",
            "anisotropic_stress": "0",
            "implementation_path": "custom dark-sector module or PPF-like frozen perturbation source",
            "support_status": "clean_if_parent_constraint_derived",
            "promotion_blocker": "needs parent Bianchi/constraint owner; otherwise closure axiom",
        },
        {
            "mode": "high_sound_speed_effective_scalar",
            "background": "w_mem(a) from conservation; rho_mem(a) fixed",
            "perturbation_rule": "standard scalar/effective-fluid perturbations with c_s_eff^2=1 and sigma=0",
            "rest_frame_sound_speed": "1",
            "anisotropic_stress": "0",
            "implementation_path": "effective scalar/PPF closure; avoid naive fluid singularities where 1+w -> 0",
            "support_status": "kill_screen_implementable_not_parent_support",
            "promotion_blocker": "scalar is reconstructed/effective and does not derive B_mem,p,u3",
        },
        {
            "mode": "controlled_modified_growth",
            "background": "rho_mem(a) fixed",
            "perturbation_rule": "derive mu(a,k), eta_slip(a,k), Sigma(a,k), F_fric(a,k), S_mem(a,k)",
            "rest_frame_sound_speed": "parent_derived",
            "anisotropic_stress": "parent_derived",
            "implementation_path": "modified Einstein-Boltzmann source functions with conservation proof",
            "support_status": "not_ready",
            "promotion_blocker": "no derived functions yet; cannot be fitted after seeing CMB/growth",
        },
    ]


def variable_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "background",
            "variable": "rho_mem(a)",
            "formula_or_contract": "1-Omega_m0 + B_mem[1-exp(-(ln(1+z)/u3)^p)]",
            "current_status": "defined",
            "Boltzmann_role": "background expansion H(a)",
            "promotion_blocker": "calibration bridge to h,r_d,Omega_m0 remains unresolved",
        },
        {
            "block": "background",
            "variable": "w_mem(a)",
            "formula_or_contract": "-1 + B_mem A_N/[3 rho_mem]",
            "current_status": "defined",
            "Boltzmann_role": "dark-sector equation of state",
            "promotion_blocker": "effective conservation law still needs parent stress owner",
        },
        {
            "block": "fluid_stability",
            "variable": "c_a2",
            "formula_or_contract": "w - w_prime/[3(1+w)]",
            "current_status": "diagnostic_only",
            "Boltzmann_role": "adiabatic pressure term in naive fluid equations",
            "promotion_blocker": "1+w -> 0 requires scalar/PPF/frozen-constraint handling",
        },
        {
            "block": "perturbations",
            "variable": "c_s_eff^2",
            "formula_or_contract": "1 for effective scalar/high-sound-speed route; not applicable for exact auxiliary route",
            "current_status": "effective_choice",
            "Boltzmann_role": "rest-frame pressure support suppressing clustering",
            "promotion_blocker": "not derived from parent MTS action",
        },
        {
            "block": "perturbations",
            "variable": "delta_mem, theta_mem",
            "formula_or_contract": "zero for exact auxiliary route, high-c_s evolved for effective scalar route",
            "current_status": "conditional_modes_defined",
            "Boltzmann_role": "Einstein source terms and late ISW/lensing response",
            "promotion_blocker": "must choose and derive the route before support claim",
        },
        {
            "block": "perturbations",
            "variable": "pi_mem / anisotropic stress",
            "formula_or_contract": "0 in both exact auxiliary and canonical scalar routes",
            "current_status": "effective_contract",
            "Boltzmann_role": "metric slip Phi-Psi and lensing source",
            "promotion_blocker": "parent action must prove no linear shear response",
        },
        {
            "block": "modified_gravity",
            "variable": "mu, eta_slip, Sigma",
            "formula_or_contract": "mu=eta=Sigma=1 in exact smooth route; bounded |mu-1| in high-c_s subhorizon route",
            "current_status": "late_time_effective_only",
            "Boltzmann_role": "growth, Weyl potential, lensing",
            "promotion_blocker": "full k,z CMB functions not derived",
        },
        {
            "block": "exchange",
            "variable": "Q^nu",
            "formula_or_contract": "0 for separate conservation or parent-derived controlled exchange with local Q^nu->0",
            "current_status": "contract_only",
            "Boltzmann_role": "continuity/Euler source terms",
            "promotion_blocker": "no covariant expression derived",
        },
        {
            "block": "initial_conditions",
            "variable": "delta_mem_ini, theta_mem_ini",
            "formula_or_contract": "negligible/zero because Omega_mem(z_star) ~ 1e-9 and w_mem -> -1",
            "current_status": "safe_effective_initial_condition",
            "Boltzmann_role": "primary acoustic-era perturbation source",
            "promotion_blocker": "still needs code implementation and spectra test",
        },
        {
            "block": "calibration",
            "variable": "h, r_d, BAO alpha, SN offset, Omega_m0",
            "formula_or_contract": "one parent calibration map, not independent rescue knobs",
            "current_status": "blocked",
            "Boltzmann_role": "theta_star, BAO ruler, distance ladder consistency",
            "promotion_blocker": "late-to-CMB transfer and joint calibration remain not promoted",
        },
    ]


def background_interface_rows() -> list[dict[str, Any]]:
    transfer = transfer_reference_row()
    omega_m0 = float(transfer["Omega_m_late"])
    h = float(transfer["h_profiled"])
    z_star = float(transfer["z_star"])
    z_drag = 1059.0
    z_values = [0.0, 0.15, 0.38, 0.51, 0.70, 0.85, 1.48, 10.0, 100.0, z_drag, z_star, 1.0e4]
    return [background_quantities(z, omega_m0, h) for z in z_values]


def cmb_safety_rows(backgrounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in backgrounds:
        z = float(row["z"])
        omega_mem = float(row["Omega_mem_fraction_with_radiation"])
        one_plus_w = float(row["one_plus_w_mem"])
        if z > 100.0 and omega_mem < 1.0e-6:
            readout = "primary_CMB_memory_background_negligible"
        elif z < 10.0:
            readout = "late_ISW_lensing_must_be_spectra_tested"
        else:
            readout = "transition_background_track"
        rows.append(
            {
                "z": z,
                "Omega_mem_fraction_with_radiation": omega_mem,
                "one_plus_w_mem": one_plus_w,
                "w_mem": row["w_mem"],
                "primary_CMB_readout": readout,
                "claim_limit": "background_safety_only_not_CMB_pass",
            }
        )
    return rows


def calibration_bridge_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in primary_transfer_rows():
        rows.append(
            {
                "test": "simple_late_Omega_m_to_CMB_transfer",
                "branch": f"{row['prior_table']}:{row['score_mode']}",
                "metric": "delta_chi2_vs_CMB_only",
                "value": row["delta_chi2_vs_CMB_only"],
                "Omega_m_late": row["Omega_m_late"],
                "Omega_m_CMB_only": row["Omega_m_CMB_only"],
                "delta_Omega_m_late_minus_CMB": row["delta_Omega_m_late_minus_CMB"],
                "status": "fail",
                "readout": "simple h-profiled transfer cannot claim CMB bridge",
            }
        )
    red_decisions = {row["decision"]: row["value"] for row in read_csv_rows(RED_TEAM_DECISION)}
    rows.append(
        {
            "test": "joint_calibration_red_team",
            "branch": "broad_r_d_joint_gate",
            "metric": "hard_failure_count",
            "value": red_decisions.get("hard_failure_count", ""),
            "Omega_m_late": "",
            "Omega_m_CMB_only": "",
            "delta_Omega_m_late_minus_CMB": "",
            "status": "mixed_not_promoted",
            "readout": f"failing margin={red_decisions.get('failing_gate_margin', '')}; BAO penalty fraction={red_decisions.get('BAO_fraction_of_failing_late_penalty', '')}",
        }
    )
    return rows


def gate_rows(backgrounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    z_star_rows = [row for row in backgrounds if float(row["z"]) > 1000.0 and float(row["z"]) < 1200.0]
    omega_star = max(float(row["Omega_mem_fraction_with_radiation"]) for row in z_star_rows)
    one_plus_w_star = max(abs(float(row["one_plus_w_mem"])) for row in z_star_rows)
    return [
        {
            "gate": "background_functions_defined",
            "status": "pass",
            "evidence": "rho_mem(a), w_mem(a), dw/dln_a, and radiation-inclusive Omega_mem(a) are tabulated",
        },
        {
            "gate": "primary_CMB_early_fraction",
            "status": "pass_background_safety",
            "evidence": f"max Omega_mem(z_star-like)={omega_star:.6g}; max |1+w_mem|={one_plus_w_star:.6g}",
        },
        {
            "gate": "perturbation_closure_modes",
            "status": "conditional",
            "evidence": "exact auxiliary and high-c_s effective modes are specified; parent choice not derived",
        },
        {
            "gate": "naive_fluid_stability",
            "status": "warning",
            "evidence": "1+w_mem approaches zero, so CLASS/CAMB implementation should use scalar/PPF/frozen-constraint handling rather than naive fluid denominators",
        },
        {
            "gate": "late_ISW_lensing_prediction",
            "status": "not_run",
            "evidence": "interface defines required variables but no spectra/lensing likelihood has been computed",
        },
        {
            "gate": "calibration_bridge",
            "status": "fail_not_promoted",
            "evidence": "simple Omega_m transfer fails and joint calibration red-team remains mixed",
        },
        {
            "gate": "CMB_support_claim",
            "status": "fail",
            "evidence": "Boltzmann interface contract is necessary wiring, not an official spectra pass",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    transfer = transfer_reference_row()
    return [
        {
            "item": "status",
            "verdict": "Boltzmann_interface_defined_primary_CMB_background_safe_support_claim_blocked",
            "evidence": "memory fraction at recombination is negligible, but perturbation route and calibration bridge are not promoted",
        },
        {
            "item": "best_implementation_mode",
            "verdict": "effective_scalar_or_exact_auxiliary_kill_screen",
            "evidence": "use c_s_eff^2=1 scalar/PPF or exact frozen memory to run a future CMB kill-screen without claiming parent support",
        },
        {
            "item": "calibration_blocker",
            "verdict": "late_to_CMB_transfer_tension_remains",
            "evidence": f"primary strict transfer delta_chi2={transfer['delta_chi2_vs_CMB_only']}; delta_Omega_m={transfer['delta_Omega_m_late_minus_CMB']}",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no TT/TE/EE/lensing spectra run, no parent perturbation action, no shared calibration theorem",
        },
        {
            "item": "next_target",
            "verdict": "151-CMB-kill-screen-runner-contract.md",
            "evidence": "after interface definition, next useful empirical move is a kill-screen runner or a derived calibration theorem",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-Boltzmann-interface-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    modes = interface_mode_rows()
    variables = variable_contract_rows()
    backgrounds = background_interface_rows()
    safety = cmb_safety_rows(backgrounds)
    calibration = calibration_bridge_rows()
    gates = gate_rows(backgrounds)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "issue"])
    write_csv(
        results_dir / "interface_modes.csv",
        modes,
        [
            "mode",
            "background",
            "perturbation_rule",
            "rest_frame_sound_speed",
            "anisotropic_stress",
            "implementation_path",
            "support_status",
            "promotion_blocker",
        ],
    )
    write_csv(
        results_dir / "Boltzmann_variable_contract.csv",
        variables,
        ["block", "variable", "formula_or_contract", "current_status", "Boltzmann_role", "promotion_blocker"],
    )
    write_csv(
        results_dir / "CMB_background_interface.csv",
        backgrounds,
        [
            "z",
            "a",
            "N_past_ln_1_plus_z",
            "A_mem",
            "dA_dN_past",
            "rho_mem_over_rhocrit0",
            "one_plus_w_mem",
            "w_mem",
            "dw_dln_a",
            "c_a2_adiabatic",
            "c_a2_status",
            "Omega_r0_approx",
            "matter_E2",
            "radiation_E2",
            "E2_no_radiation",
            "E2_with_radiation",
            "Omega_mem_fraction_no_radiation",
            "Omega_mem_fraction_with_radiation",
            "primary_CMB_relevance",
        ],
    )
    write_csv(
        results_dir / "CMB_safety_table.csv",
        safety,
        [
            "z",
            "Omega_mem_fraction_with_radiation",
            "one_plus_w_mem",
            "w_mem",
            "primary_CMB_readout",
            "claim_limit",
        ],
    )
    write_csv(
        results_dir / "calibration_bridge_table.csv",
        calibration,
        [
            "test",
            "branch",
            "metric",
            "value",
            "Omega_m_late",
            "Omega_m_CMB_only",
            "delta_Omega_m_late_minus_CMB",
            "status",
            "readout",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    transfer = transfer_reference_row()
    z_star = float(transfer["z_star"])
    z_star_row = min(backgrounds, key=lambda row: abs(float(row["z"]) - z_star))
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_B_mem": LOCKED_B_MEM,
        "locked_p": LOCKED_P,
        "locked_u3": LOCKED_U3,
        "reference_Omega_m_late": float(transfer["Omega_m_late"]),
        "reference_h_profiled": float(transfer["h_profiled"]),
        "z_star": z_star,
        "Omega_mem_at_z_star_with_radiation": float(z_star_row["Omega_mem_fraction_with_radiation"]),
        "delta_chi2_late_to_CMB_transfer_reference": float(transfer["delta_chi2_vs_CMB_only"]),
        "generated": [
            "source_register.csv",
            "interface_modes.csv",
            "Boltzmann_variable_contract.csv",
            "CMB_background_interface.csv",
            "CMB_safety_table.csv",
            "calibration_bridge_table.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "151-CMB-kill-screen-runner-contract.md",
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
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
