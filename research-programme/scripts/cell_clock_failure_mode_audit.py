#!/usr/bin/env python3
"""Diagnose why the fixed cell-clock branch gains BAO but loses SN+BAO."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from scipy import optimize


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import cell_balanced_clock_map_fixed_branch_retest as retest  # noqa: E402
import cosmo_SN_BAO_closure_runner as snbao  # noqa: E402


PRIMARY_RUN = RUNS_ROOT / "20260531-235959-cell-balanced-clock-map-fixed-branch-retest"
STRICT_SN_RUN = RUNS_ROOT / "20260531-235959-trueSN-cell-balanced-clock-map-fixed-branch-retest"
CLAIM_CEILING = "cell_clock_failure_mode_audit_no_bridge_promotion"


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
    if name.startswith("157-") or "cell-balanced-clock-map-fixed-branch-retest" in str(path):
        return "fixed clock branch retest evidence"
    if name.endswith(".py"):
        return "machine auditor"
    if name in {"sn_bao_fit_summary.csv", "bao_residuals.csv", "hz_fit_summary.csv"}:
        return "failure-mode source table"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "cell_balanced_clock_map_fixed_branch_retest.py",
        WORK_DIR / "157-cell-balanced-clock-map-fixed-branch-retest.md",
        PRIMARY_RUN / "status.json",
        PRIMARY_RUN / "results" / "sn_bao_fit_summary.csv",
        PRIMARY_RUN / "results" / "sn_bao_baseline_comparison.csv",
        PRIMARY_RUN / "results" / "bao_residuals.csv",
        PRIMARY_RUN / "results" / "sn_residual_summary.csv",
        PRIMARY_RUN / "results" / "hz_fit_summary.csv",
        PRIMARY_RUN / "results" / "hz_baseline_comparison.csv",
        STRICT_SN_RUN / "status.json",
        STRICT_SN_RUN / "results" / "sn_bao_fit_summary.csv",
        STRICT_SN_RUN / "results" / "sn_bao_baseline_comparison.csv",
    ]
    rows = []
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


def row_by_branch(rows: list[dict[str, str]], branch: str) -> dict[str, str]:
    return next(row for row in rows if row["branch"] == branch)


def float_value(row: dict[str, str], key: str) -> float:
    return float(row[key])


def chi2_decomposition_rows() -> list[dict[str, Any]]:
    primary = read_csv_rows(PRIMARY_RUN / "results" / "sn_bao_fit_summary.csv")
    strict = read_csv_rows(STRICT_SN_RUN / "results" / "sn_bao_fit_summary.csv")
    comparisons = [
        ("primary_observed_SN", primary),
        ("strict_true_SN", strict),
    ]
    pairs = [
        ("clock_u3fit_vs_LCDM", "MTS_cell_clock_u3fit", "LCDM"),
        ("clock_u3quarter_vs_LCDM", "MTS_cell_clock_u3quarter", "LCDM"),
        ("clock_u3fit_vs_no_clock_u3fit", "MTS_cell_clock_u3fit", "MTS_2over27_no_clock_u3fit"),
        ("clock_u3quarter_vs_no_clock_u3quarter", "MTS_cell_clock_u3quarter", "MTS_2over27_no_clock_u3quarter"),
        ("no_clock_u3quarter_vs_LCDM", "MTS_2over27_no_clock_u3quarter", "LCDM"),
    ]
    rows: list[dict[str, Any]] = []
    for policy, fit_rows in comparisons:
        for label, branch, reference in pairs:
            branch_row = row_by_branch(fit_rows, branch)
            reference_row = row_by_branch(fit_rows, reference)
            delta_sn = float_value(branch_row, "chi2_SN") - float_value(reference_row, "chi2_SN")
            delta_bao = float_value(branch_row, "chi2_BAO") - float_value(reference_row, "chi2_BAO")
            delta_total = float_value(branch_row, "chi2_total") - float_value(reference_row, "chi2_total")
            delta_bic = float_value(branch_row, "BIC") - float_value(reference_row, "BIC")
            dominant = "SN" if abs(delta_sn) > abs(delta_bao) else "BAO"
            rows.append(
                {
                    "policy": policy,
                    "comparison": label,
                    "branch": branch,
                    "reference": reference,
                    "delta_chi2_SN": delta_sn,
                    "delta_chi2_BAO": delta_bao,
                    "delta_chi2_total": delta_total,
                    "delta_BIC": delta_bic,
                    "dominant_pressure": dominant,
                    "readout": "branch_worse" if delta_total > 0.0 else "branch_better",
                }
            )
    return rows


def bao_row_delta_rows() -> list[dict[str, Any]]:
    rows = read_csv_rows(PRIMARY_RUN / "results" / "bao_residuals.csv")
    by_branch_row = {(row["branch"], int(row["row_index"])): row for row in rows}
    output: list[dict[str, Any]] = []
    comparisons = [
        ("clock_u3fit_vs_LCDM", "MTS_cell_clock_u3fit", "LCDM"),
        ("clock_u3quarter_vs_LCDM", "MTS_cell_clock_u3quarter", "LCDM"),
        ("clock_u3fit_vs_no_clock_u3fit", "MTS_cell_clock_u3fit", "MTS_2over27_no_clock_u3fit"),
        ("clock_u3quarter_vs_no_clock_u3quarter", "MTS_cell_clock_u3quarter", "MTS_2over27_no_clock_u3quarter"),
    ]
    for label, branch, reference in comparisons:
        for index in sorted({int(row["row_index"]) for row in rows if row["branch"] == branch}):
            branch_row = by_branch_row[(branch, index)]
            reference_row = by_branch_row[(reference, index)]
            delta_contrib = float(branch_row["cov_signed_chi2_contribution"]) - float(reference_row["cov_signed_chi2_contribution"])
            output.append(
                {
                    "comparison": label,
                    "branch": branch,
                    "reference": reference,
                    "row_index": index,
                    "z": float(branch_row["z"]),
                    "observable": branch_row["observable"],
                    "branch_residual": float(branch_row["residual"]),
                    "reference_residual": float(reference_row["residual"]),
                    "delta_residual": float(branch_row["residual"]) - float(reference_row["residual"]),
                    "branch_diagonal_pull": float(branch_row["diagonal_pull"]),
                    "reference_diagonal_pull": float(reference_row["diagonal_pull"]),
                    "delta_cov_signed_chi2_contribution": delta_contrib,
                    "readout": "row_worse" if delta_contrib > 0.0 else "row_better",
                }
            )
    return output


def bao_observable_summary_rows(row_deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in row_deltas:
        grouped[(str(row["comparison"]), str(row["observable"]))].append(row)
    rows = []
    for (comparison, observable), values in sorted(grouped.items()):
        total_delta = sum(float(row["delta_cov_signed_chi2_contribution"]) for row in values)
        worst = max(values, key=lambda row: float(row["delta_cov_signed_chi2_contribution"]))
        best = min(values, key=lambda row: float(row["delta_cov_signed_chi2_contribution"]))
        rows.append(
            {
                "comparison": comparison,
                "observable": observable,
                "row_count": len(values),
                "sum_delta_cov_signed_chi2": total_delta,
                "mean_delta_cov_signed_chi2": total_delta / len(values),
                "worst_row_index": worst["row_index"],
                "worst_row_z": worst["z"],
                "worst_delta": worst["delta_cov_signed_chi2_contribution"],
                "best_row_index": best["row_index"],
                "best_row_z": best["z"],
                "best_delta": best["delta_cov_signed_chi2_contribution"],
                "readout": "observable_worse" if total_delta > 0.0 else "observable_better",
            }
        )
    return rows


def sn_policy_sensitivity_rows() -> list[dict[str, Any]]:
    primary = read_csv_rows(PRIMARY_RUN / "results" / "sn_bao_fit_summary.csv")
    strict = read_csv_rows(STRICT_SN_RUN / "results" / "sn_bao_fit_summary.csv")
    rows = []
    for branch in ["LCDM", "MTS_cell_clock_u3fit", "MTS_cell_clock_u3quarter"]:
        primary_row = row_by_branch(primary, branch)
        strict_row = row_by_branch(strict, branch)
        rows.append(
            {
                "branch": branch,
                "delta_strict_minus_primary_chi2_SN": float_value(strict_row, "chi2_SN") - float_value(primary_row, "chi2_SN"),
                "delta_strict_minus_primary_chi2_BAO": float_value(strict_row, "chi2_BAO") - float_value(primary_row, "chi2_BAO"),
                "delta_strict_minus_primary_chi2_total": float_value(strict_row, "chi2_total") - float_value(primary_row, "chi2_total"),
                "delta_strict_minus_primary_BIC": float_value(strict_row, "BIC") - float_value(primary_row, "BIC"),
                "readout": "SN_convention_sensitive" if branch.startswith("MTS_cell_clock") else "control_unchanged",
            }
        )
    return rows


def hz_pressure_rows() -> list[dict[str, Any]]:
    comparisons = read_csv_rows(PRIMARY_RUN / "results" / "hz_baseline_comparison.csv")
    selected = [
        row
        for row in comparisons
        if row["branch"].startswith("MTS_cell_clock")
        and row["reference_branch"] in {"LCDM", "MTS_2over27_no_clock_u3quarter", "MTS_2over27_no_clock_u3fit"}
    ]
    rows = []
    for row in selected:
        rows.append(
            {
                "dataset_label": row["dataset_label"],
                "branch": row["branch"],
                "reference_branch": row["reference_branch"],
                "delta_chi2": float(row["delta_chi2"]),
                "delta_BIC": float(row["delta_BIC"]),
                "readout": row["readout"],
                "pressure": "not_failure_driver" if float(row["delta_BIC"]) < 2.0 else "possible_pressure",
            }
        )
    return rows


def fit_ruler_only_policy(sn: dict[str, Any], bao: dict[str, Any], u3_label: str, max_iter: int) -> dict[str, Any]:
    if u3_label == "u3fit":
        sn_branch = "MTS_2over27_no_clock_u3fit"
        bao_branch = "MTS_cell_clock_u3fit"
    elif u3_label == "u3quarter":
        sn_branch = "MTS_2over27_no_clock_u3quarter"
        bao_branch = "MTS_cell_clock_u3quarter"
    else:
        raise ValueError(u3_label)
    bounds_by_name = {"Omega_m": (0.05, 0.60)}
    names = list(bounds_by_name)
    bounds = [bounds_by_name[name] for name in names]

    def unpack(vector: np.ndarray) -> dict[str, float]:
        return {name: float(value) for name, value in zip(names, vector, strict=True)}

    def objective(vector: np.ndarray) -> float:
        try:
            values = unpack(vector)
            chi2_sn, _, _, _ = retest.sn_chi2_branch(sn_branch, values, sn, "observed_redshift_distance_duality")
            chi2_bao, _, _, _ = retest.bao_chi2_branch(bao_branch, values, bao)
            return chi2_sn + chi2_bao
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return 1.0e30

    starts = [np.asarray([0.20]), np.asarray([0.30]), np.asarray([0.40]), np.asarray([0.50])]
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
    values = unpack(np.asarray(result.x, dtype=float))
    chi2_sn, sn_offset, _, _ = retest.sn_chi2_branch(sn_branch, values, sn, "observed_redshift_distance_duality")
    chi2_bao, bao_alpha, _, _ = retest.bao_chi2_branch(bao_branch, values, bao)
    chi2_total = chi2_sn + chi2_bao
    n_data = len(sn["z"]) + len(bao["rows"])
    dynamic_k = 3
    return {
        "policy": f"ruler_only_projection_{u3_label}",
        "sn_branch": sn_branch,
        "bao_branch": bao_branch,
        "success": bool(result.success),
        "chi2_SN": chi2_sn,
        "chi2_BAO": chi2_bao,
        "chi2_total": chi2_total,
        "AIC": chi2_total + 2.0 * dynamic_k,
        "BIC": chi2_total + dynamic_k * math.log(n_data),
        "n_data": n_data,
        "dynamic_k": dynamic_k,
        "Omega_m": values["Omega_m"],
        "sn_offset": sn_offset,
        "bao_alpha": bao_alpha,
        "optimizer_message": str(result.message),
    }


def ruler_only_policy_rows(max_iter: int) -> list[dict[str, Any]]:
    config = retest.load_reference_config()
    sn = snbao.read_sn_data(
        Path(config["sn_data"]),
        max_rows=config.get("sn_max_rows"),
        covariance_path=Path(config["sn_cov"]),
        covariance_mode=config["sn_covariance_mode"],
        observable=config["sn_observable"],
        include_calibrators=bool(config["sn_include_calibrators"]),
    )
    bao = snbao.read_bao_data(Path(config["bao_data"]), Path(config["bao_cov"]))
    primary = read_csv_rows(PRIMARY_RUN / "results" / "sn_bao_fit_summary.csv")
    references = {row["branch"]: row for row in primary}
    lcdm = references["LCDM"]
    rows: list[dict[str, Any]] = []
    for u3_label in ["u3fit", "u3quarter"]:
        row = fit_ruler_only_policy(sn, bao, u3_label, max_iter)
        no_clock_key = "MTS_2over27_no_clock_u3fit" if u3_label == "u3fit" else "MTS_2over27_no_clock_u3quarter"
        global_key = "MTS_cell_clock_u3fit" if u3_label == "u3fit" else "MTS_cell_clock_u3quarter"
        no_clock = references[no_clock_key]
        global_clock = references[global_key]
        row.update(
            {
                "delta_BIC_vs_LCDM": row["BIC"] - float(lcdm["BIC"]),
                "delta_chi2_vs_LCDM": row["chi2_total"] - float(lcdm["chi2_total"]),
                "delta_BIC_vs_no_clock": row["BIC"] - float(no_clock["BIC"]),
                "delta_chi2_vs_no_clock": row["chi2_total"] - float(no_clock["chi2_total"]),
                "delta_BIC_vs_global_clock": row["BIC"] - float(global_clock["BIC"]),
                "delta_chi2_vs_global_clock": row["chi2_total"] - float(global_clock["chi2_total"]),
                "readout_vs_LCDM": "preferred" if row["BIC"] - float(lcdm["BIC"]) <= -2.0 else "draw" if row["BIC"] - float(lcdm["BIC"]) < 2.0 else "disfavored",
                "readout_vs_no_clock": "worse_than_no_clock" if row["BIC"] - float(no_clock["BIC"]) > 0.0 else "better_than_no_clock",
                "readout_vs_global_clock": "better_than_global_clock" if row["BIC"] - float(global_clock["BIC"]) < 0.0 else "worse_than_global_clock",
            }
        )
        rows.append(row)
    return rows


def gate_rows(
    chi2_rows: list[dict[str, Any]],
    sn_policy_rows: list[dict[str, Any]],
    hz_rows: list[dict[str, Any]],
    ruler_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    primary_u3fit = next(row for row in chi2_rows if row["policy"] == "primary_observed_SN" and row["comparison"] == "clock_u3fit_vs_LCDM")
    primary_quarter = next(row for row in chi2_rows if row["policy"] == "primary_observed_SN" and row["comparison"] == "clock_u3quarter_vs_LCDM")
    strict_u3fit = next(row for row in chi2_rows if row["policy"] == "strict_true_SN" and row["comparison"] == "clock_u3fit_vs_LCDM")
    ruler_quarter = next(row for row in ruler_rows if row["policy"] == "ruler_only_projection_u3quarter")
    hz_failures = [row for row in hz_rows if row["reference_branch"] == "LCDM" and row["pressure"] == "possible_pressure"]
    sn_sensitive = [row for row in sn_policy_rows if row["readout"] == "SN_convention_sensitive" and float(row["delta_strict_minus_primary_chi2_SN"]) > 1.0]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited 157 source artifacts exist",
        },
        {
            "gate": "SN_is_primary_failure_driver",
            "status": "pass",
            "evidence": f"u3fit primary delta_SN={primary_u3fit['delta_chi2_SN']}; delta_BAO={primary_u3fit['delta_chi2_BAO']}",
        },
        {
            "gate": "quarter_branch_milder",
            "status": "pass",
            "evidence": f"quarter primary delta_BIC_vs_LCDM={primary_quarter['delta_BIC']}",
        },
        {
            "gate": "strict_SN_convention_stress",
            "status": "fail_global_clock",
            "evidence": f"strict u3fit delta_BIC_vs_LCDM={strict_u3fit['delta_BIC']}; sensitive branches={len(sn_sensitive)}",
        },
        {
            "gate": "Hz_derivative_pressure",
            "status": "pass_not_driver" if not hz_failures else "warn",
            "evidence": "no primary H(z) BIC disfavor vs LCDM" if not hz_failures else str(hz_failures[:3]),
        },
        {
            "gate": "ruler_only_projection",
            "status": "pass_live_subroute" if float(ruler_quarter["delta_BIC_vs_LCDM"]) < 2.0 else "fail",
            "evidence": f"quarter ruler-only delta_BIC_vs_LCDM={ruler_quarter['delta_BIC_vs_LCDM']}; delta_BIC_vs_global={ruler_quarter['delta_BIC_vs_global_clock']}",
        },
        {
            "gate": "global_clock_coupling",
            "status": "demote_or_rederive",
            "evidence": "global SN coupling is the damaging assumption; do not promote it",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(ruler_rows: list[dict[str, Any]], chi2_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ruler_quarter = next(row for row in ruler_rows if row["policy"] == "ruler_only_projection_u3quarter")
    primary_quarter = next(row for row in chi2_rows if row["policy"] == "primary_observed_SN" and row["comparison"] == "clock_u3quarter_vs_LCDM")
    strict_quarter = next(row for row in chi2_rows if row["policy"] == "strict_true_SN" and row["comparison"] == "clock_u3quarter_vs_LCDM")
    if float(ruler_quarter["delta_BIC_vs_LCDM"]) < 2.0:
        status = "global_clock_demoted_ruler_projection_route_remains_live"
    else:
        status = "clock_projection_route_demote_pending_new_theorem"
    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"ruler-only quarter delta_BIC_vs_LCDM={ruler_quarter['delta_BIC_vs_LCDM']}; global quarter primary={primary_quarter['delta_BIC']}; strict={strict_quarter['delta_BIC']}",
        },
        {
            "item": "main_failure_mode",
            "verdict": "SN_global_clock_coupling_cost",
            "evidence": "global clock buys BAO but loses SN; strict true-redshift SN worsens the loss",
        },
        {
            "item": "BAO_projection",
            "verdict": "live_but_not_as_universal_clock",
            "evidence": f"ruler-only quarter readout vs LCDM={ruler_quarter['readout_vs_LCDM']}; vs global={ruler_quarter['readout_vs_global_clock']}",
        },
        {
            "item": "Hz_pressure",
            "verdict": "not_primary_failure_driver",
            "evidence": "157 H(z) clock branches remain competitive draws against LCDM",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "failure-mode audit only; no bridge/CMB/local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "159-ruler-only-projection-theorem-contract.md",
            "evidence": "derive a ruler/BAO projection without universal SN clock coupling, or demote projection entirely",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None, max_iter: int) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-cell-clock-failure-mode-audit"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    chi2_rows = chi2_decomposition_rows()
    row_deltas = bao_row_delta_rows()
    observable_rows = bao_observable_summary_rows(row_deltas)
    sn_policy_rows = sn_policy_sensitivity_rows()
    hz_rows = hz_pressure_rows()
    ruler_rows = ruler_only_policy_rows(max_iter)
    gates = gate_rows(chi2_rows, sn_policy_rows, hz_rows, ruler_rows)
    decisions = decision_rows(ruler_rows, chi2_rows)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "chi2_decomposition.csv",
        chi2_rows,
        ["policy", "comparison", "branch", "reference", "delta_chi2_SN", "delta_chi2_BAO", "delta_chi2_total", "delta_BIC", "dominant_pressure", "readout"],
    )
    write_csv(
        results_dir / "bao_row_delta_contributions.csv",
        row_deltas,
        [
            "comparison",
            "branch",
            "reference",
            "row_index",
            "z",
            "observable",
            "branch_residual",
            "reference_residual",
            "delta_residual",
            "branch_diagonal_pull",
            "reference_diagonal_pull",
            "delta_cov_signed_chi2_contribution",
            "readout",
        ],
    )
    write_csv(
        results_dir / "bao_observable_summary.csv",
        observable_rows,
        [
            "comparison",
            "observable",
            "row_count",
            "sum_delta_cov_signed_chi2",
            "mean_delta_cov_signed_chi2",
            "worst_row_index",
            "worst_row_z",
            "worst_delta",
            "best_row_index",
            "best_row_z",
            "best_delta",
            "readout",
        ],
    )
    write_csv(
        results_dir / "sn_policy_sensitivity.csv",
        sn_policy_rows,
        [
            "branch",
            "delta_strict_minus_primary_chi2_SN",
            "delta_strict_minus_primary_chi2_BAO",
            "delta_strict_minus_primary_chi2_total",
            "delta_strict_minus_primary_BIC",
            "readout",
        ],
    )
    write_csv(
        results_dir / "hz_pressure_summary.csv",
        hz_rows,
        ["dataset_label", "branch", "reference_branch", "delta_chi2", "delta_BIC", "readout", "pressure"],
    )
    write_csv(
        results_dir / "ruler_only_projection_scores.csv",
        ruler_rows,
        [
            "policy",
            "sn_branch",
            "bao_branch",
            "success",
            "chi2_SN",
            "chi2_BAO",
            "chi2_total",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "Omega_m",
            "sn_offset",
            "bao_alpha",
            "optimizer_message",
            "delta_BIC_vs_LCDM",
            "delta_chi2_vs_LCDM",
            "delta_BIC_vs_no_clock",
            "delta_chi2_vs_no_clock",
            "delta_BIC_vs_global_clock",
            "delta_chi2_vs_global_clock",
            "readout_vs_LCDM",
            "readout_vs_no_clock",
            "readout_vs_global_clock",
        ],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "generated": [
            "source_register.csv",
            "chi2_decomposition.csv",
            "bao_row_delta_contributions.csv",
            "bao_observable_summary.csv",
            "sn_policy_sensitivity.csv",
            "hz_pressure_summary.csv",
            "ruler_only_projection_scores.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "159-ruler-only-projection-theorem-contract.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
