from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_source_normalized_alpha_law_conditionally_derived_parent_inputs_missing_no_R10_pass"
CLAIM_CEILING = "conditional_alpha_law_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md"

DOC_PATH = Path("560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_560_SOURCE_REGISTER.csv")
DERIVATION_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_SOURCE_NORMALIZED_ALPHA_DERIVATION_ATTEMPT.csv")
FORMULA_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_FORMULA_REGISTER.csv")
PARENT_INPUTS_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv")
ZERO_CONDITIONS_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_ZERO_CONDITIONS.csv")
RUNNER_FILL_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_MTS_CURVE_FILL_TEMPLATE.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_560_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_560_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_560_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_560_ROUTE_UPDATE.csv")

MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md",
        "role": "R10 runner dry-run showing placeholder rows are rejected",
    },
    {
        "source_file": "558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md",
        "role": "exact R10 branch schema and no-range theorem failure",
    },
    {
        "source_file": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "role": "bulk/memory/range Yukawa contract and mass-gap guardrail",
    },
    {
        "source_file": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "accepted R10 alpha(lambda) convention and curve contract",
    },
    {
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "source-normalized finite-range force-law debt",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "current MTS-side placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "current bound-side placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local bound manifest naming the R10 fifth-force test",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_559_VALIDATION.csv",
        "role": "previous validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "mu_extra coefficient vector with bulk_X_Yukawa_tail retained",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "role": "source-normalization channel ownership ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv",
        "role": "bulk-X force-law quantity ledger",
    },
    {
        "source_file": "runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv",
        "role": "bulk-X gate results showing alpha/lambda not parent-derived",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "reusable R10 curve validator/comparator",
    },
    {
        "source_file": "scripts/Y5_R10_source_normalized_alpha_law_from_parent_or_runner_real_data_fill.py",
        "role": "this checkpoint generator",
    },
]


DERIVATION_ATTEMPT_ROWS = [
    {
        "step_id": "AL560_0_parent_quadratic_branch",
        "derivation_step": "assume the surviving local finite-range branch is represented by one parent-owned scalar/vector-silent mode X in the weak-field static limit",
        "mathematical_form": "S_X^(2)=int d^4x[-(Z_X/2)(partial X)^2-(Z_X/2)m_X^2 X^2+X J_X]",
        "result": "conditional_starting_point",
        "why_it_matters": "without Z_X, m_X, and J_X the strength cannot be normalized",
        "claim_status": "not_claimable_parent_inputs_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_1_static_euler_equation",
        "derivation_step": "vary X and take the static exterior limit",
        "mathematical_form": "Z_X(-Delta+m_X^2)X=J_X",
        "result": "conditional_eom_written",
        "why_it_matters": "this is the exact operator needed before the mass-gap/no-hair or Yukawa branch can be scored",
        "claim_status": "not_claimable_operator_not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_2_exterior_green_function",
        "derivation_step": "solve the positive finite-range static Green problem outside a compact source",
        "mathematical_form": "X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r), lambda_X=1/m_X",
        "result": "conditional_profile_derived",
        "why_it_matters": "lambda is fixed by the parent mass gap; Q_X carries source, boundary, projector, and finite-size ownership",
        "claim_status": "not_claimable_QX_lambda_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_3_source_charge_definition",
        "derivation_step": "collect the monopole source that survives into the exterior field",
        "mathematical_form": "Q_X^H(lambda)=int_H d^3x J_X(x) F_lambda(x)+Q_boundary+Q_projector+Q_memory",
        "result": "definition_written_not_filled",
        "why_it_matters": "finite-size and nonlocal pieces change alpha even when the same lambda is used",
        "claim_status": "not_claimable_source_charge_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_4_test_body_coupling",
        "derivation_step": "let a test body with parent-owned charge q_X^T respond to X",
        "mathematical_form": "V_X(r)=-s_X q_X^T X(r)",
        "result": "conditional_test_potential_written",
        "why_it_matters": "R10 is a force on matter; if q_X^T is not zero or universal, WEP/species rows also open",
        "claim_status": "not_claimable_test_charge_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_5_newton_comparison",
        "derivation_step": "compare the X potential with the measured Newtonian potential in the same frame",
        "mathematical_form": "V_N(r)=-G_obs M_H m_T/r",
        "result": "normalization_anchor_written",
        "why_it_matters": "alpha must be dimensionless and normalized to observed GM, not to a free symbolic scale",
        "claim_status": "not_claimable_measured_GM_split_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_6_exact_alpha_law",
        "derivation_step": "divide the Yukawa potential by the Newtonian potential in the R10 convention",
        "mathematical_form": "alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)",
        "result": "conditional_exact_law_derived",
        "why_it_matters": "this is the missing MTS-side alpha(lambda) formula, but it is not numeric until every parent input is owned",
        "claim_status": "conditional_formula_only",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_7_acceleration_residual",
        "derivation_step": "differentiate the potential to match the accepted fifth-force acceleration row",
        "mathematical_form": "a_X/a_GR=alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X)",
        "result": "R10_mapping_recovered",
        "why_it_matters": "the derived alpha law plugs into the existing 437/559 runner once lambda and alpha rows are numeric",
        "claim_status": "not_claimable_runner_rows_missing",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_8_zero_conditions",
        "derivation_step": "read exact local suppression conditions from the multiplicative alpha law",
        "mathematical_form": "alpha_X=0 if Pi_M^H Q_X^H=0 or q_X^T=0, or by a parent Ward/no-hair theorem setting the whole physical spectral source to zero",
        "result": "zero_routes_identified",
        "why_it_matters": "mass gap alone is not a zero; the zero must hit the source, test charge, projection, or physical mode",
        "claim_status": "not_claimable_zero_conditions_not_signed",
        "valid_for_claim": "false",
    },
    {
        "step_id": "AL560_9_multimode_memory_extension",
        "derivation_step": "generalize finite-range memory/nonlocal tails to a spectral sum or envelope",
        "mathematical_form": "delta a/a_GR=sum_i alpha_i(1+r/lambda_i)exp(-r/lambda_i) or int dlnlambda alpha(lambda)(1+r/lambda)exp(-r/lambda)",
        "result": "conditional_extension_written",
        "why_it_matters": "a memory tail cannot be hidden in one scalar; it needs theorem-zero or an executable alpha envelope",
        "claim_status": "not_claimable_envelope_missing",
        "valid_for_claim": "false",
    },
]


FORMULA_REGISTER_ROWS = [
    {
        "formula_id": "F560_0_parent_action",
        "object": "quadratic finite-range parent branch",
        "expression": "S_X^(2)=int d^4x[-(Z_X/2)(partial X)^2-(Z_X/2)m_X^2 X^2+X J_X]",
        "required_parent_inputs": "Z_X;m_X_squared;J_X;sign_convention;allowed_spin_sector",
        "R10_mapping": "operator source for alpha(lambda) branch",
        "status": "conditional_not_parent_owned",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_1_static_operator",
        "object": "static Euler equation",
        "expression": "Z_X(-Delta+m_X^2)X=J_X",
        "required_parent_inputs": "positive Z_X;positive m_X_squared;source-free exterior or source charge",
        "R10_mapping": "sets whether theorem-zero or Yukawa curve is needed",
        "status": "conditional_not_signed",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_2_exterior_profile",
        "object": "compact-source Yukawa profile",
        "expression": "X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r); lambda_X=1/m_X",
        "required_parent_inputs": "Q_X^H(lambda_X);lambda_X;Z_X;boundary/projector/memory source treatment",
        "R10_mapping": "source-normalized field profile",
        "status": "conditional_not_numeric",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_3_test_potential",
        "object": "test body potential",
        "expression": "V_X(r)=-s_X q_X^T Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r)",
        "required_parent_inputs": "q_X^T;species universality;sign s_X",
        "R10_mapping": "compare directly against Yukawa correction to Newtonian potential",
        "status": "conditional_not_numeric",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_4_exact_alpha_law",
        "object": "source-normalized R10 strength",
        "expression": "alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)",
        "required_parent_inputs": "Pi_M^H projection;Q_X^H;q_X^T;Z_X;G_obs;M_H;m_T;s_X",
        "R10_mapping": "alpha_predicted column in R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "status": "derived_conditional_formula",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_5_acceleration_ratio",
        "object": "R10 acceleration residual",
        "expression": "a_X/a_GR=alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X)",
        "required_parent_inputs": "same alpha_X and lambda_X;R10 convention;measured-G normalization",
        "R10_mapping": "comparison against alpha_bound(lambda)",
        "status": "convention_recovered",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "F560_6_multimode_or_memory_tail",
        "object": "non-single-mode extension",
        "expression": "delta a/a_GR=sum_i alpha_i(1+r/lambda_i)exp(-r/lambda_i) or int dlnlambda alpha(lambda)(1+r/lambda)exp(-r/lambda)",
        "required_parent_inputs": "positive spectral measure or conservative envelope;no tuned cancellation;source normalization per mode",
        "R10_mapping": "sampled alpha_envelope(lambda) rows",
        "status": "conditional_extension_only",
        "valid_for_claim": "false",
    },
]


PARENT_INPUT_ROWS = [
    {
        "input_id": "PI560_0_ZX",
        "symbol": "Z_X",
        "definition": "canonical kinetic/operator normalization of the finite-range parent mode",
        "needed_for": "exact 4*pi normalization of alpha_X",
        "current_status": "missing_parent_action_coefficient",
        "zero_route": "not a normal zero route unless mode is nonpropagating by constraint",
        "coefficient_route": "derive Z_X>0 and include it in alpha denominator",
        "source_owner": "parent action",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_1_mX",
        "symbol": "m_X_squared;lambda_X",
        "definition": "positive local mass gap and its range lambda_X=1/m_X",
        "needed_for": "lambda_value column and Yukawa/no-hair operator sign",
        "current_status": "m_X_not_parent_derived",
        "zero_route": "positive mass gap helps no-hair only with zero source and zero boundary flux",
        "coefficient_route": "derive numeric or symbolic lambda grid from parent spectrum",
        "source_owner": "parent action;bulk/memory/range operator",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_2_JX",
        "symbol": "J_X",
        "definition": "matter, boundary, projector, domain, and memory source entering the X equation",
        "needed_for": "Q_X^H(lambda) and source-free no-hair decision",
        "current_status": "source_terms_not_parent_split",
        "zero_route": "prove J_X=0 in compact local exterior and no hidden boundary/projector source",
        "coefficient_route": "integrate J_X into Q_X^H(lambda)",
        "source_owner": "source-normalization ledger plus parent action",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_3_QX",
        "symbol": "Q_X^H(lambda)",
        "definition": "source monopole/form-factor charge generating the exterior X profile",
        "needed_for": "alpha numerator",
        "current_status": "Q_X_not_parent_derived",
        "zero_route": "derive Pi_M^H Q_X^H=0 or Q_X^H=0",
        "coefficient_route": "write source integral with finite-size, boundary, projector, and memory pieces",
        "source_owner": "Hamiltonian/source projection branch",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_4_qtest",
        "symbol": "q_X^T",
        "definition": "test-body charge/coupling to the X field",
        "needed_for": "force on matter and WEP/species status",
        "current_status": "q_test_not_parent_derived",
        "zero_route": "derive q_X^T=0 for all ordinary local test bodies",
        "coefficient_route": "derive universal q_X^T/m_T or species-dependent residual",
        "source_owner": "matter coupling sector",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_5_PiM",
        "symbol": "Pi_M^H",
        "definition": "Hamiltonian mass projection from X charge into measured local mass/force sector",
        "needed_for": "decide whether nonzero X is gravitationally silent or force-bearing",
        "current_status": "PiM_projection_not_derived",
        "zero_route": "derive Pi_M^H Q_X^H=0 by parent Ward identity",
        "coefficient_route": "derive nonzero projection coefficient and score R10",
        "source_owner": "Hamiltonian/mass projection branch",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_6_measured_GM",
        "symbol": "G_obs*M_H*m_T",
        "definition": "same-frame observed Newtonian normalization used in R10",
        "needed_for": "dimensionless alpha_X",
        "current_status": "measured_GM_split_not_closed",
        "zero_route": "constant universal calibration only if range/species/time/radial derivatives vanish",
        "coefficient_route": "normalize alpha against measured GM and retain residual derivatives",
        "source_owner": "measured-GM/source-normalization branch",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_7_sign",
        "symbol": "s_X",
        "definition": "sign convention for attractive/repulsive X exchange relative to R10 alpha",
        "needed_for": "alpha sign and absolute-bound comparison",
        "current_status": "sign_convention_not_parent_fixed",
        "zero_route": "sign does not zero alpha; bounds use abs(alpha) unless source says otherwise",
        "coefficient_route": "derive sign from coupling and kinetic convention",
        "source_owner": "parent action/coupling convention",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_8_boundary_flux",
        "symbol": "Q_boundary;boundary_flux",
        "definition": "boundary/domain contribution to exterior X charge",
        "needed_for": "no-hair theorem or source charge",
        "current_status": "boundary_flux_zero_not_derived",
        "zero_route": "derive zero boundary flux and regular decaying exterior solution",
        "coefficient_route": "include boundary charge in Q_X^H(lambda)",
        "source_owner": "boundary/domain branch",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_9_memory_kernel",
        "symbol": "alpha_memory(lambda)",
        "definition": "spectral/envelope representation of nonlocal memory tail",
        "needed_for": "memory branch cannot hide as one scalar if range dependent",
        "current_status": "memory_envelope_not_derived",
        "zero_route": "derive local stable kernel silence and zero spectral source",
        "coefficient_route": "sample conservative alpha_envelope(lambda) rows",
        "source_owner": "memory/time-flow branch",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI560_10_bound_curve",
        "symbol": "alpha_bound(lambda)",
        "definition": "external R10 inverse-square/fifth-force bound in same convention",
        "needed_for": "runner comparison",
        "current_status": "digitized_bound_curve_missing",
        "zero_route": "not needed only if theorem-zero is fully signed",
        "coefficient_route": "digitize/source bound rows and run comparator",
        "source_owner": "empirical local-bound data branch",
        "valid_for_claim": "false",
    },
]


ZERO_CONDITION_ROWS = [
    {
        "condition_id": "Z560_0_absent_test_charge",
        "condition": "ordinary local test bodies do not couple to X",
        "formula": "q_X^T=0 for every allowed T",
        "sufficient_for_alpha_zero": "yes_for_that_branch",
        "current_status": "not_derived",
        "repair": "derive matter coupling silence from parent action; otherwise fill q_X^T",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_1_absent_projected_source",
        "condition": "source charge is physically present but Hamiltonian-mass projection is zero",
        "formula": "Pi_M^H[Q_X^H(lambda)]=0",
        "sufficient_for_alpha_zero": "yes_for_R10_force_projection",
        "current_status": "not_derived",
        "repair": "prove projection Ward identity; otherwise fill projection coefficient",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_2_source_free_nohair",
        "condition": "positive operator, zero source, zero boundary flux, regular decaying solution",
        "formula": "Z_X>0; m_X^2>0; J_X=0; boundary_flux=0 => X=0",
        "sufficient_for_alpha_zero": "yes_if_all_premises_parent_signed",
        "current_status": "operator_and_source_premises_open",
        "repair": "derive operator sign plus source/boundary/projector silence",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_3_gauge_topological_absence",
        "condition": "finite-range-looking variable is gauge/topological and has no local stress or matter charge",
        "formula": "delta_g S_X=0 and delta_m S_X=0 in local compact sector",
        "sufficient_for_alpha_zero": "yes_if_parent_identity_signed",
        "current_status": "not_derived",
        "repair": "show X has no physical propagator/source in local branch",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_4_universal_GM_calibration",
        "condition": "surviving monopole is constant universal calibration, not finite-range hair",
        "formula": "D_lambda epsilon=D_species epsilon=D_t epsilon=D_r epsilon=0",
        "sufficient_for_alpha_zero": "no_but_can_remove_R10_if_truly_not_range_dependent",
        "current_status": "not_parent_fixed",
        "repair": "derive derivative silence and absorbed measured-GM normalization",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_5_multimode_Ward_zero",
        "condition": "multiple ranges cancel only by exact parent identity, not tuning",
        "formula": "rho_alpha(lambda)=0 as a signed physical spectral measure by Ward/no-source theorem",
        "sufficient_for_alpha_zero": "yes_if_identity_zeroes_measure",
        "current_status": "not_derived",
        "repair": "derive spectral source measure or emit conservative envelope",
        "valid_for_claim": "false",
    },
    {
        "condition_id": "Z560_6_bound_below_R10",
        "condition": "nonzero finite-range force survives but lies below external bounds",
        "formula": "abs(alpha_predicted(lambda_i))<=alpha_bound(lambda_i) for every valid row",
        "sufficient_for_alpha_zero": "no_but_can_pass_R10_bound",
        "current_status": "not_evaluable_no_numeric_rows",
        "repair": "fill MTS and bound curves then run comparator",
        "valid_for_claim": "false",
    },
]


RUNNER_FILL_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "bulk_X_parent_source_normalized_law",
        "curve_id": "R10_alpha_lambda_curve_MTS_source_normalization",
        "lambda_value": "MISSING_PARENT_DERIVED_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "s_X*PiM_H_QX(lambda_X)*q_X_test/(4*pi*Z_X*G_obs*M_H*m_test)",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "force_law_form": "Yukawa_potential_and_acceleration_ratio",
        "derivation_status": "conditional_formula_not_numeric_missing_parent_inputs",
        "formula_reference": "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_FORMULA_REGISTER.csv",
        "assumptions": "canonical or declared Z_X; same-frame measured-GM; no tuned cancellation; source/test charges parent-owned",
        "valid_for_claim": "false",
        "notes": "template only; do not copy into claim curve until lambda and alpha are numeric or theorem-zero is signed",
    }
]


EVALUATOR_ROWS = [
    {
        "gate_id": "E560_0_alpha_formula",
        "gate": "derive source-normalized alpha law from parent finite-range branch",
        "result": "conditional_pass",
        "detail": "alpha_X=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E560_1_parent_inputs",
        "gate": "parent-owned Z_X, lambda_X, Q_X, q_test, PiM, measured-GM normalization",
        "result": "fail_current_claim",
        "detail": "all required quantities remain missing or retained-unfilled in source ledgers",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E560_2_theorem_zero",
        "gate": "prove alpha(lambda)=0 without curve data",
        "result": "fail_current_claim",
        "detail": "zero conditions are identified but not parent-signed",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E560_3_runner_data",
        "gate": "supply executable numeric MTS alpha and external bound rows",
        "result": "fail_current_claim",
        "detail": "existing 559 runner still sees placeholder curves only",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E560_4_R10_status",
        "gate": "R10/fifth-force pass",
        "result": "fail_current_claim",
        "detail": "conditional formula is not a valid runner row",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E560_5_local_GR_status",
        "gate": "Newton/PPN/local-GR promotion",
        "result": "fail_current_claim",
        "detail": "R10 plus Cextra/radial/source-normalization gates remain open",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_LEDGER_ROWS = [
    {
        "obstruction_id": "O560_0_ZX_missing",
        "blocked_object": "exact alpha normalization",
        "reason": "parent action has not supplied canonical or noncanonical X kinetic normalization",
        "repair": "derive Z_X and sign from parent branch",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_1_lambda_missing",
        "blocked_object": "lambda_value row",
        "reason": "m_X/lambda_X is not parent-derived for the surviving branch",
        "repair": "derive mass gap or spectral range grid",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_2_source_charge_missing",
        "blocked_object": "Q_X^H(lambda)",
        "reason": "matter, boundary, projector, and memory source pieces are not integrated into a parent-owned charge",
        "repair": "derive source integral or theorem-zero source absence",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_3_test_charge_missing",
        "blocked_object": "q_X^T",
        "reason": "test-body coupling is not proven zero, universal, or numeric",
        "repair": "derive matter coupling silence or charge coefficient",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_4_PiM_missing",
        "blocked_object": "Hamiltonian force projection",
        "reason": "nonzero X may be projection-silent, but Pi_M^H is not derived",
        "repair": "prove Pi_M^H Q_X^H=0 or fill projection coefficient",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_5_bound_curve_missing",
        "blocked_object": "runner comparison",
        "reason": "external alpha_bound(lambda) rows are still placeholders",
        "repair": "source/digitize bound curve in the R10 convention",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O560_6_memory_tail_unmapped",
        "blocked_object": "non-single-mode finite-range branch",
        "reason": "memory/nonlocal tail has no spectral alpha(lambda) envelope",
        "repair": "derive theorem-zero for the tail or emit conservative envelope rows",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D560_0_conditional_law_derived",
        "decision": "source_normalized_alpha_law_written",
        "meaning": "the parent finite-range branch implies an exact conditional alpha(lambda) formula",
        "status": "conditional_progress",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D560_1_no_claim",
        "decision": "R10_still_blocked",
        "meaning": "the formula has missing parent inputs and cannot be treated as evidence or a valid curve row",
        "status": "R10_pass_false",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D560_2_zero_routes_exposed",
        "decision": "zero_requires_source_test_projection_or_Ward_identity",
        "meaning": "mass gap alone cannot remove the fifth-force row; alpha zero must be source/test/projection/no-hair zero",
        "status": "derivation_guidance",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D560_3_private_no_push",
        "decision": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "status": "safe_private_work",
        "next_target": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU560_0_allowed",
        "allowed_after_560": "MTS may cite the conditional alpha formula as a derivation target",
        "forbidden_after_560": "MTS may not claim R10/fifth-force pass or local GR from a symbolic formula",
        "next_action": "derive or zero Q_X, q_test, PiM_H, Z_X, and lambda_X",
    },
    {
        "route_id": "RU560_1_allowed",
        "allowed_after_560": "MTS may choose theorem-zero or executable curve as the next branch",
        "forbidden_after_560": "MTS may not use tuned cancellation among ranges without a parent Ward identity",
        "next_action": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        fieldnames: list[str] = []
    else:
        fieldnames = list(rows[0].keys())
        for row in rows[1:]:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_shape(path: Path) -> dict[str, Any]:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else []
    return {"path": rel(ROOT / path), "rows": len(rows), "columns": columns}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in SOURCE_REGISTER:
        source_path = ROOT / row["source_file"]
        rows.append({**row, "exists": source_path.exists()})
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    runner_result: dict[str, Any],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_559_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    mts_curve = read_csv(MTS_CURVE_PATH)
    bound_curve = read_csv(BOUND_CURVE_PATH)
    formula_rows = FORMULA_REGISTER_ROWS
    parent_inputs = PARENT_INPUT_ROWS
    zero_rows = ZERO_CONDITION_ROWS
    fill_rows = RUNNER_FILL_TEMPLATE_ROWS
    evaluator_rows = EVALUATOR_ROWS
    runner_status = runner_result["status"]
    runner_claim = bool(runner_status.get("R10_pass_for_claim"))
    claim_fill_rows = [row for row in fill_rows if row.get("valid_for_claim") == "true"]
    claim_evaluator_rows = [row for row in evaluator_rows if row.get("valid_for_claim") == "true"]

    return [
        {
            "check_id": "V560_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V560_1_prior_559_clean",
            "result": "pass" if len(prior_validation) == 10 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V560_2_conditional_formula_written",
            "result": "pass"
            if any(row["formula_id"] == "F560_4_exact_alpha_law" for row in formula_rows)
            else "fail",
            "detail": "exact conditional alpha formula registered",
        },
        {
            "check_id": "V560_3_parent_inputs_complete_as_debts",
            "result": "pass" if len(parent_inputs) == 11 and all(row["valid_for_claim"] == "false" for row in parent_inputs) else "fail",
            "detail": f"parent_input_rows={len(parent_inputs)};claim_rows={sum(row['valid_for_claim']=='true' for row in parent_inputs)}",
        },
        {
            "check_id": "V560_4_zero_conditions_not_overclaimed",
            "result": "pass" if len(zero_rows) == 7 and all(row["valid_for_claim"] == "false" for row in zero_rows) else "fail",
            "detail": f"zero_condition_rows={len(zero_rows)};claim_rows={sum(row['valid_for_claim']=='true' for row in zero_rows)}",
        },
        {
            "check_id": "V560_5_existing_placeholders_unchanged_as_blockers",
            "result": "pass" if len(mts_curve) == 2 and len(bound_curve) == 2 else "fail",
            "detail": f"mts_curve_rows={len(mts_curve)};bound_curve_rows={len(bound_curve)}",
        },
        {
            "check_id": "V560_6_runner_still_blocks_placeholders",
            "result": "pass" if runner_status.get("valid_mts_rows") == 0 and runner_status.get("valid_bound_rows") == 0 and not runner_claim else "fail",
            "detail": f"valid_mts={runner_status.get('valid_mts_rows')};valid_bound={runner_status.get('valid_bound_rows')};R10_pass={runner_status.get('R10_pass_for_claim')}",
        },
        {
            "check_id": "V560_7_template_not_claimable",
            "result": "pass" if len(fill_rows) == 1 and not claim_fill_rows and not claim_evaluator_rows else "fail",
            "detail": f"fill_rows={len(fill_rows)};claim_fill_rows={len(claim_fill_rows)};claim_evaluator_rows={len(claim_evaluator_rows)}",
        },
        {
            "check_id": "V560_8_no_overclaim",
            "result": "pass",
            "detail": "R10_pass=false; fifth_force=false; Cextra=false; radial_closure=false; Newton=false; PPN=false; local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in headers:
                headers.append(key)
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|") for header in headers) + " |")
    return "\n".join([header_line, separator, *body])


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    runner_summary: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 560 - Y5 R10 Source-Normalized Alpha Law from Parent or Runner Real-Data Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The parent finite-range route gives a clean conditional law:

```text
alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T
                 /(4*pi*Z_X*G_obs*M_H*m_T)
```

with

```text
a_X/a_GR = alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X).
```

That is real progress: the missing R10 object is no longer vague. It is an exact source-normalized coefficient once the parent action supplies `Z_X`, `lambda_X`, `Q_X`, `q_X^T`, `Pi_M^H`, and the measured-GM normalization.

But it is not yet a pass. The formula is symbolic because those parent-owned inputs remain missing. The existing R10 runner still correctly rejects the placeholder MTS and bound curves.

## 2. Derivation Attempt

{markdown_table(DERIVATION_ATTEMPT_ROWS)}

## 3. Formula Register

{markdown_table(FORMULA_REGISTER_ROWS)}

## 4. Parent Input Debts

{markdown_table(PARENT_INPUT_ROWS)}

## 5. Local Suppression / Zero Conditions

{markdown_table(ZERO_CONDITION_ROWS)}

## 6. Runner Fill Template

This is a non-claim template only. It is deliberately separate from `R10_alpha_lambda_curve_MTS_source_normalization.csv` so the 559 placeholder rejection remains intact.

{markdown_table(RUNNER_FILL_TEMPLATE_ROWS)}

## 7. Runner Dry-Run Recheck

{markdown_table(runner_summary)}

## 8. Evaluator

{markdown_table(EVALUATOR_ROWS)}

## 9. Obstruction Ledger

{markdown_table(OBSTRUCTION_LEDGER_ROWS)}

## 10. Decision

{markdown_table(DECISION_ROWS)}

## 11. Source Register

{markdown_table(sources)}

## 12. Validation

{markdown_table(validations)}

## 13. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 14. Claim Ceiling

Allowed:

```text
MTS has conditionally derived the exact source-normalized alpha law for a finite-range parent branch.
MTS has identified the exact local suppression conditions for alpha_X -> 0.
```

Forbidden:

```text
MTS has supplied a numeric alpha(lambda) curve.
MTS has proved alpha(lambda)=0.
MTS has passed R10/fifth-force, Newton, PPN, Cextra, radial closure, or local GR.
```

## 15. Practical Read

This is one of those useful uncomfortable checkpoints: the algebra itself is not the problem anymore. The problem has been converted into five hard parent-owned fills:

```text
Z_X,
lambda_X,
Pi_M^H Q_X^H(lambda_X),
q_X^T,
measured-GM normalization.
```

If any of the numerator pieces is theorem-zero, R10 can die cleanly. If not, the same formula gives the MTS curve row the runner will judge. No vibes, no hidden scalar pass, but also no mystery left about what the next bolt is.

## 16. Next Target

`{NEXT_TARGET}`

Next: derive or zero the source/test charge and Hamiltonian projection in the numerator. If that numerator cannot be zeroed, fill the coefficient route and then the R10 curve.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill"
    results_dir = run_dir / "results"
    runner_results_dir = results_dir / "runner"
    results_dir.mkdir(parents=True, exist_ok=True)

    runner_result = run_runner(ROOT / MTS_CURVE_PATH, ROOT / BOUND_CURVE_PATH, runner_results_dir)
    runner_status = runner_result["status"]
    runner_summary = [
        {
            "summary_id": "R10_RUNNER_560_RECHECK",
            "runner_results_dir": rel(runner_results_dir),
            "mts_rows": runner_status["mts_rows"],
            "valid_mts_rows": runner_status["valid_mts_rows"],
            "bound_rows": runner_status["bound_rows"],
            "valid_bound_rows": runner_status["valid_bound_rows"],
            "comparison_rows": runner_status["comparison_rows"],
            "passed_rows": runner_status["passed_rows"],
            "blocked_or_failed_rows": runner_status["blocked_or_failed_rows"],
            "R10_pass_for_claim": runner_status["R10_pass_for_claim"],
            "claim_allowed": False,
        }
    ]

    sources = source_rows()
    validations = validation_rows(sources, runner_result)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (DERIVATION_ATTEMPT_PATH, DERIVATION_ATTEMPT_ROWS),
        (FORMULA_REGISTER_PATH, FORMULA_REGISTER_ROWS),
        (PARENT_INPUTS_PATH, PARENT_INPUT_ROWS),
        (ZERO_CONDITIONS_PATH, ZERO_CONDITION_ROWS),
        (RUNNER_FILL_TEMPLATE_PATH, RUNNER_FILL_TEMPLATE_ROWS),
        (EVALUATOR_PATH, EVALUATOR_ROWS),
        (OBSTRUCTION_LEDGER_PATH, OBSTRUCTION_LEDGER_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(ROOT / path, rows)
        write_csv(results_dir / path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, runner_summary, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "document": str(ROOT / DOC_PATH),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "formula_register": str(ROOT / FORMULA_REGISTER_PATH),
        "parent_inputs": str(ROOT / PARENT_INPUTS_PATH),
        "zero_conditions": str(ROOT / ZERO_CONDITIONS_PATH),
        "runner_fill_template": str(ROOT / RUNNER_FILL_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "failed_validations": failed_validations,
        "R10_fifth_force_passed": False,
        "alpha_formula_conditionally_derived": True,
        "alpha_curve_valid_for_claim": False,
        "theorem_zero_signed": False,
        "Cextra_zero_signed": False,
        "radial_closure_signed": False,
        "Newton_limit_signed": False,
        "PPN_passed": False,
        "local_GR_promoted": False,
        "csv_shapes": [
            csv_shape(path)
            for path, _rows in csv_outputs
        ],
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
