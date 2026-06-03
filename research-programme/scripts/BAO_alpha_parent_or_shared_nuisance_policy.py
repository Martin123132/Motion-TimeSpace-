#!/usr/bin/env python3
"""Checkpoint 199: BAO alpha parent owner or shared nuisance policy."""

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

CHECKPOINT_199_NAME = "BAO-alpha-parent-or-shared-nuisance-policy"
CHECKPOINT_198_RUN = RUNS_ROOT / "20260601-000015-BAO-radial-drift-and-alpha-owner-gate"
CHECKPOINT_197_RUN = RUNS_ROOT / "20260601-000014-BAO-common-mode-ratio-theorem-attempt"
CHECKPOINT_193_RUN = RUNS_ROOT / "20260601-000010-calibration-bridge-H0-owner-or-demotion"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
BAO_ONLY_RUN = RUNS_ROOT / "20260531-151959-locked-2over27-BAO-only-score"

STATUS = "BAO_alpha_shared_nuisance_fair_parent_owner_missing"
CLAIM_CEILING = "BAO_alpha_policy_internal_only_shared_nuisance_not_prediction"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

SPEED_OF_LIGHT_KM_S = 299_792.458


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
        (Path(__file__).resolve(), "checkpoint 199 BAO alpha policy script"),
        (WORK_DIR / "198-BAO-radial-drift-and-alpha-owner-gate.md", "radial drift and alpha gate"),
        (CHECKPOINT_198_RUN / "status.json", "checkpoint 198 machine status"),
        (CHECKPOINT_198_RUN / "results" / "alpha_owner_policy.csv", "checkpoint 198 alpha policy"),
        (WORK_DIR / "197-BAO-common-mode-ratio-theorem-attempt.md", "BAO common-mode theorem checkpoint"),
        (CHECKPOINT_197_RUN / "status.json", "checkpoint 197 machine status"),
        (WORK_DIR / "193-calibration-bridge-H0-owner-or-demotion.md", "H0 calibration bridge checkpoint"),
        (CHECKPOINT_193_RUN / "status.json", "checkpoint 193 machine status"),
        (CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv", "CAMB rdrag smoke summary"),
        (WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md", "locked 2/27 BAO-only checkpoint"),
        (BAO_ONLY_RUN / "results" / "model_register.csv", "BAO-only model register"),
        (BAO_ONLY_RUN / "results" / "fit_summary.csv", "BAO-only fit summary"),
        (WORK_DIR / "scripts" / "cosmo_SN_BAO_closure_runner.py", "shared BAO alpha implementation"),
        (WORK_DIR / "scripts" / "locked_2over27_BAO_only_release_test.py", "BAO-only runner"),
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


def rdrag_baseline() -> float:
    for row in read_csv_rows(CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv"):
        if row["branch"] == "LCDM_baseline_recomputed" and row["quantity"] == "rdrag":
            return float(row["value"])
    raise RuntimeError("Could not find LCDM rdrag baseline")


def alpha_from_h0_rdrag(h0: float, rdrag: float) -> float:
    return SPEED_OF_LIGHT_KM_S / (h0 * rdrag)


def h0_from_alpha_rdrag(alpha: float, rdrag: float) -> float:
    return SPEED_OF_LIGHT_KM_S / (alpha * rdrag)


def model_alpha_usage_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(BAO_ONLY_RUN / "results" / "model_register.csv"):
        fitted = row["fitted"]
        gets_alpha = "BAO alpha" in fitted
        rows.append(
            {
                "model": row["model"],
                "role": row["role"],
                "fitted": fitted,
                "gets_BAO_alpha": "yes" if gets_alpha else "no",
                "fairness_readout": "shared_alpha" if gets_alpha else "check_model",
                "claim_ceiling": row["claim_ceiling"],
            }
        )
    return rows


def fitted_alpha_rows(rdrag: float) -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    summary: dict[str, float] = {}
    for row in read_csv_rows(BAO_ONLY_RUN / "results" / "fit_summary.csv"):
        alpha = float(row["bao_alpha"])
        effective_h0 = h0_from_alpha_rdrag(alpha, rdrag)
        out = {
            "release": row["release"],
            "model": row["model"],
            "chi2_BAO": row["chi2_BAO"],
            "AIC": row["AIC"],
            "BIC": row["BIC"],
            "bao_alpha": alpha,
            "effective_H0_if_rdrag_fixed": effective_h0,
            "prior_edge_flag": row["prior_edge_flag"],
            "readout": "alpha is fitted shared calibration, not a parent prediction",
        }
        rows.append(out)
        key = f"{row['release']}__{row['model']}"
        summary[f"{key}__alpha"] = alpha
        summary[f"{key}__effective_H0"] = effective_h0
    return rows, summary


def parent_alpha_candidate_rows(rdrag: float, fitted_summary: dict[str, float]) -> list[dict[str, Any]]:
    status_193 = load_json(CHECKPOINT_193_RUN / "status.json")
    late_h0 = float(status_193["late_reference_H0"])
    cmb_h0 = float(status_193["CMB_profile_H0"])
    exp_half_h0 = float(status_193["exp_half_memory_H0"])
    locked_dr2_alpha = fitted_summary["DESI_DR2_primary__MTS_locked_2over27__alpha"]
    locked_dr1_alpha = fitted_summary["DESI_DR1_primary__MTS_locked_2over27__alpha"]
    candidates = [
        ("late_reference_H0_times_rdrag", late_h0, "late-reference H0 with CAMB LCDM rdrag"),
        ("same_density_CMB_profile_H0_times_rdrag", cmb_h0, "same-density CMB-profile H0 with CAMB LCDM rdrag"),
        ("exp_half_memory_H0_times_rdrag", exp_half_h0, "half-memory bridged H0 with CAMB LCDM rdrag"),
        ("DR2_locked_fit_alpha_readback", h0_from_alpha_rdrag(locked_dr2_alpha, rdrag), "read back H0 from fitted DR2 locked alpha"),
        ("DR1_locked_fit_alpha_readback", h0_from_alpha_rdrag(locked_dr1_alpha, rdrag), "read back H0 from fitted DR1 locked alpha"),
    ]
    rows: list[dict[str, Any]] = []
    for name, h0, interpretation in candidates:
        alpha = alpha_from_h0_rdrag(h0, rdrag)
        rows.append(
            {
                "candidate": name,
                "H0_input_or_readback": h0,
                "rdrag_used": rdrag,
                "alpha_predicted": alpha,
                "delta_vs_DR2_locked_alpha": alpha - locked_dr2_alpha,
                "frac_delta_vs_DR2_locked_alpha": (alpha - locked_dr2_alpha) / locked_dr2_alpha,
                "delta_vs_DR1_locked_alpha": alpha - locked_dr1_alpha,
                "frac_delta_vs_DR1_locked_alpha": (alpha - locked_dr1_alpha) / locked_dr1_alpha,
                "interpretation": interpretation,
                "status": "readback" if "readback" in name else "candidate_not_parent_selection",
            }
        )
    return rows


def alpha_theory_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "shared_empirical_nuisance",
            "definition": "BAO alpha is analytically profiled or fitted for every model branch, including baselines",
            "allowed_use": "fair empirical comparison and robustness scoring",
            "forbidden_use": "claiming MTS predicted the BAO absolute scale",
            "current_status": "default_policy",
        },
        {
            "policy": "MTS_only_alpha_rescue",
            "definition": "MTS gets extra alpha freedom not given to LCDM/wCDM/CPL",
            "allowed_use": "none",
            "forbidden_use": "any model comparison or support claim",
            "current_status": "rejected",
        },
        {
            "policy": "parent_alpha_prediction",
            "definition": "alpha = c/(H0 r_d) follows from parent-owned H0 branch and parent-owned r_d/ruler calibration",
            "allowed_use": "future theorem target",
            "forbidden_use": "using fitted alpha as proof before H0 and r_d are parent-owned",
            "current_status": "missing",
        },
        {
            "policy": "strict_no_alpha_shape",
            "definition": "fix alpha from a predeclared H0*r_d calibration and score BAO shape directly",
            "allowed_use": "strong diagnostic after parent candidate chosen",
            "forbidden_use": "outranking full fair fits without explaining calibration choice",
            "current_status": "future_stress_test",
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "H0 branch owner",
            "needed": "derive whether BAO alpha should use late-reference H0, CMB-profile H0, or half-memory bridged H0",
            "current_evidence": "checkpoint 193/194 give candidate H0 branches but not parent ownership",
            "status": "missing",
        },
        {
            "contract": "r_d owner",
            "needed": "derive sound horizon/ruler calibration in the same matter-unit frame used by BAO",
            "current_evidence": "CAMB same-density smoke shows tiny rdrag microphysics shift only",
            "status": "partial_numeric_support",
        },
        {
            "contract": "alpha nuisance policy",
            "needed": "state before fits whether alpha is shared nuisance, fixed prediction, or derived calibration",
            "current_evidence": "current runners use shared analytic/fitted alpha for all branches",
            "status": "empirical_policy_defined",
        },
        {
            "contract": "no double-counting",
            "needed": "avoid using alpha to absorb the same H0/r_d shift already claimed as a theory prediction",
            "current_evidence": "alpha remains closure-level, so no theory prediction is claimed",
            "status": "guardrail_active",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], alpha_usage: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    all_get_alpha = all(row["gets_BAO_alpha"] == "yes" for row in alpha_usage)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal policy gate",
        },
        {
            "gate": "alpha shared across BAO-only models",
            "status": "pass" if all_get_alpha else "fail",
            "evidence": f"models_checked={len(alpha_usage)}",
            "claim_allowed": "fair empirical nuisance",
        },
        {
            "gate": "MTS-only alpha rescue",
            "status": "rejected",
            "evidence": "current runners give BAO alpha to baselines and MTS alike",
            "claim_allowed": "no",
        },
        {
            "gate": "parent alpha predicted",
            "status": "fail",
            "evidence": "H0 branch and r_d calibration are not parent-owned",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO empirical score remains usable",
            "status": "pass",
            "evidence": "shared alpha is fair if counted as fitted/nuisance for all models",
            "claim_allowed": "closure score only",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(fitted_summary: dict[str, float]) -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "BAO alpha is currently a fair shared empirical nuisance, not an MTS prediction. Parent promotion requires deriving H0 branch ownership, r_d calibration, and alpha=c/(H0 r_d) before alpha is fixed or claimed.",
            "DR2_locked_alpha": fitted_summary["DESI_DR2_primary__MTS_locked_2over27__alpha"],
            "DR2_locked_effective_H0_if_rdrag_fixed": fitted_summary["DESI_DR2_primary__MTS_locked_2over27__effective_H0"],
            "DR1_locked_alpha": fitted_summary["DESI_DR1_primary__MTS_locked_2over27__alpha"],
            "DR1_locked_effective_H0_if_rdrag_fixed": fitted_summary["DESI_DR1_primary__MTS_locked_2over27__effective_H0"],
            "next_target": "200-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_199_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    rdrag = rdrag_baseline()
    sources = source_register_rows()
    usage = model_alpha_usage_rows()
    fitted, fitted_summary = fitted_alpha_rows(rdrag)
    candidates = parent_alpha_candidate_rows(rdrag, fitted_summary)
    policy = alpha_theory_policy_rows()
    contract = parent_contract_rows()
    gates = claim_gate_rows(sources, usage)
    decision = decision_rows(fitted_summary)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            sources,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "model_alpha_usage.csv": (
            usage,
            ["model", "role", "fitted", "gets_BAO_alpha", "fairness_readout", "claim_ceiling"],
        ),
        "fitted_alpha_readback.csv": (
            fitted,
            ["release", "model", "chi2_BAO", "AIC", "BIC", "bao_alpha", "effective_H0_if_rdrag_fixed", "prior_edge_flag", "readout"],
        ),
        "parent_alpha_candidates.csv": (
            candidates,
            [
                "candidate",
                "H0_input_or_readback",
                "rdrag_used",
                "alpha_predicted",
                "delta_vs_DR2_locked_alpha",
                "frac_delta_vs_DR2_locked_alpha",
                "delta_vs_DR1_locked_alpha",
                "frac_delta_vs_DR1_locked_alpha",
                "interpretation",
                "status",
            ],
        ),
        "alpha_theory_policy.csv": (
            policy,
            ["policy", "definition", "allowed_use", "forbidden_use", "current_status"],
        ),
        "parent_alpha_contract.csv": (
            contract,
            ["contract", "needed", "current_evidence", "status"],
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
                "DR2_locked_alpha",
                "DR2_locked_effective_H0_if_rdrag_fixed",
                "DR1_locked_alpha",
                "DR1_locked_effective_H0_if_rdrag_fixed",
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
        "rdrag_used": rdrag,
        "alpha_shared_across_BAO_only_models": True,
        "alpha_parent_owned": False,
        "MTS_only_alpha_rescue_rejected": True,
        "DR2_locked_alpha": fitted_summary["DESI_DR2_primary__MTS_locked_2over27__alpha"],
        "DR2_locked_effective_H0_if_rdrag_fixed": fitted_summary["DESI_DR2_primary__MTS_locked_2over27__effective_H0"],
        "DR1_locked_alpha": fitted_summary["DESI_DR1_primary__MTS_locked_2over27__alpha"],
        "DR1_locked_effective_H0_if_rdrag_fixed": fitted_summary["DESI_DR1_primary__MTS_locked_2over27__effective_H0"],
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
