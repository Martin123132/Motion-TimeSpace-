#!/usr/bin/env python3
"""Attempt to derive the reciprocal constraint from a conserved cell current."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_10_STATUS = Path("runs/20260530-230334-observer-map-symplectic-contract/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def current_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "gradient_cell_current",
            "equation": "partial_r(W partial_r R_AB)=0",
            "vacuum_solution": "W partial_r R_AB = Q_R",
            "does_it_force_R_AB_zero": "no",
            "verdict": "fails_without_no_charge_theorem",
        },
        {
            "route": "radial_flux_absence",
            "equation": "C_R^r=0 in static exterior",
            "vacuum_solution": "partial_r R_AB=0 if C_R^r=W partial_r R_AB",
            "does_it_force_R_AB_zero": "yes_if_boundary_R_infinity_zero",
            "verdict": "works_only_if_flux_absence_is_parent_derived",
        },
        {
            "route": "algebraic_cell_current",
            "equation": "C_R^r=kappa R_AB and C_R^r=0",
            "vacuum_solution": "R_AB=0",
            "does_it_force_R_AB_zero": "yes",
            "verdict": "renames_the_constraint_unless_C_R^r=0_is_derived",
        },
        {
            "route": "cell_number_continuity",
            "equation": "nabla_a N_cell^a=0",
            "vacuum_solution": "conserves integrated cell number",
            "does_it_force_R_AB_zero": "no",
            "verdict": "too_weak_without_constitutive_law_N_cell(R_AB)",
        },
        {
            "route": "noether_current_for_cell_scaling",
            "equation": "nabla_a J_Noether^a=E_T deltaT + E_S deltaS",
            "vacuum_solution": "Ward identity on equations of motion",
            "does_it_force_R_AB_zero": "no",
            "verdict": "symmetry_identity_not_constraint",
        },
        {
            "route": "topological_zero_charge",
            "equation": "Q_R=integral_source rho_R = 0 by source representation",
            "vacuum_solution": "R_AB=0 with asymptotic boundary",
            "does_it_force_R_AB_zero": "yes_if_theorem_true",
            "verdict": "best_possible_route_but_not_presently_derived",
        },
    ]


def hair_solution_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    radii = (1.0, 2.0, 10.0, 100.0)
    for charge in (0.0, 1.0e-6, 1.0e-5, 1.0e-4):
        for radius in radii:
            r_ab = -charge / radius
            rows.append(
                {
                    "W_choice": "r^2",
                    "Q_R": charge,
                    "radius_units": radius,
                    "R_AB_with_R_infinity_zero": r_ab,
                    "gamma_minus_1_proxy": abs(r_ab),
                    "internal_gamma_gate": 1.0e-5,
                    "status": "pass_at_this_radius" if abs(r_ab) <= 1.0e-5 else "fail_at_this_radius",
                }
            )
    return rows


def no_charge_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "source_representation",
            "needed_statement": "ordinary compact matter has zero reciprocal cell charge rho_R",
            "why_needed": "otherwise Q_R sources exterior R_AB hair",
            "status": "not_derived",
        },
        {
            "requirement": "boundary_variation",
            "needed_statement": "Pi_R at the source surface vanishes from the matter action",
            "why_needed": "Q_R=-Pi_R in matching",
            "status": "not_derived",
        },
        {
            "requirement": "conservation_identity",
            "needed_statement": "a Ward/Bianchi identity forbids net reciprocal charge",
            "why_needed": "turns Q_R=0 into theorem rather than assumption",
            "status": "not_derived",
        },
        {
            "requirement": "no_propagating_R_AB",
            "needed_statement": "R_AB is a constrained variable, not a kinetic exterior field",
            "why_needed": "removes the entire hair channel",
            "status": "available_as_closure_only",
        },
        {
            "requirement": "observable_residual_bound",
            "needed_statement": "if Q_R is nonzero, prove |gamma-1| below local PPN bound",
            "why_needed": "prevents reciprocal hair from breaking solar-system tests",
            "status": "not_predictive",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_10_complete",
            "status": "pass" if source.get("readout") == "observer_map_contract_written_not_satisfied" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "cell_current_equation_written",
            "status": "pass",
            "detail": "partial_r(W partial_r R_AB)=0 gives conserved Q_R",
        },
        {
            "gate": "asymptotic_boundary_kills_hair",
            "status": "fail",
            "detail": "R_AB(infinity)=0 still permits R_AB=-Q_R/r for W=r^2",
        },
        {
            "gate": "conservation_alone_derives_R_AB_zero",
            "status": "fail",
            "detail": "conservation gives a charge, not zero charge",
        },
        {
            "gate": "no_charge_theorem",
            "status": "fail",
            "detail": "no parent theorem currently forces Q_R=0 or Pi_R=0",
        },
        {
            "gate": "algebraic_constraint_available",
            "status": "conditional_pass",
            "detail": "R_AB=0 works if imposed as nonpropagating constraint, but this is closure-only",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "cell-current route does not close lambda-origin gate",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "cell_current_origin_status",
            "status": "no_charge_obstruction",
            "evidence": "a conserved current generically leaves Q_R hair",
            "next_action": "try gauge/Noether origin or keep R_AB=0 as explicit closure",
        },
        {
            "decision": "best_clean_local_route",
            "status": "nonpropagating_constraint",
            "evidence": "it removes the hair channel, but still needs parent origin",
            "next_action": "do not promote as derived",
        },
        {
            "decision": "next_target",
            "status": "gauge_noether_origin_audit",
            "evidence": "ordinary conservation has failed; only symmetry/constraint origin remains",
            "next_action": "create 12-gauge-noether-origin-audit.md",
        },
    ]


def summary_numbers() -> dict[str, Any]:
    charge = 1.0e-5
    radius = 1.0
    r_ab = -charge / radius
    return {
        "example_Q_R": charge,
        "example_radius": radius,
        "example_R_AB": r_ab,
        "example_gamma_minus_1_proxy": abs(r_ab),
        "internal_gamma_gate": 1.0e-5,
        "hair_solution_form_for_W_r2": "R_AB = R_infinity - Q_R/r",
        "finite_charge_is_allowed_by_asymptotic_flatness": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Cell-current origin attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_10_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-cell-current-origin-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    routes = current_route_rows()
    hair = hair_solution_rows()
    no_charge = no_charge_requirement_rows()
    gates = gate_rows(source)
    decisions = decision_rows()
    numbers = summary_numbers()

    write_csv(results_dir / "cell_current_routes.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "cell_current_hair_examples.csv", hair, list(hair[0].keys()))
    write_csv(results_dir / "no_charge_requirements.csv", no_charge, list(no_charge[0].keys()))
    write_csv(results_dir / "cell_current_origin_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "cell_current_origin_decision.csv", decisions, list(decisions[0].keys()))

    readout = "cell_current_origin_no_charge_obstruction"
    status = {
        "status": "complete_cell_current_origin_attempt",
        "readout": readout,
        "recommendation": "attempt_gauge_noether_origin_next_or_demote_to_closure",
        "next_target": "12-gauge-noether-origin-audit.md",
        "cell_current_conservation_written": True,
        "cell_current_derives_R_AB_zero": False,
        "no_charge_theorem_derived": False,
        "nonpropagating_constraint_remains_best_closure": True,
        "promotion_to_main_workbench_allowed": False,
        "summary_numbers": numbers,
        "outputs": {
            "cell_current_routes": str(results_dir / "cell_current_routes.csv"),
            "cell_current_hair_examples": str(results_dir / "cell_current_hair_examples.csv"),
            "no_charge_requirements": str(results_dir / "no_charge_requirements.csv"),
            "cell_current_origin_gates": str(results_dir / "cell_current_origin_gates.csv"),
            "cell_current_origin_decision": str(results_dir / "cell_current_origin_decision.csv"),
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
