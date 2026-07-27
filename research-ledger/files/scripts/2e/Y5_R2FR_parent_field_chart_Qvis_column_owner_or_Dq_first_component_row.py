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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1782"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1782_0_1781_handoff",
        "source_key": "1781_handoff_doc",
        "source_path": ROOT / "1781-Y5-R2FR-parent-q-Dq-matrix-first-row-or-Obs-e-factorisation-proof.md",
        "needles": ["QDM1781_0_parent_field_chart", "QDM1781_1_Qvis_column_contract", "NEXT1781_0_primary"],
    },
    {
        "source_id": "SRC1782_1_1781_validation",
        "source_key": "1781_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1781_VALIDATION.csv",
        "needles": ["VAL1781_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1782_2_1781_matrix_gate",
        "source_key": "1781_q_dq_matrix_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_Q_DQ_MATRIX_GATE.csv",
        "needles": ["QDM1781_0_parent_field_chart", "QDM1781_7_verdict"],
    },
    {
        "source_id": "SRC1782_3_1781_first_rows",
        "source_key": "1781_dq_obs_first_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1781_DQ_OBS_E_FIRST_ROW_SCHEMA.csv",
        "needles": ["DQR1781_0_Dq_Z_Qvis", "DQR1781_5_total_q_dq_obs_abs"],
    },
    {
        "source_id": "SRC1782_4_1667_field_chart",
        "source_key": "1667_parent_field_chart",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
        "needles": ["PFC1667_0_visible_quotient", "PFC1667_7_chart_verdict"],
    },
    {
        "source_id": "SRC1782_5_1674_qz_ansatz",
        "source_key": "1674_parent_q_z_ansatz",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv",
        "needles": ["QANS1674_0_parent_chart", "QANS1674_1_visible_quotient", "QANS1674_4_constraint_first_route"],
    },
    {
        "source_id": "SRC1782_6_1737_q_map",
        "source_key": "1737_q_map_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
        "needles": ["QMAP1737_0_Q_vis", "QMAP1737_5_Z_phi_RAB", "QMAP1737_6_boundary_projector"],
    },
    {
        "source_id": "SRC1782_7_1737_vertical_basis",
        "source_key": "1737_vertical_basis_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
        "needles": ["VB1737_0_vZ", "VB1737_5_vtau_readout"],
    },
    {
        "source_id": "SRC1782_8_1737_dq_requirements",
        "source_key": "1737_dq_matrix_requirements",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
        "needles": ["DQM1737_0_DObs_e", "DQM1737_5_Dq_total_kernel"],
    },
    {
        "source_id": "SRC1782_9_1675_coframe_descent",
        "source_key": "1675_coframe_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_COFRAME_DESCENT_GATE.csv",
        "needles": ["CDG1675_0_obs_functor", "CDG1675_3_verdict"],
    },
    {
        "source_id": "SRC1782_10_1675_source_readout",
        "source_key": "1675_source_readout_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
        "needles": ["SRD1675_0_matter_domain", "SRD1675_5_verdict"],
    },
    {
        "source_id": "SRC1782_11_1720_matter_functor",
        "source_key": "1720_matter_functor_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
    },
    {
        "source_id": "SRC1782_12_1760_premise",
        "source_key": "1760_descent_premise",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_DESCENT_PREMISE_AUDIT.csv",
        "needles": ["PRE1760_0_q_map", "PRE1760_8_verdict"],
    },
    {
        "source_id": "SRC1782_13_1760_descent",
        "source_key": "1760_matter_worldtube_descent",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1760_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv",
        "needles": ["MWD1760_1_conditional_theorem", "MWD1760_4_current_verdict"],
    },
    {
        "source_id": "SRC1782_14_1739_coframe_owner",
        "source_key": "1739_parent_coframe_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
        "needles": ["PCO1739_0_parent_q", "PCO1739_8_tau_source_normal_lock"],
    },
    {
        "source_id": "SRC1782_15_1740_shadow_frame",
        "source_key": "1740_no_shadow_frame",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
        "needles": ["NSF1740_0_parent_matter_domain", "NSF1740_6_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_SOURCE_REGISTER.csv",
    "field_chart_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_FIELD_CHART_OWNER_GATE.csv",
    "qvis_column_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_QVIS_COLUMN_OWNER_MATRIX.csv",
    "column_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_COLUMN_DESCENT_THEOREM_ATTEMPT.csv",
    "dq_first_component": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_DQ_FIRST_COMPONENT_ROW_SCHEMA.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1782_VALIDATION.csv",
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
                "role": "1782 parent field-chart and Q_vis column-owner evidence",
            }
        )
    return rows


def field_chart_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_0_parent_action_chart",
            "clause": "parent action declares the field chart before readout",
            "mathematical_form": "S_parent[Phi_parent] with Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc)",
            "source_basis": "PFC1667_7_chart_verdict;QANS1674_0_parent_chart;QDM1781_0_parent_field_chart",
            "current_status": "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED",
            "blocking_issue": "chart is useful for testing, but not adopted by an action or theorem-equivalent coordinate construction",
            "exit_condition": "parent action or derived quotient construction names all chart blocks and gauge redundancies",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_1_chart_version_consistency",
            "clause": "chart versions agree on owned gauge/constants block",
            "mathematical_form": "1667 Phi_parent omits A_owned while 1674 includes A_owned in Phi_parent and Q_vis",
            "source_basis": "PFC1667_7_chart_verdict;QANS1674_0_parent_chart;QANS1674_1_visible_quotient",
            "current_status": "CHART_VERSION_MISMATCH_A_OWNED_UNSIGNED",
            "blocking_issue": "Dq columns cannot be final while gauge/charge-owned variables are inconsistently placed",
            "exit_condition": "single canonical chart states whether A_owned is parent field, quotient data, fixed representation data, or residual row",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_2_ordinary_matter_domain",
            "clause": "ordinary matter fields are sections over the owned observed quotient",
            "mathematical_form": "Psi_A in Sec(E_A[e_obs(Q_vis)]), theta_A quotient-owned or finite residual",
            "source_basis": "PFC1667_5_matter_block;SRD1675_0_matter_domain;MFS1720_2_ordinary_matter_functor",
            "current_status": "MATTER_DOMAIN_UNSIGNED",
            "blocking_issue": "fixed/gauge vertical lift remains a convention rather than a parent theorem",
            "exit_condition": "matter category, vertical lift, constants, and representation data are parent-owned",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_3_residual_exclusion_grammar",
            "clause": "residual variables are excluded from Q_vis only by constraint, symmetry, or finite row",
            "mathematical_form": "R_phys,Z,phi,R_AB,J_q not in Q_vis iff C_X=0 before q or Dq_X=0 on all columns",
            "source_basis": "QANS1674_2_residual_vector;QANS1674_4_constraint_first_route;QMAP1737_5_Z_phi_RAB",
            "current_status": "RESIDUAL_EXCLUSION_NOT_DERIVED",
            "blocking_issue": "exclusion is currently a contract, not a derived quotient theorem",
            "exit_condition": "constraint-first/no-pole theorem or source-backed Dq_X component rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_4_boundary_support",
            "clause": "boundary, collar, projector, and source support are q-basic or finite residuals",
            "mathematical_form": "B_edge,P_loc,Q_X either descend through Q_vis or are retained in Dboundary/Dsource rows",
            "source_basis": "PFC1667_6_boundary_block;QMAP1737_6_boundary_projector;PRE1760_6_boundary",
            "current_status": "BOUNDARY_BLOCK_OPEN",
            "blocking_issue": "boundary/projector/source support can reopen local source coupling",
            "exit_condition": "boundary/projector descent theorem or finite boundary-source rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_5_tau_source_normal_lock",
            "clause": "tau and source normal are chart-owned roles, not post-fit readout choices",
            "mathematical_form": "Dq(L_tau Phi)=L_tau_red q(Phi) and tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "source_basis": "MFS1720_5_tau_source_normal_lock;PCO1739_8_tau_source_normal_lock;DQM1737_4_Dtau_pushforward",
            "current_status": "TAU_SOURCE_NORMAL_LOCK_UNSIGNED",
            "blocking_issue": "time/source/charge/orbit roles can split even if the coframe is shared",
            "exit_condition": "tau projectability plus role-lock theorem or finite tau mismatch rows",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "FCO1782_6_verdict",
            "clause": "parent field chart is owned",
            "mathematical_form": "FCO1782_0 through FCO1782_5 pass in one parent branch",
            "source_basis": "1667/1674/1720/1737/1739/1760/1781",
            "current_status": "PARENT_FIELD_CHART_NOT_OWNED",
            "blocking_issue": "chart, quotient, residual exclusion, matter domain, boundary, and tau roles are not signed together",
            "exit_condition": "one parent-owned chart or theorem-equivalent quotient construction",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qvis_column_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_0_e_obs_g_obs",
            "q_column": "e_obs,g_obs",
            "proposed_owner": "observed geometry carrier",
            "include_in_Qvis": True,
            "exclude_from_Qvis": False,
            "ownership_test": "e_obs=E(Q_vis), g_obs=e_obs^T eta e_obs, with no direct residual/common-frame argument",
            "current_status": "PARTIAL_ALIGNMENT_NOT_ACTION_OWNED",
            "source_basis": "QMAP1737_1_e_obs;CDG1675_0_obs_functor;PCO1739_1_metric_coframe_owner",
            "Dq_consequence": "DObs_e[v]=0 only if Obs_e(q) and no common-frame derivative",
            "finite_fallback": "DObs_e_Dq_leak;b_g_X",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_1_measure_connection",
            "q_column": "mu_m,D_m,omega_matter",
            "proposed_owner": "measure, derivative, and connection stack",
            "include_in_Qvis": True,
            "exclude_from_Qvis": False,
            "ownership_test": "mu_m and omega_matter descend from e_obs or owned gauge data only",
            "current_status": "MISSING_CONNECTION_DESCENT_AND_MEASURE_OWNERSHIP",
            "source_basis": "CDG1675_1_metric_connection;CDG1675_2_measure;PCO1739_3_connection_lock",
            "Dq_consequence": "connection/measure source terms can survive if not owned by e_obs",
            "finite_fallback": "Dconnection_Dq_leak;Dmeasure_Dq_leak",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_2_source_readout",
            "q_column": "source, clock, photon, ruler, orbit, detector, boundary readout data",
            "proposed_owner": "ordinary observable readout functor",
            "include_in_Qvis": True,
            "exclude_from_Qvis": False,
            "ownership_test": "all readouts are functions of Q_vis and owned gauge/constant data",
            "current_status": "READOUT_FUNCTOR_NOT_PARENT_SIGNED",
            "source_basis": "QMAP1737_2_source_readout;SRD1675_4_readouts;PRE1760_5_worldtube_support",
            "Dq_consequence": "source/readout leakage remains even if coframe leakage vanishes",
            "finite_fallback": "Dsource_readout_Dq_leak",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_3_theta_owned",
            "q_column": "theta_A, masses, charge units, clock constants, material labels",
            "proposed_owner": "ordinary constants and material standards",
            "include_in_Qvis": True,
            "exclude_from_Qvis": False,
            "ownership_test": "Lie_v theta_A=0 or finite marker rows are declared",
            "current_status": "CONSTANT_OWNER_UNSIGNED",
            "source_basis": "QMAP1737_3_theta_owned;SRD1675_2_constants_markers;MFS1720_4_constants_and_material_standards",
            "Dq_consequence": "WEP, clock, EM, and source-normal residuals survive if constants drift",
            "finite_fallback": "Dtheta_marker_Dq_leak",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_4_A_owned",
            "q_column": "A_owned or owned gauge/charge representation data",
            "proposed_owner": "owned gauge field or fixed representation sector",
            "include_in_Qvis": "candidate_in_1674",
            "exclude_from_Qvis": "not_decided_in_1667",
            "ownership_test": "A_owned is either parent field, quotient data, fixed representation data, or retained residual with no mixed status",
            "current_status": "A_OWNED_PLACEMENT_UNSIGNED",
            "source_basis": "QANS1674_0_parent_chart;QANS1674_1_visible_quotient;FCO1782_1_chart_version_consistency",
            "Dq_consequence": "charge/EM/gauge coupling column cannot be finalized",
            "finite_fallback": "D_A_owned_Dq_or_charge_unit_row",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_5_R_phys_exclusion",
            "q_column": "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling,boundary,coupling}",
            "proposed_owner": "diagnostic residual vector, not ordinary quotient data",
            "include_in_Qvis": False,
            "exclude_from_Qvis": True,
            "ownership_test": "R_phys is excluded only if constraints remove it or finite observable rows carry it",
            "current_status": "RESIDUAL_VECTOR_NOT_PARENT_LOCKED",
            "source_basis": "PFC1667_2_residual_block;QANS1674_2_residual_vector;QMAP1737_4_R_phys",
            "Dq_consequence": "if R_phys enters q, local residuals are visible rather than vertical",
            "finite_fallback": "R_phys_to_observable_projection_rows",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_6_Z_phi_RAB_exclusion",
            "q_column": "Z,phi,R_AB,J_q",
            "proposed_owner": "candidate vertical/auxiliary directions",
            "include_in_Qvis": False,
            "exclude_from_Qvis": "true_if_constraint_or_Dq_zero",
            "ownership_test": "Dq[partial_Z], Dq[partial_phi], and Dq[partial_RAB/Jq] are zero or variables are constraint-eliminated",
            "current_status": "AUXILIARY_VERTICAL_STATUS_UNSIGNED",
            "source_basis": "QMAP1737_5_Z_phi_RAB;VB1737_0_vZ;VB1737_1_vphi;VB1737_2_vRAB_Jq",
            "Dq_consequence": "cannot call these vertical while Dq component rows are missing",
            "finite_fallback": "Dq_Z_Qvis;Dq_phi_Qvis;Dq_RAB_Jq_Qvis",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_7_boundary_projector",
            "q_column": "B_edge,P_loc,Q_X",
            "proposed_owner": "boundary/projector/source-measure block",
            "include_in_Qvis": "partly_if_readout_visible",
            "exclude_from_Qvis": "partly_if_basic_boundary",
            "ownership_test": "boundary terms are q-basic or retained as finite boundary/source residuals",
            "current_status": "BOUNDARY_BLOCK_OPEN",
            "source_basis": "QMAP1737_6_boundary_projector;VB1737_3_vboundary;PRE1760_6_boundary",
            "Dq_consequence": "boundary/projector can reopen local source coupling",
            "finite_fallback": "Dboundary_projector_Dq_leak",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_8_tau_roles",
            "q_column": "tau_source,tau_charge,tau_clock,tau_orbit,tau_boundary",
            "proposed_owner": "projectable observed-time/source-normal role",
            "include_in_Qvis": "role_or_pushforward_column",
            "exclude_from_Qvis": False,
            "ownership_test": "Dq(L_tau Phi)=L_tau_red q(Phi) and all tau roles lock",
            "current_status": "TAU_SOURCE_NORMAL_LOCK_UNSIGNED",
            "source_basis": "DQM1737_4_Dtau_pushforward;MFS1720_5_tau_source_normal_lock;PCO1739_8_tau_source_normal_lock",
            "Dq_consequence": "same geometry can still have mismatched source/clock/orbit generators",
            "finite_fallback": "Delta_tau_role_lock",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "column_id": "QCO1782_9_verdict",
            "q_column": "canonical Q_vis column owner matrix",
            "proposed_owner": "one parent branch",
            "include_in_Qvis": "not_final",
            "exclude_from_Qvis": "not_final",
            "ownership_test": "QCO1782_0 through QCO1782_8 are signed or finite",
            "current_status": "QVIS_COLUMN_OWNER_NOT_SIGNED",
            "source_basis": "field chart gate plus q map/descent/signature sources",
            "Dq_consequence": "Dq matrix remains nonclaim",
            "finite_fallback": "Dq first component rows",
            "parent_signed": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def column_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CDT1782_0_pullback_column_owner",
            "claim": "Q_vis columns are parent-owned if ordinary matter is a pullback along q",
            "mathematical_form": "S_ord[Phi,Psi]=Sbar_ord[Psi,q(Phi)] and q(Phi)=Q_vis before readout",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent action chart, unique q map, matter category, and no-shadow/source-prefactor clauses",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CDT1782_1_residual_exclusion_rule",
            "claim": "residual variables may be excluded from Q_vis only by constraint/symmetry or finite Dq row",
            "mathematical_form": "X notin Q_vis is claim-safe iff C_X(Phi)=0 before q, X is pure gauge, or every Dq_i[partial_X] is zero/source-bounded",
            "proof_status": "EXACT_RULE_CONTRACT",
            "missing_for_current_claim": "constraint-first theorem and Dq component values",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CDT1782_2_first_component_law",
            "claim": "first Dq component row is forced when Q_vis ownership fails",
            "mathematical_form": "Dq_Z[e_obs]=0 cannot be inferred from naming; require e_obs=E(Q_vis) with partial_Z Q_vis=0, or retain ||Dq_Z[e_obs]||",
            "proof_status": "RESIDUAL_ROW_RULE_STAGED",
            "missing_for_current_claim": "e_obs owner, Z basis, component norm, and source path",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CDT1782_3_current_verdict",
            "claim": "current MTS owns the field chart and Q_vis columns",
            "mathematical_form": "FCO1782_0 through FCO1782_6 and QCO1782_0 through QCO1782_9 pass",
            "proof_status": "FAIL_CURRENT_PARENT_PROOF",
            "missing_for_current_claim": "field chart, column ownership, residual exclusion, readout, constants, boundary, and tau role-lock",
            "valid_for_claim": False,
        },
    ]


def dq_first_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_0_DqZ_e_obs",
            "component": "Dq_Z[e_obs,g_obs]",
            "direction": "v_Z=partial_Z",
            "zero_condition": "e_obs and g_obs descend through Q_vis and Q_vis excludes Z by constraint/symmetry",
            "finite_formula": "epsilon_Z_geom := ||D_Z e_obs|| + ||D_Z g_obs||",
            "required_inputs": "Z basis;e_obs owner;metric/coframe norm;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "coframe_metric_component_norm_MISSING",
            "source_anchor": "QCO1782_0_e_obs_g_obs;DQM1737_0_DObs_e;DQR1781_1_DObs_e_vZ",
            "current_status": "RETAINED_NONCLAIM_FIRST_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_1_DqZ_measure_connection",
            "component": "Dq_Z[mu_m,D_m,omega_matter]",
            "direction": "v_Z=partial_Z",
            "zero_condition": "measure and connection are owned by e_obs or fixed gauge data",
            "finite_formula": "epsilon_Z_conn := ||D_Z mu_m|| + ||D_Z D_m|| + ||D_Z omega_matter||",
            "required_inputs": "measure owner;connection lock;norm;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "connection_measure_norm_MISSING",
            "source_anchor": "QCO1782_1_measure_connection;CDG1675_1_metric_connection;CDG1675_2_measure",
            "current_status": "RETAINED_NONCLAIM_FIRST_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_2_DqZ_source_readout",
            "component": "Dq_Z[source/readout]",
            "direction": "v_Z=partial_Z",
            "zero_condition": "source, clock, photon, orbit, detector, and boundary readouts descend through Q_vis",
            "finite_formula": "epsilon_Z_readout := ||Dsource||+||Dclock||+||Dorbit||+||Dphoton||+||Ddetector||+||Dboundary||",
            "required_inputs": "readout functor;arena projection;component norm;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "readout_component_norm_MISSING",
            "source_anchor": "QCO1782_2_source_readout;SRD1675_4_readouts;DQR1781_2_Dsource_readout_vZ",
            "current_status": "RETAINED_NONCLAIM_FIRST_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_3_DqZ_theta_A",
            "component": "Dq_Z[theta_A]",
            "direction": "v_Z=partial_Z",
            "zero_condition": "ordinary constants/material labels are quotient-owned and Lie_Z theta_A=0",
            "finite_formula": "epsilon_Z_theta := sum_A ||Lie_Z theta_A||",
            "required_inputs": "constant superselection;material label owner;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_marker_norm_MISSING",
            "source_anchor": "QCO1782_3_theta_owned;MFS1720_4_constants_and_material_standards;DQR1781_3_Dtheta_marker_vZ",
            "current_status": "RETAINED_NONCLAIM_FIRST_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_4_DqZ_boundary_tau",
            "component": "Dq_Z[boundary/projector/tau]",
            "direction": "v_Z=partial_Z",
            "zero_condition": "boundary/projector data are q-basic and tau is projectable/role-locked",
            "finite_formula": "epsilon_Z_boundary_tau := ||Dboundary||+||Dprojector||+||Dq(L_tau Phi)-L_tau_red q(Phi)||",
            "required_inputs": "boundary descent;tau projectability;role lock;source path",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "boundary_tau_norm_MISSING",
            "source_anchor": "QCO1782_7_boundary_projector;QCO1782_8_tau_roles;DQR1781_4_Dboundary_projector_vZ",
            "current_status": "RETAINED_NONCLAIM_FIRST_COMPONENT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQF1782_5_total_DqZ_abs",
            "component": "epsilon_DqZ_Qvis_abs",
            "direction": "v_Z=partial_Z",
            "zero_condition": "all DQF1782_0 through DQF1782_4 vanish in the same parent chart",
            "finite_formula": "abs(DQF1782_0)+abs(DQF1782_1)+abs(DQF1782_2)+abs(DQF1782_3)+abs(DQF1782_4)",
            "required_inputs": "all component values;common normalizer;source paths;no-cancellation flag",
            "current_value": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "units": "common_dimensionless_or_declared_norm_MISSING",
            "source_anchor": "DQR1781_5_total_q_dq_obs_abs;DQM1737_5_Dq_total_kernel",
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
            "countermodel_id": "CM1782_0_chart_extension",
            "countermodel": "adding or moving A_owned changes charge/gauge columns without altering the old verbal q map",
            "survives_current_constraints": True,
            "why_survives": "1667 and 1674 use slightly different chart content",
            "what_kills_it": "single canonical parent chart with A_owned placement theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1782_1_residual_common_frame",
            "countermodel": "residual X is excluded from Q_vis but e_obs still carries exp(b_g X)",
            "survives_current_constraints": True,
            "why_survives": "exclusion from column names is weaker than no common-frame derivative",
            "what_kills_it": "Obs_e(q) theorem plus b_g,X=0 or finite b_g row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1782_2_readout_postmap",
            "countermodel": "readout maps apply an X-dependent source/clock/orbit projection after e_obs is constructed",
            "survives_current_constraints": True,
            "why_survives": "source/readout column ownership is unsigned",
            "what_kills_it": "one Q_vis readout functor or finite readout leakage row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1782_3_constant_marker",
            "countermodel": "masses, charge units, or material labels vary along a residual direction while geometry is unchanged",
            "survives_current_constraints": True,
            "why_survives": "theta_A owner/superselection is unsigned",
            "what_kills_it": "Lie_v theta_A=0 theorem or finite marker row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1782_4_boundary_tau_reentry",
            "countermodel": "boundary/projector support or tau role choices re-enter local source tests after the quotient",
            "survives_current_constraints": True,
            "why_survives": "boundary and tau columns are not parent-owned",
            "what_kills_it": "boundary q-basic theorem and tau pushforward role-lock certificate",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1782_0_field_chart",
            "claim": "parent field chart is owned",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "FCO1782_6 remains PARENT_FIELD_CHART_NOT_OWNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1782_1_qvis_columns",
            "claim": "canonical Q_vis column owner matrix is signed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "QCO1782_9 remains QVIS_COLUMN_OWNER_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1782_2_DqZ_first_component",
            "claim": "Dq_Z first component is zero or source-backed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "DQF1782 rows contain MISSING_NUMERIC_OR_THEOREM_ZERO and missing common norm",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1782_3_local_gr",
            "claim": "local GR/Newton/PPN/R10 follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "local reduction still depends on q/Dq/column ownership and residual exclusion",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1782_0_exact_result",
            "decision": "COLUMN_OWNER_PULLBACK_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "if ordinary matter is a pullback along q, then Q_vis columns are parent-owned by construction",
            "next_action": "keep as theorem contract, not a current claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1782_1_current_status",
            "decision": "PARENT_FIELD_CHART_AND_QVIS_COLUMNS_NOT_SIGNED",
            "reason": "chart consistency, residual exclusion, matter domain, readout, constants, boundary, and tau role-lock remain unsigned",
            "next_action": "do not promote Dq=0 or local-GR recovery",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1782_2_first_row",
            "decision": "DQ_Z_FIRST_COMPONENT_ROWS_STAGED_NONCLAIM",
            "reason": "failed column ownership has been converted into explicit Dq_Z component rows",
            "next_action": "fill no row without source path, units, norm, and no-cancellation rule",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1782_3_best_next",
            "decision": "CONSTRAINT_FIRST_RESIDUAL_EXCLUSION_OR_DQZ_COMPONENT_PROOF_IS_NEXT",
            "reason": "the least-scrutiny route is to derive C_Z=0/C_phi=0 before q; otherwise the first Dq_Z component must be bounded",
            "next_action": "build 1783 constraint-first residual-exclusion proof gate or Dq_Z[e_obs] component row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1782_0_primary",
            "next_target": "1783-Y5-R2FR-constraint-first-residual-exclusion-or-DqZ-component-proof.md",
            "script": "scripts/Y5_R2FR_constraint_first_residual_exclusion_or_DqZ_component_proof.py",
            "objective": "try to derive residual exclusion C_Z=0/C_phi=0 before q; if not, stage Dq_Z[e_obs] as the first finite component row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1782_1_parallel",
            "next_target": "1783b-Y5-R2FR-A-owned-charge-gauge-column-placement-gate.md",
            "script": "scripts/Y5_R2FR_A_owned_charge_gauge_column_placement_gate.py",
            "objective": "resolve whether A_owned is parent field, quotient data, fixed representation data, or residual row",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1782_2_later",
            "next_target": "1784-Y5-R2FR-source-readout-column-functor-or-finite-readout-row.md",
            "script": "scripts/Y5_R2FR_source_readout_column_functor_or_finite_readout_row.py",
            "objective": "attack source/clock/orbit/readout descent after residual exclusion is sharper",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "field_chart_gate": field_chart_gate_rows(),
        "qvis_column_matrix": qvis_column_matrix_rows(),
        "column_theorem": column_theorem_rows(),
        "dq_first_component": dq_first_component_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1782_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1782_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1782-Y5-R2FR-parent-field-chart-Qvis-column-owner-or-Dq-first-component-row.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1782_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1782_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1782_2_field_chart_gate_complete",
            any(row["gate_id"] == "FCO1782_6_verdict" for row in rows_map["field_chart_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["field_chart_gate"]),
            "field-chart owner gate is complete and nonclaim",
        ),
        (
            "VAL1782_3_qvis_matrix_complete",
            any(row["column_id"] == "QCO1782_9_verdict" for row in rows_map["qvis_column_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["qvis_column_matrix"]),
            "Q_vis column owner matrix is complete and nonclaim",
        ),
        (
            "VAL1782_4_pullback_theorem_written",
            any(row["theorem_id"] == "CDT1782_0_pullback_column_owner" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["column_theorem"]),
            "exact column-owner pullback theorem is written",
        ),
        (
            "VAL1782_5_current_proof_not_promoted",
            any(row["theorem_id"] == "CDT1782_3_current_verdict" and row["proof_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["column_theorem"]),
            "current field-chart/Q_vis proof remains unpromoted",
        ),
        (
            "VAL1782_6_dq_first_rows_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dq_first_component"]
            ),
            "Dq first component rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1782_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1782_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1782_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1782_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1782_11_decision_next",
            any(row["decision_id"] == "DEC1782_3_best_next" and "CONSTRAINT_FIRST" in row["decision"] for row in rows_map["decision"]),
            "decision selects constraint-first residual exclusion next",
        ),
        (
            "VAL1782_12_next_selected",
            any(row["route_id"] == "NEXT1782_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1782_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1782 CSVs parse"),
        ("VAL1782_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1782_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1782_16_formalization_untouched", formalization_untouched(), "no 1782 outputs found under formalization-workbench"),
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
            "check_id": "VAL1782_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1782 parent field-chart Q_vis column owner or Dq first component checkpoint",
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
            "# 1782 - Y5/R2FR Parent Field-Chart Q-vis Column Owner or Dq First Component Row",
            "",
            "## Verdict",
            "",
            "1782 gets more exact about what has to exist before local-GR reduction can be derived. The clean result is again conditional: if ordinary matter is literally a pullback along a parent quotient `q`, then the `Q_vis` columns are owned by construction and residual directions can be invisible only when they are constrained away, gauge, or `Dq`-zero.",
            "",
            "The current corpus does not yet sign that. The parent field chart is still candidate-only, `A_owned` placement is inconsistent between chart versions, `Q_vis` columns are not all owned, and residual exclusions are contract-level rather than theorem-level. So `Dq_Z` first-component rows are staged as nonclaim fallbacks.",
            "",
            "**Claim ceiling:** no parent chart claim, no canonical `Q_vis` owner claim, no `Dq_Z=0`, no `Obs_e(q)` promotion, no local-GR/Newton/PPN/R10 pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1782.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Field-Chart Owner Gate",
            markdown_table(rows_map["field_chart_gate"], ["gate_id", "clause", "mathematical_form", "current_status", "blocking_issue", "exit_condition", "valid_for_claim"]),
            "",
            "## Q-vis Column Owner Matrix",
            markdown_table(rows_map["qvis_column_matrix"], ["column_id", "q_column", "proposed_owner", "include_in_Qvis", "exclude_from_Qvis", "current_status", "Dq_consequence", "finite_fallback", "valid_for_claim"]),
            "",
            "## Column Descent Theorem Attempt",
            markdown_table(rows_map["column_theorem"], ["theorem_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## Dq First Component Row Schema",
            markdown_table(rows_map["dq_first_component"], ["row_id", "component", "direction", "zero_condition", "finite_formula", "current_value", "current_status", "score_ready", "valid_for_claim"]),
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
            "This is a useful failure. It says the right route is not to insist every hidden column is already owned; it is to derive a constraint-first residual exclusion. If `Z` and `phi` are removed before the quotient, the `Dq` problem shrinks. If they are live fields, then their first component rows must be bounded instead of wished away.",
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
    doc_path = ROOT / "1782-Y5-R2FR-parent-field-chart-Qvis-column-owner-or-Dq-first-component-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1782 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
