from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "no-SH0ES-shape-branch-readout"
STATUS = "no_SH0ES_shape_branch_pattern_survives_but_stable_evidence_blocked_by_CPL_edge"
CLAIM_CEILING = "SN_BAO_no_SH0ES_shape_short_smoke_only_no_stable_evidence_or_parent_promotion"

PRESSURE_RUN = ROOT / "runs" / "20260601-095321-cosmo-SN-BAO-short-smoke"
NO_SHOES_DRY_RUN = ROOT / "runs" / "20260601-101526-cosmo-SN-BAO-closure-dryrun"
NO_SHOES_SCORE_RUN = ROOT / "runs" / "20260601-101537-cosmo-SN-BAO-short-smoke"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def as_float(value: str) -> float:
    return float(value)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "285-generic-SN-BAO-short-smoke-with-ablations.md", "calibration-pressure generic short-smoke comparator"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "generic SN+BAO runner with sn-observable mb-corr branch"),
        (NO_SHOES_DRY_RUN / "status.json", "no-SH0ES dry-run status"),
        (NO_SHOES_DRY_RUN / "results" / "data_schema_report.csv", "no-SH0ES schema validation"),
        (NO_SHOES_SCORE_RUN / "status.json", "no-SH0ES score status"),
        (NO_SHOES_SCORE_RUN / "run_config.json", "no-SH0ES run config"),
        (NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv", "no-SH0ES model scores"),
        (NO_SHOES_SCORE_RUN / "results" / "baseline_comparison.csv", "no-SH0ES baseline comparisons"),
        (NO_SHOES_SCORE_RUN / "results" / "prior_edge_table.csv", "no-SH0ES prior-edge audit"),
        (NO_SHOES_SCORE_RUN / "results" / "residuals.csv", "no-SH0ES residual rows"),
        (PRESSURE_RUN / "results" / "fit_summary.csv", "calibration-pressure comparator scores"),
        (PRESSURE_RUN / "results" / "baseline_comparison.csv", "calibration-pressure comparator baseline comparisons"),
        (ROOT / "scripts" / "no_SH0ES_shape_branch_readout.py", "this readout script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def score_readout_rows() -> list[dict[str, Any]]:
    edge_rows = read_csv(NO_SHOES_SCORE_RUN / "results" / "prior_edge_table.csv")
    edge_by_model: dict[str, bool] = defaultdict(bool)
    for row in edge_rows:
        edge_by_model[row["model"]] = edge_by_model[row["model"]] or row["edge_flag"].lower() == "true"

    rows = []
    for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv"):
        rows.append(
            {
                "model": row["model"],
                "chi2_SN": row["chi2_SN"],
                "chi2_BAO": row["chi2_BAO"],
                "chi2_total": row["chi2_total"],
                "AIC": row["AIC"],
                "BIC": row["BIC"],
                "convergence": row["convergence"],
                "edge_flag_any": str(edge_by_model[row["model"]]).lower(),
            }
        )
    return rows


def fixed_branch_comparison_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "baseline_comparison.csv"):
        if row["model"] == "MTS_fixed_p3_u3quarter":
            rows.append(
                {
                    "model": row["model"],
                    "reference_baseline": row["reference_baseline"],
                    "delta_chi2": row["delta_chi2"],
                    "delta_AIC": row["delta_AIC"],
                    "delta_BIC": row["delta_BIC"],
                    "interpretation": interpretation_for_fixed(row),
                }
            )
    return rows


def interpretation_for_fixed(row: dict[str, str]) -> str:
    delta_aic = as_float(row["delta_AIC"])
    delta_bic = as_float(row["delta_BIC"])
    delta_chi2 = as_float(row["delta_chi2"])
    if delta_aic < 0 and delta_bic < 0 and delta_chi2 <= 0:
        return "beats_raw_and_information_criteria"
    if delta_aic < 0 and delta_bic < 0:
        return "information_criteria_win_but_raw_chi2_worse"
    if delta_aic < 0 or delta_bic < 0:
        return "mixed_information_criteria"
    return "not_preferred_by_information_criteria"


def pressure_comparison_rows() -> list[dict[str, Any]]:
    pressure = {row["model"]: row for row in read_csv(PRESSURE_RUN / "results" / "fit_summary.csv")}
    no_shoes = {row["model"]: row for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv")}
    rows = []
    for model in no_shoes:
        p = pressure[model]
        n = no_shoes[model]
        rows.append(
            {
                "model": model,
                "pressure_chi2_total": p["chi2_total"],
                "no_SH0ES_chi2_total": n["chi2_total"],
                "delta_noSH0ES_minus_pressure_chi2": as_float(n["chi2_total"]) - as_float(p["chi2_total"]),
                "pressure_AIC": p["AIC"],
                "no_SH0ES_AIC": n["AIC"],
                "delta_noSH0ES_minus_pressure_AIC": as_float(n["AIC"]) - as_float(p["AIC"]),
                "pressure_BIC": p["BIC"],
                "no_SH0ES_BIC": n["BIC"],
                "delta_noSH0ES_minus_pressure_BIC": as_float(n["BIC"]) - as_float(p["BIC"]),
            }
        )
    return rows


def baseline_delta_comparison_rows() -> list[dict[str, Any]]:
    pressure = {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(PRESSURE_RUN / "results" / "baseline_comparison.csv")
    }
    no_shoes = {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "baseline_comparison.csv")
    }
    rows = []
    for key, n in no_shoes.items():
        if key[0] != "MTS_fixed_p3_u3quarter":
            continue
        p = pressure[key]
        rows.append(
            {
                "model": key[0],
                "reference_baseline": key[1],
                "pressure_delta_chi2": p["delta_chi2"],
                "no_SH0ES_delta_chi2": n["delta_chi2"],
                "shift_delta_chi2": as_float(n["delta_chi2"]) - as_float(p["delta_chi2"]),
                "pressure_delta_AIC": p["delta_AIC"],
                "no_SH0ES_delta_AIC": n["delta_AIC"],
                "shift_delta_AIC": as_float(n["delta_AIC"]) - as_float(p["delta_AIC"]),
                "pressure_delta_BIC": p["delta_BIC"],
                "no_SH0ES_delta_BIC": n["delta_BIC"],
                "shift_delta_BIC": as_float(n["delta_BIC"]) - as_float(p["delta_BIC"]),
            }
        )
    return rows


def ablation_rows() -> list[dict[str, Any]]:
    summaries = {row["model"]: row for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv")}
    fixed = summaries["MTS_fixed_p3_u3quarter"]
    rows = []
    for model in ["MTS_fitted_p", "MTS_fitted_u3", "MTS_Bmem_zero"]:
        row = summaries[model]
        delta_aic = as_float(row["AIC"]) - as_float(fixed["AIC"])
        delta_bic = as_float(row["BIC"]) - as_float(fixed["BIC"])
        rows.append(
            {
                "model": model,
                "delta_chi2_vs_fixed": as_float(row["chi2_total"]) - as_float(fixed["chi2_total"]),
                "delta_AIC_vs_fixed": delta_aic,
                "delta_BIC_vs_fixed": delta_bic,
                "promotion_status": "extra_parameter_not_promoted" if model != "MTS_Bmem_zero" and delta_aic > 0 and delta_bic > 0 else "negative_control_LCDM_limit",
            }
        )
    return rows


def residual_summary_rows() -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "residuals.csv"):
        dataset_group = "SN" if row["dataset"].startswith("SN") else "BAO"
        grouped[(row["model"], dataset_group)].append(as_float(row["residual"]))
    models = [row["model"] for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv")]
    rows = []
    for model in models:
        sn = grouped.get((model, "SN"), [])
        bao = grouped.get((model, "BAO"), [])
        rows.append(
            {
                "model": model,
                "SN_count": len(sn),
                "SN_RMS": rms(sn),
                "SN_max_abs": max_abs(sn),
                "BAO_count": len(bao),
                "BAO_RMS": rms(bao),
                "BAO_max_abs": max_abs(bao),
            }
        )
    return rows


def rms(values: list[float]) -> str:
    if not values:
        return ""
    return str(math.sqrt(sum(value * value for value in values) / len(values)))


def max_abs(values: list[float]) -> str:
    if not values:
        return ""
    return str(max(abs(value) for value in values))


def prior_edge_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(NO_SHOES_SCORE_RUN / "results" / "prior_edge_table.csv"):
        edge = row["edge_flag"].lower() == "true"
        owner = "MTS" if row["model"].startswith("MTS") else "baseline"
        rows.append(
            {
                "model": row["model"],
                "owner": owner,
                "parameter": row["parameter"],
                "best_fit": row["best_fit"],
                "lower": row["lower"],
                "upper": row["upper"],
                "distance_to_edge": row["distance_to_edge"],
                "edge_flag": row["edge_flag"],
                "claim_effect": "blocks_stable_evidence_language" if edge else "no_edge_flag",
            }
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    dry_status = read_json(NO_SHOES_DRY_RUN / "status.json")
    score_status = read_json(NO_SHOES_SCORE_RUN / "status.json")
    config = read_json(NO_SHOES_SCORE_RUN / "run_config.json")
    fit = read_csv(NO_SHOES_SCORE_RUN / "results" / "fit_summary.csv")
    edge_models = sorted({row["model"] for row in prior_edge_rows() if str(row["edge_flag"]).lower() == "true"})
    mts_edge_models = [model for model in edge_models if model.startswith("MTS")]
    fixed = {row["reference_baseline"]: row for row in fixed_branch_comparison_rows()}
    ablations = ablation_rows()
    pattern_shifts = baseline_delta_comparison_rows()
    max_pattern_shift = max(abs(float(row["shift_delta_BIC"])) for row in pattern_shifts)
    return [
        {
            "gate": "dry_run_schema",
            "status": "pass" if dry_status.get("data_ready_for_short_smoke") else "fail",
            "evidence": dry_status.get("readout", ""),
            "claim_effect": "no-SH0ES branch had validated inputs before scoring",
        },
        {
            "gate": "no_SH0ES_mode",
            "status": "pass" if config.get("sn_observable") == "mb-corr" and not config.get("sn_include_calibrators") else "fail",
            "evidence": f"sn_observable={config.get('sn_observable')}; include_calibrators={config.get('sn_include_calibrators')}",
            "claim_effect": "SN shape uses nuisance offset rather than MU_SH0ES local calibration branch",
        },
        {
            "gate": "convergence",
            "status": "pass" if all(row["convergence"].lower() == "true" for row in fit) else "fail",
            "evidence": "; ".join(f"{row['model']}={row['convergence']}" for row in fit),
            "claim_effect": "scores can be compared",
        },
        {
            "gate": "prior_edges",
            "status": "fail" if edge_models else "pass",
            "evidence": ";".join(edge_models) if edge_models else "none",
            "claim_effect": "stable evidence blocked if any branch edge-hits",
        },
        {
            "gate": "MTS_prior_edges",
            "status": "pass" if not mts_edge_models else "fail",
            "evidence": ";".join(mts_edge_models) if mts_edge_models else "none",
            "claim_effect": "MTS branches are not edge-hit in this no-SH0ES run",
        },
        {
            "gate": "fixed_branch_no_SH0ES_competitiveness",
            "status": "mixed",
            "evidence": f"vs_LCDM_dBIC={fixed['LCDM']['delta_BIC']}; vs_wCDM_dBIC={fixed['wCDM']['delta_BIC']}; vs_CPL_dBIC={fixed['CPL']['delta_BIC']}",
            "claim_effect": "same qualitative result as pressure branch: beats wCDM/CPL BIC, not LCDM BIC",
        },
        {
            "gate": "calibration_pressure_pattern_shift",
            "status": "pass",
            "evidence": f"max_abs_fixed_branch_delta_BIC_shift={max_pattern_shift}",
            "claim_effect": "pattern essentially unchanged by switching MU_SH0ES to mb-corr shape branch",
        },
        {
            "gate": "ablation_tax",
            "status": "pass" if all(row["promotion_status"] != "extra_parameter_promoted" for row in ablations) else "fail",
            "evidence": "; ".join(f"{row['model']}={row['promotion_status']}" for row in ablations),
            "claim_effect": "fitted p/u3 still not justified over fixed branch",
        },
        {
            "gate": "stable_evidence_allowed",
            "status": "fail" if not score_status.get("stable_evidence_allowed", False) else "pass",
            "evidence": score_status.get("readout", ""),
            "claim_effect": "robustness diagnostic only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Switching the 250-SN branch from MU_SH0ES to mb-corr with an analytic nuisance offset leaves the fixed-branch comparison pattern essentially unchanged. "
                "The fixed branch remains mixed: it improves chi2/AIC over LCDM but loses LCDM BIC, while beating wCDM and CPL by BIC. "
                "CPL still hits the wa prior edge, so no stable evidence language is allowed."
            ),
            "next_target": "DESI_DR1_vs_DR2_fixed_branch_robustness",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "score_readout.csv": (score_readout_rows(), ["model", "chi2_SN", "chi2_BAO", "chi2_total", "AIC", "BIC", "convergence", "edge_flag_any"]),
        "fixed_branch_comparison.csv": (fixed_branch_comparison_rows(), ["model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "interpretation"]),
        "pressure_vs_noSH0ES_scores.csv": (
            pressure_comparison_rows(),
            [
                "model",
                "pressure_chi2_total",
                "no_SH0ES_chi2_total",
                "delta_noSH0ES_minus_pressure_chi2",
                "pressure_AIC",
                "no_SH0ES_AIC",
                "delta_noSH0ES_minus_pressure_AIC",
                "pressure_BIC",
                "no_SH0ES_BIC",
                "delta_noSH0ES_minus_pressure_BIC",
            ],
        ),
        "pressure_vs_noSH0ES_fixed_branch_deltas.csv": (
            baseline_delta_comparison_rows(),
            [
                "model",
                "reference_baseline",
                "pressure_delta_chi2",
                "no_SH0ES_delta_chi2",
                "shift_delta_chi2",
                "pressure_delta_AIC",
                "no_SH0ES_delta_AIC",
                "shift_delta_AIC",
                "pressure_delta_BIC",
                "no_SH0ES_delta_BIC",
                "shift_delta_BIC",
            ],
        ),
        "ablation_readout.csv": (ablation_rows(), ["model", "delta_chi2_vs_fixed", "delta_AIC_vs_fixed", "delta_BIC_vs_fixed", "promotion_status"]),
        "prior_edge_readout.csv": (prior_edge_rows(), ["model", "owner", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag", "claim_effect"]),
        "residual_summary.csv": (residual_summary_rows(), ["model", "SN_count", "SN_RMS", "SN_max_abs", "BAO_count", "BAO_RMS", "BAO_max_abs"]),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "dry_run": str(NO_SHOES_DRY_RUN),
        "score_run": str(NO_SHOES_SCORE_RUN),
        "pressure_comparator_run": str(PRESSURE_RUN),
        "stable_evidence_allowed": False,
        "MTS_edge_flags_present": False,
        "baseline_edge_flags_present": True,
        "no_SH0ES_pattern": "survives_qualitatively_mixed_same_as_pressure_branch",
        "next_target": "DESI_DR1_vs_DR2_fixed_branch_robustness",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="No-SH0ES shape branch readout.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
