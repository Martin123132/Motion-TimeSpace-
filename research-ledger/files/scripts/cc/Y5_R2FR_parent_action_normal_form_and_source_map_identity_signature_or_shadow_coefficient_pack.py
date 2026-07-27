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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1768"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1768_0_1767_handoff",
        "source_key": "1767_normal_form_next",
        "source_path": ROOT / "1767-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
        "needles": ["PARENT_ACTION_NORMAL_FORM_AND_SOURCE_MAP_SIGNATURE_IS_NEXT", "NEXT1767_0_primary"],
    },
    {
        "source_id": "SRC1768_1_1767_validation",
        "source_key": "1767_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1767_VALIDATION.csv",
        "needles": ["VAL1767_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1768_2_1767_identity",
        "source_key": "1767_identity_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
        "needles": ["SMI1767_1_identity_source_map", "SMI1767_5_current_verdict"],
    },
    {
        "source_id": "SRC1768_3_1767_shadow_inventory",
        "source_key": "1767_shadow_inventory",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
        "needles": ["NHB1767_5_verdict", "INVENTORY_READY_NONCLAIM"],
    },
    {
        "source_id": "SRC1768_4_1767_shadow_bound",
        "source_key": "1767_shadow_bound_interface",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1767_DELTAW_SHADOW_BOUND_INTERFACE.csv",
        "needles": ["DSH1767_0_delta_w_shadow", "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND"],
    },
    {
        "source_id": "SRC1768_5_1766_graph",
        "source_key": "1766_connected_graph",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1766_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
        "needles": ["OMC1766_1_connected_graph_implication", "OMC1766_4_current_verdict"],
    },
    {
        "source_id": "SRC1768_6_954_action_clause",
        "source_key": "954_total_hilbert_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    },
    {
        "source_id": "SRC1768_7_955_same_action",
        "source_key": "955_minimal_matter_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_REGISTER.csv",
    "normal_form": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
    "source_map_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
    "shadow_classification": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SHADOW_TERM_CLASSIFICATION_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_COUNTERMODEL_LEDGER.csv",
    "shadow_coefficient": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_SHADOW_COEFFICIENT_PACK.csv",
    "gr_bridge_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_GR_BRIDGE_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1768_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1768_VALIDATION.csv",
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
                "role": "parent action normal form and source-map identity signature or shadow coefficient pack",
                "valid_for_claim": False,
            }
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_0_parent_action_partition",
            "normal_form_clause": "parent action is the only owner of field equations",
            "mathematical_form": "S_parent=S_geom[e,Phi]+S_MTS[e,Phi,X]+S_matter_min[e,Psi,theta]+S_nonmin+S_boundary",
            "classification_rule": "every source-like term must be in the action partition or be forbidden/bounded",
            "status": "NORMAL_FORM_CONTRACT_WRITTEN",
            "remaining_gap": "current corpus has not supplied a complete parent action inventory",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_1_geometry_left_hand_owner",
            "normal_form_clause": "geometry/MTS variations belong on the left-hand operator",
            "mathematical_form": "E_LHS := delta(S_geom+S_MTS+S_nonmin_geometry)/delta e_obs",
            "classification_rule": "terms depending on geometry/MTS fields but not ordinary composition are LHS/operator residuals, not matter-source charges",
            "status": "CONDITIONAL_OWNER_RULE",
            "remaining_gap": "need explicit GR-limit operator and residual ledger",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_2_hilbert_matter_owner",
            "normal_form_clause": "ordinary matter source is total Hilbert/coframe derivative",
            "mathematical_form": "T_H := delta S_matter_min[e,Psi,theta]/delta e_obs",
            "classification_rule": "ordinary RHS source is T_H only; no post-variation material map is admitted",
            "status": "CONDITIONAL_SOURCE_IDENTITY",
            "remaining_gap": "identity-only source-map grammar still needs parent signature",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_3_nonminimal_term_owner",
            "normal_form_clause": "nonminimal matter-geometry terms must be classified explicitly",
            "mathematical_form": "S_nonmin[e,Phi,X,Psi] -> {LHS effective geometry, modified matter dynamics, or residual coefficient}",
            "classification_rule": "a nonminimal term cannot hide as an unowned source-shadow knob",
            "status": "CLASSIFICATION_REQUIRED",
            "remaining_gap": "current corpus lacks full nonminimal-term inventory",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_4_boundary_owner",
            "normal_form_clause": "boundary/improvement terms require silence or residual status",
            "mathematical_form": "delta S_boundary/delta e_obs or nabla_alpha U^{alpha mu nu}",
            "classification_rule": "boundary terms are boundary-silent under stated conditions, or become explicit bounded residuals",
            "status": "BOUNDARY_SILENCE_REQUIRED",
            "remaining_gap": "local/falloff boundary clauses not yet sourced/signed",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_5_forbidden_source_map",
            "normal_form_clause": "post-variation source maps are forbidden unless action-owned",
            "mathematical_form": "not exists F_shadow(T_H,labels) with T_active=F_shadow(T_H,labels)",
            "classification_rule": "if F_shadow is not an Euler variation, it is not part of a variational field theory and must be rejected or bounded",
            "status": "FORBIDDEN_BY_CONTRACT_NOT_PARENT_SIGNED",
            "remaining_gap": "needs parent object-language signature",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ANF1768_6_current_verdict",
            "normal_form_clause": "current MTS parent action normal form",
            "mathematical_form": "action partition is written as a signature, not proven as a complete parent action",
            "classification_rule": "use this as the next contract; do not promote local-GR/WEP/R10 claims",
            "status": "SIGNATURE_READY_PARENT_UNSIGNED",
            "remaining_gap": "complete action inventory, GR-limit operator, boundary silence, and shadow coefficients remain",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def source_map_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SMG1768_0_euler_equation_gate",
            "gate_clause": "field equation is Euler-Lagrange from S_parent",
            "mathematical_form": "delta S_parent/delta e_obs=0",
            "if_signed": "source map identity follows by variation",
            "current_status": "NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SMG1768_1_no_shadow_map_gate",
            "gate_clause": "no independent post-variation source map",
            "mathematical_form": "T_active=T_H, not F_shadow(T_H,labels)",
            "if_signed": "delta_w_shadow source-map route closes",
            "current_status": "CONTRACT_READY_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SMG1768_2_no_source_prefactor_gate",
            "gate_clause": "no source-only matter prefactors",
            "mathematical_form": "partial S_matter/partial w_A=0 for source-only w_A",
            "if_signed": "delta_w_species stays collapsed into ordinary connected block/common calibration",
            "current_status": "CONTRACT_READY_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SMG1768_3_gr_lhs_gate",
            "gate_clause": "left-hand operator has GR limit",
            "mathematical_form": "E_LHS -> G_munu + Lambda g_munu + higher-order residuals",
            "if_signed": "source-side work can connect to Einstein/Newton limit rather than only WEP",
            "current_status": "NEXT_BRIDGE_NOT_DERIVED_HERE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "SMG1768_4_current_verdict",
            "gate_clause": "source-map identity for current MTS",
            "mathematical_form": "T_active=T_H and delta_w_shadow=0",
            "if_signed": "would close the source-map loophole",
            "current_status": "NOT_CLAIMABLE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def shadow_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_0_hilbert_matter",
            "candidate_term": "minimal ordinary matter",
            "mathematical_form": "S_matter_min[e,Psi,theta]",
            "normal_form_owner": "RHS_HILBERT_SOURCE",
            "classification_status": "ALLOWED_SOURCE_OWNER",
            "zero_or_bound_action": "included in T_H; not a shadow residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_1_mts_geometry",
            "candidate_term": "MTS/geometric field terms",
            "mathematical_form": "S_MTS[e,Phi,X]",
            "normal_form_owner": "LHS_GEOMETRY_OPERATOR",
            "classification_status": "ALLOWED_LHS_OWNER_IF_ACTION_SIGNED",
            "zero_or_bound_action": "derive GR limit and residual operator, not RHS source charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_2_nonminimal_coupling",
            "candidate_term": "ordinary matter coupled directly to MTS/geometric scalars",
            "mathematical_form": "f(X,Phi,labels) L_m or A(X) J_m",
            "normal_form_owner": "MUST_CLASSIFY",
            "classification_status": "MISSING_NORMAL_FORM_DECISION",
            "zero_or_bound_action": "forbid, move to explicit modified matter dynamics, or bound as shadow/nonminimal coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_3_boundary_improvement",
            "candidate_term": "boundary/improvement source",
            "mathematical_form": "S_boundary or nabla_alpha U^{alpha mu nu}",
            "normal_form_owner": "BOUNDARY",
            "classification_status": "MISSING_BOUNDARY_SILENCE",
            "zero_or_bound_action": "prove local/falloff silence or bound boundary residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_4_nonhilbert_spin_torsion",
            "candidate_term": "spin/torsion/non-Hilbert current",
            "mathematical_form": "J_spin, J_torsion",
            "normal_form_owner": "MUST_CLASSIFY",
            "classification_status": "MISSING_ABSENCE_OR_LHS_RECLASSIFICATION",
            "zero_or_bound_action": "show absent, LHS connection geometry, improvement, or bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_5_post_variation_projector",
            "candidate_term": "post-variation material projector",
            "mathematical_form": "P_material(T_H)-T_H",
            "normal_form_owner": "FORBIDDEN_UNLESS_ACTION_OWNED",
            "classification_status": "FORBIDDEN_BY_NORMAL_FORM_CONTRACT_UNSIGNED",
            "zero_or_bound_action": "prove identity map or keep delta_w_shadow coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_6_decoupled_conserved_block",
            "candidate_term": "decoupled conserved sector",
            "mathematical_form": "T_D with nabla_mu T_D^{mu nu}=0 and no ordinary exchange edge",
            "normal_form_owner": "ARENA_INVENTORY",
            "classification_status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
            "zero_or_bound_action": "exclude from local test source or bound delta_w_decoupled",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "term_id": "SCL1768_7_verdict",
            "candidate_term": "complete shadow classification",
            "mathematical_form": "J_shadow inventory -> owner, zero theorem, or coefficient",
            "normal_form_owner": "INCOMPLETE",
            "classification_status": "CLASSIFICATION_LEDGER_READY_NONCLAIM",
            "zero_or_bound_action": "next checkpoint must source or sign the missing owner rows",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1768_0_unlisted_nonminimal_action",
            "countermodel": "a source-like nonminimal term exists but is absent from the normal form",
            "mathematical_form": "DeltaS=f(X,labels)L_m",
            "survives_current_constraints": True,
            "why_survives": "normal form is a signature, not a completed corpus inventory",
            "what_kills_it": "complete parent action inventory with forbid/reclassify/bound decision",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1768_1_post_variation_projector",
            "countermodel": "material projector is applied after Hilbert variation",
            "mathematical_form": "T_active=T_H+epsilon P_label(T_H)",
            "survives_current_constraints": True,
            "why_survives": "identity source-map grammar is not parent-signed",
            "what_kills_it": "parent action/object-language theorem forbids post-Euler source maps",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1768_2_boundary_material_residual",
            "countermodel": "boundary/domain term carries material data",
            "mathematical_form": "delta S_boundary[labels]/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "boundary silence conditions are not signed",
            "what_kills_it": "local/falloff boundary theorem or explicit boundary bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1768_3_gr_lhs_missing",
            "countermodel": "source side is clean but left-hand operator does not reduce to Einstein operator",
            "mathematical_form": "E_LHS != G_munu + Lambda g_munu + small residual",
            "survives_current_constraints": True,
            "why_survives": "1768 is source-map normal form, not a full GR-limit derivation",
            "what_kills_it": "derive left-hand GR/EH limit and Newtonian weak-field limit",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1768_4_verdict",
            "countermodel": "normal-form gaps retain source/local-GR residuals",
            "mathematical_form": "delta_w_shadow, boundary residual, nonminimal coefficient, and E_LHS residual remain",
            "survives_current_constraints": True,
            "why_survives": "signature is ready but parent inventory and GR-limit operator are not proven",
            "what_kills_it": "1769 GR-left-hand/source-normal-form bridge plus source-backed coefficient rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def shadow_coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCP1768_0_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "coefficient for post-Hilbert source-shadow/projector leakage",
            "mathematical_form": "T_active=T_H+delta_w_shadow J_shadow",
            "units": "dimensionless_or_arena_normalized",
            "status": "MISSING_NORMAL_FORM_ZERO_OR_BOUND",
            "required_input": "identity source-map parent signature or source-backed bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCP1768_1_c_nonminimal",
            "quantity": "c_nonminimal",
            "meaning": "coefficient for direct matter-MTS/geometric nonminimal source terms",
            "mathematical_form": "DeltaS=c_nonminimal f(X,Phi,labels)L_m",
            "units": "operator_dependent",
            "status": "MISSING_OPERATOR_BASIS_AND_BOUND",
            "required_input": "operator basis, dimensions, source path, arena projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCP1768_2_c_boundary",
            "quantity": "c_boundary",
            "meaning": "coefficient for material boundary/domain source residual",
            "mathematical_form": "delta S_boundary[labels]/delta e_obs",
            "units": "boundary_operator_dependent",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
            "required_input": "boundary conditions and local/falloff proof or bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCP1768_3_c_lhs_GR",
            "quantity": "E_LHS_GR_residual",
            "meaning": "left-hand deviation from Einstein operator in local/weak-field limit",
            "mathematical_form": "E_LHS-(G_munu+Lambda g_munu)",
            "units": "curvature_or_operator_units",
            "status": "MISSING_GR_LIMIT_DERIVATION",
            "required_input": "EH/Einstein limit and Newtonian weak-field residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCP1768_4_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "normal-form work remains private and nonclaim",
            "mathematical_form": "claim_allowed=false until parent normal form and GR-limit gates pass",
            "units": "status",
            "status": "NONCLAIM_LOCK",
            "required_input": "future 1769 validation",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GRB1768_0_source_side",
            "bridge_piece": "RHS source identity",
            "current_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "evidence": "ANF1768_2 and SMG1768_1",
            "remaining_gap": "identity source-map grammar and complete action inventory",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GRB1768_1_lhs_operator",
            "bridge_piece": "Einstein/GR left-hand limit",
            "current_status": "NOT_DERIVED_HERE",
            "evidence": "SMG1768_3 and SCP1768_3",
            "remaining_gap": "derive E_LHS -> G_munu + Lambda g_munu and weak-field Newton limit",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GRB1768_2_bianchi",
            "bridge_piece": "Bianchi/conservation compatibility",
            "current_status": "PARTLY_STRUCTURED",
            "evidence": "1765 exchange collapse + 1767 shadow trichotomy",
            "remaining_gap": "show final E_LHS is divergence-free or residual-balanced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GRB1768_3_newton",
            "bridge_piece": "Newtonian weak-field reduction",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "source normalization only becomes meaningful after GR LHS limit",
            "remaining_gap": "derive Poisson equation and calibrated G from the same normal form",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GRB1768_4_next",
            "bridge_piece": "next GR bridge",
            "current_status": "GR_LEFT_HAND_AND_NEWTON_LIMIT_IS_NEXT",
            "evidence": "source-map branch is narrowed enough to move to left-hand operator gate",
            "remaining_gap": "build 1769 EH/Einstein operator limit or residual coefficient pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1768_0_normal_form_gain",
            "decision": "SOURCE_SHADOW_REDUCED_TO_ACTION_NORMAL_FORM_CLASSIFICATION",
            "reason": "every source-looking term must now declare an owner or become a coefficient row",
            "next_action": "use the normal-form ledger rather than vague coupling language",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1768_1_no_promotion",
            "decision": "PARENT_NORMAL_FORM_NOT_CLAIMED",
            "reason": "complete parent action inventory and object-language signature remain unsigned",
            "next_action": "keep local-GR/WEP/R10 gates closed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1768_2_gr_bridge",
            "decision": "MOVE_NEXT_TO_LEFT_HAND_GR_LIMIT",
            "reason": "source-side coupling is narrowed; a GR reduction now needs the left-hand operator limit",
            "next_action": "derive E_LHS to Einstein tensor/Newton limit or stage residual coefficient pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1768_3_best_next",
            "decision": "GR_LEFT_HAND_EINSTEIN_AND_NEWTON_LIMIT_IS_NEXT",
            "reason": "without the LHS GR limit, a clean RHS source still does not give GR/Newton recovery",
            "next_action": "build 1769 parent-action GR-limit/EH-operator bridge or residual coefficient pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_0_parent_normal_form",
            "claim": "complete parent action normal form is signed",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_COMPLETE_ACTION_INVENTORY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_1_identity_source_map",
            "claim": "T_active equals total Hilbert source with no shadow map",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_MAP_OBJECT_LANGUAGE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_2_shadow_terms_classified",
            "claim": "all shadow/nonminimal/boundary/projector terms are zeroed or bounded",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_CLASSIFICATION_INCOMPLETE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_3_gr_lhs_limit",
            "claim": "left-hand operator reduces to Einstein/GR form",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_GR_LHS_LIMIT_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_4_newton_limit",
            "claim": "Newtonian weak-field limit follows",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_POISSON_LIMIT_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1768_5_local_GR_WEP_R10",
            "claim": "local GR / WEP / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NORMAL_FORM_AND_GR_LHS_GATES_OPEN",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1768_0_primary",
            "next_target": "1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
            "script": "scripts/Y5_R2FR_GR_left_hand_Einstein_Newton_limit_or_operator_residual_pack.py",
            "objective": "derive the parent left-hand operator limit E_LHS -> Einstein tensor plus Newton/Poisson weak-field limit, or stage explicit operator residual coefficients",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1768_1_fallback",
            "next_target": "1769b-Y5-R2FR-shadow-normal-form-coefficient-source-pack.md",
            "script": "scripts/Y5_R2FR_shadow_normal_form_coefficient_source_pack.py",
            "objective": "fill source-backed coefficient rows for nonminimal, boundary, projector, and shadow residuals if normal-form proof remains unsigned",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "normal_form": normal_form_rows(),
        "source_map_gate": source_map_gate_rows(),
        "shadow_classification": shadow_classification_rows(),
        "countermodel": countermodel_rows(),
        "shadow_coefficient": shadow_coefficient_rows(),
        "gr_bridge_status": gr_bridge_status_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1768_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1768_{key.upper()}.csv")


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
    status_keys = {"current_status", "status", "classification_status", "remaining_gap"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1768_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1768_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1768() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1768*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def normal_form_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["clause_id"] == "ANF1768_0_parent_action_partition"
        and row["status"] == "NORMAL_FORM_CONTRACT_WRITTEN"
        for row in rows_map["normal_form"]
    )


def normal_form_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["clause_id"] == "ANF1768_6_current_verdict"
        and row["status"] == "SIGNATURE_READY_PARENT_UNSIGNED"
        and row["valid_for_claim"] is False
        for row in rows_map["normal_form"]
    )


def source_map_gate_closed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["gate_id"] == "SMG1768_4_current_verdict"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_map_gate"]
    )


def shadow_classification_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["term_id"] == "SCL1768_7_verdict"
        and row["classification_status"] == "CLASSIFICATION_LEDGER_READY_NONCLAIM"
        for row in rows_map["shadow_classification"]
    ) and all(row["valid_for_claim"] is False for row in rows_map["shadow_classification"])


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1768_4_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def coefficient_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["shadow_coefficient"]
    return any(row["row_id"] == "SCP1768_0_delta_w_shadow" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def gr_bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "GRB1768_4_next"
        and row["current_status"] == "GR_LEFT_HAND_AND_NEWTON_LIMIT_IS_NEXT"
        for row in rows_map["gr_bridge_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1768_0_primary" and row["selection_status"] == "selected"
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
        check_row("VAL1768_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1768_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1768_2_normal_form_recorded", normal_form_recorded(rows_map), "parent action normal-form contract recorded", "normal-form contract missing"),
        check_row("VAL1768_3_normal_form_not_promoted", normal_form_not_promoted(rows_map), "normal form remains parent-unsigned/nonclaim", "normal form was promoted"),
        check_row("VAL1768_4_source_map_gate_closed", source_map_gate_closed(rows_map), "source-map current verdict remains not claimable", "source-map gate opened"),
        check_row("VAL1768_5_shadow_classification_nonclaim", shadow_classification_nonclaim(rows_map), "shadow classification ledger remains nonclaim", "shadow classification missing or promoted"),
        check_row("VAL1768_6_countermodel_retained", countermodel_retained(rows_map), "normal-form countermodel remains retained", "countermodel missing or promoted"),
        check_row("VAL1768_7_coefficient_pack_nonclaim", coefficient_pack_nonclaim(rows_map), "shadow/operator coefficient rows remain nonclaim", "coefficient pack missing or promoted"),
        check_row("VAL1768_8_gr_bridge_next", gr_bridge_next(rows_map), "GR left-hand/Newton bridge selected next", "GR bridge next status missing"),
        check_row(
            "VAL1768_9_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] in {"BLOCKED", "NONCLAIM_THEOREM_GATE"} for row in claim_gates),
            "all claim gates remain blocked/nonclaim",
            "one or more claim gates opened",
        ),
        check_row("VAL1768_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1768_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1768_12_decision_next",
            any(row["decision_id"] == "DEC1768_3_best_next" and row["decision"] == "GR_LEFT_HAND_EINSTEIN_AND_NEWTON_LIMIT_IS_NEXT" for row in rows_map["decision"]),
            "decision selects GR left-hand/Newton route",
            "best-next decision missing",
        ),
        check_row("VAL1768_13_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1768_14_csv_parse", csv_parse_all(), "all generated 1768 CSVs parse", "one or more generated 1768 CSVs fail to parse"),
        check_row("VAL1768_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1768_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1768_17_formalization_untouched", formalization_untouched_for_1768(), "no 1768 outputs found under formalization-workbench", "1768 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1768_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1768 parent action normal form and source-map identity signature or shadow coefficient pack",
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
        "# 1768 - Parent Action Normal Form And Source-Map Identity Signature Or Shadow Coefficient Pack",
        "",
        "## Verdict",
        "- 1768 writes the parent-action normal form needed to stop source-shadow ambiguity.",
        "- Every source-looking term now has to declare one owner: left-hand geometry/MTS operator, ordinary Hilbert matter source, boundary/improvement term, forbidden post-variation source map, or explicit bounded residual.",
        "- This makes the source-side coupling branch much cleaner, but it is still not a claim because the complete parent action inventory is not signed.",
        "- The new bottleneck is no longer vague WEP coupling; it is the GR bridge: derive the left-hand operator limit `E_LHS -> G_munu + Lambda g_munu` and then the Newton/Poisson weak-field limit.",
        "- `delta_w_shadow`, nonminimal coefficients, boundary coefficients, and the left-hand GR residual remain nonclaim rows.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Parent Action Normal Form Signature",
        markdown_table(rows_map["normal_form"], ["clause_id", "normal_form_clause", "mathematical_form", "classification_rule", "status", "remaining_gap"]),
        "",
        "## Source Map Identity Gate",
        markdown_table(rows_map["source_map_gate"], ["gate_id", "gate_clause", "mathematical_form", "if_signed", "current_status"]),
        "",
        "## Shadow Term Classification Ledger",
        markdown_table(rows_map["shadow_classification"], ["term_id", "candidate_term", "mathematical_form", "normal_form_owner", "classification_status", "zero_or_bound_action"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Shadow Coefficient Pack",
        markdown_table(rows_map["shadow_coefficient"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"]),
        "",
        "## GR Bridge Status",
        markdown_table(rows_map["gr_bridge_status"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap"]),
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
        "This checkpoint is a pivot. The source coupling work has been tightened enough that the next serious GR question is left-hand: can the parent action produce an Einstein-like operator and the Newtonian Poisson limit while keeping the cleaned Hilbert source on the right? If yes, the local branch starts looking like a real GR-reduction programme rather than a WEP patch. If not, the residual operator coefficients become the honest bound targets.",
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
    doc_path = ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1768 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
