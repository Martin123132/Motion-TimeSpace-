#!/usr/bin/env python3
"""Stress the CMB-calibrated C0 rows against the same growth pipeline."""

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
    branch_chi2,
    cmb_data,
    fit_sigma8,
    load_background_params,
    load_json,
    write_csv,
)
from post_checkpoint_CMB_distance_prior_implementation_audit import (  # noqa: E402
    cmb_prediction_variant,
    score_prediction,
)


SOURCE_33_RESULTS = Path("runs/20260531-003140-CMB-calibration-freedom-audit/results")
SOURCE_36_STATUS = Path("runs/20260531-004705-parent-CMB-calibration-map-attempt/status.json")
LOCKED_BRANCH = "MTS_C0_minimal_smooth_memory"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def c0_calibrated_specs() -> list[dict[str, Any]]:
    rows = read_csv(POST_CHECKPOINT / SOURCE_33_RESULTS / "CMB_calibration_freedom_audit.csv")
    specs: list[dict[str, Any]] = []
    for row in rows:
        if row["branch"] in {"C0_equal_h0_omega_shape_frozen", "C0_native_bmem_CMB_calibrated_shape_frozen"}:
            specs.append(
                {
                    "model": row["branch"],
                    "physics_model": "M6",
                    "params": json.loads(row["params_json"]),
                    "parameter_origin": "CMB_calibrated_closure",
                    "model_selection_valid": False,
                    "fit_names": row["fit_names"],
                }
            )
    return specs


def fixed_specs() -> list[dict[str, Any]]:
    background = load_background_params(MAIN_WORKBENCH)
    specs: list[dict[str, Any]] = []
    for model in ["LCDM", "wCDM", "CPL", LOCKED_BRANCH]:
        entry = background[model]
        specs.append(
            {
                "model": f"{model}_fixed_no_SH0ES",
                "physics_model": entry["physics_model"],
                "params": {key: float(value) for key, value in entry["params"].items()},
                "parameter_origin": "no_SH0ES_background_locked",
                "model_selection_valid": True,
                "fit_names": "background_fit_row",
            }
        )
    return specs


def add_deltas(rows: list[dict[str, Any]]) -> None:
    fixed_baselines = [
        row for row in rows
        if row["parameter_origin"] == "no_SH0ES_background_locked" and row["model"].startswith(("LCDM", "wCDM", "CPL"))
    ]
    best_growth = min(fixed_baselines, key=lambda row: float(row["chi2_growth_primary"]))
    best_cmb = min(fixed_baselines, key=lambda row: float(row["chi2_CMB_repaired"]))
    best_total = min(fixed_baselines, key=lambda row: float(row["chi2_primary_growth_plus_CMB"]))
    for row in rows:
        row["delta_growth_primary_vs_best_fixed_baseline"] = float(row["chi2_growth_primary"]) - float(best_growth["chi2_growth_primary"])
        row["delta_CMB_vs_best_fixed_baseline"] = float(row["chi2_CMB_repaired"]) - float(best_cmb["chi2_CMB_repaired"])
        row["delta_total_vs_best_fixed_baseline"] = float(row["chi2_primary_growth_plus_CMB"]) - float(best_total["chi2_primary_growth_plus_CMB"])
        row["best_fixed_growth_baseline"] = best_growth["model"]
        row["best_fixed_CMB_baseline"] = best_cmb["model"]
        row["best_fixed_total_baseline"] = best_total["model"]


def score_rows(config: dict[str, Any], cmb_params: list[str], cmb_obs: np.ndarray, cmb_cov: np.ndarray) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scores: list[dict[str, Any]] = []
    predictions: list[dict[str, Any]] = []
    for spec in fixed_specs() + c0_calibrated_specs():
        physics_model = str(spec["physics_model"])
        params = {key: float(value) for key, value in spec["params"].items()}
        sigma8_0, _ = fit_sigma8(physics_model, params, config["primary_growth_files"])

        primary_predictions: list[dict[str, Any]] = []
        primary_chi2 = branch_chi2(
            physics_model,
            params,
            config["primary_growth_files"],
            sigma8_0,
            primary_predictions,
            "primary_BAO_plus",
            str(spec["model"]),
        )
        predictions.extend(primary_predictions)

        full_shape_predictions: list[dict[str, Any]] = []
        full_shape_chi2 = branch_chi2(
            physics_model,
            params,
            config["robustness_growth_files"],
            sigma8_0,
            full_shape_predictions,
            "robustness_full_shape_only",
            str(spec["model"]),
        )
        predictions.extend(full_shape_predictions)

        cmb_pred_map = cmb_prediction_variant(physics_model, params, "scale_factor_quad", np.inf, True, True)
        cmb_chi2, cmb_without_l_a, l_a_pull = score_prediction(cmb_pred_map, cmb_params, cmb_obs, cmb_cov)
        scores.append(
            {
                "model": spec["model"],
                "physics_model": physics_model,
                "parameter_origin": spec["parameter_origin"],
                "fit_names": spec["fit_names"],
                "model_selection_valid": spec["model_selection_valid"],
                "chi2_growth_primary": primary_chi2,
                "chi2_growth_full_shape_only": full_shape_chi2,
                "chi2_CMB_repaired": cmb_chi2,
                "chi2_CMB_without_l_A": cmb_without_l_a,
                "l_A_pull_sigma": l_a_pull,
                "chi2_primary_growth_plus_CMB": primary_chi2 + cmb_chi2,
                "sigma8_0_fit_primary": sigma8_0,
                "params_json": json.dumps(params, sort_keys=True),
                "claim_limit": "closure_stress_only" if not spec["model_selection_valid"] else "fixed_baseline_reference",
            }
        )
    add_deltas(scores)
    return scores, predictions


def gate_rows(source_36: dict[str, Any], scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    native = next(row for row in scores if row["model"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    locked = next(row for row in scores if row["model"] == f"{LOCKED_BRANCH}_fixed_no_SH0ES")
    native_growth_delta_vs_locked = float(native["chi2_growth_primary"]) - float(locked["chi2_growth_primary"])
    native_full_shape_delta_vs_locked = float(native["chi2_growth_full_shape_only"]) - float(locked["chi2_growth_full_shape_only"])
    return [
        {
            "gate": "source_36_complete",
            "status": "pass" if source_36.get("readout") == "parent_CMB_calibration_map_not_derived_bmem_corridor_only" else "fail",
            "detail": str(source_36.get("readout")),
        },
        {
            "gate": "native_CMB_calibrated_growth_not_worse_than_locked_by_2",
            "status": "pass" if native_growth_delta_vs_locked <= 2.0 else "fail",
            "detail": f"primary_growth_delta_vs_locked={native_growth_delta_vs_locked}",
        },
        {
            "gate": "native_CMB_calibrated_full_shape_not_worse_than_locked_by_2",
            "status": "pass" if native_full_shape_delta_vs_locked <= 2.0 else "fail",
            "detail": f"full_shape_delta_vs_locked={native_full_shape_delta_vs_locked}",
        },
        {
            "gate": "native_CMB_distance_near_exact",
            "status": "pass" if float(native["chi2_CMB_repaired"]) < 1.0e-4 else "fail",
            "detail": f"chi2_CMB={native['chi2_CMB_repaired']}",
        },
        {
            "gate": "joint_model_selection_allowed",
            "status": "fail",
            "detail": "C0 calibrated rows were trained on CMB distance priors; this is not an independent model-selection score",
        },
        {
            "gate": "CMB_calibrated_support_claim_allowed",
            "status": "fail",
            "detail": "parent calibration map is missing",
        },
    ]


def decision_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    native = next(row for row in scores if row["model"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    locked = next(row for row in scores if row["model"] == f"{LOCKED_BRANCH}_fixed_no_SH0ES")
    growth_delta = float(native["chi2_growth_primary"]) - float(locked["chi2_growth_primary"])
    status = "retained_closure_diagnostic" if growth_delta <= 2.0 else "demote_calibrated_row_growth_tension"
    return [
        {
            "decision": "native_CMB_calibrated_row_status",
            "status": status,
            "evidence": f"primary_growth_delta_vs_locked={growth_delta}; CMB_chi2={native['chi2_CMB_repaired']}",
            "next_action": "if retained, predeclare a no-refit calibrated holdout; if demoted, return to parent map only",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "CMB row is calibrated and parent map is not derived",
            "next_action": "derive parent map or independent predeclaration before evidence language",
        },
        {
            "decision": "next_target",
            "status": "predeclare_closure_holdout_or_parent_map_repair",
            "evidence": "same-parameter stress tells whether the CMB-calibrated closure is worth preserving",
            "next_action": "write 38-calibrated-closure-holdout-contract.md if retained",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="CMB-calibrated C0 joint growth stress.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_36 = load_json(POST_CHECKPOINT / SOURCE_36_STATUS)
    config = load_json(MAIN_WORKBENCH / SOURCE_161_CONFIG)
    cmb_params, cmb_obs, cmb_cov = cmb_data(MAIN_WORKBENCH)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-CMB-calibrated-joint-growth-stress"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    scores, predictions = score_rows(config, cmb_params, cmb_obs, cmb_cov)
    gates = gate_rows(source_36, scores)
    decisions = decision_rows(scores)
    native = next(row for row in scores if row["model"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    locked = next(row for row in scores if row["model"] == f"{LOCKED_BRANCH}_fixed_no_SH0ES")

    write_csv(results_dir / "joint_growth_CMB_same_parameter_scores.csv", scores, list(scores[0].keys()))
    write_csv(results_dir / "growth_predictions.csv", predictions, list(predictions[0].keys()))
    write_csv(results_dir / "calibrated_joint_growth_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    growth_delta = float(native["chi2_growth_primary"]) - float(locked["chi2_growth_primary"])
    readout = (
        "CMB_calibrated_closure_retained_growth_near_locked_not_evidence"
        if growth_delta <= 2.0
        else "CMB_calibrated_closure_demoted_growth_tension"
    )
    status = {
        "status": "complete_CMB_calibrated_joint_growth_stress",
        "readout": readout,
        "recommendation": "predeclare_calibrated_closure_holdout_or_repair_parent_map_next",
        "next_target": "38-calibrated-closure-holdout-contract.md",
        "native_CMB_calibrated_growth_delta_vs_locked": growth_delta,
        "native_CMB_calibrated_CMB_chi2": native["chi2_CMB_repaired"],
        "native_CMB_calibrated_total_delta_vs_best_fixed_baseline": native["delta_total_vs_best_fixed_baseline"],
        "model_selection_valid": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "joint_growth_CMB_same_parameter_scores": str(results_dir / "joint_growth_CMB_same_parameter_scores.csv"),
            "growth_predictions": str(results_dir / "growth_predictions.csv"),
            "calibrated_joint_growth_gate_criteria": str(results_dir / "calibrated_joint_growth_gate_criteria.csv"),
            "decision": str(results_dir / "decision.csv"),
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
