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

BRANCH_ID = "MTS_R2FR_SINGLE_SOURCE_MAP_GATE_2617"
CHECKPOINT_ID = "2617"

DOC = ROOT / "2617-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_LINEAGE_LEDGER.csv",
    "source_map_identity": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
    "shadow_zero": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
    "nonhilbert_audit": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
    "countermodel": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_COUNTERMODEL_LEDGER.csv",
    "shadow_bound": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_DELTAW_SHADOW_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2617_VALIDATION.csv",
}

COPY_TARGETS = {
    "source_map_identity": LOCAL_BOUNDS / "Single_source_map_identity_theorem_2617_NONCLAIM.csv",
    "shadow_bound": LOCAL_BOUNDS / "Deltaw_shadow_bound_interface_2617_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Single_source_map_source_zero_status_2617_NONCLAIM.csv",
    "next_target": QUEUE / "JR2617_PARENT_ACTION_NORMAL_FORM_NEXT.csv",
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
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


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
            "source_id": "SRC2617_00_2616_handoff_doc",
            "source_key": "2616_single_source_map_next",
            "source_path": ROOT / "2616-Y5-R2FR-ordinary-matter-exchange-graph-connectivity-and-source-shadow-ban-or-deltaw-block-bound.md",
            "needles": ["NEXT2616_0_primary", "SINGLE_SOURCE_MAP_GRAMMAR_AND_SHADOW_BAN_IS_NEXT", "VAL2616_OVERALL"],
            "role": "current 26xx handoff selecting single-source-map grammar",
        },
        {
            "source_id": "SRC2617_01_2616_shadow_attempt",
            "source_key": "2616_source_shadow_attempt",
            "source_path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv",
            "needles": ["SSB2616_1_variational_owner_filter", "SSB2616_5_current_verdict"],
            "role": "current source-shadow route and unsigned parent grammar",
        },
        {
            "source_id": "SRC2617_02_2616_countermodel",
            "source_key": "2616_countermodel",
            "source_path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_COUNTERMODEL_LEDGER.csv",
            "needles": ["CM2616_1_source_shadow", "CM2616_2_hidden_projector", "CM2616_4_nonHilbert_label_current"],
            "role": "current source-shadow/projector/non-Hilbert countermodels",
        },
        {
            "source_id": "SRC2617_03_2616_residual",
            "source_key": "2616_residual_interface",
            "source_path": OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_RESIDUAL_BOUND_INTERFACE.csv",
            "needles": ["RBI2616_1_delta_w_shadow", "MISSING_SOURCE_SHADOW_BAN_OR_BOUND"],
            "role": "current delta_w_shadow residual interface",
        },
        {
            "source_id": "SRC2617_04_1767_doc",
            "source_key": "1767_prior_single_source_map_doc",
            "source_path": ROOT / "1767-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
            "needles": ["SMI1767_1_identity_source_map", "DEC1767_3_best_next", "VAL1767_OVERALL"],
            "role": "prior single-source-map checkpoint used as lineage evidence",
        },
        {
            "source_id": "SRC2617_05_1767_source_map",
            "source_key": "1767_source_map_identity",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1767_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv",
            "needles": ["SMI1767_1_identity_source_map", "SMI1767_5_current_verdict"],
            "role": "prior identity source-map theorem and parent unsigned verdict",
        },
        {
            "source_id": "SRC2617_06_1767_shadow_zero",
            "source_key": "1767_shadow_zero_attempt",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1767_SOURCE_SHADOW_ZERO_ATTEMPT.csv",
            "needles": ["SSZ1767_3_shadow_as_projector", "SSZ1767_4_current_verdict"],
            "role": "prior source-shadow zero attempt and projector obstruction",
        },
        {
            "source_id": "SRC2617_07_1767_nonhilbert",
            "source_key": "1767_nonhilbert_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1767_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
            "needles": ["NHB1767_4_post_variation_projector", "NHB1767_5_verdict"],
            "role": "prior non-Hilbert/boundary/projector inventory",
        },
        {
            "source_id": "SRC2617_08_1767_shadow_bound",
            "source_key": "1767_shadow_bound_interface",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1767_DELTAW_SHADOW_BOUND_INTERFACE.csv",
            "needles": ["DSH1767_0_delta_w_shadow", "DSH1767_4_nonclaim_lock"],
            "role": "prior shadow residual bound interface",
        },
        {
            "source_id": "SRC2617_09_954_parent_action",
            "source_key": "954_parent_action_clause",
            "source_path": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needles": ["PAC954_2_total_Hilbert_derivative", "PAC954_3_no_hidden_spurion_return", "PAC954_4_nonHilbert_current_split"],
            "role": "parent action clauses for Hilbert source and shadow bypasses",
        },
        {
            "source_id": "SRC2617_10_955_same_action",
            "source_key": "955_same_action_principle",
            "source_path": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needles": ["MMA955_1_same_action_principle", "MMA955_6_verdict"],
            "role": "same-action principle and parent unsigned minimal matter verdict",
        },
        {
            "source_id": "SRC2617_11_977_constant_certificate",
            "source_key": "977_constant_source_certificate",
            "source_path": OUT / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
            "needles": ["CSC977_4_single_universal_kappa", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
            "role": "constant-source certificate and guardrail against source overclaim",
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
            "lineage_id": "LIN2617_0_current_parent",
            "input_checkpoint": "2616",
            "input_artifact": "P8_Y5_EXCHANGE_GRAPH_GATE_2616_*",
            "imported_result": "ordinary graph conditionally closes block residual; source-shadow/projector route remains strongest bypass",
            "2617_use": "classify source-shadow as action term, boundary/improvement, or nonvariational residual",
        },
        {
            "lineage_id": "LIN2617_1_prior_source_map",
            "input_checkpoint": "1767",
            "input_artifact": "P8_Y5_PARENT_QLOC_1767_*",
            "imported_result": "identity-only source map theorem is clean but parent normal form unsigned",
            "2617_use": "port the trichotomy into current 26xx chain",
        },
        {
            "lineage_id": "LIN2617_2_parent_action_signature",
            "input_checkpoint": "954/955/977",
            "input_artifact": "parent action and constant source certificates",
            "imported_result": "same-action source owner is contract-ready but needs full normal form",
            "2617_use": "select parent action normal-form signature next",
        },
        {
            "lineage_id": "LIN2617_3_residual_interface",
            "input_checkpoint": "2616/1767",
            "input_artifact": "delta_w_shadow residual rows",
            "imported_result": "shadow residual requires basis, arena projection, source-backed bound or theorem-zero",
            "2617_use": "retain delta_w_shadow nonclaim interface",
        },
        {
            "lineage_id": "LIN2617_4_claim_policy",
            "input_checkpoint": "all",
            "input_artifact": "claim gates and validation ledgers",
            "imported_result": "no local-GR/Newton/WEP/PPN/clock/orbital/R10 claim while shadow route is retained",
            "2617_use": "keep all claim flags false",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_map_identity_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "SMI2617_0_variational_setup",
            "claim_piece": "single parent variational source owner",
            "mathematical_form": "S_parent=S_geom[Phi,e_obs]+S_matter[Psi,e_obs,theta]; delta S_parent/delta e_obs=0",
            "status": "SETUP_EXACT",
            "theorem_result": "ordinary source entering the field equation is the Euler/Hilbert derivative of S_matter",
            "remaining_gap": "parent action normal form not yet signed for every ordinary source channel",
        },
        {
            "theorem_id": "SMI2617_1_identity_source_map",
            "claim_piece": "identity-only source map",
            "mathematical_form": "T_active := T_H := delta S_matter/delta e_obs; no independent F_shadow(T_H,labels)",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "theorem_result": "if the field equation is the Euler equation of the same action, a post-variation material source map is not an independent operation",
            "remaining_gap": "must prove no extra source map/projector is admitted by the parent object language",
        },
        {
            "theorem_id": "SMI2617_2_shadow_trichotomy",
            "claim_piece": "source-shadow classification",
            "mathematical_form": "J_shadow is either Euler variation of a real action term, a boundary/improvement term, or nonvariational",
            "status": "TRICHOTOMY_DERIVED",
            "theorem_result": "a shadow source cannot be a harmless hidden RHS knob: it is geometry/matter action content, boundary silence, or inconsistency/bound",
            "remaining_gap": "must classify allowed MTS shadow candidates in parent action normal form",
        },
        {
            "theorem_id": "SMI2617_3_bianchi_filter",
            "claim_piece": "nonvariational shadow rejection",
            "mathematical_form": "nabla_mu E^{mu nu}=0 requires nabla_mu(T_H^{mu nu}+J_shadow^{mu nu})=0",
            "status": "DERIVED_FILTER",
            "theorem_result": "uncoupled nonvariational shadow source either violates Bianchi/Noether identity or is a separately conserved real block",
            "remaining_gap": "separately conserved real blocks need arena exclusion or finite bound",
        },
        {
            "theorem_id": "SMI2617_4_boundary_improvement_limit",
            "claim_piece": "boundary/improvement source silence",
            "mathematical_form": "J_shadow = nabla_alpha U^{alpha mu nu} or delta S_boundary/delta e_obs",
            "status": "CONDITIONAL_SILENCE",
            "theorem_result": "boundary/improvement terms do not generate a bulk composition source if falloff/local boundary conditions silence them",
            "remaining_gap": "falloff/local boundary silence still has to be parent or arena signed",
        },
        {
            "theorem_id": "SMI2617_5_current_verdict",
            "claim_piece": "current MTS source-shadow zero",
            "mathematical_form": "delta_w_shadow=0 iff identity source map + no non-Hilbert/projector/boundary shadow + no decoupled block",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "theorem_result": "source-shadow squeezed into action-normal-form and boundary/projector debts, but not eliminated",
            "remaining_gap": "parent normal form and shadow candidate classification remain unsigned",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def shadow_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "zero_id": "SSZ2617_0_target",
            "claim_piece": "delta_w_shadow zero",
            "mathematical_form": "T_active=T_H and J_shadow=0",
            "status": "TARGET_EXACT",
            "derivation_result": "closes strongest remaining source-coupling bypass if parent-signed",
            "remaining_gap": "identity source-map grammar not yet signed by parent action",
        },
        {
            "zero_id": "SSZ2617_1_shadow_as_action_term",
            "claim_piece": "variational shadow is real parent content",
            "mathematical_form": "J_shadow=delta DeltaS/delta e_obs",
            "status": "DERIVED_RECLASSIFICATION",
            "derivation_result": "not a hidden RHS knob; it must be listed as matter, geometry, nonminimal coupling, or boundary content",
            "remaining_gap": "requires parent action normal-form ledger to classify every DeltaS",
        },
        {
            "zero_id": "SSZ2617_2_shadow_as_nonvariational",
            "claim_piece": "nonvariational source-shadow",
            "mathematical_form": "J_shadow inserted into field equation without DeltaS",
            "status": "DERIVED_REJECTION_OR_BOUND",
            "derivation_result": "inconsistent with action/Bianchi unless separately conserved and therefore a real residual block to bound",
            "remaining_gap": "separately conserved residuals need source inventory and bounds",
        },
        {
            "zero_id": "SSZ2617_3_shadow_as_projector",
            "claim_piece": "post-variation source projector",
            "mathematical_form": "T_active=P_material(T_H)",
            "status": "CONTRACT_NEEDED",
            "derivation_result": "unless P_material=identity or comes from an action term, it is a source-shadow operation",
            "remaining_gap": "identity-only source-map theorem remains parent-unsigned",
        },
        {
            "zero_id": "SSZ2617_4_current_verdict",
            "claim_piece": "current source-shadow zero theorem",
            "mathematical_form": "delta_w_shadow=0",
            "status": "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF",
            "derivation_result": "shadow routes are now classified and sharply bounded by action normal form, but not parent-eliminated",
            "remaining_gap": "must build parent action normal-form/source-map signature or retain finite shadow coefficient",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def nonhilbert_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "NHB2617_0_boundary_improvement",
            "channel": "boundary/improvement current",
            "mathematical_form": "J_boundary=nabla_alpha U^{alpha mu nu} or delta S_boundary/delta e_obs",
            "status": "MISSING_BOUNDARY_SILENCE_OR_RECLASSIFICATION",
            "why_live": "can look like source if boundary/falloff is not controlled",
            "needed_to_kill": "boundary silence theorem or explicit boundary residual bound",
        },
        {
            "audit_id": "NHB2617_1_spin_torsion_current",
            "channel": "spin/torsion/non-Hilbert current",
            "mathematical_form": "J_spin or J_torsion added outside T_H",
            "status": "MISSING_ABSENCE_OR_RECLASSIFICATION",
            "why_live": "could carry material labels if torsion/connection are active source variables",
            "needed_to_kill": "show absent, pure improvement, or left-hand geometry term; otherwise bound",
        },
        {
            "audit_id": "NHB2617_2_decoupled_conserved_block",
            "channel": "separately conserved real block",
            "mathematical_form": "nabla_mu J_dec^{mu nu}=0, T_active=T_H+epsilon J_dec",
            "status": "MISSING_ARENA_EXCLUSION_OR_BOUND",
            "why_live": "Bianchi permits real conserved blocks",
            "needed_to_kill": "arena inventory excluding it from ordinary tests or finite bound",
        },
        {
            "audit_id": "NHB2617_3_nonminimal_coupling",
            "channel": "nonminimal matter-geometry coupling",
            "mathematical_form": "DeltaS=f(X,labels) R L_m or A(X) J_m",
            "status": "MISSING_NORMAL_FORM_CLASSIFICATION",
            "why_live": "changes the parent action and must be classified as LHS geometry, matter dynamics, or residual",
            "needed_to_kill": "parent action ledger must either forbid or parameterize it",
        },
        {
            "audit_id": "NHB2617_4_post_variation_projector",
            "channel": "post-variation material/source projector",
            "mathematical_form": "P_material(T_H)-T_H",
            "status": "MISSING_IDENTITY_PROOF_OR_BOUND",
            "why_live": "most direct remaining way to fake composition dependence after a clean Hilbert source",
            "needed_to_kill": "prove P_material=identity in parent grammar or bound coefficient",
        },
        {
            "audit_id": "NHB2617_5_verdict",
            "channel": "non-Hilbert/source-shadow inventory",
            "mathematical_form": "J_shadow=J_spin+J_boundary+J_nonminimal+J_projector+J_decoupled",
            "status": "INVENTORY_READY_NONCLAIM",
            "why_live": "all shadow channels are named and must be zeroed or bounded",
            "needed_to_kill": "2618 normal-form signature or coefficient pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "countermodel_id": "CM2617_0_variational_shadow_action",
            "countermodel": "extra action term produces source-like variation",
            "mathematical_form": "DeltaS_shadow[e_obs,Psi,X] with J_shadow=delta DeltaS_shadow/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "current parent corpus has not listed and excluded all nonminimal/source-shadow action terms",
            "needed_to_kill": "parent action normal form classifies every DeltaS as geometry, standard matter, boundary-silent, or forbidden",
        },
        {
            "countermodel_id": "CM2617_1_post_variation_projector",
            "countermodel": "source map applied after Hilbert variation",
            "mathematical_form": "T_active=T_H+epsilon P_label(T_H)",
            "survives_current_constraints": True,
            "why_survives": "identity-only source-map grammar is not parent-signed",
            "needed_to_kill": "prove field equation is purely Euler-Lagrange with no post-processing source map",
        },
        {
            "countermodel_id": "CM2617_2_conserved_shadow_block",
            "countermodel": "separately conserved shadow block",
            "mathematical_form": "nabla_mu J_shadow^{mu nu}=0 and T_active=T_H+epsilon J_shadow",
            "survives_current_constraints": True,
            "why_survives": "Bianchi alone allows a conserved independent block",
            "needed_to_kill": "arena exclusion, parent absence theorem, or finite empirical bound",
        },
        {
            "countermodel_id": "CM2617_3_boundary_material_term",
            "countermodel": "boundary/domain term carries material data",
            "mathematical_form": "delta S_boundary[material labels]/delta e_obs",
            "survives_current_constraints": True,
            "why_survives": "boundary silence/falloff is not yet signed for every local arena",
            "needed_to_kill": "boundary condition proof or explicit boundary residual bound",
        },
        {
            "countermodel_id": "CM2617_4_verdict",
            "countermodel": "source-shadow residual retained",
            "mathematical_form": "T_active=T_H + delta_w_shadow J_shadow",
            "survives_current_constraints": True,
            "why_survives": "2617 classifies the loophole but does not parent-sign the normal-form exclusion",
            "needed_to_kill": "2618 parent action normal-form/source-map identity signature or finite shadow bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def shadow_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DSH2617_0_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "meaning": "coefficient multiplying any source-shadow/non-Hilbert/projector residual",
            "mathematical_form": "T_active=T_H + delta_w_shadow J_shadow",
            "units": "dimensionless_or_arena_normalized",
            "status": "MISSING_PARENT_NORMAL_FORM_OR_NUMERIC_BOUND",
        },
        {
            "row_id": "DSH2617_1_shadow_basis",
            "quantity": "J_shadow basis",
            "meaning": "basis of possible shadow currents after Hilbert variation",
            "mathematical_form": "J_shadow in {spin/torsion, boundary, nonminimal, projector, decoupled}",
            "units": "basis",
            "status": "MISSING_SHADOW_BASIS_SOURCE_PATHS",
        },
        {
            "row_id": "DSH2617_2_projection",
            "quantity": "shadow-to-observable projection",
            "meaning": "map shadow source coefficient to WEP/R10/PPN/clock/orbital residual",
            "mathematical_form": "observable_residual = P_arena[J_shadow] delta_w_shadow",
            "units": "arena-specific",
            "status": "MISSING_ARENA_PROJECTION",
        },
        {
            "row_id": "DSH2617_3_R_source_shadow",
            "quantity": "R_source_shadow",
            "meaning": "shadow contribution to ordinary active-source residual",
            "mathematical_form": "||R_source,shadow||_{E*} <= U_B A_shadow",
            "units": "E*_dual_or_declared_arena_units",
            "status": "MISSING_A_SHADOW_AND_ARENA_UNITS",
        },
        {
            "row_id": "DSH2617_4_bound_table",
            "quantity": "delta_w_shadow_bound",
            "meaning": "finite empirical upper bound if zero theorem fails",
            "mathematical_form": "|delta_w_shadow| <= bound",
            "units": "dimensionless_or_arena_normalized",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
        },
        {
            "row_id": "DSH2617_5_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "source-shadow route remains blocked",
            "mathematical_form": "claim_allowed=false until normal-form zero or finite bound closes",
            "units": "status",
            "status": "NONCLAIM_LOCK",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "SZ2617_0_identity_map",
            "quantity": "single source-map identity",
            "current_status": "CONDITIONAL_THEOREM_READY",
            "evidence": "SMI2617_1",
            "remaining_gap": "parent action normal form must sign identity-only source map",
        },
        {
            "status_id": "SZ2617_1_shadow_inventory",
            "quantity": "source-shadow inventory",
            "current_status": "CLASSIFIED_NOT_ZEROED",
            "evidence": "SMI2617_2 and NHB2617_5",
            "remaining_gap": "each candidate must be forbidden, reclassified, boundary-silenced, or bounded",
        },
        {
            "status_id": "SZ2617_2_delta_w_shadow",
            "quantity": "delta_w_shadow",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "SSZ2617_4 and DSH2617_0",
            "remaining_gap": "normal-form proof or finite bound missing",
        },
        {
            "status_id": "SZ2617_3_local_GR",
            "quantity": "local GR / Newton / WEP / R10 / PPN / clock / orbital branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "source-shadow residual retained",
            "remaining_gap": "no local pass until normal-form source side is theorem-zero or finite bounded",
        },
        {
            "status_id": "SZ2617_4_next",
            "quantity": "next derivation owner",
            "current_status": "PARENT_ACTION_NORMAL_FORM_IS_NEXT",
            "evidence": "all shadow candidates reduce to action-normal-form classification",
            "remaining_gap": "build 2618 normal-form signature or shadow coefficient pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2617_0_identity_source_map",
            "claim": "active ordinary source is exactly total Hilbert source",
            "gate_pass": False,
            "status": "NONCLAIM_THEOREM_GATE",
            "blocker": "BLOCKED_PARENT_ACTION_NORMAL_FORM_UNSIGNED",
        },
        {
            "gate_id": "GATE2617_1_no_post_variation_projector",
            "claim": "no post-variation material source projector",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_IDENTITY_ONLY_SOURCE_MAP_GRAMMAR_UNSIGNED",
        },
        {
            "gate_id": "GATE2617_2_no_nonhilbert_shadow",
            "claim": "no non-Hilbert/boundary/nonminimal shadow source remains",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_INVENTORY_NOT_CLASSIFIED",
        },
        {
            "gate_id": "GATE2617_3_delta_w_shadow_zero",
            "claim": "delta_w_shadow=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SHADOW_COUNTERMODELS_RETAINED",
        },
        {
            "gate_id": "GATE2617_4_delta_w_shadow_bound",
            "claim": "delta_w_shadow finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHADOW_BASIS_PROJECTION_BOUND_TABLE_MISSING",
        },
        {
            "gate_id": "GATE2617_5_local_GR_WEP_R10",
            "claim": "local GR / Newton / WEP / PPN / clock / orbital / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_SHADOW_RETAINED",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2617_0_identity_gain",
            "decision": "SOURCE_SHADOW_IS_NOT_A_FREE_COUPLING_IF_ACTION_VARIATIONAL",
            "reason": "a post-Hilbert source term must be an action term, boundary/improvement, nonvariational inconsistency, or conserved residual block",
            "next_action": "stop treating shadow as vague coupling; classify every candidate in the parent action normal form",
        },
        {
            "decision_id": "DEC2617_1_no_promotion",
            "decision": "DELTA_W_SHADOW_NOT_ZEROED",
            "reason": "identity-only source-map grammar and boundary/projector silence are not parent-signed",
            "next_action": "retain delta_w_shadow as nonclaim residual",
        },
        {
            "decision_id": "DEC2617_2_residual_interface",
            "decision": "SHADOW_BOUND_INTERFACE_STAGED",
            "reason": "if normal-form proof fails, shadow current needs a basis, projection, and bound table",
            "next_action": "do not fill numeric bounds without source-backed arena rows",
        },
        {
            "decision_id": "DEC2617_3_best_next",
            "decision": "PARENT_ACTION_NORMAL_FORM_AND_SOURCE_MAP_SIGNATURE_IS_NEXT",
            "reason": "all remaining shadow routes reduce to whether the parent action admits them and where they live",
            "next_action": "build 2618 parent action normal-form/source-map identity signature or shadow coefficient pack",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2617_0_primary",
            "status": "selected",
            "doc": "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_parent_action_normal_form_and_source_map_identity_signature_or_shadow_coefficient_pack_2618.py",
            "task": "write the parent action normal form that classifies every source-like term as geometry, Hilbert matter, boundary-silent, forbidden, or bounded shadow residual",
            "success_condition": "every source-like term has a legal owner or explicit finite residual",
            "guardrail": "no local-GR, Newton, WEP, PPN, clock, orbital or R10 claim from 2617",
        },
        {
            "next_id": "NEXT2617_1_fallback",
            "status": "held_fallback",
            "doc": "2618b-Y5-R2FR-deltaw-shadow-basis-projection-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_shadow_basis_projection_bound_pack_2618b.py",
            "task": "stage source-backed shadow-current basis rows, observable projections, and local bound inputs if normal-form proof remains unsigned",
            "success_condition": "finite shadow residual can be carried into local tests as nonclaim plumbing",
            "guardrail": "no placeholder bound can be valid_for_claim",
        },
        {
            "next_id": "NEXT2617_2_graph_sourcing_parallel",
            "status": "queued_parallel",
            "doc": "2618c-Y5-R2FR-standard-matter-graph-source-certificate-and-arena-inventory.md",
            "script": "scripts/Y5_R2FR_standard_matter_graph_source_certificate_and_arena_inventory_2618c.py",
            "task": "source ordinary matter graph edges and arena inventory after source-map grammar is sorted",
            "success_condition": "graph rows cite source-backed components and binding terms",
            "guardrail": "graph sourcing does not close shadow normal-form debt by itself",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "source_map": source_map_identity_rows(),
        "shadow_zero": shadow_zero_rows(),
        "nonhilbert": nonhilbert_audit_rows(),
        "countermodel": countermodel_rows(),
        "shadow_bound": shadow_bound_rows(),
        "source_zero": source_zero_rows(),
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
                    "copy_id": f"COPY2617_{key}",
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
    return all(token in text for token in ["2616", "1767", "954/955/977"])


def identity_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "SMI2617_1_identity_source_map"
        and row.get("status") == "DERIVED_CONDITIONAL_THEOREM"
        for row in rows_map["source_map"]
    )


def trichotomy_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("theorem_id") == "SMI2617_2_shadow_trichotomy"
        and row.get("status") == "TRICHOTOMY_DERIVED"
        for row in rows_map["source_map"]
    )


def shadow_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("zero_id") == "SSZ2617_4_current_verdict"
        and row.get("status") == "PARTIAL_THEOREM_NOT_FULL_PARENT_PROOF"
        for row in rows_map["shadow_zero"]
    )


def inventory_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("audit_id") == "NHB2617_5_verdict"
        and row.get("status") == "INVENTORY_READY_NONCLAIM"
        for row in rows_map["nonhilbert"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("countermodel_id") == "CM2617_4_verdict"
        and str(row.get("survives_current_constraints", "false")).lower() == "true"
        for row in rows_map["countermodel"]
    )


def shadow_bound_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["shadow_bound"]
    return any(row.get("row_id") == "DSH2617_0_delta_w_shadow" for row in rows) and all(
        str(row.get("valid_for_claim", "false")).lower() == "false" for row in rows
    )


def ub_power_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("row_id") == "DSH2617_3_R_source_shadow" and "U_B" in row.get("mathematical_form", "")
        for row in rows_map["shadow_bound"]
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("status_id") == "SZ2617_3_local_GR" and row.get("current_status") == "NOT_CLAIMABLE"
        for row in rows_map["source_zero"]
    )


def claim_gates_safe(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return all(str(row.get("gate_pass", "false")).lower() == "false" for row in rows_map["claim_gates"])


def decision_next(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("decision_id") == "DEC2617_3_best_next"
        and "PARENT_ACTION_NORMAL_FORM" in row.get("decision", "")
        for row in rows_map["decisions"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row.get("next_id") == "NEXT2617_0_primary"
        and row.get("status") == "selected"
        and "parent-action-normal-form" in row.get("doc", "")
        for row in rows_map["next"]
    )


def no_formalization_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*2617*"))


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def validation_rows(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL2617_00_sources_exist", sources_pass(rows_map), "all cited source paths exist and needles are present"),
        ("VAL2617_01_lineage_complete", lineage_complete(rows_map), "lineage covers 2616 current gate plus 1767 and 954/955/977 prior inputs"),
        ("VAL2617_02_identity_theorem", identity_theorem_recorded(rows_map), "identity source-map theorem recorded"),
        ("VAL2617_03_shadow_trichotomy", trichotomy_recorded(rows_map), "shadow trichotomy recorded"),
        ("VAL2617_04_shadow_not_promoted", shadow_not_promoted(rows_map), "source-shadow zero remains unpromoted"),
        ("VAL2617_05_shadow_inventory_nonclaim", inventory_nonclaim(rows_map), "shadow inventory remains nonclaim"),
        ("VAL2617_06_countermodel_retained", countermodel_retained(rows_map), "source-shadow countermodel remains retained"),
        ("VAL2617_07_shadow_bound_nonclaim", shadow_bound_nonclaim(rows_map), "delta_w_shadow interface rows remain nonclaim"),
        ("VAL2617_08_U_B_power_retained", ub_power_retained(rows_map), "explicit U_B shadow-source residual factor retained"),
        ("VAL2617_09_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked"),
        ("VAL2617_10_claim_gates_safe", claim_gates_safe(rows_map), "all claim gates remain blocked/nonclaim"),
        ("VAL2617_11_no_claim_flags", generated_rows_have_no_claim_flags(rows_map), "claim/no-score flags stay false"),
        ("VAL2617_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        ("VAL2617_13_formalization_untouched", no_formalization_artifacts(), "no 2617 outputs found under formalization-workbench"),
        ("VAL2617_14_decision_next", decision_next(rows_map), "decision selects parent action normal-form route"),
        ("VAL2617_15_next_selected", next_selected(rows_map), "next target selected"),
        (
            "VAL2617_16_branch_copies",
            all(row["copy_exists"] and row["csv_parse"] for row in rows_map["branch_copies"]),
            "nonclaim branch copies exist and parse",
        ),
        ("VAL2617_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent"),
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
                    "check_id": f"VAL2617_CSV_{path.stem}",
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
                    "check_id": f"VAL2617_COPY_CSV_{key}",
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
                "check_id": "VAL2617_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "notes": "2617 source-shadow trichotomy selects parent action normal-form signature next",
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
            "# 2617 Y5 R2FR Single Source-Map Grammar And Source-Shadow Ban Or Shadow Bound",
            "## Summary\n"
            "- This checkpoint turns the source-shadow loophole into an action-normal-form problem.\n"
            "- If the parent field equation is the Euler-Lagrange equation of one parent action and ordinary matter enters through `S_matter`, the active ordinary source is the Hilbert/coframe derivative `T_H=delta S_matter/delta e_obs`.\n"
            "- Any `J_shadow` must be one of three things: an Euler variation of a real action term, a boundary/improvement term, or a nonvariational/conserved residual that must be excluded or bounded.\n"
            "- Current MTS still lacks the parent action normal form that classifies every source-like term as geometry, Hilbert matter, boundary-silent, forbidden, or bounded shadow residual.\n"
            "- `delta_w_shadow` remains a nonclaim residual with an explicit bound interface.",
            "## Source Register\n" + markdown_table(rows_map["sources"], ["source_id", "source_key", "source_path", "source_exists", "needles_present"]),
            "## Lineage Ledger\n" + markdown_table(rows_map["lineage"], ["lineage_id", "input_checkpoint", "imported_result", "2617_use"]),
            "## Single Source-Map Identity Theorem\n" + markdown_table(rows_map["source_map"], ["theorem_id", "claim_piece", "mathematical_form", "status", "theorem_result", "remaining_gap"]),
            "## Source-Shadow Zero Attempt\n" + markdown_table(rows_map["shadow_zero"], ["zero_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap"]),
            "## Non-Hilbert Boundary Projector Audit\n" + markdown_table(rows_map["nonhilbert"], ["audit_id", "channel", "mathematical_form", "status", "why_live", "needed_to_kill"]),
            "## Countermodel Ledger\n" + markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "needed_to_kill"]),
            "## Delta-W Shadow Bound Interface\n" + markdown_table(rows_map["shadow_bound"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status"]),
            "## Source Zero Status\n" + markdown_table(rows_map["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
            "## Claim Gates\n" + markdown_table(rows_map["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
            "## Decision Ledger\n" + markdown_table(rows_map["decisions"], ["decision_id", "decision", "reason", "next_action"]),
            "## Next Target\n" + markdown_table(rows_map["next"], ["next_id", "status", "doc", "script", "task", "success_condition", "guardrail"]),
            "## Branch Copies\n" + markdown_table(rows_map["branch_copies"], ["copy_id", "source_key", "copy_path", "copy_exists", "csv_parse", "row_count"]),
            "## Validation\n" + markdown_table(validations, ["check_id", "status", "notes", "detail", "valid_for_claim"]),
            "## Working Verdict\n"
            "The coupling branch is getting less foggy. A shadow source is not magic dust on the right-hand side. Either it comes from the parent action, in which case it must be written and owned, or it is a boundary/improvement term, or it is a nonvariational conserved residual that has to be bounded. The next useful checkpoint is the parent action normal form.",
        ]
    ) + "\n"


def main() -> None:
    rows_map = rows_by_key()
    write_csv(OUTPUTS["source_register"], rows_map["sources"])
    write_csv(OUTPUTS["lineage_ledger"], rows_map["lineage"])
    write_csv(OUTPUTS["source_map_identity"], rows_map["source_map"])
    write_csv(OUTPUTS["shadow_zero"], rows_map["shadow_zero"])
    write_csv(OUTPUTS["nonhilbert_audit"], rows_map["nonhilbert"])
    write_csv(OUTPUTS["countermodel"], rows_map["countermodel"])
    write_csv(OUTPUTS["shadow_bound"], rows_map["shadow_bound"])
    write_csv(OUTPUTS["source_zero"], rows_map["source_zero"])
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
    print(f"2617 validation {validations[-1]['status']}")


if __name__ == "__main__":
    main()
