from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1471"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1471-Y5-R10-RAB-radiative-readout-closure-or-alpha-product-prediction-fill.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1470_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1470_VALIDATION.csv"
PREV_TYPED = OUT / "P8_Y5_R10_1470_TYPED_VISIBLE_ACTION_GRAMMAR_ATTEMPT.csv"
PREV_RADIATIVE = OUT / "P8_Y5_R10_1470_RADIATIVE_READOUT_CLOSURE_AUDIT.csv"
PREV_ALPHA_FILL = OUT / "P8_Y5_R10_1470_ALPHA_PRODUCT_SOURCE_FILL_NONCLAIM.csv"

RADIATIVE_1051 = OUT / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv"
PROJECTION_1051 = OUT / "P8_Y5_R10_1051_B_ALPHA_PROJECTION_READINESS.csv"
CLOCK_CHAIN_1051 = OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"
RETAINED_1056 = OUT / "P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv"
TAU_CLOCK_647 = OUT / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv"
COEFF_ROWS_1099 = OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv"
PRED_1099 = OUT / "P8_Y5_R10_1099_ALPHA_PRODUCT_PREDICTION_NONCLAIM.csv"
PRED_1102 = OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv"
INPUT_1102 = OUT / "P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv"
DIRECT_CLOCK_1323 = OUT / "P8_Y5_R10_1323_DIRECT_CLOCK_PRODUCT_SOURCE_PACK.csv"
DIRECT_EQUATION_1324 = OUT / "P8_Y5_R10_1324_DIRECT_PRODUCT_EQUATION_ATTEMPT.csv"
WEP_PRIOR_1403 = OUT / "P8_Y5_R10_1403_BETA_SOURCE_TAU_WEP_PRIOR.csv"
WEP_SCHEMA_1407 = OUT / "P8_Y5_R10_1407_SECTOR_BETA_SOURCE_SCHEMA.csv"
WEP_TEMPLATE_1408 = OUT / "P8_Y5_R10_1408_SOURCE_READY_TEMPLATE_ROWS.csv"
BETA_ALPHA_1414 = OUT / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv"
R10_ALPHA_1034 = OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv"
BOUND_MATRIX_1048 = OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_RADIATIVE = COEFF / "radiative_readout_closure_parent_signed_import.csv"
LIVE_ALPHA_PRODUCT = COEFF / "alpha_residual_product_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1471_SOURCE_REGISTER.csv"
RADIATIVE_CLOSURE = OUT / "P8_Y5_R10_1471_RADIATIVE_READOUT_CLOSURE_ATTEMPT.csv"
READOUT_CLOSURE = OUT / "P8_Y5_R10_1471_CLOCK_WEP_R10_READOUT_CLOSURE_AUDIT.csv"
PREDICTION_COMPONENTS = OUT / "P8_Y5_R10_1471_ALPHA_PRODUCT_PREDICTION_COMPONENT_LEDGER.csv"
PREDICTION_FILL = OUT / "P8_Y5_R10_1471_ALPHA_PRODUCT_PREDICTION_FILL_NONCLAIM.csv"
PREDICTION_STATUS = OUT / "P8_Y5_R10_1471_ALPHA_PRODUCT_PREDICTION_STATUS.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1471_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1471_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1471_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1471_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1471_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1471_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1471_VALIDATION.csv"

QUAR_PREDICTION_FILL = QUARANTINE / "ALPHA_PRODUCT_PREDICTION_FILL_NONCLAIM.csv"
QUAR_COMPONENTS = QUARANTINE / "ALPHA_PRODUCT_PREDICTION_COMPONENT_LEDGER.csv"
BRANCH_PREDICTION_FILL = COEFF / "alpha_product_prediction_fill_nonclaim_1471.csv"
BRANCH_COMPONENTS = COEFF / "alpha_product_prediction_components_nonclaim_1471.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_radiative_readout_signing_decision_1471.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1471_0_1470_next", PREV_NEXT, "1470 handoff to radiative/readout closure or alpha prediction fill"),
        ("SRC1471_1_1470_validation", PREV_VALIDATION, "1470 validation baseline"),
        ("SRC1471_2_1470_typed", PREV_TYPED, "typed/no-extension conditional theorem and refusal"),
        ("SRC1471_3_1470_radiative", PREV_RADIATIVE, "1470 unsigned radiative/readout audit"),
        ("SRC1471_4_1470_alpha_fill", PREV_ALPHA_FILL, "1470 comparison-side alpha product source fill"),
        ("SRC1471_5_1051_radiative", RADIATIVE_1051, "older alpha-owner radiative closure audit"),
        ("SRC1471_6_1051_projection", PROJECTION_1051, "clock/WEP/R10 projection readiness"),
        ("SRC1471_7_1051_clock_chain", CLOCK_CHAIN_1051, "clock product prior chain"),
        ("SRC1471_8_1056_retained", RETAINED_1056, "retained b_alpha branch ledger"),
        ("SRC1471_9_tau_clock", TAU_CLOCK_647, "tau clock map definitions"),
        ("SRC1471_10_coeff_rows", COEFF_ROWS_1099, "alpha coefficient source rows"),
        ("SRC1471_11_pred_1099", PRED_1099, "older alpha product prediction nonclaim"),
        ("SRC1471_12_pred_1102", PRED_1102, "alpha product prediction attempt nonclaim"),
        ("SRC1471_13_input_1102", INPUT_1102, "alpha product input status"),
        ("SRC1471_14_direct_clock", DIRECT_CLOCK_1323, "direct clock product source pack"),
        ("SRC1471_15_direct_equation", DIRECT_EQUATION_1324, "direct product equation attempt"),
        ("SRC1471_16_wep_prior", WEP_PRIOR_1403, "beta_source tau WEP prior"),
        ("SRC1471_17_wep_schema", WEP_SCHEMA_1407, "sector beta/source schema"),
        ("SRC1471_18_wep_template", WEP_TEMPLATE_1408, "source-ready WEP template rows"),
        ("SRC1471_19_beta_alpha", BETA_ALPHA_1414, "WEP alpha finite bound/target rows"),
        ("SRC1471_20_R10_alpha", R10_ALPHA_1034, "R10 alpha bound candidate rows"),
        ("SRC1471_21_bound_matrix", BOUND_MATRIX_1048, "alpha/mass/clock bound matrix"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": str(path.relative_to(ROOT)),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def radiative_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RRC1471_0_exact_conditional",
            "target": "renormalized visible coefficient domain preservation",
            "formal_statement": "If the parent effective-action functor R maps typed visible operators to typed visible operators and never enlarges coefficient domains from Q_vis to Q_vis x I_hid, then D_hid Z_EM^eff = 0 by functorial domain preservation.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Bare coefficients factor through pi_vis; R is assumed natural over pi_vis and closed on the visible operator category; composition R o pi_vis still factors through pi_vis, so hidden vertical derivatives vanish.",
            "missing_parent_signature": "parent theorem that loop/threshold/coarse-graining/readout renormalization is a typed endofunctor on the visible action grammar",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RRC1471_1_no_threshold_leak",
            "target": "threshold masses and clock/matter labels do not re-enter alpha",
            "formal_statement": "Every threshold/readout mass m_i and label L_i used by clocks, WEP materials, or R10 source/test bodies must itself factor through the same visible quotient before it can enter Z_EM^eff.",
            "result": "REQUIRED_CLOSURE_NOT_DERIVED",
            "proof_sketch": "Otherwise ln m_i(I_hid), material fractions, or source/test labels can appear in ln Z_EM^eff even when the bare F^2 term is typed cleanly.",
            "missing_parent_signature": "threshold/readout/source-label forgetting theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RRC1471_2_observed_readout_bridge",
            "target": "clock/WEP/R10 observables preserve the no-hidden grammar",
            "formal_statement": "The observable map O_clock,WEP,R10 must be a domain-preserving natural transformation from parent fields to measured ratios/accelerations/alpha(lambda).",
            "result": "UNSIGNED_REQUIRED_BRIDGE",
            "proof_sketch": "A clean parent action does not by itself prove clean laboratory readout; the readout kernel may attach composition, source, or apparatus labels.",
            "missing_parent_signature": "lab readout functor and source/material kernel derived from MTS parent geometry",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "RRC1471_3_verdict",
            "target": "radiative/readout preservation closes the alpha branch",
            "formal_statement": "RRC1471_0 plus RRC1471_1 plus RRC1471_2 would permit alpha-product theorem-zero promotion.",
            "result": "REFUSE_PROMOTION_START_PREDICTION_FILL",
            "proof_sketch": "Only the first clause is an exact conditional theorem; the threshold/readout bridge is still unsigned.",
            "missing_parent_signature": "parent-signed effective/readout closure package",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def readout_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RO1471_0_clock",
            "arena": "clock_fine_structure",
            "required_clause": "clock frequency ratios see only parent-owned alpha variation and not hidden clock/readout coefficients",
            "available_evidence": "TAU647_0 defines tau_clock_time; EQ1324_0 defines dlnR/dt = DeltaK_alpha dln alpha_eff/dt; DCLK1323_0 still marks direct MTS product missing",
            "status": "DEFINITION_LINKED_READOUT_UNSIGNED",
            "fallback": "retain |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 as product bound, not prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RO1471_1_WEP",
            "arena": "MICROSCOPE_WEP",
            "required_clause": "material/source readout maps DeltaQ_alpha_AB, beta_source_alpha, and tau_WEP from parent fields without hidden label leakage",
            "available_evidence": "IN1102_3 gives smoke DeltaQ_alpha_AB; BWP1403 and BSB1414 define target-only source products; schema/template rows define needed source-ready columns",
            "status": "PARTIAL_COMPONENTS_LINKED_SOURCE_KERNEL_UNSIGNED",
            "fallback": "retain P_WEP_alpha product row with source/tau/basis missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RO1471_2_R10",
            "arena": "R10_short_range",
            "required_clause": "source/test charge construction gives K_X, Qbar_source, Qbar_test, Z_X, lambda_X in the same parent basis as alpha(lambda) bounds",
            "available_evidence": "R10B1034 rows provide comparison-side bound candidates; BAB1056_2 and ASR1099_4 keep projection inputs missing",
            "status": "BOUND_LINKED_PREDICTION_KERNEL_MISSING",
            "fallback": "retain alpha(lambda) product scaffold; do not claim R10/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RO1471_3_mass_clock",
            "arena": "mass_clock_constants",
            "required_clause": "mass/nuclear/clock sensitivity matrix is sourced in parent coefficient basis with units and sign convention",
            "available_evidence": "BM1048 matrix exists but no single MTS product row; EQ1324_2 says factorized clock product still needs parent b_alpha/tau",
            "status": "MATRIX_LINKED_SINGLE_PREDICTION_MISSING",
            "fallback": "keep matrix as partial nonclaim constraint source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def prediction_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_0_alpha_clock",
            "component_id": "COMP1471_clock_0_deltaK",
            "quantity": "DeltaK_alpha(YbE3/YbE2)",
            "value_or_status": "-6.95",
            "units": "dimensionless sensitivity",
            "source_path": str(CLOCK_CHAIN_1051.relative_to(ROOT)),
            "source_anchor": "BAP1051_1_CLOCK988_CAS646_1_YbE3E2; BAP1051_2_best_current_product",
            "fill_status": "SOURCE_BACKED_COMPONENT_AVAILABLE",
            "valid_for_prediction": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_0_alpha_clock",
            "component_id": "COMP1471_clock_1_tau",
            "quantity": "tau_clock_time",
            "value_or_status": "MISSING_PARENT_TAU_CLOCK_XHAT_MAP",
            "units": "yr^-1 per normalized Xhat unit",
            "source_path": str(TAU_CLOCK_647.relative_to(ROOT)),
            "source_anchor": "TAU647_0_time_drift; TAU647_3_local_silence",
            "fill_status": "DEFINITION_AVAILABLE_VALUE_MISSING",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_0_alpha_clock",
            "component_id": "COMP1471_clock_2_balpha",
            "quantity": "b_alpha_EM",
            "value_or_status": "MISSING_PARENT_ALPHA_OWNER_OR_THEOREM_ZERO",
            "units": "dimensionless vertical derivative",
            "source_path": str(COEFF_ROWS_1099.relative_to(ROOT)),
            "source_anchor": "ASR1099_0_theorem_zero_candidate",
            "fill_status": "THEOREM_ZERO_CANDIDATE_UNSIGNED",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_1_WEP_alpha",
            "component_id": "COMP1471_wep_0_deltaQ",
            "quantity": "DeltaQ_alpha_AB",
            "value_or_status": "1.989808886825000e-03",
            "units": "dimensionless smoke material contrast",
            "source_path": str(INPUT_1102.relative_to(ROOT)),
            "source_anchor": "IN1102_3_delta_Q_alpha",
            "fill_status": "SMOKE_COMPONENT_AVAILABLE_NOT_OFFICIAL_CLAIM",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_1_WEP_alpha",
            "component_id": "COMP1471_wep_1_beta_source",
            "quantity": "beta_source_alpha",
            "value_or_status": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER",
            "units": "dimensionless source coefficient",
            "source_path": str(BETA_ALPHA_1414.relative_to(ROOT)),
            "source_anchor": "BSB1414_0_definition; BSB1414_3_parent_basis_required",
            "fill_status": "DEFINITION_AVAILABLE_VALUE_MISSING",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_1_WEP_alpha",
            "component_id": "COMP1471_wep_2_tau",
            "quantity": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless projection factor",
            "source_path": str(INPUT_1102.relative_to(ROOT)),
            "source_anchor": "IN1102_6_tau_WEP",
            "fill_status": "DEFINITION_AVAILABLE_VALUE_MISSING",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_1_WEP_alpha",
            "component_id": "COMP1471_wep_3_schema",
            "quantity": "sector beta/source schema",
            "value_or_status": "SOURCE_READY_COLUMNS_DEFINED",
            "units": "schema",
            "source_path": str(WEP_SCHEMA_1407.relative_to(ROOT)),
            "source_anchor": "SCHEMA1407_0_beta_e..SCHEMA1407_5_Delta_f",
            "fill_status": "SCHEMA_READY_NO_NUMERIC_PARENT_FILL",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_2_R10_alpha_lambda",
            "component_id": "COMP1471_r10_0_bound",
            "quantity": "alpha_bound(lambda)",
            "value_or_status": "0.002344664300519378..897932.2928704522 review-candidate",
            "units": "dimensionless alpha(lambda)",
            "source_path": str(R10_ALPHA_1034.relative_to(ROOT)),
            "source_anchor": "R10B1034_3_vector_review_candidate_summary",
            "fill_status": "COMPARISON_BOUND_REVIEW_CANDIDATE_NOT_PROMOTED",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_2_R10_alpha_lambda",
            "component_id": "COMP1471_r10_1_kernel",
            "quantity": "K_X, Qbar_source, Qbar_test, Z_X, lambda_X",
            "value_or_status": "MISSING_PARENT_R10_KERNEL_AND_CHARGE_NORMALIZATION",
            "units": "mixed; must map to dimensionless alpha(lambda)",
            "source_path": str(RETAINED_1056.relative_to(ROOT)),
            "source_anchor": "BAB1056_2_R10_product",
            "fill_status": "PREDICTION_KERNEL_MISSING",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_3_mass_clock",
            "component_id": "COMP1471_mass_0_matrix",
            "quantity": "alpha/mass/clock sensitivity matrix",
            "value_or_status": "matrix_only_no_single_MTS_prediction",
            "units": "mixed sensitivity units",
            "source_path": str(BOUND_MATRIX_1048.relative_to(ROOT)),
            "source_anchor": "BM1048_0_alpha_clock",
            "fill_status": "MATRIX_LINKED_SINGLE_PRODUCT_MISSING",
            "valid_for_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def prediction_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_0_alpha_clock",
            "arena": "clock_fine_structure",
            "observable_definition": "d ln R_YbE3E2/dt = DeltaK_alpha * P_clock_alpha; P_clock_alpha := b_alpha_EM * tau_clock_time",
            "prediction_side_value": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "prediction_side_status": "DEFINITION_AND_DELTAK_LINKED_B_ALPHA_TAU_MISSING",
            "prediction_units": "yr^-1",
            "source_definition_paths": "P8_Y5_R10_647_TAU_CLOCK_MAP.csv:TAU647_0_time_drift; P8_Y5_R10_1324_DIRECT_PRODUCT_EQUATION_ATTEMPT.csv:EQ1324_0_clock_observable",
            "comparison_bound_value": "2.1e-18",
            "comparison_units": "yr^-1",
            "comparison_source": "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv:BAP1051_2_best_current_product",
            "score_ready": False,
            "reason_not_score_ready": "b_alpha_EM and tau_clock_time are not parent-derived or directly predicted",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "observable_definition": "P_WEP_alpha := DeltaQ_alpha_AB * beta_source_alpha * b_alpha_EM * tau_WEP",
            "prediction_side_value": "MISSING_P_WEP_ALPHA",
            "prediction_side_status": "DELTAQ_SCHEMA_LINKED_BETA_SOURCE_B_ALPHA_TAU_MISSING",
            "prediction_units": "dimensionless",
            "source_definition_paths": "P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv:IN1102_3_delta_Q_alpha; P8_Y5_R10_1403_BETA_SOURCE_TAU_WEP_PRIOR.csv:BWP1403_0_definition; P8_Y5_R10_1407_SECTOR_BETA_SOURCE_SCHEMA.csv:SCHEMA1407_0..5",
            "comparison_bound_value": "4.797780522732e-05 alpha-only target; 2.887280314062e-05 robust surface-including target",
            "comparison_units": "dimensionless target_only",
            "comparison_source": "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv:BSB1414_1_alpha_only_target; BSB1414_2_robust_surface_target",
            "score_ready": False,
            "reason_not_score_ready": "source normalization, tau_WEP, and parent coefficient basis are missing; DeltaQ row is smoke-only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_2_R10_alpha_lambda",
            "arena": "R10_short_range",
            "observable_definition": "alpha_pred(lambda) := K_X(lambda) * Qbar_source(lambda) * Qbar_test(lambda) /(4*pi*Z_X*G_obs)",
            "prediction_side_value": "MISSING_ALPHA_LAMBDA_PREDICTION",
            "prediction_side_status": "BOUND_LINKED_KERNEL_CHARGE_LAMBDA_NORMALIZATION_MISSING",
            "prediction_units": "dimensionless alpha(lambda)",
            "source_definition_paths": "P8_Y5_R10_1056_RETAINED_B_ALPHA_BRANCH_LEDGER.csv:BAB1056_2_R10_product; P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv:ASR1099_4_R10_projection",
            "comparison_bound_value": "0.002344664300519378..897932.2928704522 review-candidate",
            "comparison_units": "dimensionless alpha(lambda) review_candidate",
            "comparison_source": "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv:R10B1034_3_vector_review_candidate_summary",
            "score_ready": False,
            "reason_not_score_ready": "lambda_X, K_X/Z_X, source/test charges, and official promoted curve remain missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1471_3_mass_clock",
            "arena": "mass_clock_constants",
            "observable_definition": "P_mass_clock_i := sensitivity_i dot b_parent * tau_clock, with coefficient basis and units still to be derived",
            "prediction_side_value": "MISSING_MASS_CLOCK_PRODUCT",
            "prediction_side_status": "MATRIX_LINKED_PARENT_BASIS_AND_SINGLE_PRODUCT_MISSING",
            "prediction_units": "mixed product units",
            "source_definition_paths": "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1048_0_alpha_clock; P8_Y5_R10_1324_DIRECT_PRODUCT_EQUATION_ATTEMPT.csv:EQ1324_2_factorized_product",
            "comparison_bound_value": "matrix_only_no_single_bound",
            "comparison_units": "mixed",
            "comparison_source": "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1048_0_alpha_clock",
            "score_ready": False,
            "reason_not_score_ready": "coefficient basis, sensitivity vector, tau map, and single observable row are incomplete",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def prediction_status_rows(prediction_fill: list[dict[str, Any]], components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "PSTAT1471_0_prediction_side_improved",
            "summary": "prediction-side rows now name the observable identity, source definition paths, available components, and missing parent inputs",
            "products": ";".join(row["product_id"] for row in prediction_fill),
            "component_rows": len(components),
            "numeric_prediction_rows": 0,
            "score_ready_rows": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "PSTAT1471_1_nonclaim_lock",
            "summary": "no live C_parent, radiative closure, or alpha product claim import is written",
            "products": "all APR1471 rows",
            "component_rows": len(components),
            "numeric_prediction_rows": 0,
            "score_ready_rows": 0,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1471_0_effective_threshold_leak",
            "countermodel": "bare visible action has no hidden alpha term, but heavy/light thresholds depend on hidden invariants and generate Z_EM^eff(I_hid)",
            "survives_why": "radiative endofunctor closure over the typed visible grammar is not parent-signed",
            "killed_by_1471": False,
            "needed_to_kill": "parent-signed effective action closure theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1471_1_clock_readout_leak",
            "countermodel": "alpha is clean in the action but clock readout includes hidden clock-state or apparatus coefficients",
            "survives_why": "clock readout naturality/kernel is not derived",
            "killed_by_1471": False,
            "needed_to_kill": "parent-signed clock readout functor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1471_2_WEP_R10_source_label_leak",
            "countermodel": "WEP or R10 source/test labels enter source charges before the quotient forgets material labels",
            "survives_why": "source-label forgetting and source/test charge construction remain unsigned",
            "killed_by_1471": False,
            "needed_to_kill": "source/material quotient theorem plus official readout/source kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1471_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1471_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1471_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1471_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1471_4_radiative", LIVE_RADIATIVE, "live parent-signed radiative/readout closure import"),
        ("LG1471_5_alpha_product", LIVE_ALPHA_PRODUCT, "live alpha residual product claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1471": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(
    radiative: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    prediction_fill: list[dict[str, Any]],
    components: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    exact_conditional = any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in radiative)
    refusal = any(row["result"] == "REFUSE_PROMOTION_START_PREDICTION_FILL" for row in radiative)
    definitions_linked = all(row["source_definition_paths"] and "MISSING" not in row["source_definition_paths"] for row in prediction_fill)
    component_ledger_written = len(components) >= 10
    readout_unsigned = all("UNSIGNED" in row["status"] or "MISSING" in row["status"] for row in readout)
    return [
        {
            "gate_id": "GATE1471_0_radiative_conditional_theorem",
            "gate": "radiative typed-domain preservation theorem is written conditionally",
            "gate_pass": exact_conditional,
            "claim_effect": "conditional math only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_1_parent_radiative_closure_signed",
            "gate": "parent effective/readout closure is signed",
            "gate_pass": False,
            "claim_effect": "alpha theorem-zero cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_2_readout_kernels_signed",
            "gate": "clock/WEP/R10 readout kernels are signed and source-backed",
            "gate_pass": False,
            "claim_effect": "observable prediction rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_3_readout_unsigned_recorded",
            "gate": "readout closure gaps are explicitly recorded",
            "gate_pass": readout_unsigned,
            "claim_effect": "prevents false observable closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_4_prediction_definitions_linked",
            "gate": "prediction-side rows link definition/source paths",
            "gate_pass": definitions_linked,
            "claim_effect": "source map only; not numeric evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_5_component_ledger_written",
            "gate": "component-level ledger separates available, smoke-only, and missing inputs",
            "gate_pass": component_ledger_written,
            "claim_effect": "makes next fill target concrete",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_6_refusal_recorded",
            "gate": "promotion refusal is recorded",
            "gate_pass": refusal,
            "claim_effect": "no hidden promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1471_7_score_ready_rows",
            "gate": "any alpha product row is score-ready",
            "gate_pass": False,
            "claim_effect": "no R10/WEP/clock claim",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1471_0_radiative_readout",
            "target": "radiative/readout closure and alpha product prediction rows",
            "radiative_conditional_theorem_written": True,
            "parent_radiative_closure_signed": False,
            "readout_kernels_signed": False,
            "prediction_definitions_linked": True,
            "numeric_predictions_available": False,
            "alpha_theorem_zero_promotion_allowed": False,
            "alpha_product_claim_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_RADIATIVE_READOUT_PROMOTION_FILL_PREDICTION_DEFINITIONS_NONCLAIM",
            "reason": "the exact theorem is conditional, but threshold/readout/source kernels are unsigned and numeric MTS prediction components are missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1471_0",
            "decision": "keep radiative typed-domain preservation as the clean theorem route",
            "why": "it would kill hidden alpha leakage without hand-setting b_alpha to zero",
            "consequence": "future derivation should target effective-action/readout functor closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1471_1",
            "decision": "refuse promotion",
            "why": "thresholds, clocks, WEP materials, and R10 source/test labels can still re-enter the observable coefficients",
            "consequence": "alpha clock/WEP/R10 products remain live constraints",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1471_2",
            "decision": "fill prediction-side definitions and component ledger",
            "why": "we can now see which missing inputs are mathematical parent gaps versus data/source gaps",
            "consequence": "next step can hunt numeric/source-ready components without confusing them for claims",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1471_0_1472",
            "next_target": "1472-Y5-R10-RAB-alpha-product-component-source-pack-or-coupling-debt-rollup.md",
            "script": "scripts/Y5_R10_RAB_alpha_product_component_source_pack_or_coupling_debt_rollup.py",
            "objective": "try to source/fill the missing alpha-product components one by one; if numeric fill remains blocked, roll the surviving coupling debt into the local-GR reduction ledger",
            "include": "b_alpha_EM owner/theorem-zero; tau_clock_time; beta_source_alpha; tau_WEP; R10 K_X/Z_X/Qbar/lambda_X; official-readout blockers; nonclaim gates",
            "exclude": "local-GR pass; WEP/R10 claim; alpha theorem-zero promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        RADIATIVE_CLOSURE,
        READOUT_CLOSURE,
        PREDICTION_COMPONENTS,
        PREDICTION_FILL,
        PREDICTION_STATUS,
        COUNTERMODELS,
        QUAR_PREDICTION_FILL,
        QUAR_COMPONENTS,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        return all(read_csv_rows(path) for path in paths)
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_PREDICTION_FILL.exists() and BRANCH_COMPONENTS.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    radiative: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    components: list[dict[str, Any]],
    prediction_fill: list[dict[str, Any]],
    prediction_status: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_conditional = any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in radiative)
    refusal = any(row["result"] == "REFUSE_PROMOTION_START_PREDICTION_FILL" for row in radiative)
    parent_unsigned = all(not truth(row["parent_signed"]) and not truth(row["claim_allowed"]) for row in radiative)
    readout_blocked = all(not truth(row["claim_allowed"]) and row["status"] != "SIGNED" for row in readout)
    component_sources_exist = all((ROOT / row["source_path"]).exists() for row in components)
    missing_components_retained = any("MISSING" in row["value_or_status"] for row in components)
    prediction_definitions_linked = all(row["source_definition_paths"] and "MISSING" not in row["source_definition_paths"] for row in prediction_fill)
    prediction_rows_nonclaim = all(
        "MISSING" in row["prediction_side_value"]
        and not truth(row["score_ready"])
        and not truth(row["valid_prediction_row"])
        and not truth(row["claim_allowed"])
        for row in prediction_fill
    )
    status_nonclaim = all(int(row["numeric_prediction_rows"]) == 0 and int(row["score_ready_rows"]) == 0 and not truth(row["claim_allowed"]) for row in prediction_status)
    countermodels_retained = all(not truth(row["killed_by_1471"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1471"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[3]["gate_pass"]) and truth(gates[4]["gate_pass"]) and truth(gates[5]["gate_pass"]) and truth(gates[6]["gate_pass"]) and not truth(gates[1]["gate_pass"]) and not truth(gates[2]["gate_pass"]) and not truth(gates[7]["gate_pass"])
    signing_refuses = all(
        truth(row["radiative_conditional_theorem_written"])
        and truth(row["prediction_definitions_linked"])
        and not truth(row["parent_radiative_closure_signed"])
        and not truth(row["readout_kernels_signed"])
        and not truth(row["numeric_predictions_available"])
        and not truth(row["alpha_theorem_zero_promotion_allowed"])
        and not truth(row["alpha_product_claim_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1471_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1471_1_exact_conditional", exact_conditional, "radiative typed-domain preservation theorem written conditionally"),
        ("VAL1471_2_refusal", refusal, "radiative/readout promotion refused"),
        ("VAL1471_3_parent_unsigned", parent_unsigned, "all radiative clauses remain parent-unsigned for claims"),
        ("VAL1471_4_readout_blocked", readout_blocked, "clock/WEP/R10/mass readout closures remain blocked/nonclaim"),
        ("VAL1471_5_component_sources", component_sources_exist, "all component source paths exist"),
        ("VAL1471_6_missing_components", missing_components_retained, "missing prediction components are retained explicitly"),
        ("VAL1471_7_prediction_definitions", prediction_definitions_linked, "prediction rows link definition/source paths"),
        ("VAL1471_8_prediction_rows_nonclaim", prediction_rows_nonclaim, "no prediction row is numeric or score-ready"),
        ("VAL1471_9_status_nonclaim", status_nonclaim, "prediction status keeps numeric and score-ready rows at zero"),
        ("VAL1471_10_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1471_11_live_paths", live_paths_untouched, "critical live official/source/material/Cparent/radiative/product files remain absent"),
        ("VAL1471_12_gate_pattern", safe_gate_pattern, "only conditional/refusal/definition gates pass; claim gates false"),
        ("VAL1471_13_signing_refuses", signing_refuses, "parent signing refuses alpha theorem-zero/product/local claims"),
        ("VAL1471_14_generated_csv_parse", generated_parse, "all generated 1471 CSVs parse cleanly"),
        ("VAL1471_15_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1471_16_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1471_17_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1471_18_overall", overall, "1471 refuses radiative/readout promotion and fills prediction definitions nonclaim"))
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    radiative: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    components: list[dict[str, Any]],
    prediction_fill: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1471 - Y5 R10 RAB Radiative Readout Closure Or Alpha Product Prediction Fill")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- Radiative typed-domain preservation is an exact conditional theorem: if the effective/readout functor preserves the visible action grammar, hidden alpha leakage vanishes.")
    lines.append("- The parent theory has not signed the threshold/readout/source-kernel clauses, so alpha theorem-zero, WEP, R10, clock, and local-GR claims are still refused.")
    lines.append("- Prediction-side rows are improved: they now carry observable definitions, source links, component ledgers, and explicit missing inputs without becoming score-ready.")
    lines.append("")
    lines.append("## Radiative Closure Attempt")
    lines.append("| attempt_id | result | missing_parent_signature |")
    lines.append("|---|---|---|")
    for row in radiative:
        lines.append(f"| {row['attempt_id']} | {row['result']} | {row['missing_parent_signature']} |")
    lines.append("")
    lines.append("## Readout Closure Audit")
    lines.append("| audit_id | arena | status | fallback |")
    lines.append("|---|---|---|---|")
    for row in readout:
        lines.append(f"| {row['audit_id']} | {row['arena']} | {row['status']} | {row['fallback']} |")
    lines.append("")
    lines.append("## Prediction Fill")
    lines.append("| product_id | prediction_side_status | comparison_bound_value | score_ready |")
    lines.append("|---|---|---|---:|")
    for row in prediction_fill:
        lines.append(f"| {row['product_id']} | {row['prediction_side_status']} | {row['comparison_bound_value']} | {row['score_ready']} |")
    lines.append("")
    lines.append("## Component Ledger")
    lines.append("| product_id | component_id | value_or_status | fill_status |")
    lines.append("|---|---|---|---|")
    for row in components:
        lines.append(f"| {row['product_id']} | {row['component_id']} | {row['value_or_status']} | {row['fill_status']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    radiative = radiative_closure_rows()
    readout = readout_closure_rows()
    components = prediction_component_rows()
    prediction_fill = prediction_fill_rows()
    prediction_status = prediction_status_rows(prediction_fill, components)
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(radiative, readout, prediction_fill, components)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(RADIATIVE_CLOSURE, radiative)
    write_csv(READOUT_CLOSURE, readout)
    write_csv(PREDICTION_COMPONENTS, components)
    write_csv(PREDICTION_FILL, prediction_fill)
    write_csv(PREDICTION_STATUS, prediction_status)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_PREDICTION_FILL, prediction_fill)
    write_csv(QUAR_COMPONENTS, components)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(PREDICTION_FILL, BRANCH_PREDICTION_FILL)
    copy_branch(PREDICTION_COMPONENTS, BRANCH_COMPONENTS)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, radiative, readout, components, prediction_fill, prediction_status, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, radiative, readout, components, prediction_fill, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1471_radiative_readout_refusal_alpha_prediction_fill_nonclaim")


if __name__ == "__main__":
    main()
