from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-quotient-invariant-algebra-triviality-gate"
CHECKPOINT_DOC = "414-local-quotient-invariant-algebra-triviality-gate.md"
STATUS = "local_quotient_invariant_algebra_triviality_gate_written_triviality_condition_exact_extra_generators_remain_no_R0_promotion_no_local_GR_pass"
CLAIM_CEILING = "local_quotient_invariant_algebra_triviality_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "415-local-trivial-class-selector-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "fixed relative-class admissibility and open physical class selection",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "configuration-space sketch with finite fibre and boundary/domain class",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "quotient matter functor and invariant class counterexamples",
    },
    {
        "path": "413-no-marker-parent-action-theorem-attempt.md",
        "role": "no-marker theorem attempt pointing to invariant algebra triviality",
    },
    {
        "path": "62-domain-field-chiD-action-contract.md",
        "role": "domain selector/action contract and open physical domain selection",
    },
    {
        "path": "68-chiD-gated-memory-conservation-contract.md",
        "role": "chi_D-gated memory conservation contract and boundary exchange caveat",
    },
    {
        "path": "73-local-route-blocker-ledger-and-promotion-gate.md",
        "role": "local blocker ledger and promotion gate",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux hard local rows",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
    {
        "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/counterexample_markers.csv",
        "role": "marker counterexamples needing invariant algebra blockers",
    },
]


INVARIANT_GENERATORS = [
    {
        "generator": "constants",
        "symbolic_form": "R, fixed universal theta",
        "quotient_invariant": True,
        "independent_of_e_obs": False,
        "local_vacuum_status": "harmless_if_universal",
        "row_links": "R1;R2;R9",
        "verdict": "allowed_only_as_universal_constants",
    },
    {
        "generator": "observed_geometry_jets",
        "symbolic_form": "J^k(e_obs), R[g_obs], curvature scalars",
        "quotient_invariant": True,
        "independent_of_e_obs": False,
        "local_vacuum_status": "allowed_geometry",
        "row_links": "R3;R4;R11",
        "verdict": "allowed_but_EH_operator_selection_still_separate",
    },
    {
        "generator": "finite_cell_fibre_spectrum",
        "symbolic_form": "spectrum(h), trace powers tr(h^n)",
        "quotient_invariant": True,
        "independent_of_e_obs": True,
        "local_vacuum_status": "not_trivialized",
        "row_links": "R0;R1;R10",
        "verdict": "extra_marker_generator_until_integrated_out_or_constant",
    },
    {
        "generator": "relative_boundary_domain_class",
        "symbolic_form": "Q_rel, [J_rel], H_rel",
        "quotient_invariant": True,
        "independent_of_e_obs": True,
        "local_vacuum_status": "fixed_class_admissibility_only",
        "row_links": "R5;R6;R7;R8;R9",
        "verdict": "extra_generator_until_physical_local_trivial_class_is_derived",
    },
    {
        "generator": "domain_selector_chi_D",
        "symbolic_form": "chi_D, Sigma_D=boundary/level set",
        "quotient_invariant": True,
        "independent_of_e_obs": True,
        "local_vacuum_status": "selector_contract_not_physical_selection",
        "row_links": "R5;R6;R8;R9",
        "verdict": "extra_marker_generator_until domain selection theorem",
    },
    {
        "generator": "memory_or_class_scalar",
        "symbolic_form": "C_D, P_D C, I_Q",
        "quotient_invariant": True,
        "independent_of_e_obs": True,
        "local_vacuum_status": "not_silenced_as_theorem",
        "row_links": "R2;R3;R10",
        "verdict": "extra_generator_until local value and gradient vanish or are bounded",
    },
    {
        "generator": "orientation_time_arrow",
        "symbolic_form": "oriented volume/time-arrow class",
        "quotient_invariant": True,
        "independent_of_e_obs": "possibly",
        "local_vacuum_status": "not_classified",
        "row_links": "R5;R6;R7",
        "verdict": "extra_generator_until shown to be contained in e_obs or constant",
    },
    {
        "generator": "species_charge_constants",
        "symbolic_form": "theta_A(I_Q), q_A(m), m_A(C_D)",
        "quotient_invariant": True,
        "independent_of_e_obs": True,
        "local_vacuum_status": "not_universalized",
        "row_links": "R1;R2",
        "verdict": "extra_generator_until constant-sector universality theorem",
    },
    {
        "generator": "readout_projector",
        "symbolic_form": "P_read, P_active after projection",
        "quotient_invariant": "only_after_readout",
        "independent_of_e_obs": True,
        "local_vacuum_status": "no_cheat_rule_only",
        "row_links": "R0;R10;R11",
        "verdict": "extra_generator_if_varied_as_reduced_action",
    },
]


TRIVIALITY_CHAIN = [
    {
        "step": 1,
        "claim": "All fixed labels are quotient-gauge.",
        "identity": "functions on Q are constant on G_rel orbits",
        "status": "conditional_pass_from_strict_quotient",
    },
    {
        "step": 2,
        "claim": "The local vacuum relative/domain class is trivial.",
        "identity": "Q_rel=[J_rel]=H_rel=0 in local bound vacuum",
        "status": "not_derived",
    },
    {
        "step": 3,
        "claim": "Domain selector carries no independent local generator.",
        "identity": "chi_D is pure boundary bookkeeping or fixed by e_obs",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Finite cell fibre contributes only constants or integrated-out parameters.",
        "identity": "spectrum(h)=constant or absent from local matter vertices",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Memory/class scalar is locally silent.",
        "identity": "C_D=constant and grad C_D=0, or no matter coupling",
        "status": "not_derived",
    },
    {
        "step": 6,
        "claim": "Species constants are universal and independent of extra invariants.",
        "identity": "partial_I theta_A=0 for all non-geometric invariants I",
        "status": "not_derived",
    },
    {
        "step": 7,
        "claim": "Readout projectors are never parent-action variables.",
        "identity": "S_parent varied before P_read/P_active",
        "status": "conditional_template",
    },
    {
        "step": 8,
        "claim": "Local invariant algebra is geometry plus constants.",
        "identity": "I_loc(Q)=I_geom[J^k(e_obs)] tensor constants",
        "status": "conditional_target_not_derived",
    },
]


LOCAL_BRANCH_CASES = [
    {
        "branch": "strong_local_triviality",
        "assumption": "all non-geometric local invariant generators vanish, are constants, or are pure gauge",
        "result_if_true": "no-marker theorem becomes local; R0 can move toward theorem-zero",
        "current_status": "theorem_target",
    },
    {
        "branch": "fixed_relative_class_closure",
        "assumption": "local tests are restricted to Q_rel=0/trivial class by closure choice",
        "result_if_true": "runner can test closure branch honestly",
        "current_status": "allowed_closure_not_theorem",
    },
    {
        "branch": "cosmology_active_domain",
        "assumption": "FLRW/cosmology keeps active domain or memory class while local branch is silent",
        "result_if_true": "needs a selector separating local triviality from cosmological activity",
        "current_status": "open_selector_theorem",
    },
    {
        "branch": "material_marker_extension",
        "assumption": "extra marker m is admitted in Q_tilde",
        "result_if_true": "local GR branch fails unless m is bounded or decoupled",
        "current_status": "counterexample",
    },
]


ROW_IMPACT = [
    {
        "row_id": "R0_identity_coframe_direct",
        "impact": "would need all non-geometric matter-visible invariants absent",
        "new_state": "closure_zero",
        "reason": "invariant algebra triviality not derived",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "impact": "species constants/charges remain invariant-algebra debt",
        "new_state": "retained_contingent_budget",
        "reason": "constant-sector universality not derived",
    },
    {
        "row_id": "R2_clock_redshift",
        "impact": "class scalar or species constants can affect clocks",
        "new_state": "retained_budget",
        "reason": "memory/class scalar local silence not derived",
    },
    {
        "row_id": "R5_alpha1",
        "impact": "marker/domain vector leakage remains possible",
        "new_state": "retained_budget",
        "reason": "domain selector not trivialized",
    },
    {
        "row_id": "R7_alpha3",
        "impact": "boundary/domain flux generators remain possible",
        "new_state": "retained_contingent_budget",
        "reason": "relative class and Ward flux ownership still open",
    },
    {
        "row_id": "R9_Gdot",
        "impact": "domain scale drift and memory drift remain possible",
        "new_state": "retained_contingent_budget",
        "reason": "local trivial class and measured-GM drift silence not derived",
    },
    {
        "row_id": "R10_fifth_force",
        "impact": "class/memory scalar could mediate range-dependent force",
        "new_state": "unscored_parameterized",
        "reason": "range/charge/screening curve not derived",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "impact": "even trivial marker algebra does not select EH operator by itself",
        "new_state": "retained_residual",
        "reason": "EH operator selection remains separate",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The exact algebraic condition for the no-marker/local-GR route is now stated: in the local vacuum branch, the quotient-invariant algebra must reduce to observed-geometry jets plus universal constants. That would kill marker couplings without smuggling in a plateau axiom. The gate does not currently pass. Several quotient-invariant generators remain untrivialized: finite-cell spectra, relative boundary/domain class, chi_D domain selector, memory/class scalar, species constants, and readout projectors if varied as reduced actions. Therefore the local no-marker route remains a conditional theorem target or an explicit fixed-class closure, not a local-GR derivation.",
        "triviality_condition_written": True,
        "local_invariant_algebra_triviality_derived": False,
        "extra_generators_remaining": 7,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "try to derive local trivial relative/domain class under local bound vacuum/asymptotic conditions",
        "pass_condition": "Q_rel and chi_D become theorem-zero locally or remain explicit closure variables",
    },
    {
        "priority": 2,
        "target": "416-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "task": "test whether finite-cell fibre spectra can be integrated out or reduced to universal constants",
        "pass_condition": "finite fibre does not create local matter-visible marker channels",
    },
    {
        "priority": 3,
        "target": "417-local-bounds-data-intake-first-pass.md",
        "task": "fill the local-bound interface from verified sources and run the evaluator",
        "pass_condition": "external local-bound rows evaluate with references and no claim leaks",
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
                "impact": impact["impact"],
                "reason": impact["reason"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    generator_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    extra_generators = [
        row
        for row in generator_rows
        if str(row["independent_of_e_obs"]) == "True"
        or row["verdict"].startswith("extra_")
    ]
    claim_rows = [row for row in impact_rows if row["claim_allowed"]]
    theorem_rows = [row for row in impact_rows if row["theorem_credit_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "invariant_generator_register_written",
            "status": "pass",
            "evidence": f"{len(generator_rows)} candidate generators classified",
        },
        {
            "gate": "fixed_label_quotient_part_trivial",
            "status": "conditional_pass",
            "evidence": "fixed labels are removed if strict quotient parent is proven",
        },
        {
            "gate": "extra_generators_eliminated",
            "status": "fail",
            "evidence": f"{len(extra_generators)} extra or independent generators remain",
        },
        {
            "gate": "local_relative_class_triviality_derived",
            "status": "fail",
            "evidence": "Q_rel/[J_rel]/chi_D local trivial class is next target, not proven here",
        },
        {
            "gate": "finite_fibre_decoupling_derived",
            "status": "fail",
            "evidence": "finite-cell fibre spectrum is not yet integrated out or made universal",
        },
        {
            "gate": "constant_sector_universality_derived",
            "status": "fail",
            "evidence": "species constants can still depend on marker/class invariants",
        },
        {
            "gate": "local_invariant_algebra_triviality_derived",
            "status": "fail",
            "evidence": "I_loc(Q)=I_geom[e_obs] tensor constants is stated but not derived",
        },
        {
            "gate": "no_theorem_credit_or_claim_leaks",
            "status": "pass" if not theorem_rows and not claim_rows else "fail",
            "evidence": f"theorem_credit={len(theorem_rows)} claim_allowed={len(claim_rows)}",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "invariant-algebra gate only; no EH/Newton/PPN/local-GR pass",
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
    generator_table_rows = [
        {
            "generator": row["generator"],
            "local_status": row["local_vacuum_status"],
            "verdict": row["verdict"],
        }
        for row in INVARIANT_GENERATORS
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in TRIVIALITY_CHAIN
    ]
    branch_table_rows = [
        {
            "branch": row["branch"],
            "current_status": row["current_status"],
            "result_if_true": row["result_if_true"],
        }
        for row in LOCAL_BRANCH_CASES
    ]
    impact_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
            "reason": row["reason"],
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
    text = f"""# 414 - Local Quotient-Invariant Algebra Triviality Gate

Private invariant-algebra/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 413 showed that fixed active labels can be excluded by strict quotient logic, but material markers survive unless the local quotient has no extra matter-visible invariant generators. This checkpoint states and tests that exact algebraic burden.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_quotient_invariant_algebra_triviality_gate.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Triviality Condition

For the local no-marker/local-GR route to be derived, the local quotient-invariant algebra must reduce to observed geometry plus universal constants:

```text
I_loc(Q) = I_geom[J^k(e_obs)] tensor constants
```

Any independent local generator can become a marker, a source-charge channel, a clock drift, a fifth force, a domain projector, or a non-EH operator unless separately silenced.

## 4. Candidate Generators

{markdown_table(generator_table_rows, ["generator", "local_status", "verdict"])}

## 5. Triviality Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

## 6. Local Branch Cases

{markdown_table(branch_table_rows, ["branch", "current_status", "result_if_true"])}

## 7. Row Impact

{markdown_table(impact_table_rows, ["row_id", "previous_state", "new_state", "reason"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: this narrows the problem sharply. We are not saying “no markers because we dislike markers.” We now need to prove a concrete algebra statement, or explicitly run local tests as a fixed-class closure branch.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    impact_rows = row_impact_rows()
    gate_result_rows = gate_rows(source_rows, INVARIANT_GENERATORS, impact_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "invariant_generators.csv", INVARIANT_GENERATORS)
    write_csv(results_dir / "triviality_chain.csv", TRIVIALITY_CHAIN)
    write_csv(results_dir / "local_branch_cases.csv", LOCAL_BRANCH_CASES)
    write_csv(results_dir / "row_impact.csv", impact_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    extra_generators = [
        row
        for row in INVARIANT_GENERATORS
        if str(row["independent_of_e_obs"]) == "True"
        or row["verdict"].startswith("extra_")
    ]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "candidate_generators": len(INVARIANT_GENERATORS),
        "extra_generators_remaining": len(extra_generators),
        "local_invariant_algebra_triviality_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
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
        description="Write checkpoint 414 local quotient-invariant algebra triviality gate artifacts."
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
