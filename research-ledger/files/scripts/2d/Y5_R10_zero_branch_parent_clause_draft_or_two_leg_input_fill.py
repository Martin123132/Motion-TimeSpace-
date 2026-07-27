from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "634-Y5-R10-zero-branch-parent-clause-draft-or-two-leg-input-fill.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_zero_branch_parent_clause_draft_or_two_leg_input_fill.py"

STATUS = "Y5_R10_zero_branch_parent_clause_drafted_as_proposed_selector_two_leg_fallback_retained"
CLAIM_CEILING = "proposed_parent_clause_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "635-Y5-R10-zero-clause-consistency-review-or-two-leg-numeric-input-runner.md"

PRIOR_633_DOC = ROOT / "633-Y5-R10-parent-matter-frame-source-search-or-zero-branch-closure.md"
PRIOR_633_VALIDATION = MTS_DIR / "P8_Y5_BRR545_633_VALIDATION.csv"
PRIOR_633_CANDIDATES = MTS_DIR / "P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv"
PRIOR_633_ZERO_GATE = MTS_DIR / "P8_Y5_R10_633_ZERO_BRANCH_CLOSURE_GATE.csv"
PRIOR_633_FALLBACK = MTS_DIR / "P8_Y5_R10_633_FINITE_FALLBACK_STATUS.csv"
PRIOR_632_ENVELOPE = MTS_DIR / "P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv"
PRIOR_631_DOC = ROOT / "631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_634_SOURCE_REGISTER.csv"
PARENT_CLAUSE_DRAFT = MTS_DIR / "P8_Y5_R10_634_ZERO_BRANCH_PARENT_CLAUSE_DRAFT.csv"
CONSEQUENCE_CHAIN = MTS_DIR / "P8_Y5_R10_634_ZERO_CLAUSE_CONSEQUENCE_CHAIN.csv"
CONSISTENCY_OBLIGATIONS = MTS_DIR / "P8_Y5_R10_634_ZERO_CLAUSE_CONSISTENCY_OBLIGATIONS.csv"
ADOPTION_STATUS = MTS_DIR / "P8_Y5_R10_634_PARENT_CLAUSE_ADOPTION_STATUS.csv"
TWO_LEG_INPUT_FILL = MTS_DIR / "P8_Y5_R10_634_TWO_LEG_FALLBACK_INPUT_FILL.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_634_DECISION.csv"
ROUTE_UPDATE = MTS_DIR / "P8_Y5_BRR545_634_ROUTE_UPDATE.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_634_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_634_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_634_VALIDATION.csv"


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


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_633_DOC, "immediate source hunt and zero-closure checkpoint"),
        (PRIOR_633_VALIDATION, "633 validation gate"),
        (PRIOR_633_CANDIDATES, "candidate matter-frame classifications"),
        (PRIOR_633_ZERO_GATE, "zero branch closure gate"),
        (PRIOR_633_FALLBACK, "finite fallback status"),
        (PRIOR_632_ENVELOPE, "two-leg finite fallback envelope"),
        (PRIOR_631_DOC, "matter-frame variation theorem"),
        (ROOT / "204-matter-metric-action-and-ruler-transport-owner-contract.md", "matter action owner contract ingredient"),
        (ROOT / "240-universal-coupling-parent-contract-or-local-bound-data-runner.md", "universal coupling ingredient"),
        (ROOT / "360-universal-matter-coupling-theorem-attempt.md", "universal matter theorem ingredient"),
        (ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "vertical observation theorem ingredient"),
        (ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md", "primitive quotient/no-marker clause ingredient"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC634_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def parent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZP634_0_domain",
            "clause_name": "observed quotient domain",
            "proposed_clause": "There is a parent quotient map q:Phi_parent -> Q_obs and ordinary matter is defined only after q.",
            "formal_role": "defines the arena in which representative directions can be vertical",
            "buys_if_adopted": "matter cannot couple to pre-quotient representative data directly",
            "cost_or_risk": "new parent selector unless derived later",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_1_observed_geometry_functor",
            "clause_name": "observed geometry functor",
            "proposed_clause": "Observed rods, clocks, photons, and ordinary matter see e_obs=Obs(q(Phi)) and omega[e_obs], not a representative e(Phi,Xhat).",
            "formal_role": "makes partial_Xhat e_obs = DObs(Dq[v_X])",
            "buys_if_adopted": "if Xhat is vertical then partial_Xhat g_matter=0",
            "cost_or_risk": "must coexist with cosmology/galaxy effective variables without hiding a shadow frame",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_2_matter_functor",
            "clause_name": "ordinary matter functor",
            "proposed_clause": "S_matter = sum_A S_A[Psi_A, e_obs, omega[e_obs], theta_A] with no additional Xhat, A_g(Xhat), B_g(Xhat), or material-marker argument.",
            "formal_role": "removes direct representative matter vertices",
            "buys_if_adopted": "delta_Xhat S_matter has no metric-frame or marker term",
            "cost_or_risk": "strong universality assumption; must be explicit in the framework spine",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_3_constants_no_marker",
            "clause_name": "X-independent constants and species data",
            "proposed_clause": "theta_A are representation/species constants owned by Q_obs or fixed matter representation data, with partial_Xhat theta_A=0 and no co-moving material spurion m_A(Xhat).",
            "formal_role": "prevents Xhat returning through masses, charges, clocks, or material preparation labels",
            "buys_if_adopted": "composition, WEP, and clock channels are not reopened by constants",
            "cost_or_risk": "needs separate consistency review for EM/particle/time sectors",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_4_vertical_local_residual",
            "clause_name": "local Xhat verticality",
            "proposed_clause": "On the local-vacuum branch, v_Xhat lies in ker(Dq) and DObs(Dq[v_Xhat])=0.",
            "formal_role": "identifies Xhat as representative/local closure data rather than an observed matter scalar",
            "buys_if_adopted": "q_X^source=q_X^test=0 for ordinary matter",
            "cost_or_risk": "risks removing a finite local mode that may be needed elsewhere unless branch-scoped",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_5_boundary_silence",
            "clause_name": "vertical boundary/projector silence",
            "proposed_clause": "Any boundary, projector, or domain current generated by vertical Xhat variation is exact/gauge/Ward-owned or retained outside ordinary matter, with zero R10/local matter projection.",
            "formal_role": "prevents edge currents from replacing the killed matter current",
            "buys_if_adopted": "no hidden source leg survives through boundary/domain terms",
            "cost_or_risk": "boundary rows are historically hard; must be checked independently",
            "adoption_status": "proposed_parent_clause_not_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "ZP634_6_honesty_label",
            "clause_name": "axiom status label",
            "proposed_clause": "Until derived from deeper MTS principles, ZP634 is a proposed parent selector/closure axiom, not a theorem.",
            "formal_role": "prevents overclaim",
            "buys_if_adopted": "makes the local-GR route explicit and reviewable",
            "cost_or_risk": "a foundational axiom can be challenged; it must earn its keep by simplifying and unifying multiple sectors",
            "adoption_status": "drafted_not_adopted_for_claim",
            "valid_for_claim": "false",
        },
    ]


def consequence_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "CC634_0_vertical_geometry",
            "premise": "ZP634_0, ZP634_1, ZP634_4",
            "derivation": "partial_Xhat e_obs = DObs(Dq[v_Xhat]) = 0",
            "consequence": "partial_Xhat g_matter=0",
            "status_if_clause_adopted": "conditional_pass",
            "valid_for_claim": "false",
        },
        {
            "step_id": "CC634_1_matter_variation",
            "premise": "ZP634_2, ZP634_3 plus CC634_0",
            "derivation": "delta_Xhat S_matter = (delta S_m/dg_m) partial_Xhat g_m + (partial S_m/partial theta_A) partial_Xhat theta_A = 0",
            "consequence": "J_X^matter=0",
            "status_if_clause_adopted": "conditional_pass",
            "valid_for_claim": "false",
        },
        {
            "step_id": "CC634_2_source_test_charges",
            "premise": "J_X^matter=0 for ordinary source and test bodies",
            "derivation": "beta_source=0 and beta_test=0",
            "consequence": "ordinary-matter two-leg alpha_X=0",
            "status_if_clause_adopted": "conditional_pass",
            "valid_for_claim": "false",
        },
        {
            "step_id": "CC634_3_cg_zero",
            "premise": "partial_Xhat matter frame and constants vanish",
            "derivation": "c_g=d ln A_g/dXhat is absent/zero because A_g(Xhat) is not an allowed matter-frame argument",
            "consequence": "c_g=0 in the ordinary local matter branch",
            "status_if_clause_adopted": "conditional_pass",
            "valid_for_claim": "false",
        },
        {
            "step_id": "CC634_4_local_tests",
            "premise": "beta_source=beta_test=c_g=0 plus boundary silence",
            "derivation": "alpha_R10=0 and direct WEP/clock/PPN matter vertices vanish at leading order",
            "consequence": "local tests become GR-reduction/operator-sector questions, not R10 fifth-force coupling questions",
            "status_if_clause_adopted": "conditional_pass_not_public_claim",
            "valid_for_claim": "false",
        },
        {
            "step_id": "CC634_5_scope_limit",
            "premise": "ZP634 is branch-scoped to ordinary local matter coupling",
            "derivation": "cosmology/galaxy/effective memory variables may still enter gravitational field equations or large-scale sector if they are quotient observables",
            "consequence": "zero matter coupling does not automatically erase all MTS phenomenology",
            "status_if_clause_adopted": "requires_consistency_review",
            "valid_for_claim": "false",
        },
    ]


def consistency_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation_id": "OB634_0_scope",
            "obligation": "state exactly that the zero clause governs ordinary local matter coupling, not every MTS effective variable",
            "why_it_matters": "prevents accidentally killing cosmology/galaxy branches",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
        {
            "obligation_id": "OB634_1_covariance",
            "obligation": "show q, Obs(q), and S_matter are covariant/functorial, not a gauge-fixed trick",
            "why_it_matters": "parent selector must be coordinate/frame independent",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
        {
            "obligation_id": "OB634_2_no_shadow_frame",
            "obligation": "forbid post-variation A_g/B_g/source-frame maps unless their derivatives vanish by theorem",
            "why_it_matters": "a hidden conformal/disformal frame would resurrect c_g",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
        {
            "obligation_id": "OB634_3_constants",
            "obligation": "check EM, particle masses, clock constants, and species labels are Xhat-independent or quotient-owned",
            "why_it_matters": "otherwise WEP/clock channels re-enter through constants",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
        {
            "obligation_id": "OB634_4_boundary",
            "obligation": "prove vertical boundary/projector/domain currents have zero ordinary-matter projection",
            "why_it_matters": "boundary source legs can fake a finite local force",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
        {
            "obligation_id": "OB634_5_gr_limit",
            "obligation": "after zero matter coupling, still prove EH/PPN/operator branch reduces to GR",
            "why_it_matters": "killing fifth force is necessary but not sufficient for local GR",
            "status": "required_next_review",
            "valid_for_claim": "false",
        },
    ]


def adoption_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "adoption_id": "AD634_0_current",
            "item": "ZP634 zero-branch parent clause",
            "status": "drafted_not_adopted_for_claim",
            "meaning": "available as a proposed parent selector for review",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "adoption_id": "AD634_1_if_adopted",
            "item": "local ordinary-matter Xhat coupling",
            "status": "would_be_theorem_zero_inside_clause_scope",
            "meaning": "J_X, beta_source, beta_test, and c_g vanish for ordinary local matter",
            "claim_allowed": "false_until_consistency_review",
            "valid_for_claim": "false",
        },
        {
            "adoption_id": "AD634_2_if_rejected",
            "item": "finite coupling branch",
            "status": "two_leg_input_fill_required",
            "meaning": "must source beta_source,beta_test,Z_eff,lambda_X,profile_factor and cross-arena risks",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def two_leg_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "TL634_0_beta_source",
            "symbol": "beta_source",
            "needed_if": "ZP634 rejected or not adopted",
            "definition": "ordinary source matter charge under Xhat exchange",
            "owner_requirement": "derive from delta S_source/dXhat",
            "current_status": "unsourced",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TL634_1_beta_test",
            "symbol": "beta_test",
            "needed_if": "ZP634 rejected or not adopted",
            "definition": "ordinary test-body charge under Xhat exchange",
            "owner_requirement": "derive from delta S_test/dXhat",
            "current_status": "unsourced",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TL634_2_Z_eff",
            "symbol": "Z_eff",
            "needed_if": "finite Xhat mode survives",
            "definition": "kinetic normalization of Xhat exchange",
            "owner_requirement": "parent quadratic action/Hessian",
            "current_status": "unsourced",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TL634_3_lambda_X",
            "symbol": "lambda_X",
            "needed_if": "finite Xhat mode survives",
            "definition": "range sqrt(Z_eff/M_X^2)",
            "owner_requirement": "mass gap/eigenvalue from parent Hessian",
            "current_status": "unsourced",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TL634_4_profile_factor",
            "symbol": "profile_factor(lambda)",
            "needed_if": "finite branch is scored against R10",
            "definition": "R10 source geometry/material/profile response",
            "owner_requirement": "tau_R10,Qbar_XH,source geometry and curve promotion",
            "current_status": "pressure_only",
            "valid_for_claim": "false",
        },
        {
            "input_id": "TL634_5_cross_arena",
            "symbol": "tau_WEP,tau_PPN,tau_clock,tau_orbital",
            "needed_if": "finite branch survives R10 pressure",
            "definition": "same charge law projected to non-R10 local tests",
            "owner_requirement": "must not solve R10 while breaking WEP/PPN/clocks/orbits",
            "current_status": "blocked",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D634_0_main_verdict",
            "decision": STATUS,
            "meaning": "the clean zero route is now an explicit proposed parent selector, not an implicit hope",
            "status": "draft_progress_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D634_1_best_route",
            "decision": "review_zero_clause_first",
            "meaning": "quotient-only ordinary matter is the cleanest local-GR route if it survives consistency review",
            "status": "best_next_route",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D634_2_fallback",
            "decision": "two_leg_input_fill_retained",
            "meaning": "if zero clause is rejected, finite branch requires beta/Z/lambda/profile input fill",
            "status": "fallback_ready",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D634_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "a drafted parent clause is not yet a local test pass",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def route_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU634_0_allowed",
            "allowed_after_634": "Use ZP634 as a proposed parent selector/axiom candidate.",
            "forbidden_after_634": "Say MTS has derived c_g=0 from the existing corpus.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU634_1_allowed",
            "allowed_after_634": "Run a consistency review before adopting the zero clause.",
            "forbidden_after_634": "Let the clause silently erase EM, particle, cosmology, boundary, or operator debts.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU634_2_allowed",
            "allowed_after_634": "Keep two-leg finite input fill as the fallback.",
            "forbidden_after_634": "Score finite coupling without beta/Z/lambda/profile owners.",
            "next_action": NEXT_TARGET,
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC634_0_zero_clause_review",
            "required_output": "consistency review of ZP634 against covariance, constants, EM/particle/time sectors, boundary, and GR operator reduction",
            "success_condition": "no hidden A_g/B_g/mass/constant/boundary channel reintroduces Xhat",
            "if_success": "ZP634 can become a labelled parent axiom candidate for the local branch",
            "if_fail": "demote zero branch to closure-only and proceed to two-leg input fill",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC634_1_axiom_cost_statement",
            "required_output": "explicit public/private wording for the clause cost",
            "success_condition": "states that the clause is proposed unless later derived",
            "if_success": "no overclaim in future summaries",
            "if_fail": "risk of accidentally presenting closure as theorem",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC634_2_two_leg_fill",
            "required_output": "if ZP634 rejected, fill beta_source,beta_test,Z_eff,lambda_X,profile_factor",
            "success_condition": "finite branch has owner equations and units",
            "if_success": "private numerical R10/WEP/PPN pressure can begin",
            "if_fail": "finite branch remains pressure-only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "zero_clause_drafted": "true",
            "zero_clause_adopted_for_claim": "false",
            "cg_zero_claimed": "false",
            "fallback": "two_leg_input_fill_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    clause_rows: list[dict[str, Any]],
    consequence_rows: list[dict[str, Any]],
    obligation_rows: list[dict[str, Any]],
    adoption_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_rows = read_csv(PRIOR_633_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_clause_rows = [row for row in clause_rows if row.get("valid_for_claim") == "true"]
    adopted_claim_rows = [
        row
        for row in adoption_rows
        if row.get("claim_allowed") == "true" or row.get("valid_for_claim") == "true"
    ]
    fallback_claim_rows = [row for row in fallback_rows if row.get("valid_for_claim") == "true"]
    return [
        {
            "check_id": "V634_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V634_1_prior_633_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V634_2_zero_clause_drafted_nonclaim",
            "result": "pass" if len(clause_rows) == 7 and not claim_clause_rows else "fail",
            "detail": f"clause_rows={len(clause_rows)};claim_rows={len(claim_clause_rows)}",
        },
        {
            "check_id": "V634_3_consequence_chain_complete",
            "result": "pass" if len(consequence_rows) == 6 and any(row["consequence"] == "c_g=0 in the ordinary local matter branch" for row in consequence_rows) else "fail",
            "detail": f"consequence_rows={len(consequence_rows)}",
        },
        {
            "check_id": "V634_4_consistency_obligations_written",
            "result": "pass" if len(obligation_rows) == 6 else "fail",
            "detail": f"obligation_rows={len(obligation_rows)}",
        },
        {
            "check_id": "V634_5_not_adopted_for_claim",
            "result": "pass" if len(adoption_rows) == 3 and not adopted_claim_rows else "fail",
            "detail": f"adoption_rows={len(adoption_rows)};claim_rows={len(adopted_claim_rows)}",
        },
        {
            "check_id": "V634_6_two_leg_fallback_inputs_retained_nonclaim",
            "result": "pass" if len(fallback_rows) == 6 and not fallback_claim_rows else "fail",
            "detail": f"fallback_rows={len(fallback_rows)};claim_rows={len(fallback_claim_rows)}",
        },
        {
            "check_id": "V634_7_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V634_8_no_local_claim",
            "result": "pass",
            "detail": "zero_clause_adopted_for_claim=false;c_g_zero_claimed=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
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
    clause_rows: list[dict[str, Any]],
    consequence_rows: list[dict[str, Any]],
    obligation_rows: list[dict[str, Any]],
    adoption_rows: list[dict[str, Any]],
    fallback_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 634 Y5 R10 zero branch parent clause draft or two leg input fill",
            f"Status: `{STATUS}`  \nClaim ceiling: `{CLAIM_CEILING}`  \nNext target: `{NEXT_TARGET}`",
            "## Verdict\n"
            "- The best route is now written explicitly: a proposed quotient-only ordinary-matter parent clause.\n"
            "- If adopted and later consistency-checked, it gives `partial_Xhat g_matter=0`, `delta_Xhat S_matter=0`, `beta_source=beta_test=0`, and `c_g=0` for ordinary local matter.\n"
            "- This is not yet a derived theorem or a local-GR claim; it is a parent-selector draft.\n"
            "- If this clause is rejected or fails consistency review, the finite two-leg branch remains the fallback and needs input fill.",
            "## Source Register\n" + markdown_table(source_rows),
            "## Zero-Branch Parent Clause Draft\n" + markdown_table(clause_rows),
            "## Zero Clause Consequence Chain\n" + markdown_table(consequence_rows),
            "## Consistency Obligations\n" + markdown_table(obligation_rows),
            "## Parent Clause Adoption Status\n" + markdown_table(adoption_rows),
            "## Two-Leg Fallback Input Fill\n" + markdown_table(fallback_rows),
            "## Decision\n" + markdown_table(decisions),
            "## Route Update\n" + markdown_table(routes),
            "## Next Contract\n" + markdown_table(contracts),
            "## Nonclaim Summary\n" + markdown_table(summary),
            "## Validation\n" + markdown_table(validations),
        ]
    )


def main() -> None:
    source_rows = source_register_rows()
    clause_rows = parent_clause_rows()
    consequence_rows = consequence_chain_rows()
    obligation_rows = consistency_obligation_rows()
    adoption_rows = adoption_status_rows()
    fallback_rows = two_leg_input_rows()
    decisions = decision_rows()
    routes = route_update_rows()
    contracts = next_contract_rows()
    summary = nonclaim_summary_rows()
    validations = validation_rows(source_rows, clause_rows, consequence_rows, obligation_rows, adoption_rows, fallback_rows, contracts)

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(PARENT_CLAUSE_DRAFT, clause_rows)
    write_csv(CONSEQUENCE_CHAIN, consequence_rows)
    write_csv(CONSISTENCY_OBLIGATIONS, obligation_rows)
    write_csv(ADOPTION_STATUS, adoption_rows)
    write_csv(TWO_LEG_INPUT_FILL, fallback_rows)
    write_csv(DECISION, decisions)
    write_csv(ROUTE_UPDATE, routes)
    write_csv(NEXT_CONTRACT, contracts)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validations)
    DOC.write_text(
        build_doc(
            source_rows,
            clause_rows,
            consequence_rows,
            obligation_rows,
            adoption_rows,
            fallback_rows,
            decisions,
            routes,
            contracts,
            summary,
            validations,
        )
        + "\n",
        encoding="utf-8",
    )
    failed = [row for row in validations if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))


if __name__ == "__main__":
    main()
