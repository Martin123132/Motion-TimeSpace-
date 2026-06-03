#!/usr/bin/env python3
"""Audit whether phase-volume balance can justify the reciprocity constraint."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_07_STATUS = Path("runs/20260530-225112-nonpropagating-reciprocity-constraint/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def balance_rows() -> list[dict[str, Any]]:
    return [
        {
            "balance": "radial_clock_routing_cell",
            "constraint": "T sqrt(S)=1",
            "equivalent": "T^2 S=1",
            "p_result": 1.0,
            "status": "gives_GR_lane",
            "risk": "must justify why the conserved cell is radial t-r, not arbitrary",
        },
        {
            "balance": "clock_length_product",
            "constraint": "T S=1",
            "equivalent": "S=1/T",
            "p_result": 0.5,
            "status": "wrong_light_bending_lane",
            "risk": "gives half spatial routing",
        },
        {
            "balance": "full_3space_volume",
            "constraint": "T S^(3/2)=1",
            "equivalent": "S=T^(-2/3)",
            "p_result": 1.0 / 3.0,
            "status": "wrong_GR_lane",
            "risk": "shows generic volume preservation is not enough",
        },
        {
            "balance": "four_volume",
            "constraint": "T S^(3/2)=constant with angular factors",
            "equivalent": "same local exponent as full_3space_volume",
            "p_result": 1.0 / 3.0,
            "status": "wrong_GR_lane",
            "risk": "do not claim generic determinant preservation derives GR",
        },
        {
            "balance": "areal_radial_reciprocity",
            "constraint": "det(t-r block)=constant",
            "equivalent": "sqrt(A B)=1 -> A B=1",
            "p_result": 1.0,
            "status": "same_as_radial_clock_routing_cell",
            "risk": "needs areal radial gauge and physical reason for t-r block preservation",
        },
    ]


def derivation_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "load_splits_clock_capacity",
            "statement": "T^2=1-L follows from motion capacity budget",
            "status": "accepted_from_scaffold",
            "gap": "still needs parent action eventually",
        },
        {
            "step": "radial_null_transfer",
            "statement": "lost clock capacity must be carried by radial routing for local exterior propagation",
            "status": "plausible_physical_postulate",
            "gap": "not yet a variational theorem",
        },
        {
            "step": "phase_cell_preservation",
            "statement": "the local t-r clock-routing cell T sqrt(S) is conserved in vacuum",
            "status": "candidate_principle",
            "gap": "must derive from symplectic/phase-volume conservation, not assert",
        },
        {
            "step": "constraint_action",
            "statement": "lambda_R ln(T^2 S) enforces the conserved t-r cell",
            "status": "formalizes_candidate",
            "gap": "lambda_R origin remains a principle rather than theorem",
        },
        {
            "step": "GR_lane",
            "statement": "T sqrt(S)=1 -> S=1/T^2 -> p=1",
            "status": "derived_from_candidate_principle",
            "gap": "candidate principle not yet parent-derived",
        },
    ]


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_07_complete",
            "status": "pass" if source.get("readout") == "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "phase_volume_selects_p1",
            "status": "pass",
            "detail": "radial t-r cell preservation T sqrt(S)=1 gives T^2S=1 and p=1",
        },
        {
            "gate": "generic_volume_not_enough",
            "status": "pass",
            "detail": "full 3-space/four-volume preservation gives p=1/3, not GR",
        },
        {
            "gate": "radial_cell_origin_derived",
            "status": "fail",
            "detail": "why the conserved cell is specifically t-r is not yet derived",
        },
        {
            "gate": "lambda_R_parent_origin",
            "status": "fail",
            "detail": "phase-volume idea motivates lambda_R but does not derive it from parent action",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "route remains promising but still post-checkpoint only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "phase_volume_status",
            "status": "motivates_constraint_not_full_derivation",
            "evidence": "only radial t-r phase cell balance selects p=1; generic volume principles fail",
            "next_action": "derive radial-cell selection from local propagation/null-cone or Hamiltonian structure",
        },
        {
            "decision": "constraint_origin_status",
            "status": "open",
            "evidence": "lambda_R ln(T^2S) is now physically motivated but still not parent-derived",
            "next_action": "attempt Hamiltonian mass-shell derivation of the radial cell",
        },
        {
            "decision": "motion_load_route_status",
            "status": "promising_unpromoted",
            "evidence": "the route is cleaner than the old motion-field insertion but still needs one core theorem",
            "next_action": "write Hamiltonian radial-cell theorem attempt",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit phase-volume reciprocity origin.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_07_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-phase-volume-reciprocity-origin"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    balances = balance_rows()
    attempts = derivation_attempt_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "phase_volume_balance_options.csv", balances, list(balances[0].keys()))
    write_csv(results_dir / "phase_volume_derivation_attempt.csv", attempts, list(attempts[0].keys()))
    write_csv(results_dir / "phase_volume_origin_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "phase_volume_origin_decision.csv", decisions, list(decisions[0].keys()))

    readout = "phase_volume_reciprocity_motivated_not_parent_derived"
    status = {
        "status": "complete_phase_volume_reciprocity_origin",
        "readout": readout,
        "recommendation": "attempt_hamiltonian_radial_cell_derivation_next",
        "next_target": "09-hamiltonian-radial-cell-derivation.md",
        "radial_phase_cell_selects_p_equals_1": True,
        "generic_volume_principles_fail": True,
        "radial_cell_origin_derived": False,
        "constraint_parent_origin_derived": False,
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "phase_volume_balance_options": str(results_dir / "phase_volume_balance_options.csv"),
            "phase_volume_derivation_attempt": str(results_dir / "phase_volume_derivation_attempt.csv"),
            "phase_volume_origin_gates": str(results_dir / "phase_volume_origin_gates.csv"),
            "phase_volume_origin_decision": str(results_dir / "phase_volume_origin_decision.csv"),
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
