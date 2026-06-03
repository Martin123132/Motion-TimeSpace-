#!/usr/bin/env python3
"""Attempt the reciprocal-strain theorem for T^2 S = 1."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_04_STATUS = Path("runs/20260530-224152-vacuum-reciprocity-action-contract/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def theorem_steps() -> list[dict[str, Any]]:
    return [
        {
            "step": "action_ansatz",
            "equation": "S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB]",
            "result": "usable_toy_parent_form",
            "gap": "W and J_R still need derivation from full motion-load action",
        },
        {
            "step": "variation",
            "equation": "d/dr[W(r) R_AB'] = J_R",
            "result": "derived_from_toy_action",
            "gap": "not yet derived from complete parent action",
        },
        {
            "step": "vacuum_exterior",
            "equation": "J_R=0 -> W R_AB' = Q_R",
            "result": "reciprocal_charge_constant",
            "gap": "Q_R is an allowed integration constant unless killed by boundary/matching",
        },
        {
            "step": "desired_no_hair",
            "equation": "Q_R=0 -> R_AB'=0; R_AB(infinity)=0 -> R_AB=0",
            "result": "conditional_theorem",
            "gap": "Q_R=0 is not yet parent-derived",
        },
        {
            "step": "routing_result",
            "equation": "R_AB=0 -> AB=1 -> T^2 S=1 -> p=1",
            "result": "conditional_GR_routing",
            "gap": "depends on reciprocal-charge neutrality",
        },
    ]


def hair_mode_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (0, 1, 2, 3, 4):
        if n == 0:
            profile = "R_AB = -Q_R r + const"
            asym_flat_allows = False
            finite_energy_in_exterior = False
            note = "linear hair violates asymptotic flatness unless Q_R=0"
        elif n == 1:
            profile = "R_AB = -Q_R ln(r) + const"
            asym_flat_allows = False
            finite_energy_in_exterior = False
            note = "log hair violates asymptotic flatness unless Q_R=0"
        else:
            profile = f"R_AB = Q_R/({n}-1) r^(1-{n}) with R_AB(infinity)=0"
            asym_flat_allows = True
            finite_energy_in_exterior = True
            note = "decaying exterior reciprocal hair survives asymptotic flatness and finite exterior energy"
        rows.append(
            {
                "W_scaling": f"W ~ r^{n}",
                "vacuum_solution_with_QR": profile,
                "asymptotic_flatness_allows_QR_nonzero": asym_flat_allows,
                "finite_exterior_energy_allows_QR_nonzero": finite_energy_in_exterior,
                "interpretation": note,
            }
        )
    return rows


def boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "asymptotic_flatness_only",
            "kills_QR": False,
            "reason": "for natural spherical W~r^2, R_AB~Q_R/r is asymptotically flat",
            "status": "insufficient",
        },
        {
            "condition": "finite_exterior_energy_only",
            "kills_QR": False,
            "reason": "integral_R^infty Q_R^2/W dr is finite for W~r^2",
            "status": "insufficient",
        },
        {
            "condition": "regular_origin_with_no_surface",
            "kills_QR": True,
            "reason": "Q_R/r hair is singular if the vacuum solution extends to r=0",
            "status": "works_only_without_material_surface",
        },
        {
            "condition": "source_reciprocal_neutrality",
            "kills_QR": True,
            "reason": "matching condition Q_R = integral J_R dr = 0 forbids reciprocal charge",
            "status": "needed_parent_theorem",
        },
        {
            "condition": "natural_neumann_boundary_at_source",
            "kills_QR": True,
            "reason": "free boundary variation gives W R_AB'=0 at the source boundary",
            "status": "possible_but_must_be_derived",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_04_complete",
            "status": "pass" if source.get("readout") == "vacuum_reciprocity_action_contract_locked_not_satisfied" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "toy_action_variation",
            "status": "pass",
            "detail": "S_R variation gives d(W R_AB')/dr=J_R",
        },
        {
            "gate": "vacuum_equation",
            "status": "pass",
            "detail": "J_R=0 gives conserved reciprocal charge Q_R=W R_AB'",
        },
        {
            "gate": "asymptotic_flatness_no_hair",
            "status": "fail",
            "detail": "for W~r^2, Q_R/r hair is asymptotically flat and finite-energy outside the source",
        },
        {
            "gate": "reciprocal_charge_neutrality_derived",
            "status": "fail",
            "detail": "Q_R=0 must be derived from source matching or boundary variation",
        },
        {
            "gate": "conditional_AB_equals_1",
            "status": "conditional_pass",
            "detail": "if Q_R=0, then R_AB=0 and T^2S=1 follows",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "the theorem has a no-hair obstruction",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "reciprocity_theorem_status",
            "status": "conditional_not_complete",
            "evidence": "AB=1 follows only after imposing Q_R=0",
            "next_action": "derive reciprocal charge neutrality from source matching",
        },
        {
            "decision": "hidden_obstruction",
            "status": "reciprocal_hair_QR",
            "evidence": "natural W~r^2 allows R_AB~Q_R/r exterior hair",
            "next_action": "write reciprocal-charge source-neutrality gate",
        },
        {
            "decision": "motion_load_route_status",
            "status": "still_promising_not_promoted",
            "evidence": "the theorem nearly works but needs a no-reciprocal-charge law",
            "next_action": "continue in post-checkpoint sandbox",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Attempt reciprocal-strain theorem.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_04_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-reciprocity-theorem-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    steps = theorem_steps()
    hair = hair_mode_rows()
    boundaries = boundary_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "reciprocity_theorem_steps.csv", steps, list(steps[0].keys()))
    write_csv(results_dir / "reciprocal_hair_modes.csv", hair, list(hair[0].keys()))
    write_csv(results_dir / "reciprocity_boundary_conditions.csv", boundaries, list(boundaries[0].keys()))
    write_csv(results_dir / "reciprocity_theorem_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "reciprocity_theorem_decision.csv", decisions, list(decisions[0].keys()))

    readout = "reciprocity_theorem_conditional_no_hair_obstruction"
    status = {
        "status": "complete_reciprocity_theorem_attempt",
        "readout": readout,
        "recommendation": "derive_reciprocal_charge_source_neutrality_next",
        "next_target": "06-reciprocal-charge-source-neutrality.md",
        "toy_action_variation_works": True,
        "vacuum_conserved_charge_found": True,
        "AB_equals_1_if_QR_zero": True,
        "QR_zero_parent_derived": False,
        "reciprocal_hair_obstruction": True,
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "reciprocity_theorem_steps": str(results_dir / "reciprocity_theorem_steps.csv"),
            "reciprocal_hair_modes": str(results_dir / "reciprocal_hair_modes.csv"),
            "reciprocity_boundary_conditions": str(results_dir / "reciprocity_boundary_conditions.csv"),
            "reciprocity_theorem_gates": str(results_dir / "reciprocity_theorem_gates.csv"),
            "reciprocity_theorem_decision": str(results_dir / "reciprocity_theorem_decision.csv"),
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
