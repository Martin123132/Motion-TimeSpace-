#!/usr/bin/env python3
"""Write the chi_D-gated memory conservation contract."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "57_memory_action_owner_doc": Path("57-memory-action-owner-contract.md"),
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "67_aux_selector_doc": Path("67-auxiliary-selector-parent-contract.md"),
    "67_status": Path("runs/20260531-112108-auxiliary-selector-parent-contract/status.json"),
    "67_variation_chain": Path("runs/20260531-112108-auxiliary-selector-parent-contract/results/variation_chain.csv"),
    "67_gates": Path("runs/20260531-112108-auxiliary-selector-parent-contract/results/gate_results.csv"),
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


def conservation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "full_action_not_inserted_source",
            "contract": "T_mem[chi_D] must come from varying S_mem[g,u,Q,chi_D,...], not from appending a hand-made stress tensor",
            "why": "Bianchi conservation follows from diffeomorphism invariance only for action-derived terms",
            "status": "required",
            "failure_mode": "source is not conserved except by tuning",
        },
        {
            "obligation": "selector_constraint_in_action",
            "contract": "S_aux = int sqrt(-g) lambda_chi(chi_D-C_coh) or topological equivalent remains inside the same variational system",
            "why": "constraint and memory source must exchange stress consistently",
            "status": "required",
            "failure_mode": "chi_D is fixed externally",
        },
        {
            "obligation": "Ccoh_metric_variation",
            "contract": "delta_g C_coh, delta_u C_coh, and domain-average variations are accounted for or proven irrelevant",
            "why": "freezing C_coh breaks the Noether identity",
            "status": "required_open",
            "failure_mode": "fake conservation",
        },
        {
            "obligation": "local_silence",
            "contract": "where chi_D=C_coh=0 and gradients/boundaries are absent, T_mem and exchange current vanish in scalar volume-memory channel",
            "why": "recover local GR/PPN baseline",
            "status": "required",
            "failure_mode": "local residual fifth source",
        },
        {
            "obligation": "FLRW_activity",
            "contract": "where chi_D=C_coh=1, S_mem reduces to the FLRW memory-current branch",
            "why": "do not kill cosmology while silencing local systems",
            "status": "required",
            "failure_mode": "selector erases the empirical cosmology pillar",
        },
        {
            "obligation": "exchange_current_closure",
            "contract": "nabla_mu T_mem^munu + nabla_mu T_aux^munu = -nabla_mu T_matter^munu, with matter conserved or explicitly exchanged by a derived current",
            "why": "total stress must satisfy Bianchi identity",
            "status": "required_open",
            "failure_mode": "energy-momentum leak",
        },
    ]


def noether_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "identity": "S_total = S_GR_like + S_matter + S_mem[g,u,Q,chi_D] + S_aux[chi_D,C_coh,lambda_chi]",
            "readout": "all memory/selector terms must be in one diffeomorphism-invariant action",
            "status": "contract",
            "gap": "S_mem is not yet explicitly derived",
        },
        {
            "step": 2,
            "identity": "delta S_total under diffeomorphism -> nabla_mu T_total^munu = sum E_fields L_xi fields",
            "readout": "on shell, total stress is conserved",
            "status": "Noether_structure",
            "gap": "requires all relevant field equations, including u,Q,chi,lambda",
        },
        {
            "step": 3,
            "identity": "E_lambda=0 -> chi_D=C_coh",
            "readout": "selector follows coherent expansion invariant",
            "status": "conditional_pass",
            "gap": "C_coh ownership remains open",
        },
        {
            "step": 4,
            "identity": "E_chi=0 -> lambda_chi = -delta S_mem/delta chi_D",
            "readout": "selector multiplier absorbs memory-gating force",
            "status": "key_exchange_relation",
            "gap": "must compute for explicit S_mem",
        },
        {
            "step": 5,
            "identity": "delta_g S_aux includes lambda_chi delta_g C_coh",
            "readout": "auxiliary stress is not generally zero after memory coupling",
            "status": "warning",
            "gap": "needs C_coh variation, not frozen invariant",
        },
        {
            "step": 6,
            "identity": "local chi=0 branch: delta S_mem/delta chi_D may be nonzero at boundary only",
            "readout": "bulk local silence plausible, boundary/exchange current remains open",
            "status": "partial",
            "gap": "boundary layer or relative-class owner still needed",
        },
    ]


def candidate_coupling_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "multiplicative_gate",
            "form": "S_mem = int sqrt(-g) chi_D L_mem(Q,C2,...)",
            "local_branch": "chi_D=0 kills scalar memory bulk source",
            "FLRW_branch": "chi_D=1 recovers memory branch",
            "conservation_risk": "delta_chi gives lambda=-L_mem; delta_g C_coh terms enter auxiliary stress",
            "verdict": "best_minimal_test",
        },
        {
            "candidate": "projector_gate",
            "form": "S_mem = int sqrt(-g) P(chi_D) L_mem with P(0)=0,P(1)=1",
            "local_branch": "can smooth activation",
            "FLRW_branch": "can recover memory branch",
            "conservation_risk": "P choice can hide a threshold/shape function",
            "verdict": "deferred_unless_P_derived",
        },
        {
            "candidate": "boundary_only_gate",
            "form": "S_mem lives on relative boundary class selected by chi_D",
            "local_branch": "trivial local class has no bulk memory",
            "FLRW_branch": "nontrivial expansion class carries memory",
            "conservation_risk": "needs explicit topological/boundary current conservation",
            "verdict": "best_long_term_route",
        },
        {
            "candidate": "external_switch",
            "form": "T_mem = chi_D T_memory inserted directly into field equations",
            "local_branch": "can silence local systems",
            "FLRW_branch": "can keep FLRW",
            "conservation_risk": "not action-derived, generally violates Bianchi",
            "verdict": "rejected",
        },
    ]


def branch_conservation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "Minkowski_or_quiet_local_bulk",
            "chi_Ccoh": "chi_D=C_coh=0",
            "memory_result": "scalar memory bulk off",
            "aux_result": "lambda may vanish if L_mem off",
            "conservation_status": "pass_conditional",
            "remaining_gap": "boundary and C_coh variation not tested",
        },
        {
            "branch": "stationary_bound_local_interior",
            "chi_Ccoh": "low/zero",
            "memory_result": "suppressed scalar coherent memory",
            "aux_result": "small or zero bulk exchange",
            "conservation_status": "pass_conditional",
            "remaining_gap": "domain boundary current",
        },
        {
            "branch": "local_to_FLRW_boundary",
            "chi_Ccoh": "transition",
            "memory_result": "exchange current likely nonzero",
            "aux_result": "lambda delta Ccoh terms matter",
            "conservation_status": "open",
            "remaining_gap": "main Bianchi danger",
        },
        {
            "branch": "FLRW_background",
            "chi_Ccoh": "1",
            "memory_result": "active memory branch recovered",
            "aux_result": "constraint holds; homogeneous variation may be manageable",
            "conservation_status": "pass_contract",
            "remaining_gap": "explicit memory stress still missing",
        },
        {
            "branch": "collapse_merger_dynamic",
            "chi_Ccoh": "dynamic/mixed",
            "memory_result": "not forced silent",
            "aux_result": "exchange current dynamic",
            "conservation_status": "open",
            "remaining_gap": "strong-field dynamic sector",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "action_based_conservation_contract",
            "status": "pass",
            "detail": "conservation requirement is moved into S_total rather than appended stress",
        },
        {
            "gate": "external_switch_rejected",
            "status": "pass",
            "detail": "direct T_mem=chi T insertion is rejected as generally nonconserved",
        },
        {
            "gate": "local_bulk_silence_possible",
            "status": "pass_conditional",
            "detail": "chi=Ccoh=0 can turn off scalar memory bulk source",
        },
        {
            "gate": "FLRW_activity_possible",
            "status": "pass_contract",
            "detail": "chi=Ccoh=1 can recover FLRW memory branch",
        },
        {
            "gate": "Bianchi_identity_derived",
            "status": "fail",
            "detail": "explicit S_mem and Ccoh variation are still missing",
        },
        {
            "gate": "boundary_exchange_current_resolved",
            "status": "open",
            "detail": "local-to-FLRW transition current is the main unresolved danger",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "contract improves consistency but does not prove GR reduction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a conservation contract, not empirical support",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "chiD_gated_memory_conservation_status",
            "status": "contract_written_not_derived_boundary_exchange_open",
            "evidence": "action-based gating can make local bulk silence and FLRW activity plausible, but explicit Bianchi identity and boundary exchange current are not derived",
            "next_action": "attempt minimal S_mem=chi_D L_mem variation and exchange-current ledger",
        },
        {
            "decision": "local_GR_route_status",
            "status": "consistent_contract_but_unpromoted",
            "evidence": "external switch is rejected; local branch now requires explicit memory action variation",
            "next_action": "derive or reject multiplicative memory gate",
        },
        {
            "decision": "recommended_next_target",
            "status": "69-minimal-memory-gate-variation-attempt.md",
            "evidence": "the concrete next calculation is S_mem=chi_D L_mem plus S_aux variation",
            "next_action": "compute lambda relation, metric variation terms, and local/FLRW conservation gates",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "contract_written_not_derived_boundary_exchange_open",
        "key_metrics": {
            "contract_obligations": counts["conservation_contract_obligations"],
            "noether_steps": counts["noether_identity_chain"],
            "coupling_candidates": counts["candidate_couplings"],
            "branch_tests": counts["branch_conservation_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "69-minimal-memory-gate-variation-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-chiD-gated-memory-conservation-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "conservation_contract_obligations": (
            conservation_contract_rows(),
            ["obligation", "contract", "why", "status", "failure_mode"],
        ),
        "noether_identity_chain": (
            noether_identity_rows(),
            ["step", "identity", "readout", "status", "gap"],
        ),
        "candidate_couplings": (
            candidate_coupling_rows(),
            ["candidate", "form", "local_branch", "FLRW_branch", "conservation_risk", "verdict"],
        ),
        "branch_conservation_tests": (
            branch_conservation_rows(),
            ["branch", "chi_Ccoh", "memory_result", "aux_result", "conservation_status", "remaining_gap"],
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
