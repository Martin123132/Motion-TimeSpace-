#!/usr/bin/env python3
"""Design the first audited empirical closure test runner."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "26_isolated_likelihood_preflight_wrapper": Path("26-isolated-likelihood-preflight-wrapper.md"),
    "40_fresh_holdout_or_official_likelihood_roadmap": Path("40-fresh-holdout-or-official-likelihood-roadmap.md"),
    "55_u3_quarter_lock_smoke": Path("55-u3-quarter-lock-smoke.md"),
    "82_amplitude_normalization_gate": Path("82-amplitude-normalization-gate.md"),
    "83_empirical_closure_test_manifest": Path("83-empirical-closure-test-manifest.md"),
    "83_test_manifest": Path("runs/20260531-121628-empirical-closure-test-manifest/results/test_manifest.csv"),
    "83_amplitude_policy": Path("runs/20260531-121628-empirical-closure-test-manifest/results/amplitude_policy.csv"),
    "83_baseline_fairness": Path("runs/20260531-121628-empirical-closure-test-manifest/results/baseline_fairness.csv"),
    "83_output_contract": Path("runs/20260531-121628-empirical-closure-test-manifest/results/output_contract.csv"),
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
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def runner_phase_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "dry_run_manifest",
            "purpose": "validate data paths, schemas, model grid, amplitude policy, baseline parity, and output directories",
            "writes_scores": False,
            "allowed_runtime": "seconds",
            "abort_if": "missing data; malformed schema; missing baseline; amplitude policy absent",
        },
        {
            "phase": "short_smoke",
            "purpose": "fit only the minimal SN+BAO closure matrix with low iteration caps",
            "writes_scores": True,
            "allowed_runtime": "minutes_not_hours",
            "abort_if": "nonconvergence unlabelled; prior edge unreported; residuals absent",
        },
        {
            "phase": "robustness_matrix",
            "purpose": "run wide/narrow priors, fitted-p/u3 ablations, split tests, and no-SH0ES branch",
            "writes_scores": True,
            "allowed_runtime": "long_run_only_with_log_status_marker",
            "abort_if": "no log/status/complete marker; baselines not rerun under same split",
        },
        {
            "phase": "promotion_review",
            "purpose": "read results and decide whether closure has stable empirical support",
            "writes_scores": False,
            "allowed_runtime": "review_only",
            "abort_if": "edge-hit model treated as evidence; closure result called field theory proof",
        },
    ]


def model_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_key": "LCDM",
            "role": "baseline",
            "fixed_factors": "none beyond standard model definition",
            "fitted_factors": "Omega_m; nuisance offset/calibration as branch requires",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "wCDM",
            "role": "baseline",
            "fixed_factors": "constant w model form",
            "fitted_factors": "Omega_m; w; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "CPL",
            "role": "baseline",
            "fixed_factors": "CPL form w(a)=w0+wa(1-a)",
            "fitted_factors": "Omega_m; w0; wa; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
        },
        {
            "model_key": "MTS_fixed_p3_u3quarter",
            "role": "primary_closure",
            "fixed_factors": "p=3; u3=1/4",
            "fitted_factors": "B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "primary",
            "claim_ceiling": "closure_performance_only",
        },
        {
            "model_key": "MTS_fitted_p",
            "role": "ablation",
            "fixed_factors": "u3=1/4",
            "fitted_factors": "p; B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "required_short_or_robustness",
            "claim_ceiling": "closure_ablation_only",
        },
        {
            "model_key": "MTS_fitted_u3",
            "role": "ablation",
            "fixed_factors": "p=3",
            "fitted_factors": "u3; B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "required_short_or_robustness",
            "claim_ceiling": "closure_ablation_only",
        },
        {
            "model_key": "MTS_Bmem_zero",
            "role": "negative_control",
            "fixed_factors": "p=3; u3=1/4; B_mem=0",
            "fitted_factors": "Omega_m; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "control",
        },
    ]


def data_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "dataset": "SN_shape",
            "required_state": "local_path_or_download_manifest",
            "schema_check": "redshift/value/covariance_or_sigma/nuisance_offset_columns",
            "dry_run_action": "count rows and validate finite numeric columns",
            "notes": "Pantheon+ shape branch preferred before any local-H0 pressure claim",
        },
        {
            "dataset": "BAO_distances",
            "required_state": "local_path_or_download_manifest",
            "schema_check": "z; observable; value; covariance_or_sigma; survey_tag",
            "dry_run_action": "count rows and validate no duplicate incompatible covariance use",
            "notes": "DESI/BAO unchanged branch; do not double-count BAO-plus/full-shape alternatives",
        },
        {
            "dataset": "run_config",
            "required_state": "generated_in_run_dir",
            "schema_check": "model grid; priors; fixed/fitted flags; baseline parity flags",
            "dry_run_action": "write before scoring and freeze hash/checksum",
            "notes": "prevents changing rules after seeing scores",
        },
    ]


def output_artifact_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "status.json",
            "phase": "all",
            "required_fields": "readout; phase; stable_evidence_allowed; failures; next_action; created_at",
        },
        {
            "artifact": "run_config.json",
            "phase": "dry_run_manifest",
            "required_fields": "models; priors; data_paths; amplitude_policy; baseline_rules; frozen_before_fit",
        },
        {
            "artifact": "fit_summary.csv",
            "phase": "short_smoke_and_later",
            "required_fields": "model; chi2; dof; k; n; AIC; BIC; convergence; prior_edge_flag; claim_ceiling",
        },
        {
            "artifact": "amplitude_policy.csv",
            "phase": "all",
            "required_fields": "factor; treatment; prior; best_fit; edge_flag; ablation_role",
        },
        {
            "artifact": "baseline_comparison.csv",
            "phase": "short_smoke_and_later",
            "required_fields": "model; baseline; same_data; same_nuisance; same_calibration; delta_chi2; delta_AIC; delta_BIC",
        },
        {
            "artifact": "residuals.csv",
            "phase": "short_smoke_and_later",
            "required_fields": "dataset; model; observable; coordinate; observed; predicted; residual; sigma_or_cov_block",
        },
        {
            "artifact": "prior_edge_table.csv",
            "phase": "short_smoke_and_later",
            "required_fields": "model; parameter; best_fit; lower; upper; distance_to_edge; edge_flag",
        },
        {
            "artifact": "log.txt",
            "phase": "long_run",
            "required_fields": "plain text command, environment, phase, progress, failures",
        },
        {
            "artifact": "COMPLETE.txt",
            "phase": "long_run",
            "required_fields": "written only after successful run completion",
        },
    ]


def command_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "command_name": "dry_run",
            "example": "python scripts/cosmo_SN_BAO_closure_runner.py --phase dry-run --output-root runs",
            "allowed_to_fit": False,
            "required_outputs": "status.json; run_config.json; amplitude_policy.csv",
        },
        {
            "command_name": "short_smoke",
            "example": "python scripts/cosmo_SN_BAO_closure_runner.py --phase short-smoke --max-iter 200 --output-root runs",
            "allowed_to_fit": True,
            "required_outputs": "fit_summary.csv; baseline_comparison.csv; residuals.csv; prior_edge_table.csv; status.json",
        },
        {
            "command_name": "long_robustness",
            "example": "python scripts/cosmo_SN_BAO_closure_runner.py --phase robustness --output-root runs *> runs/<timestamp>/log.txt",
            "allowed_to_fit": True,
            "required_outputs": "log.txt; status.json; COMPLETE.txt plus all short-smoke outputs",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "closure_runner_design_status",
            "status": "design_ready_runner_not_implemented",
            "evidence": "phases, model matrix, data contracts, outputs, and commands are specified",
            "next_action": "implement scripts/cosmo_SN_BAO_closure_runner.py dry-run mode first",
        },
        {
            "decision": "first_execution_allowed",
            "status": "dry_run_only",
            "evidence": "data path state has not been verified in a runner yet",
            "next_action": "no scoring until dry-run validates schemas and output contract",
        },
        {
            "decision": "claim_status",
            "status": "closure_test_design_only",
            "evidence": "no SN+BAO scores produced in this checkpoint",
            "next_action": "keep field-theory claims blocked",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "closure_runner_design_ready_runner_not_implemented",
        "key_metrics": {
            "runner_phases": counts["runner_phases"],
            "model_matrix_rows": counts["model_matrix"],
            "data_contract_rows": counts["data_contract"],
            "output_artifacts": counts["output_artifacts"],
            "command_contracts": counts["command_contract"],
        },
        "decision": decision_rows()[0],
        "next_target": "85-cosmo-SN-BAO-closure-runner-dryrun.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-closure-test-runner-design"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "runner_phases": (
            runner_phase_rows(),
            ["phase", "purpose", "writes_scores", "allowed_runtime", "abort_if"],
        ),
        "model_matrix": (
            model_matrix_rows(),
            ["model_key", "role", "fixed_factors", "fitted_factors", "ablation_status", "claim_ceiling"],
        ),
        "data_contract": (
            data_contract_rows(),
            ["dataset", "required_state", "schema_check", "dry_run_action", "notes"],
        ),
        "output_artifacts": (
            output_artifact_rows(),
            ["artifact", "phase", "required_fields"],
        ),
        "command_contract": (
            command_contract_rows(),
            ["command_name", "example", "allowed_to_fit", "required_outputs"],
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
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
