#!/usr/bin/env python3
"""Joint SN+BAO+CMB calibration runner for the locked B_mem=2/27 branch."""

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


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
FORMALIZATION_WORKBENCH = POST_CHECKPOINT.parent / "formalization-workbench"
T1_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
CMB_SCORE_RUN = RUNS_ROOT / "20260531-161215-locked-2over27-CMB-distance-score"
TRANSFER_RUN = RUNS_ROOT / "20260531-162146-locked-2over27-late-CMB-transfer-score"
CONTRACT_118 = POST_CHECKPOINT / "118-locked-2over27-joint-late-CMB-calibration-contract.md"

sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as runner  # noqa: E402
from locked_2over27_CMB_distance_score import (  # noqa: E402
    C_KM_S,
    LOCKED_B_MEM,
    LOCKED_DELTA_R,
    LOCKED_P,
    LOCKED_U3,
    PRIMARY_PRIOR_TABLES,
    SCORE_MODES,
    cmb_prediction,
    prior_table_data,
    score_prediction,
    write_csv,
)


MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
RD_PRIOR_MODES = {
    "broad": (80.0, 200.0),
    "physical": (130.0, 160.0),
}
PHYSICAL_RD_WARNING = (130.0, 160.0)
PRIMARY_MODEL = "MTS_locked_2over27"
PRIMARY_LATE_BRANCH = "T1_primary_fullcov_DR2"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        T1_RUN / "run_config.json",
        T1_RUN / "results" / "fit_summary.csv",
        T7_RUN / "results" / "locked_branch_scores.csv",
        CMB_SCORE_RUN / "results" / "fit_summary.csv",
        TRANSFER_RUN / "results" / "decision.csv",
        CONTRACT_118,
        Path(__file__).resolve(),
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


def load_primary_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config = read_json(T1_RUN / "run_config.json")
    sn = runner.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config.get("sn_max_rows"),
        covariance_path=Path(config["sn_cov"]),
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = runner.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    bao["label"] = config["bao_label"]
    return config, sn, bao


def data_schema_rows(config: dict[str, Any], sn: dict[str, Any], bao: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "dataset": "SN",
            "path": config["sn_data"],
            "rows": len(sn["z"]),
            "covariance_mode": sn["covariance_mode"],
            "observable": sn["observable"],
            "status": "pass",
            "issue": "",
        },
        {
            "dataset": "SN_covariance",
            "path": config["sn_cov"],
            "rows": sn["covariance"].shape[0] if "covariance" in sn else "",
            "covariance_mode": sn["covariance_mode"],
            "observable": sn["observable"],
            "status": "pass" if "covariance" in sn else "not_used",
            "issue": "",
        },
        {
            "dataset": "BAO",
            "path": config["bao_data"],
            "rows": len(bao["rows"]),
            "covariance_mode": "full",
            "observable": bao["label"],
            "status": "pass",
            "issue": "",
        },
        {
            "dataset": "BAO_covariance",
            "path": config["bao_cov"],
            "rows": bao["covariance"].shape[0],
            "covariance_mode": "full",
            "observable": bao["label"],
            "status": "pass",
            "issue": "",
        },
    ]


def model_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "free_parameters": "Omega_m0;h;r_d;SN_offset",
            "fixed_parameters": "flat LCDM",
            "dynamic_k": 4,
        },
        {
            "model": "wCDM",
            "role": "flexible_baseline",
            "free_parameters": "Omega_m0;h;r_d;w;SN_offset",
            "fixed_parameters": "constant w",
            "dynamic_k": 5,
        },
        {
            "model": "CPL",
            "role": "flexible_baseline",
            "free_parameters": "Omega_m0;h;r_d;w0;wa;SN_offset",
            "fixed_parameters": "CPL form",
            "dynamic_k": 6,
        },
        {
            "model": "MTS_locked_2over27",
            "role": "predeclared_locked_branch",
            "free_parameters": "Omega_m0;h;r_d;SN_offset",
            "fixed_parameters": "B_mem=2/27;p=3;u3=1/4;DeltaR=2/9",
            "dynamic_k": 4,
        },
        {
            "model": "MTS_Bmem_zero",
            "role": "negative_control",
            "free_parameters": "Omega_m0;h;r_d;SN_offset",
            "fixed_parameters": "B_mem=0;p=3;u3=1/4",
            "dynamic_k": 4,
        },
    ]


def parameter_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "Omega_m0",
            "rule": "single shared Omega_m0 for SN, BAO, and CMB",
            "status": "encoded",
        },
        {
            "item": "h",
            "rule": "single shared h for BAO alpha and CMB distance",
            "status": "encoded",
        },
        {
            "item": "r_d",
            "rule": "BAO alpha = c/(100 h r_d); r_d is shared nuisance, not parent-derived",
            "status": "encoded",
        },
        {
            "item": "SN_offset",
            "rule": "profiled analytic nuisance common to all branches and counted in k",
            "status": "encoded",
        },
        {
            "item": "CMB",
            "rule": "same repaired scale-factor quadrature and compressed prior tables as checkpoint 116",
            "status": "encoded",
        },
        {
            "item": "MTS_locked",
            "rule": "B_mem=2/27; p=3; u3=1/4; no CMB retune",
            "status": "encoded",
        },
    ]


def joint_bounds(model: str, rd_mode: str) -> dict[str, tuple[float, float]]:
    bounds: dict[str, tuple[float, float]] = {
        "Omega_m0": (0.05, 0.60),
        "h": (0.45, 0.90),
        "r_d": RD_PRIOR_MODES[rd_mode],
    }
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


def bao_physical_chi2(
    physics_model: str,
    params: dict[str, float],
    values: dict[str, float],
    bao: dict[str, Any],
) -> tuple[float, float, np.ndarray, np.ndarray]:
    alpha = C_KM_S / (100.0 * values["h"] * values["r_d"])
    predicted = runner.bao_prediction(physics_model, params, bao, alpha=alpha)
    observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
    covariance = np.asarray(bao["covariance"], dtype=float)
    residual = observed - predicted
    chi2 = float(residual @ np.linalg.inv(covariance) @ residual)
    return chi2, alpha, residual, predicted


def sector_chi2(
    model: str,
    values: dict[str, float],
    sn: dict[str, Any],
    bao: dict[str, Any],
    prior_data: dict[str, Any],
    score_mode: str,
) -> dict[str, Any]:
    physics_model, params = physical_model_and_params(model, values)
    chi2_sn, sn_offset, sn_residual, sn_predicted = runner.sn_chi2(physics_model, params, sn)
    chi2_bao, alpha, bao_residual, bao_predicted = bao_physical_chi2(physics_model, params, values, bao)
    prediction = cmb_prediction(model, values, prior_data["means"])
    chi2_cmb, cmb_observed, cmb_predicted, cmb_residual = score_prediction(prediction, prior_data, score_mode)
    return {
        "physics_model": physics_model,
        "params": params,
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_CMB": chi2_cmb,
        "chi2_total": chi2_sn + chi2_bao + chi2_cmb,
        "SN_offset": sn_offset,
        "BAO_alpha": alpha,
        "sn_residual": sn_residual,
        "sn_predicted": sn_predicted,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "cmb_observed": cmb_observed,
        "cmb_predicted": cmb_predicted,
        "cmb_residual": cmb_residual,
        "cmb_prediction_map": prediction,
    }


def seed_vectors(names: list[str], bounds: list[tuple[float, float]]) -> list[np.ndarray]:
    defaults = [
        {"Omega_m0": 0.315, "h": 0.68, "r_d": 147.0, "w": -1.0, "w0": -1.0, "wa": 0.0},
        {"Omega_m0": 0.3033, "h": 0.684, "r_d": 147.0, "w": -0.9, "w0": -0.9, "wa": 0.0},
        {"Omega_m0": 0.330, "h": 0.667, "r_d": 147.0, "w": -1.0, "w0": -1.0, "wa": 0.0},
        {"Omega_m0": 0.30, "h": 0.70, "r_d": 140.0, "w": -0.8, "w0": -0.8, "wa": 0.5},
        {"Omega_m0": 0.35, "h": 0.64, "r_d": 155.0, "w": -1.2, "w0": -1.2, "wa": -0.5},
    ]
    vectors: list[np.ndarray] = []
    seen: set[tuple[float, ...]] = set()
    for default in defaults:
        values = []
        for name, (lower, upper) in zip(names, bounds, strict=True):
            value = default[name]
            value = min(max(value, lower + 1.0e-7), upper - 1.0e-7)
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


def edge_rows(
    rd_mode: str,
    prior_table: str,
    score_mode: str,
    model: str,
    values: dict[str, float],
    bounds: dict[str, tuple[float, float]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for parameter, (lower, upper) in bounds.items():
        value = values[parameter]
        span = upper - lower
        lower_fraction = (value - lower) / span
        upper_fraction = (upper - value) / span
        rows.append(
            {
                "rd_prior_mode": rd_mode,
                "prior_table": prior_table,
                "score_mode": score_mode,
                "model": model,
                "parameter": parameter,
                "value": value,
                "lower": lower,
                "upper": upper,
                "lower_fraction": lower_fraction,
                "upper_fraction": upper_fraction,
                "edge_flag": lower_fraction <= 0.01 or upper_fraction <= 0.01,
            }
        )
    return rows


def fit_joint_model(
    rd_mode: str,
    prior_table: str,
    score_mode: str,
    model: str,
    sn: dict[str, Any],
    bao: dict[str, Any],
    max_iter: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    prior_data = prior_table_data(prior_table)
    bounds_by_name = joint_bounds(model, rd_mode)
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]
    best: dict[str, Any] | None = None

    def objective(vector: np.ndarray) -> float:
        try:
            values = dict(zip(names, (float(value) for value in vector), strict=True))
            result = sector_chi2(model, values, sn, bao, prior_data, score_mode)
            if not math.isfinite(result["chi2_total"]):
                return 1.0e100
            return float(result["chi2_total"])
        except Exception:  # noqa: BLE001
            return 1.0e100

    for seed in seed_vectors(names, bounds):
        result = optimize.minimize(
            objective,
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-9},
        )
        if math.isfinite(float(result.fun)) and float(result.fun) < 1.0e90:
            if best is None or float(result.fun) < float(best["chi2_total"]):
                best = {
                    "vector": np.asarray(result.x, dtype=float),
                    "chi2_total": float(result.fun),
                    "success": bool(result.success),
                    "message": str(result.message),
                    "optimizer": "L-BFGS-B_multistart",
                }

    if best is None:
        values = {name: "" for name in names}
        row = base_failed_fit_row(rd_mode, prior_table, score_mode, model, len(names) + 1, "no_finite_fit", values)
        return row, [], {}

    values = dict(zip(names, (float(value) for value in best["vector"]), strict=True))
    sector = sector_chi2(model, values, sn, bao, prior_data, score_mode)
    dynamic_k = len(names) + 1
    n_data = len(sn["z"]) + len(bao["rows"]) + len(SCORE_MODES[score_mode])
    aic = sector["chi2_total"] + 2.0 * dynamic_k
    bic = sector["chi2_total"] + dynamic_k * math.log(n_data)
    edges = edge_rows(rd_mode, prior_table, score_mode, model, values, bounds_by_name)
    edge_flag = any(row["edge_flag"] for row in edges)
    row = {
        "rd_prior_mode": rd_mode,
        "prior_table": prior_table,
        "score_mode": score_mode,
        "model": model,
        "success": True,
        "converged": best["success"],
        "chi2_SN": sector["chi2_SN"],
        "chi2_BAO": sector["chi2_BAO"],
        "chi2_CMB": sector["chi2_CMB"],
        "chi2_total": sector["chi2_total"],
        "AIC": aic,
        "BIC": bic,
        "n_data": n_data,
        "dynamic_k": dynamic_k,
        "edge_flag": edge_flag,
        "Omega_m0": values.get("Omega_m0", ""),
        "h": values.get("h", ""),
        "r_d": values.get("r_d", ""),
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "BAO_alpha": sector["BAO_alpha"],
        "SN_offset": sector["SN_offset"],
        "z_star": sector["cmb_prediction_map"]["z_star"],
        "r_s_star": sector["cmb_prediction_map"]["r_s_star"],
        "D_M_star": sector["cmb_prediction_map"]["D_M_star"],
        "optimizer": best["optimizer"],
        "issue": "" if best["success"] else best["message"],
    }
    return row, edges, sector


def base_failed_fit_row(
    rd_mode: str,
    prior_table: str,
    score_mode: str,
    model: str,
    dynamic_k: int,
    issue: str,
    values: dict[str, Any],
) -> dict[str, Any]:
    return {
        "rd_prior_mode": rd_mode,
        "prior_table": prior_table,
        "score_mode": score_mode,
        "model": model,
        "success": False,
        "converged": False,
        "chi2_SN": "",
        "chi2_BAO": "",
        "chi2_CMB": "",
        "chi2_total": "",
        "AIC": "",
        "BIC": "",
        "n_data": "",
        "dynamic_k": dynamic_k,
        "edge_flag": "",
        "Omega_m0": values.get("Omega_m0", ""),
        "h": values.get("h", ""),
        "r_d": values.get("r_d", ""),
        "w": values.get("w", ""),
        "w0": values.get("w0", ""),
        "wa": values.get("wa", ""),
        "BAO_alpha": "",
        "SN_offset": "",
        "z_star": "",
        "r_s_star": "",
        "D_M_star": "",
        "optimizer": "failed",
        "issue": issue,
    }


def source_t7_primary() -> dict[str, float]:
    rows = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    primary = next(row for row in rows if row["branch"] == PRIMARY_LATE_BRANCH)
    return {
        "chi2_late": float(primary["chi2_total"]),
        "chi2_SN": float(primary["chi2_SN"]),
        "chi2_BAO": float(primary["chi2_BAO"]),
        "Omega_m0": float(primary["Omega_m"]),
        "B_mem": float(primary["B_mem"]),
    }


def cmb_only_lookup() -> dict[tuple[str, str], dict[str, float]]:
    rows = read_csv_rows(CMB_SCORE_RUN / "results" / "fit_summary.csv")
    out: dict[tuple[str, str], dict[str, float]] = {}
    for row in rows:
        if row["model"] == PRIMARY_MODEL:
            out[(row["prior_table"], row["score_mode"])] = {
                "chi2_CMB": float(row["chi2"]),
                "Omega_m0": float(row["Omega_m0"]),
                "h": float(row["h"]),
            }
    return out


def sector_breakdown_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in fit_rows:
        if row["success"] is not True:
            continue
        for sector in ["SN", "BAO", "CMB"]:
            rows.append(
                {
                    "rd_prior_mode": row["rd_prior_mode"],
                    "prior_table": row["prior_table"],
                    "score_mode": row["score_mode"],
                    "model": row["model"],
                    "sector": sector,
                    "chi2": row[f"chi2_{sector}"],
                }
            )
    return rows


def rd_plausibility_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    lower_warn, upper_warn = PHYSICAL_RD_WARNING
    for row in fit_rows:
        if row["success"] is not True:
            continue
        rd = float(row["r_d"])
        rows.append(
            {
                "rd_prior_mode": row["rd_prior_mode"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "model": row["model"],
                "r_d": rd,
                "physical_warning_lower": lower_warn,
                "physical_warning_upper": upper_warn,
                "physical_warning": rd < lower_warn or rd > upper_warn,
                "edge_flag": row["edge_flag"],
            }
        )
    return rows


def baseline_comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = {}
    for row in fit_rows:
        if row["success"] is True:
            grouped.setdefault((row["rd_prior_mode"], row["prior_table"], row["score_mode"]), {})[row["model"]] = row
    for (rd_mode, prior_table, score_mode), by_model in grouped.items():
        locked = by_model.get(PRIMARY_MODEL)
        if not locked:
            continue
        for reference in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            ref = by_model.get(reference)
            if not ref:
                continue
            rows.append(
                {
                    "rd_prior_mode": rd_mode,
                    "prior_table": prior_table,
                    "score_mode": score_mode,
                    "model": PRIMARY_MODEL,
                    "reference": reference,
                    "delta_chi2": float(locked["chi2_total"]) - float(ref["chi2_total"]),
                    "delta_AIC": float(locked["AIC"]) - float(ref["AIC"]),
                    "delta_BIC": float(locked["BIC"]) - float(ref["BIC"]),
                    "locked_edge_flag": locked["edge_flag"],
                    "reference_edge_flag": ref["edge_flag"],
                }
            )
    return rows


def control_reproduction_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    t7 = source_t7_primary()
    transfer_status = read_json(TRANSFER_RUN / "status.json")["status"]
    cmb_status = read_json(CMB_SCORE_RUN / "status.json")["status"]
    locked_rows = [row for row in fit_rows if row["model"] == PRIMARY_MODEL and row["success"] is True]
    return [
        {
            "control": "alpha_free_late_control",
            "status": "reference_available",
            "evidence": f"T7 primary chi2_late={t7['chi2_late']}",
            "interpretation": "source late branch available; joint runner intentionally replaces alpha with h-r_d",
        },
        {
            "control": "CMB_only_control",
            "status": "reference_available",
            "evidence": cmb_status,
            "interpretation": "checkpoint 116 CMB-only draw is the comparison anchor",
        },
        {
            "control": "late_to_CMB_transfer_control",
            "status": "reference_available",
            "evidence": transfer_status,
            "interpretation": "checkpoint 117 simple transfer fail is the comparison anchor",
        },
        {
            "control": "joint_h_rd_score",
            "status": "complete" if locked_rows else "missing",
            "evidence": f"locked_fit_rows={len(locked_rows)}",
            "interpretation": "main joint score generated",
        },
        {
            "control": "r_d_prior_sensitivity",
            "status": "complete"
            if {"broad", "physical"}.issubset({str(row["rd_prior_mode"]) for row in locked_rows})
            else "incomplete",
            "evidence": ";".join(sorted({str(row["rd_prior_mode"]) for row in locked_rows})),
            "interpretation": "broad and physical r_d prior modes required",
        },
    ]


def gate_label(delta_bic_lcdm: float, late_penalty: float, cmb_penalty: float, edge: bool) -> str:
    if edge:
        return "hard_loss_edge_dependent"
    if late_penalty > 6.0 or cmb_penalty > 6.0:
        return "hard_loss_sector_degradation"
    if delta_bic_lcdm <= -2.0 and late_penalty <= 2.0 and cmb_penalty <= 2.0:
        return "clean_win"
    if delta_bic_lcdm <= 0.0 and late_penalty <= 2.0 and cmb_penalty <= 2.0:
        return "points_win"
    if abs(delta_bic_lcdm) <= 2.0 and late_penalty <= 6.0 and cmb_penalty <= 6.0:
        return "competitive_draw"
    if delta_bic_lcdm <= 6.0 and late_penalty <= 6.0 and cmb_penalty <= 6.0:
        return "narrow_loss"
    return "hard_loss"


def joint_gate_rows(fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    t7 = source_t7_primary()
    cmb_lookup = cmb_only_lookup()
    lcdm_lookup = {
        (row["rd_prior_mode"], row["prior_table"], row["score_mode"]): row
        for row in comparisons
        if row["reference"] == "LCDM"
    }
    rows: list[dict[str, Any]] = []
    for row in fit_rows:
        if row["model"] != PRIMARY_MODEL or row["success"] is not True:
            continue
        key = (row["prior_table"], row["score_mode"])
        comparison_key = (row["rd_prior_mode"], row["prior_table"], row["score_mode"])
        cmb_anchor = cmb_lookup[key]
        lcdm = lcdm_lookup.get(comparison_key, {})
        late_penalty = float(row["chi2_SN"]) + float(row["chi2_BAO"]) - t7["chi2_late"]
        cmb_penalty = float(row["chi2_CMB"]) - cmb_anchor["chi2_CMB"]
        delta_bic = float(lcdm.get("delta_BIC", float("nan")))
        label = gate_label(delta_bic, late_penalty, cmb_penalty, bool(row["edge_flag"]))
        rows.append(
            {
                "rd_prior_mode": row["rd_prior_mode"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "model": row["model"],
                "gate": label,
                "late_chi2_penalty_vs_T7": late_penalty,
                "CMB_chi2_penalty_vs_CMB_only": cmb_penalty,
                "delta_BIC_vs_LCDM": delta_bic,
                "edge_flag": row["edge_flag"],
                "r_d": row["r_d"],
            }
        )
    return rows


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    available_rd_modes = {str(row["rd_prior_mode"]) for row in gates}
    decision_rd_modes = ["broad"] if "broad" in available_rd_modes else sorted(available_rd_modes)
    primary = [
        row
        for row in gates
        if row["rd_prior_mode"] in decision_rd_modes
        and row["prior_table"] in PRIMARY_PRIOR_TABLES
        and row["score_mode"] in SCORE_MODES
    ]
    hard = [row for row in primary if str(row["gate"]).startswith("hard_loss")]
    draws_or_better = [
        row for row in primary if row["gate"] in {"clean_win", "points_win", "competitive_draw"}
    ]
    if hard:
        status = "locked_2over27_joint_late_CMB_calibration_hard_loss"
    elif len(draws_or_better) == len(primary) and primary:
        status = "locked_2over27_joint_late_CMB_calibration_survives"
    else:
        status = "locked_2over27_joint_late_CMB_calibration_mixed_or_narrow"
    return [
        {
            "decision": "joint_status",
            "value": status,
            "rationale": "broad r_d primary gates determine first-pass status",
        },
        {
            "decision": "primary_gate_count",
            "value": len(primary),
            "rationale": f"{','.join(decision_rd_modes)} r_d across wCDM/LCDM tables and strict/marginal score modes",
        },
        {
            "decision": "primary_hard_loss_count",
            "value": len(hard),
            "rationale": "hard losses come from sector degradation, edge dependence, or BIC loss",
        },
        {
            "decision": "primary_draw_or_better_count",
            "value": len(draws_or_better),
            "rationale": "draws count as survival under the boxing scorecard",
        },
        {
            "decision": "theory_promotion_allowed",
            "value": False,
            "rationale": "compressed background-only joint stress; no parent derivation or perturbation CMB",
        },
        {
            "decision": "next_target",
            "value": "119-locked-2over27-joint-late-CMB-calibration-runner.md",
            "rationale": "write the exact score readout and decide whether to demote or repair the bridge",
        },
    ]


def run_dry_run(output_root: Path, rd_modes: list[str]) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-joint-late-CMB-dryrun"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    config, sn, bao = load_primary_data()
    sources = source_register_rows()
    data_rows = data_schema_rows(config, sn, bao)
    gates = [
        {
            "gate": "source_artifacts_exist",
            "status": "pass" if all(row["exists"] for row in sources) else "fail",
            "evidence": f"missing_count={sum(not row['exists'] for row in sources)}",
        },
        {
            "gate": "data_shapes_valid",
            "status": "pass",
            "evidence": f"SN={len(sn['z'])}; BAO={len(bao['rows'])}; CMB_modes={','.join(SCORE_MODES)}",
        },
        {
            "gate": "rd_modes_declared",
            "status": "pass" if set(rd_modes).issubset(RD_PRIOR_MODES) else "fail",
            "evidence": ";".join(rd_modes),
        },
        {
            "gate": "joint_score_allowed",
            "status": "pass",
            "evidence": "contract 118 declares h-r_d-SN_offset joint map",
        },
    ]
    write_common_registers(results_dir, sources, data_rows)
    write_csv(results_dir / "dryrun_gates.csv", gates, ["gate", "status", "evidence"])
    decisions = [
        {
            "decision": "dryrun_status",
            "value": "locked_2over27_joint_late_CMB_dryrun_pass"
            if all(row["status"] == "pass" for row in gates)
            else "locked_2over27_joint_late_CMB_dryrun_fail",
            "rationale": "source artifacts, data shapes, and contract are available",
        },
        {
            "decision": "score_ran",
            "value": False,
            "rationale": "dry-run only",
        },
    ]
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])
    status = {
        "status": decisions[0]["value"],
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": False,
        "rd_modes": rd_modes,
        "sn_rows": len(sn["z"]),
        "bao_rows": len(bao["rows"]),
        "models": MODEL_ORDER,
        "prior_tables": PRIMARY_PRIOR_TABLES,
        "score_modes": list(SCORE_MODES),
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def write_common_registers(
    results_dir: Path,
    sources: list[dict[str, Any]],
    data_rows: list[dict[str, Any]],
) -> None:
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_schema_report.csv",
        data_rows,
        ["dataset", "path", "rows", "covariance_mode", "observable", "status", "issue"],
    )
    write_csv(
        results_dir / "model_register.csv",
        model_register_rows(),
        ["model", "role", "free_parameters", "fixed_parameters", "dynamic_k"],
    )
    write_csv(results_dir / "parameter_map_register.csv", parameter_map_rows(), ["item", "rule", "status"])


def run_score(output_root: Path, rd_modes: list[str], max_iter: int) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-joint-late-CMB-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    config, sn, bao = load_primary_data()
    sources = source_register_rows()
    data_rows = data_schema_rows(config, sn, bao)
    write_common_registers(results_dir, sources, data_rows)

    fit_rows: list[dict[str, Any]] = []
    edge_table: list[dict[str, Any]] = []
    for rd_mode in rd_modes:
        for prior_table in PRIMARY_PRIOR_TABLES:
            for score_mode in SCORE_MODES:
                for model in MODEL_ORDER:
                    fit, edges, _ = fit_joint_model(
                        rd_mode,
                        prior_table,
                        score_mode,
                        model,
                        sn,
                        bao,
                        max_iter,
                    )
                    fit_rows.append(fit)
                    edge_table.extend(edges)

    sectors = sector_breakdown_rows(fit_rows)
    comparisons = baseline_comparison_rows(fit_rows)
    rd_table = rd_plausibility_rows(fit_rows)
    controls = control_reproduction_rows(fit_rows)
    gates = joint_gate_rows(fit_rows, comparisons)
    decisions = decision_rows(gates)

    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "success",
            "converged",
            "chi2_SN",
            "chi2_BAO",
            "chi2_CMB",
            "chi2_total",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "edge_flag",
            "Omega_m0",
            "h",
            "r_d",
            "w",
            "w0",
            "wa",
            "BAO_alpha",
            "SN_offset",
            "z_star",
            "r_s_star",
            "D_M_star",
            "optimizer",
            "issue",
        ],
    )
    write_csv(
        results_dir / "sector_chi2_breakdown.csv",
        sectors,
        ["rd_prior_mode", "prior_table", "score_mode", "model", "sector", "chi2"],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_table,
        [
            "rd_prior_mode",
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
        results_dir / "rd_plausibility_table.csv",
        rd_table,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "r_d",
            "physical_warning_lower",
            "physical_warning_upper",
            "physical_warning",
            "edge_flag",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "reference",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_edge_flag",
            "reference_edge_flag",
        ],
    )
    write_csv(
        results_dir / "control_reproduction.csv",
        controls,
        ["control", "status", "evidence", "interpretation"],
    )
    write_csv(
        results_dir / "joint_gates.csv",
        gates,
        [
            "rd_prior_mode",
            "prior_table",
            "score_mode",
            "model",
            "gate",
            "late_chi2_penalty_vs_T7",
            "CMB_chi2_penalty_vs_CMB_only",
            "delta_BIC_vs_LCDM",
            "edge_flag",
            "r_d",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value", "rationale"])

    status = {
        "status": next(row["value"] for row in decisions if row["decision"] == "joint_status"),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "score_ran": True,
        "claim_ceiling": "joint_compressed_background_calibration_stress_only",
        "rd_modes": rd_modes,
        "fit_rows": len(fit_rows),
        "models": MODEL_ORDER,
        "prior_tables": PRIMARY_PRIOR_TABLES,
        "score_modes": list(SCORE_MODES),
        "locked_constants": {
            "DeltaR": LOCKED_DELTA_R,
            "B_mem": LOCKED_B_MEM,
            "p": LOCKED_P,
            "u3": LOCKED_U3,
        },
        "next_target": "119-locked-2over27-joint-late-CMB-calibration-runner.md",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def parse_rd_modes(value: str) -> list[str]:
    if value == "both":
        return ["broad", "physical"]
    modes = [part.strip() for part in value.split(",") if part.strip()]
    bad = [mode for mode in modes if mode not in RD_PRIOR_MODES]
    if bad:
        raise argparse.ArgumentTypeError(f"unknown r_d prior mode(s): {','.join(bad)}")
    return modes


def main() -> None:
    parser = argparse.ArgumentParser(description="Joint late+CMB calibration runner for locked 2/27.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--score", action="store_true")
    parser.add_argument("--rd-prior-mode", type=parse_rd_modes, default=["broad"], help="broad, physical, or both")
    parser.add_argument("--max-iter", type=int, default=120)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    args = parser.parse_args()
    if args.dry_run:
        run_dry_run(args.output_root, args.rd_prior_mode)
    else:
        run_score(args.output_root, args.rd_prior_mode, args.max_iter)


if __name__ == "__main__":
    main()
