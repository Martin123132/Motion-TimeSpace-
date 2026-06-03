#!/usr/bin/env python3
"""Checkpoint 197: BAO common-mode ratio theorem attempt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_DIR = WORK_DIR.parent / "formalization-workbench"

CHECKPOINT_197_NAME = "BAO-common-mode-ratio-theorem-attempt"
CHECKPOINT_196_RUN = RUNS_ROOT / "20260601-000013-BAO-rd-endpoint-bridge-or-demotion"
CHECKPOINT_195_RUN = RUNS_ROOT / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate"
CHECKPOINT_194_RUN = RUNS_ROOT / "20260601-000011-half-memory-clock-map-derivation-attempt"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"

BAO_MEAN = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_COV = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"

STATUS = "BAO_common_mode_ratio_theorem_conditional_radial_drift_and_alpha_owner_open"
CLAIM_CEILING = "conditional_BAO_ratio_theorem_internal_only_no_parent_alpha_no_support_claim"
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
        (Path(__file__).resolve(), "checkpoint 197 BAO common-mode theorem script"),
        (WORK_DIR / "196-BAO-rd-endpoint-bridge-or-demotion.md", "BAO endpoint bridge gate"),
        (CHECKPOINT_196_RUN / "status.json", "checkpoint 196 machine status"),
        (CHECKPOINT_196_RUN / "results" / "endpoint_policy_candidates.csv", "checkpoint 196 endpoint policy candidates"),
        (CHECKPOINT_196_RUN / "results" / "BAO_theory_contract.csv", "checkpoint 196 BAO theory contract"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint Delta C rule checkpoint"),
        (CHECKPOINT_195_RUN / "status.json", "checkpoint 195 machine status"),
        (WORK_DIR / "194-half-memory-clock-map-derivation-attempt.md", "conformal matter-clock map checkpoint"),
        (CHECKPOINT_194_RUN / "status.json", "checkpoint 194 machine status"),
        (WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md", "locked 2/27 BAO-only empirical score"),
        (WORK_DIR / "124-BAO-shape-residual-decomposition.md", "BAO residual decomposition checkpoint"),
        (CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv", "CAMB acoustic distance/rdrag smoke summary"),
        (BAO_MEAN, "DESI DR2 primary BAO mean vector"),
        (BAO_COV, "DESI DR2 primary BAO covariance"),
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


def load_bao_values() -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    rows: list[dict[str, Any]] = []
    values: list[float] = []
    with BAO_MEAN.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            z_text, value_text, quantity = stripped.split()
            value = float(value_text)
            rows.append({"row": len(rows), "z": float(z_text), "quantity": quantity, "value": value})
            values.append(value)
    covariance = np.loadtxt(BAO_COV)
    return rows, np.array(values), covariance


def scale_chi2(values: np.ndarray, covariance: np.ndarray, factor: float) -> float:
    residual = (factor - 1.0) * values
    precision = np.linalg.inv(covariance)
    return float(residual @ precision @ residual)


def solve_exponent_bound(values: np.ndarray, covariance: np.ndarray, threshold: float) -> tuple[float, float]:
    high = 1.0
    while scale_chi2(values, covariance, math.exp(high * LOCKED_B_MEM / 2.0)) < threshold:
        high *= 2.0
    low = 0.0
    for _ in range(80):
        mid = 0.5 * (low + high)
        if scale_chi2(values, covariance, math.exp(mid * LOCKED_B_MEM / 2.0)) < threshold:
            low = mid
        else:
            high = mid
    exponent_mismatch = 0.5 * (low + high)
    fractional_shift = math.exp(exponent_mismatch * LOCKED_B_MEM / 2.0) - 1.0
    return exponent_mismatch, fractional_shift


def theorem_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use the matter-observer metric tilde_g_munu = exp(C) g_munu.",
            "equation": "d tilde_ell = exp(C/2) d ell and d tilde_tau = exp(C/2) d tau",
            "status": "from_conformal_metric_square_root",
        },
        {
            "step": 2,
            "statement": "For homogeneous saturated C over the BAO survey patch, transverse distances share the same late unit.",
            "equation": "tilde_D_M = exp(C_obs/2) D_M",
            "status": "conditional_on_homogeneous_late_C",
        },
        {
            "step": 3,
            "statement": "The radial distance has the same scaling only if clock drift is negligible.",
            "equation": "tilde_D_H = c/tilde_H = exp(C_obs/2) D_H / (1 + dot_C/(2H))",
            "status": "conditional_radial_drift_gate",
        },
        {
            "step": 4,
            "statement": "The isotropic volume distance inherits the mean scaling when transverse and radial scalings match.",
            "equation": "tilde_D_V = [z tilde_D_M^2 tilde_D_H]^(1/3) ~= exp(C_obs/2) D_V",
            "status": "conditional_on_DH_scaling",
        },
        {
            "step": 5,
            "statement": "The BAO standard ruler must be expressed in the same late matter unit.",
            "equation": "tilde_r_d^(late-unit) = exp(C_obs/2) r_d",
            "status": "common_mode_ruler_calibration_assumption",
        },
        {
            "step": 6,
            "statement": "The conformal unit cancels in BAO ratios.",
            "equation": "tilde_D_X / tilde_r_d = D_X / r_d for X in {M,H,V}",
            "status": "conditional_common_mode_ratio_theorem",
        },
    ]


def observable_transformation_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "D_M",
            "transformation": "tilde_D_M = exp(C_obs/2) D_M",
            "common_mode_exponent": 1.0,
            "condition": "homogeneous late C across survey bin",
            "status": "safe_if_condition_holds",
        },
        {
            "observable": "D_H",
            "transformation": "tilde_D_H = exp(C_obs/2) D_H / (1+dot_C/(2H))",
            "common_mode_exponent": 1.0,
            "condition": "dot_C/H negligible in BAO readout",
            "status": "radial_drift_hazard",
        },
        {
            "observable": "D_V",
            "transformation": "tilde_D_V ~= exp(C_obs/2) D_V when D_H also common-mode",
            "common_mode_exponent": 1.0,
            "condition": "D_M and D_H share scaling",
            "status": "inherits_radial_hazard",
        },
        {
            "observable": "r_d",
            "transformation": "tilde_r_d^(late-unit) = exp(C_obs/2) r_d",
            "common_mode_exponent": 1.0,
            "condition": "drag ruler is calibrated into the same late matter unit",
            "status": "ruler_calibration_theorem_needed",
        },
        {
            "observable": "D_M/r_d",
            "transformation": "tilde_D_M/tilde_r_d = D_M/r_d",
            "common_mode_exponent": 0.0,
            "condition": "D_M and r_d share late unit",
            "status": "ratio_invariant",
        },
        {
            "observable": "D_H/r_d",
            "transformation": "tilde_D_H/tilde_r_d = (D_H/r_d)/(1+dot_C/(2H))",
            "common_mode_exponent": 0.0,
            "condition": "dot_C/H negligible",
            "status": "ratio_invariant_only_if_radial_drift_suppressed",
        },
        {
            "observable": "D_V/r_d",
            "transformation": "tilde_D_V/tilde_r_d ~= D_V/r_d",
            "common_mode_exponent": 0.0,
            "condition": "radial drift suppressed",
            "status": "ratio_invariant_conditionally",
        },
    ]


def tolerance_rows(values: np.ndarray, covariance: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    summary: dict[str, float] = {}
    for threshold in [1.0, 4.0, 9.0, 25.0]:
        exponent_mismatch, fractional_shift = solve_exponent_bound(values, covariance, threshold)
        dotc_over_h = 2.0 * fractional_shift
        rows.append(
            {
                "delta_chi2_threshold": threshold,
                "max_abs_exponent_mismatch_in_units_of_B_over_2": exponent_mismatch,
                "max_abs_fractional_BAO_ratio_shift": fractional_shift,
                "approx_max_abs_dot_C_over_H_for_DH": dotc_over_h,
                "interpretation": "BAO common-mode cancellation tolerance using DESI DR2 covariance",
            }
        )
        summary[f"exponent_bound_chi2_{threshold:g}"] = exponent_mismatch
        summary[f"fractional_shift_bound_chi2_{threshold:g}"] = fractional_shift
        summary[f"dotc_over_h_bound_chi2_{threshold:g}"] = dotc_over_h
    full_half_shift = math.exp(-LOCKED_B_MEM / 2.0) - 1.0
    full_half_chi2 = scale_chi2(values, covariance, math.exp(-LOCKED_B_MEM / 2.0))
    summary["full_half_fractional_shift"] = full_half_shift
    summary["full_half_chi2"] = full_half_chi2
    return rows, summary


def failure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_mode": "denominator-only r_d rescaling",
            "what_breaks": "D_X/r_d receives exp(-B_mem/2)",
            "consequence": "DESI DR2 scale-mode penalty is huge",
            "status": "rejected",
        },
        {
            "failure_mode": "radial clock drift",
            "what_breaks": "D_H/r_d receives 1/(1+dot_C/(2H))",
            "consequence": "DH rows move relative to DM rows",
            "status": "must_bound_or_derive_dot_C_suppression",
        },
        {
            "failure_mode": "inhomogeneous C over survey volume",
            "what_breaks": "different redshift bins or environments receive different unit factors",
            "consequence": "BAO shape distortion, not absorbable by one alpha",
            "status": "needs_environmental_silence",
        },
        {
            "failure_mode": "r_d microphysics changes independently",
            "what_breaks": "the coordinate drag ruler is no longer shared with the late distance model",
            "consequence": "BAO ratio theorem becomes incomplete",
            "status": "partially constrained by CAMB rdrag smoke, not parent-derived",
        },
        {
            "failure_mode": "free alpha treated as proof",
            "what_breaks": "empirical nuisance absorbs scale without a parent owner",
            "consequence": "BAO remains closure-only",
            "status": "forbidden_as_theory_promotion",
        },
    ]


def theorem_contract_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "contract": "common late unit",
            "required_proof": "D_M, D_H, D_V and r_d are all expressed in the same late matter-unit frame",
            "current_evidence": "conformal algebra gives matching exp(C_obs/2) factors if C is homogeneous and saturated",
            "status": "conditional_pass",
        },
        {
            "contract": "radial drift bound",
            "required_proof": "dot_C/H is negligible for BAO radial distances",
            "current_evidence": f"DESI DR2 requires |dot_C/H| roughly below {summary['dotc_over_h_bound_chi2_1']} for delta_chi2<1 scale-mode leakage",
            "status": "bounded_not_parent_derived",
        },
        {
            "contract": "r_d coordinate microphysics",
            "required_proof": "early sound horizon coordinate scale is unchanged or its change is derived consistently",
            "current_evidence": "same-density CAMB smoke changed rdrag only at about 1e-6 fraction",
            "status": "partial_numeric_support",
        },
        {
            "contract": "no anisotropic endpoint leakage",
            "required_proof": "transverse and radial endpoint maps agree except for derived background expansion effects",
            "current_evidence": "checkpoint 124 found DH/rs was a dominant joint-gate penalty",
            "status": "open_shape_hazard",
        },
        {
            "contract": "alpha owner",
            "required_proof": "any BAO alpha used in empirical runs is either a shared nuisance or derived observer calibration",
            "current_evidence": "previous BAO score is empirical and does not parent-own alpha",
            "status": "missing_for_promotion",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    full_half_rejected = summary["full_half_chi2"] > 25.0
    common_mode_tight = summary["fractional_shift_bound_chi2_1"] < 0.005
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal theorem attempt",
        },
        {
            "gate": "BAO ratio theorem algebra written",
            "status": "pass",
            "evidence": "tilde_D_X/tilde_r_d = D_X/r_d when common late unit holds",
            "claim_allowed": "conditional theorem",
        },
        {
            "gate": "naked half-memory leakage rejected",
            "status": "pass" if full_half_rejected else "warning",
            "evidence": f"full_half_chi2={summary['full_half_chi2']}",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "common-mode cancellation tolerance quantified",
            "status": "pass" if common_mode_tight else "warning",
            "evidence": f"delta_chi2_1_fractional_bound={summary['fractional_shift_bound_chi2_1']}",
            "claim_allowed": "numeric tolerance",
        },
        {
            "gate": "radial drift parent-derived",
            "status": "fail",
            "evidence": "dot_C/H suppression is bounded but not derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO alpha parent-owned",
            "status": "fail",
            "evidence": "alpha remains empirical/shared nuisance unless future observer-map theorem owns it",
            "claim_allowed": "closure only",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The BAO common-mode ratio theorem can be written conditionally: homogeneous conformal matter units cancel in D_X/r_d. This saves the endpoint-clock route from the naked half-memory BAO failure, but only if radial drift, r_d microphysics, and alpha ownership are controlled.",
            "full_half_chi2": summary["full_half_chi2"],
            "delta_chi2_1_fractional_shift_bound": summary["fractional_shift_bound_chi2_1"],
            "delta_chi2_1_dot_C_over_H_bound": summary["dotc_over_h_bound_chi2_1"],
            "next_target": "198-BAO-radial-drift-and-alpha-owner-gate.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_197_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    _, values, covariance = load_bao_values()
    theorem_rows = theorem_derivation_rows()
    transform_rows = observable_transformation_rows()
    tolerance, summary = tolerance_rows(values, covariance)
    failures = failure_mode_rows()
    contract = theorem_contract_rows(summary)
    gates = claim_gate_rows(source_rows, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "BAO_ratio_theorem_derivation.csv": (
            theorem_rows,
            ["step", "statement", "equation", "status"],
        ),
        "observable_transformation_table.csv": (
            transform_rows,
            ["observable", "transformation", "common_mode_exponent", "condition", "status"],
        ),
        "BAO_leakage_tolerance.csv": (
            tolerance,
            [
                "delta_chi2_threshold",
                "max_abs_exponent_mismatch_in_units_of_B_over_2",
                "max_abs_fractional_BAO_ratio_shift",
                "approx_max_abs_dot_C_over_H_for_DH",
                "interpretation",
            ],
        ),
        "failure_modes.csv": (
            failures,
            ["failure_mode", "what_breaks", "consequence", "status"],
        ),
        "theorem_contract.csv": (
            contract,
            ["contract", "required_proof", "current_evidence", "status"],
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
                "full_half_chi2",
                "delta_chi2_1_fractional_shift_bound",
                "delta_chi2_1_dot_C_over_H_bound",
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
        "conditional_BAO_ratio_theorem_written": True,
        "full_half_chi2": summary["full_half_chi2"],
        "delta_chi2_1_fractional_shift_bound": summary["fractional_shift_bound_chi2_1"],
        "delta_chi2_1_exponent_bound": summary["exponent_bound_chi2_1"],
        "delta_chi2_1_dot_C_over_H_bound": summary["dotc_over_h_bound_chi2_1"],
        "radial_drift_parent_derived": False,
        "BAO_alpha_parent_owned": False,
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
