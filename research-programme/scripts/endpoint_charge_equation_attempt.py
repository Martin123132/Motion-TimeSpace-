#!/usr/bin/env python3
"""Attempt endpoint charge equations that could produce DeltaR=2/9."""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCES = [
    ("bound_domain_boundary_theorem", POST_CHECKPOINT / "61-bound-domain-boundary-theorem-attempt.md"),
    ("chiD_boundary_variation", POST_CHECKPOINT / "63-chiD-variation-to-boundary-equation-attempt.md"),
    ("binding_invariant_selector", POST_CHECKPOINT / "64-binding-invariant-domain-selector-attempt.md"),
    ("stress_free_reference_gate", POST_CHECKPOINT / "80-stress-free-reference-action-gate.md"),
    ("amplitude_normalization_gate", POST_CHECKPOINT / "82-amplitude-normalization-gate.md"),
    ("canonical_R_theorem_attempt", POST_CHECKPOINT / "97-canonical-R-theorem-attempt.md"),
    ("two_ninth_theorem_attempt", POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md"),
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def quadratic_roots(a: float, b: float, c: float) -> tuple[float, float, float]:
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0:
        raise ValueError("negative discriminant")
    root_low = (-b - math.sqrt(discriminant)) / (2.0 * a)
    root_high = (-b + math.sqrt(discriminant)) / (2.0 * a)
    return root_low, root_high, discriminant


def source_rows() -> list[dict[str, Any]]:
    return [{"source": label, "path": str(path), "exists": path.exists()} for label, path in SOURCES]


def endpoint_equation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    root_low, root_high, discriminant = quadratic_roots(27.0, -12.0, 1.0)
    rows.append(
        {
            "candidate": "spatial_cell_endpoint_quadratic",
            "equation": "27 R^2 - 12 R + 1 = 0",
            "coefficient_origin_attempt": "27=3^3 spatial determinant; 12=3x4 trace times 3+1 cell; 1=unit normalized charge",
            "R_low": root_low,
            "R_high": root_high,
            "DeltaR": root_high - root_low,
            "B_mem_if_eta1_aF1": (root_high - root_low) / 3.0,
            "status": "best_exact_theorem_target_not_action_derived",
            "failure_mode": "no parent variation currently yields this quadratic",
        }
    )

    rows.append(
        {
            "candidate": "trace_square_endpoint_pair",
            "equation": "R_high=1/3; R_low=(1/3)^2",
            "coefficient_origin_attempt": "trace projection endpoint followed by quadratic relaxation endpoint",
            "R_low": 1.0 / 9.0,
            "R_high": 1.0 / 3.0,
            "DeltaR": 2.0 / 9.0,
            "B_mem_if_eta1_aF1": 2.0 / 27.0,
            "status": "equivalent_schema_not_variational",
            "failure_mode": "squaring map is not derived from endpoint dynamics",
        }
    )

    rows.append(
        {
            "candidate": "relative_degree_product",
            "equation": "DeltaR=(2/3)(1/3)",
            "coefficient_origin_attempt": "boundary 2-form over bulk 3-form times spatial trace third",
            "R_low": "",
            "R_high": "",
            "DeltaR": 2.0 / 9.0,
            "B_mem_if_eta1_aF1": 2.0 / 27.0,
            "status": "motivation_only",
            "failure_mode": "degree counting is not a charge equation",
        }
    )

    rows.append(
        {
            "candidate": "built_to_order_polynomial",
            "equation": "(R-1/9)(R-1/3)=0",
            "coefficient_origin_attempt": "roots inserted by hand",
            "R_low": 1.0 / 9.0,
            "R_high": 1.0 / 3.0,
            "DeltaR": 2.0 / 9.0,
            "B_mem_if_eta1_aF1": 2.0 / 27.0,
            "status": "rejected_as_circular",
            "failure_mode": "endpoints are simply imposed after seeing target",
        }
    )
    return rows


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Let R=Q_boundary/Q_* be the normalized endpoint charge entering Gamma_eff.",
            "status": "required_not_derived",
        },
        {
            "step": 2,
            "statement": "Use the existing p=3 route as the spatial determinant coefficient 3^3.",
            "status": "conditional_from_prior_branch",
        },
        {
            "step": 3,
            "statement": "Use the existing u3=1/4 route as the 3+1 cell normalization coefficient 4.",
            "status": "conditional_from_prior_branch",
        },
        {
            "step": 4,
            "statement": "Require endpoint stationarity to produce 3^3 R^2 - 3*4 R + 1 = 0.",
            "status": "new_theorem_target",
        },
        {
            "step": 5,
            "statement": "The two roots are R_today=1/9 and R_early=1/3.",
            "status": "mathematical_consequence_if_step4_holds",
        },
        {
            "step": 6,
            "statement": "DeltaR=R_early-R_today=2/9 and B_mem=DeltaR/3=2/27 on eta=1,a_F=1.",
            "status": "mathematical_consequence_if_parent_contract_holds",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "shortcut": "write polynomial with desired roots",
            "verdict": "reject",
            "reason": "does not remove post-fit circularity",
        },
        {
            "shortcut": "derive from degree counting alone",
            "verdict": "reject_as_derivation",
            "reason": "form degree is not normalized charge without a variational measure",
        },
        {
            "shortcut": "reuse C_coh selector inside parent action",
            "verdict": "reject",
            "reason": "checkpoint 80 demoted this route due stress/reference obstruction",
        },
        {
            "shortcut": "fit endpoint roots branch by branch",
            "verdict": "reject",
            "reason": "would reintroduce the fitted amplitude under endpoint language",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "exact_endpoint_equation_found",
            "result": "pass_as_target",
            "reason": "27R^2-12R+1=0 gives roots 1/9 and 1/3, hence DeltaR=2/9",
        },
        {
            "gate": "coefficients_reuse_existing_branch_numbers",
            "result": "pass_conditional",
            "reason": "27=3^3 from spatial determinant route and 12=3x4 from trace/cell normalization route",
        },
        {
            "gate": "endpoint_equation_parent_derived",
            "result": "fail",
            "reason": "no action variation currently yields the quadratic",
        },
        {
            "gate": "Qstar_charge_unit_derived",
            "result": "fail",
            "reason": "normalized boundary charge unit remains missing",
        },
        {
            "gate": "post_fit_circularity_removed",
            "result": "fail",
            "reason": "the equation was sought after the locked 2/27 branch succeeded",
        },
        {
            "gate": "empirical_branch_upgrade",
            "result": "pass",
            "reason": "2/27 can now be named as a predeclared locked-amplitude branch",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "exact target is not an action theorem",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision": "verdict", "value": "endpoint_quadratic_target_found_not_derived"},
        {"decision": "best_equation_target", "value": "27 R^2 - 12 R + 1 = 0"},
        {"decision": "root_pair", "value": "R_today=1/9; R_early=1/3"},
        {"decision": "DeltaR", "value": 2.0 / 9.0},
        {"decision": "B_mem_eta1_aF1", "value": 2.0 / 27.0},
        {"decision": "promotion_allowed", "value": False},
        {"decision": "claim_ceiling", "value": "exact_endpoint_theorem_target_not_derivation"},
        {"decision": "next_action", "value": "try_to_build_parent_variational_term_for_27R2_minus12R_plus1_or_predeclare_external_holdouts"},
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-endpoint-charge-equation-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"Missing endpoint charge sources: {missing}")

    endpoint_equations = endpoint_equation_rows()
    derivation_chain = derivation_chain_rows()
    no_gos = no_go_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists"])
    write_csv(
        results_dir / "endpoint_equation_candidates.csv",
        endpoint_equations,
        ["candidate", "equation", "coefficient_origin_attempt", "R_low", "R_high", "DeltaR", "B_mem_if_eta1_aF1", "status", "failure_mode"],
    )
    write_csv(results_dir / "derivation_chain.csv", derivation_chain, ["step", "statement", "status"])
    write_csv(results_dir / "no_go_shortcuts.csv", no_gos, ["shortcut", "verdict", "reason"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "best_equation_target": "27 R^2 - 12 R + 1 = 0",
        "DeltaR": 2.0 / 9.0,
        "B_mem_eta1_aF1": 2.0 / 27.0,
        "claim_ceiling": "exact_endpoint_theorem_target_not_derivation",
        "promotion_allowed": False,
        "next_action": "try_to_build_parent_variational_term_for_endpoint_quadratic_or_predeclare_external_holdouts",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
