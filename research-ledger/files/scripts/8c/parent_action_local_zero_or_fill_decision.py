from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "parent_action_local_zero_or_fill_decision_written_derivation_first_fill_fallback_closure_only_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "fork_decision_only_derivation_first_no_parent_local_zero_no_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "484-parent-local-zero-action-clause-attempt.md"

DOC_PATH = Path("483-parent-action-local-zero-or-fill-decision.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_OR_FILL_SOURCE_REGISTER.csv")
FORK_SCORECARD_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_FORK_SCORECARD.csv")
REQUIRED_IDENTITIES_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_REQUIRED_IDENTITIES.csv")
FILL_FALLBACK_PATH = Path("source-intake/mts_residuals/P8_NUMERIC_FILL_FALLBACK_POLICY.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_OR_FILL_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_OR_FILL_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_OR_FILL_ROUTE_UPDATE.csv")

LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
PROMOTION_GATES_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv")
QCOH_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_QCOH_PARENT_ACTION_CONTRACT.csv")
ALPHA3_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv")
DOMAIN_SIBLING_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "142-domain-load-tensor-owner-promotion-gate.md",
        "role": "Q reduced to coherent volume load if D/u3 are parent-owned; D is main blocker",
    },
    {
        "source_file": "143-domain-selector-variational-action-attempt.md",
        "role": "zero-knob domain selector not derived; auxiliary selector retained as contract",
    },
    {
        "source_file": "177-parent-action-perturbation-local-GR-contract.md",
        "role": "minimal parent action and local-GR silence contract",
    },
    {
        "source_file": "179-local-GR-PPN-silence-contract.md",
        "role": "screened effective scalar is locally safe but q_loc/domain silence remains parent-open",
    },
    {
        "source_file": "481-Qcoh-parent-projector-algebra-or-closure.md",
        "role": "trace-projector algebra pass; parent ownership missing",
    },
    {
        "source_file": "482-local-residual-vector-from-domain-source-fill.md",
        "role": "explicit local residual vector with 11 failed claim components",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "machine-readable local residual vector",
    },
    {
        "source_file": str(PROMOTION_GATES_PATH),
        "role": "machine-readable local/Newton/PPN promotion gates",
    },
    {
        "source_file": str(QCOH_CONTRACT_PATH),
        "role": "Qcoh/Pcoh/chi_D/R11 parent-action contract",
    },
    {
        "source_file": str(ALPHA3_TEMPLATE_PATH),
        "role": "alpha3 boundary/domain/total product template",
    },
    {
        "source_file": str(DOMAIN_SIBLING_TEMPLATE_PATH),
        "role": "domain alpha1/alpha2/alpha3/xi/R11 fill template",
    },
    {
        "source_file": "scripts/parent_action_local_zero_or_fill_decision.py",
        "role": "this checkpoint generator",
    },
]


FORK_SCORECARD_ROWS = [
    {
        "fork_id": "F0_parent_local_zero",
        "route": "attempt parent-action local-zero clause",
        "alignment_with_goal": "highest",
        "what_it_could_win": "derived source-normalized Newton/PPN/local-GR route if all identities pass",
        "current_evidence": "Qcoh trace projector algebra is clean; residual vector tells us exactly what must vanish",
        "current_blocker": "parent Q/Pcoh/chi_D/R11/boundary flux ownership not derived",
        "decision": "selected_next",
        "claim_status": "not_promoted",
        "next_target": NEXT_TARGET,
    },
    {
        "fork_id": "F1_numeric_fill",
        "route": "fill residual-vector products/coefficient rows numerically",
        "alignment_with_goal": "medium_as_empirical_closure_only",
        "what_it_could_win": "bounded closure branch and later local-data screen",
        "current_evidence": "482 provides exact fill rows and source-locked bounds",
        "current_blocker": "numbers would not prove GR reduction; alpha3 4e-20 is brutally tight",
        "decision": "fallback_only",
        "claim_status": "closure_not_derivation",
        "next_target": "after 484 fails or after explicit user pivot",
    },
    {
        "fork_id": "F2_alpha3_refresh_now",
        "route": "rerun alpha3 product evaluator immediately",
        "alignment_with_goal": "low_now",
        "what_it_could_win": "nothing, because products/certificates are still missing",
        "current_evidence": "482 alpha3_evaluator_refresh_allowed=false",
        "current_blocker": "no theorem-zero certificates and no numeric products",
        "decision": "blocked_until_inputs_exist",
        "claim_status": "not_allowed",
        "next_target": "defer to filled theorem/numeric rows",
    },
    {
        "fork_id": "F3_local_data_runner_now",
        "route": "run local observational test now",
        "alignment_with_goal": "low_now",
        "what_it_could_win": "no meaningful score without predicted values",
        "current_evidence": "local residual vector has 11 failed/missing components",
        "current_blocker": "no numeric candidate vector",
        "decision": "blocked_until_residual_values_exist",
        "claim_status": "not_allowed",
        "next_target": "defer to closure-fill branch if chosen",
    },
]


REQUIRED_IDENTITIES_ROWS = [
    {
        "identity_id": "LZ0_Q_owner",
        "required_identity": "Q_{mu nu} is a parent-owned load/Noether/strain variable before FLRW reduction",
        "minimal_form": "delta_Q S_parent = 0 gives weak-field Q_{mu nu}; not a post-fit tensor",
        "residual_components_cleared_if_passes": "LRV_QCOH_PARENT_VARIABLE",
        "current_status": "missing_explicit_parent_variable",
        "pass_criterion_for_484": "write an action clause whose Euler equation defines Q and weak-field source normalization",
        "failure_effect": "Qcoh remains closure/theorem target",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ1_trace_projector_owner",
        "required_identity": "P_coh=(1/3)hh is forced dynamically or by a Ward/local-isotropy constraint",
        "minimal_form": "STF Q modes decouple/vanish through local PPN order; P_coh is not chosen after the fact",
        "residual_components_cleared_if_passes": "LRV_QCOH_PROJECTOR_OWNERSHIP",
        "current_status": "algebra_known_parent_ownership_missing",
        "pass_criterion_for_484": "derive trace/STF split from parent constraint without a smoothing scale",
        "failure_effect": "trace projector remains algebra-only",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ2_domain_selector",
        "required_identity": "chi_D/D is selected by parent Euler/topological law with no fitted threshold",
        "minimal_form": "delta_chi S_parent=0 and delta_D S_parent=0 select compact local trivial class and FLRW active class",
        "residual_components_cleared_if_passes": "LRV_QCOH_DOMAIN_SELECTOR",
        "current_status": "not_derived",
        "pass_criterion_for_484": "avoid dynamic wall scale, hand boundary, and outcome-selected domain",
        "failure_effect": "domain branch remains closure-level",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ3_local_zero_class",
        "required_identity": "compact stationary local vacuum gives X_D=Tr_h Q_D=0 through PPN order",
        "minimal_form": "local time-stationary/bound-volume class has no coherent expansion load while FLRW class remains active",
        "residual_components_cleared_if_passes": "LRV_QCOH_DOMAIN_SELECTOR;LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3;LRV_DOMAIN_R8_XI",
        "current_status": "conditional_not_parent_derived",
        "pass_criterion_for_484": "derive X_D=0 from parent equations, not plateau axiom",
        "failure_effect": "local PPN/source-vector rows remain unfilled",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ4_R11_EH_silence",
        "required_identity": "R11/source-normalization non-EH operator rows vanish or are retained with coefficients",
        "minimal_form": "local compact branch reduces to EH plus universal measured-GM normalization",
        "residual_components_cleared_if_passes": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "current_status": "failed_in_479",
        "pass_criterion_for_484": "derive EH-only/source-normalization zero from the same parent clause or admit coefficient fill",
        "failure_effect": "source-normalized Newton remains blocked",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ5_boundary_no_flux",
        "required_identity": "boundary sector has no local preferred momentum flux through alpha3",
        "minimal_form": "F_boundary_alpha3 = 0 from variation/conservation, not cancellation",
        "residual_components_cleared_if_passes": "LRV_BOUNDARY_R7_ALPHA3",
        "current_status": "missing_parent_boundary_no_flux_certificate",
        "pass_criterion_for_484": "derive zero boundary alpha3 flux or route to numeric product fill",
        "failure_effect": "alpha3 remains blocked even if domain improves",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ6_stress_Bianchi",
        "required_identity": "metric variation of P_coh/chi_D/domain boundary stress vanishes/topologically cancels or is retained",
        "minimal_form": "delta_g P_coh and delta_g chi_D do not create PPN-sized stress; Bianchi identity closes without hidden force",
        "residual_components_cleared_if_passes": "LRV_PROJECTOR_STRESS_ACCOUNTING",
        "current_status": "retained_debt",
        "pass_criterion_for_484": "write stress ledger tied to parent variation",
        "failure_effect": "Bianchi/local-GR claim forbidden",
        "valid_for_claim": "false",
    },
    {
        "identity_id": "LZ7_no_total_alpha3_cancellation",
        "required_identity": "alpha3 total can vanish only after individual channels pass or a parent identity forces exact cancellation before fitting",
        "minimal_form": "alpha3_boundary=0 and alpha3_domain=0, or S_parent identity enforces their cancellation independent of data",
        "residual_components_cleared_if_passes": "LRV_TOTAL_ALPHA3_GUARD",
        "current_status": "guard_active",
        "pass_criterion_for_484": "do not use cancellation unless identity is derived before scoring",
        "failure_effect": "total alpha3 cannot be used as a shortcut",
        "valid_for_claim": "false",
    },
]


FILL_FALLBACK_ROWS = [
    {
        "fallback_id": "NF0_use_only_after_derivation_attempt",
        "policy": "numeric fills are allowed only as labelled closure fallback unless parent identities fail or user pivots",
        "affected_rows": "all 482 local residual vector components",
        "minimum_input": "numeric value or theorem-zero certificate, source file, formula reference, units, assumptions",
        "claim_ceiling": "bounded closure / empirical screen only",
        "next_action": "do not start fills before 484 unless explicitly choosing closure route",
    },
    {
        "fallback_id": "NF1_alpha3_individual_first",
        "policy": "boundary and domain alpha3 must pass individually; total cancellation is not a fill strategy",
        "affected_rows": "LRV_BOUNDARY_R7_ALPHA3;LRV_DOMAIN_R7_ALPHA3;LRV_TOTAL_ALPHA3_GUARD",
        "minimum_input": "abs(W_i_alpha3 epsilon_i_flux)<=4e-20 or accepted theorem-zero certificate",
        "claim_ceiling": "alpha3 closure score only; no derived GR",
        "next_action": "rerun alpha3 evaluator only after product rows exist",
    },
    {
        "fallback_id": "NF2_domain_siblings",
        "policy": "domain alpha3 cannot pass while alpha1/alpha2/xi/R11 siblings are unfilled",
        "affected_rows": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R8_XI;LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "minimum_input": "domain vector/anisotropy/operator coefficients or parent zero certificates",
        "claim_ceiling": "domain closure score only",
        "next_action": "fill sibling rows together if closure route is chosen",
    },
    {
        "fallback_id": "NF3_local_data_runner",
        "policy": "local-data runner is meaningful only after a numeric residual vector exists",
        "affected_rows": "all local PPN/Newton components",
        "minimum_input": "complete candidate residual vector, including GR/null baseline in same pipeline",
        "claim_ceiling": "empirical compatibility screen, not theory proof",
        "next_action": "defer long-run tests",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_fork",
        "status": "derivation_first",
        "meaning": "the goal is GR/Newton reduction from a parent theory, so the next move is the parent local-zero clause attempt, not numeric closure fills",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_numeric_fill",
        "status": "fallback_only",
        "meaning": "numeric fills remain useful for closure discipline and later testing but cannot by themselves promote local GR",
        "next_action": "activate only if 484 fails or the project deliberately pivots to empirical closure",
    },
    {
        "decision_id": "D2_alpha3_refresh",
        "status": "deferred",
        "meaning": "alpha3 evaluator refresh is blocked until at least one product or theorem-zero row exists",
        "next_action": "do not rerun 477/483-alpha3 evaluator yet",
    },
    {
        "decision_id": "D3_claims",
        "status": "forbidden",
        "meaning": "no source-normalized Newton, PPN, alpha3, mu_extra-zero, or local-GR claim is earned by this fork decision",
        "next_action": "keep 482 residual vector as active gate",
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PARENT_LOCAL_ZERO",
        "previous_target": "483-parent-action-local-zero-or-fill-decision.md",
        "decision": "selected",
        "next_target": NEXT_TARGET,
        "claim_status": "attempt_only_no_promotion",
    },
    {
        "route_id": "NUMERIC_FILL",
        "previous_target": "482 residual vector",
        "decision": "fallback",
        "next_target": "closure fill pack only after parent route fails/pivots",
        "claim_status": "closure_only",
    },
    {
        "route_id": "ALPHA3_EVALUATOR_REFRESH",
        "previous_target": "483-alpha3-product-evaluator-refresh.md",
        "decision": "deferred",
        "next_target": "after product/certificate rows are filled",
        "claim_status": "blocked_now",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def validation_rows(source_register: list[dict[str, str]]) -> list[dict[str, str]]:
    local_vector = read_csv(LOCAL_VECTOR_PATH)
    qcoh_contract = read_csv(QCOH_CONTRACT_PATH)
    missing_sources = [row["source_file"] for row in source_register if row["exists"] != "True"]
    failed_components = [row for row in local_vector if row.get("passes_required_gate") != "true"]
    parent_claim_rows = [row for row in qcoh_contract if row.get("valid_for_local_GR_claim") == "true"]
    selected_forks = [row for row in FORK_SCORECARD_ROWS if row["decision"] == "selected_next"]
    return [
        {
            "rule_id": "V483_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V483_1_residual_vector_loaded",
            "rule": "482 local residual vector is loaded and still has no passing claim rows",
            "result": "pass" if local_vector and failed_components else "fail",
            "evidence": f"local_vector_rows={len(local_vector)}; failed_components={len(failed_components)}",
            "claim_effect": "fork is based on active residual evidence",
        },
        {
            "rule_id": "V483_2_parent_not_promoted",
            "rule": "Qcoh parent contract has no local-GR claim-valid rows",
            "result": "pass" if not parent_claim_rows else "fail",
            "evidence": f"parent_claim_rows={len(parent_claim_rows)}",
            "claim_effect": "no hidden derivation claim",
        },
        {
            "rule_id": "V483_3_derivation_first_selected",
            "rule": "exactly one fork is selected and it is parent local-zero",
            "result": "pass" if len(selected_forks) == 1 and selected_forks[0]["fork_id"] == "F0_parent_local_zero" else "fail",
            "evidence": ";".join(row["fork_id"] for row in selected_forks),
            "claim_effect": "next route is aligned with GR/Newton derivation objective",
        },
        {
            "rule_id": "V483_4_fill_labelled_fallback",
            "rule": "numeric fill route is retained but labelled closure-only",
            "result": "pass",
            "evidence": "F1_numeric_fill=fallback_only; NF rows claim_ceiling closure",
            "claim_effect": "no closure mistaken for derivation",
        },
        {
            "rule_id": "V483_5_no_promotion",
            "rule": "fork decision grants no Newton/PPN/local-GR promotion",
            "result": "pass",
            "evidence": STATUS,
            "claim_effect": "decision gate only",
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
    return f"""# 483 - Parent Action Local Zero Or Fill Decision

Private fork-decision checkpoint. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `482` made the local-GR failure mode explicit:

```text
11 retained local residual components;
0 claim-valid components;
no Newton/PPN/local-GR promotion.
```

This checkpoint decides the next route.

Because the project goal is not merely a fitted local closure but a derivable GR/Newton limit, the next move is:

```text
attempt the parent-action local-zero clause.
```

Numeric fills remain useful, but only as labelled closure fallback.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_action_local_zero_or_fill_decision.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Fork Scorecard

{markdown_table(FORK_SCORECARD_ROWS)}

The scorecard decision is not emotional optimism. It is tactical:

```text
numeric fills can test a closure;
only parent local-zero can derive GR/Newton.
```

So the next punch is derivation-first.

## 5. Required Parent Local-Zero Identities

{markdown_table(REQUIRED_IDENTITIES_ROWS)}

The exact target for `484` is therefore:

```text
S_parent must force Q, P_coh, chi_D/D, local X_D=0, R11 silence,
boundary no-flux, and stress/Bianchi accounting without importing a plateau axiom.
```

If that cannot be written without smuggling in the desired zero, the route gets demoted.

## 6. Numeric Fill Fallback Policy

{markdown_table(FILL_FALLBACK_ROWS)}

This fallback is not shameful. It is just a different claim type:

```text
closure compatibility, not derived local GR.
```

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The next local-GR move is parent-action local-zero derivation first.
Numeric residual-vector fills remain available as closure fallback.
The exact identities required for derivation are enumerated.
```

Forbidden:

```text
MTS has derived local GR.
MTS has derived the Newtonian limit.
MTS passes PPN.
MTS has alpha3=0 or mu_extra=0.
Numeric fills count as field-theory derivation.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | attempt the actual parent local-zero action clause and either derive it or reject it |
| 2 | closure fill pack | only if the parent local-zero route fails or is explicitly deferred |
| 3 | alpha3 evaluator refresh | only after theorem-zero certificates or numeric products exist |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-parent-action-local-zero-or-fill-decision"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(FORK_SCORECARD_PATH, FORK_SCORECARD_ROWS)
    write_csv(REQUIRED_IDENTITIES_PATH, REQUIRED_IDENTITIES_ROWS)
    write_csv(FILL_FALLBACK_PATH, FILL_FALLBACK_ROWS)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    local_vector = read_csv(LOCAL_VECTOR_PATH)
    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "fork_scorecard": str(ROOT / FORK_SCORECARD_PATH),
        "required_identities": str(ROOT / REQUIRED_IDENTITIES_PATH),
        "fill_fallback_policy": str(ROOT / FILL_FALLBACK_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "local_vector_rows": len(local_vector),
        "failed_component_count": sum(1 for row in local_vector if row.get("passes_required_gate") != "true"),
        "fork_rows": len(FORK_SCORECARD_ROWS),
        "selected_fork": "F0_parent_local_zero",
        "required_identity_rows": len(REQUIRED_IDENTITIES_ROWS),
        "fill_fallback_rows": len(FILL_FALLBACK_ROWS),
        "validation_rows": len(validations),
        "decision_rows": len(DECISION_ROWS),
        "route_update_rows": len(ROUTE_UPDATE_ROWS),
        "derivation_first_selected": True,
        "numeric_fill_selected": False,
        "numeric_fill_allowed_as_closure_fallback": True,
        "alpha3_evaluator_refresh_allowed": False,
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
