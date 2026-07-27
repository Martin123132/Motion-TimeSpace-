from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1620"
INPUT_1620 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md"

SOURCE_FILES = {
    "1619_doc": ROOT / "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md",
    "1619_validation": OUT / "P8_Y5_BRR545_1619_VALIDATION.csv",
    "1619_next": OUT / "P8_Y5_PARENT_QLOC_1619_NEXT_TARGET.csv",
    "1619_normal": OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
    "1619_gaps": OUT / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv",
    "1619_profile": OUT / "P8_Y5_PARENT_QLOC_1619_QLOC_PROFILE_ROW.csv",
    "1574_premise": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_DESCENT_PREMISE_MATRIX.csv",
    "1574_charge": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT.csv",
    "1575_vertical": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
    "1575_descent": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
    "1576_qmap": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv",
    "1505_ledger": OUT / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
    "1505_tests": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
    "1415_owner": OUT / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1416_ban": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
    "1086_source_current": OUT / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
    "992_descent": OUT / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
}

NEEDLES = {
    "1619_doc": ["FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED", "VAL1619_OVERALL"],
    "1619_validation": ["VAL1619_OVERALL", "PASS"],
    "1619_next": ["1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md", "source-current zero"],
    "1619_normal": ["NF1619_6_verdict", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "1619_gaps": ["GAP1619_7_verdict", "PARENT_SIGNATURE_OPEN_NO_PROMOTION"],
    "1619_profile": ["QPR1619_0_normal_form_profile", "MISSING_PARENT_SIGNATURE"],
    "1574_premise": ["RPM1574_5_verdict", "FAIL_CURRENT_CLAIM"],
    "1574_charge": ["RMC1574_1_chain_rule", "EXACT_CONDITIONAL_CHAIN_RULE"],
    "1575_vertical": ["VERT1575_5_verdict", "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED"],
    "1575_descent": ["MDS1575_5_verdict", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1576_qmap": ["QMAP1576_2_constraint_first", "POSSIBLE_IF_CONSTRAINT_SIGNED"],
    "1505_ledger": ["THM1505_0_vertical_residual_safe", "EXACT_CONDITIONAL_THEOREM"],
    "1505_tests": ["DQT1505_8_acceptance", "BLOCKED"],
    "1415_owner": ["SCO1415_6_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED"],
    "1416_ban": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
    "1086_source_current": ["SCZ1086_5_verdict", "SOURCE_CURRENT_ZERO_NOT_DERIVED"],
    "992_descent": ["SCD992_4_charge_current_equality", "failed_current_corpus"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1620_SOURCE_REGISTER.csv"
BRIDGE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv"
CHAIN_RULE = OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv"
VERTICALITY_MAP = OUT / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv"
BOUND_ROWS = OUT / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1620_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1620_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1620_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1620_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1620_VALIDATION.csv"

COPY_TARGETS = {
    BRIDGE_CONTRACT: [
        QUARANTINE / "PARENT_SIGNATURE_BRIDGE_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_signature_bridge_contract_nonclaim_1620.csv",
    ],
    CHAIN_RULE: [
        QUARANTINE / "CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_chain_rule_source_current_zero_attempt_1620.csv",
    ],
    VERTICALITY_MAP: [
        QUARANTINE / "QUOTIENT_VERTICALITY_MAP_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_quotient_verticality_map_audit_1620.csv",
    ],
    BOUND_ROWS: [
        QUARANTINE / "SOURCE_CURRENT_BOUND_FILL_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_current_bound_fill_rows_nonclaim_1620.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1620.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1620.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1620_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1620_parent_signature_source_current_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def bridge_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("BRC1620_0_Z_map", "map actual MTS local residual channels into normal-form odd coordinates Z^A", "Z^A=I^A(Y_loc,q_loc,R_AB,source-tail,PPN-tail)", "MISSING_PARENT_Z_MAP", "1619 formal Z exists but actual MTS residual basis is not signed"),
        ("BRC1620_1_verticality", "prove Dq[Z^A]=0 or remove Z^A by constraint/no-pole before matter coupling", "Z^A in ker(Dq) on an open neighbourhood, not just at one point", "VERTICALITY_NOT_SIGNED", "1575/1576 keep R_AB coframe-visible unless shape-only quotient or constraint route is built"),
        ("BRC1620_2_matter_descent", "ordinary matter action descends through quotient-owned observed geometry", "S_matter=sum_i Sbar_i[Psi_i,e_obs(q(Phi)),theta_i]+dB_i", "DESCENT_NOT_SIGNED", "1575 matter descent signature remains unsigned"),
        ("BRC1620_3_constant_and_marker_silence", "material constants, standards, species labels, and source weights are invariant along Z", "Lie_Z theta_i=0 and no source-only marker/pre-action species slot", "NO_MARKER_NOT_DERIVED", "1415/1416 show object-language/current-owner theorem is missing"),
        ("BRC1620_4_boundary_silence", "boundary/worldtube/symplectic contribution is zero, exact/proper, or separately bounded", "B_Z=0 or B_Z in a source-backed residual row", "BOUNDARY_OPEN", "bulk quotient descent cannot hide a boundary force"),
        ("BRC1620_5_PPN_source_lock", "Z residual vector is locked to physical q_loc/PPN/source-normalization observables", "Z^A -> {q_loc,gamma,beta,alpha_i,xi,Gdot,R11} with units", "PPN_SOURCE_LOCK_NOT_DERIVED", "source-current/charge equality remains failed downstream"),
        ("BRC1620_6_verdict", "all bridge clauses close together", "BRC1620_0 through BRC1620_5 parent-signed", "PARENT_SIGNATURE_BRIDGE_NOT_CLOSED", "normal-form local silence cannot be promoted to current MTS"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "required_signature": required_signature,
            "mathematical_contract": mathematical_contract,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_DESCENT_PREMISE_MATRIX.csv; P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv; P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bridge_id, required_signature, mathematical_contract, status, effect in rows
    ]


def chain_rule_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CR1620_0_variation_formula",
            "For a candidate vertical direction v_Z, matter variation decomposes into quotient, constants/markers, direct vertices, and boundary.",
            "delta_v S_matter = D Sbar[q,theta].Dq[v_Z] + sum_a J_theta^a Lie_v theta_a + J_direct[v_Z] + delta_v B",
            "EXACT_CONDITIONAL_FORMULA_RECORDED",
            "turns source-current zero into explicit premises instead of vibes",
        ),
        (
            "CR1620_1_zero_lemma",
            "If Dq[v_Z]=0, Lie_v theta_a=0, J_direct=0, and delta_v B=0/proper, then J_Z=delta_v S_matter=0.",
            "J_Z=0 follows by chain rule and descent, not by Noether alone",
            "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA",
            "this is a real theorem clause but only conditional",
        ),
        (
            "CR1620_2_current_application",
            "Applying the lemma to current MTS fails because verticality, matter descent, constants, no-marker, and boundary clauses are unsigned.",
            "RMC1574_4 and MDS1575_5 keep beta/source-current zero blocked",
            "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS",
            "do not promote WEP/R10/local-GR source silence",
        ),
        (
            "CR1620_3_pre_action_countermodel",
            "Locality/covariance/additivity alone do not ban pre-action species weights or current rescalings.",
            "S_matter=sum_A w_A S_A remains a countermodel unless parent object-language/current owner forbids it",
            "COUNTERMODEL_REMAINS_WITHOUT_PARENT_GRAMMAR",
            "source-current zero needs object-language/current-owner proof or finite coefficient rows",
        ),
        (
            "CR1620_4_vertical_not_enough",
            "Dq[v_Z]=0 is not enough if direct source/test charge, marker readout, boundary flux, or finite-range response survives.",
            "vertical-to-coframe can still leave alpha(lambda) nonzero",
            "BETA_ONLY_SHORTCUT_BLOCKED",
            "forces separate source/test charge and arena projection gates",
        ),
        (
            "CR1620_5_verdict",
            "The chain-rule route is exact and worth keeping, but current evidence does not fire it for MTS.",
            "source-current zero remains conditional; bound rows must stay live",
            "CHAIN_RULE_THEOREM_CLOSED_APPLICATION_BLOCKED",
            "next route should make Z vertical by construction or fill finite coefficients",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "chain_rule_id": chain_rule_id,
            "claim_piece": claim_piece,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT.csv; P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv; P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for chain_rule_id, claim_piece, mathematical_statement, status, effect in rows
    ]


def verticality_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("QVM1620_0_observer_jacobian", "q includes observer radial phase-cell/J_q data", "Dq[v_Z] nonzero or unproved", "REJECT_AS_CURRENT_VERTICAL_PROOF", "R_AB=ln(T^2 S)=2 ln(J_q) makes the direction coframe/cell-visible unless constrained"),
        ("QVM1620_1_shape_only_quotient", "q quotients reciprocal cell-volume while preserving physical shape/orientation", "possible but not constructed", "POSSIBLE_CONTRACT_NOT_CLOSED", "needs independent unit/cell normalization and observed coframe functor"),
        ("QVM1620_2_constraint_first", "impose Z/R_AB=0 as a parent constraint or no-pole field before matter coupling", "possible if lambda/constraint origin is parent-signed", "BEST_NEXT_DERIVATION_ROUTE", "avoids pretending a visible field is gauge by removing it before matter sees it"),
        ("QVM1620_3_posthoc_delete", "delete Z/R_AB after readout because it is inconvenient", "refused", "REFUSED", "would hide a real source charge and violates the no-closure-only rule"),
        ("QVM1620_4_normal_form_Z", "identify 1619 Z^A with actual MTS residuals", "missing unified basis and Dq computation", "MISSING_COMPUTATION", "the formal normal form has no parent signature until this map is explicit"),
        ("QVM1620_5_verdict", "prove Z^A in ker(Dq) or constraint-remove it", "not currently proved", "VERTICALITY_MAP_NOT_CLOSED", "select constraint-first Z-map/no-pole origin next"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "verticality_id": verticality_id,
            "candidate_map": candidate_map,
            "Dq_status": dq_status,
            "result": result,
            "effect": effect,
            "source_anchors": "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv; P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for verticality_id, candidate_map, dq_status, result, effect in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCB1620_0_JZ_bulk",
            "J_Z source current",
            "J_Z = delta_Z S_matter",
            "MISSING_PARENT_DESCENT_OR_NUMERIC_BOUND",
            "same units as action variation / source current; exact units undeclared",
            "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
            "source_current_zero_not_derived",
            "PPN/R10/WEP/source-normalization",
            "MISSING_JZ_BOUND",
            "MISSING_UNITS",
            "bulk local silence cannot be claimed while J_Z is open",
        ),
        (
            "SCB1620_1_Dq_vertical_leak",
            "quotient derivative leakage",
            "Dq[Z^A]",
            "MISSING_DQ_COMPUTATION",
            "quotient-map derivative units",
            "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
            "verticality_not_proved",
            "observed coframe/source readout",
            "MISSING_DQ_BOUND",
            "map-dependent",
            "if Dq[Z] is finite, source-current zero chain rule does not fire",
        ),
        (
            "SCB1620_2_pre_action_weight",
            "species/source/current rescaling residual",
            "w_A or c_A current/source coefficient",
            "MISSING_PARENT_GRAMMAR_OR_FINITE_COEFFICIENT",
            "dimensionless coefficient",
            "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
            "ban_not_proved",
            "WEP/R10/source-current",
            "MISSING_WEIGHT_BOUND",
            "dimensionless",
            "locality/covariance alone do not ban this countermodel",
        ),
        (
            "SCB1620_3_boundary_flux",
            "odd boundary/worldtube flux",
            "B_Z^nu or delta_Z B",
            "MISSING_BOUNDARY_NO_FLUX_OR_BOUND",
            "stress flux / action boundary units",
            "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
            "boundary_open",
            "q_loc/PPN/source mass",
            "MISSING_BOUNDARY_BOUND",
            "MISSING_UNITS",
            "bulk zero can leak through local worldtube boundary",
        ),
        (
            "SCB1620_4_PPN_source_lock",
            "Z-to-observable lock",
            "Z^A -> {q_loc, gamma, beta, alpha_i, xi, Gdot, R11}",
            "MISSING_OBSERVABLE_PROJECTION",
            "mixed; must be declared per observable",
            "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
            "source_charge_equality_failed_current_corpus",
            "PPN/Newton/orbital/R10",
            "MISSING_PROJECTION_BOUND",
            "mixed",
            "even perfect Z silence is not Newton normalization unless the observable lock is proved",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": row_id,
            "residual_channel": channel,
            "operator_or_coefficient": coefficient,
            "status": status,
            "units": units,
            "source_path": source_path,
            "current_gate": current_gate,
            "observable_map": observable_map,
            "bound_value": bound_value,
            "bound_units": bound_units,
            "blocker": blocker,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, channel, coefficient, status, units, source_path, current_gate, observable_map, bound_value, bound_units, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1620_0_sources", "1619 normal-form, parent-signature gaps, and source-current ledgers imported", "SOURCE_CONTEXT_READY", "bridge test is anchored to existing evidence"),
        ("RUN1620_1_chain_rule", "matter variation under vertical direction decomposed by quotient chain rule", "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA", "J_Z zero theorem is mathematically available if premises close"),
        ("RUN1620_2_application", "verticality/descent/no-marker/boundary clauses unsigned", "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS", "formal theorem does not promote MTS"),
        ("RUN1620_3_verticality", "R_AB/Z visible or uncomputed under current q maps", "VERTICALITY_MAP_NOT_CLOSED", "best next route is constraint-first/no-pole parent origin"),
        ("RUN1620_4_bound_rows", "finite residual rows staged for J_Z, Dq leakage, pre-action weights, boundary, and PPN lock", "SOURCE_CURRENT_BOUND_ROWS_STAGED_NONCLAIM", "fallback branch gets concrete source-backed placeholders"),
        ("RUN1620_5_local_GR", "parent bridge not closed", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1620_6_next", "constraint-first Z-map avoids gauge-by-deletion", "SELECT_1621_CONSTRAINT_FIRST_ZMAP_OR_FINITE_SOURCE_CURRENT_COEFFICIENTS", "derive parent constraint/no-pole origin or fill finite coefficients"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "input_state": input_state,
            "runner_result": result,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, input_state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1620_0_chain_rule", "chain-rule source-current zero lemma", "CLOSED_CONDITIONAL_THEOREM", "exact if quotient descent, verticality, no-marker, and boundary clauses close"),
        ("CG1620_1_Z_map", "actual MTS residuals map to normal-form Z^A", "BLOCKED", "unified parent residual basis and Dq computation missing"),
        ("CG1620_2_verticality", "Z^A in ker(Dq)", "BLOCKED", "current R_AB/observer-cell route is nonzero or unproved"),
        ("CG1620_3_matter_descent", "matter action descends through quotient", "BLOCKED", "1575 descent signature not parent-signed"),
        ("CG1620_4_no_marker", "no pre-action species/source/current weights", "BLOCKED", "1415/1416 object-language/current-owner proof missing"),
        ("CG1620_5_boundary", "boundary/no-flux silence", "BLOCKED", "boundary/worldtube terms open"),
        ("CG1620_6_PPN_source_lock", "Z maps to physical PPN/Newton/R10 residuals", "BLOCKED", "source-current/charge equality and projection maps open"),
        ("CG1620_7_local_GR", "derived local GR/Newton recovery", "BLOCKED", "parent-signature bridge not closed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1620_0_chain_rule", "CHAIN_RULE_SOURCE_CURRENT_ZERO_LEMMA_CLOSED_CONDITIONAL", "delta_v S_matter vanishes by descent if v is quotient-vertical, constants/markers are silent, and boundary is proper", "keep this as the source-current zero theorem contract"),
        ("DEC1620_1_no_application", "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS", "verticality, descent, no-marker, boundary, and PPN/source lock remain unsigned", "no WEP/R10/local-GR promotion"),
        ("DEC1620_2_best_route", "CONSTRAINT_FIRST_ZMAP_IS_BEST_NEXT_ROUTE", "current R_AB looks coframe-visible unless shape-only quotient or parent constraint removes it before matter coupling", "try parent constraint/no-pole origin before more bound filling"),
        ("DEC1620_3_bound_rows", "SOURCE_CURRENT_BOUND_ROWS_STAGED_NONCLAIM", "J_Z, Dq leakage, pre-action weights, boundary flux, and PPN lock now have explicit nonclaim rows", "use them if derivation fails"),
        ("DEC1620_4_next", "NEXT_1621_CONSTRAINT_FIRST_ZMAP_OR_FINITE_SOURCE_CURRENT_COEFFICIENTS", "this is the shortest route to make the 1619 normal form an actual MTS branch", "derive lambda/constraint/no-pole origin or fill finite coefficients"),
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
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md",
            "script": "scripts/Y5_R2FR_constraint_first_Z_map_or_finite_source_current_coefficients.py",
            "objective": "try to derive a parent constraint/no-pole origin that removes the coframe-visible Z/R_AB residual before matter coupling; if it fails, fill finite nonclaim source-current coefficients for J_Z, Dq leakage, weights, and boundary flux",
            "success_condition": "either a parent-signed constraint-first Z-map closes verticality for the normal form, or finite coefficient rows replace theorem-zero language",
            "do_not": "do not delete visible residuals after readout, do not call shape-only quotient proved without Obs_e(q), do not use source-current zero without descent, do not promote local GR",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1620() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1620-Y5",
        "P8_Y5_PARENT_QLOC_1620",
        "P8_Y5_BRR545_1620",
        "Y5_R2FR_parent_signature_map",
        "R2FR_parent_signature_bridge_contract_nonclaim_1620",
        "R2FR_source_current_bound_fill_rows_nonclaim_1620",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    bridge = read_csv(BRIDGE_CONTRACT)
    chain_rule = read_csv(CHAIN_RULE)
    verticality = read_csv(VERTICALITY_MAP)
    bounds = read_csv(BOUND_ROWS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1620_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1620 local source paths exist"),
        ("VAL1620_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1620 source needles found"),
        ("VAL1620_2_input_dir_ready", INPUT_1620.exists(), "1620 quarantine input directory exists"),
        ("VAL1620_3_bridge_not_closed", any(row["status"] == "PARENT_SIGNATURE_BRIDGE_NOT_CLOSED" for row in bridge), "parent-signature bridge blocks promotion"),
        ("VAL1620_4_chain_rule_closed_conditional", any(row["status"] == "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA" for row in chain_rule), "chain-rule source-current zero lemma is closed as conditional"),
        ("VAL1620_5_application_blocked", any(row["status"] == "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS" for row in chain_rule), "chain-rule application to current MTS is blocked"),
        ("VAL1620_6_verticality_next_route", any(row["result"] == "BEST_NEXT_DERIVATION_ROUTE" for row in verticality), "constraint-first route selected as best verticality attempt"),
        ("VAL1620_7_bound_rows_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in bounds), "source-current bound rows remain nonclaim"),
        ("VAL1620_8_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1620_9_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1620_10_decision_next", any(row["decision"] == "NEXT_1621_CONSTRAINT_FIRST_ZMAP_OR_FINITE_SOURCE_CURRENT_COEFFICIENTS" for row in decisions), "decision selects constraint-first next target"),
        ("VAL1620_11_next_target_selected", any("1621-Y5-R2FR-constraint-first-Z-map-or-finite-source-current-coefficients.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1620_12_csv_parse", csv_parses(generated_csvs), "all generated 1620 CSVs parse"),
        ("VAL1620_13_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1620 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1620_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1620_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1620_16_formalization_untouched", no_formalization_1620(), "no 1620 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1620_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1620 parent-signature map and source-current zero or q_loc bound fill validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "/").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    bridge_rows = read_csv(BRIDGE_CONTRACT)
    chain_rows = read_csv(CHAIN_RULE)
    vertical_rows = read_csv(VERTICALITY_MAP)
    bound_rows = read_csv(BOUND_ROWS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1620 - R2/fR Parent-Signature Map And Source-Current Zero Or q_loc Bound Fill

## Verdict
- 1620 closes one useful theorem clause: `J_Z=0` follows by exact chain rule if `Z` is quotient-vertical, matter descends through the observed quotient, constants/markers are silent, and boundary terms are zero/proper.
- Current MTS does not yet satisfy those premises. The parent `Z` map, `Dq[Z]=0`, matter descent, no pre-action source weights, boundary silence, and PPN/source-normalization lock remain unsigned.
- The cleanest next derivation route is constraint-first/no-pole: remove the coframe-visible `Z/R_AB` residual before matter coupling instead of calling a visible residual gauge after the fact.
- Fallback source-current rows are now staged for `J_Z`, `Dq[Z]`, pre-action/source weights, boundary flux, and observable projection; all are nonclaim.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Parent Signature Bridge Contract

{md_table(bridge_rows, ["bridge_id", "required_signature", "mathematical_contract", "status", "effect"])}

## Chain-Rule Source-Current Zero Attempt

{md_table(chain_rows, ["chain_rule_id", "claim_piece", "mathematical_statement", "status", "effect"])}

## Quotient Verticality Map Audit

{md_table(vertical_rows, ["verticality_id", "candidate_map", "Dq_status", "result", "effect"])}

## Source-Current Bound Fill Rows

{md_table(bound_rows, ["bound_row_id", "residual_channel", "operator_or_coefficient", "status", "units", "source_path", "current_gate", "observable_map", "bound_value", "bound_units", "blocker"])}

## Runner

{md_table(runner, ["runner_id", "input_state", "runner_result", "effect"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "status", "reason"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"])}

## Validation

{md_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1620.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        BRIDGE_CONTRACT: bridge_contract_rows(),
        CHAIN_RULE: chain_rule_rows(),
        VERTICALITY_MAP: verticality_map_rows(),
        BOUND_ROWS: bound_rows(),
        RUNNER: runner_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    generated_csvs = list(outputs.keys())
    remove_pycache()
    write_csv(VALIDATION, validation_rows(generated_csvs))
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
