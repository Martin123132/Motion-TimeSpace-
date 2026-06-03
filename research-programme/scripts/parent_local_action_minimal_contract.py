from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-local-action-minimal-contract"
STATUS = "parent_local_action_minimal_contract_written_required_variations_and_fallbacks_explicit_not_satisfied_no_local_GR_promotion"
CLAIM_CEILING = "parent_action_contract_only_no_WEP_PPN_EH_boundary_bulk_fifth_force_source_or_local_GR_pass"
NEXT_TARGET = "383-local-bound-runner-v2-from-retained-residuals.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent variation sectors and Ward force ledger",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force fate map and retained residual vector",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH sufficiency stack and operator obstruction ledger",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal matter coupling contract and forbidden WEP/clock vertices",
    },
    {
        "path": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "role": "lifted-C conditional route and parent/boundary/domain missing pieces",
    },
    {
        "path": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "role": "topological class selection not parent-derived; closure ledger",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common F closure and eta_WEP residual",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "EH not parent-derived; modified-gravity residual operator ledger",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "preferred-frame/vector coefficient map and no-hair target",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "fifth-force alpha(lambda) range-coupling contract",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "kappa/G_eff/M_eff/measured-GM absorption contract",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "class-only boundary action conditional no-angular theorem and retained coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X mass-gap/no-hair and alpha_X(lambda_X) force-law contract",
    },
    {
        "path": "381-local-GR-debt-ledger-rollup-after-360-380.md",
        "role": "post-360 local-GR debt ledger and next parent-action target",
    },
]


ACTION_BLOCKS = [
    {
        "block": "S_EH_or_metric_core",
        "minimal_form": "(16 pi G_*)^-1 int sqrt(-g) [R - 2 Lambda_*] plus allowed boundary/topological terms",
        "must_vary_to": "metric/coframe equation with EH as the only surviving local exterior operator",
        "closure_condition": "all non-EH operator coefficients theorem-zero, low-energy suppressed with bounds, or retained",
        "if_failed": "modified_gravity_operator_ledger",
    },
    {
        "block": "S_matter_one_coframe",
        "minimal_form": "sum_A S_A[Psi_A, ehat, omega(ehat), constants_A]",
        "must_vary_to": "delta S_matter/delta Z_I|ehat = 0 and nabla_hat_mu T_hat^mu_nu = 0",
        "closure_condition": "one ehat for all species, photons, clocks, rulers; no species F_A(C_D); no direct MTS matter vertices",
        "if_failed": "eta_WEP_alpha_clock_nonmetric_light_species_charge",
    },
    {
        "block": "S_selector_lifted_C_class",
        "minimal_form": "parent selector for lifted-C / class data with quotient representative invariance",
        "must_vary_to": "matter-visible P_D C or class metric selected without raw Cperp trace source",
        "closure_condition": "physical class/domain selector derived; local class triviality or common-mode silence follows",
        "if_failed": "projected_metric_closure_phiC_residual",
    },
    {
        "block": "S_projector_PD",
        "minimal_form": "covariant metric-independent topological/relative-chain projector or owned constrained projector",
        "must_vary_to": "F_P_bulk = 0 or retained conserved projector stress",
        "closure_condition": "no fixed external projector and no dropped metric-dependent projector stress",
        "if_failed": "gamma_xi_preferred_frame_conservation_residual",
    },
    {
        "block": "S_X_auxiliary_or_mass_gap",
        "minimal_form": "first-order constrained X sector or positive massive source-free exterior operator",
        "must_vary_to": "F_X = 0 by constraint/no-hair or alpha_X(lambda_X) force law if sourced",
        "closure_condition": "operator sign, source-free exterior, X charge/test charge, and boundary conditions owned",
        "if_failed": "epsilon_bulk_deltaG_fifth_force_gamma_beta",
    },
    {
        "block": "S_boundary_class_only",
        "minimal_form": "S_boundary(Q_rel, M_eff, V_scalar, I_top) plus Ward-owned flux terms",
        "must_vary_to": "delta S_boundary/delta B_TF = delta S_boundary/delta B_0i = 0 and flux owned",
        "closure_condition": "no angular reps, markers, normals, radial hair, or unowned flux except conserved monopole",
        "if_failed": "eps_B_TF_eps_B0i_eps_B_rad_eps_B_flux",
    },
    {
        "block": "S_domain_covariant_selector",
        "minimal_form": "covariant domain/class selector with no fixed preferred normal or external L_cg vector",
        "must_vary_to": "F_domain = 0 locally or retained domain stress with source-locked coefficients",
        "closure_condition": "domain data pure gauge, dynamical/covariant, locally constant, or bounded",
        "if_failed": "alpha1_alpha2_xi_preferred_location",
    },
    {
        "block": "S_source_normalization",
        "minimal_form": "absolute mass flux and coupling calibration sector fixing kappa, G_eff, M_eff, measured GM",
        "must_vary_to": "d(Pi_M J)=0, kappa=8 pi G_eff/c^4, mu_obs=G_eff M_eff constant universal",
        "closure_condition": "no radial/time/species/range dependence and Ward-owned conserved monopole",
        "if_failed": "deltaG_Gdot_beta_fifth_force_WEP_source_dependence",
    },
]


VARIATION_IDENTITIES = [
    {
        "identity": "total_diffeomorphism_Ward_identity",
        "required_equation": "nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu) + F_X^nu + F_P^nu + F_boundary^nu + F_domain^nu + F_matter_nonmetric^nu = 0",
        "must_show": "every force channel is varied, owned, zero-derived, boundary-only, or retained",
        "source_basis": "356",
        "current_status": "structural_identity_written_not_closed",
    },
    {
        "identity": "matter_one_coframe_variation",
        "required_equation": "delta S_matter / delta Z_I | ehat = 0 for Z_I in {X,J_rel,V_def,P_D,Cperp,species charges,...}",
        "must_show": "no direct non-geometric matter/clock/species vertices",
        "source_basis": "360,373",
        "current_status": "conditional_if_one_coframe_assumed",
    },
    {
        "identity": "EH_exterior_sufficiency",
        "required_equation": "Ward closure + no-hair + universal coupling + metric-only local 4D second-order diffeo exterior -> S_ext = S_EH + boundary",
        "must_show": "operator basis is EH-only through local PPN order",
        "source_basis": "358,375",
        "current_status": "conditional_sufficiency_not_parent_derived",
    },
    {
        "identity": "source_normalized_Newtonian_limit",
        "required_equation": "M_eff = (4 pi G_ref)^-1 int_S2 Pi_M J, d(Pi_M J)=0, mu_obs=G_eff M_eff",
        "must_show": "constant universal measured-GM absorption only, no drift/species/range leakage",
        "source_basis": "378",
        "current_status": "M_eff_conditional_GM_absorption_open",
    },
    {
        "identity": "boundary_noangular_flux_identity",
        "required_equation": "delta S_boundary/delta B_TF = delta S_boundary/delta B_0i = 0, n_mu B^{mu nu}+F_boundary_owned^nu=0",
        "must_show": "boundary action is class-only and flux is Ward-owned",
        "source_basis": "379",
        "current_status": "conditional_noangular_flux_open",
    },
    {
        "identity": "bulk_X_nohair_or_force_law",
        "required_equation": "(-Delta + m_X^2)X=0 gives X=0, or (-Delta+m_X^2)X=q_X rho gives alpha_X(lambda_X)",
        "must_show": "positive operator/source-free exterior or parent-normalized X force law",
        "source_basis": "380",
        "current_status": "contract_written_not_parent_derived",
    },
]


LOCAL_GR_SUFFICIENCY_STACK = [
    {
        "rung": 1,
        "condition": "compact ordinary local exterior",
        "required_result": "ordinary matter support is compact and exterior source data are monopole/boundary only",
        "current_status": "definition_plus_source_conditions_open",
    },
    {
        "rung": 2,
        "condition": "one observed coframe",
        "required_result": "all observables use the same ehat and no species-dependent class response",
        "current_status": "closure_axiom_not_parent_derived",
    },
    {
        "rung": 3,
        "condition": "full Ward force closure",
        "required_result": "F_X, F_P, F_boundary, F_domain, and F_matter_nonmetric vanish or are retained",
        "current_status": "mapped_not_closed",
    },
    {
        "rung": 4,
        "condition": "local no-hair / local silence",
        "required_result": "bulk, boundary, projector, vector, class, and domain hair vanish except safe monopole",
        "current_status": "conditional_mechanisms_only",
    },
    {
        "rung": 5,
        "condition": "source normalization",
        "required_result": "kappa/G_eff/M_eff/measured GM fixed and time/species/range independent",
        "current_status": "not_parent_derived",
    },
    {
        "rung": 6,
        "condition": "metric-only second-order exterior",
        "required_result": "surviving local exterior operator is EH plus Lambda through PPN order",
        "current_status": "central_blocker",
    },
    {
        "rung": 7,
        "condition": "Newton/PPN reduction",
        "required_result": "gamma=beta=1, alpha_i=0, WEP/clock/fifth-force residuals zero or bounded",
        "current_status": "not_claimable_coefficients_missing",
    },
]


RESIDUAL_FALLBACK_ROWS = [
    {
        "failed_contract": "one_coframe_or_universal_coupling",
        "fallback": "eta_WEP and alpha_clock rows remain active",
        "observable_rows": "eta_WEP; alpha_clock_redshift; nonmetric_light",
        "runner_policy": "source_locked_budget_only_no_WEP_pass",
    },
    {
        "failed_contract": "EH_operator_selection",
        "fallback": "retain modified-gravity operator coefficients c_i",
        "observable_rows": "gamma; beta; xi; fifth_force; Gdot",
        "runner_policy": "coefficient_budget_or_unscored_if_range_missing",
    },
    {
        "failed_contract": "boundary_class_only_or_Ward_flux",
        "fallback": "retain eps_B_TF, eps_B0i, eps_B_rad, eps_B_flux",
        "observable_rows": "gamma; beta; alpha1; alpha2; alpha3; xi; Gdot; fifth_force",
        "runner_policy": "budget_coefficients_no_boundary_nohair_claim",
    },
    {
        "failed_contract": "bulk_X_nohair_or_force_law",
        "fallback": "retain epsilon_bulk or derive alpha_X(lambda_X)",
        "observable_rows": "gamma; beta; delta_G_or_fifth_force; eta_WEP_if_charged",
        "runner_policy": "unscored_until_mX_qX_QX_qtest_derived",
    },
    {
        "failed_contract": "source_normalization",
        "fallback": "retain delta_G, Gdot/G, source-dependent WEP/fifth-force ambiguity",
        "observable_rows": "delta_G; Gdot/G; beta; fifth_force; eta_WEP",
        "runner_policy": "constant_universal_monopole_only_absorbable",
    },
    {
        "failed_contract": "preferred_frame_domain_covariance",
        "fallback": "retain vector/domain coefficients",
        "observable_rows": "alpha1; alpha2; alpha3; xi",
        "runner_policy": "source_locked_budget_only_no_preferred_frame_pass",
    },
]


CONTRACT_TESTS = [
    {
        "test": "all_action_blocks_varied",
        "pass_if": "delta S includes metric/coframe, matter, X, projector, boundary, domain, selector, source-normalization variations",
        "current_result": "contract_written_not_performed",
    },
    {
        "test": "no_hidden_force_channels",
        "pass_if": "every Ward force either theorem-zero, boundary-only harmless, or retained",
        "current_result": "ledger_written_not_closed",
    },
    {
        "test": "single_observed_coframe_forced",
        "pass_if": "parent symmetry/constraint gives ehat_A=ehat and F_A(C_D)=F(C_D)",
        "current_result": "fail_open",
    },
    {
        "test": "EH_operator_forced",
        "pass_if": "non-EH local operator coefficients vanish by action principle or are bounded as residuals",
        "current_result": "fail_open",
    },
    {
        "test": "source_normalization_forced",
        "pass_if": "kappa, G_eff, M_eff, and measured-GM absorption are constant/universal/Ward-owned",
        "current_result": "fail_open",
    },
    {
        "test": "boundary_and_bulk_nohair_forced",
        "pass_if": "class-only boundary and positive source-free bulk-X operator are parent-derived",
        "current_result": "fail_open",
    },
    {
        "test": "residual_fallbacks_not_erased",
        "pass_if": "failed premises feed explicit source-locked/budget/unscored rows",
        "current_result": "pass_contract",
    },
]


CLAIM_POLICY = [
    {
        "claim": "parent action contract exists",
        "allowed": "yes",
        "reason": "action blocks, variations, closure conditions, and fallbacks are explicit",
    },
    {
        "claim": "parent action satisfies the contract",
        "allowed": "no",
        "reason": "this checkpoint writes obligations; it does not perform the full derivation",
    },
    {
        "claim": "local GR is derived",
        "allowed": "no",
        "reason": "one-coframe, EH, source, boundary, bulk-X, and coefficient gates remain open",
    },
    {
        "claim": "local residual testing can proceed",
        "allowed": "yes_budget_only",
        "reason": "fallback rows are separated and can be stress-tested without pass claims",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A minimal parent local action contract is now written. It requires one observed coframe, owned selector/class/projector/domain variations, Ward force closure, EH-only exterior operator selection, source normalization, class-only/Ward-owned boundary terms, and bulk-X no-hair or source-normalized force law. The contract is not yet satisfied; it is a map for derivation or disciplined residual fallback.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "convert retained residual fallback rows into a local-bound runner v2 with derived-zero, closure-zero, budget-only, and unscored states",
        "pass_condition": "testing can proceed without treating any open gate as a pass",
    },
    {
        "priority": 2,
        "target": "384-parent-action-first-variation-obstruction-map.md",
        "task": "attempt the first explicit variation of the minimal parent action and identify the first obstruction",
        "pass_condition": "the action contract is stress-tested by variation rather than prose only",
    },
    {
        "priority": 3,
        "target": "385-one-coframe-boundary-bulk-joint-nohair-attempt.md",
        "task": "try a joint mechanism for one coframe, class-only boundary, and bulk-X silence",
        "pass_condition": "derive a shared symmetry/constraint or retain all three as independent closures",
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
            "gate": "action_blocks_listed",
            "status": "pass",
            "evidence": f"{len(ACTION_BLOCKS)} minimal action blocks specified",
        },
        {
            "gate": "variation_identities_listed",
            "status": "pass",
            "evidence": f"{len(VARIATION_IDENTITIES)} required variation identities specified",
        },
        {
            "gate": "local_GR_sufficiency_stack_written",
            "status": "pass",
            "evidence": f"{len(LOCAL_GR_SUFFICIENCY_STACK)} sufficiency rungs listed",
        },
        {
            "gate": "residual_fallback_rows_written",
            "status": "pass",
            "evidence": f"{len(RESIDUAL_FALLBACK_ROWS)} fallback rows mapped",
        },
        {
            "gate": "parent_action_contract_satisfied",
            "status": "fail",
            "evidence": "contract is written but one-coframe/EH/source/boundary/bulk-X derivations remain open",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "contract only; no WEP/PPN/EH/local-GR pass",
        },
        {
            "gate": "budget_only_testing_next_allowed",
            "status": "pass",
            "evidence": "fallback rows can feed local-bound runner v2 without pass claims",
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
    write_csv(results_dir / "action_blocks.csv", ACTION_BLOCKS)
    write_csv(results_dir / "variation_identities.csv", VARIATION_IDENTITIES)
    write_csv(results_dir / "local_GR_sufficiency_stack.csv", LOCAL_GR_SUFFICIENCY_STACK)
    write_csv(results_dir / "residual_fallback_rows.csv", RESIDUAL_FALLBACK_ROWS)
    write_csv(results_dir / "contract_tests.csv", CONTRACT_TESTS)
    write_csv(results_dir / "claim_policy.csv", CLAIM_POLICY)
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
        "action_blocks": len(ACTION_BLOCKS),
        "variation_identities": len(VARIATION_IDENTITIES),
        "local_GR_sufficiency_rungs": len(LOCAL_GR_SUFFICIENCY_STACK),
        "residual_fallback_rows": len(RESIDUAL_FALLBACK_ROWS),
        "parent_action_contract_satisfied": False,
        "derived_local_GR_claim_allowed": False,
        "budget_only_testing_next_allowed": True,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 382 parent local action minimal contract artifacts."
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
