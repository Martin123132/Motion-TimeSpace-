#!/usr/bin/env python3
"""Audit possible parent origins for reciprocal routing T^2 S = 1."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_02_STATUS = Path("runs/20260530-223507-motion-load-local-GR-reduction/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "motion_capacity_reciprocity",
            "principle": "lost clock capacity is exactly routed into radial spatial capacity",
            "derivation": "T^2 S = constant; asymptotic flatness sets constant=1",
            "status": "clean_postulate_not_parent_derived",
            "risk": "could simply rename the desired p=1 result",
            "next_requirement": "derive from a variational or conservation law",
        },
        {
            "candidate": "determinant_balance",
            "principle": "the t-r two-volume element remains flat in the local vacuum routing sector",
            "derivation": "sqrt(T^2 S)=1 -> T^2 S=1",
            "status": "conditional_geometric_axiom",
            "risk": "area/time-radial gauge condition may be chosen rather than physical",
            "next_requirement": "show why the parent load sector preserves t-r phase volume",
        },
        {
            "candidate": "vacuum_stress_balance",
            "principle": "static spherical exterior has no net radial pressure anisotropy in the routing sector",
            "derivation": "for areal metric ds^2=-A dt^2+B dr^2+r^2 dOmega^2, G^t_t=G^r_r implies (A B)'=0; flat infinity gives A B=1",
            "status": "strongest_route_but_GR_like",
            "risk": "uses Einstein-geometry style field equation unless parent action derives the same stress balance",
            "next_requirement": "derive G^t_t=G^r_r analogue from motion-load action",
        },
        {
            "candidate": "null_cone_preservation",
            "principle": "local radial null cone preserves reciprocal redshift/routing accounting",
            "derivation": "radial null speed c_r=c T/sqrt(S); requiring Schwarzschild exterior speed c(1-L) gives S=1/T^2",
            "status": "observationally_correct_but_not_explanatory",
            "risk": "imports the GR exterior coordinate speed",
            "next_requirement": "derive the c(1-L) exterior light-routing law independently",
        },
        {
            "candidate": "hamiltonian_dual_metric",
            "principle": "clock energy and radial momentum use inverse quadratic weights in the local mass-shell constraint",
            "derivation": "H=-E^2/T^2 + p_r^2/S + ... preserves flat-form duality only when S=1/T^2",
            "status": "promising_action_hint",
            "risk": "needs a real parent Hamiltonian, not analogy",
            "next_requirement": "write the parent mass-shell/action and vary it",
        },
    ]


def algebra_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in (0.0, 0.5, 1.0, 1.5, 2.0):
        exponent = 1.0 - p
        # Use representative solar limb load to show deviation is tiny observationally
        # but algebraically nonzero unless p=1.
        load = 2.0 * 6.67430e-11 * 1.98847e30 / (6.957e8 * 299_792_458.0**2)
        product = (1.0 - load) ** exponent
        rows.append(
            {
                "p": p,
                "T2S_expression": "(1-L)^(1-p)",
                "variable_L_reciprocal": p == 1.0,
                "solar_limb_T2S": product,
                "solar_limb_deviation_from_1": product - 1.0,
                "interpretation": "only p=1 makes reciprocity exact for arbitrary load L",
            }
        )
    return rows


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_02_complete",
            "status": "pass" if source.get("readout") == "motion_load_local_GR_reduction_conditional_not_promoted" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "algebra_forces_p_equals_1",
            "status": "pass",
            "detail": "T^2S=(1-L)^(1-p), so exact reciprocity for variable L requires p=1",
        },
        {
            "gate": "candidate_parent_origin_found",
            "status": "partial",
            "detail": "vacuum stress balance and Hamiltonian duality are plausible parent routes",
        },
        {
            "gate": "non_GR_parent_derivation",
            "status": "fail",
            "detail": "no independent MTS action yet derives T^2S=1",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "reciprocity remains a theorem target, not a completed theorem",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "reciprocity_status",
            "status": "algebraically_powerful_but_parent_open",
            "evidence": "T^2S=1 immediately forces p=1 and local weak-field GR lane",
            "next_action": "derive reciprocity from an action or stress-balance theorem",
        },
        {
            "decision": "best_parent_route",
            "status": "vacuum_stress_balance_plus_hamiltonian_duality",
            "evidence": "AB=1 follows from areal static vacuum stress equality; dual Hamiltonian gives an MTS-flavoured action hint",
            "next_action": "write a parent action/stress contract rather than promote the postulate",
        },
        {
            "decision": "route_promotion",
            "status": "not_allowed",
            "evidence": "strongest derivation still borrows GR-like field equation structure",
            "next_action": "continue in post-checkpoint folder only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit reciprocal routing parent-origin candidates.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_02_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-reciprocal-routing-parent-origin"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = candidate_rows()
    algebra = algebra_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "reciprocal_origin_candidates.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "reciprocity_p_algebra.csv", algebra, list(algebra[0].keys()))
    write_csv(results_dir / "reciprocity_origin_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "reciprocity_origin_decision.csv", decisions, list(decisions[0].keys()))

    readout = "reciprocal_routing_parent_origin_partial_not_derived"
    status = {
        "status": "complete_reciprocal_routing_parent_origin",
        "readout": readout,
        "recommendation": "write_vacuum_reciprocity_action_contract_next",
        "next_target": "04-vacuum-reciprocity-action-contract.md",
        "reciprocity_algebra_forces_p_equals_1": True,
        "parent_origin_candidate_found": True,
        "non_GR_parent_derivation_complete": False,
        "promotion_to_main_workbench_allowed": False,
        "best_parent_route": "vacuum_stress_balance_plus_hamiltonian_duality",
        "outputs": {
            "reciprocal_origin_candidates": str(results_dir / "reciprocal_origin_candidates.csv"),
            "reciprocity_p_algebra": str(results_dir / "reciprocity_p_algebra.csv"),
            "reciprocity_origin_gates": str(results_dir / "reciprocity_origin_gates.csv"),
            "reciprocity_origin_decision": str(results_dir / "reciprocity_origin_decision.csv"),
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
