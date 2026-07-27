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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1808"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1808_0_1807_doc",
        "source_key": "1807_doc",
        "source_path": ROOT / "1807-Y5-R2FR-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md",
        "needles": ["NEXT1807_0_primary", "DEC1807_3_best_next"],
        "role": "1807 handoff selecting no-mixed morphism or first prior-width chain.",
    },
    {
        "source_id": "SRC1808_1_1807_validation",
        "source_key": "1807_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1807_VALIDATION.csv",
        "needles": ["VAL1807_OVERALL", "PASS"],
        "role": "confirms 1807 passed before 1808 starts.",
    },
    {
        "source_id": "SRC1808_2_1807_next",
        "source_key": "1807_next",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1807_NEXT_TARGET.csv",
        "needles": ["NEXT1807_0_primary", "1808-Y5-R2FR"],
        "role": "current branch next-target row for 1808.",
    },
    {
        "source_id": "SRC1808_3_1051_doc",
        "source_key": "1051_doc",
        "source_path": ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
        "needles": ["NMM1051_5_verdict", "BAP1051_2_best_current_product"],
        "role": "older no-mixed morphism/prior chain checkpoint.",
    },
    {
        "source_id": "SRC1808_4_1051_no_mixed",
        "source_key": "1051_no_mixed",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
        "needles": ["NMM1051_2_scalar_counterexample", "NMM1051_5_verdict"],
        "role": "no-mixed morphism lemma attempt.",
    },
    {
        "source_id": "SRC1808_5_1051_scalar_obstruction",
        "source_key": "1051_scalar_obstruction",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
        "needles": ["ISO1051_0_hidden_scalar_I", "ISO1051_3_domain_marker"],
        "role": "hidden invariant scalar obstruction audit.",
    },
    {
        "source_id": "SRC1808_6_1051_alpha_audit",
        "source_key": "1051_alpha_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv",
        "needles": ["AOR1051_0_Maxwell_descent", "AOR1051_3_verdict"],
        "role": "alpha owner/radiative closure audit.",
    },
    {
        "source_id": "SRC1808_7_1051_balpha_chain",
        "source_key": "1051_balpha_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
        "needles": ["BAP1051_1_CLOCK988_CAS646_1_YbE3E2", "BAP1051_2_best_current_product"],
        "role": "first source-backed b_alpha*tau_clock product chain.",
    },
    {
        "source_id": "SRC1808_8_1051_projection",
        "source_key": "1051_projection",
        "source_path": RESIDUALS / "P8_Y5_R10_1051_B_ALPHA_PROJECTION_READINESS.csv",
        "needles": ["BAPR1051_0_clock", "BAPR1051_2_R10"],
        "role": "projection readiness for b_alpha branch.",
    },
    {
        "source_id": "SRC1808_9_988_clock_product",
        "source_key": "988_clock_product",
        "source_path": RESIDUALS / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv",
        "needles": ["CLOCK988_CAS646_1_YbE3E2", "standalone_b_alpha_bound_ready"],
        "role": "clock product import rows.",
    },
    {
        "source_id": "SRC1808_10_988_joint_alpha",
        "source_key": "988_joint_alpha",
        "source_path": RESIDUALS / "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "needles": ["JAV988_1_clock_product", "JAV988_3_cross_arena_policy"],
        "role": "joint alpha variable policy gate.",
    },
    {
        "source_id": "SRC1808_11_646_clock_sensitivity",
        "source_key": "646_clock_sensitivity",
        "source_path": RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
        "needles": ["CAS646_0_AlHg", "CAS646_1_YbE3E2"],
        "role": "source-backed clock alpha sensitivity rows.",
    },
    {
        "source_id": "SRC1808_12_1052_doc",
        "source_key": "1052_doc",
        "source_path": ROOT / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
        "needles": ["TCN1052_4_verdict", "TG1052_3_R10_transfer"],
        "role": "older tau-clock/Xhat normalization follow-up.",
    },
    {
        "source_id": "SRC1808_13_1052_tau_audit",
        "source_key": "1052_tau_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
        "needles": ["TCN1052_0_product_definition", "TCN1052_4_verdict"],
        "role": "tau_clock/Xhat normalization audit.",
    },
    {
        "source_id": "SRC1808_14_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R2_clock_redshift"],
        "role": "local WEP/source and clock bound anchors.",
    },
    {
        "source_id": "SRC1808_15_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate curve for smoke only.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_SOURCE_REGISTER.csv",
    "no_mixed_morphism_lemma_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
    "invariant_scalar_obstruction_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "alpha_owner_radiative_closure_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv",
    "b_alpha_clock_product_prior_chain": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
    "b_alpha_projection_readiness": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_B_ALPHA_PROJECTION_READINESS.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1808_B_ALPHA_CHAIN_TEMPLATE_NONCLAIM.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1808_VALIDATION.csv",
}

DOC_PATH = ROOT / "1808-Y5-R2FR-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"


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


def no_mixed_morphism_lemma_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_0_target",
            "claim_piece": "no nonconstant hidden-to-visible coefficient morphism",
            "mathematical_form": "Hom(C_hid,Coeff(O_vis)) = Const or 0 for O_vis in {F^2,mass,Yukawa,binding,clock,source}",
            "proof_status": "TARGET_SHARP",
            "obstruction": "none at definition level",
            "if_true": "kills f_X F^2 and b_alpha/mass/clock/source coefficient maps",
            "if_false": "retain coefficient priors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_1_trivial_hidden_algebra_case",
            "claim_piece": "trivial hidden invariant algebra implies no mixed morphism",
            "mathematical_form": "O(C_hid)^inv = R => any natural scalar coefficient c:C_hid->R is constant",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "obstruction": "current corpus has not proved hidden invariant algebra triviality",
            "if_true": "product functor can close visible coefficients",
            "if_false": "nonconstant scalar can feed visible coefficient",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_2_scalar_counterexample",
            "claim_piece": "surviving invariant scalar generates a mixed coefficient morphism",
            "mathematical_form": "I in O(C_hid)^inv, dI != 0 => c_I=c0+epsilon I and DeltaS=c_I O_vis is natural/covariant",
            "proof_status": "COUNTEREXAMPLE_PROVED",
            "obstruction": "scalar-obstruction lemma directly applies",
            "if_true": "no-mixed lemma fails unless I is forbidden or visible coefficients cannot take I",
            "if_false": "would need proof that all candidate I are absent",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_3_quotient_kernel_limit",
            "claim_piece": "Dq[v]=0 does not by itself kill hidden-to-visible coefficient maps",
            "mathematical_form": "Dq[v]=0, c(Phi)=c0+epsilon I_hid(Phi), Lie_v c = epsilon Lie_v I_hid can be nonzero",
            "proof_status": "LIMIT_IDENTIFIED",
            "obstruction": "quotient invisibility of geometry is not enough; coefficient functor domain must also exclude hidden invariants",
            "if_true": "forces separate no-mixed-morphism or prior route",
            "if_false": "would incorrectly claim constants descend from q",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_4_radiative_readout_limit",
            "claim_piece": "bare no-mixed morphism does not automatically survive EFT/readout",
            "mathematical_form": "S_bare no mixed terms does not imply S_eff/readout no mixed terms without symmetry or closure theorem",
            "proof_status": "UNSIGNED_CLOSURE",
            "obstruction": "alpha and clock readout can re-enter through renormalized/effective coefficients",
            "if_true": "needs radiative/readout closure before zero claim",
            "if_false": "b_alpha and b_clock_i remain live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "NMM1808_5_verdict",
            "claim_piece": "no-mixed-hidden-visible morphism lemma promotion",
            "mathematical_form": "NMM1808_1 plus no scalar counterexamples plus radiative/readout closure => no mixed visible coefficients",
            "proof_status": "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED",
            "obstruction": "scalar invariant obstruction and alpha/readout closure are open",
            "if_true": "constant-sector zero route revives",
            "if_false": "build first b_alpha clock-product prior chain",
            "valid_for_claim": False,
        },
    ]


def invariant_scalar_obstruction_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "ISO1808_0_hidden_scalar_I",
            "candidate_invariant": "generic hidden/local scalar I_hid",
            "mixed_coefficient": "c_I=c0+epsilon I_hid",
            "visible_operator": "F_Q^2, m_A psi_bar psi, clock readout, source weight",
            "status": "OBSTRUCTION_PROVED_IF_I_SURVIVES",
            "needed_to_close": "prove O(C_hid)^inv=R or forbid Coeff(O_vis) from taking hidden arguments",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "ISO1808_1_Xhat_value",
            "candidate_invariant": "Xhat or normalized hidden representative amplitude",
            "mixed_coefficient": "f_X(Xhat)",
            "visible_operator": "F_Q^2",
            "status": "LIVE_UNLESS_PRODUCT_FUNCTOR_SIGNED",
            "needed_to_close": "exact shift/sequester/product functor or Xhat=0 theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "ISO1808_2_gradient_norm",
            "candidate_invariant": "nabla Xhat squared or local hidden profile norm",
            "mixed_coefficient": "f((nabla Xhat)^2)",
            "visible_operator": "mass/binding/clock coefficient",
            "status": "EVEN_PARITY_SURVIVOR",
            "needed_to_close": "positive no-hair/profile-zero theorem or product functor",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "ISO1808_3_domain_marker",
            "candidate_invariant": "domain/source/material class marker",
            "mixed_coefficient": "theta_A(marker), kappa_A(marker)",
            "visible_operator": "source/test coupling and matter constants",
            "status": "LIVE_LABEL_OBSTRUCTION",
            "needed_to_close": "source label-forgetting and no-marker functor theorem",
            "valid_for_claim": False,
        },
    ]


def alpha_owner_radiative_closure_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AOR1808_0_Maxwell_descent",
            "object": "Maxwell action descent",
            "current_evidence": "Maxwell closure form is supported, but alpha constant owner remains blocked",
            "status": "PARTIAL",
            "missing_for_balpha_zero": "g_EM/alpha owner; Hodge/readout owner; source current normalization",
            "fallback": "b_alpha clock-product prior chain",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AOR1808_1_clock_product",
            "object": "clock product bound",
            "current_evidence": "clock import rows bound |b_alpha*tau_clock_time| from alpha-sensitive clock comparisons",
            "status": "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "missing_for_balpha_zero": "tau_clock dynamics and Xhat normalization",
            "fallback": "retain product bound, not standalone b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AOR1808_2_cross_arena",
            "object": "shared alpha branch across clock/WEP/R10",
            "current_evidence": "joint-alpha gate warns S_lab_alpha cannot be clock-only",
            "status": "POLICY_GATE_ACTIVE",
            "missing_for_balpha_zero": "shared local domain/projection rule and WEP/R10 source charge maps",
            "fallback": "do not transfer clock product to WEP/R10 without projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "AOR1808_3_verdict",
            "object": "b_alpha zero/provenance",
            "current_evidence": "no-mixed morphism fails current claim and alpha owner remains unsigned",
            "status": "RETAIN_B_ALPHA_PRODUCT_CHAIN",
            "missing_for_balpha_zero": "no mixed morphism theorem or alpha owner/radiative closure",
            "fallback": "source-backed b_alpha*tau_clock product bound only",
            "valid_for_claim": False,
        },
    ]


def b_alpha_clock_product_prior_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": "BAP1808_0_CLOCK988_CAS646_0_AlHg",
            "clock_pair": "27Al+ / 199Hg+",
            "delta_K_alpha": "2.95",
            "drift_source_value": "NIST: 1.4e-17 +/- 1.7e-17 yr^-1; Frontiers table reports -1.6e-17 +/- 2.3e-17 yr^-1",
            "product_bound_1sigma_yr_inv": "3.9e-17",
            "product_bound_2sigma_yr_inv": "6.2e-17",
            "H0_normalized_diagnostic": "5.44693e-07",
            "formula": "|b_alpha*tau_clock_time| <= |d ln R/dt|_bound / |DeltaK_alpha|",
            "source_urls": "https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "standalone_balpha_ready": False,
            "missing_for_standalone": "tau_clock_time; Xhat/chi_X normalization; clock domain map; shared WEP/R10 projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "BAP1808_1_CLOCK988_CAS646_1_YbE3E2",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "delta_K_alpha": "-6.95",
            "drift_source_value": "PTB/Frontiers: 1.0e-18 +/- 1.1e-18 yr^-1",
            "product_bound_1sigma_yr_inv": "2.1e-18",
            "product_bound_2sigma_yr_inv": "3.2e-18",
            "H0_normalized_diagnostic": "2.93296e-08",
            "formula": "|b_alpha*tau_clock_time| <= |d ln R/dt|_bound / |DeltaK_alpha|",
            "source_urls": "https://oar.ptb.de/resources/show/10.7795/110.20211216; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "standalone_balpha_ready": False,
            "missing_for_standalone": "tau_clock_time; Xhat/chi_X normalization; clock domain map; shared WEP/R10 projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "BAP1808_2_best_current_product",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "delta_K_alpha": "-6.95",
            "drift_source_value": "PTB/Frontiers imported row",
            "product_bound_1sigma_yr_inv": "2.1e-18",
            "product_bound_2sigma_yr_inv": "3.2e-18",
            "H0_normalized_diagnostic": "2.93296e-08",
            "formula": "best current imported product bound; diagnostic H0 normalization is not a theory claim",
            "source_urls": "source-intake/mts_residuals/P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv; source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "standalone_balpha_ready": False,
            "missing_for_standalone": "derive tau_clock_time from MTS local state",
            "valid_for_claim": False,
        },
    ]


def b_alpha_projection_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": "BAPR1808_0_clock",
            "arena": "clock",
            "current_status": "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "usable_now": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 best imported 1sigma product row",
            "missing_for_claim": "tau_clock_time from MTS; alpha owner or no-mixed theorem; separation from other constants",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "BAPR1808_1_WEP",
            "arena": "WEP/MICROSCOPE",
            "current_status": "ANCHOR_ONLY",
            "usable_now": "eta bound exists, but alpha composition charge and beta_source_alpha are missing",
            "missing_for_claim": "DeltaQ_alpha_AB; beta_source_alpha; tau_WEP; shared domain rule",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "BAPR1808_2_R10",
            "arena": "R10 short-range",
            "current_status": "SMOKE_ONLY",
            "usable_now": "review-candidate bound curve exists but is not promoted",
            "missing_for_claim": "lambda_X; Z_X; K_X; source/test alpha charge; promoted bound curve",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "BAPR1808_3_PPN",
            "arena": "local GR/PPN",
            "current_status": "NOT_SCORE_READY",
            "usable_now": "no direct PPN b_alpha map",
            "missing_for_claim": "weak-field/source Hamiltonian solution plus constant-sector leakage map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "b_alpha_product_chain_template_1808",
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_B_ALPHA_TAU_TO_R10_SOURCE_TEST_PROJECTION",
            "force_law_form": "R10 alpha(lambda) from b_alpha branch requires source/test alpha charges and tau_R10; clock product bound alone is not an R10 prediction",
            "derivation_status": "template_invalid_no_mixed_morphism_failed_and_R10_projection_missing",
            "valid_for_claim": False,
        }
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1808_0_no_mixed",
            "gate": "no mixed hidden-visible morphism lemma promoted",
            "current_status": "BLOCKED",
            "reason": "surviving invariant scalar counterexample and radiative/readout closure gap remain",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1808_1_product_bound",
            "gate": "first b_alpha product chain source-backed",
            "current_status": "NONCLAIM_PRODUCT_BOUND_AVAILABLE",
            "reason": "clock product bounds are sourced, but standalone b_alpha and transfer claims are blocked",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1808_2_verdict",
            "gate": "no-mixed or prior chain closes alpha branch",
            "current_status": "NO_MIXED_FAILED_PRODUCT_BOUND_NONCLAIM_ONLY",
            "reason": "the first numeric chain exists but still needs tau_clock/Xhat normalization before standalone or cross-arena use",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1808_0_no_mixed",
            "claim": "no-mixed hidden-visible morphism lemma is proved",
            "status": "BLOCKED",
            "reason": "scalar invariant counterexample survives unless hidden invariant algebra is trivial or product functor is signed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1808_1_standalone_balpha",
            "claim": "clock data bound standalone b_alpha",
            "status": "BLOCKED",
            "reason": "tau_clock_time and Xhat/chi_X normalization are not derived",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1808_2_WEP_R10_transfer",
            "claim": "clock b_alpha product transfers to WEP/R10",
            "status": "BLOCKED",
            "reason": "requires shared projection, alpha source/test charges, tau_WEP/tau_R10, K_X/Z_X and promoted R10 bound curve",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1808_3_local_GR_Newton",
            "claim": "local-GR/Newton branch closes from 1808",
            "status": "BLOCKED",
            "reason": "alpha branch remains product-bound only and source Hamiltonian/PPN gates remain separate",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1808_0_lemma_result",
            "decision": "NO_MIXED_LEMMA_FAILS_CURRENT_PROMOTION",
            "reason": "a surviving hidden invariant scalar can form a visible coefficient morphism",
            "next_action": "either prove invariant algebra triviality or keep residual priors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1808_1_balpha_progress",
            "decision": "FIRST_NUMERICAL_PRIOR_CHAIN_EXISTS_FOR_B_ALPHA_TAU_CLOCK_TIME",
            "reason": "clock import rows give source-backed product bounds from alpha sensitivities",
            "next_action": "derive tau_clock_time or source alpha WEP/R10 projections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1808_2_best_next",
            "decision": "TAU_CLOCK_XHAT_NORMALIZATION_OR_ALPHA_WEP_R10_PROJECTION_NEXT",
            "reason": "the clock product bound is useful but cannot become b_alpha or R10/WEP evidence without tau/projection",
            "next_action": "build 1809 to derive tau_clock_time/Xhat normalization or source alpha WEP/R10 projection inputs",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1808_0_primary",
            "next_target": "1809-Y5-R2FR-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
            "script": "scripts/Y5_R2FR_tau_clock_Xhat_normalization_or_alpha_WEP_R10_projection_source.py",
            "objective": "derive tau_clock_time and Xhat/chi_X normalization for the b_alpha clock-product chain; if that fails, source the alpha WEP/R10 composition/projection inputs needed to prevent clock-only screening",
            "selection_status": "selected",
            "success_condition": "standalone-transfer theorem or nonclaim transfer ledger blocking overclaim while preserving source-backed clock product rows",
            "valid_for_claim": False,
        }
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_mixed_morphism_lemma_attempt": no_mixed_morphism_lemma_attempt_rows(),
        "invariant_scalar_obstruction_audit": invariant_scalar_obstruction_audit_rows(),
        "alpha_owner_radiative_closure_audit": alpha_owner_radiative_closure_audit_rows(),
        "b_alpha_clock_product_prior_chain": b_alpha_clock_product_prior_chain_rows(),
        "b_alpha_projection_readiness": b_alpha_projection_readiness_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1808_{key.upper()}.csv")


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
        "standalone_balpha_ready",
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
        "standalone_balpha_ready",
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
        if not (RAB_QUEUE / f"JR1808_{key.upper()}.csv").exists():
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
        ("VAL1808_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1808_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1808_2_no_mixed_blocked",
            any(
                row["lemma_id"] == "NMM1808_5_verdict"
                and row["proof_status"] == "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED"
                for row in rows_map["no_mixed_morphism_lemma_attempt"]
            ),
            "no-mixed morphism lemma remains unpromoted",
        ),
        (
            "VAL1808_3_scalar_obstructions_present",
            len(rows_map["invariant_scalar_obstruction_audit"]) >= 4
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["invariant_scalar_obstruction_audit"]),
            "hidden invariant scalar obstructions are retained",
        ),
        (
            "VAL1808_4_alpha_audit_product_only",
            any(
                row["audit_id"] == "AOR1808_3_verdict"
                and row["status"] == "RETAIN_B_ALPHA_PRODUCT_CHAIN"
                and not boolish(row["valid_for_claim"])
                for row in rows_map["alpha_owner_radiative_closure_audit"]
            ),
            "alpha owner audit retains product-chain fallback only",
        ),
        (
            "VAL1808_5_product_chain_source_backed_nonclaim",
            len(rows_map["b_alpha_clock_product_prior_chain"]) >= 3
            and any(row["chain_id"] == "BAP1808_2_best_current_product" and row["product_bound_1sigma_yr_inv"] == "2.1e-18" for row in rows_map["b_alpha_clock_product_prior_chain"])
            and all(not boolish(row["standalone_balpha_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["b_alpha_clock_product_prior_chain"]),
            "b_alpha*tau_clock product chain is present and nonclaim",
        ),
        (
            "VAL1808_6_projection_readiness_blocks_transfer",
            all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["b_alpha_projection_readiness"])
            and any(row["projection_id"] == "BAPR1808_2_R10" and row["current_status"] == "SMOKE_ONLY" for row in rows_map["b_alpha_projection_readiness"]),
            "projection readiness blocks standalone and R10/WEP transfer claims",
        ),
        (
            "VAL1808_7_mts_template_schema_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1808_8_acceptance_blocks",
            any(
                row["gate_id"] == "AC1808_2_verdict"
                and row["current_status"] == "NO_MIXED_FAILED_PRODUCT_BOUND_NONCLAIM_ONLY"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks 1808 closure",
        ),
        (
            "VAL1808_9_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all no-mixed/product/local-GR claim gates remain blocked",
        ),
        ("VAL1808_10_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1808_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1808_12_decision_next",
            any(
                row["decision_id"] == "DEC1808_2_best_next"
                and row["decision"] == "TAU_CLOCK_XHAT_NORMALIZATION_OR_ALPHA_WEP_R10_PROJECTION_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects tau-clock/Xhat normalization or alpha WEP/R10 projection next",
        ),
        (
            "VAL1808_13_next_selected",
            any(row["route_id"] == "NEXT1808_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1808_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1808 CSVs parse"),
        ("VAL1808_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1808_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1808_17_formalization_untouched", formalization_untouched(), "no 1808 outputs found under formalization-workbench"),
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
            "check_id": "VAL1808_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1808 no-mixed morphism lemma or first b_alpha product prior chain checkpoint",
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
            "# 1808 - Y5/R2FR No-Mixed Hidden-Visible Morphism Lemma or First Prior-Width Chain",
            "",
            "## Verdict",
            "",
            "1808 tests the last clean derivation route in this coupling branch. A no-mixed morphism theorem would say hidden/local variables cannot map into visible coefficients for EM, masses, binding, clocks, or source labels.",
            "",
            "The theorem is exact only if the hidden invariant algebra is trivial or the parent observable algebra forbids hidden-to-visible coefficient morphisms. The current corpus does not prove that. A surviving invariant scalar `I_hid` gives the counterexample `c_I=c0+epsilon I_hid`, so `Dq[v]=0` alone is not enough.",
            "",
            "The useful progress is numerical but carefully fenced: clock data now provide source-backed nonclaim bounds on the product `b_alpha*tau_clock_time`. The best imported product row is `2.1e-18 yr^-1` at 1 sigma from Yb+ E3/E2. This is not a standalone `b_alpha`, WEP, R10, or local-GR claim.",
            "",
            "**Claim ceiling:** no no-mixed morphism theorem, no standalone `b_alpha`, no H0-normalized theory claim, no clock-to-WEP/R10 transfer, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1808.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## No-Mixed Morphism Lemma Attempt",
            markdown_table(rows_map["no_mixed_morphism_lemma_attempt"], ["lemma_id", "claim_piece", "mathematical_form", "proof_status", "obstruction", "if_false", "valid_for_claim"]),
            "",
            "## Invariant Scalar Obstruction Audit",
            markdown_table(rows_map["invariant_scalar_obstruction_audit"], ["obstruction_id", "candidate_invariant", "mixed_coefficient", "visible_operator", "status", "needed_to_close", "valid_for_claim"]),
            "",
            "## Alpha Owner/Radiative Closure Audit",
            markdown_table(rows_map["alpha_owner_radiative_closure_audit"], ["audit_id", "object", "current_evidence", "status", "missing_for_balpha_zero", "fallback", "valid_for_claim"]),
            "",
            "## b_alpha Clock Product Prior Chain",
            markdown_table(rows_map["b_alpha_clock_product_prior_chain"], ["chain_id", "clock_pair", "delta_K_alpha", "product_bound_1sigma_yr_inv", "product_bound_2sigma_yr_inv", "formula", "standalone_balpha_ready", "valid_for_claim"]),
            "",
            "## b_alpha Projection Readiness",
            markdown_table(rows_map["b_alpha_projection_readiness"], ["projection_id", "arena", "current_status", "usable_now", "missing_for_claim", "claim_allowed", "valid_for_claim"]),
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
            "This is progress in the engineering sense: the clean zero proof failed for a specific reason, and the fallback now has a real source-backed product bound. The next choke point is `tau_clock_time` and `Xhat/chi_X` normalization. Without that, the number stays useful but quarantined.",
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
    print(f"1808 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
