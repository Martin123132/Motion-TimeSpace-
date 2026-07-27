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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1807"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1807_0_1806_doc",
        "source_key": "1806_doc",
        "source_path": ROOT / "1806-Y5-R2FR-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
        "needles": ["NEXT1806_0_primary", "DEC1806_3_best_next"],
        "role": "1806 handoff selecting visible/hidden product functor next.",
    },
    {
        "source_id": "SRC1807_1_1806_validation",
        "source_key": "1806_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1806_VALIDATION.csv",
        "needles": ["VAL1806_OVERALL", "PASS"],
        "role": "confirms 1806 passed before 1807 starts.",
    },
    {
        "source_id": "SRC1807_2_1806_operator_rule",
        "source_key": "1806_operator_rule",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
        "needles": ["OCR1806_2_product_sequestration", "OCR1806_5_verdict"],
        "role": "current branch operator-classification result.",
    },
    {
        "source_id": "SRC1807_3_1806_prior_slots",
        "source_key": "1806_prior_slots",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1806_RESIDUAL_PRIOR_SLOTS.csv",
        "needles": ["RP1806_0_b_alpha", "RP1806_5_qbar_constants_abs_prior"],
        "role": "current branch residual-prior slots.",
    },
    {
        "source_id": "SRC1807_4_1050_doc",
        "source_key": "1050_doc",
        "source_path": ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
        "needles": ["PFT1050_5_verdict", "DEC1050_3_best_next"],
        "role": "older product functor/prior-width checkpoint.",
    },
    {
        "source_id": "SRC1807_5_1050_product",
        "source_key": "1050_product",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["PFT1050_1_visible_action_pullback", "PFT1050_5_verdict"],
        "role": "product functor theorem attempt.",
    },
    {
        "source_id": "SRC1807_6_1050_visible_algebra",
        "source_key": "1050_visible_algebra",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_VISIBLE_ALGEBRA_AUDIT.csv",
        "needles": ["VA1050_1_EM", "VA1050_4_source"],
        "role": "visible algebra argument audit.",
    },
    {
        "source_id": "SRC1807_7_1050_obstructions",
        "source_key": "1050_obstructions",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv",
        "needles": ["OBS1050_0_scalar_invariant", "OBS1050_4_radiative_readout"],
        "role": "product functor obstruction ledger.",
    },
    {
        "source_id": "SRC1807_8_1050_prior_pack",
        "source_key": "1050_prior_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1050_PRIOR_WIDTH_SOURCE_PACK.csv",
        "needles": ["PWP1050_0_b_alpha", "PWP1050_5_qbar_source_label"],
        "role": "older prior-width source pack.",
    },
    {
        "source_id": "SRC1807_9_980_marker_functor",
        "source_key": "980_marker_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NMF980_2_scalar_obstruction_lemma", "NMF980_5_continuous_constant_sector"],
        "role": "scalar obstruction to no-marker/product functor route.",
    },
    {
        "source_id": "SRC1807_10_642_maxwell",
        "source_key": "642_maxwell",
        "source_path": RESIDUALS / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "needles": ["MD642_1_Gauss_Ampere", "MD642_4_alpha_constant"],
        "role": "Maxwell descent and alpha owner blocker.",
    },
    {
        "source_id": "SRC1807_11_1045_matter_functor",
        "source_key": "1045_matter_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1045_2_matter_bundle_functor", "MFS1045_6_verdict"],
        "role": "parent matter functor signature audit.",
    },
    {
        "source_id": "SRC1807_12_953_source_functor",
        "source_key": "953_source_functor",
        "source_path": RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NSF953_1_domain_fork", "NSF953_5_verdict"],
        "role": "source label-forgetting theorem attempt.",
    },
    {
        "source_id": "SRC1807_13_1051_no_mixed",
        "source_key": "1051_no_mixed",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
        "needles": ["NMM1051_2_scalar_counterexample", "NMM1051_5_verdict"],
        "role": "older next-step no-mixed morphism attempt.",
    },
    {
        "source_id": "SRC1807_14_clock_sensitivity",
        "source_key": "clock_sensitivity",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock alpha sensitivity rows.",
    },
    {
        "source_id": "SRC1807_15_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R2_clock_redshift"],
        "role": "local WEP/source and clock bound anchors.",
    },
    {
        "source_id": "SRC1807_16_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate curve for smoke only.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_SOURCE_REGISTER.csv",
    "product_functor_theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
    "visible_algebra_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_VISIBLE_ALGEBRA_AUDIT.csv",
    "product_functor_obstruction_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv",
    "prior_width_source_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_PRIOR_WIDTH_SOURCE_PACK.csv",
    "projection_readiness": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_PROJECTION_READINESS.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1807_PRODUCT_FUNCTOR_PRIOR_PACK_TEMPLATE_NONCLAIM.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1807_VALIDATION.csv",
}

DOC_PATH = ROOT / "1807-Y5-R2FR-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"


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


def product_functor_theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_0_define_product_domain",
            "claim_piece": "visible/hidden product domain",
            "mathematical_form": "C_parent -> C_vis x C_hid with C_vis pulled back from q_loc(Phi) and representation labels theta_rep; hidden fields Xhat live only in C_hid",
            "derivation_step": "This is the categorical form of sequestering: visible EM/matter/readout/source functors are not allowed to take Xhat as an argument.",
            "current_status": "DEFINITION_SHARP_NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_PARENT_CONSTRUCTION_OF_PRODUCT_CATEGORY_AND_PROJECTION_FUNCTORS",
            "if_missing": "Xhat can still feed visible coefficients through legal scalar functions",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_1_visible_action_pullback",
            "claim_piece": "visible action is quotient pullback",
            "mathematical_form": "S_vis=S_EM[A_Q,q_loc(Phi),T_Q,theta_rep]+S_matter[Psi,e_obs(q),omega(q),theta_rep]+S_readout[q,theta_rep]",
            "derivation_step": "If S_vis factors only through q_loc and representation data, vertical variations in ker(Dq_loc) cannot alter visible coefficients.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_claim": "MISSING_SIGNED_PARENT_MATTER_FUNCTOR;MISSING_MAXWELL_ALPHA_OWNER;MISSING_SOURCE_LABEL_FORGETTING",
            "if_missing": "b_alpha, b_mA, b_mu, b_nuc, b_clock_i and qbar_source_label remain retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_2_forbidden_mixed_hom",
            "claim_piece": "no visible-hidden mixed coefficient morphisms",
            "mathematical_form": "Hom(C_hid,Coeff(O_vis))=Const or absent; Forbidden: Xhat -> f_X, m_A, y_A, B_A, nu_i, kappa_A",
            "derivation_step": "This is the exact condition that kills f_X F^2, mass/binding, clock, and source-label Xhat vertices.",
            "current_status": "POWERFUL_BUT_UNSIGNED",
            "missing_for_claim": "MISSING_PROOF_PARENT_OBSERVABLE_ALGEBRA_HAS_NO_NONCONSTANT_HIDDEN_TO_VISIBLE_COEFFICIENT_MORPHISMS",
            "if_missing": "scalar-obstruction lemma reopens product functor with any surviving invariant scalar",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_3_radiative_readout_closure",
            "claim_piece": "sequestering survives EFT and clock/readout reduction",
            "mathematical_form": "Renormalized/effective S_vis^eff and readout maps still factor through q_loc and theta_rep",
            "derivation_step": "Tree-level product form is not enough if loops or readout maps regenerate Xhat-dependent coefficients.",
            "current_status": "UNSIGNED",
            "missing_for_claim": "MISSING_RADIATIVE_CLOSURE_OR_EFFECTIVE_ACTION_READOUT_FUNCTOR_THEOREM",
            "if_missing": "b_alpha and b_clock_i remain live even if bare action is clean",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_4_source_forgetfulness",
            "claim_piece": "source functor forgets species labels before coupling selection",
            "mathematical_form": "F_src: Obj(C_matter)->T_total rather than Obj(C_matter)->(T_A,A); then only kappa_univ is available",
            "derivation_step": "Product functor must also prevent source/test labels from becoming relative coupling slots.",
            "current_status": "CONDITIONAL_PROOF_NOT_PARENT_DERIVED",
            "missing_for_claim": "MISSING_PARENT_SIGNED_LABEL_FORGETTING_QUOTIENT",
            "if_missing": "relative source weights and WEP/R10 source charge remain retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PFT1807_5_verdict",
            "claim_piece": "visible-hidden product functor closes constant/coupling sector",
            "mathematical_form": "PFT1807_0 through PFT1807_4 signed => b_alpha=b_mu=b_mA=b_nuc=b_clock_i=qbar_source_label=0",
            "derivation_step": "The theorem target is exact, but the current corpus has not derived the product functor, no-mixed morphism, or radiative/readout closure.",
            "current_status": "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED",
            "missing_for_claim": "MISSING_PARENT_PRODUCT_FUNCTOR_CONSTRUCTION_OR_SOURCE_BACKED_RESIDUAL_PRIOR_WIDTHS",
            "if_missing": "build prior-width source pack and keep all local claims blocked",
            "valid_for_claim": False,
        },
    ]


def visible_algebra_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "algebra_id": "VA1807_0_geometry",
            "visible_object": "observed coframe/metric/connection",
            "allowed_arguments": "q_loc(Phi)",
            "forbidden_arguments": "Xhat representative; hidden profile labels; material marker",
            "current_evidence": "parent coframe functor is sufficient as a signature but parent-signed status is open",
            "status": "CONDITIONAL",
            "residual_if_open": "qbar_geom;shadow_frame_terms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "algebra_id": "VA1807_1_EM",
            "visible_object": "EM connection and gauge kinetic normalization",
            "allowed_arguments": "A_Q,T_Q,q_loc(Phi),fixed inner product/charge lattice",
            "forbidden_arguments": "f_X(Xhat), lambda_A branch coefficient, post-readout alpha_X",
            "current_evidence": "Maxwell descent supports closure form, but alpha constant owner remains blocked",
            "status": "BLOCKED",
            "residual_if_open": "b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "algebra_id": "VA1807_2_matter",
            "visible_object": "matter masses/Yukawas/binding data",
            "allowed_arguments": "theta_rep or theta_bar(q_loc(Phi))",
            "forbidden_arguments": "m_A(Xhat), y_A(Xhat), B_A(Xhat), Lambda_QCD(Xhat)",
            "current_evidence": "parent matter category and constants split are unsigned",
            "status": "BLOCKED",
            "residual_if_open": "b_mu;b_mA;b_nuc",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "algebra_id": "VA1807_3_clocks",
            "visible_object": "clock transition/readout map",
            "allowed_arguments": "q_loc(Phi), theta_rep, quotient-owned alpha/mass/nuclear constants",
            "forbidden_arguments": "nu_i(Xhat), clock-frame Xhat, hidden readout marker",
            "current_evidence": "clock sensitivity rows exist, but MTS tau_clock/readout closure is missing",
            "status": "BLOCKED",
            "residual_if_open": "b_clock_i",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "algebra_id": "VA1807_4_source",
            "visible_object": "source/test mass and coupling functor",
            "allowed_arguments": "T_total in one observed coframe; one common kappa/G_ref",
            "forbidden_arguments": "species labels A in coupling choice; kappa_A(Xhat); source preparation marker",
            "current_evidence": "source functor theorem is conditional but parent label-forgetting is not signed",
            "status": "BLOCKED",
            "residual_if_open": "qbar_source_label;beta_source",
            "valid_for_claim": False,
        },
    ]


def product_functor_obstruction_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1807_0_scalar_invariant",
            "obstruction": "any surviving nonconstant local invariant scalar can feed a visible coefficient",
            "example": "theta(I)=theta0+epsilon I or f_X(I)F^2",
            "source_evidence": str(RESIDUALS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv") + ":NMF980_2",
            "effect": "product functor fails unless hidden-to-visible coefficient morphisms are forbidden",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1807_1_alpha_owner",
            "obstruction": "Maxwell descent does not fix g_EM or alpha_EM owner",
            "example": "g_EM or alpha_EM remains an independent visible coefficient",
            "source_evidence": str(RESIDUALS / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv") + ":MD642_4_alpha_constant",
            "effect": "b_alpha remains live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1807_2_matter_category",
            "obstruction": "parent matter category and constants split are not parent-constructed",
            "example": "m_A(Xhat), y_A(Xhat), B_A(Xhat)",
            "source_evidence": str(RESIDUALS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv") + ":MFS1045_6_verdict",
            "effect": "b_mu,b_mA,b_nuc remain live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1807_3_source_labels",
            "obstruction": "source functor does not yet prove label-forgetting",
            "example": "F((T_A,A))=kappa_A T_A remains additive and covariant",
            "source_evidence": str(RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv") + ":NSF953_5_verdict",
            "effect": "WEP/R10 source charge remains retained",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1807_4_radiative_readout",
            "obstruction": "bare action product form does not automatically survive EFT/readout reductions",
            "example": "loop-induced f_X F^2 or clock readout residual",
            "source_evidence": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1806_SYMMETRY_BAN_THEOREM_ATTEMPT.csv") + ":SBT1806_5_radiative_readout_closure",
            "effect": "b_alpha,b_clock_i remain live unless closure is signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def prior_width_source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_0_b_alpha",
            "symbol": "b_alpha",
            "source_pack_target": "dimensionless EM/gauge kinetic/readout coefficient prior width",
            "candidate_sources_in_hand": "clock alpha sensitivity rows; local_bound_claims:R1_WEP_source_charge; R10 review candidate",
            "still_missing": "actual b_alpha prior width or theorem-zero; tau_clock/tau_WEP/tau_R10; composition alpha charge; promoted R10 bound curve",
            "units": "Xhat^-1 or arena-projected dimensionless product",
            "promotion_status": "MISSING_PRIOR_WIDTH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_1_b_mu",
            "symbol": "b_mu",
            "source_pack_target": "mass-ratio coefficient prior width",
            "candidate_sources_in_hand": "residual slot only; NIST m_e/u extraction is constant provenance not MTS width",
            "still_missing": "clock K_mu sensitivities; mass-ratio drift constraints; parent Xhat normalization",
            "units": "Xhat^-1 or clock-projected product",
            "promotion_status": "MISSING_SOURCE_ROWS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_2_b_mA",
            "symbol": "b_mA",
            "source_pack_target": "material/species mass-response prior width",
            "candidate_sources_in_hand": "local_bound_claims:R1_WEP_source_charge; R10 review candidate",
            "still_missing": "composition sensitivity matrix; source/test material charge vectors; tau_WEP/tau_R10",
            "units": "Xhat^-1 or composition-projected dimensionless product",
            "promotion_status": "MISSING_COMPOSITION_MATRIX",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_3_b_nuc",
            "symbol": "b_nuc",
            "source_pack_target": "nuclear/QCD/binding-response prior width",
            "candidate_sources_in_hand": "WEP/R10 anchors only",
            "still_missing": "nuclear sensitivity coefficients; material binding fractions; clock nuclear sensitivity rows",
            "units": "Xhat^-1 or sensitivity-projected product",
            "promotion_status": "MISSING_NUCLEAR_SENSITIVITY_SOURCES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_4_b_clock_i",
            "symbol": "b_clock_i",
            "source_pack_target": "direct clock/readout residual prior width",
            "candidate_sources_in_hand": "clock alpha sensitivity rows; local_bound_claims:R2_clock_redshift",
            "still_missing": "direct readout residual model; tau_clock; separation from alpha/mass/nuclear sensitivity terms",
            "units": "Xhat^-1 or clock-projected product",
            "promotion_status": "MISSING_CLOCK_READOUT_MODEL",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PWP1807_5_qbar_source_label",
            "symbol": "qbar_source_label",
            "source_pack_target": "source/species label leakage prior width",
            "candidate_sources_in_hand": "source functor theorem attempt; local_bound_claims:R1_WEP_source_charge",
            "still_missing": "label-forgetting theorem-zero or relative source-weight prior; source/test projection",
            "units": "dimensionless source charge product",
            "promotion_status": "MISSING_SOURCE_LABEL_PRIOR",
            "valid_for_claim": False,
        },
    ]


def projection_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "readiness_id": "PR1807_0_clock",
            "arena": "clock",
            "ready_inputs": "DeltaK_alpha for Al/Hg and Yb E3/E2",
            "missing_inputs": "tau_clock; Xhat normalization; K_mu/K_nuc; direct readout residual separation",
            "status": "PARTIAL_SOURCE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "readiness_id": "PR1807_1_WEP",
            "arena": "WEP/MICROSCOPE",
            "ready_inputs": "R1_WEP_source_charge bound anchor",
            "missing_inputs": "composition charge matrix; source/test beta vectors; shared local projection",
            "status": "ANCHOR_READY_PROJECTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "readiness_id": "PR1807_2_R10",
            "arena": "short-range fifth force",
            "ready_inputs": "review-candidate R10 curve only",
            "missing_inputs": "promoted bound curve; lambda_X; Z_X; K_X; source/test Qbar projection",
            "status": "BOUND_REVIEW_CANDIDATE_AND_MTS_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "readiness_id": "PR1807_3_PPN_local_GR",
            "arena": "PPN/local_GR",
            "ready_inputs": "local bounds anchors exist",
            "missing_inputs": "weak-field solution; source Hamiltonian owner; residual vector projection",
            "status": "LOCAL_GR_NOT_SCORE_READY",
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "product_functor_or_prior_width_template_1807",
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_PRODUCT_FUNCTOR_ZERO_OR_PRIOR_WIDTH_PROJECTION",
            "force_law_form": "R10 alpha(lambda) is zero only if product functor signs; otherwise residual-prior vector projects through source/test charges",
            "derivation_status": "template_invalid_product_functor_unsigned_and_prior_widths_missing",
            "valid_for_claim": False,
        }
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1807_0_product_functor",
            "gate": "visible-hidden product functor signed",
            "current_status": "BLOCKED",
            "reason": "product category, no-mixed morphism, source label-forgetting and radiative/readout closure are not parent-derived",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1807_1_prior_width_pack",
            "gate": "fallback prior-width pack score-ready",
            "current_status": "BLOCKED",
            "reason": "candidate sources exist, but widths and arena projections are still missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1807_2_verdict",
            "gate": "product functor closes coupling sector",
            "current_status": "PRODUCT_FUNCTOR_NOT_SIGNED_PRIOR_WIDTH_PACK_NOT_SCORE_READY",
            "reason": "the theorem shape is exact but current corpus still permits hidden-to-visible coefficient morphisms",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1807_0_product_functor_zero",
            "claim": "visible-hidden product functor kills all constant/coupling residuals",
            "status": "BLOCKED",
            "reason": "product construction and no-mixed morphism lemma are not parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1807_1_prior_width_score",
            "claim": "prior-width pack can score clocks/WEP/R10/PPN",
            "status": "BLOCKED",
            "reason": "prior widths, shared local projections and source/test charges are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1807_2_local_GR_Newton",
            "claim": "local-GR/Newton branch closes from 1807",
            "status": "BLOCKED",
            "reason": "constant/coupling sector remains open and source Hamiltonian/PPN gates are separate",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1807_0_theorem_shape",
            "decision": "PRODUCT_FUNCTOR_THEOREM_SHAPE_IS_EXACT",
            "reason": "if visible action is a pullback through q_loc and representation data, vertical hidden variations cannot create visible constants",
            "next_action": "do not claim until parent category/no-mixed-morphism and readout closure are signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1807_1_current_failure",
            "decision": "CURRENT_CORPUS_DOES_NOT_PROVE_PRODUCT_FUNCTOR",
            "reason": "nonconstant invariant scalar, alpha owner, matter functor, source labels and radiative/readout closure remain open",
            "next_action": "use prior-width source pack or derive no-mixed-morphism lemma",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1807_2_prior_pack",
            "decision": "PRIOR_WIDTH_PACK_USEFUL_BUT_NOT_SCORE_READY",
            "reason": "candidate anchors exist for clock/WEP/R10, but coefficient widths and projections are missing",
            "next_action": "source one coefficient-width chain or derive no-mixed morphism",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1807_3_best_next",
            "decision": "NO_MIXED_HIDDEN_VISIBLE_MORPHISM_LEMMA_OR_FIRST_PRIOR_WIDTH_CHAIN_NEXT",
            "reason": "this is the last clean derivation route for killing constant-sector residuals without fitting many coefficients",
            "next_action": "build 1808 to try no-mixed morphism; if it fails, build first b_alpha clock-product prior chain",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1807_0_primary",
            "next_target": "1808-Y5-R2FR-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
            "script": "scripts/Y5_R2FR_no_mixed_hidden_visible_morphism_lemma_or_first_prior_width_chain.py",
            "objective": "try to prove that no nonconstant hidden-to-visible coefficient morphism exists in the parent observable algebra; if it fails, build the first source-backed prior-width chain, starting with b_alpha because clock alpha sensitivities already exist",
            "selection_status": "selected",
            "success_condition": "no-mixed morphism theorem or nonclaim b_alpha clock-product prior chain with standalone-transfer blockers",
            "valid_for_claim": False,
        }
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "product_functor_theorem_attempt": product_functor_theorem_attempt_rows(),
        "visible_algebra_audit": visible_algebra_audit_rows(),
        "product_functor_obstruction_ledger": product_functor_obstruction_ledger_rows(),
        "prior_width_source_pack": prior_width_source_pack_rows(),
        "projection_readiness": projection_readiness_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1807_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1807_{key.upper()}.csv").exists():
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
        ("VAL1807_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1807_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1807_2_product_functor_blocked",
            any(
                row["theorem_id"] == "PFT1807_5_verdict"
                and row["current_status"] == "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED"
                for row in rows_map["product_functor_theorem_attempt"]
            ),
            "product functor theorem shape is exact but not promoted",
        ),
        (
            "VAL1807_3_visible_algebra_blocked",
            all(row["status"] in {"CONDITIONAL", "BLOCKED"} and not boolish(row["valid_for_claim"]) for row in rows_map["visible_algebra_audit"])
            and any(row["algebra_id"] == "VA1807_1_EM" and row["residual_if_open"] == "b_alpha" for row in rows_map["visible_algebra_audit"]),
            "visible algebra audit keeps EM/matter/clock/source residuals live",
        ),
        (
            "VAL1807_4_obstructions_retained",
            len(rows_map["product_functor_obstruction_ledger"]) >= 5
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["product_functor_obstruction_ledger"]),
            "product functor obstruction ledger is retained as nonclaim",
        ),
        (
            "VAL1807_5_prior_pack_nonclaim_missing",
            len(rows_map["prior_width_source_pack"]) >= 6
            and all("MISSING" in row["promotion_status"] and not boolish(row["valid_for_claim"]) for row in rows_map["prior_width_source_pack"]),
            "prior-width source pack is nonclaim and input-missing",
        ),
        (
            "VAL1807_6_projection_readiness_nonclaim",
            len(rows_map["projection_readiness"]) >= 4
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["projection_readiness"]),
            "projection readiness rows remain nonclaim",
        ),
        (
            "VAL1807_7_mts_template_schema_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1807_8_acceptance_blocks",
            any(
                row["gate_id"] == "AC1807_2_verdict"
                and row["current_status"] == "PRODUCT_FUNCTOR_NOT_SIGNED_PRIOR_WIDTH_PACK_NOT_SCORE_READY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks 1807 closure",
        ),
        (
            "VAL1807_9_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all product/prior/local-GR claim gates remain blocked",
        ),
        ("VAL1807_10_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1807_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1807_12_decision_next",
            any(
                row["decision_id"] == "DEC1807_3_best_next"
                and row["decision"] == "NO_MIXED_HIDDEN_VISIBLE_MORPHISM_LEMMA_OR_FIRST_PRIOR_WIDTH_CHAIN_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects no-mixed morphism or first prior-width chain next",
        ),
        (
            "VAL1807_13_next_selected",
            any(row["route_id"] == "NEXT1807_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1807_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1807 CSVs parse"),
        ("VAL1807_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1807_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1807_17_formalization_untouched", formalization_untouched(), "no 1807 outputs found under formalization-workbench"),
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
            "check_id": "VAL1807_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1807 visible-hidden product functor derivation or prior-width source pack checkpoint",
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
            "# 1807 - Y5/R2FR Visible-Hidden Product Functor Derivation or Prior-Width Source Pack",
            "",
            "## Verdict",
            "",
            "1807 isolates the clean theorem route. If visible EM, matter, clocks, and source coupling are pullbacks through `q_loc` plus representation data, hidden representative variations cannot generate `f_X F^2`, mass, binding, source-label, or clock-readout vertices.",
            "",
            "That product functor theorem is exact as a conditional, but it is not parent-signed. The current corpus still permits nonconstant invariant scalars, lacks a signed alpha owner, lacks a signed matter category/constants split, lacks source-label forgetting, and lacks radiative/readout closure.",
            "",
            "So this checkpoint does not claim zero for the coupling sector. It stages the first prior-width source pack and makes the next derivation target explicit: prove no nonconstant hidden-to-visible coefficient morphism, or start with the `b_alpha` clock-product prior chain.",
            "",
            "**Claim ceiling:** no product-functor theorem, no no-mixed-morphism theorem, no coefficient-zero claim, no prior-width score, no local-GR/Newton claim, no R10/WEP/clock claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1807.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Product Functor Theorem Attempt",
            markdown_table(rows_map["product_functor_theorem_attempt"], ["theorem_id", "claim_piece", "mathematical_form", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "",
            "## Visible Algebra Audit",
            markdown_table(rows_map["visible_algebra_audit"], ["algebra_id", "visible_object", "allowed_arguments", "forbidden_arguments", "status", "residual_if_open", "valid_for_claim"]),
            "",
            "## Product Functor Obstruction Ledger",
            markdown_table(rows_map["product_functor_obstruction_ledger"], ["obstruction_id", "obstruction", "example", "source_evidence", "effect", "claim_allowed", "valid_for_claim"]),
            "",
            "## Prior-Width Source Pack",
            markdown_table(rows_map["prior_width_source_pack"], ["pack_id", "symbol", "source_pack_target", "candidate_sources_in_hand", "still_missing", "promotion_status", "valid_for_claim"]),
            "",
            "## Projection Readiness",
            markdown_table(rows_map["projection_readiness"], ["readiness_id", "arena", "ready_inputs", "missing_inputs", "status", "valid_for_claim"]),
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
            "This is the fork in the road for the coupling problem. If no-mixed morphism can be proved, the theory gets a structural win. If the scalar obstruction survives, the honest route is not to mourn it but to build the first numeric prior chain and test the residuals like an engineered system.",
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
    print(f"1807 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
