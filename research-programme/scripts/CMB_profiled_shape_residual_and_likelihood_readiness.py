#!/usr/bin/env python3
"""Checkpoint 189: profiled CMB shape residual and likelihood-readiness gate."""

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

CHECKPOINT_189_NAME = "CMB-profiled-shape-residual-and-likelihood-readiness"
CHECKPOINT_188_RUN = RUNS_ROOT / "20260601-000005-CMB-theta-compensation-theorem-or-profiled-fit-gate"
CHECKPOINT_187_RUN = RUNS_ROOT / "20260601-000004-CAMB-density-convention-and-locked-transfer-theta-gate"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
CHECKPOINT_183_RUN = RUNS_ROOT / "20260531-235959-LCDM-baseline-reproduction-dry-run"
BASELINE_VECTOR = CHECKPOINT_183_RUN / "results" / "baseline_parameter_vector.csv"

STATUS_READY = "CMB_profiled_shape_residuals_quantified_likelihood_readiness_open_no_claim"
STATUS_FAIL = "CMB_profiled_shape_residual_gate_failed"
CLAIM_CEILING = "profiled_shape_residual_proxy_only_no_official_likelihood_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
LOCKED_OMEGA_M0 = 0.3032827426766658
NEUTRINO_MASS_TO_OMEGA_H2 = 93.14
LMAX_EXTENDED = 1000
W_TABLE_SIZE = 700
W_TABLE_Z_MAX = 10000.0
RELATIVE_FLOOR = 1.0e-30
SAMPLE_ELLS = [2, 10, 30, 50, 100, 200, 500, 800, 1000]
BANDS = [
    ("low_ell_2_29", 2, 29),
    ("acoustic_30_200", 30, 200),
    ("extended_201_1000", 201, 1000),
    ("all_2_1000", 2, 1000),
]


@dataclass(frozen=True)
class BranchSpec:
    name: str
    family: str
    model: str
    control_branch: str
    H0: float
    ombh2: float
    omch2: float
    tau: float
    As: float
    ns: float
    mnu: float
    omk: float
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
        (Path(__file__).resolve(), "checkpoint 189 profiled shape-readiness script"),
        (WORK_DIR / "188-CMB-theta-compensation-theorem-or-profiled-fit-gate.md", "theta theorem/profile gate checkpoint"),
        (CHECKPOINT_188_RUN / "status.json", "checkpoint 188 machine status"),
        (CHECKPOINT_188_RUN / "results" / "H0_profile_results.csv", "checkpoint 188 H0 profile results"),
        (CHECKPOINT_188_RUN / "results" / "profiled_branch_parameter_matrix.csv", "checkpoint 188 profiled branch matrix"),
        (CHECKPOINT_188_RUN / "results" / "profiled_spectra_residual_summary.csv", "checkpoint 188 lmax-200 residual summary"),
        (WORK_DIR / "187-CAMB-density-convention-and-locked-transfer-theta-gate.md", "locked-transfer theta gate checkpoint"),
        (CHECKPOINT_187_RUN / "status.json", "checkpoint 187 status"),
        (WORK_DIR / "186-CAMB-high-cs-wtable-spectra-smoke.md", "same-density spectra smoke checkpoint"),
        (CHECKPOINT_186_RUN / "status.json", "checkpoint 186 status"),
        (WORK_DIR / "183-LCDM-baseline-reproduction-dry-run.md", "LCDM baseline checkpoint"),
        (CHECKPOINT_183_RUN / "status.json", "checkpoint 183 status"),
        (BASELINE_VECTOR, "checkpoint 183 baseline vector"),
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


def scale_factor_grid() -> np.ndarray:
    redshift_grid = np.geomspace(W_TABLE_Z_MAX, 1.0e-5, W_TABLE_SIZE - 1)
    return np.array(sorted([float(1.0 / (1.0 + redshift)) for redshift in redshift_grid] + [1.0]))


A_GRID = scale_factor_grid()


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


def mts_w_table(omega_m0_for_memory: float) -> np.ndarray:
    values: list[float] = []
    for scale_factor in A_GRID:
        past_efolds = -math.log(scale_factor)
        rho_mem = 1.0 - omega_m0_for_memory + LOCKED_B_MEM * activation(past_efolds)
        values.append(-1.0 + LOCKED_B_MEM * activation_derivative(past_efolds) / (3.0 * rho_mem))
    return np.array(values)


def load_profiled_branch_specs(params: dict[str, float]) -> list[BranchSpec]:
    rows = read_csv_rows(CHECKPOINT_188_RUN / "results" / "profiled_branch_parameter_matrix.csv")
    specs: list[BranchSpec] = []
    for row in rows:
        specs.append(
            BranchSpec(
                name=row["branch"],
                family=row["family"],
                model=row["model"],
                control_branch=row["control_branch"],
                H0=float(row["H0"]),
                ombh2=float(row["ombh2"]),
                omch2=float(row["omch2"]),
                tau=params["tau"],
                As=params["As"],
                ns=params["ns"],
                mnu=float(row["mnu"]),
                omk=params["omk"],
                omega_m_for_w_table=float(row["Omega_m_for_w_table"]),
                role=row["role"],
            )
        )
    return specs


def run_camb_branch(spec: BranchSpec) -> dict[str, Any]:
    params = camb.CAMBparams()
    params.set_cosmology(
        H0=spec.H0,
        ombh2=spec.ombh2,
        omch2=spec.omch2,
        tau=spec.tau,
        mnu=spec.mnu,
        omk=spec.omk,
    )
    params.InitPower.set_params(As=spec.As, ns=spec.ns)
    if spec.model == "MTS_high_cs_fluid":
        params.set_dark_energy(
            cs2=1.0,
            use_tabulated_w=True,
            wde_a_array=A_GRID,
            wde_w_array=mts_w_table(spec.omega_m_for_w_table),
            dark_energy_model="fluid",
        )
    elif spec.model != "LCDM":
        raise ValueError(f"unknown branch model {spec.model}")
    params.set_for_lmax(LMAX_EXTENDED, lens_potential_accuracy=0)
    start = datetime.now(timezone.utc)
    results = camb.get_results(params)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    powers = results.get_cmb_power_spectra(params, CMB_unit="muK")
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
        "spec": spec,
        "status": "pass",
        "elapsed_seconds": elapsed,
        "powers": powers,
        "derived": derived,
        "densities": densities,
        "error": "",
    }


def derivation_pressure_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "B_mem=2/27",
            "current_status": "empirical locked closure / theorem target",
            "derivable_now": "no",
            "why_it_matters": "sets late memory amplitude and CMB w(a) hump",
            "next_derivation_route": "parent boundary-charge or action-normalization owner",
        },
        {
            "object": "p=3,u3=1/4 activation",
            "current_status": "locked regularized activation closure",
            "derivable_now": "partial",
            "why_it_matters": "controls redshift width of distance shift",
            "next_derivation_route": "derive activation from cell-current/regularity rather than fit convenience",
        },
        {
            "object": "high-cs perturbation owner",
            "current_status": "effective scalar branch from checkpoint 178",
            "derivable_now": "partial/effective only",
            "why_it_matters": "lets CAMB run without clustered dark-energy blow-up",
            "next_derivation_route": "derive exact auxiliary or parent scalar stress equations",
        },
        {
            "object": "theta compensation",
            "current_status": "not derived; H0 profile quantified",
            "derivable_now": "no",
            "why_it_matters": "CMB acoustic angle is the live pressure point",
            "next_derivation_route": "derive a relation that enforces delta ln D_A = delta ln r_s without post-hoc H0 tuning",
        },
        {
            "object": "local GR / PPN silence",
            "current_status": "screened effective branch, not parent-owned",
            "derivable_now": "no",
            "why_it_matters": "fundamental theory claim needs GR recovery",
            "next_derivation_route": "parent local fixed point / q_loc mechanism, not CMB fitting",
        },
    ]


def branch_run_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, output in outputs.items():
        spec = output["spec"]
        densities = output["densities"]
        rows.append(
            {
                "branch": name,
                "family": spec.family,
                "model": spec.model,
                "control_branch": spec.control_branch,
                "H0": spec.H0,
                "ombh2": spec.ombh2,
                "omch2": spec.omch2,
                "Omega_m_actual": densities["Omega_m_total_b_cdm_nu"],
                "Omega_de_actual": densities["Omega_de"],
                "thetastar": output["derived"].get("thetastar", ""),
                "rdrag": output["derived"].get("rdrag", ""),
                "DAstar": output["derived"].get("DAstar", ""),
                "age": output["derived"].get("age", ""),
                "runtime_seconds": output["elapsed_seconds"],
                "status": output["status"],
                "error": output["error"],
            }
        )
    return rows


def spectra_sample_rows(outputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, output in outputs.items():
        total = output["powers"]["total"]
        for ell in SAMPLE_ELLS:
            rows.append(
                {
                    "branch": name,
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
    for name, output in outputs.items():
        spec = output["spec"]
        if name == spec.control_branch:
            continue
        control = outputs[spec.control_branch]
        total = output["powers"]["total"]
        control_total = control["powers"]["total"]
        for ell in range(2, LMAX_EXTENDED + 1):
            sigma_frac_cv = math.sqrt(2.0 / (2.0 * ell + 1.0))
            control_tt = float(control_total[ell, 0])
            control_ee = float(control_total[ell, 1])
            control_te = float(control_total[ell, 3])
            branch_tt = float(total[ell, 0])
            branch_ee = float(total[ell, 1])
            branch_te = float(total[ell, 3])
            frac_tt = (branch_tt - control_tt) / max(abs(control_tt), RELATIVE_FLOOR)
            frac_ee = (branch_ee - control_ee) / max(abs(control_ee), RELATIVE_FLOOR)
            frac_te = (branch_te - control_te) / max(abs(control_te), RELATIVE_FLOOR)
            rows.append(
                {
                    "branch": name,
                    "control_branch": spec.control_branch,
                    "family": spec.family,
                    "ell": ell,
                    "frac_delta_TT": frac_tt,
                    "frac_delta_EE": frac_ee,
                    "frac_delta_TE": frac_te,
                    "cv_sigma_frac_TT_proxy": sigma_frac_cv,
                    "TT_cv_z_proxy": frac_tt / sigma_frac_cv,
                    "EE_cv_z_proxy": frac_ee / sigma_frac_cv,
                    "TE_cv_z_proxy": frac_te / sigma_frac_cv,
                    "delta_TT_Dl_uK2": branch_tt - control_tt,
                    "delta_EE_Dl_uK2": branch_ee - control_ee,
                    "delta_TE_Dl_uK2": branch_te - control_te,
                }
            )
    return rows


def rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values)) if values else math.nan


def band_summary_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in sorted({str(row["branch"]) for row in residuals}):
        branch_rows = [row for row in residuals if row["branch"] == branch]
        for band, ell_min, ell_max in BANDS:
            selected = [row for row in branch_rows if ell_min <= int(row["ell"]) <= ell_max]
            if not selected:
                continue
            tt_frac = [float(row["frac_delta_TT"]) for row in selected]
            ee_frac = [float(row["frac_delta_EE"]) for row in selected]
            te_frac = [float(row["frac_delta_TE"]) for row in selected if math.isfinite(float(row["frac_delta_TE"]))]
            tt_cv = [float(row["TT_cv_z_proxy"]) for row in selected]
            ee_cv = [float(row["EE_cv_z_proxy"]) for row in selected]
            max_tt = max(selected, key=lambda row: abs(float(row["frac_delta_TT"])))
            max_ee = max(selected, key=lambda row: abs(float(row["frac_delta_EE"])))
            rows.append(
                {
                    "branch": branch,
                    "control_branch": selected[0]["control_branch"],
                    "band": band,
                    "ell_min": ell_min,
                    "ell_max": ell_max,
                    "n_ell": len(selected),
                    "rms_frac_delta_TT": rms(tt_frac),
                    "max_abs_frac_delta_TT": abs(float(max_tt["frac_delta_TT"])),
                    "max_abs_frac_delta_TT_ell": max_tt["ell"],
                    "rms_frac_delta_EE": rms(ee_frac),
                    "max_abs_frac_delta_EE": abs(float(max_ee["frac_delta_EE"])),
                    "max_abs_frac_delta_EE_ell": max_ee["ell"],
                    "rms_frac_delta_TE": rms(te_frac),
                    "rms_TT_cv_z_proxy": rms(tt_cv),
                    "rms_EE_cv_z_proxy": rms(ee_cv),
                    "proxy_interpretation": "not a likelihood; ignores covariance/noise/foregrounds",
                }
            )
    return rows


def readiness_rows(band_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    same_all = next(
        row for row in band_rows
        if row["branch"] == "same_physical_densities_MTS_high_cs_fluid_H0_profiled" and row["band"] == "all_2_1000"
    )
    locked_all = next(
        row for row in band_rows
        if row["branch"] == "locked_Omega_m_neutrino_subtracted_MTS_high_cs_fluid_H0_profiled" and row["band"] == "all_2_1000"
    )
    same_high = next(
        row for row in band_rows
        if row["branch"] == "same_physical_densities_MTS_high_cs_fluid_H0_profiled" and row["band"] == "extended_201_1000"
    )
    locked_high = next(
        row for row in band_rows
        if row["branch"] == "locked_Omega_m_neutrino_subtracted_MTS_high_cs_fluid_H0_profiled" and row["band"] == "extended_201_1000"
    )
    return [
        {
            "readiness_item": "same-density profiled branch",
            "status": "ready_for_mock_likelihood",
            "evidence": f"all-band TT RMS={same_all['rms_frac_delta_TT']}; high-ell TT RMS={same_high['rms_frac_delta_TT']}",
            "caveat": "requires low H0 and Omega_m drift; not locked-transfer theory evidence",
            "next_action": "run mock/official likelihood with LCDM/wCDM/CPL/MTS matched freedoms",
        },
        {
            "readiness_item": "locked-Omega_m profiled branch",
            "status": "stress_test_only_before_official_claim",
            "evidence": f"all-band TT RMS={locked_all['rms_frac_delta_TT']}; high-ell TT RMS={locked_high['rms_frac_delta_TT']}",
            "caveat": "percent-level shape residual after theta matching",
            "next_action": "keep as pressure branch; do not lead with it as CMB support",
        },
        {
            "readiness_item": "official likelihood assets",
            "status": "not_ready_locally",
            "evidence": "no Planck/ACT/SPT likelihood invoked in this checkpoint",
            "caveat": "CAMB spectra are local, but official likelihood data/code are separate",
            "next_action": "build likelihood harness or use public-lite compressed CMB proxies first",
        },
        {
            "readiness_item": "derivation-first requirement",
            "status": "open",
            "evidence": "theta theorem still failed in checkpoint 188",
            "caveat": "fitting cannot replace parent derivation",
            "next_action": "derive parent relation for D_A/r_s/H0, or explicitly label H0 profile as phenomenological closure",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], run_rows: list[dict[str, Any]], band_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_missing = sum(row["exists"] != "yes" for row in source_rows)
    branch_failures = sum(row["status"] != "pass" for row in run_rows)
    all_band_rows = [row for row in band_rows if row["band"] == "all_2_1000"]
    residuals_logged = len(all_band_rows) == 2
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if source_missing == 0 else "fail",
            "evidence": f"missing={source_missing}",
            "claim_allowed": "readiness diagnostic only",
        },
        {
            "gate": "extended CAMB branches ran",
            "status": "pass" if branch_failures == 0 else "fail",
            "evidence": f"branch_failures={branch_failures}; lmax={LMAX_EXTENDED}",
            "claim_allowed": "shape residual proxy",
        },
        {
            "gate": "profiled residuals logged",
            "status": "pass" if residuals_logged else "fail",
            "evidence": f"all_band_rows={len(all_band_rows)}",
            "claim_allowed": "likelihood readiness only",
        },
        {
            "gate": "theta compensation derived",
            "status": "fail",
            "evidence": "checkpoint 188 theorem attempt failed; checkpoint 189 only refines residual diagnostics",
            "claim_allowed": "no theory promotion",
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


def decision_rows(band_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    same_all = next(
        row for row in band_rows
        if row["branch"] == "same_physical_densities_MTS_high_cs_fluid_H0_profiled" and row["band"] == "all_2_1000"
    )
    locked_all = next(
        row for row in band_rows
        if row["branch"] == "locked_Omega_m_neutrino_subtracted_MTS_high_cs_fluid_H0_profiled" and row["band"] == "all_2_1000"
    )
    return [
        {
            "decision": STATUS_READY,
            "meaning": "post-theta shape residuals are now quantified to lmax=1000; same-density branch merits matched likelihood testing, locked-Omega_m remains a pressure branch",
            "same_density_all_TT_RMS": same_all["rms_frac_delta_TT"],
            "locked_Omega_m_all_TT_RMS": locked_all["rms_frac_delta_TT"],
            "next_target": "190-CMB-matched-mock-likelihood-or-derivation-pivot.md",
            "MTS_spectra_run": "true",
            "official_likelihood_run": "false",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_189_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    params = baseline_params()
    specs = load_profiled_branch_specs(params)
    source_rows = source_register_rows()
    derivation_rows = derivation_pressure_rows()

    outputs: dict[str, dict[str, Any]] = {}
    for spec in specs:
        try:
            outputs[spec.name] = run_camb_branch(spec)
        except Exception as exc:  # pragma: no cover - CAMB runtime dependent
            outputs[spec.name] = {
                "spec": spec,
                "status": "fail",
                "elapsed_seconds": "",
                "powers": {},
                "derived": {},
                "densities": {},
                "error": f"{type(exc).__name__}: {exc}",
            }

    run_rows = branch_run_rows(outputs)
    samples = spectra_sample_rows({name: output for name, output in outputs.items() if output["status"] == "pass"})
    residuals = residual_rows({name: output for name, output in outputs.items() if output["status"] == "pass"})
    band_rows = band_summary_rows(residuals)
    readiness = readiness_rows(band_rows)
    gates = claim_gate_rows(source_rows, run_rows, band_rows)
    decision = decision_rows(band_rows)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "derivation_pressure_ledger.csv": (
            derivation_rows,
            ["object", "current_status", "derivable_now", "why_it_matters", "next_derivation_route"],
        ),
        "extended_branch_run_summary.csv": (
            run_rows,
            ["branch", "family", "model", "control_branch", "H0", "ombh2", "omch2", "Omega_m_actual", "Omega_de_actual", "thetastar", "rdrag", "DAstar", "age", "runtime_seconds", "status", "error"],
        ),
        "extended_spectra_sample_Dl.csv": (
            samples,
            ["branch", "ell", "TT_Dl_uK2", "EE_Dl_uK2", "BB_Dl_uK2", "TE_Dl_uK2", "source"],
        ),
        "extended_spectra_residuals_vs_control.csv": (
            residuals,
            ["branch", "control_branch", "family", "ell", "frac_delta_TT", "frac_delta_EE", "frac_delta_TE", "cv_sigma_frac_TT_proxy", "TT_cv_z_proxy", "EE_cv_z_proxy", "TE_cv_z_proxy", "delta_TT_Dl_uK2", "delta_EE_Dl_uK2", "delta_TE_Dl_uK2"],
        ),
        "shape_residual_band_summary.csv": (
            band_rows,
            ["branch", "control_branch", "band", "ell_min", "ell_max", "n_ell", "rms_frac_delta_TT", "max_abs_frac_delta_TT", "max_abs_frac_delta_TT_ell", "rms_frac_delta_EE", "max_abs_frac_delta_EE", "max_abs_frac_delta_EE_ell", "rms_frac_delta_TE", "rms_TT_cv_z_proxy", "rms_EE_cv_z_proxy", "proxy_interpretation"],
        ),
        "likelihood_readiness_matrix.csv": (
            readiness,
            ["readiness_item", "status", "evidence", "caveat", "next_action"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "same_density_all_TT_RMS", "locked_Omega_m_all_TT_RMS", "next_target", "MTS_spectra_run", "official_likelihood_run", "promotion_allowed", "claim_ceiling"],
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
        "lmax": LMAX_EXTENDED,
        "theta_compensation_derived": False,
        "same_density_all_TT_RMS": decision[0]["same_density_all_TT_RMS"],
        "locked_Omega_m_all_TT_RMS": decision[0]["locked_Omega_m_all_TT_RMS"],
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
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
