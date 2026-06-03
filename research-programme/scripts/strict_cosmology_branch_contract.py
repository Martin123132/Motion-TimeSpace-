#!/usr/bin/env python3
"""Lock a strict cosmology branch contract before any scoring run."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_22_STATUS = Path("runs/20260530-234358-cosmology-bridge-run-manifest/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def strict_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "strict_C0_frozen_holdout",
            "role": "primary_strict_control",
            "definition": "Use the already declared minimal smooth memory closure with background parameters frozen before growth/CMB holdout scoring.",
            "allowed_status": "preflight_allowed_scoring_requires_next_gate",
            "claim_limit": "L1_screened_or_L2_fit_direction_only",
            "hard_rejection": "If background parameters are refit on growth/CMB or if perturbation freedoms are turned on after residuals.",
        },
        {
            "branch": "strict_memory_predeclared",
            "role": "candidate_strict_MTS_branch",
            "definition": "Omega_Gamma(N)=b_mem_pre*F_pre(N), S_Gamma(N)=b_mem_pre*dF_pre/dN, with b_mem_pre and F_pre locked before data scoring.",
            "allowed_status": "contract_defined_not_numerically_instantiated",
            "claim_limit": "L2_fit_if_same-test_and_no_edges; L3_robust_only_after_holdout_survives",
            "hard_rejection": "If b_mem or F_pre is chosen after inspecting scoring residuals.",
        },
        {
            "branch": "strict_activation_predeclared",
            "role": "secondary_candidate_only",
            "definition": "Activation parameters alpha_act, nu_act, and A_act are fixed from a predeclared parent-motivated rule or excluded.",
            "allowed_status": "not_allowed_until_values_or_ranges_are_predeclared",
            "claim_limit": "L1_screened_until_parent_rule_exists",
            "hard_rejection": "If sign, width, or amplitude is selected because it improves chi2 after a failed branch.",
        },
        {
            "branch": "shape_free_M6",
            "role": "diagnostic_only",
            "definition": "Retain as a smoke-test/bug-finder branch for likelihood behavior, never as positive support.",
            "allowed_status": "dry_run_only",
            "claim_limit": "no_support_claim",
            "hard_rejection": "Any prior-edge hit, sign chase, or shape freedom used to beat baselines.",
        },
        {
            "branch": "phenomenology_full_joint",
            "role": "secondary_diagnostic",
            "definition": "Full joint refit with all declared diagnostics and identical baselines.",
            "allowed_status": "blocked_until_preflight_passes",
            "claim_limit": "pipeline_stress_test_only",
            "hard_rejection": "If it overrides the frozen holdout verdict or uses asymmetric baseline treatment.",
        },
    ]


def parameter_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": "b_mem_pre",
            "status": "predeclared_or_absent",
            "allowed_source": "parent amplitude corridor, previous locked background branch, or explicit blind prior before scoring",
            "forbidden_use": "free amplitude rescue after holdout residuals",
            "edge_rule": "edge hit blocks support",
        },
        {
            "parameter": "F_pre(N)",
            "status": "predeclared_shape_or_absent",
            "allowed_source": "locked smooth-memory shape before scoring",
            "forbidden_use": "shape sweep after seeing one-dataset tension",
            "edge_rule": "shape instability blocks support",
        },
        {
            "parameter": "alpha_act",
            "status": "fixed_rule_or_excluded",
            "allowed_source": "parent-motivated transition scale or declared blind range",
            "forbidden_use": "unpenalized fitted transition scale",
            "edge_rule": "edge hit blocks support",
        },
        {
            "parameter": "nu_act",
            "status": "fixed_rule_or_excluded",
            "allowed_source": "parent-motivated transition width/statistics or declared blind range",
            "forbidden_use": "free shape parameter used to beat CPL",
            "edge_rule": "edge hit blocks support",
        },
        {
            "parameter": "A_act",
            "status": "sign_branch_predeclared_or_excluded",
            "allowed_source": "separate sign-free and sign-constrained branches declared before scoring",
            "forbidden_use": "choosing negative or positive sign after inspecting chi2",
            "edge_rule": "edge hit or sign instability blocks support",
        },
        {
            "parameter": "c_s,Gamma^2",
            "status": "fixed_closure_equals_1",
            "allowed_source": "growth/CMB contract",
            "forbidden_use": "late-time perturbation rescue fit",
            "edge_rule": "not fitted",
        },
        {
            "parameter": "pi_Gamma",
            "status": "fixed_closure_equals_0",
            "allowed_source": "growth/CMB contract",
            "forbidden_use": "turning on anisotropic stress to patch CMB/growth",
            "edge_rule": "not fitted",
        },
        {
            "parameter": "Q_m^nu",
            "status": "fixed_closure_equals_0",
            "allowed_source": "growth/CMB contract",
            "forbidden_use": "direct exchange rescue without conservation-law derivation",
            "edge_rule": "not fitted",
        },
        {
            "parameter": "H0,Omega_m,rd,sigma8",
            "status": "baseline_symmetric_nuisance",
            "allowed_source": "same priors and covariance handling for LCDM/wCDM/CPL/MTS",
            "forbidden_use": "counting nuisance shifts as MTS derivation",
            "edge_rule": "same diagnostics as baselines",
        },
    ]


def data_split_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "split": "no_SH0ES_background",
            "strict_role": "calibration_pressure_check",
            "branch_rule": "Use Pantheon+ shape with nuisance offset and unchanged BAO treatment.",
            "pass_condition": "MTS preference, if any, does not vanish solely when local-H0 pressure is removed.",
        },
        {
            "split": "background_training",
            "strict_role": "background_prelocking_only",
            "branch_rule": "May define frozen background parameters, but cannot be called support by itself.",
            "pass_condition": "Baselines and MTS receive identical covariance, priors, and nuisance treatment.",
        },
        {
            "split": "growth_CMB_holdout",
            "strict_role": "primary_direction_test",
            "branch_rule": "No growth/CMB refit of C0 or perturbation rescue freedoms.",
            "pass_condition": "Frozen branch is not catastrophically degraded against LCDM/wCDM/CPL.",
        },
        {
            "split": "Hz_direct_stress",
            "strict_role": "shape_fragility_probe",
            "branch_rule": "Diagnostic only until H(z) covariance/source handling is locked.",
            "pass_condition": "No single H(z) subset dominates the branch verdict.",
        },
        {
            "split": "full_joint_robustness",
            "strict_role": "secondary_same-test_refit",
            "branch_rule": "Can stress-test but cannot overwrite the primary frozen holdout result.",
            "pass_condition": "No prior-edge dependence and AIC/BIC beats best baseline under same test.",
        },
    ]


def acceptance_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_22_complete",
            "status": "pass" if source.get("readout") == "cosmology_bridge_run_manifest_locked_preflight_only" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "strict_branch_contract_defined",
            "status": "pass",
            "detail": "strict_C0_frozen, strict_memory_predeclared, activation, M6 diagnostic, and full-joint diagnostic roles are separated",
        },
        {
            "gate": "shape_free_support_blocked",
            "status": "pass",
            "detail": "M6/shape-free activation remains dry-run or diagnostic only",
        },
        {
            "gate": "same_baseline_requirement",
            "status": "pass",
            "detail": "LCDM, wCDM, and CPL must receive the same priors, data, covariance, residual plots, and AIC/BIC treatment",
        },
        {
            "gate": "parent_derived_amplitude_available",
            "status": "fail",
            "detail": "b_mem magnitude is still predeclared/phenomenological, not parent-derived",
        },
        {
            "gate": "parent_derived_shape_available",
            "status": "fail",
            "detail": "F(N) or activation shape is still a closure unless locked before scoring",
        },
        {
            "gate": "parent_derived_perturbation_sector_available",
            "status": "fail",
            "detail": "c_s,Gamma^2, pi_Gamma, and Q_m^nu remain fixed closures",
        },
        {
            "gate": "preflight_allowed_now",
            "status": "pass",
            "detail": "safe to write/run parser and likelihood preflight only",
        },
        {
            "gate": "scoring_run_allowed_now",
            "status": "fail",
            "detail": "strict numerical values and command dry-run must be locked first",
        },
        {
            "gate": "empirical_claim_allowed_now",
            "status": "fail",
            "detail": "this contract is not a data result",
        },
    ]


def claim_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "contract_defined_no_data",
            "max_claim": "L0_control",
            "allowed_language": "strict branch exists as a disciplined test object",
            "forbidden_language": "MTS is favored by cosmology",
        },
        {
            "condition": "parser_preflight_passes",
            "max_claim": "L0_control",
            "allowed_language": "pipeline/data shapes are ready for a fair run",
            "forbidden_language": "evidence",
        },
        {
            "condition": "background_fit_beats_LCDM_only",
            "max_claim": "L2_fit",
            "allowed_language": "background branch fits this split better under same test",
            "forbidden_language": "unified theory support or derived cosmology",
        },
        {
            "condition": "holdout_survives_and_AIC_BIC_beats_best_baseline",
            "max_claim": "L3_robust",
            "allowed_language": "strict branch is empirically robust enough to prioritize derivation",
            "forbidden_language": "field theory proven",
        },
        {
            "condition": "parent_action_derives_amplitude_shape_and_perturbations",
            "max_claim": "L4_derived",
            "allowed_language": "cosmology branch is derived from the parent action",
            "forbidden_language": "L5 unified until local GR, EM/time, and other pillars cohere",
        },
    ]


def next_step_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "24-cosmology-preflight-execution-plan.md",
            "purpose": "turn this strict contract into a dry-run/preflight command plan without scoring claims",
            "allowed_now": True,
        },
        {
            "next_target": "strict_branch_numeric_lock",
            "purpose": "choose b_mem_pre/F_pre or exclude them before scoring",
            "allowed_now": True,
        },
        {
            "next_target": "first_scoring_run",
            "purpose": "fit/score strict branches against LCDM/wCDM/CPL",
            "allowed_now": False,
        },
        {
            "next_target": "growth_CMB_holdout_scoring",
            "purpose": "primary frozen holdout test",
            "allowed_now": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "strict_branch_status",
            "status": "contract_locked_not_promoted",
            "evidence": "fewer freedoms are defined, but amplitude/shape/perturbation derivations remain open",
            "next_action": "write a preflight execution plan and numeric lock file before scoring",
        },
        {
            "decision": "M6_status",
            "status": "diagnostic_only",
            "evidence": "shape-free activation can find bugs/tensions but cannot count as support",
            "next_action": "exclude from evidence ladder unless predeclared and edge-safe",
        },
        {
            "decision": "empirical_status",
            "status": "no_claim",
            "evidence": "no data scoring was run in this stage",
            "next_action": "parser/likelihood preflight only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict cosmology branch contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_22_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-strict-cosmology-branch-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    branches = strict_branch_rows()
    parameters = parameter_contract_rows()
    splits = data_split_contract_rows()
    gates = acceptance_gate_rows(source)
    claims = claim_ladder_rows()
    next_steps = next_step_rows()
    decisions = decision_rows()

    write_csv(results_dir / "strict_cosmology_branches.csv", branches, list(branches[0].keys()))
    write_csv(results_dir / "strict_cosmology_parameter_contract.csv", parameters, list(parameters[0].keys()))
    write_csv(results_dir / "strict_cosmology_data_split_contract.csv", splits, list(splits[0].keys()))
    write_csv(results_dir / "strict_cosmology_acceptance_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "strict_cosmology_claim_ladder.csv", claims, list(claims[0].keys()))
    write_csv(results_dir / "strict_cosmology_next_steps.csv", next_steps, list(next_steps[0].keys()))
    write_csv(results_dir / "strict_cosmology_decision.csv", decisions, list(decisions[0].keys()))

    readout = "strict_cosmology_branch_contract_locked_no_scoring_yet"
    status = {
        "status": "complete_strict_cosmology_branch_contract",
        "readout": readout,
        "recommendation": "write_cosmology_preflight_execution_plan_next",
        "next_target": "24-cosmology-preflight-execution-plan.md",
        "strict_branch_defined": True,
        "preflight_allowed_now": True,
        "scoring_run_allowed_now": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "L0_control",
        "primary_strict_branch": "strict_C0_frozen_holdout",
        "candidate_strict_branch": "strict_memory_predeclared",
        "diagnostic_only_branches": ["shape_free_M6", "phenomenology_full_joint"],
        "critical_open_items": [
            "lock_numeric_b_mem_pre_or_exclude",
            "lock_F_pre_shape_or_exclude",
            "keep_activation_parameters_predeclared_or_absent",
            "dry_run_commands_before_scoring",
            "derive_parent_amplitude_shape_perturbations_for_L4",
        ],
        "outputs": {
            "strict_cosmology_branches": str(results_dir / "strict_cosmology_branches.csv"),
            "strict_cosmology_parameter_contract": str(results_dir / "strict_cosmology_parameter_contract.csv"),
            "strict_cosmology_data_split_contract": str(results_dir / "strict_cosmology_data_split_contract.csv"),
            "strict_cosmology_acceptance_gates": str(results_dir / "strict_cosmology_acceptance_gates.csv"),
            "strict_cosmology_claim_ladder": str(results_dir / "strict_cosmology_claim_ladder.csv"),
            "strict_cosmology_next_steps": str(results_dir / "strict_cosmology_next_steps.csv"),
            "strict_cosmology_decision": str(results_dir / "strict_cosmology_decision.csv"),
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
