from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1734"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1734 - Current Descent Lemma Dq Tau Projectability Or Theta Leak Row"
UTC = datetime.now(timezone.utc).isoformat()


def yesno(value: bool) -> str:
    return "True" if value else "False"


def no() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1734_0_1733_doc",
        "source_key": "1733_doc",
        "source_path": ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
        "needles": ["NEXT1733_0_primary", "q/Dq plus tau projectability"],
    },
    {
        "source_id": "SRC1734_1_1733_next",
        "source_key": "1733_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_NEXT_TARGET.csv",
        "needles": ["1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md", "selected"],
    },
    {
        "source_id": "SRC1734_2_1733_validation",
        "source_key": "1733_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1733_VALIDATION.csv",
        "needles": ["VAL1733_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1734_3_1667_doc",
        "source_key": "1667_q_Dq_doc",
        "source_path": ROOT / "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md",
        "needles": ["Q_NOT_COMPUTABLE_CURRENT_CORPUS", "Dq"],
    },
    {
        "source_id": "SRC1734_4_1668_doc",
        "source_key": "1668_constraint_doc",
        "source_path": ROOT / "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md",
        "needles": ["CFA1668_8_verdict", "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CORPUS"],
    },
    {
        "source_id": "SRC1734_5_1505_Dq_tests",
        "source_key": "1505_Dq_verticality",
        "source_path": RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
        "needles": ["DQT1505_8_acceptance", "BLOCKED"],
    },
    {
        "source_id": "SRC1734_6_1505_theorem",
        "source_key": "1505_quotient_vertical_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
        "needles": ["THM1505_2_current_branch_verdict", "KEEP_BETA_AND_ALPHA_CLOSURE_BOUND"],
    },
    {
        "source_id": "SRC1734_7_1022_vertical",
        "source_key": "1022_vertical_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
        "needles": ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"],
    },
    {
        "source_id": "SRC1734_8_1023_coupling",
        "source_key": "1023_coupling_descent",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "needles": ["CDA1023_4_verdict", "coupling_not_theorem_zero"],
    },
    {
        "source_id": "SRC1734_9_684_tau_audit",
        "source_key": "684_tau_generator_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "needles": ["TGA684_6_total", "NO_PARENT_SIGNED_TAU_LOCK"],
    },
    {
        "source_id": "SRC1734_10_685_tau_contract",
        "source_key": "685_tau_generator_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_6_verdict", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1734_11_742_tau_owner",
        "source_key": "742_observed_tau_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv",
        "needles": ["TOA742_4_owner_verdict", "rejected_for_current_claim"],
    },
    {
        "source_id": "SRC1734_12_742_tau_proof",
        "source_key": "742_tau_proof_verdict",
        "source_path": RESIDUALS / "P8_Y5_R10_742_TAU_PROOF_VERDICT.csv",
        "needles": ["TPV742_3_tau_owner_result", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1734_13_687_selector_tau",
        "source_key": "687_selector_tau",
        "source_path": RESIDUALS / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
        "needles": ["STT687_5_verdict", "failed_for_claim"],
    },
    {
        "source_id": "SRC1734_14_688_symgrad_tau",
        "source_key": "688_symgrad_tau",
        "source_path": RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
        "needles": ["SGT688_8_verdict", "source_input_required_nonclaim"],
    },
    {
        "source_id": "SRC1734_15_1519_coframe_tau",
        "source_key": "1519_coframe_tau_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "needles": ["OCF1519_7_verdict", "COFRAME_TAU_LOCK_NOT_PROVED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_SOURCE_REGISTER.csv",
    "projectability_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_DQ_TAU_PROJECTABILITY_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_PROJECTABLE_CURRENT_THEOREM.csv",
    "theta_leak_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1734_VALIDATION.csv",
}


COPY_MAP = {
    "projectability_audit": "R2FR_1734_DQ_TAU_PROJECTABILITY_AUDIT.csv",
    "theorem_attempt": "R2FR_1734_PROJECTABLE_CURRENT_THEOREM.csv",
    "theta_leak_rows": "R2FR_1734_THETA_QTAU_LEAK_ROWS.csv",
    "runner_refusal": "R2FR_1734_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1734_DECISION_LEDGER.csv",
    "next_target": "R2FR_1734_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1734_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles_present = all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": yesno(needles_present),
                "checked_utc": UTC,
            }
        )
    return rows


def projectability_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_0_q_map",
            "clause": "computable quotient map q",
            "required_statement": "q: Phi_parent -> Q_obs is defined before matter, clocks, source, boundary and orbit readout.",
            "current_status": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
            "blocker": "1667 records q as a partial contract, not an adopted computable parent map.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_1_Dq_kernel",
            "clause": "Dq kernel and vertical directions",
            "required_statement": "Dq[v]=0 is computed for the exact retained directions, not asserted by analogy.",
            "current_status": "DQT1505_ACCEPTANCE_BLOCKED",
            "blocker": "unified X/Z/phi/RAB basis and Dq computation are missing; source/test/marker/boundary charges may survive.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_2_tau_projectability",
            "clause": "tau projects through q",
            "required_statement": "Dq(L_tau Phi)=L_tau_red q(Phi), with tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary.",
            "current_status": "NO_PARENT_SIGNED_TAU_LOCK",
            "blocker": "684/685/742 keep tau roles split and not parent-owned.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_3_vertical_distribution_invariant",
            "clause": "tau preserves vertical equivalence",
            "required_statement": "If v is vertical, then [L_tau,v] is vertical or produces a retained source row.",
            "current_status": "MISSING_DQ_TAU_COMMUTATOR",
            "blocker": "without q, Dq, v basis and tau action, the commutator Dq([L_tau,v]) cannot be computed.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_4_stationarity",
            "clause": "stationary/Killing observed generator",
            "required_statement": "nabla_(mu tau_nu)=0 or admissible Hamiltonian stationarity is parent-derived on the compact local exterior.",
            "current_status": "KILLING_UPGRADE_REJECTED_CURRENT_CHAIN",
            "blocker": "687/688 show selector/trace silence does not kill shear, lapse, shift, boundary, stress or tau mismatch.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_5_matter_coupling",
            "clause": "matter and constants descend through q",
            "required_statement": "S_matter, constants, coframe, source measure and readout depend only on q(Phi).",
            "current_status": "COUPLING_NOT_THEOREM_ZERO",
            "blocker": "1023 and 1519 keep constants, marker, hidden frame, boundary/projector and tau/source channels open.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "DTP1734_6_verdict",
            "clause": "Dq/tau projectability for current descent",
            "required_statement": "DTP1734_0 through DTP1734_5 pass together.",
            "current_status": "PROJECTABILITY_NOT_SIGNED",
            "blocker": "q, Dq, tau lock, vertical commutator, stationarity and matter/coupling descent all remain unsigned.",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1734_0_projectable_current_identity",
            "statement": "If q is a parent quotient and tau is projectable, then the observed-time current descends.",
            "mathematical_form": "Dq(L_tau Phi)=L_tau_red q(Phi); L_parent=q^*L_red+dB+silent; J_tau^parent=q^*J_tau^red+d(i_tau B)+C_vert",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "q, Dq, tau action, boundary/reference and vertical silence are not parent-signed",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1734_1_tau_commutator_law",
            "statement": "The first obstruction is a Dq/tau commutator leak.",
            "mathematical_form": "E_Dq_tau[v] := Dq([L_tau,v]) - [L_tau_red,Dq(v)]; if Dq(v)=0 this must vanish or be retained",
            "proof_status": "OBSTRUCTION_DEFINED_NOT_ZEROED",
            "missing_for_current_claim": "q, Dq, vertical basis and tau action are missing",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1734_2_tau_stationarity_law",
            "statement": "Even projectable tau must be stationary or its nonstationary contraction must be retained.",
            "mathematical_form": "epsilon_tau contains trace, shear, lapse, shift/extrinsic, boundary motion, tau mismatch and stress contraction pieces",
            "proof_status": "SOURCE_INPUT_REQUIRED_NONCLAIM",
            "missing_for_current_claim": "688 component pack has no zero theorem or sourced values",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1734_3_current_verdict",
            "statement": "Current MTS proves Dq/tau projectability strongly enough to sign the current descent lemma.",
            "mathematical_form": "DTP1734_0..DTP1734_5 all pass; E_Dq_tau=0; epsilon_tau=0; coupling descent signed",
            "proof_status": "FAIL_CURRENT_CLAIM",
            "missing_for_current_claim": "projectability audit fails and leak rows remain required",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def theta_leak_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["projectability_audit"]),
        str(OUTPUTS["theorem_attempt"]),
        str(RESIDUALS / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"),
        str(RESIDUALS / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TLR1734_0_Dq_tau_commutator",
            "quantity": "E_Dq_tau_commutator_norm",
            "definition": "failure of tau flow to preserve quotient vertical directions",
            "formula": "||Dq([L_tau,v]) - [L_tau_red,Dq(v)]||, with Dq(v)=0 requiring zero",
            "required_inputs": "q_map;Dq;vertical_basis;L_tau_on_parent;L_tau_red;norm;source_path",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_Q_MAP;MISSING_DQ;MISSING_VERTICAL_BASIS;MISSING_TAU_ACTION;MISSING_NORM",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_DQ_TAU_COMMUTATOR",
            "units": "quotient_norm_per_time_or_dimensionless_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TLR1734_1_Dq_source_readout",
            "quantity": "Dsource_readout_Dq_tau_leak",
            "definition": "source/clock/orbit/readout leakage caused by q/Dq or tau mismatch",
            "formula": "||D_source_readout[Dq(v)]|| + ||Delta_tau_source_charge_clock_orbit_boundary||",
            "required_inputs": "source_map;clock_map;orbit_map;boundary_tau;Dq;vertical_basis;source_path",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_SOURCE_MAP;MISSING_CLOCK_MAP;MISSING_ORBIT_MAP;MISSING_BOUNDARY_TAU;MISSING_DQ",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_SOURCE_READOUT_DQ_TAU_LEAK",
            "units": "source_readout_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TLR1734_2_tau_nonstationary",
            "quantity": "epsilon_nonstationary_tau",
            "definition": "nonstationary observed-time generator obstruction",
            "formula": "abs(trace)+abs(shear)+abs(lapse/accel)+abs(shift/extrinsic)+abs(boundary_motion)+abs(tau_mismatch)+abs(T_H symgrad tau)/M_H_ref",
            "required_inputs": "SGT688 components;stress_envelope;M_H_ref;common_units;source_path",
            "current_status": "SOURCE_INPUT_REQUIRED_NONCLAIM",
            "missing_inputs": "MISSING_TRACE;MISSING_SHEAR;MISSING_LAPSE_ACCELERATION;MISSING_SHIFT_EXTRINSIC;MISSING_BOUNDARY_MOTION;MISSING_TAU_MISMATCH;MISSING_STRESS_ENVELOPE;MISSING_M_H_REF",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_EPSILON_TAU",
            "units": "dimensionless_after_MHref_or_time_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TLR1734_3_coupling_marker",
            "quantity": "qbar_XT_or_marker_tau_leak",
            "definition": "matter constants/material labels/hidden frame leakage that survives coframe Dq silence",
            "formula": "|delta_{v,tau} theta_A| + |hidden conformal/disformal X channel| + |projector/boundary source charge|",
            "required_inputs": "constant_owner;material_marker_owner;hidden_frame_coefficients;projector_boundary_charge;source_path",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "missing_inputs": "MISSING_CONSTANT_OWNER;MISSING_MATERIAL_MARKER_OWNER;MISSING_HIDDEN_FRAME_COEFFICIENTS;MISSING_PROJECTOR_BOUNDARY_CHARGE",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "MISSING_COUPLING_MARKER_LEAK",
            "units": "dimensionless_or_force_coupling_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TLR1734_4_total_theta_qtau_leak",
            "quantity": "epsilon_theta_Qtau_projectability_abs",
            "definition": "absolute no-cancellation leak envelope for projectable-current descent",
            "formula": "|E_Dq_tau| + |Dsource_readout_Dq_tau| + |epsilon_nonstationary_tau| + |qbar_XT_or_marker_tau_leak|",
            "required_inputs": "TLR1734_0 through TLR1734_3;common_units;M_H_ref_or_declared_norm;source_path",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "missing_inputs": "MISSING_DQ_TAU_COMMUTATOR;MISSING_SOURCE_READOUT_DQ_TAU_LEAK;MISSING_EPSILON_TAU;MISSING_COUPLING_MARKER_LEAK;MISSING_COMMON_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_or_theorem_value": "BLOCKED",
            "units": "dimensionless_gate_or_declared_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1734_0_projectable_current",
            "quantity": "Dq/tau projectable current theorem",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_Q_MAP;MISSING_DQ_KERNEL;MISSING_TAU_LOCK;MISSING_DQ_TAU_COMMUTATOR;MISSING_COUPLING_DESCENT",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1734_1_theta_qtau_leak",
            "quantity": "epsilon_theta_Qtau_projectability_abs",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "MISSING_COMPONENT_VALUES;MISSING_COMMON_UNITS;MISSING_MHREF_OR_NORM",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1734_2_Htau_local_GR",
            "quantity": "H_tau/M_H_ref/Newton/local-GR chain",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "PROJECTABILITY_NOT_SIGNED;THETA_QTAU_OWNER_OPEN;HTAU_INTEGRABILITY_OPEN;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1734_0_projectability_status",
            "decision": "do not sign Dq/tau projectability",
            "because": "q is not computable, Dq kernels are unfilled, tau roles are not locked, and stationarity/coupling descent are unsigned",
            "next_action": "keep the exact theorem as a contract and use leak rows for source acquisition",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1734_1_leak_pack",
            "decision": "stage theta/Qtau projectability leak rows",
            "because": "failed projectability must become testable Dq/tau/coupling residuals rather than invisible assumptions",
            "next_action": "declare units, source requirements and arena projections for the leak rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1734_2_derivation_parallel",
            "decision": "hold L_X/Q_X vertical-symplectic silence as a parallel derivation route",
            "because": "even if q/tau source rows are staged, the cleaner future proof still needs sector current ownership",
            "next_action": "after source-pack staging, attempt vertical symplectic silence from L_X/Q_X",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1734_0_primary",
            "next_target": "1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md",
            "script": "scripts/Y5_R2FR_Dq_tau_theta_leak_source_pack_units_and_arena_projections.py",
            "objective": "turn Dq/tau/current-descent leak symbols into source-ready nonclaim rows with units and R10/PPN/WEP/clock/orbit projections",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1734_1_parallel_LX",
            "next_target": "1735b-Y5-R2FR-vertical-symplectic-silence-LX-QX-proof-attempt.md",
            "script": "scripts/Y5_R2FR_vertical_symplectic_silence_LX_QX_proof_attempt.py",
            "objective": "try deriving Theta_X/Q_X silence from a sector L_X owner, or emit Q_X boundary/source residuals",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1734_2_later_Htau",
            "next_target": "1736-Y5-R2FR-Htau-first-row-component-source-pack.md",
            "script": "scripts/Y5_R2FR_Htau_first_row_component_source_pack.py",
            "objective": "combine projectability, boundary and H_tau curl components only after leak units are declared",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1734_0_q_Dq_projectability",
            "claim": "q/Dq/tau projectability is parent-signed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "DTP1734_6 verdict is PROJECTABILITY_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1734_1_current_descent",
            "claim": "current descends to observed reduced charge",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "q, Dq, tau, stationarity and coupling descent clauses remain unsigned",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1734_2_theta_leak_zero",
            "claim": "theta/Qtau projectability leak is zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "TLR1734 rows are missing values or zero theorems",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1734_3_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no projectable current, no H_tau integrability, no M_H_ref, and no local PPN pass",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "projectability_audit": projectability_audit_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "theta_leak_rows": theta_leak_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "claim_gate": claim_gate_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1734_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1734_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def theta_rows_nonclaim(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text and "BLOCKED" not in row_text:
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1734_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1734_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1734*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_register = rows_map["source_register"]
    audit = rows_map["projectability_audit"]
    theorem = rows_map["theorem_attempt"]
    leaks = rows_map["theta_leak_rows"]
    runner = rows_map["runner_refusal"]
    decision = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1734_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1734_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1734_2_1733_route_preserved",
            any(row["source_key"] == "1733_next_target" and row["needles_present"] == "True" for row in source_register),
            "1733 selected Dq/tau projectability route",
            "1733 selected route missing",
        ),
        check(
            "VAL1734_3_projectability_audit_complete",
            {row["clause"] for row in audit}
            >= {
                "computable quotient map q",
                "Dq kernel and vertical directions",
                "tau projects through q",
                "tau preserves vertical equivalence",
                "stationary/Killing observed generator",
                "matter and constants descend through q",
                "Dq/tau projectability for current descent",
            },
            "projectability audit covers q, Dq, tau, commutator, stationarity, coupling and verdict",
            "projectability audit missing required clause",
        ),
        check(
            "VAL1734_4_projectability_blocked",
            any(row["audit_id"] == "DTP1734_6_verdict" and row["current_status"] == "PROJECTABILITY_NOT_SIGNED" for row in audit),
            "Dq/tau projectability remains unsigned",
            "projectability verdict missing or claim-enabled",
        ),
        check(
            "VAL1734_5_theorem_fails_current_claim",
            any(row["theorem_id"] == "PCT1734_3_current_verdict" and row["proof_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt explicitly fails current claim",
            "theorem attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1734_6_leak_rows_nonclaim",
            len(leaks) == 5 and theta_rows_nonclaim(leaks),
            "theta/Qtau leak rows carry blockers and remain nonclaim",
            "theta/Qtau leak rows malformed or claim-enabled",
        ),
        check(
            "VAL1734_7_runner_refusals_cover_chain",
            {row["quantity"] for row in runner}
            >= {"Dq/tau projectable current theorem", "epsilon_theta_Qtau_projectability_abs", "H_tau/M_H_ref/Newton/local-GR chain"},
            "runner refusals cover projectability, leak envelope and local-GR chain",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1734_8_decision_next",
            any(row["decision_id"] == "DEC1734_1_leak_pack" for row in decision),
            "decision selects theta/Qtau leak source pack",
            "leak source-pack decision missing",
        ),
        check(
            "VAL1734_9_next_selected",
            any(row["route_id"] == "NEXT1734_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1735 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1734_10_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1734_11_csv_parse", parsed_ok, "all generated 1734 CSVs parse", "one or more generated 1734 CSVs failed to parse"),
        check("VAL1734_12_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1734_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1734_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1734_15_formalization_untouched", formalization_untouched(), "no 1734 outputs found under formalization-workbench", "1734 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1734_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1734 current descent Dq/tau projectability validation" if overall else "one or more 1734 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1734 tries the exact projectability clause needed by the descent-current lemma.",
        "- Current result: **not signed**. `q` is not computable, `Dq` kernels are unfilled, tau roles are not parent-locked, and stationarity/coupling descent remain open.",
        "- Useful progress: the first obstruction is now a concrete commutator-type leak: `E_Dq_tau = Dq([L_tau,v]) - [L_tau_red,Dq(v)]`.",
        "- If `Dq(v)=0`, this obstruction must vanish. Since it is not currently computable, it becomes a source-ready nonclaim row rather than a theorem-zero.",
        "- No `Theta_total/Q_tau`, `H_tau`, `M_H_ref`, R10, WEP, PPN, clock, orbital, Newton, local-GR, or `q_loc=0` claim is made.",
        "",
        "## Interpretation",
        "This is the useful kind of failure. It tells us exactly where the hidden assumption would live: not in a mystical mass term, but in whether the observed time flow preserves the quotient fibres and whether matter/source readout only sees the quotient. If that fails, MTS has a measurable leak vector, not a free pass.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Dq Tau Projectability Audit",
        markdown_table(rows_map["projectability_audit"], ["audit_id", "clause", "current_status", "blocker", "valid_for_claim", "claim_allowed"]),
        "",
        "## Projectable Current Theorem",
        markdown_table(rows_map["theorem_attempt"], ["theorem_id", "statement", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
        "",
        "## Theta Qtau Leak Rows",
        markdown_table(rows_map["theta_leak_rows"], ["row_id", "quantity", "current_status", "missing_inputs", "numeric_or_theorem_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "The derivation route is still alive as a contract, but the current corpus cannot sign it. The next honest move is not to keep saying 'maybe q kills it'; it is to give the Dq/tau/theta leak rows units and arena projections so they can be bounded or tested. Parallel to that, the cleaner future proof remains the L_X/Q_X vertical-symplectic silence attempt.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1734_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1734 validation FAIL")
    print("1734 validation PASS")


if __name__ == "__main__":
    main()
