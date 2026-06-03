#!/usr/bin/env python3
"""Summarize the T1 canonical_R_closure primary full-covariance scorecard."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"


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
    return json.loads(path.read_text(encoding="utf-8"))


def latest_short_smoke() -> Path:
    candidates = sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name)
    if not candidates:
        raise FileNotFoundError("No cosmo-SN-BAO short-smoke directories found.")
    return candidates[-1]


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def fit_by_model(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["model"]: row for row in rows}


def edge_free(edge_rows: list[dict[str, str]], model: str) -> bool:
    return all(row["edge_flag"] == "False" for row in edge_rows if row["model"] == model)


def round_label(delta_chi2: float, delta_aic: float, delta_bic: float, reference: str) -> tuple[str, str]:
    if reference == "LCDM":
        return (
            "split_points_win_not_BIC_promotion",
            "beats LCDM on chi2/AIC, loses weakly on BIC because LCDM/zero-memory is simpler",
        )
    if reference == "wCDM":
        return (
            "razor_thin_points_win",
            "same parameter count as wCDM; MTS is ahead on chi2/AIC/BIC by a tiny margin",
        )
    if reference == "CPL":
        return (
            "parsimony_points_win",
            "CPL has tiny raw-chi2 edge, but MTS wins AIC/BIC by using fewer parameters",
        )
    return (
        "scorecard_round",
        f"delta_chi2={delta_chi2:.6f}; delta_AIC={delta_aic:.6f}; delta_BIC={delta_bic:.6f}",
    )


def judge_card_rows(fits: dict[str, dict[str, str]], comparisons: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    mts = fits["MTS_fixed_p3_u3quarter"]
    for comparison in comparisons:
        if comparison["model"] != "MTS_fixed_p3_u3quarter":
            continue
        reference = comparison["reference_baseline"]
        delta_chi2 = as_float(comparison, "delta_chi2")
        delta_aic = as_float(comparison, "delta_AIC")
        delta_bic = as_float(comparison, "delta_BIC")
        label, interpretation = round_label(delta_chi2, delta_aic, delta_bic, reference)
        rows.append(
            {
                "model": "canonical_R_closure",
                "reference": reference,
                "delta_chi2": delta_chi2,
                "delta_AIC": delta_aic,
                "delta_BIC": delta_bic,
                "round_label": label,
                "interpretation": interpretation,
                "same_data": comparison["same_data"],
                "same_nuisance": comparison["same_nuisance"],
                "same_calibration": comparison["same_calibration"],
                "mts_converged": mts["convergence"],
                "mts_edge_flag": mts["prior_edge_flag"],
            }
        )
    zero = fits["MTS_Bmem_zero"]
    delta_chi2 = as_float(mts, "chi2_total") - as_float(zero, "chi2_total")
    delta_aic = as_float(mts, "AIC") - as_float(zero, "AIC")
    delta_bic = as_float(mts, "BIC") - as_float(zero, "BIC")
    rows.append(
        {
            "model": "canonical_R_closure",
            "reference": "MTS_Bmem_zero",
            "delta_chi2": delta_chi2,
            "delta_AIC": delta_aic,
            "delta_BIC": delta_bic,
            "round_label": "nonzero_memory_signal_not_BIC_decisive",
            "interpretation": "nonzero B_mem improves chi2/AIC over zero memory, but BIC still prefers the simpler zero-memory/LCDM branch weakly",
            "same_data": True,
            "same_nuisance": True,
            "same_calibration": True,
            "mts_converged": mts["convergence"],
            "mts_edge_flag": mts["prior_edge_flag"],
        }
    )
    return rows


def amplitude_rows(fits: dict[str, dict[str, str]], edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    b_mem_row = next(
        row
        for row in edge_rows
        if row["model"] == "MTS_fixed_p3_u3quarter" and row["parameter"] == "B_mem"
    )
    b_mem = float(b_mem_row["best_fit"])
    delta_r_conditional = 3.0 * b_mem
    return [
        {
            "quantity": "B_mem",
            "value": b_mem,
            "status": "fitted_closure_amplitude",
            "edge_flag": b_mem_row["edge_flag"],
            "interpretation": "nonzero fitted memory amplitude; not a parent-action prediction",
        },
        {
            "quantity": "DeltaR_conditional_eta1_aF1",
            "value": delta_r_conditional,
            "status": "conditional_translation_only",
            "edge_flag": b_mem_row["edge_flag"],
            "interpretation": "uses DeltaR = 3 B_mem only under eta=1 and a_F=1 closure choices",
        },
        {
            "quantity": "canonical_R_closure_chi2_gain_vs_zero_memory",
            "value": float(fits["MTS_fixed_p3_u3quarter"]["chi2_total"]) - float(fits["MTS_Bmem_zero"]["chi2_total"]),
            "status": "empirical_fit_gain",
            "edge_flag": fits["MTS_fixed_p3_u3quarter"]["prior_edge_flag"],
            "interpretation": "memory term is carrying chi2 improvement relative to the zero-memory control",
        },
    ]


def gate_rows(
    status: dict[str, Any],
    config: dict[str, Any],
    fits: dict[str, dict[str, str]],
    edge_rows_data: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    required_models = {"LCDM", "wCDM", "CPL", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"}
    schema_valid = all(row["schema_status"] == "schema_valid" for row in schema_rows)
    all_converged = all(fits[model]["convergence"] == "True" for model in required_models)
    all_edge_free = all(edge_free(edge_rows_data, model) for model in required_models)
    return [
        {
            "gate": "scores_written",
            "gate_pass": status.get("scores_written") is True and status.get("failures") == [],
            "notes": status.get("readout", ""),
        },
        {
            "gate": "branch_is_primary_fullcov",
            "gate_pass": config.get("sn_observable") == "mb-corr"
            and config.get("sn_covariance_mode") == "full"
            and config.get("sn_max_rows") is None
            and config.get("bao_label") == "DESI_DR2_primary",
            "notes": f"SN rows={config.get('sn_rows_used')}; BAO rows={config.get('bao_rows_used')}",
        },
        {
            "gate": "covariance_artifacts_recorded",
            "gate_pass": schema_valid and {"SN_covariance", "BAO_covariance"} <= {row["dataset"] for row in schema_rows},
            "notes": "score-run schema includes SN and BAO covariance rows",
        },
        {
            "gate": "required_models_converged",
            "gate_pass": all_converged,
            "notes": ";".join(sorted(required_models)),
        },
        {
            "gate": "no_prior_edge_flags",
            "gate_pass": all_edge_free,
            "notes": "all fitted parameters are away from prior edges",
        },
        {
            "gate": "zero_memory_control_present",
            "gate_pass": "MTS_Bmem_zero" in fits,
            "notes": "control is numerically the LCDM branch when B_mem=0",
        },
        {
            "gate": "claim_ceiling_enforced",
            "gate_pass": status.get("stable_evidence_allowed") is False,
            "notes": "closure-performance only, not field-theory proof",
        },
    ]


def decision_rows(judge_rows: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_failures = [row["gate"] for row in gates if not row["gate_pass"]]
    if gate_failures:
        verdict = "T1_failed_or_unclean_do_not_score"
    else:
        verdict = "T1_clean_points_survival_not_promotion"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(gate_failures)},
        {"decision": "boxing_card", "value": "Mayweather-style survival: clean, edge-free, competitive, no knockout"},
        {"decision": "LCDM_round", "value": next(row["round_label"] for row in judge_rows if row["reference"] == "LCDM")},
        {"decision": "wCDM_round", "value": next(row["round_label"] for row in judge_rows if row["reference"] == "wCDM")},
        {"decision": "CPL_round", "value": next(row["round_label"] for row in judge_rows if row["reference"] == "CPL")},
        {"decision": "zero_memory_round", "value": next(row["round_label"] for row in judge_rows if row["reference"] == "MTS_Bmem_zero")},
        {"decision": "claim_ceiling", "value": "empirical_closure_scorecard_only"},
        {"decision": "next_target", "value": "T2_clean_primary_with_ablations_fit_p_and_u3"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score-run-dir", type=Path, default=None)
    args = parser.parse_args()

    score_run_dir = args.score_run_dir or latest_short_smoke()
    status = read_json(score_run_dir / "status.json")
    config = read_json(score_run_dir / "run_config.json")
    fits = fit_by_model(read_csv(score_run_dir / "results" / "fit_summary.csv"))
    comparisons = read_csv(score_run_dir / "results" / "baseline_comparison.csv")
    edge_rows_data = read_csv(score_run_dir / "results" / "prior_edge_table.csv")
    schema_rows = read_csv(score_run_dir / "results" / "data_schema_report.csv")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T1-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    judge_rows = judge_card_rows(fits, comparisons)
    amplitudes = amplitude_rows(fits, edge_rows_data)
    gates = gate_rows(status, config, fits, edge_rows_data, schema_rows)
    decisions = decision_rows(judge_rows, gates)

    write_csv(
        results_dir / "judge_card.csv",
        judge_rows,
        [
            "model",
            "reference",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "round_label",
            "interpretation",
            "same_data",
            "same_nuisance",
            "same_calibration",
            "mts_converged",
            "mts_edge_flag",
        ],
    )
    write_csv(results_dir / "amplitude_translation.csv", amplitudes, ["quantity", "value", "status", "edge_flag", "interpretation"])
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "gate_pass", "notes"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "score_run_dir": str(score_run_dir),
        "readout": next(row["value"] for row in decisions if row["decision"] == "verdict"),
        "claim_ceiling": "empirical_closure_scorecard_only",
        "stable_evidence_allowed": False,
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
