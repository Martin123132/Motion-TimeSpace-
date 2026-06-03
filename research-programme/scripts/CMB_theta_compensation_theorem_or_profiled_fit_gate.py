#!/usr/bin/env python3
"""Checkpoint 188: theta-compensation theorem attempt plus matched H0 profile gate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import camb
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_188_NAME = "CMB-theta-compensation-theorem-or-profiled-fit-gate"
CHECKPOINT_187_RUN = RUNS_ROOT / "20260601-000004-CAMB-density-convention-and-locked-transfer-theta-gate"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
CHECKPOINT_185_RUN = RUNS_ROOT / "20260601-000002-CAMB-MTS-effective-background-module-contract"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"

BASELINE_VECTOR = CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv"

STATUS_PROFILED = "CMB_theta_compensation_theorem_blocked_H0_profile_quantified_no_likelihood_claim"
STATUS_FAIL = "CMB_theta_compensation_profile_gate_failed"
CLAIM_CEILING = "theta_profile_gate_only_no_official_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_H = 0.6842175693081872
LOCKED_H0 = 100.0 * LOCKED_H
LOCKED_OMEGA_M0 = 0.3032827426766658
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25

NEUTRINO_MASS_TO_OMEGA_H2 = 93.14
ROOT_LMAX = 50
FINAL_LMAX = 200
ROOT_LOWER_H0 = 55.0
ROOT_UPPER_H0 = 75.0
ROOT_ITERATIONS = 22
THETA_ABS_TOLERANCE = 2.0e-7
RELATIVE_FLOOR = 1.0e-30
SAMPLE_ELLS = [2, 10, 30, 50, 100, 150, 200]
W_TABLE_SIZE = 500
W_TABLE_Z_MAX = 10000.0


@dataclass(frozen=True)
class ProfileFamily:
    name: str
    density_rule: str
    unprofiled_H0: float
    description: str


@dataclass(frozen=True)
class FinalBranch:
    name: str
    family: str
    model: str
    control_branch: str
    H0: float
    ombh2: float
    omch2: float
    mnu: float
    omk: float
    tau: float
    As: float
    ns: float
    omega_m_for_w_table: float
    role: str


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 188 theta compensation/profile script"),
        (WORK_DIR / "187-CAMB-density-convention-and-locked-transfer-theta-gate.md", "locked-transfer theta gate checkpoint"),
        (CHECKPOINT_187_RUN / "status.json", "checkpoint 187 machine status"),
        (CHECKPOINT_187_RUN / "results" / "theta_gate_summary.csv", "checkpoint 187 theta gate summary"),
        (CHECKPOINT_187_RUN / "results" / "branch_parameter_matrix.csv", "checkpoint 187 branch parameter matrix"),
        (WORK_DIR / "186-CAMB-high-cs-wtable-spectra-smoke.md", "same-density spectra smoke checkpoint"),
        (CHECKPOINT_186_RUN / "status.json", "checkpoint 186 machine status"),
        (WORK_DIR / "185-CAMB-MTS-effective-background-module-contract.md", "CAMB MTS mapping contract"),
        (CHECKPOINT_185_RUN / "status.json", "checkpoint 185 machine status"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline checkpoint"),
        (CHECKPOINT_183_RUN / "status.json", "checkpoint 183 machine status"),
        (BASELINE_VECTOR, "checkpoint 183 baseline parameter vector"),
        (Path(camb.__file__).resolve(), "installed CAMB Python package"),
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


def baseline_params() -> dict[str, float]:
    return {row["parameter"]: float(row["value"]) for row in read_csv_rows(BASELINE_VECTOR)}


def approx_omnuh2(mnu: float) -> float:
    return mnu / NEUTRINO_MASS_TO_OMEGA_H2


def activation(past_efolds: float) -> float:
    if past_efolds <= 0.0:
        return 0.0
    exponent = (past_efolds / LOCKED_U3) ** LOCKED_P
    if exponent > 745.0:
        return 1.0
    return 1.0 - math.exp(-exponent)


def activation_derivative(past_efolds: float) -> float:
    if past_efolds <= 0.0:
        return 0.0
    exponent = (past_efolds / LOCKED_U3) ** LOCKED_P
    if exponent > 745.0:
        return 0.0
    return math.exp(-exponent) * LOCKED_P * past_efolds ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)


def scale_factor_grid() -> np.ndarray:
    redshift_grid = np.geomspace(W_TABLE_Z_MAX, 1.0e-5, W_TABLE_SIZE - 1)
    return np.array(sorted([float(1.0 / (1.0 + redshift)) for redshift in redshift_grid] + [1.0]))


A_GRID = scale_factor_grid()


def mts_w_table(omega_m0_for_memory: float) -> np.ndarray:
    w_values: list[float] = []
    for scale_factor in A_GRID:
        past_efolds = -math.log(scale_factor)
        rho_mem = 1.0 - omega_m0_for_memory + LOCKED_B_MEM * activation(past_efolds)
        one_plus_w = LOCKED_B_MEM * activation_derivative(past_efolds) / (3.0 * rho_mem)
        w_values.append(-1.0 + one_plus_w)
    return np.array(w_values)


def family_list(params: dict[str, float]) -> list[ProfileFamily]:
    return [
        ProfileFamily(
            name="same_physical_densities",
            density_rule="hold checkpoint-183 ombh2, omch2, mnu fixed; varying H0 changes Omega_m and MTS w(a) denominator",
            unprofiled_H0=params["H0"],
            description="CMB angle profile with exactly the same physical-density ring as checkpoint 186",
        ),
        ProfileFamily(
            name="locked_Omega_m_neutrino_subtracted",
            density_rule="hold Omega_m0=0.3032827426766658 and subtract approximate massive-neutrino omega from CDM at each H0",
            unprofiled_H0=LOCKED_H0,
            description="profile around the declared locked-transfer matter fraction without changing B,p,u3",
        ),
    ]


def density_context(H0: float, family: ProfileFamily, params: dict[str, float]) -> dict[str, float]:
    hubble_fraction = H0 / 100.0
    if family.name == "same_physical_densities":
        omch2 = params["omch2"]
        omega_m_for_w = (params["ombh2"] + omch2 + approx_omnuh2(params["mnu"])) / (hubble_fraction * hubble_fraction)
        omega_m_target = omega_m_for_w
    elif family.name == "locked_Omega_m_neutrino_subtracted":
        omega_m_target = LOCKED_OMEGA_M0
        omch2 = LOCKED_OMEGA_M0 * hubble_fraction * hubble_fraction - params["ombh2"] - approx_omnuh2(params["mnu"])
        omega_m_for_w = LOCKED_OMEGA_M0
    else:  # pragma: no cover - no other families currently declared
        raise ValueError(f"unknown family {family.name}")
    if omch2 <= 0.0:
        raise ValueError(f"non-positive omch2={omch2} for H0={H0} in {family.name}")
    return {
        "H0": H0,
        "h": hubble_fraction,
        "ombh2": params["ombh2"],
        "omch2": omch2,
        "mnu": params["mnu"],
        "omk": params["omk"],
        "omega_m_for_w": omega_m_for_w,
        "omega_m_target": omega_m_target,
    }


def run_camb(
    H0: float,
    family: ProfileFamily,
    model: str,
    params: dict[str, float],
    lmax: int,
) -> dict[str, Any]:
    density = density_context(H0, family, params)
    camb_params = camb.CAMBparams()
    camb_params.set_cosmology(
        H0=H0,
        ombh2=density["ombh2"],
        omch2=density["omch2"],
        tau=params["tau"],
        mnu=density["mnu"],
        omk=density["omk"],
    )
    camb_params.InitPower.set_params(As=params["As"], ns=params["ns"])
    if model == "MTS_high_cs_fluid":
        camb_params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=A_GRID,
            wde_w_array=mts_w_table(density["omega_m_for_w"]),
            dark_energy_model="fluid",
        )
    elif model != "LCDM":
        raise ValueError(f"unknown model {model}")
    camb_params.set_for_lmax(lmax, lens_potential_accuracy=0)
    start = datetime.now(timezone.utc)
    results = camb.get_results(camb_params)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    powers = results.get_cmb_power_spectra(camb_params, CMB_unit="muK") if lmax >= FINAL_LMAX else {}
    derived = {key: float(value) for key, value in results.get_derived_params().items()}
    densities = {
        "Omega_b": float(results.get_Omega("baryon")),
        "Omega_cdm": float(results.get_Omega("cdm")),
        "Omega_nu": float(results.get_Omega("nu")),
        "Omega_de": float(results.get_Omega("de")),
        "Omega_photon": float(results.get_Omega("photon")),
        "Omega_K": float(results.get_Omega("K")),
    }
    densities["Omega_m_total_b_cdm_nu"] = densities["Omega_b"] + densities["Omega_cdm"] + densities["Omega_nu"]
    return {
        "H0": H0,
        "family": family,
        "model": model,
        "density": density,
        "results": results,
        "powers": powers,
        "derived": derived,
        "densities": densities,
        "elapsed_seconds": elapsed,
    }


def theta_value(H0: float, family: ProfileFamily, model: str, params: dict[str, float]) -> float:
    return float(run_camb(H0, family, model, params, ROOT_LMAX)["derived"]["thetastar"])


def profile_h0_to_theta(
    family: ProfileFamily,
    model: str,
    params: dict[str, float],
    target_thetastar: float,
) -> tuple[float, list[dict[str, Any]]]:
    lo = ROOT_LOWER_H0
    hi = ROOT_UPPER_H0
    theta_lo = theta_value(lo, family, model, params)
    theta_hi = theta_value(hi, family, model, params)
    f_lo = theta_lo - target_thetastar
    f_hi = theta_hi - target_thetastar
    trace_rows: list[dict[str, Any]] = [
        {
            "family": family.name,
            "model": model,
            "iteration": "bracket_low",
            "H0": lo,
            "thetastar": theta_lo,
            "theta_minus_target": f_lo,
            "status": "ok",
        },
        {
            "family": family.name,
            "model": model,
            "iteration": "bracket_high",
            "H0": hi,
            "thetastar": theta_hi,
            "theta_minus_target": f_hi,
            "status": "ok",
        },
    ]
    if f_lo * f_hi > 0.0:
        raise ValueError(f"theta target not bracketed for {family.name}/{model}: f_lo={f_lo}, f_hi={f_hi}")
    for iteration in range(ROOT_ITERATIONS):
        mid = 0.5 * (lo + hi)
        theta_mid = theta_value(mid, family, model, params)
        f_mid = theta_mid - target_thetastar
        trace_rows.append(
            {
                "family": family.name,
                "model": model,
                "iteration": iteration,
                "H0": mid,
                "thetastar": theta_mid,
                "theta_minus_target": f_mid,
                "status": "ok",
            }
        )
        if f_lo * f_mid <= 0.0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return 0.5 * (lo + hi), trace_rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "locked MTS background internally compensates theta_star",
            "attempted_derivation": "Use locked B_mem,p,u3 non-phantom memory density in flat CAMB background at fixed physical densities.",
            "evidence": "Checkpoint 186 same-density theta_star shift is +0.004593764; checkpoint 187 locked-transfer branches are not reduced.",
            "status": "rejected_as_derived_theorem",
            "consequence": "Theta compensation cannot be claimed from the existing locked background alone.",
        },
        {
            "claim": "late memory can move r_s enough to compensate",
            "attempted_derivation": "Check whether recombination sound horizon changes instead of late distance.",
            "evidence": "Checkpoint 186 rdrag fractional shift is about -1.1e-6 while theta_star shifts about +4.6e-3.",
            "status": "rejected_for_current_branch",
            "consequence": "The hazard is mainly D_A/theta projection, not early sound-horizon physics.",
        },
        {
            "claim": "locked h/Omega_m transfer is the compensation",
            "attempted_derivation": "Declare h=0.6842175693, Omega_m0=0.3032827427 and test both neutrino conventions.",
            "evidence": "Checkpoint 187 locked fluid theta shifts are +0.004729833 and +0.004711892 vs their matched LCDM controls.",
            "status": "rejected_at_smoke_gate",
            "consequence": "The declared transfer stance runs but slightly worsens the raw theta hazard.",
        },
        {
            "claim": "H0 profiling can remove theta hazard",
            "attempted_derivation": "Treat H0 as a profiled nuisance/fit parameter and solve theta_star(H0)=theta_star,target.",
            "evidence": "This checkpoint quantifies the required H0 shifts.",
            "status": "allowed_as_fit_gate_not_theorem",
            "consequence": "If used later, LCDM/wCDM/CPL/MTS must receive the same freedom and model-selection penalties.",
        },
        {
            "claim": "parent action supplies theta compensation",
            "attempted_derivation": "Look for already-owned perturbation/ruler/local-GR mechanism from prior checkpoints.",
            "evidence": "Parent action, exact auxiliary perturbations, pair-ruler ownership, and local GR are still open/closure-limited.",
            "status": "not_derived",
            "consequence": "A future theorem may exist, but it is not available for CMB evidence now.",
        },
    ]


def profile_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_family": "LCDM",
            "profiled_parameters_allowed": "H0/theta, standard physical densities in future likelihood",
            "fixed_parameters_in_this_gate": "ombh2, omch2, tau, As, ns, mnu, omk from checkpoint 183 unless family declares Omega_m lock",
            "penalty_rule": "H0 profile is not counted as MTS evidence; future likelihood must use same nuisance/profile treatment",
            "status": "control_profile_run_here",
        },
        {
            "model_family": "wCDM",
            "profiled_parameters_allowed": "same as LCDM plus w if future official likelihood stage frees it",
            "fixed_parameters_in_this_gate": "not run in this checkpoint",
            "penalty_rule": "if w is freed, add parameter-count penalty in AIC/BIC/evidence",
            "status": "future_matched_likelihood_required",
        },
        {
            "model_family": "CPL",
            "profiled_parameters_allowed": "same as LCDM plus w0,wa if future official likelihood stage frees them",
            "fixed_parameters_in_this_gate": "not run in this checkpoint",
            "penalty_rule": "if w0,wa are freed, add parameter-count penalty in AIC/BIC/evidence",
            "status": "future_matched_likelihood_required",
        },
        {
            "model_family": "MTS_high_cs",
            "profiled_parameters_allowed": "H0/theta only in this checkpoint",
            "fixed_parameters_in_this_gate": "B_mem=2/27,p=3,u3=1/4,cs2=1,sigma=0",
            "penalty_rule": "H0 profile is a compensation cost, not a theory win; freeing B,p,u3 later must be penalized",
            "status": "MTS_profile_run_here",
        },
    ]


def build_final_branch(
    family: ProfileFamily,
    model: str,
    H0: float,
    params: dict[str, float],
    control_branch: str,
    role: str,
) -> FinalBranch:
    density = density_context(H0, family, params)
    name = f"{family.name}_{model}_H0_profiled"
    return FinalBranch(
        name=name,
        family=family.name,
        model=model,
        control_branch=control_branch,
        H0=H0,
        ombh2=density["ombh2"],
        omch2=density["omch2"],
        mnu=density["mnu"],
        omk=density["omk"],
        tau=params["tau"],
        As=params["As"],
        ns=params["ns"],
        omega_m_for_w_table=density["omega_m_for_w"],
        role=role,
    )


def run_final_branch(branch: FinalBranch) -> dict[str, Any]:
    family = ProfileFamily(branch.family, "", branch.H0, "")
    params = {
        "ombh2": branch.ombh2,
        "omch2": branch.omch2,
        "tau": branch.tau,
        "As": branch.As,
        "ns": branch.ns,
        "mnu": branch.mnu,
        "omk": branch.omk,
    }
    camb_params = camb.CAMBparams()
    camb_params.set_cosmology(
        H0=branch.H0,
        ombh2=branch.ombh2,
        omch2=branch.omch2,
        tau=branch.tau,
        mnu=branch.mnu,
        omk=branch.omk,
    )
    camb_params.InitPower.set_params(As=branch.As, ns=branch.ns)
    if branch.model == "MTS_high_cs_fluid":
        camb_params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=A_GRID,
            wde_w_array=mts_w_table(branch.omega_m_for_w_table),
            dark_energy_model="fluid",
        )
    elif branch.model != "LCDM":
        raise ValueError(f"unknown final branch model {branch.model}")
    camb_params.set_for_lmax(FINAL_LMAX, lens_potential_accuracy=0)
    start = datetime.now(timezone.utc)
    results = camb.get_results(camb_params)
    powers = results.get_cmb_power_spectra(camb_params, CMB_unit="muK")
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    derived = {key: float(value) for key, value in results.get_derived_params().items()}
    densities = {
        "Omega_b": float(results.get_Omega("baryon")),
        "Omega_cdm": float(results.get_Omega("cdm")),
        "Omega_nu": float(results.get_Omega("nu")),
        "Omega_de": float(results.get_Omega("de")),
        "Omega_K": float(results.get_Omega("K")),
    }
    densities["Omega_m_total_b_cdm_nu"] = densities["Omega_b"] + densities["Omega_cdm"] + densities["Omega_nu"]
    return {
        "branch": branch,
        "family": family,
        "params": params,
        "results": results,
        "powers": powers,
        "elapsed_seconds": elapsed,
        "derived": derived,
        "densities": densities,
    }


def profile_results_and_final_branches(
    params: dict[str, float],
    target_thetastar: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[FinalBranch]]:
    profile_rows: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    final_branches: list[FinalBranch] = []
    family_lcdm_h0: dict[str, float] = {}
    family_mts_h0: dict[str, float] = {}
    for family in family_list(params):
        for model in ["LCDM", "MTS_high_cs_fluid"]:
            root_h0, trace = profile_h0_to_theta(family, model, params, target_thetastar)
            trace_rows.extend(trace)
            final_check = run_camb(root_h0, family, model, params, FINAL_LMAX)
            unprofiled_check = run_camb(family.unprofiled_H0, family, model, params, ROOT_LMAX)
            if model == "LCDM":
                family_lcdm_h0[family.name] = root_h0
            else:
                family_mts_h0[family.name] = root_h0
            profile_rows.append(
                {
                    "family": family.name,
                    "model": model,
                    "density_rule": family.density_rule,
                    "target_thetastar": target_thetastar,
                    "unprofiled_H0": family.unprofiled_H0,
                    "unprofiled_thetastar": unprofiled_check["derived"]["thetastar"],
                    "profiled_H0": root_h0,
                    "profiled_thetastar": final_check["derived"]["thetastar"],
                    "theta_abs_error": abs(final_check["derived"]["thetastar"] - target_thetastar),
                    "delta_H0_vs_unprofiled": root_h0 - family.unprofiled_H0,
                    "delta_H0_vs_family_LCDM_profile": "",
                    "omch2_profiled": final_check["density"]["omch2"],
                    "Omega_m_actual_profiled": final_check["densities"]["Omega_m_total_b_cdm_nu"],
                    "rdrag_profiled": final_check["derived"].get("rdrag", ""),
                    "DAstar_profiled": final_check["derived"].get("DAstar", ""),
                    "age_profiled": final_check["derived"].get("age", ""),
                    "profile_status": "pass" if abs(final_check["derived"]["thetastar"] - target_thetastar) < THETA_ABS_TOLERANCE else "warning",
                    "interpretation": "control profile" if model == "LCDM" else "required MTS theta compensation, not a theorem",
                }
            )
    for row in profile_rows:
        if row["model"] == "MTS_high_cs_fluid":
            row["delta_H0_vs_family_LCDM_profile"] = float(row["profiled_H0"]) - family_lcdm_h0[row["family"]]
        else:
            row["delta_H0_vs_family_LCDM_profile"] = 0.0
    for family in family_list(params):
        lcdm_name = f"{family.name}_LCDM_H0_profiled"
        final_branches.append(
            build_final_branch(
                family,
                "LCDM",
                family_lcdm_h0[family.name],
                params,
                lcdm_name,
                "profiled LCDM control",
            )
        )
        final_branches.append(
            build_final_branch(
                family,
                "MTS_high_cs_fluid",
                family_mts_h0[family.name],
                params,
                lcdm_name,
                "profiled MTS high-cs branch",
            )
        )
    return profile_rows, trace_rows, final_branches


def branch_parameter_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_name, output in outputs.items():
        branch = output["branch"]
        densities = output["densities"]
        rows.append(
            {
                "branch": branch_name,
                "family": branch.family,
                "model": branch.model,
                "control_branch": branch.control_branch,
                "H0": branch.H0,
                "ombh2": branch.ombh2,
                "omch2": branch.omch2,
                "mnu": branch.mnu,
                "Omega_m_for_w_table": branch.omega_m_for_w_table,
                "Omega_m_actual": densities["Omega_m_total_b_cdm_nu"],
                "Omega_de_actual": densities["Omega_de"],
                "runtime_seconds": output["elapsed_seconds"],
                "role": branch.role,
            }
        )
    return rows


def acoustic_rows(outputs: dict[str, dict[str, Any]], target_thetastar: float) -> list[dict[str, Any]]:
    keys = ["age", "zstar", "rstar", "thetastar", "DAstar", "zdrag", "rdrag", "zeq", "keq"]
    rows: list[dict[str, Any]] = []
    for branch_name, output in outputs.items():
        branch = output["branch"]
        control = outputs[branch.control_branch]
        for key in keys:
            value = output["derived"].get(key, math.nan)
            control_value = control["derived"].get(key, math.nan)
            delta = value - control_value if math.isfinite(value) and math.isfinite(control_value) else math.nan
            frac = delta / control_value if control_value != 0.0 and math.isfinite(delta) else math.nan
            rows.append(
                {
                    "branch": branch_name,
                    "control_branch": branch.control_branch,
                    "quantity": key,
                    "value": value,
                    "control_value": control_value,
                    "delta_vs_control": delta,
                    "frac_delta_vs_control": frac,
                    "delta_vs_target_thetastar": value - target_thetastar if key == "thetastar" else "",
                    "claim_limit": "profiled theta gate only; no likelihood",
                }
            )
    return rows


def spectra_sample_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_name, output in outputs.items():
        total = output["powers"]["total"]
        for ell in SAMPLE_ELLS:
            rows.append(
                {
                    "branch": branch_name,
                    "ell": ell,
                    "TT_Dl_uK2": float(total[ell, 0]),
                    "EE_Dl_uK2": float(total[ell, 1]),
                    "BB_Dl_uK2": float(total[ell, 2]),
                    "TE_Dl_uK2": float(total[ell, 3]),
                    "source": "CAMB total lensed CMB power spectra",
                }
            )
    return rows


def residual_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_name, output in outputs.items():
        branch = output["branch"]
        if branch_name == branch.control_branch:
            continue
        control = outputs[branch.control_branch]
        total = output["powers"]["total"]
        control_total = control["powers"]["total"]
        for ell in range(2, FINAL_LMAX + 1):
            control_tt = float(control_total[ell, 0])
            control_ee = float(control_total[ell, 1])
            control_te = float(control_total[ell, 3])
            branch_tt = float(total[ell, 0])
            branch_ee = float(total[ell, 1])
            branch_te = float(total[ell, 3])
            rows.append(
                {
                    "branch": branch_name,
                    "control_branch": branch.control_branch,
                    "ell": ell,
                    "delta_TT_Dl_uK2": branch_tt - control_tt,
                    "frac_delta_TT": (branch_tt - control_tt) / max(abs(control_tt), RELATIVE_FLOOR),
                    "delta_EE_Dl_uK2": branch_ee - control_ee,
                    "frac_delta_EE": (branch_ee - control_ee) / max(abs(control_ee), RELATIVE_FLOOR),
                    "delta_TE_Dl_uK2": branch_te - control_te,
                    "frac_delta_TE": (branch_te - control_te) / max(abs(control_te), RELATIVE_FLOOR),
                }
            )
    return rows


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values)) if values else math.nan


def residual_summary_rows(residuals: list[dict[str, Any]], profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    profile_by_family_model = {(row["family"], row["model"]): row for row in profile_rows}
    rows: list[dict[str, Any]] = []
    for branch_name in sorted({str(row["branch"]) for row in residuals}):
        branch_rows = [row for row in residuals if row["branch"] == branch_name]
        family = branch_name.replace("_MTS_high_cs_fluid_H0_profiled", "")
        profile = profile_by_family_model.get((family, "MTS_high_cs_fluid"), {})
        tt = [float(row["frac_delta_TT"]) for row in branch_rows]
        ee = [float(row["frac_delta_EE"]) for row in branch_rows]
        te = [float(row["frac_delta_TE"]) for row in branch_rows if math.isfinite(float(row["frac_delta_TE"]))]
        max_tt_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_TT"])))
        max_ee_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_EE"])))
        rows.append(
            {
                "branch": branch_name,
                "control_branch": branch_rows[0]["control_branch"],
                "profiled_H0": profile.get("profiled_H0", ""),
                "delta_H0_vs_family_LCDM_profile": profile.get("delta_H0_vs_family_LCDM_profile", ""),
                "max_abs_frac_delta_TT": abs(float(max_tt_row["frac_delta_TT"])),
                "max_abs_frac_delta_TT_ell": max_tt_row["ell"],
                "rms_frac_delta_TT": rms(tt),
                "max_abs_frac_delta_EE": abs(float(max_ee_row["frac_delta_EE"])),
                "max_abs_frac_delta_EE_ell": max_ee_row["ell"],
                "rms_frac_delta_EE": rms(ee),
                "rms_frac_delta_TE": rms(te),
                "interpretation": "shape residual after theta has been explicitly matched",
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    residual_summary: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_missing = sum(row["exists"] != "yes" for row in source_rows)
    profile_warnings = sum(row["profile_status"] != "pass" for row in profile_rows)
    mts_profile_rows = [row for row in profile_rows if row["model"] == "MTS_high_cs_fluid"]
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if source_missing == 0 else "fail",
            "evidence": f"missing={source_missing}",
            "claim_allowed": "profile diagnostic only",
        },
        {
            "gate": "theta theorem derived",
            "status": "fail",
            "evidence": "theorem attempt rejects locked-background and locked-transfer compensation",
            "claim_allowed": "no theorem-based CMB support claim",
        },
        {
            "gate": "H0 profile roots found",
            "status": "pass" if profile_warnings == 0 else "warning",
            "evidence": f"profile_warnings={profile_warnings}",
            "claim_allowed": "compensation magnitude quantified",
        },
        {
            "gate": "MTS fixed locks preserved",
            "status": "pass",
            "evidence": f"B_mem={LOCKED_B_MEM}; p={LOCKED_P}; u3={LOCKED_U3}; rows={len(mts_profile_rows)}",
            "claim_allowed": "fixed-branch profile diagnostic",
        },
        {
            "gate": "matched baseline freedom",
            "status": "pass",
            "evidence": "LCDM profile roots run for each family; wCDM/CPL future policy logged",
            "claim_allowed": "no asymmetric scoring",
        },
        {
            "gate": "official CMB likelihood",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no CMB support claim",
        },
        {
            "gate": "profiled spectra residuals logged",
            "status": "pass" if residual_summary else "fail",
            "evidence": f"residual_rows={len(residual_summary)}",
            "claim_allowed": "shape-smoke diagnostic only",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(profile_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_theta_error = max(float(row["theta_abs_error"]) for row in profile_rows)
    same_mts = next(row for row in profile_rows if row["family"] == "same_physical_densities" and row["model"] == "MTS_high_cs_fluid")
    locked_mts = next(row for row in profile_rows if row["family"] == "locked_Omega_m_neutrino_subtracted" and row["model"] == "MTS_high_cs_fluid")
    return [
        {
            "decision": STATUS_PROFILED if max_theta_error < THETA_ABS_TOLERANCE else STATUS_FAIL,
            "meaning": "No derived theta-compensation theorem exists here; H0 profiling can force theta* but this is a fit freedom with a quantified cost.",
            "same_density_MTS_profiled_H0": same_mts["profiled_H0"],
            "same_density_delta_H0_vs_LCDM_profile": same_mts["delta_H0_vs_family_LCDM_profile"],
            "locked_Omega_m_MTS_profiled_H0": locked_mts["profiled_H0"],
            "locked_Omega_m_delta_H0_vs_LCDM_profile": locked_mts["delta_H0_vs_family_LCDM_profile"],
            "next_target": "189-CMB-profiled-shape-residual-and-likelihood-readiness.md",
            "MTS_spectra_run": "true",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_188_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params = baseline_params()
    source_rows = source_register_rows()
    target_family = family_list(params)[0]
    target_thetastar = theta_value(params["H0"], target_family, "LCDM", params)
    theorem_rows = theorem_attempt_rows()
    policy_rows = profile_policy_rows()
    profile_rows, trace_rows, final_branches = profile_results_and_final_branches(params, target_thetastar)

    final_outputs: dict[str, dict[str, Any]] = {}
    for branch in final_branches:
        final_outputs[branch.name] = run_final_branch(branch)

    parameter_rows = branch_parameter_rows(final_outputs)
    acoustic_summary = acoustic_rows(final_outputs, target_thetastar)
    spectra_samples = spectra_sample_rows(final_outputs)
    residuals = residual_rows(final_outputs)
    residual_summary = residual_summary_rows(residuals, profile_rows)
    gate_rows = claim_gate_rows(source_rows, profile_rows, residual_summary)
    decision = decision_rows(profile_rows)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "theta_compensation_theorem_attempt.csv": (
            theorem_rows,
            ["claim", "attempted_derivation", "evidence", "status", "consequence"],
        ),
        "matched_profile_policy.csv": (
            policy_rows,
            ["model_family", "profiled_parameters_allowed", "fixed_parameters_in_this_gate", "penalty_rule", "status"],
        ),
        "H0_profile_results.csv": (
            profile_rows,
            [
                "family",
                "model",
                "density_rule",
                "target_thetastar",
                "unprofiled_H0",
                "unprofiled_thetastar",
                "profiled_H0",
                "profiled_thetastar",
                "theta_abs_error",
                "delta_H0_vs_unprofiled",
                "delta_H0_vs_family_LCDM_profile",
                "omch2_profiled",
                "Omega_m_actual_profiled",
                "rdrag_profiled",
                "DAstar_profiled",
                "age_profiled",
                "profile_status",
                "interpretation",
            ],
        ),
        "H0_profile_root_trace.csv": (
            trace_rows,
            ["family", "model", "iteration", "H0", "thetastar", "theta_minus_target", "status"],
        ),
        "profiled_branch_parameter_matrix.csv": (
            parameter_rows,
            ["branch", "family", "model", "control_branch", "H0", "ombh2", "omch2", "mnu", "Omega_m_for_w_table", "Omega_m_actual", "Omega_de_actual", "runtime_seconds", "role"],
        ),
        "profiled_acoustic_summary.csv": (
            acoustic_summary,
            ["branch", "control_branch", "quantity", "value", "control_value", "delta_vs_control", "frac_delta_vs_control", "delta_vs_target_thetastar", "claim_limit"],
        ),
        "profiled_spectra_sample_Dl.csv": (
            spectra_samples,
            ["branch", "ell", "TT_Dl_uK2", "EE_Dl_uK2", "BB_Dl_uK2", "TE_Dl_uK2", "source"],
        ),
        "profiled_spectra_residuals_vs_control.csv": (
            residuals,
            ["branch", "control_branch", "ell", "delta_TT_Dl_uK2", "frac_delta_TT", "delta_EE_Dl_uK2", "frac_delta_EE", "delta_TE_Dl_uK2", "frac_delta_TE"],
        ),
        "profiled_spectra_residual_summary.csv": (
            residual_summary,
            [
                "branch",
                "control_branch",
                "profiled_H0",
                "delta_H0_vs_family_LCDM_profile",
                "max_abs_frac_delta_TT",
                "max_abs_frac_delta_TT_ell",
                "rms_frac_delta_TT",
                "max_abs_frac_delta_EE",
                "max_abs_frac_delta_EE_ell",
                "rms_frac_delta_EE",
                "rms_frac_delta_TE",
                "interpretation",
            ],
        ),
        "claim_gate_results.csv": (
            gate_rows,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "same_density_MTS_profiled_H0",
                "same_density_delta_H0_vs_LCDM_profile",
                "locked_Omega_m_MTS_profiled_H0",
                "locked_Omega_m_delta_H0_vs_LCDM_profile",
                "next_target",
                "MTS_spectra_run",
                "official_likelihood_run",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "camb_version": camb.__version__,
        "generated": list(files.keys()),
        "target_thetastar": target_thetastar,
        "same_density_MTS_profiled_H0": decision[0]["same_density_MTS_profiled_H0"],
        "locked_Omega_m_MTS_profiled_H0": decision[0]["locked_Omega_m_MTS_profiled_H0"],
        "theta_compensation_theorem_derived": False,
        "H0_profile_quantified": True,
        "MTS_spectra_run": True,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    status_payload = run(args.timestamp)
    print(json.dumps(status_payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
