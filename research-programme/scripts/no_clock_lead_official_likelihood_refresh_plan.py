#!/usr/bin/env python3
"""Plan a baseline-fair official-likelihood refresh for the no-clock lead branch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"
COSMOLOGY_DATA = FORMALIZATION_WORKBENCH / "data" / "cosmology"
DOWNLOAD_MANIFEST = COSMOLOGY_DATA / "download-manifest.json"
GROWTH_SOURCE_MANIFEST = COSMOLOGY_DATA / "growth_CMB" / "source_manifest.csv"

STATUS = "no_clock_lead_official_refresh_plan_locked"
CLAIM_CEILING = "no_clock_official_likelihood_refresh_plan_no_theory_or_CMB_promotion"


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
    if name.endswith("no_clock_lead_official_likelihood_refresh_plan.py"):
        return "current official-refresh planner"
    if name.startswith("144-"):
        return "lead empirical scorecard"
    if name.startswith("145-"):
        return "source-locked H(z) holdout"
    if name.startswith("146-"):
        return "source-locked growth covariance holdout"
    if name.startswith("147-"):
        return "ELG grid likelihood holdout"
    if name.startswith("148-"):
        return "promotion ceiling contract"
    if name.startswith("167-"):
        return "lead/sidecar governance source"
    if name.startswith("168-"):
        return "sidecar demotion/ownership gate"
    if name == "download-manifest.json":
        return "local SN/BAO data download manifest"
    if name == "source_manifest.csv":
        return "local growth/CMB source manifest"
    return "supporting source"


def source_paths(script_path: Path) -> list[Path]:
    return [
        script_path,
        WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
        WORK_DIR / "147-ELG-grid-likelihood-holdout.md",
        WORK_DIR / "148-perturbation-CMB-local-GR-promotion-contract.md",
        WORK_DIR / "167-no-clock-lead-and-pair-sidecar-test-plan.md",
        WORK_DIR / "168-pair-half-kernel-parent-ownership-gate.md",
        DOWNLOAD_MANIFEST,
        GROWTH_SOURCE_MANIFEST,
    ]


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in source_paths(script_path):
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


def normalize_hash(value: Any) -> str:
    return str(value or "").strip().lower()


def local_asset_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if DOWNLOAD_MANIFEST.exists():
        manifest = json.loads(DOWNLOAD_MANIFEST.read_text(encoding="utf-8-sig"))
        for entry in manifest:
            path = Path(entry["file"])
            expected = normalize_hash(entry.get("sha256"))
            exists = path.exists()
            actual = sha256_file(path).lower() if exists else ""
            rows.append(
                {
                    "manifest": "download-manifest.json",
                    "source_key": entry.get("source", ""),
                    "kind": "SN_BAO_asset",
                    "url": entry.get("url", ""),
                    "local_path": str(path),
                    "exists": "yes" if exists else "no",
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "hash_status": "pass" if exists and actual == expected else "fail",
                    "bytes": path.stat().st_size if exists else "",
                    "refresh_role": "hash-lock before official likelihood refresh",
                }
            )
    if GROWTH_SOURCE_MANIFEST.exists():
        for entry in read_csv_rows(GROWTH_SOURCE_MANIFEST):
            path = Path(entry["local_path"])
            expected = normalize_hash(entry.get("sha256"))
            exists = path.exists()
            actual = sha256_file(path).lower() if exists and path.is_file() else ""
            rows.append(
                {
                    "manifest": "source_manifest.csv",
                    "source_key": entry.get("source_id", ""),
                    "kind": entry.get("kind", ""),
                    "url": entry.get("remote_url", ""),
                    "local_path": str(path),
                    "exists": "yes" if exists else "no",
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "hash_status": "pass" if exists and actual == expected else "fail",
                    "bytes": path.stat().st_size if exists else "",
                    "refresh_role": "source-lock growth/CMB assets before any re-score",
                }
            )
    return rows


def official_source_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_key": "PantheonPlusSH0ES_DataRelease",
            "arena": "SN",
            "official_url": "https://github.com/PantheonPlusSH0ES/DataRelease",
            "local_status": "local_hash_locked",
            "current_role": "primary SN full-covariance shape and no-SH0ES/calibrator split source",
            "required_refresh_action": "re-fetch raw dat, stat+sys covariance, stat-only covariance, README; hash-lock; parse full covariance",
            "fairness_requirement": "same SN rows, covariance, calibrator policy, and nuisance offset for LCDM/wCDM/CPL/MTS",
            "claim_ceiling": "late-time SN support only",
        },
        {
            "source_key": "DESI_DR2_BAO_products",
            "arena": "BAO",
            "official_url": "https://data.desi.lbl.gov/doc/papers/dr2/",
            "local_status": "local_cobaya_hash_locked",
            "current_role": "primary BAO mean/covariance release target; local files currently from Cobaya bao_data mirror",
            "required_refresh_action": "confirm official DESI DR2 product location and mirror hash equivalence before scoring",
            "fairness_requirement": "same BAO mean vector, covariance, rd/rs convention, and BAO_alpha treatment for all branches",
            "claim_ceiling": "late-time BAO support only; no CMB ruler claim",
        },
        {
            "source_key": "CobayaSampler_bao_data_DESI_DR2",
            "arena": "BAO",
            "official_url": "https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2",
            "local_status": "local_hash_locked",
            "current_role": "machine-readable DESI DR2 Gaussian BAO mirror already used locally",
            "required_refresh_action": "treat as reproducibility mirror unless DESI primary files are hash-matched",
            "fairness_requirement": "document mirror-vs-official status in every scorecard",
            "claim_ceiling": "reproducible BAO compression, not full DESI likelihood ownership",
        },
        {
            "source_key": "DESI_DR1_2024_BAO_comparator",
            "arena": "BAO_release_sensitivity",
            "official_url": "https://github.com/CobayaSampler/bao_data",
            "local_status": "local_hash_locked",
            "current_role": "release-sensitivity comparator against DESI DR2",
            "required_refresh_action": "keep as comparator only; do not mix DR1 and DR2 as independent evidence",
            "fairness_requirement": "same branch definitions and nuisance treatment as DR2",
            "claim_ceiling": "release robustness only",
        },
        {
            "source_key": "CosmicChronometers_CC32_and_Moresco15",
            "arena": "Hz",
            "official_url": "https://cluster.difa.unibo.it/astro/CC_data/",
            "local_status": "source_locked_in_checkpoint_145",
            "current_role": "independent H(z) sensitivity and CC15 covariance primary branch",
            "required_refresh_action": "re-fetch CC32 and CC15 BC03 branch; preserve warning that CC32 lacks full covariance",
            "fairness_requirement": "same H(z) covariance/sensitivity branch applied to all baselines",
            "claim_ceiling": "independent H(z) survivability only",
        },
        {
            "source_key": "SDSS_eBOSS_DR16_BAO_RSD_consensus",
            "arena": "growth_RSD",
            "official_url": "https://svn.sdss.org/public/data/eboss/DR16cosmo/tags/v1_0_1/likelihoods/",
            "local_status": "source_locked_in_checkpoint_146",
            "current_role": "growth/RSD covariance and ELG grid likelihood source",
            "required_refresh_action": "hash-lock SVN files; keep BAO-plus, full-shape-only, and ELG grid separated",
            "fairness_requirement": "same sigma8 nuisance, row vectors, covariances, and jackknifes for MTS and baselines",
            "claim_ceiling": "GR-proxy growth stress test, not perturbation derivation",
        },
        {
            "source_key": "Planck2018_distance_priors_diagnostic",
            "arena": "CMB_diagnostic_only",
            "official_url": "https://arxiv.org/abs/1808.05724",
            "local_status": "local_manifested_but_not_promotion_source",
            "current_role": "compressed-distance diagnostic only",
            "required_refresh_action": "do not use as CMB pass; require Boltzmann-level MTS perturbation before promotion",
            "fairness_requirement": "if used, compare with baselines and retain transfer/joint bridge failures",
            "claim_ceiling": "CMB stress diagnostic only",
        },
    ]


def refresh_stage_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": 0,
            "name": "source_manifest_refresh",
            "purpose": "re-fetch or verify all SN/BAO/H(z)/growth files before scoring",
            "entry_condition": "official target URLs and local paths known",
            "exit_condition": "all required source files have hash locks or are marked unavailable/deferred",
            "failure_action": "stop before fitting; do not score stale or ambiguous files",
        },
        {
            "stage": 1,
            "name": "schema_and_covariance_preflight",
            "purpose": "validate rows, covariance dimensions, positive-definite/symmetric checks, observable conventions",
            "entry_condition": "source hashes locked",
            "exit_condition": "SN, BAO, H(z), and growth shapes pass or are explicitly excluded",
            "failure_action": "write parse failure report and keep prior scorecards unchanged",
        },
        {
            "stage": 2,
            "name": "single_arena_reproduction",
            "purpose": "reproduce existing SN+BAO, BAO-only, H(z), and growth scorecards before adding complexity",
            "entry_condition": "schemas pass",
            "exit_condition": "previous score signs reproduced within tolerance or discrepancy isolated",
            "failure_action": "debug data parsing/nuisance rules before any new claim",
        },
        {
            "stage": 3,
            "name": "baseline_fair_joint_refresh",
            "purpose": "score no-clock MTS against LCDM/wCDM/CPL with identical rows, priors, nuisance parameters, and jackknifes",
            "entry_condition": "single-arena reproduction passes",
            "exit_condition": "delta_chi2/AIC/BIC, residuals, edge flags, and split cards written for every branch",
            "failure_action": "mark branch unstable if edge/prior dependence dominates",
        },
        {
            "stage": 4,
            "name": "official_wrapper_upgrade",
            "purpose": "replace lightweight Gaussian approximations with official likelihood wrappers where feasible",
            "entry_condition": "baseline-fair refresh produces stable source-locked outputs",
            "exit_condition": "wrapper dependency report and reproducibility log exist",
            "failure_action": "keep result as source-locked compression, not official likelihood",
        },
        {
            "stage": 5,
            "name": "long_run_workflow",
            "purpose": "run heavier chains from VS Code terminal without Codex waiting",
            "entry_condition": "dry-run command generation and output contract pass",
            "exit_condition": "runs/<timestamp>/log.txt, status.json, and DONE/FAILED marker written",
            "failure_action": "do not burn tokens watching; user resumes when marker exists",
        },
    ]


def branch_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "LCDM",
            "role": "baseline",
            "fixed_inputs": "standard flat/selected baseline form",
            "fitted_inputs": "Omega_m plus same nuisance/calibration freedoms as MTS",
            "required_outputs": "chi2,AIC,BIC,residuals,edge_flags,jackknife_cards",
            "notes": "no baseline immunity; same punches as MTS",
        },
        {
            "branch": "wCDM",
            "role": "baseline",
            "fixed_inputs": "constant w extension",
            "fitted_inputs": "Omega_m,w plus same nuisance/calibration freedoms as MTS",
            "required_outputs": "chi2,AIC,BIC,residuals,edge_flags,jackknife_cards",
            "notes": "edge hits demote evidence just like for MTS",
        },
        {
            "branch": "CPL",
            "role": "baseline",
            "fixed_inputs": "w0-wa extension",
            "fitted_inputs": "Omega_m,w0,wa plus same nuisance/calibration freedoms as MTS",
            "required_outputs": "chi2,AIC,BIC,residuals,edge_flags,jackknife_cards",
            "notes": "flexible baseline; parameter penalty must be reported",
        },
        {
            "branch": "MTS_2over27_no_clock_u3quarter",
            "role": "lead_branch",
            "fixed_inputs": "B_mem=2/27; u3=1/4; no global clock; no pair projection",
            "fitted_inputs": "Omega_m plus same nuisance/calibration freedoms as baselines",
            "required_outputs": "chi2,AIC,BIC,residuals,edge_flags,jackknife_cards,claim_ceiling",
            "notes": "main empirical lane",
        },
        {
            "branch": "MTS_Bmem_zero",
            "role": "negative_control",
            "fixed_inputs": "B_mem=0 with MTS machinery otherwise off",
            "fitted_inputs": "same as lead branch",
            "required_outputs": "control_comparison",
            "notes": "checks whether effect is actually from frozen memory term",
        },
        {
            "branch": "MTS_pair_ruler_half_kernel",
            "role": "frozen_sidecar",
            "fixed_inputs": "T/2,S/2 sidecar from checkpoint 168",
            "fitted_inputs": "none for lead-lane refresh",
            "required_outputs": "excluded_or_sidecar_only_flag",
            "notes": "must not enter lead refresh unless explicitly sidecar-labelled",
        },
    ]


def baseline_fairness_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "same_rows_and_covariances",
            "requirement": "all branches use identical source rows, masks, covariance blocks, and excluded-row logs",
            "evidence_required": "row_manifest.csv and covariance_manifest.csv",
            "hard_fail_if_missing": "yes",
        },
        {
            "rule": "same_nuisance_freedom",
            "requirement": "SN offset, BAO_alpha/rd convention, sigma8, and H0/calibration choices are symmetric",
            "evidence_required": "nuisance_policy.csv",
            "hard_fail_if_missing": "yes",
        },
        {
            "rule": "same_priors_and_edge_flags",
            "requirement": "all fitted parameters record priors, optimizer bounds, best fits, and edge proximity",
            "evidence_required": "prior_edge_table.csv",
            "hard_fail_if_missing": "yes",
        },
        {
            "rule": "same_jackknife_and_splits",
            "requirement": "every split/jackknife applied to MTS is applied to LCDM, wCDM, CPL, and controls",
            "evidence_required": "jackknife_scorecard.csv",
            "hard_fail_if_missing": "yes",
        },
        {
            "rule": "draw_threshold",
            "requirement": "|DeltaBIC|<2 is a draw; 2-6 is weak/moderate; >6 strong, with context",
            "evidence_required": "baseline_comparisons.csv",
            "hard_fail_if_missing": "no_but_required_for_readout",
        },
        {
            "rule": "claim_ceiling",
            "requirement": "late-time scorecards cannot claim CMB pass, local GR, perturbation derivation, or parent action",
            "evidence_required": "claim_ceiling.txt or status.json",
            "hard_fail_if_missing": "yes",
        },
    ]


def artifact_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "source_hash_lock.csv",
            "purpose": "prove current source bytes and local bytes match expected hashes",
            "required_fields": "source_key,url,local_path,bytes,sha256,status",
        },
        {
            "artifact": "row_manifest.csv",
            "purpose": "prove every branch uses the same rows and masks",
            "required_fields": "arena,row_id,z,observable,include_flag,exclude_reason",
        },
        {
            "artifact": "covariance_manifest.csv",
            "purpose": "prove covariance dimensions, symmetry, positive definiteness, and block ownership",
            "required_fields": "arena,covariance_path,n_rows,shape_status,condition_number",
        },
        {
            "artifact": "branch_manifest.csv",
            "purpose": "freeze model definitions and fixed/fitted parameters before scoring",
            "required_fields": "branch,role,fixed_inputs,fitted_inputs,claim_ceiling",
        },
        {
            "artifact": "fit_summary.csv",
            "purpose": "record scorecard for MTS and baselines",
            "required_fields": "branch,arena,chi2,AIC,BIC,n,k,success,edge_flag",
        },
        {
            "artifact": "baseline_comparisons.csv",
            "purpose": "compare no-clock MTS against LCDM/wCDM/CPL and controls",
            "required_fields": "branch,reference,delta_chi2,delta_AIC,delta_BIC,readout",
        },
        {
            "artifact": "residuals.csv",
            "purpose": "find where wins/losses occur without post-hoc repair",
            "required_fields": "branch,arena,row_id,z,observable,residual,pull",
        },
        {
            "artifact": "jackknife_scorecard.csv",
            "purpose": "prove punches are symmetric across branches",
            "required_fields": "split,branch,reference,delta_BIC,readout",
        },
        {
            "artifact": "status.json",
            "purpose": "machine-readable verdict and claim ceiling",
            "required_fields": "status,claim_ceiling,lead_branch,sidecar_policy,next_target",
        },
    ]


def dry_run_command_rows() -> list[dict[str, Any]]:
    py = WORK_DIR / ".venv-score" / "Scripts" / "python.exe"
    refresh_script = WORK_DIR / "scripts" / "no_clock_official_source_refresh.py"
    score_script = WORK_DIR / "scripts" / "no_clock_official_likelihood_refresh.py"
    return [
        {
            "step": 1,
            "label": "source_refresh_dry_run",
            "command": f'& "{py}" "{refresh_script}" --dry-run --timestamp <timestamp>',
            "creates": "runs/<timestamp>-no-clock-official-source-refresh",
            "long_run": "no",
            "status": "planned_next_script",
        },
        {
            "step": 2,
            "label": "source_refresh_hash_lock",
            "command": f'& "{py}" "{refresh_script}" --timestamp <timestamp>',
            "creates": "source_hash_lock.csv; row_manifest.csv; covariance_manifest.csv",
            "long_run": "no",
            "status": "planned_next_script",
        },
        {
            "step": 3,
            "label": "single_arena_reproduction",
            "command": f'& "{py}" "{score_script}" --mode reproduce --timestamp <timestamp>',
            "creates": "single_arena_reproduction.csv",
            "long_run": "maybe",
            "status": "planned_after_source_lock",
        },
        {
            "step": 4,
            "label": "baseline_fair_refresh",
            "command": f'& "{py}" "{score_script}" --mode full-refresh --timestamp <timestamp>',
            "creates": "fit_summary.csv; baseline_comparisons.csv; residuals.csv; jackknife_scorecard.csv",
            "long_run": "yes_use_VS_Code_workflow",
            "status": "planned_after_reproduction",
        },
        {
            "step": 5,
            "label": "sidecar_exclusion_check",
            "command": f'& "{py}" "{score_script}" --mode manifest-only --assert-no-sidecar --timestamp <timestamp>',
            "creates": "branch_manifest.csv with sidecar excluded/frozen",
            "long_run": "no",
            "status": "planned_guardrail",
        },
    ]


def acceptance_gate_rows(asset_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_count = sum(1 for row in asset_rows if row["exists"] != "yes")
    hash_fail_count = sum(1 for row in asset_rows if row["hash_status"] != "pass")
    return [
        {
            "gate": "local_assets_hash_locked",
            "status": "pass" if missing_count == 0 and hash_fail_count == 0 else "fail",
            "evidence": f"missing={missing_count}; hash_fail={hash_fail_count}; audited_assets={len(asset_rows)}",
        },
        {
            "gate": "official_source_targets_named",
            "status": "pass",
            "evidence": "Pantheon+, DESI DR2 BAO, DESI DR1 comparator, CC H(z), SDSS/eBOSS, and CMB diagnostic sources listed",
        },
        {
            "gate": "no_clock_lead_only",
            "status": "pass",
            "evidence": "refresh branch matrix excludes pair-ruler sidecar from lead scoring",
        },
        {
            "gate": "baseline_fairness_contract",
            "status": "pass",
            "evidence": "same rows/covariances/nuisance/priors/jackknifes required for LCDM/wCDM/CPL/MTS",
        },
        {
            "gate": "dry_run_before_long_run",
            "status": "pass",
            "evidence": "command queue requires dry-run and source-lock before any full refresh",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(asset_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hash_fail_count = sum(1 for row in asset_rows if row["hash_status"] != "pass")
    verdict = STATUS if hash_fail_count == 0 else "no_clock_official_refresh_plan_sources_need_repair"
    return [
        {
            "item": "status",
            "verdict": verdict,
            "evidence": f"local asset hash failures={hash_fail_count}; official-refresh plan written",
        },
        {
            "item": "lead_branch",
            "verdict": "MTS_2over27_no_clock_u3quarter",
            "evidence": "sidecar remains closure-only; no-clock branch is the empirical main lane",
        },
        {
            "item": "sidecar_policy",
            "verdict": "excluded_from_lead_refresh",
            "evidence": "checkpoint 168 did not parent-own the half-kernel factor",
        },
        {
            "item": "baseline_policy",
            "verdict": "same_punches_for_LCDM_wCDM_CPL",
            "evidence": "baseline fairness contract is mandatory before score readout",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no theory/CMB/local-GR/parent-action promotion from likelihood planning",
        },
        {
            "item": "next_target",
            "verdict": "170-no-clock-official-source-refresh-runner.md",
            "evidence": "implement source refresh/hash-lock runner before any new fit",
        },
    ]


def run_plan(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-lead-official-likelihood-refresh-plan"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing_sources = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing_sources:
        raise FileNotFoundError(f"missing required source files: {missing_sources}")

    assets = local_asset_audit_rows()
    targets = official_source_target_rows()
    stages = refresh_stage_rows()
    branches = branch_matrix_rows()
    fairness = baseline_fairness_rows()
    artifacts = artifact_contract_rows()
    commands = dry_run_command_rows()
    gates = acceptance_gate_rows(assets)
    decisions = decision_rows(assets)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_policy": "excluded_from_lead_refresh",
            "web_source_check_date": "2026-05-31",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "local_asset_audit.csv",
        assets,
        [
            "manifest",
            "source_key",
            "kind",
            "url",
            "local_path",
            "exists",
            "expected_sha256",
            "actual_sha256",
            "hash_status",
            "bytes",
            "refresh_role",
        ],
    )
    write_csv(
        results_dir / "official_source_targets.csv",
        targets,
        [
            "source_key",
            "arena",
            "official_url",
            "local_status",
            "current_role",
            "required_refresh_action",
            "fairness_requirement",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "refresh_stage_ladder.csv",
        stages,
        ["stage", "name", "purpose", "entry_condition", "exit_condition", "failure_action"],
    )
    write_csv(
        results_dir / "branch_matrix.csv",
        branches,
        ["branch", "role", "fixed_inputs", "fitted_inputs", "required_outputs", "notes"],
    )
    write_csv(
        results_dir / "baseline_fairness_contract.csv",
        fairness,
        ["rule", "requirement", "evidence_required", "hard_fail_if_missing"],
    )
    write_csv(
        results_dir / "artifact_contract.csv",
        artifacts,
        ["artifact", "purpose", "required_fields"],
    )
    write_csv(
        results_dir / "dry_run_command_queue.csv",
        commands,
        ["step", "label", "command", "creates", "long_run", "status"],
    )
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    write_json(
        run_dir / "status.json",
        {
            "status": decisions[0]["verdict"],
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_policy": "excluded_from_lead_refresh",
            "local_asset_count": len(assets),
            "local_asset_hash_failures": sum(1 for row in assets if row["hash_status"] != "pass"),
            "official_source_targets": len(targets),
            "next_target": "170-no-clock-official-source-refresh-runner.md",
            "generated": [
                "source_register.csv",
                "local_asset_audit.csv",
                "official_source_targets.csv",
                "refresh_stage_ladder.csv",
                "branch_matrix.csv",
                "baseline_fairness_contract.csv",
                "artifact_contract.csv",
                "dry_run_command_queue.csv",
                "acceptance_gates.csv",
                "decision.csv",
            ],
        },
    )
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_plan(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
