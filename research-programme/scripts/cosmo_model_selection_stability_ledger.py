#!/usr/bin/env python3
"""Aggregate SN+BAO smoke-fit branches into a model-selection scorecard.

This is an internal discipline tool, not a public evidence claim. It ranks each
run by chi2/AIC/BIC and gives the fixed-MTS branch a boxing-style verdict
against every fair baseline.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_ROOT = POST_CHECKPOINT / "runs"

SELECTED_RUNS = [
    ("20260531-124544-cosmo-SN-BAO-short-smoke", "SH0ES diagonal 250-row DR2 default"),
    ("20260531-125058-cosmo-SN-BAO-short-smoke", "SH0ES diagonal 250-row DR2 CPL-wa narrow"),
    ("20260531-125112-cosmo-SN-BAO-short-smoke", "SH0ES diagonal 250-row DR2 CPL-wa wide"),
    ("20260531-125144-cosmo-SN-BAO-short-smoke", "SH0ES diagonal 250-row DR2 MTS ablations"),
    ("20260531-125701-cosmo-SN-BAO-short-smoke", "no-SH0ES full-cov 250-row DR2 ablations"),
    ("20260531-125724-cosmo-SN-BAO-short-smoke", "no-SH0ES full-cov 250-row DR1 ablations"),
    ("20260531-125813-cosmo-SN-BAO-short-smoke", "no-SH0ES diagonal full-sample DR2"),
    ("20260531-125832-cosmo-SN-BAO-short-smoke", "no-SH0ES full-cov full-sample DR2"),
]

BASELINES = ["LCDM", "wCDM", "CPL"]
MTS_FIXED = "MTS_fixed_p3_u3quarter"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def to_float(value: str | float | int) -> float:
    return float(value)


def to_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def metric_judgement(delta: float) -> str:
    if delta < -6.0:
        return "clear_points_win"
    if delta < -2.0:
        return "points_win"
    if delta < 0.0:
        return "razor_points_win"
    if delta <= 2.0:
        return "draw_or_photo_finish"
    if delta <= 6.0:
        return "narrow_loss"
    return "clear_loss"


def round_verdict(
    delta_chi2: float,
    delta_aic: float,
    delta_bic: float,
    mts_edge: bool,
    baseline_edge: bool,
    mts_converged: bool,
    baseline_converged: bool,
) -> str:
    if not mts_converged:
        return "real_trouble_mts_not_converged"
    if mts_edge:
        return "real_trouble_mts_edge_hit"
    if not baseline_converged:
        return "unclean_round_baseline_not_converged"
    if baseline_edge:
        return "unclean_round_baseline_edge_hit"

    aic_card = metric_judgement(delta_aic)
    bic_card = metric_judgement(delta_bic)
    if delta_aic < 0.0 and delta_bic < 0.0:
        if delta_chi2 < 0.0:
            return "clean_points_win"
        return "style_points_win_information_criteria"
    if abs(delta_aic) <= 2.0 and abs(delta_bic) <= 2.0:
        return "respectable_draw"
    if (delta_aic < 0.0 and delta_bic <= 2.0) or (delta_bic < 0.0 and delta_aic <= 2.0):
        return "split_card_close_round"
    if aic_card == "narrow_loss" or bic_card == "narrow_loss":
        return "narrow_loss_keep_working"
    return "clear_loss_repair_needed"


def run_context(run_dir: Path, label: str) -> dict[str, Any]:
    config = read_json(run_dir / "run_config.json")
    status = read_json(run_dir / "status.json")
    return {
        "run_id": run_dir.name,
        "branch_label": label,
        "status_readout": status.get("readout", ""),
        "status_failures": ";".join(status.get("failures", [])),
        "sn_observable": config.get("sn_observable", "mu-sh0es"),
        "sn_covariance_mode": config.get("sn_covariance_mode", "diagonal"),
        "sn_rows_used": config.get("sn_rows_used", config.get("sn_max_rows", "")),
        "bao_label": config.get("bao_label", "BAO_primary"),
        "bao_rows_used": config.get("bao_rows_used", ""),
        "max_iter": config.get("max_iter", ""),
        "include_mts_ablations": config.get("include_mts_ablations", False),
        "prior_config": json.dumps(config.get("prior_config", {}), sort_keys=True),
    }


def ranking_rows(run_dir: Path, label: str, fit_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    context = run_context(run_dir, label)
    output: list[dict[str, Any]] = []
    for metric in ["chi2_total", "AIC", "BIC"]:
        ranked = sorted(fit_rows, key=lambda row: to_float(row[metric]))
        best_model = ranked[0]["model"]
        best_edge_free = not to_bool(ranked[0]["prior_edge_flag"])
        for rank, row in enumerate(ranked, start=1):
            output.append(
                {
                    **context,
                    "metric": metric,
                    "rank": rank,
                    "model": row["model"],
                    "value": row[metric],
                    "best_model": best_model,
                    "best_model_edge_free": best_edge_free,
                    "convergence": row["convergence"],
                    "prior_edge_flag": row["prior_edge_flag"],
                    "claim_ceiling": row["claim_ceiling"],
                }
            )
    return output


def fixed_mts_rounds(run_dir: Path, label: str, fit_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    context = run_context(run_dir, label)
    by_model = {row["model"]: row for row in fit_rows}
    if MTS_FIXED not in by_model:
        return []
    mts = by_model[MTS_FIXED]
    rows: list[dict[str, Any]] = []
    for baseline in BASELINES:
        if baseline not in by_model:
            continue
        base = by_model[baseline]
        delta_chi2 = to_float(mts["chi2_total"]) - to_float(base["chi2_total"])
        delta_aic = to_float(mts["AIC"]) - to_float(base["AIC"])
        delta_bic = to_float(mts["BIC"]) - to_float(base["BIC"])
        rows.append(
            {
                **context,
                "mts_model": MTS_FIXED,
                "baseline": baseline,
                "delta_chi2": delta_chi2,
                "delta_AIC": delta_aic,
                "delta_BIC": delta_bic,
                "chi2_card": metric_judgement(delta_chi2),
                "AIC_card": metric_judgement(delta_aic),
                "BIC_card": metric_judgement(delta_bic),
                "mts_edge": to_bool(mts["prior_edge_flag"]),
                "baseline_edge": to_bool(base["prior_edge_flag"]),
                "mts_converged": to_bool(mts["convergence"]),
                "baseline_converged": to_bool(base["convergence"]),
                "round_verdict": round_verdict(
                    delta_chi2,
                    delta_aic,
                    delta_bic,
                    to_bool(mts["prior_edge_flag"]),
                    to_bool(base["prior_edge_flag"]),
                    to_bool(mts["convergence"]),
                    to_bool(base["convergence"]),
                ),
            }
        )
    return rows


def branch_summary_rows(run_dir: Path, label: str, fit_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    context = run_context(run_dir, label)
    by_model = {row["model"]: row for row in fit_rows}
    if MTS_FIXED not in by_model:
        return []
    mts = by_model[MTS_FIXED]
    edge_free_rows = [row for row in fit_rows if not to_bool(row["prior_edge_flag"]) and to_bool(row["convergence"])]
    best_aic = min(edge_free_rows, key=lambda row: to_float(row["AIC"])) if edge_free_rows else None
    best_bic = min(edge_free_rows, key=lambda row: to_float(row["BIC"])) if edge_free_rows else None
    best_chi2 = min(edge_free_rows, key=lambda row: to_float(row["chi2_total"])) if edge_free_rows else None
    edge_models = [row["model"] for row in fit_rows if to_bool(row["prior_edge_flag"])]
    baseline_edges = [model for model in BASELINES if model in by_model and to_bool(by_model[model]["prior_edge_flag"])]
    return [
        {
            **context,
            "mts_chi2": mts["chi2_total"],
            "mts_AIC": mts["AIC"],
            "mts_BIC": mts["BIC"],
            "mts_edge": mts["prior_edge_flag"],
            "edge_models": ";".join(edge_models),
            "baseline_edges": ";".join(baseline_edges),
            "best_edge_free_chi2": best_chi2["model"] if best_chi2 else "",
            "best_edge_free_AIC": best_aic["model"] if best_aic else "",
            "best_edge_free_BIC": best_bic["model"] if best_bic else "",
            "mts_rank_chi2_edge_free": 1
            + sum(to_float(row["chi2_total"]) < to_float(mts["chi2_total"]) for row in edge_free_rows),
            "mts_rank_AIC_edge_free": 1 + sum(to_float(row["AIC"]) < to_float(mts["AIC"]) for row in edge_free_rows),
            "mts_rank_BIC_edge_free": 1 + sum(to_float(row["BIC"]) < to_float(mts["BIC"]) for row in edge_free_rows),
            "promotion_allowed": False,
            "promotion_blocker": "closure amplitude not parent-derived; branch dependence still under review",
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_RUNS_ROOT)
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = args.output_root / f"{timestamp}-cosmo-model-selection-stability-ledger"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    ranking: list[dict[str, Any]] = []
    rounds: list[dict[str, Any]] = []
    summary: list[dict[str, Any]] = []
    missing: list[str] = []
    for run_id, label in SELECTED_RUNS:
        source_run = args.runs_root / run_id
        fit_path = source_run / "results" / "fit_summary.csv"
        if not fit_path.exists():
            missing.append(run_id)
            continue
        fit_rows = read_csv(fit_path)
        ranking.extend(ranking_rows(source_run, label, fit_rows))
        rounds.extend(fixed_mts_rounds(source_run, label, fit_rows))
        summary.extend(branch_summary_rows(source_run, label, fit_rows))

    write_csv(
        results_dir / "model_rankings.csv",
        ranking,
        [
            "run_id",
            "branch_label",
            "status_readout",
            "status_failures",
            "sn_observable",
            "sn_covariance_mode",
            "sn_rows_used",
            "bao_label",
            "bao_rows_used",
            "max_iter",
            "include_mts_ablations",
            "prior_config",
            "metric",
            "rank",
            "model",
            "value",
            "best_model",
            "best_model_edge_free",
            "convergence",
            "prior_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "mts_fixed_round_scorecard.csv",
        rounds,
        [
            "run_id",
            "branch_label",
            "status_readout",
            "status_failures",
            "sn_observable",
            "sn_covariance_mode",
            "sn_rows_used",
            "bao_label",
            "bao_rows_used",
            "max_iter",
            "include_mts_ablations",
            "prior_config",
            "mts_model",
            "baseline",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "chi2_card",
            "AIC_card",
            "BIC_card",
            "mts_edge",
            "baseline_edge",
            "mts_converged",
            "baseline_converged",
            "round_verdict",
        ],
    )
    write_csv(
        results_dir / "branch_summary.csv",
        summary,
        [
            "run_id",
            "branch_label",
            "status_readout",
            "status_failures",
            "sn_observable",
            "sn_covariance_mode",
            "sn_rows_used",
            "bao_label",
            "bao_rows_used",
            "max_iter",
            "include_mts_ablations",
            "prior_config",
            "mts_chi2",
            "mts_AIC",
            "mts_BIC",
            "mts_edge",
            "edge_models",
            "baseline_edges",
            "best_edge_free_chi2",
            "best_edge_free_AIC",
            "best_edge_free_BIC",
            "mts_rank_chi2_edge_free",
            "mts_rank_AIC_edge_free",
            "mts_rank_BIC_edge_free",
            "promotion_allowed",
            "promotion_blocker",
        ],
    )

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "model_selection_stability_ledger_written" if not missing else "model_selection_stability_ledger_written_with_missing_runs",
        "source_runs_requested": len(SELECTED_RUNS),
        "source_runs_found": len(SELECTED_RUNS) - len(missing),
        "missing_runs": missing,
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 90; use scorecard language, not knockout-only language",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
