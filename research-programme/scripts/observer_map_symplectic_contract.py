#!/usr/bin/env python3
"""Write and audit the observer-map contract needed for local GR reciprocity."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_09_STATUS = Path("runs/20260530-225948-hamiltonian-radial-cell-derivation/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def observer_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "clock_load_coframe",
            "definition": "theta_0 = T c dt",
            "role": "maps coordinate time to local clock interval",
            "required_status": "primitive_or_parent_derived",
        },
        {
            "object": "radial_routing_coframe",
            "definition": "theta_1 = sqrt(S) dr",
            "role": "maps coordinate radial step to local routed radial interval",
            "required_status": "primitive_or_parent_derived",
        },
        {
            "object": "local_energy",
            "definition": "E_hat = E/T",
            "role": "dual to theta_0",
            "required_status": "derived_from_coframe_duality",
        },
        {
            "object": "local_radial_momentum",
            "definition": "p_hat = p_r/sqrt(S)",
            "role": "dual to theta_1",
            "required_status": "derived_from_coframe_duality",
        },
        {
            "object": "radial_configuration_cell",
            "definition": "J_q = T sqrt(S)",
            "role": "the separate observer-cell whose preservation selects p=1",
            "required_status": "must_be_parent_derived",
        },
        {
            "object": "radial_momentum_cell",
            "definition": "J_p = 1/(T sqrt(S))",
            "role": "dual cell; cancels J_q in full phase volume",
            "required_status": "not_sufficient_by_itself",
        },
        {
            "object": "reciprocal_strain",
            "definition": "R_AB = ln(T^2 S) = 2 ln(J_q)",
            "role": "zero iff T sqrt(S)=1 and AB=1",
            "required_status": "constraint_variable_or_eliminated_mode",
        },
    ]


def contract_gate_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_09_complete",
            "status": "pass" if source.get("readout") == "hamiltonian_radial_cell_sharpened_not_parent_derived" else "fail",
            "contract_requirement": "stage 09 must have isolated the Hamiltonian obstruction",
            "current_evidence": str(source.get("readout")),
        },
        {
            "gate": "coframe_defined",
            "status": "pass",
            "contract_requirement": "define theta_0=T c dt and theta_1=sqrt(S) dr before any PPN claims",
            "current_evidence": "observer map table written",
        },
        {
            "gate": "mass_shell_defined",
            "status": "pass",
            "contract_requirement": "local mass shell must use E/T and p_r/sqrt(S)",
            "current_evidence": "stage 09 and observer map agree",
        },
        {
            "gate": "separate_cell_equation",
            "status": "pass",
            "contract_requirement": "parent equations must imply R_AB=ln(T^2 S)=0 in local vacuum",
            "current_evidence": "contract identifies exact required Euler-Lagrange output",
        },
        {
            "gate": "not_generic_liouville",
            "status": "pass",
            "contract_requirement": "do not count full phase-volume preservation as a derivation",
            "current_evidence": "J_q J_p=1 is automatic for all p",
        },
        {
            "gate": "no_reciprocal_hair",
            "status": "pass",
            "contract_requirement": "vacuum must not carry a free Q_R/r mode in R_AB",
            "current_evidence": "kinetic reciprocal-strain route already demoted",
        },
        {
            "gate": "source_neutrality",
            "status": "open",
            "contract_requirement": "compact sources must not inject boundary reciprocal charge Pi_R",
            "current_evidence": "previous neutrality was conditional, not parent-derived",
        },
        {
            "gate": "lambda_origin",
            "status": "open",
            "contract_requirement": "lambda_R must arise from a parent constraint, gauge redundancy, or conserved cell current",
            "current_evidence": "lambda_R is currently a clean closure device, not derived",
        },
        {
            "gate": "beta_completion",
            "status": "open",
            "contract_requirement": "prove beta=1 in a valid PPN coordinate map, not only gamma=1",
            "current_evidence": "p=1 gives gamma lane; beta remains completion gate",
        },
        {
            "gate": "no_GR_import",
            "status": "open",
            "contract_requirement": "derive without assuming Schwarzschild form or Einstein vacuum equations",
            "current_evidence": "contract states the prohibition; no parent proof yet",
        },
        {
            "gate": "promotion_to_main_workbench",
            "status": "fail",
            "contract_requirement": "all open gates must close before promotion",
            "current_evidence": "contract written, not satisfied",
        },
    ]


def candidate_parent_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "hard_multiplier",
            "schematic_action": "S_R = integral lambda_R ln(T^2 S)",
            "derives_R_AB_zero": "yes_by_delta_lambda",
            "hair_risk": "none",
            "verdict": "closure_only_until_lambda_origin_is_derived",
        },
        {
            "candidate": "cell_current_constraint",
            "schematic_action": "S_R = integral lambda_R div(J_cell)",
            "derives_R_AB_zero": "not_without_boundary_theorem",
            "hair_risk": "low_if_current_has_no_charge",
            "verdict": "promising_parent_route_but_unproven",
        },
        {
            "candidate": "gauge_redundancy",
            "schematic_action": "radial cell is fixed by a local redundancy of observer splitting",
            "derives_R_AB_zero": "possible_only_if_gauge_fixing_has_observable_equivalence",
            "hair_risk": "none_if_true_gauge",
            "verdict": "dangerous_unless_not_just_coordinate_choice",
        },
        {
            "candidate": "kinetic_reciprocal_strain",
            "schematic_action": "S_R = integral 0.5 W (partial R_AB)^2",
            "derives_R_AB_zero": "no",
            "hair_risk": "Q_R/r_exterior_mode",
            "verdict": "reject_as_local_GR_parent",
        },
        {
            "candidate": "generic_liouville",
            "schematic_action": "canonical Hamiltonian phase-volume preservation",
            "derives_R_AB_zero": "no",
            "hair_risk": "not_applicable",
            "verdict": "insufficient_because_true_for_any_p",
        },
        {
            "candidate": "einstein_vacuum_import",
            "schematic_action": "assume G^t_t=G^r_r or Schwarzschild AB=1",
            "derives_R_AB_zero": "yes_but_imported",
            "hair_risk": "hidden_GR_assumption",
            "verdict": "forbidden_for_MTS_derivation",
        },
    ]


def ppn_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable_gate": "Newtonian_limit",
            "required_result": "T^2 = 1 - 2U/c^2 + correct weak-field acceleration",
            "why_it_matters": "recovers the previous theory in the same way GR recovers Newton locally",
            "current_status": "partially_passed_from_motion_load_clock",
        },
        {
            "observable_gate": "PPN_gamma",
            "required_result": "gamma - 1 = 0 within local bound after R_AB=0",
            "why_it_matters": "controls light bending and Shapiro",
            "current_status": "conditional_pass_if_T2S_equals_1",
        },
        {
            "observable_gate": "PPN_beta",
            "required_result": "beta - 1 = 0 in a valid PPN coordinate construction",
            "why_it_matters": "controls nonlinear solar-system dynamics including perihelion terms",
            "current_status": "open_completion_gate",
        },
        {
            "observable_gate": "equivalence_principle",
            "required_result": "all matter sectors couple to the same observer coframe",
            "why_it_matters": "prevents species-dependent clock/load response",
            "current_status": "not_yet_a_parent_action",
        },
        {
            "observable_gate": "conservation_identity",
            "required_result": "field equations imply a Bianchi-like consistency identity",
            "why_it_matters": "prevents local stress-energy nonconservation",
            "current_status": "not_yet_derived",
        },
    ]


def failure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_mode": "closure_smuggling",
            "symptom": "write lambda_R ln(T^2S) and call it derived",
            "required_response": "label closure-only until lambda origin is proved",
        },
        {
            "failure_mode": "liouville_overclaim",
            "symptom": "claim phase-volume preservation selects p=1",
            "required_response": "reject because full radial phase volume is automatic for every p",
        },
        {
            "failure_mode": "GR_import",
            "symptom": "use Schwarzschild AB=1 or Einstein vacuum equations as premise",
            "required_response": "reject as circular for a fundamental MTS derivation",
        },
        {
            "failure_mode": "reciprocal_hair",
            "symptom": "allow kinetic R_AB with exterior Q_R/r",
            "required_response": "derive Q_R=0 or demote branch",
        },
        {
            "failure_mode": "gamma_only_win",
            "symptom": "prove p=1 but skip beta/conservation/matter coupling",
            "required_response": "keep as local gamma branch, not full GR reduction",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "contract_status",
            "status": "written_not_satisfied",
            "evidence": "exact gates for R_AB=0, no hair, lambda origin, beta, and no GR import are now explicit",
            "next_action": "attempt a cell-current or gauge-origin theorem for lambda_R",
        },
        {
            "decision": "allowed_current_claim",
            "status": "conditional_local_GR_route",
            "evidence": "if the parent action gives R_AB=0, p=1 follows cleanly",
            "next_action": "do not promote to main workbench yet",
        },
        {
            "decision": "best_next_target",
            "status": "cell_current_origin_attempt",
            "evidence": "hard multiplier is too closure-like; kinetic strain has hair; generic Liouville is too weak",
            "next_action": "create 11-cell-current-origin-attempt.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Observer-map symplectic contract audit.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_09_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-observer-map-symplectic-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    observer_map = observer_map_rows()
    gates = contract_gate_rows(source)
    candidates = candidate_parent_rows()
    ppn = ppn_requirement_rows()
    failures = failure_mode_rows()
    decisions = decision_rows()

    write_csv(results_dir / "observer_map_definitions.csv", observer_map, list(observer_map[0].keys()))
    write_csv(results_dir / "observer_map_contract_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "candidate_parent_routes.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "ppn_completion_requirements.csv", ppn, list(ppn[0].keys()))
    write_csv(results_dir / "contract_failure_modes.csv", failures, list(failures[0].keys()))
    write_csv(results_dir / "observer_map_contract_decision.csv", decisions, list(decisions[0].keys()))

    open_gates = [row["gate"] for row in gates if row["status"] == "open"]
    failed_gates = [row["gate"] for row in gates if row["status"] == "fail"]
    readout = "observer_map_contract_written_not_satisfied"
    status = {
        "status": "complete_observer_map_symplectic_contract",
        "readout": readout,
        "recommendation": "attempt_cell_current_origin_next",
        "next_target": "11-cell-current-origin-attempt.md",
        "contract_written": True,
        "parent_contract_satisfied": False,
        "promotion_to_main_workbench_allowed": False,
        "open_gates": open_gates,
        "failed_gates": failed_gates,
        "outputs": {
            "observer_map_definitions": str(results_dir / "observer_map_definitions.csv"),
            "observer_map_contract_gates": str(results_dir / "observer_map_contract_gates.csv"),
            "candidate_parent_routes": str(results_dir / "candidate_parent_routes.csv"),
            "ppn_completion_requirements": str(results_dir / "ppn_completion_requirements.csv"),
            "contract_failure_modes": str(results_dir / "contract_failure_modes.csv"),
            "observer_map_contract_decision": str(results_dir / "observer_map_contract_decision.csv"),
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
