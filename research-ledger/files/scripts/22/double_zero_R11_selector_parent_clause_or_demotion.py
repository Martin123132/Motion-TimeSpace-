from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "double_zero_R11_parent_clause_attempt_written_composite_squared_selector_sufficient_not_parent_derived_no_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "conditional_composite_squared_selector_parent_clause_only_Yloc_Euler_equations_not_derived_no_EH_R11_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "489-local-silence-multiplet-Euler-equations-or-closure.md"

DOC_PATH = Path("488-double-zero-R11-selector-parent-clause-or-demotion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_PARENT_SOURCE_REGISTER.csv")
PARENT_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_PARENT_CLAUSE.csv")
VARIATION_PROOF_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_VARIATION_PROOF.csv")
OPERATOR_MAPPING_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv")
GATE_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_GATES.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_DOUBLE_ZERO_R11_ROUTE_UPDATE.csv")

SELECTOR_LEMMA_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv")
OPERATOR_AUDIT_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv")
R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")


SOURCE_REGISTER = [
    {
        "source_file": "487-local-EH-R11-selector-theorem-attempt.md",
        "role": "double-zero sufficiency lemma and actual R11 rows not selected",
    },
    {
        "source_file": "486-R11-boundary-stress-theorem-or-closure-fill-pack.md",
        "role": "local EH/R11 selector theorem target and closure fill pack",
    },
    {
        "source_file": "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "role": "shortcut rejection and missing boundary/R11/stress premises",
    },
    {
        "source_file": "484-parent-local-zero-action-clause-attempt.md",
        "role": "local-zero trace-load input X=nabla.u and Qcoh=hX/3",
    },
    {
        "source_file": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "EH-only/R11 fork and operator family ledger",
    },
    {
        "source_file": str(SELECTOR_LEMMA_PATH),
        "role": "machine-readable double-zero lemma",
    },
    {
        "source_file": str(OPERATOR_AUDIT_PATH),
        "role": "machine-readable R11 selector audit",
    },
    {
        "source_file": str(R11_VECTOR_PATH),
        "role": "actual R11 operator-family rows",
    },
    {
        "source_file": "scripts/double_zero_R11_selector_parent_clause_or_demotion.py",
        "role": "this checkpoint generator",
    },
]


PARENT_CLAUSE_ROWS = [
    {
        "clause_id": "C0_local_silence_multiplet",
        "object": "Y_loc^A",
        "candidate_form": "Y_loc^A={X_D, Qcoh_D, Phi_boundary^i, V_domain^i, S_TF_domain, Delta_mu_source, ...}",
        "what_it_would_own": "all local channels that must vanish before non-EH operators are locally silent",
        "why_not_yet_claim": "the parent Euler equations that force every component of Y_loc^A to zero are not derived",
        "status": "sufficient_multiplet_contract",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C1_composite_squared_selector",
        "object": "Sigma_loc",
        "candidate_form": "Sigma_loc = G_AB(g,u,D) Y_loc^A Y_loc^B >= 0",
        "what_it_would_own": "double-zero behavior without treating Sigma_loc as an independent switch",
        "why_not_yet_claim": "G_AB positivity, branch locality, and Y_loc ownership are still theorem targets",
        "status": "conditional_mechanism",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C2_R11_factorization",
        "object": "S_R11_local",
        "candidate_form": "S_R11_local = int sqrt(-g) sum_A c_A Sigma_loc O_A[g,psi] + S_top",
        "what_it_would_own": "all non-topological R11 families vanish to first variation when Y_loc^A=0",
        "why_not_yet_claim": "the corpus does not yet derive that every R11 coefficient is multiplied by the same Sigma_loc",
        "status": "sufficient_parent_clause_candidate",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C3_no_independent_multiplier",
        "object": "forbidden_closure_switch",
        "candidate_form": "do not introduce Lambda_Sigma Sigma_loc as an independent constraint unless Lambda_Sigma=0 is also derived",
        "what_it_would_own": "prevents multiplier stress from undoing the double-zero proof",
        "why_not_yet_claim": "a full stress/Bianchi variation is still required",
        "status": "guard",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "C4_branch_selectivity",
        "object": "local_vs_cosmological_activation",
        "candidate_form": "Sigma_loc=0 in compact stationary local domains; Sigma_FLRW or long-memory invariants may remain active cosmologically",
        "what_it_would_own": "keeps local GR silence from killing empirical cosmology/galaxy branches by hand",
        "why_not_yet_claim": "the local/FLRW domain selector remains parent-unproved",
        "status": "consistency_gate",
        "valid_for_claim": "false",
    },
]


VARIATION_PROOF_ROWS = [
    {
        "step_id": "V0_assume_parent_Y_zero",
        "variation_step": "parent local branch equations imply Y_loc^A=0",
        "result": "Sigma_loc=G_AB Y^A Y^B=0",
        "claim_effect": "input assumption only; not yet derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "V1_composite_delta_zero",
        "variation_step": "delta Sigma_loc = delta G_AB Y^A Y^B + 2 G_AB Y^A delta Y^B",
        "result": "delta Sigma_loc=0 when Y_loc^A=0",
        "claim_effect": "this is the real double-zero mechanism",
        "valid_for_claim": "false",
    },
    {
        "step_id": "V2_R11_variation",
        "variation_step": "delta[Sigma_loc O_A]=Sigma_loc delta O_A + O_A delta Sigma_loc",
        "result": "delta[Sigma_loc O_A]=0 on the Y_loc^A=0 branch",
        "claim_effect": "non-topological R11 operators are locally silent if factorization is parent-owned",
        "valid_for_claim": "false",
    },
    {
        "step_id": "V3_topological_boundary_terms",
        "variation_step": "S_top or boundary scalar terms require separate no-hair/no-flux variation",
        "result": "not cleared by Sigma_loc unless included in Y_loc or proven topological",
        "claim_effect": "boundary/topological family remains conditional",
        "valid_for_claim": "false",
    },
    {
        "step_id": "V4_stress_Bianchi",
        "variation_step": "all retained projector/domain/boundary/selector stresses must be zero/topological or included in T_extra",
        "result": "not derived by factorization alone",
        "claim_effect": "local Bianchi/PPN promotion remains blocked",
        "valid_for_claim": "false",
    },
]


GATE_ROWS = [
    {
        "gate_id": "G0_Yloc_parent_owned",
        "rule": "Y_loc^A is derived from parent variables and its compact-local Euler equations force every component to zero",
        "current_result": "fail_for_claim",
        "evidence": "Y_loc multiplet written as contract only",
        "promotion_effect": "no local EH/R11 pass",
    },
    {
        "gate_id": "G1_composite_not_independent",
        "rule": "Sigma_loc is a composite squared norm, not an independently constrained switch",
        "current_result": "pass_as_clause_design",
        "evidence": "Sigma_loc=G_AB Y^A Y^B",
        "promotion_effect": "prevents single-zero/multiplier cheat but does not prove Y=0",
    },
    {
        "gate_id": "G2_all_R11_factorized",
        "rule": "every non-topological R11 family is multiplied by Sigma_loc or is absent",
        "current_result": "fail_for_claim",
        "evidence": "actual R11 rows still contain missing coefficients/selectors",
        "promotion_effect": "R11 silence not derived",
    },
    {
        "gate_id": "G3_boundary_topological_closed",
        "rule": "boundary/topological terms are either scalar no-flux/topological or included in Y_loc",
        "current_result": "fail_for_claim",
        "evidence": "boundary no-flux remains premise from 485/486",
        "promotion_effect": "alpha3 boundary channel still open",
    },
    {
        "gate_id": "G4_stress_Bianchi_closed",
        "rule": "selector/projector/domain/boundary stresses vanish or are retained with a conserved residual",
        "current_result": "fail_for_claim",
        "evidence": "stress/Bianchi ledger still retained",
        "promotion_effect": "no PPN/local-GR promotion",
    },
    {
        "gate_id": "G5_public_claim",
        "rule": "no Newton, PPN, alpha3, mu_extra-zero, EH-only, R11, or local-GR claim is made",
        "current_result": "pass",
        "evidence": "all parent clause and operator mapping rows valid_for_claim=false",
        "promotion_effect": "claim ceiling enforced",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_mechanism",
        "status": "conditional_mechanism_constructed",
        "meaning": "a composite squared local-silence multiplet can produce the needed double-zero behavior without an independent switch",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_derivation_status",
        "status": "not_parent_derived",
        "meaning": "the parent action has not yet been shown to force Y_loc^A=0 or factor every R11 family by Sigma_loc",
        "next_action": "derive Y_loc Euler equations or demote to closure coefficients",
    },
    {
        "decision_id": "D2_demotion",
        "status": "do_not_demote_fully_yet",
        "meaning": "the mechanism is mathematically coherent enough to keep as a theorem target, but not enough for claim credit",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no EH-only, R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "continue derivation-first route before numeric fallback",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "DOUBLE_ZERO_R11_SELECTOR",
        "previous_status": "sufficiency_lemma_only",
        "new_status": "composite_squared_parent_clause_candidate",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_EH_R11",
        "previous_status": "actual_R11_rows_unselected",
        "new_status": "factorization_mechanism_written_Yloc_Euler_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "CLOSURE_FILL",
        "previous_status": "fallback_if_selector_not_derived",
        "new_status": "deferred_but_still_required_if_Yloc_fails",
        "accepted_for_claim": "false",
        "next_target": "R11_closure_coefficients_if_489_fails",
    },
]


SELECTOR_REQUIREMENTS = {
    "boundary_topological_terms": "topological/boundary scalar no-hair or Sigma_loc boundary component",
    "R2_fR_scalar_mode": "c_R2(Sigma_loc)=c_R2_bar Sigma_loc or higher order",
    "Ricci_Weyl_squared": "Gauss-Bonnet/topological route or c_quad(Sigma_loc)=c_bar Sigma_loc",
    "scalar_tensor_class_metric": "F_phi_C derivatives vanish locally or coupling proportional to Sigma_loc",
    "vector_preferred_frame": "domain/vector marker included in Y_loc or coefficient proportional to Sigma_loc",
    "torsion_nonmetricity": "Levi-Civita branch or torsion/nonmetricity coupling proportional to Sigma_loc",
    "bulk_X_force_law": "bulk source charge included in Y_loc or q_X proportional to Sigma_loc",
    "nonlocal_memory_kernel": "compact-local kernel norm included in Y_loc or K_norm proportional to Sigma_loc",
    "source_normalization_operator": "Delta_mu_source included in Y_loc or c_source proportional to Sigma_loc",
    "projector_domain_stress": "projector stress component included in Y_loc or topological/metric-independent proof",
}


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


def operator_mapping_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(R11_VECTOR_PATH):
        operator_family = row.get("operator_family", "")
        rows.append(
            {
                "operator_family": operator_family,
                "coefficient_symbol": row.get("coefficient_symbol", ""),
                "current_coefficient_value": row.get("coefficient_value", ""),
                "affected_rows": row.get("affected_rows", ""),
                "required_parent_factorization": SELECTOR_REQUIREMENTS.get(operator_family, "Sigma_loc factor or executable coefficient"),
                "candidate_factorized_form": f"{row.get('coefficient_symbol', 'c_A')}(Sigma_loc)=cbar_A Sigma_loc + O(Sigma_loc^2)",
                "current_status": "factorization_contract_written_not_derived",
                "valid_for_claim": "false",
            }
        )
    return rows


def validation_rows(sources: list[dict[str, str]], operator_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row for row in sources if row["exists"] != "True"]
    r11_rows = read_csv(R11_VECTOR_PATH)
    selector_lemma_rows = read_csv(SELECTOR_LEMMA_PATH)
    has_double_zero_lemma = any(row.get("lemma_id") == "L2_double_zero_sufficient" for row in selector_lemma_rows)
    claim_parent_rows = [row for row in PARENT_CLAUSE_ROWS if row["valid_for_claim"] == "true"]
    claim_operator_rows = [row for row in operator_rows if row["valid_for_claim"] == "true"]
    expected_families = set(SELECTOR_REQUIREMENTS)
    present_families = {row.get("operator_family", "") for row in r11_rows}

    return [
        {
            "rule_id": "V488_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V488_1_double_zero_imported",
            "rule": "487 double-zero sufficiency lemma is loaded",
            "result": "pass" if has_double_zero_lemma else "fail",
            "evidence": "L2_double_zero_sufficient",
            "claim_effect": "parent clause addresses the correct leak",
        },
        {
            "rule_id": "V488_2_R11_family_coverage",
            "rule": "operator mapping covers all ten R11 families",
            "result": "pass" if expected_families.issubset(present_families) and len(operator_rows) == 10 else "fail",
            "evidence": f"operator_mapping_rows={len(operator_rows)}",
            "claim_effect": "no R11 family silently omitted",
        },
        {
            "rule_id": "V488_3_composite_selector",
            "rule": "Sigma_loc is written as a composite squared norm rather than an independent switch",
            "result": "pass",
            "evidence": "Sigma_loc=G_AB Y_loc^A Y_loc^B",
            "claim_effect": "avoids the single-zero trap conditionally",
        },
        {
            "rule_id": "V488_4_no_claim_parent_rows",
            "rule": "no parent-clause row is promoted as derived",
            "result": "pass" if not claim_parent_rows else "fail",
            "evidence": f"claim_valid_parent_clause_rows={len(claim_parent_rows)}",
            "claim_effect": "no fake parent-action pass",
        },
        {
            "rule_id": "V488_5_no_claim_operator_rows",
            "rule": "no R11 operator mapping row is claim-valid before Yloc Euler equations are derived",
            "result": "pass" if not claim_operator_rows else "fail",
            "evidence": f"claim_valid_operator_rows={len(claim_operator_rows)}",
            "claim_effect": "no EH/R11/local-GR promotion",
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
    operator_rows: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 488 - Double-Zero R11 Selector Parent Clause Or Demotion

Private local-GR/Newton/PPN parent-clause checkpoint. This is not a public EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `487` found the clean mathematical route:

```text
single-zero suppression leaks under variation;
double-zero suppression is sufficient to first variation.
```

This checkpoint asks whether the double-zero can be made less artificial by a parent-action clause.

Short answer:

```text
conditional mechanism constructed:
make the selector a composite squared norm Sigma_loc = G_AB Y_loc^A Y_loc^B.

not derived yet:
the parent action still has to force Y_loc^A=0 and factor every R11 family by Sigma_loc.
```

This is better than a hand switch because `delta Sigma_loc=0` follows when `Y_loc^A=0`.

It is not a local-GR pass because the `Y_loc` Euler equations are not derived.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/double_zero_R11_selector_parent_clause_or_demotion.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Parent Clause Candidate

{markdown_table(PARENT_CLAUSE_ROWS)}

The proposed local silence multiplet is schematic but precise enough to audit:

```text
Y_loc^A = {{X_D, Qcoh_D, Phi_boundary^i, V_domain^i, S_TF_domain, Delta_mu_source, ...}}
Sigma_loc = G_AB Y_loc^A Y_loc^B >= 0
S_R11_local = int sqrt(-g) sum_A c_A Sigma_loc O_A[g,psi] + S_top
```

The mechanism only works if `Sigma_loc` is composite. If `Sigma_loc` is an independent constrained variable, the multiplier can leak stress and the proof fails.

## 5. Variation Proof

{markdown_table(VARIATION_PROOF_ROWS)}

The key step is:

```text
delta Sigma_loc = delta G_AB Y^A Y^B + 2 G_AB Y^A delta Y^B.
```

So if the parent equations really give:

```text
Y_loc^A = 0,
```

then:

```text
Sigma_loc = 0
delta Sigma_loc = 0
delta[ Sigma_loc O_A ] = 0.
```

That is the double-zero mechanism in parent-action language.

## 6. R11 Operator Mapping

{markdown_table(operator_rows)}

Every R11 family now has a candidate parent-factorization contract.

None is accepted for claim yet.

## 7. Gates

{markdown_table(GATE_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
A composite squared local-silence selector is a coherent mechanism for the required double-zero R11 suppression.
The next derivation target is the parent Euler system for Y_loc^A=0.
```

Allowed:

```text
The route is not demoted to closure-only yet, because the parent-clause mechanism is mathematically coherent.
```

Forbidden:

```text
MTS has derived EH-only local GR.
MTS has derived R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
The R11 operator rows are claim-valid.
The composite squared selector is already parent-derived.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | derive or reject the Euler equations that force Y_loc^A=0 in compact local domains |
| 2 | R11 closure coefficient pack | if Y_loc Euler equations fail |
| 3 | local PPN residual certificate | only after R11, boundary, and stress rows are zero/bounded |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-double-zero-R11-selector-parent-clause-or-demotion"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    operator_rows = operator_mapping_rows()
    validations = validation_rows(sources, operator_rows)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PARENT_CLAUSE_PATH, PARENT_CLAUSE_ROWS)
    write_csv(VARIATION_PROOF_PATH, VARIATION_PROOF_ROWS)
    write_csv(OPERATOR_MAPPING_PATH, operator_rows)
    write_csv(GATE_PATH, GATE_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, operator_rows, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_parent_rows = [row for row in PARENT_CLAUSE_ROWS if row["valid_for_claim"] == "true"]
    claim_operator_rows = [row for row in operator_rows if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "parent_clause": str(ROOT / PARENT_CLAUSE_PATH),
        "variation_proof": str(ROOT / VARIATION_PROOF_PATH),
        "operator_mapping": str(ROOT / OPERATOR_MAPPING_PATH),
        "gate": str(ROOT / GATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "parent_clause_rows": len(PARENT_CLAUSE_ROWS),
        "variation_proof_rows": len(VARIATION_PROOF_ROWS),
        "operator_mapping_rows": len(operator_rows),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_parent_clause_rows": len(claim_parent_rows),
        "claim_valid_operator_rows": len(claim_operator_rows),
        "composite_squared_selector_written": True,
        "delta_Sigma_zero_if_Yloc_zero": True,
        "Yloc_Euler_equations_derived": False,
        "all_R11_families_factorized_by_parent": False,
        "EH_only_derived": False,
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
