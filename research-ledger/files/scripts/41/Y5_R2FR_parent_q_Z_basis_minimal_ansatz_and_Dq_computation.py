from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1674"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md"

SOURCE_FILES = {
    "1673_doc": ROOT / "1673-Y5-R2FR-DqZ-zero-theorem-or-first-factor-value-fill.md",
    "1673_validation": OUT / "P8_Y5_BRR545_1673_VALIDATION.csv",
    "1673_blockers": OUT / "P8_Y5_PARENT_QLOC_1673_DQZ_FACTOR_BLOCKER_LEDGER.csv",
    "1667_parent_chart": OUT / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
    "1667_quotient_audit": OUT / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
    "1667_dq_tests": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1620_verticality": OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
    "781_parent_action": OUT / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
    "783_field_map": OUT / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
    "590_vertical_map": OUT / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "1505_dq_tests": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
}

NEEDLES = {
    "1673_doc": ["`Dq_Z_norm=0` is **not proved**", "build the parent quotient map"],
    "1673_validation": ["VAL1673_OVERALL", "PASS"],
    "1673_blockers": ["BLK1673_0_parent_q", "MISSING_COMPUTABLE_Q_MAP"],
    "1667_parent_chart": ["PFC1667_7_chart_verdict", "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED"],
    "1667_quotient_audit": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
    "1667_dq_tests": ["DQT1667_1_Z_normal_form", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK"],
    "1620_verticality": ["QVM1620_2_constraint_first", "BEST_NEXT_DERIVATION_ROUTE"],
    "781_parent_action": ["MPC781_7_contract_verdict", "candidate_only_requires_782_consistency_gate"],
    "783_field_map": ["FM783_1_Q", "needed_but_not_owned"],
    "590_vertical_map": ["matter_readout", "not_derived"],
    "1505_dq_tests": ["DQT1505_2_apply_Dq", "MISSING_COMPUTATION"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1674_SOURCE_REGISTER.csv"
PARENT_Q_ANSATZ = OUT / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv"
Z_BASIS_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1674_Z_BASIS_CANDIDATE.csv"
DQ_COMPONENT_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
CONSTRAINT_FIRST_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1674_CONSTRAINT_FIRST_ZERO_LEDGER.csv"
CONDITIONAL_ZERO = OUT / "P8_Y5_PARENT_QLOC_1674_DQZ_CONDITIONAL_ZERO_ROW_NONCLAIM.csv"
FACTOR_VALUE_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1674_DQZ_FACTOR_VALUE_UPDATE_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1674_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1674_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1674_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1674_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_Q_ANSATZ,
    Z_BASIS_CANDIDATE,
    DQ_COMPONENT_MATRIX,
    CONSTRAINT_FIRST_LEDGER,
    CONDITIONAL_ZERO,
    FACTOR_VALUE_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_Q_ANSATZ,
    Z_BASIS_CANDIDATE,
    DQ_COMPONENT_MATRIX,
    CONSTRAINT_FIRST_LEDGER,
    CONDITIONAL_ZERO,
    FACTOR_VALUE_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    PARENT_Q_ANSATZ: [
        QUARANTINE / "PARENT_Q_Z_MINIMAL_ANSATZ_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_q_Z_minimal_ansatz_nonclaim_1674.csv",
        QUEUE / "JR1674_PARENT_Q_Z_MINIMAL_ANSATZ_NONCLAIM.csv",
    ],
    DQ_COMPONENT_MATRIX: [
        QUARANTINE / "DQZ_COMPONENT_DERIVATIVE_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_component_derivative_matrix_nonclaim_1674.csv",
        QUEUE / "JR1674_DQZ_COMPONENT_DERIVATIVE_MATRIX_NONCLAIM.csv",
    ],
    CONDITIONAL_ZERO: [
        QUARANTINE / "DQZ_CONDITIONAL_ZERO_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_conditional_zero_row_nonclaim_1674.csv",
        QUEUE / "JR1674_DQZ_CONDITIONAL_ZERO_ROW_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1674.csv",
        QUEUE / "JR1674_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"


def missing_marker(value: object) -> bool:
    return "MISSING_" in str(value) or "NOT_PARENT_SIGNED" in str(value) or "CONDITIONAL_ONLY" in str(value)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        body = text(path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[key]),
                "use_in_1674": "minimal parent q/Z ansatz and Dq computation source input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_q_ansatz_rows() -> list[dict[str, object]]:
    rows = [
        (
            "QANS1674_0_parent_chart",
            "Phi_parent",
            "Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc)",
            "inherits 1667 parent field chart candidate and 781 coupling owner contract",
            "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED",
            "defines system boundary but does not adopt it as parent action",
            False,
        ),
        (
            "QANS1674_1_visible_quotient",
            "Q_vis=q(Phi_parent)",
            "Q_vis=(e_obs,g_obs,mu_m,D_m,source/readout data,theta_owned,A_owned)",
            "ordinary matter sees one coframe/metric stack plus owned gauge constants",
            "MINIMAL_ANSATZ_NOT_PARENT_SIGNED",
            "directly excludes Z,R_phys,phi,Gamma_mem,chi,g(z) as ordinary-matter variables",
            False,
        ),
        (
            "QANS1674_2_residual_vector",
            "R_phys",
            "R_phys=(q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling,boundary,coupling)",
            "diagnostic vector for local-GR recovery, not matter-visible quotient data",
            "RESIDUAL_VECTOR_NOT_PARENT_LOCKED",
            "keeps failure modes measurable instead of deleting them",
            False,
        ),
        (
            "QANS1674_3_response_doublet",
            "Z^A",
            "Z^A candidate basis labels response-doublet/residual directions",
            "must be live tangent directions or constraint-eliminated fields",
            "MISSING_UNIFIED_Z_BASIS",
            "formal Z is not enough for Dq computation",
            False,
        ),
        (
            "QANS1674_4_constraint_first_route",
            "C_Z(Phi)=0 before q",
            "constraint/no-pole branch removes Z from the matter-visible quotient before readout",
            "1620 marks this as best next derivation route",
            "BEST_ROUTE_CONDITIONAL_ONLY",
            "this is the least-scrutiny route if parent-signed",
            True,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ansatz_id": ansatz_id,
            "object": object_name,
            "minimal_definition": definition,
            "source_basis": basis,
            "status": status,
            "interpretation": interpretation,
            "selected_as_best_route": selected,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ansatz_id, object_name, definition, basis, status, interpretation, selected in rows
    ]


def z_basis_candidate_rows() -> list[dict[str, object]]:
    rows = [
        ("ZB1674_0_q", "Z_q", "q_loc vector residual direction", "q_loc^nu/q_*", "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER"),
        ("ZB1674_1_Y5", "Z_mu", "measured-GM/source normalization residual", "Delta(GM)_measured/(GM)_GR", "SOURCE_CURRENT_ZERO_NOT_DERIVED"),
        ("ZB1674_2_Y6", "Z_T", "extra local stress/exterior metric residual", "DeltaT_extra/T_*", "CONSERVERVED_KERNEL_CAN_BE_VISIBLE"),
        ("ZB1674_3_PPN", "Z_PPN", "full PPN residual vector", "DeltaPPN_A", "NO_RESPONSE_OPERATOR"),
        ("ZB1674_4_boundary", "Z_H", "boundary/harmonic/source-measure residual", "q_H or boundary flux amplitude", "BOUNDARY_PROJECTOR_OPEN"),
        ("ZB1674_5_coupling", "Z_c", "matter/source/readout coupling residual", "DeltaCoupling_A", "MATTER_SOURCE_DESCENT_MISSING"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "basis_id": basis_id,
            "basis_symbol": symbol,
            "physical_channel": channel,
            "candidate_component": component,
            "current_blocker": blocker,
            "basis_status": "CANDIDATE_NOT_LIVE_PARENT_BASIS",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for basis_id, symbol, channel, component, blocker in rows
    ]


def dq_component_matrix_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DQM1674_0_coframe_metric",
            "Dq_Z[e_obs,g_obs,mu_m,D_m]",
            "partial_Z e_obs, partial_Z g_obs, partial_Z connection/measure",
            "FORMALLY_ZERO_ONLY_IF_Q_VIS_EXCLUDES_Z_AND_E_OBS_FUNCTOR_IS_Z_SILENT",
            "MISSING_OBSERVED_COFRAME_FUNCTOR",
            "not_computed",
        ),
        (
            "DQM1674_1_source_current",
            "Dq_Z[source normalization/J_H]",
            "partial_Z measured source strength and Hilbert/Gauss calibration",
            "NOT_ZERO_ON_CURRENT_EVIDENCE",
            "SOURCE_CURRENT_ZERO_NOT_DERIVED",
            "retained_leak",
        ),
        (
            "DQM1674_2_readouts",
            "Dq_Z[clock/photon/orbit/EM/PPN readouts]",
            "partial_Z O_i and readout functional R_i",
            "FORMALLY_ZERO_ONLY_IF_READOUTS_DESCEND_THROUGH_Q_VIS",
            "MISSING_READOUT_DESCENT",
            "not_computed",
        ),
        (
            "DQM1674_3_boundary_projector",
            "Dq_Z[B_edge,P_loc,Q_X]",
            "partial_Z boundary/corner/projector/source-measure terms",
            "NOT_ZERO_OR_UNPROVED",
            "BOUNDARY_PROJECTOR_OPEN",
            "retained_leak",
        ),
        (
            "DQM1674_4_residual_lock",
            "Dq_Z[R_phys -> observed residuals]",
            "physical response matrix from selected Z basis to q_loc/Y5/Y6/PPN/boundary/coupling",
            "NOT_COMPUTED",
            "COMPONENT_MAP_NOT_CLOSED",
            "not_computed",
        ),
        (
            "DQM1674_5_operator_norm",
            "Dq_Z_norm",
            "operator norm of the component derivative matrix",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "MISSING_Q_Z_NORMS_AND_DQ_MATRIX",
            "not_filled",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "matrix_row_id": row_id,
            "component": component,
            "derivative_object": derivative,
            "conditional_status": conditional,
            "blocking_issue": blocker,
            "computation_status": status,
            "computed_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, component, derivative, conditional, blocker, status in rows
    ]


def constraint_first_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CFZ1674_0_parent_constraint",
            "C_Z(Phi)=0 or no-pole regularity eliminates Z before q is formed",
            "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "write the parent action/constraint multiplier and show it is not a post-hoc gauge choice",
        ),
        (
            "CFZ1674_1_constraint_tangent",
            "allowed tangent variations satisfy delta C_Z=0 and contain no physical q/readout variation",
            "MISSING_TANGENT_SPACE_PROOF",
            "derive tangent-space projection from parent Euler/constraint equations",
        ),
        (
            "CFZ1674_2_q_factorization",
            "q(Phi)|C_Z=0 = qbar(Q_vis) with no Z argument",
            "MISSING_Q_FACTORISATION_PROOF",
            "show every q component descends through Q_vis after constraints",
        ),
        (
            "CFZ1674_3_source_readout",
            "S_matter, source current, clocks, photons, EM, and orbit readouts use Q_vis only",
            "MISSING_MATTER_SOURCE_READOUT_DESCENT",
            "derive quotient-invariant action/readout functor",
        ),
        (
            "CFZ1674_4_boundary",
            "boundary/projector/source-measure flux is zero or in Q_vis before Dq_Z is evaluated",
            "MISSING_BOUNDARY_NO_FLUX",
            "prove compact-local no-flux or keep finite boundary factor",
        ),
        (
            "CFZ1674_5_verdict",
            "Dq_Z_norm=0 from constraint-first branch",
            "CONSTRAINT_FIRST_ZERO_NOT_PROVED",
            "continue to coframe/source/readout descent rather than claiming local GR",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "required_clause": clause,
            "status": status,
            "next_action": action,
            "clause_met": False,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, status, action in rows
    ]


def conditional_zero_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CZ1674_0_conditional_zero",
            "symbol": "Dq_Z_norm",
            "conditional_value": "0",
            "condition": "C_Z eliminates Z before q, e_obs/source/readout/boundary descend through Q_vis, and q/Z norms are declared",
            "current_status": "CONDITIONAL_ONLY_NOT_PARENT_SIGNED",
            "accepted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "reason_not_accepted": "constraint-first, coframe functor, source/readout descent, and boundary silence are not derived",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def factor_update_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQZVAL1674_0_update",
            "symbol": "Dq_Z_norm",
            "previous_status": "BLOCKED_NO_THEOREM_ZERO_OR_FINITE_VALUE",
            "new_information": "minimal q/Z ansatz makes the exact derivative matrix explicit and selects constraint-first as least-scrutiny route",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "projection_formula": "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "current_status": "STRUCTURE_CLARIFIED_VALUE_STILL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1674_0_q_ansatz",
            "MINIMAL_Q_Z_ANSATZ_WRITTEN",
            "we now have a concrete visible quotient boundary and candidate Z basis to attack",
            "treat it as a contract, not a theorem",
        ),
        (
            "D1674_1_Dq_matrix",
            "DQ_MATRIX_NOT_COMPUTED",
            "component derivative rows show exactly which hidden wires can still leak into q",
            "derive coframe/source/readout/boundary silence or retain finite leak factors",
        ),
        (
            "D1674_2_best_route",
            "CONSTRAINT_FIRST_SELECTED",
            "removing Z before matter/readout sees it is stronger than declaring visible data gauge after the fact",
            "try to sign the constraint/no-pole branch next",
        ),
        (
            "D1674_3_safety",
            "NO_GR_NEWTON_CLAIM",
            "conditional zero row is not adopted and Dq_Z_norm remains missing",
            "keep all local claim gates false",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1674_0_parent_q", "minimal q(Phi) ansatz is parent-signed", False, "BLOCKED", "ansatz only"),
        ("CG1674_1_Z_basis", "selected Z basis is a live parent tangent basis", False, "BLOCKED", "candidate not live parent basis"),
        ("CG1674_2_Dq", "Dq[Z] is computed or theorem-zero", False, "BLOCKED", "component derivative matrix is missing"),
        ("CG1674_3_constraint", "constraint-first zero route is parent-signed", False, "BLOCKED", "constraint/no-pole origin missing"),
        ("CG1674_4_local_GR", "local GR/Newton reduction follows", False, "BLOCKED", "no Dq_Z zero/value and no physical-lock closure"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md",
            "script": "scripts/Y5_R2FR_constraint_first_Z_elimination_and_coframe_source_descent.py",
            "objective": "try to sign the constraint/no-pole elimination of Z before q, then prove e_obs/source/readout/boundary descent through Q_vis",
            "success_condition": "either Dq_Z_norm=0 is parent-signed through constraint-first descent, or explicit component leaks are retained as finite nonclaim factors",
            "why_next": "1674 isolates the least-scrutiny path: eliminate Z upstream before matter or readout can see it",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def validate() -> list[dict[str, object]]:
    source_register = read_csv(SOURCE_REGISTER)
    q_ansatz = read_csv(PARENT_Q_ANSATZ)
    z_basis = read_csv(Z_BASIS_CANDIDATE)
    dq_matrix = read_csv(DQ_COMPONENT_MATRIX)
    constraint = read_csv(CONSTRAINT_FIRST_LEDGER)
    conditional = read_csv(CONDITIONAL_ZERO)
    factor_update = read_csv(FACTOR_VALUE_UPDATE)
    decisions = read_csv(DECISION)
    claims = read_csv(CLAIM_GATE)
    next_targets = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_register)
    q_ansatz_written = any(row["object"] == "Q_vis=q(Phi_parent)" and "Z" in row["interpretation"] for row in q_ansatz)
    constraint_selected = any(row["object"] == "C_Z(Phi)=0 before q" and bool_cell(row["selected_as_best_route"]) for row in q_ansatz)
    z_basis_complete = len(z_basis) == 6 and all(row["basis_status"] == "CANDIDATE_NOT_LIVE_PARENT_BASIS" for row in z_basis)
    dq_matrix_blocks = {"Dq_Z[e_obs,g_obs,mu_m,D_m]", "Dq_Z[source normalization/J_H]", "Dq_Z[clock/photon/orbit/EM/PPN readouts]", "Dq_Z[B_edge,P_loc,Q_X]", "Dq_Z[R_phys -> observed residuals]", "Dq_Z_norm"} == {row["component"] for row in dq_matrix}
    dq_not_claimed = all(not bool_cell(row["theorem_zero_adopted"]) and not bool_cell(row["finite_value_present"]) for row in dq_matrix)
    constraint_verdict = any(row["clause_id"] == "CFZ1674_5_verdict" and row["status"] == "CONSTRAINT_FIRST_ZERO_NOT_PROVED" for row in constraint)
    conditional_not_adopted = conditional[0]["accepted_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO" and not bool_cell(conditional[0]["theorem_zero_adopted"])
    factor_still_missing = factor_update[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO" and factor_update[0]["current_status"] == "STRUCTURE_CLARIFIED_VALUE_STILL_MISSING"
    decision_next = any(row["decision"] == "CONSTRAINT_FIRST_SELECTED" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_targets[0]["next_target"] == "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1674*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    missing_not_claimed = True
    for path in CLAIM_CHECKED:
        for row in read_csv(path):
            if row.get("valid_for_claim", "False").lower() == "true" or row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(missing_marker(value) for value in row.values()):
                for key in ["valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "prediction_source_backed", "valid_prediction_row"]:
                    if key in row and bool_cell(row[key]):
                        missing_not_claimed = False

    checks = [
        ("VAL1674_0_sources_exist", sources_ok, "all cited 1674 source paths exist and needles are present"),
        ("VAL1674_1_q_ansatz_written", q_ansatz_written, "minimal visible quotient ansatz is written"),
        ("VAL1674_2_constraint_selected", constraint_selected, "constraint-first route is selected as best route"),
        ("VAL1674_3_z_basis_candidate", z_basis_complete, "six Z physical-channel basis candidates are present but not live"),
        ("VAL1674_4_dq_matrix_blocks", dq_matrix_blocks, "Dq_Z component derivative matrix covers coframe/source/readout/boundary/residual/norm"),
        ("VAL1674_5_dq_not_claimed", dq_not_claimed, "no Dq component is marked theorem-zero or finite"),
        ("VAL1674_6_constraint_verdict", constraint_verdict, "constraint-first zero is not proved"),
        ("VAL1674_7_conditional_not_adopted", conditional_not_adopted, "conditional Dq_Z=0 row is not adopted"),
        ("VAL1674_8_factor_still_missing", factor_still_missing, "Dq_Z_norm value remains missing"),
        ("VAL1674_9_decision_next", decision_next, "decision selects constraint-first coframe/source descent"),
        ("VAL1674_10_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1674_11_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1674_12_missing_not_ready", missing_not_claimed, "no missing/conditional row is marked claim/scoring/source ready"),
        ("VAL1674_13_next_target_selected", next_target_selected, "next target selects constraint-first Z elimination and descent"),
        ("VAL1674_14_csv_parse", csv_parse, "all generated 1674 CSVs parse"),
        ("VAL1674_15_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1674_16_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1674_17_formalization_untouched", formalization_clean, "no 1674 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1674_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1674 parent q/Z ansatz and Dq computation validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    q_rows: list[dict[str, object]],
    z_rows: list[dict[str, object]],
    dq_rows: list[dict[str, object]],
    constraint_rows: list[dict[str, object]],
    conditional_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1674 - Parent q/Z Basis Minimal Ansatz And Dq Computation

**Private status:** structural derivation checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The minimal observable boundary is now explicit enough to attack:

```text
Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,A_owned,B_edge,P_loc)
Q_vis=q(Phi_parent)=(e_obs,g_obs,mu_m,D_m,source/readout data,theta_owned,A_owned)
R_phys=(q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling,boundary,coupling)
```

The clean route is **constraint-first**:

```text
C_Z(Phi)=0 before q is formed
=> q(Phi)|C_Z=0 = qbar(Q_vis)
=> Dq[partial_Z]=0
```

But this is only conditional. The parent constraint/no-pole origin, observed-coframe functor, source/readout descent, and boundary/no-flux clause are not signed yet. Therefore `Dq_Z_norm` remains `MISSING_NUMERIC_OR_THEOREM_ZERO`.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1674"])}

## Parent q/Z Ansatz

{markdown_table(q_rows, ["ansatz_id", "object", "minimal_definition", "status", "interpretation", "selected_as_best_route"])}

## Z Basis Candidate

{markdown_table(z_rows, ["basis_id", "basis_symbol", "physical_channel", "candidate_component", "current_blocker"])}

## DqZ Component Derivative Matrix

{markdown_table(dq_rows, ["matrix_row_id", "component", "conditional_status", "blocking_issue", "computation_status"])}

## Constraint-First Zero Ledger

{markdown_table(constraint_rows, ["clause_id", "required_clause", "status", "next_action"])}

## Conditional Zero Row

{markdown_table(conditional_rows, ["row_id", "symbol", "conditional_value", "current_status", "accepted_value", "reason_not_accepted"])}

## Factor Value Update

{markdown_table(factor_rows, ["row_id", "symbol", "new_information", "candidate_value", "current_status"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is the first checkpoint in this little run that feels like it points at the right machinery rather than just naming another leak. The q/Z boundary is now concrete: if Z is eliminated before q, the derivative dies cleanly; if Z survives into coframe, source, readout, or boundary data, the leak is real and must be bounded. That is exactly the kind of yes/no engineering test we needed.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    sources = source_register_rows()
    q_rows = parent_q_ansatz_rows()
    z_rows = z_basis_candidate_rows()
    dq_rows = dq_component_matrix_rows()
    constraint_rows_ = constraint_first_rows()
    conditional_rows_ = conditional_zero_rows()
    factor_rows = factor_update_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_targets = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        sources,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1674", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        PARENT_Q_ANSATZ,
        q_rows,
        ["branch_id", "ansatz_id", "object", "minimal_definition", "source_basis", "status", "interpretation", "selected_as_best_route", "parent_signed", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        Z_BASIS_CANDIDATE,
        z_rows,
        ["branch_id", "basis_id", "basis_symbol", "physical_channel", "candidate_component", "current_blocker", "basis_status", "parent_signed", "theorem_closed_for_claim", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DQ_COMPONENT_MATRIX,
        dq_rows,
        ["branch_id", "matrix_row_id", "component", "derivative_object", "conditional_status", "blocking_issue", "computation_status", "computed_value", "theorem_zero_adopted", "finite_value_present", "prediction_source_backed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CONSTRAINT_FIRST_LEDGER,
        constraint_rows_,
        ["branch_id", "clause_id", "required_clause", "status", "next_action", "clause_met", "parent_signed", "theorem_zero_adopted", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CONDITIONAL_ZERO,
        conditional_rows_,
        ["branch_id", "row_id", "symbol", "conditional_value", "condition", "current_status", "accepted_value", "reason_not_accepted", "theorem_zero_adopted", "finite_value_present", "prediction_source_backed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        FACTOR_VALUE_UPDATE,
        factor_rows,
        ["branch_id", "row_id", "symbol", "previous_status", "new_information", "candidate_value", "upper_bound", "projection_formula", "current_status", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DECISION,
        decisions,
        ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CLAIM_GATE,
        claims,
        ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        NEXT_TARGET,
        next_targets,
        ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"],
    )

    copy_outputs()
    validation = validate()
    write_csv(VALIDATION, validation, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(sources, q_rows, z_rows, dq_rows, constraint_rows_, conditional_rows_, factor_rows, decisions, claims, next_targets, validation)

    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1674 validation PASS")


if __name__ == "__main__":
    main()
