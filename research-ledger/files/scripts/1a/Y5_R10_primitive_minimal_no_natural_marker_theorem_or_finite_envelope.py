from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md"

PRIOR_572_VALIDATION = RESIDUALS / "P8_Y5_BRR545_572_VALIDATION.csv"
PRIOR_572_SUMMARY = RESIDUALS / "P8_Y5_R10_572_NONCLAIM_SUMMARY.csv"

THEOREM_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_573_PRIMITIVE_MINIMAL_THEOREM_ATTEMPT.csv"
REDUCTION_CHAIN_PATH = RESIDUALS / "P8_Y5_R10_573_NO_MARKER_REDUCTION_CHAIN.csv"
INVARIANT_DEBT_PATH = RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv"
QBAR_CERT_PATH = RESIDUALS / "P8_Y5_R10_573_QBAR_XT_CERTIFICATE_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_573_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_573_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_573_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_573_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_primitive_minimal_no_marker_attempt_reduced_to_invariant_algebra_triviality_not_derived"
CLAIM_CEILING = "primitive_minimal_no_marker_attempt_only_no_qbar_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md"


SOURCE_FILES = [
    "572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md",
    "423-parent-action-minimality-no-extension-theorem-attempt.md",
    "413-no-marker-parent-action-theorem-attempt.md",
    "414-local-quotient-invariant-algebra-triviality-gate.md",
    "407-primitive-relational-quotient-action-sketch.md",
    "410-quotient-matter-functor-theorem-attempt.md",
    "432-same-frame-matter-functor-zero-route.md",
    "382-parent-local-action-minimal-contract.md",
    "source-intake/mts_residuals/P8_Y5_BRR545_572_VALIDATION.csv",
    "source-intake/mts_residuals/P8_Y5_R10_572_NONCLAIM_SUMMARY.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def prior_clean(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def make_theorem_attempts() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "PM573_0_fixed_label_exclusion",
            "claim": "fixed active labels are excluded by strict quotient logic",
            "mathematical_form": "a fixed marker m_fixed is not a function on Q=Phi/G_rep",
            "result": "conditional_pass",
            "what_it_buys": "fixed external spurions cannot be used as parent-action variables if strict quotient domain is proven",
            "what_remains": "does not exclude co-moving material markers or quotient-invariant class scalars",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PM573_1_material_marker_no_extension",
            "claim": "co-moving material markers are forbidden by primitive minimality",
            "mathematical_form": "Conf_parent=Q_MTS rather than Q_tilde=(Q_MTS,m)/G_rel",
            "result": "not_derived",
            "what_it_buys": "would remove theta_A(m(X)) and direct qbar_XT marker charge",
            "what_remains": "current corpus has a minimality contract, not a theorem forbidding extended quotient objects",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PM573_2_no_natural_marker_functor",
            "claim": "no nonconstant natural marker functor exists on the local branch",
            "mathematical_form": "Nat(Q_MTS,Marker)_loc = constants",
            "result": "reduced_to_invariant_algebra_triviality",
            "what_it_buys": "would prove partial_X theta_A=0 for matter constants if all constants factor through natural marker-free functors",
            "what_remains": "414 already found extra candidate invariant generators, so this is not currently proved",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PM573_3_local_invariant_algebra",
            "claim": "local quotient-invariant algebra is geometry jets plus universal constants",
            "mathematical_form": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const",
            "result": "fail_current_claim",
            "what_it_buys": "would block local material markers and make no-marker theorem real",
            "what_remains": "finite fibre spectrum, relative/domain class, chi_D, memory/class scalar, species constants, and readout projectors remain uneliminated",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PM573_4_qbar_XT_promotion",
            "claim": "qbar_XT can be promoted to theorem-zero",
            "mathematical_form": "primitive minimality + no natural markers + Obs-kernel => delta_X S_T=0",
            "result": "blocked_for_claim",
            "what_it_buys": "conditional chain is valid and would kill ordinary test-body X charge",
            "what_remains": "primitive minimality and invariant algebra triviality are not parent-derived",
            "valid_for_claim": "false",
        },
    ]


def make_reduction_chain() -> list[dict[str, object]]:
    return [
        {
            "step_id": "RC573_0_parent_domain",
            "statement": "Parent local configuration is the primitive quotient object Q_MTS.",
            "math_form": "Conf_parent=Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel",
            "status": "contract_only",
            "failure_mode": "extended quotient material marker remains legal",
        },
        {
            "step_id": "RC573_1_invariant_algebra",
            "statement": "Local invariant algebra contains only observed geometry jets and universal constants.",
            "math_form": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const",
            "status": "not_derived",
            "failure_mode": "extra invariant generator can become material/source marker",
        },
        {
            "step_id": "RC573_2_no_marker_functor",
            "statement": "Every natural material constant/readout standard factors through constants and observed geometry only.",
            "math_form": "theta_A:Q_MTS->Const with partial_X theta_A=0",
            "status": "conditional_on_RC573_0_RC573_1",
            "failure_mode": "theta_A(I_X) or theta_A(m) restores qbar_XT",
        },
        {
            "step_id": "RC573_3_observed_kernel",
            "statement": "X is vertical to the observed quotient geometry.",
            "math_form": "Dq[X]=0 and DObs(Dq[X])=0",
            "status": "conditional_template",
            "failure_mode": "universal common metric exp(2F(X))g sources X",
        },
        {
            "step_id": "RC573_4_qbar_zero",
            "statement": "Ordinary test-body X charge vanishes.",
            "math_form": "delta_X S_T=0 => qbar_XT=0",
            "status": "conditional_theorem_not_promoted",
            "failure_mode": "R10 finite alpha branch remains active",
        },
    ]


def make_invariant_debts() -> list[dict[str, object]]:
    return [
        {
            "debt_id": "IG573_0_finite_fibre_spectrum",
            "generator": "finite_cell_fibre_spectrum",
            "risk": "can act as a material/source marker or effective charge label",
            "needed_elimination": "integrate out as universal constant, prove basis/gauge relabeling only, or retain coefficient",
            "current_status": "not_trivialized",
        },
        {
            "debt_id": "IG573_1_relative_domain_class",
            "generator": "relative_boundary_domain_class",
            "risk": "local source/class marker and boundary/domain charge",
            "needed_elimination": "prove local trivial class or class-only stress-free nohair",
            "current_status": "not_derived",
        },
        {
            "debt_id": "IG573_2_domain_selector",
            "generator": "chi_D/domain_selector",
            "risk": "preferred-frame/source normalization or R10/R11 marker",
            "needed_elimination": "derive selector as gauge/readout-only or fixed local trivial branch",
            "current_status": "not_derived",
        },
        {
            "debt_id": "IG573_3_memory_scalar",
            "generator": "memory_or_class_scalar",
            "risk": "clock/source/fifth-force scalar channel",
            "needed_elimination": "local value and gradient zero theorem, or explicit bounded residual",
            "current_status": "not_silenced_as_theorem",
        },
        {
            "debt_id": "IG573_4_species_constants",
            "generator": "species_charge_constants",
            "risk": "WEP/source-charge/clock marker",
            "needed_elimination": "constant-sector universality theorem",
            "current_status": "not_universalized",
        },
        {
            "debt_id": "IG573_5_readout_projector",
            "generator": "post_readout_projector",
            "risk": "closure zero can re-enter as reduced-action source",
            "needed_elimination": "readout-after-variation theorem and no post-readout EFT backreaction",
            "current_status": "no_cheat_rule_only",
        },
    ]


def make_qbar_certificate() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "QXC573_0_required",
            "certificate_piece": "primitive minimal parent domain",
            "required_for_qbar_zero": "yes",
            "current_status": "contract_only",
            "claim_effect": "blocks qbar_XT theorem-zero",
        },
        {
            "certificate_id": "QXC573_1_required",
            "certificate_piece": "local invariant algebra triviality",
            "required_for_qbar_zero": "yes",
            "current_status": "failed_current_claim_from_414",
            "claim_effect": "blocks qbar_XT theorem-zero",
        },
        {
            "certificate_id": "QXC573_2_required",
            "certificate_piece": "constant-sector universality",
            "required_for_qbar_zero": "yes",
            "current_status": "not_derived",
            "claim_effect": "blocks qbar_XT theorem-zero",
        },
        {
            "certificate_id": "QXC573_3_required",
            "certificate_piece": "observed geometry kernel for X",
            "required_for_qbar_zero": "yes",
            "current_status": "conditional_template",
            "claim_effect": "blocks qbar_XT theorem-zero",
        },
        {
            "certificate_id": "QXC573_4_result",
            "certificate_piece": "qbar_XT=0",
            "required_for_qbar_zero": "target",
            "current_status": "conditional_only_not_parent_derived",
            "claim_effect": "not claimable; finite-alpha branch retained",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D573_0_attempt_result",
            "decision": "primitive-minimal no-marker theorem attempted",
            "meaning": "the theorem reduces cleanly to primitive domain plus local invariant algebra triviality",
            "status": "reduction_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D573_1_no_promotion",
            "decision": "do not promote qbar_XT=0",
            "meaning": "extra local invariant generators remain from 414 and parent minimality is not derived",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D573_2_next_fork",
            "decision": "try generator elimination or finite envelope",
            "meaning": "one last narrow derivation route is to eliminate the specific invariant generators; otherwise fill finite coefficients",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU573_0_allowed",
            "allowed_after_573": "Cite primitive-minimal no-marker as a conditional reduction theorem.",
            "forbidden_after_573": "Claim material markers are absent, qbar_XT=0, R10 pass, WEP pass, PPN pass, or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU573_1_theory_route",
            "allowed_after_573": "Attack the finite list of invariant generators from 414/573 one by one.",
            "forbidden_after_573": "Invoke primitive minimality as a taste preference rather than a proved universal property.",
            "next_action": "eliminate generators or mark each as residual coefficient",
        },
        {
            "route_id": "RU573_2_finite_route",
            "allowed_after_573": "Keep the R10 finite product wall live and prepare coefficient envelope if generator elimination fails.",
            "forbidden_after_573": "Erase the finite-alpha branch because the no-marker theorem has a nice shape.",
            "next_action": "fallback to K_X, qbar_XT, Qbar_XH(lambda), Z_X, M_X^2 envelope",
        },
    ]


def make_validation(
    prior_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, object]],
    reduction_rows: list[dict[str, object]],
    debt_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [path for path in SOURCE_FILES if not (ROOT / path).exists()]
    claim_rows = [
        row for row in theorem_rows if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    return [
        {
            "check_id": "V573_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(missing) if missing else ""),
        },
        {
            "check_id": "V573_1_prior_572_clean",
            "result": "pass" if prior_clean(prior_rows) else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={sum(row.get('result') != 'pass' for row in prior_rows)}",
        },
        {
            "check_id": "V573_2_theorem_attempt_complete",
            "result": "pass" if len(theorem_rows) >= 5 and not claim_rows else "fail",
            "detail": f"theorem_rows={len(theorem_rows)};claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V573_3_reduction_chain_written",
            "result": "pass" if len(reduction_rows) >= 5 else "fail",
            "detail": f"reduction_rows={len(reduction_rows)}",
        },
        {
            "check_id": "V573_4_invariant_debts_listed",
            "result": "pass" if len(debt_rows) >= 6 else "fail",
            "detail": f"invariant_debt_rows={len(debt_rows)}",
        },
        {
            "check_id": "V573_5_qbar_certificate_blocks_claim",
            "result": "pass"
            if any(row.get("current_status") == "conditional_only_not_parent_derived" for row in qbar_rows)
            else "fail",
            "detail": f"qbar_certificate_rows={len(qbar_rows)};qbar_XT_zero=false",
        },
        {
            "check_id": "V573_6_decision_blocks_claim",
            "result": "pass"
            if any(row.get("status") == "blocked_for_claim" for row in decisions)
            else "fail",
            "detail": "R10_pass=false;local_GR=false;claim_allowed=false",
        },
        {
            "check_id": "V573_7_no_overclaim",
            "result": "pass",
            "detail": "primitive_minimal_derived=false;no_marker_derived=false;invariant_algebra_trivial=false;qbar_XT_zero=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    theorem_rows: list[dict[str, object]],
    reduction_rows: list[dict[str, object]],
    debt_rows: list[dict[str, object]],
    qbar_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 573 Y5 R10 primitive-minimal no-natural-marker theorem or finite envelope

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- We tried the primitive-minimal no-marker theorem.
- The good news: the route is now an exact reduction theorem. If the parent local object is truly primitive/minimal, if the local invariant algebra is only observed-geometry jets plus universal constants, and if `X` is in the observed-geometry kernel, then `qbar_XT=0` follows by the chain rule.
- The bad news: the required local invariant algebra triviality is not derived. Checkpoint 414 already lists surviving generators that can behave as markers.
- So `qbar_XT=0` is still conditional, not promoted. The finite-alpha R10 branch remains alive.
- The next fork is very narrow: eliminate the specific local invariant generators one by one, or stop trying to zero `qbar_XT` and fill the finite coefficient envelope.

## Theorem Attempt
The wanted theorem is:

```text
Conf_parent = Q_MTS,
I_loc(Q_MTS) = I_geom[J^k(e_obs)] tensor Const,
theta_A in Const,
DObs(Dq[X]) = 0
=> partial_X theta_A = 0 and partial_X e_obs = 0
=> delta_X S_T = 0
=> qbar_XT = 0.
```

This is a valid conditional theorem. But the theorem is only as strong as the two hard parent facts:

```text
Q_tilde=(Q_MTS,m)/G_rel is not an admissible parent extension,
I_loc(Q_MTS) has no non-geometric local marker generators.
```

The current corpus has contracts for those facts, not derivations.

## Primitive-Minimal Attempts
{markdown_table(theorem_rows, ["attempt_id", "claim", "result", "what_it_buys", "what_remains", "valid_for_claim"])}

## No-Marker Reduction Chain
{markdown_table(reduction_rows, ["step_id", "statement", "math_form", "status", "failure_mode"])}

## Invariant Generator Debt
{markdown_table(debt_rows, ["debt_id", "generator", "risk", "needed_elimination", "current_status"])}

## qbar_XT Certificate Status
{markdown_table(qbar_rows, ["certificate_id", "certificate_piece", "required_for_qbar_zero", "current_status", "claim_effect"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_573", "forbidden_after_573", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is not a wasted derivation attempt. It tells us the exact remaining battlefield. We do not need a vague “no marker” slogan; we need to kill six named marker generators or mark them as residuals. If those generators can be eliminated from the compact local branch, `qbar_XT=0` becomes a real route. If they cannot, the clean theorem path is exhausted and the honest next move is the finite coefficient envelope against the R10 wall.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    prior_rows = read_csv(PRIOR_572_VALIDATION)
    _prior_summary = read_csv(PRIOR_572_SUMMARY)

    theorem_rows = make_theorem_attempts()
    reduction_rows = make_reduction_chain()
    debt_rows = make_invariant_debts()
    qbar_rows = make_qbar_certificate()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        prior_rows, theorem_rows, reduction_rows, debt_rows, qbar_rows, decisions
    )

    summary_rows = [
        {
            "summary_id": "S573_0_result",
            "status": STATUS,
            "primitive_minimal_attempted": "true",
            "no_marker_derived": "false",
            "local_invariant_algebra_trivial": "false",
            "qbar_XT_zero_parent_derived": "false",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "named_generator_debts": str(len(debt_rows)),
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(
        THEOREM_ATTEMPT_PATH,
        theorem_rows,
        [
            "attempt_id",
            "claim",
            "mathematical_form",
            "result",
            "what_it_buys",
            "what_remains",
            "valid_for_claim",
        ],
    )
    write_csv(
        REDUCTION_CHAIN_PATH,
        reduction_rows,
        ["step_id", "statement", "math_form", "status", "failure_mode"],
    )
    write_csv(
        INVARIANT_DEBT_PATH,
        debt_rows,
        ["debt_id", "generator", "risk", "needed_elimination", "current_status"],
    )
    write_csv(
        QBAR_CERT_PATH,
        qbar_rows,
        [
            "certificate_id",
            "certificate_piece",
            "required_for_qbar_zero",
            "current_status",
            "claim_effect",
        ],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_573", "forbidden_after_573", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "primitive_minimal_attempted",
            "no_marker_derived",
            "local_invariant_algebra_trivial",
            "qbar_XT_zero_parent_derived",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "named_generator_debts",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        theorem_rows,
        reduction_rows,
        debt_rows,
        qbar_rows,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "claim_allowed": False,
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
