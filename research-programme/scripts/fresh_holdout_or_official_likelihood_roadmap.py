#!/usr/bin/env python3
"""Choose the next stronger test route after the calibrated closure guardrails."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
MAIN_WORKBENCH = Path(__file__).resolve().parents[2] / "formalization-workbench"
SOURCE_39_STATUS = Path("runs/20260531-005921-calibrated-background-backreaction-guardrail/status.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def local_data_inventory_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "data_or_route": "cosmic_chronometers_covariance_branch",
            "local_path": MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/covariance_branch/Hz_CC_Moresco15_BC03.csv",
            "status": "local_available",
            "previously_used_in_corpus": True,
            "used_to_train_frozen_CMB_calibrated_row": False,
            "freshness_label": "semi_fresh_guardrail_not_support",
        },
        {
            "data_or_route": "cosmic_chronometers_full_Hz",
            "local_path": MAIN_WORKBENCH / "data/cosmology/cosmic_chronometers/Hz.csv",
            "status": "local_available",
            "previously_used_in_corpus": True,
            "used_to_train_frozen_CMB_calibrated_row": False,
            "freshness_label": "semi_fresh_guardrail_not_support",
        },
        {
            "data_or_route": "SDSS_eBOSS_growth_CMB_BAO_plus",
            "local_path": MAIN_WORKBENCH / "data/cosmology/growth_CMB/sdss_eboss_dr16/BAO-plus",
            "status": "local_available_consumed_by_checkpoint_37",
            "previously_used_in_corpus": True,
            "used_to_train_frozen_CMB_calibrated_row": False,
            "freshness_label": "consumed_stress_context",
        },
        {
            "data_or_route": "Planck_2018_compressed_distance_prior",
            "local_path": MAIN_WORKBENCH / "data/cosmology/growth_CMB/planck2018_distance_priors",
            "status": "local_available_training_data",
            "previously_used_in_corpus": True,
            "used_to_train_frozen_CMB_calibrated_row": True,
            "freshness_label": "not_holdout",
        },
        {
            "data_or_route": "official_CMB_spectra_lensing",
            "local_path": "",
            "status": "not_configured_locally",
            "previously_used_in_corpus": False,
            "used_to_train_frozen_CMB_calibrated_row": False,
            "freshness_label": "strong_route_requires_setup_and_parent_perturbation_contract",
        },
        {
            "data_or_route": "fresh_external_growth_RSD",
            "local_path": "",
            "status": "not_configured_locally",
            "previously_used_in_corpus": False,
            "used_to_train_frozen_CMB_calibrated_row": False,
            "freshness_label": "fresh_route_requires_acquisition_manifest",
        },
    ]
    rows: list[dict[str, Any]] = []
    for entry in entries:
        local_path = entry["local_path"]
        exists = bool(local_path) and Path(local_path).exists()
        rows.append(
            {
                "data_or_route": entry["data_or_route"],
                "local_path": str(local_path),
                "exists": exists,
                "status": entry["status"],
                "previously_used_in_corpus": entry["previously_used_in_corpus"],
                "used_to_train_frozen_CMB_calibrated_row": entry["used_to_train_frozen_CMB_calibrated_row"],
                "freshness_label": entry["freshness_label"],
            }
        )
    return rows


def route_score_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "calibrated_Hz_covariance_guardrail",
            "priority": 1,
            "information_gain": "medium",
            "local_feasibility": "high",
            "freshness": "semi_fresh_for_frozen_CMB_row_but_previously_touched",
            "risk": "cannot become support because H(z) was already studied in main path",
            "allowed_claim": "guardrail_only",
            "next_artifact": "41-calibrated-Hz-covariance-guardrail.md",
        },
        {
            "route": "official_CMB_spectra_lensing_fixed_params",
            "priority": 2,
            "information_gain": "very_high",
            "local_feasibility": "low_until_likelihood_setup_and_perturbations",
            "freshness": "strong_external_route",
            "risk": "background-only closure cannot be passed into full spectra without perturbation/early-sector contract",
            "allowed_claim": "strong_stress_only_until_parent_perturbations_derived",
            "next_artifact": "official-likelihood-setup-plan",
        },
        {
            "route": "fresh_external_growth_RSD_holdout",
            "priority": 3,
            "information_gain": "high",
            "local_feasibility": "medium_after_data_manifest",
            "freshness": "fresh_if_dataset_not_in_growth_CMB_folder",
            "risk": "must avoid selecting data because it is friendly",
            "allowed_claim": "internal_holdout_clue_only",
            "next_artifact": "fresh-growth-data-acquisition-manifest",
        },
        {
            "route": "parent_calibration_map_repair",
            "priority": 4,
            "information_gain": "foundational",
            "local_feasibility": "theory_work",
            "freshness": "not_empirical",
            "risk": "hard but necessary before support language",
            "allowed_claim": "derivation_only_if_equation_gate_passes",
            "next_artifact": "parent-calibration-map-repair",
        },
    ]


def official_likelihood_reference_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "Planck_2018_likelihood_code",
            "source": "ESA Planck Legacy Archive CMB spectrum and likelihood code",
            "url": "https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/CMB_spectrum_%26_Likelihood_Code",
            "local_status": "not_installed",
            "requirement_before_run": "Boltzmann/theory interface and nuisance-parameter policy",
        },
        {
            "component": "Cobaya_likelihood_framework",
            "source": "Cobaya likelihood documentation",
            "url": "https://cobaya.readthedocs.io/en/latest/cosmo_theories_likes.html",
            "local_status": "not_installed_for_MTS",
            "requirement_before_run": "define external likelihood/theory class or fixed-spectrum stress route",
        },
        {
            "component": "ACT_DR6_lensing_likelihood",
            "source": "NASA LAMBDA ACT DR6 likelihood data",
            "url": "https://lambda.gsfc.nasa.gov/product/act/actadv_dr6_lensing_lh_get.html",
            "local_status": "not_downloaded",
            "requirement_before_run": "fixed-parameter lensing prediction or official pipeline setup",
        },
        {
            "component": "ACT_DR6_data_products",
            "source": "ACT DR6 data products page",
            "url": "https://act.princeton.edu/act-dr6-data-products",
            "local_status": "not_downloaded",
            "requirement_before_run": "decide spectra/lensing target and no-new-knob perturbation contract",
        },
    ]


def no_rescue_holdout_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule": "freeze_native_CMB_calibrated_row",
            "detail": "use the exact 38 frozen h0/Omega_m0/b_mem/alpha_act/nu_act/rd row",
            "status": "required",
        },
        {
            "rule": "same_treatment_for_baselines",
            "detail": "LCDM/wCDM/CPL face the same data rows, covariance, nuisance rules, and cuts",
            "status": "required",
        },
        {
            "rule": "no_support_from_reused_data",
            "detail": "H(z) and late-background are guardrails because they were already touched in the wider corpus",
            "status": "required",
        },
        {
            "rule": "no_official_CMB_without_perturbation_contract",
            "detail": "no c_s2_Gamma, pi_Gamma, Q_m_nu, N_eff, omega_b_h2, or n_s freedom unless parent-derived first",
            "status": "required",
        },
        {
            "rule": "no_public_language",
            "detail": "no support/detection/falsification language until independent holdout or derivation gates pass",
            "status": "required",
        },
    ]


def gate_rows(source_39: dict[str, Any], inventory: list[dict[str, Any]], routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hz_available = any(row["data_or_route"] == "cosmic_chronometers_covariance_branch" and row["exists"] for row in inventory)
    selected = min(routes, key=lambda row: int(row["priority"]))
    return [
        {
            "gate": "source_39_complete",
            "status": "pass" if source_39.get("readout") == "calibrated_background_backreaction_guardrail_passes_not_evidence" else "fail",
            "detail": str(source_39.get("readout")),
        },
        {
            "gate": "local_Hz_guardrail_available",
            "status": "pass" if hz_available else "fail",
            "detail": "cosmic_chronometers_covariance_branch",
        },
        {
            "gate": "official_CMB_likelihood_ready_now",
            "status": "fail",
            "detail": "not configured locally and perturbation/early-sector contract missing",
        },
        {
            "gate": "fresh_external_growth_ready_now",
            "status": "fail",
            "detail": "requires acquisition manifest before run",
        },
        {
            "gate": "next_route_selected",
            "status": "pass" if selected["route"] == "calibrated_Hz_covariance_guardrail" else "fail",
            "detail": selected["route"],
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "roadmap only; no new independent holdout run",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "next_immediate_route",
            "status": "calibrated_Hz_covariance_guardrail",
            "evidence": "local row-locked covariance H(z) data exist and were not used to train the frozen CMB-calibrated row",
            "next_action": "run fixed-row H(z) covariance guardrail with no parameter rescue",
        },
        {
            "decision": "strong_route",
            "status": "official_CMB_likelihood_after_setup",
            "evidence": "Planck/ACT likelihoods are stronger but require external setup and perturbation contract",
            "next_action": "prepare official-likelihood setup only after fixed-row H(z) guardrail or parent perturbation contract",
        },
        {
            "decision": "claim_status",
            "status": "no_support_language",
            "evidence": "fresh independent holdout has not yet been run",
            "next_action": "keep closure-only language",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Fresh holdout or official likelihood roadmap.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_39 = load_json(POST_CHECKPOINT / SOURCE_39_STATUS)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-fresh-holdout-or-official-likelihood-roadmap"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    inventory = local_data_inventory_rows()
    routes = route_score_rows()
    references = official_likelihood_reference_rows()
    rules = no_rescue_holdout_rules()
    gates = gate_rows(source_39, inventory, routes)
    decisions = decision_rows()

    write_csv(results_dir / "local_data_inventory.csv", inventory, list(inventory[0].keys()))
    write_csv(results_dir / "route_scorecard.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "official_likelihood_reference_register.csv", references, list(references[0].keys()))
    write_csv(results_dir / "no_rescue_holdout_rules.csv", rules, list(rules[0].keys()))
    write_csv(results_dir / "roadmap_gate_criteria.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    readout = "fresh_holdout_roadmap_selects_Hz_guardrail_official_CMB_not_ready"
    status = {
        "status": "complete_fresh_holdout_or_official_likelihood_roadmap",
        "readout": readout,
        "recommendation": "run_calibrated_Hz_covariance_guardrail_next",
        "next_target": "41-calibrated-Hz-covariance-guardrail.md",
        "selected_immediate_route": "calibrated_Hz_covariance_guardrail",
        "strong_route": "official_CMB_spectra_lensing_fixed_params_after_setup",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "outputs": {
            "local_data_inventory": str(results_dir / "local_data_inventory.csv"),
            "route_scorecard": str(results_dir / "route_scorecard.csv"),
            "official_likelihood_reference_register": str(results_dir / "official_likelihood_reference_register.csv"),
            "no_rescue_holdout_rules": str(results_dir / "no_rescue_holdout_rules.csv"),
            "roadmap_gate_criteria": str(results_dir / "roadmap_gate_criteria.csv"),
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
