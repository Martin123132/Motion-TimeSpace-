#!/usr/bin/env python3
"""Checkpoint 194: derive or bound the half-memory clock-map bridge."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_194_NAME = "half-memory-clock-map-derivation-attempt"
CHECKPOINT_193_RUN = RUNS_ROOT / "20260601-000010-calibration-bridge-H0-owner-or-demotion"
CHECKPOINT_192_RUN = RUNS_ROOT / "20260601-000009-theta-H0-compensation-derivation-attempt"

STATUS = "half_memory_clock_map_metric_sqrt_candidate_domain_rule_missing"
CLAIM_CEILING = "metric_clock_map_candidate_only_no_parent_action_no_CMB_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LOCKED_B_MEM = 2.0 / 27.0


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 194 half-memory clock-map script"),
        (WORK_DIR / "193-calibration-bridge-H0-owner-or-demotion.md", "H0 calibration bridge checkpoint"),
        (CHECKPOINT_193_RUN / "status.json", "checkpoint 193 machine status"),
        (CHECKPOINT_193_RUN / "results" / "calibration_bridge_candidates.csv", "checkpoint 193 candidate table"),
        (CHECKPOINT_193_RUN / "results" / "inferred_B_from_H0_ratio.csv", "checkpoint 193 B ratio readout"),
        (CHECKPOINT_193_RUN / "results" / "candidate_derivation_contract.csv", "checkpoint 193 derivation contract"),
        (WORK_DIR / "192-theta-H0-compensation-derivation-attempt.md", "FLRW distance-response checkpoint"),
        (CHECKPOINT_192_RUN / "status.json", "checkpoint 192 machine status"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def conformal_clock_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Introduce a matter-observer metric tilde_g_munu = exp(C) g_munu.",
            "derivation": "For a comoving observer, d_tilde_tau^2 = -tilde_g_00 dt^2 = exp(C) d_tau^2.",
            "result": "d_tilde_tau = exp(C/2) d_tau",
            "status": "factor_half_derived_from_metric_square_root",
        },
        {
            "step": 2,
            "statement": "The spatial ruler also scales as tilde_a = exp(C/2) a for a pure conformal map.",
            "derivation": "tilde_g_ij = exp(C) a^2 gamma_ij, so the physical scale factor is exp(C/2) a.",
            "result": "tilde_a = exp(C/2) a",
            "status": "requires_domain_rule_for_late_rulers",
        },
        {
            "step": 3,
            "statement": "Compute the measured expansion rate in the tilde-clock frame.",
            "derivation": "tilde_H = (1/tilde_a) d(tilde_a)/d_tilde_tau = exp(-C/2)(H + dot_C/2).",
            "result": "tilde_H = exp(-C/2)(H + dot_C/2)",
            "status": "exact_for_FLRW_conformal_map",
        },
        {
            "step": 4,
            "statement": "If C is saturated or slowly varying at readout, dot_C/H is negligible.",
            "derivation": "tilde_H/H = exp(-C/2)(1 + dot_C/(2H)).",
            "result": "tilde_H ~= H exp(-C/2)",
            "status": "conditional_bridge",
        },
        {
            "step": 5,
            "statement": "Set the saturated memory jump C = B_mem.",
            "derivation": "The bridge becomes H_CMB = H_late exp(-B_mem/2).",
            "result": "half-memory exponential H0 bridge",
            "status": "metric_sqrt_derives_factor_half_but_not_C_equals_Bmem",
        },
    ]


def h0_bridge_rows(status_193: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    late_h0 = float(status_193["late_reference_H0"])
    cmb_h0 = float(status_193["CMB_profile_H0"])
    exp_pred = late_h0 * math.exp(-LOCKED_B_MEM / 2.0)
    lin_pred = late_h0 * (1.0 - LOCKED_B_MEM / 2.0)
    ratio = cmb_h0 / late_h0
    inferred_c = -2.0 * math.log(ratio)
    delta_c = inferred_c - LOCKED_B_MEM
    epsilon_required = cmb_h0 / exp_pred - 1.0
    cdot_over_h_required = 2.0 * epsilon_required
    rows = [
        {
            "quantity": "late_reference_H0",
            "value": late_h0,
            "definition": "H0 before the half-memory calibration map",
            "status": "input_from_checkpoint_193",
        },
        {
            "quantity": "same_density_CMB_profile_H0",
            "value": cmb_h0,
            "definition": "H0 required by theta profiling in the same-density CMB branch",
            "status": "input_from_checkpoint_193",
        },
        {
            "quantity": "exp_half_memory_prediction",
            "value": exp_pred,
            "definition": "H_late exp(-B_mem/2)",
            "status": "best_bridge_candidate",
        },
        {
            "quantity": "exp_half_memory_error",
            "value": exp_pred - cmb_h0,
            "definition": "predicted minus profiled CMB H0",
            "status": "small_residual",
        },
        {
            "quantity": "linear_half_memory_prediction",
            "value": lin_pred,
            "definition": "H_late (1-B_mem/2)",
            "status": "linearized_sidecar",
        },
        {
            "quantity": "inferred_C_from_ratio",
            "value": inferred_c,
            "definition": "-2 ln(H_CMB/H_late)",
            "status": "close_to_locked_B_mem",
        },
        {
            "quantity": "delta_C_vs_Bmem",
            "value": delta_c,
            "definition": "inferred_C_from_ratio - B_mem",
            "status": "residual_memory_budget",
        },
        {
            "quantity": "epsilon_required_after_exp_bridge",
            "value": epsilon_required,
            "definition": "H_CMB/(H_late exp(-B/2))-1",
            "status": "dimensionless_residual_rate_term",
        },
        {
            "quantity": "required_dot_C_over_H",
            "value": cdot_over_h_required,
            "definition": "2 epsilon_required if residual is interpreted as dot_C/(2H)",
            "status": "tiny_derivative_or_calibration_residual",
        },
    ]
    summary = {
        "late_h0": late_h0,
        "cmb_h0": cmb_h0,
        "exp_pred": exp_pred,
        "exp_error": exp_pred - cmb_h0,
        "lin_pred": lin_pred,
        "lin_error": lin_pred - cmb_h0,
        "ratio": ratio,
        "inferred_c": inferred_c,
        "delta_c": delta_c,
        "epsilon_required": epsilon_required,
        "cdot_over_h_required": cdot_over_h_required,
    }
    return rows, summary


def derivative_residual_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "interpretation": "zero_derivative_saturated_clock",
            "condition": "dot_C/H = 0 and C=B_mem",
            "predicted_H0_error": summary["exp_error"],
            "residual_requirement": "leaves a 0.0135 km/s/Mpc mismatch",
            "status": "already_close",
        },
        {
            "interpretation": "small_derivative_correction",
            "condition": "tilde_H = exp(-C/2) H (1+dot_C/(2H))",
            "predicted_H0_error": 0.0,
            "residual_requirement": f"dot_C/H={summary['cdot_over_h_required']}",
            "status": "allowed_as_bound_not_derived",
        },
        {
            "interpretation": "small_C_offset",
            "condition": "C=B_mem+delta_C",
            "predicted_H0_error": 0.0,
            "residual_requirement": f"delta_C={summary['delta_c']}",
            "status": "allowed_as_bound_not_derived",
        },
    ]


def domain_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "universal_constant_conformal_map",
            "mechanism": "same constant clock/ruler rescaling applies to every observable",
            "benefit": "derives the half factor cleanly",
            "failure_mode": "risks shifting late SN/BAO/H(z) calibration as well, erasing the intended H0 split",
            "status": "insufficient_without_domain_rule",
        },
        {
            "route": "endpoint_memory_CMB_map",
            "mechanism": "CMB inference compares an early ruler to a late clock across a saturated memory jump",
            "benefit": "naturally exposes exp(-Delta C/2) to CMB-inferred H0",
            "failure_mode": "needs derivation that late local ladders absorb common local calibration",
            "status": "best_derivation_target",
        },
        {
            "route": "local_common_mode_absorption",
            "mechanism": "locally calibrated late observables use clocks and rulers in the same memory frame",
            "benefit": "constant conformal factor cancels in local dimensionless late measurements",
            "failure_mode": "must be proven for SN/BAO/H(z), not assumed",
            "status": "needed_side_condition",
        },
        {
            "route": "branch_switching_by_hand",
            "mechanism": "choose late H0 for late data and rescaled H0 for CMB data without an observer rule",
            "benefit": "fits the numerical split",
            "failure_mode": "post-hoc and not field-theoretic",
            "status": "rejected",
        },
    ]


def parent_action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "matter metric coupling",
            "required_derivation": "parent action contains S_matter[psi, exp(C) g_munu] or a dynamically equivalent observer metric",
            "acceptance_test": "the factor 1/2 follows from the metric square root in the matter clock",
            "status": "candidate_form_written_not_parent_derived",
        },
        {
            "contract": "memory identification",
            "required_derivation": "the saturated clock-map variable obeys Delta C = B_mem = 2/27",
            "acceptance_test": "B_mem is produced by the action or a theorem, not by empirical lock",
            "status": "missing",
        },
        {
            "contract": "slow/saturated readout",
            "required_derivation": "dot_C/H is zero or bounded near the H0 readout",
            "acceptance_test": f"|dot_C/H| must be at or below about {abs(2.0 * (load_json(CHECKPOINT_193_RUN / 'status.json')['CMB_profile_H0'] / load_json(CHECKPOINT_193_RUN / 'status.json')['exp_half_memory_H0'] - 1.0))}",
            "status": "bounded_not_derived",
        },
        {
            "contract": "late/CMB domain rule",
            "required_derivation": "CMB sees the endpoint memory map while late local calibrators absorb common clock/ruler scaling",
            "acceptance_test": "same rule preserves SN/BAO/H(z) and the same-density CMB bridge",
            "status": "missing",
        },
        {
            "contract": "local GR silence",
            "required_derivation": "local fixed point suppresses gradients and clock drift of C",
            "acceptance_test": "no local PPN or clock violation is introduced by exp(C) matter metric",
            "status": "missing",
        },
        {
            "contract": "perturbation consistency",
            "required_derivation": "C perturbations do not reintroduce forbidden CMB or growth residuals",
            "acceptance_test": "replace high-cs closure with parent-owned perturbation equations",
            "status": "missing",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    half_factor_derived = True
    residual_small = abs(summary["exp_error"]) < 0.05
    derivative_bound_small = abs(summary["cdot_over_h_required"]) < 0.001
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal derivation attempt only",
        },
        {
            "gate": "factor one-half derived",
            "status": "pass" if half_factor_derived else "fail",
            "evidence": "d_tilde_tau=exp(C/2)d_tau from tilde_g=exp(C)g",
            "claim_allowed": "metric-clock algebra",
        },
        {
            "gate": "half-memory H0 bridge remains close",
            "status": "pass" if residual_small else "warning",
            "evidence": f"error_H0={summary['exp_error']}",
            "claim_allowed": "theorem target",
        },
        {
            "gate": "residual derivative budget small",
            "status": "pass" if derivative_bound_small else "warning",
            "evidence": f"required_dot_C_over_H={summary['cdot_over_h_required']}",
            "claim_allowed": "bound only",
        },
        {
            "gate": "Delta C equals B_mem derived",
            "status": "fail",
            "evidence": "C=B_mem is identified, not parent-derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "late/CMB domain rule derived",
            "status": "fail",
            "evidence": "need proof that late local calibration absorbs common map while CMB sees endpoint jump",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The exp(-B_mem/2) factor can be motivated by a conformal matter-clock map, where the half arises from the square root of the metric. The domain rule and parent action are still missing.",
            "exp_half_memory_H0": summary["exp_pred"],
            "exp_half_memory_error_H0": summary["exp_error"],
            "required_dot_C_over_H": summary["cdot_over_h_required"],
            "inferred_C_from_ratio": summary["inferred_c"],
            "delta_C_vs_Bmem": summary["delta_c"],
            "next_target": "195-late-CMB-domain-rule-and-local-silence-gate.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_194_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    status_193 = load_json(CHECKPOINT_193_RUN / "status.json")
    source_rows = source_register_rows()
    algebra_rows = conformal_clock_map_rows()
    bridge_rows, summary = h0_bridge_rows(status_193)
    derivative_rows = derivative_residual_rows(summary)
    domain_rows = domain_rule_rows()
    contract_rows = parent_action_contract_rows()
    gates = claim_gate_rows(source_rows, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "conformal_clock_map_algebra.csv": (
            algebra_rows,
            ["step", "statement", "derivation", "result", "status"],
        ),
        "H0_bridge_check.csv": (
            bridge_rows,
            ["quantity", "value", "definition", "status"],
        ),
        "derivative_residual_budget.csv": (
            derivative_rows,
            ["interpretation", "condition", "predicted_H0_error", "residual_requirement", "status"],
        ),
        "late_CMB_domain_rule_options.csv": (
            domain_rows,
            ["route", "mechanism", "benefit", "failure_mode", "status"],
        ),
        "parent_action_contract.csv": (
            contract_rows,
            ["contract", "required_derivation", "acceptance_test", "status"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "exp_half_memory_H0",
                "exp_half_memory_error_H0",
                "required_dot_C_over_H",
                "inferred_C_from_ratio",
                "delta_C_vs_Bmem",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "factor_half_derived_from_metric_sqrt": True,
        "exp_half_memory_H0": summary["exp_pred"],
        "exp_half_memory_error_H0": summary["exp_error"],
        "required_dot_C_over_H": summary["cdot_over_h_required"],
        "inferred_C_from_ratio": summary["inferred_c"],
        "delta_C_vs_Bmem": summary["delta_c"],
        "Delta_C_equals_Bmem_parent_derived": False,
        "late_CMB_domain_rule_derived": False,
        "local_silence_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
