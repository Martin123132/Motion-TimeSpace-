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
QUARANTINE = MICROSCOPE / "quarantine" / "1470"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1470-Y5-R10-RAB-no-extension-visible-action-grammar-or-alpha-product-source-fill.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1469_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1469_VALIDATION.csv"
PREV_HIDDEN = OUT / "P8_Y5_R10_1469_HIDDEN_INVARIANT_ALGEBRA_THEOREM_ATTEMPT.csv"
PREV_PRODUCT = OUT / "P8_Y5_R10_1469_ALPHA_RESIDUAL_PRODUCT_RUNNER_NONCLAIM.csv"
PREV_WAIT = OUT / "P8_Y5_R10_1469_ALPHA_RESIDUAL_PRODUCT_WAITSTATE_LEDGER.csv"
PREV_GATES = OUT / "P8_Y5_R10_1469_REDUCTION_GATES.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1469_PARENT_SIGNING_DECISION.csv"

NO_HIDDEN_1114 = OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv"
OBSTRUCTION_1114 = OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv"
PRODUCT_FUNCTOR_1050 = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
VISIBLE_EXHAUST_1058 = OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
ALLOWED_GRAMMAR_1065 = OUT / "P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv"
PARENT_GRAMMAR_1065 = OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv"
OP_CLASS_1049 = OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv"
OP_DOMAIN_1091 = OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
CLOCK_BOUND_1052 = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
BETA_ALPHA_1414 = OUT / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv"
R10_ALPHA_1034 = OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv"
BOUND_MATRIX_1048 = OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_GRAMMAR = COEFF / "typed_visible_action_grammar_parent_signed_import.csv"
LIVE_ALPHA_PRODUCT = COEFF / "alpha_residual_product_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1470_SOURCE_REGISTER.csv"
TYPED_GRAMMAR = OUT / "P8_Y5_R10_1470_TYPED_VISIBLE_ACTION_GRAMMAR_ATTEMPT.csv"
NO_EXTENSION_AUDIT = OUT / "P8_Y5_R10_1470_NO_EXTENSION_AUDIT.csv"
RADIATIVE_AUDIT = OUT / "P8_Y5_R10_1470_RADIATIVE_READOUT_CLOSURE_AUDIT.csv"
ALPHA_SOURCE_FILL = OUT / "P8_Y5_R10_1470_ALPHA_PRODUCT_SOURCE_FILL_NONCLAIM.csv"
ALPHA_FILL_STATUS = OUT / "P8_Y5_R10_1470_ALPHA_PRODUCT_FILL_STATUS.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1470_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1470_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1470_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1470_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1470_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1470_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1470_VALIDATION.csv"

QUAR_SOURCE_FILL = QUARANTINE / "ALPHA_PRODUCT_SOURCE_FILL_NONCLAIM.csv"
QUAR_FILL_STATUS = QUARANTINE / "ALPHA_PRODUCT_FILL_STATUS.csv"

BRANCH_GRAMMAR = COEFF / "typed_visible_action_grammar_attempt_1470.csv"
BRANCH_SOURCE_FILL = COEFF / "alpha_product_source_fill_nonclaim_1470.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_typed_grammar_signing_decision_1470.csv"


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
        ("SRC1470_0_1469_next", PREV_NEXT, "1469 handoff to typed/no-extension grammar or alpha product source fill"),
        ("SRC1470_1_1469_validation", PREV_VALIDATION, "1469 validation baseline"),
        ("SRC1470_2_1469_hidden", PREV_HIDDEN, "hidden invariant algebra conditional/refusal"),
        ("SRC1470_3_1469_product", PREV_PRODUCT, "strict nonclaim alpha product runner"),
        ("SRC1470_4_1469_wait", PREV_WAIT, "product waitstates"),
        ("SRC1470_5_1469_gates", PREV_GATES, "1469 gate pattern"),
        ("SRC1470_6_1469_signing", PREV_SIGNING, "1469 signing refusal"),
        ("SRC1470_7_1114_no_hidden", NO_HIDDEN_1114, "typed/product no-hidden visible morphism attempt"),
        ("SRC1470_8_1114_obstruction", OBSTRUCTION_1114, "coupling obstruction ledger"),
        ("SRC1470_9_1050_product_functor", PRODUCT_FUNCTOR_1050, "visible-hidden product functor attempt"),
        ("SRC1470_10_1058_visible_exhaust", VISIBLE_EXHAUST_1058, "visible operator-domain exhaustion attempt"),
        ("SRC1470_11_1065_allowed", ALLOWED_GRAMMAR_1065, "allowed action grammar"),
        ("SRC1470_12_1065_parent", PARENT_GRAMMAR_1065, "parent grammar audit"),
        ("SRC1470_13_1049_operator", OP_CLASS_1049, "operator classification attempt"),
        ("SRC1470_14_1091_domain", OP_DOMAIN_1091, "operator domain theorem attempt"),
        ("SRC1470_15_clock_bound", CLOCK_BOUND_1052, "clock alpha product bound"),
        ("SRC1470_16_beta_alpha", BETA_ALPHA_1414, "WEP alpha finite target rows"),
        ("SRC1470_17_R10_alpha", R10_ALPHA_1034, "R10 alpha bound candidate rows"),
        ("SRC1470_18_bound_matrix", BOUND_MATRIX_1048, "alpha/mass/clock bound matrix"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, usage in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "usage": usage,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def typed_grammar_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_0_target",
            "claim_piece": "typed visible action language excludes hidden arguments",
            "formal_statement": "Coeff(O_vis) is a typed functor on Q_vis x Rep x Level_EM; C_hid is not in its domain.",
            "result": "TARGET_SHARP",
            "what_is_exact": "if the typed parent language is signed, f(I_hid)F_Q^2 and hidden mass/clock/source coefficient terms are ill-formed",
            "what_is_missing": "parent DSL/signature deriving that domain restriction",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_1_type_theorem",
            "claim_piece": "no hidden-visible coefficient morphism by syntax",
            "formal_statement": "If hidden objects are not well-typed arguments of visible coefficient functors, Hom(C_hid,Coeff(O_vis)) is absent by grammar, not set to zero dynamically.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "what_is_exact": "this is stronger than covariance and bypasses the scalar-invariant obstruction by removing the target morphism",
            "what_is_missing": "the corpus has not derived the typed grammar from MTS primitives",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_2_product_category",
            "claim_piece": "visible-hidden product category sequester",
            "formal_statement": "C_parent=C_vis x C_hid and S_vis factors through pi_vis; D_hid coeff_vis=0 by chain rule.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "what_is_exact": "same closure route as product functor theorem",
            "what_is_missing": "parent construction of product category and projection functors",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_3_no_extension",
            "claim_piece": "no extension by hidden, material, source, or readout labels",
            "formal_statement": "visible coefficient domains cannot be enlarged after the fact to Q_vis x Rep x Level_EM x {I_hid,m,D,A,readout_branch}.",
            "result": "REQUIRED_NO_EXTENSION_NOT_DERIVED",
            "what_is_exact": "this is the clause that stops closure-by-renaming",
            "what_is_missing": "primitive no-extension theorem for MTS quotient/readout language",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_4_radiative_limit",
            "claim_piece": "typed grammar survives EFT/readout",
            "formal_statement": "S_vis^eff and readout maps preserve the same typed domains and do not generate hidden arguments.",
            "result": "UNSIGNED_REQUIRED_CLOSURE",
            "what_is_exact": "tree-level syntax is not enough for observed clock/WEP/R10 reductions",
            "what_is_missing": "radiative/readout closure theorem or explicit residual product bounds",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "TNG1470_5_verdict",
            "claim_piece": "typed/no-extension grammar closes hidden visible coefficients",
            "formal_statement": "TNG1470_1 + TNG1470_2 + TNG1470_3 + TNG1470_4 would close the route.",
            "result": "NOT_PARENT_DERIVED_START_SOURCE_FILL",
            "what_is_exact": "the conditional grammar route is clean and should stay as a theorem target",
            "what_is_missing": "parent grammar/no-extension/radiative signatures",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def no_extension_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NX1470_0_parent_DSL",
            "required_clause": "parent defines a typed action language before empirical scoring",
            "status": "UNSIGNED",
            "if_missing": "hidden coefficient maps can be declared legal later",
            "needed_to_close": "formal MTS parent DSL/signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NX1470_1_hidden_argument_absence",
            "required_clause": "hidden objects are not valid arguments of visible coefficient functors",
            "status": "EXACT_IF_PARENT_SYNTAX_ACCEPTED_NOT_DERIVED",
            "if_missing": "f(I_hid)F_Q^2 is well-typed",
            "needed_to_close": "typed-domain theorem, not covariance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NX1470_2_no_spurion_extension",
            "required_clause": "material/domain/source/readout labels cannot be imported as spurion coefficients",
            "status": "UNSIGNED",
            "if_missing": "source/test labels can re-enter WEP and R10 products",
            "needed_to_close": "primitive no-extension quotient/readout theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "NX1470_3_no_source_label_extension",
            "required_clause": "source functor cannot be extended from T_total to (T_A,A) before coupling selection",
            "status": "UNSIGNED",
            "if_missing": "beta_source_alpha and relative source weights remain legal",
            "needed_to_close": "source-label forgetting quotient theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def radiative_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RAD1470_0_bare_to_effective",
            "required_clause": "bare no-hidden grammar is stable under effective action reduction",
            "status": "UNSIGNED",
            "risk_if_missing": "loops/thresholds generate Z_EM^eff(I_hid)",
            "fallback": "retain b_alpha product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RAD1470_1_clock_readout",
            "required_clause": "clock spectroscopy readout preserves typed coefficient domains",
            "status": "UNSIGNED",
            "risk_if_missing": "clock_i(I_hid) or b_clock_i terms enter frequency ratios",
            "fallback": "retain clock product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RAD1470_2_WEP_material_readout",
            "required_clause": "material/readout reduction does not attach composition labels to hidden coefficients",
            "status": "UNSIGNED",
            "risk_if_missing": "DeltaQ_alpha_AB beta_source_alpha b_alpha tau_WEP remains live",
            "fallback": "retain WEP alpha product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "RAD1470_3_R10_source_test",
            "required_clause": "R10 source/test charge construction preserves no-hidden grammar",
            "status": "UNSIGNED",
            "risk_if_missing": "Qbar_source/test hidden coefficient products remain live",
            "fallback": "retain R10 alpha(lambda) product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def alpha_source_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1470_0_alpha_clock",
            "arena": "clock_fine_structure",
            "formula": "b_alpha_EM * tau_clock",
            "prediction_side_value": "MISSING_DIRECT_P_CLOCK_ALPHA",
            "prediction_side_status": "MISSING_MTS_VALUE_AND_DYNAMICS",
            "prediction_units": "yr^-1",
            "comparison_bound_value": "2.1e-18",
            "comparison_units": "yr^-1",
            "comparison_source": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv:ACB1052_2",
            "comparison_status": "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "source_fill_level": "COMPARISON_SIDE_FILLED_ONLY",
            "numeric_comparison_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1470_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "formula": "DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "prediction_side_value": "MISSING_P_WEP_ALPHA",
            "prediction_side_status": "MISSING_PARENT_BASIS_BETA_TAU_MATERIAL_READOUT",
            "prediction_units": "dimensionless",
            "comparison_bound_value": "4.797780522732e-05",
            "comparison_units": "dimensionless target_only",
            "comparison_source": "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv:BSB1414_1_alpha_only_target",
            "comparison_status": "TARGET_ONLY_NONCLAIM",
            "source_fill_level": "COMPARISON_SIDE_TARGET_ONLY",
            "numeric_comparison_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1470_2_R10_alpha_lambda",
            "arena": "R10_short_range",
            "formula": "K_X * Qbar_source * Qbar_test /(4*pi*Z_X*G_obs)",
            "prediction_side_value": "MISSING_ALPHA_LAMBDA_PREDICTION",
            "prediction_side_status": "MISSING_LAMBDA_K_Z_QBAR_AND_OFFICIAL_CURVE",
            "prediction_units": "dimensionless alpha(lambda)",
            "comparison_bound_value": "0.002344664300519378..897932.2928704522",
            "comparison_units": "dimensionless alpha(lambda) review_candidate",
            "comparison_source": "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv:R10B1034_3_vector_review_candidate_summary",
            "comparison_status": "REVIEW_CANDIDATE_CURVE_NONCLAIM",
            "source_fill_level": "COMPARISON_SIDE_REVIEW_CANDIDATE_ONLY",
            "numeric_comparison_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "product_id": "APR1470_3_mass_clock",
            "arena": "mass_clock_constants",
            "formula": "b_mu/b_nuc/b_clock_i * tau_clock",
            "prediction_side_value": "MISSING_MASS_CLOCK_PRODUCT",
            "prediction_side_status": "MISSING_COEFFICIENT_DEFINITIONS_SENSITIVITY_TAU_UNITS",
            "prediction_units": "mixed product units",
            "comparison_bound_value": "matrix_only_no_single_bound",
            "comparison_units": "mixed",
            "comparison_source": "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1048_0_alpha_clock",
            "comparison_status": "SOURCE_MATRIX_PARTIAL_NONCLAIM",
            "source_fill_level": "MATRIX_LINK_FILLED_ONLY",
            "numeric_comparison_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def fill_status_rows(source_fill: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "FILL1470_0_comparison_sources",
            "summary": "comparison-side anchors are now explicitly linked for clock, WEP alpha, R10 alpha(lambda), and mass/clock matrix rows",
            "rows_affected": ";".join(row["product_id"] for row in source_fill),
            "score_ready": False,
            "reason_not_score_ready": "prediction-side MTS values, units, projections, and source paths remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": "FILL1470_1_no_promotion",
            "summary": "no live coefficient/product import is written",
            "rows_affected": "all APR1470 rows",
            "score_ready": False,
            "reason_not_score_ready": "filled comparison fields are not MTS predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1470_0_typed_language_not_parent",
            "countermodel": "parent action language is not typed, so f(I_hid)F_Q^2 is simply a legal scalar-density term",
            "survives_why": "typed DSL/signature is not parent-derived",
            "killed_by_1470": False,
            "needed_to_kill": "parent typed visible action language theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1470_1_extended_quotient",
            "countermodel": "q_ext=(q_loc,I_hid) is declared the real visible quotient after the fact",
            "survives_why": "no-extension theorem is unsigned",
            "killed_by_1470": False,
            "needed_to_kill": "primitive no-extension quotient/readout theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1470_2_radiative_readout",
            "countermodel": "bare typed action is clean but effective/readout coefficient depends on I_hid",
            "survives_why": "radiative/readout closure is unsigned",
            "killed_by_1470": False,
            "needed_to_kill": "renormalized/effective/readout domain preservation theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1470_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1470_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1470_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1470_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1470_4_typed_grammar", LIVE_GRAMMAR, "live parent-signed typed grammar import"),
        ("LG1470_5_alpha_product", LIVE_ALPHA_PRODUCT, "live alpha residual product claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1470": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(grammar: list[dict[str, Any]], source_fill: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_typed = any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in grammar)
    verdict_refuses = any(row["result"] == "NOT_PARENT_DERIVED_START_SOURCE_FILL" for row in grammar)
    source_fill_written = len(source_fill) >= 4
    return [
        {
            "gate_id": "GATE1470_0_typed_theorem",
            "gate": "typed no-hidden-visible theorem is written exactly",
            "gate_pass": exact_typed,
            "claim_effect": "conditional math only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_1_parent_typed_grammar_signed",
            "gate": "parent typed visible action language is signed",
            "gate_pass": False,
            "claim_effect": "no hidden coefficient theorem cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_2_no_extension_signed",
            "gate": "primitive no-extension theorem is signed",
            "gate_pass": False,
            "claim_effect": "hidden/readout/source extensions remain possible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_3_radiative_readout_signed",
            "gate": "radiative/readout closure is signed",
            "gate_pass": False,
            "claim_effect": "effective coefficient reentry remains possible",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_4_refusal_recorded",
            "gate": "typed grammar route refusal is explicitly recorded",
            "gate_pass": verdict_refuses,
            "claim_effect": "prevents false closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_5_source_fill_written",
            "gate": "comparison-side alpha product source fill is written",
            "gate_pass": source_fill_written,
            "claim_effect": "comparison scaffold only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_6_product_rows_score_ready",
            "gate": "alpha product rows are score-ready",
            "gate_pass": False,
            "claim_effect": "prediction-side MTS values still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1470_7_local_claim",
            "gate": "local GR/WEP/R10/Newton claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1470",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1470_0_typed_grammar",
            "target": "typed/no-extension visible action grammar",
            "typed_conditional_theorem_written": True,
            "parent_typed_grammar_signed": False,
            "no_extension_signed": False,
            "radiative_readout_closure_signed": False,
            "comparison_source_fill_written": True,
            "product_rows_score_ready": False,
            "typed_grammar_import_allowed": False,
            "alpha_product_claim_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_TYPED_GRAMMAR_PROMOTION_FILL_COMPARISON_SOURCES_NONCLAIM",
            "reason": "typed grammar is exact conditionally, but parent DSL/no-extension/radiative closure are unsigned; comparison anchors are not MTS predictions",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1470_0",
            "decision": "keep typed grammar as the cleanest closure theorem target",
            "why": "syntax can forbid hidden morphisms without relying on covariance or scalar-invariant absence",
            "consequence": "future derivation should target parent DSL/no-extension",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1470_1",
            "decision": "refuse promotion",
            "why": "typed grammar, no-extension, and radiative/readout closure are not parent-signed",
            "consequence": "hidden coefficient branches remain live",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1470_2",
            "decision": "fill comparison-side source anchors",
            "why": "nonclaim product rows become more test-ready without fabricating MTS predictions",
            "consequence": "next step can fill prediction-side fields or derive theorem-zero",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1470_0_1471",
            "next_target": "1471-Y5-R10-RAB-radiative-readout-closure-or-alpha-product-prediction-fill.md",
            "script": "scripts/Y5_R10_RAB_radiative_readout_closure_or_alpha_product_prediction_fill.py",
            "objective": "try to derive radiative/readout preservation of the typed grammar; if it fails, start filling prediction-side alpha product fields with sourced MTS definitions where possible",
            "include": "S_vis^eff domain preservation; clock/WEP/R10 readout maps; b_alpha/tau/prediction source paths; no claim promotion",
            "exclude": "local-GR pass; WEP/R10 claim; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        TYPED_GRAMMAR,
        NO_EXTENSION_AUDIT,
        RADIATIVE_AUDIT,
        ALPHA_SOURCE_FILL,
        ALPHA_FILL_STATUS,
        COUNTERMODELS,
        QUAR_SOURCE_FILL,
        QUAR_FILL_STATUS,
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
    return BRANCH_GRAMMAR.exists() and BRANCH_SOURCE_FILL.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    extension: list[dict[str, Any]],
    radiative: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    fill_status: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_theorem = any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in grammar)
    refusal = any(row["result"] == "NOT_PARENT_DERIVED_START_SOURCE_FILL" for row in grammar)
    extension_unsigned = all(row["status"] in {"UNSIGNED", "EXACT_IF_PARENT_SYNTAX_ACCEPTED_NOT_DERIVED"} for row in extension)
    radiative_unsigned = all(row["status"] == "UNSIGNED" for row in radiative)
    source_fill_nonclaim = len(source_fill) >= 4 and all(
        row["source_fill_level"] != ""
        and not truth(row["numeric_comparison_ready"])
        and not truth(row["score_ready"])
        and not truth(row["valid_prediction_row"])
        and not truth(row["claim_allowed"])
        for row in source_fill
    )
    comparison_sources_filled = all(row["comparison_source"] and "MISSING" not in row["comparison_source"] for row in source_fill)
    prediction_missing = all("MISSING" in row["prediction_side_value"] or row["prediction_side_value"] == "matrix_only_no_single_bound" for row in source_fill)
    fill_status_blocks = all(not truth(row["score_ready"]) and not truth(row["claim_allowed"]) for row in fill_status)
    countermodels_retained = all(not truth(row["killed_by_1470"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1470"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[4]["gate_pass"]) and truth(gates[5]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:4] + gates[6:]
    )
    signing_refuses = all(
        truth(row["typed_conditional_theorem_written"])
        and truth(row["comparison_source_fill_written"])
        and not truth(row["parent_typed_grammar_signed"])
        and not truth(row["no_extension_signed"])
        and not truth(row["typed_grammar_import_allowed"])
        and not truth(row["alpha_product_claim_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1470_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1470_1_exact_theorem", exact_theorem, "typed no-hidden theorem written conditionally"),
        ("VAL1470_2_refusal", refusal, "typed grammar promotion refused"),
        ("VAL1470_3_extension_unsigned", extension_unsigned, "no-extension clauses remain unsigned"),
        ("VAL1470_4_radiative_unsigned", radiative_unsigned, "radiative/readout closure remains unsigned"),
        ("VAL1470_5_source_fill", source_fill_nonclaim, "comparison-side alpha product source fill written nonclaim"),
        ("VAL1470_6_comparison_sources", comparison_sources_filled, "comparison source strings are filled"),
        ("VAL1470_7_prediction_missing", prediction_missing, "prediction-side values remain missing"),
        ("VAL1470_8_fill_status_blocks", fill_status_blocks, "fill status blocks score-ready promotion"),
        ("VAL1470_9_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1470_10_live_paths", live_paths_untouched, "critical live official/source/material/Cparent/grammar/product files remain absent"),
        ("VAL1470_11_gate_pattern", safe_gate_pattern, "only conditional/refusal/source-fill gates pass; claim gates false"),
        ("VAL1470_12_signing_refuses", signing_refuses, "parent signing refuses grammar/product/local claims"),
        ("VAL1470_13_generated_csv_parse", generated_parse, "all generated 1470 CSVs parse cleanly"),
        ("VAL1470_14_branch_copies", branch_copies_exist(), "nonclaim branch copies written"),
        ("VAL1470_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1470_16_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1470_17_overall", overall, "1470 keeps typed grammar conditional and fills comparison-side alpha sources nonclaim"))
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
    grammar: list[dict[str, Any]],
    extension: list[dict[str, Any]],
    radiative: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1470 - Y5 R10 RAB No-Extension Visible Action Grammar Or Alpha Product Source Fill")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- Typed/no-extension grammar is an exact conditional route: if hidden objects are not valid visible coefficient arguments, hidden-visible morphisms are absent by syntax.")
    lines.append("- The route is not parent-signed: parent DSL, no-extension, source-label, and radiative/readout closure remain missing.")
    lines.append("- The alpha product runner is improved on the comparison side only; no MTS prediction values are filled and no row is score-ready.")
    lines.append("")
    lines.append("## Typed Grammar Attempt")
    lines.append("| attempt_id | result | what_is_missing |")
    lines.append("|---|---|---|")
    for row in grammar:
        lines.append(f"| {row['attempt_id']} | {row['result']} | {row['what_is_missing']} |")
    lines.append("")
    lines.append("## No-Extension Audit")
    lines.append("| audit_id | status | needed_to_close |")
    lines.append("|---|---|---|")
    for row in extension:
        lines.append(f"| {row['audit_id']} | {row['status']} | {row['needed_to_close']} |")
    lines.append("")
    lines.append("## Radiative/Readout Audit")
    lines.append("| audit_id | status | fallback |")
    lines.append("|---|---|---|")
    for row in radiative:
        lines.append(f"| {row['audit_id']} | {row['status']} | {row['fallback']} |")
    lines.append("")
    lines.append("## Alpha Product Source Fill")
    lines.append("| product_id | comparison_bound_value | comparison_status | prediction_side_status | score_ready |")
    lines.append("|---|---|---|---|---:|")
    for row in source_fill:
        lines.append(f"| {row['product_id']} | {row['comparison_bound_value']} | {row['comparison_status']} | {row['prediction_side_status']} | {row['score_ready']} |")
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
    grammar = typed_grammar_rows()
    extension = no_extension_audit_rows()
    radiative = radiative_audit_rows()
    source_fill = alpha_source_fill_rows()
    fill_status = fill_status_rows(source_fill)
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(grammar, source_fill)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TYPED_GRAMMAR, grammar)
    write_csv(NO_EXTENSION_AUDIT, extension)
    write_csv(RADIATIVE_AUDIT, radiative)
    write_csv(ALPHA_SOURCE_FILL, source_fill)
    write_csv(ALPHA_FILL_STATUS, fill_status)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_SOURCE_FILL, source_fill)
    write_csv(QUAR_FILL_STATUS, fill_status)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(TYPED_GRAMMAR, BRANCH_GRAMMAR)
    copy_branch(ALPHA_SOURCE_FILL, BRANCH_SOURCE_FILL)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, grammar, extension, radiative, source_fill, fill_status, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, grammar, extension, radiative, source_fill, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1470_typed_grammar_conditional_alpha_source_fill_nonclaim")


if __name__ == "__main__":
    main()
