from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "odd_residual_parentization_exchange_doublet_contract_written_component_map_incomplete_no_local_GR_promotion"
CLAIM_CEILING = "conditional_exchange_doublet_parentization_only_no_Yloc_zero_R11_EH_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "494-exchange-doublet-component-map-or-coefficient-branch.md"

DOC_PATH = Path("493-odd-residual-parentization-or-closure-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_PARENTIZATION_SOURCE_REGISTER.csv")
PARENTIZATION_CANDIDATES_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_PARENTIZATION_CANDIDATES.csv")
EXCHANGE_THEOREM_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv")
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv")
COMPONENT_MAP_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_COMPONENT_MAP.csv")
COUNTEREXAMPLE_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_COUNTEREXAMPLES.csv")
CLOSURE_FILL_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_CLOSURE_FILL.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_ODD_RESIDUAL_ROUTE_UPDATE.csv")

AUX_PARENT_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_YLOC_AUX_PARENT_CONTRACT_RESULT.csv")
AUX_PARENT_COMPONENT_PATH = Path("source-intake/mts_residuals/P8_YLOC_AUX_PARENT_COMPONENT_RESULT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "492-silence-auxiliary-parent-action-construction-or-closure.md",
        "role": "lock/Z2 triangle and odd residual parentization target",
    },
    {
        "source_file": "491-Yloc-no-linear-source-symmetry-or-closure.md",
        "role": "C0-C6 no-linear-source parent contract",
    },
    {
        "source_file": "490-Yloc-source-current-Noether-zero-or-closure-fill.md",
        "role": "Noether ownership not zero-current theorem",
    },
    {
        "source_file": "489-local-silence-multiplet-Euler-equations-or-closure.md",
        "role": "positive local Euler/no-source theorem",
    },
    {
        "source_file": "404-selector-blind-matter-axiom-origin.md",
        "role": "relational quotient/readout identified as strongest primitive target",
    },
    {
        "source_file": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter conditional theorem and exp(F(C_D)) counterexample",
    },
    {
        "source_file": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "matter pullback cancellation routes classified",
    },
    {
        "source_file": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common-F not parent-derived",
    },
    {
        "source_file": "299-local-silence-selector-attempt.md",
        "role": "local silence requires domain/boundary state theorem",
    },
    {
        "source_file": "475-domain-selector-parent-action-clause-or-coefficient-fill.md",
        "role": "double-zero domain selector action is sufficient but not derived",
    },
    {
        "source_file": str(AUX_PARENT_CONTRACT_PATH),
        "role": "492 C0-C6 contract result",
    },
    {
        "source_file": str(AUX_PARENT_COMPONENT_PATH),
        "role": "492 Yloc component result",
    },
    {
        "source_file": "scripts/odd_residual_parentization_or_closure_fill.py",
        "role": "this checkpoint generator",
    },
]


PARENTIZATION_CANDIDATES = [
    {
        "candidate_id": "P0_independent_odd_Z",
        "mechanism": "add independent Z^A with exchange parity Z^A -> -Z^A",
        "buys": "true odd auxiliary variables and no linear Z source",
        "fails": "no proof that Z^A equals physical Y_loc^A",
        "verdict": "bookkeeping_only",
        "valid_for_claim": "false",
    },
    {
        "candidate_id": "P1_exchange_doublet_representatives",
        "mechanism": "parent representatives R_+^A,R_-^A with exchange E: R_+ <-> R_-, Z^A=(R_+^A-R_-^A)/2",
        "buys": "Z^A is genuinely odd while the observed quotient/even geometry can be matter-visible",
        "fails": "component map Z^A=Y_loc^A is not yet derived",
        "verdict": "best_theorem_target",
        "valid_for_claim": "false",
    },
    {
        "candidate_id": "P2_gauge_sign_redundancy",
        "mechanism": "declare Z^A and -Z^A gauge-equivalent",
        "buys": "linear odd observables are forbidden",
        "fails": "if Y_loc is gauge, it cannot be a physical PPN residual; if physical, the gauge declaration is false",
        "verdict": "reject_unless_residual_is_representative_only",
        "valid_for_claim": "false",
    },
    {
        "candidate_id": "P3_odd_Lagrange_lock",
        "mechanism": "lambda_A(Y_loc^A-Z^A) with lambda_A odd",
        "buys": "formal lock",
        "fails": "metric variation carries lambda_A delta Y_loc^A and linear-source/stress debts reappear",
        "verdict": "not_clean_local_GR_route",
        "valid_for_claim": "false",
    },
    {
        "candidate_id": "P4_closure_coefficients",
        "mechanism": "do not parentize; keep residual coefficients and test them",
        "buys": "honest empirical branch",
        "fails": "not a derivation of GR/Newton",
        "verdict": "fallback",
        "valid_for_claim": "false",
    },
]


EXCHANGE_THEOREM_ROWS = [
    {
        "step_id": "E0_parent_doublet",
        "statement": "Introduce parent representative doublets R_+^A and R_-^A for every local residual channel.",
        "math_form": "E: R_+^A <-> R_-^A",
        "result": "exchange symmetry candidate",
        "valid_for_claim": "false",
    },
    {
        "step_id": "E1_even_observed_geometry",
        "statement": "Matter and clocks couple only to the exchange-even observed quotient geometry.",
        "math_form": "R_even^A=(R_+^A+R_-^A)/2; S_matter=S_matter[Psi,e_obs(R_even)]",
        "result": "would pay matter-neutrality if parent-derived",
        "valid_for_claim": "false",
    },
    {
        "step_id": "E2_odd_residual",
        "statement": "Dangerous local residuals are the exchange-odd projection.",
        "math_form": "Z^A=(R_+^A-R_-^A)/2 and Y_loc^A=Z^A through PPN order",
        "result": "would solve composite lock",
        "valid_for_claim": "false",
    },
    {
        "step_id": "E3_even_action",
        "statement": "The parent action is exchange-even and contains a positive local quadratic operator for Z.",
        "math_form": "S_Z=1/2 int sqrt(-g) G_AB[(nabla Z^A)(nabla Z^B)+m_A^2 Z^A Z^B]+even terms",
        "result": "forbids linear Z sources",
        "valid_for_claim": "false",
    },
    {
        "step_id": "E4_local_no_odd_boundary_charge",
        "statement": "Compact local domains have no exchange-odd boundary/source charge.",
        "math_form": "J_Z=0 and B_Z=0 on local branch",
        "result": "would activate 489 positive theorem",
        "valid_for_claim": "false",
    },
    {
        "step_id": "E5_current_corpus",
        "statement": "The current corpus does not yet derive the component map, matter evenness, or boundary odd-charge theorem.",
        "math_form": "missing P1 component certificates for Y0-Y6",
        "result": "conditional theorem only",
        "valid_for_claim": "false",
    },
]


CONTRACT_ROWS = [
    {
        "clause_id": "O0_doublet_parent_variables",
        "required_clause": "every residual channel has parent doublet variables R_+^A,R_-^A",
        "current_status": "not_derived",
        "why_needed": "makes oddness structural rather than notational",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O1_exchange_exactness",
        "required_clause": "exchange R_+^A<->R_-^A is an exact local-branch parent symmetry",
        "current_status": "conditional_template",
        "why_needed": "forbids linear odd source terms",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O2_even_matter_readout",
        "required_clause": "matter sees only exchange-even observed geometry and constants",
        "current_status": "not_derived",
        "why_needed": "prevents compact matter from sourcing Z^A",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O3_component_identity",
        "required_clause": "Z^A=Y_loc^A through local weak-field/PPN order",
        "current_status": "not_derived",
        "why_needed": "zeros actual residuals, not an auxiliary shadow",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O4_local_odd_charge_zero",
        "required_clause": "local compact boundary/source state has zero exchange-odd charge",
        "current_status": "not_derived",
        "why_needed": "removes boundary B_Z and local source J_Z",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O5_positive_operator",
        "required_clause": "exchange-odd sector has positive Hessian after gauge/constraint removal",
        "current_status": "formal_candidate_from_489",
        "why_needed": "turns zero source into Z^A=0",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "O6_even_extra_stress_or_bound",
        "required_clause": "exchange-even extra stress is topological/invisible or explicitly retained",
        "current_status": "retained_debt",
        "why_needed": "exchange symmetry does not erase even conserved stress",
        "valid_for_claim": "false",
    },
]


COMPONENT_MAP_ROWS = [
    {
        "component_id": "Y0_trace_expansion",
        "candidate_odd_parent": "antisymmetric trace-load doublet",
        "map_status": "not_derived",
        "blocker": "matter trace can be exchange-even and still source scalar geometry",
        "fallback": "trace-load closure/source-current row",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y1_coherent_projector",
        "candidate_odd_parent": "antisymmetric coherent-projector representative",
        "map_status": "not_derived",
        "blocker": "projector ownership/topological stress map incomplete",
        "fallback": "retained projector stress ledger",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y2_boundary_flux",
        "candidate_odd_parent": "exchange-odd boundary current class",
        "map_status": "conditional_promising",
        "blocker": "local zero odd boundary charge not proved",
        "fallback": "W_boundary_alpha3_epsilon_boundary_flux",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y3_domain_vector",
        "candidate_odd_parent": "exchange-odd domain representative/vector class",
        "map_status": "conditional_best",
        "blocker": "475 local scalar zero/topological selector not parent-derived",
        "fallback": "W_domain_alpha1/alpha2/alpha3 products",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y4_domain_STF_stress",
        "candidate_odd_parent": "antisymmetric STF projector stress",
        "map_status": "not_derived",
        "blocker": "tidal STF source and even conserved stress remain legal",
        "fallback": "W_domain_xi_epsilon_domain_anisotropy plus T_extra residual",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y5_source_normalization",
        "candidate_odd_parent": "antisymmetric source-normalization offset",
        "map_status": "failed_current",
        "blocker": "measured GM/source normalization is an observed even scalar unless a deeper odd/even split is derived",
        "fallback": "c_domain_source_normalization_operator",
        "valid_for_claim": "false",
    },
    {
        "component_id": "Y6_stress_Bianchi",
        "candidate_odd_parent": "none direct; divergence constraint/stress ledger",
        "map_status": "retained_debt",
        "blocker": "Bianchi-owned extra stress can be exchange-even and nonzero",
        "fallback": "retained T_extra residual vector",
        "valid_for_claim": "false",
    },
]


COUNTEREXAMPLE_ROWS = [
    {
        "counterexample_id": "CE0_even_matter_trace",
        "model": "matter couples to exchange-even geometry but sources an even trace curvature response",
        "why_it_blocks": "odd exchange symmetry alone does not force all scalar residual definitions to be odd",
        "needed_fix": "component identity O3 for Y0",
    },
    {
        "counterexample_id": "CE1_exchange_even_extra_stress",
        "model": "T_extra is exchange-even and conserved",
        "why_it_blocks": "Bianchi closes but local exterior is not EH-only",
        "needed_fix": "O6 topological/invisible stress theorem or residual bound",
    },
    {
        "counterexample_id": "CE2_boundary_odd_charge",
        "model": "compact domain carries a nonzero exchange-odd boundary class",
        "why_it_blocks": "B_Z is nonzero and can feed preferred-frame/boundary rows",
        "needed_fix": "O4 local odd boundary charge zero theorem",
    },
    {
        "counterexample_id": "CE3_even_source_normalization",
        "model": "measured GM receives an exchange-even normalization offset",
        "why_it_blocks": "odd residual symmetry does not kill even scalar source normalization",
        "needed_fix": "source-normalization even/odd split plus measured-GM theorem",
    },
]


CLOSURE_FILL_ROWS = [
    {
        "fill_id": "F0_component_map_gap",
        "if_missing": "O3 component identity",
        "closure": "keep all Yloc component residual rows unpromoted",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F1_matter_readout_gap",
        "if_missing": "O2 even matter readout",
        "closure": "identity coframe/selector-blind matter remains an explicit local closure",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F2_boundary_odd_charge_gap",
        "if_missing": "O4 local odd charge zero",
        "closure": "retain alpha3 boundary coefficient fill",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F3_source_normalization_gap",
        "if_missing": "Y5 source-normalization odd/even theorem",
        "closure": "retain c_domain_source_normalization_operator",
        "valid_for_claim": "false",
    },
    {
        "fill_id": "F4_even_stress_gap",
        "if_missing": "O6 extra-stress theorem",
        "closure": "retain T_extra residual vector and xi coefficient rows",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_exchange_doublet",
        "status": "best_conditional_route",
        "meaning": "exchange doublets can make residual oddness structural rather than cosmetic",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_component_map",
        "status": "not_derived",
        "meaning": "no current proof maps all physical Yloc residuals to exchange-odd parent variables",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_hard_rows",
        "status": "source_normalization_and_even_stress_block",
        "meaning": "Y5 and Y6 are not naturally killed by oddness and require separate theorem or closure",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no Yloc zero, R11 silence, Newton, PPN, alpha3, mu_extra-zero, or local-GR pass is earned",
        "next_action": "continue component map or closure fill",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "ODD_RESIDUAL_PARENTIZATION",
        "previous_status": "needed_after_lock_Z2_triangle",
        "new_status": "exchange_doublet_contract_written_component_map_incomplete",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "YLOC_PARENT_SYMMETRY",
        "previous_status": "auxiliary_action_attempt_finds_lock_Z2_triangle",
        "new_status": "requires_exchange_doublet_component_map_and_even_matter_readout",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_C2_C5_C6_plus_boundary_C3",
        "new_status": "blocked_by_component_map_source_normalization_even_stress_and_boundary_odd_charge",
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
    aux_contract_rows = read_csv(AUX_PARENT_CONTRACT_PATH)
    aux_component_rows = read_csv(AUX_PARENT_COMPONENT_PATH)
    claim_candidate_rows = [row for row in PARENTIZATION_CANDIDATES if row["valid_for_claim"] == "true"]
    claim_theorem_rows = [row for row in EXCHANGE_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_component_rows = [row for row in COMPONENT_MAP_ROWS if row["valid_for_claim"] == "true"]
    required_components = {
        "Y0_trace_expansion",
        "Y1_coherent_projector",
        "Y2_boundary_flux",
        "Y3_domain_vector",
        "Y4_domain_STF_stress",
        "Y5_source_normalization",
        "Y6_stress_Bianchi",
    }
    component_ids = {row["component_id"] for row in COMPONENT_MAP_ROWS}
    required_contract = {f"O{index}" for index in range(7)}
    contract_ids = {row["clause_id"].split("_", 1)[0] for row in CONTRACT_ROWS}

    return [
        {
            "rule_id": "V493_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V493_1_inputs_loaded",
            "rule": "492 contract and component result are loaded",
            "result": "pass" if len(aux_contract_rows) == 7 and len(aux_component_rows) == 7 else "fail",
            "evidence": f"aux_contract_rows={len(aux_contract_rows)};aux_component_rows={len(aux_component_rows)}",
            "claim_effect": "493 follows the active obstruction",
        },
        {
            "rule_id": "V493_2_candidate_space",
            "rule": "candidate parentizations include independent odd, exchange doublet, gauge redundancy, Lagrange lock, and closure",
            "result": "pass" if len(PARENTIZATION_CANDIDATES) == 5 else "fail",
            "evidence": ";".join(row["candidate_id"] for row in PARENTIZATION_CANDIDATES),
            "claim_effect": "fork space explicit",
        },
        {
            "rule_id": "V493_3_contract_complete",
            "rule": "exchange parentization contract O0 through O6 is explicit",
            "result": "pass" if required_contract.issubset(contract_ids) else "fail",
            "evidence": ";".join(sorted(contract_ids)),
            "claim_effect": "no hidden premise",
        },
        {
            "rule_id": "V493_4_component_coverage",
            "rule": "all Yloc components are mapped or marked unresolved",
            "result": "pass" if required_components.issubset(component_ids) else "fail",
            "evidence": ";".join(sorted(component_ids)),
            "claim_effect": "no skipped PPN blocker",
        },
        {
            "rule_id": "V493_5_no_claim_rows",
            "rule": "no candidate, theorem, or component row is promoted as claim-valid",
            "result": "pass" if not claim_candidate_rows and not claim_theorem_rows and not claim_component_rows else "fail",
            "evidence": f"candidate_claim_rows={len(claim_candidate_rows)};theorem_claim_rows={len(claim_theorem_rows)};component_claim_rows={len(claim_component_rows)}",
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
    return f"""# 493 - Odd Residual Parentization Or Closure Fill

Private local-GR/Newton/PPN parentization checkpoint. This is not a public Yloc-zero proof, EH-only proof, R11 pass, alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `492` found the lock/Z2 triangle:

```text
no linear source + physical residual lock + matter/boundary neutrality
```

cannot be claimed by merely writing `Y_loc -> -Y_loc`.

This checkpoint tests the cleanest possible mechanism:

```text
physical residuals are exchange-odd parent variables.
```

Short answer:

```text
Exchange-doublet parentization is the best non-smuggled route.
It is not yet derived component-by-component.
Y5 source normalization and Y6 extra stress are especially hard.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/odd_residual_parentization_or_closure_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Parentization Candidates

{markdown_table(PARENTIZATION_CANDIDATES)}

## 5. Conditional Exchange-Doublet Theorem

{markdown_table(EXCHANGE_THEOREM_ROWS)}

The promising construction is:

```text
E: R_+^A <-> R_-^A
Z^A = (R_+^A - R_-^A)/2
R_even^A = (R_+^A + R_-^A)/2
```

If matter sees only `R_even`, and the parent action is exactly exchange-even, then `Z^A` is not linearly sourced. If also:

```text
Z^A = Y_loc^A
```

through the PPN gate, then the 489 positive theorem could force the actual local residuals to zero.

That last identity is not currently derived.

## 6. Exchange Parentization Contract

{markdown_table(CONTRACT_ROWS)}

## 7. Component Map

{markdown_table(COMPONENT_MAP_ROWS)}

## 8. Counterexamples

{markdown_table(COUNTEREXAMPLE_ROWS)}

## 9. Closure Fill

{markdown_table(CLOSURE_FILL_ROWS)}

## 10. Validation

{markdown_table(validations)}

## 11. Decision

{markdown_table(DECISION_ROWS)}

## 12. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 13. Claim Ceiling

Allowed:

```text
The exchange-doublet route is the cleanest current candidate for real odd residuals.
It gives an exact contract for making oddness structural.
The component map remains incomplete and unpromoted.
```

Forbidden:

```text
MTS has derived odd residual parentization.
MTS has derived Y_loc=0.
MTS has derived J_Y=0 or B_Y=0.
MTS has derived EH/R11 silence.
MTS has derived Newtonian recovery or PPN recovery.
MTS has alpha3=0 or mu_extra=0.
```

## 14. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | attempt the component-by-component exchange-doublet map or demote each failed row to coefficients |
| 2 | source-normalization theorem | Y5 is the hardest scalar row and cannot be assumed odd |
| 3 | extra-stress theorem | Y6 remains Bianchi-owned but not zero |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-odd-residual-parentization-or-closure-fill"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PARENTIZATION_CANDIDATES_PATH, PARENTIZATION_CANDIDATES)
    write_csv(EXCHANGE_THEOREM_PATH, EXCHANGE_THEOREM_ROWS)
    write_csv(CONTRACT_PATH, CONTRACT_ROWS)
    write_csv(COMPONENT_MAP_PATH, COMPONENT_MAP_ROWS)
    write_csv(COUNTEREXAMPLE_PATH, COUNTEREXAMPLE_ROWS)
    write_csv(CLOSURE_FILL_PATH, CLOSURE_FILL_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_candidate_rows = [row for row in PARENTIZATION_CANDIDATES if row["valid_for_claim"] == "true"]
    claim_theorem_rows = [row for row in EXCHANGE_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_component_rows = [row for row in COMPONENT_MAP_ROWS if row["valid_for_claim"] == "true"]
    unresolved_component_rows = [
        row for row in COMPONENT_MAP_ROWS
        if row["map_status"] not in {"derived", "claim_valid"}
    ]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "parentization_candidates": str(ROOT / PARENTIZATION_CANDIDATES_PATH),
        "exchange_theorem": str(ROOT / EXCHANGE_THEOREM_PATH),
        "contract": str(ROOT / CONTRACT_PATH),
        "component_map": str(ROOT / COMPONENT_MAP_PATH),
        "counterexamples": str(ROOT / COUNTEREXAMPLE_PATH),
        "closure_fill": str(ROOT / CLOSURE_FILL_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "parentization_candidate_rows": len(PARENTIZATION_CANDIDATES),
        "exchange_theorem_rows": len(EXCHANGE_THEOREM_ROWS),
        "contract_rows": len(CONTRACT_ROWS),
        "component_map_rows": len(COMPONENT_MAP_ROWS),
        "counterexample_rows": len(COUNTEREXAMPLE_ROWS),
        "closure_fill_rows": len(CLOSURE_FILL_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_candidate_rows": len(claim_candidate_rows),
        "claim_theorem_rows": len(claim_theorem_rows),
        "claim_component_rows": len(claim_component_rows),
        "unresolved_component_rows": len(unresolved_component_rows),
        "exchange_doublet_contract_written": True,
        "exchange_doublet_parentization_derived": False,
        "component_map_complete": False,
        "source_normalization_odd_map_failed_current": True,
        "extra_stress_retained_debt": True,
        "matter_even_readout_derived": False,
        "local_odd_boundary_charge_zero_derived": False,
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
