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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1802"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1802_0_1801_doc",
        "source_key": "1801_handoff",
        "source_path": ROOT / "1801-Y5-R2FR-JX-source-zero-or-component-bound-pack.md",
        "needles": ["DEC1801_2_best_first_component", "NEXT1801_0_primary"],
        "role": "selects parent matter functor/readout no-reentry as 1802 target",
    },
    {
        "source_id": "SRC1802_1_1801_validation",
        "source_key": "1801_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1801_VALIDATION.csv",
        "needles": ["VAL1801_OVERALL", "PASS"],
        "role": "confirms 1801 passed before 1802 starts",
    },
    {
        "source_id": "SRC1802_2_1801_jx_gate",
        "source_key": "1801_jx_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_SOURCE_SILENCE_GATE.csv",
        "needles": ["JZS1801_2_matter_pullback", "JZS1801_8_verdict"],
        "role": "identifies matter/readout as the first live J_X component route",
    },
    {
        "source_id": "SRC1802_3_1045_matter_functor",
        "source_key": "1045_matter_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_0_parent_field_quotient", "MFS1045_6_verdict"],
        "role": "older exact parent matter functor signature audit",
    },
    {
        "source_id": "SRC1802_4_1720_current_matter_functor",
        "source_key": "1720_matter_functor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"],
        "role": "current branch matter functor/source signature audit",
    },
    {
        "source_id": "SRC1802_5_1737_coframe",
        "source_key": "1737_coframe_functor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv",
        "needles": ["CFZ1737_0_exact_conditional", "CFZ1737_3_current_verdict"],
        "role": "coframe functor vertical-zero attempt",
    },
    {
        "source_id": "SRC1802_6_1740_no_shadow_gate",
        "source_key": "1740_no_shadow_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_CLAUSE_GATE.csv",
        "needles": ["NSF1740_0_parent_matter_domain", "NSF1740_6_verdict"],
        "role": "no shadow frame/readout/source-prefactor clause gate",
    },
    {
        "source_id": "SRC1802_7_1740_no_shadow_theorem",
        "source_key": "1740_no_shadow_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1740_NO_SHADOW_FRAME_ZERO_THEOREM_ATTEMPT.csv",
        "needles": ["NSF1740_THM0_exact_contract", "NSF1740_THM2_bound_fallback"],
        "role": "conditional no-shadow theorem and finite fallback map",
    },
    {
        "source_id": "SRC1802_8_1761_no_direct_vertex",
        "source_key": "1761_no_direct_vertex",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
        "needles": ["NDV1761_0_target", "NDV1761_4_current_verdict"],
        "role": "no direct ordinary matter X vertex/source-weight grammar attempt",
    },
    {
        "source_id": "SRC1802_9_1454_variation_before_readout",
        "source_key": "1454_variation_before_readout",
        "source_path": RESIDUALS / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv",
        "needles": ["VBR1454_0_target", "VBR1454_6_verdict"],
        "role": "variation-before-readout theorem attempt and pre-action selector counterexample",
    },
    {
        "source_id": "SRC1802_10_1701_no_reentry",
        "source_key": "1701_no_reentry",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv",
        "needles": ["NRE1701_0_type_theorem", "NRE1701_5_verdict"],
        "role": "readout no-reentry theorem attempt",
    },
    {
        "source_id": "SRC1802_11_1701_commutator",
        "source_key": "1701_commutator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
        "needles": ["RC1701_0_define_residual", "RC1701_6_verdict"],
        "role": "readout/effective/projector commutator residual audit",
    },
    {
        "source_id": "SRC1802_12_1701_queue",
        "source_key": "1701_queue",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1701_READOUT_RESIDUAL_QUEUE.csv",
        "needles": ["RQ1701_0_C_R", "RQ1701_6_arena_branch_map"],
        "role": "readout residual queue and arena product map blockers",
    },
    {
        "source_id": "SRC1802_13_1486_readout_shadow",
        "source_key": "1486_readout_shadow",
        "source_path": RESIDUALS / "P8_Y5_R10_1486_NO_SHADOW_READOUT_REENTRY_AUDIT.csv",
        "needles": ["NSR1486_0_hidden_coefficients", "NSR1486_4_verdict"],
        "role": "no-shadow/readout reentry obstruction audit",
    },
    {
        "source_id": "SRC1802_14_1780_source_functor",
        "source_key": "1780_source_functor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
        "needles": ["QTS1780_0_parent_q_map", "QTS1780_7_verdict"],
        "role": "q/Dq/tau/source-readout functor signature gate",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_SOURCE_REGISTER.csv",
    "matter_readout_theorem_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_MATTER_READOUT_THEOREM_GATE.csv",
    "qbar_readout_component_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_QBAR_READOUT_COMPONENT_ROWS.csv",
    "readout_type_split": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_READOUT_TYPE_SPLIT.csv",
    "observable_interface": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_OBSERVABLE_INTERFACE.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_ACCEPTANCE_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1802_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1802_VALIDATION.csv",
}

DOC_PATH = ROOT / "1802-Y5-R2FR-parent-matter-functor-readout-no-reentry-or-qbar-readout-row.md"


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


def matter_readout_theorem_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_0_parent_qDq",
            "claim_piece": "parent quotient and vertical kernel",
            "required_statement": "q:Phi_parent->Q_vis exists before readout and v_X is in ker(Dq) for the local X direction",
            "derivation_status": "EXACT_IF_Q_DQ_SIGNED",
            "current_status": "Q_DQ_KERNEL_UNSIGNED",
            "missing_input": "MISSING_PARENT_Q_MAP;MISSING_DQ_KERNEL_BASIS",
            "source_paths": src("1737_coframe_functor", "1780_source_functor", "1045_matter_functor"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_1_coframe_functor",
            "claim_piece": "observed coframe/metric descent",
            "required_statement": "e_obs=Obs_e(q(Phi)) and g_obs, omega_obs are owned by the same observed coframe",
            "derivation_status": "CHAIN_RULE_ZERO_CONDITIONAL",
            "current_status": "COFRAME_FUNCTOR_NOT_PARENT_SIGNED",
            "missing_input": "MISSING_OBS_E_PARENT_OWNER;MISSING_CONNECTION_LOCK",
            "source_paths": src("1737_coframe_functor", "1720_matter_functor"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_2_matter_functor_lift",
            "claim_piece": "ordinary matter action and vertical lift",
            "required_statement": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] with fixed/gauge-owned vertical lift on Psi_A",
            "derivation_status": "SUFFICIENT_CONDITIONAL_THEOREM",
            "current_status": "MATTER_CATEGORY_AND_LIFT_UNSIGNED",
            "missing_input": "MISSING_PARENT_MATTER_CATEGORY;MISSING_VERTICAL_LIFT_THEOREM",
            "source_paths": src("1045_matter_functor", "1720_matter_functor"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_3_no_shadow_marker",
            "claim_piece": "no hidden frame/source marker",
            "required_statement": "no Weyl/disformal shadow frame, source-only prefactor, material marker, or hidden coefficient Hom enters S_ord",
            "derivation_status": "CONTRACT_EXACT_COUNTERMODELS_RETAINED",
            "current_status": "NO_SHADOW_NO_MARKER_NOT_SIGNED",
            "missing_input": "MISSING_NO_SHADOW_FRAME_THEOREM;MISSING_CONSTANT_SUPERSELECTION;MISSING_SOURCE_PREFactor_ZERO",
            "source_paths": src("1740_no_shadow_gate", "1740_no_shadow_theorem", "1486_readout_shadow", "1761_no_direct_vertex"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_4_pure_postprocessing",
            "claim_piece": "pure readout postprocessing",
            "required_statement": "R_post maps already-solved parent states to data and is absent from S_parent",
            "derivation_status": "TYPE_THEOREM_CONDITIONAL",
            "current_status": "PURE_POSTPROCESSING_SAFE_BUT_NOT_GENERAL",
            "missing_input": "MISSING_PARENT_DOMAIN_TYPING_FOR_ALL_ARENAS",
            "source_paths": src("1454_variation_before_readout", "1701_no_reentry", "1701_commutator"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_5_general_readout",
            "claim_piece": "general readout/effective/source-map no-reentry",
            "required_statement": "no pre-action weights, no field-dependent projectors, no S_eff feedback, no calibration/source-worldtube feedback",
            "derivation_status": "GENERAL_THEOREM_BLOCKED",
            "current_status": "READOUT_REENTRY_RESIDUALS_RETAINED",
            "missing_input": "MISSING_PREACTION_WEIGHT_EXCLUSION;MISSING_PROJECTOR_CHAIN_MAP;MISSING_EFFECTIVE_ACTION_DOMAIN;MISSING_CALIBRATION_FEEDBACK_ZERO",
            "source_paths": src("1701_no_reentry", "1701_commutator", "1701_queue", "1486_readout_shadow"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_6_conditional_theorem",
            "claim_piece": "conditional J_matter/readout theorem",
            "required_statement": "if MRT1802_0 through MRT1802_5 are parent-signed with pure readout typing, then delta_v S_ord=0 and C_R^pure=0",
            "derivation_status": "EXACT_CONDITIONAL_PARENT_CONTRACT",
            "current_status": "CONTRACT_READY_PARENT_UNSIGNED",
            "missing_input": "MISSING_SINGLE_PARENT_ACTION_SIGNATURE",
            "source_paths": src("1801_jx_gate", "1045_matter_functor", "1701_no_reentry"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MRT1802_7_verdict",
            "claim_piece": "current J_matter=0/readout no-reentry claim",
            "required_statement": "ordinary matter functor plus no-shadow/readout no-reentry close in the current corpus",
            "derivation_status": "FAIL_CURRENT_CLAIM",
            "current_status": "JMatter_AND_READOUT_ZERO_NOT_SIGNED_COMPONENT_ROWS_REQUIRED",
            "missing_input": "MISSING_Q_DQ_MATTER_NO_SHADOW_READOUT_SOURCE_PACK",
            "source_paths": src("1801_jx_gate", "1720_matter_functor", "1780_source_functor", "1701_commutator"),
            "theorem_zero": False,
            "valid_for_claim": False,
        },
    ]


def qbar_readout_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_0_qbar_geom",
            "symbol": "qbar_geom",
            "definition": "visible geometry/coframe leakage into ordinary test-body X charge",
            "formula_or_bound": "qbar_geom=(2M_T)^-1 int sqrt(-g_obs) T_T^{mu nu} Lie_v g_obs_munu",
            "current_value": "MISSING_LIE_V_GOBS_OR_THEOREM_ZERO",
            "required_input": "q/Dq;Obs_e parent owner;connection lock;source paths",
            "status": "NONCLAIM_COMPONENT_VALUE_MISSING",
            "source_paths": src("1737_coframe_functor", "1045_matter_functor"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_1_qbar_marker_constants",
            "symbol": "qbar_marker+qbar_constants",
            "definition": "material markers, masses, charges, alpha_EM, clocks, and hidden representation constants",
            "formula_or_bound": "|qbar_marker+qbar_constants| <= sum_A |s_A b_A| + |dtheta_A/dX| sensitivities",
            "current_value": "MISSING_MARKER_CONSTANT_COEFFICIENTS",
            "required_input": "constant superselection theorem or coefficient rows with units/source paths",
            "status": "NONCLAIM_COMPONENT_VALUE_MISSING",
            "source_paths": src("1740_no_shadow_gate", "1486_readout_shadow", "1761_no_direct_vertex"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_2_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "source-only pre-action species/class weight in the active gravitational source",
            "formula_or_bound": "|qbar_source_weight| <= max_A |w_A/w_univ-1| plus measured-G calibration tail",
            "current_value": "MISSING_PREACTION_WEIGHT_BOUND",
            "required_input": "object-language exclusion or finite Delta_w/source-weight rows",
            "status": "NONCLAIM_COMPONENT_VALUE_MISSING",
            "source_paths": src("1454_variation_before_readout", "1701_no_reentry", "1761_no_direct_vertex"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_3_C_readout_commutator",
            "symbol": "C_R[A]",
            "definition": "readout/effective source-coefficient reentry residual",
            "formula_or_bound": "|C_R[A]| <= |Pi([delta_parent,R_A]T_H)| + |Pi(delta_pre R_A)| + |Pi(delta_cal R_A)|",
            "current_value": "MISSING_READOUT_COMMUTATOR_COEFFICIENTS",
            "required_input": "pure postprocessing theorem for arena A or finite product-map coefficients",
            "status": "NONCLAIM_COMPONENT_VALUE_MISSING",
            "source_paths": src("1701_commutator", "1701_queue", "1486_readout_shadow"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_4_pure_readout_zero_candidate",
            "symbol": "C_R^pure",
            "definition": "source reentry from a strictly post-solution data map absent from S_parent",
            "formula_or_bound": "C_R^pure=0 only inside the typed postprocessing domain",
            "current_value": "0_IF_STRICT_PURE_POSTPROCESSING_TYPING_SIGNED",
            "required_input": "parent domain typing and arena-specific proof that R_post is absent from S_parent/S_eff/source normalizer",
            "status": "THEOREM_ZERO_CANDIDATE_BLOCKED_OUTSIDE_PURE_DOMAIN",
            "source_paths": src("1454_variation_before_readout", "1701_no_reentry", "1701_commutator"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QRC1802_5_total_abs_guard",
            "symbol": "qbar_readout_abs_envelope",
            "definition": "no-cancellation envelope for matter/readout source contribution to J_X",
            "formula_or_bound": "|J_matter+J_readout| <= M_T(|qbar_geom|+|qbar_marker|+|qbar_constants|+|qbar_source_weight|)+|C_R[A]|",
            "current_value": "MISSING_COMPONENT_VALUES",
            "required_input": "all theorem-zero certificates or all component values in a shared convention",
            "status": "NO_CANCELLATION_ENVELOPE_READY_VALUES_MISSING",
            "source_paths": src("1801_jx_gate", "1045_matter_functor", "1701_commutator"),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def readout_type_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "type_id": "RTS1802_0_pure_postprocessing",
            "readout_type": "pure postprocessing",
            "criterion": "map from solved parent state/gauge quotient to reported data; no arrow back into S_parent, S_eff, Pi_M, calibration source, or field equation",
            "current_status": "CONDITIONAL_SAFE_DOMAIN_DEFINED",
            "claim_scope": "only proves no source reentry for that strictly typed map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "type_id": "RTS1802_1_preaction_weight",
            "readout_type": "pre-action/source weight",
            "criterion": "coefficient or material selector appears inside S_matter before variation",
            "current_status": "COUNTERMODEL_ACTIVE",
            "claim_scope": "must be excluded by parent object-language theorem or bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "type_id": "RTS1802_2_projector_domain",
            "readout_type": "field-dependent projector/domain",
            "criterion": "Pi or domain map depends on fields, support, boundary, clocks, or source worldtube",
            "current_status": "COMMUTATOR_RESIDUAL_ACTIVE",
            "claim_scope": "needs chain-map theorem or finite commutator row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "type_id": "RTS1802_3_effective_action",
            "readout_type": "effective/radiative action",
            "criterion": "S_eff adds readout/cutoff/field-dependent terms before variation",
            "current_status": "NO_REENTRY_FAILS_IF_PREVARIATION",
            "claim_scope": "needs EFT domain theorem or coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "type_id": "RTS1802_4_calibration_feedback",
            "readout_type": "calibration/source-worldtube feedback",
            "criterion": "data-selected calibration or mask is used as a source normalizer",
            "current_status": "FORBIDDEN_AS_DERIVATION_RETAIN_AS_RESIDUAL",
            "claim_scope": "must be fixed before variation or explicitly bounded",
            "valid_for_claim": False,
        },
    ]


def observable_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1802_0_R10",
            "observable_arena": "R10 short-range force",
            "uses_components": "qbar_geom;qbar_marker;qbar_source_weight;C_R[R10]",
            "projection_rule": "alpha_X(lambda) cannot be scored until K_X,Qbar_XH,qbar_XT,C_R and a real bound curve are present",
            "current_status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1802_1_WEP",
            "observable_arena": "WEP/source-charge",
            "uses_components": "qbar_marker;qbar_constants;qbar_source_weight;C_R[WEP]",
            "projection_rule": "eta_AB requires material-pair qbar components and source normalization in the same frame",
            "current_status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1802_2_clocks_EM",
            "observable_arena": "clocks/EM constants",
            "uses_components": "qbar_constants;readout calibration;shadow frame",
            "projection_rule": "clock/EM residual needs sensitivities and dtheta_A/dX rows; no transfer from WEP/R10 by analogy",
            "current_status": "NOT_SCOREABLE_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "OBS1802_3_PPN_orbit",
            "observable_arena": "PPN/orbital/source normalization",
            "uses_components": "C_R[PPN];projector commutator;source-weight;boundary/source support",
            "projection_rule": "measured GM/Newton limit needs Pi_M chain map and source functor signature before scoring",
            "current_status": "NOT_SCOREABLE_SOURCE_FUNCTOR_OPEN",
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1802_0_jmatter_zero",
            "gate": "ordinary matter/readout source zero",
            "current_status": "FAIL_PARENT_SIGNATURE_UNSIGNED",
            "reason": "q/Dq, coframe functor, matter lift, no-shadow, constants and general readout no-reentry are not all signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1802_1_pure_readout_scope",
            "gate": "pure readout no-reentry scope",
            "current_status": "CONDITIONAL_SCOPE_WRITTEN_NOT_CLAIM",
            "reason": "pure postprocessing is safe by type, but parent domain typing is not signed for every arena",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1802_2_component_rows",
            "gate": "qbar/readout component rows",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "reason": "component formulas are written but theorem-zero certificates or numeric values are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1802_3_verdict",
            "gate": "matter/readout closure readiness",
            "current_status": "JMatter_READOUT_NOT_ZERO_AND_NOT_BOUNDED",
            "reason": "no claim-ready source-zero theorem or source-backed component envelope exists",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1802_0_shadow_frame",
            "countermodel": "matter sees A(X)^2 g_obs or a disformal/source-only frame while the visible coframe looks classical",
            "survives_current_constraints": True,
            "why_survives": "no-shadow frame theorem is a contract, not parent-signed",
            "what_kills_it": "parent no-shadow/no-marker theorem or finite shadow coefficients",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1802_1_preaction_weight",
            "countermodel": "S_matter contains species/source weights before variation, producing real source charge",
            "survives_current_constraints": True,
            "why_survives": "variation-before-readout does not kill coefficients already in the action",
            "what_kills_it": "object-language exclusion of pre-action weights or Delta_w source-backed rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1802_2_readout_projector",
            "countermodel": "field-dependent projector/domain/readout commutator carries source residual",
            "survives_current_constraints": True,
            "why_survives": "general readout commutator is not zero-proved",
            "what_kills_it": "chain-map theorem or finite C_R/I_commutator rows",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1802_3_constants_markers",
            "countermodel": "masses, alpha_EM, clocks, or material markers depend on the X direction",
            "survives_current_constraints": True,
            "why_survives": "constant superselection and no-marker clauses are unsigned",
            "what_kills_it": "constant/marker superselection theorem or clock/EM/material coefficient bounds",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1802_0_Jmatter_zero",
            "claim": "J_matter=0 and qbar_XT=0 from ordinary matter functor",
            "status": "BLOCKED",
            "reason": "MRT1802_7 says current parent signature is unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1802_1_readout_no_reentry",
            "claim": "all readout/effective maps have zero source reentry",
            "status": "BLOCKED",
            "reason": "only pure postprocessing is conditionally safe; general readout residuals remain live",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1802_2_component_bound",
            "claim": "qbar/readout component envelope is scoreable",
            "status": "BLOCKED",
            "reason": "component values and source paths are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1802_3_local_GR_Newton",
            "claim": "ordinary matter/readout closure proves local GR/Newton source side",
            "status": "BLOCKED",
            "reason": "q/Dq, source normalization, boundary/history and no-shadow routes still remain",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1802_0_exact_result",
            "decision": "PURE_POSTPROCESSING_NO_REENTRY_ONLY",
            "reason": "pure post-solution data maps cannot alter parent variation, but this is only a typed subdomain",
            "next_action": "do not apply this to pre-action weights, projectors, effective actions or calibration feedback",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1802_1_current_status",
            "decision": "JMatter_READOUT_ZERO_NOT_SIGNED",
            "reason": "the conditional theorem is exact, but q/Dq, matter functor, no-shadow/constants and general readout clauses are unsigned",
            "next_action": "keep qbar/readout component rows live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1802_2_best_next",
            "decision": "NO_SHADOW_CONSTANT_MARKER_OR_QBAR_COEFFICIENTS_NEXT",
            "reason": "shadow frames/constants/markers are the biggest loophole that can defeat the clean matter-functor chain rule even if coframe descent is accepted",
            "next_action": "build 1803 to prove no shadow/constant/marker route or emit qbar_marker/qbar_constants coefficients",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1802_0_primary",
            "next_target": "1803-Y5-R2FR-no-shadow-constant-marker-or-qbar-coefficient-pack.md",
            "script": "scripts/Y5_R2FR_no_shadow_constant_marker_or_qbar_coefficient_pack.py",
            "objective": "try to prove no hidden Weyl/disformal frame, no mass/alpha/clock/material marker X-dependence, and no source-only prefactor; if not, emit qbar_marker/qbar_constants coefficients",
            "selection_status": "selected",
            "success_condition": "no-shadow/constant theorem-zero or finite source-backed qbar coefficient pack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1802_1_parallel_qDq",
            "next_target": "1803b-Y5-R2FR-explicit-q-Dq-kernel-basis-or-frame-leak-rows.md",
            "script": "scripts/Y5_R2FR_explicit_q_Dq_kernel_basis_or_frame_leak_rows.py",
            "objective": "compute/sign q and Dq kernel for the local X direction or emit frame-leak coefficient rows",
            "selection_status": "held_parallel",
            "success_condition": "Dq[v_X]=0 proof or finite coframe/frame leak inputs",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1802_2_parallel_readout",
            "next_target": "1803c-Y5-R2FR-readout-commutator-product-map-fill.md",
            "script": "scripts/Y5_R2FR_readout_commutator_product_map_fill.py",
            "objective": "fill finite C_R[A] product rows for R10/WEP/PPN/clocks/orbits if no-reentry cannot be theorem-zero",
            "selection_status": "held_parallel",
            "success_condition": "arena-specific readout residual rows with units/source paths",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "matter_readout_theorem_gate": matter_readout_theorem_gate_rows(),
        "qbar_readout_component_rows": qbar_readout_component_rows(),
        "readout_type_split": readout_type_split_rows(),
        "observable_interface": observable_interface_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
        shutil.copy2(path, RAB_QUEUE / f"JR1802_{key.upper()}.csv")


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
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
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
        "accepted_for_scoring",
        "valid_prediction_row",
        "theorem_zero",
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
        if not (RAB_QUEUE / f"JR1802_{key.upper()}.csv").exists():
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
        ("VAL1802_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1802_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1802_2_theorem_not_promoted",
            any(
                row["gate_id"] == "MRT1802_7_verdict"
                and row["current_status"] == "JMatter_AND_READOUT_ZERO_NOT_SIGNED_COMPONENT_ROWS_REQUIRED"
                and not boolish(row["theorem_zero"])
                for row in rows_map["matter_readout_theorem_gate"]
            ),
            "matter/readout zero theorem remains unpromoted",
        ),
        (
            "VAL1802_3_pure_scope_separated",
            any(
                row["type_id"] == "RTS1802_0_pure_postprocessing"
                and row["current_status"] == "CONDITIONAL_SAFE_DOMAIN_DEFINED"
                for row in rows_map["readout_type_split"]
            )
            and any(row["type_id"] == "RTS1802_1_preaction_weight" and row["current_status"] == "COUNTERMODEL_ACTIVE" for row in rows_map["readout_type_split"]),
            "pure postprocessing is separated from pre-action/readout countermodels",
        ),
        (
            "VAL1802_4_component_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in rows_map["qbar_readout_component_rows"])
            and any("MISSING" in row["current_value"] for row in rows_map["qbar_readout_component_rows"]),
            "qbar/readout rows are nonclaim and missing live values",
        ),
        (
            "VAL1802_5_observable_interfaces_blocked",
            all(not boolish(row["valid_for_claim"]) and row["current_status"].startswith("NOT_SCOREABLE") for row in rows_map["observable_interface"]),
            "observable projection rows remain blocked",
        ),
        (
            "VAL1802_6_acceptance_blocks",
            any(
                row["gate_id"] == "AC1802_3_verdict"
                and row["current_status"] == "JMatter_READOUT_NOT_ZERO_AND_NOT_BOUNDED"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks matter/readout closure",
        ),
        (
            "VAL1802_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1802_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED" and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "claim gates are blocked",
        ),
        ("VAL1802_9_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1802_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1802_11_decision_next",
            any(
                row["decision_id"] == "DEC1802_2_best_next"
                and row["decision"] == "NO_SHADOW_CONSTANT_MARKER_OR_QBAR_COEFFICIENTS_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects no-shadow/constant marker next",
        ),
        (
            "VAL1802_12_next_selected",
            any(row["route_id"] == "NEXT1802_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1802_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1802 CSVs parse"),
        ("VAL1802_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1802_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1802_16_formalization_untouched", formalization_untouched(), "no 1802 outputs found under formalization-workbench"),
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
            "check_id": "VAL1802_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1802 parent matter functor/readout no-reentry or qbar/readout row checkpoint",
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
            "# 1802 - Y5/R2FR Parent Matter Functor, Readout No-Reentry, or qbar/Readout Row",
            "",
            "## Verdict",
            "",
            "1802 proves one narrow thing and refuses the overclaim: a strictly pure post-processing readout cannot alter the parent variation if it is absent from `S_parent`.",
            "",
            "That is useful, but it does not prove general readout silence. Pre-action weights, field-dependent projectors, effective-action feedback, calibration masks, shadow frames, constants and material markers remain live.",
            "",
            "So `J_matter=0` and `J_readout=0` are not claimed. Instead, 1802 gives a component envelope for `qbar_geom`, `qbar_marker+qbar_constants`, `qbar_source_weight`, and `C_R[A]`.",
            "",
            "**Claim ceiling:** no `J_matter=0`, no general readout no-reentry theorem, no `qbar_XT=0`, no local-GR/Newton source-normalization claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1802.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Matter/Readout Theorem Gate",
            markdown_table(rows_map["matter_readout_theorem_gate"], ["gate_id", "claim_piece", "required_statement", "current_status", "missing_input", "theorem_zero", "valid_for_claim"]),
            "",
            "## qbar/Readout Component Rows",
            markdown_table(rows_map["qbar_readout_component_rows"], ["component_id", "symbol", "definition", "formula_or_bound", "current_value", "status", "valid_for_claim"]),
            "",
            "## Readout Type Split",
            markdown_table(rows_map["readout_type_split"], ["type_id", "readout_type", "criterion", "current_status", "claim_scope", "valid_for_claim"]),
            "",
            "## Observable Interface",
            markdown_table(rows_map["observable_interface"], ["interface_id", "observable_arena", "uses_components", "projection_rule", "current_status", "valid_for_claim"]),
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
            "This is progress because the readout problem is no longer fog. Pure readout is harmless; not all readout is pure. The next best route is the shadow/constant/marker theorem, because that is where a clean matter-functor descent can still be defeated by hidden couplings.",
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
    print(f"1802 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
