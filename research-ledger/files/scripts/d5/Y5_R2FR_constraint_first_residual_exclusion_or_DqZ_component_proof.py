from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1783"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1783_0_1782_handoff",
        "source_key": "1782_handoff_doc",
        "source_path": ROOT / "1782-Y5-R2FR-parent-field-chart-Qvis-column-owner-or-Dq-first-component-row.md",
        "needles": ["CDT1782_1_residual_exclusion_rule", "DQF1782_0_DqZ_e_obs", "NEXT1782_0_primary"],
    },
    {
        "source_id": "SRC1783_1_1782_validation",
        "source_key": "1782_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1782_VALIDATION.csv",
        "needles": ["VAL1782_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1783_2_1782_column_matrix",
        "source_key": "1782_qvis_column_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_QVIS_COLUMN_OWNER_MATRIX.csv",
        "needles": ["QCO1782_6_Z_phi_RAB_exclusion", "QCO1782_9_verdict"],
    },
    {
        "source_id": "SRC1783_3_1782_dq_rows",
        "source_key": "1782_dq_first_component_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_DQ_FIRST_COMPONENT_ROW_SCHEMA.csv",
        "needles": ["DQF1782_0_DqZ_e_obs", "DQF1782_5_total_DqZ_abs"],
    },
    {
        "source_id": "SRC1783_4_1022_vertical_quotient",
        "source_key": "1022_vertical_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
        "needles": ["VQC1022_0_q_map", "VQC1022_7_verdict"],
    },
    {
        "source_id": "SRC1783_5_1022_branch_matrix",
        "source_key": "1022_branch_choice",
        "source_path": RESIDUALS / "P8_Y5_R10_1022_BRANCH_DECISION_MATRIX.csv",
        "needles": ["BDM1022_0_absent_quotient", "BDM1022_5_verdict"],
    },
    {
        "source_id": "SRC1783_6_1023_qvx_certificate",
        "source_key": "1023_qvx_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv",
        "needles": ["QVC1023_0_parent_q", "QVC1023_8_verdict"],
    },
    {
        "source_id": "SRC1783_7_1023_coupling_descent",
        "source_key": "1023_coupling_descent",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "needles": ["CDA1023_0_metric_chain_rule", "CDA1023_4_verdict"],
    },
    {
        "source_id": "SRC1783_8_1620_verticality_audit",
        "source_key": "1620_quotient_verticality",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
        "needles": ["QVM1620_2_constraint_first", "QVM1620_5_verdict"],
    },
    {
        "source_id": "SRC1783_9_1620_decision",
        "source_key": "1620_decision",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1620_DECISION.csv",
        "needles": ["DEC1620_2_best_route", "DEC1620_4_next"],
    },
    {
        "source_id": "SRC1783_10_1665_z_route",
        "source_key": "1665_z_route",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1665_Z_ROUTE_SIGNATURE_AUDIT.csv",
        "needles": ["ZRA1665_0_formal_action", "ZRA1665_8_verdict"],
    },
    {
        "source_id": "SRC1783_11_1665_phi_route",
        "source_key": "1665_phi_route",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1665_PHI_ROUTE_SIGNATURE_AUDIT.csv",
        "needles": ["PRA1665_0_tracefree_algebra", "PRA1665_6_verdict"],
    },
    {
        "source_id": "SRC1783_12_1665_coupling_vertical",
        "source_key": "1665_coupling_vertical",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv",
        "needles": ["CVG1665_0_dcdagger_map", "CVG1665_7_verdict"],
    },
    {
        "source_id": "SRC1783_13_1674_qz_ansatz",
        "source_key": "1674_qz_ansatz",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv",
        "needles": ["QANS1674_4_constraint_first_route", "QANS1674_3_response_doublet"],
    },
    {
        "source_id": "SRC1783_14_1667_dq_tests",
        "source_key": "1667_dq_zphi_tests",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "needles": ["DQT1667_5_constraint_first_escape", "DQT1667_6_verdict"],
    },
    {
        "source_id": "SRC1783_15_1555_first_class",
        "source_key": "1555_first_class_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
        "needles": ["FCC1555_0_parent_phase_space", "FCC1555_7_no_GR_import"],
    },
    {
        "source_id": "SRC1783_16_1562_constraint_class",
        "source_key": "1562_constraint_class",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
        "needles": ["CLASS1562_0_first_primary", "CLASS1562_5_second_class"],
    },
    {
        "source_id": "SRC1783_17_1562_stress_gate",
        "source_key": "1562_zero_stress_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv",
        "needles": ["STR1562_0_multiplier_E_lambda", "STR1562_5_current"],
    },
    {
        "source_id": "SRC1783_18_581_no_pole",
        "source_key": "581_quotient_vertical_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
        "needles": ["QVT581_0_parent_projection", "QVT581_7_alpha_result"],
    },
    {
        "source_id": "SRC1783_19_670_no_pole",
        "source_key": "670_no_pole_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        "needles": ["NQ670_0_null_distribution", "NQ670_8_no_pole_result"],
    },
    {
        "source_id": "SRC1783_20_670_effects",
        "source_key": "670_zero_or_residual_effect",
        "source_path": RESIDUALS / "P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
        "needles": ["ZE670_0_K_X", "ZE670_5_R10_R11"],
    },
    {
        "source_id": "SRC1783_21_odd_exchange",
        "source_key": "odd_residual_exchange",
        "source_path": RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv",
        "needles": ["E0_parent_doublet", "E5_current_corpus"],
    },
    {
        "source_id": "SRC1783_22_response_variation",
        "source_key": "response_doublet_variation",
        "source_path": RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "needles": ["AV517_2_first_variation_Z", "AV517_5_positive_theorem"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_SOURCE_REGISTER.csv",
    "constraint_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv",
    "route_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_RESIDUAL_EXCLUSION_ROUTE_MATRIX.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_EXCLUSION_THEOREM_ATTEMPT.csv",
    "dqz_component_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_DQZ_EOBS_COMPONENT_ROWS.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1783_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1783 constraint-first residual exclusion and Dq_Z component evidence",
            }
        )
    return rows


def constraint_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_0_parent_constraint",
            "clause": "residual removed before quotient by parent constraint",
            "mathematical_form": "C_X(Phi)=0 for X in {Z,phi,R_AB/J_q} before q and before matter/readout coupling",
            "source_basis": "CDT1782_1_residual_exclusion_rule;QANS1674_4_constraint_first_route;DQT1667_5_constraint_first_escape",
            "current_status": "CONSTRAINT_FIRST_ROUTE_CONDITIONAL_ONLY",
            "blocking_issue": "no parent action currently supplies C_Z=0 or C_phi=0 with owned variables and boundary terms",
            "exit_condition": "derive C_X from parent Euler/Dirac system or retain finite Dq_X rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_1_momentum_map_generator",
            "clause": "constraint is generated by a differentiable first-class momentum map",
            "mathematical_form": "delta G_X[epsilon]=Omega(delta Phi,v_epsilon), G_X=int epsilon C_X + Q_X",
            "source_basis": "VQC1022_4_momentum_map;QVC1023_5_momentum_map;FCC1555_2_generator;CVG1665_0_dcdagger_map",
            "current_status": "PARENT_OMEGA_DCX_GENERATOR_MISSING",
            "blocking_issue": "formal DCdagger/Omega-flat map exists, but parent Omega, DC_X, and field action are incomplete",
            "exit_condition": "parent symplectic potential, vertical action, differentiability, and bracket closure",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_2_action_descent_no_pole",
            "clause": "bulk action descends and has no physical residual pole",
            "mathematical_form": "S_bulk[Phi]=S_red[q(Phi)] + fixed boundary/topological terms; H(v_X,.)=0 modulo constraints",
            "source_basis": "VQC1022_1_action_descent;QVT581_1_action_factorization;NQ670_3_action_descent;NQ670_4_no_bulk_hessian_block",
            "current_status": "ACTION_DESCENT_AND_NO_POLE_NOT_PROMOTED",
            "blocking_issue": "actual parent Lagrangian, boundary/domain terms, and degree count are not signed",
            "exit_condition": "action factorization plus reduced nondegeneracy/no physical Green function",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_3_matter_readout_descent",
            "clause": "ordinary matter/readout does not source the residual",
            "mathematical_form": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A], Lie_v theta_A=0, and readouts apply after reduction",
            "source_basis": "VQC1022_2_matter_descent;QVC1023_3_matter_descent;CDA1023_1_constants_markers;CDA1023_4_verdict",
            "current_status": "MATTER_CONSTANT_READOUT_DESCENT_UNSIGNED",
            "blocking_issue": "constants, material markers, hidden frame, and post-readout source maps remain legal",
            "exit_condition": "matter category, no-marker theorem, no-shadow frame, and readout functor are signed",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_4_boundary_silence",
            "clause": "constraint carries no local edge/source charge",
            "mathematical_form": "Q_X=0/proper/exact and K_boundary=0; Pi_M^H[Q_X]=0 on compact local branch",
            "source_basis": "VQC1022_5_boundary_silence;QVC1023_6_boundary_silence;NQ670_7_boundary_and_degree_count;ZE670_2_Qbar_XH",
            "current_status": "BOUNDARY_CHARGE_ZERO_NOT_SIGNED",
            "blocking_issue": "edge hair, projector leakage, and cocycle routes are not closed",
            "exit_condition": "zero/proper boundary charge plus no edge cocycle and projector orthogonality",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_5_degree_count",
            "clause": "constraint removes a residual pair rather than hiding a physical mode",
            "mathematical_form": "primary+secondary first-class pair removes X pair; reduced Omega nondegenerate modulo ordinary gauge",
            "source_basis": "VQC1022_6_degree_count;QVC1023_7_degree_count;FCC1555_5_degree_count;CLASS1562_3_brackets_degree",
            "current_status": "DEGREE_COUNT_NOT_COMPUTED",
            "blocking_issue": "zero Hessian alone could be under-specified dynamics rather than gauge",
            "exit_condition": "rank, stabilizer, bracket closure, and reduced phase-space proof",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_6_physical_component_lock",
            "clause": "removed variable equals the physical local residual being tested",
            "mathematical_form": "Z^A=Y_loc^A through q_loc/PPN/source-normalization/coupling order, and phi/R_AB maps to live K_hat/local residuals",
            "source_basis": "ZRA1665_7_physical_residual_lock;RD516_5_PPN_lock;QVM1620_4_normal_form_Z",
            "current_status": "COMPONENT_MAP_NOT_CLOSED",
            "blocking_issue": "formal residual normal form may be a shadow variable rather than the physical PPN/source residual",
            "exit_condition": "component map from parent variables to measured local residual vector",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CFE1783_7_verdict",
            "clause": "constraint-first residual exclusion is live",
            "mathematical_form": "CFE1783_0 through CFE1783_6 pass in one parent branch",
            "source_basis": "1022/1023/1555/1562/1620/1665/1674/1782/581/670",
            "current_status": "CONSTRAINT_FIRST_EXCLUSION_NOT_DERIVED",
            "blocking_issue": "parent constraint, generator, action descent, matter descent, boundary, degree count, and component lock are not jointly signed",
            "exit_condition": "derive C_Z=0/C_phi=0/R_AB constraint-first theorem or score Dq component rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def route_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "REM1783_0_quotient_no_pole",
            "candidate": "quotient/no-pole vertical constraint",
            "target": "X in {Z,phi,R_AB/J_q} is representative data, not physical quotient data",
            "best_use": "lowest-scrutiny route if parent Omega/DC_X/boundary/degree close",
            "current_status": "BEST_ROUTE_CONDITIONAL_UNSIGNED",
            "source_basis": "VQC1022_7_verdict;QVC1023_8_verdict;QVT581_7_alpha_result;NQ670_8_no_pole_result",
            "what_it_would_close": "Dq_X=0, K_X=0, qbar_XT=0, Qbar_XH=0 for the removed channel",
            "missing": "parent Omega;field-by-field v_X;action descent;boundary silence;degree count",
            "selected_priority": 1,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "REM1783_1_exchange_doublet",
            "candidate": "exchange-odd positive response doublet",
            "target": "Z^A=0 in compact local branch by even action, zero odd source, and positive operator",
            "best_use": "strong Z-specific derivation if component lock and odd-charge zero are signed",
            "current_status": "FORMAL_NORMAL_FORM_ONLY",
            "source_basis": "ZRA1665_0_formal_action;E3_even_action;AV517_5_positive_theorem",
            "what_it_would_close": "F_1=0 and local Z amplitude zero/suppressed without pretending Z is q-vertical",
            "missing": "doublet coverage;exchange exactness;matter evenness;J_Z=0;B_Z=0;Z=Y_loc lock",
            "selected_priority": 2,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "REM1783_2_phi_auxiliary",
            "candidate": "phi trace-free auxiliary/constraint route",
            "target": "phi explains K_hat trace-free shape but is removed or source-silent before readout",
            "best_use": "secondary K_hat construction clue, not a coupling solution",
            "current_status": "PHI_OWNER_MISSING",
            "source_basis": "PRA1665_0_tracefree_algebra;PRA1665_6_verdict;DQT1667_2_phi_improvement",
            "what_it_would_close": "phi contribution to Dq/K_hat only if owner, coefficients, boundary, and coupling are signed",
            "missing": "phi parent origin;coefficient sign;boundary/domain;live K_hat adoption;matter/source coupling zero",
            "selected_priority": 3,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "REM1783_3_RAB_second_class",
            "candidate": "R_AB/J_q auxiliary second-class elimination",
            "target": "R_AB or observer-cell residual eliminated algebraically before q",
            "best_use": "possible if multiplier stress and readout regeneration are killed",
            "current_status": "BETTER_CONDITIONAL_THAN_FIRST_CLASS_BUT_UNSIGNED",
            "source_basis": "CLASS1562_5_second_class;STR1562_1_multiplier_metric_stress;STR1562_5_current",
            "what_it_would_close": "R_AB/J_q coframe-visible leak if stress/readout/boundary debts vanish",
            "missing": "zero multiplier stress;no-derivative operator grammar;matter boundary readout silence",
            "selected_priority": 4,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "REM1783_4_finite_DqZ",
            "candidate": "finite Dq_Z component scoring",
            "target": "treat Z as physical or unremoved and bound Dq_Z[e_obs] etc.",
            "best_use": "fallback if derivation-first routes fail",
            "current_status": "SCHEMA_READY_NO_VALUES",
            "source_basis": "DQF1782_0_DqZ_e_obs;DQL1667_0_Dq_Z;DQM1674_5_operator_norm",
            "what_it_would_close": "nothing theorem-zero; makes the residual testable",
            "missing": "component values, units, norms, source paths, arena projections",
            "selected_priority": 5,
            "valid_for_claim": False,
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CFT1783_0_constraint_first_theorem",
            "claim": "constraint-first residual exclusion removes X before q",
            "mathematical_form": "if C_X=0 is first-class, differentiable, boundary-silent, matter/readout-descended, and degree-counted, then q is built on the reduced space and X notin Q_vis",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "CFE1783_0 through CFE1783_6 are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CFT1783_1_no_pole_effect",
            "claim": "no-pole quotient makes local fifth-force coefficients inactive",
            "mathematical_form": "Dq[v_X]=0 plus no physical Green function and Q_X=0 implies K_X=qbar_XT=Qbar_XH=0 for that channel",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent Omega/DC_X, action descent, matter constants, boundary charge, degree count",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CFT1783_2_exchange_positive_route",
            "claim": "exchange-even positive Z sector can force Z=0 on compact local branch",
            "mathematical_form": "E:Z->-Z, S_Z even positive, J_Z=B_Z=0 => integral Z L Z=0 => Z=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "doublet coverage, exchange exactness, matter evenness, odd source/boundary zero, physical residual lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CFT1783_3_phi_warning",
            "claim": "phi trace-free algebra does not by itself remove phi from q or source coupling",
            "mathematical_form": "TF delta(int sqrt(-g) phi R) matching K_hat shape is independent of Dq_phi=0 and delta_phi S_matter=0",
            "proof_status": "COUNTERCLAIM_GUARD",
            "missing_for_current_claim": "phi owner, coefficient sign, boundary/domain, live K_hat adoption, coupling zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CFT1783_4_current_verdict",
            "claim": "current MTS derives C_Z=0/C_phi=0 and Dq_Z[e_obs]=0",
            "mathematical_form": "CFE1783_0 through CFE1783_6 pass and DZE1783 rows vanish",
            "proof_status": "FAIL_CURRENT_PARENT_PROOF",
            "missing_for_current_claim": "constraint-first certificate and Dq component values",
            "valid_for_claim": False,
        },
    ]


def dqz_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_0_geometry",
            "component": "Dq_Z[e_obs,g_obs]",
            "zero_if": "C_Z=0 before q or e_obs=Obs_e(q) and Dq[v_Z]=0 with no common-frame derivative",
            "finite_formula": "epsilon_Z_geom := ||D_Z e_obs|| + ||D_Z g_obs||",
            "required_inputs": "Z basis;parent constraint or Dq matrix;coframe metric norm;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "coframe_metric_component_norm_MISSING",
            "source_anchor": "DQF1782_0_DqZ_e_obs;DQM1674_0_coframe_metric",
            "current_status": "RETAINED_NONCLAIM_DQZ_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_1_source_readout",
            "component": "Dq_Z[source/readout]",
            "zero_if": "matter/source/readout descends through q and constants/material markers are silent",
            "finite_formula": "epsilon_Z_readout := ||Dsource||+||Dclock||+||Dorbit||+||Dphoton||+||Ddetector||+||Dboundary||",
            "required_inputs": "readout functor;constant owner;arena projection;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "readout_component_norm_MISSING",
            "source_anchor": "DQF1782_2_DqZ_source_readout;CDA1023_4_verdict",
            "current_status": "RETAINED_NONCLAIM_DQZ_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_2_constants_markers",
            "component": "Dq_Z[theta_A]",
            "zero_if": "Lie_Z theta_A=0 and no material marker/source-only scalar enters ordinary matter",
            "finite_formula": "epsilon_Z_theta := sum_A ||Lie_Z theta_A||",
            "required_inputs": "constant superselection;material marker owner;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_marker_norm_MISSING",
            "source_anchor": "DQF1782_3_DqZ_theta_A;CDA1023_1_constants_markers",
            "current_status": "RETAINED_NONCLAIM_DQZ_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_3_boundary_tau",
            "component": "Dq_Z[boundary/projector/tau]",
            "zero_if": "Q_Z=0/proper/exact, projector orthogonal, and tau is projectable/role-locked",
            "finite_formula": "epsilon_Z_boundary_tau := ||Dboundary||+||Dprojector||+||Dq(L_tau Phi)-L_tau_red q(Phi)||",
            "required_inputs": "boundary charge;projector silence;tau role lock;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "boundary_tau_norm_MISSING",
            "source_anchor": "DQF1782_4_DqZ_boundary_tau;QVC1023_6_boundary_silence",
            "current_status": "RETAINED_NONCLAIM_DQZ_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_4_component_lock",
            "component": "Z_to_Yloc_projection",
            "zero_if": "Z^A is proven equal to physical local residuals and the same theorem removes those residuals",
            "finite_formula": "epsilon_Z_map := ||Y_loc-Z|| over q_loc/PPN/source/coupling components",
            "required_inputs": "component map;PPN/source-normalization/coupling projection;source path",
            "current_value": "MISSING_COMPONENT_MAP",
            "units": "residual_projection_norm_MISSING",
            "source_anchor": "ZRA1665_7_physical_residual_lock;RD516_5_PPN_lock",
            "current_status": "RETAINED_NONCLAIM_COMPONENT_LOCK_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZE1783_5_total_abs",
            "component": "epsilon_DqZ_constraint_abs",
            "zero_if": "constraint-first theorem closes or all DZE1783_0 through DZE1783_4 vanish in same parent chart",
            "finite_formula": "abs(DZE1783_0)+abs(DZE1783_1)+abs(DZE1783_2)+abs(DZE1783_3)+abs(DZE1783_4)",
            "required_inputs": "component values;common normalizer;source paths;no-cancellation flag",
            "current_value": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "units": "common_dimensionless_or_declared_norm_MISSING",
            "source_anchor": "DQF1782_5_total_DqZ_abs",
            "current_status": "RETAINED_NONCLAIM_ENVELOPE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1783_0_under_specified_zero_hessian",
            "countermodel": "zero Hessian is declared without first-class constraints or degree count",
            "survives_current_constraints": True,
            "why_survives": "degree-count and reduced nondegeneracy are not computed",
            "what_kills_it": "Dirac/rank proof showing the residual pair is removed rather than hidden",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1783_1_boundary_edge_mode",
            "countermodel": "constraint has a nonzero boundary charge or central edge cocycle",
            "survives_current_constraints": True,
            "why_survives": "Q_X=0/proper/exact and K_boundary=0 are unsigned",
            "what_kills_it": "differentiable zero/proper boundary charge and projector-orthogonality proof",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1783_2_matter_marker_source",
            "countermodel": "matter constants or source/readout maps depend on Z even when geometry does not",
            "survives_current_constraints": True,
            "why_survives": "constant/material marker and readout descent are not parent-signed",
            "what_kills_it": "Lie_Z theta_A=0 plus no-shadow/readout functor theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1783_3_shadow_Z",
            "countermodel": "formal Z is constrained to zero but is not the physical PPN/source residual",
            "survives_current_constraints": True,
            "why_survives": "Z-to-Y_loc component map is missing",
            "what_kills_it": "component-lock proof through q_loc/PPN/source-normalization/coupling order",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1783_4_phi_shape_only",
            "countermodel": "phi reproduces a trace-free tensor shape but retains an independent source or boundary coupling",
            "survives_current_constraints": True,
            "why_survives": "K_hat shape match is independent of phi owner/coupling silence",
            "what_kills_it": "parent phi action/constraint plus boundary/domain and matter/source descent",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1783_0_constraint_first",
            "claim": "C_Z=0/C_phi=0 residual exclusion is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "CFE1783_7 remains CONSTRAINT_FIRST_EXCLUSION_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1783_1_DqZ_zero",
            "claim": "Dq_Z[e_obs]=0 or total Dq_Z=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "DZE1783 rows contain MISSING_NUMERIC_OR_THEOREM_ZERO and missing component map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1783_2_no_pole_R10_R11",
            "claim": "no-pole removes R10/R11/local residual branch",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "K_X, qbar_XT, Qbar_XH remain missing no-pole/source/boundary certificates",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1783_3_local_gr",
            "claim": "local GR/Newton/PPN follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "constraint-first exclusion, q/Dq, source-current, and boundary/tau locks remain upstream",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1783_0_exact_result",
            "decision": "CONSTRAINT_FIRST_EXCLUSION_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "a first-class, boundary-silent, matter-descended parent constraint removes X before q without post-hoc deletion",
            "next_action": "keep theorem as contract until parent clauses are signed",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1783_1_current_status",
            "decision": "C_Z_C_PHI_NOT_DERIVED_CURRENT_MTS",
            "reason": "parent constraint, Omega/DC_X generator, matter descent, boundary silence, degree count, and component lock are missing",
            "next_action": "do not claim Dq_Z=0, no-pole, or local-GR recovery",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1783_2_fallback",
            "decision": "DQZ_EOBS_COMPONENT_ROWS_STAGED_NONCLAIM",
            "reason": "if constraint-first fails, the first honest row is Dq_Z[e_obs,g_obs] plus source/readout/constant/boundary/component-lock terms",
            "next_action": "source no numeric component without units, norm, and source path",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1783_3_best_next",
            "decision": "PARENT_OMEGA_DCX_VERTICAL_ACTION_PACKET_IS_NEXT",
            "reason": "the common blocker for quotient/no-pole, constraint-first, and Dq verticality is the parent Omega/DC_X/field-action map",
            "next_action": "build 1784 parent Omega/DC_X vertical action packet or demote to finite DqZ geometry component",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1783_0_primary",
            "next_target": "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md",
            "script": "scripts/Y5_R2FR_parent_Omega_DCX_vertical_action_packet_or_DqZ_geometry_row.py",
            "objective": "try to construct the parent Omega/DC_X/v_X field-action packet needed by constraint-first exclusion; if not, stage Dq_Z[e_obs,g_obs] finite geometry row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1783_1_parallel",
            "next_target": "1784b-Y5-R2FR-Z-physical-component-lock-to-PPN-source-vector.md",
            "script": "scripts/Y5_R2FR_Z_physical_component_lock_to_PPN_source_vector.py",
            "objective": "map formal Z^A to physical q_loc/PPN/source-normalization/coupling residual vector or retain shadow-Z guard",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1783_2_later",
            "next_target": "1785-Y5-R2FR-boundary-charge-zero-proper-or-edge-mode-residual-row.md",
            "script": "scripts/Y5_R2FR_boundary_charge_zero_proper_or_edge_mode_residual_row.py",
            "objective": "attack Q_X boundary silence after vertical generator is sharper",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "constraint_gate": constraint_gate_rows(),
        "route_matrix": route_matrix_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "dqz_component_rows": dqz_component_rows(),
        "countermodel": countermodel_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1783_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1783_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1783-Y5-R2FR-constraint-first-residual-exclusion-or-DqZ-component-proof.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1783_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1783_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1783_2_constraint_gate_complete",
            any(row["gate_id"] == "CFE1783_7_verdict" for row in rows_map["constraint_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["constraint_gate"]),
            "constraint-first exclusion gate is complete and nonclaim",
        ),
        (
            "VAL1783_3_route_matrix_complete",
            any(row["route_id"] == "REM1783_0_quotient_no_pole" for row in rows_map["route_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["route_matrix"]),
            "residual exclusion route matrix is complete and nonclaim",
        ),
        (
            "VAL1783_4_conditional_theorems_written",
            any(row["theorem_id"] == "CFT1783_0_constraint_first_theorem" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["theorem_attempt"])
            and any(row["theorem_id"] == "CFT1783_2_exchange_positive_route" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["theorem_attempt"]),
            "constraint-first and exchange-positive conditional theorems are written",
        ),
        (
            "VAL1783_5_current_proof_not_promoted",
            any(row["theorem_id"] == "CFT1783_4_current_verdict" and row["proof_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["theorem_attempt"]),
            "current C_Z/C_phi/Dq_Z proof remains unpromoted",
        ),
        (
            "VAL1783_6_dqz_rows_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dqz_component_rows"]
            ),
            "Dq_Z component rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1783_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1783_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1783_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1783_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1783_11_decision_next",
            any(row["decision_id"] == "DEC1783_3_best_next" and "PARENT_OMEGA_DCX" in row["decision"] for row in rows_map["decision"]),
            "decision selects parent Omega/DC_X vertical action packet next",
        ),
        (
            "VAL1783_12_next_selected",
            any(row["route_id"] == "NEXT1783_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1783_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1783 CSVs parse"),
        ("VAL1783_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1783_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1783_16_formalization_untouched", formalization_untouched(), "no 1783 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1783_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1783 constraint-first residual exclusion or Dq_Z component proof checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1783 - Y5/R2FR Constraint-First Residual Exclusion or DqZ Component Proof",
            "",
            "## Verdict",
            "",
            "1783 proves the clean shape of the route but does not promote it. A residual `X` can be safely excluded before the quotient only if it is removed by a parent-owned constraint/symmetry with a differentiable generator, no local boundary charge, matter/readout descent, and a real degree-count proof. Then `X` is representative data, not a physical observed pole.",
            "",
            "Current MTS does not yet have that signed for `Z`, `phi`, or `R_AB/J_q`. The quotient/no-pole route remains the lowest-scrutiny path, and the exchange-odd positive `Z` route remains a strong secondary path, but both are conditional. Therefore the fallback is explicit nonclaim `Dq_Z` component rows, starting with `Dq_Z[e_obs,g_obs]`.",
            "",
            "**Claim ceiling:** no `C_Z=0`, no `C_phi=0`, no `Dq_Z=0`, no no-pole/R10/R11/local-GR pass, no source-current closure, no GitHub action, and no `formalization-workbench` edit is allowed from 1783.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Constraint-First Exclusion Gate",
            markdown_table(rows_map["constraint_gate"], ["gate_id", "clause", "mathematical_form", "current_status", "blocking_issue", "exit_condition", "valid_for_claim"]),
            "",
            "## Residual Exclusion Route Matrix",
            markdown_table(rows_map["route_matrix"], ["route_id", "candidate", "target", "best_use", "current_status", "what_it_would_close", "missing", "selected_priority", "valid_for_claim"]),
            "",
            "## Exclusion Theorem Attempt",
            markdown_table(rows_map["theorem_attempt"], ["theorem_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## DqZ Component Rows",
            markdown_table(rows_map["dqz_component_rows"], ["row_id", "component", "zero_if", "finite_formula", "current_value", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This checkpoint is a real tightening. The branch is not dead; it is now sharply localized. To get local GR in a derivable way, the next object is not another phenomenological fit. It is the parent `Omega/DC_X/v_X` packet that makes a constraint-first quotient route executable. If that packet fails, we stop trying to hide `Z` and start scoring the `Dq_Z` geometry row.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1783-Y5-R2FR-constraint-first-residual-exclusion-or-DqZ-component-proof.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1783 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
