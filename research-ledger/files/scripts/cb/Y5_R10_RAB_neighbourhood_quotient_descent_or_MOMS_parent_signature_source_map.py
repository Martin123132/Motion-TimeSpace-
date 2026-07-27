from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1486-Y5-R10-RAB-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1485_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1485_VALIDATION.csv"
PREV_DZERO = OUT / "P8_Y5_R10_1485_UNIVERSAL_MATTER_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
PREV_GENERATOR = OUT / "P8_Y5_R10_1485_V_WEP_GENERATOR_CONTRACT.csv"
PREV_FDERIV = OUT / "P8_Y5_R10_1485_FUNCTIONAL_DERIVATIVE_DEFINITION.csv"
PREV_SIGNATURE = OUT / "P8_Y5_R10_1485_PARENT_SIGNATURE_CLAUSE_GATES.csv"
PREV_PREF = OUT / "P8_Y5_R10_1485_NO_SOURCE_ONLY_PREFACTOR_GATES.csv"
PREV_LOCAL = OUT / "P8_Y5_R10_1485_LOCAL_GR_NEWTON_REDUCTION_VERDICT.csv"
PREV_IMPORT = OUT / "P8_Y5_R10_1485_C_PARENT_IMPORT_REFUSAL.csv"

CFC_943 = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
DER_943 = OUT / "P8_Y5_R10_943_DERIVATION_ATTEMPT.csv"
MFS_1045 = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
VLG_1045 = OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
PAC_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
ADG_1055 = OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv"
OLT_1066 = OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv"
ODR_1066 = OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv"
AM_1078 = OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv"
OL_1078 = OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv"
CO_1078 = OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv"
NCO_1079 = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
PCS_1009 = OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv"
SVR_1009 = OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv"
PVA_1008 = OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv"
QTA_1008 = OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv"
MOMS_1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
ZERO_1088 = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
SYN_1090 = OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv"
AX_1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
HT_1450 = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
NSSR_1450 = OUT / "P8_Y5_R10_1450_NO_SOURCE_ONLY_SLOT_REDUCTION_AUDIT.csv"
CON_1464 = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
CAL_1464 = OUT / "P8_Y5_R10_1464_COMMON_CALIBRATION_SILENCE_CONTRACT.csv"
GRC_1477 = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
SAL_1478 = OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv"
PREF_1479 = OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv"
HOM_1479 = OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv"

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1486_SOURCE_REGISTER.csv"
NEIGHBOURHOOD_DESCENT = OUT / "P8_Y5_R10_1486_NEIGHBOURHOOD_QUOTIENT_DESCENT_ATTEMPT.csv"
MOMS_SOURCE_MAP = OUT / "P8_Y5_R10_1486_MOMS_PARENT_SIGNATURE_SOURCE_MAP.csv"
CLAUSE_GATES = OUT / "P8_Y5_R10_1486_CLAUSE_ADOPTION_GATES.csv"
PARENT_ACTION_AUDIT = OUT / "P8_Y5_R10_1486_PARENT_ACTION_OBJECT_AUDIT.csv"
MATTER_FUNCTOR_AUDIT = OUT / "P8_Y5_R10_1486_MATTER_BUNDLE_FUNCTOR_AUDIT.csv"
NO_SHADOW_AUDIT = OUT / "P8_Y5_R10_1486_NO_SHADOW_READOUT_REENTRY_AUDIT.csv"
AXIOM_REFUSAL = OUT / "P8_Y5_R10_1486_AXIOM_ADOPTION_REFUSAL.csv"
LOCAL_REDUCTION = OUT / "P8_Y5_R10_1486_LOCAL_GR_NEWTON_REDUCTION_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1486_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1486_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1486_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1486_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1486"
QUAR_DESCENT = QUARANTINE / "NEIGHBOURHOOD_QUOTIENT_DESCENT_ATTEMPT_NONCLAIM.csv"
QUAR_MAP = QUARANTINE / "MOMS_PARENT_SIGNATURE_SOURCE_MAP_NONCLAIM.csv"
QUAR_AXIOMS = QUARANTINE / "AXIOM_ADOPTION_REFUSAL_NONCLAIM.csv"
BRANCH_DESCENT = BRANCH_COEFF / "neighbourhood_quotient_descent_attempt_nonclaim_1486.csv"
BRANCH_MAP = BRANCH_COEFF / "MOMS_parent_signature_source_map_nonclaim_1486.csv"
BRANCH_AXIOMS = BRANCH_COEFF / "axiom_adoption_refusal_nonclaim_1486.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1486_0_prev_next", PREV_NEXT, "1485 handoff"),
        ("SRC1486_1_prev_validation", PREV_VALIDATION, "1485 validation"),
        ("SRC1486_2_prev_dzero", PREV_DZERO, "1485 double-zero theorem attempt"),
        ("SRC1486_3_prev_generator", PREV_GENERATOR, "1485 V_WEP generator contract"),
        ("SRC1486_4_prev_fderiv", PREV_FDERIV, "1485 functional derivative definition"),
        ("SRC1486_5_prev_signature", PREV_SIGNATURE, "1485 parent signature gates"),
        ("SRC1486_6_prev_prefactor", PREV_PREF, "1485 no-source-only prefactor gates"),
        ("SRC1486_7_prev_local", PREV_LOCAL, "1485 local GR/Newton reduction verdict"),
        ("SRC1486_8_prev_import", PREV_IMPORT, "1485 C_parent import refusal"),
        ("SRC1486_9_CFC943", CFC_943, "coframe coupling contract"),
        ("SRC1486_10_DER943", DER_943, "quotient/coframe derivation attempt"),
        ("SRC1486_11_MFS1045", MFS_1045, "parent matter functor signature audit"),
        ("SRC1486_12_VLG1045", VLG_1045, "vertical lift descent gate"),
        ("SRC1486_13_PAC1055", PAC_1055, "parent action contract candidate"),
        ("SRC1486_14_ADG1055", ADG_1055, "contract adoption gates"),
        ("SRC1486_15_OLT1066", OLT_1066, "object-language typing audit"),
        ("SRC1486_16_ODR1066", ODR_1066, "operator domain rule audit"),
        ("SRC1486_17_AM1078", AM_1078, "action-measure proof attempt"),
        ("SRC1486_18_OL1078", OL_1078, "object language proof attempt"),
        ("SRC1486_19_CO1078", CO_1078, "current owner proof attempt"),
        ("SRC1486_20_NCO1079", NCO_1079, "narrow current owner theorem"),
        ("SRC1486_21_PCS1009", PCS_1009, "parent sector contract"),
        ("SRC1486_22_SVR1009", SVR_1009, "sector variation runner"),
        ("SRC1486_23_PVA1008", PVA_1008, "parent variation audit"),
        ("SRC1486_24_QTA1008", QTA_1008, "charge piece ledger"),
        ("SRC1486_25_MOMS1088", MOMS_1088, "MOMS signature clauses"),
        ("SRC1486_26_ZERO1088", ZERO_1088, "MOMS conditional zero theorem"),
        ("SRC1486_27_SYN1090", SYN_1090, "MOMS synthesis attempt"),
        ("SRC1486_28_AX1090", AX_1090, "missing axiom ledger"),
        ("SRC1486_29_HT1450", HT_1450, "source label forgetting theorem"),
        ("SRC1486_30_NSSR1450", NSSR_1450, "no source-only slot audit"),
        ("SRC1486_31_CON1464", CON_1464, "connected matter category"),
        ("SRC1486_32_CAL1464", CAL_1464, "calibration silence"),
        ("SRC1486_33_GRC1477", GRC_1477, "connected graph certificate"),
        ("SRC1486_34_SAL1478", SAL_1478, "single action-density line"),
        ("SRC1486_35_PREF1479", PREF_1479, "no-source-only prefactor theorem attempt"),
        ("SRC1486_36_HOM1479", HOM_1479, "Hom prefactor audit"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def neighbourhood_descent_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NQD1486_0_target",
            "Open-neighbourhood quotient descent",
            "There exists an open U around the compact local branch Phi0 such that S_ord[Phi,Psi,theta]=Sbar_ord[q(Phi),Psi_q,theta] and every V_WEP,X flow remains inside q-fibres in U.",
            "This is sufficient for C_parent_X=0 throughout U and hence the 1485 double-zero corollary.",
            "TARGET_EXACT",
            "parent-signed q, S_ord descent, matter lift, and no reentry clauses",
        ),
        (
            "NQD1486_1_chain_rule",
            "Pointwise vertical blindness",
            "If e_obs=Obs_e(q(Phi)) and Dq[V]=0, then Lie_V e_obs=0.",
            "DER943_0 and CFC943_1 give the exact chain-rule lemma.",
            "EXACT_CONDITIONAL_POINTWISE",
            "upgrade from pointwise lemma to open-neighbourhood parent functor",
        ),
        (
            "NQD1486_2_descent_gap",
            "Matter action descent on U",
            "S_ord must factor through q on an open set, not merely be written in desired variables at Phi0.",
            "MFS1045/PAC1055 write the desired contract but mark matter functor and constants unsigned.",
            "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "one parent action object plus matter bundle functor and fixed constants",
        ),
        (
            "NQD1486_3_reentry_gap",
            "No hidden/readout/domain reentry",
            "No shadow frame, source-only marker, domain selector, or post-variation readout may depend on the quotient-vertical direction.",
            "CFC943_6, MFS1045_4, PAC1055_3/5, ODR1066 retain this as a guard/obstruction.",
            "OBSTRUCTION_SURVIVES",
            "operator-domain exclusion or retained finite residuals",
        ),
        (
            "NQD1486_4_axiom_risk",
            "Closure-only adoption risk",
            "Adopting AX1090 clauses would close the route by stipulation rather than derivation.",
            "1090 explicitly marks AX1090_0..4 as missing axioms not adopted.",
            "AXIOM_ADOPTION_REFUSED",
            "derive/source rather than adopt closure axioms",
        ),
        (
            "NQD1486_5_verdict",
            "Neighbourhood descent status",
            "The theorem route is exact, but current evidence is still a source map of conditional clauses, not a parent-signed descent proof.",
            "No C_parent import or local-GR claim follows from 1486.",
            "NOT_CLOSED_SOURCE_MAP_BUILT",
            "prove/source parent action object and MOMS signature clauses",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "descent_id": descent_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "evidence_summary": evidence,
            "current_status": status,
            "missing_for_parent_claim": missing,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for descent_id, claim_piece, statement, evidence, status, missing in rows
    ]


def moms_source_map_rows() -> list[dict[str, Any]]:
    mapping = [
        (
            "MOMS1088_0_action_form",
            "parent ordinary-matter action form",
            "PAC1055_6;PCS1009_9;PVA1008_0;SYN1090_1",
            "single-action schema written and sector list exists",
            "no total parent action is varied across all sectors",
            "SCHEMA_AVAILABLE_NOT_DERIVED",
        ),
        (
            "MOMS1088_1_quotient_observables",
            "q-neighbourhood and observed coframe functor",
            "CFC943_0..1;DER943_0;MFS1045_0..1;PAC1055_0",
            "chain-rule vertical blindness exact as conditional",
            "q_loc/Obs_e not parent-selected on open neighbourhood for all local sectors",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        (
            "MOMS1088_2_matter_bundle",
            "ordinary matter bundle functor and vertical lift",
            "MFS1045_2..3;VLG1045_0..4;SYN1090_3",
            "fixed/gauge lift options are clean",
            "species-complete parent matter bundle functor and boundary class missing",
            "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
        ),
        (
            "MOMS1088_3_constant_superselection",
            "fixed constants and representation data",
            "CFC943_3;MFS1045_5;PAC1055_1..2;SYN1090_4",
            "fixed-representation route identified",
            "alpha/mass/clock constants not parent-signed as fixed or retained residuals",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
        ),
        (
            "MOMS1088_4_no_species_weights",
            "no w_A/action/source prefactors",
            "HT1450;NSSR1450;CON1464;GRC1477;SAL1478;PREF1479",
            "conditional theorems identify exactly how relative weights die",
            "object language, action measure, connected graph, and single line owner remain unsigned",
            "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
        ),
        (
            "MOMS1088_5_variation_order",
            "variation before readout/source projection",
            "CO1078_2;NCO1079_1..4;PVA1008;QTA1008",
            "Hilbert-source uniqueness is exact conditional after common action fixed",
            "parent readout-order axiom and total action owner remain unsigned",
            "CONDITIONAL_SUBTHEOREM_ONLY",
        ),
        (
            "MOMS1088_6_no_shadow_domain",
            "no shadow/domain/readout reentry",
            "CFC943_6;MFS1045_4;PAC1055_3/5;ODR1066;HOM1479",
            "loophole class is sharply identified",
            "operator-domain no-hidden-visible-hom theorem not derived",
            "NO_SHADOW_DOMAIN_UNSIGNED",
        ),
        (
            "MOMS1088_7_verdict",
            "all MOMS clauses parent-derived in one action signature",
            "MOMS1088;SYN1090;AX1090",
            "exact conditional proof stack exists",
            "AX1090_0..4 remain missing axioms not adopted",
            "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": map_id,
            "signature_piece": piece,
            "best_source_anchors": anchors,
            "current_support": support,
            "current_blocker": blocker,
            "source_grade": grade,
            "parent_signed": False,
            "adopt_as_axiom": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for map_id, piece, anchors, support, blocker, grade in mapping
    ]


def clause_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": row["same_parent_branch_id"],
            "gate_id": row["map_id"].replace("MOMS", "GATE1486_MOMS"),
            "signature_piece": row["signature_piece"],
            "gate_status": "BLOCKED",
            "reason": row["current_blocker"],
            "needed_for": "parent-signed neighbourhood quotient descent and C_parent double-zero",
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in moms_source_map_rows()
    ]


def parent_action_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PAO1486_0_parent_object", "one parent action object", "S_parent owns geometry, EM, ordinary matter, boundary, projector, extra/domain sectors before readout", "PAC1055_6;PCS1009_9", "SCHEMA_WRITTEN_NOT_DERIVED", "derive current-chain L_parent and variation for all retained sectors"),
        ("PAO1486_1_current_chain", "parent first variation", "delta L_parent = E_A delta Phi^A + d theta_MTS(delta Phi)", "PVA1008_0", "MISSING_EXPLICIT_CURRENT_CHAIN", "extract theta/Q/stress/boundary contributions"),
        ("PAO1486_2_sector_certificates", "retained sector certificates", "each sector has action source, variation equation, stress, boundary, tau action, and silence/retention rule", "SVR1009_0..6", "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT", "complete or demote each sector explicitly"),
        ("PAO1486_3_matter_subaction", "ordinary matter subaction", "S_matter descends through q and one observed coframe before source projection", "PCS1009_2;PAC1055_2", "CONDITIONAL_SOURCE_INPUT", "parent matter functor and constants"),
        ("PAO1486_4_verdict", "parent action object verdict", "current work has a disciplined action contract but not a signed parent action object", "SYN1090_8", "NOT_PARENT_SIGNED", "neighbourhood descent cannot close yet"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "required_statement": statement,
            "source_anchor": anchor,
            "current_status": status,
            "missing_for_claim": missing,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, statement, anchor, status, missing in rows
    ]


def matter_functor_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("MFA1486_0_bundle", "matter bundle functor", "Psi_A in Gamma(E_A[e_obs,A_obs]) for all ordinary species", "MFS1045_2", "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED"),
        ("MFA1486_1_vertical_lift", "vertical lift", "delta_v Psi_A fixed/gauge/diffeo/local-Lorentz/boundary-only", "MFS1045_3;VLG1045_0..4", "VERTICAL_LIFT_NOT_PARENT_SIGNED"),
        ("MFA1486_2_constants", "fixed constants", "Lie_v theta_A=0 or explicit retained residuals", "MFS1045_5;PAC1055_1..2", "CONSTANT_SUPERSELECTION_UNSIGNED"),
        ("MFA1486_3_action_line", "single action-density line", "one parent matter line with no independent w_A S_A slots", "SAL1478_0..4", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"),
        ("MFA1486_4_connected_category", "connected ordinary-matter category", "parent-owned morphism graph collapses relative weights by naturality", "CON1464;GRC1477", "TEMPLATE_ONLY_NOT_PARENT_OWNED"),
        ("MFA1486_5_verdict", "matter functor verdict", "conditional ordinary-matter descent is clear but not parent-signed", "MFS1045_6;MOMS1088_7", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "required_statement": statement,
            "source_anchor": anchor,
            "current_status": status,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, statement, anchor, status in rows
    ]


def no_shadow_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("NSR1486_0_hidden_coefficients", "hidden-visible coefficient Hom", "Coeff(O_vis) in Alg[q_loc,Theta_rep,Level_EM]", "PAC1055_3;ODR1066_0", "POWERFUL_IF_SIGNED_NOT_DERIVED"),
        ("NSR1486_1_shadow_frame", "shadow conformal/disformal matter frame", "no A_A(X)^2 g_obs, B_A(X), source-only metric, or material marker enters S_A", "CFC943_6;MFS1045_4", "GUARD_WRITTEN_NOT_PARENT_DERIVED"),
        ("NSR1486_2_readout_closure", "radiative/readout closure", "effective/readout maps preserve quotient and constant-sector ownership", "PAC1055_5;NCO1079_3", "READOUT_CLOSURE_UNSIGNED"),
        ("NSR1486_3_source_scalar_target", "source-only scalar target", "Hom(Arg_parent,R_+^species_source_only)=empty", "ODR1066_4;HOM1479", "EXACT_RULE_NOT_DERIVED"),
        ("NSR1486_4_verdict", "no-shadow/readout reentry verdict", "all loopholes are classified but not theorem-forbidden", "HOM1479_5;MOMS1088_6", "OBSTRUCTION_SURVIVES"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "reentry_channel": channel,
            "required_exclusion": exclusion,
            "source_anchor": anchor,
            "current_status": status,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, channel, exclusion, anchor, status in rows
    ]


def axiom_refusal_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(AX_1090):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "axiom_id": row["axiom_id"],
                "axiom_if_adopted": row["axiom_if_adopted"],
                "why_needed": row["why_needed"],
                "current_basis": row["current_basis"],
                "adoption_status": "REFUSED_CLOSURE_ONLY_AXIOM",
                "reason": row["danger_if_adopted"],
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def local_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        ("LRS1486_0_Cparent_zero", "C_parent double-zero", "would follow from parent-signed neighbourhood descent", "NOT_SIGNED", "blocks WEP/local-GR claim"),
        ("LRS1486_1_Newton", "Newtonian source universality", "would follow from source-label forgetting plus derivative-silent common calibration", "CONDITIONAL_ONLY", "relative source weights remain residuals"),
        ("LRS1486_2_GR", "GR equivalence principle", "would follow from one observed coframe and parent matter bundle functor", "CONDITIONAL_ONLY", "shadow/matter-functor gaps remain"),
        ("LRS1486_3_PPN", "PPN readout", "needs no reentry through metric/readout coefficients after variation", "OPEN", "PPN coefficient residuals remain live"),
        ("LRS1486_4_verdict", "local GR/Newton reduction", "1486 improves the source map but does not sign the descent", "NOT_CLOSED", "next target must close one missing parent-signature clause or demote to explicit axiom debt"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "reduction_if_signed": reduction,
            "current_status": status,
            "claim_effect": effect,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for status_id, target, reduction, status, effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1486_0_neighbourhood", "NEIGHBOURHOOD_DESCENT_NOT_PARENT_SIGNED", "open-neighbourhood quotient descent is exact conditional only"),
        ("REJ1486_1_parent_action", "MISSING_TOTAL_PARENT_ACTION_OBJECT", "no full current-chain parent action is promoted"),
        ("REJ1486_2_matter_functor", "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR", "ordinary matter bundle/lift not parent-owned"),
        ("REJ1486_3_constants", "CONSTANT_SUPERSELECTION_UNSIGNED", "mass/charge/clock constants are not parent-signed fixed data"),
        ("REJ1486_4_prefactors", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "w_A/source-only prefactor slots remain countermodel-active"),
        ("REJ1486_5_shadow", "NO_SHADOW_DOMAIN_UNSIGNED", "hidden/readout/domain reentry remains obstruction"),
        ("REJ1486_6_axioms", "AX1090_AXIOMS_NOT_ADOPTED", "missing axioms are refused as closure-only insertions"),
        ("REJ1486_7_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "C_parent theorem-zero/import remains forbidden"),
        ("REJ1486_8_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1486_0_source_map_not_proof", "treat MOMS clauses as a source map, not a proof", "every clause has useful support but no full parent signature", "no C_parent import"),
        ("DEC1486_1_refuse_axioms", "refuse AX1090 closure-only axiom adoption", "adopting them would hide rather than derive the local-GR reduction", "missing axioms become explicit debt"),
        ("DEC1486_2_best_next", "attack the parent action object first", "without one varied action, the matter functor and no-prefactor clauses cannot be signed", "1487 should target S_parent current-chain ownership"),
        ("DEC1486_3_data_secondary", "do not move back to numeric WEP scoring yet", "data cannot sign quotient descent or C_parent zero", "empirical branch waits until coupling/descent is signed or finite residual route is explicit"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "why": why,
            "consequence": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, why, consequence in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1486_0_1487",
            "next_target": "1487-Y5-R10-RAB-parent-action-object-current-chain-ownership-or-explicit-axiom-debt.md",
            "script": "scripts/Y5_R10_RAB_parent_action_object_current_chain_ownership_or_explicit_axiom_debt.py",
            "objective": "try to close the parent action object/current-chain owner needed by neighbourhood quotient descent; if it cannot be derived, write the explicit axiom-debt ledger rather than importing C_parent or claiming local GR",
            "include": "S_parent sector list; delta L_parent; theta_MTS; Q_tau; ordinary matter subaction owner; sector certificate gates; MOMS clause dependency update",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; numeric WEP score; closure-only axiom adoption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def all_claim_flags_false(groups: list[list[dict[str, Any]]]) -> bool:
    for group in groups:
        for row in group:
            if str(row.get("valid_prediction_row", "False")) == "True":
                return False
            if str(row.get("valid_for_claim", "False")) != "False":
                return False
            if str(row.get("claim_allowed", "False")) != "False":
                return False
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    descent: list[dict[str, Any]],
    source_map: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    matter_functor: list[dict[str, Any]],
    no_shadow: list[dict[str, Any]],
    axioms: list[dict[str, Any]],
    local: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        NEIGHBOURHOOD_DESCENT,
        MOMS_SOURCE_MAP,
        CLAUSE_GATES,
        PARENT_ACTION_AUDIT,
        MATTER_FUNCTOR_AUDIT,
        NO_SHADOW_AUDIT,
        AXIOM_REFUSAL,
        LOCAL_REDUCTION,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    sources_exist = all(row["exists_or_resolved"] for row in sources)
    descent_exact = any(row["descent_id"] == "NQD1486_0_target" and row["current_status"] == "TARGET_EXACT" for row in descent)
    descent_not_closed = any(row["descent_id"] == "NQD1486_5_verdict" and row["current_status"] == "NOT_CLOSED_SOURCE_MAP_BUILT" for row in descent)
    source_map_complete = len(source_map) == 8 and all(not row["parent_signed"] for row in source_map)
    gates_blocked = len(gates) == 8 and all(row["gate_status"] == "BLOCKED" for row in gates)
    parent_blocked = any(row["audit_id"] == "PAO1486_4_verdict" and row["current_status"] == "NOT_PARENT_SIGNED" for row in parent_action)
    matter_blocked = any(row["audit_id"] == "MFA1486_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED" for row in matter_functor)
    no_shadow_blocked = any(row["audit_id"] == "NSR1486_4_verdict" and row["current_status"] == "OBSTRUCTION_SURVIVES" for row in no_shadow)
    axioms_refused = len(axioms) >= 5 and all(row["adoption_status"] == "REFUSED_CLOSURE_ONLY_AXIOM" for row in axioms)
    local_not_closed = any(row["status_id"] == "LRS1486_4_verdict" and row["current_status"] == "NOT_CLOSED" for row in local)
    rejections_block = len(rejections) >= 9 and all(not row["claim_allowed"] for row in rejections)
    decisions_nonclaim = all(not row["claim_allowed"] for row in decisions)
    next_ok = len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1486_0_1487"
    no_cparent_import = not C_PARENT_IMPORT.exists()
    csv_parse = all(path.exists() and parse_csv(path) for path in generated)
    copies_exist = all(path.exists() for path in [QUAR_DESCENT, QUAR_MAP, QUAR_AXIOMS, BRANCH_DESCENT, BRANCH_MAP, BRANCH_AXIOMS])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = (
        not any(path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*") if path.is_file())
        if FORMALIZATION.exists()
        else True
    )
    claim_flags_false = all_claim_flags_false([sources, descent, source_map, gates, parent_action, matter_functor, no_shadow, axioms, local, rejections, decisions, next_target])
    checks = [
        ("VAL1486_0_sources", sources_exist, "all cited local source paths exist"),
        ("VAL1486_1_descent_exact", descent_exact, "neighbourhood descent target stated exactly"),
        ("VAL1486_2_descent_not_closed", descent_not_closed, "descent remains not parent-signed"),
        ("VAL1486_3_source_map", source_map_complete, "MOMS source map complete and unsigned"),
        ("VAL1486_4_clause_gates", gates_blocked, "all clause gates blocked"),
        ("VAL1486_5_parent_action", parent_blocked, "parent action object remains unsigned"),
        ("VAL1486_6_matter_functor", matter_blocked, "matter functor remains unsigned"),
        ("VAL1486_7_no_shadow", no_shadow_blocked, "no-shadow/readout reentry remains obstruction"),
        ("VAL1486_8_axioms_refused", axioms_refused, "AX1090 closure axioms refused"),
        ("VAL1486_9_local_reduction", local_not_closed, "local GR/Newton reduction remains not closed"),
        ("VAL1486_10_rejections", rejections_block, "rejection ledger blocks claim"),
        ("VAL1486_11_decisions", decisions_nonclaim, "decision ledger keeps claims false"),
        ("VAL1486_12_next", next_ok, "1487 handoff written"),
        ("VAL1486_13_no_Cparent_import", no_cparent_import, "live C_parent import remains absent"),
        ("VAL1486_14_csv_parse", csv_parse, "all generated 1486 CSVs parse cleanly"),
        ("VAL1486_15_branch_copies", copies_exist, "branch/quarantine copies written"),
        ("VAL1486_16_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1486_17_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
        ("VAL1486_18_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1486_19_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1486 builds the MOMS/neighbourhood-descent source map and refuses closure-only axiom adoption",
            "generated_utc": utc_now(),
        }
    )
    return rows


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_COEFF.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(NEIGHBOURHOOD_DESCENT, QUAR_DESCENT)
    shutil.copyfile(MOMS_SOURCE_MAP, QUAR_MAP)
    shutil.copyfile(AXIOM_REFUSAL, QUAR_AXIOMS)
    shutil.copyfile(NEIGHBOURHOOD_DESCENT, BRANCH_DESCENT)
    shutil.copyfile(MOMS_SOURCE_MAP, BRANCH_MAP)
    shutil.copyfile(AXIOM_REFUSAL, BRANCH_AXIOMS)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


def write_doc(
    descent: list[dict[str, Any]],
    source_map: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    matter_functor: list[dict[str, Any]],
    no_shadow: list[dict[str, Any]],
    axioms: list[dict[str, Any]],
    local: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines = [
        "# 1486 - Neighbourhood Quotient Descent Or MOMS Parent Signature Source Map",
        "",
        "## Verdict",
        "- The exact target is now an open-neighbourhood quotient descent: ordinary matter must factor through `q` on a neighbourhood, not merely at the fixed point.",
        "- Current evidence gives a strong source map of conditional lemmas, but not a parent-signed descent proof.",
        "- AX1090-style closure axioms are explicitly refused; the next route is the parent action object/current-chain owner.",
        "",
        "## Neighbourhood Descent",
    ]
    lines.extend(markdown_table(descent, ["descent_id", "current_status", "missing_for_parent_claim"]))
    lines.extend(["", "## MOMS Source Map"])
    lines.extend(markdown_table(source_map, ["map_id", "source_grade", "current_blocker"]))
    lines.extend(["", "## Clause Gates"])
    lines.extend(markdown_table(gates, ["gate_id", "gate_status", "reason"]))
    lines.extend(["", "## Parent Action Audit"])
    lines.extend(markdown_table(parent_action, ["audit_id", "current_status", "missing_for_claim"]))
    lines.extend(["", "## Matter Functor Audit"])
    lines.extend(markdown_table(matter_functor, ["audit_id", "current_status", "source_anchor"]))
    lines.extend(["", "## No-Shadow/Readout Audit"])
    lines.extend(markdown_table(no_shadow, ["audit_id", "current_status", "source_anchor"]))
    lines.extend(["", "## Axiom Refusal"])
    lines.extend(markdown_table(axioms, ["axiom_id", "adoption_status", "reason"]))
    lines.extend(["", "## Local GR/Newton Status"])
    lines.extend(markdown_table(local, ["status_id", "target", "current_status", "claim_effect"]))
    lines.extend(["", "## Rejection Ledger"])
    lines.extend(markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]))
    lines.extend(["", "## Decision Ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.extend(["", "## Validation"])
    lines.extend(markdown_table(validation, ["check_id", "result", "detail"]))
    lines.extend(["", "## Next Target"])
    lines.extend(markdown_table(next_target, ["next_id", "next_target", "script", "objective"]))
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    descent = neighbourhood_descent_rows()
    source_map = moms_source_map_rows()
    gates = clause_gate_rows()
    parent_action = parent_action_audit_rows()
    matter_functor = matter_functor_audit_rows()
    no_shadow = no_shadow_audit_rows()
    axioms = axiom_refusal_rows()
    local = local_reduction_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NEIGHBOURHOOD_DESCENT, descent)
    write_csv(MOMS_SOURCE_MAP, source_map)
    write_csv(CLAUSE_GATES, gates)
    write_csv(PARENT_ACTION_AUDIT, parent_action)
    write_csv(MATTER_FUNCTOR_AUDIT, matter_functor)
    write_csv(NO_SHADOW_AUDIT, no_shadow)
    write_csv(AXIOM_REFUSAL, axioms)
    write_csv(LOCAL_REDUCTION, local)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)
    copy_outputs()
    validation = validation_rows(sources, descent, source_map, gates, parent_action, matter_functor, no_shadow, axioms, local, rejections, decisions, next_target)
    write_csv(VALIDATION, validation)
    write_doc(descent, source_map, gates, parent_action, matter_functor, no_shadow, axioms, local, rejections, decisions, validation, next_target)
    print("Y5_R10_1486_neighbourhood_descent_source_map_nonclaim")


if __name__ == "__main__":
    main()
