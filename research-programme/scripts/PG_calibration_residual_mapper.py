from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "PG-calibration-residual-mapper"
CHECKPOINT_DOC = "459-PG-calibration-residual-mapper.md"
STATUS = "PG_calibration_residual_mapper_written_failed_PG_rows_mapped_to_P8_R11_inputs_no_numeric_residuals_loaded_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "PG_residual_mapper_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "460-source-normalized-Newton-branch-theorem-stack.md"
MAP_PATH = Path("source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv")
INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_PG_calibration_residual_INPUT_TEMPLATE.csv")


MAP_COLUMNS = [
    "pg_id",
    "failed_premise",
    "activated_residual_component",
    "residual_symbol",
    "affected_rows",
    "activation_rule",
    "required_input",
    "current_status",
    "valid_for_claim",
    "source_gate",
    "notes",
]

INPUT_COLUMNS = [
    "model_id",
    "branch_id",
    "pg_id",
    "component_id",
    "symbol",
    "units",
    "normalization",
    "affected_rows",
    "observable_link",
    "bound_or_target",
    "required_input",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


SOURCE_DOCS = [
    {
        "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "immediate PG0-PG10 calibration gate to be mapped",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "machine-readable PG calibration contract rows",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "canonical P8 measured-GM/source-normalization residual rows",
    },
    {
        "path": "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "canonical R0-R11 local residual prediction template",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "R11 non-EH operator-vector template required if EH-only is not derived",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 symbolic no-pass coefficient-vector contract",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH/source-normalization retained ledger and row transition policy",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration blockers",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal G_eff/kappa residual map",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "machine-readable R0-R11 residual components and locks",
    },
    {
        "path": "runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv",
        "role": "machine-readable mu_obs decomposition into source-normalization channels",
    },
    {
        "path": "runs/20260602-181500-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate/results/Poisson_Gauss_calibration_contract.csv",
        "role": "run artifact for PG0-PG10 rows",
    },
]


PG_TO_RESIDUAL_MAP = [
    {
        "pg_id": "PG0_Hamiltonian_charge_input",
        "failed_premise": "B_xi is not parent-derived as a well-defined observed-time charge",
        "activated_residual_component": "R11_EH_operator_ledger;P8_Meff_conservation;P8_frame_calibration_split",
        "residual_symbol": "c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source",
        "affected_rows": "R2;R4;R5;R6;R8;R9;R11",
        "activation_rule": "if HC0-HC3 are not derived, the candidate Hamiltonian charge is reference/operator/frame conditional",
        "required_input": "parent charge proof or retained charge/reference/operator residual vector",
        "current_status": "retained_missing_parent_charge",
        "valid_for_claim": "false",
        "source_gate": "458-PG0",
        "notes": "no Poisson/Gauss calibration can start without a real observed-time charge",
    },
    {
        "pg_id": "PG1_charge_equals_projected_Hilbert_source",
        "failed_premise": "B_xi/G_eff is not shown equal to M_eff[Pi_M J_H]",
        "activated_residual_component": "P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra;R11_EH_operator_ledger",
        "residual_symbol": "dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector",
        "affected_rows": "R1;R4;R9;R10;R11",
        "activation_rule": "if charge-current equality is missing, measured source mass is a retained calibration split",
        "required_input": "source-current Ward/Pi_M proof or numeric/source-normalization residual",
        "current_status": "retained_charge_current_split",
        "valid_for_claim": "false",
        "source_gate": "458-PG1",
        "notes": "conserved geometric charge is not automatically the Newton source",
    },
    {
        "pg_id": "PG2_same_frame_weak_field_potential",
        "failed_premise": "matter orbits are not proved to read the same Phi sourced by the metric equation",
        "activated_residual_component": "P8_frame_calibration_split;R0_identity_coframe_direct;R2_clock_redshift;R11_EH_operator_ledger",
        "residual_symbol": "delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector",
        "affected_rows": "R0;R1;R2;R11",
        "activation_rule": "if the potential/frame map is missing, calibration can hide a frame split",
        "required_input": "same-frame coframe theorem or frame residual below WEP/clock/operator locks",
        "current_status": "retained_frame_split",
        "valid_for_claim": "false",
        "source_gate": "458-PG2",
        "notes": "clock or direct-WEP success alone does not clear the source-frame split",
    },
    {
        "pg_id": "PG3_EH_to_Poisson_coefficient",
        "failed_premise": "EH-to-Poisson coefficient is conditional on EH-only and zero source_residuals",
        "activated_residual_component": "R11_EH_operator_ledger;P8_boundary_bulk_domain_mu_extra;P8_range_dependence",
        "residual_symbol": "c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda)",
        "affected_rows": "R3;R4;R8;R10;R11",
        "activation_rule": "if EH-only/source purity is missing, the Poisson coefficient is an operator/source residual",
        "required_input": "EH-only theorem-zero or complete R11 vector plus source residual map",
        "current_status": "retained_operator_source_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG3",
        "notes": "the algebra passes only inside the same-frame EH/source premise stack",
    },
    {
        "pg_id": "PG4_Gauss_surface_integral",
        "failed_premise": "surface integral is not proved equal to enclosed M_eff without residual volume/boundary terms",
        "activated_residual_component": "P8_radial_source_hair;P8_boundary_bulk_domain_mu_extra;P8_Meff_conservation",
        "residual_symbol": "partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "activation_rule": "if Gauss integral equality is missing, radial/boundary/source hair remains active",
        "required_input": "closed Pi_M flux plus zero boundary/source residual theorem or numeric residual envelope",
        "current_status": "retained_Gauss_surface_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG4",
        "notes": "this is the main measured-GM monopole calibration row",
    },
    {
        "pg_id": "PG5_orbital_inverse_square_readout",
        "failed_premise": "test bodies are not proved to read a pure inverse-square Gauss monopole",
        "activated_residual_component": "P8_range_dependence;P8_radial_source_hair;P8_species_source_charge;P8_frame_calibration_split",
        "residual_symbol": "alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source",
        "affected_rows": "R1;R2;R4;R10;R11",
        "activation_rule": "if orbital readout has extra force/source/frame terms, GM is empirical not derived",
        "required_input": "slow-particle geodesic proof plus alpha(lambda)=0/source/frame theorem or residual curve",
        "current_status": "retained_orbital_readout_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG5",
        "notes": "finite-range/radial effects cannot be absorbed into one GM",
    },
    {
        "pg_id": "PG6_zero_mu_extra_and_source_residuals",
        "failed_premise": "mu_extra and S_res are not theorem-zero",
        "activated_residual_component": "P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair;P8_range_dependence;R11_EH_operator_ledger",
        "residual_symbol": "mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "activation_rule": "if source_residuals survive, Gauss mass includes their volume/boundary contribution",
        "required_input": "Ward/no-hair/topological zero proof or executable coefficient map for all mu_extra channels",
        "current_status": "retained_mu_extra_source_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG6",
        "notes": "source_residuals are measured physics, not notation",
    },
    {
        "pg_id": "PG7_constant_universal_Geff",
        "failed_premise": "G_eff/kappa_eff is not parent-derived constant/universal/source-blind/range-blind",
        "activated_residual_component": "P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;R11_EH_operator_ledger",
        "residual_symbol": "dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector",
        "affected_rows": "R1;R4;R9;R10;R11",
        "activation_rule": "if G_eff derivatives or source labels are unproved, Gdot/source/fifth-force rows remain active",
        "required_input": "CU1-CU7 theorem-zero proof or derivative/source/range residual values",
        "current_status": "retained_Geff_derivative_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG7",
        "notes": "constant offset is calibration only after all derivatives vanish",
    },
    {
        "pg_id": "PG8_no_derivative_hair",
        "failed_premise": "mu_obs derivative silence is not parent-derived",
        "activated_residual_component": "P8_Geff_time_drift;P8_Meff_conservation;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair;P8_frame_calibration_split",
        "residual_symbol": "dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source",
        "affected_rows": "R0;R1;R2;R4;R8;R9;R10;R11",
        "activation_rule": "if any time/radial/species/range/frame/domain derivative is unproved, the matching row stays retained",
        "required_input": "row-specific theorem-zero source or numeric derivative/curve/profile",
        "current_status": "retained_derivative_hair_vector",
        "valid_for_claim": "false",
        "source_gate": "458-PG8",
        "notes": "this is the anti-calibration-cheat row",
    },
    {
        "pg_id": "PG9_second_order_source_stability",
        "failed_premise": "first-order measured-GM calibration is not proved stable at beta/gamma/PPN order",
        "activated_residual_component": "P8_nonlinear_beta_source_residue;R3_gamma;R11_EH_operator_ledger",
        "residual_symbol": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
        "affected_rows": "R3;R4;R11",
        "activation_rule": "if second-order weak-field calculation is missing, Poisson cannot be promoted to local GR",
        "required_input": "second-order PPN source/operator derivation or beta/gamma residual values",
        "current_status": "retained_second_order_source_residual",
        "valid_for_claim": "false",
        "source_gate": "458-PG9",
        "notes": "Poisson success is a first-order source gate only",
    },
    {
        "pg_id": "PG10_retained_residual_fallback",
        "failed_premise": "failed PG rows need executable residual data before any claim",
        "activated_residual_component": "all_P8_source_normalization_components;R11_EH_operator_ledger",
        "residual_symbol": "dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;mu_extra/(GM);delta_beta_source;c_nonEH_operator_vector",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "activation_rule": "if no theorem-zero proof exists, output templates and mark valid_for_claim=false",
        "required_input": "filled residual input template or derived-zero sources",
        "current_status": "template_policy_only",
        "valid_for_claim": "false",
        "source_gate": "458-PG10",
        "notes": "manual no-promotion discipline is replaced by machine-readable rows",
    },
]


RESIDUAL_INPUT_TEMPLATE = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG7;PG8",
        "component_id": "P8_Geff_time_drift",
        "symbol": "dln_Geff_dt",
        "units": "yr^-1",
        "normalization": "d ln G_eff / dt or d ln kappa_eff / dt",
        "affected_rows": "R9;R11",
        "observable_link": "Gdot_over_G",
        "bound_or_target": "9.6e-15 yr^-1 or derived zero",
        "required_input": "numeric drift, derived-zero proof, or explicit superselection source",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "d ln mu_obs/dt = d ln(G_eff M_eff)/dt",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "same observed frame; local branch; source-normalized measured GM",
        "valid_for_claim": "false",
        "notes": "cosmological memory success cannot override local Gdot lock",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG1;PG4;PG8",
        "component_id": "P8_Meff_conservation",
        "symbol": "dln_Meff_dt",
        "units": "yr^-1",
        "normalization": "d ln M_eff / dt after separating G_eff drift",
        "affected_rows": "R4;R9;R11",
        "observable_link": "beta_minus_1;Gdot_over_G",
        "bound_or_target": "beta/Gdot locks or derived conservation",
        "required_input": "mass-flux closure proof or mass drift residual",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_obs = G_eff M_eff + mu_extra",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "compact source; no unowned flux; no hidden boundary/memory exchange",
        "valid_for_claim": "false",
        "notes": "source mass conservation must be owned, not assumed",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG5;PG7;PG8",
        "component_id": "P8_species_source_charge",
        "symbol": "eta_source_AB",
        "units": "dimensionless",
        "normalization": "composition/source derivative of ln mu_obs",
        "affected_rows": "R1;R11",
        "observable_link": "eta_WEP_source_charge",
        "bound_or_target": "2.8e-15 or derived universal source charge",
        "required_input": "species/source-charge theorem or eta_source_AB residual",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_A mu_obs = 0",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "species/material markers do not alter active gravitational source",
        "valid_for_claim": "false",
        "notes": "direct WEP proxy is not the full source-normalization proof",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG3;PG5;PG6;PG7;PG8",
        "component_id": "P8_range_dependence",
        "symbol": "alpha(lambda)",
        "units": "range-dependent",
        "normalization": "Yukawa/non-Yukawa fifth-force curve or derivative of ln mu_obs with range scale",
        "affected_rows": "R10;R11",
        "observable_link": "delta_G_or_fifth_force_yukawa",
        "bound_or_target": "verified alpha(lambda) bound curve or derived zero",
        "required_input": "curve file with lambda/alpha_predicted/alpha_bound or no finite-range theorem",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_lambda mu_obs = 0",
        "source_file": "fill_curve_path_or_derivation",
        "assumptions": "same-frame source charge; screening/range assumptions explicit",
        "valid_for_claim": "false",
        "notes": "symbolic R10 cannot pass without executable curve or theorem-zero",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG4;PG5;PG6;PG8",
        "component_id": "P8_radial_source_hair",
        "symbol": "partial_r_ln_mu_obs",
        "units": "inverse_length_or_dimensionless_envelope",
        "normalization": "radial derivative or residual envelope relative to measured GM",
        "affected_rows": "R3;R4;R10;R11",
        "observable_link": "gamma_minus_1;beta_minus_1;alpha(lambda)",
        "bound_or_target": "zero radial hair or mapped PPN/fifth-force residuals",
        "required_input": "radial profile, no-hair proof, or coefficient map",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "partial_r mu_obs = 0",
        "source_file": "fill_profile_or_derivation_path",
        "assumptions": "compact exterior; boundary/domain hair accounted for",
        "valid_for_claim": "false",
        "notes": "radial dependence is physics, not calibration",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG1;PG3;PG4;PG6",
        "component_id": "P8_boundary_bulk_domain_mu_extra",
        "symbol": "mu_extra_boundary_bulk_domain",
        "units": "dimensionless_or_GM_units_after_normalization",
        "normalization": "mu_extra/(G_eff M_eff) or explicit GM units",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "observable_link": "gamma;beta;alpha3;xi;Gdot;operator_ledger",
        "bound_or_target": "zero owned exchange or coefficient residuals below row locks",
        "required_input": "exchange coefficients, Ward/no-hair proof, or boundary/domain residual map",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "mu_extra = 0",
        "source_file": "fill_exchange_derivation_or_run_path",
        "assumptions": "boundary, bulk, domain, projector, memory, and connection channels visible",
        "valid_for_claim": "false",
        "notes": "alpha3 lock is severe for unowned exchange",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG0;PG2;PG5;PG8",
        "component_id": "P8_frame_calibration_split",
        "symbol": "delta_frame_source",
        "units": "dimensionless",
        "normalization": "relative frame/source calibration residual",
        "affected_rows": "R0;R2;R11",
        "observable_link": "eta_WEP_direct_geometry;clock_redshift;operator_ledger",
        "bound_or_target": "one observed frame or explicit residual below row locks",
        "required_input": "parent frame theorem or frame split residual",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "same observed coframe for matter and metric source variation",
        "source_file": "fill_frame_derivation_or_run_path",
        "assumptions": "matter, clocks, rods, photons, and metric source use same observed frame",
        "valid_for_claim": "false",
        "notes": "calibration cannot hide a frame split",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG9",
        "component_id": "P8_nonlinear_beta_source_residue",
        "symbol": "delta_beta_source",
        "units": "dimensionless",
        "normalization": "beta_minus_1 contribution assigned to source normalization",
        "affected_rows": "R4;R11",
        "observable_link": "beta_minus_1",
        "bound_or_target": "7.8e-05 or derived second-order source closure",
        "required_input": "second-order weak-field source derivation or beta source residual",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "PPN beta after measured-GM normalization",
        "source_file": "fill_second_order_derivation_or_run_path",
        "assumptions": "same observed frame; measured-GM normalization held fixed at PPN order",
        "valid_for_claim": "false",
        "notes": "first-order Poisson success does not clear beta",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "PG_calibration_branch",
        "pg_id": "PG0;PG1;PG3;PG6;PG7;PG9",
        "component_id": "R11_EH_operator_ledger",
        "symbol": "c_nonEH_operator_vector",
        "units": "operator family",
        "normalization": "full R11 coefficient-vector normalization",
        "affected_rows": "R3;R4;R5;R6;R8;R10;R11",
        "observable_link": "operator_ledger;gamma;beta;preferred_frame;fifth_force",
        "bound_or_target": "EH-only theorem-zero or executable coefficient vector",
        "required_input": "R11 operator-vector file or EH-only parent theorem",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "R11_nonEH_operator_vector_TEMPLATE.csv",
        "source_file": "fill_operator_vector_or_EH_theorem_path",
        "assumptions": "local, same-frame, source-normalized exterior branch",
        "valid_for_claim": "false",
        "notes": "symbolic operator row cannot pass without coefficient/vector map",
    },
]


ROW_TRANSITIONS = [
    {
        "row_id": "R0_identity_coframe_direct",
        "activated_by": "PG2;PG8",
        "new_state": "retained_frame_control",
        "why": "same-frame potential/source map remains conditional",
        "claim_credit": "no",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "activated_by": "PG1;PG5;PG7;PG8",
        "new_state": "retained_source_charge",
        "why": "measured source strength may carry species/source dependence",
        "claim_credit": "no",
    },
    {
        "row_id": "R2_clock_redshift",
        "activated_by": "PG0;PG2;PG5;PG8",
        "new_state": "retained_same_frame_clock",
        "why": "orbits/clocks/source may not share one observed frame",
        "claim_credit": "no",
    },
    {
        "row_id": "R3_gamma",
        "activated_by": "PG3;PG4;PG6;PG9",
        "new_state": "retained_operator_slip",
        "why": "Poisson source purity does not prove spatial curvature/slip",
        "claim_credit": "no",
    },
    {
        "row_id": "R4_beta",
        "activated_by": "PG0;PG1;PG3;PG4;PG5;PG6;PG7;PG8;PG9",
        "new_state": "retained_source_normalization_beta",
        "why": "measured-GM and second-order source stability are not derived",
        "claim_credit": "no",
    },
    {
        "row_id": "R5_alpha1",
        "activated_by": "PG0",
        "new_state": "retained_preferred_frame_vector",
        "why": "observed-time charge generator can carry vector/preferred-frame ambiguity",
        "claim_credit": "no",
    },
    {
        "row_id": "R6_alpha2",
        "activated_by": "PG0",
        "new_state": "retained_preferred_frame_vector",
        "why": "observed-time charge generator can carry vector/preferred-frame ambiguity",
        "claim_credit": "no",
    },
    {
        "row_id": "R7_alpha3",
        "activated_by": "PG4;PG6",
        "new_state": "retained_exchange_flux",
        "why": "boundary/source residual flux can become momentum nonconservation",
        "claim_credit": "no",
    },
    {
        "row_id": "R8_xi",
        "activated_by": "PG0;PG3;PG4;PG6;PG8",
        "new_state": "retained_boundary_domain_location",
        "why": "boundary/domain hair can shift Gauss source or preferred-location response",
        "claim_credit": "no",
    },
    {
        "row_id": "R9_Gdot",
        "activated_by": "PG0;PG1;PG4;PG6;PG7;PG8",
        "new_state": "retained_Gdot_source_drift",
        "why": "G_eff and M_eff derivative silence is not derived",
        "claim_credit": "no",
    },
    {
        "row_id": "R10_fifth_force",
        "activated_by": "PG1;PG3;PG4;PG5;PG6;PG7;PG8",
        "new_state": "retained_curve_required",
        "why": "range/radial dependence requires alpha(lambda) curve or theorem-zero",
        "claim_credit": "no",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "activated_by": "PG0-PG10",
        "new_state": "retained_operator_vector_required",
        "why": "EH-only exterior and source-normalized operator purity are not parent-derived",
        "claim_credit": "no",
    },
]


GATE_TESTS = [
    {
        "gate": "PG_rows_mapped_to_residual_components",
        "pass_condition": "every PG0-PG10 row activates one or more P8/R11 residual components",
        "current_result": "pass",
        "evidence": "11 PG map rows written",
    },
    {
        "gate": "input_template_written",
        "pass_condition": "all canonical P8 source-normalization components plus R11 operator vector have fillable rows",
        "current_result": "pass",
        "evidence": "9 residual input rows written",
    },
    {
        "gate": "claim_flags_blocked",
        "pass_condition": "all generated residual input template rows have valid_for_claim=false",
        "current_result": "pass",
        "evidence": "template rows are scaffolding until filled with theorem-zero or numeric residuals",
    },
    {
        "gate": "row_transitions_preserve_no_promotion",
        "pass_condition": "R0-R11 transitions keep no theorem credit",
        "current_result": "pass",
        "evidence": "12 row transitions have claim_credit=no",
    },
    {
        "gate": "numeric_residuals_loaded",
        "pass_condition": "real theorem-zero, numeric residual, R10 curve, or R11 vector inputs are loaded",
        "current_result": "fail",
        "evidence": "this checkpoint writes mapper/template only",
    },
    {
        "gate": "measured_GM_parent_derived",
        "pass_condition": "PG1 and PG4-PG8 are closed by theorem-zero or valid residual evidence",
        "current_result": "fail",
        "evidence": "all current PG blockers remain retained",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "P8/R11 and PPN rows are theorem-zero or empirically scored",
        "current_result": "fail",
        "evidence": "residual mapper only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "PG residual mapper written",
        "status": "pass",
        "evidence": "PG0-PG10 mapped into P8/R11 components",
    },
    {
        "claim": "source-normalization input template written",
        "status": "pass",
        "evidence": "P8/R11 fillable template rows emitted",
    },
    {
        "claim": "symbolic pass-through blocked",
        "status": "pass",
        "evidence": "all mapper-generated input rows have valid_for_claim=false",
    },
    {
        "claim": "measured GM parent-derived",
        "status": "fail",
        "evidence": "no PG theorem-zero or numeric residual input supplied",
    },
    {
        "claim": "Newton/PPN/local GR promoted",
        "status": "fail",
        "evidence": "mapper only; no residual row has claim credit",
    },
]


DECISION = [
    {
        "decision": "The failed Poisson/Gauss calibration premises are now machine-routed into explicit P8/R11 residual components. This removes a major ambiguity: when PG1 or PG4-PG8 are not derived, the result is no longer a vague 'calibration gap' but concrete rows such as dln_Geff_dt, dln_Meff_dt, eta_source_AB, alpha(lambda), partial_r ln mu_obs, mu_extra/(GM), delta_frame_source, delta_beta_source, and c_nonEH_operator_vector. No numeric residuals or theorem-zero proofs were loaded here, so measured GM, Newton, PPN, and local GR remain unpromoted.",
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "460-source-normalized-Newton-branch-theorem-stack.md",
        "why_next": "assemble the finite Newton branch theorem using the PG mapper so the exact remaining derivation debts are visible",
    },
    {
        "rank": 2,
        "target": "fill_or_derive_PG_residual_inputs",
        "why_next": "the mapper is only useful once rows are filled with theorem-zero proofs, numeric residuals, R10 curves, or R11 vectors",
    },
    {
        "rank": 3,
        "target": "second-order PPN source stability attempt",
        "why_next": "PG9 remains the direct blocker from first-order Newton source calibration to local-GR/PPN completion",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"Cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    csv_fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    table_fieldnames = fieldnames or list(rows[0].keys())
    lines = [
        "| " + " | ".join(table_fieldnames) + " |",
        "| " + " | ".join(["---"] * len(table_fieldnames)) + " |",
    ]
    for row in rows:
        values = []
        for fieldname in table_fieldnames:
            value = str(row.get(fieldname, "")).replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": source_doc["path"],
            "exists": (ROOT / source_doc["path"]).exists(),
            "role": source_doc["role"],
        }
        for source_doc in SOURCE_DOCS
    ]


def build_template_health() -> list[dict[str, Any]]:
    contract_rows = read_csv(ROOT / "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv")
    source_template_rows = read_csv(ROOT / "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv")
    local_template_rows = read_csv(ROOT / "source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv")
    return [
        {
            "artifact": "PG_contract_rows",
            "count": len(contract_rows),
            "expected": 11,
            "status": "pass" if len(contract_rows) == 11 else "fail",
        },
        {
            "artifact": "P8_source_template_rows",
            "count": len(source_template_rows),
            "expected": 8,
            "status": "pass" if len(source_template_rows) == 8 else "fail",
        },
        {
            "artifact": "MTS_local_R_template_rows",
            "count": len(local_template_rows),
            "expected": 12,
            "status": "pass" if len(local_template_rows) == 12 else "fail",
        },
        {
            "artifact": "PG_residual_map_rows",
            "count": len(PG_TO_RESIDUAL_MAP),
            "expected": 11,
            "status": "pass" if len(PG_TO_RESIDUAL_MAP) == 11 else "fail",
        },
        {
            "artifact": "PG_residual_input_template_rows",
            "count": len(RESIDUAL_INPUT_TEMPLATE),
            "expected": 9,
            "status": "pass" if len(RESIDUAL_INPUT_TEMPLATE) == 9 else "fail",
        },
    ]


def build_gate_results(source_register: list[dict[str, Any]], template_health: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_register if not row["exists"]]
    all_input_claim_flags_false = all(row["valid_for_claim"] == "false" for row in RESIDUAL_INPUT_TEMPLATE)
    all_transition_claims_no = all(row["claim_credit"] == "no" for row in ROW_TRANSITIONS)
    mapped_gate_tests = [
        {
            "gate": gate_test["gate"],
            "status": gate_test["current_result"],
            "evidence": gate_test["evidence"],
        }
        for gate_test in GATE_TESTS
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "map_schema_matches",
            "status": "pass" if list(PG_TO_RESIDUAL_MAP[0].keys()) == MAP_COLUMNS else "fail",
            "evidence": str(MAP_PATH),
        },
        {
            "gate": "input_schema_matches",
            "status": "pass" if list(RESIDUAL_INPUT_TEMPLATE[0].keys()) == INPUT_COLUMNS else "fail",
            "evidence": str(INPUT_TEMPLATE_PATH),
        },
        {
            "gate": "template_health_passes",
            "status": "pass" if all(row["status"] == "pass" for row in template_health) else "fail",
            "evidence": "; ".join(f'{row["artifact"]}={row["count"]}' for row in template_health),
        },
        {
            "gate": "claim_flags_blocked",
            "status": "pass" if all_input_claim_flags_false else "fail",
            "evidence": "all generated input rows valid_for_claim=false",
        },
        {
            "gate": "row_transition_claims_blocked",
            "status": "pass" if all_transition_claims_no else "fail",
            "evidence": "all R0-R11 transitions keep claim_credit=no",
        },
        *mapped_gate_tests,
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(
    run_dir: Path,
    source_register: list[dict[str, Any]],
    template_health: list[dict[str, Any]],
    gate_results: list[dict[str, str]],
) -> str:
    return f"""# 459 - PG Calibration Residual Mapper

Private P8/R0-R11 residual-mapping checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 458 made the Poisson/Gauss measured-GM bridge exact but conditional. This checkpoint converts every failed `PG0-PG10` condition into explicit residual rows.

The aim is to stop the branch from saying "not derived yet" in prose. Each failure must now become either:

```text
derived_zero,
derived_bound,
numeric residual input,
R10 curve,
R11 operator vector,
or retained no-claim row.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PG_calibration_residual_mapper.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Residual map | `{MAP_PATH}` |
| Input template | `{INPUT_TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Template Health

{markdown_table(template_health)}

## 5. PG to Residual Map

The PG residual map has been written to `{MAP_PATH}`.

{markdown_table(PG_TO_RESIDUAL_MAP, MAP_COLUMNS)}

## 6. Residual Input Template

The fillable PG residual input template has been written to `{INPUT_TEMPLATE_PATH}`.

{markdown_table(RESIDUAL_INPUT_TEMPLATE, INPUT_COLUMNS)}

## 7. R0-R11 Row Transitions

{markdown_table(ROW_TRANSITIONS)}

## 8. Gate Tests

{markdown_table(GATE_TESTS)}

## 9. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 10. Gate Results

{markdown_table(gate_results)}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is the referee's scorecard for the Newton route. If the Hamiltonian charge does not become `GM`, we now know exactly which row gets punched: drift, source charge, radial hair, `mu_extra`, frame split, beta source residue, or the R11 operator vector. That is progress because it turns a philosophical blocker into fillable rows.

## 12. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    template_health = build_template_health()
    gate_results = build_gate_results(source_register, template_health)
    missing_sources = [row["source_file"] for row in source_register if not row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "template_health.csv", template_health)
    write_csv(results_dir / "PG_to_residual_map.csv", PG_TO_RESIDUAL_MAP, MAP_COLUMNS)
    write_csv(results_dir / "PG_residual_input_template.csv", RESIDUAL_INPUT_TEMPLATE, INPUT_COLUMNS)
    write_csv(results_dir / "row_transitions.csv", ROW_TRANSITIONS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / MAP_PATH, PG_TO_RESIDUAL_MAP, MAP_COLUMNS)
    write_csv(ROOT / INPUT_TEMPLATE_PATH, RESIDUAL_INPUT_TEMPLATE, INPUT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, template_health, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "PG_rows_mapped": len(PG_TO_RESIDUAL_MAP),
        "residual_input_rows": len(RESIDUAL_INPUT_TEMPLATE),
        "all_input_rows_valid_for_claim": False,
        "all_row_transitions_claim_credit": False,
        "numeric_residuals_loaded": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "template_health": template_health,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the MTS PG calibration residual mapper.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-191500.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
