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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1729"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1729 - Tobs Delta Tau Operator Norm Or Source Current Silence"
UTC = datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def false_text() -> str:
    return "False"


SOURCES = [
    {
        "source_id": "SRC1729_0_1728_doc",
        "source_key": "1728_doc",
        "source_path": ROOT / "1728-Y5-R2FR-local-stationary-quasilocal-generator-certificate-or-delta-tau-bound-coefficient.md",
        "needles": ["NEXT1728_0_primary", "T_obs operator norm"],
    },
    {
        "source_id": "SRC1729_1_1728_next",
        "source_key": "1728_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_NEXT_TARGET.csv",
        "needles": ["1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md", "selected"],
    },
    {
        "source_id": "SRC1729_2_1728_coefficient",
        "source_key": "1728_C_Tobs_tau_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv",
        "needles": ["DTC1728_0_C_Tobs_tau_primary", "MISSING_TOBS_OPERATOR_NORM"],
    },
    {
        "source_id": "SRC1729_3_1727_delta_tau",
        "source_key": "1727_delta_tau_source_current",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
        "needles": ["DTAU1727_1_source_current_delta_tau", "MISSING_TOBS_OPERATOR_NORM"],
    },
    {
        "source_id": "SRC1729_4_1726_Rtau_schema",
        "source_key": "1726_Rtau_source_current_bound",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv",
        "needles": ["RTAU1726_1_source_current_bound", "T_obs_operator_norm"],
    },
    {
        "source_id": "SRC1729_5_1720_doc",
        "source_key": "1720_JH_definition",
        "source_path": ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
        "needles": ["J_H[tau]=star(T_obs(tau,.))", "MISSING_NORM_CONVENTION"],
    },
    {
        "source_id": "SRC1729_6_1720_JH_row",
        "source_key": "1720_JH_norm_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
    {
        "source_id": "SRC1729_7_449_Ward",
        "source_key": "449_Ward_source_current",
        "source_path": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
        "needles": ["conditional_Hilbert_source_current_theorem", "Ward_conservation_limit"],
    },
    {
        "source_id": "SRC1729_8_1726_observed_generator",
        "source_key": "1726_observed_time_generator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_OBSERVED_TIME_GENERATOR_AUDIT.csv",
        "needles": ["OTG1726_6_verdict", "OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED"],
    },
    {
        "source_id": "SRC1729_9_1726_validation",
        "source_key": "1726_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1726_VALIDATION.csv",
        "needles": ["VAL1726_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1729_10_1728_validation",
        "source_key": "1728_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1728_VALIDATION.csv",
        "needles": ["VAL1728_OVERALL", "PASS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_SOURCE_REGISTER.csv",
    "silence_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_SOURCE_CURRENT_SILENCE_AUDIT.csv",
    "operator_norm_law": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_TOBS_OPERATOR_NORM_LAW.csv",
    "coefficient_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1729_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1729_VALIDATION.csv",
}


COPY_MAP = {
    "silence_audit": "R2FR_1729_SOURCE_CURRENT_SILENCE_AUDIT.csv",
    "operator_norm_law": "R2FR_1729_TOBS_OPERATOR_NORM_LAW.csv",
    "coefficient_rows": "R2FR_1729_C_TOBS_TAU_BOUND_ROWS.csv",
    "runner_refusal": "R2FR_1729_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1729_DECISION_LEDGER.csv",
    "next_target": "R2FR_1729_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1729_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = source_path.read_text(encoding="utf-8", errors="replace") if source_path.exists() else ""
        needles_present = all(needle in source_text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(source_path),
                "exists": bool_text(source_path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": bool_text(needles_present),
                "checked_utc": UTC,
            }
        )
    return rows


def silence_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_0_fixed_variation_silence",
            "silence_route": "fixed observed time variation",
            "mathematical_condition": "delta tau_obs=0 in the allowed parent tangent space",
            "current_status": "FIXED_VARIATION_NOT_PARENT_SIGNED",
            "blocking_gap": "1726/1727 keep boundary-clock/reference superselection and fixed variation unsigned",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_1_vacuum_support_silence",
            "silence_route": "vacuum annulus support split",
            "mathematical_condition": "T_obs|A_ext=0 or supp(T_obs) cap A_ext is empty, with boundary flux handled separately",
            "current_status": "SUPPORT_SPLIT_NOT_DECLARED",
            "blocking_gap": "A_ext is still a template and the source worldtube/vacuum annulus split is not parent-signed",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_2_kernel_silence",
            "silence_route": "delta tau lies in the stress-kernel",
            "mathematical_condition": "T_obs(delta tau_obs, .)=0 pointwise or in the declared current norm",
            "current_status": "KERNEL_CONDITION_NOT_DERIVED",
            "blocking_gap": "ordinary matter stress generically has no reason to annihilate an arbitrary moving time generator",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_3_gauge_vertical_silence",
            "silence_route": "pure gauge/vertical tau displacement",
            "mathematical_condition": "delta tau_obs is a gauge representative displacement that leaves e_obs, S_matter and T_obs unchanged",
            "current_status": "VERTICAL_TAU_GAUGE_ROUTE_UNSIGNED",
            "blocking_gap": "vertical quotient clauses exist elsewhere but do not sign the observed time-generator motion",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_4_integral_cancellation_rejected",
            "silence_route": "integral cancellation only",
            "mathematical_condition": "int_A star(T_obs(delta tau,.))=0 without a norm/kernel theorem",
            "current_status": "REJECTED_AS_NORM_SILENCE",
            "blocking_gap": "a cancellation of one integral does not bound the current norm needed by R_tau_frame",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SCS1729_5_verdict",
            "silence_route": "source-current moving-tau silence verdict",
            "mathematical_condition": "one of fixed-tau, vacuum support, stress-kernel, or gauge silence must be parent-signed",
            "current_status": "SOURCE_CURRENT_SILENCE_NOT_SIGNED",
            "blocking_gap": "no current source proves star(T_obs(delta tau_obs,.)) vanishes for the active local branch",
            "zero_theorem_signed": false_text(),
            "valid_for_claim": false_text(),
        },
    ]


def operator_norm_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_0_linear_map",
            "law_piece": "moving-tau source-current map",
            "formula": "L_Tobs^A[delta tau] := star_A(T_obs(delta tau,.))",
            "assumptions": "fixed T_obs and observed volume form while isolating the tau-variation term",
            "current_status": "DERIVED_BOUND_FORM",
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_1_operator_coefficient",
            "law_piece": "coefficient definition",
            "formula": "C_Tobs_tau(A_ext,norm) := ||L_Tobs^A||_{B_tau -> J_A}",
            "assumptions": "same A_ext, coframe, Hodge star, tau norm and current norm are declared before scoring",
            "current_status": "DEFINITION_DERIVED_INPUTS_MISSING",
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_2_L2_sup_bound",
            "law_piece": "standard L2/sup conservative bound",
            "formula": "||Delta J_H||_L2(A) <= sup_A ||T_obs||_op ||delta tau_obs||_L2(A)",
            "assumptions": "orthonormal observed coframe or sourced Hodge-star operator factor; no cancellation credit",
            "current_status": "BOUND_TEMPLATE_DERIVED_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_3_L1_sup_bound",
            "law_piece": "standard L1/sup conservative bound",
            "formula": "||Delta J_H||_L1(A) <= sup_A ||T_obs||_op ||delta tau_obs||_L1(A)",
            "assumptions": "same current measure and tau measure; Hodge-star conversion included in coefficient if not isometric",
            "current_status": "BOUND_TEMPLATE_DERIVED_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_4_dimension_rule",
            "law_piece": "units and normalization",
            "formula": "[C_Tobs_tau]=[current norm]/[tau norm], sourced by stress-energy density times Hodge/measure conversion",
            "assumptions": "units cannot be declared until A_ext, volume form, norm type and tau normalization are fixed",
            "current_status": "UNITS_RULE_DERIVED_VALUES_MISSING",
            "valid_for_claim": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "TON1729_5_verdict",
            "law_piece": "operator-norm verdict",
            "formula": "Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B",
            "assumptions": "the law is usable as a nonclaim bound row, not as a local-GR pass",
            "current_status": "BOUND_LAW_READY_COEFFICIENT_NOT_SOURCE_BACKED",
            "valid_for_claim": false_text(),
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    source_paths = [
        str(OUTPUTS["operator_norm_law"]),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv"),
        str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CTT1729_0_C_Tobs_tau_primary",
            "quantity": "C_Tobs_tau",
            "definition": "operator norm of delta tau -> star(T_obs(delta tau,.)) on the declared compact exterior",
            "bound_form": "Delta_JH_delta_tau <= C_Tobs_tau * ||delta tau_obs||_B",
            "required_inputs": "system_id;A_ext;norm_pair;observed_coframe;volume_form;Hodge_star_factor;Tobs_operator_bound;tau_norm;current_norm;units;source_path",
            "current_status": "BOUND_LAW_DERIVED_NUMERIC_INPUTS_MISSING",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_A_EXT;MISSING_NORM_PAIR;MISSING_OBSERVED_COFRAME;MISSING_VOLUME_FORM;MISSING_HODGE_FACTOR;MISSING_TOBS_OPERATOR_BOUND;MISSING_TAU_NORM;MISSING_CURRENT_NORM;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_C_TOBS_TAU",
            "units": "current_norm_per_tau_norm_MISSING",
            "score_ready": false_text(),
            "valid_for_claim": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CTT1729_1_Delta_JH_delta_tau",
            "quantity": "Delta_JH_delta_tau",
            "definition": "source-current residual induced by a moving observed time generator",
            "bound_form": "||star(T_obs(delta tau_obs,.))||_A <= C_Tobs_tau ||delta tau_obs||_B",
            "required_inputs": "C_Tobs_tau;delta_tau_obs_norm;A_ext;B_tau;current_norm;units",
            "current_status": "BOUND_FORM_READY_VALUES_MISSING",
            "missing_inputs": "MISSING_C_TOBS_TAU;MISSING_DELTA_TAU_OBS_NORM;MISSING_A_EXT;MISSING_B_TAU;MISSING_CURRENT_NORM;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_DELTA_JH_DELTA_TAU",
            "units": "current_norm_units_MISSING",
            "score_ready": false_text(),
            "valid_for_claim": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CTT1729_2_Tobs_sup_bound",
            "quantity": "sup_A_norm_Tobs_op",
            "definition": "conservative pointwise operator bound for observed stress on A_ext",
            "bound_form": "C_Tobs_tau <= C_star_measure * sup_A ||T_obs||_op",
            "required_inputs": "Tobs_components_or_energy_density_bound;observed_metric;A_ext;norm_type;Hodge_star_factor;units;source_path",
            "current_status": "SOURCE_ROW_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_TOBS_COMPONENTS_OR_ENERGY_DENSITY_BOUND;MISSING_OBSERVED_METRIC;MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_HODGE_FACTOR;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
            "numeric_value": "MISSING_SUP_TOBS_OP",
            "units": "stress_energy_or_current_conversion_units_MISSING",
            "score_ready": false_text(),
            "valid_for_claim": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CTT1729_3_vacuum_annulus_zero_candidate",
            "quantity": "Z_Tobs_Aext",
            "definition": "candidate theorem-zero flag for the T_obs source current on a vacuum exterior annulus",
            "bound_form": "if T_obs|A_ext=0 and boundary flux is retained elsewhere, then C_Tobs_tau=0 on A_ext only",
            "required_inputs": "source_worldtube;A_ext_excludes_support;Tobs_support_proof;boundary_flux_accounting;units;source_path",
            "current_status": "ZERO_ROUTE_CONDITIONAL_SUPPORT_SPLIT_MISSING",
            "missing_inputs": "MISSING_SOURCE_WORLDTUBE;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_TOBS_SUPPORT_PROOF;MISSING_BOUNDARY_FLUX_ACCOUNTING",
            "source_paths": str(OUTPUTS["silence_audit"]),
            "numeric_value": "MISSING_Z_TOBS_AEXT",
            "units": "boolean_theorem_zero_MISSING",
            "score_ready": false_text(),
            "valid_for_claim": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "CTT1729_4_C_delta_tau_stack_update",
            "quantity": "C_delta_tau_source_stack",
            "definition": "partial source-current piece of the full delta_tau propagation stack",
            "bound_form": "source_piece <= C_Tobs_tau epsilon_delta_tau ||tau_obs||_B",
            "required_inputs": "C_Tobs_tau;epsilon_delta_tau;tau_obs_norm;common_normalization;source_paths;units",
            "current_status": "STACK_LINK_READY_VALUES_MISSING",
            "missing_inputs": "MISSING_C_TOBS_TAU;MISSING_EPSILON_DELTA_TAU;MISSING_TAU_OBS_NORM;MISSING_COMMON_NORMALIZATION;MISSING_UNITS",
            "source_paths": ";".join(source_paths),
            "numeric_value": "MISSING_SOURCE_STACK_VALUE",
            "units": "dimensionless_after_common_normalization_MISSING",
            "score_ready": false_text(),
            "valid_for_claim": false_text(),
            "claim_allowed": false_text(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1729_0_source_current_silence",
            "quantity": "star(T_obs(delta tau_obs,.)) zero theorem",
            "runner_decision": "REFUSE_CLAIM",
            "refusal_reasons": "FIXED_TAU_UNSIGNED;VACUUM_SUPPORT_SPLIT_MISSING;KERNEL_CONDITION_NOT_DERIVED;GAUGE_VERTICAL_TAU_UNSIGNED",
            "accepted_for_scoring": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1729_1_C_Tobs_tau",
            "quantity": "C_Tobs_tau",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "MISSING_A_EXT;MISSING_NORM_PAIR;MISSING_TOBS_OPERATOR_BOUND;MISSING_UNITS;MISSING_SOURCE_VALUE",
            "accepted_for_scoring": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1729_2_Delta_JH_delta_tau",
            "quantity": "Delta_JH_delta_tau",
            "runner_decision": "BOUND_FORM_ONLY_REFUSE_SCORING",
            "refusal_reasons": "MISSING_C_TOBS_TAU;MISSING_DELTA_TAU_OBS_NORM;MISSING_CURRENT_NORM",
            "accepted_for_scoring": false_text(),
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1729_3_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_FIXED_TAU;NO_C_TOBS_TAU_VALUE;NO_MHREF_JH_NDOMAIN_REOPENING;PPN_VECTOR_UNCLEARED",
            "accepted_for_scoring": false_text(),
            "claim_allowed": false_text(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1729_0_zero_proof_status",
            "decision": "do not claim source-current silence",
            "because": "the only clean zero routes are fixed delta tau, vacuum support, stress-kernel, or pure gauge tau motion, and none is parent-signed",
            "next_action": "retain source-current delta_tau residual instead of hiding it",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1729_1_bound_law_progress",
            "decision": "promote the exact operator-norm law as the useful result",
            "because": "Delta_JH_delta_tau is a linear map in delta tau at fixed T_obs and can be bounded without pretending it vanishes",
            "next_action": "source A_ext, norm_pair, Tobs operator bound, Hodge factor and units",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1729_2_best_next",
            "decision": "attack the support-annulus split before numeric stress values",
            "because": "if A_ext is a vacuum exterior annulus the local source-current coefficient may be zero there, but only if boundary mass flux is kept in the Hamiltonian/source-normalization ledger",
            "next_action": "1730 should either prove T_obs|A_ext=0 with flux accounting, or fill the first Tobs norm source row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1729_0_primary",
            "next_target": "1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md",
            "script": "scripts/Y5_R2FR_Tobs_support_annulus_split_or_first_norm_source_row.py",
            "objective": "decide whether the chosen A_ext is a vacuum annulus with T_obs support excluded and boundary flux retained, or fill the first nonclaim Tobs operator-norm source row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1729_1_parallel_delta_tau_norm",
            "next_target": "1730b-Y5-R2FR-delta-tau-norm-value-or-theorem-zero.md",
            "script": "scripts/Y5_R2FR_delta_tau_norm_value_or_theorem_zero.py",
            "objective": "source ||delta tau_obs||_B or prove delta tau_obs=0 from a parent boundary-clock/reference variation class",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1729_2_later_stack_runner",
            "next_target": "1731-Y5-R2FR-CdeltaTau-total-stack-runner.md",
            "script": "scripts/Y5_R2FR_CdeltaTau_total_stack_runner.py",
            "objective": "combine C_Tobs_tau, C_Htau, C_clock_tau and later orbit/WEP terms only after each is sourced or theorem-zero",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1729_0_source_current_silence",
            "claim": "moving-tau source-current term is theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "SCS1729_5 says source-current silence is not signed",
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1729_1_C_Tobs_tau_source_backed",
            "claim": "C_Tobs_tau is numeric/source-backed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "A_ext, norm pair, Tobs operator bound, Hodge factor and units are missing",
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1729_2_Delta_JH_bound",
            "claim": "Delta_JH_delta_tau is bounded for scoring",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "C_Tobs_tau and delta_tau_obs norm are not sourced",
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1729_3_MHref_JH_Ndomain",
            "claim": "M_H_ref/J_H/N_domain can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source-current delta_tau piece is only bound-shaped, not finite or zero",
            "claim_allowed": false_text(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1729_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "fixed tau, source normalization, Hamiltonian reference and PPN residual vector remain open",
            "claim_allowed": false_text(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "silence_audit": silence_audit_rows(),
        "operator_norm_law": operator_norm_law_rows(),
        "coefficient_rows": coefficient_rows(),
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
    def table_cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(table_cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1729_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1729_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "zero_theorem_signed"}
    for rows in rows_map.values():
        for row in rows:
            for field_name, value in row.items():
                if field_name in flag_fields and str(value).lower() != "false":
                    return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1729_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1729_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for candidate_path in FORMALIZATION.rglob("*1729*"):
        path_text = str(candidate_path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if candidate_path.is_file():
            return False
    return True


def coefficient_rows_are_nonclaim(rows: list[dict[str, Any]]) -> bool:
    if len(rows) != 5:
        return False
    for row in rows:
        row_text = ";".join(str(value) for value in row.values())
        if "MISSING_" not in row_text:
            return False
        if row.get("score_ready") != "False" or row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
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
    silence_audit = rows_map["silence_audit"]
    operator_law = rows_map["operator_norm_law"]
    coefficients = rows_map["coefficient_rows"]
    refusals = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for csv_path in generated_csv_paths():
            read_csv(csv_path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1729_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1729_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1729_2_1728_handoff_preserved",
            any(row["source_key"] == "1728_next_target" and row["needles_present"] == "True" for row in source_register),
            "1728 selected Tobs/delta_tau route",
            "1728 handoff missing",
        ),
        check(
            "VAL1729_3_silence_audit_complete",
            {row["silence_route"] for row in silence_audit}
            >= {
                "fixed observed time variation",
                "vacuum annulus support split",
                "delta tau lies in the stress-kernel",
                "pure gauge/vertical tau displacement",
                "integral cancellation only",
                "source-current moving-tau silence verdict",
            },
            "silence audit covers fixed, vacuum, kernel, gauge, cancellation and verdict clauses",
            "silence audit missing required route",
        ),
        check(
            "VAL1729_4_silence_verdict_blocked",
            any(row["audit_id"] == "SCS1729_5_verdict" and row["current_status"] == "SOURCE_CURRENT_SILENCE_NOT_SIGNED" for row in silence_audit),
            "source-current silence remains unsigned",
            "source-current silence verdict missing or opened",
        ),
        check(
            "VAL1729_5_operator_law_present",
            any(row["law_id"] == "TON1729_5_verdict" and "C_Tobs_tau" in row["formula"] for row in operator_law),
            "operator-norm bound law is recorded",
            "operator-norm bound law missing",
        ),
        check(
            "VAL1729_6_primary_coefficient_nonclaim",
            any(row["coefficient_id"] == "CTT1729_0_C_Tobs_tau_primary" and row["valid_for_claim"] == "False" for row in coefficients),
            "primary C_Tobs_tau row exists and is nonclaim",
            "primary C_Tobs_tau row missing or claim-enabled",
        ),
        check(
            "VAL1729_7_coefficients_nonclaim",
            coefficient_rows_are_nonclaim(coefficients),
            "all C_Tobs_tau coefficient rows carry missing markers and remain nonclaim",
            "one or more coefficient rows are claim-enabled or malformed",
        ),
        check(
            "VAL1729_8_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals}
            >= {"star(T_obs(delta tau_obs,.)) zero theorem", "C_Tobs_tau", "Delta_JH_delta_tau", "Newton/local-GR reduction"},
            "runner refusals cover zero theorem, coefficient, residual and local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1729_9_decision_next",
            any(row["decision_id"] == "DEC1729_2_best_next" and "support-annulus" in row["decision"] for row in decisions),
            "decision selects support-annulus split next",
            "decision does not select support-annulus split",
        ),
        check(
            "VAL1729_10_next_selected",
            any(row["route_id"] == "NEXT1729_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1730 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1729_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1729_12_csv_parse", parsed_ok, "all generated 1729 CSVs parse", "one or more generated 1729 CSVs failed to parse"),
        check("VAL1729_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1729_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1729_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1729_16_formalization_untouched", formalization_untouched(), "no 1729 outputs found under formalization-workbench", "1729 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1729_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1729 Tobs/delta_tau operator-norm validation" if overall else "one or more 1729 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1729 tries to kill the moving-`tau` source-current term directly.",
        "- Current result: `star(T_obs(delta tau_obs,.))=0` is **not signed** for current MTS. The clean zero routes are fixed `delta tau_obs=0`, vacuum support, stress-kernel annihilation, or pure-gauge tau motion; none is parent-owned here.",
        "- Useful progress: the fallback is now an exact operator-norm law, `Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B`.",
        "- This means the leak is no longer vague. It has a precise coefficient owner: the stress-energy operator norm on the same compact exterior, norm pair, Hodge/volume convention, and tau normalization.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Derived Bound Shape",
        "At fixed `T_obs` and observed Hodge map, the moving-generator contribution is linear: `L_Tobs^A[delta tau]=star_A(T_obs(delta tau,.))`. Therefore `C_Tobs_tau=||L_Tobs^A||` is the honest coefficient. It may be zero only if the active annulus is vacuum/support-free, the variation is fixed, or `delta tau` lies in the stress-kernel. Otherwise it must be bounded, not hidden.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Source Current Silence Audit",
        markdown_table(rows_map["silence_audit"], ["audit_id", "silence_route", "current_status", "blocking_gap", "zero_theorem_signed", "valid_for_claim"]),
        "",
        "## Tobs Operator Norm Law",
        markdown_table(rows_map["operator_norm_law"], ["law_id", "law_piece", "formula", "current_status", "valid_for_claim"]),
        "",
        "## C Tobs Tau Bound Rows",
        markdown_table(rows_map["coefficient_rows"], ["coefficient_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "1729 is a good little gearbox click. The zero proof did not close, but the missing object is no longer mystical: `C_Tobs_tau` is the exact price of letting `tau_obs` move inside the Hilbert source current. The least-scrutinised next move is not to invent a number, but to decide the support geometry. If the compact exterior really excludes ordinary matter support, we may get a local `T_obs|A_ext=0` result while keeping boundary mass flux elsewhere. If not, the first real stress-energy operator-norm row must be sourced before any local-GR reopening.",
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
    doc_path = ROOT / "1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1729_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1729 validation FAIL")
    print("1729 validation PASS")


if __name__ == "__main__":
    main()
