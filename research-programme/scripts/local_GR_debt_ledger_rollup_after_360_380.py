from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-debt-ledger-rollup-after-360-380"
STATUS = "local_GR_debt_ledger_after_360_380_written_route_coherent_but_WEP_EH_boundary_bulk_source_gates_open_no_promotion"
CLAIM_CEILING = "local_GR_debt_ledger_only_no_WEP_PPN_EH_fifth_force_boundary_bulk_or_local_GR_pass"
NEXT_TARGET = "382-parent-local-action-minimal-contract.md"


CHECKPOINT_STATUS = [
    {
        "checkpoint": 360,
        "source_file": "360-universal-matter-coupling-theorem-attempt.md",
        "sector": "matter_coupling",
        "status": "universal_matter_coupling_conditional_theorem_sharpened_direct_WEP_clock_vertices_zero_parent_selector_open",
        "main_gain": "direct WEP/clock vertices are conditionally zero if universal coupling is parent-selected",
        "open_debt": "parent selector for universal matter coupling is still open",
        "rollup_class": "conditional_theorem_not_parent_derived",
    },
    {
        "checkpoint": 361,
        "source_file": "361-residual-gauge-principle-for-projected-matter-metric.md",
        "sector": "projected_metric_gauge",
        "status": "residual_gauge_selector_theorem_conditional_Cperp_exactness_still_open_projected_metric_not_promoted",
        "main_gain": "residual gauge selector route sharpened",
        "open_debt": "Cperp exactness remains open",
        "rollup_class": "conditional_theorem_not_parent_derived",
    },
    {
        "checkpoint": 362,
        "source_file": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
        "sector": "projected_metric",
        "status": "Cperp_scalar_exactness_rejected_projected_metric_demoted_to_explicit_closure_lifted_C_route_open",
        "main_gain": "projected metric route made honest by closure demotion",
        "open_debt": "lifted-C route required if projected metric is to be derived",
        "rollup_class": "closure_labelled",
    },
    {
        "checkpoint": 363,
        "source_file": "363-projected-metric-closure-ledger-and-lifted-C-route-contract.md",
        "sector": "projected_metric",
        "status": "projected_metric_closure_ledger_written_lifted_C_derivation_contract_set_GR_route_kept_open",
        "main_gain": "closure ledger and lifted-C derivation contract written",
        "open_debt": "lifted-C theorem not yet parent-derived",
        "rollup_class": "contract_written",
    },
    {
        "checkpoint": 364,
        "source_file": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "sector": "lifted_C",
        "status": "lifted_C_three_form_local_residual_nullness_conditionally_derived_parent_action_boundary_domain_missing",
        "main_gain": "three-form/local residual nullness route conditionally derived",
        "open_debt": "parent action, boundary, and domain selection missing",
        "rollup_class": "conditional_theorem_not_parent_derived",
    },
    {
        "checkpoint": 365,
        "source_file": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "sector": "lifted_C_boundary",
        "status": "boundary_primitive_condition_derived_as_fixed_relative_class_admissibility_physical_class_selection_open",
        "main_gain": "boundary primitive admissibility condition written",
        "open_debt": "physical class/domain selection remains open",
        "rollup_class": "conditional_theorem_not_parent_derived",
    },
    {
        "checkpoint": 366,
        "source_file": "366-representative-invariant-matter-action-for-lifted-C.md",
        "sector": "matter_action",
        "status": "representative_invariance_conditionally_selects_class_metric_direct_Cperp_vertices_forbidden_universality_and_class_selection_open",
        "main_gain": "representative invariance conditionally selects class metric and forbids direct Cperp vertices",
        "open_debt": "universality and physical class selection remain open",
        "rollup_class": "conditional_theorem_not_parent_derived",
    },
    {
        "checkpoint": 367,
        "source_file": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "sector": "class_selection",
        "status": "topological_class_selection_not_parent_derived_local_GR_route_demoted_to_labelled_closure_and_residual_testing",
        "main_gain": "topological class selection is explicitly closure-labelled",
        "open_debt": "no parent-derived class selector",
        "rollup_class": "closure_labelled",
    },
    {
        "checkpoint": 368,
        "source_file": "368-common-mode-class-metric-clock-PPN-residual-gate.md",
        "sector": "common_mode_phiC",
        "status": "class_metric_residual_gate_written_no_local_bound_pass_coefficients_and_source_locks_still_open",
        "main_gain": "clock/PPN residual gate written for common-mode class metric",
        "open_debt": "coefficients and source locks still open at that stage",
        "rollup_class": "residual_mapped",
    },
    {
        "checkpoint": 369,
        "source_file": "369-source-locked-closure-branch-local-bound-runner.md",
        "sector": "local_bounds",
        "status": "closure_branch_local_bound_runner_built_budget_only_no_coefficients_no_pass_claim",
        "main_gain": "source-locked local-bound runner built as budget-only diagnostic",
        "open_debt": "coefficients are not parent-derived",
        "rollup_class": "test_ready_budget_only",
    },
    {
        "checkpoint": 370,
        "source_file": "370-common-mode-phiC-coefficient-map.md",
        "sector": "common_mode_phiC",
        "status": "phiC_weak_field_coefficient_map_written_common_mode_bounds_require_zero_theorem_or_tiny_gradient_no_pass",
        "main_gain": "weak-field phi_C coefficient map written",
        "open_debt": "needs zero theorem or tiny gradient bound",
        "rollup_class": "residual_mapped",
    },
    {
        "checkpoint": 371,
        "source_file": "371-WEP-species-universality-or-active-eta-runner.md",
        "sector": "WEP",
        "status": "species_universality_not_parent_derived_eta_WEP_remains_active_hardest_ready_gate",
        "main_gain": "WEP eta row identified as hardest ready gate",
        "open_debt": "species universality is not parent-derived",
        "rollup_class": "active_source_locked_residual",
    },
    {
        "checkpoint": 372,
        "source_file": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "sector": "common_mode_phiC",
        "status": "local_phiC_zero_conditional_on_boundary_state_and_trivial_class_gradient_bounds_remain_if_not_parent_derived",
        "main_gain": "conditional local phi_C zero theorem written",
        "open_debt": "boundary-state/trivial-class premises are not parent-derived",
        "rollup_class": "conditional_or_budget",
    },
    {
        "checkpoint": 373,
        "source_file": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "sector": "WEP_coframe",
        "status": "one_observed_coframe_common_F_not_parent_derived_WEP_closure_axiom_required_eta_active",
        "main_gain": "one-coframe kill switch made exact if assumed",
        "open_debt": "one observed coframe/common F remains closure axiom",
        "rollup_class": "closure_labelled_active_residual",
    },
    {
        "checkpoint": 374,
        "source_file": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "sector": "source_locks",
        "status": "preferred_frame_xi_source_locked_fifth_force_parameterized_not_scalar_scored_no_local_GR_pass",
        "main_gain": "preferred-frame and xi source locks written; fifth-force kept range dependent",
        "open_debt": "fifth-force is not scalar-scored",
        "rollup_class": "test_ready_budget_only",
    },
    {
        "checkpoint": 375,
        "source_file": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "sector": "EH_exterior",
        "status": "EH_not_parent_derived_residual_operator_ledger_written_modified_gravity_coefficients_retained_no_local_GR_pass",
        "main_gain": "non-EH operator residual ledger written",
        "open_debt": "EH exterior is not parent-derived",
        "rollup_class": "central_blocker",
    },
    {
        "checkpoint": 376,
        "source_file": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "sector": "preferred_frame",
        "status": "vector_nohair_conditional_not_parent_derived_preferred_frame_coefficients_mapped_budget_only_no_PPN_pass",
        "main_gain": "preferred-frame coefficients mapped and vector no-hair route written",
        "open_debt": "vector/domain/boundary no-hair not parent-derived",
        "rollup_class": "conditional_or_budget",
    },
    {
        "checkpoint": 377,
        "source_file": "377-fifth-force-range-coupling-map.md",
        "sector": "fifth_force",
        "status": "fifth_force_range_coupling_contract_written_alphaY_lambdaY_not_parent_derived_row_remains_parameterized_unscored",
        "main_gain": "Yukawa/spectral force-law contract written",
        "open_debt": "alpha_Y(lambda_Y) not parent-derived",
        "rollup_class": "unscored_parameterized",
    },
    {
        "checkpoint": 378,
        "source_file": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "sector": "source_normalization",
        "status": "Meff_flux_conservation_imported_GM_absorption_not_parent_derived_deltaG_Gdot_rows_remain_active",
        "main_gain": "M_eff flux conservation imported and GM absorption tests written",
        "open_debt": "G_eff/GM absorption not parent-derived; delta_G/Gdot active",
        "rollup_class": "conditional_or_active_residual",
    },
    {
        "checkpoint": 379,
        "source_file": "379-class-only-boundary-action-noangular-theorem.md",
        "sector": "boundary",
        "status": "class_only_boundary_action_conditional_noangular_kill_switch_written_not_parent_derived_boundary_coefficients_retained",
        "main_gain": "class-only boundary action would kill angular/vector boundary sources",
        "open_debt": "class-only boundary dependence, radial no-hair, and Ward-owned flux not derived",
        "rollup_class": "conditional_coefficients_retained",
    },
    {
        "checkpoint": 380,
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "sector": "bulk_X",
        "status": "bulk_X_mass_gap_and_source_normalized_force_law_not_parent_derived_alphaX_lambdaX_missing_residual_retained",
        "main_gain": "bulk-X mass-gap/no-hair and source-normalized Yukawa contracts written",
        "open_debt": "m_X, q_X, Q_X, q_test, source-free exterior, and alpha_X(lambda_X) missing",
        "rollup_class": "conditional_residual_retained",
    },
]


LOCAL_GR_DEBT_LEDGER = [
    {
        "gate": "single_observed_coframe_and_universal_matter_coupling",
        "needed_for_GR": "all matter, photons, clocks, rulers, and standards couple to one observed geometry",
        "current_evidence": "360 conditionally kills direct WEP/clock vertices; 373 labels one-coframe/common-F as closure",
        "status": "not_parent_derived",
        "residual_if_open": "eta_WEP, alpha_clock, nonmetric light/ruler, species charge",
        "next_action": "derive parent coframe/common-F selector or keep WEP closure explicit",
    },
    {
        "gate": "projected_metric_or_lifted_C_parent_selector",
        "needed_for_GR": "projected/class metric must be selected by gauge/relative exactness rather than closure",
        "current_evidence": "362 rejects scalar Cperp exactness and demotes projected metric; 364-366 give lifted-C conditional route",
        "status": "closure_or_conditional_only",
        "residual_if_open": "common-mode phi_C, clock/gamma/fifth-force leakage",
        "next_action": "derive lifted-C parent action, boundary primitive, and class selector",
    },
    {
        "gate": "topological_class_selection",
        "needed_for_GR": "physical local class/representative selected without hand choosing local triviality",
        "current_evidence": "367 demotes class selection to labelled closure",
        "status": "not_parent_derived",
        "residual_if_open": "local class metric residuals and closure-only local silence",
        "next_action": "derive physical domain/class selector or keep closure branch labelled",
    },
    {
        "gate": "common_mode_phiC_zero_or_bound",
        "needed_for_GR": "common-mode class metric contribution must vanish or be source-bounded locally",
        "current_evidence": "370 maps coefficients; 372 gives conditional zero theorem with gradient fallback",
        "status": "conditional_or_budget_only",
        "residual_if_open": "clock redshift, gamma, fifth-force, WEP common-mode leakage",
        "next_action": "derive boundary-state/trivial-class premises or carry gradient coefficients",
    },
    {
        "gate": "source_locked_local_bound_manifest",
        "needed_for_GR": "if residuals remain, they must be mapped to real local bounds without fake passes",
        "current_evidence": "369/374 build budget-only/source-locked rows",
        "status": "test_ready_budget_only",
        "residual_if_open": "gamma, beta, eta_WEP, clock, alpha_i, xi, Gdot, alpha_Y(lambda)",
        "next_action": "use for stress tests only until coefficients are parent-derived",
    },
    {
        "gate": "EH_exterior_operator",
        "needed_for_GR": "surviving local exterior equations reduce to metric-only EH plus Lambda",
        "current_evidence": "375 writes residual modified-gravity operator ledger and says EH is not parent-derived",
        "status": "central_blocker",
        "residual_if_open": "higher curvature, scalar/vector/torsion/nonlocal/source-normalization operators",
        "next_action": "derive metric-only second-order diffeo exterior or retain modified-gravity coefficients",
    },
    {
        "gate": "preferred_frame_vector_nohair",
        "needed_for_GR": "no vector/marker/domain normal leakage into alpha1 alpha2 alpha3 xi",
        "current_evidence": "376 maps coefficients; vector no-hair remains conditional",
        "status": "conditional_or_budget_only",
        "residual_if_open": "alpha1, alpha2, alpha3, xi",
        "next_action": "derive vector/domain no-hair or carry coefficients into local runner",
    },
    {
        "gate": "fifth_force_range_coupling",
        "needed_for_GR": "extra scalar/radial/bulk/nonlocal force is theorem-zero or has alpha(lambda)",
        "current_evidence": "377 writes alpha_Y(lambda_Y) contract but derives no alpha_Y",
        "status": "unscored_parameterized",
        "residual_if_open": "delta_G_or_fifth_force_yukawa",
        "next_action": "derive profile/range/coupling or keep row unscored",
    },
    {
        "gate": "source_normalization_and_GM_absorption",
        "needed_for_GR": "kappa, G_eff, M_eff, measured GM, and time constancy fixed",
        "current_evidence": "378 imports M_eff flux conservation but GM absorption is not parent-derived",
        "status": "conditional_or_active_residual",
        "residual_if_open": "delta_G, Gdot/G, beta, fifth-force, WEP source dependence",
        "next_action": "derive source normalization or keep delta_G/Gdot active",
    },
    {
        "gate": "boundary_nohair",
        "needed_for_GR": "boundary leaves at most constant universal conserved monopole",
        "current_evidence": "379 gives conditional no-angular kill switch but retains boundary coefficients",
        "status": "conditional_coefficients_retained",
        "residual_if_open": "eps_B_TF, eps_B0i, eps_B_rad, eps_B_flux, eps_B_clock_WEP",
        "next_action": "derive class-only/Ward-owned boundary action or retain coefficients",
    },
    {
        "gate": "bulk_X_nohair_or_force_law",
        "needed_for_GR": "bulk X is theorem-zero, auxiliary/gauge no-hair, or source-normalized Yukawa scored",
        "current_evidence": "380 writes mass-gap and alpha_X(lambda_X) contracts but does not derive them",
        "status": "conditional_residual_retained",
        "residual_if_open": "epsilon_bulk, gamma/beta bulk terms, delta_G/fifth-force, WEP if charged",
        "next_action": "derive positive source-free operator or source-normalized alpha_X(lambda_X)",
    },
]


LOCAL_OBSERVABLE_ROWS = [
    {
        "observable": "gamma_minus_1",
        "source_lock": "2.3e-5",
        "active_sources": "boundary shear/radial hair, bulk X, scalar/common-mode, higher-curvature, nonmetric light",
        "current_status": "budget_only_coefficients_missing",
    },
    {
        "observable": "beta_minus_1",
        "source_lock": "7.8e-5",
        "active_sources": "radial boundary hair, nonlinear boundary/source normalization, bulk X, non-EH operators",
        "current_status": "budget_only_coefficients_missing",
    },
    {
        "observable": "eta_WEP",
        "source_lock": "2.8e-15",
        "active_sources": "species class response, direct nonmetric matter charge, X test charge, source normalization species split",
        "current_status": "hardest_ready_gate_active",
    },
    {
        "observable": "alpha_clock_redshift",
        "source_lock": "3.1e-5",
        "active_sources": "clock metric mismatch, common-mode phi_C, WEP/coframe closure",
        "current_status": "budget_only_coefficients_missing",
    },
    {
        "observable": "alpha1",
        "source_lock": "1.0e-4",
        "active_sources": "vector marker, boundary B_0i, domain normal/coframe vector leakage",
        "current_status": "budget_only_after_source_lock",
    },
    {
        "observable": "alpha2",
        "source_lock": "2.0e-9",
        "active_sources": "anisotropic coframe, vector/domain leakage, boundary B_0i",
        "current_status": "budget_only_after_source_lock",
    },
    {
        "observable": "alpha3",
        "source_lock": "4.0e-20 contingent",
        "active_sources": "unowned boundary flux, momentum nonconservation, Ward-force leakage",
        "current_status": "contingent_budget_only",
    },
    {
        "observable": "xi",
        "source_lock": "4.0e-9",
        "active_sources": "trace-free boundary shear, domain/external anisotropy, projector/vector leakage",
        "current_status": "budget_only_after_source_lock",
    },
    {
        "observable": "Gdot_over_G",
        "source_lock": "9.6e-15 yr^-1 contingent",
        "active_sources": "G_eff/M_eff drift, time-dependent monopole, memory/source normalization, boundary flux",
        "current_status": "contingent_budget_only",
    },
    {
        "observable": "delta_G_or_fifth_force_yukawa",
        "source_lock": "alpha_Y(lambda_Y) / alpha_X(lambda_X)",
        "active_sources": "phi_C profile, bulk X, radial boundary hair, nonlocal kernel, source normalization",
        "current_status": "parameterized_unscored",
    },
]


CLAIM_POLICY = [
    {
        "claim": "MTS derives local GR",
        "allowed": "no",
        "reason": "WEP/coframe, EH exterior, boundary no-hair, bulk X, fifth-force, and source-normalization gates remain open",
    },
    {
        "claim": "MTS local branch is dead",
        "allowed": "no",
        "reason": "conditional theorem routes exist and no contradiction has been derived",
    },
    {
        "claim": "MTS has a coherent local-GR reduction programme",
        "allowed": "yes_internal",
        "reason": "the gate ladder and residual ledgers are explicit and source mapped",
    },
    {
        "claim": "MTS passes WEP/PPN/preferred-frame/fifth-force tests",
        "allowed": "no",
        "reason": "source locks exist but parent coefficients/range laws are missing",
    },
    {
        "claim": "Local empirical testing can proceed",
        "allowed": "yes_budget_only",
        "reason": "runs may stress retained coefficients and closure branches without pass claims",
    },
    {
        "claim": "The next theory target is a parent action contract",
        "allowed": "yes",
        "reason": "the debt ledger shows the missing pieces are action-level selectors/operators, not just numeric fits",
    },
]


NEXT_ACTIONS = [
    {
        "priority": 1,
        "target": "382-parent-local-action-minimal-contract.md",
        "why": "many gates now need the same thing: a parent action that selects coframe, class, boundary, source, and X sectors together",
        "pass_condition": "contract lists exact action-level terms and variation identities required to close local GR",
    },
    {
        "priority": 2,
        "target": "383-local-bound-runner-v2-from-retained-residuals.md",
        "why": "if derivations fail, retained coefficients need stress testing without fake PPN pass claims",
        "pass_condition": "runner rows separate derived-zero, closure-zero, budget-only, and unscored residuals",
    },
    {
        "priority": 3,
        "target": "384-one-coframe-boundary-bulk-joint-nohair-attempt.md",
        "why": "WEP, boundary, and bulk X are coupled; proving them separately may be too weak",
        "pass_condition": "derive or reject a joint no-hair/one-coframe mechanism",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Checkpoints 360-380 have turned the local-GR problem from vague hope into a finite debt ledger. The route is coherent but not promoted: WEP/coframe selection, EH exterior selection, boundary no-hair, source normalization, fifth-force range/coupling, and bulk-X no-hair all remain conditional, closure-labelled, retained, or unscored.",
        "best_news": "the theory now has exact kill-switch shapes and residual maps for the main local monsters",
        "worst_news": "none of the kill switches is parent-derived strongly enough to claim local GR",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
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
    for checkpoint in CHECKPOINT_STATUS:
        source_path = ROOT / checkpoint["source_file"]
        rows.append(
            {
                "source_file": checkpoint["source_file"],
                "exists": source_path.exists(),
                "sector": checkpoint["sector"],
                "role": f"checkpoint {checkpoint['checkpoint']} source for local-GR debt rollup",
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    central_open = [
        row["gate"]
        for row in LOCAL_GR_DEBT_LEDGER
        if row["status"]
        in {
            "not_parent_derived",
            "central_blocker",
            "conditional_residual_retained",
            "conditional_coefficients_retained",
            "unscored_parameterized",
            "closure_or_conditional_only",
            "conditional_or_active_residual",
        }
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "checkpoint_status_rollup_written",
            "status": "pass",
            "evidence": f"{len(CHECKPOINT_STATUS)} checkpoints rolled up from 360 through 380",
        },
        {
            "gate": "local_GR_debt_ledger_written",
            "status": "pass",
            "evidence": f"{len(LOCAL_GR_DEBT_LEDGER)} local-GR gates classified",
        },
        {
            "gate": "observable_rows_separated",
            "status": "pass",
            "evidence": f"{len(LOCAL_OBSERVABLE_ROWS)} observable rows mapped to source locks and active sources",
        },
        {
            "gate": "derived_local_GR_claim_allowed",
            "status": "fail",
            "evidence": f"open_gates={len(central_open)}; {','.join(central_open[:6])}",
        },
        {
            "gate": "local_branch_dead_claim_allowed",
            "status": "fail",
            "evidence": "conditional theorem routes remain coherent",
        },
        {
            "gate": "empirical_pass_claim_allowed",
            "status": "fail",
            "evidence": "source locks exist but coefficients/range laws are missing",
        },
        {
            "gate": "budget_only_testing_allowed",
            "status": "pass",
            "evidence": "retained residual rows can be stress-tested with no pass claims",
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
    write_csv(results_dir / "checkpoint_status_rollup.csv", CHECKPOINT_STATUS)
    write_csv(results_dir / "local_GR_debt_ledger.csv", LOCAL_GR_DEBT_LEDGER)
    write_csv(results_dir / "local_observable_rows.csv", LOCAL_OBSERVABLE_ROWS)
    write_csv(results_dir / "claim_policy.csv", CLAIM_POLICY)
    write_csv(results_dir / "next_actions.csv", NEXT_ACTIONS)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    open_gate_count = sum(
        1
        for row in LOCAL_GR_DEBT_LEDGER
        if row["status"]
        not in {
            "test_ready_budget_only",
        }
    )
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "checkpoints_rolled_up": len(CHECKPOINT_STATUS),
        "local_GR_gates_classified": len(LOCAL_GR_DEBT_LEDGER),
        "open_or_conditional_gate_count": open_gate_count,
        "derived_local_GR_claim_allowed": False,
        "empirical_pass_claim_allowed": False,
        "budget_only_testing_allowed": True,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 381 local-GR debt ledger rollup artifacts."
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
