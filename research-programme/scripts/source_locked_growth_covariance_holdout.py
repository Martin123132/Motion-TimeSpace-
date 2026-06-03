#!/usr/bin/env python3
"""Source-lock SDSS/eBOSS growth covariances and run fair jackknife scoring."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import numpy as np
from scipy import linalg


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
SOURCE_INTAKE_ROOT = WORK_DIR / "source-intake" / "sdss_eboss_dr16"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
GROWTH_DATA_ROOT = FORMALIZATION_WORKBENCH / "data" / "cosmology" / "growth_CMB"
SDSS_ROOT = GROWTH_DATA_ROOT / "sdss_eboss_dr16"
SOURCE_MANIFEST = GROWTH_DATA_ROOT / "source_manifest.csv"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import growth_route_gate as growth  # noqa: E402


SOURCE_ID = "SDSS_eBOSS_DR16_BAO_RSD_consensus"
LOCKED_B_MEM = 2.0 / 27.0
PRIMARY_MODEL = "MTS_locked_2over27"
MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
CLAIM_CEILING = "source_locked_growth_covariance_holdout_no_perturbation_promotion"
FETCH_KINDS = {"metadata", "primary_growth", "robustness_growth"}
GROWTH_CACHE: dict[tuple[str, tuple[tuple[str, float], ...]], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}


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


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "MTS-source-lock-audit/1.0"})
    with urlopen(request, timeout=45) as response:
        return response.read()


def sdss_relative_path(local_path: str) -> Path:
    path = Path(local_path)
    parts = list(path.parts)
    try:
        index = next(i for i, part in enumerate(parts) if part.lower() == "sdss_eboss_dr16")
    except StopIteration as exc:
        raise ValueError(f"cannot find sdss_eboss_dr16 in {local_path}") from exc
    return Path(*parts[index + 1 :])


def load_fetch_manifest() -> list[dict[str, str]]:
    rows = read_csv_rows(SOURCE_MANIFEST)
    return [
        row
        for row in rows
        if row["source_id"] == SOURCE_ID
        and row["kind"] in FETCH_KINDS
        and row["remote_url"].startswith("https://svn.sdss.org/")
    ]


def fetch_and_lock(intake_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Path]]:
    intake_dir.mkdir(parents=True, exist_ok=True)
    fetched_paths: dict[str, Path] = {}
    lock_rows: list[dict[str, Any]] = []
    for row in load_fetch_manifest():
        relative = sdss_relative_path(row["local_path"])
        output_path = intake_dir / relative
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = fetch_bytes(row["remote_url"])
        output_path.write_bytes(payload)
        remote_hash = sha256_bytes(payload)
        local_path = Path(row["local_path"])
        local_hash = sha256_file(local_path) if local_path.exists() else ""
        expected_hash = row["sha256"]
        fetched_paths[str(relative).replace("\\", "/")] = output_path
        lock_rows.append(
            {
                "item_id": row["item_id"],
                "kind": row["kind"],
                "remote_url": row["remote_url"],
                "relative_path": str(relative).replace("\\", "/"),
                "fetched_path": str(output_path),
                "local_path": str(local_path),
                "fetched_bytes": len(payload),
                "manifest_bytes": row["byte_size"],
                "fetched_sha256": remote_hash,
                "manifest_sha256": expected_hash,
                "local_sha256": local_hash,
                "hash_matches_manifest": remote_hash == expected_hash,
                "hash_matches_local": remote_hash == local_hash,
                "status": "pass" if remote_hash == expected_hash and remote_hash == local_hash else "fail",
            }
        )
    return lock_rows, fetched_paths


def fetched_pair(pair: dict[str, Any], fetched_paths: dict[str, Path]) -> dict[str, Any]:
    vector_relative = sdss_relative_path(str(pair["vector_file"]))
    cov_relative = sdss_relative_path(str(pair["covariance_file"]))
    return {
        "sample": pair["sample"],
        "vector_file": fetched_paths[str(vector_relative).replace("\\", "/")],
        "covariance_file": fetched_paths[str(cov_relative).replace("\\", "/")],
    }


def fetched_primary_pairs(fetched_paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [fetched_pair(pair, fetched_paths) for pair in growth.PRIMARY_BAO_PLUS_FILES]


def fetched_full_shape_pairs(fetched_paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [fetched_pair(pair, fetched_paths) for pair in growth.ROBUSTNESS_FULL_SHAPE_FILES]


def growth_cache_key(model_key: str, params: dict[str, float]) -> tuple[str, tuple[tuple[str, float], ...]]:
    return model_key, tuple(sorted((key, float(value)) for key, value in params.items()))


def cached_growth_solution(model_key: str, params: dict[str, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    key = growth_cache_key(model_key, params)
    if key not in GROWTH_CACHE:
        GROWTH_CACHE[key] = growth.growth_solution(model_key, params)
    return GROWTH_CACHE[key]


def growth_unit_values(model_key: str, params: dict[str, float], z_values: np.ndarray) -> np.ndarray:
    x_grid, d_grid, f_grid = cached_growth_solution(model_key, params)
    x_values = np.log(1.0 / (1.0 + z_values))
    d_values = np.interp(x_values, x_grid, d_grid)
    f_values = np.interp(x_values, x_grid, f_grid)
    return d_values * f_values


def fast_prediction_components(
    model_key: str,
    params: dict[str, float],
    rows: list[tuple[float, float, str]],
) -> tuple[np.ndarray, np.ndarray]:
    z_values = np.asarray([row[0] for row in rows], dtype=float)
    integral = growth.snbao.comoving_integral(model_key, z_values, params)
    e_values = growth.snbao.e_z(model_key, z_values, params)
    alpha = float(params["BAO_alpha"])
    growth_unit = growth_unit_values(model_key, params, z_values)
    base: list[float] = []
    unit: list[float] = []
    for index, (z_value, _, quantity) in enumerate(rows):
        if quantity in {"DM_over_rs", "DM_over_rd"}:
            base.append(float(alpha * integral[index]))
            unit.append(0.0)
        elif quantity in {"DH_over_rs", "DH_over_rd"}:
            base.append(float(alpha / e_values[index]))
            unit.append(0.0)
        elif quantity in {"DV_over_rs", "DV_over_rd"}:
            base.append(float(alpha * (z_value * integral[index] * integral[index] / e_values[index]) ** (1.0 / 3.0)))
            unit.append(0.0)
        elif quantity == "f_sigma8":
            base.append(0.0)
            unit.append(float(growth_unit[index]))
        else:
            raise ValueError(f"unsupported quantity {quantity}")
    return np.asarray(base, dtype=float), np.asarray(unit, dtype=float)


def branch_definitions(fetched_paths: dict[str, Path]) -> list[dict[str, Any]]:
    primary = fetched_primary_pairs(fetched_paths)
    full_shape = fetched_full_shape_pairs(fetched_paths)
    branches = [
        {
            "branch_label": "primary_BAO_plus_all_samples",
            "file_set": "primary_BAO_plus",
            "score_role": "primary_fit",
            "files": primary,
            "included_samples": ",".join(pair["sample"] for pair in primary),
            "excluded_sample": "",
            "production_branch": True,
        },
        {
            "branch_label": "full_shape_only_all_samples",
            "file_set": "full_shape_only",
            "score_role": "alternative_full_shape_fit",
            "files": full_shape,
            "included_samples": ",".join(pair["sample"] for pair in full_shape),
            "excluded_sample": "",
            "production_branch": False,
        },
    ]
    for pair in primary:
        kept = [candidate for candidate in primary if candidate["sample"] != pair["sample"]]
        branches.append(
            {
                "branch_label": f"primary_BAO_plus_drop_{pair['sample']}",
                "file_set": "primary_BAO_plus",
                "score_role": "primary_jackknife",
                "files": kept,
                "included_samples": ",".join(candidate["sample"] for candidate in kept),
                "excluded_sample": pair["sample"],
                "production_branch": True,
            }
        )
    for pair in full_shape:
        kept = [candidate for candidate in full_shape if candidate["sample"] != pair["sample"]]
        branches.append(
            {
                "branch_label": f"full_shape_only_drop_{pair['sample']}",
                "file_set": "full_shape_only",
                "score_role": "full_shape_jackknife",
                "files": kept,
                "included_samples": ",".join(candidate["sample"] for candidate in kept),
                "excluded_sample": pair["sample"],
                "production_branch": False,
            }
        )
    return branches


def selected_observed_base_unit(
    model_key: str,
    params: dict[str, float],
    pair: dict[str, Any],
    score_mode: str,
) -> tuple[list[tuple[float, float, str]], np.ndarray, np.ndarray, np.ndarray, list[int]]:
    all_rows = growth.numeric_rows(Path(pair["vector_file"]))
    all_cov = growth.read_covariance(Path(pair["covariance_file"]))
    rows, covariance, indices = growth.selected_rows_and_covariance(all_rows, all_cov, score_mode)
    observed = np.asarray([row[1] for row in rows], dtype=float)
    base, unit = fast_prediction_components(model_key, params, rows)
    return rows, covariance, observed, base, unit, indices


def fit_sigma8_analytic(
    model_key: str,
    params: dict[str, float],
    files: list[dict[str, Any]],
    score_mode: str,
) -> tuple[float, float, bool]:
    numerator = 0.0
    denominator = 0.0
    for pair in files:
        _, covariance, observed, base, unit, _ = selected_observed_base_unit(model_key, params, pair, score_mode)
        cho = linalg.cho_factor(covariance, lower=True, check_finite=False)
        inv_residual = linalg.cho_solve(cho, observed - base, check_finite=False)
        inv_unit = linalg.cho_solve(cho, unit, check_finite=False)
        numerator += float(unit @ inv_residual)
        denominator += float(unit @ inv_unit)
    sigma8 = numerator / denominator if denominator > 0.0 else 0.8
    sigma8 = min(max(sigma8, 0.2), 1.4)
    chi2_value, _ = score_files(model_key, params, files, score_mode, sigma8, [], {})
    distance_to_edge = min(sigma8 - 0.2, 1.4 - sigma8)
    return sigma8, chi2_value, distance_to_edge <= 0.012


def score_files(
    model_key: str,
    params: dict[str, float],
    files: list[dict[str, Any]],
    score_mode: str,
    sigma8: float,
    residual_rows: list[dict[str, Any]],
    context: dict[str, Any],
) -> tuple[float, int]:
    total = 0.0
    n_rows = 0
    for pair_index, pair in enumerate(files, start=1):
        rows, covariance, observed, base, unit, indices = selected_observed_base_unit(model_key, params, pair, score_mode)
        predicted = base + sigma8 * unit
        residual = observed - predicted
        chi2_value = growth.covariance_chi2(residual, covariance)
        total += chi2_value
        n_rows += len(rows)
        diag_sigma = np.sqrt(np.diag(covariance))
        inv_cov = linalg.inv(covariance)
        signed = residual * (inv_cov @ residual)
        for local_index, ((z_value, obs, quantity), pred, res, sigma, signed_value) in enumerate(
            zip(rows, predicted, residual, diag_sigma, signed, strict=True),
            start=1,
        ):
            if context:
                residual_rows.append(
                    {
                        **context,
                        "sample": pair["sample"],
                        "pair_index": pair_index,
                        "row_index": local_index,
                        "source_row_index_0based": indices[local_index - 1],
                        "z": z_value,
                        "quantity": quantity,
                        "observed": obs,
                        "predicted": float(pred),
                        "residual": float(res),
                        "diagonal_sigma": float(sigma),
                        "diagonal_pull": float(res / sigma) if sigma > 0.0 else "",
                        "cov_signed_chi2_contribution": float(signed_value),
                        "sigma8_0": sigma8,
                    }
                )
    return total, n_rows


def schema_rows(branches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique_pairs: dict[str, dict[str, Any]] = {}
    for branch in branches:
        for pair in branch["files"]:
            unique_pairs[str(pair["vector_file"])] = pair
    rows = []
    for pair in sorted(unique_pairs.values(), key=lambda item: (str(item["vector_file"]), item["sample"])):
        vector_rows = growth.numeric_rows(Path(pair["vector_file"]))
        covariance = growth.read_covariance(Path(pair["covariance_file"]))
        eigenvalues = np.linalg.eigvalsh(covariance)
        rows.append(
            {
                "sample": pair["sample"],
                "vector_file": str(pair["vector_file"]),
                "covariance_file": str(pair["covariance_file"]),
                "rows": len(vector_rows),
                "quantity_counts": json.dumps(dict(sorted(__import__("collections").Counter(row[2] for row in vector_rows).items())), sort_keys=True),
                "covariance_shape": f"{covariance.shape[0]}x{covariance.shape[1]}",
                "min_covariance_eigenvalue": float(np.min(eigenvalues)),
                "covariance_condition": float(np.max(eigenvalues) / np.min(eigenvalues)),
                "schema_status": "pass" if covariance.shape == (len(vector_rows), len(vector_rows)) and np.min(eigenvalues) > 0 else "fail",
            }
        )
    return rows


def branch_manifest_rows(branches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "branch_label": branch["branch_label"],
            "file_set": branch["file_set"],
            "score_role": branch["score_role"],
            "included_samples": branch["included_samples"],
            "excluded_sample": branch["excluded_sample"],
            "production_branch": branch["production_branch"],
            "sample_count": len(branch["files"]),
        }
        for branch in branches
    ]


def run_fits(branches: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    specs = growth.load_background_specs()
    fit_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for spec in specs:
        for branch in branches:
            for score_mode in ["all", "fs8_only"]:
                for model in MODEL_ORDER:
                    if model != spec["model"]:
                        continue
                    sigma8, objective_chi2, edge_flag = fit_sigma8_analytic(
                        spec["model_key"], spec["params"], branch["files"], score_mode
                    )
                    context = {
                        "background_branch": spec["background_branch"],
                        "source_dataset_label": spec["source_dataset_label"],
                        "branch_label": branch["branch_label"],
                        "file_set": branch["file_set"],
                        "score_role": branch["score_role"],
                        "score_mode": score_mode,
                        "model": model,
                    }
                    score_chi2, n_data = score_files(
                        spec["model_key"],
                        spec["params"],
                        branch["files"],
                        score_mode,
                        sigma8,
                        residual_rows,
                        context,
                    )
                    k_count = 1
                    fit_rows.append(
                        {
                            "background_branch": spec["background_branch"],
                            "source_dataset_label": spec["source_dataset_label"],
                            "branch_label": branch["branch_label"],
                            "file_set": branch["file_set"],
                            "score_role": branch["score_role"],
                            "score_mode": score_mode,
                            "model": model,
                            "included_samples": branch["included_samples"],
                            "excluded_sample": branch["excluded_sample"],
                            "production_branch": branch["production_branch"],
                            "chi2": score_chi2,
                            "fit_objective_chi2": objective_chi2,
                            "n_data": n_data,
                            "dynamic_k": k_count,
                            "AIC": score_chi2 + 2.0 * k_count,
                            "BIC": score_chi2 + math.log(n_data) * k_count,
                            "sigma8_0": sigma8,
                            "sigma8_edge_flag": edge_flag,
                            "Omega_m0": spec["Omega_m0"],
                            "h": spec["h"],
                            "H0": spec["H0"],
                            "BAO_alpha": spec["BAO_alpha"],
                            "rd_inferred_from_alpha_h": spec["rd_inferred_from_alpha_h"],
                            "source_edge_flag": spec["source_edge_flag"],
                            "claim_ceiling": CLAIM_CEILING,
                        }
                    )
    return fit_rows, residual_rows


def comparison_label(delta: float) -> str:
    if delta <= -2.0:
        return "locked_preferred"
    if delta < 2.0:
        return "competitive_draw"
    return "locked_disfavored"


def baseline_comparison_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {
        (row["background_branch"], row["branch_label"], row["score_mode"], row["model"]): row
        for row in fit_rows
    }
    score_keys = sorted({(row["background_branch"], row["branch_label"], row["score_mode"]) for row in fit_rows})
    for background_branch, branch_label, score_mode in score_keys:
        locked = by_key[(background_branch, branch_label, score_mode, PRIMARY_MODEL)]
        for reference_model in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_key[(background_branch, branch_label, score_mode, reference_model)]
            delta_chi2 = float(locked["chi2"]) - float(reference["chi2"])
            rows.append(
                {
                    "background_branch": background_branch,
                    "branch_label": branch_label,
                    "file_set": locked["file_set"],
                    "score_role": locked["score_role"],
                    "score_mode": score_mode,
                    "model": PRIMARY_MODEL,
                    "reference_model": reference_model,
                    "delta_chi2": delta_chi2,
                    "delta_AIC": float(locked["AIC"]) - float(reference["AIC"]),
                    "delta_BIC": float(locked["BIC"]) - float(reference["BIC"]),
                    "locked_sigma8_edge": locked["sigma8_edge_flag"],
                    "reference_sigma8_edge": reference["sigma8_edge_flag"],
                    "reference_background_edge": reference["source_edge_flag"],
                    "readout": comparison_label(delta_chi2),
                }
            )
    return rows


def control_rows(fit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {
        (row["background_branch"], row["branch_label"], row["score_mode"], row["model"]): row
        for row in fit_rows
    }
    score_keys = sorted({(row["background_branch"], row["branch_label"], row["score_mode"]) for row in fit_rows})
    for background_branch, branch_label, score_mode in score_keys:
        lcdm = by_key[(background_branch, branch_label, score_mode, "LCDM")]
        zero = by_key[(background_branch, branch_label, score_mode, "MTS_Bmem_zero")]
        delta = float(zero["chi2"]) - float(lcdm["chi2"])
        rows.append(
            {
                "background_branch": background_branch,
                "branch_label": branch_label,
                "score_mode": score_mode,
                "control": "MTS_Bmem_zero_vs_LCDM",
                "delta_chi2": delta,
                "delta_sigma8_0": float(zero["sigma8_0"]) - float(lcdm["sigma8_0"]),
                "status": "pass" if abs(delta) < 1.0e-8 else "check",
            }
        )
    return rows


def jackknife_scorecard_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for background_branch in sorted({row["background_branch"] for row in comparisons}):
        for file_set in ["primary_BAO_plus", "full_shape_only"]:
            for score_mode in ["all", "fs8_only"]:
                selected = [
                    row
                    for row in comparisons
                    if row["background_branch"] == background_branch
                    and row["file_set"] == file_set
                    and row["score_mode"] == score_mode
                    and row["reference_model"] == "LCDM"
                    and "drop_" in row["branch_label"]
                ]
                if not selected:
                    continue
                deltas = np.asarray([float(row["delta_chi2"]) for row in selected], dtype=float)
                rows.append(
                    {
                        "background_branch": background_branch,
                        "file_set": file_set,
                        "score_mode": score_mode,
                        "jackknife_count": len(selected),
                        "preferred_count": int(np.sum(deltas <= -2.0)),
                        "draw_count": int(np.sum((deltas > -2.0) & (deltas < 2.0))),
                        "disfavored_count": int(np.sum(deltas >= 2.0)),
                        "min_delta_chi2": float(np.min(deltas)),
                        "max_delta_chi2": float(np.max(deltas)),
                        "mean_delta_chi2": float(np.mean(deltas)),
                        "status": "pass_no_disfavored_jackknife" if np.max(deltas) < 2.0 else "fail_has_disfavored_jackknife",
                    }
                )
    return rows


def source_register_rows(script_path: Path, intake_dir: Path, run_dir: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "growth_route_gate.py",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        SOURCE_MANIFEST,
        SDSS_ROOT / "row_lock_manifest.json",
        SDSS_ROOT / "covariance_validation.csv",
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        RUNS_ROOT / "20260531-183400-growth-route-gate" / "status.json",
        RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout" / "status.json",
        intake_dir,
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def decision_rows(
    lock_rows: list[dict[str, Any]],
    fit_rows: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    jackknife_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    def lcdm_delta(branch_label: str, score_mode: str) -> float:
        return float(
            next(
                row["delta_chi2"]
                for row in comparisons
                if row["background_branch"] == "DR2_noCMB_primary"
                and row["branch_label"] == branch_label
                and row["score_mode"] == score_mode
                and row["reference_model"] == "LCDM"
            )
        )

    primary_all_delta = lcdm_delta("primary_BAO_plus_all_samples", "all")
    primary_rsd_delta = lcdm_delta("primary_BAO_plus_all_samples", "fs8_only")
    full_shape_all_delta = lcdm_delta("full_shape_only_all_samples", "all")
    full_shape_rsd_delta = lcdm_delta("full_shape_only_all_samples", "fs8_only")
    source_failures = [row for row in lock_rows if row["status"] != "pass"]
    bad_controls = [row for row in controls if row["status"] != "pass"]
    locked_edges = [row for row in fit_rows if row["model"] == PRIMARY_MODEL and row["sigma8_edge_flag"] in [True, "True"]]
    jackknife_failures = [row for row in jackknife_rows if row["status"].startswith("fail")]

    if source_failures:
        status = "growth_covariance_source_lock_failure"
    elif bad_controls:
        status = "growth_covariance_control_failure"
    elif locked_edges:
        status = "growth_covariance_locked_sigma8_edge"
    elif primary_all_delta > 2.0 or primary_rsd_delta > 2.0:
        status = "growth_covariance_primary_tension_vs_LCDM"
    elif jackknife_failures:
        status = "growth_covariance_jackknife_mixed_or_fragile"
    elif full_shape_all_delta > 2.0 or full_shape_rsd_delta > 2.0:
        status = "growth_covariance_full_shape_tension_vs_LCDM"
    elif primary_all_delta <= -2.0 and primary_rsd_delta < 2.0:
        status = "growth_covariance_source_locked_primary_preferred_or_draw"
    else:
        status = "growth_covariance_source_locked_competitive_draw"

    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary_all_delta={primary_all_delta:.12g}; primary_RSD_delta={primary_rsd_delta:.12g}; full_shape_all_delta={full_shape_all_delta:.12g}; jackknife_failures={len(jackknife_failures)}",
        },
        {
            "item": "source_lock",
            "verdict": "pass" if not source_failures else "fail",
            "evidence": f"fetched_files={len(lock_rows)}; failures={len(source_failures)}",
        },
        {
            "item": "primary_BAO_plus_all_vs_LCDM",
            "verdict": comparison_label(primary_all_delta),
            "evidence": f"delta_chi2={primary_all_delta:.12g}; covariance all rows",
        },
        {
            "item": "primary_RSD_only_vs_LCDM",
            "verdict": comparison_label(primary_rsd_delta),
            "evidence": f"delta_chi2={primary_rsd_delta:.12g}; f_sigma8 rows only",
        },
        {
            "item": "full_shape_all_vs_LCDM",
            "verdict": comparison_label(full_shape_all_delta),
            "evidence": f"delta_chi2={full_shape_all_delta:.12g}; alternative compression, not combined",
        },
        {
            "item": "full_shape_RSD_only_vs_LCDM",
            "verdict": comparison_label(full_shape_rsd_delta),
            "evidence": f"delta_chi2={full_shape_rsd_delta:.12g}; alternative compression, not combined",
        },
        {
            "item": "jackknife_stability_vs_LCDM",
            "verdict": "pass" if not jackknife_failures else "mixed",
            "evidence": f"jackknife_groups={len(jackknife_rows)}; failing_groups={len(jackknife_failures)}",
        },
        {
            "item": "negative_control",
            "verdict": "pass" if not bad_controls else "check",
            "evidence": "MTS_Bmem_zero reproduces LCDM in every branch" if not bad_controls else f"{len(bad_controls)} control rows failed",
        },
        {
            "item": "claim_status",
            "verdict": "conditional_growth_covariance_holdout_only",
            "evidence": "GR-proxy growth with shared sigma8_0; no MTS perturbation derivation, CMB claim, or local-GR theorem.",
        },
        {
            "item": "next_target",
            "verdict": "official_likelihood_reimplementation_or_ELG_grid_parser",
            "evidence": "Gaussian SDSS/eBOSS covariance branch is source-locked; ELG grid and official likelihood stack remain parser/likelihood work.",
        },
    ]


def gate_rows(
    lock_rows: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    jackknife_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    status = next(row["verdict"] for row in decisions if row["item"] == "status")
    primary_all = next(row["evidence"] for row in decisions if row["item"] == "primary_BAO_plus_all_vs_LCDM")
    primary_rsd = next(row["evidence"] for row in decisions if row["item"] == "primary_RSD_only_vs_LCDM")
    return [
        {
            "gate": "source_fetch_hash_lock",
            "status": "pass" if all(row["status"] == "pass" for row in lock_rows) else "fail",
            "evidence": f"files={len(lock_rows)}",
        },
        {
            "gate": "covariance_schema",
            "status": "pass" if all(row["schema_status"] == "pass" for row in schema) else "fail",
            "evidence": f"unique vector/covariance pairs={len(schema)}",
        },
        {
            "gate": "frozen_B_mem_no_refit",
            "status": "pass",
            "evidence": f"B_mem={LOCKED_B_MEM}; only sigma8_0 profiled for every model",
        },
        {
            "gate": "same_test_retest_baselines",
            "status": "pass",
            "evidence": "LCDM, wCDM, CPL, locked MTS, and Bmem-zero control scored on every branch",
        },
        {
            "gate": "primary_growth_not_disfavored",
            "status": "pass" if "locked_disfavored" not in status and "tension" not in status else "fail",
            "evidence": f"{primary_all}; {primary_rsd}",
        },
        {
            "gate": "jackknife_no_hard_loss",
            "status": "pass" if all(row["status"] == "pass_no_disfavored_jackknife" for row in jackknife_rows) else "fail",
            "evidence": f"jackknife_groups={len(jackknife_rows)}",
        },
        {
            "gate": "do_not_combine_alternative_compressions",
            "status": "pass",
            "evidence": "BAO-plus and full-shape-only are scored separately",
        },
        {
            "gate": "theory_promotion",
            "status": "fail",
            "evidence": "growth covariance stress cannot derive perturbation action/local GR/CMB",
        },
    ]


def run_holdout(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-source-locked-growth-covariance-holdout"
    results_dir = run_dir / "results"
    intake_dir = SOURCE_INTAKE_ROOT / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)

    lock_rows, fetched_paths = fetch_and_lock(intake_dir)
    branches = branch_definitions(fetched_paths)
    schema = schema_rows(branches)
    fit_rows, residual_rows = run_fits(branches)
    comparisons = baseline_comparison_rows(fit_rows)
    controls = control_rows(fit_rows)
    jackknife_rows = jackknife_scorecard_rows(comparisons)
    decisions = decision_rows(lock_rows, fit_rows, comparisons, controls, jackknife_rows)
    gates = gate_rows(lock_rows, schema, controls, decisions, jackknife_rows)
    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")

    source_rows = source_register_rows(Path(__file__).resolve(), intake_dir, run_dir)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "fetch_hash_lock.csv",
        lock_rows,
        [
            "item_id",
            "kind",
            "remote_url",
            "relative_path",
            "fetched_path",
            "local_path",
            "fetched_bytes",
            "manifest_bytes",
            "fetched_sha256",
            "manifest_sha256",
            "local_sha256",
            "hash_matches_manifest",
            "hash_matches_local",
            "status",
        ],
    )
    write_csv(
        results_dir / "data_schema.csv",
        schema,
        [
            "sample",
            "vector_file",
            "covariance_file",
            "rows",
            "quantity_counts",
            "covariance_shape",
            "min_covariance_eigenvalue",
            "covariance_condition",
            "schema_status",
        ],
    )
    write_csv(
        results_dir / "branch_manifest.csv",
        branch_manifest_rows(branches),
        ["branch_label", "file_set", "score_role", "included_samples", "excluded_sample", "production_branch", "sample_count"],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "background_branch",
            "source_dataset_label",
            "branch_label",
            "file_set",
            "score_role",
            "score_mode",
            "model",
            "included_samples",
            "excluded_sample",
            "production_branch",
            "chi2",
            "fit_objective_chi2",
            "n_data",
            "dynamic_k",
            "AIC",
            "BIC",
            "sigma8_0",
            "sigma8_edge_flag",
            "Omega_m0",
            "h",
            "H0",
            "BAO_alpha",
            "rd_inferred_from_alpha_h",
            "source_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "background_branch",
            "branch_label",
            "file_set",
            "score_role",
            "score_mode",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_sigma8_edge",
            "reference_sigma8_edge",
            "reference_background_edge",
            "readout",
        ],
    )
    write_csv(
        results_dir / "control_reproduction.csv",
        controls,
        ["background_branch", "branch_label", "score_mode", "control", "delta_chi2", "delta_sigma8_0", "status"],
    )
    write_csv(
        results_dir / "jackknife_scorecard.csv",
        jackknife_rows,
        [
            "background_branch",
            "file_set",
            "score_mode",
            "jackknife_count",
            "preferred_count",
            "draw_count",
            "disfavored_count",
            "min_delta_chi2",
            "max_delta_chi2",
            "mean_delta_chi2",
            "status",
        ],
    )
    write_csv(
        results_dir / "residuals.csv",
        residual_rows,
        [
            "background_branch",
            "source_dataset_label",
            "branch_label",
            "file_set",
            "score_role",
            "score_mode",
            "model",
            "sample",
            "pair_index",
            "row_index",
            "source_row_index_0based",
            "z",
            "quantity",
            "observed",
            "predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
            "sigma8_0",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_intake_dir": str(intake_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_B_mem": LOCKED_B_MEM,
        "models": MODEL_ORDER,
        "branches": len(branches),
        "fit_rows": len(fit_rows),
        "generated": [
            "source_register.csv",
            "fetch_hash_lock.csv",
            "data_schema.csv",
            "branch_manifest.csv",
            "fit_summary.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "jackknife_scorecard.csv",
            "residuals.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "official_likelihood_reimplementation_or_ELG_grid_parser",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_holdout(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
