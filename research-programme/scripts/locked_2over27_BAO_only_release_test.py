#!/usr/bin/env python3
"""BAO-only DR1/DR2 release test for the locked B_mem=2/27 branch."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg, optimize


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = POST_CHECKPOINT / "scripts"
RUNS_ROOT = POST_CHECKPOINT / "runs"
FORMALIZATION_WORKBENCH = POST_CHECKPOINT.parent / "formalization-workbench"
DATA_ROOT = FORMALIZATION_WORKBENCH / "data" / "cosmology"

sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as runner  # noqa: E402


LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25

RELEASES = {
    "DESI_DR2_primary": {
        "mean": DATA_ROOT / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": DATA_ROOT / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt",
    },
    "DESI_DR1_primary": {
        "mean": DATA_ROOT / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": DATA_ROOT / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt",
    },
}

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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def file_sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def model_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "fixed": "LCDM background",
            "fitted": "Omega_m; BAO alpha",
            "claim_ceiling": "baseline",
        },
        {
            "model": "wCDM",
            "role": "baseline",
            "fixed": "constant w",
            "fitted": "Omega_m; w; BAO alpha",
            "claim_ceiling": "baseline",
        },
        {
            "model": "CPL",
            "role": "baseline",
            "fixed": "CPL form",
            "fitted": "Omega_m; w0; wa; BAO alpha",
            "claim_ceiling": "baseline",
        },
        {
            "model": "MTS_locked_2over27",
            "role": "predeclared_locked_branch",
            "fixed": "p=3; u3=1/4; DeltaR=2/9; B_mem=2/27",
            "fitted": "Omega_m; BAO alpha",
            "claim_ceiling": "external_holdout_empirical_branch_not_prediction",
        },
        {
            "model": "MTS_Bmem_zero",
            "role": "negative_control",
            "fixed": "p=3; u3=1/4; B_mem=0",
            "fitted": "Omega_m; BAO alpha",
            "claim_ceiling": "control",
        },
        {
            "model": "MTS_fitted_Bmem_diagnostic",
            "role": "diagnostic_only",
            "fixed": "p=3; u3=1/4",
            "fitted": "Omega_m; B_mem; BAO alpha",
            "claim_ceiling": "diagnostic_not_holdout",
        },
    ]


def priors_for_model(model: str) -> dict[str, tuple[float, float]]:
    priors: dict[str, tuple[float, float]] = {"Omega_m": (0.05, 0.6)}
    if model == "wCDM":
        priors["w"] = (-2.0, -0.2)
    elif model == "CPL":
        priors["w0"] = (-2.0, -0.2)
        priors["wa"] = (-2.0, 2.0)
    elif model == "MTS_fitted_Bmem_diagnostic":
        priors["B_mem"] = (-1.0, 1.0)
    return priors


def physical_model_and_params(model: str, params: dict[str, float]) -> tuple[str, dict[str, float]]:
    if model == "MTS_locked_2over27":
        out = dict(params)
        out.update({"B_mem": LOCKED_B_MEM, "p": LOCKED_P, "u3": LOCKED_U3})
        return "MTS_fixed_p3_u3quarter", out
    if model == "MTS_fitted_Bmem_diagnostic":
        out = dict(params)
        out.update({"p": LOCKED_P, "u3": LOCKED_U3})
        return "MTS_fixed_p3_u3quarter", out
    if model == "MTS_Bmem_zero":
        out = dict(params)
        out.update({"B_mem": 0.0, "p": LOCKED_P, "u3": LOCKED_U3})
        return "MTS_Bmem_zero", out
    return model, dict(params)


def schema_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for release, paths in RELEASES.items():
        for kind, path in paths.items():
            exists = path.exists()
            readable = False
            row_count = ""
            columns = ""
            issue = ""
            sha256 = ""
            try:
                if exists:
                    sha256 = file_sha256(path)
                    with path.open("r", encoding="utf-8-sig") as handle:
                        non_comment = [line.strip() for line in handle if line.strip() and not line.strip().startswith("#")]
                    readable = True
                    row_count = len(non_comment)
                    columns = len(non_comment[0].split()) if non_comment else 0
            except Exception as exc:  # noqa: BLE001
                issue = str(exc)
            rows.append(
                {
                    "release": release,
                    "kind": kind,
                    "path": str(path),
                    "exists": exists,
                    "readable": readable,
                    "row_count": row_count,
                    "columns": columns,
                    "sha256": sha256,
                    "issue": issue,
                }
            )
    return rows


def loaded_release_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for release, paths in RELEASES.items():
        try:
            bao = runner.read_bao_data(paths["mean"], paths["cov"])
            covariance = np.asarray(bao["covariance"], dtype=float)
            eig_min = float(np.min(linalg.eigvalsh(covariance)))
            quantities = ";".join(sorted({row["quantity"] for row in bao["rows"]}))
            rows.append(
                {
                    "release": release,
                    "mean_path": str(paths["mean"]),
                    "cov_path": str(paths["cov"]),
                    "bao_rows": len(bao["rows"]),
                    "cov_shape": f"{covariance.shape[0]}x{covariance.shape[1]}",
                    "min_cov_eigenvalue": eig_min,
                    "quantities": quantities,
                    "load_status": "pass" if eig_min > 0.0 else "warning_nonpositive_covariance",
                    "issue": "",
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "release": release,
                    "mean_path": str(paths["mean"]),
                    "cov_path": str(paths["cov"]),
                    "bao_rows": "",
                    "cov_shape": "",
                    "min_cov_eigenvalue": "",
                    "quantities": "",
                    "load_status": "fail",
                    "issue": str(exc),
                }
            )
    return rows


def params_from_vector(model: str, names: list[str], vector: np.ndarray) -> dict[str, float]:
    return dict(zip(names, (float(value) for value in vector), strict=True))


def prior_edge_rows(release: str, model: str, priors: dict[str, tuple[float, float]], params: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for parameter, (lower, upper) in priors.items():
        best_fit = params[parameter]
        width = upper - lower
        distance = min(best_fit - lower, upper - best_fit)
        edge_flag = distance < 0.01 * width
        rows.append(
            {
                "release": release,
                "model": model,
                "parameter": parameter,
                "best_fit": best_fit,
                "lower": lower,
                "upper": upper,
                "distance_to_edge": distance,
                "edge_flag": edge_flag,
            }
        )
    return rows


def score_model(release: str, model: str, bao: dict[str, Any], max_iter: int) -> dict[str, Any]:
    priors = priors_for_model(model)
    names = list(priors)
    bounds = [priors[name] for name in names]

    def objective(vector: np.ndarray) -> float:
        try:
            params = params_from_vector(model, names, vector)
            physical_model, physical_params = physical_model_and_params(model, params)
            chi2, _, _, _ = runner.bao_chi2(physical_model, physical_params, bao)
            return chi2
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)]
    rng = np.random.default_rng(22027)
    for _ in range(max(6, min(18, max_iter // 10))):
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
    params = params_from_vector(model, names, np.asarray(result.x, dtype=float))
    physical_model, physical_params = physical_model_and_params(model, params)
    chi2, alpha, residual, predicted = runner.bao_chi2(physical_model, physical_params, bao)
    n_points = int(len(bao["rows"]))
    k_count = len(names) + 1
    aic = chi2 + 2.0 * k_count
    bic = chi2 + k_count * math.log(n_points)
    edge_rows = prior_edge_rows(release, model, priors, params)
    return {
        "release": release,
        "model": model,
        "physical_model": physical_model,
        "chi2_BAO": chi2,
        "k": k_count,
        "n": n_points,
        "AIC": aic,
        "BIC": bic,
        "converged": bool(result.success),
        "optimizer_message": str(result.message),
        "prior_edge_flag": any(row["edge_flag"] for row in edge_rows),
        "Omega_m": params.get("Omega_m", ""),
        "w": params.get("w", ""),
        "w0": params.get("w0", ""),
        "wa": params.get("wa", ""),
        "B_mem": LOCKED_B_MEM if model == "MTS_locked_2over27" else params.get("B_mem", 0.0 if model == "MTS_Bmem_zero" else ""),
        "B_mem_fit_status": "frozen" if model == "MTS_locked_2over27" else ("diagnostic_fit" if model == "MTS_fitted_Bmem_diagnostic" else "not_applicable"),
        "p": LOCKED_P if model.startswith("MTS") else "",
        "u3": LOCKED_U3 if model.startswith("MTS") else "",
        "bao_alpha": alpha,
        "claim_ceiling": "external_holdout_empirical_branch_not_prediction" if model == "MTS_locked_2over27" else ("diagnostic_not_holdout" if model == "MTS_fitted_Bmem_diagnostic" else "baseline_or_control"),
        "edge_rows": edge_rows,
        "residual": residual,
        "predicted": predicted,
    }


def fit_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "release": score["release"],
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
            "p": score["p"],
            "u3": score["u3"],
            "bao_alpha": score["bao_alpha"],
            "claim_ceiling": score["claim_ceiling"],
        }
        for score in scores
    ]


def comparison_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_release_model = {(score["release"], score["model"]): score for score in scores}
    references = ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero", "MTS_fitted_Bmem_diagnostic"]
    for release in RELEASES:
        locked = by_release_model[(release, "MTS_locked_2over27")]
        for reference in references:
            ref = by_release_model[(release, reference)]
            rows.append(
                {
                    "release": release,
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
        if delta_chi2 <= 0.25:
            return "locked_matches_fitted_amplitude_diagnostic"
        if delta_chi2 <= 2.0:
            return "locked_small_penalty_vs_fitted_amplitude"
        return "locked_large_penalty_vs_fitted_amplitude"
    if delta_aic < 0.0 and delta_bic < 0.0:
        return "locked_wins_AIC_BIC"
    if delta_aic < 0.0 <= delta_bic:
        return "locked_split_AIC_only"
    if delta_aic >= 0.0 and delta_bic < 0.0:
        return "locked_split_BIC_only"
    return "locked_loses_AIC_BIC"


def residual_rows(scores: list[dict[str, Any]], bao_by_release: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        bao = bao_by_release[score["release"]]
        for index, (bao_row, residual, predicted) in enumerate(zip(bao["rows"], score["residual"], score["predicted"], strict=True)):
            rows.append(
                {
                    "release": score["release"],
                    "model": score["model"],
                    "row_index": index,
                    "z": bao_row["z"],
                    "quantity": bao_row["quantity"],
                    "observed": bao_row["value"],
                    "predicted": float(predicted),
                    "residual": float(residual),
                }
            )
    return rows


def release_gate_rows(scores: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_release_model = {(score["release"], score["model"]): score for score in scores}
    by_release_reference = {(row["release"], row["reference"]): row for row in comparisons}
    for release in RELEASES:
        locked = by_release_model[(release, "MTS_locked_2over27")]
        vs_lcdm = by_release_reference[(release, "LCDM")]
        vs_fitted = by_release_reference[(release, "MTS_fitted_Bmem_diagnostic")]
        if locked["prior_edge_flag"] or not locked["converged"]:
            result = "fail_locked_branch_unstable"
        elif float(vs_lcdm["delta_AIC"]) < 0.0 and float(vs_lcdm["delta_BIC"]) < 0.0:
            result = "pass_locked_beats_LCDM_IC"
        elif float(vs_lcdm["delta_chi2"]) < 0.0:
            result = "warning_locked_improves_chi2_not_IC"
        else:
            result = "fail_locked_does_not_improve_LCDM"
        rows.append(
            {
                "release": release,
                "result": result,
                "locked_B_mem": LOCKED_B_MEM,
                "locked_edge_flag": locked["prior_edge_flag"],
                "locked_converged": locked["converged"],
                "delta_chi2_vs_LCDM": vs_lcdm["delta_chi2"],
                "delta_AIC_vs_LCDM": vs_lcdm["delta_AIC"],
                "delta_BIC_vs_LCDM": vs_lcdm["delta_BIC"],
                "delta_chi2_vs_fitted_Bmem": vs_fitted["delta_chi2"],
                "interpretation": release_interpretation(result, vs_lcdm, vs_fitted),
            }
        )
    return rows


def release_interpretation(result: str, vs_lcdm: dict[str, Any], vs_fitted: dict[str, Any]) -> str:
    if result == "pass_locked_beats_LCDM_IC":
        return "locked 2/27 branch beats LCDM on BAO-only information criteria for this release"
    if result == "warning_locked_improves_chi2_not_IC":
        return "locked 2/27 improves chi2 but does not clear information-criterion gate"
    if "large_penalty" in str(vs_fitted["readout"]):
        return "locked 2/27 differs materially from fitted-amplitude diagnostic"
    return "locked branch fails this BAO-only release gate"


def decision_rows(gates: list[dict[str, Any]], comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pass_count = sum(1 for row in gates if str(row["result"]).startswith("pass"))
    warning_count = sum(1 for row in gates if str(row["result"]).startswith("warning"))
    fail_count = sum(1 for row in gates if str(row["result"]).startswith("fail"))
    if pass_count == len(RELEASES):
        verdict = "locked_2over27_BAO_only_release_pass"
    elif fail_count == 0:
        verdict = "locked_2over27_BAO_only_release_mixed_warning"
    else:
        verdict = "locked_2over27_BAO_only_release_failed_or_unstable"
    return [
        {"decision": "verdict", "value": verdict},
        {"decision": "locked_B_mem", "value": LOCKED_B_MEM},
        {"decision": "locked_DeltaR", "value": LOCKED_DELTA_R},
        {"decision": "release_pass_count", "value": pass_count},
        {"decision": "release_warning_count", "value": warning_count},
        {"decision": "release_fail_count", "value": fail_count},
        {"decision": "claim_ceiling", "value": "BAO_only_locked_amplitude_empirical_stress_not_prediction"},
        {"decision": "theory_promotion_allowed", "value": False},
        {"decision": "next_action", "value": "write_checkpoint_113_and_then_consider_CMB_distance_dry_run"},
    ]


def run_dry_run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-BAO-only-dryrun"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    schemas = schema_rows()
    loaded = loaded_release_rows()
    models = model_rows()
    failures = [
        f"{row['release']}:{row['kind']}:{row['issue'] or 'missing_or_unreadable'}"
        for row in schemas
        if not row["exists"] or not row["readable"]
    ] + [
        f"{row['release']}:load:{row['issue'] or row['load_status']}"
        for row in loaded
        if row["load_status"] != "pass"
    ]
    run_config = {
        "phase": "dry-run",
        "locked_B_mem": LOCKED_B_MEM,
        "locked_DeltaR": LOCKED_DELTA_R,
        "locked_p": LOCKED_P,
        "locked_u3": LOCKED_U3,
        "releases": {release: {key: str(value) for key, value in paths.items()} for release, paths in RELEASES.items()},
        "models": models,
        "claim_ceiling": "BAO_only_locked_amplitude_empirical_stress_not_prediction",
    }
    (run_dir / "run_config.json").write_text(json.dumps(run_config, indent=2), encoding="utf-8")
    write_csv(results_dir / "data_schema_report.csv", schemas, ["release", "kind", "path", "exists", "readable", "row_count", "columns", "sha256", "issue"])
    write_csv(results_dir / "bao_release_load_report.csv", loaded, ["release", "mean_path", "cov_path", "bao_rows", "cov_shape", "min_cov_eigenvalue", "quantities", "load_status", "issue"])
    write_csv(results_dir / "model_register.csv", models, ["model", "role", "fixed", "fitted", "claim_ceiling"])
    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "phase": "dry-run",
        "readout": "locked_2over27_BAO_only_dryrun_pass" if not failures else "locked_2over27_BAO_only_dryrun_failed",
        "scores_written": False,
        "failures": failures,
        "next_action": "run --phase score if dry-run passes" if not failures else "fix missing/unreadable BAO inputs before scoring",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def run_score(output_root: Path, max_iter: int) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-BAO-only-score"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    loaded = loaded_release_rows()
    failures = [f"{row['release']}:load:{row['issue'] or row['load_status']}" for row in loaded if row["load_status"] != "pass"]
    if failures:
        status = {
            "script": str(Path(__file__).resolve()),
            "run_dir": str(run_dir),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "phase": "score",
            "readout": "locked_2over27_BAO_only_score_aborted",
            "scores_written": False,
            "failures": failures,
        }
        write_csv(results_dir / "bao_release_load_report.csv", loaded, ["release", "mean_path", "cov_path", "bao_rows", "cov_shape", "min_cov_eigenvalue", "quantities", "load_status", "issue"])
        (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
        print(json.dumps(status, indent=2))
        return run_dir

    bao_by_release = {release: runner.read_bao_data(paths["mean"], paths["cov"]) for release, paths in RELEASES.items()}
    scores: list[dict[str, Any]] = []
    for release, bao in bao_by_release.items():
        for model in MODEL_ORDER:
            scores.append(score_model(release, model, bao, max_iter=max_iter))

    comparisons = comparison_rows(scores)
    gates = release_gate_rows(scores, comparisons)
    decisions = decision_rows(gates, comparisons)
    edge_rows = [edge_row for score in scores for edge_row in score["edge_rows"]]
    residuals = residual_rows(scores, bao_by_release)
    run_config = {
        "phase": "score",
        "max_iter": max_iter,
        "locked_B_mem": LOCKED_B_MEM,
        "locked_DeltaR": LOCKED_DELTA_R,
        "locked_p": LOCKED_P,
        "locked_u3": LOCKED_U3,
        "releases": {release: {key: str(value) for key, value in paths.items()} for release, paths in RELEASES.items()},
        "models": model_rows(),
        "claim_ceiling": "BAO_only_locked_amplitude_empirical_stress_not_prediction",
    }
    (run_dir / "run_config.json").write_text(json.dumps(run_config, indent=2), encoding="utf-8")
    write_csv(results_dir / "bao_release_load_report.csv", loaded, ["release", "mean_path", "cov_path", "bao_rows", "cov_shape", "min_cov_eigenvalue", "quantities", "load_status", "issue"])
    write_csv(results_dir / "model_register.csv", model_rows(), ["model", "role", "fixed", "fitted", "claim_ceiling"])
    write_csv(results_dir / "fit_summary.csv", fit_summary_rows(scores), ["release", "model", "chi2_BAO", "k", "n", "AIC", "BIC", "converged", "prior_edge_flag", "Omega_m", "w", "w0", "wa", "B_mem", "B_mem_fit_status", "p", "u3", "bao_alpha", "claim_ceiling"])
    write_csv(results_dir / "prior_edge_table.csv", edge_rows, ["release", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(results_dir / "locked_branch_comparisons.csv", comparisons, ["release", "candidate", "reference", "delta_chi2", "delta_AIC", "delta_BIC", "readout"])
    write_csv(results_dir / "release_gates.csv", gates, ["release", "result", "locked_B_mem", "locked_edge_flag", "locked_converged", "delta_chi2_vs_LCDM", "delta_AIC_vs_LCDM", "delta_BIC_vs_LCDM", "delta_chi2_vs_fitted_Bmem", "interpretation"])
    write_csv(results_dir / "residuals.csv", residuals, ["release", "model", "row_index", "z", "quantity", "observed", "predicted", "residual"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "phase": "score",
        "readout": decisions[0]["value"],
        "scores_written": True,
        "locked_B_mem": LOCKED_B_MEM,
        "locked_DeltaR": LOCKED_DELTA_R,
        "release_count": len(RELEASES),
        "claim_ceiling": "BAO_only_locked_amplitude_empirical_stress_not_prediction",
        "theory_promotion_allowed": False,
        "next_action": "inspect release_gates and write checkpoint 113",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["dry-run", "score"], default="dry-run")
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--max-iter", type=int, default=180)
    args = parser.parse_args()
    if args.phase == "dry-run":
        run_dry_run(args.output_root)
    else:
        run_score(args.output_root, max_iter=args.max_iter)


if __name__ == "__main__":
    main()
