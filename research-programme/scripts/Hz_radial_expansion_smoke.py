"""H(z) radial-expansion smoke test for the locked 2/27 branch.

This script fits H(z)=100 h E(z) to local cosmic-chronometer data using the
same rows/covariance for LCDM, wCDM, CPL, MTS_locked_2over27, and MTS_Bmem_zero.
It is a radial consistency stress test, not a BAO/CMB repair model.
"""

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
from scipy import optimize

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
ROOT = WORK_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
DATA_ROOT = ROOT / "formalization-workbench" / "data" / "cosmology" / "cosmic_chronometers"
COV_BRANCH_DIR = DATA_ROOT / "covariance_branch"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402

HZ_32 = DATA_ROOT / "Hz.csv"
SOURCE_METADATA = DATA_ROOT / "source_metadata.json"
HZ_15 = COV_BRANCH_DIR / "Hz_CC_Moresco15_BC03.csv"
COVARIANCE_FILES = {
    "diagonal_total_error": COV_BRANCH_DIR / "covariance_diagonal_total_error.csv",
    "suggested": COV_BRANCH_DIR / "covariance_suggested.csv",
    "conservative": COV_BRANCH_DIR / "covariance_conservative.csv",
    "extra_conservative": COV_BRANCH_DIR / "covariance_extra_conservative.csv",
    "nonstat_systematic_only": COV_BRANCH_DIR / "covariance_nonstat_systematic_only.csv",
}
ROUTE_RUN = RUNS_ROOT / "20260531-174600-Hz-radial-stress-route-gate"

MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
PRIMARY_DATASET = "CC15_suggested_primary"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        HZ_32,
        SOURCE_METADATA,
        HZ_15,
        *COVARIANCE_FILES.values(),
        ROUTE_RUN / "results" / "decision.csv",
        WORK_DIR / "125-BAO-shape-theorem-target-or-non-CMB-stress-route.md",
        script_path,
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def read_covariance_matrix(path: Path) -> tuple[list[float], np.ndarray]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        z_header = [float(value) for value in header[1:]]
        rows = [[float(value) for value in row[1:]] for row in reader]
    matrix = np.asarray(rows, dtype=float)
    if matrix.shape != (len(z_header), len(z_header)):
        raise ValueError(f"bad covariance shape {matrix.shape} for {path}")
    return z_header, matrix


def load_hz15_dataset(covariance_label: str, dataset_label: str, role: str) -> dict[str, Any]:
    rows = read_csv_rows(HZ_15)
    z = np.asarray([float(row["z"]) for row in rows], dtype=float)
    h_obs = np.asarray([float(row["H"]) for row in rows], dtype=float)
    sigma = np.asarray([float(row["sigma"]) for row in rows], dtype=float)
    cov_z, covariance = read_covariance_matrix(COVARIANCE_FILES[covariance_label])
    if len(cov_z) != len(z) or np.max(np.abs(np.asarray(cov_z, dtype=float) - z)) > 1.0e-8:
        raise ValueError(f"covariance redshift header mismatch for {covariance_label}")
    return {
        "dataset_label": dataset_label,
        "role": role,
        "data_path": str(HZ_15),
        "covariance_label": covariance_label,
        "covariance_path": str(COVARIANCE_FILES[covariance_label]),
        "covariance_mode": "full",
        "rows_raw": rows,
        "z": z,
        "H": h_obs,
        "sigma": sigma,
        "covariance": covariance,
    }


def load_hz32_diagonal_dataset() -> dict[str, Any]:
    rows = read_csv_rows(HZ_32)
    z = np.asarray([float(row["z"]) for row in rows], dtype=float)
    h_obs = np.asarray([float(row["H"]) for row in rows], dtype=float)
    sigma = np.asarray([float(row["sigma"]) for row in rows], dtype=float)
    return {
        "dataset_label": "CC32_diagonal_sensitivity",
        "role": "diagonal_sensitivity",
        "data_path": str(HZ_32),
        "covariance_label": "diagonal_sigma",
        "covariance_path": "",
        "covariance_mode": "diagonal",
        "rows_raw": rows,
        "z": z,
        "H": h_obs,
        "sigma": sigma,
        "covariance": np.diag(sigma * sigma),
    }


def datasets_to_score() -> list[dict[str, Any]]:
    return [
        load_hz15_dataset("suggested", PRIMARY_DATASET, "primary"),
        load_hz15_dataset("diagonal_total_error", "CC15_diagonal_total_error_sensitivity", "covariance_sensitivity"),
        load_hz15_dataset("conservative", "CC15_conservative_sensitivity", "covariance_sensitivity"),
        load_hz15_dataset("extra_conservative", "CC15_extra_conservative_sensitivity", "covariance_sensitivity"),
        load_hz15_dataset("nonstat_systematic_only", "CC15_nonstat_systematic_only_diagnostic", "diagnostic_only"),
        load_hz32_diagonal_dataset(),
    ]


def model_bounds(model: str) -> dict[str, tuple[float, float]]:
    bounds: dict[str, tuple[float, float]] = {
        "Omega_m0": (0.05, 0.60),
        "h": (0.45, 0.90),
    }
    if model == "wCDM":
        bounds["w"] = (-2.0, -0.2)
    if model == "CPL":
        bounds["w0"] = (-2.0, -0.2)
        bounds["wa"] = (-2.0, 2.0)
    return bounds


def physical_model_and_params(model: str, values: dict[str, float]) -> tuple[str, dict[str, float]]:
    params = {"Omega_m": values["Omega_m0"]}
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


def h_prediction(model: str, values: dict[str, float], z: np.ndarray) -> np.ndarray:
    physics_model, params = physical_model_and_params(model, values)
    return 100.0 * values["h"] * snbao.e_z(physics_model, z, params)


def chi2_for_values(model: str, values: dict[str, float], dataset: dict[str, Any]) -> tuple[float, np.ndarray, np.ndarray]:
    predicted = h_prediction(model, values, dataset["z"])
    residual = dataset["H"] - predicted
    inv_cov = np.linalg.inv(dataset["covariance"])
    chi2 = float(residual @ inv_cov @ residual)
    return chi2, residual, predicted


def seed_vectors(names: list[str], bounds: list[tuple[float, float]]) -> list[np.ndarray]:
    defaults = {
        "Omega_m0": 0.30,
        "h": 0.68,
        "w": -1.0,
        "w0": -1.0,
        "wa": 0.0,
    }
    seed_dicts = [
        defaults,
        {**defaults, "Omega_m0": 0.25, "h": 0.72},
        {**defaults, "Omega_m0": 0.35, "h": 0.65},
        {**defaults, "Omega_m0": 0.20, "h": 0.75},
        {**defaults, "Omega_m0": 0.45, "h": 0.58},
        {**defaults, "w": -0.8, "w0": -0.8, "wa": 0.5},
        {**defaults, "w": -1.2, "w0": -1.2, "wa": -0.5},
    ]
    vectors: list[np.ndarray] = []
    for seed in seed_dicts:
        values = []
        for name, (lower, upper) in zip(names, bounds, strict=True):
            values.append(min(max(seed.get(name, 0.5 * (lower + upper)), lower), upper))
        vector = np.asarray(values, dtype=float)
        if not any(np.allclose(vector, previous) for previous in vectors):
            vectors.append(vector)
    midpoint = np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)
    if not any(np.allclose(midpoint, previous) for previous in vectors):
        vectors.append(midpoint)
    return vectors


def edge_rows(
    dataset_label: str,
    model: str,
    values: dict[str, float],
    bounds_by_name: dict[str, tuple[float, float]],
) -> list[dict[str, Any]]:
    rows = []
    for name, (lower, upper) in bounds_by_name.items():
        best = values[name]
        width = upper - lower
        distance = min(best - lower, upper - best)
        rows.append(
            {
                "dataset_label": dataset_label,
                "model": model,
                "parameter": name,
                "best_fit": best,
                "lower": lower,
                "upper": upper,
                "distance_to_edge": distance,
                "edge_flag": bool(distance <= 0.01 * width),
            }
        )
    return rows


def fit_model(dataset: dict[str, Any], model: str, max_iter: int) -> tuple[dict[str, Any], list[dict[str, Any]], np.ndarray, np.ndarray]:
    bounds_by_name = model_bounds(model)
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]

    def unpack(vector: np.ndarray) -> dict[str, float]:
        return {name: float(value) for name, value in zip(names, vector, strict=True)}

    def objective(vector: np.ndarray) -> float:
        try:
            values = unpack(vector)
            chi2, _, _ = chi2_for_values(model, values, dataset)
            return chi2
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return 1.0e30

    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-10},
        )
        for start in seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    chi2, residual, predicted = chi2_for_values(model, values, dataset)
    edge = edge_rows(dataset["dataset_label"], model, values, bounds_by_name)
    edge_flag = any(row["edge_flag"] for row in edge)
    n_data = len(dataset["z"])
    k_count = len(names)
    aic = chi2 + 2.0 * k_count
    bic = chi2 + k_count * math.log(n_data)
    row = {
        "dataset_label": dataset["dataset_label"],
        "dataset_role": dataset["role"],
        "covariance_label": dataset["covariance_label"],
        "covariance_mode": dataset["covariance_mode"],
        "model": model,
        "success": bool(result.success),
        "chi2": chi2,
        "AIC": aic,
        "BIC": bic,
        "n_data": n_data,
        "dynamic_k": k_count,
        "dof": n_data - k_count,
        "edge_flag": edge_flag,
        "Omega_m0": values.get("Omega_m0", ""),
        "h": values.get("h", ""),
        "H0": 100.0 * values["h"],
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "optimizer": "L-BFGS-B_multistart",
        "optimizer_message": str(result.message),
        "claim_ceiling": "radial_expansion_stress_only",
    }
    return row, edge, residual, predicted


def residual_rows_for_fit(dataset: dict[str, Any], fit_row: dict[str, Any], residual: np.ndarray, predicted: np.ndarray) -> list[dict[str, Any]]:
    inv_cov = np.linalg.inv(dataset["covariance"])
    inv_residual = inv_cov @ residual
    signed_contrib = residual * inv_residual
    sigma = np.sqrt(np.diag(dataset["covariance"]))
    rows = []
    raw_rows = dataset["rows_raw"]
    for index, (z_value, observed, predicted_value, residual_value, sigma_value, contribution) in enumerate(
        zip(dataset["z"], dataset["H"], predicted, residual, sigma, signed_contrib, strict=True)
    ):
        rows.append(
            {
                "dataset_label": fit_row["dataset_label"],
                "model": fit_row["model"],
                "row_index": index,
                "z": float(z_value),
                "H_observed": float(observed),
                "H_predicted": float(predicted_value),
                "residual": float(residual_value),
                "diagonal_sigma": float(sigma_value),
                "diagonal_pull": float(residual_value / sigma_value),
                "cov_signed_chi2_contribution": float(contribution),
                "reference": raw_rows[index].get("reference", ""),
            }
        )
    return rows


def data_schema_rows(datasets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for dataset in datasets:
        covariance = dataset["covariance"]
        eigvals = np.linalg.eigvalsh(covariance)
        rows.append(
            {
                "dataset_label": dataset["dataset_label"],
                "role": dataset["role"],
                "data_path": dataset["data_path"],
                "covariance_path": dataset["covariance_path"],
                "covariance_label": dataset["covariance_label"],
                "rows": len(dataset["z"]),
                "covariance_shape": f"{covariance.shape[0]}x{covariance.shape[1]}",
                "z_min": float(np.min(dataset["z"])),
                "z_max": float(np.max(dataset["z"])),
                "min_eigenvalue": float(np.min(eigvals)),
                "positive_definite": bool(np.min(eigvals) > 0.0),
                "status": "pass" if np.min(eigvals) > 0.0 else "fail",
            }
        )
    return rows


def baseline_comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_dataset_model = {(row["dataset_label"], row["model"]): row for row in fit_rows}
    for dataset_label in sorted({row["dataset_label"] for row in fit_rows}):
        locked = by_dataset_model[(dataset_label, "MTS_locked_2over27")]
        for reference_model in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_dataset_model[(dataset_label, reference_model)]
            rows.append(
                {
                    "dataset_label": dataset_label,
                    "model": "MTS_locked_2over27",
                    "reference_model": reference_model,
                    "delta_chi2": float(locked["chi2"]) - float(reference["chi2"]),
                    "delta_AIC": float(locked["AIC"]) - float(reference["AIC"]),
                    "delta_BIC": float(locked["BIC"]) - float(reference["BIC"]),
                    "locked_edge_flag": locked["edge_flag"],
                    "reference_edge_flag": reference["edge_flag"],
                    "readout": comparison_label(float(locked["BIC"]) - float(reference["BIC"])),
                }
            )
    return rows


def comparison_label(delta_bic: float) -> str:
    if delta_bic <= -2.0:
        return "locked_preferred_by_BIC"
    if delta_bic < 2.0:
        return "competitive_draw_by_BIC"
    return "locked_disfavored_by_BIC"


def control_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_dataset_model = {(row["dataset_label"], row["model"]): row for row in fit_rows}
    for dataset_label in sorted({row["dataset_label"] for row in fit_rows}):
        lcdm = by_dataset_model[(dataset_label, "LCDM")]
        zero = by_dataset_model[(dataset_label, "MTS_Bmem_zero")]
        rows.append(
            {
                "dataset_label": dataset_label,
                "control": "MTS_Bmem_zero_vs_LCDM",
                "delta_chi2": float(zero["chi2"]) - float(lcdm["chi2"]),
                "delta_Omega_m0": float(zero["Omega_m0"]) - float(lcdm["Omega_m0"]),
                "delta_h": float(zero["h"]) - float(lcdm["h"]),
                "status": "pass"
                if abs(float(zero["chi2"]) - float(lcdm["chi2"])) < 1.0e-8
                else "check",
            }
        )
    return rows


def decision_rows(fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary_fits = [row for row in fit_rows if row["dataset_label"] == PRIMARY_DATASET]
    primary_locked = next(row for row in primary_fits if row["model"] == "MTS_locked_2over27")
    primary_lcdm = next(row for row in primary_fits if row["model"] == "LCDM")
    primary_wc = next(row for row in primary_fits if row["model"] == "wCDM")
    primary_cpl = next(row for row in primary_fits if row["model"] == "CPL")
    primary_comparisons = [row for row in comparisons if row["dataset_label"] == PRIMARY_DATASET]
    locked_and_lcdm_stable = not any(
        row["edge_flag"] in [True, "True"]
        for row in primary_fits
        if row["model"] in {"LCDM", "MTS_locked_2over27", "MTS_Bmem_zero"}
    )
    flexible_edge_models = [
        row["model"]
        for row in primary_fits
        if row["model"] in {"wCDM", "CPL"} and row["edge_flag"] in [True, "True"]
    ]
    bic_vs_lcdm = next(row for row in primary_comparisons if row["reference_model"] == "LCDM")
    bic_vs_wc = next(row for row in primary_comparisons if row["reference_model"] == "wCDM")
    bic_vs_cpl = next(row for row in primary_comparisons if row["reference_model"] == "CPL")
    if not locked_and_lcdm_stable:
        status = "Hz_radial_smoke_locked_or_LCDM_edge_flagged"
    elif flexible_edge_models and abs(float(bic_vs_lcdm["delta_BIC"])) < 2.0:
        status = "Hz_radial_smoke_LCDM_draw_flexible_edges"
    elif float(bic_vs_lcdm["delta_BIC"]) <= 2.0 and float(bic_vs_wc["delta_BIC"]) <= 2.0:
        status = "Hz_radial_smoke_competitive_or_better"
    else:
        status = "Hz_radial_smoke_not_preferred"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary locked chi2={float(primary_locked['chi2']):.12g}; LCDM={float(primary_lcdm['chi2']):.12g}; wCDM={float(primary_wc['chi2']):.12g}; CPL={float(primary_cpl['chi2']):.12g}",
        },
        {
            "item": "primary_BIC_vs_LCDM",
            "verdict": bic_vs_lcdm["readout"],
            "evidence": f"delta_BIC={float(bic_vs_lcdm['delta_BIC']):.12g}",
        },
        {
            "item": "primary_BIC_vs_wCDM",
            "verdict": bic_vs_wc["readout"],
            "evidence": f"delta_BIC={float(bic_vs_wc['delta_BIC']):.12g}",
        },
        {
            "item": "primary_BIC_vs_CPL",
            "verdict": bic_vs_cpl["readout"],
            "evidence": f"delta_BIC={float(bic_vs_cpl['delta_BIC']):.12g}",
        },
        {
            "item": "primary_edge_flags",
            "verdict": "flexible_baseline_edges" if flexible_edge_models else "no_primary_edges",
            "evidence": ";".join(flexible_edge_models) if flexible_edge_models else "none",
        },
        {
            "item": "primary_H0_locked",
            "verdict": "fitted_no_local_prior",
            "evidence": f"H0={float(primary_locked['H0']):.12g}; Omega_m0={float(primary_locked['Omega_m0']):.12g}",
        },
        {
            "item": "claim_status",
            "verdict": "radial_expansion_stress_only_no_promotion",
            "evidence": "no BAO-shape correction, CMB claim, or Omega-map term was fitted",
        },
        {
            "item": "next_target",
            "verdict": "interpret_Hz_result_against_BAO_radial_pressure",
            "evidence": "decide whether radial pressure is independently supported or likely BAO/compressed-bridge-specific",
        },
    ]


def run_smoke(output_root: Path, timestamp: str | None = None, max_iter: int = 300) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Hz-radial-expansion-smoke"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    datasets = datasets_to_score()
    schema_rows = data_schema_rows(datasets)
    fit_rows: list[dict[str, Any]] = []
    edge_table: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []

    for dataset in datasets:
        for model in MODEL_ORDER:
            fit, edges, residual, predicted = fit_model(dataset, model, max_iter)
            fit_rows.append(fit)
            edge_table.extend(edges)
            residual_rows.extend(residual_rows_for_fit(dataset, fit, residual, predicted))

    comparisons = baseline_comparison_rows(fit_rows)
    controls = control_rows(fit_rows)
    decisions = decision_rows(fit_rows, comparisons)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_schema.csv",
        schema_rows,
        [
            "dataset_label",
            "role",
            "data_path",
            "covariance_path",
            "covariance_label",
            "rows",
            "covariance_shape",
            "z_min",
            "z_max",
            "min_eigenvalue",
            "positive_definite",
            "status",
        ],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "dataset_label",
            "dataset_role",
            "covariance_label",
            "covariance_mode",
            "model",
            "success",
            "chi2",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "dof",
            "edge_flag",
            "Omega_m0",
            "h",
            "H0",
            "w",
            "w0",
            "wa",
            "optimizer",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_table,
        ["dataset_label", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(
        results_dir / "residuals.csv",
        residual_rows,
        [
            "dataset_label",
            "model",
            "row_index",
            "z",
            "H_observed",
            "H_predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
            "reference",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "dataset_label",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_edge_flag",
            "reference_edge_flag",
            "readout",
        ],
    )
    write_csv(
        results_dir / "control_reproduction.csv",
        controls,
        ["dataset_label", "control", "delta_chi2", "delta_Omega_m0", "delta_h", "status"],
    )
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "radial_expansion_stress_only",
        "primary_dataset": PRIMARY_DATASET,
        "datasets": [dataset["dataset_label"] for dataset in datasets],
        "models": MODEL_ORDER,
        "fit_rows": len(fit_rows),
        "generated": [
            "source_register.csv",
            "data_schema.csv",
            "fit_summary.csv",
            "prior_edge_table.csv",
            "residuals.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "decision.csv",
        ],
        "next_target": "126-Hz-radial-expansion-smoke.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_smoke(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
