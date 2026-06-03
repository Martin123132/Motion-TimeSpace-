from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Cexp-domain-candidate-generator"
CHECKPOINT_DOC = "418-Cexp-domain-candidate-generator.md"
STATUS = "Cexp_domain_candidate_generator_written_candidates_first_score_second_contract_but_parent_generator_not_derived_no_local_GR_pass"
CLAIM_CEILING = "Cexp_domain_candidate_generator_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "419-boundary-exchange-coefficient-retained-evaluator.md"


SOURCE_DOCS = [
    {
        "path": "61-bound-domain-boundary-theorem-attempt.md",
        "role": "stationary/extremal boundary partial theorem",
    },
    {
        "path": "62-domain-field-chiD-action-contract.md",
        "role": "chi_D domain selector contract",
    },
    {
        "path": "64-binding-invariant-domain-selector-attempt.md",
        "role": "C_coh/C_exp invariant and rejected imports",
    },
    {
        "path": "65-Ccoh-phase-field-selector-attempt.md",
        "role": "phase-field drive candidate and threshold risks",
    },
    {
        "path": "416-binding-invariant-domain-selector-repair.md",
        "role": "binding selector repair and averaging-domain circularity blocker",
    },
    {
        "path": "417-boundary-exchange-nohair-theorem-attempt.md",
        "role": "boundary exchange no-hair attempt and next target",
    },
    {
        "path": "runs/20260531-111219-binding-invariant-domain-selector-attempt/results/candidate_invariant_ledger.csv",
        "role": "candidate invariant ledger",
    },
    {
        "path": "runs/20260602-070500-binding-invariant-domain-selector-repair/results/blocker_matrix.csv",
        "role": "machine-readable blocker matrix",
    },
    {
        "path": "runs/20260602-071500-boundary-exchange-nohair-theorem-attempt/results/next_queue.csv",
        "role": "machine-readable next queue pointing to C_exp domain generator",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
]


DOMAIN_GENERATOR_CONTRACT = [
    {
        "contract_item": "candidate_before_score",
        "requirement": "Generate admissible candidate domains D_i from parent variables before evaluating C_exp[D_i].",
        "status": "written_not_derived",
    },
    {
        "contract_item": "no_data_window",
        "requirement": "Candidate domains cannot be chosen from PPN/SPARC/Pantheon/BAO/CMB residual performance.",
        "status": "pass_guardrail",
    },
    {
        "contract_item": "no_lower_limit_import",
        "requirement": "Candidate domains cannot use Newtonian binding energy or GR turnaround surfaces.",
        "status": "pass_guardrail",
    },
    {
        "contract_item": "finite_candidate_set_or_measure",
        "requirement": "The parent action must define either a finite family of D_i or a covariant measure over candidates.",
        "status": "not_derived",
    },
    {
        "contract_item": "single_rule_local_FLRW",
        "requirement": "The same generator must allow local stationary domains and coherent FLRW domains.",
        "status": "not_derived",
    },
    {
        "contract_item": "boundary_exchange_compatibility",
        "requirement": "Generated domains must come with boundary-current/Bianchi bookkeeping.",
        "status": "not_derived",
    },
]


CANDIDATE_DOMAIN_SOURCES = [
    {
        "source": "relative_current_boundary",
        "schematic_generator": "partial D_i from support/level surfaces of J_rel=(j_3,b_2)",
        "why_allowed": "uses parent boundary/current objects already in the relative-current route",
        "risk": "J_rel owner and physical representative still not derived",
        "status": "best_candidate_contract",
    },
    {
        "source": "Cexp_extremal_surfaces",
        "schematic_generator": "D_i are stationary points of C_exp[D] under admissible boundary variations",
        "why_allowed": "uses motion/volume-flow invariant instead of Newton/GR/data imports",
        "risk": "C_exp is defined on D, so variational measure over D_i is needed",
        "status": "promising_but_circular_until_generator_defined",
    },
    {
        "source": "chiD_parent_level_sets",
        "schematic_generator": "D_i are level-set/boundary components of auxiliary chi_D",
        "why_allowed": "uses the proposed selector field",
        "risk": "chi_D equation currently needs C_exp and boundary ownership",
        "status": "contract_only",
    },
    {
        "source": "coherence_phase_components",
        "schematic_generator": "connected components of Pi[C_exp] or C_coh phase projection",
        "why_allowed": "could separate stationary local and coherent FLRW branches",
        "risk": "threshold/projector origin can become a hidden fit knob",
        "status": "open",
    },
    {
        "source": "topological_boundary_projector",
        "schematic_generator": "D_i selected by relative/topological boundary class representatives",
        "why_allowed": "can be metric-stress safe if truly topological",
        "risk": "physical local-zero/FLRW-nonzero representative not selected",
        "status": "open_best_no_stress_route",
    },
    {
        "source": "empirical_residual_window",
        "schematic_generator": "D_i chosen to improve local/cosmology data fits",
        "why_allowed": "not allowed",
        "risk": "posthoc rescue knob",
        "status": "forbidden",
    },
]


SCORING_CHAIN = [
    {
        "step": 1,
        "claim": "Parent geometry/current fields generate candidate domains.",
        "identity": "G_parent[fields] -> {D_i} or measure dmu(D)",
        "status": "not_derived",
    },
    {
        "step": 2,
        "claim": "C_exp is evaluated only after candidates exist.",
        "identity": "C_exp[D_i]=sign(<theta>_D)<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps)",
        "status": "contract_written",
    },
    {
        "step": 3,
        "claim": "Selector chooses local stationary branch and active FLRW branch by one rule.",
        "identity": "local: C_exp~0; FLRW: C_exp~+1",
        "status": "kinematic_support_not_selector_theorem",
    },
    {
        "step": 4,
        "claim": "Boundary exchange for selected candidates is owned.",
        "identity": "d_rel J_rel=0 plus Bianchi boundary terms cancel/vanish",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "No data-tuned candidate survives audit.",
        "identity": "D_i independent of residual scores",
        "status": "guardrail_pass",
    },
    {
        "step": 6,
        "claim": "Local trivial class follows from selected candidate.",
        "identity": "selected local D_i has Q_rel=0",
        "status": "conditional_target_not_promoted",
    },
]


ANTI_CIRCULARITY_TESTS = [
    {
        "test": "candidate_generated_before_Cexp_score",
        "pass_condition": "D_i exists before C_exp[D_i] is computed",
        "current_result": "contract_only",
    },
    {
        "test": "candidate_independent_of_empirical_residuals",
        "pass_condition": "D_i independent of local/cosmology fit success",
        "current_result": "guardrail_pass",
    },
    {
        "test": "candidate_independent_of_GR_Newton_import",
        "pass_condition": "D_i independent of Newtonian binding and GR turnaround",
        "current_result": "guardrail_pass",
    },
    {
        "test": "single_rule_generates_local_and_FLRW",
        "pass_condition": "same generator admits stationary local and coherent FLRW branches",
        "current_result": "not_derived",
    },
    {
        "test": "Bianchi_boundary_bookkeeping_attached",
        "pass_condition": "each D_i has owned boundary exchange current",
        "current_result": "not_derived",
    },
    {
        "test": "finite_or_integrable_candidate_family",
        "pass_condition": "candidate set/measure is well-defined and not arbitrary",
        "current_result": "not_derived",
    },
]


ROW_IMPACT = [
    {
        "row_id": "R5_alpha1",
        "new_state": "retained_budget",
        "reason": "domain candidate generator not derived, so vector leakage remains retained",
    },
    {
        "row_id": "R6_alpha2",
        "new_state": "retained_budget",
        "reason": "domain anisotropy/vector branch remains open",
    },
    {
        "row_id": "R7_alpha3",
        "new_state": "retained_contingent_budget",
        "reason": "candidate domains still lack owned boundary exchange current",
    },
    {
        "row_id": "R8_xi",
        "new_state": "retained_budget",
        "reason": "topological/preferred-location candidate selection not derived",
    },
    {
        "row_id": "R9_Gdot",
        "new_state": "retained_contingent_budget",
        "reason": "domain scale drift cannot be silenced until selected domains are parent-derived",
    },
    {
        "row_id": "R10_fifth_force",
        "new_state": "unscored_parameterized",
        "reason": "selector/projector transition can still become a fifth-force-like curve",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The C_exp selector is now protected against its main circularity by a candidates-first contract: parent variables must generate admissible domains before C_exp scores them. The best candidate sources are relative-current boundaries, topological boundary projectors, or auxiliary chi_D level-set structures. The contract blocks empirical residual windows, Newtonian binding energy, and GR turnaround imports. But the parent candidate generator is not derived: the candidate family/measure, single local-FLRW rule, and attached boundary-exchange bookkeeping remain open. Therefore C_exp remains a promising selector contract, not a local-GR derivation.",
        "candidate_before_score_contract_written": True,
        "empirical_windows_blocked": True,
        "Newton_GR_import_blocked": True,
        "parent_candidate_generator_derived": False,
        "boundary_exchange_attached": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "define retained boundary-exchange coefficients for alpha3/Gdot/domain rows if theorem-zero remains unavailable",
        "pass_condition": "exchange rows become testable without claim leakage",
    },
    {
        "priority": 2,
        "target": "420-relative-current-boundary-generator-theorem-attempt.md",
        "task": "try to make relative-current boundaries generate admissible D_i directly",
        "pass_condition": "candidate domains are parent-generated from J_rel or remain closure-labelled",
    },
    {
        "priority": 3,
        "target": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "task": "test whether finite-cell fibre spectra can be integrated out or reduced to universal constants",
        "pass_condition": "finite fibre does not create local matter-visible marker channels",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_impact_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    rows: list[dict[str, Any]] = []
    for impact in ROW_IMPACT:
        matrix_row = matrix_by_id.get(impact["row_id"], {})
        rows.append(
            {
                "row_id": impact["row_id"],
                "previous_state": matrix_row.get("runner_v4_state", "missing"),
                "new_state": impact["new_state"],
                "reason": impact["reason"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in impact_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in impact_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "candidate_before_score_contract_written",
            "status": "pass",
            "evidence": "G_parent[fields] -> D_i before C_exp[D_i]",
        },
        {
            "gate": "candidate_sources_written",
            "status": "pass",
            "evidence": f"{len(CANDIDATE_DOMAIN_SOURCES)} candidate sources classified",
        },
        {
            "gate": "empirical_windows_blocked",
            "status": "pass",
            "evidence": "residual-based domain windows forbidden",
        },
        {
            "gate": "Newton_GR_import_blocked",
            "status": "pass",
            "evidence": "Newtonian binding and GR turnaround imports forbidden",
        },
        {
            "gate": "parent_candidate_generator_derived",
            "status": "fail",
            "evidence": "candidate family/measure is contract-level only",
        },
        {
            "gate": "single_rule_local_FLRW_derived",
            "status": "fail",
            "evidence": "same generator has not derived both local and FLRW branches",
        },
        {
            "gate": "boundary_exchange_attached",
            "status": "fail",
            "evidence": "candidate domains do not yet carry owned boundary exchange currents",
        },
        {
            "gate": "arbitrary_candidate_family_removed",
            "status": "fail",
            "evidence": "finite/integrable parent measure over D_i is not derived",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{len(theorem_rows)} theorem-credit row upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "domain-candidate contract only; no EH/Newton/PPN/local-GR pass",
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


def write_checkpoint_markdown(
    run_dir: Path,
    impact_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    contract_table_rows = [
        {
            "item": row["contract_item"],
            "status": row["status"],
            "requirement": row["requirement"],
        }
        for row in DOMAIN_GENERATOR_CONTRACT
    ]
    source_table_rows = [
        {
            "source": row["source"],
            "status": row["status"],
            "risk": row["risk"],
        }
        for row in CANDIDATE_DOMAIN_SOURCES
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in SCORING_CHAIN
    ]
    test_table_rows = [
        {
            "test": row["test"],
            "result": row["current_result"],
        }
        for row in ANTI_CIRCULARITY_TESTS
    ]
    impact_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
        }
        for row in impact_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 418 - Cexp Domain Candidate Generator

Private domain-selector/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 417 left the domain circularity problem: `C_exp[D]` cannot honestly select a domain if `D` was chosen after the fact. This checkpoint writes the candidates-first contract: parent variables must generate candidate domains before `C_exp` scores them.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Cexp_domain_candidate_generator.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Domain Generator Contract

{markdown_table(contract_table_rows, ["item", "status", "requirement"])}

## 4. Candidate Domain Sources

{markdown_table(source_table_rows, ["source", "status", "risk"])}

## 5. Scoring Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

## 6. Anti-Circularity Tests

{markdown_table(test_table_rows, ["test", "result"])}

## 7. Row Impact

{markdown_table(impact_table_rows, ["row_id", "previous_state", "new_state"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: this is the fair-play rule for `C_exp`. We can use it as footwork only after the ring is drawn by the theory, not by the judges after the round.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    impact_rows = row_impact_rows()
    gate_result_rows = gate_rows(source_rows, impact_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "domain_generator_contract.csv", DOMAIN_GENERATOR_CONTRACT)
    write_csv(results_dir / "candidate_domain_sources.csv", CANDIDATE_DOMAIN_SOURCES)
    write_csv(results_dir / "scoring_chain.csv", SCORING_CHAIN)
    write_csv(results_dir / "anti_circularity_tests.csv", ANTI_CIRCULARITY_TESTS)
    write_csv(results_dir / "row_impact.csv", impact_rows)
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
        "candidate_before_score_contract_written": True,
        "empirical_windows_blocked": True,
        "Newton_GR_import_blocked": True,
        "parent_candidate_generator_derived": False,
        "boundary_exchange_attached": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, impact_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 418 C_exp domain candidate generator artifacts."
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
