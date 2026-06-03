#!/usr/bin/env python3
"""Decide the next route after the post-checkpoint local branch summary."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_17_STATUS = Path("runs/20260530-232735-post-checkpoint-promotion-gate-summary/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def strategic_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "A_new_constrained_parent_action",
            "description": "try to build a parent action with R_AB=0/no-Q_R as a first-class or multiplier constraint",
            "upside": "only route that could eventually turn closure into derived local GR",
            "risk": "highest mathematical risk; may become formal closure with no deeper origin",
            "score_foundational_value": 5,
            "score_empirical_nearness": 2,
            "score_overclaim_safety": 4,
            "recommendation": "do_next_as_skeleton_contract_not_full_claim",
        },
        {
            "option": "B_empirical_pillars_now",
            "description": "return to cosmology/galaxy/clock/EM tests using the new gate discipline",
            "upside": "fastest route to data pressure and useful failures",
            "risk": "can become phenomenology without field-theory derivation",
            "score_foundational_value": 3,
            "score_empirical_nearness": 5,
            "score_overclaim_safety": 4,
            "recommendation": "run_in_parallel_after_parent_skeleton",
        },
        {
            "option": "C_promote_sandbox_to_main_now",
            "description": "copy closure benchmark and ledgers into the main workbench immediately",
            "upside": "integrates useful discipline",
            "risk": "premature promotion may blur closure vs derivation",
            "score_foundational_value": 2,
            "score_empirical_nearness": 2,
            "score_overclaim_safety": 1,
            "recommendation": "do_not_do_yet",
        },
        {
            "option": "D_continue_local_derivation_grind",
            "description": "keep searching within the same Hamiltonian/current/gauge routes for R_AB=0",
            "upside": "could find missed trick",
            "risk": "already tested major routes; likely token sink and circularity risk",
            "score_foundational_value": 2,
            "score_empirical_nearness": 1,
            "score_overclaim_safety": 3,
            "recommendation": "stop_as_default",
        },
        {
            "option": "E_two_track_with_order",
            "description": "first write parent-action skeleton, then resume empirical pillars with explicit closure labels",
            "upside": "keeps unified-field ambition while preserving test pressure",
            "risk": "requires strict file separation and claim labels",
            "score_foundational_value": 5,
            "score_empirical_nearness": 4,
            "score_overclaim_safety": 5,
            "recommendation": "best_default",
        },
    ]


def next_track_rows() -> list[dict[str, Any]]:
    return [
        {
            "track": "parent_action_skeleton",
            "priority": 1,
            "next_file": "19-constrained-parent-action-skeleton.md",
            "purpose": "write the minimal covariant/constrained action contract that could produce R_AB=0 without GR import",
            "acceptance_gate": "must label every constraint as derived, postulated, or closure",
        },
        {
            "track": "empirical_pillar_queue",
            "priority": 2,
            "next_file": "20-empirical-pillar-test-queue.md",
            "purpose": "rank cosmology, galaxy, clock/local, EM, and orbital tests by readiness and risk",
            "acceptance_gate": "must separate closure benchmark tests from novel MTS predictions",
        },
        {
            "track": "promotion_patch",
            "priority": 3,
            "next_file": "deferred_main_workbench_patch_plan.md",
            "purpose": "plan eventual main-workbench updates without editing the main workbench yet",
            "acceptance_gate": "requires user approval or explicit promotion instruction",
        },
        {
            "track": "raw_local_likelihoods",
            "priority": 4,
            "next_file": "deferred_local_raw_likelihood_plan.md",
            "purpose": "only build raw Cassini/INPOP/Galileo/MICROSCOPE likelihoods if a branch predicts nonzero deviations",
            "acceptance_gate": "needs data/covariance availability and no double-counting",
        },
    ]


def parent_action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "fields",
            "minimum_requirement": "define metric/coframe, load scalar or capacity variable, reciprocal strain R_AB, matter fields",
            "must_not": "hide GR equations as definitions",
            "status": "next_skeleton_needed",
        },
        {
            "component": "constraint_sector",
            "minimum_requirement": "explain whether R_AB=0 is first-class, multiplier-imposed, or emergent",
            "must_not": "call multiplier closure a derivation",
            "status": "critical",
        },
        {
            "component": "source_matching",
            "minimum_requirement": "prove Q_R=0/Pi_R=0 for compact sources or remove R_AB kinetic hair",
            "must_not": "assume source neutrality",
            "status": "critical",
        },
        {
            "component": "local_limit",
            "minimum_requirement": "recover Newtonian limit, gamma=1, beta=1, universal matter coupling",
            "must_not": "fit p=1 from observations",
            "status": "critical",
        },
        {
            "component": "cosmology_bridge",
            "minimum_requirement": "state how the same action produces FLRW/cosmology variables without conflicting with local closure",
            "must_not": "use unrelated phenomenological knobs",
            "status": "high",
        },
        {
            "component": "test_hooks",
            "minimum_requirement": "identify q_R, delta_beta, alpha_clock, epsilon_matter, cosmology amplitudes as outputs or closure parameters",
            "must_not": "mix derived parameters with fitted closures",
            "status": "high",
        },
    ]


def empirical_pillar_rows() -> list[dict[str, Any]]:
    return [
        {
            "pillar": "local_PPN_clocks",
            "readiness": "ready_as_screening",
            "current_artifact": "16-local-bounds-gate-runner.md",
            "next_use": "pre-screen any local branch",
            "claim_limit": "screening only, not raw data fit",
        },
        {
            "pillar": "cosmology",
            "readiness": "ready_for_robustness_return",
            "current_artifact": "formalization-workbench cosmology smoke/robustness files",
            "next_use": "test whether C0/M branches survive with priors/splits",
            "claim_limit": "must not claim edge-hitting models",
        },
        {
            "pillar": "galaxies",
            "readiness": "separate_repo_thread",
            "current_artifact": "galaxy work explicitly not mixed into this sandbox",
            "next_use": "treat as empirical pillar only",
            "claim_limit": "not a unified field proof by itself",
        },
        {
            "pillar": "EM_time",
            "readiness": "needs_variable_audit",
            "current_artifact": "attachments and earlier corpus audit",
            "next_use": "map to parent action matter/coupling sector",
            "claim_limit": "avoid speculative hardware/processor overclaim",
        },
        {
            "pillar": "orbital_systems",
            "readiness": "partly_ready",
            "current_artifact": "local PPN sensitivity budget",
            "next_use": "use after parent branch predicts nonzero orbital deviations",
            "claim_limit": "published-bound screening before raw fit",
        },
    ]


def decision_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_17_complete",
            "status": "pass" if source.get("readout") == "post_checkpoint_promotion_summary_ready_no_main_mutation" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "derived_local_GR_available",
            "status": "fail",
            "detail": "source 17 explicitly says derived local GR is not promotable",
        },
        {
            "gate": "parent_action_needed",
            "status": "pass",
            "detail": "critical obligations require a parent action or permanent closure label",
        },
        {
            "gate": "empirical_tests_ready",
            "status": "conditional_pass",
            "detail": "local screening ready; cosmology/galaxies need their own robustness discipline",
        },
        {
            "gate": "main_workbench_edit_allowed",
            "status": "fail",
            "detail": "no direct main mutation in this stage",
        },
        {
            "gate": "best_default_selected",
            "status": "pass",
            "detail": "two-track ordered route selected: parent skeleton first, empirical queue second",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "next_default",
            "status": "two_track_parent_first",
            "evidence": "field-theory ambition needs parent action; empirical pressure remains necessary but must not replace derivation",
            "next_action": "create 19-constrained-parent-action-skeleton.md",
        },
        {
            "decision": "local_branch_status",
            "status": "closure_control_lane",
            "evidence": "local route passed only as closure benchmark and screening harness",
            "next_action": "use only as constraint on future parent action",
        },
        {
            "decision": "main_workbench_status",
            "status": "do_not_mutate_yet",
            "evidence": "post-checkpoint package is prepared but not explicitly promoted",
            "next_action": "keep work in post-checkpoint folder",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Parent-action or empirical-pillar decision.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_17_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-parent-action-or-empirical-pillar-decision"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    options = strategic_option_rows()
    tracks = next_track_rows()
    parent_contract = parent_action_contract_rows()
    pillars = empirical_pillar_rows()
    gates = decision_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "strategic_options.csv", options, list(options[0].keys()))
    write_csv(results_dir / "ordered_next_tracks.csv", tracks, list(tracks[0].keys()))
    write_csv(results_dir / "parent_action_contract_requirements.csv", parent_contract, list(parent_contract[0].keys()))
    write_csv(results_dir / "empirical_pillar_readiness.csv", pillars, list(pillars[0].keys()))
    write_csv(results_dir / "path_decision_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "path_decision.csv", decisions, list(decisions[0].keys()))

    readout = "parent_action_or_empirical_decision_two_track_parent_first"
    status = {
        "status": "complete_parent_action_or_empirical_pillar_decision",
        "readout": readout,
        "recommendation": "write_constrained_parent_action_skeleton_next; then_empirical_pillar_queue",
        "next_target": "19-constrained-parent-action-skeleton.md",
        "selected_strategy": "two_track_parent_first",
        "main_workbench_mutation_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "local_branch_role": "closure_control_lane_and_screening_harness",
        "outputs": {
            "strategic_options": str(results_dir / "strategic_options.csv"),
            "ordered_next_tracks": str(results_dir / "ordered_next_tracks.csv"),
            "parent_action_contract_requirements": str(results_dir / "parent_action_contract_requirements.csv"),
            "empirical_pillar_readiness": str(results_dir / "empirical_pillar_readiness.csv"),
            "path_decision_gates": str(results_dir / "path_decision_gates.csv"),
            "path_decision": str(results_dir / "path_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
