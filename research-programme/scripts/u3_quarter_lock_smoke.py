#!/usr/bin/env python3
"""No-refit smoke test for the structural u3=1/4 activation lock."""

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
POST_SCRIPTS = POST_CHECKPOINT / "scripts"
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
sys.path.insert(0, str(POST_SCRIPTS))

import C2_activation_background_smoke as bg  # noqa: E402
import C2_activation_growth_CMB_retest as gc  # noqa: E402


SOURCE_PATHS = {
    "54_doc": Path("54-coherent-domain-and-u3-origin.md"),
    "54_status": Path("runs/20260531-103455-coherent-domain-and-u3-origin/status.json"),
    "54_u3_candidates": Path("runs/20260531-103455-coherent-domain-and-u3-origin/results/u3_candidate_ledger.csv"),
    "47_status": Path("runs/20260531-014459-C2-activation-background-smoke/status.json"),
    "47_scores": Path("runs/20260531-014459-C2-activation-background-smoke/results/C2_activation_background_scores.csv"),
    "48_status": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/status.json"),
    "48_scores": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/results/C2_activation_growth_CMB_scores.csv"),
}

ORIGINAL_LABEL = "C0_frozen_original_fractional_weibull"
FITTED_C2_LABEL = "C2_weibull_p3_match_N50"
QUARTER_LABEL = "C2_weibull_p3_u3_quarter_lock"
QUARTER_U3 = 0.25
SAMPLE_N = [0.05, 0.1, 0.2, 0.21500703361675252, 0.5, 1.0, 2.0]


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json_file(path: Path) -> dict[str, Any]:
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


def source_register_rows() -> list[dict[str, Any]]:
    paths: dict[str, Path] = dict(SOURCE_PATHS)
    paths.update(
        {
            "38_status": Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json"),
            "background_config": bg.CONFIG_PATH,
            "growth_CMB_config": gc.MAIN_WORKBENCH / gc.SOURCE_161_CONFIG,
            "Hz_table": bg.HZ_TABLE,
            "Hz_manifest": bg.HZ_MANIFEST,
        }
    )
    rows: list[dict[str, Any]] = []
    for key, path in paths.items():
        absolute = POST_CHECKPOINT / path if not path.is_absolute() else path
        rows.append({"source_key": key, "path": str(absolute), "exists": absolute.exists()})
    missing = [row["path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def weibull_p3_u3_quarter(load_n: np.ndarray) -> np.ndarray:
    scaled = np.maximum(load_n, 0.0) / QUARTER_U3
    return 1.0 - np.exp(-np.clip(scaled**3.0, 0.0, 745.0))


def activation_shape_rows(u_fit: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n_value in SAMPLE_N:
        fitted = 1.0 - math.exp(-((max(n_value, 0.0) / u_fit) ** 3.0))
        quarter = 1.0 - math.exp(-((max(n_value, 0.0) / QUARTER_U3) ** 3.0))
        rows.append(
            {
                "N": n_value,
                "F_fitted_C2": fitted,
                "F_quarter_lock": quarter,
                "delta_F_quarter_minus_fitted": quarter - fitted,
                "relative_delta_F_quarter_minus_fitted": (quarter - fitted) / fitted if fitted else "",
            }
        )
    return rows


def custom_specs(source_38: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    params = {key: float(value) for key, value in json.loads(source_38["frozen_params_json"]).items()}
    background_specs = bg.source_fit_rows()
    for spec in bg.repair_specs(source_38):
        if spec["label"] in {ORIGINAL_LABEL, FITTED_C2_LABEL}:
            background_specs.append(spec)
    background_specs.append(
        {
            "label": QUARTER_LABEL,
            "kind": "frozen_activation_candidate",
            "physics_model": "custom_M6",
            "params": dict(params),
            "activation_candidate": "weibull_p3_u3_quarter_lock",
            "activation_fn": weibull_p3_u3_quarter,
            "parameter_origin": "checkpoint_54_structural_u3_quarter_no_refit",
            "n_params_reference": 0,
            "claim_limit": "quarter_lock_guardrail_only",
        }
    )

    growth_specs = gc.fixed_specs(source_38)
    growth_specs.append(
        {
            "model": QUARTER_LABEL,
            "physics_model": "custom_M6",
            "params": dict(params),
            "activation_candidate": "weibull_p3_u3_quarter_lock",
            "activation_fn": weibull_p3_u3_quarter,
            "parameter_origin": "checkpoint_54_structural_u3_quarter_no_refit",
            "claim_limit": "quarter_lock_guardrail_only",
        }
    )
    return background_specs, growth_specs


def evaluate_background(specs: list[dict[str, Any]], integration_steps: int) -> list[dict[str, Any]]:
    config = bg.load_json(bg.CONFIG_PATH)
    sn = bg.load_pantheon(bg.REPO_ROOT, bg.select_dataset(config, "Pantheon"), branch="no_sh0es")
    bao = bg.load_bao(bg.REPO_ROOT, bg.select_dataset(config, "BAO"))
    hz_rows = bg.load_hz_rows()
    hz_cov = bg.read_hz_covariance()
    scores = [bg.evaluate_spec(spec, sn, bao, hz_rows, hz_cov, integration_steps) for spec in specs]
    bg.add_deltas(scores)
    fitted = next(row for row in scores if row["model"] == FITTED_C2_LABEL)
    for row in scores:
        row["delta_late_SN_BAO_vs_fitted_C2"] = float(row["chi2_late_SN_BAO"]) - float(fitted["chi2_late_SN_BAO"])
        row["delta_late_plus_Hz_vs_fitted_C2"] = float(row["chi2_late_plus_Hz"]) - float(fitted["chi2_late_plus_Hz"])
    return scores


def evaluate_growth_cmb(specs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    config = gc.load_json(gc.MAIN_WORKBENCH / gc.SOURCE_161_CONFIG)
    scores, growth_predictions, cmb_predictions = gc.score_all(config, specs)
    fitted = next(row for row in scores if row["model"] == FITTED_C2_LABEL)
    for row in scores:
        row["delta_growth_primary_vs_fitted_C2"] = float(row["chi2_growth_primary"]) - float(fitted["chi2_growth_primary"])
        row["delta_growth_full_shape_vs_fitted_C2"] = float(row["chi2_growth_full_shape_only"]) - float(
            fitted["chi2_growth_full_shape_only"]
        )
        row["delta_CMB_vs_fitted_C2"] = float(row["chi2_CMB_repaired"]) - float(fitted["chi2_CMB_repaired"])
        row["delta_Hz_vs_fitted_C2"] = float(row["chi2_Hz_suggested"]) - float(fitted["chi2_Hz_suggested"])
        row["delta_total_vs_fitted_C2"] = float(row["chi2_primary_growth_plus_CMB_plus_Hz"]) - float(
            fitted["chi2_primary_growth_plus_CMB_plus_Hz"]
        )
    return scores, growth_predictions, cmb_predictions


def comparison_rows(background_scores: list[dict[str, Any]], growth_scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bg_quarter = next(row for row in background_scores if row["model"] == QUARTER_LABEL)
    bg_fitted = next(row for row in background_scores if row["model"] == FITTED_C2_LABEL)
    gr_quarter = next(row for row in growth_scores if row["model"] == QUARTER_LABEL)
    gr_fitted = next(row for row in growth_scores if row["model"] == FITTED_C2_LABEL)
    return [
        {
            "metric": "late_SN_BAO",
            "fitted_C2": bg_fitted["chi2_late_SN_BAO"],
            "quarter_lock": bg_quarter["chi2_late_SN_BAO"],
            "delta_quarter_minus_fitted_C2": bg_quarter["delta_late_SN_BAO_vs_fitted_C2"],
            "threshold": 0.25,
            "status": "pass" if float(bg_quarter["delta_late_SN_BAO_vs_fitted_C2"]) <= 0.25 else "fail",
        },
        {
            "metric": "late_SN_BAO_Hz",
            "fitted_C2": bg_fitted["chi2_late_plus_Hz"],
            "quarter_lock": bg_quarter["chi2_late_plus_Hz"],
            "delta_quarter_minus_fitted_C2": bg_quarter["delta_late_plus_Hz_vs_fitted_C2"],
            "threshold": 0.35,
            "status": "pass" if float(bg_quarter["delta_late_plus_Hz_vs_fitted_C2"]) <= 0.35 else "fail",
        },
        {
            "metric": "growth_primary",
            "fitted_C2": gr_fitted["chi2_growth_primary"],
            "quarter_lock": gr_quarter["chi2_growth_primary"],
            "delta_quarter_minus_fitted_C2": gr_quarter["delta_growth_primary_vs_fitted_C2"],
            "threshold": 0.5,
            "status": "pass" if float(gr_quarter["delta_growth_primary_vs_fitted_C2"]) <= 0.5 else "fail",
        },
        {
            "metric": "growth_full_shape",
            "fitted_C2": gr_fitted["chi2_growth_full_shape_only"],
            "quarter_lock": gr_quarter["chi2_growth_full_shape_only"],
            "delta_quarter_minus_fitted_C2": gr_quarter["delta_growth_full_shape_vs_fitted_C2"],
            "threshold": 0.5,
            "status": "pass" if float(gr_quarter["delta_growth_full_shape_vs_fitted_C2"]) <= 0.5 else "fail",
        },
        {
            "metric": "CMB_distance_repaired",
            "fitted_C2": gr_fitted["chi2_CMB_repaired"],
            "quarter_lock": gr_quarter["chi2_CMB_repaired"],
            "delta_quarter_minus_fitted_C2": gr_quarter["delta_CMB_vs_fitted_C2"],
            "threshold": 1.0,
            "status": "pass" if float(gr_quarter["delta_CMB_vs_fitted_C2"]) <= 1.0 else "fail",
        },
        {
            "metric": "Hz_suggested",
            "fitted_C2": gr_fitted["chi2_Hz_suggested"],
            "quarter_lock": gr_quarter["chi2_Hz_suggested"],
            "delta_quarter_minus_fitted_C2": gr_quarter["delta_Hz_vs_fitted_C2"],
            "threshold": 0.25,
            "status": "pass" if float(gr_quarter["delta_Hz_vs_fitted_C2"]) <= 0.25 else "fail",
        },
        {
            "metric": "growth_CMB_Hz_total",
            "fitted_C2": gr_fitted["chi2_primary_growth_plus_CMB_plus_Hz"],
            "quarter_lock": gr_quarter["chi2_primary_growth_plus_CMB_plus_Hz"],
            "delta_quarter_minus_fitted_C2": gr_quarter["delta_total_vs_fitted_C2"],
            "threshold": 1.5,
            "status": "pass" if float(gr_quarter["delta_total_vs_fitted_C2"]) <= 1.5 else "fail",
        },
    ]


def gate_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures = [row for row in comparisons if row["status"] == "fail"]
    return [
        {
            "gate": "u3_quarter_no_refit_branch_evaluated",
            "status": "pass",
            "detail": "quarter-lock branch included in late background, growth, compressed CMB, and H(z) guardrails",
        },
        {
            "gate": "quarter_lock_not_materially_worse_than_fitted_C2",
            "status": "pass" if not failures else "fail",
            "detail": f"failed_metrics={[row['metric'] for row in failures]}",
        },
        {
            "gate": "model_freedom_reduced",
            "status": "pass",
            "detail": "u3 fixed to 1/4 rather than inherited from fitted N50",
        },
        {
            "gate": "u3_parent_derived",
            "status": "fail",
            "detail": "1/4 is empirically smoked and structurally motivated, not derived from parent action",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "official CMB, perturbations, amplitude, action owner, and parent scale theorem remain missing",
        },
    ]


def decision_rows(comparisons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures = [row for row in comparisons if row["status"] == "fail"]
    retained = not failures
    return [
        {
            "decision": "u3_quarter_lock_status",
            "status": "retained_as_less_free_closure_candidate" if retained else "demoted_by_smoke_guardrail",
            "evidence": "all no-refit guardrail deltas pass thresholds" if retained else f"failed metrics: {[row['metric'] for row in failures]}",
            "next_action": "try to derive u3=1/4 from a parent cell/coherence theorem" if retained else "return to fitted-u3 C2 branch",
        },
        {
            "decision": "claim_status",
            "status": "private_guardrail_only",
            "evidence": "quarter lock is not a parent derivation and does not create public support",
            "next_action": "keep closure language",
        },
        {
            "decision": "recommended_next_target",
            "status": "56-u3-quarter-parent-cell-theorem-attempt.md" if retained else "56-u3-scale-repair-or-demotion.md",
            "evidence": "fixed quarter branch survives enough to deserve derivation" if retained else "fixed quarter branch fails smoke",
            "next_action": "derive or reject the 3+1 cell normalization",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="u3=1/4 no-refit smoke.")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--integration-steps", type=int, default=2048)
    args = parser.parse_args()

    source_register = source_register_rows()
    source_38 = load_json_file(POST_CHECKPOINT / "runs/20260531-005438-calibrated-closure-holdout-contract/status.json")
    source_54 = load_json_file(absolute_source("54_status"))
    u_fit = float(source_54["key_metrics"]["u3_fit"])

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-u3-quarter-lock-smoke"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    background_specs, growth_specs = custom_specs(source_38)
    background_scores = evaluate_background(background_specs, args.integration_steps)
    growth_scores, growth_predictions, cmb_predictions = evaluate_growth_cmb(growth_specs)
    shape_rows = activation_shape_rows(u_fit)
    comparisons = comparison_rows(background_scores, growth_scores)
    gates = gate_rows(comparisons)
    decisions = decision_rows(comparisons)
    retained = next(row for row in decisions if row["decision"] == "u3_quarter_lock_status")["status"] == "retained_as_less_free_closure_candidate"

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "u3_quarter_background_scores.csv", background_scores, list(background_scores[0].keys()))
    write_csv(results_dir / "u3_quarter_growth_CMB_scores.csv", growth_scores, list(growth_scores[0].keys()))
    write_csv(results_dir / "u3_quarter_guardrail_comparison.csv", comparisons, list(comparisons[0].keys()))
    write_csv(results_dir / "u3_quarter_activation_shape.csv", shape_rows, list(shape_rows[0].keys()))
    write_csv(results_dir / "u3_quarter_growth_predictions.csv", growth_predictions, list(growth_predictions[0].keys()))
    write_csv(results_dir / "u3_quarter_CMB_predictions.csv", cmb_predictions, list(cmb_predictions[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    quarter_background = next(row for row in background_scores if row["model"] == QUARTER_LABEL)
    quarter_growth = next(row for row in growth_scores if row["model"] == QUARTER_LABEL)
    status = {
        "status": "complete_u3_quarter_lock_smoke",
        "readout": "u3_quarter_lock_retained_as_less_free_closure_candidate" if retained else "u3_quarter_lock_demoted_by_smoke",
        "recommendation": "attempt_u3_quarter_parent_cell_theorem_next" if retained else "return_to_fitted_u3_C2_branch",
        "next_target": "56-u3-quarter-parent-cell-theorem-attempt.md" if retained else "56-u3-scale-repair-or-demotion.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "key_metrics": {
            "u3_fitted_C2": u_fit,
            "u3_quarter_lock": QUARTER_U3,
            "frac_delta_u3_quarter_vs_fitted": (QUARTER_U3 - u_fit) / u_fit,
            "quarter_delta_late_plus_Hz_vs_fitted_C2": quarter_background["delta_late_plus_Hz_vs_fitted_C2"],
            "quarter_delta_growth_primary_vs_fitted_C2": quarter_growth["delta_growth_primary_vs_fitted_C2"],
            "quarter_delta_CMB_vs_fitted_C2": quarter_growth["delta_CMB_vs_fitted_C2"],
            "quarter_delta_Hz_vs_fitted_C2": quarter_growth["delta_Hz_vs_fitted_C2"],
            "quarter_delta_total_vs_fitted_C2": quarter_growth["delta_total_vs_fitted_C2"],
            "failed_guardrails": [row["metric"] for row in comparisons if row["status"] == "fail"],
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "u3_quarter_background_scores": str(results_dir / "u3_quarter_background_scores.csv"),
            "u3_quarter_growth_CMB_scores": str(results_dir / "u3_quarter_growth_CMB_scores.csv"),
            "u3_quarter_guardrail_comparison": str(results_dir / "u3_quarter_guardrail_comparison.csv"),
            "u3_quarter_activation_shape": str(results_dir / "u3_quarter_activation_shape.csv"),
            "u3_quarter_growth_predictions": str(results_dir / "u3_quarter_growth_predictions.csv"),
            "u3_quarter_CMB_predictions": str(results_dir / "u3_quarter_CMB_predictions.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
