#!/usr/bin/env python3
"""Gate the parent-theory ownership status of B_mem, p, and u3.

This is a private theory-discipline artifact. It does not promote the cosmology
branch; it records exactly what is conditionally derived, what is merely
bounded, and what remains fitted.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCE_CHECKPOINTS = [
    "50-parent-activation-law-attempt.md",
    "51-FLRW-memory-current-contract.md",
    "52-load-tensor-origin-attempt.md",
    "56-u3-quarter-parent-cell-theorem-attempt.md",
    "57-memory-action-owner-contract.md",
    "58-S-cell-variation-attempt.md",
    "59-topological-cell-current-owner-attempt.md",
    "61-bound-domain-boundary-theorem-attempt.md",
    "82-amplitude-normalization-gate.md",
    "90-cosmo-model-selection-stability-ledger.md",
]

COSMO_RUNS = [
    "20260531-124544-cosmo-SN-BAO-short-smoke",
    "20260531-125701-cosmo-SN-BAO-short-smoke",
    "20260531-125724-cosmo-SN-BAO-short-smoke",
    "20260531-125813-cosmo-SN-BAO-short-smoke",
    "20260531-125832-cosmo-SN-BAO-short-smoke",
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_checkpoint_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rel in SOURCE_CHECKPOINTS:
        path = POST_CHECKPOINT / rel
        rows.append(
            {
                "source": str(path),
                "exists": path.exists(),
                "role": {
                    "50-parent-activation-law-attempt.md": "p=3 regularity and hazard route",
                    "51-FLRW-memory-current-contract.md": "det(Q) memory-current contract",
                    "52-load-tensor-origin-attempt.md": "Q tensor kinematic origin",
                    "56-u3-quarter-parent-cell-theorem-attempt.md": "u3=1/4 3+1 cell route",
                    "57-memory-action-owner-contract.md": "single owner action contract",
                    "58-S-cell-variation-attempt.md": "direct variation failure",
                    "59-topological-cell-current-owner-attempt.md": "topological hair-control attempt",
                    "61-bound-domain-boundary-theorem-attempt.md": "local/FLRW boundary split",
                    "82-amplitude-normalization-gate.md": "previous amplitude status",
                    "90-cosmo-model-selection-stability-ledger.md": "empirical reason to revisit ownership",
                }[rel],
            }
        )
    return rows


def cosmology_parameter_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_id in COSMO_RUNS:
        edge_path = RUNS_ROOT / run_id / "results" / "prior_edge_table.csv"
        config_path = RUNS_ROOT / run_id / "run_config.json"
        if not edge_path.exists():
            continue
        config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        for row in read_csv(edge_path):
            if not row["model"].startswith("MTS"):
                continue
            if row["parameter"] not in {"B_mem", "p", "u3"}:
                continue
            rows.append(
                {
                    "run_id": run_id,
                    "branch": f"{config.get('sn_observable', 'mu-sh0es')}|{config.get('sn_covariance_mode', 'diagonal')}|{config.get('bao_label', 'BAO_primary')}|rows={config.get('sn_rows_used', config.get('sn_max_rows', ''))}",
                    "model": row["model"],
                    "parameter": row["parameter"],
                    "best_fit": row["best_fit"],
                    "lower": row["lower"],
                    "upper": row["upper"],
                    "edge_flag": row["edge_flag"],
                }
            )
    return rows


def fixed_bmem_range(rows: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    values = [
        float(row["best_fit"])
        for row in rows
        if row["model"] == "MTS_fixed_p3_u3quarter" and row["parameter"] == "B_mem"
    ]
    if not values:
        return None, None
    return min(values), max(values)


def ownership_attempt_rows(bmin: float | None, bmax: float | None) -> list[dict[str, Any]]:
    b_range = "" if bmin is None or bmax is None else f"{bmin:.6f} to {bmax:.6f}"
    return [
        {
            "quantity": "p",
            "target_value": "3",
            "best_current_owner": "I_M = det(Q_coh) with three spatial coherent-load eigenvalues",
            "derivation_status": "conditional_shape_derivation",
            "what_is_earned": "cubic exposure follows from a spatial determinant once Q_coh is parent-owned",
            "what_is_missing": "parent action/current for Q_coh and proof that exposure uses spatial determinant rather than an inserted cubic",
            "promotion_status": "not_promoted",
        },
        {
            "quantity": "u3",
            "target_value": "1/4",
            "best_current_owner": "3+1 coherent observer-cell normalization C4 with spatial determinant exposure",
            "derivation_status": "conditional_cell_normalization",
            "what_is_earned": "X_FLRW = 4N gives u3=1/4 if the clock leg normalizes the coherent load",
            "what_is_missing": "action/current proof that the time leg normalizes but is not a fourth exposure eigenvalue",
            "promotion_status": "not_promoted",
        },
        {
            "quantity": "B_mem",
            "target_value": b_range,
            "best_current_owner": "memory stress amplitude corridor B_mem ~ a_F DeltaR / (3 eta^2)",
            "derivation_status": "order_one_corridor_only",
            "what_is_earned": "fixed-branch B_mem is positive, non-edge, and order-one-corridor compatible across tested branches",
            "what_is_missing": "prediction of eta, a_F, DeltaR, sign, and conservation exchange from parent action",
            "promotion_status": "not_promoted",
        },
    ]


def equation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "Theta^i_j = h^{i alpha} h_{j beta} nabla_alpha u^beta",
            "status": "kinematic_definition",
            "risk": "needs parent ownership of u^mu and coherent projection",
        },
        {
            "step": 2,
            "equation": "Q^i_j = 4 integral_t^t0 P_coh[Theta]^i_j d tau",
            "status": "conditional_3plus1_normalized_load",
            "risk": "the factor 4 is not action-derived yet",
        },
        {
            "step": 3,
            "equation": "Q^i_j|FLRW = 4N delta^i_j",
            "status": "conditional_FLRW_reduction",
            "risk": "requires FLRW coherent branch and C4 normalization",
        },
        {
            "step": 4,
            "equation": "I_M = det(Q_coh) = (4N)^3",
            "status": "conditional_spatial_determinant",
            "risk": "must prove spatial determinant, not four-dimensional determinant",
        },
        {
            "step": 5,
            "equation": "F(N) = 1 - exp[-I_M] = 1 - exp[-(N/(1/4))^3]",
            "status": "conditional_activation_law",
            "risk": "shape owned conditionally; amplitude B_mem still fitted",
        },
        {
            "step": 6,
            "equation": "Delta H^2/H0^2 ~ B_mem F(N)",
            "status": "closure_stress_response",
            "risk": "B_mem needs parent stress/conservation prediction",
        },
    ]


def gate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fixed_b = [
        row for row in rows if row["model"] == "MTS_fixed_p3_u3quarter" and row["parameter"] == "B_mem"
    ]
    fixed_b_edge_count = sum(str(row["edge_flag"]).lower() == "true" for row in fixed_b)
    fitted_u3_edges = [
        row for row in rows if row["model"] == "MTS_fitted_u3" and str(row["edge_flag"]).lower() == "true"
    ]
    return [
        {
            "gate": "p3_shape_owned_by_spatial_determinant",
            "result": "pass_conditional",
            "reason": "det(Q_coh) gives cubic exposure once Q is owned",
        },
        {
            "gate": "u3_quarter_owned_by_3plus1_cell",
            "result": "pass_conditional",
            "reason": "C4 route gives X_FLRW=4N but clock/spatial split is not action-derived",
        },
        {
            "gate": "Bmem_non_edge_in_fixed_branch",
            "result": "pass" if fixed_b and fixed_b_edge_count == 0 else "fail",
            "reason": f"{len(fixed_b)} fixed-branch B_mem values inspected; edge hits={fixed_b_edge_count}",
        },
        {
            "gate": "Bmem_parent_predicted",
            "result": "fail",
            "reason": "only an order-one amplitude corridor exists",
        },
        {
            "gate": "fitted_u3_ablation_stable",
            "result": "fail" if fitted_u3_edges else "open",
            "reason": f"fitted-u3 edge rows={len(fitted_u3_edges)}",
        },
        {
            "gate": "single_parent_owner_satisfied",
            "result": "fail",
            "reason": "S_cell/S_stress contract exists but direct variation/topology did not derive the branch",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "conditional ownership is not a field-theory derivation",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "p_status",
            "value": "conditionally_owned_shape_not_promoted",
        },
        {
            "decision": "u3_status",
            "value": "conditional_3plus1_cell_scale_not_promoted",
        },
        {
            "decision": "Bmem_status",
            "value": "non_edge_empirical_amplitude_with_order_one_corridor_not_prediction",
        },
        {
            "decision": "cosmology_branch_status",
            "value": "empirically_competitive_closure_candidate_pending_parent_amplitude_owner",
        },
        {
            "decision": "next_target",
            "value": "derive_S_stress_memory_exchange_or_keep_Bmem_as_closure",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-Bmem-p-u3-parent-ownership-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    parameter_rows = cosmology_parameter_rows()
    bmin, bmax = fixed_bmem_range(parameter_rows)

    write_csv(
        results_dir / "source_checkpoint_register.csv",
        source_checkpoint_rows(),
        ["source", "exists", "role"],
    )
    write_csv(
        results_dir / "cosmology_parameter_evidence.csv",
        parameter_rows,
        ["run_id", "branch", "model", "parameter", "best_fit", "lower", "upper", "edge_flag"],
    )
    write_csv(
        results_dir / "ownership_attempts.csv",
        ownership_attempt_rows(bmin, bmax),
        [
            "quantity",
            "target_value",
            "best_current_owner",
            "derivation_status",
            "what_is_earned",
            "what_is_missing",
            "promotion_status",
        ],
    )
    write_csv(
        results_dir / "equation_chain.csv",
        equation_chain_rows(),
        ["step", "equation", "status", "risk"],
    )
    write_csv(
        results_dir / "gate_results.csv",
        gate_rows(parameter_rows),
        ["gate", "result", "reason"],
    )
    write_csv(results_dir / "decision.csv", decision_rows(), ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "Bmem_p_u3_parent_ownership_gate_written_not_promoted",
        "fixed_branch_Bmem_range": [bmin, bmax],
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 91 and decide whether to attack S_stress/Bmem prediction next",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
