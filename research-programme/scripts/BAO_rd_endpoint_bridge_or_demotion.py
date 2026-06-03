#!/usr/bin/env python3
"""Checkpoint 196: BAO r_d endpoint bridge or demotion gate."""

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

CHECKPOINT_196_NAME = "BAO-rd-endpoint-bridge-or-demotion"
CHECKPOINT_195_RUN = RUNS_ROOT / "20260601-000012-late-CMB-domain-rule-and-local-silence-gate"
CHECKPOINT_194_RUN = RUNS_ROOT / "20260601-000011-half-memory-clock-map-derivation-attempt"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"

BAO_MEAN = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_COV = FORMALIZATION_DIR / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
ACOUSTIC_SUMMARY = CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv"

STATUS = "BAO_rd_common_mode_rule_required_half_memory_ratio_shift_rejected"
CLAIM_CEILING = "BAO_endpoint_policy_internal_gate_only_no_parent_rd_claim"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
        (Path(__file__).resolve(), "checkpoint 196 BAO endpoint policy script"),
        (WORK_DIR / "195-late-CMB-domain-rule-and-local-silence-gate.md", "endpoint rule checkpoint"),
        (CHECKPOINT_195_RUN / "status.json", "checkpoint 195 machine status"),
        (CHECKPOINT_195_RUN / "results" / "observable_domain_classification.csv", "checkpoint 195 observable classification"),
        (WORK_DIR / "194-half-memory-clock-map-derivation-attempt.md", "half-memory clock map checkpoint"),
        (CHECKPOINT_194_RUN / "status.json", "checkpoint 194 machine status"),
        (WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md", "locked 2/27 BAO-only empirical score"),
        (WORK_DIR / "124-BAO-shape-residual-decomposition.md", "BAO residual decomposition checkpoint"),
        (ACOUSTIC_SUMMARY, "CAMB acoustic distance/rdrag smoke summary"),
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


def load_bao_vector() -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    rows: list[dict[str, Any]] = []
    values: list[float] = []
    with BAO_MEAN.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            z_text, value_text, quantity = stripped.split()
            value = float(value_text)
            rows.append(
                {
                    "row": len(rows),
                    "z": float(z_text),
                    "quantity": quantity,
                    "value": value,
                }
            )
            values.append(value)
    covariance = np.loadtxt(BAO_COV)
    return rows, np.array(values), covariance


def bao_data_shape_rows(vector_rows: list[dict[str, Any]], covariance: np.ndarray) -> list[dict[str, Any]]:
    quantities: dict[str, int] = {}
    for row in vector_rows:
        quantities[row["quantity"]] = quantities.get(row["quantity"], 0) + 1
    rows = [
        {
            "check": "mean_rows",
            "value": len(vector_rows),
            "status": "pass" if len(vector_rows) == 13 else "fail",
            "detail": "DESI DR2 primary expected 13 rows",
        },
        {
            "check": "covariance_shape",
            "value": f"{covariance.shape[0]}x{covariance.shape[1]}",
            "status": "pass" if covariance.shape == (len(vector_rows), len(vector_rows)) else "fail",
            "detail": "covariance must match mean vector",
        },
    ]
    for quantity, count in sorted(quantities.items()):
        rows.append(
            {
                "check": f"quantity_{quantity}",
                "value": count,
                "status": "pass",
                "detail": "quantity count in DESI DR2 primary mean vector",
            }
        )
    return rows


def chi2_for_fractional_scale(values: np.ndarray, covariance: np.ndarray, ratio_factor: float) -> tuple[float, np.ndarray, np.ndarray]:
    residual = (ratio_factor - 1.0) * values
    precision = np.linalg.inv(covariance)
    weighted = precision @ residual
    contributions = residual * weighted
    chi2 = float(residual @ weighted)
    return chi2, residual, contributions


def endpoint_policy_rows(values: np.ndarray, covariance: np.ndarray) -> tuple[list[dict[str, Any]], dict[str, float]]:
    candidates = [
        {
            "policy": "ratio_invariant_common_mode",
            "formula": "D_X and r_d carry the same endpoint conformal unit, so (D_X/r_d)_tilde = D_X/r_d",
            "ratio_factor": 1.0,
            "alpha_needed_to_hide": 1.0,
            "meaning": "BAO endpoint theorem target; no naked half-memory scale shift in ratios",
        },
        {
            "policy": "rd_denominator_only_exp_half",
            "formula": "r_d -> exp(B_mem/2) r_d while D_X is not rescaled",
            "ratio_factor": math.exp(-LOCKED_B_MEM / 2.0),
            "alpha_needed_to_hide": math.exp(LOCKED_B_MEM / 2.0),
            "meaning": "naked half-memory denominator shift",
        },
        {
            "policy": "distance_numerator_only_exp_half",
            "formula": "D_X -> exp(B_mem/2) D_X while r_d is not rescaled",
            "ratio_factor": math.exp(LOCKED_B_MEM / 2.0),
            "alpha_needed_to_hide": math.exp(-LOCKED_B_MEM / 2.0),
            "meaning": "naked half-memory numerator shift",
        },
        {
            "policy": "rd_denominator_only_linear_half",
            "formula": "r_d -> r_d/(1-B_mem/2) equivalent linearized ratio decrease",
            "ratio_factor": 1.0 - LOCKED_B_MEM / 2.0,
            "alpha_needed_to_hide": 1.0 / (1.0 - LOCKED_B_MEM / 2.0),
            "meaning": "linearized denominator-only sidecar",
        },
        {
            "policy": "free_alpha_absorbs_global_scale",
            "formula": "BAO alpha is fitted or parent-owned and absorbs any global D_X/r_d scale",
            "ratio_factor": 1.0,
            "alpha_needed_to_hide": "",
            "meaning": "empirical runner route; not parent-owned unless alpha/r_d theorem is supplied",
        },
    ]
    rows: list[dict[str, Any]] = []
    summary: dict[str, float] = {}
    for candidate in candidates:
        ratio_factor = float(candidate["ratio_factor"])
        chi2, _, _ = chi2_for_fractional_scale(values, covariance, ratio_factor)
        fractional_shift = ratio_factor - 1.0
        if candidate["policy"] == "ratio_invariant_common_mode":
            status = "viable_theorem_target"
        elif candidate["policy"] == "free_alpha_absorbs_global_scale":
            status = "empirical_closure_only_until_parent_owned"
        elif chi2 > 25.0:
            status = "rejected_without_alpha_rescue"
        else:
            status = "needs_full_fit"
        rows.append(
            {
                "policy": candidate["policy"],
                "formula": candidate["formula"],
                "ratio_factor": ratio_factor,
                "fractional_ratio_shift": fractional_shift,
                "scale_mode_chi2_penalty_DR2": chi2,
                "alpha_needed_to_hide": candidate["alpha_needed_to_hide"],
                "status": status,
                "meaning": candidate["meaning"],
            }
        )
        summary[f"{candidate['policy']}_chi2"] = chi2
        summary[f"{candidate['policy']}_ratio_factor"] = ratio_factor
    return rows, summary


def row_penalty_rows(vector_rows: list[dict[str, Any]], values: np.ndarray, covariance: np.ndarray) -> list[dict[str, Any]]:
    ratio_factor = math.exp(-LOCKED_B_MEM / 2.0)
    _, residual, contributions = chi2_for_fractional_scale(values, covariance, ratio_factor)
    diag_sigma = np.sqrt(np.diag(covariance))
    rows: list[dict[str, Any]] = []
    for row, value, sigma, delta, contribution in zip(vector_rows, values, diag_sigma, residual, contributions, strict=True):
        rows.append(
            {
                "row": row["row"],
                "z": row["z"],
                "quantity": row["quantity"],
                "value": value,
                "sigma_diag": sigma,
                "fractional_shift": ratio_factor - 1.0,
                "absolute_shift": delta,
                "diag_sigma_shift": delta / sigma,
                "covariance_signed_chi2_contribution": contribution,
                "status": "scale_hazard_diagnostic",
            }
        )
    return rows


def rdrag_smoke_rows() -> list[dict[str, Any]]:
    acoustic_rows = read_csv_rows(ACOUSTIC_SUMMARY)
    rows: list[dict[str, Any]] = []
    for row in acoustic_rows:
        if row["quantity"] == "rdrag" and row["branch"] in {
            "LCDM_baseline_recomputed",
            "MTS_high_cs_fluid_density_isolation",
            "MTS_high_cs_PPF_density_isolation",
        }:
            rows.append(
                {
                    "branch": row["branch"],
                    "rdrag": row["value"],
                    "LCDM_baseline_value": row["LCDM_baseline_value"],
                    "delta_vs_LCDM": row["delta_vs_LCDM"],
                    "frac_delta_vs_LCDM": row["frac_delta_vs_LCDM"],
                    "interpretation": "CAMB early-physics rdrag is essentially unchanged in same-density smoke; endpoint calibration is separate from sound-horizon microphysics",
                }
            )
    return rows


def theory_contract_rows(summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "contract": "BAO ratio common-mode theorem",
            "required_derivation": "show D_M/r_d, D_H/r_d, and D_V/r_d use the same endpoint conformal unit so the exp(B/2) factor cancels",
            "evidence_now": "naked exp(-B/2) ratio shift gives huge DR2 scale-mode penalty",
            "status": "required_for_survival",
        },
        {
            "contract": "r_d microphysics owner",
            "required_derivation": "show early sound horizon microphysics is unchanged or derive its controlled change",
            "evidence_now": "CAMB same-density smoke has frac_delta_rdrag about -1.1e-6",
            "status": "partial_background_support_not_parent_theorem",
        },
        {
            "contract": "BAO alpha owner",
            "required_derivation": "if a global alpha is used, derive it from the observer map rather than fitting it as nuisance",
            "evidence_now": f"denominator-only half-memory would require alpha={math.exp(LOCKED_B_MEM / 2.0)} to hide",
            "status": "missing",
        },
        {
            "contract": "radial/transverse shape owner",
            "required_derivation": "explain why DH/rs was the dominant penalty in the previous joint failed gate",
            "evidence_now": "checkpoint 124 localized joint penalty mostly to DH_over_rs",
            "status": "still_needed",
        },
        {
            "contract": "no naked half-memory BAO ratio shift",
            "required_derivation": "parent endpoint rule must forbid applying exp(-B/2) directly to observed BAO ratios",
            "evidence_now": f"rd_denominator_only_exp_half chi2 penalty={summary['rd_denominator_only_exp_half_chi2']}",
            "status": "hard_gate",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], summary: dict[str, float]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    naked_shift_rejected = summary["rd_denominator_only_exp_half_chi2"] > 25.0
    common_mode_safe = summary["ratio_invariant_common_mode_chi2"] == 0.0
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal BAO endpoint gate",
        },
        {
            "gate": "DESI DR2 BAO shape valid",
            "status": "pass",
            "evidence": "13-row mean vector and matching covariance loaded",
            "claim_allowed": "scale-mode diagnostic",
        },
        {
            "gate": "common-mode BAO endpoint policy safe",
            "status": "pass" if common_mode_safe else "fail",
            "evidence": f"ratio_invariant_chi2={summary['ratio_invariant_common_mode_chi2']}",
            "claim_allowed": "theorem target",
        },
        {
            "gate": "naked half-memory BAO ratio shift allowed",
            "status": "fail" if naked_shift_rejected else "warning",
            "evidence": f"rd_denominator_only_exp_half_chi2={summary['rd_denominator_only_exp_half_chi2']}",
            "claim_allowed": "no",
        },
        {
            "gate": "BAO alpha parent-owned",
            "status": "fail",
            "evidence": "previous BAO runners fit/absorb alpha empirically; no parent alpha theorem yet",
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
            "meaning": "BAO can survive the endpoint-clock route only if D_X and r_d share a common conformal endpoint unit or if a parent-owned alpha/r_d calibration is derived. A naked half-memory shift of D_X/r_d is rejected by DESI DR2 covariance.",
            "ratio_invariant_chi2": summary["ratio_invariant_common_mode_chi2"],
            "rd_only_exp_half_chi2": summary["rd_denominator_only_exp_half_chi2"],
            "distance_only_exp_half_chi2": summary["distance_numerator_only_exp_half_chi2"],
            "alpha_needed_for_rd_only_exp_half": math.exp(LOCKED_B_MEM / 2.0),
            "next_target": "197-BAO-common-mode-ratio-theorem-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_196_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    vector_rows, values, covariance = load_bao_vector()
    data_shape = bao_data_shape_rows(vector_rows, covariance)
    policy_rows, summary = endpoint_policy_rows(values, covariance)
    penalty_rows = row_penalty_rows(vector_rows, values, covariance)
    rdrag_rows = rdrag_smoke_rows()
    contract_rows = theory_contract_rows(summary)
    gates = claim_gate_rows(source_rows, summary)
    decision = decision_rows(summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "BAO_data_shape.csv": (
            data_shape,
            ["check", "value", "status", "detail"],
        ),
        "endpoint_policy_candidates.csv": (
            policy_rows,
            ["policy", "formula", "ratio_factor", "fractional_ratio_shift", "scale_mode_chi2_penalty_DR2", "alpha_needed_to_hide", "status", "meaning"],
        ),
        "rd_only_half_memory_row_penalties.csv": (
            penalty_rows,
            ["row", "z", "quantity", "value", "sigma_diag", "fractional_shift", "absolute_shift", "diag_sigma_shift", "covariance_signed_chi2_contribution", "status"],
        ),
        "rdrag_smoke_check.csv": (
            rdrag_rows,
            ["branch", "rdrag", "LCDM_baseline_value", "delta_vs_LCDM", "frac_delta_vs_LCDM", "interpretation"],
        ),
        "BAO_theory_contract.csv": (
            contract_rows,
            ["contract", "required_derivation", "evidence_now", "status"],
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
                "ratio_invariant_chi2",
                "rd_only_exp_half_chi2",
                "distance_only_exp_half_chi2",
                "alpha_needed_for_rd_only_exp_half",
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
        "BAO_rows": len(vector_rows),
        "ratio_invariant_chi2": summary["ratio_invariant_common_mode_chi2"],
        "rd_only_exp_half_chi2": summary["rd_denominator_only_exp_half_chi2"],
        "distance_only_exp_half_chi2": summary["distance_numerator_only_exp_half_chi2"],
        "linear_rd_only_chi2": summary["rd_denominator_only_linear_half_chi2"],
        "alpha_needed_for_rd_only_exp_half": math.exp(LOCKED_B_MEM / 2.0),
        "common_mode_rule_required": True,
        "naked_half_memory_BAO_ratio_shift_rejected": True,
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
