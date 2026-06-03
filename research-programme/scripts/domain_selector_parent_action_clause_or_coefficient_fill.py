from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "domain_selector_parent_action_clause_written_double_zero_sufficient_not_parent_derived_coefficients_retained_no_PPN_Newton_or_local_GR_pass"
CLAIM_CEILING = "parent_action_clause_contract_or_coefficient_fill_only_no_selector_theorem_no_domain_channel_PPN_Newton_or_local_GR_pass"
NEXT_TARGET = "476-double-zero-memory-coupling-origin-or-coefficient-runner.md"

DOC_PATH = Path("475-domain-selector-parent-action-clause-or-coefficient-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_SOURCE_REGISTER.csv")
CLAUSE_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv")
VARIATION_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv")
FORK_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_FORKS.csv")
GATE_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_GATE.csv")
COEFFICIENT_FILL_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_CLOSURE_COEFFICIENT_FILL.csv")
VECTOR_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv")
DOMAIN_COEFFICIENTS_PATH = Path("source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_PARENT_ACTION_DECISION.csv")

SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
RESIDUAL_COMPONENTS_PATH = Path("runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv")
R11_EXECUTABLE_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")

SOURCE_REGISTER = [
    {
        "path": "67-auxiliary-selector-parent-contract.md",
        "role": "earlier algebraic chi_D parent contract; no kinetic stress but memory coupling open",
    },
    {
        "path": "143-domain-selector-variational-action-attempt.md",
        "role": "selector not parent-derived; auxiliary contract retained",
    },
    {
        "path": "308-selector-parent-theorem-attempt.md",
        "role": "spectral/topological selector route with local gap and FLRW activity contracts",
    },
    {
        "path": "309-MTS-boundary-projector-contract-attempt.md",
        "role": "conditional local exact/no-flux representative and projector contract",
    },
    {
        "path": "348-N5-projector-stress-conservation-theorem.md",
        "role": "metric-independent topological projector gives conditional no-bulk-stress route",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent action must expose S_domain and F_domain in Ward ledger",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward ownership permits covariant domain-vector counterexample unless no-vector theorem is supplied",
    },
    {
        "path": "474-domain-selector-no-vector-theorem-or-coefficient.md",
        "role": "conditional scalar-selector no-vector lemma and coefficient gate",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "source-locked PPN bounds for domain coefficient fallback",
    },
    {
        "path": str(RESIDUAL_COMPONENTS_PATH),
        "role": "residual component definitions for R5/R6/R7/R8",
    },
    {
        "path": str(R11_EXECUTABLE_VECTOR_PATH),
        "role": "R11 vector path; parseable but zero claim-valid rows",
    },
    {
        "path": "scripts/domain_selector_parent_action_clause_or_coefficient_fill.py",
        "role": "this checkpoint generator",
    },
]

TARGET_ROWS = [
    ("R5_alpha1", "alpha1", "W_domain_alpha1_epsilon_domain_vector"),
    ("R6_alpha2", "alpha2", "W_domain_alpha2_epsilon_domain_vector"),
    ("R7_alpha3", "alpha3", "W_domain_alpha3_epsilon_domain_flux"),
    ("R8_xi", "xi", "W_domain_xi_epsilon_domain_anisotropy"),
    ("R11_EH_operator_ledger", "non_EH_operator_coefficients", "c_domain_source_normalization_operator"),
]

FALLBACK_BOUNDS = {
    "R5_alpha1": "1e-04",
    "R6_alpha2": "2e-09",
    "R7_alpha3": "4e-20",
    "R8_xi": "4e-09",
    "R11_EH_operator_ledger": "symbolic",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "source_file": item["path"],
            "exists": str((ROOT / item["path"]).exists()),
            "role": item["role"],
        }
        for item in SOURCE_REGISTER
    ]


def bound_map() -> dict[str, str]:
    bounds = dict(FALLBACK_BOUNDS)
    if (ROOT / SCORECARD_PATH).exists():
        for row in read_csv(SCORECARD_PATH):
            if row.get("epsilon_channel") == "domain_projector_mass" and row.get("target_row") in bounds:
                bounds[row["target_row"]] = row.get("bound_value") or bounds[row["target_row"]]
    if (ROOT / RESIDUAL_COMPONENTS_PATH).exists():
        for row in read_csv(RESIDUAL_COMPONENTS_PATH):
            if row.get("row_id") in bounds:
                bounds[row["row_id"]] = row.get("source_bound") or bounds[row["row_id"]]
    return bounds


def r11_claimable_rows() -> int:
    if not (ROOT / R11_EXECUTABLE_VECTOR_PATH).exists():
        return 0
    return sum(1 for row in read_csv(R11_EXECUTABLE_VECTOR_PATH) if row.get("valid_for_claim") == "true")


def build_parent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "C0_parent_domain_sector",
            "object": "S_domain",
            "mathematical_form": "S_D = integral sqrt(-g) lambda_D(chi_D - Sigma_D) + integral sqrt(-g) chi_D^2 L_mem,D + S_top[P_MTS,D,J_B]",
            "required_property": "chi_D is auxiliary and scalar; no kinetic term, no independent n_mu, no domain velocity field",
            "local_effect_if_parent_derived": "no propagating selector force or preferred vector",
            "current_status": "admissible_contract_not_parent_derived",
        },
        {
            "clause_id": "C1_scalar_selector_source",
            "object": "Sigma_D",
            "mathematical_form": "Sigma_D = sigma(b_D,c_D), with b_D from MTS-projected boundary spectrum and c_D from relative boundary class",
            "required_property": "Sigma_D depends only on scalar/topological domain invariants, not an empirical threshold or local vector",
            "local_effect_if_parent_derived": "stationary local branch has constant Sigma_D",
            "current_status": "conditional_from_308_not_parent_owned",
        },
        {
            "clause_id": "C2_local_zero",
            "object": "local compact branch",
            "mathematical_form": "b_local = 0 or c_local = 0, hence Sigma_local = chi_local = 0",
            "required_property": "parent proves projected local spectral gap or exact/trivial relative class",
            "local_effect_if_parent_derived": "nabla_i chi_D = 0 and local memory activation vanishes",
            "current_status": "not_parent_derived",
        },
        {
            "clause_id": "C3_double_zero_memory",
            "object": "memory coupling",
            "mathematical_form": "S_mem,D = integral sqrt(-g) chi_D^2 L_mem,D",
            "required_property": "memory stress and delta S_mem over delta chi_D vanish at chi_D=0",
            "local_effect_if_parent_derived": "lambda_D = 0 on local branch, killing hidden metric variation of Sigma_D",
            "current_status": "sufficient_clause_not_derived",
        },
        {
            "clause_id": "C4_topological_projector",
            "object": "P_MTS,D",
            "mathematical_form": "P_MTS,D is metric-independent, diffeo-covariant, and parent-owned as relative-chain/cohomology projector",
            "required_property": "no Hodge/metric projector and no external after-solve filter",
            "local_effect_if_parent_derived": "bulk projector stress is zero by 348 route",
            "current_status": "conditional_not_parent_owned",
        },
        {
            "clause_id": "C5_R11_silence",
            "object": "domain source normalization",
            "mathematical_form": "c_domain_source_normalization_operator = 0 or executable R11 coefficient vector supplies all mapped rows",
            "required_property": "R11 rows have concrete coefficients, units, maps, and valid_for_claim true",
            "local_effect_if_parent_derived": "domain source-normalization cannot reintroduce PPN residuals",
            "current_status": "fail_current_corpus",
        },
    ]


def build_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "V0_lambda_variation",
            "variation": "delta S_D over delta lambda_D",
            "equation": "chi_D - Sigma_D = 0",
            "local_consequence": "chi_local = Sigma_local",
            "proof_status": "formal_pass_if_clause_allowed",
            "claim_effect": "constraint only",
        },
        {
            "step_id": "V1_chi_variation",
            "variation": "delta S_D over delta chi_D",
            "equation": "lambda_D + 2 chi_D L_mem,D + chi_D^2 partial_chi L_mem,D = 0",
            "local_consequence": "if chi_local=0 then lambda_local=0",
            "proof_status": "formal_pass_for_double_zero_clause",
            "claim_effect": "kills hidden constraint stress locally only under C2 and C3",
        },
        {
            "step_id": "V2_metric_variation",
            "variation": "delta S_D over delta g_munu",
            "equation": "T_D includes lambda_D delta_g Sigma_D plus chi_D^2 T_mem,D plus topological projector terms",
            "local_consequence": "lambda_local=0 and chi_local=0 remove bulk selector/memory stress",
            "proof_status": "conditional_pass_if_C2_C3_C4_hold",
            "claim_effect": "no local STF/vector stress only if parent owns the clause",
        },
        {
            "step_id": "V3_Ward_force",
            "variation": "diffeomorphism Ward identity",
            "equation": "F_domain^nu = E_chi nabla^nu chi_D + E_lambda nabla^nu lambda_D + divergence of T_D terms",
            "local_consequence": "on shell with chi_local=lambda_local=0 and no boundary flux, F_domain^nu=0",
            "proof_status": "conditional_pass_if_local_boundary_terms_zero",
            "claim_effect": "would set epsilon_vector, epsilon_flux, and epsilon_anisotropy to zero",
        },
        {
            "step_id": "V4_failure_mode",
            "variation": "linear memory coupling or kinetic selector",
            "equation": "S_mem proportional chi_D L_mem,D or K_chi(g,nabla chi) not equal zero",
            "local_consequence": "lambda_local or gradient stress can survive even when chi_local=0",
            "proof_status": "rejected_route",
            "claim_effect": "requires explicit PPN coefficients",
        },
    ]


def build_fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "F0_double_zero_parent_clause",
            "route": "accept only a scalar auxiliary selector with chi_D^2 memory activation and topological P_MTS,D",
            "what_it_buys": "formal local no-vector/no-flux/no-anisotropy theorem if local zero and R11 silence are also parent-derived",
            "what_still_missing": "origin of chi_D^2 coupling, local spectral/trivial-class theorem, topological projector ownership, R11 coefficients",
            "decision": "best_theory_route_but_not_promoted",
        },
        {
            "fork_id": "F1_linear_selector",
            "route": "allow S_mem proportional chi_D",
            "what_it_buys": "simpler activation",
            "what_still_missing": "lambda_D need not vanish at chi_D=0, so hidden selector stress can survive",
            "decision": "reject_for_local_GR_branch_unless_bound",
        },
        {
            "fork_id": "F2_dynamic_selector",
            "route": "give chi_D a kinetic term or smooth domain-wall field",
            "what_it_buys": "standard variational scalar dynamics",
            "what_still_missing": "new scalar force, length scale, and PPN residuals",
            "decision": "coefficient_branch_only",
        },
        {
            "fork_id": "F3_external_window",
            "route": "choose chi_D or P_D after solving",
            "what_it_buys": "easy phenomenology",
            "what_still_missing": "variational Ward ownership",
            "decision": "forbidden_as_field_theory_derivation",
        },
        {
            "fork_id": "F4_numeric_coefficients",
            "route": "retain W_domain_alpha1, W_domain_alpha2, W_domain_alpha3, W_domain_xi, and c_domain_source_normalization_operator",
            "what_it_buys": "testable closure branch without pretending derivation",
            "what_still_missing": "actual values or theorem-zero sources",
            "decision": "required_fallback",
        },
    ]


def build_coefficient_rows(bounds: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target_row, observable, coefficient_symbol in TARGET_ROWS:
        if target_row == "R11_EH_operator_ledger":
            value_or_theorem = "MISSING_DOMAIN_SOURCE_NORMALIZATION_OPERATOR_ZERO_OR_EXECUTABLE_COEFFICIENT_VECTOR"
            premise_status = "R11_claim_valid_rows_zero"
            map_text = "R11 includes domain_projector_mass source-normalization operator coefficients and weak-field maps"
            score_status = "not_scoreable"
        elif target_row == "R7_alpha3":
            value_or_theorem = "0_IF_DOUBLE_ZERO_PARENT_CLAUSE_AND_LOCAL_ZERO_AND_TOPOLOGICAL_PROJECTOR_AND_R11_SILENCE_ELSE_PRODUCT_REQUIRED"
            premise_status = "double_zero_clause_sufficient_but_not_parent_derived"
            map_text = "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux"
            score_status = "conditional_not_scoreable"
        elif target_row == "R8_xi":
            value_or_theorem = "0_IF_DOUBLE_ZERO_PARENT_CLAUSE_REMOVES_LOCAL_STF_STRESS_ELSE_PRODUCT_REQUIRED"
            premise_status = "selector_STF_zero_sufficient_but_not_parent_derived"
            map_text = "xi_domain = W_domain_xi * epsilon_domain_anisotropy"
            score_status = "not_scoreable"
        else:
            value_or_theorem = "0_IF_DOUBLE_ZERO_PARENT_CLAUSE_AND_LOCAL_SCALAR_ZERO_ELSE_PRODUCT_REQUIRED"
            premise_status = "scalar_double_zero_clause_sufficient_but_not_parent_derived"
            map_text = f"{observable}_domain = {coefficient_symbol.replace('_epsilon_', ' * epsilon_')}"
            score_status = "not_scoreable"
        rows.append(
            {
                "channel": "domain_projector_mass",
                "target_row": target_row,
                "observable": observable,
                "coefficient_symbol": coefficient_symbol,
                "map": map_text,
                "value_or_theorem": value_or_theorem,
                "premise_status": premise_status,
                "target_bound": bounds.get(target_row, FALLBACK_BOUNDS[target_row]),
                "score_status": score_status,
                "valid_for_claim": "false",
                "source": str(DOC_PATH),
            }
        )
    return rows


def build_gate_rows(clause_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed_claim_clauses = [row for row in clause_rows if row["current_status"] in {"not_parent_derived", "fail_current_corpus", "sufficient_clause_not_derived", "conditional_not_parent_owned"}]
    return [
        {
            "gate_id": "G0_clause_written",
            "requirement": "exact sufficient parent-action clause is stated",
            "result": "pass_contract",
            "evidence": "S_D with lambda_D(chi_D-Sigma_D), chi_D^2 memory activation, topological projector route",
            "claim_effect": "mathematical target sharpened",
        },
        {
            "gate_id": "G1_parent_derivation",
            "requirement": "clause is derived from deeper MTS parent variables rather than stipulated",
            "result": "fail_for_claim",
            "evidence": f"unowned_or_failed_clause_rows={len(failed_claim_clauses)}",
            "claim_effect": "no selector theorem promotion",
        },
        {
            "gate_id": "G2_double_zero_origin",
            "requirement": "chi_D^2 activation follows from symmetry, topological charge, or parent expansion",
            "result": "open",
            "evidence": "double-zero is sufficient but not derived",
            "claim_effect": "next target",
        },
        {
            "gate_id": "G3_local_zero",
            "requirement": "parent proves b_local=0 or c_local=0 for compact stationary local domains",
            "result": "fail_for_claim",
            "evidence": "308 local spectral gap and relative triviality are conditional",
            "claim_effect": "epsilon_domain_vector and epsilon_domain_flux not theorem-zero",
        },
        {
            "gate_id": "G4_R11_silence",
            "requirement": "domain source-normalization operator is zero or executable",
            "result": "fail_for_claim",
            "evidence": f"R11_claimable_rows={r11_claimable_rows()}",
            "claim_effect": "R11 and mapped PPN rows still blocked",
        },
        {
            "gate_id": "G5_coefficients_retained",
            "requirement": "fallback coefficient products remain explicit and unpromoted",
            "result": "pass",
            "evidence": f"coefficient_rows={len(coefficient_rows)} valid_for_claim_true={sum(1 for row in coefficient_rows if row['valid_for_claim'] == 'true')}",
            "claim_effect": "honest closure/test branch preserved",
        },
    ]


def build_validation(
    source_rows: list[dict[str, str]],
    clause_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = sum(1 for row in source_rows if row["exists"] != "True")
    targets = {row["target_row"] for row in coefficient_rows}
    claim_true = sum(1 for row in coefficient_rows if row["valid_for_claim"] == "true")
    return [
        {
            "rule_id": "V475_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing_sources={missing_sources}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V475_1_clause",
            "rule": "parent-action clause has selector, scalar source, local zero, double-zero memory, topological projector, and R11 rows",
            "result": "pass" if len(clause_rows) == 6 else "fail",
            "evidence": f"clause_rows={len(clause_rows)}",
            "claim_effect": "contract completeness only",
        },
        {
            "rule_id": "V475_2_variation",
            "rule": "variation chain shows why double-zero is needed",
            "result": "pass" if len(variation_rows) == 5 else "fail",
            "evidence": f"variation_rows={len(variation_rows)}",
            "claim_effect": "sufficient theorem attempt, not promotion",
        },
        {
            "rule_id": "V475_3_forks",
            "rule": "bad routes are explicitly rejected or demoted",
            "result": "pass" if len(fork_rows) == 5 else "fail",
            "evidence": f"fork_rows={len(fork_rows)}",
            "claim_effect": "no smuggled closure",
        },
        {
            "rule_id": "V475_4_coefficients",
            "rule": "coefficient fallback covers R5/R6/R7/R8/R11 and stays unpromoted",
            "result": "pass" if targets == {row[0] for row in TARGET_ROWS} and claim_true == 0 else "fail",
            "evidence": f"targets={';'.join(sorted(targets))}; valid_for_claim_true={claim_true}",
            "claim_effect": "no PPN/Newton/local-GR pass",
        },
        {
            "rule_id": "V475_5_gates",
            "rule": "promotion gates include parent derivation, local zero, double-zero origin, and R11 silence",
            "result": "pass" if len(gate_rows) == 6 else "fail",
            "evidence": f"gate_rows={len(gate_rows)}",
            "claim_effect": "next blockers are explicit",
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_parent_clause",
            "status": "sufficient_clause_written_not_derived",
            "meaning": "a scalar auxiliary selector with chi_D^2 memory activation can formally kill local selector stress/vector leakage if its local-zero premises hold",
            "next_action": "derive the origin of the double-zero memory coupling",
        },
        {
            "decision_id": "D1_no_vector",
            "status": "not_promoted",
            "meaning": "no-vector follows only if Sigma_D is scalar/topological and local branch has Sigma_D=0 by parent theorem",
            "next_action": "derive projected local gap or relative triviality",
        },
        {
            "decision_id": "D2_coefficients",
            "status": "retained",
            "meaning": "R5/R6/R7/R8/R11 products remain the honest fallback",
            "next_action": "fill numeric products or theorem-zero sources before any score",
        },
        {
            "decision_id": "D3_R11",
            "status": "still_blocking",
            "meaning": "domain source-normalization operator has zero claim-valid R11 rows",
            "next_action": "R11 domain source-normalization zero-or-fill after double-zero origin",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "meaning": "no domain channel, PPN, Newtonian-limit, or local-GR pass is earned",
            "next_action": NEXT_TARGET,
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    clause_rows = read_csv(CLAUSE_PATH)
    variation_rows = read_csv(VARIATION_PATH)
    fork_rows = read_csv(FORK_PATH)
    gate_rows = read_csv(GATE_PATH)
    coefficient_rows = read_csv(COEFFICIENT_FILL_PATH)
    validation_rows = read_csv(VALIDATION_PATH)
    decision_rows = read_csv(DECISION_PATH)
    compact_coefficients = [
        {
            "target_row": row["target_row"],
            "observable": row["observable"],
            "coefficient_symbol": row["coefficient_symbol"],
            "value_or_theorem": row["value_or_theorem"],
            "target_bound": row["target_bound"],
            "valid_for_claim": row["valid_for_claim"],
        }
        for row in coefficient_rows
    ]
    return f"""# 475 - Domain Selector Parent-Action Clause Or Coefficient Fill

Private parent-action/PPN-coefficient checkpoint. This is not a public PPN pass, Newtonian-limit pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `474` found the clean conditional lemma:

```text
scalar stationary selector + no local vector/flux/anisotropy => domain PPN leakage zero.
```

This checkpoint asks whether the parent action can force that lemma.

Short answer:

```text
There is an exact sufficient parent-action clause.
It needs a double-zero memory activation, chi_D^2 L_mem.
The current corpus does not derive that clause, so coefficients stay alive.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/domain_selector_parent_action_clause_or_coefficient_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Parent-Action Clause

The sufficient clause is:

```text
S_D = integral sqrt(-g) lambda_D(chi_D - Sigma_D)
    + integral sqrt(-g) chi_D^2 L_mem,D
    + S_top[P_MTS,D,J_B].
```

with:

```text
Sigma_D = sigma(b_D,c_D),
```

where `b_D` is an MTS-projected boundary spectral scalar and `c_D` is a relative boundary-class scalar.

{md_table(clause_rows)}

The key trick is the double zero:

```text
S_mem,D = chi_D^2 L_mem,D.
```

At `chi_D=0`, both the memory stress and the chi-variation source vanish.

That is what the old linear selector did not guarantee.

## 5. Variation Chain

{md_table(variation_rows)}

If all the premises were parent-derived, the local branch would get:

```text
chi_local = 0,
lambda_local = 0,
T_domain_bulk = 0,
F_domain^nu = 0,
epsilon_domain_vector = epsilon_domain_flux = epsilon_domain_anisotropy = 0.
```

That would be serious business.

But right now it is a sufficient contract, not a derivation.

## 6. Fork Table

{md_table(fork_rows)}

The branch discipline is:

```text
double-zero scalar/topological selector: keep as theorem target;
linear selector or dynamic selector: demote to coefficient branch;
external window: forbidden.
```

## 7. Gate Results

{md_table(gate_rows)}

The grim-but-useful read:

```text
We found the exact shape of the lock.
We have not forged the key from the parent action yet.
```

## 8. Coefficient Fill

{md_table(compact_coefficients)}

These rows were also written to:

```text
source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv
source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv
```

Important:

```text
valid_for_claim=false for every row.
```

## 9. Validation

{md_table(validation_rows)}

## 10. Decision

{md_table(decision_rows)}

## 11. Claim Ceiling

Allowed:

```text
MTS has an exact sufficient parent-action clause for local selector silence.
```

Allowed:

```text
The clause requires double-zero memory activation plus scalar/topological local zero plus R11 silence.
```

Forbidden:

```text
MTS derives the parent selector clause.
```

Forbidden:

```text
MTS passes domain alpha3, PPN, Newton, or local GR.
```

## 12. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `476-double-zero-memory-coupling-origin-or-coefficient-runner.md` | the new lock is chi_D^2; either derive that double zero or treat it as closure |
| 2 | `477-alpha3-bound-product-evaluator.md` | useful only after W_domain_alpha3 epsilon_domain_flux becomes numeric or theorem-zero |
| 3 | `478-R11-domain-source-normalization-zero-or-fill.md` | R11 source-normalization still blocks PPN/local-GR promotion |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-domain-selector-parent-action-clause-or-coefficient-fill"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    bounds = bound_map()
    clause_rows = build_parent_clause_rows()
    variation_rows = build_variation_rows()
    fork_rows = build_fork_rows()
    coefficient_rows = build_coefficient_rows(bounds)
    gate_rows = build_gate_rows(clause_rows, coefficient_rows)
    validation_rows = build_validation(source_rows, clause_rows, variation_rows, fork_rows, gate_rows, coefficient_rows)
    decision_rows = build_decision()

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(CLAUSE_PATH, clause_rows)
    write_csv(VARIATION_PATH, variation_rows)
    write_csv(FORK_PATH, fork_rows)
    write_csv(GATE_PATH, gate_rows)
    write_csv(COEFFICIENT_FILL_PATH, coefficient_rows)
    write_csv(VECTOR_COEFFICIENTS_PATH, coefficient_rows)
    write_csv(DOMAIN_COEFFICIENTS_PATH, coefficient_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(DECISION_PATH, decision_rows)

    for path in [
        SOURCE_REGISTER_PATH,
        CLAUSE_PATH,
        VARIATION_PATH,
        FORK_PATH,
        GATE_PATH,
        COEFFICIENT_FILL_PATH,
        VECTOR_COEFFICIENTS_PATH,
        DOMAIN_COEFFICIENTS_PATH,
        VALIDATION_PATH,
        DECISION_PATH,
    ]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "parent_action_clause": str(ROOT / CLAUSE_PATH),
        "variation_chain": str(ROOT / VARIATION_PATH),
        "forks": str(ROOT / FORK_PATH),
        "gate": str(ROOT / GATE_PATH),
        "coefficient_fill": str(ROOT / COEFFICIENT_FILL_PATH),
        "domain_coefficients_updated": str(ROOT / DOMAIN_COEFFICIENTS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "clause_rows": len(clause_rows),
        "variation_rows": len(variation_rows),
        "fork_rows": len(fork_rows),
        "gate_rows": len(gate_rows),
        "coefficient_rows": len(coefficient_rows),
        "validation_rows": len(validation_rows),
        "decision_rows": len(decision_rows),
        "R11_claimable_rows": r11_claimable_rows(),
        "double_zero_clause_written": True,
        "double_zero_clause_parent_derived": False,
        "selector_no_vector_parent_derived": False,
        "domain_vector_coefficients_required": True,
        "domain_alpha3_score_ready": False,
        "domain_channel_promoted": False,
        "mu_extra_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    print(json.dumps(write_run(args.timestamp), indent=2))


if __name__ == "__main__":
    main()
