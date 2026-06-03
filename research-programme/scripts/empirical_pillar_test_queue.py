#!/usr/bin/env python3
"""Build an empirical pillar test queue from the parent-action skeleton."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_19_STATUS = Path("runs/20260530-233405-constrained-parent-action-skeleton/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pillar_rows() -> list[dict[str, Any]]:
    return [
        {
            "pillar": "local_PPN_clocks",
            "priority": 1,
            "readiness": "screening_ready",
            "available_artifacts": "13-16 local closure/deviation/data-map/gate-runner",
            "parameters": "q_R,Q_R,delta_beta,alpha_clock,epsilon_matter",
            "next_test": "use gate-runner for any proposed local branch",
            "claim_limit": "screening/control only; no raw likelihood and no derived local GR",
        },
        {
            "pillar": "cosmology",
            "priority": 2,
            "readiness": "robustness_ready_but_parent_bridge_open",
            "available_artifacts": "formalization-workbench cosmology smoke/robustness branch; parent skeleton C/M placeholder",
            "parameters": "C(t),M_cosmo_or_memory,b_mem,A_act,nu_act,alpha_act",
            "next_test": "return to robustness matrix only after mapping closure vs derived parameters",
            "claim_limit": "no claim if preference hits prior edges or parameters remain phenomenological",
        },
        {
            "pillar": "galaxies",
            "priority": 3,
            "readiness": "separate_thread_ready",
            "available_artifacts": "galaxy repo/thread; not modified in post-checkpoint route",
            "parameters": "acceleration/routing/memory parameters to be mapped later",
            "next_test": "treat as empirical pillar after parent-action hooks are named",
            "claim_limit": "not a unified-field proof by itself",
        },
        {
            "pillar": "EM_time",
            "priority": 4,
            "readiness": "audit_needed",
            "available_artifacts": "attachments/corpus notes only",
            "parameters": "alpha_clock,epsilon_matter,EM coupling candidates",
            "next_test": "variable/action mapping before numerical tests",
            "claim_limit": "avoid speculative hardware/processor overclaim",
        },
        {
            "pillar": "orbital_systems",
            "priority": 5,
            "readiness": "partly_screening_ready",
            "available_artifacts": "local PPN sensitivity and bounds gate-runner",
            "parameters": "q_R,delta_beta,Q_R,alpha_clock",
            "next_test": "only fit raw orbit data if a nonzero branch survives screening",
            "claim_limit": "published-bound screening before raw fit",
        },
        {
            "pillar": "particle_quantum",
            "priority": 6,
            "readiness": "not_ready",
            "available_artifacts": "corpus audit only",
            "parameters": "matter-coupling and mass-generation variables unknown",
            "next_test": "defer until parent matter action is explicit",
            "claim_limit": "no quantitative claim",
        },
    ]


def next_run_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "local_branch_screening",
            "pillar": "local_PPN_clocks",
            "run_type": "short",
            "command_or_artifact": "scripts/local_bounds_gate_runner.py",
            "entry_condition": "any proposed local branch with q_R/delta_beta/alpha_clock/epsilon_matter/Q_R values",
            "exit_gate": "branch must pass all screening gates or be rejected/demoted",
        },
        {
            "run_id": "cosmology_bridge_audit",
            "pillar": "cosmology",
            "run_type": "document_audit",
            "command_or_artifact": "new 21-cosmology-parent-bridge-audit.md",
            "entry_condition": "identify C/M variables that can be tied to parent skeleton",
            "exit_gate": "each fitted cosmology parameter labeled derived/postulated/phenomenological",
        },
        {
            "run_id": "cosmology_robustness_return",
            "pillar": "cosmology",
            "run_type": "medium_or_long",
            "command_or_artifact": "formalization-workbench cosmology robustness scripts",
            "entry_condition": "bridge audit complete and priors/splits fixed",
            "exit_gate": "no edge-hit branch treated as stable evidence",
        },
        {
            "run_id": "EM_time_variable_map",
            "pillar": "EM_time",
            "run_type": "document_audit",
            "command_or_artifact": "new EM/time variable-to-action map",
            "entry_condition": "extract symbols from corpus/attachments",
            "exit_gate": "testable couplings separated from speculation",
        },
        {
            "run_id": "galaxy_pillar_interface",
            "pillar": "galaxies",
            "run_type": "interface_only",
            "command_or_artifact": "do not modify galaxy repo here",
            "entry_condition": "galaxy work remains separate",
            "exit_gate": "only shared variables/action hooks exported back to unified programme",
        },
    ]


def claim_ladder_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_level": "L0_control",
            "allowed_phrase": "closure/control benchmark reproduces known limit",
            "evidence_needed": "explicit closure assumptions and sanity-check numbers",
            "forbidden_upgrade": "calling closure a derivation",
        },
        {
            "claim_level": "L1_screened",
            "allowed_phrase": "candidate branch survives published-bound screening",
            "evidence_needed": "gate-runner pass/fail output",
            "forbidden_upgrade": "calling screening a raw-data fit",
        },
        {
            "claim_level": "L2_fit",
            "allowed_phrase": "candidate improves a dataset under specified likelihood",
            "evidence_needed": "raw/curated likelihood, baselines, AIC/BIC, residuals, priors",
            "forbidden_upgrade": "ignoring prior-edge or baseline failures",
        },
        {
            "claim_level": "L3_robust",
            "allowed_phrase": "signal survives priors, splits, jackknives, and baselines",
            "evidence_needed": "robustness matrix against GR/LCDM/MOND-like baselines as applicable",
            "forbidden_upgrade": "testing MTS harder than baselines without reporting baseline failures",
        },
        {
            "claim_level": "L4_derived",
            "allowed_phrase": "parameter follows from parent action",
            "evidence_needed": "variation, conservation identity, local/cosmology limits",
            "forbidden_upgrade": "fitted parameter relabeled as derived",
        },
        {
            "claim_level": "L5_unified",
            "allowed_phrase": "same parent action explains multiple pillars",
            "evidence_needed": "shared variables, no contradictory limits, independent robust tests",
            "forbidden_upgrade": "one empirical pillar treated as full theory proof",
        },
    ]


def risk_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk": "phenomenology_without_parent",
            "where": "cosmology/galaxies",
            "severity": "high",
            "mitigation": "every parameter labeled derived/postulated/phenomenological",
        },
        {
            "risk": "closure_as_derivation",
            "where": "local_PPN",
            "severity": "critical",
            "mitigation": "claim ladder and stage-17 promotion summary",
        },
        {
            "risk": "baseline_asymmetry",
            "where": "all empirical pillars",
            "severity": "high",
            "mitigation": "apply jackknife/split/baseline tests to MTS and competitors where possible",
        },
        {
            "risk": "prior_edge_signal",
            "where": "cosmology",
            "severity": "high",
            "mitigation": "no prior-edge branch treated as evidence",
        },
        {
            "risk": "repo_scope_contamination",
            "where": "galaxies/main workbench",
            "severity": "medium",
            "mitigation": "keep post-checkpoint and galaxy work separate unless explicitly promoted",
        },
        {
            "risk": "speculative_EM_overclaim",
            "where": "EM_time/hardware anecdotes",
            "severity": "medium",
            "mitigation": "map variables and tests before public-facing claims",
        },
    ]


def queue_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_19_complete",
            "status": "pass" if source.get("readout") == "constrained_parent_action_skeleton_contract_not_derivation" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "all_major_pillars_listed",
            "status": "pass",
            "detail": "local, cosmology, galaxies, EM/time, orbital, particle/quantum included",
        },
        {
            "gate": "claim_ladder_defined",
            "status": "pass",
            "detail": "control/screened/fit/robust/derived/unified levels separated",
        },
        {
            "gate": "next_runs_prioritized",
            "status": "pass",
            "detail": "local screening and cosmology bridge are first actionable tests",
        },
        {
            "gate": "empirical_claim_allowed_now",
            "status": "fail",
            "detail": "queue defines tests; it is not test completion",
        },
        {
            "gate": "main_workbench_mutation_allowed",
            "status": "fail",
            "detail": "queue remains post-checkpoint planning",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "empirical_queue_status",
            "status": "ready_for_disciplined_next_runs",
            "evidence": "pillars, runs, claim ladder, and risks are mapped",
            "next_action": "build 21-cosmology-parent-bridge-audit.md before long cosmology runs",
        },
        {
            "decision": "first_empirical_target",
            "status": "cosmology_bridge_audit",
            "evidence": "local branch is already screened; cosmology has active signals but parent bridge is open",
            "next_action": "map cosmology variables to parent skeleton",
        },
        {
            "decision": "local_branch_use",
            "status": "screening_tool_only",
            "evidence": "local closure remains non-derived",
            "next_action": "reuse gate-runner for any proposed local deviations",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Empirical pillar test queue.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_19_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-empirical-pillar-test-queue"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    pillars = pillar_rows()
    runs = next_run_rows()
    claims = claim_ladder_rows()
    risks = risk_register_rows()
    gates = queue_gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "empirical_pillars.csv", pillars, list(pillars[0].keys()))
    write_csv(results_dir / "next_empirical_runs.csv", runs, list(runs[0].keys()))
    write_csv(results_dir / "claim_ladder.csv", claims, list(claims[0].keys()))
    write_csv(results_dir / "empirical_risk_register.csv", risks, list(risks[0].keys()))
    write_csv(results_dir / "empirical_queue_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "empirical_queue_decision.csv", decisions, list(decisions[0].keys()))

    readout = "empirical_pillar_test_queue_ready_no_claims"
    status = {
        "status": "complete_empirical_pillar_test_queue",
        "readout": readout,
        "recommendation": "build_cosmology_parent_bridge_audit_next",
        "next_target": "21-cosmology-parent-bridge-audit.md",
        "empirical_claim_allowed_now": False,
        "main_workbench_mutation_allowed_now": False,
        "first_empirical_target": "cosmology_bridge_audit",
        "claim_ladder_levels": [row["claim_level"] for row in claims],
        "outputs": {
            "empirical_pillars": str(results_dir / "empirical_pillars.csv"),
            "next_empirical_runs": str(results_dir / "next_empirical_runs.csv"),
            "claim_ladder": str(results_dir / "claim_ladder.csv"),
            "empirical_risk_register": str(results_dir / "empirical_risk_register.csv"),
            "empirical_queue_gates": str(results_dir / "empirical_queue_gates.csv"),
            "empirical_queue_decision": str(results_dir / "empirical_queue_decision.csv"),
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
