#!/usr/bin/env python3
"""Attempt a parent-cell theorem for the u3=1/4 quarter lock."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "10_observer_map_doc": Path("10-observer-map-symplectic-contract.md"),
    "51_memory_current_doc": Path("51-FLRW-memory-current-contract.md"),
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "54_domain_u3_doc": Path("54-coherent-domain-and-u3-origin.md"),
    "55_quarter_smoke_doc": Path("55-u3-quarter-lock-smoke.md"),
    "55_status": Path("runs/20260531-104003-u3-quarter-lock-smoke/status.json"),
    "55_guardrails": Path("runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_guardrail_comparison.csv"),
    "55_gates": Path("runs/20260531-104003-u3-quarter-lock-smoke/results/gate_results.csv"),
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


def theorem_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use a parent coherent 3+1 observer cell, not a spatial-only cell.",
            "equation": "C_4 = theta^0 wedge theta^1 wedge theta^2 wedge theta^3",
            "status": "contractual",
            "meaning": "the normalization cell includes one clock leg and three spatial/load legs",
            "missing_theorem": "parent action must define this cell as the memory-normalization object",
        },
        {
            "step": 2,
            "statement": "In FLRW conformal/coherent gauge all four cell legs scale with the same log expansion.",
            "equation": "d ln C_4/dtau = 4H",
            "status": "conditional_kinematic_pass",
            "meaning": "three spatial legs plus one clock/coherence leg give four equal contributions",
            "missing_theorem": "the temporal/coherence leg contribution must be derived, not asserted",
        },
        {
            "step": 3,
            "statement": "The integrated four-cell load from epoch to today is 4N.",
            "equation": "L_4 = integral_t^t0 4H dt = 4 ln(a0/a)=4N",
            "status": "conditional_pass",
            "meaning": "the quarter lock follows if the memory load eigenvalue is normalized by the coherent 4-cell",
            "missing_theorem": "requires the physical branch N>=0 and a parent time orientation",
        },
        {
            "step": 4,
            "statement": "Identify the scalar load eigenvalue with four-cell-normalized e-fold load.",
            "equation": "X_FLRW = 4N = N/u3",
            "status": "conditional_pass",
            "meaning": "this gives u3=1/4",
            "missing_theorem": "must show this is the same X used in Q^i_j and not a post-hoc rescaling",
        },
        {
            "step": 5,
            "statement": "Keep the memory exposure as a spatial coherent-load determinant.",
            "equation": "Q^i_j = X_FLRW delta^i_j; I_M=det(Q)=X_FLRW^3=(4N)^3",
            "status": "conditional_pass",
            "meaning": "three spatial eigen-directions still give p=3 while the 3+1 cell gives the quarter scale",
            "missing_theorem": "why normalization is 4D while determinant is spatial 3D must be action-owned",
        },
        {
            "step": 6,
            "statement": "Activation follows by survival exposure.",
            "equation": "F=1-exp[-(4N)^3] = 1-exp[-(N/(1/4))^3]",
            "status": "exact_given_previous_steps",
            "meaning": "the retained quarter branch is reproduced exactly",
            "missing_theorem": "survival/exposure law remains conditional until parent-owned",
        },
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "conformal_3plus1_coherence_cell",
            "status": "best_conditional_theorem_candidate",
            "what_it_gives": "u3=1/4 from four equal coherent cell legs in FLRW",
            "what_it_does_not_give": "parent action, temporal leg origin, amplitude, conservation, perturbations",
            "risk": "could be a clever normalization story unless the 4-cell is independently required",
        },
        {
            "route": "spatial_only_cell",
            "status": "rejected_for_scale",
            "what_it_gives": "u3=1/3 if one normalizes by three spatial legs",
            "what_it_does_not_give": "the smoke-retained quarter value",
            "risk": "would ignore the clock leg even though MTS is motion-time-space, not space-only",
        },
        {
            "route": "phase_space_3plus1_dual_cell",
            "status": "interesting_but_unbuilt",
            "what_it_gives": "possible link to observer-map cell contracts and local reciprocity",
            "what_it_does_not_give": "a clean derivation of the cosmology activation normalization",
            "risk": "generic phase-volume arguments already failed locally unless made specific",
        },
        {
            "route": "empirical_quarter_lock",
            "status": "insufficient_alone",
            "what_it_gives": "u3=1/4 survives the internal smoke",
            "what_it_does_not_give": "a theorem",
            "risk": "numerology if used without the 3+1 cell contract",
        },
        {
            "route": "arbitrary_rescale_X_to_4N",
            "status": "rejected_circular",
            "what_it_gives": "the answer by definition",
            "what_it_does_not_give": "non-circular theory content",
            "risk": "exactly the smuggling we are trying to avoid",
        },
    ]


def noncircularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "cell_defined_before_quarter_score",
            "status": "pass_partial",
            "evidence": "observer-cell and coherent-domain language already existed before the quarter smoke",
            "failure_mode": "if the 3+1 cell is only invoked because 1/4 survived",
        },
        {
            "test": "fourth_leg_is_physical",
            "status": "fail_currently",
            "evidence": "the clock/coherence leg is motivated by MTS and conformal FLRW but not derived",
            "failure_mode": "time leg becomes a decorative factor of four",
        },
        {
            "test": "spatial_determinant_vs_4D_normalization_consistent",
            "status": "open",
            "evidence": "p=3 comes from spatial determinant, u3=1/4 from 3+1 normalization",
            "failure_mode": "a critic can ask why determinant is not 4D too",
        },
        {
            "test": "local_GR_branch_not_damaged",
            "status": "open",
            "evidence": "local observer-cell contract exists but is not yet linked to this cosmology 4-cell theorem",
            "failure_mode": "cosmology normalization and local reciprocity remain separate closures",
        },
        {
            "test": "empirical_smoke_not_used_as_proof",
            "status": "pass",
            "evidence": "quarter lock retained as less-free closure candidate only",
            "failure_mode": "claiming the smoke derives the scale",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "u3_quarter_cell_route_written",
            "status": "pass",
            "detail": "3+1 coherent observer-cell route gives X_FLRW=4N and u3=1/4",
        },
        {
            "gate": "u3_quarter_parent_derived",
            "status": "fail",
            "detail": "the route is conditional; no parent action or constraint derives the 4-cell normalization",
        },
        {
            "gate": "time_leg_origin_derived",
            "status": "fail",
            "detail": "clock/coherence leg contribution H is motivated but not derived",
        },
        {
            "gate": "spatial_determinant_and_4D_cell_reconciled",
            "status": "open",
            "detail": "p=3 uses spatial determinant while u3=1/4 uses 3+1 normalization; needs action-level reconciliation",
        },
        {
            "gate": "quarter_lock_empirical_smoke_survived",
            "status": "pass",
            "detail": "checkpoint 55 retained u3=1/4 with failed_guardrails=[]",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "still missing action owner, conservation, amplitude, perturbations, official CMB, and fresh holdout",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "u3_quarter_parent_cell_status",
            "status": "conditional_cell_theorem_candidate_not_parent_derivation",
            "evidence": "3+1 coherent cell gives u3=1/4 if the clock leg and memory normalization are parent-owned",
            "next_action": "write the action/current contract that would own the 4-cell normalization",
        },
        {
            "decision": "quarter_branch_status",
            "status": "retained_less_free_closure_candidate",
            "evidence": "checkpoint 55 smoke survived and this checkpoint supplies a non-circular candidate theorem route",
            "next_action": "connect 4-cell normalization to conservation/action ownership",
        },
        {
            "decision": "recommended_next_target",
            "status": "57-memory-action-owner-contract.md",
            "evidence": "the same missing object now owns p=3, u3=1/4, conservation, amplitude, and perturbations",
            "next_action": "define the minimal parent action/current owner or demote the branch to closure-only",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="u3=1/4 parent-cell theorem attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_55 = load_json("55_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-u3-quarter-parent-cell-theorem-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    theorem = theorem_chain_rows()
    routes = route_rows()
    noncircularity = noncircularity_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "u3_quarter_theorem_chain.csv", theorem, list(theorem[0].keys()))
    write_csv(results_dir / "candidate_cell_routes.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "noncircularity_tests.csv", noncircularity, list(noncircularity[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    metrics_55 = status_55["key_metrics"]
    status = {
        "status": "complete_u3_quarter_parent_cell_theorem_attempt",
        "readout": "u3_quarter_has_conditional_3plus1_cell_route_not_parent_derivation",
        "recommendation": "write_memory_action_owner_contract_next",
        "next_target": "57-memory-action-owner-contract.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_route": "conformal_3plus1_coherence_cell",
        "key_metrics": {
            "u3_quarter": 0.25,
            "X_FLRW_quarter_relation": "X_FLRW=4N",
            "spatial_determinant_power": 3,
            "coherent_cell_legs": 4,
            "quarter_delta_total_vs_fitted_C2": metrics_55["quarter_delta_total_vs_fitted_C2"],
            "failed_guardrails_from_55": metrics_55["failed_guardrails"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "u3_quarter_theorem_chain": str(results_dir / "u3_quarter_theorem_chain.csv"),
            "candidate_cell_routes": str(results_dir / "candidate_cell_routes.csv"),
            "noncircularity_tests": str(results_dir / "noncircularity_tests.csv"),
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
