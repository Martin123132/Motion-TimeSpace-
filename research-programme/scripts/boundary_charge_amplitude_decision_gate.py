#!/usr/bin/env python3
"""Decision gate for the locked B_mem=2/27 amplitude after hazard/pressure progress."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
HAZARD_RUN = RUNS_ROOT / "20260531-203000-density-law-hazard-theorem-attempt"
HAZARD_RESULTS = HAZARD_RUN / "results"

DELTA_R_TARGET = 2.0 / 9.0
B_MEM_TARGET = 2.0 / 27.0
CLAIM_CEILING = "amplitude_empirical_closure_boundary_charge_theorem_target"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path, hazard_run: Path) -> list[dict[str, Any]]:
    hazard_results = hazard_run / "results"
    paths = [
        script_path,
        WORK_DIR / "108-two-ninth-fixed-amplitude-robustness.md",
        WORK_DIR / "109-boundary-charge-two-ninth-theorem-attempt.md",
        WORK_DIR / "110-endpoint-charge-equation-attempt.md",
        WORK_DIR / "111-endpoint-quadratic-variational-owner-attempt.md",
        WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md",
        WORK_DIR / "139-density-law-hazard-theorem-attempt.md",
        hazard_run / "status.json",
        hazard_results / "summary.csv",
        hazard_results / "gate_results.csv",
        hazard_results / "decision.csv",
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def endpoint_quadratic_rows() -> list[dict[str, Any]]:
    a = 27.0
    b = -12.0
    c = 1.0
    discriminant = b * b - 4.0 * a * c
    sqrt_disc = math.sqrt(discriminant)
    low = (-b - sqrt_disc) / (2.0 * a)
    high = (-b + sqrt_disc) / (2.0 * a)
    delta_r = high - low
    b_mem = delta_r / 3.0
    return [
        {
            "object": "endpoint_quadratic",
            "expression": "27 R^2 - 12 R + 1 = 0",
            "value": "",
            "status": "formal_target_not_parent_derived",
            "evidence": "coefficients 27 and 12 reuse p=3/u3=1/4 structures but are not Ward-fixed",
        },
        {
            "object": "R_today_low_root",
            "expression": "(12-6)/54",
            "value": low,
            "status": "mathematical_if_quadratic_holds",
            "evidence": "equals 1/9",
        },
        {
            "object": "R_early_high_root",
            "expression": "(12+6)/54",
            "value": high,
            "status": "mathematical_if_quadratic_holds",
            "evidence": "equals 1/3",
        },
        {
            "object": "DeltaR",
            "expression": "R_early - R_today",
            "value": delta_r,
            "status": "mathematical_if_quadratic_holds",
            "evidence": "equals 2/9",
        },
        {
            "object": "B_mem",
            "expression": "DeltaR / 3",
            "value": b_mem,
            "status": "mathematical_if_quadratic_holds",
            "evidence": "equals 2/27, but DeltaR and the projection relation are not fully parent-derived",
        },
        {
            "object": "U_curvature_low_root",
            "expression": "54R - 12 at R=1/9",
            "value": 54.0 * low - 12.0,
            "status": "arrow_problem",
            "evidence": "low endpoint is a maximum for U=9R^3-6R^2+R",
        },
        {
            "object": "U_curvature_high_root",
            "expression": "54R - 12 at R=1/3",
            "value": 54.0 * high - 12.0,
            "status": "arrow_problem",
            "evidence": "high endpoint is a minimum for U=9R^3-6R^2+R",
        },
    ]


def factor_ownership_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor": "activation_shape",
            "target": "A=1-exp(-I_M)",
            "current_owner": "additive hazard / survival composition",
            "status": "pass_conditional",
            "what_is_missing": "parent proof that coherent memory exposure has independent additive increments",
        },
        {
            "factor": "pressure_trace_factor",
            "target": "p=-rho+rho_N/3",
            "current_owner": "coherent-volume spatial metric variation",
            "status": "pass_conditional",
            "what_is_missing": "domain selector D and boundary variation J_rel",
        },
        {
            "factor": "cubic_exposure",
            "target": "I_M=det(Q)=X^3",
            "current_owner": "spatial load determinant contract",
            "status": "pass_conditional",
            "what_is_missing": "parent action deriving Q^i_j",
        },
        {
            "factor": "quarter_scale",
            "target": "u3=1/4",
            "current_owner": "3+1 coherent-cell normalization contract",
            "status": "pass_conditional",
            "what_is_missing": "parent action deriving why 4 normalizes X while exposure remains spatial cubic",
        },
        {
            "factor": "normalized_boundary_contrast",
            "target": "DeltaR=2/9",
            "current_owner": "endpoint quadratic target",
            "status": "fail_not_derived",
            "what_is_missing": "Q_*, endpoint equations, Ward-fixed coefficients, and endpoint arrow",
        },
        {
            "factor": "amplitude",
            "target": "B_mem=DeltaR/3=2/27",
            "current_owner": "locked empirical branch plus formal endpoint target",
            "status": "empirical_closure_not_theorem",
            "what_is_missing": "parent derivation of DeltaR and proof that the 1/3 projection maps boundary contrast to density amplitude",
        },
    ]


def amplitude_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "direct_hazard_derivation",
            "result": "reject_for_amplitude",
            "reason": "hazard composition selects shape, not total released charge",
            "next_action": "do not use hazard law to claim B_mem",
        },
        {
            "route": "degree_counting_product",
            "result": "reject_as_theorem",
            "reason": "(2/3)(1/3) motivates a target but does not define Q_* or dynamics",
            "next_action": "keep only as mnemonic, not derivation",
        },
        {
            "route": "endpoint_quadratic",
            "result": "retain_as_theorem_target",
            "reason": "if 27R^2-12R+1 follows from variation, roots imply DeltaR=2/9",
            "next_action": "derive coefficients and arrow or demote",
        },
        {
            "route": "formal_potential_U",
            "result": "formal_not_parent",
            "reason": "U=9R^3-6R^2+R gives the right derivative but coefficients are arranged and arrow is wrong for simple relaxation",
            "next_action": "require Ward identity or boundary action, no multiplier trick",
        },
        {
            "route": "empirical_locked_branch",
            "result": "retain_as_predeclared_closure",
            "reason": "2/27 survived fixed-amplitude robustness and external late-time gates, but remains empirical",
            "next_action": "use as frozen branch in future tests with no refit",
        },
    ]


def noncircularity_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "roots_not_inserted",
            "status": "fail_for_current_theory",
            "evidence": "the endpoint quadratic was found after the empirical 2/27 branch; coefficients are not parent-forced",
        },
        {
            "test": "Qstar_defined_before_data",
            "status": "fail",
            "evidence": "no action-derived normalized boundary charge unit Q_* exists yet",
        },
        {
            "test": "endpoint_arrow_derived",
            "status": "fail",
            "evidence": "formal U has low root as maximum and high root as minimum for ordinary down-gradient relaxation",
        },
        {
            "test": "shape_amplitude_separated",
            "status": "pass",
            "evidence": "checkpoint 139 explicitly shows hazard law derives shape only",
        },
        {
            "test": "empirical_branch_predeclared_for_future",
            "status": "pass",
            "evidence": "B_mem=2/27 is now treated as frozen closure in future tests, not refit amplitude",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "endpoint_quadratic_math",
            "status": "pass_formal",
            "evidence": "27R^2-12R+1 has roots 1/9 and 1/3, giving DeltaR=2/9 and B_mem=2/27",
        },
        {
            "gate": "endpoint_quadratic_parent_derivation",
            "status": "fail",
            "evidence": "coefficients and charge unit are not derived from an action or Ward identity",
        },
        {
            "gate": "endpoint_arrow",
            "status": "fail",
            "evidence": "formal U stability points opposite to simple early-to-today relaxation unless arrow is derived",
        },
        {
            "gate": "Bmem_amplitude_theorem",
            "status": "fail",
            "evidence": "DeltaR=2/9 remains target, not prediction",
        },
        {
            "gate": "Bmem_empirical_closure",
            "status": "pass",
            "evidence": "locked 2/27 branch remains valid as a predeclared no-refit empirical closure",
        },
        {
            "gate": "shape_mechanics_retained",
            "status": "pass_conditional",
            "evidence": "pressure kernel and hazard shape remain conditional theory progress independent of amplitude proof",
        },
        {
            "gate": "public_theory_promotion",
            "status": "fail",
            "evidence": "amplitude is not parent-derived; no unified field theory claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "amplitude_not_derived_empirical_closure_retained",
            "evidence": "shape and pressure mechanics improved, but B_mem=2/27 still lacks normalized boundary-charge derivation",
        },
        {
            "item": "theory_target",
            "verdict": "endpoint_quadratic_retained_as_exact_target",
            "evidence": "a future parent action must derive 27R^2-12R+1=0 and the endpoint arrow",
        },
        {
            "item": "framework_status",
            "verdict": "locked_memory_is_EFT_closure_not_parent_theorem",
            "evidence": "use B_mem=2/27 as frozen branch for tests, not as derived field-theory prediction",
        },
        {
            "item": "next_target",
            "verdict": "build_consolidated_memory_branch_contract",
            "evidence": "assemble shape, pressure, amplitude status, local-silence conditions, and empirical gates into one branch contract",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, hazard_run: Path = HAZARD_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-boundary-charge-amplitude-decision-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), hazard_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    hazard_status = read_json(hazard_run / "status.json")
    endpoint_math = endpoint_quadratic_rows()
    factor_ownership = factor_ownership_rows()
    routes = amplitude_route_rows()
    tests = noncircularity_test_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "endpoint_quadratic_retest.csv", endpoint_math, ["object", "expression", "value", "status", "evidence"])
    write_csv(results_dir / "factor_ownership_ledger.csv", factor_ownership, ["factor", "target", "current_owner", "status", "what_is_missing"])
    write_csv(results_dir / "amplitude_route_ledger.csv", routes, ["route", "result", "reason", "next_action"])
    write_csv(results_dir / "noncircularity_tests.csv", tests, ["test", "status", "evidence"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": hazard_status["status"],
        "target_values": {
            "DeltaR": DELTA_R_TARGET,
            "B_mem": B_MEM_TARGET,
        },
        "generated": [
            "source_register.csv",
            "endpoint_quadratic_retest.csv",
            "factor_ownership_ledger.csv",
            "amplitude_route_ledger.csv",
            "noncircularity_tests.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "build_consolidated_memory_branch_contract",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--hazard-run", type=Path, default=HAZARD_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.hazard_run))


if __name__ == "__main__":
    main()
