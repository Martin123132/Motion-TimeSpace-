#!/usr/bin/env python3
"""Predeclare no-rescue holdout rules for the CMB-calibrated closure row."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
MAIN_SCRIPTS = MAIN_WORKBENCH / "scripts"
sys.path.insert(0, str(MAIN_SCRIPTS))

from growth_CMB_first_scoring_run import SOURCE_161_CONFIG, load_json  # noqa: E402


SOURCE_37_STATUS = Path("runs/20260531-005015-CMB-calibrated-joint-growth-stress/status.json")
SOURCE_37_RESULTS = Path("runs/20260531-005015-CMB-calibrated-joint-growth-stress/results")
NATIVE_BRANCH = "C0_native_bmem_CMB_calibrated_shape_frozen"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def native_score_row() -> dict[str, str]:
    scores = read_csv(POST_CHECKPOINT / SOURCE_37_RESULTS / "joint_growth_CMB_same_parameter_scores.csv")
    return next(row for row in scores if row["model"] == NATIVE_BRANCH)


def frozen_parameter_manifest(row: dict[str, str]) -> list[dict[str, Any]]:
    params = json.loads(row["params_json"])
    lock_reasons = {
        "h0": "CMB-calibrated closure value; cannot move without redoing the training step",
        "omega_m0": "CMB-calibrated closure value; defines the tested background",
        "b_mem": "CMB-calibrated memory amplitude; the main closure clue under test",
        "alpha_act": "frozen fixed-shape value inherited from the predeclared M6_min shape",
        "nu_act": "frozen fixed-shape value inherited from the predeclared M6_min shape",
        "rd": "late-background BAO sound-scale parameter from source row; holdout must declare whether used",
    }
    rows: list[dict[str, Any]] = []
    for parameter in ["h0", "omega_m0", "b_mem", "alpha_act", "nu_act", "rd"]:
        rows.append(
            {
                "branch": NATIVE_BRANCH,
                "parameter": parameter,
                "frozen_value": params.get(parameter, ""),
                "status": "frozen_no_rescue",
                "lock_reason": lock_reasons[parameter],
                "allowed_to_vary_in_holdout": False,
            }
        )
    rows.append(
        {
            "branch": NATIVE_BRANCH,
            "parameter": "sigma8_0",
            "frozen_value": row["sigma8_0_fit_primary"],
            "status": "nuisance_predeclared",
            "lock_reason": "growth-amplitude nuisance; may be fit only if each baseline gets identical one-parameter treatment",
            "allowed_to_vary_in_holdout": "same_rule_for_all_models_only",
        }
    )
    return rows


def consumed_data_register(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "data_block": "Planck_2018_compressed_distance_prior",
            "role_so_far": "training_for_CMB_calibrated_row",
            "independent_holdout_status": "not_independent",
            "path_or_count": str(MAIN_WORKBENCH / "data/cosmology/growth_CMB/planck2018_distance_priors"),
            "rule": "cannot be reused as proof of model selection after calibration",
        },
        {
            "data_block": "SDSS_eBOSS_DR16_BAO_plus_growth",
            "role_so_far": "same_parameter_closure_stress",
            "independent_holdout_status": "already_touched",
            "path_or_count": len(config["primary_growth_files"]),
            "rule": "use only as context unless a new split was predeclared before scoring",
        },
        {
            "data_block": "SDSS_eBOSS_DR16_full_shape_growth",
            "role_so_far": "same_parameter_closure_stress",
            "independent_holdout_status": "already_touched",
            "path_or_count": len(config["robustness_growth_files"]),
            "rule": "use only as robustness context; not fresh evidence",
        },
        {
            "data_block": "Pantheon_plus_DESI_late_background",
            "role_so_far": "original no-SH0ES background basin source",
            "independent_holdout_status": "backreaction_guardrail_available_not_independent",
            "path_or_count": "formalization-workbench cosmology smoke-fit data",
            "rule": "can test whether CMB calibration wrecks late background, but not a fresh discovery claim",
        },
        {
            "data_block": "official_CMB_spectra_lensing_or_ACT",
            "role_so_far": "not_run",
            "independent_holdout_status": "stronger_likelihood_route",
            "path_or_count": "not configured locally",
            "rule": "fixed parameters only; no perturbation knobs unless parent-derived before run",
        },
    ]
    return rows


def no_rescue_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule": "freeze_calibrated_row",
            "allowed": True,
            "forbidden_action": "changing h0, omega_m0, b_mem, alpha_act, or nu_act after seeing any holdout residual",
            "consequence_if_violated": "restart as a new training branch; previous holdout becomes invalid",
        },
        {
            "rule": "same_baseline_treatment",
            "allowed": True,
            "forbidden_action": "giving C0 a nuisance, prior, covariance choice, or data cut not given to LCDM/wCDM/CPL",
            "consequence_if_violated": "result becomes pipeline debugging only",
        },
        {
            "rule": "sigma8_nuisance_limited",
            "allowed": "only_if_predeclared_for_all_models",
            "forbidden_action": "using growth-amplitude fitting to hide background-shape failure",
            "consequence_if_violated": "growth comparison cannot be claimed even internally",
        },
        {
            "rule": "CMB_prior_reuse_limit",
            "allowed": "diagnostic_only",
            "forbidden_action": "claiming the compressed CMB prior as an independent success after calibrating on it",
            "consequence_if_violated": "support claim is void",
        },
        {
            "rule": "official_likelihood_knob_lock",
            "allowed": True,
            "forbidden_action": "adding c_s2_Gamma, pi_Gamma, Q_m_nu, N_eff, omega_b_h2, or n_s freedom without a parent derivation",
            "consequence_if_violated": "official-likelihood result is phenomenological only",
        },
        {
            "rule": "public_language_lock",
            "allowed": False,
            "forbidden_action": "using support, detection, proof, falsification, or beats-LCDM language",
            "consequence_if_violated": "overclaim relative to current evidence",
        },
    ]


def holdout_route_register() -> list[dict[str, Any]]:
    return [
        {
            "route": "late_background_backreaction_guardrail",
            "priority": 1,
            "current_status": "available_next",
            "test": "score the frozen native CMB-calibrated row on the no-SH0ES SN/BAO background path without moving parameters",
            "pass_condition": "does not catastrophically worsen SN/BAO versus locked C0 and baselines; no model-selection claim",
            "claim_allowed": "closure_guardrail_only",
        },
        {
            "route": "fresh_growth_or_RSD_holdout",
            "priority": 2,
            "current_status": "requires_new_or_untouched_data",
            "test": "use a growth/RSD dataset not used in checkpoint 37",
            "pass_condition": "native calibrated row remains within predeclared delta-chi2 tolerance versus baselines",
            "claim_allowed": "internal_holdout_clue_only",
        },
        {
            "route": "official_CMB_spectra_lensing_fixed_params",
            "priority": 3,
            "current_status": "requires_likelihood_setup",
            "test": "run Planck/ACT spectra or lensing with fixed calibrated background and no new perturbation freedoms",
            "pass_condition": "no severe peak/lensing/damping failure relative to calibrated baselines",
            "claim_allowed": "strong_stress_result_only_until_parent_perturbations_derived",
        },
        {
            "route": "parent_calibration_map_repair",
            "priority": 4,
            "current_status": "theory_required",
            "test": "derive H0/Omega_m0/b_mem map from L_cg, a_F, DeltaR, and endpoint trace law",
            "pass_condition": "calibrated row is predicted before empirical reuse",
            "claim_allowed": "derivation_claim_only_after_equation_gate",
        },
    ]


def gate_rows(source_37: dict[str, Any], frozen_rows: list[dict[str, Any]], routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frozen_count = sum(1 for row in frozen_rows if row["status"] == "frozen_no_rescue")
    available_routes = [row for row in routes if row["current_status"] == "available_next"]
    return [
        {
            "gate": "source_37_complete",
            "status": "pass" if source_37.get("readout") == "CMB_calibrated_closure_retained_growth_near_locked_not_evidence" else "fail",
            "detail": str(source_37.get("readout")),
        },
        {
            "gate": "native_calibrated_row_frozen",
            "status": "pass" if frozen_count >= 6 else "fail",
            "detail": f"frozen_no_rescue_parameter_count={frozen_count}",
        },
        {
            "gate": "no_rescue_rules_declared",
            "status": "pass",
            "detail": "parameter, nuisance, CMB-prior, official-likelihood, and public-language locks declared",
        },
        {
            "gate": "available_next_guardrail_exists",
            "status": "pass" if available_routes else "fail",
            "detail": "; ".join(row["route"] for row in available_routes) if available_routes else "none",
        },
        {
            "gate": "independent_support_claim_allowed",
            "status": "fail",
            "detail": "no independent holdout or parent map has been run",
        },
        {
            "gate": "public_claim_allowed",
            "status": "fail",
            "detail": "closure contract only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "calibrated_row_status",
            "status": "frozen_closure_candidate",
            "evidence": "checkpoint 37 retained growth proximity but not evidence",
            "next_action": "run late-background backreaction guardrail with frozen native calibrated row",
        },
        {
            "decision": "holdout_language_status",
            "status": "no_support_language",
            "evidence": "CMB prior was used to train the row",
            "next_action": "require fresh holdout or official likelihood before any evidence language",
        },
        {
            "decision": "next_target",
            "status": "background_backreaction_guardrail",
            "evidence": "available local data can test whether CMB calibration wrecks late SN/BAO consistency",
            "next_action": "create 39-calibrated-background-backreaction-guardrail.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Predeclare calibrated closure holdout contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_37 = load_json(POST_CHECKPOINT / SOURCE_37_STATUS)
    config = load_json(MAIN_WORKBENCH / SOURCE_161_CONFIG)
    native_row = native_score_row()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-calibrated-closure-holdout-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    frozen_rows = frozen_parameter_manifest(native_row)
    consumed_rows = consumed_data_register(config)
    rescue_rows = no_rescue_rules()
    route_rows = holdout_route_register()
    gates = gate_rows(source_37, frozen_rows, route_rows)
    decisions = decision_rows()

    write_csv(results_dir / "frozen_parameter_manifest.csv", frozen_rows, list(frozen_rows[0].keys()))
    write_csv(results_dir / "consumed_data_register.csv", consumed_rows, list(consumed_rows[0].keys()))
    write_csv(results_dir / "no_rescue_rules.csv", rescue_rows, list(rescue_rows[0].keys()))
    write_csv(results_dir / "holdout_route_register.csv", route_rows, list(route_rows[0].keys()))
    write_csv(results_dir / "holdout_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    readout = "calibrated_closure_holdout_contract_frozen_no_rescue"
    status = {
        "status": "complete_calibrated_closure_holdout_contract",
        "readout": readout,
        "recommendation": "run_frozen_calibrated_background_backreaction_guardrail_next",
        "next_target": "39-calibrated-background-backreaction-guardrail.md",
        "frozen_branch": NATIVE_BRANCH,
        "frozen_params_json": native_row["params_json"],
        "support_claim_allowed": False,
        "death_claim_allowed": False,
        "public_claim_allowed": False,
        "available_next_guardrail": "late_background_backreaction_guardrail",
        "outputs": {
            "frozen_parameter_manifest": str(results_dir / "frozen_parameter_manifest.csv"),
            "consumed_data_register": str(results_dir / "consumed_data_register.csv"),
            "no_rescue_rules": str(results_dir / "no_rescue_rules.csv"),
            "holdout_route_register": str(results_dir / "holdout_route_register.csv"),
            "holdout_gate_criteria": str(results_dir / "holdout_gate_criteria.csv"),
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
