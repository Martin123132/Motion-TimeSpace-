from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-operator-selection-under-identity-closure"
STATUS = "EH_operator_selection_under_identity_closure_attempt_written_EH_conditional_not_parent_derived_nonEH_operators_retained_no_local_GR_pass"
CLAIM_CEILING = "EH_operator_selection_under_identity_closure_only_no_EH_PPN_source_boundary_bulk_fifth_force_or_local_GR_pass"
NEXT_TARGET = "393-source-normalized-Newtonian-limit-under-identity-closure.md"


SOURCE_DOCS = [
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "conditional EH sufficiency stack: Ward closure plus no-hair plus metric-only local second-order exterior",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "EH not parent-derived and residual modified-gravity operator ledger",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "vector/domain/preferred-frame operator residues and alpha_i/xi rows",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "kappa/G_eff/M_eff/measured-GM source-normalization blocker",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary class-only/no-angular theorem and retained boundary coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X no-hair or source-normalized fifth-force contract",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent local action contract and full local-GR sufficiency ladder",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "GR/null baseline sanity and local residual budget rows",
    },
    {
        "path": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe as labelled closure, not parent-derived WEP theorem",
    },
    {
        "path": "390-class-metric-counterstress-nohair-contract.md",
        "role": "class-metric branch demoted to separate modified-gravity/counterstress route",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "post-identity local-GR stack and EH operator selection as next target",
    },
]


OPERATOR_SELECTION_PREMISES = [
    {
        "premise": "identity_coframe_closure",
        "mathematical_form": "S_matter = sum_A S_A[Psi_A, e, omega[e], theta_A]",
        "would_do": "removes direct matter pullback Pi_I^matter for the GR-facing branch",
        "current_status": "closure_zero_not_derived_zero",
        "failure_residual": "does not restrict pure gravitational operator basis",
    },
    {
        "premise": "diffeomorphism_covariance",
        "mathematical_form": "delta_xi S_ext = 0",
        "would_do": "gives a conserved total exterior field equation",
        "current_status": "structural_needed_not_selective",
        "failure_residual": "many non-EH covariant operators are also conserved",
    },
    {
        "premise": "Ward_force_closure",
        "mathematical_form": "nabla_mu E_total^{mu nu} + F_X^nu + F_boundary^nu + F_domain^nu = 0",
        "would_do": "prevents unowned force leakage into matter motion and PPN rows",
        "current_status": "mapped_not_closed",
        "failure_residual": "source drift, preferred-frame, beta, alpha3, fifth-force rows",
    },
    {
        "premise": "compact_source_exterior",
        "mathematical_form": "T_matter^{mu nu}=0 outside compact support; only conserved monopole/boundary data remain",
        "would_do": "makes local exterior an operator-selection problem rather than an active matter-source problem",
        "current_status": "definition_plus_source_conditions_open",
        "failure_residual": "radial scalar or boundary charge becomes delta_G/fifth-force/source-normalization residue",
    },
    {
        "premise": "metric_only_field_content",
        "mathematical_form": "S_ext = S_ext[g] + boundary/topological, no local Z_I propagation",
        "would_do": "removes scalar, vector, torsion, nonmetricity, and memory-kernel operators",
        "current_status": "not_parent_derived",
        "failure_residual": "modified-gravity operator ledger remains active",
    },
    {
        "premise": "local_4D_second_order_metric_equations",
        "mathematical_form": "E_{mu nu}[g] contains no derivatives beyond second order in 4D",
        "would_do": "selects G_{mu nu}+Lambda g_{mu nu} as the only local metric operator up to normalization",
        "current_status": "conditional_sufficiency_not_parent_derived",
        "failure_residual": "R^2, f(R), Ricci^2, Weyl^2, nonlocal, or EFT operators survive",
    },
    {
        "premise": "boundary_topological_ownership",
        "mathematical_form": "delta S_boundary gives only GHY/topological/class-only harmless terms or Ward-owned flux",
        "would_do": "prevents hidden boundary hair from masquerading as EH exterior",
        "current_status": "not_parent_derived",
        "failure_residual": "eps_B_TF, eps_B0i, eps_B_rad, eps_B_flux feed PPN/preferred-frame rows",
    },
    {
        "premise": "source_normalization",
        "mathematical_form": "kappa, G_eff, M_eff, and mu_obs=G_eff M_eff are universal constants locally",
        "would_do": "turns EH operator into the measured Newtonian/PPN limit",
        "current_status": "open",
        "failure_residual": "delta_G, Gdot/G, fifth-force normalization, beta ambiguity",
    },
    {
        "premise": "local_nohair",
        "mathematical_form": "Z_I is zero, pure gauge, constant monopole, or source-budgeted in the exterior",
        "would_do": "kills local scalar/vector/domain/projector/bulk hair",
        "current_status": "conditional_fragments_only",
        "failure_residual": "gamma, beta, alpha_i, xi, fifth-force rows remain active",
    },
]


SELECTION_ATTEMPTS = [
    {
        "attempt": "identity_closure_only",
        "claim_tested": "ehat=e should force GR",
        "result": "fail",
        "reason": "matter sees one coframe, but pure exterior gravity can still contain non-EH operators",
        "retained_residue": "full operator ledger",
    },
    {
        "attempt": "Bianchi_or_Ward_only",
        "claim_tested": "conservation should force Einstein equations",
        "result": "fail",
        "reason": "covariant higher-curvature, scalar-tensor, vector, torsion, and nonlocal equations can be conserved too",
        "retained_residue": "conserved non-EH tensors",
    },
    {
        "attempt": "metric_only_without_second_order",
        "claim_tested": "one metric should be enough",
        "result": "fail",
        "reason": "metric-only does not exclude f(R), R^2, Ricci^2, Weyl^2, and nonlocal curvature kernels",
        "retained_residue": "higher-derivative and memory operators",
    },
    {
        "attempt": "low_energy_EFT_truncation",
        "claim_tested": "higher operators are negligible at local scales",
        "result": "conditional_budget_not_derivation",
        "reason": "suppression can justify a budget branch but not exact zero-derived GR reduction",
        "retained_residue": "scale-suppressed coefficients need ranges/couplings",
    },
    {
        "attempt": "local_4D_metric_second_order",
        "claim_tested": "metric-only local second-order 4D exterior selects EH plus Lambda",
        "result": "conditional_pass_if_premises_assumed",
        "reason": "this is the correct EH-selection theorem shape, but MTS has not derived the premise from the parent action",
        "retained_residue": "premise debt remains rather than operator victory",
    },
    {
        "attempt": "nohair_source_boundary_stack",
        "claim_tested": "extra MTS fields reduce to boundary/monopole data and source normalization fixes GM",
        "result": "not_yet_satisfied",
        "reason": "boundary, bulk-X, preferred-frame/domain, and source-normalization contracts remain open",
        "retained_residue": "PPN/source/fifth-force residual vector",
    },
]


EH_SUFFICIENCY_LADDER = [
    {
        "rung": 1,
        "condition": "identity coframe for matter",
        "required_result": "no direct nonmetric matter-pullback force",
        "current_status": "closure_pass_only",
        "promotion_allowed": "branch_testing_yes_parent_claim_no",
    },
    {
        "rung": 2,
        "condition": "compact source-normalized exterior",
        "required_result": "ordinary matter absent outside compact support and source is constant measured GM",
        "current_status": "open",
        "promotion_allowed": "no",
    },
    {
        "rung": 3,
        "condition": "full Ward force closure",
        "required_result": "all nonmetric force terms vanish, cancel, or are retained as explicit stress",
        "current_status": "mapped_not_closed",
        "promotion_allowed": "no",
    },
    {
        "rung": 4,
        "condition": "local no-hair/local silence",
        "required_result": "bulk, boundary, projector, vector, class, and domain hair are zero/gauge/monopole",
        "current_status": "conditional_fragments_only",
        "promotion_allowed": "no",
    },
    {
        "rung": 5,
        "condition": "metric-only local exterior",
        "required_result": "no independent scalar/vector/torsion/nonmetricity/nonlocal kernel propagates",
        "current_status": "not_parent_derived",
        "promotion_allowed": "no",
    },
    {
        "rung": 6,
        "condition": "4D second-order metric equations",
        "required_result": "surviving operator is EH plus Lambda and boundary/topological terms",
        "current_status": "conditional_theorem_only",
        "promotion_allowed": "no_until_parent_premise_derived",
    },
    {
        "rung": 7,
        "condition": "Newtonian and PPN reduction",
        "required_result": "gamma=beta=1, alpha_i=xi=0, no fifth force, constant G_eff M_eff",
        "current_status": "not_claimable_coefficients_missing",
        "promotion_allowed": "no",
    },
]


NON_EH_OPERATOR_LEDGER = [
    {
        "operator_family": "Einstein_Hilbert_plus_Lambda",
        "schematic_operator": "sqrt(-g)(R - 2 Lambda)",
        "why_allowed_if_premise_fails": "target operator survives, but is not uniquely selected unless the metric-only second-order premise is derived",
        "observable_rows": "Newtonian_limit; gamma; beta",
        "current_policy": "conditional target, not a standalone proof",
    },
    {
        "operator_family": "boundary_or_topological",
        "schematic_operator": "GHY; Euler/Gauss-Bonnet topological; class boundary functionals",
        "why_allowed_if_premise_fails": "boundary variations can hide shear, vector, radial, or flux hair if not owned",
        "observable_rows": "gamma; beta; alpha3; xi",
        "current_policy": "retain unless class-only/topological/Ward-owned",
    },
    {
        "operator_family": "higher_curvature_scalar",
        "schematic_operator": "R^2; f(R)",
        "why_allowed_if_premise_fails": "diffeomorphism covariance allows scalar curvature corrections if second-order exactness is not derived",
        "observable_rows": "gamma; beta; delta_G_or_fifth_force_yukawa",
        "current_policy": "derive zero or map mass/range/coupling",
    },
    {
        "operator_family": "higher_curvature_spin2_or_Weyl",
        "schematic_operator": "R_{mu nu}R^{mu nu}; C_{mu nu rho sigma}C^{mu nu rho sigma}",
        "why_allowed_if_premise_fails": "metric-only still permits higher-derivative spin-2/shear operators",
        "observable_rows": "gamma; xi; lensing_slip; wave_sector_if_used",
        "current_policy": "retain coefficient ledger until low-energy/nohair theorem exists",
    },
    {
        "operator_family": "scalar_tensor_or_class_metric",
        "schematic_operator": "F(C_D)R; (nabla C_D)^2; V(C_D); phi_C metric factor",
        "why_allowed_if_premise_fails": "identity matter coframe does not delete a universal scalar/class metric in the gravity sector",
        "observable_rows": "gamma; beta; clock; fifth_force; Gdot/G",
        "current_policy": "separate modified-gravity/counterstress branch after 390",
    },
    {
        "operator_family": "vector_or_preferred_frame",
        "schematic_operator": "u^mu u^nu R_{mu nu}; B_0i; marker/domain-normal couplings",
        "why_allowed_if_premise_fails": "identity coframe does not prove domain/projector/vector no-hair",
        "observable_rows": "alpha1; alpha2; alpha3; xi",
        "current_policy": "retain until vector/domain no-hair or coefficient map",
    },
    {
        "operator_family": "torsion_or_nonmetricity",
        "schematic_operator": "T^2; Q^2; independent connection terms",
        "why_allowed_if_premise_fails": "one observed coframe does not globally prove Levi-Civita-only parent connection",
        "observable_rows": "WEP_if_matter_coupled; clock; spin; light_cone",
        "current_policy": "forbid by compatibility theorem or retain as nonmetric residual",
    },
    {
        "operator_family": "bulk_X_or_auxiliary",
        "schematic_operator": "(-Delta + m_X^2)X; X R; X T; source-normalized X charge",
        "why_allowed_if_premise_fails": "bulk-X mass gap/source-free exterior is not parent-derived",
        "observable_rows": "fifth_force; gamma; beta; delta_G",
        "current_policy": "derive theorem-zero or alpha_X(lambda_X)",
    },
    {
        "operator_family": "nonlocal_or_memory_kernel",
        "schematic_operator": "R Box^-1 R; history/domain kernels; delayed boundary response",
        "why_allowed_if_premise_fails": "locality and kernel silence are not derived from the parent programme",
        "observable_rows": "Gdot/G; delta_G; fifth_force; cosmology_local_leakage",
        "current_policy": "retain until local kernel silence/screening scale is derived",
    },
    {
        "operator_family": "source_normalization_operator",
        "schematic_operator": "kappa(C_D); G_eff(C_D); M_eff boundary charge",
        "why_allowed_if_premise_fails": "EH without fixed source normalization is not the measured Newtonian limit",
        "observable_rows": "delta_G; Gdot/G; beta; fifth_force",
        "current_policy": "next target: derive constant universal GM absorption or retain rows",
    },
]


RUNNER_TRANSITION_UNDER_IDENTITY = [
    {
        "observable_row": "eta_WEP",
        "before_392": "active or budgeted through matter-coframe pullback",
        "after_392_policy": "closure_zero inside identity branch only",
        "reason": "all matter placed on ehat=e by explicit assumption",
        "local_GR_implication": "does not imply EH or PPN pass",
    },
    {
        "observable_row": "alpha_clock_redshift",
        "before_392": "active if clocks see class/nonmetric spurions",
        "after_392_policy": "direct matter-clock spurion closed by identity branch; gravitational/source residues still tracked",
        "reason": "clock matter action uses e, but source drift/nonlocal kernels may still affect observables",
        "local_GR_implication": "no public clock claim",
    },
    {
        "observable_row": "gamma_minus_1",
        "before_392": "ready budget only",
        "after_392_policy": "retained",
        "reason": "higher-curvature, scalar/class, boundary, bulk, and vector residues can shift light bending/slip",
        "local_GR_implication": "no PPN gamma pass",
    },
    {
        "observable_row": "beta_minus_1",
        "before_392": "ready budget only",
        "after_392_policy": "retained",
        "reason": "nonlinear curvature, source normalization, boundary radial hair, and bulk/source terms remain",
        "local_GR_implication": "no PPN beta pass",
    },
    {
        "observable_row": "preferred_frame_alpha_i_and_xi",
        "before_392": "source-locked budget/contingent rows",
        "after_392_policy": "retained",
        "reason": "identity matter coframe does not kill domain/projector/vector/boundary preferred-frame operators",
        "local_GR_implication": "no preferred-frame pass",
    },
    {
        "observable_row": "delta_G_or_fifth_force_yukawa",
        "before_392": "unscored parameterized force-law row",
        "after_392_policy": "retained",
        "reason": "scalar, bulk-X, source-normalization, and nonlocal residues still need alpha(lambda)",
        "local_GR_implication": "no fifth-force pass",
    },
    {
        "observable_row": "Gdot_over_G",
        "before_392": "contingent source-normalization row",
        "after_392_policy": "retained",
        "reason": "identity coframe does not derive constant G_eff M_eff or local memory silence",
        "local_GR_implication": "no source-normalized Newtonian pass",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "identity_closure_does_not_select_EH",
        "statement": "Putting matter on one coframe closes direct WEP pullback, but leaves the pure gravity operator basis open.",
        "consequence": "EH operator selection remains a separate theorem target.",
    },
    {
        "no_go": "Bianchi_identity_is_not_uniqueness",
        "statement": "Diffeomorphism covariance gives a conserved field equation, not a unique field equation.",
        "consequence": "conserved non-EH tensors and extra-field stress tensors remain allowed unless excluded.",
    },
    {
        "no_go": "metric_only_is_not_enough",
        "statement": "A single metric can still carry higher-curvature, f(R), Weyl, and nonlocal curvature operators.",
        "consequence": "second-order/locality or low-energy coefficient control is mandatory.",
    },
    {
        "no_go": "EFT_suppression_is_not_exact_reduction",
        "statement": "Small higher operators may be empirically safe, but that is not the same as deriving exact local GR.",
        "consequence": "suppressed residues can be a competitive modified-gravity branch, not an EH proof.",
    },
    {
        "no_go": "EH_without_source_normalization_is_not_Newton",
        "statement": "Even an EH operator needs kappa, G_eff, M_eff, and measured GM fixed to recover Newton/PPN.",
        "consequence": "source-normalized Newtonian limit becomes the next target.",
    },
]


GATE_POLICY = [
    {
        "gate": "EH_selection_if_full_premises_assumed",
        "current_result": "conditional_pass",
        "meaning": "identity closure plus metric-only local 4D second-order exterior plus no-hair/source/boundary ownership selects EH plus Lambda",
        "claim_policy": "may be used as conditional theorem shape only",
    },
    {
        "gate": "EH_parent_derived_from_MTS",
        "current_result": "fail",
        "meaning": "MTS has not derived metric-only second-order exterior or deleted all non-EH operators",
        "claim_policy": "no EH/local-GR claim",
    },
    {
        "gate": "residual_modified_gravity_branch",
        "current_result": "pass",
        "meaning": "non-EH families are explicitly retained and tied to local observable rows",
        "claim_policy": "allowed as internal test/budget branch",
    },
    {
        "gate": "source_normalization_ready",
        "current_result": "fail",
        "meaning": "kappa/G_eff/M_eff/measured-GM map is still open",
        "claim_policy": "next checkpoint target",
    },
    {
        "gate": "PPN_local_GR_pass",
        "current_result": "fail",
        "meaning": "gamma, beta, alpha_i, xi, fifth-force, and Gdot rows are not theorem-zero",
        "claim_policy": "no PPN or local-GR promotion",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Under identity-coframe closure, EH is selected only conditionally if the exterior is also metric-only, local, four-dimensional, second-order, source-normalized, and free of boundary/bulk/vector/nonlocal hair. The current MTS branch has not parent-derived those premises. Therefore the honest result is: identity closure helps isolate the GR-facing route, but all non-EH operator families remain explicit retained residuals. No EH, PPN, source-normalized Newtonian, fifth-force, or local-GR pass is claimed.",
        "conditional_EH_theorem": "alive",
        "EH_parent_derived": False,
        "non_EH_operators_retained": True,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive kappa/G_eff/M_eff/measured-GM absorption under identity closure",
        "pass_condition": "constant universal source normalization is parent-derived or delta_G/Gdot/fifth-force rows remain active",
    },
    {
        "priority": 2,
        "target": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "task": "jointly test whether boundary and bulk residues are theorem-zero, pure gauge, constant monopole, or source-budgeted",
        "pass_condition": "boundary/bulk coefficients vanish by theorem or remain in local runner",
    },
    {
        "priority": 3,
        "target": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "task": "derive or budget vector/domain/projector preferred-frame residues after identity closure",
        "pass_condition": "alpha1/alpha2/alpha3/xi are theorem-zero or coefficient-mapped",
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
            "gate": "identity_closure_retained_as_label",
            "status": "pass",
            "evidence": "identity coframe is used as closure_zero_not_derived_zero, not parent-derived WEP",
        },
        {
            "gate": "EH_conditional_selection_theorem_written",
            "status": "pass",
            "evidence": "metric-only local 4D second-order exterior selects EH plus Lambda if assumed",
        },
        {
            "gate": "EH_parent_derived",
            "status": "fail",
            "evidence": "metric-only, second-order, source-normalization, boundary, bulk, and preferred-frame no-hair premises remain open",
        },
        {
            "gate": "non_EH_operator_ledger_retained",
            "status": "pass",
            "evidence": f"{len(NON_EH_OPERATOR_LEDGER)} operator families retained or conditionally targeted",
        },
        {
            "gate": "runner_transition_written",
            "status": "pass",
            "evidence": f"{len(RUNNER_TRANSITION_UNDER_IDENTITY)} observable rows updated under identity policy",
        },
        {
            "gate": "source_normalized_Newtonian_limit_derived",
            "status": "fail",
            "evidence": "kappa/G_eff/M_eff/measured-GM absorption remains the next target",
        },
        {
            "gate": "PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "gamma, beta, alpha_i, xi, fifth-force, and Gdot rows remain retained/budgeted",
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
    write_csv(results_dir / "operator_selection_premises.csv", OPERATOR_SELECTION_PREMISES)
    write_csv(results_dir / "selection_attempts.csv", SELECTION_ATTEMPTS)
    write_csv(results_dir / "EH_sufficiency_ladder.csv", EH_SUFFICIENCY_LADDER)
    write_csv(results_dir / "nonEH_operator_ledger_under_identity.csv", NON_EH_OPERATOR_LEDGER)
    write_csv(results_dir / "runner_transition_under_identity.csv", RUNNER_TRANSITION_UNDER_IDENTITY)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "gate_policy.csv", GATE_POLICY)
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
        "operator_selection_premises": len(OPERATOR_SELECTION_PREMISES),
        "non_EH_operator_families_retained": len(NON_EH_OPERATOR_LEDGER),
        "identity_closure_state": "closure_zero_not_derived_zero",
        "EH_conditional_selection_theorem_written": True,
        "EH_operator_parent_derived": False,
        "source_normalized_Newtonian_limit_derived": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 392 EH operator selection under identity closure artifacts."
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
