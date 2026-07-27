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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1797"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1797_0_1796_doc",
        "source_key": "1796_handoff",
        "source_path": ROOT / "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md",
        "needles": ["DEC1796_3_next", "NEXT1796_0_primary"],
        "role": "selects Delta_integrability source acquisition as 1797 target",
    },
    {
        "source_id": "SRC1797_1_1796_validation",
        "source_key": "1796_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1796_VALIDATION.csv",
        "needles": ["VAL1796_OVERALL", "PASS"],
        "role": "confirms 1796 passed before 1797 starts",
    },
    {
        "source_id": "SRC1797_2_1796_first_row",
        "source_key": "1796_first_delta_integrability_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1796_FIRST_DELTA_INTEGRABILITY_ROW.csv",
        "needles": ["DIR1796_1_delta_H_tau_nonintegrable", "DIR1796_6_acceptance"],
        "role": "declares the five missing Delta_integrability inputs",
    },
    {
        "source_id": "SRC1797_3_1732_Htau_MHref",
        "source_key": "1732_htau_mhref_source_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
        "needles": ["HMS1732_0_M_H_ref", "HMS1732_1_delta_H_tau"],
        "role": "older H_tau/M_H_ref source rows for denominator and curl inputs",
    },
    {
        "source_id": "SRC1797_4_1733_first_row_schema",
        "source_key": "1733_htau_first_row_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_HTAU_FIRST_ROW_SCHEMA.csv",
        "needles": ["HFR1733_0_alpha_tau", "HFR1733_2_total_deltaH"],
        "role": "Hamiltonian one-form and curl decomposition schema",
    },
    {
        "source_id": "SRC1797_5_1733_components",
        "source_key": "1733_theta_qtau_component_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
        "needles": ["TQC1733_0_EH", "TQC1733_6_total_Qtau"],
        "role": "sector split for Theta_total and Q_tau^MTS",
    },
    {
        "source_id": "SRC1797_6_1733_owner_audit",
        "source_key": "1733_theta_qtau_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        "needles": ["COA1733_0_L_parent", "COA1733_7_owner_verdict"],
        "role": "current owner audit for parent Theta/Q_tau extraction",
    },
    {
        "source_id": "SRC1797_7_993_curl_schema",
        "source_key": "993_deltaH_curl_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_993_DELTAH_CURL_INPUT_SCHEMA.csv",
        "needles": ["DHC993_0_sector_current_extraction", "DHC993_3_deltaH_curl_value"],
        "role": "source-ready schema for the deltaH curl value",
    },
    {
        "source_id": "SRC1797_8_994_envelope",
        "source_key": "994_deltaH_no_cancellation",
        "source_path": RESIDUALS / "P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
        "needles": ["DHE994_0_definition", "DHE994_2_EH_limit"],
        "role": "no-cancellation envelope and EH limit guard",
    },
    {
        "source_id": "SRC1797_9_994_input_schemas",
        "source_key": "994_residual_input_schemas",
        "source_path": RESIDUALS / "P8_Y5_R10_994_RESIDUAL_INPUT_SCHEMAS.csv",
        "needles": ["RIS994_1_residual_current_values", "RIS994_2_deltaH_envelope_values"],
        "role": "residual-current and deltaH envelope input schemas",
    },
    {
        "source_id": "SRC1797_10_995_bound_schema",
        "source_key": "995_residual_bound_row_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_995_RC9940_RESIDUAL_BOUND_ROW_SCHEMA.csv",
        "needles": ["BR995_0_Delta_ref", "BR995_5_RC9940_total_abs"],
        "role": "reference/boundary/symplectic bound row schema",
    },
    {
        "source_id": "SRC1797_11_995_map",
        "source_key": "995_delta_ref_symp_map",
        "source_path": RESIDUALS / "P8_Y5_R10_995_DELTA_REF_SYMP_MAP.csv",
        "needles": ["MAP995_0_reference", "MAP995_3_no_cancellation_total"],
        "role": "maps Delta_ref, Delta_symp and B_zero_flux into the RC994_0 pack",
    },
    {
        "source_id": "SRC1797_12_996_input_pack",
        "source_key": "996_source_bound_input_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_996_RC9940_SOURCE_BOUND_INPUT_PACK.csv",
        "needles": ["SBI996_0_Delta_ref", "SBI996_5_RC9940_total_abs"],
        "role": "claim requirements for reference/boundary/symplectic source bounds",
    },
    {
        "source_id": "SRC1797_13_997_delta_ref_template",
        "source_key": "997_delta_ref_template",
        "source_path": RESIDUALS / "P8_Y5_R10_997_DELTA_REF_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["DRS997_0_claim_ready_schema", "DRS997_3_no_cancellation_guard"],
        "role": "Delta_ref source row template and derivative vector sidecar",
    },
    {
        "source_id": "SRC1797_14_997_mhref_guard",
        "source_key": "997_mhref_guard",
        "source_path": RESIDUALS / "P8_Y5_R10_997_MHREF_DENOMINATOR_GUARD.csv",
        "needles": ["MHG997_0_positive_denominator", "MHG997_2_not_orbital_import"],
        "role": "positive same-frame M_H_ref denominator guard",
    },
    {
        "source_id": "SRC1797_15_1007_schema",
        "source_key": "1007_symplectic_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv",
        "needles": ["SRS1007_0_integrability_formula", "SRS1007_3_no_fitted_reference"],
        "role": "full integrability formula and shortcut refusals",
    },
    {
        "source_id": "SRC1797_16_1007_audit",
        "source_key": "1007_Htau_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1007_HTAU_INTEGRABILITY_THEOREM_AUDIT.csv",
        "needles": ["HTA1007_1_parent_theta_Qtau", "HTA1007_6_integrability_verdict"],
        "role": "H_tau integrability theorem audit keeps parent current owner blocked",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_SOURCE_REGISTER.csv",
    "zero_proof_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_DELTA_INTEGRABILITY_ZERO_PROOF_ATTEMPT.csv",
    "source_acquisition_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_SOURCE_ACQUISITION_MATRIX.csv",
    "bound_row_candidate": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_DELTA_INTEGRABILITY_BOUND_ROW_CANDIDATE.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1797_VALIDATION.csv",
}

DOC_PATH = ROOT / "1797-Y5-R2FR-Delta-integrability-source-acquisition-or-bound-row.md"


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


def zero_proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_0_parent_Htau_one_form",
            "target": "delta_H_tau_nonintegrable_over_MH=0",
            "required_zero_condition": "alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref is an exact one-form on the allowed local branch",
            "current_evidence": "HFR1733_0 defines alpha_tau but Theta_total/Q_tau^MTS remain missing or component-only",
            "current_status": "ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_THETA_TOTAL;MISSING_Q_TAU_MTS;MISSING_VARIATION_DOMAIN;MISSING_M_H_REF",
            "source_paths": src("1733_htau_first_row_schema", "1733_theta_qtau_component_rows", "1733_theta_qtau_owner_audit", "993_deltaH_curl_schema"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_1_fixed_reference",
            "target": "Delta_ref_over_MH=0",
            "required_zero_condition": "H_ref is fixed before readout and derivative-silent under source, radius, time, frame and lambda changes",
            "current_evidence": "DRS997 rows define the required derivative sidecar but B_ref rule, Delta_ref value and M_H_ref are missing",
            "current_status": "ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_BREF_RULE;MISSING_DELTA_REF_VALUE;MISSING_DERIVATIVE_VECTOR;MISSING_M_H_REF",
            "source_paths": src("997_delta_ref_template", "997_mhref_guard", "995_residual_bound_row_schema", "996_source_bound_input_pack"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_2_boundary_relative_class",
            "target": "B_zero_flux_over_MH=0",
            "required_zero_condition": "boundary improvement lives in a fixed relative class with zero linking-sphere flux",
            "current_evidence": "MAP995_2 and SBI996_1 give the row contract but no primitive/class theorem or flux profile",
            "current_status": "ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_BOUNDARY_PRIMITIVE;MISSING_RELATIVE_CLASS_RULE;MISSING_FLUX_PROFILE;MISSING_M_H_REF",
            "source_paths": src("995_delta_ref_symp_map", "996_source_bound_input_pack", "995_residual_bound_row_schema"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_3_symplectic_boundary_silence",
            "target": "Delta_symp_over_MH=0",
            "required_zero_condition": "extra-sector/projector/boundary symplectic current has zero pullback on the local branch boundary",
            "current_evidence": "SRS1007 and BR995_1 identify Delta_symp, but theta/B_ref/projector boundary terms are not extracted",
            "current_status": "ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_OMEGA_TOTAL;MISSING_THETA_RULE;MISSING_PROJECTOR_RULE;MISSING_BOUNDARY_CONDITION;MISSING_M_H_REF",
            "source_paths": src("1007_symplectic_schema", "1007_Htau_audit", "995_residual_bound_row_schema", "996_source_bound_input_pack"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_4_tau_MHref_lock",
            "target": "tau_MHref_denominator_lock=true",
            "required_zero_condition": "one observed tau/coframe/frame and positive M_H_ref are used by source, charge, reference and readout",
            "current_evidence": "HMS1732_0 and MHG997 identify the guard, but M_H_ref, tau id and source frame are missing",
            "current_status": "ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_STABLE_MH_REF;MISSING_TAU_ID;MISSING_COFRAME_FRAME_LOCK;MISSING_NOT_ORBITAL_DENOMINATOR_SOURCE",
            "source_paths": src("1732_htau_mhref_source_rows", "997_mhref_guard"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "ZP1797_5_verdict",
            "target": "Delta_integrability_over_MH=0",
            "required_zero_condition": "ZP1797_0 through ZP1797_4 all close in one parent branch",
            "current_evidence": "every required sub-input is source-mapped but none is theorem-zero or finite source-backed",
            "current_status": "DELTA_INTEGRABILITY_ZERO_PROOF_NOT_CLOSED",
            "blocking_gap": "MISSING_PARENT_CURRENT_OWNER_AND_REFERENCE_BOUND_PACK",
            "source_paths": src("1796_first_delta_integrability_row", "1007_symplectic_schema"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def source_acquisition_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "AQR1797_0_delta_H_tau_nonintegrable",
            "target_quantity": "delta_H_tau_nonintegrable_over_MH",
            "canonical_formula": "(|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref",
            "required_payload": "Theta_total;Q_tau^MTS;omega_total;allowed_variation_pair;boundary_conditions;positive_M_H_ref;source_path;equation_ref",
            "best_source_candidates": src("1733_htau_first_row_schema", "1733_theta_qtau_component_rows", "1733_theta_qtau_owner_audit", "993_deltaH_curl_schema", "994_deltaH_no_cancellation"),
            "current_payload": "MISSING_THETA_TOTAL;MISSING_Q_TAU_MTS;MISSING_OMEGA_TOTAL;MISSING_FIELD_VARIATION_PAIR;MISSING_M_H_REF",
            "source_status": "SOURCE_MAPPED_NOT_FILLED",
            "acceptance_rule": "all curl components theorem-zero or source-backed numeric with same units and no cancellation",
            "recommended_next_move": "derive parent Theta_total/Q_tau^MTS owner or emit component rows I_X,I_projector,I_boundary,I_ref,I_tau,I_surface,I_Dq",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "AQR1797_1_Delta_ref",
            "target_quantity": "Delta_ref_over_MH",
            "canonical_formula": "abs(H_ref[S,tau]-H_ref[fixed_branch])/M_H_ref",
            "required_payload": "H_ref_rule;fixed_branch_id;surface_pair;tau_id;derivative_vector;positive_M_H_ref;source_path;equation_ref",
            "best_source_candidates": src("997_delta_ref_template", "997_mhref_guard", "995_residual_bound_row_schema", "996_source_bound_input_pack"),
            "current_payload": "MISSING_BREF_RULE;MISSING_DELTA_REF_VALUE;MISSING_DERIVATIVE_VECTOR;MISSING_M_H_REF",
            "source_status": "SOURCE_MAPPED_NOT_FILLED",
            "acceptance_rule": "Delta_ref numeric finite same-frame ratio or theorem_zero=true plus source/r/t/frame/lambda derivative sidecar",
            "recommended_next_move": "derive fixed branch selector before readout or source Delta_ref derivative vector",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "AQR1797_2_B_zero_flux",
            "target_quantity": "B_zero_flux_over_MH",
            "canonical_formula": "abs(int_S2 B_imp - int_S1 B_imp)/M_H_ref",
            "required_payload": "boundary_primitive;relative_class_rule;surface_pair;flux_profile;positive_M_H_ref;source_path;equation_ref",
            "best_source_candidates": src("995_delta_ref_symp_map", "996_source_bound_input_pack", "995_residual_bound_row_schema"),
            "current_payload": "MISSING_BOUNDARY_PRIMITIVE;MISSING_RELATIVE_CLASS_ZERO;MISSING_FLUX_PROFILE;MISSING_M_H_REF",
            "source_status": "SOURCE_MAPPED_NOT_FILLED",
            "acceptance_rule": "relative class theorem-zero or sourced flux profile with dimensionless bound and no MISSING markers",
            "recommended_next_move": "construct relative boundary class certificate or retain finite boundary flux row",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "AQR1797_3_Delta_symp",
            "target_quantity": "Delta_symp_over_MH",
            "canonical_formula": "abs(int_boundary omega_extra(delta Phi,L_tau Phi))/M_H_ref",
            "required_payload": "omega_total;Theta_rule;B_ref_rule;projector_rule;boundary_condition;positive_M_H_ref;source_path;equation_ref",
            "best_source_candidates": src("1007_symplectic_schema", "1007_Htau_audit", "995_residual_bound_row_schema", "996_source_bound_input_pack"),
            "current_payload": "MISSING_OMEGA_TOTAL;MISSING_THETA_RULE;MISSING_BREF_RULE;MISSING_PROJECTOR_RULE;MISSING_BOUNDARY_CONDITION;MISSING_M_H_REF",
            "source_status": "SOURCE_MAPPED_NOT_FILLED",
            "acceptance_rule": "theta/B_ref/projector boundary terms all theorem-zero or numeric, sourced, same-frame",
            "recommended_next_move": "derive extra-sector omega pullback silence or source Delta_symp boundary value",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "AQR1797_4_tau_MHref_lock",
            "target_quantity": "tau_MHref_denominator_lock",
            "canonical_formula": "tau_source=tau_charge=tau_MHref=tau_readout and M_H_ref>0",
            "required_payload": "tau_id;observed_coframe;source_frame;charge_frame;positive_M_H_ref;not_orbital_import;source_path",
            "best_source_candidates": src("1732_htau_mhref_source_rows", "997_mhref_guard"),
            "current_payload": "MISSING_TAU_ID;MISSING_OBSERVED_COFRAME;MISSING_SOURCE_FRAME;MISSING_STABLE_MH_REF",
            "source_status": "SOURCE_MAPPED_NOT_FILLED",
            "acceptance_rule": "positive same-frame Hamiltonian/source denominator; GM_orbit cannot be substituted before source equality",
            "recommended_next_move": "derive same observed-time/coframe denominator certificate",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bound_row_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "DIB1797_0_candidate_formula",
            "target": "Delta_integrability_over_MH",
            "formula": "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_ref_over_MH)+abs(B_zero_flux_over_MH)+abs(Delta_symp_over_MH)",
            "delta_H_tau_nonintegrable_over_MH": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "Delta_ref_over_MH": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "B_zero_flux_over_MH": "MISSING_BOUNDARY_FLUX_NUMERIC_OR_THEOREM_ZERO",
            "Delta_symp_over_MH": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "M_H_ref": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "dimensionless_ratio_to_M_H_ref",
            "source_paths": src("1796_first_delta_integrability_row", "1007_symplectic_schema", "997_delta_ref_template", "996_source_bound_input_pack"),
            "bound_value": "NOT_COMPUTED",
            "status": "REJECT_CURRENT_BOUND_ROW",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "candidate_id": "DIB1797_1_theorem_zero_switch",
            "target": "Delta_integrability_zero_switch",
            "formula": "theorem_zero=true iff parent-signed H_tau integrability, fixed reference, boundary/symplectic silence and tau/MHref lock all pass",
            "delta_H_tau_nonintegrable_over_MH": "NOT_ZERO_PROVED",
            "Delta_ref_over_MH": "NOT_ZERO_PROVED",
            "B_zero_flux_over_MH": "NOT_ZERO_PROVED",
            "Delta_symp_over_MH": "NOT_ZERO_PROVED",
            "M_H_ref": "MISSING_SAME_FRAME_POSITIVE_MHREF",
            "units": "gate",
            "source_paths": src("1007_symplectic_schema", "1007_Htau_audit", "1796_first_delta_integrability_row"),
            "bound_value": "FALSE",
            "status": "ZERO_SWITCH_REJECTED",
            "accepted_for_scoring": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AG1797_0_source_paths",
            "gate": "all source candidate paths exist",
            "current_status": "PASS_SOURCE_PATHS_EXIST",
            "reason": "1797 maps each input to existing source files",
            "gate_pass": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AG1797_1_numeric_or_zero_payload",
            "gate": "each input is theorem-zero or numeric finite with units",
            "current_status": "FAIL_MISSING_PAYLOADS",
            "reason": "each target still contains MISSING_* values",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AG1797_2_same_frame_denominator",
            "gate": "positive same-frame M_H_ref and tau/coframe lock",
            "current_status": "FAIL_MISSING_MHREF_TAU_LOCK",
            "reason": "M_H_ref and observed-time/coframe certificate are absent",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AG1797_3_no_cancellation",
            "gate": "absolute envelope with no fitted reference or cancellation",
            "current_status": "POLICY_PASS_VALUES_MISSING",
            "reason": "policy is installed, but no scored values exist",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AG1797_4_verdict",
            "gate": "Delta_integrability row claim readiness",
            "current_status": "DELTA_INTEGRABILITY_BOUND_ROW_NOT_READY",
            "reason": "source acquisition succeeds as plumbing, not as physics closure",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1797_0_exactness_failure",
            "countermodel": "alpha_tau is not exact because extra/projector/boundary/current terms have nonzero field-space curl",
            "survives_current_constraints": True,
            "why_survives": "Theta_total/Q_tau^MTS and omega_total are not extracted from one parent action",
            "what_kills_it": "parent current owner plus curl component zero theorem or finite bound rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1797_1_reference_knob",
            "countermodel": "Delta_ref is adjusted by branch/reference/counterterm choice after readout",
            "survives_current_constraints": True,
            "why_survives": "fixed branch selector and derivative sidecar are missing",
            "what_kills_it": "pre-readout reference superselection certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1797_2_boundary_class_flux",
            "countermodel": "relative boundary class carries finite linking-sphere flux",
            "survives_current_constraints": True,
            "why_survives": "boundary primitive and relative class zero theorem are not supplied",
            "what_kills_it": "relative cohomology/no-flux certificate or source-backed flux bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1797_3_symplectic_tail",
            "countermodel": "extra-sector or projector symplectic tail changes the Hamiltonian mass",
            "survives_current_constraints": True,
            "why_survives": "extra omega/projector boundary pullback is not zero-proved",
            "what_kills_it": "presymplectic degeneracy/null proof for retained vertical directions",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1797_4_denominator_mix",
            "countermodel": "a charge/reference from one tau frame is divided by a mass/readout from another",
            "survives_current_constraints": True,
            "why_survives": "positive same-frame M_H_ref and tau/coframe lock remain missing",
            "what_kills_it": "single observed-time denominator certificate",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1797_0_zero_proof",
            "claim": "Delta_integrability=0",
            "status": "BLOCKED",
            "reason": "ZP1797_5 verdict is DELTA_INTEGRABILITY_ZERO_PROOF_NOT_CLOSED",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "claim_id": "CL1797_1_finite_bound",
            "claim": "Delta_integrability finite bound row can be scored",
            "status": "BLOCKED",
            "reason": "DIB1797 rows contain MISSING_* payloads and are rejected",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1797_2_Htau_integrability",
            "claim": "H_tau is an integrable fixed-reference Hamiltonian source charge",
            "status": "BLOCKED",
            "reason": "parent Theta/Q_tau owner and fixed reference remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1797_3_source_normalized_Newton",
            "claim": "source-normalized Newton/local-GR reduction follows",
            "status": "BLOCKED",
            "reason": "first Delta_Hsrc component is not zero or bounded",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1797_0_result",
            "decision": "SOURCE_ACQUISITION_MATRIX_BUILT",
            "reason": "all five Delta_integrability sub-inputs now point to existing source candidates and acceptance rules",
            "next_action": "use matrix rather than hunting randomly through older checkpoints",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1797_1_zero_proof",
            "decision": "ZERO_PROOF_NOT_CLOSED",
            "reason": "no sub-input is theorem-zero in the current corpus",
            "next_action": "do not claim Delta_integrability=0",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1797_2_bound_row",
            "decision": "BOUND_ROW_REJECTED_NONCLAIM",
            "reason": "source paths exist but payloads remain MISSING and M_H_ref is not locked",
            "next_action": "do not score the row until payloads are real",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1797_3_next",
            "decision": "PARENT_THETA_QTAU_OWNER_OR_DELTAH_CURL_COMPONENT_PACK_NEXT",
            "reason": "delta_H_tau_nonintegrable is the highest-leverage blocker because it owns Theta_total, Q_tau, omega_total and the allowed variation domain",
            "next_action": "build 1798 to derive parent Theta/Q_tau current owner or emit the I_X/I_projector/I_boundary/I_ref/I_tau/I_surface/I_Dq component pack",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1797_0_primary",
            "next_target": "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md",
            "script": "scripts/Y5_R2FR_parent_Theta_Qtau_current_owner_or_deltaH_curl_component_pack.py",
            "objective": "try to derive the parent Theta_total/Q_tau^MTS current owner; if not, emit strict deltaH curl component rows for I_X,I_projector,I_boundary,I_ref,I_tau,I_surface,I_Dq",
            "selection_status": "selected",
            "success_condition": "parent current owner closes, or every curl component is source-backed/theorem-zero with common units and positive M_H_ref",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1797_1_parallel_Delta_ref",
            "next_target": "1798b-Y5-R2FR-fixed-reference-branch-selector-or-Delta-ref-derivative-vector.md",
            "script": "scripts/Y5_R2FR_fixed_reference_branch_selector_or_Delta_ref_derivative_vector.py",
            "objective": "derive fixed pre-readout H_ref branch selector or fill Delta_ref derivative sidecar",
            "selection_status": "held_parallel",
            "success_condition": "Delta_ref theorem-zero or source-backed finite derivative-vector row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1797_2_parallel_boundary_symp",
            "next_target": "1798c-Y5-R2FR-relative-boundary-class-and-symplectic-flux-zero-or-bound.md",
            "script": "scripts/Y5_R2FR_relative_boundary_class_and_symplectic_flux_zero_or_bound.py",
            "objective": "derive B_zero_flux and Delta_symp silence or source finite boundary/symplectic flux rows",
            "selection_status": "held_parallel",
            "success_condition": "relative boundary and symplectic flux rows become theorem-zero or source-backed finite",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "zero_proof_attempt": zero_proof_attempt_rows(),
        "source_acquisition_matrix": source_acquisition_matrix_rows(),
        "bound_row_candidate": bound_row_candidate_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1797_{key.upper()}.csv")


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
        "theorem_zero",
        "valid_prediction_row",
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
        "theorem_zero",
        "valid_prediction_row",
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
        if not (RAB_QUEUE / f"JR1797_{key.upper()}.csv").exists():
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
        ("VAL1797_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1797_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1797_2_zero_proof_not_closed",
            any(
                row["proof_id"] == "ZP1797_5_verdict"
                and row["current_status"] == "DELTA_INTEGRABILITY_ZERO_PROOF_NOT_CLOSED"
                for row in rows_map["zero_proof_attempt"]
            )
            and all(not boolish(row["theorem_zero"]) and not boolish(row["valid_for_claim"]) for row in rows_map["zero_proof_attempt"]),
            "Delta_integrability zero proof remains open",
        ),
        (
            "VAL1797_3_acquisition_matrix_mapped",
            len(rows_map["source_acquisition_matrix"]) == 5
            and all(row["source_status"] == "SOURCE_MAPPED_NOT_FILLED" for row in rows_map["source_acquisition_matrix"]),
            "five source acquisition rows are mapped but not filled",
        ),
        (
            "VAL1797_4_bound_row_rejected",
            all(row["status"] in {"REJECT_CURRENT_BOUND_ROW", "ZERO_SWITCH_REJECTED"} for row in rows_map["bound_row_candidate"])
            and all(not boolish(row["accepted_for_scoring"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["bound_row_candidate"]),
            "Delta_integrability bound row is rejected",
        ),
        (
            "VAL1797_5_acceptance_gate_blocks",
            any(
                row["gate_id"] == "AG1797_4_verdict"
                and row["current_status"] == "DELTA_INTEGRABILITY_BOUND_ROW_NOT_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks scoring",
        ),
        (
            "VAL1797_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1797_7_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1797_8_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1797_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1797_10_decision_next",
            any(
                row["decision_id"] == "DEC1797_3_next"
                and row["decision"] == "PARENT_THETA_QTAU_OWNER_OR_DELTAH_CURL_COMPONENT_PACK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects parent Theta/Q_tau owner or curl component pack next",
        ),
        (
            "VAL1797_11_next_selected",
            any(row["route_id"] == "NEXT1797_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1797_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1797 CSVs parse"),
        ("VAL1797_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1797_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1797_15_formalization_untouched", formalization_untouched(), "no 1797 outputs found under formalization-workbench"),
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
            "check_id": "VAL1797_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1797 Delta_integrability source acquisition or bound row checkpoint",
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
            "# 1797 - Y5/R2FR Delta-Integrability Source Acquisition or Bound Row",
            "",
            "## Verdict",
            "",
            "1797 does the source-acquisition pass for the first `Delta_Hsrc` component. The useful result is not a physics claim; it is a clean routing map for the five missing pieces of `Delta_integrability`.",
            "",
            "The zero route still does not close. The finite-bound route also cannot be scored yet. But every missing slot now has a best source candidate set, an acceptance rule, and a recommended next move.",
            "",
            "The active nonclaim identity remains:",
            "",
            "`Delta_integrability/M_H_ref = |delta_H_tau_nonintegrable|/M_H_ref + |Delta_ref|/M_H_ref + |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref`.",
            "",
            "**Claim ceiling:** no `Delta_integrability=0`, no finite `Delta_integrability` score, no integrable `H_tau`, no source-normalized Newton/local-GR claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1797.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Zero-Proof Attempt",
            markdown_table(rows_map["zero_proof_attempt"], ["proof_id", "target", "required_zero_condition", "current_status", "blocking_gap", "theorem_zero", "valid_for_claim"]),
            "",
            "## Source Acquisition Matrix",
            markdown_table(rows_map["source_acquisition_matrix"], ["input_id", "target_quantity", "canonical_formula", "current_payload", "source_status", "recommended_next_move", "score_ready", "valid_for_claim"]),
            "",
            "## Bound Row Candidate",
            markdown_table(rows_map["bound_row_candidate"], ["candidate_id", "target", "formula", "bound_value", "status", "accepted_for_scoring", "valid_prediction_row", "valid_for_claim"]),
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
            "The best next shot is not to chase all five slots at once. The parent `Theta_total/Q_tau^MTS` owner is the leverage point: it controls `delta_H_tau`, tells us which symplectic tails are real, and stops us from importing GR charge machinery before the MTS parent branch earns it.",
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
    print(f"1797 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
