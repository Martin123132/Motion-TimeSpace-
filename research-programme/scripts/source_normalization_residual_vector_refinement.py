from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-normalization-residual-vector-refinement"
CHECKPOINT_DOC = "444-source-normalization-residual-vector-refinement.md"
STATUS = "source_normalization_residual_vector_refinement_written_measured_GM_not_parent_derived_P8_demoted_to_source_residual_vector_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "source_normalization_residual_vector_only_no_WEP_EH_Newton_PPN_R10_R11_or_local_GR_pass"
NEXT_TARGET = "445-measured-GM-Ward-source-ownership-theorem-attempt.md"
P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
P8_R11_TEMPLATE_PATH = Path("source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv")


R11_VECTOR_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


P8_RESIDUAL_COLUMNS = [
    "model_id",
    "branch_id",
    "component_id",
    "symbol",
    "definition",
    "units",
    "normalization",
    "affected_rows",
    "observable_link",
    "bound_or_target",
    "residual_input",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


SOURCE_DOCS = [
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and mu_obs normalization chain",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "local GR/Newton stack partition and no-promotion policy",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "source-normalization channel plan and local-bound test matrix",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "12-row residual-vector input contract",
    },
    {
        "path": "431-MTS-local-residual-vector-evaluator.md",
        "role": "residual evaluator rules blocking symbolic pass-through",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P8 constant source-normalization rung",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "source-normalization retained sector row",
    },
    {
        "path": "441-extra-sector-nohair-priority-gate.md",
        "role": "source-normalization selected as parallel Newton lane",
    },
    {
        "path": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
        "role": "previous P4 checkpoint and next-target handoff",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/same_frame_theorem_pair.csv",
        "role": "same-frame theorem pair and source-normalization blockers",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/weak_field_chain.csv",
        "role": "EH to G_eff to mu_obs weak-field chain",
    },
    {
        "path": "runs/20260602-043500-EH-source-normalization-parent-pair/results/source_normalization_tests.csv",
        "role": "source-normalization test rows from the parent-pair checkpoint",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/source_normalization_channel_plan.csv",
        "role": "source-normalization channel split",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/local_bound_test_matrix.csv",
        "role": "local-bound tests and baseline policy",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/row_transition_attempt.csv",
        "role": "R0-R11 row-state transitions",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "canonical R0-R11 residual components",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/local_GR_pass_requirements.csv",
        "role": "local-GR pass requirements and measured-GM row",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/prediction_template_rows.csv",
        "role": "MTS local residual prediction template rows",
    },
    {
        "path": "runs/20260602-105000-MTS-local-residual-vector-evaluator/results/evaluator_rules.csv",
        "role": "numeric/symbolic evaluator gates",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "sourced local-bound claims for R1/R4/R9/R10/R11",
    },
    {
        "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "existing 12-row MTS residual template",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "canonical R11 template containing source-normalization operator row",
    },
]


P8_PROBLEM_STATEMENT = [
    {
        "item": "P8_target",
        "statement": "derive that measured gravitational source strength is constant, conserved, universal, and range independent in the observed local branch",
        "mathematical_form": "mu_obs = G_eff M_eff + mu_extra with partial_{t,r,A,lambda} mu_obs=0 and mu_extra=0",
        "current_status": "central_Newton_blocker_not_parent_derived",
    },
    {
        "item": "why_it_matters",
        "statement": "EH-shaped equations are not measured Newtonian gravity unless kappa/G_eff and the source monopole are normalized to what orbital dynamics measures",
        "mathematical_form": "nabla^2 Phi = 4 pi G_eff rho_eff is Newton only after G_eff M_eff = GM_measured",
        "current_status": "conditional_only",
    },
    {
        "item": "legal_success",
        "statement": "the parent action owns every exchange/source channel so that source charge, boundary/domain/bulk memory, radial hair, and finite-range leakage vanish",
        "mathematical_form": "delta_mu_species=delta_mu_time=delta_mu_range=delta_mu_radial=delta_mu_extra=0",
        "current_status": "not_derived",
    },
    {
        "item": "legal_failure",
        "statement": "if any source-normalization component survives, it must be a named residual component with units, bound, row mapping, and source path",
        "mathematical_form": "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "current_status": "template_written_by_this_checkpoint",
    },
]


MU_OBS_DECOMPOSITION = [
    {
        "term": "baseline_monopole",
        "symbol": "G_eff M_eff",
        "definition": "same-frame gravitational coupling times conserved effective source monopole",
        "safe_condition": "constant, conserved, species-independent, range-independent measured GM",
        "affected_rows": "R1;R4;R9;R10",
    },
    {
        "term": "coupling_drift",
        "symbol": "delta_G(t,r,A)",
        "definition": "time, radial, frame, or species dependence in kappa_eff or G_eff",
        "safe_condition": "partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "affected_rows": "R1;R4;R9;R11",
    },
    {
        "term": "source_charge",
        "symbol": "delta_M_A",
        "definition": "material/species dependence in the effective source or test charge",
        "safe_condition": "partial_A mu_obs=0 across materials and source compositions",
        "affected_rows": "R1;R11",
    },
    {
        "term": "source_flux_or_nonconservation",
        "symbol": "dot_M_eff or Phi_boundary",
        "definition": "boundary, bulk, domain, or memory exchange changing the measured mass monopole",
        "safe_condition": "dM_eff/dt=0 and no unowned exterior flux",
        "affected_rows": "R4;R7;R9;R11",
    },
    {
        "term": "finite_range_source_hair",
        "symbol": "delta_mu_lambda(r)",
        "definition": "range-dependent fifth-force/source normalization correction",
        "safe_condition": "partial_lambda mu_obs=0 or alpha(lambda) curve below sourced bounds",
        "affected_rows": "R10;R11",
    },
    {
        "term": "radial_or_boundary_hair",
        "symbol": "delta_mu_r",
        "definition": "radial source profile, boundary hair, domain shear, or bulk load not reducible to a constant monopole",
        "safe_condition": "partial_r mu_obs=0 and boundary/domain terms are Ward-owned or coefficient-mapped",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
    },
    {
        "term": "frame_calibration_split",
        "symbol": "delta_frame",
        "definition": "matter and gravity evaluate source strength in different observed frames/coframes",
        "safe_condition": "one observed frame and universal calibration for matter, clocks, rods, photons, and source charge",
        "affected_rows": "R0;R2;R11",
    },
]


SOURCE_DERIVATION_ROUTES = [
    {
        "route_id": "P8_R0_EH_Poisson_if_assumed",
        "route_claim": "if EH plus same-frame source normalization is already derived, Poisson algebra gives Newtonian measured GM",
        "required_parent_evidence": "P1/P4/P6/P8/P9 closed plus mu_extra=0",
        "result": "conditional_Newton_chain",
        "status": "pass_conditional_not_derivation",
        "why_not_enough": "this route assumes P8 rather than deriving constant measured GM",
    },
    {
        "route_id": "P8_R1_Ward_exchange_owner_identity",
        "route_claim": "Bianchi/Ward identities force every source-exchange term into an owned conserved current with no exterior flux",
        "required_parent_evidence": "explicit current decomposition showing q_loc^nu, boundary flux, domain exchange, and memory load integrate to zero source residual",
        "result": "would_kill_mu_extra",
        "status": "not_supplied",
        "why_not_enough": "current corpus has Ward/exchange contracts but not the integrated measured-GM theorem",
    },
    {
        "route_id": "P8_R2_universal_matter_source_charge",
        "route_claim": "all matter species and source compositions couple to one universal source charge",
        "required_parent_evidence": "no material marker, class label, bulk charge, torsion/projective source charge, or species spurion in source action",
        "result": "would_close_R1_source_channel",
        "status": "not_parent_derived",
        "why_not_enough": "direct WEP proxy does not prove the full source-normalization channel",
    },
    {
        "route_id": "P8_R3_conserved_monopole_no_flux",
        "route_claim": "compact ordinary source has a conserved local monopole and no boundary/domain/bulk flux into orbital dynamics",
        "required_parent_evidence": "source continuity equation plus no-boundary-flux/no-domain-exchange theorem in the observed frame",
        "result": "would_close_mass_conservation_and_Gdot_piece",
        "status": "not_parent_derived",
        "why_not_enough": "boundary, bulk, domain, and memory channels are still retained elsewhere",
    },
    {
        "route_id": "P8_R4_no_finite_range_source_hair",
        "route_claim": "source normalization has no radius/range dependence and no finite-range extra charge",
        "required_parent_evidence": "alpha(lambda)=0 by theorem or executable alpha(lambda) curve below sourced inverse-square bounds",
        "result": "would_close_R10_or_make_it_empirical",
        "status": "not_derived_symbolic",
        "why_not_enough": "symbolic fifth-force placeholders cannot pass the evaluator",
    },
    {
        "route_id": "P8_R5_empirical_source_residual_vector",
        "route_claim": "retain all source-normalization leakage as a component vector and compare each component to sourced local bounds",
        "required_parent_evidence": "numeric residuals, units, normalizations, source paths, and same-pipeline GR/null baselines",
        "result": "modified_or_stress_test_branch_only",
        "status": "residual_vector_demotion",
        "why_not_enough": "empirical smallness can keep the branch viable but is not theorem-zero Newton/GR reduction",
    },
]


P8_RESIDUAL_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_Geff_time_drift",
        "symbol": "dln_Geff_dt",
        "definition": "time drift of G_eff or kappa_eff in the observed local branch",
        "units": "yr^-1",
        "normalization": "d ln G_eff / dt or d ln kappa_eff / dt",
        "affected_rows": "R9;R11",
        "observable_link": "Gdot_over_G",
        "bound_or_target": "9.6e-15 yr^-1 or derived zero",
        "residual_input": "fill_numeric_drift_or_derived_zero_source",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "d ln mu_obs/dt = d ln(G_eff M_eff)/dt",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_clock_source_memory_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; cosmological memory success cannot override local Gdot lock",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_Meff_conservation",
        "symbol": "dln_Meff_dt",
        "definition": "time drift or nonconservation of measured effective source mass",
        "units": "yr^-1",
        "normalization": "d ln M_eff / dt after separating G_eff drift",
        "affected_rows": "R4;R9;R11",
        "observable_link": "beta_minus_1;Gdot_over_G",
        "bound_or_target": "beta/Gdot locks or derived conservation",
        "residual_input": "fill_mass_flux_or_conservation_proof",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_obs = G_eff M_eff + mu_extra",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_compact_source_no_flux_no_memory_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; source mass conservation must be owned, not assumed",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_species_source_charge",
        "symbol": "partial_A_ln_mu_obs or eta_source_AB",
        "definition": "composition/species dependence of the gravitational source charge",
        "units": "dimensionless",
        "normalization": "eta_source_AB or species derivative of ln mu_obs",
        "affected_rows": "R1;R11",
        "observable_link": "eta_WEP_source_charge",
        "bound_or_target": "2.8e-15 or derived universal source charge",
        "residual_input": "fill_species_source_charge_or_no_marker_proof",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_A mu_obs = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_species_material_marker_source_charge_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; direct WEP proxy is not the full source-normalization proof",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_range_dependence",
        "symbol": "partial_lambda_ln_mu_obs or alpha(lambda)",
        "definition": "range-dependent source strength or finite-range force correction",
        "units": "range-dependent",
        "normalization": "alpha(lambda) curve or derivative of ln mu_obs with range scale",
        "affected_rows": "R10;R11",
        "observable_link": "delta_G_or_fifth_force_yukawa",
        "bound_or_target": "verified alpha(lambda) bound curve or derived zero",
        "residual_input": "fill_curve_path_or_no_finite_range_charge_proof",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_lambda mu_obs = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_screening_range_source_charge_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; symbolic R10 cannot pass without executable curve or theorem-zero",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_radial_source_hair",
        "symbol": "partial_r_ln_mu_obs",
        "definition": "radial dependence of the measured source strength after monopole extraction",
        "units": "inverse_length_or_dimensionless_envelope",
        "normalization": "radial derivative or residual envelope relative to GM_measured",
        "affected_rows": "R3;R4;R10;R11",
        "observable_link": "gamma_minus_1;beta_minus_1;alpha(lambda)",
        "bound_or_target": "zero radial hair or mapped PPN/fifth-force residuals",
        "residual_input": "fill_radial_profile_or_nohair_proof",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_r mu_obs = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_compact_exterior_boundary_radial_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; radial dependence is physics, not calibration",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "symbol": "mu_extra_boundary_bulk_domain",
        "definition": "extra measured-GM contribution from boundary, bulk, domain, projector, or memory exchange channels",
        "units": "dimensionless_or_GM_units_after_normalization",
        "normalization": "mu_extra / (G_eff M_eff) or explicit GM units",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "observable_link": "gamma;beta;alpha3;xi;Gdot;operator_ledger",
        "bound_or_target": "zero owned exchange or coefficient residuals below row locks",
        "residual_input": "fill_exchange_coefficients_or_Ward_owner_proof",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_extra = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_boundary_bulk_domain_projector_memory_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; alpha3 lock is especially severe for unowned exchange",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_frame_calibration_split",
        "symbol": "delta_frame_source",
        "definition": "difference between matter-frame source calibration and gravity-frame source calibration",
        "units": "dimensionless",
        "normalization": "relative frame/source calibration residual",
        "affected_rows": "R0;R2;R11",
        "observable_link": "eta_WEP_direct_geometry;clock_redshift;operator_ledger",
        "bound_or_target": "one observed frame or explicit residual below row locks",
        "residual_input": "fill_frame_split_residual_or_parent_frame_theorem",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "same observed e/coframe for matter and metric source variation",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_matter_metric_source_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; calibration cannot hide frame split",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "component_id": "P8_nonlinear_beta_source_residue",
        "symbol": "delta_beta_source",
        "definition": "second-order nonlinear source-normalization residue after first-order Poisson matching",
        "units": "dimensionless",
        "normalization": "beta_minus_1 contribution assigned to source normalization",
        "affected_rows": "R4;R11",
        "observable_link": "beta_minus_1",
        "bound_or_target": "7.8e-05 or derived second-order source closure",
        "residual_input": "fill_beta_source_piece_or_second_order_derivation",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "PPN beta after measured-GM normalization",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_second_order_PPN_source_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 template only; first-order Poisson success does not clear beta",
    },
]


P8_R11_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "source_normalization_operator",
        "coefficient_symbol": "c_source_or_mu_extra",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_GM_units_or_dimensionless_after_normalization",
        "normalization": "fill_relative_to_G_eff_M_eff_or_EH_source_scale",
        "operator_form": "mu_obs = G_eff M_eff + mu_extra with source-normalization operator corrections",
        "weak_field_map": "fill_R1_R4_R9_R10_R11_source_residual_map",
        "affected_rows": "R1;R4;R9;R10;R11",
        "induced_observable": "eta_source;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
        "predicted_residual_or_bound_source": "fill_P8_source_normalization_residual_vector_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_obs = G_eff M_eff + mu_extra",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_constant_universal_conserved_range_independent_source_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; measured-GM normalization is not a calibration if any derivative/channel survives",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "species_source_charge",
        "coefficient_symbol": "c_A_or_partial_A_mu",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "dimensionless",
        "normalization": "fill_eta_source_or_species_derivative_normalization",
        "operator_form": "partial_A mu_obs or material-marker/source-charge coupling",
        "weak_field_map": "fill_WEP_source_charge_map",
        "affected_rows": "R1;R11",
        "induced_observable": "eta_WEP_source_charge;operator_ledger",
        "predicted_residual_or_bound_source": "fill_species_source_residual_or_bound_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_A mu_obs = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_no_material_marker_species_universality_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; direct geometry WEP does not automatically clear this row",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "time_drift_source_memory",
        "coefficient_symbol": "c_t_or_dln_mu_dt",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "yr^-1",
        "normalization": "fill_dln_mu_obs_dt_or_dln_Geff_dt",
        "operator_form": "partial_t mu_obs from G_eff drift, M_eff drift, memory, or flux exchange",
        "weak_field_map": "fill_Gdot_and_beta_source_map",
        "affected_rows": "R4;R9;R11",
        "induced_observable": "beta_minus_1;Gdot_over_G;operator_ledger",
        "predicted_residual_or_bound_source": "fill_Gdot_source_residual_or_bound_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "d ln mu_obs/dt = d ln(G_eff M_eff + mu_extra)/dt",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_memory_flux_conservation_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; local Gdot lock remains active",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "range_dependent_GM_fifth_force",
        "coefficient_symbol": "c_lambda_or_alpha_lambda",
        "coefficient_value": "fill_numeric_curve_or_zero",
        "coefficient_units": "range-dependent",
        "normalization": "fill_alpha_lambda_curve_normalization",
        "operator_form": "partial_lambda mu_obs or finite-range source-hair potential",
        "weak_field_map": "fill_alpha_lambda_curve_path",
        "affected_rows": "R10;R11",
        "induced_observable": "alpha(lambda);operator_ledger",
        "predicted_residual_or_bound_source": "fill_alpha_lambda_curve_or_theorem_zero_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_lambda mu_obs = 0 or alpha(lambda)",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_range_screening_source_charge_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; no symbolic fifth-force pass",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "boundary_bulk_domain_mass_charge",
        "coefficient_symbol": "c_BXD_or_mu_extra_BXD",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "dimensionless_or_GM_units_after_normalization",
        "normalization": "fill_mu_extra_over_Geff_Meff_or_flux_normalization",
        "operator_form": "boundary/bulk/domain/projector/memory contribution to mu_extra",
        "weak_field_map": "fill_gamma_beta_alpha3_xi_Gdot_source_map",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha3;xi;Gdot_over_G;operator_ledger",
        "predicted_residual_or_bound_source": "fill_exchange_coefficients_or_Ward_owner_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_extra[B,X,D,J,P] = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_boundary_bulk_domain_projector_memory_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; unowned exchange hits the alpha3/Gdot rows hard",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P8_source_normalization_rows",
        "operator_family": "frame_calibration_source_split",
        "coefficient_symbol": "c_frame_source",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "dimensionless",
        "normalization": "fill_relative_source_frame_calibration",
        "operator_form": "matter-frame and metric-frame source calibration mismatch",
        "weak_field_map": "fill_WEP_clock_operator_map",
        "affected_rows": "R0;R2;R11",
        "induced_observable": "eta_WEP_direct_geometry;clock_redshift;operator_ledger",
        "predicted_residual_or_bound_source": "fill_frame_source_residual_or_theorem_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "same observed frame for source and metric variation",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_same_frame_source_calibration_assumptions",
        "valid_for_claim": "false",
        "notes": "P8 R11 template only; calibration cannot hide a frame split",
    },
]


P8_GATE_TESTS = [
    {
        "gate": "constant_coupling_gate",
        "pass_condition": "kappa_eff/G_eff is constant and universal in the observed branch",
        "current_result": "fail_open",
        "evidence": "constant_kappa_to_Geff is not parent-derived",
    },
    {
        "gate": "conserved_monopole_gate",
        "pass_condition": "M_eff is the conserved mass/source monopole measured by orbital dynamics",
        "current_result": "fail_open",
        "evidence": "boundary, bulk, domain, and memory exchange can still alter measured mass",
    },
    {
        "gate": "species_universality_gate",
        "pass_condition": "partial_A mu_obs=0 across species/material/source labels",
        "current_result": "fail_open",
        "evidence": "full source-charge row remains retained even if direct WEP proxy is available",
    },
    {
        "gate": "range_independence_gate",
        "pass_condition": "partial_lambda mu_obs=0 or executable alpha(lambda) curve passes sourced bounds",
        "current_result": "demote_to_R10_R11",
        "evidence": "R10 remains symbolic until a curve or theorem-zero is supplied",
    },
    {
        "gate": "radial_boundary_silence_gate",
        "pass_condition": "partial_r mu_obs=0 and all boundary/bulk/domain mu_extra terms are Ward-owned or coefficient-mapped",
        "current_result": "fail_open",
        "evidence": "boundary and exchange rows remain retained with severe alpha3/Gdot locks",
    },
    {
        "gate": "same_frame_source_calibration_gate",
        "pass_condition": "source calibration uses the same observed metric/coframe as matter, clocks, photons, and gravity",
        "current_result": "conditional_open",
        "evidence": "same-frame route is coherent but not parent-derived",
    },
    {
        "gate": "source_residual_vector_gate",
        "pass_condition": "all surviving source-normalization components have executable residuals or derived zeros",
        "current_result": "template_only",
        "evidence": str(P8_TEMPLATE_PATH),
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "P8 residual components refined",
        "status": "pass",
        "evidence": "8 component residual vector written with affected rows and bounds",
    },
    {
        "claim": "EH to Poisson algebra preserved",
        "status": "pass_conditional",
        "evidence": "weak-field chain remains valid if same-frame EH/source normalization premises are derived",
    },
    {
        "claim": "measured GM parent-derived",
        "status": "fail",
        "evidence": "no parent theorem proves partial_{t,r,A,lambda} mu_obs=0 and mu_extra=0",
    },
    {
        "claim": "source-normalization theorem-zero",
        "status": "fail",
        "evidence": "species, time, radial, range, boundary/bulk/domain, and frame-calibration channels remain legal",
    },
    {
        "claim": "P8 demoted to executable residual vector",
        "status": "pass",
        "evidence": str(P8_TEMPLATE_PATH),
    },
    {
        "claim": "P8 source operator demoted to R11 rows",
        "status": "pass",
        "evidence": str(P8_R11_TEMPLATE_PATH),
    },
    {
        "claim": "WEP/EH/Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "P8 refinement only; no source residual data and no local-GR pass",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "P8_problem_statement_written",
        "status": "pass",
        "evidence": "P8 target, success, and failure conditions recorded",
    },
    {
        "gate": "mu_obs_decomposition_written",
        "status": "pass",
        "evidence": "7 decomposition terms recorded",
    },
    {
        "gate": "source_derivation_routes_audited",
        "status": "pass",
        "evidence": "6 routes audited",
    },
    {
        "gate": "P8_residual_template_written",
        "status": "pass",
        "evidence": str(P8_TEMPLATE_PATH),
    },
    {
        "gate": "P8_R11_template_written",
        "status": "pass",
        "evidence": str(P8_R11_TEMPLATE_PATH),
    },
    {
        "gate": "measured_GM_parent_derived",
        "status": "fail",
        "evidence": "constant, conserved, universal, range-independent measured GM remains unproved",
    },
    {
        "gate": "mu_extra_zero_derived",
        "status": "fail",
        "evidence": "boundary/bulk/domain/memory/source extra terms remain retained",
    },
    {
        "gate": "source_residual_data_supplied",
        "status": "fail",
        "evidence": "template rows only; no numeric residuals, curves, or theorem-zero sources supplied",
    },
    {
        "gate": "Newtonian_reduction_promoted",
        "status": "fail",
        "evidence": "EH-shaped Poisson algebra is conditional until P8 closes",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "P8 audit only; no WEP/EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "P8 is now split into an exact source-normalization residual vector. The clean Newtonian route is still alive: if the parent action proves one observed frame, constant G_eff, conserved universal M_eff, no mu_extra, no radial/range dependence, and no boundary/bulk/domain/source charge leakage, then the EH-to-Poisson chain becomes measured Newtonian GM. The current corpus does not derive those identities. Therefore measured GM is not promoted; P8 is demoted to an executable residual-vector template plus R11 source-normalization rows.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "why_next": "try the actual derivation: prove Ward/Bianchi exchange ownership kills mu_extra and source drift",
    },
    {
        "rank": 2,
        "target": "fill P8_source_normalization_residual_vector_TEMPLATE.csv",
        "why_next": "if the theorem fails, source residuals need numeric values, bounds, curves, and source paths",
    },
    {
        "rank": 3,
        "target": "connect P8 residual components into runner-v4 evaluator",
        "why_next": "measured-GM residuals must be scored against GR/null baselines without symbolic pass-through",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    p8_template_schema_gate = {
        "gate": "P8_template_schema_matches_contract",
        "status": "pass" if list(P8_RESIDUAL_TEMPLATE_ROWS[0].keys()) == P8_RESIDUAL_COLUMNS else "fail",
        "evidence": "P8 residual template columns match source-normalization residual schema"
        if list(P8_RESIDUAL_TEMPLATE_ROWS[0].keys()) == P8_RESIDUAL_COLUMNS
        else "P8 residual template schema mismatch",
    }
    r11_template_schema_gate = {
        "gate": "P8_R11_template_schema_matches_R11",
        "status": "pass" if list(P8_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS else "fail",
        "evidence": "P8 R11 template columns match canonical R11 vector schema"
        if list(P8_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS
        else "P8 R11 template schema mismatch",
    }
    return [source_gate, p8_template_schema_gate, r11_template_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 444 - Source-Normalization Residual Vector Refinement

Private Newton/source-normalization checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R10/R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 443 closed the immediate connection fork by demoting torsion/nonmetricity to R11 unless the parent action derives Levi-Civita compatibility. This checkpoint attacks the parallel Newton lane: can the current corpus derive measured `GM`, or must source normalization become an explicit residual vector?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_residual_vector_refinement.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| P8 residual template | `{P8_TEMPLATE_PATH}` |
| P8 R11 template | `{P8_R11_TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. P8 Problem Statement

{markdown_table(P8_PROBLEM_STATEMENT, ["item", "statement", "mathematical_form", "current_status"])}

## 5. Measured-GM Decomposition

{markdown_table(MU_OBS_DECOMPOSITION, ["term", "symbol", "definition", "safe_condition", "affected_rows"])}

## 6. Source-Derivation Routes

{markdown_table(SOURCE_DERIVATION_ROUTES, ["route_id", "route_claim", "result", "status", "why_not_enough"])}

## 7. P8 Source Residual Template Rows

The P8 source-normalization residual template has been written to `{P8_TEMPLATE_PATH}`.

{markdown_table(P8_RESIDUAL_TEMPLATE_ROWS, P8_RESIDUAL_COLUMNS)}

## 8. P8 R11 Source-Operator Rows

The P8-specific R11 template has been written to `{P8_R11_TEMPLATE_PATH}`.

{markdown_table(P8_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)}

## 9. P8 Gate Tests

{markdown_table(P8_GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 10. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is the Newton round card. If MTS derives P8, it gets to say the local EH branch really lands on measured Newtonian gravity. If it cannot, it can still fight as a modified branch, but every source-normalization move must show its component, units, bound, and baseline. No hiding a jab under the towel.

## 13. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "P8_problem_statement.csv", P8_PROBLEM_STATEMENT)
    write_csv(results_dir / "mu_obs_decomposition.csv", MU_OBS_DECOMPOSITION)
    write_csv(results_dir / "source_derivation_routes.csv", SOURCE_DERIVATION_ROUTES)
    write_csv(results_dir / "P8_source_residual_template_rows.csv", P8_RESIDUAL_TEMPLATE_ROWS, P8_RESIDUAL_COLUMNS)
    write_csv(results_dir / "P8_R11_source_operator_rows.csv", P8_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "P8_gate_tests.csv", P8_GATE_TESTS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / P8_TEMPLATE_PATH, P8_RESIDUAL_TEMPLATE_ROWS, P8_RESIDUAL_COLUMNS)
    write_csv(ROOT / P8_R11_TEMPLATE_PATH, P8_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "P8_residual_components": len(P8_RESIDUAL_TEMPLATE_ROWS),
        "P8_R11_source_operator_rows": len(P8_R11_TEMPLATE_ROWS),
        "source_derivation_routes": len(SOURCE_DERIVATION_ROUTES),
        "measured_GM_parent_derived": False,
        "mu_extra_zero_derived": False,
        "source_residual_data_supplied": False,
        "P8_promoted": False,
        "WEP_promoted": False,
        "EH_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "P8_template_path": str(ROOT / P8_TEMPLATE_PATH),
        "P8_R11_template_path": str(ROOT / P8_R11_TEMPLATE_PATH),
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 444 source-normalization residual-vector refinement artifacts."
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
