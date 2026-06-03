#!/usr/bin/env python3
"""Lock strict cosmology numerical inputs before any post-checkpoint score."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_26_STATUS = Path("runs/20260531-000031-isolated-likelihood-preflight-wrapper/status.json")
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
BACKGROUND_FIT_RESULTS = MAIN_WORKBENCH / "runs" / "20260528-032713-cosmology-smoke-fit" / "results" / "smoke_fit_results.csv"
MINIMAL_VALIDATION_STATUS = MAIN_WORKBENCH / "runs" / "20260528-032702-minimal-memory-predeclared-validation" / "status.json"

MODEL_MAP = {
    "LCDM": ("M0", "M0"),
    "wCDM": ("M2_wCDM", "M2_wCDM"),
    "CPL": ("M2_CPL", "M2_CPL"),
    "MTS_C0_minimal_smooth_memory": ("M6_min_predeclared_fixed_shape", "M6"),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_background_lock_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(BACKGROUND_FIT_RESULTS)
    locked_rows: list[dict[str, Any]] = []
    for public_model, (source_model, physics_model) in MODEL_MAP.items():
        matches = [
            row
            for row in source_rows
            if row["branch"] == "no_sh0es"
            and row["model"] == source_model
            and row["mode"] == "fit"
            and row["success"] == "True"
        ]
        if not matches:
            raise ValueError(f"missing no_sh0es fit row for {public_model}/{source_model}")
        source_row = matches[0]
        params = json.loads(source_row["params_json"])
        locked_rows.append(
            {
                "public_model": public_model,
                "source_model": source_model,
                "physics_model": physics_model,
                "branch": source_row["branch"],
                "mode": source_row["mode"],
                "n_params": source_row["n_params"],
                "h0": params.get("h0", ""),
                "omega_m0": params.get("omega_m0", ""),
                "rd": params.get("rd", ""),
                "w": params.get("w", ""),
                "w0": params.get("w0", ""),
                "wa": params.get("wa", ""),
                "b_mem": params.get("b_mem", ""),
                "alpha_act": params.get("alpha_act", ""),
                "nu_act": params.get("nu_act", ""),
                "params_json": json.dumps(params, sort_keys=True),
                "source_path": str(BACKGROUND_FIT_RESULTS),
                "fit_allowed_in_next_growth_CMB_score": False,
            }
        )
    return locked_rows


def mts_numeric_lock_rows(background_rows: list[dict[str, Any]], validation: dict[str, Any]) -> list[dict[str, Any]]:
    mts_row = next(row for row in background_rows if row["public_model"] == "MTS_C0_minimal_smooth_memory")
    frozen_shape = validation.get("frozen_shape", {})
    return [
        {
            "quantity": "h0",
            "locked_value": mts_row["h0"],
            "source": "no_sh0es_background_fit_row",
            "status": "locked_for_holdout_no_refit",
            "claim_limit": "background_fit_input_not_derivation",
        },
        {
            "quantity": "omega_m0",
            "locked_value": mts_row["omega_m0"],
            "source": "no_sh0es_background_fit_row",
            "status": "locked_for_holdout_no_refit",
            "claim_limit": "background_fit_input_not_derivation",
        },
        {
            "quantity": "rd",
            "locked_value": mts_row["rd"],
            "source": "no_sh0es_background_fit_row",
            "status": "locked_for_holdout_no_refit",
            "claim_limit": "background_fit_input_not_derivation",
        },
        {
            "quantity": "b_mem",
            "locked_value": mts_row["b_mem"],
            "source": "no_sh0es_background_fit_row",
            "status": "locked_for_holdout_no_refit",
            "claim_limit": "phenomenological_amplitude_not_parent_derived",
        },
        {
            "quantity": "alpha_act",
            "locked_value": mts_row["alpha_act"],
            "source": frozen_shape.get("source", "minimal_memory_predeclared_validation"),
            "status": "locked_shape_no_refit",
            "claim_limit": "predeclared_shape_not_parent_derived",
        },
        {
            "quantity": "nu_act",
            "locked_value": mts_row["nu_act"],
            "source": frozen_shape.get("source", "minimal_memory_predeclared_validation"),
            "status": "locked_shape_no_refit",
            "claim_limit": "predeclared_shape_not_parent_derived",
        },
        {
            "quantity": "c_s2_Gamma",
            "locked_value": 1,
            "source": "growth_CMB_contract",
            "status": "fixed_closure",
            "claim_limit": "closure_not_perturbation_derivation",
        },
        {
            "quantity": "pi_Gamma",
            "locked_value": 0,
            "source": "growth_CMB_contract",
            "status": "fixed_closure",
            "claim_limit": "closure_not_perturbation_derivation",
        },
        {
            "quantity": "Q_m_nu",
            "locked_value": 0,
            "source": "growth_CMB_contract",
            "status": "fixed_closure",
            "claim_limit": "closure_not_conservation_derivation",
        },
    ]


def branch_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "primary_branch",
            "locked_value": "no_sh0es_background_fit_then_growth_CMB_holdout",
            "reason": "avoids local-H0 calibration pressure as the first strict score",
            "forbidden_change": "switching to SH0ES branch after seeing growth/CMB residuals",
        },
        {
            "policy": "b_mem_sign",
            "locked_value": "positive_from_locked_no_sh0es_fit",
            "reason": "matches parent-boundary sign expectation and avoids sign chasing",
            "forbidden_change": "allowing sign-free b_mem in the first strict holdout score",
        },
        {
            "policy": "activation_parameters",
            "locked_value": "alpha_act and nu_act frozen; A_act excluded",
            "reason": "minimal memory branch uses fixed shape, not activation-amplitude rescue",
            "forbidden_change": "turning on A_act/M5/M6 shape freedom in the first score",
        },
        {
            "policy": "sigma8",
            "locked_value": "fit one sigma8_0 normalization per model on primary growth rows",
            "reason": "existing scorer treats growth normalization symmetrically",
            "forbidden_change": "model-specific hidden growth amplitude priors",
        },
        {
            "policy": "claim_level",
            "locked_value": "L0 now; at most L2/L3 after same-test score and robustness",
            "reason": "b_mem and shape are not parent-derived",
            "forbidden_change": "calling a score a parent-field derivation",
        },
    ]


def scoring_readiness_gate_rows(source_26: dict[str, Any], background_rows: list[dict[str, Any]], validation: dict[str, Any]) -> list[dict[str, Any]]:
    models_locked = [row["public_model"] for row in background_rows]
    return [
        {
            "gate": "source_26_complete",
            "status": "pass" if source_26.get("readout") == "isolated_likelihood_preflight_locked_no_score_scoring_still_blocked" else "fail",
            "detail": str(source_26.get("readout")),
        },
        {
            "gate": "background_rows_locked",
            "status": "pass" if models_locked == ["LCDM", "wCDM", "CPL", "MTS_C0_minimal_smooth_memory"] else "fail",
            "detail": "; ".join(models_locked),
        },
        {
            "gate": "frozen_shape_source_locked",
            "status": "pass" if validation.get("frozen_shape", {}).get("shape_refit") is False else "fail",
            "detail": json.dumps(validation.get("frozen_shape", {}), sort_keys=True),
        },
        {
            "gate": "mts_growth_CMB_refit_allowed",
            "status": "fail",
            "detail": "all listed C0/MTS background and memory parameters are frozen for the first holdout score",
        },
        {
            "gate": "scoring_run_executed_here",
            "status": "pass",
            "detail": "false; this stage only locks numeric inputs",
        },
        {
            "gate": "isolated_scoring_runner_available",
            "status": "fail",
            "detail": "existing scorer reads legacy source_163; next stage should make post-checkpoint runner or manifest",
        },
        {
            "gate": "empirical_claim_allowed_now",
            "status": "fail",
            "detail": "numeric locks are not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "numeric_lock_status",
            "status": "ready_for_scoring_manifest_not_score",
            "evidence": "no_SH0ES background rows and MTS memory parameters are frozen from existing source rows",
            "next_action": "create isolated first-score runner that consumes these locks",
        },
        {
            "decision": "b_mem_status",
            "status": "locked_phenomenological_amplitude",
            "evidence": "b_mem is fixed for the holdout but not parent-derived",
            "next_action": "do not upgrade above empirical fit/robustness without parent amplitude derivation",
        },
        {
            "decision": "scoring_status",
            "status": "blocked_until_runner",
            "evidence": "no score was run and existing first-score script points to legacy preflight",
            "next_action": "write 28-isolated-growth-CMB-first-score-runner.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict cosmology numeric lock.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_26 = load_json(root / SOURCE_26_STATUS)
    validation = load_json(MINIMAL_VALIDATION_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-strict-cosmology-numeric-lock"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    background_rows = load_background_lock_rows()
    mts_rows = mts_numeric_lock_rows(background_rows, validation)
    policies = branch_policy_rows()
    gates = scoring_readiness_gate_rows(source_26, background_rows, validation)
    decisions = decision_rows()

    write_csv(results_dir / "strict_background_numeric_lock.csv", background_rows, list(background_rows[0].keys()))
    write_csv(results_dir / "strict_mts_parameter_lock.csv", mts_rows, list(mts_rows[0].keys()))
    write_csv(results_dir / "strict_branch_policy_lock.csv", policies, list(policies[0].keys()))
    write_csv(results_dir / "strict_numeric_lock_gates.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "strict_numeric_lock_decision.csv", decisions, list(decisions[0].keys()))

    mts_row = next(row for row in background_rows if row["public_model"] == "MTS_C0_minimal_smooth_memory")
    readout = "strict_cosmology_numeric_lock_ready_for_scoring_manifest_no_score"
    status = {
        "status": "complete_strict_cosmology_numeric_lock",
        "readout": readout,
        "recommendation": "create_isolated_growth_CMB_first_score_runner_next",
        "next_target": "28-isolated-growth-CMB-first-score-runner.md",
        "locked_primary_branch": "no_sh0es_background_fit_then_growth_CMB_holdout",
        "locked_mts_params": {
            "h0": mts_row["h0"],
            "omega_m0": mts_row["omega_m0"],
            "rd": mts_row["rd"],
            "b_mem": mts_row["b_mem"],
            "alpha_act": mts_row["alpha_act"],
            "nu_act": mts_row["nu_act"],
            "c_s2_Gamma": 1,
            "pi_Gamma": 0,
            "Q_m_nu": 0,
        },
        "data_fit_performed": False,
        "fit_allowed_now": False,
        "scoring_run_allowed_now": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "L0_control",
        "claim_limit_after_score": "L2_fit_or_L3_robust_only_if_same-test_and_no_edge_flags",
        "outputs": {
            "strict_background_numeric_lock": str(results_dir / "strict_background_numeric_lock.csv"),
            "strict_mts_parameter_lock": str(results_dir / "strict_mts_parameter_lock.csv"),
            "strict_branch_policy_lock": str(results_dir / "strict_branch_policy_lock.csv"),
            "strict_numeric_lock_gates": str(results_dir / "strict_numeric_lock_gates.csv"),
            "strict_numeric_lock_decision": str(results_dir / "strict_numeric_lock_decision.csv"),
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
