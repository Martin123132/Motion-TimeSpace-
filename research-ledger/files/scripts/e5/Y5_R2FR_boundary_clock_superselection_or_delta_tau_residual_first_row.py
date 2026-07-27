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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1727"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1727 - Boundary Clock Superselection Or Delta Tau Residual First Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1727_0_1726_doc",
        "source_key": "1726_doc",
        "source_path": ROOT / "1726-Y5-R2FR-observed-time-generator-fixed-variation-or-Rtau-residual-bound.md",
        "needles": ["NEXT1726_0_primary", "boundary-clock/reference superselection"],
    },
    {
        "source_id": "SRC1727_1_1726_next",
        "source_key": "1726_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_NEXT_TARGET.csv",
        "needles": ["1727-Y5-R2FR-boundary-clock-superselection-or-delta-tau-residual-first-row.md", "selected"],
    },
    {
        "source_id": "SRC1727_2_1726_validation",
        "source_key": "1726_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1726_VALIDATION.csv",
        "needles": ["VAL1726_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1727_3_1726_Rtau_schema",
        "source_key": "1726_Rtau_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv",
        "needles": ["RTAU1726_0_vector_schema", "MISSING_TAU_OBS"],
    },
    {
        "source_id": "SRC1727_4_1725_no_lapse_guard",
        "source_key": "1725_no_lapse_guard",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NO_LAPSE_RESCALING_GUARD.csv",
        "needles": ["NLR1725_4_verdict", "NO_LAPSE_RESCALING_GUARD_ACTIVE"],
    },
    {
        "source_id": "SRC1727_5_685_killing_clock",
        "source_key": "685_killing_clock_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        "needles": ["KCG685_4_boundary_reference", "MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS"],
    },
    {
        "source_id": "SRC1727_6_685_tau_contract",
        "source_key": "685_tau_generator_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_3_clock_normalization_route", "clock_product_bound_only"],
    },
    {
        "source_id": "SRC1727_7_664_integrability",
        "source_key": "664_integrability",
        "source_path": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        "needles": ["HCI664_4_time_generator_lock", "delta tau=0"],
    },
    {
        "source_id": "SRC1727_8_boundary_first_row",
        "source_key": "boundary_first_row_status",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["epsilon_boundary_reference_abs", "first_row_unfilled"],
    },
    {
        "source_id": "SRC1727_9_boundary_minimal_contract",
        "source_key": "boundary_minimal_contract",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
        "needles": ["MAC545_2_reference_lock", "reference choice remains a contract"],
    },
    {
        "source_id": "SRC1727_10_boundary_ownership",
        "source_key": "boundary_ownership_audit",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_PARENT_OWNERSHIP_AUDIT.csv",
        "needles": ["POA545_5_denominator", "false"],
    },
    {
        "source_id": "SRC1727_11_boundary_zero_gate",
        "source_key": "boundary_zero_gate_995",
        "source_path": RESIDUALS / "P8_Y5_R10_995_BOUNDARY_REFERENCE_ZERO_THEOREM_GATE.csv",
        "needles": ["ZT995_1_Bref_superselection", "reference lock remains a contract"],
    },
    {
        "source_id": "SRC1727_12_boundary_zero_attempt",
        "source_key": "boundary_zero_attempt",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["BRT543_0_fixed_reference", "not_derived"],
    },
    {
        "source_id": "SRC1727_13_boundary_zero_audit",
        "source_key": "boundary_zero_audit",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv",
        "needles": ["rejected_reference_only", "reference zero is not current MTS evidence"],
    },
    {
        "source_id": "SRC1727_14_546_doc",
        "source_key": "546_boundary_search_doc",
        "source_path": ROOT / "546-Y5-parent-action-boundary-reference-clause-search-or-residual-score.md",
        "needles": ["D546_0_no_MAC545_clause_owned", "ownership_search_negative_for_claim"],
    },
    {
        "source_id": "SRC1727_15_547_doc",
        "source_key": "547_boundary_template_doc",
        "source_path": ROOT / "547-Y5-boundary-reference-residual-input-template-and-local-lock-map.md",
        "needles": ["BRC547_0_reference_lock", "missing_certificate"],
    },
    {
        "source_id": "SRC1727_16_same_coframe",
        "source_key": "same_coframe_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_2_readout_uses_same_e", "conditional_clause_written_not_current_MTS_derived"],
    },
    {
        "source_id": "SRC1727_17_tau_clock_map",
        "source_key": "647_tau_clock_map",
        "source_path": RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
        "needles": ["TAU647_0_time_drift", "defined_product_map"],
    },
    {
        "source_id": "SRC1727_18_clock_doc",
        "source_key": "648_clock_doc",
        "source_path": ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md",
        "needles": ["tau_clock", "not derived"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_SOURCE_REGISTER.csv",
    "superselection_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_FIXED_VARIATION_SUPERSELECTION_THEOREM_ATTEMPT.csv",
    "delta_tau_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1727_VALIDATION.csv",
}


COPY_MAP = {
    "superselection_audit": "R2FR_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv",
    "theorem_attempt": "R2FR_1727_FIXED_VARIATION_SUPERSELECTION_THEOREM_ATTEMPT.csv",
    "delta_tau_row": "R2FR_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
    "runner_refusal": "R2FR_1727_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1727_DECISION_LEDGER.csv",
    "next_target": "R2FR_1727_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1727_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows = []
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


def superselection_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_0_boundary_clock_data",
            "superselection_clause": "boundary clock data",
            "candidate_statement": "A boundary/local clock standard fixes the unit normalization of tau_obs before source, orbit, WEP, or R10 readout.",
            "mathematical_form": "B_clock=(clock_species, worldline/surface, e_obs|_B, N_B[e_obs,tau_obs]=1, units)",
            "current_status": "MISSING_PARENT_BOUNDARY_CLOCK_CLASS",
            "blocking_gap": "clock maps and bounds exist, but no parent clock class selects the Hamiltonian time generator",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_1_reference_class",
            "superselection_clause": "reference subtraction class",
            "candidate_statement": "H_ref/B_ref is fixed by the parent branch and cannot depend on source, surface, time, frame, radius, range, or fit choice.",
            "mathematical_form": "partial_{source,r,t,frame,lambda} H_ref = 0 and partial_{source,r,t,frame,lambda} Delta_ref = 0",
            "current_status": "REFERENCE_SUPERSELECTION_NOT_PARENT_OWNED",
            "blocking_gap": "boundary reference rows remain templates or conditional/failed theorem rows",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_2_fixed_phase_space",
            "superselection_clause": "fixed phase-space boundary class",
            "candidate_statement": "Allowed variations are tangent to a fixed boundary-clock/reference class, not to a moving readout surface.",
            "mathematical_form": "delta B_clock = delta B_ref = delta orientation = 0; delta tau_obs follows from fixed boundary data",
            "current_status": "PHASE_SPACE_CLASS_NOT_DECLARED",
            "blocking_gap": "current corpus has target variation forms but no parent declaration of the allowed boundary-fixed tangent space",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_3_generator_extension",
            "superselection_clause": "bulk extension of tau_obs",
            "candidate_statement": "Boundary normalization plus stationary/quasilocal conditions uniquely extend tau_obs into the local exterior branch.",
            "mathematical_form": "tau_obs|_B fixed; L_tau g_obs=0 or quasilocal lapse/shift evolution equation fixes tau_obs in A_ext",
            "current_status": "GENERATOR_EXTENSION_NOT_SOURCED",
            "blocking_gap": "stationary/Killing or quasilocal certificate is still missing",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_4_delta_tau_zero",
            "superselection_clause": "fixed tau variation",
            "candidate_statement": "If B_clock and B_ref are superselected and the generator extension is unique, then delta tau_obs=0 in source and Hamiltonian variations.",
            "mathematical_form": "tau_obs=F[e_obs|_B,B_clock,B_ref,orientation]; delta B=0 and fixed extension class => delta tau_obs=0",
            "current_status": "DELTA_TAU_ZERO_CONDITIONAL_ONLY",
            "blocking_gap": "the antecedent superselection and uniqueness clauses are not parent-signed",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_5_no_post_readout_clock",
            "superselection_clause": "no readout backfill",
            "candidate_statement": "tau_obs cannot be set by orbital GM, R10, WEP, clock residual minimization, or tau_eff=1 after data are known.",
            "mathematical_form": "partial_{GM_orbit,R10,WEP,fit} tau_obs = 0; tau -> f tau rejected unless f fixed by B_clock before readout",
            "current_status": "GUARD_ACTIVE_SELECTION_MISSING",
            "blocking_gap": "1725 no-lapse guard rejects the cheat but does not supply the parent-selected clock class",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_6_same_frame_clock",
            "superselection_clause": "same coframe clock/source frame",
            "candidate_statement": "The clock standard, source current, Hamiltonian charge, photons, rods, and slow orbits use the same observed coframe.",
            "mathematical_form": "e_source=e_clock=e_photon=e_orbit=e_obs and tau_clock=tau_obs after parent selection",
            "current_status": "SAME_FRAME_CLOCK_CONDITIONAL_ONLY",
            "blocking_gap": "same-coframe clauses are written but not current-MTS derived",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BCS1727_7_verdict",
            "superselection_clause": "boundary-clock/reference verdict",
            "candidate_statement": "The required superselection theorem is exact in shape but not signed by the current corpus.",
            "mathematical_form": "B_clock+B_ref fixed => tau_obs fixed and delta tau_obs=0 remains a conditional route, not a claim",
            "current_status": "BOUNDARY_CLOCK_SUPERSELECTION_NOT_PARENT_SIGNED",
            "blocking_gap": "clock class, reference class, fixed phase space, generator extension and same-frame proof are all unsigned",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BCT1727_0_theorem_statement",
            "claim": "boundary-clock/reference superselection fixes tau_obs and delta tau_obs",
            "mathematical_form": "If C_B=(B_clock,B_ref,orientation,extension_class) is parent-selected and delta C_B=0, then tau_obs=F(C_B) and delta tau_obs=0.",
            "current_result": "EXACT_CONDITIONAL_THEOREM_FORM",
            "why_not_enough": "C_B is not parent-selected for current MTS",
            "activated_residual": "R_delta_tau;R_tau_frame;Delta_ref;Delta_symp",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BCT1727_1_clock_normalization_step",
            "claim": "B_clock fixes lapse normalization",
            "mathematical_form": "N_B[e_obs,tau_obs]=1 and delta N_B=0 for allowed variations",
            "current_result": "CLOCK_NORMALIZATION_NOT_DERIVED",
            "why_not_enough": "clock product bounds are readout constraints, not a parent Hamiltonian time generator",
            "activated_residual": "epsilon_clock_tau",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BCT1727_2_reference_step",
            "claim": "B_ref/H_ref is source-independent",
            "mathematical_form": "partial_{source,r,t,frame,lambda} H_ref=0",
            "current_result": "REFERENCE_LOCK_NOT_DERIVED",
            "why_not_enough": "boundary-reference zero theorem gates remain blocked and first-row status has no claim-valid source/theorem row",
            "activated_residual": "Delta_ref_over_MH;epsilon_Delta_symp_abs",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BCT1727_3_variation_step",
            "claim": "fixed boundary data imply delta tau_obs=0",
            "mathematical_form": "delta tau_obs = D F[C_B] delta C_B = 0 if delta C_B=0",
            "current_result": "FIXED_VARIATION_ROUTE_CONDITIONAL",
            "why_not_enough": "the fixed boundary phase space and unique extension map F are not parent-owned",
            "activated_residual": "R_delta_tau",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BCT1727_4_verdict",
            "claim": "current MTS signs tau_obs and delta tau_obs=0",
            "mathematical_form": "tau_obs=F(C_B), delta tau_obs=0, valid_for_claim=true",
            "current_result": "FAIL_CURRENT_CLAIM",
            "why_not_enough": "all superselection antecedents are unsigned",
            "activated_residual": "delta_tau_first_row_required",
            "valid_for_claim": no(),
        },
    ]


def delta_tau_rows() -> list[dict[str, Any]]:
    source_bundle = ";".join(str(source["source_path"]) for source in SOURCES)
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "DTAU1727_0_delta_tau_first_residual",
            "quantity": "epsilon_delta_tau",
            "definition": "first explicit residual for a moving observed time generator in the local branch",
            "formula": "epsilon_delta_tau := ||delta tau_obs||_B / ||tau_obs||_B",
            "required_inputs": "system_id;tau_obs_id;boundary_clock_class;reference_class;variation_class;norm_type;delta_tau_value_or_bound;units;source_path",
            "current_status": "FIRST_ROW_TEMPLATE_ONLY_NOT_SCORE_READY",
            "missing_inputs": "MISSING_TAU_OBS;MISSING_BOUNDARY_CLOCK_CLASS;MISSING_REFERENCE_CLASS;MISSING_VARIATION_CLASS;MISSING_NORM_TYPE;MISSING_DELTA_TAU_VALUE_OR_THEOREM_ZERO;MISSING_UNITS",
            "source_paths": source_bundle,
            "numeric_value": "MISSING_EPSILON_DELTA_TAU",
            "units": "dimensionless_after_norm_declared",
            "affected_downstream": "J_H[tau];H_tau;M_H_ref;clock_normalization;orbit_readout;WEP_tau;R_tau_frame",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "DTAU1727_1_source_current_delta_tau",
            "quantity": "Delta_JH_delta_tau",
            "definition": "source-current variation term created if delta tau_obs is not zero",
            "formula": "Delta_JH_delta_tau := ||star(T_obs(delta tau_obs,.))||_A",
            "required_inputs": "T_obs_operator_norm;delta_tau_obs;A_ext;current_norm;units",
            "current_status": "BOUND_FORM_ONLY_NOT_SCORE_READY",
            "missing_inputs": "MISSING_TOBS_OPERATOR_NORM;MISSING_DELTA_TAU_OBS;MISSING_A_EXT;MISSING_CURRENT_NORM;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
            "numeric_value": "MISSING_DELTA_JH_DELTA_TAU",
            "units": "current_norm_units_MISSING",
            "affected_downstream": "J_H_total;N_domain;M_H_ref;source-normalization",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "DTAU1727_2_hamiltonian_delta_tau",
            "quantity": "Delta_H_delta_tau",
            "definition": "Hamiltonian charge variation term created if the generator moves",
            "formula": "Delta_H_delta_tau/M_H_ref := |H_{tau+delta_tau}-H_tau|/M_H_ref plus reference/symplectic terms",
            "required_inputs": "C_Htau;delta_tau_obs;M_H_ref;Delta_ref;Delta_symp;units",
            "current_status": "BOUND_FORM_ONLY_NOT_SCORE_READY",
            "missing_inputs": "MISSING_C_HTAU;MISSING_DELTA_TAU_OBS;MISSING_M_H_REF;MISSING_DELTA_REF;MISSING_DELTA_SYMP;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv") + ";" + str(RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"),
            "numeric_value": "MISSING_DELTA_H_DELTA_TAU",
            "units": "dimensionless_after_M_H_ref_MISSING",
            "affected_downstream": "M_H_ref;Qbar;R10;PPN;Newton_local_GR",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "DTAU1727_3_clock_normalization_delta",
            "quantity": "Delta_clock_boundary_tau",
            "definition": "clock-boundary normalization mismatch if the clock class is not superselected",
            "formula": "Delta_clock_boundary_tau := |delta N_B| + |delta ln nu_clock|",
            "required_inputs": "B_clock;clock_pair;tau_obs;delta_tau_obs;clock_normalization_rule;units",
            "current_status": "BOUND_FORM_ONLY_NOT_SCORE_READY",
            "missing_inputs": "MISSING_B_CLOCK;MISSING_CLOCK_NORMALIZATION_RULE;MISSING_TAU_OBS;MISSING_DELTA_TAU_OBS;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv") + ";" + str(ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md"),
            "numeric_value": "MISSING_CLOCK_BOUNDARY_TAU_DELTA",
            "units": "dimensionless_or_fractional_frequency_MISSING",
            "affected_downstream": "clock_tests;alpha_EM;source_charge_clock_comparison",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1727_0_superselection_theorem",
            "quantity": "boundary-clock/reference superselection",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_CLAIM",
            "refusal_reasons": "MISSING_BOUNDARY_CLOCK_CLASS;MISSING_REFERENCE_SUPERSELECTION;MISSING_FIXED_PHASE_SPACE;MISSING_GENERATOR_EXTENSION;MISSING_SAME_FRAME_CLOCK_PROOF",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1727_1_delta_tau_zero",
            "quantity": "delta tau_obs=0",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "SUPERSELECTION_ANTECEDENTS_UNSIGNED;DELTA_TAU_FIRST_ROW_REQUIRED",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1727_2_delta_tau_first_row",
            "quantity": "delta_tau residual first row",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "ROWS_HAVE_MISSING_INPUTS_AND_VALID_FOR_CLAIM_FALSE",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1727_3_MHref_JH_Ndomain",
            "quantity": "M_H_ref/J_H/N_domain reopening",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_DELTA_TAU_ZERO;NO_DELTA_TAU_BOUND;BOUNDARY_REFERENCE_STILL_OPEN;COMMON_NORM_OWNER_STILL_BLOCKED",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1727_4_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_FIXED_TAU;NO_M_H_REF;NO_JH_TOTAL;NO_NDOMAIN;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1727_0_superselection_verdict",
            "decision": "boundary-clock/reference superselection not claimed",
            "because": "clock class, reference class, fixed phase space, generator extension and same-frame clock proof are unsigned",
            "next_action": "do not use delta tau_obs=0 as a theorem-zero input",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1727_1_delta_tau_first_row",
            "decision": "delta_tau residual row opened",
            "because": "a moving time generator creates explicit source-current and Hamiltonian-charge terms",
            "next_action": "source or bound epsilon_delta_tau before reopening M_H_ref/J_H/N_domain",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1727_2_best_next",
            "decision": "try stationary/quasilocal generator certificate next",
            "because": "the boundary class cannot fix tau_obs without an extension/certificate for the local exterior generator",
            "next_action": "derive or source a local stationary/Killing or quasilocal time-flow certificate without using orbital GM",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1727_0_primary",
            "next_target": "1728-Y5-R2FR-local-stationary-quasilocal-generator-certificate-or-delta-tau-bound-coefficient.md",
            "script": "scripts/Y5_R2FR_local_stationary_quasilocal_generator_certificate_or_delta_tau_bound_coefficient.py",
            "objective": "derive/source the local stationary/Killing or quasilocal time-flow certificate that extends boundary clock data to tau_obs, or add the first coefficient needed to bound delta_tau residuals",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1727_1_parallel_reference_lock",
            "next_target": "1728b-Y5-R2FR-Bref-reference-superselection-or-Delta-ref-first-bound.md",
            "script": "scripts/Y5_R2FR_Bref_reference_superselection_or_Delta_ref_first_bound.py",
            "objective": "try to parent-sign H_ref/B_ref source-independence or carry Delta_ref as a finite residual",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1727_2_later_Rtau_numeric",
            "next_target": "1729-Y5-R2FR-Rtau-frame-residual-numeric-bound-intake.md",
            "script": "scripts/Y5_R2FR_Rtau_frame_residual_numeric_bound_intake.py",
            "objective": "fill R_tau_frame constants and sector residuals if theorem-route certificates fail",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1727_0_boundary_clock_superselection",
            "claim": "boundary-clock/reference class fixes tau_obs",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "BCS1727_7 verdict says superselection is not parent-signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1727_1_delta_tau_zero",
            "claim": "delta tau_obs=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "BCT1727 theorem attempt is conditional only and first residual row is open",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1727_2_delta_tau_bound",
            "claim": "epsilon_delta_tau is bounded or theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "DTAU1727 rows are templates with missing values, constants, norms and units",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1727_3_MHref_JH_Ndomain",
            "claim": "M_H_ref/J_H/N_domain can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "fixed tau, boundary reference and common norm owner remain unclosed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1727_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no fixed tau theorem, no source-normalization denominator, no N_domain and no PPN closure",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "superselection_audit": superselection_audit_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "delta_tau_row": delta_tau_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1727_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1727_{key.upper()}.csv")


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


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1727_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1727_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1727*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def delta_rows_have_missing(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        combined = ";".join(str(value) for value in row.values())
        if "MISSING_" not in combined:
            return False
        if row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
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
    audit = rows_map["superselection_audit"]
    theorem = rows_map["theorem_attempt"]
    delta = rows_map["delta_tau_row"]
    refusals = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1727_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1727_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1727_2_1726_handoff_preserved",
            any(row["source_key"] == "1726_next_target" and row["needles_present"] == "True" for row in source_register),
            "1726 selected boundary-clock superselection route",
            "1726 handoff missing",
        ),
        check(
            "VAL1727_3_superselection_audit_complete",
            {row["superselection_clause"] for row in audit} >= {"boundary clock data", "reference subtraction class", "fixed phase-space boundary class", "bulk extension of tau_obs", "fixed tau variation", "no readout backfill", "same coframe clock/source frame"},
            "superselection audit covers clock, reference, phase-space, extension, fixed tau, no-backfill and same-frame clauses",
            "superselection audit missing required clause",
        ),
        check(
            "VAL1727_4_superselection_verdict_blocked",
            any(row["audit_id"] == "BCS1727_7_verdict" and row["current_status"] == "BOUNDARY_CLOCK_SUPERSELECTION_NOT_PARENT_SIGNED" for row in audit),
            "boundary-clock superselection remains blocked",
            "boundary-clock verdict missing or opened",
        ),
        check(
            "VAL1727_5_theorem_attempt_conditional",
            any(row["theorem_id"] == "BCT1727_4_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt explicitly fails current claim",
            "theorem attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1727_6_delta_tau_rows_nonclaim",
            len(delta) == 4 and delta_rows_have_missing(delta),
            "delta_tau residual rows remain nonclaim and carry missing markers",
            "delta_tau rows are incomplete or claim-enabled",
        ),
        check(
            "VAL1727_7_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals} >= {"boundary-clock/reference superselection", "delta tau_obs=0", "delta_tau residual first row", "Newton/local-GR reduction"},
            "runner refusals cover superselection, delta tau, residual row and Newton/local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1727_8_decision_next",
            any(row["decision_id"] == "DEC1727_2_best_next" and "stationary/quasilocal" in row["decision"] for row in decisions),
            "decision selects stationary/quasilocal generator certificate next",
            "decision does not select stationary/quasilocal certificate",
        ),
        check(
            "VAL1727_9_next_selected",
            any(row["route_id"] == "NEXT1727_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1728 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1727_10_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1727_11_csv_parse", parsed_ok, "all generated 1727 CSVs parse", "one or more generated 1727 CSVs failed to parse"),
        check("VAL1727_12_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1727_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1727_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1727_15_formalization_untouched", formalization_untouched(), "no 1727 outputs found under formalization-workbench", "1727 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1727_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1727 boundary-clock superselection validation" if overall else "one or more 1727 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1727 tries the boundary-clock/reference superselection route that 1726 selected.",
        "- The theorem shape is clean: if the parent branch fixes `B_clock`, `B_ref`, orientation, and the time-flow extension class, then `tau_obs` is fixed and `delta tau_obs=0` follows for allowed variations.",
        "- Current result: that superselection class is **not parent-signed**. The corpus has boundary/reference contracts and clock product bounds, not a parent-owned clock/reference class.",
        "- The honest fallback is now opened as `epsilon_delta_tau` plus source-current, Hamiltonian, and clock-boundary residual rows.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, `M_H_ref`, `J_H_total`, `N_domain`, fixed-`tau`, or source-normalization claim is made.",
        "",
        "## Conditional Superselection Theorem",
        "If a parent action supplies a boundary clock class `B_clock`, a reference subtraction class `B_ref`, a fixed boundary phase-space class, a unique stationary/quasilocal extension of `tau_obs`, and one observed coframe for clocks/source/orbits, then `tau_obs=F(B_clock,B_ref,orientation,extension_class)` and `delta tau_obs=0` for allowed variations. Current MTS has the form of the theorem, but not the parent signatures needed to use it as evidence.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Superselection Audit",
        markdown_table(rows_map["superselection_audit"], ["audit_id", "superselection_clause", "current_status", "blocking_gap", "derivation_ready", "valid_for_claim"]),
        "",
        "## Theorem Attempt",
        markdown_table(rows_map["theorem_attempt"], ["theorem_id", "claim", "current_result", "why_not_enough", "activated_residual", "valid_for_claim"]),
        "",
        "## Delta Tau First Residual Row",
        markdown_table(rows_map["delta_tau_row"], ["input_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "1727 does not magically make local GR work, but it tightens the noose around the right object. A fixed observed time generator is not a vibe; it needs a parent-owned boundary clock/reference class. Since that class is not signed, `delta_tau` now becomes an explicit residual rather than a silent assumption. The next best derivation attack is the local stationary/Killing or quasilocal generator certificate, because without a legitimate extension from the boundary class into the local exterior, `tau_obs` is still only a target label.",
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
    doc_path = ROOT / "1727-Y5-R2FR-boundary-clock-superselection-or-delta-tau-residual-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1727_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1727 validation FAIL")
    print("1727 validation PASS")


if __name__ == "__main__":
    main()
