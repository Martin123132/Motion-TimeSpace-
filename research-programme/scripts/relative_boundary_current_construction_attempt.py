#!/usr/bin/env python3
"""Attempt to construct the relative boundary current needed for C_coh exchange."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "59_topological_owner_doc": Path("59-topological-cell-current-owner-attempt.md"),
    "60_relative_boundary_doc": Path("60-relative-cohomology-boundary-contract.md"),
    "61_boundary_theorem_doc": Path("61-bound-domain-boundary-theorem-attempt.md"),
    "69_memory_gate_doc": Path("69-minimal-memory-gate-variation-attempt.md"),
    "70_Ccoh_boundary_audit_doc": Path("70-Ccoh-variation-and-boundary-current-audit.md"),
    "70_status": Path("runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/status.json"),
    "70_boundary_candidates": Path("runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/boundary_current_candidates.csv"),
    "70_gates": Path("runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/gate_results.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def construction_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "object": "relative_pair",
            "definition": "J_rel = (j_3, b_2) in C^3(D,boundary D)",
            "condition": "d_rel(j_3,b_2) = (d j_3, i_star j_3 - d_boundary b_2) = 0",
            "status": "formal_construction",
            "gap": "physical representative not yet action-derived",
        },
        {
            "step": 2,
            "object": "bulk_current",
            "definition": "j_3 is the coherent scalar memory 3-current sourced by C_coh L_mem",
            "condition": "d j_3 = 0 in bulk on memory equations",
            "status": "conditional",
            "gap": "L_mem and Q/u equations still missing",
        },
        {
            "step": 3,
            "object": "boundary_current",
            "definition": "b_2 absorbs the pullback i_star j_3 on boundary(D)",
            "condition": "i_star j_3 = d_boundary b_2",
            "status": "formal_closure",
            "gap": "b_2 must not become arbitrary PPN-tuned surface stress",
        },
        {
            "step": 4,
            "object": "local_trivial_class",
            "definition": "stationary bound domain has j_3 exact or zero and b_2 exact/zero",
            "condition": "[J_rel]=0",
            "status": "pass_conditional",
            "gap": "bound-domain rule remains parent-dependent",
        },
        {
            "step": 5,
            "object": "FLRW_expansion_class",
            "definition": "coherent FLRW domain carries nonzero integral of j_3 proportional to I_M=det(Q_coh)",
            "condition": "integral_D j_3 nonzero with d ln V_D/dtau=3H",
            "status": "pass_contract",
            "gap": "normalization p=3,u3=1/4,b_mem still not selected",
        },
        {
            "step": 6,
            "object": "exchange_current",
            "definition": "local-to-FLRW exchange is boundary bookkeeping in b_2 rather than propagating bulk stress",
            "condition": "closed relative pair conserves total current",
            "status": "best_route_not_derived",
            "gap": "needs parent action/topological term to force this pair",
        },
    ]


def closure_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "quiet_local_bulk",
            "j_3": "0",
            "b_2": "0",
            "relative_class": "trivial",
            "stress_risk": "none in bulk",
            "status": "pass_conditional",
            "gap": "local quiet solution must be derived",
        },
        {
            "arena": "stationary_bound_boundary",
            "j_3": "zero or exact volume-memory current",
            "b_2": "exact or zero boundary primitive",
            "relative_class": "trivial if bound-domain rule holds",
            "stress_risk": "no PPN surface stress if topological/exact",
            "status": "pass_conditional",
            "gap": "bound boundary theorem remains conditional",
        },
        {
            "arena": "FLRW_background",
            "j_3": "nonzero coherent expansion current",
            "b_2": "compatible boundary primitive or closed comoving class",
            "relative_class": "nontrivial expansion class",
            "stress_risk": "none in homogeneous bulk if topological",
            "status": "pass_contract",
            "gap": "amplitude and perturbations missing",
        },
        {
            "arena": "local_to_FLRW_transition",
            "j_3": "changes from trivial to nontrivial representative",
            "b_2": "required exchange primitive",
            "relative_class": "relative class jump/transition",
            "stress_risk": "main danger if b_2 is physical surface stress",
            "status": "open",
            "gap": "must be topological or conserved boundary bookkeeping",
        },
        {
            "arena": "FLRW_perturbations",
            "j_3": "background plus perturbative current",
            "b_2": "unknown",
            "relative_class": "mixed/unknown",
            "stress_risk": "lensing/growth conservation risk",
            "status": "open",
            "gap": "perturbation current construction missing",
        },
        {
            "arena": "collapse_merger",
            "j_3": "dynamic nonzero possible",
            "b_2": "dynamic boundary primitive",
            "relative_class": "not forced trivial",
            "stress_risk": "strong-field/radiative",
            "status": "open",
            "gap": "not a local PPN baseline",
        },
    ]


def stress_safety_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "metric_independent_topological_pair",
            "stress_behavior": "no local bulk stress from J_rel itself",
            "local_safety": "best",
            "FLRW_behavior": "can carry global class",
            "status": "preferred_if_constructed",
            "risk": "must still couple to memory amplitude without breaking conservation",
        },
        {
            "route": "boundary_surface_stress",
            "stress_behavior": "physical surface energy on boundary",
            "local_safety": "dangerous",
            "FLRW_behavior": "could carry exchange but likely observable",
            "status": "rejected_for_local_GR_unless_bounded",
            "risk": "PPN-sized wall/source",
        },
        {
            "route": "exact_local_boundary_term",
            "stress_behavior": "exact form integrates away on stationary local boundaries",
            "local_safety": "conditional",
            "FLRW_behavior": "allows nontrivial global class",
            "status": "live",
            "risk": "exactness must be parent-derived",
        },
        {
            "route": "arbitrary_boundary_counterterm",
            "stress_behavior": "chosen to cancel bad terms",
            "local_safety": "fake",
            "FLRW_behavior": "tunable",
            "status": "rejected",
            "risk": "renamed rescue knob",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "relative_pair_written",
            "status": "pass",
            "detail": "J_rel=(j_3,b_2) with d_rel J_rel=0 gives a formal conserved relative current",
        },
        {
            "gate": "local_trivial_class_possible",
            "status": "pass_conditional",
            "detail": "stationary bound domains can be trivial if j_3/b_2 are exact or zero",
        },
        {
            "gate": "FLRW_nontrivial_class_possible",
            "status": "pass_contract",
            "detail": "coherent FLRW expansion can carry nonzero relative class",
        },
        {
            "gate": "PPN_surface_stress_avoided",
            "status": "pass_conditional",
            "detail": "avoided only if J_rel is topological/exact bookkeeping, not physical wall stress",
        },
        {
            "gate": "parent_action_derives_Jrel",
            "status": "fail",
            "detail": "no action/topological term yet forces the relative pair",
        },
        {
            "gate": "amplitude_normalization_derived",
            "status": "fail",
            "detail": "p=3,u3=1/4,b_mem remain outside this construction",
        },
        {
            "gate": "perturbation_current_resolved",
            "status": "open",
            "detail": "FLRW perturbation/lensing current is not constructed",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "formal relative current is not a full GR reduction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "construction is a consistency route, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "relative_boundary_current_status",
            "status": "formal_current_constructed_not_parent_derived",
            "evidence": "closed relative pair can encode trivial local and nontrivial FLRW classes, but no parent action forces it",
            "next_action": "attempt topological/action owner for J_rel",
        },
        {
            "decision": "local_GR_route_status",
            "status": "boundary_current_formal_but_unpromoted",
            "evidence": "PPN danger is avoided only if the current is topological/exact, not physical surface stress",
            "next_action": "derive or reject metric-independent topological coupling",
        },
        {
            "decision": "recommended_next_target",
            "status": "72-relative-current-action-owner-attempt.md",
            "evidence": "the next bottleneck is an action/topological term whose variation gives d_rel J_rel=0",
            "next_action": "vary a BF/relative-pair owner and test whether it imposes or derives J_rel",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "formal_current_constructed_not_parent_derived",
        "key_metrics": {
            "construction_steps": counts["construction_chain"],
            "closure_tests": counts["closure_tests"],
            "stress_routes": counts["stress_safety_ledger"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "72-relative-current-action-owner-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-relative-boundary-current-construction-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "construction_chain": (
            construction_chain_rows(),
            ["step", "object", "definition", "condition", "status", "gap"],
        ),
        "closure_tests": (
            closure_test_rows(),
            ["arena", "j_3", "b_2", "relative_class", "stress_risk", "status", "gap"],
        ),
        "stress_safety_ledger": (
            stress_safety_rows(),
            ["route", "stress_behavior", "local_safety", "FLRW_behavior", "status", "risk"],
        ),
        "gate_results": (
            gate_rows(),
            ["gate", "status", "detail"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
