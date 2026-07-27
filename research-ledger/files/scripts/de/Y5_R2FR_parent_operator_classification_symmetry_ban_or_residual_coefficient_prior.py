from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1806"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1806_0_1805_doc",
        "source_key": "1805_doc",
        "source_path": ROOT / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md",
        "needles": ["NEXT1805_0_primary", "DEC1805_3_best_next"],
        "role": "1805 handoff selecting operator classification/symmetry ban next.",
    },
    {
        "source_id": "SRC1806_1_1805_validation",
        "source_key": "1805_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1805_VALIDATION.csv",
        "needles": ["VAL1805_OVERALL", "PASS"],
        "role": "confirms 1805 passed before 1806 starts.",
    },
    {
        "source_id": "SRC1806_2_1805_vertices",
        "source_key": "1805_vertices",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv",
        "needles": ["VT1805_1_scalar_F2", "VT1805_6_clock_readout_X"],
        "role": "current branch catalog of dangerous visible-sector vertices.",
    },
    {
        "source_id": "SRC1806_3_1805_bound_matrix",
        "source_key": "1805_bound_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
        "needles": ["BM1805_0_alpha_clock", "BM1805_4_PPN_source"],
        "role": "current branch fallback alpha/mass/clock bound matrix.",
    },
    {
        "source_id": "SRC1806_4_1049_doc",
        "source_key": "1049_doc",
        "source_path": ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
        "needles": ["OCR1049_5_verdict", "DEC1049_3_best_next"],
        "role": "older operator-classification/symmetry-ban checkpoint.",
    },
    {
        "source_id": "SRC1806_5_1049_operator",
        "source_key": "1049_operator",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
        "needles": ["OCR1049_2_product_sequestration", "OCR1049_5_verdict"],
        "role": "operator-classification route and product-sequestration status.",
    },
    {
        "source_id": "SRC1806_6_1049_symmetry",
        "source_key": "1049_symmetry",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
        "needles": ["SBT1049_0_diffeomorphism_covariance", "SBT1049_4_product_functor"],
        "role": "symmetry tests showing ordinary covariance/gauge invariance do not forbid the vertices.",
    },
    {
        "source_id": "SRC1806_7_1049_prior_slots",
        "source_key": "1049_prior_slots",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_RESIDUAL_PRIOR_SLOTS.csv",
        "needles": ["RP1049_0_b_alpha", "RP1049_5_qbar_constants_abs_prior"],
        "role": "older residual-prior slot template.",
    },
    {
        "source_id": "SRC1806_8_1049_prior_matrix",
        "source_key": "1049_prior_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_1049_ALPHA_MASS_CLOCK_PRIOR_MATRIX.csv",
        "needles": ["PM1049_0_clock_alpha_mu", "PM1049_3_PPN_source"],
        "role": "older nonclaim alpha/mass/clock prior projection matrix.",
    },
    {
        "source_id": "SRC1806_9_operator_requirements",
        "source_key": "operator_requirements",
        "source_path": RESIDUALS / "P8_OPERATOR_CLASSIFICATION_REQUIREMENTS.csv",
        "needles": ["retained_residual", "field_redefinition_redundant"],
        "role": "local operator classification requirements.",
    },
    {
        "source_id": "SRC1806_10_1050_doc",
        "source_key": "1050_doc",
        "source_path": ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
        "needles": ["PFT1050_5_verdict", "DEC1050_"],
        "role": "older product-functor target and prior-width handoff.",
    },
    {
        "source_id": "SRC1806_11_1050_product",
        "source_key": "1050_product",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["PFT1050_1_visible_action_pullback", "PFT1050_5_verdict"],
        "role": "product functor theorem attempt used to select 1807.",
    },
    {
        "source_id": "SRC1806_12_1050_prior_pack",
        "source_key": "1050_prior_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_PRIOR_WIDTH_SOURCE_PACK.csv",
        "needles": ["PWP1050_0_b_alpha", "PWP1050_5_qbar_source_label"],
        "role": "prior-width source pack template after product-functor failure.",
    },
    {
        "source_id": "SRC1806_13_clock_sensitivity",
        "source_key": "clock_sensitivity",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock alpha sensitivity rows.",
    },
    {
        "source_id": "SRC1806_14_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R9_Gdot"],
        "role": "local WEP/source, clock, PPN and Gdot anchors.",
    },
    {
        "source_id": "SRC1806_15_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate curve for smoke only.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_SOURCE_REGISTER.csv",
    "operator_classification_rule_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
    "symmetry_ban_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_SYMMETRY_BAN_THEOREM_ATTEMPT.csv",
    "operator_decision_table": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_OPERATOR_DECISION_TABLE.csv",
    "residual_prior_slots": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_RESIDUAL_PRIOR_SLOTS.csv",
    "alpha_mass_clock_prior_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_ALPHA_MASS_CLOCK_PRIOR_MATRIX.csv",
    "prior_promotion_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_PRIOR_PROMOTION_GATES.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1806_RESIDUAL_PRIOR_TEMPLATE_NONCLAIM.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1806_VALIDATION.csv",
}

DOC_PATH = ROOT / "1806-Y5-R2FR-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"


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


def operator_classification_rule_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_0_declared_parent_domain",
            "candidate_rule": "Every local operator must be generated from the declared parent fields, quotient map and representation data before empirical fitting.",
            "mathematical_form": "Op_allowed subset Alg[q(Phi),Dq(Phi),F_parent,theta_rep,topological classes] with no arbitrary scalar coefficient functions of Xhat.",
            "would_forbid": "post-hoc f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), clock-readout_Xhat unless declared retained residuals",
            "derivation_status": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
            "failure_mode": "without this rule, any neutral scalar can multiply gauge/matter/readout operators",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_1_quotient_descent_selection",
            "candidate_rule": "Ordinary visible-sector coefficients must descend through q_loc or be discrete/topological representation labels.",
            "mathematical_form": "c_i(Phi)=cbar_i(q_loc(Phi)) or c_i in Rep_top; Dq[v_X]=0 => Lie_v c_i=0",
            "would_forbid": "smooth vertical coefficient functions in visible matter/EM/readout sectors",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "failure_mode": "does not prove the actual parent action classifies alpha/mass/clock constants this way",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_2_product_sequestration",
            "candidate_rule": "Hidden/local-relaxation fields are sequestered from visible kinetic, mass, binding and readout coefficients except through quotient geometry.",
            "mathematical_form": "S_parent=S_vis[q(Phi),Psi,theta_rep]+S_hidden[Xhat,...]+S_coupling_allowed[q] and excludes Xhat*O_vis",
            "would_forbid": "f_X F^2, m_A(Xhat), y_A(Xhat), B_A(Xhat), nu_i(Xhat), source-label coupling slots",
            "derivation_status": "POWERFUL_BUT_PARENT_AXIOM_IF_UNSIGNED",
            "failure_mode": "sequestration is exactly the missing thing; it cannot be smuggled in after failed local tests",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_3_symmetry_filter",
            "candidate_rule": "A shift/parity/internal symmetry for Xhat forbids visible-sector coefficient functions unless broken only inside hidden sector.",
            "mathematical_form": "Xhat -> Xhat+const or Xhat -> -Xhat; require visible coefficient maps invariant/constant",
            "would_forbid": "linear Xhat*O_vis under shift/parity; full f_X only under stronger shift/sequestration",
            "derivation_status": "INSUFFICIENT_BY_ITSELF",
            "failure_mode": "parity allows Xhat^2 F^2; broken shift allows radiative/readout re-entry; hidden profile terms may break the symmetry",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_4_naturalness_guard",
            "candidate_rule": "If a forbidden vertex is not symmetry-forbidden, retain it as a residual with prior/source provenance.",
            "mathematical_form": "not symmetry_banned(Op_i) => coefficient_i in residual vector R_const with prior/status/source gates",
            "would_forbid": "claiming zero from aesthetic minimality or absence in the current draft",
            "derivation_status": "VALID_AUDIT_POLICY",
            "failure_mode": "prevents the theory from passing local tests by omission",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "rule_id": "OCR1806_5_verdict",
            "candidate_rule": "operator-classification symmetry ban closes alpha/mass/clock vertices",
            "mathematical_form": "OCR1806_0+1+2 plus symmetry/radiative closure => b_alpha=b_mu=b_mA=b_nuc=b_clock_i=0",
            "would_forbid": "all 1805 hidden constant/coupling vertices",
            "derivation_status": "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED",
            "failure_mode": "current corpus has conditional contracts, not a derived parent symmetry/operator classification",
            "valid_for_claim": False,
        },
    ]


def symmetry_ban_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_0_diffeomorphism_covariance",
            "symmetry_or_principle": "diffeomorphism covariance",
            "operator_tested": "f_X(Xhat)F_Q^2; m_A(Xhat)psi_bar psi; y_A(Xhat)psi H psi; B_A(Xhat)",
            "result": "DOES_NOT_FORBID",
            "reason": "all are scalar densities/covariant local terms when Xhat is a scalar field or representative marker",
            "residual_if_fail": "b_alpha;b_mA;b_mu;b_nuc",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_1_gauge_invariance",
            "symmetry_or_principle": "visible U(1)/gauge invariance",
            "operator_tested": "f_X(Xhat)F_Q^2",
            "result": "DOES_NOT_FORBID",
            "reason": "gauge invariance allows scalar gauge kinetic functions unless a stronger parent connection-norm uniqueness rule excludes them",
            "residual_if_fail": "b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_2_shift_symmetry",
            "symmetry_or_principle": "exact vertical shift symmetry",
            "operator_tested": "all non-derivative Xhat coefficient functions",
            "result": "WOULD_FORBID_IF_EXACT_BUT_UNSIGNED",
            "reason": "an exact shift can ban f_X, m_X, y_X, B_X and clock_X terms, but current local profiles/potentials/projections are not proven shift-invariant",
            "residual_if_fail": "all constant residual coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_3_parity_evenness",
            "symmetry_or_principle": "Xhat -> -Xhat parity",
            "operator_tested": "linear Xhat*O_vis",
            "result": "INSUFFICIENT",
            "reason": "parity kills only odd terms; Xhat^2 F^2 and even mass/binding responses still survive unless Xhat=0 is separately proved",
            "residual_if_fail": "quadratic/even residual coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_4_product_functor",
            "symmetry_or_principle": "visible/hidden product functor or sequestering",
            "operator_tested": "Xhat*O_vis and f_X(Xhat)O_vis",
            "result": "WOULD_FORBID_IF_PARENT_SIGNED",
            "reason": "this is the strongest clean route: visible matter/EM only see q_loc, hidden sector only couples through permitted quotient geometry",
            "residual_if_fail": "all alpha/mass/clock bound matrix rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "SBT1806_5_radiative_readout_closure",
            "symmetry_or_principle": "renormalization and readout closure",
            "operator_tested": "loop-induced f_XF^2 and effective clock/readout Xhat dependence",
            "result": "UNSIGNED",
            "reason": "even a tree-level ban needs the same rule to survive effective/readout reductions",
            "residual_if_fail": "b_alpha;b_clock_i",
            "valid_for_claim": False,
        },
    ]


def operator_decision_table_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ODT1806_0_fX_F2",
            "operator": "f_X(Xhat)F_Q^2 or lambda_A F_Q^2",
            "classification_needed": "forbidden by product/sequester or exact shift symmetry",
            "current_classification": "retained_residual",
            "why": "covariant and gauge-invariant; not excluded by current parent action",
            "residual_slot": "RP1806_0_b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ODT1806_1_mass_X",
            "operator": "m_A(Xhat) psi_bar_A psi_A",
            "classification_needed": "forbidden by fixed matter spectrum or exact shift/sequester",
            "current_classification": "retained_residual",
            "why": "local covariant matter term; no derived spectrum owner",
            "residual_slot": "RP1806_2_b_mA",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ODT1806_2_yukawa_X",
            "operator": "y_A(Xhat) psi_A H psi_B",
            "classification_needed": "forbidden by representation-owned Yukawa/mass-ratio data",
            "current_classification": "retained_residual",
            "why": "dimensionless mass ratios are observable and unowned",
            "residual_slot": "RP1806_1_b_mu",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ODT1806_3_binding_X",
            "operator": "B_A(Xhat), Lambda_QCD(Xhat), nuclear/EM binding response",
            "classification_needed": "forbidden by composite matter response theorem or bounded sensitivity matrix",
            "current_classification": "retained_residual",
            "why": "composite bodies can carry WEP/R10 charge even when point-particle masses are quiet",
            "residual_slot": "RP1806_3_b_nuc",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "operator_id": "ODT1806_4_clock_X",
            "operator": "nu_i(Xhat), clock-frame/readout Xhat dependence",
            "classification_needed": "forbidden by quotient-owned readout functor and upstream constants",
            "current_classification": "retained_residual",
            "why": "clock rows can reopen through readout even if WEP is silent",
            "residual_slot": "RP1806_4_b_clock_i",
            "valid_for_claim": False,
        },
    ]


def residual_prior_slots_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_0_b_alpha",
            "symbol": "b_alpha",
            "residual_definition": "vertical derivative of dimensionless EM/gauge kinetic/readout alpha channel",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock alpha drift/sensitivity; WEP composition alpha charge; R10 source/test projection; parent Xhat normalization",
            "promotion_rule": "valid only if parent theorem-zero signs or numeric prior width and projection are source-backed",
            "observable_links": "clock;WEP;R10;EM_spectra",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_1_b_mu",
            "symbol": "b_mu",
            "residual_definition": "vertical derivative of dimensionless mass ratios such as m_e/m_p",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock K_mu sensitivities; mass-ratio variation constraints; parent spectrum normalization",
            "promotion_rule": "valid only if mass-ratio theorem-zero signs or K_mu/b_mu prior rows are source-backed",
            "observable_links": "clock;WEP;composition",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_2_b_mA",
            "symbol": "b_mA",
            "residual_definition": "vertical derivative of material/species mass response after removing unit common mode",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "composition sensitivity matrix; source/test material charges; MICROSCOPE/R10 projection; parent Xhat normalization",
            "promotion_rule": "valid only if composition matrix and local projection are sourced",
            "observable_links": "WEP;R10;Newton_GM;clock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_3_b_nuc",
            "symbol": "b_nuc",
            "residual_definition": "vertical derivative of nuclear/QCD/electromagnetic binding response",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "nuclear sensitivity coefficients; material response table; clock nuclear sensitivity rows",
            "promotion_rule": "valid only if binding-response theorem-zero signs or sensitivity/prior rows are source-backed",
            "observable_links": "WEP;R10;clock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_4_b_clock_i",
            "symbol": "b_clock_i",
            "residual_definition": "vertical derivative of direct clock/readout residual not already covered by alpha/mass/nuclear constants",
            "prior_shape": "log_abs_or_theorem_zero",
            "prior_width_status": "MISSING_PRIOR_WIDTH",
            "required_sources": "clock pair sensitivity matrix; redshift/LPI readout model; tau_clock projection",
            "promotion_rule": "valid only if readout theorem-zero signs or clock residual prior is source-backed",
            "observable_links": "clock_comparison;redshift_LPI",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "prior_id": "RP1806_5_qbar_constants_abs_prior",
            "symbol": "qbar_constants_abs_prior",
            "residual_definition": "absolute-envelope prior for all constant-sector source/readout leakage",
            "prior_shape": "sum_abs_components_no_cancellation",
            "prior_width_status": "MISSING_COMPONENT_PRIORS",
            "required_sources": "RP1806_0 through RP1806_4; arena projection matrices; no-cancellation envelope",
            "promotion_rule": "valid only if every component is theorem-zero or numeric/source-backed",
            "observable_links": "WEP;R10;clock;PPN;local_GR",
            "valid_for_claim": False,
        },
    ]


def alpha_mass_clock_prior_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "PM1806_0_clock_alpha_mu",
            "arena": "clock_frequency_ratios",
            "prior_vector": "[b_alpha,b_mu,b_nuc,b_clock_i]",
            "projection_formula": "d ln R_ab = DeltaK_alpha*b_alpha*dXhat + DeltaK_mu*b_mu*dXhat + DeltaK_nuc*b_nuc*dXhat + b_clock_ab*dXhat",
            "source_anchor": str(RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"),
            "missing_for_score": "K_mu/K_nuc rows; tau_clock; b priors/theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "PM1806_1_WEP_composition",
            "arena": "MICROSCOPE_WEP",
            "prior_vector": "[b_alpha,b_mA,b_mu,b_nuc]",
            "projection_formula": "eta_AB = DeltaQ_AB dot beta_source_test[b_alpha,b_mA,b_mu,b_nuc] * tau_WEP",
            "source_anchor": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R1_WEP_source_charge",
            "missing_for_score": "composition charge matrix; source/test beta vectors; tau_WEP; b priors/theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "PM1806_2_R10_short_range",
            "arena": "R10_short_range_fifth_force",
            "prior_vector": "[b_alpha,b_mA,b_mu,b_nuc,qbar_marker,qbar_source]",
            "projection_formula": "alpha_X(lambda_X)=K_X Q_source(lambda_X) Q_test(lambda_X)/(4*pi*Z_X*G_obs)",
            "source_anchor": str(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"),
            "missing_for_score": "lambda_X;Z_X;K_X;Q_source/test;promoted bound curve; b priors/theorem-zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "PM1806_3_PPN_source",
            "arena": "local_GR_PPN_source",
            "prior_vector": "[metric_residual,source_Hamiltonian_residual,qbar_constants_abs_prior]",
            "projection_formula": "PPN/local source vector = P_metric[source charge, constant leakage, readout residual]",
            "source_anchor": str(LOCAL_BOUNDS / "local_bound_claims.csv") + ":R3_gamma_through_R9_Gdot",
            "missing_for_score": "weak-field solution; source Hamiltonian owner; constant-sector residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def prior_promotion_gates_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PG1806_0_theorem_zero_gate",
            "promotion_condition": "A coefficient can be set to zero only if the parent action symmetry/operator classification forbids the corresponding vertex including radiative/readout re-entry.",
            "current_status": "not_satisfied",
            "why": "no signed product/sequester or exact shift symmetry currently covers all visible sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PG1806_1_numeric_prior_gate",
            "promotion_condition": "A retained coefficient prior can be used only with source path, units, normalization and arena projection.",
            "current_status": "not_satisfied",
            "why": "prior slots are named but have MISSING_PRIOR_WIDTH and missing local projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PG1806_2_no_cancellation_gate",
            "promotion_condition": "Multi-coefficient residuals must be tested as absolute envelopes unless a theorem enforces cancellation.",
            "current_status": "active_guard",
            "why": "prevents tuned cancellations between alpha, mass, clock, marker and source leakage",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PG1806_3_shared_domain_gate",
            "promotion_condition": "The same local domain/projection rule must be used for WEP, R10, clocks and PPN.",
            "current_status": "not_satisfied",
            "why": "domain/screen rule remains a parent-level open clause",
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "residual_prior_alpha_mass_clock_template_1806",
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_PRIOR_VECTOR_AND_QSOURCE_QTEST_PROJECTION",
            "force_law_form": "R10 alpha(lambda) from residual-prior vector [b_alpha,b_mA,b_mu,b_nuc,qbar_marker,qbar_source] through source/test charge projection",
            "derivation_status": "template_invalid_operator_ban_failed_and_prior_widths_missing",
            "valid_for_claim": False,
        }
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1806_0_operator_ban",
            "gate": "parent symmetry/operator classification forbids alpha/mass/clock hidden vertices",
            "current_status": "BLOCKED",
            "reason": "ordinary covariance/gauge invariance do not forbid vertices; product/sequester rule is unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1806_1_prior_scoring",
            "gate": "residual priors can score WEP/R10/clock/PPN",
            "current_status": "BLOCKED",
            "reason": "prior widths, source/test charge projections and local domain maps are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1806_2_verdict",
            "gate": "operator classification closes constant/coupling sector",
            "current_status": "OPERATOR_BAN_NOT_SIGNED_PRIORS_NOT_SCORE_READY",
            "reason": "product functor is the clean theorem route but remains a target rather than a proof",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1806_0_operator_ban",
            "claim": "parent symmetry/operator classification forbids alpha/mass/clock hidden vertices",
            "status": "BLOCKED",
            "reason": "diffeomorphism/gauge invariance do not forbid the vertices; stronger sequester/shift rule is unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1806_1_zero_coefficients",
            "claim": "b_alpha,b_mu,b_mA,b_nuc,b_clock_i can be set to zero",
            "status": "BLOCKED",
            "reason": "theorem-zero promotion gate is not satisfied",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1806_2_prior_scoring",
            "claim": "residual priors can score WEP/R10/clock/PPN",
            "status": "BLOCKED",
            "reason": "prior widths, source/test charge projections and local domain maps are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1806_3_local_GR_Newton",
            "claim": "local-GR/Newton branch closes from 1806",
            "status": "BLOCKED",
            "reason": "operator-classification/prior stage does not replace source Hamiltonian and PPN weak-field derivations",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1806_0_symmetry_result",
            "decision": "ORDINARY_COVARIANCE_AND_GAUGE_SYMMETRY_ARE_INSUFFICIENT",
            "reason": "the unwanted vertices are legal scalar/gauge-invariant operators",
            "next_action": "do not claim zero from minimality; require signed sequester/shift rule or priors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1806_1_best_theorem_route",
            "decision": "PRODUCT_SEQUESTER_PARENT_FUNCTOR_IS_THE_CLEAN_THEOREM_ROUTE",
            "reason": "it would make visible matter/EM depend only on q_loc and representation data",
            "next_action": "attempt to derive product functor from parent quotient/readout architecture",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1806_2_fallback_route",
            "decision": "RESIDUAL_PRIOR_SLOTS_ARE_EXPLICIT_BUT_NOT_SCORE_READY",
            "reason": "coefficient names, arenas and promotion rules exist but prior widths/projections are missing",
            "next_action": "source prior widths or derive zero before running empirical score",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1806_3_best_next",
            "decision": "VISIBLE_HIDDEN_PRODUCT_FUNCTOR_DERIVATION_OR_PRIOR_WIDTH_SOURCE_PACK_NEXT",
            "reason": "deriving sequester would collapse the constant-sector debt more cleanly than fitting many priors",
            "next_action": "build 1807 to test the product functor; if it fails, source the first prior-width pack",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1806_0_primary",
            "next_target": "1807-Y5-R2FR-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
            "script": "scripts/Y5_R2FR_visible_hidden_product_functor_derivation_or_prior_width_source_pack.py",
            "objective": "try to derive the visible/hidden product functor that makes visible matter and EM depend only on q_loc and representation data; if it fails, source prior-width packs for b_alpha, b_mu, b_mA, b_nuc, b_clock_i and qbar_source_label",
            "selection_status": "selected",
            "success_condition": "signed product/sequester theorem or nonclaim prior-width source pack with explicit projection blockers",
            "valid_for_claim": False,
        }
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "operator_classification_rule_attempt": operator_classification_rule_attempt_rows(),
        "symmetry_ban_theorem_attempt": symmetry_ban_theorem_attempt_rows(),
        "operator_decision_table": operator_decision_table_rows(),
        "residual_prior_slots": residual_prior_slots_rows(),
        "alpha_mass_clock_prior_matrix": alpha_mass_clock_prior_matrix_rows(),
        "prior_promotion_gates": prior_promotion_gates_rows(),
        "mts_r10_template": mts_r10_template_rows(),
        "acceptance_gate": acceptance_gate_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1806_{key.upper()}.csv")


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
        "score_ready",
        "numeric_score_ready",
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
        "score_ready",
        "numeric_score_ready",
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
        if not (RAB_QUEUE / f"JR1806_{key.upper()}.csv").exists():
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
        ("VAL1806_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1806_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1806_2_operator_rule_attempt_blocked",
            any(
                row["rule_id"] == "OCR1806_5_verdict"
                and row["derivation_status"] == "FAIL_CURRENT_CLAIM_RESIDUAL_PRIORS_REQUIRED"
                for row in rows_map["operator_classification_rule_attempt"]
            ),
            "operator-classification rule has exact conditional piece but current claim remains blocked",
        ),
        (
            "VAL1806_3_symmetry_tests_blocked",
            any(row["test_id"] == "SBT1806_0_diffeomorphism_covariance" and row["result"] == "DOES_NOT_FORBID" for row in rows_map["symmetry_ban_theorem_attempt"])
            and any(row["test_id"] == "SBT1806_4_product_functor" and row["result"] == "WOULD_FORBID_IF_PARENT_SIGNED" for row in rows_map["symmetry_ban_theorem_attempt"]),
            "ordinary symmetries do not forbid vertices; product functor would if signed",
        ),
        (
            "VAL1806_4_decision_table_complete",
            len(rows_map["operator_decision_table"]) >= 5
            and all(row["current_classification"] == "retained_residual" for row in rows_map["operator_decision_table"]),
            "all alpha/mass/clock forbidden vertices have retained residual decisions",
        ),
        (
            "VAL1806_5_prior_slots_nonclaim",
            len(rows_map["residual_prior_slots"]) >= 6
            and all(not boolish(row["valid_for_claim"]) and "MISSING" in row["prior_width_status"] for row in rows_map["residual_prior_slots"]),
            "residual-prior slots are present and not claim-valid",
        ),
        (
            "VAL1806_6_prior_matrix_nonclaim",
            len(rows_map["alpha_mass_clock_prior_matrix"]) >= 4
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_mass_clock_prior_matrix"]),
            "clock/WEP/R10/PPN prior matrix is staged as nonclaim",
        ),
        (
            "VAL1806_7_promotion_gates_blocked",
            all(row["current_status"] in {"not_satisfied", "active_guard"} and not boolish(row["valid_for_claim"]) for row in rows_map["prior_promotion_gates"]),
            "theorem-zero and numeric-prior promotion gates remain blocked",
        ),
        (
            "VAL1806_8_mts_template_schema_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1806_9_acceptance_blocks",
            any(
                row["gate_id"] == "AC1806_2_verdict"
                and row["current_status"] == "OPERATOR_BAN_NOT_SIGNED_PRIORS_NOT_SCORE_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks 1806 closure",
        ),
        (
            "VAL1806_10_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all operator-ban/prior/local-GR claim gates remain blocked",
        ),
        ("VAL1806_11_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1806_12_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1806_13_decision_next",
            any(
                row["decision_id"] == "DEC1806_3_best_next"
                and row["decision"] == "VISIBLE_HIDDEN_PRODUCT_FUNCTOR_DERIVATION_OR_PRIOR_WIDTH_SOURCE_PACK_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects visible/hidden product functor next",
        ),
        (
            "VAL1806_14_next_selected",
            any(row["route_id"] == "NEXT1806_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1806_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1806 CSVs parse"),
        ("VAL1806_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1806_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1806_18_formalization_untouched", formalization_untouched(), "no 1806 outputs found under formalization-workbench"),
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
            "check_id": "VAL1806_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1806 parent operator classification symmetry ban or residual coefficient prior checkpoint",
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
            "# 1806 - Y5/R2FR Parent Operator Classification, Symmetry Ban, or Residual Coefficient Prior",
            "",
            "## Verdict",
            "",
            "1806 tests the obvious escape route for the coupling problem: maybe ordinary covariance, gauge invariance, or simple symmetry already forbids the dangerous terms. It does not. The vertices `f_X F^2`, `m_A(Xhat)`, `y_A(Xhat)`, binding-response terms, and clock-readout slots are legal unless a stronger parent operator rule is signed.",
            "",
            "The exact conditional rule is now clean: visible coefficients must either descend through `q_loc` or be discrete/topological representation data. A visible/hidden product functor would do the job by making visible EM, matter, clocks, and source coupling depend only on `q_loc` plus representation labels.",
            "",
            "That product/sequester rule is not derived here. Therefore `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `b_clock_i`, and `qbar_constants_abs_prior` stay as retained nonclaim residual-prior slots.",
            "",
            "**Claim ceiling:** no operator-ban theorem, no zero coefficient claim, no residual-prior score, no local-GR/Newton claim, no R10/WEP/clock claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1806.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Operator Classification Rule Attempt",
            markdown_table(rows_map["operator_classification_rule_attempt"], ["rule_id", "candidate_rule", "mathematical_form", "would_forbid", "derivation_status", "failure_mode", "valid_for_claim"]),
            "",
            "## Symmetry Ban Theorem Attempt",
            markdown_table(rows_map["symmetry_ban_theorem_attempt"], ["test_id", "symmetry_or_principle", "operator_tested", "result", "reason", "residual_if_fail", "valid_for_claim"]),
            "",
            "## Operator Decision Table",
            markdown_table(rows_map["operator_decision_table"], ["operator_id", "operator", "classification_needed", "current_classification", "why", "residual_slot", "valid_for_claim"]),
            "",
            "## Residual Prior Slots",
            markdown_table(rows_map["residual_prior_slots"], ["prior_id", "symbol", "residual_definition", "prior_shape", "prior_width_status", "promotion_rule", "valid_for_claim"]),
            "",
            "## Alpha/Mass/Clock Prior Matrix",
            markdown_table(rows_map["alpha_mass_clock_prior_matrix"], ["matrix_id", "arena", "prior_vector", "projection_formula", "missing_for_score", "claim_allowed", "valid_for_claim"]),
            "",
            "## Prior Promotion Gates",
            markdown_table(rows_map["prior_promotion_gates"], ["gate_id", "promotion_condition", "current_status", "why", "valid_for_claim"]),
            "",
            "## MTS R10 Smoke Template",
            markdown_table(rows_map["mts_r10_template"], ["model_id", "branch_id", "lambda_value", "alpha_predicted", "derivation_status", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "valid_for_claim"]),
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
            "This is a hard but useful result. We cannot win local GR by saying the couplings are 'not natural'; they are allowed unless the parent observable algebra blocks hidden-to-visible coefficient morphisms. The best next derivation is therefore the product functor itself. If that fails, we stop chasing zero and start sourcing prior widths.",
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
    print(f"1806 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
