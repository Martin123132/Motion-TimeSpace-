#!/usr/bin/env python3
"""Decide whether the local route is demoted or gets a bounded parent u/D owner attempt."""

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
    "74_priority_doc": Path("74-next-derivation-priority-decision.md"),
    "75_Ccoh_contract_doc": Path("75-Ccoh-parent-variation-contract.md"),
    "76_Bianchi_doc": Path("76-Ccoh-Bianchi-identity-attempt.md"),
    "76_status": Path("runs/20260531-114923-Ccoh-Bianchi-identity-attempt/status.json"),
    "76_gates": Path("runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/gate_results.csv"),
    "76_closure_options": Path("runs/20260531-114923-Ccoh-Bianchi-identity-attempt/results/closure_options.csv"),
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


def fork_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "demote_now_to_diagnostic_closure",
            "benefit": "stops spending effort on a route whose Bianchi closure failed",
            "cost": "leaves local GR reduction unresolved and moves away from user's core requirement",
            "failure_clarity": "high",
            "promotion_value": "medium",
            "verdict": "too_early_as_final_move",
        },
        {
            "option": "continue_one_bounded_parent_uD_owner_attempt",
            "benefit": "attacks exact missing E_u/E_D equations that blocked Bianchi closure",
            "cost": "could become another deep tunnel if not bounded",
            "failure_clarity": "high",
            "promotion_value": "high",
            "verdict": "selected",
        },
        {
            "option": "continue_unbounded_local_derivation",
            "benefit": "may improve formal support",
            "cost": "risks topology/scaffolding drift after checkpoint 73 already set blockers",
            "failure_clarity": "low",
            "promotion_value": "low",
            "verdict": "rejected",
        },
        {
            "option": "pivot_to_empirical_tests_now",
            "benefit": "gets data feedback soon",
            "cost": "tests a closure with failed/open conservation interpretation",
            "failure_clarity": "medium",
            "promotion_value": "medium",
            "verdict": "deferred",
        },
        {
            "option": "pivot_to_amplitude_now",
            "benefit": "attacks p=3,u3,b_mem critical blocker",
            "cost": "amplitude derivation is less meaningful if local conservation route fails",
            "failure_clarity": "high",
            "promotion_value": "high",
            "verdict": "second_priority",
        },
    ]


def decision_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "criterion": "attacks_checkpoint_76_failure_directly",
            "demote_now": "medium",
            "bounded_uD_attempt": "high",
            "pivot_amplitude": "low",
            "empirical_now": "low",
            "winner": "bounded_uD_attempt",
        },
        {
            "criterion": "has_clear_failure_mode",
            "demote_now": "high",
            "bounded_uD_attempt": "high",
            "pivot_amplitude": "medium",
            "empirical_now": "medium",
            "winner": "bounded_uD_attempt",
        },
        {
            "criterion": "avoids_endless_scaffolding",
            "demote_now": "high",
            "bounded_uD_attempt": "high_if_strictly_bounded",
            "pivot_amplitude": "medium",
            "empirical_now": "medium",
            "winner": "bounded_uD_attempt_or_demote",
        },
        {
            "criterion": "preserves_derivation_ambition",
            "demote_now": "low",
            "bounded_uD_attempt": "high",
            "pivot_amplitude": "medium",
            "empirical_now": "low",
            "winner": "bounded_uD_attempt",
        },
        {
            "criterion": "keeps_empirical_interpretation_clean",
            "demote_now": "medium",
            "bounded_uD_attempt": "high",
            "pivot_amplitude": "medium",
            "empirical_now": "low_until_conservation_cleaner",
            "winner": "bounded_uD_then_amplitude_or_empirical",
        },
    ]


def demotion_label_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_piece": "Ccoh_gated_memory_action",
            "label_now": "conditional_closure_not_field_theory",
            "reason": "Bianchi closure failed without parent u/D/Q equations",
            "can_promote_if": "parent u/D owner closes boundary and perturbation exchange",
        },
        {
            "route_piece": "local_bulk_silence",
            "label_now": "conditional_support",
            "reason": "constant Ccoh=0 bulk is safe only if local parent solution exists",
            "can_promote_if": "E_D derives stationary bound domains and Q_coh=0",
        },
        {
            "route_piece": "FLRW_background_activity",
            "label_now": "background_contract",
            "reason": "constant Ccoh=1 recovers L_mem but L_mem is not fully derived",
            "can_promote_if": "memory action gives background and perturbation equations",
        },
        {
            "route_piece": "relative_current_support",
            "label_now": "formal_conservation_support",
            "reason": "closure can be imposed but representative not selected",
            "can_promote_if": "parent action selects physical representative and amplitude",
        },
    ]


def bounded_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "u_owner",
            "required_result": "observer congruence u has a parent equation, constraint, or coframe origin",
            "kill_condition": "u is chosen only to make Ccoh work",
        },
        {
            "gate": "D_owner",
            "required_result": "domain/boundary D follows from variational, constraint, or topological rule",
            "kill_condition": "D is a smoothing/window choice",
        },
        {
            "gate": "Noether_exchange",
            "required_result": "E_u and E_D terms can absorb delta Ccoh exchange in S_gate",
            "kill_condition": "boundary or perturbation exchange remains uncontrolled",
        },
        {
            "gate": "local_FLRW_limits",
            "required_result": "same owner gives local quiet bulk and FLRW active background",
            "kill_condition": "owner protects one branch by damaging the other",
        },
        {
            "gate": "no_new_stress",
            "required_result": "u/D owner is constrained/topological or stress-bounded",
            "kill_condition": "new field creates PPN-scale source",
        },
    ]


def kill_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "kill_condition": "u_frame_chosen_by_hand",
            "meaning": "observer congruence is selected only because it makes Ccoh quiet locally",
            "consequence": "demote_to_closure_only",
        },
        {
            "kill_condition": "D_or_averaging_window_chosen_by_hand",
            "meaning": "domain selection is external smoothing rather than a derived or constrained object",
            "consequence": "demote_to_closure_only",
        },
        {
            "kill_condition": "Bianchi_requires_frozen_Ccoh",
            "meaning": "conservation works only by forbidding the metric/domain variation of Ccoh",
            "consequence": "remove_Ccoh_from_action_or_demote",
        },
        {
            "kill_condition": "new_stress_or_scale_unbounded",
            "meaning": "u/D owner adds a local source, fifth-force channel, or free transition scale",
            "consequence": "fail_local_PPN_branch",
        },
        {
            "kill_condition": "quiet_bulk_only_boundary_fails",
            "meaning": "local silence holds only in ideal constant domains while boundary exchange remains open",
            "consequence": "closure_only_not_derived_GR",
        },
    ]


def gate_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "current_local_route_promoted",
            "result": "fail",
            "reason": "checkpoint 76 did not close Bianchi, boundary, or perturbation exchange",
        },
        {
            "gate": "demotion_label_applied",
            "result": "pass",
            "reason": "current Ccoh-gated route is explicitly labelled closure-level",
        },
        {
            "gate": "bounded_uD_attempt_allowed",
            "result": "pass",
            "reason": "one bounded attempt directly targets the missing E_u/E_D owner",
        },
        {
            "gate": "unbounded_subbranching_allowed",
            "result": "fail",
            "reason": "continuing without kill conditions would hide the failure mode",
        },
        {
            "gate": "amplitude_pivot_now",
            "result": "defer",
            "reason": "amplitude remains critical but conservation ownership comes first",
        },
        {
            "gate": "empirical_test_now",
            "result": "defer",
            "reason": "testing now would test a closure, not a promoted local field theory",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "no public claim until local conservation and limits are derived or bounded",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "local_route_gate_status",
            "status": "demoted_current_route_bounded_parent_uD_attempt_allowed",
            "evidence": "current Ccoh-gated local route is not a field theory, but the exact missing owner E_u/E_D is now identifiable and worth one bounded attempt",
            "next_action": "create 78-parent-uD-owner-contract.md",
        },
        {
            "decision": "claim_status",
            "status": "no_local_GR_claim",
            "evidence": "Bianchi closure and boundary/perturbation exchange are not solved",
            "next_action": "keep route private/internal only",
        },
        {
            "decision": "fallback_if_78_fails",
            "status": "demote_to_diagnostic_closure_and_return_to_amplitude_or_empirical_tests",
            "evidence": "if u/D owner cannot be made non-arbitrary, Ccoh cannot remain inside the action",
            "next_action": "move to amplitude normalization or empirical closure testing",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "demoted_current_route_bounded_parent_uD_attempt_allowed",
        "key_metrics": {
            "fork_options": counts["fork_options"],
            "decision_matrix_rows": counts["decision_matrix"],
            "demotion_labels": counts["demotion_labels"],
            "bounded_gates": counts["bounded_attempt_gates"],
            "kill_conditions": counts["kill_conditions"],
            "gate_results": counts["gate_results"],
            "selected_option": "continue_one_bounded_parent_uD_owner_attempt",
        },
        "decision": decision_rows()[0],
        "next_target": "78-parent-uD-owner-contract.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-local-route-demote-or-continue-gate"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "fork_options": (
            fork_option_rows(),
            ["option", "benefit", "cost", "failure_clarity", "promotion_value", "verdict"],
        ),
        "decision_matrix": (
            decision_matrix_rows(),
            ["criterion", "demote_now", "bounded_uD_attempt", "pivot_amplitude", "empirical_now", "winner"],
        ),
        "demotion_labels": (
            demotion_label_rows(),
            ["route_piece", "label_now", "reason", "can_promote_if"],
        ),
        "bounded_attempt_gates": (
            bounded_attempt_rows(),
            ["gate", "required_result", "kill_condition"],
        ),
        "kill_conditions": (
            kill_condition_rows(),
            ["kill_condition", "meaning", "consequence"],
        ),
        "gate_results": (
            gate_result_rows(),
            ["gate", "result", "reason"],
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
