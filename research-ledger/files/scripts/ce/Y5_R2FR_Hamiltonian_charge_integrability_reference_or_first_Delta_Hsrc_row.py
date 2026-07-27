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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1796"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1796_0_1795_doc",
        "source_key": "1795_handoff",
        "source_path": ROOT / "1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md",
        "needles": ["DHC1795_0_integrability_reference", "NEXT1795_0_primary"],
        "role": "selects Hamiltonian charge integrability/reference as first Delta_Hsrc component",
    },
    {
        "source_id": "SRC1796_1_1795_validation",
        "source_key": "1795_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1795_VALIDATION.csv",
        "needles": ["VAL1795_OVERALL", "PASS"],
        "role": "confirms 1795 passed before 1796 starts",
    },
    {
        "source_id": "SRC1796_2_1795_component_pack",
        "source_key": "1795_delta_hsrc_component_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_DELTA_HSRC_COMPONENT_PACK.csv",
        "needles": ["DHC1795_0_integrability_reference", "MISSING_INTEGRABILITY_REFERENCE_INPUTS"],
        "role": "defines Delta_integrability as the first strict source-measure component",
    },
    {
        "source_id": "SRC1796_3_1795_next",
        "source_key": "1795_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1795_NEXT_TARGET.csv",
        "needles": ["NEXT1795_0_primary", "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md"],
        "role": "confirms 1796 is the selected primary target",
    },
    {
        "source_id": "SRC1796_4_HCI554",
        "source_key": "hamiltonian_charge_integrability_reference",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
        "needles": ["HCI554_0_target", "HCI554_6_integrability_verdict"],
        "role": "prior integrability/reference attempt and verdict",
    },
    {
        "source_id": "SRC1796_5_RCT555",
        "source_key": "radial_cterm_theorem_attempt",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_RADIAL_CTERM_THEOREM_ATTEMPT.csv",
        "needles": ["RCT555_0_target", "RCT555_6_verdict"],
        "role": "radial C-term and reference closure attempt",
    },
    {
        "source_id": "SRC1796_6_FB554",
        "source_key": "integrability_source_equality_fill_rows",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
        "needles": ["FB554_0_HPiM_integrability_reference_bound", "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO"],
        "role": "first unfilled finite integrability/reference row",
    },
    {
        "source_id": "SRC1796_7_FB554_eval",
        "source_key": "integrability_source_equality_evaluator",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_EVALUATOR.csv",
        "needles": ["FB554_0_HPiM_integrability_reference_bound", "not_claimable"],
        "role": "evaluator marks the integrability/reference row nonclaim",
    },
    {
        "source_id": "SRC1796_8_HPRD553",
        "source_key": "hamiltonian_repair_decomposition",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["HPRD553_0_integrability", "HPRD553_6_total_no_cancellation"],
        "role": "Hamiltonian PiM repair decomposition with strict no-cancellation policy",
    },
    {
        "source_id": "SRC1796_9_HSI541",
        "source_key": "hamiltonian_source_measure_inputs",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv",
        "needles": ["HSI541_0_boundary_reference", "HSI541_6_PPN_vector"],
        "role": "boundary/reference, frame, calibration and PPN input requirements",
    },
    {
        "source_id": "SRC1796_10_HSS541",
        "source_key": "hamiltonian_source_measure_scorecard",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
        "needles": ["HSS541_1_charge_integrability", "HSS541_7_PPN_followthrough"],
        "role": "source-measure scorecard keeps charge integrability failed",
    },
    {
        "source_id": "SRC1796_11_C505_ledger",
        "source_key": "noether_c_term_ledger",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv",
        "needles": ["C505_projector", "C505_boundary"],
        "role": "C-term ledger for EH, extra, projector and boundary terms",
    },
    {
        "source_id": "SRC1796_12_T505_theorem",
        "source_key": "noether_closure_theorem",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_conditional_Noether_mass_charge_closure", "T505_Newton_limit_corollary"],
        "role": "conditional Noether mass closure theorem and Newton corollary",
    },
    {
        "source_id": "SRC1796_13_D505_chain",
        "source_key": "noether_closure_chain",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        "needles": ["D505_3_exterior_derivative", "D505_6_worldtube_readout"],
        "role": "derivation chain that local charge closure requires C-term silence",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_SOURCE_REGISTER.csv",
    "integrability_reference_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
    "cterm_reference_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_CTERM_REFERENCE_GATE.csv",
    "first_delta_integrability_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_FIRST_DELTA_INTEGRABILITY_ROW.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1796_VALIDATION.csv",
}

DOC_PATH = ROOT / "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": source["role"],
            }
        )
    return rows


def integrability_reference_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_0_phase_space_exactness",
            "required_piece": "Hamiltonian variation is exact on the allowed local branch",
            "mathematical_form": "delta H_tau[S] = int_S(delta Q_tau^MTS - i_tau Theta_MTS), with curl_deltaH=0",
            "current_status": "TARGET_DEFINED_NOT_PARENT_DERIVED",
            "blocking_gap": "MTS still lacks a fully varied parent L, Theta_MTS and Q_tau for all active sectors",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_1_parent_theta_Q_owner",
            "required_piece": "one parent action owns the symplectic potential and Noether charge",
            "mathematical_form": "delta L_parent = E_A delta Phi^A + dTheta_MTS(Phi,delta Phi); J_tau = Theta_MTS(Phi,L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau",
            "current_status": "CONDITIONAL_ROUTE_ONLY",
            "blocking_gap": "EH/covariant-phase-space route is known, but inheritance by MTS sectors is not signed",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_2_fixed_reference_lock",
            "required_piece": "reference subtraction is fixed before source/orbit/readout comparison",
            "mathematical_form": "partial_source H_ref = partial_r H_ref = partial_t H_ref = partial_frame H_ref = 0",
            "current_status": "REFERENCE_LOCK_MISSING",
            "blocking_gap": "Delta_ref source/radius/time/frame silence is not theorem-zero or source-bounded",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_3_tau_lock",
            "required_piece": "same observed time generator in source, charge, denominator and readout",
            "mathematical_form": "tau_source = tau_charge = tau_MHref = tau_readout and delta tau = 0 on local variations",
            "current_status": "TAU_MHREF_LOCK_MISSING",
            "blocking_gap": "observed coframe/time branch is not parent-derived through the Hamiltonian source-measure map",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_4_symplectic_boundary_silence",
            "required_piece": "extra symplectic flux and boundary reference flux vanish or are fixed topological constants",
            "mathematical_form": "Delta_symp = 0 and B_zero_flux = 0, or both source-backed finite rows enter Delta_integrability",
            "current_status": "MISSING_BOUNDARY_REFERENCE_ZERO_OR_BOUND",
            "blocking_gap": "boundary cohomology/no-hair and projector silence remain retained blockers",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_5_Cterm_silence",
            "required_piece": "radial/reference C-terms do not contribute to the compact exterior charge",
            "mathematical_form": "int_A(C_EH + C_extra + C_projector + C_boundary + C_ref)=0",
            "current_status": "C_TERM_ZERO_NOT_DERIVED",
            "blocking_gap": "radial C-term theorem attempt leaves EH, extra, projector, boundary and reference clauses unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "HIR1796_6_verdict",
            "required_piece": "claim-grade integrable fixed-reference Hamiltonian mass functional",
            "mathematical_form": "HIR1796_0 through HIR1796_5 pass in one parent action and one local branch",
            "current_status": "INTEGRABILITY_REFERENCE_NOT_PROVED",
            "blocking_gap": "the derivation route is alive, but today it stops at named missing clauses",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def cterm_reference_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_0_C_EH",
            "term": "C_EH",
            "required_zero_or_bound": "local exterior EH equations hold with fixed Lambda/background subtraction",
            "source_anchor": "C505_EH;RCT555_2_C_EH_zero",
            "current_status": "CONDITIONAL_NOT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_1_C_extra",
            "term": "C_extra",
            "required_zero_or_bound": "non-EH/domain/memory/range/motion sectors carry no exterior Hamiltonian mass charge",
            "source_anchor": "C505_extra;RCT555_3_C_extra_zero",
            "current_status": "EXTRA_SECTOR_SILENCE_NOT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_2_C_projector",
            "term": "C_projector",
            "required_zero_or_bound": "mass projector is fixed/covariantly constant and creates no commutator hair",
            "source_anchor": "C505_projector;RCT555_4_C_projector_zero",
            "current_status": "PROJECTOR_COMMUTATOR_NOT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_3_C_boundary",
            "term": "C_boundary",
            "required_zero_or_bound": "boundary/improvement flux vanishes or is fixed by source-independent topology",
            "source_anchor": "C505_boundary;RCT555_5_C_boundary_ref_zero",
            "current_status": "BOUNDARY_FLUX_ZERO_NOT_SIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_4_C_ref",
            "term": "C_ref / Delta_ref",
            "required_zero_or_bound": "reference subtraction cannot depend on source, radius, time, frame, or readout",
            "source_anchor": "HCI554_3_reference_lock;FB554_0_HPiM_integrability_reference_bound",
            "current_status": "REFERENCE_SUBTRACTION_NOT_FIXED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CRG1796_5_verdict",
            "term": "C_total",
            "required_zero_or_bound": "all C terms vanish or enter a strict source-backed absolute envelope",
            "source_anchor": "RCT555_6_verdict;D505_3_exterior_derivative",
            "current_status": "CTERM_REFERENCE_GATE_NOT_CLOSED",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def first_delta_integrability_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_0_identity",
            "component": "Delta_integrability_over_MH",
            "definition": "first Delta_Hsrc component: nonintegrable or reference-shifted Hamiltonian mass charge",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(B_zero_flux_over_MH)+abs(Delta_symp_over_MH)",
            "required_input": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;B_zero_flux_over_MH;Delta_symp_over_MH;M_H_ref;source_file;assumptions",
            "current_value": "MISSING_COMPONENT_NUMERIC_OR_THEOREM_ZERO",
            "status": "STAGED_NONCLAIM_SCHEMA",
            "source_path": str(RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv"),
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_1_delta_H_tau_nonintegrable",
            "component": "delta_H_tau_nonintegrable_over_MH",
            "definition": "curl/non-exact part of the Hamiltonian charge variation",
            "formula": "||delta_1 delta_2 H_tau - delta_2 delta_1 H_tau|| / M_H_ref",
            "required_input": "parent Theta_MTS;Q_tau^MTS;allowed variation domain;integrability source path",
            "current_value": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "status": "MISSING_PARENT_SYMPLECTIC_CURL_INPUT",
            "source_path": "MISSING_SOURCE_FILE",
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_2_Delta_ref",
            "component": "Delta_ref_over_MH",
            "definition": "fixed-reference subtraction mismatch in the same Hamiltonian mass branch",
            "formula": "|H_ref(active)-H_ref(fixed)|/M_H_ref",
            "required_input": "reference convention;source/radius/time/frame derivative checks;source path",
            "current_value": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "status": "MISSING_FIXED_REFERENCE_INPUT",
            "source_path": "MISSING_SOURCE_FILE",
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_3_B_zero_flux",
            "component": "B_zero_flux_over_MH",
            "definition": "boundary/improvement flux through the compact exterior linking surface",
            "formula": "|int_boundary B_tau|/M_H_ref",
            "required_input": "boundary primitive;linking surface;orientation;source path;units",
            "current_value": "MISSING_BOUNDARY_FLUX_NUMERIC_OR_THEOREM_ZERO",
            "status": "MISSING_BOUNDARY_PRIMITIVE_INPUT",
            "source_path": "MISSING_SOURCE_FILE",
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_4_Delta_symp",
            "component": "Delta_symp_over_MH",
            "definition": "uncontrolled extra symplectic flux in the Hamiltonian charge variation",
            "formula": "|int_boundary omega_extra(delta Phi,L_tau Phi)|/M_H_ref",
            "required_input": "extra-sector omega;local branch boundary condition;source path",
            "current_value": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "status": "MISSING_EXTRA_SYMPLECTIC_INPUT",
            "source_path": "MISSING_SOURCE_FILE",
            "units": "dimensionless_ratio_to_M_H_ref",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_5_tau_MHref_lock",
            "component": "tau_MHref_denominator_lock",
            "definition": "same observed time and same positive M_H_ref denominator for the charge row",
            "formula": "tau_source=tau_charge=tau_MHref and M_H_ref>0",
            "required_input": "tau lock certificate;positive M_H_ref;same-frame certificate",
            "current_value": "MISSING_TAU_LOCK_CERTIFICATE",
            "status": "MISSING_DENOMINATOR_LOCK_INPUT",
            "source_path": "MISSING_SOURCE_FILE",
            "units": "certificate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DIR1796_6_acceptance",
            "component": "Delta_integrability_row_acceptance",
            "definition": "acceptance gate for the first Delta_Hsrc component",
            "formula": "all DIR1796_1..DIR1796_5 are theorem-zero or source-backed numeric rows with no MISSING markers",
            "required_input": "complete source-backed row pack",
            "current_value": "NOT_ACCEPTED",
            "status": "REJECT_CURRENT_DELTA_INTEGRABILITY_ROW",
            "source_path": str(RESIDUALS / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_EVALUATOR.csv"),
            "units": "gate",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1796_0_nonintegrable_charge",
            "countermodel": "Q_tau exists as a surface expression but its variation has nonzero curl on the allowed MTS branch",
            "survives_current_constraints": True,
            "why_survives": "Theta_MTS/Q_tau/variation-domain owner is still conditional",
            "what_kills_it": "parent-signed exactness theorem or finite curl bound row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1796_1_reference_after_readout",
            "countermodel": "H_ref silently absorbs source, radius, time, frame, or orbital readout dependence",
            "survives_current_constraints": True,
            "why_survives": "fixed-reference derivatives are not theorem-zero or source-backed",
            "what_kills_it": "reference superselection certificate with derivative silence",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1796_2_boundary_symplectic_flux",
            "countermodel": "boundary/improvement or extra symplectic flux shifts the Hamiltonian mass",
            "survives_current_constraints": True,
            "why_survives": "B_zero_flux and Delta_symp remain named missing inputs",
            "what_kills_it": "boundary primitive/no-flux theorem or measured finite bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1796_3_Cterm_radial_hair",
            "countermodel": "C_extra, C_projector, C_boundary, or C_ref carries radial Hamiltonian mass hair",
            "survives_current_constraints": True,
            "why_survives": "radial C-term theorem is conditional and rejects current claim",
            "what_kills_it": "C-term zero theorem or source-backed radial envelope",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1796_4_tau_denominator_mismatch",
            "countermodel": "the charge is normalized with a different time generator or M_H_ref than the source/readout branch",
            "survives_current_constraints": True,
            "why_survives": "tau_MHref lock and same-frame certificate are missing",
            "what_kills_it": "single observed-time/coframe denominator certificate",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1796_0_integrable_Htau",
            "claim": "Q_tau defines an integrable fixed-reference Hamiltonian mass",
            "status": "BLOCKED",
            "reason": "HIR1796 verdict is INTEGRABILITY_REFERENCE_NOT_PROVED",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1796_1_Delta_integrability_zero",
            "claim": "Delta_integrability=0",
            "status": "BLOCKED",
            "reason": "reference, symplectic, boundary and tau lock clauses remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1796_2_finite_Delta_integrability_score",
            "claim": "finite source-backed Delta_integrability score",
            "status": "BLOCKED",
            "reason": "first row schema contains MISSING_* inputs and no accepted numeric row",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1796_3_Delta_Hsrc_score",
            "claim": "Delta_Hsrc is zero or numerically bounded",
            "status": "BLOCKED",
            "reason": "first component is unclosed before R_eq, commutator and extra-charge rows are reached",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1796_4_local_GR_Newton_source_normalization",
            "claim": "source-normalized local GR/Newton recovery",
            "status": "BLOCKED",
            "reason": "Hamiltonian source-measure equality is not derived or source-bounded",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1796_0_result",
            "decision": "ZERO_PROOF_NOT_CLOSED",
            "reason": "phase-space exactness, fixed reference, symplectic/boundary silence, C-term silence and tau lock remain unsigned",
            "next_action": "do not claim integrability; use named blockers",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1796_1_first_row",
            "decision": "FIRST_DELTA_INTEGRABILITY_ROW_EMITTED_NONCLAIM",
            "reason": "the exact missing row now has component slots and units but no numeric/theorem-zero payload",
            "next_action": "source or derive DIR1796_1 through DIR1796_5",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1796_2_policy",
            "decision": "NO_CANCELLATION_NO_READOUT_REFERENCE_POLICY_RETAINED",
            "reason": "a readout-fitted reference could fake source-measure equality",
            "next_action": "keep absolute-envelope scoring and source-before-orbit ordering",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1796_3_next",
            "decision": "DELTA_INTEGRABILITY_SOURCE_ACQUISITION_OR_BOUND_ROW_NEXT",
            "reason": "the first live object is now a concrete row pack rather than a vague integrability problem",
            "next_action": "build 1797 to source/derive delta_H_tau_nonintegrable, Delta_ref, B_zero_flux, Delta_symp and tau/MHref lock",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1796_0_primary",
            "next_target": "1797-Y5-R2FR-Delta-integrability-source-acquisition-or-bound-row.md",
            "script": "scripts/Y5_R2FR_Delta_integrability_source_acquisition_or_bound_row.py",
            "objective": "try to source or derive the first Delta_integrability row inputs; otherwise emit a blocker ledger with no claim",
            "selection_status": "selected",
            "success_condition": "DIR1796_1 through DIR1796_5 become theorem-zero or source-backed finite rows with units and paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1796_1_parallel_commutator",
            "next_target": "1797b-Y5-R2FR-PiM-commutator-chainmap-or-finite-Icommutator-row.md",
            "script": "scripts/Y5_R2FR_PiM_commutator_chainmap_or_finite_Icommutator_row.py",
            "objective": "prove [d,Pi_M^H]J_H=0 or source a finite commutator profile row",
            "selection_status": "held_parallel",
            "success_condition": "parent-signed chainmap theorem or source-backed commutator envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1796_2_parallel_Req",
            "next_target": "1797c-Y5-R2FR-Hilbert-topological-equality-or-Req-bound-row.md",
            "script": "scripts/Y5_R2FR_Hilbert_topological_equality_or_Req_bound_row.py",
            "objective": "prove same-worldtube Hilbert/topological equality or fill R_eq source-measure residual row",
            "selection_status": "held_parallel",
            "success_condition": "R_eq theorem-zero or source-backed residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "integrability_reference_attempt": integrability_reference_attempt_rows(),
        "cterm_reference_gate": cterm_reference_gate_rows(),
        "first_delta_integrability_row": first_delta_integrability_row_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1796_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    claim_flags = (
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "score_emitted",
        "accepted_for_scoring",
        "theorem_closed_for_claim",
        "parent_signed",
        "valid_prediction_row",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            for flag in claim_flags:
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    ready_flags = (
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "score_emitted",
        "accepted_for_scoring",
        "theorem_closed_for_claim",
        "valid_prediction_row",
        "gate_pass",
    )
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in ready_flags:
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1796_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1796_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1796_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1796_2_integrability_reference_not_proved",
            any(
                row["attempt_id"] == "HIR1796_6_verdict"
                and row["current_status"] == "INTEGRABILITY_REFERENCE_NOT_PROVED"
                for row in rows_map["integrability_reference_attempt"]
            )
            and all(
                not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"])
                for row in rows_map["integrability_reference_attempt"]
            ),
            "integrability/reference zero proof is not closed",
        ),
        (
            "VAL1796_3_cterm_reference_gate_blocks",
            any(
                row["gate_id"] == "CRG1796_5_verdict"
                and row["current_status"] == "CTERM_REFERENCE_GATE_NOT_CLOSED"
                for row in rows_map["cterm_reference_gate"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["cterm_reference_gate"]),
            "C-term/reference gate blocks the zero proof",
        ),
        (
            "VAL1796_4_first_delta_row_rejected",
            any(
                row["row_id"] == "DIR1796_6_acceptance"
                and row["status"] == "REJECT_CURRENT_DELTA_INTEGRABILITY_ROW"
                for row in rows_map["first_delta_integrability_row"]
            )
            and all(
                not boolish(row["accepted_for_scoring"])
                and not boolish(row["valid_prediction_row"])
                and not boolish(row["valid_for_claim"])
                and not boolish(row["claim_allowed"])
                for row in rows_map["first_delta_integrability_row"]
            ),
            "first Delta_integrability row is a nonclaim rejected schema",
        ),
        (
            "VAL1796_5_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1796_6_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1796_7_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1796_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1796_9_decision_next",
            any(
                row["decision_id"] == "DEC1796_3_next"
                and row["decision"] == "DELTA_INTEGRABILITY_SOURCE_ACQUISITION_OR_BOUND_ROW_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects Delta_integrability source acquisition next",
        ),
        (
            "VAL1796_10_next_selected",
            any(row["route_id"] == "NEXT1796_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1796_11_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1796 CSVs parse"),
        ("VAL1796_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1796_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1796_14_formalization_untouched", formalization_untouched(), "no 1796 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1796_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1796 Hamiltonian charge integrability/reference or first Delta_integrability row checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1796 - Y5/R2FR Hamiltonian Charge Integrability Reference or First Delta-Hsrc Row",
            "",
            "## Verdict",
            "",
            "1796 tries the derivation route first. The target is clean: `Q_tau^MTS` must define an integrable Hamiltonian mass functional with a fixed reference and the same observed time generator used by the source/readout branch.",
            "",
            "That proof is not closed in the current corpus. The failure is not hand-wavy now: it is localized to phase-space exactness, parent `Theta/Q_tau` ownership, fixed-reference silence, symplectic/boundary flux silence, radial/reference C-term silence, and the `tau/M_H_ref` denominator lock.",
            "",
            "So the checkpoint emits the first exact nonclaim row for the `Delta_Hsrc` pack:",
            "",
            "`Delta_integrability/M_H_ref = |delta_H_tau_nonintegrable|/M_H_ref + |Delta_ref|/M_H_ref + |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref`.",
            "",
            "**Claim ceiling:** no integrable Hamiltonian mass charge, no `Delta_integrability=0`, no finite `Delta_integrability` score, no `Delta_Hsrc` score, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1796.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Integrability Reference Attempt",
            markdown_table(rows_map["integrability_reference_attempt"], ["attempt_id", "required_piece", "mathematical_form", "current_status", "blocking_gap", "valid_for_claim"]),
            "",
            "## C-Term Reference Gate",
            markdown_table(rows_map["cterm_reference_gate"], ["gate_id", "term", "required_zero_or_bound", "source_anchor", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## First Delta-Integrability Row",
            markdown_table(rows_map["first_delta_integrability_row"], ["row_id", "component", "formula", "current_value", "status", "units", "accepted_for_scoring", "valid_prediction_row", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This does not kill the route. It makes the next job sharper: either prove the first row is zero from the parent action, or fill it with finite source-backed inputs. The useful win is that `Delta_Hsrc` is no longer a fog bank; its first unresolved term now has named slots, units, and acceptance rules.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1796 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
