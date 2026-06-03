#!/usr/bin/env python3
"""Run the locked DeltaR=2/9 amplitude scout across existing robustness branches."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

import canonical_R_fixed_amplitude_scout as scout
import cosmo_SN_BAO_closure_runner as runner


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"
DELTA_R_LOCK = 2.0 / 9.0
B_MEM_LOCK = 2.0 / 27.0

BRANCHES = [
    {
        "branch": "T1_primary_fullcov_DR2",
        "run": RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke",
        "role": "primary",
    },
    {
        "branch": "T3_diagonal_fullsample_DR2",
        "run": RUNS_ROOT / "20260531-142133-cosmo-SN-BAO-short-smoke",
        "role": "covariance_diagnostic",
    },
    {
        "branch": "T4_small_fullcov_DR2",
        "run": RUNS_ROOT / "20260531-142622-cosmo-SN-BAO-short-smoke",
        "role": "small_sample_diagnostic",
    },
    {
        "branch": "T5_SH0ES_pressure",
        "run": RUNS_ROOT / "20260531-143143-cosmo-SN-BAO-short-smoke",
        "role": "local_H0_pressure_stress",
    },
    {
        "branch": "T5_matched_control",
        "run": RUNS_ROOT / "20260531-143247-cosmo-SN-BAO-short-smoke",
        "role": "matched_pressure_control",
    },
    {
        "branch": "T6_small_fullcov_DR1",
        "run": RUNS_ROOT / "20260531-143908-cosmo-SN-BAO-short-smoke",
        "role": "BAO_release_diagnostic",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_branch_data(run_dir: Path) -> tuple[dict[str, np.ndarray], dict[str, Any], dict[str, Any]]:
    config = json.loads((run_dir / "run_config.json").read_text(encoding="utf-8"))
    sn = runner.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config["sn_max_rows"],
        covariance_path=Path(config["sn_cov"]) if config["sn_cov"] else None,
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = runner.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    bao["label"] = config["bao_label"]
    return sn, bao, config


def baselines(run_dir: Path) -> dict[str, dict[str, float]]:
    rows = read_csv(run_dir / "results" / "fit_summary.csv")
    out: dict[str, dict[str, float]] = {}
    for row in rows:
        out[row["model"]] = {
            "chi2": float(row["chi2_total"]),
            "AIC": float(row["AIC"]),
            "BIC": float(row["BIC"]),
            "k": float(row["k"]),
            "n": float(row["n"]),
        }
    return out


def fitted_bmem(run_dir: Path) -> float:
    rows = read_csv(run_dir / "results" / "amplitude_policy.csv")
    for row in rows:
        if row["factor"] == "B_mem/b_mem":
            return float(row["best_fit"])
    return float("nan")


def branch_score(branch: dict[str, Any]) -> dict[str, Any]:
    sn, bao, config = load_branch_data(branch["run"])
    candidate = {
        "candidate": "two_ninth_boundary_charge",
        "DeltaR_fraction": "2/9",
        "DeltaR": DELTA_R_LOCK,
        "B_mem": B_MEM_LOCK,
    }
    score = scout.score_fixed_amplitude(candidate, sn, bao, max_iter=int(config["max_iter"]))
    fit_bmem = fitted_bmem(branch["run"])
    score.update(
        {
            "branch": branch["branch"],
            "role": branch["role"],
            "source_run": str(branch["run"]),
            "sn_rows": config["sn_rows_used"],
            "bao_rows": config["bao_rows_used"],
            "sn_covariance_mode": config["sn_covariance_mode"],
            "sn_observable": config["sn_observable"],
            "bao_label": config["bao_label"],
            "fitted_B_mem_reference": fit_bmem,
            "B_mem_lock_minus_fit": B_MEM_LOCK - fit_bmem,
            "relative_B_mem_lock_minus_fit": (B_MEM_LOCK - fit_bmem) / fit_bmem if fit_bmem else "",
        }
    )
    return score


def comparison_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    references = ["LCDM", "wCDM", "CPL", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"]
    rows: list[dict[str, Any]] = []
    for score in scores:
        ref_scores = baselines(Path(score["source_run"]))
        for reference in references:
            ref = ref_scores[reference]
            delta_chi2 = score["chi2_total"] - ref["chi2"]
            delta_aic = score["AIC"] - ref["AIC"]
            delta_bic = score["BIC"] - ref["BIC"]
            rows.append(
                {
                    "branch": score["branch"],
                    "reference": reference,
                    "delta_chi2": delta_chi2,
                    "delta_AIC": delta_aic,
                    "delta_BIC": delta_bic,
                    "readout": comparison_readout(reference, delta_chi2, delta_aic, delta_bic),
                }
            )
    return rows


def comparison_readout(reference: str, delta_chi2: float, delta_aic: float, delta_bic: float) -> str:
    if reference == "MTS_fixed_p3_u3quarter":
        if delta_chi2 <= 0.25:
            return "locked_amplitude_matches_fitted_branch"
        if delta_chi2 <= 2.0:
            return "locked_amplitude_small_penalty_vs_fitted"
        return "locked_amplitude_large_penalty_vs_fitted"
    if delta_aic < 0.0 and delta_bic < 0.0:
        return "locked_amplitude_wins_AIC_BIC"
    if delta_aic < 0.0 <= delta_bic:
        return "locked_amplitude_split_AIC_only"
    if delta_aic >= 0.0 and delta_bic < 0.0:
        return "locked_amplitude_split_BIC_only"
    return "locked_amplitude_loses_AIC_BIC"


def branch_gate_rows(scores: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_branch_reference = {(row["branch"], row["reference"]): row for row in comparisons}
    for score in scores:
        branch = score["branch"]
        vs_lcdm = by_branch_reference[(branch, "LCDM")]
        vs_fitted = by_branch_reference[(branch, "MTS_fixed_p3_u3quarter")]
        vs_zero = by_branch_reference[(branch, "MTS_Bmem_zero")]
        if score["role"] == "primary":
            gate = "primary_locked_amplitude_gate"
            result = (
                "pass"
                if float(vs_lcdm["delta_AIC"]) < 0.0
                and float(vs_lcdm["delta_BIC"]) < 0.0
                and float(vs_fitted["delta_chi2"]) <= 0.25
                else "fail"
            )
        else:
            gate = f"{score['role']}_stress_gate"
            result = (
                "pass"
                if float(vs_zero["delta_chi2"]) < 0.0 and float(vs_fitted["delta_chi2"]) <= 2.0
                else "warning"
            )
        rows.append(
            {
                "branch": branch,
                "gate": gate,
                "result": result,
                "locked_minus_fitted_B_mem": score["B_mem_lock_minus_fit"],
                "delta_chi2_vs_LCDM": vs_lcdm["delta_chi2"],
                "delta_AIC_vs_LCDM": vs_lcdm["delta_AIC"],
                "delta_BIC_vs_LCDM": vs_lcdm["delta_BIC"],
                "delta_chi2_vs_fitted_MTS": vs_fitted["delta_chi2"],
                "delta_chi2_vs_zero_memory": vs_zero["delta_chi2"],
                "interpretation": gate_interpretation(score, vs_lcdm, vs_fitted, vs_zero, result),
            }
        )
    return rows


def gate_interpretation(
    score: dict[str, Any],
    vs_lcdm: dict[str, Any],
    vs_fitted: dict[str, Any],
    vs_zero: dict[str, Any],
    result: str,
) -> str:
    if score["role"] == "primary" and result == "pass":
        return "locked 2/27 amplitude reproduces the primary fitted branch and beats LCDM without an amplitude parameter"
    if float(vs_fitted["delta_chi2"]) > 2.0:
        return "locked 2/27 amplitude underfits relative to branch-specific fitted amplitude; theorem target not robust here"
    if float(vs_zero["delta_chi2"]) < 0.0:
        return "locked 2/27 amplitude still improves over zero memory but remains diagnostic"
    return "locked 2/27 amplitude does not improve enough over zero memory in this branch"


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in gates if row["branch"] == "T1_primary_fullcov_DR2")
    warnings = [row for row in gates if row["result"] == "warning"]
    if primary["result"] == "pass" and warnings:
        verdict = "two_ninth_primary_passes_but_robustness_warnings"
    elif primary["result"] == "pass":
        verdict = "two_ninth_locked_amplitude_survives_matrix"
    else:
        verdict = "two_ninth_locked_amplitude_primary_fails"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "locked_DeltaR", "value": DELTA_R_LOCK},
        {"decision": "locked_B_mem", "value": B_MEM_LOCK},
        {"decision": "primary_gate", "value": primary["result"]},
        {"decision": "warning_gate_count", "value": len(warnings)},
        {"decision": "claim_ceiling", "value": "locked_amplitude_robustness_scout_only"},
        {"decision": "theory_promotion_allowed", "value": False},
        {"decision": "next_action", "value": "attempt_or_reject_parent_derivation_of_boundary_charge_contrast_2_over_9"},
    ]


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch in BRANCHES:
        rows.append(
            {
                "branch": branch["branch"],
                "source_run": str(branch["run"]),
                "run_config_exists": (branch["run"] / "run_config.json").exists(),
                "fit_summary_exists": (branch["run"] / "results" / "fit_summary.csv").exists(),
                "amplitude_policy_exists": (branch["run"] / "results" / "amplitude_policy.csv").exists(),
            }
        )
    return rows


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-two-ninth-T7-robustness"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [
        row
        for row in sources
        if not row["run_config_exists"] or not row["fit_summary_exists"] or not row["amplitude_policy_exists"]
    ]
    if missing:
        raise FileNotFoundError(f"Missing T7 source artifacts: {missing}")

    scores = [branch_score(branch) for branch in BRANCHES]
    comparisons = comparison_rows(scores)
    gates = branch_gate_rows(scores, comparisons)
    decisions = decision_rows(gates)

    write_csv(results_dir / "source_register.csv", sources, ["branch", "source_run", "run_config_exists", "fit_summary_exists", "amplitude_policy_exists"])
    write_csv(
        results_dir / "locked_branch_scores.csv",
        scores,
        [
            "branch",
            "role",
            "source_run",
            "sn_rows",
            "bao_rows",
            "sn_covariance_mode",
            "sn_observable",
            "bao_label",
            "candidate",
            "DeltaR_fraction",
            "DeltaR",
            "B_mem",
            "fitted_B_mem_reference",
            "B_mem_lock_minus_fit",
            "relative_B_mem_lock_minus_fit",
            "Omega_m",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "k",
            "n",
            "converged",
            "Omega_m_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(results_dir / "locked_branch_comparisons.csv", comparisons, ["branch", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "readout"])
    write_csv(
        results_dir / "branch_gates.csv",
        gates,
        [
            "branch",
            "gate",
            "result",
            "locked_minus_fitted_B_mem",
            "delta_chi2_vs_LCDM",
            "delta_AIC_vs_LCDM",
            "delta_BIC_vs_LCDM",
            "delta_chi2_vs_fitted_MTS",
            "delta_chi2_vs_zero_memory",
            "interpretation",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "locked_DeltaR": DELTA_R_LOCK,
        "locked_B_mem": B_MEM_LOCK,
        "branches_scored": len(scores),
        "claim_ceiling": "locked_amplitude_robustness_scout_only",
        "theory_promotion_allowed": False,
        "next_action": "inspect warnings before deciding whether 2/9 is a theorem target or primary coincidence",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
