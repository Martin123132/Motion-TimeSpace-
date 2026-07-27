from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_PARENT_ACTION_NORMAL_FORM_GATE_2618"
CHECKPOINT_ID = "2618"

DOC = ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_LINEAGE_LEDGER.csv",
    "normal_form": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
    "source_map_gate": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SOURCE_MAP_IDENTITY_GATE.csv",
    "shadow_classification": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_TERM_CLASSIFICATION_LEDGER.csv",
    "countermodel": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_COUNTERMODEL_LEDGER.csv",
    "shadow_coefficient": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_COEFFICIENT_PACK.csv",
    "gr_bridge_status": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_GR_BRIDGE_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2618_VALIDATION.csv",
}

COPY_TARGETS = {
    "normal_form": LOCAL_BOUNDS / "Parent_action_normal_form_signature_2618_NONCLAIM.csv",
    "shadow_coefficient": LOCAL_BOUNDS / "Shadow_coefficient_pack_2618_NONCLAIM.csv",
    "gr_bridge_status": LOCAL_BOUNDS / "GR_bridge_status_2618_NONCLAIM.csv",
    "next_target": QUEUE / "JR2618_GR_LEFT_HAND_EINSTEIN_NEWTON_NEXT.csv",
}

FALSE_FLAGS = {
    "score_ready": False,
    "valid_prediction_row": False,
    "valid_for_claim": False,
    "claim_allowed": False,
    "accepted_for_scoring": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": utc_now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def false_flags() -> dict[str, bool]:
    return dict(FALSE_FLAGS)


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2618_00_2617_handoff_doc",
            "source_key": "2617_normal_form_next",
            "source_path": ROOT / "2617-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
            "needles": ["NEXT2617_0_primary", "PARENT_ACTION_NORMAL_FORM_AND_SOURCE_MAP_SIGNATURE_IS_NEXT", "VAL2617_OVERALL"],
            "role": "current 26xx handoff selecting parent action normal form",
        },
        {
            "source_id": "SRC2618_01_2617_identity",
            "source_key": "2617_identity_theorem",
            "source_path": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
            "needles": ["SMI2617_1_identity_source_map", "SMI2617_5_current_verdict"],
            "role": "current identity source-map theorem and parent unsigned verdict",
        },
        {
            "source_id": "SRC2618_02_2617_shadow_inventory",
            "source_key": "2617_shadow_inventory",
            "source_path": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
            "needles": ["NHB2617_5_verdict", "INVENTORY_READY_NONCLAIM"],
            "role": "current non-Hilbert/boundary/projector inventory",
        },
        {
            "source_id": "SRC2618_03_2617_shadow_bound",
            "source_key": "2617_shadow_bound_interface",
            "source_path": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_DELTAW_SHADOW_BOUND_INTERFACE.csv",
            "needles": ["DSH2617_0_delta_w_shadow", "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND"],
            "role": "current shadow coefficient interface",
        },
        {
            "source_id": "SRC2618_04_1768_doc",
            "source_key": "1768_prior_normal_form_doc",
            "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
            "needles": ["ANF1768_6_current_verdict", "DEC1768_3_best_next", "VAL1768_OVERALL"],
            "role": "prior normal-form checkpoint used as lineage evidence",
        },
        {
            "source_id": "SRC2618_05_1768_normal_form",
            "source_key": "1768_normal_form_signature",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1768_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv",
            "needles": ["ANF1768_0_parent_action_partition", "ANF1768_6_current_verdict"],
            "role": "prior normal-form signature and unsigned verdict",
        },
        {
            "source_id": "SRC2618_06_1768_source_map",
            "source_key": "1768_source_map_gate",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1768_SOURCE_MAP_IDENTITY_GATE.csv",
            "needles": ["SMG1768_0_euler_equation_gate", "SMG1768_4_current_verdict"],
            "role": "prior source-map gate and GR LHS pointer",
        },
        {
            "source_id": "SRC2618_07_1768_shadow_classification",
            "source_key": "1768_shadow_classification",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1768_SHADOW_TERM_CLASSIFICATION_LEDGER.csv",
            "needles": ["SCL1768_0_hilbert_matter", "SCL1768_7_verdict"],
            "role": "prior shadow classification ledger",
        },
        {
            "source_id": "SRC2618_08_1768_gr_bridge",
            "source_key": "1768_gr_bridge_status",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1768_GR_BRIDGE_STATUS.csv",
            "needles": ["GRB1768_1_lhs_operator", "GRB1768_4_next"],
            "role": "prior GR bridge status selecting LHS/Newton target",
        },
        {
            "source_id": "SRC2618_09_2616_graph",
            "source_key": "2616_connected_graph",
            "source_path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv",
            "needles": ["OMC2616_1_connected_graph_implication", "OMC2616_4_current_verdict"],
            "role": "current connected-ordinary-source theorem behind source-side normalization",
        },
        {
            "source_id": "SRC2618_10_954_action_clause",
            "source_key": "954_parent_action_clause",
            "source_path": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
            "role": "parent action clauses for source identity",
        },
        {
            "source_id": "SRC2618_11_955_same_action",
            "source_key": "955_minimal_matter_lemma",
            "source_path": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
            "role": "same-action principle and parent unsigned minimal matter verdict",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_key": spec["source_key"],
                    "source_path": spec["source_path"],
                    "source_exists": spec["source_path"].exists(),
                    "needles": spec["needles"],
                    "needles_present": not missing,
                    "missing_needles": missing,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "lineage_id": "LIN2618_0_current_parent",
            "input_checkpoint": "2617",
            "input_artifact": "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_*",
            "imported_result": "source-shadow reduced to action-normal-form classification",
            "2618_use": "write the source-side parent action signature explicitly",
        },
        {
            "lineage_id": "LIN2618_1_prior_normal_form",
            "input_checkpoint": "1768",
            "input_artifact": "P8_Y5_PARENT_QLOC_1768_*",
            "imported_result": "normal-form contract exists but parent inventory and GR LHS limit are unsigned",
            "2618_use": "port verdict into current 26xx chain without claiming GR",
        },
        {
            "lineage_id": "LIN2618_2_source_side_stack",
            "input_checkpoint": "2614-2617",
            "input_artifact": "Hom/species/Noether/graph/shadow gates",
            "imported_result": "source-side coupling has been narrowed to normal-form residual rows",
            "2618_use": "pivot next work toward left-hand Einstein/Newton operator limit",
        },
        {
            "lineage_id": "LIN2618_3_gr_bridge",
            "input_checkpoint": "1768",
            "input_artifact": "GR bridge status",
            "imported_result": "clean RHS source still does not imply GR without E_LHS -> Einstein tensor and Poisson limit",
            "2618_use": "select 2619 GR-left-hand/Newton limit target",
        },
        {
            "lineage_id": "LIN2618_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and validation ledgers",
            "imported_result": "no local-GR/Newton/WEP/PPN/clock/orbital/R10 claim while normal-form and LHS gates are open",
            "2618_use": "keep all claim flags false",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def normal_form_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "ANF2618_0_parent_action_partition",
            "normal_form_clause": "parent action is the only owner of field equations",
            "mathematical_form": "S_parent=S_geom[e,Phi]+S_MTS[e,Phi,X]+S_matter_min[e,Psi,theta]+S_nonmin+S_boundary",
            "classification_rule": "every source-like term must be in the action partition or be forbidden/bounded",
            "status": "NORMAL_FORM_CONTRACT_WRITTEN",
            "remaining_gap": "current corpus has not supplied a complete parent action inventory",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_1_geometry_left_hand_owner",
            "normal_form_clause": "geometry/MTS variations belong on the left-hand operator",
            "mathematical_form": "E_LHS := delta(S_geom+S_MTS+S_nonmin_geometry)/delta e_obs",
            "classification_rule": "terms depending on geometry/MTS fields but not ordinary composition are LHS/operator residuals, not matter-source charges",
            "status": "CONDITIONAL_OWNER_RULE",
            "remaining_gap": "need explicit GR-limit operator and residual ledger",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_2_hilbert_matter_owner",
            "normal_form_clause": "ordinary matter source is total Hilbert/coframe derivative",
            "mathematical_form": "T_H := delta S_matter_min[e,Psi,theta]/delta e_obs",
            "classification_rule": "ordinary RHS source is T_H only; no post-variation material map is admitted",
            "status": "CONDITIONAL_SOURCE_IDENTITY",
            "remaining_gap": "identity-only source-map grammar still needs parent signature",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_3_nonminimal_term_owner",
            "normal_form_clause": "nonminimal matter-geometry terms must be classified explicitly",
            "mathematical_form": "S_nonmin[e,Phi,X,Psi] -> {LHS effective geometry, modified matter dynamics, or residual coefficient}",
            "classification_rule": "a nonminimal term cannot hide as an unowned source-shadow knob",
            "status": "CLASSIFICATION_REQUIRED",
            "remaining_gap": "current corpus lacks full nonminimal-term inventory",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_4_boundary_owner",
            "normal_form_clause": "boundary/improvement terms require silence or residual status",
            "mathematical_form": "delta S_boundary/delta e_obs or nabla_alpha U^{alpha mu nu}",
            "classification_rule": "boundary terms are boundary-silent under stated conditions, or become explicit bounded residuals",
            "status": "BOUNDARY_SILENCE_REQUIRED",
            "remaining_gap": "local/falloff boundary clauses not yet sourced/signed",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_5_forbidden_source_map",
            "normal_form_clause": "post-variation source maps are forbidden unless action-owned",
            "mathematical_form": "not exists F_shadow(T_H,labels) with T_active=F_shadow(T_H,labels)",
            "classification_rule": "if F_shadow is not an Euler variation, it is not part of a variational field theory and must be rejected or bounded",
            "status": "FORBIDDEN_BY_CONTRACT_NOT_PARENT_SIGNED",
            "remaining_gap": "needs parent object-language signature",
            "parent_signed": False,
        },
        {
            "clause_id": "ANF2618_6_current_verdict",
            "normal_form_clause": "current MTS parent action normal form",
            "mathematical_form": "action partition is written as a signature, not proven as a complete parent action",
            "classification_rule": "use this as the next contract; do not promote local-GR/WEP/R10 claims",
            "status": "SIGNATURE_READY_PARENT_UNSIGNED",
            "remaining_gap": "complete action inventory, GR-limit operator, boundary silence, and shadow coefficients remain",
            "parent_signed": False,
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_map_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "SMG2618_0_euler_equation_gate",
            "gate": "field equation is Euler-Lagrange from S_parent",
            "mathematical_form": "delta S_parent/delta e_obs=0",
            "would_imply": "source map identity follows by variation",
            "status": "NOT_PARENT_SIGNED",
        },
        {
            "gate_id": "SMG2618_1_no_shadow_map_gate",
            "gate": "no independent post-variation source map",
            "mathematical_form": "T_active=T_H, not F_shadow(T_H,labels)",
            "would_imply": "delta_w_shadow source-map route closes",
            "status": "CONTRACT_READY_UNSIGNED",
        },
        {
            "gate_id": "SMG2618_2_no_source_prefactor_gate",
            "gate": "no source-only matter prefactors",
            "mathematical_form": "partial S_matter/partial w_A=0 for source-only w_A",
            "would_imply": "delta_w_species stays collapsed into ordinary connected block/common calibration",
            "status": "CONTRACT_READY_UNSIGNED",
        },
        {
            "gate_id": "SMG2618_3_gr_lhs_gate",
            "gate": "left-hand operator has GR limit",
            "mathematical_form": "E_LHS -> G_munu + Lambda g_munu + higher-order residuals",
            "would_imply": "source-side work can connect to Einstein/Newton limit rather than only WEP",
            "status": "NEXT_BRIDGE_NOT_DERIVED_HERE",
        },
        {
            "gate_id": "SMG2618_4_current_verdict",
            "gate": "source-map identity for current MTS",
            "mathematical_form": "T_active=T_H and delta_w_shadow=0",
            "would_imply": "would close the source-map loophole",
            "status": "NOT_CLAIMABLE",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def shadow_classification_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "class_id": "SCL2618_0_hilbert_matter",
            "term": "minimal ordinary matter",
            "mathematical_form": "S_matter_min[e,Psi,theta]",
            "owner": "RHS_HILBERT_SOURCE",
            "status": "ALLOWED_SOURCE_OWNER",
            "next_action": "included in T_H; not a shadow residual",
        },
        {
            "class_id": "SCL2618_1_geometry_operator",
            "term": "pure geometry/MTS operator",
            "mathematical_form": "S_geom+S_MTS",
            "owner": "LHS_OPERATOR",
            "status": "ALLOWED_LHS_OWNER",
            "next_action": "must derive GR/EH/Newton limit",
        },
        {
            "class_id": "SCL2618_2_nonminimal_coupling",
            "term": "ordinary matter coupled directly to MTS/geometric scalars",
            "mathematical_form": "f(X,Phi,labels) L_m or A(X) J_m",
            "owner": "MUST_CLASSIFY",
            "status": "MISSING_NORMAL_FORM_DECISION",
            "next_action": "forbid, move to explicit modified matter dynamics, or bound as shadow/nonminimal coefficient",
        },
        {
            "class_id": "SCL2618_3_boundary_improvement",
            "term": "boundary/improvement term",
            "mathematical_form": "S_boundary or nabla_alpha U^{alpha mu nu}",
            "owner": "BOUNDARY_OR_RESIDUAL",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
            "next_action": "prove silence under local/falloff conditions or retain coefficient",
        },
        {
            "class_id": "SCL2618_4_nonHilbert_label_current",
            "term": "spin/torsion/non-Hilbert label current",
            "mathematical_form": "J_spin, J_torsion, J_label",
            "owner": "MUST_CLASSIFY",
            "status": "MISSING_ABSENCE_RECLASSIFICATION_OR_BOUND",
            "next_action": "show absent, LHS geometry, pure improvement, or bounded residual",
        },
        {
            "class_id": "SCL2618_5_post_variation_projector",
            "term": "post-variation material projector",
            "mathematical_form": "P_material(T_H)-T_H",
            "owner": "FORBIDDEN_UNLESS_ACTION_OWNED",
            "status": "FORBIDDEN_BY_NORMAL_FORM_CONTRACT_UNSIGNED",
            "next_action": "prove identity map or keep delta_w_shadow coefficient",
        },
        {
            "class_id": "SCL2618_6_decoupled_block",
            "term": "separately conserved decoupled block",
            "mathematical_form": "J_dec with nabla_mu J_dec^{mu nu}=0",
            "owner": "ARENA_INVENTORY_OR_RESIDUAL",
            "status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
            "next_action": "exclude from tested ordinary source or bound",
        },
        {
            "class_id": "SCL2618_7_verdict",
            "term": "complete shadow classification",
            "mathematical_form": "J_shadow inventory -> owner, zero theorem, or coefficient",
            "owner": "INCOMPLETE",
            "status": "CLASSIFICATION_LEDGER_READY_NONCLAIM",
            "next_action": "next checkpoint must source or sign the missing owner rows",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2618_0_unlisted_nonminimal_action",
            "countermodel": "a source-like nonminimal term exists but is absent from the normal form",
            "mathematical_form": "DeltaS=f(X,labels)L_m",
            "survives_current_constraints": True,
            "why_survives": "normal form is a signature, not a completed corpus inventory",
            "needed_to_kill": "complete parent action inventory with forbid/reclassify/bound decision",
        },
        {
            "countermodel_id": "CM2618_1_post_variation_projector",
            "countermodel": "material projector is applied after Hilbert variation",
            "mathematical_form": "T_active=T_H+epsilon P_label(T_H)",
            "survives_current_constraints": True,
            "why_survives": "identity source-map grammar is not parent-signed",
            "needed_to_kill": "parent action/object-language theorem forbids post-Euler source maps",
        },
        {
            "countermodel_id": "CM2618_2_boundary_material_residual",
            "countermodel": "boundary/domain term carries material data",
            "mathematical_form": "delta S_boundary[labels]/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "boundary silence conditions are not signed",
            "needed_to_kill": "local/falloff boundary theorem or explicit boundary bound",
        },
        {
            "countermodel_id": "CM2618_3_gr_lhs_missing",
            "countermodel": "source side is clean but left-hand operator does not reduce to Einstein operator",
            "mathematical_form": "E_LHS != G_munu + Lambda g_munu + small residual",
            "survives_current_constraints": True,
            "why_survives": "2618 is source-map normal form, not a full GR-limit derivation",
            "needed_to_kill": "derive left-hand GR/EH limit and Newtonian weak-field limit",
        },
        {
            "countermodel_id": "CM2618_4_verdict",
            "countermodel": "normal-form gaps retain source/local-GR residuals",
            "mathematical_form": "delta_w_shadow, boundary residual, nonminimal coefficient, and E_LHS residual remain",
            "survives_current_constraints": True,
            "why_survives": "signature is ready but parent inventory and GR-limit operator are not proven",
            "needed_to_kill": "2619 GR-left-hand/source-normal-form bridge plus source-backed coefficient rows",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def shadow_coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "SCP2618_0_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "coefficient for post-Hilbert source-shadow/projector leakage",
            "mathematical_form": "T_active=T_H+delta_w_shadow J_shadow",
            "units": "dimensionless_or_arena_normalized",
            "status": "MISSING_NORMAL_FORM_ZERO_OR_BOUND",
        },
        {
            "row_id": "SCP2618_1_c_nonminimal",
            "quantity": "c_nonminimal",
            "meaning": "coefficient for direct matter-MTS/geometric nonminimal source terms",
            "mathematical_form": "DeltaS=c_nonminimal f(X,Phi,labels)L_m",
            "units": "operator_dependent",
            "status": "MISSING_OPERATOR_BASIS_AND_BOUND",
        },
        {
            "row_id": "SCP2618_2_c_boundary",
            "quantity": "c_boundary",
            "meaning": "coefficient for material boundary/domain source residual",
            "mathematical_form": "delta S_boundary[labels]/delta e_obs",
            "units": "boundary_operator_dependent",
            "status": "MISSING_BOUNDARY_SILENCE_OR_BOUND",
        },
        {
            "row_id": "SCP2618_3_c_lhs_GR",
            "quantity": "E_LHS_GR_residual",
            "meaning": "left-hand deviation from Einstein operator in local/weak-field limit",
            "mathematical_form": "E_LHS-(G_munu+Lambda g_munu)",
            "units": "curvature_or_operator_units",
            "status": "MISSING_GR_LIMIT_DERIVATION",
        },
        {
            "row_id": "SCP2618_4_R_total_residual",
            "quantity": "R_total_local_source_operator_residual",
            "meaning": "combined local source/operator residual after normal-form split",
            "mathematical_form": "||R_total|| <= U_B(A_shadow+A_boundary+A_nonminimal) + ||E_LHS-G_Lambda||",
            "units": "mixed_operator_units",
            "status": "MISSING_COMPONENT_NORMS_AND_GR_LIMIT",
        },
        {
            "row_id": "SCP2618_5_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "normal-form work remains private and nonclaim",
            "mathematical_form": "claim_allowed=false until parent normal form and GR-limit gates pass",
            "units": "status",
            "status": "NONCLAIM_LOCK",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def gr_bridge_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bridge_id": "GRB2618_0_source_side",
            "bridge_piece": "RHS source identity",
            "status": "CONTRACT_READY_PARENT_UNSIGNED",
            "evidence": "ANF2618_2 and SMG2618_1",
            "remaining_gap": "identity source-map grammar and complete action inventory",
        },
        {
            "bridge_id": "GRB2618_1_lhs_operator",
            "bridge_piece": "Einstein/GR left-hand limit",
            "status": "NOT_DERIVED_HERE",
            "evidence": "SMG2618_3 and SCP2618_3",
            "remaining_gap": "derive E_LHS -> G_munu + Lambda g_munu and weak-field Newton limit",
        },
        {
            "bridge_id": "GRB2618_2_bianchi",
            "bridge_piece": "Bianchi/conservation compatibility",
            "status": "PARTLY_STRUCTURED",
            "evidence": "Noether exchange collapse plus source-shadow trichotomy",
            "remaining_gap": "show final E_LHS is divergence-free or residual-balanced",
        },
        {
            "bridge_id": "GRB2618_3_newton",
            "bridge_piece": "Newtonian weak-field reduction",
            "status": "NOT_CLAIMABLE",
            "evidence": "source normalization only becomes meaningful after GR LHS limit",
            "remaining_gap": "derive Poisson equation and calibrated G from the same normal form",
        },
        {
            "bridge_id": "GRB2618_4_next",
            "bridge_piece": "next GR bridge",
            "status": "GR_LEFT_HAND_AND_NEWTON_LIMIT_IS_NEXT",
            "evidence": "source-map branch is narrowed enough to move to left-hand operator gate",
            "remaining_gap": "build 2619 EH/Einstein operator limit or residual coefficient pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2618_0_parent_normal_form", "complete parent action normal form is signed", "NONCLAIM_THEOREM_GATE", "BLOCKED_COMPLETE_ACTION_INVENTORY_UNSIGNED"),
        ("GATE2618_1_identity_source_map", "T_active equals total Hilbert source with no shadow map", "BLOCKED", "BLOCKED_SOURCE_MAP_OBJECT_LANGUAGE_UNSIGNED"),
        ("GATE2618_2_shadow_terms_classified", "all shadow/nonminimal/boundary/projector terms are zeroed or bounded", "BLOCKED", "BLOCKED_SHADOW_CLASSIFICATION_INCOMPLETE"),
        ("GATE2618_3_gr_lhs_limit", "left-hand operator reduces to Einstein/GR form", "BLOCKED", "BLOCKED_GR_LHS_LIMIT_NOT_DERIVED"),
        ("GATE2618_4_newton_limit", "Newtonian weak-field limit follows", "BLOCKED", "BLOCKED_POISSON_LIMIT_NOT_DERIVED"),
        ("GATE2618_5_local_GR_WEP_R10", "local GR / Newton / WEP / PPN / clock / orbital / R10 source branch passes", "BLOCKED", "BLOCKED_NORMAL_FORM_AND_GR_LHS_GATES_OPEN"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": status,
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2618_0_normal_form_gain",
            "decision": "SOURCE_SHADOW_REDUCED_TO_ACTION_NORMAL_FORM_CLASSIFICATION",
            "reason": "every source-looking term must now declare an owner or become a coefficient row",
            "next_action": "use the normal-form ledger rather than vague coupling language",
        },
        {
            "decision_id": "DEC2618_1_no_promotion",
            "decision": "PARENT_NORMAL_FORM_NOT_CLAIMED",
            "reason": "complete parent action inventory and object-language signature remain unsigned",
            "next_action": "keep local-GR/WEP/R10 gates closed",
        },
        {
            "decision_id": "DEC2618_2_gr_bridge",
            "decision": "MOVE_NEXT_TO_LEFT_HAND_GR_LIMIT",
            "reason": "source-side coupling is narrowed; a GR reduction now needs the left-hand operator limit",
            "next_action": "derive E_LHS to Einstein tensor/Newton limit or stage residual coefficient pack",
        },
        {
            "decision_id": "DEC2618_3_best_next",
            "decision": "GR_LEFT_HAND_EINSTEIN_AND_NEWTON_LIMIT_IS_NEXT",
            "reason": "without the LHS GR limit, a clean RHS source still does not give GR/Newton recovery",
            "next_action": "build 2619 parent-action GR-limit/EH-operator bridge or residual coefficient pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2618_0_primary",
            "status": "selected",
            "doc": "2619-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
            "script": "scripts/Y5_R2FR_GR_left_hand_Einstein_Newton_limit_or_operator_residual_pack_2619.py",
            "task": "derive the parent left-hand operator limit E_LHS -> Einstein tensor plus Newton/Poisson weak-field limit, or stage explicit operator residual coefficients",
            "success_condition": "E_LHS is theorem-reduced to Einstein/Newton form or explicit nonclaim operator residual rows exist",
            "guardrail": "do not claim local GR/Newton until both source normal form and LHS operator limits pass",
        },
        {
            "next_id": "NEXT2618_1_fallback",
            "status": "held_fallback",
            "doc": "2619b-Y5-R2FR-shadow-normal-form-coefficient-source-pack.md",
            "script": "scripts/Y5_R2FR_shadow_normal_form_coefficient_source_pack_2619b.py",
            "task": "fill source-backed coefficient rows for nonminimal, boundary, projector, and shadow residuals if normal-form proof remains unsigned",
            "success_condition": "finite shadow/normal-form residuals can be carried into local tests",
            "guardrail": "no placeholder coefficient is valid_for_claim",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "normal_form": normal_form_rows(),
        "source_map": source_map_gate_rows(),
        "shadow": shadow_classification_rows(),
        "countermodel": countermodel_rows(),
        "coefficients": shadow_coefficient_rows(),
        "gr_bridge": gr_bridge_status_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def copy_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        ok, count, error = csv_parses(target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2618_{key}",
                    "source_key": key,
                    "source_path": source,
                    "copy_path": target,
                    "copy_exists": target.exists(),
                    "csv_parse": ok,
                    "row_count": count,
                    "error": error,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = set(FALSE_FLAGS)
    for key, rows in rows_map.items():
        if key == "sources":
            continue
        for row in rows:
            for field in flag_fields:
                if str(row.get(field, "false")).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(row_value(value) for value in row.values())
            if "MISSING_" not in text:
                continue
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return False
            status = str(row.get("status", row.get("attempt_status", ""))).upper()
            if status in {"READY", "PASS", "VALID_FOR_CLAIM"}:
                return False
    return True


def sources_pass(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(row["source_exists"] and row["needles_present"] for row in rows_map["sources"])


def lineage_complete(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    text = " ".join(row_value(value) for row in rows_map["lineage"] for value in row.values())
    return all(token in text for token in ["2617", "1768", "2614-2617"])


def normal_form_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(row.get("clause_id") == "ANF2618_0_parent_action_partition" for row in rows_map["normal_form"])


def normal_form_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("clause_id") == "ANF2618_6_current_verdict"
        and row.get("status") == "SIGNATURE_READY_PARENT_UNSIGNED"
        for row in rows_map["normal_form"]
    )


def source_map_not_claimable(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("gate_id") == "SMG2618_4_current_verdict" and row.get("status") == "NOT_CLAIMABLE"
        for row in rows_map["source_map"]
    )


def shadow_classification_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("class_id") == "SCL2618_7_verdict"
        and row.get("status") == "CLASSIFICATION_LEDGER_READY_NONCLAIM"
        for row in rows_map["shadow"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("countermodel_id") == "CM2618_4_verdict"
        and str(row.get("survives_current_constraints", "false")).lower() == "true"
        for row in rows_map["countermodel"]
    )


def coefficient_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["coefficients"]
    return any(row.get("row_id") == "SCP2618_0_delta_w_shadow" for row in rows) and all(
        str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows
    )


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("row_id") == "SCP2618_4_R_total_residual" and "U_B" in row.get("mathematical_form", "")
        for row in rows_map["coefficients"]
    )


def gr_bridge_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("bridge_id") == "GRB2618_4_next"
        and row.get("status") == "GR_LEFT_HAND_AND_NEWTON_LIMIT_IS_NEXT"
        for row in rows_map["gr_bridge"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2618_3_best_next"
        and "GR_LEFT_HAND_EINSTEIN" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2618_0_primary"
        and row.get("status") == "selected"
        and "GR-left-hand" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2618*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2618_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2618_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2617 current gate plus 1768 and source-side stack"),
        ("VAL2618_02_normal_form_recorded", normal_form_recorded(rows_map), "parent action normal-form contract recorded"),
        ("VAL2618_03_normal_form_not_promoted", normal_form_not_promoted(rows_map), "normal form remains parent-unsigned/nonclaim"),
        ("VAL2618_04_source_map_not_claimable", source_map_not_claimable(rows_map), "source-map current verdict remains not claimable"),
        ("VAL2618_05_shadow_classification_nonclaim", shadow_classification_nonclaim(rows_map), "shadow classification ledger remains nonclaim"),
        ("VAL2618_06_countermodel_retained", countermodel_retained(rows_map), "normal-form countermodel remains retained"),
        ("VAL2618_07_coefficient_pack_nonclaim", coefficient_pack_nonclaim(rows_map), "shadow/operator coefficient rows remain nonclaim"),
        ("VAL2618_08_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B residual factor retained"),
        ("VAL2618_09_gr_bridge_next", gr_bridge_next(rows_map), "GR left-hand/Newton bridge selected next"),
        ("VAL2618_10_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim"),
        ("VAL2618_11_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2618_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2618_13_formalization_untouched", no_formalization_artifacts(), "no 2618 outputs found under formalization-workbench"),
        ("VAL2618_14_decision_next", decision_next(rows_map), "decision selects GR left-hand/Newton route"),
        ("VAL2618_15_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2618_16_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2618_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": detail,
                    "detail": "",
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2618_CSV_{path.stem}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"CSV parses with {count} rows" if ok else "CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    for key, path in COPY_TARGETS.items():
        ok, count, error = csv_parses(path)
        rows.append(
            with_stamp(
                {
                    "check_id": f"VAL2618_COPY_CSV_{key}",
                    "status": "PASS" if ok else "FAIL",
                    "notes": f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
                    "detail": error,
                    "valid_for_claim": False,
                }
            )
        )

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        with_stamp(
            {
                "check_id": "VAL2618_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2618 parent action normal form selects GR left-hand Einstein/Newton limit next",
                "detail": "",
                "valid_for_claim": False,
            }
        )
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validations: list[dict[str, Any]]) -> str:
    return "\n\n".join(
        [
            "# 2618 Y5 R2FR Parent Action Normal Form And Source-Map Identity Signature Or Shadow Coefficient Pack",
            "## Summary\n"
            "- This checkpoint writes the parent-action normal form needed to stop source-shadow ambiguity.\n"
            "- Every source-looking term now has to declare one owner: left-hand geometry/MTS operator, ordinary Hilbert matter source, boundary/improvement term, forbidden post-variation source map, or explicit bounded residual.\n"
            "- The source-side coupling problem is narrowed enough to pivot to the left-hand GR bridge.\n"
            "- The new bottleneck is deriving `E_LHS -> G_munu + Lambda g_munu` and then the Newton/Poisson weak-field limit.\n"
            "- `delta_w_shadow`, nonminimal coefficients, boundary coefficients, and the left-hand GR residual remain nonclaim rows.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2618_use"]),
            "## Parent Action Normal Form Signature\n" + markdown_table(rows_map["normal_form"], ["clause_id", "normal_form_clause", "mathematical_form", "classification_rule", "status", "remaining_gap"]),
            "## Source Map Identity Gate\n" + markdown_table(rows_map["source_map"], ["gate_id", "gate", "mathematical_form", "would_imply", "status"]),
            "## Shadow Term Classification Ledger\n" + markdown_table(rows_map["shadow"], ["class_id", "term", "mathematical_form", "owner", "status", "next_action"]),
            "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "needed_to_kill"]),
            "## Shadow Coefficient Pack\n" + markdown_table(rows_map["coefficients"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status"]),
            "## GR Bridge Status\n" + markdown_table(rows_map["gr_bridge"], ["bridge_id", "bridge_piece", "status", "evidence", "remaining_gap"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
            "## Working Verdict\n"
            "This is the pivot we wanted. The source-side coupling is no longer allowed to be hand-wavy: every source-looking term needs an owner or a coefficient. But a clean RHS still does not recover GR. The next serious derivation target is the left-hand operator: Einstein tensor first, Newton/Poisson second.",
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["normal_form"], rows_map["normal_form"])
    write_csv(OUTPUTS["source_map_gate"], rows_map["source_map"])
    write_csv(OUTPUTS["shadow_classification"], rows_map["shadow"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["shadow_coefficient"], rows_map["coefficients"])
    write_csv(OUTPUTS["gr_bridge_status"], rows_map["gr_bridge"])
    write_csv(OUTPUTS["claim_gates"], rows_map["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], rows_map["decisions"])
    write_csv(OUTPUTS["next_target"], rows_map["next"])
    rows_map["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_map["branch_copies"])
    validations = validation_rows(rows_map)
    write_csv(OUTPUTS["validation"], validations)
    DOC.write_text(build_markdown(rows_map, validations), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"2618 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
