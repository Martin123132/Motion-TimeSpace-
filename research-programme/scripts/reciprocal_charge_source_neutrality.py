#!/usr/bin/env python3
"""Test whether the reciprocal charge Q_R can be killed by source neutrality."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_05_STATUS = Path("runs/20260530-224448-reciprocity-theorem-attempt/status.json")
INTERNAL_GAMMA_GATE = 1.0e-5


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def matching_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "exterior_charge",
            "equation": "J_R=0 -> W R_AB' = Q_R",
            "meaning": "the exterior reciprocal strain carries a conserved charge",
            "status": "derived_in_05",
        },
        {
            "step": "source_boundary_variation",
            "equation": "delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface",
            "meaning": "Pi_R is the source reciprocal momentum/charge",
            "status": "matching_formula",
        },
        {
            "step": "matching_condition",
            "equation": "Q_R = -Pi_R",
            "meaning": "exterior reciprocal hair equals source reciprocal charge",
            "status": "conditional_parent_matching",
        },
        {
            "step": "neutral_source",
            "equation": "Pi_R=0 -> Q_R=0 -> AB=1",
            "meaning": "reciprocity is derived if matter/load sources carry no reciprocal charge",
            "status": "conditional_success",
        },
        {
            "step": "open_parent_task",
            "equation": "delta S_source/dR_AB = 0",
            "meaning": "must be derived from source coupling, not assumed",
            "status": "not_derived",
        },
    ]


def source_cases() -> list[dict[str, Any]]:
    return [
        {
            "case": "clock_only_load_coupling",
            "source_rule": "source couples to A=T^2 and mass-load L, not independently to R_AB",
            "Pi_R": "0",
            "QR_status": "killed_conditionally",
            "risk": "must prove spatial routing is not independently sourced by matter",
        },
        {
            "case": "natural_neumann_surface",
            "source_rule": "free variation of R_AB at the material surface gives W R_AB'=0",
            "Pi_R": "0",
            "QR_status": "killed_conditionally",
            "risk": "boundary variation may be too strong for real material interiors",
        },
        {
            "case": "fixed_surface_reciprocity",
            "source_rule": "R_AB is fixed at the source boundary",
            "Pi_R": "uncontrolled",
            "QR_status": "not_killed",
            "risk": "Dirichlet boundary can hide fitted reciprocal hair",
        },
        {
            "case": "anisotropic_routing_source",
            "source_rule": "matter carries independent radial routing stress",
            "Pi_R": "nonzero",
            "QR_status": "hair_generated",
            "risk": "produces gamma-1 residual unless extremely suppressed",
        },
        {
            "case": "constraint_not_kinetic_mode",
            "source_rule": "R_AB is a Lagrange/constraint mode rather than propagating scalar hair",
            "Pi_R": "forbidden",
            "QR_status": "best_structural_route",
            "risk": "requires rewriting the parent action so R_AB has no exterior charge mode",
        },
    ]


def ppn_bound_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for q_ratio in (0.0, 1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2):
        rows.append(
            {
                "q_ratio": q_ratio,
                "definition": "R_AB = q_ratio * L in weak field, L=2GM/(rc^2)",
                "gamma_minus_1_proxy": q_ratio,
                "internal_gate": INTERNAL_GAMMA_GATE,
                "status": "pass" if abs(q_ratio) <= INTERNAL_GAMMA_GATE else "fail",
                "interpretation": "nonzero reciprocal charge behaves like a PPN gamma residual",
            }
        )
    return rows


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_05_complete",
            "status": "pass" if source.get("readout") == "reciprocity_theorem_conditional_no_hair_obstruction" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "source_matching_formula",
            "status": "pass",
            "detail": "boundary variation gives Q_R=-Pi_R",
        },
        {
            "gate": "QR_zero_if_source_neutral",
            "status": "conditional_pass",
            "detail": "Pi_R=0 kills exterior reciprocal hair",
        },
        {
            "gate": "source_neutrality_parent_derived",
            "status": "fail",
            "detail": "delta S_source/dR_AB=0 is not yet derived from a full source action",
        },
        {
            "gate": "nonzero_QR_PPN_safety",
            "status": "fail",
            "detail": f"without neutrality, |Q_R/r_s| must be below internal gamma gate {INTERNAL_GAMMA_GATE:.1e}",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "reciprocity still depends on source-neutrality theorem",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "source_neutrality_status",
            "status": "conditional_not_complete",
            "evidence": "Q_R=-Pi_R and Pi_R=0 would derive AB=1, but Pi_R=0 is not parent-derived",
            "next_action": "derive source action independence from R_AB or replace R_AB by constraint",
        },
        {
            "decision": "best_route",
            "status": "constraint_or_clock_only_source",
            "evidence": "non-propagating reciprocal constraint is cleaner than tolerating reciprocal hair",
            "next_action": "write nonpropagating reciprocity constraint contract",
        },
        {
            "decision": "PPN_status",
            "status": "danger_if_nonzero",
            "evidence": f"reciprocal hair acts like gamma-1 and must be <= {INTERNAL_GAMMA_GATE:.1e}",
            "next_action": "do not promote unless Q_R=0 or tightly derived",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check reciprocal charge source neutrality.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_05_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-reciprocal-charge-source-neutrality"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    matching = matching_rows()
    cases = source_cases()
    bounds = ppn_bound_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "reciprocal_charge_matching.csv", matching, list(matching[0].keys()))
    write_csv(results_dir / "source_neutrality_cases.csv", cases, list(cases[0].keys()))
    write_csv(results_dir / "reciprocal_charge_ppn_bounds.csv", bounds, list(bounds[0].keys()))
    write_csv(results_dir / "source_neutrality_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "source_neutrality_decision.csv", decisions, list(decisions[0].keys()))

    readout = "reciprocal_charge_neutrality_conditional_not_parent_derived"
    status = {
        "status": "complete_reciprocal_charge_source_neutrality",
        "readout": readout,
        "recommendation": "write_nonpropagating_reciprocity_constraint_contract_next",
        "next_target": "07-nonpropagating-reciprocity-constraint.md",
        "QR_equals_minus_source_PiR": True,
        "QR_zero_if_source_neutral": True,
        "source_neutrality_parent_derived": False,
        "nonzero_QR_ppn_danger": True,
        "internal_gamma_gate": INTERNAL_GAMMA_GATE,
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "reciprocal_charge_matching": str(results_dir / "reciprocal_charge_matching.csv"),
            "source_neutrality_cases": str(results_dir / "source_neutrality_cases.csv"),
            "reciprocal_charge_ppn_bounds": str(results_dir / "reciprocal_charge_ppn_bounds.csv"),
            "source_neutrality_gates": str(results_dir / "source_neutrality_gates.csv"),
            "source_neutrality_decision": str(results_dir / "source_neutrality_decision.csv"),
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
