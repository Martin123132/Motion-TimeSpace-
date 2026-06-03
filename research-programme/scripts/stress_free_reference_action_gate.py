#!/usr/bin/env python3
"""Gate whether a stress-free reference action can own u and D."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "77_local_route_gate": Path("77-local-route-demote-or-continue-gate.md"),
    "78_parent_uD_owner_contract": Path("78-parent-uD-owner-contract.md"),
    "79_auxiliary_clock_cell_variation": Path("79-auxiliary-clock-cell-variation-attempt.md"),
    "79_decision": Path("runs/20260531-120154-auxiliary-clock-cell-variation-attempt/results/decision.csv"),
    "79_stress_channels": Path("runs/20260531-120154-auxiliary-clock-cell-variation-attempt/results/stress_channels.csv"),
    "79_limit_gates": Path("runs/20260531-120154-auxiliary-clock-cell-variation-attempt/results/limit_gates.csv"),
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
            "candidate": "physical_reference_dust",
            "action_form": "S_ref = -int sqrt(-g) rho(n)",
            "owns_u": "yes",
            "owns_D": "yes",
            "stress_status": "nonzero_dust_stress",
            "verdict": "reject",
        },
        {
            "candidate": "khronon_or_aether_clock",
            "action_form": "S_ref = int sqrt(-g) F(nabla u, u^2)",
            "owns_u": "yes",
            "owns_D": "no",
            "stress_status": "propagating_preferred_frame_stress",
            "verdict": "reject_for_clean_local_GR",
        },
        {
            "candidate": "Lagrange_multiplier_unit_and_advection_constraints",
            "action_form": "S_ref = int sqrt(-g)[lambda_u(u^2+1)+lambda_chi u.nabla chi_D]",
            "owns_u": "partial",
            "owns_D": "partial",
            "stress_status": "multiplier_stress_generically_nonzero",
            "verdict": "reject_unless_multipliers_vanish_on_shell",
        },
        {
            "candidate": "metric_independent_topological_cell_current",
            "action_form": "S_ref = int B_2 wedge dJ_1 or int eta_I dX^I constraints",
            "owns_u": "no_or_indirect",
            "owns_D": "yes",
            "stress_status": "stress_free_if_metric_independent",
            "verdict": "support_only",
        },
        {
            "candidate": "gauge_fixed_reference_labels_only",
            "action_form": "T and X^I are gauge/reference labels with no stress action; Ccoh is diagnostic not action-coupled",
            "owns_u": "gauge_only",
            "owns_D": "gauge_only",
            "stress_status": "stress_free",
            "verdict": "closure_only_not_parent_action",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction": "metric_dependence_required_to_define_unit_u",
            "why_it_matters": "u_mu = -nabla_mu T/sqrt(-X_T) varies with g",
            "consequence": "T_ref contributes stress if it appears in the action nontrivially",
            "severity": "high",
        },
        {
            "obstruction": "multipliers_are_sources",
            "why_it_matters": "lambda_u and lambda_chi terms vary with g",
            "consequence": "constraints can leave dust-like or anisotropic stress",
            "severity": "high",
        },
        {
            "obstruction": "Ccoh_action_coupling_reintroduces_metric_variation",
            "why_it_matters": "S_gate = int sqrt(-g) Ccoh L_mem makes Ccoh part of T_munu",
            "consequence": "cannot claim stress-free reference sector while Ccoh depends on metric-owned kinematics",
            "severity": "high",
        },
        {
            "obstruction": "topological_current_owns_D_not_u",
            "why_it_matters": "metric-independent cell currents can be stress-free but do not select the observer congruence",
            "consequence": "only half of E_u/E_D problem is solved",
            "severity": "medium",
        },
        {
            "obstruction": "gauge_labels_are_not_physical_selectors",
            "why_it_matters": "pure labels can be stress-free but cannot determine where memory is active",
            "consequence": "route becomes diagnostic closure rather than parent derivation",
            "severity": "high",
        },
    ]


def gate_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "stress_free_parent_action_found",
            "result": "fail",
            "reason": "every action that dynamically owns u through metric-normalized T carries metric variation or multipliers",
        },
        {
            "gate": "stress_free_D_owner_found",
            "result": "partial_pass",
            "reason": "metric-independent/topological cell currents can own D but not the full u/D pair",
        },
        {
            "gate": "Ccoh_inside_action_allowed",
            "result": "fail",
            "reason": "Ccoh action coupling reintroduces reference/metric stress unless treated as diagnostic closure",
        },
        {
            "gate": "local_GR_branch_promoted",
            "result": "fail",
            "reason": "no stress-free parent owner for both u and D was found",
        },
        {
            "gate": "diagnostic_closure_route_allowed",
            "result": "pass",
            "reason": "T/X labels or topological currents may still define a non-claimable closure/benchmark",
        },
        {
            "gate": "next_work_should_continue_local_parent_route",
            "result": "fail",
            "reason": "checkpoint 77 kill condition now triggers for the parent-action local route",
        },
    ]


def demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_piece": "Ccoh_inside_parent_action",
            "new_status": "demoted",
            "allowed_use": "not used as derived local GR mechanism",
            "reason": "stress-free parent action was not found",
        },
        {
            "route_piece": "auxiliary_clock_cell_reference",
            "new_status": "diagnostic_closure_only",
            "allowed_use": "define cells/frames for internal tests, not as physical fields",
            "reason": "pure gauge labels are stress-free but not physical selectors",
        },
        {
            "route_piece": "topological_D_current",
            "new_status": "support_structure",
            "allowed_use": "boundary/conservation bookkeeping",
            "reason": "can own D-like current but not the full local-GR reduction",
        },
        {
            "route_piece": "local_GR_reduction",
            "new_status": "unresolved_not_derived",
            "allowed_use": "must be addressed by another route or empirical closure only",
            "reason": "u/D parent ownership failed the stress-free action gate",
        },
    ]


def next_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_next": "amplitude_normalization_gate",
            "why_now": "local parent route failed; amplitude remains a central cross-sector theoretical parameter",
            "risk": "still not a full field theory without local GR route",
            "priority": "high",
        },
        {
            "candidate_next": "empirical_closure_testing",
            "why_now": "closure-level models can still be tested honestly against cosmology/galaxy/local data",
            "risk": "tests phenomenology rather than derived theory",
            "priority": "high",
        },
        {
            "candidate_next": "perturbation_lensing_growth_contract",
            "why_now": "needed for cosmology seriousness and comparison with GR",
            "risk": "requires a stable background closure",
            "priority": "medium_high",
        },
        {
            "candidate_next": "new_local_GR_derivation_route",
            "why_now": "the core requirement remains that MTS reduce to GR locally",
            "risk": "must avoid repeating hidden-selector route",
            "priority": "deferred_until_new_idea",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "stress_free_reference_action_status",
            "status": "failed_as_parent_action",
            "evidence": "stress-free topological/gauge structures can support diagnostics but do not own both u and D as physical parent equations",
            "next_action": "demote local Ccoh parent route and pivot to amplitude/empirical closure gates",
        },
        {
            "decision": "local_Ccoh_route_status",
            "status": "demoted_to_diagnostic_closure",
            "evidence": "checkpoint 79 kill rule triggered: no full stress-free parent owner found",
            "next_action": "create 81-post-local-route-pivot-decision.md",
        },
        {
            "decision": "local_GR_status",
            "status": "not_derived",
            "evidence": "no acceptable stress-free u/D parent action",
            "next_action": "preserve result as honest blocker, not a claim",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "stress_free_reference_parent_action_failed_local_Ccoh_demoted",
        "key_metrics": {
            "action_candidates": counts["action_candidates"],
            "obstructions": counts["obstructions"],
            "gate_results": counts["gate_results"],
            "demotions": counts["demotion_register"],
            "next_routes": counts["next_route_options"],
        },
        "decision": decision_rows()[0],
        "next_target": "81-post-local-route-pivot-decision.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-stress-free-reference-action-gate"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "action_candidates": (
            action_candidate_rows(),
            ["candidate", "action_form", "owns_u", "owns_D", "stress_status", "verdict"],
        ),
        "obstructions": (
            obstruction_rows(),
            ["obstruction", "why_it_matters", "consequence", "severity"],
        ),
        "gate_results": (
            gate_result_rows(),
            ["gate", "result", "reason"],
        ),
        "demotion_register": (
            demotion_rows(),
            ["route_piece", "new_status", "allowed_use", "reason"],
        ),
        "next_route_options": (
            next_route_rows(),
            ["candidate_next", "why_now", "risk", "priority"],
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
