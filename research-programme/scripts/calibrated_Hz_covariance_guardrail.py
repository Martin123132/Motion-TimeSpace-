#!/usr/bin/env python3
"""Frozen CMB-calibrated C0 row against row-locked H(z) covariance guardrail."""

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


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_likelihood_smoke import e2_array  # noqa: E402


SOURCE_40_STATUS = Path("runs/20260531-010340-fresh-holdout-or-official-likelihood-roadmap/status.json")
SOURCE_38_STATUS = Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json")
BACKGROUND_RESULTS = MAIN_WORKBENCH / "runs/20260528-032713-cosmology-smoke-fit/results/smoke_fit_results.csv"
BRANCH_TABLE = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/Hz_CC_Moresco15_BC03.csv"
ROW_LOCK_MANIFEST = MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/row_lock_manifest.json"
VARIANTS = ["diagonal_total_error", "suggested", "conservative", "extra_conservative"]
BASELINES = ["LCDM_fixed_no_SH0ES", "wCDM_fixed_no_SH0ES", "CPL_fixed_no_SH0ES"]
LOCKED_C0 = "locked_C0_no_SH0ES"
NATIVE_CMB_CALIBRATED = "C0_native_bmem_CMB_calibrated_shape_frozen"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_float(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    return f"{number:.12g}" if math.isfinite(number) else ""


def background_specs() -> list[dict[str, Any]]:
    source_rows = read_csv(BACKGROUND_RESULTS)
    wanted = {
        "M0": ("LCDM_fixed_no_SH0ES", "M0"),
        "M2_wCDM": ("wCDM_fixed_no_SH0ES", "M2_wCDM"),
        "M2_CPL": ("CPL_fixed_no_SH0ES", "M2_CPL"),
        "M6_min_predeclared_fixed_shape": (LOCKED_C0, "M6"),
    }
    specs: list[dict[str, Any]] = []
    for row in source_rows:
        if row["branch"] != "no_sh0es" or row["mode"] != "fit" or row["success"] != "True":
            continue
        if row["model"] not in wanted:
            continue
        label, physics_model = wanted[row["model"]]
        specs.append(
            {
                "model": label,
                "physics_model": physics_model,
                "params": json.loads(row["params_json"]),
                "parameter_origin": "no_SH0ES_background_fit_reference",
                "claim_limit": "reference_only",
            }
        )
    return specs


def frozen_native_spec(source_38: dict[str, Any]) -> dict[str, Any]:
    return {
        "model": NATIVE_CMB_CALIBRATED,
        "physics_model": "M6",
        "params": json.loads(source_38["frozen_params_json"]),
        "parameter_origin": "CMB_calibrated_frozen_closure_from_38",
        "claim_limit": "Hz_guardrail_only_not_support",
    }


def data_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(BRANCH_TABLE):
        rows.append(
            {
                "index": int(row["branch_index"]),
                "z": float(row["z"]),
                "hz": float(row["H"]),
                "sigma": float(row["sigma"]),
                "reference": row.get("reference", ""),
            }
        )
    return rows


def read_matrix(path: Path) -> np.ndarray:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        matrix = np.asarray([[float(value) for value in row[1:]] for row in reader], dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or len(header) != matrix.shape[0] + 1:
        raise ValueError(f"matrix shape/header mismatch: {path}")
    return matrix


def matrix_paths() -> dict[str, Path]:
    manifest = load_json(ROW_LOCK_MANIFEST)
    paths: dict[str, Path] = {}
    for variant in VARIANTS:
        relative = Path(manifest["matrix_paths"][variant])
        paths[variant] = relative if relative.is_absolute() else MAIN_WORKBENCH / relative
    return paths


def h_model(physics_model: str, z: float, params: dict[str, float]) -> float:
    e2 = float(e2_array(physics_model, np.asarray([z], dtype=float), params)[0])
    return float(params["h0"]) * math.sqrt(e2) if e2 > 0.0 and math.isfinite(e2) else math.nan


def residual_vector(rows: list[dict[str, Any]], spec: dict[str, Any]) -> np.ndarray:
    params = {key: float(value) for key, value in spec["params"].items()}
    predicted = np.asarray([h_model(spec["physics_model"], row["z"], params) for row in rows], dtype=float)
    observed = np.asarray([row["hz"] for row in rows], dtype=float)
    return predicted - observed


def chi2_covariance(residual: np.ndarray, covariance: np.ndarray) -> tuple[float, np.ndarray]:
    lower = np.linalg.cholesky(covariance)
    y = np.linalg.solve(lower, residual)
    weighted = np.linalg.solve(lower.T, y)
    return float(residual @ weighted), weighted


def score_all(rows: list[dict[str, Any]], specs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scores: list[dict[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    paths = matrix_paths()
    for variant, matrix_path in paths.items():
        covariance = read_matrix(matrix_path)
        if covariance.shape[0] != len(rows):
            raise ValueError(f"matrix/data mismatch for {variant}: {covariance.shape[0]} vs {len(rows)}")
        variant_results: dict[str, dict[str, Any]] = {}
        for spec in specs:
            residual = residual_vector(rows, spec)
            chi2, weighted = chi2_covariance(residual, covariance)
            variant_results[spec["model"]] = {"chi2": chi2, "residual": residual, "weighted": weighted, "spec": spec}
        best_baseline = min(BASELINES, key=lambda model: variant_results[model]["chi2"])
        best_all = min(variant_results, key=lambda model: variant_results[model]["chi2"])
        locked_chi2 = variant_results[LOCKED_C0]["chi2"]
        native_chi2 = variant_results[NATIVE_CMB_CALIBRATED]["chi2"]
        for model, result in variant_results.items():
            spec = result["spec"]
            scores.append(
                {
                    "variant": variant,
                    "model": model,
                    "physics_model": spec["physics_model"],
                    "parameter_origin": spec["parameter_origin"],
                    "n_rows": len(rows),
                    "chi2_cov": result["chi2"],
                    "best_baseline_model": best_baseline,
                    "best_overall_model": best_all,
                    "delta_chi2_vs_best_baseline": result["chi2"] - variant_results[best_baseline]["chi2"],
                    "delta_chi2_vs_locked_C0": result["chi2"] - locked_chi2,
                    "delta_chi2_vs_native_CMB_calibrated": result["chi2"] - native_chi2,
                    "claim_limit": spec["claim_limit"],
                    "params_json": json.dumps(spec["params"], sort_keys=True),
                }
            )
            for row_index, data_row in enumerate(rows):
                diag_sigma = math.sqrt(float(covariance[row_index, row_index]))
                residuals.append(
                    {
                        "variant": variant,
                        "index": data_row["index"],
                        "z": data_row["z"],
                        "model": model,
                        "H_obs": data_row["hz"],
                        "residual_model_minus_obs": result["residual"][row_index],
                        "diag_sigma_from_covariance": diag_sigma,
                        "diag_pull": result["residual"][row_index] / diag_sigma,
                        "signed_weighted_chi2_component": result["residual"][row_index] * result["weighted"][row_index],
                        "reference": data_row["reference"],
                    }
                )
    return scores, residuals


def variant_summary_rows(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        subset = [row for row in scores if row["variant"] == variant]
        native = next(row for row in subset if row["model"] == NATIVE_CMB_CALIBRATED)
        locked = next(row for row in subset if row["model"] == LOCKED_C0)
        rows.append(
            {
                "variant": variant,
                "native_chi2": native["chi2_cov"],
                "locked_C0_chi2": locked["chi2_cov"],
                "native_delta_vs_locked_C0": native["delta_chi2_vs_locked_C0"],
                "native_delta_vs_best_baseline": native["delta_chi2_vs_best_baseline"],
                "best_baseline_model": native["best_baseline_model"],
                "best_overall_model": native["best_overall_model"],
                "row_subset": "Moresco15_BC03_not_full32",
            }
        )
    return rows


def gate_rows(source_40: dict[str, Any], summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    suggested = next(row for row in summary if row["variant"] == "suggested")
    worst_delta_locked = max(float(row["native_delta_vs_locked_C0"]) for row in summary)
    best_delta_locked = min(float(row["native_delta_vs_locked_C0"]) for row in summary)
    preferred_count = sum(1 for row in summary if float(row["native_delta_vs_locked_C0"]) <= 0.0)
    return [
        {
            "gate": "source_40_complete",
            "status": "pass" if source_40.get("readout") == "fresh_holdout_roadmap_selects_Hz_guardrail_official_CMB_not_ready" else "fail",
            "detail": str(source_40.get("readout")),
        },
        {
            "gate": "frozen_native_row_evaluated_all_covariances",
            "status": "pass" if len(summary) == len(VARIANTS) else "fail",
            "detail": f"variant_count={len(summary)}",
        },
        {
            "gate": "suggested_covariance_not_worse_than_locked_C0_by_2",
            "status": "pass" if float(suggested["native_delta_vs_locked_C0"]) <= 2.0 else "fail",
            "detail": f"delta={suggested['native_delta_vs_locked_C0']}; threshold=2",
        },
        {
            "gate": "all_covariances_not_worse_than_locked_C0_by_3",
            "status": "pass" if worst_delta_locked <= 3.0 else "fail",
            "detail": f"worst_delta={worst_delta_locked}; threshold=3",
        },
        {
            "gate": "native_preferred_over_locked_count",
            "status": "pass" if preferred_count >= 1 else "warn",
            "detail": f"preferred_count={preferred_count}; best_delta={best_delta_locked}",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "H(z) was previously used in corpus; this is a guardrail only",
        },
        {
            "gate": "official_CMB_problem_solved",
            "status": "fail",
            "detail": "official spectra/lensing likelihood and perturbation contract still missing",
        },
    ]


def decision_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    suggested = next(row for row in summary if row["variant"] == "suggested")
    worst_delta = max(float(row["native_delta_vs_locked_C0"]) for row in summary)
    pass_guardrail = float(suggested["native_delta_vs_locked_C0"]) <= 2.0 and worst_delta <= 3.0
    return [
        {
            "decision": "Hz_guardrail_status",
            "status": "passes_guardrail" if pass_guardrail else "fails_guardrail",
            "evidence": f"suggested_delta_vs_locked_C0={suggested['native_delta_vs_locked_C0']}; worst_delta={worst_delta}",
            "next_action": "if pass, package closure-candidate evidence ledger; if fail, demote CMB-calibrated route",
        },
        {
            "decision": "support_claim_status",
            "status": "forbidden",
            "evidence": "direct H(z) is a reused/semi-fresh guardrail, not a clean independent holdout",
            "next_action": "official CMB setup or fresh external growth acquisition before evidence language",
        },
        {
            "decision": "next_target",
            "status": "closure_candidate_ledger_or_official_setup",
            "evidence": "H(z) guardrail completes the local fixed-row guardrail stack",
            "next_action": "write 42-calibrated-closure-candidate-ledger.md if pass",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrated H(z) covariance guardrail.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_40 = load_json(POST_CHECKPOINT / SOURCE_40_STATUS)
    source_38 = load_json(POST_CHECKPOINT / SOURCE_38_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-calibrated-Hz-covariance-guardrail"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    rows = data_rows()
    specs = background_specs() + [frozen_native_spec(source_38)]
    scores, residuals = score_all(rows, specs)
    summary = variant_summary_rows(scores)
    gates = gate_rows(source_40, summary)
    decisions = decision_rows(summary)
    suggested = next(row for row in summary if row["variant"] == "suggested")
    pass_guardrail = next(row for row in decisions if row["decision"] == "Hz_guardrail_status")["status"] == "passes_guardrail"

    write_csv(results_dir / "Hz_covariance_guardrail_scores.csv", scores, list(scores[0].keys()))
    write_csv(results_dir / "Hz_covariance_guardrail_residuals.csv", residuals, list(residuals[0].keys()))
    write_csv(results_dir / "Hz_covariance_variant_summary.csv", summary, list(summary[0].keys()))
    write_csv(results_dir / "Hz_covariance_guardrail_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    readout = (
        "calibrated_Hz_covariance_guardrail_passes_not_support"
        if pass_guardrail
        else "calibrated_Hz_covariance_guardrail_fails_demote_closure"
    )
    status = {
        "status": "complete_calibrated_Hz_covariance_guardrail",
        "readout": readout,
        "recommendation": "write_closure_candidate_ledger_or_demote_next",
        "next_target": "42-calibrated-closure-candidate-ledger.md" if pass_guardrail else "42-calibrated-closure-demotion.md",
        "suggested_covariance_native_delta_vs_locked_C0": suggested["native_delta_vs_locked_C0"],
        "suggested_covariance_native_delta_vs_best_baseline": suggested["native_delta_vs_best_baseline"],
        "row_subset": "Moresco15_BC03_not_full32",
        "guardrail_claim_only": True,
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "Hz_covariance_guardrail_scores": str(results_dir / "Hz_covariance_guardrail_scores.csv"),
            "Hz_covariance_guardrail_residuals": str(results_dir / "Hz_covariance_guardrail_residuals.csv"),
            "Hz_covariance_variant_summary": str(results_dir / "Hz_covariance_variant_summary.csv"),
            "Hz_covariance_guardrail_gates": str(results_dir / "Hz_covariance_guardrail_gates.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
