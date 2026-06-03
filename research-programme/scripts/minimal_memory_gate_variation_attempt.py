#!/usr/bin/env python3
"""Attempt the minimal S_mem=chi_D L_mem plus auxiliary selector variation."""

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
    "67_aux_selector_doc": Path("67-auxiliary-selector-parent-contract.md"),
    "68_conservation_doc": Path("68-chiD-gated-memory-conservation-contract.md"),
    "68_status": Path("runs/20260531-112455-chiD-gated-memory-conservation-contract/status.json"),
    "68_noether_chain": Path("runs/20260531-112455-chiD-gated-memory-conservation-contract/results/noether_identity_chain.csv"),
    "68_couplings": Path("runs/20260531-112455-chiD-gated-memory-conservation-contract/results/candidate_couplings.csv"),
    "68_gates": Path("runs/20260531-112455-chiD-gated-memory-conservation-contract/results/gate_results.csv"),
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


def variation_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "action_definition",
            "result": "S_gate = int sqrt(-g)[chi_D L_mem(Q,g,u,...) + lambda_chi(chi_D-C_coh)]",
            "status": "minimal_test_action",
            "meaning": "memory is active only through chi_D and selector is auxiliary",
            "gap": "L_mem itself still underived",
        },
        {
            "variation": "delta_lambda",
            "result": "chi_D = C_coh",
            "status": "pass",
            "meaning": "selector remains threshold-free",
            "gap": "C_coh parent ownership remains",
        },
        {
            "variation": "delta_chi",
            "result": "lambda_chi = -L_mem",
            "status": "exchange_relation",
            "meaning": "auxiliary multiplier stores the memory-gating exchange",
            "gap": "L_mem must be known to evaluate stress",
        },
        {
            "variation": "on_shell_gate_action",
            "result": "S_gate_on_shell = int sqrt(-g) C_coh L_mem",
            "status": "compact_effective_action",
            "meaning": "auxiliary constraint reduces to a C_coh-weighted memory action",
            "gap": "metric variation of C_coh is unavoidable",
        },
        {
            "variation": "metric_variation",
            "result": "T_gate_munu = C_coh T_Lmem_munu + L_mem T_Ccoh_munu plus Q,u,domain terms",
            "status": "key_result",
            "meaning": "conservation requires extra C_coh variation stress, not just chi times memory stress",
            "gap": "T_Ccoh_munu is not constructed",
        },
        {
            "variation": "Noether_identity",
            "result": "nabla_mu T_gate^munu vanishes only with E_Q,E_u,E_domain and C_coh variations included",
            "status": "conditional",
            "meaning": "action-derived gate can conserve, but not if C_coh is frozen",
            "gap": "full parent equations missing",
        },
    ]


def conservation_term_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "Ccoh_T_Lmem",
            "form": "C_coh T_Lmem^munu",
            "role": "ordinary memory stress weighted by selector",
            "local_behavior": "suppressed where C_coh=0",
            "FLRW_behavior": "full memory stress where C_coh=1",
            "risk": "not conserved alone when C_coh varies",
        },
        {
            "term": "Lmem_T_Ccoh",
            "form": "terms from delta_g C_coh",
            "role": "exchange/conservation completion for variable selector",
            "local_behavior": "zero in constant quiet bulk; active near transitions",
            "FLRW_behavior": "may vanish in homogeneous branch if C_coh constant",
            "risk": "unknown until C_coh variation is derived",
        },
        {
            "term": "Q_u_field_equations",
            "form": "E_Q L_xi Q + E_u L_xi u",
            "role": "Noether cancellation terms",
            "local_behavior": "must vanish or exchange consistently on shell",
            "FLRW_behavior": "must reproduce background memory dynamics",
            "risk": "memory owner still missing",
        },
        {
            "term": "domain_boundary_current",
            "form": "relative/domain boundary contribution from averaging/projector",
            "role": "handles local-to-FLRW transition",
            "local_behavior": "main local PPN danger",
            "FLRW_behavior": "absent or homogeneous in background",
            "risk": "not yet derived",
        },
    ]


def branch_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "quiet_local_bulk",
            "Ccoh": "0 constant",
            "effective_memory_action": "0",
            "extra_Ccoh_terms": "0 if Ccoh variation constant/quiet",
            "status": "pass_conditional",
            "remaining_gap": "prove Ccoh variation quiet in parent local solution",
        },
        {
            "branch": "stationary_bound_interior",
            "Ccoh": "low/constant after averaging",
            "effective_memory_action": "suppressed",
            "extra_Ccoh_terms": "small/zero if domain average stationary",
            "status": "pass_conditional",
            "remaining_gap": "averaging/domain theorem",
        },
        {
            "branch": "FLRW_background",
            "Ccoh": "1 constant",
            "effective_memory_action": "L_mem recovered",
            "extra_Ccoh_terms": "zero if homogeneous Ccoh=1 fixed by symmetry",
            "status": "pass_contract",
            "remaining_gap": "explicit L_mem background equations",
        },
        {
            "branch": "transition_boundary",
            "Ccoh": "varies",
            "effective_memory_action": "interpolates",
            "extra_Ccoh_terms": "nonzero exchange stress/current",
            "status": "open",
            "remaining_gap": "dominant unresolved conservation/local-boundary issue",
        },
        {
            "branch": "dynamic_collapse",
            "Ccoh": "time-dependent/mixed",
            "effective_memory_action": "active dynamic memory",
            "extra_Ccoh_terms": "nonzero",
            "status": "open",
            "remaining_gap": "strong-field branch",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "minimal_variation_performed",
            "status": "pass",
            "detail": "delta_lambda and delta_chi give chi=Ccoh and lambda=-L_mem",
        },
        {
            "gate": "external_switch_avoided",
            "status": "pass",
            "detail": "on-shell action is Ccoh L_mem, so metric variation includes Ccoh terms",
        },
        {
            "gate": "local_bulk_silence_retained",
            "status": "pass_conditional",
            "detail": "constant Ccoh=0 quiet bulk has no scalar memory action",
        },
        {
            "gate": "FLRW_branch_retained",
            "status": "pass_contract",
            "detail": "constant Ccoh=1 recovers L_mem",
        },
        {
            "gate": "Bianchi_identity_completed",
            "status": "fail",
            "detail": "T_Ccoh and domain-boundary current are not derived",
        },
        {
            "gate": "boundary_exchange_resolved",
            "status": "open",
            "detail": "variable Ccoh creates transition/exchange terms",
        },
        {
            "gate": "Lmem_parent_derived",
            "status": "fail",
            "detail": "memory Lagrangian owner remains underived",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "minimal gate improves consistency but is not yet a GR reduction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "variation is a consistency narrowing result, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "minimal_memory_gate_status",
            "status": "variation_successful_but_conservation_completion_missing",
            "evidence": "minimal action gives lambda=-L_mem and on-shell Ccoh L_mem, but Bianchi completion requires T_Ccoh and boundary current",
            "next_action": "derive Ccoh metric variation/exchange current or shift to boundary-only topological gate",
        },
        {
            "decision": "local_GR_route_status",
            "status": "local_bulk_plausible_boundary_unresolved",
            "evidence": "quiet bulk and FLRW limits work at contract level; transition boundary remains the dangerous region",
            "next_action": "try boundary-only/topological memory gate or Ccoh variation audit",
        },
        {
            "decision": "recommended_next_target",
            "status": "70-Ccoh-variation-and-boundary-current-audit.md",
            "evidence": "the missing mathematical object is delta_g Ccoh and the associated exchange current",
            "next_action": "audit whether Ccoh can be varied locally/covariantly without importing GR",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "variation_successful_but_conservation_completion_missing",
        "key_metrics": {
            "variation_results": counts["variation_results"],
            "conservation_terms": counts["conservation_terms"],
            "branch_tests": counts["branch_variation_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "70-Ccoh-variation-and-boundary-current-audit.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-minimal-memory-gate-variation-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "variation_results": (
            variation_result_rows(),
            ["variation", "result", "status", "meaning", "gap"],
        ),
        "conservation_terms": (
            conservation_term_rows(),
            ["term", "form", "role", "local_behavior", "FLRW_behavior", "risk"],
        ),
        "branch_variation_tests": (
            branch_variation_rows(),
            ["branch", "Ccoh", "effective_memory_action", "extra_Ccoh_terms", "status", "remaining_gap"],
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
