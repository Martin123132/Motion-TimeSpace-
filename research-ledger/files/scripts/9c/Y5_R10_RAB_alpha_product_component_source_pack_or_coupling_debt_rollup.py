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
QUARANTINE = MICROSCOPE / "quarantine" / "1472"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1472-Y5-R10-RAB-alpha-product-component-source-pack-or-coupling-debt-rollup.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1471_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1471_VALIDATION.csv"
PREV_COMPONENTS = OUT / "P8_Y5_R10_1471_ALPHA_PRODUCT_PREDICTION_COMPONENT_LEDGER.csv"
PREV_PREDICTION_FILL = OUT / "P8_Y5_R10_1471_ALPHA_PRODUCT_PREDICTION_FILL_NONCLAIM.csv"
PREV_READOUT = OUT / "P8_Y5_R10_1471_CLOCK_WEP_R10_READOUT_CLOSURE_AUDIT.csv"

UEM_1099 = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
OBS_1114 = OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv"
BETA_QCD_1410 = OUT / "P8_Y5_R10_1410_BETA_EM_QCD_OWNER_AUDIT.csv"
BETA_OWNER_1414 = OUT / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv"
COUPLING_HUNT_1430 = OUT / "P8_Y5_R10_1430_COUPLING_SOURCE_HUNT.csv"
CPARENT_CONTRACT_1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_CONTRACT.csv"
CPARENT_AUDIT_1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_AUDIT.csv"
PARENT_CANDIDATES_1446 = OUT / "P8_Y5_R10_1446_PARENT_ACTION_COUPLING_CANDIDATE_LEDGER.csv"

TAU_CLOCK_647 = OUT / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv"
TAU_AUDIT_1053 = OUT / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv"
TAU_SOURCE_1069 = OUT / "P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv"
TAU_STATUS_1072 = OUT / "P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv"
TAU_READOUT_1322 = OUT / "P8_Y5_R10_1322_TAU_READOUT_DERIVATION_ATTEMPT.csv"
COFRAME_TAU_1361 = OUT / "P8_Y5_R10_1361_COFRAME_TAU_LOCK_ATTEMPT.csv"
SHARED_TAU_1402 = OUT / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv"

R10_INPUT_1034 = OUT / "P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv"
R10_BOUND_1034 = OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv"
KERNEL_1035 = OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv"
KX_ROWS_1035 = OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv"
QBAR_1044 = OUT / "P8_Y5_R10_1044_QBARXT_BOUND_FALLBACK_ROWS.csv"
QBAR_MARKER_1046 = OUT / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
CLOCK_PROJ_1047 = OUT / "P8_Y5_R10_1047_CLOCK_CONSTANT_PROJECTION_ROWS.csv"
BOUND_MATRIX_1048 = OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"

FINITE_630 = OUT / "P8_Y5_R10_630_FINITE_COUPLING_DERIVATION.csv"
MATTER_COUPLING_716 = OUT / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv"
OWNER_GATES_1076 = OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
DEBT_1219 = OUT / "P8_Y5_R10_1219_FINITE_COUPLING_CLOSURE_DEBT_ROWS.csv"
LOCAL_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
LOCAL_GATE_1230 = OUT / "P8_Y5_R10_1230_LOCAL_GR_SOURCE_COUPLING_GATE_UPDATE.csv"
LOCAL_ACTION_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
LOCAL_FIXED_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"
LOCAL_VECTOR = OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv"
NEWTON_SPINE_956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
NEWTON_LHS_956 = OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv"
NEWTON_LADDER_990 = OUT / "P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv"
NEWTON_BLOCKERS_1339 = OUT / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv"
PPN_GATE_1339 = OUT / "P8_Y5_R10_1339_PPN_COMPLETION_GATE.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_ALPHA_PRODUCT = COEFF / "alpha_residual_product_claim_rows.csv"
LIVE_COMPONENT_SOURCE_PACK = COEFF / "alpha_product_component_source_pack_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1472_SOURCE_REGISTER.csv"
SOURCE_PACK = OUT / "P8_Y5_R10_1472_ALPHA_PRODUCT_COMPONENT_SOURCE_PACK.csv"
NUMERIC_ATTEMPT = OUT / "P8_Y5_R10_1472_ALPHA_PRODUCT_NUMERIC_FILL_ATTEMPT.csv"
ACTION_CONTRACT = OUT / "P8_Y5_R10_1472_PARENT_ACTION_COUPLING_CONTRACT_ATTEMPT.csv"
COUPLING_DEBT = OUT / "P8_Y5_R10_1472_COUPLING_DEBT_ROLLUP.csv"
LOCAL_FEED = OUT / "P8_Y5_R10_1472_LOCAL_GR_FEED_LEDGER.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1472_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1472_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1472_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1472_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1472_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1472_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1472_VALIDATION.csv"

QUAR_SOURCE_PACK = QUARANTINE / "ALPHA_PRODUCT_COMPONENT_SOURCE_PACK.csv"
QUAR_COUPLING_DEBT = QUARANTINE / "COUPLING_DEBT_ROLLUP.csv"
BRANCH_SOURCE_PACK = COEFF / "alpha_product_component_source_pack_nonclaim_1472.csv"
BRANCH_COUPLING_DEBT = COEFF / "coupling_debt_rollup_nonclaim_1472.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_component_source_pack_signing_decision_1472.csv"


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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1472_0_1471_next", PREV_NEXT, "1471 handoff to component source pack or coupling debt rollup"),
        ("SRC1472_1_1471_validation", PREV_VALIDATION, "1471 validation baseline"),
        ("SRC1472_2_1471_components", PREV_COMPONENTS, "1471 component ledger"),
        ("SRC1472_3_1471_prediction", PREV_PREDICTION_FILL, "1471 prediction-side nonclaim fill"),
        ("SRC1472_4_1471_readout", PREV_READOUT, "1471 readout closure audit"),
        ("SRC1472_5_UEM", UEM_1099, "EM kinetic owner theorem attempt"),
        ("SRC1472_6_obstruction", OBS_1114, "coupling obstruction ledger"),
        ("SRC1472_7_beta_qcd", BETA_QCD_1410, "beta EM/QCD owner audit"),
        ("SRC1472_8_beta_source_owner", BETA_OWNER_1414, "beta_source_alpha owner attempt"),
        ("SRC1472_9_coupling_hunt", COUPLING_HUNT_1430, "coupling source hunt"),
        ("SRC1472_10_Cparent_contract", CPARENT_CONTRACT_1445, "C_parent coupling contract"),
        ("SRC1472_11_Cparent_audit", CPARENT_AUDIT_1445, "C_parent coupling audit"),
        ("SRC1472_12_parent_candidates", PARENT_CANDIDATES_1446, "parent action coupling candidate ledger"),
        ("SRC1472_13_tau_clock", TAU_CLOCK_647, "tau clock definitions"),
        ("SRC1472_14_tau_audit", TAU_AUDIT_1053, "tau WEP/R10 projection audit"),
        ("SRC1472_15_tau_source", TAU_SOURCE_1069, "first real tau source row"),
        ("SRC1472_16_tau_status", TAU_STATUS_1072, "numeric tau status"),
        ("SRC1472_17_tau_readout", TAU_READOUT_1322, "tau readout derivation attempt"),
        ("SRC1472_18_coframe_tau", COFRAME_TAU_1361, "coframe tau lock attempt"),
        ("SRC1472_19_shared_tau", SHARED_TAU_1402, "shared tau transfer theorem audit"),
        ("SRC1472_20_R10_input", R10_INPUT_1034, "R10 projection input pack"),
        ("SRC1472_21_R10_bound", R10_BOUND_1034, "R10 alpha bound candidates"),
        ("SRC1472_22_kernel", KERNEL_1035, "K_X kernel derivation audit"),
        ("SRC1472_23_KX", KX_ROWS_1035, "K_X factorization rows"),
        ("SRC1472_24_qbar", QBAR_1044, "qbar fallback rows"),
        ("SRC1472_25_qbar_marker", QBAR_MARKER_1046, "qbar marker coefficients"),
        ("SRC1472_26_clock_proj", CLOCK_PROJ_1047, "clock projection rows"),
        ("SRC1472_27_bound_matrix", BOUND_MATRIX_1048, "alpha/mass/clock bound matrix"),
        ("SRC1472_28_finite_coupling", FINITE_630, "finite coupling derivation"),
        ("SRC1472_29_matter_coupling", MATTER_COUPLING_716, "matter coupling derivation"),
        ("SRC1472_30_owner_gates", OWNER_GATES_1076, "coupling owner gates"),
        ("SRC1472_31_wep_owner", WEP_OWNER_1077, "parent WEP coupling owner theorem attempt"),
        ("SRC1472_32_debt", DEBT_1219, "finite coupling closure debt rows"),
        ("SRC1472_33_local_coupling", LOCAL_COUPLING_1229, "local GR source coupling theorem contract"),
        ("SRC1472_34_local_gate", LOCAL_GATE_1230, "local GR source coupling gate update"),
        ("SRC1472_35_local_action", LOCAL_ACTION_511, "minimum parent local-GR action blocks"),
        ("SRC1472_36_local_fixed", LOCAL_FIXED_511, "minimum parent local-GR fixed point conditions"),
        ("SRC1472_37_local_vector", LOCAL_VECTOR, "local-GR residual vector"),
        ("SRC1472_38_newton_spine", NEWTON_SPINE_956, "source-side GR/Newton spine"),
        ("SRC1472_39_newton_lhs", NEWTON_LHS_956, "left-hand EH/Newton gate map"),
        ("SRC1472_40_newton_ladder", NEWTON_LADDER_990, "GR/Newton reentry ladder"),
        ("SRC1472_41_newton_blockers", NEWTON_BLOCKERS_1339, "Newton transfer blockers"),
        ("SRC1472_42_ppn_gate", PPN_GATE_1339, "PPN completion gate"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_0_DeltaK_clock",
            "product_id": "APR1471_0_alpha_clock",
            "quantity": "DeltaK_alpha(YbE3/YbE2)",
            "value_or_status": "-6.95",
            "units": "dimensionless sensitivity",
            "source_path": rel(CLOCK_PROJ_1047),
            "source_anchor": "CLK1047_1_CAS646_1_YbE3E2",
            "fill_class": "NUMERIC_SOURCE_BACKED_COMPONENT",
            "remaining_gap": "not an MTS prediction without b_alpha_EM and tau_clock_time",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_1_b_alpha_EM",
            "product_id": "APR1471_0_alpha_clock;APR1471_1_WEP_alpha;APR1471_2_R10_alpha_lambda",
            "quantity": "b_alpha_EM",
            "value_or_status": "MISSING_PARENT_ALPHA_OWNER_OR_SIGNED_THEOREM_ZERO",
            "units": "dimensionless vertical derivative",
            "source_path": rel(UEM_1099),
            "source_anchor": "UEM1099_3_verdict",
            "fill_class": "THEOREM_ZERO_CANDIDATE_UNSIGNED",
            "remaining_gap": "EM kinetic owner plus no-hidden coefficient plus radiative/readout closure",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_2_tau_clock_time",
            "product_id": "APR1471_0_alpha_clock",
            "quantity": "tau_clock_time",
            "value_or_status": "MISSING_PARENT_TAU_CLOCK_XHAT_MAP",
            "units": "yr^-1 per normalized Xhat unit",
            "source_path": rel(TAU_READOUT_1322),
            "source_anchor": "TAU1322_0_product_definition;TAU1322_5_time_profile",
            "fill_class": "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED",
            "remaining_gap": "chi_X parent status and local lab time profile",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_3_DeltaQ_WEP",
            "product_id": "APR1471_1_WEP_alpha",
            "quantity": "DeltaQ_alpha_AB",
            "value_or_status": "1.989808886825000e-03",
            "units": "dimensionless smoke material contrast",
            "source_path": rel(PREV_COMPONENTS),
            "source_anchor": "COMP1471_wep_0_deltaQ",
            "fill_class": "SMOKE_COMPONENT_AVAILABLE_NOT_OFFICIAL",
            "remaining_gap": "official material/readout tensor and parent basis",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_4_beta_source_alpha",
            "product_id": "APR1471_1_WEP_alpha",
            "quantity": "beta_source_alpha",
            "value_or_status": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER",
            "units": "dimensionless source coefficient",
            "source_path": rel(BETA_OWNER_1414),
            "source_anchor": "BSA1414_5_verdict",
            "fill_class": "OWNER_NOT_DERIVED_FINITE_TARGET_ROW_REQUIRED",
            "remaining_gap": "T_Q/current owner, official readout kernel, no current rescaling theorem",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_5_tau_WEP",
            "product_id": "APR1471_1_WEP_alpha",
            "quantity": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless projection factor",
            "source_path": rel(TAU_STATUS_1072),
            "source_anchor": "NTS1072_2_tau_WEP",
            "fill_class": "DATA_ANCHOR_EXISTS_NUMERIC_TAU_NOT_ACQUIRED",
            "remaining_gap": "CMSM arrays or official reconstruction of orbit/attitude/gravity kernels",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_6_shared_tau_domain",
            "product_id": "APR1471_0_alpha_clock;APR1471_1_WEP_alpha;APR1471_2_R10_alpha_lambda",
            "quantity": "shared D_parent/local tau map",
            "value_or_status": "Z_shared_tau_domain=false",
            "units": "theorem gate",
            "source_path": rel(SHARED_TAU_1402),
            "source_anchor": "DTT1402_7_current_verdict",
            "fill_class": "TRANSFER_THEOREM_CONDITIONAL_ONLY",
            "remaining_gap": "parent domain map proving no private clock/WEP/R10 screens",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_7_alpha_bound_R10",
            "product_id": "APR1471_2_R10_alpha_lambda",
            "quantity": "alpha_bound(lambda)",
            "value_or_status": "review_candidate_curve_present_nonclaim",
            "units": "dimensionless alpha(lambda)",
            "source_path": rel(R10_BOUND_1034),
            "source_anchor": "R10B1034_3_vector_review_candidate_summary",
            "fill_class": "COMPARISON_BOUND_REVIEW_CANDIDATE",
            "remaining_gap": "official curve/table promotion and matching convention",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_8_KX_lambda",
            "product_id": "APR1471_2_R10_alpha_lambda",
            "quantity": "K_X(lambda)",
            "value_or_status": "MISSING_KERNEL_NORMALIZATION",
            "units": "dimensionless alpha-normalized factor",
            "source_path": rel(KX_ROWS_1035),
            "source_anchor": "KXF1035_4_total",
            "fill_class": "SYMBOLIC_SHAPE_CONTRACT_NUMERIC_MISSING",
            "remaining_gap": "Z_X, charge-unit convention, source/test support, and R10 harmonic projection",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_9_Qbar_source_test",
            "product_id": "APR1471_2_R10_alpha_lambda",
            "quantity": "Qbar_source, Qbar_test, qbar_marker",
            "value_or_status": "MISSING_SOURCE_CHARGE_AND_MARKER_ZERO",
            "units": "dimensionless_or_declared",
            "source_path": rel(QBAR_MARKER_1046),
            "source_anchor": "QMC1046_3_qbar_marker_abs",
            "fill_class": "MARKER_ENVELOPE_REQUIRED",
            "remaining_gap": "all marker/frame coefficients theorem-zero or numeric source-backed",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_10_lambda_ZX",
            "product_id": "APR1471_2_R10_alpha_lambda",
            "quantity": "lambda_X and Z_X",
            "value_or_status": "MISSING_PARENT_RANGE_AND_KINETIC_NORMALIZATION",
            "units": "m and parent-declared kinetic units",
            "source_path": rel(R10_INPUT_1034),
            "source_anchor": "R10P1034_1_KX_lambda;R10P1034_4_cg;R10P1034_6_alpha_predicted",
            "fill_class": "PARENT_OPERATOR_MISSING",
            "remaining_gap": "finite mode quadratic operator must be parent-signed and normalized",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "CSP1472_11_mass_clock_matrix",
            "product_id": "APR1471_3_mass_clock",
            "quantity": "alpha/mass/clock sensitivity matrix",
            "value_or_status": "matrix_only_no_single_MTS_prediction",
            "units": "mixed sensitivity units",
            "source_path": rel(BOUND_MATRIX_1048),
            "source_anchor": "BM1048_0_alpha_clock",
            "fill_class": "MATRIX_LINKED_SINGLE_PRODUCT_MISSING",
            "remaining_gap": "parent coefficient basis, units, sign convention, and single observable row",
            "usable_for_numeric_prediction": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def numeric_attempt_rows(source_pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "NUM1472_0_clock",
            "product_id": "APR1471_0_alpha_clock",
            "formula": "P_clock_alpha = b_alpha_EM * tau_clock_time",
            "available_numeric_components": "DeltaK_alpha=-6.95; comparison product bound=2.1e-18 yr^-1",
            "missing_components": "b_alpha_EM; tau_clock_time; direct P_clock_alpha",
            "numeric_prediction": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "score_ready": False,
            "reason": "available clock sensitivity/bound is not an MTS prediction",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "NUM1472_1_WEP",
            "product_id": "APR1471_1_WEP_alpha",
            "formula": "P_WEP_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha_EM * tau_WEP",
            "available_numeric_components": "DeltaQ_alpha_AB smoke=1.989808886825000e-03; target bounds exist",
            "missing_components": "beta_source_alpha; b_alpha_EM; tau_WEP; official material/source/readout kernel",
            "numeric_prediction": "MISSING_P_WEP_ALPHA",
            "score_ready": False,
            "reason": "only a smoke DeltaQ and target bound exist; no parent product",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "NUM1472_2_R10",
            "product_id": "APR1471_2_R10_alpha_lambda",
            "formula": "alpha_pred(lambda) = K_X(lambda) * Qbar_source(lambda) * Qbar_test(lambda)/(4*pi*Z_X*G_obs)",
            "available_numeric_components": "review-candidate alpha_bound(lambda) only",
            "missing_components": "K_X(lambda); Qbar_source; Qbar_test; Z_X; lambda_X; official curve promotion",
            "numeric_prediction": "MISSING_ALPHA_LAMBDA_PREDICTION",
            "score_ready": False,
            "reason": "comparison curve and symbolic kernel do not determine a parent alpha prediction",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "NUM1472_3_mass_clock",
            "product_id": "APR1471_3_mass_clock",
            "formula": "P_mass_clock_i = sensitivity_i dot b_parent * tau_clock",
            "available_numeric_components": "matrix source link only",
            "missing_components": "parent b vector; tau map; units; sign convention; single observable row",
            "numeric_prediction": "MISSING_MASS_CLOCK_PRODUCT",
            "score_ready": False,
            "reason": "matrix link is not a scalar prediction",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PAC1472_0_parent_action_slot",
            "contract": "S_parent must declare every coupling slot before empirical scoring: S_EH[g_obs] + S_top[kappa] + S_extra[Phi] + S_matter[psi,g_obs,theta] + S_readout.",
            "mathematical_test": "No coefficient entering clocks, WEP, R10, Newton, or PPN may be introduced after the parent variation as a source/readout label.",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "source_path": rel(CPARENT_CONTRACT_1445),
            "source_anchor": "CTC1445_0_parent_action;CTC1445_4_no_bound_inversion",
            "blocks_if_open": "all alpha-product rows and source-side local-GR transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PAC1472_1_double_zero",
            "contract": "Every non-EH coupling that can affect observed local matter or metric readout has C_i(Phi0)=0 and partial_A C_i(Phi0)=0 at the compact local fixed point.",
            "mathematical_test": "F_1=0 for alpha_EM, source weights, matter-frame coefficients, Pi_M, metric readout, and finite-range charges.",
            "current_status": "LOCAL_GR_REQUIREMENT_KNOWN_NOT_DERIVED",
            "source_path": rel(LOCAL_FIXED_511),
            "source_anchor": "FP511_1_double_zero_nonEH_coupling;FP511_4_universal_observed_coframe;FP511_7_metric_PPN_readout",
            "blocks_if_open": "WEP/R10/clock silence and PPN/local-GR promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PAC1472_2_universal_source_coupling",
            "contract": "ordinary matter descends through one source/current owner, so species/source multipliers are either one common factor or projected null modes.",
            "mathematical_test": "delta S_matter/delta g_obs gives T_total with no independent w_A, beta_source_A, or source-only current rescaling.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": rel(LOCAL_COUPLING_1229),
            "source_anchor": "THM1229_1_iff;THM1229_3_residual_vector",
            "blocks_if_open": "Newton source side, WEP beta_source_alpha, and R10 source/test charge normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PAC1472_3_same_readout_frame",
            "contract": "clock, photon, orbital, boundary, and source readouts use one observed coframe/metric through the tested order.",
            "mathematical_test": "e_source=e_clock=e_photon=e_orbit=e_boundary=e_obs and first readout variations vanish or enter retained residual rows.",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_DERIVED",
            "source_path": rel(COFRAME_TAU_1361),
            "source_anchor": "CTL1361_0_one_observed_coframe;CTL1361_5_tau_clock_orbit_boundary_lock",
            "blocks_if_open": "clock-WEP-R10 transfer and measured-GM/PPN readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "PAC1472_4_positive_operator_or_zero_mode_absence",
            "contract": "finite local modes have a parent-owned positive operator, range, and normalization, or are absent by theorem.",
            "mathematical_test": "S_X^(2) fixes Z_X>0, lambda_X, boundary conditions, and source charges before alpha(lambda) scoring.",
            "current_status": "SYMBOLIC_CONTRACT_NUMERIC_PARENT_OPERATOR_MISSING",
            "source_path": rel(KERNEL_1035),
            "source_anchor": "KXD1035_0_parent_quadratic_operator;KXD1035_5_verdict",
            "blocks_if_open": "R10 alpha(lambda), finite-range Newton deviations, and local extra hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def coupling_debt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_0_alpha_owner",
            "debt": "alpha_EM / F_Q^2 owner and hidden-coefficient theorem-zero",
            "current_status": "THEOREM_TARGET_UNSIGNED",
            "source_path": rel(UEM_1099),
            "source_anchor": "UEM1099_3_verdict;OBS1114_3_radiative",
            "needed_to_close": "EM kinetic owner, typed no-hidden coefficient grammar, and radiative/readout closure",
            "blocks_clock": True,
            "blocks_WEP": True,
            "blocks_R10": True,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive parent-signed EM owner plus effective/readout closure or retain b_alpha products",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_1_source_current_owner",
            "debt": "single ordinary-matter source/current owner",
            "current_status": "CONDITIONAL_ONLY",
            "source_path": rel(WEP_OWNER_1077),
            "source_anchor": "WCO1077_5_verdict;OWN1076_2_current_owner",
            "needed_to_close": "species-blind measure/current/source normalization and no source-only scalars",
            "blocks_clock": False,
            "blocks_WEP": True,
            "blocks_R10": True,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "prove connected ordinary matter category/source-label forgetting or retain finite source residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_2_tau_domain_map",
            "debt": "shared local tau/domain map across clocks, WEP, R10, and PPN",
            "current_status": "TRANSFER_BLOCKED",
            "source_path": rel(SHARED_TAU_1402),
            "source_anchor": "DTT1402_7_current_verdict",
            "needed_to_close": "parent local domain map with no arena-specific screens",
            "blocks_clock": True,
            "blocks_WEP": True,
            "blocks_R10": True,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive D_parent fixed-point/readout map or keep arena-specific products separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_3_R10_operator",
            "debt": "finite-mode operator, range, charges, and R10 harmonic projection",
            "current_status": "SYMBOLIC_ONLY_NUMERIC_MISSING",
            "source_path": rel(KX_ROWS_1035),
            "source_anchor": "KXF1035_4_total;R10P1034_6_alpha_predicted",
            "needed_to_close": "Z_X, lambda_X, K_X, Qbar_source/test, official bound-curve convention",
            "blocks_clock": False,
            "blocks_WEP": True,
            "blocks_R10": True,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "fill parent quadratic operator/source charges or demote R10 branch to bound-input only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_4_EH_Newton_PPN_left_side",
            "debt": "EH operator, measured-GM calibration, and PPN weak-field completion",
            "current_status": "NOT_REACHED",
            "source_path": rel(NEWTON_LADDER_990),
            "source_anchor": "LAD990_1_operator;LAD990_3_Newton;LAD990_4_PPN",
            "needed_to_close": "EH-only operator theorem, Hamiltonian/Pi_M source charge, measured-GM calibration, and PPN residual vector",
            "blocks_clock": False,
            "blocks_WEP": False,
            "blocks_R10": True,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "feed coupling debts into local residual vector rather than claiming Newton/GR transfer",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "debt_id": "DEBT1472_5_official_empirical_readout",
            "debt": "official readout/source data for empirical scoring",
            "current_status": "DATA_ACQUISITION_STILL_PARTIAL",
            "source_path": rel(TAU_STATUS_1072),
            "source_anchor": "NTS1072_0_schema_inventory;NTS1072_2_tau_WEP",
            "needed_to_close": "official MICROSCOPE CMSM arrays, source worldtube/readout kernels, and promoted R10 bound curve/table",
            "blocks_clock": False,
            "blocks_WEP": True,
            "blocks_R10": True,
            "blocks_Newton": False,
            "blocks_PPN": False,
            "blocks_local_GR": False,
            "next_action": "acquire data after parent-component definitions are stable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_feed_rows(debt_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "feed_id": "LGF1472_0_to_min_parent_action",
            "target_artifact": rel(LOCAL_ACTION_511),
            "feed_statement": "alpha/WEP/R10 coupling debt collapses onto the minimum local-GR parent action blocks A511_2, A511_3, A511_6.",
            "affected_rows": "A511_2_universal_matter;A511_3_extra_field_silence;A511_6_metric_readout",
            "promotion_effect": "none; local GR remains blocked",
            "next_action": "turn coupling debt into double-zero/action-block proof obligations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "feed_id": "LGF1472_1_to_fixed_point",
            "target_artifact": rel(LOCAL_FIXED_511),
            "feed_statement": "the missing components are exactly first-variation leaks at the local fixed point unless theorem-zero or positive operator clauses close.",
            "affected_rows": "FP511_1_double_zero_nonEH_coupling;FP511_4_universal_observed_coframe;FP511_8_local_cosmology_transition_control",
            "promotion_effect": "none; fixed point conditions remain requirements",
            "next_action": "derive C_i(Phi0)=0 and partial_A C_i(Phi0)=0 for alpha/source/readout slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "feed_id": "LGF1472_2_to_Newton_spine",
            "target_artifact": rel(NEWTON_SPINE_956),
            "feed_statement": "source-current owner debt is the same thing as the right-hand-side Newton source closure debt.",
            "affected_rows": "SSG956_1_no_species_source_functor;SSG956_2_total_Hilbert_source;SSG956_5_source_side_verdict",
            "promotion_effect": "none; Newton transfer still fails without measured-GM and EH-left-side closure",
            "next_action": "prove source functor has no species/source label argument or retain q_source residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "feed_id": "LGF1472_3_to_residual_vector",
            "target_artifact": rel(LOCAL_VECTOR),
            "feed_statement": "failed component fills must remain executable residual rows, not verbal closure assumptions.",
            "affected_rows": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION;LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_BOUNDARY_R7_ALPHA3",
            "promotion_effect": "none; PPN/local-GR branch remains nonclaim",
            "next_action": "append or update executable residual rows only after parent coefficients are numeric or theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1472_0_species_weight",
            "countermodel": "S_matter=sum_A(1+epsilon_A)S_A leaves classical species equations plausible but changes Hilbert source and WEP/source charge.",
            "survives_why": "source-label forgetting and single current owner remain unsigned",
            "killed_by_1472": False,
            "needed_to_kill": "universal source coupling theorem from parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1472_1_hidden_F2",
            "countermodel": "DeltaS=-1/4 integral f_X(Xhat)F_Q^2 regenerates b_alpha_EM even if the visible Maxwell block is clean.",
            "survives_why": "typed/no-hidden and radiative/readout closure are not parent-signed",
            "killed_by_1472": False,
            "needed_to_kill": "parent-signed EM kinetic owner and effective-action closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1472_2_arena_private_screen",
            "countermodel": "clock, WEP, and R10 each use a private tau/screen so a clock product bound cannot transfer to WEP/R10/local PPN.",
            "survives_why": "shared D_parent/tau theorem is conditional only",
            "killed_by_1472": False,
            "needed_to_kill": "parent domain map and same-readout-frame theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1472_3_EH_looking_not_Newton",
            "countermodel": "a field equation can look Poisson-like but the measured orbital GM is shifted by Pi_M, boundary, or finite-range source normalization.",
            "survives_why": "measured-GM calibration, Pi_M lock, and finite-mode operator remain open",
            "killed_by_1472": False,
            "needed_to_kill": "Hamiltonian/Gauss calibration and PPN residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1472_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1472_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1472_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1472_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1472_4_alpha_product", LIVE_ALPHA_PRODUCT, "live alpha residual product claim rows"),
        ("LG1472_5_component_source_pack", LIVE_COMPONENT_SOURCE_PACK, "live component source pack claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": rel(path),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1472": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def gate_rows(
    source_pack: list[dict[str, Any]],
    numeric_attempt: list[dict[str, Any]],
    action_contract: list[dict[str, Any]],
    debt_rows: list[dict[str, Any]],
    local_feed: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pack_written = len(source_pack) >= 12
    missing_retained = any("MISSING" in row["value_or_status"] for row in source_pack)
    no_numeric = all(not truth(row["score_ready"]) and not truth(row["valid_prediction_row"]) for row in numeric_attempt)
    contract_written = len(action_contract) >= 5
    debt_blocks_local = any(truth(row["blocks_local_GR"]) for row in debt_rows)
    local_feed_written = len(local_feed) >= 4
    return [
        {
            "gate_id": "GATE1472_0_component_source_pack_written",
            "gate": "component source pack written with source paths and anchors",
            "gate_pass": pack_written,
            "claim_effect": "inventory only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_1_missing_components_retained",
            "gate": "missing parent components remain explicit",
            "gate_pass": missing_retained,
            "claim_effect": "prevents false numeric fill",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_2_numeric_predictions_score_ready",
            "gate": "any alpha product numeric prediction is score-ready",
            "gate_pass": False,
            "claim_effect": "no clock/WEP/R10 score claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_3_numeric_refusal",
            "gate": "numeric fill refusal is recorded for every product",
            "gate_pass": no_numeric,
            "claim_effect": "nonclaim lock",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_4_parent_action_contract_written",
            "gate": "parent action coupling contract attempt written",
            "gate_pass": contract_written,
            "claim_effect": "theorem target only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_5_parent_action_contract_signed",
            "gate": "parent action coupling contract is signed",
            "gate_pass": False,
            "claim_effect": "local-GR transfer remains blocked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_6_coupling_debt_rollup_written",
            "gate": "coupling debts are rolled into local-GR/Newton/PPN blockers",
            "gate_pass": debt_blocks_local and local_feed_written,
            "claim_effect": "routing improvement only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1472_7_local_GR_claim",
            "gate": "local GR/Newton/PPN promotion allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1472",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1472_0_component_source_pack",
            "target": "alpha-product component source pack and coupling debt rollup",
            "component_source_pack_written": True,
            "numeric_predictions_available": False,
            "parent_action_contract_signed": False,
            "coupling_debt_rolled_to_local_GR": True,
            "alpha_product_claim_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "component_claim_import_allowed": False,
            "Newton_transfer_allowed": False,
            "PPN_claim_allowed": False,
            "local_GR_claim_allowed": False,
            "decision": "REFUSE_NUMERIC_ALPHA_PRODUCT_PROMOTION_ROLL_COUPLING_DEBT_TO_LOCAL_GR",
            "reason": "component sources are sharper, but b_alpha, tau, source normalization, R10 kernel, and parent action contracts are still unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1472_0",
            "decision": "source pack is useful but not score-ready",
            "why": "some comparison/sensitivity components are sourced, but every product still lacks at least one parent-owned factor",
            "consequence": "keep alpha products nonclaim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1472_1",
            "decision": "coupling is the shared bottleneck",
            "why": "the same missing current/readout/tau/finite-operator clauses block WEP, R10, clocks, Newton, PPN, and local GR",
            "consequence": "attack parent action contracts instead of arena-specific shortcuts",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1472_2",
            "decision": "roll debt into local-GR route",
            "why": "the final theory needs GR/Newton derivability, so source/alpha couplings must become fixed-point double-zero or residual-vector entries",
            "consequence": "next target should attempt the parent coupling double-zero theorem or append executable residual rows",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1472_0_1473",
            "next_target": "1473-Y5-R10-RAB-parent-coupling-double-zero-theorem-or-executable-residual-vector.md",
            "script": "scripts/Y5_R10_RAB_parent_coupling_double_zero_theorem_or_executable_residual_vector.py",
            "objective": "try to derive the parent fixed-point double-zero law for alpha/source/readout couplings; if it fails, emit executable residual-vector rows for local GR/Newton/PPN instead of claim prose",
            "include": "C_i(Phi0)=0; partial_A C_i(Phi0)=0; universal matter source current; same-readout frame; finite-mode operator; PPN residual hooks",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        SOURCE_PACK,
        NUMERIC_ATTEMPT,
        ACTION_CONTRACT,
        COUPLING_DEBT,
        LOCAL_FEED,
        COUNTERMODELS,
        QUAR_SOURCE_PACK,
        QUAR_COUPLING_DEBT,
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
    return BRANCH_SOURCE_PACK.exists() and BRANCH_COUPLING_DEBT.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    source_pack: list[dict[str, Any]],
    numeric_attempt: list[dict[str, Any]],
    action_contract: list[dict[str, Any]],
    debt_rows: list[dict[str, Any]],
    local_feed: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    pack_sources_exist = all((ROOT / row["source_path"]).exists() for row in source_pack)
    pack_has_source_anchors = all(row["source_anchor"] and "MISSING" not in row["source_anchor"] for row in source_pack)
    missing_retained = any("MISSING" in row["value_or_status"] or "false" in str(row["value_or_status"]).lower() for row in source_pack)
    no_numeric_claims = all(
        "MISSING" in row["numeric_prediction"]
        and not truth(row["score_ready"])
        and not truth(row["valid_prediction_row"])
        and not truth(row["claim_allowed"])
        for row in numeric_attempt
    )
    action_unsigned = all(not truth(row["claim_allowed"]) and row["current_status"] != "SIGNED" for row in action_contract)
    debt_sources_exist = all((ROOT / row["source_path"]).exists() for row in debt_rows)
    debt_blocks_core = any(truth(row["blocks_Newton"]) for row in debt_rows) and any(truth(row["blocks_PPN"]) for row in debt_rows) and any(truth(row["blocks_local_GR"]) for row in debt_rows)
    local_feed_nonclaim = all(not truth(row["claim_allowed"]) and row["promotion_effect"].startswith("none") for row in local_feed)
    countermodels_retained = all(not truth(row["killed_by_1472"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1472"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and not truth(gates[2]["gate_pass"]) and truth(gates[3]["gate_pass"]) and truth(gates[4]["gate_pass"]) and not truth(gates[5]["gate_pass"]) and truth(gates[6]["gate_pass"]) and not truth(gates[7]["gate_pass"])
    signing_refuses = all(
        truth(row["component_source_pack_written"])
        and truth(row["coupling_debt_rolled_to_local_GR"])
        and not truth(row["numeric_predictions_available"])
        and not truth(row["parent_action_contract_signed"])
        and not truth(row["alpha_product_claim_allowed"])
        and not truth(row["Newton_transfer_allowed"])
        and not truth(row["PPN_claim_allowed"])
        and not truth(row["local_GR_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1472_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1472_1_pack_sources", pack_sources_exist, "all component source-pack paths exist"),
        ("VAL1472_2_pack_anchors", pack_has_source_anchors, "all component rows have nonmissing anchors"),
        ("VAL1472_3_missing_retained", missing_retained, "missing components remain explicit"),
        ("VAL1472_4_no_numeric_claims", no_numeric_claims, "numeric fill attempts remain nonclaim and missing"),
        ("VAL1472_5_action_unsigned", action_unsigned, "parent action contract rows are not signed claims"),
        ("VAL1472_6_debt_sources", debt_sources_exist, "all coupling debt source paths exist"),
        ("VAL1472_7_debt_blocks_core", debt_blocks_core, "coupling debt blocks Newton/PPN/local-GR explicitly"),
        ("VAL1472_8_local_feed_nonclaim", local_feed_nonclaim, "local-GR feed rows are routing only"),
        ("VAL1472_9_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1472_10_live_paths", live_paths_untouched, "critical live claim/import paths remain absent"),
        ("VAL1472_11_gate_pattern", safe_gate_pattern, "source/debt gates pass while claim gates fail"),
        ("VAL1472_12_signing_refuses", signing_refuses, "parent signing refuses product/Newton/PPN/local-GR promotion"),
        ("VAL1472_13_generated_csv_parse", generated_parse, "all generated 1472 CSVs parse cleanly"),
        ("VAL1472_14_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1472_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1472_16_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1472_17_overall", overall, "1472 writes component source pack, refuses numeric promotion, and rolls coupling debt into local-GR route"))
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
    source_pack: list[dict[str, Any]],
    numeric_attempt: list[dict[str, Any]],
    action_contract: list[dict[str, Any]],
    debt_rows: list[dict[str, Any]],
    local_feed: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1472 - Y5 R10 RAB Alpha Product Component Source Pack Or Coupling Debt Rollup")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The component hunt improved the map but did not produce a score-ready alpha product: every clock/WEP/R10/mass-clock product still lacks at least one parent-owned factor.")
    lines.append("- The real shared bottleneck is now explicit: parent coupling ownership, shared tau/readout frame, finite-mode normalization, and source-current universality.")
    lines.append("- The coupling debt is rolled into the local-GR/Newton route as double-zero/action-block obligations, not promoted as a claim.")
    lines.append("")
    lines.append("## Component Source Pack")
    lines.append("| component_id | quantity | value_or_status | fill_class | remaining_gap |")
    lines.append("|---|---|---|---|---|")
    for row in source_pack:
        lines.append(f"| {row['component_id']} | {row['quantity']} | {row['value_or_status']} | {row['fill_class']} | {row['remaining_gap']} |")
    lines.append("")
    lines.append("## Numeric Fill Attempt")
    lines.append("| attempt_id | product_id | numeric_prediction | score_ready | reason |")
    lines.append("|---|---|---|---:|---|")
    for row in numeric_attempt:
        lines.append(f"| {row['attempt_id']} | {row['product_id']} | {row['numeric_prediction']} | {row['score_ready']} | {row['reason']} |")
    lines.append("")
    lines.append("## Parent Action Contract")
    lines.append("| contract_id | current_status | blocks_if_open |")
    lines.append("|---|---|---|")
    for row in action_contract:
        lines.append(f"| {row['contract_id']} | {row['current_status']} | {row['blocks_if_open']} |")
    lines.append("")
    lines.append("## Coupling Debt Rollup")
    lines.append("| debt_id | current_status | needed_to_close | blocks_local_GR |")
    lines.append("|---|---|---|---:|")
    for row in debt_rows:
        lines.append(f"| {row['debt_id']} | {row['current_status']} | {row['needed_to_close']} | {row['blocks_local_GR']} |")
    lines.append("")
    lines.append("## Local-GR Feed")
    lines.append("| feed_id | target_artifact | feed_statement |")
    lines.append("|---|---|---|")
    for row in local_feed:
        lines.append(f"| {row['feed_id']} | `{row['target_artifact']}` | {row['feed_statement']} |")
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
    source_pack = source_pack_rows()
    numeric_attempt = numeric_attempt_rows(source_pack)
    action_contract = action_contract_rows()
    debt_rows = coupling_debt_rows()
    local_feed = local_feed_rows(debt_rows)
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = gate_rows(source_pack, numeric_attempt, action_contract, debt_rows, local_feed)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SOURCE_PACK, source_pack)
    write_csv(NUMERIC_ATTEMPT, numeric_attempt)
    write_csv(ACTION_CONTRACT, action_contract)
    write_csv(COUPLING_DEBT, debt_rows)
    write_csv(LOCAL_FEED, local_feed)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_SOURCE_PACK, source_pack)
    write_csv(QUAR_COUPLING_DEBT, debt_rows)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(SOURCE_PACK, BRANCH_SOURCE_PACK)
    copy_branch(COUPLING_DEBT, BRANCH_COUPLING_DEBT)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, source_pack, numeric_attempt, action_contract, debt_rows, local_feed, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, source_pack, numeric_attempt, action_contract, debt_rows, local_feed, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1472_component_source_pack_coupling_debt_rollup_nonclaim")


if __name__ == "__main__":
    main()
