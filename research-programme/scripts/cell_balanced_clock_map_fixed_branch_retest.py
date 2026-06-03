#!/usr/bin/env python3
"""Retest the fixed cell-balanced clock map against SN, BAO, and H(z)."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import integrate, linalg, optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
ROOT = WORK_DIR.parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import Hz_radial_expansion_smoke as hzsmoke  # noqa: E402


SN_BAO_REFERENCE_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
HZ_REFERENCE_RUN = RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout"
CELL_CLOCK_RUN = RUNS_ROOT / "20260531-235959-clock-projection-functional-theorem-or-demotion"

B_MEM = 2.0 / 27.0
U3_FIT = 0.2429466120286312
U3_QUARTER = 0.25
KAPPA_4 = 1.0 / 24.0
CLAIM_CEILING = "fixed_cell_clock_retest_no_bridge_promotion"


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


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("156-") or "clock-projection-functional" in str(path):
        return "cell-balanced clock theorem target"
    if name.startswith("155-"):
        return "redshift clock target"
    if "cosmo-SN-BAO" in str(path) or name == "run_config.json":
        return "SN+BAO reference run/data contract"
    if "fresh-CC-Hz" in str(path) or name.startswith("Hz") or name.startswith("covariance"):
        return "H(z) reference/source-locked data"
    if name.endswith(".py"):
        return "machine auditor"
    if "Pantheon" in name or "desi" in name.lower():
        return "empirical data"
    return "supporting source"


def source_register_rows(script_path: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "155-redshift-projection-clock-map-owner.md",
        WORK_DIR / "156-clock-projection-functional-theorem-or-demotion.md",
        CELL_CLOCK_RUN / "results" / "decision.csv",
        CELL_CLOCK_RUN / "results" / "cell_balance_candidate_scorecard.csv",
        SN_BAO_REFERENCE_RUN / "run_config.json",
        SN_BAO_REFERENCE_RUN / "results" / "fit_summary.csv",
        SN_BAO_REFERENCE_RUN / "results" / "baseline_comparison.csv",
        Path(config["sn_data"]),
        Path(config["sn_cov"]),
        Path(config["bao_data"]),
        Path(config["bao_cov"]),
        HZ_REFERENCE_RUN / "results" / "fit_summary.csv",
        HZ_REFERENCE_RUN / "results" / "baseline_comparisons.csv",
        hzsmoke.HZ_15,
        hzsmoke.HZ_32,
        *hzsmoke.COVARIANCE_FILES.values(),
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def load_reference_config() -> dict[str, Any]:
    return json.loads((SN_BAO_REFERENCE_RUN / "run_config.json").read_text(encoding="utf-8"))


def branch_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "LCDM",
            "sector": "baseline",
            "clock_map": "off",
            "fixed_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "wCDM",
            "sector": "baseline",
            "clock_map": "off",
            "fixed_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m,w + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m,h,w",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "CPL",
            "sector": "baseline",
            "clock_map": "off",
            "fixed_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m,w0,wa + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m,h,w0,wa",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "MTS_2over27_no_clock_u3fit",
            "sector": "control",
            "clock_map": "off",
            "fixed_parameters": f"B_mem={B_MEM}; p=3; u3={U3_FIT}",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "fixed_background_control_only",
        },
        {
            "branch": "MTS_2over27_no_clock_u3quarter",
            "sector": "control",
            "clock_map": "off",
            "fixed_parameters": f"B_mem={B_MEM}; p=3; u3={U3_QUARTER}",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "fixed_background_control_only",
        },
        {
            "branch": "MTS_cell_clock_u3fit",
            "sector": "primary_clock_branch",
            "clock_map": "Theta=B_mem*(1/24)*X*F*(1-X/4)",
            "fixed_parameters": f"B_mem={B_MEM}; p=3; u3={U3_FIT}; kappa=1/24",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": CLAIM_CEILING,
        },
        {
            "branch": "MTS_cell_clock_u3quarter",
            "sector": "fixed_quarter_clock_branch",
            "clock_map": "Theta=B_mem*(1/24)*X*F*(1-X/4)",
            "fixed_parameters": f"B_mem={B_MEM}; p=3; u3={U3_QUARTER}; kappa=1/24",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": CLAIM_CEILING,
        },
    ]


def branch_u3(branch: str) -> float:
    if branch.endswith("u3fit"):
        return U3_FIT
    return U3_QUARTER


def is_mts(branch: str) -> bool:
    return branch.startswith("MTS_")


def has_clock(branch: str) -> bool:
    return branch.startswith("MTS_cell_clock")


def model_bounds(branch: str, include_h: bool = False) -> dict[str, tuple[float, float]]:
    bounds: dict[str, tuple[float, float]] = {"Omega_m": (0.05, 0.60)}
    if include_h:
        bounds["h"] = (0.45, 0.90)
    if branch == "wCDM":
        bounds["w"] = (-2.0, -0.2)
    if branch == "CPL":
        bounds["w0"] = (-2.0, -0.2)
        bounds["wa"] = (-2.0, 2.0)
    return bounds


def activation_x(x: np.ndarray) -> np.ndarray:
    return 1.0 - np.exp(-(x**3))


def cell_clock_map(branch: str, z_obs: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    z_obs = np.asarray(z_obs, dtype=float)
    if not has_clock(branch):
        zeros = np.zeros_like(z_obs)
        return z_obs, np.ones_like(z_obs), zeros, zeros
    u3 = branch_u3(branch)
    n_load = np.log1p(z_obs)
    x = n_load / u3
    f_value = activation_x(x)
    theta = B_MEM * KAPPA_4 * x * f_value * (1.0 - x / 4.0)
    f_prime = 3.0 * x * x * np.exp(-(x**3))
    dtheta_dx = B_MEM * KAPPA_4 * (
        f_value * (1.0 - x / 4.0)
        + x * f_prime * (1.0 - x / 4.0)
        - x * f_value / 4.0
    )
    dtheta_dz = dtheta_dx / (u3 * (1.0 + z_obs))
    zeta = -(1.0 + z_obs) * theta
    dzeta_dz = -theta - (1.0 + z_obs) * dtheta_dz
    z_prime = 1.0 + dzeta_dz
    z_true = z_obs + zeta
    if np.any(z_true <= 0.0) or np.any(z_prime <= 0.0):
        raise ValueError("clock map produced non-positive z_true or dz_true/dz_obs")
    return z_true, z_prime, theta, zeta


def e_z_branch(branch: str, z_true: np.ndarray, values: dict[str, float]) -> np.ndarray:
    omega_m = values["Omega_m"]
    if branch == "LCDM":
        return snbao.e_z("LCDM", z_true, {"Omega_m": omega_m})
    if branch == "wCDM":
        return snbao.e_z("wCDM", z_true, {"Omega_m": omega_m, "w": values["w"]})
    if branch == "CPL":
        return snbao.e_z("CPL", z_true, {"Omega_m": omega_m, "w0": values["w0"], "wa": values["wa"]})
    if is_mts(branch):
        return snbao.e_z(
            "MTS_fixed_p3_u3quarter",
            z_true,
            {"Omega_m": omega_m, "B_mem": B_MEM, "p": 3.0, "u3": branch_u3(branch)},
        )
    raise ValueError(f"unknown branch {branch}")


def comoving_integral_branch(branch: str, z_eval: np.ndarray, values: dict[str, float]) -> np.ndarray:
    z_arr = np.asarray(z_eval, dtype=float)
    z_max = float(np.max(z_arr))
    if z_max <= 0.0:
        return np.zeros_like(z_arr)
    grid_size = max(512, min(4096, int(512 + 192 * z_max)))
    grid = np.linspace(0.0, z_max, grid_size)
    inv_e = 1.0 / e_z_branch(branch, grid, values)
    cumulative = integrate.cumulative_trapezoid(inv_e, grid, initial=0.0)
    return np.interp(z_arr, grid, cumulative)


def sn_chi2_branch(branch: str, values: dict[str, float], sn: dict[str, Any], sn_policy: str) -> tuple[float, float, np.ndarray, np.ndarray]:
    z_obs = np.asarray(sn["z"], dtype=float)
    z_true, _, _, _ = cell_clock_map(branch, z_obs)
    integral = comoving_integral_branch(branch, z_true, values)
    redshift_factor = 1.0 + (z_true if sn_policy == "true_redshift_Etherington" else z_obs)
    dl_shape = np.maximum(redshift_factor * integral, 1.0e-12)
    mu_shape = 5.0 * np.log10(dl_shape)
    if sn.get("covariance_mode") == "full":
        chi2, offset, residual = snbao.analytic_offset_chi2_covariance(sn["mu"], mu_shape, sn["inv_covariance"])
    else:
        chi2, offset, residual = snbao.analytic_offset_chi2(sn["mu"], mu_shape, sn["sigma"])
    return chi2, offset, residual, mu_shape + offset


def bao_prediction_branch(branch: str, values: dict[str, float], bao: dict[str, Any], alpha: float) -> np.ndarray:
    z_obs = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    z_true, z_prime, _, _ = cell_clock_map(branch, z_obs)
    integral = comoving_integral_branch(branch, z_true, values)
    ez = e_z_branch(branch, z_true, values)
    predictions: list[float] = []
    for row, z_value, dm, e_value, radial_factor in zip(bao["rows"], z_obs, integral, ez, z_prime, strict=True):
        quantity = row["quantity"]
        if quantity == "DM_over_rs":
            predictions.append(alpha * float(dm))
        elif quantity == "DH_over_rs":
            predictions.append(alpha * float(radial_factor / e_value))
        elif quantity == "DV_over_rs":
            predictions.append(alpha * float((z_value * dm * dm * radial_factor / e_value) ** (1.0 / 3.0)))
        else:
            raise ValueError(f"unsupported BAO quantity {quantity}")
    return np.asarray(predictions, dtype=float)


def bao_chi2_branch(branch: str, values: dict[str, float], bao: dict[str, Any]) -> tuple[float, float, np.ndarray, np.ndarray]:
    observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
    covariance = np.asarray(bao["covariance"], dtype=float)
    inv_cov = linalg.inv(covariance)
    unit_pred = bao_prediction_branch(branch, values, bao, alpha=1.0)
    alpha = float((unit_pred @ inv_cov @ observed) / (unit_pred @ inv_cov @ unit_pred))
    predicted = alpha * unit_pred
    residual = observed - predicted
    chi2 = float(residual @ inv_cov @ residual)
    return chi2, alpha, residual, predicted


def edge_rows(branch: str, values: dict[str, float], bounds: dict[str, tuple[float, float]], dataset: str) -> list[dict[str, Any]]:
    rows = []
    for name, (lower, upper) in bounds.items():
        best = values[name]
        width = upper - lower
        distance = min(best - lower, upper - best)
        rows.append(
            {
                "dataset": dataset,
                "branch": branch,
                "parameter": name,
                "best_fit": best,
                "lower": lower,
                "upper": upper,
                "distance_to_edge": distance,
                "edge_flag": bool(distance <= 0.01 * width),
            }
        )
    return rows


def seed_vectors(names: list[str], bounds: list[tuple[float, float]]) -> list[np.ndarray]:
    defaults = {"Omega_m": 0.30, "h": 0.68, "w": -1.0, "w0": -1.0, "wa": 0.0}
    seed_dicts = [
        defaults,
        {**defaults, "Omega_m": 0.25, "h": 0.72},
        {**defaults, "Omega_m": 0.35, "h": 0.65},
        {**defaults, "Omega_m": 0.45, "h": 0.60},
        {**defaults, "w": -0.8, "w0": -0.8, "wa": 0.5},
        {**defaults, "w": -1.2, "w0": -1.2, "wa": -0.5},
    ]
    vectors: list[np.ndarray] = []
    for seed in seed_dicts:
        vector = np.asarray(
            [min(max(seed.get(name, 0.5 * (lower + upper)), lower), upper) for name, (lower, upper) in zip(names, bounds, strict=True)],
            dtype=float,
        )
        if not any(np.allclose(vector, previous) for previous in vectors):
            vectors.append(vector)
    midpoint = np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)
    if not any(np.allclose(midpoint, previous) for previous in vectors):
        vectors.append(midpoint)
    return vectors


def fit_sn_bao_branch(
    branch: str,
    sn: dict[str, Any],
    bao: dict[str, Any],
    sn_policy: str,
    max_iter: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    bounds_by_name = model_bounds(branch, include_h=False)
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]

    def unpack(vector: np.ndarray) -> dict[str, float]:
        return {name: float(value) for name, value in zip(names, vector, strict=True)}

    def objective(vector: np.ndarray) -> float:
        try:
            values = unpack(vector)
            chi2_sn, _, _, _ = sn_chi2_branch(branch, values, sn, sn_policy)
            chi2_bao, _, _, _ = bao_chi2_branch(branch, values, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    results = [
        optimize.minimize(
            objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-9},
        )
        for seed in seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    chi2_sn, sn_offset, sn_residual, sn_predicted = sn_chi2_branch(branch, values, sn, sn_policy)
    chi2_bao, bao_alpha, bao_residual, bao_predicted = bao_chi2_branch(branch, values, bao)
    chi2_total = chi2_sn + chi2_bao
    n_points = int(len(sn["z"]) + len(bao["rows"]))
    dynamic_k = len(names) + 2
    aic = chi2_total + 2.0 * dynamic_k
    bic = chi2_total + dynamic_k * math.log(n_points)
    edge = edge_rows(branch, values, bounds_by_name, "SN_BAO")
    row = {
        "dataset": "SN_BAO",
        "sn_policy": sn_policy,
        "branch": branch,
        "success": bool(result.success),
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "AIC": aic,
        "BIC": bic,
        "n_data": n_points,
        "dynamic_k": dynamic_k,
        "dof": n_points - dynamic_k,
        "edge_flag": any(item["edge_flag"] for item in edge),
        "Omega_m": values["Omega_m"],
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "u3": branch_u3(branch) if is_mts(branch) else "",
        "clock_map": has_clock(branch),
        "optimizer_message": str(result.message),
        "claim_ceiling": "baseline" if not is_mts(branch) else CLAIM_CEILING,
    }
    return row, edge, sn_residual, sn_predicted, bao_residual, bao_predicted


def h_prediction_branch(branch: str, values: dict[str, float], z_obs: np.ndarray) -> np.ndarray:
    z_true, z_prime, _, _ = cell_clock_map(branch, z_obs)
    ez = e_z_branch(branch, z_true, values)
    if has_clock(branch):
        correction = (1.0 + z_true) / (1.0 + z_obs) / z_prime
    else:
        correction = np.ones_like(z_obs)
    return 100.0 * values["h"] * ez * correction


def fit_hz_branch(
    branch: str,
    dataset: dict[str, Any],
    max_iter: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], np.ndarray, np.ndarray]:
    bounds_by_name = model_bounds(branch, include_h=True)
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]

    def unpack(vector: np.ndarray) -> dict[str, float]:
        return {name: float(value) for name, value in zip(names, vector, strict=True)}

    def objective(vector: np.ndarray) -> float:
        try:
            values = unpack(vector)
            predicted = h_prediction_branch(branch, values, dataset["z"])
            residual = dataset["H"] - predicted
            inv_cov = np.linalg.inv(dataset["covariance"])
            return float(residual @ inv_cov @ residual)
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return 1.0e30

    results = [
        optimize.minimize(
            objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-10},
        )
        for seed in seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    predicted = h_prediction_branch(branch, values, dataset["z"])
    residual = dataset["H"] - predicted
    inv_cov = np.linalg.inv(dataset["covariance"])
    chi2 = float(residual @ inv_cov @ residual)
    dynamic_k = len(names)
    n_data = len(dataset["z"])
    edge = edge_rows(branch, values, bounds_by_name, dataset["dataset_label"])
    row = {
        "dataset_label": dataset["dataset_label"],
        "dataset_role": dataset["role"],
        "covariance_label": dataset["covariance_label"],
        "branch": branch,
        "success": bool(result.success),
        "chi2": chi2,
        "AIC": chi2 + 2.0 * dynamic_k,
        "BIC": chi2 + dynamic_k * math.log(n_data),
        "n_data": n_data,
        "dynamic_k": dynamic_k,
        "dof": n_data - dynamic_k,
        "edge_flag": any(item["edge_flag"] for item in edge),
        "Omega_m": values["Omega_m"],
        "h": values["h"],
        "H0": 100.0 * values["h"],
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "u3": branch_u3(branch) if is_mts(branch) else "",
        "clock_map": has_clock(branch),
        "optimizer_message": str(result.message),
        "claim_ceiling": "baseline" if not is_mts(branch) else CLAIM_CEILING,
    }
    return row, edge, residual, predicted


def comparison_label(delta_bic: float) -> str:
    if delta_bic <= -2.0:
        return "branch_preferred_by_BIC"
    if delta_bic < 2.0:
        return "competitive_draw_by_BIC"
    return "branch_disfavored_by_BIC"


def comparison_rows(fit_rows: list[dict[str, Any]], dataset_key: str, branch_field: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_dataset_branch = {(row[dataset_key], row[branch_field]): row for row in fit_rows}
    datasets = sorted({row[dataset_key] for row in fit_rows})
    targets = [
        "MTS_2over27_no_clock_u3fit",
        "MTS_2over27_no_clock_u3quarter",
        "MTS_cell_clock_u3fit",
        "MTS_cell_clock_u3quarter",
    ]
    references = ["LCDM", "wCDM", "CPL"]
    for dataset in datasets:
        for target in targets:
            if (dataset, target) not in by_dataset_branch:
                continue
            target_row = by_dataset_branch[(dataset, target)]
            for reference in references:
                reference_row = by_dataset_branch[(dataset, reference)]
                rows.append(
                    {
                        dataset_key: dataset,
                        "branch": target,
                        "reference_branch": reference,
                        "delta_chi2": float(target_row.get("chi2_total", target_row.get("chi2"))) - float(reference_row.get("chi2_total", reference_row.get("chi2"))),
                        "delta_AIC": float(target_row["AIC"]) - float(reference_row["AIC"]),
                        "delta_BIC": float(target_row["BIC"]) - float(reference_row["BIC"]),
                        "branch_edge_flag": target_row["edge_flag"],
                        "reference_edge_flag": reference_row["edge_flag"],
                        "readout": comparison_label(float(target_row["BIC"]) - float(reference_row["BIC"])),
                    }
                )
    return rows


def bao_residual_rows(bao: dict[str, Any], fit_rows: list[dict[str, Any]], residuals: dict[str, np.ndarray], predictions: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    covariance = np.asarray(bao["covariance"], dtype=float)
    inv_cov = np.linalg.inv(covariance)
    sigma = np.sqrt(np.diag(covariance))
    rows: list[dict[str, Any]] = []
    for fit in fit_rows:
        branch = fit["branch"]
        residual = residuals[branch]
        predicted = predictions[branch]
        signed = residual * (inv_cov @ residual)
        for index, (bao_row, pred, res, diag_sigma, contrib) in enumerate(zip(bao["rows"], predicted, residual, sigma, signed, strict=True)):
            rows.append(
                {
                    "branch": branch,
                    "row_index": index,
                    "z": bao_row["z"],
                    "observable": bao_row["quantity"],
                    "observed": bao_row["value"],
                    "predicted": pred,
                    "residual": res,
                    "diagonal_sigma": diag_sigma,
                    "diagonal_pull": res / diag_sigma,
                    "cov_signed_chi2_contribution": contrib,
                }
            )
    return rows


def sn_residual_summary_rows(sn: dict[str, Any], fit_rows: list[dict[str, Any]], residuals: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    sigma = np.sqrt(np.diag(sn["covariance"])) if sn.get("covariance_mode") == "full" else sn["sigma"]
    rows = []
    for fit in fit_rows:
        branch = fit["branch"]
        residual = residuals[branch]
        pulls = residual / sigma
        rows.append(
            {
                "branch": branch,
                "sn_policy": fit["sn_policy"],
                "rows": len(residual),
                "mean_residual": float(np.mean(residual)),
                "rms_residual": float(np.sqrt(np.mean(residual * residual))),
                "max_abs_residual": float(np.max(np.abs(residual))),
                "rms_diagonal_pull": float(np.sqrt(np.mean(pulls * pulls))),
                "max_abs_diagonal_pull": float(np.max(np.abs(pulls))),
            }
        )
    return rows


def hz_residual_rows(datasets: list[dict[str, Any]], fit_rows: list[dict[str, Any]], residuals: dict[tuple[str, str], np.ndarray], predictions: dict[tuple[str, str], np.ndarray]) -> list[dict[str, Any]]:
    dataset_by_label = {dataset["dataset_label"]: dataset for dataset in datasets}
    rows = []
    for fit in fit_rows:
        dataset = dataset_by_label[fit["dataset_label"]]
        key = (fit["dataset_label"], fit["branch"])
        residual = residuals[key]
        predicted = predictions[key]
        sigma = np.sqrt(np.diag(dataset["covariance"]))
        inv_cov = np.linalg.inv(dataset["covariance"])
        signed = residual * (inv_cov @ residual)
        for index, (z_value, obs, pred, res, diag_sigma, contrib) in enumerate(
            zip(dataset["z"], dataset["H"], predicted, residual, sigma, signed, strict=True)
        ):
            rows.append(
                {
                    "dataset_label": fit["dataset_label"],
                    "branch": fit["branch"],
                    "row_index": index,
                    "z": z_value,
                    "H_observed": obs,
                    "H_predicted": pred,
                    "residual": res,
                    "diagonal_sigma": diag_sigma,
                    "diagonal_pull": res / diag_sigma,
                    "cov_signed_chi2_contribution": contrib,
                }
            )
    return rows


def gate_rows(
    sn_bao_rows: list[dict[str, Any]],
    sn_bao_comparisons: list[dict[str, Any]],
    hz_rows: list[dict[str, Any]],
    hz_comparisons: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    primary_clock = next(row for row in sn_bao_rows if row["branch"] == "MTS_cell_clock_u3fit")
    quarter_clock = next(row for row in sn_bao_rows if row["branch"] == "MTS_cell_clock_u3quarter")
    sn_bao_bad = [
        row
        for row in sn_bao_comparisons
        if row["branch"].startswith("MTS_cell_clock") and row["reference_branch"] == "LCDM" and float(row["delta_BIC"]) > 2.0
    ]
    hz_primary_comparisons = [
        row
        for row in hz_comparisons
        if row["dataset_label"] in {"CC15_suggested_primary"} and row["branch"].startswith("MTS_cell_clock")
    ]
    hz_bad = [row for row in hz_primary_comparisons if row["reference_branch"] == "LCDM" and float(row["delta_BIC"]) > 2.0]
    nonconverged = [row["branch"] for row in sn_bao_rows if str(row["success"]) != "True"] + [
        f"{row['dataset_label']}:{row['branch']}" for row in hz_rows if str(row["success"]) != "True"
    ]
    edge_flags = [row["branch"] for row in sn_bao_rows if row["edge_flag"] in {True, "True"} and row["branch"].startswith("MTS_cell_clock")]
    return [
        {
            "gate": "same_data_same_nuisance",
            "status": "pass",
            "evidence": "SN+BAO uses reference Pantheon+/DESI rows; H(z) uses same CC datasets/covariances as baselines",
        },
        {
            "gate": "no_extra_clock_freedom",
            "status": "pass",
            "evidence": "clock branches fit only Omega_m plus standard nuisance; B_mem,u3,kappa are fixed per branch",
        },
        {
            "gate": "convergence",
            "status": "pass" if not nonconverged else "warn",
            "evidence": "all fitted branches converged" if not nonconverged else ";".join(nonconverged),
        },
        {
            "gate": "SN_BAO_primary_clock_u3fit",
            "status": "pass_draw_or_better" if not sn_bao_bad else "fail_disfavored_vs_LCDM",
            "evidence": f"u3fit chi2_total={primary_clock['chi2_total']}; BIC={primary_clock['BIC']}",
        },
        {
            "gate": "SN_BAO_quarter_clock",
            "status": "pass_draw_or_better" if float(quarter_clock["BIC"]) - float(next(row for row in sn_bao_rows if row["branch"] == "LCDM")["BIC"]) < 2.0 else "fail_disfavored_vs_LCDM",
            "evidence": f"quarter chi2_total={quarter_clock['chi2_total']}; BIC={quarter_clock['BIC']}",
        },
        {
            "gate": "Hz_primary_clock",
            "status": "pass_draw_or_better" if not hz_bad else "fail_disfavored_vs_LCDM",
            "evidence": "primary H(z) clock branches are not BIC-disfavored vs LCDM" if not hz_bad else str(hz_bad),
        },
        {
            "gate": "prior_edge_safety",
            "status": "pass" if not edge_flags else "warn",
            "evidence": "clock branches not edge-flagged" if not edge_flags else ";".join(edge_flags),
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(sn_bao_comparisons: list[dict[str, Any]], hz_comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def comparison(dataset_key: str, rows: list[dict[str, Any]], branch: str, reference: str, dataset_value: str = "SN_BAO") -> dict[str, Any]:
        return next(row for row in rows if row[dataset_key] == dataset_value and row["branch"] == branch and row["reference_branch"] == reference)

    u3fit_lcdm = comparison("dataset", sn_bao_comparisons, "MTS_cell_clock_u3fit", "LCDM")
    u3fit_wc = comparison("dataset", sn_bao_comparisons, "MTS_cell_clock_u3fit", "wCDM")
    quarter_lcdm = comparison("dataset", sn_bao_comparisons, "MTS_cell_clock_u3quarter", "LCDM")
    primary_hz_lcdm = comparison("dataset_label", hz_comparisons, "MTS_cell_clock_u3fit", "LCDM", "CC15_suggested_primary")
    if float(u3fit_lcdm["delta_BIC"]) < 2.0 and float(primary_hz_lcdm["delta_BIC"]) < 2.0:
        status = "fixed_cell_clock_branch_survives_first_SN_BAO_Hz_retest"
    elif float(quarter_lcdm["delta_BIC"]) < 2.0 and float(primary_hz_lcdm["delta_BIC"]) < 2.0:
        status = "fixed_cell_clock_mixed_retest_quarter_survives_u3fit_rework"
    else:
        status = "fixed_cell_clock_branch_demote_or_rework_after_retest"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"SN+BAO u3fit delta_BIC_vs_LCDM={u3fit_lcdm['delta_BIC']}; H(z) primary delta_BIC_vs_LCDM={primary_hz_lcdm['delta_BIC']}",
        },
        {
            "item": "u3fit_vs_LCDM",
            "verdict": u3fit_lcdm["readout"],
            "evidence": f"SN+BAO delta_chi2={u3fit_lcdm['delta_chi2']}; delta_BIC={u3fit_lcdm['delta_BIC']}",
        },
        {
            "item": "u3fit_vs_wCDM",
            "verdict": u3fit_wc["readout"],
            "evidence": f"SN+BAO delta_chi2={u3fit_wc['delta_chi2']}; delta_BIC={u3fit_wc['delta_BIC']}",
        },
        {
            "item": "quarter_vs_LCDM",
            "verdict": quarter_lcdm["readout"],
            "evidence": f"SN+BAO delta_chi2={quarter_lcdm['delta_chi2']}; delta_BIC={quarter_lcdm['delta_BIC']}",
        },
        {
            "item": "Hz_primary_vs_LCDM",
            "verdict": primary_hz_lcdm["readout"],
            "evidence": f"H(z) delta_chi2={primary_hz_lcdm['delta_chi2']}; delta_BIC={primary_hz_lcdm['delta_BIC']}",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "fixed branch empirical stress only; no parent action/gauge/CMB/local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md",
            "evidence": "inspect whether gains/losses are radial BAO, transverse BAO, SN offset, or chronometer derivative-map pressure",
        },
    ]


def run_retest(output_root: Path, timestamp: str | None, max_iter: int, sn_policy: str) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-cell-balanced-clock-map-fixed-branch-retest"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    config = load_reference_config()
    sources = source_register_rows(Path(__file__).resolve(), config)
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    sn = snbao.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config.get("sn_max_rows"),
        covariance_path=Path(config["sn_cov"]),
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = snbao.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    bao["label"] = config.get("bao_label", "DESI_DR2_primary")

    branches = ["LCDM", "wCDM", "CPL", "MTS_2over27_no_clock_u3fit", "MTS_2over27_no_clock_u3quarter", "MTS_cell_clock_u3fit", "MTS_cell_clock_u3quarter"]
    sn_bao_rows: list[dict[str, Any]] = []
    sn_bao_edges: list[dict[str, Any]] = []
    sn_residuals: dict[str, np.ndarray] = {}
    bao_residuals: dict[str, np.ndarray] = {}
    bao_predictions: dict[str, np.ndarray] = {}
    for branch in branches:
        fit, edge, sn_residual, _, bao_residual, bao_predicted = fit_sn_bao_branch(branch, sn, bao, sn_policy, max_iter)
        sn_bao_rows.append(fit)
        sn_bao_edges.extend(edge)
        sn_residuals[branch] = sn_residual
        bao_residuals[branch] = bao_residual
        bao_predictions[branch] = bao_predicted

    hz_datasets = hzsmoke.datasets_to_score()
    hz_rows: list[dict[str, Any]] = []
    hz_edges: list[dict[str, Any]] = []
    hz_residuals: dict[tuple[str, str], np.ndarray] = {}
    hz_predictions: dict[tuple[str, str], np.ndarray] = {}
    for dataset in hz_datasets:
        for branch in branches:
            fit, edge, residual, predicted = fit_hz_branch(branch, dataset, max_iter)
            hz_rows.append(fit)
            hz_edges.extend(edge)
            hz_residuals[(dataset["dataset_label"], branch)] = residual
            hz_predictions[(dataset["dataset_label"], branch)] = predicted

    sn_bao_comparisons = comparison_rows(sn_bao_rows, "dataset", "branch")
    hz_comparisons = comparison_rows(hz_rows, "dataset_label", "branch")
    gates = gate_rows(sn_bao_rows, sn_bao_comparisons, hz_rows, hz_comparisons)
    decisions = decision_rows(sn_bao_comparisons, hz_comparisons)

    run_config = {
        "timestamp": run_stamp,
        "claim_ceiling": CLAIM_CEILING,
        "reference_SN_BAO_run": str(SN_BAO_REFERENCE_RUN),
        "reference_Hz_run": str(HZ_REFERENCE_RUN),
        "sn_policy": sn_policy,
        "max_iter": max_iter,
        "branches": branch_contract_rows(),
        "sn_rows": int(len(sn["z"])),
        "bao_rows": int(len(bao["rows"])),
        "hz_datasets": [dataset["dataset_label"] for dataset in hz_datasets],
    }
    write_json(run_dir / "run_config.json", run_config)
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "branch_contract.csv",
        branch_contract_rows(),
        ["branch", "sector", "clock_map", "fixed_parameters", "fitted_parameters_SN_BAO", "fitted_parameters_Hz", "claim_ceiling"],
    )
    write_csv(
        results_dir / "sn_bao_fit_summary.csv",
        sn_bao_rows,
        [
            "dataset",
            "sn_policy",
            "branch",
            "success",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "dof",
            "edge_flag",
            "Omega_m",
            "w",
            "w0",
            "wa",
            "sn_offset",
            "bao_alpha",
            "u3",
            "clock_map",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "sn_bao_prior_edges.csv", sn_bao_edges, ["dataset", "branch", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(
        results_dir / "sn_bao_baseline_comparison.csv",
        sn_bao_comparisons,
        ["dataset", "branch", "reference_branch", "delta_chi2", "delta_AIC", "delta_BIC", "branch_edge_flag", "reference_edge_flag", "readout"],
    )
    write_csv(
        results_dir / "bao_residuals.csv",
        bao_residual_rows(bao, sn_bao_rows, bao_residuals, bao_predictions),
        ["branch", "row_index", "z", "observable", "observed", "predicted", "residual", "diagonal_sigma", "diagonal_pull", "cov_signed_chi2_contribution"],
    )
    write_csv(
        results_dir / "sn_residual_summary.csv",
        sn_residual_summary_rows(sn, sn_bao_rows, sn_residuals),
        ["branch", "sn_policy", "rows", "mean_residual", "rms_residual", "max_abs_residual", "rms_diagonal_pull", "max_abs_diagonal_pull"],
    )
    write_csv(
        results_dir / "hz_fit_summary.csv",
        hz_rows,
        [
            "dataset_label",
            "dataset_role",
            "covariance_label",
            "branch",
            "success",
            "chi2",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "dof",
            "edge_flag",
            "Omega_m",
            "h",
            "H0",
            "w",
            "w0",
            "wa",
            "u3",
            "clock_map",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "hz_prior_edges.csv", hz_edges, ["dataset", "branch", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(
        results_dir / "hz_baseline_comparison.csv",
        hz_comparisons,
        ["dataset_label", "branch", "reference_branch", "delta_chi2", "delta_AIC", "delta_BIC", "branch_edge_flag", "reference_edge_flag", "readout"],
    )
    write_csv(
        results_dir / "hz_residuals.csv",
        hz_residual_rows(hz_datasets, hz_rows, hz_residuals, hz_predictions),
        ["dataset_label", "branch", "row_index", "z", "H_observed", "H_predicted", "residual", "diagonal_sigma", "diagonal_pull", "cov_signed_chi2_contribution"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "sn_policy": sn_policy,
        "sn_rows": int(len(sn["z"])),
        "bao_rows": int(len(bao["rows"])),
        "hz_fit_rows": len(hz_rows),
        "generated": [
            "source_register.csv",
            "branch_contract.csv",
            "sn_bao_fit_summary.csv",
            "sn_bao_prior_edges.csv",
            "sn_bao_baseline_comparison.csv",
            "bao_residuals.csv",
            "sn_residual_summary.csv",
            "hz_fit_summary.csv",
            "hz_prior_edges.csv",
            "hz_baseline_comparison.csv",
            "hz_residuals.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=100)
    parser.add_argument(
        "--sn-policy",
        choices=["observed_redshift_distance_duality", "true_redshift_Etherington"],
        default="observed_redshift_distance_duality",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_retest(args.output_root, args.timestamp, args.max_iter, args.sn_policy))


if __name__ == "__main__":
    main()
