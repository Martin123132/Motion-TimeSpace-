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

DOC = ROOT / "2873-Y5-R2FR-first-triplet-parent-source-current-identity-reentry-under-AX1090.md"

SRC_2872_DOC = ROOT / "2872-Y5-R2FR-qReff-parent-source-equation-or-finite-row-under-AX1090.md"
SRC_2872_NEXT = RESIDUALS / "P8_Y5_R2FR_2872_NEXT_TARGET.csv"
SRC_2872_QREFF_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_REQUEST = RESIDUALS / "P8_Y5_R2FR_2872_NARROW_SOURCE_REQUEST.csv"
SRC_2872_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2872_VALIDATION.csv"
SRC_2871_QCAB_LAW = RESIDUALS / "P8_Y5_R2FR_2871_QCAB_SOURCE_EQUATION_AUDIT.csv"
SRC_2871_REQUEST = RESIDUALS / "P8_Y5_R2FR_2871_NARROW_SOURCE_REQUEST.csv"
SRC_2871_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2871_VALIDATION.csv"

SRC_2851_COMMON = RESIDUALS / "P8_Y5_R2FR_2851_COMMON_CURRENT_ANSATZ.csv"
SRC_2851_PROOF = RESIDUALS / "P8_Y5_R2FR_2851_ALGEBRAIC_PROOF_ATTEMPT.csv"
SRC_2851_NOGO = RESIDUALS / "P8_Y5_R2FR_2851_NO_GO_TUNING_LEDGER.csv"
SRC_2851_REQ = RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv"
SRC_2852_ACCEPT = RESIDUALS / "P8_Y5_R2FR_2852_OWNER_ACCEPTANCE_TEST.csv"
SRC_2853_REENTRY = RESIDUALS / "P8_Y5_R2FR_2853_PARENT_ACTION_REENTRY_HOOK.csv"
SRC_2855_EQUATION_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"

SRC_2866_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv"
SRC_2866_VARIATION = RESIDUALS / "P8_Y5_R2FR_2866_VARIATIONAL_DERIVATION_CHECK.csv"
SRC_2866_REENTRY = RESIDUALS / "P8_Y5_R2FR_2866_REENTRY_ACCEPTANCE_GATE.csv"
SRC_2866_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2866_VALIDATION.csv"
SRC_2867_HESSIAN = RESIDUALS / "P8_Y5_R2FR_2867_HESSIAN_FACTORISATION_TEST.csv"
SRC_2867_ROUTE = RESIDUALS / "P8_Y5_R2FR_2867_SIGMA_ORIGIN_ROUTE_AUDIT.csv"
SRC_2867_VERTICAL = RESIDUALS / "P8_Y5_R2FR_2867_VERTICAL_GENERATOR_DERIVATION_GATE.csv"
SRC_2867_DQ = RESIDUALS / "P8_Y5_R2FR_2867_QUOTIENT_DQ_GATE.csv"
SRC_2867_DCO = RESIDUALS / "P8_Y5_R2FR_2867_DCDAGGER_OMEGA_GATE.csv"
SRC_2867_GUARDS = RESIDUALS / "P8_Y5_R2FR_2867_CLAIM_GUARDS.csv"
SRC_2867_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2867_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2867_VALIDATION.csv"

SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_PARENT_SOURCE = RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv"
SRC_PARENT_DECISION = RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_DECISION.csv"
SRC_WARD_CONTRACT = RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv"
SRC_SOURCE_CURRENT_CONTRACT = RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_PARENT_ACTION_TERMS = RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2873_SOURCE_REGISTER.csv",
    "review": RESIDUALS / "P8_Y5_R2FR_2873_PARENT_IDENTITY_EVIDENCE_REVIEW.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_2873_REENTRY_DERIVATION_AUDIT.csv",
    "owner_gate": RESIDUALS / "P8_Y5_R2FR_2873_OWNER_CLAUSE_GATE.csv",
    "request": RESIDUALS / "P8_Y5_R2FR_2873_PARENT_ACTION_CLAUSE_REQUEST.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2873_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2873_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2873_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2873_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2873_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2873_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "derivation_copy": LOCAL_BOUNDS / "RAB_FIRST_TRIPLET_PARENT_IDENTITY_2873_NONCLAIM.csv",
    "request_copy": SOURCE_WEIGHT / "RAB_FIRST_TRIPLET_PARENT_ACTION_REQUEST_2873_NONCLAIM.csv",
    "owner_copy": BETA_DOCS / "RAB_FIRST_TRIPLET_OWNER_CLAUSE_GATE_2873_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2873_rank_one_amplitude_action_clause_search_NEXT.csv",
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
        ("SRC2873_0_2872_doc", SRC_2872_DOC, "NEXT2872_0_2873;VAL2872_OVERALL", "2872 selected first-triplet parent re-entry"),
        ("SRC2873_1_2872_next", SRC_2872_NEXT, "NEXT2872_0_2873", "handoff to 2873"),
        ("SRC2873_2_2872_qreff_law", SRC_2872_QREFF_LAW, "LAW2872_1_compact_source_charge;LAW2872_5_common_amplitude", "q_R_eff source contract"),
        ("SRC2873_3_2872_request", SRC_2872_REQUEST, "REQ2872_QREFF_PARENT_SOURCE_ROW", "q_R_eff narrow request"),
        ("SRC2873_4_2872_validation", SRC_2872_VALIDATION, "VAL2872_OVERALL", "2872 validation"),
        ("SRC2873_5_2871_qcab_law", SRC_2871_QCAB_LAW, "LAW2871_1_operator_source_contract;LAW2871_5_common_green_sign", "Q_CAB source contract"),
        ("SRC2873_6_2871_request", SRC_2871_REQUEST, "REQ2871_QCAB_PARENT_SOURCE_ROW", "Q_CAB narrow request"),
        ("SRC2873_7_2871_validation", SRC_2871_VALIDATION, "VAL2871_OVERALL", "2871 validation"),
        ("SRC2873_8_2851_common", SRC_2851_COMMON, "ANS2851_0_general_source_doublet;ANS2851_1_candidate_owner_ratio", "common-current ansatz"),
        ("SRC2873_9_2851_proof", SRC_2851_PROOF, "ALG2851_2_zero_condition;ALG2851_4_no_free_lunch", "algebraic proof/no-free-lunch"),
        ("SRC2873_10_2851_nogo", SRC_2851_NOGO, "NG2851_1_current_rescaling;NG2851_3_boundary_shift", "tuning and boundary no-go"),
        ("SRC2873_11_2851_req", SRC_2851_REQ, "REQ2851_1_symmetry_owner;REQ2851_2_current_owner;REQ2851_4_boundary_silence", "parent signature requirements"),
        ("SRC2873_12_2852_accept", SRC_2852_ACCEPT, "OWN2852_1_no_independent_rescaling;OWN2852_5_verdict", "source-doublet owner acceptance failure"),
        ("SRC2873_13_2853_reentry", SRC_2853_REENTRY, "RE2853_0_parent_source_equation;RE2853_1_symmetry_owner", "prior parent re-entry hook"),
        ("SRC2873_14_2855_equation", SRC_2855_EQUATION_DRAFT, "PEQ2855_0_CAB_source;PEQ2855_1_R_source;PEQ2855_3_amp_current_identity", "draft source-current identity"),
        ("SRC2873_15_2866_contract", SRC_2866_CONTRACT, "PACT2866_2_invariant;PACT2866_4_source_split;PACT2866_6_boundary", "minimal parent action contract"),
        ("SRC2873_16_2866_variation", SRC_2866_VARIATION, "VAR2866_2_source_variation;VAR2866_4_integrated_charge;VAR2866_6_claim_status", "variational derivation check"),
        ("SRC2873_17_2866_reentry", SRC_2866_REENTRY, "RE2866_0_parent_action;RE2866_5_finite_rows", "re-entry acceptance gate"),
        ("SRC2873_18_2866_validation", SRC_2866_VALIDATION, "VAL2866_OVERALL", "2866 validation"),
        ("SRC2873_19_2867_hessian", SRC_2867_HESSIAN, "HESS2867_1_rank_one_H;HESS2867_3_source_covector;HESS2867_5_verdict", "rank-one Hessian/source covector test"),
        ("SRC2873_20_2867_route", SRC_2867_ROUTE, "SIGROUTE2867_0_hessian;SIGROUTE2867_4_source_doublet;SIGROUTE2867_5_boundary_matter", "sigma/current route audit"),
        ("SRC2873_21_2867_vertical", SRC_2867_VERTICAL, "VGEN2867_2_actual_Dq;VGEN2867_6_verdict", "vertical generator gate"),
        ("SRC2873_22_2867_dq", SRC_2867_DQ, "DQ2867_0_chain_rule;DQ2867_4_verdict", "quotient Dq gate"),
        ("SRC2873_23_2867_dco", SRC_2867_DCO, "DCO2867_0_precise_map;DCO2867_6_verdict", "DCdagger/Omega gate"),
        ("SRC2873_24_2867_guards", SRC_2867_GUARDS, "GUARD2867_2_no_Uamp_theorem;GUARD2867_3_no_A_total_score", "claim guards"),
        ("SRC2873_25_2867_demotion", SRC_2867_DEMOTION, "DEM2867_0_Uamp_route;DEM2867_1_reopen_condition", "U_amp closure demotion/reopen condition"),
        ("SRC2873_26_2867_validation", SRC_2867_VALIDATION, "VAL2867_OVERALL", "2867 validation"),
        ("SRC2873_27_2844_flux", SRC_2844_FLUX, "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "A_total algebra"),
        ("SRC2873_28_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_1_source_current;CONTRACT2844_2_boundary;CONTRACT2844_5_sign", "amplitude source-current/sign contract"),
        ("SRC2873_29_parent_source", SRC_PARENT_SOURCE, "I499_3_parent_source_identity;I499_4_closed_flux_sufficient_conditions", "general parent source identity template"),
        ("SRC2873_30_parent_decision", SRC_PARENT_DECISION, "D499_0_identity;D499_4_promotion", "general parent source identity decision"),
        ("SRC2873_31_ward_contract", SRC_WARD_CONTRACT, "C1_exact_owner_decomposition;C2_zero_owner_flux;C3_closed_calibrated_mass_current", "Ward source-owner contract"),
        ("SRC2873_32_source_current_contract", SRC_SOURCE_CURRENT_CONTRACT, "SC4_no_nonHilbert_source_current;SC5_zero_compact_boundary_flux;SC6_closed_calibrated_mass_projector", "source-current Ward universality contract"),
        ("SRC2873_33_parent_action_terms", SRC_PARENT_ACTION_TERMS, "A1_source_owner_decomposition;A3_boundary_class_topological;A4_mass_flux_projector", "parent action source-owner terms"),
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


def evidence_review_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "review_id": "REV2873_0_qcab_contract",
            "quantity": "Q_CAB",
            "source_path": str(SRC_2871_QCAB_LAW),
            "source_anchor": "LAW2871_1_operator_source_contract",
            "evidence": "Q_CAB=int_W J_CAB dV plus boundary term under a parent L_CAB/source convention",
            "verdict": "CONTRACT_AVAILABLE_NOT_PARENT_ACCEPTED",
            "reason_not_accepted": "L_CAB, J_CAB, B_CAB and common sign/Green convention remain unowned",
        },
        {
            "review_id": "REV2873_1_qreff_contract",
            "quantity": "q_R_eff",
            "source_path": str(SRC_2872_QREFF_LAW),
            "source_anchor": "LAW2872_1_compact_source_charge",
            "evidence": "q_R_eff=-int_W S_R/Z_R d^3x plus boundary term in the normalized Green branch",
            "verdict": "CONTRACT_AVAILABLE_NOT_PARENT_ACCEPTED",
            "reason_not_accepted": "S_R/Z_R, ell_R, H_R, measured-GM and common convention remain unowned",
        },
        {
            "review_id": "REV2873_2_common_current_ansatz",
            "quantity": "J_CAB+sigma_R*J_R",
            "source_path": str(SRC_2851_COMMON),
            "source_anchor": "ANS2851_1_candidate_owner_ratio",
            "evidence": "source-doublet ratio (a_C,a_R)=kappa_star*(-sigma_R,1) gives Q_CAB=-sigma_R*q_R_eff",
            "verdict": "CONDITIONAL_ZERO_TEMPLATE",
            "reason_not_accepted": "ratio is not symmetry/current owned before fitting",
        },
        {
            "review_id": "REV2873_3_variational_source_split",
            "quantity": "J_CAB+sigma_R*J_R",
            "source_path": str(SRC_2866_VARIATION),
            "source_anchor": "VAR2866_2_source_variation",
            "evidence": "S_src=<J_U,U_amp> gives J_CAB=-sigma_R*J_U and J_R=J_U",
            "verdict": "CONDITIONAL_VARIATION_VALID",
            "reason_not_accepted": "J_U, measure, sign convention and parent action provenance remain unsourced",
        },
        {
            "review_id": "REV2873_4_integrated_charge",
            "quantity": "Q_CAB+sigma_R*q_R_eff",
            "source_path": str(SRC_2866_VARIATION),
            "source_anchor": "VAR2866_4_integrated_charge",
            "evidence": "integrating the current identity gives Q_CAB+sigma_R*q_R_eff=boundary/improvement",
            "verdict": "BOUNDARY_CONDITIONAL",
            "reason_not_accepted": "boundary/corner theorem missing",
        },
        {
            "review_id": "REV2873_5_hessian_source_covector",
            "quantity": "sigma_R_source_sign",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_3_source_covector",
            "evidence": "j_amp=J_U*n gives j_C=-sigma J_U, j_R=J_U and J_CAB+sigma J_R=0",
            "verdict": "DERIVED_CONDITIONAL",
            "reason_not_accepted": "J_U, worldtube measure, and parent Hessian/operator entries are missing",
        },
        {
            "review_id": "REV2873_6_rescaling_guard",
            "quantity": "source-current owner",
            "source_path": str(SRC_2852_ACCEPT),
            "source_anchor": "OWN2852_1_no_independent_rescaling",
            "evidence": "the 1078 current-rescaling counterexample survives",
            "verdict": "OWNER_TEST_FAILS",
            "reason_not_accepted": "independent projection/current rescaling is not forbidden by a parent owner",
        },
        {
            "review_id": "REV2873_7_uamp_demotion",
            "quantity": "U_amp route",
            "source_path": str(SRC_2867_DEMOTION),
            "source_anchor": "DEM2867_0_Uamp_route",
            "evidence": "U_amp route is demoted to closure-only because sigma origin and vertical generator are not parent-derived",
            "verdict": "CLOSURE_ONLY_CURRENT_STATUS",
            "reason_not_accepted": "re-entry requires source-backed parent Hessian/Omega/Dq/boundary/matter certificate",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_parent_identity": False,
                "theorem_zero_accepted": False,
                "parent_source_row_accepted": False,
            }
        )
    return [add_common(row) for row in rows]


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "DER2873_0_define_doublet",
            "step": "Define amplitude doublet and invariant",
            "conditional_math": "Y_amp=(C_AB,delta_R)^T, n=(-sigma_R_source_sign,1), U_amp=n dot Y_amp=delta_R-sigma_R_source_sign*C_AB.",
            "result": "vertical candidate v_amp=(1,sigma_R_source_sign) satisfies n(v_amp)=0",
            "status": "ALGEBRAICALLY_VALID",
            "missing_for_theorem": "parent field chart, sigma origin and actual quotient/vertical generator",
            "source_path": str(SRC_2867_HESSIAN),
            "source_anchor": "HESS2867_0_amplitude_doublet",
        },
        {
            "derivation_id": "DER2873_1_rank_one_action",
            "step": "Assume rank-one parent amplitude action",
            "conditional_math": "S_amp=1/2<U_amp,L_U U_amp> + <J_U,U_amp> + S_boundary[U_amp,W].",
            "result": "H_amp=n^T L_U n and source covector j_amp=J_U n share one parent direction",
            "status": "CONDITIONAL_ACTION_TEMPLATE",
            "missing_for_theorem": "source-backed L_U, J_U, worldtube measure, boundary differentiability and parent provenance",
            "source_path": str(SRC_2866_CONTRACT),
            "source_anchor": "PACT2866_3_action;PACT2866_4_source_split",
        },
        {
            "derivation_id": "DER2873_2_local_current_identity",
            "step": "Vary the parent action with respect to C_AB and delta_R",
            "conditional_math": "j_CAB=-sigma_R_source_sign*J_U and j_R=J_U.",
            "result": "J_CAB + sigma_R_source_sign*J_R = 0, or dK_amp if improvement terms are retained",
            "status": "DERIVED_CONDITIONAL_IDENTITY",
            "missing_for_theorem": "parent source current owner, no independent rescaling, and sign/source convention",
            "source_path": str(SRC_2866_VARIATION),
            "source_anchor": "VAR2866_2_source_variation",
        },
        {
            "derivation_id": "DER2873_3_integrated_charge_identity",
            "step": "Integrate over the local worldtube",
            "conditional_math": "Q_CAB + sigma_R_source_sign*q_R_eff = integral_W(J_CAB+sigma_R_source_sign*J_R)dV + surface_integral_boundary(K_amp+B_CAB+sigma_R_source_sign*B_R).",
            "result": "if the parent current identity and boundary silence hold, Q_CAB=-sigma_R_source_sign*q_R_eff",
            "status": "DERIVED_CONDITIONAL_CHARGE_IDENTITY",
            "missing_for_theorem": "boundary/corner silence theorem or explicit included boundary charge row",
            "source_path": str(SRC_2855_EQUATION_DRAFT),
            "source_anchor": "PEQ2855_3_amp_current_identity",
        },
        {
            "derivation_id": "DER2873_4_local_amplitude",
            "step": "Insert the charge identity into the leading local amplitude",
            "conditional_math": "A_total=(sigma_R_source_sign*q_R_eff+Q_CAB)/(4*pi).",
            "result": "A_total=0 for the first one-over-r gamma lane if the parent identity is accepted",
            "status": "CONDITIONAL_THEOREM_TARGET",
            "missing_for_theorem": "common 4*pi Green convention, Q_CAB/q_R_eff source acceptance, sigma owner, and no tail/full-vector leakage",
            "source_path": str(SRC_2844_FLUX),
            "source_anchor": "FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition",
        },
        {
            "derivation_id": "DER2873_5_no_rescaling_guard",
            "step": "Test whether the identity is forced or tunable",
            "conditional_math": "An arbitrary source vector j=(j_C,j_R) cancels only if j_C/j_R=-sigma_R_source_sign.",
            "result": "without a parent-parallel-source theorem, independent rescaling breaks A_total=0",
            "status": "NO_TUNING_GUARD_ACTIVE",
            "missing_for_theorem": "object-language/current owner forbidding independent source/projection rescaling",
            "source_path": str(SRC_2851_PROOF),
            "source_anchor": "ALG2851_4_no_free_lunch",
        },
        {
            "derivation_id": "DER2873_6_verdict",
            "step": "2873 re-entry verdict",
            "conditional_math": "The parent identity is exact if the rank-one action/current/boundary clauses are parent-signed.",
            "result": "conditional mechanism found; theorem not promoted; A_total remains locked",
            "status": "MECHANISM_CONDITIONAL_PARENT_CLAUSES_UNSIGNED",
            "missing_for_theorem": "rank-one parent action/Hessian, source covector, common Green/sign convention, boundary silence, no-rescaling owner, matter/GM/full-vector descent",
            "source_path": str(SRC_2867_DEMOTION),
            "source_anchor": "DEM2867_0_Uamp_route;DEM2867_1_reopen_condition",
        },
    ]
    for row in rows:
        row.update(
            {
                "algebraically_valid": row["status"] not in {"MECHANISM_CONDITIONAL_PARENT_CLAUSES_UNSIGNED"},
                "parent_signed": False,
                "theorem_claimed": False,
                "atotal_unlocked": False,
            }
        )
    return [add_common(row) for row in rows]


def owner_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("OWN2873_0_field_chart", "parent field chart owns Y_amp=(C_AB,delta_R)", "FAIL", "field-by-field parent map q(Phi) and matter lift remain unsigned", SRC_2866_CONTRACT, "PACT2866_0_fields"),
        ("OWN2873_1_sigma_origin", "sigma_R_source_sign derived before readout", "FAIL", "quadratic action, Hessian entries, metric signature and Green orientation are not parent-signed", SRC_2867_HESSIAN, "HESS2867_2_extract_sigma"),
        ("OWN2873_2_rank_one_hessian", "H_amp=n^T L_U n is a parent Hessian block", "FAIL", "H_CC, H_CR, H_RR and L_U are absent from current parent action", SRC_2867_HESSIAN, "HESS2867_1_rank_one_H"),
        ("OWN2873_3_source_covector", "source covector is parent-parallel to n", "FAIL", "J_U and worldtube/source measure are not sourced", SRC_2867_HESSIAN, "HESS2867_3_source_covector"),
        ("OWN2873_4_no_rescaling", "one owner forbids independent current/projection rescaling", "FAIL", "owner acceptance test says the current-rescaling counterexample survives", SRC_2852_ACCEPT, "OWN2852_1_no_independent_rescaling"),
        ("OWN2873_5_common_green", "C_AB and delta_R use one exterior 4*pi convention", "FAIL", "operator pair, range hierarchy, boundary class and sign orientation remain conditional", SRC_2866_CONTRACT, "PACT2866_5_common_Green"),
        ("OWN2873_6_boundary", "K_amp+B_CAB+sigma_R B_R boundary charge is zero or explicitly included", "FAIL", "boundary/corner silence theorem missing", SRC_2866_CONTRACT, "PACT2866_6_boundary"),
        ("OWN2873_7_quotient_vertical", "v_amp is actual parent vertical generator with Dq[v_amp]=0", "FAIL", "actual q/v_amp/readout functor is not sourced", SRC_2867_DQ, "DQ2867_4_verdict"),
        ("OWN2873_8_matter_GM", "ordinary matter and measured GM descend to quotient/basic variables", "FAIL", "matter descent and measured-GM source measure remain unsigned", SRC_2866_CONTRACT, "PACT2866_7_matter_readout"),
        ("OWN2873_9_full_vector", "full local PPN/Newton residual vector closes in same branch", "FAIL", "beta/preferred/source/endpoint/clock/orbital/q_loc rows remain open", SRC_2866_CONTRACT, "PACT2866_8_full_vector"),
    ]
    return [
        add_common(
            {
                "owner_id": owner_id,
                "required_clause": clause,
                "result": result,
                "reason": reason,
                "source_path": str(source_path),
                "source_anchor": source_anchor,
                "clause_passed": False,
                "parent_owned": False,
                "claim_unlocked": False,
            }
        )
        for owner_id, clause, result, reason, source_path, source_anchor in specs
    ]


def request_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "request_id": "REQ2873_0_rank_one_parent_action",
            "needed_clause": "rank-one amplitude parent action",
            "exact_request": "Provide a source-backed parent action/equation anchor for Y_amp=(C_AB,delta_R)^T with U_amp=delta_R-sigma_R_source_sign*C_AB and S_amp=1/2<U_amp,L_U U_amp>+<J_U,U_amp>+S_boundary[U_amp,W], or an equivalent parent theorem.",
            "acceptance_requirements": "source_path; equation_anchor; H_CC,H_CR,H_RR or L_U; sigma extraction; measure; branch id; units; proof the term exists before local PPN readout",
            "status": "OPEN_PARENT_ACTION_CLAUSE_REQUEST",
        },
        {
            "request_id": "REQ2873_1_source_current_owner",
            "needed_clause": "parallel source covector/no-rescaling owner",
            "exact_request": "Show that the source covector is j_amp=J_U*(-sigma_R_source_sign,1), so J_CAB+sigma_R_source_sign*J_R=dK_amp, and prove independent rescalings of J_CAB/J_R are illegal.",
            "acceptance_requirements": "parent current definition; object-language slot; no auxiliary plateau multiplier; no fitted ratio; no hidden orthogonal source marker",
            "status": "OPEN_PARENT_ACTION_CLAUSE_REQUEST",
        },
        {
            "request_id": "REQ2873_2_boundary_green_readout",
            "needed_clause": "boundary/common-Green/readout closure",
            "exact_request": "Prove surface_integral_boundary(K_amp+B_CAB+sigma_R_source_sign*B_R)=0 or include it as an explicit charge row, and bind C_AB and delta_R to one 4*pi exterior Green convention and measured-GM/readout branch.",
            "acceptance_requirements": "boundary/corner theorem or finite boundary row; common Green/range hierarchy; sigma sign; matter/GM descent; full local residual vector guard",
            "status": "OPEN_PARENT_ACTION_CLAUSE_REQUEST",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_clause_supplied": False,
                "ready_for_runner": False,
            }
        )
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2873_0_identity", "J_CAB+sigma_R J_R=dK_amp parent identity accepted", "FAIL", "identity is conditional; parent current/action owner unsigned"),
        ("GATE2873_1_action", "rank-one parent action/Hessian supplied", "FAIL", "Hessian/action entries and L_U/J_U are not sourced"),
        ("GATE2873_2_sigma", "sigma_R_source_sign derived before readout", "FAIL", "sigma origin remains conditional"),
        ("GATE2873_3_no_rescaling", "independent current/projection rescaling forbidden", "FAIL", "rescaling counterexample survives"),
        ("GATE2873_4_boundary", "boundary/improvement term zero or included", "FAIL", "boundary/corner theorem missing"),
        ("GATE2873_5_common_green", "shared 4*pi Green convention accepted", "FAIL", "operator/range/sign convention not parent-signed"),
        ("GATE2873_6_matter_GM", "matter and GM readout descend correctly", "FAIL", "matter/GM source glue remains unsigned"),
        ("GATE2873_7_A_total", "A_total runner unlocked by theorem", "FAIL", "theorem route remains closure-only; finite first-triplet rows still absent"),
        ("GATE2873_8_local_GR", "local GR/Newton reduction claim allowed", "FAIL", "full PPN/source/clock/orbital vector not derived"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "runner_ready": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2873_0_PARENT_IDENTITY_gate",
                "status": "REFUSED",
                "accepted_parent_identity_rows": 0,
                "required_parent_identity_rows": 1,
                "accepted_first_triplet_rows": 0,
                "required_first_triplet_rows": 4,
                "reason": "the parent source-current identity is algebraically sharp but not parent-signed; A_total and local-GR scoring remain locked",
                "runner_ready": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2873_0_mechanism", "Attempt the parent source-current identity.", "CONDITIONAL_MECHANISM_FOUND", "rank-one U_amp action would derive J_CAB+sigma_R J_R=dK_amp and Q_CAB=-sigma_R q_R_eff if parent-signed."),
        ("DEC2873_1_claim", "Promote the identity to theorem-zero.", "REJECTED", "rank-one action/Hessian, J_U, no-rescaling owner, boundary and common Green clauses are unsigned."),
        ("DEC2873_2_runner", "Unlock A_total runner.", "REFUSED", "parent theorem route remains closure-only and finite first-triplet rows are absent."),
        ("DEC2873_3_request", "Emit exact parent-action clause request.", "COMPLETE", "the missing action/current/boundary clauses are now specified without ambiguity."),
        ("DEC2873_4_next", "Search specifically for the rank-one amplitude parent-action clause.", "SELECTED_2874", "this is the least-circular derivation route before falling back to finite-row empirical acquisition."),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2873_0_2874",
                "status": "selected_primary",
                "target_doc": "2874-Y5-R2FR-rank-one-amplitude-parent-action-clause-search-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_rank_one_amplitude_parent_action_clause_search_under_AX1090_2874.py",
                "mission": "search/extract or constructively reject a source-backed parent action clause with U_amp=delta_R-sigma_R*C_AB, rank-one Hessian H=n^T L_U n, source covector J_U n, common Green convention, and boundary/readout descent; if absent, demote the parent identity route explicitly and return to finite first-triplet acquisition",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2873_0_derivation", OUTPUTS["derivation"], BRANCH_OUTPUTS["derivation_copy"], "first-triplet parent identity derivation nonclaim copy"),
        ("COPY2873_1_request", OUTPUTS["request"], BRANCH_OUTPUTS["request_copy"], "parent action clause request nonclaim copy"),
        ("COPY2873_2_owner", OUTPUTS["owner_gate"], BRANCH_OUTPUTS["owner_copy"], "owner clause gate nonclaim copy"),
        ("COPY2873_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to rank-one parent action clause search"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_parent_identity",
        "theorem_zero_accepted",
        "parent_source_row_accepted",
        "parent_signed",
        "theorem_claimed",
        "atotal_unlocked",
        "clause_passed",
        "parent_owned",
        "claim_unlocked",
        "parent_clause_supplied",
        "ready_for_runner",
        "gate_passed",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    path_keys = {"source_path", "source_table", "copy_path"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key not in path_keys:
                    continue
                if value in {"", None}:
                    continue
                if not Path(str(value)).exists():
                    return False
    return True


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2873_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2873_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered source anchors were found"),
        ("VAL2873_2_evidence_review_complete", len(rows_by_name["review"]) >= 8 and all(not row["accepted_parent_identity"] for row in rows_by_name["review"]), "parent identity evidence reviewed and none accepted for claim"),
        ("VAL2873_3_derivation_conditional", any(row["derivation_id"] == "DER2873_2_local_current_identity" and row["status"] == "DERIVED_CONDITIONAL_IDENTITY" for row in rows_by_name["derivation"]), "conditional local current identity derived"),
        ("VAL2873_4_no_theorem_claimed", all(not row["theorem_claimed"] for row in rows_by_name["derivation"]), "no theorem promotion is claimed"),
        ("VAL2873_5_owner_gates_fail_closed", all(not row["clause_passed"] for row in rows_by_name["owner_gate"]), "all owner clauses fail closed"),
        ("VAL2873_6_request_open", len(rows_by_name["request"]) == 3 and all(row["status"] == "OPEN_PARENT_ACTION_CLAUSE_REQUEST" for row in rows_by_name["request"]), "exact parent action clause requests emitted"),
        ("VAL2873_7_acceptance_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["gates"]), "all acceptance gates fail closed"),
        ("VAL2873_8_runner_refused", all(row["status"] == "REFUSED" and not row["runner_ready"] for row in rows_by_name["runner"]), "runner remains refused"),
        ("VAL2873_9_next_target_2874", rows_by_name["next"][0]["next_id"] == "NEXT2873_0_2874", "rank-one parent action clause search selected next"),
        ("VAL2873_10_outputs_exist", all(path.exists() for path in output_paths), "all generated CSV outputs exist before validation write"),
        ("VAL2873_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2873_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2873_13_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local paths exist"),
        ("VAL2873_14_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2873_15_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2873_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2873_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
    rows.append(
        {
            "validation_id": "VAL2873_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2873 derived the conditional first-triplet parent source-current identity, rejected theorem promotion, kept A_total locked, emitted exact parent-action clause requests, and selected rank-one parent action clause search for 2874.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2873 - Y5 R2FR First Triplet Parent Source-Current Identity Re-entry Under AX1090",
        "",
        "Status: `Y5_R2FR_2873_parent_source_current_identity_conditional_mechanism_found_theorem_not_promoted_2874_next`",
        "",
        "## Private Verdict",
        "",
        "2873 is the cleanest derivation shot so far for the first-triplet amplitude problem. If the parent action owns the amplitude invariant",
        "",
        "`U_amp = delta_R - sigma_R_source_sign*C_AB`,",
        "",
        "and the source term is parent-parallel to that invariant, then variation gives `J_CAB=-sigma_R_source_sign*J_U`, `J_R=J_U`, hence `J_CAB+sigma_R_source_sign*J_R=0` up to owned improvement terms. Integrated over the worldtube, this gives `Q_CAB+sigma_R_source_sign*q_R_eff=0` if the boundary/improvement charge vanishes or is explicitly included.",
        "",
        "That would derive the first `A_total` cancellation rather than fitting it. But it is still conditional: the rank-one parent action/Hessian, source covector, no-rescaling owner, boundary silence, common Green convention, matter/GM descent, and full local residual vector are not parent-signed. So no local-GR/Newton claim and no `A_total` score are unlocked.",
        "",
        "The next move is not another vague hunt. It is a very specific search for the parent action clause: `H_amp=n^T L_U n`, `j_amp=J_U n`, with `n=(-sigma_R_source_sign,1)`, plus boundary/readout descent.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Parent Identity Evidence Review",
        "",
        markdown_table(rows["review"], ["review_id", "quantity", "source_path", "source_anchor", "verdict", "accepted_parent_identity", "reason_not_accepted", "valid_for_claim"]),
        "",
        "## Re-entry Derivation Audit",
        "",
        markdown_table(rows["derivation"], ["derivation_id", "step", "status", "result", "missing_for_theorem", "parent_signed", "theorem_claimed", "valid_for_claim"]),
        "",
        "## Owner Clause Gate",
        "",
        markdown_table(rows["owner_gate"], ["owner_id", "required_clause", "result", "reason", "clause_passed", "claim_unlocked", "valid_for_claim"]),
        "",
        "## Parent Action Clause Request",
        "",
        markdown_table(rows["request"], ["request_id", "needed_clause", "exact_request", "acceptance_requirements", "status", "ready_for_runner", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        markdown_table(rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        markdown_table(rows["runner"], ["runner_id", "status", "accepted_parent_identity_rows", "required_parent_identity_rows", "accepted_first_triplet_rows", "required_first_triplet_rows", "reason", "runner_ready", "score_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["review"] = evidence_review_rows()
    rows["derivation"] = derivation_rows()
    rows["owner_gate"] = owner_gate_rows()
    rows["request"] = request_rows()
    rows["gates"] = gate_rows()
    rows["runner"] = runner_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "review", "derivation", "owner_gate", "request", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2873_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2873_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
