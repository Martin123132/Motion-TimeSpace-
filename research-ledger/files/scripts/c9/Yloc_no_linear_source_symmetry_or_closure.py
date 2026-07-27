from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Yloc_no_linear_source_conditional_theorem_written_naive_composite_reflection_rejected_parent_Z2_not_derived_closure_still_required"
CLAIM_CEILING = "conditional_no_linear_source_symmetry_contract_only_no_Yloc_zero_R11_EH_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "492-silence-auxiliary-parent-action-construction-or-closure.md"

DOC_PATH = Path("491-Yloc-no-linear-source-symmetry-or-closure.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv")
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv")
COMPONENT_AUDIT_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_COMPONENT_AUDIT.csv")
COUNTEREXAMPLES_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_COUNTEREXAMPLES.csv")
CLOSURE_DEMOTION_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_CLOSURE_DEMOTION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_ROUTE_UPDATE.csv")

SOURCE_CURRENT_AUDIT_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_COMPONENT_AUDIT.csv")
CLOSURE_FILL_PATH = Path("source-intake/mts_residuals/P8_YLOC_SOURCE_CURRENT_CLOSURE_FILL.csv")
EULER_SYSTEM_PATH = Path("source-intake/mts_residuals/P8_YLOC_EULER_SYSTEM.csv")


SOURCE_REGISTER = [
    {
        "source_file": "489-local-silence-multiplet-Euler-equations-or-closure.md",
        "role": "positive no-source theorem requiring J_Y=0 and B_Y=0",
    },
    {
        "source_file": "490-Yloc-source-current-Noether-zero-or-closure-fill.md",
        "role": "Noether/Ward ownership gate and no-linear-source target",
    },
    {
        "source_file": "488-double-zero-R11-selector-parent-clause-or-demotion.md",
        "role": "composite squared selector that becomes useful only after Y_loc=0",
    },
    {
        "source_file": "487-local-EH-R11-selector-theorem-attempt.md",
        "role": "double-zero variation sufficiency and single-zero rejection",
    },
    {
        "source_file": "12-gauge-noether-origin-audit.md",
        "role": "Noether identity warning: symmetry identities do not automatically set fields to zero",
    },
    {
        "source_file": "207-domain-projector-action-and-Bianchi-identity.md",
        "role": "Bianchi ledger with retained projector/domain/boundary stresses",
    },
    {
        "source_file": str(SOURCE_CURRENT_AUDIT_PATH),
        "role": "current source-current blockers from checkpoint 490",
    },
    {
        "source_file": str(CLOSURE_FILL_PATH),
        "role": "fallback fill rows if symmetry route fails",
    },
    {
        "source_file": str(EULER_SYSTEM_PATH),
        "role": "Y_loc component list from checkpoint 489",
    },
    {
        "source_file": "scripts/Yloc_no_linear_source_symmetry_or_closure.py",
        "role": "this checkpoint generator",
    },
]


THEOREM_ROWS = [
    {
        "step_id": "T0_local_expansion",
        "statement": "Expand the parent local action around the compact local branch in variables y^A that map to Y_loc^A.",
        "math_form": "S = S_0 + integral sqrt(h)[L_A y^A + 1/2 y^A L_AB y^B + ...] + boundary terms",
        "result": "linear coefficients L_A are the source currents J_Y and boundary B_Y",
        "valid_for_claim": "false",
    },
    {
        "step_id": "T1_exact_reflection",
        "statement": "If an exact parent branch symmetry sends y^A -> -y^A while holding physical local observables fixed, the action is even in y.",
        "math_form": "S[y,g,psi] = S[-y,g,psi]",
        "result": "all odd terms vanish, so L_A = 0 at y=0",
        "valid_for_claim": "false",
    },
    {
        "step_id": "T2_boundary_evenness",
        "statement": "If the boundary/collar action is also even or stationary with no marker sources, the linear boundary variation vanishes.",
        "math_form": "delta S_boundary/delta y^A at y=0 = 0",
        "result": "B_Y=0",
        "valid_for_claim": "false",
    },
    {
        "step_id": "T3_positive_operator",
        "statement": "With positive local Hessian, the 489 energy identity forces y^A=0.",
        "math_form": "integral[(nabla y)^2 + m^2 y^2] = 0",
        "result": "conditional Y_loc zero theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "T4_composite_lock",
        "statement": "The auxiliary variables must be locked to the actual composite local residuals through PPN order.",
        "math_form": "y^A = Y_loc^A + O(PPN beyond gate)",
        "result": "needed before the theorem clears alpha3, mu_extra, R11, or local GR",
        "valid_for_claim": "false",
    },
    {
        "step_id": "T5_current_corpus",
        "statement": "The current corpus does not yet derive the exact reflection, matter neutrality, boundary evenness, and composite lock.",
        "math_form": "missing C0/C1/C2/C3/C4/C5 parent certificates",
        "result": "conditional theorem only; no promotion",
        "valid_for_claim": "false",
    },
]


CONTRACT_ROWS = [
    {
        "clause_id": "C0_true_auxiliary_variables",
        "required_clause": "Introduce genuine parent variables y^A, not only post-hoc composite diagnostics.",
        "why_needed": "a reflection symmetry is meaningful for independent variables, not automatically for derived residuals",
        "current_status": "not_derived",
        "failure_effect": "naive Y_loc -> -Y_loc is only notation",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C1_exact_Z2_or_selection_rule",
        "required_clause": "Parent action must be invariant under y^A -> -y^A on the compact local branch.",
        "why_needed": "forbids linear source terms J_A y^A",
        "current_status": "conditional_written_not_sourced",
        "failure_effect": "J_Y can be nonzero while Noether/Bianchi still hold",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C2_matter_neutrality",
        "required_clause": "Matter couples only to the physical metric/coframe and not linearly to y^A.",
        "why_needed": "ordinary matter trace, tidal fields, or source normalization can act as linear sources",
        "current_status": "not_derived",
        "failure_effect": "compact bodies source y^A and leave PPN hair",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C3_boundary_even_or_no_flux",
        "required_clause": "Boundary/collar terms are even in y^A or have stationary no-flux conditions.",
        "why_needed": "removes B_Y and preferred-frame boundary leakage",
        "current_status": "not_derived",
        "failure_effect": "alpha3 boundary term remains open",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C4_positive_hessian",
        "required_clause": "The quadratic y^A operator is positive on compact local domains after gauge/constraint modes are removed.",
        "why_needed": "turns zero source into y^A=0 rather than a flat direction",
        "current_status": "partly_formal_from_489",
        "failure_effect": "local branch may have unsuppressed zero modes",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C5_composite_residual_lock",
        "required_clause": "The auxiliary y^A variables equal the actual residual components X_D, Phi_boundary, V_domain, S_TF, Delta_mu, and Bianchi stress through the local PPN gate.",
        "why_needed": "otherwise the theorem zeros a bookkeeping field rather than physical local residuals",
        "current_status": "not_derived",
        "failure_effect": "R11, alpha3, mu_extra, and local GR remain unproved",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C6_extra_stress_accounting",
        "required_clause": "Any stress not killed by symmetry is topological, exactly conserved and invisible, or explicitly retained and bounded.",
        "why_needed": "Bianchi consistency alone allows extra conserved stress",
        "current_status": "retained_debt",
        "failure_effect": "EH-only local exterior is not derived",
        "valid_for_claim": "false",
    },
]


COMPONENT_AUDIT_ROWS = [
    {
        "component_id": "Y0_trace_expansion",
        "Y_component": "X_D",
        "symmetry_result": "conditional_only",
        "reason": "a scalar trace residual can have a linear matter-trace source unless matter neutrality and branch stationarity are derived",
        "needed_contract_clauses": "C1;C2;C4;C5",
        "blocks": "coherent trace-load source",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y1_coherent_projector",
        "Y_component": "Qcoh_D - h X_D/3",
        "symmetry_result": "conditional_only",
        "reason": "projector stress can be linearly sourced by anisotropic or domain data unless composite lock and stress accounting are proved",
        "needed_contract_clauses": "C1;C5;C6",
        "blocks": "LRV_QCOH_PROJECTOR_OWNERSHIP;LRV_PROJECTOR_STRESS_ACCOUNTING",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y2_boundary_flux",
        "Y_component": "Phi_boundary^i",
        "symmetry_result": "not_zeroed",
        "reason": "boundary/collar markers can source a vector flux unless the boundary action is scalar, even, and no-flux",
        "needed_contract_clauses": "C1;C3;C5",
        "blocks": "LRV_BOUNDARY_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y3_domain_vector",
        "Y_component": "V_domain^i",
        "symmetry_result": "not_zeroed",
        "reason": "a covariant domain vector is allowed if the domain carries a marker vector; Z2 must be backed by no-vector domain selection",
        "needed_contract_clauses": "C1;C2;C5",
        "blocks": "LRV_DOMAIN_R5_ALPHA1;LRV_DOMAIN_R6_ALPHA2;LRV_DOMAIN_R7_ALPHA3",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y4_domain_STF_stress",
        "Y_component": "S_TF_domain^{ij}",
        "symmetry_result": "not_zeroed",
        "reason": "STF stress can couple linearly to a tidal STF tensor unless isotropy/topological stress is derived",
        "needed_contract_clauses": "C1;C2;C5;C6",
        "blocks": "LRV_DOMAIN_R8_XI;LRV_PROJECTOR_STRESS_ACCOUNTING",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y5_source_normalization",
        "Y_component": "Delta_mu_source",
        "symmetry_result": "not_zeroed",
        "reason": "a scalar source-normalization offset is not killed by parity unless measured-GM neutrality and composite lock are proved",
        "needed_contract_clauses": "C1;C2;C5",
        "blocks": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y6_stress_Bianchi",
        "Y_component": "nabla_mu T_extra^{mu nu}",
        "symmetry_result": "retained_not_zeroed",
        "reason": "a divergence identity is not an independent odd field; extra stress can be conserved but nonzero",
        "needed_contract_clauses": "C5;C6",
        "blocks": "LRV_PROJECTOR_STRESS_ACCOUNTING;LRV_TOTAL_ALPHA3_GUARD",
        "valid_for_claim": "false",
    },
]


COUNTEREXAMPLE_ROWS = [
    {
        "counterexample_id": "CE0_conserved_scalar_source",
        "toy_action": "S = integral sqrt(h)[1/2 m^2 y^2 + epsilon y]",
        "why_allowed_without_contract": "epsilon can be a scalar source owned by the Ward ledger",
        "failure": "Euler equation gives y = -epsilon/m^2, not y=0",
        "forbidden_by": "C1_exact_Z2_or_selection_rule;C2_matter_neutrality",
    },
    {
        "counterexample_id": "CE1_boundary_marker_vector",
        "toy_action": "S_boundary = integral_boundary epsilon_i Phi^i",
        "why_allowed_without_contract": "boundary/collar data can carry a preferred vector marker",
        "failure": "B_Y is nonzero and can feed alpha3",
        "forbidden_by": "C3_boundary_even_or_no_flux",
    },
    {
        "counterexample_id": "CE2_tidal_STF_source",
        "toy_action": "S = integral sqrt(h) E_ij S_TF^ij",
        "why_allowed_without_contract": "E_ij S_TF^ij is a scalar and can respect covariance",
        "failure": "STF stress is sourced even though Bianchi accounting can close",
        "forbidden_by": "C2_matter_neutrality;C6_extra_stress_accounting",
    },
    {
        "counterexample_id": "CE3_source_normalization_offset",
        "toy_action": "S = integral sqrt(h) epsilon Delta_mu_source",
        "why_allowed_without_contract": "a scalar source offset can be conserved and still nonzero",
        "failure": "mu_extra or R11 normalization hair remains",
        "forbidden_by": "C2_matter_neutrality;C5_composite_residual_lock",
    },
]


CLOSURE_DEMOTION_ROWS = [
    {
        "closure_id": "CL0_symmetry_route_status",
        "if_missing": "any of C0-C6",
        "demotion": "no-linear-source route remains an explicit parent-action contract, not a derived theorem",
        "fallback": "use 490 closure fill rows",
        "valid_for_claim": "false",
    },
    {
        "closure_id": "CL1_boundary_alpha3",
        "if_missing": "C3",
        "demotion": "boundary flux must be bounded numerically or by a separate no-flux theorem",
        "fallback": "W_boundary_alpha3_epsilon_boundary_flux",
        "valid_for_claim": "false",
    },
    {
        "closure_id": "CL2_domain_preferred_frame",
        "if_missing": "C1 or C2 or C5",
        "demotion": "domain vector terms must be retained in alpha1, alpha2, and alpha3 residual vector",
        "fallback": "W_domain_alpha1/alpha2/alpha3 products",
        "valid_for_claim": "false",
    },
    {
        "closure_id": "CL3_projector_STF_stress",
        "if_missing": "C5 or C6",
        "demotion": "STF/projector stress must be retained or bounded",
        "fallback": "W_domain_xi_epsilon_domain_anisotropy plus T_extra residual",
        "valid_for_claim": "false",
    },
    {
        "closure_id": "CL4_source_normalization",
        "if_missing": "C2 or C5",
        "demotion": "source-normalization operator remains a fit/closure debt rather than Newton-derived",
        "fallback": "c_domain_source_normalization_operator",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_conditional_theorem",
        "status": "written",
        "meaning": "an exact parent evenness/no-linear-source symmetry would zero J_Y and B_Y and activate the 489 positive theorem",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_naive_reflection",
        "status": "rejected",
        "meaning": "writing Y_loc -> -Y_loc on composite residuals is not enough; it must be an actual parent variable symmetry",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_current_corpus",
        "status": "not_derived",
        "meaning": "matter neutrality, boundary evenness, composite lock, and extra-stress accounting are still open",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Yloc zero, R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "continue parent-action construction or closure fill",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "YLOC_SOURCE_CURRENT",
        "previous_status": "Noether_ownership_not_zero_no_linear_source_symmetry_needed",
        "new_status": "conditional_no_linear_source_theorem_contract_written_not_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "DOUBLE_ZERO_R11_SELECTOR",
        "previous_status": "requires_no_linear_source_or_closure_fills",
        "new_status": "requires_auxiliary_parent_Z2_and_composite_lock",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_unzeroed_Yloc_source_currents",
        "new_status": "blocked_by_missing_parent_symmetry_contract_C0_to_C6",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        exists = (ROOT / row["source_file"]).exists()
        rows.append({**row, "exists": str(exists)})
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row for row in sources if row["exists"] != "True"]
    current_rows = read_csv(SOURCE_CURRENT_AUDIT_PATH)
    closure_rows = read_csv(CLOSURE_FILL_PATH)
    euler_rows = read_csv(EULER_SYSTEM_PATH)
    claim_theorem_rows = [row for row in THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_component_rows = [row for row in COMPONENT_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    required_contract = {f"C{index}" for index in range(7)}
    contract_ids = {row["clause_id"].split("_", 1)[0] for row in CONTRACT_ROWS}
    required_components = {
        "Y0_trace_expansion",
        "Y1_coherent_projector",
        "Y2_boundary_flux",
        "Y3_domain_vector",
        "Y4_domain_STF_stress",
        "Y5_source_normalization",
        "Y6_stress_Bianchi",
    }
    component_ids = {row["component_id"] for row in COMPONENT_AUDIT_ROWS}

    return [
        {
            "rule_id": "V491_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V491_1_inputs_loaded",
            "rule": "490 current audit, 490 closure fills, and 489 Euler system are loaded",
            "result": "pass" if len(current_rows) == 6 and len(closure_rows) == 5 and len(euler_rows) == 7 else "fail",
            "evidence": f"current_rows={len(current_rows)};closure_rows={len(closure_rows)};euler_rows={len(euler_rows)}",
            "claim_effect": "symmetry test is tied to current blockers",
        },
        {
            "rule_id": "V491_2_contract_complete",
            "rule": "parent symmetry contract lists clauses C0 through C6",
            "result": "pass" if required_contract.issubset(contract_ids) else "fail",
            "evidence": ";".join(sorted(contract_ids)),
            "claim_effect": "exact contract is explicit",
        },
        {
            "rule_id": "V491_3_component_coverage",
            "rule": "component audit covers all Yloc Euler components",
            "result": "pass" if required_components.issubset(component_ids) else "fail",
            "evidence": ";".join(sorted(component_ids)),
            "claim_effect": "no hidden local residual skipped",
        },
        {
            "rule_id": "V491_4_counterexamples_written",
            "rule": "counterexamples show why naive symmetry is insufficient",
            "result": "pass" if len(COUNTEREXAMPLE_ROWS) >= 4 else "fail",
            "evidence": f"counterexamples={len(COUNTEREXAMPLE_ROWS)}",
            "claim_effect": "prevents smuggled zero-source axiom",
        },
        {
            "rule_id": "V491_5_no_claim_rows",
            "rule": "no theorem or component row is claim-valid",
            "result": "pass" if not claim_theorem_rows and not claim_component_rows else "fail",
            "evidence": f"claim_valid_theorem_rows={len(claim_theorem_rows)};claim_valid_component_rows={len(claim_component_rows)}",
            "claim_effect": "no local-GR promotion",
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


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 491 - Yloc No-Linear-Source Symmetry Or Closure

Private local-GR/Newton/PPN parent-symmetry checkpoint. This is not a public Yloc-zero proof, EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `490` showed that Noether/Ward identities own source currents but do not set them to zero. The next possible move is stronger:

```text
an exact parent local-silence symmetry forbids all terms linear in Y_loc.
```

This checkpoint derives the conditional theorem and then stress-tests whether the current corpus actually has that symmetry.

Short answer:

```text
Conditional theorem: yes.
Current derived MTS parent symmetry: not yet.
Naive composite reflection Y_loc -> -Y_loc: rejected as insufficient.
```

The theory now has a precise contract, not a free pass.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Yloc_no_linear_source_symmetry_or_closure.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Conditional No-Linear-Source Theorem

{markdown_table(THEOREM_ROWS)}

The useful theorem is:

```text
S[y,g,psi] = S[-y,g,psi]
```

with even/stationary boundary terms and matter neutrality. Then the local expansion cannot contain:

```text
integral sqrt(h) J_A y^A
```

or a boundary linear term. Therefore:

```text
J_Y = 0,
B_Y = 0.
```

Combined with the positive identity from checkpoint `489`, this would force:

```text
Y_loc^A = 0.
```

But only if the parent clauses below are real.

## 5. Parent Symmetry Contract

{markdown_table(CONTRACT_ROWS)}

## 6. Component Audit

{markdown_table(COMPONENT_AUDIT_ROWS)}

## 7. Counterexamples To Naive Symmetry

{markdown_table(COUNTEREXAMPLE_ROWS)}

These are not claims about nature. They are guardrails: they show that covariance, conservation, and a written reflection symbol are not enough to force the local residuals to zero.

## 8. Closure Demotion If Contract Fails

{markdown_table(CLOSURE_DEMOTION_ROWS)}

## 9. Validation

{markdown_table(validations)}

## 10. Decision

{markdown_table(DECISION_ROWS)}

## 11. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 12. Claim Ceiling

Allowed:

```text
An exact parent no-linear-source symmetry would be sufficient to zero Yloc source currents.
The current corpus now has the exact contract such a parent action must satisfy.
The naive composite reflection route is rejected unless promoted to a genuine parent variable symmetry.
```

Forbidden:

```text
MTS has derived the no-linear-source symmetry.
MTS has derived Y_loc=0.
MTS has derived J_Y=0 or B_Y=0.
MTS has derived EH/R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
MTS has alpha3=0 or mu_extra=0.
```

## 13. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | try to construct an auxiliary parent action whose actual Euler equations and symmetries satisfy C0-C6 |
| 2 | closure fill pack | if the auxiliary parent action cannot satisfy the contract |
| 3 | local PPN residual certificate | only after source currents and boundary terms are zero/bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Yloc-no-linear-source-symmetry-or-closure"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_PATH, THEOREM_ROWS)
    write_csv(CONTRACT_PATH, CONTRACT_ROWS)
    write_csv(COMPONENT_AUDIT_PATH, COMPONENT_AUDIT_ROWS)
    write_csv(COUNTEREXAMPLES_PATH, COUNTEREXAMPLE_ROWS)
    write_csv(CLOSURE_DEMOTION_PATH, CLOSURE_DEMOTION_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_theorem_rows = [row for row in THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_component_rows = [row for row in COMPONENT_AUDIT_ROWS if row["valid_for_claim"] == "true"]
    contract_unproved_rows = [row for row in CONTRACT_ROWS if row["current_status"] != "derived"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem": str(ROOT / THEOREM_PATH),
        "contract": str(ROOT / CONTRACT_PATH),
        "component_audit": str(ROOT / COMPONENT_AUDIT_PATH),
        "counterexamples": str(ROOT / COUNTEREXAMPLES_PATH),
        "closure_demotion": str(ROOT / CLOSURE_DEMOTION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "theorem_rows": len(THEOREM_ROWS),
        "contract_rows": len(CONTRACT_ROWS),
        "component_audit_rows": len(COMPONENT_AUDIT_ROWS),
        "counterexample_rows": len(COUNTEREXAMPLE_ROWS),
        "closure_demotion_rows": len(CLOSURE_DEMOTION_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_theorem_rows": len(claim_theorem_rows),
        "claim_valid_component_rows": len(claim_component_rows),
        "contract_unproved_rows": len(contract_unproved_rows),
        "conditional_no_linear_source_theorem_written": True,
        "naive_composite_reflection_rejected": True,
        "parent_Z2_symmetry_derived": False,
        "matter_neutrality_derived": False,
        "boundary_evenness_derived": False,
        "composite_residual_lock_derived": False,
        "extra_stress_accounting_closed": False,
        "Yloc_Euler_equations_derived": False,
        "Yloc_source_currents_zeroed": False,
        "boundary_terms_zeroed": False,
        "R11_silence_derived": False,
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
