#!/usr/bin/env python3
"""Gate whether endpoint relaxation can own DeltaR for the B_mem amplitude.

Private theory-discipline tool. It tries to separate what is actually derived
from the endpoint-relaxation/Lyapunov route from what is merely a post-fit
contrast budget.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "91-Bmem-p-u3-parent-ownership-gate.md",
    POST_CHECKPOINT / "92-memory-stress-amplitude-prediction-attempt.md",
    POST_CHECKPOINT / "93-Lcg-trace-contrast-owner-gate.md",
    FORMALIZATION / "69-relaxation-functional-lock.md",
    FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
    FORMALIZATION / "87-Lcg-coarse-graining-rule.md",
    FORMALIZATION / "88-Lcg-rule-gate.md",
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


def latest_lcg_run() -> Path:
    runs = sorted(RUNS_ROOT.glob("*-Lcg-trace-contrast-owner-gate"))
    if not runs:
        raise FileNotFoundError("No Lcg trace-contrast owner-gate run found.")
    return runs[-1]


def flrw_product_values(lcg_run: Path) -> list[dict[str, Any]]:
    path = lcg_run / "results" / "eta_product_budget.csv"
    rows = read_csv(path)
    values: list[dict[str, Any]] = []
    for row in rows:
        if row.get("eta_case") != "FLRW_Hubble_cap":
            continue
        values.append(
            {
                "run_id": row["run_id"],
                "branch": row["branch"],
                "B_mem": float(row["B_mem"]),
                "eta": float(row["eta"]),
                "required_aF_DeltaR": float(row["required_aF_DeltaR"]),
            }
        )
    if not values:
        raise ValueError(f"No FLRW_Hubble_cap rows found in {path}")
    return values


def source_rows() -> list[dict[str, Any]]:
    role = {
        "91-Bmem-p-u3-parent-ownership-gate.md": "p/u3/Bmem ownership status before amplitude separation",
        "92-memory-stress-amplitude-prediction-attempt.md": "Bmem stress-exchange corridor and eta bound",
        "93-Lcg-trace-contrast-owner-gate.md": "eta=1 conditional lock and a_F DeltaR target range",
        "69-relaxation-functional-lock.md": "candidate convex relaxation functional and F1=0 route",
        "70-relaxation-functional-lock-first-results.md": "conditional local screening and stiffness warnings",
        "87-Lcg-coarse-graining-rule.md": "candidate universal L_cg closure",
        "88-Lcg-rule-gate.md": "Hubble-cap pass and fitted-Lcg rejection",
        "174-bmem-parent-boundary-law.md": "endpoint contrast identity Bmem=a_F DeltaR/(3 eta^2)",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def relaxation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "convex_endpoint_functional",
            "equation": "R(m;X_B)=R_L(X_B)+1/2 lambda_R(X_B)[m-m_L(X_B)]^2+O([m-m_L]^3)",
            "earns": "R has a local minimum and DeltaR can be non-negative under ordered endpoints",
            "missing": "global convexity and endpoint displacement are not derived",
            "status": "conditional",
        },
        {
            "contract_item": "local_extremum_lock",
            "equation": "F(m;X_B)=F_L(X_B)+a_F[R(m;X_B)-R(m_L;X_B)] -> F_1=a_F partial_m R|m_L=0",
            "earns": "linear trace force vanishes at the relaxed endpoint",
            "missing": "only local; does not predict endpoint contrast amplitude",
            "status": "conditional_pass",
        },
        {
            "contract_item": "monotone_relaxation",
            "equation": "nabla_mu J_m^mu=-gamma_B partial_m R + [1-Pi_B]S_cg",
            "earns": "with S_cg off and gamma_B>0, relaxation moves down the R functional",
            "missing": "source leakage and Pi_B behaviour along FLRW history",
            "status": "conditional",
        },
        {
            "contract_item": "lyapunov_descent",
            "equation": "dR/dtau=-gamma_B(partial_m R)^2 <= 0",
            "earns": "DeltaR=R_early-R_today >= 0 if today is downstream in relaxation time",
            "missing": "the parent action has not fixed the cosmological arrow/endpoints",
            "status": "conditional_sign",
        },
        {
            "contract_item": "memory_amplitude_identity",
            "equation": "B_mem=a_F DeltaR/(3 eta^2)",
            "earns": "with eta=1 the target is exactly a_F DeltaR=3 B_mem",
            "missing": "a_F normalization and DeltaR magnitude",
            "status": "identity_after_closure",
        },
        {
            "contract_item": "local_ppn_safety",
            "equation": "F_2=a_F lambda_R=a_F mu_B/gamma_B",
            "earns": "high gamma_B can screen locally without huge F_2",
            "missing": "proof that cosmological DeltaR can be order-one while local residuals stay small",
            "status": "open_guardrail",
        },
    ]


def candidate_model_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "candidate": "strict_convex_Lyapunov_endpoint",
            "claim": "DeltaR=R_early-R_today >= 0",
            "works_if": "gamma_B>0, R convex enough on the path, source leakage controlled, endpoint ordering proven",
            "amplitude_power": "sign only",
            "risk": "magnitude remains free",
            "status": "conditional_sign_owner",
        },
        {
            "candidate": "bounded_normalized_contrast",
            "claim": "0 <= DeltaR <= 1",
            "works_if": "R is normalized as a bounded parent contrast before fitting",
            "amplitude_power": f"requires a_F >= {product_high:.6f} to cover all inspected branches",
            "risk": "normalization of R is not yet from the action",
            "status": "conditional_order_window",
        },
        {
            "candidate": "quadratic_displacement_route",
            "claim": "DeltaR=1/2 lambda_R (Delta m)^2",
            "works_if": "lambda_R and endpoint displacement are parent-fixed",
            "amplitude_power": f"for a_F=lambda_R=1, Delta m={math.sqrt(2.0 * product_low):.6f} to {math.sqrt(2.0 * product_high):.6f}",
            "risk": "Delta m is still an unpredicted endpoint separation",
            "status": "conditional_magnitude_template",
        },
        {
            "candidate": "high_mobility_screening",
            "claim": "large gamma_B gives fast local relaxation without large lambda_R",
            "works_if": "local screening uses mobility rather than stiff trace curvature",
            "amplitude_power": "keeps order-one DeltaR compatible with small local residuals",
            "risk": "requires a parent mobility law and locality proof",
            "status": "preferred_local_safe_route",
        },
        {
            "candidate": "stiff_R_magnitude_route",
            "claim": "large lambda_R forces enough DeltaR from small Delta m",
            "works_if": "F_2=a_F lambda_R somehow remains PPN-safe",
            "amplitude_power": "can manufacture magnitude",
            "risk": "dangerous because the same stiffness amplifies local trace coupling",
            "status": "rejected_as_default_route",
        },
        {
            "candidate": "flat_or_nonconvex_R",
            "claim": "DeltaR sign and endpoint ordering are not controlled",
            "works_if": "extra nonlocal boundary rule is added by hand",
            "amplitude_power": "none",
            "risk": "collapses to closure-only amplitude",
            "status": "fail",
        },
    ]


def required_delta_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for a_f in [0.25, 0.5, product_high, 1.0, 2.0]:
        delta_low = product_low / a_f
        delta_high = product_high / a_f
        rows.append(
            {
                "a_F": a_f,
                "DeltaR_low": delta_low,
                "DeltaR_high": delta_high,
                "fits_0_to_1_DeltaR": 0.0 <= delta_low <= 1.0 and 0.0 <= delta_high <= 1.0,
                "fits_0_to_half_DeltaR": 0.0 <= delta_low <= 0.5 and 0.0 <= delta_high <= 0.5,
                "interpretation": interpretation_for_delta(a_f, delta_low, delta_high, product_high),
            }
        )
    return rows


def interpretation_for_delta(a_f: float, delta_low: float, delta_high: float, product_high: float) -> str:
    if math.isclose(a_f, product_high, rel_tol=0.0, abs_tol=5e-7):
        return "minimum a_F if DeltaR is unit-bounded"
    if delta_high > 1.0:
        return "requires DeltaR above unit-normalized range for high-B branch"
    if delta_high > 0.5:
        return "fits unit contrast but exceeds half-budget for high-B branch"
    return "fits a conservative order-one contrast window"


def quadratic_displacement_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for a_f in [0.5, 1.0, 2.0]:
        for lambda_r in [0.5, 1.0, 2.0]:
            delta_r_low = product_low / a_f
            delta_r_high = product_high / a_f
            rows.append(
                {
                    "a_F": a_f,
                    "lambda_R": lambda_r,
                    "Delta_m_low": math.sqrt(2.0 * delta_r_low / lambda_r),
                    "Delta_m_high": math.sqrt(2.0 * delta_r_high / lambda_r),
                    "risk_note": "large lambda_R lowers Delta_m but raises F_2=a_F lambda_R",
                }
            )
    return rows


def gate_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "gate": "DeltaR_positive_from_convex_relaxation",
            "result": "pass_conditional",
            "reason": "if R is Lyapunov-like and today is downstream, DeltaR=R_early-R_today is non-negative",
        },
        {
            "gate": "endpoint_ordering_parent_derived",
            "result": "fail",
            "reason": "the parent action has not yet proven which cosmological endpoint has the larger R",
        },
        {
            "gate": "DeltaR_order_one_window_available",
            "result": "pass_conditional",
            "reason": f"eta=1 requires a_F DeltaR={product_low:.6f} to {product_high:.6f}, an order-one product",
        },
        {
            "gate": "DeltaR_predicted_without_SN_BAO_fit",
            "result": "fail",
            "reason": "the numerical window is inherited from fitted B_mem, not predicted first",
        },
        {
            "gate": "aF_lower_bound_if_DeltaR_le1",
            "result": "pass_bound",
            "reason": f"if 0<=DeltaR<=1, all inspected branches require a_F >= {product_high:.6f}",
        },
        {
            "gate": "aF_lower_bound_if_DeltaR_le_half",
            "result": "pass_bound",
            "reason": f"if 0<=DeltaR<=0.5, all inspected branches require a_F >= {2.0 * product_high:.6f}",
        },
        {
            "gate": "stiff_R_default_route_safe",
            "result": "fail_open",
            "reason": "using large lambda_R to force amplitude threatens local PPN through F_2=a_F lambda_R",
        },
        {
            "gate": "high_mobility_route_preferred",
            "result": "pass_conditional",
            "reason": "local screening should come from gamma_B rather than huge lambda_R if this branch is to survive",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "DeltaR sign/order bounds help, but B_mem is still not predicted before fitting",
        },
    ]


def decision_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": "DeltaR_status",
            "value": "positive_sign_and_order_one_window_conditional_not_prediction",
        },
        {
            "decision": "aF_if_unit_DeltaR",
            "value": f"a_F_must_be_at_least_{product_high:.6f}",
        },
        {
            "decision": "aF_near_one_readout",
            "value": f"if_a_F_is_order_one_near_1_then_DeltaR_required_{product_low:.6f}_to_{product_high:.6f}",
        },
        {
            "decision": "local_safety_preference",
            "value": "prefer_high_gamma_B_mobility_screening_over_large_lambda_R_stiffness",
        },
        {
            "decision": "next_target",
            "value": "derive_or_bound_trace_coupling_a_F_normalization",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-endpoint-relaxation-DeltaR-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    lcg_run = latest_lcg_run()
    values = flrw_product_values(lcg_run)
    products = [item["required_aF_DeltaR"] for item in values]
    product_low = min(products)
    product_high = max(products)

    write_csv(results_dir / "source_checkpoint_register.csv", source_rows(), ["source", "exists", "role"])
    write_csv(
        results_dir / "flrw_eta1_product_inputs.csv",
        values,
        ["run_id", "branch", "B_mem", "eta", "required_aF_DeltaR"],
    )
    write_csv(
        results_dir / "relaxation_functional_contract.csv",
        relaxation_contract_rows(),
        ["contract_item", "equation", "earns", "missing", "status"],
    )
    write_csv(
        results_dir / "DeltaR_candidate_models.csv",
        candidate_model_rows(product_low, product_high),
        ["candidate", "claim", "works_if", "amplitude_power", "risk", "status"],
    )
    write_csv(
        results_dir / "required_DeltaR_by_aF.csv",
        required_delta_rows(product_low, product_high),
        ["a_F", "DeltaR_low", "DeltaR_high", "fits_0_to_1_DeltaR", "fits_0_to_half_DeltaR", "interpretation"],
    )
    write_csv(
        results_dir / "quadratic_displacement_budget.csv",
        quadratic_displacement_rows(product_low, product_high),
        ["a_F", "lambda_R", "Delta_m_low", "Delta_m_high", "risk_note"],
    )
    write_csv(results_dir / "gate_results.csv", gate_rows(product_low, product_high), ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decision_rows(product_low, product_high), ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_lcg_run": str(lcg_run),
        "readout": "DeltaR_sign_and_order_bound_conditional_not_prediction",
        "eta1_required_aF_DeltaR_range": [product_low, product_high],
        "aF_min_if_DeltaR_le1": product_high,
        "aF_min_if_DeltaR_le_half": 2.0 * product_high,
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 94; derive or bound trace-coupling a_F normalization next",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
