#!/usr/bin/env python3
"""Guardrail: does the frozen CMB-calibrated C0 row wreck late-background SN/BAO?"""

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
REPO_ROOT = MAIN_WORKBENCH.parent
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from cosmology_likelihood_smoke import (  # noqa: E402
    bao_model_vector,
    chi2_bao,
    chi2_sn,
    load_bao,
    load_json,
    load_pantheon,
    select_dataset,
)


SOURCE_38_STATUS = Path("runs/20260531-005438-calibrated-closure-holdout-contract/status.json")
BACKGROUND_RESULTS = Path("runs/20260528-032713-cosmology-smoke-fit/results/smoke_fit_results.csv")
CONFIG_PATH = Path("runs/20260528-032702-minimal-memory-predeclared-validation/configs/no_sh0es_dr1_config.json")
NATIVE_BRANCH = "C0_native_bmem_CMB_calibrated_shape_frozen"
LOCKED_MODEL = "M6_min_predeclared_fixed_shape"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_fit_rows() -> list[dict[str, Any]]:
    rows = read_csv(MAIN_WORKBENCH / BACKGROUND_RESULTS)
    keep = {"M0": "LCDM_fixed_fit", "M2_wCDM": "wCDM_fixed_fit", "M2_CPL": "CPL_fixed_fit", LOCKED_MODEL: "locked_C0_no_SH0ES_fit"}
    out: list[dict[str, Any]] = []
    for row in rows:
        if row["branch"] != "no_sh0es" or row["mode"] != "fit" or row["success"] != "True" or row["model"] not in keep:
            continue
        physics_model = "M6" if row["model"] == LOCKED_MODEL else row["model"]
        out.append(
            {
                "label": keep[row["model"]],
                "source_model": row["model"],
                "physics_model": physics_model,
                "params": json.loads(row["params_json"]),
                "parameter_origin": "no_SH0ES_background_fit_reference",
                "n_params_reference": int(row["n_params"]),
                "claim_limit": "reference_only",
            }
        )
    return out


def frozen_native_spec(source_38: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": NATIVE_BRANCH,
        "source_model": NATIVE_BRANCH,
        "physics_model": "M6",
        "params": json.loads(source_38["frozen_params_json"]),
        "parameter_origin": "CMB_calibrated_frozen_closure_from_38",
        "n_params_reference": 0,
        "claim_limit": "guardrail_only_not_model_selection",
    }


def evaluate_fixed(spec: dict[str, Any], sn: dict[str, Any], bao: dict[str, Any], steps: int) -> dict[str, Any]:
    physics_model = str(spec["physics_model"])
    params = {key: float(value) for key, value in spec["params"].items()}
    sn_chi2, sn_offset = chi2_sn(physics_model, params, sn, steps)
    bao_chi2 = chi2_bao(physics_model, params, bao, steps)
    predicted_bao = bao_model_vector(physics_model, params, bao, steps)
    bao_fractional = bao["obs"] / predicted_bao - 1.0
    return {
        "model": spec["label"],
        "physics_model": physics_model,
        "parameter_origin": spec["parameter_origin"],
        "chi2_sn": sn_chi2,
        "chi2_bao": bao_chi2,
        "chi2_total": sn_chi2 + bao_chi2,
        "sn_offset": sn_offset,
        "bao_fractional_rms": float(np.sqrt(np.mean(bao_fractional**2))),
        "bao_fractional_max_abs": float(np.max(np.abs(bao_fractional))),
        "n_params_reference": spec["n_params_reference"],
        "claim_limit": spec["claim_limit"],
        "params_json": json.dumps(params, sort_keys=True),
    }


def add_deltas(rows: list[dict[str, Any]]) -> None:
    locked = next(row for row in rows if row["model"] == "locked_C0_no_SH0ES_fit")
    baselines = [row for row in rows if row["model"] in {"LCDM_fixed_fit", "wCDM_fixed_fit", "CPL_fixed_fit"}]
    best_baseline_total = min(baselines, key=lambda row: float(row["chi2_total"]))
    best_baseline_sn = min(baselines, key=lambda row: float(row["chi2_sn"]))
    best_baseline_bao = min(baselines, key=lambda row: float(row["chi2_bao"]))
    for row in rows:
        row["delta_sn_vs_locked_C0"] = float(row["chi2_sn"]) - float(locked["chi2_sn"])
        row["delta_bao_vs_locked_C0"] = float(row["chi2_bao"]) - float(locked["chi2_bao"])
        row["delta_total_vs_locked_C0"] = float(row["chi2_total"]) - float(locked["chi2_total"])
        row["delta_total_vs_best_fixed_baseline"] = float(row["chi2_total"]) - float(best_baseline_total["chi2_total"])
        row["best_fixed_baseline_total"] = best_baseline_total["model"]
        row["best_fixed_baseline_sn"] = best_baseline_sn["model"]
        row["best_fixed_baseline_bao"] = best_baseline_bao["model"]


def gate_rows(source_38: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    native = next(row for row in rows if row["model"] == NATIVE_BRANCH)
    return [
        {
            "gate": "source_38_complete",
            "status": "pass" if source_38.get("readout") == "calibrated_closure_holdout_contract_frozen_no_rescue" else "fail",
            "detail": str(source_38.get("readout")),
        },
        {
            "gate": "frozen_native_row_evaluated",
            "status": "pass" if math.isfinite(float(native["chi2_total"])) else "fail",
            "detail": f"chi2_total={native['chi2_total']}",
        },
        {
            "gate": "total_backreaction_not_catastrophic_vs_locked_C0",
            "status": "pass" if float(native["delta_total_vs_locked_C0"]) <= 10.0 else "fail",
            "detail": f"delta_total_vs_locked_C0={native['delta_total_vs_locked_C0']}; threshold=10",
        },
        {
            "gate": "SN_backreaction_not_catastrophic_vs_locked_C0",
            "status": "pass" if float(native["delta_sn_vs_locked_C0"]) <= 7.5 else "fail",
            "detail": f"delta_sn_vs_locked_C0={native['delta_sn_vs_locked_C0']}; threshold=7.5",
        },
        {
            "gate": "BAO_backreaction_not_catastrophic_vs_locked_C0",
            "status": "pass" if float(native["delta_bao_vs_locked_C0"]) <= 5.0 else "fail",
            "detail": f"delta_bao_vs_locked_C0={native['delta_bao_vs_locked_C0']}; threshold=5",
        },
        {
            "gate": "model_selection_claim_allowed",
            "status": "fail",
            "detail": "guardrail uses a CMB-trained closure row and late-background data connected to original shape selection",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "parent map and independent holdout remain missing",
        },
    ]


def decision_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    native = next(row for row in rows if row["model"] == NATIVE_BRANCH)
    passes_guardrail = (
        float(native["delta_total_vs_locked_C0"]) <= 10.0
        and float(native["delta_sn_vs_locked_C0"]) <= 7.5
        and float(native["delta_bao_vs_locked_C0"]) <= 5.0
    )
    return [
        {
            "decision": "late_background_backreaction_status",
            "status": "passes_guardrail" if passes_guardrail else "fails_guardrail",
            "evidence": f"delta_total_vs_locked_C0={native['delta_total_vs_locked_C0']}",
            "next_action": "if pass, package as frozen closure candidate for fresh/official holdout; if fail, demote CMB calibration route",
        },
        {
            "decision": "model_selection_status",
            "status": "forbidden",
            "evidence": "not an independent holdout and no parent map",
            "next_action": "do not compare AIC/BIC as evidence from this guardrail",
        },
        {
            "decision": "next_target",
            "status": "fresh_or_official_holdout_required" if passes_guardrail else "return_to_parent_map_repair",
            "evidence": "backreaction guardrail is only a consistency check",
            "next_action": "write 40-fresh-holdout-or-official-likelihood-roadmap.md if pass",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen CMB-calibrated row late-background backreaction guardrail.")
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--integration-steps", type=int, default=1024)
    args = parser.parse_args()

    source_38 = load_json(POST_CHECKPOINT / SOURCE_38_STATUS)
    config = load_json(MAIN_WORKBENCH / CONFIG_PATH)
    sn = load_pantheon(REPO_ROOT, select_dataset(config, "Pantheon"), branch="no_sh0es")
    bao = load_bao(REPO_ROOT, select_dataset(config, "BAO"))

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-calibrated-background-backreaction-guardrail"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    specs = source_fit_rows() + [frozen_native_spec(source_38)]
    scores = [evaluate_fixed(spec, sn, bao, args.integration_steps) for spec in specs]
    add_deltas(scores)
    gates = gate_rows(source_38, scores)
    decisions = decision_rows(scores)
    native = next(row for row in scores if row["model"] == NATIVE_BRANCH)
    passes_guardrail = next(row for row in decisions if row["decision"] == "late_background_backreaction_status")["status"] == "passes_guardrail"

    write_csv(results_dir / "background_backreaction_scores.csv", scores, list(scores[0].keys()))
    write_csv(results_dir / "background_backreaction_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    readout = (
        "calibrated_background_backreaction_guardrail_passes_not_evidence"
        if passes_guardrail
        else "calibrated_background_backreaction_guardrail_fails_demote_closure"
    )
    status = {
        "status": "complete_calibrated_background_backreaction_guardrail",
        "readout": readout,
        "recommendation": "fresh_or_official_holdout_required_next" if passes_guardrail else "repair_parent_calibration_map_before_more_data",
        "next_target": "40-fresh-holdout-or-official-likelihood-roadmap.md" if passes_guardrail else "40-parent-calibration-map-repair.md",
        "native_delta_total_vs_locked_C0": native["delta_total_vs_locked_C0"],
        "native_delta_sn_vs_locked_C0": native["delta_sn_vs_locked_C0"],
        "native_delta_bao_vs_locked_C0": native["delta_bao_vs_locked_C0"],
        "guardrail_claim_only": True,
        "model_selection_claim_allowed": False,
        "support_claim_allowed": False,
        "death_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "background_backreaction_scores": str(results_dir / "background_backreaction_scores.csv"),
            "background_backreaction_gate_criteria": str(results_dir / "background_backreaction_gate_criteria.csv"),
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
