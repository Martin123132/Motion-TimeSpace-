from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1767"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1767_0_1766_handoff",
        "source_key": "1766_source_shadow_next",
        "source_path": ROOT / "1766-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
        "needles": ["SINGLE_SOURCE_MAP_GRAMMAR_AND_SHADOW_BAN_IS_NEXT", "NEXT1766_0_primary"],
    },
    {
        "source_id": "SRC1767_1_1766_validation",
        "source_key": "1766_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1766_VALIDATION.csv",
        "needles": ["VAL1766_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1767_2_1766_shadow_attempt",
        "source_key": "1766_shadow_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_SOURCE_SHADOW_BAN_ATTEMPT.csv",
        "needles": ["SSB1766_1_variational_owner_filter", "SSB1766_4_current_verdict"],
    },
    {
        "source_id": "SRC1767_3_1766_countermodel",
        "source_key": "1766_countermodel",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM1766_1_source_shadow", "CM1766_2_hidden_projector"],
    },
    {
        "source_id": "SRC1767_4_1766_residual",
        "source_key": "1766_residual_interface",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_RESIDUAL_BOUND_INTERFACE.csv",
        "needles": ["RBI1766_1_delta_w_shadow", "MISSING_SOURCE_SHADOW_BAN_OR_BOUND"],
    },
    {
        "source_id": "SRC1767_5_954_total_hilbert",
        "source_key": "954_total_hilbert_source",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_2_total_Hilbert_derivative", "conditional_math_clean"],
    },
    {
        "source_id": "SRC1767_6_955_same_action",
        "source_key": "955_same_action_principle",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
    },
    {
        "source_id": "SRC1767_7_977_constant_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_4_single_universal_kappa", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SOURCE_REGISTER.csv",
    "source_map_identity": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
    "shadow_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
    "nonhilbert_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_COUNTERMODEL_LEDGER.csv",
    "shadow_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_DELTAW_SHADOW_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1767_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "single source-map grammar and source-shadow ban or shadow bound",
                "valid_for_claim": False,
            }
        )
    return rows


def source_map_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_0_variational_setup",
            "claim_piece": "single parent variational source owner",
            "mathematical_form": "S_parent=S_geom[Phi,e_obs]+S_matter[Psi,e_obs,theta]; delta S_parent/delta e_obs=0",
            "status": "SETUP_EXACT",
            "theorem_result": "the ordinary source entering the field equation is the Euler/Hilbert derivative of S_matter",
            "remaining_gap": "parent action normal form not yet signed for every ordinary source channel",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_1_identity_source_map",
            "claim_piece": "identity-only source map",
            "mathematical_form": "T_active := T_H := delta S_matter/delta e_obs; no independent F_shadow(T_H,labels)",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "theorem_result": "if the field equation is the Euler equation of the same action, a post-variation material source map is not an independent operation",
            "remaining_gap": "must prove no extra source map/projector is admitted by the parent object language",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_2_shadow_trichotomy",
            "claim_piece": "source-shadow classification",
            "mathematical_form": "J_shadow is either Euler variation of a real action term, a boundary/improvement term, or nonvariational",
            "status": "TRICHOTOMY_DERIVED",
            "theorem_result": "a shadow source cannot be a harmless hidden RHS knob: it is geometry/matter action content, boundary silence, or inconsistency/bound",
            "remaining_gap": "must classify allowed MTS shadow candidates in parent action normal form",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_3_bianchi_filter",
            "claim_piece": "nonvariational shadow rejection",
            "mathematical_form": "nabla_mu E^{mu nu}=0 requires nabla_mu(T_H^{mu nu}+J_shadow^{mu nu})=0",
            "status": "DERIVED_FILTER",
            "theorem_result": "an uncoupled nonvariational shadow source either violates the Bianchi/Noether identity or must be a separately conserved real block",
            "remaining_gap": "separately conserved real blocks need arena exclusion or finite bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_4_boundary_improvement_limit",
            "claim_piece": "boundary/improvement source silence",
            "mathematical_form": "J_shadow = nabla_alpha U^{alpha mu nu} or delta S_boundary/delta e_obs",
            "status": "CONDITIONAL_SILENCE",
            "theorem_result": "boundary/improvement terms do not generate a bulk composition source if falloff/local boundary conditions silence them",
            "remaining_gap": "falloff/local boundary silence still has to be parent or arena signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SMI1767_5_current_verdict",
            "claim_piece": "current MTS source-shadow zero",
            "mathematical_form": "delta_w_shadow=0 iff identity source map + no non-Hilbert/projector/boundary shadow + no decoupled block",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "theorem_result": "source-shadow is squeezed into explicit action-normal-form and boundary/projector debts, but not eliminated",
            "remaining_gap": "parent normal form and shadow candidate classification remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def shadow_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSZ1767_0_target",
            "claim_piece": "delta_w_shadow zero",
            "mathematical_form": "T_active=T_H and J_shadow=0",
            "proof_status": "TARGET_EXACT",
            "proof_result": "closes the strongest remaining source-coupling bypass if parent-signed",
            "gap": "identity source-map grammar not yet signed by parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSZ1767_1_shadow_as_action_term",
            "claim_piece": "variational shadow is real parent content",
            "mathematical_form": "J_shadow=delta DeltaS/delta e_obs",
            "proof_status": "DERIVED_RECLASSIFICATION",
            "proof_result": "not a hidden RHS knob; it must be listed as matter, geometry, nonminimal coupling, or boundary content",
            "gap": "requires parent action normal-form ledger to classify every DeltaS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSZ1767_2_shadow_as_nonvariational",
            "claim_piece": "nonvariational source-shadow",
            "mathematical_form": "J_shadow inserted into field equation without DeltaS",
            "proof_status": "DERIVED_REJECTION_OR_BOUND",
            "proof_result": "inconsistent with action/Bianchi unless separately conserved and therefore a real residual block to bound",
            "gap": "separately conserved residuals need source inventory and bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSZ1767_3_shadow_as_projector",
            "claim_piece": "post-variation source projector",
            "mathematical_form": "T_active=P_material(T_H)",
            "proof_status": "CONTRACT_NEEDED",
            "proof_result": "unless P_material=identity or comes from an action term, it is a source-shadow operation",
            "gap": "identity-only source-map theorem remains parent-unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SSZ1767_4_current_verdict",
            "claim_piece": "current source-shadow zero theorem",
            "mathematical_form": "delta_w_shadow=0",
            "proof_status": "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF",
            "proof_result": "shadow routes are now classified and sharply bounded by action normal form, but not parent-eliminated",
            "gap": "must build parent action normal-form/source-map signature or retain finite shadow coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def nonhilbert_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_0_hilbert_current",
            "candidate": "Hilbert/coframe source current",
            "mathematical_form": "T_H=delta S_matter/delta e_obs",
            "status": "PRIMARY_SOURCE_OWNER",
            "effect": "identity map source branch",
            "remaining_gap": "parent normal form must make this the only ordinary source owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_1_spin_torsion_current",
            "candidate": "spin/torsion/non-Hilbert current",
            "mathematical_form": "J_spin or J_torsion added outside T_H",
            "status": "MISSING_ABSENCE_OR_RECLASSIFICATION",
            "effect": "could carry material labels if torsion/connection are active source variables",
            "remaining_gap": "show absent, pure improvement, or left-hand geometry term; otherwise bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_2_boundary_improvement",
            "candidate": "boundary/improvement source",
            "mathematical_form": "nabla_alpha U^{alpha mu nu} or delta S_boundary/delta e_obs",
            "status": "MISSING_BOUNDARY_SILENCE",
            "effect": "could vanish under local/falloff conditions or become explicit boundary residual",
            "remaining_gap": "state falloff/local boundary conditions and source them",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_3_nonminimal_coupling",
            "candidate": "nonminimal matter-geometry coupling",
            "mathematical_form": "DeltaS=f(X,labels) R L_m or A(X) J_m",
            "status": "MISSING_NORMAL_FORM_CLASSIFICATION",
            "effect": "is not a hidden source map; it changes the parent action and must be classified as LHS geometry, matter dynamics, or residual",
            "remaining_gap": "parent action ledger must either forbid or parameterize it",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_4_post_variation_projector",
            "candidate": "post-variation material/source projector",
            "mathematical_form": "P_material(T_H)-T_H",
            "status": "MISSING_IDENTITY_PROOF_OR_BOUND",
            "effect": "most direct remaining way to fake composition dependence after a clean Hilbert source",
            "remaining_gap": "prove P_material=identity in parent grammar or bound coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NHB1767_5_verdict",
            "candidate": "non-Hilbert/source-shadow inventory",
            "mathematical_form": "J_shadow=J_spin+J_boundary+J_nonminimal+J_projector+J_decoupled",
            "status": "INVENTORY_READY_NONCLAIM",
            "effect": "all shadow channels are named and must be zeroed or bounded",
            "remaining_gap": "1768 normal-form signature or coefficient pack",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1767_0_variational_shadow_action",
            "countermodel": "extra action term produces source-like variation",
            "mathematical_form": "DeltaS_shadow[e_obs,Psi,X] with J_shadow=delta DeltaS_shadow/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "the current parent corpus has not listed and excluded all nonminimal/source-shadow action terms",
            "what_kills_it": "parent action normal form classifies every DeltaS as geometry, standard matter, boundary-silent, or forbidden",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1767_1_post_variation_projector",
            "countermodel": "source map applied after Hilbert variation",
            "mathematical_form": "T_active=T_H+epsilon P_label(T_H)",
            "survives_current_constraints": True,
            "why_survives": "identity-only source-map grammar is not parent-signed",
            "what_kills_it": "prove the field equation is purely Euler-Lagrange with no post-processing source map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1767_2_conserved_shadow_block",
            "countermodel": "separately conserved shadow block",
            "mathematical_form": "nabla_mu J_shadow^{mu nu}=0 and T_active=T_H+epsilon J_shadow",
            "survives_current_constraints": True,
            "why_survives": "Bianchi alone allows a conserved independent block",
            "what_kills_it": "arena exclusion, parent absence theorem, or finite empirical bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1767_3_boundary_material_term",
            "countermodel": "boundary/domain term carries material data",
            "mathematical_form": "delta S_boundary[material labels]/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "boundary silence/falloff is not yet signed for every local arena",
            "what_kills_it": "boundary condition proof or explicit boundary residual bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1767_4_verdict",
            "countermodel": "source-shadow residual retained",
            "mathematical_form": "T_active=T_H + delta_w_shadow J_shadow",
            "survives_current_constraints": True,
            "why_survives": "1767 classifies the loophole but does not parent-sign the normal-form exclusion",
            "what_kills_it": "1768 parent action normal-form/source-map identity signature or finite shadow bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def shadow_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSH1767_0_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "coefficient multiplying any source-shadow/non-Hilbert/projector residual",
            "mathematical_form": "T_active=T_H + delta_w_shadow J_shadow",
            "units": "dimensionless or arena-normalized",
            "status": "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND",
            "required_input": "normal-form zero theorem or source-backed bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSH1767_1_shadow_basis",
            "quantity": "J_shadow basis",
            "meaning": "basis of possible shadow currents after Hilbert variation",
            "mathematical_form": "J_shadow in {spin/torsion, boundary, nonminimal, projector, decoupled}",
            "units": "basis",
            "status": "MISSING_SHADOW_BASIS_SOURCE_PATHS",
            "required_input": "parent action normal-form ledger",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSH1767_2_projection",
            "quantity": "shadow-to-observable projection",
            "meaning": "map shadow source coefficient to WEP/R10/PPN/clock/orbital residual",
            "mathematical_form": "observable_residual = P_arena[J_shadow] delta_w_shadow",
            "units": "arena-specific",
            "status": "MISSING_ARENA_PROJECTION",
            "required_input": "local arena projection and normalization convention",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSH1767_3_bound_table",
            "quantity": "delta_w_shadow_bound",
            "meaning": "finite empirical upper bound if zero theorem fails",
            "mathematical_form": "|delta_w_shadow| <= bound",
            "units": "dimensionless or arena-normalized",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
            "required_input": "WEP/R10/PPN/clock/orbital bound source rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DSH1767_4_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "source-shadow route remains blocked",
            "mathematical_form": "claim_allowed=false until normal-form zero or finite bound closes",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "required_input": "future 1768 validation",
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1767_0_identity_map",
            "quantity": "single source-map identity",
            "current_status": "CONDITIONAL_THEOREM_READY",
            "evidence": "SMI1767_1",
            "remaining_gap": "parent action normal form must sign identity-only source map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1767_1_shadow_inventory",
            "quantity": "source-shadow inventory",
            "current_status": "CLASSIFIED_NOT_ZEROED",
            "evidence": "SMI1767_2 and NHB1767_5",
            "remaining_gap": "each candidate must be forbidden, reclassified, boundary-silenced, or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1767_2_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "SSZ1767_4 and DSH1767_0",
            "remaining_gap": "normal-form proof or finite bound missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1767_3_local_GR",
            "quantity": "local GR / WEP / R10 branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "source-shadow residual retained",
            "remaining_gap": "no local-GR, WEP, PPN, clock, orbital, or R10 pass allowed from 1767",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1767_4_next",
            "quantity": "next derivation owner",
            "current_status": "PARENT_ACTION_NORMAL_FORM_IS_NEXT",
            "evidence": "all shadow candidates reduce to action-normal-form classification",
            "remaining_gap": "build 1768 normal-form signature or shadow coefficient pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1767_0_identity_gain",
            "decision": "SOURCE_SHADOW_IS_NOT_A_FREE_COUPLING_IF_ACTION_VARIATIONAL",
            "reason": "a post-Hilbert source term must be an action term, boundary/improvement, nonvariational inconsistency, or conserved residual block",
            "next_action": "stop treating shadow as vague coupling; classify every candidate in the parent action normal form",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1767_1_no_promotion",
            "decision": "DELTA_W_SHADOW_NOT_ZEROED",
            "reason": "identity-only source-map grammar and boundary/projector silence are not parent-signed",
            "next_action": "retain delta_w_shadow as nonclaim residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1767_2_residual_interface",
            "decision": "SHADOW_BOUND_INTERFACE_STAGED",
            "reason": "if normal-form proof fails, shadow current needs a basis, projection, and bound table",
            "next_action": "do not fill numeric bounds without source-backed arena rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1767_3_best_next",
            "decision": "PARENT_ACTION_NORMAL_FORM_AND_SOURCE_MAP_SIGNATURE_IS_NEXT",
            "reason": "all remaining shadow routes reduce to whether the parent action admits them and where they live",
            "next_action": "build 1768 parent action normal-form/source-map identity signature or shadow coefficient pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_0_identity_source_map",
            "claim": "active ordinary source is exactly total Hilbert source",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_PARENT_ACTION_NORMAL_FORM_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_1_no_post_variation_projector",
            "claim": "no post-variation material source projector",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_IDENTITY_ONLY_SOURCE_MAP_GRAMMAR_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_2_no_nonhilbert_shadow",
            "claim": "no non-Hilbert/boundary/nonminimal shadow source remains",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_INVENTORY_NOT_CLASSIFIED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_3_delta_w_shadow_zero",
            "claim": "delta_w_shadow=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SHADOW_COUNTERMODELS_RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_4_delta_w_shadow_bound",
            "claim": "delta_w_shadow finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_BASIS_PROJECTION_BOUND_TABLE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1767_5_local_GR_WEP_R10",
            "claim": "local GR / WEP / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_SHADOW_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1767_0_primary",
            "next_target": "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_parent_action_normal_form_and_source_map_identity_signature_or_shadow_coefficient_pack.py",
            "objective": "write the parent action normal form that classifies every source-like term as geometry, Hilbert matter, boundary-silent, forbidden, or bounded shadow residual",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1767_1_fallback",
            "next_target": "1768b-Y5-R2FR-deltaw-shadow-basis-projection-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_shadow_basis_projection_bound_pack.py",
            "objective": "stage source-backed shadow-current basis rows, observable projections, and local bound inputs if normal-form proof remains unsigned",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "source_map_identity": source_map_identity_rows(),
        "shadow_zero": shadow_zero_rows(),
        "nonhilbert_audit": nonhilbert_audit_rows(),
        "countermodel": countermodel_rows(),
        "shadow_bound": shadow_bound_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1767_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1767_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "proof_status", "theorem_result", "proof_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1767_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1767_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1767() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1767*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def identity_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SMI1767_1_identity_source_map"
        and row["status"] == "DERIVED_CONDITIONAL_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["source_map_identity"]
    )


def shadow_trichotomy_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SMI1767_2_shadow_trichotomy"
        and row["status"] == "TRICHOTOMY_DERIVED"
        for row in rows_map["source_map_identity"]
    )


def shadow_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "SSZ1767_4_current_verdict"
        and row["proof_status"] == "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF"
        and row["claim_allowed"] is False
        for row in rows_map["shadow_zero"]
    )


def shadow_inventory_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["audit_id"] == "NHB1767_5_verdict"
        and row["status"] == "INVENTORY_READY_NONCLAIM"
        for row in rows_map["nonhilbert_audit"]
    ) and all(row["valid_for_claim"] is False for row in rows_map["nonhilbert_audit"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1767_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def shadow_bound_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["shadow_bound"]
    return any(row["row_id"] == "DSH1767_0_delta_w_shadow" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1767_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1767_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1767_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1767_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1767_2_identity_theorem", identity_theorem_recorded(rows_map), "identity source-map theorem recorded", "identity source-map theorem missing"),
        check_row("VAL1767_3_shadow_trichotomy", shadow_trichotomy_recorded(rows_map), "shadow trichotomy recorded", "shadow trichotomy missing"),
        check_row("VAL1767_4_shadow_not_promoted", shadow_not_promoted(rows_map), "source-shadow zero remains unpromoted", "source-shadow zero was promoted"),
        check_row("VAL1767_5_shadow_inventory_nonclaim", shadow_inventory_nonclaim(rows_map), "shadow inventory remains nonclaim", "shadow inventory missing or promoted"),
        check_row("VAL1767_6_countermodel_retained", countermodel_retained(rows_map), "source-shadow countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1767_7_shadow_bound_nonclaim", shadow_bound_nonclaim(rows_map), "delta_w_shadow interface rows remain nonclaim", "delta_w_shadow interface missing or promoted"),
        check_row("VAL1767_8_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked", "local source status missing or promoted"),
        check_row(
            "VAL1767_9_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in claim_gates),
            "all claim gates remain blocked/nonclaim",
            "one or more claim gates opened",
        ),
        check_row("VAL1767_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1767_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1767_12_decision_next",
            any(row["decision_id"] == "DEC1767_3_best_next" and row["decision"] == "PARENT_ACTION_NORMAL_FORM_AND_SOURCE_MAP_SIGNATURE_IS_NEXT" for row in rows_map["decision"]),
            "decision selects parent action normal-form route",
            "best-next decision missing",
        ),
        check_row("VAL1767_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1767_14_csv_parse", csv_parse_all(), "all generated 1767 CSVs parse", "one or more generated 1767 CSVs fail to parse"),
        check_row("VAL1767_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1767_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1767_17_formalization_untouched", formalization_untouched_for_1767(), "no 1767 outputs found under formalization-workbench", "1767 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1767_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1767 single source-map grammar and source-shadow ban or shadow bound",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1767 - Single Source-Map Grammar And Source-Shadow Ban Or Shadow Bound",
        "",
        "## Verdict",
        "- 1767 turns the source-shadow loophole into an action-normal-form problem.",
        "- If the parent field equation is the Euler-Lagrange equation of one parent action and ordinary matter enters through `S_matter`, the active ordinary source is the Hilbert/coframe derivative `T_H=delta S_matter/delta e_obs`; a post-variation material source map is not an independent operation.",
        "- Any `J_shadow` must be one of three things: an Euler variation of a real action term, a boundary/improvement term, or a nonvariational/conserved residual that must be excluded or bounded.",
        "- This is progress, but not a claim. Current MTS still lacks the parent action normal form that classifies every source-like term as geometry, Hilbert matter, boundary-silent, forbidden, or bounded shadow residual.",
        "- `delta_w_shadow` remains a nonclaim residual with an explicit bound interface.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Single Source-Map Identity Theorem",
        markdown_table(rows_map["source_map_identity"], ["theorem_id", "claim_piece", "mathematical_form", "status", "theorem_result", "remaining_gap"]),
        "",
        "## Source-Shadow Zero Attempt",
        markdown_table(rows_map["shadow_zero"], ["attempt_id", "claim_piece", "mathematical_form", "proof_status", "proof_result", "gap"]),
        "",
        "## Non-Hilbert Boundary Projector Audit",
        markdown_table(rows_map["nonhilbert_audit"], ["audit_id", "candidate", "mathematical_form", "status", "effect", "remaining_gap"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Delta-w Shadow Bound Interface",
        markdown_table(rows_map["shadow_bound"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
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
        "The coupling branch is getting less foggy. A shadow source is not magic dust we can sprinkle on the right-hand side. Either it comes from the parent action, in which case it must be written and owned, or it is a boundary/improvement term, or it is a nonvariational conserved residual that has to be bounded. The next useful checkpoint is the parent action normal form: sort every source-looking term into a legal owner before making any local-GR/WEP claim.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1767-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1767 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
