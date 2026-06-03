#!/usr/bin/env python3
"""Source-lock and preflight official no-clock lead inputs without scoring models."""

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
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
COSMOLOGY_DATA = FORMALIZATION_WORKBENCH / "data" / "cosmology"

PANTHEON_DIR = COSMOLOGY_DATA / "pantheon_plus"
PANTHEON_DAT = PANTHEON_DIR / "Pantheon+SH0ES.dat"
PANTHEON_COV_SYS = PANTHEON_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
PANTHEON_COV_STAT = PANTHEON_DIR / "Pantheon+SH0ES_STATONLY.cov"
PANTHEON_README = PANTHEON_DIR / "README"

DESI_DR2_MEAN = COSMOLOGY_DATA / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
DESI_DR2_COV = COSMOLOGY_DATA / "desi_dr2_bao" / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
DESI_DR1_MEAN = COSMOLOGY_DATA / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_mean.txt"
DESI_DR1_COV = COSMOLOGY_DATA / "desi_dr1_bao" / "desi_2024_gaussian_bao_ALL_GCcomb_cov.txt"

CC_DIR = COSMOLOGY_DATA / "cosmic_chronometers"
CC32_CSV = CC_DIR / "Hz.csv"
CC32_RAW = CC_DIR / "data_CC_unibo_raw.dat"
CC_SOURCE_METADATA = CC_DIR / "source_metadata.json"
CC15_DIR = CC_DIR / "covariance_branch"
CC15_CSV = CC15_DIR / "Hz_CC_Moresco15_BC03.csv"
CC15_ROW_LOCK = CC15_DIR / "row_lock_manifest.json"
CC15_COVARIANCES = {
    "diagonal_total_error": CC15_DIR / "covariance_diagonal_total_error.csv",
    "suggested": CC15_DIR / "covariance_suggested.csv",
    "conservative": CC15_DIR / "covariance_conservative.csv",
    "extra_conservative": CC15_DIR / "covariance_extra_conservative.csv",
    "nonstat_systematic_only": CC15_DIR / "covariance_nonstat_systematic_only.csv",
}

GROWTH_DIR = COSMOLOGY_DATA / "growth_CMB"
GROWTH_SOURCE_MANIFEST = GROWTH_DIR / "source_manifest.csv"
PLANCK_VECTOR = GROWTH_DIR / "planck2018_distance_priors" / "planck2018_distance_prior_vector.csv"
PLANCK_COV = GROWTH_DIR / "planck2018_distance_priors" / "planck2018_distance_prior_covariance.csv"
DOWNLOAD_MANIFEST = COSMOLOGY_DATA / "download-manifest.json"

STATUS_PASS = "no_clock_official_source_refresh_preflight_passed"
STATUS_FAIL = "no_clock_official_source_refresh_preflight_failed"
CLAIM_CEILING = "source_refresh_preflight_only_no_model_scoring_or_theory_promotion"


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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.endswith("no_clock_official_source_refresh.py"):
        return "current source refresh runner"
    if name.startswith("169-"):
        return "refresh plan source"
    if name == "download-manifest.json":
        return "SN/BAO source hash manifest"
    if name == "source_manifest.csv":
        return "growth/CMB source hash manifest"
    if "Pantheon" in name or name == "README":
        return "Pantheon+ SN source asset"
    if "desi" in name.lower():
        return "DESI BAO source asset"
    if "Hz" in name or "covariance" in name:
        return "cosmic chronometer source asset"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "169-no-clock-lead-official-likelihood-refresh-plan.md",
        DOWNLOAD_MANIFEST,
        GROWTH_SOURCE_MANIFEST,
        PANTHEON_DAT,
        PANTHEON_COV_SYS,
        PANTHEON_COV_STAT,
        PANTHEON_README,
        DESI_DR2_MEAN,
        DESI_DR2_COV,
        DESI_DR1_MEAN,
        DESI_DR1_COV,
        CC32_CSV,
        CC32_RAW,
        CC_SOURCE_METADATA,
        CC15_CSV,
        CC15_ROW_LOCK,
        *CC15_COVARIANCES.values(),
        PLANCK_VECTOR,
        PLANCK_COV,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def normalize_hash(value: Any) -> str:
    return str(value or "").strip().lower()


def source_hash_lock_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if DOWNLOAD_MANIFEST.exists():
        for entry in json.loads(DOWNLOAD_MANIFEST.read_text(encoding="utf-8-sig")):
            path = Path(entry["file"])
            expected = normalize_hash(entry.get("sha256"))
            rows.append(hash_row("download-manifest.json", entry.get("source", ""), entry.get("url", ""), path, expected))
    if GROWTH_SOURCE_MANIFEST.exists():
        for entry in read_csv_rows(GROWTH_SOURCE_MANIFEST):
            rows.append(
                hash_row(
                    "growth_CMB/source_manifest.csv",
                    f"{entry.get('source_id', '')}:{entry.get('kind', '')}",
                    entry.get("remote_url", ""),
                    Path(entry["local_path"]),
                    normalize_hash(entry.get("sha256")),
                )
            )
    cc_metadata = [
        ("CC32_full_table", "https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat", CC32_CSV),
        ("CC32_raw_source", "https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat", CC32_RAW),
        ("CC32_source_metadata", "https://cluster.difa.unibo.it/astro/CC_data/", CC_SOURCE_METADATA),
        ("CC15_BC03_branch_table", "https://gitlab.com/mmoresco/CCcovariance", CC15_CSV),
        ("CC15_row_lock_manifest", "https://gitlab.com/mmoresco/CCcovariance", CC15_ROW_LOCK),
    ]
    cc_metadata.extend((f"CC15_covariance_{label}", "https://gitlab.com/mmoresco/CCcovariance", path) for label, path in CC15_COVARIANCES.items())
    for source_key, url, path in cc_metadata:
        rows.append(hash_row("cosmic_chronometer_current_hash", source_key, url, path, ""))
    return rows


def hash_row(manifest: str, source_key: str, url: str, path: Path, expected_hash: str) -> dict[str, Any]:
    exists = path.exists()
    actual = sha256_file(path).lower() if exists and path.is_file() else ""
    if not exists:
        status = "missing"
    elif expected_hash:
        status = "pass" if actual == expected_hash else "hash_mismatch"
    else:
        status = "recorded_no_expected_hash"
    return {
        "manifest": manifest,
        "source_key": source_key,
        "url": url,
        "local_path": str(path),
        "exists": "yes" if exists else "no",
        "expected_sha256": expected_hash,
        "actual_sha256": actual,
        "bytes": path.stat().st_size if exists else "",
        "status": status,
    }


def read_pantheon_rows() -> list[dict[str, str]]:
    with PANTHEON_DAT.open("r", encoding="utf-8-sig") as handle:
        header = handle.readline().strip().split()
        return [dict(zip(header, line.strip().split(), strict=False)) for line in handle if line.strip()]


def numeric(value: Any, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def row_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(sn_row_manifest())
    rows.extend(bao_row_manifest("DESI_DR2_BAO", DESI_DR2_MEAN, "primary_release"))
    rows.extend(bao_row_manifest("DESI_DR1_BAO", DESI_DR1_MEAN, "release_sensitivity"))
    rows.extend(hz_row_manifest("CC32_full_diagonal_sensitivity", CC32_CSV, "diagonal_sensitivity"))
    rows.extend(hz_row_manifest("CC15_BC03_covariance_primary", CC15_CSV, "primary_covariance_branch"))
    rows.extend(growth_row_manifest())
    rows.extend(planck_row_manifest())
    return rows


def sn_row_manifest() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_pantheon_rows()):
        is_calibrator = str(row.get("IS_CALIBRATOR", "0")) == "1"
        used_hf = str(row.get("USED_IN_SH0ES_HF", "0")) == "1"
        rows.append(
            {
                "arena": "SN",
                "dataset": "PantheonPlusSH0ES",
                "row_index": index,
                "row_id": row.get("CID", f"SN_{index}"),
                "z": row.get("zHD", ""),
                "observable": "m_b_corr",
                "value": row.get("m_b_corr", ""),
                "uncertainty": row.get("m_b_corr_err_DIAG", ""),
                "include_flag": "include_noSH0ES_shape" if not is_calibrator else "exclude_calibrator_noSH0ES_shape",
                "source_path": str(PANTHEON_DAT),
                "notes": f"IS_CALIBRATOR={int(is_calibrator)}; USED_IN_SH0ES_HF={int(used_hf)}; full covariance required",
            }
        )
    return rows


def bao_row_manifest(dataset: str, mean_path: Path, role: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with mean_path.open("r", encoding="utf-8-sig") as handle:
        for row_index, line in enumerate(line for line in handle if line.strip() and not line.lstrip().startswith("#")):
            parts = line.split()
            rows.append(
                {
                    "arena": "BAO",
                    "dataset": dataset,
                    "row_index": row_index,
                    "row_id": f"{dataset}_{row_index}",
                    "z": parts[0],
                    "observable": parts[2] if len(parts) >= 3 else "",
                    "value": parts[1] if len(parts) >= 2 else "",
                    "uncertainty": "",
                    "include_flag": role,
                    "source_path": str(mean_path),
                    "notes": "covariance-owned uncertainty; rd/rs convention must be documented in scorer",
                }
            )
    return rows


def hz_row_manifest(dataset: str, path: Path, role: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv_rows(path)):
        rows.append(
            {
                "arena": "Hz",
                "dataset": dataset,
                "row_index": index,
                "row_id": row.get("branch_index", index),
                "z": row.get("z", ""),
                "observable": "H_z",
                "value": row.get("H", ""),
                "uncertainty": row.get("sigma", ""),
                "include_flag": role,
                "source_path": str(path),
                "notes": row.get("reference", ""),
            }
        )
    return rows


def growth_row_manifest() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not GROWTH_SOURCE_MANIFEST.exists():
        return rows
    for entry in read_csv_rows(GROWTH_SOURCE_MANIFEST):
        local_path = Path(entry["local_path"])
        kind = entry.get("kind", "")
        if "cov" in local_path.stem.lower():
            continue
        if kind not in {"primary_growth", "robustness_growth", "grid_growth_candidate"}:
            continue
        if kind == "grid_growth_candidate":
            rows.append(
                {
                    "arena": "growth_RSD",
                    "dataset": entry.get("item_id", local_path.stem),
                    "row_index": 0,
                    "row_id": "ELG_grid_file",
                    "z": "",
                    "observable": "grid_likelihood",
                    "value": "",
                    "uncertainty": "",
                    "include_flag": "grid_parser_required_not_gaussian_vector",
                    "source_path": str(local_path),
                    "notes": "ELG grid is a separate non-Gaussian likelihood branch",
                }
            )
            continue
        if not local_path.exists():
            continue
        with local_path.open("r", encoding="utf-8-sig") as handle:
            data_lines = [line for line in handle if line.strip() and not line.lstrip().startswith("#")]
        for row_index, line in enumerate(data_lines):
            parts = line.split()
            rows.append(
                {
                    "arena": "growth_RSD",
                    "dataset": entry.get("item_id", local_path.stem),
                    "row_index": row_index,
                    "row_id": f"{local_path.stem}_{row_index}",
                    "z": parts[0] if len(parts) >= 1 else "",
                    "observable": parts[2] if len(parts) >= 3 else "",
                    "value": parts[1] if len(parts) >= 2 else "",
                    "uncertainty": "",
                    "include_flag": kind,
                    "source_path": str(local_path),
                    "notes": "covariance-owned uncertainty; do not combine BAO-plus and full-shape-only as independent evidence",
                }
            )
    return rows


def planck_row_manifest() -> list[dict[str, Any]]:
    if not PLANCK_VECTOR.exists():
        return []
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(read_csv_rows(PLANCK_VECTOR)):
        key = row.get("parameter") or row.get("name") or row.get("label") or f"planck_prior_{index}"
        value = row.get("value") or row.get("mean") or next((value for value in row.values() if value), "")
        rows.append(
            {
                "arena": "CMB_diagnostic",
                "dataset": "Planck2018_distance_priors",
                "row_index": index,
                "row_id": key,
                "z": "",
                "observable": key,
                "value": value,
                "uncertainty": "",
                "include_flag": "diagnostic_only_no_CMB_promotion",
                "source_path": str(PLANCK_VECTOR),
                "notes": "compressed distance prior only; not a Boltzmann-level MTS CMB likelihood",
            }
        )
    return rows


def covariance_manifest_rows(row_counts: dict[tuple[str, str], int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        sn_covariance_row("PantheonPlusSH0ES_STAT+SYS", PANTHEON_COV_SYS, row_counts.get(("SN", "PantheonPlusSH0ES"), 0)),
        sn_covariance_row("PantheonPlusSH0ES_STATONLY", PANTHEON_COV_STAT, row_counts.get(("SN", "PantheonPlusSH0ES"), 0)),
        matrix_covariance_row("DESI_DR2_BAO", DESI_DR2_COV, row_counts.get(("BAO", "DESI_DR2_BAO"), 0), "whitespace_matrix"),
        matrix_covariance_row("DESI_DR1_BAO", DESI_DR1_COV, row_counts.get(("BAO", "DESI_DR1_BAO"), 0), "whitespace_matrix"),
    ]
    for label, path in CC15_COVARIANCES.items():
        rows.append(csv_covariance_row(f"CC15_BC03_{label}", path, row_counts.get(("Hz", "CC15_BC03_covariance_primary"), 0)))
    rows.extend(growth_covariance_rows(row_counts))
    if PLANCK_COV.exists():
        rows.append(planck_covariance_row("Planck2018_distance_priors", PLANCK_COV, row_counts.get(("CMB_diagnostic", "Planck2018_distance_priors"), 0)))
    return rows


def sn_covariance_row(dataset: str, path: Path, expected_rows: int) -> dict[str, Any]:
    if not path.exists():
        return covariance_row(dataset, "SN", path, expected_rows, "", "", "", "", "missing")
    try:
        values = np.loadtxt(path)
        n_rows = int(values[0])
        matrix_values = values[1:]
        complete = matrix_values.size == n_rows * n_rows
        diag_min = ""
        diag_max = ""
        symmetry = ""
        condition = "skipped_large_full_covariance"
        if complete:
            matrix = matrix_values.reshape((n_rows, n_rows))
            diagonal = np.diag(matrix)
            diag_min = float(np.min(diagonal))
            diag_max = float(np.max(diagonal))
            symmetry = float(np.max(np.abs(matrix - matrix.T)))
        status = "pass" if complete and n_rows == expected_rows and (symmetry == "" or float(symmetry) < 1.0e-7) else "fail"
        return covariance_row(dataset, "SN", path, expected_rows, n_rows, f"{n_rows}x{n_rows}", symmetry, condition, status, diag_min, diag_max)
    except Exception as exc:
        return covariance_row(dataset, "SN", path, expected_rows, "", "", "", "", "fail", issue=str(exc))


def matrix_covariance_row(dataset: str, path: Path, expected_rows: int, format_label: str) -> dict[str, Any]:
    if not path.exists():
        return covariance_row(dataset, "matrix", path, expected_rows, "", "", "", "", "missing")
    try:
        matrix = np.loadtxt(path)
        return covariance_matrix_payload(dataset, format_label, path, expected_rows, matrix)
    except Exception as exc:
        return covariance_row(dataset, format_label, path, expected_rows, "", "", "", "", "fail", issue=str(exc))


def csv_covariance_row(dataset: str, path: Path, expected_rows: int) -> dict[str, Any]:
    if not path.exists():
        return covariance_row(dataset, "csv_matrix", path, expected_rows, "", "", "", "", "missing")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            matrix = np.asarray([[float(value) for value in row[1:]] for row in reader], dtype=float)
        return covariance_matrix_payload(dataset, "csv_matrix", path, expected_rows or len(header) - 1, matrix)
    except Exception as exc:
        return covariance_row(dataset, "csv_matrix", path, expected_rows, "", "", "", "", "fail", issue=str(exc))


def planck_covariance_row(dataset: str, path: Path, expected_rows: int) -> dict[str, Any]:
    if not path.exists():
        return covariance_row(dataset, "long_form_planck_covariance", path, expected_rows, "", "", "", "", "missing")
    try:
        rows = read_csv_rows(path)
        default_rows = [row for row in rows if str(row.get("default_for_C0", "")).lower() == "true"]
        row_set = {(row["model"], row["row_parameter"]) for row in rows}
        col_set = {(row["model"], row["col_parameter"]) for row in rows}
        status = "pass" if rows and row_set == col_set else "fail"
        issue = "" if status == "pass" else "row/column parameter coverage mismatch"
        return covariance_row(
            dataset,
            "long_form_planck_covariance",
            path,
            expected_rows,
            len(rows),
            f"long_form_entries={len(rows)};default_entries={len(default_rows)}",
            "",
            "not_matrix_form",
            status,
            issue=issue,
        )
    except Exception as exc:
        return covariance_row(dataset, "long_form_planck_covariance", path, expected_rows, "", "", "", "", "fail", issue=str(exc))


def growth_covariance_rows(row_counts: dict[tuple[str, str], int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not GROWTH_SOURCE_MANIFEST.exists():
        return rows
    for entry in read_csv_rows(GROWTH_SOURCE_MANIFEST):
        path = Path(entry["local_path"])
        if entry.get("kind", "") not in {"primary_growth", "robustness_growth"}:
            continue
        if "cov" not in path.stem.lower() or not path.exists():
            continue
        vector_key = path.stem.replace("_covtot", "")
        expected = next((count for (arena, dataset), count in row_counts.items() if arena == "growth_RSD" and vector_key in dataset), 0)
        rows.append(matrix_covariance_row(entry.get("item_id", path.stem), path, expected, "growth_whitespace_matrix"))
    return rows


def covariance_matrix_payload(dataset: str, arena: str, path: Path, expected_rows: int, matrix: np.ndarray) -> dict[str, Any]:
    if matrix.ndim != 2:
        return covariance_row(dataset, arena, path, expected_rows, "", str(matrix.shape), "", "", "fail", issue="matrix is not 2D")
    n_rows, n_cols = matrix.shape
    symmetry = float(np.max(np.abs(matrix - matrix.T))) if n_rows == n_cols and n_rows > 0 else ""
    diagonal = np.diag(matrix) if n_rows == n_cols and n_rows > 0 else np.asarray([], dtype=float)
    diag_min = float(np.min(diagonal)) if diagonal.size else ""
    diag_max = float(np.max(diagonal)) if diagonal.size else ""
    condition = float(np.linalg.cond(matrix)) if n_rows == n_cols and 0 < n_rows <= 200 else "skipped_large_or_non_square"
    expected_ok = expected_rows in {0, n_rows}
    status = "pass" if n_rows == n_cols and expected_ok and (symmetry == "" or float(symmetry) < 1.0e-8) and np.all(np.isfinite(matrix)) else "fail"
    return covariance_row(dataset, arena, path, expected_rows, n_rows, f"{n_rows}x{n_cols}", symmetry, condition, status, diag_min, diag_max)


def covariance_row(
    dataset: str,
    arena: str,
    path: Path,
    expected_rows: Any,
    n_rows: Any,
    shape: Any,
    symmetry: Any,
    condition: Any,
    status: str,
    diag_min: Any = "",
    diag_max: Any = "",
    issue: str = "",
) -> dict[str, Any]:
    return {
        "arena": arena,
        "dataset": dataset,
        "covariance_path": str(path),
        "exists": "yes" if path.exists() else "no",
        "expected_rows": expected_rows,
        "n_rows": n_rows,
        "shape": shape,
        "symmetry_max_abs": symmetry,
        "condition_number": condition,
        "diag_min": diag_min,
        "diag_max": diag_max,
        "status": status,
        "issue": issue,
    }


def row_count_index(rows: list[dict[str, Any]]) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (str(row["arena"]), str(row["dataset"]))
        counts[key] = counts.get(key, 0) + 1
    return counts


def branch_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "LCDM",
            "role": "baseline",
            "fixed_inputs": "standard flat/selected baseline form",
            "fitted_inputs": "Omega_m plus same nuisance/calibration freedoms as MTS",
            "included_in_lead_refresh": "yes",
            "sidecar_policy": "not_applicable",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "wCDM",
            "role": "baseline",
            "fixed_inputs": "constant w extension",
            "fitted_inputs": "Omega_m,w plus same nuisance/calibration freedoms as MTS",
            "included_in_lead_refresh": "yes",
            "sidecar_policy": "not_applicable",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "CPL",
            "role": "baseline",
            "fixed_inputs": "w0-wa extension",
            "fitted_inputs": "Omega_m,w0,wa plus same nuisance/calibration freedoms as MTS",
            "included_in_lead_refresh": "yes",
            "sidecar_policy": "not_applicable",
            "claim_ceiling": "baseline",
        },
        {
            "branch": "MTS_2over27_no_clock_u3quarter",
            "role": "lead_branch",
            "fixed_inputs": "B_mem=2/27; u3=1/4; no global clock; no pair projection",
            "fitted_inputs": "Omega_m plus same nuisance/calibration freedoms as baselines",
            "included_in_lead_refresh": "yes",
            "sidecar_policy": "no_pair_ruler_projection",
            "claim_ceiling": CLAIM_CEILING,
        },
        {
            "branch": "MTS_Bmem_zero",
            "role": "negative_control",
            "fixed_inputs": "B_mem=0; no global clock; no pair projection",
            "fitted_inputs": "Omega_m plus same nuisance/calibration freedoms as baselines",
            "included_in_lead_refresh": "yes",
            "sidecar_policy": "no_pair_ruler_projection",
            "claim_ceiling": "control_only",
        },
        {
            "branch": "MTS_pair_ruler_half_kernel",
            "role": "frozen_sidecar",
            "fixed_inputs": "T=(B/8)F(1-2e^-N); S=(B/12)(1-e^-2N)",
            "fitted_inputs": "none in lead-lane refresh",
            "included_in_lead_refresh": "no",
            "sidecar_policy": "excluded_until_parent_owned",
            "claim_ceiling": "sidecar_closure_only",
        },
    ]


def nuisance_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "SN",
            "nuisance": "SN_offset_or_absolute_magnitude",
            "policy": "analytic/profiled identically for LCDM/wCDM/CPL/MTS",
            "evidence_required_next": "nuisance_policy_applied_in_fit_summary",
        },
        {
            "arena": "BAO",
            "nuisance": "BAO_alpha_or_rd_rs_scale",
            "policy": "same alpha/convention for every branch; no branch-specific ruler rescue",
            "evidence_required_next": "BAO_alpha listed for every scored branch",
        },
        {
            "arena": "Hz",
            "nuisance": "H0_or_expansion_scale",
            "policy": "same H0/calibration treatment for every branch",
            "evidence_required_next": "Hz branch manifest and prior table",
        },
        {
            "arena": "growth_RSD",
            "nuisance": "sigma8_0",
            "policy": "same sigma8-only profiling if using GR-proxy growth",
            "evidence_required_next": "growth fit_summary and jackknife_scorecard",
        },
        {
            "arena": "all",
            "nuisance": "prior_edges",
            "policy": "edge hits demote evidence for every model, including baselines",
            "evidence_required_next": "prior_edge_table.csv",
        },
    ]


def dry_run_command_rows() -> list[dict[str, Any]]:
    py = WORK_DIR / ".venv-score" / "Scripts" / "python.exe"
    source_script = WORK_DIR / "scripts" / "no_clock_official_source_refresh.py"
    score_script = WORK_DIR / "scripts" / "no_clock_official_likelihood_refresh.py"
    return [
        {
            "step": 1,
            "label": "repeat_preflight",
            "command": f'& "{py}" "{source_script}" --timestamp <timestamp>',
            "purpose": "rebuild source_hash_lock,row_manifest,covariance_manifest before fitting",
            "long_run": "no",
        },
        {
            "step": 2,
            "label": "manifest_only_fit_guard",
            "command": f'& "{py}" "{score_script}" --mode manifest-only --assert-no-sidecar --timestamp <timestamp>',
            "purpose": "prove branch/nuisance/row contracts before scoring",
            "long_run": "no",
        },
        {
            "step": 3,
            "label": "single_arena_reproduction",
            "command": f'& "{py}" "{score_script}" --mode reproduce --timestamp <timestamp>',
            "purpose": "reproduce existing signs before joint refresh",
            "long_run": "maybe",
        },
        {
            "step": 4,
            "label": "baseline_fair_refresh",
            "command": f'& "{py}" "{score_script}" --mode full-refresh --timestamp <timestamp>',
            "purpose": "score no-clock MTS vs LCDM/wCDM/CPL with identical punches",
            "long_run": "yes_use_VS_Code_marker_workflow",
        },
    ]


def preflight_gate_rows(
    source_hashes: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    covariances: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_hashes if row["status"] == "missing"]
    hash_mismatches = [row for row in source_hashes if row["status"] == "hash_mismatch"]
    covariance_failures = [row for row in covariances if row["status"] != "pass"]
    sidecar_included = [row for row in branches if row["branch"] == "MTS_pair_ruler_half_kernel" and row["included_in_lead_refresh"] == "yes"]
    row_counts = row_count_index(rows)
    required_row_keys = [
        ("SN", "PantheonPlusSH0ES"),
        ("BAO", "DESI_DR2_BAO"),
        ("Hz", "CC15_BC03_covariance_primary"),
    ]
    missing_required_rows = [f"{arena}:{dataset}" for arena, dataset in required_row_keys if row_counts.get((arena, dataset), 0) == 0]
    if not any(row["arena"] == "growth_RSD" and row["include_flag"] == "primary_growth" for row in rows):
        missing_required_rows.append("growth_RSD:primary_growth")
    return [
        {
            "gate": "source_files_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing={len(missing_sources)}",
        },
        {
            "gate": "expected_hashes_match",
            "status": "pass" if not hash_mismatches else "fail",
            "evidence": f"hash_mismatches={len(hash_mismatches)}; recorded_no_expected_hash={sum(1 for row in source_hashes if row['status'] == 'recorded_no_expected_hash')}",
        },
        {
            "gate": "required_row_manifests_present",
            "status": "pass" if not missing_required_rows else "fail",
            "evidence": f"total_rows={len(rows)}; missing_required={';'.join(missing_required_rows)}",
        },
        {
            "gate": "covariance_preflight",
            "status": "pass" if not covariance_failures else "fail",
            "evidence": f"covariance_failures={len(covariance_failures)}; covariance_rows={len(covariances)}",
        },
        {
            "gate": "sidecar_excluded_from_lead_refresh",
            "status": "pass" if not sidecar_included else "fail",
            "evidence": "MTS_pair_ruler_half_kernel included_in_lead_refresh=no",
        },
        {
            "gate": "no_model_scoring",
            "status": "pass",
            "evidence": "runner produced manifests only; no chi2/AIC/BIC model scoring",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row for row in gates if row["status"] != "pass"]
    status = STATUS_PASS if not failed else STATUS_FAIL
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"failed_gates={len(failed)}",
        },
        {
            "item": "lead_branch",
            "verdict": "MTS_2over27_no_clock_u3quarter",
            "evidence": "branch manifest keeps no-clock as lead",
        },
        {
            "item": "sidecar_policy",
            "verdict": "excluded_from_lead_refresh",
            "evidence": "half-kernel remains closure-only from checkpoint 168",
        },
        {
            "item": "fit_status",
            "verdict": "not_run_by_design",
            "evidence": "source refresh/preflight only",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no theory/CMB/local-GR/parent-action promotion",
        },
        {
            "item": "next_target",
            "verdict": "171-no-clock-manifest-only-fit-guard.md",
            "evidence": "implement scorer manifest guard before reproduction or long refresh",
        },
    ]


def run_preflight(output_root: Path, timestamp: str | None, dry_run: bool) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = "dryrun" if dry_run else "no-clock-official-source-refresh"
    run_dir = output_root / f"{run_stamp}-{suffix}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    source_hashes = source_hash_lock_rows()
    rows = row_manifest_rows()
    row_counts = row_count_index(rows)
    covariances = covariance_manifest_rows(row_counts)
    branches = branch_manifest_rows()
    nuisances = nuisance_policy_rows()
    commands = dry_run_command_rows()
    gates = preflight_gate_rows(source_hashes, rows, covariances, branches)
    decisions = decision_rows(gates)
    status = decisions[0]["verdict"]

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "dry_run": dry_run,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_policy": "excluded_from_lead_refresh",
            "model_scoring": "not_run",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(results_dir / "source_hash_lock.csv", source_hashes, ["manifest", "source_key", "url", "local_path", "exists", "expected_sha256", "actual_sha256", "bytes", "status"])
    write_csv(results_dir / "row_manifest.csv", rows, ["arena", "dataset", "row_index", "row_id", "z", "observable", "value", "uncertainty", "include_flag", "source_path", "notes"])
    write_csv(results_dir / "covariance_manifest.csv", covariances, ["arena", "dataset", "covariance_path", "exists", "expected_rows", "n_rows", "shape", "symmetry_max_abs", "condition_number", "diag_min", "diag_max", "status", "issue"])
    write_csv(results_dir / "branch_manifest.csv", branches, ["branch", "role", "fixed_inputs", "fitted_inputs", "included_in_lead_refresh", "sidecar_policy", "claim_ceiling"])
    write_csv(results_dir / "nuisance_policy.csv", nuisances, ["arena", "nuisance", "policy", "evidence_required_next"])
    write_csv(results_dir / "dry_run_command_queue.csv", commands, ["step", "label", "command", "purpose", "long_run"])
    write_csv(results_dir / "preflight_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": status,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_policy": "excluded_from_lead_refresh",
            "model_scoring": "not_run",
            "source_hash_rows": len(source_hashes),
            "row_manifest_rows": len(rows),
            "covariance_manifest_rows": len(covariances),
            "failed_gates": [row["gate"] for row in gates if row["status"] != "pass"],
            "next_target": "171-no-clock-manifest-only-fit-guard.md",
            "generated": [
                "source_register.csv",
                "source_hash_lock.csv",
                "row_manifest.csv",
                "covariance_manifest.csv",
                "branch_manifest.csv",
                "nuisance_policy.csv",
                "dry_run_command_queue.csv",
                "preflight_gates.csv",
                "decision.csv",
            ],
        },
    )
    marker = "DONE.txt" if status == STATUS_PASS else "FAILED.txt"
    (run_dir / marker).write_text(f"{status}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Write preflight artifacts with a dry-run run-name suffix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_preflight(args.output_root, args.timestamp, args.dry_run))


if __name__ == "__main__":
    main()
