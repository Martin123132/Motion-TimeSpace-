#!/usr/bin/env python3
"""Gate whether L_cg, a_F, or DeltaR can own the B_mem corridor.

Private theory-discipline tool. It checks whether the amplitude corridor can be
made predictive by deriving eta = H0 L_cg/c, a_F, or DeltaR before further fits.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
RUNS_ROOT = POST_CHECKPOINT / "runs"
AMPLITUDE_RUN = RUNS_ROOT / "20260531-132504-memory-stress-amplitude-prediction-attempt"

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "92-memory-stress-amplitude-prediction-attempt.md",
    FORMALIZATION / "87-Lcg-coarse-graining-rule.md",
    FORMALIZATION / "88-Lcg-rule-gate.md",
    FORMALIZATION / "90-Lcg-gradient-trace-bound.md",
    FORMALIZATION / "91-trace-suppression-closure-gate.md",
    FORMALIZATION / "92-solar-transition-current-ppn-gate.md",
    FORMALIZATION / "174-bmem-parent-boundary-law.md",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    role = {
        "92-memory-stress-amplitude-prediction-attempt.md": "latest Bmem corridor and eta bound",
        "87-Lcg-coarse-graining-rule.md": "candidate universal L_cg rule",
        "88-Lcg-rule-gate.md": "free/fitted L_cg rejection and FLRW Hubble-cap pass",
        "90-Lcg-gradient-trace-bound.md": "L_cg gradient leakage warning",
        "91-trace-suppression-closure-gate.md": "universal U_B^2 trace law compatibility",
        "92-solar-transition-current-ppn-gate.md": "transition-shell local failure",
        "174-bmem-parent-boundary-law.md": "Bmem endpoint/source identity and trace corridor",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def bmem_values() -> list[dict[str, Any]]:
    rows = read_csv(AMPLITUDE_RUN / "results" / "source_profile_summary.csv")
    return [
        {
            "run_id": row["run_id"],
            "branch": row["branch"],
            "B_mem": float(row["B_mem"]),
        }
        for row in rows
    ]


def owner_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner": "L_cg / eta",
            "candidate_rule": "curvature-source coherence length with Hubble cap",
            "conditional_result": "homogeneous FLRW gives G_K=0, L_cg=L_H, eta=H0 L_cg/c=1 at z=0",
            "earned": "eta=1 is no longer arbitrary if the L_cg coherence rule is accepted",
            "missing": "L_cg rule, alpha_K, eta_H, and memory-diffusion fixed point are not parent-derived",
            "status": "conditional_background_owner_not_parent_theorem",
        },
        {
            "owner": "DeltaR",
            "candidate_rule": "endpoint contrast of memory trace functional R(m;X_B)",
            "conditional_result": "DeltaR>=0 if the parent relaxation orders early endpoint above present endpoint",
            "earned": "positive sign has a plausible Lyapunov/relaxation route",
            "missing": "functional R, endpoint ordering, and magnitude are not derived",
            "status": "conditional_sign_owner_magnitude_open",
        },
        {
            "owner": "a_F",
            "candidate_rule": "dimensionless trace-coupling normalization",
            "conditional_result": "a_F>0 gives positive B_mem when DeltaR>=0",
            "earned": "sign can be tied to attractive/relaxing trace coupling",
            "missing": "normalization and upper range are not fixed by an action",
            "status": "conditional_sign_owner_scale_open",
        },
        {
            "owner": "a_F DeltaR product",
            "candidate_rule": "parent contrast budget",
            "conditional_result": "with eta=1, required product is 3 B_mem",
            "earned": "observed fixed-branch range asks for an order-one product, not a ridiculous one",
            "missing": "product is still inferred from fitted B_mem rather than predicted before the fit",
            "status": "corridor_budget_only",
        },
    ]


def eta_budget_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    eta_cases = [
        ("sub_horizon_half", 0.5, "toy sub-horizon"),
        ("FLRW_Hubble_cap", 1.0, "conditional eta from homogeneous L_cg=L_H"),
        ("unit_budget_max_from_92", 1.474203, "largest eta allowed if a_F DeltaR<=1 for max B_mem"),
    ]
    rows: list[dict[str, Any]] = []
    for item in values:
        for label, eta, note in eta_cases:
            product = 3.0 * item["B_mem"] * eta**2
            rows.append(
                {
                    "run_id": item["run_id"],
                    "branch": item["branch"],
                    "B_mem": item["B_mem"],
                    "eta_case": label,
                    "eta": eta,
                    "required_aF_DeltaR": product,
                    "within_unit_budget": 0.0 < product <= 1.0,
                    "within_half_budget": 0.0 < product <= 0.5,
                    "note": note,
                }
            )
    return rows


def predictive_prior_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidate_products = [
        ("very_weak_unit_budget", 0.0, 1.0, "derived only if parent proves 0<a_F DeltaR<=1"),
        ("half_budget", 0.0, 0.5, "derived only if parent proves 0<a_F DeltaR<=0.5"),
        ("observed_order_window_not_prior", 0.2236, 0.4602, "matches eta=1 observed branches but is not an independent prior"),
    ]
    rows: list[dict[str, Any]] = []
    for label, low, high, status in candidate_products:
        rows.append(
            {
                "candidate_prior": label,
                "eta": 1.0,
                "aF_DeltaR_low": low,
                "aF_DeltaR_high": high,
                "Bmem_low": low / 3.0,
                "Bmem_high": high / 3.0,
                "contains_all_inspected_fixed_Bmem": all(low / 3.0 <= item["B_mem"] <= high / 3.0 for item in values),
                "status": status,
            }
        )
    return rows


def equation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "L_cg = [L_H^-2 + alpha_K G_K^2]^-1/2",
            "status": "candidate_universal_closure",
            "risk": "not parent-derived; gradients are dangerous locally",
        },
        {
            "step": 2,
            "equation": "FLRW: G_K = 0 -> L_cg = L_H = c/H_bg",
            "status": "conditional_background_reduction",
            "risk": "depends on accepting the L_cg coherence rule",
        },
        {
            "step": 3,
            "equation": "today: eta = H0 L_cg/c = 1",
            "status": "conditional_eta_lock",
            "risk": "not a microscopic theorem",
        },
        {
            "step": 4,
            "equation": "B_mem = a_F DeltaR / (3 eta^2)",
            "status": "trace_contrast_corridor",
            "risk": "a_F and DeltaR remain unseparated",
        },
        {
            "step": 5,
            "equation": "eta=1 -> a_F DeltaR = 3 B_mem",
            "status": "conditional_product_requirement",
            "risk": "product inferred from fitted B_mem",
        },
        {
            "step": 6,
            "equation": "support claim requires prior prediction of eta, a_F, and DeltaR",
            "status": "promotion_gate",
            "risk": "not yet satisfied",
        },
    ]


def gate_rows(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    b_values = [item["B_mem"] for item in values]
    product_low = 3.0 * min(b_values)
    product_high = 3.0 * max(b_values)
    return [
        {
            "gate": "free_or_fit_chosen_Lcg_rejected",
            "result": "pass",
            "reason": "previous L_cg gate rejects sector/fitted/residual-selected L_cg",
        },
        {
            "gate": "FLRW_eta1_from_Lcg_coherence",
            "result": "pass_conditional",
            "reason": "homogeneous FLRW gives G_K=0 and L_cg=L_H, so eta=1 today",
        },
        {
            "gate": "eta_parent_derived",
            "result": "fail",
            "reason": "the L_cg coherence rule remains a closure candidate, not microscopic dynamics",
        },
        {
            "gate": "eta1_product_order_one",
            "result": "pass",
            "reason": f"eta=1 implies a_F DeltaR={product_low:.6f} to {product_high:.6f}",
        },
        {
            "gate": "DeltaR_sign_condition",
            "result": "pass_conditional",
            "reason": "positive DeltaR follows only if endpoint relaxation ordering is derived",
        },
        {
            "gate": "aF_sign_condition",
            "result": "pass_conditional",
            "reason": "positive a_F is plausible for a relaxing trace coupling but not action-normalized",
        },
        {
            "gate": "aF_DeltaR_separately_predicted",
            "result": "fail",
            "reason": "only the product is constrained; neither factor is independently predicted",
        },
        {
            "gate": "predictive_Bmem_prior_earned",
            "result": "fail",
            "reason": "the only narrow window comes from the fitted B_mem range, not from parent theory",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "conditional eta=1 plus order-one product is still a corridor, not a prediction",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "eta_status",
            "value": "eta_equals_1_conditionally_from_FLRW_Hubble_cap_not_parent_derived",
        },
        {
            "decision": "trace_product_status",
            "value": "aF_DeltaR_order_one_required_not_predicted",
        },
        {
            "decision": "Bmem_prior_status",
            "value": "wide_corridor_tightened_to_eta1_product_but_not_predictive",
        },
        {
            "decision": "cosmology_branch_status",
            "value": "still_empirically_competitive_closure_candidate",
        },
        {
            "decision": "next_target",
            "value": "derive_endpoint_relaxation_contrast_DeltaR_or_trace_coupling_aF",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-Lcg-trace-contrast-owner-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    values = bmem_values()
    write_csv(results_dir / "source_checkpoint_register.csv", source_rows(), ["source", "exists", "role"])
    write_csv(
        results_dir / "owner_candidates.csv",
        owner_candidate_rows(),
        ["owner", "candidate_rule", "conditional_result", "earned", "missing", "status"],
    )
    write_csv(
        results_dir / "equation_chain.csv",
        equation_chain_rows(),
        ["step", "equation", "status", "risk"],
    )
    write_csv(
        results_dir / "eta_product_budget.csv",
        eta_budget_rows(values),
        [
            "run_id",
            "branch",
            "B_mem",
            "eta_case",
            "eta",
            "required_aF_DeltaR",
            "within_unit_budget",
            "within_half_budget",
            "note",
        ],
    )
    write_csv(
        results_dir / "predictive_prior_test.csv",
        predictive_prior_rows(values),
        [
            "candidate_prior",
            "eta",
            "aF_DeltaR_low",
            "aF_DeltaR_high",
            "Bmem_low",
            "Bmem_high",
            "contains_all_inspected_fixed_Bmem",
            "status",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gate_rows(values), ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decision_rows(), ["decision", "value"])

    products = [3.0 * item["B_mem"] for item in values]
    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "Lcg_eta_conditionally_locked_trace_product_not_predicted",
        "eta_status": "eta=1 conditional on FLRW Hubble-cap L_cg",
        "eta1_required_aF_DeltaR_range": [min(products), max(products)],
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 93; attack DeltaR endpoint relaxation or a_F trace coupling next",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
