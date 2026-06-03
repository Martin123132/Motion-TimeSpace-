from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-exterior-operator-or-residual-modified-gravity-ledger"
STATUS = "EH_not_parent_derived_residual_operator_ledger_written_modified_gravity_coefficients_retained_no_local_GR_pass"
CLAIM_CEILING = "EH_operator_or_residual_modified_gravity_ledger_only_no_EH_PPN_WEP_fifth_force_or_local_GR_pass"
NEXT_TARGET = "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md"


SOURCE_DOCS = [
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH sufficiency stack: Ward closure is necessary but not enough; second-order metric-only operator remains open",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force channels and retained PPN residual vector feeding operator residuals",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked PPN residual runner policy and ready/quarantined residual rows",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "WEP closure audit: one observed coframe/common F(C_D) not parent-derived",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "preferred-frame/xi source locks and fifth-force Yukawa parameterization policy",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary no-hair residual decomposition: radial, trace-free, vector, conservation flux hazards",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward identity and projector/domain variation context",
    },
    {
        "path": "370-common-mode-phiC-coefficient-map.md",
        "role": "common-mode phi_C weak-field map and clock/gamma/fifth-force budget pressure",
    },
]


EH_ROUTE_STATUS = [
    {
        "premise": "compact_local_exterior",
        "required_statement": "outside ordinary matter support, source appears only as conserved monopole/boundary data",
        "status_after_375": "definition_plus_monopole_condition_open",
        "failure_mode": "radial scalar/boundary charge gives delta_G or fifth-force row",
    },
    {
        "premise": "single_physical_metric_or_coframe",
        "required_statement": "all matter, light, clocks, and rods see one observed geometry",
        "status_after_375": "closure_axiom_not_parent_derived",
        "failure_mode": "eta_WEP and clock/nonmetric residuals remain active",
    },
    {
        "premise": "Ward_force_closure",
        "required_statement": "all parent variation force terms vanish, cancel, or are owned in total conservation",
        "status_after_375": "mapped_not_proved",
        "failure_mode": "unowned selector/boundary flux feeds alpha3, Gdot, beta, and fifth-force rows",
    },
    {
        "premise": "local_nohair",
        "required_statement": "bulk, boundary, projector, vector, and trace-free MTS hair vanish or reduce to conserved monopole",
        "status_after_375": "not_derived",
        "failure_mode": "gamma, xi, preferred-frame, beta, and fifth-force residuals",
    },
    {
        "premise": "metric_only_exterior",
        "required_statement": "no independent scalar, vector, torsion, nonmetricity, or memory kernel propagates locally",
        "status_after_375": "not_parent_derived",
        "failure_mode": "modified-gravity residual operator ledger required",
    },
    {
        "premise": "local_diffeomorphic_4D_second_order_operator",
        "required_statement": "surviving exterior action is local, diffeo invariant, 4D, and gives second-order metric equations",
        "status_after_375": "sufficiency_condition_not_parent_derived",
        "failure_mode": "higher-curvature or nonlocal residual operator survives",
    },
    {
        "premise": "source_normalization",
        "required_statement": "kappa, G_eff, and measured M_eff/GM are fixed by the parent action",
        "status_after_375": "open",
        "failure_mode": "delta_G, Gdot/G, or fifth-force normalization ambiguity",
    },
]


DERIVATION_ATTEMPT_STEPS = [
    {
        "step": 1,
        "statement": "Assume the full local sufficiency stack from checkpoint 358.",
        "equation": "Ward closure + no hair + universal metric coupling + metric-only local 4D second-order diffeo action",
        "result": "EH follows conditionally",
        "status": "conditional_theorem",
    },
    {
        "step": 2,
        "statement": "Remove any premise that is not parent-derived.",
        "equation": "metric-only, second-order, source normalization, universal coframe, and no-hair are still open",
        "result": "EH no longer follows",
        "status": "actual_current_branch",
    },
    {
        "step": 3,
        "statement": "Write the honest exterior action when EH is not derived.",
        "equation": "S_ext = S_EH + sum_i c_i O_i + S_boundary/topological",
        "result": "modified-gravity residual operator ledger",
        "status": "required",
    },
    {
        "step": 4,
        "statement": "Each coefficient must be theorem-zero, source-bounded, or explicitly unscored.",
        "equation": "c_i in {0 by theorem, bounded by runner, quarantined}",
        "result": "no silent deletion of non-EH operators",
        "status": "discipline_rule",
    },
    {
        "step": 5,
        "statement": "Do not promote local GR until every residual operator channel is closed.",
        "equation": "EH_pass = all(c_i controlled) and universal coupling and source normalization",
        "result": "local_GR_pass_forbidden_now",
        "status": "fail_promotion",
    },
]


OPERATOR_BASIS_RESIDUAL_LEDGER = [
    {
        "operator_family": "Einstein_Hilbert_plus_Lambda",
        "schematic_operator": "sqrt(-g) (R - 2 Lambda)",
        "would_be_effect": "GR exterior baseline with negligible local Lambda",
        "MTS_status": "target_if_sufficiency_stack_derived",
        "residual_policy": "not enough by itself because stack is not parent-derived",
    },
    {
        "operator_family": "boundary_or_topological_terms",
        "schematic_operator": "GHY; Euler/Gauss-Bonnet topological pieces; relative-class boundary terms",
        "would_be_effect": "no bulk PPN effect if owned and class-only",
        "MTS_status": "allowed_conditionally",
        "residual_policy": "retain boundary shear/vector/flux if ownership not proved",
    },
    {
        "operator_family": "higher_curvature_scalar",
        "schematic_operator": "c_R2 R^2 or f(R)",
        "would_be_effect": "extra scalar mode, Yukawa force, gamma/beta shifts",
        "MTS_status": "not_forbidden",
        "residual_policy": "derive c_R2=0 or map mass/range/coupling into fifth-force and PPN rows",
    },
    {
        "operator_family": "higher_curvature_spin2_or_Weyl",
        "schematic_operator": "c_Ricci R_mn R^mn + c_W Weyl^2",
        "would_be_effect": "spin-2/higher-derivative correction, trace-free shear, light bending/slip risk",
        "MTS_status": "not_forbidden",
        "residual_policy": "derive zero by low-energy theorem or bound gamma/xi/wave/slip effects",
    },
    {
        "operator_family": "scalar_tensor_or_class_metric",
        "schematic_operator": "F(C_D) R, (nabla C_D)^2, V(C_D), phi_C metric factor",
        "would_be_effect": "gamma, beta, clock drift, fifth force, WEP if species-specific",
        "MTS_status": "conditional local phi_C silence only",
        "residual_policy": "zero by local-class theorem or retain clock/gamma/fifth-force/WEP rows",
    },
    {
        "operator_family": "vector_or_preferred_frame",
        "schematic_operator": "u^m u^n R_mn, B_0i operators, marker/domain-normal couplings",
        "would_be_effect": "alpha1, alpha2, alpha3, xi, preferred-location effects",
        "MTS_status": "not_nohair_derived",
        "residual_policy": "derive vector no-hair or coefficient-map alpha1/alpha2/alpha3/xi",
    },
    {
        "operator_family": "torsion_or_nonmetricity",
        "schematic_operator": "T^2, Q^2, independent connection couplings",
        "would_be_effect": "spin, WEP, clock, light-cone, matter-coupling residuals",
        "MTS_status": "not_a_lead_branch_but_not_globally_excluded",
        "residual_policy": "forbid by metric/coframe compatibility theorem or retain nonmetric residuals",
    },
    {
        "operator_family": "nonlocal_or_memory_kernel",
        "schematic_operator": "R Box^-1 R, history/domain kernels, delayed boundary response",
        "would_be_effect": "scale-dependent delta_G, fifth-force, secular drift, Gdot/G, cosmology-local leakage",
        "MTS_status": "not_parent_excluded",
        "residual_policy": "prove local kernel silence/screening or retain nonlocal modified-gravity row",
    },
    {
        "operator_family": "source_normalization_operator",
        "schematic_operator": "kappa(C_D), G_eff(C_D), M_eff boundary charge",
        "would_be_effect": "measured-GM ambiguity, delta_G, Gdot/G, fifth-force normalization",
        "MTS_status": "open",
        "residual_policy": "derive conserved universal monopole absorption or score as delta_G/Gdot channel",
    },
]


COEFFICIENT_TO_OBSERVABLE_MAP = [
    {
        "coefficient": "c_R2_or_fR",
        "observable_rows": "gamma_minus_1;beta_minus_1;delta_G_or_fifth_force_yukawa",
        "ready_bound_status": "gamma_beta_ready;fifth_force_parameterized",
        "needed_MTS_derivation": "mass/range and coupling of scalar mode or theorem c_R2=0",
    },
    {
        "coefficient": "c_Ricci_or_c_Weyl",
        "observable_rows": "gamma_minus_1;xi_preferred_location_anisotropy;lensing_slip;wave_sector_if_used",
        "ready_bound_status": "gamma_xi_ready_internal;wave_sector_not_in_this_runner",
        "needed_MTS_derivation": "trace-free/shear coefficient and local low-energy suppression",
    },
    {
        "coefficient": "c_scalar_class_phiC",
        "observable_rows": "alpha_clock_redshift;gamma_minus_1;delta_G_or_fifth_force_yukawa;eta_WEP_if_species_specific",
        "ready_bound_status": "clock_gamma_eta_ready;fifth_force_parameterized",
        "needed_MTS_derivation": "local phi_C zero theorem, universal F(C_D), or gradient/range map",
    },
    {
        "coefficient": "c_vector_marker",
        "observable_rows": "preferred_frame_alpha1;preferred_frame_alpha2;preferred_frame_alpha3;xi_preferred_location_anisotropy",
        "ready_bound_status": "preferred_frame_xi_ready_internal",
        "needed_MTS_derivation": "vector no-hair or weak-field alpha_i coefficient map",
    },
    {
        "coefficient": "c_torsion_nonmetricity",
        "observable_rows": "eta_WEP;alpha_clock_redshift;nonmetric_light;spin_coupling",
        "ready_bound_status": "WEP_clock_ready;spin/nonmetric_light not separately source-locked here",
        "needed_MTS_derivation": "metric/coframe compatibility and no direct matter connection split",
    },
    {
        "coefficient": "c_nonlocal_memory",
        "observable_rows": "Gdot_over_G;delta_G_or_fifth_force_yukawa;secular_orbital_drift;cosmology_local_leakage",
        "ready_bound_status": "Gdot_contingent;fifth_force_parameterized",
        "needed_MTS_derivation": "local kernel silence, screening scale, and conservation ledger",
    },
    {
        "coefficient": "c_source_norm",
        "observable_rows": "delta_G_or_fifth_force_yukawa;Gdot_over_G;Newtonian_limit",
        "ready_bound_status": "Gdot_contingent;fifth_force_parameterized",
        "needed_MTS_derivation": "kappa/G_eff/M_eff map and universal GM absorption theorem",
    },
]


SOURCE_BOUND_JOIN = [
    {
        "residual": "gamma_minus_1",
        "source_locked_scale": 2.3e-5,
        "operator_sources": "higher_curvature;trace_free_shear;scalar_tensor;nonmetric_light",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale": 7.8e-5,
        "operator_sources": "higher_curvature;radial_scalar_hair;nonlinear_boundary;source_normalization",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "eta_WEP",
        "source_locked_scale": 2.8e-15,
        "operator_sources": "species_specific_metric;nonmetricity;direct_class_response",
        "current_status": "ready_budget_only_WEP_closure_required",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale": 3.1e-5,
        "operator_sources": "clock_metric_mismatch;phiC_gradient;varying_constants",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha1",
        "source_locked_scale": 1.0e-4,
        "operator_sources": "vector_marker;domain_normal;coframe_slip",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha2",
        "source_locked_scale": 2.0e-9,
        "operator_sources": "vector_marker;domain_normal;anisotropic coframe",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "preferred_frame_alpha3",
        "source_locked_scale": 4.0e-20,
        "operator_sources": "unowned_flux;momentum_nonconservation;preferred_frame_vector",
        "current_status": "contingent_budget_only_if_channel_exists",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_locked_scale": 4.0e-9,
        "operator_sources": "trace_free_boundary_shear;external_domain_anisotropy;Weyl_squared",
        "current_status": "ready_budget_only_coefficients_missing",
    },
    {
        "residual": "Gdot_over_G",
        "source_locked_scale": "9.6e-15 yr^-1",
        "operator_sources": "time_varying_G_eff;nonlocal_memory_kernel;source_normalization_drift",
        "current_status": "contingent_budget_only_if_channel_exists",
    },
    {
        "residual": "delta_G_or_fifth_force_yukawa",
        "source_locked_scale": "alpha_Y(lambda_Y), not one scalar",
        "operator_sources": "scalar_hair;bulk_X;phiC_gradient;nonlocal_kernel;source_normalization",
        "current_status": "parameterized_not_scalar_scored",
    },
]


MODIFIED_GRAVITY_BRANCH_CONTRACT = [
    {
        "contract_item": "explicit_residual_action",
        "required_form": "S_ext = S_EH + sum_i c_i O_i + boundary/topological terms",
        "why": "prevents hidden deletion of non-EH operators",
        "status": "written",
    },
    {
        "contract_item": "coefficient_fate",
        "required_form": "each c_i is theorem-zero, source-bounded, or explicitly quarantined",
        "why": "turns modified-gravity leftovers into testable residuals",
        "status": "written",
    },
    {
        "contract_item": "range_and_coupling_for_force_rows",
        "required_form": "derive alpha_Y(lambda_Y) or equivalent a_extra/a_GR map",
        "why": "fifth-force cannot be scored as one scalar",
        "status": "missing",
    },
    {
        "contract_item": "metric_only_or_metric_compatibility",
        "required_form": "no independent scalar/vector/torsion/nonmetricity couples locally, or coefficients are bounded",
        "why": "EH exterior and WEP/clock safety both depend on this",
        "status": "open",
    },
    {
        "contract_item": "source_normalization",
        "required_form": "derive kappa, G_eff, M_eff, and measured GM absorption",
        "why": "Newtonian limit and delta_G/Gdot rows need a fixed source map",
        "status": "open",
    },
    {
        "contract_item": "claim_policy",
        "required_form": "no EH/local-GR promotion until all residual operator rows are controlled",
        "why": "Ward closure and source locks alone are not an EH derivation",
        "status": "enforced",
    },
]


PROMOTION_RULES = [
    {
        "promotion": "conditional_EH_if_full_stack_assumed",
        "allowed": "yes_as_conditional_theorem",
        "current_result": "already sharpened in 358",
        "blocker": "premises not parent-derived",
    },
    {
        "promotion": "parent_EH_operator_derived",
        "allowed": "no",
        "current_result": "fail",
        "blocker": "metric-only, second-order, no-hair, source-normalization, and universal coupling not derived",
    },
    {
        "promotion": "modified_gravity_residuals_testable",
        "allowed": "yes_internal_ledger",
        "current_result": "pass",
        "blocker": "coefficients/ranges missing for actual pass/fail scoring",
    },
    {
        "promotion": "PPN_or_preferred_frame_pass",
        "allowed": "no",
        "current_result": "fail",
        "blocker": "source locks exist but MTS residual coefficients are missing",
    },
    {
        "promotion": "fifth_force_pass",
        "allowed": "no",
        "current_result": "fail",
        "blocker": "alpha_Y(lambda_Y) or force range/coupling map missing",
    },
    {
        "promotion": "local_GR_pass",
        "allowed": "no",
        "current_result": "fail",
        "blocker": "EH derivation, WEP closure, no-hair, source normalization, and residual coefficients open",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The EH exterior follows only conditionally if the full sufficiency stack is assumed. In the actual current branch, EH is not parent-derived; therefore all non-EH operator families must be retained as a modified-gravity residual ledger with coefficients mapped to source-locked or quarantined local rows.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive vector/marker/domain no-hair or map B0i/coframe vector leakage into alpha1/alpha2/alpha3/xi coefficients",
        "pass_condition": "preferred-frame coefficients are theorem-zero or budgeted against source-locked rows",
    },
    {
        "priority": 2,
        "target": "377-fifth-force-range-coupling-map.md",
        "task": "derive alpha_Y(lambda_Y) or another source-normalized force residual for scalar/bulk/phi_C/nonlocal channels",
        "pass_condition": "fifth-force row becomes scalar/range scorable or remains explicitly unscored",
    },
    {
        "priority": 3,
        "target": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "task": "derive kappa, G_eff, M_eff, and measured-GM absorption or keep delta_G/Gdot rows active",
        "pass_condition": "Newtonian source normalization is parent-derived or source-bounded",
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
            "gate": "conditional_EH_theorem_preserved",
            "status": "pass",
            "evidence": "full 358 sufficiency stack still gives EH as a conditional theorem",
        },
        {
            "gate": "parent_EH_operator_derived",
            "status": "fail",
            "evidence": "metric-only, second-order, no-hair, source-normalization, and universal-coupling premises remain open",
        },
        {
            "gate": "residual_operator_ledger_written",
            "status": "pass",
            "evidence": f"{len(OPERATOR_BASIS_RESIDUAL_LEDGER)} operator families mapped",
        },
        {
            "gate": "coefficients_joined_to_observables",
            "status": "pass",
            "evidence": f"{len(COEFFICIENT_TO_OBSERVABLE_MAP)} coefficient families mapped to source-locked or quarantined rows",
        },
        {
            "gate": "fifth_force_scalar_scored",
            "status": "fail",
            "evidence": "alpha_Y(lambda_Y) or equivalent range/coupling map is missing",
        },
        {
            "gate": "source_normalization_derived",
            "status": "fail",
            "evidence": "kappa/G_eff/M_eff/measured-GM map remains open",
        },
        {
            "gate": "PPN_or_preferred_frame_pass_claimed",
            "status": "fail",
            "evidence": "local rows have source locks but no MTS coefficients",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "EH operator is not parent-derived and residual operator coefficients remain active",
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
    write_csv(results_dir / "EH_route_status.csv", EH_ROUTE_STATUS)
    write_csv(results_dir / "derivation_attempt_steps.csv", DERIVATION_ATTEMPT_STEPS)
    write_csv(results_dir / "operator_basis_residual_ledger.csv", OPERATOR_BASIS_RESIDUAL_LEDGER)
    write_csv(results_dir / "coefficient_to_observable_map.csv", COEFFICIENT_TO_OBSERVABLE_MAP)
    write_csv(results_dir / "source_bound_join.csv", SOURCE_BOUND_JOIN)
    write_csv(results_dir / "modified_gravity_branch_contract.csv", MODIFIED_GRAVITY_BRANCH_CONTRACT)
    write_csv(results_dir / "promotion_rules.csv", PROMOTION_RULES)
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
        "operator_families_mapped": len(OPERATOR_BASIS_RESIDUAL_LEDGER),
        "parent_EH_operator_derived": False,
        "local_GR_pass_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 375 EH exterior operator or residual modified-gravity ledger artifacts."
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
