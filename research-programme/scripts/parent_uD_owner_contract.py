#!/usr/bin/env python3
"""Build the checkpoint-78 parent u/D owner contract."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "75_Ccoh_parent_variation_contract": Path("75-Ccoh-parent-variation-contract.md"),
    "76_Ccoh_Bianchi_identity_attempt": Path("76-Ccoh-Bianchi-identity-attempt.md"),
    "77_local_route_demote_gate": Path("77-local-route-demote-or-continue-gate.md"),
    "77_decision": Path("runs/20260531-115514-local-route-demote-or-continue-gate/results/decision.csv"),
    "77_bounded_attempt_gates": Path("runs/20260531-115514-local-route-demote-or-continue-gate/results/bounded_attempt_gates.csv"),
    "77_kill_conditions": Path("runs/20260531-115514-local-route-demote-or-continue-gate/results/kill_conditions.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def owner_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "external_observer_and_window",
            "u_owner": "chosen frame",
            "D_owner": "chosen averaging window",
            "strength": "simple diagnostic closure",
            "fatal_problem": "violates checkpoint-77 kill conditions",
            "verdict": "reject_as_field_theory",
        },
        {
            "candidate": "Einstein_aether_or_khronon",
            "u_owner": "unit timelike vector or scalar clock with kinetic terms",
            "D_owner": "not automatically owned",
            "strength": "true variational owner for u",
            "fatal_problem": "propagating local mode and PPN/fifth-force risk unless heavily tuned",
            "verdict": "reject_for_local_GR_route",
        },
        {
            "candidate": "Brown_Kuchar_dust_reference",
            "u_owner": "dust proper-time field",
            "D_owner": "comoving material coordinates",
            "strength": "owns u and D together",
            "fatal_problem": "physical dust stress unless reference sector is auxiliary or decoupled",
            "verdict": "use_as_template_not_as_physical_dust",
        },
        {
            "candidate": "auxiliary_clock_cell_reference",
            "u_owner": "constraint clock T with u_mu = -grad_mu T / sqrt(-grad T squared)",
            "D_owner": "comoving cell labels X^I or equivalent conserved 3-form current",
            "strength": "owns both missing variables while allowing no-propagating-stress limit",
            "fatal_problem": "must prove auxiliary sector stress cancels or is pure constraint",
            "verdict": "selected_contract_route",
        },
        {
            "candidate": "pure_topological_relative_current",
            "u_owner": "not owned directly",
            "D_owner": "relative cycle/current closure",
            "strength": "good conservation bookkeeping",
            "fatal_problem": "does not select physical observer congruence or amplitude",
            "verdict": "support_only",
        },
    ]


def selected_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "clock_field_T",
            "role": "owns local time direction and observer congruence",
            "contract_equation": "u_mu = -nabla_mu T / sqrt(-X_T), X_T = g^ab nabla_a T nabla_b T < 0",
            "stress_guard": "T must enter as constraint/reference data, not as a propagating khronon with free kinetic energy",
        },
        {
            "object": "unit_constraint_lambda_u",
            "role": "enforces u_mu u^mu = -1 if u is kept as independent variable",
            "contract_equation": "delta_lambda_u S gives u_mu u^mu + 1 = 0",
            "stress_guard": "lambda_u terms must vanish or combine into already-present matter/reference equations on shell",
        },
        {
            "object": "cell_labels_XI_or_3form_JD",
            "role": "owns D as a comoving domain rather than arbitrary smoothing",
            "contract_equation": "J_D^mu = star(dX1 wedge dX2 wedge dX3), nabla_mu J_D^mu = 0",
            "stress_guard": "cell-label sector must be topological/auxiliary or stress-bounded",
        },
        {
            "object": "domain_indicator_chi_D",
            "role": "represents the selected cell/domain",
            "contract_equation": "L_u chi_D = 0 plus boundary flux n_mu J_D^mu = 0",
            "stress_guard": "no threshold/smoothing scale can be added by hand",
        },
        {
            "object": "memory_field_Q",
            "role": "carries the MTS memory/load sector",
            "contract_equation": "E_Q = delta S_mem/delta Q = 0",
            "stress_guard": "memory exchange with C_coh must close through E_T/E_XI/E_Q, not by freezing C_coh",
        },
    ]


def noether_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint_76_term": "E_u L_xi u",
            "parent_replacement": "E_T L_xi T plus constraint projection terms",
            "closure_condition": "u is derived from T or constrained by a parent equation; E_u is not arbitrary",
            "status": "contract_not_derived",
        },
        {
            "checkpoint_76_term": "E_D L_xi D",
            "parent_replacement": "E_XI L_xi X^I or E_J L_xi J_D",
            "closure_condition": "domain boundaries are comoving/current-defined and varied in the action",
            "status": "contract_not_derived",
        },
        {
            "checkpoint_76_term": "boundary_exchange",
            "parent_replacement": "relative boundary current plus no-flux cell condition",
            "closure_condition": "surface terms cancel without imposing fixed C_coh by hand",
            "status": "open",
        },
        {
            "checkpoint_76_term": "perturbation_exchange",
            "parent_replacement": "linearized E_T/E_XI/E_Q equations",
            "closure_condition": "no extra unsuppressed scalar/vector response in local weak fields",
            "status": "open",
        },
    ]


def limit_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "limit": "local_bound_quiet_bulk",
            "required_condition": "D is a stationary comoving bound cell, average expansion tends to zero, and C_coh tends to zero on shell",
            "failure_mode": "quietness appears only because D was chosen around the answer",
            "status": "must_test_in_79",
        },
        {
            "limit": "FLRW_active_background",
            "required_condition": "cell labels comove with the cosmological congruence, shear/vorticity vanish, and C_coh tends to one",
            "failure_mode": "same owner that quiets local cells suppresses FLRW memory too",
            "status": "must_test_in_79",
        },
        {
            "limit": "PPN_local_residual",
            "required_condition": "reference sector adds no measurable PPN stress, slip, or preferred-frame signal above bound",
            "failure_mode": "clock/cell fields behave like aether, dust, or fifth-force matter",
            "status": "must_bound_before_promotion",
        },
        {
            "limit": "boundary_transition",
            "required_condition": "transition from bound cells to coherent FLRW regions has controlled surface current",
            "failure_mode": "boundary layer becomes the hidden source of the effect",
            "status": "open",
        },
    ]


def kill_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "hand_chosen_clock",
            "question": "Can T be shifted or chosen freely to force C_coh?",
            "pass_condition": "No; T is fixed by a variational/reference equation or gauge-invariant matter rest frame.",
        },
        {
            "test": "hand_chosen_domain",
            "question": "Can X^I or chi_D be chosen after seeing the target local/FLRW behavior?",
            "pass_condition": "No; cell labels or current are determined before fitting the branch.",
        },
        {
            "test": "frozen_Ccoh_escape",
            "question": "Does the conservation proof require delta C_coh = 0?",
            "pass_condition": "No; delta C_coh terms are absorbed by E_T/E_XI/E_Q or cancel as boundary terms.",
        },
        {
            "test": "new_local_stress",
            "question": "Does the owner sector source a new weak-field potential?",
            "pass_condition": "No; stress is auxiliary/topological/on-shell zero or below a derived bound.",
        },
        {
            "test": "same_owner_two_limits",
            "question": "Does one owner produce both local silence and FLRW activity?",
            "pass_condition": "Yes; no branch-specific hand switch is introduced.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "parent_uD_owner_status",
            "status": "contract_route_found_not_derived",
            "evidence": "auxiliary clock plus comoving cell labels can own u and D at contract level",
            "next_action": "attempt explicit variation and stress audit",
        },
        {
            "decision": "selected_route",
            "status": "auxiliary_clock_cell_reference",
            "evidence": "it is the only candidate that owns u and D while not immediately adding a propagating PPN field",
            "next_action": "create 79-auxiliary-clock-cell-variation-attempt.md",
        },
        {
            "decision": "claim_status",
            "status": "no_local_GR_derivation_yet",
            "evidence": "contract still needs variation, boundary closure, and PPN stress proof",
            "next_action": "keep local route demoted until those gates pass",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "parent_uD_contract_route_found_not_derived",
        "key_metrics": {
            "owner_candidates": counts["owner_candidates"],
            "selected_contract_terms": counts["selected_contract_terms"],
            "noether_map_rows": counts["noether_identity_map"],
            "limit_conditions": counts["limit_conditions"],
            "kill_tests": counts["kill_tests"],
            "selected_route": "auxiliary_clock_cell_reference",
        },
        "decision": decision_rows()[0],
        "next_target": "79-auxiliary-clock-cell-variation-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-parent-uD-owner-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "owner_candidates": (
            owner_candidate_rows(),
            ["candidate", "u_owner", "D_owner", "strength", "fatal_problem", "verdict"],
        ),
        "selected_contract_terms": (
            selected_contract_rows(),
            ["object", "role", "contract_equation", "stress_guard"],
        ),
        "noether_identity_map": (
            noether_map_rows(),
            ["checkpoint_76_term", "parent_replacement", "closure_condition", "status"],
        ),
        "limit_conditions": (
            limit_condition_rows(),
            ["limit", "required_condition", "failure_mode", "status"],
        ),
        "kill_tests": (
            kill_test_rows(),
            ["test", "question", "pass_condition"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
