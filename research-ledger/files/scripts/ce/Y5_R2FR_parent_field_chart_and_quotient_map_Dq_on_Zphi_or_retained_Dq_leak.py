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
QUARANTINE = MICROSCOPE / "quarantine" / "1667"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md"

SOURCE_FILES = {
    "1666_doc": ROOT / "1666-Y5-R2FR-coupling-vertical-generator-parent-object-language-or-residual-bound-handoff.md",
    "1666_validation": OUT / "P8_Y5_BRR545_1666_VALIDATION.csv",
    "1666_object_language": OUT / "P8_Y5_PARENT_QLOC_1666_OBJECT_LANGUAGE_PACKET.csv",
    "1666_residual_handoff": OUT / "P8_Y5_PARENT_QLOC_1666_RESIDUAL_BOUND_HANDOFF.csv",
    "1505_dq_tests": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
    "1505_vertical_theorem": OUT / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
    "1620_q_verticality": OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
    "1575_vertical_signature": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
    "781_minimal_action": OUT / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
    "783_field_map": OUT / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
    "1045_vertical_lift": OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
    "761_matter_vertical": OUT / "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
    "1282_component_map": OUT / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv",
    "1665_z_route": OUT / "P8_Y5_PARENT_QLOC_1665_Z_ROUTE_SIGNATURE_AUDIT.csv",
    "1665_phi_route": OUT / "P8_Y5_PARENT_QLOC_1665_PHI_ROUTE_SIGNATURE_AUDIT.csv",
    "1022_vertical_quotient": OUT / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
    "1023_coupling_descent": OUT / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
    "1541_dqvm_finite": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "778_descent_gate": OUT / "P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv",
}

NEEDLES = {
    "1666_doc": ["The first domino is now `q` and `Dq`", "1667-Y5-R2FR-parent-field-chart"],
    "1666_validation": ["VAL1666_OVERALL", "PASS"],
    "1666_object_language": ["OLP1666_1_quotient_map", "Q_NOT_OWNED"],
    "1666_residual_handoff": ["RBH1666_1_Dq_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
    "1505_dq_tests": ["DQT1505_8_acceptance", "BLOCKED"],
    "1505_vertical_theorem": ["THM1505_2_current_branch_verdict", "KEEP_BETA_AND_ALPHA_CLOSURE_BOUND"],
    "1620_q_verticality": ["QVM1620_5_verdict", "VERTICALITY_MAP_NOT_CLOSED"],
    "1575_vertical_signature": ["VERT1575_5_verdict", "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED"],
    "781_minimal_action": ["MPC781_7_contract_verdict", "candidate_only_requires_782_consistency_gate"],
    "783_field_map": ["FM783_1_Q", "needed_but_not_owned"],
    "1045_vertical_lift": ["VLG1045_4_verdict", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"],
    "761_matter_vertical": ["MVA761_5_evaluability_verdict", "parent_matter_vertical_action_not_signed"],
    "1282_component_map": ["RCM1282_6_verdict", "COMPONENT_MAP_NOT_CLOSED"],
    "1665_z_route": ["ZRA1665_8_verdict", "DO_NOT_ADOPT_LIVE_NONCLAIM"],
    "1665_phi_route": ["PRA1665_6_verdict", "DO_NOT_ADOPT_LIVE_NONCLAIM"],
    "1022_vertical_quotient": ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"],
    "1023_coupling_descent": ["CDA1023_4_verdict", "coupling_not_theorem_zero"],
    "1541_dqvm_finite": ["DQC1541_4_Scg_envelope", "NONCLAIM_SCHEMA_READY_INPUTS_MISSING"],
    "778_descent_gate": ["CDT778_7_theorem_result", "conditional_theorem_only_not_current_MTS_claim"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1667_SOURCE_REGISTER.csv"
FIELD_CHART = OUT / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv"
QUOTIENT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv"
DQ_TESTS = OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"
CONSTRAINT_BRANCH = OUT / "P8_Y5_PARENT_QLOC_1667_CONSTRAINT_FIRST_BRANCH_AUDIT.csv"
RETAINED_DQ_LEAKS = OUT / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1667_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1667_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1667_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1667_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    FIELD_CHART,
    QUOTIENT_AUDIT,
    DQ_TESTS,
    CONSTRAINT_BRANCH,
    RETAINED_DQ_LEAKS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    FIELD_CHART,
    QUOTIENT_AUDIT,
    DQ_TESTS,
    CONSTRAINT_BRANCH,
    RETAINED_DQ_LEAKS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    FIELD_CHART: [
        QUARANTINE / "PARENT_FIELD_CHART_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_field_chart_candidate_nonclaim_1667.csv",
        QUEUE / "JR1667_PARENT_FIELD_CHART_CANDIDATE_NONCLAIM.csv",
    ],
    QUOTIENT_AUDIT: [
        QUARANTINE / "QUOTIENT_MAP_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_quotient_map_audit_nonclaim_1667.csv",
        QUEUE / "JR1667_QUOTIENT_MAP_AUDIT_NONCLAIM.csv",
    ],
    DQ_TESTS: [
        QUARANTINE / "DQ_ON_ZPHI_TESTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Dq_on_Zphi_tests_nonclaim_1667.csv",
        QUEUE / "JR1667_DQ_ON_ZPHI_TESTS_NONCLAIM.csv",
    ],
    CONSTRAINT_BRANCH: [
        QUARANTINE / "CONSTRAINT_FIRST_BRANCH_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_constraint_first_branch_audit_nonclaim_1667.csv",
        QUEUE / "JR1667_CONSTRAINT_FIRST_BRANCH_AUDIT_NONCLAIM.csv",
    ],
    RETAINED_DQ_LEAKS: [
        QUARANTINE / "RETAINED_DQ_LEAK_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_retained_Dq_leak_rows_nonclaim_1667.csv",
        QUEUE / "JR1667_RETAINED_DQ_LEAK_ROWS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1667.csv",
        QUEUE / "JR1667_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "local_gr_claim_allowed",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "theorem_closed",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1667 parent field chart and quotient Dq test input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def field_chart_rows() -> list[dict[str, object]]:
    rows = [
        ("PFC1667_0_visible_quotient", "Q_vis", "ordinary-matter-visible quotient data", "Q_vis=(e_obs,g_obs,source/readout data, theta_owned)", "candidate from MPC781/FM783, not parent-signed", "CANDIDATE_CONTRACT_ONLY"),
        ("PFC1667_1_geometry_block", "G_obs", "observed geometry", "e_obs=E(Q_vis); g_obs=e_obs^T eta e_obs", "FM783 gives strongest partial alignment to g_mu_nu/psi metric ansatz, but coframe/action ownership open", "PARTIAL_ALIGNMENT_NOT_ACTION_OWNED"),
        ("PFC1667_2_residual_block", "R_phys", "physical local residual vector", "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling,boundary,coupling}", "RCM1282 says full Z-to-R_phys lock is not closed", "RESIDUAL_VECTOR_NOT_PARENT_LOCKED"),
        ("PFC1667_3_Z_block", "Z^A", "formal response-doublet residual coordinate", "Z^A=(R_+^A-R_-^A)/2", "1665 keeps Z as formal route only", "AUXILIARY_FORMAL_NOT_LIVE"),
        ("PFC1667_4_phi_block", "phi", "trace-free improvement auxiliary candidate", "TF delta[int sqrt(-g) phi R] -> K_L shape", "1665 keeps phi owner/adoption unsigned", "AUXILIARY_FORMAL_NOT_LIVE"),
        ("PFC1667_5_matter_block", "Psi_A,theta_A", "ordinary matter and constants", "matter fields are sections over e_obs(q(Phi)); theta_A owned constants", "761/1045 say matter vertical action and lift are not parent-signed", "MATTER_DOMAIN_UNSIGNED"),
        ("PFC1667_6_boundary_block", "B_edge,P_loc,Q_X", "boundary/projector/source-measure block", "boundary charges, compact collar, projector and source support data", "1666 and 1023 retain boundary/projector leakage", "BOUNDARY_BLOCK_OPEN"),
        ("PFC1667_7_chart_verdict", "Phi_parent", "minimal current field chart", "Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,B_edge,P_loc)", "useful chart written for testing, but it is not an adopted parent action chart", "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "chart_id": chart_id,
            "symbol": symbol,
            "role": role,
            "candidate_definition": definition,
            "current_evidence": evidence,
            "status": status,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for chart_id, symbol, role, definition, evidence, status in rows
    ]


def quotient_audit_rows() -> list[dict[str, object]]:
    rows = [
        ("QMA1667_0_q_prior", "q(Phi)=(e_obs,g_obs,source/readout data)", "DQT1505_0 calls this a partial prior contract", "PARTIAL_PRIOR_CONTRACT", "good start but not computable"),
        ("QMA1667_1_Q_needed", "Q=q(Phi_parent) as ordinary-matter-visible quotient", "FM783_1 says Q is needed but not owned", "NEEDED_BUT_NOT_OWNED", "renames the theorem unless q and ker(Dq) are explicit"),
        ("QMA1667_2_e_obs_candidate", "g_obs/e_obs from psi or metric-repair branch", "FM783_2 gives strongest partial alignment", "PARTIAL_ALIGNMENT", "coframe, connection, covariance/action ownership remain open"),
        ("QMA1667_3_q_excludes_Rphys", "q_loc/R_phys should not be ordinary-matter quotient data", "FM783_7/8 say q_loc is residual, not quotient", "CORRECT_GUARD_CONTRACT", "if q includes residuals, matter sees the failure mode"),
        ("QMA1667_4_observer_Jq_risk", "q includes observer radial phase-cell/J_q data", "QVM1620_0 says Dq[v_Z] nonzero or unproved", "REJECT_AS_CURRENT_VERTICAL_PROOF", "R_AB/J_q can be coframe/cell-visible"),
        ("QMA1667_5_shape_only_option", "q quotients reciprocal cell-volume while preserving physical shape/orientation", "QVM1620_1 says possible but not constructed", "POSSIBLE_CONTRACT_NOT_CLOSED", "needs independent unit/cell normalization and observed coframe functor"),
        ("QMA1667_6_verdict", "computable current q", "1666/1505/1620 combined audit", "Q_NOT_COMPUTABLE_CURRENT_CORPUS", "Dq leak must be retained unless constraint-first route closes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "quotient_clause": clause,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, clause, evidence, status, effect in rows
    ]


def dq_test_rows() -> list[dict[str, object]]:
    rows = [
        ("DQT1667_0_test_definition", "Dq[v]=(delta e_obs, delta source/readout, delta theta_owned, delta boundary/projector) for the proposed direction v", "requires explicit q, tangent basis, normalization, and boundary/readout maps", "TEST_DEFINED_NOT_RUNNABLE_ON_LIVE_Q", "current q is not computable"),
        ("DQT1667_1_Z_normal_form", "Dq[partial_Z]", "requires Z basis mapped to R_phys and q dependence on R_phys declared", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK", "formal normal-form Z could be a shadow variable"),
        ("DQT1667_2_phi_improvement", "Dq[partial_phi]", "requires phi owner and whether phi enters e_obs/source/readout directly", "PHI_OWNER_MISSING_DQ_NOT_COMPUTABLE", "Khat algebra alone does not prove matter invisibility"),
        ("DQT1667_3_RAB_Jq_direction", "Dq[v_R] for R_AB/J_q residual", "QVM1620_0 says nonzero or unproved if q includes observer radial cell data", "REJECT_ZERO_CURRENT_EVIDENCE", "cannot call visible cell data gauge"),
        ("DQT1667_4_Dq_zero_not_enough", "Dq[v]=0 only for coframe/readout", "THM1505_1 says source/test charge, marker, boundary, or finite operator can survive", "COUNTERMODEL_GUARD_ACTIVE", "beta-zero shortcut forbidden"),
        ("DQT1667_5_constraint_first_escape", "constraint/no-pole eliminates Z/phi/R_AB before matter coupling", "QVM1620_2 and VQC1022_7 mark this as best route but current-claim failed", "BEST_DERIVATION_ROUTE_UNSIGNED", "needs parent action/constraint origin"),
        ("DQT1667_6_verdict", "Dq[Z/phi]=0 or constraint-eliminated", "DQT1667_0 through DQT1667_5", "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK", "emit retained Dq leak rows"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": test_id,
            "test": test,
            "required_input": required_input,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for test_id, test, required_input, status, effect in rows
    ]


def constraint_branch_rows() -> list[dict[str, object]]:
    rows = [
        ("CFB1667_0_Z_constraint", "lambda_Z Z=0 or equivalent source-free constraint before matter/readout", "would remove formal Z before q sees it", "POSSIBLE_BUT_PARENT_ORIGIN_UNSIGNED", "needs parent action, multiplier stress silence, and boundary certificate"),
        ("CFB1667_1_phi_constraint", "local auxiliary phi equation fixes phi or makes only trace-free improvement response observable", "could keep Khat construction while preventing matter-visible phi hair", "POSSIBLE_BUT_PHI_OWNER_MISSING", "needs local phi action, not inverse-Box shorthand"),
        ("CFB1667_2_RAB_constraint", "lambda_R R_AB=0 or no-pole field before matter coupling", "QVM1620/1575 mark this as best escape for visible R_AB/J_q", "BEST_ROUTE_BUT_UNSIGNED", "needs lambda_R origin and no independent Green/source charge"),
        ("CFB1667_3_first_class_no_pole", "q/v/action/matter/boundary/degree certificate removes the mode as gauge/topological", "VQC1022 gives strongest path to local-GR-like silence", "FAIL_CURRENT_CLAIM_BUT_BEST_TARGET", "needs q, v_X, action descent, boundary silence, and degree count"),
        ("CFB1667_4_posthoc_delete", "delete Z/phi/R_AB after readout because it is inconvenient", "forbidden", "REFUSED", "would hide a real source charge"),
        ("CFB1667_5_verdict", "constraint-first branch", "best derivation path, not currently sourced", "SELECT_NEXT_CONSTRAINT_OR_DQ_LEAK_BOUND", "try parent constraint action next or retain leak bounds"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "constraint_id": constraint_id,
            "route": route,
            "why_it_could_work": why,
            "status": status,
            "missing_to_promote": missing,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for constraint_id, route, why, status, missing in rows
    ]


def retained_dq_leak_rows() -> list[dict[str, object]]:
    rows = [
        ("DQL1667_0_Dq_Z", "Dq_Z_norm", "MISSING_NUMERIC_OR_THEOREM_ZERO", "arena dependent", "Z normal-form quotient leak", "DQT1667_1_Z_normal_form", "needed before Z can be called quotient-vertical"),
        ("DQL1667_1_Dq_phi", "Dq_phi_norm", "MISSING_NUMERIC_OR_THEOREM_ZERO", "arena dependent", "phi improvement quotient leak", "DQT1667_2_phi_improvement", "needed before phi can be matter/readout-invisible"),
        ("DQL1667_2_Dq_RAB_Jq", "Dq_RAB_or_Jq_norm", "MISSING_NUMERIC_OR_THEOREM_ZERO", "arena dependent", "R_AB/J_q cell-visible leak", "DQT1667_3_RAB_Jq_direction", "needed if R_AB/J_q remains in q"),
        ("DQL1667_3_DObs_e", "DObs_e_Dq_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "coframe norm", "observed geometry channel", "DQC1541_0_C_qm_definition", "feeds stress-mediated source coupling"),
        ("DQL1667_4_Dsource_readout", "Dsource_readout_Dq_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "source/readout norm", "Newton/source/readout channel", "DQT1505_7_boundary_readout; CDT778_4_readout_descent", "prevents hidden source/orbit/clock maps"),
        ("DQL1667_5_Dtheta_marker", "Dtheta_marker_Dq_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "dimensionless", "constants/material marker channel", "CDA1023_1_constants_markers", "Dq=0 for coframe is insufficient if markers move"),
        ("DQL1667_6_boundary_projector", "Dboundary_projector_Dq_leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "boundary/projector norm", "boundary and projector channel", "CDA1023_3_projector_boundary", "edge/source projection can reopen coupling"),
        ("DQL1667_7_Scg_envelope", "S_cg_norm", "0.5||T||_source*C_qm + S_direct + S_source_norm_extra + S_boundary", "E* forcing units", "absolute no-cancellation envelope", "DQC1541_4_Scg_envelope", "finite fallback if q-kernel proof fails"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "leak_id": leak_id,
            "symbol": symbol,
            "value_or_formula": value,
            "units": units,
            "channel": channel,
            "source_anchor": source_anchor,
            "why_needed": why_needed,
            "status": "RETAINED_NONCLAIM_DQ_LEAK_INPUT",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for leak_id, symbol, value, units, channel, source_anchor, why_needed in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1667_0_field_chart", "FIELD_CHART_CANDIDATE_WRITTEN", "we now have a minimal test chart for Q/R/Z/phi/matter/boundary", "do not treat it as adopted parent action"),
        ("DEC1667_1_q_status", "Q_NOT_COMPUTABLE_CURRENT_CORPUS", "q is a partial prior contract, not an explicit map", "retain Dq leak until q is sourced"),
        ("DEC1667_2_Dq_status", "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK", "Z/phi cannot be proved quotient-vertical from current files", "emit retained Dq leak rows"),
        ("DEC1667_3_best_route", "NEXT_CONSTRAINT_FIRST_OR_DQ_LEAK_BOUND", "constraint-first is cleaner than pretending visible residuals are gauge", "try parent Z/phi/R_AB constraint/no-pole action or fill Dq leak source pack"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1667_0_field_chart_adopted", "parent field chart is adopted as MTS action chart", False, "BLOCKED", "candidate chart only"),
        ("CG1667_1_q_computable", "q(Phi_parent) is explicit and computable", False, "BLOCKED", "q not owned/currently computable"),
        ("CG1667_2_Dq_Z_zero", "Dq[Z]=0 or Z is constraint-eliminated", False, "BLOCKED", "Z basis/component lock missing"),
        ("CG1667_3_Dq_phi_zero", "Dq[phi]=0 or phi is constraint-eliminated", False, "BLOCKED", "phi owner missing"),
        ("CG1667_4_Dq_enough_for_matter", "Dq result also kills source/test/marker/boundary channels", False, "BLOCKED", "Dq=0 alone is insufficient"),
        ("CG1667_5_local_GR_Newton", "local GR/Newton follows from quotient verticality", False, "NO_CLAIM", "Dq leak retained and source descent unresolved"),
        ("CG1667_6_PPN_R10_WEP_clock_orbit", "PPN/R10/WEP/clock/orbit passes follow", False, "NO_CLAIM", "no arena claim without theorem-zero or numeric leak bounds"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md",
            "script": "scripts/Y5_R2FR_constraint_first_Zphi_RAB_action_or_Dq_leak_source_pack.py",
            "objective": "try the cleaner route first: derive a parent constraint/no-pole action that removes Z/phi/R_AB before matter/readout sees them; if that fails, stage source-ready Dq leak bound rows for local tests",
            "success_condition": "either Z/phi/R_AB are parent-eliminated before q and matter coupling, or Dq leak rows are promoted into a source-pack schema with units and arena projections still nonclaim",
            "forbidden_shortcuts": "no visible-residual-as-gauge shortcut; no post-readout deletion; no local GR/Newton/PPN/R10/WEP claim; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def validation_rows(
    source_rows: list[dict[str, object]],
    chart: list[dict[str, object]],
    quotient: list[dict[str, object]],
    dq_tests: list[dict[str, object]],
    constraint: list[dict[str, object]],
    leaks: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    generated_name_markers = (
        "1667-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1667",
        "P8_Y5_BRR545_1667",
        "JR1667",
        "Y5_R2FR_parent_field_chart_and_quotient_map",
    )
    formalization_dirty = (
        any(
            "1667" in path.name
            and any(marker in path.name for marker in generated_name_markers)
            for path in FORMALIZATION.rglob("*1667*")
        )
        if FORMALIZATION.exists()
        else False
    )
    chart_candidate = any(row["chart_id"] == "PFC1667_7_chart_verdict" and row["status"] == "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED" for row in chart)
    q_not_computable = any(row["audit_id"] == "QMA1667_6_verdict" and row["status"] == "Q_NOT_COMPUTABLE_CURRENT_CORPUS" for row in quotient)
    dq_not_closed = any(row["test_id"] == "DQT1667_6_verdict" and row["status"] == "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK" for row in dq_tests)
    constraint_selected = any(row["constraint_id"] == "CFB1667_5_verdict" and row["status"] == "SELECT_NEXT_CONSTRAINT_OR_DQ_LEAK_BOUND" for row in constraint)
    leaks_nonclaim = all(row["claim_allowed"] is False and row["valid_for_claim"] is False and row["valid_prediction_row"] is False for row in leaks)
    next_target_selected = next_targets[0]["next_target"] == "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md"

    checks = [
        ("VAL1667_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1667 source paths exist and needles are present"),
        ("VAL1667_1_chart_candidate_nonclaim", chart_candidate, "field chart is candidate only, not parent-signed"),
        ("VAL1667_2_q_not_computable", q_not_computable, "current q map remains not computable"),
        ("VAL1667_3_Dq_not_closed", dq_not_closed, "Dq[Z/phi] zero is not proved"),
        ("VAL1667_4_constraint_route_selected", constraint_selected, "constraint-first or Dq leak bound selected next"),
        ("VAL1667_5_Dq_leaks_nonclaim", leaks_nonclaim, "retained Dq leak rows remain nonclaim/unscored"),
        ("VAL1667_6_decision_has_Dq_status", any(row["decision"] == "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK" for row in decisions), "decision records Dq closure failure"),
        ("VAL1667_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS local claims false"),
        ("VAL1667_8_next_target_selected", next_target_selected, "next target selects constraint-first or Dq leak source pack"),
        ("VAL1667_9_csv_parse", generated_csv_parse, "all generated 1667 CSVs parse"),
        ("VAL1667_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1667 generated rows keep MTS claim/no-score flags false"),
        ("VAL1667_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1667_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1667_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1667_14_formalization_untouched", not formalization_dirty, "no 1667 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1667_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1667 parent field chart and quotient map Dq on Z/phi validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    chart: list[dict[str, object]],
    quotient: list[dict[str, object]],
    dq_tests: list[dict[str, object]],
    constraint: list[dict[str, object]],
    leaks: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1667 - Parent Field Chart And Quotient Map Dq On Z/phi Or Retained Dq Leak

**Private status:** q/Dq first-domino checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The parent field chart can be written as a useful test object, but it is **not** a parent-signed MTS action chart.

```text
Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,B_edge,P_loc)
Q_vis=(e_obs,g_obs,source/readout data,theta_owned)
```

The `Dq` test does **not** close:

```text
Dq[Z]   : missing unified Z basis and physical residual lock.
Dq[phi] : phi owner/action is missing.
Dq[R_AB/J_q] : visible or unproved if q contains observer cell data.
```

So the current branch cannot honestly call `Z` or `phi` gauge/quotient-vertical. The clean route is constraint-first: remove `Z/phi/R_AB` by a parent action/no-pole mechanism before matter and readout see them. If that fails, the retained `Dq` leak rows become source-pack inputs.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Parent Field Chart Candidate

{markdown_table(chart, ["chart_id", "symbol", "role", "candidate_definition", "current_evidence", "status"])}

## Quotient Map Audit

{markdown_table(quotient, ["audit_id", "quotient_clause", "evidence", "status", "effect"])}

## Dq On Z/phi Tests

{markdown_table(dq_tests, ["test_id", "test", "required_input", "status", "effect"])}

## Constraint-First Branch Audit

{markdown_table(constraint, ["constraint_id", "route", "why_it_could_work", "status", "missing_to_promote"])}

## Retained Dq Leak Rows

{markdown_table(leaks, ["leak_id", "symbol", "value_or_formula", "units", "channel", "why_needed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is not grim; it is disciplined. The theory now has a precise target: either derive the constraint/no-pole mechanism that removes the local residual variables before the ordinary matter quotient is formed, or keep their `Dq` leakage as explicit testable residuals. That is exactly the kind of move needed if MTS is going to reduce to GR/Newton instead of merely resembling another fitted modification.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    chart = field_chart_rows()
    quotient = quotient_audit_rows()
    dq_tests = dq_test_rows()
    constraint = constraint_branch_rows()
    leaks = retained_dq_leak_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (FIELD_CHART, chart),
        (QUOTIENT_AUDIT, quotient),
        (DQ_TESTS, dq_tests),
        (CONSTRAINT_BRANCH, constraint),
        (RETAINED_DQ_LEAKS, leaks),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, chart, quotient, dq_tests, constraint, leaks, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, chart, quotient, dq_tests, constraint, leaks, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1667 validation failed; see P8_Y5_BRR545_1667_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1667 validation PASS")


if __name__ == "__main__":
    main()
