#!/usr/bin/env python3
"""Dry-run wrapper for the first SN+BAO empirical closure test.

This script intentionally does not score models yet. The first phase only freezes
the model matrix, amplitude policy, baseline fairness rules, output contract, and
data-path state.
"""

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
from scipy import integrate, linalg, optimize


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = POST_CHECKPOINT / "runs"
DESIGN_RUN = POST_CHECKPOINT / "runs" / "20260531-122041-closure-test-runner-design" / "results"
MANIFEST_RUN = POST_CHECKPOINT / "runs" / "20260531-121628-empirical-closure-test-manifest" / "results"
LOCKED_B_MEM = 2.0 / 27.0


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def model_matrix() -> list[dict[str, Any]]:
    return [
        {
            "model_key": "LCDM",
            "role": "baseline",
            "fixed_factors": "standard model form",
            "fitted_factors": "Omega_m; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
            "k_count_dry_run": 2,
        },
        {
            "model_key": "wCDM",
            "role": "baseline",
            "fixed_factors": "constant-w form",
            "fitted_factors": "Omega_m; w; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
            "k_count_dry_run": 3,
        },
        {
            "model_key": "CPL",
            "role": "baseline",
            "fixed_factors": "CPL form",
            "fitted_factors": "Omega_m; w0; wa; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "baseline",
            "k_count_dry_run": 4,
        },
        {
            "model_key": "MTS_fixed_2over27_no_clock",
            "role": "primary_closure",
            "fixed_factors": "p=3; u3=1/4; B_mem=2/27; no global clock",
            "fitted_factors": "Omega_m; nuisance offset/calibration",
            "ablation_status": "primary",
            "claim_ceiling": "closure_performance_only_locked_amplitude",
            "k_count_dry_run": 2,
        },
        {
            "model_key": "MTS_fixed_p3_u3quarter",
            "role": "diagnostic_fitted_amplitude",
            "fixed_factors": "p=3; u3=1/4",
            "fitted_factors": "B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "fitted_amplitude_diagnostic",
            "claim_ceiling": "diagnostic_only_not_locked_closure",
            "k_count_dry_run": 3,
        },
        {
            "model_key": "MTS_fitted_p",
            "role": "ablation",
            "fixed_factors": "u3=1/4",
            "fitted_factors": "p; B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "required_short_or_robustness",
            "claim_ceiling": "closure_ablation_only",
            "k_count_dry_run": 4,
        },
        {
            "model_key": "MTS_fitted_u3",
            "role": "ablation",
            "fixed_factors": "p=3",
            "fitted_factors": "u3; B_mem/b_mem; Omega_m; nuisance offset/calibration",
            "ablation_status": "required_short_or_robustness",
            "claim_ceiling": "closure_ablation_only",
            "k_count_dry_run": 4,
        },
        {
            "model_key": "MTS_Bmem_zero",
            "role": "negative_control",
            "fixed_factors": "p=3; u3=1/4; B_mem=0",
            "fitted_factors": "Omega_m; nuisance offset/calibration",
            "ablation_status": "required",
            "claim_ceiling": "control",
            "k_count_dry_run": 2,
        },
    ]


def amplitude_policy() -> list[dict[str, Any]]:
    return [
        {
            "factor": "p=3",
            "treatment": "fixed_primary",
            "prior": "ablation fitted_p required before robustness claim",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "fixed_vs_fitted_p",
        },
        {
            "factor": "u3=1/4",
            "treatment": "fixed_primary",
            "prior": "ablation fitted_u3 and inherited_C2_u3 required",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "fixed_vs_fitted_u3",
        },
        {
            "factor": "B_mem=2/27",
            "treatment": "fixed_primary_locked_no_clock",
            "prior": "theorem-target closure value; no fit freedom in primary branch",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "locked_amplitude_primary",
        },
        {
            "factor": "B_mem/b_mem",
            "treatment": "fitted_diagnostic_not_primary",
            "prior": "wide fitted diagnostic only; cannot be described as locked 2/27 evidence",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "dangerous_amplitude",
        },
        {
            "factor": "Ccoh",
            "treatment": "diagnostic_only",
            "prior": "not used as derived local suppression",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "selector_off_or_nonselector",
        },
        {
            "factor": "A_loc/q_loc",
            "treatment": "bound_only",
            "prior": "set_to_zero_GR_limit for SN+BAO background runner",
            "best_fit": "",
            "edge_flag": "not_scored",
            "ablation_role": "local_residual_constraint",
        },
    ]


def baseline_fairness() -> list[dict[str, Any]]:
    return [
        {
            "baseline_rule": "same_data_splits",
            "requirement": "MTS and baselines use identical SN/BAO rows and any split masks",
            "dry_run_status": "required_before_scoring",
        },
        {
            "baseline_rule": "same_nuisance_freedom",
            "requirement": "SN offset/calibration treatment is symmetric across MTS and baselines",
            "dry_run_status": "required_before_scoring",
        },
        {
            "baseline_rule": "same_calibration_branch",
            "requirement": "no-SH0ES or calibration-free branch must apply to baselines too",
            "dry_run_status": "required_before_scoring",
        },
        {
            "baseline_rule": "symmetric_failure_reporting",
            "requirement": "jackknife/split failures must be reported for MTS and baselines",
            "dry_run_status": "required_before_scoring",
        },
        {
            "baseline_rule": "no_claim_from_edge_hits",
            "requirement": "prior-edge best fits are unstable, not evidence",
            "dry_run_status": "required_before_scoring",
        },
    ]


def candidate_files(kind: str) -> list[Path]:
    patterns = {
        "SN_shape": ("pantheon", "supernova", "sh0es", "sn_"),
        "BAO_distances": ("bao", "desi"),
    }[kind]
    formalization = POST_CHECKPOINT.parent / "formalization-workbench"
    priority_paths = {
        "SN_shape": [
            formalization / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat",
        ],
        "BAO_distances": [
            formalization / "data" / "cosmology" / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt",
            formalization / "data" / "cosmology" / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt",
        ],
    }[kind]
    roots = [POST_CHECKPOINT, formalization]
    suffixes = {".csv", ".txt", ".dat"}
    candidates: list[Path] = []
    for path in priority_paths:
        if path.exists() and path.is_file():
            candidates.append(path)
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            lowered_parent = str(path.parent).lower()
            if "\\runs\\" in lowered_parent or "/runs/" in lowered_parent:
                continue
            lowered = path.name.lower() + " " + str(path.parent).lower()
            if any(pattern in lowered for pattern in patterns):
                if path not in candidates:
                    candidates.append(path)
            if len(candidates) >= 25:
                return candidates
    return candidates


def schema_status(kind: str, columns: str, row_count: int, readable: bool) -> tuple[str, str]:
    if not readable:
        return "candidate_unreadable", "file could not be parsed"
    lowered_columns = {column.strip().lower() for column in columns.split(",") if column.strip()}
    if row_count <= 0:
        return "schema_invalid", "no data rows found"

    redshift_like = {"z", "redshift", "zcmb", "zhel", "z_hd", "zhelio"}
    sn_value_like = {"mu", "mu_obs", "muobs", "mb", "m_b", "distance_modulus", "mu_sh0es"}
    sn_unc_like = {"sigma", "sigma_mu", "dmu", "muerr", "error", "stat"}
    bao_value_like = {
        "value",
        "measurement",
        "dv",
        "dm",
        "dh",
        "da",
        "rd_over_dv",
        "dv_over_rd",
        "dm_over_rd",
        "dh_over_rd",
        "observable",
    }
    bao_unc_like = {"sigma", "error", "uncertainty", "covariance", "cov", "stat"}

    if kind == "SN_shape":
        has_z = bool(lowered_columns & redshift_like)
        has_value = bool(lowered_columns & sn_value_like)
        has_uncertainty = bool(lowered_columns & sn_unc_like) or "cov" in " ".join(lowered_columns)
        if has_z and has_value and has_uncertainty:
            return "schema_valid", ""
        return (
            "schema_mismatch",
            "SN candidate needs redshift-like, distance/magnitude-like, and uncertainty/covariance columns",
        )

    has_z = bool(lowered_columns & redshift_like)
    has_value = bool(lowered_columns & bao_value_like)
    has_uncertainty = bool(lowered_columns & bao_unc_like)
    if has_z and has_value and "quantity" in lowered_columns:
        return "schema_valid_mean_vector_needs_paired_covariance", ""
    if has_z and has_value and has_uncertainty:
        return "schema_valid", ""
    return "schema_mismatch", "BAO candidate needs redshift, observable/value, and uncertainty/covariance columns"


def inspect_table(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "readable": False,
            "row_count": 0,
            "columns": "",
            "sha256": "",
            "issue": "missing_path",
        }
    try:
        if path.suffix.lower() == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                columns = ",".join(payload.keys())
                row_count = len(payload)
            elif isinstance(payload, list):
                columns = ",".join(payload[0].keys()) if payload and isinstance(payload[0], dict) else ""
                row_count = len(payload)
            else:
                columns = type(payload).__name__
                row_count = 1
        else:
            with path.open("r", newline="", encoding="utf-8-sig") as handle:
                sample = handle.read(4096)
                handle.seek(0)
                if "_cov" in path.name.lower() or "covariance" in path.name.lower():
                    rows = [
                        line.strip().split()
                        for line in sample.splitlines()
                        if line.strip() and not line.strip().startswith("#")
                    ]
                    if rows and all(len(row) == len(rows[0]) for row in rows):
                        columns = "cov_matrix"
                        row_count = len(rows)
                    else:
                        raise csv.Error("Could not parse covariance matrix")
                else:
                    try:
                        dialect = csv.Sniffer().sniff(sample, delimiters=",\t ;|")
                        reader = csv.reader(handle, dialect)
                        header = next(reader, [])
                        row_count = sum(1 for _ in reader)
                        columns = ",".join(str(column) for column in header)
                    except csv.Error:
                        rows = [
                            line.strip().split()
                            for line in sample.splitlines()
                            if line.strip() and not line.strip().startswith("#")
                        ]
                        if rows and len(rows[0]) == 3 and "mean" in path.name.lower():
                            columns = "z,value,quantity"
                            row_count = len(rows)
                        elif rows and all(len(row) == len(rows[0]) for row in rows):
                            columns = "cov_matrix"
                            row_count = len(rows)
                        else:
                            raise
        return {
            "path": str(path),
            "exists": True,
            "readable": True,
            "row_count": row_count,
            "columns": columns,
            "sha256": file_sha256(path),
            "issue": "",
        }
    except Exception as exc:  # noqa: BLE001 - dry-run should report schema/read errors.
        return {
            "path": str(path),
            "exists": path.exists(),
            "readable": False,
            "row_count": 0,
            "columns": "",
            "sha256": "",
            "issue": f"{type(exc).__name__}: {exc}",
        }


def covariance_schema_row(
    dataset: str,
    path: Path | None,
    expected_size: int | None = None,
    flattened_with_size: bool = False,
) -> dict[str, Any]:
    if path is None:
        return {
            "dataset": dataset,
            "path": "",
            "explicit_path": False,
            "exists": False,
            "readable": False,
            "row_count": 0,
            "columns": "cov_matrix",
            "sha256": "",
            "schema_status": "missing",
            "issue": f"{dataset} path not provided",
        }
    if not path.exists():
        return {
            "dataset": dataset,
            "path": str(path),
            "explicit_path": True,
            "exists": False,
            "readable": False,
            "row_count": 0,
            "columns": "cov_matrix",
            "sha256": "",
            "schema_status": "missing",
            "issue": "covariance path does not exist",
        }
    try:
        if flattened_with_size:
            values = np.fromfile(path, sep=" ")
            if values.size < 2:
                raise ValueError("covariance file is empty or too short")
            matrix_size = int(values[0])
            value_count = int(values.size - 1)
            expected_count = matrix_size * matrix_size
            valid_shape = value_count == expected_count
        else:
            matrix = np.loadtxt(path)
            if matrix.ndim != 2:
                raise ValueError("covariance is not a 2D matrix")
            matrix_size = int(matrix.shape[0])
            valid_shape = matrix.shape[0] == matrix.shape[1]
        if expected_size is not None and matrix_size != expected_size:
            valid_shape = False
            issue = f"covariance size {matrix_size} does not match expected size {expected_size}"
        else:
            issue = "" if valid_shape else "covariance shape is not square or complete"
        return {
            "dataset": dataset,
            "path": str(path),
            "explicit_path": True,
            "exists": True,
            "readable": True,
            "row_count": matrix_size,
            "columns": "cov_matrix",
            "sha256": file_sha256(path),
            "schema_status": "schema_valid" if valid_shape else "schema_mismatch",
            "issue": issue,
        }
    except Exception as exc:  # noqa: BLE001 - dry-run should report schema/read errors.
        return {
            "dataset": dataset,
            "path": str(path),
            "explicit_path": True,
            "exists": path.exists(),
            "readable": False,
            "row_count": 0,
            "columns": "cov_matrix",
            "sha256": "",
            "schema_status": "schema_mismatch",
            "issue": f"{type(exc).__name__}: {exc}",
        }


def data_schema_rows(
    sn_data: Path | None,
    bao_data: Path | None,
    sn_cov: Path | None = None,
    bao_cov: Path | None = None,
    require_sn_full_covariance: bool = False,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    explicit = {"SN_shape": sn_data, "BAO_distances": bao_data}
    for kind, explicit_path in explicit.items():
        paths = [explicit_path] if explicit_path else candidate_files(kind)[:5]
        if not paths:
            rows.append(
                {
                    "dataset": kind,
                    "path": "",
                    "explicit_path": bool(explicit_path),
                    "exists": False,
                    "readable": False,
                    "row_count": 0,
                    "columns": "",
                    "sha256": "",
                    "schema_status": "missing",
                    "issue": "no candidate path found; provide --sn-data or --bao-data",
                }
            )
            continue
        for path in paths:
            info = inspect_table(path)
            status, schema_issue = schema_status(kind, info["columns"], info["row_count"], info["readable"])
            if status == "schema_valid_mean_vector_needs_paired_covariance":
                cov_path = Path(str(path).replace("_mean", "_cov"))
                if cov_path.exists():
                    cov_info = inspect_table(cov_path)
                    if cov_info["readable"] and int(cov_info["row_count"]) == int(info["row_count"]):
                        status = "schema_valid"
                        schema_issue = f"paired covariance validated: {cov_path}"
                    else:
                        status = "schema_mismatch"
                        schema_issue = f"paired covariance missing/unreadable/shape mismatch: {cov_path}"
                else:
                    status = "schema_mismatch"
                    schema_issue = f"paired covariance missing: {cov_path}"
            issue = info["issue"] or schema_issue
            rows.append(
                {
                    "dataset": kind,
                    "path": info["path"],
                    "explicit_path": bool(explicit_path),
                    "exists": info["exists"],
                    "readable": info["readable"],
                    "row_count": info["row_count"],
                    "columns": info["columns"],
                    "sha256": info["sha256"],
                    "schema_status": status,
                    "issue": issue,
                }
            )
    sn_source_size: int | None = None
    for row in rows:
        if row["dataset"] == "SN_shape" and row["schema_status"] == "schema_valid":
            sn_source_size = int(row["row_count"])
            break
    if require_sn_full_covariance or sn_cov is not None:
        rows.append(covariance_schema_row("SN_covariance", sn_cov, sn_source_size, flattened_with_size=True))
    bao_mean_size: int | None = None
    for row in rows:
        if row["dataset"] == "BAO_distances" and row["schema_status"] == "schema_valid" and "mean" in Path(row["path"]).name.lower():
            bao_mean_size = int(row["row_count"])
            break
    if bao_cov is not None:
        rows.append(covariance_schema_row("BAO_covariance", bao_cov, bao_mean_size, flattened_with_size=False))
    return rows


def output_contract_rows() -> list[dict[str, Any]]:
    return [
        {"artifact": "status.json", "phase": "dry-run", "created_now": True},
        {"artifact": "run_config.json", "phase": "dry-run", "created_now": True},
        {"artifact": "model_matrix.csv", "phase": "dry-run", "created_now": True},
        {"artifact": "amplitude_policy.csv", "phase": "dry-run", "created_now": True},
        {"artifact": "baseline_fairness.csv", "phase": "dry-run", "created_now": True},
        {"artifact": "data_schema_report.csv", "phase": "dry-run", "created_now": True},
        {"artifact": "fit_summary.csv", "phase": "short-smoke", "created_now": False},
        {"artifact": "baseline_comparison.csv", "phase": "short-smoke", "created_now": False},
        {"artifact": "residuals.csv", "phase": "short-smoke", "created_now": False},
        {"artifact": "prior_edge_table.csv", "phase": "short-smoke", "created_now": False},
    ]


def read_sn_covariance(path: Path, selected_indices: list[int]) -> np.ndarray:
    values = np.fromfile(path, sep=" ")
    if values.size < 2:
        raise ValueError(f"SN covariance file is empty or unreadable: {path}")
    matrix_size = int(values[0])
    expected = matrix_size * matrix_size
    matrix_values = values[1:]
    if matrix_values.size != expected:
        raise ValueError(f"SN covariance has {matrix_values.size} values but expected {expected}")
    covariance = matrix_values.reshape((matrix_size, matrix_size))
    selector = np.asarray(selected_indices, dtype=int)
    if np.any(selector < 0) or np.any(selector >= matrix_size):
        raise ValueError("SN covariance selector is outside matrix range")
    return covariance[np.ix_(selector, selector)]


def read_sn_data(
    path: Path,
    max_rows: int | None = None,
    covariance_path: Path | None = None,
    covariance_mode: str = "diagonal",
    observable: str = "mu-sh0es",
    include_calibrators: bool = False,
) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        header = handle.readline().strip().split()
        rows = [
            dict(zip(header, line.strip().split(), strict=False))
            for line in handle
            if line.strip() and not line.strip().startswith("#")
        ]
    z_values: list[float] = []
    mu_values: list[float] = []
    sigma_values: list[float] = []
    selected_indices: list[int] = []
    for row_index, row in enumerate(rows):
        try:
            z = float(row.get("zHD") or row.get("zCMB") or row.get("z"))
            if observable == "mb-corr":
                mu = float(row.get("m_b_corr") or row.get("mu") or row.get("MU_SH0ES"))
                sigma = float(row.get("m_b_corr_err_DIAG") or row.get("sigma_mu") or row.get("MU_SH0ES_ERR_DIAG"))
            else:
                mu = float(row.get("MU_SH0ES") or row.get("mu") or row.get("m_b_corr"))
                sigma = float(row.get("MU_SH0ES_ERR_DIAG") or row.get("sigma_mu") or row.get("m_b_corr_err_DIAG"))
            is_calibrator = int(float(row.get("IS_CALIBRATOR", "0")))
        except (TypeError, ValueError):
            continue
        if not math.isfinite(z + mu + sigma) or z <= 0.0 or sigma <= 0.0:
            continue
        if is_calibrator and not include_calibrators:
            continue
        z_values.append(z)
        mu_values.append(mu)
        sigma_values.append(max(sigma, 0.03))
        selected_indices.append(row_index)
        if max_rows is not None and len(z_values) >= max_rows:
            break
    if not z_values:
        raise ValueError(f"no usable SN rows in {path}")
    output: dict[str, Any] = {
        "z": np.asarray(z_values, dtype=float),
        "mu": np.asarray(mu_values, dtype=float),
        "sigma": np.asarray(sigma_values, dtype=float),
        "row_indices": np.asarray(selected_indices, dtype=int),
        "covariance_mode": covariance_mode,
        "observable": observable,
        "include_calibrators": include_calibrators,
    }
    if covariance_mode == "full":
        if covariance_path is None:
            raise ValueError("SN full covariance requested but --sn-cov was not provided")
        covariance = read_sn_covariance(covariance_path, selected_indices)
        output["covariance"] = covariance
        output["inv_covariance"] = linalg.inv(covariance)
        output["covariance_path"] = str(covariance_path)
    return output


def read_bao_data(mean_path: Path, cov_path: Path) -> dict[str, Any]:
    bao_rows: list[dict[str, Any]] = []
    with mean_path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            z_text, value_text, quantity = stripped.split()[:3]
            bao_rows.append({"z": float(z_text), "value": float(value_text), "quantity": quantity})
    cov_rows: list[list[float]] = []
    with cov_path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            cov_rows.append([float(value) for value in stripped.split()])
    covariance = np.asarray(cov_rows, dtype=float)
    if covariance.shape != (len(bao_rows), len(bao_rows)):
        raise ValueError(f"BAO covariance shape {covariance.shape} does not match mean vector {len(bao_rows)}")
    return {"rows": bao_rows, "covariance": covariance}


def e_z(model_key: str, z: np.ndarray, params: dict[str, float]) -> np.ndarray:
    omega_m = params["Omega_m"]
    one_plus_z = 1.0 + z
    if model_key == "LCDM":
        e2 = omega_m * one_plus_z**3 + 1.0 - omega_m
    elif model_key == "wCDM":
        w = params["w"]
        e2 = omega_m * one_plus_z**3 + (1.0 - omega_m) * one_plus_z ** (3.0 * (1.0 + w))
    elif model_key == "CPL":
        w0 = params["w0"]
        wa = params["wa"]
        a = 1.0 / one_plus_z
        dark = one_plus_z ** (3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * z / one_plus_z)
        e2 = omega_m * one_plus_z**3 + (1.0 - omega_m) * dark
    elif model_key in {"MTS_fixed_2over27_no_clock", "MTS_fixed_p3_u3quarter", "MTS_fitted_p", "MTS_fitted_u3", "MTS_Bmem_zero"}:
        p = params.get("p", 3.0)
        u3 = params.get("u3", 0.25)
        b_mem = params.get("B_mem", 0.0)
        n_past = np.log1p(z)
        activation = 1.0 - np.exp(-((n_past / u3) ** p))
        e2 = omega_m * one_plus_z**3 + 1.0 - omega_m + b_mem * activation
    else:
        raise ValueError(f"unknown model {model_key}")
    if np.any(e2 <= 0.0) or np.any(~np.isfinite(e2)):
        raise ValueError("non-positive or non-finite E^2")
    return np.sqrt(e2)


def comoving_integral(model_key: str, z: np.ndarray, params: dict[str, float]) -> np.ndarray:
    z_arr = np.asarray(z, dtype=float)
    z_max = float(np.max(z_arr))
    if z_max <= 0.0:
        return np.zeros_like(z_arr)
    grid_size = max(256, min(2048, int(256 + 128 * z_max)))
    grid = np.linspace(0.0, z_max, grid_size)
    inv_e = 1.0 / e_z(model_key, grid, params)
    cumulative = integrate.cumulative_trapezoid(inv_e, grid, initial=0.0)
    return np.interp(z_arr, grid, cumulative)


def analytic_offset_chi2(observed: np.ndarray, predicted_shape: np.ndarray, sigma: np.ndarray) -> tuple[float, float, np.ndarray]:
    weights = 1.0 / (sigma**2)
    offset = float(np.sum(weights * (observed - predicted_shape)) / np.sum(weights))
    predicted = predicted_shape + offset
    residual = observed - predicted
    chi2 = float(np.sum((residual / sigma) ** 2))
    return chi2, offset, residual


def analytic_offset_chi2_covariance(
    observed: np.ndarray,
    predicted_shape: np.ndarray,
    inv_covariance: np.ndarray,
) -> tuple[float, float, np.ndarray]:
    delta = observed - predicted_shape
    ones = np.ones_like(delta)
    inv_delta = inv_covariance @ delta
    inv_ones = inv_covariance @ ones
    offset = float((ones @ inv_delta) / (ones @ inv_ones))
    residual = delta - offset
    chi2 = float(residual @ inv_covariance @ residual)
    return chi2, offset, residual


def sn_chi2(model_key: str, params: dict[str, float], sn: dict[str, np.ndarray]) -> tuple[float, float, np.ndarray, np.ndarray]:
    z = sn["z"]
    integral = comoving_integral(model_key, z, params)
    dl_shape = np.maximum((1.0 + z) * integral, 1.0e-12)
    mu_shape = 5.0 * np.log10(dl_shape)
    if sn.get("covariance_mode") == "full":
        chi2, offset, residual = analytic_offset_chi2_covariance(sn["mu"], mu_shape, sn["inv_covariance"])
    else:
        chi2, offset, residual = analytic_offset_chi2(sn["mu"], mu_shape, sn["sigma"])
    return chi2, offset, residual, mu_shape + offset


def bao_prediction(model_key: str, params: dict[str, float], bao: dict[str, Any], alpha: float) -> np.ndarray:
    z = np.asarray([row["z"] for row in bao["rows"]], dtype=float)
    integral = comoving_integral(model_key, z, params)
    ez = e_z(model_key, z, params)
    predictions: list[float] = []
    for row, dm, e_value in zip(bao["rows"], integral, ez):
        quantity = row["quantity"]
        if quantity == "DM_over_rs":
            predictions.append(alpha * float(dm))
        elif quantity == "DH_over_rs":
            predictions.append(alpha / float(e_value))
        elif quantity == "DV_over_rs":
            predictions.append(alpha * float((row["z"] * dm * dm / e_value) ** (1.0 / 3.0)))
        else:
            raise ValueError(f"unsupported BAO quantity {quantity}")
    return np.asarray(predictions, dtype=float)


def bao_chi2(model_key: str, params: dict[str, float], bao: dict[str, Any]) -> tuple[float, float, np.ndarray, np.ndarray]:
    observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
    covariance = np.asarray(bao["covariance"], dtype=float)
    unit_pred = bao_prediction(model_key, params, bao, alpha=1.0)
    inv_cov = linalg.inv(covariance)
    numerator = float(unit_pred @ inv_cov @ observed)
    denominator = float(unit_pred @ inv_cov @ unit_pred)
    alpha = numerator / denominator
    predicted = alpha * unit_pred
    residual = observed - predicted
    chi2 = float(residual @ inv_cov @ residual)
    return chi2, alpha, residual, predicted


def model_priors(model_key: str, prior_config: dict[str, tuple[float, float]] | None = None) -> dict[str, tuple[float, float]]:
    prior_config = prior_config or {}
    priors: dict[str, tuple[float, float]] = {"Omega_m": (0.05, 0.6)}
    if model_key == "wCDM":
        priors["w"] = (-2.0, -0.2)
    elif model_key == "CPL":
        priors["w0"] = prior_config.get("CPL.w0", (-2.0, -0.2))
        priors["wa"] = prior_config.get("CPL.wa", (-2.0, 2.0))
    elif model_key == "MTS_fixed_p3_u3quarter":
        priors["B_mem"] = (-1.0, 1.0)
    elif model_key == "MTS_fitted_p":
        priors["B_mem"] = (-1.0, 1.0)
        priors["p"] = (1.0, 6.0)
    elif model_key == "MTS_fitted_u3":
        priors["B_mem"] = (-1.0, 1.0)
        priors["u3"] = (0.05, 1.0)
    return priors


def params_from_vector(model_key: str, names: list[str], vector: np.ndarray) -> dict[str, float]:
    params = dict(zip(names, (float(value) for value in vector), strict=True))
    if model_key in {"MTS_fixed_2over27_no_clock", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"}:
        params["p"] = 3.0
        params["u3"] = 0.25
    elif model_key == "MTS_fitted_p":
        params["u3"] = 0.25
    elif model_key == "MTS_fitted_u3":
        params["p"] = 3.0
    if model_key == "MTS_fixed_2over27_no_clock":
        params["B_mem"] = LOCKED_B_MEM
    elif model_key == "MTS_Bmem_zero":
        params["B_mem"] = 0.0
    return params


def score_model(
    model_key: str,
    sn: dict[str, np.ndarray],
    bao: dict[str, Any],
    max_iter: int,
    prior_config: dict[str, tuple[float, float]] | None = None,
) -> dict[str, Any]:
    priors = model_priors(model_key, prior_config)
    names = list(priors)
    bounds = [priors[name] for name in names]

    def objective(vector: np.ndarray) -> float:
        try:
            params = params_from_vector(model_key, names, vector)
            chi2_sn, _, _, _ = sn_chi2(model_key, params, sn)
            chi2_bao, _, _, _ = bao_chi2(model_key, params, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, linalg.LinAlgError):
            return 1.0e30

    rng = np.random.default_rng(12345)
    starts = [np.asarray([(lower + upper) / 2.0 for lower, upper in bounds], dtype=float)]
    for _ in range(max(4, min(12, max_iter // 10))):
        starts.append(np.asarray([rng.uniform(lower, upper) for lower, upper in bounds], dtype=float))
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
    params = params_from_vector(model_key, names, np.asarray(result.x, dtype=float))
    chi2_sn, sn_offset, sn_residual, sn_predicted = sn_chi2(model_key, params, sn)
    chi2_bao, bao_alpha, bao_residual, bao_predicted = bao_chi2(model_key, params, bao)
    chi2_total = chi2_sn + chi2_bao
    n_points = int(len(sn["z"]) + len(bao["rows"]))
    k_count = len(names) + 2
    dof = n_points - k_count
    aic = chi2_total + 2.0 * k_count
    bic = chi2_total + k_count * math.log(n_points)
    edge_rows = prior_edge_rows(model_key, priors, params)
    edge_flag = any(row["edge_flag"] for row in edge_rows)
    return {
        "model": model_key,
        "params": params,
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "dof": dof,
        "k": k_count,
        "n": n_points,
        "AIC": aic,
        "BIC": bic,
        "convergence": bool(result.success),
        "optimizer_message": str(result.message),
        "prior_edge_flag": edge_flag,
        "claim_ceiling": claim_ceiling(model_key),
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "sn_residual": sn_residual,
        "sn_predicted": sn_predicted,
        "bao_residual": bao_residual,
        "bao_predicted": bao_predicted,
        "edge_rows": edge_rows,
    }


def claim_ceiling(model_key: str) -> str:
    for row in model_matrix():
        if row["model_key"] == model_key:
            return str(row["claim_ceiling"])
    return "closure_only"


def prior_edge_rows(model_key: str, priors: dict[str, tuple[float, float]], params: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for parameter, (lower, upper) in priors.items():
        best_fit = params[parameter]
        width = upper - lower
        distance = min(best_fit - lower, upper - best_fit)
        edge_flag = distance < 0.01 * width
        rows.append(
            {
                "model": model_key,
                "parameter": parameter,
                "best_fit": best_fit,
                "lower": lower,
                "upper": upper,
                "distance_to_edge": distance,
                "edge_flag": edge_flag,
            }
        )
    return rows


def fit_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "model": score["model"],
            "chi2_SN": score["chi2_SN"],
            "chi2_BAO": score["chi2_BAO"],
            "chi2_total": score["chi2_total"],
            "dof": score["dof"],
            "k": score["k"],
            "n": score["n"],
            "AIC": score["AIC"],
            "BIC": score["BIC"],
            "convergence": score["convergence"],
            "prior_edge_flag": score["prior_edge_flag"],
            "claim_ceiling": score["claim_ceiling"],
            "optimizer_message": score["optimizer_message"],
        }
        for score in scores
    ]


def baseline_comparison_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    baseline_names = ["LCDM", "wCDM", "CPL"]
    rows: list[dict[str, Any]] = []
    for score in scores:
        for baseline in baseline_names:
            if baseline not in by_model or score["model"] == baseline:
                continue
            base = by_model[baseline]
            rows.append(
                {
                    "model": score["model"],
                    "reference_baseline": baseline,
                    "delta_chi2": score["chi2_total"] - base["chi2_total"],
                    "delta_AIC": score["AIC"] - base["AIC"],
                    "delta_BIC": score["BIC"] - base["BIC"],
                    "same_data": True,
                    "same_nuisance": True,
                    "same_calibration": True,
                }
            )
    return rows


def residual_rows(scores: list[dict[str, Any]], sn: dict[str, np.ndarray], bao: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sn_cov_label = "full_covariance" if sn.get("covariance_mode") == "full" else "diagonal_sigma"
    bao_label = bao.get("label", "BAO_primary")
    for score in scores:
        for index, (z, observed, predicted, residual, sigma) in enumerate(
            zip(sn["z"], sn["mu"], score["sn_predicted"], score["sn_residual"], sn["sigma"])
        ):
            rows.append(
                {
                    "dataset": f"SN_{sn.get('observable', 'mu-sh0es')}",
                    "model": score["model"],
                    "observable": "mu_shape_with_offset",
                    "coordinate": z,
                    "observed": observed,
                    "predicted": predicted,
                    "residual": residual,
                    "sigma_or_cov_block": f"{sn_cov_label}:{sigma if sn_cov_label == 'diagonal_sigma' else index}",
                    "row_index": index,
                }
            )
        for index, (bao_row, predicted, residual) in enumerate(
            zip(bao["rows"], score["bao_predicted"], score["bao_residual"])
        ):
            rows.append(
                {
                    "dataset": bao_label,
                    "model": score["model"],
                    "observable": bao_row["quantity"],
                    "coordinate": bao_row["z"],
                    "observed": bao_row["value"],
                    "predicted": predicted,
                    "residual": residual,
                    "sigma_or_cov_block": f"cov_index_{index}",
                    "row_index": index,
                }
            )
    return rows


def scored_amplitude_policy_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model = {score["model"]: score for score in scores}
    rows = amplitude_policy()
    for row in rows:
        if row["factor"] == "B_mem=2/27" and "MTS_fixed_2over27_no_clock" in by_model:
            score = by_model["MTS_fixed_2over27_no_clock"]
            row["best_fit"] = score["params"].get("B_mem", LOCKED_B_MEM)
            row["edge_flag"] = False
        elif row["factor"] == "B_mem/b_mem" and "MTS_fixed_p3_u3quarter" in by_model:
            score = by_model["MTS_fixed_p3_u3quarter"]
            row["best_fit"] = score["params"].get("B_mem", "")
            row["edge_flag"] = score["prior_edge_flag"]
        elif row["factor"] == "p=3":
            row["best_fit"] = "3 fixed"
            row["edge_flag"] = False
        elif row["factor"] == "u3=1/4":
            row["best_fit"] = "0.25 fixed"
            row["edge_flag"] = False
    return rows


def status_payload(run_dir: Path, phase: str, rows: list[dict[str, Any]], require_sn_full_covariance: bool = False) -> dict[str, Any]:
    readable_sn = any(row["dataset"] == "SN_shape" and row["schema_status"] == "schema_valid" for row in rows)
    readable_bao = any(row["dataset"] == "BAO_distances" and row["schema_status"] == "schema_valid" for row in rows)
    readable_sn_covariance = any(row["dataset"] == "SN_covariance" and row["schema_status"] == "schema_valid" for row in rows)
    data_ready = readable_sn and readable_bao and (readable_sn_covariance or not require_sn_full_covariance)
    failures: list[str] = []
    if not readable_sn:
        failures.append("SN_shape_data_not_validated")
    if not readable_bao:
        failures.append("BAO_distance_data_not_validated")
    if require_sn_full_covariance and not readable_sn_covariance:
        failures.append("SN_full_covariance_not_validated")
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "phase": phase,
        "readout": "dry_run_pass_data_candidates_validated" if data_ready else "dry_run_incomplete_missing_or_unvalidated_data",
        "stable_evidence_allowed": False,
        "scores_written": False,
        "data_ready_for_short_smoke": data_ready,
        "failures": failures,
        "next_action": "run short-smoke only after explicit SN, SN-covariance, and BAO data paths are validated" if data_ready else "provide explicit --sn-data, --sn-cov, --bao-data, and --bao-cov paths or add local data manifest",
    }


def run_dry_run(
    output_root: Path,
    sn_data: Path | None,
    bao_data: Path | None,
    sn_cov: Path | None,
    bao_cov: Path | None,
    sn_covariance_mode: str,
    sn_observable: str,
    include_calibrators: bool,
    sn_max_rows: int | None,
    bao_label: str,
    timestamp: str | None = None,
) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-cosmo-SN-BAO-closure-dryrun"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    require_sn_full_covariance = sn_covariance_mode == "full"
    data_rows = data_schema_rows(sn_data, bao_data, sn_cov, bao_cov, require_sn_full_covariance)
    config = {
        "phase": "dry-run",
        "frozen_before_fit": True,
        "scores_allowed": False,
        "requested_branch": {
            "sn_observable": sn_observable,
            "sn_covariance_mode": sn_covariance_mode,
            "sn_max_rows": sn_max_rows,
            "sn_rows": "full" if sn_max_rows is None else sn_max_rows,
            "sn_include_calibrators": include_calibrators,
            "bao_label": bao_label,
        },
        "manifest_sources": {
            "design_run": str(DESIGN_RUN),
            "empirical_manifest": str(MANIFEST_RUN),
        },
        "models": model_matrix(),
        "amplitude_policy": amplitude_policy(),
        "baseline_fairness": baseline_fairness(),
        "explicit_data_paths": {
            "SN_shape": str(sn_data) if sn_data else "",
            "SN_covariance": str(sn_cov) if sn_cov else "",
            "BAO_distances": str(bao_data) if bao_data else "",
            "BAO_covariance": str(bao_cov) if bao_cov else "",
        },
    }
    (run_dir / "run_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    write_csv(
        result_dir / "model_matrix.csv",
        model_matrix(),
        ["model_key", "role", "fixed_factors", "fitted_factors", "ablation_status", "claim_ceiling", "k_count_dry_run"],
    )
    write_csv(
        result_dir / "amplitude_policy.csv",
        amplitude_policy(),
        ["factor", "treatment", "prior", "best_fit", "edge_flag", "ablation_role"],
    )
    write_csv(
        result_dir / "baseline_fairness.csv",
        baseline_fairness(),
        ["baseline_rule", "requirement", "dry_run_status"],
    )
    write_csv(
        result_dir / "data_schema_report.csv",
        data_rows,
        ["dataset", "path", "explicit_path", "exists", "readable", "row_count", "columns", "sha256", "schema_status", "issue"],
    )
    write_csv(
        result_dir / "output_contract.csv",
        output_contract_rows(),
        ["artifact", "phase", "created_now"],
    )
    status = status_payload(run_dir, "dry-run", data_rows, require_sn_full_covariance)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def explicit_data_ready(
    sn_data: Path | None,
    bao_data: Path | None,
    sn_cov: Path | None,
    bao_cov: Path | None,
    sn_covariance_mode: str,
) -> tuple[bool, list[dict[str, Any]], list[str]]:
    if sn_data is None or bao_data is None:
        return False, [], ["explicit_SN_or_BAO_path_missing"]
    rows = data_schema_rows(sn_data, bao_data, sn_cov, bao_cov, sn_covariance_mode == "full")
    failures: list[str] = []
    if not any(row["dataset"] == "SN_shape" and row["schema_status"] == "schema_valid" for row in rows):
        failures.append("explicit_SN_schema_not_valid")
    if not any(row["dataset"] == "BAO_distances" and row["schema_status"] == "schema_valid" for row in rows):
        failures.append("explicit_BAO_schema_not_valid")
    if sn_covariance_mode == "full" and not any(
        row["dataset"] == "SN_covariance" and row["schema_status"] == "schema_valid" for row in rows
    ):
        failures.append("explicit_SN_covariance_schema_not_valid")
    if bao_cov is not None and not any(
        row["dataset"] == "BAO_covariance" and row["schema_status"] == "schema_valid" for row in rows
    ):
        failures.append("explicit_BAO_covariance_schema_not_valid")
    return not failures, rows, failures


def run_short_smoke(
    output_root: Path,
    sn_data: Path | None,
    bao_data: Path | None,
    bao_cov: Path | None,
    max_iter: int,
    sn_max_rows: int | None,
    cpl_w0_prior: tuple[float, float] | None,
    cpl_wa_prior: tuple[float, float] | None,
    include_mts_ablations: bool,
    sn_cov: Path | None,
    sn_covariance_mode: str,
    sn_observable: str,
    include_calibrators: bool,
    bao_label: str,
    timestamp: str | None = None,
) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-cosmo-SN-BAO-short-smoke"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    if bao_data is not None:
        inferred_cov = Path(str(bao_data).replace("_mean", "_cov"))
    else:
        inferred_cov = None
    selected_bao_cov = bao_cov or inferred_cov
    ready, schema_rows, schema_failures = explicit_data_ready(
        sn_data,
        bao_data,
        sn_cov,
        selected_bao_cov,
        sn_covariance_mode,
    )
    failures.extend(schema_failures)
    if selected_bao_cov is None or not selected_bao_cov.exists():
        failures.append("explicit_BAO_covariance_missing")
    if not ready or failures:
        status = {
            "script": str(Path(__file__).resolve()),
            "run_dir": str(run_dir),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "phase": "short-smoke",
            "readout": "short_smoke_aborted_explicit_data_not_validated",
            "stable_evidence_allowed": False,
            "scores_written": False,
            "failures": failures,
            "next_action": "rerun explicit dry-run with valid --sn-data --bao-data --bao-cov",
        }
        if schema_rows:
            write_csv(
                result_dir / "data_schema_report.csv",
                schema_rows,
                ["dataset", "path", "explicit_path", "exists", "readable", "row_count", "columns", "sha256", "schema_status", "issue"],
            )
        (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
        print(json.dumps(status, indent=2))
        return run_dir

    assert sn_data is not None
    assert bao_data is not None
    assert selected_bao_cov is not None

    if sn_covariance_mode == "full" and (sn_cov is None or not sn_cov.exists()):
        raise ValueError("SN full covariance requested but --sn-cov is missing or unreadable")

    sn = read_sn_data(
        sn_data,
        max_rows=sn_max_rows,
        covariance_path=sn_cov,
        covariance_mode=sn_covariance_mode,
        observable=sn_observable,
        include_calibrators=include_calibrators,
    )
    bao = read_bao_data(bao_data, selected_bao_cov)
    bao["label"] = bao_label
    prior_config: dict[str, tuple[float, float]] = {}
    if cpl_w0_prior is not None:
        prior_config["CPL.w0"] = cpl_w0_prior
    if cpl_wa_prior is not None:
        prior_config["CPL.wa"] = cpl_wa_prior
    required_models = ["LCDM", "wCDM", "CPL", "MTS_fixed_2over27_no_clock", "MTS_fixed_p3_u3quarter", "MTS_Bmem_zero"]
    if include_mts_ablations:
        required_models.extend(["MTS_fitted_p", "MTS_fitted_u3"])
    run_config = {
        "phase": "short-smoke",
        "scores_allowed": True,
        "claim_ceiling": "closure_testing_only",
        "sn_data": str(sn_data),
        "bao_data": str(bao_data),
        "bao_cov": str(selected_bao_cov),
        "bao_label": bao_label,
        "sn_cov": str(sn_cov) if sn_cov else "",
        "sn_covariance_mode": sn_covariance_mode,
        "sn_observable": sn_observable,
        "sn_include_calibrators": include_calibrators,
        "sn_rows_used": int(len(sn["z"])),
        "bao_rows_used": int(len(bao["rows"])),
        "max_iter": max_iter,
        "sn_max_rows": sn_max_rows,
        "prior_config": prior_config,
        "include_mts_ablations": include_mts_ablations,
        "priors": {row["model_key"]: model_priors(row["model_key"], prior_config) for row in model_matrix()},
        "models": model_matrix(),
        "scored_models": required_models,
        "amplitude_policy": amplitude_policy(),
        "baseline_fairness": baseline_fairness(),
    }
    (run_dir / "run_config.json").write_text(json.dumps(run_config, indent=2), encoding="utf-8")
    write_csv(
        result_dir / "data_schema_report.csv",
        schema_rows,
        ["dataset", "path", "explicit_path", "exists", "readable", "row_count", "columns", "sha256", "schema_status", "issue"],
    )

    scores: list[dict[str, Any]] = []
    for model_key in required_models:
        scores.append(score_model(model_key, sn, bao, max_iter=max_iter, prior_config=prior_config))

    fit_rows = fit_summary_rows(scores)
    edge_rows = [edge_row for score in scores for edge_row in score["edge_rows"]]
    baseline_rows = baseline_comparison_rows(scores)
    residual_output_rows = residual_rows(scores, sn, bao)
    amplitude_rows = scored_amplitude_policy_rows(scores)

    write_csv(
        result_dir / "fit_summary.csv",
        fit_rows,
        [
            "model",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "dof",
            "k",
            "n",
            "AIC",
            "BIC",
            "convergence",
            "prior_edge_flag",
            "claim_ceiling",
            "optimizer_message",
        ],
    )
    write_csv(
        result_dir / "baseline_comparison.csv",
        baseline_rows,
        ["model", "reference_baseline", "delta_chi2", "delta_AIC", "delta_BIC", "same_data", "same_nuisance", "same_calibration"],
    )
    write_csv(
        result_dir / "residuals.csv",
        residual_output_rows,
        ["dataset", "model", "observable", "coordinate", "observed", "predicted", "residual", "sigma_or_cov_block", "row_index"],
    )
    write_csv(
        result_dir / "prior_edge_table.csv",
        edge_rows,
        ["model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(
        result_dir / "amplitude_policy.csv",
        amplitude_rows,
        ["factor", "treatment", "prior", "best_fit", "edge_flag", "ablation_role"],
    )

    unstable = any(row["prior_edge_flag"] in {True, "True", "true"} for row in fit_rows)
    failed_convergence = [row["model"] for row in fit_rows if str(row["convergence"]) != "True"]
    if failed_convergence:
        failures.append("nonconverged_models:" + ",".join(failed_convergence))
    if unstable:
        failures.append("prior_edge_flags_present")
    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "phase": "short-smoke",
        "readout": "short_smoke_scores_written_unstable" if failures else "short_smoke_scores_written_no_edge_flags",
        "stable_evidence_allowed": False,
        "scores_written": True,
        "failures": failures,
        "next_action": "inspect CSVs; do not claim evidence; run ablations/robustness only after review",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", default="dry-run", choices=["dry-run", "short-smoke"])
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--sn-data", type=Path, default=None, help="Explicit SN shape data path.")
    parser.add_argument("--sn-cov", type=Path, default=None, help="Explicit Pantheon+ SN covariance path for --sn-covariance-mode full.")
    parser.add_argument("--sn-covariance-mode", choices=["diagonal", "full"], default="diagonal")
    parser.add_argument("--sn-observable", choices=["mu-sh0es", "mb-corr"], default="mu-sh0es")
    parser.add_argument("--include-calibrators", action="store_true", help="Include Cepheid calibrator-host SNe; default excludes them.")
    parser.add_argument("--bao-data", type=Path, default=None, help="Explicit BAO data path.")
    parser.add_argument("--bao-cov", type=Path, default=None, help="Explicit BAO covariance path.")
    parser.add_argument("--bao-label", default="BAO_primary", help="Label written to residual rows for the BAO release/split.")
    parser.add_argument("--max-iter", type=int, default=120)
    parser.add_argument("--sn-max-rows", type=int, default=250, help="Maximum SN rows to use; set 0 for the full selected SN sample.")
    parser.add_argument("--cpl-wa-lower", type=float, default=None, help="Override lower bound for CPL wa.")
    parser.add_argument("--cpl-wa-upper", type=float, default=None, help="Override upper bound for CPL wa.")
    parser.add_argument("--cpl-w0-lower", type=float, default=None, help="Override lower bound for CPL w0.")
    parser.add_argument("--cpl-w0-upper", type=float, default=None, help="Override upper bound for CPL w0.")
    parser.add_argument("--include-mts-ablations", action="store_true", help="Also score MTS_fitted_p and MTS_fitted_u3.")
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix for reproducible run directories.")
    args = parser.parse_args()
    cpl_wa_prior = None
    cpl_w0_prior = None
    if args.cpl_w0_lower is not None or args.cpl_w0_upper is not None:
        if args.cpl_w0_lower is None or args.cpl_w0_upper is None:
            parser.error("--cpl-w0-lower and --cpl-w0-upper must be provided together")
        if args.cpl_w0_lower >= args.cpl_w0_upper:
            parser.error("--cpl-w0-lower must be less than --cpl-w0-upper")
        cpl_w0_prior = (args.cpl_w0_lower, args.cpl_w0_upper)
    if args.cpl_wa_lower is not None or args.cpl_wa_upper is not None:
        if args.cpl_wa_lower is None or args.cpl_wa_upper is None:
            parser.error("--cpl-wa-lower and --cpl-wa-upper must be provided together")
        if args.cpl_wa_lower >= args.cpl_wa_upper:
            parser.error("--cpl-wa-lower must be less than --cpl-wa-upper")
        cpl_wa_prior = (args.cpl_wa_lower, args.cpl_wa_upper)
    sn_max_rows = None if args.sn_max_rows == 0 else args.sn_max_rows
    if args.phase == "dry-run":
        run_dry_run(
            args.output_root,
            args.sn_data,
            args.bao_data,
            args.sn_cov,
            args.bao_cov,
            args.sn_covariance_mode,
            args.sn_observable,
            args.include_calibrators,
            sn_max_rows,
            args.bao_label,
            args.timestamp,
        )
    else:
        run_short_smoke(
            args.output_root,
            args.sn_data,
            args.bao_data,
            args.bao_cov,
            args.max_iter,
            sn_max_rows,
            cpl_w0_prior,
            cpl_wa_prior,
            args.include_mts_ablations,
            args.sn_cov,
            args.sn_covariance_mode,
            args.sn_observable,
            args.include_calibrators,
            args.bao_label,
            args.timestamp,
        )


if __name__ == "__main__":
    main()
