#!/usr/bin/env python3
"""Run repaired post-checkpoint growth/CMB score with scale-factor CMB integral."""

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


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
POST_SCRIPTS = POST_CHECKPOINT / "scripts"
sys.path.insert(0, str(POST_SCRIPTS))
sys.path.insert(0, str(MAIN_SCRIPTS))

from growth_CMB_first_scoring_run import (  # noqa: E402
    SOURCE_161_CONFIG,
    add_deltas,
    branch_chi2,
    chi2,
    cmb_data,
    fit_sigma8,
    load_background_params,
    load_json,
    write_csv,
)
from post_checkpoint_CMB_distance_prior_implementation_audit import cmb_prediction_variant  # noqa: E402


SOURCE_30_STATUS = Path("runs/20260531-001848-CMB-distance-prior-implementation-audit/status.json")


def verdict_rows(score_rows: list[dict[str, Any]], readout: str) -> list[dict[str, Any]]:
    best_chi2 = min(score_rows, key=lambda row: row["chi2_total"])
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    return [
        {
            "verdict_label": readout,
            "best_chi2_model": best_chi2["model"],
            "best_aic_model": best_aic["model"],
            "best_bic_model": best_bic["model"],
            "C0_delta_chi2_vs_best_baseline": c0["delta_chi2_vs_best_baseline"],
            "C0_delta_aic_vs_best_baseline": c0["delta_aic_vs_best_baseline"],
            "C0_delta_bic_vs_best_baseline": c0["delta_bic_vs_best_baseline"],
            "public_claim_allowed": False,
            "C0_support_claim_allowed": False,
            "C0_death_claim_allowed": False,
            "next_recommendation": "growth_only_readout_plus_CMB_calibration_freedom_audit",
        }
    ]


def readout_from_scores(score_rows: list[dict[str, Any]]) -> str:
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    if best_aic["model"] == "MTS_C0_minimal_smooth_memory" and best_bic["model"] == "MTS_C0_minimal_smooth_memory":
        return "C0_preferred_repaired_CMB_distance_score_needs_external_validation"
    if c0["delta_aic_vs_best_baseline"] < 0.0:
        return "C0_AIC_improves_repaired_CMB_but_BIC_or_chi2_needs_caution"
    return "C0_not_preferred_repaired_CMB_distance_score"


def main() -> int:
    parser = argparse.ArgumentParser(description="Repaired post-checkpoint growth/CMB score.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_30 = load_json(POST_CHECKPOINT / SOURCE_30_STATUS)
    if source_30.get("readout") != "CMB_distance_prior_implementation_error_found_repair_required":
        raise SystemExit("CMB audit has not selected repaired scoring")

    config = load_json(MAIN_WORKBENCH / SOURCE_161_CONFIG)
    background = load_background_params(MAIN_WORKBENCH)
    cmb_params, cmb_obs, cmb_cov = cmb_data(MAIN_WORKBENCH)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-repaired-growth-CMB-score"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    predictions: list[dict[str, Any]] = []
    cmb_rows: list[dict[str, Any]] = []
    robustness_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    data_count = 18

    for model in config["models"]:
        entry = background[model]
        physics_model = entry["physics_model"]
        params = {key: float(value) for key, value in entry["params"].items()}
        sigma8_0, _ = fit_sigma8(physics_model, params, config["primary_growth_files"])

        primary_predictions: list[dict[str, Any]] = []
        primary_chi2 = branch_chi2(
            physics_model,
            params,
            config["primary_growth_files"],
            sigma8_0,
            primary_predictions,
            "primary_BAO_plus",
            model,
        )
        predictions.extend(primary_predictions)

        robustness_predictions: list[dict[str, Any]] = []
        robustness_chi2 = branch_chi2(
            physics_model,
            params,
            config["robustness_growth_files"],
            sigma8_0,
            robustness_predictions,
            "robustness_full_shape_only",
            model,
        )
        predictions.extend(robustness_predictions)
        robustness_rows.append(
            {
                "model": model,
                "chi2_growth_full_shape_only": robustness_chi2,
                "sigma8_0_from_primary": sigma8_0,
            }
        )

        cmb_pred_map = cmb_prediction_variant(physics_model, params, "scale_factor_quad", np.inf, True, True)
        cmb_pred = np.asarray([cmb_pred_map[name] for name in cmb_params], dtype=float)
        cmb_residual = cmb_obs - cmb_pred
        cmb_chi2 = chi2(cmb_residual, cmb_cov)
        for parameter, observed, predicted, residual in zip(cmb_params, cmb_obs, cmb_pred, cmb_residual):
            cmb_rows.append(
                {
                    "model": model,
                    "parameter": parameter,
                    "observed": observed,
                    "predicted": float(predicted),
                    "residual": float(residual),
                }
            )

        parameter_count = int(entry["background_n_params"]) + 1
        total = primary_chi2 + cmb_chi2
        score_rows.append(
            {
                "model": model,
                "physics_model": physics_model,
                "background_source_model": entry["source_row_model"],
                "chi2_growth_primary": primary_chi2,
                "chi2_CMB_distance_repaired": cmb_chi2,
                "chi2_total": total,
                "n_data": data_count,
                "n_params": parameter_count,
                "aic": total + 2.0 * parameter_count,
                "bic": total + parameter_count * math.log(data_count),
                "sigma8_0_fit_primary": sigma8_0,
                "background_params_json": json.dumps(params, sort_keys=True),
                "stability_flags": "post_checkpoint_repaired_CMB_scale_factor_quad;no_growth_CMB_refit;distance_prior_lightweight",
            }
        )

    add_deltas(score_rows)
    readout = readout_from_scores(score_rows)
    verdict = verdict_rows(score_rows, readout)

    write_csv(results_dir / "model_scores.csv", score_rows, list(score_rows[0].keys()))
    write_csv(results_dir / "growth_predictions.csv", predictions, list(predictions[0].keys()))
    write_csv(results_dir / "CMB_distance_scores.csv", cmb_rows, list(cmb_rows[0].keys()))
    write_csv(results_dir / "robustness_diagnostics.csv", robustness_rows, list(robustness_rows[0].keys()))
    write_csv(results_dir / "comparative_verdict.csv", verdict, list(verdict[0].keys()))

    best_chi2 = min(score_rows, key=lambda row: row["chi2_total"])
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    status = {
        "status": "complete_repaired_growth_CMB_score",
        "readout": readout,
        "recommendation": "growth_only_readout_plus_CMB_calibration_freedom_audit",
        "next_target": "32-repaired-score-readout-and-decision.md",
        "data_fit_performed": True,
        "public_claim_allowed": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "best_chi2_model": best_chi2["model"],
        "best_aic_model": best_aic["model"],
        "best_bic_model": best_bic["model"],
        "C0_delta_chi2_vs_best_baseline": c0["delta_chi2_vs_best_baseline"],
        "C0_delta_aic_vs_best_baseline": c0["delta_aic_vs_best_baseline"],
        "C0_delta_bic_vs_best_baseline": c0["delta_bic_vs_best_baseline"],
        "outputs": {
            "model_scores": str(results_dir / "model_scores.csv"),
            "growth_predictions": str(results_dir / "growth_predictions.csv"),
            "CMB_distance_scores": str(results_dir / "CMB_distance_scores.csv"),
            "robustness_diagnostics": str(results_dir / "robustness_diagnostics.csv"),
            "comparative_verdict": str(results_dir / "comparative_verdict.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
