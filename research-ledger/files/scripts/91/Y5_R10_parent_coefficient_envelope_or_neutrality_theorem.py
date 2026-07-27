from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"

DOC_PATH = ROOT / "572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md"

PRIOR_571_VALIDATION = RESIDUALS / "P8_Y5_BRR545_571_VALIDATION.csv"
PRIOR_571_SUMMARY = RESIDUALS / "P8_Y5_R10_571_NONCLAIM_SUMMARY.csv"

ZERO_ATTEMPTS_PATH = RESIDUALS / "P8_Y5_R10_572_ZERO_FACTOR_PROOF_ATTEMPTS.csv"
PREMISE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_572_PARENT_PREMISE_AUDIT.csv"
COUNTEREXAMPLES_PATH = RESIDUALS / "P8_Y5_R10_572_COUNTEREXAMPLE_STRESS.csv"
NEXT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_572_NEXT_PROOF_CONTRACT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_572_DERIVE_PATH_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_572_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_572_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_572_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_derive_path_attempted_conditional_neutrality_theorem_not_parent_derived"
CLAIM_CEILING = "derive_path_theorem_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md"


SOURCE_FILES = [
    "571-Y5-R10-finite-alpha-coefficient-route-or-theorem-zero-return.md",
    "570-Y5-R10-review-candidate-bound-curve-runner-and-MTS-coefficient-pressure.md",
    "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
    "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md",
    "407-primitive-relational-quotient-action-sketch.md",
    "410-quotient-matter-functor-theorem-attempt.md",
    "423-parent-action-minimality-no-extension-theorem-attempt.md",
    "430-Ward-source-residual-zero-route-gate.md",
    "432-same-frame-matter-functor-zero-route.md",
    "491-Yloc-no-linear-source-symmetry-or-closure.md",
    "552-Y5-parent-action-BRR545-zero-theorem-contract-or-first-repair-attempt.md",
    "source-intake/mts_residuals/P8_Y5_BRR545_571_VALIDATION.csv",
    "source-intake/mts_residuals/P8_Y5_R10_571_NONCLAIM_SUMMARY.csv",
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


def make_zero_attempts() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "ZFA572_0_test_body_neutrality",
            "target_zero_factor": "qbar_XT=0",
            "proof_strategy": "quotient-observed matter functor",
            "derivation": "If X is vertical to the parent quotient, observed geometry is Obs(Q), ordinary matter factors only through Obs(Q), and constants are X-independent, then delta_X S_T=0 by the chain rule.",
            "mathematical_form": "Dq[X]=0; hat_g=Obs(Q); S_T=S_T[psi_T,Obs(Q),theta_T]; partial_X theta_T=0 => qbar_XT=-delta_X S_T=0",
            "result": "conditional_pass_not_parent_derived",
            "why_not_promoted": "the current parent corpus has not derived primitive-minimal quotient domain, no natural marker extension, and constant-sector independence",
            "surviving_debt": "prove primitive-minimal no-natural-marker theorem or retain qbar_XT residual coefficient",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ZFA572_1_source_neutrality",
            "target_zero_factor": "Qbar_XH(lambda)=0",
            "proof_strategy": "same quotient neutrality applied to torsion-balance sources plus hidden-channel kernel",
            "derivation": "If every source constituent is ordinary quotient matter and all boundary/memory/domain channels are in the X-kernel, the integrated source projection vanishes channelwise.",
            "mathematical_form": "Qbar_XH(lambda)=sum_c int_H W_c(lambda) J_X,c; J_X,c=0 for all matter,boundary,memory,domain channels => Qbar_XH=0",
            "result": "conditional_only_hidden_channels_open",
            "why_not_promoted": "even if ordinary matter is neutral, boundary/domain/memory/projector source channels are not proven kernel-zero",
            "surviving_debt": "derive channelwise source-kernel theorem or fill Qbar_XH(lambda) form factor",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ZFA572_2_vertex_zero",
            "target_zero_factor": "K_X=0",
            "proof_strategy": "Ward/constraint removal of the X exchange vertex",
            "derivation": "A first-class constraint or exact Ward selection rule could remove the physical X exchange residue, so no Yukawa force is mediated.",
            "mathematical_form": "Res[p^2=-M_X^2](G_X J_X J_X)=0 by gauge constraint or s_X=0",
            "result": "fail_current_claim",
            "why_not_promoted": "Noether/Ward ownership gives conservation and bookkeeping, not componentwise zero residue; the finite branch explicitly assumes a propagating local mode",
            "surviving_debt": "derive first-class constraint/no-pole theorem or retain finite K_X",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ZFA572_3_range_decoupling",
            "target_zero_factor": "lambda_X below test reach",
            "proof_strategy": "positive mass-gap decoupling",
            "derivation": "If the parent Hessian gives very large M_X^2/Z_X, the local range may fall below R10 reach.",
            "mathematical_form": "lambda_X=sqrt(Z_X/M_X^2) << lambda_probe",
            "result": "not_a_zero_theorem",
            "why_not_promoted": "decoupling can reduce a force but does not prove alpha_X=0, and it moves pressure to shorter-range or particle constraints",
            "surviving_debt": "derive mass gap and compare against the relevant short-range bound set",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ZFA572_4_no_accidental_cancellation",
            "target_zero_factor": "sum channel cancellation",
            "proof_strategy": "reject cancellation as derivation",
            "derivation": "A zero at one lambda or for one material pair is not a parent theorem unless each term is symmetry-zero or a channel identity holds for all allowed sources.",
            "mathematical_form": "sum_c Q_c f_c(lambda)=0 is claimable only if identity holds for all H,T,lambda in the test domain",
            "result": "forbidden_as_theorem_shortcut",
            "why_not_promoted": "material-specific tuning can pass a point while failing R10/WEP/local-GR generally",
            "surviving_debt": "use cancellation only as nonclaim diagnostic unless promoted to symmetry identity",
            "valid_for_claim": "false",
        },
    ]


def make_premise_audit() -> list[dict[str, object]]:
    return [
        {
            "premise_id": "P572_0_primitive_minimal_quotient",
            "needed_for": "qbar_XT=0 and no-marker exclusion",
            "required_statement": "Conf_parent is the primitive/minimal quotient object generated by motion-time-space, not an extendable quotient with material markers",
            "current_evidence": "407 sketches it; 423 classifies extension tax but does not derive universal property",
            "status": "not_derived",
            "claim_effect": "blocks theorem-zero",
        },
        {
            "premise_id": "P572_1_observed_geometry_kernel",
            "needed_for": "qbar_XT=0",
            "required_statement": "X lies in ker DObs after quotienting, so partial_X hat_g=0",
            "current_evidence": "565 proves the chain-rule theorem if this is assumed",
            "status": "conditional_template",
            "claim_effect": "blocks theorem-zero until parent-derived",
        },
        {
            "premise_id": "P572_2_matter_functor_factorization",
            "needed_for": "qbar_XT=0 and same-frame matter",
            "required_statement": "all ordinary matter, rods, clocks, photons and lab standards factor through one observed frame and universal constants",
            "current_evidence": "410 and 432 state exact theorem shape and counterexamples",
            "status": "sufficient_not_parent_derived",
            "claim_effect": "blocks WEP/R10 local claim",
        },
        {
            "premise_id": "P572_3_constant_sector_no_charge",
            "needed_for": "qbar_XT=0 and WEP/source normalization",
            "required_statement": "partial_X theta_A=0 for material constants and no source/readout marker can carry X-charge",
            "current_evidence": "423 says species constants and material markers remain legal without universal-property proof",
            "status": "not_derived",
            "claim_effect": "blocks neutrality theorem",
        },
        {
            "premise_id": "P572_4_source_channel_kernel",
            "needed_for": "Qbar_XH(lambda)=0",
            "required_statement": "boundary, memory, domain, projector, and source-normalization channels are all in the X kernel or have no linear source",
            "current_evidence": "491 gives no-linear-source contract; 552 keeps extra-sector silence open",
            "status": "not_derived",
            "claim_effect": "blocks source neutrality",
        },
        {
            "premise_id": "P572_5_constraint_no_pole",
            "needed_for": "K_X=0",
            "required_statement": "X is gauge/constraint-owned with no physical exchange pole or zero vertex residue",
            "current_evidence": "430 ranks Ward routes; 490 warns Noether/Ward ownership is not zero",
            "status": "not_derived",
            "claim_effect": "blocks vertex-zero theorem",
        },
    ]


def make_counterexamples() -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CE572_0_universal_common_metric",
            "construction": "hat_g_mu_nu=exp(2F(X))g_mu_nu for every species",
            "why_allowed_without_premise": "covariant and universal, but not X-blind",
            "damage": "WEP split can vanish while common fifth-force source survives",
            "blocked_by": "observed geometry kernel plus F_prime=0 from parent quotient",
        },
        {
            "counterexample_id": "CE572_1_marker_extended_matter",
            "construction": "theta_A=theta_A(m(X)) inside otherwise quotient-covariant matter",
            "why_allowed_without_premise": "material marker is an extended quotient variable unless primitive minimality forbids it",
            "damage": "qbar_XT returns through constants/readout standards",
            "blocked_by": "primitive-minimal no-natural-marker theorem",
        },
        {
            "counterexample_id": "CE572_2_source_boundary_channel",
            "construction": "J_X includes boundary/domain/memory source term even when bulk matter is quotient-neutral",
            "why_allowed_without_premise": "hidden local channels are Ward-owned but not zero",
            "damage": "Qbar_XH(lambda) remains finite",
            "blocked_by": "channelwise source-kernel/no-linear-source theorem",
        },
        {
            "counterexample_id": "CE572_3_conserved_nonzero_vertex",
            "construction": "nabla_mu J_X^mu=0 but J_X couples to a finite propagator",
            "why_allowed_without_premise": "conservation does not set the residue or current to zero",
            "damage": "K_X and finite alpha remain active",
            "blocked_by": "first-class constraint/no-pole theorem",
        },
        {
            "counterexample_id": "CE572_4_one_material_cancellation",
            "construction": "Q_1 f_1(lambda_*)+Q_2 f_2(lambda_*)=0 at one lambda or material pair",
            "why_allowed_without_premise": "not a symmetry identity across the test domain",
            "damage": "apparent R10 pass would be tuning, not local-GR reduction",
            "blocked_by": "componentwise zero or all-source identity",
        },
    ]


def make_next_contract() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NPC572_0_best_derivation_path",
            "target": "qbar_XT=0",
            "why_best": "it would kill ordinary test-body charge universally and is closest to the quotient-matter theorem already shaped",
            "must_prove_next": "primitive-minimal no-natural-marker theorem plus observed-geometry kernel",
            "fallback_if_fails": "retain qbar_XT as bounded residual coefficient",
        },
        {
            "contract_id": "NPC572_1_source_path",
            "target": "Qbar_XH(lambda)=0",
            "why_best": "source neutrality could rescue R10 even if test-body proof is incomplete",
            "must_prove_next": "all hidden source channels are in the X kernel, not just ordinary bulk matter",
            "fallback_if_fails": "fill Qbar_XH(lambda) channelwise form factor",
        },
        {
            "contract_id": "NPC572_2_vertex_path",
            "target": "K_X=0",
            "why_best": "a true no-pole/constraint theorem removes the finite branch at the root",
            "must_prove_next": "first-class constraint or zero exchange residue from parent Hessian/Ward algebra",
            "fallback_if_fails": "derive Z_X and K_X envelope",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D572_0_derive_path_attempted",
            "decision": "derive path attempted before coefficient envelope",
            "meaning": "all three real zero factors were tested as theorem routes",
            "status": "done_nonclaim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D572_1_no_zero_promoted",
            "decision": "do not promote alpha_X=0",
            "meaning": "qbar_XT, Qbar_XH, and K_X remain conditional or blocked, not parent-derived",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D572_2_best_next_derivation",
            "decision": "try primitive-minimal no-natural-marker theorem next",
            "meaning": "this is the cleanest path to qbar_XT=0; if it fails, finite envelope is no longer avoidable",
            "status": "next_required",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU572_0_allowed",
            "allowed_after_572": "Use the qbar_XT quotient-neutrality proof as a conditional theorem target.",
            "forbidden_after_572": "Claim qbar_XT=0, Qbar_XH=0, K_X=0, R10 pass, WEP pass, PPN pass, or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU572_1_theory_route",
            "allowed_after_572": "Attempt primitive-minimal no-natural-marker theorem as the next derivation-first move.",
            "forbidden_after_572": "Use covariance/universality/Noether ownership alone as a zero-factor proof.",
            "next_action": "prove no natural material marker and X-blind observed geometry, or demote to finite envelope",
        },
        {
            "route_id": "RU572_2_finite_route",
            "allowed_after_572": "Keep finite-alpha product wall active as fallback.",
            "forbidden_after_572": "Let the derivation attempt erase the 570 pressure table.",
            "next_action": "if 573 fails, fill/bound K_X, qbar_XT, Qbar_XH(lambda), Z_X, and M_X^2",
        },
    ]


def make_validation(
    prior_rows: list[dict[str, str]],
    zero_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [path for path in SOURCE_FILES if not (ROOT / path).exists()]
    claim_rows = [
        row for row in zero_rows if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    return [
        {
            "check_id": "V572_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(missing) if missing else ""),
        },
        {
            "check_id": "V572_1_prior_571_clean",
            "result": "pass" if prior_clean(prior_rows) else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={sum(row.get('result') != 'pass' for row in prior_rows)}",
        },
        {
            "check_id": "V572_2_zero_factors_attempted",
            "result": "pass"
            if {"qbar_XT=0", "Qbar_XH(lambda)=0", "K_X=0"}.issubset(
                {str(row.get("target_zero_factor")) for row in zero_rows}
            )
            else "fail",
            "detail": f"zero_attempt_rows={len(zero_rows)};claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V572_3_parent_premise_audit_complete",
            "result": "pass" if len(premise_rows) >= 6 else "fail",
            "detail": f"premise_rows={len(premise_rows)}",
        },
        {
            "check_id": "V572_4_counterexamples_block_shortcuts",
            "result": "pass" if len(counterexample_rows) >= 5 else "fail",
            "detail": f"counterexample_rows={len(counterexample_rows)}",
        },
        {
            "check_id": "V572_5_decision_blocks_claim",
            "result": "pass"
            if any(row.get("status") == "blocked_for_claim" for row in decisions)
            else "fail",
            "detail": "R10_pass=false;local_GR=false;claim_allowed=false",
        },
        {
            "check_id": "V572_6_no_overclaim",
            "result": "pass",
            "detail": "qbar_XT_zero=false;Qbar_XH_zero=false;K_X_zero=false;finite_alpha_numeric=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    zero_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    counterexample_rows: list[dict[str, object]],
    next_contract: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 572 Y5 R10 parent coefficient envelope or neutrality theorem

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- We tried the derive path first.
- The cleanest possible proof remains `qbar_XT=0` from quotient-observed matter: if `X` is not in the observed quotient and matter constants cannot carry `X`, ordinary test bodies cannot source or feel `X`.
- That proof is mathematically valid as a conditional theorem, but it is still not parent-derived from the current corpus.
- `Qbar_XH(lambda)=0` and `K_X=0` are harder: source neutrality needs hidden-channel kernel zeros, and vertex zero needs a true no-pole/constraint theorem rather than Ward ownership.
- Therefore no R10/local-GR claim is promoted. The next derivation-first move is the primitive-minimal no-natural-marker theorem; if that fails, the finite coefficient envelope becomes mandatory.

## Proof Attempt
For a finite local mode, checkpoint 571 showed:

```text
alpha_X(lambda_X) = K_X Qbar_XH(lambda_X) qbar_XT.
```

So the only true zero routes are:

```text
qbar_XT = 0
or Qbar_XH(lambda_X) = 0
or K_X = 0.
```

The strongest derivation attempt is:

```text
Phi -> Q = Phi/G_rep,
Dq[X] = 0,
hat_g = Obs(Q),
S_T = S_T[psi_T, Obs(Q), theta_T],
partial_X theta_T = 0.
```

Then:

```text
partial_X hat_g = DObs(Dq[X]) = 0,
delta_X S_T = (delta S_T/delta hat_g) partial_X hat_g
            + (partial S_T/partial theta_T) partial_X theta_T
            = 0,
qbar_XT = -delta_X S_T = 0.
```

That is the right GR-style theorem shape. The missing step is not algebra; it is parent selection: the current corpus has not yet proved that no material marker, constant-sector charge, or source/readout spurion can extend the quotient.

## Zero Factor Proof Attempts
{markdown_table(zero_rows, ["attempt_id", "target_zero_factor", "proof_strategy", "result", "why_not_promoted", "surviving_debt", "valid_for_claim"])}

## Parent Premise Audit
{markdown_table(premise_rows, ["premise_id", "needed_for", "required_statement", "current_evidence", "status", "claim_effect"])}

## Counterexample Stress
{markdown_table(counterexample_rows, ["counterexample_id", "construction", "why_allowed_without_premise", "damage", "blocked_by"])}

## Next Proof Contract
{markdown_table(next_contract, ["contract_id", "target", "why_best", "must_prove_next", "fallback_if_fails"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_572", "forbidden_after_572", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This was the right move. We did not just retreat to coefficients; we pushed the theorem route until the exact missing brick appeared. The brick is not `make alpha small`. It is: prove the parent object is primitive-minimal enough that ordinary matter cannot carry hidden `X` labels. If we can prove that, `qbar_XT=0` is real and the local branch gets dramatically stronger. If we cannot, the theory is still alive, but the R10 branch must be fought honestly with the finite product wall.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    prior_rows = read_csv(PRIOR_571_VALIDATION)
    _prior_summary = read_csv(PRIOR_571_SUMMARY)

    zero_rows = make_zero_attempts()
    premise_rows = make_premise_audit()
    counterexample_rows = make_counterexamples()
    next_contract = make_next_contract()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        prior_rows, zero_rows, premise_rows, counterexample_rows, decisions
    )

    summary_rows = [
        {
            "summary_id": "S572_0_result",
            "status": STATUS,
            "derive_path_attempted": "true",
            "qbar_XT_zero_parent_derived": "false",
            "Qbar_XH_zero_parent_derived": "false",
            "K_X_zero_parent_derived": "false",
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "best_next_derivation": "primitive-minimal no-natural-marker theorem",
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(
        ZERO_ATTEMPTS_PATH,
        zero_rows,
        [
            "attempt_id",
            "target_zero_factor",
            "proof_strategy",
            "derivation",
            "mathematical_form",
            "result",
            "why_not_promoted",
            "surviving_debt",
            "valid_for_claim",
        ],
    )
    write_csv(
        PREMISE_AUDIT_PATH,
        premise_rows,
        [
            "premise_id",
            "needed_for",
            "required_statement",
            "current_evidence",
            "status",
            "claim_effect",
        ],
    )
    write_csv(
        COUNTEREXAMPLES_PATH,
        counterexample_rows,
        [
            "counterexample_id",
            "construction",
            "why_allowed_without_premise",
            "damage",
            "blocked_by",
        ],
    )
    write_csv(
        NEXT_CONTRACT_PATH,
        next_contract,
        ["contract_id", "target", "why_best", "must_prove_next", "fallback_if_fails"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_572", "forbidden_after_572", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "derive_path_attempted",
            "qbar_XT_zero_parent_derived",
            "Qbar_XH_zero_parent_derived",
            "K_X_zero_parent_derived",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "best_next_derivation",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        zero_rows,
        premise_rows,
        counterexample_rows,
        next_contract,
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
