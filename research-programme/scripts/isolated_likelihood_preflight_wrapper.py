#!/usr/bin/env python3
"""Post-checkpoint likelihood preflight wrapper with no scoring."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_25_STATUS = Path("runs/20260530-235656-cosmology-preflight-safe-run-readout/status.json")
DEFAULT_PARSER_STATUS = Path(
    "runs/20260530-235530-cosmology-preflight-safe-run/parser-smoke-no-score/status.json"
)
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
DEFAULT_CONFIG = (
    MAIN_WORKBENCH
    / "runs"
    / "20260528-225042-growth-CMB-holdout-dry-run-design"
    / "results"
    / "holdout_dry_run_config.json"
)
FORBIDDEN = {"model_scores.csv", "growth_predictions.csv", "CMB_distance_scores.csv", "comparative_verdict.csv"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def forbidden_artifacts(root: Path) -> list[str]:
    if not root.exists():
        return []
    return [str(path) for path in root.rglob("*") if path.is_file() and path.name in FORBIDDEN]


def parameter_sources(models: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in models:
        if model == "MTS_C0_minimal_smooth_memory":
            background_source = "frozen MTS C0 background from predeclared branch; no growth/CMB refit in first score"
            perturbation_source = "fixed closure c_s2_Gamma=1; pi_Gamma=0; Q_m_nu=0"
            parameter_count_rule = "count inherited frozen background parameters plus zero new perturbation knobs"
        else:
            background_source = "same background-fit/import convention as C0 comparison branch"
            perturbation_source = "standard smooth dark-energy perturbation convention documented before scoring"
            parameter_count_rule = "count all fitted background and nuisance parameters used by this baseline"
        rows.append(
            {
                "model": model,
                "background_parameter_source": background_source,
                "perturbation_parameter_source": perturbation_source,
                "growth_data_source": "BAO-plus primary; Full-shape-only robustness only",
                "CMB_data_source": "Planck2018 distance-prior wCDM table",
                "parameter_count_rule": parameter_count_rule,
                "may_change_after_scores": False,
            }
        )
    return rows


def baseline_parity() -> list[dict[str, Any]]:
    return [
        {"criterion": "same_growth_rows", "requirement": "LCDM/wCDM/CPL/C0 use identical BAO-plus primary rows", "abort_if_failed": True},
        {"criterion": "same_CMB_rows", "requirement": "LCDM/wCDM/CPL/C0 use identical Planck wCDM distance-prior vector/covariance", "abort_if_failed": True},
        {"criterion": "same_covariance_math", "requirement": "all branches use identical residual^T C^-1 residual calculation", "abort_if_failed": True},
        {"criterion": "same_failure_flags", "requirement": "convergence/prior-edge/parser failures are reported for all models", "abort_if_failed": True},
        {"criterion": "same_information_criteria", "requirement": "Delta AIC/BIC are computed against LCDM, wCDM, and CPL with explicit k and n", "abort_if_failed": True},
        {"criterion": "no_asymmetric_jackknife", "requirement": "any jackknife/source split applied to C0 must also be applied to baselines", "abort_if_failed": True},
    ]


def nuisance_treatment() -> list[dict[str, Any]]:
    return [
        {"nuisance": "growth_amplitude_normalization", "treatment": "predeclare fitted/imported sigma8 or amplitude convention before scoring", "applies_to": "all models", "fit_allowed_in_first_score": True},
        {"nuisance": "sound_horizon_or_distance_scale", "treatment": "same r_d/H0 convention as background branch; no model-specific hidden prior", "applies_to": "all models", "fit_allowed_in_first_score": True},
        {"nuisance": "Planck_distance_prior_covariance", "treatment": "use validated wCDM covariance unchanged", "applies_to": "all models", "fit_allowed_in_first_score": False},
        {"nuisance": "ELG_grid_likelihood", "treatment": "excluded until parser exists", "applies_to": "all models", "fit_allowed_in_first_score": False},
        {"nuisance": "C0_perturbation_knobs", "treatment": "c_s2_Gamma pi_Gamma Q_m_nu fixed; no rescue knobs", "applies_to": "C0", "fit_allowed_in_first_score": False},
    ]


def information_rules() -> list[dict[str, Any]]:
    return [
        {"rule": "chi2_total", "definition": "chi2_growth_primary + chi2_CMB_distance_prior", "required": True},
        {"rule": "AIC", "definition": "AIC = chi2_total + 2*k", "required": True},
        {"rule": "BIC", "definition": "BIC = chi2_total + k*ln(n)", "required": True},
        {"rule": "delta_reference_set", "definition": "report deltas against fitted LCDM, wCDM, and CPL", "required": True},
        {"rule": "edge_flag_veto", "definition": "no branch with unresolved prior-edge or parser flags can be called stable evidence", "required": True},
        {"rule": "public_claim_veto", "definition": "first pass may give internal support/tension only, never parent-field proof", "required": True},
    ]


def output_contract() -> list[dict[str, Any]]:
    return [
        {"artifact": "status.json", "allowed_in_preflight": True, "allowed_in_first_score": True},
        {"artifact": "parameter_sources.csv", "allowed_in_preflight": True, "allowed_in_first_score": False},
        {"artifact": "baseline_parity_contract.csv", "allowed_in_preflight": True, "allowed_in_first_score": False},
        {"artifact": "nuisance_treatment_contract.csv", "allowed_in_preflight": True, "allowed_in_first_score": False},
        {"artifact": "information_criteria_rules.csv", "allowed_in_preflight": True, "allowed_in_first_score": False},
        {"artifact": "abort_conditions.csv", "allowed_in_preflight": True, "allowed_in_first_score": False},
        {"artifact": "model_scores.csv", "allowed_in_preflight": False, "allowed_in_first_score": True},
        {"artifact": "growth_predictions.csv", "allowed_in_preflight": False, "allowed_in_first_score": True},
        {"artifact": "CMB_distance_scores.csv", "allowed_in_preflight": False, "allowed_in_first_score": True},
        {"artifact": "comparative_verdict.csv", "allowed_in_preflight": False, "allowed_in_first_score": True},
    ]


def abort_conditions() -> list[dict[str, Any]]:
    return [
        {"abort_condition": "parser_shape_failure", "reason": "row/covariance dimensions must remain locked"},
        {"abort_condition": "BAO_plus_full_shape_double_counting", "reason": "primary and robustness branches are alternatives"},
        {"abort_condition": "ELG_grid_used_without_parser", "reason": "grid likelihood is explicitly blocked"},
        {"abort_condition": "C0_only_diagnostic", "reason": "baseline parity failure"},
        {"abort_condition": "forbidden_artifact_in_preflight", "reason": "preflight must not score"},
        {"abort_condition": "post_score_rule_change", "reason": "parameter/count/verdict rules must be frozen before scoring"},
        {"abort_condition": "strict_numeric_lock_missing", "reason": "post-checkpoint scoring still needs b_mem_pre/F_pre/baseline prior lock"},
    ]


def dependency_report(source_25: dict[str, Any], parser_status_path: Path, parser_status: dict[str, Any], config_path: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "dependency": "source_25_safe_run_readout",
            "path": str(Path(__file__).resolve().parents[1] / SOURCE_25_STATUS),
            "status": "pass" if source_25.get("readout") == "cosmology_preflight_safe_run_two_steps_passed_no_score_likelihood_wrapper_needed" else "fail",
            "detail": str(source_25.get("readout")),
        },
        {
            "dependency": "post_checkpoint_parser_status",
            "path": str(parser_status_path),
            "status": "pass" if parser_status.get("readout") == "growth_CMB_parser_smoke_dry_run_passed_no_score" else "fail",
            "detail": str(parser_status.get("readout")),
        },
        {
            "dependency": "holdout_config",
            "path": str(config_path),
            "status": "pass" if config.get("score_allowed") is False else "fail",
            "detail": f"models={';'.join(config.get('models', []))}; score_allowed={config.get('score_allowed')}",
        },
    ]


def gate_rows(parser_status: dict[str, Any], config: dict[str, Any], parity_rows: list[dict[str, Any]], info_rows: list[dict[str, Any]], forbidden: list[str]) -> list[dict[str, Any]]:
    models = config.get("models", [])
    return [
        {"criterion": "post_checkpoint_parser_passed", "status": "pass" if parser_status.get("readout") == "growth_CMB_parser_smoke_dry_run_passed_no_score" else "fail", "detail": str(parser_status.get("readout"))},
        {"criterion": "models_locked", "status": "pass" if models == ["LCDM", "wCDM", "CPL", "MTS_C0_minimal_smooth_memory"] else "fail", "detail": "; ".join(models)},
        {"criterion": "config_score_forbidden", "status": "pass" if config.get("score_allowed") is False else "fail", "detail": f"score_allowed={config.get('score_allowed')}"},
        {"criterion": "baseline_parity_locked", "status": "pass" if all(row["abort_if_failed"] for row in parity_rows) else "fail", "detail": f"criteria={len(parity_rows)}"},
        {"criterion": "information_rules_locked", "status": "pass" if all(row["required"] for row in info_rows) else "fail", "detail": f"rules={len(info_rows)}"},
        {"criterion": "forbidden_artifacts_absent", "status": "pass" if not forbidden else "fail", "detail": "; ".join(forbidden) if forbidden else "none"},
        {"criterion": "first_scoring_still_blocked_by_post_checkpoint_contract", "status": "pass", "detail": "wrapper locks likelihood preflight only; strict numeric lock is next"},
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Isolated no-score likelihood preflight wrapper.")
    parser.add_argument("--parser-status", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    parser_status_path = args.parser_status or root / DEFAULT_PARSER_STATUS
    config_path = args.config
    source_25 = load_json(root / SOURCE_25_STATUS)
    parser_status = load_json(parser_status_path)
    config = load_json(config_path)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-isolated-likelihood-preflight-wrapper"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    models = config["models"]
    rows_parameter = parameter_sources(models)
    rows_parity = baseline_parity()
    rows_nuisance = nuisance_treatment()
    rows_info = information_rules()
    rows_output = output_contract()
    rows_abort = abort_conditions()
    rows_dependency = dependency_report(source_25, parser_status_path, parser_status, config_path, config)
    forbidden = forbidden_artifacts(out_dir)
    gates = gate_rows(parser_status, config, rows_parity, rows_info, forbidden)
    contract_passed = all(row["status"] == "pass" for row in gates)

    write_csv(results_dir / "parameter_sources.csv", rows_parameter, list(rows_parameter[0].keys()))
    write_csv(results_dir / "baseline_parity_contract.csv", rows_parity, list(rows_parity[0].keys()))
    write_csv(results_dir / "nuisance_treatment_contract.csv", rows_nuisance, list(rows_nuisance[0].keys()))
    write_csv(results_dir / "information_criteria_rules.csv", rows_info, list(rows_info[0].keys()))
    write_csv(results_dir / "output_contract.csv", rows_output, list(rows_output[0].keys()))
    write_csv(results_dir / "abort_conditions.csv", rows_abort, list(rows_abort[0].keys()))
    write_csv(results_dir / "wrapper_dependency_report.csv", rows_dependency, list(rows_dependency[0].keys()))
    write_csv(results_dir / "likelihood_preflight_gate_criteria.csv", gates, list(gates[0].keys()))

    readout = "isolated_likelihood_preflight_locked_no_score_scoring_still_blocked" if contract_passed else "isolated_likelihood_preflight_blocked"
    status = {
        "status": "complete_isolated_likelihood_preflight_wrapper",
        "readout": readout,
        "recommendation": "lock_strict_numeric_branch_next" if contract_passed else "repair_isolated_likelihood_preflight",
        "next_target": "27-strict-cosmology-numeric-lock.md" if contract_passed else "repair_26_isolated_likelihood_preflight_wrapper",
        "parser_status_path": str(parser_status_path),
        "config_path": str(config_path),
        "data_fit_performed": False,
        "fit_allowed_now": False,
        "likelihood_contract_passed": contract_passed,
        "first_scoring_run_allowed_next": False,
        "scoring_run_allowed_now": False,
        "long_run_allowed_now": False,
        "empirical_claim_allowed_now": False,
        "claim_limit_now": "L0_control",
        "models": models,
        "forbidden_artifacts_found": forbidden,
        "outputs": {
            "parameter_sources": str(results_dir / "parameter_sources.csv"),
            "baseline_parity_contract": str(results_dir / "baseline_parity_contract.csv"),
            "nuisance_treatment_contract": str(results_dir / "nuisance_treatment_contract.csv"),
            "information_criteria_rules": str(results_dir / "information_criteria_rules.csv"),
            "output_contract": str(results_dir / "output_contract.csv"),
            "abort_conditions": str(results_dir / "abort_conditions.csv"),
            "wrapper_dependency_report": str(results_dir / "wrapper_dependency_report.csv"),
            "likelihood_preflight_gate_criteria": str(results_dir / "likelihood_preflight_gate_criteria.csv"),
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
