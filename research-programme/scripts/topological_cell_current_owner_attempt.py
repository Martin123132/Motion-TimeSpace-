#!/usr/bin/env python3
"""Attempt a topological/nonpropagating owner for the memory cell current."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "11_cell_current_doc": Path("11-cell-current-origin-attempt.md"),
    "12_gauge_noether_doc": Path("12-gauge-noether-origin-audit.md"),
    "57_owner_contract_doc": Path("57-memory-action-owner-contract.md"),
    "58_S_cell_doc": Path("58-S-cell-variation-attempt.md"),
    "58_status": Path("runs/20260531-105020-S-cell-variation-attempt/status.json"),
    "58_variation_candidates": Path("runs/20260531-105020-S-cell-variation-attempt/results/variation_candidate_ledger.csv"),
    "58_gates": Path("runs/20260531-105020-S-cell-variation-attempt/results/gate_results.csv"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


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


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "ordinary_conserved_cell_current",
            "schematic_term": "S=int sqrt(-g) W (dR)^2/2",
            "variation_result": "d star J=0, Q_cell=constant",
            "status": "rejected",
            "why": "checkpoint 11 showed conservation permits nonzero charge/hair",
            "remaining_gap": "needs zero-charge theorem",
        },
        {
            "candidate": "direct_topological_multiplier",
            "schematic_term": "S=int B wedge (F_cell-F_target)",
            "variation_result": "F_cell=F_target, dB=0",
            "status": "closure_constraint_not_derivation",
            "why": "protects target if supplied but still inserts F_target",
            "remaining_gap": "does not select spatial determinant or 3+1 normalization",
        },
        {
            "candidate": "BF_flat_connection_owner",
            "schematic_term": "S=int B wedge F[A] + boundary terms",
            "variation_result": "F[A]=0 and d_A B=0",
            "status": "conditional_no_local_hair_owner",
            "why": "flatness removes local propagating cell curvature; only global/topological sectors remain",
            "remaining_gap": "topological class must be fixed to zero or to the desired memory flux",
        },
        {
            "candidate": "closed_form_memory_flux",
            "schematic_term": "S=int lambda wedge dJ_M + boundary pairing",
            "variation_result": "dJ_M=0 except sources/boundaries",
            "status": "partial_current_owner",
            "why": "nonpropagating closed flux can protect conservation bookkeeping",
            "remaining_gap": "closed does not mean zero; flux class remains free",
        },
        {
            "candidate": "relative_cohomology_boundary_lock",
            "schematic_term": "S=int_M B wedge F + int_boundary B wedge A with fixed relative class",
            "variation_result": "bulk hair killed; allowed charge determined by boundary/cohomology class",
            "status": "best_next_contract_candidate",
            "why": "could replace local hair with a global boundary datum instead of fitted local charge",
            "remaining_gap": "must derive the relevant class and show it gives the quarter-cell memory branch",
        },
        {
            "candidate": "characteristic_class_selection",
            "schematic_term": "I_M proportional to characteristic class built from spatial triad/coherent cell bundle",
            "variation_result": "quantized/topological invariant may select dimension/counting factors",
            "status": "interesting_but_unbuilt",
            "why": "only route here that might select 3 and 4 structurally",
            "remaining_gap": "no explicit bundle/characteristic class has been constructed",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "S_BF = integral B wedge F[A]",
            "variation": "delta B",
            "result": "F[A]=0",
            "status": "pass_conditional",
            "meaning": "cell connection is locally flat/nonpropagating",
        },
        {
            "step": 2,
            "equation": "S_BF = integral B wedge F[A]",
            "variation": "delta A",
            "result": "d_A B=0",
            "status": "pass_conditional",
            "meaning": "cell flux is covariantly closed",
        },
        {
            "step": 3,
            "equation": "F[A]=0 locally",
            "variation": "local solution",
            "result": "A=g^{-1}dg, no local curvature hair",
            "status": "pass_conditional",
            "meaning": "local propagating reciprocal/memory hair is removed",
        },
        {
            "step": 4,
            "equation": "Q_top = integral_cycle B",
            "variation": "global sector",
            "result": "Q_top is fixed by cohomology/boundary data, not by local EOM",
            "status": "open",
            "meaning": "zero-charge or desired-charge theorem is still needed",
        },
        {
            "step": 5,
            "equation": "target branch: I_M=det(Q_coh), X=4N",
            "variation": "selection test",
            "result": "not obtained from BF flatness alone",
            "status": "fail",
            "meaning": "topology protects constraints but does not yet select the quarter branch",
        },
        {
            "step": 6,
            "equation": "relative boundary class [B,A]|boundary",
            "variation": "boundary condition",
            "result": "could fix global memory class if parent boundary rule exists",
            "status": "best_next_contract",
            "meaning": "the live problem moves to cohomology/boundary selection",
        },
    ]


def no_charge_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "local_hair_removed",
            "status": "pass_conditional",
            "evidence": "flat BF connection has no local curvature hair",
            "failure_mode": "global holonomy/flux can remain",
        },
        {
            "test": "ordinary_conserved_charge_removed",
            "status": "pass_partial",
            "evidence": "charge becomes topological/boundary data rather than arbitrary radial integration constant",
            "failure_mode": "boundary class may still be arbitrary",
        },
        {
            "test": "zero_charge_theorem_derived",
            "status": "fail",
            "evidence": "no parent rule sets the relevant cohomology class to zero in local systems",
            "failure_mode": "topological sector carries hidden hair",
        },
        {
            "test": "cosmology_memory_class_selected",
            "status": "fail",
            "evidence": "no class has been shown to equal det(Q_coh) with 3+1 normalization",
            "failure_mode": "topology protects a placeholder, not the MTS branch",
        },
        {
            "test": "local_silence_and_FLRW_activity_coexist",
            "status": "open",
            "evidence": "relative cohomology could allow trivial local bound-domain class and nontrivial FLRW class",
            "failure_mode": "same boundary rule may silence both or activate both",
        },
    ]


def selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "p=3",
            "can_topology_protect": "yes_conditionally",
            "can_topology_select": "not_yet",
            "reason": "spatial triad/3-cycle could protect determinant exposure, but no characteristic class is defined",
            "next_requirement": "construct spatial coherent-cell bundle whose invariant reduces to det(Q_coh)",
        },
        {
            "target": "u3=1/4",
            "can_topology_protect": "yes_conditionally",
            "can_topology_select": "not_yet",
            "reason": "3+1 cell can be represented as a four-leg coframe volume, but no class forces X=4N",
            "next_requirement": "derive 4-cell normalization from coframe bundle/relative boundary rule",
        },
        {
            "target": "local silence",
            "can_topology_protect": "partial",
            "can_topology_select": "open",
            "reason": "flat local connection kills local curvature hair; zero holonomy/flux still needs boundary theorem",
            "next_requirement": "prove bound domains have trivial relative cell class",
        },
        {
            "target": "Bianchi conservation",
            "can_topology_protect": "partial",
            "can_topology_select": "no",
            "reason": "closed flux helps conservation bookkeeping but not stress-energy amplitude",
            "next_requirement": "couple topological owner to S_stress without importing perturbations",
        },
        {
            "target": "b_mem",
            "can_topology_protect": "no_currently",
            "can_topology_select": "no",
            "reason": "topological class may quantize a flux, but no amplitude map to cosmological stress is defined",
            "next_requirement": "amplitude/stress theorem remains separate unless boundary class fixes magnitude",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "topological_owner_attempted",
            "status": "pass",
            "detail": "BF flat-connection, closed-form, relative cohomology, and characteristic-class routes audited",
        },
        {
            "gate": "local_propagating_hair_removed",
            "status": "pass_conditional",
            "detail": "flat BF-type owner can remove local curvature hair",
        },
        {
            "gate": "zero_charge_theorem_derived",
            "status": "fail",
            "detail": "global flux/holonomy class remains unless boundary/cohomology rule fixes it",
        },
        {
            "gate": "p3_selected_by_topology",
            "status": "fail",
            "detail": "no spatial coherent-cell characteristic class has been built",
        },
        {
            "gate": "u3_quarter_selected_by_topology",
            "status": "fail",
            "detail": "no 3+1 coframe class has been shown to force X=4N",
        },
        {
            "gate": "local_silence_FLRW_activity_split",
            "status": "open",
            "detail": "relative cohomology could separate local bound domains from FLRW, but this is not derived",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "topology narrows the owner problem but does not derive the branch",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "topological_cell_owner_status",
            "status": "protects_against_local_hair_conditionally_not_branch_derivation",
            "evidence": "BF/closed-form owner can remove local curvature hair but leaves global class selection open",
            "next_action": "write relative cohomology boundary contract",
        },
        {
            "decision": "quarter_branch_status",
            "status": "retained_less_free_closure_candidate_pending_cohomology_owner",
            "evidence": "topological route does not kill the branch, but does not derive p=3/u3=1/4",
            "next_action": "derive or reject characteristic class for spatial determinant and 3+1 normalization",
        },
        {
            "decision": "recommended_next_target",
            "status": "60-relative-cohomology-boundary-contract.md",
            "evidence": "global/boundary class is now the precise missing theorem",
            "next_action": "define the local-zero/FLRW-nonzero boundary rule or demote topological owner",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Topological cell-current owner attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_58 = load_json("58_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-topological-cell-current-owner-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = candidate_rows()
    variations = variation_chain_rows()
    no_charge = no_charge_rows()
    selection = selection_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "topological_candidate_ledger.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "topological_variation_chain.csv", variations, list(variations[0].keys()))
    write_csv(results_dir / "no_charge_tests.csv", no_charge, list(no_charge[0].keys()))
    write_csv(results_dir / "branch_selection_tests.csv", selection, list(selection[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_topological_cell_current_owner_attempt",
        "readout": "topological_owner_conditions_local_hair_not_branch_derivation",
        "recommendation": "write_relative_cohomology_boundary_contract_next",
        "next_target": "60-relative-cohomology-boundary-contract.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_route": "relative_cohomology_boundary_lock",
        "key_metrics": {
            "u3_quarter": status_58["key_metrics"]["u3_quarter"],
            "topological_candidates": len(candidates),
            "selection_targets": len(selection),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "topological_candidate_ledger": str(results_dir / "topological_candidate_ledger.csv"),
            "topological_variation_chain": str(results_dir / "topological_variation_chain.csv"),
            "no_charge_tests": str(results_dir / "no_charge_tests.csv"),
            "branch_selection_tests": str(results_dir / "branch_selection_tests.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
