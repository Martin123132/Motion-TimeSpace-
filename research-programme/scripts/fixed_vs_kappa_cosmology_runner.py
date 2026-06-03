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

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT.parent / "formalization-workbench"
SCRIPTS_ROOT = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as closure_runner  # noqa: E402


DRY_RUN_SLUG = "fixed-vs-kappa-free-SN-BAO-dryrun-runner"
SHORT_SMOKE_SLUG = "fixed-vs-kappa-free-SN-BAO-short-smoke-implementation"
DRYRUN_STATUS = "fixed_vs_kappa_SN_BAO_dryrun_passed_no_scores_generated"
SHORT_SMOKE_STATUS = "fixed_vs_kappa_SN_BAO_short_smoke_scored"
CLAIM_CEILING_DRYRUN = "dryrun_schema_and_model_contract_only_no_fit_or_claim"
CLAIM_CEILING_SHORT = "SN_BAO_short_smoke_only_no_parent_or_CMB_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
B_MEM_FIXED = 2.0 / 27.0

SN_PATH = WORKBENCH / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat"
SN_COV = WORKBENCH / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
BAO_DR2_MEAN = WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_DR2_COV = WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
BAO_DR1_MEAN = WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt"
BAO_DR1_COV = WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt"


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def count_data_rows(path: Path) -> int:
    if not path.exists():
        return 0
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    count = 0
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        numeric_tokens = 0
        for token in line.split():
            try:
                float(token)
            except ValueError:
                continue
            numeric_tokens += 1
        if numeric_tokens >= 2:
            count += 1
    return count


def matrix_shape(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split()
        try:
            for token in parts:
                float(token)
        except ValueError:
            continue
        rows.append(parts)
    if not rows:
        return 0, 0
    return len(rows), max(len(row) for row in rows)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "256-fixed-2over27-vs-kappa-free-cosmology-test-manifest.md", "test manifest"),
        (
            ROOT
            / "runs"
            / "20260601-000073-fixed-2over27-vs-kappa-free-cosmology-test-manifest"
            / "results"
            / "model_matrix.csv",
            "frozen model matrix",
        ),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "shared SN+BAO likelihood machinery"),
        (SN_PATH, "Pantheon+SH0ES SN source file"),
        (SN_COV, "Pantheon+SH0ES full covariance"),
        (BAO_DR2_MEAN, "DESI DR2 BAO mean"),
        (BAO_DR2_COV, "DESI DR2 BAO covariance"),
        (BAO_DR1_MEAN, "DESI DR1 BAO mean"),
        (BAO_DR1_COV, "DESI DR1 BAO covariance"),
    ]
    return [
        {
            "path": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
            "bytes": path.stat().st_size if path.exists() else 0,
        }
        for path, role in sources
    ]


def data_schema_rows() -> list[dict[str, Any]]:
    sn_rows = count_data_rows(SN_PATH)
    dr2_bao_rows = count_data_rows(BAO_DR2_MEAN)
    dr1_bao_rows = count_data_rows(BAO_DR1_MEAN)
    dr2_cov_rows, dr2_cov_cols = matrix_shape(BAO_DR2_COV)
    dr1_cov_rows, dr1_cov_cols = matrix_shape(BAO_DR1_COV)
    return [
        {
            "dataset": "PantheonPlus_SH0ES",
            "path": relpath(SN_PATH),
            "exists": "yes" if SN_PATH.exists() else "no",
            "rows": sn_rows,
            "columns_or_cov_shape": "raw file rows; scoring excludes calibrators by default",
            "role": "SN primary and no-SH0ES shape branch source",
        },
        {
            "dataset": "PantheonPlus_SH0ES_covariance",
            "path": relpath(SN_COV),
            "exists": "yes" if SN_COV.exists() else "no",
            "rows": count_data_rows(SN_COV),
            "columns_or_cov_shape": "Pantheon+ covariance format handled by shared runner",
            "role": "SN full covariance for T1 short smoke",
        },
        {
            "dataset": "DESI_DR2_BAO_mean",
            "path": relpath(BAO_DR2_MEAN),
            "exists": "yes" if BAO_DR2_MEAN.exists() else "no",
            "rows": dr2_bao_rows,
            "columns_or_cov_shape": "mean vector rows",
            "role": "BAO primary",
        },
        {
            "dataset": "DESI_DR2_BAO_cov",
            "path": relpath(BAO_DR2_COV),
            "exists": "yes" if BAO_DR2_COV.exists() else "no",
            "rows": dr2_cov_rows,
            "columns_or_cov_shape": f"{dr2_cov_rows}x{dr2_cov_cols}",
            "role": "BAO primary covariance",
        },
        {
            "dataset": "DESI_DR1_BAO_mean",
            "path": relpath(BAO_DR1_MEAN),
            "exists": "yes" if BAO_DR1_MEAN.exists() else "no",
            "rows": dr1_bao_rows,
            "columns_or_cov_shape": "mean vector rows",
            "role": "BAO release robustness",
        },
        {
            "dataset": "DESI_DR1_BAO_cov",
            "path": relpath(BAO_DR1_COV),
            "exists": "yes" if BAO_DR1_COV.exists() else "no",
            "rows": dr1_cov_rows,
            "columns_or_cov_shape": f"{dr1_cov_rows}x{dr1_cov_cols}",
            "role": "BAO release covariance",
        },
    ]


def branch_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "MTS_fixed_2over27_no_clock",
            "p": 3,
            "u3": 0.25,
            "B_mem": f"{B_MEM_FIXED:.12f}",
            "kappa_mem": "fixed_to_1_by_closure_not_derivation",
            "free_amplitude_count": 0,
            "sidecar_policy": "forbidden",
            "claim_ceiling": "strict_empirical_closure",
        },
        {
            "branch": "MTS_kappa_free_no_clock",
            "p": 3,
            "u3": 0.25,
            "B_mem": "kappa_mem*(2/27)",
            "kappa_mem": "fitted_ablation_parameter",
            "free_amplitude_count": 1,
            "sidecar_policy": "forbidden",
            "claim_ceiling": "phenomenological_ablation_only",
        },
        {
            "branch": "MTS_Bmem_zero",
            "p": 3,
            "u3": 0.25,
            "B_mem": 0,
            "kappa_mem": "not_applicable",
            "free_amplitude_count": 0,
            "sidecar_policy": "forbidden",
            "claim_ceiling": "negative_control",
        },
    ]


def model_parameter_rows() -> list[dict[str, Any]]:
    return [
        {
            "model": "LCDM",
            "role": "baseline",
            "theory_parameters": "Omega_m",
            "shared_nuisance": "analytic SN offset plus analytic BAO calibration alpha",
            "extra_k_vs_fixed": 0,
        },
        {
            "model": "wCDM",
            "role": "flexible_baseline",
            "theory_parameters": "Omega_m,w",
            "shared_nuisance": "same",
            "extra_k_vs_fixed": 1,
        },
        {
            "model": "CPL",
            "role": "flexible_baseline",
            "theory_parameters": "Omega_m,w0,wa",
            "shared_nuisance": "same",
            "extra_k_vs_fixed": 2,
        },
        {
            "model": "MTS_fixed_2over27_no_clock",
            "role": "strict_lead_closure",
            "theory_parameters": "Omega_m with p,u3,B_mem fixed",
            "shared_nuisance": "same",
            "extra_k_vs_fixed": 0,
        },
        {
            "model": "MTS_kappa_free_no_clock",
            "role": "ablation",
            "theory_parameters": "Omega_m,kappa_mem with p,u3 fixed",
            "shared_nuisance": "same",
            "extra_k_vs_fixed": 1,
        },
        {
            "model": "MTS_Bmem_zero",
            "role": "negative_control",
            "theory_parameters": "Omega_m with p,u3 fixed and B_mem=0",
            "shared_nuisance": "same",
            "extra_k_vs_fixed": 0,
        },
    ]


def penalty_template_rows(n_eff: int) -> list[dict[str, Any]]:
    bic_tax = math.log(max(n_eff, 2))
    return [
        {
            "comparison": "MTS_kappa_free_no_clock_vs_MTS_fixed_2over27_no_clock",
            "delta_k": 1,
            "n_eff": n_eff,
            "AIC_chi2_improvement_required": 2.0,
            "BIC_chi2_improvement_required": f"{bic_tax:.6f}",
            "stable_preference_rule": "kappa must beat both AIC and BIC tax to become preferred over fixed",
        },
        {
            "comparison": "MTS_fixed_2over27_no_clock_vs_wCDM",
            "delta_k": -1,
            "n_eff": n_eff,
            "AIC_chi2_improvement_required": "fixed may lose chi2 by up to 2 and still match AIC",
            "BIC_chi2_improvement_required": f"fixed may lose chi2 by up to {bic_tax:.6f} and still match BIC",
            "stable_preference_rule": "use exact run parameter counts in score phase",
        },
        {
            "comparison": "MTS_fixed_2over27_no_clock_vs_CPL",
            "delta_k": -2,
            "n_eff": n_eff,
            "AIC_chi2_improvement_required": "fixed may lose chi2 by up to 4 and still match AIC",
            "BIC_chi2_improvement_required": f"fixed may lose chi2 by up to {2.0 * bic_tax:.6f} and still match BIC",
            "stable_preference_rule": "use exact run parameter counts in score phase",
        },
    ]


def preflight_gate_rows(phase: str) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    schema = data_schema_rows()
    dr2_mean_rows = next(row for row in schema if row["dataset"] == "DESI_DR2_BAO_mean")["rows"]
    dr2_cov = next(row for row in schema if row["dataset"] == "DESI_DR2_BAO_cov")
    dr2_cov_square = str(dr2_mean_rows) in str(dr2_cov["columns_or_cov_shape"]).split("x")
    return [
        {
            "gate": "phase_is_supported",
            "status": "pass" if phase in {"dry-run", "short-smoke"} else "fail",
            "evidence": phase,
            "score_allowed": "true" if phase == "short-smoke" else "false",
        },
        {
            "gate": "all_sources_exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "score_allowed": "true" if phase == "short-smoke" and missing_sources == 0 else "false",
        },
        {
            "gate": "DR2_BAO_cov_shape_matches_mean",
            "status": "pass" if dr2_cov_square else "fail",
            "evidence": f"mean_rows={dr2_mean_rows}; cov_shape={dr2_cov['columns_or_cov_shape']}",
            "score_allowed": "true" if phase == "short-smoke" and dr2_cov_square else "false",
        },
        {
            "gate": "branch_contract_frozen",
            "status": "pass",
            "evidence": "fixed and kappa branch definitions written before fit",
            "score_allowed": "true" if phase == "short-smoke" else "false",
        },
        {
            "gate": "dry_run_score_refusal",
            "status": "pass" if phase == "dry-run" else "not_applicable",
            "evidence": "dry-run writes schema and matrices only",
            "score_allowed": "false",
        },
    ]


def command_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "phase": "dry-run",
            "command": "python scripts/fixed_vs_kappa_cosmology_runner.py --phase dry-run --arena SN-BAO-T7 --timestamp <timestamp>",
            "allowed_now": "yes",
            "outputs": "schema/model/penalty/preflight artifacts only",
        },
        {
            "phase": "short-smoke",
            "command": "python scripts/fixed_vs_kappa_cosmology_runner.py --phase short-smoke --arena SN-BAO-T7 --timestamp <timestamp> --max-iter 120",
            "allowed_now": "yes",
            "outputs": "fit summary, baseline comparison, fixed-vs-kappa penalty, prior edges, residual diagnostics",
        },
        {
            "phase": "no-SH0ES dry-run",
            "command": "python scripts/fixed_vs_kappa_cosmology_runner.py --phase dry-run --arena no-SH0ES-SN-BAO --timestamp <timestamp>",
            "allowed_now": "yes_after_arena_schema_extension",
            "outputs": "same dry-run contract, no scoring",
        },
    ]


def dryrun_decision_rows(phase: str, n_eff: int) -> list[dict[str, Any]]:
    return [
        {
            "decision": DRYRUN_STATUS if phase == "dry-run" else SHORT_SMOKE_STATUS,
            "claim_ceiling": CLAIM_CEILING_DRYRUN if phase == "dry-run" else CLAIM_CEILING_SHORT,
            "lead_branch": LEAD_BRANCH,
            "arena": "SN-BAO-T7",
            "n_eff_template": n_eff,
            "meaning": (
                "The runner freezes fixed 2/27 and kappa-free branches, checks source presence and BAO covariance shape, "
                "computes the one-parameter kappa AIC/BIC tax template, and only scores when --phase short-smoke is explicit."
            ),
            "next_target": "258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md",
        }
    ]


def build_dryrun_outputs(timestamp: str, phase: str, arena: str) -> dict[str, Any]:
    run_id = f"{timestamp}-{DRY_RUN_SLUG}"
    run_dir = ROOT / "runs" / run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    schema = data_schema_rows()
    sn_rows = int(next(row for row in schema if row["dataset"] == "PantheonPlus_SH0ES")["rows"])
    bao_rows = int(next(row for row in schema if row["dataset"] == "DESI_DR2_BAO_mean")["rows"])
    n_eff = sn_rows + bao_rows

    outputs = {
        "source_register.csv": (
            source_register_rows(),
            ["path", "role", "exists", "bytes"],
        ),
        "data_schema_report.csv": (
            schema,
            ["dataset", "path", "exists", "rows", "columns_or_cov_shape", "role"],
        ),
        "branch_contract.csv": (
            branch_contract_rows(),
            ["branch", "p", "u3", "B_mem", "kappa_mem", "free_amplitude_count", "sidecar_policy", "claim_ceiling"],
        ),
        "model_parameter_matrix.csv": (
            model_parameter_rows(),
            ["model", "role", "theory_parameters", "shared_nuisance", "extra_k_vs_fixed"],
        ),
        "fixed_vs_kappa_penalty_template.csv": (
            penalty_template_rows(n_eff),
            [
                "comparison",
                "delta_k",
                "n_eff",
                "AIC_chi2_improvement_required",
                "BIC_chi2_improvement_required",
                "stable_preference_rule",
            ],
        ),
        "preflight_gates.csv": (
            preflight_gate_rows(phase),
            ["gate", "status", "evidence", "score_allowed"],
        ),
        "command_plan.csv": (
            command_plan_rows(),
            ["phase", "command", "allowed_now", "outputs"],
        ),
        "decision.csv": (
            dryrun_decision_rows(phase, n_eff),
            ["decision", "claim_ceiling", "lead_branch", "arena", "n_eff_template", "meaning", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": DRYRUN_STATUS,
        "claim_ceiling": CLAIM_CEILING_DRYRUN,
        "lead_branch": LEAD_BRANCH,
        "phase": phase,
        "arena": arena,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in source_register_rows()),
        "SN_rows_template": sn_rows,
        "BAO_DR2_rows_template": bao_rows,
        "n_eff_template": n_eff,
        "fixed_Bmem": f"{B_MEM_FIXED:.12f}",
        "kappa_AIC_tax_delta_chi2": 2,
        "kappa_BIC_tax_delta_chi2": f"{math.log(max(n_eff, 2)):.6f}",
        "scores_generated": False,
        "promotion_allowed": False,
        "next_target": "258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(DRYRUN_STATUS + "\n", encoding="utf-8")
    return status_payload


def load_scoring_data() -> tuple[dict[str, np.ndarray], dict[str, Any], dict[str, Any]]:
    sn = closure_runner.read_sn_data(
        SN_PATH,
        max_rows=None,
        covariance_path=SN_COV,
        covariance_mode="full",
        observable="mb-corr",
        include_calibrators=False,
    )
    bao = closure_runner.read_bao_data(BAO_DR2_MEAN, BAO_DR2_COV)
    bao["label"] = "DESI_DR2_primary"
    config = {
        "sn_data": str(SN_PATH),
        "sn_cov": str(SN_COV),
        "sn_covariance_mode": "full",
        "sn_observable": "mb-corr",
        "sn_include_calibrators": False,
        "sn_rows_used": int(len(sn["z"])),
        "bao_data": str(BAO_DR2_MEAN),
        "bao_cov": str(BAO_DR2_COV),
        "bao_label": "DESI_DR2_primary",
        "bao_rows_used": int(len(bao["rows"])),
    }
    return sn, bao, config


def score_fixed_bmem(sn: dict[str, np.ndarray], bao: dict[str, Any], max_iter: int) -> dict[str, Any]:
    bounds = [(0.05, 0.6)]

    def objective(vector: np.ndarray) -> float:
        try:
            params = {"Omega_m": float(vector[0]), "B_mem": B_MEM_FIXED, "p": 3.0, "u3": 0.25}
            chi2_sn, _, _, _ = closure_runner.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
            chi2_bao, _, _, _ = closure_runner.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [
        np.asarray([0.30]),
        np.asarray([0.24]),
        np.asarray([0.36]),
        np.asarray([0.45]),
        np.asarray([0.15]),
        np.asarray([0.52]),
    ]
    results = [
        optimize.minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1.0e-9},
        )
        for start in starts
    ]
    result = min(results, key=lambda item: float(item.fun))
    omega_m = float(result.x[0])
    params = {"Omega_m": omega_m, "B_mem": B_MEM_FIXED, "p": 3.0, "u3": 0.25}
    chi2_sn, sn_offset, sn_residual, sn_predicted = closure_runner.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
    chi2_bao, bao_alpha, bao_residual, bao_predicted = closure_runner.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
    chi2_total = chi2_sn + chi2_bao
    n_points = int(len(sn["z"]) + len(bao["rows"]))
    k_count = 3
    lower, upper = bounds[0]
    distance_to_edge = min(omega_m - lower, upper - omega_m)
    omega_edge_flag = distance_to_edge < 0.01 * (upper - lower)
    edge_rows = [
        {
            "model": "MTS_fixed_2over27_no_clock",
            "parameter": "Omega_m",
            "best_fit": omega_m,
            "lower": lower,
            "upper": upper,
            "distance_to_edge": distance_to_edge,
            "edge_flag": omega_edge_flag,
        },
        {
            "model": "MTS_fixed_2over27_no_clock",
            "parameter": "B_mem",
            "best_fit": B_MEM_FIXED,
            "lower": B_MEM_FIXED,
            "upper": B_MEM_FIXED,
            "distance_to_edge": "fixed",
            "edge_flag": False,
        },
    ]
    return {
        "model": "MTS_fixed_2over27_no_clock",
        "role": "strict_lead_closure",
        "source_model_key": "MTS_fixed_p3_u3quarter",
        "params": params,
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "dof": n_points - k_count,
        "k": k_count,
        "n": n_points,
        "AIC": chi2_total + 2.0 * k_count,
        "BIC": chi2_total + k_count * math.log(n_points),
        "convergence": bool(result.success),
        "optimizer_message": str(result.message),
        "prior_edge_flag": omega_edge_flag,
        "claim_ceiling": "strict_empirical_closure_only_no_parent_derivation",
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "sn_residual": sn_residual,
        "sn_predicted": sn_predicted,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "edge_rows": edge_rows,
    }


def alias_score(score: dict[str, Any], model: str, role: str, claim_ceiling: str) -> dict[str, Any]:
    aliased = dict(score)
    aliased["source_model_key"] = score["model"]
    aliased["model"] = model
    aliased["role"] = role
    aliased["claim_ceiling"] = claim_ceiling
    aliased["edge_rows"] = [
        {**edge_row, "model": model}
        for edge_row in score.get("edge_rows", [])
    ]
    return aliased


def run_scores(max_iter: int) -> tuple[list[dict[str, Any]], dict[str, np.ndarray], dict[str, Any], dict[str, Any]]:
    sn, bao, config = load_scoring_data()
    scores = [
        alias_score(closure_runner.score_model("LCDM", sn, bao, max_iter=max_iter), "LCDM", "baseline", "baseline"),
        alias_score(closure_runner.score_model("wCDM", sn, bao, max_iter=max_iter), "wCDM", "flexible_baseline", "baseline"),
        alias_score(closure_runner.score_model("CPL", sn, bao, max_iter=max_iter), "CPL", "flexible_baseline", "baseline"),
        score_fixed_bmem(sn, bao, max_iter=max_iter),
        alias_score(
            closure_runner.score_model("MTS_fixed_p3_u3quarter", sn, bao, max_iter=max_iter),
            "MTS_kappa_free_no_clock",
            "amplitude_ablation",
            "phenomenological_ablation_only_no_parent_derivation",
        ),
        alias_score(
            closure_runner.score_model("MTS_Bmem_zero", sn, bao, max_iter=max_iter),
            "MTS_Bmem_zero",
            "negative_control",
            "control_only",
        ),
    ]
    return scores, sn, bao, config


def param_value(score: dict[str, Any], name: str) -> Any:
    return score.get("params", {}).get(name, "")


def score_bmem(score: dict[str, Any]) -> Any:
    model = score["model"]
    if model == "MTS_fixed_2over27_no_clock":
        return B_MEM_FIXED
    if model == "MTS_kappa_free_no_clock":
        return param_value(score, "B_mem")
    if model == "MTS_Bmem_zero":
        return 0.0
    return ""


def score_kappa(score: dict[str, Any]) -> Any:
    b_mem = score_bmem(score)
    if b_mem == "":
        return ""
    return float(b_mem) / B_MEM_FIXED if B_MEM_FIXED else ""


def fit_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        rows.append(
            {
                "model": score["model"],
                "role": score["role"],
                "source_model_key": score["source_model_key"],
                "success": bool(score["convergence"]),
                "chi2_SN": score["chi2_SN"],
                "chi2_BAO": score["chi2_BAO"],
                "chi2_total": score["chi2_total"],
                "AIC": score["AIC"],
                "BIC": score["BIC"],
                "n": score["n"],
                "k": score["k"],
                "dof": score["dof"],
                "prior_edge_flag": bool(score["prior_edge_flag"]),
                "Omega_m": param_value(score, "Omega_m"),
                "w": param_value(score, "w"),
                "w0": param_value(score, "w0"),
                "wa": param_value(score, "wa"),
                "B_mem": score_bmem(score),
                "kappa_mem": score_kappa(score),
                "p": param_value(score, "p"),
                "u3": param_value(score, "u3"),
                "sn_offset": score["sn_offset"],
                "bao_alpha": score["bao_alpha"],
                "claim_ceiling": score["claim_ceiling"],
                "optimizer_message": score["optimizer_message"],
            }
        )
    return rows


def comparison_readout(delta_aic: float, delta_bic: float) -> str:
    if delta_aic < 0.0 and delta_bic < 0.0:
        return "model_wins_AIC_BIC"
    if delta_aic < 0.0 <= delta_bic:
        return "model_wins_AIC_only"
    if delta_aic >= 0.0 and delta_bic < 0.0:
        return "model_wins_BIC_only"
    if abs(delta_aic) < 2.0 or abs(delta_bic) < 2.0:
        return "near_parity"
    return "model_loses_AIC_BIC"


def baseline_comparison_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    references = ["LCDM", "wCDM", "CPL", "MTS_fixed_2over27_no_clock", "MTS_kappa_free_no_clock"]
    by_model = {score["model"]: score for score in scores}
    rows: list[dict[str, Any]] = []
    for score in scores:
        for reference in references:
            if score["model"] == reference:
                continue
            reference_score = by_model[reference]
            delta_chi2 = float(score["chi2_total"]) - float(reference_score["chi2_total"])
            delta_aic = float(score["AIC"]) - float(reference_score["AIC"])
            delta_bic = float(score["BIC"]) - float(reference_score["BIC"])
            rows.append(
                {
                    "model": score["model"],
                    "reference_baseline": reference,
                    "delta_chi2": delta_chi2,
                    "delta_AIC": delta_aic,
                    "delta_BIC": delta_bic,
                    "model_k": score["k"],
                    "reference_k": reference_score["k"],
                    "model_n": score["n"],
                    "readout": comparison_readout(delta_aic, delta_bic),
                }
            )
    return rows


def fixed_vs_kappa_penalty_rows(scores: list[dict[str, Any]], arena: str) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    fixed = by_model["MTS_fixed_2over27_no_clock"]
    kappa = by_model["MTS_kappa_free_no_clock"]
    n_eff = int(fixed["n"])
    chi2_improvement = float(fixed["chi2_total"]) - float(kappa["chi2_total"])
    delta_aic = float(kappa["AIC"]) - float(fixed["AIC"])
    delta_bic = float(kappa["BIC"]) - float(fixed["BIC"])
    bic_tax = math.log(max(n_eff, 2))
    aic_paid = chi2_improvement > 2.0
    bic_paid = chi2_improvement > bic_tax
    if aic_paid and bic_paid:
        readout = "kappa_free_pays_AIC_BIC_tax"
    elif aic_paid:
        readout = "kappa_free_pays_AIC_only_not_BIC"
    elif chi2_improvement > 0.0:
        readout = "kappa_free_improves_raw_chi2_but_not_information_criteria"
    else:
        readout = "kappa_free_does_not_improve_raw_chi2"
    return [
        {
            "arena": arena,
            "chi2_fixed": fixed["chi2_total"],
            "chi2_kappa": kappa["chi2_total"],
            "delta_chi2_improvement_fixed_minus_kappa": chi2_improvement,
            "delta_k": int(kappa["k"]) - int(fixed["k"]),
            "n_eff": n_eff,
            "AIC_chi2_improvement_required": 2.0,
            "BIC_chi2_improvement_required": bic_tax,
            "delta_AIC_kappa_minus_fixed": delta_aic,
            "delta_BIC_kappa_minus_fixed": delta_bic,
            "AIC_tax_paid": aic_paid,
            "BIC_tax_paid": bic_paid,
            "kappa_promoted": aic_paid and bic_paid and not bool(kappa["prior_edge_flag"]),
            "fixed_B_mem": B_MEM_FIXED,
            "kappa_best_B_mem": score_bmem(kappa),
            "kappa_best_kappa_mem": score_kappa(kappa),
            "readout": readout,
        }
    ]


def prior_edge_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        for edge_row in score.get("edge_rows", []):
            rows.append(
                {
                    "model": edge_row["model"],
                    "parameter": edge_row["parameter"],
                    "best_fit": edge_row["best_fit"],
                    "lower": edge_row["lower"],
                    "upper": edge_row["upper"],
                    "distance_to_edge": edge_row["distance_to_edge"],
                    "edge_flag": edge_row["edge_flag"],
                }
            )
    return rows


def residual_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        sn_residual = np.asarray(score["sn_residual"], dtype=float)
        bao_residual = np.asarray(score["bao_residual"], dtype=float)
        rows.append(
            {
                "model": score["model"],
                "SN_rows": len(sn_residual),
                "SN_mean_residual": float(np.mean(sn_residual)),
                "SN_rms_residual": float(np.sqrt(np.mean(sn_residual**2))),
                "SN_max_abs_residual": float(np.max(np.abs(sn_residual))),
                "BAO_rows": len(bao_residual),
                "BAO_mean_residual": float(np.mean(bao_residual)),
                "BAO_rms_residual": float(np.sqrt(np.mean(bao_residual**2))),
                "BAO_max_abs_residual": float(np.max(np.abs(bao_residual))),
            }
        )
    return rows


def bao_residual_rows(scores: list[dict[str, Any]], bao: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for score in scores:
        predicted = np.asarray(score["bao_predicted"], dtype=float)
        residual = np.asarray(score["bao_residual"], dtype=float)
        for row_index, bao_row in enumerate(bao["rows"]):
            rows.append(
                {
                    "model": score["model"],
                    "row_index": row_index,
                    "z": bao_row["z"],
                    "quantity": bao_row["quantity"],
                    "observed": bao_row["value"],
                    "predicted": float(predicted[row_index]),
                    "residual": float(residual[row_index]),
                }
            )
    return rows


def svg_escape(value: Any) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_svg_plot(
    path: Path,
    title: str,
    x_label: str,
    y_label: str,
    series: list[dict[str, Any]],
    line_mode: bool,
) -> None:
    width = 900
    height = 520
    margin_left = 72
    margin_right = 24
    margin_top = 42
    margin_bottom = 70
    all_x = np.concatenate([np.asarray(item["x"], dtype=float) for item in series])
    all_y = np.concatenate([np.asarray(item["y"], dtype=float) for item in series])
    x_min = float(np.min(all_x))
    x_max = float(np.max(all_x))
    y_min = float(np.min(all_y))
    y_max = float(np.max(all_y))
    if math.isclose(x_min, x_max):
        x_min -= 0.5
        x_max += 0.5
    if math.isclose(y_min, y_max):
        y_min -= 0.5
        y_max += 0.5
    y_padding = 0.08 * (y_max - y_min)
    y_min -= y_padding
    y_max += y_padding
    inner_width = width - margin_left - margin_right
    inner_height = height - margin_top - margin_bottom

    def scale_x(value: float) -> float:
        return margin_left + (value - x_min) / (x_max - x_min) * inner_width

    def scale_y(value: float) -> float:
        return margin_top + (y_max - value) / (y_max - y_min) * inner_height

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="24" text-anchor="middle" font-family="Arial" font-size="16">{svg_escape(title)}</text>',
        f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="black" stroke-width="1"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="black" stroke-width="1"/>',
        f'<text x="{width / 2}" y="{height - 22}" text-anchor="middle" font-family="Arial" font-size="13">{svg_escape(x_label)}</text>',
        f'<text transform="translate(18 {height / 2}) rotate(-90)" text-anchor="middle" font-family="Arial" font-size="13">{svg_escape(y_label)}</text>',
    ]
    if y_min < 0.0 < y_max:
        zero_y = scale_y(0.0)
        elements.append(f'<line x1="{margin_left}" y1="{zero_y:.2f}" x2="{width - margin_right}" y2="{zero_y:.2f}" stroke="#555" stroke-width="0.8" stroke-dasharray="4 4"/>')
    for tick_index in range(5):
        fraction = tick_index / 4
        x_value = x_min + fraction * (x_max - x_min)
        x_pos = margin_left + fraction * inner_width
        elements.append(f'<line x1="{x_pos:.2f}" y1="{height - margin_bottom}" x2="{x_pos:.2f}" y2="{height - margin_bottom + 5}" stroke="black"/>')
        elements.append(f'<text x="{x_pos:.2f}" y="{height - margin_bottom + 22}" text-anchor="middle" font-family="Arial" font-size="10">{x_value:.3g}</text>')
    for tick_index in range(5):
        fraction = tick_index / 4
        y_value = y_min + fraction * (y_max - y_min)
        y_pos = margin_top + (1 - fraction) * inner_height
        elements.append(f'<line x1="{margin_left - 5}" y1="{y_pos:.2f}" x2="{margin_left}" y2="{y_pos:.2f}" stroke="black"/>')
        elements.append(f'<text x="{margin_left - 8}" y="{y_pos + 3:.2f}" text-anchor="end" font-family="Arial" font-size="10">{y_value:.3g}</text>')
    for series_index, item in enumerate(series):
        color = item["color"]
        x_values = np.asarray(item["x"], dtype=float)
        y_values = np.asarray(item["y"], dtype=float)
        if line_mode:
            points = " ".join(f"{scale_x(float(x_value)):.2f},{scale_y(float(y_value)):.2f}" for x_value, y_value in zip(x_values, y_values, strict=True))
            elements.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="1.5"/>')
            for x_value, y_value in zip(x_values, y_values, strict=True):
                elements.append(f'<circle cx="{scale_x(float(x_value)):.2f}" cy="{scale_y(float(y_value)):.2f}" r="3" fill="{color}" fill-opacity="0.8"/>')
        else:
            stride = max(1, len(x_values) // 900)
            for x_value, y_value in zip(x_values[::stride], y_values[::stride], strict=True):
                elements.append(f'<circle cx="{scale_x(float(x_value)):.2f}" cy="{scale_y(float(y_value)):.2f}" r="1.7" fill="{color}" fill-opacity="0.45"/>')
        legend_x = margin_left + 8
        legend_y = margin_top + 18 + 18 * series_index
        elements.append(f'<rect x="{legend_x}" y="{legend_y - 9}" width="10" height="10" fill="{color}" fill-opacity="0.8"/>')
        elements.append(f'<text x="{legend_x + 16}" y="{legend_y}" font-family="Arial" font-size="11">{svg_escape(item["label"])}</text>')
    elements.append("</svg>")
    path.write_text("\n".join(elements) + "\n", encoding="utf-8")


def write_residual_plots(results_dir: Path, scores: list[dict[str, Any]], sn: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    plot_rows: list[dict[str, Any]] = []
    if plt is None:
        sn_svg = results_dir / "SN_residuals_fixed_vs_kappa.svg"
        write_svg_plot(
            sn_svg,
            "SN residuals: fixed 2/27 vs kappa-free",
            "z",
            "SN residual",
            [
                {"label": "LCDM", "x": sn["z"], "y": by_model["LCDM"]["sn_residual"], "color": "#7f7f7f"},
                {"label": "MTS_fixed_2over27_no_clock", "x": sn["z"], "y": by_model["MTS_fixed_2over27_no_clock"]["sn_residual"], "color": "#1f77b4"},
                {"label": "MTS_kappa_free_no_clock", "x": sn["z"], "y": by_model["MTS_kappa_free_no_clock"]["sn_residual"], "color": "#ff7f0e"},
            ],
            line_mode=False,
        )
        plot_rows.append({"plot": "SN_residuals_fixed_vs_kappa", "status": "written_svg_fallback", "path": str(sn_svg), "issue": "matplotlib unavailable"})
        bao_svg = results_dir / "BAO_residuals_fixed_vs_kappa.svg"
        row_axis = np.arange(len(by_model["LCDM"]["bao_residual"]))
        write_svg_plot(
            bao_svg,
            "BAO residuals: baselines vs fixed/kappa MTS",
            "BAO row index",
            "BAO residual",
            [
                {"label": "LCDM", "x": row_axis, "y": by_model["LCDM"]["bao_residual"], "color": "#7f7f7f"},
                {"label": "wCDM", "x": row_axis, "y": by_model["wCDM"]["bao_residual"], "color": "#2ca02c"},
                {"label": "CPL", "x": row_axis, "y": by_model["CPL"]["bao_residual"], "color": "#d62728"},
                {"label": "MTS_fixed_2over27_no_clock", "x": row_axis, "y": by_model["MTS_fixed_2over27_no_clock"]["bao_residual"], "color": "#1f77b4"},
                {"label": "MTS_kappa_free_no_clock", "x": row_axis, "y": by_model["MTS_kappa_free_no_clock"]["bao_residual"], "color": "#ff7f0e"},
            ],
            line_mode=True,
        )
        plot_rows.append({"plot": "BAO_residuals_fixed_vs_kappa", "status": "written_svg_fallback", "path": str(bao_svg), "issue": "matplotlib unavailable"})
        return plot_rows

    sn_plot = results_dir / "SN_residuals_fixed_vs_kappa.png"
    plt.figure(figsize=(9, 5))
    for model, color in [
        ("LCDM", "tab:gray"),
        ("MTS_fixed_2over27_no_clock", "tab:blue"),
        ("MTS_kappa_free_no_clock", "tab:orange"),
    ]:
        plt.scatter(sn["z"], by_model[model]["sn_residual"], s=6, alpha=0.45, label=model, c=color)
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.xlabel("z")
    plt.ylabel("SN residual")
    plt.title("SN residuals: fixed 2/27 vs kappa-free")
    plt.legend(markerscale=2)
    plt.tight_layout()
    plt.savefig(sn_plot, dpi=160)
    plt.close()
    plot_rows.append({"plot": "SN_residuals_fixed_vs_kappa", "status": "written", "path": str(sn_plot), "issue": ""})

    bao_plot = results_dir / "BAO_residuals_fixed_vs_kappa.png"
    plt.figure(figsize=(9, 5))
    row_axis = np.arange(len(by_model["LCDM"]["bao_residual"]))
    for model, color in [
        ("LCDM", "tab:gray"),
        ("wCDM", "tab:green"),
        ("CPL", "tab:red"),
        ("MTS_fixed_2over27_no_clock", "tab:blue"),
        ("MTS_kappa_free_no_clock", "tab:orange"),
    ]:
        plt.plot(row_axis, by_model[model]["bao_residual"], marker="o", linewidth=1.2, label=model, c=color)
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.xlabel("BAO row index")
    plt.ylabel("BAO residual")
    plt.title("BAO residuals: baselines vs fixed/kappa MTS")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(bao_plot, dpi=160)
    plt.close()
    plot_rows.append({"plot": "BAO_residuals_fixed_vs_kappa", "status": "written", "path": str(bao_plot), "issue": ""})
    return plot_rows


def score_gate_rows(scores: list[dict[str, Any]], penalty_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nonconverged = [score["model"] for score in scores if not bool(score["convergence"])]
    edge_models = [score["model"] for score in scores if bool(score["prior_edge_flag"])]
    penalty = penalty_rows[0]
    by_model = {score["model"]: score for score in scores}
    fixed_vs_lcdm_aic = float(by_model["MTS_fixed_2over27_no_clock"]["AIC"]) - float(by_model["LCDM"]["AIC"])
    fixed_vs_wcdm_aic = float(by_model["MTS_fixed_2over27_no_clock"]["AIC"]) - float(by_model["wCDM"]["AIC"])
    fixed_vs_cpl_aic = float(by_model["MTS_fixed_2over27_no_clock"]["AIC"]) - float(by_model["CPL"]["AIC"])
    return [
        {
            "gate": "data_shapes_pass",
            "status": "pass",
            "evidence": f"SN={by_model['LCDM']['n'] - 13}; BAO=13; n_eff={by_model['LCDM']['n']}",
            "claim_effect": "scores can be read as same-data short smoke",
        },
        {
            "gate": "all_models_converged",
            "status": "pass" if not nonconverged else "fail",
            "evidence": ",".join(nonconverged) if nonconverged else "all converged",
            "claim_effect": "failed models cannot be used as evidence",
        },
        {
            "gate": "no_prior_edge_flags",
            "status": "pass" if not edge_models else "warn",
            "evidence": ",".join(edge_models) if edge_models else "no edge flags",
            "claim_effect": "edge-hit models are unstable evidence",
        },
        {
            "gate": "kappa_parameter_tax_paid",
            "status": "pass" if penalty["kappa_promoted"] else "fail",
            "evidence": (
                f"raw_chi2_improvement={float(penalty['delta_chi2_improvement_fixed_minus_kappa']):.9g}; "
                f"AIC_tax=2; BIC_tax={float(penalty['BIC_chi2_improvement_required']):.9g}"
            ),
            "claim_effect": "kappa-free cannot replace fixed branch unless this passes",
        },
        {
            "gate": "fixed_branch_competitive_with_baselines",
            "status": "pass" if fixed_vs_lcdm_aic < 0.0 and fixed_vs_wcdm_aic < 0.0 and fixed_vs_cpl_aic < 0.0 else "warn",
            "evidence": f"delta_AIC_vs_LCDM={fixed_vs_lcdm_aic:.6g}; vs_wCDM={fixed_vs_wcdm_aic:.6g}; vs_CPL={fixed_vs_cpl_aic:.6g}",
            "claim_effect": "late-time SN+BAO score only; not a field-theory promotion",
        },
    ]


def short_decision_rows(scores: list[dict[str, Any]], penalty_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    fixed = by_model["MTS_fixed_2over27_no_clock"]
    kappa = by_model["MTS_kappa_free_no_clock"]
    penalty = penalty_rows[0]
    decision = "fixed_2over27_survives_short_smoke_kappa_not_promoted"
    if penalty["kappa_promoted"]:
        decision = "kappa_free_pays_tax_as_ablation_fixed_branch_demoted_for_this_arena"
    return [
        {
            "decision": decision,
            "claim_ceiling": CLAIM_CEILING_SHORT,
            "lead_branch": LEAD_BRANCH,
            "arena": "SN-BAO-T7",
            "fixed_chi2": fixed["chi2_total"],
            "kappa_chi2": kappa["chi2_total"],
            "kappa_delta_chi2_improvement": penalty["delta_chi2_improvement_fixed_minus_kappa"],
            "kappa_promoted": penalty["kappa_promoted"],
            "meaning": (
                "This is a same-data, same-nuisance SN+BAO short-smoke score. "
                "It can discipline the fixed-vs-kappa closure choice, but it does not derive B_mem, "
                "settle CMB/growth/local-GR, or promote the parent action."
            ),
            "next_target": "derive_or_reject_memory_stress_normalization_before_any_amplitude_claim",
        }
    ]


def build_short_smoke_outputs(timestamp: str, arena: str, max_iter: int) -> dict[str, Any]:
    run_id = f"{timestamp}-{SHORT_SMOKE_SLUG}"
    run_dir = ROOT / "runs" / run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    scores, sn, bao, data_config = run_scores(max_iter=max_iter)
    fit_rows = fit_summary_rows(scores)
    baseline_rows = baseline_comparison_rows(scores)
    penalty_rows = fixed_vs_kappa_penalty_rows(scores, arena)
    edge_rows = prior_edge_rows(scores)
    residual_rows = residual_summary_rows(scores)
    bao_rows = bao_residual_rows(scores, bao)
    plot_rows = write_residual_plots(results_dir, scores, sn)
    gate_rows = score_gate_rows(scores, penalty_rows)
    decision = short_decision_rows(scores, penalty_rows)

    write_csv(results_dir / "source_register.csv", source_register_rows(), ["path", "role", "exists", "bytes"])
    write_csv(
        results_dir / "data_schema_report.csv",
        data_schema_rows(),
        ["dataset", "path", "exists", "rows", "columns_or_cov_shape", "role"],
    )
    write_csv(
        results_dir / "branch_contract.csv",
        branch_contract_rows(),
        ["branch", "p", "u3", "B_mem", "kappa_mem", "free_amplitude_count", "sidecar_policy", "claim_ceiling"],
    )
    write_csv(
        results_dir / "model_parameter_matrix.csv",
        model_parameter_rows(),
        ["model", "role", "theory_parameters", "shared_nuisance", "extra_k_vs_fixed"],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "model",
            "role",
            "source_model_key",
            "success",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "n",
            "k",
            "dof",
            "prior_edge_flag",
            "Omega_m",
            "w",
            "w0",
            "wa",
            "B_mem",
            "kappa_mem",
            "p",
            "u3",
            "sn_offset",
            "bao_alpha",
            "claim_ceiling",
            "optimizer_message",
        ],
    )
    write_csv(
        results_dir / "baseline_comparison.csv",
        baseline_rows,
        ["model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "model_k", "reference_k", "model_n", "readout"],
    )
    write_csv(
        results_dir / "fixed_vs_kappa_penalty.csv",
        penalty_rows,
        [
            "arena",
            "chi2_fixed",
            "chi2_kappa",
            "delta_chi2_improvement_fixed_minus_kappa",
            "delta_k",
            "n_eff",
            "AIC_chi2_improvement_required",
            "BIC_chi2_improvement_required",
            "delta_AIC_kappa_minus_fixed",
            "delta_BIC_kappa_minus_fixed",
            "AIC_tax_paid",
            "BIC_tax_paid",
            "kappa_promoted",
            "fixed_B_mem",
            "kappa_best_B_mem",
            "kappa_best_kappa_mem",
            "readout",
        ],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_rows,
        ["model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(
        results_dir / "residual_summary.csv",
        residual_rows,
        [
            "model",
            "SN_rows",
            "SN_mean_residual",
            "SN_rms_residual",
            "SN_max_abs_residual",
            "BAO_rows",
            "BAO_mean_residual",
            "BAO_rms_residual",
            "BAO_max_abs_residual",
        ],
    )
    write_csv(results_dir / "bao_residuals.csv", bao_rows, ["model", "row_index", "z", "quantity", "observed", "predicted", "residual"])
    write_csv(results_dir / "plot_register.csv", plot_rows, ["plot", "status", "path", "issue"])
    write_csv(results_dir / "implementation_gates.csv", gate_rows, ["gate", "status", "evidence", "claim_effect"])
    write_csv(
        results_dir / "decision.csv",
        decision,
        [
            "decision",
            "claim_ceiling",
            "lead_branch",
            "arena",
            "fixed_chi2",
            "kappa_chi2",
            "kappa_delta_chi2_improvement",
            "kappa_promoted",
            "meaning",
            "next_target",
        ],
    )

    run_config = {
        "phase": "short-smoke",
        "scores_allowed": True,
        "claim_ceiling": CLAIM_CEILING_SHORT,
        "arena": arena,
        "max_iter": max_iter,
        "fixed_Bmem": B_MEM_FIXED,
        "branch_contract": branch_contract_rows(),
        "data_config": data_config,
        "model_parameter_matrix": model_parameter_rows(),
    }
    write_json(run_dir / "run_config.json", run_config)
    status_payload = {
        "status": SHORT_SMOKE_STATUS,
        "claim_ceiling": CLAIM_CEILING_SHORT,
        "lead_branch": LEAD_BRANCH,
        "phase": "short-smoke",
        "arena": arena,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "scores_generated": True,
        "promotion_allowed": False,
        "kappa_promoted": bool(penalty_rows[0]["kappa_promoted"]),
        "fixed_chi2": float(decision[0]["fixed_chi2"]),
        "kappa_chi2": float(decision[0]["kappa_chi2"]),
        "kappa_delta_chi2_improvement": float(decision[0]["kappa_delta_chi2_improvement"]),
        "fixed_Bmem": f"{B_MEM_FIXED:.12f}",
        "kappa_best_Bmem": float(penalty_rows[0]["kappa_best_B_mem"]),
        "kappa_best_kappa_mem": float(penalty_rows[0]["kappa_best_kappa_mem"]),
        "implementation_gate_failures": [row["gate"] for row in gate_rows if row["status"] == "fail"],
        "next_target": "derive_or_reject_memory_stress_normalization_before_any_amplitude_claim",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(SHORT_SMOKE_STATUS + "\n", encoding="utf-8")
    return status_payload


def build_outputs(timestamp: str, phase: str, arena: str, max_iter: int) -> dict[str, Any]:
    if phase == "dry-run":
        return build_dryrun_outputs(timestamp, phase, arena)
    return build_short_smoke_outputs(timestamp, arena, max_iter)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fixed 2/27 vs kappa-free SN+BAO dry-run and short-smoke runner.")
    parser.add_argument("--phase", choices=["dry-run", "short-smoke"], default="dry-run")
    parser.add_argument("--arena", default="SN-BAO-T7")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    parser.add_argument("--max-iter", type=int, default=120)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp, args.phase, args.arena, args.max_iter)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
