#!/usr/bin/env python3
"""Audit whether Hamiltonian structure derives the radial reciprocity cell."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_08_STATUS = Path("runs/20260530-225432-phase-volume-reciprocity-origin/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cell_factor(load: float, p_value: float) -> float:
    return (1.0 - load) ** ((1.0 - p_value) / 2.0)


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "radial_mass_shell",
            "statement": "-E^2/T^2 + p_r^2/S + m^2 c^2 = 0",
            "cell_condition": "none",
            "p_result": "undetermined",
            "status": "does_not_derive_p",
            "reason": "local dispersion fixes E/T and p_r/sqrt(S), but does not relate T to S",
        },
        {
            "candidate": "radial_null_speed",
            "statement": "dr/dt = c T/sqrt(S)",
            "cell_condition": "none",
            "p_result": "undetermined",
            "status": "does_not_derive_p",
            "reason": "null propagation gives an effective speed for any S_p; it is not a reciprocity theorem",
        },
        {
            "candidate": "newtonian_slow_particle_limit",
            "statement": "T^2 = 1 - L gives the Newtonian potential in g_tt",
            "cell_condition": "none_at_first_order",
            "p_result": "undetermined",
            "status": "does_not_derive_p",
            "reason": "the Newtonian acceleration fixes the clock/load term first; gamma/routing remains open",
        },
        {
            "candidate": "radial_configuration_cell",
            "statement": "d tau d ell = dt dr",
            "cell_condition": "T sqrt(S)=1",
            "p_result": "1",
            "status": "conditional_p_equals_1",
            "reason": "separate preservation of the t-r configuration cell forces the GR lane",
        },
        {
            "candidate": "radial_energy_momentum_cell",
            "statement": "dE_local dp_local = dE dp_r",
            "cell_condition": "1/(T sqrt(S))=1",
            "p_result": "1",
            "status": "conditional_p_equals_1",
            "reason": "dual preservation of the radial energy-momentum cell is equivalent to T sqrt(S)=1",
        },
        {
            "candidate": "full_radial_phase_cell",
            "statement": "(d tau d ell)(dE_local dp_local) = dt dr dE dp_r",
            "cell_condition": "automatic",
            "p_result": "any_p",
            "status": "fails_as_derivation",
            "reason": "the T sqrt(S) and 1/(T sqrt(S)) Jacobians cancel for every p",
        },
        {
            "candidate": "liouville_theorem",
            "statement": "canonical phase volume is preserved by Hamiltonian flow",
            "cell_condition": "automatic_in_canonical_variables",
            "p_result": "any_p",
            "status": "fails_as_derivation",
            "reason": "ordinary symplectic conservation is true without selecting T sqrt(S)=1",
        },
        {
            "candidate": "canonical_observer_map",
            "statement": "theta = -E dt + p_r dr = -E_hat theta^0 + p_hat theta^1",
            "cell_condition": "requires_extra_observer_map_rule",
            "p_result": "undetermined",
            "status": "promising_but_open",
            "reason": "the coframe rewrite is clean, but radial variation of T supplies connection terms rather than p=1",
        },
    ]


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "metric_scaffold",
            "equation": "ds^2 = -T^2 c^2 dt^2 + S dr^2 + r^2 dOmega^2",
            "status": "working_scaffold",
            "gap": "parent action still open",
        },
        {
            "step": "motion_load_clock",
            "equation": "T^2 = 1 - L",
            "status": "accepted_from_motion_load_route",
            "gap": "load law origin still ultimately needed",
        },
        {
            "step": "routing_family",
            "equation": "S_p = (1-L)^(-p)",
            "status": "audit_dial",
            "gap": "p must be derived, not fitted",
        },
        {
            "step": "local_mass_shell",
            "equation": "-(E/T)^2 + (p_r/sqrt(S))^2 + m^2 c^2 = 0",
            "status": "derived_inside_scaffold",
            "gap": "does not itself link T and S",
        },
        {
            "step": "separate_radial_cell",
            "equation": "T sqrt(S)=1",
            "status": "sufficient_for_GR_lane",
            "gap": "separate cell preservation is an extra principle",
        },
        {
            "step": "full_phase_cell",
            "equation": "(T sqrt(S))*(1/(T sqrt(S)))=1",
            "status": "automatic_identity",
            "gap": "ordinary Hamiltonian/Liouville structure cannot select p=1",
        },
        {
            "step": "required_parent_theorem",
            "equation": "observer map must preserve the radial t-r cell separately, or impose lambda_R ln(T^2 S)",
            "status": "open_contract",
            "gap": "not yet derived from an action",
        },
    ]


def weak_field_cell_rows() -> list[dict[str, Any]]:
    load = 1.0e-6
    rows: list[dict[str, Any]] = []
    for p_value in (0.0, 0.5, 1.0, 1.00001, 2.0):
        factor = cell_factor(load, p_value)
        rows.append(
            {
                "p": p_value,
                "T_sqrt_S_exact_at_L_1e_minus_6": factor,
                "linear_coefficient_in_L": (p_value - 1.0) / 2.0,
                "gamma_proxy": p_value,
                "gamma_minus_1_proxy": p_value - 1.0,
                "status": "reciprocal_cell" if math.isclose(p_value, 1.0) else "cell_drift",
            }
        )
    return rows


def gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_08_complete",
            "status": "pass" if source.get("readout") == "phase_volume_reciprocity_motivated_not_parent_derived" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "mass_shell_written",
            "status": "pass",
            "detail": "static radial Hamiltonian gives local E/T and p_r/sqrt(S)",
        },
        {
            "gate": "separate_radial_cell_selects_p1",
            "status": "pass",
            "detail": "T sqrt(S)=1 implies p=1 for variable load L",
        },
        {
            "gate": "hamiltonian_law_derives_separate_cell",
            "status": "fail",
            "detail": "full phase-space preservation is automatic and therefore does not select p=1",
        },
        {
            "gate": "null_dispersion_derives_p1",
            "status": "fail",
            "detail": "null dispersion gives dr/dt=cT/sqrt(S) for any p",
        },
        {
            "gate": "observer_map_parent_origin",
            "status": "fail",
            "detail": "need a parent action or observer-map theorem that preserves the radial t-r cell separately",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "detail": "Hamiltonian route sharpens the target but does not promote the motion-load branch",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "hamiltonian_route_status",
            "status": "sharpened_not_derived",
            "evidence": "mass shell and Liouville structure do not force T sqrt(S)=1",
            "next_action": "write an observer-map/symplectic contract for any future parent action",
        },
        {
            "decision": "strongest_viable_route",
            "status": "separate_radial_observer_cell_constraint",
            "evidence": "it gives p=1 exactly while generic phase volume remains too weak",
            "next_action": "derive why the t-r cell is separately conserved rather than merely full phase volume",
        },
        {
            "decision": "local_GR_branch",
            "status": "conditional_promising_not_claimable",
            "evidence": "p=1 is clean once reciprocity is imposed, but reciprocity is still a closure/constraint",
            "next_action": "do not edit main workbench; continue post-checkpoint only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Hamiltonian radial-cell derivation audit.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_08_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-hamiltonian-radial-cell-derivation"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = candidate_rows()
    derivation = derivation_chain_rows()
    weak_field = weak_field_cell_rows()
    gates = gate_rows(source)
    decisions = decision_rows()

    write_csv(results_dir / "hamiltonian_radial_cell_candidates.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "hamiltonian_derivation_chain.csv", derivation, list(derivation[0].keys()))
    write_csv(results_dir / "weak_field_cell_expansion.csv", weak_field, list(weak_field[0].keys()))
    write_csv(results_dir / "hamiltonian_radial_cell_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "hamiltonian_radial_cell_decision.csv", decisions, list(decisions[0].keys()))

    readout = "hamiltonian_radial_cell_sharpened_not_parent_derived"
    status = {
        "status": "complete_hamiltonian_radial_cell_derivation_audit",
        "readout": readout,
        "recommendation": "write_observer_map_symplectic_contract_next",
        "next_target": "10-observer-map-symplectic-contract.md",
        "p_equals_1_from_separate_radial_cell": True,
        "p_equals_1_from_generic_hamiltonian_or_liouville": False,
        "mass_shell_derives_T_S_relation": False,
        "observer_map_parent_origin_derived": False,
        "promotion_to_main_workbench_allowed": False,
        "outputs": {
            "hamiltonian_radial_cell_candidates": str(results_dir / "hamiltonian_radial_cell_candidates.csv"),
            "hamiltonian_derivation_chain": str(results_dir / "hamiltonian_derivation_chain.csv"),
            "weak_field_cell_expansion": str(results_dir / "weak_field_cell_expansion.csv"),
            "hamiltonian_radial_cell_gates": str(results_dir / "hamiltonian_radial_cell_gates.csv"),
            "hamiltonian_radial_cell_decision": str(results_dir / "hamiltonian_radial_cell_decision.csv"),
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
