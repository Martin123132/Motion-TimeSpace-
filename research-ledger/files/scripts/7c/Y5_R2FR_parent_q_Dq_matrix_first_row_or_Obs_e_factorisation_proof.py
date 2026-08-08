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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1781"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1781_0_1780_handoff",
        "source_key": "1780_handoff_doc",
        "source_path": ROOT / "1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md",
        "needles": ["QTS1780_0_parent_q_map", "QTS1780_7_verdict", "NEXT1780_0_primary"],
    },
    {
        "source_id": "SRC1781_1_1780_validation",
        "source_key": "1780_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1780_VALIDATION.csv",
        "needles": ["VAL1780_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1781_2_1780_signature_gate",
        "source_key": "1780_q_dq_tau_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
        "needles": ["QTS1780_0_parent_q_map", "QTS1780_2_observed_coframe_functor", "QTS1780_7_verdict"],
    },
    {
        "source_id": "SRC1781_3_1780_delta_rows",
        "source_key": "1780_delta_frame_tau_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_DELTA_FRAME_TAU_FIRST_ROW_SCHEMA.csv",
        "needles": ["DFT1780_0_DObs_e", "DFT1780_1_Dreadout", "DFT1780_6_total_abs"],
    },
    {
        "source_id": "SRC1781_4_1667_field_chart",
        "source_key": "1667_parent_field_chart",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
        "needles": ["PFC1667_0_visible_quotient", "PFC1667_7_chart_verdict"],
    },
    {
        "source_id": "SRC1781_5_1667_q_audit",
        "source_key": "1667_quotient_map_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
        "needles": ["QMA1667_0_q_prior", "QMA1667_6_verdict"],
    },
    {
        "source_id": "SRC1781_6_1667_dq_tests",
        "source_key": "1667_dq_on_zphi_tests",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "needles": ["DQT1667_0_test_definition", "DQT1667_6_verdict"],
    },
    {
        "source_id": "SRC1781_7_1667_dq_leaks",
        "source_key": "1667_retained_dq_leaks",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
        "needles": ["DQL1667_0_Dq_Z", "DQL1667_3_DObs_e", "DQL1667_7_Scg_envelope"],
    },
    {
        "source_id": "SRC1781_8_1674_qz_ansatz",
        "source_key": "1674_parent_q_z_ansatz",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv",
        "needles": ["QANS1674_0_parent_chart", "QANS1674_4_constraint_first_route"],
    },
    {
        "source_id": "SRC1781_9_1674_dqz_matrix",
        "source_key": "1674_dqz_component_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv",
        "needles": ["DQM1674_0_coframe_metric", "DQM1674_5_operator_norm"],
    },
    {
        "source_id": "SRC1781_10_1675_coframe_descent",
        "source_key": "1675_coframe_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_COFRAME_DESCENT_GATE.csv",
        "needles": ["CDG1675_0_obs_functor", "CDG1675_3_verdict"],
    },
    {
        "source_id": "SRC1781_11_1675_source_readout",
        "source_key": "1675_source_readout_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
        "needles": ["SRD1675_0_matter_domain", "SRD1675_5_verdict"],
    },
    {
        "source_id": "SRC1781_12_1737_q_map_contract",
        "source_key": "1737_q_map_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
        "needles": ["QMAP1737_0_Q_vis", "QMAP1737_2_source_readout", "QMAP1737_6_boundary_projector"],
    },
    {
        "source_id": "SRC1781_13_1737_vertical_basis",
        "source_key": "1737_vertical_basis_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
        "needles": ["VB1737_0_vZ", "VB1737_5_vtau_readout"],
    },
    {
        "source_id": "SRC1781_14_1737_dq_requirements",
        "source_key": "1737_dq_matrix_requirements",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
        "needles": ["DQM1737_0_DObs_e", "DQM1737_5_Dq_total_kernel"],
    },
    {
        "source_id": "SRC1781_15_1738_kernel_theorem",
        "source_key": "1738_kernel_theorem_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_KERNEL_THEOREM_ATTEMPT.csv",
        "needles": ["DOK1738_0_chain_rule_kernel", "DOK1738_2_current_verdict"],
    },
    {
        "source_id": "SRC1781_16_1738_dobs_rows",
        "source_key": "1738_finite_dobs_e_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
        "needles": ["DBG1738_0_common_frame_log_derivative", "DOE1738_4_total_coframe_kernel_envelope"],
    },
    {
        "source_id": "SRC1781_17_1739_coframe_owner",
        "source_key": "1739_parent_coframe_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
        "needles": ["PCO1739_0_parent_q", "PCO1739_6_no_source_prefactor"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_SOURCE_REGISTER.csv",
    "q_dq_matrix_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_Q_DQ_MATRIX_GATE.csv",
    "obs_factorisation": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_OBS_E_FACTORISATION_THEOREM_ATTEMPT.csv",
    "dq_obs_first_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_DQ_OBS_E_FIRST_ROW_SCHEMA.csv",
    "retained_direction_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_RETAINED_DIRECTION_MATRIX_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1781_VALIDATION.csv",
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
                "role": "1781 parent q/Dq matrix and Obs_e factorisation evidence",
            }
        )
    return rows


def q_dq_matrix_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_0_parent_field_chart",
            "object": "Phi_parent",
            "mathematical_form": "Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc)",
            "source_basis": "PFC1667_7_chart_verdict;QANS1674_0_parent_chart",
            "current_status": "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED",
            "blocks": "q and Dq cannot be represented as a parent-owned matrix until chart coordinates are adopted",
            "exit_condition": "parent action declares the chart or proves chart-equivalent coordinates",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_1_Qvis_column_contract",
            "object": "Q_vis columns",
            "mathematical_form": "Q_vis=(e_obs,g_obs,mu_m,D_m,source/readout data,theta_owned,A_owned)",
            "source_basis": "QANS1674_1_visible_quotient;QMAP1737_0_Q_vis;QMAP1737_2_source_readout",
            "current_status": "VISIBLE_QUOTIENT_COLUMNS_CANDIDATE_ONLY",
            "blocks": "columns are named, but not owned as the unique ordinary-matter quotient",
            "exit_condition": "one source-backed q column table with every retained parent variable included or excluded by theorem",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_2_vertical_basis_rows",
            "object": "candidate vertical basis",
            "mathematical_form": "v_a in {v_Z,v_phi,v_RAB/Jq,v_boundary,v_theta_marker,v_tau_readout}",
            "source_basis": "VB1737_0_vZ..VB1737_5_vtau_readout;DQT1667_6_verdict",
            "current_status": "VERTICAL_BASIS_UNSIGNED",
            "blocks": "Dq[v_a]=0 cannot be claimed without an explicit basis and norms",
            "exit_condition": "basis vectors are generated by parent symmetries/constraints or retained as finite rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_3_Dq_matrix_object",
            "object": "Dq component matrix",
            "mathematical_form": "M_{ia}=Dq_i[v_a] for q_i in (e_obs,g_obs,source/readout,theta,boundary,tau pushforward)",
            "source_basis": "DQM1737_0_DObs_e..DQM1737_5_Dq_total_kernel;DQM1674_0_coframe_metric..DQM1674_5_operator_norm",
            "current_status": "MISSING_DQ_MATRIX_VALUES_OR_THEOREM_ZEROS",
            "blocks": "chain-rule zero cannot be applied componentwise",
            "exit_condition": "every matrix cell has theorem-zero or finite value with units, norm, and source path",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_4_Obs_e_factorisation",
            "object": "observed coframe functor",
            "mathematical_form": "e_obs(Phi)=Obs_e(q(Phi)) and DObs_e[v]=DObs_e|_q Dq[v]",
            "source_basis": "CDG1675_0_obs_functor;DOK1738_0_chain_rule_kernel;QTS1780_2_observed_coframe_functor",
            "current_status": "FACTORISATION_NOT_PARENT_SIGNED",
            "blocks": "same visible frame can still depend on a residual representative through a common-frame derivative",
            "exit_condition": "Obs_e(q) owner plus b_g,X=0 theorem or finite DObs_e source rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_5_source_readout_columns",
            "object": "source/readout quotient columns",
            "mathematical_form": "Dsource_readout[Dq(v)]=Dclock[Dq(v)]=Dorbit[Dq(v)]=Dboundary[Dq(v)]=0",
            "source_basis": "SRD1675_0_matter_domain..SRD1675_5_verdict;DFT1780_1_Dreadout",
            "current_status": "SOURCE_READOUT_DESCENT_NOT_CLOSED",
            "blocks": "coframe silence alone is not enough for source, clock, orbit, detector, or boundary silence",
            "exit_condition": "readout functor descends through Q_vis or finite leakage rows are sourced",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_6_DqZ_first_component",
            "object": "Dq_Z first row",
            "mathematical_form": "Dq_Z[e_obs,g_obs,mu_m,D_m,source/readout,theta,boundary,tau]",
            "source_basis": "DQL1667_0_Dq_Z;DQM1674_0_coframe_metric;DQM1674_1_source_current;DQM1674_3_boundary_projector",
            "current_status": "FIRST_COMPONENT_ROW_STAGED_NONCLAIM",
            "blocks": "Z cannot be called quotient-vertical while any component remains MISSING_NUMERIC_OR_THEOREM_ZERO",
            "exit_condition": "Dq_Z is theorem-zero on all Q_vis columns or finite Dq_Z norm is source-backed",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "QDM1781_7_verdict",
            "object": "parent q/Dq matrix and Obs_e factorisation",
            "mathematical_form": "QDM1781_0 through QDM1781_6 pass in one parent branch",
            "source_basis": "1667/1674/1675/1737/1738/1739 plus 1780 handoff",
            "current_status": "Q_DQ_MATRIX_NOT_CONSTRUCTED_OBS_E_FACTORISATION_NOT_SIGNED",
            "blocks": "Delta_frame_tau and DObs_e/Dq rows remain mandatory",
            "exit_condition": "construct q matrix, Dq matrix, Obs_e(q) factorisation, source/readout descent, and tau pushforward",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def obs_factorisation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OEF1781_0_chain_rule_theorem",
            "claim": "observed coframe leakage vanishes if e_obs factors through q and v is q-vertical",
            "mathematical_form": "for e_obs=Obs_e(q(Phi)), delta_v e_obs=DObs_e|_q[Dq[v]], so Dq[v]=0 implies delta_v e_obs=0",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent q, retained basis, Dq matrix, and Obs_e(q) ownership are not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OEF1781_1_matrix_requirement",
            "claim": "the chain rule requires a declared matrix, not a verbal quotient",
            "mathematical_form": "Dq[v_a]=(Dq_i[v_a])_i with rows for coframe/metric, source-readout, theta, boundary/projector, and tau pushforward",
            "proof_status": "REQUIREMENT_DEFINED",
            "missing_for_current_claim": "Dq_i[v_a] cells are currently missing theorem-zero or finite source-backed values",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OEF1781_2_finite_row_fallback",
            "claim": "if matrix-zero fails, the honest fallback is a finite DObs_e/Dq residual row",
            "mathematical_form": "epsilon_DObs_e_abs=sum_a ||DObs_e|_q[Dq[v_a]]|| plus common-frame derivative b_g,X",
            "proof_status": "RESIDUAL_ROW_STAGED",
            "missing_for_current_claim": "component values, common norm, units, and source paths",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OEF1781_3_common_frame_countermodel",
            "claim": "one matter frame does not prove factorisation through q",
            "mathematical_form": "e_obs(Phi)=exp(b_g X)e0(q(Phi)) gives delta_X e_obs=b_g e_obs while all species still see one frame",
            "proof_status": "COUNTERMODEL_EXPOSED",
            "missing_for_current_claim": "no-shadow/common-frame derivative theorem or finite b_g,X row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OEF1781_4_current_verdict",
            "claim": "current MTS proves Obs_e(q) and DObs_e[v]=0",
            "mathematical_form": "QDM1781_0 through QDM1781_6 pass and all retained direction rows vanish",
            "proof_status": "FAIL_CURRENT_PARENT_PROOF",
            "missing_for_current_claim": "q/Dq matrix, Q_vis column ownership, source-readout descent, and common-frame silence",
            "valid_for_claim": False,
        },
    ]


def dq_obs_first_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_0_Dq_Z_Qvis",
            "component": "Dq_Z_Qvis",
            "direction": "v_Z=partial_Z",
            "derivative_object": "Dq_Z[e_obs,g_obs,mu_m,D_m,source/readout,theta,boundary,tau]",
            "formula": "||Dq_Z||_Qvis = sqrt(sum_i ||Dq_i[v_Z]||^2)",
            "required_parent_input": "parent chart;Q_vis columns;Z basis;component norms;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "component_norm_or_declared_dimensionless_MISSING",
            "source_anchor": "DQL1667_0_Dq_Z;DQM1674_0..5;DQM1737_5_Dq_total_kernel",
            "current_status": "RETAINED_NONCLAIM_DQ_FIRST_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_1_DObs_e_vZ",
            "component": "DObs_e_vZ",
            "direction": "v_Z=partial_Z",
            "derivative_object": "observed coframe derivative along Z",
            "formula": "||DObs_e[v_Z]|| <= ||DObs_e|_q|| ||Dq[v_Z]|| + |b_g,Z|",
            "required_parent_input": "Obs_e(q);Dq_Z;common-frame derivative b_g,Z;coframe norm;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "coframe_norm_or_metric_norm_MISSING",
            "source_anchor": "DQL1667_3_DObs_e;DOE1738_0_vZ;DFT1780_0_DObs_e",
            "current_status": "RETAINED_NONCLAIM_DOBS_E_FIRST_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_2_Dsource_readout_vZ",
            "component": "Dsource_readout_vZ",
            "direction": "v_Z=partial_Z",
            "derivative_object": "source, clock, orbit, photon, detector, and boundary readout derivative",
            "formula": "||Dreadout[Dq(v_Z)]|| = ||Dsource||+||Dclock||+||Dorbit||+||Dphoton||+||Dboundary||",
            "required_parent_input": "readout functor;arena projection;component norms;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "readout_norm_MISSING",
            "source_anchor": "DQL1667_4_Dsource_readout;SRD1675_4_readouts;DFT1780_1_Dreadout",
            "current_status": "RETAINED_NONCLAIM_READOUT_FIRST_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_3_Dtheta_marker_vZ",
            "component": "Dtheta_marker_vZ",
            "direction": "v_Z=partial_Z",
            "derivative_object": "constants/material marker leakage",
            "formula": "sum_A ||Lie_vZ theta_A|| + ||D_marker[Dq(v_Z)]||",
            "required_parent_input": "constant superselection;material marker owner;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_marker_norm_MISSING",
            "source_anchor": "DQL1667_5_Dtheta_marker;SRD1675_2_constants_markers;DFT1780_3_constants_marker",
            "current_status": "RETAINED_NONCLAIM_MARKER_FIRST_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_4_Dboundary_projector_vZ",
            "component": "Dboundary_projector_vZ",
            "direction": "v_Z=partial_Z",
            "derivative_object": "boundary, collar, projector, and source-support leakage",
            "formula": "||Pi_local delta_vZ B_A|| + ||delta_vZ P_loc|| + ||delta_vZ W_source||",
            "required_parent_input": "boundary descent;projector descent;worldtube support;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "boundary_projector_norm_MISSING",
            "source_anchor": "DQL1667_6_boundary_projector;QMAP1737_6_boundary_projector;DFT1780_5_worldtube_boundary",
            "current_status": "RETAINED_NONCLAIM_BOUNDARY_FIRST_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQR1781_5_total_q_dq_obs_abs",
            "component": "epsilon_q_Dq_Obs_abs",
            "direction": "all retained local directions",
            "derivative_object": "absolute no-cancellation q/Dq/Obs_e leakage envelope",
            "formula": "abs(DQR1781_0)+abs(DQR1781_1)+abs(DQR1781_2)+abs(DQR1781_3)+abs(DQR1781_4)+tau_pushforward_term",
            "required_parent_input": "all component values;common normalizer;no-cancellation flag;source paths",
            "current_value": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "units": "common_dimensionless_or_declared_arena_norm_MISSING",
            "source_anchor": "DFT1780_6_total_abs;DQM1737_5_Dq_total_kernel",
            "current_status": "RETAINED_NONCLAIM_ENVELOPE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def retained_direction_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_0_vZ",
            "direction": "v_Z=partial_Z",
            "declared_role": "response-doublet/residual local direction",
            "q_columns_to_test": "e_obs;g_obs;source/readout;theta;boundary/projector;tau pushforward",
            "current_Dq_status": "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK",
            "DObs_e_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_basis": "DQT1667_1_Z_normal_form;DQM1674_0..5;DOE1738_0_vZ",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_1_vphi",
            "direction": "v_phi=partial_phi",
            "declared_role": "trace-free improvement auxiliary candidate",
            "q_columns_to_test": "e_obs;connection;source/readout;boundary/projector",
            "current_Dq_status": "PHI_OWNER_MISSING_DQ_NOT_COMPUTABLE",
            "DObs_e_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_basis": "DQT1667_2_phi_improvement;DQL1667_1_Dq_phi;DOE1738_1_vphi",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_2_vRAB_Jq",
            "direction": "v_RAB/Jq",
            "declared_role": "radial phase-cell or observer cell direction",
            "q_columns_to_test": "coframe/cell data;source normalization;readout;boundary",
            "current_Dq_status": "REJECT_ZERO_CURRENT_EVIDENCE",
            "DObs_e_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_basis": "DQT1667_3_RAB_Jq_direction;DQL1667_2_Dq_RAB_Jq;DOE1738_2_vRAB_Jq",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_3_vboundary",
            "direction": "v_boundary/projector",
            "declared_role": "boundary, collar, projector, and source support direction",
            "q_columns_to_test": "boundary/projector;worldtube support;readout",
            "current_Dq_status": "BOUNDARY_PROJECTOR_OPEN",
            "DObs_e_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "source_basis": "QMAP1737_6_boundary_projector;DQL1667_6_boundary_projector;DOE1738_3_vboundary",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_4_vtheta_marker",
            "direction": "v_theta_marker",
            "declared_role": "constants/material marker direction",
            "q_columns_to_test": "theta_owned;source labels;clock/EM constants",
            "current_Dq_status": "CONSTANT_MARKER_SILENCE_NOT_DERIVED",
            "DObs_e_status": "not_applicable_until_marker_owner_known",
            "source_basis": "SRD1675_2_constants_markers;DQM1737_2_Dtheta_marker;DFT1780_3_constants_marker",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "direction_id": "RDM1781_5_vtau_readout",
            "direction": "v_tau_readout",
            "declared_role": "tau pushforward and role-lock direction",
            "q_columns_to_test": "source tau;charge tau;clock tau;orbit tau;boundary tau",
            "current_Dq_status": "MISSING_TAU_PROJECTABILITY_AND_LOCK",
            "DObs_e_status": "not_closed_without_tau_pushforward",
            "source_basis": "DQM1737_4_Dtau_pushforward;QTS1780_3_tau_projectability;DFT1780_2_tau_roles",
            "kernel_claimed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1781_0_partial_q_definition",
            "countermodel": "q verbally excludes residual variables, but no parent matrix prevents e_obs from depending on their representative",
            "survives_current_constraints": True,
            "why_survives": "Q_vis columns are candidate-only and Dq cells are not computed",
            "what_kills_it": "explicit q table plus Dq matrix with theorem-zero or source-backed finite rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1781_1_common_frame_residual",
            "countermodel": "all matter sees the same frame e_obs=exp(b_g X)e0, but the common frame changes with residual X",
            "survives_current_constraints": True,
            "why_survives": "same frame is weaker than Obs_e(q)",
            "what_kills_it": "Obs_e(q) factorisation and b_g,X=0 theorem or finite b_g,X row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1781_2_source_readout_postmap",
            "countermodel": "source, detector, clock, or orbit readouts apply an X-dependent post-map after coframe construction",
            "survives_current_constraints": True,
            "why_survives": "source-readout descent remains unsigned",
            "what_kills_it": "readout functor descends through Q_vis or finite readout leakage rows are bounded",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1781_3_tau_pushforward_mismatch",
            "countermodel": "tau selected in parent space does not push forward to the same source/charge/clock/orbit generator",
            "survives_current_constraints": True,
            "why_survives": "Dq(L_tau Phi)-L_tau_red q(Phi) is not computed",
            "what_kills_it": "tau projectability theorem and role-lock rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1781_4_boundary_projector_reentry",
            "countermodel": "boundary, collar, or projector terms re-enter local source/readout even when bulk coframe is silent",
            "survives_current_constraints": True,
            "why_survives": "boundary/projector descent is open",
            "what_kills_it": "boundary/projector q-basic theorem or finite boundary row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1781_0_q_matrix",
            "claim": "parent q/Dq matrix is constructed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "QDM1781_7 remains Q_DQ_MATRIX_NOT_CONSTRUCTED_OBS_E_FACTORISATION_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1781_1_obs_factorisation",
            "claim": "Obs_e factors through q and DObs_e[v]=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "OEF1781_4 remains FAIL_CURRENT_PARENT_PROOF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1781_2_dq_first_rows",
            "claim": "finite Dq/DObs_e rows are source-backed and ready",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "DQR1781 rows contain MISSING_NUMERIC_OR_THEOREM_ZERO and missing norms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1781_3_local_gr",
            "claim": "local GR/Newton/PPN/R10 pass follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "q/Dq/Obs_e/source-readout/tau machinery is upstream of local-GR recovery",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1781_0_exact_result",
            "decision": "OBS_E_FACTORISATION_CHAIN_RULE_IS_EXACT_CONDITIONAL",
            "reason": "if e_obs=Obs_e(q(Phi)) and Dq[v]=0, then DObs_e[v]=0 is a direct differential-chain-rule statement",
            "next_action": "keep as theorem contract only",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1781_1_current_status",
            "decision": "Q_DQ_MATRIX_NOT_CONSTRUCTED_OBS_E_FACTORISATION_NOT_SIGNED",
            "reason": "q columns, vertical basis, Dq cells, source-readout columns, and tau pushforward are still candidate-only",
            "next_action": "do not promote local-GR or source-current closure",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1781_2_first_row",
            "decision": "Dq_AND_DObs_E_FIRST_ROWS_STAGED_NONCLAIM",
            "reason": "the failed proof has been converted into explicit component rows with missing values and gates",
            "next_action": "fill no component without source path, units, norm, and no-cancellation rule",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1781_3_best_next",
            "decision": "PARENT_FIELD_CHART_AND_QVIS_COLUMN_OWNER_IS_NEXT",
            "reason": "Dq matrix cells cannot be filled until the parent chart and Q_vis columns are owned",
            "next_action": "build 1782 parent field-chart/Q_vis column-owner gate or first Dq component theorem row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1781_0_primary",
            "next_target": "1782-Y5-R2FR-parent-field-chart-Qvis-column-owner-or-Dq-first-component-row.md",
            "script": "scripts/Y5_R2FR_parent_field_chart_Qvis_column_owner_or_Dq_first_component_row.py",
            "objective": "try to parent-own the field chart and Q_vis columns; if not, stage the first Dq component theorem/value row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1781_1_parallel",
            "next_target": "1782b-Y5-R2FR-tau-pushforward-role-lock-component-pack.md",
            "script": "scripts/Y5_R2FR_tau_pushforward_role_lock_component_pack.py",
            "objective": "prepare tau pushforward and source/charge/clock/orbit/boundary role-lock rows",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1781_2_later",
            "next_target": "1783-Y5-R2FR-no-shadow-common-frame-derivative-zero-or-bg-first-row.md",
            "script": "scripts/Y5_R2FR_no_shadow_common_frame_derivative_zero_or_bg_first_row.py",
            "objective": "attack the b_g,X common-frame derivative after q/Dq columns are sharper",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "q_dq_matrix_gate": q_dq_matrix_gate_rows(),
        "obs_factorisation": obs_factorisation_rows(),
        "dq_obs_first_rows": dq_obs_first_rows(),
        "retained_direction_matrix": retained_direction_matrix_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1781_{key.upper()}.csv")


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
                "kernel_claimed",
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
        if not (RAB_QUEUE / f"JR1781_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1781-Y5-R2FR-parent-q-Dq-matrix-first-row-or-Obs-e-factorisation-proof.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1781_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1781_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1781_2_q_matrix_gate_complete",
            any(row["gate_id"] == "QDM1781_7_verdict" for row in rows_map["q_dq_matrix_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["q_dq_matrix_gate"]),
            "q/Dq matrix gate is complete and nonclaim",
        ),
        (
            "VAL1781_3_chain_rule_theorem_written",
            any(row["theorem_id"] == "OEF1781_0_chain_rule_theorem" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["obs_factorisation"]),
            "exact Obs_e(q) chain-rule theorem is written",
        ),
        (
            "VAL1781_4_current_proof_not_promoted",
            any(row["theorem_id"] == "OEF1781_4_current_verdict" and row["proof_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["obs_factorisation"]),
            "current Obs_e/Dq proof remains unpromoted",
        ),
        (
            "VAL1781_5_first_rows_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dq_obs_first_rows"]
            ),
            "Dq/DObs_e first rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1781_6_retained_directions_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["kernel_claimed"]) for row in rows_map["retained_direction_matrix"]),
            "retained direction matrix claims no kernel",
        ),
        (
            "VAL1781_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1781_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1781_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1781_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1781_11_decision_next",
            any(row["decision_id"] == "DEC1781_3_best_next" and "PARENT_FIELD_CHART" in row["decision"] for row in rows_map["decision"]),
            "decision selects parent field-chart/Q_vis column owner next",
        ),
        (
            "VAL1781_12_next_selected",
            any(row["route_id"] == "NEXT1781_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1781_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1781 CSVs parse"),
        ("VAL1781_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1781_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1781_16_formalization_untouched", formalization_untouched(), "no 1781 outputs found under formalization-workbench"),
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
            "check_id": "VAL1781_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1781 parent q/Dq matrix first row or Obs_e factorisation proof checkpoint",
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
            "# 1781 - Y5/R2FR Parent q-Dq Matrix First Row or Obs-e Factorisation Proof",
            "",
            "## Verdict",
            "",
            "1781 sharpens the 1780 handoff. The clean theorem is real and simple: if the observed coframe is genuinely a functor of the parent quotient, `e_obs=Obs_e(q(Phi))`, and a retained direction is truly vertical, `Dq[v]=0`, then `DObs_e[v]=0` follows by the chain rule.",
            "",
            "The current corpus still does not own the parent `q` matrix, the `Dq` matrix cells, the retained basis, the source/readout columns, or the tau pushforward. So the proof is not promoted. The work product is a nonclaim q/Dq matrix gate and first-row schema for `Dq_Z`, `DObs_e[v_Z]`, readout, constants, boundary, and the total absolute envelope.",
            "",
            "**Claim ceiling:** no q/Dq matrix claim, no `Obs_e(q)` claim, no `DObs_e=0`, no source-current closure, no local-GR/Newton/PPN/R10 pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1781.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## q/Dq Matrix Gate",
            markdown_table(rows_map["q_dq_matrix_gate"], ["gate_id", "object", "mathematical_form", "current_status", "source_basis", "blocks", "exit_condition", "valid_for_claim"]),
            "",
            "## Obs-e Factorisation Theorem Attempt",
            markdown_table(rows_map["obs_factorisation"], ["theorem_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## Dq / DObs-e First Row Schema",
            markdown_table(rows_map["dq_obs_first_rows"], ["row_id", "component", "direction", "derivative_object", "formula", "current_value", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Retained Direction Matrix",
            markdown_table(rows_map["retained_direction_matrix"], ["direction_id", "direction", "declared_role", "q_columns_to_test", "current_Dq_status", "DObs_e_status", "kernel_claimed", "valid_for_claim"]),
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
            "This is one of the better routes because it asks for the least magic. Instead of smuggling in local GR by saying the extra directions are invisible, it demands the exact object that makes invisibility true: a parent-owned quotient map and its differential. If that fails, the residual is already named and ready to be bounded rather than hand-waved.",
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
    doc_path = ROOT / "1781-Y5-R2FR-parent-q-Dq-matrix-first-row-or-Obs-e-factorisation-proof.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1781 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
