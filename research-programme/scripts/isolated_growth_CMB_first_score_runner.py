#!/usr/bin/env python3
"""Run the isolated post-checkpoint first growth/CMB score."""

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
sys.path.insert(0, str(MAIN_SCRIPTS))

from growth_CMB_first_scoring_run import (  # noqa: E402
    SOURCE_161_CONFIG,
    add_deltas,
    branch_chi2,
    chi2,
    cmb_data,
    cmb_prediction,
    fit_sigma8,
    load_background_params,
    load_json,
    write_csv,
)


SOURCE_26_STATUS = Path("runs/20260531-000031-isolated-likelihood-preflight-wrapper/status.json")
SOURCE_27_STATUS = Path("runs/20260531-000551-strict-cosmology-numeric-lock/status.json")
FORBIDDEN_BEFORE_SCORE = {"model_scores.csv", "growth_predictions.csv", "CMB_distance_scores.csv", "comparative_verdict.csv"}


def forbidden_artifacts(root: Path) -> list[str]:
    if not root.exists():
        return []
    return [str(path) for path in root.rglob("*") if path.is_file() and path.name in FORBIDDEN_BEFORE_SCORE]


def pre_run_gate_rows(source_26: dict[str, Any], source_27: dict[str, Any], forbidden_before: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_26_isolated_preflight_passed",
            "status": "pass" if source_26.get("readout") == "isolated_likelihood_preflight_locked_no_score_scoring_still_blocked" else "fail",
            "detail": str(source_26.get("readout")),
        },
        {
            "gate": "source_27_numeric_lock_passed",
            "status": "pass" if source_27.get("readout") == "strict_cosmology_numeric_lock_ready_for_scoring_manifest_no_score" else "fail",
            "detail": str(source_27.get("readout")),
        },
        {
            "gate": "forbidden_score_artifacts_absent_before_run",
            "status": "pass" if not forbidden_before else "fail",
            "detail": "; ".join(forbidden_before) if forbidden_before else "none",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "internal scoring only",
        },
    ]


def readout_from_scores(score_rows: list[dict[str, Any]]) -> str:
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0_row = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    if best_aic["model"] == "MTS_C0_minimal_smooth_memory" and best_bic["model"] == "MTS_C0_minimal_smooth_memory":
        return "isolated_C0_preferred_internal_first_score_needs_robustness"
    if c0_row["delta_aic_vs_best_baseline"] < 0.0:
        return "isolated_C0_AIC_improves_but_BIC_or_chi2_needs_caution"
    return "isolated_C0_not_preferred_first_growth_CMB_score"


def verdict_rows(score_rows: list[dict[str, Any]], readout: str) -> list[dict[str, Any]]:
    best_chi2 = min(score_rows, key=lambda row: row["chi2_total"])
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0_row = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    return [
        {
            "verdict_label": readout,
            "best_chi2_model": best_chi2["model"],
            "best_aic_model": best_aic["model"],
            "best_bic_model": best_bic["model"],
            "C0_delta_chi2_vs_best_baseline": c0_row["delta_chi2_vs_best_baseline"],
            "C0_delta_aic_vs_best_baseline": c0_row["delta_aic_vs_best_baseline"],
            "C0_delta_bic_vs_best_baseline": c0_row["delta_bic_vs_best_baseline"],
            "public_claim_allowed": False,
            "claim_limit": "internal_L2_fit_diagnostic_only",
            "next_recommendation": "robustness_and_CMB_approximation_audit_before_interpretation",
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Isolated post-checkpoint first growth/CMB score.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_26 = load_json(POST_CHECKPOINT / SOURCE_26_STATUS)
    source_27 = load_json(POST_CHECKPOINT / SOURCE_27_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-isolated-growth-CMB-first-score-runner"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    forbidden_before = forbidden_artifacts(out_dir)
    gates = pre_run_gate_rows(source_26, source_27, forbidden_before)
    if any(row["status"] == "fail" and row["gate"] != "public_claim_allowed" for row in gates):
        write_csv(results_dir / "score_pre_run_gates.csv", gates, list(gates[0].keys()))
        raise SystemExit("pre-run gates failed")

    config = load_json(MAIN_WORKBENCH / SOURCE_161_CONFIG)
    background = load_background_params(MAIN_WORKBENCH)
    cmb_params, cmb_obs, cmb_cov = cmb_data(MAIN_WORKBENCH)

    predictions: list[dict[str, Any]] = []
    cmb_rows: list[dict[str, Any]] = []
    robustness_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    data_count = 14 + 4

    for model in config["models"]:
        entry = background[model]
        physics_model = entry["physics_model"]
        params = {key: float(value) for key, value in entry["params"].items()}
        sigma8_0, primary_chi2 = fit_sigma8(physics_model, params, config["primary_growth_files"])
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

        cmb_pred_map = cmb_prediction(physics_model, params)
        cmb_pred = np.asarray([cmb_pred_map[name] for name in cmb_params], dtype=float)
        cmb_residual = cmb_obs - cmb_pred
        cmb_chi2_value = chi2(cmb_residual, cmb_cov)
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
        total_chi2 = primary_chi2 + cmb_chi2_value
        score_rows.append(
            {
                "model": model,
                "physics_model": physics_model,
                "background_source_model": entry["source_row_model"],
                "chi2_growth_primary": primary_chi2,
                "chi2_CMB_distance": cmb_chi2_value,
                "chi2_total": total_chi2,
                "n_data": data_count,
                "n_params": parameter_count,
                "aic": total_chi2 + 2.0 * parameter_count,
                "bic": total_chi2 + parameter_count * math.log(data_count),
                "sigma8_0_fit_primary": sigma8_0,
                "background_params_json": json.dumps(params, sort_keys=True),
                "stability_flags": "post_checkpoint_isolated;CMB_distance_prior_approximation;no_growth_CMB_refit",
            }
        )

    add_deltas(score_rows)
    readout = readout_from_scores(score_rows)
    verdict = verdict_rows(score_rows, readout)

    write_csv(results_dir / "score_pre_run_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "model_scores.csv", score_rows, list(score_rows[0].keys()))
    write_csv(results_dir / "growth_predictions.csv", predictions, list(predictions[0].keys()))
    write_csv(results_dir / "CMB_distance_scores.csv", cmb_rows, list(cmb_rows[0].keys()))
    write_csv(results_dir / "robustness_diagnostics.csv", robustness_rows, list(robustness_rows[0].keys()))
    write_csv(results_dir / "comparative_verdict.csv", verdict, list(verdict[0].keys()))

    best_chi2 = min(score_rows, key=lambda row: row["chi2_total"])
    best_aic = min(score_rows, key=lambda row: row["aic"])
    best_bic = min(score_rows, key=lambda row: row["bic"])
    c0_row = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    status = {
        "status": "complete_isolated_growth_CMB_first_score_runner",
        "readout": readout,
        "recommendation": "robustness_and_CMB_approximation_audit_before_interpretation",
        "next_target": "29-growth-CMB-score-readout-and-robustness-gate.md",
        "data_fit_performed": True,
        "fit_allowed_now": False,
        "public_claim_allowed": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "internal_L2_fit_diagnostic_only",
        "best_chi2_model": best_chi2["model"],
        "best_aic_model": best_aic["model"],
        "best_bic_model": best_bic["model"],
        "C0_delta_chi2_vs_best_baseline": c0_row["delta_chi2_vs_best_baseline"],
        "C0_delta_aic_vs_best_baseline": c0_row["delta_aic_vs_best_baseline"],
        "C0_delta_bic_vs_best_baseline": c0_row["delta_bic_vs_best_baseline"],
        "outputs": {
            "score_pre_run_gates": str(results_dir / "score_pre_run_gates.csv"),
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
