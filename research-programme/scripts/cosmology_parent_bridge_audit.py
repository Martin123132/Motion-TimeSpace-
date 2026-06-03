#!/usr/bin/env python3
"""Audit how cosmology variables bridge to the post-checkpoint parent skeleton."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_20_STATUS = Path("runs/20260530-233654-empirical-pillar-test-queue/status.json")
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"

SOURCE_FILES = {
    "C0_demotion": MAIN_WORKBENCH / "176-C0-radflat-demotion-decision.md",
    "parent_amplitude_attempt": MAIN_WORKBENCH / "178-parent-amplitude-theorem-attempt.md",
    "growth_CMB_contract": MAIN_WORKBENCH / "157-minimal-smooth-memory-growth-CMB-test-contract.md",
    "bmem_boundary_law": MAIN_WORKBENCH / "174-bmem-parent-boundary-law.md",
    "variable_audit": MAIN_WORKBENCH / "04-variable-audit.csv",
    "unification_spine": MAIN_WORKBENCH / "07-unification-spine.md",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": {
                "C0_demotion": "locks C0 as closure benchmark, not support",
                "parent_amplitude_attempt": "shows amplitude corridor but no prediction",
                "growth_CMB_contract": "locks growth/CMB holdout rules and claim limits",
                "bmem_boundary_law": "derives b_mem meaning/source integral but demotes magnitude",
                "variable_audit": "canonical cosmology variable registry",
                "unification_spine": "long-form status spine and prior warnings",
            }[source_id],
        }
        for source_id, path in SOURCE_FILES.items()
    ]


def variable_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "cosmology_variable": "C(t)",
            "parent_skeleton_hook": "C(x), S_load",
            "current_status": "target_not_derived",
            "evidence": "parent skeleton requires C^2 local limit and cosmology memory bridge",
            "claim_level": "L0_or_L1_only",
            "next_action": "derive homogeneous FLRW equation from S_load/S_cosmo_memory",
        },
        {
            "cosmology_variable": "M_cosmo_or_memory",
            "parent_skeleton_hook": "M_cosmo_or_memory, S_cosmo_memory",
            "current_status": "placeholder_not_action_derived",
            "evidence": "stage 19 labels memory sector placeholder",
            "claim_level": "L0_contract",
            "next_action": "map M to Gamma_eff/Omega_Gamma or declare phenomenological",
        },
        {
            "cosmology_variable": "Omega_Gamma(z)",
            "parent_skeleton_hook": "memory trace projection / cosmology bridge",
            "current_status": "closure_variable",
            "evidence": "b_mem boundary law defines endpoint contrast",
            "claim_level": "L1_screened_if_tests_pass",
            "next_action": "derive from action variation, not fitted expansion ansatz",
        },
        {
            "cosmology_variable": "b_mem",
            "parent_skeleton_hook": "integrated memory-source budget",
            "current_status": "meaning_derived_magnitude_phenomenological",
            "evidence": "b_mem=Omega_Gamma,inf-Omega_Gamma0 and integral S_Gamma dN derive; magnitude does not",
            "claim_level": "L1_screened_not_L4",
            "next_action": "derive eta, a_F, DeltaR or keep as calibrated amplitude",
        },
        {
            "cosmology_variable": "F(N)",
            "parent_skeleton_hook": "memory transition shape in S_cosmo_memory",
            "current_status": "shape_closure",
            "evidence": "Weibull/smooth law used to define S_Gamma source",
            "claim_level": "L0_control_or_L1_screened",
            "next_action": "derive transition shape from parent invariant or predeclare before fitting",
        },
        {
            "cosmology_variable": "S_Gamma(N)",
            "parent_skeleton_hook": "source term in memory equation",
            "current_status": "identity_derived_given_F",
            "evidence": "S_Gamma=dOmega_Gamma/dN=b_mem dF/dN",
            "claim_level": "L4_only_for_identity_not_shape",
            "next_action": "derive F(N) and amplitude budget",
        },
        {
            "cosmology_variable": "alpha_act",
            "parent_skeleton_hook": "transition scale / equality delay",
            "current_status": "fitted_or_shape_parameter",
            "evidence": "variable audit flags alpha_activation as fitted and symbol-conflicting",
            "claim_level": "L1_or_L2_only",
            "next_action": "rename consistently and derive from memory-domain ensemble or freeze predeclared value",
        },
        {
            "cosmology_variable": "nu_act",
            "parent_skeleton_hook": "transition distribution shape",
            "current_status": "fitted_shape_parameter",
            "evidence": "variable audit says not derived from field statistics",
            "claim_level": "L1_or_L2_only",
            "next_action": "derive from memory-domain statistics or carry AIC/BIC penalty",
        },
        {
            "cosmology_variable": "A_act",
            "parent_skeleton_hook": "activation amplitude / source normalization",
            "current_status": "phenomenological_until_parent_law",
            "evidence": "prior-edge robustness plan warns sign and priors need testing",
            "claim_level": "L1_or_L2_only",
            "next_action": "test sign-constrained and sign-free branches with edge flags",
        },
        {
            "cosmology_variable": "c_s,Gamma^2",
            "parent_skeleton_hook": "perturbation sector of S_cosmo_memory",
            "current_status": "fixed_closure_equals_1",
            "evidence": "growth/CMB contract locks c_s,Gamma^2=1",
            "claim_level": "L0_control",
            "next_action": "do not refit after seeing growth/CMB residuals",
        },
        {
            "cosmology_variable": "pi_Gamma",
            "parent_skeleton_hook": "anisotropic stress / tensor memory sector",
            "current_status": "fixed_closure_zero",
            "evidence": "growth/CMB contract locks pi_Gamma=0",
            "claim_level": "L0_control",
            "next_action": "do not turn on as rescue without perturbation action",
        },
        {
            "cosmology_variable": "Q_m^nu",
            "parent_skeleton_hook": "matter-memory exchange current",
            "current_status": "fixed_closure_zero",
            "evidence": "growth/CMB contract locks Q_m^nu=0",
            "claim_level": "L0_control",
            "next_action": "no direct exchange rescue without parent conservation law",
        },
        {
            "cosmology_variable": "H0,Omega_m0,rd,sigma8_0",
            "parent_skeleton_hook": "nuisance/background calibration",
            "current_status": "fitted_dataset_parameters",
            "evidence": "full-joint fits shift H0, omega_m, rd, sigma8 with branch choices",
            "claim_level": "L2_fit_only",
            "next_action": "always compare same priors and baselines; never count as MTS derivation",
        },
    ]


def branch_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "C0_minimal_smooth_memory",
            "status": "closure_benchmark",
            "usable_next": "yes_as_holdout_contract",
            "blocked_claim": "parent_derivation_or_support",
            "reason": "C0 is demoted; b_mem amplitude not stable/predicted",
        },
        {
            "branch": "M6_or_activation_shape",
            "status": "fragile_phenomenology",
            "usable_next": "only_after_bridge_labels_and_edge_rules",
            "blocked_claim": "evidence_or_parent_shape",
            "reason": "shape/amplitude parameters not parent-derived and prior edges were a concern",
        },
        {
            "branch": "growth_CMB_holdout",
            "status": "contract_locked",
            "usable_next": "data-source/bridge audit before fit",
            "blocked_claim": "growth_CMB_refit_support",
            "reason": "primary split forbids growth/CMB refit and rescue perturbation freedoms",
        },
        {
            "branch": "full_joint_radflat",
            "status": "near_competitive_but_closure_only",
            "usable_next": "diagnostic only",
            "blocked_claim": "support",
            "reason": "AIC/BIC near baseline but b_mem shifts by factor about 6",
        },
        {
            "branch": "strict_future_branch",
            "status": "needed",
            "usable_next": "define after bridge audit",
            "blocked_claim": "not_yet_existing",
            "reason": "must reduce amplitude freedom or derive it from parent action",
        },
    ]


def robustness_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "label_every_parameter",
            "requirement": "derived/postulated/closure/phenomenological/fitted_nuisance",
            "why": "prevents fitted closures becoming theory claims",
        },
        {
            "rule": "same_baselines",
            "requirement": "LCDM, wCDM, CPL get same data, priors, covariance, and diagnostics",
            "why": "prevents baseline asymmetry",
        },
        {
            "rule": "edge_flags_block_support",
            "requirement": "prior-edge branch cannot be stable evidence",
            "why": "prevents prior-chasing",
        },
        {
            "rule": "holdout_split_respected",
            "requirement": "growth/CMB holdout does not refit C0 closure parameters in primary test",
            "why": "tests prediction direction rather than rescue freedom",
        },
        {
            "rule": "no_parent_language",
            "requirement": "closure success cannot be called parent derivation",
            "why": "parent bridge is still open",
        },
        {
            "rule": "no_long_run_before_bridge",
            "requirement": "cosmology robustness run waits until this bridge audit is locked",
            "why": "saves compute and prevents ambiguous outputs",
        },
    ]


def next_command_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_step": "bridge_label_patch",
            "allowed": True,
            "action": "write a parameter-label manifest for existing cosmology scripts",
            "not_allowed": "main workbench mutation without explicit promotion",
        },
        {
            "next_step": "growth_CMB_data_run",
            "allowed": "conditional",
            "action": "only after source/covariance manifest and bridge labels are verified",
            "not_allowed": "C0 growth/CMB refit in the primary holdout",
        },
        {
            "next_step": "full_joint_cosmology_robustness",
            "allowed": "conditional",
            "action": "same-test matrix for LCDM/wCDM/CPL/C0 or strict branch",
            "not_allowed": "prior-edge or one-dataset win language",
        },
        {
            "next_step": "strict_branch_definition",
            "allowed": True,
            "action": "define branch with fewer amplitude freedoms or parent-predeclared shape",
            "not_allowed": "more free rescue parameters",
        },
        {
            "next_step": "public_claim",
            "allowed": False,
            "action": "none",
            "not_allowed": "any support/unification claim from current cosmology bridge",
        },
    ]


def bridge_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_20_complete",
            "status": "pass" if source.get("readout") == "empirical_pillar_test_queue_ready_no_claims" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "main_sources_exist",
            "status": "pass" if all(row["exists"] for row in source_rows()) else "fail",
            "detail": "required cosmology status files checked",
        },
        {
            "gate": "variables_mapped_to_parent_hooks",
            "status": "pass",
            "detail": "C/M/b_mem/F/S_Gamma/activation/perturbation/nuisance variables classified",
        },
        {
            "gate": "parent_derived_cosmology_available",
            "status": "fail",
            "detail": "amplitude, shape, perturbation sector, and FLRW bridge remain open",
        },
        {
            "gate": "long_run_allowed_now",
            "status": "fail",
            "detail": "bridge labels must be turned into a run manifest before long cosmology execution",
        },
        {
            "gate": "empirical_claim_allowed",
            "status": "fail",
            "detail": "this is a bridge audit, not a data result",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "cosmology_bridge_status",
            "status": "mapped_but_not_derived",
            "evidence": "b_mem meaning derives but magnitude/shape/perturbation bridge remain open",
            "next_action": "write 22-cosmology-bridge-run-manifest.md",
        },
        {
            "decision": "first_cosmology_run_status",
            "status": "not_yet",
            "evidence": "run manifest and parameter labels must be locked first",
            "next_action": "prepare dry-run manifest before compute",
        },
        {
            "decision": "C0_status",
            "status": "closure_benchmark_only",
            "evidence": "C0 demoted; parent amplitude only corridor, not prediction",
            "next_action": "use as holdout benchmark, not support",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cosmology parent-bridge audit.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_20_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-cosmology-parent-bridge-audit"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    variables = variable_bridge_rows()
    branches = branch_status_rows()
    rules = robustness_rule_rows()
    command_contract = next_command_contract_rows()
    gates = bridge_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "cosmology_bridge_sources.csv", sources, list(sources[0].keys()))
    write_csv(results_dir / "cosmology_variable_parent_bridge.csv", variables, list(variables[0].keys()))
    write_csv(results_dir / "cosmology_branch_status.csv", branches, list(branches[0].keys()))
    write_csv(results_dir / "cosmology_robustness_rules.csv", rules, list(rules[0].keys()))
    write_csv(results_dir / "cosmology_next_command_contract.csv", command_contract, list(command_contract[0].keys()))
    write_csv(results_dir / "cosmology_bridge_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "cosmology_bridge_decision.csv", decisions, list(decisions[0].keys()))

    readout = "cosmology_parent_bridge_mapped_not_derived_no_long_run"
    status = {
        "status": "complete_cosmology_parent_bridge_audit",
        "readout": readout,
        "recommendation": "write_cosmology_bridge_run_manifest_next",
        "next_target": "22-cosmology-bridge-run-manifest.md",
        "cosmology_parent_derived": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "C0_role": "closure_benchmark_only",
        "critical_open_items": [
            "derive_b_mem_magnitude",
            "derive_F_N_or_activation_shape",
            "derive_FLRW_memory_equations",
            "derive_perturbation_sector",
            "lock_same-test_robustness_manifest",
        ],
        "outputs": {
            "cosmology_bridge_sources": str(results_dir / "cosmology_bridge_sources.csv"),
            "cosmology_variable_parent_bridge": str(results_dir / "cosmology_variable_parent_bridge.csv"),
            "cosmology_branch_status": str(results_dir / "cosmology_branch_status.csv"),
            "cosmology_robustness_rules": str(results_dir / "cosmology_robustness_rules.csv"),
            "cosmology_next_command_contract": str(results_dir / "cosmology_next_command_contract.csv"),
            "cosmology_bridge_gates": str(results_dir / "cosmology_bridge_gates.csv"),
            "cosmology_bridge_decision": str(results_dir / "cosmology_bridge_decision.csv"),
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
