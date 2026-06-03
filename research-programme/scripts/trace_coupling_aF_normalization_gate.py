#!/usr/bin/env python3
"""Gate whether the trace coupling a_F can be normalized before fitting.

Private theory-discipline tool. It separates an actual action-level
normalization of a_F from weaker sign/order/compatibility bounds.
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

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "82-amplitude-normalization-gate.md",
    POST_CHECKPOINT / "93-Lcg-trace-contrast-owner-gate.md",
    POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
    FORMALIZATION / "69-relaxation-functional-lock.md",
    FORMALIZATION / "70-relaxation-functional-lock-first-results.md",
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


def latest_delta_run() -> Path:
    runs = sorted(RUNS_ROOT.glob("*-endpoint-relaxation-DeltaR-gate"))
    if not runs:
        raise FileNotFoundError("No endpoint-relaxation DeltaR gate run found.")
    return runs[-1]


def source_rows() -> list[dict[str, Any]]:
    role = {
        "82-amplitude-normalization-gate.md": "earlier amplitude-status demotion baseline",
        "93-Lcg-trace-contrast-owner-gate.md": "eta=1 conditional lock and a_F DeltaR product",
        "94-endpoint-relaxation-DeltaR-gate.md": "DeltaR sign/order window and a_F lower bounds",
        "69-relaxation-functional-lock.md": "F_1=0 and F_2=a_F lambda_R trace-lock relation",
        "70-relaxation-functional-lock-first-results.md": "high-mobility vs stiff-R local-safety rule",
        "174-bmem-parent-boundary-law.md": "Gamma_eff trace projection and b_mem=a_F DeltaR/(3 eta^2)",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def product_inputs(delta_run: Path) -> list[dict[str, Any]]:
    rows = read_csv(delta_run / "results" / "flrw_eta1_product_inputs.csv")
    return [
        {
            "run_id": row["run_id"],
            "branch": row["branch"],
            "B_mem": float(row["B_mem"]),
            "eta": float(row["eta"]),
            "required_aF_DeltaR": float(row["required_aF_DeltaR"]),
        }
        for row in rows
    ]


def trace_normalization_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "dimensionless_R_normalization",
            "needed_statement": "R is a dimensionless parent contrast with fixed zero and unit scale",
            "why_it_matters": "otherwise a_F can be absorbed into a rescaling of R",
            "current_status": "missing",
            "result": "fail",
        },
        {
            "contract_item": "canonical_trace_projection",
            "needed_statement": "Gamma_eff = L_cg^-2 [F_L + (R-R_L)] with no extra dimensionless coefficient",
            "why_it_matters": "this would set a_F=1 by normalization",
            "current_status": "plausible gauge/normalization choice, not action-derived",
            "result": "pass_conditional_as_choice_only",
        },
        {
            "contract_item": "positive_relaxing_sign",
            "needed_statement": "a_F > 0 so positive DeltaR gives positive B_mem",
            "why_it_matters": "keeps the observed positive memory amplitude aligned with relaxation",
            "current_status": "conditional from relaxing trace-coupling orientation",
            "result": "pass_conditional",
        },
        {
            "contract_item": "local_quadratic_safety",
            "needed_statement": "F_2 = a_F lambda_R stays inside the local residual budget",
            "why_it_matters": "a_F cannot be made huge without risking local PPN residuals",
            "current_status": "bound template exists, numeric local cap not parent-derived",
            "result": "bound_only",
        },
        {
            "contract_item": "boundary_charge_matching",
            "needed_statement": "integrated memory-source flux fixes a_F before SN+BAO fitting",
            "why_it_matters": "would convert B_mem from fitted amplitude to predicted charge",
            "current_status": "currently circular because flux budget is inferred from fitted B_mem",
            "result": "fail",
        },
        {
            "contract_item": "field_redefinition_guard",
            "needed_statement": "m and R normalizations are fixed independently of the cosmology amplitude",
            "why_it_matters": "prevents hiding B_mem inside a variable convention",
            "current_status": "not yet proven",
            "result": "fail",
        },
    ]


def candidate_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "candidate": "canonical_unit_trace_coupling",
            "candidate_aF": 1.0,
            "what_it_would_mean": "F uses the same normalized R with unit coefficient",
            "amplitude_readout": f"requires DeltaR={product_low:.6f} to {product_high:.6f}",
            "local_safety_readout": "F_2=lambda_R, so order-one lambda_R is preferred",
            "status": "best_current_closure_choice_not_derivation",
        },
        {
            "candidate": "minimum_unit_DeltaR_coupling",
            "candidate_aF": product_high,
            "what_it_would_mean": "smallest a_F that can cover all inspected branches if DeltaR<=1",
            "amplitude_readout": "forces the highest branch to DeltaR=1",
            "local_safety_readout": "less trace stress than a_F=1 but needs near-maximal endpoint contrast",
            "status": "derived_lower_bound_if_unit_DeltaR",
        },
        {
            "candidate": "half_budget_coupling",
            "candidate_aF": 2.0 * product_high,
            "what_it_would_mean": "smallest a_F that can cover all inspected branches if DeltaR<=0.5",
            "amplitude_readout": "puts highest branch at DeltaR=0.5",
            "local_safety_readout": "near-unit a_F, safe only if lambda_R is not stiff",
            "status": "derived_lower_bound_if_half_DeltaR",
        },
        {
            "candidate": "weak_trace_coupling",
            "candidate_aF": 0.25,
            "what_it_would_mean": "trace coupling deliberately small",
            "amplitude_readout": f"requires DeltaR up to {product_high / 0.25:.6f}",
            "local_safety_readout": "locally gentle, but amplitude needs too much normalized contrast",
            "status": "disfavored_if_DeltaR_unit_bounded",
        },
        {
            "candidate": "strong_trace_coupling",
            "candidate_aF": 2.0,
            "what_it_would_mean": "trace coupling stronger than canonical unit normalization",
            "amplitude_readout": f"requires DeltaR={product_low / 2.0:.6f} to {product_high / 2.0:.6f}",
            "local_safety_readout": "raises F_2 unless lambda_R is small or local mobility absorbs screening",
            "status": "possible_but_needs_local_F2_proof",
        },
        {
            "candidate": "negative_trace_coupling",
            "candidate_aF": -1.0,
            "what_it_would_mean": "opposite trace orientation",
            "amplitude_readout": "would require negative DeltaR for positive B_mem",
            "local_safety_readout": "breaks the relaxation-sign story",
            "status": "rejected_for_positive_DeltaR_branch",
        },
    ]


def compatibility_rows(product_high: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    delta_caps = [0.5, 1.0]
    lambda_values = [0.25, 0.5, 1.0, 2.0, 4.0]
    f2_caps = [0.5, 1.0, 2.0]
    for delta_cap in delta_caps:
        a_f_low = product_high / delta_cap
        for lambda_r in lambda_values:
            for f2_cap in f2_caps:
                a_f_high = f2_cap / lambda_r
                rows.append(
                    {
                        "DeltaR_cap": delta_cap,
                        "lambda_R": lambda_r,
                        "F2_cap": f2_cap,
                        "aF_low_from_amplitude": a_f_low,
                        "aF_high_from_local_F2": a_f_high,
                        "window_exists": a_f_low <= a_f_high,
                        "canonical_aF1_allowed": a_f_low <= 1.0 <= a_f_high,
                        "interpretation": compatibility_interpretation(a_f_low, a_f_high),
                    }
                )
    return rows


def compatibility_interpretation(a_f_low: float, a_f_high: float) -> str:
    if a_f_low > a_f_high:
        return "no overlap between amplitude lower bound and local F2 upper bound"
    if a_f_low <= 1.0 <= a_f_high:
        return "canonical a_F=1 survives this toy bound"
    if a_f_high < 1.0:
        return "only sub-canonical a_F survives; needs large DeltaR"
    return "super-canonical a_F allowed but not required"


def degeneracy_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "degeneracy": "R_rescaling",
            "map": "R -> c_R R, a_F -> a_F/c_R",
            "effect_on_Bmem": "a_F DeltaR is invariant if DeltaR rescales with R",
            "break_condition": "parent action fixes the absolute normalization of R",
            "status": "major_open_blocker",
        },
        {
            "degeneracy": "m_coordinate_rescaling",
            "map": "m -> c_m m changes lambda_R and Delta m bookkeeping",
            "effect_on_Bmem": "quadratic DeltaR can be moved between curvature and displacement",
            "break_condition": "parent field metric or kinetic term fixes m units",
            "status": "open",
        },
        {
            "degeneracy": "local_safety_product",
            "map": "F_2=a_F lambda_R",
            "effect_on_Bmem": "cosmology wants a_F DeltaR, local safety sees a_F lambda_R",
            "break_condition": "simultaneous parent law for DeltaR and lambda_R",
            "status": "useful_constraint_pair_not_prediction",
        },
        {
            "degeneracy": "observed_product_window",
            "map": f"a_F DeltaR={product_low:.6f}..{product_high:.6f}",
            "effect_on_Bmem": "data fixes only product after eta=1",
            "break_condition": "derive either a_F or DeltaR before fitting",
            "status": "current_bottleneck",
        },
    ]


def gate_rows(product_low: float, product_high: float, windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    viable_canonical = sum(1 for row in windows if row["canonical_aF1_allowed"])
    total_windows = len(windows)
    return [
        {
            "gate": "aF_positive_sign",
            "result": "pass_conditional",
            "reason": "positive a_F is compatible with the relaxation sign route and positive B_mem",
        },
        {
            "gate": "aF_order_one_required",
            "result": "pass_bound",
            "reason": f"if DeltaR<=1 then a_F>={product_high:.6f}; if DeltaR<=0.5 then a_F>={2.0 * product_high:.6f}",
        },
        {
            "gate": "canonical_aF1_viable",
            "result": "pass_conditional",
            "reason": f"a_F=1 gives DeltaR={product_low:.6f} to {product_high:.6f}, inside the disciplined order-one corridor",
        },
        {
            "gate": "canonical_aF1_derived",
            "result": "fail",
            "reason": "unit coefficient is a clean normalization choice but not derived from an action/Ward identity",
        },
        {
            "gate": "R_rescaling_degeneracy_broken",
            "result": "fail",
            "reason": "without a parent normalization of R, a_F can be moved into the definition of R",
        },
        {
            "gate": "local_F2_overlap_exists",
            "result": "pass_conditional",
            "reason": f"{viable_canonical}/{total_windows} toy local-F2 windows allow canonical a_F=1",
        },
        {
            "gate": "stiff_lambdaR_safe_for_aF1",
            "result": "fail_open",
            "reason": "if lambda_R is stiff, F_2=a_F lambda_R can violate local safety even for a_F=1",
        },
        {
            "gate": "boundary_charge_predicts_aF",
            "result": "fail",
            "reason": "current boundary/source budget is inferred from fitted B_mem, not predicted independently",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "a_F is bounded and has a natural canonical choice, but remains a closure normalization",
        },
    ]


def decision_rows(product_low: float, product_high: float) -> list[dict[str, Any]]:
    return [
        {
            "decision": "aF_status",
            "value": "positive_order_one_and_canonical_unit_viable_but_not_parent_derived",
        },
        {
            "decision": "best_private_closure_choice",
            "value": f"use_a_F_equals_1_as_canonical_trace_normalization_implies_DeltaR_{product_low:.6f}_to_{product_high:.6f}",
        },
        {
            "decision": "hard_blocker",
            "value": "R_rescaling_degeneracy_and_missing_action_Ward_identity",
        },
        {
            "decision": "local_safety_rule",
            "value": "keep_lambda_R_order_one_or_screen_through_gamma_B_so_F2=a_F_lambda_R_stays_small",
        },
        {
            "decision": "next_target",
            "value": "derive_parent_normalization_of_R_or_demote_aF_equals_1_to_explicit_closure_choice",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-trace-coupling-aF-normalization-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    delta_run = latest_delta_run()
    inputs = product_inputs(delta_run)
    products = [item["required_aF_DeltaR"] for item in inputs]
    product_low = min(products)
    product_high = max(products)
    windows = compatibility_rows(product_high)

    write_csv(results_dir / "source_checkpoint_register.csv", source_rows(), ["source", "exists", "role"])
    write_csv(
        results_dir / "flrw_eta1_product_inputs.csv",
        inputs,
        ["run_id", "branch", "B_mem", "eta", "required_aF_DeltaR"],
    )
    write_csv(
        results_dir / "trace_normalization_contract.csv",
        trace_normalization_contract_rows(),
        ["contract_item", "needed_statement", "why_it_matters", "current_status", "result"],
    )
    write_csv(
        results_dir / "aF_candidate_normalizations.csv",
        candidate_rows(product_low, product_high),
        ["candidate", "candidate_aF", "what_it_would_mean", "amplitude_readout", "local_safety_readout", "status"],
    )
    write_csv(
        results_dir / "aF_DeltaR_F2_compatibility.csv",
        windows,
        [
            "DeltaR_cap",
            "lambda_R",
            "F2_cap",
            "aF_low_from_amplitude",
            "aF_high_from_local_F2",
            "window_exists",
            "canonical_aF1_allowed",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "normalization_degeneracies.csv",
        degeneracy_rows(product_low, product_high),
        ["degeneracy", "map", "effect_on_Bmem", "break_condition", "status"],
    )
    write_csv(results_dir / "gate_results.csv", gate_rows(product_low, product_high, windows), ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decision_rows(product_low, product_high), ["decision", "value"])

    canonical_count = sum(1 for row in windows if row["canonical_aF1_allowed"])
    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_delta_run": str(delta_run),
        "readout": "aF_order_one_canonical_viable_not_parent_derived",
        "eta1_required_aF_DeltaR_range": [product_low, product_high],
        "aF_min_if_DeltaR_le1": product_high,
        "aF_min_if_DeltaR_le_half": 2.0 * product_high,
        "canonical_aF1_DeltaR_range": [product_low, product_high],
        "canonical_aF1_toy_local_windows": canonical_count,
        "toy_local_windows_total": len(windows),
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "write checkpoint 95; derive parent normalization of R or label a_F=1 as closure choice",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
