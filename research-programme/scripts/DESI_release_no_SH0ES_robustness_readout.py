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
RUN_SLUG = "DESI-release-no-SH0ES-robustness-readout"
STATUS = "DESI_DR1_DR2_no_SH0ES_fixed_branch_survives_qualitatively_but_LCDM_BIC_gap_worsens"
CLAIM_CEILING = "DESI_release_short_smoke_robustness_only_no_stable_evidence_or_parent_promotion"

DR2_DRY_RUN = ROOT / "runs" / "20260601-101526-cosmo-SN-BAO-closure-dryrun"
DR2_SCORE_RUN = ROOT / "runs" / "20260601-101537-cosmo-SN-BAO-short-smoke"
DR1_DRY_RUN = ROOT / "runs" / "20260601-102027-cosmo-SN-BAO-closure-dryrun"
DR1_SCORE_RUN = ROOT / "runs" / "20260601-102042-cosmo-SN-BAO-short-smoke"


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
        (ROOT / "289-no-SH0ES-shape-branch-readout.md", "DR2 no-SH0ES comparator checkpoint"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "generic SN+BAO runner"),
        (DR2_DRY_RUN / "status.json", "DR2 no-SH0ES dry-run status"),
        (DR2_SCORE_RUN / "status.json", "DR2 no-SH0ES score status"),
        (DR2_SCORE_RUN / "results" / "fit_summary.csv", "DR2 no-SH0ES scores"),
        (DR2_SCORE_RUN / "results" / "baseline_comparison.csv", "DR2 no-SH0ES baseline comparisons"),
        (DR2_SCORE_RUN / "results" / "prior_edge_table.csv", "DR2 no-SH0ES prior-edge audit"),
        (DR1_DRY_RUN / "status.json", "DR1 no-SH0ES dry-run status"),
        (DR1_SCORE_RUN / "status.json", "DR1 no-SH0ES score status"),
        (DR1_SCORE_RUN / "results" / "fit_summary.csv", "DR1 no-SH0ES scores"),
        (DR1_SCORE_RUN / "results" / "baseline_comparison.csv", "DR1 no-SH0ES baseline comparisons"),
        (DR1_SCORE_RUN / "results" / "prior_edge_table.csv", "DR1 no-SH0ES prior-edge audit"),
        (ROOT / "scripts" / "DESI_release_no_SH0ES_robustness_readout.py", "this readout script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def fit_rows_for_release(label: str, run: Path) -> list[dict[str, Any]]:
    rows = []
    edge_rows = read_csv(run / "results" / "prior_edge_table.csv")
    edge_by_model: dict[str, bool] = defaultdict(bool)
    for row in edge_rows:
        edge_by_model[row["model"]] = edge_by_model[row["model"]] or row["edge_flag"].lower() == "true"
    for row in read_csv(run / "results" / "fit_summary.csv"):
        rows.append(
            {
                "release": label,
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


def score_readout_rows() -> list[dict[str, Any]]:
    return fit_rows_for_release("DESI_DR2", DR2_SCORE_RUN) + fit_rows_for_release("DESI_DR1", DR1_SCORE_RUN)


def fixed_branch_rows_for_release(label: str, run: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(run / "results" / "baseline_comparison.csv"):
        if row["model"] == "MTS_fixed_p3_u3quarter":
            rows.append(
                {
                    "release": label,
                    "reference_baseline": row["reference_baseline"],
                    "delta_chi2": row["delta_chi2"],
                    "delta_AIC": row["delta_AIC"],
                    "delta_BIC": row["delta_BIC"],
                    "interpretation": interpretation_for_fixed(row),
                }
            )
    return rows


def fixed_branch_comparison_rows() -> list[dict[str, Any]]:
    return fixed_branch_rows_for_release("DESI_DR2", DR2_SCORE_RUN) + fixed_branch_rows_for_release("DESI_DR1", DR1_SCORE_RUN)


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


def release_shift_rows() -> list[dict[str, Any]]:
    dr2_scores = {row["model"]: row for row in read_csv(DR2_SCORE_RUN / "results" / "fit_summary.csv")}
    dr1_scores = {row["model"]: row for row in read_csv(DR1_SCORE_RUN / "results" / "fit_summary.csv")}
    rows = []
    for model in dr2_scores:
        dr2 = dr2_scores[model]
        dr1 = dr1_scores[model]
        rows.append(
            {
                "model": model,
                "DR2_chi2_total": dr2["chi2_total"],
                "DR1_chi2_total": dr1["chi2_total"],
                "DR1_minus_DR2_chi2": as_float(dr1["chi2_total"]) - as_float(dr2["chi2_total"]),
                "DR2_AIC": dr2["AIC"],
                "DR1_AIC": dr1["AIC"],
                "DR1_minus_DR2_AIC": as_float(dr1["AIC"]) - as_float(dr2["AIC"]),
                "DR2_BIC": dr2["BIC"],
                "DR1_BIC": dr1["BIC"],
                "DR1_minus_DR2_BIC": as_float(dr1["BIC"]) - as_float(dr2["BIC"]),
            }
        )
    return rows


def fixed_delta_shift_rows() -> list[dict[str, Any]]:
    dr2 = {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(DR2_SCORE_RUN / "results" / "baseline_comparison.csv")
    }
    dr1 = {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(DR1_SCORE_RUN / "results" / "baseline_comparison.csv")
    }
    rows = []
    for key, row2 in dr2.items():
        if key[0] != "MTS_fixed_p3_u3quarter":
            continue
        row1 = dr1[key]
        rows.append(
            {
                "model": key[0],
                "reference_baseline": key[1],
                "DR2_delta_chi2": row2["delta_chi2"],
                "DR1_delta_chi2": row1["delta_chi2"],
                "DR1_minus_DR2_delta_chi2": as_float(row1["delta_chi2"]) - as_float(row2["delta_chi2"]),
                "DR2_delta_AIC": row2["delta_AIC"],
                "DR1_delta_AIC": row1["delta_AIC"],
                "DR1_minus_DR2_delta_AIC": as_float(row1["delta_AIC"]) - as_float(row2["delta_AIC"]),
                "DR2_delta_BIC": row2["delta_BIC"],
                "DR1_delta_BIC": row1["delta_BIC"],
                "DR1_minus_DR2_delta_BIC": as_float(row1["delta_BIC"]) - as_float(row2["delta_BIC"]),
            }
        )
    return rows


def amplitude_shift_rows() -> list[dict[str, Any]]:
    def params(run: Path) -> dict[tuple[str, str], str]:
        return {(row["model"], row["parameter"]): row["best_fit"] for row in read_csv(run / "results" / "prior_edge_table.csv")}

    dr2 = params(DR2_SCORE_RUN)
    dr1 = params(DR1_SCORE_RUN)
    rows = []
    for model in ["MTS_fixed_p3_u3quarter", "MTS_fitted_p", "MTS_fitted_u3"]:
        for parameter in ["Omega_m", "B_mem", "p", "u3"]:
            key = (model, parameter)
            if key not in dr2 or key not in dr1:
                continue
            value2 = as_float(dr2[key])
            value1 = as_float(dr1[key])
            rows.append(
                {
                    "model": model,
                    "parameter": parameter,
                    "DR2_best_fit": value2,
                    "DR1_best_fit": value1,
                    "DR1_minus_DR2": value1 - value2,
                    "relative_shift_vs_DR2": "" if value2 == 0.0 else (value1 - value2) / value2,
                }
            )
    return rows


def ablation_rows_for_release(label: str, run: Path) -> list[dict[str, Any]]:
    summaries = {row["model"]: row for row in read_csv(run / "results" / "fit_summary.csv")}
    fixed = summaries["MTS_fixed_p3_u3quarter"]
    rows = []
    for model in ["MTS_fitted_p", "MTS_fitted_u3", "MTS_Bmem_zero"]:
        row = summaries[model]
        delta_aic = as_float(row["AIC"]) - as_float(fixed["AIC"])
        delta_bic = as_float(row["BIC"]) - as_float(fixed["BIC"])
        rows.append(
            {
                "release": label,
                "model": model,
                "delta_chi2_vs_fixed": as_float(row["chi2_total"]) - as_float(fixed["chi2_total"]),
                "delta_AIC_vs_fixed": delta_aic,
                "delta_BIC_vs_fixed": delta_bic,
                "promotion_status": "extra_parameter_not_promoted" if model != "MTS_Bmem_zero" and delta_aic > 0 and delta_bic > 0 else "negative_control_LCDM_limit",
            }
        )
    return rows


def ablation_rows() -> list[dict[str, Any]]:
    return ablation_rows_for_release("DESI_DR2", DR2_SCORE_RUN) + ablation_rows_for_release("DESI_DR1", DR1_SCORE_RUN)


def prior_edge_rows() -> list[dict[str, Any]]:
    rows = []
    for label, run in [("DESI_DR2", DR2_SCORE_RUN), ("DESI_DR1", DR1_SCORE_RUN)]:
        for row in read_csv(run / "results" / "prior_edge_table.csv"):
            edge = row["edge_flag"].lower() == "true"
            owner = "MTS" if row["model"].startswith("MTS") else "baseline"
            rows.append(
                {
                    "release": label,
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
    rows = []
    for label, run in [("DESI_DR2", DR2_SCORE_RUN), ("DESI_DR1", DR1_SCORE_RUN)]:
        grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
        for row in read_csv(run / "results" / "residuals.csv"):
            dataset_group = "SN" if row["dataset"].startswith("SN") else "BAO"
            grouped[(row["model"], dataset_group)].append(as_float(row["residual"]))
        models = [row["model"] for row in read_csv(run / "results" / "fit_summary.csv")]
        for model in models:
            sn = grouped.get((model, "SN"), [])
            bao = grouped.get((model, "BAO"), [])
            rows.append(
                {
                    "release": label,
                    "model": model,
                    "SN_count": len(sn),
                    "SN_RMS": rms(sn),
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
    dr2_dry = read_json(DR2_DRY_RUN / "status.json")
    dr1_dry = read_json(DR1_DRY_RUN / "status.json")
    dr2_status = read_json(DR2_SCORE_RUN / "status.json")
    dr1_status = read_json(DR1_SCORE_RUN / "status.json")
    dr1_fit = read_csv(DR1_SCORE_RUN / "results" / "fit_summary.csv")
    edge_rows = prior_edge_rows()
    edge_releases = sorted({row["release"] + ":" + row["model"] for row in edge_rows if row["edge_flag"].lower() == "true"})
    mts_edges = [item for item in edge_releases if ":MTS" in item]
    fixed_shift = {row["reference_baseline"]: row for row in fixed_delta_shift_rows()}
    ablations = ablation_rows()
    return [
        {
            "gate": "DR2_schema",
            "status": "pass" if dr2_dry.get("data_ready_for_short_smoke") else "fail",
            "evidence": dr2_dry.get("readout", ""),
            "claim_effect": "DR2 comparator valid",
        },
        {
            "gate": "DR1_schema",
            "status": "pass" if dr1_dry.get("data_ready_for_short_smoke") else "fail",
            "evidence": dr1_dry.get("readout", ""),
            "claim_effect": "DR1 branch valid",
        },
        {
            "gate": "DR1_convergence",
            "status": "pass" if all(row["convergence"].lower() == "true" for row in dr1_fit) else "fail",
            "evidence": "; ".join(f"{row['model']}={row['convergence']}" for row in dr1_fit),
            "claim_effect": "DR1 scores can be compared",
        },
        {
            "gate": "prior_edges",
            "status": "fail" if edge_releases else "pass",
            "evidence": ";".join(edge_releases) if edge_releases else "none",
            "claim_effect": "stable evidence blocked by edge-hit baseline",
        },
        {
            "gate": "MTS_prior_edges",
            "status": "pass" if not mts_edges else "fail",
            "evidence": ";".join(mts_edges) if mts_edges else "none",
            "claim_effect": "MTS branches are not edge-hit in DR1 or DR2",
        },
        {
            "gate": "DR1_fixed_branch_competitiveness",
            "status": "mixed",
            "evidence": f"vs_LCDM_dBIC={fixed_shift['LCDM']['DR1_delta_BIC']}; vs_wCDM_dBIC={fixed_shift['wCDM']['DR1_delta_BIC']}; vs_CPL_dBIC={fixed_shift['CPL']['DR1_delta_BIC']}",
            "claim_effect": "DR1 preserves wCDM/CPL BIC wins but worsens LCDM BIC loss",
        },
        {
            "gate": "release_shift_against_LCDM",
            "status": "warn",
            "evidence": f"LCDM dBIC shift={fixed_shift['LCDM']['DR1_minus_DR2_delta_BIC']}",
            "claim_effect": "release sensitivity is not zero; no stable evidence claim",
        },
        {
            "gate": "ablation_tax",
            "status": "pass" if all(row["promotion_status"] != "extra_parameter_promoted" for row in ablations) else "fail",
            "evidence": "; ".join(f"{row['release']}:{row['model']}={row['promotion_status']}" for row in ablations),
            "claim_effect": "fitted p/u3 still not promoted in either release",
        },
        {
            "gate": "stable_evidence_allowed",
            "status": "fail" if not dr1_status.get("stable_evidence_allowed", False) or not dr2_status.get("stable_evidence_allowed", False) else "pass",
            "evidence": f"DR1={dr1_status.get('readout')}; DR2={dr2_status.get('readout')}",
            "claim_effect": "release robustness diagnostic only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Under the same no-SH0ES 250-SN setup, switching DESI DR2 to DR1 preserves the qualitative fixed-branch pattern: MTS still beats wCDM and CPL by BIC, while losing to LCDM by BIC. "
                "The LCDM BIC loss worsens from about 2.93 to about 4.44, so the release split is a caution rather than a promotion. "
                "CPL edge flags remain baseline-side and no MTS branch edge-hits."
            ),
            "next_target": "tighten_CPL_prior_or_run_full_sample_full_covariance_release_test",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "score_readout.csv": (score_readout_rows(), ["release", "model", "chi2_SN", "chi2_BAO", "chi2_total", "AIC", "BIC", "convergence", "edge_flag_any"]),
        "fixed_branch_comparison.csv": (fixed_branch_comparison_rows(), ["release", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "interpretation"]),
        "release_score_shifts.csv": (
            release_shift_rows(),
            ["model", "DR2_chi2_total", "DR1_chi2_total", "DR1_minus_DR2_chi2", "DR2_AIC", "DR1_AIC", "DR1_minus_DR2_AIC", "DR2_BIC", "DR1_BIC", "DR1_minus_DR2_BIC"],
        ),
        "fixed_branch_release_delta_shifts.csv": (
            fixed_delta_shift_rows(),
            [
                "model",
                "reference_baseline",
                "DR2_delta_chi2",
                "DR1_delta_chi2",
                "DR1_minus_DR2_delta_chi2",
                "DR2_delta_AIC",
                "DR1_delta_AIC",
                "DR1_minus_DR2_delta_AIC",
                "DR2_delta_BIC",
                "DR1_delta_BIC",
                "DR1_minus_DR2_delta_BIC",
            ],
        ),
        "amplitude_shift_readout.csv": (
            amplitude_shift_rows(),
            ["model", "parameter", "DR2_best_fit", "DR1_best_fit", "DR1_minus_DR2", "relative_shift_vs_DR2"],
        ),
        "ablation_readout.csv": (ablation_rows(), ["release", "model", "delta_chi2_vs_fixed", "delta_AIC_vs_fixed", "delta_BIC_vs_fixed", "promotion_status"]),
        "prior_edge_readout.csv": (prior_edge_rows(), ["release", "model", "owner", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag", "claim_effect"]),
        "residual_summary.csv": (residual_summary_rows(), ["release", "model", "SN_count", "SN_RMS", "BAO_count", "BAO_RMS", "BAO_max_abs"]),
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
        "DR2_score_run": str(DR2_SCORE_RUN),
        "DR1_score_run": str(DR1_SCORE_RUN),
        "stable_evidence_allowed": False,
        "MTS_edge_flags_present": False,
        "baseline_edge_flags_present": True,
        "release_pattern": "qualitatively_survives_but_LCDM_BIC_gap_worsens_in_DR1",
        "next_target": "tighten_CPL_prior_or_run_full_sample_full_covariance_release_test",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DESI release no-SH0ES robustness readout.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
