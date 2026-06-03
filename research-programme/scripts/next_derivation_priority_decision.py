#!/usr/bin/env python3
"""Rank the next derivation priority after the local-route blocker ledger."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "73_blocker_doc": Path("73-local-route-blocker-ledger-and-promotion-gate.md"),
    "73_status": Path("runs/20260531-114006-local-route-blocker-ledger-and-promotion-gate/status.json"),
    "73_blockers": Path("runs/20260531-114006-local-route-blocker-ledger-and-promotion-gate/results/blocker_ledger.csv"),
    "73_promotion_gate": Path("runs/20260531-114006-local-route-blocker-ledger-and-promotion-gate/results/promotion_gate.csv"),
    "73_support": Path("runs/20260531-114006-local-route-blocker-ledger-and-promotion-gate/results/support_ledger.csv"),
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


def priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "Ccoh_Bianchi_ownership",
            "promotion_value": 10,
            "failure_clarity": 9,
            "empirical_readiness_gain": 7,
            "risk": "hard variational work; may force demotion of local route",
            "reason": "without Ccoh variation and Bianchi closure, no local GR reduction or perturbation equations are credible",
            "rank": 1,
        },
        {
            "candidate": "amplitude_normalization_p3_u3_bmem",
            "promotion_value": 9,
            "failure_clarity": 8,
            "empirical_readiness_gain": 8,
            "risk": "may reveal quarter branch is closure-only",
            "reason": "p=3,u3=1/4,b_mem control whether cosmology/growth tests are predictive rather than fitted",
            "rank": 2,
        },
        {
            "candidate": "perturbation_lensing_growth_contract",
            "promotion_value": 8,
            "failure_clarity": 7,
            "empirical_readiness_gain": 10,
            "risk": "premature if Bianchi/Ccoh ownership missing",
            "reason": "needed for CMB/growth/lensing tests, but requires conservation structure first",
            "rank": 3,
        },
        {
            "candidate": "empirical_smoke_test_readiness",
            "promotion_value": 6,
            "failure_clarity": 9,
            "empirical_readiness_gain": 10,
            "risk": "tests a closure rather than a field theory if done now",
            "reason": "valuable soon, but local theoretical gates are not closed enough to interpret failures cleanly",
            "rank": 4,
        },
        {
            "candidate": "more_topological_current_subbranches",
            "promotion_value": 3,
            "failure_clarity": 4,
            "empirical_readiness_gain": 2,
            "risk": "elegant scaffolding without resolving critical blockers",
            "reason": "checkpoint 73 says topology is support, not the next decisive blocker",
            "rank": 5,
        },
    ]


def decision_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "attacks_critical_blocker",
            "Ccoh_Bianchi": "yes",
            "amplitude": "yes",
            "perturbations": "major_not_first",
            "empirical": "not_theory_blocker",
            "decision": "Ccoh_Bianchi",
        },
        {
            "gate": "clear_failure_mode",
            "Ccoh_Bianchi": "yes: conservation either closes or local route demotes",
            "amplitude": "yes: constants derive or remain closure",
            "perturbations": "partial",
            "empirical": "yes but interpretation weak",
            "decision": "Ccoh_Bianchi",
        },
        {
            "gate": "prevents_wasted_scaffolding",
            "Ccoh_Bianchi": "yes",
            "amplitude": "yes",
            "perturbations": "partial",
            "empirical": "partial",
            "decision": "Ccoh_Bianchi",
        },
        {
            "gate": "unlocks_next_tests",
            "Ccoh_Bianchi": "unlocks perturbations and local GR",
            "amplitude": "unlocks parameter-free background/growth",
            "perturbations": "unlocks observables",
            "empirical": "unlocks data checks only",
            "decision": "Ccoh_Bianchi",
        },
    ]


def workplan_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "target": "75-Ccoh-parent-variation-contract.md",
            "purpose": "write exact parent-variable contract for theta/sigma/omega/domain averages and Ccoh variation",
            "pass_condition": "all Ccoh dependencies have variational owners or are explicitly demoted",
        },
        {
            "step": 2,
            "target": "76-Ccoh-Bianchi-identity-attempt.md",
            "purpose": "attempt Noether/Bianchi closure for S_gate=Ccoh L_mem with Ccoh variation included",
            "pass_condition": "exchange terms organize into conserved total stress or fail cleanly",
        },
        {
            "step": 3,
            "target": "77-local-route-demote-or-continue-gate.md",
            "purpose": "decide whether local route remains derivation candidate after Ccoh/Bianchi attempt",
            "pass_condition": "route either advances to perturbation/amplitude work or is labeled closure-only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "next_priority",
            "status": "Ccoh_Bianchi_ownership_first",
            "evidence": "highest promotion value and clearest failure mode; without it local GR and perturbations are not credible",
            "next_action": "create 75-Ccoh-parent-variation-contract.md",
        },
        {
            "decision": "defer_amplitude",
            "status": "second_priority",
            "evidence": "p=3,u3,b_mem are critical but less useful if conservation fails first",
            "next_action": "return after Ccoh/Bianchi gate",
        },
        {
            "decision": "defer_empirical",
            "status": "not_now",
            "evidence": "data tests are valuable but would test a closure with unclear conservation",
            "next_action": "prepare only after theory gate produces equations",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "next_priority_Ccoh_Bianchi_ownership_first",
        "key_metrics": {
            "ranked_candidates": counts["priority_ranking"],
            "decision_gates": counts["decision_gates"],
            "planned_steps": counts["workplan"],
            "selected_rank": 1,
        },
        "decision": decision_rows()[0],
        "next_target": "75-Ccoh-parent-variation-contract.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-next-derivation-priority-decision"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "priority_ranking": (
            priority_rows(),
            ["candidate", "promotion_value", "failure_clarity", "empirical_readiness_gain", "risk", "reason", "rank"],
        ),
        "decision_gates": (
            decision_gate_rows(),
            ["gate", "Ccoh_Bianchi", "amplitude", "perturbations", "empirical", "decision"],
        ),
        "workplan": (
            workplan_rows(),
            ["step", "target", "purpose", "pass_condition"],
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
