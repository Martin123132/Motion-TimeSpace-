#!/usr/bin/env python3
"""Attempt an effective pair-action owner for the BAO ruler kernel."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

NULL_RUN = RUNS_ROOT / "20260531-235959-pair-ruler-operator-null-response-contract"
NULL_RESULTS = NULL_RUN / "results"
SOURCE_LAW_RUN = RUNS_ROOT / "20260531-235959-trace-quadrupole-source-law-attempt"
SOURCE_LAW_RESULTS = SOURCE_LAW_RUN / "results"

CLAIM_CEILING = "effective_pair_action_owner_attempt_no_bridge_promotion"
STATUS = "connected_compensated_pair_action_constructed_not_fundamental_parent_derived"


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("163-") or name.endswith("effective_pair_action_owner_attempt.py"):
        return "current effective pair-action owner attempt"
    if name.startswith("162-") or "pair-ruler-operator-null-response-contract" in str(path):
        return "pair-ruler null-response contract"
    if name.startswith("161-") or "trace-quadrupole-source-law" in str(path):
        return "trace/quadrupole source-law candidate"
    if name.startswith("160-"):
        return "ruler tensor decomposition"
    if name.startswith("53-") or name.startswith("54-"):
        return "coherent domain/local silence"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "160-ruler-projection-parent-tensor-attempt.md",
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        WORK_DIR / "162-pair-ruler-operator-null-response-contract.md",
        SOURCE_LAW_RUN / "status.json",
        SOURCE_LAW_RESULTS / "equation_contract.csv",
        SOURCE_LAW_RESULTS / "combined_projection_scorecard.csv",
        NULL_RUN / "status.json",
        NULL_RESULTS / "operator_condition_contract.csv",
        NULL_RESULTS / "theorem_chain.csv",
        NULL_RESULTS / "gate_results.csv",
        NULL_RESULTS / "decision.csv",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def compensated_kernel_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "object": "raw finite-pair kernel",
            "formula": "K_raw^A_B(x,y)=T_D h^A_B+S_D(n^A n_B-h^A_B/3)",
            "result": "finite-pair BAO response exists",
            "status": "from_160_161",
        },
        {
            "step": 2,
            "object": "x-marginal",
            "formula": "K_x^A_B(x)=integral dmu_y W(x,y) K_raw^A_B(x,y)",
            "result": "one-point leakage term",
            "status": "must_subtract",
        },
        {
            "step": 3,
            "object": "y-marginal",
            "formula": "K_y^A_B(y)=integral dmu_x W(x,y) K_raw^A_B(x,y)",
            "result": "opposite one-point leakage term",
            "status": "must_subtract",
        },
        {
            "step": 4,
            "object": "domain mean",
            "formula": "K_bar^A_B=integral dmu_x dmu_y W(x,y) K_raw^A_B(x,y)",
            "result": "restores pair normalization after marginal subtraction",
            "status": "must_add_back",
        },
        {
            "step": 5,
            "object": "connected compensated kernel",
            "formula": "K_c=K_raw-K_x-K_y+K_bar",
            "result": "integral dmu_y W K_c=0 and integral dmu_x W K_c=0",
            "status": "algebraic_pass",
        },
        {
            "step": 6,
            "object": "response split",
            "formula": "delta O_1 proportional to marginal(K_c)=0; delta O_2 proportional to K_c(x,y)",
            "result": "one-point null response with finite pair response",
            "status": "conditional_pass",
        },
    ]


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "raw_bilocal_pair_action",
            "formula": "S_pair~integral dmu_x dmu_y delta_g(x)delta_g(y) ell_A K_raw^A_B ell^B",
            "what_it_owns": "finite-pair BAO response",
            "status": "incomplete",
            "failure": "raw kernel can have one-point marginal leakage",
            "next_action": "replace with connected/compensated kernel",
        },
        {
            "candidate": "connected_compensated_pair_action",
            "formula": "S_pair~1/2 integral dmu_x dmu_y :delta_g(x)delta_g(y): ell_A K_c^A_B ell^B",
            "what_it_owns": "zero one-point marginal and finite pair response",
            "status": "best_effective_owner",
            "failure": "effective/coarse-grained, not fundamental parent action yet",
            "next_action": "derive from MTS coherent-domain current or parent field integration",
        },
        {
            "candidate": "conserved_pair_current_action",
            "formula": "S_pair~integral J_pair^AB K_c_AB with nabla_A J_pair^AB=0",
            "what_it_owns": "possible conservation identity for zero marginal",
            "status": "open_theorem_target",
            "failure": "J_pair not constructed",
            "next_action": "attempt pair-current origin only if effective action remains viable",
        },
        {
            "candidate": "local_parent_action_direct",
            "formula": "S_parent[g,fields] local; K_c emerges after coarse-graining",
            "what_it_owns": "true field-theory status",
            "status": "missing",
            "failure": "no derivation from local parent variables",
            "next_action": "long-term parent-action work",
        },
        {
            "candidate": "BAO_likelihood_patch",
            "formula": "shift D_M,D_H in the likelihood only",
            "what_it_owns": "data fit",
            "status": "rejected",
            "failure": "not theory",
            "next_action": "forbidden except as diagnostic closure",
        },
    ]


def response_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "background expansion",
            "linear_variation": "delta S_pair/delta background at <delta_g>=0",
            "result": "zero_if_normal_ordered_and_compensated",
            "reason": "connected pair density has no one-point contraction",
            "remaining_risk": "backreaction at higher order not derived",
        },
        {
            "observable": "SN luminosity distance",
            "linear_variation": "no direct photon/geodesic coupling in S_pair",
            "result": "zero_conditional",
            "reason": "action acts on galaxy-pair/ruler sector, not null geodesics",
            "remaining_risk": "must prove no hidden metric or source-redshift coupling",
        },
        {
            "observable": "cosmic chronometer H(z)",
            "linear_variation": "no clock/lapse/background deformation",
            "result": "zero_conditional",
            "reason": "zero one-point marginal removes one-point expansion response",
            "remaining_risk": "higher-order/background renormalization open",
        },
        {
            "observable": "BAO correlation peak",
            "linear_variation": "delta xi_BAO from K_c at finite separation",
            "result": "nonzero",
            "reason": "finite pair kernel survives marginal subtraction",
            "remaining_risk": "must run fixed source laws through official BAO covariance",
        },
        {
            "observable": "growth/RSD/lensing two-point statistics",
            "linear_variation": "may inherit connected pair action",
            "result": "open_not_null",
            "reason": "operator is explicitly two-point",
            "remaining_risk": "must be tested as a consistency gate",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths",
            "status": "pass",
            "evidence": "all required source paths exist",
        },
        {
            "gate": "compensated_kernel_identity",
            "status": "pass_algebraic",
            "evidence": "K_c=K_raw-K_x-K_y+K_bar has zero x/y marginals by construction",
        },
        {
            "gate": "effective_pair_action",
            "status": "conditional_pass",
            "evidence": "normal-ordered connected pair action can own finite-pair response without one-point linear response",
        },
        {
            "gate": "fundamental_parent_action",
            "status": "fail_open",
            "evidence": "compensated action is an effective/coarse-grained ansatz, not derived from local parent fields",
        },
        {
            "gate": "source_law_insertion",
            "status": "fail_open",
            "evidence": "T_D and S_D from 161 are inserted into K_raw, not varied from the action",
        },
        {
            "gate": "SN_Hz_null",
            "status": "conditional_pass",
            "evidence": "holds at leading order only if no metric/clock/geodesic coupling and compensated marginal is exact",
        },
        {
            "gate": "lensing_growth",
            "status": "open_mandatory",
            "evidence": "two-point observables may be changed; this must become a test, not an ignored issue",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "a connected compensated effective pair action can own zero one-point marginal algebraically, but it is not a fundamental parent derivation",
        },
        {
            "item": "best_candidate",
            "verdict": "S_pair~1/2 integral :delta_g(x)delta_g(y): ell_A K_c^A_B ell^B",
            "evidence": "normal ordering and compensated kernel remove one-point leakage while retaining finite-pair response",
        },
        {
            "item": "kernel_owner",
            "verdict": "K_c=K_raw-K_x-K_y+K_bar",
            "evidence": "zero marginal is algebraically guaranteed for normalized domain measure",
        },
        {
            "item": "what_improved",
            "verdict": "zero marginal is now constructed, not merely demanded",
            "evidence": "162 open condition becomes an effective-action theorem target",
        },
        {
            "item": "what_still_fails",
            "verdict": "fundamental parent action and source-law variation still missing",
            "evidence": "connected compensated action is effective/coarse-grained and still inserts 161 source laws",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no bridge promotion; no CMB/local-GR claim",
        },
        {
            "item": "next_target",
            "verdict": "164-fixed-pair-ruler-branch-smoke.md",
            "evidence": "run a fixed trace/quadrupole pair-ruler branch against SN+BAO/H(z) without adding fitted BAO knobs",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-effective-pair-action-owner-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    proof = compensated_kernel_proof_rows()
    actions = action_candidate_rows()
    responses = response_proof_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "compensated_kernel_proof.csv", proof, ["step", "object", "formula", "result", "status"])
    write_csv(
        results_dir / "action_candidate_ledger.csv",
        actions,
        ["candidate", "formula", "what_it_owns", "status", "failure", "next_action"],
    )
    write_csv(
        results_dir / "response_proof_matrix.csv",
        responses,
        ["observable", "linear_variation", "result", "reason", "remaining_risk"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "best_candidate": "connected_compensated_pair_action",
        "kernel_owner": "K_c=K_raw-K_x-K_y+K_bar",
        "generated": [
            "source_register.csv",
            "compensated_kernel_proof.csv",
            "action_candidate_ledger.csv",
            "response_proof_matrix.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "164-fixed-pair-ruler-branch-smoke.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_attempt(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
