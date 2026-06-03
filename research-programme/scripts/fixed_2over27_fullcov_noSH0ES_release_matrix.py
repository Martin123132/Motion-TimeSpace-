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


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT.parent / "formalization-workbench"
SCRIPTS_ROOT = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))
import cosmo_SN_BAO_closure_runner as closure_runner  # noqa: E402


RUN_SLUG = "fixed-2over27-fullcov-noSH0ES-release-matrix"
STATUS = "fixed_2over27_fullcov_noSH0ES_DR1_DR2_matrix_scored_no_parent_claim"
CLAIM_CEILING = "fixed_2over27_late_time_background_score_only_no_parent_CMB_or_local_GR_promotion"
LEAD_BRANCH = "MTS_fixed_2over27_no_clock"
KAPPA_BRANCH = "MTS_kappa_free_no_clock"
B_MEM_FIXED = 2.0 / 27.0

SN_PATH = WORKBENCH / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat"
SN_COV = WORKBENCH / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES_STAT+SYS.cov"
BAO_RELEASES = {
    "DESI_DR2_fullcov_noSH0ES": {
        "mean": WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": WORKBENCH / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt",
    },
    "DESI_DR1_fullcov_noSH0ES": {
        "mean": WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
        "cov": WORKBENCH / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt",
    },
}
CPL_WIDE_PRIORS = {"CPL.w0": (-4.0, 1.0), "CPL.wa": (-5.0, 5.0)}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "315-fullcov-noSH0ES-score-readout.md", "fitted-B full-cov no-SH0ES predecessor"),
        (ROOT / "316-FLRW-memory-projection-amplitude-contract.md", "FLRW memory projection amplitude contract"),
        (ROOT / "317-kappa-mem-Ward-scale-lock-attempt.md", "kappa Ward scale-lock no-go"),
        (ROOT / "258-fixed-vs-kappa-free-SN-BAO-short-smoke-implementation.md", "DR2 fixed-vs-kappa predecessor"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "shared SN+BAO likelihood functions"),
        (ROOT / "scripts" / "fixed_2over27_fullcov_noSH0ES_release_matrix.py", "this release matrix script"),
        (SN_PATH, "Pantheon+SH0ES SN source"),
        (SN_COV, "Pantheon+SH0ES full covariance"),
    ]
    for label, paths in BAO_RELEASES.items():
        sources.append((paths["mean"], f"{label} BAO mean"))
        sources.append((paths["cov"], f"{label} BAO covariance"))
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": yes_no(path.exists()),
            "bytes": path.stat().st_size if path.exists() else 0,
        }
        for path, role in sources
    ]


def load_release_data(label: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    paths = BAO_RELEASES[label]
    sn = closure_runner.read_sn_data(
        SN_PATH,
        max_rows=None,
        covariance_path=SN_COV,
        covariance_mode="full",
        observable="mb-corr",
        include_calibrators=False,
    )
    bao = closure_runner.read_bao_data(paths["mean"], paths["cov"])
    bao["label"] = label
    config = {
        "release_branch": label,
        "sn_data": str(SN_PATH),
        "sn_cov": str(SN_COV),
        "sn_covariance_mode": "full",
        "sn_observable": "mb-corr",
        "sn_include_calibrators": False,
        "sn_rows_used": int(len(sn["z"])),
        "bao_data": str(paths["mean"]),
        "bao_cov": str(paths["cov"]),
        "bao_label": label,
        "bao_rows_used": int(len(bao["rows"])),
        "n_eff": int(len(sn["z"]) + len(bao["rows"])),
    }
    return sn, bao, config


def score_fixed_bmem(sn: dict[str, Any], bao: dict[str, Any], max_iter: int) -> dict[str, Any]:
    bounds = [(0.05, 0.6)]

    def objective(vector: np.ndarray) -> float:
        try:
            params = {"Omega_m": float(vector[0]), "B_mem": B_MEM_FIXED, "p": 3.0, "u3": 0.25}
            chi2_sn, _, _, _ = closure_runner.sn_chi2("MTS_fixed_p3_u3quarter", params, sn)
            chi2_bao, _, _, _ = closure_runner.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([value], dtype=float) for value in [0.30, 0.24, 0.36, 0.45, 0.15, 0.52]]
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
    return {
        "model": LEAD_BRANCH,
        "source_model_key": "MTS_fixed_p3_u3quarter",
        "role": "strict_lead_closure",
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
        "prior_edge_flag": False,
        "claim_ceiling": "strict_empirical_closure_no_parent_amplitude",
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "sn_residual": sn_residual,
        "sn_predicted": sn_predicted,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "edge_rows": [
            {
                "model": LEAD_BRANCH,
                "parameter": "Omega_m",
                "best_fit": omega_m,
                "lower": 0.05,
                "upper": 0.6,
                "distance_to_edge": min(omega_m - 0.05, 0.6 - omega_m),
                "edge_flag": min(omega_m - 0.05, 0.6 - omega_m) < 0.0055,
            },
            {
                "model": LEAD_BRANCH,
                "parameter": "B_mem",
                "best_fit": B_MEM_FIXED,
                "lower": B_MEM_FIXED,
                "upper": B_MEM_FIXED,
                "distance_to_edge": "fixed",
                "edge_flag": False,
            },
        ],
    }


def alias_score(score: dict[str, Any], model: str, role: str, claim_ceiling: str) -> dict[str, Any]:
    score = dict(score)
    score["model"] = model
    score["role"] = role
    score["source_model_key"] = score.get("source_model_key", "MTS_fixed_p3_u3quarter")
    score["claim_ceiling"] = claim_ceiling
    score["edge_rows"] = [dict(row, model=model) for row in score.get("edge_rows", [])]
    return score


def score_release(label: str, max_iter: int) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    sn, bao, config = load_release_data(label)
    scores = [
        closure_runner.score_model("LCDM", sn, bao, max_iter=max_iter),
        closure_runner.score_model("wCDM", sn, bao, max_iter=max_iter),
        closure_runner.score_model("CPL", sn, bao, max_iter=max_iter, prior_config=CPL_WIDE_PRIORS),
        score_fixed_bmem(sn, bao, max_iter=max_iter),
        alias_score(
            closure_runner.score_model("MTS_fixed_p3_u3quarter", sn, bao, max_iter=max_iter),
            KAPPA_BRANCH,
            "amplitude_ablation",
            "kappa_free_ablation_no_parent_amplitude",
        ),
        closure_runner.score_model("MTS_Bmem_zero", sn, bao, max_iter=max_iter),
    ]
    for score in scores:
        score.setdefault("role", "baseline" if score["model"] in {"LCDM", "wCDM", "CPL"} else "control")
        score.setdefault("source_model_key", score["model"])
    return scores, sn, bao, config


def fit_summary_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        for score in scores:
            params = score["params"]
            rows.append(
                {
                    "release_branch": release,
                    "model": score["model"],
                    "role": score.get("role", ""),
                    "source_model_key": score.get("source_model_key", score["model"]),
                    "chi2_SN": score["chi2_SN"],
                    "chi2_BAO": score["chi2_BAO"],
                    "chi2_total": score["chi2_total"],
                    "AIC": score["AIC"],
                    "BIC": score["BIC"],
                    "n": score["n"],
                    "k": score["k"],
                    "dof": score["dof"],
                    "convergence": score["convergence"],
                    "prior_edge_flag": score["prior_edge_flag"],
                    "Omega_m": params.get("Omega_m", ""),
                    "w": params.get("w", ""),
                    "w0": params.get("w0", ""),
                    "wa": params.get("wa", ""),
                    "B_mem": params.get("B_mem", ""),
                    "kappa_mem": (params.get("B_mem", "") / B_MEM_FIXED) if isinstance(params.get("B_mem", ""), float) and B_MEM_FIXED else "",
                    "p": params.get("p", ""),
                    "u3": params.get("u3", ""),
                    "sn_offset": score["sn_offset"],
                    "bao_alpha": score["bao_alpha"],
                    "claim_ceiling": score["claim_ceiling"],
                    "optimizer_message": score["optimizer_message"],
                }
            )
    return rows


def baseline_comparison_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        by_model = {score["model"]: score for score in scores}
        for model in [LEAD_BRANCH, KAPPA_BRANCH, "MTS_Bmem_zero", "LCDM", "wCDM", "CPL"]:
            if model not in by_model:
                continue
            score = by_model[model]
            for reference in ["LCDM", "wCDM", "CPL", LEAD_BRANCH, KAPPA_BRANCH]:
                if reference not in by_model or reference == model:
                    continue
                base = by_model[reference]
                rows.append(
                    {
                        "release_branch": release,
                        "model": model,
                        "reference_baseline": reference,
                        "delta_chi2": score["chi2_total"] - base["chi2_total"],
                        "delta_AIC": score["AIC"] - base["AIC"],
                        "delta_BIC": score["BIC"] - base["BIC"],
                        "model_k": score["k"],
                        "reference_k": base["k"],
                        "same_data": True,
                        "same_nuisance": True,
                        "same_calibration": True,
                        "readout": comparison_readout(score["chi2_total"] - base["chi2_total"], score["AIC"] - base["AIC"], score["BIC"] - base["BIC"]),
                    }
                )
    return rows


def comparison_readout(delta_chi2: float, delta_aic: float, delta_bic: float) -> str:
    if delta_chi2 < 0 and delta_aic < 0 and delta_bic < 0:
        return "raw_AIC_BIC_win"
    if delta_chi2 < 0 and delta_aic < 0 and delta_bic > 0:
        return "raw_AIC_win_BIC_penalty_loss"
    if delta_chi2 > 0 and delta_aic < 0 and delta_bic < 0:
        return "penalty_adjusted_win_despite_raw_chi2_loss"
    if delta_aic < 0 or delta_bic < 0:
        return "mixed_information_criteria"
    return "not_preferred"


def fixed_vs_kappa_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        by_model = {score["model"]: score for score in scores}
        fixed = by_model[LEAD_BRANCH]
        kappa = by_model[KAPPA_BRANCH]
        improvement = fixed["chi2_total"] - kappa["chi2_total"]
        delta_aic = kappa["AIC"] - fixed["AIC"]
        delta_bic = kappa["BIC"] - fixed["BIC"]
        rows.append(
            {
                "release_branch": release,
                "fixed_chi2": fixed["chi2_total"],
                "kappa_chi2": kappa["chi2_total"],
                "delta_chi2_improvement_fixed_minus_kappa": improvement,
                "delta_AIC_kappa_minus_fixed": delta_aic,
                "delta_BIC_kappa_minus_fixed": delta_bic,
                "AIC_tax_paid": improvement > 2.0,
                "BIC_tax_paid": improvement > math.log(max(int(fixed["n"]), 2)),
                "kappa_promoted": delta_aic < 0.0 and delta_bic < 0.0,
                "fixed_B_mem": B_MEM_FIXED,
                "kappa_best_B_mem": kappa["params"].get("B_mem", ""),
                "kappa_best_kappa_mem": kappa["params"].get("B_mem", 0.0) / B_MEM_FIXED,
                "readout": "kappa_not_promoted" if not (delta_aic < 0.0 and delta_bic < 0.0) else "kappa_promoted_by_information_criteria",
            }
        )
    return rows


def prior_edge_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        for score in scores:
            for row in score.get("edge_rows", []):
                rows.append({"release_branch": release, **row})
    return rows


def residual_summary_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        for score in scores:
            sn_residual = np.asarray(score["sn_residual"], dtype=float)
            bao_residual = np.asarray(score["bao_residual"], dtype=float)
            rows.append(
                {
                    "release_branch": release,
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


def release_stability_rows(all_scores: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    dr2 = {score["model"]: score for score in all_scores["DESI_DR2_fullcov_noSH0ES"]}
    dr1 = {score["model"]: score for score in all_scores["DESI_DR1_fullcov_noSH0ES"]}
    rows = []
    for model in [LEAD_BRANCH, KAPPA_BRANCH, "LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
        for metric in ["chi2_total", "AIC", "BIC"]:
            value2 = float(dr2[model][metric])
            value1 = float(dr1[model][metric])
            rows.append(
                {
                    "model": model,
                    "metric": metric,
                    "DR2": value2,
                    "DR1": value1,
                    "DR1_minus_DR2": value1 - value2,
                    "relative_shift_vs_DR2": "" if value2 == 0.0 else (value1 - value2) / abs(value2),
                }
            )
    for model in [LEAD_BRANCH, KAPPA_BRANCH]:
        b2 = float(dr2[model]["params"].get("B_mem", 0.0))
        b1 = float(dr1[model]["params"].get("B_mem", 0.0))
        rows.append(
            {
                "model": model,
                "metric": "B_mem",
                "DR2": b2,
                "DR1": b1,
                "DR1_minus_DR2": b1 - b2,
                "relative_shift_vs_DR2": "" if b2 == 0.0 else (b1 - b2) / abs(b2),
            }
        )
    return rows


def score_gate_rows(all_scores: dict[str, list[dict[str, Any]]], comparisons: list[dict[str, Any]], kappa_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_register_rows())
    score_rows = fit_summary_rows(all_scores)
    converged = all(str(row["convergence"]) == "True" or row["convergence"] is True for row in score_rows)
    no_edges = all(str(row["edge_flag"]) == "False" or row["edge_flag"] is False for row in prior_edge_rows(all_scores))
    fixed_vs_lcdm = [row for row in comparisons if row["model"] == LEAD_BRANCH and row["reference_baseline"] == "LCDM"]
    fixed_vs_wcdm = [row for row in comparisons if row["model"] == LEAD_BRANCH and row["reference_baseline"] == "wCDM"]
    fixed_vs_cpl = [row for row in comparisons if row["model"] == LEAD_BRANCH and row["reference_baseline"] == "CPL"]
    kappa_not_promoted = all(str(row["kappa_promoted"]) == "False" or row["kappa_promoted"] is False for row in kappa_rows)
    gates = [
        ("source_paths_exist", sources_ok, "all release matrix source artifacts exist"),
        ("all_models_converged", converged, "all scored branches converged"),
        ("no_prior_edge_flags", no_edges, "no fitted parameter sits on a prior boundary; fixed B is marked fixed"),
        ("fixed_beats_LCDM_AIC_BIC_both_releases", all(float(row["delta_AIC"]) < 0 and float(row["delta_BIC"]) < 0 for row in fixed_vs_lcdm), "strict fixed branch beats LCDM by AIC/BIC in DR2 and DR1"),
        ("fixed_beats_wCDM_AIC_BIC_both_releases", all(float(row["delta_AIC"]) < 0 and float(row["delta_BIC"]) < 0 for row in fixed_vs_wcdm), "strict fixed branch beats wCDM by AIC/BIC in DR2 and DR1"),
        ("fixed_beats_CPL_AIC_BIC_both_releases", all(float(row["delta_AIC"]) < 0 and float(row["delta_BIC"]) < 0 for row in fixed_vs_cpl), "strict fixed branch beats CPL by AIC/BIC in DR2 and DR1"),
        ("kappa_free_not_promoted", kappa_not_promoted, "kappa-free fails information-criterion tax in both releases"),
        ("Bmem_parent_derived", False, "2/27 is fixed by closure/theorem target, not parent-derived"),
        ("stable_evidence_allowed", False, "short-smoke/release matrix is diagnostic, not stable evidence"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def svg_escape(value: Any) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_svg_plot(path: Path, title: str, x_label: str, y_label: str, series: list[dict[str, Any]], line_mode: bool) -> None:
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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(elements) + "\n", encoding="utf-8")


def plot_rows(result_dir: Path, all_scores: dict[str, list[dict[str, Any]]], release_data: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> list[dict[str, Any]]:
    rows = []
    for release, scores in all_scores.items():
        by_model = {score["model"]: score for score in scores}
        sn, bao = release_data[release]
        sn_path = result_dir / "plots" / f"{release}_SN_fixed_2over27_vs_LCDM.svg"
        write_svg_plot(
            sn_path,
            f"{release} SN residuals: fixed 2/27 vs LCDM",
            "z",
            "SN residual",
            [
                {"label": "LCDM", "x": sn["z"], "y": by_model["LCDM"]["sn_residual"], "color": "#7f7f7f"},
                {"label": LEAD_BRANCH, "x": sn["z"], "y": by_model[LEAD_BRANCH]["sn_residual"], "color": "#1f77b4"},
            ],
            line_mode=False,
        )
        bao_path = result_dir / "plots" / f"{release}_BAO_fixed_2over27_vs_baselines.svg"
        row_axis = np.arange(len(bao["rows"]))
        write_svg_plot(
            bao_path,
            f"{release} BAO residuals: fixed 2/27 vs baselines",
            "BAO row index",
            "BAO residual",
            [
                {"label": "LCDM", "x": row_axis, "y": by_model["LCDM"]["bao_residual"], "color": "#7f7f7f"},
                {"label": "wCDM", "x": row_axis, "y": by_model["wCDM"]["bao_residual"], "color": "#2ca02c"},
                {"label": "CPL", "x": row_axis, "y": by_model["CPL"]["bao_residual"], "color": "#d62728"},
                {"label": LEAD_BRANCH, "x": row_axis, "y": by_model[LEAD_BRANCH]["bao_residual"], "color": "#1f77b4"},
            ],
            line_mode=True,
        )
        rows.append({"release_branch": release, "dataset": "SN", "plot": relpath(sn_path), "status": "written_svg"})
        rows.append({"release_branch": release, "dataset": "BAO", "plot": relpath(bao_path), "status": "written_svg"})
    return rows


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fixed_all = all(row["status"] == "pass" for row in gates if row["gate"].startswith("fixed_beats"))
    kappa_not = next(row for row in gates if row["gate"] == "kappa_free_not_promoted")["status"] == "pass"
    if fixed_all and kappa_not:
        status = STATUS
        readout = "strict_fixed_2over27_survives_DR1_DR2_fullcov_noSH0ES_matrix"
    else:
        status = "fixed_2over27_fullcov_noSH0ES_release_matrix_mixed_or_failed"
        readout = "strict_fixed_2over27_needs_repair_or_demotion_for_this_matrix"
    return [
        {"key": "status", "value": status},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "readout", "value": readout},
        {"key": "stable_evidence_allowed", "value": "false"},
        {"key": "parent_amplitude_derived", "value": "false"},
        {"key": "next_action", "value": "extend_to_symmetric_jackknife_and_external_Hz_growth_holdouts_before_any_stronger_empirical_language"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=180)
    args = parser.parse_args()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    missing = [row["source"] for row in source_register_rows() if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing source artifacts: {missing}")

    all_scores: dict[str, list[dict[str, Any]]] = {}
    release_configs: list[dict[str, Any]] = []
    release_data: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for release in BAO_RELEASES:
        scores, sn, bao, config = score_release(release, args.max_iter)
        all_scores[release] = scores
        release_configs.append(config)
        release_data[release] = (sn, bao)

    fit_rows = fit_summary_rows(all_scores)
    comparison_rows = baseline_comparison_rows(all_scores)
    kappa_rows = fixed_vs_kappa_rows(all_scores)
    edge_rows = prior_edge_rows(all_scores)
    residual_rows = residual_summary_rows(all_scores)
    stability_rows = release_stability_rows(all_scores)
    gates = score_gate_rows(all_scores, comparison_rows, kappa_rows)
    plots = plot_rows(result_dir, all_scores, release_data)
    decisions = decision_rows(gates)

    write_csv(result_dir / "source_register.csv", source_register_rows(), ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "release_config.csv", release_configs, ["release_branch", "sn_data", "sn_cov", "sn_covariance_mode", "sn_observable", "sn_include_calibrators", "sn_rows_used", "bao_data", "bao_cov", "bao_label", "bao_rows_used", "n_eff"])
    write_csv(
        result_dir / "fit_summary.csv",
        fit_rows,
        ["release_branch", "model", "role", "source_model_key", "chi2_SN", "chi2_BAO", "chi2_total", "AIC", "BIC", "n", "k", "dof", "convergence", "prior_edge_flag", "Omega_m", "w", "w0", "wa", "B_mem", "kappa_mem", "p", "u3", "sn_offset", "bao_alpha", "claim_ceiling", "optimizer_message"],
    )
    write_csv(
        result_dir / "baseline_comparison.csv",
        comparison_rows,
        ["release_branch", "model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "model_k", "reference_k", "same_data", "same_nuisance", "same_calibration", "readout"],
    )
    write_csv(
        result_dir / "fixed_vs_kappa.csv",
        kappa_rows,
        ["release_branch", "fixed_chi2", "kappa_chi2", "delta_chi2_improvement_fixed_minus_kappa", "delta_AIC_kappa_minus_fixed", "delta_BIC_kappa_minus_fixed", "AIC_tax_paid", "BIC_tax_paid", "kappa_promoted", "fixed_B_mem", "kappa_best_B_mem", "kappa_best_kappa_mem", "readout"],
    )
    write_csv(result_dir / "prior_edge_table.csv", edge_rows, ["release_branch", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"])
    write_csv(result_dir / "residual_summary.csv", residual_rows, ["release_branch", "model", "SN_rows", "SN_mean_residual", "SN_rms_residual", "SN_max_abs_residual", "BAO_rows", "BAO_mean_residual", "BAO_rms_residual", "BAO_max_abs_residual"])
    write_csv(result_dir / "release_stability.csv", stability_rows, ["model", "metric", "DR2", "DR1", "DR1_minus_DR2", "relative_shift_vs_DR2"])
    write_csv(result_dir / "plot_manifest.csv", plots, ["release_branch", "dataset", "plot", "status"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": next(row["value"] for row in decisions if row["key"] == "status"),
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence_allowed": False,
        "parent_amplitude_derived": False,
        "release_branches": list(BAO_RELEASES),
        "max_iter": args.max_iter,
        "next_action": "symmetric jackknife/external holdouts before stronger empirical language",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(payload["status"] + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
