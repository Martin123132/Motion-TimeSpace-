#!/usr/bin/env python3
"""Run the fixed trace/quadrupole pair-ruler branch against SN+BAO and H(z)."""

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

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cell_balanced_clock_map_fixed_branch_retest as retest  # noqa: E402
import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import Hz_radial_expansion_smoke as hzsmoke  # noqa: E402


SN_BAO_REFERENCE_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
SOURCE_LAW_RUN = RUNS_ROOT / "20260531-235959-trace-quadrupole-source-law-attempt"
PAIR_ACTION_RUN = RUNS_ROOT / "20260531-235959-effective-pair-action-owner-attempt"

B_MEM = 2.0 / 27.0
U3_QUARTER = 0.25
TRACE_COEFF = B_MEM / 4.0
QUAD_COEFF = B_MEM / 6.0
PAIR_BRANCH = "MTS_pair_ruler_fixed_u3quarter"
NO_CLOCK_QUARTER = "MTS_2over27_no_clock_u3quarter"
CLAIM_CEILING = "fixed_pair_ruler_branch_smoke_no_bridge_promotion"


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
    if name.startswith("164-") or name.endswith("fixed_pair_ruler_branch_smoke.py"):
        return "current fixed pair-ruler smoke"
    if name.startswith("161-") or "trace-quadrupole-source-law" in str(path):
        return "fixed trace/quadrupole source laws"
    if name.startswith("163-") or "effective-pair-action-owner" in str(path):
        return "effective pair action/null response owner"
    if name.endswith(".py"):
        return "machine dependency"
    if name == "run_config.json" or "cosmo-SN-BAO-short-smoke" in str(path):
        return "SN+BAO reference configuration"
    if "Pantheon" in name or "desi" in name.lower() or "bao" in name.lower():
        return "empirical data"
    return "supporting source"


def load_reference_config() -> dict[str, Any]:
    return json.loads((SN_BAO_REFERENCE_RUN / "run_config.json").read_text(encoding="utf-8"))


def source_register_rows(script_path: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "cell_balanced_clock_map_fixed_branch_retest.py",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        SCRIPT_DIR / "Hz_radial_expansion_smoke.py",
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        WORK_DIR / "162-pair-ruler-operator-null-response-contract.md",
        WORK_DIR / "163-effective-pair-action-owner-attempt.md",
        SOURCE_LAW_RUN / "status.json",
        SOURCE_LAW_RUN / "results" / "source_law_scorecard.csv",
        SOURCE_LAW_RUN / "results" / "combined_projection_scorecard.csv",
        PAIR_ACTION_RUN / "status.json",
        PAIR_ACTION_RUN / "results" / "compensated_kernel_proof.csv",
        SN_BAO_REFERENCE_RUN / "run_config.json",
        SN_BAO_REFERENCE_RUN / "results" / "fit_summary.csv",
        Path(config["sn_data"]),
        Path(config["sn_cov"]),
        Path(config["bao_data"]),
        Path(config["bao_cov"]),
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


def branches() -> list[str]:
    return [
        "LCDM",
        "wCDM",
        "CPL",
        "MTS_2over27_no_clock_u3fit",
        NO_CLOCK_QUARTER,
        PAIR_BRANCH,
    ]


def base_branch(branch: str) -> str:
    if branch == PAIR_BRANCH:
        return NO_CLOCK_QUARTER
    return branch


def is_pair_branch(branch: str) -> bool:
    return branch == PAIR_BRANCH


def is_mts_branch(branch: str) -> bool:
    return branch.startswith("MTS_")


def pair_projection_factors(z_values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    z_arr = np.asarray(z_values, dtype=float)
    load_n = np.log1p(z_arr)
    activation = 1.0 - np.exp(-((load_n / U3_QUARTER) ** 3))
    trace = TRACE_COEFF * activation * (1.0 - 2.0 * np.exp(-load_n))
    quadrupole = QUAD_COEFF * (1.0 - np.exp(-2.0 * load_n))
    pi_perp = trace - quadrupole / 3.0
    pi_parallel = trace + 2.0 * quadrupole / 3.0
    return trace, quadrupole, pi_perp, pi_parallel


def branch_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "LCDM",
            "role": "baseline",
            "background": "LCDM",
            "SN_policy": "standard one-point SN distance",
            "BAO_policy": "standard FLRW ruler",
            "Hz_policy": "standard H(z)",
            "fixed_projection_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "wCDM",
            "role": "baseline",
            "background": "wCDM",
            "SN_policy": "standard one-point SN distance",
            "BAO_policy": "standard FLRW ruler",
            "Hz_policy": "standard H(z)",
            "fixed_projection_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m,w + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m,h,w",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "CPL",
            "role": "baseline",
            "background": "CPL",
            "SN_policy": "standard one-point SN distance",
            "BAO_policy": "standard FLRW ruler",
            "Hz_policy": "standard H(z)",
            "fixed_projection_parameters": "",
            "fitted_parameters_SN_BAO": "Omega_m,w0,wa + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m,h,w0,wa",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "MTS_2over27_no_clock_u3fit",
            "role": "MTS control",
            "background": "fixed B_mem=2/27,p=3,u3=0.2429466120286312",
            "SN_policy": "no-clock one-point branch",
            "BAO_policy": "standard FLRW ruler",
            "Hz_policy": "no-clock H(z)",
            "fixed_projection_parameters": "none",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "fixed_background_control_only",
        },
        {
            "branch": NO_CLOCK_QUARTER,
            "role": "MTS control",
            "background": "fixed B_mem=2/27,p=3,u3=1/4",
            "SN_policy": "no-clock one-point branch",
            "BAO_policy": "standard FLRW ruler",
            "Hz_policy": "no-clock H(z)",
            "fixed_projection_parameters": "none",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha",
            "fitted_parameters_Hz": "Omega_m + h",
            "claim_ceiling": "fixed_background_control_only",
        },
        {
            "branch": PAIR_BRANCH,
            "role": "fixed pair-ruler test branch",
            "background": "fixed B_mem=2/27,p=3,u3=1/4",
            "SN_policy": "null-response: no-clock one-point branch",
            "BAO_policy": "fixed pair-ruler projection from 161",
            "Hz_policy": "null-response: no-clock H(z)",
            "fixed_projection_parameters": "T=(B_mem/4)F_D(1-2e^-N); S=(B_mem/6)(1-e^-2N)",
            "fitted_parameters_SN_BAO": "Omega_m + SN_offset + BAO_alpha; no projection amplitudes",
            "fitted_parameters_Hz": "Omega_m + h; no projection amplitudes",
            "claim_ceiling": CLAIM_CEILING,
        },
    ]


def model_bounds(branch: str, include_h: bool = False) -> dict[str, tuple[float, float]]:
    return retest.model_bounds(base_branch(branch), include_h=include_h)


def e_z_branch(branch: str, z_eval: np.ndarray, values: dict[str, float]) -> np.ndarray:
    return retest.e_z_branch(base_branch(branch), z_eval, values)


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


def sn_chi2_branch(branch: str, values: dict[str, float], sn: dict[str, Any]) -> tuple[float, float, np.ndarray, np.ndarray]:
    return retest.sn_chi2_branch(base_branch(branch), values, sn, "observed_redshift_distance_duality")


def bao_prediction_branch(branch: str, values: dict[str, float], bao: dict[str, Any], alpha: float) -> np.ndarray:
    z_values = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    dm_values = comoving_integral_branch(branch, z_values, values)
    ez_values = e_z_branch(branch, z_values, values)
    if is_pair_branch(branch):
        _, _, pi_perp, pi_parallel = pair_projection_factors(z_values)
    else:
        pi_perp = np.zeros_like(z_values)
        pi_parallel = np.zeros_like(z_values)
    predictions: list[float] = []
    for row, z_value, dm_value, ez_value, perp, parallel in zip(
        bao["rows"], z_values, dm_values, ez_values, pi_perp, pi_parallel, strict=True
    ):
        dm_projected = (1.0 + perp) * dm_value
        dh_projected = (1.0 + parallel) / ez_value
        quantity = row["quantity"]
        if quantity == "DM_over_rs":
            predictions.append(alpha * float(dm_projected))
        elif quantity == "DH_over_rs":
            predictions.append(alpha * float(dh_projected))
        elif quantity == "DV_over_rs":
            predictions.append(alpha * float((z_value * dm_projected * dm_projected * dh_projected) ** (1.0 / 3.0)))
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


def fit_sn_bao_branch(
    branch: str,
    sn: dict[str, Any],
    bao: dict[str, Any],
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
            chi2_sn, _, _, _ = sn_chi2_branch(branch, values, sn)
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
        for seed in retest.seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    chi2_sn, sn_offset, sn_residual, sn_predicted = sn_chi2_branch(branch, values, sn)
    chi2_bao, bao_alpha, bao_residual, bao_predicted = bao_chi2_branch(branch, values, bao)
    chi2_total = chi2_sn + chi2_bao
    n_points = int(len(sn["z"]) + len(bao["rows"]))
    dynamic_k = len(names) + 2
    aic = chi2_total + 2.0 * dynamic_k
    bic = chi2_total + dynamic_k * math.log(n_points)
    edge = retest.edge_rows(branch, values, bounds_by_name, "SN_BAO")
    row = {
        "dataset": "SN_BAO",
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
        "projection_policy": "fixed_pair_ruler" if is_pair_branch(branch) else "none",
        "optimizer_message": str(result.message),
        "claim_ceiling": "baseline" if not is_mts_branch(branch) else CLAIM_CEILING,
    }
    return row, edge, sn_residual, sn_predicted, bao_residual, bao_predicted


def h_prediction_branch(branch: str, values: dict[str, float], z_values: np.ndarray) -> np.ndarray:
    return retest.h_prediction_branch(base_branch(branch), values, z_values)


def fit_hz_branch(branch: str, dataset: dict[str, Any], max_iter: int) -> tuple[dict[str, Any], list[dict[str, Any]], np.ndarray, np.ndarray]:
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
        for seed in retest.seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    predicted = h_prediction_branch(branch, values, dataset["z"])
    residual = dataset["H"] - predicted
    inv_cov = np.linalg.inv(dataset["covariance"])
    chi2 = float(residual @ inv_cov @ residual)
    dynamic_k = len(names)
    n_data = len(dataset["z"])
    edge = retest.edge_rows(branch, values, bounds_by_name, dataset["dataset_label"])
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
        "projection_policy": "null_response_no_clock_Hz" if is_pair_branch(branch) else "none",
        "optimizer_message": str(result.message),
        "claim_ceiling": "baseline" if not is_mts_branch(branch) else CLAIM_CEILING,
    }
    return row, edge, residual, predicted


def comparison_label(delta_bic: float) -> str:
    if delta_bic <= -2.0:
        return "branch_preferred_by_BIC"
    if delta_bic < 2.0:
        return "competitive_draw_by_BIC"
    return "branch_disfavored_by_BIC"


def comparison_rows(fit_rows: list[dict[str, Any]], dataset_key: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_dataset_branch = {(row[dataset_key], row["branch"]): row for row in fit_rows}
    datasets = sorted({row[dataset_key] for row in fit_rows})
    targets = ["MTS_2over27_no_clock_u3fit", NO_CLOCK_QUARTER, PAIR_BRANCH]
    references = ["LCDM", "wCDM", "CPL", "MTS_2over27_no_clock_u3fit", NO_CLOCK_QUARTER]
    for dataset in datasets:
        for target in targets:
            if (dataset, target) not in by_dataset_branch:
                continue
            target_row = by_dataset_branch[(dataset, target)]
            for reference in references:
                if target == reference or (dataset, reference) not in by_dataset_branch:
                    continue
                reference_row = by_dataset_branch[(dataset, reference)]
                target_chi = float(target_row.get("chi2_total", target_row.get("chi2")))
                reference_chi = float(reference_row.get("chi2_total", reference_row.get("chi2")))
                delta_bic = float(target_row["BIC"]) - float(reference_row["BIC"])
                rows.append(
                    {
                        dataset_key: dataset,
                        "branch": target,
                        "reference_branch": reference,
                        "delta_chi2": target_chi - reference_chi,
                        "delta_AIC": float(target_row["AIC"]) - float(reference_row["AIC"]),
                        "delta_BIC": delta_bic,
                        "branch_edge_flag": target_row["edge_flag"],
                        "reference_edge_flag": reference_row["edge_flag"],
                        "readout": comparison_label(delta_bic),
                    }
                )
    return rows


def projection_factor_rows(bao: dict[str, Any]) -> list[dict[str, Any]]:
    z_values = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    trace, quadrupole, pi_perp, pi_parallel = pair_projection_factors(z_values)
    rows: list[dict[str, Any]] = []
    for index, (bao_row, t_value, s_value, perp, parallel) in enumerate(
        zip(bao["rows"], trace, quadrupole, pi_perp, pi_parallel, strict=True)
    ):
        rows.append(
            {
                "row_index": index,
                "z": bao_row["z"],
                "observable": bao_row["quantity"],
                "T_trace": t_value,
                "S_quadrupole": s_value,
                "Pi_perp": perp,
                "Pi_parallel": parallel,
                "DM_factor": 1.0 + perp,
                "DH_factor": 1.0 + parallel,
                "fixed_law": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-2N)",
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
    rows: list[dict[str, Any]] = []
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


def get_comparison(rows: list[dict[str, Any]], dataset_key: str, dataset: str, branch: str, reference: str) -> dict[str, Any]:
    return next(row for row in rows if row[dataset_key] == dataset and row["branch"] == branch and row["reference_branch"] == reference)


def gate_rows(
    sn_bao_rows: list[dict[str, Any]],
    sn_bao_comparisons: list[dict[str, Any]],
    hz_rows: list[dict[str, Any]],
    hz_comparisons: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pair = next(row for row in sn_bao_rows if row["branch"] == PAIR_BRANCH)
    no_clock = next(row for row in sn_bao_rows if row["branch"] == NO_CLOCK_QUARTER)
    pair_vs_lcdm = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, "LCDM")
    pair_vs_no_clock = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, NO_CLOCK_QUARTER)
    pair_hz_primary = get_comparison(hz_comparisons, "dataset_label", "CC15_suggested_primary", PAIR_BRANCH, "LCDM")
    pair_hz_no_clock = get_comparison(hz_comparisons, "dataset_label", "CC15_suggested_primary", PAIR_BRANCH, NO_CLOCK_QUARTER)
    nonconverged = [row["branch"] for row in sn_bao_rows if str(row["success"]) != "True"] + [
        f"{row['dataset_label']}:{row['branch']}" for row in hz_rows if str(row["success"]) != "True"
    ]
    edge_flags = [row["branch"] for row in sn_bao_rows if row["edge_flag"] in {True, "True"} and is_mts_branch(row["branch"])]
    sn_delta_vs_no_clock = float(pair["chi2_SN"]) - float(no_clock["chi2_SN"])
    bao_delta_vs_no_clock = float(pair["chi2_BAO"]) - float(no_clock["chi2_BAO"])
    return [
        {
            "gate": "same_data_same_nuisance",
            "status": "pass",
            "evidence": "all branches use the same Pantheon+/DESI/H(z) data and same SN offset/BAO alpha freedom",
        },
        {
            "gate": "no_extra_projection_knobs",
            "status": "pass",
            "evidence": "pair branch fixes B_mem=2/27, u3=1/4, T_D and S_D; only Omega_m/SN_offset/BAO_alpha are fitted in SN+BAO",
        },
        {
            "gate": "convergence",
            "status": "pass" if not nonconverged else "warn",
            "evidence": "all fitted branches converged" if not nonconverged else ";".join(nonconverged),
        },
        {
            "gate": "pair_vs_LCDM",
            "status": "pass_preferred_or_draw" if float(pair_vs_lcdm["delta_BIC"]) < 2.0 else "fail_disfavored",
            "evidence": f"delta_chi2={pair_vs_lcdm['delta_chi2']}; delta_BIC={pair_vs_lcdm['delta_BIC']}; readout={pair_vs_lcdm['readout']}",
        },
        {
            "gate": "pair_vs_no_clock_control",
            "status": "pass_competitive" if float(pair_vs_no_clock["delta_BIC"]) < 2.0 else "fail_worse_than_no_clock",
            "evidence": f"delta_chi2={pair_vs_no_clock['delta_chi2']}; delta_BIC={pair_vs_no_clock['delta_BIC']}; BAO_delta={bao_delta_vs_no_clock}; SN_delta={sn_delta_vs_no_clock}",
        },
        {
            "gate": "SN_null_policy",
            "status": "pass" if sn_delta_vs_no_clock < 1.0 else "warn_SN_shift_from_refit",
            "evidence": f"pair chi2_SN - no_clock chi2_SN = {sn_delta_vs_no_clock}",
        },
        {
            "gate": "Hz_null_policy",
            "status": "pass" if abs(float(pair_hz_no_clock["delta_chi2"])) < 1.0e-6 else "warn",
            "evidence": f"primary CC15 pair vs no_clock delta_chi2={pair_hz_no_clock['delta_chi2']}; pair vs LCDM delta_BIC={pair_hz_primary['delta_BIC']}",
        },
        {
            "gate": "prior_edge_safety",
            "status": "pass" if not edge_flags else "warn",
            "evidence": "MTS branches not edge-flagged" if not edge_flags else ";".join(edge_flags),
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(sn_bao_comparisons: list[dict[str, Any]], hz_comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pair_vs_lcdm = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, "LCDM")
    pair_vs_wc = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, "wCDM")
    pair_vs_cpl = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, "CPL")
    pair_vs_no_clock = get_comparison(sn_bao_comparisons, "dataset", "SN_BAO", PAIR_BRANCH, NO_CLOCK_QUARTER)
    pair_hz_lcdm = get_comparison(hz_comparisons, "dataset_label", "CC15_suggested_primary", PAIR_BRANCH, "LCDM")
    if float(pair_vs_lcdm["delta_BIC"]) < 2.0 and float(pair_vs_no_clock["delta_BIC"]) < 2.0:
        status = "fixed_pair_ruler_branch_survives_smoke_competitive_not_promoted"
    elif float(pair_vs_lcdm["delta_BIC"]) < 2.0:
        status = "fixed_pair_ruler_branch_beats_or_draws_LCDM_but_loses_to_no_clock"
    else:
        status = "fixed_pair_ruler_branch_demote_or_rework_after_smoke"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"SN+BAO delta_BIC_vs_LCDM={pair_vs_lcdm['delta_BIC']}; delta_BIC_vs_no_clock={pair_vs_no_clock['delta_BIC']}; H(z) primary delta_BIC_vs_LCDM={pair_hz_lcdm['delta_BIC']}",
        },
        {
            "item": "pair_vs_LCDM",
            "verdict": pair_vs_lcdm["readout"],
            "evidence": f"delta_chi2={pair_vs_lcdm['delta_chi2']}; delta_AIC={pair_vs_lcdm['delta_AIC']}; delta_BIC={pair_vs_lcdm['delta_BIC']}",
        },
        {
            "item": "pair_vs_wCDM",
            "verdict": pair_vs_wc["readout"],
            "evidence": f"delta_chi2={pair_vs_wc['delta_chi2']}; delta_AIC={pair_vs_wc['delta_AIC']}; delta_BIC={pair_vs_wc['delta_BIC']}",
        },
        {
            "item": "pair_vs_CPL",
            "verdict": pair_vs_cpl["readout"],
            "evidence": f"delta_chi2={pair_vs_cpl['delta_chi2']}; delta_AIC={pair_vs_cpl['delta_AIC']}; delta_BIC={pair_vs_cpl['delta_BIC']}",
        },
        {
            "item": "pair_vs_no_clock_control",
            "verdict": pair_vs_no_clock["readout"],
            "evidence": f"delta_chi2={pair_vs_no_clock['delta_chi2']}; delta_AIC={pair_vs_no_clock['delta_AIC']}; delta_BIC={pair_vs_no_clock['delta_BIC']}",
        },
        {
            "item": "Hz_primary_vs_LCDM",
            "verdict": pair_hz_lcdm["readout"],
            "evidence": f"delta_chi2={pair_hz_lcdm['delta_chi2']}; delta_BIC={pair_hz_lcdm['delta_BIC']}",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "fixed branch smoke only; no parent-action, CMB, lensing/growth, or local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "165-pair-ruler-residual-and-two-point-safety-audit.md",
            "evidence": "inspect BAO row residuals and define the next growth/lensing/two-point safety test",
        },
    ]


def run_smoke(output_root: Path, timestamp: str | None, max_iter: int) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-fixed-pair-ruler-branch-smoke"
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

    fit_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    sn_residuals: dict[str, np.ndarray] = {}
    bao_residuals: dict[str, np.ndarray] = {}
    bao_predictions: dict[str, np.ndarray] = {}
    for branch in branches():
        fit, edges, sn_residual, _, bao_residual, bao_predicted = fit_sn_bao_branch(branch, sn, bao, max_iter)
        fit_rows.append(fit)
        edge_rows.extend(edges)
        sn_residuals[branch] = sn_residual
        bao_residuals[branch] = bao_residual
        bao_predictions[branch] = bao_predicted

    hz_datasets = hzsmoke.datasets_to_score()
    hz_rows: list[dict[str, Any]] = []
    hz_edges: list[dict[str, Any]] = []
    hz_residuals: dict[tuple[str, str], np.ndarray] = {}
    hz_predictions: dict[tuple[str, str], np.ndarray] = {}
    for dataset in hz_datasets:
        for branch in branches():
            fit, edges, residual, predicted = fit_hz_branch(branch, dataset, max_iter)
            hz_rows.append(fit)
            hz_edges.extend(edges)
            hz_residuals[(dataset["dataset_label"], branch)] = residual
            hz_predictions[(dataset["dataset_label"], branch)] = predicted

    sn_bao_comparisons = comparison_rows(fit_rows, "dataset")
    hz_comparisons = comparison_rows(hz_rows, "dataset_label")
    gates = gate_rows(fit_rows, sn_bao_comparisons, hz_rows, hz_comparisons)
    decisions = decision_rows(sn_bao_comparisons, hz_comparisons)

    run_config = {
        "timestamp": run_stamp,
        "claim_ceiling": CLAIM_CEILING,
        "reference_SN_BAO_run": str(SN_BAO_REFERENCE_RUN),
        "source_law_run": str(SOURCE_LAW_RUN),
        "pair_action_run": str(PAIR_ACTION_RUN),
        "max_iter": max_iter,
        "sn_rows": int(len(sn["z"])),
        "bao_rows": int(len(bao["rows"])),
        "hz_datasets": [dataset["dataset_label"] for dataset in hz_datasets],
        "branches": branch_contract_rows(),
    }
    write_json(run_dir / "run_config.json", run_config)
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "branch_contract.csv",
        branch_contract_rows(),
        [
            "branch",
            "role",
            "background",
            "SN_policy",
            "BAO_policy",
            "Hz_policy",
            "fixed_projection_parameters",
            "fitted_parameters_SN_BAO",
            "fitted_parameters_Hz",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "sn_bao_fit_summary.csv",
        fit_rows,
        [
            "dataset",
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
            "projection_policy",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "sn_bao_prior_edges.csv", edge_rows, ["dataset", "branch", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(
        results_dir / "sn_bao_baseline_comparison.csv",
        sn_bao_comparisons,
        ["dataset", "branch", "reference_branch", "delta_chi2", "delta_AIC", "delta_BIC", "branch_edge_flag", "reference_edge_flag", "readout"],
    )
    write_csv(
        results_dir / "pair_projection_factors.csv",
        projection_factor_rows(bao),
        ["row_index", "z", "observable", "T_trace", "S_quadrupole", "Pi_perp", "Pi_parallel", "DM_factor", "DH_factor", "fixed_law"],
    )
    write_csv(
        results_dir / "bao_residuals.csv",
        bao_residual_rows(bao, fit_rows, bao_residuals, bao_predictions),
        ["branch", "row_index", "z", "observable", "observed", "predicted", "residual", "diagonal_sigma", "diagonal_pull", "cov_signed_chi2_contribution"],
    )
    write_csv(
        results_dir / "sn_residual_summary.csv",
        sn_residual_summary_rows(sn, fit_rows, sn_residuals),
        ["branch", "rows", "mean_residual", "rms_residual", "max_abs_residual", "rms_diagonal_pull", "max_abs_diagonal_pull"],
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
            "projection_policy",
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
        "sn_rows": int(len(sn["z"])),
        "bao_rows": int(len(bao["rows"])),
        "hz_fit_rows": len(hz_rows),
        "generated": [
            "source_register.csv",
            "branch_contract.csv",
            "sn_bao_fit_summary.csv",
            "sn_bao_prior_edges.csv",
            "sn_bao_baseline_comparison.csv",
            "pair_projection_factors.csv",
            "bao_residuals.csv",
            "sn_residual_summary.csv",
            "hz_fit_summary.csv",
            "hz_prior_edges.csv",
            "hz_baseline_comparison.csv",
            "hz_residuals.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "165-pair-ruler-residual-and-two-point-safety-audit.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_smoke(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
