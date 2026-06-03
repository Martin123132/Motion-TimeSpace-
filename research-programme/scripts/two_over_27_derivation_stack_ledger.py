from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "two-over-27-derivation-stack-ledger"
STATUS = "two_over_27_stack_ledger_closure_contract_not_parent_derivation"
CLAIM_CEILING = "locked_empirical_closure_with_conditional_derivation_stack_no_full_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "283-fixed-vs-kappa-short-smoke-readout.md", "fixed 2/27 branch empirical support against kappa-free branch"),
        (ROOT / "286-memory-stress-normalization-scale-no-go.md", "scale no-go showing stress equations do not derive amplitude"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "boundary current support and missing charge unit"),
        (ROOT / "288-k9-Ward-index-level-attempt.md", "rank-nine target before explicit relative index"),
        (ROOT / "291-CPL-prior-sensitivity-readout.md", "latest no-SH0ES/CPL baseline caution"),
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional k=9 relative-index route"),
        (ROOT / "293-domain-topology-selection-attempt.md", "conditional B3 domain topology theorem target"),
        (ROOT / "294-endpoint-occupancy-arrow-law-attempt.md", "conditional endpoint rank-defect law"),
        (ROOT / "295-arrow-semigroup-parent-time-attempt.md", "conditional semigroup/H-theorem arrow"),
        (ROOT / "296-positive-coarse-graining-parent-action-attempt.md", "open/Onsager parent-time contract"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def derivation_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "stack_item": "empirical_target_Bmem",
            "formula_or_statement": "B_mem=2/27",
            "status": "locked_empirical_closure",
            "support": "fixed no-clock branch remains competitive in short SN+BAO diagnostics",
            "blocker": "empirical support is mixed/short-smoke and does not derive parent amplitude",
            "promotion_requirement": "full robustness plus parent derivation stack",
        },
        {
            "stack_item": "stress_shape_equations",
            "formula_or_statement": "memory stress/hazard equations shape the branch",
            "status": "partial_support",
            "support": "checkpoint 286 shows shape-like behaviour is possible",
            "blocker": "equations are homogeneous in B_mem",
            "promotion_requirement": "external boundary charge or normalized parent current",
        },
        {
            "stack_item": "boundary_current_owner",
            "formula_or_statement": "relative current J_B=(j_3,b_2)",
            "status": "formal_support",
            "support": "conserved relative current can be written",
            "blocker": "Q_* and endpoint occupancies are not selected",
            "promotion_requirement": "parent-owned charge quantization and endpoint law",
        },
        {
            "stack_item": "k_level",
            "formula_or_statement": "k=|index(End(TSigma_D),rel)|=9",
            "status": "conditional_pass",
            "support": "relative index gives -9 for single contractible B3 coherent cell",
            "blocker": "B3 domain topology not parent-selected",
            "promotion_requirement": "derive coherent domain as single contractible 3-cell",
        },
        {
            "stack_item": "domain_topology",
            "formula_or_statement": "D is B3-like: one S2 boundary, no H1/H2 cycles, irreducible interior",
            "status": "conditional_contract",
            "support": "exact topology theorem target formulated",
            "blocker": "single-boundary/no-cycle/irreducibility not action-derived",
            "promotion_requirement": "admissible-domain or boundary-sector principle",
        },
        {
            "stack_item": "trace_partition",
            "formula_or_statement": "Pi_iso(Q)=(Tr Q/3)I",
            "status": "conditional_pass",
            "support": "unique SO(3)-equivariant scalar projection gives factor 1/3",
            "blocker": "Ward stress coupling to FLRW source not parent-varied",
            "promotion_requirement": "parent stress variation couples only scalar trace charge",
        },
        {
            "stack_item": "endpoint_gap",
            "formula_or_statement": "Delta n=Tr(P_axis)-Tr(P_iso)=3-1=2",
            "status": "conditional_pass",
            "support": "projector-rank interpretation avoids built polynomial roots",
            "blocker": "early axis-resolved endpoint not parent-owned",
            "promotion_requirement": "derive early resolved axis-load occupancy",
        },
        {
            "stack_item": "endpoint_arrow",
            "formula_or_statement": "P_axis -> P_iso via Phi_tau=P_iso+exp(-gamma tau)(I-P_iso)",
            "status": "conditional_pass",
            "support": "semigroup/H-theorem gives monotone 3->1 for gamma>0",
            "blocker": "physical time and gamma>=0 not parent-derived",
            "promotion_requirement": "positive coarse-graining time from parent action",
        },
        {
            "stack_item": "open_parent_sector",
            "formula_or_statement": "Onsager/SK influence sector with positive noise or mobility",
            "status": "contract_only",
            "support": "would derive gamma>=0 if N>=0 and FDT/KMS-like condition holds",
            "blocker": "not present in current parent action",
            "promotion_requirement": "explicit open-boundary parent action",
        },
        {
            "stack_item": "full_amplitude_chain",
            "formula_or_statement": "B_mem=Delta n/(3*k)=2/(3*9)=2/27",
            "status": "conditional_chain_only",
            "support": "all mathematical factors now have candidate origins",
            "blocker": "multiple links remain conditional/contract-only",
            "promotion_requirement": "derive every upstream link in one parent action",
        },
        {
            "stack_item": "local_silence",
            "formula_or_statement": "q_loc -> 0 or PPN-safe bound in local domains",
            "status": "fail_unproven",
            "support": "none from the 2/27 stack",
            "blocker": "cosmology amplitude route does not suppress local source",
            "promotion_requirement": "derive local q_loc suppression and PPN residual bounds",
        },
        {
            "stack_item": "stable_empirical_evidence",
            "formula_or_statement": "fixed branch remains preferred under robust data/baselines",
            "status": "not_yet",
            "support": "short-smoke scorecards are promising but mixed",
            "blocker": "CPL/DR split/full covariance/CMB/local tests not settled",
            "promotion_requirement": "full-covariance and independent holdout robustness",
        },
    ]


def dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "parent": "B3_domain_topology",
            "child": "k=9_relative_index",
            "dependency_status": "conditional",
            "failure_effect": "index level can be 0 or 18 instead of 9",
        },
        {
            "parent": "SO3_trace_projection",
            "child": "trace_partition_1_over_3",
            "dependency_status": "conditional_pass",
            "failure_effect": "DeltaR does not become B_mem=DeltaR/3",
        },
        {
            "parent": "endpoint_projector_ranks",
            "child": "Delta_n=2",
            "dependency_status": "conditional_pass",
            "failure_effect": "endpoint gap returns to fitted/inserted value",
        },
        {
            "parent": "positive_semigroup_arrow",
            "child": "3_to_1_direction",
            "dependency_status": "conditional",
            "failure_effect": "projectors give endpoints but no physical arrow",
        },
        {
            "parent": "open_Onsager_or_influence_sector",
            "child": "positive_gamma_parent_owned",
            "dependency_status": "contract_only",
            "failure_effect": "arrow remains closure",
        },
        {
            "parent": "Ward_trace_stress_variation",
            "child": "FLRW_memory_source",
            "dependency_status": "not_derived",
            "failure_effect": "amplitude may not source cosmology consistently",
        },
        {
            "parent": "local_silence_filter",
            "child": "local_GR_PPN_safety",
            "dependency_status": "not_derived",
            "failure_effect": "cosmology branch could violate local gravity",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoints exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "ledger traceable",
        },
        {
            "gate": "Bmem_parent_derived",
            "status": "fail",
            "evidence": "full amplitude chain still includes conditional/contract-only links",
            "claim_effect": "no parent-amplitude promotion",
        },
        {
            "gate": "conditional_chain_exists",
            "status": "pass",
            "evidence": "B3 index, SO3 trace, projector gap, and semigroup arrow form a coherent conditional stack",
            "claim_effect": "theorem target is much sharper than raw closure",
        },
        {
            "gate": "ordinary_reversible_parent_sufficient",
            "status": "fail",
            "evidence": "irreversible projector arrow requires open/coarse-graining structure",
            "claim_effect": "future parent action must include open/Onsager/contact/influence sector",
        },
        {
            "gate": "local_GR_safe",
            "status": "fail",
            "evidence": "no q_loc suppression or PPN residual proof follows from this stack",
            "claim_effect": "local branch remains unpromoted",
        },
        {
            "gate": "stable_empirical_evidence_allowed",
            "status": "fail",
            "evidence": "SN+BAO short-smoke remains mixed; CPL/DR sensitivity not fully resolved",
            "claim_effect": "no public evidence claim",
        },
        {
            "gate": "closure_contract_written",
            "status": "pass",
            "evidence": "this ledger explicitly classifies derived/conditional/closure pieces",
            "claim_effect": "branch can be used safely as disciplined internal theory target",
        },
    ]


def closure_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "allowed_statement": "B_mem=2/27 is a locked empirical closure with a detailed conditional derivation stack.",
            "forbidden_statement": "B_mem=2/27 has been derived from the parent action.",
            "reason": "domain topology, open arrow, Ward stress coupling, and local silence remain unproved.",
        },
        {
            "allowed_statement": "k=9 has a conditional relative-index origin if the coherent domain is B3-like.",
            "forbidden_statement": "k=9 is unconditionally derived.",
            "reason": "the parent action has not selected the B3 topology.",
        },
        {
            "allowed_statement": "Delta n=2 has a clean projector-rank interpretation.",
            "forbidden_statement": "the physical endpoint arrow is fully derived.",
            "reason": "positive coarse-graining time is not parent-owned.",
        },
        {
            "allowed_statement": "The 2/27 stack is now a serious theorem target, not numerology.",
            "forbidden_statement": "MTS has completed its fundamental field theory amplitude derivation.",
            "reason": "the full chain is conditional and local-GR safety remains open.",
        },
        {
            "allowed_statement": "Short-smoke cosmology keeps the fixed branch worth testing.",
            "forbidden_statement": "MTS has stable cosmological evidence from current runs.",
            "reason": "current scorecards are mixed and not full-covariance/final-baseline robust.",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "explicit_open_boundary_parent_sector",
            "task": "write an SK/Onsager/contact parent sector with q_r, q_a, N>=0, Gamma>=0, Ward trace coupling, and local silence clauses",
            "success_gate": "positive gamma and scalar trace coupling derived without inserting 2/27",
        },
        {
            "priority": 2,
            "target": "local_silence_filter",
            "task": "derive or bound q_loc for the open-sector branch",
            "success_gate": "PPN residual vector is provably zero/suppressed in local domains",
        },
        {
            "priority": 3,
            "target": "full_covariance_empirical_run",
            "task": "move beyond 250-SN diagonal short smoke to stronger covariance/baseline handling",
            "success_gate": "fixed branch remains competitive without edge-dependent baselines",
        },
        {
            "priority": 4,
            "target": "non_SN_holdout",
            "task": "test the fixed branch against radial/growth/non-SN data not used to motivate the closure",
            "success_gate": "independent arena does not force branch demotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The 2/27 branch is no longer a loose empirical number: it now has a disciplined conditional stack "
                "through B3 relative index k=9, SO(3) trace partition, endpoint projector rank defect Delta n=2, "
                "and positive semigroup arrow. But it is not parent-derived because B3 topology, positive open-sector "
                "time, Ward stress coupling, local silence, and robust empirical promotion remain incomplete."
            ),
            "next_target": "explicit_open_boundary_parent_sector_then_local_silence_or_full_covariance_empirical_run",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "derivation_stack.csv": (
            derivation_stack_rows(),
            ["stack_item", "formula_or_statement", "status", "support", "blocker", "promotion_requirement"],
        ),
        "dependency_graph.csv": (
            dependency_rows(),
            ["parent", "child", "dependency_status", "failure_effect"],
        ),
        "promotion_gates.csv": (
            promotion_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "closure_contract.csv": (
            closure_contract_rows(),
            ["allowed_statement", "forbidden_statement", "reason"],
        ),
        "next_targets.csv": (
            next_target_rows(),
            ["priority", "target", "task", "success_gate"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "B_mem_parent_derived_now": False,
        "conditional_derivation_stack_exists": True,
        "local_GR_promoted_now": False,
        "stable_empirical_evidence_now": False,
        "next_target": "explicit_open_boundary_parent_sector_then_local_silence_or_full_covariance_empirical_run",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="2/27 derivation stack ledger.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
