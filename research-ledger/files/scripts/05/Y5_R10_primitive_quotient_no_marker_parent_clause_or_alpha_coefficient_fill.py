from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_primitive_quotient_no_marker_clause_sufficient_but_not_derived_alpha_coefficient_fill_required_next"
CLAIM_CEILING = "primitive_quotient_no_marker_clause_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "567-Y5-R10-finite-alpha-coefficient-fill-and-real-bound-curve-runner.md"

DOC_PATH = Path("566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_SOURCE_REGISTER.csv")
PARENT_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_PRIMITIVE_QUOTIENT_PARENT_CLAUSE.csv")
NO_MARKER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_NO_MARKER_THEOREM_ATTEMPT.csv")
DERIVATION_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_DERIVATION_AUDIT.csv")
X_DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_X_VERTICALITY_DECISION.csv")
ALPHA_FILL_QUEUE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_ALPHA_COEFFICIENT_FILL_QUEUE.csv")
RUNNER_SUMMARY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_RUNNER_SUMMARY.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_EVALUATOR.csv")
BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_566_BLOCKER_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_566_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_566_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_566_ROUTE_UPDATE.csv")

PRIOR_VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_565_VALIDATION.csv")
LIVE_MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
LIVE_BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "role": "immediate upstream vertical observation theorem attempt",
    },
    {
        "source_file": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "conditional quotient matter functor theorem and counterexamples",
    },
    {
        "source_file": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive relational quotient action sketch",
    },
    {
        "source_file": "404-selector-blind-matter-axiom-origin.md",
        "role": "selector-blind matter origin audit",
    },
    {
        "source_file": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "no material marker extension route",
    },
    {
        "source_file": "401-parent-matter-selector-theorem-attempt.md",
        "role": "weak-premise counterexample: universal class metric",
    },
    {
        "source_file": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe parent principle contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_565_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "live MTS placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live bound placeholder file retained unchanged",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "existing R10 runner reused as guardrail",
    },
    {
        "source_file": "scripts/Y5_R10_primitive_quotient_no_marker_parent_clause_or_alpha_coefficient_fill.py",
        "role": "this checkpoint generator",
    },
]


PARENT_CLAUSE_ROWS = [
    {
        "clause_id": "PQ566_0_parent_domain",
        "clause": "primitive parent configuration space is a quotient stack/orbit space of relational motion-time-space data",
        "mathematical_form": "Phi -> Q=Phi/G_rep with physical action S_parent=S_Q[Q]+S_constraints[vertical generators]",
        "would_pay": "representative variables do not enter observed matter geometry",
        "attempt_result": "sufficient_clause_written",
        "parent_derived": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "PQ566_1_X_vertical",
        "clause": "X is declared a vertical representative/gauge direction rather than a quotient observable",
        "mathematical_form": "Dq[X]=0 and DObs(Dq[X])=0",
        "would_pay": "partial_X hat_g=0",
        "attempt_result": "sufficient_clause_written",
        "parent_derived": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "PQ566_2_matter_functor",
        "clause": "ordinary matter is a natural functor only of observed quotient geometry",
        "mathematical_form": "S_m=sum_A S_A[psi_A,Obs(Q),omega[Obs(Q)],theta_A]",
        "would_pay": "matter selector-blindness by chain rule",
        "attempt_result": "sufficient_clause_written",
        "parent_derived": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "PQ566_3_no_marker",
        "clause": "no material/readout marker extension can depend on vertical X",
        "mathematical_form": "partial_X theta_A=0; no m_A(X); no class/source spurion in ordinary matter constants",
        "would_pay": "prevents X returning through constants after geometry is X-blind",
        "attempt_result": "necessary_clause_written",
        "parent_derived": "false",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "PQ566_4_flux_owner",
        "clause": "vertical-sector boundary/projector/domain flux is gauge/Ward-owned or retained as coefficient",
        "mathematical_form": "J_boundary+J_projector+J_memory+J_domain=0 by identity, else coefficient rows",
        "would_pay": "prevents hidden source channels from replacing matter pullback",
        "attempt_result": "not_derived_retained",
        "parent_derived": "false",
        "valid_for_claim": "false",
    },
]


NO_MARKER_ROWS = [
    {
        "test_id": "NM566_0_minimality",
        "claim": "parent minimality forbids material marker extension",
        "attempted_derivation": "allow only quotient-natural local scalars in ordinary matter constants",
        "result": "conditional_pass",
        "failure_mode": "minimality is a selection principle, not yet derived from dynamics",
        "repair": "promote minimal quotient/no-marker clause as explicit axiom, or fill marker/source coefficients",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NM566_1_naturality",
        "claim": "vertical X cannot enter matter constants because it is not a quotient-natural invariant",
        "attempted_derivation": "if Dq[X]=0, any quotient-natural theta_A(Q) has partial_X theta_A=0",
        "result": "conditional_pass",
        "failure_mode": "requires X verticality and theta_A factorization through Q",
        "repair": "derive X verticality or keep qbar_XT/source-charge row",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NM566_2_counterexample_marker",
        "claim": "no-marker follows from covariance/universality alone",
        "attempted_derivation": "ordinary matter is universal and covariant",
        "result": "fail_current_claim",
        "failure_mode": "theta_A=theta_A(I_X) remains possible if I_X is admitted as an invariant or spurion",
        "repair": "forbid marker/spurion extension explicitly or bound the resulting source charge",
        "valid_for_claim": "false",
    },
    {
        "test_id": "NM566_3_verdict",
        "claim": "no-marker theorem is derived in current corpus",
        "attempted_derivation": "combine minimality, quotient naturality, and selector-blind matter",
        "result": "not_derived_current_claim",
        "failure_mode": "the parent action does not yet prove quotient-only matter and no-spurion constants",
        "repair": "alpha coefficient fill becomes mandatory unless a new parent principle is supplied",
        "valid_for_claim": "false",
    },
]


DERIVATION_AUDIT_ROWS = [
    {
        "audit_id": "DA566_0_good_news",
        "finding": "A compact parent clause exists that would kill the ordinary matter X pullback.",
        "meaning": "MTS has an exact structural theorem target, not a vague hope.",
        "claim_impact": "conditional only",
    },
    {
        "audit_id": "DA566_1_bad_news",
        "finding": "The clause is not forced by current weaker premises.",
        "meaning": "covariance, universality, species-blindness, and field redefinition all allow counterexamples.",
        "claim_impact": "blocks theorem-zero",
    },
    {
        "audit_id": "DA566_2_physics_fork",
        "finding": "If X is vertical, ordinary matter pullback can zero; if X is physical, finite alpha(lambda) must be scored.",
        "meaning": "R10 cannot be left in limbo after this checkpoint.",
        "claim_impact": "forces coefficient-fill next",
    },
]


X_DECISION_ROWS = [
    {
        "decision_id": "XD566_0_vertical_branch",
        "branch": "X is representative/vertical",
        "required_parent_fact": "Dq[X]=0 and matter functor/no-marker clauses are parent-derived",
        "consequence": "qbar_XT and J_matter_pullback become theorem-zero candidates",
        "current_state": "not_parent_derived",
        "next_action": "do not promote; certificate remains unfilled",
    },
    {
        "decision_id": "XD566_1_physical_branch",
        "branch": "X is physical finite-range mode",
        "required_parent_fact": "Z_X, M_X^2, Qbar_XH, qbar_XT are coefficient-filled or bounded",
        "consequence": "alpha_X(lambda)=K_X Qbar_XH qbar_XT must face R10 bound curve",
        "current_state": "retained_required",
        "next_action": "build coefficient-fill runner",
    },
    {
        "decision_id": "XD566_2_constraint_branch",
        "branch": "X is nonpropagating constraint",
        "required_parent_fact": "constraint algebra removes physical source and hidden flux",
        "consequence": "no finite alpha row only if constraint theorem is signed",
        "current_state": "not_parent_derived",
        "next_action": "treat as unfilled unless explicit constraint equations appear",
    },
]


ALPHA_FILL_QUEUE_ROWS = [
    {
        "queue_id": "AF566_0_ZX",
        "symbol": "Z_X",
        "needed_for": "lambda_X and K_X",
        "current_status": "missing_parent_Hessian_value",
        "fill_policy": "derive sign/value or sample conservative coefficient range",
        "valid_for_claim": "false",
    },
    {
        "queue_id": "AF566_1_MX",
        "symbol": "M_X^2;lambda_X",
        "needed_for": "R10 lambda_value",
        "current_status": "missing_parent_Hessian_value",
        "fill_policy": "derive mass gap or define finite-range scan grid",
        "valid_for_claim": "false",
    },
    {
        "queue_id": "AF566_2_qtest",
        "symbol": "qbar_XT",
        "needed_for": "ordinary test-body X charge",
        "current_status": "not_theorem_zero",
        "fill_policy": "derive zero or enter coefficient/residual bound row",
        "valid_for_claim": "false",
    },
    {
        "queue_id": "AF566_3_source",
        "symbol": "Qbar_XH(lambda)",
        "needed_for": "source projected X charge",
        "current_status": "hidden_source_channels_open",
        "fill_policy": "source integral/form factor or channelwise bound",
        "valid_for_claim": "false",
    },
    {
        "queue_id": "AF566_4_bound_curve",
        "symbol": "alpha_bound(lambda)",
        "needed_for": "external R10 comparison",
        "current_status": "anchor_only_noncurve",
        "fill_policy": "digitize full Eot-Wash curve or source machine-readable rows",
        "valid_for_claim": "false",
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": row["source_file"],
            "role": row["role"],
            "exists": str((ROOT / row["source_file"]).exists()),
        }
        for row in SOURCE_REGISTER
    ]


def build_runner_summary(result: dict[str, Any]) -> list[dict[str, Any]]:
    status = result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_566_LIVE_PLACEHOLDER_RECHECK",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "mts_rows": status["mts_rows"],
            "valid_mts_rows": status["valid_mts_rows"],
            "bound_rows": status["bound_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "passed_rows": status["passed_rows"],
            "blocked_or_failed_rows": status["blocked_or_failed_rows"],
            "R10_pass_for_claim": status["R10_pass_for_claim"],
            "claim_allowed": status["claim_allowed"],
            "notes": "no theorem-zero promotion; live placeholders remain blocked",
        }
    ]


def build_evaluator(runner_result: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "E566_0_parent_clause",
            "gate": "write sufficient primitive quotient/no-marker parent clause",
            "result": "conditional_pass",
            "detail": "clause would make X vertical and ordinary matter selector-blind if adopted by parent action",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E566_1_derivation_from_current_corpus",
            "gate": "derive clause from current MTS principles",
            "result": "fail_current_claim",
            "detail": "no current principle forces quotient-only matter, no marker constants, and X verticality",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E566_2_no_marker",
            "gate": "derive no material/readout marker extension",
            "result": "fail_current_claim",
            "detail": "marker/spurion extension remains a legal counterexample unless excluded by parent clause",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E566_3_R10_transition",
            "gate": "decide theorem-zero vs coefficient fill",
            "result": "coefficient_fill_required_next",
            "detail": "no further zero route is available without adding a new parent principle",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E566_4_runner_guardrail",
            "gate": "R10 runner remains blocked",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
            "valid_for_claim": "false",
        },
    ]


def build_blocker_rows() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "B566_0_parent_clause_not_derived",
            "blocker": "Primitive quotient/no-marker clause is sufficient but not forced by current corpus.",
            "why_it_matters": "R10 theorem-zero would otherwise be an inserted closure.",
            "next_action": "move to finite alpha coefficient fill unless a new parent principle is supplied",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B566_1_X_physical_mode_not_excluded",
            "blocker": "X remains allowed as a physical finite-range mode in the retained branch.",
            "why_it_matters": "physical X means alpha_X(lambda) must be tested rather than zeroed.",
            "next_action": "fill Z_X, M_X^2, qbar_XT, Qbar_XH",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B566_2_real_bound_curve_missing",
            "blocker": "External R10 curve is still anchor-only/non-claim.",
            "why_it_matters": "numeric alpha cannot be judged against two threshold anchors alone.",
            "next_action": "digitize/source full alpha_bound(lambda) curve",
            "claim_blocked": "true",
        },
    ]


def build_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D566_0_clause_sufficient",
            "decision": "primitive quotient/no-marker parent clause is sufficient",
            "meaning": "if adopted and parent-derived, it would zero ordinary matter X pullback",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D566_1_clause_not_derived",
            "decision": "do not promote theorem-zero",
            "meaning": "current corpus does not derive the clause; using it would be closure",
            "status": "R10_retained",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D566_2_coefficient_fill_required",
            "decision": "move to finite alpha coefficient fill",
            "meaning": "zero-route attempts have reduced to a new parent axiom; next work must score/bound the residual",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def build_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU566_0_allowed",
            "allowed_after_566": "MTS may cite the primitive quotient/no-marker clause as a sufficient parent-action contract.",
            "forbidden_after_566": "MTS may not claim the clause is derived, or that R10/WEP/PPN/local-GR passed.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU566_1_forced_next",
            "allowed_after_566": "MTS should now construct the finite alpha coefficient-fill runner unless the user supplies a new parent action principle.",
            "forbidden_after_566": "MTS may not keep cycling zero-route attempts without new premises.",
            "next_action": "build R10 coefficient fill and real bound curve runner",
        },
    ]


def build_validation_rows(
    source_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    runner_result: dict[str, Any],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_rows = [
        row
        for table in [PARENT_CLAUSE_ROWS, NO_MARKER_ROWS, ALPHA_FILL_QUEUE_ROWS]
        for row in table
        if str(row.get("valid_for_claim", "")).lower() == "true" or row.get("parent_derived") == "true"
    ]
    clause_written = len(PARENT_CLAUSE_ROWS) >= 5
    no_marker_attempted = any(row["test_id"] == "NM566_3_verdict" for row in NO_MARKER_ROWS)
    fill_queue_written = len(ALPHA_FILL_QUEUE_ROWS) >= 5
    no_overclaim = not runner_result["status"]["R10_pass_for_claim"] and not claim_rows
    return [
        {
            "check_id": "V566_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V566_1_prior_565_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V566_2_parent_clause_written",
            "result": "pass" if clause_written else "fail",
            "detail": f"clause_rows={len(PARENT_CLAUSE_ROWS)}",
        },
        {
            "check_id": "V566_3_no_marker_attempted_not_overclaimed",
            "result": "pass" if no_marker_attempted else "fail",
            "detail": f"no_marker_rows={len(NO_MARKER_ROWS)};derived=false",
        },
        {
            "check_id": "V566_4_alpha_fill_queue_written",
            "result": "pass" if fill_queue_written else "fail",
            "detail": f"fill_queue_rows={len(ALPHA_FILL_QUEUE_ROWS)}",
        },
        {
            "check_id": "V566_5_runner_still_blocks_placeholders",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
        },
        {
            "check_id": "V566_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V566_7_no_overclaim",
            "result": "pass" if no_overclaim else "fail",
            "detail": "primitive_clause_parent_derived=false;no_marker_derived=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    runner_summary: list[dict[str, Any]],
    evaluator_rows: list[dict[str, str]],
    blocker_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> None:
    body = f"""# 566 Y5 R10 primitive quotient no-marker parent clause or alpha coefficient fill

Generated: {datetime.now(timezone.utc).isoformat()}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The primitive quotient/no-marker clause is sufficient but not derived.
- If the parent action is genuinely defined on quotient data `Q=Phi/G_rep`, if `X` is vertical with `Dq[X]=0`, and if ordinary matter is a quotient functor with no X-dependent markers/constants, then ordinary matter cannot source `X`.
- The current corpus does not force those clauses. The same counterexamples survive: universal class metrics, marker-extended matter constants, and frame redefinitions.
- Therefore this is the end of the clean zero-route without new premises. The next honest move is finite `alpha_X(lambda)` coefficient fill plus real R10 bound curve.

## Primitive Parent Clause
{markdown_table(PARENT_CLAUSE_ROWS)}

## No-Marker Theorem Attempt
{markdown_table(NO_MARKER_ROWS)}

## Derivation Audit
{markdown_table(DERIVATION_AUDIT_ROWS)}

## X Verticality Decision
{markdown_table(X_DECISION_ROWS)}

## Alpha Coefficient Fill Queue
{markdown_table(ALPHA_FILL_QUEUE_ROWS)}

## Runner Summary
{markdown_table(runner_summary)}

## Evaluator
{markdown_table(evaluator_rows)}

## Blocker Ledger
{markdown_table(blocker_rows)}

## Decision
{markdown_table(decision_rows)}

## Source Register
{markdown_table(source_rows)}

## Validation
{markdown_table(validation_rows)}

## Route Update
{markdown_table(route_rows)}

## Practical Read
This is the honest fork. We found the exact parent clause that would make the local R10 matter pullback vanish, but deriving that clause from the existing corpus would require adding a new primitive principle: quotient-only observed matter with no marker/spurion extension. Without that, `X` remains a retained finite-range branch. The next job should stop trying to magically zero it and start filling `Z_X`, `M_X^2`, `qbar_XT`, `Qbar_XH(lambda)`, and the real `alpha_bound(lambda)` curve.
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = ROOT / "runs" / f"{timestamp}-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill" / "results"
    runner_result = run_runner(ROOT / LIVE_MTS_CURVE_PATH, ROOT / LIVE_BOUND_CURVE_PATH, run_root / "live_placeholder_runner")

    source_rows = source_register_rows()
    prior_rows = read_csv(ROOT / PRIOR_VALIDATION_PATH)
    runner_summary = build_runner_summary(runner_result)
    evaluator_rows = build_evaluator(runner_result)
    blocker_rows = build_blocker_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    validation_rows = build_validation_rows(source_rows, prior_rows, runner_result)

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(PARENT_CLAUSE_PATH, PARENT_CLAUSE_ROWS)
    write_csv(NO_MARKER_PATH, NO_MARKER_ROWS)
    write_csv(DERIVATION_AUDIT_PATH, DERIVATION_AUDIT_ROWS)
    write_csv(X_DECISION_PATH, X_DECISION_ROWS)
    write_csv(ALPHA_FILL_QUEUE_PATH, ALPHA_FILL_QUEUE_ROWS)
    write_csv(RUNNER_SUMMARY_PATH, runner_summary)
    write_csv(EVALUATOR_PATH, evaluator_rows)
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows)
    write_csv(DECISION_PATH, decision_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(ROUTE_UPDATE_PATH, route_rows)
    write_doc(source_rows, runner_summary, evaluator_rows, blocker_rows, decision_rows, validation_rows, route_rows)

    summary = {
        "status": STATUS,
        "doc": rel(ROOT / DOC_PATH),
        "parent_clause": rel(ROOT / PARENT_CLAUSE_PATH),
        "no_marker_attempt": rel(ROOT / NO_MARKER_PATH),
        "alpha_fill_queue": rel(ROOT / ALPHA_FILL_QUEUE_PATH),
        "validation": rel(ROOT / VALIDATION_PATH),
        "validation_failed": [row for row in validation_rows if row["result"] != "pass"],
        "claim_ceiling": CLAIM_CEILING,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
