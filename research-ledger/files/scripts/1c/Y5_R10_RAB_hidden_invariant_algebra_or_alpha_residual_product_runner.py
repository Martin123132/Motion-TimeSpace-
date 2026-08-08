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
QUARANTINE = MICROSCOPE / "quarantine" / "1469"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1469-Y5-R10-RAB-hidden-invariant-algebra-or-alpha-residual-product-runner.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1468_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1468_VALIDATION.csv"
PREV_ALGEBRA = OUT / "P8_Y5_R10_1468_PARENT_VISIBLE_COEFFICIENT_ALGEBRA_TRIVIALITY_ATTEMPT.csv"
PREV_HIDDEN = OUT / "P8_Y5_R10_1468_HIDDEN_INVARIANT_ALGEBRA_AUDIT.csv"
PREV_GRAMMAR = OUT / "P8_Y5_R10_1468_VISIBLE_ACTION_GRAMMAR_NO_EXTENSION_AUDIT.csv"
PREV_RETAINED = OUT / "P8_Y5_R10_1468_RETAINED_ALPHA_CONSTANT_BOUND_ROWS.csv"
PREV_WAITSTATE = OUT / "P8_Y5_R10_1468_RETAINED_ALPHA_WAITSTATE_LEDGER.csv"
PREV_COUNTER = OUT / "P8_Y5_R10_1468_COUNTERMODEL_LEDGER.csv"
PREV_GATES = OUT / "P8_Y5_R10_1468_REDUCTION_GATES.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1468_PARENT_SIGNING_DECISION.csv"

VERTICAL_LIFT_1045 = OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
OP_CLASS_1049 = OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv"
PRODUCT_FUNCTOR_1050 = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
OBSTRUCTION_1054 = OUT / "P8_Y5_R10_1054_COUNTEREXAMPLE_OBSTRUCTION_LEDGER.csv"
MAXWELL_1057 = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
VISIBLE_EXHAUST_1058 = OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
ALLOWED_GRAMMAR_1065 = OUT / "P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv"
PARENT_GRAMMAR_1065 = OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv"
DOMAIN_RULE_1066 = OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv"
OP_DOMAIN_1091 = OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
NO_HIDDEN_1114 = OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv"
OBSTRUCTION_1114 = OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv"
BOUND_MATRIX_1048 = OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"
CLOCK_BOUND_1052 = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
BETA_ALPHA_1414 = OUT / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv"
R10_ALPHA_1034 = OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv"
ALPHA_GATE_1396 = OUT / "P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_VISIBLE_ALGEBRA = COEFF / "visible_coefficient_algebra_parent_signed_import.csv"
LIVE_ALPHA_PRODUCT = COEFF / "alpha_residual_product_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1469_SOURCE_REGISTER.csv"
HIDDEN_THEOREM = OUT / "P8_Y5_R10_1469_HIDDEN_INVARIANT_ALGEBRA_THEOREM_ATTEMPT.csv"
ORBIT_AUDIT = OUT / "P8_Y5_R10_1469_VERTICAL_ORBIT_TRANSITIVITY_AUDIT.csv"
DISCRETE_AUDIT = OUT / "P8_Y5_R10_1469_DISCRETE_HIDDEN_SECTOR_AUDIT.csv"
PRODUCT_SCHEMA = OUT / "P8_Y5_R10_1469_ALPHA_RESIDUAL_PRODUCT_SCHEMA.csv"
PRODUCT_RUNNER = OUT / "P8_Y5_R10_1469_ALPHA_RESIDUAL_PRODUCT_RUNNER_NONCLAIM.csv"
PRODUCT_WAITSTATE = OUT / "P8_Y5_R10_1469_ALPHA_RESIDUAL_PRODUCT_WAITSTATE_LEDGER.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1469_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1469_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1469_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1469_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1469_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1469_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1469_VALIDATION.csv"

QUAR_PRODUCT_SCHEMA = QUARANTINE / "ALPHA_RESIDUAL_PRODUCT_SCHEMA_NONCLAIM.csv"
QUAR_PRODUCT_RUNNER = QUARANTINE / "ALPHA_RESIDUAL_PRODUCT_RUNNER_NONCLAIM.csv"
QUAR_PRODUCT_WAITSTATE = QUARANTINE / "ALPHA_RESIDUAL_PRODUCT_WAITSTATE_LEDGER_NONCLAIM.csv"

BRANCH_HIDDEN_THEOREM = COEFF / "hidden_invariant_algebra_theorem_attempt_1469.csv"
BRANCH_PRODUCT_RUNNER = COEFF / "alpha_residual_product_runner_nonclaim_1469.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_hidden_invariant_signing_decision_1469.csv"


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
        ("SRC1469_0_1468_next", PREV_NEXT, "1468 handoff to hidden invariant algebra/product runner"),
        ("SRC1469_1_1468_validation", PREV_VALIDATION, "1468 validation baseline"),
        ("SRC1469_2_1468_algebra", PREV_ALGEBRA, "visible coefficient algebra attempt"),
        ("SRC1469_3_1468_hidden", PREV_HIDDEN, "hidden invariant algebra audit"),
        ("SRC1469_4_1468_grammar", PREV_GRAMMAR, "visible action grammar audit"),
        ("SRC1469_5_1468_retained", PREV_RETAINED, "retained alpha/constant bound rows"),
        ("SRC1469_6_1468_waitstate", PREV_WAITSTATE, "retained alpha waitstate ledger"),
        ("SRC1469_7_1468_counter", PREV_COUNTER, "1468 countermodels"),
        ("SRC1469_8_1468_gates", PREV_GATES, "1468 gate pattern"),
        ("SRC1469_9_1468_signing", PREV_SIGNING, "1468 signing refusal"),
        ("SRC1469_10_vertical_lift", VERTICAL_LIFT_1045, "vertical lift descent gate"),
        ("SRC1469_11_operator_class", OP_CLASS_1049, "operator classification rule attempt"),
        ("SRC1469_12_product_functor", PRODUCT_FUNCTOR_1050, "product functor theorem attempt"),
        ("SRC1469_13_obstruction_1054", OBSTRUCTION_1054, "scalar invariant obstruction ledger"),
        ("SRC1469_14_maxwell", MAXWELL_1057, "unique Maxwell subblock attempt"),
        ("SRC1469_15_visible_exhaust", VISIBLE_EXHAUST_1058, "visible operator-domain exhaustion attempt"),
        ("SRC1469_16_allowed_grammar", ALLOWED_GRAMMAR_1065, "allowed action grammar"),
        ("SRC1469_17_parent_grammar", PARENT_GRAMMAR_1065, "parent grammar audit"),
        ("SRC1469_18_domain_rule", DOMAIN_RULE_1066, "operator-domain rule audit"),
        ("SRC1469_19_operator_domain", OP_DOMAIN_1091, "operator-domain theorem attempt"),
        ("SRC1469_20_no_hidden_1114", NO_HIDDEN_1114, "no hidden-visible morphism theorem attempt"),
        ("SRC1469_21_obstruction_1114", OBSTRUCTION_1114, "coupling obstruction ledger"),
        ("SRC1469_22_bound_matrix", BOUND_MATRIX_1048, "alpha/mass/clock bound matrix"),
        ("SRC1469_23_clock_bound", CLOCK_BOUND_1052, "clock alpha product bound"),
        ("SRC1469_24_beta_alpha", BETA_ALPHA_1414, "WEP beta_source_alpha finite bound rows"),
        ("SRC1469_25_R10_alpha", R10_ALPHA_1034, "R10 alpha bound candidates"),
        ("SRC1469_26_alpha_gate", ALPHA_GATE_1396, "alphaEM/WEP/clock/R10 gate"),
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


def hidden_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "HIT1469_0_target",
            "claim_piece": "hidden invariant algebra triviality",
            "mathematical_statement": "O(C_hid)^Gv = R or, relative to p=(q_loc,pi_const), O(C_parent)^Gv = p^*O(Q_obs,K_const)",
            "proof_status": "TARGET_SHARP",
            "what_is_exact": "this is the exact condition needed to collapse hidden-to-visible coefficient maps",
            "what_is_missing": "parent vertical group/action and orbit/fibre theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "HIT1469_1_orbit_descent",
            "claim_piece": "orbit transitivity implies descent",
            "mathematical_statement": "if Gv-orbits are exactly connected fibres of p, then every Gv-invariant smooth coefficient is constant on fibres and descends to the quotient",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "what_is_exact": "standard quotient/descent logic; it would close smooth hidden scalar leakage on connected fibres",
            "what_is_missing": "MTS has not derived the Gv action or proved orbit=fibre",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "HIT1469_2_infinitesimal_limit",
            "claim_piece": "infinitesimal silence is weaker than global fibre triviality",
            "mathematical_statement": "L_v c=0 for all vertical generators proves local orbit constancy, but not constancy across disconnected fibres or invariant labels not generated by the vertical algebra",
            "proof_status": "EXACT_LIMITATION",
            "what_is_exact": "vertical derivative tests cannot kill discrete hidden sectors or untouched invariant scalars",
            "what_is_missing": "connectedness/completeness of the vertical generator system",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "HIT1469_3_scalar_obstruction",
            "claim_piece": "surviving hidden scalar defeats algebra triviality",
            "mathematical_statement": "if I_hid in O(C_hid)^Gv is nonconstant, c=c0+epsilon I_hid is a valid continuous hidden-visible coefficient unless the target grammar forbids it",
            "proof_status": "COUNTEREXAMPLE_PROVED",
            "what_is_exact": "one invariant scalar is enough to reopen f(I_hid)F_Q^2, mass, clock, and source-weight channels",
            "what_is_missing": "no-extra-invariant theorem or no-extension visible grammar",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "HIT1469_4_verdict",
            "claim_piece": "current corpus derives hidden invariant algebra triviality",
            "mathematical_statement": "HIT1469_1 plus connected/no-extra-invariant clauses would sign the route",
            "proof_status": "NOT_PARENT_DERIVED_PRODUCT_RUNNER_REQUIRED",
            "what_is_exact": "the theorem target is now fully specified",
            "what_is_missing": "orbit transitivity, no extra invariant scalars, disconnected-sector exclusion, and radiative/readout closure",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def orbit_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ORB1469_0_vertical_group",
            "required_clause": "parent defines a vertical groupoid/action Gv preserving q_loc and pi_const",
            "status": "UNSIGNED",
            "why_needed": "without a defined action, orbit transitivity is not a theorem",
            "counterexample_if_missing": "vertical directions are a chosen distribution, not a complete gauge-like group",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ORB1469_1_orbit_equals_fibre",
            "required_clause": "Gv-orbits equal fibres of p=(q_loc,pi_const)",
            "status": "UNSIGNED",
            "why_needed": "only then do invariant functions descend to quotient/constants",
            "counterexample_if_missing": "C_parent=QxKxR_X with trivial Gv action on X leaves X as invariant label",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ORB1469_2_generator_completeness",
            "required_clause": "listed vertical generators span all hidden fibre tangent directions",
            "status": "UNSIGNED",
            "why_needed": "L_v c=0 only tests generated directions",
            "counterexample_if_missing": "an ungenerated scalar direction carries Z_EM drift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "ORB1469_3_no_extra_invariants",
            "required_clause": "no invariant scalar I_hid survives outside q_loc/pi_const",
            "status": "UNSIGNED",
            "why_needed": "I_hid feeds continuous visible coefficient targets",
            "counterexample_if_missing": "Z_EM=g0^-2+epsilon I_hid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def discrete_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "DS1469_0_connected_fibre",
            "risk": "disconnected hidden fibre components",
            "status": "UNSIGNED",
            "why_it_matters": "smooth vertical derivatives can vanish while component constants differ",
            "needed_to_close": "connected fibre theorem or discrete-sector superselection with one visible coefficient value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "DS1469_1_topological_label",
            "risk": "topological hidden label not included in pi_const",
            "status": "UNSIGNED",
            "why_it_matters": "visible coefficients could depend on a hidden topological sector",
            "needed_to_close": "expand pi_const to include it or prove it cannot enter S_vis",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "DS1469_2_readout_branch_label",
            "risk": "readout branch label differs while q_loc appears fixed",
            "status": "UNSIGNED",
            "why_it_matters": "observed effective coefficients can carry branch labels after reduction",
            "needed_to_close": "radiative/readout no-extension theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def product_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "APS1469_0_required_columns",
            "required_columns": "product_id; arena; predicted_product_value; predicted_product_units; comparison_bound_value; comparison_bound_units; source_path; equation_ref; sign_or_abs_policy; all_factor_status",
            "schema_pass": True,
            "claim_rule": "valid_for_claim=true only if numeric predicted value, units, source path, equation ref, sign policy, and bound source all exist",
            "valid_for_claim": False,
        },
        {
            "schema_id": "APS1469_1_missing_marker_rule",
            "required_columns": "no MISSING_* marker in any claim-critical field",
            "schema_pass": True,
            "claim_rule": "any MISSING_* marker forces score_ready=false",
            "valid_for_claim": False,
        },
        {
            "schema_id": "APS1469_2_bound_rule",
            "required_columns": "comparison bound must be source-backed and not target-only unless explicitly smoke/nonclaim",
            "schema_pass": True,
            "claim_rule": "target-only and review-candidate bounds remain nonclaim",
            "valid_for_claim": False,
        },
    ]


def product_runner_rows() -> list[dict[str, Any]]:
    products = [
        (
            "APR1469_0_alpha_clock",
            "clock_fine_structure",
            "b_alpha_EM * tau_clock",
            "MISSING_DIRECT_P_CLOCK_ALPHA",
            "yr^-1",
            "2.1e-18",
            "yr^-1",
            "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv:ACB1052_2",
            "missing b_alpha_EM, tau_clock, readout model, source path",
        ),
        (
            "APR1469_1_WEP_alpha",
            "MICROSCOPE_WEP",
            "DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "MISSING_P_WEP_ALPHA",
            "dimensionless",
            "4.797780522732e-05",
            "dimensionless target_only",
            "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv:BSB1414_1_alpha_only_target",
            "missing parent basis map, beta_source_alpha, tau_WEP, material/readout composition matrix",
        ),
        (
            "APR1469_2_R10_alpha_lambda",
            "R10_short_range",
            "K_X * Qbar_source * Qbar_test /(4*pi*Z_X*G_obs)",
            "MISSING_ALPHA_LAMBDA_PREDICTION",
            "dimensionless alpha(lambda)",
            "review_candidate_curve_nonclaim",
            "dimensionless alpha(lambda)",
            "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv:R10B1034_3_vector_review_candidate_summary",
            "missing lambda_X, Z_X, K_X, Qbar_source/test, official or QA-approved bound curve",
        ),
        (
            "APR1469_3_mass_clock",
            "mass_clock_constants",
            "b_mu/b_nuc/b_clock_i * tau_clock",
            "MISSING_MASS_CLOCK_PRODUCT",
            "mixed product units",
            "matrix_only_no_single_bound",
            "mixed",
            "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1048_0_alpha_clock",
            "missing coefficient definitions, sensitivity matrix, tau_clock, units, source paths",
        ),
        (
            "APR1469_4_kappa_local",
            "Newton_PPN_Gdot",
            "dln_Geff_dt or partial_A/r ln G_eff residual product",
            "MISSING_KAPPA_RESIDUAL_VECTOR",
            "arena-dependent",
            "fallback_policy_only",
            "arena-dependent",
            "P8_global_coupling_superselection_CONTRACT.csv:GS7_scalar_branch_fallback",
            "missing numeric residual coefficients, source-normalized Newtonian map, local/orbital projections",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for product_id, arena, formula, predicted, units, bound, bound_units, source, missing in products:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "product_id": product_id,
                "arena": arena,
                "formula": formula,
                "predicted_product_value": predicted,
                "predicted_product_units": units,
                "comparison_bound_value": bound,
                "comparison_bound_units": bound_units,
                "comparison_source": source,
                "missing_inputs": missing,
                "all_factor_status": "BLOCKED_MISSING_INPUTS",
                "numeric_comparison_ready": False,
                "score_ready": False,
                "abs_predicted_le_bound": "not_evaluated",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def product_waitstate_rows() -> list[dict[str, Any]]:
    waitstates = [
        ("PWAIT1469_0", "APR1469_0_alpha_clock", "b_alpha_EM", "MISSING_MTS_VALUE", "derive hidden EM response or theorem-zero"),
        ("PWAIT1469_1", "APR1469_0_alpha_clock", "tau_clock", "MISSING_DYNAMICS", "derive clock hidden-flow normalization"),
        ("PWAIT1469_2", "APR1469_1_WEP_alpha", "tau_WEP", "MISSING_WEP_PROJECTION", "derive WEP readout/projection kernel"),
        ("PWAIT1469_3", "APR1469_1_WEP_alpha", "parent_basis_map", "MISSING_PARENT_BASIS", "fix source/current normalization basis"),
        ("PWAIT1469_4", "APR1469_2_R10_alpha_lambda", "R10_bound_curve", "REVIEW_CANDIDATE_NOT_CLAIM_READY", "obtain official/QA bound curve"),
        ("PWAIT1469_5", "APR1469_2_R10_alpha_lambda", "Qbar_source_test", "MISSING_MATERIAL_SOURCE_FACTORS", "derive/source material charges"),
        ("PWAIT1469_6", "APR1469_3_mass_clock", "mass_clock_coefficients", "MISSING_COEFFICIENT_DEFINITIONS", "derive coefficient definitions and units"),
        ("PWAIT1469_7", "APR1469_4_kappa_local", "source_normalized_Newton_map", "MISSING_LOCAL_SOURCE_MAP", "derive Newton/PPN source-normalized map"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "waitstate_id": wait_id,
            "product_id": product_id,
            "blocked_field": field,
            "current_value": marker,
            "required_resolution": resolution,
            "claim_effect": "product row remains nonclaim and score_ready=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for wait_id, product_id, field, marker, resolution in waitstates
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1469_0_surviving_scalar",
            "countermodel": "nonconstant invariant scalar I_hid exists and Z_EM=Z0+epsilon I_hid",
            "survives_why": "orbit transitivity/no-extra-invariant theorem is not parent-signed",
            "killed_by_1469": False,
            "needed_to_kill": "hidden invariant algebra triviality or no-extension visible grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1469_1_discrete_sector",
            "countermodel": "two disconnected hidden components share q/pi but have different visible coefficient constants",
            "survives_why": "infinitesimal vertical derivative tests do not see disconnected labels",
            "killed_by_1469": False,
            "needed_to_kill": "connected fibre theorem or discrete-sector inclusion in pi_const",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1469_2_readout_reentry",
            "countermodel": "bare coefficient algebra descends but effective/readout coefficient depends on hidden branch label",
            "survives_why": "radiative/readout closure remains unsigned",
            "killed_by_1469": False,
            "needed_to_kill": "radiative/readout no-extension theorem or explicit product bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1469_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1469_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1469_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1469_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1469_4_visible_algebra", LIVE_VISIBLE_ALGEBRA, "live parent-signed visible algebra import"),
        ("LG1469_5_alpha_product", LIVE_ALPHA_PRODUCT, "live alpha residual product claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1469": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(hidden: list[dict[str, Any]], products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conditional = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in hidden)
    obstruction = any(row["proof_status"] == "COUNTEREXAMPLE_PROVED" for row in hidden)
    product_rows = len(products) >= 5
    return [
        {
            "gate_id": "GATE1469_0_orbit_descent_theorem",
            "gate": "orbit-transitivity descent theorem is written",
            "gate_pass": conditional,
            "claim_effect": "conditional math only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_1_scalar_obstruction_written",
            "gate": "surviving hidden scalar obstruction is explicitly retained",
            "gate_pass": obstruction,
            "claim_effect": "prevents false algebra closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_2_parent_orbit_transitivity_signed",
            "gate": "parent proves orbit=fibre and no extra invariants",
            "gate_pass": False,
            "claim_effect": "hidden invariant algebra cannot be promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_3_discrete_sector_closed",
            "gate": "disconnected/topological hidden sector labels are excluded or included in pi_const",
            "gate_pass": False,
            "claim_effect": "discrete hidden coefficient branch remains",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_4_product_schema_written",
            "gate": "strict alpha residual product schema and runner rows are written",
            "gate_pass": product_rows,
            "claim_effect": "fallback runner scaffold only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_5_product_rows_score_ready",
            "gate": "alpha residual product rows are score-ready",
            "gate_pass": False,
            "claim_effect": "missing MTS values/projections/source paths",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1469_6_local_claim",
            "gate": "local GR/WEP/R10/Newton claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1469",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1469_0_hidden_invariant",
            "target": "hidden invariant algebra/orbit transitivity",
            "orbit_descent_conditional_theorem": True,
            "scalar_obstruction_retained": True,
            "parent_orbit_transitivity_signed": False,
            "no_extra_invariants_signed": False,
            "discrete_sector_closed": False,
            "radiative_readout_closure_signed": False,
            "product_runner_written": True,
            "product_rows_score_ready": False,
            "hidden_algebra_import_allowed": False,
            "visible_algebra_import_allowed": False,
            "alpha_product_claim_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_HIDDEN_ALGEBRA_PROMOTION_WRITE_NONCLAIM_PRODUCT_RUNNER",
            "reason": "orbit descent is exact conditionally, but parent orbit transitivity/no-extra-invariant/discrete-sector/radiative clauses are unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1469_0",
            "decision": "preserve the orbit-transitivity theorem as conditional math",
            "why": "it is the cleanest possible derivation route for hidden coefficient silence",
            "consequence": "future proof work should target parent Gv action and orbit=fibre",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1469_1",
            "decision": "do not hide the scalar/discrete obstruction",
            "why": "one invariant scalar or disconnected fibre label defeats no-hidden-visible coefficients",
            "consequence": "alpha/clock/WEP/R10 residuals remain live",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1469_2",
            "decision": "turn retained alpha rows into a strict product runner",
            "why": "failed derivation routes must become testable residual products with units and source gates",
            "consequence": "runner is schema-ready but not score-ready",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1469_0_1470",
            "next_target": "1470-Y5-R10-RAB-no-extension-visible-action-grammar-or-alpha-product-source-fill.md",
            "script": "scripts/Y5_R10_RAB_no_extension_visible_action_grammar_or_alpha_product_source_fill.py",
            "objective": "try the alternative no-extension visible action grammar route; if it fails, start filling alpha product runner inputs with sourced nonclaim rows",
            "include": "typed visible action language; no hidden argument slots; radiative/readout closure requirement; b_alpha/tau/source-path product fields",
            "exclude": "local-GR pass; WEP/R10 claim; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        HIDDEN_THEOREM,
        ORBIT_AUDIT,
        DISCRETE_AUDIT,
        PRODUCT_SCHEMA,
        PRODUCT_RUNNER,
        PRODUCT_WAITSTATE,
        COUNTERMODELS,
        QUAR_PRODUCT_SCHEMA,
        QUAR_PRODUCT_RUNNER,
        QUAR_PRODUCT_WAITSTATE,
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
    return BRANCH_HIDDEN_THEOREM.exists() and BRANCH_PRODUCT_RUNNER.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    hidden: list[dict[str, Any]],
    orbit: list[dict[str, Any]],
    discrete: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    products: list[dict[str, Any]],
    waits: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    conditional_written = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in hidden)
    scalar_obstruction = any(row["proof_status"] == "COUNTEREXAMPLE_PROVED" for row in hidden)
    theorem_refused = any(row["proof_status"] == "NOT_PARENT_DERIVED_PRODUCT_RUNNER_REQUIRED" for row in hidden)
    orbit_unsigned = all(row["status"] == "UNSIGNED" for row in orbit)
    discrete_unsigned = all(row["status"] == "UNSIGNED" for row in discrete)
    schema_ok = len(schema) >= 3 and all(truth(row["schema_pass"]) for row in schema)
    products_nonclaim = len(products) >= 5 and all(
        not truth(row["numeric_comparison_ready"])
        and not truth(row["score_ready"])
        and not truth(row["valid_for_claim"])
        and "MISSING" in row["predicted_product_value"]
        for row in products
    )
    waits_block = len(waits) >= 8 and all(not truth(row["claim_allowed"]) and "MISSING" in row["current_value"] or row["current_value"] == "REVIEW_CANDIDATE_NOT_CLAIM_READY" for row in waits)
    countermodels_retained = all(not truth(row["killed_by_1469"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1469"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and truth(gates[4]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[2:4] + gates[5:]
    )
    signing_refuses = all(
        truth(row["orbit_descent_conditional_theorem"])
        and truth(row["scalar_obstruction_retained"])
        and not truth(row["parent_orbit_transitivity_signed"])
        and not truth(row["hidden_algebra_import_allowed"])
        and not truth(row["alpha_product_claim_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1469_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1469_1_conditional", conditional_written, "orbit-transitivity descent theorem written"),
        ("VAL1469_2_scalar_obstruction", scalar_obstruction, "scalar obstruction retained"),
        ("VAL1469_3_refusal", theorem_refused, "hidden algebra promotion refused"),
        ("VAL1469_4_orbit_unsigned", orbit_unsigned, "orbit clauses remain unsigned"),
        ("VAL1469_5_discrete_unsigned", discrete_unsigned, "discrete hidden sector clauses remain unsigned"),
        ("VAL1469_6_schema", schema_ok, "alpha residual product schema written"),
        ("VAL1469_7_products_nonclaim", products_nonclaim, "product runner rows are nonclaim and not score-ready"),
        ("VAL1469_8_waitstates", waits_block, "waitstates block all product rows"),
        ("VAL1469_9_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1469_10_live_paths", live_paths_untouched, "critical live official/source/material/Cparent/algebra/product files remain absent"),
        ("VAL1469_11_gate_pattern", safe_gate_pattern, "only conditional/obstruction/schema gates pass; claim gates false"),
        ("VAL1469_12_signing_refuses", signing_refuses, "parent signing refuses hidden algebra/product/local claims"),
        ("VAL1469_13_generated_csv_parse", generated_parse, "all generated 1469 CSVs parse cleanly"),
        ("VAL1469_14_branch_copies", branch_copies_exist(), "nonclaim branch copies written"),
        ("VAL1469_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1469_16_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1469_17_overall", overall, "1469 keeps hidden algebra conditional and writes strict nonclaim alpha product runner"))
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
    hidden: list[dict[str, Any]],
    orbit: list[dict[str, Any]],
    discrete: list[dict[str, Any]],
    products: list[dict[str, Any]],
    waits: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1469 - Y5 R10 RAB Hidden Invariant Algebra Or Alpha Residual Product Runner")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- Orbit-transitivity would close hidden coefficient silence, but only as an exact conditional theorem.")
    lines.append("- The parent corpus still has not signed the vertical group action, orbit=fibre, no-extra-invariant, discrete-sector, or radiative/readout clauses.")
    lines.append("- A surviving invariant scalar or disconnected hidden sector still permits `f(I_hid)F_Q^2` and related mass/clock/source coefficient leakage.")
    lines.append("- The fallback alpha/constant residual product runner is now stricter, but all rows remain nonclaim and not score-ready.")
    lines.append("")
    lines.append("## Hidden Invariant Algebra Attempt")
    lines.append("| theorem_id | proof_status | what_is_missing |")
    lines.append("|---|---|---|")
    for row in hidden:
        lines.append(f"| {row['theorem_id']} | {row['proof_status']} | {row['what_is_missing']} |")
    lines.append("")
    lines.append("## Orbit Audit")
    lines.append("| audit_id | status | counterexample_if_missing |")
    lines.append("|---|---|---|")
    for row in orbit:
        lines.append(f"| {row['audit_id']} | {row['status']} | {row['counterexample_if_missing']} |")
    lines.append("")
    lines.append("## Discrete Sector Audit")
    lines.append("| audit_id | status | needed_to_close |")
    lines.append("|---|---|---|")
    for row in discrete:
        lines.append(f"| {row['audit_id']} | {row['status']} | {row['needed_to_close']} |")
    lines.append("")
    lines.append("## Alpha Product Runner")
    lines.append("| product_id | arena | predicted_product_value | comparison_bound_value | score_ready |")
    lines.append("|---|---|---|---|---:|")
    for row in products:
        lines.append(f"| {row['product_id']} | {row['arena']} | {row['predicted_product_value']} | {row['comparison_bound_value']} | {row['score_ready']} |")
    lines.append("")
    lines.append("## Product Waitstates")
    lines.append("| waitstate_id | product_id | blocked_field | current_value |")
    lines.append("|---|---|---|---|")
    for row in waits:
        lines.append(f"| {row['waitstate_id']} | {row['product_id']} | {row['blocked_field']} | {row['current_value']} |")
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
    hidden = hidden_theorem_rows()
    orbit = orbit_audit_rows()
    discrete = discrete_audit_rows()
    schema = product_schema_rows()
    products = product_runner_rows()
    waits = product_waitstate_rows()
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(hidden, products)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(HIDDEN_THEOREM, hidden)
    write_csv(ORBIT_AUDIT, orbit)
    write_csv(DISCRETE_AUDIT, discrete)
    write_csv(PRODUCT_SCHEMA, schema)
    write_csv(PRODUCT_RUNNER, products)
    write_csv(PRODUCT_WAITSTATE, waits)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_PRODUCT_SCHEMA, schema)
    write_csv(QUAR_PRODUCT_RUNNER, products)
    write_csv(QUAR_PRODUCT_WAITSTATE, waits)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(HIDDEN_THEOREM, BRANCH_HIDDEN_THEOREM)
    copy_branch(PRODUCT_RUNNER, BRANCH_PRODUCT_RUNNER)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, hidden, orbit, discrete, schema, products, waits, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, hidden, orbit, discrete, products, waits, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1469_hidden_invariant_conditional_alpha_product_runner_nonclaim")


if __name__ == "__main__":
    main()
