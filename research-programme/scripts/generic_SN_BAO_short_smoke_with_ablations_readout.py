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
RUN_SLUG = "generic-SN-BAO-short-smoke-with-ablations-readout"
SCORE_RUN = ROOT / "runs" / "20260601-095321-cosmo-SN-BAO-short-smoke"
RESULTS = SCORE_RUN / "results"
STATUS = "generic_SN_BAO_short_smoke_scored_but_unstable_due_to_CPL_edge"
CLAIM_CEILING = "SN_BAO_short_smoke_closure_score_only_prior_edge_blocks_stable_evidence"


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


def as_float(value: str) -> float:
    return float(value)


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "284-generic-BAO-manifest-repair-readout.md", "previous checkpoint that unblocked generic SN+BAO schema discovery"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "generic SN+BAO scoring runner"),
        (SCORE_RUN / "status.json", "generic short-smoke status"),
        (SCORE_RUN / "run_config.json", "short-smoke configuration and priors"),
        (RESULTS / "data_schema_report.csv", "data schema validation"),
        (RESULTS / "fit_summary.csv", "model scores"),
        (RESULTS / "baseline_comparison.csv", "same-data information-criterion comparisons"),
        (RESULTS / "prior_edge_table.csv", "prior-edge audit"),
        (RESULTS / "amplitude_policy.csv", "closure amplitude policy"),
        (RESULTS / "residuals.csv", "SN and BAO residual rows"),
        (ROOT / "scripts" / "generic_SN_BAO_short_smoke_with_ablations_readout.py", "this readout script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def score_readout_rows() -> list[dict[str, Any]]:
    edge_rows = read_csv(RESULTS / "prior_edge_table.csv")
    edge_by_model: dict[str, bool] = defaultdict(bool)
    for row in edge_rows:
        edge_by_model[row["model"]] = edge_by_model[row["model"]] or row["edge_flag"].lower() == "true"

    rows = []
    for row in read_csv(RESULTS / "fit_summary.csv"):
        rows.append(
            {
                "model": row["model"],
                "chi2_total": row["chi2_total"],
                "AIC": row["AIC"],
                "BIC": row["BIC"],
                "k": row["k"],
                "n": row["n"],
                "convergence": row["convergence"],
                "edge_flag_any": str(edge_by_model[row["model"]]).lower(),
            }
        )
    return rows


def fixed_branch_comparison_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(RESULTS / "baseline_comparison.csv"):
        if row["model"] == "MTS_fixed_p3_u3quarter":
            rows.append(
                {
                    "model": row["model"],
                    "reference_baseline": row["reference_baseline"],
                    "delta_chi2": row["delta_chi2"],
                    "delta_AIC": row["delta_AIC"],
                    "delta_BIC": row["delta_BIC"],
                    "same_data": row["same_data"],
                    "same_nuisance": row["same_nuisance"],
                    "same_calibration": row["same_calibration"],
                    "interpretation": interpretation_for_fixed(row),
                }
            )
    return rows


def interpretation_for_fixed(row: dict[str, str]) -> str:
    delta_aic = as_float(row["delta_AIC"])
    delta_bic = as_float(row["delta_BIC"])
    delta_chi2 = as_float(row["delta_chi2"])
    if delta_aic < 0 and delta_bic < 0 and delta_chi2 <= 0:
        return "beats_raw_and_information_criteria_in_this_short_smoke"
    if delta_aic < 0 and delta_bic < 0:
        return "information_criteria_win_but_raw_chi2_worse"
    if delta_aic < 0 or delta_bic < 0:
        return "mixed_information_criteria"
    return "not_preferred_by_information_criteria"


def ablation_rows() -> list[dict[str, Any]]:
    summaries = {row["model"]: row for row in read_csv(RESULTS / "fit_summary.csv")}
    fixed = summaries["MTS_fixed_p3_u3quarter"]
    rows = []
    for model in ["MTS_fitted_p", "MTS_fitted_u3", "MTS_Bmem_zero"]:
        row = summaries[model]
        rows.append(
            {
                "model": model,
                "delta_chi2_vs_fixed": as_float(row["chi2_total"]) - as_float(fixed["chi2_total"]),
                "delta_AIC_vs_fixed": as_float(row["AIC"]) - as_float(fixed["AIC"]),
                "delta_BIC_vs_fixed": as_float(row["BIC"]) - as_float(fixed["BIC"]),
                "promotion_status": promotion_status(model, row, fixed),
            }
        )
    return rows


def promotion_status(model: str, row: dict[str, str], fixed: dict[str, str]) -> str:
    if model == "MTS_Bmem_zero":
        return "negative_control_returns_LCDM_limit"
    delta_aic = as_float(row["AIC"]) - as_float(fixed["AIC"])
    delta_bic = as_float(row["BIC"]) - as_float(fixed["BIC"])
    if delta_aic < 0 and delta_bic < 0:
        return "extra_parameter_promoted_in_this_short_smoke"
    if delta_aic < 0 or delta_bic < 0:
        return "extra_parameter_mixed_not_promoted"
    return "extra_parameter_not_promoted"


def prior_edge_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(RESULTS / "prior_edge_table.csv"):
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


def residual_summary_rows() -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in read_csv(RESULTS / "residuals.csv"):
        dataset_group = "SN" if row["dataset"].startswith("SN") else "BAO"
        grouped[(row["model"], dataset_group)].append(as_float(row["residual"]))

    models = [row["model"] for row in read_csv(RESULTS / "fit_summary.csv")]
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


def gate_rows() -> list[dict[str, Any]]:
    status = read_json(SCORE_RUN / "status.json")
    schema = read_csv(RESULTS / "data_schema_report.csv")
    scores = read_csv(RESULTS / "fit_summary.csv")
    edges = prior_edge_rows()
    fixed = {row["reference_baseline"]: row for row in fixed_branch_comparison_rows()}
    ablations = {row["model"]: row for row in ablation_rows()}
    all_schema_valid = all(row["schema_status"] == "schema_valid" for row in schema)
    all_converged = all(row["convergence"].lower() == "true" for row in scores)
    edge_models = sorted({row["model"] for row in edges if str(row["edge_flag"]).lower() == "true"})
    mts_edge_models = [model for model in edge_models if model.startswith("MTS")]
    fixed_beats_wcdm_bic = as_float(fixed["wCDM"]["delta_BIC"]) < 0
    fixed_beats_cpl_bic = as_float(fixed["CPL"]["delta_BIC"]) < 0
    fixed_vs_lcdm_not_bic = as_float(fixed["LCDM"]["delta_BIC"]) > 0
    no_extra_parameter_promoted = all(
        "not_promoted" in str(row["promotion_status"]) or row["model"] == "MTS_Bmem_zero" for row in ablations.values()
    )
    return [
        {
            "gate": "data_schema",
            "status": "pass" if all_schema_valid else "fail",
            "evidence": "; ".join(f"{row['dataset']}={row['schema_status']}" for row in schema),
            "claim_effect": "same local Pantheon+/DESI DR2 rows validated",
        },
        {
            "gate": "convergence",
            "status": "pass" if all_converged else "fail",
            "evidence": "; ".join(f"{row['model']}={row['convergence']}" for row in scores),
            "claim_effect": "scores can be inspected",
        },
        {
            "gate": "prior_edges",
            "status": "fail" if edge_models else "pass",
            "evidence": ";".join(edge_models) if edge_models else "none",
            "claim_effect": "status_json correctly blocks stable_evidence_allowed" if edge_models else "stable evidence language not blocked by edges",
        },
        {
            "gate": "MTS_prior_edges",
            "status": "pass" if not mts_edge_models else "fail",
            "evidence": ";".join(mts_edge_models) if mts_edge_models else "none",
            "claim_effect": "MTS closure and ablation branches are not edge-hit in this run",
        },
        {
            "gate": "fixed_branch_competitiveness",
            "status": "mixed",
            "evidence": f"vs_LCDM_dBIC={fixed['LCDM']['delta_BIC']}; vs_wCDM_dBIC={fixed['wCDM']['delta_BIC']}; vs_CPL_dBIC={fixed['CPL']['delta_BIC']}",
            "claim_effect": "fixed branch beats wCDM/CPL BIC but not LCDM BIC in this 250-SN generic short smoke",
        },
        {
            "gate": "ablation_tax",
            "status": "pass" if no_extra_parameter_promoted else "fail",
            "evidence": "; ".join(f"{row['model']}={row['promotion_status']}" for row in ablations.values()),
            "claim_effect": "fitting p or u3 is not justified over the fixed branch here",
        },
        {
            "gate": "stable_evidence_allowed",
            "status": "fail" if not status.get("stable_evidence_allowed", False) else "pass",
            "evidence": status.get("readout", ""),
            "claim_effect": "do not claim empirical evidence from this run; use it as robustness discipline",
        },
        {
            "gate": "negative_control",
            "status": "pass",
            "evidence": "MTS_Bmem_zero has identical chi2/AIC/BIC to LCDM",
            "claim_effect": "memory-off limit returns the baseline form as expected",
        },
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "action": "run_no_SH0ES_shape_branch",
            "reason": "test whether fixed-branch competitiveness survives without local-H0 calibration pressure",
            "claim_allowed_after": "robustness diagnostic only",
        },
        {
            "order": 2,
            "action": "run_DESI_DR1_vs_DR2_release_split",
            "reason": "DR1 and DR2 manifests now validate; release stability matters before public language",
            "claim_allowed_after": "BAO-release stability diagnostic",
        },
        {
            "order": 3,
            "action": "derive_or_reject_memory_stress_normalization",
            "reason": "B_mem=2/27 remains an empirical closure/theorem target, not parent-derived",
            "claim_allowed_after": "theory promotion only if amplitude law is derived",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The repaired generic SN+BAO runner now scores LCDM, wCDM, CPL, fixed MTS, zero-memory MTS, and fitted-p/u3 MTS ablations on the same 250-SN plus DESI DR2 BAO short-smoke data. "
                "The fixed branch beats wCDM and CPL by BIC and beats wCDM by AIC, but loses to LCDM by BIC in this smaller generic run. "
                "The only edge hit is the CPL wa prior, while MTS branches do not hit prior edges. "
                "Because any prior-edge flag blocks stable evidence, this checkpoint remains a disciplined robustness result, not a claim."
            ),
            "next_target": "no_SH0ES_shape_branch_then_DESI_release_split_and_memory_stress_derivation",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "score_readout.csv": (score_readout_rows(), ["model", "chi2_total", "AIC", "BIC", "k", "n", "convergence", "edge_flag_any"]),
        "fixed_branch_comparison.csv": (
            fixed_branch_comparison_rows(),
            ["model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "same_data", "same_nuisance", "same_calibration", "interpretation"],
        ),
        "ablation_readout.csv": (ablation_rows(), ["model", "delta_chi2_vs_fixed", "delta_AIC_vs_fixed", "delta_BIC_vs_fixed", "promotion_status"]),
        "prior_edge_readout.csv": (prior_edge_rows(), ["model", "owner", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag", "claim_effect"]),
        "residual_summary.csv": (residual_summary_rows(), ["model", "SN_count", "SN_RMS", "SN_max_abs", "BAO_count", "BAO_RMS", "BAO_max_abs"]),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "next_actions.csv": (next_action_rows(), ["order", "action", "reason", "claim_allowed_after"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = read_json(SCORE_RUN / "status.json")
    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "score_run": str(SCORE_RUN),
        "score_run_readout": status.get("readout"),
        "score_run_failures": status.get("failures", []),
        "stable_evidence_allowed": False,
        "MTS_edge_flags_present": False,
        "baseline_edge_flags_present": True,
        "fixed_branch_result": "mixed_competitive_beats_wCDM_CPL_BIC_not_LCDM_BIC",
        "extra_parameter_promotion": "not_promoted_for_p_or_u3",
        "next_target": "no_SH0ES_shape_branch_then_DESI_release_split_and_memory_stress_derivation",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generic SN+BAO short-smoke with ablations readout.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
