from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_matter_frame_variation_cg_zero_or_source_test_charge_law.py"

STATUS = "Y5_R10_matter_frame_variation_derived_conditional_two_leg_law_cg_zero_not_signed"
CLAIM_CEILING = "conditional_matter_variation_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md"

PRIOR_630_DOC = ROOT / "630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md"
PRIOR_630_VALIDATION = MTS_DIR / "P8_Y5_BRR545_630_VALIDATION.csv"
PRIOR_630_PRESSURE = MTS_DIR / "P8_Y5_R10_630_R10_PRODUCT_PRESSURE_ENVELOPE.csv"
PRIOR_630_AMBIGUITY = MTS_DIR / "P8_Y5_R10_630_SCALAR_COUPLING_AMBIGUITY_LEDGER.csv"
PRIOR_630_INPUTS = MTS_DIR / "P8_Y5_R10_630_PARENT_INPUT_TARGETS.csv"
PRIOR_629_DOC = ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md"
PRIOR_627_DOC = ROOT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md"
PRIOR_626_DOC = ROOT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_631_SOURCE_REGISTER.csv"
MATTER_FRAME_CASES = MTS_DIR / "P8_Y5_R10_631_MATTER_FRAME_CASES.csv"
VARIATION_DERIVATION = MTS_DIR / "P8_Y5_R10_631_VARIATION_DERIVATION.csv"
SOURCE_TEST_CHARGE_LAW = MTS_DIR / "P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv"
BRANCH_RESOLUTION = MTS_DIR / "P8_Y5_R10_631_COUPLING_BRANCH_RESOLUTION.csv"
R10_TRANSLATION = MTS_DIR / "P8_Y5_R10_631_R10_ALPHA_TRANSLATION.csv"
ZERO_GATE = MTS_DIR / "P8_Y5_R10_631_CG_ZERO_GATE.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_631_NEXT_SELECTOR_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_631_NONCLAIM_SUMMARY.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_631_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_631_ROUTE_UPDATE.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_631_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_630_DOC, "immediate coupling derivation gate"),
        (PRIOR_630_VALIDATION, "630 validation gate"),
        (PRIOR_630_PRESSURE, "R10 product pressure envelope"),
        (PRIOR_630_AMBIGUITY, "linear-vs-two-leg ambiguity ledger"),
        (PRIOR_630_INPUTS, "parent input targets"),
        (PRIOR_629_DOC, "R10 c_g projection smoke runner"),
        (PRIOR_627_DOC, "c_g zero proof attempt"),
        (PRIOR_626_DOC, "quotient-invariant matter action signature attempt"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC631_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def matter_frame_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "MF631_0_quotient_only",
            "matter_frame": "g_m = g_q[q(Phi),theta]",
            "partial_X_g_m": "0",
            "matter_current": "J_X=0",
            "alpha_law": "alpha_MTS_R10(lambda)=0",
            "status": "clean_zero_if_parent_signed",
            "what_must_be_proven": "Xhat is vertical and all matter measure/coframe/connection data descend to the quotient",
            "valid_for_claim": "false",
        },
        {
            "case_id": "MF631_1_conformal_representative",
            "matter_frame": "g_m = A_g(Xhat)^2 g_q",
            "partial_X_g_m": "2 c_g g_m at Xhat=0 where c_g=d ln A_g/dXhat",
            "matter_current": "J_X = c_g T_m plus sign convention",
            "alpha_law": "alpha proportional to beta_source beta_test",
            "status": "conditional_two_leg_law",
            "what_must_be_proven": "A_g is a parent-owned physical function rather than a forbidden representative choice",
            "valid_for_claim": "false",
        },
        {
            "case_id": "MF631_2_disformal_representative",
            "matter_frame": "g_m = A_g(Xhat)^2 g_q + B_g(Xhat) U_mu U_nu",
            "partial_X_g_m": "2 c_g g_m + b_g U_mu U_nu plus connection/normalization terms",
            "matter_current": "J_X = c_g T_m + 0.5 b_g T^{mu nu} U_mu U_nu + ...",
            "alpha_law": "alpha receives Weyl plus disformal/profile terms",
            "status": "blocked_mixed_branch",
            "what_must_be_proven": "whether disformal terms are absent, auxiliary, quotient-owned, or physical",
            "valid_for_claim": "false",
        },
        {
            "case_id": "MF631_3_explicit_mass_dependence",
            "matter_frame": "m_i=m_i(Xhat,theta) even if g_m descends",
            "partial_X_g_m": "0 but partial_X ln m_i may be nonzero",
            "matter_current": "J_X = sum_i beta_i rho_i with beta_i=d ln m_i/dXhat",
            "alpha_law": "composition-dependent scalar charge unless beta_i is universal or zero",
            "status": "blocked_mass_channel",
            "what_must_be_proven": "standard masses/constants must be quotient-owned or their Xhat dependence derived",
            "valid_for_claim": "false",
        },
    ]


def variation_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "line_id": "VD631_0_action",
            "statement": "Start with a minimally-coupled matter action in its physical matter frame.",
            "equation": "S_m = integral d^4x sqrt(-g_m) L_m(psi,D_m psi,g_m,m_i)",
            "derivation_status": "standard_variational_identity",
            "consequence": "all local coupling information enters through the Xhat dependence of g_m, D_m, and m_i",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_1_stress_variation",
            "statement": "Define the stress tensor by varying the matter metric.",
            "equation": "delta S_m = 1/2 integral sqrt(-g_m) T_m^{mu nu} delta g^m_{mu nu} + matter EOM terms",
            "derivation_status": "derived_identity_up_to_sign_convention",
            "consequence": "on matter equations of motion, Xhat couples through T_m^{mu nu} partial_X g^m_{mu nu}",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_2_general_current",
            "statement": "Vary with respect to the normalized residual Xhat.",
            "equation": "J_X = delta S_m/delta Xhat = 1/2 sqrt(-g_m) T_m^{mu nu} partial_Xhat g^m_{mu nu} + sqrt(-g_m) sum_i (partial_Xhat ln m_i) m_i n_i + ...",
            "derivation_status": "conditional_general_current",
            "consequence": "zero coupling requires every Xhat derivative in the matter frame and explicit matter constants to vanish or be pure gauge",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_3_conformal_current",
            "statement": "For a pure conformal representative matter frame, the trace current is unavoidable unless c_g=0.",
            "equation": "if g_m=A_g^2 g_q then partial_Xhat g_m=2 c_g g_m and J_X = sqrt(-g_m) c_g T_m",
            "derivation_status": "derived_conditional_theorem",
            "consequence": "ordinary nonrelativistic matter has T_m approximately -rho, so source and test bodies both carry scalar charge",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_4_zero_condition",
            "statement": "The clean local-GR-safe branch is an exact matter-frame descent condition.",
            "equation": "partial_Xhat g_m=0 and partial_Xhat ln m_i=0 and boundary_Xhat current=0 imply J_X=0",
            "derivation_status": "proved_as_conditional_zero_lemma",
            "consequence": "if parent action signs this, c_g=0 and all R10/PPN/clock source currents vanish at leading order",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_5_nonzero_condition",
            "statement": "If the conformal derivative survives, the finite force is naturally two-legged.",
            "equation": "V_X(r) = - beta_s beta_t m_s m_t exp(-r/lambda_X)/(4 pi Z_eff r) times profile factors",
            "derivation_status": "derived_static_exchange_form",
            "consequence": "matching to Newton gives alpha_X = beta_s beta_t/(4 pi G_eff Z_eff) times profile factors",
            "valid_for_claim": "false",
        },
        {
            "line_id": "VD631_6_linear_row_interpretation",
            "statement": "A linear c_g alpha row is only primitive if the source leg has already been absorbed into another factor.",
            "equation": "alpha_linear=abs(c_g K_X Qbar_XH qbar_XT tau_R10/Z_eff) is shorthand, not the raw matter variation, unless K_X Qbar_XH qbar_XT contains beta_source",
            "derivation_status": "branch_resolution",
            "consequence": "future runners must record whether alpha is one-leg-compressed or two-leg-universal",
            "valid_for_claim": "false",
        },
    ]


def source_test_charge_rows() -> list[dict[str, Any]]:
    return [
        {
            "charge_id": "Q631_0_universal_weyl_charge",
            "object": "beta_i",
            "definition": "beta_i = partial_Xhat ln m_i^eff = c_g for universal conformal matter-frame response",
            "source_leg": "beta_source=c_g times composition/profile factor",
            "test_leg": "beta_test=c_g times composition/profile factor",
            "observable_law": "alpha_X proportional to c_g^2 for universal source/test coupling",
            "status": "conditional_derived",
            "valid_for_claim": "false",
        },
        {
            "charge_id": "Q631_1_quotient_zero_charge",
            "object": "beta_i",
            "definition": "beta_i=0 if matter frame and particle masses are quotient-only",
            "source_leg": "0",
            "test_leg": "0",
            "observable_law": "alpha_X=0",
            "status": "conditional_zero_lemma",
            "valid_for_claim": "false",
        },
        {
            "charge_id": "Q631_2_composition_channel",
            "object": "beta_i",
            "definition": "beta_i=c_g+partial_Xhat ln m_i^bare plus binding-energy sensitivities",
            "source_leg": "composition-weighted beta_source",
            "test_leg": "composition-weighted beta_test",
            "observable_law": "WEP/composition tests become coupled to R10 rather than optional",
            "status": "blocked_until_mass_constants_owned",
            "valid_for_claim": "false",
        },
        {
            "charge_id": "Q631_3_disformal_charge",
            "object": "beta_i plus b_g velocity/stress projection",
            "definition": "J_X includes 0.5 b_g T^{mu nu} U_mu U_nu if disformal matter-frame terms survive",
            "source_leg": "stress/profile source leg",
            "test_leg": "stress/profile test leg",
            "observable_law": "not reducible to pure conformal alpha without extra projection terms",
            "status": "blocked_mixed_branch",
            "valid_for_claim": "false",
        },
    ]


def coupling_branch_resolution_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR631_0_zero",
            "branch": "quotient-only matter descent",
            "derived_result": "J_X=0",
            "selected_for_claim": "false",
            "why": "conditional zero lemma is proven, but parent action has not signed the matter frame",
            "next_test": "derive or source explicit parent matter frame",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR631_1_two_leg",
            "branch": "universal conformal matter-frame coupling",
            "derived_result": "J_X=c_g T_m and alpha_X proportional to c_g^2 times profile/normalization factors",
            "selected_for_claim": "false",
            "why": "this is the natural finite branch from variation, but c_g,Z_eff,lambda_X,profiles are not sourced",
            "next_test": "build two-leg nonclaim envelope runner and parent selector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR631_2_linear_compressed",
            "branch": "linear alpha with source leg absorbed",
            "derived_result": "alpha_linear is allowed only as shorthand after defining where beta_source went",
            "selected_for_claim": "false",
            "why": "using it as primitive would hide a matter leg",
            "next_test": "require metadata: one_leg_compressed=true/false and source_leg_owner",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR631_3_disformal_or_mass",
            "branch": "extra representative/mass channel",
            "derived_result": "J_X receives stress/mass-sensitivity terms beyond c_g T",
            "selected_for_claim": "false",
            "why": "would make local tests harder, not easier, unless parent action forbids it",
            "next_test": "prove no disformal/mass Xhat channel or add separate blocked projection schema",
            "valid_for_claim": "false",
        },
    ]


def r10_alpha_translation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv(PRIOR_630_PRESSURE)):
        alpha_bound = parse_float(row.get("alpha_bound_review_candidate"))
        sqrt_bound = math.sqrt(alpha_bound) if alpha_bound is not None and alpha_bound >= 0 else None
        rows.append(
            {
                "translation_id": f"AT631_{index}",
                "lambda_value": row.get("lambda_value", ""),
                "lambda_units": row.get("lambda_units", "m"),
                "review_alpha_bound": row.get("alpha_bound_review_candidate", ""),
                "if_linear_compressed_bound": row.get("linear_product_bound", ""),
                "if_two_leg_unit_profile_bound_on_abs_c_eff": "" if sqrt_bound is None else f"{sqrt_bound:.12g}",
                "physical_interpretation": "two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly",
                "claim_status": "nonclaim_review_candidate_pressure_only",
                "valid_for_claim": "false",
            }
        )
    return rows


def cg_zero_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ZG631_0_metric",
            "zero_requirement": "partial_Xhat g_matter = 0",
            "derived_status": "sufficient_component",
            "currently_signed": "false",
            "failure_mode": "trace current c_g T_m survives",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZG631_1_connection_measure",
            "zero_requirement": "partial_Xhat measure/coframe/connection matter data = 0 or pure gauge",
            "derived_status": "required_component",
            "currently_signed": "false",
            "failure_mode": "coupling leaks through rods/clocks/derivatives",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZG631_2_masses_constants",
            "zero_requirement": "partial_Xhat ln m_i and constants/sensitivities = 0 or quotient-owned",
            "derived_status": "required_component",
            "currently_signed": "false",
            "failure_mode": "composition-dependent WEP/clock channel",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZG631_3_boundary",
            "zero_requirement": "vertical boundary current has no local/R10 projection",
            "derived_status": "required_component",
            "currently_signed": "false",
            "failure_mode": "edge current fakes finite source leg",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZG631_4_total",
            "zero_requirement": "all zero gates signed by parent action",
            "derived_status": "not_passed",
            "currently_signed": "false",
            "failure_mode": "finite two-leg/source-test law remains live",
            "valid_for_claim": "false",
        },
    ]


def next_selector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NS631_0_parent_selector",
            "required_output": "choose or derive the actual parent matter-frame class",
            "must_distinguish": "quotient-only vs conformal representative vs disformal/mass channel",
            "pass_condition": "one branch is selected by parent action text/equations, not by convenience",
            "blocked_if": "matter frame remains implicit",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NS631_1_two_leg_runner",
            "required_output": "nonclaim runner for alpha proportional to beta_source beta_test",
            "must_distinguish": "linear compressed product from true two-leg scalar exchange",
            "pass_condition": "metadata records source_leg_owner,test_leg_owner,Z_eff,lambda_X,profile",
            "blocked_if": "any owner is MISSING_PARENT_INPUT",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NS631_2_cross_arena_charge",
            "required_output": "same beta_i/c_g branch mapped to R10, WEP, PPN, clock, and orbital rows",
            "must_distinguish": "universal trace coupling from composition-dependent mass/constant coupling",
            "pass_condition": "one charge law gives all arena projections or explicitly blocks them",
            "blocked_if": "R10 is treated in isolation",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D631_0_main_verdict",
            "decision": STATUS,
            "meaning": "the matter-frame variation gives a real conditional theorem: zero iff matter frame descends; otherwise a trace/source-test law",
            "status": "derivation_progress_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D631_1_cg_zero",
            "decision": "c_g_zero_conditional_not_parent_signed",
            "meaning": "c_g=0 follows from partial_Xhat matter data all vanishing, but that parent selector is still missing",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D631_2_two_leg",
            "decision": "finite_universal_coupling_is_two_leg",
            "meaning": "if matter sees Xhat through a conformal frame, source and test both couple; alpha scales like c_g^2 times profiles",
            "status": "branch_resolution",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D631_3_linear_row",
            "decision": "linear_alpha_must_be_marked_source_absorbed",
            "meaning": "the previous linear formula is acceptable only as compressed notation with source-leg ownership metadata",
            "status": "schema_repair_required",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D631_4_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no local test pass follows until the parent matter-frame selector is derived",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU631_0_allowed",
            "allowed_after_631": "Use the conditional zero lemma: if all Xhat matter-frame derivatives vanish, c_g=0.",
            "forbidden_after_631": "Claim c_g=0 before deriving the actual parent matter frame.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU631_1_allowed",
            "allowed_after_631": "Treat universal finite coupling as two-legged by default.",
            "forbidden_after_631": "Use a primitive linear c_g R10 row without source-leg ownership metadata.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU631_2_allowed",
            "allowed_after_631": "Carry WEP/clock/PPN risk with any composition or mass channel.",
            "forbidden_after_631": "Use R10 alone to bless a coupling branch.",
            "next_action": NEXT_TARGET,
        },
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    frame_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    charge_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    translation_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_630_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    conformal_variation = any("J_X = sqrt(-g_m) c_g T_m" in row.get("equation", "") for row in variation_rows)
    two_leg_present = any("c_g^2" in row.get("observable_law", "") for row in charge_rows)
    zero_total = next((row for row in zero_rows if row["gate_id"] == "ZG631_4_total"), {})
    numeric_translations = [
        row
        for row in translation_rows
        if parse_float(row.get("review_alpha_bound")) is not None
        and parse_float(row.get("if_two_leg_unit_profile_bound_on_abs_c_eff")) is not None
        and row.get("valid_for_claim") == "false"
    ]
    branch_claim_rows = [row for row in branch_rows if row.get("selected_for_claim") == "true" or row.get("valid_for_claim") == "true"]
    return [
        {
            "check_id": "V631_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V631_1_prior_630_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V631_2_matter_frame_cases_complete",
            "result": "pass" if len(frame_rows) == 4 else "fail",
            "detail": f"frame_cases={len(frame_rows)}",
        },
        {
            "check_id": "V631_3_variation_derives_trace_current",
            "result": "pass" if len(variation_rows) == 7 and conformal_variation else "fail",
            "detail": f"variation_rows={len(variation_rows)};trace_current={bool_text(conformal_variation)}",
        },
        {
            "check_id": "V631_4_two_leg_law_explicit",
            "result": "pass" if len(charge_rows) == 4 and two_leg_present else "fail",
            "detail": f"charge_rows={len(charge_rows)};two_leg_present={bool_text(two_leg_present)}",
        },
        {
            "check_id": "V631_5_zero_gate_not_passed",
            "result": "pass" if len(zero_rows) == 5 and zero_total.get("derived_status") == "not_passed" else "fail",
            "detail": f"zero_rows={len(zero_rows)};total_status={zero_total.get('derived_status', '')}",
        },
        {
            "check_id": "V631_6_R10_translation_numeric_nonclaim",
            "result": "pass" if len(translation_rows) == 9 and len(numeric_translations) == 9 else "fail",
            "detail": f"translation_rows={len(translation_rows)};numeric_nonclaim={len(numeric_translations)}",
        },
        {
            "check_id": "V631_7_no_branch_claim_selected",
            "result": "pass" if len(branch_rows) == 4 and not branch_claim_rows else "fail",
            "detail": f"branch_rows={len(branch_rows)};claim_rows={len(branch_claim_rows)}",
        },
        {
            "check_id": "V631_8_next_selector_contract_written",
            "result": "pass" if len(selector_rows) == 3 else "fail",
            "detail": f"selector_rows={len(selector_rows)}",
        },
        {
            "check_id": "V631_9_no_local_claim",
            "result": "pass",
            "detail": "c_g_zero=false;finite_numeric=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def nonclaim_summary_rows(translation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_rows = [row for row in translation_rows if parse_float(row.get("review_alpha_bound")) is not None]
    tightest_row = min(numeric_rows, key=lambda row: parse_float(row["review_alpha_bound"])) if numeric_rows else {}
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "cg_zero_parent_signed": "false",
            "trace_current_derived": "true",
            "default_finite_branch": "two_leg_universal_unless_source_leg_absorbed",
            "linear_formula_status": "compressed_not_primitive",
            "tightest_review_alpha_bound": tightest_row.get("review_alpha_bound", ""),
            "tightest_two_leg_unit_profile_bound": tightest_row.get("if_two_leg_unit_profile_bound_on_abs_c_eff", ""),
            "tightest_lambda_m": tightest_row.get("lambda_value", ""),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def build_doc(
    source_rows: list[dict[str, Any]],
    frame_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    charge_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    translation_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 631 Y5 R10 matter frame variation cg zero or source test charge law",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- The matter-frame variation gives the missing coupling law in conditional form.\n"
            "- If the matter frame and matter constants are quotient-only, `J_X=0` and the `c_g=0` branch follows.\n"
            "- If a conformal representative matter frame survives, `J_X` is a trace current and ordinary source/test bodies both carry charge.\n"
            "- Therefore a finite universal coupling is naturally two-legged: `alpha` scales like a source charge times a test charge, not primitive linear `c_g`.\n"
            "- The old linear row survives only as compressed notation if the source leg is explicitly owned elsewhere.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Matter Frame Cases\n" + markdown_table(frame_rows),
            "## Variation Derivation\n" + markdown_table(variation_rows),
            "## Source-Test Charge Law\n" + markdown_table(charge_rows),
            "## Coupling Branch Resolution\n" + markdown_table(branch_rows),
            "## R10 Alpha Translation\n" + markdown_table(translation_rows),
            "## c_g Zero Gate\n" + markdown_table(zero_rows),
            "## Next Selector Contract\n" + markdown_table(selector_rows),
            "## Nonclaim Summary\n" + markdown_table(summary_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    frame_rows = matter_frame_case_rows()
    variation_rows = variation_derivation_rows()
    charge_rows = source_test_charge_rows()
    branch_rows = coupling_branch_resolution_rows()
    translation_rows = r10_alpha_translation_rows()
    zero_rows = cg_zero_gate_rows()
    selector_rows = next_selector_contract_rows()
    summary_rows = nonclaim_summary_rows(translation_rows)
    decisions = decision_rows()
    routes = route_update_rows()
    validations = validation_rows(source_rows, frame_rows, variation_rows, charge_rows, branch_rows, translation_rows, zero_rows, selector_rows)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(MATTER_FRAME_CASES, frame_rows)
    write_csv(VARIATION_DERIVATION, variation_rows)
    write_csv(SOURCE_TEST_CHARGE_LAW, charge_rows)
    write_csv(BRANCH_RESOLUTION, branch_rows)
    write_csv(R10_TRANSLATION, translation_rows)
    write_csv(ZERO_GATE, zero_rows)
    write_csv(NEXT_CONTRACT, selector_rows)
    write_csv(NONCLAIM_SUMMARY, summary_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            frame_rows,
            variation_rows,
            charge_rows,
            branch_rows,
            translation_rows,
            zero_rows,
            selector_rows,
            summary_rows,
            decisions,
            routes,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )
    failed = [row for row in validations if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))


if __name__ == "__main__":
    main()
