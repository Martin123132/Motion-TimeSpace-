from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "second-order-beta-response-attempt"
STATUS = "second_order_beta_zero_condition_derived_nonlinear_completion_not_parent_owned"
CLAIM_CEILING = "conditional_beta_zero_condition_no_local_GR_or_official_PPN_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def beta_eff(a1: float, b1: float, epsilon: float) -> float:
    first_order_scale = 1.0 + a1 * epsilon
    second_order_scale = 1.0 + b1 * epsilon
    return second_order_scale / (first_order_scale * first_order_scale)


def beta_linear_coefficient(a1: float, b1: float) -> float:
    return b1 - 2.0 * a1


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "beta manifest and coefficient blocker"),
        (ROOT / "301-epsilon-loc-local-bound-runner.md", "epsilon_loc proxy local-bound runner"),
        (ROOT / "302-epsilon-loc-parent-coefficient-map-attempt.md", "beta second-order target"),
        (ROOT / "runs" / "20260601-000125-epsilon-loc-parent-coefficient-map-attempt" / "results" / "coefficient_derivation.csv", "checkpoint 302 coefficient rows"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def beta_formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "weak_field_g00",
            "formula": "g00=-1+2 A U-2 B U^2+O(U^3)",
            "meaning": "A is the first-order local potential scale; B is the second-order temporal coefficient scale",
            "status": "PPN_parameterization",
        },
        {
            "quantity": "observed_newtonian_potential",
            "formula": "U_obs=A U",
            "meaning": "first-order local measurements absorb A into the fitted GM/Newtonian potential",
            "status": "standard_local_fit_step",
        },
        {
            "quantity": "effective_beta",
            "formula": "beta_eff=B/A^2",
            "meaning": "after fitting the first-order potential, beta is the mismatch between B and A^2",
            "status": "derived_algebraically",
        },
        {
            "quantity": "epsilon_expansion",
            "formula": "A=1+a1 epsilon_loc, B=1+b1 epsilon_loc",
            "meaning": "epsilon_loc leakage affects first and second weak-field coefficients",
            "status": "linearized_contract",
        },
        {
            "quantity": "beta_linear_coefficient",
            "formula": "beta_eff-1=(b1-2a1)epsilon_loc+O(epsilon_loc^2)",
            "meaning": "c_beta=b1-2a1",
            "status": "derived_algebraically",
        },
        {
            "quantity": "beta_zero_condition",
            "formula": "b1=2a1",
            "meaning": "second-order response must track the square of the first-order mass/potential renormalization",
            "status": "conditional_theorem_target",
        },
    ]


def beta_case_rows() -> list[dict[str, Any]]:
    epsilon = 1.0e-5
    cases = [
        {
            "case": "exact_selector_silence",
            "a1": 0.0,
            "b1": 0.0,
            "interpretation": "sigma_D=0 gives no local leakage",
            "status": "pass_exact",
        },
        {
            "case": "GR_mass_renormalization",
            "a1": 1.0,
            "b1": 2.0,
            "interpretation": "A=1+epsilon and B=(1+epsilon)^2 to linear order",
            "status": "conditional_beta_zero",
        },
        {
            "case": "linear_only_trace_leak",
            "a1": 1.0,
            "b1": 0.0,
            "interpretation": "linear potential changes but nonlinear GR completion does not follow",
            "status": "fail_beta_active",
        },
        {
            "case": "half_completed_nonlinear_response",
            "a1": 1.0,
            "b1": 1.0,
            "interpretation": "second-order response partially tracks first-order leakage",
            "status": "fail_beta_active",
        },
        {
            "case": "over_completed_response",
            "a1": 1.0,
            "b1": 3.0,
            "interpretation": "second-order response overshoots the GR mass-renormalization condition",
            "status": "fail_beta_active",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        a1 = float(case["a1"])
        b1 = float(case["b1"])
        c_beta = beta_linear_coefficient(a1, b1)
        beta = beta_eff(a1, b1, epsilon)
        rows.append(
            {
                **case,
                "epsilon_probe": epsilon,
                "c_beta_linear": c_beta,
                "beta_eff_probe": beta,
                "beta_minus_1_probe": beta - 1.0,
                "abs_c_beta_recommended_guard": abs(c_beta),
            }
        )
    return rows


def runner_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "exact_silence",
            "c_beta": 0.0,
            "when_allowed": "sigma_D=0 theorem derived",
            "status": "conditional_exact",
            "why": "no local source means no beta residual",
        },
        {
            "policy": "GR_mass_renormalization",
            "c_beta": 0.0,
            "when_allowed": "parent weak-field equations prove B=A^2 to second order",
            "status": "conditional_promotion_target",
            "why": "local leakage is just fitted GM/mass renormalization",
        },
        {
            "policy": "linear_only_guard",
            "c_beta": 2.0,
            "when_allowed": "nonlinear completion is not derived",
            "status": "recommended_safety_guard",
            "why": "linear-only leak gives beta_eff-1≈-2 epsilon_loc",
        },
        {
            "policy": "old_checkpoint_302_guard",
            "c_beta": 1.0,
            "when_allowed": "superseded",
            "status": "too_optimistic_for_linear_only_leak",
            "why": "does not catch the full linear-only beta mismatch",
        },
    ]


def derivation_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoint inputs exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "beta_formula_derived",
            "status": "pass",
            "evidence": "beta_eff=B/A^2 and c_beta=b1-2a1",
            "claim_effect": "beta blocker is now an exact nonlinear-completion condition",
        },
        {
            "gate": "beta_zero_condition_identified",
            "status": "pass",
            "evidence": "b1=2a1 gives beta_eff=1 to O(epsilon_loc)",
            "claim_effect": "trace-only leakage can be safe if it is GR-like mass renormalization",
        },
        {
            "gate": "parent_proves_B_equals_A_squared",
            "status": "fail",
            "evidence": "no second-order parent weak-field equation proves B=A^2",
            "claim_effect": "beta not promoted",
        },
        {
            "gate": "linear_only_leak_guarded",
            "status": "pass",
            "evidence": "linear-only case gives c_beta=-2, so safety guard should be |c_beta|=2",
            "claim_effect": "local runner can be made more conservative",
        },
        {
            "gate": "official_PPN_claim_allowed",
            "status": "fail",
            "evidence": "beta zero is conditional and parent nonlinear completion missing",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "fifth_force_gradient_closed",
            "status": "fail",
            "evidence": "this beta calculation does not solve spatial trace-source gradients",
            "claim_effect": "fifth-force branch remains open",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "second-order beta map does not derive 2/27 amplitude",
            "claim_effect": "amplitude remains closure/theorem target",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "update_epsilon_runner_beta_guard",
            "task": "change the conservative common-mode beta guard from c_beta=1 to c_beta=2 unless B=A^2 is derived",
            "success_gate": "linear-only fail probe remains safely rejected",
        },
        {
            "priority": 2,
            "target": "derive_B_equals_A_squared",
            "task": "derive second-order local field equations showing trace-only leakage renormalizes mass/GM as A and B=A^2",
            "success_gate": "c_beta=0 becomes parent-owned rather than conditional",
        },
        {
            "priority": 3,
            "target": "fifth_force_gradient_runner",
            "task": "bound gradients of the local trace source for nonzero selectors",
            "success_gate": "bounded leakage has no untested fifth-force channel",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The beta blocker is now exact: after fitting the Newtonian potential, beta_eff=B/A^2. "
                "If A=1+a1 epsilon_loc and B=1+b1 epsilon_loc, then beta_eff-1=(b1-2a1)epsilon_loc. "
                "Thus beta is safe if the parent weak-field solution proves B=A^2, i.e. b1=2a1. "
                "That condition is not yet parent-derived, and a linear-only leak needs a conservative |c_beta|=2 guard."
            ),
            "next_target": "update_epsilon_runner_beta_guard_then_fifth_force_gradient_runner",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "beta_formula.csv": (
            beta_formula_rows(),
            ["quantity", "formula", "meaning", "status"],
        ),
        "beta_cases.csv": (
            beta_case_rows(),
            ["case", "a1", "b1", "interpretation", "status", "epsilon_probe", "c_beta_linear", "beta_eff_probe", "beta_minus_1_probe", "abs_c_beta_recommended_guard"],
        ),
        "runner_policy_update.csv": (
            runner_policy_rows(),
            ["policy", "c_beta", "when_allowed", "status", "why"],
        ),
        "derivation_gates.csv": (
            derivation_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "next_targets.csv": (
            next_target_rows(),
            ["priority", "target", "task", "success_gate"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "beta_formula_derived": True,
        "beta_zero_condition_identified": True,
        "parent_B_equals_A_squared_derived_now": False,
        "recommended_beta_guard_without_completion": 2.0,
        "local_GR_promoted_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "update_epsilon_runner_beta_guard_then_fifth_force_gradient_runner",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Second-order beta response derivation attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
