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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1789"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1789_0_1788_handoff",
        "source_key": "1788_handoff_doc",
        "source_path": ROOT / "1788-Y5-R2FR-parent-second-order-no-extra-scalar-premise-or-R2FR-bound-row.md",
        "needles": ["PPG1788_4_no_integrated_out_tower", "DEC1788_1_parent_status", "NEXT1788_0_primary"],
    },
    {
        "source_id": "SRC1789_1_1788_validation",
        "source_key": "1788_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1788_VALIDATION.csv",
        "needles": ["VAL1788_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1789_2_1788_premise_gate",
        "source_key": "1788_parent_premise_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1788_PARENT_PREMISE_ACTIVATION_GATE.csv",
        "needles": ["PPG1788_4_no_integrated_out_tower", "PPG1788_6_verdict"],
    },
    {
        "source_id": "SRC1789_3_962_relative",
        "source_key": "962_r2fr_zero_proof",
        "source_path": RESIDUALS / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
        "needles": ["R2Z962_2_trace_scalar_pole", "R2Z962_5_relative_zero_theorem"],
    },
    {
        "source_id": "SRC1789_4_963_derivative",
        "source_key": "963_derivative_order",
        "source_path": RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_2_440_sector_reduction", "DO963_6_verdict"],
    },
    {
        "source_id": "SRC1789_5_964_minimality",
        "source_key": "964_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_2_no_integrated_out_tower", "MIN964_5_verdict"],
    },
    {
        "source_id": "SRC1789_6_965_primitive",
        "source_key": "965_primitive_quotient",
        "source_path": RESIDUALS / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        "needles": ["PQ965_2_no_natural_marker_functor", "PQ965_5_verdict"],
    },
    {
        "source_id": "SRC1789_7_970_quadratic_memory",
        "source_key": "970_quadratic_memory_action",
        "source_path": RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "needles": ["QMA970_0_action", "QMA970_6_integrated_out_tower", "QMA970_7_verdict"],
    },
    {
        "source_id": "SRC1789_8_970_tower_gate",
        "source_key": "970_no_integrated_out_tower",
        "source_path": RESIDUALS / "P8_Y5_R10_970_NO_INTEGRATED_OUT_TOWER_GATE.csv",
        "needles": ["NIT970_0_zero_solution_case", "NIT970_4_verdict"],
    },
    {
        "source_id": "SRC1789_9_970_source_boundary",
        "source_key": "970_source_boundary_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_970_SOURCE_BOUNDARY_GATE.csv",
        "needles": ["SBG970_1_J_chiD_wall", "SBG970_8_verdict"],
    },
    {
        "source_id": "SRC1789_10_970_branch_audit",
        "source_key": "970_active_vs_double_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_970_ACTIVE_VS_DOUBLE_ZERO_BRANCH_AUDIT.csv",
        "needles": ["ADB970_0_active_positive_operator", "ADB970_3_verdict"],
    },
    {
        "source_id": "SRC1789_11_710_descent",
        "source_key": "710_descent_parent_action_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
        "needles": ["DPC710_4_no_local_kinetic_mode", "DPC710_9_verdict"],
    },
    {
        "source_id": "SRC1789_12_710_counterexamples",
        "source_key": "710_counterexample_ledger",
        "source_path": RESIDUALS / "P8_Y5_R10_710_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["CE710_0_variable_prefactor", "CE710_5_Ward_drop"],
    },
    {
        "source_id": "SRC1789_13_1710_scalaron",
        "source_key": "1710_scalaron_map_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_SCALARON_MAP_CONTRACT.csv",
        "needles": ["SMC1710_0_flat_R_plus_aR2", "SMC1710_4_prediction_row"],
    },
    {
        "source_id": "SRC1789_14_1710_input_pack",
        "source_key": "1710_cr2_input_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_CR2_INPUT_PACK_CONTRACT.csv",
        "needles": ["IP1710_1_coefficient", "IP1710_8_acceptance"],
    },
    {
        "source_id": "SRC1789_15_1710_runner_refusal",
        "source_key": "1710_runner_refusal",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_RUNNER_REFUSAL.csv",
        "needles": ["RUN1710_1_input_pack", "RUN1710_5_future_accept"],
    },
    {
        "source_id": "SRC1789_16_1710_hunt",
        "source_key": "1710_coefficient_hunt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_COEFFICIENT_SOURCE_HUNT_REFRESH.csv",
        "needles": ["CH1710_0_parent_zero", "CH1710_6_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_SOURCE_REGISTER.csv",
    "elimination_identity": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_ELIMINATION_IDENTITY_GATE.csv",
    "tower_exclusion_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_NO_INTEGRATED_OUT_TOWER_GATE.csv",
    "effective_coefficient_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_EFFECTIVE_CR2_COEFFICIENT_PACK.csv",
    "finite_scalar_input_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_FINITE_SCALAR_INPUT_PACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1789_VALIDATION.csv",
}

DOC_PATH = ROOT / "1789-Y5-R2FR-no-integrated-out-curvature-tower-or-finite-scalar-bound-pack.md"


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
                "role": "1789 no-integrated-out curvature tower and finite scalar bound evidence",
            }
        )
    return rows


def elimination_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "identity_id": "EID1789_0_quadratic_sector",
            "claim": "quadratic hidden sector has an exact elimination identity",
            "mathematical_form": "S_X=1/2 <X,L_X X> - <J_X,X> + S_boundary, E_X=0 => X=L_X^{-1}J_X",
            "result": "EXACT_CONDITIONAL_IDENTITY",
            "source_basis": "QMA970_0_action;QMA970_1_variation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "EID1789_1_effective_tail",
            "claim": "eliminating a sourced hidden sector generates a Green-function tail",
            "mathematical_form": "S_eff = S_rest - 1/2 <J_X,L_X^{-1}J_X> + boundary/readout terms",
            "result": "EXACT_CONDITIONAL_IDENTITY",
            "source_basis": "QMA970_6_integrated_out_tower;NIT970_1_nonzero_source_case",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "EID1789_2_curvature_projection",
            "claim": "curvature coupling regenerates R2/fR or nonlocal curvature operators",
            "mathematical_form": "if J_X contains B_R R + B_T T + B_bdy K, then -1/2 B_R R L_X^{-1} B_R R gives R L_X^{-1}R, locally R^2/m_X^2 + higher derivative tower",
            "result": "EXACT_CONDITIONAL_RISK",
            "source_basis": "NIT970_2_curvature_coupled_case;DO963_2_440_sector_reduction",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "EID1789_3_safe_zero_case",
            "claim": "no tower follows only if source and boundary pieces vanish before elimination",
            "mathematical_form": "J_X=0, boundary flux=0, zero mode removed/universal => X=0 or universal constant => no finite L_X^{-1} tail",
            "result": "EXACT_CONDITIONAL_SAFE_CASE",
            "source_basis": "NIT970_0_zero_solution_case;QMA970_2_positivity",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "identity_id": "EID1789_4_verdict",
            "claim": "MTS current corpus satisfies the safe zero case",
            "mathematical_form": "EID1789_3 plus all source/boundary/readout/matter-frame gates pass",
            "result": "SAFE_ZERO_CASE_NOT_PARENT_SIGNED",
            "source_basis": "SBG970_8_verdict;DPC710_9_verdict",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def tower_exclusion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_0_bare_higher_curvature",
            "needed_statement": "bare R2/fR/R F(Box) R terms are absent or topological/redundant",
            "current_status": "UNSIGNED_NO_BARE_HIGHER_CURVATURE_CLAUSE",
            "blocker": "minimality/no-higher-derivative theorem remains unproven",
            "zero_if_closed": "c_bare=0",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_1_hidden_source_zero",
            "needed_statement": "hidden/memory/scalar sectors have J_X=0 in compact local exterior",
            "current_status": "SOURCE_ZERO_NOT_DERIVED",
            "blocker": "J_matter, chi_D wall, boundary exchange, readout, and history kernel gates fail/open",
            "zero_if_closed": "B_X L_X^{-1} B_X contribution absent",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_2_boundary_readout_zero",
            "needed_statement": "boundary/readout reduction creates no pre-variation curvature/source counterterm",
            "current_status": "BOUNDARY_READOUT_ZERO_NOT_CERTIFIED",
            "blocker": "readout-after-variation and boundary no-flux are closure discipline, not parent theorem",
            "zero_if_closed": "c_boundary=c_measure=0",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_3_no_scalar_class_kinetic",
            "needed_statement": "scalar/class labels have no local kinetic mode, R-prefactor, matter frame, or projection stress",
            "current_status": "DESCENT_CLAUSE_NOT_PARENT_OWNED",
            "blocker": "DPC710_0 through DPC710_7 are candidate clauses only",
            "zero_if_closed": "scalar-tensor/f(R)-like leakage absent",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_4_effective_law_components",
            "needed_statement": "all finite effective coefficient pieces are either zero theorem or numeric/source-backed",
            "current_status": "EFFECTIVE_COMPONENTS_MISSING",
            "blocker": "c_bare, B_X, L_inverse, M_X2, Z_X, c_measure, c_boundary are not sourced",
            "zero_if_closed": "complete c_R2_eff row or zero certificate",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "NIT1789_5_verdict",
            "needed_statement": "no integrated-out curvature/scalar/nonlocal tower theorem",
            "current_status": "NO_INTEGRATED_OUT_TOWER_NOT_DERIVED",
            "blocker": "bare, hidden-source, boundary/readout, scalar-class, and effective-component gates remain unsigned",
            "zero_if_closed": "activates parent second-order/no-extra-scalar premise for the R2/fR zero theorem",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def effective_coefficient_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "CEC1789_0_effective_law",
            "component": "c_R2_eff",
            "formula": "c_R2_eff = c_bare + 1/2 B_R^T L_X^{-1} B_R + c_measure + c_boundary + c_field_redef_remnant",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_basis": "IP1710_3_effective_law_components;EID1789_1_effective_tail",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CEC1789_1_c_bare",
            "component": "bare higher-curvature coefficient",
            "formula": "coefficient of local R^2/f(R)/R F(Box)R term before eliminating hidden sectors",
            "current_value": "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE",
            "source_basis": "CH1710_1_bare_operator",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CEC1789_2_memory_vertex",
            "component": "B_R^T L_X^{-1} B_R",
            "formula": "curvature/source vertex times inverse hidden operator times curvature/source vertex",
            "current_value": "MISSING_B_X_L_INVERSE_MASS_GAP",
            "source_basis": "QMA970_6_integrated_out_tower;CH1710_2_memory_vertex",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CEC1789_3_measure_boundary",
            "component": "measure/Jacobian/boundary contribution",
            "formula": "c_measure + c_boundary from projection, field redefinition, corner/reference and readout terms",
            "current_value": "MISSING_MEASURE_BOUNDARY_FRAME_OWNER",
            "source_basis": "CH1710_4_measure_boundary;CE710_2_boundary_jacobian",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "CEC1789_4_verdict",
            "component": "claim-grade effective coefficient pack",
            "formula": "all coefficient values, units, signs, normalization, source paths, and observable maps supplied",
            "current_value": "NO_EXECUTABLE_COEFFICIENT_FOUND_CURRENT_CORPUS",
            "source_basis": "CH1710_6_verdict;IP1710_8_acceptance",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def finite_scalar_input_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_0_identity",
            "required_field": "model_id;operator_family",
            "current_value": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428;R2_fR_scalar_mode",
            "status": "READY_AS_CONTRACT_ONLY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_1_coefficient",
            "required_field": "c_R2_or_fRR",
            "current_value": "MISSING_PARENT_COEFFICIENT",
            "status": "BLOCKING_FIELD",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_2_units_normalization",
            "required_field": "coefficient_units;sign;normalization",
            "current_value": "MISSING_UNITS_SIGN_NORMALIZATION",
            "status": "BLOCKING_FIELD",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_3_scalaron_map",
            "required_field": "m_s_or_lambda_s;alpha_s;screening_flag;matter_coupling_frame",
            "current_value": "FORMULA_READY_PARENT_INPUT_MISSING",
            "status": "BLOCKING_FIELD",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_4_source_provenance",
            "required_field": "source_path;equation_ref;extraction_method",
            "current_value": "MISSING_SOURCE_PROVENANCE",
            "status": "BLOCKING_FIELD",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_5_arena_maps",
            "required_field": "R10_map;PPN_map;clock_map;orbital_map",
            "current_value": "MISSING_ARENA_PROJECTIONS",
            "status": "BLOCKING_FIELD",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "FSI1789_6_acceptance",
            "required_field": "zero_theorem_signed OR complete finite numeric row",
            "current_value": "NEITHER_CONDITION_MET",
            "status": "REJECT_CURRENT_INPUT_PACK",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1789_0_nonzero_hidden_source",
            "countermodel": "hidden memory/scalar source J_X is nonzero and integration generates -1/2 J L^-1 J",
            "survives_current_constraints": True,
            "why_survives": "source/boundary gates in 970 do not pass",
            "what_kills_it": "J_X=0 theorem plus boundary flux zero and zero-mode removal",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1789_1_curvature_vertex",
            "countermodel": "hidden sector couples to R, T, boundary curvature, or observed coframe and produces R L^-1 R",
            "survives_current_constraints": True,
            "why_survives": "curvature-coupled case is explicitly not excluded",
            "what_kills_it": "B_R=0/no-curvature-vertex theorem or finite c_R2_eff row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1789_2_readout_reduced_eft",
            "countermodel": "readout-reduced action is varied and creates a new EFT branch rather than parent theorem-zero",
            "survives_current_constraints": True,
            "why_survives": "readout-domain certificate is closure discipline, not primitive parent theorem",
            "what_kills_it": "prove readout occurs after variation or exclude readout masks from Conf_parent",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1789_3_scalar_class_prefactor",
            "countermodel": "quotient/scalar label enters F(sigma)R or a matter-frame transform",
            "survives_current_constraints": True,
            "why_survives": "710 descent clauses are candidate-only and counterexamples remain live",
            "what_kills_it": "derive DPC710_0 through DPC710_7 from quotient geometry",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1789_4_anchor_backsolve",
            "countermodel": "R10 anchors are used to infer MTS c_R2/fRR instead of testing a parent prediction",
            "survives_current_constraints": True,
            "why_survives": "1710 runner refusal forbids anchor backsolve and prediction is missing",
            "what_kills_it": "parent-sourced coefficient and full curve comparison",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1789_0_no_tower",
            "claim": "eliminated sectors cannot regenerate R2/fR/Yukawa/nonlocal terms",
            "status": "BLOCKED",
            "reason": "source, curvature-vertex, boundary/readout, and scalar-class gates are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1789_1_cR2_zero",
            "claim": "c_R2/fRR theorem-zero",
            "status": "BLOCKED",
            "reason": "no integrated-out tower is a missing premise for activating the relative R2/fR theorem",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1789_2_finite_prediction",
            "claim": "finite scalaron prediction row is executable",
            "status": "BLOCKED",
            "reason": "coefficient, units, normalization, screening, source path, and arena maps are missing",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1789_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED",
            "reason": "R2/fR remains an open component of the hybrid extra-sector silence matrix",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1789_0_identity",
            "decision": "ELIMINATION_IDENTITY_IS_EXACT_CONDITIONAL",
            "reason": "quadratic hidden-sector elimination necessarily produces -1/2<J,L^-1J> unless J/boundary vanish",
            "next_action": "use this as the coefficient-owner law, not as a pass",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1789_1_no_tower_status",
            "decision": "NO_INTEGRATED_OUT_TOWER_NOT_DERIVED",
            "reason": "current corpus does not prove source zero, curvature-vertex absence, boundary/readout silence, or scalar-class descent",
            "next_action": "attack the owner of J_X/B_R/L_X rather than looping on broad minimality language",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1789_2_input_pack_status",
            "decision": "FINITE_SCALAR_INPUT_PACK_REJECTED_NONCLAIM",
            "reason": "1710 already shows the c_R2/fRR input pack lacks coefficient, units, maps, and source paths",
            "next_action": "run a strict owner-bundle gate before any curve QA",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1789_3_next",
            "decision": "GAMMA_KHAT_PLOC_OWNER_BUNDLE_OR_CR2_INPUT_PACK_SMOKE_IS_NEXT",
            "reason": "the next narrow owner is the response/source bundle that could set B_R/J_X to zero or supply finite c_R2_eff inputs",
            "next_action": "build 1790 owner-bundle gate and reject incomplete input packs by schema",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1789_0_primary",
            "next_target": "1790-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-input-pack-smoke-runner.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_Ploc_owner_bundle_or_cR2_input_pack_smoke_runner.py",
            "objective": "attack the Gamma_eff/K_hat/P_loc response owner as the theorem route for J_X/B_R/c_R2_eff; if it fails, run a strict schema smoke validator that rejects incomplete c_R2/fRR input packs",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1789_1_parallel",
            "next_target": "1790b-Y5-R2FR-scalar-class-descent-clause-parent-ownership.md",
            "script": "scripts/Y5_R2FR_scalar_class_descent_clause_parent_ownership.py",
            "objective": "derive DPC710 scalar/class descent clauses from quotient geometry or keep scalar zero route closure-only",
            "selection_status": "queued_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1789_2_data",
            "next_target": "1790c-Y5-R2FR-R10-curve-QA-only-after-cR2-prediction.md",
            "script": "scripts/Y5_R2FR_R10_curve_QA_only_after_cR2_prediction.py",
            "objective": "hold curve QA until a real MTS alpha/lambda prediction exists; anchors remain smoke-only",
            "selection_status": "held_until_prediction",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "elimination_identity": elimination_identity_rows(),
        "tower_exclusion_gate": tower_exclusion_gate_rows(),
        "effective_coefficient_pack": effective_coefficient_pack_rows(),
        "finite_scalar_input_pack": finite_scalar_input_pack_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
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
        shutil.copy2(path, RAB_QUEUE / f"JR1789_{key.upper()}.csv")


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
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
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
        if not (RAB_QUEUE / f"JR1789_{key.upper()}.csv").exists():
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
        ("VAL1789_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1789_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1789_2_identity_written",
            any(
                row["identity_id"] == "EID1789_1_effective_tail"
                and row["result"] == "EXACT_CONDITIONAL_IDENTITY"
                for row in rows_map["elimination_identity"]
            ),
            "integrated-out Green-function identity is written",
        ),
        (
            "VAL1789_3_safe_zero_not_promoted",
            any(
                row["identity_id"] == "EID1789_4_verdict"
                and row["result"] == "SAFE_ZERO_CASE_NOT_PARENT_SIGNED"
                for row in rows_map["elimination_identity"]
            ),
            "safe zero case is not promoted",
        ),
        (
            "VAL1789_4_tower_gate_blocks",
            any(
                row["gate_id"] == "NIT1789_5_verdict"
                and row["current_status"] == "NO_INTEGRATED_OUT_TOWER_NOT_DERIVED"
                for row in rows_map["tower_exclusion_gate"]
            )
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["tower_exclusion_gate"]),
            "no-integrated-out tower gate remains unsigned",
        ),
        (
            "VAL1789_5_effective_pack_nonclaim",
            any(
                row["component_id"] == "CEC1789_4_verdict"
                and row["current_value"] == "NO_EXECUTABLE_COEFFICIENT_FOUND_CURRENT_CORPUS"
                for row in rows_map["effective_coefficient_pack"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["effective_coefficient_pack"]),
            "effective coefficient pack is nonclaim and not score-ready",
        ),
        (
            "VAL1789_6_input_pack_rejected",
            any(
                row["pack_id"] == "FSI1789_6_acceptance"
                and row["status"] == "REJECT_CURRENT_INPUT_PACK"
                for row in rows_map["finite_scalar_input_pack"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["finite_scalar_input_pack"]),
            "finite scalar input pack is rejected by strict schema",
        ),
        (
            "VAL1789_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live",
        ),
        (
            "VAL1789_8_claim_gates_blocked",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["gate_pass"])
                and row["status"] == "BLOCKED"
                for row in rows_map["claim_gate"]
            ),
            "claim gates are blocked",
        ),
        ("VAL1789_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1789_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1789_11_decision_next",
            any(
                row["decision_id"] == "DEC1789_3_next"
                and row["decision"] == "GAMMA_KHAT_PLOC_OWNER_BUNDLE_OR_CR2_INPUT_PACK_SMOKE_IS_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects owner-bundle/input-pack smoke next",
        ),
        (
            "VAL1789_12_next_selected",
            any(row["route_id"] == "NEXT1789_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1789_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1789 CSVs parse"),
        ("VAL1789_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1789_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1789_16_formalization_untouched", formalization_untouched(), "no 1789 outputs found under formalization-workbench"),
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
            "check_id": "VAL1789_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1789 no-integrated-out curvature tower or finite scalar bound pack checkpoint",
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
            "# 1789 - Y5/R2FR No Integrated-Out Curvature Tower or Finite Scalar Bound Pack",
            "",
            "## Verdict",
            "",
            "1789 isolates the exact danger in the R2/fR route. Eliminating a quadratic hidden sector is not automatically harmless. If `S_X = 1/2<X,L_X X> - <J_X,X>`, then solving `E_X=0` gives `S_eff = S_rest - 1/2<J_X,L_X^{-1}J_X>` plus boundary/readout terms. If `J_X` contains curvature, matter, boundary, or coframe pieces, the reduced action can regenerate `R L_X^{-1} R`, local `R^2/f(R)` expansions, Yukawa forces, or nonlocal kernels.",
            "",
            "So the no-integrated-out tower theorem is not derived. The safe branch needs `J_X=0`, zero boundary flux, zero/readout-safe modes, and no scalar/class/matter-frame leakage before elimination. Current corpus does not sign those clauses. The finite scalar branch also remains rejected because the `c_R2/fRR` coefficient pack has no source-backed value, units, normalization, screening map, or arena projections.",
            "",
            "**Claim ceiling:** no no-tower theorem, no `c_R2/fRR=0` theorem, no scalaron score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1789.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Elimination Identity Gate",
            markdown_table(rows_map["elimination_identity"], ["identity_id", "claim", "mathematical_form", "result", "source_basis", "valid_for_claim"]),
            "",
            "## No Integrated-Out Tower Gate",
            markdown_table(rows_map["tower_exclusion_gate"], ["gate_id", "needed_statement", "current_status", "blocker", "zero_if_closed", "valid_for_claim"]),
            "",
            "## Effective cR2 Coefficient Pack",
            markdown_table(rows_map["effective_coefficient_pack"], ["component_id", "component", "formula", "current_value", "source_basis", "score_ready", "valid_for_claim"]),
            "",
            "## Finite Scalar Input Pack",
            markdown_table(rows_map["finite_scalar_input_pack"], ["pack_id", "required_field", "current_value", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful tightening of the theory. The problem is not vaguely 'higher derivatives'. It is a named source-response law: either the parent proves the hidden-sector source and curvature vertex vanish before elimination, or the scalar channel must be treated as a finite response with real coefficients. Next, the right move is to hunt the `Gamma_eff/K_hat/P_loc` owner bundle that could actually own or kill `J_X`, `B_R`, and `c_R2_eff`.",
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
    print(f"1789 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
