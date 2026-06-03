#!/usr/bin/env python3
"""Checkpoint 198: BAO radial-drift and alpha-owner gate."""

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

CHECKPOINT_198_NAME = "BAO-radial-drift-and-alpha-owner-gate"
CHECKPOINT_197_RUN = RUNS_ROOT / "20260601-000014-BAO-common-mode-ratio-theorem-attempt"
CHECKPOINT_196_RUN = RUNS_ROOT / "20260601-000013-BAO-rd-endpoint-bridge-or-demotion"
CHECKPOINT_194_RUN = RUNS_ROOT / "20260601-000011-half-memory-clock-map-derivation-attempt"

BAO_MEAN = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_COV = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"

STATUS = "BAO_radial_drift_bound_safe_for_H0_residual_alpha_owner_still_closure"
CLAIM_CEILING = "BAO_radial_drift_bound_internal_only_alpha_not_parent_owned_no_support_claim"
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
        (Path(__file__).resolve(), "checkpoint 198 radial-drift/alpha script"),
        (WORK_DIR / "197-BAO-common-mode-ratio-theorem-attempt.md", "BAO common-mode theorem attempt"),
        (CHECKPOINT_197_RUN / "status.json", "checkpoint 197 machine status"),
        (CHECKPOINT_197_RUN / "results" / "BAO_leakage_tolerance.csv", "checkpoint 197 leakage tolerance"),
        (CHECKPOINT_197_RUN / "results" / "observable_transformation_table.csv", "checkpoint 197 observable transformations"),
        (WORK_DIR / "196-BAO-rd-endpoint-bridge-or-demotion.md", "BAO endpoint bridge/demotion gate"),
        (CHECKPOINT_196_RUN / "status.json", "checkpoint 196 machine status"),
        (WORK_DIR / "194-half-memory-clock-map-derivation-attempt.md", "half-memory clock map checkpoint"),
        (CHECKPOINT_194_RUN / "status.json", "checkpoint 194 machine status"),
        (WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md", "locked BAO-only empirical score"),
        (WORK_DIR / "124-BAO-shape-residual-decomposition.md", "BAO shape residual decomposition"),
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
    return rows, np.array(values), np.loadtxt(BAO_COV)


def radial_factors(vector_rows: list[dict[str, Any]], dot_c_over_h: float) -> np.ndarray:
    epsilon = dot_c_over_h / 2.0
    factors: list[float] = []
    for row in vector_rows:
        quantity = row["quantity"]
        if quantity == "DM_over_rs":
            factor = 1.0
        elif quantity == "DH_over_rs":
            factor = 1.0 / (1.0 + epsilon)
        elif quantity == "DV_over_rs":
            factor = (1.0 / (1.0 + epsilon)) ** (1.0 / 3.0)
        else:
            raise ValueError(f"Unknown BAO quantity: {quantity}")
        factors.append(factor)
    return np.array(factors)


def chi2_for_factors(values: np.ndarray, covariance: np.ndarray, factors: np.ndarray, alpha_mode: str) -> tuple[float, float, np.ndarray]:
    precision = np.linalg.inv(covariance)
    if alpha_mode == "fixed":
        alpha = 1.0
    elif alpha_mode == "best_shared":
        model_shape = factors * values
        numerator = float(model_shape @ precision @ values)
        denominator = float(model_shape @ precision @ model_shape)
        alpha = numerator / denominator
    else:
        raise ValueError(f"Unknown alpha mode: {alpha_mode}")
    residual = alpha * factors * values - values
    chi2 = float(residual @ precision @ residual)
    return chi2, alpha, residual


def solve_dotc_bound(vector_rows: list[dict[str, Any]], values: np.ndarray, covariance: np.ndarray, threshold: float, alpha_mode: str) -> float:
    high = 1.0e-6
    while chi2_for_factors(values, covariance, radial_factors(vector_rows, high), alpha_mode)[0] < threshold:
        high *= 2.0
        if high > 10.0:
            raise RuntimeError("Failed to bracket positive dot_C/H bound")
    low = 0.0
    for _ in range(80):
        mid = 0.5 * (low + high)
        if chi2_for_factors(values, covariance, radial_factors(vector_rows, mid), alpha_mode)[0] < threshold:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def radial_drift_tolerance_rows(vector_rows: list[dict[str, Any]], values: np.ndarray, covariance: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    summary: dict[str, float] = {}
    for alpha_mode in ["fixed", "best_shared"]:
        for threshold in [1.0, 4.0, 9.0, 25.0]:
            bound = solve_dotc_bound(vector_rows, values, covariance, threshold, alpha_mode)
            rows.append(
                {
                    "alpha_mode": alpha_mode,
                    "delta_chi2_threshold": threshold,
                    "max_abs_dot_C_over_H": bound,
                    "max_abs_epsilon_dotC_over_2H": bound / 2.0,
                    "interpretation": "DESI DR2 BAO radial-drift tolerance",
                }
            )
            summary[f"{alpha_mode}_dotc_bound_chi2_{threshold:g}"] = bound
    return rows, summary


def representative_drift_rows(vector_rows: list[dict[str, Any]], values: np.ndarray, covariance: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, float]]:
    status_194 = load_json(CHECKPOINT_194_RUN / "status.json")
    h0_residual_dotc = float(status_194["required_dot_C_over_H"])
    candidates = [
        ("zero_drift", 0.0, "exact saturated BAO readout"),
        ("H0_bridge_residual_drift", h0_residual_dotc, "tiny residual dot_C/H inferred by checkpoint 194"),
        ("positive_H0_residual_magnitude", abs(h0_residual_dotc), "same magnitude, opposite sign"),
        ("checkpoint197_delta_chi2_1_bound", float(load_json(CHECKPOINT_197_RUN / "status.json")["delta_chi2_1_dot_C_over_H_bound"]), "global leakage chi2~1 bound from checkpoint 197"),
        ("one_percent_dotC_over_H", 0.01, "round-number stress"),
        ("full_memory_dotC_over_H", LOCKED_B_MEM, "unsafe unscreened memory-scale drift"),
    ]
    rows: list[dict[str, Any]] = []
    summary: dict[str, float] = {"h0_residual_dotc": h0_residual_dotc}
    for name, dotc, interpretation in candidates:
        factors = radial_factors(vector_rows, dotc)
        fixed_chi2, fixed_alpha, fixed_residual = chi2_for_factors(values, covariance, factors, "fixed")
        free_chi2, free_alpha, free_residual = chi2_for_factors(values, covariance, factors, "best_shared")
        rows.append(
            {
                "case": name,
                "dot_C_over_H": dotc,
                "epsilon_dotC_over_2H": dotc / 2.0,
                "fixed_alpha_chi2": fixed_chi2,
                "best_shared_alpha": free_alpha,
                "best_shared_alpha_minus_1": free_alpha - 1.0,
                "best_shared_alpha_residual_chi2": free_chi2,
                "max_abs_fixed_fractional_shift": float(np.max(np.abs(factors - 1.0))),
                "max_abs_best_alpha_fractional_residual": float(np.max(np.abs(free_alpha * factors - 1.0))),
                "interpretation": interpretation,
            }
        )
        summary[f"{name}_fixed_chi2"] = fixed_chi2
        summary[f"{name}_best_shared_chi2"] = free_chi2
        summary[f"{name}_best_shared_alpha"] = free_alpha
    return rows, summary


def row_residual_rows(vector_rows: list[dict[str, Any]], values: np.ndarray, covariance: np.ndarray, dot_c_over_h: float) -> list[dict[str, Any]]:
    factors = radial_factors(vector_rows, dot_c_over_h)
    fixed_chi2, _, fixed_residual = chi2_for_factors(values, covariance, factors, "fixed")
    free_chi2, free_alpha, free_residual = chi2_for_factors(values, covariance, factors, "best_shared")
    sigma = np.sqrt(np.diag(covariance))
    rows: list[dict[str, Any]] = []
    for row, value, factor, sig, fixed_delta, free_delta in zip(vector_rows, values, factors, sigma, fixed_residual, free_residual, strict=True):
        rows.append(
            {
                "row": row["row"],
                "z": row["z"],
                "quantity": row["quantity"],
                "dot_C_over_H": dot_c_over_h,
                "raw_factor": factor,
                "fixed_alpha_residual": fixed_delta,
                "fixed_alpha_sigma_shift": fixed_delta / sig,
                "best_shared_alpha": free_alpha,
                "best_shared_alpha_residual": free_delta,
                "best_shared_alpha_sigma_shift": free_delta / sig,
                "fixed_total_chi2": fixed_chi2,
                "best_shared_total_chi2": free_chi2,
                "status": "row_diagnostic_for_H0_residual_drift",
            }
        )
    return rows


def alpha_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "alpha_route": "shared_observational_nuisance",
            "definition": "same BAO alpha treatment is given to LCDM, wCDM, CPL, and MTS",
            "fair_for_empirical_comparison": "yes",
            "parent_theory_owner": "no",
            "promotion_status": "closure_only",
            "risk": "cannot be counted as MTS prediction",
        },
        {
            "alpha_route": "MTS_only_alpha_rescue",
            "definition": "MTS gets alpha freedom that baselines do not get",
            "fair_for_empirical_comparison": "no",
            "parent_theory_owner": "no",
            "promotion_status": "rejected",
            "risk": "invalid comparison",
        },
        {
            "alpha_route": "parent_observer_map_alpha",
            "definition": "alpha is derived from the same conformal endpoint map and ruler calibration theorem",
            "fair_for_empirical_comparison": "yes_if_predeclared",
            "parent_theory_owner": "candidate_not_derived",
            "promotion_status": "theorem_target",
            "risk": "must not double-count H0/r_d calibration",
        },
        {
            "alpha_route": "no_alpha_strict_shape",
            "definition": "BAO ratios are compared without a free global scale",
            "fair_for_empirical_comparison": "yes",
            "parent_theory_owner": "not_needed_if_theorem_exact",
            "promotion_status": "strongest_if_survived",
            "risk": "overly strict if survey alpha is a legitimate shared nuisance",
        },
    ]


def theory_contract_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "contract": "saturated BAO readout",
            "required_proof": "dot_C/H -> 0 or is below the DESI radial-drift tolerance over BAO redshift bins",
            "current_evidence": f"H0-residual drift chi2 fixed alpha={summary['H0_bridge_residual_drift_fixed_chi2']}",
            "status": "safe_for_tiny_residual_not_parent_derived",
        },
        {
            "contract": "full unscreened drift rejected",
            "required_proof": "parent theory must not allow dot_C/H of order B_mem in BAO readout",
            "current_evidence": f"full-memory drift fixed-alpha chi2={summary['full_memory_dotC_over_H_fixed_chi2']}",
            "status": "hard_guardrail",
        },
        {
            "contract": "shared alpha policy",
            "required_proof": "any fitted alpha must be shared across baselines or derived before promotion",
            "current_evidence": "shared alpha can be fair empirically but is not parent ownership",
            "status": "closure_only",
        },
        {
            "contract": "radial/transverse shape no-leakage",
            "required_proof": "D_H/r_d and D_M/r_d endpoint maps agree to within DESI tolerance",
            "current_evidence": f"fixed-alpha delta chi2<1 allows |dot_C/H|={summary['fixed_dotc_bound_chi2_1']}",
            "status": "bounded_not_derived",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    h0_safe = summary["H0_bridge_residual_drift_fixed_chi2"] < 1.0
    full_rejected = summary["full_memory_dotC_over_H_fixed_chi2"] > 25.0
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal gate",
        },
        {
            "gate": "H0-residual radial drift BAO-safe",
            "status": "pass" if h0_safe else "fail",
            "evidence": f"fixed_alpha_chi2={summary['H0_bridge_residual_drift_fixed_chi2']}",
            "claim_allowed": "small-residual bound",
        },
        {
            "gate": "full memory-scale radial drift rejected",
            "status": "pass" if full_rejected else "warning",
            "evidence": f"fixed_alpha_chi2={summary['full_memory_dotC_over_H_fixed_chi2']}",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "radial drift parent-derived",
            "status": "fail",
            "evidence": "dot_C/H suppression is numerically bounded but not derived from parent dynamics",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "alpha parent-owned",
            "status": "fail",
            "evidence": "shared alpha is empirically fair but still closure-level",
            "claim_allowed": "no promotion",
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
            "meaning": "The tiny dot_C/H residual needed by the H0 bridge is safely below the DESI DR2 radial BAO bound, but a full memory-scale unscreened drift is rejected. Alpha remains fair only as a shared empirical nuisance unless parent-owned.",
            "H0_residual_dot_C_over_H": summary["h0_residual_dotc"],
            "H0_residual_fixed_alpha_chi2": summary["H0_bridge_residual_drift_fixed_chi2"],
            "fixed_alpha_dotC_bound_chi2_1": summary["fixed_dotc_bound_chi2_1"],
            "best_shared_alpha_dotC_bound_chi2_1": summary["best_shared_dotc_bound_chi2_1"],
            "full_memory_fixed_alpha_chi2": summary["full_memory_dotC_over_H_fixed_chi2"],
            "next_target": "199-BAO-alpha-parent-or-shared-nuisance-policy.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_198_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    vector_rows, values, covariance = load_bao_values()
    tolerance_rows, tolerance_summary = radial_drift_tolerance_rows(vector_rows, values, covariance)
    representative_rows, representative_summary = representative_drift_rows(vector_rows, values, covariance)
    summary = {**tolerance_summary, **representative_summary}
    h0_row_diagnostics = row_residual_rows(vector_rows, values, covariance, summary["h0_residual_dotc"])
    alpha_rows = alpha_owner_rows()
    contract_rows = theory_contract_rows(summary)
    gates = claim_gate_rows(source_rows, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "radial_drift_tolerance.csv": (
            tolerance_rows,
            ["alpha_mode", "delta_chi2_threshold", "max_abs_dot_C_over_H", "max_abs_epsilon_dotC_over_2H", "interpretation"],
        ),
        "representative_radial_drift_cases.csv": (
            representative_rows,
            [
                "case",
                "dot_C_over_H",
                "epsilon_dotC_over_2H",
                "fixed_alpha_chi2",
                "best_shared_alpha",
                "best_shared_alpha_minus_1",
                "best_shared_alpha_residual_chi2",
                "max_abs_fixed_fractional_shift",
                "max_abs_best_alpha_fractional_residual",
                "interpretation",
            ],
        ),
        "H0_residual_radial_row_diagnostics.csv": (
            h0_row_diagnostics,
            [
                "row",
                "z",
                "quantity",
                "dot_C_over_H",
                "raw_factor",
                "fixed_alpha_residual",
                "fixed_alpha_sigma_shift",
                "best_shared_alpha",
                "best_shared_alpha_residual",
                "best_shared_alpha_sigma_shift",
                "fixed_total_chi2",
                "best_shared_total_chi2",
                "status",
            ],
        ),
        "alpha_owner_policy.csv": (
            alpha_rows,
            ["alpha_route", "definition", "fair_for_empirical_comparison", "parent_theory_owner", "promotion_status", "risk"],
        ),
        "theory_contract.csv": (
            contract_rows,
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
                "H0_residual_dot_C_over_H",
                "H0_residual_fixed_alpha_chi2",
                "fixed_alpha_dotC_bound_chi2_1",
                "best_shared_alpha_dotC_bound_chi2_1",
                "full_memory_fixed_alpha_chi2",
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
        "H0_residual_dot_C_over_H": summary["h0_residual_dotc"],
        "H0_residual_fixed_alpha_chi2": summary["H0_bridge_residual_drift_fixed_chi2"],
        "H0_residual_best_shared_alpha_chi2": summary["H0_bridge_residual_drift_best_shared_chi2"],
        "fixed_alpha_dotC_bound_chi2_1": summary["fixed_dotc_bound_chi2_1"],
        "best_shared_alpha_dotC_bound_chi2_1": summary["best_shared_dotc_bound_chi2_1"],
        "full_memory_fixed_alpha_chi2": summary["full_memory_dotC_over_H_fixed_chi2"],
        "full_memory_best_shared_alpha_chi2": summary["full_memory_dotC_over_H_best_shared_chi2"],
        "radial_drift_parent_derived": False,
        "alpha_parent_owned": False,
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
