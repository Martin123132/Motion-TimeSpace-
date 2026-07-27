from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_source_test_charge_PiM_zero_not_derived_numerator_coefficient_template_written"
CLAIM_CEILING = "R10_numerator_zero_attempt_or_coefficient_template_only_no_fifth_force_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md"

DOC_PATH = Path("561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_561_SOURCE_REGISTER.csv")
NUMERATOR_FACTOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_FACTOR_REGISTER.csv")
ZERO_PROOF_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_ZERO_PROOF_ATTEMPT.csv")
COEFFICIENT_VECTOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_COEFFICIENT_VECTOR.csv")
THEOREM_CERTIFICATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_ZERO_THEOREM_CERTIFICATE_TEMPLATE.csv")
ALPHA_FILL_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_ALPHA_FILL_TEMPLATE.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_561_EVALUATOR.csv")
OBSTRUCTION_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_561_OBSTRUCTION_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_561_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_561_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_561_ROUTE_UPDATE.csv")

MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md",
        "role": "conditional alpha law and numerator target",
    },
    {
        "source_file": "559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md",
        "role": "R10 runner placeholder rejection",
    },
    {
        "source_file": "557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md",
        "role": "bulk/memory/range Yukawa route and no mass-gap-only credit",
    },
    {
        "source_file": "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "role": "extra mass projection silence theorem attempt",
    },
    {
        "source_file": "553-Y5-Hamiltonian-PiM-repair-clause-test-or-bound-fill.md",
        "role": "Hamiltonian PiM repair obstruction ledger",
    },
    {
        "source_file": "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
        "role": "Hamiltonian PiM readout decision gate",
    },
    {
        "source_file": "447-no-species-source-charge-one-coframe-theorem-attempt.md",
        "role": "matter/test/source-charge silence attempt",
    },
    {
        "source_file": "446-source-owner-current-parent-action-contract.md",
        "role": "parent source-owner action term contract",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "PiM algebra and projection ownership contract",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "PiM flux closure Ward/topological contract",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "mu_extra source-normalization coefficient-vector fallback",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_FORMULA_REGISTER.csv",
        "role": "560 exact alpha law formula register",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
        "role": "560 parent input debts",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
        "role": "test/source charge silence contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "source-owner parent action terms",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "PiM parent symplectic projector algebra contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "PiM flux closure Ward/topological contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_560_VALIDATION.csv",
        "role": "previous validation gate",
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
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "reusable R10 curve comparator",
    },
    {
        "source_file": "scripts/Y5_R10_source_test_charge_and_PiM_projection_zero_or_coefficient_fill.py",
        "role": "this checkpoint generator",
    },
]


NUMERATOR_FACTOR_ROWS = [
    {
        "factor_id": "NF561_0_alpha_numerator_definition",
        "object": "R10 alpha numerator",
        "expression": "N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T",
        "meaning": "all local finite-range force strength not already in Z_X, G_obs, M_H, m_T, or sign",
        "zero_if": "Pi_M^H[Q_X^H]=0 or q_X^T=0",
        "coefficient_if_not_zero": "N_X(lambda) retained as source-test-projection coefficient",
        "status": "defined",
        "valid_for_claim": "false",
    },
    {
        "factor_id": "NF561_1_source_charge",
        "object": "projected source charge",
        "expression": "Q_X^H(lambda)=int_H d^3x J_X(x)F_lambda(x)+Q_boundary+Q_projector+Q_memory+Q_domain",
        "meaning": "compact-source monopole/form-factor that sources exterior X",
        "zero_if": "all source, boundary, projector, memory, and domain pieces vanish or are pure gauge/topological",
        "coefficient_if_not_zero": "Qhat_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H with units declared",
        "status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "factor_id": "NF561_2_test_charge",
        "object": "ordinary-matter test charge",
        "expression": "q_X^T=-delta S_T/dX in the local weak-field branch",
        "meaning": "how a test body responds to X exchange",
        "zero_if": "matter action has no X, no X-dependent constants, and no post-readout material marker coupling",
        "coefficient_if_not_zero": "chat_XT=q_X^T/m_T; species split Delta chat_XAB opens R1/WEP",
        "status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "factor_id": "NF561_3_Hamiltonian_projection",
        "object": "Pi_M^H projection",
        "expression": "Pi_M^H[Q_X^H]=ell_M(Pi_M^H Q_X^H)",
        "meaning": "whether the X charge lands in the measured Hamiltonian mass/force channel",
        "zero_if": "parent symplectic/Hamiltonian projector is orthogonal to X source including delta Pi_M and boundary terms",
        "coefficient_if_not_zero": "pi_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/Q_X^H(lambda) or direct projected charge",
        "status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "factor_id": "NF561_4_universal_nonzero_case",
        "object": "universal but nonzero numerator",
        "expression": "q_X^T/m_T=constant and Pi_M^H Q_X^H/M_H=constant_nonzero",
        "meaning": "WEP may survive but finite-range R10 still sees a Yukawa force",
        "zero_if": "not zero; only absorbable into GM if range, time, radius, and species derivatives vanish",
        "coefficient_if_not_zero": "score alpha(lambda); do not absorb finite-range hair into GM",
        "status": "guardrail_written",
        "valid_for_claim": "false",
    },
    {
        "factor_id": "NF561_5_memory_multimode_case",
        "object": "memory or multimode numerator",
        "expression": "N_X(lambda)->rho_N(lambda) or sum_i N_i delta(lambda-lambda_i)",
        "meaning": "nonlocal memory tail must be zero as a measure or bounded as an envelope",
        "zero_if": "rho_N(lambda)=0 by parent Ward/no-source theorem",
        "coefficient_if_not_zero": "alpha_envelope(lambda) sampled into R10 curve",
        "status": "not_parent_derived",
        "valid_for_claim": "false",
    },
]


ZERO_PROOF_ROWS = [
    {
        "test_id": "NZ561_0_matter_X_absence",
        "zero_target": "q_X^T=0",
        "attempted_derivation": "ordinary matter action is selector-blind and depends only on one observed coframe, not on X or material markers",
        "required_identity": "delta S_matter/dX=0; partial_A theta=0; no material/readout marker in active source",
        "evidence_status": "not_parent_derived",
        "failure_mode": "447/no-species-source contract leaves constant-sector universality, source normalization species-blindness, and bulk/boundary composition charge open",
        "fallback": "retain q_X^T/m_T coefficient and species split if nonuniversal",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_1_source_absence",
        "zero_target": "Q_X^H(lambda)=0",
        "attempted_derivation": "X is source-free in compact local exterior and its compact source monopole vanishes",
        "required_identity": "J_X=0 plus Q_boundary=Q_projector=Q_memory=Q_domain=0",
        "evidence_status": "not_parent_derived",
        "failure_mode": "446/557 leave source-owner decomposition, boundary/projector/memory/domain sources open",
        "fallback": "retain Q_X^H(lambda) source integral/form factor",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_2_projected_source_absence",
        "zero_target": "Pi_M^H[Q_X^H(lambda)]=0",
        "attempted_derivation": "X charge exists but is orthogonal to Hamiltonian mass projector",
        "required_identity": "Pi_M^H X_source=0 including delta Pi_M, boundary, and symplectic metric terms",
        "evidence_status": "not_parent_derived",
        "failure_mode": "454/455/553 leave projector algebra, flux closure, integrability, and reference-boundary terms open",
        "fallback": "retain projected source charge Pi_M^H[Q_X^H(lambda)]",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_3_Hamiltonian_charge_integrability",
        "zero_target": "Pi_M^H numerator is a legal Hamiltonian charge projection",
        "attempted_derivation": "define Pi_M^H by Hamiltonian charge map Q_tau before readout",
        "required_identity": "Q_tau integrable; fixed reference boundary; same observed frame; Poisson/Gauss readout",
        "evidence_status": "not_enough",
        "failure_mode": "540 says Pi_M^H fixes wrong-object naming but not source measure or readout",
        "fallback": "keep epsilon_HPiM_source_equality_abs and R10 numerator coefficient",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_4_no_cancellation",
        "zero_target": "N_X(lambda)=0 by cancellation among source/test/projection pieces",
        "attempted_derivation": "allow Q_boundary+Q_projector+Q_memory to cancel ordinary source",
        "required_identity": "single parent Ward identity zeros the full physical numerator measure",
        "evidence_status": "forbidden_without_identity",
        "failure_mode": "522 no-cancellation policy requires channelwise theorem-zero or individual bounds",
        "fallback": "use absolute channelwise coefficient vector",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_5_universal_nonzero_GM_absorption",
        "zero_target": "finite-range force removed as measured-GM calibration",
        "attempted_derivation": "nonzero universal numerator is treated as calibration rather than force",
        "required_identity": "D_lambda N=D_r N=D_t N=D_species N=0",
        "evidence_status": "not_satisfied",
        "failure_mode": "finite-range Yukawa factor gives lambda/r dependence unless theorem-zero or infinite-range constant branch is proved",
        "fallback": "score universal nonzero alpha(lambda) against R10",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NZ561_6_verdict",
        "zero_target": "R10 numerator",
        "attempted_derivation": "try all clean zero routes before coefficient fill",
        "required_identity": "q_X^T=0 or Pi_M^H Q_X^H=0 or parent Ward/no-hair spectral source zero",
        "evidence_status": "fail_current_claim",
        "failure_mode": "none of the required identities is parent-signed in the current corpus",
        "fallback": "write numerator coefficient vector and keep R10 blocked",
        "valid_for_claim": "false",
    },
]


COEFFICIENT_VECTOR_ROWS = [
    {
        "coefficient_id": "NC561_0_alpha_numerator",
        "symbol": "N_X(lambda)",
        "definition": "N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T",
        "units": "product_units_of_projected_source_charge_and_test_charge",
        "normalization": "alpha_X=s_X N_X/(4*pi*Z_X*G_obs*M_H*m_T)",
        "zero_condition": "N_X(lambda)=0 for every local R10 lambda by parent theorem",
        "required_input": "source/test/projection theorem-zero or numeric/source-backed coefficient",
        "mapped_rows": "R10;R1_if_species_dependent;R9_if_time_dependent;R4_if_radial_dependent;R11_if_operator_source",
        "current_status": "retained_unfilled",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_1_projected_source_charge",
        "symbol": "Qbar_XH(lambda)",
        "definition": "Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H",
        "units": "projected_X_charge_per_source_mass",
        "normalization": "N_X/(M_H*m_T)=Qbar_XH(lambda)*(q_X^T/m_T)",
        "zero_condition": "Pi_M^H[Q_X^H(lambda)]=0",
        "required_input": "source integral, boundary/projector/memory/domain split, and PiM projection",
        "mapped_rows": "R10;R4;R9;R11",
        "current_status": "missing_projected_source_charge",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_2_test_charge_ratio",
        "symbol": "qbar_XT",
        "definition": "qbar_XT=q_X^T/m_T",
        "units": "test_X_charge_per_test_mass",
        "normalization": "N_X/(M_H*m_T)=Qbar_XH(lambda)*qbar_XT",
        "zero_condition": "q_X^T=0 for all ordinary local test bodies",
        "required_input": "matter coupling variation and species universality proof",
        "mapped_rows": "R10;R1;R2",
        "current_status": "missing_test_charge_ratio",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_3_species_split",
        "symbol": "Delta_qbar_XAB",
        "definition": "Delta_qbar_XAB=qbar_XA-qbar_XB",
        "units": "test_X_charge_per_mass_difference",
        "normalization": "eta_source_AB branch if nonzero",
        "zero_condition": "selector-blind matter/source action gives Delta_qbar_XAB=0",
        "required_input": "no species/source charge theorem or WEP bound input",
        "mapped_rows": "R1;R10",
        "current_status": "retained_if_qbar_nonuniversal",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_4_projector_leak",
        "symbol": "epsilon_PiM_X(lambda)",
        "definition": "epsilon_PiM_X(lambda)=Pi_M^H[Q_X^H(lambda)]/Q_X^H(lambda) when Q_X is nonzero",
        "units": "dimensionless_projection_fraction",
        "normalization": "Qbar_XH=epsilon_PiM_X Q_X^H/M_H",
        "zero_condition": "Pi_M^H orthogonal to X source including delta Pi_M terms",
        "required_input": "parent symplectic projector algebra plus flux closure",
        "mapped_rows": "R10;R8;R11",
        "current_status": "missing_projector_leak_coefficient",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_5_boundary_memory_source",
        "symbol": "Q_X_boundary_memory(lambda)",
        "definition": "Q_boundary+Q_projector+Q_memory+Q_domain contributions to Q_X^H(lambda)",
        "units": "X_source_charge",
        "normalization": "included inside Q_X^H(lambda)",
        "zero_condition": "boundary/domain/memory no-hair or topological class-only zero-flux theorem",
        "required_input": "channelwise source charge or theorem-zero rows",
        "mapped_rows": "R7;R8;R9;R10;R11",
        "current_status": "retained_channel_source",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_6_range_derivative",
        "symbol": "D_lambda_N_X",
        "definition": "range dependence of the numerator or spectral measure",
        "units": "numerator_per_log_lambda",
        "normalization": "finite-range R10 cannot be absorbed into measured GM if D_lambda_N_X nonzero",
        "zero_condition": "D_lambda_N_X=0 and branch is constant universal calibration, or numerator zero",
        "required_input": "lambda grid/spectral measure or derivative theorem",
        "mapped_rows": "R10",
        "current_status": "missing_range_dependence",
        "valid_for_claim": "false",
    },
    {
        "coefficient_id": "NC561_7_alpha_prefactor_guard",
        "symbol": "K_X=s_X/(4*pi*Z_X*G_obs)",
        "definition": "remaining coupling prefactor after numerator mass normalization",
        "units": "inverse_product_units_needed_to_make_alpha_dimensionless",
        "normalization": "alpha_X=K_X Qbar_XH(lambda) qbar_XT",
        "zero_condition": "not a zero route unless parent removes X mode or coupling",
        "required_input": "Z_X, sign, G_obs same-frame normalization",
        "mapped_rows": "R10",
        "current_status": "deferred_to_562_ZX_lambda_gate",
        "valid_for_claim": "false",
    },
]


THEOREM_CERTIFICATE_ROWS = [
    {
        "certificate_id": "NT561_0_source_test_projection_zero_certificate",
        "required_clause": "one of q_X^T=0, Pi_M^H Q_X^H=0, or full physical spectral source zero is parent-derived",
        "mathematical_form": "forall lambda in local R10 range: N_X(lambda)=0",
        "required_sources": "parent action variation; matter coupling ledger; PiM projector algebra; boundary/memory/source split",
        "current_status": "template_unfilled",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "NT561_1_no_species_or_marker_charge",
        "required_clause": "ordinary test/source matter has no X or material-marker charge",
        "mathematical_form": "delta S_matter/dX=0 and partial_A mu_obs=0",
        "required_sources": "selector-blind matter/source theorem",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "NT561_2_projected_source_orthogonality",
        "required_clause": "Pi_M^H is orthogonal to the X source including variation and boundary pieces",
        "mathematical_form": "ell_M(Pi_M^H Q_X^H)=0",
        "required_sources": "parent symplectic projector metric; delta PiM stress; Hamiltonian charge integrability",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "NT561_3_no_cancellation",
        "required_clause": "zero is channelwise or Ward-owned, not fitted cancellation",
        "mathematical_form": "rho_N(lambda)=0 as a parent identity, not sum_i rho_i approximately 0",
        "required_sources": "Ward/source-owner identity",
        "current_status": "policy_only",
        "valid_for_claim": "false",
    },
]


ALPHA_FILL_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "R10_numerator_coefficient_branch",
        "curve_id": "R10_alpha_lambda_curve_MTS_source_normalization",
        "lambda_value": "MISSING_PARENT_DERIVED_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "K_X*Qbar_XH(lambda_X)*qbar_XT",
        "alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
        "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "force_law_form": "Yukawa_potential_and_acceleration_ratio",
        "derivation_status": "numerator_coefficient_template_not_numeric",
        "formula_reference": "561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_COEFFICIENT_VECTOR.csv",
        "assumptions": "same-frame measured-GM; channelwise no-cancellation; source/test/PiM parent-owned before claim",
        "valid_for_claim": "false",
        "notes": "do not insert into the claim curve until Qbar_XH, qbar_XT, K_X, lambda, and alpha_bound are numeric/source-backed or theorem-zero is signed",
    }
]


EVALUATOR_ROWS = [
    {
        "gate_id": "E561_0_numerator_factorization",
        "gate": "factor R10 alpha numerator",
        "result": "pass_contract",
        "detail": "N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_1_test_charge_zero",
        "gate": "derive q_X^T=0",
        "result": "fail_current_claim",
        "detail": "matter/source selector-blindness and no bulk/boundary composition charge are not parent-derived",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_2_projected_source_zero",
        "gate": "derive Pi_M^H[Q_X^H]=0",
        "result": "fail_current_claim",
        "detail": "PiM algebra/flux closure/integrability/reference terms remain open",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_3_source_absence",
        "gate": "derive Q_X^H(lambda)=0",
        "result": "fail_current_claim",
        "detail": "source-owner decomposition and boundary/projector/memory/domain sources remain open",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_4_coefficient_fallback",
        "gate": "write numerator coefficient vector",
        "result": "pass_template",
        "detail": "N_X, Qbar_XH, qbar_XT, species split, projector leak, boundary/memory source, range derivative, and K_X rows written",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_5_R10_status",
        "gate": "R10/fifth-force pass",
        "result": "fail_current_claim",
        "detail": "numerator is not zeroed or numeric; runner still blocks placeholder rows",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "E561_6_local_GR_status",
        "gate": "Newton/PPN/local-GR promotion",
        "result": "fail_current_claim",
        "detail": "R10 numerator plus Z_X/lambda/bound curve and remaining Cextra/radial gates remain open",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_LEDGER_ROWS = [
    {
        "obstruction_id": "O561_0_matter_coupling_open",
        "blocked_object": "q_X^T zero theorem",
        "reason": "ordinary matter has not been proven independent of X/source markers in the active parent action",
        "repair": "derive selector-blind matter/source theorem or fill qbar_XT",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O561_1_source_integral_open",
        "blocked_object": "Q_X^H(lambda)",
        "reason": "J_X plus boundary/projector/memory/domain charges are not integrated or zeroed",
        "repair": "derive source-free no-hair or source integral/form-factor row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O561_2_PiM_orthogonality_open",
        "blocked_object": "Pi_M^H[Q_X^H]=0",
        "reason": "projector algebra is conditional and delta PiM/source flux/reference terms remain active",
        "repair": "derive parent symplectic projector orthogonality or fill epsilon_PiM_X",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O561_3_Hamiltonian_readout_open",
        "blocked_object": "measured mass-channel readout",
        "reason": "Hamiltonian charge map does not yet prove same-frame source measure or Poisson/Gauss orbital readout",
        "repair": "derive source-measure/readout theorem after numerator closure",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O561_4_no_cancellation_policy",
        "blocked_object": "claiming numerator zero by mixed channels",
        "reason": "channel cancellation without a parent Ward identity is forbidden",
        "repair": "show Ward-owned zero of full spectral numerator or bound every channel",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "O561_5_prefactor_and_range_deferred",
        "blocked_object": "numeric alpha(lambda)",
        "reason": "Z_X, sign, lambda_X, and external alpha_bound(lambda) are still missing",
        "repair": NEXT_TARGET,
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D561_0_numerator_factorized",
        "decision": "N_X_factorization_written",
        "meaning": "R10 numerator is exactly Pi_M^H[Q_X^H(lambda)] q_X^T",
        "status": "contract_progress",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D561_1_zero_not_derived",
        "decision": "source_test_projection_zero_failed_current_claim",
        "meaning": "no current parent proof sets q_X^T, Q_X^H, or Pi_M^H Q_X^H to zero",
        "status": "R10_retained",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D561_2_coefficient_vector_written",
        "decision": "numerator_coefficient_fallback_written",
        "meaning": "if zero proof fails, numerator must be filled as Qbar_XH, qbar_XT, projector leak, and range/source rows",
        "status": "template_only",
        "next_target": NEXT_TARGET,
    },
    {
        "decision_id": "D561_3_private_no_push",
        "decision": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "status": "safe_private_work",
        "next_target": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU561_0_allowed",
        "allowed_after_561": "MTS may use N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T as the exact R10 numerator gate",
        "forbidden_after_561": "MTS may not claim the numerator is zero or harmless without a parent theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "route_id": "RU561_1_allowed",
        "allowed_after_561": "MTS may fill qbar_XT, Qbar_XH, epsilon_PiM_X, and range-derivative rows as coefficients",
        "forbidden_after_561": "MTS may not absorb finite-range universal nonzero alpha into measured GM unless all range/radial/time/species derivatives vanish",
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
    fieldnames: list[str] = list(rows[0].keys()) if rows else []
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


def count_claim_rows(row_groups: list[list[dict[str, Any]]]) -> int:
    return sum(1 for rows in row_groups for row in rows if str(row.get("valid_for_claim", "")).lower() == "true")


def validation_rows(
    sources: list[dict[str, Any]],
    runner_result: dict[str, Any],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_validation = read_csv(Path("source-intake/mts_residuals/P8_Y5_BRR545_560_VALIDATION.csv"))
    prior_fails = [row for row in prior_validation if row.get("result") == "fail"]
    mts_curve = read_csv(MTS_CURVE_PATH)
    bound_curve = read_csv(BOUND_CURVE_PATH)
    runner_status = runner_result["status"]
    claim_rows = count_claim_rows(
        [
            NUMERATOR_FACTOR_ROWS,
            ZERO_PROOF_ROWS,
            COEFFICIENT_VECTOR_ROWS,
            THEOREM_CERTIFICATE_ROWS,
            ALPHA_FILL_TEMPLATE_ROWS,
            EVALUATOR_ROWS,
            OBSTRUCTION_LEDGER_ROWS,
        ]
    )

    return [
        {
            "check_id": "V561_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V561_1_prior_560_clean",
            "result": "pass" if len(prior_validation) == 9 and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_validation)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V561_2_numerator_factorized",
            "result": "pass" if any(row["factor_id"] == "NF561_0_alpha_numerator_definition" for row in NUMERATOR_FACTOR_ROWS) else "fail",
            "detail": "N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T",
        },
        {
            "check_id": "V561_3_zero_attempt_rejected_without_parent_premises",
            "result": "pass" if len(ZERO_PROOF_ROWS) == 7 and all(row["valid_for_claim"] == "false" for row in ZERO_PROOF_ROWS) else "fail",
            "detail": f"zero_attempt_rows={len(ZERO_PROOF_ROWS)};claim_rows={sum(row['valid_for_claim']=='true' for row in ZERO_PROOF_ROWS)}",
        },
        {
            "check_id": "V561_4_coefficient_vector_written",
            "result": "pass" if len(COEFFICIENT_VECTOR_ROWS) == 8 and all(row["valid_for_claim"] == "false" for row in COEFFICIENT_VECTOR_ROWS) else "fail",
            "detail": f"coefficient_rows={len(COEFFICIENT_VECTOR_ROWS)};claim_rows={sum(row['valid_for_claim']=='true' for row in COEFFICIENT_VECTOR_ROWS)}",
        },
        {
            "check_id": "V561_5_existing_placeholders_unchanged_as_blockers",
            "result": "pass" if len(mts_curve) == 2 and len(bound_curve) == 2 else "fail",
            "detail": f"mts_curve_rows={len(mts_curve)};bound_curve_rows={len(bound_curve)}",
        },
        {
            "check_id": "V561_6_runner_still_blocks_placeholders",
            "result": "pass" if runner_status.get("valid_mts_rows") == 0 and runner_status.get("valid_bound_rows") == 0 and runner_status.get("R10_pass_for_claim") is False else "fail",
            "detail": f"valid_mts={runner_status.get('valid_mts_rows')};valid_bound={runner_status.get('valid_bound_rows')};R10_pass={runner_status.get('R10_pass_for_claim')}",
        },
        {
            "check_id": "V561_7_no_claim_rows",
            "result": "pass" if claim_rows == 0 else "fail",
            "detail": f"claim_rows={claim_rows}",
        },
        {
            "check_id": "V561_8_no_overclaim",
            "result": "pass",
            "detail": "numerator_zero=false; R10_pass=false; fifth_force=false; Cextra=false; Newton=false; PPN=false; local_GR=false",
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
    return f"""# 561 - Y5 R10 Source/Test Charge and PiM Projection Zero or Coefficient Fill

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The R10 numerator has now been isolated:

```text
N_X(lambda)=Pi_M^H[Q_X^H(lambda)] q_X^T
alpha_X(lambda)=s_X N_X(lambda)/(4*pi*Z_X*G_obs*M_H*m_T).
```

This is useful because the zero problem is sharp. The local finite-range force dies only if:

```text
q_X^T = 0,
or Pi_M^H[Q_X^H(lambda)] = 0,
or a parent Ward/no-hair theorem zeros the full physical source measure for every local lambda.
```

Current result: none of those zero routes is parent-signed in the corpus. So the numerator is not proved harmless. It is retained as an explicit coefficient vector feeding R10, WEP/source-charge rows if species dependent, and time/radial/source-normalization rows if it drifts.

## 2. Numerator Factor Register

{markdown_table(NUMERATOR_FACTOR_ROWS)}

## 3. Zero Proof Attempt

{markdown_table(ZERO_PROOF_ROWS)}

## 4. Coefficient Vector Fallback

{markdown_table(COEFFICIENT_VECTOR_ROWS)}

## 5. Theorem-Zero Certificate Template

{markdown_table(THEOREM_CERTIFICATE_ROWS)}

## 6. Alpha Fill Template

This is deliberately not written into the live R10 curve. It is the exact shape of the future row once `Qbar_XH`, `qbar_XT`, `K_X`, `lambda_X`, and `alpha_bound` are real or theorem-zero is signed.

{markdown_table(ALPHA_FILL_TEMPLATE_ROWS)}

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
MTS has isolated the exact R10 numerator N_X(lambda).
MTS has tested the clean zero routes and retained a coefficient fallback.
```

Forbidden:

```text
MTS has proved q_X^T=0.
MTS has proved Pi_M^H Q_X^H=0.
MTS has produced numeric alpha(lambda) rows.
MTS has passed R10/fifth-force, Newton, PPN, Cextra, radial closure, or local GR.
```

## 15. Practical Read

This is a good but slightly brutal gate. If the theory has the local-GR route, the numerator must be killed by a real parent identity, not by “it feels source-free.” If it cannot be killed, then the object to fit/bound is now explicit:

```text
alpha_X(lambda)=K_X Qbar_XH(lambda) qbar_XT.
```

That means the next work is not philosophical. It is: derive `Z_X`, `lambda_X`, the units of `K_X`, and then either theorem-zero the numerator or put real curve rows into the runner.

## 16. Next Target

`{NEXT_TARGET}`

Next: handle the prefactor/range side: `Z_X`, `lambda_X`, mass-gap sign, and the bound-curve data. If those cannot be derived, R10 remains an explicit retained local-bound branch.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill"
    results_dir = run_dir / "results"
    runner_results_dir = results_dir / "runner"
    results_dir.mkdir(parents=True, exist_ok=True)

    runner_result = run_runner(ROOT / MTS_CURVE_PATH, ROOT / BOUND_CURVE_PATH, runner_results_dir)
    runner_status = runner_result["status"]
    runner_summary = [
        {
            "summary_id": "R10_RUNNER_561_RECHECK",
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
        (NUMERATOR_FACTOR_PATH, NUMERATOR_FACTOR_ROWS),
        (ZERO_PROOF_ATTEMPT_PATH, ZERO_PROOF_ROWS),
        (COEFFICIENT_VECTOR_PATH, COEFFICIENT_VECTOR_ROWS),
        (THEOREM_CERTIFICATE_PATH, THEOREM_CERTIFICATE_ROWS),
        (ALPHA_FILL_TEMPLATE_PATH, ALPHA_FILL_TEMPLATE_ROWS),
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
        "numerator_factor_register": str(ROOT / NUMERATOR_FACTOR_PATH),
        "zero_proof_attempt": str(ROOT / ZERO_PROOF_ATTEMPT_PATH),
        "coefficient_vector": str(ROOT / COEFFICIENT_VECTOR_PATH),
        "theorem_certificate_template": str(ROOT / THEOREM_CERTIFICATE_PATH),
        "alpha_fill_template": str(ROOT / ALPHA_FILL_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "failed_validations": failed_validations,
        "numerator_factorized": True,
        "numerator_zero_signed": False,
        "q_test_zero_signed": False,
        "projected_source_zero_signed": False,
        "source_charge_zero_signed": False,
        "coefficient_template_written": True,
        "R10_fifth_force_passed": False,
        "alpha_curve_valid_for_claim": False,
        "Cextra_zero_signed": False,
        "radial_closure_signed": False,
        "Newton_limit_signed": False,
        "PPN_passed": False,
        "local_GR_promoted": False,
        "csv_shapes": [csv_shape(path) for path, _rows in csv_outputs],
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nfailed_validations={len(failed_validations)}\nnext={NEXT_TARGET}\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
