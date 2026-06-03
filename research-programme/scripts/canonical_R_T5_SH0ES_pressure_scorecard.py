#!/usr/bin/env python3
"""Summarize the T5 SH0ES-pressure branch against a matched no-SH0ES control."""

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


def latest_run(observable: str) -> Path:
    candidates: list[Path] = []
    for candidate in sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name):
        config_path = candidate / "run_config.json"
        if not config_path.exists():
            continue
        config = read_json(config_path)
        if (
            config.get("sn_observable") == observable
            and config.get("sn_covariance_mode") == "diagonal"
            and config.get("sn_max_rows") == 250
            and config.get("include_mts_ablations") is True
            and config.get("bao_label") == "DESI_DR2_primary"
        ):
            candidates.append(candidate)
    if not candidates:
        raise FileNotFoundError(f"No matching T5-style run found for observable={observable}.")
    return candidates[-1]


def pressure_model_shift_rows(control_run: Path, pressure_run: Path) -> list[dict[str, Any]]:
    control = fit_by_model(control_run)
    pressure = fit_by_model(pressure_run)
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        rows.append(
            {
                "model": model,
                "control_chi2": float(control[model]["chi2_total"]),
                "pressure_chi2": float(pressure[model]["chi2_total"]),
                "pressure_minus_control_chi2": float(pressure[model]["chi2_total"]) - float(control[model]["chi2_total"]),
                "control_AIC": float(control[model]["AIC"]),
                "pressure_AIC": float(pressure[model]["AIC"]),
                "pressure_minus_control_AIC": float(pressure[model]["AIC"]) - float(control[model]["AIC"]),
                "control_BIC": float(control[model]["BIC"]),
                "pressure_BIC": float(pressure[model]["BIC"]),
                "pressure_minus_control_BIC": float(pressure[model]["BIC"]) - float(control[model]["BIC"]),
                "control_edge_flag": control[model]["prior_edge_flag"],
                "pressure_edge_flag": pressure[model]["prior_edge_flag"],
            }
        )
    return rows


def fixed_relative_rows(control_run: Path, pressure_run: Path) -> list[dict[str, Any]]:
    control_lookup = comparison_lookup(control_run)
    pressure_lookup = comparison_lookup(pressure_run)
    rows: list[dict[str, Any]] = []
    for reference in BASELINES:
        control = control_lookup[(PRIMARY, reference)]
        pressure = pressure_lookup[(PRIMARY, reference)]
        control_delta_chi2 = float(control["delta_chi2"])
        control_delta_aic = float(control["delta_AIC"])
        control_delta_bic = float(control["delta_BIC"])
        pressure_delta_chi2 = float(pressure["delta_chi2"])
        pressure_delta_aic = float(pressure["delta_AIC"])
        pressure_delta_bic = float(pressure["delta_BIC"])
        max_abs_shift = max(
            abs(pressure_delta_chi2 - control_delta_chi2),
            abs(pressure_delta_aic - control_delta_aic),
            abs(pressure_delta_bic - control_delta_bic),
        )
        verdict = "pressure_pattern_unchanged" if max_abs_shift < 0.05 else "pressure_changes_relative_round"
        rows.append(
            {
                "reference": reference,
                "control_delta_chi2": control_delta_chi2,
                "control_delta_AIC": control_delta_aic,
                "control_delta_BIC": control_delta_bic,
                "pressure_delta_chi2": pressure_delta_chi2,
                "pressure_delta_AIC": pressure_delta_aic,
                "pressure_delta_BIC": pressure_delta_bic,
                "max_abs_relative_shift": max_abs_shift,
                "verdict": verdict,
            }
        )
    return rows


def edge_comparison_rows(control_run: Path, pressure_run: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch, run_dir in [("matched_no_SH0ES_control", control_run), ("SH0ES_pressure", pressure_run)]:
        branch_edges = edge_flags(run_dir)
        if not branch_edges:
            rows.append(
                {
                    "branch": branch,
                    "model": "",
                    "parameter": "",
                    "best_fit": "",
                    "edge_status": "no_edge_flags",
                    "interpretation": "clean branch",
                }
            )
            continue
        for row in branch_edges:
            rows.append(
                {
                    "branch": branch,
                    "model": row["model"],
                    "parameter": row["parameter"],
                    "best_fit": row["best_fit"],
                    "edge_status": "edge_flag",
                    "interpretation": "baseline/ablation instability blocks stable evidence",
                }
            )
    return rows


def ablation_vs_fixed_rows(pressure_run: Path) -> list[dict[str, Any]]:
    fits = fit_by_model(pressure_run)
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


def amplitude_rows(control_run: Path, pressure_run: Path) -> list[dict[str, Any]]:
    def lookup(run_dir: Path) -> dict[tuple[str, str], dict[str, str]]:
        return {
            (row["model"], row["parameter"]): row
            for row in read_csv(run_dir / "results" / "prior_edge_table.csv")
        }

    control = lookup(control_run)
    pressure = lookup(pressure_run)
    rows: list[dict[str, Any]] = []
    for model in [PRIMARY, *ABLATIONS]:
        control_b = float(control[(model, "B_mem")]["best_fit"])
        pressure_b = float(pressure[(model, "B_mem")]["best_fit"])
        rows.append(
            {
                "model": model,
                "control_B_mem": control_b,
                "pressure_B_mem": pressure_b,
                "pressure_minus_control": pressure_b - control_b,
                "relative_shift": (pressure_b - control_b) / control_b if control_b else float("nan"),
                "pressure_edge_flag": pressure[(model, "B_mem")]["edge_flag"],
            }
        )
    return rows


def gate_rows(
    control_status: dict[str, Any],
    pressure_status: dict[str, Any],
    control_config: dict[str, Any],
    pressure_config: dict[str, Any],
    fixed_rows: list[dict[str, Any]],
    edge_rows_data: list[dict[str, Any]],
    ablation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pressure_edges = [row for row in edge_rows_data if row["branch"] == "SH0ES_pressure" and row["edge_status"] == "edge_flag"]
    pressure_mts_edges = [row for row in pressure_edges if str(row["model"]).startswith("MTS")]
    pressure_pattern_unchanged = all(row["verdict"] == "pressure_pattern_unchanged" for row in fixed_rows)
    fixed_wins_ablations = all(row["verdict"] == "fixed_branch_wins_information_criteria" for row in ablation_rows)
    return [
        {
            "gate": "matched_control_scores_written",
            "gate_pass": control_status.get("scores_written") is True,
            "notes": control_status.get("readout", ""),
        },
        {
            "gate": "pressure_scores_written",
            "gate_pass": pressure_status.get("scores_written") is True,
            "notes": pressure_status.get("readout", ""),
        },
        {
            "gate": "matched_branch_pair_confirmed",
            "gate_pass": control_config.get("sn_observable") == "mb-corr"
            and pressure_config.get("sn_observable") == "mu-sh0es"
            and control_config.get("sn_covariance_mode") == pressure_config.get("sn_covariance_mode") == "diagonal"
            and control_config.get("sn_max_rows") == pressure_config.get("sn_max_rows") == 250
            and control_config.get("include_mts_ablations") is True
            and pressure_config.get("include_mts_ablations") is True,
            "notes": "same rows/covariance/BAO/ablations; observable changed only",
        },
        {
            "gate": "pressure_edge_flags_are_baseline_only",
            "gate_pass": bool(pressure_edges) and not pressure_mts_edges,
            "notes": ";".join(f"{row['model']}:{row['parameter']}" for row in pressure_edges),
        },
        {
            "gate": "relative_scorecard_not_changed_by_SH0ES_observable",
            "gate_pass": pressure_pattern_unchanged,
            "notes": "fixed MTS deltas versus LCDM/wCDM/CPL are nearly unchanged",
        },
        {
            "gate": "fixed_branch_still_beats_ablations_by_IC",
            "gate_pass": fixed_wins_ablations,
            "notes": "fitted p/u3 do not displace fixed branch on AIC/BIC",
        },
        {
            "gate": "stress_branch_not_evidence",
            "gate_pass": pressure_status.get("stable_evidence_allowed") is False,
            "notes": "SH0ES-pressure branch remains stress-only",
        },
    ]


def decision_rows(gates: list[dict[str, Any]], edge_rows_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures = [row["gate"] for row in gates if not row["gate_pass"]]
    pressure_edges = [
        f"{row['model']}:{row['parameter']}"
        for row in edge_rows_data
        if row["branch"] == "SH0ES_pressure" and row["edge_status"] == "edge_flag"
    ]
    if failures:
        verdict = "T5_pressure_branch_unclean"
    else:
        verdict = "T5_SH0ES_pressure_neutral_stress_only"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(failures)},
        {"decision": "pressure_edge_flags", "value": ";".join(pressure_edges)},
        {"decision": "boxing_card", "value": "SH0ES pressure changes the lighting, not the fight; no standalone support"},
        {"decision": "claim_ceiling", "value": "stress_test_only_no_stable_evidence"},
        {"decision": "next_target", "value": "T6_BAO_release_sensitivity"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-run-dir", type=Path, default=None)
    parser.add_argument("--pressure-run-dir", type=Path, default=None)
    args = parser.parse_args()

    control_run = args.control_run_dir or latest_run("mb-corr")
    pressure_run = args.pressure_run_dir or latest_run("mu-sh0es")
    control_status = read_json(control_run / "status.json")
    pressure_status = read_json(pressure_run / "status.json")
    control_config = read_json(control_run / "run_config.json")
    pressure_config = read_json(pressure_run / "run_config.json")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T5-SH0ES-pressure-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    shifts = pressure_model_shift_rows(control_run, pressure_run)
    fixed_rows = fixed_relative_rows(control_run, pressure_run)
    edge_rows_data = edge_comparison_rows(control_run, pressure_run)
    ablation_rows = ablation_vs_fixed_rows(pressure_run)
    amplitudes = amplitude_rows(control_run, pressure_run)
    gates = gate_rows(control_status, pressure_status, control_config, pressure_config, fixed_rows, edge_rows_data, ablation_rows)
    decisions = decision_rows(gates, edge_rows_data)

    write_csv(
        results_dir / "pressure_model_shift.csv",
        shifts,
        [
            "model",
            "control_chi2",
            "pressure_chi2",
            "pressure_minus_control_chi2",
            "control_AIC",
            "pressure_AIC",
            "pressure_minus_control_AIC",
            "control_BIC",
            "pressure_BIC",
            "pressure_minus_control_BIC",
            "control_edge_flag",
            "pressure_edge_flag",
        ],
    )
    write_csv(
        results_dir / "fixed_relative_pattern.csv",
        fixed_rows,
        [
            "reference",
            "control_delta_chi2",
            "control_delta_AIC",
            "control_delta_BIC",
            "pressure_delta_chi2",
            "pressure_delta_AIC",
            "pressure_delta_BIC",
            "max_abs_relative_shift",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "edge_flag_comparison.csv",
        edge_rows_data,
        ["branch", "model", "parameter", "best_fit", "edge_status", "interpretation"],
    )
    write_csv(
        results_dir / "ablation_vs_fixed_pressure.csv",
        ablation_rows,
        ["ablation", "delta_chi2_vs_fixed", "delta_AIC_vs_fixed", "delta_BIC_vs_fixed", "verdict"],
    )
    write_csv(
        results_dir / "amplitude_pressure_shift.csv",
        amplitudes,
        ["model", "control_B_mem", "pressure_B_mem", "pressure_minus_control", "relative_shift", "pressure_edge_flag"],
    )
    write_csv(results_dir / "scorecard_gates.csv", gates, ["gate", "gate_pass", "notes"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "control_run_dir": str(control_run),
        "pressure_run_dir": str(pressure_run),
        "readout": next(row["value"] for row in decisions if row["decision"] == "verdict"),
        "claim_ceiling": "stress_test_only_no_stable_evidence",
        "stable_evidence_allowed": False,
        "next_action": next(row["value"] for row in decisions if row["decision"] == "next_target"),
    }
    (run_dir / "status.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
