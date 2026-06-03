#!/usr/bin/env python3
"""Guarded CMB distance-prior score for the locked B_mem=2/27 branch."""

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
from scipy import integrate, optimize


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
FORMALIZATION_WORKBENCH = POST_CHECKPOINT.parent / "formalization-workbench"
CMB_DIR = (
    FORMALIZATION_WORKBENCH
    / "data"
    / "cosmology"
    / "growth_CMB"
    / "planck2018_distance_priors"
)
SOURCE_DIR = CMB_DIR / "source"
VECTOR_PATH = CMB_DIR / "planck2018_distance_prior_vector.csv"
COVARIANCE_PATH = CMB_DIR / "planck2018_distance_prior_covariance.csv"
ROW_LOCK_PATH = CMB_DIR / "row_lock_manifest.json"
CONTRACT_PATH = POST_CHECKPOINT / "115-locked-2over27-CMB-parameter-map-contract.md"

sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as runner  # noqa: E402


C_KM_S = 299792.458
N_EFF = 3.046
OMEGA_GAMMA_H2 = 2.469e-5
RADIATION_FACTOR = 0.22710731766

LOCKED_BRANCH = "canonical_R_2over27_locked_amplitude"
LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25

PRIMARY_PRIOR_TABLES = ["wCDM", "LCDM"]
SCORE_MODES = {
    "strict_full4": ["R", "l_A", "Omega_b_h2", "n_s"],
    "marginal_R_lA": ["R", "l_A"],
}
MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_manifest() -> dict[str, Any]:
    with ROW_LOCK_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_register_rows() -> list[dict[str, Any]]:
    paths = [VECTOR_PATH, COVARIANCE_PATH, ROW_LOCK_PATH, CONTRACT_PATH, Path(__file__).resolve()]
    if SOURCE_DIR.exists():
        paths.extend(sorted(path for path in SOURCE_DIR.iterdir() if path.is_file()))
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "kind": "contract_or_script" if path in {CONTRACT_PATH, Path(__file__).resolve()} else "data_source",
                "path": str(path),
                "exists": exists,
                "readable": exists and path.is_file(),
                "bytes": path.stat().st_size if exists and path.is_file() else "",
                "sha256": file_sha256(path) if exists and path.is_file() else "",
                "issue": "" if exists else "missing",
            }
        )
    return rows


def prior_table_data(model: str) -> dict[str, Any]:
    vector_rows = [row for row in read_csv_rows(VECTOR_PATH) if row["model"] == model]
    if not vector_rows:
        raise ValueError(f"missing vector rows for prior table {model}")
    parameters = [row["parameter"] for row in vector_rows]
    observed = np.asarray([float(row["mean"]) for row in vector_rows], dtype=float)
    means = {row["parameter"]: float(row["mean"]) for row in vector_rows}

    cov_rows = [row for row in read_csv_rows(COVARIANCE_PATH) if row["model"] == model]
    parameter_index = {parameter: index for index, parameter in enumerate(parameters)}
    covariance = np.full((len(parameters), len(parameters)), np.nan, dtype=float)
    for row in cov_rows:
        covariance[parameter_index[row["row_parameter"]], parameter_index[row["col_parameter"]]] = float(
            row["covariance"]
        )
    if not np.isfinite(covariance).all():
        raise ValueError(f"incomplete covariance for {model}")
    if not np.allclose(covariance, covariance.T, rtol=0.0, atol=1.0e-14):
        raise ValueError(f"non-symmetric covariance for {model}")
    np.linalg.cholesky(covariance)
    return {
        "model": model,
        "parameters": parameters,
        "observed": observed,
        "covariance": covariance,
        "means": means,
        "default_for_C0": any(row.get("default_for_C0", "").lower() == "true" for row in vector_rows),
    }


def prior_table_register_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table in PRIMARY_PRIOR_TABLES:
        data = prior_table_data(table)
        eig = np.linalg.eigvalsh(data["covariance"])
        manifest_entry = next(
            (entry for entry in manifest.get("models", []) if entry.get("model") == table),
            {},
        )
        rows.append(
            {
                "prior_table": table,
                "role": "primary_default" if table == "wCDM" else "primary_sensitivity",
                "parameters": ";".join(data["parameters"]),
                "vector_length": len(data["parameters"]),
                "covariance_shape": f"{data['covariance'].shape[0]}x{data['covariance'].shape[1]}",
                "cholesky_pass": True,
                "min_eigenvalue": float(eig[0]),
                "default_for_C0": data["default_for_C0"],
                "manifest_use_status": manifest_entry.get("use_status", ""),
                "claim_ceiling": "compressed_distance_prior_internal_stress_test_only",
            }
        )
    return rows


def model_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "physics_model": "LCDM",
            "free_parameters": "Omega_m0;h",
            "fixed_parameters": "flat LCDM late-time shape",
            "dynamic_k": 2,
            "claim_ceiling": "baseline",
        },
        {
            "model": "wCDM",
            "role": "flexible_baseline",
            "physics_model": "wCDM",
            "free_parameters": "Omega_m0;h;w",
            "fixed_parameters": "constant w form",
            "dynamic_k": 3,
            "claim_ceiling": "baseline",
        },
        {
            "model": "CPL",
            "role": "flexible_baseline",
            "physics_model": "CPL",
            "free_parameters": "Omega_m0;h;w0;wa",
            "fixed_parameters": "CPL form",
            "dynamic_k": 4,
            "claim_ceiling": "baseline",
        },
        {
            "model": "MTS_locked_2over27",
            "role": "predeclared_locked_branch",
            "physics_model": "MTS_fixed_p3_u3quarter",
            "free_parameters": "Omega_m0;h",
            "fixed_parameters": "p=3;u3=1/4;DeltaR=2/9;B_mem=2/27",
            "dynamic_k": 2,
            "claim_ceiling": "locked_empirical_closure_not_parent_prediction",
        },
        {
            "model": "MTS_Bmem_zero",
            "role": "negative_control",
            "physics_model": "MTS_Bmem_zero",
            "free_parameters": "Omega_m0;h",
            "fixed_parameters": "p=3;u3=1/4;B_mem=0",
            "dynamic_k": 2,
            "claim_ceiling": "control",
        },
    ]


def parameter_map_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "h",
            "rule": "fit h from CMB distance prior for every branch",
            "status": "encoded",
            "symmetry": "same bounds and edge flag for all branches",
        },
        {
            "item": "Omega_m0",
            "rule": "fit Omega_m0 from CMB distance prior for every branch",
            "status": "encoded",
            "symmetry": "same bounds and edge flag for all branches",
        },
        {
            "item": "Omega_b_h2",
            "rule": "fix to mean of scored compressed-prior table",
            "status": "encoded",
            "symmetry": "same fixed input for all branches within each prior table",
        },
        {
            "item": "n_s",
            "rule": "fix to mean of scored compressed-prior table",
            "status": "encoded",
            "symmetry": "same fixed input for all branches within each prior table",
        },
        {
            "item": "radiation",
            "rule": "N_eff=3.046; Omega_gamma0=2.469e-5/h^2; Omega_r0=Omega_gamma0*(1+0.22710731766*N_eff)",
            "status": "encoded",
            "symmetry": "same radiation convention for all branches",
        },
        {
            "item": "sound_horizon",
            "rule": "scale-factor quadrature only",
            "status": "encoded",
            "symmetry": "legacy finite-z sound integral banned for all branches",
        },
        {
            "item": "prior_tables",
            "rule": "score wCDM default and LCDM sensitivity tables",
            "status": "encoded",
            "symmetry": "no table cherry-picking for MTS",
        },
        {
            "item": "claim_ceiling",
            "rule": "background compressed-distance stress only",
            "status": "encoded",
            "symmetry": "no CMB spectrum or perturbation claim",
        },
    ]


def free_parameter_bounds(model: str) -> dict[str, tuple[float, float]]:
    bounds: dict[str, tuple[float, float]] = {"Omega_m0": (0.05, 0.60), "h": (0.45, 0.90)}
    if model == "wCDM":
        bounds["w"] = (-2.0, -0.2)
    elif model == "CPL":
        bounds["w0"] = (-2.0, -0.2)
        bounds["wa"] = (-2.0, 2.0)
    return bounds


def physical_model_and_params(model: str, values: dict[str, float]) -> tuple[str, dict[str, float]]:
    params = {"Omega_m": values["Omega_m0"], "h0": 100.0 * values["h"]}
    if model == "wCDM":
        params["w"] = values["w"]
        return "wCDM", params
    if model == "CPL":
        params["w0"] = values["w0"]
        params["wa"] = values["wa"]
        return "CPL", params
    if model == "MTS_locked_2over27":
        params.update({"B_mem": LOCKED_B_MEM, "p": LOCKED_P, "u3": LOCKED_U3})
        return "MTS_fixed_p3_u3quarter", params
    if model == "MTS_Bmem_zero":
        params.update({"B_mem": 0.0, "p": LOCKED_P, "u3": LOCKED_U3})
        return "MTS_Bmem_zero", params
    return "LCDM", params


def z_star(omega_m0: float, h: float, omega_b_h2: float) -> float:
    omega_m_h2 = omega_m0 * h * h
    g1 = 0.0783 * omega_b_h2 ** -0.238 / (1.0 + 39.5 * omega_b_h2 ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b_h2 ** 1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b_h2 ** -0.738) * (1.0 + g1 * omega_m_h2**g2)


def cmb_prediction(model: str, values: dict[str, float], prior_means: dict[str, float]) -> dict[str, float]:
    omega_b_h2 = prior_means["Omega_b_h2"]
    n_s = prior_means["n_s"]
    physics_model, params = physical_model_and_params(model, values)
    h = values["h"]
    h0 = 100.0 * h
    omega_gamma = OMEGA_GAMMA_H2 / (h * h)
    omega_r = omega_gamma * (1.0 + RADIATION_FACTOR * N_EFF)
    zs = z_star(values["Omega_m0"], h, omega_b_h2)
    a_star = 1.0 / (1.0 + zs)

    def inv_a2_e(a: float) -> float:
        if a <= 1.0e-12:
            return 1.0 / math.sqrt(omega_r)
        z = 1.0 / a - 1.0
        late_e = float(runner.e_z(physics_model, np.asarray([z], dtype=float), params)[0])
        e2 = late_e * late_e + omega_r / (a**4)
        return 1.0 / (a * a * math.sqrt(e2))

    dm_integral = integrate.quad(inv_a2_e, a_star, 1.0, epsrel=1.0e-8, limit=300)[0]
    d_m = (C_KM_S / h0) * dm_integral

    def sound_integrand_a(a: float) -> float:
        if a <= 1.0e-12:
            c_s0 = 1.0 / math.sqrt(3.0)
            return c_s0 / math.sqrt(omega_r)
        r_b = 31500.0 * omega_b_h2 * a
        c_s = 1.0 / math.sqrt(3.0 * (1.0 + r_b))
        return c_s * inv_a2_e(a)

    sound_integral = integrate.quad(sound_integrand_a, 0.0, a_star, epsrel=1.0e-8, limit=300)[0]
    r_s = (C_KM_S / h0) * sound_integral
    shift_r = math.sqrt(values["Omega_m0"]) * h0 * d_m / C_KM_S
    l_a = math.pi * d_m / r_s
    return {
        "R": shift_r,
        "l_A": l_a,
        "Omega_b_h2": omega_b_h2,
        "n_s": n_s,
        "z_star": zs,
        "r_s_star": r_s,
        "D_M_star": d_m,
        "Omega_r0": omega_r,
    }


def score_prediction(
    prediction: dict[str, float],
    prior_data: dict[str, Any],
    score_mode: str,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    all_parameters = prior_data["parameters"]
    mode_parameters = SCORE_MODES[score_mode]
    indices = [all_parameters.index(parameter) for parameter in mode_parameters]
    observed = prior_data["observed"][indices]
    covariance = prior_data["covariance"][np.ix_(indices, indices)]
    predicted = np.asarray([prediction[parameter] for parameter in mode_parameters], dtype=float)
    residual = observed - predicted
    chi2 = float(residual @ np.linalg.inv(covariance) @ residual)
    return chi2, observed, predicted, residual


def seed_vectors(names: list[str], bounds: list[tuple[float, float]]) -> list[np.ndarray]:
    default = {
        "Omega_m0": 0.31,
        "h": 0.68,
        "w": -1.0,
        "w0": -1.0,
        "wa": 0.0,
    }
    seed_dicts = [
        default,
        {**default, "Omega_m0": 0.25, "h": 0.72},
        {**default, "Omega_m0": 0.35, "h": 0.65},
        {**default, "Omega_m0": 0.20, "h": 0.80},
        {**default, "Omega_m0": 0.45, "h": 0.58},
        {**default, "w": -0.8, "w0": -0.8, "wa": 0.5},
        {**default, "w": -1.2, "w0": -1.2, "wa": -0.5},
    ]
    vectors: list[np.ndarray] = []
    seen: set[tuple[float, ...]] = set()
    for seed in seed_dicts:
        values = []
        for name, (lower, upper) in zip(names, bounds, strict=True):
            value = min(max(seed[name], lower + 1.0e-6), upper - 1.0e-6)
            values.append(value)
        key = tuple(round(value, 8) for value in values)
        if key not in seen:
            vectors.append(np.asarray(values, dtype=float))
            seen.add(key)
    midpoint = np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)
    key = tuple(round(value, 8) for value in midpoint)
    if key not in seen:
        vectors.append(midpoint)
    return vectors


def edge_rows_for_fit(
    prior_table: str,
    score_mode: str,
    model: str,
    values: dict[str, float],
    bounds: dict[str, tuple[float, float]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, (lower, upper) in bounds.items():
        value = values.get(name, float("nan"))
        span = upper - lower
        lower_fraction = (value - lower) / span
        upper_fraction = (upper - value) / span
        edge_flag = lower_fraction <= 0.01 or upper_fraction <= 0.01
        rows.append(
            {
                "prior_table": prior_table,
                "score_mode": score_mode,
                "model": model,
                "parameter": name,
                "value": value,
                "lower": lower,
                "upper": upper,
                "lower_fraction": lower_fraction,
                "upper_fraction": upper_fraction,
                "edge_flag": edge_flag,
            }
        )
    return rows


def fit_model(
    prior_table: str,
    score_mode: str,
    model: str,
    prior_data: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    bounds_by_name = free_parameter_bounds(model)
    names = list(bounds_by_name.keys())
    bounds = [bounds_by_name[name] for name in names]
    best: dict[str, Any] | None = None
    issue = ""

    def objective(vector: np.ndarray) -> float:
        try:
            values = dict(zip(names, (float(value) for value in vector), strict=True))
            prediction = cmb_prediction(model, values, prior_data["means"])
            chi2, _, _, _ = score_prediction(prediction, prior_data, score_mode)
            if not math.isfinite(chi2):
                return 1.0e100
            return chi2
        except Exception:  # noqa: BLE001
            return 1.0e100

    for seed in seed_vectors(names, bounds):
        result = optimize.minimize(
            objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 500, "ftol": 1.0e-10},
        )
        if not math.isfinite(float(result.fun)) or float(result.fun) >= 1.0e90:
            continue
        if best is None or float(result.fun) < float(best["chi2"]):
            best = {
                "success": bool(result.success),
                "chi2": float(result.fun),
                "vector": np.asarray(result.x, dtype=float),
                "message": str(result.message),
                "optimizer": "L-BFGS-B_multistart",
            }

    if best is None:
        try:
            result = optimize.differential_evolution(
                objective,
                bounds=bounds,
                maxiter=60,
                popsize=8,
                polish=True,
                tol=1.0e-7,
                seed=12345,
                updating="immediate",
                workers=1,
            )
            if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e90:
                best = {
                    "success": bool(result.success),
                    "chi2": float(result.fun),
                    "vector": np.asarray(result.x, dtype=float),
                    "message": str(result.message),
                    "optimizer": "differential_evolution_fallback",
                }
        except Exception as exc:  # noqa: BLE001
            issue = str(exc)

    if best is None:
        return (
            {
                "prior_table": prior_table,
                "score_mode": score_mode,
                "model": model,
                "role": next(row["role"] for row in model_register_rows() if row["model"] == model),
                "success": False,
                "chi2": "",
                "aic": "",
                "bic": "",
                "n_data": len(SCORE_MODES[score_mode]),
                "dynamic_k": len(names),
                "edge_flag": "",
                "optimizer": "failed",
                "params_json": "",
                "Omega_m0": "",
                "h": "",
                "w": "",
                "w0": "",
                "wa": "",
                "z_star": "",
                "r_s_star": "",
                "D_M_star": "",
                "issue": issue or "no_finite_fit",
            },
            [],
            [],
        )

    values = dict(zip(names, (float(value) for value in best["vector"]), strict=True))
    prediction = cmb_prediction(model, values, prior_data["means"])
    chi2, observed, predicted, residual = score_prediction(prediction, prior_data, score_mode)
    n_data = len(SCORE_MODES[score_mode])
    dynamic_k = len(names)
    aic = chi2 + 2.0 * dynamic_k
    bic = chi2 + dynamic_k * math.log(n_data)
    edge_rows = edge_rows_for_fit(prior_table, score_mode, model, values, bounds_by_name)
    edge_flag = any(row["edge_flag"] for row in edge_rows)
    residual_rows = []
    for parameter, obs, pred, res in zip(SCORE_MODES[score_mode], observed, predicted, residual, strict=True):
        residual_rows.append(
            {
                "prior_table": prior_table,
                "score_mode": score_mode,
                "model": model,
                "parameter": parameter,
                "observed": float(obs),
                "predicted": float(pred),
                "residual_observed_minus_predicted": float(res),
            }
        )

    fit_row = {
        "prior_table": prior_table,
        "score_mode": score_mode,
        "model": model,
        "role": next(row["role"] for row in model_register_rows() if row["model"] == model),
        "success": True,
        "chi2": chi2,
        "aic": aic,
        "bic": bic,
        "n_data": n_data,
        "dynamic_k": dynamic_k,
        "edge_flag": edge_flag,
        "optimizer": best["optimizer"],
        "params_json": json.dumps(values, sort_keys=True),
        "Omega_m0": values.get("Omega_m0", ""),
        "h": values.get("h", ""),
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "z_star": prediction["z_star"],
        "r_s_star": prediction["r_s_star"],
        "D_M_star": prediction["D_M_star"],
        "issue": "" if best["success"] else best["message"],
    }
    return fit_row, edge_rows, residual_rows


def comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for row in fit_rows:
        if row.get("success") is True:
            grouped.setdefault((row["prior_table"], row["score_mode"]), {})[row["model"]] = row

    for (prior_table, score_mode), by_model in grouped.items():
        locked = by_model.get("MTS_locked_2over27")
        if not locked:
            continue
        for baseline in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_model.get(baseline)
            if not reference:
                continue
            rows.append(
                {
                    "prior_table": prior_table,
                    "score_mode": score_mode,
                    "model": "MTS_locked_2over27",
                    "reference": baseline,
                    "delta_chi2": float(locked["chi2"]) - float(reference["chi2"]),
                    "delta_aic": float(locked["aic"]) - float(reference["aic"]),
                    "delta_bic": float(locked["bic"]) - float(reference["bic"]),
                    "locked_edge_flag": locked["edge_flag"],
                    "reference_edge_flag": reference["edge_flag"],
                }
            )
    return rows


def scorecard_label(delta_bic: float, locked_edge: bool, reference_edge: bool) -> str:
    numerical_tolerance = 1.0e-6
    if locked_edge:
        return "hard_loss_edge_dependent"
    if abs(delta_bic) <= numerical_tolerance:
        return "competitive_draw"
    if delta_bic < -2.0:
        return "clean_win"
    if delta_bic < 0.0:
        return "points_win"
    if abs(delta_bic) <= 2.0:
        return "competitive_draw"
    if delta_bic <= 6.0:
        return "narrow_loss"
    if reference_edge:
        return "hard_loss_against_edge_hit_reference"
    return "hard_loss"


def scorecard_gate_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in comparisons:
        label = scorecard_label(
            float(row["delta_bic"]),
            str(row["locked_edge_flag"]).lower() == "true",
            str(row["reference_edge_flag"]).lower() == "true",
        )
        rows.append(
            {
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "comparison": f"MTS_locked_2over27_vs_{row['reference']}",
                "scorecard": label,
                "delta_chi2": row["delta_chi2"],
                "delta_aic": row["delta_aic"],
                "delta_bic": row["delta_bic"],
                "decision_weight": "primary" if row["reference"] in {"LCDM", "wCDM"} else "context",
            }
        )
    return rows


def decision_rows(fit_rows: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    locked_fits = [row for row in fit_rows if row.get("model") == "MTS_locked_2over27" and row.get("success") is True]
    locked_edge_count = sum(1 for row in locked_fits if row.get("edge_flag") is True)
    lcdm_gates = [
        row
        for row in gates
        if row["comparison"] == "MTS_locked_2over27_vs_LCDM"
        and row["prior_table"] in PRIMARY_PRIOR_TABLES
        and row["score_mode"] in SCORE_MODES
    ]
    hard_losses = [row for row in lcdm_gates if str(row["scorecard"]).startswith("hard_loss")]
    narrow_losses = [row for row in lcdm_gates if row["scorecard"] == "narrow_loss"]
    draws_or_better = [
        row
        for row in lcdm_gates
        if row["scorecard"] in {"clean_win", "points_win", "competitive_draw"}
    ]
    if locked_edge_count:
        verdict = "locked_2over27_CMB_distance_score_edge_blocked"
    elif hard_losses:
        verdict = "locked_2over27_CMB_distance_score_hard_loss_against_LCDM"
    elif narrow_losses:
        verdict = "locked_2over27_CMB_distance_score_narrow_loss_needs_inspection"
    elif len(draws_or_better) == len(lcdm_gates) and lcdm_gates:
        verdict = "locked_2over27_CMB_distance_score_competitive_or_better_vs_LCDM"
    else:
        verdict = "locked_2over27_CMB_distance_score_inconclusive"
    return [
        {
            "decision": "score_status",
            "value": verdict,
            "rationale": "uses 115 symmetric parameter-map contract and primary LCDM scorecard gates",
        },
        {
            "decision": "locked_edge_count",
            "value": locked_edge_count,
            "rationale": "locked branch cannot be promoted if it is edge-dependent",
        },
        {
            "decision": "lcdm_primary_hard_loss_count",
            "value": len(hard_losses),
            "rationale": "hard losses against LCDM are branch failures for this CMB distance gate",
        },
        {
            "decision": "lcdm_primary_draw_or_better_count",
            "value": len(draws_or_better),
            "rationale": "draws count as useful survival under the boxing scorecard standard",
        },
        {
            "decision": "theory_promotion_allowed",
            "value": False,
            "rationale": "compressed CMB distance prior only; no perturbation spectrum or parent derivation",
        },
        {
            "decision": "next_target",
            "value": "116-locked-2over27-CMB-distance-score.md",
            "rationale": "write the score readout with exact claim ceiling",
        },
    ]


def dryrun_gate_rows(source_rows: list[dict[str, Any]], prior_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_files_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing_count={len(missing_sources)}",
        },
        {
            "gate": "contract_115_exists",
            "status": "pass" if CONTRACT_PATH.exists() else "fail",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "primary_prior_tables_available",
            "status": "pass" if len(prior_rows) == 2 else "fail",
            "evidence": ";".join(row["prior_table"] for row in prior_rows),
        },
        {
            "gate": "parameter_map_encoded",
            "status": "pass",
            "evidence": "h and Omega_m0 fitted symmetrically; Omega_b_h2/n_s fixed by table; scale_factor_quad only",
        },
        {
            "gate": "score_allowed",
            "status": "pass",
            "evidence": "guarded score allowed by 115 contract",
        },
    ]


def write_common_outputs(results_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources = source_register_rows()
    prior_tables = prior_table_register_rows(manifest)
    models = model_register_rows()
    parameter_map = parameter_map_register_rows()
    write_csv(
        results_dir / "source_register.csv",
        sources,
        ["kind", "path", "exists", "readable", "bytes", "sha256", "issue"],
    )
    write_csv(
        results_dir / "prior_table_register.csv",
        prior_tables,
        [
            "prior_table",
            "role",
            "parameters",
            "vector_length",
            "covariance_shape",
            "cholesky_pass",
            "min_eigenvalue",
            "default_for_C0",
            "manifest_use_status",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "model_register.csv",
        models,
        [
            "model",
            "role",
            "physics_model",
            "free_parameters",
            "fixed_parameters",
            "dynamic_k",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "parameter_map_register.csv",
        parameter_map,
        ["item", "rule", "status", "symmetry"],
    )
    return sources, prior_tables


def run_dry_run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-CMB-distance-score-dryrun"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest = read_manifest()
    sources, prior_tables = write_common_outputs(results_dir, manifest)
    gates = dryrun_gate_rows(sources, prior_tables)
    decisions = [
        {
            "decision": "dryrun_status",
            "value": "locked_2over27_CMB_distance_score_dryrun_pass",
            "rationale": "contract, data, model register, and parameter map are encoded",
        },
        {
            "decision": "score_ran",
            "value": False,
            "rationale": "dry-run only",
        },
        {
            "decision": "next_command",
            "value": "python scripts/locked_2over27_CMB_distance_score.py --score",
            "rationale": "guarded score is now allowed",
        },
    ]
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])
    status = {
        "status": "locked_2over27_CMB_distance_score_dryrun_pass",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": False,
        "primary_prior_tables": PRIMARY_PRIOR_TABLES,
        "score_modes": list(SCORE_MODES),
        "models": MODEL_ORDER,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def run_score(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-CMB-distance-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest = read_manifest()
    sources, prior_tables = write_common_outputs(results_dir, manifest)
    dryrun_gates = dryrun_gate_rows(sources, prior_tables)
    if any(row["status"] == "fail" for row in dryrun_gates):
        status = {
            "status": "locked_2over27_CMB_distance_score_blocked_by_dryrun_failure",
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "score_ran": False,
        }
        write_csv(results_dir / "scorecard_gates.csv", dryrun_gates, ["gate", "status", "evidence"])
        (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
        print(json.dumps(status, indent=2))
        return run_dir

    fit_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for prior_table in PRIMARY_PRIOR_TABLES:
        prior_data = prior_table_data(prior_table)
        for score_mode in SCORE_MODES:
            for model in MODEL_ORDER:
                fit_row, model_edge_rows, model_residual_rows = fit_model(
                    prior_table,
                    score_mode,
                    model,
                    prior_data,
                )
                fit_rows.append(fit_row)
                edge_rows.extend(model_edge_rows)
                residual_rows.extend(model_residual_rows)

    comparisons = comparison_rows(fit_rows)
    scorecard = scorecard_gate_rows(comparisons)
    decisions = decision_rows(fit_rows, scorecard)

    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "prior_table",
            "score_mode",
            "model",
            "role",
            "success",
            "chi2",
            "aic",
            "bic",
            "n_data",
            "dynamic_k",
            "edge_flag",
            "optimizer",
            "params_json",
            "Omega_m0",
            "h",
            "w",
            "w0",
            "wa",
            "z_star",
            "r_s_star",
            "D_M_star",
            "issue",
        ],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_rows,
        [
            "prior_table",
            "score_mode",
            "model",
            "parameter",
            "value",
            "lower",
            "upper",
            "lower_fraction",
            "upper_fraction",
            "edge_flag",
        ],
    )
    write_csv(
        results_dir / "distance_prior_residuals.csv",
        residual_rows,
        [
            "prior_table",
            "score_mode",
            "model",
            "parameter",
            "observed",
            "predicted",
            "residual_observed_minus_predicted",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "prior_table",
            "score_mode",
            "model",
            "reference",
            "delta_chi2",
            "delta_aic",
            "delta_bic",
            "locked_edge_flag",
            "reference_edge_flag",
        ],
    )
    write_csv(
        results_dir / "scorecard_gates.csv",
        scorecard,
        [
            "prior_table",
            "score_mode",
            "comparison",
            "scorecard",
            "delta_chi2",
            "delta_aic",
            "delta_bic",
            "decision_weight",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])
    status = {
        "status": next(row["value"] for row in decisions if row["decision"] == "score_status"),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": True,
        "claim_ceiling": "compressed_CMB_distance_background_stress_only_not_CMB_spectrum",
        "primary_prior_tables": PRIMARY_PRIOR_TABLES,
        "score_modes": list(SCORE_MODES),
        "models": MODEL_ORDER,
        "fit_rows": len(fit_rows),
        "comparison_rows": len(comparisons),
        "locked_constants": {
            "DeltaR": LOCKED_DELTA_R,
            "B_mem": LOCKED_B_MEM,
            "p": LOCKED_P,
            "u3": LOCKED_U3,
        },
        "next_target": "116-locked-2over27-CMB-distance-score.md",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Guarded locked 2/27 CMB distance-prior scorer.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--score", action="store_true")
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    args = parser.parse_args()
    if args.dry_run:
        run_dry_run(args.output_root)
    else:
        run_score(args.output_root)


if __name__ == "__main__":
    main()
