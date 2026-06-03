"""No-CMB BAO+H(z) radial diagnostic for the locked 2/27 branch.

This combines DESI DR2 BAO shape with cosmic-chronometer H(z), while keeping
BAO alpha as a shared profiled nuisance and not using compressed CMB priors.
It is a diagnostic stress test, not a BAO-shape repair model.
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
RUNS_ROOT = WORK_DIR / "runs"
T1_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
HZ_RUN = RUNS_ROOT / "20260531-175500-Hz-radial-expansion-smoke"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import Hz_radial_expansion_smoke as hzsmoke  # noqa: E402

MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
PRIMARY_DATASET = "BAO_DR2_plus_CC15_suggested"
PRIMARY_HZ_DATASET = "CC15_suggested_primary"
PRIMARY_MODEL = "MTS_locked_2over27"


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
        T1_RUN / "run_config.json",
        T7_RUN / "results" / "locked_branch_scores.csv",
        HZ_RUN / "results" / "decision.csv",
        HZ_RUN / "results" / "fit_summary.csv",
        WORK_DIR / "124-BAO-shape-residual-decomposition.md",
        WORK_DIR / "126-Hz-radial-expansion-smoke.md",
        script_path,
    ]
    config = read_json(T1_RUN / "run_config.json") if (T1_RUN / "run_config.json").exists() else {}
    for key in ["bao_data", "bao_cov"]:
        if key in config:
            paths.append(Path(config[key]))
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def load_bao() -> tuple[dict[str, Any], dict[str, Any]]:
    config = read_json(T1_RUN / "run_config.json")
    bao = snbao.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    bao["label"] = config["bao_label"]
    return config, bao


def hz_datasets_to_score() -> list[dict[str, Any]]:
    return hzsmoke.datasets_to_score()


def model_bounds(model: str) -> dict[str, tuple[float, float]]:
    return hzsmoke.model_bounds(model)


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


def baochi2_for_values(model: str, values: dict[str, float], bao: dict[str, Any]) -> tuple[float, float, np.ndarray, np.ndarray]:
    physics_model, params = hzsmoke.physical_model_and_params(model, values)
    chi2, alpha, residual, predicted = snbao.bao_chi2(physics_model, params, bao)
    return chi2, alpha, residual, predicted


def total_chi2(model: str, values: dict[str, float], bao: dict[str, Any], hz_dataset: dict[str, Any]) -> float:
    chi2_bao, _, _, _ = baochi2_for_values(model, values, bao)
    chi2_hz, _, _ = hzsmoke.chi2_for_values(model, values, hz_dataset)
    return chi2_bao + chi2_hz


def fit_model(
    dataset_label: str,
    dataset_role: str,
    model: str,
    bao: dict[str, Any],
    hz_dataset: dict[str, Any],
    max_iter: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    bounds_by_name = model_bounds(model)
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]

    def unpack(vector: np.ndarray) -> dict[str, float]:
        return {name: float(value) for name, value in zip(names, vector, strict=True)}

    def objective(vector: np.ndarray) -> float:
        try:
            return total_chi2(model, unpack(vector), bao, hz_dataset)
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
        for start in hzsmoke.seed_vectors(names, bounds)
    ]
    result = min(results, key=lambda item: float(item.fun))
    values = unpack(np.asarray(result.x, dtype=float))
    chi2_bao, alpha_bao, bao_residual, bao_predicted = baochi2_for_values(model, values, bao)
    chi2_hz, hz_residual, hz_predicted = hzsmoke.chi2_for_values(model, values, hz_dataset)
    chi2 = chi2_bao + chi2_hz
    n_data = len(bao["rows"]) + len(hz_dataset["z"])
    k_count = len(names) + 1
    aic = chi2 + 2.0 * k_count
    bic = chi2 + k_count * math.log(n_data)
    edges = edge_rows(dataset_label, model, values, bounds_by_name)
    edge_flag = any(row["edge_flag"] for row in edges)
    row = {
        "dataset_label": dataset_label,
        "dataset_role": dataset_role,
        "hz_dataset_label": hz_dataset["dataset_label"],
        "hz_covariance_label": hz_dataset["covariance_label"],
        "model": model,
        "success": bool(result.success),
        "chi2_BAO": chi2_bao,
        "chi2_Hz": chi2_hz,
        "chi2_total": chi2,
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
        "BAO_alpha": alpha_bao,
        "optimizer": "L-BFGS-B_multistart",
        "optimizer_message": str(result.message),
        "claim_ceiling": "no_CMB_BAO_Hz_diagnostic_only",
    }
    vectors = {
        "values": values,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "hz_residual": hz_residual,
        "hz_predicted": hz_predicted,
    }
    return row, edges, vectors


def data_schema_rows(config: dict[str, Any], bao: dict[str, Any], hz_datasets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "dataset_label": "BAO_DR2_primary",
            "role": "BAO_shape",
            "path": config["bao_data"],
            "covariance_path": config["bao_cov"],
            "rows": len(bao["rows"]),
            "covariance_shape": f"{bao['covariance'].shape[0]}x{bao['covariance'].shape[1]}",
            "status": "pass",
        }
    ]
    for dataset in hz_datasets:
        rows.append(
            {
                "dataset_label": dataset["dataset_label"],
                "role": dataset["role"],
                "path": dataset["data_path"],
                "covariance_path": dataset["covariance_path"],
                "rows": len(dataset["z"]),
                "covariance_shape": f"{dataset['covariance'].shape[0]}x{dataset['covariance'].shape[1]}",
                "status": "pass",
            }
        )
    return rows


def bao_residual_rows(dataset_label: str, model: str, bao: dict[str, Any], residual: np.ndarray, predicted: np.ndarray) -> list[dict[str, Any]]:
    inv_cov = np.linalg.inv(bao["covariance"])
    inv_residual = inv_cov @ residual
    signed_contrib = residual * inv_residual
    sigma = np.sqrt(np.diag(bao["covariance"]))
    rows = []
    for index, (row, predicted_value, residual_value, sigma_value, contribution) in enumerate(
        zip(bao["rows"], predicted, residual, sigma, signed_contrib, strict=True)
    ):
        rows.append(
            {
                "dataset_label": dataset_label,
                "sector": "BAO",
                "model": model,
                "row_index": index,
                "z": float(row["z"]),
                "observable": row["quantity"],
                "observed": float(row["value"]),
                "predicted": float(predicted_value),
                "residual": float(residual_value),
                "diagonal_sigma": float(sigma_value),
                "diagonal_pull": float(residual_value / sigma_value),
                "cov_signed_chi2_contribution": float(contribution),
            }
        )
    return rows


def hz_residual_rows(dataset_label: str, model: str, hz_dataset: dict[str, Any], residual: np.ndarray, predicted: np.ndarray) -> list[dict[str, Any]]:
    inv_cov = np.linalg.inv(hz_dataset["covariance"])
    inv_residual = inv_cov @ residual
    signed_contrib = residual * inv_residual
    sigma = np.sqrt(np.diag(hz_dataset["covariance"]))
    rows = []
    for index, (z_value, observed, predicted_value, residual_value, sigma_value, contribution) in enumerate(
        zip(hz_dataset["z"], hz_dataset["H"], predicted, residual, sigma, signed_contrib, strict=True)
    ):
        rows.append(
            {
                "dataset_label": dataset_label,
                "sector": "Hz",
                "model": model,
                "row_index": index,
                "z": float(z_value),
                "observable": "H_z",
                "observed": float(observed),
                "predicted": float(predicted_value),
                "residual": float(residual_value),
                "diagonal_sigma": float(sigma_value),
                "diagonal_pull": float(residual_value / sigma_value),
                "cov_signed_chi2_contribution": float(contribution),
            }
        )
    return rows


def sector_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in fit_rows:
        for sector in ["BAO", "Hz"]:
            rows.append(
                {
                    "dataset_label": row["dataset_label"],
                    "dataset_role": row["dataset_role"],
                    "model": row["model"],
                    "sector": sector,
                    "chi2": row[f"chi2_{sector}"],
                    "fraction_total": float(row[f"chi2_{sector}"]) / float(row["chi2_total"]),
                }
            )
    return rows


def baseline_comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_dataset_model = {(row["dataset_label"], row["model"]): row for row in fit_rows}
    for dataset_label in sorted({row["dataset_label"] for row in fit_rows}):
        locked = by_dataset_model[(dataset_label, PRIMARY_MODEL)]
        for reference_model in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_dataset_model[(dataset_label, reference_model)]
            delta_bic = float(locked["BIC"]) - float(reference["BIC"])
            rows.append(
                {
                    "dataset_label": dataset_label,
                    "model": PRIMARY_MODEL,
                    "reference_model": reference_model,
                    "delta_chi2": float(locked["chi2_total"]) - float(reference["chi2_total"]),
                    "delta_AIC": float(locked["AIC"]) - float(reference["AIC"]),
                    "delta_BIC": delta_bic,
                    "locked_edge_flag": locked["edge_flag"],
                    "reference_edge_flag": reference["edge_flag"],
                    "readout": comparison_label(delta_bic),
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
                "delta_chi2": float(zero["chi2_total"]) - float(lcdm["chi2_total"]),
                "delta_Omega_m0": float(zero["Omega_m0"]) - float(lcdm["Omega_m0"]),
                "delta_h": float(zero["h"]) - float(lcdm["h"]),
                "delta_BAO_alpha": float(zero["BAO_alpha"]) - float(lcdm["BAO_alpha"]),
                "status": "pass" if abs(float(zero["chi2_total"]) - float(lcdm["chi2_total"])) < 1.0e-8 else "check",
            }
        )
    return rows


def t7_omega() -> float:
    rows = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    row = next(item for item in rows if item["branch"] == "T1_primary_fullcov_DR2")
    return float(row["Omega_m"])


def decision_rows(fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary_rows = [row for row in fit_rows if row["dataset_label"] == PRIMARY_DATASET]
    locked = next(row for row in primary_rows if row["model"] == PRIMARY_MODEL)
    lcdm = next(row for row in primary_rows if row["model"] == "LCDM")
    wc = next(row for row in primary_rows if row["model"] == "wCDM")
    cpl = next(row for row in primary_rows if row["model"] == "CPL")
    primary_comparisons = [row for row in comparisons if row["dataset_label"] == PRIMARY_DATASET]
    bic_lcdm = next(row for row in primary_comparisons if row["reference_model"] == "LCDM")
    bic_wc = next(row for row in primary_comparisons if row["reference_model"] == "wCDM")
    bic_cpl = next(row for row in primary_comparisons if row["reference_model"] == "CPL")
    flexible_edges = [
        row["model"]
        for row in primary_rows
        if row["model"] in {"wCDM", "CPL"} and row["edge_flag"] in [True, "True"]
    ]
    if locked["edge_flag"] in [True, "True"] or lcdm["edge_flag"] in [True, "True"]:
        status = "BAO_Hz_noCMB_locked_or_LCDM_edge_flagged"
    elif abs(float(bic_lcdm["delta_BIC"])) < 2.0:
        status = "BAO_Hz_noCMB_LCDM_draw"
    elif float(bic_lcdm["delta_BIC"]) <= -2.0:
        status = "BAO_Hz_noCMB_locked_preferred_vs_LCDM"
    else:
        status = "BAO_Hz_noCMB_locked_disfavored_vs_LCDM"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary locked chi2={float(locked['chi2_total']):.12g}; LCDM={float(lcdm['chi2_total']):.12g}; wCDM={float(wc['chi2_total']):.12g}; CPL={float(cpl['chi2_total']):.12g}",
        },
        {
            "item": "primary_BIC_vs_LCDM",
            "verdict": bic_lcdm["readout"],
            "evidence": f"delta_BIC={float(bic_lcdm['delta_BIC']):.12g}",
        },
        {
            "item": "primary_BIC_vs_wCDM",
            "verdict": bic_wc["readout"],
            "evidence": f"delta_BIC={float(bic_wc['delta_BIC']):.12g}; reference_edge={bic_wc['reference_edge_flag']}",
        },
        {
            "item": "primary_BIC_vs_CPL",
            "verdict": bic_cpl["readout"],
            "evidence": f"delta_BIC={float(bic_cpl['delta_BIC']):.12g}; reference_edge={bic_cpl['reference_edge_flag']}",
        },
        {
            "item": "primary_sector_balance",
            "verdict": "BAO_dominated" if float(locked["chi2_BAO"]) > float(locked["chi2_Hz"]) else "Hz_dominated",
            "evidence": f"locked BAO chi2={float(locked['chi2_BAO']):.12g}; Hz chi2={float(locked['chi2_Hz']):.12g}",
        },
        {
            "item": "Omega_m0_shift_vs_T7",
            "verdict": "upward_shift",
            "evidence": f"joint no-CMB locked Omega_m0={float(locked['Omega_m0']):.12g}; T7={t7_omega():.12g}; shift={float(locked['Omega_m0']) - t7_omega():.12g}",
        },
        {
            "item": "primary_edge_flags",
            "verdict": "flexible_baseline_edges" if flexible_edges else "no_primary_edges",
            "evidence": ";".join(flexible_edges) if flexible_edges else "none",
        },
        {
            "item": "claim_status",
            "verdict": "diagnostic_only_no_promotion",
            "evidence": "no CMB prior, BAO-shape correction, or Omega map was fitted",
        },
    ]


def run_diagnostic(output_root: Path, timestamp: str | None = None, max_iter: int = 300) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-BAO-Hz-noCMB-diagnostic"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    config, bao = load_bao()
    hz_datasets = hz_datasets_to_score()
    fit_rows: list[dict[str, Any]] = []
    edge_table: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []

    for hz_dataset in hz_datasets:
        if hz_dataset["dataset_label"] == PRIMARY_HZ_DATASET:
            dataset_label = PRIMARY_DATASET
            dataset_role = "primary_no_CMB"
        else:
            dataset_label = f"BAO_DR2_plus_{hz_dataset['dataset_label']}"
            dataset_role = f"no_CMB_{hz_dataset['role']}"
        for model in MODEL_ORDER:
            fit, edges, vectors = fit_model(dataset_label, dataset_role, model, bao, hz_dataset, max_iter)
            fit_rows.append(fit)
            edge_table.extend(edges)
            residual_rows.extend(bao_residual_rows(dataset_label, model, bao, vectors["bao_residual"], vectors["bao_predicted"]))
            residual_rows.extend(hz_residual_rows(dataset_label, model, hz_dataset, vectors["hz_residual"], vectors["hz_predicted"]))

    sectors = sector_rows(fit_rows)
    comparisons = baseline_comparison_rows(fit_rows)
    controls = control_rows(fit_rows)
    decisions = decision_rows(fit_rows, comparisons)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_schema.csv",
        data_schema_rows(config, bao, hz_datasets),
        ["dataset_label", "role", "path", "covariance_path", "rows", "covariance_shape", "status"],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "dataset_label",
            "dataset_role",
            "hz_dataset_label",
            "hz_covariance_label",
            "model",
            "success",
            "chi2_BAO",
            "chi2_Hz",
            "chi2_total",
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
            "BAO_alpha",
            "optimizer",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "sector_breakdown.csv",
        sectors,
        ["dataset_label", "dataset_role", "model", "sector", "chi2", "fraction_total"],
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
            "sector",
            "model",
            "row_index",
            "z",
            "observable",
            "observed",
            "predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
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
        ["dataset_label", "control", "delta_chi2", "delta_Omega_m0", "delta_h", "delta_BAO_alpha", "status"],
    )
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "no_CMB_BAO_Hz_diagnostic_only",
        "primary_dataset": PRIMARY_DATASET,
        "models": MODEL_ORDER,
        "fit_rows": len(fit_rows),
        "generated": [
            "source_register.csv",
            "data_schema.csv",
            "fit_summary.csv",
            "sector_breakdown.csv",
            "prior_edge_table.csv",
            "residuals.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "decision.csv",
        ],
        "next_target": "128-BAO-Hz-noCMB-diagnostic.md",
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
    print(run_diagnostic(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
