#!/usr/bin/env python3
"""Attempt an action/topological owner for the relative boundary current J_rel."""

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
    "71_relative_current_doc": Path("71-relative-boundary-current-construction-attempt.md"),
    "71_status": Path("runs/20260531-113439-relative-boundary-current-construction-attempt/status.json"),
    "71_construction_chain": Path("runs/20260531-113439-relative-boundary-current-construction-attempt/results/construction_chain.csv"),
    "71_stress_safety": Path("runs/20260531-113439-relative-boundary-current-construction-attempt/results/stress_safety_ledger.csv"),
    "71_gates": Path("runs/20260531-113439-relative-boundary-current-construction-attempt/results/gate_results.csv"),
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


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "relative_BF_multiplier",
            "schematic_action": "S_rel = integral_D B_0 d j_3 + integral_boundaryD beta_1 (i_star j_3 - d_boundary b_2)",
            "variation_result": "imposes d_rel J_rel=0",
            "local_FLRW_selection": "none by itself",
            "status": "closure_enforcer_not_selector",
            "risk": "restates the desired closure as a multiplier constraint",
        },
        {
            "candidate": "BF_plus_boundary_polarization",
            "schematic_action": "S = integral B wedge F[A] + integral_boundaryD Pi(C_coh) wedge b_2",
            "variation_result": "flat bulk plus boundary class weighted by coherent expansion",
            "local_FLRW_selection": "local C_coh=0 suppresses boundary polarization; FLRW C_coh=1 allows class",
            "status": "best_live_route",
            "risk": "Pi(C_coh) and normalization are not parent-derived",
        },
        {
            "candidate": "relative_Chern_Simons_boundary",
            "schematic_action": "S_boundary = k integral_boundaryD b_2 wedge d b_2 plus coupling to pullback memory current",
            "variation_result": "boundary current conservation/topological response",
            "local_FLRW_selection": "could carry nontrivial expansion boundary class",
            "status": "deferred",
            "risk": "dimension/degree matching and physical variables unclear",
        },
        {
            "candidate": "metric_surface_stress_action",
            "schematic_action": "S_wall = integral_boundaryD sqrt(|gamma|) sigma_wall(C_coh)",
            "variation_result": "physical surface stress",
            "local_FLRW_selection": "can be tuned",
            "status": "rejected",
            "risk": "PPN-sized wall stress and phenomenological tuning",
        },
    ]


def variation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "action_piece": "S_closure = <Lambda_rel, d_rel J_rel>",
            "variation": "delta_Lambda_rel -> d_rel J_rel=0",
            "readout": "closure is imposed",
            "status": "works_but_weak",
            "gap": "does not select physical representative",
        },
        {
            "step": 2,
            "action_piece": "delta_J S_closure",
            "variation": "d_rel^dagger Lambda_rel = 0",
            "readout": "multiplier is closed/co-closed depending on pairing",
            "status": "formal",
            "gap": "no local-zero/FLRW-nonzero selection",
        },
        {
            "step": 3,
            "action_piece": "S_pol = <Pi(C_coh), J_rel>",
            "variation": "source/polarization biases relative class by coherent expansion",
            "readout": "possible selector if Pi(0)=0 and Pi(1) nonzero",
            "status": "best_live_route",
            "gap": "Pi is a new function unless derived",
        },
        {
            "step": 4,
            "action_piece": "local branch C_coh=0",
            "variation": "Pi(0)=0 -> no boundary polarization",
            "readout": "trivial local class possible",
            "status": "pass_conditional",
            "gap": "bound-domain rule still required",
        },
        {
            "step": 5,
            "action_piece": "FLRW branch C_coh=1",
            "variation": "Pi(1) selects allowed expansion class",
            "readout": "nontrivial FLRW class possible",
            "status": "pass_contract",
            "gap": "amplitude p/u3/b_mem not selected",
        },
        {
            "step": 6,
            "action_piece": "metric variation",
            "variation": "topological pieces safe only if metric-independent; Pi(C_coh) reintroduces delta C_coh",
            "readout": "boundary current problem moves into polarization variation",
            "status": "open_warning",
            "gap": "Bianchi completion not solved",
        },
    ]


def selection_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "does_action_close_Jrel",
            "result": "yes if multiplier/BF closure term is allowed",
            "status": "pass_formal",
            "problem": "closure alone is not physical selection",
        },
        {
            "test": "does_action_select_local_zero",
            "result": "only if C_coh polarization vanishes or bound-domain class is trivial",
            "status": "pass_conditional",
            "problem": "still depends on C_coh/domain theorem",
        },
        {
            "test": "does_action_select_FLRW_nonzero",
            "result": "only if Pi(1) or boundary condition selects expansion class",
            "status": "pass_contract",
            "problem": "normalization not derived",
        },
        {
            "test": "does_action_avoid_PPN_wall",
            "result": "yes for metric-independent topological term; no for physical wall action",
            "status": "pass_conditional",
            "problem": "Pi(C_coh) variation can reintroduce stress",
        },
        {
            "test": "does_action_derive_p3_u3_bmem",
            "result": "no",
            "status": "fail",
            "problem": "branch amplitude/normalization still outside owner",
        },
        {
            "test": "does_action_complete_Bianchi",
            "result": "not yet",
            "status": "fail",
            "problem": "delta C_coh and memory stress still unresolved",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "action_owner_attempted",
            "status": "pass",
            "detail": "relative BF/multiplier and boundary-polarization candidates were tested",
        },
        {
            "gate": "drel_closure_obtained",
            "status": "pass_formal",
            "detail": "multiplier action can impose d_rel J_rel=0",
        },
        {
            "gate": "physical_representative_selected",
            "status": "fail",
            "detail": "closure action alone does not select local-zero/FLRW-nonzero representative",
        },
        {
            "gate": "local_zero_possible",
            "status": "pass_conditional",
            "detail": "requires Pi(0)=0 plus bound-domain rule",
        },
        {
            "gate": "FLRW_nonzero_possible",
            "status": "pass_contract",
            "detail": "requires Pi(1) or boundary condition selecting expansion class",
        },
        {
            "gate": "PPN_wall_stress_avoided",
            "status": "pass_conditional",
            "detail": "only if current owner is metric-independent/topological",
        },
        {
            "gate": "Bianchi_completed",
            "status": "fail",
            "detail": "C_coh polarization reopens delta C_coh exchange terms",
        },
        {
            "gate": "p3_u3_bmem_selected",
            "status": "fail",
            "detail": "relative current owner does not select determinant degree, quarter scale, or amplitude",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "still not a GR reduction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a construction attempt, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "relative_current_action_owner_status",
            "status": "closure_imposable_selection_not_derived",
            "evidence": "action can impose d_rel J_rel=0, but physical local-zero/FLRW-nonzero representative needs C_coh polarization/boundary data not parent-derived",
            "next_action": "demote pure relative-current owner to closure support and return to amplitude/representative selection",
        },
        {
            "decision": "local_GR_route_status",
            "status": "formal_conservation_support_not_derivation",
            "evidence": "topological closure can help bookkeeping, but cannot alone derive local GR reduction",
            "next_action": "audit remaining blockers and decide next highest-value derivation/test",
        },
        {
            "decision": "recommended_next_target",
            "status": "73-local-route-blocker-ledger-and-promotion-gate.md",
            "evidence": "local route has many formal supports but still lacks selection of representative, amplitude, and Bianchi completion",
            "next_action": "compile explicit blocker ledger before digging another sub-branch",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "closure_imposable_selection_not_derived",
        "key_metrics": {
            "action_candidates": counts["action_candidate_ledger"],
            "variation_steps": counts["variation_attempt_chain"],
            "selection_tests": counts["selection_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
            "formal_pass_gates": sum(1 for row in gates if row["status"] == "pass_formal"),
        },
        "decision": decision_rows()[0],
        "next_target": "73-local-route-blocker-ledger-and-promotion-gate.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-relative-current-action-owner-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "action_candidate_ledger": (
            action_candidate_rows(),
            ["candidate", "schematic_action", "variation_result", "local_FLRW_selection", "status", "risk"],
        ),
        "variation_attempt_chain": (
            variation_attempt_rows(),
            ["step", "action_piece", "variation", "readout", "status", "gap"],
        ),
        "selection_tests": (
            selection_test_rows(),
            ["test", "result", "status", "problem"],
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
