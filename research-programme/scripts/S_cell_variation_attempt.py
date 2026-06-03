#!/usr/bin/env python3
"""Attempt a variational S_cell owner for p=3 and u3=1/4."""

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
    "19_parent_action_skeleton": Path("19-constrained-parent-action-skeleton.md"),
    "56_cell_theorem_doc": Path("56-u3-quarter-parent-cell-theorem-attempt.md"),
    "57_owner_contract_doc": Path("57-memory-action-owner-contract.md"),
    "57_status": Path("runs/20260531-104702-memory-action-owner-contract/status.json"),
    "57_action_contract": Path("runs/20260531-104702-memory-action-owner-contract/results/action_term_contract.csv"),
    "57_equation_contract": Path("runs/20260531-104702-memory-action-owner-contract/results/equation_ownership_contract.csv"),
    "57_gates": Path("runs/20260531-104702-memory-action-owner-contract/results/gate_results.csv"),
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


def variation_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "direct_multiplier_constraints",
            "schematic_term": "S_cell=int sqrt(-g)[lambda_I(I_M-det Q)+lambda_X(X-4N)]",
            "variation_result": "delta lambda_I gives I_M=det Q; delta lambda_X gives X=4N",
            "status": "closure_not_derivation",
            "why": "it imposes p=3 and u3=1/4 directly",
            "next_action": "use only as benchmark contract, not parent theorem",
        },
        {
            "candidate": "soft_potential_lock",
            "schematic_term": "S_cell=int sqrt(-g)[-k_I(I_M-det Q)^2-k_X(X-4N)^2]",
            "variation_result": "drives system toward target if k terms dominate",
            "status": "rejected_as_parent_derivation",
            "why": "introduces arbitrary stiffnesses and propagating deviations/hair",
            "next_action": "reject unless k terms arise from integrating out a known sector",
        },
        {
            "candidate": "first_order_current_constraints",
            "schematic_term": "S_cell=int sqrt(-g)[lambda_Q(D_tau Q-P_coh Theta/u3)+lambda_I(I_M-det Q)]",
            "variation_result": "derives evolution equations from multipliers but still assumes normalization/source",
            "status": "partial_contract",
            "why": "turns the closure into local first-order equations but does not explain u3=1/4",
            "next_action": "add an independent cell-current/no-charge theorem for the normalization",
        },
        {
            "candidate": "coframe_volume_ratio_action",
            "schematic_term": "S_cell=int sqrt(-g) Lambda Phi(det Q / C4_spatial_projection)",
            "variation_result": "can relate spatial determinant to 3+1 coframe cell only after choosing Phi and projection",
            "status": "interesting_but_underdefined",
            "why": "may reconcile 3D determinant and 4D normalization but needs a precise invariant",
            "next_action": "formulate as differential-form/topological current rather than scalar potential",
        },
        {
            "candidate": "topological_BF_or_closed_form_owner",
            "schematic_term": "S_cell=int B wedge dA + lambda(cell_flux - spatial_memory_flux)",
            "variation_result": "can impose closed/nonpropagating cell current and potentially forbid local hair",
            "status": "best_next_route_not_built",
            "why": "matches the need for nonpropagating constraints and no-charge structure, but equations are not specified",
            "next_action": "attempt topological cell-current owner",
        },
    ]


def euler_lagrange_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "delta lambda_I",
            "equation": "I_M-det(Q_coh)=0",
            "status": "easy_constraint",
            "interpretation": "gets p=3 in FLRW but only by imposing determinant exposure",
            "problem": "not explanatory unless lambda_I has parent origin",
        },
        {
            "variation": "delta lambda_X",
            "equation": "X_FLRW-4N=0",
            "status": "easy_constraint",
            "interpretation": "gets u3=1/4 but only by imposing the quarter normalization",
            "problem": "directly smuggles the answer",
        },
        {
            "variation": "delta lambda_Q",
            "equation": "D_tau Q^i_j=(1/u3)P_coh[Theta]^i_j",
            "status": "partial_first_order_owner",
            "interpretation": "turns Q into an accumulated-load field equation",
            "problem": "still needs u3 and P_coh from deeper terms",
        },
        {
            "variation": "delta Q",
            "equation": "lambda_Q evolution tied to lambda_I Cof(Q)",
            "status": "mathematical_consistency",
            "interpretation": "determinant variation naturally produces cofactor structure",
            "problem": "does not select determinant by itself",
        },
        {
            "variation": "delta e or delta u",
            "equation": "cell stress/current contribution to coframe and clock-flow equations",
            "status": "missing_required",
            "interpretation": "needed for conservation, local silence, and perturbations",
            "problem": "not computed in current scalar contract",
        },
        {
            "variation": "boundary variation",
            "equation": "cell charge or flux boundary term must vanish/topologically cancel",
            "status": "missing_required",
            "interpretation": "needed to avoid local reciprocal/memory hair",
            "problem": "ordinary current conservation permits nonzero charge",
        },
    ]


def no_smuggling_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "does_action_select_determinant_without_lambda_I",
            "status": "fail",
            "evidence": "all scalar routes need an explicit determinant term or equivalent definition",
            "consequence": "p=3 is not variationally selected yet",
        },
        {
            "test": "does_action_select_4N_without_lambda_X",
            "status": "fail",
            "evidence": "the quarter normalization is imposed by X=4N unless a 4-cell current is built",
            "consequence": "u3=1/4 is not variationally selected yet",
        },
        {
            "test": "does_first_order_Q_improve_theory_status",
            "status": "pass_partial",
            "evidence": "D_tau Q=P_coh Theta/u3 is a field equation rather than a post-processed integral",
            "consequence": "useful contract, not full derivation",
        },
        {
            "test": "does_soft_potential_avoid_closure",
            "status": "fail",
            "evidence": "soft potentials add arbitrary stiffness and allow deviations/hair",
            "consequence": "not preferred for local-GR-safe branch",
        },
        {
            "test": "does_topological_route_avoid_hair_in_principle",
            "status": "open",
            "evidence": "nonpropagating/topological constraints could forbid local charge, unlike ordinary current conservation",
            "consequence": "best next attempt",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "direct_variation_attempted",
            "status": "pass",
            "detail": "multiplier, first-order, potential, coframe-ratio, and topological routes audited",
        },
        {
            "gate": "S_cell_derives_p3_without_imposition",
            "status": "fail",
            "detail": "det(Q) still has to be inserted or constrained explicitly",
        },
        {
            "gate": "S_cell_derives_u3_quarter_without_imposition",
            "status": "fail",
            "detail": "X=4N still has to be inserted or constrained explicitly",
        },
        {
            "gate": "first_order_Q_field_equation_available",
            "status": "pass_partial",
            "detail": "D_tau Q=P_coh Theta/u3 can make Q a local accumulated-load field",
        },
        {
            "gate": "ordinary_current_sufficient",
            "status": "fail",
            "detail": "checkpoint 11 showed ordinary current conservation permits nonzero charge/hair",
        },
        {
            "gate": "topological_owner_needed",
            "status": "pass",
            "detail": "only a nonpropagating/topological or no-charge owner looks capable of avoiding direct imposition",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "S_cell variation did not derive the branch; support language remains forbidden",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "S_cell_variation_status",
            "status": "direct_variation_fails_as_derivation",
            "evidence": "local multiplier action can impose p=3/u3=1/4 but does not select them",
            "next_action": "attempt topological/nonpropagating cell-current owner",
        },
        {
            "decision": "quarter_branch_status",
            "status": "retained_as_less_free_closure_candidate_not_derived",
            "evidence": "checkpoint 55 smoke survives, checkpoint 58 variation does not derive the scale",
            "next_action": "keep quarter lock as benchmark while testing owner routes",
        },
        {
            "decision": "recommended_next_target",
            "status": "59-topological-cell-current-owner-attempt.md",
            "evidence": "ordinary current conservation permits hair; direct multipliers impose answer; topological/no-charge route is the next live possibility",
            "next_action": "try a BF/closed-form/no-charge owner for the memory cell",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="S_cell variation attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_57 = load_json("57_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-S-cell-variation-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = variation_candidate_rows()
    variations = euler_lagrange_rows()
    tests = no_smuggling_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "variation_candidate_ledger.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "euler_lagrange_contract.csv", variations, list(variations[0].keys()))
    write_csv(results_dir / "no_smuggling_tests.csv", tests, list(tests[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_S_cell_variation_attempt",
        "readout": "S_cell_direct_variation_fails_as_derivation_topological_owner_next",
        "recommendation": "attempt_topological_cell_current_owner_next",
        "next_target": "59-topological-cell-current-owner-attempt.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "key_metrics": {
            "u3_quarter": status_57["key_metrics"]["u3_quarter"],
            "variation_candidates": len(candidates),
            "euler_lagrange_rows": len(variations),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "pass_partial_gates": sum(1 for row in gates if row["status"] == "pass_partial"),
            "best_next_route": "topological_BF_or_closed_form_owner",
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "variation_candidate_ledger": str(results_dir / "variation_candidate_ledger.csv"),
            "euler_lagrange_contract": str(results_dir / "euler_lagrange_contract.csv"),
            "no_smuggling_tests": str(results_dir / "no_smuggling_tests.csv"),
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
