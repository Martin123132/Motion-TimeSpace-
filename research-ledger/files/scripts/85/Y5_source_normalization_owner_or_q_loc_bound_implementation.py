from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_source_normalization_owner_theorem_attempt_written_current_MTS_not_derived_bound_runner_input_written"
CLAIM_CEILING = "Y5_owner_or_bound_input_only_no_source_normalized_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "519-fill-Y5-bound-runner-or-source-owner-clause.md"

DOC_PATH = Path("518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_SOURCE_REGISTER.csv")
OWNER_THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv")
EVEN_SCALAR_GATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_EVEN_SCALAR_GATE.csv")
AMPLITUDE_LAW_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_AMPLITUDE_LAW.csv")
BOUND_RUNNER_INPUT_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "role": "selects Y5 source normalization as the next hard blocker after formal response-doublet variation",
    },
    {
        "source_file": "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "role": "Gamma_eff owner candidate and q_loc bound runner specification",
    },
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "source-measure M_eff flux closure contract and residual map",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue and Meff residual runner",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal local GR fixed-point parent-action contract",
    },
    {
        "source_file": "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
        "role": "even scalar source-normalization theorem stack",
    },
    {
        "source_file": "497-source-normalization-derived-zero-route-or-numeric-input-template.md",
        "role": "eight-channel source-normalization derived-zero or numeric routing",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "radial M_eff and calibration source-normalization theorem attempt",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "exact parent source identity and radial fallback template",
    },
    {
        "source_file": "508-constant-kappa-superselection-or-drift-residual.md",
        "role": "constant kappa/G_eff superselection gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "role": "Y0-Y6 response-doublet Euler source ledger with Y5 marked hard fail",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
        "role": "q_loc residual-bound trigger ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "role": "q_loc residual-bound runner specification",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
        "role": "source-normalization theorem-zero targets",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
        "role": "source-normalization numeric input templates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "source-normalization residual vector template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton branch stack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source-measure M_eff flux residual map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "worldtube M_eff residual runner rows",
    },
    {
        "source_file": "scripts/Y5_source_normalization_owner_or_q_loc_bound_implementation.py",
        "role": "this checkpoint generator",
    },
]


OWNER_THEOREM_ROWS = [
    {
        "owner_id": "Y5O_0_observable_split",
        "required_statement": "Observed local source strength is split before calibration into an owned EH/Hilbert source charge plus explicit extra source-normalization terms.",
        "math_form": "mu_obs = G_eff M_H[Pi_M J_H] + mu_extra = G_eff M_H (1 + epsilon_mu)",
        "if_derived": "Y5 is no longer a hidden fitted GM parameter; every deviation is either owned source charge or explicit residual",
        "current_status": "definition_written_not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_1_same_observed_coframe",
        "required_statement": "Matter variation, clocks, photons, source current, exterior charge, and orbital readout use one observed coframe.",
        "math_form": "e_obs = e_matter = e_source = e_charge = e_orbit",
        "if_derived": "source normalization cannot hide in a frame split",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_2_constant_universal_coupling",
        "required_statement": "The local coupling is constant, universal, source-blind, range-blind, and frame-blind.",
        "math_form": "partial_t,r,A,lambda,frame G_eff = 0, equivalently partial kappa_eff = 0",
        "if_derived": "no Gdot, fifth-force, species, radial, or frame derivative can masquerade as measured GM",
        "current_status": "conditional_from_508_not_current_MTS_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_3_parent_source_charge",
        "required_statement": "The measured source mass is a parent Noether/Hamiltonian/Hilbert mass charge, not an orbital fit.",
        "math_form": "M_H[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
        "if_derived": "M_eff has a source-side owner before Kepler readout",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_4_flux_closure",
        "required_statement": "The projected Hilbert mass current is closed in compact source-free exterior regions.",
        "math_form": "M_H(S2)-M_H(S1) = integral_A d(Pi_M J_H); d(Pi_M J_H)=0",
        "if_derived": "no radial M_eff hair or local source-mass drift survives",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_5_no_extra_mass_projection",
        "required_statement": "Boundary, domain, projector, bulk, memory, non-EH, frame, species, and calibration channels carry no independent mass projection.",
        "math_form": "mu_extra = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_cal + Delta_PPN = 0",
        "if_derived": "epsilon_mu=0 rather than a tuned or cancelled source-normalization coefficient",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_6_Gauss_orbital_calibration",
        "required_statement": "The closed parent charge normalizes to the inverse-square orbital coefficient with one universal G_ref.",
        "math_form": "a_r = -G_ref M_H/r^2 + controlled_PPN_terms",
        "if_derived": "Kepler/Newton measured GM becomes a consequence, not an input",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_7_second_order_PPN_stability",
        "required_statement": "The same source charge remains stable through beta/gamma/preferred-frame PPN order.",
        "math_form": "Delta_PPN_source = {gamma-1, beta-1, alpha_i, xi, zeta_i}_source = 0 or explicitly bounded",
        "if_derived": "local Newton does not pass while local GR quietly fails at second order",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "owner_id": "Y5O_8_owner_theorem",
        "required_statement": "If Y5O_1 through Y5O_7 hold together, source normalization is an owned local GR/Newton consequence.",
        "math_form": "mu_obs = G0 M_H; d ln mu_obs = 0; epsilon_mu = 0; Y5_source_normalization = 0",
        "if_derived": "Y5 closes as a theorem rather than a plateau axiom or fitted GM absorption",
        "current_status": "theorem_written_current_MTS_does_not_satisfy_premises",
        "valid_for_claim": "false",
    },
]


EVEN_SCALAR_GATE_ROWS = [
    {
        "gate_id": "ES518_0_exchange_parity",
        "issue": "Y5 is an observed even scalar source strength, not an exchange-odd leakage variable.",
        "test": "Does Z -> -Z force mu_obs or epsilon_mu to vanish?",
        "result": "fail_for_physical_Y5",
        "claim_effect": "response-doublet parity alone cannot prove source-normalized Newton",
    },
    {
        "gate_id": "ES518_1_auxiliary_double_zero",
        "issue": "The quadratic Gamma_eff action can zero an auxiliary Z component.",
        "test": "partial_A Gamma_eff|Z=0 = 0",
        "result": "pass_conditional_for_auxiliary_Z",
        "claim_effect": "formal F_1 route survives but does not close physical measured-GM residuals",
    },
    {
        "gate_id": "ES518_2_physical_lock",
        "issue": "The auxiliary Y5/Z component must be proven equal to the measured source-normalization residual.",
        "test": "Z_Y5 = epsilon_mu and mu_extra terms through weak-field/PPN order",
        "result": "not_derived",
        "claim_effect": "Y5 remains an active local-GR blocker",
    },
    {
        "gate_id": "ES518_3_no_cancellation_policy",
        "issue": "Large open terms cannot be hidden by cancellation between G_eff, M_eff, and mu_extra.",
        "test": "Each derivative/source channel must be theorem-zero or individually bounded before claim credit",
        "result": "policy_pass_theorem_fail",
        "claim_effect": "a fit can be recorded, but not counted as derived local GR",
    },
    {
        "gate_id": "ES518_4_bound_branch_trigger",
        "issue": "If the source owner theorem is not derived, Y5 must become a residual vector.",
        "test": "Bound runner has rows for Gdot, Mdot, radial, species, range, frame, mu_extra, beta/PPN, and q_loc projection",
        "result": "pass_input_written_not_scored",
        "claim_effect": "testability preserved with no Newton/PPN promotion",
    },
]


AMPLITUDE_LAW_ROWS = [
    {
        "law_id": "AL518_0_source_split",
        "statement": "Define the source-normalization amplitude epsilon_mu by the owned source split.",
        "math_form": "epsilon_mu := mu_extra/(G_eff M_H), so mu_obs = G_eff M_H (1 + epsilon_mu)",
        "interpretation": "Y5 is exactly the failure of observed measured-GM to be just one constant coupling times one owned source charge",
        "claim_status": "definition_only",
    },
    {
        "law_id": "AL518_1_local_derivative_law",
        "statement": "The local source-strength derivative splits into coupling, mass-flux, and extra-source pieces.",
        "math_form": "d ln mu_obs = d ln G_eff + d ln M_H + d ln(1 + epsilon_mu)",
        "interpretation": "constant measured GM follows only if all three terms are zero or an explicitly justified cancellation is scored as a fit",
        "claim_status": "exact_identity_after_definition",
    },
    {
        "law_id": "AL518_2_small_residual_law",
        "statement": "For small source-normalization residuals, the amplitude is additive.",
        "math_form": "Delta mu_obs/mu_obs ~= Delta ln G_eff + Delta ln M_H + Delta epsilon_mu",
        "interpretation": "the runner can score Gdot, Mdot, radial hair, species charge, range dependence, and extra-sector mass charge separately",
        "claim_status": "bound_runner_identity",
    },
    {
        "law_id": "AL518_3_finite_shell_bound",
        "statement": "A conservative finite-shell bound avoids relying on cancellation.",
        "math_form": "|Delta mu/mu| <= |Delta ln G_eff| + |Delta ln M_H| + |Delta epsilon_mu|/(1-|epsilon_mu|)",
        "interpretation": "a nonzero Y5 branch can still be tested against local/orbital bounds without pretending it is derived",
        "claim_status": "bound_runner_policy",
    },
    {
        "law_id": "AL518_4_owner_zero_limit",
        "statement": "The theorem limit is a true zero, not a fitted plateau.",
        "math_form": "partial G_eff = 0, d(Pi_M J_H)=0, mu_extra=0 => epsilon_mu=0 and d ln mu_obs=0",
        "interpretation": "this is the exact local-GR/Newton source-normalization target",
        "claim_status": "conditional_not_current_MTS_derived",
    },
]


BOUND_RUNNER_INPUT_ROWS = [
    {
        "bound_id": "Y5B_0_Geff_time_drift",
        "component_id": "P8_Geff_time_drift",
        "symbol": "dln_Geff_dt",
        "definition": "time drift of G_eff or kappa_eff in the observed local source branch",
        "units": "yr^-1",
        "normalization": "d ln G_eff / dt",
        "affected_rows": "R9;R11;Y5",
        "observable_link": "Gdot_over_G",
        "bound_or_target": "<= 9.6e-15 yr^-1 or derived zero",
        "residual_input": "fill_numeric_drift_or_derived_zero_source",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "d ln mu_obs = d ln G_eff + d ln M_H + d ln(1+epsilon_mu)",
        "source_file": "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "assumptions": "same observed clock and source frame",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_1_Meff_conservation",
        "component_id": "P8_Meff_conservation",
        "symbol": "dln_Meff_dt",
        "definition": "time drift or nonconservation of measured effective source mass after separating coupling drift",
        "units": "yr^-1",
        "normalization": "d ln M_eff / dt",
        "affected_rows": "R4;R9;R11;Y5",
        "observable_link": "GMdot_or_Gdot_after_G_split",
        "bound_or_target": "<= 9.6e-15 yr^-1 proxy until separate GMdot bound is sourced, or derived zero",
        "residual_input": "fill_mass_flux_or_conservation_proof",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "M_eff(S2)-M_eff(S1)=integral_A d(Pi_M J_H)",
        "source_file": "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "assumptions": "compact source exterior and fixed source measure",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_2_radial_source_hair",
        "component_id": "P8_radial_source_hair",
        "symbol": "partial_r_ln_mu_obs",
        "definition": "radial dependence of the measured source strength after monopole extraction",
        "units": "inverse_length_or_dimensionless_shell_envelope",
        "normalization": "radial derivative or finite-shell Delta mu/mu relative to GM_measured",
        "affected_rows": "R3;R4;R10;R11;Y5",
        "observable_link": "orbital residuals; beta_minus_1; alpha(lambda)",
        "bound_or_target": "zero radial hair or mapped PPN/fifth-force residuals",
        "residual_input": "fill_radial_profile_or_nohair_proof",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "epsilon_radial_Meff = integral_A d(Pi_M J_H)/M_eff",
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "assumptions": "linked compact exterior shells and no hidden calibration absorption",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_3_species_source_charge",
        "component_id": "P8_species_source_charge",
        "symbol": "eta_source_AB",
        "definition": "composition/species dependence of gravitational source charge",
        "units": "dimensionless",
        "normalization": "species derivative of ln mu_obs or source-side eta_AB",
        "affected_rows": "R1;R2;R11;Y5",
        "observable_link": "source-side WEP and clock/source residual",
        "bound_or_target": "<= 2.8e-15 or selector-blind source theorem",
        "residual_input": "fill_species_source_charge_or_no_marker_proof",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "partial_A mu_obs = 0",
        "source_file": "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "assumptions": "material labels do not enter source charge pullback",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_4_range_dependence",
        "component_id": "P8_range_dependence",
        "symbol": "alpha(lambda)",
        "definition": "finite-range or scale-dependent source strength correction",
        "units": "dimensionless_plus_length_scale",
        "normalization": "Yukawa alpha(lambda) curve or derivative of ln mu_obs with range scale",
        "affected_rows": "R10;R11;Y5",
        "observable_link": "fifth-force and range-dependent G tests",
        "bound_or_target": "verified alpha(lambda) curve below local bounds or derived mass-gap zero",
        "residual_input": "fill_curve_path_or_no_finite_range_charge_proof",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "partial_lambda mu_obs = 0",
        "source_file": "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
        "assumptions": "same source normalization across the relevant length scale",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_5_extra_mass_projection",
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "symbol": "mu_extra_boundary_bulk_domain",
        "definition": "extra measured-GM contribution from boundary, bulk, domain, projector, memory, or non-EH channels",
        "units": "dimensionless_or_GM_units_after_normalization",
        "normalization": "mu_extra/(G_eff M_eff)",
        "affected_rows": "R3;R4;R7;R8;R9;R11;Y5",
        "observable_link": "gamma;beta;alpha3;xi;Gdot;operator_ledger",
        "bound_or_target": "zero owned exchange or coefficient residuals below row locks; alpha3 <= 4e-20 where applicable",
        "residual_input": "fill_exchange_coefficients_or_Ward_owner_proof",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "mu_obs = G_eff M_H + mu_extra",
        "source_file": "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "assumptions": "channelwise accounting with no unsourced cancellation",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_6_frame_calibration_split",
        "component_id": "P8_frame_calibration_split",
        "symbol": "delta_frame_source",
        "definition": "difference between matter-frame source calibration and gravity/orbital readout frame",
        "units": "dimensionless",
        "normalization": "relative frame/source calibration residual",
        "affected_rows": "R0;R2;R11;Y5",
        "observable_link": "WEP geometry; clock redshift; preferred-frame source residual",
        "bound_or_target": "one observed frame theorem or explicit residual below row locks",
        "residual_input": "fill_frame_split_residual_or_parent_frame_theorem",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "e_obs = e_matter = e_source = e_orbit",
        "source_file": "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "assumptions": "source and readout frames are not calibrated separately",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_7_beta_source_tail",
        "component_id": "P8_nonlinear_beta_source_residue",
        "symbol": "delta_beta_source",
        "definition": "second-order nonlinear source-normalization residue after first-order Poisson matching",
        "units": "dimensionless",
        "normalization": "beta_minus_1 contribution assigned to source normalization",
        "affected_rows": "R4;R11;Y5",
        "observable_link": "PPN beta and perihelion-style second-order source closure",
        "bound_or_target": "<= 7.8e-05 or derived second-order source closure",
        "residual_input": "fill_beta_source_piece_or_second_order_derivation",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "PPN beta after measured-GM normalization",
        "source_file": "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "assumptions": "first-order Poisson success is not counted as PPN source stability",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_8_full_PPN_source_vector",
        "component_id": "P8_PPN_source_vector",
        "symbol": "Delta_PPN_source",
        "definition": "full PPN residual vector sourced by source-normalization or q_loc leakage",
        "units": "dimensionless_vector",
        "normalization": "{gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i}_source",
        "affected_rows": "R3;R4;R5;R6;R7;R8;R11;Y5",
        "observable_link": "solar-system PPN tests",
        "bound_or_target": "gamma<=2.3e-5; beta<=7.8e-5; alpha1<=1e-4; alpha2<=2e-9; alpha3<=4e-20; xi<=4e-9 or derived zero",
        "residual_input": "fill_PPN_source_map_or_parent_PPN_expansion",
        "current_value": "missing",
        "derivation_status": "not_scored",
        "formula_reference": "Delta_PPN depends only on explicit Delta rows after source equality",
        "source_file": "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "assumptions": "weak-field metric solution sourced by q_loc/Y5 is known",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_9_q_loc_projection",
        "component_id": "P8_q_loc_source_normalization_projection",
        "symbol": "C_qmu q_loc",
        "definition": "projection from q_loc stress-divergence residual into measured-GM/source-normalization channel",
        "units": "mixed_until_projection_fixed",
        "normalization": "source-normalization component of P_loc(nabla Gamma_eff - nabla K_hat)",
        "affected_rows": "Y5;R11;q_loc",
        "observable_link": "measured-GM residual vector and compact-shell leakage budget",
        "bound_or_target": "compact-shell proxy 7.432631961576971e-06 must be mapped into PPN/source-normalization units before scoring",
        "residual_input": "fill_q_loc_to_mu_projection_operator",
        "current_value": "missing_projection",
        "derivation_status": "not_scored",
        "formula_reference": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
        "source_file": "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "assumptions": "C_qmu normalization and units are derived or explicitly bounded",
        "pass_state": "open",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D518_0_owner_attempt",
        "status": "conditional_theorem_written",
        "meaning": "Y5 can close only if measured GM is one constant coupling times one parent-owned Hilbert/Noether source charge with zero extra mass projection",
        "claim_status": "not_current_MTS_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D518_1_even_scalar",
        "status": "exchange_odd_insufficient",
        "meaning": "response-doublet parity can supply a formal auxiliary double-zero but cannot by itself kill the physical even measured-GM residual",
        "claim_status": "Y5_blocker_active",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D518_2_amplitude_law",
        "status": "exact_identity_written",
        "meaning": "Y5 amplitude is now split into G_eff drift, M_eff flux, and epsilon_mu/mu_extra pieces",
        "claim_status": "runner_ready_not_scored",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D518_3_bound_branch",
        "status": "input_rows_written",
        "meaning": "q_loc/source-normalization fallback rows are explicit but all current values remain missing or unscored",
        "claim_status": "test_branch_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D518_4_promotion",
        "status": "forbidden",
        "meaning": "no source-normalized Newton, PPN, or local-GR claim is earned until owner premises are derived or residual rows are scored below gates",
        "claim_status": "local_GR_claim_false",
        "next_action": "derive owner clauses or fill bound runner from source-backed inputs",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5_SOURCE_NORMALIZATION",
        "previous_status": "hard_fail_current_from_response_doublet_ledger",
        "new_status": "owner_theorem_contract_written_current_MTS_not_derived_bound_runner_input_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RESPONSE_DOUBLET_LOCAL_GR",
        "previous_status": "formal_double_zero_survives_Y5_Y6_blockers_active",
        "new_status": "formal_auxiliary_zero_not_enough_for_even_measured_GM_without_Y5_owner_lock",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_by_source_measure_flux_and_extra_mass_projection",
        "new_status": "blocked_until_mu_obs_equals_G0_parent_source_charge_with_no_derivative_hair",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "QLOC_BOUND_BRANCH",
        "previous_status": "runner_spec_written_not_scored",
        "new_status": "Y5_specific_q_loc_projection_and_source_normalization_bound_inputs_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_Y5_source_normalization_Y6_stress_Bianchi_PPN_lock",
        "new_status": "still_blocked_Y5_sharpened_to_owner_or_bound_gate",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": full_path.exists(),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    euler_rows = read_csv(Path("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv"))
    trigger_rows = read_csv(Path("source-intake/mts_residuals/P8_QLOC_BOUND_TRIGGER_LEDGER.csv"))
    qloc_spec_rows = read_csv(Path("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv"))
    source_template_rows = read_csv(Path("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv"))
    y5_rows = [row for row in euler_rows if row.get("component_id") == "Y5_source_normalization"]
    claim_owner_rows = [row for row in OWNER_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in BOUND_RUNNER_INPUT_ROWS if row["valid_for_claim"] == "true"]
    required_bound_ids = {
        "Y5B_0_Geff_time_drift",
        "Y5B_1_Meff_conservation",
        "Y5B_2_radial_source_hair",
        "Y5B_3_species_source_charge",
        "Y5B_4_range_dependence",
        "Y5B_5_extra_mass_projection",
        "Y5B_6_frame_calibration_split",
        "Y5B_7_beta_source_tail",
        "Y5B_8_full_PPN_source_vector",
        "Y5B_9_q_loc_projection",
    }
    bound_ids = {row["bound_id"] for row in BOUND_RUNNER_INPUT_ROWS}
    return [
        {
            "check_id": "V518_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V518_1_prior_Y5_loaded",
            "result": "pass" if len(y5_rows) == 1 else "fail",
            "detail": f"euler_rows={len(euler_rows)};Y5_rows={len(y5_rows)}",
        },
        {
            "check_id": "V518_2_bound_priors_loaded",
            "result": "pass" if len(trigger_rows) >= 5 and len(qloc_spec_rows) >= 5 and len(source_template_rows) >= 8 else "fail",
            "detail": f"trigger_rows={len(trigger_rows)};qloc_spec_rows={len(qloc_spec_rows)};source_template_rows={len(source_template_rows)}",
        },
        {
            "check_id": "V518_3_owner_theorem_complete",
            "result": "pass" if len(OWNER_THEOREM_ROWS) == 9 else "fail",
            "detail": f"owner_rows={len(OWNER_THEOREM_ROWS)}",
        },
        {
            "check_id": "V518_4_amplitude_law_present",
            "result": "pass" if len(AMPLITUDE_LAW_ROWS) == 5 else "fail",
            "detail": f"amplitude_rows={len(AMPLITUDE_LAW_ROWS)}",
        },
        {
            "check_id": "V518_5_bound_runner_coverage",
            "result": "pass" if required_bound_ids.issubset(bound_ids) else "fail",
            "detail": ";".join(sorted(bound_ids)),
        },
        {
            "check_id": "V518_6_no_overclaim",
            "result": "pass" if not claim_owner_rows and not claim_bound_rows else "fail",
            "detail": f"claim_owner_rows={len(claim_owner_rows)};claim_bound_rows={len(claim_bound_rows)};Y5_owner_derived_for_MTS=false;Y5_bound_runner_scored=false;local_GR_claim_allowed=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 518 - Y5 Source Normalization Owner or q_loc Bound Implementation

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

Y5 is now sharper.

The clean route is not "the motion field has a local plateau." The clean route is:

```text
mu_obs = G_eff M_H[Pi_M J_H] + mu_extra
       = G_eff M_H (1 + epsilon_mu)
```

and local Newton/GR source normalization follows only if the parent action proves:

```text
G_eff = G0,
d(Pi_M J_H)=0,
mu_extra=0,
and the same source charge survives PPN order.
```

That is a real derivation target, not dead paperwork. But the current MTS corpus does not yet prove the premises. So the branch is not promoted; the fallback q_loc/source-normalization bound runner input is now explicit.

## 2. Owner Theorem Attempt

{markdown_table(OWNER_THEOREM_ROWS)}

## 3. Even-Scalar Gate

{markdown_table(EVEN_SCALAR_GATE_ROWS)}

## 4. Local Amplitude Law

{markdown_table(AMPLITUDE_LAW_ROWS)}

## 5. Bound Runner Input

{markdown_table(BOUND_RUNNER_INPUT_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS now has an exact Y5 source-normalization owner theorem contract.
The local source-strength amplitude law is explicit.
The q_loc/source-normalization fallback runner has concrete input rows.
```

Forbidden:

```text
MTS has derived source-normalized Newtonian recovery.
MTS has derived Y5_source_normalization = 0 for the current parent action.
MTS has mapped q_loc into source-normalization/PPN units and scored it.
MTS has derived local GR or PPN silence.
```

## 11. What This Means

This is still a live route, but only through one of two honest doors:

```text
Door A: derive the source owner theorem from the parent action.
Door B: fill the Y5 bound runner with sourced residuals and show every open channel is below local gates.
```

No cancellation or calibration shortcut gets derivation credit.

## 12. Next Target

`{NEXT_TARGET}`

Either fill the Y5 bound runner with source-backed/theorem-zero inputs, or derive one missing owner clause strongly enough to remove a bound row.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-source-normalization-owner-or-q_loc-bound-implementation"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (OWNER_THEOREM_PATH, OWNER_THEOREM_ROWS),
        (EVEN_SCALAR_GATE_PATH, EVEN_SCALAR_GATE_ROWS),
        (AMPLITUDE_LAW_PATH, AMPLITUDE_LAW_ROWS),
        (BOUND_RUNNER_INPUT_PATH, BOUND_RUNNER_INPUT_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "owner_theorem": str(ROOT / OWNER_THEOREM_PATH),
        "even_scalar_gate": str(ROOT / EVEN_SCALAR_GATE_PATH),
        "amplitude_law": str(ROOT / AMPLITUDE_LAW_PATH),
        "bound_runner_input": str(ROOT / BOUND_RUNNER_INPUT_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "owner_theorem_rows": len(OWNER_THEOREM_ROWS),
        "even_scalar_gate_rows": len(EVEN_SCALAR_GATE_ROWS),
        "amplitude_law_rows": len(AMPLITUDE_LAW_ROWS),
        "bound_runner_input_rows": len(BOUND_RUNNER_INPUT_ROWS),
        "failed_validation_rows": len(failed_validations),
        "Y5_owner_theorem_written": True,
        "Y5_owner_derived_for_MTS": False,
        "Y5_even_scalar_solved_by_exchange_parity": False,
        "Y5_amplitude_law_written": True,
        "q_loc_bound_runner_input_written": True,
        "Y5_bound_runner_scored": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
