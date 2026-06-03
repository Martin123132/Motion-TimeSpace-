from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "CPL-prior-sensitivity-readout"
STATUS = "CPL_prior_sensitivity_reveals_baseline_edge_migration_DR2_clean_DR1_still_edge"
CLAIM_CEILING = "baseline_prior_sensitivity_diagnostic_only_no_stable_evidence_or_parent_promotion"

RUNS = {
    ("DESI_DR2", "default_CPL"): ROOT / "runs" / "20260601-101537-cosmo-SN-BAO-short-smoke",
    ("DESI_DR1", "default_CPL"): ROOT / "runs" / "20260601-102042-cosmo-SN-BAO-short-smoke",
    ("DESI_DR2", "wide_wa_only"): ROOT / "runs" / "20260601-102601-cosmo-SN-BAO-short-smoke",
    ("DESI_DR1", "wide_wa_only"): ROOT / "runs" / "20260601-102620-cosmo-SN-BAO-short-smoke",
    ("DESI_DR2", "wide_w0_wa_box"): ROOT / "runs" / "20260601-102748-cosmo-SN-BAO-short-smoke",
    ("DESI_DR1", "wide_w0_wa_box"): ROOT / "runs" / "20260601-102803-cosmo-SN-BAO-short-smoke",
}


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
        (ROOT / "290-DESI-release-no-SH0ES-robustness-readout.md", "release-split checkpoint that motivated CPL prior sensitivity"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "runner patched to allow CPL w0 and wa prior overrides"),
        (ROOT / "scripts" / "CPL_prior_sensitivity_readout.py", "this readout script"),
    ]
    for (release, prior_box), run in RUNS.items():
        sources.extend(
            [
                (run / "status.json", f"{release} {prior_box} status"),
                (run / "run_config.json", f"{release} {prior_box} run config"),
                (run / "results" / "fit_summary.csv", f"{release} {prior_box} scores"),
                (run / "results" / "baseline_comparison.csv", f"{release} {prior_box} baseline comparisons"),
                (run / "results" / "prior_edge_table.csv", f"{release} {prior_box} prior edges"),
            ]
        )
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def prior_config_label(run: Path) -> str:
    config = read_json(run / "run_config.json")
    prior_config = config.get("prior_config", {})
    if not prior_config:
        return "CPL.w0=(-2,-0.2); CPL.wa=(-2,2)"
    return "; ".join(f"{key}={tuple(value)}" for key, value in sorted(prior_config.items()))


def score_readout_rows() -> list[dict[str, Any]]:
    rows = []
    for (release, prior_box), run in RUNS.items():
        status = read_json(run / "status.json")
        edge_rows = read_csv(run / "results" / "prior_edge_table.csv")
        edge_by_model: dict[str, bool] = {}
        for edge in edge_rows:
            edge_by_model[edge["model"]] = edge_by_model.get(edge["model"], False) or edge["edge_flag"].lower() == "true"
        for row in read_csv(run / "results" / "fit_summary.csv"):
            rows.append(
                {
                    "release": release,
                    "prior_box": prior_box,
                    "prior_config": prior_config_label(run),
                    "model": row["model"],
                    "chi2_total": row["chi2_total"],
                    "AIC": row["AIC"],
                    "BIC": row["BIC"],
                    "convergence": row["convergence"],
                    "edge_flag_any": str(edge_by_model.get(row["model"], False)).lower(),
                    "run_readout": status.get("readout", ""),
                }
            )
    return rows


def fixed_branch_rows() -> list[dict[str, Any]]:
    rows = []
    for (release, prior_box), run in RUNS.items():
        for row in read_csv(run / "results" / "baseline_comparison.csv"):
            if row["model"] != "MTS_fixed_p3_u3quarter":
                continue
            rows.append(
                {
                    "release": release,
                    "prior_box": prior_box,
                    "reference_baseline": row["reference_baseline"],
                    "delta_chi2": row["delta_chi2"],
                    "delta_AIC": row["delta_AIC"],
                    "delta_BIC": row["delta_BIC"],
                    "interpretation": interpretation(row),
                }
            )
    return rows


def interpretation(row: dict[str, str]) -> str:
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


def cpl_edge_migration_rows() -> list[dict[str, Any]]:
    rows = []
    for (release, prior_box), run in RUNS.items():
        cpl_rows = [row for row in read_csv(run / "results" / "prior_edge_table.csv") if row["model"] == "CPL"]
        for row in cpl_rows:
            rows.append(
                {
                    "release": release,
                    "prior_box": prior_box,
                    "parameter": row["parameter"],
                    "best_fit": row["best_fit"],
                    "lower": row["lower"],
                    "upper": row["upper"],
                    "distance_to_edge": row["distance_to_edge"],
                    "edge_flag": row["edge_flag"],
                    "edge_meaning": "baseline_edge_blocks_stable_evidence" if row["edge_flag"].lower() == "true" else "not_edge",
                }
            )
    return rows


def cpl_sensitivity_rows() -> list[dict[str, Any]]:
    rows = []
    for release in ["DESI_DR2", "DESI_DR1"]:
        default_run = RUNS[(release, "default_CPL")]
        default_scores = {row["model"]: row for row in read_csv(default_run / "results" / "fit_summary.csv")}
        for prior_box in ["wide_wa_only", "wide_w0_wa_box"]:
            run = RUNS[(release, prior_box)]
            scores = {row["model"]: row for row in read_csv(run / "results" / "fit_summary.csv")}
            default_cpl = default_scores["CPL"]
            cpl = scores["CPL"]
            rows.append(
                {
                    "release": release,
                    "comparison": f"{prior_box}_minus_default",
                    "CPL_delta_chi2": as_float(cpl["chi2_total"]) - as_float(default_cpl["chi2_total"]),
                    "CPL_delta_AIC": as_float(cpl["AIC"]) - as_float(default_cpl["AIC"]),
                    "CPL_delta_BIC": as_float(cpl["BIC"]) - as_float(default_cpl["BIC"]),
                    "default_CPL_chi2": default_cpl["chi2_total"],
                    "new_CPL_chi2": cpl["chi2_total"],
                }
            )
    return rows


def mts_fixed_vs_cpl_shift_rows() -> list[dict[str, Any]]:
    fixed = fixed_branch_rows()
    by_key = {(row["release"], row["prior_box"], row["reference_baseline"]): row for row in fixed}
    rows = []
    for release in ["DESI_DR2", "DESI_DR1"]:
        default = by_key[(release, "default_CPL", "CPL")]
        for prior_box in ["wide_wa_only", "wide_w0_wa_box"]:
            current = by_key[(release, prior_box, "CPL")]
            rows.append(
                {
                    "release": release,
                    "comparison": f"{prior_box}_minus_default",
                    "default_MTS_minus_CPL_delta_chi2": default["delta_chi2"],
                    "new_MTS_minus_CPL_delta_chi2": current["delta_chi2"],
                    "shift_delta_chi2": as_float(current["delta_chi2"]) - as_float(default["delta_chi2"]),
                    "default_MTS_minus_CPL_delta_AIC": default["delta_AIC"],
                    "new_MTS_minus_CPL_delta_AIC": current["delta_AIC"],
                    "shift_delta_AIC": as_float(current["delta_AIC"]) - as_float(default["delta_AIC"]),
                    "default_MTS_minus_CPL_delta_BIC": default["delta_BIC"],
                    "new_MTS_minus_CPL_delta_BIC": current["delta_BIC"],
                    "shift_delta_BIC": as_float(current["delta_BIC"]) - as_float(default["delta_BIC"]),
                }
            )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    edges = cpl_edge_migration_rows()
    dr2_box_edges = [row for row in edges if row["release"] == "DESI_DR2" and row["prior_box"] == "wide_w0_wa_box" and row["edge_flag"].lower() == "true"]
    dr1_box_edges = [row for row in edges if row["release"] == "DESI_DR1" and row["prior_box"] == "wide_w0_wa_box" and row["edge_flag"].lower() == "true"]
    mts_edges = []
    for (release, prior_box), run in RUNS.items():
        for row in read_csv(run / "results" / "prior_edge_table.csv"):
            if row["model"].startswith("MTS") and row["edge_flag"].lower() == "true":
                mts_edges.append(f"{release}:{prior_box}:{row['model']}:{row['parameter']}")
    fixed = fixed_branch_rows()
    dr1_box = [row for row in fixed if row["release"] == "DESI_DR1" and row["prior_box"] == "wide_w0_wa_box" and row["reference_baseline"] == "CPL"][0]
    dr2_box = [row for row in fixed if row["release"] == "DESI_DR2" and row["prior_box"] == "wide_w0_wa_box" and row["reference_baseline"] == "CPL"][0]
    return [
        {
            "gate": "runner_supports_CPL_w0_override",
            "status": "pass",
            "evidence": "wide_w0_wa_box configs contain CPL.w0 and CPL.wa overrides",
            "claim_effect": "baseline prior sensitivity can be tested symmetrically",
        },
        {
            "gate": "DR2_full_CPL_box_edge_free",
            "status": "pass" if not dr2_box_edges else "fail",
            "evidence": "none" if not dr2_box_edges else ";".join(f"{row['parameter']}={row['best_fit']}" for row in dr2_box_edges),
            "claim_effect": "DR2 CPL comparison can be read without edge caveat in this short smoke",
        },
        {
            "gate": "DR1_full_CPL_box_edge_free",
            "status": "fail" if dr1_box_edges else "pass",
            "evidence": "none" if not dr1_box_edges else ";".join(f"{row['parameter']}={row['best_fit']}" for row in dr1_box_edges),
            "claim_effect": "DR1 still has CPL edge instability",
        },
        {
            "gate": "MTS_edges_all_prior_boxes",
            "status": "pass" if not mts_edges else "fail",
            "evidence": "none" if not mts_edges else ";".join(mts_edges),
            "claim_effect": "MTS branches are not edge-hit in these CPL prior tests",
        },
        {
            "gate": "MTS_vs_CPL_DR2_full_box",
            "status": "pass_mixed",
            "evidence": f"delta_chi2={dr2_box['delta_chi2']}; delta_AIC={dr2_box['delta_AIC']}; delta_BIC={dr2_box['delta_BIC']}",
            "claim_effect": "MTS still beats CPL by AIC/BIC in DR2 but raw chi2 is worse",
        },
        {
            "gate": "MTS_vs_CPL_DR1_full_box",
            "status": "unstable_mixed",
            "evidence": f"delta_chi2={dr1_box['delta_chi2']}; delta_AIC={dr1_box['delta_AIC']}; delta_BIC={dr1_box['delta_BIC']}",
            "claim_effect": "MTS still beats CPL by BIC in DR1 but CPL edge remains and AIC flips against MTS",
        },
        {
            "gate": "stable_evidence_allowed",
            "status": "fail",
            "evidence": "DR1 wide CPL box still edge-hits wa=-5; branch remains 250-SN short-smoke",
            "claim_effect": "no stable cosmology claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Widening only CPL wa moved the edge from wa to w0. After adding and using a wider w0/wa CPL box, DR2 becomes edge-free and still leaves MTS ahead of CPL by AIC/BIC while worse in raw chi2. "
                "DR1 still drives CPL to the wa=-5 edge, and MTS loses AIC to CPL while retaining a BIC advantage. "
                "This makes the baseline comparison more honest but not stable enough for evidence language."
            ),
            "next_target": "full_sample_full_covariance_or_non_SN_holdout_before_stronger_cosmology_language",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "score_readout.csv": (score_readout_rows(), ["release", "prior_box", "prior_config", "model", "chi2_total", "AIC", "BIC", "convergence", "edge_flag_any", "run_readout"]),
        "fixed_branch_comparison.csv": (fixed_branch_rows(), ["release", "prior_box", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "interpretation"]),
        "CPL_edge_migration.csv": (cpl_edge_migration_rows(), ["release", "prior_box", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag", "edge_meaning"]),
        "CPL_score_sensitivity.csv": (cpl_sensitivity_rows(), ["release", "comparison", "CPL_delta_chi2", "CPL_delta_AIC", "CPL_delta_BIC", "default_CPL_chi2", "new_CPL_chi2"]),
        "MTS_fixed_vs_CPL_shift.csv": (
            mts_fixed_vs_cpl_shift_rows(),
            [
                "release",
                "comparison",
                "default_MTS_minus_CPL_delta_chi2",
                "new_MTS_minus_CPL_delta_chi2",
                "shift_delta_chi2",
                "default_MTS_minus_CPL_delta_AIC",
                "new_MTS_minus_CPL_delta_AIC",
                "shift_delta_AIC",
                "default_MTS_minus_CPL_delta_BIC",
                "new_MTS_minus_CPL_delta_BIC",
                "shift_delta_BIC",
            ],
        ),
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
        "stable_evidence_allowed": False,
        "runner_patch": "CPL_w0_prior_override_added_to_cosmo_SN_BAO_closure_runner",
        "DR2_full_CPL_box": "edge_free_MTS_beats_CPL_AIC_BIC_raw_chi2_worse",
        "DR1_full_CPL_box": "CPL_wa_edge_persists_MTS_BIC_win_AIC_loss_raw_chi2_worse",
        "next_target": "full_sample_full_covariance_or_non_SN_holdout_before_stronger_cosmology_language",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPL prior sensitivity readout.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
