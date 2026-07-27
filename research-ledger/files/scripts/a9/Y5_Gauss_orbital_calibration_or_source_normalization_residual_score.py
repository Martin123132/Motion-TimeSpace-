from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Gauss_orbital_calibration_chain_written_residual_scorecard_unfilled_no_measured_GM_Newton_PPN_or_local_GR_promotion"
CLAIM_CEILING = "Gauss_orbital_calibration_or_source_normalization_residual_score_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "524-Y5-second-order-PPN-source-stability-or-residual-evaluator.md"

DOC_PATH = Path("523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_SOURCE_REGISTER.csv")
FORMULA_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv")
CALIBRATION_CHAIN_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_CALIBRATION_CHAIN.csv")
RESIDUAL_SCORECARD_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "role": "imports the channelwise mu_extra obstruction and no-cancellation policy",
    },
    {
        "source_file": "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "role": "Ward-to-mass-flux bridge showing conservation is not yet mass-flux closure",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M owner fork and projector commutator/radial bound inputs",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "PG0-PG10 charge-to-Poisson/Gauss calibration contract",
    },
    {
        "source_file": "459-PG-calibration-residual-mapper.md",
        "role": "maps failed PG rows into executable P8/R11 residual rows",
    },
    {
        "source_file": "460-source-normalized-Newton-branch-theorem-stack.md",
        "role": "SN0-SN11 source-normalized Newton theorem stack",
    },
    {
        "source_file": "461-PG-residual-input-derive-or-fill-gate.md",
        "role": "shows all PG residual input rows are retained and unfilled",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert-current-to-measured-GM calibration blockers",
    },
    {
        "source_file": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal G_eff/kappa attempt and derivative-silence debt",
    },
    {
        "source_file": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "earlier GM absorption theorem and absolute-calibration warning",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "machine-readable PG calibration contract rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv",
        "role": "machine-readable PG-to-residual map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PG_residual_input_STATUS.csv",
        "role": "machine-readable status showing PG residual inputs are unfilled/no-claim",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "machine-readable SN0-SN11 Newton theorem stack",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "Hilbert-monopole measured-GM contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "canonical source-normalization residual-vector template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "same-source/same-measure residual map for M_eff flux",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv",
        "role": "nine channelwise extra-mass residual inputs from checkpoint 522",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv",
        "role": "observable map for total extra-mass and radial/PPN source residuals",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local empirical locks for WEP, gamma, beta, preferred-frame, Gdot, fifth-force, and R11",
    },
    {
        "source_file": "scripts/Y5_Gauss_orbital_calibration_or_source_normalization_residual_score.py",
        "role": "this checkpoint generator",
    },
]


FORMULA_LEDGER_ROWS = [
    {
        "formula_id": "GO523_0_observed_orbital_monopole",
        "quantity": "mu_obs",
        "formula": "mu_obs(r,A,t,lambda)=r^2 |a_r|=v^2 r for a slow nearly circular test body in the observed frame",
        "meaning": "the actual Newtonian observable is orbital GM, not an arbitrary conserved current",
        "status": "definition_for_gate",
    },
    {
        "formula_id": "GO523_1_parent_source_monopole",
        "quantity": "mu_parent",
        "formula": "mu_parent=G_eff M_H[Pi_M J_H]",
        "meaning": "the candidate parent-derived source side after same-frame Hilbert current and Pi_M projection",
        "status": "conditional_candidate_not_calibrated",
    },
    {
        "formula_id": "GO523_2_Gauss_residual",
        "quantity": "Delta_mu_Gauss",
        "formula": "surface_int_S grad Phi dot dS = 4 pi (G_eff M_H + Delta_mu_Gauss)",
        "meaning": "volume, boundary, non-EH, projector, and domain terms enter Gauss mass unless theorem-zero",
        "status": "residual_active_until_zero_or_scored",
    },
    {
        "formula_id": "GO523_3_extra_source_residual",
        "quantity": "mu_extra",
        "formula": "mu_obs=G_eff M_H + mu_extra + Delta_mu_Gauss + Delta_mu_readout",
        "meaning": "extra mass channels from 522 are physical residuals, not notation",
        "status": "channelwise_inputs_written_not_filled",
    },
    {
        "formula_id": "GO523_4_source_normalization_error",
        "quantity": "epsilon_SN",
        "formula": "epsilon_SN=(mu_obs-G_eff M_H)/(G_eff M_H)",
        "meaning": "dimensionless score target for source-normalization mismatch",
        "status": "score_target_defined_not_evaluated",
    },
    {
        "formula_id": "GO523_5_no_cancellation_bound",
        "quantity": "epsilon_SN_bound",
        "formula": "|epsilon_SN| <= |epsilon_charge|+|epsilon_Poisson|+|epsilon_Gauss|+|epsilon_orbit|+sum_i|epsilon_extra_i|+|epsilon_derivative|+|epsilon_PPN|",
        "meaning": "open residuals cannot be hidden by tuned signs",
        "status": "policy_active_unscored",
    },
    {
        "formula_id": "GO523_6_PPN_residual_vector",
        "quantity": "Delta_PPN_source",
        "formula": "Delta_PPN_source=(gamma-1, beta-1, alpha1, alpha2, alpha3, xi)_source after measured-GM normalization",
        "meaning": "first-order Newton is not local GR until second-order source/operator residues vanish",
        "status": "next_gate_not_derived",
    },
]


CALIBRATION_CHAIN_ROWS = [
    {
        "chain_id": "CAL523_0_observed_frame_and_charge",
        "gate": "observed-time Hamiltonian charge exists",
        "required_identity": "the charge B_xi is generated by observed time and uses the same frame as matter/orbits",
        "math_form": "H_xi=B_xi on shell; e_source=e_matter=e_obs",
        "mapped_prior_rows": "PG0;PG2;SN0;SN2",
        "open_debt": "observed-frame charge is conditional and frame residuals remain retained",
        "current_status": "conditional_not_parent_derived",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_1_charge_current_identity",
        "gate": "charge equals projected Hilbert source",
        "required_identity": "the Hamiltonian charge is the parent-defined Pi_M Hilbert mass current",
        "math_form": "B_xi/G_eff=M_eff[Pi_M J_H]; delta B_xi=delta int_S Pi_M J_H",
        "mapped_prior_rows": "PG1;SN3;HM2;HM3;Y5B_1",
        "open_debt": "Pi_M ownership, commutator silence, Hilbert equality, and absolute normalization remain open",
        "current_status": "not_parent_derived",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_2_EH_Poisson_coefficient",
        "gate": "same-frame EH-to-Poisson coefficient",
        "required_identity": "the weak-field 00 equation is EH-only and has the standard coefficient",
        "math_form": "nabla^2 Phi=(kappa_eff c^4/2)rho_H=4 pi G_eff rho_H",
        "mapped_prior_rows": "PG3;SN1;SN5;R11",
        "open_debt": "EH-only local exterior and zero source-residual operator vector are not parent-derived",
        "current_status": "conditional_R11_vector_unfilled",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_3_Gauss_surface_no_residual",
        "gate": "Gauss integral equals enclosed source mass",
        "required_identity": "surface Gauss mass has no residual volume, boundary, non-EH, domain, projector, or memory terms",
        "math_form": "surface_int_S grad Phi dot dS=4 pi G_eff M_eff with Delta_mu_Gauss=0",
        "mapped_prior_rows": "PG4;SN4;SN8;EX522_0;EX522_1;EX522_3;EX522_6",
        "open_debt": "closed Pi_M flux and all Gauss residual channels are unfilled/not theorem-zero",
        "current_status": "not_derived_not_scored",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_4_orbital_inverse_square_readout",
        "gate": "slow orbital readout is pure inverse square",
        "required_identity": "test bodies read the same Phi with no finite-range, radial, frame, species, or direct-force correction",
        "math_form": "a_r=-partial_r Phi=-G_eff M_eff/r^2 and v^2 r=G_eff M_eff",
        "mapped_prior_rows": "PG5;SN9;R0;R1;R2;R10",
        "open_debt": "same-frame orbital readout and alpha(lambda)/radial/source residual curves are unfilled",
        "current_status": "not_derived_not_scored",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_5_zero_extra_mass_projection",
        "gate": "no hidden extra mass source",
        "required_identity": "all 522 extra current channels have zero Pi_M projection or valid below-lock residual bounds",
        "math_form": "Pi_M dJ_extra=0; mu_extra=0; S_res=0",
        "mapped_prior_rows": "PG6;SN6;EX522_0..EX522_8;OM522_0",
        "open_debt": "nine channelwise rows are visible but unfilled; no mu_extra=0 theorem",
        "current_status": "channelwise_inputs_written_not_filled",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_6_constant_universal_Geff",
        "gate": "constant universal coupling",
        "required_identity": "G_eff/kappa_eff is constant, universal, source-blind, range-blind, frame-blind, and domain-blind",
        "math_form": "partial_{t,r,A,lambda,frame,domain} G_eff=0",
        "mapped_prior_rows": "PG7;SN7;HM4;EX522_4",
        "open_debt": "global coupling superselection is not parent-derived; Gdot/source/range rows remain retained",
        "current_status": "not_parent_derived",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_7_no_derivative_hair",
        "gate": "measured source strength has no derivative hair",
        "required_identity": "mu_obs has no time, radial, species, range, frame, or domain derivative",
        "math_form": "partial_t mu_obs=partial_r mu_obs=partial_A mu_obs=partial_lambda mu_obs=partial_frame mu_obs=partial_domain mu_obs=0",
        "mapped_prior_rows": "PG8;SN10;R1;R4;R9;R10;Y5B_2",
        "open_debt": "derivative silence is not derived and no residual profile/curve is loaded",
        "current_status": "not_derived_not_scored",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_8_second_order_PPN_source_stability",
        "gate": "first-order calibration survives PPN order",
        "required_identity": "after measured-GM normalization, beta/gamma and preferred-frame/source residues vanish",
        "math_form": "delta_beta_source=0; gamma-1=0; alpha_i=0; xi=0 in the source-normalized local branch",
        "mapped_prior_rows": "PG9;SN11;R3;R4;R5;R6;R7;R8;R11",
        "open_debt": "second-order source/operator expansion is still missing",
        "current_status": "not_derived",
        "claim_credit": "false",
    },
    {
        "chain_id": "CAL523_9_residual_score_all_clear",
        "gate": "scorecard is derived-zero or below local locks",
        "required_identity": "every open calibration residual is either theorem-zero or numerically below its mapped local bound",
        "math_form": "all_i score_i in {derived_zero, below_bound}; no edge/open/manual closure rows",
        "mapped_prior_rows": "PG10;P8 residual inputs;local_bound_claims",
        "open_debt": "scorecard is written here but not filled or evaluated",
        "current_status": "scorecard_unfilled_no_claim",
        "claim_credit": "false",
    },
]


RESIDUAL_SCORECARD_ROWS = [
    {
        "score_id": "SRC523_0_charge_current_normalization",
        "residual_symbol": "epsilon_charge",
        "definition": "(B_xi/G_eff - M_H[Pi_M J_H])/M_H",
        "activated_by": "PG1;CAL523_1",
        "required_input": "charge-current equality proof or dimensionless mismatch with source file",
        "observable_lock": "measured-GM normalization;R4;R9;R11",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_1_Poisson_operator_source",
        "residual_symbol": "epsilon_Poisson_or_c_nonEH",
        "definition": "deviation of local 00 operator/source coefficient from 4 pi G_eff rho_H",
        "activated_by": "PG3;CAL523_2",
        "required_input": "EH-only theorem or executable R11 operator coefficient vector",
        "observable_lock": "gamma<=2.3e-5;beta<=7.8e-5;alpha(lambda);R11",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_2_Gauss_volume_boundary",
        "residual_symbol": "epsilon_Gauss",
        "definition": "Delta_mu_Gauss/(G_eff M_H) from volume/boundary/projector/domain terms",
        "activated_by": "PG4;CAL523_3",
        "required_input": "Gauss no-residual theorem or volume/boundary residual integral",
        "observable_lock": "beta;alpha3<=4e-20;xi<=4e-9;Gdot<=9.6e-15 yr^-1",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_3_orbital_readout",
        "residual_symbol": "epsilon_orbit",
        "definition": "(r^2 |a_r|-mu_Gauss)/mu_Gauss after same-frame slow-particle readout",
        "activated_by": "PG5;CAL523_4",
        "required_input": "geodesic/readout proof or orbital residual profile",
        "observable_lock": "WEP/source charge;clock/frame;alpha(lambda);radial source hair",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_4_extra_mass_channels_total",
        "residual_symbol": "epsilon_mu_extra_total",
        "definition": "sum_i |epsilon_extra_i| over 522 boundary/domain/bulk/nonEH/kappa/frame/species/projector/anomaly/calibration channels",
        "activated_by": "PG6;CAL523_5;OM522_0",
        "required_input": "all nine 522 channel rows theorem-zero or individually below mapped local locks",
        "observable_lock": "R3;R4;R7;R8;R9;R10;R11",
        "current_value": "not_loaded",
        "score_status": "unfilled_no_cancellation",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_5_Geff_time_or_range_drift",
        "residual_symbol": "dln_Geff_dt;partial_r_Geff;partial_lambda_Geff",
        "definition": "derivatives of the effective coupling after source normalization",
        "activated_by": "PG7;PG8;CAL523_6;CAL523_7",
        "required_input": "global coupling superselection proof or derivative residual rows",
        "observable_lock": "Gdot/G<=9.6e-15 yr^-1;alpha(lambda)",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_6_Meff_flux_derivative",
        "residual_symbol": "dln_Meff_dt;partial_r_ln_Meff",
        "definition": "time/radial derivative of the projected Hilbert mass flux after Pi_M ownership",
        "activated_by": "PG1;PG4;PG8;Y5B_1;Y5B_2",
        "required_input": "d(Pi_M J_H)=0 proof including [d,Pi_M]J_H=0, or derivative profile",
        "observable_lock": "beta;Gdot;radial source hair",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_7_species_source_charge",
        "residual_symbol": "eta_source_AB",
        "definition": "composition/source dependence of the active gravitational source charge",
        "activated_by": "PG5;PG7;PG8",
        "required_input": "selector-blind source theorem or eta_source_AB residual",
        "observable_lock": "eta_source_AB<=2.8e-15",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_8_radial_source_hair",
        "residual_symbol": "partial_r_ln_mu_obs",
        "definition": "radial derivative/envelope of measured source strength outside compact support",
        "activated_by": "PG4;PG5;PG6;PG8",
        "required_input": "no-radial-hair theorem or executable radial profile",
        "observable_lock": "gamma;beta;fifth-force curve",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_9_range_dependence",
        "residual_symbol": "alpha(lambda)",
        "definition": "finite-range/Yukawa or non-Yukawa source-normalization correction curve",
        "activated_by": "PG3;PG5;PG6;PG7;PG8",
        "required_input": "no-range theorem or lambda/alpha_predicted/alpha_bound curve",
        "observable_lock": "R10 fifth-force symbolic curve required",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_10_second_order_PPN_source",
        "residual_symbol": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
        "definition": "PPN source/operator residue after the first-order measured-GM calibration",
        "activated_by": "PG9;SN11;CAL523_8",
        "required_input": "second-order weak-field source/operator derivation or beta/gamma residual vector",
        "observable_lock": "gamma<=2.3e-5;beta<=7.8e-5;preferred-frame/location locks",
        "current_value": "not_loaded",
        "score_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "score_id": "SRC523_11_total_no_cancellation_score",
        "residual_symbol": "epsilon_SN_envelope",
        "definition": "no-cancellation envelope over all open source-normalization calibration residuals",
        "activated_by": "GO523_5;PG10;CAL523_9",
        "required_input": "every preceding row theorem-zero or bounded with units, normalization, and source path",
        "observable_lock": "all mapped local locks; no manual closure credit",
        "current_value": "not_computed",
        "score_status": "not_run_preconditions_unfilled",
        "valid_for_claim": "false",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "AG523_0_source_paths_exist",
        "pass_condition": "all cited source paths exist inside post-checkpoint-work",
        "current_result": "computed_in_validation",
        "claim_effect": "fail_if_missing",
    },
    {
        "gate_id": "AG523_1_chain_complete",
        "pass_condition": "calibration chain covers charge, Poisson, Gauss, orbit, extra mass, G_eff, derivative hair, PPN, and residual score",
        "current_result": "written_but_not_satisfied",
        "claim_effect": "no_claim_until_all_chain_rows_close",
    },
    {
        "gate_id": "AG523_2_no_extra_mass_unfilled",
        "pass_condition": "all 522 extra-mass channels are theorem-zero or individually below local locks",
        "current_result": "fail_open_channels_unfilled",
        "claim_effect": "blocks_measured_GM_and_Newton",
    },
    {
        "gate_id": "AG523_3_residual_scorecard_scored",
        "pass_condition": "all scorecard rows have numeric or theorem-zero evidence with units and source paths",
        "current_result": "fail_scorecard_unfilled",
        "claim_effect": "blocks_source_normalized_Newton",
    },
    {
        "gate_id": "AG523_4_PPN_source_stability",
        "pass_condition": "second-order beta/gamma/source/operator residual vector vanishes or is below locks",
        "current_result": "fail_not_derived",
        "claim_effect": "blocks_local_GR_even_if_Newton_lands",
    },
    {
        "gate_id": "AG523_5_no_overclaim",
        "pass_condition": "no row grants measured-GM/Newton/PPN/local-GR credit before derivation or scoring",
        "current_result": "pass_policy_enforced",
        "claim_effect": "keeps_private_checkpoint_safe",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D523_0_chain_written",
        "status": "exact_calibration_contract_written",
        "meaning": "closed/silent source charge becomes orbital GM only through a finite chain from observed charge to Poisson, Gauss, orbital readout, zero extra mass, constant G_eff, derivative silence, and PPN stability",
        "claim_status": "conditional_not_satisfied",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D523_1_scorecard_unfilled",
        "status": "residual_scorecard_written_not_scored",
        "meaning": "the branch now has explicit residual rows, but no numeric/theorem-zero evidence has been loaded",
        "claim_status": "no_Newton_or_local_GR_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D523_2_measured_GM_not_derived",
        "status": "mu_obs_equals_Geff_MH_not_parent_derived",
        "meaning": "conservation, Pi_M ownership, and extra-mass silence are still not enough without Gauss/orbital calibration",
        "claim_status": "source_normalization_open",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D523_3_second_order_is_next",
        "status": "PPN_source_stability_is_next_hard_gate",
        "meaning": "even a future first-order Newton pass would still require beta/gamma/source/operator stability at second order",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D523_4_private_no_github",
        "status": "private_checkpoint_only",
        "meaning": "this work stays in post-checkpoint-work and is not pushed to GitHub",
        "claim_status": "internal_derivation_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5_GAUSS_ORBITAL_CALIBRATION",
        "previous_status": "selected_as_next_after_522_extra_mass_projection_gate",
        "new_status": "calibration_chain_and_residual_scorecard_written_unfilled_no_claim",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_EXTRA_MASS_PROJECTION",
        "previous_status": "channelwise_bound_inputs_written_not_filled",
        "new_status": "imported_as_required_zero_or_bound_component_of_orbital_GM_calibration",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_unfilled_mu_extra_channels_and_Gauss_orbital_calibration",
        "new_status": "still_blocked_scorecard_unfilled_and_measured_GM_not_parent_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_extra_mass_projection_and_second_order_PPN_source_stability",
        "new_status": "still_blocked_by_unfilled_source_normalization_scorecard_and_second_order_PPN_source_vector",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PUBLIC_REPO",
        "previous_status": "github_updates_paused_by_user",
        "new_status": "no_push_no_commit_private_work_only",
        "accepted_for_claim": "false",
        "next_target": "continue_private_framework_work",
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
        rows.append({**item, "exists": full_path.exists()})
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    pg_contract_rows = read_csv(Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"))
    pg_map_rows = read_csv(Path("source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv"))
    pg_status_rows = read_csv(Path("source-intake/mts_residuals/P8_PG_residual_input_STATUS.csv"))
    newton_stack_rows = read_csv(Path("source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv"))
    extra_channel_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"))
    local_bound_rows = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    local_row_ids = {row.get("row_id", "") for row in local_bound_rows}
    required_local_rows = {"R1_WEP_source_charge", "R3_gamma", "R4_beta", "R9_Gdot", "R10_fifth_force", "R11_EH_operator_ledger"}
    score_claim_rows = [row for row in RESIDUAL_SCORECARD_ROWS if row["valid_for_claim"] == "true"]
    chain_claim_rows = [row for row in CALIBRATION_CHAIN_ROWS if row["claim_credit"] == "true"]
    pg_claim_rows = [row for row in pg_status_rows if row.get("valid_for_claim", "").lower() == "true"]
    extra_claim_rows = [row for row in extra_channel_rows if row.get("valid_for_claim", "").lower() == "true"]
    required_chain_ids = {
        "CAL523_0_observed_frame_and_charge",
        "CAL523_1_charge_current_identity",
        "CAL523_2_EH_Poisson_coefficient",
        "CAL523_3_Gauss_surface_no_residual",
        "CAL523_4_orbital_inverse_square_readout",
        "CAL523_5_zero_extra_mass_projection",
        "CAL523_6_constant_universal_Geff",
        "CAL523_7_no_derivative_hair",
        "CAL523_8_second_order_PPN_source_stability",
        "CAL523_9_residual_score_all_clear",
    }
    chain_ids = {row["chain_id"] for row in CALIBRATION_CHAIN_ROWS}
    return [
        {
            "check_id": "V523_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V523_1_prior_PG_contract_loaded",
            "result": "pass" if len(pg_contract_rows) >= 11 else "fail",
            "detail": f"pg_contract_rows={len(pg_contract_rows)}",
        },
        {
            "check_id": "V523_2_prior_PG_map_and_status_loaded",
            "result": "pass" if len(pg_map_rows) >= 11 and len(pg_status_rows) >= 9 else "fail",
            "detail": f"pg_map_rows={len(pg_map_rows)};pg_status_rows={len(pg_status_rows)};pg_claim_rows={len(pg_claim_rows)}",
        },
        {
            "check_id": "V523_3_Newton_stack_loaded",
            "result": "pass" if len(newton_stack_rows) >= 12 else "fail",
            "detail": f"newton_stack_rows={len(newton_stack_rows)}",
        },
        {
            "check_id": "V523_4_extra_mass_channels_loaded",
            "result": "pass" if len(extra_channel_rows) == 9 and not extra_claim_rows else "fail",
            "detail": f"extra_channel_rows={len(extra_channel_rows)};extra_claim_rows={len(extra_claim_rows)}",
        },
        {
            "check_id": "V523_5_chain_coverage",
            "result": "pass" if required_chain_ids.issubset(chain_ids) and not chain_claim_rows else "fail",
            "detail": f"chain_rows={len(CALIBRATION_CHAIN_ROWS)};claim_credit_rows={len(chain_claim_rows)}",
        },
        {
            "check_id": "V523_6_scorecard_written_unclaimed",
            "result": "pass" if len(RESIDUAL_SCORECARD_ROWS) == 12 and not score_claim_rows else "fail",
            "detail": f"score_rows={len(RESIDUAL_SCORECARD_ROWS)};score_claim_rows={len(score_claim_rows)};scored=false",
        },
        {
            "check_id": "V523_7_local_locks_available",
            "result": "pass" if required_local_rows.issubset(local_row_ids) else "fail",
            "detail": f"required_local_rows_present={required_local_rows.issubset(local_row_ids)};local_rows={len(local_bound_rows)}",
        },
        {
            "check_id": "V523_8_no_overclaim",
            "result": "pass" if not score_claim_rows and not chain_claim_rows and not pg_claim_rows and not extra_claim_rows else "fail",
            "detail": "measured_GM_parent_derived=false; source_normalized_Newton_promoted=false; PPN_promoted=false; local_GR_claim_allowed=false",
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
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 523 - Y5 Gauss Orbital Calibration or Source Normalization Residual Score

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This is the exact place where a tempting shortcut has to be stopped.

A closed/silent source charge is still not automatically the measured orbital `GM`. The chain has to land all the way from parent charge to Poisson coefficient to Gauss surface mass to slow-orbit readout:

```text
H_xi -> B_xi/G_eff -> M_H[Pi_M J_H] -> Phi -> surface Gauss mass -> r^2 |a_r|.
```

Current MTS has useful pieces, but the full calibration is not derived. This checkpoint writes the finite contract and a residual scorecard. Nothing here promotes measured `GM`, Newton, PPN, or local GR.

## 2. Formula Ledger

{markdown_table(FORMULA_LEDGER_ROWS)}

## 3. Calibration Chain

{markdown_table(CALIBRATION_CHAIN_ROWS)}

## 4. Residual Scorecard

{markdown_table(RESIDUAL_SCORECARD_ROWS)}

## 5. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

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
MTS now has an explicit Gauss/orbital calibration contract.
The measured-GM obstruction is finite and row-addressable.
The source-normalization residual scorecard is written.
The no-cancellation policy is preserved.
```

Forbidden:

```text
MTS has derived mu_obs = G_eff M_H.
MTS has derived measured orbital GM from the parent source charge.
MTS has scored the source-normalization residual vector below local locks.
MTS has derived source-normalized Newton, PPN silence, or local GR.
```

## 11. Next Target

`{NEXT_TARGET}`

The sharpest next derivation target is second-order PPN source stability. If the first-order Gauss/Newton chain ever lands, local GR still fails unless the same measured-GM normalization survives the beta/gamma/source/operator expansion.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (FORMULA_LEDGER_PATH, FORMULA_LEDGER_ROWS),
        (CALIBRATION_CHAIN_PATH, CALIBRATION_CHAIN_ROWS),
        (RESIDUAL_SCORECARD_PATH, RESIDUAL_SCORECARD_ROWS),
        (ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
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
        "formula_ledger": str(ROOT / FORMULA_LEDGER_PATH),
        "calibration_chain": str(ROOT / CALIBRATION_CHAIN_PATH),
        "residual_scorecard": str(ROOT / RESIDUAL_SCORECARD_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "formula_rows": len(FORMULA_LEDGER_ROWS),
        "calibration_chain_rows": len(CALIBRATION_CHAIN_ROWS),
        "residual_scorecard_rows": len(RESIDUAL_SCORECARD_ROWS),
        "failed_validation_rows": len(failed_validations),
        "gauss_orbital_calibration_chain_written": True,
        "residual_scorecard_written": True,
        "residual_scorecard_scored": False,
        "calibration_parent_derived_for_MTS": False,
        "measured_GM_parent_derived": False,
        "mu_obs_equals_Geff_MH_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
