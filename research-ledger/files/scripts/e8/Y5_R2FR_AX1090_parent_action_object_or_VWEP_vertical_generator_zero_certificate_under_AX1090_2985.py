from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICRO = ROOT / "source-intake" / "microscope"
MICRO_COEFF = MICRO / "branch_locked_wep" / "coefficients"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2985"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2985-Y5-R2FR-AX1090-parent-action-object-or-VWEP-vertical-generator-zero-certificate-under-AX1090.md"

SRC_2984_DOC = ROOT / "2984-Y5-R2FR-CMSM-inventory-extractor-or-Cparent-theorem-zero-source-under-AX1090.md"
SRC_2984_NEXT = RESIDUALS / "P8_Y5_R2FR_2984_NEXT_TARGET.csv"
SRC_2984_ZERO = RESIDUALS / "P8_Y5_R2FR_2984_CPARENT_THEOREM_ZERO_SOURCE_AUDIT.csv"
SRC_2984_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2984_PROMOTION_REFUSAL_GATES.csv"
SRC_2984_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2984_VALIDATION.csv"

SRC_AX1090 = MICRO_COEFF / "AX1090_parent_object_proof_attempt.csv"
SRC_AXRED1441 = RESIDUALS / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
SRC_VWEP_MAP = MICRO_COEFF / "V_WEP_field_by_field_action_map.csv"
SRC_VWEP_CANDIDATE = MICRO_COEFF / "V_WEP_generator_candidate.csv"
SRC_VWEP_DOMAIN = RESIDUALS / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
SRC_QVX = RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
SRC_LIFT = RESIDUALS / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
SRC_NO_SHADOW = RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
SRC_CONSTANTS = RESIDUALS / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv"
SRC_NO_SOURCE = RESIDUALS / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv"
SRC_MIN_CLAUSE = MICRO_COEFF / "C_parent_WEP_minimal_parent_clause.csv"
SRC_CLOSURE = MICRO_COEFF / "C_parent_WEP_clause_closure_demotion.csv"
SRC_SOURCE_FACTOR = MICRO_COEFF / "C_parent_WEP_source_factorization_signing_decision_1461.csv"
SRC_NO_SOURCE_SIGN = MICRO_COEFF / "C_parent_WEP_no_source_slot_signing_decision_1451.csv"
SRC_VARIATION_BEFORE = MICRO_COEFF / "variation_before_readout_theorem_attempt_1454.csv"
SRC_PARENT_DOMAIN = MICRO_COEFF / "parent_variation_domain_order_attempt_1455.csv"
SRC_FD = MICRO_COEFF / "C_parent_WEP_functional_derivative_definition_attempt.csv"
SRC_ZERO_ATTEMPT = MICRO_COEFF / "C_parent_WEP_slot_zero_attempt.csv"
SRC_QT_ZERO = MICRO_COEFF / "QT_zero_route_status.csv"
SRC_COUPLING = MICRO_COEFF / "C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2985_SOURCE_REGISTER.csv",
    "conditional": RESIDUALS / "P8_Y5_R2FR_2985_VERTICAL_ZERO_CONDITIONAL_THEOREM.csv",
    "ax1090": RESIDUALS / "P8_Y5_R2FR_2985_AX1090_PARENT_ACTION_OBJECT_AUDIT.csv",
    "field_map": RESIDUALS / "P8_Y5_R2FR_2985_VWEP_FIELD_MAP_SATISFACTION_AUDIT.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2985_CPARENT_ZERO_CERTIFICATE_ASSEMBLY.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2985_RETAINED_RESIDUAL_TARGETS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2985_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2985_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2985_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2985_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2985_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "conditional_copy": PARENT_ACTION / "VWEP_vertical_zero_conditional_theorem_2985_NOT_PARENT_SIGNED.csv",
    "certificate_copy": PARENT_ACTION / "C_parent_WEP_zero_certificate_assembly_2985_NOT_CLOSED.csv",
    "residuals_copy": LOCAL_BOUNDS / "VWEP_Cparent_retained_residual_targets_2985_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2985_q_vX_action_descent_or_residual_vector_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2985_00_2984_doc", SRC_2984_DOC, ["Status:", "NEXT2984_0_2985"], "2984 handoff"),
        ("SRC2985_01_2984_next", SRC_2984_NEXT, ["NEXT2984_0_2985", "V_WEP"], "selected 2985 target"),
        ("SRC2985_02_2984_zero", SRC_2984_ZERO, ["CZ2984_5_verdict", "NOT_ZERO_CERTIFIED"], "2984 C_parent zero audit"),
        ("SRC2985_03_2984_promotion", SRC_2984_PROMOTION, ["PROM2984_1_C_parent_live", "zero certificate not closed"], "2984 promotion refusal"),
        ("SRC2985_04_2984_validation", SRC_2984_VALIDATION, ["VAL2984_OVERALL"], "2984 validation"),
        ("SRC2985_05_AX1090", SRC_AX1090, ["AXP1447_3_verdict", "PARENT_OBJECT_NOT_PROVEN"], "AX1090 parent object proof attempt"),
        ("SRC2985_06_AXRED1441", SRC_AXRED1441, ["AXRED1441_0_parent_object", "NOT_REDUCED"], "AX1090 reduction audit"),
        ("SRC2985_07_VWEP_map", SRC_VWEP_MAP, ["parent_configuration", "boundary_domain_readout"], "field-by-field V_WEP map"),
        ("SRC2985_08_VWEP_candidate", SRC_VWEP_CANDIDATE, ["VWEP1448_0_candidate", "CANDIDATE_ONLY_NOT_PARENT_SIGNED"], "V_WEP generator candidate"),
        ("SRC2985_09_VWEP_domain", SRC_VWEP_DOMAIN, ["VDP1448_0_chain_rule", "VDP1448_6_verdict"], "V_WEP domain proof attempt"),
        ("SRC2985_10_QVX", SRC_QVX, ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"], "q/v_X certificate"),
        ("SRC2985_11_lift", SRC_LIFT, ["VLG1045_4_verdict", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"], "vertical matter lift gate"),
        ("SRC2985_12_no_shadow", SRC_NO_SHADOW, ["NSF1046_5_verdict", "FAIL_CURRENT_CLAIM_NO_SHADOW_FRAME_NOT_SIGNED"], "no shadow frame theorem"),
        ("SRC2985_13_constants", SRC_CONSTANTS, ["CST1047_5_verdict", "FAIL_CURRENT_CLAIM_COEFFICIENT_PROVENANCE_REQUIRED"], "constant superselection theorem"),
        ("SRC2985_14_no_source", SRC_NO_SOURCE, ["NSS1064_2_relative_weight", "retained_nonclaim"], "no source-only slot audit"),
        ("SRC2985_15_min_clause", SRC_MIN_CLAUSE, ["MPC1439_1_formal_zero", "NOT_ADOPTED_NOT_ZERO_CERTIFIED"], "minimal parent clause"),
        ("SRC2985_16_closure", SRC_CLOSURE, ["CLOS1440_1_C_parent_WEP_zero", "NOT_ZERO_CERTIFIED"], "closure demotion"),
        ("SRC2985_17_source_factor", SRC_SOURCE_FACTOR, ["SIGN1461_0_source_factorization", "C_parent_WEP_import_allowed"], "source factorization signing decision"),
        ("SRC2985_18_no_source_sign", SRC_NO_SOURCE_SIGN, ["SIGN1451_0_no_slot", "REFUSE_ZERO_IMPORT_KEEP_BOUND_INPUTS"], "no source-only slot signing decision"),
        ("SRC2985_19_variation_before", SRC_VARIATION_BEFORE, ["VBR1454_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"], "variation-before-readout theorem"),
        ("SRC2985_20_parent_domain", SRC_PARENT_DOMAIN, ["PVD1455_6_verdict", "NOT_REDUCED_KEEP_NONCLAIM_LEDGERS"], "parent variation domain order"),
        ("SRC2985_21_fd", SRC_FD, ["FD1447_1_zero_branch", "CONDITIONAL_ZERO_ONLY"], "C_parent functional derivative definition"),
        ("SRC2985_22_zero_attempt", SRC_ZERO_ATTEMPT, ["CZ1438_5_zero_certificate", "NOT_CLOSED"], "C_parent slot zero attempt"),
        ("SRC2985_23_qt_zero", SRC_QT_ZERO, ["Q_T_over_m_zero_theorem", "CLOSURE_ONLY_NOT_DERIVED"], "trace zero route"),
        ("SRC2985_24_coupling", SRC_COUPLING, ["CPD1484_5_verdict", "NOT_CLOSED"], "C_parent coupling derivation attempt"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "theorem_id": "VZT2985_0_statement",
                "object": "vertical zero theorem for C_parent_WEP",
                "formal_statement": "If S_parent = S_red[q(Phi),Psi,theta] + B and V_WEP in ker(Dq), with owned fixed/gauge matter lift, Lie_V theta=0, no source-only/shadow slots, and silent boundary/readout, then dS_parent[V_WEP]=0.",
                "proof_status": "EXACT_CONDITIONAL_THEOREM",
                "parent_signed": False,
                "why_nonclaim": "premises are not signed together in the current corpus",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_1_chain_rule",
                "object": "observed geometry term",
                "formal_statement": "delta_V S_red contains E_q[Dq(V_WEP)], and Dq(V_WEP)=0 kills the visible metric/coframe/connection contribution.",
                "proof_status": "EXACT_CONDITIONAL_MATH_PASS",
                "parent_signed": False,
                "why_nonclaim": "actual physical V_WEP is not parent-signed as the quotient-kernel generator",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_2_matter_euler",
                "object": "ordinary matter lift",
                "formal_statement": "Matter terms vanish if delta_V Psi_A is fixed/gauge/on-shell and no material marker is hidden in the lift.",
                "proof_status": "CONDITIONAL_LIFT_ONLY",
                "parent_signed": False,
                "why_nonclaim": "parent matter bundle functor does not assign a species-complete lift",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_3_constants",
                "object": "dimensionless constants and material spectra",
                "formal_statement": "partial_theta L * Lie_V theta vanishes if constants descend through q or are topological/superselected representation data.",
                "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
                "parent_signed": False,
                "why_nonclaim": "alpha, mass ratios, nuclear response, and clock constants are not parent-owned in one action",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_4_forbidden_slots",
                "object": "source-only/shadow/readout slots",
                "formal_statement": "The derivative has no w_A, J_A, c_A, shadow frame, source-worldtube, or post-readout selector term only if those slots are absent before variation.",
                "proof_status": "COUNTERMODEL_GUARD_ACTIVE",
                "parent_signed": False,
                "why_nonclaim": "pre-action selectors and hidden-visible homomorphism countermodels survive",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_5_boundary",
                "object": "boundary/domain/readout term",
                "formal_statement": "B'[V_WEP] is zero/exact/projected silent, and empirical readout acts downstream on the already-defined parent derivative.",
                "proof_status": "CONDITIONAL_NOT_SOURCE_SIGNED",
                "parent_signed": False,
                "why_nonclaim": "boundary silence, source-worldtube support, and K_CMSM readout are not tied to the parent variation",
            }
        ),
        add(
            {
                "theorem_id": "VZT2985_6_verdict",
                "object": "C_parent_WEP DERIVED_ZERO",
                "formal_statement": "The proof skeleton is valid as a theorem-if-premises-signed, but it does not currently import a DERIVED_ZERO row.",
                "proof_status": "CONDITIONAL_THEOREM_RETAINED_ZERO_NOT_CERTIFIED",
                "parent_signed": False,
                "why_nonclaim": "AX1090 parent object and V_WEP field map are unsigned",
            }
        ),
    ]


def ax1090_rows() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows(SRC_AX1090):
        out.append(
            add(
                {
                    "audit_id": f"AX2985_{row.get('proof_step_id', 'unknown')}",
                    "claim": row.get("claim", ""),
                    "test": row.get("test", ""),
                    "source_result": row.get("result", ""),
                    "evidence": row.get("evidence", ""),
                    "can_sign_AXIOM": row.get("can_sign_AX1090_0", "False"),
                    "audit_status": "NOT_SIGNED_FOR_2985",
                }
            )
        )
    for row in rows(SRC_AXRED1441):
        out.append(
            add(
                {
                    "audit_id": f"AXRED2985_{row.get('reduction_id', 'unknown')}",
                    "claim": row.get("axiom_target", ""),
                    "test": row.get("candidate_MTS_reduction", ""),
                    "source_result": row.get("reduction_status", ""),
                    "evidence": row.get("why_not_reduced", ""),
                    "can_sign_AXIOM": False,
                    "audit_status": "NOT_REDUCED_FOR_2985",
                }
            )
        )
    return out


def field_map_rows() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows(SRC_VWEP_MAP):
        status = row.get("current_status", "")
        map_satisfied = str(row.get("map_satisfied", "")).lower() == "true"
        if map_satisfied:
            verdict = "SIGNED_OR_SATISFIED"
        elif "EXACT_CONDITIONAL" in status:
            verdict = "CONDITIONAL_MATH_PASS_PARENT_UNSIGNED"
        else:
            verdict = "UNSATISFIED_BLOCKS_ZERO_CERTIFICATE"
        out.append(
            add(
                {
                    "map_id": f"FM2985_{row.get('field_block', 'unknown')}",
                    "field_block": row.get("field_block", ""),
                    "object": row.get("object", ""),
                    "proposed_V_WEP_action": row.get("proposed_V_WEP_action", ""),
                    "required_zero_or_control": row.get("required_zero_or_control", ""),
                    "current_status": status,
                    "missing_signature": row.get("missing_signature", ""),
                    "countermodel_if_unsigned": row.get("countermodel_if_unsigned", ""),
                    "map_satisfied": map_satisfied,
                    "audit_status": verdict,
                }
            )
        )
    out.append(
        add(
            {
                "map_id": "FM2985_verdict",
                "field_block": "all_blocks",
                "object": "V_WEP as parent-owned vertical generator",
                "proposed_V_WEP_action": "field-by-field action map closes simultaneously",
                "required_zero_or_control": "every map row signed or retained as finite residual",
                "current_status": "NOT_PARENT_SIGNED",
                "missing_signature": "actual parent transformation law plus matter/constants/source/boundary/readout owners",
                "countermodel_if_unsigned": "V_WEP remains symbolic and C_parent_WEP cannot be evaluated or zeroed",
                "map_satisfied": all(str(row.get("map_satisfied", "")).lower() == "true" for row in rows(SRC_VWEP_MAP)),
                "audit_status": "ZERO_CERTIFICATE_BLOCKED_BY_FIELD_MAP",
            }
        )
    )
    return out


def certificate_rows() -> list[dict[str, Any]]:
    data = [
        ("CERT2985_0_parent_action", "AX1090 parent action object", "S_parent owns fields, variation, measure/current, matter/source/readout before projection", "AXP1447_3;AXRED1441_0", "MISSING_PARENT_OBJECT", False),
        ("CERT2985_1_quotient", "q/v_X action descent", "S_parent descends through q and V_WEP is the actual ker(Dq) generator", "QVC1023_8;VDP1448_6", "MISSING_SINGLE_Q_VX_CERTIFICATE", False),
        ("CERT2985_2_field_map", "field-by-field V_WEP map", "geometry, hidden fields, matter, EM, constants, source, measure, and boundary/readout all signed", "FM2985_verdict", "FIELD_MAP_UNSATISFIED", False),
        ("CERT2985_3_no_slots", "no source-only/shadow/pre-action selectors", "no w_A, J_A, c_A, f_X, shadow frame, material marker, or source-label reentry before variation", "NSS1064;NSF1046;SIGN1451;SIGN1461", "COUNTERMODELS_SURVIVE", False),
        ("CERT2985_4_boundary_readout", "boundary/readout downstream order", "boundary exact/projected silent and readout acts only after parent derivative", "VBR1454;PVD1455", "CONDITIONAL_ORDER_ONLY", False),
        ("CERT2985_5_verdict", "C_parent_WEP DERIVED_ZERO certificate", "all certificate rows close together", "2985 assembly", "NOT_CLOSED_DO_NOT_IMPORT", False),
    ]
    return [
        add(
            {
                "certificate_id": cert_id,
                "clause": clause,
                "required_evidence": required,
                "source_anchor": anchor,
                "status": status,
                "certificate_clause_signed": signed,
                "zero_certificate_status": "QT_ZERO_CLOSED" if signed and cert_id.endswith("verdict") else "NOT_ZERO_CERTIFIED",
            }
        )
        for cert_id, clause, required, anchor, status, signed in data
    ]


def residual_rows() -> list[dict[str, Any]]:
    data = [
        ("RES2985_0_epsilon_VWEP", "epsilon_VWEP_field_map", "norm of unsigned field-map leakage", "V_WEP actual parent transformation law missing", "local_GR;WEP;R10;clock;PPN"),
        ("RES2985_1_delta_w_A", "relative source/action weights", "source-only prefactor residual", "no-source-only slot and source-label forgetting unsigned", "WEP;Newton_source;R10"),
        ("RES2985_2_b_alpha", "EM/alpha marker", "Lie_V ln alpha_EM or f_X F^2 coefficient", "unique EM kinetic owner and constant superselection unsigned", "clock;EM;R10;WEP"),
        ("RES2985_3_b_mass_clock", "mass/clock material marker", "Lie_V dimensionless spectra or clock constants", "matter spectrum superselection unsigned", "clock;WEP;particle"),
        ("RES2985_4_c_shadow", "shadow-frame/domain coupling", "hidden conformal/disformal/source frame marker", "no-shadow frame theorem unsigned", "PPN;R10;clock;WEP"),
        ("RES2985_5_Q_boundary", "boundary/source-worldtube leakage", "edge/support/readout projection residual", "boundary silence and official readout not signed", "WEP;R10;orbital"),
    ]
    return [
        add(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "meaning": meaning,
                "why_retained": why,
                "test_arenas": arenas,
                "status": "RETAINED_NONCLAIM_UNTIL_ZERO_CERTIFIED_OR_BOUNDED",
            }
        )
        for residual_id, symbol, meaning, why, arenas in data
    ]


def claim_rows() -> list[dict[str, Any]]:
    data = [
        ("CG2985_0_AX1090", "AX1090 parent object proven", False, "parent object remains not reduced", False),
        ("CG2985_1_VWEP", "V_WEP true parent vertical generator", False, "field-by-field map unsatisfied", False),
        ("CG2985_2_Cparent_zero", "C_parent_WEP DERIVED_ZERO", False, "zero certificate assembly not closed", False),
        ("CG2985_3_Cparent_import", "C_parent_WEP_slot_import.csv written", False, "live import target remains absent", False),
        ("CG2985_4_deltawe", "delta_w_e deproxied", False, "coupling/readout/source product incomplete", False),
        ("CG2985_5_local_GR", "local GR/Newton reduction", False, "residual vector retained", False),
        ("CG2985_6_empirical", "WEP/R10/PPN/clock/orbital scoring", False, "no claim-grade coefficient/product", False),
    ]
    return [add({"claim_gate_id": gate_id, "claim": claim, "condition_passed": passed, "status": status, "claim_allowed": allowed}) for gate_id, claim, passed, status, allowed in data]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2985_0_preserve_theorem",
                "decision": "Preserve the vertical-zero theorem as an exact conditional skeleton.",
                "because": "the chain rule proof is mathematically clean once S_parent descends through q and V_WEP is truly vertical.",
                "next_action": "turn the conditional into a source-signed certificate rather than repeating the proof",
            }
        ),
        add(
            {
                "decision_id": "DEC2985_1_refuse_import",
                "decision": "Do not write or promote C_parent_WEP_slot_import.csv.",
                "because": "AX1090 parent object and V_WEP field map are both unsigned; multiple countermodels remain.",
                "next_action": "retain residual vector rows until each clause is zero-certified or bounded",
            }
        ),
        add(
            {
                "decision_id": "DEC2985_2_next",
                "decision": "Attack q/v_X/action descent and actual parent transformation law next.",
                "because": "that is the upstream missing object shared by AX1090, V_WEP, QVX, boundary silence, and local-GR reduction.",
                "next_action": "build a single q-vX-action descent certificate or a finite epsilon_VWEP leakage bound",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2985_0_2986",
                "priority": "selected_primary",
                "next_doc": "2986-Y5-R2FR-q-vX-action-descent-certificate-or-epsilon-VWEP-leakage-bound-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_q_vX_action_descent_certificate_or_epsilon_VWEP_leakage_bound_under_AX1090_2986.py",
                "objective": "Try to parent-sign the upstream q/v_X/action descent certificate: q canonical, v_X/V_WEP actual field-space generator, Dq[v_X]=0, S_parent descent, matter descent, boundary silence, and rank/nondegeneracy; if not, stage epsilon_VWEP leakage bound rows.",
                "include": "q canonical;v_X field action;Dq[v_X]=0;S_parent=S_red[q]+B;matter descent;boundary silence;constraint rank;epsilon_VWEP residual",
                "exclude": "C_parent import;CMSM live-file fabrication;DD smoke promotion;unit tau shortcut;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for p in FORMALIZATION.rglob("*2985*") if p.is_file()) if FORMALIZATION.exists() else 0
    verdict_conditional = any(row["theorem_id"] == "VZT2985_6_verdict" and row["proof_status"] == "CONDITIONAL_THEOREM_RETAINED_ZERO_NOT_CERTIFIED" for row in all_rows["conditional"])
    field_map_blocked = any(row["map_id"] == "FM2985_verdict" and row["audit_status"] == "ZERO_CERTIFICATE_BLOCKED_BY_FIELD_MAP" for row in all_rows["field_map"])
    cert_not_closed = any(row["certificate_id"] == "CERT2985_5_verdict" and row["status"] == "NOT_CLOSED_DO_NOT_IMPORT" for row in all_rows["certificate"])
    checks = [
        ("VAL2985_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2985_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2985_2_conditional_theorem_retained", verdict_conditional, "vertical-zero theorem retained as conditional", True),
        ("VAL2985_3_AX1090_not_signed", all(row["audit_status"].startswith("NOT_") for row in all_rows["ax1090"]), "AX1090 parent object remains unsigned", True),
        ("VAL2985_4_field_map_blocked", field_map_blocked, "V_WEP field map blocks zero certificate", True),
        ("VAL2985_5_certificate_not_closed", cert_not_closed, "C_parent zero certificate not closed", True),
        ("VAL2985_6_no_live_cparent", not LIVE_C_PARENT.exists(), "live C_parent import target not fabricated", True),
        ("VAL2985_7_residuals_retained", len(all_rows["residuals"]) >= 6, "retained residual target rows written", True),
        ("VAL2985_8_claims_blocked", all(not row["claim_allowed"] for row in all_rows["claims"]), "all claim gates blocked", True),
        ("VAL2985_9_next_written", any(row["next_id"] == "NEXT2985_0_2986" for row in all_rows["next"]), "2986 q-vX/action target selected", True),
        ("VAL2985_10_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2985_11_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2985_12_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2985_13_formalization_clean", formal_count == 0, f"no 2985 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2985_14_doc_written", DOC.exists(), "2985 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2985_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2985 validation overall", "required": True}))
    return out_rows


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2985 - AX1090 Parent Action Object or V_WEP Vertical Generator Zero Certificate

Status: `Y5_R2FR_2985_vertical_zero_theorem_exact_conditional_AX1090_unsigned_VWEP_field_map_unsigned_Cparent_zero_not_certified_nonclaim`

Claim ceiling: `no_AX1090_parent_object_no_VWEP_parent_generator_no_Cparent_DERIVED_ZERO_no_Cparent_import_no_deltawe_deproxy_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The good news: the vertical-zero theorem is mathematically clean as a conditional chain-rule result.
- The hard stop: `AX1090` does not yet give one parent action object, and `V_WEP` is not parent-signed as the actual field-space vertical generator.
- The field-by-field map isolates the leak points: matter lift, constants, source-only weights, shadow frames, measure/current normalization, and boundary/readout.
- Therefore `C_parent_WEP = DERIVED_ZERO` is not imported and `C_parent_WEP_slot_import.csv` remains absent.
- Best next route is upstream: prove the single `q/v_X/action descent` certificate or retain an explicit `epsilon_VWEP` leakage bound.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Conditional Vertical-Zero Theorem

{table(all_rows["conditional"], ["theorem_id", "object", "proof_status", "parent_signed", "why_nonclaim"])}

## AX1090 Parent Action Audit

{table(all_rows["ax1090"], ["audit_id", "claim", "source_result", "evidence", "can_sign_AXIOM", "audit_status"])}

## V_WEP Field Map Audit

{table(all_rows["field_map"], ["map_id", "field_block", "current_status", "missing_signature", "map_satisfied", "audit_status"])}

## C_parent Zero Certificate Assembly

{table(all_rows["certificate"], ["certificate_id", "clause", "status", "certificate_clause_signed", "zero_certificate_status"])}

## Retained Residual Targets

{table(all_rows["residuals"], ["residual_id", "symbol", "meaning", "why_retained", "test_arenas", "status"])}

## Claim Gates

{table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "conditional": conditional_theorem_rows(),
        "ax1090": ax1090_rows(),
        "field_map": field_map_rows(),
        "certificate": certificate_rows(),
        "residuals": residual_rows(),
        "claims": claim_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["conditional"], BRANCH_OUTPUTS["conditional_copy"])
    shutil.copyfile(OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"])
    shutil.copyfile(OUTPUTS["residuals"], BRANCH_OUTPUTS["residuals_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2985 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
