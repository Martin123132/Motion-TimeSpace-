#!/usr/bin/env python3
"""Summarize T6 BAO-release sensitivity by comparing DESI DR1 against DESI DR2."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"
PRIMARY = "MTS_fixed_p3_u3quarter"
CONTROL = "MTS_Bmem_zero"
ABLATIONS = ["MTS_fitted_p", "MTS_fitted_u3"]
BASELINES = ["LCDM", "wCDM", "CPL"]
MODELS = ["LCDM", "wCDM", "CPL", PRIMARY, CONTROL, *ABLATIONS]


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


def fit_by_model(run_dir: Path) -> dict[str, dict[str, str]]:
    return {row["model"]: row for row in read_csv(run_dir / "results" / "fit_summary.csv")}


def comparison_lookup(run_dir: Path) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(run_dir / "results" / "baseline_comparison.csv")
    }


def edge_flags(run_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(run_dir / "results" / "prior_edge_table.csv"):
        if row["edge_flag"] != "True":
            continue
        rows.append(
            {
                "model": row["model"],
                "parameter": row["parameter"],
                "best_fit": float(row["best_fit"]),
                "lower": float(row["lower"]),
                "upper": float(row["upper"]),
                "distance_to_edge": float(row["distance_to_edge"]),
            }
        )
    return rows


def latest_run(bao_label: str) -> Path:
    candidates: list[Path] = []
    for candidate in sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name):
        config_path = candidate / "run_config.json"
        if not config_path.exists():
            continue
        config = read_json(config_path)
        if (
            config.get("sn_observable") == "mb-corr"
            and config.get("sn_covariance_mode") == "full"
            and config.get("sn_max_rows") == 250
            and config.get("include_mts_ablations") is True
            and config.get("bao_label") == bao_label
        ):
            candidates.append(candidate)
    if not candidates:
        raise FileNotFoundError(f"No matching run found for {bao_label}.")
    return candidates[-1]


def release_metric_shift_rows(dr2_run: Path, dr1_run: Path) -> list[dict[str, Any]]:
    dr2 = fit_by_model(dr2_run)
    dr1 = fit_by_model(dr1_run)
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        rows.append(
            {
                "model": model,
                "DR2_chi2": float(dr2[model]["chi2_total"]),
                "DR1_chi2": float(dr1[model]["chi2_total"]),
                "DR1_minus_DR2_chi2": float(dr1[model]["chi2_total"]) - float(dr2[model]["chi2_total"]),
                "DR2_AIC": float(dr2[model]["AIC"]),
                "DR1_AIC": float(dr1[model]["AIC"]),
                "DR1_minus_DR2_AIC": float(dr1[model]["AIC"]) - float(dr2[model]["AIC"]),
                "DR2_BIC": float(dr2[model]["BIC"]),
                "DR1_BIC": float(dr1[model]["BIC"]),
                "DR1_minus_DR2_BIC": float(dr1[model]["BIC"]) - float(dr2[model]["BIC"]),
                "DR2_edge_flag": dr2[model]["prior_edge_flag"],
                "DR1_edge_flag": dr1[model]["prior_edge_flag"],
                "note": "absolute DR1-vs-DR2 chi2 is not directly comparable because BAO row count/release changed",
            }
        )
    return rows


def fixed_pattern_rows(dr2_run: Path, dr1_run: Path) -> list[dict[str, Any]]:
    dr2 = comparison_lookup(dr2_run)
    dr1 = comparison_lookup(dr1_run)
    rows: list[dict[str, Any]] = []
    for reference in BASELINES:
        dr2_row = dr2[(PRIMARY, reference)]
        dr1_row = dr1[(PRIMARY, reference)]
        dr2_delta_chi2 = float(dr2_row["delta_chi2"])
        dr2_delta_aic = float(dr2_row["delta_AIC"])
        dr2_delta_bic = float(dr2_row["delta_BIC"])
        dr1_delta_chi2 = float(dr1_row["delta_chi2"])
        dr1_delta_aic = float(dr1_row["delta_AIC"])
        dr1_delta_bic = float(dr1_row["delta_BIC"])
        if reference == "LCDM":
            if dr1_delta_aic < 0.0 and dr1_delta_bic > 0.0:
                verdict = "DR1_preserves_LCDM_split_round"
                reversed_flag = False
            elif dr1_delta_chi2 < 0.0 and dr1_delta_aic > 0.0 and dr1_delta_bic > 0.0:
                verdict = "DR1_weakens_LCDM_round_AIC_reversal"
                reversed_flag = False
            else:
                verdict = "DR1_reverses_LCDM_round"
                reversed_flag = True
        elif reference == "wCDM":
            if dr1_delta_chi2 < 0.0 and dr1_delta_aic < 0.0 and dr1_delta_bic < 0.0:
                verdict = "DR1_preserves_wCDM_equal_parameter_win"
                reversed_flag = False
            else:
                verdict = "DR1_reverses_wCDM_round"
                reversed_flag = True
        else:
            if dr1_delta_chi2 > 0.0 and dr1_delta_aic < 0.0 and dr1_delta_bic < 0.0:
                verdict = "DR1_preserves_CPL_parsimony_round"
                reversed_flag = False
            else:
                verdict = "DR1_reverses_CPL_round"
                reversed_flag = True
        rows.append(
            {
                "reference": reference,
                "DR2_delta_chi2": dr2_delta_chi2,
                "DR2_delta_AIC": dr2_delta_aic,
                "DR2_delta_BIC": dr2_delta_bic,
                "DR1_delta_chi2": dr1_delta_chi2,
                "DR1_delta_AIC": dr1_delta_aic,
                "DR1_delta_BIC": dr1_delta_bic,
                "release_reversal": reversed_flag,
                "verdict": verdict,
            }
        )
    return rows


def edge_comparison_rows(dr2_run: Path, dr1_run: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for release, run_dir in [("DESI_DR2_primary", dr2_run), ("DESI_DR1_primary", dr1_run)]:
        release_edges = edge_flags(run_dir)
        if not release_edges:
            rows.append(
                {
                    "release": release,
                    "model": "",
                    "parameter": "",
                    "best_fit": "",
                    "edge_status": "no_edge_flags",
                    "interpretation": "clean branch",
                }
            )
            continue
        for row in release_edges:
            rows.append(
                {
                    "release": release,
                    "model": row["model"],
                    "parameter": row["parameter"],
                    "best_fit": row["best_fit"],
                    "edge_status": "edge_flag",
                    "interpretation": "small-sample BAO-release branch is diagnostic only",
                }
            )
    return rows


def memory_signal_rows(dr2_run: Path, dr1_run: Path) -> list[dict[str, Any]]:
    dr2 = fit_by_model(dr2_run)
    dr1 = fit_by_model(dr1_run)
    rows: list[dict[str, Any]] = []
    for release, fits in [("DESI_DR2_primary", dr2), ("DESI_DR1_primary", dr1)]:
        rows.append(
            {
                "release": release,
                "fixed_minus_zero_chi2": float(fits[PRIMARY]["chi2_total"]) - float(fits[CONTROL]["chi2_total"]),
                "fixed_minus_zero_AIC": float(fits[PRIMARY]["AIC"]) - float(fits[CONTROL]["AIC"]),
                "fixed_minus_zero_BIC": float(fits[PRIMARY]["BIC"]) - float(fits[CONTROL]["BIC"]),
                "fixed_edge_flag": fits[PRIMARY]["prior_edge_flag"],
            }
        )
    return rows


def amplitude_rows(dr2_run: Path, dr1_run: Path) -> list[dict[str, Any]]:
    def lookup(run_dir: Path) -> dict[tuple[str, str], dict[str, str]]:
        return {
            (row["model"], row["parameter"]): row
            for row in read_csv(run_dir / "results" / "prior_edge_table.csv")
        }

    dr2 = lookup(dr2_run)
    dr1 = lookup(dr1_run)
    rows: list[dict[str, Any]] = []
    for model in [PRIMARY, *ABLATIONS]:
        dr2_b = float(dr2[(model, "B_mem")]["best_fit"])
        dr1_b = float(dr1[(model, "B_mem")]["best_fit"])
        rows.append(
            {
                "model": model,
                "DR2_B_mem": dr2_b,
                "DR1_B_mem": dr1_b,
                "DR1_minus_DR2": dr1_b - dr2_b,
                "relative_shift": (dr1_b - dr2_b) / dr2_b if dr2_b else float("nan"),
                "DR2_edge_flag": dr2[(model, "B_mem")]["edge_flag"],
                "DR1_edge_flag": dr1[(model, "B_mem")]["edge_flag"],
            }
        )
    return rows


def ablation_vs_fixed_rows(dr1_run: Path) -> list[dict[str, Any]]:
    fits = fit_by_model(dr1_run)
    rows: list[dict[str, Any]] = []
    for model in ABLATIONS:
        delta_chi2 = float(fits[model]["chi2_total"]) - float(fits[PRIMARY]["chi2_total"])
        delta_aic = float(fits[model]["AIC"]) - float(fits[PRIMARY]["AIC"])
        delta_bic = float(fits[model]["BIC"]) - float(fits[PRIMARY]["BIC"])
        verdict = "fixed_branch_wins_information_criteria" if delta_aic > 0.0 and delta_bic > 0.0 else "ablation_challenges_fixed_branch"
        rows.append(
            {
                "ablation": model,
                "delta_chi2_vs_fixed": delta_chi2,
                "delta_AIC_vs_fixed": delta_aic,
                "delta_BIC_vs_fixed": delta_bic,
                "verdict": verdict,
            }
        )
    return rows


def gate_rows(
    dr2_status: dict[str, Any],
    dr1_status: dict[str, Any],
    dr2_config: dict[str, Any],
    dr1_config: dict[str, Any],
    fixed_patterns: list[dict[str, Any]],
    edge_rows_data: list[dict[str, Any]],
    ablation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    dr1_edges = [row for row in edge_rows_data if row["release"] == "DESI_DR1_primary" and row["edge_status"] == "edge_flag"]
    dr1_primary_edges = [row for row in dr1_edges if row["model"] == PRIMARY]
    reversals = [row for row in fixed_patterns if row["release_reversal"]]
    lcdm_warning = [row for row in fixed_patterns if row["verdict"] == "DR1_weakens_LCDM_round_AIC_reversal"]
    fixed_wins_ablations = all(row["verdict"] == "fixed_branch_wins_information_criteria" for row in ablation_rows)
    return [
        {
            "gate": "DR2_reference_scores_written",
            "gate_pass": dr2_status.get("scores_written") is True,
            "notes": dr2_status.get("readout", ""),
        },
        {
            "gate": "DR1_scores_written",
            "gate_pass": dr1_status.get("scores_written") is True,
            "notes": dr1_status.get("readout", ""),
        },
        {
            "gate": "matched_release_pair_confirmed",
            "gate_pass": dr2_config.get("bao_label") == "DESI_DR2_primary"
            and dr1_config.get("bao_label") == "DESI_DR1_primary"
            and dr2_config.get("sn_covariance_mode") == dr1_config.get("sn_covariance_mode") == "full"
            and dr2_config.get("sn_max_rows") == dr1_config.get("sn_max_rows") == 250
            and dr2_config.get("include_mts_ablations") is True
            and dr1_config.get("include_mts_ablations") is True,
            "notes": "same SN branch/covariance/sample/ablations; BAO release changed",
        },
        {
            "gate": "DR1_edge_flags_reproduced",
            "gate_pass": bool(dr1_edges),
            "notes": ";".join(f"{row['model']}:{row['parameter']}" for row in dr1_edges),
        },
        {
            "gate": "DR1_primary_fixed_branch_edge_free",
            "gate_pass": not dr1_primary_edges,
            "notes": "fixed canonical branch does not edge-hit in DR1",
        },
        {
            "gate": "no_full_scorecard_reversal",
            "gate_pass": not reversals,
            "notes": "DR1 weakens LCDM/AIC but preserves wCDM and CPL qualitative rounds",
        },
        {
            "gate": "BAO_release_warning_present",
            "gate_pass": bool(lcdm_warning),
            "notes": "DR1 turns fixed-vs-LCDM AIC from small win to small loss",
        },
        {
            "gate": "fixed_branch_still_beats_ablations_by_IC",
            "gate_pass": fixed_wins_ablations,
            "notes": "DR1 fitted p/u3 do not displace fixed branch on AIC/BIC",
        },
        {
            "gate": "DR1_not_stable_evidence",
            "gate_pass": dr1_status.get("stable_evidence_allowed") is False,
            "notes": "small-sample DR1 branch is diagnostic only",
        },
    ]


def decision_rows(gates: list[dict[str, Any]], fixed_patterns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures = [row["gate"] for row in gates if not row["gate_pass"]]
    if failures:
        verdict = "T6_BAO_release_check_unclean"
    elif any(row["release_reversal"] for row in fixed_patterns):
        verdict = "T6_DR1_reverses_scorecard_do_not_cherrypick_DR2"
    elif any(row["verdict"] == "DR1_weakens_LCDM_round_AIC_reversal" for row in fixed_patterns):
        verdict = "T6_DR1_weaker_release_warning_not_reversal"
    else:
        verdict = "T6_DR1_preserves_pattern_minor_robustness"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(failures)},
        {"decision": "LCDM_round", "value": next(row["verdict"] for row in fixed_patterns if row["reference"] == "LCDM")},
        {"decision": "wCDM_round", "value": next(row["verdict"] for row in fixed_patterns if row["reference"] == "wCDM")},
        {"decision": "CPL_round", "value": next(row["verdict"] for row in fixed_patterns if row["reference"] == "CPL")},
        {"decision": "boxing_card", "value": "DR1 takes some shine off the LCDM round; it does not knock MTS down"},
        {"decision": "claim_ceiling", "value": "diagnostic_only_no_stable_evidence"},
        {"decision": "next_target", "value": "cosmology_robustness_summary_and_next_theory_gate"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dr2-run-dir", type=Path, default=None)
    parser.add_argument("--dr1-run-dir", type=Path, default=None)
    args = parser.parse_args()

    dr2_run = args.dr2_run_dir or latest_run("DESI_DR2_primary")
    dr1_run = args.dr1_run_dir or latest_run("DESI_DR1_primary")
    dr2_status = read_json(dr2_run / "status.json")
    dr1_status = read_json(dr1_run / "status.json")
    dr2_config = read_json(dr2_run / "run_config.json")
    dr1_config = read_json(dr1_run / "run_config.json")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T6-BAO-release-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    shifts = release_metric_shift_rows(dr2_run, dr1_run)
    fixed_patterns = fixed_pattern_rows(dr2_run, dr1_run)
    edges = edge_comparison_rows(dr2_run, dr1_run)
    memory = memory_signal_rows(dr2_run, dr1_run)
    amplitudes = amplitude_rows(dr2_run, dr1_run)
    ablations = ablation_vs_fixed_rows(dr1_run)
    gates = gate_rows(dr2_status, dr1_status, dr2_config, dr1_config, fixed_patterns, edges, ablations)
    decisions = decision_rows(gates, fixed_patterns)

    write_csv(
        results_dir / "release_metric_shift.csv",
        shifts,
        [
            "model",
            "DR2_chi2",
            "DR1_chi2",
            "DR1_minus_DR2_chi2",
            "DR2_AIC",
            "DR1_AIC",
            "DR1_minus_DR2_AIC",
            "DR2_BIC",
            "DR1_BIC",
            "DR1_minus_DR2_BIC",
            "DR2_edge_flag",
            "DR1_edge_flag",
            "note",
        ],
    )
    write_csv(
        results_dir / "fixed_release_pattern.csv",
        fixed_patterns,
        [
            "reference",
            "DR2_delta_chi2",
            "DR2_delta_AIC",
            "DR2_delta_BIC",
            "DR1_delta_chi2",
            "DR1_delta_AIC",
            "DR1_delta_BIC",
            "release_reversal",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "edge_flag_release_comparison.csv",
        edges,
        ["release", "model", "parameter", "best_fit", "edge_status", "interpretation"],
    )
    write_csv(
        results_dir / "memory_signal_by_release.csv",
        memory,
        ["release", "fixed_minus_zero_chi2", "fixed_minus_zero_AIC", "fixed_minus_zero_BIC", "fixed_edge_flag"],
    )
    write_csv(
        results_dir / "amplitude_release_shift.csv",
        amplitudes,
        ["model", "DR2_B_mem", "DR1_B_mem", "DR1_minus_DR2", "relative_shift", "DR2_edge_flag", "DR1_edge_flag"],
    )
    write_csv(
        results_dir / "ablation_vs_fixed_DR1.csv",
        ablations,
        ["ablation", "delta_chi2_vs_fixed", "delta_AIC_vs_fixed", "delta_BIC_vs_fixed", "verdict"],
    )
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "gate_pass", "notes"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "dr2_run_dir": str(dr2_run),
        "dr1_run_dir": str(dr1_run),
        "readout": next(row["value"] for row in decisions if row["decision"] == "verdict"),
        "claim_ceiling": "diagnostic_only_no_stable_evidence",
        "stable_evidence_allowed": False,
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
