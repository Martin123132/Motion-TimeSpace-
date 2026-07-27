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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1809"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1809_0_1808_doc",
        "source_key": "1808_doc",
        "source_path": ROOT / "1808-Y5-R2FR-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md",
        "needles": ["NEXT1808_0_primary", "BAP1808_2_best_current_product"],
        "role": "1808 handoff selecting tau-clock/Xhat normalization or alpha WEP/R10 projection.",
    },
    {
        "source_id": "SRC1809_1_1808_validation",
        "source_key": "1808_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1808_VALIDATION.csv",
        "needles": ["VAL1808_OVERALL", "PASS"],
        "role": "confirms 1808 passed before 1809 starts.",
    },
    {
        "source_id": "SRC1809_2_1808_chain",
        "source_key": "1808_chain",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
        "needles": ["BAP1808_1_CLOCK988_CAS646_1_YbE3E2", "2.1e-18"],
        "role": "current branch source-backed b_alpha*tau_clock product chain.",
    },
    {
        "source_id": "SRC1809_3_1808_projection",
        "source_key": "1808_projection",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1808_B_ALPHA_PROJECTION_READINESS.csv",
        "needles": ["BAPR1808_0_clock", "BAPR1808_2_R10"],
        "role": "current branch b_alpha projection readiness.",
    },
    {
        "source_id": "SRC1809_4_1052_doc",
        "source_key": "1052_doc",
        "source_path": ROOT / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
        "needles": ["TCN1052_4_verdict", "TG1052_3_R10_transfer"],
        "role": "older tau-clock/Xhat normalization and transfer gate checkpoint.",
    },
    {
        "source_id": "SRC1809_5_1052_tau",
        "source_key": "1052_tau",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
        "needles": ["TCN1052_0_product_definition", "TCN1052_4_verdict"],
        "role": "tau_clock/Xhat normalization audit.",
    },
    {
        "source_id": "SRC1809_6_1052_clock_bound",
        "source_key": "1052_clock_bound",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "needles": ["ACB1052_2", "2.1e-18"],
        "role": "clock product bound ledger.",
    },
    {
        "source_id": "SRC1809_7_1052_wep",
        "source_key": "1052_wep",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
        "needles": ["AWP1052_0_alpha_Coulomb", "4.797780522732e-05"],
        "role": "alpha WEP projection/pressure ledger.",
    },
    {
        "source_id": "SRC1809_8_1052_r10",
        "source_key": "1052_r10",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv",
        "needles": ["RAP1052_0_product_law", "RAP1052_2_clock_to_R10_transfer"],
        "role": "alpha R10 projection ledger.",
    },
    {
        "source_id": "SRC1809_9_1052_transfer",
        "source_key": "1052_transfer",
        "source_path": RESIDUALS / "P8_Y5_R10_1052_TRANSFER_CLAIM_GATES.csv",
        "needles": ["TG1052_1_standalone_balpha", "TG1052_3_R10_transfer"],
        "role": "transfer claim gates.",
    },
    {
        "source_id": "SRC1809_10_647_tau_clock",
        "source_key": "647_tau_clock",
        "source_path": RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
        "needles": ["TAU647_0_time_drift", "TAU647_1_H0_normalized_drift"],
        "role": "tau-clock map definitions.",
    },
    {
        "source_id": "SRC1809_11_647_chix",
        "source_key": "647_chix",
        "source_path": RESIDUALS / "P8_Y5_R10_647_CHIX_DEFINITION_ATTEMPT.csv",
        "needles": ["CHX647_1_finite_alpha_pressure_coordinate"],
        "role": "chi_X definition/status.",
    },
    {
        "source_id": "SRC1809_12_648_chix_dynamics",
        "source_key": "648_chix_dynamics",
        "source_path": RESIDUALS / "P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv",
        "needles": ["LCD648_3_parent_vertical_norm"],
        "role": "local chi_X dynamics/silence attempts.",
    },
    {
        "source_id": "SRC1809_13_988_joint_alpha",
        "source_key": "988_joint_alpha",
        "source_path": RESIDUALS / "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
        "needles": ["JAV988_1_clock_product", "JAV988_3_cross_arena_policy"],
        "role": "joint alpha variable policy gate.",
    },
    {
        "source_id": "SRC1809_14_988_wep_alpha",
        "source_key": "988_wep_alpha",
        "source_path": RESIDUALS / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
        "needles": ["WEP988_WAS651_0_alpha_Coulomb"],
        "role": "WEP alpha pressure import.",
    },
    {
        "source_id": "SRC1809_15_651_dd_charge",
        "source_key": "651_dd_charge",
        "source_path": RESIDUALS / "P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv",
        "needles": ["Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb"],
        "role": "Damour-Donoghue alpha/composition charge smoke estimates.",
    },
    {
        "source_id": "SRC1809_16_1035_source_test",
        "source_key": "1035_source_test",
        "source_path": RESIDUALS / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
        "needles": ["BETA1035_0_product_law"],
        "role": "R10 source/test charge split/product law.",
    },
    {
        "source_id": "SRC1809_17_1033_tau_r10",
        "source_key": "1033_tau_r10",
        "source_path": RESIDUALS / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
        "needles": ["TAUR1033_6_verdict"],
        "role": "tau_R10 derivation audit.",
    },
    {
        "source_id": "SRC1809_18_1053_doc",
        "source_key": "1053_doc",
        "source_path": ROOT / "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
        "needles": ["BSA1053_5_verdict", "DEC1053_3_best_next"],
        "role": "older beta-source/tau source-chain follow-up.",
    },
    {
        "source_id": "SRC1809_19_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "R2_clock_redshift"],
        "role": "local WEP/source and clock bound anchors.",
    },
    {
        "source_id": "SRC1809_20_R10_review_curve",
        "source_key": "R10_review_curve",
        "source_path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        "needles": ["review_candidate_only", "valid_for_claim"],
        "role": "R10 review-candidate curve for smoke only.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_SOURCE_REGISTER.csv",
    "tau_clock_xhat_normalization_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
    "alpha_clock_product_bound_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
    "alpha_wep_projection_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ALPHA_WEP_PROJECTION_LEDGER.csv",
    "alpha_r10_projection_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ALPHA_R10_PROJECTION_LEDGER.csv",
    "transfer_claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_TRANSFER_CLAIM_GATES.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1809_TAU_CLOCK_ALPHA_PROJECTION_TEMPLATE_NONCLAIM.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1809_VALIDATION.csv",
}

DOC_PATH = ROOT / "1809-Y5-R2FR-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"


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


def tau_clock_xhat_normalization_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TCN1809_0_product_definition",
            "claim_piece": "tau_clock_time definition",
            "mathematical_form": "tau_clock_time := d chi_X/dt and d ln(alpha_EM)/dt = b_alpha * tau_clock_time",
            "derivation_status": "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED",
            "support": "TAU647_0_time_drift",
            "blocking_gap": "chi_X parent state and local time projection are not derived",
            "usable_now": "clock data bound b_alpha*tau_clock_time only",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TCN1809_1_H0_diagnostic",
            "claim_piece": "H0-normalized diagnostic",
            "mathematical_form": "tau_clock_time = H0 * d chi_X/dN with nominal H0=7.16e-11 yr^-1",
            "derivation_status": "DIAGNOSTIC_ONLY",
            "support": "TAU647_1_H0_normalized_drift; AWP767_1_H0_screen",
            "blocking_gap": "no parent proof that lab clock tau equals H0 dchi_X/dN",
            "usable_now": "dimensionless diagnostic |b_alpha*dchi_X/dN| <= 2.93296e-08 for best row if H0 assumption is made",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TCN1809_2_chix_closure_coordinate",
            "claim_piece": "chi_X normalization",
            "mathematical_form": "d ln(alpha_EM)=b_alpha d chi_X",
            "derivation_status": "CLOSURE_COORDINATE_ONLY",
            "support": "CHX647_1_finite_alpha_pressure_coordinate",
            "blocking_gap": "chi_X is not identified with a parent-owned local field or normalized vertical norm",
            "usable_now": "finite-runner product-bound coordinate, not standalone b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TCN1809_3_local_silence",
            "claim_piece": "tau_clock_time = 0 local silence branch",
            "mathematical_form": "tau_clock_time=0 if strict local coframe or closed/gapped local boundary state is parent-selected",
            "derivation_status": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "support": "LCD648 local silence decisions",
            "blocking_gap": "strict-local representative and closed/gapped split remain unproved",
            "usable_now": "cannot use local silence to evade clock bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TCN1809_4_verdict",
            "claim_piece": "standalone b_alpha from clocks",
            "mathematical_form": "b_alpha = (d ln R/dt)/(DeltaK_alpha*tau_clock_time)",
            "derivation_status": "FAIL_CURRENT_CLAIM_TAU_NOT_DERIVED",
            "support": "1808 clock product chain plus 647 tau map",
            "blocking_gap": "tau_clock_time, Xhat/chi_X normalization, and shared WEP/R10 projection",
            "usable_now": "retain source-backed product bound only",
            "valid_for_claim": False,
        },
    ]


def alpha_clock_product_bound_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ACB1809_0",
            "row_type": "imported_clock_pair",
            "clock_pair": "27Al+ / 199Hg+",
            "delta_K_alpha": "2.95",
            "product_bound_1sigma_yr_inv": "3.9e-17",
            "product_bound_2sigma_yr_inv": "6.2e-17",
            "H0_normalized_diagnostic": "5.44693e-07",
            "interpretation": "bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived",
            "standalone_balpha_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ACB1809_1",
            "row_type": "imported_clock_pair",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "delta_K_alpha": "-6.95",
            "product_bound_1sigma_yr_inv": "2.1e-18",
            "product_bound_2sigma_yr_inv": "3.2e-18",
            "H0_normalized_diagnostic": "2.93296e-08",
            "interpretation": "bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock_time=H0*dchi_X/dN is derived",
            "standalone_balpha_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ACB1809_2",
            "row_type": "best_current",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "delta_K_alpha": "-6.95",
            "product_bound_1sigma_yr_inv": "2.1e-18",
            "product_bound_2sigma_yr_inv": "3.2e-18",
            "H0_normalized_diagnostic": "2.93296e-08",
            "interpretation": "best imported product row; useful clock-only nonclaim constraint",
            "standalone_balpha_ready": False,
            "valid_for_claim": False,
        },
    ]


def alpha_wep_projection_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": "AWP1809_0_alpha_Coulomb",
            "arena": "MICROSCOPE_WEP",
            "channel": "alpha/Coulomb composition channel",
            "source_row": "WEP988_WAS651_0_alpha_Coulomb",
            "delta_Q_abs": "1.989808886825e-03",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "5.836031862511e-11",
            "overshoot_factor": "2.084297e+04",
            "required_abs_beta_source_max": "4.797780522732e-05",
            "missing_for_claim": "beta_source_alpha theorem/prior; tau_WEP; shared domain rule; full material model",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "AWP1809_1_surface_binding",
            "arena": "MICROSCOPE_WEP",
            "channel": "surface/binding composition channel",
            "source_row": "WEP988_WAS651_1_surface_binding",
            "delta_Q_abs": "3.306456347405e-03",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "9.697707515141e-11",
            "overshoot_factor": "3.463467e+04",
            "required_abs_beta_source_max": "2.887280314062e-05",
            "missing_for_claim": "binding coefficient theorem/prior; tau_WEP; shared domain rule; full material model",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "AWP1809_2_clock_screen_warning",
            "arena": "cross_arena_policy",
            "channel": "clock-screen-only branch",
            "source_row": "JAV988_3_cross_arena_policy",
            "delta_Q_abs": "not_applicable",
            "eta_bound": "2.8e-15",
            "unit_source_eta_prediction": "not_applicable",
            "overshoot_factor": "not_applicable",
            "required_abs_beta_source_max": "not_applicable",
            "missing_for_claim": "same alpha domain/projection must be used in clock/WEP/R10 unless theorem-zero closes branch",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def alpha_r10_projection_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": "RAP1809_0_product_law",
            "arena": "R10_short_range",
            "formula": "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)",
            "support": "BETA1035_0_product_law",
            "available_inputs": "review-candidate nonclaim R10 bound curve",
            "missing_inputs": "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; alpha composition projection; promoted bound curve",
            "unity_shortcut": "rejected",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "RAP1809_1_tau_R10",
            "arena": "R10_short_range",
            "formula": "tau_R10 := normalized test-leg/material/readout projection under selected Yukawa profile convention",
            "support": "TAUR1033_2_tau_definition; TAUR1033_6_verdict",
            "available_inputs": "definition-only tau_R10 rows",
            "missing_inputs": "material/readout trace convention; Xhat normalization; finite-source correction; profile integral",
            "unity_shortcut": "do_not_set_tau_R10_to_one",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "projection_id": "RAP1809_2_clock_to_R10_transfer",
            "arena": "clock_to_R10_transfer",
            "formula": "clock product bound cannot determine alpha_X(lambda) without beta_s beta_t and tau_R10",
            "support": "1808 claim gate plus 1035/1033 projection rows",
            "available_inputs": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
            "missing_inputs": "relation between tau_clock_time and tau_R10; source/test alpha charges; K_X/Z_X",
            "unity_shortcut": "forbidden",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def transfer_claim_gates_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TG1809_0_clock_product_retained",
            "claim": "clock b_alpha product bound is usable as a nonclaim constraint row",
            "gate_status": "true_nonclaim_only",
            "reason": "source-backed product rows exist and are numerically populated",
            "promotion_blocker": "not standalone b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TG1809_1_standalone_balpha",
            "claim": "derive standalone b_alpha from clock product",
            "gate_status": "false",
            "reason": "tau_clock_time and Xhat/chi_X normalization are not parent-derived",
            "promotion_blocker": "TCN1809_4_verdict",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TG1809_2_WEP_transfer",
            "claim": "transfer clock b_alpha product to WEP",
            "gate_status": "false",
            "reason": "requires alpha composition charges, beta_source_alpha, tau_WEP and shared domain; stress-test rows show pressure but not pass",
            "promotion_blocker": "AWP1809 rows nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "TG1809_3_R10_transfer",
            "claim": "transfer clock b_alpha product to R10 alpha(lambda)",
            "gate_status": "false",
            "reason": "requires beta_s beta_t product, tau_R10, K_X/Z_X, lambda_X and promoted bound curve",
            "promotion_blocker": "RAP1809 rows nonclaim",
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "tau_clock_alpha_projection_template_1809",
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_TAU_R10_BETA_SOURCE_BETA_TEST_KX_ZX_FROM_CLOCK_PRODUCT",
            "force_law_form": "clock product bound constrains b_alpha*tau_clock_time; R10 needs beta_s beta_t K_X/Z_X tau_R10 and cannot be inferred directly",
            "derivation_status": "template_invalid_tau_clock_not_derived_and_R10_projection_missing",
            "valid_for_claim": False,
        }
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1809_0_tau_clock",
            "gate": "tau_clock_time and Xhat/chi_X normalization derived",
            "current_status": "BLOCKED",
            "reason": "tau_clock_time is product-defined but not parent-derived",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1809_1_transfer",
            "gate": "clock alpha product transferable to WEP/R10",
            "current_status": "BLOCKED",
            "reason": "WEP/R10 projection factors, source/test charges and shared-domain map are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1809_2_verdict",
            "gate": "clock product becomes standalone or cross-arena evidence",
            "current_status": "CLOCK_PRODUCT_RETAINED_STANDALONE_AND_TRANSFER_BLOCKED",
            "reason": "the product bound is source-backed but remains quarantined until tau/projection ownership closes",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1809_0_standalone_balpha",
            "claim": "clock product gives standalone b_alpha",
            "status": "BLOCKED",
            "reason": "tau_clock_time and Xhat/chi_X normalization are not parent-derived",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1809_1_H0_theory_claim",
            "claim": "H0-normalized diagnostic is an MTS theory prediction",
            "status": "BLOCKED",
            "reason": "no parent proof that lab tau_clock_time equals H0*dchi_X/dN",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1809_2_WEP_transfer",
            "claim": "clock product bound transfers to WEP",
            "status": "BLOCKED",
            "reason": "requires beta_source_alpha, tau_WEP, composition charge matrix and shared domain",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1809_3_R10_transfer",
            "claim": "clock product bound transfers to R10",
            "status": "BLOCKED",
            "reason": "requires beta_s beta_t, tau_R10, K_X/Z_X, lambda_X and promoted bound curve",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CL1809_4_local_GR_Newton",
            "claim": "local-GR/Newton branch closes from 1809",
            "status": "BLOCKED",
            "reason": "alpha transfer and source Hamiltonian/PPN gates remain open",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1809_0_tau_result",
            "decision": "TAU_CLOCK_TIME_REMAINS_PRODUCT_DEFINED_NOT_PARENT_DERIVED",
            "reason": "tau map defines the clock product but local chi_X dynamics and normalization remain conditional",
            "next_action": "do not promote standalone b_alpha",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1809_1_projection_result",
            "decision": "WEP_R10_PROJECTION_LEDGERS_EXPLICIT",
            "reason": "alpha composition pressure rows and R10 product-law rows exist but companion factors are missing",
            "next_action": "derive/source beta_source_alpha and tau_WEP/tau_R10 before transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1809_2_best_next",
            "decision": "BETA_SOURCE_ALPHA_AND_TAU_WEP_R10_SOURCE_CHAIN_NEXT",
            "reason": "standalone clock b_alpha is blocked; next empirical bridge is source/test projection",
            "next_action": "build 1810 to derive beta_source_alpha=0 or source first beta_source_alpha/tau_WEP prior width",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1809_0_primary",
            "next_target": "1810-Y5-R2FR-beta-source-alpha-and-tau-WEP-R10-source-chain.md",
            "script": "scripts/Y5_R2FR_beta_source_alpha_and_tau_WEP_R10_source_chain.py",
            "objective": "derive or source beta_source_alpha, tau_WEP, and tau_R10 so the b_alpha product branch can be tested consistently across clock, WEP, and R10 rather than as a clock-only screen",
            "selection_status": "selected",
            "success_condition": "beta_source_alpha theorem/prior and tau_WEP/tau_R10 source-chain rows, all nonclaim unless promotion gates close",
            "valid_for_claim": False,
        }
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "tau_clock_xhat_normalization_audit": tau_clock_xhat_normalization_audit_rows(),
        "alpha_clock_product_bound_ledger": alpha_clock_product_bound_ledger_rows(),
        "alpha_wep_projection_ledger": alpha_wep_projection_ledger_rows(),
        "alpha_r10_projection_ledger": alpha_r10_projection_ledger_rows(),
        "transfer_claim_gates": transfer_claim_gates_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1809_{key.upper()}.csv")


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
        "standalone_balpha_ready",
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
        "standalone_balpha_ready",
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
        if not (RAB_QUEUE / f"JR1809_{key.upper()}.csv").exists():
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
        ("VAL1809_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1809_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1809_2_tau_not_promoted",
            any(
                row["tau_id"] == "TCN1809_4_verdict"
                and row["derivation_status"] == "FAIL_CURRENT_CLAIM_TAU_NOT_DERIVED"
                and not boolish(row["valid_for_claim"])
                for row in rows_map["tau_clock_xhat_normalization_audit"]
            ),
            "standalone b_alpha remains blocked by tau/Xhat normalization",
        ),
        (
            "VAL1809_3_clock_bound_retained_nonclaim",
            any(row["bound_id"] == "ACB1809_2" and row["product_bound_1sigma_yr_inv"] == "2.1e-18" for row in rows_map["alpha_clock_product_bound_ledger"])
            and all(not boolish(row["standalone_balpha_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_clock_product_bound_ledger"]),
            "best clock product bound retained as nonclaim",
        ),
        (
            "VAL1809_4_wep_projection_nonclaim",
            any(row["projection_id"] == "AWP1809_0_alpha_Coulomb" and row["required_abs_beta_source_max"] == "4.797780522732e-05" for row in rows_map["alpha_wep_projection_ledger"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_wep_projection_ledger"]),
            "WEP alpha projection pressure is nonclaim and input-missing",
        ),
        (
            "VAL1809_5_r10_projection_nonclaim",
            any(row["projection_id"] == "RAP1809_2_clock_to_R10_transfer" and row["unity_shortcut"] == "forbidden" for row in rows_map["alpha_r10_projection_ledger"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_r10_projection_ledger"]),
            "R10 projection transfer remains blocked",
        ),
        (
            "VAL1809_6_transfer_gates_block",
            any(row["gate_id"] == "TG1809_0_clock_product_retained" and row["gate_status"] == "true_nonclaim_only" for row in rows_map["transfer_claim_gates"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["transfer_claim_gates"]),
            "transfer gates preserve clock product while blocking overclaims",
        ),
        (
            "VAL1809_7_mts_template_schema_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1809_8_acceptance_blocks",
            any(
                row["gate_id"] == "AC1809_2_verdict"
                and row["current_status"] == "CLOCK_PRODUCT_RETAINED_STANDALONE_AND_TRANSFER_BLOCKED"
                and not boolish(row["gate_pass"])
                for row in rows_map["acceptance_gate"]
            ),
            "acceptance gate blocks 1809 closure",
        ),
        (
            "VAL1809_9_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["claim_allowed"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all standalone/transfer/local-GR claim gates remain blocked",
        ),
        ("VAL1809_10_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1809_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1809_12_decision_next",
            any(
                row["decision_id"] == "DEC1809_2_best_next"
                and row["decision"] == "BETA_SOURCE_ALPHA_AND_TAU_WEP_R10_SOURCE_CHAIN_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects beta-source-alpha and tau WEP/R10 source chain next",
        ),
        (
            "VAL1809_13_next_selected",
            any(row["route_id"] == "NEXT1809_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1809_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1809 CSVs parse"),
        ("VAL1809_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1809_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1809_17_formalization_untouched", formalization_untouched(), "no 1809 outputs found under formalization-workbench"),
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
            "check_id": "VAL1809_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1809 tau-clock Xhat normalization or alpha WEP/R10 projection source checkpoint",
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
            "# 1809 - Y5/R2FR tau-clock/Xhat Normalization or Alpha WEP/R10 Projection Source",
            "",
            "## Verdict",
            "",
            "1809 keeps the first coupling number honest. The clock product bound is real and source-backed: the best current imported row gives `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1` at 1 sigma.",
            "",
            "But `tau_clock_time=d chi_X/dt` and the `Xhat/chi_X` normalization are product-map definitions, not parent-derived dynamics. Therefore the clock row cannot become standalone `b_alpha`, an H0-normalized theory claim, a WEP claim, an R10 claim, or a local-GR/Newton claim.",
            "",
            "The WEP/R10 transfer ledgers are now explicit. WEP gives a hard normalized-factor pressure target, while R10 requires source/test alpha charges, `tau_R10`, `K_X/Z_X`, `lambda_X`, and a promoted bound curve before any comparison is meaningful.",
            "",
            "**Claim ceiling:** no standalone `b_alpha`, no H0-normalized theory claim, no clock-to-WEP/R10 transfer, no local-GR/Newton claim, no R10/WEP/clock pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1809.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## tau-clock/Xhat Normalization Audit",
            markdown_table(rows_map["tau_clock_xhat_normalization_audit"], ["tau_id", "claim_piece", "mathematical_form", "derivation_status", "blocking_gap", "usable_now", "valid_for_claim"]),
            "",
            "## Alpha Clock Product Bound Ledger",
            markdown_table(rows_map["alpha_clock_product_bound_ledger"], ["bound_id", "row_type", "clock_pair", "product_bound_1sigma_yr_inv", "H0_normalized_diagnostic", "interpretation", "standalone_balpha_ready", "valid_for_claim"]),
            "",
            "## Alpha WEP Projection Ledger",
            markdown_table(rows_map["alpha_wep_projection_ledger"], ["projection_id", "arena", "channel", "delta_Q_abs", "eta_bound", "required_abs_beta_source_max", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Alpha R10 Projection Ledger",
            markdown_table(rows_map["alpha_r10_projection_ledger"], ["projection_id", "arena", "formula", "available_inputs", "missing_inputs", "unity_shortcut", "valid_for_claim"]),
            "",
            "## Transfer Claim Gates",
            markdown_table(rows_map["transfer_claim_gates"], ["gate_id", "claim", "gate_status", "reason", "promotion_blocker", "valid_for_claim"]),
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
            "This is not a defeat; it is a proper quarantine. The clock arena has given us the first sharp finite number in the coupling branch, but the bridge to WEP/R10/local-GR has to be built with source/test projections, not assumed. The next target is exactly that bridge.",
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
    print(f"1809 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
