#!/usr/bin/env python3
"""Audit equal CMB calibration freedom after the repaired score."""

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
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
POST_SCRIPTS = POST_CHECKPOINT / "scripts"
sys.path.insert(0, str(POST_SCRIPTS))
sys.path.insert(0, str(MAIN_SCRIPTS))

from growth_CMB_first_scoring_run import cmb_data, load_background_params  # noqa: E402
from post_checkpoint_CMB_distance_prior_implementation_audit import (  # noqa: E402
    cmb_prediction_variant,
    score_prediction,
)


SOURCE_32_STATUS = Path("runs/20260531-002511-repaired-score-readout-and-decision/status.json")
SOURCE_31_RESULTS = Path("runs/20260531-002219-repaired-growth-CMB-score/results")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fit_cmb_branch(
    tier: str,
    branch: str,
    physics_model: str,
    base_params: dict[str, float],
    fit_names: list[str],
    bounds: list[tuple[float, float]],
    params_order: list[str],
    obs: np.ndarray,
    cov: np.ndarray,
    support_allowed: bool,
) -> dict[str, Any]:
    def objective(vector: np.ndarray) -> float:
        params = dict(base_params)
        params.update({name: float(value) for name, value in zip(fit_names, vector)})
        try:
            prediction = cmb_prediction_variant(physics_model, params, "scale_factor_quad", np.inf, True, True)
            value, _, _ = score_prediction(prediction, params_order, obs, cov)
            if not math.isfinite(value):
                return 1.0e30
            return value
        except Exception:
            return 1.0e30

    starts: list[np.ndarray] = []
    starts.append(np.asarray([0.5 * (lo + hi) for lo, hi in bounds], dtype=float))
    starts.append(
        np.asarray(
            [min(max(float(base_params.get(name, 0.5 * (lo + hi))), lo), hi) for name, (lo, hi) in zip(fit_names, bounds)],
            dtype=float,
        )
    )
    for fraction in (0.15, 0.3, 0.7, 0.85):
        starts.append(np.asarray([lo + fraction * (hi - lo) for lo, hi in bounds], dtype=float))

    best = None
    for start in starts:
        result = optimize.minimize(objective, start, method="L-BFGS-B", bounds=bounds, options={"maxiter": 500})
        if best is None or result.fun < best.fun:
            best = result
    assert best is not None

    params = dict(base_params)
    params.update({name: float(value) for name, value in zip(fit_names, best.x)})
    prediction = cmb_prediction_variant(physics_model, params, "scale_factor_quad", np.inf, True, True)
    chi2, chi2_without_l_a, l_a_pull = score_prediction(prediction, params_order, obs, cov)
    parameter_count = len(fit_names)
    data_count = len(params_order)
    edge_flags = [
        name
        for name, value, (lo, hi) in zip(fit_names, best.x, bounds)
        if abs(float(value) - lo) <= 0.01 * (hi - lo) or abs(float(value) - hi) <= 0.01 * (hi - lo)
    ]
    return {
        "tier": tier,
        "branch": branch,
        "physics_model": physics_model,
        "fit_names": ";".join(fit_names),
        "chi2_CMB": chi2,
        "chi2_without_l_A": chi2_without_l_a,
        "l_A_pull_sigma": l_a_pull,
        "n_data": data_count,
        "n_fit_params": parameter_count,
        "aic": chi2 + 2.0 * parameter_count,
        "bic": chi2 + parameter_count * math.log(data_count),
        "edge_flags": ";".join(edge_flags),
        "success": bool(best.success),
        "support_allowed": support_allowed,
        "message": str(best.message),
        "params_json": json.dumps(params, sort_keys=True),
    }


def calibration_specs() -> list[dict[str, Any]]:
    return [
        {
            "tier": "equal_two_parameter_calibration",
            "branch": "LCDM_equal_h0_omega",
            "background_key": "LCDM",
            "physics_model": "M0",
            "fit_names": ["omega_m0", "h0"],
            "bounds": [(0.15, 0.45), (55.0, 80.0)],
            "support_allowed": False,
        },
        {
            "tier": "equal_two_parameter_calibration",
            "branch": "wCDM_equal_h0_omega",
            "background_key": "wCDM",
            "physics_model": "M2_wCDM",
            "fit_names": ["omega_m0", "h0"],
            "bounds": [(0.15, 0.45), (55.0, 80.0)],
            "support_allowed": False,
        },
        {
            "tier": "equal_two_parameter_calibration",
            "branch": "CPL_equal_h0_omega",
            "background_key": "CPL",
            "physics_model": "M2_CPL",
            "fit_names": ["omega_m0", "h0"],
            "bounds": [(0.15, 0.45), (55.0, 80.0)],
            "support_allowed": False,
        },
        {
            "tier": "equal_two_parameter_calibration",
            "branch": "C0_equal_h0_omega_shape_frozen",
            "background_key": "MTS_C0_minimal_smooth_memory",
            "physics_model": "M6",
            "fit_names": ["omega_m0", "h0"],
            "bounds": [(0.15, 0.45), (55.0, 80.0)],
            "support_allowed": False,
        },
        {
            "tier": "native_background_calibration",
            "branch": "LCDM_native_CMB_calibrated",
            "background_key": "LCDM",
            "physics_model": "M0",
            "fit_names": ["omega_m0", "h0"],
            "bounds": [(0.15, 0.45), (55.0, 80.0)],
            "support_allowed": False,
        },
        {
            "tier": "native_background_calibration",
            "branch": "wCDM_native_CMB_calibrated",
            "background_key": "wCDM",
            "physics_model": "M2_wCDM",
            "fit_names": ["omega_m0", "h0", "w"],
            "bounds": [(0.15, 0.45), (55.0, 80.0), (-1.5, -0.3)],
            "support_allowed": False,
        },
        {
            "tier": "native_background_calibration",
            "branch": "CPL_native_CMB_calibrated",
            "background_key": "CPL",
            "physics_model": "M2_CPL",
            "fit_names": ["omega_m0", "h0", "w0", "wa"],
            "bounds": [(0.15, 0.45), (55.0, 80.0), (-1.5, -0.3), (-2.0, 2.0)],
            "support_allowed": False,
        },
        {
            "tier": "native_background_calibration",
            "branch": "C0_native_bmem_CMB_calibrated_shape_frozen",
            "background_key": "MTS_C0_minimal_smooth_memory",
            "physics_model": "M6",
            "fit_names": ["omega_m0", "h0", "b_mem"],
            "bounds": [(0.15, 0.45), (55.0, 80.0), (-0.5, 0.5)],
            "support_allowed": False,
        },
        {
            "tier": "diagnostic_shape_free",
            "branch": "C0_shape_free_CMB_calibrated",
            "background_key": "MTS_C0_minimal_smooth_memory",
            "physics_model": "M6",
            "fit_names": ["omega_m0", "h0", "b_mem", "alpha_act", "nu_act"],
            "bounds": [(0.15, 0.45), (55.0, 80.0), (-0.5, 0.5), (0.1, 2.5), (0.4, 3.0)],
            "support_allowed": False,
        },
    ]


def add_tier_deltas(rows: list[dict[str, Any]]) -> None:
    native_baselines = [
        row
        for row in rows
        if row["tier"] == "native_background_calibration" and not row["branch"].startswith("C0")
    ]
    native_best_chi2 = min(native_baselines, key=lambda row: float(row["chi2_CMB"])) if native_baselines else None
    native_best_aic = min(native_baselines, key=lambda row: float(row["aic"])) if native_baselines else None
    native_best_bic = min(native_baselines, key=lambda row: float(row["bic"])) if native_baselines else None
    for tier in sorted({row["tier"] for row in rows}):
        tier_rows = [row for row in rows if row["tier"] == tier]
        baseline_rows = [row for row in tier_rows if not row["branch"].startswith("C0")]
        if not baseline_rows and native_best_aic is not None:
            for row in tier_rows:
                row["best_baseline_by_aic"] = native_best_aic["branch"]
                row["delta_chi2_vs_best_baseline"] = float(row["chi2_CMB"]) - float(native_best_chi2["chi2_CMB"])
                row["delta_aic_vs_best_baseline"] = float(row["aic"]) - float(native_best_aic["aic"])
                row["delta_bic_vs_best_baseline"] = float(row["bic"]) - float(native_best_bic["bic"])
            continue
        if not baseline_rows:
            continue
        best_baseline_chi2 = min(baseline_rows, key=lambda row: float(row["chi2_CMB"]))
        best_baseline_aic = min(baseline_rows, key=lambda row: float(row["aic"]))
        best_baseline_bic = min(baseline_rows, key=lambda row: float(row["bic"]))
        for row in tier_rows:
            row["best_baseline_by_aic"] = best_baseline_aic["branch"]
            row["delta_chi2_vs_best_baseline"] = float(row["chi2_CMB"]) - float(best_baseline_chi2["chi2_CMB"])
            row["delta_aic_vs_best_baseline"] = float(row["aic"]) - float(best_baseline_aic["aic"])
            row["delta_bic_vs_best_baseline"] = float(row["bic"]) - float(best_baseline_bic["bic"])


def missing_piece_rows(calibration_rows: list[dict[str, Any]], fixed_c0_chi2: float) -> list[dict[str, Any]]:
    equal_c0 = next(row for row in calibration_rows if row["branch"] == "C0_equal_h0_omega_shape_frozen")
    native_c0 = next(row for row in calibration_rows if row["branch"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    shape_free_c0 = next(row for row in calibration_rows if row["branch"] == "C0_shape_free_CMB_calibrated")
    return [
        {
            "missing_piece": "fixed_background_CMB_calibration",
            "status": "confirmed",
            "evidence": f"fixed C0 repaired CMB chi2={fixed_c0_chi2:.6f}; native calibrated C0 chi2={float(native_c0['chi2_CMB']):.6f}",
            "required_fix": "label CMB-calibrated results secondary; do not use fixed-background CMB alone as branch death",
        },
        {
            "missing_piece": "equal_two_parameter_test",
            "status": "insufficient_for_C0" if float(equal_c0["delta_aic_vs_best_baseline"]) > 10.0 else "near_competitive",
            "evidence": f"C0 equal h0/omega delta AIC={float(equal_c0['delta_aic_vs_best_baseline']):.6f}",
            "required_fix": "if insufficient, C0 needs b_mem/early-limit calibration to address CMB",
        },
        {
            "missing_piece": "native_C0_CMB_calibration",
            "status": "near_competitive_secondary" if abs(float(native_c0["delta_aic_vs_best_baseline"])) <= 10.0 else "still_tense",
            "evidence": f"C0 native frozen-shape delta AIC={float(native_c0['delta_aic_vs_best_baseline']):.6f}; edge_flags={native_c0['edge_flags']}",
            "required_fix": "derive why b_mem/H0/omega_m0 may be CMB-calibrated from parent early-time limit",
        },
        {
            "missing_piece": "shape_free_guardrail",
            "status": "diagnostic_only",
            "evidence": f"C0 shape-free delta AIC={float(shape_free_c0['delta_aic_vs_best_baseline']):.6f}; edge_flags={shape_free_c0['edge_flags']}",
            "required_fix": "shape-free CMB tuning cannot count as support without parent-derived shape",
        },
        {
            "missing_piece": "official_CMB_likelihood",
            "status": "required_before_public_claim",
            "evidence": "this audit uses compressed Planck distance priors, model-dependent by construction",
            "required_fix": "define official Planck/ACT likelihood upgrade path before any public CMB claim",
        },
    ]


def gate_rows(source_32: dict[str, Any], calibration_rows: list[dict[str, Any]], fixed_c0_chi2: float) -> list[dict[str, Any]]:
    native_c0 = next(row for row in calibration_rows if row["branch"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    equal_c0 = next(row for row in calibration_rows if row["branch"] == "C0_equal_h0_omega_shape_frozen")
    return [
        {
            "gate": "source_32_complete",
            "status": "pass" if source_32.get("readout") == "locked_C0_demoted_for_repaired_CMB_distance_but_growth_subdiagnostic_retained" else "fail",
            "detail": str(source_32.get("readout")),
        },
        {
            "gate": "fixed_background_CMB_tense",
            "status": "pass" if fixed_c0_chi2 > 100.0 else "fail",
            "detail": f"fixed_C0_CMB_chi2={fixed_c0_chi2}",
        },
        {
            "gate": "equal_two_parameter_C0_near_competitive",
            "status": "pass" if abs(float(equal_c0["delta_aic_vs_best_baseline"])) <= 10.0 else "fail",
            "detail": f"equal_delta_AIC={equal_c0['delta_aic_vs_best_baseline']}",
        },
        {
            "gate": "native_C0_calibration_near_competitive",
            "status": "pass" if abs(float(native_c0["delta_aic_vs_best_baseline"])) <= 10.0 else "fail",
            "detail": f"native_delta_AIC={native_c0['delta_aic_vs_best_baseline']}",
        },
        {
            "gate": "calibrated_CMB_support_allowed",
            "status": "fail",
            "detail": "secondary CMB-calibrated closure only; parent early-time limit missing",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "compressed distance-prior stress test only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "fixed_branch_status",
            "status": "demoted",
            "evidence": "repaired fixed-background score strongly disfavors locked C0 in CMB-distance block",
            "next_action": "do not use fixed branch as cosmology support",
        },
        {
            "decision": "calibration_branch_status",
            "status": "secondary_closure_only",
            "evidence": "native CMB calibration can change the verdict but uses CMB retuning",
            "next_action": "derive CMB-compatible early-time/calibration limit",
        },
        {
            "decision": "growth_status",
            "status": "retained_subdiagnostic",
            "evidence": "growth rows remain close under same treatment",
            "next_action": "write growth-only readout separately",
        },
        {
            "decision": "next_theory_gate",
            "status": "parent_limit_required",
            "evidence": "without parent early-time limit, CMB calibration is phenomenological",
            "next_action": "write CMB-compatible MTS limit contract",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="CMB calibration freedom audit.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_32 = load_json(POST_CHECKPOINT / SOURCE_32_STATUS)
    repaired_scores = read_csv(POST_CHECKPOINT / SOURCE_31_RESULTS / "model_scores.csv")
    fixed_c0 = next(row for row in repaired_scores if row["model"] == "MTS_C0_minimal_smooth_memory")
    fixed_c0_chi2 = float(fixed_c0["chi2_CMB_distance_repaired"])
    params_order, obs, cov = cmb_data(MAIN_WORKBENCH)
    background = load_background_params(MAIN_WORKBENCH)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-CMB-calibration-freedom-audit"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    calibration_rows: list[dict[str, Any]] = []
    for spec in calibration_specs():
        base_params = {key: float(value) for key, value in background[spec["background_key"]]["params"].items()}
        calibration_rows.append(
            fit_cmb_branch(
                str(spec["tier"]),
                str(spec["branch"]),
                str(spec["physics_model"]),
                base_params,
                list(spec["fit_names"]),
                list(spec["bounds"]),
                params_order,
                obs,
                cov,
                bool(spec["support_allowed"]),
            )
        )
    add_tier_deltas(calibration_rows)

    missing_pieces = missing_piece_rows(calibration_rows, fixed_c0_chi2)
    gates = gate_rows(source_32, calibration_rows, fixed_c0_chi2)
    decisions = decision_rows()

    write_csv(results_dir / "CMB_calibration_freedom_audit.csv", calibration_rows, list(calibration_rows[0].keys()))
    write_csv(results_dir / "CMB_missing_piece_register.csv", missing_pieces, list(missing_pieces[0].keys()))
    write_csv(results_dir / "CMB_calibration_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "CMB_calibration_decision.csv", decisions, list(decisions[0].keys()))

    native_c0 = next(row for row in calibration_rows if row["branch"] == "C0_native_bmem_CMB_calibrated_shape_frozen")
    equal_c0 = next(row for row in calibration_rows if row["branch"] == "C0_equal_h0_omega_shape_frozen")
    readout = "CMB_calibration_freedom_changes_C0_status_but_parent_limit_missing"
    status = {
        "status": "complete_CMB_calibration_freedom_audit",
        "readout": readout,
        "recommendation": "write_CMB_compatible_MTS_limit_contract_next",
        "next_target": "34-CMB-compatible-MTS-limit-contract.md",
        "fixed_C0_CMB_chi2": fixed_c0_chi2,
        "C0_equal_two_parameter_delta_AIC": equal_c0["delta_aic_vs_best_baseline"],
        "C0_native_calibrated_delta_AIC": native_c0["delta_aic_vs_best_baseline"],
        "fixed_branch_status": "demoted",
        "calibrated_branch_status": "secondary_closure_only",
        "public_claim_allowed": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "outputs": {
            "CMB_calibration_freedom_audit": str(results_dir / "CMB_calibration_freedom_audit.csv"),
            "CMB_missing_piece_register": str(results_dir / "CMB_missing_piece_register.csv"),
            "CMB_calibration_gate_criteria": str(results_dir / "CMB_calibration_gate_criteria.csv"),
            "CMB_calibration_decision": str(results_dir / "CMB_calibration_decision.csv"),
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
