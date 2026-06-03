from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "constant_GM_derivative_hair_fill_gate_written_exact_log_derivative_identity_derived_all_hair_channels_retained_unfilled_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "constant_GM_derivative_hair_gate_only_no_constant_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "466-constant-GM-zero-theorem-or-local-residual-runner.md"

DOC_PATH = Path("465-constant-GM-derivative-hair-fill-gate.md")
DERIVATIVE_GATE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv")
FILL_QUEUE_PATH = Path("source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv")
R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv")

P8_PG_GATE_PATH = Path("source-intake/mts_residuals/P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv")
P8_PG_STATUS_PATH = Path("source-intake/mts_residuals/P8_PG_residual_input_STATUS.csv")
R11_SKELETON_PATH = Path("source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv")
R11_P8_TEMPLATE_PATH = Path("source-intake/mts_residuals/R11_P8_source_normalization_rows_TEMPLATE.csv")
MU_EXTRA_DECOMP_PATH = Path("runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_decomposition.csv")


SOURCE_REGISTER = [
    {
        "path": "434-measured-GM-mu-extra-zero-route.md",
        "role": "mu_obs = G_eff M_eff + mu_extra decomposition and mu_extra zero route",
    },
    {
        "path": "460-source-normalized-Newton-branch-theorem-stack.md",
        "role": "source-normalized Newton theorem stack and SN closure dependencies",
    },
    {
        "path": "461-PG-residual-input-derive-or-fill-gate.md",
        "role": "P8 derivative/source-normalization residual rows",
    },
    {
        "path": "462-charge-current-equality-direct-derivation-attempt.md",
        "role": "charge-current residual decomposition feeding measured-source closure",
    },
    {
        "path": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "EH-only failure and R11 vector branch decision",
    },
    {
        "path": "464-R11-executable-vector-minimum-fill-skeleton.md",
        "role": "source_normalization_operator chosen as highest-priority R11 family",
    },
    {
        "path": str(P8_PG_GATE_PATH),
        "role": "machine-readable P8 derive/fill rows",
    },
    {
        "path": str(P8_PG_STATUS_PATH),
        "role": "machine-readable P8 no-claim status rows",
    },
    {
        "path": str(R11_SKELETON_PATH),
        "role": "minimum executable R11 skeleton with source_normalization_operator row",
    },
    {
        "path": str(R11_P8_TEMPLATE_PATH),
        "role": "source-normalization operator template rows",
    },
    {
        "path": str(MU_EXTRA_DECOMP_PATH),
        "role": "mu_extra channel decomposition from checkpoint 434",
    },
]


DERIVATIVE_COLUMNS = [
    "channel_id",
    "derivative_channel",
    "exact_identity",
    "zero_condition",
    "mapped_P8_component",
    "mapped_symbol",
    "affected_rows",
    "current_evidence",
    "evidence_required",
    "minimum_fill_artifact",
    "cancellation_policy",
    "current_decision",
    "valid_for_Newton_claim",
    "valid_for_local_GR_claim",
    "notes",
]


DERIVATIVE_ROWS = [
    {
        "channel_id": "CGM0_master_identity",
        "derivative_channel": "any channel X in {t,r,A,lambda,frame,domain}",
        "exact_identity": "epsilon_mu := mu_extra/(G_eff M_eff); mu_obs = G_eff M_eff(1+epsilon_mu); D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
        "zero_condition": "D_X ln G_eff = 0, D_X ln M_eff = 0, and D_X epsilon_mu = 0, or their cancellation is a parent-derived identity",
        "mapped_P8_component": "all_P8_source_normalization_rows",
        "mapped_symbol": "D_X_ln_mu_obs",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_evidence": "exact algebraic identity derived from the existing mu_obs decomposition",
        "evidence_required": "for a pass, each derivative channel must be theorem-zero or numerically filled below its lock",
        "minimum_fill_artifact": "this gate plus one channel-specific residual/theorem artifact per active derivative channel",
        "cancellation_policy": "not allowed as a tuning; only a Ward/superselection/source identity may cancel terms for claim credit",
        "current_decision": "derived_identity_only_no_zero_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "this is the useful law; it converts vague measured-GM language into a row-by-row derivative scorecard",
    },
    {
        "channel_id": "CGM1_time_drift",
        "derivative_channel": "D_t",
        "exact_identity": "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_mu)/dt",
        "zero_condition": "dln_Geff_dt = 0; dln_Meff_dt = 0; partial_t epsilon_mu = 0, or parent-owned exact cancellation",
        "mapped_P8_component": "P8_Geff_time_drift;P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra",
        "mapped_symbol": "dln_Geff_dt;dln_Meff_dt;partial_t_epsilon_mu",
        "affected_rows": "R4;R9;R11",
        "current_evidence": "461 retains dln_Geff_dt and dln_Meff_dt unfilled; 462 leaves Delta_flux/Delta_G/Delta_extra active",
        "evidence_required": "parent superselection plus calibrated Pi_M flux conservation, or numeric local drift residual",
        "minimum_fill_artifact": "P8_time_drift_residual_or_zero.csv with units yr^-1 and separate G_eff/M_eff/mu_extra terms",
        "cancellation_policy": "time cancellation must be an identity, not a fitted epoch-by-epoch balance",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "this is the local Gdot lock; cosmology memory activity cannot be imported as local drift silence",
    },
    {
        "channel_id": "CGM2_radial_hair",
        "derivative_channel": "D_r",
        "exact_identity": "partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu)",
        "zero_condition": "no radial G_eff profile, no radial M_eff leakage, and no radial mu_extra outside compact support",
        "mapped_P8_component": "P8_radial_source_hair;P8_boundary_bulk_domain_mu_extra;P8_range_dependence",
        "mapped_symbol": "partial_r_ln_mu_obs;partial_r_epsilon_mu;alpha(lambda)",
        "affected_rows": "R4;R10;R11",
        "current_evidence": "461 retains partial_r_ln_mu_obs unfilled; 434 identifies radial mu_extra as a failure channel",
        "evidence_required": "Gauss/no-hair theorem or radial profile envelope relative to measured GM",
        "minimum_fill_artifact": "P8_radial_mu_profile_or_zero.csv with radius units and bound source",
        "cancellation_policy": "radial cancellation must hold for every exterior radius, not only at an orbital calibration point",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "if this survives, Newton becomes range/radius-dependent rather than clean inverse-square source normalization",
    },
    {
        "channel_id": "CGM3_species_source_charge",
        "derivative_channel": "D_A or Delta_AB across source/test species",
        "exact_identity": "Delta_AB ln mu_obs = Delta_AB ln G_eff + Delta_AB ln M_eff + Delta_AB ln(1+epsilon_mu)",
        "zero_condition": "source action is selector-blind and mu_obs is composition/species independent",
        "mapped_P8_component": "P8_species_source_charge;P8_frame_calibration_split",
        "mapped_symbol": "eta_source_AB;partial_A_ln_mu_obs",
        "affected_rows": "R1;R11",
        "current_evidence": "461 separates source-charge WEP from direct coframe WEP and retains eta_source_AB unfilled",
        "evidence_required": "no-species source-charge theorem or eta_source_AB residual below the source lock",
        "minimum_fill_artifact": "P8_species_source_charge_residual_or_zero.csv with material/source assumptions",
        "cancellation_policy": "species cancellation must be universal over allowed sources, not tuned per material",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "direct WEP geometry is helpful but does not alone prove source-current universality",
    },
    {
        "channel_id": "CGM4_range_dependence",
        "derivative_channel": "D_lambda or finite-range branch scan",
        "exact_identity": "D_lambda ln mu_obs = D_lambda ln G_eff + D_lambda ln M_eff + D_lambda ln(1+epsilon_mu); a nonzero finite-range term maps to alpha(lambda)",
        "zero_condition": "alpha(lambda)=0 by theorem, or an executable alpha(lambda) curve stays below bounds for every relevant lambda",
        "mapped_P8_component": "P8_range_dependence;R11_EH_operator_ledger",
        "mapped_symbol": "alpha(lambda);D_lambda_ln_mu_obs",
        "affected_rows": "R10;R11",
        "current_evidence": "461 and 464 both mark the R10 alpha(lambda) link required but missing",
        "evidence_required": "no-range theorem or R10 alpha(lambda) curve with predicted and bound columns",
        "minimum_fill_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv or theorem-zero source path",
        "cancellation_policy": "range cancellation must be functional in lambda, not a single-scale calibration",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "symbolic fifth-force silence is not enough; this row needs a curve or a proof",
    },
    {
        "channel_id": "CGM5_frame_domain_split",
        "derivative_channel": "Delta_frame or D_domain",
        "exact_identity": "Delta_frame ln mu_obs = Delta_frame ln G_eff + Delta_frame ln M_eff + Delta_frame ln(1+epsilon_mu)",
        "zero_condition": "one observed coframe/source frame/domain readout is parent-selected for source variation and matter motion",
        "mapped_P8_component": "P8_frame_calibration_split",
        "mapped_symbol": "delta_frame_source",
        "affected_rows": "R0;R2;R11",
        "current_evidence": "461 reports only partial conditional same-frame evidence; source variation remains not parent-derived",
        "evidence_required": "parent frame theorem or frame/source calibration residual below WEP and clock locks",
        "minimum_fill_artifact": "P8_frame_source_split_residual_or_zero.csv with same-frame assumptions",
        "cancellation_policy": "frame cancellation must be a single parent pullback, not post-hoc coordinate relabeling",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "this keeps the source-side frame issue attached to the variational source, not just the geodesic readout",
    },
    {
        "channel_id": "CGM6_mu_extra_amplitude",
        "derivative_channel": "epsilon_mu amplitude and all D_X epsilon_mu",
        "exact_identity": "epsilon_mu = mu_extra/(G_eff M_eff); D_X ln(1+epsilon_mu) = (D_X epsilon_mu)/(1+epsilon_mu)",
        "zero_condition": "epsilon_mu = 0, or epsilon_mu is a universal constant calibration and every derivative D_X epsilon_mu vanishes",
        "mapped_P8_component": "P8_boundary_bulk_domain_mu_extra;R11_EH_operator_ledger",
        "mapped_symbol": "mu_extra_boundary_bulk_domain/(G_eff M_eff);D_X_epsilon_mu",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "current_evidence": "434 decomposes mu_extra channels; 461 retains the central mu_extra row unfilled; 464 leaves source_normalization_operator unfilled",
        "evidence_required": "mu_extra=0 theorem or coefficient/residual map for every boundary, bulk, domain, memory, and non-EH channel",
        "minimum_fill_artifact": "P8_mu_extra_over_Geff_Meff_vector.csv with channel coefficients and derivative tags",
        "cancellation_policy": "constant universal calibration may be absorbed; radial/time/species/range/frame variation may not",
        "current_decision": "retained_unfilled_no_claim",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "notes": "this is the main hair vector: even if its amplitude is tiny, it must be sourced or bounded",
    },
    {
        "channel_id": "CGM7_second_order_beta_residue",
        "derivative_channel": "second-order source-normalized weak field",
        "exact_identity": "after first-order mu_obs is fixed, delta_beta_source is the remaining U^2 source-normalization residue",
        "zero_condition": "delta_beta_source=0 and gamma-1=0 after measured-GM normalization",
        "mapped_P8_component": "P8_nonlinear_beta_source_residue;R11_EH_operator_ledger",
        "mapped_symbol": "delta_beta_source;beta_minus_1;gamma_minus_1",
        "affected_rows": "R3;R4;R11",
        "current_evidence": "461 marks beta residue not required for first-order only but blocking for local-GR promotion",
        "evidence_required": "second-order weak-field theorem-zero or numeric PPN residual vector after constant-GM rows are owned",
        "minimum_fill_artifact": "P8_second_order_source_normalized_PPN_vector.csv",
        "cancellation_policy": "beta cancellation cannot be inferred from first-order Poisson/Gauss",
        "current_decision": "deferred_until_first_order_source_rows_owned",
        "valid_for_Newton_claim": "not_required_for_first_order_only",
        "valid_for_local_GR_claim": "false",
        "notes": "kept in the gate so nobody accidentally upgrades Newton to GR on first-order evidence",
    },
]


FILL_QUEUE_COLUMNS = [
    "priority",
    "target_row",
    "symbol",
    "minimum_acceptance",
    "artifact_required",
    "blocks",
    "claim_if_missing",
    "next_action",
]


FILL_QUEUE_ROWS = [
    {
        "priority": "1",
        "target_row": "CGM6_mu_extra_amplitude",
        "symbol": "mu_extra_boundary_bulk_domain/(G_eff M_eff)",
        "minimum_acceptance": "mu_extra=0 theorem or explicit coefficient vector with units/normalization/source paths",
        "artifact_required": "P8_mu_extra_over_Geff_Meff_vector.csv",
        "blocks": "constant_GM;Newton;R11_source_normalization_operator",
        "claim_if_missing": "no measured-GM absorption claim",
        "next_action": "try parent no-hair/Ward owner zero; otherwise fill coefficients",
    },
    {
        "priority": "2",
        "target_row": "CGM1_time_drift",
        "symbol": "dln_Geff_dt;dln_Meff_dt;partial_t_epsilon_mu",
        "minimum_acceptance": "separate drift terms in yr^-1 or parent superselection/flux-conservation theorem-zero",
        "artifact_required": "P8_time_drift_residual_or_zero.csv",
        "blocks": "Gdot_over_G;local_GR",
        "claim_if_missing": "no local Gdot silence",
        "next_action": "derive global-coupling superselection and Pi_M conservation or load drift bound",
    },
    {
        "priority": "3",
        "target_row": "CGM2_radial_hair",
        "symbol": "partial_r_ln_mu_obs",
        "minimum_acceptance": "radial no-hair theorem or profile envelope relative to measured GM",
        "artifact_required": "P8_radial_mu_profile_or_zero.csv",
        "blocks": "inverse_square_Newton;R10",
        "claim_if_missing": "no radius-independent GM claim",
        "next_action": "derive Gauss/no-hair exterior or fill radial profile",
    },
    {
        "priority": "4",
        "target_row": "CGM4_range_dependence",
        "symbol": "alpha(lambda)",
        "minimum_acceptance": "theorem-zero or executable alpha(lambda) curve",
        "artifact_required": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "blocks": "fifth_force;R10;R11",
        "claim_if_missing": "no finite-range silence claim",
        "next_action": "build source-normalization alpha(lambda) curve or no-range theorem",
    },
    {
        "priority": "5",
        "target_row": "CGM3_species_source_charge",
        "symbol": "eta_source_AB",
        "minimum_acceptance": "source-charge theorem-zero or residual below source lock",
        "artifact_required": "P8_species_source_charge_residual_or_zero.csv",
        "blocks": "R1_source_charge;WEP_full",
        "claim_if_missing": "direct WEP only; source WEP retained",
        "next_action": "prove selector-blind source action or fill eta_source_AB",
    },
    {
        "priority": "6",
        "target_row": "CGM5_frame_domain_split",
        "symbol": "delta_frame_source",
        "minimum_acceptance": "same parent pullback for source variation and matter readout or residual bound",
        "artifact_required": "P8_frame_source_split_residual_or_zero.csv",
        "blocks": "same_frame_Newton;clock_link",
        "claim_if_missing": "no same-frame source-normalization claim",
        "next_action": "attach frame theorem to source variation, not only matter motion",
    },
    {
        "priority": "7",
        "target_row": "CGM7_second_order_beta_residue",
        "symbol": "delta_beta_source",
        "minimum_acceptance": "second-order source-normalized PPN vector after first-order rows are closed",
        "artifact_required": "P8_second_order_source_normalized_PPN_vector.csv",
        "blocks": "local_GR;PPN_beta_gamma",
        "claim_if_missing": "Newton may remain first-order only; local GR cannot pass",
        "next_action": "defer until CGM1-CGM6 are theorem-zero or numerically scored",
    },
]


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


R11_VECTOR_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "source_normalization_operator",
        "coefficient_symbol": "epsilon_mu_vector",
        "coefficient_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_BOUND",
        "coefficient_units": "dimensionless",
        "normalization": "epsilon_mu=mu_extra/(G_eff M_eff)",
        "operator_form": "mu_obs = G_eff M_eff(1+epsilon_mu)",
        "weak_field_map": "CGM0_master_identity;CGM6_mu_extra_amplitude",
        "affected_rows": "R1;R4;R9;R10;R11",
        "induced_observable": "eta_source_AB;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_P8_MU_EXTRA_VECTOR_OR_ZERO_THEOREM",
        "derivation_status": "retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "same-frame weak-field branch; source-normalization decomposition from checkpoint 434",
        "valid_for_claim": "false",
        "notes": "exact epsilon definition supplied, but no zero/bound coefficient supplied",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "time_drift_source_memory",
        "coefficient_symbol": "dln_mu_obs_dt_vector",
        "coefficient_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_DRIFT",
        "coefficient_units": "yr^-1",
        "normalization": "d ln mu_obs/dt = dln_Geff_dt + dln_Meff_dt + dln(1+epsilon_mu)/dt",
        "operator_form": "local time drift of measured source strength",
        "weak_field_map": "CGM1_time_drift",
        "affected_rows": "R4;R9;R11",
        "induced_observable": "Gdot_over_G;beta_minus_1;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_P8_TIME_DRIFT_RESIDUAL_OR_ZERO_THEOREM",
        "derivation_status": "retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "local compact exterior, no imported cosmological drift cancellation",
        "valid_for_claim": "false",
        "notes": "must report G_eff, M_eff, and epsilon_mu contributions separately",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "radial_range_source_hair",
        "coefficient_symbol": "partial_r_ln_mu_obs_and_alpha_lambda",
        "coefficient_value": "MISSING_DERIVED_ZERO_PROFILE_OR_ALPHA_CURVE",
        "coefficient_units": "1/length_or_range_dependent",
        "normalization": "partial_r ln mu_obs and alpha(lambda) relative to measured GM",
        "operator_form": "radial/range-dependent measured-source strength",
        "weak_field_map": "CGM2_radial_hair;CGM4_range_dependence",
        "affected_rows": "R4;R10;R11",
        "induced_observable": "alpha(lambda);perihelion;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_RADIAL_PROFILE_OR_R10_ALPHA_LAMBDA_CURVE",
        "derivation_status": "retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "radius and range silence must be functional, not single-calibration",
        "valid_for_claim": "false",
        "notes": "this row prevents hiding finite-range hair inside measured GM",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "species_source_charge",
        "coefficient_symbol": "eta_source_AB_or_partial_A_ln_mu_obs",
        "coefficient_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_SOURCE_CHARGE",
        "coefficient_units": "dimensionless",
        "normalization": "eta_source_AB from source-side mu_obs composition dependence",
        "operator_form": "species/material/source marker coupling in measured source strength",
        "weak_field_map": "CGM3_species_source_charge",
        "affected_rows": "R1;R11",
        "induced_observable": "eta_source_AB;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_SOURCE_CHARGE_RESIDUAL_OR_ZERO_THEOREM",
        "derivation_status": "retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "source action is selector-blind across allowed materials",
        "valid_for_claim": "false",
        "notes": "direct WEP geometry does not auto-fill this source-side row",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "frame_calibration_source_split",
        "coefficient_symbol": "delta_frame_source",
        "coefficient_value": "MISSING_DERIVED_ZERO_OR_NUMERIC_FRAME_SPLIT",
        "coefficient_units": "dimensionless",
        "normalization": "Delta_frame ln mu_obs in observed matter/source frame",
        "operator_form": "frame/source calibration mismatch in measured-source strength",
        "weak_field_map": "CGM5_frame_domain_split",
        "affected_rows": "R0;R2;R11",
        "induced_observable": "eta_WEP_direct_geometry;clock_redshift;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_FRAME_SOURCE_SPLIT_RESIDUAL_OR_ZERO_THEOREM",
        "derivation_status": "retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "one parent pullback for source variation and matter readout",
        "valid_for_claim": "false",
        "notes": "source variation must live in the same observed frame as the orbital readout",
    },
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "constant_GM_derivative_hair_gate",
        "vector_id": "R11_source_normalization_derivative_hair_vector",
        "operator_family": "second_order_source_normalization",
        "coefficient_symbol": "delta_beta_source",
        "coefficient_value": "MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR",
        "coefficient_units": "dimensionless",
        "normalization": "source-normalized U^2 coefficient after first-order measured GM is fixed",
        "operator_form": "second-order source-normalization residue",
        "weak_field_map": "CGM7_second_order_beta_residue",
        "affected_rows": "R3;R4;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;operator_ledger",
        "predicted_residual_or_bound_source": "MISSING_SECOND_ORDER_PPN_VECTOR_OR_ZERO_THEOREM",
        "derivation_status": "deferred_retained_unfilled",
        "formula_reference": "465-constant-GM-derivative-hair-fill-gate.md",
        "source_file": str(DERIVATIVE_GATE_PATH),
        "assumptions": "first-order CGM rows are already theorem-zero or numerically scored",
        "valid_for_claim": "false",
        "notes": "blocks local-GR promotion even if first-order Newton later passes",
    },
]


GATE_RESULT_COLUMNS = ["gate", "status", "evidence", "claim_credit"]


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_REGISTER:
        rows.append(
            {
                "path": source["path"],
                "exists": str((ROOT / source["path"]).exists()),
                "role": source["role"],
            }
        )
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def count_token(rows: list[dict[str, Any]], token: str) -> int:
    return sum(str(value).count(token) for row in rows for value in row.values())


def gate_results(
    source_paths_missing: int,
    pg_rows: int,
    r11_skeleton_rows: int,
    r11_source_norm_rows: int,
    p8_template_rows: int,
    missing_markers: int,
    generic_fill_tokens: int,
) -> list[dict[str, str]]:
    return [
        {
            "gate": "CGMV0_source_paths",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
            "claim_credit": "audit_only",
        },
        {
            "gate": "CGMV1_P8_rows_loaded",
            "status": "pass" if pg_rows == 9 else "fail",
            "evidence": f"P8 PG rows loaded = {pg_rows}",
            "claim_credit": "schema_only",
        },
        {
            "gate": "CGMV2_R11_source_norm_loaded",
            "status": "pass" if r11_skeleton_rows >= 1 and r11_source_norm_rows == 1 else "fail",
            "evidence": f"R11 skeleton rows = {r11_skeleton_rows}; source_normalization_operator rows = {r11_source_norm_rows}",
            "claim_credit": "schema_only",
        },
        {
            "gate": "CGMV3_derivative_identity",
            "status": "pass",
            "evidence": "mu_obs = G_eff M_eff(1+epsilon_mu) implies exact D_X ln mu_obs identity",
            "claim_credit": "identity_only",
        },
        {
            "gate": "CGMV4_zero_conditions_parent_derived",
            "status": "fail",
            "evidence": "all derivative channels retain missing theorem-zero or numeric residual artifacts",
            "claim_credit": "none",
        },
        {
            "gate": "CGMV5_R11_vector_executable",
            "status": "fail",
            "evidence": f"missing markers in derivative R11 vector = {missing_markers}; generic output placeholders = {generic_fill_tokens}",
            "claim_credit": "none",
        },
        {
            "gate": "CGMV6_constant_GM_promoted",
            "status": "fail",
            "evidence": "constant measured GM requires CGM1-CGM6 theorem-zero or numeric scoring",
            "claim_credit": "none",
        },
    ]


def theorem_status_rows() -> list[dict[str, str]]:
    return [
        {
            "claim": "exact constant-GM derivative law derived",
            "status": "pass_identity",
            "evidence": "D_X ln mu_obs identity follows algebraically from mu_obs = G_eff M_eff + mu_extra",
        },
        {
            "claim": "source-normalization derivative hair is zero",
            "status": "fail",
            "evidence": "no parent-zero theorem or numeric residual vector supplied for CGM1-CGM6",
        },
        {
            "claim": "constant measured GM is parent-derived",
            "status": "fail",
            "evidence": "G_eff, M_eff, epsilon_mu, source, range, radial, and frame derivatives remain retained",
        },
        {
            "claim": "Newtonian reduction promoted",
            "status": "fail",
            "evidence": "constant measured GM and R11 source-normalization vector are not executable",
        },
        {
            "claim": "local GR promoted",
            "status": "fail",
            "evidence": "second-order beta/gamma source-normalized vector remains deferred and unfilled",
        },
    ]


def render_doc(
    timestamp: str,
    run_dir: Path,
    source_rows: list[dict[str, str]],
    result_rows: list[dict[str, str]],
    pg_rows: int,
    p8_template_rows: int,
    r11_source_norm_rows: int,
    missing_markers: int,
    generic_fill_tokens: int,
) -> str:
    theorem_columns = ["claim", "status", "evidence"]
    return f"""# 465 - Constant-GM Derivative-Hair Fill Gate

Private source-normalization checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 464 identified `source_normalization_operator` as the highest-priority R11 row because it decides whether measured Newtonian `GM` is a constant source charge or a place where hidden boundary/bulk/domain/range/source hair can hide.

This checkpoint asks the sharper question:

Can `mu_obs` be constant in time, radius, species, range, frame, and domain from the parent theory, or must every surviving derivative become an explicit residual row?

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/constant_GM_derivative_hair_fill_gate.py` |
| Run directory | `{run_dir}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Derivative gate CSV | `{DERIVATIVE_GATE_PATH}` |
| Fill queue CSV | `{FILL_QUEUE_PATH}` |
| R11 derivative vector CSV | `{R11_VECTOR_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["path", "exists", "role"])}

## 4. Exact Law

Start from the measured-source decomposition already isolated in the P8 route:

```text
mu_obs = G_eff M_eff + mu_extra.
```

Define the dimensionless source-normalization hair

```text
epsilon_mu := mu_extra / (G_eff M_eff).
```

Then

```text
mu_obs = G_eff M_eff (1 + epsilon_mu).
```

For any local derivative/readout channel

```text
X in {{t, r, species A, range lambda, frame, domain}},
```

the exact log-derivative law is

```text
D_X ln mu_obs
  = D_X ln G_eff
  + D_X ln M_eff
  + D_X ln(1 + epsilon_mu).
```

So constant measured `GM` is not a vibe; it is the finite checklist

```text
D_X ln mu_obs = 0 for every X.
```

A row can pass only if the terms are theorem-zero, numerically bounded below the relevant lock, or cancelled by a parent-derived identity. Tuned cancellation does not count.

## 5. Derivative-Hair Gate

The derivative-hair gate has been written to `{DERIVATIVE_GATE_PATH}`.

{md_table(DERIVATIVE_ROWS, DERIVATIVE_COLUMNS)}

## 6. Minimum Fill Queue

The minimum fill queue has been written to `{FILL_QUEUE_PATH}`.

{md_table(FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)}

## 7. R11 Source-Normalization Vector

The derivative-specialized R11 vector has been written to `{R11_VECTOR_PATH}`.

{md_table(R11_VECTOR_ROWS, R11_VECTOR_COLUMNS)}

## 8. Gate Results

{md_table(result_rows, GATE_RESULT_COLUMNS)}

## 9. Theorem Status

{md_table(theorem_status_rows(), theorem_columns)}

## 10. Decision

The exact derivative law lands. That is real progress: measured `GM` now has a clean algebraic spine instead of a loose calibration phrase.

But the zero theorem does not land yet. The law exposes the debt:

```text
constant GM requires
D_X ln G_eff = 0,
D_X ln M_eff = 0,
D_X epsilon_mu = 0
for every local channel X,
or a parent identity that cancels them exactly.
```

Current corpus state: P8 rows loaded = `{pg_rows}`, P8 source-normalization template rows = `{p8_template_rows}`, R11 source-normalization skeleton rows = `{r11_source_norm_rows}`, derivative-vector `MISSING_` markers = `{missing_markers}`, generic output `fill_` placeholders = `{generic_fill_tokens}`.

So the round is scored like this: we landed the jab cleanly, but we do not raise the belt. Exact identity: yes. Constant-GM theorem: no. Newton/local-GR promotion: no.

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | either prove `epsilon_mu`, `G_eff`, and `M_eff` are derivative-silent, or start loading actual local residual/bound rows |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | range dependence cannot pass with symbolic `alpha(lambda)` language |
| 3 | `P8_second_order_source_normalized_PPN_vector.csv` | local GR needs beta/gamma after first-order source normalization |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-constant-GM-derivative-hair-fill-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    source_paths_missing = sum(1 for row in source_rows if row["exists"] != "True")
    pg_gate_rows = read_csv_rows(P8_PG_GATE_PATH)
    p8_template_rows = read_csv_rows(R11_P8_TEMPLATE_PATH)
    r11_skeleton_rows = read_csv_rows(R11_SKELETON_PATH)
    r11_source_norm_rows = [row for row in r11_skeleton_rows if row.get("operator_family") == "source_normalization_operator"]

    missing_markers = count_token(R11_VECTOR_ROWS, "MISSING_")
    generic_fill_tokens = count_token(R11_VECTOR_ROWS, "fill_") + count_token(DERIVATIVE_ROWS, "fill_")

    result_rows = gate_results(
        source_paths_missing=source_paths_missing,
        pg_rows=len(pg_gate_rows),
        r11_skeleton_rows=len(r11_skeleton_rows),
        r11_source_norm_rows=len(r11_source_norm_rows),
        p8_template_rows=len(p8_template_rows),
        missing_markers=missing_markers,
        generic_fill_tokens=generic_fill_tokens,
    )

    write_csv(ROOT / DERIVATIVE_GATE_PATH, DERIVATIVE_ROWS, DERIVATIVE_COLUMNS)
    write_csv(ROOT / FILL_QUEUE_PATH, FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)
    write_csv(ROOT / R11_VECTOR_PATH, R11_VECTOR_ROWS, R11_VECTOR_COLUMNS)

    write_csv(results_dir / "P8_constant_GM_derivative_hair_gate.csv", DERIVATIVE_ROWS, DERIVATIVE_COLUMNS)
    write_csv(results_dir / "P8_constant_GM_derivative_hair_fill_queue.csv", FILL_QUEUE_ROWS, FILL_QUEUE_COLUMNS)
    write_csv(results_dir / "R11_source_normalization_derivative_hair_vector.csv", R11_VECTOR_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "source_register.csv", source_rows, ["path", "exists", "role"])
    write_csv(results_dir / "gate_results.csv", result_rows, GATE_RESULT_COLUMNS)
    write_csv(results_dir / "theorem_status.csv", theorem_status_rows(), ["claim", "status", "evidence"])

    doc = render_doc(
        timestamp=timestamp,
        run_dir=Path("runs") / f"{timestamp}-constant-GM-derivative-hair-fill-gate",
        source_rows=source_rows,
        result_rows=result_rows,
        pg_rows=len(pg_gate_rows),
        p8_template_rows=len(p8_template_rows),
        r11_source_norm_rows=len(r11_source_norm_rows),
        missing_markers=missing_markers,
        generic_fill_tokens=generic_fill_tokens,
    )
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "source_paths_missing": source_paths_missing,
        "pg_derivative_rows_loaded": len(pg_gate_rows),
        "p8_source_normalization_template_rows_loaded": len(p8_template_rows),
        "r11_skeleton_rows_loaded": len(r11_skeleton_rows),
        "r11_source_normalization_rows_loaded": len(r11_source_norm_rows),
        "derivative_gate_rows": len(DERIVATIVE_ROWS),
        "fill_queue_rows": len(FILL_QUEUE_ROWS),
        "r11_derivative_vector_rows": len(R11_VECTOR_ROWS),
        "exact_log_derivative_identity_derived": True,
        "all_zero_conditions_parent_derived": False,
        "numeric_residuals_loaded": False,
        "missing_markers_in_R11_derivative_vector": missing_markers,
        "generic_fill_placeholder_tokens_in_outputs": generic_fill_tokens,
        "source_normalization_operator_filled": False,
        "constant_GM_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", status)
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default="20260602-211500")
    arguments = parser.parse_args()
    status = write_run(arguments.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
