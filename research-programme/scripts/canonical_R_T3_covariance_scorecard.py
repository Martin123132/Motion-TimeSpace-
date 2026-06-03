#!/usr/bin/env python3
"""Compare T3 diagonal-covariance sensitivity against the T1 full-covariance primary run."""

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
BASELINES = ["LCDM", "wCDM", "CPL"]
MODELS = ["LCDM", "wCDM", "CPL", PRIMARY, CONTROL]


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


def edge_rows(run_dir: Path) -> list[dict[str, str]]:
    return read_csv(run_dir / "results" / "prior_edge_table.csv")


def comparison_lookup(run_dir: Path) -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(run_dir / "results" / "baseline_comparison.csv")
    }


def latest_run_with_covariance_mode(mode: str) -> Path:
    candidates: list[Path] = []
    for candidate in sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name):
        config_path = candidate / "run_config.json"
        if not config_path.exists():
            continue
        config = read_json(config_path)
        if (
            config.get("sn_covariance_mode") == mode
            and config.get("sn_observable") == "mb-corr"
            and config.get("bao_label") == "DESI_DR2_primary"
            and config.get("include_mts_ablations") is False
        ):
            candidates.append(candidate)
    if not candidates:
        raise FileNotFoundError(f"No matching {mode} short-smoke run found.")
    return candidates[-1]


def metric_shift_rows(full_fits: dict[str, dict[str, str]], diag_fits: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        full = full_fits[model]
        diag = diag_fits[model]
        rows.append(
            {
                "model": model,
                "full_chi2": float(full["chi2_total"]),
                "diagonal_chi2": float(diag["chi2_total"]),
                "diagonal_minus_full_chi2": float(diag["chi2_total"]) - float(full["chi2_total"]),
                "full_AIC": float(full["AIC"]),
                "diagonal_AIC": float(diag["AIC"]),
                "diagonal_minus_full_AIC": float(diag["AIC"]) - float(full["AIC"]),
                "full_BIC": float(full["BIC"]),
                "diagonal_BIC": float(diag["BIC"]),
                "diagonal_minus_full_BIC": float(diag["BIC"]) - float(full["BIC"]),
                "note": "absolute full-vs-diagonal chi2 is not directly comparable because covariance weighting changed",
            }
        )
    return rows


def baseline_pattern_rows(full_run: Path, diag_run: Path) -> list[dict[str, Any]]:
    full_lookup = comparison_lookup(full_run)
    diag_lookup = comparison_lookup(diag_run)
    rows: list[dict[str, Any]] = []
    for reference in BASELINES:
        full = full_lookup[(PRIMARY, reference)]
        diag = diag_lookup[(PRIMARY, reference)]
        full_delta_chi2 = float(full["delta_chi2"])
        full_delta_aic = float(full["delta_AIC"])
        full_delta_bic = float(full["delta_BIC"])
        diag_delta_chi2 = float(diag["delta_chi2"])
        diag_delta_aic = float(diag["delta_AIC"])
        diag_delta_bic = float(diag["delta_BIC"])
        if reference == "LCDM":
            verdict = "diagonal_strengthens_LCDM_round" if diag_delta_bic < 0.0 else "diagonal_keeps_LCDM_BIC_reservation"
        elif reference == "wCDM":
            verdict = "diagonal_preserves_equal_parameter_win" if diag_delta_aic < 0.0 and diag_delta_bic < 0.0 else "diagonal_reverses_wCDM_round"
        else:
            verdict = "diagonal_strengthens_CPL_round" if diag_delta_chi2 < 0.0 and diag_delta_aic < 0.0 and diag_delta_bic < 0.0 else "diagonal_weakens_CPL_round"
        rows.append(
            {
                "reference": reference,
                "full_delta_chi2": full_delta_chi2,
                "full_delta_AIC": full_delta_aic,
                "full_delta_BIC": full_delta_bic,
                "diagonal_delta_chi2": diag_delta_chi2,
                "diagonal_delta_AIC": diag_delta_aic,
                "diagonal_delta_BIC": diag_delta_bic,
                "qualitative_reversal": verdict in {"diagonal_reverses_wCDM_round", "diagonal_weakens_CPL_round"},
                "verdict": verdict,
            }
        )
    return rows


def b_mem(edge_data: list[dict[str, str]]) -> float:
    for row in edge_data:
        if row["model"] == PRIMARY and row["parameter"] == "B_mem":
            return float(row["best_fit"])
    raise KeyError("B_mem row not found for primary MTS branch.")


def amplitude_rows(full_run: Path, diag_run: Path) -> list[dict[str, Any]]:
    full_b = b_mem(edge_rows(full_run))
    diag_b = b_mem(edge_rows(diag_run))
    shift = diag_b - full_b
    relative = shift / full_b if full_b else float("nan")
    verdict = "amplitude_moves_but_same_order" if abs(relative) < 0.5 else "amplitude_strongly_covariance_sensitive"
    return [
        {
            "quantity": "B_mem",
            "full_covariance": full_b,
            "diagonal_covariance": diag_b,
            "diagonal_minus_full": shift,
            "relative_shift": relative,
            "verdict": verdict,
        },
        {
            "quantity": "DeltaR_conditional_eta1_aF1",
            "full_covariance": 3.0 * full_b,
            "diagonal_covariance": 3.0 * diag_b,
            "diagonal_minus_full": 3.0 * shift,
            "relative_shift": relative,
            "verdict": "conditional_translation_only",
        },
    ]


def gate_rows(
    full_run: Path,
    diag_run: Path,
    full_status: dict[str, Any],
    diag_status: dict[str, Any],
    diag_config: dict[str, Any],
    diag_fits: dict[str, dict[str, str]],
    diag_edges: list[dict[str, str]],
    pattern_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required = set(MODELS)
    all_converged = all(diag_fits[model]["convergence"] == "True" for model in required)
    edge_free = all(row["edge_flag"] == "False" for row in diag_edges)
    no_qualitative_reversal = not any(row["qualitative_reversal"] for row in pattern_rows)
    return [
        {
            "gate": "full_primary_reference_exists",
            "gate_pass": full_run.exists() and full_status.get("scores_written") is True,
            "notes": str(full_run),
        },
        {
            "gate": "diagonal_scores_written",
            "gate_pass": diag_status.get("scores_written") is True and diag_status.get("failures") == [],
            "notes": diag_status.get("readout", ""),
        },
        {
            "gate": "diagonal_branch_confirmed",
            "gate_pass": diag_config.get("sn_covariance_mode") == "diagonal"
            and diag_config.get("sn_observable") == "mb-corr"
            and diag_config.get("bao_label") == "DESI_DR2_primary",
            "notes": f"SN rows={diag_config.get('sn_rows_used')}; BAO rows={diag_config.get('bao_rows_used')}",
        },
        {
            "gate": "diagonal_required_models_converged",
            "gate_pass": all_converged,
            "notes": ";".join(sorted(required)),
        },
        {
            "gate": "diagonal_no_prior_edge_flags",
            "gate_pass": edge_free,
            "notes": "all diagonal fitted parameters are away from prior edges",
        },
        {
            "gate": "qualitative_scorecard_not_reversed",
            "gate_pass": no_qualitative_reversal,
            "notes": "diagonal covariance preserves or strengthens the baseline pattern",
        },
        {
            "gate": "full_covariance_remains_primary",
            "gate_pass": True,
            "notes": "diagonal branch is diagnostic only and does not outrank full covariance",
        },
    ]


def decision_rows(gates: list[dict[str, Any]], pattern_rows: list[dict[str, Any]], amplitudes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_failures = [row["gate"] for row in gates if not row["gate_pass"]]
    bmem_row = next(row for row in amplitudes if row["quantity"] == "B_mem")
    if gate_failures:
        verdict = "T3_unclean_do_not_use"
    elif any(row["qualitative_reversal"] for row in pattern_rows):
        verdict = "T3_covariance_sensitive_reversal"
    else:
        verdict = "T3_diagonal_preserves_or_strengthens_pattern"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(gate_failures)},
        {"decision": "LCDM_round", "value": next(row["verdict"] for row in pattern_rows if row["reference"] == "LCDM")},
        {"decision": "wCDM_round", "value": next(row["verdict"] for row in pattern_rows if row["reference"] == "wCDM")},
        {"decision": "CPL_round", "value": next(row["verdict"] for row in pattern_rows if row["reference"] == "CPL")},
        {"decision": "B_mem_relative_shift", "value": bmem_row["relative_shift"]},
        {"decision": "claim_ceiling", "value": "empirical_closure_scorecard_only"},
        {"decision": "next_target", "value": "T4_small_sample_reproduction"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-run-dir", type=Path, default=None)
    parser.add_argument("--diagonal-run-dir", type=Path, default=None)
    args = parser.parse_args()

    full_run = args.full_run_dir or latest_run_with_covariance_mode("full")
    diag_run = args.diagonal_run_dir or latest_run_with_covariance_mode("diagonal")
    full_status = read_json(full_run / "status.json")
    diag_status = read_json(diag_run / "status.json")
    diag_config = read_json(diag_run / "run_config.json")
    full_fits = fit_by_model(full_run)
    diag_fits = fit_by_model(diag_run)
    diag_edges = edge_rows(diag_run)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T3-covariance-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    shifts = metric_shift_rows(full_fits, diag_fits)
    patterns = baseline_pattern_rows(full_run, diag_run)
    amplitudes = amplitude_rows(full_run, diag_run)
    gates = gate_rows(full_run, diag_run, full_status, diag_status, diag_config, diag_fits, diag_edges, patterns)
    decisions = decision_rows(gates, patterns, amplitudes)

    write_csv(
        results_dir / "model_metric_shift.csv",
        shifts,
        [
            "model",
            "full_chi2",
            "diagonal_chi2",
            "diagonal_minus_full_chi2",
            "full_AIC",
            "diagonal_AIC",
            "diagonal_minus_full_AIC",
            "full_BIC",
            "diagonal_BIC",
            "diagonal_minus_full_BIC",
            "note",
        ],
    )
    write_csv(
        results_dir / "baseline_pattern_comparison.csv",
        patterns,
        [
            "reference",
            "full_delta_chi2",
            "full_delta_AIC",
            "full_delta_BIC",
            "diagonal_delta_chi2",
            "diagonal_delta_AIC",
            "diagonal_delta_BIC",
            "qualitative_reversal",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "amplitude_sensitivity.csv",
        amplitudes,
        ["quantity", "full_covariance", "diagonal_covariance", "diagonal_minus_full", "relative_shift", "verdict"],
    )
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "gate_pass", "notes"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "full_run_dir": str(full_run),
        "diagonal_run_dir": str(diag_run),
        "readout": next(row["value"] for row in decisions if row["decision"] == "verdict"),
        "claim_ceiling": "empirical_closure_scorecard_only",
        "stable_evidence_allowed": False,
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
