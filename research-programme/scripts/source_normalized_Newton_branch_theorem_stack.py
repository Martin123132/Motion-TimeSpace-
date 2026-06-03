from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-normalized-Newton-branch-theorem-stack"
CHECKPOINT_DOC = "460-source-normalized-Newton-branch-theorem-stack.md"
STATUS = "source_normalized_Newton_branch_theorem_stack_written_conditional_theorem_only_PG_residual_bindings_visible_no_measured_GM_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_Newton_theorem_stack_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "461-PG-residual-input-derive-or-fill-gate.md"
STACK_PATH = Path("source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv")


STACK_COLUMNS = [
    "rung_id",
    "required_identity",
    "math_form",
    "theorem_use",
    "depends_on",
    "residual_if_failed",
    "current_status",
    "valid_for_Newton_claim",
    "valid_for_local_GR_claim",
    "next_action",
]

PG_BINDING_COLUMNS = [
    "pg_id",
    "stack_rungs",
    "residual_symbol",
    "affected_rows",
    "current_status",
    "valid_for_claim",
    "why_it_blocks_Newton_or_GR",
]

BLOCKER_COLUMNS = [
    "rank",
    "blocker",
    "dominant_stack_rungs",
    "dominant_pg_rows",
    "why_it_matters",
    "best_next_action",
]


SOURCE_DOCS = [
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "same-frame EH/source-to-Poisson reduction gate",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH/operator residual ledger and source-normalization transition rules",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "non-EH operator vector contract required if EH-only is not derived",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "EH-only local exterior parent-premise ladder",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "second-order metric/PPN sector reduction attempt",
    },
    {
        "path": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration gate",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector and Euler closure attempt",
    },
    {
        "path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "role": "constant universal Geff/kappa identity attempt",
    },
    {
        "path": "453-global-coupling-superselection-parent-action-contract.md",
        "role": "global coupling superselection parent-action contract",
    },
    {
        "path": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Pi_M flux closure Ward/topological current attempt",
    },
    {
        "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge route to mass current",
    },
    {
        "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "PG0-PG10 Hamiltonian charge to Poisson/Gauss calibration gate",
    },
    {
        "path": "459-PG-calibration-residual-mapper.md",
        "role": "PG failures mapped into explicit P8/R11 residual components",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "machine-readable PG0-PG10 calibration contract",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_calibration_residual_MAP.csv",
        "role": "machine-readable PG-to-residual map",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_calibration_residual_INPUT_TEMPLATE.csv",
        "role": "fillable residual input template for failed PG rows",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "canonical local R0-R11 residual components",
    },
    {
        "path": "runs/20260602-181500-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate/results/Poisson_Gauss_calibration_contract.csv",
        "role": "run artifact for PG0-PG10 rows",
    },
    {
        "path": "runs/20260602-191500-PG-calibration-residual-mapper/results/PG_to_residual_map.csv",
        "role": "run artifact for PG-to-residual bindings",
    },
    {
        "path": "runs/20260602-191500-PG-calibration-residual-mapper/results/PG_residual_input_template.csv",
        "role": "run artifact for fillable PG residual rows",
    },
]


THEOREM_STATEMENT = [
    {
        "claim": "conditional_source_normalized_Newton_theorem",
        "statement": "If SN0-SN10 are parent-derived theorem-zero identities, or are filled by valid residual evidence with zero effective residue, the local weak-field branch reduces to the Newtonian measured-GM force law.",
        "math_form": "nabla^2 Phi = 4 pi G0 rho_H; surface_integral grad Phi dot dS = 4 pi G0 M_H; a = -grad Phi = -G0 M_H rhat/r^2; mu_obs = G0 M_H",
        "current_status": "theorem_stack_written_conditionally_not_satisfied",
    },
    {
        "claim": "residualized_failure_theorem",
        "statement": "If any SN rung fails, the failed premise must appear as a P8/R11 residual component rather than being absorbed into GM by prose.",
        "math_form": "mu_obs = G_eff M_eff + mu_extra; d ln mu_obs = d ln G_eff + d ln M_eff + d[mu_extra/(G_eff M_eff)]",
        "current_status": "mapper_available_but_inputs_unfilled",
    },
    {
        "claim": "Newton_not_local_GR",
        "statement": "A first-order Poisson/Gauss success would still not promote local GR unless SN11 also kills the second-order beta/gamma/source/operator residues.",
        "math_form": "gamma - 1 = 0 and delta_beta_source = 0 after measured-GM normalization",
        "current_status": "not_derived",
    },
    {
        "claim": "current_corpus_status",
        "statement": "The current corpus has the finite theorem target and residual bindings, but not parent-derived measured GM, not a Newton pass, and not local GR.",
        "math_form": "exists stack; not exists filled theorem-zero or numeric residual certificate for all required rungs",
        "current_status": "no_promotion",
    },
]


NEWTON_STACK = [
    {
        "rung_id": "SN0_same_observed_frame",
        "required_identity": "matter, clocks, rods, photons, and metric-source variation use one observed coframe/frame",
        "math_form": "e_obs = e_matter = e_source; delta_frame_source = 0",
        "theorem_use": "lets orbital acceleration read the same Phi sourced by the weak-field equation",
        "depends_on": "424;459-PG2;459-PG8",
        "residual_if_failed": "delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector",
        "current_status": "conditional_not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive same-frame source variation or fill frame residual input",
    },
    {
        "rung_id": "SN1_EH_or_R11_operator_zero",
        "required_identity": "local exterior operator is EH-only, or every non-EH R11 coefficient is theorem-zero or scored",
        "math_form": "E_munu = G_munu + Lambda g_munu + sum_i c_i O_i; require c_i O_i -> 0 in local branch",
        "theorem_use": "allows the 00 weak-field equation to reduce to a Poisson operator",
        "depends_on": "425;438;439;459-PG0;459-PG3;459-PG9",
        "residual_if_failed": "c_nonEH_operator_vector;gamma_minus_1;delta_beta_source;alpha(lambda)",
        "current_status": "conditional_EH_only_not_parent_derived_R11_vector_unfilled",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive EH-only exterior from parent action or fill executable R11 vector",
    },
    {
        "rung_id": "SN2_observed_time_Hamiltonian_charge",
        "required_identity": "the boundary charge is well-defined, conserved, and generated by observed time",
        "math_form": "H_xi = B_xi on shell with xi normalized in the observed frame",
        "theorem_use": "gives a candidate source charge before attempting measured-GM identification",
        "depends_on": "457;458-PG0;459-PG0",
        "residual_if_failed": "c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source",
        "current_status": "conditional_from_457_not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "prove observed-time Hamiltonian charge or keep charge/reference residuals",
    },
    {
        "rung_id": "SN3_charge_equals_Hilbert_mass_current",
        "required_identity": "Hamiltonian boundary charge equals the projected Hilbert mass current",
        "math_form": "B_xi/G_eff = M_eff[Pi_M J_H] and delta B_xi = delta integral_S Pi_M J_H",
        "theorem_use": "turns a conserved geometric charge into the source mass that appears in Newton's law",
        "depends_on": "450;457;458-PG1;459-PG1",
        "residual_if_failed": "dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector;eta_source_AB",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive charge-current equality or fill measured-source residual rows",
    },
    {
        "rung_id": "SN4_closed_Meff_flux",
        "required_identity": "projected mass flux is closed and conserved in the compact local exterior",
        "math_form": "d(Pi_M J_H) = 0; partial_t M_eff = 0; partial_r M_eff = 0 outside compact support",
        "theorem_use": "prevents hidden time drift, radial hair, and boundary flux from entering measured GM",
        "depends_on": "451;455;458-PG4;459-PG4;459-PG8",
        "residual_if_failed": "dln_Meff_dt;partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;alpha3",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive closed Pi_M flux or fill mass drift/radial hair residuals",
    },
    {
        "rung_id": "SN5_EH_to_Poisson_coefficient",
        "required_identity": "same-frame weak-field EH 00 equation has the standard source coefficient",
        "math_form": "g_00 = -1 + 2 Phi/c^2; T_00 = rho_H c^2; nabla^2 Phi = (kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H",
        "theorem_use": "sets the curvature-to-Newton coupling normalization",
        "depends_on": "424;452;458-PG3;459-PG3;459-PG7",
        "residual_if_failed": "c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda);dln_Geff_dt",
        "current_status": "conditional_formula_inside_EH_source_stack_only",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "tie kappa_eff to one constant G_eff after source purity is proved",
    },
    {
        "rung_id": "SN6_zero_mu_extra_and_source_residuals",
        "required_identity": "boundary, bulk, domain, memory, projector, range, and connection pieces add no unowned monopole",
        "math_form": "mu_obs = G_eff M_eff + mu_extra with mu_extra = 0 and S_res = 0",
        "theorem_use": "stops extra source terms from masquerading as measured mass",
        "depends_on": "438;450;458-PG6;459-PG6",
        "residual_if_failed": "mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive Ward/no-hair/topological zero route or fill mu_extra map",
    },
    {
        "rung_id": "SN7_constant_universal_Geff",
        "required_identity": "G_eff/kappa_eff is constant, universal, source-blind, range-blind, and frame-blind",
        "math_form": "partial_t,r,A,lambda,frame G_eff = 0",
        "theorem_use": "allows one calibrated G0 instead of hidden Gdot, fifth-force, source-charge, or frame dependence",
        "depends_on": "452;453;458-PG7;459-PG7",
        "residual_if_failed": "dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector",
        "current_status": "conditional_not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive global coupling superselection or fill derivative/source/range residuals",
    },
    {
        "rung_id": "SN8_Gauss_surface_integral",
        "required_identity": "Poisson source integrates to the same enclosed source mass with no residual volume or boundary terms",
        "math_form": "surface_integral grad Phi dot dS = 4 pi G_eff M_eff",
        "theorem_use": "connects local source density to the monopole measured outside the source",
        "depends_on": "450;451;458-PG4;459-PG4",
        "residual_if_failed": "partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "prove Gauss equality for Pi_M source or fill radial/boundary residual envelope",
    },
    {
        "rung_id": "SN9_orbital_inverse_square_readout",
        "required_identity": "slow test bodies read the Gauss monopole as a pure inverse-square acceleration in the observed frame",
        "math_form": "a_r = -partial_r Phi = -G_eff M_eff/r^2 and v^2 r = G_eff M_eff",
        "theorem_use": "turns the source-normalized Poisson branch into measured Kepler/Newton GM",
        "depends_on": "424;458-PG5;459-PG5",
        "residual_if_failed": "alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive slow-particle geodesic readout plus zero range/source/frame terms",
    },
    {
        "rung_id": "SN10_no_derivative_hair",
        "required_identity": "measured source strength has no time, radial, species, range, frame, or domain derivative",
        "math_form": "partial_t mu_obs = partial_r mu_obs = partial_A mu_obs = partial_lambda mu_obs = partial_frame mu_obs = 0",
        "theorem_use": "prevents a fitted constant GM from hiding real local residual physics",
        "depends_on": "452;459-PG8",
        "residual_if_failed": "dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source",
        "current_status": "not_parent_derived",
        "valid_for_Newton_claim": "false",
        "valid_for_local_GR_claim": "false",
        "next_action": "derive derivative-zero identities or fill row-specific residual values",
    },
    {
        "rung_id": "SN11_second_order_PPN_source_stability",
        "required_identity": "first-order source calibration survives beta/gamma/PPN order in the same observed frame",
        "math_form": "gamma - 1 = 0 and delta_beta_source = 0 after measured-GM normalization",
        "theorem_use": "required for local GR; not enough to have only first-order Newton",
        "depends_on": "440;458-PG9;459-PG9",
        "residual_if_failed": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
        "current_status": "not_derived",
        "valid_for_Newton_claim": "not_required_for_first_order_Newton_but_required_for_GR_promotion",
        "valid_for_local_GR_claim": "false",
        "next_action": "perform second-order weak-field source/operator calculation",
    },
]


PG_BINDINGS = [
    {
        "pg_id": "PG0_Hamiltonian_charge_input",
        "stack_rungs": "SN1;SN2",
        "residual_symbol": "c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source",
        "affected_rows": "R2;R4;R5;R6;R8;R9;R11",
        "current_status": "retained_missing_parent_charge",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "without a real observed-time charge, no source mass can be calibrated",
    },
    {
        "pg_id": "PG1_charge_equals_projected_Hilbert_source",
        "stack_rungs": "SN3;SN4;SN6",
        "residual_symbol": "dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "retained_charge_current_split",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "a conserved geometric charge is not yet the Newton source",
    },
    {
        "pg_id": "PG2_same_frame_weak_field_potential",
        "stack_rungs": "SN0;SN5;SN9",
        "residual_symbol": "delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector",
        "affected_rows": "R0;R1;R2;R11",
        "current_status": "retained_frame_split",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "the orbiting body may not read the same potential sourced by the equation",
    },
    {
        "pg_id": "PG3_EH_to_Poisson_coefficient",
        "stack_rungs": "SN1;SN5;SN6",
        "residual_symbol": "c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda)",
        "affected_rows": "R3;R4;R8;R10;R11",
        "current_status": "retained_operator_source_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "operator/source residues change the Poisson coefficient",
    },
    {
        "pg_id": "PG4_Gauss_surface_integral",
        "stack_rungs": "SN4;SN8;SN10",
        "residual_symbol": "partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "retained_Gauss_surface_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "the enclosed mass may include unowned boundary or volume hair",
    },
    {
        "pg_id": "PG5_orbital_inverse_square_readout",
        "stack_rungs": "SN0;SN9;SN10",
        "residual_symbol": "alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source",
        "affected_rows": "R1;R2;R4;R10;R11",
        "current_status": "retained_orbital_readout_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "the observed acceleration can contain non-inverse-square or source-dependent terms",
    },
    {
        "pg_id": "PG6_zero_mu_extra_and_source_residuals",
        "stack_rungs": "SN1;SN6;SN8;SN10",
        "residual_symbol": "mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector",
        "affected_rows": "R3;R4;R7;R8;R9;R10;R11",
        "current_status": "retained_mu_extra_source_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "extra source terms are physical unless theorem-zero or scored",
    },
    {
        "pg_id": "PG7_constant_universal_Geff",
        "stack_rungs": "SN5;SN7;SN10",
        "residual_symbol": "dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "retained_Geff_derivative_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "a nonconstant or nonuniversal G_eff cannot be hidden inside one measured GM",
    },
    {
        "pg_id": "PG8_no_derivative_hair",
        "stack_rungs": "SN0;SN4;SN7;SN10",
        "residual_symbol": "dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source",
        "affected_rows": "R0;R1;R2;R4;R8;R9;R10;R11",
        "current_status": "retained_derivative_hair_vector",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "time, radial, species, range, or frame derivatives are observable residuals",
    },
    {
        "pg_id": "PG9_second_order_source_stability",
        "stack_rungs": "SN1;SN11",
        "residual_symbol": "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector",
        "affected_rows": "R3;R4;R11",
        "current_status": "retained_second_order_source_residual",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "first-order Poisson cannot be promoted to local GR without beta/gamma stability",
    },
    {
        "pg_id": "PG10_retained_residual_fallback",
        "stack_rungs": "SN0-SN11",
        "residual_symbol": "dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;mu_extra/(GM);delta_beta_source;c_nonEH_operator_vector",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "valid_for_claim": "false",
        "why_it_blocks_Newton_or_GR": "unfilled residual rows mean no theorem credit",
    },
]


PROOF_CHAIN = [
    {
        "step": "1",
        "move": "Choose the observed local frame",
        "mathematical_content": "all matter readouts and the source variation use e_obs",
        "requires": "SN0",
        "failure_mode": "frame split residual",
    },
    {
        "step": "2",
        "move": "Linearize the retained local operator",
        "mathematical_content": "EH-only gives the Poisson operator; non-EH terms become R11 coefficients",
        "requires": "SN1",
        "failure_mode": "operator vector residual",
    },
    {
        "step": "3",
        "move": "Insert the nonrelativistic Hilbert source",
        "mathematical_content": "T_00 = rho_H c^2 and G_eff = kappa_eff c^4/(8 pi)",
        "requires": "SN3;SN5;SN7",
        "failure_mode": "source-normalization or G_eff residual",
    },
    {
        "step": "4",
        "move": "Identify the Hamiltonian charge with the source mass",
        "mathematical_content": "B_xi/G_eff = M_eff[Pi_M J_H]",
        "requires": "SN2;SN3;SN4",
        "failure_mode": "charge-current split or M_eff drift",
    },
    {
        "step": "5",
        "move": "Kill extra monopole pieces",
        "mathematical_content": "mu_extra = 0 and source_residuals = 0",
        "requires": "SN6;SN10",
        "failure_mode": "boundary/bulk/domain/range/source hair",
    },
    {
        "step": "6",
        "move": "Integrate Poisson over a sphere",
        "mathematical_content": "surface_integral grad Phi dot dS = 4 pi G_eff M_eff",
        "requires": "SN8",
        "failure_mode": "Gauss surface residual",
    },
    {
        "step": "7",
        "move": "Read the slow-particle acceleration",
        "mathematical_content": "a = -grad Phi = -G_eff M_eff rhat/r^2",
        "requires": "SN9",
        "failure_mode": "range/source/frame readout residual",
    },
    {
        "step": "8",
        "move": "Decide whether local GR is also claimed",
        "mathematical_content": "gamma - 1 = 0 and delta_beta_source = 0",
        "requires": "SN11",
        "failure_mode": "Newton-only or no-promotion branch",
    },
]


BLOCKERS = [
    {
        "rank": "1",
        "blocker": "charge-current equality",
        "dominant_stack_rungs": "SN2;SN3;SN4",
        "dominant_pg_rows": "PG0;PG1;PG4",
        "why_it_matters": "without this, Hamiltonian charge is not measured source mass",
        "best_next_action": "derive B_xi/G_eff = M_eff[Pi_M J_H] or fill dln_Meff_dt/mu_extra residuals",
    },
    {
        "rank": "2",
        "blocker": "zero mu_extra and derivative hair",
        "dominant_stack_rungs": "SN6;SN10",
        "dominant_pg_rows": "PG6;PG8",
        "why_it_matters": "hidden boundary, radial, range, species, or time terms invalidate constant GM absorption",
        "best_next_action": "derive theorem-zero for mu_extra and derivative rows or put numbers into the PG input template",
    },
    {
        "rank": "3",
        "blocker": "EH-only or complete R11 operator vector",
        "dominant_stack_rungs": "SN1;SN5",
        "dominant_pg_rows": "PG3;PG9",
        "why_it_matters": "the Poisson coefficient and beta/gamma order depend on operator purity",
        "best_next_action": "derive EH-only exterior or fill c_nonEH_operator_vector",
    },
    {
        "rank": "4",
        "blocker": "constant universal Geff",
        "dominant_stack_rungs": "SN7;SN10",
        "dominant_pg_rows": "PG7;PG8",
        "why_it_matters": "one Newton constant is legal only after time/range/species/frame derivatives vanish",
        "best_next_action": "derive global coupling superselection or score Gdot/source/fifth-force residuals",
    },
    {
        "rank": "5",
        "blocker": "second-order PPN source stability",
        "dominant_stack_rungs": "SN11",
        "dominant_pg_rows": "PG9",
        "why_it_matters": "Newton first order is not local GR unless beta/gamma/source normalization survive",
        "best_next_action": "perform second-order weak-field source/operator calculation after first-order rows are filled",
    },
]


def utc_now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": item["path"],
            "exists": str(exists(item["path"])),
            "role": item["role"],
        }
        for item in SOURCE_DOCS
    ]


def gate_rows(source_paths_missing: int) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
        },
        {
            "gate": "stack_csv_written",
            "status": "pass",
            "evidence": str(STACK_PATH),
        },
        {
            "gate": "Newton_stack_rungs",
            "status": "pass" if len(NEWTON_STACK) == 12 else "fail",
            "evidence": f"{len(NEWTON_STACK)} rungs written; SN0-SN11 expected",
        },
        {
            "gate": "PG_bindings_cover_PG0_to_PG10",
            "status": "pass" if len(PG_BINDINGS) == 11 else "fail",
            "evidence": f"{len(PG_BINDINGS)} PG residual bindings written",
        },
        {
            "gate": "conditional_theorem_written",
            "status": "pass",
            "evidence": "source-normalized Newton theorem statement written as conditional theorem",
        },
        {
            "gate": "all_current_claim_flags_blocked",
            "status": "pass",
            "evidence": "no stack rung grants current Newton or local-GR claim credit",
        },
        {
            "gate": "residual_fallback_visible",
            "status": "pass",
            "evidence": "failed rungs bind to P8/R11 PG residual components",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "SN3/SN4/SN6/SN8/SN10 remain not parent-derived",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "conditional theorem stack only; no theorem-zero or filled residual certificate",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "SN11 second-order PPN source stability not derived",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def theorem_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "finite Newton branch theorem target",
            "status": "pass",
            "evidence": "SN0-SN11 theorem stack written",
        },
        {
            "claim": "PG failure rows bound to residuals",
            "status": "pass",
            "evidence": "PG0-PG10 mapped into stack rungs and P8/R11 residual symbols",
        },
        {
            "claim": "measured GM parent-derived",
            "status": "fail",
            "evidence": "charge-current equality, Gauss calibration, mu_extra=0, derivative hair, and constant Geff remain open",
        },
        {
            "claim": "Newtonian limit promoted",
            "status": "fail",
            "evidence": "no current rung has valid theorem credit for the full branch",
        },
        {
            "claim": "local GR/PPN promoted",
            "status": "fail",
            "evidence": "SN11 beta/gamma/source stability remains not derived",
        },
    ]


def render_doc(timestamp: str, run_dir: Path, source_paths_missing: int) -> str:
    source_rows = source_register()
    gates = gate_rows(source_paths_missing)
    theorem_status = theorem_status_rows()
    next_queue = [
        {
            "rank": "1",
            "target": "461-PG-residual-input-derive-or-fill-gate.md",
            "why_next": "the theorem stack is only useful once the active PG residual inputs are either derived-zero or filled with real residual evidence",
        },
        {
            "rank": "2",
            "target": "second-order PPN source stability attempt",
            "why_next": "SN11 is the required bridge from Newton/Poisson to local GR",
        },
        {
            "rank": "3",
            "target": "EH-only parent action or R11 coefficient vector",
            "why_next": "operator purity controls both Poisson coefficient and PPN promotion",
        },
    ]

    return f"""# 460 - Source-Normalized Newton Branch Theorem Stack

Private GR/Newton reduction checkpoint. This is not a public Newtonian-limit, measured-GM, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 459 mapped the failed Poisson/Gauss conditions into explicit P8/R11 residual rows. This checkpoint assembles the finite theorem stack for a source-normalized Newton branch.

The question is precise:

```text
What exact identities must a parent MTS action satisfy before the branch is allowed to say it derives Newton?
```

The answer is also precise: SN0-SN10 are required for first-order measured-GM Newton. SN11 is required before any local-GR/PPN promotion.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalized_Newton_branch_theorem_stack.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Stack CSV | `{STACK_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["source_file", "exists", "role"])}

## 4. Conditional Theorem Statement

{md_table(THEOREM_STATEMENT, ["claim", "statement", "math_form", "current_status"])}

## 5. Newton Stack

The stack CSV has been written to `{STACK_PATH}`.

{md_table(NEWTON_STACK, STACK_COLUMNS)}

## 6. Proof Chain

{md_table(PROOF_CHAIN, ["step", "move", "mathematical_content", "requires", "failure_mode"])}

## 7. PG Residual Bindings

{md_table(PG_BINDINGS, PG_BINDING_COLUMNS)}

## 8. Current Blocker Ranking

{md_table(BLOCKERS, BLOCKER_COLUMNS)}

## 9. What Would Count as a Newton Pass

To promote the first-order Newton branch, the corpus needs one of these for every SN0-SN10 rung:

```text
parent-derived identity,
derived-zero residual theorem,
or valid numeric/source residual evidence with the effective row below its lock.
```

The current corpus does not have that certificate. The branch is therefore a theorem target and residual map, not a Newton claim.

## 10. What Would Count as a Local-GR Pass

Local GR needs the Newton certificate plus SN11:

```text
gamma - 1 = 0,
delta_beta_source = 0,
and c_nonEH_operator_vector = 0
```

after measured-GM normalization in the same observed frame. A Poisson/Gauss success alone would be first order only.

## 11. Gate Results

{md_table(gates, ["gate", "status", "evidence"])}

## 12. Theorem Status

{md_table(theorem_status, ["claim", "status", "evidence"])}

## 13. Decision

The Newton branch is now in the right mathematical shape: not a vibe, not a loose analogy, and not a hidden calibration trick. It is a finite stack. If SN0-SN10 are derived or residual-scored to zero, MTS gets a legal first-order Newton reduction:

```text
nabla^2 Phi = 4 pi G0 rho_H
surface_integral grad Phi dot dS = 4 pi G0 M_H
a = -grad Phi = -G0 M_H rhat/r^2
mu_obs = G0 M_H
```

But the current state is not there yet. The hardest blockers are charge-current equality, zero `mu_extra`, derivative-hair silence, constant universal `G_eff`, and second-order PPN source stability.

Practical read: this is actually good news, because the route is no longer mushy. We know exactly what has to be proved, and exactly what row gets punched if it is not proved. Right now the branch is conditional theorem architecture, not a pass. The next useful move is to attack the PG residual input rows directly: derive them, fill them, or keep them as no-claim residuals.

## 14. Next Queue

{md_table(next_queue, ["rank", "target", "why_next"])}
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_paths_missing = sum(1 for item in SOURCE_DOCS if not exists(item["path"]))
    missing_sources = [item["path"] for item in SOURCE_DOCS if not exists(item["path"])]

    write_csv(ROOT / STACK_PATH, NEWTON_STACK, STACK_COLUMNS)
    write_csv(results_dir / "Newton_branch_stack.csv", NEWTON_STACK, STACK_COLUMNS)
    write_csv(results_dir / "PG_residual_bindings.csv", PG_BINDINGS, PG_BINDING_COLUMNS)
    write_csv(results_dir / "current_blockers.csv", BLOCKERS, BLOCKER_COLUMNS)

    doc_text = render_doc(timestamp, run_dir, source_paths_missing)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    stack_rows = read_csv_count(ROOT / STACK_PATH)
    pg_binding_rows = read_csv_count(results_dir / "PG_residual_bindings.csv")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": source_paths_missing,
        "missing_sources": missing_sources,
        "Newton_stack_rungs": stack_rows,
        "PG_residual_bindings": pg_binding_rows,
        "conditional_theorem_written": True,
        "residual_fallback_visible": True,
        "all_current_claim_flags_blocked": True,
        "measured_GM_parent_derived": False,
        "Newton_branch_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=utc_now_tag())
    args = parser.parse_args()
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
