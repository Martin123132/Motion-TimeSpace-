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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1826"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1826-Y5-R2FR-log-holonomy-action-owner-or-trace-norm-c2-prior.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1826_0_1825_next",
        "source_key": "1825_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_NEXT_TARGET.csv",
        "needles": ["NEXT1825_0_primary", "selected"],
        "role": "1825 selects log-holonomy action ownership versus trace/norm c2 prior as the next target.",
    },
    {
        "source_id": "SRC1826_1_1825_validation",
        "source_key": "1825_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1825_VALIDATION.csv",
        "needles": ["VAL1825_OVERALL", "PASS"],
        "role": "confirms 1825 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1826_2_1825_oddness",
        "source_key": "1825_signed_deficit_oddness",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_SIGNED_DEFICIT_ODDNESS_THEOREM_ATTEMPT.csv",
        "needles": ["SDO1825_4_log_angle_route", "LOG_ANGLE_OWNER_MISSING"],
        "role": "identifies signed log-angle ownership as the best unresolved zero route.",
    },
    {
        "source_id": "SRC1826_3_1825_owner",
        "source_key": "1825_orientation_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_ORIENTATION_OWNER_AUDIT.csv",
        "needles": ["OOA1825_4_verdict", "FAIL_CURRENT_OWNER_STACK"],
        "role": "shows the current physical orientation/action owner stack fails.",
    },
    {
        "source_id": "SRC1826_4_1825_c2",
        "source_key": "1825_c2_prior",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1825_C2_PRIOR_SOURCE_ROW.csv",
        "needles": ["C2P1825_4_total", "MISSING_ZERO_OR_FINITE_PRIOR_ROW_NONCLAIM"],
        "role": "keeps c2 visible as explicit nonclaim coefficient debt.",
    },
    {
        "source_id": "SRC1826_5_1823_regge_bridge",
        "source_key": "1823_regge_bridge",
        "source_path": ROOT / "1823-Y5-R2FR-primitive-deficit-action-law-or-visible-c2-owner-row.md",
        "needles": ["DAL1823_1_Regge_EH_bridge", "MTS_PRIMITIVE_ACTION_LAW_UNSIGNED"],
        "role": "records the known conditional Regge/EH bridge and its unsigned MTS status.",
    },
    {
        "source_id": "SRC1826_6_1165_lifted_action",
        "source_key": "1165_lifted_C_action_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv",
        "needles": ["LPC1165_2_parent_action_term", "ACTION_CONTRACT_STUB_ONLY"],
        "role": "parent action term remains a contract stub, not a signed Lagrangian.",
    },
    {
        "source_id": "SRC1826_7_920_holonomy",
        "source_key": "920_holonomy_zero",
        "source_path": RESIDUALS / "P8_Y5_R10_920_HOLONOMY_ZERO_AUDIT.csv",
        "needles": ["HOL920_3_nontrivial_cycle_fallback", "retained_bound_row"],
        "role": "nontrivial holonomy cycles remain retained residual/bound rows.",
    },
    {
        "source_id": "SRC1826_8_867_orientation_arrow",
        "source_key": "867_orientation_arrow",
        "source_path": RESIDUALS / "P8_Y5_R10_867_ORIENTATION_ARROW_AUDIT.csv",
        "needles": ["OA867_1_boundary_orientation_flip", "mathematically_viable_but_unsigned"],
        "role": "boundary orientation flip is viable but still unsigned.",
    },
    {
        "source_id": "SRC1826_9_881_orientation_signature",
        "source_key": "881_orientation_signature",
        "source_path": RESIDUALS / "P8_Y5_R10_881_ORIENTATION_SIGNATURE_AUDIT.csv",
        "needles": ["OS881_4_orientation_verdict", "partial_progress_nonclaim"],
        "role": "relative-chain orientation remains partial progress, not a parent action owner.",
    },
    {
        "source_id": "SRC1826_10_1561_EH_ansatz",
        "source_key": "1561_minimal_EH_ansatz",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["ANS1561_C_EH_only", "not adopted"],
        "role": "EH core is available as a conditional ansatz but not adopted as MTS parent theory.",
    },
    {
        "source_id": "SRC1826_11_463_EH_R11_gate",
        "source_key": "463_EH_only_R11_gate",
        "source_path": ROOT / "463-EH-only-or-R11-executable-vector-gate.md",
        "needles": ["EHV2_Lovelock_assumptions_earned", "R2_fR_scalar_mode"],
        "role": "EH-only/Lovelock assumptions and R2/fR vector remain unearned/unfilled.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_SOURCE_REGISTER.csv",
    "log_owner_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_LOG_HOLONOMY_ACTION_OWNER_ATTEMPT.csv",
    "palatini_regge_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_PALATINI_REGGE_OWNER_CONTRACT.csv",
    "trace_norm_prior": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_TRACE_NORM_C2_PRIOR_ROWS.csv",
    "gauge_orientation_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_GAUGE_ORIENTATION_AUDIT.csv",
    "decision_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_C2_DECISION_MATRIX.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1826_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "log_owner_attempt": log_owner_attempt_rows(),
        "palatini_regge_contract": palatini_regge_contract_rows(),
        "trace_norm_prior": trace_norm_prior_rows(),
        "gauge_orientation_audit": gauge_orientation_audit_rows(),
        "decision_matrix": decision_matrix_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }
    return rows


def log_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_0_target",
            "claim_piece": "signed log-holonomy action owner",
            "mathematical_statement": "Derive that each primitive local cell/hinge contributes S_h = kappa A_h delta_h + boundary, where delta_h is the signed small-angle logarithm of the holonomy, not a class trace or norm.",
            "derivation_result": "TARGET_ATTEMPTED",
            "current_status": "NOT_PARENT_PROVEN",
            "consequence": "c2_visible cannot be zeroed from this checkpoint alone",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_1_exact_log_math",
            "claim_piece": "signed log angle is odd",
            "mathematical_statement": "For U_h = exp(delta_h J_h) in a fixed small-curvature branch, reversing the oriented hinge sends delta_h -> -delta_h; a linear response Phi(delta_h)=k1 delta_h has Phi''(0)=0.",
            "derivation_result": "EXACT_CONDITIONAL_LEMMA",
            "current_status": "MATH_OK_OWNER_UNSIGNED",
            "consequence": "the zero mechanism is real if the parent action chooses this signed variable",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_2_palatini_regge_bridge",
            "claim_piece": "linear curvature action bridge",
            "mathematical_statement": "A Palatini/Regge-shaped action, int epsilon e e F or sum_h A_h delta_h, is linear in curvature/deficit and has the right EH-continuum shape under its own assumptions.",
            "derivation_result": "CONDITIONAL_BRIDGE_READY",
            "current_status": "MTS_FIELD_OWNERSHIP_UNSIGNED",
            "consequence": "this is the best derivation route, but not a proof that MTS owns the route",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_3_gauge_scalar_problem",
            "claim_piece": "make log holonomy an action scalar",
            "mathematical_statement": "Log(U_h) is gauge-covariant, not automatically an action scalar; it must be paired with a parent-owned oriented bivector/coframe/hinge generator before tracing or contracting.",
            "derivation_result": "OWNER_REQUIREMENT_IDENTIFIED",
            "current_status": "BIVECTOR_COFAME_MATCH_MISSING",
            "consequence": "trace and norm actions remain legal countermodels until this pairing is derived",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_4_variation_stress_problem",
            "claim_piece": "action-level variation",
            "mathematical_statement": "The owner must supply fields, variation variables, boundary terms, and Bianchi/Ward stress accounting; a named holonomy action without variation is not a parent derivation.",
            "derivation_result": "ACTION_CONTRACT_REQUIRED",
            "current_status": "VARIATION_NOT_SUPPLIED",
            "consequence": "cannot promote local EH/GR even if the action shape is attractive",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_5_cycle_residual_problem",
            "claim_piece": "local holonomy silence",
            "mathematical_statement": "Even a log-holonomy branch must account for local domains with nontrivial cycles, defects, branch cuts, or boundary holonomy residuals.",
            "derivation_result": "RESIDUAL_ROUTE_RETAINED",
            "current_status": "NONTRIVIAL_CYCLE_FALLBACK_LIVE",
            "consequence": "R10/PPN/local rows stay blocked unless cycles are excluded or bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGO1826_6_verdict",
            "claim_piece": "1826 proves log-holonomy action ownership",
            "mathematical_statement": "1826 constructs the exact owner contract that would make the visible c2 zero route credible, but current sources do not yet identify MTS variables with a parent Palatini/Regge action and variation.",
            "derivation_result": "CONTRACT_SHARPENED_NOT_SIGNED",
            "current_status": "DEMOTE_TO_CONTRACT_PLUS_C2_PRIOR",
            "consequence": "next step must field-match the Palatini/Regge contract or fill finite c2/scalaron rows",
            "valid_for_claim": False,
        },
    ]


def palatini_regge_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_0_field_list",
            "required_owner": "MTS field match to coframe/connection/hinge data",
            "contract_expression": "e^I_mu, omega^{IJ}_mu, F^{IJ}[omega], B_h ~ integral_h e wedge e, U_h = P exp integral omega",
            "current_status": "MISSING_MTS_FIELD_MATCH",
            "missing_piece": "map Q/load/motion variables to observed coframe, compatible connection, and oriented hinge bivector",
            "would_unlock": "gauge-covariant log holonomy can become a parent scalar density",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_1_action_term",
            "required_owner": "linear curvature/deficit action",
            "contract_expression": "S_grav = kappa int epsilon_IJKL e^I wedge e^J wedge F^{KL} or S_cell = kappa sum_h A_h delta_h",
            "current_status": "CONTRACT_SHAPE_READY_NOT_MTS_DERIVED",
            "missing_piece": "derive this term from MTS parent grammar rather than importing EH/Regge as a repair ansatz",
            "would_unlock": "linear response and no visible c2 at the primitive level",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_2_signed_branch",
            "required_owner": "physical signed angle branch",
            "contract_expression": "delta_h = <sigma_h, Log U_h> in a parent-selected small-curvature branch with orientation reversal delta_h -> -delta_h",
            "current_status": "BRANCH_AND_ORIENTATION_NOT_PARENT_SIGNED",
            "missing_piece": "relative-chain orientation, branch convention, and physical-not-gauge reversal theorem",
            "would_unlock": "Phi(-delta)=-Phi(delta) becomes a parent statement instead of a convention",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_3_not_trace_norm",
            "required_owner": "exclude even holonomy costs",
            "contract_expression": "Phi is not Tr(I-U), 1-cos(delta), ||Log U||^2, delta^2, entropy, or positive mismatch energy",
            "current_status": "NOT_EXCLUDED",
            "missing_piece": "parent minimality/linearity principle that chooses first-moment signed deficit over class-function energy",
            "would_unlock": "removes the main c2 countermodels",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_4_variation_and_stress",
            "required_owner": "Euler/Ward/Bianchi-safe variation",
            "contract_expression": "delta S_parent = E_e delta e + E_omega delta omega + d theta, with boundary/projector/source stresses retained",
            "current_status": "VARIATION_NOT_WRITTEN_FOR_THIS_OWNER",
            "missing_piece": "explicit parent Lagrangian density, variables, boundary terms, and stress tensor",
            "would_unlock": "prevents fake EH import and fake stress deletion",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_5_continuum_limit",
            "required_owner": "Regge/EH continuum map",
            "contract_expression": "sum_h A_h delta_h -> const * int sqrt(-g) R plus controlled boundary and higher-order errors",
            "current_status": "KNOWN_CONDITIONAL_BRIDGE_MTS_PREMISES_UNSIGNED",
            "missing_piece": "cell refinement/locality/shape-factor assumptions and MTS primitive cell identification",
            "would_unlock": "connects the primitive action to GR rather than just to a symbolic zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PRC1826_6_total",
            "required_owner": "Palatini/Regge owner closes current c2 route",
            "contract_expression": "PRC1826_0 through PRC1826_5 all pass in one parent action with no hidden trace/norm term",
            "current_status": "CONTRACT_WRITTEN_NOT_SIGNED",
            "missing_piece": "single parent action tying MTS fields to linear oriented curvature and matter/readout descent",
            "would_unlock": "conditional zero of visible c2 becomes promotable only after these clauses close",
            "valid_for_claim": False,
        },
    ]


def trace_norm_prior_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_0_trace_cost",
            "row_type": "finite_prior_example",
            "quantity": "c2_visible",
            "formula_or_value": "1/2 for Phi(delta)=1-cos(delta) under the current expansion convention",
            "required_inputs": "parent selection of trace/class holonomy cost; normalization convention; source path",
            "units": "dimensionless_deficit_response",
            "current_status": "EXAMPLE_ONLY_PARENT_SELECTION_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_1_norm_cost",
            "row_type": "finite_prior_example",
            "quantity": "c2_visible",
            "formula_or_value": "1 for Phi(delta)=delta^2 or ||Log U||^2 under the current expansion convention",
            "required_inputs": "parent selection of squared norm/mismatch energy; normalization convention; source path",
            "units": "dimensionless_deficit_response",
            "current_status": "EXAMPLE_ONLY_PARENT_SELECTION_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_2_general_analytic",
            "row_type": "finite_c2_prior_source_row",
            "quantity": "c2_visible",
            "formula_or_value": "c2_visible = 1/2 Phi''(0)",
            "required_inputs": "parent Phi expansion; sign; uncertainty/prior width; cell scale; shape factor; source path",
            "units": "dimensionless_deficit_response",
            "current_status": "MISSING_PARENT_PHI_AND_PRIOR_WIDTH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_3_R2_map",
            "row_type": "continuum_map",
            "quantity": "c_R2_eff",
            "formula_or_value": "c_R2_eff ~ shape_factor * c2_visible * ell_cell^2 / EH_normalization",
            "required_inputs": "ell_cell; shape_factor; EH normalization; continuum reduction convention; source path",
            "units": "length_squared_or_declared_operator_units",
            "current_status": "MISSING_CELL_SCALE_SHAPE_AND_EH_NORMALIZATION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_4_observable_map",
            "row_type": "scalaron_or_R11_map",
            "quantity": "alpha_lambda_gamma_beta_map",
            "formula_or_value": "map c_R2_eff into scalar mass/coupling, alpha(lambda), gamma-1, beta-1, and R11 operator rows",
            "required_inputs": "weak-field linearization; matter coupling; source normalization; R10 bound curve; PPN response map",
            "units": "mixed_observable_units",
            "current_status": "MISSING_WEAK_FIELD_AND_LOCAL_BOUND_MAPS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TNF1826_5_total",
            "row_type": "trace_norm_c2_prior_contract",
            "quantity": "visible_c2_to_R2FR_scalar_mode",
            "formula_or_value": "valid only after TNF1826_2, TNF1826_3, and TNF1826_4 are sourced",
            "required_inputs": "finite c2 prior; continuum map; scalaron/PPN/R10 map; source paths; no-cancellation policy",
            "units": "row_contract",
            "current_status": "C2_PRIOR_CONTRACT_READY_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def gauge_orientation_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GOA1826_0_trace_invariant",
            "issue": "trace/class functions are gauge-natural but even",
            "technical_point": "Tr(U), Tr(I-U), and 1-cos(delta) do not retain the sign of a small oriented angle.",
            "current_status": "COUNTERMODEL_LIVE",
            "needed_to_close": "derive that MTS does not use class-function trace energy as the primitive action",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GOA1826_1_log_covariant",
            "issue": "Log(U) is covariant before contraction",
            "technical_point": "A signed log-holonomy term needs an owned bivector/generator sigma_h so <sigma_h, Log U_h> is a physical scalar density.",
            "current_status": "BIVECTOR_OWNER_MISSING",
            "needed_to_close": "map MTS coframe/load primitive to the oriented hinge bivector and show covariance",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GOA1826_2_orientation_physical",
            "issue": "orientation reversal may be gauge or physical",
            "technical_point": "If delta -> -delta is just a representative relabeling, the action should be invariant; if it is a physical boundary-charge orientation, an odd term can be meaningful.",
            "current_status": "PHYSICAL_ORIENTATION_UNSIGNED",
            "needed_to_close": "parent relative-chain action owner plus root/arrow assignment",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GOA1826_3_branch_domain",
            "issue": "small-angle log branch must be selected",
            "technical_point": "The local log map is clean only on a chosen small-curvature branch; defects/cycles/large holonomies become residual rows.",
            "current_status": "LOCAL_BRANCH_AND_CYCLE_GUARD_MISSING",
            "needed_to_close": "admissible local topology theorem or retained holonomy residual bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GOA1826_4_verdict",
            "issue": "gauge/orientation status of log-holonomy owner",
            "technical_point": "Log-angle ownership is mathematically coherent, but current MTS does not yet own the scalar contraction, physical orientation, or branch domain.",
            "current_status": "GAUGE_ORIENTATION_STACK_BLOCKED",
            "needed_to_close": "Palatini/Regge field match and relative-chain orientation theorem",
            "valid_for_claim": False,
        },
    ]


def decision_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "CDM1826_0_log_owner",
            "route": "Palatini/Regge signed log-holonomy owner",
            "current_result": "BEST_DERIVATION_ROUTE_CONTRACT_ONLY",
            "why": "linear oriented curvature is exactly the structure that would kill visible c2 while connecting to EH",
            "risk": "MTS field ownership, variation, and matter descent are not signed",
            "selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "CDM1826_1_trace_norm",
            "route": "trace/norm c2 prior branch",
            "current_result": "FALLBACK_NONCLAIM_ROW_READY",
            "why": "if the parent action is an even holonomy energy, c2 must be explicit and tested",
            "risk": "no parent Phi, cell scale, continuum map, or scalaron/local bound map yet",
            "selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "CDM1826_2_import_EH_warning",
            "route": "import EH action directly",
            "current_result": "REJECT_AS_DERIVATION",
            "why": "using EH as an ansatz can benchmark the target but does not prove MTS reduces to GR",
            "risk": "would smuggle in the conclusion the project is trying to derive",
            "selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "CDM1826_3_best_next",
            "route": "field-match Palatini/Regge owner or build finite c2 scalaron map",
            "current_result": "NEXT_TARGET_SELECTED",
            "why": "this is the narrowest honest fork after 1826",
            "risk": "if field match fails, R2/fR remains a live bounded-residual branch",
            "selected_for_claim": False,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1826_0_if_owner_closes",
            "if_closed": "MTS parent action is field-matched to Palatini/Regge linear oriented curvature with no trace/norm c2 term",
            "would_buy": "visible c2/R2 primitive wound can close by theorem and the EH bridge becomes much more serious",
            "still_missing": "higher odd terms, connection compatibility, matter/source descent, PPN beta, q_loc, and local-bound maps",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1826_1_if_trace_norm",
            "if_closed": "parent action is trace/norm/even holonomy cost",
            "would_buy": "honest finite residual branch with c2_visible rather than vague failure",
            "still_missing": "Phi, c2 uncertainty, c_R2_eff, scalaron coupling/mass, R10/PPN maps",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1826_2_verdict",
            "if_closed": "1826 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone",
            "still_missing": "1826 writes a contract and fallback rows; it does not derive the parent action",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1826_0_contract_written",
            "gate": "Palatini/Regge log-holonomy owner contract written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1826 states the exact field/action/variation clauses needed",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1826_1_field_match",
            "gate": "MTS fields matched to coframe/connection/hinge variables",
            "current_status": "BLOCKED",
            "reason": "Q/load/motion variables are not yet identified with e, omega, F, B_h, and U_h in one parent action",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1826_2_not_trace_norm",
            "gate": "trace/norm/even holonomy costs excluded",
            "current_status": "BLOCKED",
            "reason": "even cost countermodels remain live",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1826_3_variation",
            "gate": "Euler/Ward/Bianchi-safe parent variation written",
            "current_status": "BLOCKED",
            "reason": "action variables, boundary terms, and stress accounting are not supplied",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1826_4_c2_prior",
            "gate": "finite c2 prior/scalaron branch score-ready",
            "current_status": "BLOCKED",
            "reason": "parent Phi, c_R2_eff, scalaron/PPN/R10 maps are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1826_0_log_owner",
            "claim": "parent action owns signed log-holonomy",
            "status": "BLOCKED",
            "reason": "Palatini/Regge contract is written but not matched to MTS fields or varied",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1826_1_c2_zero",
            "claim": "c2_visible=0",
            "status": "BLOCKED",
            "reason": "zero follows only if signed linear owner clauses pass",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1826_2_finite_c2_score",
            "claim": "finite c2/R2/fR branch is score-ready",
            "status": "BLOCKED",
            "reason": "trace/norm prior rows are examples/contracts, not sourced predictions",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1826_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "REFUSED",
            "reason": "operator, source, q_loc, matter descent, PPN, and local-bound gates remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1826_0_owner_result",
            "decision": "LOG_HOLONOMY_OWNER_NOT_PROVEN",
            "reason": "the Palatini/Regge shape is the right mathematical route, but current MTS does not yet own the fields, orientation, variation, or trace/norm exclusion",
            "next_action": "do not set c2_visible to zero",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1826_1_best_route",
            "decision": "PALATINI_REGGE_FIELD_MATCH_NEXT",
            "reason": "field-matching MTS primitives to e, omega, F, B_h and U_h is the least-cheaty derivation path",
            "next_action": "attempt parent field/action match before filling numeric c2 rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1826_2_fallback",
            "decision": "TRACE_NORM_C2_SCALARON_MAP_READY_NONCLAIM",
            "reason": "if the linear owner fails, the honest branch is finite c2 plus R2/fR scalaron/PPN/R10 mapping",
            "next_action": "keep fallback valid_for_claim=false until all inputs are sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1826_3_best_next",
            "decision": "FIELD_MATCH_OR_C2_SCALARON_MAP_NEXT",
            "reason": "1826 reduces the issue from broad oddness to a concrete parent action fork",
            "next_action": "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1826_0_primary",
            "next_target": "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md",
            "script": "scripts/Y5_R2FR_Palatini_Regge_field_match_or_c2_scalaron_map.py",
            "objective": "try to map MTS parent variables to a Palatini/Regge linear curvature action; if this fails, build the finite c2-to-R2/fR scalaron map as nonclaim rows",
            "selection_status": "selected",
            "success_condition": "field/action/variation owner signed, or finite c2/scalaron rows remain valid_for_claim=false with all missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1826_1_parallel",
            "next_target": "1827b-Y5-R2FR-higher-odd-term-gate-if-c2-zero.md",
            "script": "scripts/Y5_R2FR_higher_odd_term_gate_if_c2_zero.py",
            "objective": "only if c2 is zeroed by a signed owner, audit cubic and higher odd curvature terms before any EH/local-GR claim",
            "selection_status": "held_parallel",
            "success_condition": "higher odd terms are theorem-zero, bounded, or retained nonclaim",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed", "score_ready", "selected_for_claim"}
    for rows in rows_map.values():
        for row in rows:
            for key in guarded_keys.intersection(row):
                if str(row[key]).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness_keys = ["valid_for_claim", "claim_allowed", "score_ready", "selected_for_claim"]
    for rows in rows_map.values():
        for row in rows:
            has_missing = any("MISSING" in str(value) for value in row.values())
            if not has_missing:
                continue
            if any(str(row.get(key, "")).lower() == "true" for key in readiness_keys):
                return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1826-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1826") or name.startswith("P8_Y5_BRR545_1826"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1826_0_sources_exist",
            all(str(row["exists"]).lower() == "true" for row in source_rows),
            "all cited source paths exist",
        ),
        (
            "VAL1826_1_needles_present",
            all(str(row["needles_present"]).lower() == "true" for row in source_rows),
            "all cited source needles are present",
        ),
        (
            "VAL1826_2_log_owner_attempt_written",
            any(row["attempt_id"] == "LGO1826_0_target" for row in rows_map["log_owner_attempt"]),
            "log-holonomy action owner attempt is written",
        ),
        (
            "VAL1826_3_exact_log_math_nonclaim",
            any(
                row["attempt_id"] == "LGO1826_1_exact_log_math"
                and row["derivation_result"] == "EXACT_CONDITIONAL_LEMMA"
                and row["valid_for_claim"] is False
                for row in rows_map["log_owner_attempt"]
            ),
            "signed log-angle math is exact but owner premise remains unsigned",
        ),
        (
            "VAL1826_4_owner_not_promoted",
            any(
                row["attempt_id"] == "LGO1826_6_verdict"
                and row["derivation_result"] == "CONTRACT_SHARPENED_NOT_SIGNED"
                and row["valid_for_claim"] is False
                for row in rows_map["log_owner_attempt"]
            ),
            "1826 owner route is not promoted as current proof",
        ),
        (
            "VAL1826_5_palatini_contract_nonclaim",
            any(
                row["contract_id"] == "PRC1826_6_total"
                and row["current_status"] == "CONTRACT_WRITTEN_NOT_SIGNED"
                and row["valid_for_claim"] is False
                for row in rows_map["palatini_regge_contract"]
            ),
            "Palatini/Regge contract is written but unsigned",
        ),
        (
            "VAL1826_6_trace_norm_prior_nonclaim",
            any(
                row["row_id"] == "TNF1826_5_total"
                and row["current_status"] == "C2_PRIOR_CONTRACT_READY_NONCLAIM"
                and row["score_ready"] is False
                and row["valid_for_claim"] is False
                for row in rows_map["trace_norm_prior"]
            ),
            "trace/norm c2 prior rows are nonclaim",
        ),
        (
            "VAL1826_7_gauge_orientation_blocked",
            any(
                row["audit_id"] == "GOA1826_4_verdict"
                and row["current_status"] == "GAUGE_ORIENTATION_STACK_BLOCKED"
                for row in rows_map["gauge_orientation_audit"]
            ),
            "gauge/orientation stack remains blocked",
        ),
        (
            "VAL1826_8_decision_matrix_fork",
            any(row["decision_id"] == "CDM1826_3_best_next" for row in rows_map["decision_matrix"]),
            "decision matrix selects the field-match versus c2-scalar map fork",
        ),
        (
            "VAL1826_9_gr_newton_nonclaim",
            all(row["valid_for_claim"] is False and row["claim_allowed_now"] is False for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1826_10_acceptance_blocks",
            any(
                row["gate_id"] == "AC1826_0_contract_written"
                and row["gate_pass"] is True
                and row["claim_allowed"] is False
                for row in rows_map["acceptance_gate"]
            )
            and all(row["claim_allowed"] is False for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1826_11_claim_gates_blocked",
            all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in rows_map["claim_gate"]),
            "all log-owner/c2/local-GR claim gates remain blocked or refused",
        ),
        (
            "VAL1826_12_no_claim_flags",
            no_claim_flags(rows_map),
            "no generated score/claim flags are true",
        ),
        (
            "VAL1826_13_missing_not_ready",
            missing_rows_not_ready(rows_map),
            "no MISSING_* row is marked ready",
        ),
        (
            "VAL1826_14_decision_next",
            any(
                row["decision_id"] == "DEC1826_3_best_next"
                and row["decision"] == "FIELD_MATCH_OR_C2_SCALARON_MAP_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects field-match or c2-scalar map next",
        ),
        (
            "VAL1826_15_next_selected",
            any(
                row["route_id"] == "NEXT1826_0_primary"
                and row["selection_status"] == "selected"
                for row in rows_map["next_target"]
            ),
            "next target selected",
        ),
        (
            "VAL1826_16_csv_parse",
            csv_parse_ok(output_paths),
            "all generated 1826 CSVs parse",
        ),
        (
            "VAL1826_17_branch_copies",
            branch_copies_exist(copied_paths),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1826_18_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1826_19_formalization_untouched",
            no_formalization_outputs(),
            "no 1826 outputs found under formalization-workbench",
        ),
    ]
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall = all(row["result"] == "PASS" for row in validation_rows)
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1826_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1826 log-holonomy action owner or trace/norm c2 prior checkpoint",
        }
    )
    return validation_rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1826 Y5 R2FR log-holonomy action owner or trace-norm c2 prior",
            "",
            "**Progress:** 1826 turns the oddness problem into a sharper parent-action fork. A Palatini/Regge-shaped action, `int e e F` or `sum A_h delta_h`, is the clean derivation route because it is linear in oriented curvature/deficit. But that shape is not yet owned by MTS variables.",
            "",
            "**Current verdict:** no zero claim yet. The best route is now a field match: show that MTS primitives define the coframe, connection, oriented hinge bivector, signed log-holonomy branch, and variation of a linear curvature action. If that cannot be derived, the trace/norm `c2_visible` branch must be filled honestly as a finite nonclaim residual.",
            "",
            "**Claim ceiling:** no signed log-holonomy ownership claim, no `c2_visible=0` claim, no finite R2/fR score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1826.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Log-Holonomy Action Owner Attempt",
            markdown_table(rows_map["log_owner_attempt"], ["attempt_id", "claim_piece", "mathematical_statement", "derivation_result", "current_status", "consequence", "valid_for_claim"]),
            "",
            "## Palatini Regge Owner Contract",
            markdown_table(rows_map["palatini_regge_contract"], ["contract_id", "required_owner", "contract_expression", "current_status", "missing_piece", "would_unlock", "valid_for_claim"]),
            "",
            "## Trace Norm C2 Prior Rows",
            markdown_table(rows_map["trace_norm_prior"], ["row_id", "row_type", "quantity", "formula_or_value", "required_inputs", "units", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Gauge Orientation Audit",
            markdown_table(rows_map["gauge_orientation_audit"], ["audit_id", "issue", "technical_point", "current_status", "needed_to_close", "valid_for_claim"]),
            "",
            "## C2 Decision Matrix",
            markdown_table(rows_map["decision_matrix"], ["decision_id", "route", "current_result", "why", "risk", "selected_for_claim", "valid_for_claim"]),
            "",
            "## GR Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
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
            "This is one of the better-looking forks in the local-GR chain, but it is still a fork. If MTS can own a Palatini/Regge-style linear curvature action, the visible quadratic wound has a clean route to closure. If MTS owns an even trace/norm energy instead, that is not death; it just means the theory must carry a finite `c2_visible` scalar-mode residual and survive the local tests honestly.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1826 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
