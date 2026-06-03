#!/usr/bin/env python3
"""Freeze the SN+BAO short-smoke scoring contract before any fits."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
WORKBENCH = POST_CHECKPOINT.parent / "formalization-workbench"

DRYRUN_DIR = POST_CHECKPOINT / "runs" / "20260531-122858-cosmo-SN-BAO-closure-dryrun"

SN_PATH = WORKBENCH / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat"
BAO_DR2_MEAN = WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_DR2_COV = WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
BAO_DR1_MEAN = WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_DR1_COV = WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt"

SOURCE_PATHS = {
    "83_empirical_manifest": Path("83-empirical-closure-test-manifest.md"),
    "84_runner_design": Path("84-closure-test-runner-design.md"),
    "85_dryrun_readout": Path("85-cosmo-SN-BAO-closure-runner-dryrun.md"),
    "85_dryrun_status": Path("runs/20260531-122858-cosmo-SN-BAO-closure-dryrun/status.json"),
    "85_dryrun_schema": Path("runs/20260531-122858-cosmo-SN-BAO-closure-dryrun/results/data_schema_report.csv"),
    "85_dryrun_model_matrix": Path("runs/20260531-122858-cosmo-SN-BAO-closure-dryrun/results/model_matrix.csv"),
    "85_dryrun_amplitude_policy": Path("runs/20260531-122858-cosmo-SN-BAO-closure-dryrun/results/amplitude_policy.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    for key, absolute_path in {
        "SN_primary": SN_PATH,
        "BAO_DR2_primary_mean": BAO_DR2_MEAN,
        "BAO_DR2_primary_cov": BAO_DR2_COV,
        "BAO_DR1_robustness_mean": BAO_DR1_MEAN,
        "BAO_DR1_robustness_cov": BAO_DR1_COV,
    }.items():
        rows.append(
            {
                "source_key": key,
                "relative_path": "",
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def frozen_data_rows() -> list[dict[str, Any]]:
    return [
        {
            "dataset": "SN_primary",
            "role": "primary",
            "path": str(SN_PATH),
            "branch": "PantheonPlus_SH0ES_file_shape_plus_offset",
            "short_smoke_use": "shape_with_nuisance_offset; no field-theory claim",
        },
        {
            "dataset": "BAO_primary",
            "role": "primary",
            "path": str(BAO_DR2_MEAN),
            "paired_covariance": str(BAO_DR2_COV),
            "branch": "DESI_DR2_GCcomb_mean_cov",
            "short_smoke_use": "primary BAO distance vector",
        },
        {
            "dataset": "BAO_robustness",
            "role": "robustness",
            "path": str(BAO_DR1_MEAN),
            "paired_covariance": str(BAO_DR1_COV),
            "branch": "DESI_DR1_2024_GCcomb_mean_cov",
            "short_smoke_use": "not used in first short smoke unless explicitly selected",
        },
    ]


def fit_phase_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "explicit_dry_run",
            "command": "python scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run --sn-data <SN_PATH> --bao-data <BAO_DR2_MEAN>",
            "must_pass_before": "short_smoke",
            "scores_allowed": False,
        },
        {
            "phase": "short_smoke",
            "command": "python scripts/cosmo_SN_BAO_closure_runner.py --phase short-smoke --sn-data <SN_PATH> --bao-data <BAO_DR2_MEAN> --bao-cov <BAO_DR2_COV> --max-iter 200",
            "must_pass_before": "robustness",
            "scores_allowed": True,
        },
        {
            "phase": "DR1_robustness",
            "command": "same short-smoke command with DR1 mean/cov paths",
            "must_pass_before": "any robustness claim",
            "scores_allowed": True,
        },
    ]


def model_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_key": "LCDM",
            "role": "baseline",
            "required_in_short_smoke": True,
            "fitted_parameters": "Omega_m; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "wCDM",
            "role": "baseline",
            "required_in_short_smoke": True,
            "fitted_parameters": "Omega_m; w; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "CPL",
            "role": "baseline",
            "required_in_short_smoke": True,
            "fitted_parameters": "Omega_m; w0; wa; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "MTS_fixed_p3_u3quarter",
            "role": "primary_closure",
            "required_in_short_smoke": True,
            "fitted_parameters": "Omega_m; B_mem/b_mem; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "closure_performance_only",
        },
        {
            "model_key": "MTS_Bmem_zero",
            "role": "negative_control",
            "required_in_short_smoke": True,
            "fitted_parameters": "Omega_m; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "control",
        },
        {
            "model_key": "MTS_fitted_p",
            "role": "ablation",
            "required_in_short_smoke": "optional_if_runtime_allows_else_next",
            "fitted_parameters": "Omega_m; p; B_mem/b_mem; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "closure_ablation_only",
        },
        {
            "model_key": "MTS_fitted_u3",
            "role": "ablation",
            "required_in_short_smoke": "optional_if_runtime_allows_else_next",
            "fitted_parameters": "Omega_m; u3; B_mem/b_mem; SN_offset_or_absolute_nuisance",
            "claim_ceiling": "closure_ablation_only",
        },
    ]


def prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": "Omega_m",
            "models": "all",
            "short_smoke_prior": "0.05 <= Omega_m <= 0.6",
            "edge_rule": "distance_to_edge < 1 percent of prior width flags unstable",
        },
        {
            "parameter": "B_mem/b_mem",
            "models": "MTS_fixed_p3_u3quarter; MTS_fitted_p; MTS_fitted_u3",
            "short_smoke_prior": "symmetric finite prior must be written in run_config before scoring",
            "edge_rule": "any edge hit blocks stable-evidence language",
        },
        {
            "parameter": "p",
            "models": "MTS_fitted_p only",
            "short_smoke_prior": "1 <= p <= 6",
            "edge_rule": "edge hit means p=3 ablation inconclusive",
        },
        {
            "parameter": "u3",
            "models": "MTS_fitted_u3 only",
            "short_smoke_prior": "0.05 <= u3 <= 1.0",
            "edge_rule": "edge hit means quarter-lock ablation inconclusive",
        },
        {
            "parameter": "SN_offset_or_absolute_nuisance",
            "models": "all SN branches",
            "short_smoke_prior": "analytic or fitted nuisance; same treatment for all models",
            "edge_rule": "not a theory parameter but must be reported",
        },
    ]


def output_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "fit_summary.csv",
            "required": True,
            "required_columns": "model; chi2_SN; chi2_BAO; chi2_total; dof; k; n; AIC; BIC; convergence; prior_edge_flag; claim_ceiling",
        },
        {
            "artifact": "baseline_comparison.csv",
            "required": True,
            "required_columns": "model; reference_baseline; delta_chi2; delta_AIC; delta_BIC; same_data; same_nuisance; same_calibration",
        },
        {
            "artifact": "residuals.csv",
            "required": True,
            "required_columns": "dataset; model; observable; coordinate; observed; predicted; residual; sigma_or_cov_block",
        },
        {
            "artifact": "prior_edge_table.csv",
            "required": True,
            "required_columns": "model; parameter; best_fit; lower; upper; distance_to_edge; edge_flag",
        },
        {
            "artifact": "amplitude_policy.csv",
            "required": True,
            "required_columns": "factor; treatment; prior; best_fit; edge_flag; ablation_role",
        },
        {
            "artifact": "status.json",
            "required": True,
            "required_columns": "readout; stable_evidence_allowed; scores_written; failures; next_action",
        },
    ]


def abort_rows() -> list[dict[str, Any]]:
    return [
        {
            "abort_condition": "explicit_data_dry_run_not_passed",
            "reason": "automatic candidate detection is not enough for scoring",
        },
        {
            "abort_condition": "BAO_mean_cov_shape_mismatch",
            "reason": "DESI vector and covariance must have matching dimension",
        },
        {
            "abort_condition": "baseline_missing",
            "reason": "MTS cannot be scored without LCDM/wCDM/CPL in same run",
        },
        {
            "abort_condition": "asymmetric_SN_offset",
            "reason": "SN nuisance treatment must be identical across branches",
        },
        {
            "abort_condition": "unreported_prior_edge",
            "reason": "edge-hitting can fake a result",
        },
        {
            "abort_condition": "field_theory_claim_language",
            "reason": "this is closure testing only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "short_smoke_contract_status",
            "status": "contract_ready_runner_scoring_not_implemented",
            "evidence": "explicit data paths, primary/robustness branch, model policies, priors, outputs, and aborts are frozen",
            "next_action": "extend cosmo_SN_BAO_closure_runner.py with explicit dry-run options and then short-smoke scoring",
        },
        {
            "decision": "primary_data_choice",
            "status": "PantheonPlus_SH0ES_file_plus_DESI_DR2_primary",
            "evidence": "dry-run validated Pantheon+ file and DESI DR2 mean/cov pair",
            "next_action": "rerun dry-run with explicit SN and BAO DR2 paths before scoring",
        },
        {
            "decision": "claim_status",
            "status": "no_scores_no_evidence_yet",
            "evidence": "checkpoint 86 only freezes the contract",
            "next_action": "keep empirical claims blocked until short-smoke artifacts exist",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "SN_BAO_short_smoke_contract_ready_no_scores",
        "key_metrics": {
            "frozen_data_rows": counts["frozen_data"],
            "fit_phases": counts["fit_phases"],
            "model_policies": counts["model_policy"],
            "prior_rows": counts["priors"],
            "required_outputs": counts["required_outputs"],
            "abort_conditions": counts["abort_conditions"],
        },
        "decision": decision_rows()[0],
        "next_target": "87-cosmo-SN-BAO-short-smoke-implementation.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-cosmo-SN-BAO-short-smoke-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "frozen_data": (
            frozen_data_rows(),
            ["dataset", "role", "path", "paired_covariance", "branch", "short_smoke_use"],
        ),
        "fit_phases": (
            fit_phase_rows(),
            ["phase", "command", "must_pass_before", "scores_allowed"],
        ),
        "model_policy": (
            model_policy_rows(),
            ["model_key", "role", "required_in_short_smoke", "fitted_parameters", "claim_ceiling"],
        ),
        "priors": (
            prior_rows(),
            ["parameter", "models", "short_smoke_prior", "edge_rule"],
        ),
        "required_outputs": (
            output_rows(),
            ["artifact", "required", "required_columns"],
        ),
        "abort_conditions": (
            abort_rows(),
            ["abort_condition", "reason"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=POST_CHECKPOINT / "runs")
    args = parser.parse_args()
    run_dir = run(args.output_root)
    print((run_dir / "status.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
