from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "parent_local_zero_action_clause_attempt_written_Q_trace_owned_local_zero_conditional_boundary_R11_stress_open_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_parent_local_zero_clause_only_no_boundary_no_flux_no_R11_silence_no_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "485-boundary-no-flux-and-R11-silence-from-local-zero.md"

DOC_PATH = Path("484-parent-local-zero-action-clause-attempt.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_SOURCE_REGISTER.csv")
ACTION_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv")
VARIATION_CHAIN_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv")
IDENTITY_SCORECARD_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_IDENTITY_SCORECARD.csv")
RESIDUAL_IMPACT_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_RESIDUAL_IMPACT.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_ROUTE_UPDATE.csv")

REQUIRED_IDENTITIES_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_REQUIRED_IDENTITIES.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
QCOH_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "04-vacuum-reciprocity-action-contract.md",
        "role": "local-vacuum no-source theorem template and no-smuggling rules",
    },
    {
        "source_file": "10-observer-map-symplectic-contract.md",
        "role": "local GR reduction requires parent-owned observer/cell constraints and Bianchi completion",
    },
    {
        "source_file": "142-domain-load-tensor-owner-promotion-gate.md",
        "role": "Q can be coherent-volume load if D/u3 are owned; stationary local branch gives conditional Q=0",
    },
    {
        "source_file": "143-domain-selector-variational-action-attempt.md",
        "role": "domain selector and boundary representative remain open",
    },
    {
        "source_file": "177-parent-action-perturbation-local-GR-contract.md",
        "role": "minimal parent action and local-GR silence requirements",
    },
    {
        "source_file": "179-local-GR-PPN-silence-contract.md",
        "role": "q_loc/domain silence still lacks parent action despite screened EFT safety",
    },
    {
        "source_file": "481-Qcoh-parent-projector-algebra-or-closure.md",
        "role": "trace projector algebra fixed but parent ownership missing",
    },
    {
        "source_file": "482-local-residual-vector-from-domain-source-fill.md",
        "role": "current local residual vector and promotion blockers",
    },
    {
        "source_file": "483-parent-action-local-zero-or-fill-decision.md",
        "role": "derivation-first fork decision",
    },
    {
        "source_file": str(REQUIRED_IDENTITIES_PATH),
        "role": "required identities for parent local-zero route",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "local residual components impacted by this attempt",
    },
    {
        "source_file": str(QCOH_CONTRACT_PATH),
        "role": "Qcoh/Pcoh/chi_D parent contract",
    },
    {
        "source_file": "scripts/parent_local_zero_action_clause_attempt.py",
        "role": "this checkpoint generator",
    },
]


ACTION_CLAUSE_ROWS = [
    {
        "clause_id": "A0_variables",
        "object": "u^mu, h_mu_nu, X, Qcoh_mu_nu, chi_D",
        "candidate_form": "u^2=-1; h_mu_nu=g_mu_nu+u_mu u_nu; X=nabla_mu u^mu; Qcoh_mu_nu=(1/3)h_mu_nu X",
        "what_it_owns": "coherent scalar load and trace projector without arbitrary smoothing",
        "what_it_does_not_own": "physical domain selector D, boundary representative, R11/source-normalization silence",
        "status": "formal_candidate",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "A1_parent_clause",
        "object": "S_local_zero",
        "candidate_form": "int sqrt(-g)[lambda_u(u^2+1)+Lambda_X(X-nabla.u)+Lambda_Q^{mu nu}(Qcoh_mu_nu-h_mu_nu X/3)+L_mem(I_D)+L_chi(chi_D,D)]",
        "what_it_owns": "X and Qcoh can be varied/defined before FLRW; Pcoh is a definition from h and X",
        "what_it_does_not_own": "full MTS parent action; L_chi/D still a contract; multipliers may carry stress",
        "status": "partial_action_clause",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "A2_domain_load",
        "object": "I_D",
        "candidate_form": "I_D = [V_D^{-1} int_D sqrt(h) chi_D X]^3 or det_h(Qcoh_D)",
        "what_it_owns": "cubic/double-zero exposure once local X_D=0",
        "what_it_does_not_own": "domain selection and boundary flux",
        "status": "conditional_double_zero",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "A3_local_zero_theorem",
        "object": "stationary compact local branch",
        "candidate_form": "if u is proportional to a local stationary Killing flow and boundary is comoving, X=nabla.u=0 and dV_D/dtau=int_D X=0",
        "what_it_owns": "local zero follows from stationarity/volume conservation, not from a plateau axiom",
        "what_it_does_not_own": "existence/selection of that branch from parent equations; dynamic local safety",
        "status": "conditional_theorem",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "A4_forbidden_rescue",
        "object": "do-not-use terms",
        "candidate_form": "no term of the form kappa chi_D X^2 with fitted kappa may be used as proof of local silence",
        "what_it_owns": "prevents forcing zero by a hand penalty",
        "what_it_does_not_own": "a theorem by itself",
        "status": "guard",
        "valid_for_claim": "false",
    },
]


VARIATION_CHAIN_ROWS = [
    {
        "step_id": "V0_delta_lambda_u",
        "variation": "delta_{lambda_u} S=0",
        "result": "u^mu u_mu=-1",
        "clears_identity": "normalizes local observer flow",
        "status": "formal_pass",
        "claim_effect": "sets coframe variable only",
    },
    {
        "step_id": "V1_delta_Lambda_X",
        "variation": "delta_{Lambda_X} S=0",
        "result": "X=nabla_mu u^mu",
        "clears_identity": "LZ0_Q_owner partial: coherent scalar load defined before FLRW",
        "status": "formal_pass_partial",
        "claim_effect": "Q owner improves but full parent action still missing",
    },
    {
        "step_id": "V2_delta_Lambda_Q",
        "variation": "delta_{Lambda_Q} S=0",
        "result": "Qcoh_mu_nu=(1/3)h_mu_nu X",
        "clears_identity": "LZ1_trace_projector_owner partial: trace projector owned by definition of coherent scalar load",
        "status": "formal_pass_partial",
        "claim_effect": "removes arbitrary smoothing; not full PPN pass",
    },
    {
        "step_id": "V3_stationary_branch",
        "variation": "local stationary/Killing branch condition",
        "result": "X=0, Qcoh=0, det_h(Qcoh)=0",
        "clears_identity": "LZ3 local zero conditional",
        "status": "conditional_pass",
        "claim_effect": "local zero is a conditional theorem target, not global derivation",
    },
    {
        "step_id": "V4_delta_chi_D_or_D",
        "variation": "delta_chi_D S=0 and delta_D S=0",
        "result": "domain/boundary selection remains open",
        "clears_identity": "LZ2 not cleared",
        "status": "fail_for_claim",
        "claim_effect": "domain selector still blocks promotion",
    },
    {
        "step_id": "V5_delta_g_stress",
        "variation": "delta_g S=0",
        "result": "multiplier, projector, and boundary stress must be shown zero/topological or retained",
        "clears_identity": "LZ6 not cleared",
        "status": "retained_debt",
        "claim_effect": "Bianchi/local-GR claim still forbidden",
    },
    {
        "step_id": "V6_boundary_flux",
        "variation": "boundary variation / Noether current",
        "result": "volume flux zero under comoving stationary branch, but alpha3 preferred momentum flux is not proven zero",
        "clears_identity": "LZ5 not cleared",
        "status": "fail_for_claim",
        "claim_effect": "boundary alpha3 still blocks",
    },
    {
        "step_id": "V7_R11_source",
        "variation": "source-normalization / non-EH operator sector",
        "result": "EH-only/R11 silence does not follow from X=0 alone",
        "clears_identity": "LZ4 not cleared",
        "status": "fail_for_claim",
        "claim_effect": "source-normalized Newton still blocked",
    },
]


IDENTITY_SCORECARD_ROWS = [
    {
        "identity_id": "LZ0_Q_owner",
        "attempt_result": "partial_formal_pass",
        "evidence": "X=nabla.u and Qcoh=hX/3 can be included as constrained parent variables",
        "still_missing": "full parent source-normalization equation and coupling to matter/readout",
        "residual_effect": "LRV_QCOH_PARENT_VARIABLE improved but not claim-valid",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ1_trace_projector_owner",
        "attempt_result": "partial_formal_pass",
        "evidence": "if coherent load is scalar X, trace projector is owned by construction rather than smoothing",
        "still_missing": "proof that STF modes do not re-enter via stress, boundary, or R11 channels",
        "residual_effect": "LRV_QCOH_PROJECTOR_OWNERSHIP improved but not claim-valid",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ2_domain_selector",
        "attempt_result": "fail_for_claim",
        "evidence": "L_chi/D remains a contract; no zero-knob Euler law selects D and representative",
        "still_missing": "domain/boundary representative theorem",
        "residual_effect": "LRV_QCOH_DOMAIN_SELECTOR remains failed",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ3_local_zero_class",
        "attempt_result": "conditional_pass",
        "evidence": "stationary Killing/comoving branch gives X=0 and dV_D/dtau=0",
        "still_missing": "parent derivation that solar-system local branch is exactly in this class through PPN order",
        "residual_effect": "domain alpha1/alpha2/alpha3/xi become theorem-target rows, not passes",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ4_R11_EH_silence",
        "attempt_result": "fail_for_claim",
        "evidence": "X=0 does not remove non-EH/source-normalization operator families",
        "still_missing": "EH-only/R11 zero theorem or coefficient vector",
        "residual_effect": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION remains failed",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ5_boundary_no_flux",
        "attempt_result": "fail_for_claim",
        "evidence": "comoving stationary volume flux is zero but alpha3 preferred momentum flux K_boundary is not proven zero",
        "still_missing": "boundary no-flux / no preferred momentum theorem",
        "residual_effect": "LRV_BOUNDARY_R7_ALPHA3 remains failed",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ6_stress_Bianchi",
        "attempt_result": "fail_for_claim",
        "evidence": "covariant action gives formal total conservation only after all retained stresses are included",
        "still_missing": "projector/domain/boundary stress ledger and local Bianchi closure",
        "residual_effect": "LRV_PROJECTOR_STRESS_ACCOUNTING remains failed",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ7_no_total_alpha3_cancellation",
        "attempt_result": "guard_pass",
        "evidence": "no total alpha3 cancellation is used in the clause",
        "still_missing": "individual boundary/domain passes",
        "residual_effect": "LRV_TOTAL_ALPHA3_GUARD remains active",
        "valid_for_claim": "false",
    },
]


RESIDUAL_IMPACT_ROWS = [
    {
        "component_id": "LRV_QCOH_PARENT_VARIABLE",
        "old_status": "missing_explicit_parent_variable",
        "new_status": "partial_formal_clause",
        "reason": "X=nabla.u and Qcoh=hX/3 are now written as constrained parent variables",
        "claim_effect": "improved_theorem_target_not_claim_valid",
    },
    {
        "component_id": "LRV_QCOH_PROJECTOR_OWNERSHIP",
        "old_status": "algebra_known_parent_ownership_missing",
        "new_status": "partial_owned_by_scalar_definition",
        "reason": "coherent tensor is trace-only by definition from scalar expansion load",
        "claim_effect": "raw smoothing objection reduced; stress/boundary still open",
    },
    {
        "component_id": "LRV_QCOH_DOMAIN_SELECTOR",
        "old_status": "not_derived",
        "new_status": "still_not_derived",
        "reason": "local zero uses stationary branch but does not derive physical D/representative",
        "claim_effect": "blocks_local_GR",
    },
    {
        "component_id": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3;LRV_DOMAIN_R8_XI",
        "old_status": "template_unfilled",
        "new_status": "conditional_zero_if_all_domain_couplings_reduce_to_X",
        "reason": "X=0 kills pure coherent-trace domain source, but not vector/R11/boundary leakage",
        "claim_effect": "not_claim_valid",
    },
    {
        "component_id": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "old_status": "template_unfilled",
        "new_status": "failed_for_claim",
        "reason": "R11/source-normalization silence does not follow from X=0 alone",
        "claim_effect": "blocks_Newton_and_local_GR",
    },
    {
        "component_id": "LRV_BOUNDARY_R7_ALPHA3",
        "old_status": "template_unfilled",
        "new_status": "failed_for_claim",
        "reason": "volume flux zero is not the same as preferred momentum no-flux",
        "claim_effect": "blocks_alpha3_and_local_GR",
    },
    {
        "component_id": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "old_status": "retained_debt",
        "new_status": "retained_debt",
        "reason": "multiplier/projector/domain stress must still be varied or shown topological",
        "claim_effect": "blocks_Bianchi_PPN",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_clause",
        "status": "partial_constructed",
        "meaning": "a parent clause can own coherent scalar load X and trace Qcoh without arbitrary smoothing",
        "next_action": "carry Q/Pcoh partial win forward",
    },
    {
        "decision_id": "D1_local_zero",
        "status": "conditional_theorem",
        "meaning": "stationary compact local branch gives X_D=0 without a plateau axiom",
        "next_action": "test whether boundary/R11/stress terms also vanish",
    },
    {
        "decision_id": "D2_promotion",
        "status": "forbidden",
        "meaning": "domain selector, boundary alpha3 no-flux, R11 silence, and stress/Bianchi closure remain open",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_numeric_fill",
        "status": "deferred",
        "meaning": "numeric closure fills remain fallback only; the theory route gained a partial clause worth auditing",
        "next_action": "do not fill until boundary/R11 route is tested or explicitly pivoted",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "QCOH_PARENT",
        "previous_status": "not_parent_owned",
        "new_status": "partial_formal_clause",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_ZERO",
        "previous_status": "conditional_not_parent_derived",
        "new_status": "conditional_stationary_theorem",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BOUNDARY_R11_STRESS",
        "previous_status": "failed_or_retained",
        "new_status": "active_blocker",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_REGISTER:
        path = ROOT / source["source_file"]
        rows.append(
            {
                "source_file": source["source_file"],
                "exists": str(path.exists()),
                "role": source["role"],
            }
        )
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    claim_valid_identities = [row for row in IDENTITY_SCORECARD_ROWS if row["valid_for_claim"] == "true"]
    failed_for_claim = [row for row in IDENTITY_SCORECARD_ROWS if "fail_for_claim" in row["attempt_result"]]
    partial_or_conditional = [
        row
        for row in IDENTITY_SCORECARD_ROWS
        if row["attempt_result"] in {"partial_formal_pass", "conditional_pass", "guard_pass"}
    ]
    return [
        {
            "rule_id": "V484_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V484_1_clause_written",
            "rule": "candidate parent local-zero clause explicitly defines X and Qcoh",
            "result": "pass",
            "evidence": "A1_parent_clause;V1_delta_Lambda_X;V2_delta_Lambda_Q",
            "claim_effect": "Q/Pcoh route sharpened",
        },
        {
            "rule_id": "V484_2_no_plateau_axiom",
            "rule": "local zero is tied to stationarity/volume conservation rather than an inserted penalty forcing X=0",
            "result": "pass",
            "evidence": "A3_local_zero_theorem;A4_forbidden_rescue",
            "claim_effect": "conditional theorem target is clean",
        },
        {
            "rule_id": "V484_3_blockers_retained",
            "rule": "domain selector, boundary no-flux, R11 silence, and stress/Bianchi closure remain unpromoted",
            "result": "pass",
            "evidence": f"fail_for_claim_identities={len(failed_for_claim)}",
            "claim_effect": "no hidden local-GR pass",
        },
        {
            "rule_id": "V484_4_no_claim_valid_rows",
            "rule": "no identity row is claim-valid",
            "result": "pass" if not claim_valid_identities else "fail",
            "evidence": f"claim_valid_identity_rows={len(claim_valid_identities)}",
            "claim_effect": "no Newton/PPN/local-GR promotion",
        },
        {
            "rule_id": "V484_5_partial_progress_recorded",
            "rule": "partial/conditional wins are separated from failures",
            "result": "pass",
            "evidence": f"partial_or_conditional_rows={len(partial_or_conditional)}",
            "claim_effect": "next route can target remaining blockers",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(timestamp: str, generated_at_utc: str, run_dir: Path, sources: list[dict[str, str]], validations: list[dict[str, str]]) -> str:
    return f"""# 484 - Parent Local-Zero Action Clause Attempt

Private derivation attempt. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `483` chose the derivation-first fork:

```text
try to make local zero come from a parent action before falling back to numeric closure fills.
```

This checkpoint attempts the actual clause.

Short answer:

```text
partial win:
X = nabla_mu u^mu and Qcoh_mu_nu = h_mu_nu X/3 can parent-own the trace projector route.

conditional win:
stationary compact local domains give X_D=0 without a plateau axiom.

not a promotion:
domain selection, boundary alpha3 no-flux, R11/source-normalization silence,
and projector/domain stress accounting remain open.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_local_zero_action_clause_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Candidate Action Clause

{markdown_table(ACTION_CLAUSE_ROWS)}

The useful clause is:

```text
X = nabla_mu u^mu
Qcoh_mu_nu = (1/3) h_mu_nu X
```

This means `P_coh` is no longer an arbitrary smoothing operator in this route. It is the tensor lift of a parent-owned scalar expansion load.

## 5. Variation Chain

{markdown_table(VARIATION_CHAIN_ROWS)}

The local-zero theorem target is:

```text
if the compact local branch is stationary and the domain boundary is comoving,
then dV_D/dtau = int_D sqrt(h) chi_D X = 0,
so X_D=0 and det_h(Qcoh_D)=0.
```

That is not a plateau axiom. It is a stationarity/volume-conservation theorem.

But it is only conditional until the parent action selects that branch and closes the boundary/R11/stress ledgers.

## 6. Identity Scorecard

{markdown_table(IDENTITY_SCORECARD_ROWS)}

## 7. Residual Impact

{markdown_table(RESIDUAL_IMPACT_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The Qcoh/trace-projector route now has a concrete parent-clause candidate.
Local X_D=0 follows conditionally for stationary compact comoving domains.
This is a real derivation target and better than arbitrary closure.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived the Newtonian limit.
MTS passes PPN.
MTS has alpha3=0 or mu_extra=0.
Boundary volume flux zero is the same as alpha3 preferred-momentum no-flux.
R11/source-normalization silence follows from X_D=0.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | test the remaining blockers: boundary no-flux, R11 silence, and stress/Bianchi closure |
| 2 | closure fill pack | only if boundary/R11 theorem route fails or is explicitly deferred |
| 3 | alpha3 evaluator refresh | only after theorem-zero certificates or numeric products exist |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-parent-local-zero-action-clause-attempt"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ACTION_CLAUSE_PATH, ACTION_CLAUSE_ROWS)
    write_csv(VARIATION_CHAIN_PATH, VARIATION_CHAIN_ROWS)
    write_csv(IDENTITY_SCORECARD_PATH, IDENTITY_SCORECARD_ROWS)
    write_csv(RESIDUAL_IMPACT_PATH, RESIDUAL_IMPACT_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    claim_valid_identities = [row for row in IDENTITY_SCORECARD_ROWS if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "action_clause": str(ROOT / ACTION_CLAUSE_PATH),
        "variation_chain": str(ROOT / VARIATION_CHAIN_PATH),
        "identity_scorecard": str(ROOT / IDENTITY_SCORECARD_PATH),
        "residual_impact": str(ROOT / RESIDUAL_IMPACT_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "action_clause_rows": len(ACTION_CLAUSE_ROWS),
        "variation_chain_rows": len(VARIATION_CHAIN_ROWS),
        "identity_scorecard_rows": len(IDENTITY_SCORECARD_ROWS),
        "residual_impact_rows": len(RESIDUAL_IMPACT_ROWS),
        "claim_valid_identity_rows": len(claim_valid_identities),
        "Q_owner_partial": True,
        "trace_projector_parent_clause_candidate": True,
        "local_XD_zero_conditional": True,
        "domain_selector_derived": False,
        "boundary_no_flux_derived": False,
        "R11_silence_derived": False,
        "stress_Bianchi_closed": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "alpha3_passed": False,
        "mu_extra_zero_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
