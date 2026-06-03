#!/usr/bin/env python3
"""Checkpoint 200: BAO strict-alpha shape stress or parent H0-r_d contract."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as runner  # noqa: E402
import locked_2over27_BAO_only_release_test as bao_only  # noqa: E402


CHECKPOINT_200_NAME = "BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract"
CHECKPOINT_199_RUN = RUNS_ROOT / "20260601-000016-BAO-alpha-parent-or-shared-nuisance-policy"
CHECKPOINT_198_RUN = RUNS_ROOT / "20260601-000015-BAO-radial-drift-and-alpha-owner-gate"
CHECKPOINT_193_RUN = RUNS_ROOT / "20260601-000010-calibration-bridge-H0-owner-or-demotion"
CHECKPOINT_186_RUN = RUNS_ROOT / "20260601-000003-CAMB-high-cs-wtable-spectra-smoke"
BAO_ONLY_RUN = RUNS_ROOT / "20260531-151959-locked-2over27-BAO-only-score"

STATUS = "BAO_strict_alpha_stress_run_parent_H0_rd_contract_still_missing"
CLAIM_CEILING = "strict_alpha_BAO_stress_internal_only_no_parent_alpha_no_support_claim"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

SPEED_OF_LIGHT_KM_S = 299_792.458
MODEL_ORDER = [
    "LCDM",
    "wCDM",
    "CPL",
    "MTS_locked_2over27",
    "MTS_Bmem_zero",
    "MTS_fitted_Bmem_diagnostic",
]


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
        (Path(__file__).resolve(), "checkpoint 200 strict-alpha script"),
        (WORK_DIR / "199-BAO-alpha-parent-or-shared-nuisance-policy.md", "alpha policy checkpoint"),
        (CHECKPOINT_199_RUN / "status.json", "checkpoint 199 machine status"),
        (CHECKPOINT_199_RUN / "results" / "parent_alpha_candidates.csv", "checkpoint 199 parent alpha candidates"),
        (CHECKPOINT_199_RUN / "results" / "fitted_alpha_readback.csv", "checkpoint 199 fitted alpha readback"),
        (WORK_DIR / "198-BAO-radial-drift-and-alpha-owner-gate.md", "radial drift alpha gate"),
        (CHECKPOINT_198_RUN / "status.json", "checkpoint 198 machine status"),
        (WORK_DIR / "193-calibration-bridge-H0-owner-or-demotion.md", "H0 calibration bridge checkpoint"),
        (CHECKPOINT_193_RUN / "status.json", "checkpoint 193 machine status"),
        (CHECKPOINT_186_RUN / "results" / "acoustic_distance_summary.csv", "CAMB rdrag smoke summary"),
        (WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md", "BAO-only locked score checkpoint"),
        (BAO_ONLY_RUN / "results" / "fit_summary.csv", "BAO-only shared-alpha fit summary"),
        (Path(bao_only.__file__).resolve(), "BAO-only runner module"),
        (Path(runner.__file__).resolve(), "BAO prediction module"),
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
    raise RuntimeError("Missing rdrag baseline")


def alpha_from_h0_rdrag(h0: float, rdrag: float) -> float:
    return SPEED_OF_LIGHT_KM_S / (h0 * rdrag)


def shared_fit_lookup() -> dict[tuple[str, str], dict[str, str]]:
    return {
        (row["release"], row["model"]): row
        for row in read_csv_rows(BAO_ONLY_RUN / "results" / "fit_summary.csv")
    }


def alpha_candidates(rdrag: float) -> list[dict[str, Any]]:
    status_193 = load_json(CHECKPOINT_193_RUN / "status.json")
    status_199 = load_json(CHECKPOINT_199_RUN / "status.json")
    return [
        {
            "alpha_candidate": "late_reference_H0_rdrag",
            "alpha": alpha_from_h0_rdrag(float(status_193["late_reference_H0"]), rdrag),
            "basis": "late-reference H0 times CAMB rdrag",
            "parent_status": "candidate_not_parent_owned",
        },
        {
            "alpha_candidate": "same_density_CMB_profile_H0_rdrag",
            "alpha": alpha_from_h0_rdrag(float(status_193["CMB_profile_H0"]), rdrag),
            "basis": "same-density CMB-profile H0 times CAMB rdrag",
            "parent_status": "candidate_not_parent_owned",
        },
        {
            "alpha_candidate": "exp_half_memory_H0_rdrag",
            "alpha": alpha_from_h0_rdrag(float(status_193["exp_half_memory_H0"]), rdrag),
            "basis": "half-memory bridged H0 times CAMB rdrag",
            "parent_status": "candidate_not_parent_owned",
        },
        {
            "alpha_candidate": "DR2_locked_fit_readback",
            "alpha": float(status_199["DR2_locked_alpha"]),
            "basis": "readback from DESI DR2 locked 2/27 shared-alpha BAO fit",
            "parent_status": "readback_not_prediction",
        },
        {
            "alpha_candidate": "DR1_locked_fit_readback",
            "alpha": float(status_199["DR1_locked_alpha"]),
            "basis": "readback from DESI DR1 locked 2/27 shared-alpha BAO fit",
            "parent_status": "readback_not_prediction",
        },
    ]


def alpha_candidate_rows(candidates: list[dict[str, Any]], shared_lookup: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, Any]]:
    dr2_locked = float(shared_lookup[("DESI_DR2_primary", "MTS_locked_2over27")]["bao_alpha"])
    dr1_locked = float(shared_lookup[("DESI_DR1_primary", "MTS_locked_2over27")]["bao_alpha"])
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        alpha = float(candidate["alpha"])
        rows.append(
            {
                "alpha_candidate": candidate["alpha_candidate"],
                "alpha": alpha,
                "delta_vs_DR2_locked_shared_alpha": alpha - dr2_locked,
                "frac_delta_vs_DR2_locked_shared_alpha": (alpha - dr2_locked) / dr2_locked,
                "delta_vs_DR1_locked_shared_alpha": alpha - dr1_locked,
                "frac_delta_vs_DR1_locked_shared_alpha": (alpha - dr1_locked) / dr1_locked,
                "basis": candidate["basis"],
                "parent_status": candidate["parent_status"],
            }
        )
    return rows


def bao_chi2_fixed_alpha(model_key: str, params: dict[str, float], bao: dict[str, Any], alpha: float) -> tuple[float, np.ndarray, np.ndarray]:
    observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
    covariance = np.asarray(bao["covariance"], dtype=float)
    predicted = runner.bao_prediction(model_key, params, bao, alpha=alpha)
    residual = observed - predicted
    inv_cov = linalg.inv(covariance)
    chi2 = float(residual @ inv_cov @ residual)
    return chi2, residual, predicted


def score_model_fixed_alpha(release: str, model: str, bao: dict[str, Any], alpha_candidate: str, alpha: float, max_iter: int) -> dict[str, Any]:
    priors = bao_only.priors_for_model(model)
    names = list(priors)
    bounds = [priors[name] for name in names]

    def objective(vector: np.ndarray) -> float:
        try:
            params = bao_only.params_from_vector(model, names, vector)
            physical_model, physical_params = bao_only.physical_model_and_params(model, params)
            chi2, _, _ = bao_chi2_fixed_alpha(physical_model, physical_params, bao, alpha)
            return chi2
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)]
    rng = np.random.default_rng(abs(hash((release, model, alpha_candidate))) % (2**32))
    for _ in range(max(8, min(24, max_iter // 8))):
        starts.append(np.asarray([rng.uniform(lower, upper) for lower, upper in bounds], dtype=float))
    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-10},
        )
        for start in starts
    ]
    result = min(results, key=lambda item: float(item.fun))
    params = bao_only.params_from_vector(model, names, np.asarray(result.x, dtype=float))
    physical_model, physical_params = bao_only.physical_model_and_params(model, params)
    chi2, residual, predicted = bao_chi2_fixed_alpha(physical_model, physical_params, bao, alpha)
    edge_rows = bao_only.prior_edge_rows(release, model, priors, params)
    n_points = len(bao["rows"])
    k = len(names)
    return {
        "release": release,
        "alpha_candidate": alpha_candidate,
        "alpha_fixed": alpha,
        "model": model,
        "physical_model": physical_model,
        "chi2_BAO": chi2,
        "k": k,
        "n": n_points,
        "AIC": chi2 + 2.0 * k,
        "BIC": chi2 + k * math.log(n_points),
        "converged": bool(result.success),
        "optimizer_message": str(result.message),
        "prior_edge_flag": any(row["edge_flag"] for row in edge_rows),
        "Omega_m": params.get("Omega_m", ""),
        "w": params.get("w", ""),
        "w0": params.get("w0", ""),
        "wa": params.get("wa", ""),
        "B_mem": bao_only.LOCKED_B_MEM if model == "MTS_locked_2over27" else params.get("B_mem", 0.0 if model == "MTS_Bmem_zero" else ""),
        "B_mem_fit_status": "frozen" if model == "MTS_locked_2over27" else ("diagnostic_fit" if model == "MTS_fitted_Bmem_diagnostic" else "not_applicable"),
        "residual": residual,
        "predicted": predicted,
        "edge_rows": edge_rows,
    }


def fixed_alpha_fit_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "release": score["release"],
            "alpha_candidate": score["alpha_candidate"],
            "alpha_fixed": score["alpha_fixed"],
            "model": score["model"],
            "chi2_BAO": score["chi2_BAO"],
            "k": score["k"],
            "n": score["n"],
            "AIC": score["AIC"],
            "BIC": score["BIC"],
            "converged": score["converged"],
            "prior_edge_flag": score["prior_edge_flag"],
            "Omega_m": score["Omega_m"],
            "w": score["w"],
            "w0": score["w0"],
            "wa": score["wa"],
            "B_mem": score["B_mem"],
            "B_mem_fit_status": score["B_mem_fit_status"],
            "claim_ceiling": "fixed_alpha_shape_stress_only",
        }
        for score in scores
    ]


def shared_alpha_reference_rows(shared_lookup: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (release, model), row in sorted(shared_lookup.items()):
        rows.append(
            {
                "release": release,
                "model": model,
                "shared_alpha_chi2_BAO": row["chi2_BAO"],
                "shared_alpha_AIC": row["AIC"],
                "shared_alpha_BIC": row["BIC"],
                "shared_alpha": row["bao_alpha"],
                "k_includes_alpha": row["k"],
                "claim_ceiling": "shared_alpha_empirical_reference_only",
            }
        )
    return rows


def locked_comparison_rows(scores: list[dict[str, Any]], shared_lookup: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_key = {(score["release"], score["alpha_candidate"], score["model"]): score for score in scores}
    references = ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero", "MTS_fitted_Bmem_diagnostic"]
    alpha_candidates_sorted = sorted({score["alpha_candidate"] for score in scores})
    releases_sorted = sorted({score["release"] for score in scores})
    for release in releases_sorted:
        shared_locked = shared_lookup[(release, "MTS_locked_2over27")]
        for alpha_candidate in alpha_candidates_sorted:
            locked = by_key[(release, alpha_candidate, "MTS_locked_2over27")]
            rows.append(
                {
                    "release": release,
                    "alpha_candidate": alpha_candidate,
                    "candidate": "MTS_locked_2over27",
                    "reference": "MTS_locked_2over27_shared_alpha",
                    "delta_chi2": locked["chi2_BAO"] - float(shared_locked["chi2_BAO"]),
                    "delta_AIC": locked["AIC"] - float(shared_locked["AIC"]),
                    "delta_BIC": locked["BIC"] - float(shared_locked["BIC"]),
                    "readout": "strict_alpha_penalty_vs_shared_alpha_reference",
                }
            )
            for reference in references:
                ref = by_key[(release, alpha_candidate, reference)]
                rows.append(
                    {
                        "release": release,
                        "alpha_candidate": alpha_candidate,
                        "candidate": "MTS_locked_2over27",
                        "reference": reference,
                        "delta_chi2": locked["chi2_BAO"] - ref["chi2_BAO"],
                        "delta_AIC": locked["AIC"] - ref["AIC"],
                        "delta_BIC": locked["BIC"] - ref["BIC"],
                        "readout": comparison_readout(reference, locked["chi2_BAO"] - ref["chi2_BAO"], locked["AIC"] - ref["AIC"], locked["BIC"] - ref["BIC"]),
                    }
                )
    return rows


def comparison_readout(reference: str, delta_chi2: float, delta_aic: float, delta_bic: float) -> str:
    if reference == "MTS_fitted_Bmem_diagnostic":
        if delta_chi2 <= 0.5:
            return "locked_close_to_fitted_Bmem_diagnostic"
        if delta_chi2 <= 2.0:
            return "locked_small_penalty_vs_fitted_Bmem"
        return "locked_large_penalty_vs_fitted_Bmem"
    if delta_aic < 0.0 and delta_bic < 0.0:
        return "locked_wins_AIC_BIC"
    if delta_aic < 0.0 <= delta_bic:
        return "locked_split_AIC_only"
    if delta_aic >= 0.0 and delta_bic < 0.0:
        return "locked_split_BIC_only"
    return "locked_loses_AIC_BIC"


def candidate_scorecard_rows(scores: list[dict[str, Any]], shared_lookup: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_key = {(score["release"], score["alpha_candidate"], score["model"]): score for score in scores}
    for release in sorted({score["release"] for score in scores}):
        shared_locked = shared_lookup[(release, "MTS_locked_2over27")]
        for alpha_candidate in sorted({score["alpha_candidate"] for score in scores}):
            locked = by_key[(release, alpha_candidate, "MTS_locked_2over27")]
            lcdm = by_key[(release, alpha_candidate, "LCDM")]
            wc_dm = by_key[(release, alpha_candidate, "wCDM")]
            cpl = by_key[(release, alpha_candidate, "CPL")]
            delta_shared = locked["chi2_BAO"] - float(shared_locked["chi2_BAO"])
            if delta_shared <= 1.0 and locked["chi2_BAO"] <= lcdm["chi2_BAO"]:
                verdict = "strict_alpha_survives"
            elif delta_shared <= 4.0:
                verdict = "strict_alpha_soft_warning"
            else:
                verdict = "strict_alpha_pressure"
            rows.append(
                {
                    "release": release,
                    "alpha_candidate": alpha_candidate,
                    "locked_chi2": locked["chi2_BAO"],
                    "locked_delta_chi2_vs_shared_alpha": delta_shared,
                    "locked_delta_chi2_vs_LCDM_same_alpha": locked["chi2_BAO"] - lcdm["chi2_BAO"],
                    "locked_delta_chi2_vs_wCDM_same_alpha": locked["chi2_BAO"] - wc_dm["chi2_BAO"],
                    "locked_delta_chi2_vs_CPL_same_alpha": locked["chi2_BAO"] - cpl["chi2_BAO"],
                    "locked_edge_flag": locked["prior_edge_flag"],
                    "verdict": verdict,
                }
            )
    return rows


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "fixed-alpha branch choice",
            "needed": "derive which H0-r_d product fixes alpha before seeing BAO residuals",
            "current_status": "not_parent_owned",
            "promotion_gate": "fail",
        },
        {
            "contract": "shared-alpha scorecard policy",
            "needed": "when alpha is fitted, count it as a nuisance parameter and give it to all baselines",
            "current_status": "implemented_in_existing_runners",
            "promotion_gate": "empirical_only",
        },
        {
            "contract": "strict-alpha survival",
            "needed": "predeclared fixed alpha should not catastrophically worsen BAO shape",
            "current_status": "tested_here",
            "promotion_gate": "diagnostic",
        },
        {
            "contract": "no cherry-picked alpha",
            "needed": "readback alpha values cannot become predictions after seeing BAO",
            "current_status": "guardrail_active",
            "promotion_gate": "fail_if_violated",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    strict_survivors = [row for row in scorecard if row["verdict"] == "strict_alpha_survives"]
    severe_pressure = [row for row in scorecard if row["verdict"] == "strict_alpha_pressure"]
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal stress gate",
        },
        {
            "gate": "fixed-alpha candidates scored against same baselines",
            "status": "pass",
            "evidence": f"scorecard_rows={len(scorecard)}",
            "claim_allowed": "fair diagnostic",
        },
        {
            "gate": "at least one strict-alpha branch survives diagnostic",
            "status": "pass" if strict_survivors else "warning",
            "evidence": f"strict_survivors={len(strict_survivors)}",
            "claim_allowed": "diagnostic only",
        },
        {
            "gate": "strict-alpha pressure recorded",
            "status": "warning" if severe_pressure else "pass",
            "evidence": f"strict_alpha_pressure_rows={len(severe_pressure)}",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "parent H0-r_d alpha derived",
            "status": "fail",
            "evidence": "fixed alpha candidates are tested/readbacks, not parent-derived",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "BAO support claim allowed",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows(scorecard: list[dict[str, Any]]) -> list[dict[str, Any]]:
    survivors = [row for row in scorecard if row["verdict"] == "strict_alpha_survives"]
    warnings = [row for row in scorecard if row["verdict"] == "strict_alpha_soft_warning"]
    pressures = [row for row in scorecard if row["verdict"] == "strict_alpha_pressure"]
    best_row = min(scorecard, key=lambda row: float(row["locked_delta_chi2_vs_shared_alpha"]))
    return [
        {
            "decision": STATUS,
            "meaning": "Fixed-alpha BAO shape stress has been run against the same baselines. Any strict-alpha survival is diagnostic only because the H0-r_d product is not parent-derived; shared alpha remains the fair empirical policy.",
            "strict_alpha_survivor_count": len(survivors),
            "strict_alpha_soft_warning_count": len(warnings),
            "strict_alpha_pressure_count": len(pressures),
            "best_release": best_row["release"],
            "best_alpha_candidate": best_row["alpha_candidate"],
            "best_locked_delta_chi2_vs_shared_alpha": best_row["locked_delta_chi2_vs_shared_alpha"],
            "next_target": "201-BAO-strict-alpha-results-and-H0-rd-owner-decision.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None, max_iter: int = 160) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_200_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    rdrag = rdrag_baseline()
    sources = source_register_rows()
    shared_lookup = shared_fit_lookup()
    candidates = alpha_candidates(rdrag)
    candidate_rows = alpha_candidate_rows(candidates, shared_lookup)
    bao_by_release = {
        release: runner.read_bao_data(paths["mean"], paths["cov"])
        for release, paths in bao_only.RELEASES.items()
    }
    scores: list[dict[str, Any]] = []
    for release, bao in bao_by_release.items():
        for candidate in candidates:
            for model in MODEL_ORDER:
                scores.append(score_model_fixed_alpha(release, model, bao, candidate["alpha_candidate"], float(candidate["alpha"]), max_iter))
    fit_summary = fixed_alpha_fit_summary_rows(scores)
    shared_refs = shared_alpha_reference_rows(shared_lookup)
    comparisons = locked_comparison_rows(scores, shared_lookup)
    scorecard = candidate_scorecard_rows(scores, shared_lookup)
    contract = parent_contract_rows()
    gates = claim_gate_rows(sources, scorecard)
    decision = decision_rows(scorecard)

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            sources,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "alpha_candidate_manifest.csv": (
            candidate_rows,
            [
                "alpha_candidate",
                "alpha",
                "delta_vs_DR2_locked_shared_alpha",
                "frac_delta_vs_DR2_locked_shared_alpha",
                "delta_vs_DR1_locked_shared_alpha",
                "frac_delta_vs_DR1_locked_shared_alpha",
                "basis",
                "parent_status",
            ],
        ),
        "fixed_alpha_fit_summary.csv": (
            fit_summary,
            [
                "release",
                "alpha_candidate",
                "alpha_fixed",
                "model",
                "chi2_BAO",
                "k",
                "n",
                "AIC",
                "BIC",
                "converged",
                "prior_edge_flag",
                "Omega_m",
                "w",
                "w0",
                "wa",
                "B_mem",
                "B_mem_fit_status",
                "claim_ceiling",
            ],
        ),
        "shared_alpha_reference.csv": (
            shared_refs,
            ["release", "model", "shared_alpha_chi2_BAO", "shared_alpha_AIC", "shared_alpha_BIC", "shared_alpha", "k_includes_alpha", "claim_ceiling"],
        ),
        "locked_branch_comparisons.csv": (
            comparisons,
            ["release", "alpha_candidate", "candidate", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "readout"],
        ),
        "alpha_candidate_scorecard.csv": (
            scorecard,
            [
                "release",
                "alpha_candidate",
                "locked_chi2",
                "locked_delta_chi2_vs_shared_alpha",
                "locked_delta_chi2_vs_LCDM_same_alpha",
                "locked_delta_chi2_vs_wCDM_same_alpha",
                "locked_delta_chi2_vs_CPL_same_alpha",
                "locked_edge_flag",
                "verdict",
            ],
        ),
        "parent_H0_rd_contract.csv": (
            contract,
            ["contract", "needed", "current_status", "promotion_gate"],
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
                "strict_alpha_survivor_count",
                "strict_alpha_soft_warning_count",
                "strict_alpha_pressure_count",
                "best_release",
                "best_alpha_candidate",
                "best_locked_delta_chi2_vs_shared_alpha",
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
        "fixed_alpha_scores": len(scores),
        "strict_alpha_survivor_count": decision[0]["strict_alpha_survivor_count"],
        "strict_alpha_soft_warning_count": decision[0]["strict_alpha_soft_warning_count"],
        "strict_alpha_pressure_count": decision[0]["strict_alpha_pressure_count"],
        "best_release": decision[0]["best_release"],
        "best_alpha_candidate": decision[0]["best_alpha_candidate"],
        "best_locked_delta_chi2_vs_shared_alpha": decision[0]["best_locked_delta_chi2_vs_shared_alpha"],
        "parent_H0_rd_alpha_derived": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    parser.add_argument("--max-iter", type=int, default=160, help="Optimizer iteration budget per start.")
    args = parser.parse_args()
    payload = run(args.timestamp, args.max_iter)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
