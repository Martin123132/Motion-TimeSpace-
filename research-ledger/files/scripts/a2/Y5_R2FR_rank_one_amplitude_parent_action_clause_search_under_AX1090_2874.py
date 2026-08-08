from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2874-Y5-R2FR-rank-one-amplitude-parent-action-clause-search-under-AX1090.md"

SRC_2873_DOC = ROOT / "2873-Y5-R2FR-first-triplet-parent-source-current-identity-reentry-under-AX1090.md"
SRC_2873_NEXT = RESIDUALS / "P8_Y5_R2FR_2873_NEXT_TARGET.csv"
SRC_2873_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2873_REENTRY_DERIVATION_AUDIT.csv"
SRC_2873_OWNER = RESIDUALS / "P8_Y5_R2FR_2873_OWNER_CLAUSE_GATE.csv"
SRC_2873_REQUEST = RESIDUALS / "P8_Y5_R2FR_2873_PARENT_ACTION_CLAUSE_REQUEST.csv"
SRC_2873_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2873_VALIDATION.csv"

SRC_2866_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv"
SRC_2866_VARIATION = RESIDUALS / "P8_Y5_R2FR_2866_VARIATIONAL_DERIVATION_CHECK.csv"
SRC_2866_REENTRY = RESIDUALS / "P8_Y5_R2FR_2866_REENTRY_ACCEPTANCE_GATE.csv"
SRC_2866_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2866_VALIDATION.csv"

SRC_2867_HESSIAN = RESIDUALS / "P8_Y5_R2FR_2867_HESSIAN_FACTORISATION_TEST.csv"
SRC_2867_ROUTE = RESIDUALS / "P8_Y5_R2FR_2867_SIGMA_ORIGIN_ROUTE_AUDIT.csv"
SRC_2867_VERTICAL = RESIDUALS / "P8_Y5_R2FR_2867_VERTICAL_GENERATOR_DERIVATION_GATE.csv"
SRC_2867_DQ = RESIDUALS / "P8_Y5_R2FR_2867_QUOTIENT_DQ_GATE.csv"
SRC_2867_DCO = RESIDUALS / "P8_Y5_R2FR_2867_DCDAGGER_OMEGA_GATE.csv"
SRC_2867_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2867_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2867_VALIDATION.csv"

SRC_2857_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2857_MINIMAL_DOUBLET_ACTION_ANSATZ.csv"
SRC_2857_ALGEBRA = RESIDUALS / "P8_Y5_R2FR_2857_ANSATZ_ALGEBRA_CHECK.csv"
SRC_2857_OWNER = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2859_ORIGIN = RESIDUALS / "P8_Y5_R2FR_2859_PARENT_ORIGIN_SCAN.csv"
SRC_2859_SEARCH = RESIDUALS / "P8_Y5_R2FR_2859_UAMP_CORPUS_SEARCH_AUDIT.csv"
SRC_2859_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2859_DERIVATION_ATTEMPT_LEDGER.csv"
SRC_2859_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2859_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2859_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2859_VALIDATION.csv"

SRC_PARENT_ACTION_SEARCH = RESIDUALS / "P8_Y5_MAC545_PARENT_ACTION_CLAUSE_SEARCH.csv"
SRC_PARENT_ACTION_TESTS = RESIDUALS / "P8_Y5_BRR545_PARENT_ACTION_CLAUSE_TESTS.csv"
SRC_PARENT_ACTION_ATTEMPT = RESIDUALS / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv"
SRC_PARENT_ACTION_DECISION = RESIDUALS / "P8_Y5_PARENT_ACTION_CONTRACT_DECISION.csv"
SRC_1784_PACKET = RESIDUALS / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv"
SRC_1784_ALIGNMENT = RESIDUALS / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_ALIGNMENT_MATRIX.csv"
SRC_1784_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv"
SRC_1791_LAW = RESIDUALS / "P8_Y5_PARENT_QLOC_1791_AMPLITUDE_AND_CR2_LAW.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2874_SOURCE_REGISTER.csv",
    "candidate_review": RESIDUALS / "P8_Y5_R2FR_2874_ACTION_CLAUSE_CANDIDATE_REVIEW.csv",
    "hessian": RESIDUALS / "P8_Y5_R2FR_2874_RANK_ONE_HESSIAN_EXTRACTION_AUDIT.csv",
    "rejection": RESIDUALS / "P8_Y5_R2FR_2874_PARENT_ORIGIN_REJECTION_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2874_DEMOTION_AND_FALLBACK_DECISION.csv",
    "requests": RESIDUALS / "P8_Y5_R2FR_2874_EXACT_SOURCE_REQUESTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2874_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2874_RUNNER_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2874_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2874_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2874_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": LOCAL_BOUNDS / "RAB_RANK_ONE_PARENT_ACTION_CANDIDATE_REVIEW_2874_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_RANK_ONE_PARENT_ACTION_REQUESTS_2874_NONCLAIM.csv",
    "decision_copy": BETA_DOCS / "RAB_RANK_ONE_PARENT_ACTION_DEMOTION_2874_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2874_finite_first_triplet_acquisition_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2874_0_2873_doc", SRC_2873_DOC, "Status: `Y5_R2FR_2873_parent_source_current_identity_conditional_mechanism_found_theorem_not_promoted_2874_next`;The next move is not another vague hunt", "2873 selected the exact rank-one parent action search"),
        ("SRC2874_1_2873_next", SRC_2873_NEXT, "NEXT2873_0_2874", "handoff to 2874"),
        ("SRC2874_2_2873_derivation", SRC_2873_DERIVATION, "DER2873_1_rank_one_action;DER2873_6_verdict", "rank-one action conditional mechanism"),
        ("SRC2874_3_2873_owner", SRC_2873_OWNER, "OWN2873_2_rank_one_hessian;OWN2873_3_source_covector;OWN2873_7_quotient_vertical", "owner clauses that remain unsigned"),
        ("SRC2874_4_2873_request", SRC_2873_REQUEST, "REQ2873_0_rank_one_parent_action;REQ2873_1_source_current_owner;REQ2873_2_boundary_green_readout", "exact parent action/source/boundary requests"),
        ("SRC2874_5_2873_validation", SRC_2873_VALIDATION, "VAL2873_OVERALL", "2873 validation"),
        ("SRC2874_6_2866_contract", SRC_2866_CONTRACT, "PACT2866_3_action;PACT2866_4_source_split;PACT2866_9_acceptance", "minimal parent action contract/template"),
        ("SRC2874_7_2866_variation", SRC_2866_VARIATION, "VAR2866_2_source_variation;VAR2866_4_integrated_charge;VAR2866_6_claim_status", "conditional variation check"),
        ("SRC2874_8_2866_reentry", SRC_2866_REENTRY, "RE2866_0_parent_action;RE2866_5_finite_rows", "2866 re-entry gate"),
        ("SRC2874_9_2866_validation", SRC_2866_VALIDATION, "VAL2866_OVERALL", "2866 validation"),
        ("SRC2874_10_2867_hessian", SRC_2867_HESSIAN, "HESS2867_1_rank_one_H;HESS2867_2_extract_sigma;HESS2867_3_source_covector;HESS2867_5_verdict", "rank-one Hessian formula and missing inputs"),
        ("SRC2874_11_2867_route", SRC_2867_ROUTE, "SIGROUTE2867_0_hessian;SIGROUTE2867_4_source_doublet;SIGROUTE2867_5_boundary_matter", "sigma origin route audit"),
        ("SRC2874_12_2867_vertical", SRC_2867_VERTICAL, "VGEN2867_2_actual_Dq;VGEN2867_6_verdict", "vertical generator gate"),
        ("SRC2874_13_2867_dq", SRC_2867_DQ, "DQ2867_0_chain_rule;DQ2867_4_verdict", "quotient Dq gate"),
        ("SRC2874_14_2867_dco", SRC_2867_DCO, "DCO2867_0_precise_map;DCO2867_3_parent_Omega;DCO2867_4_DCamp;DCO2867_6_verdict", "DCdagger/Omega route"),
        ("SRC2874_15_2867_demotion", SRC_2867_DEMOTION, "DEM2867_0_Uamp_route;DEM2867_1_reopen_condition", "U_amp closure demotion/reopen condition"),
        ("SRC2874_16_2867_validation", SRC_2867_VALIDATION, "VAL2867_OVERALL", "2867 validation"),
        ("SRC2874_17_2857_ansatz", SRC_2857_ANSATZ, "ANS2857_2_quotient_invariant;ANS2857_3_action;ANS2857_4_source_split", "minimal doublet action ansatz"),
        ("SRC2874_18_2857_algebra", SRC_2857_ALGEBRA, "ALG2857_0_invariant;ALG2857_2_source_split;ALG2857_5_tuning_guard", "ansatz algebra check"),
        ("SRC2874_19_2857_owner", SRC_2857_OWNER, "OWN2857_2_generator;OWN2857_3_action;OWN2857_6_full_vector", "parent ownership gate for the ansatz"),
        ("SRC2874_20_2859_origin", SRC_2859_ORIGIN, "ORG2859_0_direct_parent_uamp;ORG2859_3_action_origin;ORG2859_4_generator_origin", "parent U_amp origin scan"),
        ("SRC2874_21_2859_search", SRC_2859_SEARCH, "SEARCH2859_0_pre_ansatz_parent_hits", "corpus search: pre-ansatz U_amp hits"),
        ("SRC2874_22_2859_derivation", SRC_2859_DERIVATION, "DER2859_0_possible_form;DER2859_1_source_identity;DER2859_3_no_claim_rule", "conditional derivation/no-claim guard"),
        ("SRC2874_23_2859_demotion", SRC_2859_DEMOTION, "DEM2859_0_candidate_status;DEM2859_1_claim_status;DEM2859_3_reentry_status", "U_amp closure demotion ledger"),
        ("SRC2874_24_2859_validation", SRC_2859_VALIDATION, "VAL2859_OVERALL", "2859 validation"),
        ("SRC2874_25_parent_action_search", SRC_PARENT_ACTION_SEARCH, "CS546_0_MAC545_0;CS546_3_MAC545_3", "generic parent action clause search"),
        ("SRC2874_26_parent_action_tests", SRC_PARENT_ACTION_TESTS, "CT552_0_reference_symplectic;CT552_5_extra_sector_leak_check", "generic parent action clause tests"),
        ("SRC2874_27_parent_action_attempt", SRC_PARENT_ACTION_ATTEMPT, "DAT537_0_variation;DAT537_5_local_readout", "parent action derivation attempt"),
        ("SRC2874_28_parent_action_decision", SRC_PARENT_ACTION_DECISION, "D537_0_contract_written;D537_4_private_no_push", "parent action contract decision"),
        ("SRC2874_29_1784_packet", SRC_1784_PACKET, "FAP1784_0_metric_coframe;FAP1784_5_boundary_edge_modes", "field action packet candidate"),
        ("SRC2874_30_1784_alignment", SRC_1784_ALIGNMENT, "ALN1784_0_DCadjoint_covector;ALN1784_1_Omega_flat;ALN1784_5_verdict", "Omega/DCX alignment"),
        ("SRC2874_31_1784_gate", SRC_1784_GATE, "ODP1784_0_parent_variable_set;ODP1784_8_verdict", "Omega/DCX vertical packet gate"),
        ("SRC2874_32_1791_law", SRC_1791_LAW, "ACL1791_0_sourced_extremum;ACL1791_5_verdict", "amplitude law and CR2 guard"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def candidate_review_rows() -> list[dict[str, Any]]:
    candidates = [
        {
            "candidate_id": "ACT2874_0_2857_ansatz_action",
            "candidate": "S_amp=1/2<U_amp,L_U U_amp>+<J_U,U_amp> from minimal doublet construction",
            "source_path": str(SRC_2857_ANSATZ),
            "source_anchor": "ANS2857_3_action",
            "evidence_status": "CONSTRUCTED_ANSATZ_ONLY",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "the row constructs the desired mechanism after the target is known; it does not source the parent action from an upstream field principle",
        },
        {
            "candidate_id": "ACT2874_1_2866_template_action",
            "candidate": "same rank-one U_amp parent action contract",
            "source_path": str(SRC_2866_CONTRACT),
            "source_anchor": "PACT2866_3_action",
            "evidence_status": "DERIVATION_TEMPLATE_ONLY",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "L_U, J_U, worldtube measure, boundary differentiability and parent provenance are explicitly missing",
        },
        {
            "candidate_id": "ACT2874_2_2866_source_split",
            "candidate": "variation gives J_CAB=-sigma_R_source_sign*J_U and J_R=J_U",
            "source_path": str(SRC_2866_CONTRACT),
            "source_anchor": "PACT2866_4_source_split",
            "evidence_status": "CONDITIONAL_ALGEBRA_VALID",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "the algebra follows if the action is granted, but the action/current owner is not granted",
        },
        {
            "candidate_id": "ACT2874_3_2867_hessian_formula",
            "candidate": "H_amp=n^T L_U n with n=(-sigma_R_source_sign,1)",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_1_rank_one_H",
            "evidence_status": "FORMULA_READY_INPUTS_MISSING",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "H_CC, H_CR, H_RR or L_U are not sourced from a parent action block",
        },
        {
            "candidate_id": "ACT2874_4_2867_source_covector",
            "candidate": "j_amp=J_U*n",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_3_source_covector",
            "evidence_status": "CONDITIONAL_SOURCE_COVECTOR",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "J_U and the source/worldtube measure remain missing",
        },
        {
            "candidate_id": "ACT2874_5_2867_omega_dc_route",
            "candidate": "(DC_amp)^dagger epsilon = Omega_parent^flat(v_amp[epsilon])",
            "source_path": str(SRC_2867_DCO),
            "source_anchor": "DCO2867_0_precise_map",
            "evidence_status": "FORMAL_GEOMETRIC_ROUTE",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "parent Omega, DC_amp, reduced inverse and field-by-field vertical action are absent",
        },
        {
            "candidate_id": "ACT2874_6_2859_origin_scan",
            "candidate": "direct parent-origin evidence for U_amp",
            "source_path": str(SRC_2859_ORIGIN),
            "source_anchor": "ORG2859_0_direct_parent_uamp",
            "evidence_status": "NO_PRIOR_PARENT_SOURCE_FOUND",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "pre-ansatz corpus search did not find a parent-owned U_amp clause",
        },
        {
            "candidate_id": "ACT2874_7_generic_parent_action_packet",
            "candidate": "generic parent Lagrangian/Omega/DCX packet",
            "source_path": str(SRC_1784_GATE),
            "source_anchor": "ODP1784_8_verdict",
            "evidence_status": "FORMAL_PACKET_NOT_AMPLITUDE_SPECIFIC",
            "accepted_source_backed_action": False,
            "reason_not_accepted": "the packet does not instantiate the rank-one amplitude Hessian/source covector and still fails the parent Omega/DCX gates",
        },
    ]
    return [add_common(row) for row in candidates]


def hessian_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "HRA2874_0_doublet",
            "object": "Y_amp=(C_AB,delta_R)^T",
            "formula": "n=(-sigma_R_source_sign,1), U_amp=n dot Y_amp=delta_R-sigma_R_source_sign*C_AB",
            "status": "ALGEBRAICALLY_VALID",
            "missing_for_acceptance": "parent field chart and sigma_R_source_sign origin before readout",
            "parent_signed": False,
            "theorem_claimed": False,
        },
        {
            "audit_id": "HRA2874_1_rank_one_hessian",
            "object": "H_amp",
            "formula": "H_amp=n^T L_U n = [[sigma_R^2 L_U,-sigma_R L_U],[-sigma_R L_U,L_U]]",
            "status": "FORMULA_READY",
            "missing_for_acceptance": "source-backed L_U or H_CC,H_CR,H_RR with domain, units, branch and equation anchor",
            "parent_signed": False,
            "theorem_claimed": False,
        },
        {
            "audit_id": "HRA2874_2_sigma_extraction",
            "object": "sigma_R_source_sign",
            "formula": "sigma_R_source_sign=-H_CR/H_RR=-H_CC/H_CR when det(H)=H_CC*H_RR-H_CR^2=0",
            "status": "EXTRACTION_RULE_READY_INPUTS_MISSING",
            "missing_for_acceptance": "numeric or symbolic parent Hessian block entries before any local readout fitting",
            "parent_signed": False,
            "theorem_claimed": False,
        },
        {
            "audit_id": "HRA2874_3_source_covector",
            "object": "j_amp",
            "formula": "j_amp=J_U*n=(-sigma_R_source_sign*J_U,J_U)",
            "status": "FORMULA_READY",
            "missing_for_acceptance": "parent J_U, source measure, sign convention and no independent source rescaling theorem",
            "parent_signed": False,
            "theorem_claimed": False,
        },
        {
            "audit_id": "HRA2874_4_boundary_readout",
            "object": "boundary/improvement charge",
            "formula": "surface_integral(K_amp+B_CAB+sigma_R_source_sign*B_R)=0 or explicit finite charge row",
            "status": "OPEN_BLOCKER",
            "missing_for_acceptance": "boundary/corner silence theorem or finite included boundary row plus common Green convention",
            "parent_signed": False,
            "theorem_claimed": False,
        },
        {
            "audit_id": "HRA2874_5_verdict",
            "object": "rank-one amplitude parent action clause",
            "formula": "S_amp=1/2<U_amp,L_U U_amp>+<J_U,U_amp>+S_boundary[U_amp,W]",
            "status": "NOT_SOURCE_BACKED_IN_CURRENT_CORPUS",
            "missing_for_acceptance": "action provenance, Hessian/source entries, quotient vertical map, boundary/readout descent and matter/GM descent",
            "parent_signed": False,
            "theorem_claimed": False,
        },
    ]
    return [add_common(row) for row in rows]


def rejection_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "rejection_id": "REJ2874_0_direct_Uamp_source",
            "claim_tested": "direct upstream parent source for U_amp",
            "source_path": str(SRC_2859_SEARCH),
            "source_anchor": "SEARCH2859_0_pre_ansatz_parent_hits",
            "verdict": "REJECT_CURRENTLY",
            "reason": "prior search reports no pre-ansatz parent U_amp source; current hits are downstream ansatz/checkpoint artifacts",
            "reopen_condition": "a source path/equation anchor showing U_amp before local readout and before ansatz construction",
        },
        {
            "rejection_id": "REJ2874_1_action_origin",
            "claim_tested": "S_amp is a parent action clause",
            "source_path": str(SRC_2866_CONTRACT),
            "source_anchor": "PACT2866_3_action",
            "verdict": "REJECT_CURRENTLY",
            "reason": "present row is a contract/template, not a sourced parent Lagrangian block",
            "reopen_condition": "full parent action block or theorem deriving the rank-one block from parent fields and symmetries",
        },
        {
            "rejection_id": "REJ2874_2_hessian_origin",
            "claim_tested": "H_amp is sourced by parent Hessian",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_2_extract_sigma",
            "verdict": "REJECT_CURRENTLY",
            "reason": "extraction formula exists but parent H_CC,H_CR,H_RR or L_U are missing",
            "reopen_condition": "source-backed Hessian entries satisfying det(H)=0 and the sigma extraction identities",
        },
        {
            "rejection_id": "REJ2874_3_source_covector_origin",
            "claim_tested": "source covector is parent-parallel to n",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_3_source_covector",
            "verdict": "REJECT_CURRENTLY",
            "reason": "J_U, worldtube measure and no-rescaling owner are absent",
            "reopen_condition": "parent current/source definition giving j_C=-sigma_R*j_R with no independent rescaling freedom",
        },
        {
            "rejection_id": "REJ2874_4_Omega_DC_route",
            "claim_tested": "v_amp is derived as an actual vertical generator",
            "source_path": str(SRC_2873_OWNER),
            "source_anchor": "OWN2873_7_quotient_vertical",
            "verdict": "REJECT_CURRENTLY",
            "reason": "actual q, v_amp, DC_amp and Omega inverse are not sourced",
            "reopen_condition": "field-by-field quotient map with Dq[v_amp]=0 and Omega-flat equality checked",
        },
        {
            "rejection_id": "REJ2874_5_boundary_readout",
            "claim_tested": "boundary/readout descent silences the improvement charge",
            "source_path": str(SRC_2873_REQUEST),
            "source_anchor": "REQ2873_2_boundary_green_readout",
            "verdict": "REJECT_CURRENTLY",
            "reason": "boundary/corner theorem, common 4*pi Green convention and measured-GM descent remain unsigned",
            "reopen_condition": "boundary theorem or explicit finite boundary row plus common readout convention",
        },
        {
            "rejection_id": "REJ2874_6_total_route",
            "claim_tested": "rank-one route proves the first-triplet A_total zero",
            "source_path": str(SRC_2873_DERIVATION),
            "source_anchor": "DER2873_6_verdict",
            "verdict": "DEMOTE_TO_CLOSURE_ONLY_CURRENT_STATUS",
            "reason": "the mechanism is sharp but every parent ownership clause needed for theorem promotion is unsigned",
            "reopen_condition": "all rank-one action/source/boundary/readout clauses pass together, or finite source rows are acquired instead",
        },
    ]
    return [add_common(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2874_0_search_result",
            "decision": "Accept a source-backed rank-one parent action clause.",
            "result": "REJECTED_FOR_NOW",
            "because": "all currently available rows are ansatz, template, formal map, or missing-input clauses",
        },
        {
            "decision_id": "DEC2874_1_route_status",
            "decision": "Discard the rank-one route entirely.",
            "result": "REJECTED",
            "because": "the algebra is still the cleanest derivation-shaped mechanism; it should remain as a closure candidate",
        },
        {
            "decision_id": "DEC2874_2_claim_status",
            "decision": "Promote local-GR/Newton or A_total theorem-zero claims.",
            "result": "REFUSED",
            "because": "the parent action/source/current/boundary clauses are not source-backed",
        },
        {
            "decision_id": "DEC2874_3_fallback",
            "decision": "Return to finite first-triplet acquisition.",
            "result": "SELECTED",
            "because": "if the theorem route cannot be parent-signed today, the honest route is to source Q_CAB, q_R_eff, sigma_R_source_sign and common Green rows explicitly",
        },
        {
            "decision_id": "DEC2874_4_next",
            "decision": "Set 2875 target.",
            "result": "SELECTED_2875",
            "because": "2875 should build the finite first-triplet acquisition pack without claiming theorem-zero",
        },
    ]
    return [add_common(row) for row in rows]


def exact_request_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "request_id": "REQ2874_0_rank_one_action_source",
            "needed_clause": "source-backed rank-one parent action",
            "exact_request": "Provide a parent action/equation anchor for Y_amp=(C_AB,delta_R)^T, U_amp=delta_R-sigma_R_source_sign*C_AB, and S_amp=1/2<U_amp,L_U U_amp>+<J_U,U_amp>+S_boundary[U_amp,W].",
            "acceptance_requirements": "source_path; equation_anchor; parent field list; L_U domain/units; branch; proof the clause exists before local readout",
            "status": "OPEN_PARENT_ACTION_SOURCE_REQUEST",
            "ready_for_runner": False,
        },
        {
            "request_id": "REQ2874_1_hessian_block",
            "needed_clause": "H_CC,H_CR,H_RR or L_U source row",
            "exact_request": "Supply the parent Hessian block and verify H_CC=sigma_R^2 L_U, H_CR=-sigma_R L_U, H_RR=L_U, det(H)=0, and sigma_R=-H_CR/H_RR=-H_CC/H_CR.",
            "acceptance_requirements": "symbolic or numeric entries; units; operator domain; sign convention; no post-fit sigma insertion",
            "status": "OPEN_PARENT_HESSIAN_REQUEST",
            "ready_for_runner": False,
        },
        {
            "request_id": "REQ2874_2_source_covector",
            "needed_clause": "parallel source covector/no-rescaling owner",
            "exact_request": "Show j_amp=J_U*(-sigma_R_source_sign,1), with J_U and the source measure parent-defined, and prove independent rescalings of J_CAB and J_R are not legal.",
            "acceptance_requirements": "J_U source; worldtube/source measure; current object-language slot; no hidden orthogonal source marker",
            "status": "OPEN_PARENT_CURRENT_REQUEST",
            "ready_for_runner": False,
        },
        {
            "request_id": "REQ2874_3_omega_dc_vertical",
            "needed_clause": "actual vertical generator rather than guessed doublet",
            "exact_request": "Map (DC_amp)^dagger epsilon to Omega_parent^flat(v_amp[epsilon]) and show Dq[v_amp]=0 field-by-field on parent, matter/readout and boundary variables.",
            "acceptance_requirements": "Theta/Omega; DC_amp; reduced inverse; q-map; v_amp field action; boundary variables",
            "status": "OPEN_GEOMETRY_OWNER_REQUEST",
            "ready_for_runner": False,
        },
        {
            "request_id": "REQ2874_4_boundary_readout",
            "needed_clause": "boundary/common-Green/measured-GM descent",
            "exact_request": "Prove surface_integral(K_amp+B_CAB+sigma_R_source_sign*B_R)=0 or include it as a finite charge row, then bind C_AB and delta_R to one exterior 4*pi Green/readout convention.",
            "acceptance_requirements": "boundary/corner theorem or row; range hierarchy; common sign; measured-GM and ordinary-matter descent",
            "status": "OPEN_BOUNDARY_READOUT_REQUEST",
            "ready_for_runner": False,
        },
    ]
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2874_0_action", "source-backed rank-one parent action supplied", "FAIL", "only ansatz/template rows exist"),
        ("GATE2874_1_hessian", "H_CC,H_CR,H_RR or L_U sourced", "FAIL", "formula ready but parent Hessian entries missing"),
        ("GATE2874_2_sigma", "sigma_R_source_sign extracted before readout", "FAIL", "no accepted Hessian block or equivalent parent theorem"),
        ("GATE2874_3_source", "source covector is parent-parallel to n", "FAIL", "J_U/source measure/no-rescaling owner missing"),
        ("GATE2874_4_vertical", "v_amp is actual quotient vertical generator", "FAIL", "q, Dq, DC_amp and Omega inverse absent"),
        ("GATE2874_5_boundary", "boundary/improvement charge zero or included", "FAIL", "boundary/corner theorem missing"),
        ("GATE2874_6_common_green", "C_AB and delta_R share common exterior Green convention", "FAIL", "operator/range/sign convention not parent-signed"),
        ("GATE2874_7_matter_GM", "ordinary matter and measured GM descend correctly", "FAIL", "matter/readout/GM glue unsigned"),
        ("GATE2874_8_claim", "A_total/local-GR theorem route unlocked", "FAIL", "parent action clause rejected for now"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "claim_unlocked": False,
            }
        )
        for gate_id, criterion, result, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2874_0_rank_one_action_gate",
                "status": "REFUSED",
                "accepted_source_backed_action_rows": 0,
                "required_source_backed_action_rows": 1,
                "accepted_hessian_rows": 0,
                "required_hessian_rows": 1,
                "accepted_source_covector_rows": 0,
                "required_source_covector_rows": 1,
                "accepted_boundary_readout_rows": 0,
                "required_boundary_readout_rows": 1,
                "reason": "rank-one action is not parent-signed; fallback finite first-triplet acquisition selected",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2874_0_2875",
                "status": "selected_primary",
                "target_doc": "2875-Y5-R2FR-finite-first-triplet-acquisition-after-parent-action-clause-rejection-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_first_triplet_acquisition_after_parent_action_clause_rejection_under_AX1090_2875.py",
                "mission": "build source-backed finite acquisition rows for Q_CAB, q_R_eff, sigma_R_source_sign, common Green, boundary/tail, measured-GM/readout and full local vector; do not use theorem-zero unless the parent action clauses later close",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    pairs = [
        ("COPY2874_0_candidate", OUTPUTS["candidate_review"], BRANCH_OUTPUTS["candidate_copy"], "rank-one parent action candidate review nonclaim copy"),
        ("COPY2874_1_requests", OUTPUTS["requests"], BRANCH_OUTPUTS["request_copy"], "exact parent action/source/boundary requests nonclaim copy"),
        ("COPY2874_2_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["decision_copy"], "rank-one route demotion and fallback decision nonclaim copy"),
        ("COPY2874_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to finite first-triplet acquisition"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_source_backed_action",
        "parent_signed",
        "theorem_claimed",
        "ready_for_runner",
        "gate_passed",
        "claim_unlocked",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["sources"]
    candidates = rows_by_name["candidate_review"]
    hessian_rows = rows_by_name["hessian"]
    rejection_rows = rows_by_name["rejection"]
    decision = rows_by_name["decision"]
    requests = rows_by_name["requests"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2874_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2874_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2874_2_candidate_review_complete", len(candidates) >= 8 and not any(row["accepted_source_backed_action"] for row in candidates), "all action candidates reviewed and none accepted as source-backed"),
        ("VAL2874_3_hessian_formula_recorded", any(row["audit_id"] == "HRA2874_1_rank_one_hessian" and "H_amp=n^T L_U n" in row["formula"] for row in hessian_rows), "rank-one Hessian formula recorded"),
        ("VAL2874_4_parent_clause_rejected", any(row["rejection_id"] == "REJ2874_6_total_route" and row["verdict"] == "DEMOTE_TO_CLOSURE_ONLY_CURRENT_STATUS" for row in rejection_rows), "parent identity theorem route demoted to closure-only"),
        ("VAL2874_5_fallback_selected", any(row["decision_id"] == "DEC2874_3_fallback" and row["result"] == "SELECTED" for row in decision), "finite first-triplet acquisition selected"),
        ("VAL2874_6_exact_requests_open", len(requests) >= 5 and all(row["status"].startswith("OPEN_") for row in requests), "exact source requests emitted and left open"),
        ("VAL2874_7_gates_fail_closed", all(row["result"] == "FAIL" and row["gate_passed"] is False for row in gates), "all acceptance gates fail closed"),
        ("VAL2874_8_runner_refused", runner[0]["status"] == "REFUSED" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2874_9_next_target_2875", next_target[0]["next_id"] == "NEXT2874_0_2875" and next_target[0]["selected"] is True, "2875 finite acquisition selected next"),
        ("VAL2874_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2874_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2874_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2874_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2874_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2874_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2874_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2874_OVERALL",
            "passed": overall,
            "detail": "2874 searched the exact rank-one amplitude parent-action clause, found only ansatz/template/formal rows, rejected theorem promotion, kept the route closure-only, and selected finite first-triplet acquisition for 2875.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2874 - Y5 R2FR Rank-One Amplitude Parent Action Clause Search Under AX1090

Status: `Y5_R2FR_2874_rank_one_parent_action_clause_not_source_backed_route_demoted_to_closure_only_2875_next`

## Private Verdict

2874 did the narrow search 2873 asked for. The rank-one mechanism is still mathematically attractive:

`U_amp = delta_R - sigma_R_source_sign*C_AB`, `n=(-sigma_R_source_sign,1)`, `H_amp=n^T L_U n`, and `j_amp=J_U n`.

If those clauses were parent-signed, the first-triplet current identity would be derived instead of fitted. But the current corpus only contains ansatz/template/formal-map versions of that clause. There is no accepted source-backed parent action block, parent Hessian block, source covector, boundary/readout descent, or actual quotient-vertical generator.

So the verdict is fail-closed but not dead: keep the rank-one route as a closure candidate, do not use it for `A_total`, local-GR, Newton, R10, PPN, clock, orbital, or WEP claims, and move next to finite first-triplet acquisition.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Action Clause Candidate Review

{md_table(rows_by_name["candidate_review"], ["candidate_id", "candidate", "evidence_status", "accepted_source_backed_action", "reason_not_accepted", "valid_for_claim"])}

## Rank-One Hessian Extraction Audit

{md_table(rows_by_name["hessian"], ["audit_id", "object", "formula", "status", "missing_for_acceptance", "parent_signed", "valid_for_claim"])}

## Parent Origin Rejection Ledger

{md_table(rows_by_name["rejection"], ["rejection_id", "claim_tested", "verdict", "reason", "reopen_condition", "valid_for_claim"])}

## Demotion And Fallback Decision

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Exact Source Requests

{md_table(rows_by_name["requests"], ["request_id", "needed_clause", "exact_request", "status", "ready_for_runner", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_source_backed_action_rows", "accepted_hessian_rows", "accepted_source_covector_rows", "accepted_boundary_readout_rows", "reason", "runner_ready", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "candidate_review": candidate_review_rows(),
        "hessian": hessian_audit_rows(),
        "rejection": rejection_ledger_rows(),
        "decision": decision_rows(),
        "requests": exact_request_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs(rows_by_name)
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2874_OVERALL")
    print(f"VAL2874_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
