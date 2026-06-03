#!/usr/bin/env python3
"""Test whether the pair-ruler half-kernel factor is parent-owned."""

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

RUN_166 = RUNS_ROOT / "20260531-235959-pair-ruler-row-repair-or-demotion-gate"
RUN_167 = RUNS_ROOT / "20260531-235959-no-clock-lead-and-pair-sidecar-test-plan"

STATUS = "half_kernel_contract_constructed_parent_ownership_not_proven"
CLAIM_CEILING = "pair_half_kernel_parent_ownership_gate_no_sidecar_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
    if name.endswith("pair_half_kernel_parent_ownership_gate.py"):
        return "current half-kernel ownership gate"
    if name.startswith("161-"):
        return "base trace/quadrupole source law"
    if name.startswith("162-"):
        return "pair-ruler null-response contract"
    if name.startswith("163-"):
        return "effective pair action owner"
    if name.startswith("166-") or "pair-ruler-row-repair-or-demotion-gate" in str(path):
        return "half-kernel repair evidence"
    if name.startswith("167-") or "no-clock-lead-and-pair-sidecar-test-plan" in str(path):
        return "lead/sidecar governance source"
    return "supporting source"


def source_paths(script_path: Path) -> list[Path]:
    return [
        script_path,
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        WORK_DIR / "162-pair-ruler-operator-null-response-contract.md",
        WORK_DIR / "163-effective-pair-action-owner-attempt.md",
        WORK_DIR / "166-pair-ruler-row-repair-or-demotion-gate.md",
        WORK_DIR / "167-no-clock-lead-and-pair-sidecar-test-plan.md",
        RUN_166 / "status.json",
        RUN_166 / "results" / "repair_variant_scorecard.csv",
        RUN_166 / "results" / "gate_results.csv",
        RUN_166 / "results" / "decision.csv",
        RUN_167 / "status.json",
        RUN_167 / "results" / "branch_lane_assignment.csv",
        RUN_167 / "results" / "claim_boundary_matrix.csv",
        RUN_167 / "results" / "sidecar_test_queue.csv",
    ]


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in source_paths(script_path):
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


def pair_score_rows() -> dict[str, dict[str, str]]:
    scorecard = RUN_166 / "results" / "repair_variant_scorecard.csv"
    return {row["variant"]: row for row in read_csv_rows(scorecard)}


def variational_counting_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route": "ordered_pair_double_count_only",
            "action_domain": "D_x x D_y ordered with symmetric kernel",
            "action_prefactor": 0.5,
            "endpoint_or_variation_multiplicity": 2.0,
            "net_source_factor": 1.0,
            "what_the_half_does": "removes double counting of x,y and y,x",
            "does_it_own_half_kernel": "no",
            "reason": "the endpoint-symmetric variation cancels the bookkeeping half",
        },
        {
            "route": "unordered_pair_measure",
            "action_domain": "(D_x x D_y minus diagonal)/Z2",
            "action_prefactor": 1.0,
            "endpoint_or_variation_multiplicity": 1.0,
            "net_source_factor": 1.0,
            "what_the_half_does": "absorbed into the measure definition",
            "does_it_own_half_kernel": "no",
            "reason": "the unordered measure counts each physical pair once and gives no extra 1/2 source law",
        },
        {
            "route": "single_pair_auxiliary_K_equation",
            "action_domain": "ordered pair integral with K varied as a single pair object",
            "action_prefactor": 0.5,
            "endpoint_or_variation_multiplicity": 1.0,
            "net_source_factor": 0.5,
            "what_the_half_does": "normalizes the source in the K equation of motion",
            "does_it_own_half_kernel": "conditional",
            "reason": "works only if the parent varies K once per unordered pair, not once per endpoint",
        },
        {
            "route": "normal_ordered_connected_pair_current",
            "action_domain": "connected unordered pair current J_pair coupled to K_c",
            "action_prefactor": 0.5,
            "endpoint_or_variation_multiplicity": 1.0,
            "net_source_factor": 0.5,
            "what_the_half_does": "sets the current normalization after one-point contractions are removed",
            "does_it_own_half_kernel": "conditional",
            "reason": "requires an independently normalized conserved pair current, not just a written prefactor",
        },
        {
            "route": "post_hoc_BAO_repair_factor",
            "action_domain": "none",
            "action_prefactor": 0.5,
            "endpoint_or_variation_multiplicity": 1.0,
            "net_source_factor": 0.5,
            "what_the_half_does": "shrinks the BAO projection after residuals are known",
            "does_it_own_half_kernel": "rejected",
            "reason": "data repair is not a parent-action derivation",
        },
    ]
    return rows


def ownership_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "Z2_pair_quotient",
            "required_statement": "the pair sector is defined on unordered pairs or an ordered domain with an explicit Z2 quotient",
            "current_evidence": "163 writes a symmetric 1/2 pair action; 167 marks half-kernel conditional",
            "status": "partial",
            "failure_mode": "the 1/2 is only bookkeeping and does not halve the source law",
        },
        {
            "condition": "single_pair_variation",
            "required_statement": "the variation producing K_c or its source is taken once per physical pair, not once per endpoint",
            "current_evidence": "not specified in 163; no auxiliary K equation has been varied",
            "status": "missing",
            "failure_mode": "endpoint multiplicity cancels the 1/2",
        },
        {
            "condition": "base_law_normalization_origin",
            "required_statement": "the checkpoint-161 B/4 and B/6 laws are shown to be ordered-pair normalizations before quotienting",
            "current_evidence": "161 supplied inserted candidate laws; no parent normalization derivation",
            "status": "missing",
            "failure_mode": "halving them is a new empirical branch rather than a derived quotient",
        },
        {
            "condition": "zero_marginal_preserved",
            "required_statement": "K_c=K_raw-K_x-K_y+K_bar still has zero one-point marginal after the half normalization",
            "current_evidence": "linear rescaling preserves the 163 compensated-kernel identity",
            "status": "pass_conditional",
            "failure_mode": "none for a global scalar half factor",
        },
        {
            "condition": "conservation_or_current_owner",
            "required_statement": "the connected pair current is conserved or otherwise compatible with parent Bianchi/local constraints",
            "current_evidence": "pair current remains an open theorem target",
            "status": "missing",
            "failure_mode": "sidecar can leak into growth/lensing/local conservation inconsistently",
        },
        {
            "condition": "pre_data_normalization_lock",
            "required_statement": "the half factor is fixed before BAO residual scoring and cannot be tuned",
            "current_evidence": "166 tested it as a discrete structural variant after a row-pressure diagnosis",
            "status": "weak",
            "failure_mode": "looks like a repair even if motivated by the action prefactor",
        },
    ]


def exact_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_step": 1,
            "name": "domain",
            "required_formula": "P=(D x D - diagonal)/Z2 or 1/2 integral_DxD for symmetric ordered pairs",
            "reason": "physical pair must be counted once",
        },
        {
            "contract_step": 2,
            "name": "kernel_symmetry",
            "required_formula": "K_c^A_B(x,y)=swap[K_c^A_B(y,x)] with trace/quadrupole eigenstructure",
            "reason": "the unordered pair operator must be well-defined",
        },
        {
            "contract_step": 3,
            "name": "zero_marginal",
            "required_formula": "integral dmu_y W_D(x,y) K_c(x,y)=0 and x<->y",
            "reason": "SN/H(z)/one-point null response cannot be assumed",
        },
        {
            "contract_step": 4,
            "name": "single_pair_source_equation",
            "required_formula": "delta S / delta K_c = 0 gives K_c proportional to 1/2 J_pair, not J_endpoint",
            "reason": "this is the only route that makes the half-kernel physical rather than bookkeeping",
        },
        {
            "contract_step": 5,
            "name": "normalization_link",
            "required_formula": "J_pair normalization maps T=(B/4)F(1-2e^-N), S=(B/6)(1-e^-2N) to T/2,S/2",
            "reason": "must explain why the checkpoint-161 laws are halved",
        },
        {
            "contract_step": 6,
            "name": "conservation_safety",
            "required_formula": "nabla_mu T_pair^{mu nu}=0 or explicit exchange current with zero local/one-point leakage",
            "reason": "Bianchi/local constraints cannot be postponed forever",
        },
        {
            "contract_step": 7,
            "name": "observable_safety",
            "required_formula": "growth/RSD, lensing/slip, and CMB-ruler responses are derived or bounded",
            "reason": "a two-point ruler sidecar can affect other two-point observables",
        },
    ]


def branch_verdict_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    base = scores["base_161_fixed"]
    return [
        {
            "branch": "base_161_pair_ruler",
            "formula": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-2N)",
            "empirical_readout": f"delta_BIC_vs_no_clock={base['delta_BIC_vs_no_clock']}; delta_BIC_vs_LCDM={base['delta_BIC_vs_LCDM']}",
            "ownership_readout": "source laws inserted from checkpoint 161, not parent-varied",
            "verdict": "live_reference_not_lead",
        },
        {
            "branch": "half_kernel_pair_ruler",
            "formula": "T=(B/8)F(1-2e^-N); S=(B/12)(1-e^-2N)",
            "empirical_readout": f"delta_BIC_vs_no_clock={half['delta_BIC_vs_no_clock']}; delta_BIC_vs_base={half['delta_BIC_vs_base_161']}",
            "ownership_readout": "conditional exact contract exists, but 1/2 is not yet derived from a varied parent/source equation",
            "verdict": "best_sidecar_candidate_but_closure_only",
        },
        {
            "branch": "no_clock_lead",
            "formula": "B_mem=2/27; u3=1/4; no pair-ruler projection",
            "empirical_readout": "lead lane from checkpoint 167",
            "ownership_readout": "unaffected by half-kernel ownership failure",
            "verdict": "empirical_lead_remains",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "written_action_prefactor_exists",
            "status": "pass_limited",
            "evidence": "checkpoint 163 writes S_pair with a 1/2 ordered-pair prefactor",
        },
        {
            "gate": "bookkeeping_half_is_enough",
            "status": "fail",
            "evidence": "for endpoint-symmetric variation, the 1/2 is canceled by two endpoint/order contributions",
        },
        {
            "gate": "single_pair_source_equation",
            "status": "fail_open",
            "evidence": "no varied auxiliary K_c equation or conserved pair current has been constructed",
        },
        {
            "gate": "zero_marginal_survives_halving",
            "status": "pass_conditional",
            "evidence": "linear half-rescaling preserves the compensated-kernel zero marginal",
        },
        {
            "gate": "pre_data_parent_ownership",
            "status": "fail_open",
            "evidence": "half-kernel was motivated structurally but tested after residual pressure; parent normalization is not proven",
        },
        {
            "gate": "sidecar_promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "exact contract built, but existing action prefactor does not by itself derive the half-kernel law",
        },
        {
            "item": "half_factor_verdict",
            "verdict": "not_owned_yet",
            "evidence": "bookkeeping 1/2 can be canceled by endpoint/order multiplicity unless a single-pair K equation is derived",
        },
        {
            "item": "sidecar_status",
            "verdict": "best_sidecar_candidate_but_closure_only",
            "evidence": f"half-kernel remains empirically useful with delta_BIC_vs_no_clock={half['delta_BIC_vs_no_clock']} but is not promoted",
        },
        {
            "item": "lead_status",
            "verdict": "no_clock_MTS_remains_empirical_lead",
            "evidence": "half-kernel ownership gap does not weaken the no-clock lead lane",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no CMB/local-GR/parent-action/sidecar promotion",
        },
        {
            "item": "next_target",
            "verdict": "169-no-clock-lead-official-likelihood-refresh-plan.md",
            "evidence": "do not spend the next round on sidecar growth claims until half-kernel ownership or current is derived",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-pair-half-kernel-parent-ownership-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    scores = pair_score_rows()
    counting = variational_counting_rows()
    conditions = ownership_condition_rows()
    contract = exact_contract_rows()
    branches = branch_verdict_rows(scores)
    gates = gate_rows()
    decisions = decision_rows(scores)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "input_runs": [str(RUN_166), str(RUN_167)],
            "test_question": "does the effective pair action own the half-kernel factor before data scoring?",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "variational_counting_table.csv",
        counting,
        [
            "route",
            "action_domain",
            "action_prefactor",
            "endpoint_or_variation_multiplicity",
            "net_source_factor",
            "what_the_half_does",
            "does_it_own_half_kernel",
            "reason",
        ],
    )
    write_csv(
        results_dir / "ownership_conditions.csv",
        conditions,
        ["condition", "required_statement", "current_evidence", "status", "failure_mode"],
    )
    write_csv(
        results_dir / "exact_parent_contract.csv",
        contract,
        ["contract_step", "name", "required_formula", "reason"],
    )
    write_csv(
        results_dir / "branch_verdict_matrix.csv",
        branches,
        ["branch", "formula", "empirical_readout", "ownership_readout", "verdict"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    write_json(
        run_dir / "status.json",
        {
            "status": STATUS,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "half_factor_verdict": "not_owned_yet",
            "sidecar_status": "best_sidecar_candidate_but_closure_only",
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "next_target": "169-no-clock-lead-official-likelihood-refresh-plan.md",
            "generated": [
                "source_register.csv",
                "variational_counting_table.csv",
                "ownership_conditions.csv",
                "exact_parent_contract.csv",
                "branch_verdict_matrix.csv",
                "gate_results.csv",
                "decision.csv",
            ],
        },
    )
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
