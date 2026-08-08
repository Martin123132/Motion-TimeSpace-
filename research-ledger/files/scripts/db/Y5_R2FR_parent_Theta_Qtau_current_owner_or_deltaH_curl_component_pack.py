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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1798"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1798_0_1797_doc",
        "source_key": "1797_handoff",
        "source_path": ROOT / "1797-Y5-R2FR-Delta-integrability-source-acquisition-or-bound-row.md",
        "needles": ["DEC1797_3_next", "NEXT1797_0_primary"],
        "role": "selects parent Theta/Q_tau owner or deltaH curl component pack as 1798 target",
    },
    {
        "source_id": "SRC1798_1_1797_validation",
        "source_key": "1797_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1797_VALIDATION.csv",
        "needles": ["VAL1797_OVERALL", "PASS"],
        "role": "confirms 1797 passed before 1798 starts",
    },
    {
        "source_id": "SRC1798_2_1797_next",
        "source_key": "1797_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_NEXT_TARGET.csv",
        "needles": ["NEXT1797_0_primary", "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md"],
        "role": "selected 1798 route",
    },
    {
        "source_id": "SRC1798_3_1797_matrix",
        "source_key": "1797_source_acquisition_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_SOURCE_ACQUISITION_MATRIX.csv",
        "needles": ["AQR1797_0_delta_H_tau_nonintegrable", "SOURCE_MAPPED_NOT_FILLED"],
        "role": "delta_H_tau acquisition row routes to Theta/Q_tau owner",
    },
    {
        "source_id": "SRC1798_4_1645_theorem",
        "source_key": "1645_htau_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1645_HTAU_INTEGRABILITY_THEOREM.csv",
        "needles": ["HTM1645_2_curl_decomposition", "HTM1645_5_verdict"],
        "role": "H_tau integrability theorem and curl decomposition",
    },
    {
        "source_id": "SRC1798_5_1653_owner_gate",
        "source_key": "1653_owner_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1653_HTAU_QTAU_CURRENT_OWNER_GATE.csv",
        "needles": ["HTO1653_0_parent_action_current", "HTO1653_5_owner_verdict"],
        "role": "H_tau/Q_tau current-owner gate",
    },
    {
        "source_id": "SRC1798_6_1733_owner_audit",
        "source_key": "1733_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "needles": ["COA1733_0_L_parent", "COA1733_7_owner_verdict"],
        "role": "Theta_total/Q_tau owner audit",
    },
    {
        "source_id": "SRC1798_7_1733_components",
        "source_key": "1733_component_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
        "needles": ["TQC1733_0_EH", "TQC1733_6_total_Qtau"],
        "role": "Theta/Q_tau component rows by sector",
    },
    {
        "source_id": "SRC1798_8_1733_first_row",
        "source_key": "1733_first_row_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_HTAU_FIRST_ROW_SCHEMA.csv",
        "needles": ["HFR1733_1_curl_components", "HFR1733_2_total_deltaH"],
        "role": "deltaH curl component formula and total",
    },
    {
        "source_id": "SRC1798_9_1734_leaks",
        "source_key": "1734_leak_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1734_THETA_QTAU_LEAK_ROWS.csv",
        "needles": ["TLR1734_0_Dq_tau_commutator", "TLR1734_4_total_theta_qtau_leak"],
        "role": "Dq/tau/source/readout leak rows",
    },
    {
        "source_id": "SRC1798_10_1785_parent_gate",
        "source_key": "1785_parent_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_PARENT_LAGRANGIAN_THETA_VX_GATE.csv",
        "needles": ["PLT1785_0_L_parent", "PLT1785_8_verdict"],
        "role": "parent Lagrangian/theta/vX gate",
    },
    {
        "source_id": "SRC1798_11_993_current_gate",
        "source_key": "993_current_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv",
        "needles": ["CEG993_0_action_inventory", "CEG993_4_verdict"],
        "role": "current extraction gate",
    },
    {
        "source_id": "SRC1798_12_993_sector_ledger",
        "source_key": "993_sector_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv",
        "needles": ["SEC993_0_EH_core", "SEC993_7_EM_charge_coupling"],
        "role": "sector-current extraction ledger",
    },
    {
        "source_id": "SRC1798_13_993_qtau_decomposition",
        "source_key": "993_qtau_decomposition",
        "source_path": RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        "needles": ["QDEC993_0_EH", "QDEC993_5_total"],
        "role": "Q_tau decomposition ledger",
    },
    {
        "source_id": "SRC1798_14_993_eh_credit",
        "source_key": "993_eh_credit",
        "source_path": RESIDUALS / "P8_Y5_R10_993_EH_BASELINE_CREDIT_LEDGER.csv",
        "needles": ["EHC993_0_EH_current_shape", "EHC993_2_EH_boundary_terms"],
        "role": "EH baseline credit guard",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_SOURCE_REGISTER.csv",
    "parent_current_owner_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_PARENT_CURRENT_OWNER_ATTEMPT.csv",
    "deltah_curl_component_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1798_VALIDATION.csv",
}

DOC_PATH = ROOT / "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md"


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


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(str(by_key[key]) for key in keys)


def parent_current_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_0_parent_action_current",
            "needed_object": "one explicit local parent current action",
            "required_form": "delta L_parent = E_A delta Phi^A + dTheta_total, with EH, matter, extra, projector, boundary, tau, reference and coupling sectors included before readout",
            "current_evidence": "structural inventory exists in CEG993_0 and HTO1653_0",
            "current_status": "TEMPLATE_AVAILABLE_NOT_CURRENT_OWNER",
            "blocking_gap": "MISSING_EXPLICIT_L_PARENT_VARIATION_FOR_ALL_RETAINED_SECTORS",
            "source_paths": src("1653_owner_gate", "1785_parent_gate", "993_current_gate"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_1_theta_total_extraction",
            "needed_object": "Theta_total",
            "required_form": "Theta_total = Theta_EH + Theta_matter + Theta_X + Theta_projector + delta B_ref + Theta_boundary",
            "current_evidence": "COA1733_1 gives the split; TQC1733 rows keep non-EH pieces missing",
            "current_status": "THETA_TOTAL_NOT_EXTRACTED",
            "blocking_gap": "MISSING_THETA_X;MISSING_THETA_PROJECTOR;MISSING_BOUNDARY_REFERENCE_OWNER;MISSING_MATTER_COUPLING_DESCENT",
            "source_paths": src("1733_owner_audit", "1733_component_rows", "993_sector_ledger"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_2_Qtau_extraction",
            "needed_object": "Q_tau^MTS",
            "required_form": "J_tau = Theta_total(Phi,L_tau Phi)-i_tau L_parent = dQ_tau^MTS + C_tau, with Q_tau^MTS=sum_s Q_tau_s",
            "current_evidence": "QDEC993 lists the decomposition but marks only EH as conditional reference",
            "current_status": "QTAU_TOTAL_NOT_PROMOTED",
            "blocking_gap": "MISSING_Q_X;MISSING_Q_PROJECTOR;MISSING_Q_BOUNDARY;MISSING_SOURCE_GLUE;MISSING_DQ_DESCENT",
            "source_paths": src("993_qtau_decomposition", "1733_component_rows", "1653_owner_gate"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_3_tau_projectability",
            "needed_object": "observed tau action through q and all readouts",
            "required_form": "L_tau Phi projectable through q; tau_source=tau_charge=tau_clock=tau_boundary=tau_readout",
            "current_evidence": "COA1733_3 and TLR1734 rows retain Dq/tau leakage",
            "current_status": "TAU_PROJECTABILITY_NOT_PARENT_OWNED",
            "blocking_gap": "MISSING_Q_MAP;MISSING_DQ;MISSING_VERTICAL_BASIS;MISSING_TAU_ACTION;MISSING_SOURCE_READOUT_LOCK",
            "source_paths": src("1733_owner_audit", "1734_leak_rows"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_4_boundary_reference_owner",
            "needed_object": "B_ref, H_ref and boundary representative",
            "required_form": "boundary improvement/reference subtraction fixed before readout and derivative-silent",
            "current_evidence": "COA1733_4 and TQC1733_3 retain boundary/reference owner gaps",
            "current_status": "BOUNDARY_REFERENCE_NOT_PARENT_OWNED",
            "blocking_gap": "MISSING_B_REF;MISSING_B_CLASS;MISSING_CORNER_TERMS;MISSING_REFERENCE_LOCK;MISSING_BOUNDARY_NOHAIR",
            "source_paths": src("1733_owner_audit", "1733_component_rows", "993_eh_credit"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_5_matter_quotient_coupling_descent",
            "needed_object": "matter/source/coupling descent in the same current",
            "required_form": "matter measure, coframe, connection, constants and source readout descend through q(Phi) or produce finite leakage rows",
            "current_evidence": "COA1733_5/6 and PLT1785_7 keep matter/projector silence and q/Dq descent unsigned",
            "current_status": "DESCENT_NOT_SIGNED",
            "blocking_gap": "MISSING_MATTER_FUNCTOR_DESCENT;MISSING_Q_DQ;MISSING_OBSERVED_COFRAME_FUNCTOR;MISSING_COUPLING_MARKER_LEAK",
            "source_paths": src("1733_owner_audit", "1734_leak_rows", "1785_parent_gate"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCO1798_6_verdict",
            "needed_object": "parent Theta_total/Q_tau^MTS current owner",
            "required_form": "PCO1798_0 through PCO1798_5 pass together in one parent branch",
            "current_evidence": "all source gates route to formal contracts or missing component rows",
            "current_status": "PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "blocking_gap": "MISSING_ONE_SIGNED_PARENT_CURRENT_CHAIN",
            "source_paths": src("1733_owner_audit", "1653_owner_gate", "993_current_gate"),
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def deltah_curl_component_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_0_EH_baseline",
            "symbol": "I_EH",
            "definition": "EH covariant-phase-space curl contribution for the observed metric sector",
            "formula": "I_EH = d_field alpha_tau^EH under fixed EH boundary/reference conditions",
            "current_status": "CONDITIONAL_GR_REFERENCE_ONLY",
            "required_input": "MTS parent reduction to EH;fixed tau;fixed boundary/reference;extra-sector silence",
            "source_anchor": "TQC1733_0_EH;SEC993_0_EH_core;EHC993_0_EH_current_shape",
            "component_value": "NOT_COUNTED_AS_MTS_PROOF",
            "units": "energy_variation_curl_or_dimensionless_after_MHref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_1_I_X",
            "symbol": "I_X",
            "definition": "extra motion/time/memory/range sector curl obstruction",
            "formula": "|d_field alpha_tau^X|/M_H_ref",
            "current_status": "MISSING_EXTRA_SECTOR_CURRENT",
            "required_input": "L_X;Theta_X;Q_tau_X;C_tau_X;boundary_conditions;M_H_ref;source_path",
            "source_anchor": "TQC1733_1_X_extra;SEC993_3_extra_motion_time_memory",
            "component_value": "MISSING_I_X_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_2_I_projector",
            "symbol": "I_projector",
            "definition": "projector/source-current contribution to the Hamiltonian curl",
            "formula": "|d_field alpha_tau^projector|/M_H_ref",
            "current_status": "MISSING_PROJECTOR_CURRENT_OWNER",
            "required_input": "Pi_M definition;delta Pi_M;J_H;commutator zero/bound;M_H_ref;source_path",
            "source_anchor": "TQC1733_2_projector_PiM;SEC993_4_domain_projector_selector;SEC993_6_metric_readout_PiM",
            "component_value": "MISSING_I_PROJECTOR_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_3_I_boundary",
            "symbol": "I_boundary",
            "definition": "boundary/corner/improvement contribution to the Hamiltonian curl",
            "formula": "|d_field alpha_tau^boundary|/M_H_ref",
            "current_status": "MISSING_BOUNDARY_REFERENCE_OWNER",
            "required_input": "B_ref;B_class;corner_terms;boundary_nohair;boundary_condition;M_H_ref;source_path",
            "source_anchor": "TQC1733_3_boundary_reference;SEC993_5_boundary_reference;EHC993_2_EH_boundary_terms",
            "component_value": "MISSING_I_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_4_I_ref",
            "symbol": "I_ref",
            "definition": "field-space curl from changing H_ref/B_ref branch",
            "formula": "|curl(delta H_ref)|/M_H_ref",
            "current_status": "MISSING_FIXED_REFERENCE_LOCK",
            "required_input": "H_ref rule;fixed_branch_id;derivative-silent reference;surface_pair;tau_id;M_H_ref",
            "source_anchor": "HTM1645_3_fixed_reference_law;TQC1733_4_tau_surface;COA1733_4_boundary_reference",
            "component_value": "MISSING_I_REF_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_5_I_tau",
            "symbol": "I_tau",
            "definition": "nonprojectable or nonstationary observed-time generator contribution",
            "formula": "|curl_tau alpha_tau|/M_H_ref",
            "current_status": "MISSING_TAU_PROJECTABILITY_LOCK",
            "required_input": "tau_id;tau action on parent fields;Dq_tau_commutator;stationarity/symgrad_tau envelope;M_H_ref",
            "source_anchor": "COA1733_3_tau_projectability;TLR1734_0_Dq_tau_commutator;TLR1734_2_tau_nonstationary",
            "component_value": "MISSING_I_TAU_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref_or_declared_time_norm",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_6_I_surface",
            "symbol": "I_surface",
            "definition": "surface-pair/frame/source-readout mismatch in the Hamiltonian one-form",
            "formula": "|curl_surface alpha_tau|/M_H_ref",
            "current_status": "MISSING_SURFACE_FRAME_SOURCE_LOCK",
            "required_input": "surface_pair;frame_lock;source_readout_lock;boundary_tau;M_H_ref",
            "source_anchor": "TQC1733_4_tau_surface;TLR1734_1_Dq_source_readout",
            "component_value": "MISSING_I_SURFACE_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_7_I_Dq",
            "symbol": "I_Dq",
            "definition": "quotient-map/current leakage into Theta/Q_tau or source readout",
            "formula": "|Dq_current_leak + source_readout_Dq_leak + coupling_marker_leak|/M_H_ref",
            "current_status": "MISSING_Q_DQ_DESCENT",
            "required_input": "q_map;Dq;vertical_basis;observed_coframe_functor;coupling_marker_owner;M_H_ref",
            "source_anchor": "TQC1733_5_Dq_leak;COA1733_6_q_Dq_descent;TLR1734_4_total_theta_qtau_leak",
            "component_value": "MISSING_I_DQ_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_ratio_to_M_H_ref_or_declared_norm",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "DCC1798_8_total_abs_envelope",
            "symbol": "delta_H_tau_nonintegrable_over_MH",
            "definition": "strict absolute envelope for the field-space curl obstruction",
            "formula": "(|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref",
            "current_status": "REJECT_CURRENT_DELTAH_CURL_PACK",
            "required_input": "DCC1798_1 through DCC1798_7 theorem-zero or source-backed finite rows with common units and positive same-frame M_H_ref",
            "source_anchor": "HFR1733_2_total_deltaH;HTM1645_2_curl_decomposition",
            "component_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless_gate",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACG1798_0_EH_import_guard",
            "gate": "EH current may be used as comparator but not as MTS proof",
            "current_status": "GUARD_PASS_NO_CLAIM",
            "reason": "EH baseline shape is allowed only after MTS parent reduction and extra-sector silence",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACG1798_1_parent_owner",
            "gate": "parent Theta_total/Q_tau owner signed",
            "current_status": "FAIL_OWNER_NOT_SIGNED",
            "reason": "PCO1798_6 verdict remains not signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACG1798_2_component_values",
            "gate": "curl components theorem-zero or source-backed finite",
            "current_status": "FAIL_COMPONENTS_MISSING",
            "reason": "DCC1798_1 through DCC1798_7 contain MISSING_* component values",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACG1798_3_MHref_units",
            "gate": "positive same-frame M_H_ref and common units",
            "current_status": "FAIL_DENOMINATOR_COMMON_UNITS_MISSING",
            "reason": "M_H_ref remains missing and several components lack common units",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ACG1798_4_verdict",
            "gate": "deltaH curl component pack claim readiness",
            "current_status": "DELTAH_CURL_PACK_NOT_READY",
            "reason": "component pack is useful routing, not a scoreable row",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1798_0_extra_current_tail",
            "countermodel": "extra motion/time/memory sector carries nonzero Noether current curl",
            "survives_current_constraints": True,
            "why_survives": "L_X, Theta_X and Q_tau_X are not extracted from one parent action",
            "what_kills_it": "I_X theorem-zero or finite source-backed component row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1798_1_projector_curl",
            "countermodel": "Pi_M variation or commutator contributes to d_field alpha_tau",
            "survives_current_constraints": True,
            "why_survives": "Pi_M chain map and projector current owner are not signed",
            "what_kills_it": "I_projector theorem-zero or finite commutator/curl bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1798_2_boundary_reference_tail",
            "countermodel": "boundary/reference representative shifts Q_tau or H_ref under variations",
            "survives_current_constraints": True,
            "why_survives": "B_ref, boundary class and fixed reference are still parent-open",
            "what_kills_it": "I_boundary and I_ref theorem-zero or finite source-backed rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1798_3_tau_surface_mismatch",
            "countermodel": "tau, surface, frame or readout choice changes the Hamiltonian one-form",
            "survives_current_constraints": True,
            "why_survives": "tau projectability and surface/source-readout locks remain missing",
            "what_kills_it": "I_tau and I_surface theorem-zero or finite source-backed rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1798_4_Dq_coupling_leak",
            "countermodel": "quotient/current/coupling leakage survives into the charge or source readout",
            "survives_current_constraints": True,
            "why_survives": "q, Dq, observed coframe functor and coupling-marker owner are not signed",
            "what_kills_it": "I_Dq theorem-zero or finite source-backed row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1798_0_parent_current_owner",
            "claim": "parent Theta_total/Q_tau^MTS current owner is signed",
            "status": "BLOCKED",
            "reason": "PCO1798_6 is PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1798_1_deltaH_curl_score",
            "claim": "delta_H_tau_nonintegrable_over_MH can be scored",
            "status": "BLOCKED",
            "reason": "DCC1798_8 total envelope is rejected because component rows are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1798_2_integrability_zero",
            "claim": "d_field alpha_tau=0",
            "status": "BLOCKED",
            "reason": "no current-owner theorem and no component zero pack",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1798_3_local_GR_Newton",
            "claim": "local GR/Newton source-normalized branch is derived",
            "status": "BLOCKED",
            "reason": "Hamiltonian source charge remains unowned/unintegrated",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1798_0_owner_result",
            "decision": "PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "reason": "one signed parent current chain has not been varied across EH, extra, projector, boundary, tau, reference and coupling sectors",
            "next_action": "do not promote Q_tau^MTS beyond component scaffold",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1798_1_component_pack",
            "decision": "DELTAH_CURL_COMPONENT_PACK_EMITTED_NONCLAIM",
            "reason": "the curl obstruction is now split into I_X, I_projector, I_boundary, I_ref, I_tau, I_surface and I_Dq",
            "next_action": "source or derive components one by one with no cancellation",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1798_2_EH_policy",
            "decision": "EH_BASELINE_RETAINED_AS_COMPARATOR_ONLY",
            "reason": "GR charge formalism is useful shape evidence but not a proof of the MTS total current",
            "next_action": "require MTS reduction and sector silence before giving EH credit",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1798_3_next",
            "decision": "MINIMAL_PARENT_CURRENT_ACTION_SKELETON_OR_FIRST_IX_ROW_NEXT",
            "reason": "I_X is the first non-EH live curl component and depends on the same parent action that could close the owner route",
            "next_action": "build 1799 to try a minimal parent current action skeleton; if it fails, emit the first I_X row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1798_0_primary",
            "next_target": "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
            "script": "scripts/Y5_R2FR_minimal_parent_current_action_skeleton_or_first_Ix_row.py",
            "objective": "try to write a minimal parent current action skeleton that owns the first non-EH curl component I_X; if not, emit strict I_X source/bound row",
            "selection_status": "selected",
            "success_condition": "I_X is theorem-zero from a parent action or becomes a finite source-backed component row with units and M_H_ref",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1798_1_parallel_projector",
            "next_target": "1799b-Y5-R2FR-PiM-projector-current-owner-or-Iprojector-row.md",
            "script": "scripts/Y5_R2FR_PiM_projector_current_owner_or_Iprojector_row.py",
            "objective": "derive projector current owner/chain map or emit I_projector row",
            "selection_status": "held_parallel",
            "success_condition": "I_projector theorem-zero or finite source-backed row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1798_2_parallel_tau_Dq",
            "next_target": "1799c-Y5-R2FR-tau-Dq-projectability-or-Itau-IDq-row.md",
            "script": "scripts/Y5_R2FR_tau_Dq_projectability_or_Itau_IDq_row.py",
            "objective": "derive tau/Dq projectability or emit I_tau/I_Dq source rows",
            "selection_status": "held_parallel",
            "success_condition": "I_tau and I_Dq theorem-zero or finite source-backed rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_current_owner_attempt": parent_current_owner_attempt_rows(),
        "deltah_curl_component_pack": deltah_curl_component_pack_rows(),
        "acceptance_gate": acceptance_gate_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1798_{key.upper()}.csv")


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
        "parent_signed",
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
        if not (RAB_QUEUE / f"JR1798_{key.upper()}.csv").exists():
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
        ("VAL1798_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1798_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1798_2_parent_owner_not_signed",
            any(
                row["attempt_id"] == "PCO1798_6_verdict"
                and row["current_status"] == "PARENT_THETA_QTAU_OWNER_NOT_SIGNED"
                for row in rows_map["parent_current_owner_attempt"]
            )
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["parent_current_owner_attempt"]),
            "parent Theta/Q_tau owner remains unsigned",
        ),
        (
            "VAL1798_3_curl_pack_rejected",
            any(
                row["component_id"] == "DCC1798_8_total_abs_envelope"
                and row["current_status"] == "REJECT_CURRENT_DELTAH_CURL_PACK"
                for row in rows_map["deltah_curl_component_pack"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["deltah_curl_component_pack"]),
            "deltaH curl component pack is rejected and non-scoreable",
        ),
        (
            "VAL1798_4_acceptance_gate_blocks",
            any(
                row["gate_id"] == "ACG1798_4_verdict"
                and row["current_status"] == "DELTAH_CURL_PACK_NOT_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks scoring",
        ),
        (
            "VAL1798_5_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1798_6_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1798_7_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1798_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1798_9_decision_next",
            any(
                row["decision_id"] == "DEC1798_3_next"
                and row["decision"] == "MINIMAL_PARENT_CURRENT_ACTION_SKELETON_OR_FIRST_IX_ROW_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects minimal parent current action or first I_X row next",
        ),
        (
            "VAL1798_10_next_selected",
            any(row["route_id"] == "NEXT1798_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1798_11_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1798 CSVs parse"),
        ("VAL1798_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1798_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1798_14_formalization_untouched", formalization_untouched(), "no 1798 outputs found under formalization-workbench"),
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
            "check_id": "VAL1798_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1798 parent Theta/Q_tau current owner or deltaH curl component pack checkpoint",
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
            "# 1798 - Y5/R2FR Parent Theta-Qtau Current Owner or DeltaH Curl Component Pack",
            "",
            "## Verdict",
            "",
            "1798 tries the derivation route first: make `Theta_total` and `Q_tau^MTS` parent-owned from one current chain. That route remains alive but not signed. The EH current is usable as a comparator shape, not as proof of the total MTS Hamiltonian charge.",
            "",
            "The checkpoint therefore emits the strict `delta_H_tau` curl component pack:",
            "",
            "`delta_H_tau_nonintegrable/M_H_ref = (|I_X| + |I_projector| + |I_boundary| + |I_ref| + |I_tau| + |I_surface| + |I_Dq|)/M_H_ref`.",
            "",
            "**Claim ceiling:** no parent `Theta_total/Q_tau^MTS` owner, no scoreable `delta_H_tau` row, no `H_tau` integrability, no source-normalized Newton/local-GR claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1798.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Parent Current Owner Attempt",
            markdown_table(rows_map["parent_current_owner_attempt"], ["attempt_id", "needed_object", "required_form", "current_status", "blocking_gap", "parent_signed", "valid_for_claim"]),
            "",
            "## DeltaH Curl Component Pack",
            markdown_table(rows_map["deltah_curl_component_pack"], ["component_id", "symbol", "definition", "formula", "current_status", "component_value", "score_ready", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
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
            "The curl problem is now properly decomposed. The strongest next move is to attack `I_X`, not because it is guaranteed to close, but because it is the first non-EH place where a minimal parent action could either make the sector silent or force a finite residual.",
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
    print(f"1798 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
