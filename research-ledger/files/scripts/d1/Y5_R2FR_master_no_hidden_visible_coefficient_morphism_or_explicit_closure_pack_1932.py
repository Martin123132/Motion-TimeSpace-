from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1932"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1932-Y5-R2FR-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1931_doc": ROOT / "1931-Y5-R2FR-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
    "1931_validation": OUT / "P8_Y5_BRR545_1931_VALIDATION.csv",
    "1931_signature": OUT / "P8_Y5_PARENT_QLOC_1931_PARENT_SIGNATURE_LEDGER.csv",
    "1931_theorem": OUT / "P8_Y5_PARENT_QLOC_1931_CONDITIONAL_THEOREM.csv",
    "1931_closure": OUT / "P8_Y5_PARENT_QLOC_1931_EXPLICIT_CLOSURE_LEDGER.csv",
    "1931_finite": OUT / "P8_Y5_PARENT_QLOC_1931_FINITE_SOURCE_REQUIREMENTS.csv",
    "1931_claims": OUT / "P8_Y5_PARENT_QLOC_1931_CLAIM_GATE.csv",
    "1931_next": OUT / "P8_Y5_PARENT_QLOC_1931_NEXT_TARGET.csv",
    "1105_master": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
    "1105_closure_pack": OUT / "P8_Y5_R10_1105_EXPLICIT_CLOSURE_PACK.csv",
    "1105_finite_requirements": OUT / "P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv",
    "1105_claims": OUT / "P8_Y5_R10_1105_CLAIM_GATES.csv",
    "1105_validation": OUT / "P8_Y5_BRR545_1105_VALIDATION.csv",
}

NEEDLES = {
    "1931_doc": ["SIG1931_10_verdict", "CLOS1931_1_master_closure_candidate", "VAL1931_OVERALL"],
    "1931_validation": ["VAL1931_OVERALL", "PASS"],
    "1931_signature": ["SIG1931_5_no_hidden_visible_hom", "SIG1931_10_verdict"],
    "1931_theorem": ["THM1931_1_chain_rule_if_signature_signed", "THM1931_4_verdict"],
    "1931_closure": ["CLOS1931_1_master_closure_candidate", "CLOS1931_5_finite_branch"],
    "1931_finite": ["FIN1931_0_alpha_coefficient", "FIN1931_5_mass_binding"],
    "1931_claims": ["CG1931_0_parent_signature", "CG1931_5_finite_product_claims"],
    "1931_next": ["NEXT1931_0_primary", "master-no-hidden-visible"],
    "1105_master": ["MHM1105_3_scalar_counterexample", "MHM1105_6_verdict"],
    "1105_closure_pack": ["PACK1105_0_parent_object_language", "PACK1105_4_residual_vector_if_unsigned"],
    "1105_finite_requirements": ["FIN1105_0_alpha_coefficient", "FIN1105_5_mass_binding"],
    "1105_claims": ["CG1105_0_master_theorem", "CG1105_3_finite_rows"],
    "1105_validation": ["V1105_SUMMARY", "pass"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1932_SOURCE_REGISTER.csv",
    "morphism_attempt": OUT / "P8_Y5_PARENT_QLOC_1932_MASTER_MORPHISM_ATTEMPT.csv",
    "conditional_theorem": OUT / "P8_Y5_PARENT_QLOC_1932_CONDITIONAL_DESCENT_THEOREM.csv",
    "counterexamples": OUT / "P8_Y5_PARENT_QLOC_1932_COUNTEREXAMPLE_LEDGER.csv",
    "closure_pack": OUT / "P8_Y5_PARENT_QLOC_1932_EXPLICIT_CLOSURE_PACK.csv",
    "finite_requirements": OUT / "P8_Y5_PARENT_QLOC_1932_FINITE_SOURCE_REQUIREMENTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1932_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1932_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1932_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1932_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1932_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_closure_pack": SOURCE_WEIGHT_DOCS / "ORDINARY_SECTOR_NO_HIDDEN_VISIBLE_CLOSURE_PACK_1932_NONCLAIM.csv",
    "microscope_conditional_theorem": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1932_CONDITIONAL_DESCENT_THEOREM_NONCLAIM.csv",
    "finite_queue": QUEUE / "JR1932_FIRST_FINITE_COEFFICIENT_ROW_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1932_CLAIM_GATE.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, source_path in SOURCES.items():
        path_exists = source_path.exists()
        source_text = read_text(source_path) if path_exists else ""
        missing_needles = [needle for needle in NEEDLES[source_key] if needle not in source_text]
        status = "EXISTS_NEEDLES_CONFIRMED" if path_exists and not missing_needles else "MISSING_OR_NEEDLE_FAILED"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "needed_for": "1932 master no-hidden-visible coefficient morphism audit",
                "needles": ";".join(NEEDLES[source_key]),
                "status": status,
                "missing_needles": ";".join(missing_needles),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def morphism_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MHM1932_0_target",
            "target_statement": "Hom(hidden invariant algebra, visible coefficient sheaf) is absent or constant",
            "derivation_move": "Treat visible ordinary-sector coefficients as sections generated only by quotient visible data.",
            "result": "NOT_SIGNED_BY_PARENT",
            "obstruction": "A parent rule saying coefficients descend through q is still missing.",
            "residual": "hidden-visible coefficient morphism remains a live closure candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MHM1932_1_vertical_chain_rule",
            "target_statement": "If c_vis = q^* c_bar and v_X is vertical, then Lie_v_X c_vis = 0.",
            "derivation_move": "Use Dq(v_X)=0 and the chain rule: d(q^*c_bar)(v_X)=dc_bar(Dq v_X)=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "It proves vertical silence only after descent is assumed or derived.",
            "residual": "prove coefficient descent from parent typing",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MHM1932_2_constant_quotient",
            "target_statement": "If the quotient coefficient base has no ordinary scalar moduli, descended coefficients are constants.",
            "derivation_move": "A smooth section over a connected zero-dimensional coefficient base is fixed by normalization.",
            "result": "CONDITIONAL_CONSTANT_SECTOR",
            "obstruction": "The quotient base and normalization owner are not yet parent-signed.",
            "residual": "constant-sector universality remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MHM1932_3_counterexample",
            "target_statement": "Ordinary covariance and U(1) gauge symmetry forbid hidden-dependent coefficients.",
            "derivation_move": "Test f(I_hid) F_mn F^mn, w_A(I_hid) T_A, and clock readout nu(I_hid).",
            "result": "FALSE_WITH_CURRENT_ASSUMPTIONS",
            "obstruction": "Gauge/diffeomorphism symmetry permits scalar coefficient functions unless object-language typing forbids them.",
            "residual": "active counterexample family",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MHM1932_4_verdict",
            "target_statement": "Master no-hidden-visible coefficient morphism is derived in current MTS.",
            "derivation_move": "Combine 1931 signature ledger with 1105 master morphism attempt.",
            "result": "MASTER_THEOREM_NOT_DERIVED",
            "obstruction": "Only the conditional vertical-descent theorem is clean; descent itself is unsigned.",
            "residual": "promote coefficient-descent typing to next target or keep explicit closure pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1932_0_setup",
            "statement": "Let q:P->Pbar be the parent quotient and v_X in ker(Dq) a hidden/vertical variation.",
            "proof_status": "DEFINITIONAL_SETUP",
            "proof_sketch": "Vertical means Dq(v_X)=0; visible coefficient descent means c_vis=q^*c_bar.",
            "what_it_gives": "a sharp local target for q_loc/coupling silence",
            "what_it_does_not_give": "it does not prove that c_vis descends",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1932_1_vertical_descent_zero",
            "statement": "If c_vis=q^*c_bar, then dc_vis(v_X)=0 for every v_X in ker(Dq).",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "dc_vis(v_X)=d(q^*c_bar)(v_X)=dc_bar(Dq(v_X))=dc_bar(0)=0.",
            "what_it_gives": "the mathematical shape of the desired no-coupling result",
            "what_it_does_not_give": "the parent action signature clause c_vis=q^*c_bar",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1932_2_local_residual_vector",
            "statement": "If descent fails, the residual vector is R_c(v_X)=dc_vis(v_X).",
            "proof_status": "EXACT_DIAGNOSTIC",
            "proof_sketch": "The obstruction is the vertical derivative of the visible coefficient section.",
            "what_it_gives": "a direct object to bound in alpha, WEP/source, clock, R10, and mass/binding branches",
            "what_it_does_not_give": "a zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1932_3_constant_if_base_trivial",
            "statement": "If the descended coefficient base is connected and has no scalar moduli, c_bar is fixed by one normalization.",
            "proof_status": "CONDITIONAL_CONSTANT_SECTOR",
            "proof_sketch": "With no allowed coordinate/invariant on the coefficient base, there is no nonconstant smooth coefficient function.",
            "what_it_gives": "the clean route to alpha/source/clock/mass universality",
            "what_it_does_not_give": "a proof that the parent quotient has trivial coefficient base",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM1932_4_verdict",
            "statement": "The master no-hidden-visible coefficient morphism is proved.",
            "proof_status": "NOT_DERIVED",
            "proof_sketch": "Current evidence proves only the conditional chain-rule zero after coefficient descent.",
            "what_it_gives": "a precise next derivation target",
            "what_it_does_not_give": "local GR/WEP/R10/clock/alpha claim permission",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CEX1932_0_hidden_scalar_F2",
            "sector": "alpha/EM",
            "allowed_term": "f(I_hid) F_mn F^mn",
            "why_allowed_without_closure": "I_hid is a scalar and F_mn F^mn is gauge/diffeomorphism invariant.",
            "damage": "alpha can drift unless f is constant or absent",
            "status": "ACTIVE_IF_COEFFICIENT_DESCENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CEX1932_1_composition_source_weight",
            "sector": "WEP/source",
            "allowed_term": "w_A(I_hid) T_A or w_A(I_hid) m_A",
            "why_allowed_without_closure": "A scalar source weight can be written while preserving ordinary covariance.",
            "damage": "composition dependence and WEP residuals remain possible",
            "status": "ACTIVE_IF_SOURCE_DESCENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CEX1932_2_clock_readout",
            "sector": "clock/readout",
            "allowed_term": "nu_clock = nu_0[1+k(I_hid-I_0)]",
            "why_allowed_without_closure": "Readout maps can carry hidden dependence unless radiative/readout descent is signed.",
            "damage": "clock bounds cannot be claimed as zero by geometry alone",
            "status": "ACTIVE_IF_READOUT_DESCENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CEX1932_3_mass_binding",
            "sector": "mass/binding",
            "allowed_term": "m_A(I_hid) and E_bind,A(I_hid)",
            "why_allowed_without_closure": "Mass and binding coefficients are scalar ordinary-sector inputs unless their owner is fixed.",
            "damage": "material response can leak into WEP and orbital tests",
            "status": "ACTIVE_IF_MASS_OWNER_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CEX1932_4_boundary_projection",
            "sector": "boundary/local projection",
            "allowed_term": "boundary or representative-dependent coefficient shift",
            "why_allowed_without_closure": "Projection maps can generate apparent local coefficients if boundary silence is not proved.",
            "damage": "local q_loc residuals can reappear after an apparent bulk zero",
            "status": "ACTIVE_IF_BOUNDARY_SILENCE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def closure_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_0_parent_object_language",
            "closure_clause": "visible coefficients are generated only from quotient-visible data and fixed representation labels",
            "role": "forbids hidden scalar slots in alpha, masses, source weights, clocks, and R10 coefficients",
            "status": "EXPLICIT_CLOSURE_UNLESS_DERIVED",
            "next_derivation_test": "prove this as a typing theorem of the parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_1_coefficient_descent",
            "closure_clause": "c_vis = q^* c_bar for each visible ordinary-sector coefficient",
            "role": "turns vertical hidden variation into dc_vis(v_X)=0 by chain rule",
            "status": "BEST_DERIVABLE_SUBTARGET",
            "next_derivation_test": "derive from quotient/category structure rather than assume",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_2_hidden_invariant_triviality_or_no_target",
            "closure_clause": "either hidden invariant algebra is trivial or no visible coefficient target accepts it",
            "role": "kills f(I_hid), w_A(I_hid), m_A(I_hid), and nu(I_hid) counterexamples",
            "status": "UNSIGNED_STRONG_CLAUSE",
            "next_derivation_test": "classify hidden invariants and visible target spaces",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_3_radiative_readout_stability",
            "closure_clause": "effective action and readout maps preserve coefficient descent",
            "role": "prevents loops, clocks, and measurement maps from reintroducing hidden-visible coefficients",
            "status": "UNSIGNED_EFT_READOUT_CLAUSE",
            "next_derivation_test": "make radiative/readout silence a theorem or finite residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_4_boundary_projection_silence",
            "closure_clause": "boundary and local projection operations do not generate representative-dependent visible coefficients",
            "role": "protects local q_loc and PPN branches from boundary leakage",
            "status": "UNSIGNED_LOCAL_CLAUSE",
            "next_derivation_test": "audit boundary terms and projection maps",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "closure_id": "PACK1932_5_finite_fallback",
            "closure_clause": "if any closure is unsigned, keep finite coefficient/product rows and score only sourced values",
            "role": "keeps theory testable without pretending the zero theorem exists",
            "status": "FALLBACK_BRANCH_ACTIVE",
            "next_derivation_test": "choose first finite source-backed row if coefficient descent cannot be signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def finite_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_0_alpha_coefficient",
            "channel": "alpha/EM",
            "needed_input": "theorem-zero no-extra-F2 or source-backed b_alpha/c_alpha coefficient",
            "why_needed": "CEX1932_0 permits f(I_hid)F^2 until coefficient descent is signed",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_1_WEP_source_weight",
            "channel": "WEP/source",
            "needed_input": "theorem-zero Delta w_A or source-backed beta_source/tau_WEP product",
            "why_needed": "CEX1932_1 permits composition weights",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_2_clock_product",
            "channel": "clock/readout",
            "needed_input": "numeric tau_clock, Xhat normalization, and clock readout coefficient",
            "why_needed": "CEX1932_2 permits hidden-dependent readout",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_3_R10_product",
            "channel": "R10 short range",
            "needed_input": "numeric alpha(lambda), lambda, tau_R10, and valid bound curve row",
            "why_needed": "R10 cannot use closure-only coefficients as claim evidence",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_4_mass_binding",
            "channel": "mass/binding/material",
            "needed_input": "theorem-zero mass/binding hidden dependence or sourced b_m and b_bind rows",
            "why_needed": "CEX1932_3 permits material response residuals",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "FIN1932_5_boundary_projection",
            "channel": "local q_loc/PPN/orbital",
            "needed_input": "boundary silence theorem or explicit projection residual coefficient",
            "why_needed": "CEX1932_4 permits local coefficient leakage",
            "claim_status": "BLOCKED_SOURCE_OR_THEOREM_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gate_data = [
        ("CG1932_0_master_morphism", "master no-hidden-visible coefficient morphism is derived", "descent/typing clause unsigned"),
        ("CG1932_1_alpha_zero", "alpha hidden-visible coefficient is theorem-zero", "F^2 scalar counterexample remains active"),
        ("CG1932_2_WEP_source_zero", "WEP/source composition weights are theorem-zero", "source weight counterexample remains active"),
        ("CG1932_3_clock_zero", "clock/readout hidden dependence is theorem-zero", "readout closure remains unsigned"),
        ("CG1932_4_local_GR_Newton", "local GR/Newton reduction is derived", "ordinary-sector coefficient descent is necessary but not sufficient"),
        ("CG1932_5_finite_rows", "finite coefficient rows are source-backed and scoreable", "rows are queued, not sourced"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "FAIL_BLOCKED",
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for gate_id, claim, reason in gate_data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1932_0_master_verdict",
            "decision": "MASTER_MORPHISM_NOT_DERIVED",
            "rationale": "The vertical chain-rule zero is exact only after coefficient descent is assumed or derived.",
            "next_action": "split master closure into a coefficient-descent typing theorem and finite source fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1932_1_best_route",
            "decision": "ATTACK_COEFFICIENT_DESCENT_TYPING_NEXT",
            "rationale": "This is narrower and more defensible than trying to prove the whole master morphism in one swing.",
            "next_action": "prove c_vis=q^*c_bar from parent object-language typing or list the minimal closure explicitly",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1932_2_empirical_fallback",
            "decision": "FINITE_ROWS_REMAIN_NONCLAIM_PRESSURE_TESTS",
            "rationale": "If descent cannot be signed, alpha/WEP/clock/R10/mass branches need real coefficients.",
            "next_action": "choose one finite row only after the derivation route is exhausted or made explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1932_0_primary",
            "selection_status": "selected",
            "target_doc": "1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md",
            "target_script": "scripts/Y5_R2FR_coefficient_descent_typing_proof_or_finite_source_row_selection_1933.py",
            "objective": "prove visible ordinary-sector coefficient sections descend through the parent quotient, c_vis=q^*c_bar, so vertical hidden variations give dc_vis(v_X)=0; if unsigned, select the first finite source-backed coefficient row without making claims",
            "success_condition": "a parent-signed coefficient descent theorem, or a minimal explicit closure plus a single finite source-row acquisition target",
            "do_not": "do not claim local GR, set hidden coefficients to zero by taste, use standalone b_alpha, set tau=1, absorb source weights into measured G, or modify formalization-workbench",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1932_0_project_position",
            "status": "DERIVATION_GATE_NARROWED",
            "summary": "1932 reduces the coupling problem to coefficient descent through the parent quotient.",
            "strongest_result": "dc_vis(v_X)=0 follows exactly if c_vis=q^*c_bar and v_X is vertical.",
            "missing_piece": "parent object-language typing or quotient construction that forces c_vis=q^*c_bar",
            "claim_position": "all local-GR/WEP/R10/clock/alpha claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_closure_pack"], rows_by_name["closure_pack"])
    write_csv(BRANCH_COPIES["microscope_conditional_theorem"], rows_by_name["conditional_theorem"])
    write_csv(BRANCH_COPIES["finite_queue"], rows_by_name["finite_requirements"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for artifact in FORMALIZATION.rglob("*1932*") if artifact.is_file())


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation_rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        validation_rows.append(
            {
                "validation_id": validation_id,
                "status": "PASS" if status else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    add("VAL1932_00_sources", source_ok, "all local source paths exist and needles found")

    morphism_ok = any(row["result"] == "MASTER_THEOREM_NOT_DERIVED" for row in rows_by_name["morphism_attempt"]) and any(
        row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_by_name["morphism_attempt"]
    )
    add("VAL1932_01_morphism_attempt", morphism_ok, "master theorem not promoted; conditional vertical theorem retained")

    theorem_ok = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_by_name["conditional_theorem"]) and any(
        row["proof_status"] == "NOT_DERIVED" for row in rows_by_name["conditional_theorem"]
    )
    add("VAL1932_02_conditional_theorem", theorem_ok, "coefficient descent gives a clean chain-rule zero but remains unsigned")

    counterexamples_ok = len(rows_by_name["counterexamples"]) == 5 and all(
        str(row["status"]).startswith("ACTIVE_IF_") for row in rows_by_name["counterexamples"]
    )
    add("VAL1932_03_counterexamples", counterexamples_ok, "alpha, WEP/source, clock, mass/binding, and boundary counterexamples active")

    closure_ok = len(rows_by_name["closure_pack"]) == 6 and any(
        row["closure_id"] == "PACK1932_1_coefficient_descent" for row in rows_by_name["closure_pack"]
    )
    add("VAL1932_04_closure_pack", closure_ok, "explicit closure pack includes coefficient descent, readout, boundary, and fallback clauses")

    finite_ok = len(rows_by_name["finite_requirements"]) == 6 and all(
        row["claim_status"] == "BLOCKED_SOURCE_OR_THEOREM_REQUIRED" for row in rows_by_name["finite_requirements"]
    )
    add("VAL1932_05_finite_requirements", finite_ok, "finite source requirements remain nonclaim")

    gates_ok = len(rows_by_name["claim_gate"]) == 6 and all(row["status"] == "FAIL_BLOCKED" for row in rows_by_name["claim_gate"])
    add("VAL1932_06_claim_gates_blocked", gates_ok, "all local GR/WEP/R10/clock/alpha claim gates remain blocked")

    decision_ok = any(row["decision"] == "ATTACK_COEFFICIENT_DESCENT_TYPING_NEXT" for row in rows_by_name["decision"])
    add("VAL1932_07_decision", decision_ok, "coefficient descent typing selected as next target")

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1933-Y5-R2FR-coefficient-descent")
    add("VAL1932_08_next_target", next_ok, "1933 coefficient descent target selected")

    claim_flags_ok = all(
        str(row.get("valid_for_claim")) == "False" and str(row.get("claim_allowed")) == "False"
        for rows in rows_by_name.values()
        for row in rows
    )
    add("VAL1932_09_claim_flags_safe", claim_flags_ok, "claim flags all false")

    csv_ok = True
    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        try:
            csv_ok = csv_ok and bool(parse_csv(output_path))
        except Exception:
            csv_ok = False
    add("VAL1932_10_csv_parse", csv_ok, "all generated CSVs parse with rows")

    copies_ok = all(path.exists() and bool(parse_csv(path)) for path in BRANCH_COPIES.values())
    add("VAL1932_11_branch_copies", copies_ok, "; ".join(str(path) for path in BRANCH_COPIES.values()))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    add("VAL1932_12_pycache_absent", pycache_absent, "scripts __pycache__ absent")

    formalization_count = formalization_artifact_count()
    add("VAL1932_13_formalization_untouched", formalization_count == 0, f"formalization_1932_artifact_count={formalization_count}")

    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "validation_id": "VAL1932_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1932 master no-hidden-visible coefficient morphism or explicit closure pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1932 Y5 R2FR: Master No-Hidden-Visible Coefficient Morphism or Explicit Closure Pack",
        "",
        "## Verdict",
        "",
        "The master no-hidden-visible coefficient morphism is **not derived** in the current parent signature. The clean theorem we do have is conditional: if a visible coefficient descends through the parent quotient, `c_vis=q^*c_bar`, then every vertical hidden variation gives `dc_vis(v_X)=0`. That is useful, sharp, and not enough by itself.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Master Morphism Attempt",
        "",
        markdown_table(rows_by_name["morphism_attempt"]),
        "",
        "## Conditional Descent Theorem",
        "",
        markdown_table(rows_by_name["conditional_theorem"]),
        "",
        "## Counterexample Ledger",
        "",
        markdown_table(rows_by_name["counterexamples"]),
        "",
        "## Explicit Closure Pack",
        "",
        markdown_table(rows_by_name["closure_pack"]),
        "",
        "## Finite Source Requirements",
        "",
        markdown_table(rows_by_name["finite_requirements"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "morphism_attempt": morphism_attempt_rows(),
        "conditional_theorem": conditional_theorem_rows(),
        "counterexamples": counterexample_rows(),
        "closure_pack": closure_pack_rows(),
        "finite_requirements": finite_requirement_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
