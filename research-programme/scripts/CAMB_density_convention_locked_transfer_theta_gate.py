#!/usr/bin/env python3
"""Checkpoint 187: density-convention and locked-transfer theta gate for MTS CAMB smoke."""

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

CHECKPOINT_187_NAME = "CAMB-density-convention-and-locked-transfer-theta-gate"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
CHECKPOINT_185_RUN = RUNS_ROOT / "20260601-000002-CAMB-MTS-effective-background-module-contract"
CHECKPOINT_184_RUN = RUNS_ROOT / "20260601-000001-MTS-CMB-background-injection-dry-run"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"

W_TABLE = CHECKPOINT_185_RUN / "results" / "MTS_CAMB_w_table.csv"
BASELINE_VECTOR = CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv"

STATUS_THETA_NOT_REDUCED = "CAMB_locked_transfer_theta_gate_ran_theta_hazard_not_reduced_no_likelihood_claim"
STATUS_FAIL = "CAMB_locked_transfer_theta_gate_failed"
CLAIM_CEILING = "locked_transfer_theta_gate_only_no_official_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_H = 0.6842175693081872
LOCKED_OMEGA_M0 = 0.3032827426766658
LOCKED_H0 = 100.0 * LOCKED_H
LOCKED_OMEGA_M_H2 = LOCKED_OMEGA_M0 * LOCKED_H * LOCKED_H
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25

LMAX = 200
SAMPLE_ELLS = [2, 10, 30, 50, 100, 150, 200]
THETA_FRAC_WARNING = 1.0e-3
IMPROVEMENT_TOLERANCE = 1.0e-5
RELATIVE_FLOOR = 1.0e-30
NEUTRINO_MASS_TO_OMEGA_H2 = 93.14


@dataclass(frozen=True)
class BranchSpec:
    name: str
    control_name: str
    density_convention: str
    dark_energy_model: str
    H0: float
    ombh2: float
    omch2: float
    tau: float
    As: float
    ns: float
    mnu: float
    omk: float
    role: str
    rule: str


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
        (Path(__file__).resolve(), "checkpoint 187 locked-transfer theta gate script"),
        (WORK_DIR / "186-CAMB-high-cs-wtable-spectra-smoke.md", "same-density spectra smoke checkpoint"),
        (CHECKPOINT_186_RUN / "status.json", "checkpoint 186 machine status"),
        (CHECKPOINT_186_RUN / "results" / "spectra_residual_summary.csv", "checkpoint 186 theta warning summary"),
        (WORK_DIR / "185-CAMB-MTS-effective-background-module-contract.md", "CAMB MTS mapping contract"),
        (CHECKPOINT_185_RUN / "status.json", "checkpoint 185 machine status"),
        (W_TABLE, "locked MTS CAMB w(a) table"),
        (WORK_DIR / "184-MTS-CMB-background-injection-dry-run.md", "MTS CMB background injection checkpoint"),
        (CHECKPOINT_184_RUN / "status.json", "checkpoint 184 machine status"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline checkpoint"),
        (CHECKPOINT_183_RUN / "status.json", "checkpoint 183 machine status"),
        (BASELINE_VECTOR, "checkpoint 183 physical-density baseline vector"),
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


def w_table_arrays() -> tuple[np.ndarray, np.ndarray]:
    rows = read_csv_rows(W_TABLE)
    scale_factors = np.array([float(row["a"]) for row in rows])
    w_values = np.array([float(row["w_mem"]) for row in rows])
    return scale_factors, w_values


def approximate_omnuh2(mnu: float) -> float:
    return mnu / NEUTRINO_MASS_TO_OMEGA_H2


def branch_specs(params: dict[str, float]) -> list[BranchSpec]:
    omnu_h2_approx = approximate_omnuh2(params["mnu"])
    omch2_neutrino_subtracted = LOCKED_OMEGA_M_H2 - params["ombh2"] - omnu_h2_approx
    omch2_neutrino_not_subtracted = LOCKED_OMEGA_M_H2 - params["ombh2"]
    if omch2_neutrino_subtracted <= 0.0 or omch2_neutrino_not_subtracted <= 0.0:
        raise ValueError("locked-transfer omch2 convention produced non-positive CDM density")
    common = {
        "tau": params["tau"],
        "As": params["As"],
        "ns": params["ns"],
        "mnu": params["mnu"],
        "omk": params["omk"],
    }
    specs = [
        BranchSpec(
            name="LCDM_checkpoint183_control",
            control_name="LCDM_checkpoint183_control",
            density_convention="checkpoint183_plancklike_control",
            dark_energy_model="lcdm",
            H0=params["H0"],
            ombh2=params["ombh2"],
            omch2=params["omch2"],
            role="reference control",
            rule="recompute checkpoint-183 CAMB baseline",
            **common,
        ),
        BranchSpec(
            name="MTS_same_density_fluid_control",
            control_name="LCDM_checkpoint183_control",
            density_convention="checkpoint183_plancklike_control",
            dark_energy_model="fluid",
            H0=params["H0"],
            ombh2=params["ombh2"],
            omch2=params["omch2"],
            role="same-density hazard comparator",
            rule="same physical densities as LCDM; only MTS w(a) table changes",
            **common,
        ),
        BranchSpec(
            name="LCDM_locked_transfer_neutrino_subtracted",
            control_name="LCDM_locked_transfer_neutrino_subtracted",
            density_convention="locked_Omega_m_includes_massive_nu_approx_subtracted",
            dark_energy_model="lcdm",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_subtracted,
            role="locked-transfer LCDM control",
            rule="Omega_m0 target includes baryons+CDM+massive neutrino approximation",
            **common,
        ),
        BranchSpec(
            name="MTS_locked_transfer_neutrino_subtracted_fluid",
            control_name="LCDM_locked_transfer_neutrino_subtracted",
            density_convention="locked_Omega_m_includes_massive_nu_approx_subtracted",
            dark_energy_model="fluid",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_subtracted,
            role="locked-transfer MTS fluid branch",
            rule="declared locked h/Omega_m0; no post-hoc theta tuning",
            **common,
        ),
        BranchSpec(
            name="MTS_locked_transfer_neutrino_subtracted_PPF",
            control_name="LCDM_locked_transfer_neutrino_subtracted",
            density_convention="locked_Omega_m_includes_massive_nu_approx_subtracted",
            dark_energy_model="ppf",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_subtracted,
            role="locked-transfer PPF comparator",
            rule="diagnostic comparator only",
            **common,
        ),
        BranchSpec(
            name="LCDM_locked_transfer_neutrino_not_subtracted",
            control_name="LCDM_locked_transfer_neutrino_not_subtracted",
            density_convention="locked_Omega_m_excludes_massive_nu_from_target",
            dark_energy_model="lcdm",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_not_subtracted,
            role="density-convention LCDM control",
            rule="Omega_m0 target assigned to baryons+CDM, CAMB neutrino density added on top",
            **common,
        ),
        BranchSpec(
            name="MTS_locked_transfer_neutrino_not_subtracted_fluid",
            control_name="LCDM_locked_transfer_neutrino_not_subtracted",
            density_convention="locked_Omega_m_excludes_massive_nu_from_target",
            dark_energy_model="fluid",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_not_subtracted,
            role="density-convention MTS fluid branch",
            rule="same locked h/Omega_m0 convention with neutrino density added on top",
            **common,
        ),
        BranchSpec(
            name="MTS_locked_transfer_neutrino_not_subtracted_PPF",
            control_name="LCDM_locked_transfer_neutrino_not_subtracted",
            density_convention="locked_Omega_m_excludes_massive_nu_from_target",
            dark_energy_model="ppf",
            H0=LOCKED_H0,
            ombh2=params["ombh2"],
            omch2=omch2_neutrino_not_subtracted,
            role="density-convention PPF comparator",
            rule="diagnostic comparator only",
            **common,
        ),
    ]
    return specs


def run_camb_branch(
    branch: BranchSpec,
    scale_factors: np.ndarray,
    w_values: np.ndarray,
) -> dict[str, Any]:
    start = datetime.now(timezone.utc)
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=branch.H0,
        ombh2=branch.ombh2,
        omch2=branch.omch2,
        tau=branch.tau,
        mnu=branch.mnu,
        omk=branch.omk,
    )
    params.InitPower.set_params(As=branch.As, ns=branch.ns)
    if branch.dark_energy_model in {"fluid", "ppf"}:
        params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=scale_factors,
            wde_w_array=w_values,
            dark_energy_model=branch.dark_energy_model,
        )
    params.set_for_lmax(LMAX, lens_potential_accuracy=0)
    results = camb.get_results(params)
    powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
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
        "branch": branch,
        "results": results,
        "powers": powers,
        "derived": derived,
        "densities": densities,
        "elapsed_seconds": elapsed,
        "status": "pass",
        "error": "",
    }


def density_convention_rows(params: dict[str, float], specs: list[BranchSpec]) -> list[dict[str, Any]]:
    omnu_h2_approx = approximate_omnuh2(params["mnu"])
    convention_rows = [
        {
            "convention": "checkpoint183_plancklike_control",
            "H0": params["H0"],
            "h": params["H0"] / 100.0,
            "Omega_m0_target": "",
            "omega_m_h2_target": params["ombh2"] + params["omch2"] + omnu_h2_approx,
            "ombh2": params["ombh2"],
            "omch2_rule": "checkpoint-183 fixed value",
            "omch2": params["omch2"],
            "approx_omnuh2": omnu_h2_approx,
            "purpose": "Planck-like smoke control",
        },
        {
            "convention": "locked_Omega_m_includes_massive_nu_approx_subtracted",
            "H0": LOCKED_H0,
            "h": LOCKED_H,
            "Omega_m0_target": LOCKED_OMEGA_M0,
            "omega_m_h2_target": LOCKED_OMEGA_M_H2,
            "ombh2": params["ombh2"],
            "omch2_rule": "Omega_m0*h^2 - ombh2 - mnu/93.14",
            "omch2": LOCKED_OMEGA_M_H2 - params["ombh2"] - omnu_h2_approx,
            "approx_omnuh2": omnu_h2_approx,
            "purpose": "best declared CAMB convention if locked Omega_m includes massive neutrino density",
        },
        {
            "convention": "locked_Omega_m_excludes_massive_nu_from_target",
            "H0": LOCKED_H0,
            "h": LOCKED_H,
            "Omega_m0_target": LOCKED_OMEGA_M0,
            "omega_m_h2_target": LOCKED_OMEGA_M_H2,
            "ombh2": params["ombh2"],
            "omch2_rule": "Omega_m0*h^2 - ombh2",
            "omch2": LOCKED_OMEGA_M_H2 - params["ombh2"],
            "approx_omnuh2": omnu_h2_approx,
            "purpose": "sensitivity convention; neutrino density is added by CAMB on top",
        },
    ]
    used_conventions = sorted({spec.density_convention for spec in specs})
    for row in convention_rows:
        row["used_in_run"] = "yes" if row["convention"] in used_conventions else "no"
    return convention_rows


def branch_parameter_rows(specs: list[BranchSpec], outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        output = outputs.get(spec.name, {})
        densities = output.get("densities", {})
        rows.append(
            {
                "branch": spec.name,
                "control_branch": spec.control_name,
                "density_convention": spec.density_convention,
                "CAMB_dark_energy_model": spec.dark_energy_model,
                "H0": spec.H0,
                "ombh2": spec.ombh2,
                "omch2": spec.omch2,
                "mnu": spec.mnu,
                "omk": spec.omk,
                "Omega_m_total_actual": densities.get("Omega_m_total_b_cdm_nu", ""),
                "Omega_de_actual": densities.get("Omega_de", ""),
                "role": spec.role,
                "rule": spec.rule,
            }
        )
    return rows


def branch_run_summary_rows(specs: list[BranchSpec], outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        output = outputs.get(spec.name, {})
        rows.append(
            {
                "branch": spec.name,
                "CAMB_dark_energy_model": spec.dark_energy_model,
                "density_convention": spec.density_convention,
                "status": output.get("status", "missing"),
                "runtime_seconds": output.get("elapsed_seconds", ""),
                "role": spec.role,
                "error": output.get("error", "branch output missing"),
            }
        )
    return rows


def spectra_sample_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_name, output in outputs.items():
        if output["status"] != "pass":
            continue
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


def theta_gate_rows(specs: list[BranchSpec], outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    same_density_theta_frac = math.nan
    plancklike_theta = outputs["LCDM_checkpoint183_control"]["derived"]["thetastar"]
    for spec in specs:
        if spec.name == spec.control_name:
            continue
        output = outputs.get(spec.name)
        control = outputs.get(spec.control_name)
        if not output or not control or output["status"] != "pass" or control["status"] != "pass":
            continue
        theta = output["derived"]["thetastar"]
        control_theta = control["derived"]["thetastar"]
        frac_vs_control = (theta - control_theta) / control_theta
        frac_vs_plancklike = (theta - plancklike_theta) / plancklike_theta
        if spec.name == "MTS_same_density_fluid_control":
            same_density_theta_frac = frac_vs_control
        rows.append(
            {
                "branch": spec.name,
                "control_branch": spec.control_name,
                "density_convention": spec.density_convention,
                "CAMB_dark_energy_model": spec.dark_energy_model,
                "thetastar": theta,
                "control_thetastar": control_theta,
                "delta_thetastar_vs_control": theta - control_theta,
                "frac_delta_thetastar_vs_control": frac_vs_control,
                "abs_frac_delta_thetastar_vs_control": abs(frac_vs_control),
                "frac_delta_thetastar_vs_checkpoint183_LCDM": frac_vs_plancklike,
                "warning_threshold": THETA_FRAC_WARNING,
                "theta_warning": "yes" if abs(frac_vs_control) > THETA_FRAC_WARNING else "no",
                "same_density_reference_abs_frac": "",
                "improvement_vs_same_density_abs_frac": "",
                "gate_readout": "reference_same_density_hazard" if spec.name == "MTS_same_density_fluid_control" else "pending",
            }
        )
    for row in rows:
        if row["branch"] == "MTS_same_density_fluid_control":
            row["same_density_reference_abs_frac"] = abs(same_density_theta_frac)
            row["improvement_vs_same_density_abs_frac"] = 0.0
            continue
        if str(row["CAMB_dark_energy_model"]) not in {"fluid", "ppf"}:
            continue
        improvement = abs(same_density_theta_frac) - float(row["abs_frac_delta_thetastar_vs_control"])
        row["same_density_reference_abs_frac"] = abs(same_density_theta_frac)
        row["improvement_vs_same_density_abs_frac"] = improvement
        if improvement > IMPROVEMENT_TOLERANCE:
            row["gate_readout"] = "improved_but_still_requires_likelihood" if row["theta_warning"] == "yes" else "theta_hazard_reduced_in_smoke"
        else:
            row["gate_readout"] = "not_reduced"
    return rows


def acoustic_distance_rows(specs: list[BranchSpec], outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    keys = ["age", "zstar", "rstar", "thetastar", "DAstar", "zdrag", "rdrag", "zeq", "keq"]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        output = outputs.get(spec.name)
        control = outputs.get(spec.control_name)
        if not output or not control or output["status"] != "pass" or control["status"] != "pass":
            continue
        for key in keys:
            value = float(output["derived"].get(key, math.nan))
            control_value = float(control["derived"].get(key, math.nan))
            delta = value - control_value if math.isfinite(value) and math.isfinite(control_value) else math.nan
            frac = delta / control_value if control_value != 0.0 and math.isfinite(delta) else math.nan
            rows.append(
                {
                    "branch": spec.name,
                    "control_branch": spec.control_name,
                    "quantity": key,
                    "value": value,
                    "control_value": control_value,
                    "delta_vs_control": delta,
                    "frac_delta_vs_control": frac,
                    "claim_limit": "theta gate diagnostic; no official likelihood",
                }
            )
    return rows


def residual_rows(specs: list[BranchSpec], outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        if spec.name == spec.control_name:
            continue
        output = outputs.get(spec.name)
        control = outputs.get(spec.control_name)
        if not output or not control or output["status"] != "pass" or control["status"] != "pass":
            continue
        total = output["powers"]["total"]
        control_total = control["powers"]["total"]
        for ell in range(2, LMAX + 1):
            control_tt = float(control_total[ell, 0])
            control_ee = float(control_total[ell, 1])
            control_te = float(control_total[ell, 3])
            branch_tt = float(total[ell, 0])
            branch_ee = float(total[ell, 1])
            branch_te = float(total[ell, 3])
            rows.append(
                {
                    "branch": spec.name,
                    "control_branch": spec.control_name,
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


def residual_summary_rows(residuals: list[dict[str, Any]], theta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theta_by_branch = {row["branch"]: row for row in theta_rows}
    rows: list[dict[str, Any]] = []
    for branch_name in sorted({str(row["branch"]) for row in residuals}):
        branch_rows = [row for row in residuals if row["branch"] == branch_name]
        tt = [float(row["frac_delta_TT"]) for row in branch_rows]
        ee = [float(row["frac_delta_EE"]) for row in branch_rows]
        te = [float(row["frac_delta_TE"]) for row in branch_rows if math.isfinite(float(row["frac_delta_TE"]))]
        max_tt_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_TT"])))
        max_ee_row = max(branch_rows, key=lambda row: abs(float(row["frac_delta_EE"])))
        theta_row = theta_by_branch.get(branch_name, {})
        rows.append(
            {
                "branch": branch_name,
                "control_branch": branch_rows[0]["control_branch"],
                "max_abs_frac_delta_TT": abs(float(max_tt_row["frac_delta_TT"])),
                "max_abs_frac_delta_TT_ell": max_tt_row["ell"],
                "rms_frac_delta_TT": rms(tt),
                "max_abs_frac_delta_EE": abs(float(max_ee_row["frac_delta_EE"])),
                "max_abs_frac_delta_EE_ell": max_ee_row["ell"],
                "rms_frac_delta_EE": rms(ee),
                "rms_frac_delta_TE": rms(te),
                "frac_delta_thetastar_vs_control": theta_row.get("frac_delta_thetastar_vs_control", ""),
                "theta_warning": theta_row.get("theta_warning", ""),
                "gate_readout": theta_row.get("gate_readout", ""),
            }
        )
    return rows


def claim_gate_rows(
    source_rows: list[dict[str, Any]],
    branch_summary: list[dict[str, Any]],
    theta_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    branches_ok = all(row["status"] == "pass" for row in branch_summary)
    locked_fluid_rows = [
        row for row in theta_rows
        if str(row["branch"]).startswith("MTS_locked_transfer") and row["CAMB_dark_energy_model"] == "fluid"
    ]
    locked_improved = any(float(row["improvement_vs_same_density_abs_frac"]) > IMPROVEMENT_TOLERANCE for row in locked_fluid_rows)
    locked_theta_warnings = sum(row["theta_warning"] == "yes" for row in locked_fluid_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": f"missing={sum(row['exists'] != 'yes' for row in source_rows)}",
            "claim_allowed": "theta diagnostic only",
        },
        {
            "gate": "all declared branches ran",
            "status": "pass" if branches_ok else "fail",
            "evidence": f"branch_failures={sum(row['status'] != 'pass' for row in branch_summary)}",
            "claim_allowed": "pipeline comparison",
        },
        {
            "gate": "density conventions declared",
            "status": "pass",
            "evidence": "neutrino-subtracted and not-subtracted locked conventions both logged",
            "claim_allowed": "prevents silent density rescue",
        },
        {
            "gate": "locked-transfer theta hazard reduced",
            "status": "warning" if not locked_improved else "pass",
            "evidence": f"locked_fluid_branches_improved={sum(float(row['improvement_vs_same_density_abs_frac']) > IMPROVEMENT_TOLERANCE for row in locked_fluid_rows)}",
            "claim_allowed": "no CMB support claim if warning",
        },
        {
            "gate": "locked-transfer theta warning",
            "status": "warning" if locked_theta_warnings else "pass",
            "evidence": f"locked_fluid_theta_warnings={locked_theta_warnings}",
            "claim_allowed": "requires derived theta compensation or matched likelihood fit",
        },
        {
            "gate": "exact auxiliary spectra",
            "status": "blocked",
            "evidence": "checkpoint 185 found no built-in CAMB delta=theta=0 primitive",
            "claim_allowed": "no exact auxiliary CMB claim",
        },
        {
            "gate": "official likelihood run",
            "status": "not_run",
            "evidence": "no Planck/ACT/SPT likelihood called",
            "claim_allowed": "no CMB support claim",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(gate_rows: list[dict[str, Any]], theta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hard_failures = [row for row in gate_rows if row["status"] == "fail" and row["gate"] != "support claim allowed"]
    locked_not_reduced = any(
        row["CAMB_dark_energy_model"] == "fluid"
        and str(row["branch"]).startswith("MTS_locked_transfer")
        and row["gate_readout"] == "not_reduced"
        for row in theta_rows
    )
    status = STATUS_FAIL if hard_failures else STATUS_THETA_NOT_REDUCED
    next_target = (
        "188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md"
        if locked_not_reduced and status != STATUS_FAIL
        else "188-CMB-likelihood-readiness-or-theta-fit-gate.md"
    )
    return [
        {
            "decision": status,
            "meaning": "locked h/Omega_m transfer branches run but do not reduce the raw theta* hazard relative to the same-density smoke"
            if locked_not_reduced
            else "locked h/Omega_m transfer branches run; theta hazard requires next likelihood/fitting gate",
            "next_target": next_target,
            "MTS_spectra_run": "true",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_187_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params = baseline_params()
    scale_factors, w_values = w_table_arrays()
    specs = branch_specs(params)
    source_rows = source_register_rows()

    outputs: dict[str, dict[str, Any]] = {}
    for spec in specs:
        try:
            outputs[spec.name] = run_camb_branch(spec, scale_factors, w_values)
        except Exception as exc:  # pragma: no cover - engine/runtime dependent
            outputs[spec.name] = {
                "branch": spec,
                "status": "fail",
                "error": f"{type(exc).__name__}: {exc}",
                "elapsed_seconds": "",
            }

    density_rows = density_convention_rows(params, specs)
    parameter_rows = branch_parameter_rows(specs, outputs)
    branch_summary = branch_run_summary_rows(specs, outputs)
    theta_rows = theta_gate_rows(specs, outputs)
    acoustic_rows = acoustic_distance_rows(specs, outputs)
    spectra_samples = spectra_sample_rows(outputs)
    residuals = residual_rows(specs, outputs)
    residual_summary = residual_summary_rows(residuals, theta_rows)
    gate_rows = claim_gate_rows(source_rows, branch_summary, theta_rows)
    decision = decision_rows(gate_rows, theta_rows)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "density_convention_ledger.csv": (
            density_rows,
            ["convention", "H0", "h", "Omega_m0_target", "omega_m_h2_target", "ombh2", "omch2_rule", "omch2", "approx_omnuh2", "purpose", "used_in_run"],
        ),
        "branch_parameter_matrix.csv": (
            parameter_rows,
            ["branch", "control_branch", "density_convention", "CAMB_dark_energy_model", "H0", "ombh2", "omch2", "mnu", "omk", "Omega_m_total_actual", "Omega_de_actual", "role", "rule"],
        ),
        "branch_run_summary.csv": (
            branch_summary,
            ["branch", "CAMB_dark_energy_model", "density_convention", "status", "runtime_seconds", "role", "error"],
        ),
        "theta_gate_summary.csv": (
            theta_rows,
            [
                "branch",
                "control_branch",
                "density_convention",
                "CAMB_dark_energy_model",
                "thetastar",
                "control_thetastar",
                "delta_thetastar_vs_control",
                "frac_delta_thetastar_vs_control",
                "abs_frac_delta_thetastar_vs_control",
                "frac_delta_thetastar_vs_checkpoint183_LCDM",
                "warning_threshold",
                "theta_warning",
                "same_density_reference_abs_frac",
                "improvement_vs_same_density_abs_frac",
                "gate_readout",
            ],
        ),
        "acoustic_distance_summary.csv": (
            acoustic_rows,
            ["branch", "control_branch", "quantity", "value", "control_value", "delta_vs_control", "frac_delta_vs_control", "claim_limit"],
        ),
        "spectra_sample_Dl.csv": (
            spectra_samples,
            ["branch", "ell", "TT_Dl_uK2", "EE_Dl_uK2", "BB_Dl_uK2", "TE_Dl_uK2", "source"],
        ),
        "spectra_residuals_vs_control.csv": (
            residuals,
            ["branch", "control_branch", "ell", "delta_TT_Dl_uK2", "frac_delta_TT", "delta_EE_Dl_uK2", "frac_delta_EE", "delta_TE_Dl_uK2", "frac_delta_TE"],
        ),
        "spectra_residual_summary.csv": (
            residual_summary,
            [
                "branch",
                "control_branch",
                "max_abs_frac_delta_TT",
                "max_abs_frac_delta_TT_ell",
                "rms_frac_delta_TT",
                "max_abs_frac_delta_EE",
                "max_abs_frac_delta_EE_ell",
                "rms_frac_delta_EE",
                "rms_frac_delta_TE",
                "frac_delta_thetastar_vs_control",
                "theta_warning",
                "gate_readout",
            ],
        ),
        "claim_gate_results.csv": (
            gate_rows,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "next_target", "MTS_spectra_run", "official_likelihood_run", "promotion_allowed", "claim_ceiling"],
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
        "branches": [spec.name for spec in specs],
        "lmax": LMAX,
        "locked_h": LOCKED_H,
        "locked_Omega_m0": LOCKED_OMEGA_M0,
        "locked_B_mem": LOCKED_B_MEM,
        "locked_p": LOCKED_P,
        "locked_u3": LOCKED_U3,
        "MTS_spectra_run": True,
        "official_likelihood_run": False,
        "promotion_allowed": False,
        "locked_transfer_theta_hazard_reduced": False,
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
