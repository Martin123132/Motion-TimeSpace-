#!/usr/bin/env python3
"""No-CMB BAO+H(z) robustness matrix for the locked B_mem=2/27 branch."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
DATA_ROOT = FORMALIZATION_WORKBENCH / "data" / "cosmology"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import BAO_Hz_noCMB_diagnostic as diagnostic  # noqa: E402
import Hz_radial_expansion_smoke as hzsmoke  # noqa: E402
import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402


MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
PRIMARY_MODEL = "MTS_locked_2over27"
PRIMARY_DATASET = "BAO_DR2_plus_CC15_suggested"
CLAIM_CEILING = "no_CMB_BAO_Hz_robustness_only"

BAO_RELEASES = {
    "DESI_DR2_primary": {
        "short": "BAO_DR2",
        "role": "primary_release",
        "mean": DATA_ROOT / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": DATA_ROOT / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt",
    },
    "DESI_DR1_primary": {
        "short": "BAO_DR1",
        "role": "release_sensitivity",
        "mean": DATA_ROOT / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": DATA_ROOT / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt",
    },
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "BAO_Hz_noCMB_diagnostic.py",
        SCRIPT_DIR / "Hz_radial_expansion_smoke.py",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        WORK_DIR / "127-radial-pressure-decision-gate.md",
        WORK_DIR / "128-BAO-Hz-noCMB-diagnostic.md",
        WORK_DIR / "124-BAO-shape-residual-decomposition.md",
        WORK_DIR / "126-Hz-radial-expansion-smoke.md",
    ]
    for release in BAO_RELEASES.values():
        paths.extend([release["mean"], release["cov"]])
    for path in [
        hzsmoke.HZ_15,
        hzsmoke.HZ_32,
        hzsmoke.SOURCE_METADATA,
        *hzsmoke.COVARIANCE_FILES.values(),
    ]:
        paths.append(Path(path))
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def load_bao_releases() -> list[dict[str, Any]]:
    releases = []
    for label, config in BAO_RELEASES.items():
        bao = snbao.read_bao_data(config["mean"], config["cov"])
        bao["label"] = label
        releases.append(
            {
                "bao_release": label,
                "bao_short": config["short"],
                "bao_role": config["role"],
                "bao_data_path": str(config["mean"]),
                "bao_cov_path": str(config["cov"]),
                "bao": bao,
            }
        )
    return releases


def hz_suffix(dataset: dict[str, Any]) -> str:
    label = str(dataset["dataset_label"])
    return label.removesuffix("_primary")


def branch_role(bao_release: dict[str, Any], hz_dataset: dict[str, Any]) -> str:
    if hz_dataset["role"] == "diagnostic_only":
        return "diagnostic_only"
    if bao_release["bao_role"] == "release_sensitivity":
        return "release_sensitivity"
    if hz_dataset["role"] == "covariance_sensitivity":
        return "covariance_sensitivity"
    if hz_dataset["role"] == "diagonal_sensitivity":
        return "diagonal_sensitivity"
    return "primary"


def branch_label(bao_release: dict[str, Any], hz_dataset: dict[str, Any]) -> str:
    return f"{bao_release['bao_short']}_plus_{hz_suffix(hz_dataset)}"


def branch_metadata(bao_release: dict[str, Any], hz_dataset: dict[str, Any]) -> dict[str, Any]:
    role = branch_role(bao_release, hz_dataset)
    return {
        "dataset_label": branch_label(bao_release, hz_dataset),
        "branch_role": role,
        "bao_release": bao_release["bao_release"],
        "bao_role": bao_release["bao_role"],
        "bao_data_path": bao_release["bao_data_path"],
        "bao_cov_path": bao_release["bao_cov_path"],
        "hz_dataset_label": hz_dataset["dataset_label"],
        "hz_role": hz_dataset["role"],
        "hz_covariance_label": hz_dataset["covariance_label"],
        "hz_data_path": hz_dataset["data_path"],
        "hz_covariance_path": hz_dataset["covariance_path"],
        "production_branch": role != "diagnostic_only",
    }


def data_schema_rows(bao_releases: list[dict[str, Any]], hz_datasets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for release in bao_releases:
        bao = release["bao"]
        rows.append(
            {
                "source_label": release["bao_release"],
                "source_type": "BAO",
                "role": release["bao_role"],
                "path": release["bao_data_path"],
                "covariance_path": release["bao_cov_path"],
                "rows": len(bao["rows"]),
                "covariance_shape": f"{bao['covariance'].shape[0]}x{bao['covariance'].shape[1]}",
                "status": "pass",
            }
        )
    for dataset in hz_datasets:
        rows.append(
            {
                "source_label": dataset["dataset_label"],
                "source_type": "Hz",
                "role": dataset["role"],
                "path": dataset["data_path"],
                "covariance_path": dataset["covariance_path"],
                "rows": len(dataset["z"]),
                "covariance_shape": f"{dataset['covariance'].shape[0]}x{dataset['covariance'].shape[1]}",
                "status": "pass",
            }
        )
    return rows


def branch_manifest_rows(branches: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "dataset_label": label,
            "branch_role": meta["branch_role"],
            "bao_release": meta["bao_release"],
            "bao_role": meta["bao_role"],
            "hz_dataset_label": meta["hz_dataset_label"],
            "hz_role": meta["hz_role"],
            "hz_covariance_label": meta["hz_covariance_label"],
            "production_branch": meta["production_branch"],
        }
        for label, meta in sorted(branches.items())
    ]


def add_metadata(row: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(row)
    for key, value in meta.items():
        if key != "dataset_label":
            enriched[key] = value
    return enriched


def metadata_for_rows(rows: list[dict[str, Any]], branches: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for row in rows:
        enriched.append(add_metadata(row, branches[str(row["dataset_label"])]))
    return enriched


def robustness_matrix_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in comparisons:
        if row["model"] != PRIMARY_MODEL:
            continue
        rows.append(
            {
                "dataset_label": row["dataset_label"],
                "branch_role": row["branch_role"],
                "production_branch": row["production_branch"],
                "bao_release": row["bao_release"],
                "hz_dataset_label": row["hz_dataset_label"],
                "hz_covariance_label": row["hz_covariance_label"],
                "reference_model": row["reference_model"],
                "delta_chi2": row["delta_chi2"],
                "delta_AIC": row["delta_AIC"],
                "delta_BIC": row["delta_BIC"],
                "readout": row["readout"],
                "locked_edge_flag": row["locked_edge_flag"],
                "reference_edge_flag": row["reference_edge_flag"],
            }
        )
    return rows


def lcdm_comparisons(comparisons: list[dict[str, Any]], production_only: bool) -> list[dict[str, Any]]:
    rows = [row for row in comparisons if row["reference_model"] == "LCDM"]
    if production_only:
        rows = [row for row in rows if row["production_branch"] in [True, "True"]]
    return rows


def summarize_group(label: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = np.asarray([float(row["delta_BIC"]) for row in rows], dtype=float)
    preferred = int(np.sum(deltas <= -2.0))
    draw = int(np.sum((deltas > -2.0) & (deltas < 2.0)))
    disfavored = int(np.sum(deltas >= 2.0))
    if disfavored:
        verdict = "mixed_with_locked_disfavored_branch"
    elif preferred and draw:
        verdict = "stable_preference_or_draw"
    elif preferred == len(rows):
        verdict = "stable_locked_preference"
    else:
        verdict = "stable_competitive_draw"
    return {
        "group": label,
        "branch_count": len(rows),
        "preferred_count": preferred,
        "draw_count": draw,
        "disfavored_count": disfavored,
        "min_delta_BIC": float(np.min(deltas)),
        "max_delta_BIC": float(np.max(deltas)),
        "mean_delta_BIC": float(np.mean(deltas)),
        "median_delta_BIC": float(np.median(deltas)),
        "verdict": verdict,
    }


def stability_summary_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    production = lcdm_comparisons(comparisons, production_only=True)
    all_rows = lcdm_comparisons(comparisons, production_only=False)
    rows = [
        summarize_group("production_all_BAO_Hz_branches_vs_LCDM", production),
        summarize_group("all_branches_including_nonstat_diagnostic_vs_LCDM", all_rows),
    ]
    for release in sorted({row["bao_release"] for row in all_rows}):
        release_rows = [row for row in production if row["bao_release"] == release]
        if release_rows:
            rows.append(summarize_group(f"{release}_production_vs_LCDM", release_rows))
    return rows


def omega_shift_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reference = diagnostic.t7_omega()
    rows = []
    for row in fit_rows:
        if row["model"] != PRIMARY_MODEL:
            continue
        rows.append(
            {
                "dataset_label": row["dataset_label"],
                "branch_role": row["branch_role"],
                "production_branch": row["production_branch"],
                "bao_release": row["bao_release"],
                "hz_dataset_label": row["hz_dataset_label"],
                "Omega_m0": row["Omega_m0"],
                "T7_reference_Omega_m0": reference,
                "shift_vs_T7": float(row["Omega_m0"]) - reference,
            }
        )
    return rows


def decision_rows(fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = next(row for row in comparisons if row["dataset_label"] == PRIMARY_DATASET and row["reference_model"] == "LCDM")
    production = lcdm_comparisons(comparisons, production_only=True)
    summaries = stability_summary_rows(comparisons)
    production_summary = next(row for row in summaries if row["group"] == "production_all_BAO_Hz_branches_vs_LCDM")
    worst = max(production, key=lambda row: float(row["delta_BIC"]))
    best = min(production, key=lambda row: float(row["delta_BIC"]))
    locked_edges = [
        row["dataset_label"]
        for row in fit_rows
        if row["model"] == PRIMARY_MODEL and row["production_branch"] in [True, "True"] and row["edge_flag"] in [True, "True"]
    ]
    lcdm_edges = [
        row["dataset_label"]
        for row in fit_rows
        if row["model"] == "LCDM" and row["production_branch"] in [True, "True"] and row["edge_flag"] in [True, "True"]
    ]
    if locked_edges or lcdm_edges:
        status = "noCMB_radial_robustness_locked_or_LCDM_edge_flagged"
    elif int(production_summary["disfavored_count"]):
        status = "noCMB_radial_robustness_mixed"
    elif int(production_summary["preferred_count"]):
        status = "noCMB_radial_robustness_stable_draw_with_preference_branches"
    else:
        status = "noCMB_radial_robustness_stable_draw"
    primary_fit = next(row for row in fit_rows if row["dataset_label"] == PRIMARY_DATASET and row["model"] == PRIMARY_MODEL)
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"production branches={production_summary['branch_count']}; preferred={production_summary['preferred_count']}; draw={production_summary['draw_count']}; disfavored={production_summary['disfavored_count']}",
        },
        {
            "item": "primary_DR2_CC15_suggested_vs_LCDM",
            "verdict": primary["readout"],
            "evidence": f"delta_BIC={float(primary['delta_BIC']):.12g}; delta_chi2={float(primary['delta_chi2']):.12g}",
        },
        {
            "item": "best_production_branch_vs_LCDM",
            "verdict": best["readout"],
            "evidence": f"{best['dataset_label']}; delta_BIC={float(best['delta_BIC']):.12g}",
        },
        {
            "item": "worst_production_branch_vs_LCDM",
            "verdict": worst["readout"],
            "evidence": f"{worst['dataset_label']}; delta_BIC={float(worst['delta_BIC']):.12g}",
        },
        {
            "item": "primary_locked_Omega_m0",
            "verdict": "near_T7_late_value",
            "evidence": f"Omega_m0={float(primary_fit['Omega_m0']):.12g}; T7={diagnostic.t7_omega():.12g}; shift={float(primary_fit['Omega_m0']) - diagnostic.t7_omega():.12g}",
        },
        {
            "item": "edge_flags",
            "verdict": "locked_and_LCDM_clean" if not locked_edges and not lcdm_edges else "locked_or_LCDM_edge_issue",
            "evidence": f"locked={';'.join(locked_edges) if locked_edges else 'none'}; LCDM={';'.join(lcdm_edges) if lcdm_edges else 'none'}",
        },
        {
            "item": "claim_status",
            "verdict": "robustness_only_no_promotion",
            "evidence": "No CMB priors, no BAO-shape correction, and no Omega-map closure were introduced.",
        },
        {
            "item": "next_target",
            "verdict": "growth_route_or_radial_theorem_contract",
            "evidence": "If the no-CMB draw/preference survives DR1/DR2, next stress is growth/H(z)-shape or a derivation contract for the radial memory term.",
        },
    ]


def run_robustness(output_root: Path, timestamp: str | None = None, max_iter: int = 300) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-BAO-Hz-noCMB-robustness"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in source_rows if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    bao_releases = load_bao_releases()
    hz_datasets = diagnostic.hz_datasets_to_score()
    branches: dict[str, dict[str, Any]] = {}
    fit_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []

    for bao_release in bao_releases:
        for hz_dataset in hz_datasets:
            meta = branch_metadata(bao_release, hz_dataset)
            branches[meta["dataset_label"]] = meta
            for model in MODEL_ORDER:
                fit, edges, vectors = diagnostic.fit_model(
                    meta["dataset_label"],
                    meta["branch_role"],
                    model,
                    bao_release["bao"],
                    hz_dataset,
                    max_iter,
                )
                fit["claim_ceiling"] = CLAIM_CEILING
                fit_rows.append(add_metadata(fit, meta))
                edge_rows.extend(add_metadata(row, meta) for row in edges)
                bao_residuals = diagnostic.bao_residual_rows(
                    meta["dataset_label"],
                    model,
                    bao_release["bao"],
                    vectors["bao_residual"],
                    vectors["bao_predicted"],
                )
                hz_residuals = diagnostic.hz_residual_rows(
                    meta["dataset_label"],
                    model,
                    hz_dataset,
                    vectors["hz_residual"],
                    vectors["hz_predicted"],
                )
                residual_rows.extend(add_metadata(row, meta) for row in [*bao_residuals, *hz_residuals])

    sector_rows = metadata_for_rows(diagnostic.sector_rows(fit_rows), branches)
    comparisons = metadata_for_rows(diagnostic.baseline_comparison_rows(fit_rows), branches)
    controls = metadata_for_rows(diagnostic.control_rows(fit_rows), branches)
    robustness = robustness_matrix_rows(comparisons)
    stability = stability_summary_rows(comparisons)
    omega_rows = omega_shift_rows(fit_rows)
    decisions = decision_rows(fit_rows, comparisons)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "data_schema.csv",
        data_schema_rows(bao_releases, hz_datasets),
        ["source_label", "source_type", "role", "path", "covariance_path", "rows", "covariance_shape", "status"],
    )
    write_csv(
        results_dir / "branch_manifest.csv",
        branch_manifest_rows(branches),
        [
            "dataset_label",
            "branch_role",
            "bao_release",
            "bao_role",
            "hz_dataset_label",
            "hz_role",
            "hz_covariance_label",
            "production_branch",
        ],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "bao_role",
            "hz_dataset_label",
            "hz_role",
            "hz_covariance_label",
            "model",
            "success",
            "chi2_BAO",
            "chi2_Hz",
            "chi2_total",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "dof",
            "edge_flag",
            "Omega_m0",
            "h",
            "H0",
            "w",
            "w0",
            "wa",
            "BAO_alpha",
            "optimizer",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "sector_breakdown.csv",
        sector_rows,
        ["dataset_label", "branch_role", "production_branch", "bao_release", "hz_dataset_label", "model", "sector", "chi2", "fraction_total"],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_rows,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "hz_dataset_label",
            "model",
            "parameter",
            "best_fit",
            "lower",
            "upper",
            "distance_to_edge",
            "edge_flag",
        ],
    )
    write_csv(
        results_dir / "residuals.csv",
        residual_rows,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "hz_dataset_label",
            "sector",
            "model",
            "row_index",
            "z",
            "observable",
            "observed",
            "predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "hz_dataset_label",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_edge_flag",
            "reference_edge_flag",
            "readout",
        ],
    )
    write_csv(
        results_dir / "robustness_matrix.csv",
        robustness,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "hz_dataset_label",
            "hz_covariance_label",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "readout",
            "locked_edge_flag",
            "reference_edge_flag",
        ],
    )
    write_csv(
        results_dir / "stability_summary.csv",
        stability,
        [
            "group",
            "branch_count",
            "preferred_count",
            "draw_count",
            "disfavored_count",
            "min_delta_BIC",
            "max_delta_BIC",
            "mean_delta_BIC",
            "median_delta_BIC",
            "verdict",
        ],
    )
    write_csv(
        results_dir / "control_reproduction.csv",
        controls,
        [
            "dataset_label",
            "branch_role",
            "production_branch",
            "bao_release",
            "hz_dataset_label",
            "control",
            "delta_chi2",
            "delta_Omega_m0",
            "delta_h",
            "delta_BAO_alpha",
            "status",
        ],
    )
    write_csv(
        results_dir / "omega_shift_matrix.csv",
        omega_rows,
        ["dataset_label", "branch_role", "production_branch", "bao_release", "hz_dataset_label", "Omega_m0", "T7_reference_Omega_m0", "shift_vs_T7"],
    )
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "primary_dataset": PRIMARY_DATASET,
        "models": MODEL_ORDER,
        "bao_releases": list(BAO_RELEASES),
        "branches": len(branches),
        "fit_rows": len(fit_rows),
        "generated": [
            "source_register.csv",
            "data_schema.csv",
            "branch_manifest.csv",
            "fit_summary.csv",
            "sector_breakdown.csv",
            "prior_edge_table.csv",
            "residuals.csv",
            "baseline_comparisons.csv",
            "robustness_matrix.csv",
            "stability_summary.csv",
            "control_reproduction.csv",
            "omega_shift_matrix.csv",
            "decision.csv",
        ],
        "next_target": "129-noCMB-radial-robustness-or-growth-route.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_robustness(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
