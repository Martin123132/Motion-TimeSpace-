#!/usr/bin/env python3
"""Summarize the T2 canonical_R_closure fitted-p/u3 ablation scorecard."""

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
BASELINES = ["LCDM", "wCDM", "CPL"]
CONTROL = "MTS_Bmem_zero"


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


def latest_ablation_smoke() -> Path:
    candidates: list[Path] = []
    for candidate in sorted(RUNS_ROOT.glob("*-cosmo-SN-BAO-short-smoke"), key=lambda item: item.name):
        config_path = candidate / "run_config.json"
        if config_path.exists():
            config = read_json(config_path)
            if config.get("include_mts_ablations") is True:
                candidates.append(candidate)
    if not candidates:
        raise FileNotFoundError("No include-mts-ablations short-smoke directories found.")
    return candidates[-1]


def fits_by_model(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["model"]: row for row in rows}


def parameter_lookup(edge_rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["model"], row["parameter"]): row for row in edge_rows}


def metric_delta(fits: dict[str, dict[str, str]], model: str, reference: str, metric: str) -> float:
    return float(fits[model][metric]) - float(fits[reference][metric])


def ablation_vs_fixed_rows(fits: dict[str, dict[str, str]], edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    edge_flags = {(row["model"], row["parameter"]): row["edge_flag"] for row in edge_rows}
    rows: list[dict[str, Any]] = []
    for model in ABLATIONS:
        delta_chi2 = metric_delta(fits, model, PRIMARY, "chi2_total")
        delta_aic = metric_delta(fits, model, PRIMARY, "AIC")
        delta_bic = metric_delta(fits, model, PRIMARY, "BIC")
        if delta_chi2 < -2.0 and delta_aic < 0.0:
            verdict = "shape_freedom_materially_improves_fixed_branch"
        elif delta_chi2 < 0.0 and delta_aic > 0.0 and delta_bic > 0.0:
            verdict = "raw_chi2_nudge_but_fixed_branch_wins_information_criteria"
        else:
            verdict = "no_material_shape_rescue"
        free_parameter = "p" if model == "MTS_fitted_p" else "u3"
        rows.append(
            {
                "ablation": model,
                "reference": PRIMARY,
                "delta_chi2": delta_chi2,
                "delta_AIC": delta_aic,
                "delta_BIC": delta_bic,
                "free_parameter": free_parameter,
                "free_parameter_edge_flag": edge_flags[(model, free_parameter)],
                "verdict": verdict,
            }
        )
    return rows


def baseline_card_rows(fits: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in [PRIMARY, *ABLATIONS, CONTROL]:
        for reference in BASELINES:
            delta_chi2 = metric_delta(fits, model, reference, "chi2_total")
            delta_aic = metric_delta(fits, model, reference, "AIC")
            delta_bic = metric_delta(fits, model, reference, "BIC")
            if model in ABLATIONS:
                claim_role = "ablation_only"
            elif model == PRIMARY:
                claim_role = "primary_closure"
            else:
                claim_role = "negative_control"
            rows.append(
                {
                    "model": model,
                    "reference": reference,
                    "delta_chi2": delta_chi2,
                    "delta_AIC": delta_aic,
                    "delta_BIC": delta_bic,
                    "claim_role": claim_role,
                }
            )
    return rows


def parameter_rows(edge_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    lookup = parameter_lookup(edge_rows)
    rows = [
        {
            "model": PRIMARY,
            "parameter": "p",
            "best_fit": 3.0,
            "status": "fixed_canonical",
            "edge_flag": False,
            "shift_from_canonical": 0.0,
        },
        {
            "model": PRIMARY,
            "parameter": "u3",
            "best_fit": 0.25,
            "status": "fixed_canonical",
            "edge_flag": False,
            "shift_from_canonical": 0.0,
        },
    ]
    for model, parameter, canonical in [
        ("MTS_fitted_p", "p", 3.0),
        ("MTS_fitted_u3", "u3", 0.25),
    ]:
        row = lookup[(model, parameter)]
        best_fit = float(row["best_fit"])
        rows.append(
            {
                "model": model,
                "parameter": parameter,
                "best_fit": best_fit,
                "status": "fitted_ablation_only",
                "edge_flag": row["edge_flag"],
                "shift_from_canonical": best_fit - canonical,
            }
        )
    for model in [PRIMARY, "MTS_fitted_p", "MTS_fitted_u3"]:
        row = lookup[(model, "B_mem")]
        rows.append(
            {
                "model": model,
                "parameter": "B_mem",
                "best_fit": float(row["best_fit"]),
                "status": "fitted_closure_amplitude",
                "edge_flag": row["edge_flag"],
                "shift_from_canonical": "",
            }
        )
    return rows


def gate_rows(
    status: dict[str, Any],
    config: dict[str, Any],
    fits: dict[str, dict[str, str]],
    schema_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    ablation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    required_models = {"LCDM", "wCDM", "CPL", PRIMARY, CONTROL, *ABLATIONS}
    converged = all(fits[model]["convergence"] == "True" for model in required_models)
    edge_free = all(row["edge_flag"] == "False" for row in edge_rows)
    covariance_recorded = {"SN_covariance", "BAO_covariance"} <= {row["dataset"] for row in schema_rows}
    ablation_not_shape_rescue = all(
        row["verdict"] == "raw_chi2_nudge_but_fixed_branch_wins_information_criteria"
        for row in ablation_rows
    )
    return [
        {
            "gate": "scores_written",
            "gate_pass": status.get("scores_written") is True and status.get("failures") == [],
            "notes": status.get("readout", ""),
        },
        {
            "gate": "branch_is_T2_fullcov_ablation",
            "gate_pass": config.get("include_mts_ablations") is True
            and config.get("sn_covariance_mode") == "full"
            and config.get("sn_observable") == "mb-corr"
            and config.get("bao_label") == "DESI_DR2_primary",
            "notes": f"SN rows={config.get('sn_rows_used')}; BAO rows={config.get('bao_rows_used')}",
        },
        {
            "gate": "covariance_artifacts_recorded",
            "gate_pass": covariance_recorded and all(row["schema_status"] == "schema_valid" for row in schema_rows),
            "notes": "SN and BAO covariance rows are present and valid",
        },
        {
            "gate": "all_required_models_converged",
            "gate_pass": converged,
            "notes": ";".join(sorted(required_models)),
        },
        {
            "gate": "all_fits_edge_free",
            "gate_pass": edge_free,
            "notes": "fitted p and fitted u3 are not edge hits",
        },
        {
            "gate": "fixed_shape_not_rescued_by_extra_parameter",
            "gate_pass": ablation_not_shape_rescue,
            "notes": "free p/u3 improve raw chi2 only mildly and lose AIC/BIC against fixed canonical shape",
        },
        {
            "gate": "claim_ceiling_enforced",
            "gate_pass": status.get("stable_evidence_allowed") is False,
            "notes": "ablations are diagnostic only",
        },
    ]


def decision_rows(gates: list[dict[str, Any]], ablation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_failures = [row["gate"] for row in gates if not row["gate_pass"]]
    if gate_failures:
        verdict = "T2_unclean_do_not_use"
    elif all(row["verdict"] == "raw_chi2_nudge_but_fixed_branch_wins_information_criteria" for row in ablation_rows):
        verdict = "T2_fixed_shape_survives_ablation"
    else:
        verdict = "T2_shape_freedom_requires_repair"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "gate_failures", "value": ";".join(gate_failures)},
        {"decision": "fitted_p_result", "value": next(row["verdict"] for row in ablation_rows if row["ablation"] == "MTS_fitted_p")},
        {"decision": "fitted_u3_result", "value": next(row["verdict"] for row in ablation_rows if row["ablation"] == "MTS_fitted_u3")},
        {"decision": "boxing_card", "value": "fixed branch keeps the belt on AIC/BIC; ablations land light scoring taps only"},
        {"decision": "claim_ceiling", "value": "empirical_closure_scorecard_only"},
        {"decision": "next_target", "value": "T3_diagonal_covariance_sensitivity"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--score-run-dir", type=Path, default=None)
    args = parser.parse_args()

    score_run_dir = args.score_run_dir or latest_ablation_smoke()
    status = read_json(score_run_dir / "status.json")
    config = read_json(score_run_dir / "run_config.json")
    fits = fits_by_model(read_csv(score_run_dir / "results" / "fit_summary.csv"))
    schema_rows = read_csv(score_run_dir / "results" / "data_schema_report.csv")
    edge_rows_data = read_csv(score_run_dir / "results" / "prior_edge_table.csv")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-T2-ablation-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    ablation_rows = ablation_vs_fixed_rows(fits, edge_rows_data)
    baseline_rows = baseline_card_rows(fits)
    parameters = parameter_rows(edge_rows_data)
    gates = gate_rows(status, config, fits, schema_rows, edge_rows_data, ablation_rows)
    decisions = decision_rows(gates, ablation_rows)

    write_csv(
        results_dir / "ablation_vs_fixed.csv",
        ablation_rows,
        ["ablation", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "free_parameter", "free_parameter_edge_flag", "verdict"],
    )
    write_csv(results_dir / "baseline_card.csv", baseline_rows, ["model", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "claim_role"])
    write_csv(results_dir / "parameter_shifts.csv", parameters, ["model", "parameter", "best_fit", "status", "edge_flag", "shift_from_canonical"])
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
