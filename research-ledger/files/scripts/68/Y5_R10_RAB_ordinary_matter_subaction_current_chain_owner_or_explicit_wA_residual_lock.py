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
DOC = ROOT / "1488-Y5-R10-RAB-ordinary-matter-subaction-current-chain-owner-or-explicit-wA-residual-lock.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1487_next": OUT / "P8_Y5_R10_1487_NEXT_TARGET.csv",
    "1487_validation": OUT / "P8_Y5_BRR545_1487_VALIDATION.csv",
    "1487_matter_owner": OUT / "P8_Y5_R10_1487_ORDINARY_MATTER_SUBACTION_OWNER.csv",
    "1487_axiom_debt": OUT / "P8_Y5_R10_1487_EXPLICIT_AXIOM_DEBT_LEDGER.csv",
    "1487_moms_update": OUT / "P8_Y5_R10_1487_MOMS_DEPENDENCY_UPDATE.csv",
    "1487_local_status": OUT / "P8_Y5_R10_1487_LOCAL_GR_NEWTON_STATUS.csv",
    "1486_neighbourhood": OUT / "P8_Y5_R10_1486_NEIGHBOURHOOD_QUOTIENT_DESCENT_ATTEMPT.csv",
    "1045_matter_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1088_zero_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1450_hilbert_label_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1464_connected_category": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1478_single_action_line": OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv",
    "1479_prefactor_typing": OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv",
    "1479_hom_audit": OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv",
    "1055_parent_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1055_adoption_gates": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1488_SOURCE_REGISTER.csv"
CURRENT_CHAIN_ATTEMPT = OUT / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv"
HILBERT_SOURCE_AUDIT = OUT / "P8_Y5_R10_1488_HILBERT_SOURCE_OWNER_AUDIT.csv"
SINGLE_ACTION_GATE = OUT / "P8_Y5_R10_1488_SINGLE_ACTION_DENSITY_LINE_GATE.csv"
NO_SOURCE_HOM_GATE = OUT / "P8_Y5_R10_1488_NO_SOURCE_ONLY_HOM_GATE.csv"
FIXED_CONSTANTS_GATE = OUT / "P8_Y5_R10_1488_FIXED_CONSTANTS_REPRESENTATION_GATE.csv"
NEIGHBOURHOOD_LINK = OUT / "P8_Y5_R10_1488_OPEN_NEIGHBOURHOOD_DESCENT_LINK.csv"
WA_RESIDUAL_LOCK = OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1488_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1488_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1488_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1488_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1488_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1488_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1488"
QUAR_CHAIN = QUARANTINE / "ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT_NONCLAIM.csv"
QUAR_WA = QUARANTINE / "WA_DELTAW_RESIDUAL_LOCK_NONCLAIM.csv"
QUAR_HOM = QUARANTINE / "NO_SOURCE_ONLY_HOM_GATE_NONCLAIM.csv"
BRANCH_WA = BRANCH_RESIDUALS / "wA_deltaW_residual_lock_nonclaim_1488.csv"
BRANCH_HOM = BRANCH_RESIDUALS / "no_source_only_Hom_gate_nonclaim_1488.csv"
BRANCH_CHAIN = BRANCH_COEFF / "ordinary_matter_subaction_current_chain_attempt_nonclaim_1488.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative_path(path: Path) -> str:
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


def false_flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1487_next": "authoritative 1488 handoff",
        "1487_validation": "previous validation state",
        "1487_matter_owner": "ordinary matter owner source rows",
        "1487_axiom_debt": "explicit axiom debt inherited into 1488",
        "1487_moms_update": "MOMS dependency status",
        "1487_local_status": "local GR/Newton status before 1488",
        "1486_neighbourhood": "open-neighbourhood descent target",
        "1045_matter_functor": "matter bundle/coframe/fixed-constant signature audit",
        "1088_zero_theorem": "conditional zero theorem under MOMS signature",
        "1450_hilbert_label_forgetting": "Hilbert source label-forgetting attempt",
        "1464_connected_category": "connected matter category attempt",
        "1478_single_action_line": "single action-density line proof attempt",
        "1479_prefactor_typing": "no source-only prefactor typing theorem attempt",
        "1479_hom_audit": "Hom species/hidden/readout to source-prefactor audit",
        "1055_parent_contract": "parent action contract candidate",
        "1055_adoption_gates": "contract-adoption gates",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1488_{idx}_{key}",
            "path_or_url": relative_path(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage[key],
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for idx, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def current_chain_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OMSCC1488_0_target",
            "ordinary matter current-chain target",
            "S_ord[Psi_A,e_obs(q(Phi)),theta_A] is defined before source/readout; delta L_ord = E_Psi delta Psi + 1/2 T_H^{ab} delta g_obs_ab + d theta_ord",
            "OMSO1487_0;OMSO1487_1;MFS1045_2",
            "TARGET_EXACT",
            "parent-construct matter bundle, vertical lift, and single density line",
            "This is the smallest non-circular local-GR coupling target.",
        ),
        (
            "OMSCC1488_1_variation_owner",
            "ordinary first variation owner",
            "all ordinary bulk source terms are Hilbert/coframe variations of the same S_ord",
            "HT1450_1;HT1450_4",
            "EXACT_CONDITIONAL_GUARD",
            "same-action source owner still allows pre-action relative w_A unless grammar forbids it",
            "Useful but not enough; covariance alone does not kill the coupling slot.",
        ),
        (
            "OMSCC1488_2_vertical_blindness",
            "vertical local flow blindness",
            "Dq[v_X]=0 implies Lie_v e_obs=Lie_v g_obs=0, and an owned matter lift gives delta_v S_ord=0 up to gauge/boundary terms",
            "MFS1045_0..3;THM1088_1..2",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "parent signature must own q, observed coframe, matter lift, and boundary class on an open neighbourhood",
            "This would buy the C_parent double-zero, but the parent signature is still unsigned.",
        ),
        (
            "OMSCC1488_3_prefactor_countermodel",
            "source/action prefactor countermodel",
            "S_ord = sum_A w_A S_A gives correct matter EOM scaling but active source T_source = sum_A w_A T_A",
            "HT1450_3;SAL1478_2;NST1479_3",
            "COUNTERMODEL_SURVIVES",
            "derive no-source-only Hom/grammar exclusion or retain finite delta_w_A residuals",
            "This is the coupling problem in sharp form.",
        ),
        (
            "OMSCC1488_4_current_chain_verdict",
            "ordinary current-chain verdict",
            "ordinary matter has exact conditional theorem pieces but no parent-signed source-weight exclusion",
            "1488 synthesis",
            "NOT_CLOSED_WA_RESIDUAL_LOCKED",
            "lock w_A/delta_w_A as explicit nonclaim residuals and attack Hom exclusion next",
            "We fail honestly here, which is exactly the right kind of useful failure.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim_piece": claim_piece,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "route_note": route_note,
            **false_flags(),
        }
        for attempt_id, claim_piece, formal_statement, source_anchor, current_status, missing_for_claim, route_note in rows
    ]


def hilbert_source_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HSO1488_0_total_source",
            "total Hilbert source",
            "T_total^{mu nu} = 2/sqrt(-g) delta S_ord/delta g_obs_munu",
            "HT1450_1",
            "EXACT_CONDITIONAL_MATH_PASS",
            "needs single S_ord before variation and no pre-action w_A",
        ),
        (
            "HSO1488_1_additive_uniqueness",
            "label-forgotten additive map",
            "F_src(T+U)=F_src(T)+F_src(U) and covariance give F_src(T)=kappa_univ T after labels are forgotten",
            "HT1450_2",
            "CONDITIONAL_UNIQUENESS_PASS",
            "labels must actually be absent before coupling",
        ),
        (
            "HSO1488_2_same_action_guard",
            "same-action dynamics/source guard",
            "matter EOM and active source come from the same matter action",
            "HT1450_4",
            "STRONG_CONDITIONAL_GUARD",
            "constant w_A inside the same action still survives",
        ),
        (
            "HSO1488_3_nonHilbert_bypass",
            "non-Hilbert source bypass",
            "J_src = kappa_univ T_Hilbert + J_NH_retained",
            "HT1450_5",
            "PARALLEL_GATE_OPEN",
            "non-Hilbert currents must be zero/exact/projected-silent or retained",
        ),
        (
            "HSO1488_4_verdict",
            "Hilbert source owner verdict",
            "Hilbert source label-forgetting is exact conditional but not parent-derived",
            "HT1450_6",
            "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
            "no-source-only-slot and common measure/current owner remain unsigned",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "subtarget": subtarget,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **false_flags(),
        }
        for audit_id, subtarget, formal_statement, source_anchor, current_status, missing_for_claim in rows
    ]


def single_action_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SADL1488_0_target",
            "single parent ordinary-matter action-density line",
            "S_ord = integral dmu_parent L_ord(Psi_A,gauge,theta_A,e_obs)/hbar_parent with no independent w_A S_A slots",
            "SAL1478_0",
            "TARGET_EXACT",
            "construct L_action, hbar_parent, measure owner, and ordinary matter syntax",
        ),
        (
            "SADL1488_1_conditional",
            "one-line action theorem",
            "single line + common measure/current + connected source-normalization + no readout reentry gives delta_w_A=0 modulo common w_*",
            "SAL1478_1",
            "EXACT_CONDITIONAL_THEOREM",
            "premises remain closure clauses, not derivations from MTS primitives",
        ),
        (
            "SADL1488_2_countermodel",
            "direct-sum component weights",
            "if ordinary matter decomposes into disconnected source-normalization components, w_i can be independent",
            "SAL1478_3;CON1464_3",
            "COUNTERMODEL_SURVIVES",
            "parent-owned connected graph plus single line owner",
        ),
        (
            "SADL1488_3_verdict",
            "single action-density line verdict",
            "single-line proof is not closed; finite component delta_w vector must stay live",
            "SAL1478_4",
            "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED",
            "derive parent action syntax or retain explicit delta_w_A residuals",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **false_flags(),
        }
        for gate_id, gate, formal_statement, source_anchor, current_status, missing_for_claim in rows
    ]


def hom_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HOMG1488_0_target",
            "no source-only prefactor target",
            "Hom_parent(species_label or hidden_marker, R_+ active-source-prefactor) is empty or common-constant only",
            "NST1479_0",
            "TARGET_EXACT",
            "derive object-language/admissibility principle from parent MTS primitives",
        ),
        (
            "HOMG1488_1_typed_theorem",
            "typed object-language theorem",
            "allowed arguments are observable geometry, matter fields, gauge/current data, fixed representation data, and universal constants",
            "NST1479_1",
            "EXACT_CONDITIONAL_META_THEOREM",
            "hidden invariant and source-label countermodels remain live",
        ),
        (
            "HOMG1488_2_species_prefactor",
            "species label to source prefactor",
            "Hom(species label, R_+ active source/action prefactor)",
            "HOM1479_1",
            "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED",
            "typed object-language theorem or common action-measure owner",
        ),
        (
            "HOMG1488_3_hidden_prefactor",
            "hidden invariant to source coefficient",
            "Hom(hidden invariant I_hid, R_+ source coefficient)",
            "HOM1479_2",
            "OBSTRUCTION_SURVIVES",
            "hidden invariant algebra triviality or coefficient target exclusion",
        ),
        (
            "HOMG1488_4_readout_prefactor",
            "readout/source-worldtube to source weight",
            "post-variation source/readout selector feeding active source weight",
            "HOM1479_5",
            "READOUT_TRANSFER_UNSIGNED",
            "variation-before-readout plus official/source-worldtube transfer",
        ),
        (
            "HOMG1488_5_verdict",
            "Hom exclusion verdict",
            "the no-source-only prefactor theorem is exact as a grammar condition but not parent-derived",
            "NST1479_4;HOM1479_5",
            "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED",
            "next target should derive Hom exclusion or build delta_w bound interface",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **false_flags(),
        }
        for gate_id, gate, formal_statement, source_anchor, current_status, missing_for_claim in rows
    ]


def fixed_constants_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FCR1488_0_alpha_owner",
            "alpha_EM and Maxwell normalization",
            "alpha/Maxwell kinetic normalization is fixed representation data or separately derived",
            "ADG1055_1;MFS1045_5",
            "BEST_ROUTE_NOT_PROVED",
            "derive gauge-fibre normalization/topological level or keep alpha residual rows nonclaim",
        ),
        (
            "FCR1488_1_mass_clock_owner",
            "mass ratios and clock constants",
            "ordinary masses/clock constants are fixed theta_A or retained residual fields with Lie_v theta_A=0 only if parent-signed",
            "MFS1045_5;THM1088_3",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "derive fixed constant sector or retain clock/WEP/fine-structure residuals",
        ),
        (
            "FCR1488_2_common_calibration",
            "common calibration mode",
            "a universal w_* can be absorbed into measured G_N/GM only after no species/time/range/frame dependence",
            "HOM1479_0",
            "CALIBRATION_ONLY_IF_UNIVERSAL_SILENT",
            "prove universality/silence or keep calibration as nonclaim nuisance",
        ),
        (
            "FCR1488_3_verdict",
            "fixed constants verdict",
            "constant sector does not close the matter owner in 1488",
            "PAC1055_1..2;ADG1055_1..2",
            "CONSTANT_DEBT_RETAINED",
            "do not hide charge/mass/clock debt inside universal coupling",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "constant_channel": channel,
            "required_statement": required_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **false_flags(),
        }
        for gate_id, channel, required_statement, source_anchor, current_status, missing_for_claim in rows
    ]


def neighbourhood_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OND1488_0_link",
            "ordinary matter descent link",
            "if S_ord factors through q on an open neighbourhood U and v_X in ker(Dq), then delta_v S_ord=0 up to gauge/boundary",
            "NQD1486_0;THM1088_5",
            "EXACT_CONDITIONAL_LINK",
            "parent signature of q, e_obs, matter lift, fixed constants, and no weight leak",
        ),
        (
            "OND1488_1_Cparent_corollary",
            "C_parent double-zero corollary",
            "open-neighbourhood blindness implies C_parent_X(Phi0)=0 and partial_A C_parent_X(Phi0)=0",
            "OMSO1487_5;THM1088_5",
            "COROLLARY_CONDITIONAL_ONLY",
            "ordinary matter owner is unsigned and w_A residuals survive",
        ),
        (
            "OND1488_2_verdict",
            "neighbourhood descent status after 1488",
            "the descent theorem route remains exact but cannot be promoted while source-weight Hom is unsigned",
            "1488 synthesis",
            "NOT_PROMOTED_WA_OBSTRUCTION",
            "attack Hom exclusion or use residual-bound branch",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "link_id": link_id,
            "claim_piece": claim_piece,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **false_flags(),
        }
        for link_id, claim_piece, formal_statement, source_anchor, current_status, missing_for_claim in rows
    ]


def wa_residual_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WA1488_0_common_mode",
            "w_star",
            "common universal calibration multiplying all ordinary Hilbert sources",
            "calibration nuisance",
            "HOM1479_0",
            "COMMON_MODE_ONLY_NOT_WEP_SIGNAL",
            "absorbed into measured G_N/GM only if time/range/frame/species silence is proved",
        ),
        (
            "WA1488_1_component_vector",
            "delta_w_A",
            "finite ordinary source/action weight residual vector over source-relevant components",
            "symbolic residual vector",
            "SAL1478_4;NST1479_4",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "requires parent component basis or empirical bound interface before scoring",
        ),
        (
            "WA1488_2_species_label_slot",
            "delta_w_species",
            "species-label to active-source prefactor leakage",
            "countermodel slot",
            "HOM1479_1",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "killed only by typed object-language theorem/common action-measure owner",
        ),
        (
            "WA1488_3_hidden_invariant_slot",
            "delta_w_hidden",
            "hidden invariant to source coefficient leakage",
            "countermodel slot",
            "HOM1479_2",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "killed only by hidden invariant algebra triviality or coefficient target exclusion",
        ),
        (
            "WA1488_4_marker_domain_slot",
            "delta_w_marker",
            "material/domain/boundary marker to source coefficient leakage",
            "countermodel slot",
            "HOM1479_3",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "killed only by no-marker/no-spurion closure and readout no-reentry",
        ),
        (
            "WA1488_5_current_norm_slot",
            "delta_w_current",
            "current-label or non-Hilbert current normalization leakage",
            "countermodel slot",
            "HOM1479_4;HT1450_5",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "requires current owner and Hilbert/non-Hilbert source split",
        ),
        (
            "WA1488_6_readout_slot",
            "delta_w_readout",
            "post-variation source/readout transfer leakage",
            "countermodel slot",
            "HOM1479_5",
            "RETAINED_RESIDUAL_SYMBOLIC",
            "requires variation-before-readout plus official/source-worldtube transfer",
        ),
        (
            "WA1488_7_lock_verdict",
            "delta_w_lock",
            "no source-weight row is claimable until Hom exclusion is derived or real bound interface is sourced",
            "branch lock",
            "1488 synthesis",
            "NONCLAIM_LOCK",
            "1489 should target Hom exclusion first, bound interface second",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "residual_kind": residual_kind,
            "source_anchor": source_anchor,
            "status": status,
            "numeric_value": "MISSING_PARENT_INPUT",
            "units": "dimensionless_relative_source_weight",
            "missing_for_claim": missing_for_claim,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, definition, residual_kind, source_anchor, status, missing_for_claim in rows
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1488_0_live_import",
            "forbidden_object": relative_path(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "ordinary matter current-chain did not close; w_A residuals remain live",
            "action_taken": "no C_parent import written",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LRS1488_0_WEP",
            "WEP/local source universality",
            "delta_w_A=0 modulo common calibration",
            "NOT_CLOSED_RESIDUAL_LOCKED",
            "no-source-only Hom exclusion and single action-density owner remain unsigned",
            "WEP claim blocked",
        ),
        (
            "LRS1488_1_Newton",
            "Newtonian active source",
            "one Hilbert source with no relative active-source weights",
            "CONDITIONAL_ONLY",
            "Hilbert label forgetting is exact but source labels/prefactors can survive",
            "Newton reduction not yet derivable",
        ),
        (
            "LRS1488_2_GR",
            "local GR matter coupling",
            "same observed metric/coframe and universal matter coupling",
            "CONDITIONAL_ONLY",
            "matter functor, fixed constants, and no-shadow Hom remain unsigned",
            "GR reduction not yet claimable",
        ),
        (
            "LRS1488_3_Cparent",
            "C_parent double-zero",
            "ordinary matter local vertical variation vanishes on open neighbourhood",
            "COROLLARY_BLOCKED_BY_WA",
            "w_A residual lock prevents theorem-zero promotion",
            "C_parent import forbidden",
        ),
        (
            "LRS1488_4_verdict",
            "local GR/Newton/WEP status",
            "ordinary matter route sharpened but not proved",
            "NOT_CLOSED_NEXT_HOM_OR_BOUND_INTERFACE",
            "derive Hom exclusion or build source-ready delta_w bound interface",
            "no local-GR/Newton/WEP/R10 claim from 1488",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "required_statement": required_statement,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "claim_effect": claim_effect,
            **false_flags(),
        }
        for status_id, target, required_statement, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1488_0_current_chain", "ORDINARY_CURRENT_CHAIN_NOT_PARENT_SIGNED", "ordinary matter current chain remains exact conditional only"),
        ("REJ1488_1_wA", "SOURCE_WEIGHT_RESIDUALS_RETAINED", "relative source/action weights survive as finite nonclaim residuals"),
        ("REJ1488_2_hom", "NO_SOURCE_ONLY_HOM_NOT_DERIVED", "source-only prefactor target is a grammar condition, not parent-derived"),
        ("REJ1488_3_single_line", "SINGLE_ACTION_DENSITY_LINE_NOT_DERIVED", "common measure/current/action line remains unsigned"),
        ("REJ1488_4_constants", "FIXED_CONSTANTS_UNSIGNED", "alpha/mass/clock constant sector remains explicit debt"),
        ("REJ1488_5_neighbourhood", "OPEN_NEIGHBOURHOOD_DESCENT_NOT_PROMOTED", "conditional descent is blocked by w_A/Hom channels"),
        ("REJ1488_6_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "no theorem-zero C_parent row can be imported"),
        ("REJ1488_7_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1488_0_fail_honestly",
            "do not promote ordinary matter owner",
            "same-action/Hilbert arguments do not ban pre-action source weights",
            "keep w_A/delta_w_A residuals explicit",
        ),
        (
            "DEC1488_1_no_Cparent",
            "do not import C_parent double-zero",
            "open-neighbourhood descent remains conditional and w_A survives",
            "keep local-GR/WEP branch blocked",
        ),
        (
            "DEC1488_2_next_derivation",
            "target no-source-only Hom exclusion",
            "this is the smallest remaining coupling theorem",
            "derive parent object-language exclusion or build delta_w bound interface",
        ),
        (
            "DEC1488_3_data_wait",
            "do not numeric-score WEP yet",
            "without Hom exclusion, any score would be a residual-bound problem not a theorem-zero test",
            "build source-ready bound interface only if derivation fails again",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1488_0_1489",
            "next_target": "1489-Y5-R10-RAB-no-source-only-Hom-exclusion-or-delta-w-bound-interface.md",
            "script": "scripts/Y5_R10_RAB_no_source_only_Hom_exclusion_or_delta_w_bound_interface.py",
            "objective": "try to derive the parent object-language exclusion Hom(species/hidden/readout -> active source prefactor)=empty/common-only; if it fails, build source-ready nonclaim delta_w bound-interface rows",
            "include": "typed coefficient targets; species-label Hom; hidden-invariant Hom; marker/readout Hom; common calibration mode; delta_w bound interface",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; numeric WEP claim; closure-only axiom adoption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        CURRENT_CHAIN_ATTEMPT,
        HILBERT_SOURCE_AUDIT,
        SINGLE_ACTION_GATE,
        NO_SOURCE_HOM_GATE,
        FIXED_CONSTANTS_GATE,
        NEIGHBOURHOOD_LINK,
        WA_RESIDUAL_LOCK,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    BRANCH_COEFF.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CURRENT_CHAIN_ATTEMPT, QUAR_CHAIN)
    shutil.copyfile(WA_RESIDUAL_LOCK, QUAR_WA)
    shutil.copyfile(NO_SOURCE_HOM_GATE, QUAR_HOM)
    shutil.copyfile(WA_RESIDUAL_LOCK, BRANCH_WA)
    shutil.copyfile(NO_SOURCE_HOM_GATE, BRANCH_HOM)
    shutil.copyfile(CURRENT_CHAIN_ATTEMPT, BRANCH_CHAIN)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows() -> list[dict[str, Any]]:
    source_register = read_csv(SOURCE_REGISTER)
    current_chain = read_csv(CURRENT_CHAIN_ATTEMPT)
    hilbert = read_csv(HILBERT_SOURCE_AUDIT)
    single_action = read_csv(SINGLE_ACTION_GATE)
    hom_gate = read_csv(NO_SOURCE_HOM_GATE)
    constants = read_csv(FIXED_CONSTANTS_GATE)
    descent = read_csv(NEIGHBOURHOOD_LINK)
    wa_rows = read_csv(WA_RESIDUAL_LOCK)
    c_parent = read_csv(C_PARENT_REFUSAL)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_target = read_csv(NEXT_TARGET)

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1488_0_sources",
            all(row["exists_or_resolved"].lower() == "true" for row in source_register),
            "all cited local source paths exist",
        ),
        (
            "VAL1488_1_current_chain_not_closed",
            any(row["current_status"] == "NOT_CLOSED_WA_RESIDUAL_LOCKED" for row in current_chain),
            "ordinary matter current-chain remains not closed and w_A residuals are locked",
        ),
        (
            "VAL1488_2_hilbert_conditional",
            any(row["current_status"] == "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED" for row in hilbert),
            "Hilbert source theorem remains conditional",
        ),
        (
            "VAL1488_3_single_action_blocked",
            any(row["current_status"] == "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED" for row in single_action),
            "single action-density line remains blocked",
        ),
        (
            "VAL1488_4_hom_blocked",
            any(row["current_status"] == "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED" for row in hom_gate),
            "no-source-only Hom exclusion remains blocked",
        ),
        (
            "VAL1488_5_constants_blocked",
            any(row["current_status"] == "CONSTANT_DEBT_RETAINED" for row in constants),
            "fixed constant/representation debt retained",
        ),
        (
            "VAL1488_6_descent_not_promoted",
            any(row["current_status"] == "NOT_PROMOTED_WA_OBSTRUCTION" for row in descent),
            "open-neighbourhood descent not promoted because w_A obstruction survives",
        ),
        (
            "VAL1488_7_wa_nonclaim",
            all(row["numeric_value"] == "MISSING_PARENT_INPUT" and row["claim_allowed"].lower() == "false" for row in wa_rows),
            "all w_A/delta_w_A rows are symbolic nonclaim residuals",
        ),
        (
            "VAL1488_8_no_Cparent_import",
            (not C_PARENT_IMPORT.exists()) and all(row["claim_allowed"].lower() == "false" for row in c_parent),
            "live C_parent import remains absent and refused",
        ),
        (
            "VAL1488_9_local_blocked",
            any(row["current_status"] == "NOT_CLOSED_NEXT_HOM_OR_BOUND_INTERFACE" for row in local),
            "local GR/Newton/WEP remains blocked",
        ),
        (
            "VAL1488_10_rejections",
            len(rejections) >= 8 and all(row["claim_allowed"].lower() == "false" for row in rejections),
            "rejection ledger blocks all claim promotion",
        ),
        (
            "VAL1488_11_decisions",
            any(row["decision_id"] == "DEC1488_2_next_derivation" for row in decisions),
            "decision ledger selects Hom exclusion as next derivation target",
        ),
        (
            "VAL1488_12_next",
            len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1488_0_1489",
            "1489 handoff written",
        ),
        (
            "VAL1488_13_csv_parse",
            all(parse_csv(path) for path in generated_csvs()),
            "all generated 1488 CSVs parse cleanly",
        ),
        (
            "VAL1488_14_branch_copies",
            all(path.exists() for path in [QUAR_CHAIN, QUAR_WA, QUAR_HOM, BRANCH_WA, BRANCH_HOM, BRANCH_CHAIN]),
            "branch/quarantine nonclaim copies written",
        ),
    ]

    remove_pycache()
    checks.append(
        (
            "VAL1488_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        )
    )
    modified_count = formalization_modified_count()
    checks.append(
        (
            "VAL1488_16_formalization_untouched",
            modified_count == 0,
            f"formalization modified-file count since start={modified_count}",
        )
    )
    claim_paths = generated_csvs() + [QUAR_CHAIN, QUAR_WA, QUAR_HOM, BRANCH_WA, BRANCH_HOM, BRANCH_CHAIN]
    claim_flags_false = True
    for path in claim_paths:
        for row in read_csv(path):
            for flag in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag in row and row[flag].lower() != "false":
                    claim_flags_false = False
    checks.append(("VAL1488_17_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"))
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1488_18_overall",
            overall,
            "1488 fails the ordinary-matter owner honestly, locks w_A residuals, and selects Hom exclusion as the next target",
        )
    )
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    current_chain = read_csv(CURRENT_CHAIN_ATTEMPT)
    hilbert = read_csv(HILBERT_SOURCE_AUDIT)
    single_action = read_csv(SINGLE_ACTION_GATE)
    hom_gate = read_csv(NO_SOURCE_HOM_GATE)
    constants = read_csv(FIXED_CONSTANTS_GATE)
    descent = read_csv(NEIGHBOURHOOD_LINK)
    wa_rows = read_csv(WA_RESIDUAL_LOCK)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    validation = read_csv(VALIDATION)
    next_target = read_csv(NEXT_TARGET)

    lines = [
        "# 1488 - Ordinary Matter Subaction Current Chain Owner Or Explicit w_A Residual Lock",
        "",
        "## Verdict",
        "- The ordinary-matter current-chain route gives exact conditional pieces, but it does not yet prove universal coupling.",
        "- The surviving obstruction is precise: pre-action/source-only weights `w_A` remain legal unless the parent object language forbids `Hom(species/hidden/readout -> active source prefactor)`.",
        "- 1488 therefore locks `w_A/delta_w_A` as explicit nonclaim residuals and hands off to a no-source-only Hom derivation attempt.",
        "",
        "## Ordinary Matter Current Chain Attempt",
        markdown_table(current_chain, ["attempt_id", "current_status", "missing_for_claim"]),
        "",
        "## Hilbert Source Owner",
        markdown_table(hilbert, ["audit_id", "current_status", "missing_for_claim"]),
        "",
        "## Single Action Density Line Gate",
        markdown_table(single_action, ["gate_id", "current_status", "missing_for_claim"]),
        "",
        "## No Source Only Hom Gate",
        markdown_table(hom_gate, ["gate_id", "current_status", "missing_for_claim"]),
        "",
        "## Fixed Constants Gate",
        markdown_table(constants, ["gate_id", "constant_channel", "current_status", "missing_for_claim"]),
        "",
        "## Open Neighbourhood Descent Link",
        markdown_table(descent, ["link_id", "current_status", "missing_for_claim"]),
        "",
        "## w_A / delta_w_A Residual Lock",
        markdown_table(wa_rows, ["residual_id", "symbol", "status", "numeric_value", "missing_for_claim"]),
        "",
        "## Local GR/Newton Status",
        markdown_table(local, ["status_id", "target", "current_status", "claim_effect"]),
        "",
        "## Rejection Ledger",
        markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]),
        "",
        "## Decision Ledger",
    ]
    for decision in decisions:
        lines.append(f"- `{decision['decision_id']}`: {decision['decision']} - {decision['next_action']}.")
    lines.extend(
        [
            "",
            "## Validation",
            markdown_table(validation, ["check_id", "result", "detail"]),
            "",
            "## Next Target",
            markdown_table(next_target, ["next_id", "next_target", "script", "objective"]),
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(CURRENT_CHAIN_ATTEMPT, current_chain_rows())
    write_csv(HILBERT_SOURCE_AUDIT, hilbert_source_rows())
    write_csv(SINGLE_ACTION_GATE, single_action_rows())
    write_csv(NO_SOURCE_HOM_GATE, hom_gate_rows())
    write_csv(FIXED_CONSTANTS_GATE, fixed_constants_rows())
    write_csv(NEIGHBOURHOOD_LINK, neighbourhood_rows())
    write_csv(WA_RESIDUAL_LOCK, wa_residual_rows())
    write_csv(C_PARENT_REFUSAL, c_parent_refusal_rows())
    write_csv(LOCAL_STATUS, local_status_rows())
    write_csv(REJECTION_LEDGER, rejection_rows())
    write_csv(DECISION_LEDGER, decision_rows())
    write_csv(NEXT_TARGET, next_target_rows())
    copy_outputs()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {VALIDATION}")


if __name__ == "__main__":
    main()
