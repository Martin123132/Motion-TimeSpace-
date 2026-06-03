#!/usr/bin/env python3
"""Attempt Noether/Bianchi closure for S_gate = C_coh L_mem."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "69_memory_gate_doc": Path("69-minimal-memory-gate-variation-attempt.md"),
    "70_Ccoh_variation_doc": Path("70-Ccoh-variation-and-boundary-current-audit.md"),
    "75_Ccoh_contract_doc": Path("75-Ccoh-parent-variation-contract.md"),
    "75_status": Path("runs/20260531-114606-Ccoh-parent-variation-contract/status.json"),
    "75_dependencies": Path("runs/20260531-114606-Ccoh-parent-variation-contract/results/dependency_contract.csv"),
    "75_variation_obligations": Path("runs/20260531-114606-Ccoh-parent-variation-contract/results/variation_obligations.csv"),
    "75_gates": Path("runs/20260531-114606-Ccoh-parent-variation-contract/results/gate_results.csv"),
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


def noether_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "S_gate = integral sqrt(-g) C_coh[g,u,D] L_mem[g,u,Q,...]",
            "identity_piece": "T_gate = C_coh T_mem + L_mem T_Ccoh + mixed field-equation terms",
            "status": "setup",
            "failure_mode": "none",
        },
        {
            "step": 2,
            "statement": "diffeomorphism variation gives nabla_mu T_gate^munu = E_Q L_xi Q + E_u L_xi u + E_D L_xi D + E_mem L_xi fields",
            "identity_piece": "conservation closes only if Q,u,D equations are included",
            "status": "formal_Noether",
            "failure_mode": "missing parent equations",
        },
        {
            "step": 3,
            "statement": "If C_coh is composite from varied fields, delta C_coh terms are not anomalies",
            "identity_piece": "they are part of E_u and E_D exchange",
            "status": "conditional_pass",
            "failure_mode": "only works with real E_u/E_D",
        },
        {
            "step": 4,
            "statement": "If u and D are constrained auxiliary fields, their multiplier equations must cancel L_mem delta C_coh",
            "identity_piece": "exchange can be bookkeeping, not independent stress",
            "status": "conditional",
            "failure_mode": "multipliers impose rather than derive frame/domain",
        },
        {
            "step": 5,
            "statement": "If C_coh is frozen or diagnostic, S_gate=C_coh L_mem is not a variationally conserved source",
            "identity_piece": "Bianchi fails except in constant branches",
            "status": "fail_for_frozen_Ccoh",
            "failure_mode": "fake conservation",
        },
        {
            "step": 6,
            "statement": "Explicit local-to-FLRW boundary term remains uncomputed",
            "identity_piece": "J_boundary/J_rel required for nonconstant D/C_coh",
            "status": "open",
            "failure_mode": "uncontrolled exchange at boundary",
        },
    ]


def branch_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "quiet_local_bulk",
            "Ccoh": "0 constant",
            "identity_status": "passes at bulk-contract level",
            "reason": "S_gate=0 and delta Ccoh can vanish on shell in ideal quiet bulk",
            "remaining_gap": "derive local parent solution",
        },
        {
            "branch": "stationary_bound_interior",
            "Ccoh": "low/constant",
            "identity_status": "passes conditionally",
            "reason": "exchange suppressed if domain average stationary and E_D holds",
            "remaining_gap": "derive D and averaging equation",
        },
        {
            "branch": "FLRW_background",
            "Ccoh": "1 constant",
            "identity_status": "passes background contract",
            "reason": "S_gate=L_mem and Ccoh variation vanishes by symmetry for background",
            "remaining_gap": "L_mem background stress still underived",
        },
        {
            "branch": "FLRW_perturbations",
            "Ccoh": "1 + delta Ccoh",
            "identity_status": "open/fail_currently",
            "reason": "delta Ccoh terms require perturbative E_u/E_D and boundary response",
            "remaining_gap": "perturbation equations missing",
        },
        {
            "branch": "local_to_FLRW_boundary",
            "Ccoh": "varies",
            "identity_status": "fail_open",
            "reason": "J_boundary/J_rel not parent-derived",
            "remaining_gap": "main obstruction",
        },
    ]


def closure_options_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "full_variational_owner",
            "what_closes": "E_g,E_u,E_D,E_Q jointly close Noether identity",
            "status": "best_but_not_available",
            "cost": "requires deriving parent equations for u and D",
            "verdict": "continue_only_if_parent_owner_constructed",
        },
        {
            "option": "constrained_auxiliary_owner",
            "what_closes": "multiplier equations absorb Ccoh exchange",
            "status": "conditional",
            "cost": "may impose frame/domain rather than derive",
            "verdict": "live_closure_route",
        },
        {
            "option": "pure_diagnostic_Ccoh",
            "what_closes": "nothing inside action; Ccoh used after solving fields",
            "status": "safe_demotion",
            "cost": "cannot gate memory action or derive local GR",
            "verdict": "demote_if_owner_fails",
        },
        {
            "option": "frozen_action_Ccoh",
            "what_closes": "only constant branches by assumption",
            "status": "rejected",
            "cost": "violates Bianchi for variable Ccoh",
            "verdict": "not_allowed",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "Noether_structure_identified",
            "status": "pass",
            "detail": "Ccoh variation can be part of field equations if u,D,Q are varied",
        },
        {
            "gate": "frozen_Ccoh_rejected_again",
            "status": "pass",
            "detail": "frozen Ccoh in action fails for nonconstant branches",
        },
        {
            "gate": "quiet_bulk_identity",
            "status": "pass_conditional",
            "detail": "constant Ccoh=0 bulk can be conserved at contract level",
        },
        {
            "gate": "FLRW_background_identity",
            "status": "pass_contract",
            "detail": "constant Ccoh=1 background reduces to L_mem branch",
        },
        {
            "gate": "boundary_identity",
            "status": "fail_open",
            "detail": "nonconstant Ccoh boundary exchange current is not derived",
        },
        {
            "gate": "perturbation_identity",
            "status": "fail_open",
            "detail": "delta Ccoh perturbation response lacks E_u/E_D equations",
        },
        {
            "gate": "full_Bianchi_closure",
            "status": "fail",
            "detail": "requires parent u/D/Q equations not yet constructed",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "Bianchi closure not complete",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a failed/conditional conservation attempt, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "Ccoh_Bianchi_status",
            "status": "partial_Noether_structure_but_no_full_closure",
            "evidence": "Ccoh exchange can be conserved only if u,D,Q parent equations exist; boundary and perturbation branches fail/open now",
            "next_action": "local route must be demoted to closure unless parent u/D owner is constructed",
        },
        {
            "decision": "local_route_status",
            "status": "demote_or_construct_parent_uD_owner",
            "evidence": "quiet bulk and FLRW background survive as contracts; variable Ccoh branches are not conserved yet",
            "next_action": "create 77-local-route-demote-or-continue-gate.md",
        },
        {
            "decision": "recommended_next_target",
            "status": "77-local-route-demote-or-continue-gate.md",
            "evidence": "checkpoint 76 did not close Bianchi; decide whether to build parent u/D owner or demote local route",
            "next_action": "make explicit continue/demote decision",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "partial_Noether_structure_but_no_full_closure",
        "key_metrics": {
            "noether_steps": counts["noether_attempt_chain"],
            "branch_tests": counts["branch_identity_tests"],
            "closure_options": counts["closure_options"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "fail_open_gates": sum(1 for row in gates if row["status"] == "fail_open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "77-local-route-demote-or-continue-gate.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Ccoh-Bianchi-identity-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "noether_attempt_chain": (
            noether_attempt_rows(),
            ["step", "statement", "identity_piece", "status", "failure_mode"],
        ),
        "branch_identity_tests": (
            branch_identity_rows(),
            ["branch", "Ccoh", "identity_status", "reason", "remaining_gap"],
        ),
        "closure_options": (
            closure_options_rows(),
            ["option", "what_closes", "status", "cost", "verdict"],
        ),
        "gate_results": (
            gate_rows(),
            ["gate", "status", "detail"],
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
