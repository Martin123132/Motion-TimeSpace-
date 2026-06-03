from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-matter-selector-theorem-attempt"
CHECKPOINT_DOC = "401-parent-matter-selector-theorem-attempt.md"
STATUS = "parent_matter_selector_theorem_attempt_written_selector_blind_axiom_sufficient_counterexample_blocks_derivation_from_existing_premises_R0_remains_closure_no_local_GR_pass"
CLAIM_CEILING = "parent_matter_selector_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "402-EH-source-normalization-parent-pair.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward ledger and nonmetric matter force channel",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action contract and matter/coframe identity",
    },
    {
        "path": "388-WEP-species-symmetry-common-F-parent-selector-attempt.md",
        "role": "species-blind geometry functor attempt and common-F counterlimit",
    },
    {
        "path": "389-identity-coframe-parent-selection-principle.md",
        "role": "identity coframe sufficiency proof and no-go warnings",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity closure branch policy and remaining GR stack",
    },
    {
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "role": "parent action obligations for runner-v3 rows",
    },
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "numeric pressure showing direct coframe and WEP-source tolerances",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "runner-v3 R0/R1/R2 row states",
    },
    {
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/runner_row_parent_obligations.csv",
        "role": "R0 parent obligation and fallback",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv",
        "role": "hardest channel bounds after checkpoint 400",
    },
]


SELECTOR_AXIOM_TESTS = [
    {
        "candidate_principle": "diffeomorphism covariance only",
        "assumption": "S_matter is a scalar functional of some covariant matter geometry ehat",
        "allowed_geometry": "ehat=exp(F(C_D))e is still legal",
        "result_for_deltaS_deltaZ": "not_zero_generically",
        "verdict": "reject_as_identity_derivation",
        "reason": "covariance allows universal class-metric pullback",
    },
    {
        "candidate_principle": "weak equivalence / one geometry",
        "assumption": "all species use one shared geometry ehat",
        "allowed_geometry": "common ehat may still be exp(F(C_D))e",
        "result_for_deltaS_deltaZ": "common_mode_pullback_remains",
        "verdict": "conditional_common_geometry_only",
        "reason": "kills species split but not common F prime source",
    },
    {
        "candidate_principle": "species-blind geometry functor",
        "assumption": "species labels are internal-only and geometry map is independent of A",
        "allowed_geometry": "ehat=ehat(e,Z) independent of species",
        "result_for_deltaS_deltaZ": "Delta_F_AB_zero_but_Pi_I_matter_may_remain",
        "verdict": "conditional_WEP_source_help_not_identity",
        "reason": "one common F still produces matter pullback into selector equations",
    },
    {
        "candidate_principle": "field redefinition e_prime=ehat",
        "assumption": "rename the matter geometry as the metric frame",
        "allowed_geometry": "all matter uses e_prime",
        "result_for_deltaS_deltaZ": "not_a_parent_selection",
        "verdict": "reject_as_proof",
        "reason": "moves EH/operator/source-normalization debts into the renamed frame",
    },
    {
        "candidate_principle": "selector-blind matter symmetry",
        "assumption": "nonmetric selectors Z_I are gauge/representative variables forbidden from S_matter and theta_A",
        "allowed_geometry": "S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]",
        "result_for_deltaS_deltaZ": "zero_by_chain_rule",
        "verdict": "sufficient_conditional_theorem",
        "reason": "exactly yields delta S_matter/delta Z_I|e=0",
    },
    {
        "candidate_principle": "source-normalized constant conformal factor",
        "assumption": "ehat=A0 e, A0 constant universal and absorbed into units/source normalization",
        "allowed_geometry": "constant universal rescaling only",
        "result_for_deltaS_deltaZ": "zero_for_selector_derivatives_but_frame_debts_remain",
        "verdict": "conditional_identity_up_to_units",
        "reason": "requires A0 source-normalized and EH/source frame aligned",
    },
]


VARIATION_CHAIN_RULE = [
    {
        "step": 1,
        "claim": "Define nonmetric local selectors Z_I",
        "expression": "Z_I in {C_D, C_perp, P_D, X, boundary, domain, source-normalization, class data}",
        "status": "definition",
    },
    {
        "step": 2,
        "claim": "Selector-blind matter action",
        "expression": "S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]",
        "status": "extra_parent_axiom_needed",
    },
    {
        "step": 3,
        "claim": "Matter geometry independent of selectors at fixed e",
        "expression": "partial e/partial Z_I|e=0 and partial omega[e]/partial Z_I|e=0",
        "status": "follows_from_step_2",
    },
    {
        "step": 4,
        "claim": "Matter constants/source charges selector-independent",
        "expression": "partial theta_A/partial Z_I=0 and partial q_A/partial Z_I=0",
        "status": "extra_species_blind_constants_axiom_needed",
    },
    {
        "step": 5,
        "claim": "Matter selector momentum vanishes",
        "expression": "delta S_matter/delta Z_I|e = (delta S_matter/delta e)(partial e/partial Z_I)+sum_A(partial L_A/partial theta_A)(partial theta_A/partial Z_I)=0",
        "status": "conditional_theorem",
    },
    {
        "step": 6,
        "claim": "R0 direct coframe pullback can move to derived_zero only under the selector-blind axiom",
        "expression": "Pi_I^matter=0 -> eta_WEP_direct_geometry=0",
        "status": "not_derived_from_existing_premises",
    },
]


COUNTEREXAMPLE_MODELS = [
    {
        "model": "universal_class_metric",
        "matter_geometry": "ehat=exp(F(C_D))e",
        "satisfies": "covariance; one shared geometry; species-blind if F is common",
        "fails": "delta S_matter/delta C_D = T_hat dF/dC_D is generically nonzero",
        "lesson": "WEP/covariance/species-blindness alone do not derive identity coframe",
    },
    {
        "model": "species_common_F_with_constant_masses",
        "matter_geometry": "ehat=exp(F(C_D))e and theta_A constant",
        "satisfies": "no species split in F_A and no theta_A(C_D)",
        "fails": "common-mode pullback remains unless F prime is zero or source-owned",
        "lesson": "R1 can improve while R0 remains closure-only",
    },
    {
        "model": "renamed_matter_frame",
        "matter_geometry": "e_prime=ehat",
        "satisfies": "matter minimal coupling in e_prime",
        "fails": "EH/source/boundary/operator terms may not be EH in e_prime",
        "lesson": "frame redefinition is not a GR reduction",
    },
    {
        "model": "constant_universal_rescaling",
        "matter_geometry": "ehat=A0 e with constant A0",
        "satisfies": "delta S_matter/delta Z_I=0 for nonmetric selectors",
        "fails": "A0 must be unit/source-normalized and aligned with EH frame",
        "lesson": "identity can be up to units only if source normalization is derived",
    },
]


MINIMAL_SELECTOR_CONTRACT = [
    {
        "contract_item": "single metric-core coframe",
        "required_statement": "the only coframe argument available to local matter, clocks, rulers, and photons is e",
        "pays_row": "R0_identity_coframe_direct",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "selector-blind matter symmetry",
        "required_statement": "nonmetric selectors Z_I are gauge/representative variables and cannot appear in S_matter",
        "pays_row": "R0_identity_coframe_direct",
        "current_status": "candidate_axiom_not_derived",
    },
    {
        "contract_item": "species labels internal-only",
        "required_statement": "theta_A may contain masses/charges/representations but not theta_A(Z_I)",
        "pays_row": "R1_WEP_source_charge; R2_clock_redshift",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "no class/source spurions",
        "required_statement": "no sigma_A C_D O_A, lambda_A f(C_D)O_A, q_A(X), or boundary/domain species charge",
        "pays_row": "R1_WEP_source_charge",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "constant conformal normalization fixed",
        "required_statement": "ehat=A0 e is allowed only if A0 is constant, universal, and absorbed by source/unit normalization",
        "pays_row": "R0_identity_coframe_direct; R4_beta; R9_Gdot",
        "current_status": "coupled_to_source_normalization_debt",
    },
]


ROW_TRANSITION_DECISION = [
    {
        "runner_row": "R0_identity_coframe_direct",
        "current_state": "closure_zero",
        "attempt_result": "selector-blind matter axiom would be sufficient",
        "new_state": "closure_zero",
        "why_not_promoted": "the axiom is not yet derived from existing MTS parent variation; counterexample exp(F(C_D))e remains legal under weaker premises",
    },
    {
        "runner_row": "R1_WEP_source_charge",
        "current_state": "contingent_budget",
        "attempt_result": "species-blind/internal-only constants would help",
        "new_state": "contingent_budget",
        "why_not_promoted": "source/bulk/boundary/domain species charges are not forbidden by an existing parent theorem",
    },
    {
        "runner_row": "R2_clock_redshift",
        "current_state": "budget_only",
        "attempt_result": "clock constants close only if theta_A is selector-independent",
        "new_state": "budget_only",
        "why_not_promoted": "clock/source normalization remains a separate theorem obligation",
    },
]


NO_CHEAT_RULES = [
    {
        "rule": "do not call WEP a derivation",
        "forbidden_move": "using empirical WEP or universality to assert ehat=e",
        "safe_move": "state that WEP motivates a selector axiom but does not prove it",
    },
    {
        "rule": "do not hide common F",
        "forbidden_move": "treating common ehat=exp(F)e as local GR",
        "safe_move": "either derive F prime=0/source-owned or retain Pi_I^matter",
    },
    {
        "rule": "do not frame-rename GR",
        "forbidden_move": "renaming ehat as e and ignoring EH/source/operator debts",
        "safe_move": "prove EH and source normalization in the same frame matter sees",
    },
    {
        "rule": "do not close R1 with R0",
        "forbidden_move": "assuming identity coframe also forbids species/source charges",
        "safe_move": "keep species and source charges as separate rows",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The parent matter-selector theorem has a clean conditional form: if nonmetric MTS selectors are gauge/representative variables forbidden from the matter action and from matter constants, then delta S_matter/delta Z_I|e=0 by the chain rule and the direct coframe/WEP pullback row would be derived-zero. The existing corpus does not yet derive that selector-blind matter symmetry. A universal class metric ehat=exp(F(C_D))e is a counterexample to weaker premises: it is covariant, universal, and species-blind, yet still gives a common-mode matter pullback when F prime is nonzero. Therefore R0 remains closure_zero, not derived_zero.",
        "R0_transition": "closure_zero_retained",
        "conditional_theorem_available": True,
        "parent_axiom_derived_from_existing_MTS": False,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt the EH/source-normalization parent pair in the same frame matter sees",
        "pass_condition": "gamma/beta/source-normalization debts either derive EH+measured-GM form or remain explicit coefficients",
    },
    {
        "priority": 2,
        "target": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "task": "attack alpha3/Gdot/domain-vector hard bounds with Ward-owned flux/no-hair equations",
        "pass_condition": "the 4e-20 flux rows are theorem-zero, source-owned, or explicitly retained",
    },
    {
        "priority": 3,
        "target": "404-selector-blind-matter-axiom-origin.md",
        "task": "look for a deeper MTS origin of selector-blind matter symmetry from motion/time/space primitives",
        "pass_condition": "selector-blind matter becomes derived from primitive symmetry or is declared a postulate",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    counterexample_written = len(COUNTEREXAMPLE_MODELS) > 0
    sufficient_theorem = any(
        row["verdict"] == "sufficient_conditional_theorem" for row in SELECTOR_AXIOM_TESTS
    )
    existing_derivation = DECISION[0]["parent_axiom_derived_from_existing_MTS"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "candidate_selector_principles_audited",
            "status": "pass",
            "evidence": f"{len(SELECTOR_AXIOM_TESTS)} selector principles tested",
        },
        {
            "gate": "counterexample_to_weak_premises_written",
            "status": "pass" if counterexample_written else "fail",
            "evidence": "universal ehat=exp(F(C_D))e blocks derivation from covariance/WEP/species-blindness alone",
        },
        {
            "gate": "selector_blind_axiom_sufficient",
            "status": "conditional_pass" if sufficient_theorem else "fail",
            "evidence": "chain-rule proof gives delta S_matter/delta Z_I|e=0 if matter is selector-blind",
        },
        {
            "gate": "selector_blind_axiom_parent_derived",
            "status": "fail" if not existing_derivation else "pass",
            "evidence": "no existing MTS parent variation yet forbids universal class metric or selector spurions",
        },
        {
            "gate": "R0_promoted_to_derived_zero",
            "status": "fail",
            "evidence": "R0 remains closure_zero; promotion needs parent-derived selector-blind symmetry",
        },
        {
            "gate": "R1_R2_separate_debts_retained",
            "status": "pass",
            "evidence": "source-charge and clock constants are not closed by R0 identity alone",
        },
        {
            "gate": "local_GR_or_WEP_promoted",
            "status": "fail",
            "evidence": "conditional theorem attempt only",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    axiom_rows = [
        {
            "principle": row["candidate_principle"],
            "result": row["result_for_deltaS_deltaZ"],
            "verdict": row["verdict"],
        }
        for row in SELECTOR_AXIOM_TESTS
    ]
    transition_rows = [
        {
            "row": row["runner_row"],
            "new_state": row["new_state"],
            "reason": row["why_not_promoted"],
        }
        for row in ROW_TRANSITION_DECISION
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 401 - Parent Matter Selector Theorem Attempt

Private parent-action/WEP-selector checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 400 made the pressure point sharp: direct coframe slip and WEP/source charge need suppressions near `2.8e-15`, while flux channels are even harder. The cleanest route is not to tune them; it is to derive that local matter cannot see nonmetric selector variables.

This checkpoint attempts that derivation.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/parent_matter_selector_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Result In One Line

The theorem exists only conditionally:

```text
S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]
partial_Z e|e = 0
partial_Z theta_A = 0
=> delta S_matter/delta Z_I|e = 0
```

But the existing MTS parent action has not yet derived why matter must be selector-blind. So `R0` does not move to `derived_zero`.

## 4. Selector Principle Audit

{markdown_table(axiom_rows, ["principle", "result", "verdict"])}

## 5. The Counterexample

The killer counterexample to weak premises is:

```text
ehat = exp(F(C_D)) e
```

This is covariant. It can be universal. It can be species-blind. But if `F'(C_D) != 0`, then:

```text
delta S_matter/delta C_D ~ T_hat F'(C_D)
```

So WEP/covariance/common geometry do not force identity coframe. They only tell us what extra selector principle we need.

## 6. Row Transition Decision

{markdown_table(transition_rows, ["row", "new_state", "reason"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: this is not a defeat. It is the correct Grossmann move: we found the exact missing principle. Either MTS derives selector-blind matter from its primitive motion/time/space structure, or identity coframe remains an explicit local closure used to test the rest of the GR stack.

## 9. Next Target

`{NEXT_TARGET}`

Now test whether the dynamics in the same matter frame can become EH plus source-normalized measured `GM`, instead of leaving `gamma`, `beta`, and source-normalization as inserted budgets.
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "selector_axiom_tests.csv", SELECTOR_AXIOM_TESTS)
    write_csv(results_dir / "variation_chain_rule.csv", VARIATION_CHAIN_RULE)
    write_csv(results_dir / "counterexample_models.csv", COUNTEREXAMPLE_MODELS)
    write_csv(results_dir / "minimal_selector_contract.csv", MINIMAL_SELECTOR_CONTRACT)
    write_csv(results_dir / "row_transition_decision.csv", ROW_TRANSITION_DECISION)
    write_csv(results_dir / "no_cheat_rules.csv", NO_CHEAT_RULES)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "selector_principles_tested": len(SELECTOR_AXIOM_TESTS),
        "counterexamples_written": len(COUNTEREXAMPLE_MODELS),
        "conditional_selector_theorem_available": True,
        "parent_axiom_derived_from_existing_MTS": False,
        "R0_new_state": "closure_zero",
        "derived_local_GR_claim_allowed": False,
        "WEP_pass_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 401 parent matter selector theorem attempt artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
