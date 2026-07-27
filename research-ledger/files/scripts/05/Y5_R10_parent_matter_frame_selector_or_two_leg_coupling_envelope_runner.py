from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_parent_matter_frame_selector_or_two_leg_coupling_envelope_runner.py"

STATUS = "Y5_R10_parent_matter_frame_not_selected_two_leg_envelope_runner_built_nonclaim"
CLAIM_CEILING = "selector_and_two_leg_envelope_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "633-Y5-R10-parent-matter-frame-source-search-or-zero-branch-closure.md"

PRIOR_631_DOC = ROOT / "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md"
PRIOR_631_VALIDATION = MTS_DIR / "P8_Y5_BRR545_631_VALIDATION.csv"
PRIOR_631_FRAME_CASES = MTS_DIR / "P8_Y5_R10_631_MATTER_FRAME_CASES.csv"
PRIOR_631_BRANCH = MTS_DIR / "P8_Y5_R10_631_COUPLING_BRANCH_RESOLUTION.csv"
PRIOR_631_TRANSLATION = MTS_DIR / "P8_Y5_R10_631_R10_ALPHA_TRANSLATION.csv"
PRIOR_631_ZERO_GATE = MTS_DIR / "P8_Y5_R10_631_CG_ZERO_GATE.csv"
PRIOR_631_SELECTOR = MTS_DIR / "P8_Y5_R10_631_NEXT_SELECTOR_CONTRACT.csv"
PRIOR_630_DOC = ROOT / "630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md"
PRIOR_629_DOC = ROOT / "629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_632_SOURCE_REGISTER.csv"
PARENT_SELECTOR_AUDIT = MTS_DIR / "P8_Y5_R10_632_PARENT_MATTER_FRAME_SELECTOR_AUDIT.csv"
BRANCH_SELECTION = MTS_DIR / "P8_Y5_R10_632_BRANCH_SELECTION_STATUS.csv"
TWO_LEG_SCHEMA = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_SCHEMA.csv"
TWO_LEG_ENVELOPE = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv"
LINEAR_REPAIR = MTS_DIR / "P8_Y5_R10_632_LINEAR_COMPRESSED_METADATA_REPAIR.csv"
CROSS_ARENA = MTS_DIR / "P8_Y5_R10_632_CROSS_ARENA_RISK_MATRIX.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_632_NEXT_SOURCE_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_632_NONCLAIM_SUMMARY.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_632_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_632_ROUTE_UPDATE.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_632_VALIDATION.csv"

PROFILE_FACTORS = [0.01, 0.1, 1.0, 10.0]


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
        (PRIOR_631_DOC, "immediate matter-frame variation checkpoint"),
        (PRIOR_631_VALIDATION, "631 validation gate"),
        (PRIOR_631_FRAME_CASES, "matter-frame cases"),
        (PRIOR_631_BRANCH, "branch resolution status"),
        (PRIOR_631_TRANSLATION, "R10 alpha translation into two-leg bounds"),
        (PRIOR_631_ZERO_GATE, "c_g zero gate"),
        (PRIOR_631_SELECTOR, "next selector contract"),
        (PRIOR_630_DOC, "coupling derivation gate"),
        (PRIOR_629_DOC, "R10 pressure smoke runner"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC632_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def parent_selector_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_id": "SEL632_0_quotient_only",
            "candidate_branch": "quotient_only_zero",
            "parent_requirement": "g_matter, measure, coframe, connection, particle masses, constants, and boundary currents are quotient-owned with no Xhat derivative",
            "evidence_available": "conditional lemma from 631, but no explicit parent matter-frame source",
            "selector_result": "not_selected_for_claim",
            "working_role": "preferred_target_for_local_GR_if_parent_signed",
            "why_not_selected": "parent action has not signed all zero gates",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "SEL632_1_universal_conformal",
            "candidate_branch": "universal_two_leg_conformal",
            "parent_requirement": "g_matter=A_g(Xhat)^2 g_q with A_g parent-owned and no disformal/mass channels",
            "evidence_available": "variation theorem derives J_X=c_g T_m if this frame is selected",
            "selector_result": "selected_for_nonclaim_runner_only",
            "working_role": "default_finite_branch_if_zero_route_fails",
            "why_not_selected": "c_g,Z_eff,lambda_X,profile factors are unsourced",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "SEL632_2_linear_compressed",
            "candidate_branch": "linear_source_absorbed",
            "parent_requirement": "source leg is explicitly owned by K_X/Qbar_XH/qbar_XT metadata",
            "evidence_available": "631 allows it only as compressed notation",
            "selector_result": "schema_repair_required",
            "working_role": "not_primitive",
            "why_not_selected": "would hide source/test leg unless repaired",
            "valid_for_claim": "false",
        },
        {
            "selector_id": "SEL632_3_disformal_mass",
            "candidate_branch": "mixed_disformal_or_mass_channel",
            "parent_requirement": "B_g, U_mu U_nu, particle masses, binding energies, and constants are either absent/quotient-owned or separately projected",
            "evidence_available": "631 identifies this as extra local-test risk",
            "selector_result": "blocked_mixed_branch",
            "working_role": "do_not_score_inside_conformal_cg",
            "why_not_selected": "could generate WEP/clock/PPN leakage not captured by R10 envelope",
            "valid_for_claim": "false",
        },
    ]


def branch_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BS632_0_claim_selected",
            "question": "Is any matter-frame branch parent-selected for claim?",
            "answer": "false",
            "selected_branch": "none",
            "reason": "no explicit parent matter-frame source signs quotient-only, conformal, or mixed branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BS632_1_private_zero_target",
            "question": "Which branch should be tried first for local GR?",
            "answer": "quotient_only_zero",
            "selected_branch": "private_derivation_target",
            "reason": "it is the only branch that naturally makes R10/PPN/clock/orbital silent",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BS632_2_private_finite_runner",
            "question": "Which finite branch gets a nonclaim runner?",
            "answer": "universal_two_leg_conformal",
            "selected_branch": "private_runner_default",
            "reason": "631 variation shows finite universal matter coupling is two-legged by default",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BS632_3_public_status",
            "question": "Can any local test pass be claimed?",
            "answer": "false",
            "selected_branch": "none",
            "reason": "review curve remains nonclaim and theory inputs remain unsourced",
            "valid_for_claim": "false",
        },
    ]


def two_leg_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "TLS632_0_effective_coupling",
            "field": "c_eff",
            "definition": "dimensionless effective source/test coupling after absorbing 4 pi G_eff Z_eff normalization",
            "equation": "alpha_X(lambda)=profile_factor(lambda)*c_eff_source(lambda)*c_eff_test(lambda)",
            "required_owner": "parent matter-frame selector plus Z_eff/profile normalization",
            "status": "nonclaim_runner_variable",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TLS632_1_universal_case",
            "field": "universal_two_leg",
            "definition": "c_eff_source=c_eff_test=c_eff",
            "equation": "|c_eff| <= sqrt(alpha_bound/profile_factor)",
            "required_owner": "universal composition-independent matter-frame coupling",
            "status": "computed_as_private_pressure",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TLS632_2_profile_factor",
            "field": "profile_factor",
            "definition": "positive dimensionless package of source geometry, range response, and normalization not yet parent-sourced",
            "equation": "profile_factor in {0.01,0.1,1,10} for pressure sensitivity only",
            "required_owner": "Qbar_XH(lambda;lambda_X), tau_R10(lambda), Z_eff, material geometry",
            "status": "scan_not_fit",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "TLS632_3_claim_gate",
            "field": "claim_allowed",
            "definition": "true only if parent branch, profile factors, R10 curve, and source/test charges are all source-backed",
            "equation": "claim_allowed=false while any row has valid_for_claim=false or MISSING_PARENT_INPUT",
            "required_owner": "future promoted source files",
            "status": "hard_block",
            "valid_for_claim": "false",
        },
    ]


def two_leg_envelope_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    translations = read_csv(PRIOR_631_TRANSLATION)
    for translation in translations:
        alpha_bound = parse_float(translation.get("review_alpha_bound"))
        for profile_factor in PROFILE_FACTORS:
            if alpha_bound is None or alpha_bound < 0 or profile_factor <= 0:
                bound = ""
                status = "not_numeric"
            else:
                bound = f"{math.sqrt(alpha_bound / profile_factor):.12g}"
                status = "numeric_nonclaim"
            rows.append(
                {
                    "envelope_id": f"TE632_{len(rows)}",
                    "translation_id": translation.get("translation_id", ""),
                    "lambda_value": translation.get("lambda_value", ""),
                    "lambda_units": "m",
                    "review_alpha_bound": translation.get("review_alpha_bound", ""),
                    "profile_factor": f"{profile_factor:.12g}",
                    "universal_two_leg_bound_abs_c_eff": bound,
                    "law": "alpha_X=profile_factor*c_eff^2",
                    "runner_status": status,
                    "source": rel(PRIOR_631_TRANSLATION),
                    "valid_for_claim": "false",
                }
            )
    return rows


def linear_repair_rows() -> list[dict[str, Any]]:
    return [
        {
            "repair_id": "LR632_0_source_leg_owner",
            "required_metadata": "source_leg_owner",
            "allowed_values": "explicit_beta_source|absorbed_in_KX_Qbar_qbar|zero_by_descent|missing",
            "current_status": "missing",
            "why_required": "linear alpha can only be shorthand if the source leg is not silently dropped",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "LR632_1_test_leg_owner",
            "required_metadata": "test_leg_owner",
            "allowed_values": "explicit_beta_test|absorbed_in_qbar_XT|zero_by_descent|missing",
            "current_status": "missing",
            "why_required": "R10 force compares source-test interaction, not a one-body readout alone",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "LR632_2_compression_flag",
            "required_metadata": "one_leg_compressed",
            "allowed_values": "true|false",
            "current_status": "missing",
            "why_required": "distinguishes primitive two-leg scalar exchange from compressed product notation",
            "valid_for_claim": "false",
        },
        {
            "repair_id": "LR632_3_units_normalization",
            "required_metadata": "normalization_owner",
            "allowed_values": "Z_eff_4piG|KX_absorbed|dimensionless_prior|missing",
            "current_status": "missing",
            "why_required": "prevents arbitrary rescaling of c_g into K_X or Z_eff",
            "valid_for_claim": "false",
        },
    ]


def cross_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "CA632_0_R10",
            "arena": "short_range_inverse_square",
            "zero_branch_result": "silent if quotient-only",
            "two_leg_result": "bounded by R10 alpha(lambda) envelope once curve/profile are promoted",
            "mixed_branch_risk": "material/profile dependence",
            "status": "nonclaim_pressure_available",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CA632_1_WEP",
            "arena": "composition_equivalence_principle",
            "zero_branch_result": "silent if masses/constants quotient-owned",
            "two_leg_result": "universal trace coupling may be composition-safe only if beta_i universal",
            "mixed_branch_risk": "composition-dependent beta_i or binding-energy sensitivity",
            "status": "blocked_until_charge_law_owned",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CA632_2_PPN",
            "arena": "solar_system_PPN",
            "zero_branch_result": "local GR-safe if fully silent",
            "two_leg_result": "scalar-tensor-like gamma/beta pressure if long-enough range/profile survives",
            "mixed_branch_risk": "frame/clock/connection leakage",
            "status": "blocked_until_tau_PPN_and_lambda_X",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CA632_3_CLOCK",
            "arena": "clock_constants_redshift",
            "zero_branch_result": "silent if constants and masses are quotient-owned",
            "two_leg_result": "universal metric coupling may still affect redshift only through GR metric if quotient-selected",
            "mixed_branch_risk": "alpha_dot/alpha or mass ratio sensitivity",
            "status": "blocked_until_constants_channel_proven_absent",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "CA632_4_ORBITAL",
            "arena": "orbital_lunar_binary",
            "zero_branch_result": "silent if no finite residual force",
            "two_leg_result": "range-dependent fifth-force/orbital drift pressure",
            "mixed_branch_risk": "profile and self-energy sensitivities",
            "status": "blocked_until_tau_orbital_and_lambda_X",
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC632_0_parent_source_search",
            "required_output": "explicit parent matter-frame source line/equation or new closure axiom",
            "success_condition": "one of quotient-only, conformal two-leg, mixed/disformal, or mass-channel branch is signed",
            "if_success": "632 runner can be rerun with selected_branch metadata",
            "if_fail": "local coupling remains closure-only",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC632_1_zero_branch_closure",
            "required_output": "prove all c_g zero gates from parent action",
            "success_condition": "partial_Xhat matter-frame, constants, connection, and boundary currents vanish",
            "if_success": "local branch can pursue GR reduction without R10 fifth-force pressure",
            "if_fail": "finite two-leg branch remains live",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC632_2_two_leg_numeric_inputs",
            "required_output": "Z_eff, lambda_X, profile_factor(lambda), beta_source, beta_test",
            "success_condition": "every factor has owner equation, units, and source path",
            "if_success": "private numeric nonclaim scan becomes meaningful",
            "if_fail": "envelope remains pressure-only",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D632_0_main_verdict",
            "decision": STATUS,
            "meaning": "no parent matter-frame branch is selected for claim, but the finite branch now has a two-leg pressure runner",
            "status": "progress_but_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D632_1_zero_target",
            "decision": "quotient_only_zero_remains_best_GR_route",
            "meaning": "zero branch is the cleanest route to local GR but still requires parent source/signature",
            "status": "derive_first",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D632_2_finite_default",
            "decision": "two_leg_conformal_is_default_finite_runner",
            "meaning": "finite universal coupling is not treated as primitive linear c_g",
            "status": "runner_built_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D632_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no R10/WEP/PPN/clock/orbital/local-GR pass follows from selector or envelope rows",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU632_0_allowed",
            "allowed_after_632": "Pursue quotient-only parent matter-frame proof as the clean GR route.",
            "forbidden_after_632": "Call quotient-only selected without parent source/signature.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU632_1_allowed",
            "allowed_after_632": "Use two-leg envelope as private pressure for finite coupling.",
            "forbidden_after_632": "Treat profile-factor scan as a fit or public bound.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU632_2_allowed",
            "allowed_after_632": "Require source/test ownership metadata before any linear row is scored.",
            "forbidden_after_632": "Hide source leg in K_X/Qbar/qbar without saying so.",
            "next_action": NEXT_TARGET,
        },
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_631_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_selector_rows = [row for row in selector_rows if row.get("valid_for_claim") == "true" or row.get("selector_result") == "selected_for_claim"]
    numeric_envelope_rows = [
        row
        for row in envelope_rows
        if parse_float(row.get("review_alpha_bound")) is not None
        and parse_float(row.get("profile_factor")) is not None
        and parse_float(row.get("universal_two_leg_bound_abs_c_eff")) is not None
        and row.get("valid_for_claim") == "false"
    ]
    tightest_unit = [
        row
        for row in envelope_rows
        if row.get("profile_factor") == "1" and parse_float(row.get("universal_two_leg_bound_abs_c_eff")) is not None
    ]
    tightest_unit_value = min((parse_float(row["universal_two_leg_bound_abs_c_eff"]) for row in tightest_unit), default=None)
    linear_source_owner_required = any(row.get("required_metadata") == "source_leg_owner" for row in repair_rows)
    return [
        {
            "check_id": "V632_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V632_1_prior_631_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V632_2_parent_selector_no_claim",
            "result": "pass" if len(selector_rows) == 4 and not claim_selector_rows else "fail",
            "detail": f"selector_rows={len(selector_rows)};claim_rows={len(claim_selector_rows)}",
        },
        {
            "check_id": "V632_3_branch_status_has_zero_and_two_leg",
            "result": "pass" if len(branch_rows) == 4 and any(row.get("answer") == "quotient_only_zero" for row in branch_rows) and any(row.get("answer") == "universal_two_leg_conformal" for row in branch_rows) else "fail",
            "detail": f"branch_rows={len(branch_rows)}",
        },
        {
            "check_id": "V632_4_two_leg_schema_complete",
            "result": "pass" if len(schema_rows) == 4 and all(row.get("valid_for_claim") == "false" for row in schema_rows) else "fail",
            "detail": f"schema_rows={len(schema_rows)}",
        },
        {
            "check_id": "V632_5_two_leg_envelope_numeric_nonclaim",
            "result": "pass" if len(envelope_rows) == 36 and len(numeric_envelope_rows) == 36 and tightest_unit_value is not None and tightest_unit_value < 0.05 else "fail",
            "detail": f"envelope_rows={len(envelope_rows)};numeric_nonclaim={len(numeric_envelope_rows)};tightest_unit={tightest_unit_value}",
        },
        {
            "check_id": "V632_6_linear_metadata_repair_blocks_primitive_linear",
            "result": "pass" if len(repair_rows) == 4 and linear_source_owner_required else "fail",
            "detail": f"repair_rows={len(repair_rows)};source_owner_required={bool_text(linear_source_owner_required)}",
        },
        {
            "check_id": "V632_7_cross_arena_risk_complete",
            "result": "pass" if len(arena_rows) == 5 and all(row.get("valid_for_claim") == "false" for row in arena_rows) else "fail",
            "detail": f"arena_rows={len(arena_rows)}",
        },
        {
            "check_id": "V632_8_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V632_9_no_local_claim",
            "result": "pass",
            "detail": "selected_claim_branch=none;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def nonclaim_summary_rows(envelope_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unit_rows = [
        row
        for row in envelope_rows
        if row.get("profile_factor") == "1" and parse_float(row.get("universal_two_leg_bound_abs_c_eff")) is not None
    ]
    tightest = min(unit_rows, key=lambda row: parse_float(row["universal_two_leg_bound_abs_c_eff"])) if unit_rows else {}
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "parent_branch_selected_for_claim": "false",
            "private_zero_target": "quotient_only_zero",
            "private_finite_runner": "universal_two_leg_conformal",
            "envelope_rows": len(envelope_rows),
            "tightest_unit_profile_lambda_m": tightest.get("lambda_value", ""),
            "tightest_unit_profile_abs_c_eff_bound": tightest.get("universal_two_leg_bound_abs_c_eff", ""),
            "linear_formula_status": "blocked_until_source_test_metadata",
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
    selector_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 632 Y5 R10 parent matter frame selector or two leg coupling envelope runner",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- No parent matter-frame branch can be selected for claim yet.\n"
            "- The best local-GR route remains the quotient-only zero branch, but it needs a parent source/signature.\n"
            "- If the zero branch fails, the finite default is the two-leg conformal runner, not primitive linear `c_g`.\n"
            "- The two-leg envelope is now executable as a private pressure tool across profile-factor sensitivities.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Parent Matter-Frame Selector Audit\n" + markdown_table(selector_rows),
            "## Branch Selection Status\n" + markdown_table(branch_rows),
            "## Two-Leg Envelope Schema\n" + markdown_table(schema_rows),
            "## Two-Leg Envelope Runner\n" + markdown_table(envelope_rows),
            "## Linear Compressed Metadata Repair\n" + markdown_table(repair_rows),
            "## Cross-Arena Risk Matrix\n" + markdown_table(arena_rows),
            "## Next Source Contract\n" + markdown_table(contract_rows),
            "## Nonclaim Summary\n" + markdown_table(summary_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    selector_rows = parent_selector_audit_rows()
    branch_rows = branch_selection_rows()
    schema_rows = two_leg_schema_rows()
    envelope_rows = two_leg_envelope_rows()
    repair_rows = linear_repair_rows()
    arena_rows = cross_arena_rows()
    contract_rows = next_contract_rows()
    summary_rows = nonclaim_summary_rows(envelope_rows)
    decisions = decision_rows()
    routes = route_update_rows()
    validations = validation_rows(source_rows, selector_rows, branch_rows, schema_rows, envelope_rows, repair_rows, arena_rows, contract_rows)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(PARENT_SELECTOR_AUDIT, selector_rows)
    write_csv(BRANCH_SELECTION, branch_rows)
    write_csv(TWO_LEG_SCHEMA, schema_rows)
    write_csv(TWO_LEG_ENVELOPE, envelope_rows)
    write_csv(LINEAR_REPAIR, repair_rows)
    write_csv(CROSS_ARENA, arena_rows)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            selector_rows,
            branch_rows,
            schema_rows,
            envelope_rows,
            repair_rows,
            arena_rows,
            contract_rows,
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
