#!/usr/bin/env python3
"""Audit whether gauge or Noether structure can derive R_AB=0."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_11_STATUS = Path("runs/20260530-230553-cell-current-origin-attempt/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def gauge_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "radial_coordinate_gauge",
            "claim": "choose radial coordinate so AB=1",
            "problem": "areal radius gauge already fixes r by 4pi r^2; AB=1 is not residual coordinate freedom",
            "can_derive_R_AB_zero": "no",
            "verdict": "forbidden_as_GR_import_or_coordinate_confusion",
        },
        {
            "route": "cell_scale_gauge",
            "claim": "T sqrt(S) is gauge and can be fixed to one",
            "problem": "if metric/matter see T and S, changing T sqrt(S) changes observables such as gamma",
            "can_derive_R_AB_zero": "only_if_new_gauge_invariant_matter_map_exists",
            "verdict": "not_available_in_current_scaffold",
        },
        {
            "route": "reciprocal_split_gauge",
            "claim": "T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S)",
            "problem": "this leaves T sqrt(S) unchanged, so it cannot set R_AB=0",
            "can_derive_R_AB_zero": "no",
            "verdict": "wrong_transformation_for_target_constraint",
        },
        {
            "route": "noether_identity",
            "claim": "local symmetry gives a Ward identity that enforces reciprocity",
            "problem": "Noether identities relate equations of motion; they do not set a field value without a constraint equation",
            "can_derive_R_AB_zero": "no_by_itself",
            "verdict": "insufficient_without_first_class_constraint",
        },
        {
            "route": "first_class_constraint",
            "claim": "R_AB is eliminated by a primary constraint and gauge fixing",
            "problem": "would require a full constrained Hamiltonian parent theory and gauge-invariant observables",
            "can_derive_R_AB_zero": "possible_in_principle",
            "verdict": "future_parent_action_contract_not_current_derivation",
        },
        {
            "route": "lagrange_multiplier_constraint",
            "claim": "delta lambda_R gives R_AB=0",
            "problem": "works algebraically but lambda_R origin is not derived",
            "can_derive_R_AB_zero": "yes_as_closure",
            "verdict": "honest_closure_only_route",
        },
    ]


def noether_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "gauge_symmetry_output",
            "statement": "sum_i E_i delta_phi_i + divergence = 0",
            "implication": "relates Euler-Lagrange equations",
            "why_not_enough": "does not force R_AB=0 unless one E_i is a multiplier equation",
        },
        {
            "item": "constraint_equation_output",
            "statement": "delta lambda_R S = R_AB",
            "implication": "R_AB=0",
            "why_not_enough": "lambda_R still needs a parent origin",
        },
        {
            "item": "charge_elimination_output",
            "statement": "first-class constraint removes conjugate reciprocal charge",
            "implication": "Q_R may be gauge-forbidden",
            "why_not_enough": "requires a constrained Hamiltonian derivation not present here",
        },
        {
            "item": "matter_coupling_output",
            "statement": "all matter observables are invariant under cell-scale gauge",
            "implication": "gauge fixing J_q=1 could be harmless",
            "why_not_enough": "current scaffold treats T and S as observable clock/routing factors",
        },
    ]


def coordinate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "coordinate_issue": "areal_radius",
            "statement": "spherical metric uses r through r^2 dOmega^2",
            "impact": "r is physically tied to surface area",
            "verdict": "cannot freely use radial coordinate to impose AB=1",
        },
        {
            "coordinate_issue": "schwarzschild_gauge",
            "statement": "AB=1 in Schwarzschild coordinates follows from vacuum GR equations",
            "impact": "using it as an input imports the target theory",
            "verdict": "forbidden_as_parent_derivation",
        },
        {
            "coordinate_issue": "ppn_coordinates",
            "statement": "PPN beta/gamma require a valid coordinate map",
            "impact": "areal-coordinate p=1 is not the whole PPN proof",
            "verdict": "beta_completion_still_open",
        },
        {
            "coordinate_issue": "observer_map_not_coordinate_map",
            "statement": "theta_0 and theta_1 define local measured intervals",
            "impact": "changing their product is physical unless a new gauge principle says otherwise",
            "verdict": "gauge_origin_not_currently_available",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_11_complete",
            "status": "pass" if source.get("readout") == "cell_current_origin_no_charge_obstruction" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "radial_coordinate_gauge_derives_AB1",
            "status": "fail",
            "detail": "areal radius already fixes the radial coordinate; AB=1 is not free gauge",
        },
        {
            "gate": "cell_scale_gauge_available",
            "status": "fail",
            "detail": "current scaffold makes T and S observable; no gauge-invariant matter map exists",
        },
        {
            "gate": "noether_identity_derives_R_AB_zero",
            "status": "fail",
            "detail": "Noether identity is not an algebraic constraint equation",
        },
        {
            "gate": "first_class_parent_constraint",
            "status": "open",
            "detail": "possible future route, but requires a full constrained parent action",
        },
        {
            "gate": "closure_route_available",
            "status": "pass",
            "detail": "lambda_R R_AB remains a clean local closure for benchmarking",
        },
        {
            "gate": "promotion_to_main_workbench_as_derived_GR",
            "status": "fail",
            "detail": "local reciprocity is not parent-derived",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "gauge_noether_origin_status",
            "status": "not_derived",
            "evidence": "coordinate gauge, cell-scale gauge, and Noether identity all fail in the current scaffold",
            "next_action": "demote local reciprocity to closure-only unless a new parent action is introduced",
        },
        {
            "decision": "local_branch_status",
            "status": "closure_only_GR_limit",
            "evidence": "R_AB=0 is a useful benchmark constraint but not a theorem",
            "next_action": "run PPN/local tests as a closure benchmark, not as derived proof",
        },
        {
            "decision": "programme_status",
            "status": "still_useful",
            "evidence": "the branch is now disciplined: it tells us exactly what a future parent action must beat",
            "next_action": "create 13-local-closure-PPN-benchmark.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Gauge/Noether origin audit for R_AB=0.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_11_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-gauge-noether-origin-audit"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    gauge_routes = gauge_route_rows()
    noether = noether_identity_rows()
    coordinates = coordinate_audit_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "gauge_origin_routes.csv", gauge_routes, list(gauge_routes[0].keys()))
    write_csv(results_dir / "noether_identity_limits.csv", noether, list(noether[0].keys()))
    write_csv(results_dir / "coordinate_gauge_audit.csv", coordinates, list(coordinates[0].keys()))
    write_csv(results_dir / "gauge_noether_origin_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "gauge_noether_origin_decision.csv", decisions, list(decisions[0].keys()))

    readout = "gauge_noether_origin_not_derived_closure_only"
    status = {
        "status": "complete_gauge_noether_origin_audit",
        "readout": readout,
        "recommendation": "treat_local_reciprocity_as_closure_benchmark_until_new_parent_action",
        "next_target": "13-local-closure-PPN-benchmark.md",
        "gauge_noether_derives_R_AB_zero": False,
        "first_class_constraint_parent_possible_but_absent": True,
        "closure_route_available": True,
        "local_GR_claim_status": "closure_only_not_derived",
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "gauge_origin_routes": str(results_dir / "gauge_origin_routes.csv"),
            "noether_identity_limits": str(results_dir / "noether_identity_limits.csv"),
            "coordinate_gauge_audit": str(results_dir / "coordinate_gauge_audit.csv"),
            "gauge_noether_origin_gates": str(results_dir / "gauge_noether_origin_gates.csv"),
            "gauge_noether_origin_decision": str(results_dir / "gauge_noether_origin_decision.csv"),
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
