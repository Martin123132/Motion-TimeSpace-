#!/usr/bin/env python3
"""Audit the auxiliary clock/cell variation route for u/D ownership."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "76_Ccoh_Bianchi_identity_attempt": Path("76-Ccoh-Bianchi-identity-attempt.md"),
    "77_local_route_gate": Path("77-local-route-demote-or-continue-gate.md"),
    "78_parent_uD_owner_contract": Path("78-parent-uD-owner-contract.md"),
    "78_decision": Path("runs/20260531-115848-parent-uD-owner-contract/results/decision.csv"),
    "78_selected_terms": Path("runs/20260531-115848-parent-uD-owner-contract/results/selected_contract_terms.csv"),
    "78_kill_tests": Path("runs/20260531-115848-parent-uD-owner-contract/results/kill_tests.csv"),
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


def variation_block_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "clock_gradient_definition",
            "variation": "u_mu = -nabla_mu T/sqrt(-X_T)",
            "euler_term": "E_T receives divergence of the projection of delta S/delta u_mu",
            "stress_result": "safe only if T has no standalone kinetic Lagrangian",
            "verdict": "conditional_pass",
        },
        {
            "block": "unit_vector_multiplier",
            "variation": "lambda_u(u_mu u^mu + 1)",
            "euler_term": "delta_u gives 2 lambda_u u^mu plus couplings",
            "stress_result": "lambda_u u_mu u_nu acts like dust unless lambda_u is constrained to vanish or cancels on shell",
            "verdict": "danger",
        },
        {
            "block": "cell_label_current",
            "variation": "J_D = star(dX1 wedge dX2 wedge dX3)",
            "euler_term": "E_XI is a conservation/no-flux equation for comoving labels",
            "stress_result": "topological if action depends only on conserved current constraints; dust-like if energy density depends on J_D norm",
            "verdict": "conditional_pass",
        },
        {
            "block": "domain_indicator",
            "variation": "L_u chi_D = 0 and n_mu J_D^mu = 0",
            "euler_term": "advection and boundary constraints, not a dynamical smoothing field",
            "stress_result": "safe only as constraint; unsafe if chi_D has gradient/phase-field energy",
            "verdict": "conditional_pass",
        },
        {
            "block": "Ccoh_memory_gate",
            "variation": "delta(C_coh L_mem)",
            "euler_term": "delta C_coh terms must be absorbed by E_T, E_XI, E_Q, and boundary currents",
            "stress_result": "not safe if proof freezes C_coh or ignores boundary terms",
            "verdict": "open",
        },
    ]


def stress_channel_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel": "physical_dust_energy",
            "how_it_appears": "reference cell labels carry an energy density rho_ref(n)",
            "ppn_risk": "adds Newtonian source and changes local gravity",
            "allowed_status": "forbidden_for_local_GR_route",
        },
        {
            "channel": "aether_khronon_kinetic_terms",
            "how_it_appears": "T or u has kinetic invariants such as (nabla u)^2",
            "ppn_risk": "preferred-frame modes and scalar/vector propagation",
            "allowed_status": "forbidden_unless_separately_bounded",
        },
        {
            "channel": "constraint_multiplier_residual",
            "how_it_appears": "lambda terms remain nonzero in T_munu on shell",
            "ppn_risk": "acts like pressureless or anisotropic reference stress",
            "allowed_status": "must_cancel_or_vanish",
        },
        {
            "channel": "phase_field_boundary_energy",
            "how_it_appears": "chi_D has gradient energy or smoothing length",
            "ppn_risk": "new boundary force or transition shell source",
            "allowed_status": "forbidden_in_parent_owner_route",
        },
        {
            "channel": "pure_constraint_or_topological_reference",
            "how_it_appears": "reference fields impose foliation/cell bookkeeping without physical energy density",
            "ppn_risk": "minimal if stress is on-shell zero or pure gauge",
            "allowed_status": "only_viable_channel",
        },
    ]


def noether_closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "E_u L_xi u",
            "attempted_replacement": "E_T L_xi T plus algebraic unit/projection constraint",
            "result": "works at identity level if u is derived from T",
            "remaining_gap": "must prove multiplier stress vanishes or is gauge/reference-only",
        },
        {
            "term": "E_D L_xi D",
            "attempted_replacement": "E_XI L_xi X^I or conserved current boundary equation",
            "result": "works at identity level if D is comoving/current-defined",
            "remaining_gap": "must prove no hidden smoothing/window choice enters C_coh",
        },
        {
            "term": "delta C_coh bulk exchange",
            "attempted_replacement": "functional derivatives of C_coh with respect to T, X^I, and g",
            "result": "formal route exists",
            "remaining_gap": "actual expression is complex and not yet computed",
        },
        {
            "term": "delta Ccoh boundary exchange",
            "attempted_replacement": "no-flux J_D boundary plus relative current",
            "result": "not closed",
            "remaining_gap": "boundary current still requires explicit cancellation",
        },
    ]


def limit_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "local_bound_quiet_bulk",
            "attempt_result": "possible_if_cell_current_stationary_and_Ccoh_functional_has_double_zero",
            "status": "conditional_open",
            "reason": "still needs proof that stationary bound domains follow from the same owner",
        },
        {
            "gate": "FLRW_active_background",
            "attempt_result": "possible_if_cosmological_comoving_labels_make_Ccoh_to_one",
            "status": "conditional_open",
            "reason": "must show same functional is active in FLRW without hand switching",
        },
        {
            "gate": "PPN_reference_stress",
            "attempt_result": "fails_for_dust_or_aether; survives_only_for_pure_constraint_topological_reference",
            "status": "narrow_pass_contract_only",
            "reason": "safe route exists only if auxiliary stress is on-shell zero or pure gauge",
        },
        {
            "gate": "boundary_transition",
            "attempt_result": "not_closed",
            "status": "fail_open",
            "reason": "surface current cancellation not derived",
        },
        {
            "gate": "full_local_GR_promotion",
            "attempt_result": "not_promoted",
            "status": "fail",
            "reason": "variation gives a route, not a completed stress-safe theorem",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "auxiliary_clock_cell_status",
            "status": "conditional_route_survives_only_as_pure_constraint_or_topological_reference",
            "evidence": "clock/cell variation can own E_u/E_D formally, but any dust/aether/phase-field stress is fatal",
            "next_action": "derive stress-free reference action contract and boundary current",
        },
        {
            "decision": "local_GR_status",
            "status": "not_derived",
            "evidence": "PPN-safe stress cancellation and boundary exchange are not proven",
            "next_action": "create 80-stress-free-reference-action-gate.md",
        },
        {
            "decision": "demotion_status",
            "status": "not_demoted_yet_but_narrowed",
            "evidence": "one viable channel remains: pure constraint/topological reference structure",
            "next_action": "kill route if that channel cannot be written without residual stress",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "conditional_route_survives_only_as_stress_free_reference",
        "key_metrics": {
            "variation_blocks": counts["variation_blocks"],
            "stress_channels": counts["stress_channels"],
            "noether_closure_rows": counts["noether_closure_attempt"],
            "limit_gates": counts["limit_gates"],
            "fatal_stress_channels": 4,
            "viable_channel": "pure_constraint_or_topological_reference",
        },
        "decision": decision_rows()[0],
        "next_target": "80-stress-free-reference-action-gate.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-auxiliary-clock-cell-variation-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "variation_blocks": (
            variation_block_rows(),
            ["block", "variation", "euler_term", "stress_result", "verdict"],
        ),
        "stress_channels": (
            stress_channel_rows(),
            ["channel", "how_it_appears", "ppn_risk", "allowed_status"],
        ),
        "noether_closure_attempt": (
            noether_closure_rows(),
            ["term", "attempted_replacement", "result", "remaining_gap"],
        ),
        "limit_gates": (
            limit_gate_rows(),
            ["gate", "attempt_result", "status", "reason"],
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
