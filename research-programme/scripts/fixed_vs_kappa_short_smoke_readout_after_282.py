from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fixed-vs-kappa-short-smoke-readout-after-282"
STATUS = "fixed_2over27_short_smoke_competitive_kappa_not_promoted_no_parent_claim"
CLAIM_CEILING = "SN_BAO_short_smoke_closure_score_only_no_parent_CMB_or_local_GR_promotion"
SHORT_RUN = ROOT / "runs" / "20260601-000105-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "282-empirical-preflight-readout-after-281.md", "preflight readout that authorized fixed-vs-kappa route"),
        (ROOT / "scripts" / "fixed_vs_kappa_cosmology_runner.py", "scoring runner"),
        (SHORT_RUN / "status.json", "short-smoke status"),
        (SHORT_RUN / "results" / "fit_summary.csv", "model fit summary"),
        (SHORT_RUN / "results" / "baseline_comparison.csv", "AIC/BIC baseline comparison"),
        (SHORT_RUN / "results" / "prior_edge_table.csv", "prior edge diagnostics"),
        (SHORT_RUN / "results" / "residual_summary.csv", "SN and BAO residual diagnostics"),
        (SHORT_RUN / "results" / "implementation_gates.csv", "implementation gate results"),
        (ROOT / "scripts" / "fixed_vs_kappa_short_smoke_readout_after_282.py", "this readout script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def fit_lookup() -> dict[str, dict[str, str]]:
    return {row["model"]: row for row in read_csv(SHORT_RUN / "results" / "fit_summary.csv")}


def comparison_lookup() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["model"], row["reference_baseline"]): row
        for row in read_csv(SHORT_RUN / "results" / "baseline_comparison.csv")
    }


def score_readout_rows() -> list[dict[str, Any]]:
    fits = fit_lookup()
    comparisons = comparison_lookup()
    fixed = fits["MTS_fixed_2over27_no_clock"]
    kappa = fits["MTS_kappa_free_no_clock"]
    lcdm = comparisons[("MTS_fixed_2over27_no_clock", "LCDM")]
    wcdm = comparisons[("MTS_fixed_2over27_no_clock", "wCDM")]
    cpl = comparisons[("MTS_fixed_2over27_no_clock", "CPL")]
    fixed_vs_kappa = comparisons[("MTS_fixed_2over27_no_clock", "MTS_kappa_free_no_clock")]
    return [
        {
            "readout": "fixed_branch_vs_LCDM",
            "value": f"delta_chi2={lcdm['delta_chi2']}; delta_AIC={lcdm['delta_AIC']}; delta_BIC={lcdm['delta_BIC']}",
            "interpretation": "fixed branch beats LCDM in this same-data short smoke",
        },
        {
            "readout": "fixed_branch_vs_wCDM",
            "value": f"delta_chi2={wcdm['delta_chi2']}; delta_AIC={wcdm['delta_AIC']}; delta_BIC={wcdm['delta_BIC']}",
            "interpretation": "fixed branch is slightly better chi2 and wins AIC/BIC vs wCDM here",
        },
        {
            "readout": "fixed_branch_vs_CPL",
            "value": f"delta_chi2={cpl['delta_chi2']}; delta_AIC={cpl['delta_AIC']}; delta_BIC={cpl['delta_BIC']}",
            "interpretation": "CPL has slightly better raw chi2 but fixed branch wins AIC/BIC due fewer parameters",
        },
        {
            "readout": "fixed_branch_vs_kappa_free",
            "value": f"delta_chi2={fixed_vs_kappa['delta_chi2']}; delta_AIC={fixed_vs_kappa['delta_AIC']}; delta_BIC={fixed_vs_kappa['delta_BIC']}",
            "interpretation": "kappa-free gains negligible chi2 and fails information-criterion tax",
        },
        {
            "readout": "kappa_best_fit",
            "value": f"B_mem={kappa['B_mem']}; kappa_mem={kappa['kappa_mem']}; fixed_Bmem={fixed['B_mem']}",
            "interpretation": "kappa-free optimum sits very close to fixed 2/27 branch",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    status = read_json(SHORT_RUN / "status.json")
    gates = read_csv(SHORT_RUN / "results" / "implementation_gates.csv")
    edge_rows = read_csv(SHORT_RUN / "results" / "prior_edge_table.csv")
    edge_flags = [row for row in edge_rows if row["edge_flag"] == "True"]
    return [
        {
            "gate": "scores_generated",
            "status": "pass" if status.get("scores_generated") is True else "fail",
            "evidence": str(status.get("scores_generated")),
            "claim_effect": "short-smoke scoring exists",
        },
        {
            "gate": "all_models_converged",
            "status": next(row["status"] for row in gates if row["gate"] == "all_models_converged"),
            "evidence": next(row["evidence"] for row in gates if row["gate"] == "all_models_converged"),
            "claim_effect": "nonconverged models cannot be evidence",
        },
        {
            "gate": "prior_edges_absent",
            "status": "pass" if not edge_flags else "warn",
            "evidence": "no edge flags" if not edge_flags else ",".join(row["model"] for row in edge_flags),
            "claim_effect": "edge-hit branches would be unstable evidence",
        },
        {
            "gate": "fixed_branch_competitive_with_baselines",
            "status": next(row["status"] for row in gates if row["gate"] == "fixed_branch_competitive_with_baselines"),
            "evidence": next(row["evidence"] for row in gates if row["gate"] == "fixed_branch_competitive_with_baselines"),
            "claim_effect": "late-time SN+BAO closure score only",
        },
        {
            "gate": "kappa_parameter_tax_paid",
            "status": next(row["status"] for row in gates if row["gate"] == "kappa_parameter_tax_paid"),
            "evidence": next(row["evidence"] for row in gates if row["gate"] == "kappa_parameter_tax_paid"),
            "claim_effect": "kappa-free is not promoted",
        },
        {
            "gate": "parent_or_CMB_promotion_allowed",
            "status": "fail",
            "evidence": "short smoke only; no CMB/growth/local bound integration",
            "claim_effect": "no parent/CMB/local-GR promotion",
        },
    ]


def residual_readout_rows() -> list[dict[str, Any]]:
    rows = read_csv(SHORT_RUN / "results" / "residual_summary.csv")
    return [
        {
            "model": row["model"],
            "SN_rms_residual": row["SN_rms_residual"],
            "BAO_rms_residual": row["BAO_rms_residual"],
            "BAO_max_abs_residual": row["BAO_max_abs_residual"],
            "readout": "diagnostic_only",
        }
        for row in rows
    ]


def next_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "action": "repair_generic_BAO_manifest",
            "reason": "generic SN+BAO runner remains blocked even though fixed-vs-kappa runner has explicit paths",
            "claim_allowed_after": "schema readiness only",
        },
        {
            "order": 2,
            "action": "run_no_SH0ES_shape_branch",
            "reason": "current short smoke uses Pantheon+/SH0ES source with calibrators excluded but not full no-SH0ES policy audit",
            "claim_allowed_after": "closure robustness only",
        },
        {
            "order": 3,
            "action": "split_or_release_robustness",
            "reason": "same-data short smoke must survive BAO release/split and prior sensitivity before stronger empirical language",
            "claim_allowed_after": "stability diagnostic",
        },
        {
            "order": 4,
            "action": "derive_or_reject_memory_stress_normalization",
            "reason": "kappa-free optimum near fixed 2/27 is encouraging but not a derivation",
            "claim_allowed_after": "theorem target only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The fixed 2/27 no-clock branch is competitive in this SN+BAO short smoke: it beats LCDM/wCDM/CPL by AIC/BIC in the recorded comparison, all models converge, and no prior-edge flags appear. "
                "The kappa-free branch improves raw chi2 by only ~0.00019 and fails the AIC/BIC tax, so kappa is not promoted. "
                "This is empirical closure evidence only; it does not derive B_mem or settle CMB/growth/local-GR."
            ),
            "next_target": "BAO_manifest_repair_noSH0ES_and_split_robustness_before_stronger_claims",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "score_readout.csv": (score_readout_rows(), ["readout", "value", "interpretation"]),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "residual_readout.csv": (residual_readout_rows(), ["model", "SN_rms_residual", "BAO_rms_residual", "BAO_max_abs_residual", "readout"]),
        "next_actions.csv": (next_action_rows(), ["order", "action", "reason", "claim_allowed_after"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = read_json(SHORT_RUN / "status.json")
    fits = fit_lookup()
    comparisons = comparison_lookup()
    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_short_smoke_run": str(SHORT_RUN),
        "generated": list(outputs),
        "scores_generated": True,
        "fixed_branch_AIC_vs_LCDM": float(comparisons[("MTS_fixed_2over27_no_clock", "LCDM")]["delta_AIC"]),
        "fixed_branch_AIC_vs_wCDM": float(comparisons[("MTS_fixed_2over27_no_clock", "wCDM")]["delta_AIC"]),
        "fixed_branch_AIC_vs_CPL": float(comparisons[("MTS_fixed_2over27_no_clock", "CPL")]["delta_AIC"]),
        "kappa_delta_chi2_improvement": float(status["kappa_delta_chi2_improvement"]),
        "kappa_promoted": bool(status["kappa_promoted"]),
        "all_models_converged": True,
        "prior_edge_flags": False,
        "parent_or_CMB_or_local_GR_promotion_allowed": False,
        "next_target": "BAO_manifest_repair_noSH0ES_and_split_robustness_before_stronger_claims",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Readout for fixed-vs-kappa short smoke after checkpoint 282.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
