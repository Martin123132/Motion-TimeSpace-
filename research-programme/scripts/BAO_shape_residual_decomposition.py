"""Decompose BAO shape residuals by observable and redshift row.

This is a diagnostic audit, not a repair model.  It compares late-only,
joint-tied-alpha, and CMB-compatible/free-alpha BAO residual shapes using the
same DESI DR2 rows and covariance.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402
import locked_2over27_joint_late_CMB_calibration_runner as joint  # noqa: E402

T1_RUN = RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke"
T7_RUN = RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness"
CMB_RUN = RUNS_ROOT / "20260531-161215-locked-2over27-CMB-distance-score"
JOINT_RUN = RUNS_ROOT / "20260531-164201-locked-2over27-joint-late-CMB-score"
ROUTE_RUN = RUNS_ROOT / "20260531-173000-CMB-bridge-demotion-and-next-test-route"

LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
PRIMARY_MODEL = "MTS_locked_2over27"
PRIMARY_FAILED_PRIOR_TABLE = "LCDM"
PRIMARY_FAILED_SCORE_MODE = "strict_full4"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def maybe_float(value: str | float | int | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        T1_RUN / "run_config.json",
        T1_RUN / "results" / "fit_summary.csv",
        T1_RUN / "results" / "residuals.csv",
        T7_RUN / "results" / "locked_branch_scores.csv",
        CMB_RUN / "results" / "fit_summary.csv",
        JOINT_RUN / "results" / "fit_summary.csv",
        ROUTE_RUN / "results" / "decision.csv",
        WORK_DIR / "123-CMB-bridge-demotion-and-next-test-route.md",
        script_path,
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


def load_primary_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    config = read_json(T1_RUN / "run_config.json")
    sn = snbao.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config.get("sn_max_rows"),
        covariance_path=Path(config["sn_cov"]),
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = snbao.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    bao["label"] = config["bao_label"]
    return config, sn, bao


def t7_locked_params() -> dict[str, float]:
    rows = read_csv_rows(T7_RUN / "results" / "locked_branch_scores.csv")
    matches = [row for row in rows if row["branch"] == "T1_primary_fullcov_DR2"]
    if len(matches) != 1:
        raise RuntimeError(f"expected one T7 primary row, found {len(matches)}")
    return {
        "Omega_m": float(matches[0]["Omega_m"]),
        "B_mem": LOCKED_B_MEM,
        "p": LOCKED_P,
        "u3": LOCKED_U3,
    }


def row_labels(bao: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "row_index": index,
            "z": float(row["z"]),
            "observable": row["quantity"],
            "observed": float(row["value"]),
        }
        for index, row in enumerate(bao["rows"])
    ]


def residual_diagnostics(
    residual: np.ndarray,
    predicted: np.ndarray,
    bao: dict[str, Any],
    branch: dict[str, Any],
) -> tuple[list[dict[str, Any]], float]:
    labels = row_labels(bao)
    covariance = np.asarray(bao["covariance"], dtype=float)
    inv_cov = np.linalg.inv(covariance)
    inv_residual = inv_cov @ residual
    diagonal_sigma = np.sqrt(np.diag(covariance))
    signed_contrib = residual * inv_residual
    chi2 = float(residual @ inv_cov @ residual)

    rows: list[dict[str, Any]] = []
    for label, predicted_value, residual_value, sigma, contribution in zip(
        labels, predicted, residual, diagonal_sigma, signed_contrib, strict=True
    ):
        rows.append(
            {
                **branch,
                "row_index": label["row_index"],
                "z": label["z"],
                "observable": label["observable"],
                "observed": label["observed"],
                "predicted": float(predicted_value),
                "residual": float(residual_value),
                "diagonal_sigma": float(sigma),
                "diagonal_pull": float(residual_value / sigma),
                "cov_signed_chi2_contribution": float(contribution),
                "abs_cov_signed_chi2_contribution": abs(float(contribution)),
                "chi2_BAO_branch_total": chi2,
            }
        )
    return rows, chi2


def branch_base(
    branch_id: str,
    branch_family: str,
    model: str,
    alpha_mode: str,
    source: str,
    prior_table: str = "",
    score_mode: str = "",
    role: str = "",
) -> dict[str, Any]:
    return {
        "branch_id": branch_id,
        "branch_family": branch_family,
        "model": model,
        "prior_table": prior_table,
        "score_mode": score_mode,
        "alpha_mode": alpha_mode,
        "source": source,
        "role": role,
    }


def t1_late_residual_branches(bao: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fit_lookup = {row["model"]: row for row in read_csv_rows(T1_RUN / "results" / "fit_summary.csv")}
    residual_rows = [
        row
        for row in read_csv_rows(T1_RUN / "results" / "residuals.csv")
        if row["dataset"] == "DESI_DR2_primary"
    ]
    by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in residual_rows:
        by_model[row["model"]].append(row)

    branch_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for model, rows in sorted(by_model.items()):
        rows_sorted = sorted(rows, key=lambda row: int(row["row_index"]))
        residual = np.asarray([float(row["residual"]) for row in rows_sorted], dtype=float)
        predicted = np.asarray([float(row["predicted"]) for row in rows_sorted], dtype=float)
        branch_id = f"late_T1_free_alpha__{model}"
        branch = branch_base(
            branch_id,
            "late_T1_free_alpha",
            model,
            "free_alpha_existing_T1",
            "T1 residuals.csv",
            role="late_baseline_or_fitted_closure",
        )
        rows_out, chi2 = residual_diagnostics(residual, predicted, bao, branch)
        detail_rows.extend(rows_out)
        fit = fit_lookup.get(model, {})
        branch_rows.append(
            {
                **branch,
                "Omega_m0": "",
                "h": "",
                "r_d": "",
                "alpha_BAO": "",
                "chi2_BAO": chi2,
                "chi2_BAO_reported": fit.get("chi2_BAO", ""),
                "success": fit.get("convergence", ""),
                "edge_flag": fit.get("prior_edge_flag", ""),
                "notes": "late-only SN+BAO fit from existing T1 smoke residuals",
            }
        )
    return branch_rows, detail_rows


def t7_locked_branch(bao: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    params = t7_locked_params()
    chi2, alpha, residual, predicted = snbao.bao_chi2("MTS_fixed_p3_u3quarter", params, bao)
    branch = branch_base(
        "late_T7_locked_2over27_free_alpha__MTS_locked_2over27",
        "late_T7_locked_2over27_free_alpha",
        PRIMARY_MODEL,
        "free_alpha_recomputed_T7",
        "T7 locked_branch_scores.csv",
        role="primary_late_reference",
    )
    rows_out, chi2_check = residual_diagnostics(residual, predicted, bao, branch)
    branch_rows = [
        {
            **branch,
            "Omega_m0": params["Omega_m"],
            "h": "",
            "r_d": "",
            "alpha_BAO": alpha,
            "chi2_BAO": chi2_check,
            "chi2_BAO_reported": chi2,
            "success": True,
            "edge_flag": False,
            "notes": "locked 2/27 late reference used for MTS delta diagnostics",
        }
    ]
    return branch_rows, rows_out


def values_from_fit_row(row: dict[str, str]) -> dict[str, float]:
    values = {
        "Omega_m0": float(row["Omega_m0"]),
        "h": float(row["h"]),
    }
    for key in ["r_d", "w", "w0", "wa"]:
        parsed = maybe_float(row.get(key))
        if parsed is not None:
            values[key] = parsed
    return values


def computed_branch(
    branch: dict[str, Any],
    model: str,
    values: dict[str, float],
    bao: dict[str, Any],
    alpha_mode: str,
    alpha_value: float | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    physics_model, params = joint.physical_model_and_params(model, values)
    if alpha_mode == "tied_c_over_100_h_rd":
        if alpha_value is None:
            if "r_d" not in values:
                raise ValueError("tied alpha requires r_d")
            alpha_value = joint.C_KM_S / (100.0 * values["h"] * values["r_d"])
        predicted = snbao.bao_prediction(physics_model, params, bao, alpha=float(alpha_value))
        observed = np.asarray([row["value"] for row in bao["rows"]], dtype=float)
        residual = observed - predicted
        chi2 = float(residual @ np.linalg.inv(np.asarray(bao["covariance"], dtype=float)) @ residual)
        alpha = float(alpha_value)
    elif alpha_mode == "free_alpha_shape_only":
        chi2, alpha, residual, predicted = snbao.bao_chi2(physics_model, params, bao)
    else:
        raise ValueError(f"unknown alpha mode {alpha_mode}")

    detail_rows, chi2_check = residual_diagnostics(residual, predicted, bao, branch)
    branch_row = {
        **branch,
        "Omega_m0": values.get("Omega_m0", ""),
        "h": values.get("h", ""),
        "r_d": values.get("r_d", ""),
        "alpha_BAO": alpha,
        "chi2_BAO": chi2_check,
        "chi2_BAO_reported": chi2,
        "success": True,
        "edge_flag": "",
        "notes": "",
    }
    return branch_row, detail_rows


def joint_branches(bao: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    branch_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for row in read_csv_rows(JOINT_RUN / "results" / "fit_summary.csv"):
        if row["rd_prior_mode"] != "broad" or row["success"] != "True":
            continue
        model = row["model"]
        values = values_from_fit_row(row)
        branch_id = f"joint_tied_alpha__{row['prior_table']}__{row['score_mode']}__{model}"
        branch = branch_base(
            branch_id,
            "joint_tied_alpha",
            model,
            "tied_c_over_100_h_rd",
            "joint fit_summary.csv",
            prior_table=row["prior_table"],
            score_mode=row["score_mode"],
            role="joint_late_CMB",
        )
        branch_row, rows_out = computed_branch(
            branch,
            model,
            values,
            bao,
            "tied_c_over_100_h_rd",
            alpha_value=float(row["BAO_alpha"]),
        )
        branch_row["chi2_BAO_reported"] = row["chi2_BAO"]
        branch_row["success"] = row["success"]
        branch_row["edge_flag"] = row["edge_flag"]
        detail_rows.extend(rows_out)
        branch_rows.append(branch_row)
    return branch_rows, detail_rows


def cmb_compatible_branches(bao: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    branch_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for row in read_csv_rows(CMB_RUN / "results" / "fit_summary.csv"):
        if row["success"] != "True":
            continue
        model = row["model"]
        values = values_from_fit_row(row)
        branch_id = f"CMB_only_free_alpha_shape__{row['prior_table']}__{row['score_mode']}__{model}"
        branch = branch_base(
            branch_id,
            "CMB_only_free_alpha_shape",
            model,
            "free_alpha_shape_only",
            "CMB distance fit_summary.csv",
            prior_table=row["prior_table"],
            score_mode=row["score_mode"],
            role="CMB_compatible_shape_probe",
        )
        branch_row, rows_out = computed_branch(branch, model, values, bao, "free_alpha_shape_only")
        branch_row["success"] = row["success"]
        branch_row["edge_flag"] = row["edge_flag"]
        branch_row["notes"] = "CMB-only Omega/h shape confronted with BAO using free alpha; not a tied-r_d score"
        detail_rows.extend(rows_out)
        branch_rows.append(branch_row)
    return branch_rows, detail_rows


def group_rows(detail_rows: list[dict[str, Any]], group_field: str) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in detail_rows:
        grouped[(row["branch_id"], str(row[group_field]))].append(row)

    output: list[dict[str, Any]] = []
    for (branch_id, group_value), rows in sorted(grouped.items()):
        first = rows[0]
        pulls = [float(row["diagonal_pull"]) for row in rows]
        signed = [float(row["cov_signed_chi2_contribution"]) for row in rows]
        output.append(
            {
                "branch_id": branch_id,
                "branch_family": first["branch_family"],
                "model": first["model"],
                "prior_table": first["prior_table"],
                "score_mode": first["score_mode"],
                group_field: group_value,
                "rows": len(rows),
                "signed_chi2_sum": sum(signed),
                "abs_signed_chi2_sum": sum(abs(value) for value in signed),
                "diagonal_pull_rms": math.sqrt(sum(value * value for value in pulls) / len(pulls)),
                "max_abs_diagonal_pull": max(abs(value) for value in pulls),
            }
        )
    return output


def t7_detail_lookup(detail_rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    t7_rows = [
        row
        for row in detail_rows
        if row["branch_id"] == "late_T7_locked_2over27_free_alpha__MTS_locked_2over27"
    ]
    if len(t7_rows) != 13:
        raise RuntimeError(f"expected 13 T7 BAO rows, found {len(t7_rows)}")
    return {int(row["row_index"]): row for row in t7_rows}


def mts_delta_rows(detail_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    t7_lookup = t7_detail_lookup(detail_rows)
    rows: list[dict[str, Any]] = []
    for row in detail_rows:
        if row["model"] != PRIMARY_MODEL or row["branch_family"] == "late_T7_locked_2over27_free_alpha":
            continue
        t7 = t7_lookup[int(row["row_index"])]
        delta = float(row["cov_signed_chi2_contribution"]) - float(t7["cov_signed_chi2_contribution"])
        rows.append(
            {
                "branch_id": row["branch_id"],
                "branch_family": row["branch_family"],
                "prior_table": row["prior_table"],
                "score_mode": row["score_mode"],
                "row_index": row["row_index"],
                "z": row["z"],
                "observable": row["observable"],
                "delta_signed_chi2_vs_T7": delta,
                "abs_delta_signed_chi2_vs_T7": abs(delta),
                "branch_contribution": row["cov_signed_chi2_contribution"],
                "T7_contribution": t7["cov_signed_chi2_contribution"],
                "branch_residual": row["residual"],
                "T7_residual": t7["residual"],
                "branch_diagonal_pull": row["diagonal_pull"],
                "T7_diagonal_pull": t7["diagonal_pull"],
            }
        )
    return rows


def mts_delta_group_rows(delta_rows: list[dict[str, Any]], group_field: str) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in delta_rows:
        grouped[(row["branch_id"], str(row[group_field]))].append(row)
    output: list[dict[str, Any]] = []
    for (branch_id, group_value), rows in sorted(grouped.items()):
        first = rows[0]
        deltas = [float(row["delta_signed_chi2_vs_T7"]) for row in rows]
        output.append(
            {
                "branch_id": branch_id,
                "branch_family": first["branch_family"],
                "prior_table": first["prior_table"],
                "score_mode": first["score_mode"],
                group_field: group_value,
                "rows": len(rows),
                "delta_signed_chi2_sum_vs_T7": sum(deltas),
                "positive_delta_sum": sum(value for value in deltas if value > 0.0),
                "negative_delta_sum": sum(value for value in deltas if value < 0.0),
                "abs_delta_sum": sum(abs(value) for value in deltas),
            }
        )
    return output


def primary_failed_driver_rows(delta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed_branch = (
        f"joint_tied_alpha__{PRIMARY_FAILED_PRIOR_TABLE}__"
        f"{PRIMARY_FAILED_SCORE_MODE}__{PRIMARY_MODEL}"
    )
    rows = [row for row in delta_rows if row["branch_id"] == failed_branch]
    positives = sorted(
        [row for row in rows if float(row["delta_signed_chi2_vs_T7"]) > 0.0],
        key=lambda row: float(row["delta_signed_chi2_vs_T7"]),
        reverse=True,
    )
    negatives = sorted(
        [row for row in rows if float(row["delta_signed_chi2_vs_T7"]) < 0.0],
        key=lambda row: float(row["delta_signed_chi2_vs_T7"]),
    )
    output: list[dict[str, Any]] = []
    for rank, row in enumerate(positives[:8], start=1):
        output.append({**row, "rank": rank, "driver_type": "largest_positive_penalty"})
    for rank, row in enumerate(negatives[:5], start=1):
        output.append({**row, "rank": rank, "driver_type": "largest_negative_offset"})
    return output


def branch_chi2_summary(branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    t7 = next(row for row in branch_rows if row["branch_id"] == "late_T7_locked_2over27_free_alpha__MTS_locked_2over27")
    t7_chi2 = float(t7["chi2_BAO"])
    for row in branch_rows:
        output.append(
            {
                **row,
                "delta_chi2_BAO_vs_T7_locked": float(row["chi2_BAO"]) - t7_chi2
                if row["model"] == PRIMARY_MODEL
                else "",
            }
        )
    return output


def decision_rows(
    branch_rows: list[dict[str, Any]],
    delta_observable_rows: list[dict[str, Any]],
    delta_redshift_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    failed_branch = (
        f"joint_tied_alpha__{PRIMARY_FAILED_PRIOR_TABLE}__"
        f"{PRIMARY_FAILED_SCORE_MODE}__{PRIMARY_MODEL}"
    )
    failed_branch_row = next(row for row in branch_rows if row["branch_id"] == failed_branch)
    failed_chi2 = float(failed_branch_row["chi2_BAO"])
    t7_row = next(row for row in branch_rows if row["branch_id"] == "late_T7_locked_2over27_free_alpha__MTS_locked_2over27")
    t7_chi2 = float(t7_row["chi2_BAO"])
    failed_observable = [
        row for row in delta_observable_rows if row["branch_id"] == failed_branch
    ]
    failed_redshift = [row for row in delta_redshift_rows if row["branch_id"] == failed_branch]
    top_observable = max(failed_observable, key=lambda row: float(row["positive_delta_sum"]))
    top_redshift = max(failed_redshift, key=lambda row: float(row["positive_delta_sum"]))
    return [
        {
            "item": "status",
            "verdict": "BAO_shape_residual_decomposition_complete",
            "evidence": "row, observable, and redshift covariance-signed BAO residual contributions written",
        },
        {
            "item": "primary_failed_gate_BAO_delta",
            "verdict": "localized",
            "evidence": f"failed BAO chi2={failed_chi2:.12g}; T7 BAO chi2={t7_chi2:.12g}; delta={failed_chi2 - t7_chi2:.12g}",
        },
        {
            "item": "dominant_observable",
            "verdict": str(top_observable["observable"]),
            "evidence": f"positive delta sum={float(top_observable['positive_delta_sum']):.12g}; signed delta sum={float(top_observable['delta_signed_chi2_sum_vs_T7']):.12g}",
        },
        {
            "item": "dominant_redshift",
            "verdict": str(top_redshift["z"]),
            "evidence": f"positive delta sum={float(top_redshift['positive_delta_sum']):.12g}; signed delta sum={float(top_redshift['delta_signed_chi2_sum_vs_T7']):.12g}",
        },
        {
            "item": "claim_status",
            "verdict": "diagnostic_only_no_promotion",
            "evidence": "no BAO deformation or Omega map was fitted",
        },
        {
            "item": "next_target",
            "verdict": "derive_BAO_shape_or_choose_non_CMB_test",
            "evidence": "use the localized residual pattern as a theorem target, not a rescue knob",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-BAO-shape-residual-decomposition"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    _, _, bao = load_primary_data()

    branch_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for builder in [t1_late_residual_branches, t7_locked_branch, joint_branches, cmb_compatible_branches]:
        branches, details = builder(bao)
        branch_rows.extend(branches)
        detail_rows.extend(details)

    branch_summary = branch_chi2_summary(branch_rows)
    observable_summary = group_rows(detail_rows, "observable")
    redshift_summary = group_rows(detail_rows, "z")
    delta_rows = mts_delta_rows(detail_rows)
    delta_observable = mts_delta_group_rows(delta_rows, "observable")
    delta_redshift = mts_delta_group_rows(delta_rows, "z")
    failed_drivers = primary_failed_driver_rows(delta_rows)
    decisions = decision_rows(branch_rows, delta_observable, delta_redshift)

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "branch_chi2_summary.csv",
        branch_summary,
        [
            "branch_id",
            "branch_family",
            "model",
            "prior_table",
            "score_mode",
            "alpha_mode",
            "source",
            "role",
            "Omega_m0",
            "h",
            "r_d",
            "alpha_BAO",
            "chi2_BAO",
            "chi2_BAO_reported",
            "delta_chi2_BAO_vs_T7_locked",
            "success",
            "edge_flag",
            "notes",
        ],
    )
    write_csv(
        results_dir / "bao_row_residuals.csv",
        detail_rows,
        [
            "branch_id",
            "branch_family",
            "model",
            "prior_table",
            "score_mode",
            "alpha_mode",
            "source",
            "role",
            "row_index",
            "z",
            "observable",
            "observed",
            "predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
            "abs_cov_signed_chi2_contribution",
            "chi2_BAO_branch_total",
        ],
    )
    write_csv(
        results_dir / "observable_group_summary.csv",
        observable_summary,
        [
            "branch_id",
            "branch_family",
            "model",
            "prior_table",
            "score_mode",
            "observable",
            "rows",
            "signed_chi2_sum",
            "abs_signed_chi2_sum",
            "diagonal_pull_rms",
            "max_abs_diagonal_pull",
        ],
    )
    write_csv(
        results_dir / "redshift_group_summary.csv",
        redshift_summary,
        [
            "branch_id",
            "branch_family",
            "model",
            "prior_table",
            "score_mode",
            "z",
            "rows",
            "signed_chi2_sum",
            "abs_signed_chi2_sum",
            "diagonal_pull_rms",
            "max_abs_diagonal_pull",
        ],
    )
    write_csv(
        results_dir / "mts_delta_vs_T7_by_row.csv",
        delta_rows,
        [
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "row_index",
            "z",
            "observable",
            "delta_signed_chi2_vs_T7",
            "abs_delta_signed_chi2_vs_T7",
            "branch_contribution",
            "T7_contribution",
            "branch_residual",
            "T7_residual",
            "branch_diagonal_pull",
            "T7_diagonal_pull",
        ],
    )
    write_csv(
        results_dir / "mts_delta_vs_T7_by_observable.csv",
        delta_observable,
        [
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "observable",
            "rows",
            "delta_signed_chi2_sum_vs_T7",
            "positive_delta_sum",
            "negative_delta_sum",
            "abs_delta_sum",
        ],
    )
    write_csv(
        results_dir / "mts_delta_vs_T7_by_redshift.csv",
        delta_redshift,
        [
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "z",
            "rows",
            "delta_signed_chi2_sum_vs_T7",
            "positive_delta_sum",
            "negative_delta_sum",
            "abs_delta_sum",
        ],
    )
    write_csv(
        results_dir / "primary_failed_gate_drivers.csv",
        failed_drivers,
        [
            "rank",
            "driver_type",
            "branch_id",
            "branch_family",
            "prior_table",
            "score_mode",
            "row_index",
            "z",
            "observable",
            "delta_signed_chi2_vs_T7",
            "abs_delta_signed_chi2_vs_T7",
            "branch_contribution",
            "T7_contribution",
            "branch_residual",
            "T7_residual",
            "branch_diagonal_pull",
            "T7_diagonal_pull",
        ],
    )
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": "BAO_shape_residual_decomposition_complete",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "diagnostic_residual_map_only",
        "bao_rows": len(bao["rows"]),
        "branches": len(branch_rows),
        "row_residuals": len(detail_rows),
        "primary_failed_branch": (
            f"joint_tied_alpha__{PRIMARY_FAILED_PRIOR_TABLE}__"
            f"{PRIMARY_FAILED_SCORE_MODE}__{PRIMARY_MODEL}"
        ),
        "generated": [
            "source_register.csv",
            "branch_chi2_summary.csv",
            "bao_row_residuals.csv",
            "observable_group_summary.csv",
            "redshift_group_summary.csv",
            "mts_delta_vs_T7_by_row.csv",
            "mts_delta_vs_T7_by_observable.csv",
            "mts_delta_vs_T7_by_redshift.csv",
            "primary_failed_gate_drivers.csv",
            "decision.csv",
        ],
        "next_target": "125-BAO-shape-theorem-target-or-non-CMB-stress-route.md",
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
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
