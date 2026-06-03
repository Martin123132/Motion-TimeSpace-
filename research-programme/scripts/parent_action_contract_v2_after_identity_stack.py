from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-action-contract-v2-after-identity-stack"
STATUS = "parent_action_contract_v2_after_identity_stack_written_runner_v3_nonderived_rows_mapped_to_parent_obligations_contract_not_satisfied_no_local_GR_pass"
CLAIM_CEILING = "parent_action_contract_v2_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "399-local-GR-status-for-human-review.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger and no-hidden-projector/boundary/domain force rule",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "first minimal parent local action contract and action block list",
    },
    {
        "path": "388-WEP-species-symmetry-common-F-parent-selector-attempt.md",
        "role": "species-blind matter functor and WEP source-charge obligations",
    },
    {
        "path": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe as parent theorem target or labelled closure",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH operator selection obligation and non-EH operator ledger",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "kappa/G_eff/M_eff/GM source-normalization obligations",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "joint boundary/bulk Ward flux and no-hair obligations",
    },
    {
        "path": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "role": "domain/projector/preferred-frame no-hair obligations",
    },
    {
        "path": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "role": "local-GR sufficiency stack and runner-v3 readiness audit",
    },
    {
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "role": "runner-v3 matrix with non-derived row states",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "machine-readable runner-v3 row/state matrix",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/retained_residual_families.csv",
        "role": "machine-readable retained residual families from runner-v3",
    },
]


PARENT_ACTION_BLOCKS_V2 = [
    {
        "block": "S_metric_core",
        "minimal_form": "local metric/coframe core with candidate EH operator plus allowed boundary/topological terms",
        "must_vary_to": "metric-only local 4D second-order exterior or explicit retained non-EH coefficients",
        "runner_rows_paid": "R3_gamma; R4_beta; R8_xi; R10_fifth_force; R11_EH_operator_ledger",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_matter_identity_or_selector",
        "minimal_form": "sum_A S_A[Psi_A, e, omega[e], theta_A] or parent-derived selector ehat=e",
        "must_vary_to": "delta S_matter/delta Z_I = 0 for nonmetric selector variables and no species class spurions",
        "runner_rows_paid": "R0_eta_WEP_direct; R1_eta_WEP_source_charge; R2_clock",
        "current_status": "closure_only_not_parent_derived",
    },
    {
        "block": "S_species_blind_constants",
        "minimal_form": "theta_A independent of C_D, P_D, X, boundary, domain, and source-normalization variables",
        "must_vary_to": "no species-dependent source charge, constants drift, or composition response",
        "runner_rows_paid": "R1_eta_WEP_source_charge; R2_clock; R10_fifth_force_if_composition",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_source_normalization",
        "minimal_form": "calibration sector fixing kappa_eff, G_eff, M_eff, Pi_M J, and measured GM",
        "must_vary_to": "mu_obs=G_eff M_eff is constant, universal, range-independent, and Ward-owned",
        "runner_rows_paid": "R4_beta; R9_Gdot; R10_fifth_force; R1_eta_WEP_source_charge",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_boundary_class_flux",
        "minimal_form": "class-only boundary action S_boundary(Q_rel,M_eff,V_scalar,I_top) plus owned flux current",
        "must_vary_to": "delta S/delta B_TF=0, delta S/delta B_0i=0, B_rad=0 or constant monopole, flux Ward-owned",
        "runner_rows_paid": "R3_gamma; R4_beta; R5_alpha1; R6_alpha2; R7_alpha3; R8_xi; R9_Gdot; R10_fifth_force",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_bulk_X",
        "minimal_form": "positive source-free mass-gap or parent-normalized sourced force-law sector",
        "must_vary_to": "X=0 by no-hair or alpha_X(lambda_X) with source/test charges and measured-GM normalization",
        "runner_rows_paid": "R1_eta_WEP_source_charge; R3_gamma; R4_beta; R10_fifth_force",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_projector_domain",
        "minimal_form": "covariant metric-independent/topological projector plus scalar/topological domain selector or retained stress",
        "must_vary_to": "no physical domain vector/normal/projector representative leakage; all stresses retained if physical",
        "runner_rows_paid": "R5_alpha1; R6_alpha2; R7_alpha3; R8_xi; R9_Gdot",
        "current_status": "not_satisfied",
    },
    {
        "block": "S_total_Ward_owner",
        "minimal_form": "single diffeo-invariant parent action varying metric, matter, X, projector, boundary, domain, and source sectors together",
        "must_vary_to": "F_X^nu+F_P^nu+F_boundary^nu+F_domain^nu+F_source^nu+F_matter_nonmetric^nu=0 or retained",
        "runner_rows_paid": "R7_alpha3; R9_Gdot; R4_beta; source drift rows",
        "current_status": "ledger_written_not_closed",
    },
]


RUNNER_ROW_PARENT_OBLIGATIONS = [
    {
        "runner_row": "R0_eta_WEP_direct_geometry",
        "runner_state": "closure_zero",
        "parent_obligation": "derive ehat=e from the parent matter/metric variational principle, or keep branch labelled as closure",
        "required_identity": "delta S_matter/delta Z_I|e = 0 for all nonmetric local selector variables",
        "failure_fallback": "closure branch only; no parent-derived WEP claim",
    },
    {
        "runner_row": "R1_eta_WEP_source_charge",
        "runner_state": "contingent_budget",
        "parent_obligation": "forbid species-dependent source, bulk-X, boundary, class, and normalization charges",
        "required_identity": "partial_A mu_obs = 0 and q_X,A/m_A universal or zero",
        "failure_fallback": "retain WEP-source/composition guardrail",
    },
    {
        "runner_row": "R2_alpha_clock_redshift",
        "runner_state": "budget_only",
        "parent_obligation": "fix matter constants and clock sectors independent of nonmetric selectors and source drift",
        "required_identity": "partial_Z theta_A = 0 and partial_t clock normalization = 0",
        "failure_fallback": "retain clock/redshift budget row",
    },
    {
        "runner_row": "R3_gamma_minus_1",
        "runner_state": "budget_only",
        "parent_obligation": "derive EH-only exterior and remove/budget boundary shear, bulk-X, domain/projector stress, and non-EH slip operators",
        "required_identity": "gamma-1 coefficient map equals zero by theorem or all terms source-budgeted",
        "failure_fallback": "retain gamma budget row",
    },
    {
        "runner_row": "R4_beta_minus_1",
        "runner_state": "budget_only",
        "parent_obligation": "derive source-normalized nonlinear Newtonian limit plus no radial boundary/source/bulk hair",
        "required_identity": "beta_SN=0, B_rad=0, nonlinear non-EH/source terms zero or budgeted",
        "failure_fallback": "retain beta budget row",
    },
    {
        "runner_row": "R5_alpha1",
        "runner_state": "budget_only",
        "parent_obligation": "prove boundary vector, domain vector, projector vector, and marker leakage are absent/gauge/topological",
        "required_identity": "eps_B0i=eps_domain_vec=eps_P_vector=eps_marker=0 or coefficient-mapped",
        "failure_fallback": "retain alpha1 budget row",
    },
    {
        "runner_row": "R6_alpha2",
        "runner_state": "budget_only",
        "parent_obligation": "prove anisotropic/domain/projector vector residues vanish or are coefficient-mapped",
        "required_identity": "eps_B0i=eps_domain_vec=eps_domain_aniso=eps_P_vector=0 or budgeted",
        "failure_fallback": "retain alpha2 budget row",
    },
    {
        "runner_row": "R7_alpha3",
        "runner_state": "contingent_budget",
        "parent_obligation": "own or eliminate boundary/bulk/domain/projector momentum flux in the total Ward identity",
        "required_identity": "n_mu B^{mu i}+F_X^i+F_domain^i+F_projector^i=0 or retained",
        "failure_fallback": "retain alpha3 as contingent guardrail if channel exists",
    },
    {
        "runner_row": "R8_xi",
        "runner_state": "budget_only",
        "parent_obligation": "remove preferred-location anisotropy from boundary shear, domain topology/cycles, and external-domain data",
        "required_identity": "eps_B_TF_l>=2=eps_domain_aniso=eps_H1H2_cycle=0 or coefficient-mapped",
        "failure_fallback": "retain xi budget row separate from gamma",
    },
    {
        "runner_row": "R9_Gdot_over_G",
        "runner_state": "contingent_budget",
        "parent_obligation": "derive time-independent G_eff M_eff and no memory/domain/flux drift",
        "required_identity": "partial_t ln(G_eff M_eff)+kernel/flux drift = 0",
        "failure_fallback": "retain Gdot/G contingent guardrail",
    },
    {
        "runner_row": "R10_delta_G_or_fifth_force_yukawa",
        "runner_state": "unscored_parameterized",
        "parent_obligation": "derive theorem-zero finite-range channels or alpha(lambda), range, source/test charge, and screening profile",
        "required_identity": "alpha_X(lambda_X), alpha_B(lambda_B), alpha_Y(lambda_Y) or zero theorem",
        "failure_fallback": "retain unscored parameterized fifth-force row",
    },
    {
        "runner_row": "R11_non_EH_operator_coefficients",
        "runner_state": "retained_residual",
        "parent_obligation": "derive metric-only local 4D second-order exterior or keep every non-EH operator coefficient explicit",
        "required_identity": "c_R2=c_fR=c_Weyl=c_scalar=c_vector=c_nonlocal=c_source=0 or source-budgeted",
        "failure_fallback": "retain modified-gravity operator ledger",
    },
]


REQUIRED_VARIATION_IDENTITIES_V2 = [
    {
        "identity": "matter_identity_coframe_selector",
        "equation": "delta S_matter/delta Z_I|e = 0; ehat=e; partial_Z theta_A=0",
        "must_show": "no nonmetric selector enters local matter geometry or constants",
        "current_status": "closure_label_only",
    },
    {
        "identity": "species_blind_source_charge",
        "equation": "partial_A mu_obs=0 and q_X,A/m_A=q_X,B/m_B or q_X=0",
        "must_show": "no composition/source-charge WEP leakage",
        "current_status": "not_derived",
    },
    {
        "identity": "EH_operator_selection",
        "equation": "E_ext^{mu nu}=a G^{mu nu}+b g^{mu nu}; all H_i^{mu nu} coefficients zero/retained",
        "must_show": "metric-only local 4D second-order exterior or explicit residual action",
        "current_status": "not_derived",
    },
    {
        "identity": "source_normalized_Newtonian_limit",
        "equation": "G_eff=kappa_eff c^4/(8 pi); mu_obs=G_eff M_eff; partial_r,t,A mu_obs=0",
        "must_show": "constant universal measured-GM absorption",
        "current_status": "not_derived",
    },
    {
        "identity": "boundary_class_flux_nohair",
        "equation": "delta S_boundary/delta B_TF=0; delta S_boundary/delta B_0i=0; B_rad=0; n_mu B^{mu nu}+F_owned^nu=0",
        "must_show": "no boundary shear/vector/radial/flux hair except safe monopole",
        "current_status": "conditional_not_parent_derived",
    },
    {
        "identity": "bulk_X_nohair_or_force_law",
        "equation": "(-Delta+m_X^2)X=0 -> X=0, or (-Delta+m_X^2)X=q_X rho -> alpha_X(lambda_X)",
        "must_show": "bulk X is theorem-zero or fifth-force scorable",
        "current_status": "not_derived",
    },
    {
        "identity": "domain_projector_nohair",
        "equation": "P_D topological/gauge or T_P,T_D retained; domain selector scalar/topological; no H1/H2 vector cycles",
        "must_show": "no preferred frame/location from domain/projector data",
        "current_status": "not_derived",
    },
    {
        "identity": "total_Ward_force_closure",
        "equation": "F_X^nu+F_P^nu+F_boundary^nu+F_domain^nu+F_source^nu+F_matter_nonmetric^nu=0 or retained",
        "must_show": "no hidden force channel is erased",
        "current_status": "mapped_not_closed",
    },
]


NO_CHEAT_RULES_V2 = [
    {
        "rule": "closure_not_derivation",
        "forbids": "calling ehat=e a parent theorem unless it follows from S_parent variation",
        "runner_reason": "R0 closure_zero cannot become derived_zero by wording",
    },
    {
        "rule": "field_redefinition_not_GR",
        "forbids": "renaming ehat as the metric while leaving EH/source/operator debts unpaid",
        "runner_reason": "R11 and source rows remain after frame relabeling",
    },
    {
        "rule": "Bianchi_not_uniqueness",
        "forbids": "using conservation alone to delete non-EH operators",
        "runner_reason": "R11 retained operator ledger remains",
    },
    {
        "rule": "GM_absorption_only_constant_universal",
        "forbids": "absorbing radial/time/species/range dependence into measured mass",
        "runner_reason": "R4/R9/R10/R1 remain unless source theorem holds",
    },
    {
        "rule": "boundary_effect_not_a_bucket",
        "forbids": "hiding shear/vector/radial/flux pieces under one harmless boundary word",
        "runner_reason": "boundary pieces feed gamma/beta/alpha_i/xi/Gdot/fifth-force",
    },
    {
        "rule": "alpha3_contingent_not_optional",
        "forbids": "ignoring unowned flux or applying alpha3 when no channel exists",
        "runner_reason": "R7 stays contingent",
    },
    {
        "rule": "fifth_force_needs_profile",
        "forbids": "scoring delta_G/fifth force as one scalar without alpha(lambda)",
        "runner_reason": "R10 stays unscored_parameterized",
    },
    {
        "rule": "projector_stress_not_droppable",
        "forbids": "using a projector/domain action while dropping its stress/flux",
        "runner_reason": "domain/projector rows remain until Ward-owned or retained",
    },
]


DERIVATION_MILESTONES = [
    {
        "milestone": 1,
        "target": "identity_matter_selector_parent_theorem",
        "success_condition": "R0 moves from closure_zero to derived_zero and R1 species/source charges are forbidden or universal",
        "next_artifact": "parent matter-sector theorem or no-go",
    },
    {
        "milestone": 2,
        "target": "EH_operator_parent_selection",
        "success_condition": "R11 non-EH operator coefficients become derived_zero or explicit retained EFT coefficients with bounds",
        "next_artifact": "operator-selection parent action proof",
    },
    {
        "milestone": 3,
        "target": "source_normalization_parent_theorem",
        "success_condition": "R4/R9/R10 source-normalization exits close except true force-law rows",
        "next_artifact": "kappa/G_eff/M_eff/GM derivation",
    },
    {
        "milestone": 4,
        "target": "boundary_bulk_Ward_nohair_theorem",
        "success_condition": "boundary/bulk coefficients either derived_zero or alpha(lambda)-scored",
        "next_artifact": "joint no-hair/force-law proof",
    },
    {
        "milestone": 5,
        "target": "domain_projector_gauge_or_retained_stress_theorem",
        "success_condition": "alpha1/alpha2/alpha3/xi/Gdot domain/projector channels close or coefficient-map quantitatively",
        "next_artifact": "domain/projector parent variation theorem",
    },
    {
        "milestone": 6,
        "target": "PPN_coefficient_derivation",
        "success_condition": "gamma=beta=1, alpha_i=xi=0, no fifth force, no Gdot/G follow from the parent action",
        "next_artifact": "local PPN coefficient derivation or runner-v3 numeric residual sweep",
    },
]


CONTRACT_TESTS_V2 = [
    {
        "test": "every_runner_v3_row_has_parent_obligation",
        "expected": "one parent obligation per runner-v3 row/family",
        "current_result": "pass_contract_written",
    },
    {
        "test": "identity_branch_not_mislabeled",
        "expected": "R0 remains closure_zero unless parent theorem exists",
        "current_result": "pass_policy",
    },
    {
        "test": "nonEH_operators_not_deleted",
        "expected": "R11 retained unless EH selection theorem derives zero",
        "current_result": "pass_policy",
    },
    {
        "test": "source_boundary_bulk_domain_flux_owned",
        "expected": "total Ward force closure derived",
        "current_result": "fail_open",
    },
    {
        "test": "alpha_lambda_force_law_derived",
        "expected": "finite-range channels become alpha(lambda)-scorable or theorem-zero",
        "current_result": "fail_open",
    },
    {
        "test": "local_GR_claim_allowed",
        "expected": "all rows derived_zero/harmless and no closure-only public claim",
        "current_result": "fail_open",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Parent-action contract v2 maps every runner-v3 non-derived row to an explicit parent-action obligation. The contract is now sharper than the earlier skeleton: identity closure must become a parent matter-selector theorem, EH must be selected in the same matter frame, source normalization must fix measured GM, boundary/bulk/domain/projector flux must be Ward-owned or retained, finite-range forces need alpha(lambda), and PPN coefficients must be derived rather than budgeted. The contract is written, not satisfied. No WEP, EH, Newtonian, PPN, fifth-force, boundary/bulk/domain, or local-GR pass is claimed.",
        "contract_written": True,
        "contract_satisfied": False,
        "runner_v3_rows_mapped": len(RUNNER_ROW_PARENT_OBLIGATIONS),
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "write a concise private status memo for human review: what is strong, what is open, what to test next",
        "pass_condition": "clear project overview with no public overclaim and direct pointers to runner-v3/contract artifacts",
    },
    {
        "priority": 2,
        "target": "400-runner-v3-numeric-smoke-extension.md",
        "task": "extend runner-v3 smoke controls toward real symbolic/numeric coefficient sweeps",
        "pass_condition": "same-pipeline GR/null baseline plus MTS retained residual sweeps",
    },
    {
        "priority": 3,
        "target": "401-parent-matter-selector-theorem-attempt.md",
        "task": "attempt the first contract-v2 theorem: derive or reject the parent identity matter selector",
        "pass_condition": "R0 can move toward derived_zero or remains explicit closure only",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "parent_action_blocks_v2_written",
            "status": "pass",
            "evidence": f"{len(PARENT_ACTION_BLOCKS_V2)} action blocks specified",
        },
        {
            "gate": "runner_rows_mapped_to_obligations",
            "status": "pass",
            "evidence": f"{len(RUNNER_ROW_PARENT_OBLIGATIONS)} runner-v3 row obligations written",
        },
        {
            "gate": "variation_identities_written",
            "status": "pass",
            "evidence": f"{len(REQUIRED_VARIATION_IDENTITIES_V2)} required variation identities written",
        },
        {
            "gate": "no_cheat_rules_written",
            "status": "pass",
            "evidence": f"{len(NO_CHEAT_RULES_V2)} no-cheat rules recorded",
        },
        {
            "gate": "contract_satisfied",
            "status": "fail",
            "evidence": "contract obligations are written but not parent-derived",
        },
        {
            "gate": "all_runner_rows_promotable",
            "status": "fail",
            "evidence": "runner-v3 rows remain closure, contingent, budget, unscored, or retained",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "parent action contract v2 is unsatisfied",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "parent_action_blocks_v2.csv", PARENT_ACTION_BLOCKS_V2)
    write_csv(results_dir / "runner_row_parent_obligations.csv", RUNNER_ROW_PARENT_OBLIGATIONS)
    write_csv(results_dir / "required_variation_identities_v2.csv", REQUIRED_VARIATION_IDENTITIES_V2)
    write_csv(results_dir / "no_cheat_rules_v2.csv", NO_CHEAT_RULES_V2)
    write_csv(results_dir / "derivation_milestones.csv", DERIVATION_MILESTONES)
    write_csv(results_dir / "contract_tests_v2.csv", CONTRACT_TESTS_V2)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "parent_action_blocks_v2": len(PARENT_ACTION_BLOCKS_V2),
        "runner_rows_mapped": len(RUNNER_ROW_PARENT_OBLIGATIONS),
        "variation_identities_v2": len(REQUIRED_VARIATION_IDENTITIES_V2),
        "contract_written": True,
        "contract_satisfied": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 398 parent action contract v2 after identity stack artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
