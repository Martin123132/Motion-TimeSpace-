from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1596"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md"

SOURCE_FILES = {
    "1595_doc": ROOT / "1595-Y5-R2FR-first-source-backed-beta-or-action-measure-owner-reopen.md",
    "1595_validation": OUT / "P8_Y5_BRR545_1595_VALIDATION.csv",
    "1595_candidate": OUT / "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv",
    "1595_next_inputs": OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv",
    "1595_next_target": OUT / "P8_Y5_PARENT_QLOC_1595_NEXT_TARGET.csv",
    "1066_tau_contract": OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
    "1066_prior_schema": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
    "1224_finite_weight_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
    "1225_symbolic_tau_formula": OUT / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
    "1225_tau_projection_attempt": OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
    "1482_tau_readiness": OUT / "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv",
    "1083_source_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1078_action_measure": OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
    "1452_common_measure": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1453_current_source": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
}

NEEDLES = {
    "1595_doc": ["abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15", "NEXT_1596"],
    "1595_validation": ["VAL1595_OVERALL", "PASS"],
    "1595_candidate": ["SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor", "BOUND_ANCHOR_ONLY_NO_MTS_PREDICTION"],
    "1595_next_inputs": ["NIR1595_0_tau_WEP", "source tau_WEP/readout kernel"],
    "1595_next_target": ["1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate", "tau_WEP"],
    "1066_tau_contract": ["TWP1066_7_verdict", "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED"],
    "1066_prior_schema": ["DWP1066_3_finite_prior_width", "blocked_by_tau_WEP"],
    "1224_finite_weight_contract": ["FSW1224_2_tau_WEP", "MISSING_LAB_SOURCE_ORBIT_PROJECTION"],
    "1225_symbolic_tau_formula": ["FORM1225_0_tau_WEP_functional", "SYMBOLIC_ONLY_NONCLAIM"],
    "1225_tau_projection_attempt": ["TAU1225_6_verdict", "TAU_WEP_PROJECTION_NOT_DERIVED"],
    "1482_tau_readiness": ["TAU1482_7_numeric_tau", "NOT_EVALUATED"],
    "1083_source_caveat": ["SCG1083_0_profile_weighting", "MISSING_SOURCE_PROFILE_WEIGHTING"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1078_action_measure": ["AM1078_4_verdict", "ACTION_MEASURE_NOT_SIGNED"],
    "1452_common_measure": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1453_current_source": ["CSO1453_7_verdict", "PARTIAL_THEOREM_NOT_CLOSED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1596_SOURCE_REGISTER.csv"
CONTRACTION_LAW = OUT / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv"
TAU_FACTOR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv"
ACTION_LAST_GATE = OUT / "P8_Y5_PARENT_QLOC_1596_ACTION_MEASURE_OWNER_LAST_GATE.csv"
DELTA_W_BOUND_STATUS = OUT / "P8_Y5_PARENT_QLOC_1596_DELTA_W_BOUND_STATUS.csv"
TAU_SOURCE_ACQ = OUT / "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1596_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1596_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1596_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1596_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1596_VALIDATION.csv"

COPY_TARGETS = {
    CONTRACTION_LAW: [
        QUARANTINE / "TAU_WEP_CONTRACTION_LAW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_WEP_contraction_law_nonclaim_1596.csv",
    ],
    TAU_FACTOR_AUDIT: [
        QUARANTINE / "TAU_FACTOR_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_factor_audit_nonclaim_1596.csv",
    ],
    ACTION_LAST_GATE: [
        QUARANTINE / "ACTION_MEASURE_OWNER_LAST_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_measure_owner_last_gate_nonclaim_1596.csv",
    ],
    DELTA_W_BOUND_STATUS: [
        QUARANTINE / "DELTA_W_BOUND_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_delta_w_bound_status_nonclaim_1596.csv",
    ],
    TAU_SOURCE_ACQ: [
        QUARANTINE / "TAU_SOURCE_ACQUISITION_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_tau_source_acquisition_rows_nonclaim_1596.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1596.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1596_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1596_tau_projection_or_action_measure_gate_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def contraction_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "law_id": "TCL1596_0_linearized_observable",
            "object": "MICROSCOPE Ti/Pt Eotvos channel",
            "statement": "eta_TiPt = Delta_w_TiPt * tau_WEP + O((Delta_w_TiPt*tau_WEP)^2) in the weak finite-source branch",
            "derivation_status": "CONDITIONAL_LINEAR_CONTRACTION_DERIVED",
            "conditions": "same parent branch; weak residual; absolute-product guard; no measured-G absorption; no signed cancellation model",
            "source": "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv:SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "law_id": "TCL1596_1_product_bound",
            "object": "P_WEP_relative_source_weight",
            "statement": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "derivation_status": "SOURCE_BACKED_PRODUCT_BOUND_FROM_1595",
            "conditions": "MICROSCOPE bound anchor only; tau_WEP not evaluated; Delta_w_TiPt not individually bounded",
            "source": "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv:SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "law_id": "TCL1596_2_delta_w_amplitude_law",
            "object": "Delta_w_TiPt",
            "statement": "if abs(tau_WEP) >= tau_min > 0 then abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "derivation_status": "EXACT_CONDITIONAL_AMPLITUDE_LAW",
            "conditions": "requires sourced nonzero lower bound tau_min; upper bound on tau alone is insufficient",
            "source": "P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv:DWP1066_3_finite_prior_width",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "law_id": "TCL1596_3_tau_null_escape",
            "object": "tau_WEP",
            "statement": "if tau_WEP can vanish or be arbitrarily small, the MICROSCOPE product bound gives no finite Delta_w_TiPt bound",
            "derivation_status": "NO_SHORTCUT_THEOREM",
            "conditions": "cannot set tau_WEP=1 by convention; cannot hide missing source projection inside measured G",
            "source": "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_5_no_unity_shortcut",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def tau_factor_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_0_source_worldtube",
            "factor": "R_source or T_source^Earth(x)",
            "required_object": "profile-weighted Earth/source stress-current in observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_0_profile_weighting",
            "effect_on_tau": "tau_WEP cannot be numeric and no tau_min lower bound exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_1_orbit_average",
            "factor": "orbit/session/mask average",
            "required_object": "time-weighted projection into the reported MICROSCOPE eta channel",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source": "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv:TAU1225_1_orbit_average",
            "effect_on_tau": "normalization of tau_WEP remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_2_observed_coframe",
            "factor": "e_obs/readout frame",
            "required_object": "same observed coframe for force law, clocks, source variation and readout",
            "current_status": "CONDITIONAL_FROM_PRIOR_SPINE",
            "source": "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_2_observed_coframe",
            "effect_on_tau": "frame consistency is conditional, not a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_3_material_tensor",
            "factor": "Ti/Pt material response",
            "required_object": "TA6V-minus-PtRh10 response tensor in the same source-weight convention",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source": "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv:TAU1482_6_material_tensor",
            "effect_on_tau": "Delta_w_TiPt mapping remains incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_4_readout_matrix",
            "factor": "K_MICROSCOPE / K_CMSM",
            "required_object": "official readout/design matrix with masks, segment timing, orbit/attitude convention and units",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_0_CMSM_arrays",
            "effect_on_tau": "no surrogate kernel can promote a WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_5_product_convention",
            "factor": "eta product normalization",
            "required_object": "map from source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv:RIG1084_1_product_convention",
            "effect_on_tau": "tau_WEP=1 shortcut remains forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factor_id": "TFA1596_6_parent_coupling_slot",
            "factor": "C_parent or action-measure owner",
            "required_object": "theorem-zero route or sourced finite coupling coefficient in the same parent branch",
            "current_status": "MISSING_C_PARENT_IMPORT",
            "source": "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv:TAU1482_5_C_parent",
            "effect_on_tau": "finite branch cannot be promoted to parent-derived local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_last_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AMG1596_0_common_measure_theorem",
            "route": "zero theorem",
            "required_signature": "single parent-owned action measure/coframe for all matter sectors before variation",
            "current_evidence": "common/current measure attempts are partial or failed",
            "source": "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv:CMT1452_6_verdict",
            "result": "UNSIGNED",
            "effect": "cannot set w_A=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AMG1596_1_current_owner_theorem",
            "route": "post-variation current ownership",
            "required_signature": "all effective currents descend from the same parent quotient with no representative weights",
            "current_evidence": "current-source normalization owner remains partial",
            "source": "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv:CSO1453_7_verdict",
            "result": "PARTIAL_NOT_CLOSING_PRE_VARIATION_W_A",
            "effect": "current owner does not kill pre-variation action weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AMG1596_2_classical_equation_route",
            "route": "classical EOM / source equation",
            "required_signature": "EOM removes every representative action/source weight rather than just moving it",
            "current_evidence": "1595 reopen found no new parent-signed owner",
            "source": "P8_Y5_PARENT_QLOC_1595_ACTION_MEASURE_OWNER_REOPEN.csv:AMR1595_5_verdict",
            "result": "DOES_NOT_EXCLUDE_W_A",
            "effect": "finite source-weight branch remains necessary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AMG1596_3_last_gate_verdict",
            "route": "action-measure owner last gate",
            "required_signature": "parent-signed common action measure plus quotient-invariant matter descent",
            "current_evidence": "no cited source currently signs this package",
            "source": "AMG1596_0_common_measure_theorem;AMG1596_1_current_owner_theorem;AMG1596_2_classical_equation_route",
            "result": "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED",
            "effect": "1596 must proceed through tau_WEP source projection/lower-bound route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_w_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "DWB1596_0_product_anchor",
            "quantity": "abs(Delta_w_TiPt * tau_WEP)",
            "bound_statement": "<= 2.8e-15",
            "bound_type": "source-backed product bound",
            "status": "AVAILABLE_FROM_1595",
            "source": "P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv:SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor",
            "numeric_value": "2.8e-15",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "DWB1596_1_tau_value",
            "quantity": "tau_WEP",
            "bound_statement": "numeric value or lower bound required",
            "bound_type": "missing projection input",
            "status": "NOT_EVALUATED",
            "source": "P8_Y5_R10_1482_TAU_WEP_READINESS_UPDATE.csv:TAU1482_7_numeric_tau",
            "numeric_value": "not_available",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "DWB1596_2_tau_lower_bound",
            "quantity": "tau_min",
            "bound_statement": "need abs(tau_WEP) >= tau_min > 0",
            "bound_type": "missing nonzero lower bound",
            "status": "NO_TAU_MIN_SOURCE",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv:TFA1596_0_to_TFA1596_6",
            "numeric_value": "not_available",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": "DWB1596_3_delta_w_bound",
            "quantity": "abs(Delta_w_TiPt)",
            "bound_statement": "if tau_min exists, abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "bound_type": "conditional amplitude law",
            "status": "SYMBOLIC_ONLY_NO_NUMERIC_DELTA_W",
            "source": "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv:TCL1596_2_delta_w_amplitude_law",
            "numeric_value": "not_available",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def tau_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acq_id": "TSA1596_0_readout_matrix",
            "needed_file_or_object": "P_WEP_K_CMSM_readout.csv",
            "required_fields": "time; segment/session id; gx; gz; Sxx; Sxz; masks; calibration flags; attitude/orbit convention; units",
            "source_or_derivation_route": "official MICROSCOPE CMSM/export arrays or validated exact equivalent",
            "acceptance_gate": "no surrogate-only matrix may claim WEP",
            "priority": "highest",
            "status": "SOURCE_NEEDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acq_id": "TSA1596_1_source_worldtube",
            "needed_file_or_object": "P_WEP_R_source_Earth_worldtube.csv",
            "required_fields": "radius/depth shell; density/stress proxy; composition/source response; orbit/source kernel convention; units",
            "source_or_derivation_route": "Earth source profile weighted in observed local frame",
            "acceptance_gate": "bulk composition alone is not enough",
            "priority": "highest",
            "status": "SOURCE_NEEDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acq_id": "TSA1596_2_material_tensor",
            "needed_file_or_object": "P_WEP_TiPt_material_response_tensor.csv",
            "required_fields": "TA6V response; PtRh10 response; source-weight convention; uncertainty; provenance",
            "source_or_derivation_route": "derive from parent matter action or source from official material/composition model",
            "acceptance_gate": "alloy labels alone are not a response tensor",
            "priority": "high",
            "status": "SOURCE_NEEDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acq_id": "TSA1596_3_tau_min",
            "needed_file_or_object": "P_WEP_tau_min_lower_bound.csv",
            "required_fields": "tau_min; confidence; derivation/source path; sign/absolute convention; assumptions",
            "source_or_derivation_route": "prove readout/source contraction cannot vanish, or compute a sourced lower bound",
            "acceptance_gate": "must be strictly positive; tau_WEP=1 convention is forbidden",
            "priority": "highest",
            "status": "DERIVATION_OR_SOURCE_NEEDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "acq_id": "TSA1596_4_action_measure_owner",
            "needed_file_or_object": "parent_action_measure_owner_theorem",
            "required_fields": "common measure; coframe; quotient descent; no representative w_A; boundary terms controlled",
            "source_or_derivation_route": "derive theorem-zero route so Delta_w_TiPt=0 and tau numeric becomes optional",
            "acceptance_gate": "must be parent-signed, not post-variation redefinition",
            "priority": "highest_parallel_route",
            "status": "DERIVATION_NEEDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1596_0_product_anchor",
            "acceptance_rule": "accept 1595 MICROSCOPE product bound as source-backed bound input",
            "input_state": "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15",
            "runner_result": "ACCEPT_PRODUCT_BOUND_ONLY",
            "effect": "kept as private nonclaim bound anchor",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1596_1_delta_w_score",
            "acceptance_rule": "numeric Delta_w bound requires tau_WEP or tau_min",
            "input_state": "tau_WEP not evaluated; no tau_min",
            "runner_result": "REJECT_NUMERIC_DELTA_W_SCORE",
            "effect": "no WEP/local-GR score produced",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1596_2_action_measure_zero",
            "acceptance_rule": "Delta_w=0 requires parent-signed action-measure owner",
            "input_state": "last gate not closed",
            "runner_result": "REJECT_ZERO_THEOREM_CLAIM",
            "effect": "finite source-weight route remains open",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1596_3_local_gr",
            "acceptance_rule": "local GR requires zero theorem or all finite residuals bounded below test thresholds",
            "input_state": "tau source projection incomplete",
            "runner_result": "BLOCK_LOCAL_GR_CLAIM",
            "effect": "continue derivation/source acquisition",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "CG1596_0_WEP",
            "claim": "MTS passes MICROSCOPE/WEP",
            "status": "BLOCKED",
            "reason": "product anchor exists but tau_WEP/source/readout projection is not numeric",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "CG1596_1_Delta_w",
            "claim": "finite bound on Delta_w_TiPt",
            "status": "BLOCKED",
            "reason": "needs tau_min>0 or tau_WEP numeric value",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "CG1596_2_action_measure",
            "claim": "action-measure owner kills w_A",
            "status": "BLOCKED",
            "reason": "last gate not parent-signed",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "CG1596_3_local_GR",
            "claim": "derived local GR branch",
            "status": "BLOCKED",
            "reason": "source-weight/coupling residual still open",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1596_0_math_progress",
            "decision": "PRODUCT_TO_DELTA_W_LAW_DERIVED",
            "reason": "the 1595 bound becomes a Delta_w constraint only through a nonzero tau_WEP lower bound",
            "next_action": "hunt tau_min or close action-measure owner",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1596_1_no_shortcut",
            "decision": "TAU_UNITY_SHORTCUT_REJECTED",
            "reason": "tau_WEP is a physical projection, not a convention; measured-G absorption would hide the residual",
            "next_action": "source readout/source/worldtube factors",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1596_2_owner_status",
            "decision": "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED",
            "reason": "current-owner and common-measure evidence does not remove pre-variation w_A",
            "next_action": "keep finite branch open",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1596_3_next",
            "decision": "NEXT_1597_TAU_LOWER_BOUND_OR_COUPLING_ZERO_PROOF",
            "reason": "that is the cleanest route to make the MICROSCOPE product anchor actionable",
            "next_action": "derive tau_min>0 from geometry/readout or derive coupling/action-measure zero theorem",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
            "script": "scripts/Y5_R2FR_tau_lower_bound_or_coupling_zero_proof.py",
            "objective": "derive a strictly positive tau_WEP lower bound from source/readout geometry, or close the parent coupling/action-measure zero theorem",
            "success_condition": "tau_min>0 with source paths, or parent-signed Delta_w_TiPt=0 theorem; otherwise WEP remains product-bound only",
            "do_not": "do not set tau_WEP=1, do not score WEP from the product anchor alone, do not use measured-G absorption, do not edit formalization-workbench",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for src, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)


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
    truthy = {"true", "1", "yes", "y"}
    flagged_fields = {"score_ready", "valid_prediction_row", "claim_allowed"}
    for path in paths:
        for row in read_csv(path):
            for field in flagged_fields:
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1596() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1596*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    law = read_csv(CONTRACTION_LAW)
    factors = read_csv(TAU_FACTOR_AUDIT)
    action = read_csv(ACTION_LAST_GATE)
    bounds = read_csv(DELTA_W_BOUND_STATUS)
    acq = read_csv(TAU_SOURCE_ACQ)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        (
            "VAL1596_0_sources_exist",
            all(row["exists"] == "True" or row["exists"] is True for row in sources),
            "all cited 1596 source paths exist",
        ),
        (
            "VAL1596_1_needles_found",
            all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources),
            "all required source needles found",
        ),
        (
            "VAL1596_2_product_law",
            any(row["law_id"] == "TCL1596_1_product_bound" and "2.8e-15" in row["statement"] for row in law),
            "MICROSCOPE product bound retained",
        ),
        (
            "VAL1596_3_amplitude_law",
            any(row["law_id"] == "TCL1596_2_delta_w_amplitude_law" and "tau_min > 0" in row["statement"] for row in law),
            "conditional Delta_w amplitude law recorded",
        ),
        (
            "VAL1596_4_tau_null_guard",
            any(row["law_id"] == "TCL1596_3_tau_null_escape" for row in law),
            "tau vanishing escape blocks finite Delta_w bound",
        ),
        (
            "VAL1596_5_tau_factors_block",
            len(factors) >= 6 and all(row["claim_allowed"].lower() == "false" for row in factors),
            "tau factor audit remains nonclaim",
        ),
        (
            "VAL1596_6_action_last_gate_blocks",
            any(row["gate_id"] == "AMG1596_3_last_gate_verdict" and row["result"] == "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED" for row in action),
            "action-measure owner last gate not closed",
        ),
        (
            "VAL1596_7_delta_w_not_numeric",
            any(row["bound_id"] == "DWB1596_3_delta_w_bound" and row["status"] == "SYMBOLIC_ONLY_NO_NUMERIC_DELTA_W" for row in bounds),
            "Delta_w bound remains symbolic",
        ),
        (
            "VAL1596_8_acquisition_requires_tau_min",
            any(row["acq_id"] == "TSA1596_3_tau_min" and "strictly positive" in row["acceptance_gate"] for row in acq),
            "tau_min acquisition row exists",
        ),
        (
            "VAL1596_9_runner_refuses_score",
            any(row["runner_id"] == "RUN1596_1_delta_w_score" and row["runner_result"] == "REJECT_NUMERIC_DELTA_W_SCORE" for row in runner),
            "runner rejects numeric Delta_w score",
        ),
        (
            "VAL1596_10_claim_gates_closed",
            gates and all(row["claim_allowed"].lower() == "false" for row in gates),
            "all claim gates remain closed",
        ),
        (
            "VAL1596_11_decision_next",
            any(row["decision"] == "NEXT_1597_TAU_LOWER_BOUND_OR_COUPLING_ZERO_PROOF" for row in decisions),
            "decision selects 1597 tau lower-bound/coupling-zero target",
        ),
        (
            "VAL1596_12_csv_parse",
            csv_parses(generated_csvs),
            "all generated 1596 CSVs parse",
        ),
        (
            "VAL1596_13_claim_safety_flags",
            no_claim_flags(generated_csvs),
            "no generated 1596 rows are score-ready, prediction rows, or claim-allowed",
        ),
        (
            "VAL1596_14_branch_copies",
            all(path.exists() for path in copies),
            "branch/quarantine nonclaim copies exist",
        ),
        (
            "VAL1596_15_pycache_absent",
            not (Path(__file__).resolve().parent / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1596_16_formalization_untouched",
            no_formalization_1596(),
            "no 1596 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1596_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1596 tau-WEP projection or action-measure owner last-gate validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    law: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    action: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    acq: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1596 - R2/fR tau_WEP Source Projection Or Action-Measure Owner Last Gate",
                "## Verdict\n"
                "- 1596 derives the exact useful amplitude law: the 1595 MICROSCOPE anchor bounds `abs(Delta_w_TiPt*tau_WEP)`, not `Delta_w_TiPt` alone.\n"
                "- Therefore `abs(Delta_w_TiPt) <= 2.8e-15/tau_min` only if a sourced lower bound `abs(tau_WEP) >= tau_min > 0` exists.\n"
                "- No such `tau_min` or numeric `tau_WEP` exists in the current corpus; `tau_WEP=1` and measured-`G` absorption are explicitly rejected.\n"
                "- The action-measure owner route is reopened as a last gate and still does not close: no source signs a pre-variation common action-measure package that kills `w_A`.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## tau_WEP Contraction Law",
                md_table(law, ["law_id", "object", "statement", "derivation_status", "conditions"]),
                "## tau_WEP Factor Audit",
                md_table(factors, ["factor_id", "factor", "current_status", "source", "effect_on_tau"]),
                "## Action-Measure Owner Last Gate",
                md_table(action, ["gate_id", "route", "required_signature", "result", "effect"]),
                "## Delta_w Bound Status",
                md_table(bounds, ["bound_id", "quantity", "bound_statement", "status", "numeric_value"]),
                "## tau Source Acquisition Rows",
                md_table(acq, ["acq_id", "needed_file_or_object", "required_fields", "acceptance_gate", "priority", "status"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    law = contraction_law_rows()
    factors = tau_factor_rows()
    action = action_last_gate_rows()
    bounds = delta_w_bound_rows()
    acq = tau_source_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        CONTRACTION_LAW,
        TAU_FACTOR_AUDIT,
        ACTION_LAST_GATE,
        DELTA_W_BOUND_STATUS,
        TAU_SOURCE_ACQ,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CONTRACTION_LAW, law)
    write_csv(TAU_FACTOR_AUDIT, factors)
    write_csv(ACTION_LAST_GATE, action)
    write_csv(DELTA_W_BOUND_STATUS, bounds)
    write_csv(TAU_SOURCE_ACQ, acq)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, law, factors, action, bounds, acq, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
