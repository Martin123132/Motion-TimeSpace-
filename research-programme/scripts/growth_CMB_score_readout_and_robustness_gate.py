#!/usr/bin/env python3
"""Read out the isolated growth/CMB first score and lock the robustness gate."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_28_STATUS = Path("runs/20260531-001059-isolated-growth-CMB-first-score-runner/status.json")
SOURCE_28_RESULTS = Path("runs/20260531-001059-isolated-growth-CMB-first-score-runner/results")


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


def score_leaderboard_rows(score_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    sorted_rows = sorted(score_rows, key=lambda row: float(row["aic"]))
    return [
        {
            "rank_AIC": rank,
            "model": row["model"],
            "chi2_growth_primary": float(row["chi2_growth_primary"]),
            "chi2_CMB_distance": float(row["chi2_CMB_distance"]),
            "chi2_total": float(row["chi2_total"]),
            "aic": float(row["aic"]),
            "bic": float(row["bic"]),
            "delta_aic_vs_best_baseline": float(row["delta_aic_vs_best_baseline"]),
            "delta_bic_vs_best_baseline": float(row["delta_bic_vs_best_baseline"]),
        }
        for rank, row in enumerate(sorted_rows, start=1)
    ]


def dataset_decomposition_rows(score_rows: list[dict[str, str]], robustness_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    robustness_by_model = {row["model"]: row for row in robustness_rows}
    return [
        {
            "model": row["model"],
            "growth_primary_chi2": float(row["chi2_growth_primary"]),
            "CMB_distance_chi2": float(row["chi2_CMB_distance"]),
            "total_chi2": float(row["chi2_total"]),
            "CMB_fraction_of_total": float(row["chi2_CMB_distance"]) / float(row["chi2_total"]),
            "growth_full_shape_chi2": float(robustness_by_model[row["model"]]["chi2_growth_full_shape_only"]),
            "sigma8_0_from_primary": float(robustness_by_model[row["model"]]["sigma8_0_from_primary"]),
        }
        for row in score_rows
    ]


def c0_delta_rows(score_rows: list[dict[str, str]], robustness_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    c0 = next(row for row in score_rows if row["model"] == "MTS_C0_minimal_smooth_memory")
    baselines = [row for row in score_rows if row["model"] in {"LCDM", "wCDM", "CPL"}]
    best_growth = min(baselines, key=lambda row: float(row["chi2_growth_primary"]))
    best_cmb = min(baselines, key=lambda row: float(row["chi2_CMB_distance"]))
    best_total = min(baselines, key=lambda row: float(row["chi2_total"]))
    robustness_by_model = {row["model"]: row for row in robustness_rows}
    best_full_shape = min(
        [row for row in robustness_rows if row["model"] in {"LCDM", "wCDM", "CPL"}],
        key=lambda row: float(row["chi2_growth_full_shape_only"]),
    )
    c0_full_shape = robustness_by_model["MTS_C0_minimal_smooth_memory"]
    return [
        {
            "comparison": "primary_growth_vs_best_baseline",
            "best_baseline": best_growth["model"],
            "C0_value": float(c0["chi2_growth_primary"]),
            "baseline_value": float(best_growth["chi2_growth_primary"]),
            "C0_minus_baseline": float(c0["chi2_growth_primary"]) - float(best_growth["chi2_growth_primary"]),
            "interpretation": "growth_side_close",
        },
        {
            "comparison": "CMB_distance_vs_best_baseline",
            "best_baseline": best_cmb["model"],
            "C0_value": float(c0["chi2_CMB_distance"]),
            "baseline_value": float(best_cmb["chi2_CMB_distance"]),
            "C0_minus_baseline": float(c0["chi2_CMB_distance"]) - float(best_cmb["chi2_CMB_distance"]),
            "interpretation": "CMB_distance_side_dominates_failure",
        },
        {
            "comparison": "total_vs_best_baseline",
            "best_baseline": best_total["model"],
            "C0_value": float(c0["chi2_total"]),
            "baseline_value": float(best_total["chi2_total"]),
            "C0_minus_baseline": float(c0["chi2_total"]) - float(best_total["chi2_total"]),
            "interpretation": "not_preferred",
        },
        {
            "comparison": "full_shape_growth_robustness",
            "best_baseline": best_full_shape["model"],
            "C0_value": float(c0_full_shape["chi2_growth_full_shape_only"]),
            "baseline_value": float(best_full_shape["chi2_growth_full_shape_only"]),
            "C0_minus_baseline": float(c0_full_shape["chi2_growth_full_shape_only"]) - float(best_full_shape["chi2_growth_full_shape_only"]),
            "interpretation": "full_shape_growth_close",
        },
    ]


def gate_rows(source_28: dict[str, Any], score_rows: list[dict[str, str]], deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c0_total_delta = next(row for row in deltas if row["comparison"] == "total_vs_best_baseline")["C0_minus_baseline"]
    c0_growth_delta = next(row for row in deltas if row["comparison"] == "primary_growth_vs_best_baseline")["C0_minus_baseline"]
    c0_cmb_delta = next(row for row in deltas if row["comparison"] == "CMB_distance_vs_best_baseline")["C0_minus_baseline"]
    all_cmb_huge = all(float(row["chi2_CMB_distance"]) > 1000.0 for row in score_rows)
    return [
        {
            "gate": "source_28_complete",
            "status": "pass" if source_28.get("readout") == "isolated_C0_not_preferred_first_growth_CMB_score" else "fail",
            "detail": str(source_28.get("readout")),
        },
        {
            "gate": "C0_preferred_in_first_score",
            "status": "fail",
            "detail": f"delta_total_vs_best_baseline={c0_total_delta}",
        },
        {
            "gate": "growth_side_competitive",
            "status": "pass" if abs(c0_growth_delta) < 2.0 else "fail",
            "detail": f"delta_primary_growth={c0_growth_delta}",
        },
        {
            "gate": "CMB_distance_side_dominates_C0_failure",
            "status": "pass" if c0_cmb_delta > 1000.0 else "fail",
            "detail": f"delta_CMB_distance={c0_cmb_delta}",
        },
        {
            "gate": "CMB_distance_implementation_audit_required",
            "status": "pass" if all_cmb_huge else "fail",
            "detail": "all models have very large compressed CMB-distance chi2; audit before interpretation",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "internal diagnostic only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "locked_C0_status",
            "status": "first_score_tension",
            "evidence": "C0 is not preferred under total chi2/AIC/BIC",
            "next_action": "audit compressed CMB-distance implementation before demotion",
        },
        {
            "decision": "growth_status",
            "status": "not_the_problem_in_this_run",
            "evidence": "primary and full-shape growth chi2 are close to best baseline",
            "next_action": "keep growth decomposition separate in robustness",
        },
        {
            "decision": "CMB_status",
            "status": "dominant_tension_and_possible_pipeline_stress",
            "evidence": "all models have huge CMB-distance chi2, and C0/CPL are much worse than wCDM",
            "next_action": "create CMB-distance-prior implementation audit",
        },
        {
            "decision": "claim_status",
            "status": "no_claim",
            "evidence": "first score is internal and CMB approximation is not audited",
            "next_action": "do not call support or death",
        },
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "30-CMB-distance-prior-implementation-audit.md",
            "purpose": "check R, l_A, covariance ordering, units, and default Planck table assumptions",
        },
        {
            "priority": 2,
            "target": "growth_only_sanity_readout",
            "purpose": "record the near-competitive growth-only result separately from CMB",
        },
        {
            "priority": 3,
            "target": "CMB_only_baseline_reproduction",
            "purpose": "verify LCDM/wCDM/CPL reproduce a known compressed CMB benchmark before judging MTS",
        },
        {
            "priority": 4,
            "target": "branch_demote_if_audit_passes",
            "purpose": "if CMB audit is correct, demote this locked C0 branch for CMB/growth holdout",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Growth/CMB score readout and robustness gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_28 = load_json(root / SOURCE_28_STATUS)
    results_root = root / SOURCE_28_RESULTS
    score_rows = read_csv(results_root / "model_scores.csv")
    robustness_rows = read_csv(results_root / "robustness_diagnostics.csv")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-growth-CMB-score-readout-and-robustness-gate"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    leaderboard = score_leaderboard_rows(score_rows)
    decomposition = dataset_decomposition_rows(score_rows, robustness_rows)
    deltas = c0_delta_rows(score_rows, robustness_rows)
    gates = gate_rows(source_28, score_rows, deltas)
    decisions = decision_rows()
    next_actions = next_action_rows()

    write_csv(results_dir / "score_leaderboard.csv", leaderboard, list(leaderboard[0].keys()))
    write_csv(results_dir / "dataset_tension_decomposition.csv", decomposition, list(decomposition[0].keys()))
    write_csv(results_dir / "C0_delta_decomposition.csv", deltas, list(deltas[0].keys()))
    write_csv(results_dir / "robustness_gate_decision.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "score_readout_decision.csv", decisions, list(decisions[0].keys()))
    write_csv(results_dir / "next_actions.csv", next_actions, list(next_actions[0].keys()))

    readout = "growth_CMB_score_disfavors_locked_C0_but_CMB_distance_block_dominates"
    status = {
        "status": "complete_growth_CMB_score_readout_and_robustness_gate",
        "readout": readout,
        "recommendation": "audit_CMB_distance_prior_before_interpretation",
        "next_target": "30-CMB-distance-prior-implementation-audit.md",
        "C0_first_score_status": "not_preferred",
        "growth_side_status": "near_competitive",
        "CMB_distance_status": "dominant_tension_audit_required",
        "public_claim_allowed": False,
        "empirical_claim_allowed_now": False,
        "branch_death_claim_allowed": False,
        "branch_support_claim_allowed": False,
        "outputs": {
            "score_leaderboard": str(results_dir / "score_leaderboard.csv"),
            "dataset_tension_decomposition": str(results_dir / "dataset_tension_decomposition.csv"),
            "C0_delta_decomposition": str(results_dir / "C0_delta_decomposition.csv"),
            "robustness_gate_decision": str(results_dir / "robustness_gate_decision.csv"),
            "score_readout_decision": str(results_dir / "score_readout_decision.csv"),
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
