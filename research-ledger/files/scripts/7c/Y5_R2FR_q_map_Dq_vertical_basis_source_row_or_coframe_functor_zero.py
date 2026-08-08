from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1737"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1737 - q Map Dq Vertical Basis Source Row Or Coframe Functor Zero"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1737_0_1736_doc",
        "source_key": "1736_handoff_doc",
        "source_path": ROOT / "1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md",
        "needles": ["NEXT1736_0_primary", "VAL1736_OVERALL"],
    },
    {
        "source_id": "SRC1737_1_1736_proof",
        "source_key": "1736_commutator_proof_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_COMMUTATOR_PROOF_AUDIT.csv",
        "needles": ["DTC1736_0_q_explicit", "THEOREM_ZERO_NOT_SIGNED"],
    },
    {
        "source_id": "SRC1737_2_1736_finite_rows",
        "source_key": "1736_first_finite_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_FIRST_FINITE_BOUND_ROW_SCHEMA.csv",
        "needles": ["EDT1736_1_q_map_source", "MISSING_Q_MAP"],
    },
    {
        "source_id": "SRC1737_3_1667_parent_chart",
        "source_key": "1667_parent_field_chart",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
        "needles": ["PFC1667_7_chart_verdict", "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1737_4_1667_q_audit",
        "source_key": "1667_quotient_map_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
        "needles": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
    },
    {
        "source_id": "SRC1737_5_1667_Dq_tests",
        "source_key": "1667_Dq_on_Zphi_tests",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "needles": ["DQT1667_6_verdict", "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK"],
    },
    {
        "source_id": "SRC1737_6_1667_retained_Dq",
        "source_key": "1667_retained_Dq_leaks",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
        "needles": ["DQL1667_3_DObs_e", "RETAINED_NONCLAIM_DQ_LEAK_INPUT"],
    },
    {
        "source_id": "SRC1737_7_same_coframe",
        "source_key": "same_coframe_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_0_single_coframe_field", "conditional_clause_written_not_current_MTS_derived"],
    },
    {
        "source_id": "SRC1737_8_1363_bridge",
        "source_key": "1363_qObs_current_chain_bridge",
        "source_path": RESIDUALS / "P8_Y5_R10_1363_QOBS_CURRENT_CHAIN_BRIDGE_ATTEMPT.csv",
        "needles": ["BTA1363_7_verdict", "QOBS_CURRENT_CHAIN_BRIDGE_NOT_PROVED"],
    },
    {
        "source_id": "SRC1737_9_1363_obstruction",
        "source_key": "1363_bridge_obstruction_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_1363_BRIDGE_OBSTRUCTION_LEDGER.csv",
        "needles": ["BOB1363_6_matter_constants_not_q_owned", "OPEN"],
    },
    {
        "source_id": "SRC1737_10_1519_coframe_tau",
        "source_key": "1519_coframe_tau_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "needles": ["OCF1519_7_verdict", "COFRAME_TAU_LOCK_NOT_PROVED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_SOURCE_REGISTER.csv",
    "q_map_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
    "vertical_basis": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
    "dq_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
    "coframe_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
    "finite_dq_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_FINITE_DQ_SOURCE_ROWS.csv",
    "arena_gate_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_ARENA_GATE_MAP.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1737_VALIDATION.csv",
}


COPY_MAP = {
    "q_map_contract": "R2FR_1737_Q_MAP_CONTRACT.csv",
    "vertical_basis": "R2FR_1737_VERTICAL_BASIS_CONTRACT.csv",
    "dq_matrix": "R2FR_1737_DQ_MATRIX_REQUIREMENTS.csv",
    "coframe_zero": "R2FR_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
    "finite_dq_rows": "R2FR_1737_FINITE_DQ_SOURCE_ROWS.csv",
    "arena_gate_map": "R2FR_1737_ARENA_GATE_MAP.csv",
    "decision": "R2FR_1737_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1737_CLAIM_GATE.csv",
    "next_target": "R2FR_1737_NEXT_TARGET.csv",
}


Q_MAP_COMPONENTS = [
    {
        "component_id": "QMAP1737_0_Q_vis",
        "symbol": "Q_vis",
        "role": "ordinary-matter-visible quotient",
        "candidate_definition": "Q_vis=(e_obs,g_obs,source/readout data,theta_owned)",
        "include_in_q": "True",
        "exclude_from_q": no(),
        "Dq_requirement": "Dq must be computable on every retained parent tangent direction",
        "current_status": "CANDIDATE_CONTRACT_ONLY",
        "blocker": "PFC1667_7 keeps the field chart candidate not parent-signed",
    },
    {
        "component_id": "QMAP1737_1_e_obs",
        "symbol": "e_obs,g_obs",
        "role": "single observed geometry carrier",
        "candidate_definition": "g_obs=e_obs^T eta e_obs",
        "include_in_q": "True",
        "exclude_from_q": no(),
        "Dq_requirement": "DObs_e[v]=0 is required before any v can be called coframe-invisible",
        "current_status": "PARTIAL_ALIGNMENT_NOT_ACTION_OWNED",
        "blocker": "same-coframe clause is written but not derived from current MTS",
    },
    {
        "component_id": "QMAP1737_2_source_readout",
        "symbol": "source/readout",
        "role": "source, clock, photon, ruler, orbit and boundary readout data",
        "candidate_definition": "readouts are functors of e_obs and quotient-owned matter/constants",
        "include_in_q": "True",
        "exclude_from_q": no(),
        "Dq_requirement": "Dsource_readout[Dq(v)]=0 or finite source/readout row",
        "current_status": "READOUT_FUNCTOR_NOT_PARENT_SIGNED",
        "blocker": "clock/orbit/source/boundary maps are not one parent functor",
    },
    {
        "component_id": "QMAP1737_3_theta_owned",
        "symbol": "theta_A",
        "role": "ordinary constants/material labels",
        "candidate_definition": "masses, charge units, clock constants and labels are fixed quotient data",
        "include_in_q": "True",
        "exclude_from_q": no(),
        "Dq_requirement": "Dtheta_marker[Dq(v)]=0 or finite marker/coupling row",
        "current_status": "CONSTANT_OWNER_UNSIGNED",
        "blocker": "1363 obstruction keeps matter constants not q-owned",
    },
    {
        "component_id": "QMAP1737_4_R_phys",
        "symbol": "R_phys",
        "role": "physical residual vector",
        "candidate_definition": "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling,boundary,coupling}",
        "include_in_q": no(),
        "exclude_from_q": "True",
        "Dq_requirement": "residuals must either be constraint-eliminated or retained as finite observable rows",
        "current_status": "RESIDUAL_VECTOR_NOT_PARENT_LOCKED",
        "blocker": "if R_phys enters q, the local residual is visible rather than quotient-vertical",
    },
    {
        "component_id": "QMAP1737_5_Z_phi_RAB",
        "symbol": "Z,phi,R_AB,J_q",
        "role": "candidate vertical or auxiliary directions",
        "candidate_definition": "formal response/improvement/cell directions that might be invisible to ordinary matter",
        "include_in_q": no(),
        "exclude_from_q": "True_IF_Dq_ZERO_OR_CONSTRAINT_ELIMINATED",
        "Dq_requirement": "Dq[partial_Z], Dq[partial_phi], Dq[partial_RAB/Jq] must be computed",
        "current_status": "AUXILIARY_VERTICAL_STATUS_UNSIGNED",
        "blocker": "DQT1667_6 keeps Dq[Z/phi] not closed and leak rows retained",
    },
    {
        "component_id": "QMAP1737_6_boundary_projector",
        "symbol": "B_edge,P_loc,Q_X",
        "role": "boundary/projector/source-measure block",
        "candidate_definition": "compact collar, projector and source support data",
        "include_in_q": "PARTLY_IF_READOUT_VISIBLE",
        "exclude_from_q": "PARTLY_IF_BASIC_BOUNDARY",
        "Dq_requirement": "Dboundary_projector[Dq(v)]=0 or finite boundary/source residual",
        "current_status": "BOUNDARY_BLOCK_OPEN",
        "blocker": "boundary/projector leakage remains open in 1667 and 1363",
    },
]


VERTICAL_DIRECTIONS = [
    {
        "direction_id": "VB1737_0_vZ",
        "symbol": "v_Z=partial_Z",
        "intended_vertical_role": "formal response-doublet residual direction",
        "required_Dq_zero_components": "DObs_e;Dsource_readout;Dtheta_marker;Dboundary_projector;Dtau_pushforward",
        "current_status": "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK",
        "blocker": "Z can still be a shadow variable or source/readout-visible residual",
    },
    {
        "direction_id": "VB1737_1_vphi",
        "symbol": "v_phi=partial_phi",
        "intended_vertical_role": "trace-free improvement auxiliary direction",
        "required_Dq_zero_components": "DObs_e;Dsource_readout;Dtheta_marker;Dboundary_projector;Dtau_pushforward",
        "current_status": "PHI_OWNER_MISSING_DQ_NOT_COMPUTABLE",
        "blocker": "Khat algebra alone does not prove matter/readout invisibility",
    },
    {
        "direction_id": "VB1737_2_vRAB_Jq",
        "symbol": "v_RAB/Jq",
        "intended_vertical_role": "cell/radial response or observer phase-cell direction",
        "required_Dq_zero_components": "DObs_e;Dsource_readout;Dboundary_projector;Dtau_pushforward",
        "current_status": "REJECT_ZERO_CURRENT_EVIDENCE",
        "blocker": "if q contains observer radial/cell data this direction is visible",
    },
    {
        "direction_id": "VB1737_3_vboundary",
        "symbol": "v_boundary/projector",
        "intended_vertical_role": "compact boundary or projector representative variation",
        "required_Dq_zero_components": "Dboundary_projector;Dsource_readout;DObs_e;Dtheta_marker",
        "current_status": "BOUNDARY_PROJECTOR_NOT_BASIC",
        "blocker": "boundary and projector source charge can reopen local coupling",
    },
    {
        "direction_id": "VB1737_4_vtheta_marker",
        "symbol": "v_theta_marker",
        "intended_vertical_role": "material label or constant-owner variation",
        "required_Dq_zero_components": "Dtheta_marker;Dsource_readout;Dclock_constants",
        "current_status": "CONSTANT_MARKER_VERTICALITY_REJECTED_FOR_NOW",
        "blocker": "ordinary constants/material labels are not shown to descend through q",
    },
    {
        "direction_id": "VB1737_5_vtau_readout",
        "symbol": "v_tau_readout",
        "intended_vertical_role": "tau/source/clock/orbit/boundary readout mismatch direction",
        "required_Dq_zero_components": "Dtau_pushforward;Dsource_readout;Dclock_readout;Dorbit_readout",
        "current_status": "NO_PARENT_SIGNED_TAU_LOCK",
        "blocker": "one parent-selected observed-time generator is not signed",
    },
]


DQ_REQUIREMENTS = [
    {
        "dq_row_id": "DQM1737_0_DObs_e",
        "component": "DObs_e[v]",
        "meaning": "variation of the observed coframe/metric under candidate vertical directions",
        "zero_condition": "e_obs depends only on Q_vis and is invariant under v",
        "finite_fallback": "DObs_e_Dq_leak",
        "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "source_anchor": "DQL1667_3_DObs_e",
    },
    {
        "dq_row_id": "DQM1737_1_Dsource_readout",
        "component": "Dsource_readout[Dq(v)]",
        "meaning": "source, clock, orbit, photon, ruler and boundary readout leakage",
        "zero_condition": "all readout functors descend through e_obs and quotient-owned constants",
        "finite_fallback": "Dsource_readout_Dq_leak",
        "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "source_anchor": "DQL1667_4_Dsource_readout",
    },
    {
        "dq_row_id": "DQM1737_2_Dtheta_marker",
        "component": "Dtheta_marker[Dq(v)]",
        "meaning": "constants/material marker leakage",
        "zero_condition": "theta_A are fixed quotient-owned constants and not MTS/domain/source fields",
        "finite_fallback": "Dtheta_marker_Dq_leak",
        "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "source_anchor": "DQL1667_5_Dtheta_marker",
    },
    {
        "dq_row_id": "DQM1737_3_Dboundary_projector",
        "component": "Dboundary_projector[Dq(v)]",
        "meaning": "compact boundary/projector/source-measure leakage",
        "zero_condition": "boundary terms are q-basic or fixed before readout",
        "finite_fallback": "Dboundary_projector_Dq_leak",
        "status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
        "source_anchor": "DQL1667_6_boundary_projector",
    },
    {
        "dq_row_id": "DQM1737_4_Dtau_pushforward",
        "component": "Dq(L_tau Phi)-L_tau_red q(Phi)",
        "meaning": "tau pushforward mismatch",
        "zero_condition": "tau is selected on Q_vis and used by source, charge, clock, orbit and boundary sectors",
        "finite_fallback": "tau_projectability_source",
        "status": "MISSING_PARENT_TAU_LOCK",
        "source_anchor": "EDT1736_3_tau_projectability_source",
    },
    {
        "dq_row_id": "DQM1737_5_Dq_total_kernel",
        "component": "Dq[v_a]",
        "meaning": "total quotient derivative on candidate vertical basis",
        "zero_condition": "all DQM1737_0 through DQM1737_4 vanish in the same parent chart",
        "finite_fallback": "Dq_total_kernel_leak",
        "status": "DQ_KERNEL_UNSIGNED_RETAIN_FINITE_ROWS",
        "source_anchor": "DQT1667_6_verdict",
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
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
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def q_map_contract_rows() -> list[dict[str, Any]]:
    rows = []
    for component in Q_MAP_COMPONENTS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **component,
                "parent_signed": no(),
                "theorem_closed_for_claim": no(),
                "accepted_for_scoring": no(),
                "score_ready": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def vertical_basis_rows() -> list[dict[str, Any]]:
    rows = []
    for direction in VERTICAL_DIRECTIONS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **direction,
                "Dq_zero_proved": no(),
                "retained_as_finite_source_row": "True",
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def dq_matrix_rows() -> list[dict[str, Any]]:
    rows = []
    for requirement in DQ_REQUIREMENTS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                **requirement,
                "required_inputs": "parent_chart;q_map;vertical_basis;component_functor;norm;source_path",
                "parent_signed": no(),
                "numeric_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "units": "component_norm_or_declared_dimensionless_MISSING",
                "score_ready": no(),
                "valid_prediction_row": no(),
                "valid_for_claim": no(),
                "claim_allowed": no(),
            }
        )
    return rows


def coframe_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CFZ1737_0_exact_conditional",
            "claim_piece": "coframe functor kills vertical leak",
            "required_form": "e_obs=E(q(Phi)) and Dq[v]=0 imply DObs_e[v]=0",
            "mathematical_form": "DObs_e[v] = DE|_q(Dq[v]) = 0",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "why_not_claim": "current q and Dq are not computable and E(q) is not parent-action owned",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CFZ1737_1_same_coframe_lift",
            "claim_piece": "all local matter sees one coframe",
            "required_form": "e_obs := e_matter := e_source := e_clock := e_photon := e_orbit",
            "mathematical_form": "S_m=sum_A S_A[psi_A,e_obs;theta_A] with no hidden conformal/disformal/source frame",
            "result": "CONDITIONAL_CLAUSE_NOT_CURRENT_MTS_DERIVED",
            "why_not_claim": "UOC519 records the clause as written but not derived",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CFZ1737_2_marker_guard",
            "claim_piece": "constants/material labels do not reopen the killed direction",
            "required_form": "partial_v theta_A=0 and no material marker depends on MTS residuals",
            "mathematical_form": "Dtheta_marker[Dq(v)] = 0",
            "result": "CONSTANT_OWNER_UNSIGNED",
            "why_not_claim": "1363 keeps matter constants and material labels not q-owned",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CFZ1737_3_current_verdict",
            "claim_piece": "current corpus proves the coframe functor zero",
            "required_form": "CFZ1737_0 through CFZ1737_2 all pass with source paths in one parent chart",
            "mathematical_form": "DObs_e[v_a]=0 for every retained vertical v_a",
            "result": "COFRAME_FUNCTOR_ZERO_NOT_SIGNED",
            "why_not_claim": "q/Dq/vertical basis, matter constants, hidden frames and readout maps remain unsigned",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def finite_dq_rows() -> list[dict[str, Any]]:
    rows = []
    for direction in VERTICAL_DIRECTIONS:
        for requirement in DQ_REQUIREMENTS[:-1]:
            rows.append(
                {
                    "branch_id": BRANCH_ID,
                    "row_id": f"FDQ1737_{direction['direction_id'].split('_')[-1]}_{requirement['dq_row_id'].split('_')[-1]}",
                    "direction_id": direction["direction_id"],
                    "direction_symbol": direction["symbol"],
                    "dq_component": requirement["component"],
                    "source_anchor": requirement["source_anchor"],
                    "value_or_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                    "units": "component_norm_or_declared_dimensionless_MISSING",
                    "status": "RETAINED_NONCLAIM_DQ_LEAK_INPUT",
                    "source_path": "MISSING_SOURCE_PATH",
                    "accepted_for_scoring": no(),
                    "score_ready": no(),
                    "valid_prediction_row": no(),
                    "valid_for_claim": no(),
                    "claim_allowed": no(),
                }
            )
    return rows


def arena_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_gate_id": "AGM1737_0_local_metric",
            "arena": "local_GR_Newton_metric_limit",
            "needs_zero_or_bound": "DObs_e[v_a]",
            "gate_status": "BLOCKED",
            "blocker": "COFRAME_FUNCTOR_ZERO_NOT_SIGNED",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "arena_gate_id": "AGM1737_1_WEP",
            "arena": "WEP_same_frame",
            "needs_zero_or_bound": "DObs_e;Dsource_readout;Dtheta_marker",
            "gate_status": "BLOCKED",
            "blocker": "SOURCE_READOUT_AND_MARKER_DQ_ROWS_MISSING",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "arena_gate_id": "AGM1737_2_PPN",
            "arena": "PPN_gamma_beta_preferred_frame",
            "needs_zero_or_bound": "DObs_e;Dtau_pushforward;Dboundary_projector",
            "gate_status": "BLOCKED",
            "blocker": "DQ_KERNEL_AND_TAU_PUSHFORWARD_UNSIGNED",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "arena_gate_id": "AGM1737_3_R10",
            "arena": "R10_short_range",
            "needs_zero_or_bound": "Dsource_readout;Dtheta_marker;Dboundary_projector",
            "gate_status": "BLOCKED",
            "blocker": "R10_FIELD_MAP_AND_DQ_SOURCE_ROWS_MISSING",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1737_0_visible_quotient",
            "decision": "Q_VIS_CONTRACT_STAGED_NOT_SIGNED",
            "reason": "the visible quotient can be written cleanly, but current evidence keeps it a candidate rather than a parent action chart",
            "next_action": "source or derive the observed coframe functor E(q) and its kernel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1737_1_coframe_zero",
            "decision": "COFRAME_ZERO_ROUTE_IS_EXACT_CONDITIONAL",
            "reason": "if e_obs is a functor of q and Dq[v]=0, then DObs_e[v]=0 follows by the chain rule",
            "next_action": "try to prove DObs_e[v_Z], DObs_e[v_phi], and DObs_e[v_RAB/Jq] vanish",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1737_2_current_status",
            "decision": "DQ_KERNEL_NOT_CLOSED_RETAIN_FINITE_ROWS",
            "reason": "vertical directions and all component functors remain unsigned, so finite Dq rows are required",
            "next_action": "keep local claims blocked until DObs_e/source/marker/boundary/tau rows close or are bounded",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1737_3_best_next_domino",
            "decision": "TARGET_DOBS_E_KERNEL_FIRST",
            "reason": "metric/coframe invisibility is the least discretionary gate; without it there is no clean GR/Newton reduction",
            "next_action": "build observed-coframe kernel theorem or first finite DObs_e row",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1737_0_q_map",
            "claim": "q is a parent-signed quotient map",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "Q_VIS_CONTRACT_ONLY",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1737_1_vertical_basis",
            "claim": "candidate basis is vertical",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "Dq[v_a]_NOT_COMPUTED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1737_2_coframe_zero",
            "claim": "DObs_e[v_a]=0",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "COFRAME_FUNCTOR_ZERO_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1737_3_commutator_zero",
            "claim": "E_Dq_tau=0 follows from q/Dq basis",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "Dq_KERNEL_AND_TAU_PUSHFORWARD_UNSIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1737_4_local_GR_Newton",
            "claim": "local GR/Newton reduction derived from quotient geometry",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "NO_DOBS_E_ZERO_NO_SOURCE_READOUT_ZERO_NO_TAU_LOCK",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1737_0_primary",
            "next_target": "1738-Y5-R2FR-observed-coframe-kernel-zero-or-first-finite-DObs-e-row.md",
            "script": "scripts/Y5_R2FR_observed_coframe_kernel_zero_or_first_finite_DObs_e_row.py",
            "objective": "prove DObs_e[v]=0 for the candidate vertical basis from the observed coframe functor, or stage the first finite coframe leak row",
            "success_condition": "parent-signed coframe-kernel theorem or finite DObs_e row ready for local metric/WEP/PPN smoke gates",
            "selection_status": "selected",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1737_1_parallel_readout",
            "next_target": "1738b-Y5-R2FR-source-readout-marker-Dq-zero-or-finite-row.md",
            "script": "scripts/Y5_R2FR_source_readout_marker_Dq_zero_or_finite_row.py",
            "objective": "prove source/readout and material-marker functors descend through q, or keep finite leak rows",
            "success_condition": "source/readout and marker rows source-backed with units and nonclaim comparisons",
            "selection_status": "held_parallel",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1737_2_later_tau",
            "next_target": "1739-Y5-R2FR-tau-pushforward-on-qvis-or-finite-Dtau-row.md",
            "script": "scripts/Y5_R2FR_tau_pushforward_on_qvis_or_finite_Dtau_row.py",
            "objective": "prove the observed-time generator is the pushforward of one parent tau on Q_vis",
            "success_condition": "tau pushforward theorem or finite Dtau row for commutator and PPN gates",
            "selection_status": "later",
            "valid_for_claim": no(),
            "claim_allowed": no(),
            "score_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "q_map_contract": q_map_contract_rows(),
        "vertical_basis": vertical_basis_rows(),
        "dq_matrix": dq_matrix_rows(),
        "coframe_zero": coframe_zero_rows(),
        "finite_dq_rows": finite_dq_rows(),
        "arena_gate_map": arena_gate_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1737_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1737_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "accepted_for_scoring",
        "claim_allowed",
        "Dq_zero_proved",
        "gate_pass",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {
        "accepted_for_scoring",
        "claim_allowed",
        "Dq_zero_proved",
        "gate_pass",
        "parent_signed",
        "score_ready",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1737_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1737_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1737*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    source_register = rows_map["source_register"]
    q_rows = rows_map["q_map_contract"]
    vertical_rows = rows_map["vertical_basis"]
    dq_rows = rows_map["dq_matrix"]
    coframe_rows = rows_map["coframe_zero"]
    finite_rows = rows_map["finite_dq_rows"]
    arena_rows = rows_map["arena_gate_map"]
    decision = rows_map["decision"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    required_dq = {row["dq_row_id"] for row in dq_rows}
    expected_dq = {row["dq_row_id"] for row in DQ_REQUIREMENTS}

    validation = [
        check("VAL1737_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1737_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check("VAL1737_2_q_contract_complete", {row["component_id"] for row in q_rows} == {row["component_id"] for row in Q_MAP_COMPONENTS}, "q-map contract covers visible, residual, auxiliary and boundary blocks", "q-map contract missing component"),
        check("VAL1737_3_q_contract_nonclaim", all(row["parent_signed"] == "False" and row["claim_allowed"] == "False" for row in q_rows), "q-map contract remains nonclaim", "q-map contract opened a claim flag"),
        check("VAL1737_4_vertical_basis_complete", {row["direction_id"] for row in vertical_rows} == {row["direction_id"] for row in VERTICAL_DIRECTIONS}, "candidate vertical basis rows are staged", "vertical basis missing direction"),
        check("VAL1737_5_vertical_basis_nonclaim", all(row["Dq_zero_proved"] == "False" and row["valid_for_claim"] == "False" for row in vertical_rows), "no candidate basis vector is called vertical by assertion", "candidate basis vector was marked zero/claim-ready"),
        check("VAL1737_6_Dq_requirements_complete", required_dq == expected_dq, "Dq matrix requirements cover coframe, readout, marker, boundary, tau and total kernel", "Dq matrix requirements missing component"),
        check("VAL1737_7_coframe_conditional_recorded", any(row["attempt_id"] == "CFZ1737_0_exact_conditional" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in coframe_rows), "exact coframe-functor conditional theorem is recorded", "coframe conditional theorem row missing"),
        check("VAL1737_8_coframe_current_blocked", any(row["attempt_id"] == "CFZ1737_3_current_verdict" and row["result"] == "COFRAME_FUNCTOR_ZERO_NOT_SIGNED" for row in coframe_rows), "current coframe-zero claim is explicitly blocked", "coframe-zero blocked verdict missing"),
        check("VAL1737_9_finite_rows_nonclaim", all(row["status"] == "RETAINED_NONCLAIM_DQ_LEAK_INPUT" and row["valid_for_claim"] == "False" for row in finite_rows), "finite Dq rows are retained as nonclaim leak inputs", "finite Dq row became claim-ready"),
        check("VAL1737_10_arena_gates_blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in arena_rows), "arena gates remain blocked until Dq/coframe/readout/tau rows close", "arena gate opened"),
        check("VAL1737_11_decision_next_domino", any(row["decision_id"] == "DEC1737_3_best_next_domino" and row["decision"] == "TARGET_DOBS_E_KERNEL_FIRST" for row in decision), "decision selects observed-coframe kernel as next domino", "decision ledger did not select observed-coframe kernel"),
        check("VAL1737_12_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows), "all claim gates keep local claims false", "one or more claim gates opened"),
        check("VAL1737_13_no_claim_flags", no_claim_flags(rows_map), "all generated rows keep claim/no-score flags false", "one or more generated flags enabled a claim"),
        check("VAL1737_14_missing_not_ready", missing_rows_not_ready(rows_map), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready", "a missing row is marked ready"),
        check("VAL1737_15_next_selected", any(row["route_id"] == "NEXT1737_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selects observed coframe kernel zero or first finite DObs_e row", "next target missing selected primary route"),
        check("VAL1737_16_csv_parse", parsed_ok, "all generated 1737 CSVs parse", "one or more generated 1737 CSVs failed to parse"),
        check("VAL1737_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1737_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1737_19_formalization_untouched", formalization_untouched(), "no 1737 outputs found under formalization-workbench", "1737 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1737_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1737 q-map/Dq vertical-basis source row or coframe-functor zero validation" if overall else "one or more 1737 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1737 writes the visible quotient candidate `Q_vis` and the candidate vertical basis in one place.",
        "- The clean coframe route is exact as a conditional theorem: if `e_obs=E(q(Phi))` and `Dq[v]=0`, then `DObs_e[v]=0` by the chain rule.",
        "- Current MTS still cannot claim the zero because the parent `q`, `Dq`, vertical basis, constants, readout maps, and tau pushforward are not jointly signed.",
        "- Therefore all `Dq` components remain finite nonclaim source rows until derived or bounded.",
        "- No local-GR, Newton, PPN, WEP, R10, orbital, clock, or `q_loc=0` claim is made.",
        "",
        "## Why This Matters",
        "This is the least slippery local-GR gate. If a candidate residual direction changes the observed coframe, it is not invisible to GR/Newton physics. If it does not change the coframe, we still must stop source/readout, material-marker, boundary, and tau channels reopening it.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## q Map Contract",
        markdown_table(rows_map["q_map_contract"], ["component_id", "symbol", "role", "candidate_definition", "include_in_q", "exclude_from_q", "current_status", "blocker"]),
        "",
        "## Vertical Basis Contract",
        markdown_table(rows_map["vertical_basis"], ["direction_id", "symbol", "intended_vertical_role", "required_Dq_zero_components", "current_status", "blocker"]),
        "",
        "## Dq Matrix Requirements",
        markdown_table(rows_map["dq_matrix"], ["dq_row_id", "component", "meaning", "zero_condition", "finite_fallback", "status"]),
        "",
        "## Coframe Functor Zero Attempt",
        markdown_table(rows_map["coframe_zero"], ["attempt_id", "claim_piece", "mathematical_form", "result", "why_not_claim"]),
        "",
        "## Finite Dq Source Rows",
        markdown_table(rows_map["finite_dq_rows"][:12], ["row_id", "direction_symbol", "dq_component", "value_or_formula", "status", "source_path"]),
        "",
        "_Finite Dq table preview shows the first 12 rows; the CSV contains all direction/component pairs._",
        "",
        "## Arena Gate Map",
        markdown_table(rows_map["arena_gate_map"], ["arena_gate_id", "arena", "needs_zero_or_bound", "gate_status", "blocker"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The project is not cycling; it has found the local-GR hinge. The next useful theorem is smaller and harder to dodge: prove the observed coframe kernel `DObs_e[v]=0` for the candidate vertical directions. If that fails, the coframe leak becomes the first local metric residual to bound.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1737_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1737 validation FAIL")
    print("1737 validation PASS")


if __name__ == "__main__":
    main()
