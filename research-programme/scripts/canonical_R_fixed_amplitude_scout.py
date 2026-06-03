#!/usr/bin/env python3
"""Scout exact fixed-amplitude candidates for canonical_R_closure."""

from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
PRIMARY_SCORE_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
PRIMARY_SCORECARD_RUN = RUNS_ROOT / "20260531-141359-canonical-R-T1-scorecard"

sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as runner  # noqa: E402


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def baseline_by_model() -> dict[str, dict[str, float]]:
    rows = read_csv(PRIMARY_SCORE_RUN / "results" / "fit_summary.csv")
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


def amplitude_translation() -> dict[str, float]:
    rows = read_csv(PRIMARY_SCORECARD_RUN / "results" / "amplitude_translation.csv")
    out: dict[str, float] = {}
    for row in rows:
        if row["quantity"] in {"B_mem", "DeltaR_conditional_eta1_aF1"}:
            out[row["quantity"]] = float(row["value"])
    return out


def candidate_rows(primary_bmem: float, primary_delta_r: float) -> list[dict[str, Any]]:
    candidates = [
        ("two_ninth_boundary_charge", Fraction(2, 9), "closest simple charge split to strict full-cov fitted DeltaR"),
        ("quarter_boundary_charge", Fraction(1, 4), "cell-quarter contrast scout"),
        ("one_third_trace_charge", Fraction(1, 3), "unit trace-third contrast scout"),
        ("four_ninth_boundary_charge", Fraction(4, 9), "small-sample high-branch contrast scout"),
        ("half_boundary_charge", Fraction(1, 2), "maximally simple half-contrast scout"),
    ]
    rows: list[dict[str, Any]] = []
    for label, delta_r, rationale in candidates:
        b_mem = float(delta_r) / 3.0
        rows.append(
            {
                "candidate": label,
                "DeltaR_fraction": f"{delta_r.numerator}/{delta_r.denominator}",
                "DeltaR": float(delta_r),
                "B_mem": b_mem,
                "distance_to_primary_Bmem": b_mem - primary_bmem,
                "relative_distance_to_primary_Bmem": (b_mem - primary_bmem) / primary_bmem,
                "distance_to_primary_DeltaR": float(delta_r) - primary_delta_r,
                "relative_distance_to_primary_DeltaR": (float(delta_r) - primary_delta_r) / primary_delta_r,
                "theory_status": "scout_not_derived",
                "rationale": rationale,
            }
        )
    rows.sort(key=lambda item: abs(float(item["relative_distance_to_primary_Bmem"])))
    return rows


def load_primary_data() -> tuple[dict[str, np.ndarray], dict[str, Any], dict[str, Any]]:
    config = json.loads((PRIMARY_SCORE_RUN / "run_config.json").read_text(encoding="utf-8"))
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


def score_fixed_amplitude(
    candidate: dict[str, Any],
    sn: dict[str, np.ndarray],
    bao: dict[str, Any],
    max_iter: int,
) -> dict[str, Any]:
    b_mem = float(candidate["B_mem"])
    bounds = [(0.05, 0.6)]

    def objective(vector: np.ndarray) -> float:
        try:
            params = {"Omega_m": float(vector[0]), "B_mem": b_mem, "p": 3.0, "u3": 0.25}
            chi2_sn, _, _, _ = runner.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
            chi2_bao, _, _, _ = runner.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([0.30]), np.asarray([0.24]), np.asarray([0.36]), np.asarray([0.45])]
    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-9},
        )
        for start in starts
    ]
    result = min(results, key=lambda item: float(item.fun))
    omega_m = float(result.x[0])
    params = {"Omega_m": omega_m, "B_mem": b_mem, "p": 3.0, "u3": 0.25}
    chi2_sn, sn_offset, _, _ = runner.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
    chi2_bao, bao_alpha, _, _ = runner.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
    chi2_total = chi2_sn + chi2_bao
    n_points = int(len(sn["z"]) + len(bao["rows"]))
    k_count = 3
    aic = chi2_total + 2.0 * k_count
    bic = chi2_total + k_count * math.log(n_points)
    lower, upper = bounds[0]
    distance = min(omega_m - lower, upper - omega_m)
    return {
        "candidate": candidate["candidate"],
        "DeltaR_fraction": candidate["DeltaR_fraction"],
        "DeltaR": candidate["DeltaR"],
        "B_mem": b_mem,
        "Omega_m": omega_m,
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "AIC": aic,
        "BIC": bic,
        "k": k_count,
        "n": n_points,
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "converged": bool(result.success),
        "optimizer_message": str(result.message),
        "Omega_m_edge_flag": distance < 0.01 * (upper - lower),
        "claim_ceiling": "fixed_amplitude_scout_not_derived",
    }


def comparison_rows(scores: list[dict[str, Any]], baselines: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    references = ["LCDM", "wCDM", "CPL", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"]
    rows: list[dict[str, Any]] = []
    for score in scores:
        for reference in references:
            ref = baselines[reference]
            rows.append(
                {
                    "candidate": score["candidate"],
                    "reference": reference,
                    "delta_chi2": score["chi2_total"] - ref["chi2"],
                    "delta_AIC": score["AIC"] - ref["AIC"],
                    "delta_BIC": score["BIC"] - ref["BIC"],
                    "readout": fixed_candidate_readout(score, reference, ref),
                }
            )
    return rows


def fixed_candidate_readout(score: dict[str, Any], reference: str, ref: dict[str, float]) -> str:
    delta_aic = score["AIC"] - ref["AIC"]
    delta_bic = score["BIC"] - ref["BIC"]
    if reference == "MTS_fixed_p3_u3quarter":
        return "penalty_vs_fitted_amplitude" if delta_aic > 0 else "beats_fitted_branch_unexpected"
    if delta_aic < 0.0 and delta_bic < 0.0:
        return "fixed_candidate_wins_AIC_BIC"
    if delta_aic < 0.0 <= delta_bic:
        return "fixed_candidate_split_AIC_only"
    if delta_aic >= 0.0 and delta_bic < 0.0:
        return "fixed_candidate_BIC_only"
    return "fixed_candidate_loses_AIC_BIC"


def decision_rows(scores: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_candidate = {row["candidate"]: row for row in scores}
    two_ninth = by_candidate["two_ninth_boundary_charge"]
    penalty = next(
        float(row["delta_chi2"])
        for row in comparisons
        if row["candidate"] == "two_ninth_boundary_charge" and row["reference"] == "MTS_fixed_p3_u3quarter"
    )
    lcdm = next(
        row
        for row in comparisons
        if row["candidate"] == "two_ninth_boundary_charge" and row["reference"] == "LCDM"
    )
    if penalty <= 0.25 and float(lcdm["delta_AIC"]) < 0.0:
        verdict = "two_ninth_fixed_amplitude_scout_promising_not_derived"
    else:
        verdict = "two_ninth_fixed_amplitude_scout_not_strong_enough"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "best_fixed_candidate", "value": scores[0]["candidate"]},
        {"decision": "two_ninth_Bmem", "value": two_ninth["B_mem"]},
        {"decision": "two_ninth_DeltaR", "value": two_ninth["DeltaR"]},
        {"decision": "two_ninth_chi2_penalty_vs_fitted_MTS", "value": penalty},
        {"decision": "two_ninth_vs_LCDM_readout", "value": lcdm["readout"]},
        {"decision": "claim_ceiling", "value": "amplitude_scout_only_not_prediction"},
        {"decision": "next_action", "value": "write_boundary_charge_theorem_target_or_reject_two_ninth_if_not_reproducible"},
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-fixed-amplitude-scout"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    primary = amplitude_translation()
    candidates = candidate_rows(primary["B_mem"], primary["DeltaR_conditional_eta1_aF1"])
    sn, bao, config = load_primary_data()
    max_iter = int(config["max_iter"])
    scores = [score_fixed_amplitude(candidate, sn, bao, max_iter=max_iter) for candidate in candidates]
    scores.sort(key=lambda row: float(row["chi2_total"]))
    comparisons = comparison_rows(scores, baseline_by_model())
    decisions = decision_rows(scores, comparisons)

    write_csv(
        results_dir / "rational_candidate_register.csv",
        candidates,
        [
            "candidate",
            "DeltaR_fraction",
            "DeltaR",
            "B_mem",
            "distance_to_primary_Bmem",
            "relative_distance_to_primary_Bmem",
            "distance_to_primary_DeltaR",
            "relative_distance_to_primary_DeltaR",
            "theory_status",
            "rationale",
        ],
    )
    write_csv(
        results_dir / "fixed_candidate_scores.csv",
        scores,
        [
            "candidate",
            "DeltaR_fraction",
            "DeltaR",
            "B_mem",
            "Omega_m",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "k",
            "n",
            "sn_offset",
            "bao_alpha",
            "converged",
            "optimizer_message",
            "Omega_m_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "fixed_candidate_comparisons.csv",
        comparisons,
        ["candidate", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "readout"],
    )
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "primary_score_run": str(PRIMARY_SCORE_RUN),
        "primary_scorecard_run": str(PRIMARY_SCORECARD_RUN),
        "candidates_scored": len(scores),
        "claim_ceiling": "amplitude_scout_only_not_prediction",
        "theory_promotion_allowed": False,
        "next_action": "inspect fixed-candidate scorecard; only then decide whether two_ninth deserves a theorem target",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
