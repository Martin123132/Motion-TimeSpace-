#!/usr/bin/env python3
"""Summarize T4 small-sample reproduction against the full-sample T2 branch."""

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
ABLATIONS = ["MTS_fitted_p", "MTS_fitted_u3"]
CONTROL = "MTS_Bmem_zero"
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


def latest_run(sn_max_rows: int | None, include_ablations: bool) -> Path:
    candidates: list[Path] = []
    for candidate in sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name):
        config_path = candidate / "run_config.json"
        if not config_path.exists():
            continue
        config = read_json(config_path)
        if (
            config.get("sn_covariance_mode") == "full"
            and config.get("sn_observable") == "mb-corr"
            and config.get("bao_label") == "DESI_DR2_primary"
            and config.get("include_mts_ablations") is include_ablations
            and config.get("sn_max_rows") == sn_max_rows
        ):
            candidates.append(candidate)
    if not candidates:
        label = "full" if sn_max_rows is None else str(sn_max_rows)
        raise FileNotFoundError(f"No matching full-covariance run found for sn_max_rows={label}.")
    return candidates[-1]


def edge_flag_rows(small_run: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(small_run / "results" / "prior_edge_table.csv"):
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
                "interpretation": "small_sample_edge_flag_diagnostic_only",
            }
        )
    return rows


def fixed_pattern_rows(full_run: Path, small_run: Path) -> list[dict[str, Any]]:
    full_lookup = comparison_lookup(full_run)
    small_lookup = comparison_lookup(small_run)
    rows: list[dict[str, Any]] = []
    for reference in BASELINES:
        full = full_lookup[(PRIMARY, reference)]
        small = small_lookup[(PRIMARY, reference)]
        full_delta_chi2 = float(full["delta_chi2"])
        full_delta_aic = float(full["delta_AIC"])
        full_delta_bic = float(full["delta_BIC"])
        small_delta_chi2 = float(small["delta_chi2"])
        small_delta_aic = float(small["delta_AIC"])
        small_delta_bic = float(small["delta_BIC"])
        if reference == "LCDM":
            pattern = small_delta_chi2 < 0.0 and small_delta_aic < 0.0 and small_delta_bic > 0.0
            verdict = "small_preserves_LCDM_split_round" if pattern else "small_reverses_LCDM_round"
        elif reference == "wCDM":
            pattern = small_delta_chi2 < 0.0 and small_delta_aic < 0.0 and small_delta_bic < 0.0
            verdict = "small_preserves_wCDM_equal_parameter_win" if pattern else "small_reverses_wCDM_round"
        else:
            pattern = small_delta_chi2 > 0.0 and small_delta_aic < 0.0 and small_delta_bic < 0.0
            verdict = "small_preserves_CPL_parsimony_round" if pattern else "small_reverses_CPL_round"
        rows.append(
            {
                "reference": reference,
                "full_delta_chi2": full_delta_chi2,
                "full_delta_AIC": full_delta_aic,
                "full_delta_BIC": full_delta_bic,
                "small_delta_chi2": small_delta_chi2,
                "small_delta_AIC": small_delta_aic,
                "small_delta_BIC": small_delta_bic,
                "qualitative_pattern_preserved": pattern,
                "verdict": verdict,
            }
        )
    return rows


def sample_shift_rows(full_run: Path, small_run: Path) -> list[dict[str, Any]]:
    full_fits = fit_by_model(full_run)
    small_fits = fit_by_model(small_run)
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        rows.append(
            {
                "model": model,
                "full_chi2": float(full_fits[model]["chi2_total"]),
                "small_chi2": float(small_fits[model]["chi2_total"]),
                "full_AIC": float(full_fits[model]["AIC"]),
                "small_AIC": float(small_fits[model]["AIC"]),
                "full_BIC": float(full_fits[model]["BIC"]),
                "small_BIC": float(small_fits[model]["BIC"]),
                "full_edge_flag": full_fits[model]["prior_edge_flag"],
                "small_edge_flag": small_fits[model]["prior_edge_flag"],
                "note": "absolute full-vs-small chi2 is not directly comparable because n changed",
            }
        )
    return rows


def amplitude_rows(full_run: Path, small_run: Path) -> list[dict[str, Any]]:
    def lookup(run: Path) -> dict[tuple[str, str], dict[str, str]]:
        return {
            (row["model"], row["parameter"]): row
            for row in read_csv(run / "results" / "prior_edge_table.csv")
        }

    full = lookup(full_run)
    small = lookup(small_run)
    rows: list[dict[str, Any]] = []
    for model in [PRIMARY, "MTS_fitted_p", "MTS_fitted_u3"]:
        full_value = float(full[(model, "B_mem")]["best_fit"])
        small_value = float(small[(model, "B_mem")]["best_fit"])
        shift = small_value - full_value
        relative = shift / full_value if full_value else float("nan")
        rows.append(
            {
                "model": model,
                "parameter": "B_mem",
                "full_sample": full_value,
                "small_sample": small_value,
                "small_minus_full": shift,
                "relative_shift": relative,
                "small_edge_flag": small[(model, "B_mem")]["edge_flag"],
                "interpretation": "small-sample amplitude diagnostic only",
            }
        )
    return rows


def gate_rows(
    full_run: Path,
    small_run: Path,
    full_status: dict[str, Any],
    small_status: dict[str, Any],
    small_config: dict[str, Any],
    fixed_patterns: list[dict[str, Any]],
    edge_rows_data: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    edge_models = {row["model"] for row in edge_rows_data}
    primary_edge_free = PRIMARY not in edge_models
    return [
        {
            "gate": "full_sample_reference_exists",
            "gate_pass": full_run.exists() and full_status.get("scores_written") is True,
            "notes": str(full_run),
        },
        {
            "gate": "small_sample_scores_written",
            "gate_pass": small_status.get("scores_written") is True,
            "notes": small_status.get("readout", ""),
        },
        {
            "gate": "small_sample_branch_confirmed",
            "gate_pass": small_config.get("sn_max_rows") == 250
            and small_config.get("sn_covariance_mode") == "full"
            and small_config.get("include_mts_ablations") is True
            and small_config.get("bao_label") == "DESI_DR2_primary",
            "notes": f"SN rows={small_config.get('sn_rows_used')}; BAO rows={small_config.get('bao_rows_used')}",
        },
        {
            "gate": "edge_flags_reproduced",
            "gate_pass": len(edge_rows_data) > 0,
            "notes": ";".join(f"{row['model']}:{row['parameter']}" for row in edge_rows_data),
        },
        {
            "gate": "primary_fixed_branch_edge_free",
            "gate_pass": primary_edge_free,
            "notes": "small-sample edge flags are in CPL and fitted-u3 ablation, not fixed canonical branch",
        },
        {
            "gate": "fixed_pattern_broadly_preserved",
            "gate_pass": all(row["qualitative_pattern_preserved"] for row in fixed_patterns),
            "notes": "fixed branch keeps LCDM split, wCDM win, CPL parsimony pattern",
        },
        {
            "gate": "small_sample_not_decisive",
            "gate_pass": small_status.get("stable_evidence_allowed") is False,
            "notes": "edge flags block stable-evidence language from T4",
        },
    ]


def decision_rows(gates: list[dict[str, Any]], edge_rows_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_failures = [row["gate"] for row in gates if not row["gate_pass"]]
    edge_labels = ";".join(f"{row['model']}:{row['parameter']}" for row in edge_rows_data)
    if gate_failures:
        verdict = "T4_small_sample_reproduction_unclean"
    elif edge_rows_data:
        verdict = "T4_reproduces_small_sample_instability_but_fixed_pattern_survives"
    else:
        verdict = "T4_small_sample_clean_minor_robustness_point"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(gate_failures)},
        {"decision": "edge_flags", "value": edge_labels},
        {"decision": "boxing_card", "value": "small-sample undercard is messy; fixed branch stays upright but no promotion"},
        {"decision": "claim_ceiling", "value": "diagnostic_only_no_stable_evidence"},
        {"decision": "next_target", "value": "T5_SH0ES_pressure_branch"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full-run-dir", type=Path, default=None)
    parser.add_argument("--small-run-dir", type=Path, default=None)
    args = parser.parse_args()

    full_run = args.full_run_dir or latest_run(None, True)
    small_run = args.small_run_dir or latest_run(250, True)
    full_status = read_json(full_run / "status.json")
    small_status = read_json(small_run / "status.json")
    small_config = read_json(small_run / "run_config.json")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T4-small-sample-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    edges = edge_flag_rows(small_run)
    fixed_patterns = fixed_pattern_rows(full_run, small_run)
    shifts = sample_shift_rows(full_run, small_run)
    amplitudes = amplitude_rows(full_run, small_run)
    gates = gate_rows(full_run, small_run, full_status, small_status, small_config, fixed_patterns, edges)
    decisions = decision_rows(gates, edges)

    write_csv(
        results_dir / "edge_flag_reproduction.csv",
        edges,
        ["model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "interpretation"],
    )
    write_csv(
        results_dir / "fixed_pattern_comparison.csv",
        fixed_patterns,
        [
            "reference",
            "full_delta_chi2",
            "full_delta_AIC",
            "full_delta_BIC",
            "small_delta_chi2",
            "small_delta_AIC",
            "small_delta_BIC",
            "qualitative_pattern_preserved",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "sample_size_metric_shift.csv",
        shifts,
        ["model", "full_chi2", "small_chi2", "full_AIC", "small_AIC", "full_BIC", "small_BIC", "full_edge_flag", "small_edge_flag", "note"],
    )
    write_csv(
        results_dir / "amplitude_sample_sensitivity.csv",
        amplitudes,
        ["model", "parameter", "full_sample", "small_sample", "small_minus_full", "relative_shift", "small_edge_flag", "interpretation"],
    )
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "gate_pass", "notes"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "full_run_dir": str(full_run),
        "small_run_dir": str(small_run),
        "readout": next(row["value"] for row in decisions if row["decision"] == "verdict"),
        "claim_ceiling": "diagnostic_only_no_stable_evidence",
        "stable_evidence_allowed": False,
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
