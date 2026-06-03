#!/usr/bin/env python3
"""Lock the repaired growth/CMB score decision without overclaiming."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_31_STATUS = Path("runs/20260531-002219-repaired-growth-CMB-score/status.json")
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


def leaderboard_rows(score_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "rank_AIC": rank,
            "model": row["model"],
            "chi2_growth_primary": float(row["chi2_growth_primary"]),
            "chi2_CMB_distance_repaired": float(row["chi2_CMB_distance_repaired"]),
            "chi2_total": float(row["chi2_total"]),
            "aic": float(row["aic"]),
            "bic": float(row["bic"]),
            "delta_aic_vs_best_baseline": float(row["delta_aic_vs_best_baseline"]),
            "delta_bic_vs_best_baseline": float(row["delta_bic_vs_best_baseline"]),
        }
        for rank, row in enumerate(sorted(score_rows, key=lambda item: float(item["aic"])), start=1)
    ]


def branch_decision_rows(score_rows: list[dict[str, str]], robustness_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    baselines = [row for row in score_rows if row["model"] in {"LCDM", "wCDM", "CPL"}]
    best_growth = min(baselines, key=lambda row: float(row["chi2_growth_primary"]))
    best_cmb = min(baselines, key=lambda row: float(row["chi2_CMB_distance_repaired"]))
    best_total = min(baselines, key=lambda row: float(row["chi2_total"]))
    robustness_by_model = {row["model"]: row for row in robustness_rows}
    best_full_shape = min(
        [row for row in robustness_rows if row["model"] in {"LCDM", "wCDM", "CPL"}],
        key=lambda row: float(row["chi2_growth_full_shape_only"]),
    )
    c0_full_shape = robustness_by_model["MTS_C0_minimal_smooth_memory"]
    return [
        {
            "branch": "locked_C0_growth_CMB",
            "decision": "demote_for_repaired_lightweight_CMB_distance_holdout",
            "evidence": f"delta_total_chi2={float(c0['chi2_total']) - float(best_total['chi2_total'])}",
            "claim_allowed": "no",
            "next_action": "do not use this locked branch as cosmology support",
        },
        {
            "branch": "growth_only_projection",
            "decision": "retain_as_interesting_near_competitive_subdiagnostic",
            "evidence": f"delta_primary_growth_chi2={float(c0['chi2_growth_primary']) - float(best_growth['chi2_growth_primary'])}",
            "claim_allowed": "no",
            "next_action": "record growth-only behavior separately from CMB",
        },
        {
            "branch": "full_shape_growth_robustness",
            "decision": "retain_as_near_competitive_subdiagnostic",
            "evidence": f"delta_full_shape_chi2={float(c0_full_shape['chi2_growth_full_shape_only']) - float(best_full_shape['chi2_growth_full_shape_only'])}",
            "claim_allowed": "no",
            "next_action": "apply any future growth jackknife to baselines and MTS equally",
        },
        {
            "branch": "CMB_distance_projection",
            "decision": "requires_calibration_or_parent_early_limit_before_revival",
            "evidence": f"delta_repaired_CMB_chi2={float(c0['chi2_CMB_distance_repaired']) - float(best_cmb['chi2_CMB_distance_repaired'])}",
            "claim_allowed": "no",
            "next_action": "audit CMB calibration freedoms and official likelihood path",
        },
    ]


def gate_rows(source_31: dict[str, Any], score_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    c0_delta_aic = float(c0["delta_aic_vs_best_baseline"])
    return [
        {
            "gate": "source_31_complete",
            "status": "pass" if source_31.get("readout") == "C0_not_preferred_repaired_CMB_distance_score" else "fail",
            "detail": str(source_31.get("readout")),
        },
        {
            "gate": "locked_C0_support_allowed",
            "status": "fail",
            "detail": f"delta_AIC_vs_best_baseline={c0_delta_aic}",
        },
        {
            "gate": "locked_C0_death_claim_allowed",
            "status": "fail",
            "detail": "this is one locked background/CMB-distance branch, not the full theory",
        },
        {
            "gate": "growth_only_subdiagnostic_retained",
            "status": "pass",
            "detail": "growth primary and full-shape deltas are small compared with CMB-distance delta",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "internal lightweight CMB-distance result only",
        },
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "33-CMB-calibration-freedom-audit.md",
            "purpose": "test whether equal CMB calibration/background freedom changes the CMB-distance verdict",
        },
        {
            "priority": 2,
            "target": "34-growth-only-holdout-readout.md",
            "purpose": "preserve the near-competitive growth-only result without calling it unified support",
        },
        {
            "priority": 3,
            "target": "official_CMB_likelihood_upgrade_contract",
            "purpose": "define when compressed distance priors must be replaced by official Planck/ACT likelihoods",
        },
        {
            "priority": 4,
            "target": "parent_early_time_limit_contract",
            "purpose": "derive the early radiation/sound-horizon behavior before claiming CMB compatibility",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Repaired score readout and decision.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_31 = load_json(root / SOURCE_31_STATUS)
    results_root = root / SOURCE_31_RESULTS
    score_rows = read_csv(results_root / "model_scores.csv")
    robustness_rows = read_csv(results_root / "robustness_diagnostics.csv")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-repaired-score-readout-and-decision"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    leaderboard = leaderboard_rows(score_rows)
    branch_decisions = branch_decision_rows(score_rows, robustness_rows)
    gates = gate_rows(source_31, score_rows)
    next_actions = next_action_rows()

    write_csv(results_dir / "repaired_score_leaderboard.csv", leaderboard, list(leaderboard[0].keys()))
    write_csv(results_dir / "branch_decision_register.csv", branch_decisions, list(branch_decisions[0].keys()))
    write_csv(results_dir / "repaired_decision_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "next_actions.csv", next_actions, list(next_actions[0].keys()))

    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    readout = "locked_C0_demoted_for_repaired_CMB_distance_but_growth_subdiagnostic_retained"
    status = {
        "status": "complete_repaired_score_readout_and_decision",
        "readout": readout,
        "recommendation": "CMB_calibration_freedom_audit_next",
        "next_target": "33-CMB-calibration-freedom-audit.md",
        "locked_C0_growth_CMB_status": "demoted_for_repaired_lightweight_CMB_distance_holdout",
        "growth_only_status": "retained_as_near_competitive_subdiagnostic",
        "C0_delta_aic_vs_best_baseline": c0["delta_aic_vs_best_baseline"],
        "public_claim_allowed": False,
        "C0_support_claim_allowed": False,
        "C0_death_claim_allowed": False,
        "outputs": {
            "repaired_score_leaderboard": str(results_dir / "repaired_score_leaderboard.csv"),
            "branch_decision_register": str(results_dir / "branch_decision_register.csv"),
            "repaired_decision_gates": str(results_dir / "repaired_decision_gates.csv"),
            "next_actions": str(results_dir / "next_actions.csv"),
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
