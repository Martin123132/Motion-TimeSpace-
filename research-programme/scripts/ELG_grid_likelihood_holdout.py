#!/usr/bin/env python3
"""Parse the eBOSS DR16 ELG non-Gaussian grid likelihood and score MTS fairly."""

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
from scipy import interpolate, optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
SOURCE_INTAKE_ROOT = WORK_DIR / "source-intake" / "sdss_eboss_dr16_elg_grid"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
GROWTH_DATA_ROOT = FORMALIZATION_WORKBENCH / "data" / "cosmology" / "growth_CMB"
SDSS_ROOT = GROWTH_DATA_ROOT / "sdss_eboss_dr16"
SOURCE_MANIFEST = GROWTH_DATA_ROOT / "source_manifest.csv"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import growth_route_gate as growth  # noqa: E402
import source_locked_growth_covariance_holdout as gaussian_holdout  # noqa: E402


SOURCE_ID = "SDSS_eBOSS_DR16_BAO_RSD_consensus"
ELG_ITEM_ID = "sdss_DR16_ELG_FSBAO_DMDHfs8gridlikelihood.txt"
BAO_PLUS_README_ID = "README.txt"
ELG_Z_EFF = 0.85
LOCKED_B_MEM = 2.0 / 27.0
PRIMARY_MODEL = "MTS_locked_2over27"
MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
CLAIM_CEILING = "ELG_grid_likelihood_holdout_no_perturbation_or_CMB_promotion"
LOG_FLOOR_PROBABILITY = 1.0e-300
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


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "MTS-ELG-grid-audit/1.0"})
    with urlopen(request, timeout=90) as response:
        return response.read()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows_for_items() -> list[dict[str, str]]:
    rows = read_csv_rows(SOURCE_MANIFEST)
    wanted = []
    for row in rows:
        if row["source_id"] != SOURCE_ID:
            continue
        if row["item_id"] == ELG_ITEM_ID or (
            row["item_id"] == BAO_PLUS_README_ID and "BAO-plus" in row["local_path"]
        ):
            wanted.append(row)
    if len(wanted) != 2:
        raise ValueError(f"expected ELG grid and BAO-plus README manifest rows, got {len(wanted)}")
    return wanted


def sdss_relative_path(local_path: str) -> Path:
    path = Path(local_path)
    parts = list(path.parts)
    index = next(i for i, part in enumerate(parts) if part.lower() == "sdss_eboss_dr16")
    return Path(*parts[index + 1 :])


def fetch_and_lock(intake_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Path]]:
    intake_dir.mkdir(parents=True, exist_ok=True)
    fetched: dict[str, Path] = {}
    lock_rows = []
    for row in source_rows_for_items():
        relative = sdss_relative_path(row["local_path"])
        output_path = intake_dir / relative
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = fetch_bytes(row["remote_url"])
        output_path.write_bytes(payload)
        fetched_hash = sha256_bytes(payload)
        local_path = Path(row["local_path"])
        local_hash = sha256_file(local_path) if local_path.exists() else ""
        status = "pass" if fetched_hash == row["sha256"] and fetched_hash == local_hash else "fail"
        fetched[str(relative).replace("\\", "/")] = output_path
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
                "fetched_sha256": fetched_hash,
                "manifest_sha256": row["sha256"],
                "local_sha256": local_hash,
                "hash_matches_manifest": fetched_hash == row["sha256"],
                "hash_matches_local": fetched_hash == local_hash,
                "status": status,
            }
        )
    return lock_rows, fetched


def load_grid(path: Path) -> tuple[dict[str, Any], interpolate.RegularGridInterpolator]:
    array = np.loadtxt(path)
    if array.ndim != 2 or array.shape[1] != 4:
        raise ValueError(f"ELG grid must have 4 columns, got shape {array.shape}")
    dm_values = np.unique(array[:, 0])
    dh_values = np.unique(array[:, 1])
    fs8_values = np.unique(array[:, 2])
    expected = len(dm_values) * len(dh_values) * len(fs8_values)
    if expected != array.shape[0]:
        raise ValueError(f"grid is not rectangular: expected {expected}, got {array.shape[0]}")
    probabilities = array[:, 3].reshape((len(dm_values), len(dh_values), len(fs8_values)))
    clipped = np.clip(probabilities, LOG_FLOOR_PROBABILITY, None)
    log_prob = np.log(clipped)
    interpolator = interpolate.RegularGridInterpolator(
        (dm_values, dh_values, fs8_values),
        log_prob,
        bounds_error=False,
        fill_value=math.log(LOG_FLOOR_PROBABILITY),
    )
    max_index = np.unravel_index(int(np.argmax(probabilities)), probabilities.shape)
    schema = {
        "grid_path": str(path),
        "rows": int(array.shape[0]),
        "columns": int(array.shape[1]),
        "dm_unique": int(len(dm_values)),
        "dh_unique": int(len(dh_values)),
        "fs8_unique": int(len(fs8_values)),
        "dm_min": float(dm_values.min()),
        "dm_max": float(dm_values.max()),
        "dh_min": float(dh_values.min()),
        "dh_max": float(dh_values.max()),
        "fs8_min": float(fs8_values.min()),
        "fs8_max": float(fs8_values.max()),
        "probability_min": float(probabilities.min()),
        "probability_max": float(probabilities.max()),
        "positive_probability_rows": int(np.count_nonzero(probabilities > 0.0)),
        "zero_probability_rows": int(np.count_nonzero(probabilities == 0.0)),
        "log_floor_probability": LOG_FLOOR_PROBABILITY,
        "best_dm_over_rd": float(dm_values[max_index[0]]),
        "best_dh_over_rd": float(dh_values[max_index[1]]),
        "best_fsigma8": float(fs8_values[max_index[2]]),
        "best_probability": float(probabilities[max_index]),
        "status": "pass",
    }
    return schema, interpolator


def growth_cache_key(model_key: str, params: dict[str, float]) -> tuple[str, tuple[tuple[str, float], ...]]:
    return model_key, tuple(sorted((key, float(value)) for key, value in params.items()))


def cached_growth_solution(model_key: str, params: dict[str, float]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    key = growth_cache_key(model_key, params)
    if key not in GROWTH_CACHE:
        GROWTH_CACHE[key] = growth.growth_solution(model_key, params)
    return GROWTH_CACHE[key]


def fsigma8_unit(model_key: str, params: dict[str, float], z_value: float) -> float:
    x_grid, d_grid, f_grid = cached_growth_solution(model_key, params)
    x_value = math.log(1.0 / (1.0 + z_value))
    d_value = float(np.interp(x_value, x_grid, d_grid))
    f_value = float(np.interp(x_value, x_grid, f_grid))
    return d_value * f_value


def elg_prediction_components(model_key: str, params: dict[str, float]) -> dict[str, float]:
    z_values = np.asarray([ELG_Z_EFF], dtype=float)
    dm = float(params["BAO_alpha"] * growth.snbao.comoving_integral(model_key, z_values, params)[0])
    dh = float(params["BAO_alpha"] / growth.snbao.e_z(model_key, z_values, params)[0])
    fs8_unit_value = fsigma8_unit(model_key, params, ELG_Z_EFF)
    return {
        "z_eff": ELG_Z_EFF,
        "dm_over_rd": dm,
        "dh_over_rd": dh,
        "fsigma8_unit_sigma8_1": fs8_unit_value,
    }


def in_grid(schema: dict[str, Any], dm: float, dh: float, fs8: float) -> bool:
    return (
        schema["dm_min"] <= dm <= schema["dm_max"]
        and schema["dh_min"] <= dh <= schema["dh_max"]
        and schema["fs8_min"] <= fs8 <= schema["fs8_max"]
    )


def chi2_from_grid(
    schema: dict[str, Any],
    interpolator: interpolate.RegularGridInterpolator,
    dm: float,
    dh: float,
    fs8: float,
) -> tuple[float, float, bool]:
    inside = in_grid(schema, dm, dh, fs8)
    log_probability = float(interpolator([[dm, dh, fs8]])[0])
    chi2 = -2.0 * log_probability
    return chi2, log_probability, inside


def fit_sigma8_grid(
    schema: dict[str, Any],
    interpolator: interpolate.RegularGridInterpolator,
    prediction: dict[str, float],
) -> tuple[float, float, float, bool, bool]:
    def objective(sigma8: float) -> float:
        fs8 = sigma8 * prediction["fsigma8_unit_sigma8_1"]
        chi2, _, _ = chi2_from_grid(schema, interpolator, prediction["dm_over_rd"], prediction["dh_over_rd"], fs8)
        return chi2

    result = optimize.minimize_scalar(objective, bounds=(0.2, 1.4), method="bounded", options={"xatol": 1.0e-6})
    if not result.success:
        raise ValueError(f"sigma8 optimization failed: {result.message}")
    sigma8 = float(result.x)
    fs8 = sigma8 * prediction["fsigma8_unit_sigma8_1"]
    chi2, log_probability, inside = chi2_from_grid(
        schema, interpolator, prediction["dm_over_rd"], prediction["dh_over_rd"], fs8
    )
    sigma8_edge = min(sigma8 - 0.2, 1.4 - sigma8) <= 0.012
    return sigma8, chi2, log_probability, sigma8_edge, inside


def fit_rows(
    schema: dict[str, Any],
    interpolator: interpolate.RegularGridInterpolator,
) -> list[dict[str, Any]]:
    specs = growth.load_background_specs()
    rows = []
    for spec in specs:
        prediction = elg_prediction_components(spec["model_key"], spec["params"])
        sigma8, chi2, log_probability, sigma8_edge, inside = fit_sigma8_grid(schema, interpolator, prediction)
        rows.append(
            {
                "background_branch": spec["background_branch"],
                "source_dataset_label": spec["source_dataset_label"],
                "model": spec["model"],
                "z_eff": ELG_Z_EFF,
                "dm_over_rd": prediction["dm_over_rd"],
                "dh_over_rd": prediction["dh_over_rd"],
                "fsigma8_unit_sigma8_1": prediction["fsigma8_unit_sigma8_1"],
                "sigma8_0": sigma8,
                "fsigma8": sigma8 * prediction["fsigma8_unit_sigma8_1"],
                "grid_chi2": chi2,
                "neg2_log_relative_probability": chi2,
                "log_relative_probability": log_probability,
                "AIC": chi2 + 2.0,
                "BIC": chi2 + math.log(1.0),
                "n_data_effective": 1,
                "dynamic_k": 1,
                "sigma8_edge_flag": sigma8_edge,
                "inside_grid": inside,
                "Omega_m0": spec["Omega_m0"],
                "h": spec["h"],
                "H0": spec["H0"],
                "BAO_alpha": spec["BAO_alpha"],
                "source_edge_flag": spec["source_edge_flag"],
                "claim_ceiling": CLAIM_CEILING,
            }
        )
    return rows


def comparison_label(delta: float) -> str:
    if delta <= -2.0:
        return "locked_preferred"
    if delta < 2.0:
        return "competitive_draw"
    return "locked_disfavored"


def baseline_comparison_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {(row["background_branch"], row["model"]): row for row in fits}
    for background_branch in sorted({row["background_branch"] for row in fits}):
        locked = by_key[(background_branch, PRIMARY_MODEL)]
        for reference_model in ["LCDM", "wCDM", "CPL", "MTS_Bmem_zero"]:
            reference = by_key[(background_branch, reference_model)]
            delta = float(locked["grid_chi2"]) - float(reference["grid_chi2"])
            rows.append(
                {
                    "background_branch": background_branch,
                    "model": PRIMARY_MODEL,
                    "reference_model": reference_model,
                    "delta_chi2": delta,
                    "delta_AIC": float(locked["AIC"]) - float(reference["AIC"]),
                    "delta_BIC": float(locked["BIC"]) - float(reference["BIC"]),
                    "locked_sigma8_edge": locked["sigma8_edge_flag"],
                    "reference_sigma8_edge": reference["sigma8_edge_flag"],
                    "locked_inside_grid": locked["inside_grid"],
                    "reference_inside_grid": reference["inside_grid"],
                    "reference_background_edge": reference["source_edge_flag"],
                    "readout": comparison_label(delta),
                }
            )
    return rows


def control_rows(fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_key = {(row["background_branch"], row["model"]): row for row in fits}
    for background_branch in sorted({row["background_branch"] for row in fits}):
        lcdm = by_key[(background_branch, "LCDM")]
        zero = by_key[(background_branch, "MTS_Bmem_zero")]
        delta = float(zero["grid_chi2"]) - float(lcdm["grid_chi2"])
        rows.append(
            {
                "background_branch": background_branch,
                "control": "MTS_Bmem_zero_vs_LCDM",
                "delta_chi2": delta,
                "delta_sigma8_0": float(zero["sigma8_0"]) - float(lcdm["sigma8_0"]),
                "status": "pass" if abs(delta) < 1.0e-8 else "check",
            }
        )
    return rows


def nearest_grid_rows(schema: dict[str, Any], fits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for fit in fits:
        rows.append(
            {
                "background_branch": fit["background_branch"],
                "model": fit["model"],
                "dm_offset_from_best": float(fit["dm_over_rd"]) - float(schema["best_dm_over_rd"]),
                "dh_offset_from_best": float(fit["dh_over_rd"]) - float(schema["best_dh_over_rd"]),
                "fs8_offset_from_best": float(fit["fsigma8"]) - float(schema["best_fsigma8"]),
                "grid_chi2": fit["grid_chi2"],
                "inside_grid": fit["inside_grid"],
            }
        )
    return rows


def combined_with_gaussian_rows(elg_comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaussian_path = RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout" / "results" / "baseline_comparisons.csv"
    gaussian_rows = read_csv_rows(gaussian_path)
    rows = []
    for background_branch in sorted({row["background_branch"] for row in elg_comparisons}):
        elg_lcdm = next(
            row
            for row in elg_comparisons
            if row["background_branch"] == background_branch and row["reference_model"] == "LCDM"
        )
        gaussian_lcdm = next(
            row
            for row in gaussian_rows
            if row["background_branch"] == background_branch
            and row["branch_label"] == "primary_BAO_plus_all_samples"
            and row["score_mode"] == "all"
            and row["reference_model"] == "LCDM"
        )
        total_delta = float(gaussian_lcdm["delta_chi2"]) + float(elg_lcdm["delta_chi2"])
        rows.append(
            {
                "background_branch": background_branch,
                "combination": "primary_Gaussian_BAO_plus_all_plus_ELG_grid_diagnostic",
                "gaussian_delta_chi2_vs_LCDM": gaussian_lcdm["delta_chi2"],
                "ELG_grid_delta_chi2_vs_LCDM": elg_lcdm["delta_chi2"],
                "sum_delta_chi2_vs_LCDM": total_delta,
                "readout": comparison_label(total_delta),
                "claim_limit": "diagnostic_sum_only; not official combined likelihood",
            }
        )
    return rows


def source_register_rows(script_path: Path, intake_dir: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "growth_route_gate.py",
        SCRIPT_DIR / "source_locked_growth_covariance_holdout.py",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        SOURCE_MANIFEST,
        SDSS_ROOT / "row_lock_manifest.json",
        WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
        RUNS_ROOT / "20260531-224500-source-locked-growth-covariance-holdout" / "status.json",
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
    fits: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    combined: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    primary = next(
        row
        for row in comparisons
        if row["background_branch"] == "DR2_noCMB_primary" and row["reference_model"] == "LCDM"
    )
    primary_delta = float(primary["delta_chi2"])
    combined_primary = next(row for row in combined if row["background_branch"] == "DR2_noCMB_primary")
    source_failures = [row for row in lock_rows if row["status"] != "pass"]
    bad_controls = [row for row in controls if row["status"] != "pass"]
    locked_edges = [row for row in fits if row["model"] == PRIMARY_MODEL and row["sigma8_edge_flag"] in [True, "True"]]
    outside = [row for row in fits if row["inside_grid"] not in [True, "True"]]
    if source_failures:
        status = "ELG_grid_source_lock_failure"
    elif outside:
        status = "ELG_grid_prediction_outside_grid"
    elif bad_controls:
        status = "ELG_grid_control_failure"
    elif locked_edges:
        status = "ELG_grid_locked_sigma8_edge"
    elif primary_delta > 2.0:
        status = "ELG_grid_primary_tension_vs_LCDM"
    elif primary_delta <= -2.0:
        status = "ELG_grid_primary_preferred_vs_LCDM"
    else:
        status = "ELG_grid_primary_competitive_draw"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary_ELG_delta_vs_LCDM={primary_delta:.12g}; combined_diagnostic_sum={float(combined_primary['sum_delta_chi2_vs_LCDM']):.12g}",
        },
        {
            "item": "source_lock",
            "verdict": "pass" if not source_failures else "fail",
            "evidence": f"fetched_files={len(lock_rows)}; failures={len(source_failures)}",
        },
        {
            "item": "primary_ELG_grid_vs_LCDM",
            "verdict": primary["readout"],
            "evidence": f"delta_chi2={primary_delta:.12g}; z_eff={ELG_Z_EFF}",
        },
        {
            "item": "combined_diagnostic_vs_LCDM",
            "verdict": combined_primary["readout"],
            "evidence": f"sum_delta_chi2={float(combined_primary['sum_delta_chi2_vs_LCDM']):.12g}; not official joint likelihood",
        },
        {
            "item": "negative_control",
            "verdict": "pass" if not bad_controls else "check",
            "evidence": "MTS_Bmem_zero reproduces LCDM on ELG grid" if not bad_controls else f"{len(bad_controls)} control rows failed",
        },
        {
            "item": "claim_status",
            "verdict": "ELG_grid_holdout_only_no_theory_promotion",
            "evidence": "Non-Gaussian grid likelihood scored with shared sigma8_0; no perturbation derivation, CMB claim, or local-GR theorem.",
        },
        {
            "item": "next_target",
            "verdict": "official_likelihood_wrapper_or_CMB_perturbation_contract",
            "evidence": "ELG parser closes the obvious SDSS/eBOSS Gaussian-only gap; remaining empirical lift is official stack integration.",
        },
    ]


def gate_rows(
    lock_rows: list[dict[str, Any]],
    schema: dict[str, Any],
    fits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    status = next(row["verdict"] for row in decisions if row["item"] == "status")
    return [
        {
            "gate": "source_fetch_hash_lock",
            "status": "pass" if all(row["status"] == "pass" for row in lock_rows) else "fail",
            "evidence": f"files={len(lock_rows)}",
        },
        {
            "gate": "grid_schema",
            "status": schema["status"],
            "evidence": f"{schema['dm_unique']}x{schema['dh_unique']}x{schema['fs8_unique']} grid; rows={schema['rows']}",
        },
        {
            "gate": "prediction_inside_grid",
            "status": "pass" if all(row["inside_grid"] in [True, "True"] for row in fits) else "fail",
            "evidence": f"fit_rows={len(fits)}",
        },
        {
            "gate": "frozen_B_mem_no_refit",
            "status": "pass",
            "evidence": f"B_mem={LOCKED_B_MEM}; only sigma8_0 profiled for every model",
        },
        {
            "gate": "negative_control",
            "status": "pass" if all(row["status"] == "pass" for row in controls) else "fail",
            "evidence": "Bmem-zero control reproduces LCDM",
        },
        {
            "gate": "primary_ELG_not_disfavored",
            "status": "pass" if "tension" not in status and "failure" not in status else "fail",
            "evidence": status,
        },
        {
            "gate": "official_joint_claim",
            "status": "fail",
            "evidence": "combined Gaussian+ELG row is diagnostic only, not an official likelihood wrapper",
        },
        {
            "gate": "theory_promotion",
            "status": "fail",
            "evidence": "ELG grid stress cannot derive perturbation action/local GR/CMB",
        },
    ]


def run_holdout(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-ELG-grid-likelihood-holdout"
    results_dir = run_dir / "results"
    intake_dir = SOURCE_INTAKE_ROOT / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)

    lock_rows, fetched = fetch_and_lock(intake_dir)
    grid_relative = "BAO-plus/sdss_DR16_ELG_FSBAO_DMDHfs8gridlikelihood.txt"
    grid_schema, grid_interpolator = load_grid(fetched[grid_relative])
    fits = fit_rows(grid_schema, grid_interpolator)
    comparisons = baseline_comparison_rows(fits)
    controls = control_rows(fits)
    nearest = nearest_grid_rows(grid_schema, fits)
    combined = combined_with_gaussian_rows(comparisons)
    decisions = decision_rows(lock_rows, fits, comparisons, controls, combined)
    gates = gate_rows(lock_rows, grid_schema, fits, controls, decisions)
    sources = source_register_rows(Path(__file__).resolve(), intake_dir)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
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
    write_csv(results_dir / "grid_schema.csv", [grid_schema], list(grid_schema))
    write_csv(
        results_dir / "fit_summary.csv",
        fits,
        [
            "background_branch",
            "source_dataset_label",
            "model",
            "z_eff",
            "dm_over_rd",
            "dh_over_rd",
            "fsigma8_unit_sigma8_1",
            "sigma8_0",
            "fsigma8",
            "grid_chi2",
            "neg2_log_relative_probability",
            "log_relative_probability",
            "AIC",
            "BIC",
            "n_data_effective",
            "dynamic_k",
            "sigma8_edge_flag",
            "inside_grid",
            "Omega_m0",
            "h",
            "H0",
            "BAO_alpha",
            "source_edge_flag",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "background_branch",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_sigma8_edge",
            "reference_sigma8_edge",
            "locked_inside_grid",
            "reference_inside_grid",
            "reference_background_edge",
            "readout",
        ],
    )
    write_csv(results_dir / "control_reproduction.csv", controls, ["background_branch", "control", "delta_chi2", "delta_sigma8_0", "status"])
    write_csv(results_dir / "nearest_grid_offsets.csv", nearest, ["background_branch", "model", "dm_offset_from_best", "dh_offset_from_best", "fs8_offset_from_best", "grid_chi2", "inside_grid"])
    write_csv(
        results_dir / "combined_gaussian_plus_ELG_diagnostic.csv",
        combined,
        [
            "background_branch",
            "combination",
            "gaussian_delta_chi2_vs_LCDM",
            "ELG_grid_delta_chi2_vs_LCDM",
            "sum_delta_chi2_vs_LCDM",
            "readout",
            "claim_limit",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_intake_dir": str(intake_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_B_mem": LOCKED_B_MEM,
        "z_eff": ELG_Z_EFF,
        "grid_shape": f"{grid_schema['dm_unique']}x{grid_schema['dh_unique']}x{grid_schema['fs8_unique']}",
        "generated": [
            "source_register.csv",
            "fetch_hash_lock.csv",
            "grid_schema.csv",
            "fit_summary.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "nearest_grid_offsets.csv",
            "combined_gaussian_plus_ELG_diagnostic.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "official_likelihood_wrapper_or_CMB_perturbation_contract",
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
