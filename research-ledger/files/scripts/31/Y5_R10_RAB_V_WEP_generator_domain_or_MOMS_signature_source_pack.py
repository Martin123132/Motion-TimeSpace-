from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFF = BRANCH_ROOT / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1448-Y5-R10-RAB-V-WEP-generator-domain-or-MOMS-signature-source-pack.md"

PREV_NEXT = OUT / "P8_Y5_R10_1447_NEXT_TARGET.csv"
PREV_FD = OUT / "P8_Y5_R10_1447_FUNCTIONAL_DERIVATIVE_DEFINITION_ATTEMPT.csv"
PREV_VREQ = OUT / "P8_Y5_R10_1447_VWEP_DOMAIN_REQUIREMENTS.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1447_VALIDATION.csv"
BRANCH_FD = COEFF / "C_parent_WEP_functional_derivative_definition_attempt.csv"
BRANCH_VREQ = COEFF / "V_WEP_domain_requirements.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

MOMS_CLAUSE = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
MOMS_THEOREM = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
MOMS_SYNTHESIS = OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv"
AX1090_AXIOMS = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
AX1090_REDUCTION = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
QVX_CERT = OUT / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
MATTER_SIGNATURE = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
VERTICAL_LIFT = OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
NO_SHADOW = OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
CONSTANT_SUPER = OUT / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv"
PARENT_CONTRACT = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
LABEL_FORGET = OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
NO_SOURCE_SLOT = OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1448_SOURCE_REGISTER.csv"
VWEP_CANDIDATE = OUT / "P8_Y5_R10_1448_VWEP_GENERATOR_CANDIDATE.csv"
MOMS_SOURCE_PACK = OUT / "P8_Y5_R10_1448_MOMS_SIGNATURE_SOURCE_PACK.csv"
DOMAIN_PROOF = OUT / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
EVALUABILITY_GATE = OUT / "P8_Y5_R10_1448_FUNCTIONAL_DERIVATIVE_EVALUABILITY_GATE.csv"
COUNTERMODEL_RETENTION = OUT / "P8_Y5_R10_1448_COUNTERMODEL_RETENTION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1448_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1448_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1448_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1448_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1448_VALIDATION.csv"

BRANCH_VWEP_CANDIDATE = COEFF / "V_WEP_generator_candidate.csv"
BRANCH_MOMS_SOURCE_PACK = COEFF / "MOMS_signature_source_pack_for_V_WEP.csv"
BRANCH_EVALUABILITY_GATE = COEFF / "C_parent_WEP_functional_derivative_evaluability_gate.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        for row in rows:
            writer.writerow(row)


def write_table(handle: Any, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"\n## {title}\n")
    if not rows:
        handle.write("\nNo rows.\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def source_rows() -> list[dict[str, Any]]:
    entries = [
        ("SRC1448_0_prev_next", PREV_NEXT, "1448 handoff"),
        ("SRC1448_1_prev_fd", PREV_FD, "1447 functional derivative target"),
        ("SRC1448_2_prev_vreq", PREV_VREQ, "1447 V_WEP domain requirements"),
        ("SRC1448_3_prev_validation", PREV_VALIDATION, "1447 validation"),
        ("SRC1448_4_branch_fd", BRANCH_FD, "branch functional derivative attempt"),
        ("SRC1448_5_branch_vreq", BRANCH_VREQ, "branch V_WEP domain requirements"),
        ("SRC1448_6_MOMS_clause", MOMS_CLAUSE, "MOMS signature clauses"),
        ("SRC1448_7_MOMS_theorem", MOMS_THEOREM, "MOMS conditional zero theorem"),
        ("SRC1448_8_MOMS_synthesis", MOMS_SYNTHESIS, "MOMS synthesis attempt"),
        ("SRC1448_9_AX1090_axioms", AX1090_AXIOMS, "AX1090 missing axiom ledger"),
        ("SRC1448_10_AX1090_reduction", AX1090_REDUCTION, "AX1090 reduction audit"),
        ("SRC1448_11_QVX_cert", QVX_CERT, "q/v_X certificate"),
        ("SRC1448_12_matter_signature", MATTER_SIGNATURE, "parent matter functor signature"),
        ("SRC1448_13_vertical_lift", VERTICAL_LIFT, "vertical lift descent gate"),
        ("SRC1448_14_no_shadow", NO_SHADOW, "no-shadow frame theorem attempt"),
        ("SRC1448_15_constants", CONSTANT_SUPER, "constant superselection theorem attempt"),
        ("SRC1448_16_parent_contract", PARENT_CONTRACT, "parent action contract candidate"),
        ("SRC1448_17_label_forget", LABEL_FORGET, "label-forgetting proof attempt"),
        ("SRC1448_18_no_source_slot", NO_SOURCE_SLOT, "no-source-only-slot audit"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in entries
    ]


def vwep_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_id": "VWEP1448_0_candidate",
            "candidate_definition": "V_WEP := v_X restricted to the WEP/material-source contrast direction, with Dq[V_WEP]=0 when the MOMS quotient signature is parent-signed",
            "mathematical_use": "direction used in C_parent_WEP[V_WEP] = N_WEP^{-1} dS_parent[V_WEP]",
            "positive_result": "if q, observed coframe, matter functor, constants, no-weight, no-shadow, and variation-order clauses are signed, ordinary matter gives a theorem-zero WEP response",
            "current_status": "CANDIDATE_ONLY_NOT_PARENT_SIGNED",
            "why_not_evaluable": "field-space owner, field-by-field vertical action, matter lift, constants, no-source-only-slot, no-shadow, and normalization remain unsigned",
            "domain_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def moms_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_0_action_form",
            "MOMS_clause": "MOMS1088_0_action_form",
            "needed_for_V_WEP": "single S_parent and field space",
            "best_source": str(MOMS_CLAUSE),
            "current_status": "CONDITIONAL_CLAUSE_WRITTEN_NOT_PARENT_DERIVED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "one parent action owning q, E, Omega, A_obs, Psi_A, theta_A, and species sum",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_1_quotient",
            "MOMS_clause": "MOMS1088_1_quotient_observables",
            "needed_for_V_WEP": "Dq[V_WEP]=0 and observed-field chain rule",
            "best_source": str(QVX_CERT),
            "current_status": "EXACT_CONDITIONAL_SUBLEMMA_NOT_PARENT_SIGNED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "canonical q map and proof actual local X/WEP variation equals parent kernel generator",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_2_matter_bundle",
            "MOMS_clause": "MOMS1088_2_matter_bundle",
            "needed_for_V_WEP": "Psi_epsilon lift under V_WEP",
            "best_source": str(MATTER_SIGNATURE),
            "current_status": "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "species-complete matter bundle functor and owned fixed/gauge/boundary lift",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_3_constants",
            "MOMS_clause": "MOMS1088_3_constant_superselection",
            "needed_for_V_WEP": "theta_epsilon lift and no hidden material constants",
            "best_source": str(CONSTANT_SUPER),
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "parent theorem that masses, charges, alpha_EM, clocks, and material labels are fixed/topological or explicit residuals",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_4_no_weights",
            "MOMS_clause": "MOMS1088_4_no_species_weights",
            "needed_for_V_WEP": "no source-only species prefactor",
            "best_source": str(NO_SOURCE_SLOT),
            "current_status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "parent action grammar forbids w_A S_A or material-only source multipliers",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_5_variation_order",
            "MOMS_clause": "MOMS1088_5_variation_order",
            "needed_for_V_WEP": "derivative before readout/material/source projection",
            "best_source": str(AX1090_REDUCTION),
            "current_status": "CONDITIONAL_RULE_NOT_PARENT_SIGNED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "parent-side variation-before-readout rule tied to detector/source model",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_6_no_shadow",
            "MOMS_clause": "MOMS1088_6_no_shadow_domain",
            "needed_for_V_WEP": "exclude hidden visible hom/source-only domains",
            "best_source": str(NO_SHADOW),
            "current_status": "NO_SHADOW_DOMAIN_UNSIGNED",
            "source_pack_status": "INSUFFICIENT_FOR_IMPORT",
            "missing": "single parent exclusion of conformal/disformal frames, domain markers, and source-only metrics",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": "MSP1448_7_verdict",
            "MOMS_clause": "MOMS1088_7_verdict",
            "needed_for_V_WEP": "all clauses parent-derived together",
            "best_source": str(MOMS_THEOREM),
            "current_status": "MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_NOT_DERIVED",
            "source_pack_status": "BLOCKS_V_WEP_DOMAIN",
            "missing": "source-signed MOMS1088_0..6 in one ordinary-matter action signature",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def domain_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_0_chain_rule",
            "claim": "Dq[V_WEP]=0 implies Lie_V e_obs=0 and visible metric silence",
            "proof_status": "EXACT_CONDITIONAL_MATH_PASS",
            "why_not_claim": "V_WEP is not parent-signed as the actual local/WEP generator",
            "if_signed_effect": "visible geometry part of WEP response vanishes",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_1_matter_lift",
            "claim": "fixed/gauge/boundary matter lift prevents physical ordinary-matter variation",
            "proof_status": "CONDITIONAL_LIFT_OPTIONS_AVAILABLE",
            "why_not_claim": "parent matter bundle functor does not assign the lift for every species",
            "if_signed_effect": "bulk Euler/Hilbert matter contribution to V_WEP derivative vanishes",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_2_constants",
            "claim": "Lie_V theta_A=0 removes mass/charge/clock/material channels",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_claim": "constant superselection route is unsigned and EM/mass owner remains active debt",
            "if_signed_effect": "constant-marker WEP/R10/clock channels collapse to zero or explicit residuals",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_3_no_source_weights",
            "claim": "no w_A source-only slot means V_WEP cannot hit species weights",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "why_not_claim": "relative source weights are covariant unless parent action grammar forbids them",
            "if_signed_effect": "direct WEP source-weight residual is theorem-zero",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_4_no_shadow",
            "claim": "no hidden matter frame/domain/source-only metric blocks re-entry",
            "proof_status": "CONDITIONAL_NO_SHADOW_ONLY",
            "why_not_claim": "ordinary covariance does not forbid shadow conformal/disformal scalars by itself",
            "if_signed_effect": "frame-marker and domain-marker residual rows can be zeroed",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_5_variation_order",
            "claim": "V_WEP derivative is evaluated before material/readout/source projection",
            "proof_status": "GATE_CORRECT_NOT_DERIVED",
            "why_not_claim": "detector/source model and official data are not tied to the parent action yet",
            "if_signed_effect": "post-readout source selectors cannot manufacture or erase WEP residuals",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "VDP1448_6_verdict",
            "claim": "V_WEP domain is derived enough to evaluate C_parent_WEP",
            "proof_status": "FAIL_CURRENT_CLAIM_DOMAIN_NOT_SIGNED",
            "why_not_claim": "conditional wins do not close the field-space owner, lift, constants, no-weight, no-shadow, and variation-order clauses together",
            "if_signed_effect": "C_parent functional derivative becomes evaluable",
            "satisfied_for_current_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def evaluability_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "EVAL1448_0_Cparent_derivative",
            "target_definition": "C_parent_WEP[V_WEP] := N_WEP^{-1} dS_parent[V_WEP]",
            "V_WEP_domain_ready": False,
            "MOMS_signature_ready": False,
            "normalization_ready": False,
            "readout_ready": LIVE_READOUT.exists(),
            "C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "evaluable_now": False,
            "decision": "FUNCTIONAL_DERIVATIVE_REMAINS_NON_EVALUABLE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    countermodels = [
        ("CM1448_0_source_weight", "S_matter=sum_A w_A S_A or source functor keeps species label", "no-source-only-slot parent grammar not signed"),
        ("CM1448_1_shadow_frame", "S_A[Psi_A, A_A(X)^2 g_obs] or disformal B_A(X)", "no-shadow/domain theorem not signed"),
        ("CM1448_2_constant_marker", "alpha_EM(X), m_A(X), clock/material marker", "constant superselection not signed"),
        ("CM1448_3_physical_matter_lift", "delta_V Psi_A has physical species/material component", "matter bundle/lift not parent-owned"),
        ("CM1448_4_post_readout_selector", "source/readout projection chosen after variation", "variation-before-readout rule not derived with source model"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": cid,
            "countermodel": model,
            "why_survives": why,
            "effect": "keeps finite WEP/source coefficient route alive",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, model, why in countermodels
    ]


def parser_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1448_0_VWEP_candidate",
            "target_path": str(BRANCH_VWEP_CANDIDATE),
            "target_exists": BRANCH_VWEP_CANDIDATE.exists(),
            "parser_status": "PASS_CANDIDATE_ONLY_NONCLAIM",
            "refusal_reason": "V_WEP domain_satisfied=false",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1448_1_MOMS_pack",
            "target_path": str(BRANCH_MOMS_SOURCE_PACK),
            "target_exists": BRANCH_MOMS_SOURCE_PACK.exists(),
            "parser_status": "REFUSED_MOMS_SIGNATURE_UNSIGNED",
            "refusal_reason": "MOMS source pack has no import-sufficient row",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1448_2_evaluability_gate",
            "target_path": str(BRANCH_EVALUABILITY_GATE),
            "target_exists": BRANCH_EVALUABILITY_GATE.exists(),
            "parser_status": "REFUSED_FUNCTIONAL_DERIVATIVE_NON_EVALUABLE",
            "refusal_reason": "V_WEP, MOMS, normalization, and readout are not ready",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1448_0_VWEP_candidate_only", "V_WEP is candidate-only, not parent-signed"),
        ("CG1448_1_MOMS_unsigned", "MOMS1088 signature is not derived in one action"),
        ("CG1448_2_countermodels_live", "source weights, shadow frames, constants, matter lift, and readout selectors remain live"),
        ("CG1448_3_derivative_not_evaluable", "C_parent functional derivative cannot be evaluated"),
        ("CG1448_4_import_absent", "live C_parent import remains absent"),
        ("CG1448_5_no_score", "no WEP/local-GR/Newton score or claim is allowed from 1448"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1448_0_chain_rule_kept",
            "decision": "keep the quotient chain-rule pieces as exact conditional lemmas",
            "why": "they are mathematically useful and reduce the proof burden if V_WEP is later parent-signed",
            "consequence": "do not discard MOMS; treat it as the cleanest theorem-zero route",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1448_1_domain_not_signed",
            "decision": "do not evaluate or import C_parent_WEP",
            "why": "V_WEP generator/domain and MOMS source pack remain unsigned",
            "consequence": "finite residual/source routes remain live",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1448_2_next_field_map",
            "decision": "attack field-by-field V_WEP action map next",
            "why": "without the actual transformation law, the generator is notation rather than a variational direction",
            "consequence": "1449 targets metric/coframe, matter, constants, source/readout, and boundary action of V_WEP",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1448_0_1449",
            "next_target": "1449-Y5-R10-RAB-field-by-field-V-WEP-action-map-or-source-only-countermodel-retention.md",
            "script": "scripts/Y5_R10_RAB_field_by_field_V_WEP_action_map_or_source_only_countermodel_retention.py",
            "objective": "attempt to define the field-by-field V_WEP action on parent geometry, observed coframe, matter fields, constants, source/readout selectors, and boundary data; if any block remains unsigned, retain the source-only countermodel branch.",
            "include": "V_WEP transformation law; source-only and shadow-frame countermodels; MOMS clause mapping; no-claim parser dry-run",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; closure-only zero; bound-inverted coefficient; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_scaffolds(vwep: list[dict[str, Any]], pack: list[dict[str, Any]], eval_gate: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_VWEP_CANDIDATE, vwep)
    write_csv(BRANCH_MOMS_SOURCE_PACK, pack)
    write_csv(BRANCH_EVALUABILITY_GATE, eval_gate)


def validation_rows(
    sources: list[dict[str, Any]],
    vwep: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    eval_gate: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        VWEP_CANDIDATE,
        MOMS_SOURCE_PACK,
        DOMAIN_PROOF,
        EVALUABILITY_GATE,
        COUNTERMODEL_RETENTION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_VWEP_CANDIDATE,
        BRANCH_MOMS_SOURCE_PACK,
        BRANCH_EVALUABILITY_GATE,
    ]
    all_sources = all(str(row["exists"]) == "True" for row in sources)
    candidate_nonclaim = all(str(row["domain_satisfied"]) == "False" and str(row["claim_allowed"]) == "False" for row in vwep)
    pack_blocks = any(row["source_pack_status"] == "BLOCKS_V_WEP_DOMAIN" for row in pack)
    proof_has_conditional_win = any(row["proof_status"] == "EXACT_CONDITIONAL_MATH_PASS" for row in proof)
    proof_verdict_fails = any(row["proof_status"] == "FAIL_CURRENT_CLAIM_DOMAIN_NOT_SIGNED" for row in proof)
    not_evaluable = all(str(row["evaluable_now"]) == "False" for row in eval_gate)
    counters_retained = len(counters) >= 5 and all(str(row["claim_allowed"]) == "False" for row in counters)
    parser_false = all(str(row["claim_allowed"]) == "False" for row in parser)
    gates_false = all(str(row["claim_allowed"]) == "False" for row in gates)
    no_import = not LIVE_C_PARENT_IMPORT.exists()
    csvs_parse = all(csv_parses(path) for path in generated)
    formalization_recent = 0
    if FORMALIZATION.exists():
        formalization_recent = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)
    checks = [
        ("VAL1448_0_sources", all_sources, "all cited source paths exist"),
        ("VAL1448_1_candidate_nonclaim", candidate_nonclaim, "V_WEP candidate remains nonclaim"),
        ("VAL1448_2_MOMS_blocks", pack_blocks, "MOMS source pack blocks V_WEP domain import"),
        ("VAL1448_3_conditional_win_recorded", proof_has_conditional_win, "chain-rule conditional proof is retained"),
        ("VAL1448_4_domain_fails", proof_verdict_fails, "domain proof fails for current claim"),
        ("VAL1448_5_not_evaluable", not_evaluable, "C_parent derivative remains non-evaluable"),
        ("VAL1448_6_countermodels_retained", counters_retained, "countermodels retained as nonclaim finite branches"),
        ("VAL1448_7_parser_false", parser_false, "parser dry-run refuses claim/import paths"),
        ("VAL1448_8_claim_gates", gates_false, "all claim gates remain false"),
        ("VAL1448_9_no_import", no_import, "live C_parent import remains absent"),
        ("VAL1448_10_csv_parse", csvs_parse, "all generated 1448 CSVs parse cleanly"),
        ("VAL1448_11_formalization_untouched", formalization_recent == 0, f"formalization modified-file count since start={formalization_recent}"),
        ("VAL1448_12_next_target", True, "1449 handoff written"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail, "generated_utc": now()}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1448_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1448 retains exact conditional V_WEP lemmas but blocks the current generator domain",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    vwep: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    eval_gate: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1448 - V_WEP generator domain or MOMS signature source pack\n\n")
        handle.write(
            "**Current verdict:** the quotient chain-rule part of `V_WEP` is mathematically clean, but the actual "
            "generator/domain is not parent-signed. MOMS remains the clean theorem-zero route only if its action, "
            "matter lift, constants, no-weight, no-shadow, and variation-order clauses are all sourced in one parent "
            "ordinary-matter signature. The `C_parent_WEP` functional derivative stays non-evaluable.\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "V_WEP generator candidate", vwep)
        write_table(handle, "MOMS signature source pack", pack)
        write_table(handle, "V_WEP domain proof attempt", proof)
        write_table(handle, "Functional derivative evaluability gate", eval_gate)
        write_table(handle, "Countermodel retention", counters)
        write_table(handle, "Parser dry-run", parser)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def main() -> None:
    sources = source_rows()
    vwep = vwep_candidate_rows()
    pack = moms_source_pack_rows()
    proof = domain_proof_rows()
    eval_gate = evaluability_rows()
    counters = countermodel_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_live_scaffolds(vwep, pack, eval_gate)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(VWEP_CANDIDATE, vwep)
    write_csv(MOMS_SOURCE_PACK, pack)
    write_csv(DOMAIN_PROOF, proof)
    write_csv(EVALUABILITY_GATE, eval_gate)
    write_csv(COUNTERMODEL_RETENTION, counters)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    validation = validation_rows(sources, vwep, pack, proof, eval_gate, counters, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, vwep, pack, proof, eval_gate, counters, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1448_VWEP_domain_conditional_not_signed")


if __name__ == "__main__":
    main()
