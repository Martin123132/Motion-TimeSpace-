from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_X_coframe_pullback_zero_conditional_vertical_observation_theorem_written_parent_factorization_not_derived"
CLAIM_CEILING = "X_pullback_zero_theorem_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md"

DOC_PATH = Path("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_VERTICAL_OBSERVATION_THEOREM.csv")
PROOF_CHAIN_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_X_PULLBACK_ZERO_PROOF_CHAIN.csv")
COUNTEREXAMPLE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_COUNTEREXAMPLES.csv")
CERTIFICATE_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv")
POLICY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_R10_TRANSITION_POLICY.csv")
RUNNER_SUMMARY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_RUNNER_SUMMARY.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_EVALUATOR.csv")
BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_565_BLOCKER_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_565_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_565_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_565_ROUTE_UPDATE.csv")

PRIOR_VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_564_VALIDATION.csv")
LIVE_MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
LIVE_BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "564-Y5-R10-parent-hessian-source-zero-attempt.md",
        "role": "immediate upstream X pullback obstruction",
    },
    {
        "source_file": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "quotient matter functor conditional theorem and counterexamples",
    },
    {
        "source_file": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt and universal class metric counterexample",
    },
    {
        "source_file": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe theorem contract",
    },
    {
        "source_file": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "coframe pullback cancellation route classification",
    },
    {
        "source_file": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive quotient route candidate",
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
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_564_VALIDATION.csv",
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
        "source_file": "scripts/Y5_R10_coframe_pullback_zero_or_finite_alpha_coefficient.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_ROWS = [
    {
        "theorem_id": "VT565_0_vertical_observation_theorem",
        "name": "X-vertical observed-geometry theorem",
        "statement": "If the parent configuration has quotient q:Phi->Q, observed geometry Obs(Q), matter S_m[psi,Obs(Q),theta], X is vertical with Dq[X]=0, DObs(Dq[X])=0, and theta is X-independent, then delta_X S_matter=0.",
        "proof_status": "conditional_proof_valid",
        "current_parent_status": "factorization_not_parent_derived",
        "claim_status": "not_valid_for_claim",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "VT565_1_R10_pullback_corollary",
        "name": "ordinary matter X-charge zero corollary",
        "statement": "Under VT565_0, q_X^T=-delta_X S_T=0 and J_matter_pullback=(1/2)sqrt(-hat_g)T_hat partial_X hat_g=0.",
        "proof_status": "conditional_corollary",
        "current_parent_status": "requires VT565_0 parent premises",
        "claim_status": "not_valid_for_claim",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "VT565_2_no_hidden_marker_clause",
        "name": "no material marker extension clause",
        "statement": "Matter constants theta_A and material/readout markers must factor through quotient invariants only; otherwise X can re-enter through constants even if Obs is X-blind.",
        "proof_status": "necessary_premise_identified",
        "current_parent_status": "not_parent_derived",
        "claim_status": "not_valid_for_claim",
        "valid_for_claim": "false",
    },
]


PROOF_CHAIN_ROWS = [
    {
        "step_id": "PC565_0_parent_quotient",
        "claim": "Parent variables Phi are quotiented by representative/gauge directions into Q.",
        "mathematical_form": "q:Phi -> Q",
        "result": "premise_open",
        "why": "The quotient route is sketched but not derived as the unique parent configuration space.",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PC565_1_X_vertical",
        "claim": "X is a representative/vertical direction, not an observed geometry direction.",
        "mathematical_form": "Dq[X]=0",
        "result": "premise_open",
        "why": "Current corpus treats X as a possible finite-range physical mode, so verticality is not established.",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PC565_2_observed_functor",
        "claim": "Observed coframe/metric depends only on Q.",
        "mathematical_form": "hat_g = Obs(Q)",
        "result": "conditional_template",
        "why": "If true, partial_X hat_g = DObs(Dq[X]) = 0.",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PC565_3_matter_factorization",
        "claim": "Matter action factors only through observed geometry and X-independent constants.",
        "mathematical_form": "S_m = S_m[psi, Obs(Q), theta], partial_X theta = 0",
        "result": "sufficient_if_parent_derived",
        "why": "Then chain rule gives delta_X S_m = (delta S_m/dhat_g) partial_X hat_g + (partial S_m/partial theta) partial_X theta = 0.",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PC565_4_R10_charge_zero",
        "claim": "ordinary matter pullback source vanishes.",
        "mathematical_form": "q_X^T=0; J_matter_pullback=0",
        "result": "conditional_corollary",
        "why": "Follows only if PC565_1 through PC565_3 are parent-derived.",
        "valid_for_claim": "false",
    },
    {
        "step_id": "PC565_5_verdict",
        "claim": "R10 matter pullback theorem-zero is proved from current corpus.",
        "mathematical_form": "partial_X hat_g = 0 as parent theorem",
        "result": "fail_current_claim",
        "why": "X verticality, matter factorization, and no-marker/constant-sector independence remain open.",
        "valid_for_claim": "false",
    },
]


COUNTEREXAMPLE_ROWS = [
    {
        "counterexample_id": "CE565_0_universal_X_metric",
        "premise_it_satisfies": "covariant universal one-coframe matter",
        "construction": "hat_g_mu_nu = exp(2 F(X)) g_mu_nu",
        "failure": "partial_X hat_g_mu_nu = 2 F_prime exp(2F) g_mu_nu, so J_matter_pullback is proportional to T_hat F_prime",
        "lesson": "universal matter coupling is not enough; X-blindness or constant F is required",
        "blocks_claim": "true",
    },
    {
        "counterexample_id": "CE565_1_species_blind_nonzero_common_mode",
        "premise_it_satisfies": "species-blind common F",
        "construction": "same F(X) for every material species",
        "failure": "WEP composition split can vanish while common fifth-force/clock/source-normalization rows remain",
        "lesson": "qbar_XA=qbar_XB does not imply qbar_XT=0",
        "blocks_claim": "true",
    },
    {
        "counterexample_id": "CE565_2_marker_extended_matter",
        "premise_it_satisfies": "observed geometry functor is X-blind",
        "construction": "theta_A = theta_A(X) or material marker m_A(X) in matter constants",
        "failure": "delta_X S_matter returns through constants/readout markers",
        "lesson": "no-marker/no-class-charge clause is necessary",
        "blocks_claim": "true",
    },
    {
        "counterexample_id": "CE565_3_field_redefinition",
        "premise_it_satisfies": "choose e_prime=hat_e",
        "construction": "rename the observed coframe as the metric variable",
        "failure": "moves debts into EH/operator/source frame rather than proving X verticality",
        "lesson": "frame renaming is not parent selection",
        "blocks_claim": "true",
    },
]


CERTIFICATE_ROWS = [
    {
        "certificate_id": "CT565_0_X_pullback_zero_certificate",
        "required_clause": "X is vertical to the observation quotient",
        "mathematical_form": "Dq[X]=0 and DObs(Dq[X])=0",
        "current_status": "not_parent_derived",
        "needed_source": "primitive quotient parent action or exact selector-blind matter theorem",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "CT565_1_matter_factorization_certificate",
        "required_clause": "matter factors through Obs(Q) only",
        "mathematical_form": "S_matter=sum_A S_A[psi_A, Obs(Q), omega[Obs(Q)], theta_A]",
        "current_status": "not_parent_derived",
        "needed_source": "matter functor/no-marker theorem",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "CT565_2_no_marker_constant_certificate",
        "required_clause": "constants/material markers are X-independent",
        "mathematical_form": "partial_X theta_A=0 and no material/readout marker extension",
        "current_status": "not_parent_derived",
        "needed_source": "no-marker parent action theorem",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "CT565_3_R10_source_zero_certificate",
        "required_clause": "ordinary matter pullback source zero",
        "mathematical_form": "q_X^T=0 and J_matter_pullback=0",
        "current_status": "template_unfilled",
        "needed_source": "CT565_0 through CT565_2 plus hidden channel zero",
        "valid_for_claim": "false",
    },
]


POLICY_ROWS = [
    {
        "policy_id": "RP565_0_if_vertical_theorem_proved",
        "case": "Dq[X]=0, matter factorization, and no-marker clauses are parent-derived",
        "R10_transition": "ordinary-matter qbar_XT and J_matter_pullback can become theorem-zero",
        "remaining_debt": "hidden boundary/projector/memory/domain source channels and Hessian signs still need closure",
        "claim_status": "blocked_until_full_certificate",
    },
    {
        "policy_id": "RP565_1_if_common_mode_survives",
        "case": "hat_g depends on X through universal F(X)",
        "R10_transition": "retain finite alpha(lambda) coefficient branch",
        "remaining_debt": "fill Z_X, M_X^2, Qbar_XH, qbar_XT and real bound curve",
        "claim_status": "blocked_until_numeric_runner",
    },
    {
        "policy_id": "RP565_2_if_marker_extension_survives",
        "case": "matter constants or source markers depend on X",
        "R10_transition": "retain WEP/source-charge/fifth-force residuals",
        "remaining_debt": "derive no-marker theorem or fill species/source coefficients",
        "claim_status": "blocked_until_source_charge_bound",
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
    out: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        source_file = row["source_file"]
        out.append(
            {
                "source_file": source_file,
                "role": row["role"],
                "exists": str((ROOT / source_file).exists()),
            }
        )
    return out


def build_runner_summary(result: dict[str, Any]) -> list[dict[str, Any]]:
    status = result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_565_LIVE_PLACEHOLDER_RECHECK",
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
            "notes": "proof attempt only; live claim rows remain placeholders",
        }
    ]


def build_evaluator(runner_result: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "E565_0_conditional_theorem",
            "gate": "prove pullback zero under vertical observation/factorization premises",
            "result": "conditional_pass",
            "detail": "chain rule gives delta_X S_matter=0 if Dq[X]=0, DObs(DqX)=0, and constants are X-independent",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E565_1_parent_derivation",
            "gate": "derive vertical observation/factorization from current parent action",
            "result": "fail_current_claim",
            "detail": "quotient/factorization/no-marker clauses remain open; X may be a physical finite-range mode",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E565_2_counterexamples",
            "gate": "rule out weak-premise shortcuts",
            "result": "pass",
            "detail": "universal class metric, species-blind common mode, marker extension, and frame rename counterexamples recorded",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E565_3_R10_zero_certificate",
            "gate": "promote qbar_XT/J_matter to theorem-zero",
            "result": "fail_current_claim",
            "detail": "certificate rows remain unfilled",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E565_4_runner_guardrail",
            "gate": "R10 runner remains blocked",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
            "valid_for_claim": "false",
        },
    ]


def build_blocker_rows() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "B565_0_X_verticality_not_derived",
            "blocker": "The current corpus does not prove X is vertical to the observed quotient.",
            "why_it_matters": "If X is not vertical, ordinary matter can source it and R10 alpha remains active.",
            "next_action": "derive primitive quotient parent clause or treat X as finite residual",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B565_1_matter_factorization_not_derived",
            "blocker": "Matter factorization through Obs(Q) only is still an axiom/template.",
            "why_it_matters": "Without factorization, chain-rule zero does not apply.",
            "next_action": "prove matter functor/no-marker theorem",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B565_2_common_mode_counterexample",
            "blocker": "hat_g=exp(2F(X))g remains a legal counterexample under weaker premises.",
            "why_it_matters": "Covariant, universal, species-blind matter can still produce a common fifth force.",
            "next_action": "derive F_prime=0/source-normalized constant or coefficient-fill alpha(lambda)",
            "claim_blocked": "true",
        },
    ]


def build_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D565_0_theorem_shape_found",
            "decision": "vertical observation theorem is the clean proof shape",
            "meaning": "if X lies in the kernel of observed geometry and matter factors through the quotient, q_XT and J_matter vanish",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D565_1_not_parent_derived",
            "decision": "do not promote R10 theorem-zero",
            "meaning": "the exact parent premises are not derived in current corpus",
            "status": "R10_retained",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D565_2_next_fork",
            "decision": "primitive quotient/no-marker proof or coefficient fill",
            "meaning": "one more structural proof attempt is warranted before finite alpha scoring",
            "status": "sharp_fork",
            "next_target": NEXT_TARGET,
        },
    ]


def build_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU565_0_allowed",
            "allowed_after_565": "MTS may cite the vertical-observation theorem as a conditional proof of ordinary matter X-pullback zero.",
            "forbidden_after_565": "MTS may not claim the parent action has derived X-verticality, theorem-zero, R10 pass, WEP pass, PPN pass, or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU565_1_decision",
            "allowed_after_565": "MTS may attempt one primitive quotient/no-marker parent clause before coefficient fill.",
            "forbidden_after_565": "MTS may not use universal/species-blind coupling alone as proof of zero alpha.",
            "next_action": "if 566 fails, fill finite alpha coefficient rows",
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
        for table in [THEOREM_ROWS, PROOF_CHAIN_ROWS, CERTIFICATE_ROWS]
        for row in table
        if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    theorem_written = any("Dq[X]=0" in row["statement"] for row in THEOREM_ROWS)
    counterexamples_written = len(COUNTEREXAMPLE_ROWS) >= 4 and all(row["blocks_claim"] == "true" for row in COUNTEREXAMPLE_ROWS)
    certificate_unfilled = all(row["valid_for_claim"] == "false" for row in CERTIFICATE_ROWS)
    no_overclaim = not runner_result["status"]["R10_pass_for_claim"] and not claim_rows
    return [
        {
            "check_id": "V565_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V565_1_prior_564_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V565_2_vertical_theorem_written",
            "result": "pass" if theorem_written else "fail",
            "detail": f"theorem_rows={len(THEOREM_ROWS)}",
        },
        {
            "check_id": "V565_3_counterexamples_block_weak_premises",
            "result": "pass" if counterexamples_written else "fail",
            "detail": f"counterexample_rows={len(COUNTEREXAMPLE_ROWS)}",
        },
        {
            "check_id": "V565_4_certificate_unfilled_no_claim",
            "result": "pass" if certificate_unfilled else "fail",
            "detail": f"certificate_rows={len(CERTIFICATE_ROWS)};claim_rows=0",
        },
        {
            "check_id": "V565_5_runner_still_blocks_placeholders",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
        },
        {
            "check_id": "V565_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V565_7_no_overclaim",
            "result": "pass" if no_overclaim else "fail",
            "detail": "X_vertical_parent_derived=false;pullback_zero_claim=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
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
    body = f"""# 565 Y5 R10 coframe pullback zero or finite alpha coefficient

Generated: {datetime.now(timezone.utc).isoformat()}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- We tried to prove the clean route first.
- The proof exists conditionally: if `X` is vertical to the observed quotient and matter factors only through observed geometry with X-independent constants, then `partial_X hat_g=0`, `q_X^T=0`, and `J_matter_pullback=0`.
- The proof is not parent-derived from the current corpus because X-verticality, matter-factorization, and no-marker/constant-sector independence remain open.
- Weak premises fail: universal, species-blind, covariant matter can still have `hat_g=exp(2F(X))g` and produce a common-mode fifth-force source.

## The Proof Attempt
Let parent fields be `Phi`, quotient data be `Q`, and observed geometry be `hat_g=Obs(Q)`. If:

```text
q: Phi -> Q,
Dq[X] = 0,
hat_g = Obs(Q),
S_matter = S_matter[psi, Obs(Q), theta],
partial_X theta = 0,
```

then:

```text
partial_X hat_g = DObs(Dq[X]) = 0,
delta_X S_matter = (delta S_matter/dhat_g) partial_X hat_g
                  + (partial S_matter/partial theta) partial_X theta
                  = 0.
```

So ordinary matter has:

```text
q_X^T = 0,
J_matter_pullback = 0.
```

That is the proof we wanted. The bad news is that the current parent action has not yet earned the premises.

## Vertical Observation Theorem
{markdown_table(THEOREM_ROWS)}

## Proof Chain
{markdown_table(PROOF_CHAIN_ROWS)}

## Counterexamples
{markdown_table(COUNTEREXAMPLE_ROWS)}

## Certificate Template
{markdown_table(CERTIFICATE_ROWS)}

## R10 Transition Policy
{markdown_table(POLICY_ROWS)}

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
This is genuinely useful. We did not prove `partial_X hat_g=0` from the existing action, but we now know the exact kind of proof that would work: `X` must be a vertical/representative variable invisible to observed quotient geometry, and matter constants must not smuggle it back in. If that cannot be derived next, the honest route is finite `alpha_X(lambda)` coefficient fill.
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = ROOT / "runs" / f"{timestamp}-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient" / "results"
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
    write_csv(THEOREM_PATH, THEOREM_ROWS)
    write_csv(PROOF_CHAIN_PATH, PROOF_CHAIN_ROWS)
    write_csv(COUNTEREXAMPLE_PATH, COUNTEREXAMPLE_ROWS)
    write_csv(CERTIFICATE_PATH, CERTIFICATE_ROWS)
    write_csv(POLICY_PATH, POLICY_ROWS)
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
        "theorem": rel(ROOT / THEOREM_PATH),
        "proof_chain": rel(ROOT / PROOF_CHAIN_PATH),
        "counterexamples": rel(ROOT / COUNTEREXAMPLE_PATH),
        "validation": rel(ROOT / VALIDATION_PATH),
        "validation_failed": [row for row in validation_rows if row["result"] != "pass"],
        "claim_ceiling": CLAIM_CEILING,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
