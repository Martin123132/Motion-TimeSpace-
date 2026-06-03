#!/usr/bin/env python3
"""Create a safe cosmology bridge run manifest before any long execution."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_21_STATUS = Path("runs/20260530-234037-cosmology-parent-bridge-audit/status.json")
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def model_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "parameter_labels": "H0:fitted_nuisance; Omega_m:fitted_nuisance; rd:fitted_or_prior_nuisance; sigma8:fitted_nuisance_if_growth",
            "allowed": True,
            "claim_limit": "baseline_only",
        },
        {
            "model": "wCDM",
            "role": "baseline",
            "parameter_labels": "w:fitted_extension; standard nuisances:fitted",
            "allowed": True,
            "claim_limit": "baseline_only",
        },
        {
            "model": "CPL",
            "role": "baseline",
            "parameter_labels": "w0,wa:fitted_extension; standard nuisances:fitted",
            "allowed": True,
            "claim_limit": "baseline_only",
        },
        {
            "model": "C0_minimal_smooth_memory",
            "role": "MTS_closure_benchmark",
            "parameter_labels": "b_mem:phenomenological_amplitude; F(N):closure_shape; c_s^2=1:closure; pi_Gamma=0:closure; Q_m=0:closure",
            "allowed": True,
            "claim_limit": "L0_control_or_L1_screened_only",
        },
        {
            "model": "C0_frozen_background_holdout",
            "role": "primary_holdout_candidate",
            "parameter_labels": "background frozen from prior branch; growth/CMB not refit",
            "allowed": True,
            "claim_limit": "holdout_direction_test_not_support",
        },
        {
            "model": "M6_or_shape_free_activation",
            "role": "fragile_phenomenology",
            "parameter_labels": "alpha_act,nu_act,A_act,b_mem:phenomenological/fitted unless predeclared",
            "allowed": "dry_run_only",
            "claim_limit": "no_support_if_prior_edge_or_shape_free",
        },
        {
            "model": "strict_future_MTS_branch",
            "role": "future_candidate",
            "parameter_labels": "shape/amplitude must be predeclared or parent-derived",
            "allowed": "not_until_defined",
            "claim_limit": "not_existing_yet",
        },
    ]


def dataset_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split": "background_training",
            "datasets": "Pantheon+/SN shape; BAO background",
            "use": "define or compare background expansion",
            "rule": "same nuisance/covariance treatment for all models",
        },
        {
            "split": "no_SH0ES_background",
            "datasets": "Pantheon+ shape with nuisance offset; BAO unchanged",
            "use": "test whether preference survives without local-H0 calibration pressure",
            "rule": "reported separately from SH0ES-calibrated branch",
        },
        {
            "split": "growth_CMB_holdout",
            "datasets": "f_sigma8/growth plus compressed CMB distance diagnostics",
            "use": "primary holdout for frozen C0 branch",
            "rule": "no growth/CMB refit in primary holdout",
        },
        {
            "split": "Hz_direct_stress",
            "datasets": "H(z) covariance branch",
            "use": "stress H(z) shape and BAO/DH fragility",
            "rule": "diagnostic only unless covariance handling is locked",
        },
        {
            "split": "full_joint_robustness",
            "datasets": "background plus growth/CMB with same treatment across all models",
            "use": "secondary robustness refit",
            "rule": "cannot overwrite primary holdout verdict",
        },
    ]


def parameter_label_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": "b_mem",
            "label": "meaning_derived_magnitude_phenomenological",
            "edge_rule": "report shifts; no support if amplitude unstable",
            "parent_gate": "derive eta,a_F,DeltaR",
        },
        {
            "parameter": "F(N)",
            "label": "closure_shape",
            "edge_rule": "predeclare shape before fit",
            "parent_gate": "derive transition shape from memory dynamics",
        },
        {
            "parameter": "alpha_act",
            "label": "fitted_shape_or_transition_scale",
            "edge_rule": "prior-edge flag blocks support",
            "parent_gate": "derive from memory-domain ensemble",
        },
        {
            "parameter": "nu_act",
            "label": "fitted_shape_parameter",
            "edge_rule": "prior-edge flag blocks support",
            "parent_gate": "derive from field statistics",
        },
        {
            "parameter": "A_act",
            "label": "phenomenological_amplitude",
            "edge_rule": "test sign-free and sign-constrained; edge flag blocks support",
            "parent_gate": "derive source normalization",
        },
        {
            "parameter": "c_s,Gamma^2",
            "label": "fixed_closure_1",
            "edge_rule": "must not refit after growth/CMB residuals",
            "parent_gate": "derive perturbation action",
        },
        {
            "parameter": "pi_Gamma",
            "label": "fixed_closure_0",
            "edge_rule": "turning on is rescue unless predeclared",
            "parent_gate": "derive anisotropic stress sector",
        },
        {
            "parameter": "Q_m^nu",
            "label": "fixed_closure_0",
            "edge_rule": "turning on is rescue unless conservation law derives it",
            "parent_gate": "derive matter-memory exchange current",
        },
        {
            "parameter": "H0,Omega_m,rd,sigma8",
            "label": "fitted_nuisance_or_dataset_calibration",
            "edge_rule": "same priors for baselines and MTS branches",
            "parent_gate": "none for immediate empirical comparison",
        },
    ]


def command_manifest_rows() -> list[dict[str, Any]]:
    candidates = [
        ("bridge_manifest_only", "post-checkpoint-work/scripts/cosmology_bridge_run_manifest.py", "already_run", "safe_manifest"),
        ("data_source_audit", "formalization-workbench/scripts/growth_CMB_data_source_audit.py", "short", "audit_only_no_fit"),
        ("parser_smoke", "formalization-workbench/scripts/growth_CMB_parser_smoke_dry_run.py", "short", "dry_run_no_model_score"),
        ("likelihood_preflight", "formalization-workbench/scripts/growth_CMB_likelihood_preflight.py", "short", "preflight_only"),
        ("first_scoring_run", "formalization-workbench/scripts/growth_CMB_first_scoring_run.py", "medium", "requires_manifest_approval"),
        ("full_joint_radflat", "formalization-workbench/scripts/full_joint_radflat_phenomenology_fit.py", "medium_or_long", "secondary_only"),
        ("cosmology_likelihood_smoke", "formalization-workbench/scripts/cosmology_likelihood_smoke.py", "medium_or_long", "robustness_matrix_only"),
    ]
    rows: list[dict[str, Any]] = []
    for run_id, rel_path, duration, permission in candidates:
        full_path = (MAIN_WORKBENCH.parent / rel_path).resolve()
        rows.append(
            {
                "run_id": run_id,
                "script_path": str(full_path),
                "exists": full_path.exists(),
                "duration_class": duration,
                "permission_status": permission,
                "allowed_now": run_id in {"bridge_manifest_only", "data_source_audit", "parser_smoke", "likelihood_preflight"},
            }
        )
    return rows


def output_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "output_file": "status.json",
            "required_fields": "readout; claim_label; model_list; data_split; prior_edge_flags; baseline_same_test_done",
            "purpose": "machine-readable verdict",
        },
        {
            "output_file": "model_scores.csv",
            "required_fields": "model; chi2; k; n; AIC; BIC; delta_AIC_vs_best_baseline; delta_BIC_vs_best_baseline",
            "purpose": "fair model comparison",
        },
        {
            "output_file": "parameter_labels.csv",
            "required_fields": "parameter; label; prior; edge_flag; parent_gate",
            "purpose": "prevent fitted-to-derived relabeling",
        },
        {
            "output_file": "residuals_by_dataset.csv",
            "required_fields": "model; dataset; point_id; z; observable; residual; normalized_residual",
            "purpose": "find one-dataset or one-point domination",
        },
        {
            "output_file": "robustness_diagnostics.csv",
            "required_fields": "model; split; jackknife; prior_variant; baseline_same_test; verdict",
            "purpose": "robustness and shared-tension accounting",
        },
        {
            "output_file": "claim_ladder_verdict.csv",
            "required_fields": "model; max_claim_level; reason; forbidden_upgrades",
            "purpose": "keeps results private/accurate",
        },
    ]


def acceptance_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_21_complete",
            "status": "pass" if source.get("readout") == "cosmology_parent_bridge_mapped_not_derived_no_long_run" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "models_and_labels_locked",
            "status": "pass",
            "detail": "baselines, C0, M6/activation, and strict future branch labels are listed",
        },
        {
            "gate": "data_splits_locked",
            "status": "pass",
            "detail": "background, no-SH0ES, growth/CMB, Hz, and full-joint branches separated",
        },
        {
            "gate": "output_contract_locked",
            "status": "pass",
            "detail": "required status/scores/labels/residuals/robustness outputs defined",
        },
        {
            "gate": "long_run_allowed_now",
            "status": "fail",
            "detail": "only audit/preflight/smoke steps allowed without explicit next approval",
        },
        {
            "gate": "empirical_claim_allowed",
            "status": "fail",
            "detail": "manifest is not data evidence",
        },
        {
            "gate": "main_workbench_mutation_allowed",
            "status": "fail",
            "detail": "manifest remains post-checkpoint only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "manifest_status",
            "status": "locked_for_safe_preflight",
            "evidence": "models, labels, splits, command classes, and outputs are explicit",
            "next_action": "run only allowed preflight/smoke or write strict branch contract",
        },
        {
            "decision": "long_run_status",
            "status": "not_allowed_yet",
            "evidence": "full scoring/robustness requires explicit approval and manifest adherence",
            "next_action": "start with dry-run/preflight if continuing empirically",
        },
        {
            "decision": "next_target",
            "status": "strict_cosmology_branch_or_preflight",
            "evidence": "current C0 is closure-only; strict branch could reduce amplitude freedom",
            "next_action": "create 23-strict-cosmology-branch-contract.md or run preflight only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cosmology bridge run manifest.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_21_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-cosmology-bridge-run-manifest"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    models = model_rows()
    splits = dataset_split_rows()
    labels = parameter_label_rows()
    commands = command_manifest_rows()
    outputs = output_contract_rows()
    gates = acceptance_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "cosmology_models_manifest.csv", models, list(models[0].keys()))
    write_csv(results_dir / "cosmology_data_splits_manifest.csv", splits, list(splits[0].keys()))
    write_csv(results_dir / "cosmology_parameter_label_manifest.csv", labels, list(labels[0].keys()))
    write_csv(results_dir / "cosmology_command_manifest.csv", commands, list(commands[0].keys()))
    write_csv(results_dir / "cosmology_output_contract.csv", outputs, list(outputs[0].keys()))
    write_csv(results_dir / "cosmology_manifest_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "cosmology_manifest_decision.csv", decisions, list(decisions[0].keys()))

    readout = "cosmology_bridge_run_manifest_locked_preflight_only"
    status = {
        "status": "complete_cosmology_bridge_run_manifest",
        "readout": readout,
        "recommendation": "preflight_only_or_define_strict_branch_next",
        "next_target": "23-strict-cosmology-branch-contract.md",
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "allowed_now": [
            row["run_id"] for row in commands if row["allowed_now"] is True
        ],
        "blocked_long_runs": [
            row["run_id"] for row in commands if row["allowed_now"] is not True
        ],
        "outputs": {
            "cosmology_models_manifest": str(results_dir / "cosmology_models_manifest.csv"),
            "cosmology_data_splits_manifest": str(results_dir / "cosmology_data_splits_manifest.csv"),
            "cosmology_parameter_label_manifest": str(results_dir / "cosmology_parameter_label_manifest.csv"),
            "cosmology_command_manifest": str(results_dir / "cosmology_command_manifest.csv"),
            "cosmology_output_contract": str(results_dir / "cosmology_output_contract.csv"),
            "cosmology_manifest_gates": str(results_dir / "cosmology_manifest_gates.csv"),
            "cosmology_manifest_decision": str(results_dir / "cosmology_manifest_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
