#!/usr/bin/env python3
"""No-CMB growth route gate for the locked B_mem=2/27 branch.

This is a conditional growth stress: the backgrounds are fixed from the no-CMB
BAO+H(z) robustness pass, then only sigma8_0 is profiled. It is not a derived
MTS perturbation theory.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import integrate, linalg, optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
DATA_ROOT = FORMALIZATION_WORKBENCH / "data" / "cosmology" / "growth_CMB"
SDSS_ROOT = DATA_ROOT / "sdss_eboss_dr16"
BAO_PLUS_ROOT = SDSS_ROOT / "BAO-plus"
FULL_SHAPE_ROOT = SDSS_ROOT / "Full-shape-only"
BACKGROUND_RUN = RUNS_ROOT / "20260531-181900-BAO-Hz-noCMB-robustness"
BACKGROUND_RESULTS = BACKGROUND_RUN / "results" / "fit_summary.csv"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402


C_KM_S = 299792.458
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
PRIMARY_MODEL = "MTS_locked_2over27"
MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
BACKGROUND_BRANCHES = {
    "DR2_noCMB_primary": "BAO_DR2_plus_CC15_suggested",
    "DR1_noCMB_release_sensitivity": "BAO_DR1_plus_CC15_suggested",
}
CLAIM_CEILING = "conditional_growth_gate_only_no_MTS_perturbation_claim"

PRIMARY_BAO_PLUS_FILES = [
    {
        "sample": "MGS",
        "vector_file": BAO_PLUS_ROOT / "sdss_MGS_FSBAO_DVfs8.txt",
        "covariance_file": BAO_PLUS_ROOT / "sdss_MGS_FSBAO_DVfs8_covtot.txt",
    },
    {
        "sample": "BOSS_DR12_LRG",
        "vector_file": BAO_PLUS_ROOT / "sdss_DR12_LRG_FSBAO_DMDHfs8.txt",
        "covariance_file": BAO_PLUS_ROOT / "sdss_DR12_LRG_FSBAO_DMDHfs8_covtot.txt",
    },
    {
        "sample": "eBOSS_DR16_LRG",
        "vector_file": BAO_PLUS_ROOT / "sdss_DR16_LRG_FSBAO_DMDHfs8.txt",
        "covariance_file": BAO_PLUS_ROOT / "sdss_DR16_LRG_FSBAO_DMDHfs8_covtot.txt",
    },
    {
        "sample": "eBOSS_DR16_QSO",
        "vector_file": BAO_PLUS_ROOT / "sdss_DR16_QSO_FSBAO_DMDHfs8.txt",
        "covariance_file": BAO_PLUS_ROOT / "sdss_DR16_QSO_FSBAO_DMDHfs8_covtot.txt",
    },
]
ROBUSTNESS_FULL_SHAPE_FILES = [
    {
        "sample": "BOSS_DR12_LRG",
        "vector_file": FULL_SHAPE_ROOT / "sdss_DR12_LRG_FS_DMDHfs8.txt",
        "covariance_file": FULL_SHAPE_ROOT / "sdss_DR12_LRG_FS_DMDHfs8_covtot.txt",
    },
    {
        "sample": "eBOSS_DR16_LRG",
        "vector_file": FULL_SHAPE_ROOT / "sdss_DR16_LRG_FS_DMDHfs8.txt",
        "covariance_file": FULL_SHAPE_ROOT / "sdss_DR16_LRG_FS_DMDHfs8_covtot.txt",
    },
    {
        "sample": "eBOSS_DR16_QSO",
        "vector_file": FULL_SHAPE_ROOT / "sdss_DR16_QSO_FS_DMDHfs8.txt",
        "covariance_file": FULL_SHAPE_ROOT / "sdss_DR16_QSO_FS_DMDHfs8_covtot.txt",
    },
]


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
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        WORK_DIR / "129-noCMB-radial-robustness-or-growth-route.md",
        BACKGROUND_RUN / "status.json",
        BACKGROUND_RESULTS,
        DATA_ROOT / "source_manifest.csv",
        SDSS_ROOT / "sdss_likelihoods_README.txt",
        BAO_PLUS_ROOT / "README.txt",
        FULL_SHAPE_ROOT / "README.txt",
        SDSS_ROOT / "row_lock_manifest.json",
        SDSS_ROOT / "covariance_validation.csv",
    ]
    for pair in [*PRIMARY_BAO_PLUS_FILES, *ROBUSTNESS_FULL_SHAPE_FILES]:
        paths.extend([pair["vector_file"], pair["covariance_file"]])
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def numeric_rows(path: Path) -> list[tuple[float, float, str]]:
    rows: list[tuple[float, float, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) >= 3:
            rows.append((float(parts[0]), float(parts[1]), parts[2]))
    return rows


def read_covariance(path: Path) -> np.ndarray:
    matrix = np.loadtxt(path)
    if matrix.ndim == 1:
        n = int(round(math.sqrt(matrix.size)))
        matrix = matrix.reshape((n, n))
    return np.asarray(matrix, dtype=float)


def covariance_chi2(residual: np.ndarray, covariance: np.ndarray) -> float:
    cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
    return float(residual @ linalg.cho_solve(cho, residual, check_finite=False))


def selected_rows_and_covariance(
    rows: list[tuple[float, float, str]],
    covariance: np.ndarray,
    mode: str,
) -> tuple[list[tuple[float, float, str]], np.ndarray, list[int]]:
    if mode == "all":
        indices = list(range(len(rows)))
    elif mode == "fs8_only":
        indices = [index for index, row in enumerate(rows) if row[2] == "f_sigma8"]
    else:
        raise ValueError(f"unsupported score mode {mode}")
    if not indices:
        raise ValueError(f"no rows available for score mode {mode}")
    sub_rows = [rows[index] for index in indices]
    sub_cov = covariance[np.ix_(indices, indices)]
    return sub_rows, sub_cov, indices


def model_key_and_params(model: str, source: dict[str, str]) -> tuple[str, dict[str, float]]:
    params: dict[str, float] = {
        "Omega_m": float(source["Omega_m0"]),
        "BAO_alpha": float(source["BAO_alpha"]),
        "h": float(source["h"]),
        "H0": float(source["H0"]),
    }
    if model == "wCDM":
        params["w"] = float(source["w"])
    elif model == "CPL":
        params["w0"] = float(source["w0"])
        params["wa"] = float(source["wa"])
    model_key = model
    if model == "MTS_locked_2over27":
        params.update({"B_mem": LOCKED_B_MEM, "p": LOCKED_P, "u3": LOCKED_U3})
        model_key = "MTS_fixed_p3_u3quarter"
    elif model == "MTS_Bmem_zero":
        params.update({"B_mem": 0.0, "p": LOCKED_P, "u3": LOCKED_U3})
    return model_key, params


def load_background_specs() -> list[dict[str, Any]]:
    rows = read_csv_rows(BACKGROUND_RESULTS)
    specs: list[dict[str, Any]] = []
    for background_branch, dataset_label in BACKGROUND_BRANCHES.items():
        for model in MODEL_ORDER:
            match = next(row for row in rows if row["dataset_label"] == dataset_label and row["model"] == model)
            model_key, params = model_key_and_params(model, match)
            h = float(match["h"])
            alpha = float(match["BAO_alpha"])
            rd_inferred = C_KM_S / (100.0 * h * alpha)
            specs.append(
                {
                    "background_branch": background_branch,
                    "source_dataset_label": dataset_label,
                    "model": model,
                    "model_key": model_key,
                    "params": params,
                    "Omega_m0": float(match["Omega_m0"]),
                    "h": h,
                    "H0": float(match["H0"]),
                    "BAO_alpha": alpha,
                    "rd_inferred_from_alpha_h": rd_inferred,
                    "w": match.get("w", ""),
                    "w0": match.get("w0", ""),
                    "wa": match.get("wa", ""),
                    "source_edge_flag": match["edge_flag"],
                    "background_source": str(BACKGROUND_RESULTS),
                }
            )
    return specs


def e2_at_a(model_key: str, params: dict[str, float], a: float) -> float:
    z = np.asarray([1.0 / a - 1.0], dtype=float)
    return float(snbao.e_z(model_key, z, params)[0] ** 2)


def growth_solution(model_key: str, params: dict[str, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x0 = math.log(1.0e-3)
    x1 = 0.0

    def deriv(x: float, y: np.ndarray) -> list[float]:
        a = math.exp(x)
        e2 = e2_at_a(model_key, params, a)
        eps = 1.0e-4
        if x + eps > 0.0:
            e2_p = e2
            e2_m = e2_at_a(model_key, params, math.exp(x - eps))
            dlnh_dlna = 0.5 * (math.log(e2_p) - math.log(e2_m)) / eps
        else:
            e2_p = e2_at_a(model_key, params, math.exp(x + eps))
            e2_m = e2_at_a(model_key, params, math.exp(x - eps))
            dlnh_dlna = 0.25 * (math.log(e2_p) - math.log(e2_m)) / eps
        omega_m_a = float(params["Omega_m"]) * a**-3 / e2
        return [float(y[1]), float(-(2.0 + dlnh_dlna) * y[1] + 1.5 * omega_m_a * y[0])]

    y0 = np.asarray([math.exp(x0), math.exp(x0)], dtype=float)
    sol = integrate.solve_ivp(deriv, (x0, x1), y0, rtol=1.0e-6, atol=1.0e-9, dense_output=False, max_step=0.02)
    if not sol.success:
        raise ValueError(sol.message)
    d_norm = sol.y[0] / sol.y[0, -1]
    f_values = sol.y[1] / sol.y[0]
    return sol.t, d_norm, f_values


def growth_fsigma8(model_key: str, params: dict[str, float], z_values: np.ndarray, sigma8_0: float) -> np.ndarray:
    x_grid, d_grid, f_grid = growth_solution(model_key, params)
    x = np.log(1.0 / (1.0 + z_values))
    d_values = np.interp(x, x_grid, d_grid)
    f_values = np.interp(x, x_grid, f_grid)
    return sigma8_0 * d_values * f_values


def prediction(model_key: str, params: dict[str, float], rows: list[tuple[float, float, str]], sigma8_0: float) -> np.ndarray:
    z_values = np.asarray([row[0] for row in rows], dtype=float)
    integral = snbao.comoving_integral(model_key, z_values, params)
    e_values = snbao.e_z(model_key, z_values, params)
    alpha = float(params["BAO_alpha"])
    growth = growth_fsigma8(model_key, params, z_values, sigma8_0)
    predicted: list[float] = []
    for index, (z, _, quantity) in enumerate(rows):
        if quantity in {"DM_over_rs", "DM_over_rd"}:
            predicted.append(float(alpha * integral[index]))
        elif quantity in {"DH_over_rs", "DH_over_rd"}:
            predicted.append(float(alpha / e_values[index]))
        elif quantity in {"DV_over_rs", "DV_over_rd"}:
            predicted.append(float(alpha * (z * integral[index] * integral[index] / e_values[index]) ** (1.0 / 3.0)))
        elif quantity == "f_sigma8":
            predicted.append(float(growth[index]))
        else:
            raise ValueError(f"unsupported quantity {quantity}")
    return np.asarray(predicted, dtype=float)


def score_file_set(
    model_key: str,
    params: dict[str, float],
    files: list[dict[str, Any]],
    sigma8_0: float,
    score_mode: str,
    residual_rows: list[dict[str, Any]],
    context: dict[str, Any],
) -> tuple[float, int]:
    total = 0.0
    n_rows = 0
    for pair_index, pair in enumerate(files, start=1):
        all_rows = numeric_rows(Path(pair["vector_file"]))
        all_covariance = read_covariance(Path(pair["covariance_file"]))
        rows, covariance, indices = selected_rows_and_covariance(all_rows, all_covariance, score_mode)
        observed = np.asarray([row[1] for row in rows], dtype=float)
        predicted = prediction(model_key, params, rows, sigma8_0)
        residual = observed - predicted
        chi2_value = covariance_chi2(residual, covariance)
        total += chi2_value
        n_rows += len(rows)
        diag_sigma = np.sqrt(np.diag(covariance))
        try:
            inv_cov = linalg.inv(covariance)
            signed = residual * (inv_cov @ residual)
        except (ValueError, linalg.LinAlgError):
            signed = np.full(len(rows), np.nan)
        for local_index, ((z, obs, quantity), pred, res, sigma, signed_value) in enumerate(
            zip(rows, predicted, residual, diag_sigma, signed, strict=True),
            start=1,
        ):
            residual_rows.append(
                {
                    **context,
                    "file_set": context["file_set"],
                    "sample": pair["sample"],
                    "pair_index": pair_index,
                    "row_index": local_index,
                    "source_row_index_0based": indices[local_index - 1],
                    "z": z,
                    "quantity": quantity,
                    "observed": obs,
                    "predicted": float(pred),
                    "residual": float(res),
                    "diagonal_sigma": float(sigma),
                    "diagonal_pull": float(res / sigma) if sigma > 0.0 else "",
                    "cov_signed_chi2_contribution": float(signed_value),
                    "sigma8_0": sigma8_0,
                }
            )
    return total, n_rows


def fit_sigma8(
    model_key: str,
    params: dict[str, float],
    files: list[dict[str, Any]],
    score_mode: str,
) -> tuple[float, float, bool]:
    def objective(value: float) -> float:
        scratch: list[dict[str, Any]] = []
        context = {
            "background_branch": "scratch",
            "source_dataset_label": "scratch",
            "model": "scratch",
            "file_set": "scratch",
            "score_mode": score_mode,
            "score_role": "scratch",
        }
        chi2_value, _ = score_file_set(model_key, params, files, float(value), score_mode, scratch, context)
        return chi2_value

    result = optimize.minimize_scalar(objective, bounds=(0.2, 1.4), method="bounded", options={"xatol": 1.0e-5})
    if not result.success:
        raise ValueError("sigma8 optimization failed")
    sigma8 = float(result.x)
    distance_to_edge = min(sigma8 - 0.2, 1.4 - sigma8)
    edge_flag = distance_to_edge <= 0.012
    return sigma8, float(result.fun), edge_flag


def data_schema_rows() -> list[dict[str, Any]]:
    rows = []
    for file_set, role, files in [
        ("primary_BAO_plus", "recommended_BAO_plus_primary", PRIMARY_BAO_PLUS_FILES),
        ("robustness_full_shape_only", "full_shape_only_sensitivity", ROBUSTNESS_FULL_SHAPE_FILES),
    ]:
        for pair in files:
            vector_rows = numeric_rows(pair["vector_file"])
            covariance = read_covariance(pair["covariance_file"])
            quantities = Counter(row[2] for row in vector_rows)
            eigenvalues = np.linalg.eigvalsh(covariance)
            rows.append(
                {
                    "file_set": file_set,
                    "role": role,
                    "sample": pair["sample"],
                    "vector_file": str(pair["vector_file"]),
                    "covariance_file": str(pair["covariance_file"]),
                    "rows": len(vector_rows),
                    "quantity_counts": json.dumps(dict(sorted(quantities.items())), sort_keys=True),
                    "covariance_shape": f"{covariance.shape[0]}x{covariance.shape[1]}",
                    "min_covariance_eigenvalue": float(np.min(eigenvalues)),
                    "covariance_condition": float(np.max(eigenvalues) / np.min(eigenvalues)),
                    "schema_status": "pass" if covariance.shape == (len(vector_rows), len(vector_rows)) and np.min(eigenvalues) > 0 else "check",
                }
            )
    return rows


def background_rows(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "background_branch": spec["background_branch"],
            "source_dataset_label": spec["source_dataset_label"],
            "model": spec["model"],
            "Omega_m0": spec["Omega_m0"],
            "h": spec["h"],
            "H0": spec["H0"],
            "BAO_alpha": spec["BAO_alpha"],
            "rd_inferred_from_alpha_h": spec["rd_inferred_from_alpha_h"],
            "w": spec["w"],
            "w0": spec["w0"],
            "wa": spec["wa"],
            "source_edge_flag": spec["source_edge_flag"],
            "background_source": spec["background_source"],
        }
        for spec in specs
    ]


def comparison_label(delta: float) -> str:
    if delta <= -2.0:
        return "locked_preferred"
    if delta < 2.0:
        return "competitive_draw"
    return "locked_disfavored"


def baseline_comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {
        (row["background_branch"], row["score_role"], row["score_mode"], row["model"]): row
        for row in fit_rows
    }
    score_keys = sorted({(row["background_branch"], row["score_role"], row["score_mode"]) for row in fit_rows})
    for background_branch, score_role, score_mode in score_keys:
        locked = by_key[(background_branch, score_role, score_mode, PRIMARY_MODEL)]
        for reference_model in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_key[(background_branch, score_role, score_mode, reference_model)]
            delta_chi2 = float(locked["chi2"]) - float(reference["chi2"])
            rows.append(
                {
                    "background_branch": background_branch,
                    "score_role": score_role,
                    "score_mode": score_mode,
                    "model": PRIMARY_MODEL,
                    "reference_model": reference_model,
                    "delta_chi2": delta_chi2,
                    "delta_AIC": float(locked["AIC"]) - float(reference["AIC"]),
                    "delta_BIC": float(locked["BIC"]) - float(reference["BIC"]),
                    "locked_sigma8_edge": locked["sigma8_edge_flag"],
                    "reference_sigma8_edge": reference["sigma8_edge_flag"],
                    "reference_background_edge": reference["source_edge_flag"],
                    "readout": comparison_label(delta_chi2),
                }
            )
    return rows


def control_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {
        (row["background_branch"], row["score_role"], row["score_mode"], row["model"]): row
        for row in fit_rows
    }
    score_keys = sorted({(row["background_branch"], row["score_role"], row["score_mode"]) for row in fit_rows})
    for background_branch, score_role, score_mode in score_keys:
        lcdm = by_key[(background_branch, score_role, score_mode, "LCDM")]
        zero = by_key[(background_branch, score_role, score_mode, "MTS_Bmem_zero")]
        delta = float(zero["chi2"]) - float(lcdm["chi2"])
        rows.append(
            {
                "background_branch": background_branch,
                "score_role": score_role,
                "score_mode": score_mode,
                "control": "MTS_Bmem_zero_vs_LCDM",
                "delta_chi2": delta,
                "delta_sigma8_0": float(zero["sigma8_0"]) - float(lcdm["sigma8_0"]),
                "status": "pass" if abs(delta) < 1.0e-8 else "check",
            }
        )
    return rows


def decision_rows(fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]], controls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary_all = next(
        row
        for row in comparisons
        if row["background_branch"] == "DR2_noCMB_primary"
        and row["score_role"] == "primary_fit"
        and row["score_mode"] == "all"
        and row["reference_model"] == "LCDM"
    )
    primary_rsd = next(
        row
        for row in comparisons
        if row["background_branch"] == "DR2_noCMB_primary"
        and row["score_role"] == "primary_fit"
        and row["score_mode"] == "fs8_only"
        and row["reference_model"] == "LCDM"
    )
    transfer_all = next(
        row
        for row in comparisons
        if row["background_branch"] == "DR2_noCMB_primary"
        and row["score_role"] == "robustness_transfer"
        and row["score_mode"] == "all"
        and row["reference_model"] == "LCDM"
    )
    locked_edges = [
        row
        for row in fit_rows
        if row["model"] == PRIMARY_MODEL and row["sigma8_edge_flag"] in [True, "True"]
    ]
    bad_controls = [row for row in controls if row["status"] != "pass"]
    if bad_controls:
        status = "growth_gate_control_failure"
    elif locked_edges:
        status = "growth_gate_locked_sigma8_edge"
    elif float(primary_all["delta_chi2"]) > 2.0 or float(primary_rsd["delta_chi2"]) > 2.0:
        status = "growth_gate_primary_tension_vs_LCDM"
    elif float(transfer_all["delta_chi2"]) > 2.0:
        status = "growth_gate_full_shape_transfer_tension_vs_LCDM"
    elif float(primary_all["delta_chi2"]) <= -2.0 and float(primary_rsd["delta_chi2"]) < 2.0:
        status = "growth_gate_locked_primary_preferred_or_draw"
    else:
        status = "growth_gate_locked_competitive_draw"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary_all_delta_vs_LCDM={float(primary_all['delta_chi2']):.12g}; primary_RSD_delta_vs_LCDM={float(primary_rsd['delta_chi2']):.12g}; transfer_all_delta_vs_LCDM={float(transfer_all['delta_chi2']):.12g}",
        },
        {
            "item": "primary_BAO_plus_all_vs_LCDM",
            "verdict": primary_all["readout"],
            "evidence": f"delta_chi2={float(primary_all['delta_chi2']):.12g}; same sigma8-only stage k for both models",
        },
        {
            "item": "primary_RSD_only_vs_LCDM",
            "verdict": primary_rsd["readout"],
            "evidence": f"delta_chi2={float(primary_rsd['delta_chi2']):.12g}; geometry rows removed",
        },
        {
            "item": "full_shape_transfer_vs_LCDM",
            "verdict": transfer_all["readout"],
            "evidence": f"delta_chi2={float(transfer_all['delta_chi2']):.12g}; sigma8 transferred from primary BAO-plus all fit",
        },
        {
            "item": "locked_sigma8_edges",
            "verdict": "clean" if not locked_edges else "edge_hit",
            "evidence": "none" if not locked_edges else ";".join(f"{row['background_branch']}:{row['score_role']}:{row['score_mode']}" for row in locked_edges),
        },
        {
            "item": "negative_control",
            "verdict": "pass" if not bad_controls else "check",
            "evidence": "MTS_Bmem_zero reproduces LCDM in all growth stages" if not bad_controls else f"{len(bad_controls)} control rows failed",
        },
        {
            "item": "claim_status",
            "verdict": "conditional_growth_gate_only",
            "evidence": "Uses GR growth equation on fixed MTS background; no derived MTS perturbation theory or CMB prior.",
        },
        {
            "item": "next_target",
            "verdict": "write_growth_readout_then_choose_growth_or_perturbation_contract",
            "evidence": "Promote only as a stress-test target unless a parent perturbation equation derives the growth law.",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-growth-route-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in source_rows if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    specs = load_background_specs()
    fit_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for spec in specs:
        for score_mode in ["all", "fs8_only"]:
            primary_sigma8, primary_chi2, primary_edge = fit_sigma8(
                spec["model_key"],
                spec["params"],
                PRIMARY_BAO_PLUS_FILES,
                score_mode,
            )
            context = {
                "background_branch": spec["background_branch"],
                "source_dataset_label": spec["source_dataset_label"],
                "model": spec["model"],
                "file_set": "primary_BAO_plus",
                "score_mode": score_mode,
                "score_role": "primary_fit",
            }
            primary_residuals: list[dict[str, Any]] = []
            primary_check_chi2, primary_n = score_file_set(
                spec["model_key"],
                spec["params"],
                PRIMARY_BAO_PLUS_FILES,
                primary_sigma8,
                score_mode,
                primary_residuals,
                context,
            )
            residual_rows.extend(primary_residuals)
            k_count = 1
            fit_rows.append(
                {
                    "background_branch": spec["background_branch"],
                    "source_dataset_label": spec["source_dataset_label"],
                    "model": spec["model"],
                    "file_set": "primary_BAO_plus",
                    "score_role": "primary_fit",
                    "score_mode": score_mode,
                    "chi2": primary_check_chi2,
                    "fit_objective_chi2": primary_chi2,
                    "n_data": primary_n,
                    "dynamic_k": k_count,
                    "AIC": primary_check_chi2 + 2.0 * k_count,
                    "BIC": primary_check_chi2 + math.log(primary_n) * k_count,
                    "sigma8_0": primary_sigma8,
                    "sigma8_edge_flag": primary_edge,
                    "Omega_m0": spec["Omega_m0"],
                    "h": spec["h"],
                    "H0": spec["H0"],
                    "BAO_alpha": spec["BAO_alpha"],
                    "rd_inferred_from_alpha_h": spec["rd_inferred_from_alpha_h"],
                    "source_edge_flag": spec["source_edge_flag"],
                    "claim_ceiling": CLAIM_CEILING,
                }
            )

            transfer_context = {
                "background_branch": spec["background_branch"],
                "source_dataset_label": spec["source_dataset_label"],
                "model": spec["model"],
                "file_set": "robustness_full_shape_only",
                "score_mode": score_mode,
                "score_role": "robustness_transfer",
            }
            transfer_residuals: list[dict[str, Any]] = []
            transfer_chi2, transfer_n = score_file_set(
                spec["model_key"],
                spec["params"],
                ROBUSTNESS_FULL_SHAPE_FILES,
                primary_sigma8,
                score_mode,
                transfer_residuals,
                transfer_context,
            )
            residual_rows.extend(transfer_residuals)
            fit_rows.append(
                {
                    "background_branch": spec["background_branch"],
                    "source_dataset_label": spec["source_dataset_label"],
                    "model": spec["model"],
                    "file_set": "robustness_full_shape_only",
                    "score_role": "robustness_transfer",
                    "score_mode": score_mode,
                    "chi2": transfer_chi2,
                    "fit_objective_chi2": "",
                    "n_data": transfer_n,
                    "dynamic_k": k_count,
                    "AIC": transfer_chi2 + 2.0 * k_count,
                    "BIC": transfer_chi2 + math.log(transfer_n) * k_count,
                    "sigma8_0": primary_sigma8,
                    "sigma8_edge_flag": primary_edge,
                    "Omega_m0": spec["Omega_m0"],
                    "h": spec["h"],
                    "H0": spec["H0"],
                    "BAO_alpha": spec["BAO_alpha"],
                    "rd_inferred_from_alpha_h": spec["rd_inferred_from_alpha_h"],
                    "source_edge_flag": spec["source_edge_flag"],
                    "claim_ceiling": CLAIM_CEILING,
                }
            )

    comparisons = baseline_comparison_rows(fit_rows)
    controls = control_rows(fit_rows)
    decisions = decision_rows(fit_rows, comparisons, controls)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_schema.csv",
        data_schema_rows(),
        [
            "file_set",
            "role",
            "sample",
            "vector_file",
            "covariance_file",
            "rows",
            "quantity_counts",
            "covariance_shape",
            "min_covariance_eigenvalue",
            "covariance_condition",
            "schema_status",
        ],
    )
    write_csv(
        results_dir / "background_params.csv",
        background_rows(specs),
        [
            "background_branch",
            "source_dataset_label",
            "model",
            "Omega_m0",
            "h",
            "H0",
            "BAO_alpha",
            "rd_inferred_from_alpha_h",
            "w",
            "w0",
            "wa",
            "source_edge_flag",
            "background_source",
        ],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "background_branch",
            "source_dataset_label",
            "model",
            "file_set",
            "score_role",
            "score_mode",
            "chi2",
            "fit_objective_chi2",
            "n_data",
            "dynamic_k",
            "AIC",
            "BIC",
            "sigma8_0",
            "sigma8_edge_flag",
            "Omega_m0",
            "h",
            "H0",
            "BAO_alpha",
            "rd_inferred_from_alpha_h",
            "source_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "background_branch",
            "score_role",
            "score_mode",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_sigma8_edge",
            "reference_sigma8_edge",
            "reference_background_edge",
            "readout",
        ],
    )
    write_csv(
        results_dir / "control_reproduction.csv",
        controls,
        ["background_branch", "score_role", "score_mode", "control", "delta_chi2", "delta_sigma8_0", "status"],
    )
    write_csv(
        results_dir / "residuals.csv",
        residual_rows,
        [
            "background_branch",
            "source_dataset_label",
            "model",
            "file_set",
            "score_mode",
            "score_role",
            "sample",
            "pair_index",
            "row_index",
            "source_row_index_0based",
            "z",
            "quantity",
            "observed",
            "predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
            "sigma8_0",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "background_run": str(BACKGROUND_RUN),
        "models": MODEL_ORDER,
        "fit_rows": len(fit_rows),
        "generated": [
            "source_register.csv",
            "data_schema.csv",
            "background_params.csv",
            "fit_summary.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "residuals.csv",
            "decision.csv",
        ],
        "next_target": "130-growth-route-gate.md",
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
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
