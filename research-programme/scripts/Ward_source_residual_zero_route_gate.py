from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Ward-source-residual-zero-route-gate"
CHECKPOINT_DOC = "430-Ward-source-residual-zero-route-gate.md"
STATUS = "Ward_source_residual_zero_route_gate_written_C0_C7_ranked_derivation_vs_bound_routes_no_zero_promotion_no_local_GR_pass"
CLAIM_CEILING = "Ward_source_residual_zero_route_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "431-MTS-local-residual-vector-evaluator.md"


SOURCE_DOCS = [
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "conditional Ward/Bianchi q_loc identity and C0-C7 zero conditions",
    },
    {
        "path": "428-MTS-local-residual-vector-input-contract.md",
        "role": "12-component residual-vector contract",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "EH/source-normalization retained ledger",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "Ward closure not enough for EH operator selection",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "Ward-force fates and no-hair/retained residual map",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "parent Ward force ledger and projector variation fork",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/exchange_owner_conditions.csv",
        "role": "C0-C7 machine-readable conditions",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv",
        "role": "source_residuals term decomposition",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/mu_extra_decomposition.csv",
        "role": "mu_extra channel decomposition",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "R0-R11 residual vector components",
    },
    {
        "path": "runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv",
        "role": "sourced local-bound row locks",
    },
]


ROUTE_RANKING = [
    {
        "rank": 1,
        "condition_id": "C1_auxiliary_on_shell",
        "route_class": "best_theorem_route",
        "route": "derive all auxiliary/projector/domain Euler equations from the parent action and show E_A=0 in the local exterior",
        "derivation_status": "structurally_available_not_supplied",
        "bound_fallback": "retain q_loc/alpha3/Gdot/fifth-force contributions in residual vector",
        "blocks_rows": "R7;R9;R10;R11",
        "why_ranked_here": "this is the direct Ward/Bianchi owner of the off-shell force term",
        "promotion_effect_if_solved": "kills the E_Z nabla Z part of q_loc",
    },
    {
        "rank": 2,
        "condition_id": "C0_same_frame",
        "route_class": "hard_theorem_route",
        "route": "derive universal single observed metric/coframe matter coupling for clocks, rods, photons, and masses",
        "derivation_status": "not_parent_derived",
        "bound_fallback": "evaluate WEP, clock, gamma, beta residuals as empirical retained rows",
        "blocks_rows": "R0;R1;R2;R3;R4;R11",
        "why_ranked_here": "without same-frame ownership, source and metric equations can be fair-looking but not GR",
        "promotion_effect_if_solved": "removes nonmetric/frame exchange and makes local residuals physically comparable",
    },
    {
        "rank": 3,
        "condition_id": "C5_constant_kappa_Geff",
        "route_class": "hard_source_normalization_route",
        "route": "derive kappa_eff/G_eff as constant, universal, species-independent, and range-independent in the local branch",
        "derivation_status": "not_derived",
        "bound_fallback": "score R1/R4/R9/R10 source-normalization residuals",
        "blocks_rows": "R1;R4;R9;R10",
        "why_ranked_here": "Poisson can look right while G_eff or measured GM drifts",
        "promotion_effect_if_solved": "kills T_obs nabla kappa_eff and major source_residual terms",
    },
    {
        "rank": 4,
        "condition_id": "C6_mu_extra_zero",
        "route_class": "hard_measured_source_route",
        "route": "derive mu_obs=G_eff M_eff with no hidden species/time/range/domain/boundary correction",
        "derivation_status": "not_derived",
        "bound_fallback": "keep mu_extra channels split across WEP source, beta, Gdot, fifth-force, preferred-frame rows",
        "blocks_rows": "R1;R4;R5;R6;R7;R8;R9;R10",
        "why_ranked_here": "Ward can conserve a hidden contribution without making it absent from measured GM",
        "promotion_effect_if_solved": "turns Poisson algebra into measured Newton source normalization",
    },
    {
        "rank": 5,
        "condition_id": "C2_projector_covariant",
        "route_class": "mixed_theorem_or_bound_route",
        "route": "prove P_D is covariant/dynamical/topological and not a fixed external projector",
        "derivation_status": "conditional_open",
        "bound_fallback": "map projector/domain vector leakage to alpha1/alpha2/alpha3/xi rows",
        "blocks_rows": "R5;R6;R7;R8;R11",
        "why_ranked_here": "fixed projectors are forbidden; covariant projectors still may carry local hair",
        "promotion_effect_if_solved": "removes explicit diffeo breaking, but no-hair still required",
    },
    {
        "rank": 6,
        "condition_id": "C3_boundary_nohair",
        "route_class": "mostly_bound_until_nohair_theorem",
        "route": "prove boundary terms are class/topological constants or conserved monopoles with no shear/vector/drift",
        "derivation_status": "not_derived",
        "bound_fallback": "retain boundary coefficients against gamma/beta/alpha3/xi/Gdot locks",
        "blocks_rows": "R3;R4;R7;R8;R9",
        "why_ranked_here": "boundary ownership is not the same as local silence",
        "promotion_effect_if_solved": "collapses boundary flux/source_residuals to harmless calibration",
    },
    {
        "rank": 7,
        "condition_id": "C4_nonEH_divergence_silent",
        "route_class": "operator_selection_or_bound_route",
        "route": "derive EH-only exterior operator or supply non-EH coefficient vector mapped below bounds",
        "derivation_status": "retained",
        "bound_fallback": "R11 coefficient vector plus induced R3/R4/R5/R6/R8/R10 residuals",
        "blocks_rows": "R3;R4;R5;R6;R8;R10;R11",
        "why_ranked_here": "Ward-conserved non-EH operators are common counterexamples to local GR",
        "promotion_effect_if_solved": "essential for EH/local-GR route, otherwise empirical modified-gravity branch only",
    },
    {
        "rank": 8,
        "condition_id": "C7_R10_R11_resolved",
        "route_class": "executable_symbolic_blocker",
        "route": "provide alpha(lambda) curve and non-EH operator coefficient vector, or prove both theorem-zero",
        "derivation_status": "symbolic_deferred",
        "bound_fallback": "make R10/R11 executable and compare; do not claim symbolic pass",
        "blocks_rows": "R10;R11",
        "why_ranked_here": "not conceptually first, but absolutely blocks any all-row local-GR pass",
        "promotion_effect_if_solved": "turns symbolic blockers into evaluated residuals or theorem-zero channels",
    },
]


ZERO_ROUTE_GATE = [
    {
        "gate_id": "G0_forbidden_route",
        "route_type": "forbid",
        "description": "fixed external projector, dropped metric-dependent stress, or hidden frame split",
        "conditions": "C0;C2",
        "result_if_present": "invalid parent/local-GR route",
        "action": "reject branch, not merely bound",
    },
    {
        "gate_id": "G1_direct_Ward_zero",
        "route_type": "derive",
        "description": "auxiliary equations and Ward force terms vanish on-shell in local exterior",
        "conditions": "C1",
        "result_if_present": "q_loc off-shell source removed",
        "action": "promote only the specific force term, not full local GR",
    },
    {
        "gate_id": "G2_same_frame_zero",
        "route_type": "derive",
        "description": "one universal observed metric/coframe for matter and gravity",
        "conditions": "C0",
        "result_if_present": "nonmetric matter exchange removed",
        "action": "allow WEP/clock frame rows to seek theorem-zero",
    },
    {
        "gate_id": "G3_source_normalization_zero",
        "route_type": "derive",
        "description": "constant kappa/G_eff and mu_extra=0",
        "conditions": "C5;C6",
        "result_if_present": "Poisson source becomes measured Newton source",
        "action": "allow source_residuals/mu_extra rows to seek theorem-zero",
    },
    {
        "gate_id": "G4_nohair_zero",
        "route_type": "derive_or_bound",
        "description": "boundary/domain/projector hair vanishes, is pure gauge/topological, or is bounded",
        "conditions": "C2;C3",
        "result_if_present": "PPN vector/shear/flux residuals controlled",
        "action": "if not theorem-zero, carry coefficients into residual evaluator",
    },
    {
        "gate_id": "G5_operator_zero",
        "route_type": "derive_or_bound",
        "description": "EH-only exterior or mapped non-EH coefficient vector",
        "conditions": "C4;C7",
        "result_if_present": "operator residuals become testable or vanish",
        "action": "block local-GR promotion while symbolic",
    },
]


SOURCE_RESIDUAL_ROUTE_MATRIX = [
    {
        "source_residual_term": "delta_kappa_source",
        "zero_route": "derive C5 from scale/source-normalization theorem",
        "bound_route": "R1/R4/R9 numeric residuals and R10 source-range row",
        "current_route_status": "bound_route_ready_derivation_missing",
        "next_required_artifact": "kappa/G_eff local constancy lemma",
    },
    {
        "source_residual_term": "nonEH_divergence",
        "zero_route": "derive EH-only exterior or pure-boundary non-EH terms",
        "bound_route": "R11 coefficient vector mapped to PPN/fifth-force rows",
        "current_route_status": "symbolic_blocker",
        "next_required_artifact": "R10-R11 curve/operator-vector contract",
    },
    {
        "source_residual_term": "auxiliary_offshell_force",
        "zero_route": "derive E_Z=0 for every local auxiliary/domain/memory variable",
        "bound_route": "alpha3/Gdot/fifth-force residual vector components",
        "current_route_status": "best_derivation_target_open",
        "next_required_artifact": "parent local auxiliary Euler-equation ledger",
    },
    {
        "source_residual_term": "projector_domain_force",
        "zero_route": "prove covariant/topological projector and no preferred-frame vector hair",
        "bound_route": "alpha1/alpha2/alpha3/xi rows",
        "current_route_status": "mixed_route",
        "next_required_artifact": "projector no-vector/no-shear lemma",
    },
    {
        "source_residual_term": "boundary_flux",
        "zero_route": "class/topological boundary leaves only fixed universal monopole",
        "bound_route": "gamma/beta/alpha3/xi/Gdot retained coefficients",
        "current_route_status": "mostly_bound_route",
        "next_required_artifact": "boundary class-only nohair theorem attempt",
    },
    {
        "source_residual_term": "nonmetric_matter_exchange",
        "zero_route": "universal matter metric/coframe theorem",
        "bound_route": "WEP/clock/gamma/beta source rows",
        "current_route_status": "hard_theorem_route_open",
        "next_required_artifact": "same-frame matter functor theorem attempt",
    },
]


MU_EXTRA_ROUTE_MATRIX = [
    {
        "mu_channel": "species_source_charge",
        "zero_route": "derive material/species blindness of source coupling",
        "bound_route": "R1 direct/full source-charge residual",
        "current_route_status": "hard_theorem_route_open",
    },
    {
        "mu_channel": "time_drift",
        "zero_route": "derive stationary local kappa and conserved measured mass",
        "bound_route": "R9 Gdot/G residual",
        "current_route_status": "bound_route_ready_derivation_missing",
    },
    {
        "mu_channel": "range_dependence",
        "zero_route": "prove no finite-range local force",
        "bound_route": "R10 alpha(lambda) curve",
        "current_route_status": "symbolic_blocker",
    },
    {
        "mu_channel": "boundary_monopole_shift",
        "zero_route": "prove only universal fixed calibration survives",
        "bound_route": "R4/R9 source-normalization residuals",
        "current_route_status": "mostly_bound_route",
    },
    {
        "mu_channel": "domain_projector_mass",
        "zero_route": "derive no preferred-frame/location/domain mass correction",
        "bound_route": "R5/R6/R7/R8/R11 residuals",
        "current_route_status": "mixed_route",
    },
]


PROMOTION_DECISION_TREE = [
    {
        "decision_node": "D0_invalid",
        "test": "fixed external projector, hidden frame split, dropped stress, or placeholder symbolic pass exists",
        "outcome": "reject branch",
        "local_GR_credit": "none",
    },
    {
        "decision_node": "D1_empirical_viability",
        "test": "all numeric residuals below bounds and R10/R11 executable but derivation statuses include fitted/phenomenological/closure",
        "outcome": "viable modified-gravity/MTS stress-test branch",
        "local_GR_credit": "empirical_only_no_derived_GR",
    },
    {
        "decision_node": "D2_partial_theorem",
        "test": "some C0-C7 conditions theorem-zero but others bounded/retained",
        "outcome": "partial local-GR support with retained residual vector",
        "local_GR_credit": "partial_no_promotion",
    },
    {
        "decision_node": "D3_derived_local_GR_candidate",
        "test": "C0-C7 theorem-zero or harmless universal calibration plus EH/local PPN completion",
        "outcome": "candidate derived local GR reduction",
        "local_GR_credit": "candidate_only_pending independent audit",
    },
]


NEXT_DERIVATION_QUEUE = [
    {
        "queue_id": "Q1",
        "target": "same-frame matter functor theorem",
        "conditions": "C0",
        "reason": "without universal matter metric/coframe, local residuals are not GR-comparable",
        "suggested_next_file": "431-same-frame-matter-functor-zero-route.md",
    },
    {
        "queue_id": "Q2",
        "target": "kappa/G_eff local constancy lemma",
        "conditions": "C5",
        "reason": "direct source_residual term and Gdot/source-charge rows depend on this",
        "suggested_next_file": "431-kappa-Geff-local-constancy-lemma.md",
    },
    {
        "queue_id": "Q3",
        "target": "mu_extra measured-source nohair theorem",
        "conditions": "C6",
        "reason": "Ward ownership does not prove absence from measured GM",
        "suggested_next_file": "431-mu-extra-measured-source-nohair-theorem.md",
    },
    {
        "queue_id": "Q4",
        "target": "MTS local residual-vector evaluator",
        "conditions": "all",
        "reason": "we need executable empirical stress tests while derivations remain partial",
        "suggested_next_file": "431-MTS-local-residual-vector-evaluator.md",
    },
]


DECISION = [
    {
        "decision": "C0-C7 have been ranked into theorem, mixed, bound, and symbolic-blocker routes. The strongest derivation path is C1 auxiliary on-shell plus C0 same-frame plus C5/C6 source normalization. The weakest immediate path is C4/C7, which must become an executable non-EH/fifth-force coefficient contract or remain a hard local-GR blocker. No zero route is promoted yet.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "best_derivation_routes": "C1;C0;C5;C6",
        "mostly_bound_routes": "C2;C3;C4",
        "symbolic_blockers": "C7 plus unresolved C4",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "431-MTS-local-residual-vector-evaluator.md",
        "task": "build evaluator for a filled MTS residual prediction file, with derivation-status gates and no symbolic R10/R11 pass",
        "priority": "P0",
    },
    {
        "next_file": "431-same-frame-matter-functor-zero-route.md",
        "task": "attempt the C0 theorem route for universal observed metric/coframe matter coupling",
        "priority": "P0",
    },
    {
        "next_file": "431-kappa-Geff-local-constancy-lemma.md",
        "task": "attempt C5 local constancy of kappa/G_eff and define fallback residuals",
        "priority": "P1",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        path = ROOT / item["path"]
        rows.append({"source_file": item["path"], "exists": path.exists(), "role": item["role"]})
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    theorem_promoted = []
    symbolic_blockers = [row for row in ROUTE_RANKING if row["route_class"] == "executable_symbolic_blocker"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "C0_C7_ranked",
            "status": "pass" if len(ROUTE_RANKING) == 8 else "fail",
            "evidence": f"{len(ROUTE_RANKING)} ranked conditions",
        },
        {
            "gate": "zero_route_gate_written",
            "status": "pass" if len(ZERO_ROUTE_GATE) == 6 else "fail",
            "evidence": f"{len(ZERO_ROUTE_GATE)} route gates",
        },
        {
            "gate": "source_residual_route_matrix_written",
            "status": "pass" if len(SOURCE_RESIDUAL_ROUTE_MATRIX) == 6 else "fail",
            "evidence": f"{len(SOURCE_RESIDUAL_ROUTE_MATRIX)} source-residual routes",
        },
        {
            "gate": "mu_extra_route_matrix_written",
            "status": "pass" if len(MU_EXTRA_ROUTE_MATRIX) == 5 else "fail",
            "evidence": f"{len(MU_EXTRA_ROUTE_MATRIX)} mu_extra routes",
        },
        {
            "gate": "promotion_decision_tree_written",
            "status": "pass" if len(PROMOTION_DECISION_TREE) == 4 else "fail",
            "evidence": f"{len(PROMOTION_DECISION_TREE)} decision nodes",
        },
        {
            "gate": "symbolic_blockers_identified",
            "status": "pass" if symbolic_blockers else "fail",
            "evidence": ";".join(row["condition_id"] for row in symbolic_blockers),
        },
        {
            "gate": "theorem_zero_promoted",
            "status": "pass" if not theorem_promoted else "fail",
            "evidence": f"{len(theorem_promoted)} theorem-zero promotions",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "route gate only; C0-C7 not solved",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_cell(row[column]) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(run_dir: Path, source_rows: list[dict[str, Any]], gate_result_rows: list[dict[str, str]]) -> None:
    source_table_rows = [
        {"source_file": row["source_file"], "exists": row["exists"], "role": row["role"]}
        for row in source_rows
    ]
    route_rows = [
        {
            "rank": row["rank"],
            "condition_id": row["condition_id"],
            "route_class": row["route_class"],
            "derivation_status": row["derivation_status"],
            "blocks_rows": row["blocks_rows"],
        }
        for row in ROUTE_RANKING
    ]
    zero_gate_rows = [
        {
            "gate_id": row["gate_id"],
            "route_type": row["route_type"],
            "conditions": row["conditions"],
            "action": row["action"],
        }
        for row in ZERO_ROUTE_GATE
    ]
    source_route_rows = [
        {
            "source_residual_term": row["source_residual_term"],
            "current_route_status": row["current_route_status"],
            "next_required_artifact": row["next_required_artifact"],
        }
        for row in SOURCE_RESIDUAL_ROUTE_MATRIX
    ]
    mu_route_rows = [
        {
            "mu_channel": row["mu_channel"],
            "zero_route": row["zero_route"],
            "bound_route": row["bound_route"],
            "current_route_status": row["current_route_status"],
        }
        for row in MU_EXTRA_ROUTE_MATRIX
    ]
    decision_tree_rows = [
        {
            "decision_node": row["decision_node"],
            "test": row["test"],
            "outcome": row["outcome"],
            "local_GR_credit": row["local_GR_credit"],
        }
        for row in PROMOTION_DECISION_TREE
    ]
    derivation_queue_rows = [
        {
            "queue_id": row["queue_id"],
            "target": row["target"],
            "conditions": row["conditions"],
            "suggested_next_file": row["suggested_next_file"],
        }
        for row in NEXT_DERIVATION_QUEUE
    ]
    gate_table_rows = [
        {"gate": row["gate"], "status": row["status"], "evidence": row["evidence"]}
        for row in gate_result_rows
    ]
    text = f"""# 430 - Ward Source-Residual Zero Route Gate

Private route-ranking checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 429 gave the conditional Ward/Bianchi identity for `q_loc^nu`. This checkpoint ranks the C0-C7 zero conditions by route: what looks theorem-derivable, what is mixed, what is only empirically boundable for now, and what remains a hard symbolic blocker.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/Ward_source_residual_zero_route_gate.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_table_rows, ["source_file", "exists", "role"])}

## 4. C0-C7 Route Ranking

{markdown_table(route_rows, ["rank", "condition_id", "route_class", "derivation_status", "blocks_rows"])}

The useful read is:

```text
best theorem pressure: C1, C0, C5, C6
mixed theorem/bound pressure: C2, C3, C4
hard symbolic blocker: C7, plus unresolved C4
```

## 5. Zero Route Gate

{markdown_table(zero_gate_rows, ["gate_id", "route_type", "conditions", "action"])}

## 6. Source-Residual Route Matrix

{markdown_table(source_route_rows, ["source_residual_term", "current_route_status", "next_required_artifact"])}

## 7. `mu_extra` Route Matrix

{markdown_table(mu_route_rows, ["mu_channel", "zero_route", "bound_route", "current_route_status"])}

## 8. Promotion Decision Tree

{markdown_table(decision_tree_rows, ["decision_node", "test", "outcome", "local_GR_credit"])}

## 9. Next Derivation Queue

{markdown_table(derivation_queue_rows, ["queue_id", "target", "conditions", "suggested_next_file"])}

## 10. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is where the work stops being vague. We either push theorem routes C1/C0/C5/C6, or we build the residual evaluator and let the retained rows fight the sourced bounds. Both are legitimate. What is no longer legitimate is pretending a Ward identity alone hands us local GR.

## 12. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "route_ranking.csv", ROUTE_RANKING)
    write_csv(results_dir / "zero_route_gate.csv", ZERO_ROUTE_GATE)
    write_csv(results_dir / "source_residual_route_matrix.csv", SOURCE_RESIDUAL_ROUTE_MATRIX)
    write_csv(results_dir / "mu_extra_route_matrix.csv", MU_EXTRA_ROUTE_MATRIX)
    write_csv(results_dir / "promotion_decision_tree.csv", PROMOTION_DECISION_TREE)
    write_csv(results_dir / "next_derivation_queue.csv", NEXT_DERIVATION_QUEUE)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_gates = [
        row["gate"]
        for row in gate_result_rows
        if row["status"] == "fail" and row["gate"] != "local_GR_promoted"
    ]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "ranked_conditions": len(ROUTE_RANKING),
        "zero_route_gates": len(ZERO_ROUTE_GATE),
        "source_residual_routes": len(SOURCE_RESIDUAL_ROUTE_MATRIX),
        "mu_extra_routes": len(MU_EXTRA_ROUTE_MATRIX),
        "best_derivation_routes": ["C1", "C0", "C5", "C6"],
        "symbolic_blockers": ["C7", "C4_unresolved"],
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "failed_operational_gates": failed_gates,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, source_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 430 Ward source-residual zero route gate."
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
