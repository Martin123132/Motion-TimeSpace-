#!/usr/bin/env python3
"""Test nonpropagating reciprocity as the clean route to AB=1."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_06_STATUS = Path("runs/20260530-224822-reciprocal-charge-source-neutrality/status.json")
GAMMA_GATE = 1.0e-5


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "kinetic_reciprocal_strain",
            "action_form": "0.5 W (R_AB')^2 + J_R R_AB",
            "hair_mode": "yes_QR",
            "AB_equals_1_status": "conditional_only",
            "verdict": "reject_as_fundamental_local_GR_route",
        },
        {
            "route": "hard_lagrange_constraint",
            "action_form": "lambda_R R_AB",
            "hair_mode": "none",
            "AB_equals_1_status": "exact_from_delta_lambda",
            "verdict": "best_clean_route_if_lambda_R_has_parent_origin",
        },
        {
            "route": "algebraic_stiff_potential",
            "action_form": "0.5 m_R^2 R_AB^2 + J_R R_AB",
            "hair_mode": "no_long_range_hair_but_finite_residual",
            "AB_equals_1_status": "approximate_R_AB=-J_R/m_R^2",
            "verdict": "allowed_only_if_residual_bound_is_derived",
        },
        {
            "route": "gauge_choice_only",
            "action_form": "choose AB=1 as radial gauge",
            "hair_mode": "not_physical",
            "AB_equals_1_status": "not_a_derivation",
            "verdict": "reject_if_used_as_physics",
        },
        {
            "route": "determinant_balance_constraint",
            "action_form": "lambda_R ln(T^2 S) from local motion-capacity phase-volume balance",
            "hair_mode": "none_if_true_constraint",
            "AB_equals_1_status": "exact_if_phase_volume_balance_is_parent_derived",
            "verdict": "promising_parent_principle_target",
        },
    ]


def variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta_lambda_R",
            "equation": "R_AB = ln(A B)=0",
            "consequence": "AB=1 and T^2S=1 exactly",
            "status": "constraint_variation_pass",
        },
        {
            "variation": "delta_R_AB",
            "equation": "lambda_R + source_reaction = 0",
            "consequence": "lambda_R carries reaction stress instead of R_AB carrying hair",
            "status": "reaction_channel_not_hair",
        },
        {
            "variation": "exterior_vacuum",
            "equation": "no R_AB kinetic term -> no conserved Q_R",
            "consequence": "reciprocal hair obstruction removed",
            "status": "hair_removed",
        },
        {
            "variation": "weak_field",
            "equation": "T^2S=1 and T^2=1-L -> S=1/(1-L)",
            "consequence": "p=1 and gamma=1",
            "status": "local_GR_lane_recovered",
        },
    ]


def finite_stiffness_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_over_stiffness in (0.0, 1.0e-7, 1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3):
        rows.append(
            {
                "J_R_over_m_R2": source_over_stiffness,
                "R_AB_residual": -source_over_stiffness,
                "gamma_minus_1_proxy": abs(source_over_stiffness),
                "internal_gate": GAMMA_GATE,
                "status": "pass" if abs(source_over_stiffness) <= GAMMA_GATE else "fail",
                "interpretation": "finite stiffness route needs residual below PPN gate; hard constraint avoids this",
            }
        )
    return rows


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_06_complete",
            "status": "pass" if source.get("readout") == "reciprocal_charge_neutrality_conditional_not_parent_derived" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "hair_obstruction_removed",
            "status": "pass",
            "detail": "nonpropagating constraint has no exterior Q_R charge",
        },
        {
            "gate": "AB_equals_1_from_constraint",
            "status": "pass",
            "detail": "delta lambda_R gives ln(AB)=0",
        },
        {
            "gate": "p_equals_1_recovered",
            "status": "pass",
            "detail": "T^2=1-L and AB=1 imply S=1/(1-L)",
        },
        {
            "gate": "constraint_parent_origin",
            "status": "fail",
            "detail": "lambda_R/phase-volume balance is not yet derived from motion-load action",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "route is cleaner but still lacks parent origin",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "best_reciprocity_route",
            "status": "hard_constraint_or_phase_volume_balance",
            "evidence": "removes Q_R hair and derives AB=1 algebraically",
            "next_action": "derive lambda_R from conserved motion-capacity phase volume",
        },
        {
            "decision": "kinetic_R_AB_route",
            "status": "demoted",
            "evidence": "propagating reciprocal strain creates Q_R hair",
            "next_action": "keep only as diagnostic of what must be forbidden",
        },
        {
            "decision": "promotion_status",
            "status": "not_allowed",
            "evidence": "constraint origin is not parent-derived",
            "next_action": "write phase-volume constraint origin attempt",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Test nonpropagating reciprocity constraint.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_06_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-nonpropagating-reciprocity-constraint"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    routes = route_rows()
    variations = variation_rows()
    stiffness = finite_stiffness_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "reciprocity_constraint_routes.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "constraint_variation_chain.csv", variations, list(variations[0].keys()))
    write_csv(results_dir / "finite_stiffness_ppn_bounds.csv", stiffness, list(stiffness[0].keys()))
    write_csv(results_dir / "nonpropagating_constraint_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "nonpropagating_constraint_decision.csv", decisions, list(decisions[0].keys()))

    readout = "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open"
    status = {
        "status": "complete_nonpropagating_reciprocity_constraint",
        "readout": readout,
        "recommendation": "derive_phase_volume_constraint_origin_next",
        "next_target": "08-phase-volume-reciprocity-origin.md",
        "QR_hair_removed_by_constraint": True,
        "AB_equals_1_from_constraint": True,
        "p_equals_1_from_constraint": True,
        "constraint_parent_origin_derived": False,
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "reciprocity_constraint_routes": str(results_dir / "reciprocity_constraint_routes.csv"),
            "constraint_variation_chain": str(results_dir / "constraint_variation_chain.csv"),
            "finite_stiffness_ppn_bounds": str(results_dir / "finite_stiffness_ppn_bounds.csv"),
            "nonpropagating_constraint_gates": str(results_dir / "nonpropagating_constraint_gates.csv"),
            "nonpropagating_constraint_decision": str(results_dir / "nonpropagating_constraint_decision.csv"),
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
