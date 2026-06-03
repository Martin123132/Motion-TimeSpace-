#!/usr/bin/env python3
"""Fetch source cosmic-chronometer H(z) tables and run a frozen-branch holdout."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
SOURCE_INTAKE_ROOT = WORK_DIR / "source-intake" / "cosmic_chronometers"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import Hz_radial_expansion_smoke as hzsmoke  # noqa: E402


CC32_URL = "https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat"
CC32_SOURCE_PAGE = "https://cluster.difa.unibo.it/astro/CC_data/"
CC15_BC03_URL = "https://gitlab.com/mmoresco/CCcovariance/-/raw/master/data/HzTable_MM_BC03.dat"
CC15_RECIPE_REPO = "https://gitlab.com/mmoresco/CCcovariance"
LOCKED_B_MEM = 2.0 / 27.0
MODEL_ORDER = ["LCDM", "wCDM", "CPL", "MTS_locked_2over27", "MTS_Bmem_zero"]
PRIMARY_DATASET = "source_CC15_BC03_suggested_primary"
CLAIM_CEILING = "fresh_CC_Hz_source_locked_holdout_no_theory_promotion"
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "MTS-source-lock-audit/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8-sig")


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def parse_cc32(text: str) -> list[dict[str, str]]:
    body = normalize_whitespace(text.split("reference", 1)[1])
    pattern = re.compile(
        rf"(?P<z>{NUMBER}),(?P<H>{NUMBER}),(?P<sigma>{NUMBER}),(?P<reference>.*?)(?=\s+{NUMBER},{NUMBER},|\Z)"
    )
    rows = [
        {
            "z": match.group("z"),
            "H": match.group("H"),
            "sigma": match.group("sigma"),
            "reference": normalize_whitespace(match.group("reference")),
        }
        for match in pattern.finditer(body)
    ]
    if len(rows) != 32:
        raise ValueError(f"expected 32 CC rows, parsed {len(rows)}")
    return rows


def parse_cc15_bc03(text: str) -> list[dict[str, str]]:
    body = normalize_whitespace(text.split("reference", 1)[1])
    pattern = re.compile(
        rf"(?P<z>{NUMBER}),(?P<H>{NUMBER}),(?P<sigma>{NUMBER}),"
        rf"(?P<sigma_stat>{NUMBER}),(?P<sigma_met>{NUMBER}),(?P<reference>.*?)(?=\s+{NUMBER},{NUMBER},|\Z)"
    )
    rows = [
        {
            "z": match.group("z"),
            "H": match.group("H"),
            "sigma": match.group("sigma"),
            "sigma_stat": match.group("sigma_stat"),
            "sigma_met": match.group("sigma_met"),
            "reference": normalize_whitespace(match.group("reference")),
        }
        for match in pattern.finditer(body)
    ]
    if len(rows) != 15:
        raise ValueError(f"expected 15 BC03 rows, parsed {len(rows)}")
    return rows


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


def fetch_and_lock_sources(intake_dir: Path) -> dict[str, Any]:
    intake_dir.mkdir(parents=True, exist_ok=True)
    cc32_text = fetch_text(CC32_URL)
    cc15_text = fetch_text(CC15_BC03_URL)

    cc32_raw = intake_dir / "data_CC_unibo_raw.dat"
    cc15_raw = intake_dir / "HzTable_MM_BC03_raw.dat"
    cc32_raw.write_text(cc32_text, encoding="utf-8")
    cc15_raw.write_text(cc15_text, encoding="utf-8")

    cc32_rows = parse_cc32(cc32_text)
    cc15_rows = parse_cc15_bc03(cc15_text)

    cc32_csv = intake_dir / "CC32_source_normalized.csv"
    cc15_csv = intake_dir / "CC15_BC03_source_normalized.csv"
    write_csv(cc32_csv, cc32_rows, ["z", "H", "sigma", "reference"])
    write_csv(cc15_csv, cc15_rows, ["z", "H", "sigma", "sigma_stat", "sigma_met", "reference"])

    manifest = {
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "cc32_url": CC32_URL,
        "cc32_source_page": CC32_SOURCE_PAGE,
        "cc32_raw_path": str(cc32_raw),
        "cc32_normalized_csv": str(cc32_csv),
        "cc32_rows": len(cc32_rows),
        "cc15_bc03_url": CC15_BC03_URL,
        "cc15_recipe_repo": CC15_RECIPE_REPO,
        "cc15_raw_path": str(cc15_raw),
        "cc15_normalized_csv": str(cc15_csv),
        "cc15_rows": len(cc15_rows),
    }
    manifest_path = intake_dir / "source_lock_manifest.json"
    write_json(manifest_path, manifest)
    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "cc32_rows": cc32_rows,
        "cc15_rows": cc15_rows,
        "cc32_csv": cc32_csv,
        "cc15_csv": cc15_csv,
        "cc32_raw": cc32_raw,
        "cc15_raw": cc15_raw,
    }


def max_abs_delta(source_rows: list[dict[str, str]], local_rows: list[dict[str, str]], field: str) -> float:
    return max(
        abs(float(source[field]) - float(local[field]))
        for source, local in zip(source_rows, local_rows, strict=True)
    )


def reference_mismatches(source_rows: list[dict[str, str]], local_rows: list[dict[str, str]]) -> int:
    return sum(
        normalize_whitespace(source.get("reference", "")) != normalize_whitespace(local.get("reference", ""))
        for source, local in zip(source_rows, local_rows, strict=True)
    )


def row_lock_rows(source_lock: dict[str, Any]) -> list[dict[str, Any]]:
    cc32_local = read_csv_rows(hzsmoke.HZ_32)
    cc15_local = read_csv_rows(hzsmoke.HZ_15)
    checks = [
        ("CC32_full_table", source_lock["cc32_rows"], cc32_local, ["z", "H", "sigma"]),
        ("CC15_BC03_covariance_branch", source_lock["cc15_rows"], cc15_local, ["z", "H", "sigma", "sigma_stat", "sigma_met"]),
    ]
    rows = []
    for label, source_rows, local_rows, numeric_fields in checks:
        numeric_deltas = {
            f"max_abs_delta_{field}": max_abs_delta(source_rows, local_rows, field)
            for field in numeric_fields
        }
        ref_mismatch_count = reference_mismatches(source_rows, local_rows)
        status = "pass" if all(value <= 1.0e-10 for value in numeric_deltas.values()) and ref_mismatch_count == 0 else "warn"
        rows.append(
            {
                "dataset": label,
                "source_rows": len(source_rows),
                "local_rows": len(local_rows),
                "reference_mismatch_count": ref_mismatch_count,
                "status": status,
                **numeric_deltas,
            }
        )
    return rows


def load_source_hz15_dataset(
    source_lock: dict[str, Any], covariance_label: str, dataset_label: str, role: str
) -> dict[str, Any]:
    rows = source_lock["cc15_rows"]
    z = np.asarray([float(row["z"]) for row in rows], dtype=float)
    h_obs = np.asarray([float(row["H"]) for row in rows], dtype=float)
    sigma = np.asarray([float(row["sigma"]) for row in rows], dtype=float)
    cov_z, covariance = hzsmoke.read_covariance_matrix(hzsmoke.COVARIANCE_FILES[covariance_label])
    if len(cov_z) != len(z) or np.max(np.abs(np.asarray(cov_z, dtype=float) - z)) > 1.0e-8:
        raise ValueError(f"covariance redshift header mismatch for {covariance_label}")
    return {
        "dataset_label": dataset_label,
        "role": role,
        "data_path": str(source_lock["cc15_csv"]),
        "covariance_label": covariance_label,
        "covariance_path": str(hzsmoke.COVARIANCE_FILES[covariance_label]),
        "covariance_mode": "full",
        "rows_raw": rows,
        "z": z,
        "H": h_obs,
        "sigma": sigma,
        "covariance": covariance,
    }


def load_source_hz32_diagonal_dataset(source_lock: dict[str, Any]) -> dict[str, Any]:
    rows = source_lock["cc32_rows"]
    z = np.asarray([float(row["z"]) for row in rows], dtype=float)
    h_obs = np.asarray([float(row["H"]) for row in rows], dtype=float)
    sigma = np.asarray([float(row["sigma"]) for row in rows], dtype=float)
    return {
        "dataset_label": "source_CC32_diagonal_sensitivity",
        "role": "diagonal_sensitivity",
        "data_path": str(source_lock["cc32_csv"]),
        "covariance_label": "diagonal_sigma",
        "covariance_path": "",
        "covariance_mode": "diagonal",
        "rows_raw": rows,
        "z": z,
        "H": h_obs,
        "sigma": sigma,
        "covariance": np.diag(sigma * sigma),
    }


def datasets_to_score(source_lock: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        load_source_hz15_dataset(source_lock, "suggested", PRIMARY_DATASET, "primary"),
        load_source_hz15_dataset(source_lock, "diagonal_total_error", "source_CC15_BC03_diagonal_total_error_sensitivity", "covariance_sensitivity"),
        load_source_hz15_dataset(source_lock, "conservative", "source_CC15_BC03_conservative_sensitivity", "covariance_sensitivity"),
        load_source_hz15_dataset(source_lock, "extra_conservative", "source_CC15_BC03_extra_conservative_sensitivity", "covariance_sensitivity"),
        load_source_hz15_dataset(source_lock, "nonstat_systematic_only", "source_CC15_BC03_nonstat_systematic_only_diagnostic", "diagnostic_only"),
        load_source_hz32_diagonal_dataset(source_lock),
    ]


def source_register_rows(script_path: Path, source_lock: dict[str, Any], run_dir: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        SCRIPT_DIR / "Hz_radial_expansion_smoke.py",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        WORK_DIR / "125-BAO-shape-theorem-target-or-non-CMB-stress-route.md",
        WORK_DIR / "126-Hz-radial-expansion-smoke.md",
        WORK_DIR / "129-noCMB-radial-robustness-or-growth-route.md",
        WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md",
        RUNS_ROOT / "20260531-214500-frozen-branch-empirical-holdout-scorecard" / "status.json",
        Path(source_lock["manifest"]["cc32_raw_path"]),
        Path(source_lock["manifest"]["cc32_normalized_csv"]),
        Path(source_lock["manifest"]["cc15_raw_path"]),
        Path(source_lock["manifest"]["cc15_normalized_csv"]),
        Path(source_lock["manifest_path"]),
        hzsmoke.HZ_32,
        hzsmoke.HZ_15,
        hzsmoke.SOURCE_METADATA,
        *hzsmoke.COVARIANCE_FILES.values(),
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


def source_url_rows() -> list[dict[str, Any]]:
    return [
        {
            "source": "CC32_full_table",
            "url": CC32_URL,
            "context_url": CC32_SOURCE_PAGE,
            "role": "source fetch for diagonal sensitivity",
            "caveat": "source page says full covariance is not provided",
        },
        {
            "source": "CC15_BC03_covariance_branch",
            "url": CC15_BC03_URL,
            "context_url": CC15_RECIPE_REPO,
            "role": "source fetch for covariance-branch row lock",
            "caveat": "covariance recipe files remain local precomputed matrices from the recipe branch",
        },
    ]


def score_models(datasets: list[dict[str, Any]], max_iter: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    fit_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    residual_rows: list[dict[str, Any]] = []
    for dataset in datasets:
        for model in MODEL_ORDER:
            fit, edges, residual, predicted = hzsmoke.fit_model(dataset, model, max_iter)
            fit["claim_ceiling"] = CLAIM_CEILING
            fit_rows.append(fit)
            edge_rows.extend(edges)
            residual_rows.extend(hzsmoke.residual_rows_for_fit(dataset, fit, residual, predicted))
    return fit_rows, edge_rows, residual_rows


def boolish(value: Any) -> bool:
    return value in [True, "True", "true", "1", 1]


def decision_rows(
    fit_rows: list[dict[str, Any]], comparisons: list[dict[str, Any]], row_locks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    primary_fits = [row for row in fit_rows if row["dataset_label"] == PRIMARY_DATASET]
    primary_locked = next(row for row in primary_fits if row["model"] == "MTS_locked_2over27")
    primary_lcdm = next(row for row in primary_fits if row["model"] == "LCDM")
    primary_comparisons = [row for row in comparisons if row["dataset_label"] == PRIMARY_DATASET]
    bic_vs_lcdm = next(row for row in primary_comparisons if row["reference_model"] == "LCDM")
    delta_bic_lcdm = float(bic_vs_lcdm["delta_BIC"])
    locked_lcdm_edges = any(
        boolish(row["edge_flag"])
        for row in primary_fits
        if row["model"] in {"LCDM", "MTS_locked_2over27", "MTS_Bmem_zero"}
    )
    all_lcdm_comparisons = [row for row in comparisons if row["reference_model"] == "LCDM"]
    preferred_count = sum(float(row["delta_BIC"]) <= -2.0 for row in all_lcdm_comparisons)
    draw_count = sum(-2.0 < float(row["delta_BIC"]) < 2.0 for row in all_lcdm_comparisons)
    disfavored_count = sum(float(row["delta_BIC"]) >= 2.0 for row in all_lcdm_comparisons)

    if locked_lcdm_edges:
        status = "fresh_CC_source_locked_Hz_holdout_edge_flagged"
    elif delta_bic_lcdm <= -2.0:
        status = "fresh_CC_source_locked_Hz_holdout_preferred_vs_LCDM"
    elif delta_bic_lcdm < 2.0:
        status = "fresh_CC_source_locked_Hz_holdout_competitive_draw"
    else:
        status = "fresh_CC_source_locked_Hz_holdout_disfavored_vs_LCDM"

    return [
        {
            "item": "status",
            "verdict": status,
            "evidence": f"primary delta_BIC_vs_LCDM={delta_bic_lcdm:.12g}; locked chi2={float(primary_locked['chi2']):.12g}; LCDM chi2={float(primary_lcdm['chi2']):.12g}",
        },
        {
            "item": "source_lock",
            "verdict": "pass" if all(row["status"] == "pass" for row in row_locks) else "warn",
            "evidence": "; ".join(f"{row['dataset']}={row['status']}" for row in row_locks),
        },
        {
            "item": "all_Hz_vs_LCDM_card",
            "verdict": "draw_or_better" if disfavored_count == 0 else "mixed",
            "evidence": f"preferred={preferred_count}; draws={draw_count}; disfavored={disfavored_count}",
        },
        {
            "item": "frozen_branch_rule",
            "verdict": "pass",
            "evidence": f"B_mem fixed at {LOCKED_B_MEM}; no H(z) amplitude refit parameter",
        },
        {
            "item": "claim_status",
            "verdict": "H_z_holdout_only_no_theory_or_CMB_promotion",
            "evidence": "cosmic chronometer scoring only; no BAO/CMB/local-GR/theory promotion",
        },
        {
            "item": "next_target",
            "verdict": "official_likelihood_or_growth_covariance_holdout",
            "evidence": "H(z) source-locked result is a late-time draw, so next useful empirical pressure is official likelihood/growth covariance",
        },
    ]


def gate_rows(
    source_lock: dict[str, Any],
    row_locks: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    primary_delta = float(
        next(
            row["delta_BIC"]
            for row in comparisons
            if row["dataset_label"] == PRIMARY_DATASET and row["reference_model"] == "LCDM"
        )
    )
    decision_status = next(row["verdict"] for row in decisions if row["item"] == "status")
    all_lcdm = [row for row in comparisons if row["reference_model"] == "LCDM"]
    disfavored_count = sum(float(row["delta_BIC"]) >= 2.0 for row in all_lcdm)
    return [
        {
            "gate": "source_fetch",
            "status": "pass",
            "evidence": f"CC32 rows={source_lock['manifest']['cc32_rows']}; CC15 rows={source_lock['manifest']['cc15_rows']}",
        },
        {
            "gate": "row_lock_against_local_tables",
            "status": "pass" if all(row["status"] == "pass" for row in row_locks) else "warn",
            "evidence": "; ".join(f"{row['dataset']}:{row['status']}" for row in row_locks),
        },
        {
            "gate": "covariance_shapes_positive",
            "status": "pass" if all(row["status"] == "pass" for row in schema_rows) else "fail",
            "evidence": f"datasets checked={len(schema_rows)}",
        },
        {
            "gate": "frozen_B_mem_no_refit",
            "status": "pass",
            "evidence": f"B_mem={LOCKED_B_MEM}",
        },
        {
            "gate": "primary_Hz_not_disfavored_vs_LCDM",
            "status": "pass" if primary_delta < 2.0 else "fail",
            "evidence": f"primary delta_BIC_vs_LCDM={primary_delta}",
        },
        {
            "gate": "all_Hz_sensitivities_not_disfavored_vs_LCDM",
            "status": "pass" if disfavored_count == 0 else "fail",
            "evidence": f"LCDM-comparison disfavored_count={disfavored_count}",
        },
        {
            "gate": "theory_promotion",
            "status": "fail",
            "evidence": f"{decision_status}; H(z) holdout cannot derive action/amplitude/CMB/local GR",
        },
    ]


def run_holdout(output_root: Path, timestamp: str | None = None, max_iter: int = 300) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-fresh-CC-Hz-source-locked-holdout"
    results_dir = run_dir / "results"
    intake_dir = SOURCE_INTAKE_ROOT / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)

    source_lock = fetch_and_lock_sources(intake_dir)
    row_locks = row_lock_rows(source_lock)
    datasets = datasets_to_score(source_lock)
    schema_rows = hzsmoke.data_schema_rows(datasets)
    fit_rows, edge_rows, residual_rows = score_models(datasets, max_iter)
    comparisons = hzsmoke.baseline_comparison_rows(fit_rows)
    controls = hzsmoke.control_rows(fit_rows)
    decisions = decision_rows(fit_rows, comparisons, row_locks)
    gates = gate_rows(source_lock, row_locks, schema_rows, comparisons, decisions)
    sources = source_register_rows(Path(__file__).resolve(), source_lock, run_dir)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing source paths after fetch: {missing}")

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "source_url_register.csv", source_url_rows(), ["source", "url", "context_url", "role", "caveat"])
    write_csv(
        results_dir / "row_lock_comparison.csv",
        row_locks,
        [
            "dataset",
            "source_rows",
            "local_rows",
            "reference_mismatch_count",
            "status",
            "max_abs_delta_z",
            "max_abs_delta_H",
            "max_abs_delta_sigma",
            "max_abs_delta_sigma_stat",
            "max_abs_delta_sigma_met",
        ],
    )
    write_csv(
        results_dir / "data_schema.csv",
        schema_rows,
        [
            "dataset_label",
            "role",
            "data_path",
            "covariance_path",
            "covariance_label",
            "rows",
            "covariance_shape",
            "z_min",
            "z_max",
            "min_eigenvalue",
            "positive_definite",
            "status",
        ],
    )
    write_csv(
        results_dir / "fit_summary.csv",
        fit_rows,
        [
            "dataset_label",
            "dataset_role",
            "covariance_label",
            "covariance_mode",
            "model",
            "success",
            "chi2",
            "AIC",
            "BIC",
            "n_data",
            "dynamic_k",
            "dof",
            "edge_flag",
            "Omega_m0",
            "h",
            "H0",
            "w",
            "w0",
            "wa",
            "optimizer",
            "optimizer_message",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "prior_edge_table.csv",
        edge_rows,
        ["dataset_label", "model", "parameter", "best_fit", "lower", "upper", "distance_to_edge", "edge_flag"],
    )
    write_csv(
        results_dir / "residuals.csv",
        residual_rows,
        [
            "dataset_label",
            "model",
            "row_index",
            "z",
            "H_observed",
            "H_predicted",
            "residual",
            "diagonal_sigma",
            "diagonal_pull",
            "cov_signed_chi2_contribution",
            "reference",
        ],
    )
    write_csv(
        results_dir / "baseline_comparisons.csv",
        comparisons,
        [
            "dataset_label",
            "model",
            "reference_model",
            "delta_chi2",
            "delta_AIC",
            "delta_BIC",
            "locked_edge_flag",
            "reference_edge_flag",
            "readout",
        ],
    )
    write_csv(results_dir / "control_reproduction.csv", controls, ["dataset_label", "control", "delta_chi2", "delta_Omega_m0", "delta_h", "status"])
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
        "primary_dataset": PRIMARY_DATASET,
        "source_urls": [CC32_URL, CC15_BC03_URL],
        "generated": [
            "source_register.csv",
            "source_url_register.csv",
            "row_lock_comparison.csv",
            "data_schema.csv",
            "fit_summary.csv",
            "prior_edge_table.csv",
            "residuals.csv",
            "baseline_comparisons.csv",
            "control_reproduction.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "146-official-likelihood-or-growth-covariance-holdout.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--max-iter", type=int, default=300)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_holdout(args.output_root, args.timestamp, args.max_iter))


if __name__ == "__main__":
    main()
