#!/usr/bin/env python3
"""Attempt a parent variational owner for the endpoint quadratic."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCES = [
    ("canonical_R_theorem_attempt", POST_CHECKPOINT / "97-canonical-R-theorem-attempt.md"),
    ("two_ninth_theorem_attempt", POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md"),
    ("endpoint_charge_equation_attempt", POST_CHECKPOINT / "110-endpoint-charge-equation-attempt.md"),
]

R_LOW = 1.0 / 9.0
R_HIGH = 1.0 / 3.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def potential_u(r_value: float) -> float:
    return 9.0 * r_value**3 - 6.0 * r_value**2 + r_value


def first_derivative(r_value: float) -> float:
    return 27.0 * r_value**2 - 12.0 * r_value + 1.0


def second_derivative(r_value: float) -> float:
    return 54.0 * r_value - 12.0


def source_rows() -> list[dict[str, Any]]:
    return [{"source": label, "path": str(path), "exists": path.exists()} for label, path in SOURCES]


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "determinant_trace_cell_potential",
            "term": "U(R)=9R^3-6R^2+R",
            "variation": "dU/dR=27R^2-12R+1",
            "what_it_would_mean": "cubic determinant self-term competes with trace-cell quadratic term and unit charge source",
            "result": "best_writeable_owner_not_derived",
            "failure_mode": "coefficients are arranged to match the target; no parent symmetry forces them",
        },
        {
            "candidate": "lagrange_multiplier_endpoint_constraint",
            "term": "Lambda(27R^2-12R+1)",
            "variation": "delta_Lambda imposes endpoint quadratic",
            "what_it_would_mean": "endpoint equation is imposed as a constraint",
            "result": "reject_as_derivation",
            "failure_mode": "constraint simply renames the desired result",
        },
        {
            "candidate": "ward_identity_generated_potential",
            "term": "unknown Ward-fixed determinant/trace functional",
            "variation": "would have to yield 27R^2-12R+1",
            "what_it_would_mean": "true parent derivation if a Ward identity fixes coefficients",
            "result": "open_best_future_route",
            "failure_mode": "identity is not available in the current corpus",
        },
        {
            "candidate": "relative_charge_pairing_action",
            "term": "<J_rel,J_rel>_Q + boundary pairing",
            "variation": "could generate charge roots if the pairing metric is fixed",
            "what_it_would_mean": "relative current gives normalized charge dynamics",
            "result": "conditional_only",
            "failure_mode": "charge metric/Q_* and physical representative are not derived",
        },
    ]


def stability_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, r_value in [("R_low_today_candidate", R_LOW), ("R_high_early_candidate", R_HIGH)]:
        curvature = second_derivative(r_value)
        rows.append(
            {
                "root": label,
                "R": r_value,
                "U": potential_u(r_value),
                "dU_dR": first_derivative(r_value),
                "d2U_dR2": curvature,
                "standard_gradient_role_for_U": "minimum" if curvature > 0 else "maximum",
                "standard_gradient_role_for_minus_U": "minimum" if curvature < 0 else "maximum",
            }
        )
    return rows


def arrow_rows() -> list[dict[str, Any]]:
    return [
        {
            "arrow_option": "relax_down_U",
            "flow": "dR/dtau=-gamma dU/dR",
            "endpoint_preference": "R_high=1/3 stable; R_low=1/9 unstable",
            "status": "wrong_default_if_today_is_R_low",
        },
        {
            "arrow_option": "relax_down_minus_U",
            "flow": "dR/dtau=+gamma dU/dR",
            "endpoint_preference": "R_low=1/9 stable; R_high=1/3 unstable",
            "status": "matches_early_high_to_today_low_but_sign_must_be_derived",
        },
        {
            "arrow_option": "first_order_boundary_arrow",
            "flow": "nabla_mu J_R^mu = -gamma A_arrow(C_exp) (27R^2-12R+1)",
            "endpoint_preference": "depends on derived sign of A_arrow",
            "status": "best_contract_not_derived",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "variational_term_can_be_written",
            "result": "pass_formal",
            "reason": "U(R)=9R^3-6R^2+R has derivative 27R^2-12R+1",
        },
        {
            "gate": "coefficients_parent_forced",
            "result": "fail",
            "reason": "no symmetry/Ward identity currently fixes 9,-6,1 or equivalently 27,-12,1",
        },
        {
            "gate": "endpoint_arrow_derived",
            "result": "fail",
            "reason": "standard U makes R_high stable, not R_low; reversing sign needs a derived arrow",
        },
        {
            "gate": "Qstar_charge_metric_derived",
            "result": "fail",
            "reason": "normalized charge measure remains missing",
        },
        {
            "gate": "constraint_trick_rejected",
            "result": "pass",
            "reason": "Lambda times the target equation is labelled as imposition, not derivation",
        },
        {
            "gate": "support_claim_allowed",
            "result": "fail",
            "reason": "formal potential is not a parent action theorem",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision": "verdict", "value": "variational_owner_written_but_not_parent_derived"},
        {"decision": "best_formal_term", "value": "U(R)=9R^3-6R^2+R"},
        {"decision": "variation", "value": "dU/dR=27R^2-12R+1"},
        {"decision": "main_failure", "value": "coefficients_and_endpoint_arrow_not_derived"},
        {"decision": "promotion_allowed", "value": False},
        {"decision": "claim_ceiling", "value": "formal_variational_target_only"},
        {"decision": "next_action", "value": "predeclare_Bmem_2over27_external_holdout_manifest"},
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-endpoint-quadratic-variational-owner-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"Missing variational owner sources: {missing}")

    actions = action_candidate_rows()
    stability = stability_rows()
    arrows = arrow_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists"])
    write_csv(results_dir / "action_candidates.csv", actions, ["candidate", "term", "variation", "what_it_would_mean", "result", "failure_mode"])
    write_csv(results_dir / "stability_table.csv", stability, ["root", "R", "U", "dU_dR", "d2U_dR2", "standard_gradient_role_for_U", "standard_gradient_role_for_minus_U"])
    write_csv(results_dir / "endpoint_arrow_options.csv", arrows, ["arrow_option", "flow", "endpoint_preference", "status"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "result", "reason"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "formal_term": "U(R)=9R^3-6R^2+R",
        "variation": "27R^2-12R+1",
        "claim_ceiling": "formal_variational_target_only",
        "promotion_allowed": False,
        "next_action": "predeclare_Bmem_2over27_external_holdout_manifest",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
