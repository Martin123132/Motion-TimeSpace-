#!/usr/bin/env python3
"""Summarize post-checkpoint promotion, parking, and rejection decisions."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_16_STATUS = Path("runs/20260530-232506-local-bounds-gate-runner/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def stage_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": "00_pre_pivot_checkpoint",
            "main_result": "main workbench protected before route change",
            "decision": "keep",
            "promotion_class": "sandbox_governance",
        },
        {
            "stage": "01_motion_load_route_contract",
            "main_result": "motion/load route defined with explicit promotion gates",
            "decision": "keep",
            "promotion_class": "route_contract",
        },
        {
            "stage": "02_local_GR_reduction",
            "main_result": "T^2=1-L plus T^2S=1 recovers local GR numbers",
            "decision": "promote_only_as_closure_benchmark",
            "promotion_class": "benchmark",
        },
        {
            "stage": "03_reciprocal_routing_origin",
            "main_result": "p=1 follows from reciprocity but reciprocity not parent-derived",
            "decision": "park_as_open_derivation",
            "promotion_class": "open_obligation",
        },
        {
            "stage": "04_vacuum_reciprocity_contract",
            "main_result": "exact action contract for R_AB=0 written",
            "decision": "promote_as_obligation",
            "promotion_class": "proof_contract",
        },
        {
            "stage": "05_reciprocity_theorem_attempt",
            "main_result": "kinetic R_AB leaves Q_R/r hair",
            "decision": "reject_as_parent_route",
            "promotion_class": "negative_result",
        },
        {
            "stage": "06_source_neutrality",
            "main_result": "Q_R=0 requires source neutrality theorem not yet available",
            "decision": "park_as_open_derivation",
            "promotion_class": "open_obligation",
        },
        {
            "stage": "07_nonpropagating_constraint",
            "main_result": "lambda_R R_AB cleanly enforces GR lane without hair",
            "decision": "promote_only_as_closure_benchmark",
            "promotion_class": "closure_mechanism",
        },
        {
            "stage": "08_phase_volume_origin",
            "main_result": "radial t-r cell selects p=1 but generic volume fails",
            "decision": "promote_as_motivating_but_not_proof",
            "promotion_class": "conditional_motivation",
        },
        {
            "stage": "09_hamiltonian_radial_cell",
            "main_result": "Hamiltonian/Liouville structure does not derive the separate cell",
            "decision": "promote_as_negative_result",
            "promotion_class": "negative_result",
        },
        {
            "stage": "10_observer_map_contract",
            "main_result": "observer-map contract states exact no-smuggling requirements",
            "decision": "promote_as_obligation",
            "promotion_class": "proof_contract",
        },
        {
            "stage": "11_cell_current_origin",
            "main_result": "ordinary conserved current gives Q_R, not Q_R=0",
            "decision": "reject_as_parent_route",
            "promotion_class": "negative_result",
        },
        {
            "stage": "12_gauge_noether_origin",
            "main_result": "coordinate gauge and Noether identity do not derive R_AB=0",
            "decision": "reject_current_scaffold_as_derivation",
            "promotion_class": "negative_result",
        },
        {
            "stage": "13_local_closure_PPN",
            "main_result": "closure reproduces GR local control values",
            "decision": "promote_only_as_control_baseline",
            "promotion_class": "benchmark",
        },
        {
            "stage": "14_deviation_sensitivity",
            "main_result": "q_R, delta_beta, alpha_clock, epsilon_matter leakage channels quantified",
            "decision": "promote_as_test_budget",
            "promotion_class": "test_budget",
        },
        {
            "stage": "15_observables_data_map",
            "main_result": "published local bounds mapped to MTS leak parameters",
            "decision": "promote_as_screening_map",
            "promotion_class": "empirical_screening",
        },
        {
            "stage": "16_bounds_gate_runner",
            "main_result": "candidate branches pass/fail screened against published-bound gates",
            "decision": "promote_as_screening_tool",
            "promotion_class": "empirical_screening",
        },
    ]


def promotion_package_rows() -> list[dict[str, Any]]:
    return [
        {
            "package_item": "local_closure_control_baseline",
            "content": "Assume R_AB=0, Q_R=0, T^2=1-L, S=1/T^2",
            "allowed_claim": "reproduces GR-like local exterior as a benchmark",
            "forbidden_claim": "derives GR from motion-load alone",
            "destination": "main workbench benchmark appendix only",
        },
        {
            "package_item": "proof_obligation_R_AB_zero",
            "content": "Future parent action must derive ln(T^2S)=0 without GR import",
            "allowed_claim": "core local-GR derivation target is now exact",
            "forbidden_claim": "the target is already proven",
            "destination": "main proof-obligation queue",
        },
        {
            "package_item": "proof_obligation_no_QR_hair",
            "content": "Kinetic/current routes must prove Q_R=0 or be rejected",
            "allowed_claim": "nonzero reciprocal charge is a local-screening failure",
            "forbidden_claim": "finite Q_R is harmless by asymptotic flatness",
            "destination": "main proof-obligation queue",
        },
        {
            "package_item": "negative_route_register",
            "content": "generic volume, Liouville, coordinate gauge, Noether identity, and ordinary current conservation fail",
            "allowed_claim": "these routes are audited and should not be reused casually",
            "forbidden_claim": "volume/symplectic conservation alone derives p=1",
            "destination": "red-team ledger",
        },
        {
            "package_item": "local_screening_harness",
            "content": "q_R, delta_beta, alpha_clock, epsilon_matter, Q_R pass/fail gates",
            "allowed_claim": "candidate branches can be screened before empirical work",
            "forbidden_claim": "published-bound screening is a raw-data fit",
            "destination": "test workflow",
        },
    ]


def unresolved_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "parent_action_for_R_AB_zero",
            "why_required": "local GR reduction requires reciprocity as theorem, not closure",
            "current_status": "open",
            "severity": "critical",
            "next_possible_action": "construct constrained parent action or demote permanently to closure",
        },
        {
            "obligation": "no_reciprocal_charge_theorem",
            "why_required": "Q_R/r hair violates local screening unless exactly zero",
            "current_status": "open",
            "severity": "critical",
            "next_possible_action": "derive source neutrality or keep nonpropagating constraint only",
        },
        {
            "obligation": "beta_completion_without_GR_import",
            "why_required": "gamma lane is insufficient for full local GR/PPN reduction",
            "current_status": "conditional",
            "severity": "high",
            "next_possible_action": "formal PPN coordinate expansion under closure",
        },
        {
            "obligation": "universal_matter_coupling",
            "why_required": "epsilon_matter is constrained at MICROSCOPE scale",
            "current_status": "assumed_in_benchmark",
            "severity": "high",
            "next_possible_action": "define matter action on common coframe",
        },
        {
            "obligation": "raw_likelihood_local_data",
            "why_required": "published-bound screening cannot support empirical claims",
            "current_status": "not_started",
            "severity": "medium",
            "next_possible_action": "only after parent branch predicts nonzero deviations",
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "generic_volume_preservation",
            "reason": "selects wrong exponents such as p=1/3 or p=1/2",
            "status": "rejected",
        },
        {
            "route": "ordinary_Liouville_preservation",
            "reason": "full phase cell preservation is automatic for all p",
            "status": "rejected",
        },
        {
            "route": "kinetic_R_AB_parent",
            "reason": "permits exterior Q_R/r reciprocal hair",
            "status": "rejected_as_local_GR_parent",
        },
        {
            "route": "ordinary_cell_current",
            "reason": "conservation gives constant Q_R, not Q_R=0",
            "status": "rejected_as_derivation",
        },
        {
            "route": "radial_coordinate_gauge_AB1",
            "reason": "areal radius fixes radial coordinate; AB=1 would import GR",
            "status": "forbidden",
        },
        {
            "route": "Noether_identity_alone",
            "reason": "identity relates equations but does not impose R_AB=0",
            "status": "insufficient",
        },
        {
            "route": "perihelion_cancellation_hiding",
            "reason": "combined perihelion residual can hide individual q_R or beta failures",
            "status": "blocked_by_gate_runner",
        },
    ]


def promotion_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_16_complete",
            "status": "pass" if source.get("readout") == "local_bounds_gate_runner_operational_screening_not_fit" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "closure_benchmark_promotable",
            "status": "conditional_pass",
            "detail": "promotable only as an explicitly assumed control baseline",
        },
        {
            "gate": "derived_local_GR_promotable",
            "status": "fail",
            "detail": "R_AB=0, Q_R=0, beta completion, and matter coupling are not parent-derived",
        },
        {
            "gate": "negative_results_promotable",
            "status": "pass",
            "detail": "failed derivation routes are valuable red-team evidence",
        },
        {
            "gate": "screening_harness_promotable",
            "status": "pass",
            "detail": "published-bound gate runner can be reused as a local pre-screen",
        },
        {
            "gate": "main_workbench_mutation_allowed_now",
            "status": "fail",
            "detail": "this summary prepares a promotion package but does not itself edit the main workbench",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "post_checkpoint_branch_status",
            "status": "useful_but_not_derived_local_GR",
            "evidence": "closure reproduces local GR controls but parent derivation failed through multiple routes",
            "next_action": "prepare a separate promotion patch only if user wants main workbench updates",
        },
        {
            "decision": "promotion_allowed_now",
            "status": "no_direct_main_mutation",
            "evidence": "sandbox rule says no main changes until explicit promotion gate",
            "next_action": "keep current output as post-checkpoint summary",
        },
        {
            "decision": "scientific_value",
            "status": "high_as_discipline_tool",
            "evidence": "it prevents overclaiming and gives exact local screening tests",
            "next_action": "move next to parent-action or cosmology/galaxy empirical pillars",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Post-checkpoint promotion gate summary.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_16_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-post-checkpoint-promotion-gate-summary"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    stages = stage_summary_rows()
    packages = promotion_package_rows()
    obligations = unresolved_obligation_rows()
    rejections = rejection_rows()
    gates = promotion_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "post_checkpoint_stage_summary.csv", stages, list(stages[0].keys()))
    write_csv(results_dir / "promotion_package_items.csv", packages, list(packages[0].keys()))
    write_csv(results_dir / "unresolved_promotion_obligations.csv", obligations, list(obligations[0].keys()))
    write_csv(results_dir / "rejected_local_derivation_routes.csv", rejections, list(rejections[0].keys()))
    write_csv(results_dir / "promotion_gate_summary_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "promotion_gate_summary_decision.csv", decisions, list(decisions[0].keys()))

    readout = "post_checkpoint_promotion_summary_ready_no_main_mutation"
    status = {
        "status": "complete_post_checkpoint_promotion_gate_summary",
        "readout": readout,
        "recommendation": "do_not_promote_as_derived_GR; optionally_promote_as_closure_benchmark_and_obligation_set",
        "next_target": "18-parent-action-or-empirical-pillar-decision.md",
        "derived_local_GR_promotable": False,
        "closure_benchmark_promotable_with_label": True,
        "negative_results_promotable": True,
        "screening_harness_promotable": True,
        "main_workbench_mutation_allowed_now": False,
        "critical_open_obligations": [
            "parent_action_for_R_AB_zero",
            "no_reciprocal_charge_theorem",
            "beta_completion_without_GR_import",
            "universal_matter_coupling",
        ],
        "outputs": {
            "post_checkpoint_stage_summary": str(results_dir / "post_checkpoint_stage_summary.csv"),
            "promotion_package_items": str(results_dir / "promotion_package_items.csv"),
            "unresolved_promotion_obligations": str(results_dir / "unresolved_promotion_obligations.csv"),
            "rejected_local_derivation_routes": str(results_dir / "rejected_local_derivation_routes.csv"),
            "promotion_gate_summary_gates": str(results_dir / "promotion_gate_summary_gates.csv"),
            "promotion_gate_summary_decision": str(results_dir / "promotion_gate_summary_decision.csv"),
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
